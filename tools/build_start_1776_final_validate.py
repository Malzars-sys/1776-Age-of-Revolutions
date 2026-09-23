#!/usr/bin/env python3
"""Final static validator for the BUILD START 1776 V2 implementation."""

from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

import build_start_1776_blocker_resolution as blocker
import build_start_1776_research_input_pack as catalog_tools
import build_start_1776_world_apply as world


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "docs" / "reports" / "buildings"
RUNTIME_MATRIX = REPORTS / "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_RUNTIME_V1.csv"
MATRIX = RUNTIME_MATRIX if RUNTIME_MATRIX.exists() else REPORTS / "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv"
TECH_CHANGES = REPORTS / "BUILD_START_1776_START_TECH_CHANGES_FINAL_V2.csv"
GATES = REPORTS / "BUILD_START_1776_GATE_RECONCILIATION_CORRIGE_V2.csv"
CATALOG = REPORTS / "BUILD_START_1776_BUILDING_CATALOG.csv"
STATE_CATALOG = REPORTS / "BUILD_START_1776_STATE_CATALOG.csv"
RUNTIME_INFRA = REPORTS / "BUILD_START_1776_RUNTIME_INFRASTRUCTURE_AUDIT.csv"
INFRA = RUNTIME_INFRA if RUNTIME_INFRA.exists() else REPORTS / "BUILD_START_1776_INFRASTRUCTURE_PM_PLAN.csv"
CURRENT_BASELINE = REPORTS / "BUILD_START_1776_CURRENT_BUILDINGS.csv"
VALIDATION = REPORTS / "BUILD_START_1776_FINAL_TARGET_VALIDATION.csv"
SUMMARY = REPORTS / "BUILD_START_1776_FINAL_VALIDATION_SUMMARY.json"

REVIEWS = {
	("CHI", "regulated_small_arms"),
	("MARATH", "standardized_field_artillery"),
	("MUG", "standardized_field_artillery"),
	("USA", "regulated_small_arms"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def integer(value: str | int) -> int:
    return int(float(value or 0))


def gates(block: catalog_tools.Block) -> set[str]:
    return set(catalog_tools.tokens_flat(
        catalog_tools.braced_tokens(block.text, "unlocking_technologies")
    ))


def semantic_baseline(rows: list[dict[str, str]], predicate) -> dict[tuple[str, str, str], tuple[int, tuple[str, ...]]]:
    return {
        (row["Owner_TAG"], row["State_ID"], row["Building_ID"]): (
            integer(row["Current_Level"]),
            tuple(sorted(pm for pm in row["Current_PM_Overrides"].split("|") if pm and pm != "NONE")),
        )
        for row in rows if predicate(row)
    }


def main() -> None:
    # The engine expects one configuration per state. A building-level tally
    # alone would miss duplicate s:STATE_* / region_state:* history blocks.
    state_sources: dict[str, list[str]] = defaultdict(list)
    region_sources: dict[tuple[str, str], list[str]] = defaultdict(list)
    for path in sorted(world.HISTORY.glob("*.txt")):
        for state in catalog_tools.named_blocks(path, r"s:STATE_[A-Za-z0-9_]+", 1):
            state_sources[state.object_id].append(f"{path.name}:{state.line}")
            for region in catalog_tools.subblocks(state, r"region_state:[A-Za-z0-9_]+"):
                region_sources[(state.object_id, region.object_id)].append(f"{path.name}:{region.line}")
    repeated_states = {key: value for key, value in state_sources.items() if len(value) > 1}
    repeated_regions = {key: value for key, value in region_sources.items() if len(value) > 1}

    matrix = read_csv(MATRIX)
    tech_changes = read_csv(TECH_CHANGES)
    gate_rows = read_csv(GATES)
    catalog = {row["Building_ID"]: row for row in read_csv(CATALOG)}
    state_pairs = {(row["Owner_TAG"], row["State_ID"]) for row in read_csv(STATE_CATALOG)}
    infra = {
        (row["Owner_TAG"], row["State_ID"]): row for row in read_csv(INFRA)
        if integer(row.get("Final_Target_Level", row.get("Target_Building_Level", "0"))) > 0
    }

    target = {
        (row["Owner_TAG"], row["State_ID"], row["Building_ID"]): integer(row["Target_Level"])
        for row in matrix
    }
    target_positive = {key: level for key, level in target.items() if level > 0}

    raw_actual = catalog_tools.parse_current_buildings()
    actual = {
        (str(row["owner"]), str(row["state"]), str(row["building"])): integer(row["level"])
        for row in raw_actual if (str(row["owner"]), str(row["state"])) in state_pairs
    }
    actual_pms = {
        (str(row["owner"]), str(row["state"]), str(row["building"])): tuple(sorted(str(pm) for pm in row["pms"]))
        for row in raw_actual if (str(row["owner"]), str(row["state"])) in state_pairs
    }
    orphan_rows = [
        row for row in raw_actual if (str(row["owner"]), str(row["state"])) not in state_pairs
    ]

    comparison: list[dict[str, object]] = []
    for key, expected in sorted(target_positive.items()):
        got = actual.get(key, 0)
        status = "MATCH" if got == expected else ("MISSING" if got == 0 else "MISMATCH")
        comparison.append({
            "Owner_TAG": key[0], "State_ID": key[1], "Building_ID": key[2],
            "Expected_Level": expected, "Actual_Level": got, "Status": status,
            "Extra_Classification": "",
        })
    for key, got in sorted(actual.items()):
        if got > 0 and key not in target_positive:
            comparison.append({
                "Owner_TAG": key[0], "State_ID": key[1], "Building_ID": key[2],
                "Expected_Level": 0, "Actual_Level": got, "Status": "EXTRA",
                "Extra_Classification": "UNEXPECTED_EFFECTIVE_MANUAL_PLACEMENT",
            })
    with VALIDATION.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(comparison[0]))
        writer.writeheader()
        writer.writerows(comparison)
    statuses = Counter(str(row["Status"]) for row in comparison)

    # Semantic preservation against the frozen pre-write catalog.
    baseline = read_csv(CURRENT_BASELINE)
    protected_before = semantic_baseline(baseline, lambda row: row["Building_ID"] in world.PROTECTED)
    serenissima_before = semantic_baseline(baseline, lambda row: row["Owner_TAG"] in world.SERENISSIMA)
    protected_after = {
        key: (level, actual_pms.get(key, ())) for key, level in actual.items() if key[2] in world.PROTECTED
    }
    serenissima_after = {
        key: (level, actual_pms.get(key, ())) for key, level in actual.items() if key[0] in world.SERENISSIMA
    }
    protected_changes = sum(protected_before.get(key) != protected_after.get(key) for key in set(protected_before) | set(protected_after))
    serenissima_changes = sum(serenissima_before.get(key) != serenissima_after.get(key) for key in set(serenissima_before) | set(serenissima_after))

    # Technology graph and direct-grant integrity.
    technology = catalog_tools.effective_objects(
        "common/technology/technologies", r"[A-Za-z0-9_]+", mod_only=True
    )
    parents = {tech: gates(block) for tech, block in technology.items()}
    starts = blocker.starting_techs()
    unknown_tech = sorted(
        (tag, tech) for tag, values in starts.items() for tech in values if tech not in technology
    )
    direct_debt = sorted({
        (tag, tech, parent)
        for tag, values in starts.items()
        for tech in values if tech in parents
        for parent in parents[tech] if parent not in values
    })

    def ancestors(tech: str, seen: set[str] | None = None) -> set[str]:
        seen = set() if seen is None else seen
        for parent in parents.get(tech, set()):
            if parent not in seen:
                seen.add(parent)
                ancestors(parent, seen)
        return seen

    transitive_debt = sorted({
        (tag, tech, parent)
        for tag, values in starts.items()
        for tech in values if tech in parents
        for parent in ancestors(tech) if parent not in values
    })
    duplicate_grants: list[tuple[str, str]] = []
    direct_by_tag: dict[str, list[str]] = defaultdict(list)
    for tag, text in blocker.country_blocks():
        direct_by_tag[tag].extend(blocker.direct_assignments(text, "add_technology_researched"))
    for tag, values in direct_by_tag.items():
        duplicate_grants.extend((tag, tech) for tech, count in Counter(values).items() if count > 1)

    expected_add = {
        (row["TAG"], row["Technology"])
        for row in tech_changes if row["Final_Decision"] == "ADD"
    }
    missing_approved_adds = sorted(
        pair for pair in expected_add if pair[1] not in starts.get(pair[0], set())
    )
    review_applied = sorted(pair for pair in REVIEWS if pair[1] in starts.get(pair[0], set()))

    # Effective building/PM gate validation, excluding immutable protections
    # and the three explicitly deferred military pairs.
    buildings = catalog_tools.effective_objects("common/buildings", r"building_[A-Za-z0-9_]+")
    pms = catalog_tools.effective_objects("common/production_methods", r"[A-Za-z0-9_]+")
    _, parsed = world.all_placements(world.HISTORY)
    effective = [row for row in parsed if (row.owner, row.state) in state_pairs]
    building_gate_debt = set()
    pm_gate_debt = set()
    unknown_pm = set()
    for placement in effective:
        if placement.owner in world.SERENISSIMA or placement.building in world.PROTECTED:
            continue
        for technology_id in gates(buildings[placement.building]):
            if technology_id not in starts.get(placement.owner, set()) and (placement.owner, technology_id) not in REVIEWS:
                building_gate_debt.add((placement.owner, placement.state, placement.building, technology_id))
        for pm in placement.pms:
            if pm not in pms:
                unknown_pm.add((placement.owner, placement.state, placement.building, pm))
                continue
            for technology_id in gates(pms[pm]):
                if technology_id not in starts.get(placement.owner, set()) and (placement.owner, technology_id) not in REVIEWS:
                    pm_gate_debt.add((placement.owner, placement.state, placement.building, pm, technology_id))

    # Gate architecture decisions themselves.
    gate_architecture_errors = []
    for row in gate_rows:
        building_gates = gates(buildings[row["Building_ID"]])
        if row["Decision"] == "REMOVE_BUILDING_GATE" and row["Required_Technology"] in building_gates:
            gate_architecture_errors.append((row["Building_ID"], "NOT_REMOVED"))
        elif row["Decision"] == "CHANGE_BUILDING_GATE" and row["Replacement_Gate"] not in building_gates:
            gate_architecture_errors.append((row["Building_ID"], "REPLACEMENT_MISSING"))
        elif row["Decision"] == "KEEP_CURRENT_GATE" and row["Required_Technology"] not in building_gates:
            gate_architecture_errors.append((row["Building_ID"], "CURRENT_GATE_MISSING"))

    # Infrastructure plan exactness.
    infra_bad = []
    for key, row in infra.items():
        placement_key = (key[0], key[1], "building_railway")
        expected = {
            row["Road_PM"], row["Canal_PM"], row["Rail_PM"], row["Passenger_PM"]
        }
        expected_level = integer(row.get("Final_Target_Level", row.get("Target_Building_Level", "0")))
        if set(actual_pms.get(placement_key, ())) != expected or actual.get(placement_key, 0) != expected_level:
            infra_bad.append(placement_key)

    auto_violations = [
        key for key in target_positive
        if catalog.get(key[2], {}).get("Auto_Generated") == "YES"
    ]
    post_1776_violations = [
        key for key in target_positive
        if catalog.get(key[2], {}).get("Relevant_For_1776_Start_Research") == "NO_POST_1776"
    ]
    steel_targets = [key for key in target_positive if key[2] == "building_steel_mill"]
    steel_without_coke = [key for key in steel_targets if "coke_smelting" not in starts.get(key[0], set())]
    coke_from_steel = [
        row for row in tech_changes
        if row["Technology"] == "coke_smelting"
        and row["Final_Decision"] == "ADD"
        and row["Required_By_Buildings"] == "building_steel_mill"
    ]

    decisions = Counter(row["Decision"] for row in matrix)
    active_canals = sum(row["Canal_PM"] != "pm_no_canal_network" for row in infra.values())
    active_rail = sum(row["Rail_PM"] != "pm_no_rail_network" for row in infra.values())
    active_passenger = sum(row["Passenger_PM"] != "pm_no_passenger_trains" for row in infra.values())
    non_serenissima_trade = [
        (key, level) for key, level in target_positive.items()
        if key[2] == "building_trade_center" and key[0] not in world.SERENISSIMA
    ]

    summary = {
        "history_state_definitions": len(state_sources),
        "duplicate_history_state_definitions": len(repeated_states),
        "duplicate_history_region_owner_definitions": len(repeated_regions),
        "matrix_rows": len(matrix),
        "target_positive_rows": len(target_positive),
        "target_manual_levels": sum(target_positive.values()),
        "decision_counts": dict(sorted(decisions.items())),
        "build_target_match": statuses["MATCH"],
        "build_target_mismatch": statuses["MISMATCH"],
        "build_target_missing": statuses["MISSING"],
        "build_target_extra": statuses["EXTRA"],
        "orphan_history_rows": len(orphan_rows),
        "orphan_history_levels": sum(integer(row["level"]) for row in orphan_rows),
        "admin_levels": sum(level for key, level in target_positive.items() if key[2] == "building_government_administration"),
        "logging_levels": sum(level for key, level in target_positive.items() if key[2] == "building_logging_camp"),
        "protected_placements": len(protected_after),
        "protected_levels": sum(value[0] for value in protected_after.values()),
        "protected_changes": protected_changes,
        "serenissima_changes": serenissima_changes,
        "final_start_tech_add": len(expected_add),
        "final_start_tech_review": sum(row["Final_Decision"] == "REVIEW" for row in tech_changes),
        "missing_approved_adds": len(missing_approved_adds),
        "review_applied": len(review_applied),
        "unknown_tech": len(unknown_tech),
        "duplicate_tech_grants": len(duplicate_grants),
        "direct_prerequisite_debt": len(direct_debt),
        "transitive_prerequisite_debt": len(transitive_debt),
        "gate_groups": len(gate_rows),
        "gate_conflicts_after_v2": sum(integer(row["Conflict_Count"]) for row in gate_rows),
        "building_gates_removed": sum(row["Decision"] == "REMOVE_BUILDING_GATE" for row in gate_rows),
        "building_gates_changed": sum(row["Decision"] == "CHANGE_BUILDING_GATE" for row in gate_rows),
        "gate_architecture_errors": len(gate_architecture_errors),
        "unresolved_building_gates": len(building_gate_debt),
        "unresolved_active_pm_gates": len(pm_gate_debt),
        "unknown_active_pm": len(unknown_pm),
        "infrastructure_rows": len(infra),
        "infrastructure_mismatches": len(infra_bad),
        "active_canal_pm_rows": active_canals,
        "active_rail_pm": active_rail,
        "active_passenger_pm": active_passenger,
        "trade_center_non_serenissima_rows": len(non_serenissima_trade),
        "trade_center_non_serenissima_levels": sum(level for _, level in non_serenissima_trade),
        "auto_generated_violations": len(auto_violations),
        "post_1776_violations": len(post_1776_violations),
        "countries_with_coke_smelting": sorted(tag for tag, values in starts.items() if "coke_smelting" in values),
        "countries_with_target_steel_mills": sorted({key[0] for key in steel_targets}),
        "steel_mill_without_coke_smelting": len(steel_without_coke),
        "coke_smelting_grants_caused_by_steel": len(coke_from_steel),
        "new_steel_pm_created": int("pm_charcoal_ironworks" in pms),
        "new_steel_tech_created": int("charcoal_ironworks" in technology),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    failures = {
        key: value for key, value in summary.items()
        if key in {
            "duplicate_history_state_definitions", "duplicate_history_region_owner_definitions",
            "build_target_mismatch", "build_target_missing", "build_target_extra",
            "protected_changes", "serenissima_changes", "missing_approved_adds",
            "review_applied", "unknown_tech", "duplicate_tech_grants",
            "direct_prerequisite_debt", "transitive_prerequisite_debt",
            "gate_architecture_errors", "unresolved_building_gates",
            "unresolved_active_pm_gates", "unknown_active_pm",
            "infrastructure_mismatches", "active_rail_pm", "active_passenger_pm",
            "auto_generated_violations", "post_1776_violations",
            "steel_mill_without_coke_smelting", "coke_smelting_grants_caused_by_steel",
            "new_steel_pm_created", "new_steel_tech_created",
        } and value != 0
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    if failures:
        raise SystemExit("VALIDATION FAILED: " + json.dumps(failures, ensure_ascii=False))


if __name__ == "__main__":
    main()
