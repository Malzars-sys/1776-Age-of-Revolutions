"""Inspect installed vanilla art and current definitions; write ASSET4 reports only.

No gameplay or texture references are edited. Contact sheets are local research
previews, not originals or redistributable replacement assets.
"""
from collections import Counter
from io import BytesIO
import csv
import hashlib
import json
from pathlib import Path
import re
import struct

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game")
OUT = ROOT / "docs/reports/assets"
TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|\#[^\n]*|\{|\}|=|[^\s{}=#]+')


def pairs(tokens):
    i = 0
    while i + 2 < len(tokens):
        if tokens[i + 1] != "=":
            i += 1
            continue
        key, val = tokens[i], tokens[i + 2]
        if val != "{":
            yield key, val.strip('"')
            i += 3
            continue
        depth, j = 1, i + 3
        while j < len(tokens) and depth:
            depth += (tokens[j] == "{") - (tokens[j] == "}")
            j += 1
        if depth:
            raise ValueError("Unbalanced definition: " + key)
        yield key, tokens[i + 3:j - 1]
        i = j


def field(tokens, name, default=""):
    return next((v for k, v in pairs(tokens) if k == name), default)


def parse(path):
    return [t for t in TOKENS.findall(path.read_text(encoding="utf-8-sig")) if not t.startswith("#")]


def catalog(subdir, native_only=False):
    files = {p.name: p for p in (GAME / subdir).glob("*.txt")}
    if not native_only:
        if subdir == "common/technology/technologies":
            files = {}  # descriptor.mod explicitly replaces this directory.
        files.update({p.name: p for p in (ROOT / subdir).glob("*.txt")})
    result = {}
    for _, path in sorted(files.items()):
        for key, tokens in pairs(parse(path)):
            if isinstance(tokens, list):
                result[key] = (tokens, path)
    return result


def locs(language):
    result = {}
    for base in (GAME, ROOT):
        folder = base / "localization" / language
        paths = sorted(folder.rglob("*.yml"), key=lambda p: ("replace" in p.relative_to(folder).parts, str(p)))
        for path in paths:
            for key, text in re.findall(r'^\s*([\w.\-]+):\d*\s+"((?:\\.|[^"\\])*)"', path.read_text(encoding="utf-8-sig"), re.M):
                result[key] = text
    return result


def resolve(relative):
    if (ROOT / relative).is_file():
        return ROOT / relative
    if (GAME / relative).is_file():
        return GAME / relative
    return None


def state(relative):
    path = resolve(relative)
    if not relative:
        return "NO_EXPLICIT_VISUAL"
    if not path:
        return "MISSING_FILE"
    if re.search(r"(?:^|/)error_[^/]+\.dds$", relative):
        return "PLACEHOLDER"
    if path.is_relative_to(GAME):
        return "VANILLA_REFERENCE_NOT_SEMANTICALLY_VALIDATED"
    return "LOCAL_EXISTING_PROVENANCE_AND_SUBJECT_TO_REVIEW"


def header(path):
    with path.open("rb") as stream:
        data = stream.read(148)
    if data[:4] != b"DDS ":
        return {"error": "Not DDS"}
    h, w = struct.unpack_from("<II", data, 12)
    fourcc = data[84:88].decode("ascii", errors="replace").strip("\0")
    dxgi = struct.unpack_from("<I", data, 128)[0] if fourcc == "DX10" else None
    return {"width": w, "height": h, "mips": struct.unpack_from("<I", data, 28)[0],
            "format": "DXGI:" + str(dxgi) if dxgi else fourcc or "RGB/RGBA:" + str(struct.unpack_from("<I", data, 88)[0])}


def decode(path):
    data = bytearray(path.read_bytes())
    if data[84:88] == b"DX10":
        dxgi = struct.unpack_from("<I", data, 128)[0]
        aliases = {99: 98, 72: 71, 75: 74, 78: 77, 29: 28}
        if dxgi in aliases:
            struct.pack_into("<I", data, 128, aliases[dxgi])
    return Image.open(BytesIO(data)).convert("RGBA")


def csvout(name, rows):
    if not rows:
        raise ValueError("Empty report: " + name)
    with (OUT / name).open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main():
    fr = locs("french")
    native = {kind: catalog(folder, True) for kind, folder in {
        "TECH": "common/technology/technologies", "GOOD": "common/goods",
        "BUILDING": "common/buildings", "PM": "common/production_methods"}.items()}
    current = {kind: catalog(folder) for kind, folder in {
        "TECH": "common/technology/technologies", "GOOD": "common/goods", "BUILDING": "common/buildings",
        "PM": "common/production_methods", "PMG": "common/production_method_groups", "UNIT": "common/combat_unit_types", "SHIP": "common/ship_types"}.items()}
    used_groups = {pmg for tokens, _ in current["BUILDING"].values() for pmg in field(tokens, "production_method_groups", [])}
    used_pms = {pm for pmg in used_groups if pmg in current["PMG"] for pm in field(current["PMG"][pmg][0], "production_methods", [])}
    rows, variants = [], []
    for kind in ("TECH", "GOOD", "BUILDING", "PM", "UNIT", "SHIP"):
        for key, (tokens, source) in sorted(current[kind].items()):
            if kind == "PM" and key not in used_pms:
                continue
            if kind == "TECH" and field(tokens, "can_research") == "no":
                continue
            if kind == "UNIT":
                paths = []
                for variant, (name, image) in enumerate((p for p in pairs(tokens) if p[0] == "combat_unit_image"), 1):
                    texture = field(image, "texture")
                    paths.append(texture)
                    trigger = field(image, "trigger", [])
                    variants.append({"unit": key, "name_fr": fr.get(key, key), "variant": variant,
                                     "culture_condition": " ".join(trigger) if trigger else "FALLBACK",
                                     "texture": texture, "status": state(texture), "definition": str(source.relative_to(ROOT) if source.is_relative_to(ROOT) else source.relative_to(GAME))})
            elif kind == "SHIP":
                paths = [field(tokens,"icon"), field(tokens,"profile_texture")]
            else:
                paths = [field(tokens, "icon" if kind == "BUILDING" else "texture")]
            statuses = sorted({state(p) for p in paths}) or ["NO_EXPLICIT_VISUAL"]
            status = next((s for s in ("PLACEHOLDER", "MISSING_FILE", "NO_EXPLICIT_VISUAL") if s in statuses), "|".join(statuses))
            rows.append({"type": kind, "id": key, "name_fr": fr.get(key, key),
                         "category_or_group": field(tokens, "category") or field(tokens, "building_group") or field(tokens, "group") or field(tokens,"ship_group"),
                         "era": field(tokens, "era"), "technologies": "|".join(field(tokens, "unlocking_technologies", [])),
                         "textures": "|".join(dict.fromkeys(paths)), "status": status,
                         "direct_copper_exclusion": "YES" if "copper" in key or "copper" in source.name else "NO",
                         "definition": str(source.relative_to(ROOT) if source.is_relative_to(ROOT) else source.relative_to(GAME)),
                         "definition_origin": "MOD" if source.is_relative_to(ROOT) else "VANILLA"})
    csvout("ASSET4_CURRENT_VISUAL_INVENTORY_2026-10-01.csv", rows)
    csvout("ASSET4_UNIT_VISUAL_INVENTORY_2026-10-01.csv", variants)

    subjects = {
        "TECH": ["mechanical_tools", "steelworking", "intensive_agriculture", "rationalism", "academia", "rifling", "artillery", "electrical_generation"],
        "GOOD": ["coal", "iron", "steel", "tools", "fertilizer", "sulfur", "glass", "paper"],
        "BUILDING": ["building_coal_mine", "building_iron_mine", "building_chemical_plant", "building_glassworks", "building_steel_mill", "building_university", "building_arms_industry", "building_artillery_foundry"],
        "PM": ["pm_picks_and_shovels_building_coal_mine", "pm_atmospheric_engine_pump_building_coal_mine", "pm_nitroglycerin_building_coal_mine", "pm_dynamite_building_coal_mine", "pm_bessemer_process", "pm_open_hearth_process", "pm_philosophy_department", "pm_automatic_power_looms"]}
    refs = []
    font_path = Path(r"C:\Windows\Fonts\segoeui.ttf")
    font = ImageFont.truetype(str(font_path), 15) if font_path.is_file() else ImageFont.load_default()
    small = ImageFont.truetype(str(font_path), 12) if font_path.is_file() else font
    sheet = Image.new("RGB", (8 * 182, 4 * 258), "#292a2c")
    draw = ImageDraw.Draw(sheet)
    for row_index, (kind, ids) in enumerate(subjects.items()):
        for column, key in enumerate(ids):
            if key not in native[kind]:
                raise KeyError("Native style reference missing: " + key)
            tokens, _ = native[kind][key]
            relative = field(tokens, "icon" if kind == "BUILDING" else "texture")
            path = GAME / relative
            icon = decode(path)
            x, y = column * 182, row_index * 258
            large = icon.copy()
            large.thumbnail((156, 156), Image.Resampling.LANCZOS)
            sheet.paste(large, (x + (182-large.width)//2, y+6+(156-large.height)//2), large)
            tiny = icon.copy()
            tiny.thumbnail((32,32), Image.Resampling.LANCZOS)
            for offset, bg in ((18,"#423b2e"),(66,"#d8d1c1")):
                draw.rectangle((x+offset,y+170,x+offset+35,y+205),fill=bg)
                sheet.paste(tiny,(x+offset+(36-tiny.width)//2,y+170+(36-tiny.height)//2),tiny)
            draw.text((x+8,y+214), kind, font=font, fill="white")
            label = path.stem
            draw.text((x+8,y+237), label[:24], font=small, fill="#dddddd")
            a = icon.getchannel("A")
            refs.append({"family":kind,"id":key,"texture":relative,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                         **header(path),"alpha_min":a.getextrema()[0],"alpha_max":a.getextrema()[1]})
    sheet.save(OUT / "ASSET4_VANILLA_FOUR_FAMILIES_REFERENCE.png")
    unit_refs = ["infantry_eu_irregular", "infantry_eu_line", "artillery_eu_cannon", "artillery_eu_mobile", "cavalry_eu_hussar", "cavalry_eu_cuirassier"]
    unit_sheet = Image.new("RGB", (6*250,330), "#292a2c")
    unit_draw = ImageDraw.Draw(unit_sheet)
    for column, key in enumerate(unit_refs):
        relative = "gfx/unit_illustrations/" + key + ".dds"
        path = GAME / relative
        icon = decode(path)
        original = icon.size
        icon.thumbnail((230,250),Image.Resampling.LANCZOS)
        unit_sheet.paste(icon,(column*250+(250-icon.width)//2,8+(250-icon.height)//2),icon)
        unit_draw.text((column*250+6,270),key,font=font,fill="white")
        unit_draw.text((column*250+6,295),str(original),font=font,fill="#cccccc")
        refs.append({"family":"UNIT","id":key,"texture":relative,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),**header(path),
                     "alpha_min":icon.getchannel("A").getextrema()[0],"alpha_max":icon.getchannel("A").getextrema()[1]})
    unit_sheet.save(OUT / "ASSET4_VANILLA_UNIT_REFERENCE.png")
    csvout("ASSET4_VANILLA_REFERENCE_METADATA.csv",refs)
    technical = {}
    for kind, folder in {"TECH":"gfx/interface/icons/invention_icons","GOOD":"gfx/interface/icons/goods_icons",
                         "BUILDING":"gfx/interface/icons/building_icons","PM":"gfx/interface/icons/production_method_icons","UNIT":"gfx/unit_illustrations"}.items():
        counts = Counter()
        for path in (GAME/folder).glob("*.dds"):
            info = header(path)
            counts[f'{info["width"]}x{info["height"]}; mips={info["mips"]}; {info["format"]}'] += 1
        technical[kind] = dict(counts.most_common())
    batch = json.loads((OUT/"ASSET4_FIRST_BATCH_2026-10-01.json").read_text(encoding="utf-8"))
    indexed = {(r["type"],r["id"]):r for r in rows}
    batch_rows = []
    for item in batch["assets"]:
        row = indexed[(item["family"],item["id"])]
        if row["direct_copper_exclusion"] != "NO":
            raise ValueError("Copper subject entered the excluded batch: " + item["id"])
        if resolve(item["target_dds"]):
            raise ValueError("Proposed output already exists: " + item["target_dds"])
        batch_rows.append({**item,"current_texture":row["textures"],"current_status":row["status"],"definition":row["definition"]})
    if len(batch_rows) != 14 or len({r["target_dds"] for r in batch_rows}) != 14:
        raise ValueError("First batch must contain 14 distinct outputs")
    if Counter(r["family"] for r in batch_rows) != Counter({"TECH":2,"GOOD":2,"BUILDING":2,"PM":5,"UNIT":3}):
        raise ValueError("First batch family counts differ from brief")
    csvout("ASSET4_FIRST_BATCH_2026-10-01.csv",batch_rows)
    summary = {"date":"2026-10-01","game":str(GAME),"scope":"Resolvable definitions, reachable PMs and ship types; not runtime visibility or artistic approval",
               "objects":dict(Counter(r["type"] for r in rows)),"placeholders":dict(Counter(r["type"] for r in rows if r["status"]=="PLACEHOLDER")),
               "missing_files":dict(Counter(r["type"] for r in rows if r["status"]=="MISSING_FILE")),
               "unit_placeholders":[r for r in variants if r["status"] in ("PLACEHOLDER","MISSING_FILE")],
               "native_main_directory_dds_formats":technical,"reference_count":len(refs),"first_batch_outputs":len(batch_rows),"first_batch_pilots":[r["id"] for r in batch_rows if r["stage"]=="PILOT"]}
    (OUT/"ASSET4_AUDIT_SUMMARY_2026-10-01.json").write_text(json.dumps(summary,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(summary,ensure_ascii=False,indent=2))


if __name__ == "__main__":
    main()
