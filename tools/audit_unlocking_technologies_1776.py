"""Report multi-technology gates; optionally simplify them with --apply."""

from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def masked(text: str) -> str:
    """Blank comments and quoted content while retaining offsets and braces."""
    out = list(text)
    quote = False
    comment = False
    escaped = False
    for i, c in enumerate(text):
        if comment:
            if c == "\n":
                comment = False
            else:
                out[i] = " "
        elif quote:
            out[i] = " "
            if escaped:
                escaped = False
            elif c == "\\":
                escaped = True
            elif c == '"':
                quote = False
        elif c == "#":
            comment = True
            out[i] = " "
        elif c == '"':
            quote = True
            out[i] = " "
    return "".join(out)


def blocks(text: str):
    clean = masked(text)
    pattern = re.compile(r"(?m)^\s*([A-Za-z_][\w.-]*)\s*=\s*\{")
    pos = 0
    while match := pattern.search(clean, pos):
        start = match.end() - 1
        depth = 0
        end = start
        for end in range(start, len(clean)):
            if clean[end] == "{":
                depth += 1
            elif clean[end] == "}":
                depth -= 1
                if depth == 0:
                    break
        if depth:
            raise ValueError(f"Unbalanced definition {match[1]}")
        yield match[1], match.start(), end + 1, clean[match.start() : end + 1]
        pos = end + 1


def gate(block_text: str):
    match = re.search(r"\bunlocking_technologies\s*=\s*\{([^{}]*)\}", block_text)
    return re.findall(r"[A-Za-z_][\w.-]*", match[1]) if match else []


# One technology unlocks each gameplay object. Building gates carry the basic
# access restriction; methods receive the technology for their own process.
OVERRIDES = {
    "pm_combustion_derricks": "combustion_engine",
    "pm_all_metal_aircraft": "military_aviation",
    "pm_atmospheric_engine_pump_building_bauxite_mine": "atmospheric_engine",
    "pm_condensing_engine_pump_building_bauxite_mine": "watertube_boiler",
    "pm_diesel_pump_building_bauxite_mine": "compression_ignition",
    "pm_nitroglycerin_building_bauxite_mine": "nitroglycerin",
    "pm_dynamite_building_bauxite_mine": "dynamite",
    "pm_ore_concentration_building_bauxite_mine": "geological_surveying",
    "pm_steam_donkey_building_bauxite_mine": "steam_donkey",
    "pm_rail_transport_building_bauxite_mine": "railways",
    "pm_steam_mine_ventilation_building_bauxite_mine": "deep_mine_engineering",
    "pm_electric_mine_ventilation_building_bauxite_mine": "electrical_capacitors",
}


if __name__ == "__main__":
    tech_era = {}
    tech_parent = {}
    for file in sorted((ROOT / "common/technology/technologies").glob("*.txt")):
        for key, _, _, body in blocks(file.read_text(encoding="utf-8-sig", errors="replace")):
            era_match = re.search(r"\bera\s*=\s*era_(\d+)", body)
            if era_match:
                tech_era[key] = int(era_match[1])
                tech_parent[key] = gate(body)

    def ancestors(key, seen=None):
        seen = set() if seen is None else seen
        for parent in tech_parent.get(key, []):
            if parent not in seen:
                seen.add(parent)
                ancestors(parent, seen)
        return seen

    found = []
    updates = {}
    for file in sorted((ROOT / "common").rglob("*.txt")):
        if "technology" in file.relative_to(ROOT / "common").parts:
            continue
        content = file.read_text(encoding="utf-8-sig", errors="replace")
        if "unlocking_technologies" not in content:
            continue
        try:
            parsed = list(blocks(content))
        except ValueError as exc:
            print(f"SKIPPED_UNBALANCED={file.relative_to(ROOT)}:{exc}")
            continue
        for key, start, end, body in parsed:
            names = gate(body)
            if len(names) > 1:
                found.append((file.relative_to(ROOT), key, names, start, end))
    for file, key, names, start, end in found:
        latest_era = max(tech_era.get(name, -1) for name in names)
        candidates = [name for name in names if tech_era.get(name, -1) == latest_era]
        candidate = OVERRIDES.get(key, candidates[0] if len(candidates) == 1 else "TIE")
        if candidate not in names:
            raise ValueError(f"Invalid selection {candidate} for {key}")
        redundant = ",".join(name for name in names if candidate != "TIE" and name in ancestors(candidate))
        print(f"{file}|{key}|{','.join(f'{n}:{tech_era.get(n, "?")}' for n in names)}|LATEST={candidate}|ANCESTORS={redundant}")
        if candidate == "TIE":
            raise ValueError(f"Unresolved tie {key}")
        updates.setdefault(ROOT / file, []).append((start, end, key, names, candidate))
    print(f"TOTAL={len(found)}")
    if "--apply" in sys.argv:
        for file, changes in updates.items():
            original = file.read_text(encoding="utf-8-sig", errors="replace")
            edited = original
            for start, end, key, names, choice in sorted(changes, reverse=True):
                block_text = edited[start:end]
                match = re.search(r"(unlocking_technologies\s*=\s*\{)([^{}]*)(\})", block_text)
                if not match or gate(block_text) != names:
                    raise ValueError(f"Unexpected gate while editing {file}:{key}")
                inner = match[2]
                if "\n" in inner:
                    indent = re.search(r"\n([ \t]*)\S", inner)[1]
                    close_indent = re.search(r"\n([ \t]*)$", inner)[1]
                    replacement = f"\n{indent}{choice}\n{close_indent}"
                else:
                    replacement = f" {choice} "
                rewritten = block_text[:match.start(2)] + replacement + block_text[match.end(2):]
                edited = edited[:start] + rewritten + edited[end:]
            if edited != original:
                encoding = "utf-8-sig" if file.read_bytes().startswith(b"\xef\xbb\xbf") else "utf-8"
                file.write_text(edited, encoding=encoding, newline="")
        print(f"FILES_UPDATED={len(updates)}")
