"""Read-only Victoria 3 1.15 ship-category audit and optional issue #36 dump probe.

Usage: python issue36_naval_ai_audit.py --mod-root MOD --vanilla-root GAME
Optional: --dump minidump.dmp --exe victoria3.exe
Outputs JSON to stdout only. A passing schema audit is NOT an in-game test.
The dump probe reports measured RTTI/register evidence, not private PDB symbols.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import struct
import sys

TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|\x23[^\n]*|[{}=]|[^\s{}=]+')

def definitions(path, prefix):
    text = path.read_text(encoding="utf-8-sig")
    tokens = [m for m in TOKENS.finditer(text) if not m[0].startswith("#")]
    depth, current, result = 0, None, []
    i = 0
    while i < len(tokens):
        value = tokens[i][0]
        if depth == 0 and value.startswith(prefix) and i + 2 < len(tokens):
            if tokens[i+1][0] == "=" and tokens[i+2][0] == "{":
                current = {"key": value, "line": text.count("\n", 0, tokens[i].start())+1, "fields": []}
        if current and depth == 1 and value == "ai_ship_category":
            if i + 2 < len(tokens) and tokens[i+1][0] == "=":
                current["fields"].append({
                    "category": tokens[i+2][0],
                    "line": text.count("\n", 0, tokens[i].start())+1})
        if value == "{":
            depth += 1
        elif value == "}":
            depth -= 1
            if depth < 0:
                raise ValueError(f"Unbalanced closing brace: {path}")
            if current and depth == 0:
                result.append(current)
                current = None
        i += 1
    if depth != 0:
        raise ValueError(f"Unbalanced braces: {path}")
    return result

def audit(mod, vanilla):
    if not (mod/"common"/"ship_types").is_dir():
        raise ValueError("Mod root must contain common/ship_types")
    if not (vanilla/"common"/"ai_ship_categories").is_dir():
        raise ValueError("Vanilla root must contain 1.15 AI ship categories")
    # This audit models one mod layered over canonical vanilla, by relative path.
    # It does not certify another playset's file order or the game's resolved objects.
    files = {}
    for root in (vanilla, mod):
        for folder in ("ship_types", "ai_ship_categories"):
            for path in sorted((root/"common"/folder).glob("*.txt")):
                files[path.relative_to(root).as_posix()] = path
    categories = set()
    for relative, path in files.items():
        if "/ai_ship_categories/" in relative:
            categories.update(d["key"] for d in definitions(path, "ai_ship_category_"))
    rows, errors, seen = [], [], {}
    for relative, path in sorted(files.items()):
        if "/ship_types/" not in relative:
            continue
        for item in definitions(path, "ship_type_"):
            item.update(file=relative, source=str(path))
            rows.append(item)
            key = item["key"]
            if key in seen:
                errors.append({"key": key, "problem": "duplicate definition", "files": [seen[key], relative]})
            seen[key] = relative
            if len(item["fields"]) != 1:
                errors.append({"key": key, "file": relative, "line": item["line"],
                               "problem": "requires exactly one ai_ship_category", "found": len(item["fields"])})
            elif item["fields"][0]["category"] not in categories:
                errors.append({"key": key, "file": relative, **item["fields"][0],
                               "problem": "undefined ai_ship_category"})
    return {"status": "PASS_STATIC_ONLY" if not errors else "FAIL_STATIC",
            "runtime_tested": False, "ship_types": len(rows),
            "defined_categories": sorted(categories), "errors": errors, "mapping": rows}

def probe(dump_path, exe_path):
    data, exe = dump_path.read_bytes(), exe_path.read_bytes()
    def unpack(fmt, offset):
        return struct.unpack_from("<"+fmt, data, offset)
    if data[:4] != b"MDMP":
        raise ValueError("Not a Microsoft minidump")
    streams = {}
    count, directory = unpack("II", 8)
    for i in range(count):
        kind, size, rva = unpack("III", directory+i*12)
        if rva+size > len(data):
            raise ValueError("Invalid stream bounds")
        streams[kind] = (rva, size)
    modules = []
    offset = streams[4][0]
    for i in range(unpack("I", offset)[0]):
        p = offset+4+i*108
        base, size, checksum, timestamp, name = unpack("QIIII", p)
        length = unpack("I", name)[0]
        modules.append({"base": base, "size": size, "timestamp": timestamp,
                        "name": data[name+4:name+4+length].decode("utf-16le")})
    offset = streams[6][0]
    code = unpack("I", offset+8)[0]
    address = unpack("Q", offset+24)[0]
    parameters = [unpack("Q", offset+40+i*8)[0] for i in range(unpack("I", offset+32)[0])]
    context_size, context = unpack("II", offset+160)
    if context_size < 256:
        raise ValueError("Missing AMD64 register context")
    names = "rax rcx rdx rbx rsp rbp rsi rdi r8 r9 r10 r11 r12 r13 r14 r15 rip".split()
    regs = dict(zip(names, unpack("17Q", context+120)))
    ranges = []
    if 5 in streams:
        offset = streams[5][0]
        for i in range(unpack("I", offset)[0]):
            ranges.append(unpack("QII", offset+4+i*16))
    if 9 in streams:
        offset = streams[9][0]
        count, rva = unpack("QQ", offset)
        for i in range(count):
            base, size = unpack("QQ", offset+16+i*16)
            ranges.append((base, size, rva))
            rva += size
    def memory(address, size):
        for base, length, rva in ranges:
            if base <= address and address+size <= base+length:
                return data[rva+address-base:rva+address-base+size]
        return None
    image = next(m for m in modules if Path(m["name"]).name.lower() == "victoria3.exe")
    def eu(fmt, offset):
        return struct.unpack_from("<"+fmt, exe, offset)
    pe = eu("I", 0x3c)[0]
    if exe[pe:pe+4] != b"PE\0\0":
        raise ValueError("Not a PE image")
    if eu("H", pe+24)[0] != 0x20b:
        raise ValueError("Expected PE32+ image")
    if eu("I", pe+8)[0] != image["timestamp"]:
        raise ValueError("Dump and executable timestamps differ")
    preferred = eu("Q", pe+48)[0]
    sections = []
    for i in range(eu("H", pe+6)[0]):
        p = pe+24+eu("H", pe+20)[0]+i*40
        virtual_size, va, size, raw = eu("IIII", p+8)
        sections.append((va, size, raw))
    def image_bytes(rva, size):
        for va, length, raw in sections:
            if va <= rva and rva+size <= va+length:
                return exe[raw+rva-va:raw+rva-va+size]
        return None
    def rtti(vtable):
        raw = image_bytes(vtable-image["base"]-8, 8)
        if not raw:
            return None
        locator = image_bytes(struct.unpack("<Q", raw)[0]-preferred, 24)
        if not locator:
            return None
        descriptor = struct.unpack_from("<I", locator, 12)[0]
        text = image_bytes(descriptor+16, 240)
        return text.split(b"\0")[0].decode("ascii", errors="replace") if text else None
    fault_bytes = memory(address, 3)
    if fault_bytes != image_bytes(address-image["base"], 3):
        raise ValueError("Dump and executable fault instruction differ")
    def pointer(address):
        raw = memory(address, 8)
        return struct.unpack("<Q", raw)[0] if raw else None
    object_vtable = pointer(regs["rdi"])
    group_allocator = pointer(regs["rbp"]+24)
    corrupt = pointer(regs["rcx"])
    repaired = ((image["base"] & ~0xffffffff) | (corrupt & 0xffffffff)) if corrupt else None
    increments = (corrupt-repaired)//(1<<32) if repaired and corrupt>=repaired else None
    return {
        "scope": "Measured issue #36 evidence; layout offsets specific to this captured build/frame",
        "dump_sha256": hashlib.sha256(data).hexdigest(),
        "exe_sha256": hashlib.sha256(exe).hexdigest(),
        "exception_code": hex(code), "exception_parameters": [hex(v) for v in parameters],
        "fault_rva": hex(address-image["base"]), "fault_bytes": fault_bytes.hex(),
        "rdi_object_rtti": rtti(object_vtable) if object_vtable else None,
        "stack_allocator_rtti": rtti(group_allocator) if group_allocator else None,
        "corrupt_vtable": hex(corrupt) if corrupt else None,
        "candidate_original_vtable": hex(repaired) if repaired else None,
        "candidate_original_rtti": rtti(repaired) if repaired else None,
        "high_dword_increment_difference": increments,
        "inline_array_pointer_matches_allocator_plus_8": pointer(regs["rcx"]-24) == regs["rcx"]+8,
        "interpretation": "A negative category index can increment the high DWORD of the preceding allocator vtable; this is causal inference, not a completed runtime isolation test.",
        "runtime_tested": False}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mod-root", type=Path, required=True)
    parser.add_argument("--vanilla-root", type=Path, required=True)
    parser.add_argument("--dump", type=Path)
    parser.add_argument("--exe", type=Path)
    args = parser.parse_args()
    result = audit(args.mod_root, args.vanilla_root)
    if bool(args.dump) != bool(args.exe):
        parser.error("--dump and --exe must be supplied together")
    if args.dump:
        result["crash_probe"] = probe(args.dump, args.exe)
    print(json.dumps(result, indent=2))
    return 1 if result["errors"] else 0

if __name__ == "__main__":
    sys.exit(main())
