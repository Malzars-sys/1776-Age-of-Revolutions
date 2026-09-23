#!/usr/bin/env python3
"""BUILD START 1776 runtime calibration wave 1.

This pass is deliberately layered over the frozen historical V2 matrix.  It
calibrates only deterministic state infrastructure, the user-authorized
deincorporation profiles, and small administrative reinforcements.  Market
orders are runtime-only data, so supply and trade rows remain explicit retest
items rather than fabricated corrections.
"""

from __future__ import annotations

import argparse
import csv
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import build_start_1776_blocker_resolution as blocker
import build_start_1776_research_input_pack as catalog_tools
import build_start_1776_world_apply as world


ROOT = Path(__file__).resolve().parents[1]
VANILLA = Path(r"C:\Games\Victoria 3\game")
REPORTS = ROOT / "docs" / "reports" / "buildings"
HISTORY = ROOT / "common" / "history" / "buildings"
STATE_HISTORY = ROOT / "common" / "history" / "states" / "00_states.txt"
RUNTIME_BUILDING_OVERLAY = HISTORY / "97_build_start_1776_runtime_wave1.txt"

BASE_MATRIX = REPORTS / "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv"
STATE_CATALOG = REPORTS / "BUILD_START_1776_STATE_CATALOG.csv"
BASE_INFRA_PLAN = REPORTS / "BUILD_START_1776_INFRASTRUCTURE_PM_PLAN.csv"
BASE_ADMIN = REPORTS / "BUILD_START_1776_ADMINISTRATION_CALIBRATION.csv"
DEINCORP_SCREEN = REPORTS / "BUILD_START_1776_ADMINISTRATION_DEINCORPORATION_RUNTIME_PLAN.csv"
FALLBACKS = REPORTS / "BUILD_START_1776_PM_GATE_FALLBACKS.csv"

INFRA_AUDIT = REPORTS / "BUILD_START_1776_RUNTIME_INFRASTRUCTURE_AUDIT.csv"
INFRA_OVERLAY = REPORTS / "BUILD_START_1776_RUNTIME_INFRASTRUCTURE_OVERLAY.csv"
ACCESS_EXCEPTIONS = REPORTS / "BUILD_START_1776_MARKET_ACCESS_HISTORICAL_EXCEPTIONS.csv"
DEINCORP_REVIEW = REPORTS / "BUILD_START_1776_DEINCORPORATION_HISTORICAL_REVIEW.csv"
BUREAUCRACY_AUDIT = REPORTS / "BUILD_START_1776_RUNTIME_BUREAUCRACY_AUDIT.csv"
ADMIN_OVERLAY = REPORTS / "BUILD_START_1776_RUNTIME_ADMINISTRATION_OVERLAY.csv"
MARKET_AUDIT = REPORTS / "BUILD_START_1776_RUNTIME_MARKET_GOODS_AUDIT.csv"
FALLBACK_IMPACT = REPORTS / "BUILD_START_1776_RUNTIME_PM_FALLBACK_IMPACT.csv"
SHORTAGE_EXCEPTIONS = REPORTS / "BUILD_START_1776_HISTORICAL_STARTING_SHORTAGES.csv"
SUPPLY_OVERLAY = REPORTS / "BUILD_START_1776_RUNTIME_MARKET_SUPPLY_OVERLAY.csv"
RUNTIME_MATRIX = REPORTS / "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_RUNTIME_V1.csv"
REPORT = REPORTS / "BUILD_START_1776_RUNTIME_CALIBRATION_WAVE1_REPORT.md"

ADMIN = "building_government_administration"
INFRA = "building_railway"
BASE_INFRASTRUCTURE = 3.0
DESIRED_SURPLUS = 2.0  # PRODUCTION_BUILDING_DESIRED_INFRASTRUCTURE_SURPLUS

KNOWN_RUNTIME_BALANCE = {
    "FRA": 52.5,
    "GBR": -829.0,
    "CHI": -11100.0,
}

# Explicitly authorized by the historical criteria note and the user.  Qing
# frontier states already marked unincorporated are not rewritten.
DEINCORPORATIONS = {
    ("GBR", "STATE_HIGHLANDS"): (
        "HISTORICALLY_ELIGIBLE_HIGH_AUTONOMY",
        "Scotland retained a distinct constitutional, legal and institutional settlement; user-authoritative example.",
    ),
    ("GBR", "STATE_LOWLANDS"): (
        "HISTORICALLY_ELIGIBLE_HIGH_AUTONOMY",
        "Scotland retained a distinct constitutional, legal and institutional settlement; user-authoritative example.",
    ),
    ("GBR", "STATE_WALES"): (
        "HISTORICALLY_ELIGIBLE_WEAK_INTEGRATION",
        "User-authoritative runtime compromise for weaker Welsh fiscal-administrative integration; historically less distinct than Scotland.",
    ),
    ("CHI", "STATE_YUNNAN"): (
        "HISTORICALLY_ELIGIBLE_WEAK_INTEGRATION",
        "Selected southern Qing territory with long-standing high local autonomy; user-authoritative profile.",
    ),
    ("CHI", "STATE_GUIZHOU"): (
        "HISTORICALLY_ELIGIBLE_INDIRECT_RULE",
        "Selected southern Qing territory represented through indirect/local administration; user-authoritative profile.",
    ),
    ("CHI", "STATE_GUANGXI"): (
        "HISTORICALLY_ELIGIBLE_HIGH_AUTONOMY",
        "Selected southern Qing territory with materially weaker direct fiscal integration; user-authoritative profile.",
    ),
}

# Runtime anchor: Scotland and Wales save about 165 bureaucracy, then 67
# simple-organization levels distributed across the principal English
# administrative regions close the observed British -829 balance.  China
# receives only a modest ten simple-organization levels, split between its
# established administrative centers; this intentionally does not hide its
# population burden.
ADMIN_ADDITIONS = {
    ("GBR", "STATE_HOME_COUNTIES", ADMIN): 37,
    ("GBR", "STATE_LANCASHIRE", ADMIN): 14,
    ("GBR", "STATE_MIDLANDS", ADMIN): 9,
    ("GBR", "STATE_YORKSHIRE", ADMIN): 7,
    ("CHI", "STATE_BEIJING", ADMIN): 5,
    ("CHI", "STATE_NANJING", ADMIN): 5,
}

MARKETS = [
    "British Market", "French Market", "Russian Market", "Chinese Market",
    "Japanese Market", "Austrian Market", "Ottoman Market", "Spanish Market",
    "American Market", "Iranian Market",
]
PRIORITY_GOODS = [
    "wood", "grain", "fabric", "clothes", "paper", "tools", "iron", "coal",
    "liquor", "groceries", "small_arms", "artillery", "ammunition", "merchant_marine",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def number(text: str, key: str, default: float = 0.0) -> float:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*(-?\d+(?:\.\d+)?)", text)
    return float(match.group(1)) if match else default


def token(text: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*\"?([A-Za-z0-9_]+)", text)
    return match.group(1) if match else ""


def split_pms(value: str) -> list[str]:
    return [item for item in value.split("|") if item and item != "NONE"]


def actual_semantics() -> tuple[dict[tuple[str, str, str], int], dict[tuple[str, str, str], tuple[str, ...]], list[world.Placement]]:
    _, placements = world.all_placements(HISTORY)
    levels: dict[tuple[str, str, str], int] = defaultdict(int)
    pms: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for placement in placements:
        levels[placement.key] += placement.level
        pms[placement.key].update(placement.pms)
    return dict(levels), {key: tuple(sorted(value)) for key, value in pms.items()}, placements


def effective_infrastructure_usage() -> tuple[dict[str, float], dict[str, str]]:
    groups = catalog_tools.effective_objects("common/building_groups", r"bg_[A-Za-z0-9_]+")
    buildings = catalog_tools.effective_objects("common/buildings", r"building_[A-Za-z0-9_]+")
    cache: dict[str, float] = {}

    def group_usage(group: str, seen: set[str] | None = None) -> float:
        if group in cache:
            return cache[group]
        seen = set() if seen is None else seen
        if group in seen or group not in groups:
            return 0.0
        seen.add(group)
        text = groups[group].text
        if re.search(r"(?m)^\s*infrastructure_usage_per_level\s*=", text):
            value = number(text, "infrastructure_usage_per_level")
        else:
            parent = token(text, "parent_group")
            value = group_usage(parent, seen) if parent else 0.0
        cache[group] = value
        return value

    building_group = {building: token(block.text, "building_group") for building, block in buildings.items()}
    return {building: group_usage(group) for building, group in building_group.items()}, building_group


def state_trait_infrastructure() -> dict[str, float]:
    trait_objects = catalog_tools.effective_objects("common/state_traits", r"[A-Za-z0-9_]+")
    trait_values = {
        trait: number(block.text, "state_infrastructure_add")
        for trait, block in trait_objects.items()
    }
    result: dict[str, float] = defaultdict(float)
    for path in sorted((ROOT / "map_data" / "state_regions").glob("*.txt")):
        for block in catalog_tools.named_blocks(path, r"STATE_[A-Za-z0-9_]+", 1):
            traits = catalog_tools.braced_tokens(block.text, "traits")
            result[block.object_id] += sum(trait_values.get(trait, 0.0) for trait in traits)
    return dict(result)


def fixed_infra_per_level(pms: list[str], pm_objects: dict[str, catalog_tools.Block]) -> float:
    return sum(number(pm_objects[pm].text, "state_infrastructure_add") for pm in pms if pm in pm_objects)


def infrastructure_plan(
    state_rows: list[dict[str, str]],
    levels: dict[tuple[str, str, str], int],
    pms: dict[tuple[str, str, str], tuple[str, ...]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[tuple[str, str, str], int], dict[tuple[str, str], dict[str, str]]]:
    usage_by_building, _ = effective_infrastructure_usage()
    state_traits = state_trait_infrastructure()
    pm_objects = catalog_tools.effective_objects("common/production_methods", r"[A-Za-z0-9_]+")
    historical_plan = {(row["Owner_TAG"], row["State_ID"]): row for row in read_csv(BASE_INFRA_PLAN)}
    state_pairs = {(row["Owner_TAG"], row["State_ID"]) for row in state_rows}

    used: dict[tuple[str, str], float] = defaultdict(float)
    for (owner, state, building), level in levels.items():
        if (owner, state) in state_pairs:
            used[(owner, state)] += level * usage_by_building.get(building, 0.0)

    audit: list[dict[str, object]] = []
    overlay: list[dict[str, object]] = []
    targets: dict[tuple[str, str, str], int] = {}
    final_plans: dict[tuple[str, str], dict[str, str]] = {}
    for state_row in sorted(state_rows, key=lambda row: (row["Owner_TAG"], row["State_ID"])):
        owner, state = state_row["Owner_TAG"], state_row["State_ID"]
        key = (owner, state, INFRA)
        current = levels.get(key, 0)
        plan = historical_plan.get((owner, state))
        if plan:
            road, canal = plan["Road_PM"], plan["Canal_PM"]
            rail, passenger = plan["Rail_PM"], plan["Passenger_PM"]
            evidence = plan["Historical_Rationale"]
        else:
            active = set(pms.get(key, ()))
            road = next((pm for pm in active if pm.startswith("pm_") and "road" in pm), "pm_traditional_road_network")
            canal = next((pm for pm in active if "canal" in pm), "pm_no_canal_network")
            rail = next((pm for pm in active if "rail" in pm), "pm_no_rail_network")
            passenger = next((pm for pm in active if "passenger" in pm), "pm_no_passenger_trains")
            evidence = "No prior historical transport row; gameplay capacity uses the least-modern road PM."
        selected = [road, canal, rail, passenger]
        per_level = fixed_infra_per_level(selected, pm_objects)
        if per_level <= 0:
            road, canal, rail, passenger = (
                "pm_traditional_road_network", "pm_no_canal_network",
                "pm_no_rail_network", "pm_no_passenger_trains",
            )
            selected = [road, canal, rail, passenger]
            per_level = fixed_infra_per_level(selected, pm_objects)
        non_network = BASE_INFRASTRUCTURE + state_traits.get(state, 0.0)
        available = non_network + current * per_level
        infrastructure_used = used.get((owner, state), 0.0)
        needed = max(current, math.ceil(max(0.0, infrastructure_used + DESIRED_SURPLUS - non_network) / per_level))
        if owner in world.SERENISSIMA:
            needed = current
        targets[key] = needed
        final_plans[(owner, state)] = {
            "Road_PM": road, "Canal_PM": canal, "Rail_PM": rail, "Passenger_PM": passenger,
        }
        before_access = 100.0 if infrastructure_used <= available or infrastructure_used <= 0 else min(100.0, 100.0 * available / infrastructure_used)
        final_available = non_network + needed * per_level
        runtime_access = "51_RUNTIME" if owner == "FRA" and state == "STATE_CHAMPAGNE" else f"{before_access:.1f}_PROJECTED"
        reason = (
            f"Target satisfies usage {infrastructure_used:.1f} plus engine AI surplus {DESIRED_SURPLUS:.0f}; "
            f"fixed capacity {per_level:.1f} per level; no rail or passenger service."
        )
        row = {
            "Owner_TAG": owner,
            "Country": state_row["Owner_Name"],
            "State_ID": state,
            "State_Name": state_row["State_Display_Name"],
            "Current_Level": current,
            "Road_PM": road,
            "Canal_PM": canal,
            "Rail_PM": rail,
            "Passenger_PM": passenger,
            "Infrastructure_Available": f"{available:.1f}",
            "Infrastructure_Used": f"{infrastructure_used:.1f}",
            "Current_Market_Access": runtime_access,
            "Additional_Level_Needed": max(0, needed - current),
            "Historical_Connectivity_Exception": "NO",
            "Evidence": evidence,
            "Final_Target_Level": needed,
            "Final_Infrastructure_Available": f"{final_available:.1f}",
            "Reason": reason,
        }
        audit.append(row)
        if needed > current:
            overlay.append({
                "Owner_TAG": owner,
                "Country": state_row["Owner_Name"],
                "State_ID": state,
                "State_Name": state_row["State_Display_Name"],
                "Building_ID": INFRA,
                "Historical_Level": current,
                "Runtime_Additional_Level": needed - current,
                "Runtime_Final_Target_Level": needed,
                "Road_PM": road,
                "Canal_PM": canal,
                "Rail_PM": rail,
                "Passenger_PM": passenger,
                "Capacity_Per_Level": f"{per_level:.1f}",
                "Reason": reason,
            })
    return audit, overlay, targets, final_plans


def rescale_existing(
    placements: list[world.Placement],
    targets: dict[tuple[str, str, str], int],
    plans: dict[tuple[str, str], dict[str, str]],
) -> tuple[dict[Path, str], list[tuple[str, str, str, int, str]]]:
    by_key: dict[tuple[str, str, str], list[world.Placement]] = defaultdict(list)
    for placement in placements:
        by_key[placement.key].append(placement)
    raw_by_path = {path: path.read_text(encoding="utf-8-sig") for path in {p.path for p in placements if p.path.is_relative_to(ROOT)}}
    changes: dict[Path, list[tuple[int, int, str]]] = defaultdict(list)
    additions: list[tuple[str, str, str, int, str]] = []

    _, vanilla_placements = world.all_placements(VANILLA / "common" / "history" / "buildings")
    templates: dict[str, world.Placement] = {}
    for placement in placements + vanilla_placements:
        templates.setdefault(placement.building, placement)

    for key, target in sorted(targets.items()):
        current = sum(item.level for item in by_key.get(key, []))
        if target == current:
            continue
        existing = by_key.get(key, [])
        if existing:
            first = existing[0]
            block = world.rescale_ownership(first.text, target)
            if key[2] == INFRA:
                plan = plans[(key[0], key[1])]
                block = world.replace_active_pms(block, [
                    plan["Road_PM"], plan["Canal_PM"], plan["Rail_PM"], plan["Passenger_PM"]
                ])
            changes[first.path].append((first.start, first.end, block))
            for duplicate in existing[1:]:
                changes[duplicate.path].append((duplicate.start, duplicate.end, ""))
        elif target > 0:
            template = next(
                (
                    item for item in placements
                    if item.owner == key[0] and item.building == key[2]
                ),
                templates[key[2]],
            )
            if key[2] == INFRA:
                plan = plans[(key[0], key[1])]
                selected_pms = [plan["Road_PM"], plan["Canal_PM"], plan["Rail_PM"], plan["Passenger_PM"]]
            else:
                selected_pms = list(template.pms)
            block = world.transform_template(template, key[0], key[1], target, selected_pms)
            additions.append((key[0], key[1], key[2], target, block))

    transformed = dict(raw_by_path)
    for path, replacements in changes.items():
        raw = transformed[path]
        for start, end, replacement in sorted(replacements, reverse=True):
            raw = raw[:start] + replacement + raw[end:]
        catalog_tools.brace_maps(catalog_tools.clean_comments(raw))
        transformed[path] = raw
    return transformed, additions


def patch_state_history(raw: str, owner: str, state: str) -> str:
    state_spans = world.block_spans(raw, rf"s:{re.escape(state)}", 1)
    if len(state_spans) != 1:
        raise RuntimeError(f"Expected one state block for {state}, got {len(state_spans)}")
    _, state_start, state_end = state_spans[0]
    current_text = raw[state_start:state_end]
    creates = world.block_spans(current_text, r"create_state", 1)
    chosen = next((item for item in creates if re.search(rf"\bcountry\s*=\s*c:{owner}\b", current_text[item[1]:item[2]])), None)
    if not chosen:
        raise RuntimeError(f"No create_state for {owner}/{state}")
    _, start, end = chosen
    create = current_text[start:end]
    if re.search(r"(?m)^\s*state_type\s*=\s*unincorporated\b", create):
        create = re.sub(
            r"\n[ \t]+\n(?=[ \t]*state_type\s*=\s*unincorporated\b)",
            "\n\n",
            create,
        )
        state_new = current_text[:start] + create + current_text[end:]
        return raw[:state_start] + state_new + raw[state_end:]
    closing = create.rfind("}")
    create = create[:closing].rstrip() + "\n\n\t\t\tstate_type = unincorporated\n\t\t" + create[closing:]
    state_new = current_text[:start] + create + current_text[end:]
    return raw[:state_start] + state_new + raw[state_end:]


def pm_output(pm: str, pm_objects: dict[str, catalog_tools.Block]) -> float:
    if pm not in pm_objects:
        return 0.0
    return number(pm_objects[pm].text, "country_bureaucracy_add")


def bureaucracy_reports(
    state_rows: list[dict[str, str]],
    levels: dict[tuple[str, str, str], int],
    pms: dict[tuple[str, str, str], tuple[str, ...]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    state_by_pair = {(row["Owner_TAG"], row["State_ID"]): row for row in state_rows}
    states_by_tag: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in state_rows:
        states_by_tag[row["Owner_TAG"]].append(row)
    incorporated = blocker.state_incorporation()
    pm_objects = catalog_tools.effective_objects("common/production_methods", r"[A-Za-z0-9_]+")

    reduction_by_tag: dict[str, float] = defaultdict(float)
    selected_by_tag: dict[str, list[str]] = defaultdict(list)
    for owner, state in DEINCORPORATIONS:
        pop = int(state_by_pair[(owner, state)]["Current_Population"])
        reduction_by_tag[owner] += 10 + 4 * pop / 100_000
        selected_by_tag[owner].append(state)

    additions_by_tag: dict[str, int] = defaultdict(int)
    output_by_tag: dict[str, float] = defaultdict(float)
    for key, delta in ADMIN_ADDITIONS.items():
        additions_by_tag[key[0]] += delta
        active = pms.get(key, ())
        base = next((pm for pm in active if pm in {"pm_simple_organization", "pm_horizontal_drawer_cabinets", "pm_vertical_filing_cabinets", "pm_switch_boards"}), "pm_simple_organization")
        output_by_tag[key[0]] += delta * pm_output(base, pm_objects)

    audit: list[dict[str, object]] = []
    for tag, owned in sorted(states_by_tag.items()):
        admin_levels = sum(level for (owner, _, building), level in levels.items() if owner == tag and building == ADMIN)
        final_levels = admin_levels + additions_by_tag[tag]
        static_gross = 0.0
        for key, level in levels.items():
            if key[0] != tag or key[2] != ADMIN:
                continue
            active = pms.get(key, ())
            base = next((pm for pm in active if pm in {"pm_simple_organization", "pm_horizontal_drawer_cabinets", "pm_vertical_filing_cabinets", "pm_switch_boards"}), "pm_simple_organization")
            static_gross += level * pm_output(base, pm_objects)
        inc_states = [row for row in owned if incorporated.get(row["State_ID"], True)]
        static_cost = 10 * len(inc_states) + 4 * sum(int(row["Current_Population"]) for row in inc_states) / 100_000
        observed = KNOWN_RUNTIME_BALANCE.get(tag)
        before = observed if observed is not None else static_gross - static_cost
        projected = before + reduction_by_tag[tag] + output_by_tag[tag]
        if projected >= 0:
            status = "HEALTHY"
        elif projected >= -100:
            status = "MANAGEABLE_DEFICIT"
        elif projected >= -500:
            status = "SEVERE_DEFICIT"
        else:
            status = "CATASTROPHIC_DEFICIT"
        country = owned[0]["Owner_Name"]
        audit.append({
            "TAG": tag,
            "Country": country,
            "Current_Admin_Levels": admin_levels,
            "Runtime_Bureaucracy_Balance": f"{observed:.1f}" if observed is not None else f"NOT_OBSERVED; STATIC={before:.1f}",
            "Historically_Eligible_Deincorporations": "|".join(sorted(selected_by_tag[tag])) or "NONE",
            "Projected_Balance_After_Deincorporation": f"{before + reduction_by_tag[tag]:.1f}",
            "Additional_Admin_Needed": additions_by_tag[tag],
            "Final_Admin_Target": final_levels,
            "Projected_Final_Balance": f"{projected:.1f}",
            "Runtime_Target_Status": status,
            "Notes": (
                "Observed runtime anchor used." if observed is not None else
                "Static state-cost estimate only; requires runtime observation before any further write."
            ),
        })

    overlay: list[dict[str, object]] = []
    for key, delta in sorted(ADMIN_ADDITIONS.items()):
        row = state_by_pair[(key[0], key[1])]
        current = levels.get(key, 0)
        overlay.append({
            "Owner_TAG": key[0], "Country": row["Owner_Name"], "State_ID": key[1],
            "State_Name": row["State_Display_Name"], "Building_ID": ADMIN,
            "Historical_Level": current, "Runtime_Additional_Level": delta,
            "Runtime_Final_Target_Level": current + delta,
            "Reason": "Runtime bureaucracy anchor after historically justified deincorporation; no tax-capacity normalization.",
        })
    return audit, overlay


def deincorporation_review(state_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    by_pair = {(row["Owner_TAG"], row["State_ID"]): row for row in state_rows}
    screened = read_csv(DEINCORP_SCREEN)
    keys = {(row["Owner_TAG"], row["State_ID"]) for row in screened} | set(DEINCORPORATIONS)
    screened_by_key = {(row["Owner_TAG"], row["State_ID"]): row for row in screened}
    rows: list[dict[str, object]] = []
    for key in sorted(keys):
        state = by_pair.get(key)
        old = screened_by_key.get(key, {})
        selected = DEINCORPORATIONS.get(key)
        if selected:
            classification, evidence = selected
            decision = "APPLY"
        else:
            classification = "RESEARCH_REQUIRED"
            evidence = "The old numerical screening is not historical evidence; no explicit repository justification was found in this wave."
            decision = "NO_WRITE"
        rows.append({
            "Owner_TAG": key[0],
            "Country": state["Owner_Name"] if state else old.get("Country", ""),
            "State_ID": key[1],
            "State_Name": state["State_Display_Name"] if state else old.get("State_Name", ""),
            "Current_Population": state["Current_Population"] if state else old.get("Current_Population", ""),
            "Old_Numerical_Priority": old.get("Priority", "NOT_IN_OLD_SCREEN"),
            "Classification": classification,
            "Evidence": evidence,
            "Wave1_Decision": decision,
        })
    return rows


def goods_outputs(pm: str, objects: dict[str, catalog_tools.Block]) -> dict[str, float]:
    if pm not in objects:
        return {}
    result: dict[str, float] = defaultdict(float)
    for good, value in re.findall(r"goods_output_([A-Za-z0-9_]+)_add\s*=\s*(-?\d+(?:\.\d+)?)", objects[pm].text):
        result[good] += float(value)
    return dict(result)


def format_goods(values: dict[str, float]) -> str:
    return "|".join(f"{good}:{value:g}" for good, value in sorted(values.items())) or "NONE"


def market_reports() -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    observed_markets = {"British Market", "Russian Market", "Chinese Market", "Japanese Market", "Austrian Market", "Iranian Market"}
    market_rows = []
    for market in MARKETS:
        for good in PRIORITY_GOODS:
            market_rows.append({
                "Market": market, "Good": good, "Buy_Orders": "RUNTIME_NOT_CAPTURED",
                "Sell_Orders": "RUNTIME_NOT_CAPTURED", "Balance": "RUNTIME_NOT_CAPTURED",
                "Price": "RUNTIME_NOT_CAPTURED",
                "Shortage_Status": "GENERAL_DEFICITS_REPORTED; RETEST_REQUIRED" if market in observed_markets else "RETEST_REQUIRED",
                "Main_Consumers": "RUNTIME_INSPECTION_REQUIRED", "Current_Producers": "STATIC_PLACEMENTS_AVAILABLE; MARKET_AGGREGATE_REQUIRED",
                "PMs": "SEE_RUNTIME_PM_FALLBACK_IMPACT", "Potential_Domestic_Producers": "DO_NOT_ADD_BEFORE_POST_INFRA_RETEST",
                "Import_Capacity": "RUNTIME_INSPECTION_REQUIRED", "Historical_Shortage_Justification": "NONE_FOUND",
                "Wave1_Decision": "RETEST_AFTER_INFRASTRUCTURE",
            })

    pm_objects = catalog_tools.effective_objects("common/production_methods", r"[A-Za-z0-9_]+")
    fallback_rows = []
    for row in read_csv(FALLBACKS):
        before = goods_outputs(row["Old_PM"], pm_objects)
        after = goods_outputs(row["Fallback_Base_PM"], pm_objects)
        goods = sorted(set(before) | set(after))
        delta = {good: after.get(good, 0.0) - before.get(good, 0.0) for good in goods}
        fallback_rows.append({
            **row,
            "Output_Before": format_goods(before),
            "Output_After": format_goods(after),
            "Output_Delta": format_goods(delta),
            "Runtime_Market_Link": "RETEST_REQUIRED",
            "Shortage_Impact": "CANNOT_BE_DETERMINED_WITHOUT_MARKET_ORDERS",
            "Wave1_Change": "NO",
            "Decision": "KEEP_TECH_VALID_FALLBACK_PENDING_POST_INFRA_RUNTIME",
        })
    return market_rows, fallback_rows


def runtime_matrix(
    base_rows: list[dict[str, str]],
    target_changes: dict[tuple[str, str, str], int],
    state_rows: list[dict[str, str]],
) -> list[dict[str, object]]:
    by_key = {(row["Owner_TAG"], row["State_ID"], row["Building_ID"]): row for row in base_rows}
    state_by_pair = {(row["Owner_TAG"], row["State_ID"]): row for row in state_rows}
    output: list[dict[str, object]] = []
    for key in sorted(set(by_key) | set(target_changes)):
        base = dict(by_key.get(key, {}))
        if not base:
            state = state_by_pair[(key[0], key[1])]
            base = {name: "" for name in base_rows[0]}
            base.update({
                "Research_Region": state["Region"], "Owner_TAG": key[0], "Country": state["Owner_Name"],
                "State_ID": key[1], "State_Name": state["State_Display_Name"], "Building_ID": key[2],
                "Building_Name": "Regional Infrastructure" if key[2] == INFRA else "Government Administration",
                "Current_Level": 0, "Target_Level": 0, "Delta": 0, "Decision": "RUNTIME_ADD",
                "Confidence": "RUNTIME_DETERMINISTIC", "Serenissima_Protected": "NO",
                "Historical_Evidence": "No historical placement; runtime capacity overlay only.",
                "Level_Rationale": "Runtime capacity requirement.", "Base_Historical_Target_Level": 0,
                "Overlay_Type": "RUNTIME_WAVE1", "Overlay_Reason": "Deterministic gameplay capacity.",
            })
        historical_target = int(float(base.get("Target_Level") or 0))
        final_target = target_changes.get(key, historical_target)
        row: dict[str, object] = dict(base)
        row.update({
            "Runtime_Base_Target_Level": historical_target,
            "Runtime_Level_Delta": final_target - historical_target,
            "Runtime_Final_Target_Level": final_target,
            "Runtime_Overlay_Type": "RUNTIME_WAVE1" if final_target != historical_target else "NONE",
            "Runtime_Overlay_Reason": (
                "Infrastructure capacity to usage plus engine surplus" if key[2] == INFRA and final_target != historical_target
                else "Runtime bureaucracy calibration" if key[2] == ADMIN and final_target != historical_target
                else "Frozen V2 historical target"
            ),
        })
        # The final validator consumes Target_Level, while provenance remains in
        # Runtime_Base_Target_Level.
        row["Target_Level"] = final_target
        row["Delta"] = final_target - int(float(base.get("Current_Level") or 0))
        if final_target != historical_target:
            row["Decision"] = "RUNTIME_INCREASE" if historical_target else "RUNTIME_ADD"
        output.append(row)
    return output


def report_text(
    infra_audit: list[dict[str, object]],
    infra_overlay: list[dict[str, object]],
    bureaucracy: list[dict[str, object]],
    fallback_count: int,
    deincorp_count: int,
    admin_before: int,
    admin_after: int,
) -> str:
    by_tag = {row["TAG"]: row for row in bureaucracy}
    below_before = sum(float(row["Infrastructure_Used"]) > float(row["Infrastructure_Available"]) for row in infra_audit)
    levels_added = sum(int(row["Runtime_Additional_Level"]) for row in infra_overlay)
    return f"""# BUILD START 1776 — Runtime calibration Wave 1

> Superseded for population and bureaucracy by `BUILD_START_1776_RUNTIME_CALIBRATION_WAVE2_REPORT.md`. Infrastructure and market-audit provenance from this wave remains valid.

## 1. Runtime observations

France starts near viability (`+52.5` bureaucracy). Great Britain starts at about `-829`, China at about `-11.1K`, and Champagne was observed at `51%` market access with `5 / 3` infrastructure.

## 2. Infrastructure failure

The audit covers **{len(infra_audit)}** owner/state pairs. **{below_before}** pairs were statically below capacity before this overlay. Infrastructure use is calculated from effective building-group usage. Available infrastructure includes the engine base value of 3, fixed state-trait infrastructure and fixed road/canal output.

## 3. Market-access calibration

The target is `usage + 2`, using the engine AI define `PRODUCTION_BUILDING_DESIRED_INFRASTRUCTURE_SURPLUS = 2`. Variable population/automobile road bonuses and automatic urban-center output are excluded, making the target conservative. **{levels_added}** regional-infrastructure levels were added. Every new row uses traditional roads, no canals unless already historically validated, no rail and no passenger trains.

## 4. Historical market-access exceptions

None were proven from the existing repository research. The exceptions CSV is intentionally empty. Serenissima remains protected and unchanged.

## 5. Bureaucracy

The pass does not target 100% taxation. Only the three supplied runtime anchors are treated as observed; other countries remain static estimates and require a runtime retest.

## 6. Historical deincorporation

**{deincorp_count}** selected cases were applied: the two Scottish regions, Wales, and Yunnan, Guizhou and Guangxi. Scotland and the three Qing regions follow the historical-autonomy rule; Wales is an explicit user-authoritative gameplay compromise and is labelled as such in the audit. Every old numerical candidate without independent repository evidence remains `RESEARCH_REQUIRED` and was not written.

## 7. Great Britain

Scotland and Wales reduce the structural burden by about 165. Sixty-seven simple-organization administration levels were distributed across Home Counties, Lancashire, the Midlands and Yorkshire. Projected balance: **{by_tag['GBR']['Projected_Final_Balance']}** from the observed `-829` anchor.

## 8. China

The three selected southern states reduce the structural burden by about 1,063. Ten simple-organization levels were split between Beijing and Nanjing. Projected balance: **{by_tag['CHI']['Projected_Final_Balance']}**. This remains a catastrophic deficit: fully cancelling it would require mass core deincorporation or hundreds of simple-administration levels, both explicitly forbidden. It is therefore a documented runtime/design blocker, not hidden by an ahistorical write.

## 9. Other severe deficits

Rows without observed balances are classified from the static state-cost model only. No automatic writes were made from that unreliable estimate.

## 10. Market shortages

The open game window was not exposed to the control interface, and the prompt provides no per-good orders/prices. Ten named markets and fourteen priority goods are recorded as post-infrastructure runtime checks. No shortage is falsely declared solved.

## 11. PM fallback impact

All **{fallback_count}** fallback rows were audited for scripted output before/after. None is changed before the post-infrastructure market retest.

## 12. Supply corrections

None in this wave. Existing producer geography remains authoritative until market orders identify a genuine non-historical shortage after access is fixed.

## 13. Trade/import corrections

None in this wave. Import dependence and port/trade capacity require market-level runtime evidence.

## 14. Historical shortage exceptions

None documented; the file is empty. The default remains `FIX` once a real shortage is confirmed.

## 15. Protected systems

VEN and GEN, barracks, naval administration and naval fortifications are unchanged. The four military technology reviews remain reviews. No military or naval resizing occurs.

## 16. Files modified

Runtime reports/overlays, the combined runtime matrix, deterministic building history, and six targeted state incorporation statuses. The frozen V2 matrix is not rewritten.

## 17. Static revalidation

Run `build_start_1776_final_validate.py` against the runtime matrix, then `git diff --check`. Required invariants remain zero, including active rail/passenger service and protected semantic changes.

## 18. Runtime retest checklist

1. Start a new 1776 game (the current save cannot reload history changes).
2. Confirm Champagne and Rhône have no infrastructure penalty.
3. Inspect one dense state per major market and every state still below 100% access; distinguish connection penalties from infrastructure penalties.
4. Record bureaucracy for FRA, GBR, CHI, RUS, TUR, JAP, SPA, AUS and USA.
5. For each flagged good, record buy orders, sell orders, price and the actual shortage icon after infrastructure employment stabilizes.
6. Only then authorize PM, supply or trade corrections.

Administration levels: **{admin_before} → {admin_after}**.
"""


def apply() -> dict[str, object]:
    state_rows = read_csv(STATE_CATALOG)
    base_matrix = read_csv(BASE_MATRIX)
    levels, pms, placements = actual_semantics()
    protected_before = world.semantic(placements, lambda row: row.owner in world.SERENISSIMA or row.building in world.PROTECTED)

    infra_audit, infra_overlay, infra_targets, plans = infrastructure_plan(state_rows, levels, pms)
    bureaucracy, admin_overlay = bureaucracy_reports(state_rows, levels, pms)
    deincorp_rows = deincorporation_review(state_rows)
    market_rows, fallback_rows = market_reports()

    building_targets = dict(infra_targets)
    for key, delta in ADMIN_ADDITIONS.items():
        building_targets[key] = levels.get(key, 0) + delta

    transformed, additions = rescale_existing(placements, building_targets, plans)
    for path, raw in transformed.items():
        if raw != path.read_text(encoding="utf-8-sig"):
            path.write_text(raw, encoding="utf-8")
    overlay_text = world.build_overlay(additions).replace(
        "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv",
        "BUILD_START_1776_RUNTIME_INFRASTRUCTURE_OVERLAY.csv + BUILD_START_1776_RUNTIME_ADMINISTRATION_OVERLAY.csv",
    )
    catalog_tools.brace_maps(catalog_tools.clean_comments(overlay_text))
    RUNTIME_BUILDING_OVERLAY.write_text(overlay_text, encoding="utf-8")

    state_raw = STATE_HISTORY.read_text(encoding="utf-8-sig")
    for owner, state in sorted(DEINCORPORATIONS):
        state_raw = patch_state_history(state_raw, owner, state)
    catalog_tools.brace_maps(catalog_tools.clean_comments(state_raw))
    STATE_HISTORY.write_text(state_raw, encoding="utf-8")

    infra_fields = [
        "Owner_TAG", "Country", "State_ID", "State_Name", "Current_Level", "Road_PM", "Canal_PM",
        "Rail_PM", "Passenger_PM", "Infrastructure_Available", "Infrastructure_Used", "Current_Market_Access",
        "Additional_Level_Needed", "Historical_Connectivity_Exception", "Evidence", "Final_Target_Level",
        "Final_Infrastructure_Available", "Reason",
    ]
    write_csv(INFRA_AUDIT, infra_fields, infra_audit)
    write_csv(INFRA_OVERLAY, list(infra_overlay[0]) if infra_overlay else [
        "Owner_TAG", "Country", "State_ID", "State_Name", "Building_ID", "Historical_Level",
        "Runtime_Additional_Level", "Runtime_Final_Target_Level", "Road_PM", "Canal_PM", "Rail_PM",
        "Passenger_PM", "Capacity_Per_Level", "Reason",
    ], infra_overlay)
    write_csv(ACCESS_EXCEPTIONS, [
        "Owner_TAG", "Country", "State_ID", "State_Name", "Expected_Market_Access", "Historical_Reason",
        "Evidence", "Intended_Gameplay_Effect",
    ], [])
    write_csv(DEINCORP_REVIEW, list(deincorp_rows[0]), deincorp_rows)
    write_csv(BUREAUCRACY_AUDIT, list(bureaucracy[0]), bureaucracy)
    write_csv(ADMIN_OVERLAY, list(admin_overlay[0]), admin_overlay)
    write_csv(MARKET_AUDIT, list(market_rows[0]), market_rows)
    write_csv(FALLBACK_IMPACT, list(fallback_rows[0]), fallback_rows)
    write_csv(SHORTAGE_EXCEPTIONS, [
        "Market", "Good", "Shortage_Level", "Historical_Reason", "Evidence", "Intended_Gameplay_Effect", "Keep_or_Fix",
    ], [])
    write_csv(SUPPLY_OVERLAY, [
        "Market", "Owner_TAG", "State_ID", "Building_ID", "Historical_Level", "Runtime_Additional_Level",
        "Runtime_Final_Target_Level", "PM_Change", "Trade_or_Port_Change", "Evidence", "Reason",
    ], [])

    runtime_changes = {key: target for key, target in building_targets.items() if target != levels.get(key, 0)}
    matrix_rows = runtime_matrix(base_matrix, runtime_changes, state_rows)
    write_csv(RUNTIME_MATRIX, list(matrix_rows[0]), matrix_rows)

    admin_before = sum(level for key, level in levels.items() if key[2] == ADMIN)
    admin_after = admin_before + sum(ADMIN_ADDITIONS.values())
    REPORT.write_text(report_text(
        infra_audit, infra_overlay, bureaucracy, len(fallback_rows), len(DEINCORPORATIONS), admin_before, admin_after,
    ), encoding="utf-8")

    _, after = world.all_placements(HISTORY)
    protected_after = world.semantic(after, lambda row: row.owner in world.SERENISSIMA or row.building in world.PROTECTED)
    if protected_before != protected_after:
        raise RuntimeError("Protected/Serenissima semantics changed")
    return {
        "states_audited": len(infra_audit),
        "states_below_before": sum(float(row["Infrastructure_Used"]) > float(row["Infrastructure_Available"]) for row in infra_audit),
        "infrastructure_rows_changed": len(infra_overlay),
        "infrastructure_levels_added": sum(int(row["Runtime_Additional_Level"]) for row in infra_overlay),
        "deincorporations": len(DEINCORPORATIONS),
        "admin_levels_before": admin_before,
        "admin_levels_after": admin_after,
        "fallbacks_audited": len(fallback_rows),
        "market_rows": len(market_rows),
        "protected_changes": 0,
    }


def refresh() -> dict[str, object]:
    """Recalculate Wave 1 from the frozen V2 baseline after policy edits.

    This mode is intentionally idempotent.  It never treats the already
    applied runtime increases as a new historical baseline, and therefore
    cannot double the administration or infrastructure overlay.
    """
    state_rows = read_csv(STATE_CATALOG)
    base_matrix = read_csv(BASE_MATRIX)
    base_levels = {
        (row["Owner_TAG"], row["State_ID"], row["Building_ID"]): int(float(row.get("Target_Level") or 0))
        for row in base_matrix
    }
    actual_levels, pms, placements = actual_semantics()
    protected_before = world.semantic(
        placements,
        lambda row: row.owner in world.SERENISSIMA or row.building in world.PROTECTED,
    )

    # Administration values have already been written by the first pass.
    # Validate them rather than applying the deltas a second time.
    for key, delta in ADMIN_ADDITIONS.items():
        expected = base_levels.get(key, 0) + delta
        if actual_levels.get(key, 0) != expected:
            raise RuntimeError(
                f"Runtime administration mismatch for {key}: "
                f"actual={actual_levels.get(key, 0)} expected={expected}"
            )

    # Infrastructure demand must include the final administration overlay.
    calibration_levels = dict(base_levels)
    for key, delta in ADMIN_ADDITIONS.items():
        calibration_levels[key] = base_levels.get(key, 0) + delta
    infra_audit, infra_overlay, infra_targets, plans = infrastructure_plan(
        state_rows, calibration_levels, pms
    )
    bureaucracy, admin_overlay = bureaucracy_reports(state_rows, base_levels, pms)
    deincorp_rows = deincorporation_review(state_rows)
    market_rows, fallback_rows = market_reports()

    transformed, additions = rescale_existing(placements, infra_targets, plans)
    if additions:
        raise RuntimeError(
            "Refresh unexpectedly requires new infrastructure placement(s); "
            "run a reviewed full apply instead of rewriting the existing overlay."
        )
    for path, raw in transformed.items():
        if raw != path.read_text(encoding="utf-8-sig"):
            path.write_text(raw, encoding="utf-8")

    state_raw = STATE_HISTORY.read_text(encoding="utf-8-sig")
    for owner, state in sorted(DEINCORPORATIONS):
        state_raw = patch_state_history(state_raw, owner, state)
    catalog_tools.brace_maps(catalog_tools.clean_comments(state_raw))
    STATE_HISTORY.write_text(state_raw, encoding="utf-8")

    infra_fields = [
        "Owner_TAG", "Country", "State_ID", "State_Name", "Current_Level", "Road_PM", "Canal_PM",
        "Rail_PM", "Passenger_PM", "Infrastructure_Available", "Infrastructure_Used", "Current_Market_Access",
        "Additional_Level_Needed", "Historical_Connectivity_Exception", "Evidence", "Final_Target_Level",
        "Final_Infrastructure_Available", "Reason",
    ]
    write_csv(INFRA_AUDIT, infra_fields, infra_audit)
    write_csv(INFRA_OVERLAY, list(infra_overlay[0]) if infra_overlay else [
        "Owner_TAG", "Country", "State_ID", "State_Name", "Building_ID", "Historical_Level",
        "Runtime_Additional_Level", "Runtime_Final_Target_Level", "Road_PM", "Canal_PM", "Rail_PM",
        "Passenger_PM", "Capacity_Per_Level", "Reason",
    ], infra_overlay)
    write_csv(ACCESS_EXCEPTIONS, [
        "Owner_TAG", "Country", "State_ID", "State_Name", "Expected_Market_Access", "Historical_Reason",
        "Evidence", "Intended_Gameplay_Effect",
    ], [])
    write_csv(DEINCORP_REVIEW, list(deincorp_rows[0]), deincorp_rows)
    write_csv(BUREAUCRACY_AUDIT, list(bureaucracy[0]), bureaucracy)
    write_csv(ADMIN_OVERLAY, list(admin_overlay[0]), admin_overlay)
    write_csv(MARKET_AUDIT, list(market_rows[0]), market_rows)
    write_csv(FALLBACK_IMPACT, list(fallback_rows[0]), fallback_rows)
    write_csv(SHORTAGE_EXCEPTIONS, [
        "Market", "Good", "Shortage_Level", "Historical_Reason", "Evidence", "Intended_Gameplay_Effect", "Keep_or_Fix",
    ], [])
    write_csv(SUPPLY_OVERLAY, [
        "Market", "Owner_TAG", "State_ID", "Building_ID", "Historical_Level", "Runtime_Additional_Level",
        "Runtime_Final_Target_Level", "PM_Change", "Trade_or_Port_Change", "Evidence", "Reason",
    ], [])

    runtime_changes = {
        key: target for key, target in infra_targets.items()
        if target != base_levels.get(key, 0)
    }
    for key, delta in ADMIN_ADDITIONS.items():
        runtime_changes[key] = base_levels.get(key, 0) + delta
    matrix_rows = runtime_matrix(base_matrix, runtime_changes, state_rows)
    write_csv(RUNTIME_MATRIX, list(matrix_rows[0]), matrix_rows)

    admin_before = sum(level for key, level in base_levels.items() if key[2] == ADMIN)
    admin_after = admin_before + sum(ADMIN_ADDITIONS.values())
    REPORT.write_text(report_text(
        infra_audit, infra_overlay, bureaucracy, len(fallback_rows), len(DEINCORPORATIONS), admin_before, admin_after,
    ), encoding="utf-8")

    _, after = world.all_placements(HISTORY)
    protected_after = world.semantic(
        after,
        lambda row: row.owner in world.SERENISSIMA or row.building in world.PROTECTED,
    )
    if protected_before != protected_after:
        raise RuntimeError("Protected/Serenissima semantics changed")
    return {
        "states_audited": len(infra_audit),
        "states_below_before": sum(
            float(row["Infrastructure_Used"]) > float(row["Infrastructure_Available"])
            for row in infra_audit
        ),
        "infrastructure_rows_changed": len(infra_overlay),
        "infrastructure_levels_added": sum(int(row["Runtime_Additional_Level"]) for row in infra_overlay),
        "deincorporations": len(DEINCORPORATIONS),
        "admin_levels_before": admin_before,
        "admin_levels_after": admin_after,
        "fallbacks_audited": len(fallback_rows),
        "market_rows": len(market_rows),
        "protected_changes": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    if args.apply == args.refresh:
        raise SystemExit("Use exactly one of --apply or --refresh")
    import json
    result = apply() if args.apply else refresh()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
