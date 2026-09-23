#!/usr/bin/env python3
"""Downgrade only technically invalid surviving PM overrides to group bases."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

import build_start_1776_blocker_resolution as blocker
import build_start_1776_research_input_pack as catalog_tools
import build_start_1776_world_apply as world


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "reports" / "buildings" / "BUILD_START_1776_PM_GATE_FALLBACKS.csv"
STATE_CATALOG = ROOT / "docs" / "reports" / "buildings" / "BUILD_START_1776_STATE_CATALOG.csv"
MATRIX = ROOT / "docs" / "reports" / "buildings" / "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv"
REVIEWS = {
    ("CHI", "regulated_small_arms"),
    ("MARATH", "standardized_field_artillery"),
    ("MUG", "standardized_field_artillery"),
    ("USA", "regulated_small_arms"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def tech_gates(block: catalog_tools.Block) -> set[str]:
    return set(catalog_tools.tokens_flat(
        catalog_tools.braced_tokens(block.text, "unlocking_technologies")
    ))


def main() -> None:
    starts = blocker.starting_techs()
    pms = catalog_tools.effective_objects(
        "common/production_methods", r"[A-Za-z0-9_]+"
    )
    groups = catalog_tools.effective_objects(
        "common/production_method_groups", r"[A-Za-z0-9_]+"
    )
    pm_to_group: dict[str, str] = {}
    base_by_group: dict[str, str] = {}
    for group_id, group in groups.items():
        methods = catalog_tools.tokens_flat(
            catalog_tools.braced_tokens(group.text, "production_methods")
        )
        if not methods:
            continue
        base_by_group[group_id] = methods[0]
        for pm in methods:
            pm_to_group[pm] = group_id

    valid_owner_states = {
        (row["Owner_TAG"], row["State_ID"]) for row in read_csv(STATE_CATALOG)
    }
    raws, placements = world.all_placements(world.HISTORY)
    before_levels: dict[tuple[str, str, str], int] = defaultdict(int)
    for placement in placements:
        before_levels[placement.key] += placement.level

    replacements: dict[Path, list[tuple[int, int, str]]] = defaultdict(list)
    report: list[dict[str, str]] = []
    for placement in placements:
        if (placement.owner, placement.state) not in valid_owner_states:
            continue
        if placement.owner in world.SERENISSIMA or placement.building in world.PROTECTED:
            continue
        revised = list(placement.pms)
        changed = False
        for index, pm in enumerate(placement.pms):
            if pm not in pms:
                raise SystemExit(f"Unknown active PM {pm} at {placement.key}")
            missing = sorted(
                tech for tech in tech_gates(pms[pm])
                if tech not in starts.get(placement.owner, set())
                and (placement.owner, tech) not in REVIEWS
            )
            if not missing:
                continue
            group = pm_to_group.get(pm)
            fallback = base_by_group.get(group or "")
            if not fallback or fallback not in pms:
                raise SystemExit(f"No base PM fallback for {pm} at {placement.key}")
            fallback_missing = sorted(
                tech for tech in tech_gates(pms[fallback])
                if tech not in starts.get(placement.owner, set())
            )
            if fallback_missing:
                raise SystemExit(
                    f"Base PM {fallback} still gated by {fallback_missing} at {placement.key}"
                )
            revised[index] = fallback
            changed = True
            report.append({
                "Owner_TAG": placement.owner,
                "State_ID": placement.state,
                "Building_ID": placement.building,
                "Production_Method_Group": group or "UNKNOWN",
                "Old_PM": pm,
                "Missing_Technologies": "|".join(missing),
                "Fallback_Base_PM": fallback,
                "Reason": "SURVIVING_OVERRIDE_NOT_TECHNICALLY_VALID_AT_1776_START",
            })
        if changed:
            replacements[placement.path].append((
                placement.start,
                placement.end,
                world.replace_active_pms(placement.text, revised),
            ))

    transformed = dict(raws)
    for path, changes in replacements.items():
        raw = transformed[path]
        for start, end, replacement in sorted(changes, reverse=True):
            raw = raw[:start] + replacement + raw[end:]
        catalog_tools.brace_maps(catalog_tools.clean_comments(raw))
        transformed[path] = raw
    for path, raw in transformed.items():
        if raw != raws[path]:
            path.write_text(raw, encoding="utf-8")

    _, after = world.all_placements(world.HISTORY)
    after_levels: dict[tuple[str, str, str], int] = defaultdict(int)
    after_pms: dict[tuple[str, str, str], set[str]] = defaultdict(set)
    for placement in after:
        after_levels[placement.key] += placement.level
        after_pms[placement.key].update(placement.pms)
    if dict(after_levels) != dict(before_levels):
        raise SystemExit("PM reconciliation changed building levels")

    # Preserve a reproducible audit after the rewrite has already happened.
    # The V2 matrix records the original PM signature in Notes, so subsequent
    # idempotent runs can still report the fallbacks rather than erasing them.
    reported = {
        (row["Owner_TAG"], row["State_ID"], row["Building_ID"], row["Old_PM"])
        for row in report
    }
    for row in read_csv(MATRIX):
        owner = row["Owner_TAG"]
        state = row["State_ID"]
        building = row["Building_ID"]
        if int(float(row["Target_Level"] or 0)) <= 0:
            continue
        if owner in world.SERENISSIMA or building in world.PROTECTED:
            continue
        notes = row.get("Notes", "")
        if "CURRENT_PM=" not in notes:
            continue
        old_pms = notes.split("CURRENT_PM=", 1)[1].strip().split("|")
        current = after_pms.get((owner, state, building), set())
        for pm in old_pms:
            if pm not in pms or pm in current:
                continue
            missing = sorted(
                tech for tech in tech_gates(pms[pm])
                if tech not in starts.get(owner, set())
                and (owner, tech) not in REVIEWS
            )
            if not missing:
                continue
            group = pm_to_group.get(pm)
            fallback = base_by_group.get(group or "")
            audit_key = (owner, state, building, pm)
            if not fallback or fallback not in current or audit_key in reported:
                continue
            report.append({
                "Owner_TAG": owner,
                "State_ID": state,
                "Building_ID": building,
                "Production_Method_Group": group or "UNKNOWN",
                "Old_PM": pm,
                "Missing_Technologies": "|".join(missing),
                "Fallback_Base_PM": fallback,
                "Reason": "SURVIVING_OVERRIDE_NOT_TECHNICALLY_VALID_AT_1776_START",
            })
            reported.add(audit_key)

    fields = [
        "Owner_TAG", "State_ID", "Building_ID", "Production_Method_Group",
        "Old_PM", "Missing_Technologies", "Fallback_Base_PM", "Reason",
    ]
    with REPORT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(sorted(report, key=lambda row: (
            row["Owner_TAG"], row["State_ID"], row["Building_ID"], row["Old_PM"]
        )))

    print(json.dumps({
        "placements_changed": len(replacements),
        "pm_fallbacks": len(report),
        "building_level_changes": 0,
    }, indent=2))


if __name__ == "__main__":
    main()
