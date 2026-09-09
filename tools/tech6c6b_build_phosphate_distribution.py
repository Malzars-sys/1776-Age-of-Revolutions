"""Build the reviewed TECH6C6B phosphate matrix and apply capped resources."""

from __future__ import annotations

import csv
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_DIR = ROOT / "map_data" / "state_regions"
SOURCE = ROOT / "docs" / "reports" / "industry" / "TECH6C6A_PHOSPHATE_RESOURCE_CANDIDATES.csv"
OUTPUT = ROOT / "docs" / "reports" / "industry" / "TECH6C6B_PHOSPHATE_GLOBAL_RESOURCE_MATRIX.csv"
TIERS = {0: "NONE", 8: "LOW", 16: "MODEST", 24: "MEDIUM", 36: "HIGH", 48: "VERY_HIGH", 60: "WORLD_CLASS"}

# Final exceptions after exact district/state review. All other preliminary positives
# remain unchanged. A zero means the proposed Victoria 3 state mapping was rejected.
OVERRIDES = {
    "STATE_SINAI": 0,
    "STATE_ALGIERS": 0,
    "STATE_CAJAMARCA": 24,
    "STATE_NEJD": 0,
    "STATE_WESTERN_AUSTRALIA": 0,
    "STATE_WEST_KARELIA": 0,
}

SOURCES = {
    "egypt": ("OFFICIAL_EGYPTIAN_SURVEY", "https://emra.gov.eg/ca/about-us"),
    "morocco": ("USGS_DISTRICT_REPORT", "https://pubs.usgs.gov/of/1978/1008/report.pdf"),
    "algeria": ("USGS_MINERALS_YEARBOOK", "https://pubs.usgs.gov/myb/vol3/2017-18/myb3-2017-18-algeria.pdf"),
    "tunisia": ("OFFICIAL_TUNISIAN_MINING_OFFICE", "https://www.onm.nat.tn/en/index.php?p=indminier"),
    "world": ("USGS_WORLD_PHOSPHATE_DATABASE", "https://pubs.usgs.gov/publication/ofr02156"),
    "model": ("USGS_GRADE_TONNAGE_MODEL", "https://pubs.usgs.gov/bul/b1693/html/bull6spx.htm"),
    "usa": ("USGS_FACT_SHEET", "https://pubs.usgs.gov/fs/fs155-99/fs155-99.html"),
    "peru": ("USGS_SECHURA_COORDINATES", "https://pubs.usgs.gov/of/2005/1294/b/OFR2005-1294B.pdf"),
    "brazil": ("USGS_BRAZIL_FACILITIES", "https://pubs.usgs.gov/of/2006/1375/pdf/ofr2006-1375-table.pdf"),
    "saudi": ("USGS_MINERALS_YEARBOOK", "https://pubs.usgs.gov/myb/vol3/2022/myb3-2022-saudi-arabia.pdf"),
    "eurasia": ("USGS_EUROPE_CENTRAL_ASIA_ASSESSMENT", "https://pubs.usgs.gov/of/2005/1294/d/of2005-1294d.pdf"),
    "india": ("USGS_PHOSPHATE_BIBLIOGRAPHY", "https://pubs.usgs.gov/of/1983/0841/report.pdf"),
    "islands": ("USGS_STRATEGIC_PHOSPHATE_INVENTORY", "https://pubs.usgs.gov/circ/1984/0930c/report.pdf"),
    "china": ("USGS_WORLD_DATABASE_AND_CHINA_YEARBOOK", "https://pubs.usgs.gov/of/2002/0156/pdf/OF02-156A.pdf"),
    "vietnam": ("USGS_ASIA_PACIFIC_FACILITIES", "https://pubs.usgs.gov/of/2010/1254/pdf/USGS_ofr2010_1254_table.pdf"),
    "australia": ("GEOSCIENCE_AUSTRALIA", "https://www.ga.gov.au/digital-publication/aimr2019/commodity-summaries"),
}

SOURCE_GROUPS = {
    "egypt": "STATE_UPPER_EGYPT STATE_EGYPTIAN_DESERT STATE_SINAI",
    "morocco": "STATE_MARRAKECH STATE_INNER_MOROCCO",
    "algeria": "STATE_ALGIERS STATE_CONSTANTINE",
    "tunisia": "STATE_TUNISIA",
    "model": "STATE_WEST_SAHARA STATE_SENEGAL STATE_TOGO STATE_TRANSVAAL STATE_BAJA_CALIFORNIA STATE_TRANSJORDAN STATE_PALESTINE STATE_SYRIA STATE_BAGHDAD STATE_DIYARBAKIR",
    "usa": "STATE_IDAHO STATE_TENNESSEE STATE_FLORIDA STATE_NORTH_CAROLINA STATE_UTAH",
    "peru": "STATE_CAJAMARCA",
    "brazil": "STATE_GOIAS STATE_MINAS_GERAIS",
    "saudi": "STATE_NEJD STATE_HAIL",
    "eurasia": "STATE_UZBEKIA STATE_WEST_KARELIA STATE_KOLA STATE_SYRDARYA",
    "india": "STATE_RAJPUTANA",
    "islands": "STATE_INDIAN_OCEAN_TERRITORY STATE_EAST_MICRONESIA STATE_NAURU",
    "china": "STATE_SICHUAN STATE_YUNNAN STATE_GUIZHOU STATE_WESTERN_HUBEI STATE_EASTERN_HUBEI",
    "vietnam": "STATE_TONKIN",
    "australia": "STATE_QUEENSLAND STATE_WESTERN_AUSTRALIA STATE_NORTHERN_TERRITORY",
}

STATE_SOURCE = {
    state: source
    for source, states in SOURCE_GROUPS.items()
    for state in states.split()
}

CHANGE_REASONS = {
    "STATE_SINAI": "Retiré : la source officielle situe les grands phosphates égyptiens dans la vallée du Nil, le désert oriental et la côte de la mer Rouge, pas dans le Sinaï.",
    "STATE_ALGIERS": "Retiré : Djebel Onk est à Tébessa dans l'est algérien, représenté par STATE_CONSTANTINE.",
    "STATE_CAJAMARCA": "Réduit de 36 à 24 : Bayóvar/Sechura est prouvé à Piura, mais STATE_CAJAMARCA n'est qu'une agrégation de jeu voisine.",
    "STATE_NEJD": "Retiré : Al Jalamid, Al Khabra et Umm Wu'al sont dans le nord saoudien, représenté par STATE_HAIL.",
    "STATE_WESTERN_AUSTRALIA": "Retiré : les ressources économiques retenues sont dans le bassin Georgina (Queensland/Territoire du Nord) et l'île Christmas.",
    "STATE_WEST_KARELIA": "Retiré : Khibiny et Kovdor appartiennent à la péninsule de Kola, déjà représentée par STATE_KOLA.",
}


def decode(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    return raw.decode("utf-8-sig"), raw.startswith(b"\xef\xbb\xbf")


def encode(path: Path, text: str, bom: bool) -> None:
    raw = text.encode("utf-8")
    path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + raw)


def state_blocks(text: str) -> list[tuple[str, int, int]]:
    starts = list(re.finditer(r"(?m)^(STATE_[A-Z0-9_]+)\s*=\s*\{", text))
    blocks: list[tuple[str, int, int]] = []
    for match in starts:
        depth = 0
        for pos in range(match.end() - 1, len(text)):
            if text[pos] == "{":
                depth += 1
            elif text[pos] == "}":
                depth -= 1
                if depth == 0:
                    blocks.append((match.group(1), match.start(), pos + 1))
                    break
        else:
            raise RuntimeError(f"Unclosed state block: {match.group(1)}")
    return blocks


def strip_phosphate(text: str) -> str:
    return re.sub(r"(?m)^[ \t]*building_phosphate_mine\s*=\s*\d+[ \t]*(?:\r?\n)?", "", text)


def insert_resource(text: str, start: int, end: int, value: int) -> str:
    block = text[start:end]
    match = re.search(r"(?m)^([ \t]*)capped_resources\s*=\s*\{", block)
    if not match:
        raise RuntimeError("Positive phosphate state has no capped_resources block")
    depth = 0
    close_pos = None
    for pos in range(match.end() - 1, len(block)):
        if block[pos] == "{":
            depth += 1
        elif block[pos] == "}":
            depth -= 1
            if depth == 0:
                close_pos = pos
                break
    if close_pos is None:
        raise RuntimeError("Unclosed capped_resources block")
    newline = "\r\n" if "\r\n" in text else "\n"
    close_line_start = block.rfind(newline, 0, close_pos) + len(newline)
    indent = match.group(1)
    insertion = f"{indent}    building_phosphate_mine = {value}{newline}{indent}"
    return text[: start + close_line_start] + insertion + text[start + close_pos :]


def evidence_for(state_id: str, preliminary_basis: str) -> tuple[str, str, str, str]:
    group = STATE_SOURCE.get(state_id, "world")
    category, url = SOURCES[group]
    final = OVERRIDES.get(state_id)
    if final == 0:
        result = "REJECTED_EXACT_STATE_MAPPING"
        confidence = "HIGH"
    elif state_id == "STATE_CAJAMARCA":
        result = "CONFIRMED_NEIGHBOURING_GAME_AGGREGATION_DOWNGRADED"
        confidence = "MEDIUM"
    else:
        result = "CONFIRMED_DISTRICT_OR_GAME_STATE_AGGREGATION"
        confidence = "HIGH" if group not in {"world", "islands"} else "MEDIUM"
    return result, confidence, category, url


def main() -> None:
    with SOURCE.open(encoding="utf-8-sig", newline="") as stream:
        preliminary = list(csv.DictReader(stream))
    if len(preliminary) != 675 or len({r["state_id"] for r in preliminary}) != 675:
        raise RuntimeError("The TECH6C6A phosphate screen must contain 675 unique states")

    file_cache: dict[Path, tuple[str, bool, list[tuple[str, int, int]], str]] = {}
    state_to_path: dict[str, Path] = {}
    for path in sorted(STATE_DIR.glob("*.txt")):
        original, bom = decode(path)
        stripped = strip_phosphate(original)
        blocks = state_blocks(stripped)
        file_cache[path] = (stripped, bom, blocks, stripped)
        state_to_path.update({state_id: path for state_id, _, _ in blocks})
    if len(state_to_path) != 675:
        raise RuntimeError(f"Expected 675 state regions, found {len(state_to_path)}")

    rows: list[dict[str, object]] = []
    reviewed: dict[str, int] = {}
    positive_review_count = 0
    for row in preliminary:
        state_id = row["state_id"]
        pre = int(row["potential"])
        final = OVERRIDES.get(state_id, pre)
        if pre > 0:
            positive_review_count += 1
            result, confidence, category, url = evidence_for(state_id, row["geological_basis"])
            reason = CHANGE_REASONS.get(state_id, "Confirmé après contrôle du district et de son rattachement à l'État de jeu.")
        else:
            result = "CONFIRMED_ZERO_GLOBAL_SCREEN"
            confidence = row["confidence"]
            category = row["source_category"]
            url = row["source_url"]
            reason = "Aucun district de phosphate de roche à l'échelle du jeu retenu par le criblage mondial."
        if final > 0:
            reviewed[state_id] = final
        rows.append({
            "state_id": state_id,
            "state_region_file": state_to_path[state_id].relative_to(ROOT).as_posix(),
            "preliminary_potential": pre,
            "final_potential": final,
            "final_tier": TIERS[final],
            "implementation_action": "ADD_CAPPED_RESOURCE" if final else "KEEP_ZERO",
            "revalidation_result": result,
            "confidence": confidence,
            "geological_basis": row["geological_basis"],
            "source_category": category,
            "source_url": url,
            "change_reason": reason,
        })
    if positive_review_count != 45:
        raise RuntimeError(f"Expected to revalidate 45 preliminary positives, found {positive_review_count}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    for path, (text, bom, blocks, non_phosphate_before) in file_cache.items():
        changes = [(start, end, reviewed[state_id]) for state_id, start, end in blocks if state_id in reviewed]
        for start, end, value in reversed(changes):
            text = insert_resource(text, start, end, value)
        if strip_phosphate(text) != non_phosphate_before:
            raise RuntimeError(f"Non-phosphate resources changed unexpectedly in {path}")
        encode(path, text, bom)

    counts = Counter(row["final_tier"] for row in rows)
    total = sum(int(row["final_potential"]) for row in rows)
    print(f"states=675 reviewed_preliminary_positives=45 implemented={len(reviewed)} total={total}")
    print("tiers=" + ",".join(f"{tier}:{counts[tier]}" for tier in TIERS.values()))
    print(f"modified_state_files={len({state_to_path[state] for state in reviewed})}")
    print("non_phosphate_resources_preserved=PASS")


if __name__ == "__main__":
    main()
