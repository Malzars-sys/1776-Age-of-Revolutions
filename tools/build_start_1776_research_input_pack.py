#!/usr/bin/env python3
"""Build the technical input pack for the future 1776 starting-building audit.

This script is read-only with respect to gameplay data. It derives its outputs
from the current working tree and Victoria 3 1.13.11, then writes only reports.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VANILLA = Path(r"C:\Games\Victoria 3\game")
OUT = ROOT / "docs" / "reports" / "buildings"

REGION_BY_FILE = {
    "00_west_europe.txt": "R1_WESTERN_EUROPE",
    "01_south_europe.txt": "R1_WESTERN_EUROPE",
    "02_east_europe.txt": "R2_NORTHERN_CENTRAL_EASTERN_EUROPE",
    "03_north_africa.txt": "R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA",
    "04_subsaharan_africa.txt": "R7_SUBSAHARAN_AFRICA",
    "05_north_america.txt": "R8_NORTH_AMERICA_CARIBBEAN",
    "06_central_america.txt": "R8_NORTH_AMERICA_CARIBBEAN",
    "07_south_america.txt": "R9_SOUTH_AMERICA",
    "08_middle_east.txt": "R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA",
    "09_central_asia.txt": "R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA",
    "10_india.txt": "R4_SOUTH_ASIA",
    "11_east_asia.txt": "R5_EAST_ASIA",
    "12_indonesia.txt": "R6_SOUTHEAST_ASIA_OCEANIA",
    "13_australasia.txt": "R6_SOUTHEAST_ASIA_OCEANIA",
    "14_siberia.txt": "R5_EAST_ASIA",
    "15_russia.txt": "R2_NORTHERN_CENTRAL_EASTERN_EUROPE",
}

VIETNAM_REWORK_STATES = {
    "STATE_CAMBODIA",
    "STATE_TONKIN",
    "STATE_ANNAM",
    "STATE_MEKONG",
    "STATE_LAOS",
}

AUTO_BUILDINGS = {
    "building_urban_center",
    "building_manor_house",
    "building_financial_district",
    "building_subsistence_farm",
    "building_subsistence_orchards",
    "building_subsistence_pastures",
    "building_subsistence_fishing_villages",
}

POST_1776_BUILDINGS = {
    "building_big_ben",
    "building_capitol_hill",
    "building_central_park",
    "building_cristo_redentor",
    "building_eiffel_tower",
    "building_estacion_de_madrid_atocha",
    "building_gran_teatro_de_la_habana",
    "building_kaiserforum_1",
    "building_kaiserforum_2",
    "building_kaiserforum_3",
    "building_kaiserforum_4",
    "building_manila_cathedral_monument",
    "building_mosque_of_djenne",
    "building_pena_palace",
    "building_sagrada_familia_cathedral_1",
    "building_sagrada_familia_cathedral_2",
    "building_sagrada_familia_cathedral_3",
    "building_skyscraper",
    "building_statue_of_liberty",
    "building_victoria_terminus",
    "building_white_house",
}

SPECIAL_SYSTEM_BUILDINGS = {
    "building_halloween_castledracula",
    "building_manila_cathedral_ruins",
    "building_power_bloc_statue",
}

# These map-only monuments deliberately inherit building_dummy in vanilla.
# The report needs usable labels, without changing the game's localization.
DUMMY_DISPLAY_NAMES = {
    "building_argebam": ("Arg-e Bam", "Citadelle de Bam"),
    "building_capitol_hill": ("Capitol Hill", "Capitole des États-Unis"),
    "building_central_park": ("Central Park", "Central Park"),
    "building_chichen_itza": ("Chichén Itzá", "Chichén Itzá"),
    "building_easter_island_heads": ("Easter Island Moai", "Moaï de l’île de Pâques"),
    "building_eye_of_sahara": ("Eye of the Sahara", "Œil du Sahara"),
    "building_giza_necropolis": ("Giza Necropolis", "Nécropole de Gizeh"),
    "building_khaju_bridge": ("Khaju Bridge", "Pont Khaju"),
    "building_machu_picchu": ("Machu Picchu", "Machu Picchu"),
    "building_martandsuntemple": ("Martand Sun Temple", "Temple du Soleil de Martand"),
    "building_observatorygreenwich": ("Royal Observatory Greenwich", "Observatoire royal de Greenwich"),
    "building_petra": ("Petra", "Pétra"),
    "building_temple_of_poseidon": ("Temple of Poseidon", "Temple de Poséidon"),
    "building_wat_arun": ("Wat Arun", "Wat Arun"),
}


@dataclass
class Block:
    object_id: str
    text: str
    source: Path
    line: int


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="ignore")


def clean_comments(text: str) -> str:
    out: list[str] = []
    quoted = False
    escaped = False
    comment = False
    for ch in text:
        if comment:
            if ch == "\n":
                comment = False
                out.append(ch)
            else:
                out.append(" ")
            continue
        if quoted:
            out.append(ch)
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
            out.append(ch)
        elif ch == "#":
            comment = True
            out.append(" ")
        else:
            out.append(ch)
    return "".join(out)


def brace_maps(text: str) -> tuple[list[int], dict[int, int]]:
    depths = [0] * (len(text) + 1)
    stack: list[int] = []
    pairs: dict[int, int] = {}
    depth = 0
    quoted = False
    escaped = False
    for index, ch in enumerate(text):
        depths[index] = depth
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == '"':
            quoted = True
        elif ch == "{":
            stack.append(index)
            depth += 1
        elif ch == "}":
            depth -= 1
            if not stack or depth < 0:
                raise ValueError("Unbalanced closing brace")
            pairs[stack.pop()] = index
    depths[len(text)] = depth
    if depth or stack:
        raise ValueError("Unbalanced braces")
    return depths, pairs


def named_blocks(path: Path, identifier: str, target_depth: int) -> list[Block]:
    raw = read(path)
    text = clean_comments(raw)
    depths, pairs = brace_maps(text)
    pattern = re.compile(rf"(?m)^[ \t]*(?P<id>{identifier})[ \t]*=[ \t]*\{{")
    result: list[Block] = []
    for match in pattern.finditer(text):
        if depths[match.start()] != target_depth:
            continue
        opening = text.find("{", match.start(), match.end())
        closing = pairs[opening]
        object_id = match.group("id").replace("REPLACE_OR_CREATE:", "")
        result.append(Block(object_id, raw[match.start() : closing + 1], path, raw.count("\n", 0, match.start()) + 1))
    return result


def subblocks(block: Block, identifier: str, target_depth: int = 1) -> list[Block]:
    temp = clean_comments(block.text)
    depths, pairs = brace_maps(temp)
    pattern = re.compile(rf"(?m)^[ \t]*(?P<id>{identifier})[ \t]*=[ \t]*\{{")
    result: list[Block] = []
    for match in pattern.finditer(temp):
        if depths[match.start()] != target_depth:
            continue
        opening = temp.find("{", match.start(), match.end())
        closing = pairs[opening]
        line = block.line + block.text.count("\n", 0, match.start())
        result.append(Block(match.group("id"), block.text[match.start() : closing + 1], block.source, line))
    return result


def scalar(text: str, key: str, default: str = "") -> str:
    match = re.search(rf"(?m)^[ \t]*{re.escape(key)}[ \t]*=[ \t]*(?:\"([^\"]*)\"|([^\s#\}}]+))", clean_comments(text))
    return (match.group(1) or match.group(2)) if match else default


def braced_tokens(text: str, key: str) -> list[str]:
    cleaned = clean_comments(text)
    match = re.search(rf"(?m)^[ \t]*{re.escape(key)}[ \t]*=[ \t]*\{{", cleaned)
    if not match:
        return []
    opening = cleaned.find("{", match.start(), match.end())
    _, pairs = brace_maps(cleaned)
    content = cleaned[opening + 1 : pairs[opening]]
    return re.findall(r'"([^\"]+)"|([A-Za-z0-9_:.\-]+)', content)


def tokens_flat(values: list[tuple[str, str]]) -> list[str]:
    return [left or right for left, right in values]


def relative_source(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return "VANILLA/" + path.relative_to(VANILLA).as_posix()


def effective_objects(relative: str, identifier: str, mod_only: bool = False) -> dict[str, Block]:
    objects: dict[str, Block] = {}
    roots = [] if mod_only else [VANILLA / relative]
    roots.append(ROOT / relative)
    for folder in roots:
        if not folder.exists():
            continue
        for path in sorted(folder.glob("*.txt"), key=lambda item: item.name.lower()):
            for block in named_blocks(path, identifier, 0):
                objects[block.object_id] = block
    return objects


def localizations(language: str) -> dict[str, str]:
    result: dict[str, str] = {}
    roots = [VANILLA / "localization" / language, ROOT / "localization" / language]
    for root in roots:
        if not root.exists():
            continue
        normal = [path for path in root.rglob("*.yml") if "replace" not in path.parts]
        replacement = [path for path in root.rglob("*.yml") if "replace" in path.parts]
        for path in sorted(normal) + sorted(replacement):
            for line in read(path).splitlines():
                match = re.match(r'^\s*([^\s:#]+):(?:\d+)?\s+"(.*?)"\s*(?:#.*)?$', line)
                if match:
                    result[match.group(1)] = match.group(2).replace('\\"', '"')
    return result


def parse_map_regions() -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    for path in sorted((ROOT / "map_data" / "state_regions").glob("*.txt")):
        research_region = REGION_BY_FILE.get(path.name, "R5_EAST_ASIA")
        for block in named_blocks(path, r"STATE_[A-Za-z0-9_]+", 0):
            ports = re.findall(r'(?m)^\s*port\s*=\s*"?([A-Za-z0-9_]+)"?', clean_comments(block.text))
            result[block.object_id] = {
                "source": path,
                "research_region": research_region,
                "ports": set(ports),
                "coastal": bool(ports or scalar(block.text, "naval_exit_id")),
                "block": block,
            }
    return result


def parse_state_owners() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in sorted((ROOT / "common" / "history" / "states").glob("*.txt")):
        for state in named_blocks(path, r"s:STATE_[A-Za-z0-9_]+", 1):
            state_id = state.object_id.removeprefix("s:")
            homelands = re.findall(r"(?m)^\s*add_homeland\s*=\s*(?:cu:)?([A-Za-z0-9_]+)", clean_comments(state.text))
            claims = re.findall(r"(?m)^\s*add_claim\s*=\s*(?:c:)?([A-Za-z0-9_]+)", clean_comments(state.text))
            for created in subblocks(state, "create_state"):
                country = scalar(created.text, "country").removeprefix("c:")
                provinces = set(tokens_flat(braced_tokens(created.text, "owned_provinces")))
                rows.append(
                    {
                        "state": state_id,
                        "owner": country,
                        "provinces": provinces,
                        "homelands": homelands,
                        "claims": claims,
                        "source": path,
                        "line": created.line,
                    }
                )
    return rows


def parse_populations() -> dict[tuple[str, str], int]:
    result: dict[tuple[str, str], int] = defaultdict(int)
    for path in sorted((ROOT / "common" / "history" / "pops").glob("*.txt")):
        for state in named_blocks(path, r"s:STATE_[A-Za-z0-9_]+", 1):
            state_id = state.object_id.removeprefix("s:")
            for region_state in subblocks(state, r"region_state:[A-Za-z0-9_]+"):
                tag = region_state.object_id.split(":", 1)[1]
                result[(state_id, tag)] += sum(int(value) for value in re.findall(r"(?m)^\s*size\s*=\s*(\d+)", clean_comments(region_state.text)))
    return result


def parse_current_buildings() -> list[dict[str, object]]:
    combined: dict[tuple[str, str, str], dict[str, object]] = {}
    for path in sorted((ROOT / "common" / "history" / "buildings").glob("*.txt")):
        for state in named_blocks(path, r"s:STATE_[A-Za-z0-9_]+", 1):
            state_id = state.object_id.removeprefix("s:")
            for region_state in subblocks(state, r"region_state:[A-Za-z0-9_]+"):
                tag = region_state.object_id.split(":", 1)[1]
                for created in subblocks(region_state, "create_building"):
                    building = scalar(created.text, "building")
                    levels = sum(int(value) for value in re.findall(r"\blevels\s*=\s*(\d+)", clean_comments(created.text)))
                    if not levels:
                        levels = int(scalar(created.text, "level", "0") or 0)
                    pms = tokens_flat(braced_tokens(created.text, "activate_production_methods"))
                    key = (tag, state_id, building)
                    row = combined.setdefault(
                        key,
                        {"owner": tag, "state": state_id, "building": building, "level": 0, "pms": set(), "sources": []},
                    )
                    row["level"] += levels
                    row["pms"].update(pms)
                    row["sources"].append(f"{relative_source(path)}:{created.line}")
    return sorted(combined.values(), key=lambda row: (row["owner"], row["state"], row["building"]))


def group_ancestry(group_id: str, groups: dict[str, Block]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    current = group_id
    while current and current not in seen:
        result.append(current)
        seen.add(current)
        current = scalar(groups.get(current, Block("", "", ROOT, 0)).text, "parent_group")
    return result


def building_category(building_id: str, group_id: str, ancestry: list[str]) -> str:
    joined = " ".join([building_id, group_id, *ancestry])
    if building_id == "building_trade_center":
        return "TRADE_CENTER"
    if building_id == "building_port":
        return "PORT"
    if building_id in {"building_railway", "building_construction_sector"} or "infrastructure" in joined:
        return "INFRASTRUCTURE"
    if "ship_construction" in joined or "shipyard" in joined:
        return "SHIPBUILDING"
    if "military" in joined or building_id in {"building_barracks", "building_conscription_center"}:
        return "MILITARY"
    if building_id == "building_university" or "education" in joined:
        return "EDUCATION"
    if building_id == "building_government_administration" or "administration" in joined:
        return "ADMINISTRATION"
    if "plantation" in joined:
        return "PLANTATION"
    if any(word in joined for word in ("mining", "mine", "logging", "fishing", "whaling", "oil", "rubber", "resource", "gold")):
        return "RESOURCE_EXTRACTION"
    if "agriculture" in joined or "farm" in joined or "ranch" in joined:
        return "AGRICULTURE_COMMERCIAL"
    if building_id == "building_power_plant" or any(word in joined for word in ("manufacturing", "industry", "industries", "arts")):
        return "MANUFACTURING"
    return "OTHER"


def map_risk(state_id: str, research_region: str) -> str:
    if research_region == "R4_SOUTH_ASIA":
        return "INDIA_FUTURE_REWORK"
    if state_id in VIETNAM_REWORK_STATES:
        return "VIETNAM_FUTURE_REWORK"
    return "NONE"


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    en = localizations("english")
    fr = localizations("french")
    map_regions = parse_map_regions()
    owners = parse_state_owners()
    populations = parse_populations()
    raw_current_buildings = parse_current_buildings()
    valid_owner_states = {(str(row["owner"]), str(row["state"])) for row in owners}
    orphan_current_buildings = [
        row for row in raw_current_buildings
        if (str(row["owner"]), str(row["state"])) not in valid_owner_states
    ]
    current_buildings = [
        row for row in raw_current_buildings
        if (str(row["owner"]), str(row["state"])) in valid_owner_states
    ]

    state_rows: list[dict[str, object]] = []
    for item in owners:
        state_id = str(item["state"])
        owner = str(item["owner"])
        region_data = map_regions.get(state_id, {})
        research_region = str(region_data.get("research_region", "R5_EAST_ASIA"))
        ports = region_data.get("ports", set())
        excluded = "YES" if owner in {"VEN", "GEN"} else "NO"
        homeland_core = []
        if item["homelands"]:
            homeland_core.append("Homelands=" + "|".join(sorted(set(item["homelands"]))))
        if item["claims"]:
            homeland_core.append("Claims=" + "|".join(sorted(set(item["claims"]))))
        source_parts = [f"{relative_source(item['source'])}:{item['line']}"]
        if region_data:
            source_parts.append(f"{relative_source(region_data['source'])}:{region_data['block'].line}")
        state_rows.append(
            {
                "State_ID": state_id,
                "State_Display_Name": en.get(state_id, state_id),
                "Region": research_region,
                "Owner_TAG": owner,
                "Owner_Name": en.get(owner, owner),
                "Homeland_or_Core_Info": "; ".join(homeland_core),
                "Coastal": "YES" if region_data.get("coastal") else "NO",
                "Has_Port_Access": "YES" if set(item["provinces"]) & set(ports) else "NO",
                "Current_Population": populations.get((state_id, owner), 0),
                "Excluded_Serenissima": excluded,
                "Map_Rework_Risk": map_risk(state_id, research_region),
                "Source_File": "; ".join(source_parts),
            }
        )
    state_rows.sort(key=lambda row: (row["Region"], row["State_ID"], row["Owner_TAG"]))
    write_csv(
        OUT / "BUILD_START_1776_STATE_CATALOG.csv",
        [
            "State_ID", "State_Display_Name", "Region", "Owner_TAG", "Owner_Name",
            "Homeland_or_Core_Info", "Coastal", "Has_Port_Access", "Current_Population",
            "Excluded_Serenissima", "Map_Rework_Risk", "Source_File",
        ],
        state_rows,
    )

    current_rows: list[dict[str, object]] = []
    for row in current_buildings:
        excluded = "YES" if row["owner"] in {"VEN", "GEN"} else "NO"
        note = []
        if row["building"] == "building_trade_center":
            note.append("MANUAL_1.13_TRADE_CAPACITY_SEED")
        if row["building"] == "building_railway":
            note.append("TECH7A_UNIFIED_ROAD_CANAL_RAIL_BUILDING")
        if excluded == "YES":
            note.append("EXCLUDED_FROM_GENERAL_REDISTRIBUTION")
        current_rows.append(
            {
                "Owner_TAG": row["owner"],
                "State_ID": row["state"],
                "Building_ID": row["building"],
                "Current_Level": row["level"],
                "Current_PM_Overrides": "|".join(sorted(row["pms"])),
                "Source_File": "|".join(source.split(":", 1)[0] for source in row["sources"]),
                "Source_Line_or_Block": "|".join(row["sources"]),
                "Excluded_Serenissima": excluded,
                "Notes": "; ".join(note),
            }
        )
    write_csv(
        OUT / "BUILD_START_1776_CURRENT_BUILDINGS.csv",
        [
            "Owner_TAG", "State_ID", "Building_ID", "Current_Level", "Current_PM_Overrides",
            "Source_File", "Source_Line_or_Block", "Excluded_Serenissima", "Notes",
        ],
        current_rows,
    )

    buildings = effective_objects("common/buildings", r"building_[A-Za-z0-9_]+")
    groups = effective_objects("common/building_groups", r"bg_[A-Za-z0-9_]+")
    pmgs = effective_objects("common/production_method_groups", r"(?:REPLACE_OR_CREATE:)?pmg_[A-Za-z0-9_]+")
    pms = effective_objects("common/production_methods", r"pm_[A-Za-z0-9_]+")
    techs = effective_objects("common/technology/technologies", r"[A-Za-z0-9_]+", mod_only=True)
    placed = {str(row["building"]) for row in current_buildings}

    building_rows: list[dict[str, object]] = []
    for building_id, block in sorted(buildings.items()):
        group_id = scalar(block.text, "building_group")
        ancestry = group_ancestry(group_id, groups)
        category = building_category(building_id, group_id, ancestry)
        group = groups.get(group_id)
        group_auto = bool(group and scalar(group.text, "auto_place_buildings") == "yes")
        is_auto = (
            building_id in AUTO_BUILDINGS
            or building_id.startswith("building_subsistence_")
            or building_id == "building_conscription_center"
            or group_auto
            or "bg_subsistence" in ancestry
            or "bg_owner_buildings" in ancestry
        )
        gates = tokens_flat(braced_tokens(block.text, "unlocking_technologies"))
        pmg_ids = tokens_flat(braced_tokens(block.text, "production_method_groups"))
        base_pms: list[str] = []
        inputs: set[str] = set()
        outputs: set[str] = set()
        pm_techs: set[str] = set()
        for pmg_id in pmg_ids:
            pmg = pmgs.get(pmg_id)
            if not pmg:
                continue
            pm_ids = tokens_flat(braced_tokens(pmg.text, "production_methods"))
            defaults = [pm_id for pm_id in pm_ids if pm_id in pms and scalar(pms[pm_id].text, "is_default") == "yes"]
            chosen = defaults[0] if defaults else (pm_ids[0] if pm_ids else "")
            if chosen:
                base_pms.append(f"{pmg_id}:{chosen}")
            for pm_id in pm_ids:
                pm = pms.get(pm_id)
                if not pm:
                    continue
                inputs.update(re.findall(r"goods_input_([A-Za-z0-9_]+)_add", pm.text))
                outputs.update(re.findall(r"goods_output_([A-Za-z0-9_]+)_add", pm.text))
                pm_techs.update(tokens_flat(braced_tokens(pm.text, "unlocking_technologies")))

        max_rules: list[str] = []
        if group and scalar(group.text, "stateregion_max_level") == "yes":
            max_rules.append("STATE_REGION_RESOURCE_CAP")
        if scalar(block.text, "max_level"):
            max_rules.append("max_level=" + scalar(block.text, "max_level"))
        if building_id == "building_port":
            max_rules.append("COASTAL_ONLY")
        if is_auto:
            max_rules.append("ENGINE_GENERATED_LEVELS")
        if not max_rules:
            max_rules.append("NO_EXPLICIT_DEFINITION_CAP")

        if category in {"AGRICULTURE_COMMERCIAL", "PLANTATION"}:
            resource_constraint = "ARABLE_LAND_AND_STATE_ARABLE_RESOURCE"
        elif category == "RESOURCE_EXTRACTION":
            resource_constraint = "STATE_REGION_RESOURCE_CAP_OR_DISCOVERY"
        elif category == "PORT":
            resource_constraint = "COASTAL_STATE"
        elif "monument" in " ".join(ancestry).lower() or "monument" in building_id:
            resource_constraint = "STATE_SPECIFIC_POTENTIAL"
        else:
            resource_constraint = "NONE_EXPLICIT"

        gate_eras = []
        for gate in gates:
            era = scalar(techs.get(gate, Block("", "", ROOT, 0)).text, "era")
            match = re.search(r"(\d+)", era)
            if match:
                gate_eras.append(int(match.group(1)))
        if is_auto:
            relevance = "NO_AUTO_GENERATED"
        elif building_id in POST_1776_BUILDINGS:
            relevance = "NO_POST_1776"
        elif building_id in SPECIAL_SYSTEM_BUILDINGS:
            relevance = "NO_SPECIAL_SYSTEM"
        elif building_id == "building_trade_center":
            relevance = "YES_CASE_BY_CASE_TRADE_SEED"
        elif building_id == "building_railway":
            relevance = "YES_ROADS_CANALS_ONLY_NO_RAIL"
        elif gate_eras and max(gate_eras) >= 4:
            relevance = "NO_POST_1776"
        elif gates:
            relevance = "YES_TECH_DISTRIBUTION_REVIEW"
        else:
            relevance = "YES"

        if is_auto:
            history_placeable = "NO_ENGINE_GENERATED"
        elif building_id in placed:
            history_placeable = "YES_USED_IN_CURRENT_HISTORY"
        elif scalar(block.text, "buildable") == "no":
            history_placeable = "NO_NONBUILDABLE_OR_EVENT_CONTROLLED"
        elif scalar(block.text, "potential"):
            history_placeable = "CONDITIONAL_POTENTIAL"
        else:
            history_placeable = "YES_TECHNICALLY"

        notes = ["FORK_OVERRIDE" if block.source.is_relative_to(ROOT) else "VANILLA_FALLBACK"]
        aliases = tokens_flat(braced_tokens(block.text, "aliases"))
        if aliases:
            notes.append("Aliases=" + "|".join(aliases))
        if building_id == "building_railway":
            notes.append("TECH7A_UNIFIED_ROADS_CANALS_RAIL")
        if is_auto:
            notes.append("DO_NOT_RESEARCH_AS_MANUAL_STARTING_BUILDING")
        if building_id in POST_1776_BUILDINGS:
            notes.append("POST_1776_EXPLICIT_DATE_FILTER")
        if building_id in SPECIAL_SYSTEM_BUILDINGS:
            notes.append("SPECIAL_OR_EVENT_SYSTEM_NOT_START_RESEARCH")
        if pm_techs:
            notes.append("PM_Gates=" + "|".join(sorted(pm_techs)))

        display_en = en.get(building_id, building_id)
        display_fr = fr.get(building_id, building_id)
        if building_id in DUMMY_DISPLAY_NAMES and (display_en == "$building_dummy$" or display_fr == "$building_dummy$"):
            display_en, display_fr = DUMMY_DISPLAY_NAMES[building_id]
            notes.append("REPORT_LABEL_FALLBACK_FOR_VANILLA_BUILDING_DUMMY")

        building_rows.append(
            {
                "Building_ID": building_id,
                "Display_Name_EN": display_en,
                "Display_Name_FR": display_fr,
                "Building_Group": group_id,
                "Category": category,
                "History_Placeable": history_placeable,
                "Auto_Generated": "YES" if is_auto else "NO",
                "Technology_Gates": "|".join(gates) if gates else "NONE",
                "Base_PM": "|".join(base_pms),
                "Important_Inputs": "|".join(sorted(inputs)) if inputs else "NONE",
                "Important_Outputs": "|".join(sorted(outputs)) if outputs else "NONE",
                "Max_Level_Rules": "|".join(max_rules),
                "Resource_Constraint": resource_constraint,
                "Relevant_For_1776_Start_Research": relevance,
                "Notes": "; ".join(notes),
            }
        )
    write_csv(
        OUT / "BUILD_START_1776_BUILDING_CATALOG.csv",
        [
            "Building_ID", "Display_Name_EN", "Display_Name_FR", "Building_Group", "Category",
            "History_Placeable", "Auto_Generated", "Technology_Gates", "Base_PM",
            "Important_Inputs", "Important_Outputs", "Max_Level_Rules", "Resource_Constraint",
            "Relevant_For_1776_Start_Research", "Notes",
        ],
        building_rows,
    )

    research_rows = []
    for row in state_rows:
        research_rows.append(
            {
                "State_ID": row["State_ID"],
                "State_Display_Name": row["State_Display_Name"],
                "Owner_TAG": row["Owner_TAG"],
                "Owner_Name": row["Owner_Name"],
                "Research_Region": "EXCLUDED_SERENISSIMA" if row["Excluded_Serenissima"] == "YES" else row["Region"],
                "Excluded_Serenissima": row["Excluded_Serenissima"],
                "Map_Rework_Risk": row["Map_Rework_Risk"],
                "Source_File": row["Source_File"],
            }
        )
    write_csv(
        OUT / "BUILD_START_1776_RESEARCH_REGIONS.csv",
        [
            "State_ID", "State_Display_Name", "Owner_TAG", "Owner_Name", "Research_Region",
            "Excluded_Serenissima", "Map_Rework_Risk", "Source_File",
        ],
        research_rows,
    )

    trade_rows = [row for row in current_rows if row["Building_ID"] == "building_trade_center"]
    trade_levels = sum(int(row["Current_Level"]) for row in trade_rows)
    trade_doc = f"""# Centres de commerce — mécanique effective Victoria 3 1.13.11 + fork

Date de l’audit : 2026-09-16  
Portée : audit technique uniquement, sans modification du système.

## Résultat direct

- **ID exact :** `building_trade_center`.
- **Placement historique :** oui, via `create_building` dans `common/history/buildings`, sous le couple `s:STATE_*` / `region_state:TAG`. Ce n’est pas une entrée de `common/history/states`.
- **Génération par routes commerciales :** non dans le système 1.13.11. Les centres de commerce sont des bâtiments construits ou préplacés qui donnent la capacité utilisée par le commerce mondial autonome ; une route commerciale ne crée pas automatiquement un niveau.
- **Niveaux manuels actuels :** {len(trade_rows)} implantations, {trade_levels} niveaux au total dans le working tree.
- **Conservation :** un niveau créé dans l’historique est chargé comme tout autre niveau de bâtiment. Il peut ensuite être agrandi ou réduit selon l’activité et les règles normales.

## Emplois et capacité

Le PM de base `pm_trade_center` ajoute par niveau 800 employés de bureau et 200 commerçants. À effectif complet, il fournit par niveau :

- `state_weekly_trades_add = 1` ;
- `state_trade_capacity_add = 10`.

Le PM quantitatif normal, actif par défaut, consomme `goods_input_merchant_marine_add = 4` à l’échelle de la main-d’œuvre. Le groupe `bg_trade` consomme aussi 0,5 infrastructure par niveau, n’emploie pas l’économie d’échelle et porte les revenus commerciaux.

## Interaction avec le commerce, les ports et le marché

- Le niveau ne représente pas une route individuelle : il fournit de la capacité et un nombre de transactions hebdomadaires au commerce autonome.
- Le centre n’a pas besoin d’être côtier. En revanche, l’accès au marché mondial demeure nécessaire ; un pays enclavé doit disposer d’un accès ou de droits de transit.
- Les ports produisent le bien `merchant_marine` consommé par le centre de commerce. Leur relation est donc économique et logistique, pas une relation de génération automatique.
- Les avantages commerciaux, accords, ports de traité, embargos, guerres, intérêts et péages influencent où et comment la capacité est utilisée.
- La construction publique ou privée appelle `trade_center_construction_allowed`. L’isolationnisme l’interdit normalement ; les lois Canton System et Sakoku imposent des États et plafonds spécifiques.

## Risques d’un niveau manuel

Un niveau préplacé sans volume commercial correspondant peut créer des emplois non rentables, une demande de marine marchande, une consommation d’infrastructure et de la capacité inutilisée. Le moteur peut ensuite envisager une réduction automatique lorsque la capacité inutilisée dépasse ses seuils. Il n’existe pas de risque de « doublon par route », mais il existe un risque de surcapacité si l’historique et la construction ultérieure sont tous deux trop généreux.

## Sources techniques

- `common/buildings/11_private_infrastructure.txt` — définition et règles de construction ;
- `common/production_method_groups/11_private_infrastructure.txt` — PMG ;
- `common/production_methods/11_private_infrastructure.txt` — emplois, capacité et marine marchande ;
- `common/building_groups/00_building_groups.txt` (vanilla effectif) — groupe `bg_trade` ;
- `common/scripted_triggers/00_building_triggers.txt` (vanilla effectif) — restrictions de construction ;
- `common/defines/00_defines.txt` (vanilla effectif) — sélection, avantage et réduction automatique ;
- `common/history/buildings/*.txt` — niveaux initiaux du fork.
"""
    (OUT / "BUILD_START_1776_TRADE_CENTER_MECHANICS.md").write_text(trade_doc, encoding="utf-8")

    infra = buildings["building_railway"]
    infra_pmgs = tokens_flat(braced_tokens(infra.text, "production_method_groups"))
    excluded_rows = [row for row in state_rows if row["Excluded_Serenissima"] == "YES"]
    india_rows = [row for row in state_rows if row["Map_Rework_Risk"] == "INDIA_FUTURE_REWORK"]
    vietnam_rows = [row for row in state_rows if row["Map_Rework_Risk"] == "VIETNAM_FUTURE_REWORK"]
    relevant_buildings = [row for row in building_rows if str(row["Relevant_For_1776_Start_Research"]).startswith("YES")]
    auto_rows = [row for row in building_rows if row["Auto_Generated"] == "YES"]
    post_1776_rows = [row for row in building_rows if row["Building_ID"] in POST_1776_BUILDINGS]
    special_system_rows = [row for row in building_rows if row["Building_ID"] in SPECIAL_SYSTEM_BUILDINGS]
    orphan_summary = sorted(
        {
            f"{row['owner']} / {row['state']} ({'|'.join(row['sources'])})"
            for row in orphan_current_buildings
        }
    )

    report = f"""# BUILD START 1776 — Research Input Pack

Date : 2026-09-16  
Autorité : working tree local actuel  
Référence moteur : Victoria 3 1.13.11 (`C:\\Games\\Victoria 3\\game`)

## Résumé quantitatif

- États possédés actuels : **{len(state_rows)}** instances État/propriétaire, couvrant **{len({row['State_ID'] for row in state_rows})}** identifiants de région d’État.
- Bâtiments effectivement disponibles : **{len(building_rows)}**.
- Bâtiments pertinents pour une première recherche 1776 : **{len(relevant_buildings)}**.
- Entrées de bâtiments de départ actuelles : **{len(current_rows)}** couples propriétaire/État/bâtiment.
- Sérénissimes exclues : **{len(excluded_rows)}** instances État/propriétaire appartenant à VEN ou GEN.
- Risque Inde : **{len(india_rows)}** instances ; risque Vietnam : **{len(vietnam_rows)}** instances.

Les lignes d’États divisés sont conservées séparément par propriétaire. C’est indispensable pour la population, l’accès au port et l’exclusion exacte de VEN/GEN.

## Exclusion VEN / GEN

Toutes les lignes possédées par `VEN` ou `GEN` portent `Excluded_Serenissima = YES`. Elles sont affectées à `EXCLUDED_SERENISSIMA` dans la partition de recherche. Aucun de ces États ne doit recevoir de recommandation issue de la redistribution mondiale générale.

## Risques de refonte cartographique

- `INDIA_FUTURE_REWORK` : toutes les régions d’État du fichier cartographique actuel `10_india.txt`.
- `VIETNAM_FUTURE_REWORK` : Cambodge, Tonkin, Annam, Mékong et Laos dans la carte actuelle.
- La carte Tsar mise à jour n’est jamais utilisée comme cible dans ce pack.

## Bâtiments automatiquement générés

Les chercheurs ne doivent pas proposer manuellement les bâtiments suivants :

{chr(10).join('- `' + str(row['Building_ID']) + '`' for row in auto_rows)}

Le catalogue les marque `Auto_Generated = YES`, `History_Placeable = NO_ENGINE_GENERATED` et `Relevant_For_1776_Start_Research = NO_AUTO_GENERATED`.

## Filtre chronologique et bâtiments spéciaux

Les bâtiments suivants sont explicitement exclus de la recherche de départ parce que leur forme représentée est postérieure au 1er janvier 1776 :

{chr(10).join('- `' + str(row['Building_ID']) + '`' for row in post_1776_rows)}

Les bâtiments suivants relèvent d’un système spécial ou événementiel et ne sont pas des candidats ordinaires à implanter au départ :

{chr(10).join('- `' + str(row['Building_ID']) + '`' for row in special_system_rows)}

## Centres de commerce

`building_trade_center` est un bâtiment manuel/construit dans Victoria 3 1.13.11, et non un bâtiment généré niveau par niveau par des routes commerciales. Les niveaux historiques sont conservés, fournissent emplois et capacité commerciale, consomment marine marchande et infrastructure, et peuvent créer une surcapacité. Voir `BUILD_START_1776_TRADE_CENTER_MECHANICS.md`.

## REGIONAL_INFRASTRUCTURE_STARTING_LEVELS

| Champ | Valeur effective |
|---|---|
| Building_ID | `building_railway` |
| Alias | `building_land_transport_network` |
| PMGs | {', '.join('`' + pmg + '`' for pmg in infra_pmgs)} |
| Routes | `pm_traditional_road_network` (défaut), `pm_turnpike_road_network` → `turnpike_road_networks`, `pm_engineered_road_network` → `improved_road_engineering`, `pm_paved_road_network` → `paved_roads` |
| Canaux | `pm_no_canal_network` (défaut), `pm_industrial_canals` → `industrial_canals`, `pm_engineered_canals` → `professional_civil_engineering` |
| Rail | `pm_no_rail_network` (défaut), `pm_early_trains` → `railways`, puis PM vapeur/électriques/diesel avec leurs technologies supplémentaires |
| Gate du bâtiment | aucune : les portes sont portées par les PM |
| Placement historique | `create_building` avec l’ID canonique `building_railway`; routes actives par défaut, aucun canal et aucun rail par défaut |
| Règle 1776 | rechercher séparément routes et canaux ; conserver obligatoirement `pm_no_rail_network` car le rail est anachronique |

Les trois PMG routes/canaux/rail sont simultanés : leurs infrastructures et effets s’additionnent. Le quatrième PMG, `pmg_passenger_trains`, ne devient matériellement pertinent qu’avec un réseau ferroviaire actif.

## Technologies et gates

Le champ `Technology_Gates` du catalogue contient les technologies nécessaires au bâtiment lui-même. Le champ `Notes` ajoute les `PM_Gates` de toutes ses méthodes. Si la recherche historique exige un bâtiment dont le pays ne possède pas la porte correspondante, la future synthèse doit inscrire **`TECH_DISTRIBUTION_REVIEW`** et ne pas supprimer artificiellement le bâtiment.

Cas structurants :

- ports : `enclosed_dock_systems` ;
- bâtiment régional TECH7A : aucune porte globale, portes distinctes pour routes, canaux et rail ;
- industries et ressources avancées : vérifier leur porte et leur ère dans le catalogue ;
- bâtiments marqués `NO_POST_1776` : ne pas rechercher comme implantation initiale ordinaire.

## Discipline anti-ancrage

`BUILD_START_1776_CURRENT_BUILDINGS.csv` est réservé à la seconde passe de synthèse et au calcul du delta. Il ne doit pas être transmis aux chercheurs pendant leur première recherche historique : leur première proposition doit partir des sources de 1776, du catalogue des bâtiments et de la partition régionale, sans connaître le setup existant.

Le parseur a également ignoré **{len(orphan_current_buildings)}** entrées de bâtiments orphelines, dont le couple propriétaire/État ne correspond plus à la carte effective du working tree :

{chr(10).join('- `' + item + '`' for item in orphan_summary)}

Elles restent intactes dans les fichiers de gameplay ; elles ne sont simplement pas présentées comme bâtiments de départ effectifs dans ce pack technique.

## Neuf régions de recherche

1. `R1_WESTERN_EUROPE`
2. `R2_NORTHERN_CENTRAL_EASTERN_EUROPE`
3. `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA`
4. `R4_SOUTH_ASIA`
5. `R5_EAST_ASIA`
6. `R6_SOUTHEAST_ASIA_OCEANIA`
7. `R7_SUBSAHARAN_AFRICA`
8. `R8_NORTH_AMERICA_CARIBBEAN`
9. `R9_SOUTH_AMERICA`

Les possessions coloniales sont classées par emplacement de l’État, jamais par métropole.

## Fichiers livrés

- `BUILD_START_1776_STATE_CATALOG.csv`
- `BUILD_START_1776_BUILDING_CATALOG.csv`
- `BUILD_START_1776_CURRENT_BUILDINGS.csv`
- `BUILD_START_1776_RESEARCH_REGIONS.csv`
- `BUILD_START_1776_TRADE_CENTER_MECHANICS.md`
- présent rapport

Aucun fichier de gameplay n’a été modifié. Aucun commit et aucun push.
"""
    (OUT / "BUILD_START_1776_RESEARCH_INPUT_PACK.md").write_text(report, encoding="utf-8")

    # Hard validations required by the research contract.
    assert len(state_rows) == len({(row["State_ID"], row["Owner_TAG"]) for row in state_rows})
    assert all(str(row["State_ID"]) in map_regions for row in state_rows)
    assert all(int(row["Current_Population"]) > 0 for row in state_rows)
    assert all(row["Excluded_Serenissima"] == ("YES" if row["Owner_TAG"] in {"VEN", "GEN"} else "NO") for row in state_rows)
    assert all(row["Research_Region"] == "EXCLUDED_SERENISSIMA" for row in research_rows if row["Excluded_Serenissima"] == "YES")
    assert all(row["Research_Region"] in set(REGION_BY_FILE.values()) for row in research_rows if row["Excluded_Serenissima"] == "NO")
    assert {row["Research_Region"] for row in research_rows if row["Excluded_Serenissima"] == "NO"} == set(REGION_BY_FILE.values())
    assert {row["Map_Rework_Risk"] for row in state_rows} <= {"NONE", "INDIA_FUTURE_REWORK", "VIETNAM_FUTURE_REWORK", "OTHER"}
    assert {"building_trade_center", "building_railway"}.issubset(buildings)
    assert all(row["Building_ID"] for row in building_rows)
    assert {
        "AGRICULTURE_COMMERCIAL", "PLANTATION", "RESOURCE_EXTRACTION", "MANUFACTURING",
        "SHIPBUILDING", "PORT", "INFRASTRUCTURE", "TRADE_CENTER", "MILITARY",
        "ADMINISTRATION", "EDUCATION", "OTHER",
    } <= {row["Category"] for row in building_rows}
    assert all(not str(row["Display_Name_EN"]).startswith("$") for row in building_rows)
    assert all(not str(row["Display_Name_FR"]).startswith("$") for row in building_rows)
    assert all((str(row["owner"]), str(row["state"])) in valid_owner_states for row in current_buildings)
    assert all(str(row["building"]) in buildings and int(row["level"]) > 0 for row in current_buildings)
    assert not {str(row["Building_ID"]) for row in building_rows if row["Auto_Generated"] == "YES"} & POST_1776_BUILDINGS
    print(
        f"BUILD START INPUT PACK: PASS — {len(state_rows)} owned states, "
        f"{len(building_rows)} buildings, {len(current_rows)} current building rows"
    )


if __name__ == "__main__":
    main()
