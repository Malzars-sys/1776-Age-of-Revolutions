#!/usr/bin/env python3
"""Apply the final 1776 steel-good abstraction to report artifacts.

This is a report-only transformation.  It deliberately does not alter any
building, production-method, technology, or history definition.
"""

from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

import build_start_1776_blocker_resolution as blocker


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "docs" / "reports" / "buildings"

MATRIX_V1 = "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE.csv"
MATRIX_V2 = "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv"
GATES_V1 = "BUILD_START_1776_GATE_RECONCILIATION_CORRIGE.csv"
GATES_V2 = "BUILD_START_1776_GATE_RECONCILIATION_CORRIGE_V2.csv"
TECH_V1 = "BUILD_START_1776_START_TECH_CHANGES_FINAL.csv"
TECH_V2 = "BUILD_START_1776_START_TECH_CHANGES_FINAL_V2.csv"
STEEL_REVIEW = "BUILD_START_1776_STEEL_TARGET_REVIEW.csv"


def read(name: str) -> list[dict[str, str]]:
    with (REPORTS / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (REPORTS / name).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def integer(value: str | int) -> int:
    return int(float(value or 0))


def recalc_decision(current: int, target: int, serenissima: bool) -> str:
    if serenissima:
        return "PRESERVE_SERENISSIMA"
    if current == target:
        return "KEEP"
    if current == 0:
        return "ADD"
    if target == 0:
        return "REMOVE"
    return "INCREASE" if target > current else "DECREASE"


def main() -> None:
    start_techs = blocker.starting_techs()

    matrix = read(MATRIX_V1)
    matrix_fields = list(matrix[0])
    review: list[dict[str, object]] = []
    historical_positive = 0
    final_positive = 0
    removed_by_abstraction = 0

    for row in matrix:
        if row["Building_ID"] != "building_steel_mill":
            continue
        tag = row["Owner_TAG"]
        current = integer(row["Current_Level"])
        historical = integer(row["Base_Historical_Target_Level"])
        has_coke = "coke_smelting" in start_techs.get(tag, set())
        final = historical if has_coke else 0
        old_target = integer(row["Target_Level"])

        if historical > 0:
            historical_positive += 1
        if final > 0:
            final_positive += 1
        if old_target > 0 and final == 0:
            removed_by_abstraction += 1

        row["Base_Historical_Target_Level"] = str(historical)
        row["Target_Level"] = str(final)
        row["Delta"] = str(final - current)
        row["Decision"] = recalc_decision(
            current, final, row.get("Serenissima_Protected") == "YES"
        )
        row["Overlay_Type"] = "STEEL_GAMEPLAY_ABSTRACTION"
        row["Overlay_Reason"] = (
            "PRE_COKE_METALLURGY_ABSTRACTED_OUTSIDE_STEEL_GOOD"
        )
        review.append({
            "Owner_TAG": tag,
            "Country": row["Country"],
            "State_ID": row["State_ID"],
            "Current_Steel_Mill_Level": current,
            "Historical_Target_Level": historical,
            "Country_Has_Coke_Smelting": "YES" if has_coke else "NO",
            "Final_Target_Level": final,
            "Decision": row["Decision"],
            "Overlay_Type": "STEEL_GAMEPLAY_ABSTRACTION",
            "Reason": "PRE_COKE_METALLURGY_ABSTRACTED_OUTSIDE_STEEL_GOOD",
        })

    write(MATRIX_V2, matrix_fields, matrix)
    write(STEEL_REVIEW, [
        "Owner_TAG", "Country", "State_ID", "Current_Steel_Mill_Level",
        "Historical_Target_Level", "Country_Has_Coke_Smelting",
        "Final_Target_Level", "Decision", "Overlay_Type", "Reason",
    ], review)

    gates = read(GATES_V1)
    gate_fields = list(gates[0])
    steel_gate_rows = 0
    small_arms_gate_rows = 0
    for row in gates:
        if row["Required_Technology"] == "coke_smelting" and row["Building_ID"] == "building_steel_mill":
            steel_gate_rows += 1
            row.update({
                "PM_ID": "pm_coke_blast_furnaces",
                "Conflict_Count": "0",
                "Affected_TAG_Count": "0",
                "Affected_State_Count": "0",
                "Current_Gate": "BUILDING:coke_smelting",
                "Decision": "KEEP_CURRENT_GATE",
                "Replacement_Gate": "coke_smelting",
                "Starting_Tech_Changes_Required": "NO",
                "Building_Definition_Change": "NO",
                "PM_Definition_Change": "NO",
                "Reason": "STEEL_GOOD_BEGINS_WITH_COKE_IN_GAMEPLAY_ABSTRACTION",
                "Risk": "LOW",
            })
        if row["Required_Technology"] == "regulated_small_arms" and row["Building_ID"] == "building_arms_industry":
            small_arms_gate_rows += 1
            row.update({
                "Conflict_Count": "2",
                "Affected_TAG_Count": "2",
                "Affected_State_Count": "2",
                "Current_Gate": "BUILDING:regulated_small_arms",
                "Decision": "KEEP_CURRENT_GATE",
                "Replacement_Gate": "regulated_small_arms",
                "Starting_Tech_Changes_Required": "REVIEW — 2 TAGS: CHI|USA",
                "Building_Definition_Change": "NO",
                "PM_Definition_Change": "NO",
                "Reason": "The arms-industry target alone is insufficient to grant a military starting technology; CHI and USA remain explicit historical reviews.",
                "Risk": "MEDIUM",
            })
    if steel_gate_rows != 1:
        raise SystemExit(f"Expected one steel gate row, found {steel_gate_rows}")
    if small_arms_gate_rows != 1:
        raise SystemExit(f"Expected one small-arms gate row, found {small_arms_gate_rows}")
    late_farm_gates = {
        "building_rye_farm": (2, 2, 1),
        "building_silk_plantation": (1, 1, 1),
    }
    existing_gate_pairs = {
        (row["Required_Technology"], row["Building_ID"]) for row in gates
    }
    for building, (conflicts, tags, states) in late_farm_gates.items():
        pair = ("improved_husbandry", building)
        if pair in existing_gate_pairs:
            continue
        gates.append({
            "Required_Technology": "improved_husbandry",
            "Building_ID": building,
            "PM_ID": "",
            "Conflict_Count": str(conflicts),
            "Affected_TAG_Count": str(tags),
            "Affected_State_Count": str(states),
            "Current_Gate": "BUILDING:improved_husbandry",
            "Decision": "REMOVE_BUILDING_GATE",
            "Replacement_Gate": "NONE",
            "Starting_Tech_Changes_Required": "NO",
            "Building_Definition_Change": "YES",
            "PM_Definition_Change": "NO",
            "Reason": "[B — BUILDING_GATE_TOO_ADVANCED] The building's default PM is basic cultivation. Improved techniques remain represented by later PM gates.",
            "Risk": "LOW",
        })
    gates.sort(key=lambda row: (
        row["Required_Technology"], row["Building_ID"], row.get("PM_ID", "")
    ))
    write(GATES_V2, gate_fields, gates)

    tech = read(TECH_V1)
    tech_fields = list(tech[0])
    for row in tech:
        if row["Technology"] != "coke_smelting":
            continue
        steel_only = (
            row.get("Required_By_Buildings", "") == "building_steel_mill"
            and not row.get("Required_By_PMs", "")
        )
        if steel_only and row["Final_Decision"] == "ADD":
            row["Final_Decision"] = "NO_CHANGE_STEEL_ABSTRACTION"
            row["Reason"] = "PRE_COKE_METALLURGY_ABSTRACTED_OUTSIDE_STEEL_GOOD"
    # Effective-tree reconciliation discovered six valid omissions in the old
    # conflict snapshot. Four are required by positive V2 target rows and two
    # close shaft_mining beneath an already-granted applied_mineralogy.
    # The authoritative infrastructure plan also requires industrial canals
    # in four additional countries, plus turnpike_road_networks prerequisite
    # closure for the three that did not already possess it.
    effective_additions = {
        ("AUS", "industrial_canals"): ("building_railway", "pm_industrial_canals"),
        ("DEI", "industrial_canals"): ("building_railway", "pm_industrial_canals"),
        ("DEI", "turnpike_road_networks"): ("PREREQUISITE:industrial_canals", ""),
        ("KRA", "shaft_mining"): ("PREREQUISITE:applied_mineralogy", ""),
        ("MOR", "shaft_mining"): ("PREREQUISITE:applied_mineralogy", ""),
        ("MSN", "organized_textile_production"): ("building_textile_mill", ""),
        ("MSN", "shaft_mining"): ("building_salt_mine", ""),
        ("NEP", "organized_textile_production"): ("building_textile_mill", ""),
        ("SC2", "shaft_mining"): ("building_gold_mine", ""),
        ("SIA", "industrial_canals"): ("building_railway", "pm_industrial_canals"),
        ("SIA", "turnpike_road_networks"): ("PREREQUISITE:industrial_canals", ""),
        ("TUR", "industrial_canals"): ("building_railway", "pm_industrial_canals"),
        ("TUR", "turnpike_road_networks"): ("PREREQUISITE:industrial_canals", ""),
    }
    existing_pairs = {(row["TAG"], row["Technology"]) for row in tech}
    for (tag, technology), (buildings, pms) in sorted(effective_additions.items()):
        if (tag, technology) in existing_pairs:
            continue
        tech.append({
            "TAG": tag,
            "Technology": technology,
            "Required_By_Buildings": buildings,
            "Required_By_PMs": pms,
            "Historical_Tech_Status": "MISSING_FROM_START",
            "Prerequisite_Closure": "COMPLETE",
            "Final_Decision": "ADD",
            "Reason": "Recalculated from the effective V2 target and current technology graph; omitted by the stale pre-V2 conflict snapshot.",
        })
    usa_pair = ("USA", "regulated_small_arms")
    usa_reason = (
        "Existing authoritative 1776 synthesis keeps this capability under "
        "REVIEW_ABSENT because evidence is sectoral/frontier and insufficient "
        "for the national node threshold; building_arms_industry alone is not "
        "a grant justification. Source: docs/reports/technology/"
        "TECH_START_1776_SECOND_PASS_WORLD_MATRIX.csv (USA regulated_small_arms)."
    )
    usa_row = next(
        (row for row in tech if (row["TAG"], row["Technology"]) == usa_pair),
        None,
    )
    if usa_row is None:
        tech.append({
            "TAG": "USA",
            "Technology": "regulated_small_arms",
            "Required_By_Buildings": "building_arms_industry",
            "Required_By_PMs": "",
            "Historical_Tech_Status": "MISSING_FROM_START",
            "Prerequisite_Closure": "DEFERRED_WITH_REVIEW",
            "Final_Decision": "REVIEW",
            "Reason": usa_reason,
        })
    else:
        usa_row.update({
            "Prerequisite_Closure": "DEFERRED_WITH_REVIEW",
            "Final_Decision": "REVIEW",
            "Reason": usa_reason,
        })
    tech.sort(key=lambda row: (row["TAG"], row["Technology"]))
    write(TECH_V2, tech_fields, tech)

    target_steel = [row for row in review if integer(row["Final_Target_Level"]) > 0]
    steel_without_coke = [
        row for row in target_steel if row["Country_Has_Coke_Smelting"] != "YES"
    ]
    decisions = Counter(row["Decision"] for row in matrix)
    tech_decisions = Counter(row["Final_Decision"] for row in tech)
    result = {
        "matrix_rows": len(matrix),
        "target_positive_rows": sum(integer(row["Target_Level"]) > 0 for row in matrix),
        "target_manual_levels": sum(integer(row["Target_Level"]) for row in matrix),
        "decisions": dict(sorted(decisions.items())),
        "admin_levels": sum(integer(row["Target_Level"]) for row in matrix if row["Building_ID"] == "building_government_administration"),
        "logging_levels": sum(integer(row["Target_Level"]) for row in matrix if row["Building_ID"] == "building_logging_camp"),
        "steel_historical_target_rows_before": historical_positive,
        "steel_target_rows_after": final_positive,
        "steel_rows_removed_by_abstraction": removed_by_abstraction,
        "countries_with_coke_smelting": sorted(tag for tag, techs in start_techs.items() if "coke_smelting" in techs),
        "countries_with_target_steel_mills": sorted({row["Owner_TAG"] for row in target_steel}),
        "steel_mill_without_coke_smelting": len(steel_without_coke),
        "gate_conflicts_after_v2": sum(integer(row["Conflict_Count"]) for row in gates),
        "tech_decisions": dict(sorted(tech_decisions.items())),
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
