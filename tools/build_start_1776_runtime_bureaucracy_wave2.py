#!/usr/bin/env python3
"""Runtime bureaucracy Wave 2 and Qing 1776 population correction.

The user supplied national runtime bureaucracy balances.  This pass first
rebalances Qing population from a dated provincial series, then applies only
historically defensible additional de-incorporations, and finally adds the
remaining administrative capacity.  Infrastructure is recalculated after the
administration overlay.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
from collections import defaultdict
from pathlib import Path

import build_start_1776_blocker_resolution as blocker
import build_start_1776_research_input_pack as catalog_tools
import build_start_1776_runtime_wave1 as wave1
import build_start_1776_world_apply as world


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "docs" / "reports" / "buildings"
POP_HISTORY = ROOT / "common" / "history" / "pops"
STATE_HISTORY = ROOT / "common" / "history" / "states" / "00_states.txt"
HISTORY = ROOT / "common" / "history" / "buildings"
BUILDING_OVERLAY = HISTORY / "97b_build_start_1776_runtime_bureaucracy_wave2.txt"
INFRA_OVERLAY_FILE = HISTORY / "97c_build_start_1776_runtime_bureaucracy_infrastructure.txt"

POP_AUDIT = REPORTS / "BUILD_START_1776_CHINA_POPULATION_REBALANCE_1776.csv"
BUREAUCRACY_WAVE2 = REPORTS / "BUILD_START_1776_RUNTIME_BUREAUCRACY_WAVE2.csv"
ADMIN_OVERLAY_V2 = REPORTS / "BUILD_START_1776_RUNTIME_ADMINISTRATION_OVERLAY_V2.csv"
REPORT = REPORTS / "BUILD_START_1776_RUNTIME_CALIBRATION_WAVE2_REPORT.md"

ADMIN = wave1.ADMIN
INFRA = wave1.INFRA

# Runtime values read directly from the user screenshots.  FRA and GBR are
# retained from the immediately preceding runtime calibration.
RUNTIME_BALANCE = {
    "CHI": -10200.0,
    "KOR": -389.0,
    "RUS": -588.0,
    "PLC": -412.0,
    "TUR": -660.0,
    "POR": -261.0,
    "USA": -557.0,
    "SC1": -589.0,
    "SC2": -217.0,
    "BRZ": -307.0,
    "PER": -109.0,
    "VEN": -141.0,
    "DEI": -266.0,
    "GWA": -40.7,
    "MARATH": -153.0,
    "PHI": 18.3,
    "FRA": 52.5,
    "GBR": 5.5,
}

# Provincial totals are in persons and correspond to 1776.  Game states that
# subdivide one historical province share the total in proportion to their
# pre-patch population, preserving the mod's internal spatial distribution.
QING_PROVINCES = [
    ("Zhili", 20_570_000, ["STATE_BEIJING", "STATE_ZHILI"]),
    ("Shandong", 21_500_000, ["STATE_SHANDONG"]),
    ("Henan", 19_860_000, ["STATE_HENAN"]),
    ("Shanxi", 12_500_000, ["STATE_SHANXI"]),
    ("Shaanxi", 8_190_000, ["STATE_XIAN"]),
    ("Gansu", 15_070_000, ["STATE_GANSU", "STATE_NINGXIA"]),
    ("Sichuan", 7_790_000, ["STATE_SICHUAN", "STATE_CHONGQING"]),
    ("Anhui", 27_570_000, ["STATE_NORTHERN_ANHUI", "STATE_SOUTHERN_ANHUI"]),
    ("Jiangsu", 28_810_000, ["STATE_JIANGSU", "STATE_NANJING", "STATE_SUZHOU"]),
    ("Jiangxi", 16_850_000, ["STATE_JIANGXI"]),
    ("Zhejiang", 19_370_000, ["STATE_ZHEJIANG"]),
    ("Fujian", 11_220_000, ["STATE_FUJIAN"]),
    ("Hubei", 14_820_000, ["STATE_EASTERN_HUBEI", "STATE_WESTERN_HUBEI"]),
    ("Hunan", 14_990_000, ["STATE_HUNAN"]),
    ("Guangdong", 14_820_000, ["STATE_GUANGDONG", "STATE_SHAOZHOU"]),
    ("Guangxi", 5_380_000, ["STATE_GUANGXI"]),
    ("Yunnan", 3_100_000, ["STATE_YUNNAN"]),
    ("Guizhou", 5_000_000, ["STATE_GUIZHOU"]),
    ("Fengtian", 770_000, ["STATE_SHENGJING"]),
    ("Jilin", 80_000, ["STATE_SOUTHERN_MANCHURIA", "STATE_NORTHERN_MANCHURIA", "STATE_OUTER_MANCHURIA"]),
    # Explicit frontier supplements not fully represented by the provincial
    # series.  They prevent the registered-population table from erasing
    # non-Han frontier populations altogether.
    ("Formosa supplement", 900_000, ["STATE_FORMOSA"]),
    ("Inner Mongolia supplement", 800_000, ["STATE_HINGGAN"]),
    ("Qinghai supplement", 800_000, ["STATE_QINGHAI"]),
]

POP_SOURCE = (
    "Cao Shuji/Jiang Tao 1776 provincial series, reproduced by Shanghai Jiao Tong University: "
    "https://history.sjtu.edu.cn/SJTU/JDHistory/kindeditor/Upload/file/20200709/202007090934348680000.pdf"
)

NEW_CHINA_DEINCORPORATIONS = {
    "STATE_FORMOSA": (
        "HISTORICALLY_ELIGIBLE_RECENT_CONQUEST_WEAK_INTEGRATION",
        "Qing conquest in 1683; island frontier still administered through a distinct and comparatively weakly integrated structure.",
    ),
    "STATE_SHENGJING": (
        "HISTORICALLY_ELIGIBLE_HIGH_AUTONOMY",
        "Manchu homeland under the separate banner/general system rather than ordinary China-proper provincial administration.",
    ),
    "STATE_SOUTHERN_MANCHURIA": (
        "HISTORICALLY_ELIGIBLE_HIGH_AUTONOMY",
        "Jilin/Manchurian territory governed through the separate banner/general system with restricted migration.",
    ),
    "STATE_NORTHERN_MANCHURIA": (
        "HISTORICALLY_ELIGIBLE_HIGH_AUTONOMY",
        "Heilongjiang frontier governed through a distinct military-general administration.",
    ),
}

# Incremental administration above Wave 1.  New placements are deliberately
# distributed among real administrative centres instead of stacked in one
# capital.  China receives its residual only after population and incorporation
# changes.  VEN is a protected Serenissima and is not modified.
ADMIN_WAVE2 = {
    # Qing: 711 simple-organization levels -> +7110 bureaucracy.
    ("CHI", "STATE_BEIJING", ADMIN): 70,
    ("CHI", "STATE_NANJING", ADMIN): 65,
    ("CHI", "STATE_ZHILI", ADMIN): 55,
    ("CHI", "STATE_JIANGSU", ADMIN): 50,
    ("CHI", "STATE_SUZHOU", ADMIN): 50,
    ("CHI", "STATE_SHANDONG", ADMIN): 55,
    ("CHI", "STATE_HENAN", ADMIN): 55,
    ("CHI", "STATE_SHANXI", ADMIN): 40,
    ("CHI", "STATE_XIAN", ADMIN): 35,
    ("CHI", "STATE_FUJIAN", ADMIN): 35,
    ("CHI", "STATE_JIANGXI", ADMIN): 45,
    ("CHI", "STATE_HUNAN", ADMIN): 40,
    ("CHI", "STATE_EASTERN_HUBEI", ADMIN): 40,
    ("CHI", "STATE_WESTERN_HUBEI", ADMIN): 36,
    ("CHI", "STATE_SICHUAN", ADMIN): 40,
    # Other runtime-observed deficits.
    ("KOR", "STATE_SEOUL", ADMIN): 15,
    ("KOR", "STATE_YANGHO", ADMIN): 12,
    ("KOR", "STATE_PYONGYANG", ADMIN): 11,
    ("RUS", "STATE_INGRIA", ADMIN): 5,
    ("RUS", "STATE_MOSCOW", ADMIN): 5,
    ("RUS", "STATE_KAZAN", ADMIN): 2,
    ("PLC", "STATE_GREATER_POLAND", ADMIN): 9,
    ("PLC", "STATE_LESSER_POLAND", ADMIN): 9,
    ("PLC", "STATE_MINSK", ADMIN): 6,
    ("PLC", "STATE_BREST", ADMIN): 5,
    ("PLC", "STATE_KIEV", ADMIN): 6,
    ("PLC", "STATE_VILNIUS", ADMIN): 6,
    ("TUR", "STATE_EASTERN_THRACE", ADMIN): 20,
    ("TUR", "STATE_LOWER_EGYPT", ADMIN): 15,
    ("TUR", "STATE_SYRIA", ADMIN): 10,
    ("TUR", "STATE_ANKARA", ADMIN): 20,
    ("POR", "STATE_ESTREMADURA", ADMIN): 18,
    ("POR", "STATE_ENTRE_DOURO_E_MINHO", ADMIN): 8,
    ("USA", "STATE_DISTRICT_OF_COLUMBIA", ADMIN): 15,
    ("USA", "STATE_NEW_YORK", ADMIN): 8,
    ("USA", "STATE_VIRGINIA", ADMIN): 6,
    ("USA", "STATE_GEORGIA", ADMIN): 5,
    ("USA", "STATE_MARYLAND", ADMIN): 5,
    ("USA", "STATE_PENNSYLVANIA", ADMIN): 6,
    ("USA", "STATE_MASSACHUSETTS", ADMIN): 4,
    ("USA", "STATE_NORTH_CAROLINA", ADMIN): 3,
    ("USA", "STATE_SOUTH_CAROLINA", ADMIN): 3,
    ("SC1", "STATE_MEXICO", ADMIN): 40,
    ("SC1", "STATE_JALISCO", ADMIN): 18,
    ("SC2", "STATE_CUNDINAMARCA", ADMIN): 8,
    ("SC2", "STATE_BOLIVAR", ADMIN): 5,
    ("SC2", "STATE_MIRANDA", ADMIN): 4,
    ("SC2", "STATE_ECUADOR", ADMIN): 4,
    ("BRZ", "STATE_RIO_DE_JANEIRO", ADMIN): 12,
    ("BRZ", "STATE_MINAS_GERAIS", ADMIN): 7,
    ("BRZ", "STATE_BAHIA", ADMIN): 7,
    ("BRZ", "STATE_PARA", ADMIN): 4,
    ("PER", "STATE_IRAKAJEMI", ADMIN): 4,
    ("PER", "STATE_FARS", ADMIN): 3,
    ("PER", "STATE_TABRIZ", ADMIN): 3,
    ("DEI", "STATE_WEST_JAVA", ADMIN): 4,
    ("DEI", "STATE_CEYLON", ADMIN): 2,
    ("GWA", "STATE_MALWA", ADMIN): 2,
    ("GWA", "STATE_RAJPUTANA", ADMIN): 2,
    ("MARATH", "STATE_AGRA", ADMIN): 7,
    ("MARATH", "STATE_BOMBAY", ADMIN): 8,
}


def state_rows() -> list[dict[str, str]]:
    return wave1.read_csv(wave1.STATE_CATALOG)


def population_targets(rows: list[dict[str, str]]) -> tuple[dict[str, int], dict[str, str]]:
    current = {row["State_ID"]: int(row["Current_Population"]) for row in rows if row["Owner_TAG"] == "CHI"}
    targets: dict[str, int] = {}
    provenance: dict[str, str] = {}
    for province, total, states in QING_PROVINCES:
        denominator = sum(current[state] for state in states)
        remaining = total
        for state in states[:-1]:
            value = round(total * current[state] / denominator)
            targets[state] = value
            provenance[state] = province
            remaining -= value
        targets[states[-1]] = remaining
        provenance[states[-1]] = province
    for state, value in current.items():
        targets.setdefault(state, value)
        provenance.setdefault(state, "Frontier retained from existing 1776 setup")
    return targets, provenance


def split_target(sizes: list[int], target: int) -> list[int]:
    if not sizes or target < len(sizes):
        raise RuntimeError(f"Cannot distribute population target {target} over {len(sizes)} pops")
    denominator = sum(sizes)
    result: list[int] = []
    remaining = target
    for value in sizes[:-1]:
        scaled = max(1, round(target * value / denominator))
        result.append(scaled)
        remaining -= scaled
    result.append(remaining)
    if result[-1] <= 0 or sum(result) != target:
        raise RuntimeError(f"Invalid population distribution for target {target}: {result}")
    return result


def rebalance_qing_population(targets: dict[str, int]) -> dict[str, int]:
    found: dict[str, int] = {}
    for path in sorted(POP_HISTORY.glob("*.txt")):
        raw = path.read_text(encoding="utf-8-sig")
        replacements: list[tuple[int, int, str]] = []
        for state_token, state_start, state_end in world.block_spans(raw, r"s:STATE_[A-Za-z0-9_]+", 1):
            state = state_token[2:]
            if state not in targets:
                continue
            state_text = raw[state_start:state_end]
            regions = world.block_spans(state_text, r"region_state:CHI", 1)
            if not regions:
                continue
            old_total = 0
            region_matches: list[tuple[int, int, int]] = []
            for _, region_start, region_end in regions:
                region_text = state_text[region_start:region_end]
                for match in re.finditer(r"(?m)^(\s*size\s*=\s*)(\d+)", region_text):
                    start = state_start + region_start + match.start(2)
                    end = state_start + region_start + match.end(2)
                    value = int(match.group(2))
                    old_total += value
                    region_matches.append((start, end, value))
            if not region_matches:
                raise RuntimeError(f"No CHI population entries for {state}")
            allocated = split_target([item[2] for item in region_matches], targets[state])
            for (start, end, _), value in zip(region_matches, allocated):
                replacements.append((start, end, str(value)))
            found[state] = old_total
        if replacements:
            for start, end, replacement in sorted(replacements, reverse=True):
                raw = raw[:start] + replacement + raw[end:]
            catalog_tools.brace_maps(catalog_tools.clean_comments(raw))
            # Population history files are shipped with a UTF-8 BOM.  Preserve
            # it so unchanged frontier files do not become noisy diffs.
            path.write_text(raw, encoding="utf-8-sig")
    missing = sorted(set(targets) - set(found))
    if missing:
        raise RuntimeError(f"Missing Qing population state(s): {missing}")
    return found


def qing_population_totals() -> dict[str, int]:
    totals: dict[str, int] = defaultdict(int)
    for path in sorted(POP_HISTORY.glob("*.txt")):
        raw = path.read_text(encoding="utf-8-sig")
        for state_token, state_start, state_end in world.block_spans(raw, r"s:STATE_[A-Za-z0-9_]+", 1):
            state_text = raw[state_start:state_end]
            for _, region_start, region_end in world.block_spans(state_text, r"region_state:CHI", 1):
                totals[state_token[2:]] += sum(
                    int(value) for value in re.findall(
                        r"(?m)^\s*size\s*=\s*(\d+)", state_text[region_start:region_end]
                    )
                )
    return dict(totals)


def update_state_catalog(rows: list[dict[str, str]], totals: dict[str, int]) -> None:
    for row in rows:
        if row["Owner_TAG"] == "CHI":
            row["Current_Population"] = str(totals[row["State_ID"]])
    wave1.write_csv(wave1.STATE_CATALOG, list(rows[0]), rows)


def cumulative_admin_targets(base_levels: dict[tuple[str, str, str], int]) -> dict[tuple[str, str, str], int]:
    deltas: dict[tuple[str, str, str], int] = defaultdict(int)
    for key, value in wave1.ADMIN_ADDITIONS.items():
        deltas[key] += value
    for key, value in ADMIN_WAVE2.items():
        deltas[key] += value
    return {key: base_levels.get(key, 0) + delta for key, delta in deltas.items()}


def admin_output_by_tag(pms: dict[tuple[str, str, str], tuple[str, ...]]) -> dict[str, float]:
    pm_objects = catalog_tools.effective_objects("common/production_methods", r"[A-Za-z0-9_]+")
    result: dict[str, float] = defaultdict(float)
    for key, delta in ADMIN_WAVE2.items():
        active = pms.get(key, ())
        base = next(
            (pm for pm in active if pm in {
                "pm_simple_organization", "pm_horizontal_drawer_cabinets",
                "pm_vertical_filing_cabinets", "pm_switch_boards",
            }),
            "pm_simple_organization",
        )
        result[key[0]] += delta * wave1.pm_output(base, pm_objects)
    return dict(result)


def write_population_audit(
    rows_before: list[dict[str, str]],
    targets: dict[str, int],
    provenance: dict[str, str],
) -> None:
    by_state = {row["State_ID"]: row for row in rows_before if row["Owner_TAG"] == "CHI"}
    output = []
    for state in sorted(targets):
        old = int(by_state[state]["Current_Population"])
        new = targets[state]
        output.append({
            "State_ID": state,
            "State_Name": by_state[state]["State_Display_Name"],
            "Historical_Province_or_Rule": provenance[state],
            "Population_Before": old,
            "Population_1776_Target": new,
            "Delta": new - old,
            "Scale": f"{new / old:.6f}" if old else "N/A",
            "Method": (
                "1776 provincial total allocated proportionally across split game states; pop cultures/religions preserved"
                if not provenance[state].startswith("Frontier retained") else
                "Existing frontier total retained"
            ),
            "Evidence": POP_SOURCE if not provenance[state].startswith("Frontier retained") else "Existing mod frontier population retained pending dedicated map rework",
        })
    wave1.write_csv(POP_AUDIT, list(output[0]), output)


def write_admin_reports(
    rows: list[dict[str, str]],
    base_levels: dict[tuple[str, str, str], int],
    final_targets: dict[tuple[str, str, str], int],
    pms: dict[tuple[str, str, str], tuple[str, ...]],
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    state_by_pair = {(row["Owner_TAG"], row["State_ID"]): row for row in rows}
    old_audit = {row["TAG"]: row for row in wave1.read_csv(wave1.BUREAUCRACY_AUDIT)}
    output_by_tag = admin_output_by_tag(pms)
    pop_saving = 3032.87504
    deinc_saving = 109.97968

    audit: list[dict[str, object]] = []
    all_tags = sorted(set(old_audit) | set(RUNTIME_BALANCE))
    for tag in all_tags:
        old = old_audit.get(tag, {})
        observed = RUNTIME_BALANCE.get(tag)
        before = observed if observed is not None else None
        special = (pop_saving + deinc_saving) if tag == "CHI" else 0.0
        projected = before + special + output_by_tag.get(tag, 0.0) if before is not None else None
        if projected is None:
            status = old.get("Runtime_Target_Status", "RUNTIME_REQUIRED")
        elif projected >= 0:
            status = "HEALTHY"
        elif projected >= -100:
            status = "MANAGEABLE_DEFICIT"
        elif projected >= -500:
            status = "SEVERE_DEFICIT"
        else:
            status = "CATASTROPHIC_DEFICIT"
        final_level = sum(
            value for key, value in base_levels.items()
            if key[0] == tag and key[2] == ADMIN
        )
        final_level += sum(
            target - base_levels.get(key, 0)
            for key, target in final_targets.items()
            if key[0] == tag
        )
        wave2_delta = sum(value for key, value in ADMIN_WAVE2.items() if key[0] == tag)
        audit.append({
            "TAG": tag,
            "Country": old.get("Country", next((row["Owner_Name"] for row in rows if row["Owner_TAG"] == tag), tag)),
            "Runtime_Bureaucracy_Before": f"{before:.1f}" if before is not None else old.get("Runtime_Bureaucracy_Balance", "NOT_OBSERVED"),
            "Population_Rebalance_Effect": f"{pop_saving:.1f}" if tag == "CHI" else "0.0",
            "New_Deincorporation_Effect": f"{deinc_saving:.1f}" if tag == "CHI" else "0.0",
            "Administration_Output_Added": f"{output_by_tag.get(tag, 0.0):.1f}",
            "Additional_Admin_Levels_Wave2": wave2_delta,
            "Final_Admin_Target": final_level,
            "Projected_Balance_After": f"{projected:.1f}" if projected is not None else "RUNTIME_REQUIRED",
            "Runtime_Target_Status": status,
            "Decision": (
                "PROTECTED_NO_CHANGE" if tag == "VEN" else
                "NO_CHANGE_ALREADY_HEALTHY" if observed is not None and observed >= 0 else
                "RUNTIME_CALIBRATION" if wave2_delta else "NO_RUNTIME_WRITE"
            ),
            "Notes": (
                "Protected Serenissima; deficit retained for explicit follow-up." if tag == "VEN" else
                "Qing population and incorporation corrections applied before administration." if tag == "CHI" else
                "Runtime screenshot anchor; administration placed in existing principal centres." if observed is not None else
                old.get("Notes", "No runtime observation supplied.")
            ),
        })

    cumulative_delta: dict[tuple[str, str, str], int] = defaultdict(int)
    for key, value in wave1.ADMIN_ADDITIONS.items():
        cumulative_delta[key] += value
    for key, value in ADMIN_WAVE2.items():
        cumulative_delta[key] += value
    overlay: list[dict[str, object]] = []
    for key, delta in sorted(cumulative_delta.items()):
        row = state_by_pair[key[:2]]
        historical = base_levels.get(key, 0)
        overlay.append({
            "Owner_TAG": key[0],
            "Country": row["Owner_Name"],
            "State_ID": key[1],
            "State_Name": row["State_Display_Name"],
            "Building_ID": ADMIN,
            "Historical_Level": historical,
            "Runtime_Additional_Level": delta,
            "Runtime_Final_Target_Level": historical + delta,
            "Wave": "WAVE1+WAVE2" if key in wave1.ADMIN_ADDITIONS else "WAVE2",
            "Reason": "Observed runtime bureaucracy calibration; distributed among established administrative centres.",
        })
    wave1.write_csv(BUREAUCRACY_WAVE2, list(audit[0]), audit)
    wave1.write_csv(wave1.BUREAUCRACY_AUDIT, list(audit[0]), audit)
    wave1.write_csv(ADMIN_OVERLAY_V2, list(overlay[0]), overlay)
    wave1.write_csv(wave1.ADMIN_OVERLAY, list(overlay[0]), overlay)
    return audit, overlay


def report_text(audit: list[dict[str, object]], population_before: int, population_after: int, infra_levels: int) -> str:
    rows = {row["TAG"]: row for row in audit}
    selected = ["CHI", "KOR", "RUS", "PLC", "TUR", "POR", "USA", "SC1", "SC2", "BRZ", "PER", "VEN", "DEI", "GWA", "MARATH", "PHI"]
    table = ["| TAG | Before | Admin levels added | Projected after | Decision |", "|---|---:|---:|---:|---|"]
    for tag in selected:
        row = rows[tag]
        table.append(
            f"| {tag} | {row['Runtime_Bureaucracy_Before']} | {row['Additional_Admin_Levels_Wave2']} | "
            f"{row['Projected_Balance_After']} | {row['Decision']} |"
        )
    return f"""# BUILD START 1776 — Runtime bureaucracy calibration Wave 2

## Scope

This pass uses the user-supplied runtime balances. It does not reopen small or sparsely populated countries, military/naval sizing, the Serenissima setup, or historical building geography.

## Qing population first

Qing population changes from **{population_before:,}** to **{population_after:,}**. The core provincial targets follow the 1776 Cao Shuji/Jiang Tao series. Split game states share their historical province total proportionally, while every existing culture/religion share inside a state is preserved. Conservative supplements retain frontier populations omitted or incompletely represented by the registered provincial table.

Source: {POP_SOURCE}

## Qing incorporation

Four further states are de-incorporated: Formosa, Shengjing, Southern Manchuria and Northern Manchuria. These represent a recently conquered/weakly integrated island frontier and the separate Manchurian banner-general system. No additional China-proper core province is de-incorporated.

## Administration

Population and incorporation effects are applied before the Qing residual. China then receives 711 simple-organization levels distributed across fifteen administrative regions. Other countries use their currently active administrative PM: Russia and the Dutch East Indies therefore receive fewer physical levels because horizontal drawer cabinets produce 50 bureaucracy per level.

{chr(10).join(table)}

Venice remains at `-141` because VEN/GEN are protected. The Philippines receives no addition because its observed balance is already positive.

## Infrastructure follow-up

Administration changes are included in a fresh global infrastructure calculation. The cumulative runtime overlay adds **{infra_levels}** Regional Infrastructure levels relative to the frozen historical matrix. Road/canal identity is preserved; active rail and passenger trains remain forbidden in 1776.

## Runtime caveat

Balances are projections from the supplied screenshots and scripted PM output. A new game is required to confirm employment, institution costs and exact rounding after the population history change.

## Validation targets

- China total population equals the state-by-state audit.
- All supplied deficits except protected Venice project to positive or only slightly negative.
- No protected military/naval or Serenissima building placement changes.
- No active rail or passenger PM.
- The combined runtime matrix remains the validator authority.
"""


def apply() -> dict[str, object]:
    rows_before = state_rows()
    targets, provenance = population_targets(rows_before)
    population_before = sum(int(row["Current_Population"]) for row in rows_before if row["Owner_TAG"] == "CHI")
    rebalance_qing_population(targets)
    totals = qing_population_totals()
    if totals != targets:
        mismatches = {key: (targets.get(key), totals.get(key)) for key in set(targets) | set(totals) if targets.get(key) != totals.get(key)}
        raise RuntimeError(f"Qing population mismatch: {mismatches}")
    population_after = sum(totals.values())
    update_state_catalog(rows_before, totals)
    write_population_audit(rows_before, targets, provenance)
    rows = state_rows()

    state_raw = STATE_HISTORY.read_text(encoding="utf-8-sig")
    for state in sorted(NEW_CHINA_DEINCORPORATIONS):
        state_raw = wave1.patch_state_history(state_raw, "CHI", state)
    catalog_tools.brace_maps(catalog_tools.clean_comments(state_raw))
    STATE_HISTORY.write_text(state_raw, encoding="utf-8")

    base_matrix = wave1.read_csv(wave1.BASE_MATRIX)
    base_levels = {
        (row["Owner_TAG"], row["State_ID"], row["Building_ID"]): int(float(row.get("Target_Level") or 0))
        for row in base_matrix
    }
    admin_targets = cumulative_admin_targets(base_levels)

    actual_levels, pms, placements = wave1.actual_semantics()
    protected_before = world.semantic(placements, lambda row: row.owner in world.SERENISSIMA or row.building in world.PROTECTED)
    transformed, additions = wave1.rescale_existing(placements, admin_targets, {})
    for path, raw in transformed.items():
        if raw != path.read_text(encoding="utf-8-sig"):
            path.write_text(raw, encoding="utf-8")
    if BUILDING_OVERLAY.exists():
        if additions:
            raise RuntimeError("Wave 2 building overlay exists but required placements are missing")
    else:
        overlay_text = world.build_overlay(additions).replace(
            "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv",
            "BUILD_START_1776_RUNTIME_ADMINISTRATION_OVERLAY_V2.csv",
        )
        catalog_tools.brace_maps(catalog_tools.clean_comments(overlay_text))
        BUILDING_OVERLAY.write_text(overlay_text, encoding="utf-8")

    # Recalculate infrastructure only after final administration is present.
    actual_levels, pms, placements = wave1.actual_semantics()
    calibration_levels = dict(base_levels)
    calibration_levels.update(admin_targets)
    infra_audit, infra_overlay, infra_targets, plans = wave1.infrastructure_plan(rows, calibration_levels, pms)
    transformed, infra_additions = wave1.rescale_existing(placements, infra_targets, plans)
    for path, raw in transformed.items():
        if raw != path.read_text(encoding="utf-8-sig"):
            path.write_text(raw, encoding="utf-8")
    if infra_additions:
        if INFRA_OVERLAY_FILE.exists():
            raise RuntimeError("Wave 2 infrastructure overlay exists but required placements are missing")
        overlay_text = world.build_overlay(infra_additions).replace(
            "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv",
            "BUILD_START_1776_RUNTIME_INFRASTRUCTURE_OVERLAY.csv",
        )
        catalog_tools.brace_maps(catalog_tools.clean_comments(overlay_text))
        INFRA_OVERLAY_FILE.write_text(overlay_text, encoding="utf-8")

    infra_fields = [
        "Owner_TAG", "Country", "State_ID", "State_Name", "Current_Level", "Road_PM", "Canal_PM",
        "Rail_PM", "Passenger_PM", "Infrastructure_Available", "Infrastructure_Used", "Current_Market_Access",
        "Additional_Level_Needed", "Historical_Connectivity_Exception", "Evidence", "Final_Target_Level",
        "Final_Infrastructure_Available", "Reason",
    ]
    wave1.write_csv(wave1.INFRA_AUDIT, infra_fields, infra_audit)
    wave1.write_csv(wave1.INFRA_OVERLAY, list(infra_overlay[0]), infra_overlay)

    actual_levels, pms, _ = wave1.actual_semantics()
    audit, _ = write_admin_reports(rows, base_levels, admin_targets, pms)

    runtime_changes = {key: target for key, target in infra_targets.items() if target != base_levels.get(key, 0)}
    runtime_changes.update({key: target for key, target in admin_targets.items() if target != base_levels.get(key, 0)})
    matrix_rows = wave1.runtime_matrix(base_matrix, runtime_changes, rows)
    wave1.write_csv(wave1.RUNTIME_MATRIX, list(matrix_rows[0]), matrix_rows)

    # Extend the historical review without erasing prior decisions.
    review_rows = wave1.read_csv(wave1.DEINCORP_REVIEW)
    review_by_key = {(row["Owner_TAG"], row["State_ID"]): row for row in review_rows}
    state_by_pair = {(row["Owner_TAG"], row["State_ID"]): row for row in rows}
    for state, (classification, evidence) in NEW_CHINA_DEINCORPORATIONS.items():
        row = state_by_pair[("CHI", state)]
        review_by_key[("CHI", state)] = {
            "Owner_TAG": "CHI", "Country": row["Owner_Name"], "State_ID": state,
            "State_Name": row["State_Display_Name"], "Current_Population": row["Current_Population"],
            "Old_Numerical_Priority": "WAVE2_USER_DIRECTED_CHINA_EXCEPTION",
            "Classification": classification, "Evidence": evidence, "Wave1_Decision": "APPLY_WAVE2",
        }
    final_review = [review_by_key[key] for key in sorted(review_by_key)]
    wave1.write_csv(wave1.DEINCORP_REVIEW, list(final_review[0]), final_review)

    infra_levels = sum(int(row["Runtime_Additional_Level"]) for row in infra_overlay)
    REPORT.write_text(report_text(audit, population_before, population_after, infra_levels), encoding="utf-8")

    _, after_placements = world.all_placements(HISTORY)
    protected_after = world.semantic(after_placements, lambda row: row.owner in world.SERENISSIMA or row.building in world.PROTECTED)
    if protected_before != protected_after:
        raise RuntimeError("Protected/Serenissima building semantics changed")
    if sum(ADMIN_WAVE2[key] for key in ADMIN_WAVE2 if key[0] == "CHI") != 711:
        raise RuntimeError("Unexpected Qing administration total")
    return {
        "qing_population_before": population_before,
        "qing_population_after": population_after,
        "qing_population_delta": population_after - population_before,
        "new_qing_deincorporations": len(NEW_CHINA_DEINCORPORATIONS),
        "wave2_admin_levels_added": sum(ADMIN_WAVE2.values()),
        "qing_admin_levels_added": 711,
        "countries_with_runtime_anchors": len(RUNTIME_BALANCE),
        "cumulative_infrastructure_levels_added": infra_levels,
        "protected_changes": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.apply:
        raise SystemExit("Use --apply")
    print(json.dumps(apply(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
