#!/usr/bin/env python3
"""Apply the reviewed British-market shortage correction.

The pass deliberately keeps resource geography authoritative: no state-region
potential is added.  Colonial resources are used outside BIC, while urban
manufacturing and the tooling export anchor remain in Great Britain.
"""

from __future__ import annotations

import csv
import math
import re
import sys
from collections import defaultdict
from pathlib import Path

import build_start_1776_research_input_pack as catalog_tools
import build_start_1776_runtime_wave1 as runtime
import build_start_1776_world_apply as world


ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "common" / "history" / "buildings"
REPORTS = ROOT / "docs" / "reports" / "buildings"
OVERLAY = HISTORY / "98b_build_start_1776_british_market_correction.txt"
MATRIX = REPORTS / "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_RUNTIME_V1.csv"
STATE_CATALOG = REPORTS / "BUILD_START_1776_STATE_CATALOG.csv"
BUILDING_CATALOG = REPORTS / "BUILD_START_1776_BUILDING_CATALOG.csv"
INFRA_AUDIT = REPORTS / "BUILD_START_1776_RUNTIME_INFRASTRUCTURE_AUDIT.csv"
INFRA_OVERLAY = REPORTS / "BUILD_START_1776_RUNTIME_INFRASTRUCTURE_OVERLAY.csv"
MARKET_AUDIT = REPORTS / "BUILD_START_1776_RUNTIME_MARKET_GOODS_AUDIT.csv"
SUPPLY_OVERLAY = REPORTS / "BUILD_START_1776_RUNTIME_MARKET_SUPPLY_OVERLAY.csv"
REPORT = REPORTS / "BUILD_START_1776_BRITISH_DOMESTIC_SUPPLY_CORRECTION.md"


COLONIAL_PM = {
    "building_banana_plantation": [
        "default_building_banana_plantation", "default_labour", "pm_road_carts",
    ],
    "building_salt_pan": ["default_building_salt_pan"],
    "building_logging_camp": [
        "pm_simple_forestry", "pm_no_hardwood", "pm_no_equipment", "pm_road_carts",
    ],
    "building_lead_mine": [
        "pm_picks_and_shovels_building_lead_mine", "pm_no_explosives",
        "pm_no_steam_automation", "pm_road_carts",
        "pm_no_ore_concentration_building_lead_mine", "pm_no_mine_ventilation",
    ],
    "building_limestone_quarry": [
        "pm_picks_and_shovels_building_limestone_quarry",
        "pm_no_stone_processing_building_limestone_quarry",
    ],
    "building_furniture_manufactory": [
        "pm_handcrafted_furniture", "pm_no_luxuries", "pm_automation_disabled",
    ],
    "building_textile_mill": [
        "pm_handsewn_clothes", "pm_craftsman_sewing", "pm_traditional_looms",
    ],
    "building_chemical_plant": [
        "pm_artificial_fertilizers", "pm_no_industrial_chemicals",
        "pm_no_pharmaceutical_production",
    ],
    "building_port": ["pm_anchorage"],
    "building_railway": [
        "pm_traditional_road_network", "pm_no_canal_network",
        "pm_no_rail_network", "pm_no_passenger_trains",
    ],
}


# New levels only. Existing Florida dye is rescaled separately; the invalid
# Bahamas salt placement is removed because that state has no salt potential.
ADDITIONS = {
    ("GBR", "STATE_JAMAICA", "building_banana_plantation"): 8,
    ("GBR", "STATE_JAMAICA", "building_logging_camp"): 3,
    ("GBR", "STATE_WEST_INDIES", "building_banana_plantation"): 6,
    ("GBR", "STATE_FLORIDA", "building_limestone_quarry"): 2,
    ("GBR", "STATE_BAHAMAS", "building_limestone_quarry"): 3,
    ("GBR", "STATE_NEWFOUNDLAND", "building_lead_mine"): 4,
    ("GBR", "STATE_WEST_COUNTRY", "building_lead_mine"): 5,
    ("GBR", "STATE_WEST_COUNTRY", "building_furniture_manufactory"): 4,
    ("GBR", "STATE_WEST_COUNTRY", "building_textile_mill"): 4,
    ("GBR", "STATE_LANCASHIRE", "building_chemical_plant"): 7,
    # Senegal is a British colonial subject with an existing salt-pan cap of
    # 30.  The salt works are British-capital-owned and use 24 of that cap.
    ("SIL", "STATE_SENEGAL", "building_salt_pan"): 24,
    ("SIL", "STATE_SENEGAL", "building_port"): 1,
}

ROAD_PAIRS = {
    ("GBR", "STATE_EAST_ANGLIA"), ("GBR", "STATE_JAMAICA"),
    ("GBR", "STATE_WEST_INDIES"), ("GBR", "STATE_BAHAMAS"),
    ("GBR", "STATE_FLORIDA"), ("GBR", "STATE_BERMUDA"),
    ("GBR", "STATE_NEWFOUNDLAND"), ("GBR", "STATE_WEST_COUNTRY"),
    ("GBR", "STATE_LANCASHIRE"), ("GBR", "STATE_MIDLANDS"),
    ("SIL", "STATE_SENEGAL"),
}

# The earlier user-requested HBC fishery correction created three small
# post-Wave-1 infrastructure gaps.  They are retained here as one-level road
# repairs so the world infrastructure invariant remains true.
POST_HBC_ROAD_REPAIRS = {
    ("HBC", "STATE_MANITOBA", "building_railway"): 1,
    ("HBC", "STATE_ONTARIO", "building_railway"): 1,
    ("HBC", "STATE_QUEBEC", "building_railway"): 1,
}

NO_ORCHARD_STATES = {
    "STATE_EAST_ANGLIA", "STATE_HOME_COUNTIES", "STATE_LANCASHIRE",
    "STATE_LOWLANDS", "STATE_MIDLANDS",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def ownership_type(building: str) -> str:
    if building == "building_banana_plantation":
        return "building_manor_house"
    if building in {
        "building_furniture_manufactory", "building_textile_mill",
        "building_chemical_plant", "building_salt_pan", "building_logging_camp",
    }:
        return "building_financial_district"
    return building


def create_block(owner: str, state: str, building: str, level: int) -> str:
    pms = " ".join(f'"{pm}"' for pm in COLONIAL_PM[building])
    holder = ownership_type(building)
    holder_country = "GBR" if (owner, state, building) == (
        "SIL", "STATE_SENEGAL", "building_salt_pan"
    ) else owner
    return (
        "create_building = {\n"
        f'\tbuilding = "{building}"\n'
        "\tadd_ownership = {\n"
        "\t\tbuilding = {\n"
        f'\t\t\ttype = "{holder}"\n'
        f'\t\t\tcountry = "c:{holder_country}"\n'
        f"\t\t\tlevels = {level}\n"
        f'\t\t\tregion = "{state}"\n'
        "\t\t}\n"
        "\t}\n"
        "\treserves = 1\n"
        f"\tactivate_production_methods = {{ {pms} }}\n"
        "}"
    )


def apply_existing_edits() -> None:
    raws, placements = world.all_placements(HISTORY)
    changes: dict[Path, list[tuple[int, int, str]]] = defaultdict(list)
    seen: set[tuple[str, str, str]] = set()

    remove = {
        ("GBR", "STATE_EAST_ANGLIA", "building_dye_plantation"),
        ("GBR", "STATE_EAST_ANGLIA", "building_sugar_plantation"),
        ("GBR", "STATE_EAST_ANGLIA", "building_salt_pan"),
        ("GBR", "STATE_BAHAMAS", "building_salt_pan"),
    }
    rescale = {
        ("GBR", "STATE_FLORIDA", "building_dye_plantation"): 2,
    }
    chemical_key = ("GBR", "STATE_MIDLANDS", "building_chemical_works")

    for placement in placements:
        replacement: str | None = None
        if placement.key in remove:
            replacement = ""
            seen.add(placement.key)
        elif placement.key in rescale:
            replacement = world.rescale_ownership(placement.text, rescale[placement.key])
            seen.add(placement.key)
        elif (
            placement.owner == "GBR" and placement.state in NO_ORCHARD_STATES
            and placement.building == "building_rye_farm"
        ):
            selected = ["pm_no_secondary" if pm == "pm_apple_orchards" else pm for pm in placement.pms]
            replacement = world.replace_active_pms(placement.text, selected)
        elif placement.key == chemical_key:
            replacement = placement.text.replace("building_chemical_works", "building_chemical_plant")
            replacement = world.replace_active_pms(replacement, [
                "pm_no_fertilizer_production", "pm_lead_chamber_process",
                "pm_no_pharmaceutical_production",
            ])
            seen.add(chemical_key)
        if replacement is not None:
            changes[placement.path].append((placement.start, placement.end, replacement))

    expected = remove | set(rescale) | {chemical_key}
    if seen != expected:
        raise RuntimeError(f"Existing correction preflight mismatch: missing={sorted(expected - seen)}")

    for path, replacements in changes.items():
        raw = raws[path]
        for start, end, replacement in sorted(replacements, reverse=True):
            raw = raw[:start] + replacement + raw[end:]
        catalog_tools.brace_maps(catalog_tools.clean_comments(raw))
        path.write_text(raw, encoding="utf-8")


def remove_effective_key(key: tuple[str, str, str]) -> None:
    """Remove every effective history placement for one reviewed key."""
    raws, placements = world.all_placements(HISTORY)
    matches = [placement for placement in placements if placement.key == key]
    if not matches:
        return
    changes: dict[Path, list[tuple[int, int, str]]] = defaultdict(list)
    for placement in matches:
        changes[placement.path].append((placement.start, placement.end, ""))
    for path, replacements in changes.items():
        raw = raws[path]
        for start, end, replacement in sorted(replacements, reverse=True):
            raw = raw[:start] + replacement + raw[end:]
        catalog_tools.brace_maps(catalog_tools.clean_comments(raw))
        path.write_text(raw, encoding="utf-8")


def write_supply_buildings(dynamic_roads: dict[tuple[str, str, str], int] | None = None) -> None:
    complete = ADDITIONS | POST_HBC_ROAD_REPAIRS | (dynamic_roads or {})
    rows = [
        (owner, state, building, level, create_block(owner, state, building, level))
        for (owner, state, building), level in sorted(complete.items())
    ]
    text = world.build_overlay(rows).replace(
        "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv",
        "BUILD_START_1776_BRITISH_DOMESTIC_SUPPLY_CORRECTION.md",
    )
    text = text.replace(
        "# Generated from BUILD_START_1776_BRITISH_DOMESTIC_SUPPLY_CORRECTION.md",
        "# British-market shortage correction; no resource potentials were added.\n"
        "# Colonial placements exclude BIC.  Manufacturing/tooling remains British.",
    )
    catalog_tools.brace_maps(catalog_tools.clean_comments(text))
    OVERLAY.write_text(text, encoding="utf-8")


def set_exact_roads() -> dict[tuple[str, str, str], int]:
    state_rows = read_csv(STATE_CATALOG)
    levels, pms, placements = runtime.actual_semantics()
    calibration = dict(levels)
    for owner, state in ROAD_PAIRS:
        calibration[(owner, state, runtime.INFRA)] = 0
    _, _, targets, plans = runtime.infrastructure_plan(state_rows, calibration, pms)
    road_targets = {
        (owner, state, runtime.INFRA): targets[(owner, state, runtime.INFRA)]
        for owner, state in ROAD_PAIRS
    }

    by_key: dict[tuple[str, str, str], list[world.Placement]] = defaultdict(list)
    for placement in placements:
        by_key[placement.key].append(placement)
    missing = {key: target for key, target in road_targets.items() if not by_key.get(key) and target > 0}
    if missing:
        write_supply_buildings(missing)
        levels, pms, placements = runtime.actual_semantics()
        by_key = defaultdict(list)
        for placement in placements:
            by_key[placement.key].append(placement)

    changes: dict[Path, list[tuple[int, int, str]]] = defaultdict(list)
    for key, target in sorted(road_targets.items()):
        existing = by_key.get(key, [])
        if len(existing) != 1:
            raise RuntimeError(f"Expected one road placement for {key}, got {len(existing)}")
        placement = existing[0]
        if target <= 0:
            replacement = ""
        else:
            replacement = world.rescale_ownership(placement.text, target)
            plan = plans[(key[0], key[1])]
            replacement = world.replace_active_pms(replacement, [
                plan["Road_PM"], plan["Canal_PM"], plan["Rail_PM"], plan["Passenger_PM"],
            ])
        changes[placement.path].append((placement.start, placement.end, replacement))

    for path, replacements in changes.items():
        raw = path.read_text(encoding="utf-8-sig")
        for start, end, replacement in sorted(replacements, reverse=True):
            raw = raw[:start] + replacement + raw[end:]
        catalog_tools.brace_maps(catalog_tools.clean_comments(raw))
        path.write_text(raw, encoding="utf-8")
    return road_targets


def update_infrastructure_reports() -> None:
    state_rows = read_csv(STATE_CATALOG)
    levels, pms, _ = runtime.actual_semantics()
    audit, overlay, _, _ = runtime.infrastructure_plan(state_rows, levels, pms)
    fields = [
        "Owner_TAG", "Country", "State_ID", "State_Name", "Current_Level", "Road_PM", "Canal_PM",
        "Rail_PM", "Passenger_PM", "Infrastructure_Available", "Infrastructure_Used", "Current_Market_Access",
        "Additional_Level_Needed", "Historical_Connectivity_Exception", "Evidence", "Final_Target_Level",
        "Final_Infrastructure_Available", "Reason",
    ]
    write_csv(INFRA_AUDIT, fields, audit)
    overlay_fields = list(overlay[0]) if overlay else [
        "Owner_TAG", "Country", "State_ID", "State_Name", "Building_ID", "Historical_Level",
        "Runtime_Additional_Level", "Runtime_Final_Target_Level", "Road_PM", "Canal_PM", "Rail_PM",
        "Passenger_PM", "Capacity_Per_Level", "Reason",
    ]
    write_csv(INFRA_OVERLAY, overlay_fields, overlay)


def update_matrix(road_targets: dict[tuple[str, str, str], int]) -> None:
    rows = read_csv(MATRIX)
    fields = list(rows[0])
    states = {(row["Owner_TAG"], row["State_ID"]): row for row in read_csv(STATE_CATALOG)}
    buildings = {row["Building_ID"]: row for row in read_csv(BUILDING_CATALOG)}
    targets = dict(ADDITIONS)
    targets.update(road_targets)
    targets.update(POST_HBC_ROAD_REPAIRS)
    targets.update({
        ("GBR", "STATE_EAST_ANGLIA", "building_dye_plantation"): 0,
        ("GBR", "STATE_EAST_ANGLIA", "building_sugar_plantation"): 0,
        ("GBR", "STATE_EAST_ANGLIA", "building_salt_pan"): 0,
        ("GBR", "STATE_BAHAMAS", "building_salt_pan"): 0,
        ("GBR", "STATE_BERMUDA", "building_salt_pan"): 0,
        ("GBR", "STATE_FLORIDA", "building_salt_pan"): 0,
        ("GBR", "STATE_JAMAICA", "building_salt_pan"): 0,
        ("GBR", "STATE_WEST_INDIES", "building_salt_pan"): 0,
        ("GBR", "STATE_FLORIDA", "building_dye_plantation"): 2,
        ("GBR", "STATE_MIDLANDS", "building_chemical_works"): 0,
        ("GBR", "STATE_MIDLANDS", "building_chemical_plant"): 1,
    })
    by_key = {(row["Owner_TAG"], row["State_ID"], row["Building_ID"]): row for row in rows}

    for key, target in sorted(targets.items()):
        row = by_key.get(key)
        if row is None:
            state = states[(key[0], key[1])]
            cat = buildings.get(key[2], {})
            row = {field: "" for field in fields}
            row.update({
                "Research_Region": state["Region"], "Owner_TAG": key[0], "Country": state["Owner_Name"],
                "State_ID": key[1], "State_Name": state["State_Display_Name"], "Building_ID": key[2],
                "Building_Name": cat.get("Display_Name_EN", key[2]), "Current_Level": 0,
                "Confidence": "RUNTIME_TARGETED", "Economic_Role": "DOMESTIC_MARKET_SUPPLY",
                "Domestic_Demand": "BRITISH_MARKET", "Export_Orientation": "NONE",
                "Industry_Form": "REVIEWED_RUNTIME_PLACEMENT", "Tech_Distribution_Review": "NO",
                "Map_Rework_Risk": "NONE", "Serenissima_Protected": "NO",
                "Historical_Evidence": "Observed red shortage in the supplied British-market runtime capture.",
                "Level_Rationale": "Capacity sized from the captured deficit and the selected 1776 PM output.",
                "Base_Historical_Target_Level": 0, "Overlay_Type": "NONE",
                "Overlay_Reason": "Frozen historical target remains zero.",
            })
            rows.append(row)
            by_key[key] = row
        old_runtime = int(float(row.get("Runtime_Base_Target_Level") or row.get("Base_Historical_Target_Level") or 0))
        current = int(float(row.get("Current_Level") or 0))
        if key[2] in buildings:
            row["Building_Name"] = buildings[key[2]]["Display_Name_EN"]
        row.update({
            "Target_Level": target,
            "Delta": target - current,
            "Decision": (
                "RUNTIME_REMOVE" if target == 0
                else "RUNTIME_INCREASE" if target > old_runtime and old_runtime > 0
                else "RUNTIME_DECREASE" if target < old_runtime
                else "RUNTIME_ADD" if old_runtime == 0
                else row.get("Decision", "KEEP")
            ),
            "Runtime_Base_Target_Level": old_runtime,
            "Runtime_Level_Delta": target - old_runtime,
            "Runtime_Final_Target_Level": target,
            "Runtime_Overlay_Type": "BRITISH_MARKET_SHORTAGE_CORRECTION_V2",
            "Runtime_Overlay_Reason": "Observed British-market shortage correction without new resource potential or BIC placement.",
        })
    rows.sort(key=lambda row: (row["Research_Region"], row["Owner_TAG"], row["State_ID"], row["Building_ID"]))
    write_csv(MATRIX, fields, rows)


def update_market_reports() -> None:
    fields = [
        "Market", "Good", "Buy_Orders", "Sell_Orders", "Balance", "Price", "Shortage_Status",
        "Main_Consumers", "Current_Producers", "PMs", "Potential_Domestic_Producers", "Import_Capacity",
        "Historical_Shortage_Justification", "Wave1_Decision",
    ]
    captured = {
        "fruit": (398, 0, -398, 52, "building_banana_plantation", "default_building_banana_plantation", "ADD_14_COLONIAL_BANANA_LEVELS"),
        "lead": (234, 60, -174, 70, "building_lead_mine", "pm_picks_and_shovels_building_lead_mine", "ADD_9_LEAD_MINE_LEVELS"),
        "furniture": (213, 51, -162, 105, "building_furniture_manufactory", "pm_handcrafted_furniture", "ADD_4_BRITISH_FURNITURE_LEVELS"),
        "luxury_clothes": (197, 80, -117, 70, "building_textile_mill", "pm_craftsman_sewing", "ADD_4_BRITISH_LUXURY_TEXTILE_LEVELS"),
        "fertilizer": (266, 16, -250, 52, "building_chemical_plant", "pm_artificial_fertilizers", "ADD_7_BRITISH_CHEMICAL_COMPLEX_LEVELS"),
        "groceries": (794, 330, -464, 52, "building_food_industry", "pm_bakery", "KEEP_12_BRITISH_FOOD_INDUSTRY_LEVELS"),
        "dye": (20, 0, -20, 70, "building_dye_plantation", "default_building_dye_plantation", "RAISE_FLORIDA_DYE_TO_2"),
        "salt": (172, 0, -172, 52, "building_salt_pan", "default_building_salt_pan", "ADD_24_SENEGAL_SALT_LEVELS"),
    }
    rows: list[dict[str, object]] = []
    for good, (buy, sell, balance, price, building, pm, decision) in captured.items():
        rows.append({
            "Market": "British Market", "Good": good, "Buy_Orders": buy, "Sell_Orders": sell,
            "Balance": balance, "Price": price, "Shortage_Status": "RED_SHORTAGE_AT_CAPTURE",
            "Main_Consumers": "RUNTIME_CAPTURE", "Current_Producers": building, "PMs": pm,
            "Potential_Domestic_Producers": "EXISTING_STATE_POTENTIAL_ONLY",
            "Import_Capacity": "NOT_USED_FOR_THIS_CORRECTION",
            "Historical_Shortage_Justification": "NONE; FIX",
            "Wave1_Decision": decision,
        })
    rows.append({
        "Market": "British Market", "Good": "tools", "Buy_Orders": "RUNTIME_RETEST",
        "Sell_Orders": "RUNTIME_RETEST", "Balance": "RUNTIME_RETEST", "Price": "RUNTIME_RETEST",
        "Shortage_Status": "EXPORT_DEPENDENCY_OBJECTIVE", "Main_Consumers": "BIC_AND_BRITISH_INDUSTRY",
        "Current_Producers": "building_tooling_workshop", "PMs": "pm_crude_tools",
        "Potential_Domestic_Producers": "LANCASHIRE|MIDLANDS", "Import_Capacity": "SHARED_MARKET",
        "Historical_Shortage_Justification": "NONE", "Wave1_Decision": "KEEP_10_ADDED_TOOLING_LEVELS",
    })
    write_csv(MARKET_AUDIT, fields, rows)

    supply_fields = [
        "Market", "Owner_TAG", "State_ID", "Building_ID", "Historical_Level", "Runtime_Additional_Level",
        "Runtime_Final_Target_Level", "PM_Change", "Trade_or_Port_Change", "Evidence", "Reason",
    ]
    levels, _, _ = runtime.actual_semantics()
    supply: list[dict[str, object]] = []
    for key, final in sorted({**ADDITIONS,
        ("GBR", "STATE_FLORIDA", "building_dye_plantation"): 2,
        ("GBR", "STATE_MIDLANDS", "building_chemical_plant"): 1,
    }.items()):
        if key in ADDITIONS:
            historical = 0
        elif key == ("GBR", "STATE_FLORIDA", "building_dye_plantation"):
            historical = 1
        else:
            historical = 0
        actual = levels.get(key, final)
        supply.append({
            "Market": "British Market", "Owner_TAG": key[0], "State_ID": key[1], "Building_ID": key[2],
            "Historical_Level": historical, "Runtime_Additional_Level": actual - historical,
            "Runtime_Final_Target_Level": actual, "PM_Change": "|".join(COLONIAL_PM.get(key[2], [])) or "MERGED_CHEMICAL_PM",
            "Trade_or_Port_Change": "NONE", "Evidence": "Supplied British-market runtime capture",
            "Reason": "Resolve confirmed red shortage; no new resource potential; BIC excluded.",
        })
    supply.append({
        "Market": "British Market", "Owner_TAG": "GBR", "State_ID": "STATE_MIDLANDS",
        "Building_ID": "building_chemical_works", "Historical_Level": 1, "Runtime_Additional_Level": -1,
        "Runtime_Final_Target_Level": 0, "PM_Change": "MIGRATED_TO_BUILDING_CHEMICAL_PLANT",
        "Trade_or_Port_Change": "NONE", "Evidence": "Tech & Res merged-building pattern",
        "Reason": "Remove the obsolete separate chemical-works building identifier.",
    })
    write_csv(SUPPLY_OVERLAY, supply_fields, supply)


def write_report(road_targets: dict[tuple[str, str, str], int]) -> None:
    road_text = ", ".join(
        f"{state.replace('STATE_', '')}={level}" for (_, state, _), level in sorted(road_targets.items())
    )
    REPORT.write_text(f"""# BUILD START 1776 — British market correction V2

## Runtime evidence

The supplied British-market capture showed red shortages for fruit (398), lead (174), furniture (162), luxury clothes (117), fertilizer (250), groceries (464), dye (20), and salt (172). Only those red-marked goods are treated as shortages.

## Placement policy

- No resource potential was added to the British Isles or anywhere else.
- Colonial extraction and plantations use existing potential outside BIC.
- British manufacturing remains in Lancashire, the Midlands and the West Country.
- The previously added ten tooling-workshop levels are retained to create the intended Indian dependence on British tools.
- The erroneous East Anglia dye, sugar and salt placements were removed. Apple-orchard PMs on the five added rye-farm blocks were disabled, restoring their grain focus.

## Capacity correction

- Fruit: 8 banana levels in Jamaica and 6 in the British West Indies (420 theoretical output).
- Dye: Florida raised from 1 to 2 levels (60 theoretical output).
- Lead: 4 levels in Newfoundland and 5 in the West Country (180 theoretical output).
- Furniture: 4 handcrafted levels in the West Country (180 theoretical output).
- Luxury clothes: 4 craftsman-sewing textile levels in the West Country (120 theoretical output).
- Fertilizer: 7 early fertilizer lines in Lancashire (280 theoretical output).
- Groceries: the 12 Home Counties bakery levels are retained (500 theoretical output from the ten-level runtime increase).
- Salt: 24 levels in Senegal (240 theoretical output), within its pre-existing 30-level salt potential. A level-1 anchorage connects the colonial state to the British market. The salt works are owned by British capitalists.
- Inputs: 3 limestone levels in the Bahamas, 2 in Florida, and 3 logging levels in Jamaica support the new chains. No BIC building was used.
- The prior HBC fishery addition receives one traditional-road level in Manitoba, Ontario and Quebec; this closes the three infrastructure gaps created after Wave 1.

## Chemical consolidation (Tech & Res pattern)

The local subscribed `[1.13] Tech & Res` mod at `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3472248460` was used as the structural reference: fertilizer and industrial-chemical production now coexist as separate PM groups in the canonical `building_chemical_plant`.

The complex unlocks at `industrial_acids`, which Great Britain already possesses. The obsolete `artificial_fertilizers` technology was removed; `improved_fertilizer` now requires `advanced_crop_rotations` and `industrial_acids` directly. The early fertilizer PM uses limestone and tools; the fork's phosphate input is preserved in the improved and nitrogen-fixation PMs, where the advanced mining chain is appropriate. The obsolete separate `building_chemical_works` definition and placement were removed/migrated.

## Infrastructure

Road levels were recalculated after the supply write against effective building-group usage and the +2 AI surplus target: {road_text}. No rail or passenger PM was introduced.

## Required runtime retest

Reload the mod and inspect the British market after employment stabilizes. Static capacity resolves the captured orders, but final prices and the BIC dependence score remain runtime outcomes.
""", encoding="utf-8")


def main() -> None:
    if OVERLAY.exists():
        OVERLAY.unlink()
    apply_existing_edits()
    write_supply_buildings()
    road_targets = set_exact_roads()
    update_infrastructure_reports()
    update_matrix(road_targets)
    update_market_reports()
    write_report(road_targets)

    levels, _, _ = runtime.actual_semantics()
    for key, expected in ADDITIONS.items():
        if levels.get(key, 0) != expected:
            raise RuntimeError(f"Final level mismatch for {key}: {levels.get(key, 0)} != {expected}")
    if levels.get(("GBR", "STATE_MIDLANDS", "building_chemical_works"), 0):
        raise RuntimeError("Obsolete chemical works placement remains")
    print(f"British market correction applied; {len(ADDITIONS)} new placement rows; roads={road_targets}")


if __name__ == "__main__":
    main()
