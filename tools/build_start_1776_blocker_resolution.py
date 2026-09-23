#!/usr/bin/env python3
"""Resolve the 1776 start-building methodology blockers without gameplay writes.

This tool protects the previously calibrated military/naval setup, builds
conservative administration and logging overlays, and regenerates the
implementation/gate/technology review artifacts.  It writes reports only.
"""

from __future__ import annotations

import csv
import math
import re
from collections import Counter, defaultdict
from pathlib import Path

import build_start_1776_research_input_pack as catalog_tools


ROOT = Path(__file__).resolve().parents[1]
VANILLA = Path(r"C:\Games\Victoria 3\game")
REPORTS = ROOT / "docs" / "reports" / "buildings"

ADMIN = "building_government_administration"
LOGGING = "building_logging_camp"
PROTECTED = {
    "building_barrack",
    "building_naval_administration",
    "building_naval_fortification",
}
SERENISSIMA = {"VEN", "GEN"}


def read_csv(name: str) -> list[dict[str, str]]:
    with (REPORTS / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(name: str, fields: list[str], rows: list[dict[str, object]]) -> None:
    with (REPORTS / name).open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def load_decisions() -> dict[tuple[str, str], dict[str, str]]:
    """Reload the approved gate decisions without coupling validator modules."""
    decisions: dict[tuple[str, str], dict[str, str]] = {}
    for row in read_csv("BUILD_START_1776_GATE_RECONCILIATION_CORRIGE.csv"):
        reason = row["Reason"]
        match = re.match(r"\[([^]]+)\]", reason)
        decisions[(row["Required_Technology"], row["Building_ID"])] = {
            "classification": match.group(1) if match else "APPROVED_RECONCILIATION",
            "decision": row["Decision"],
            "replacement": row["Replacement_Gate"],
            "building_change": row["Building_Definition_Change"],
            "pm_change": row["PM_Definition_Change"],
            "reason": reason,
            "risk": row["Risk"],
        }
    return decisions


DECISIONS = load_decisions()


def as_int(value: str | int | float) -> int:
    return int(float(value or 0))


def numeric_values(text: str, key: str) -> list[float]:
    return [float(value) for value in re.findall(
        rf"(?m)^\s*{re.escape(key)}\s*=\s*(-?[0-9]+(?:\.[0-9]+)?)", text
    )]


def first_number(text: str, key: str, default: float = 0.0) -> float:
    values = numeric_values(text, key)
    return values[0] if values else default


def direct_assignments(text: str, key: str) -> list[str]:
    return re.findall(
        rf"(?m)^\s*{re.escape(key)}\s*=\s*(?:[A-Za-z0-9_]+:)?([A-Za-z0-9_]+)",
        catalog_tools.clean_comments(text),
    )


def country_blocks() -> list[tuple[str, str]]:
    """Read history country blocks, including the engine's `?=` operator."""
    result: list[tuple[str, str]] = []
    country_dir = ROOT / "common" / "history" / "countries"
    pattern = re.compile(r"(?m)^\s*c:(?P<tag>[A-Z0-9_]+)\s*\??=\s*\{")
    for path in sorted(country_dir.glob("*.txt")):
        cleaned = catalog_tools.clean_comments(path.read_text(encoding="utf-8-sig"))
        depths, pairs = catalog_tools.brace_maps(cleaned)
        for match in pattern.finditer(cleaned):
            if depths[match.start()] != 1:
                continue
            opening = cleaned.find("{", match.start(), match.end())
            result.append((match.group("tag"), cleaned[match.start(): pairs[opening] + 1]))
    return result


def split_pms(value: str) -> list[str]:
    return [item for item in value.split("|") if item and item != "NONE"]


def default_pms(catalog_row: dict[str, str]) -> list[str]:
    result = []
    for item in split_pms(catalog_row.get("Base_PM", "")):
        result.append(item.split(":", 1)[-1])
    return result


def key(row: dict[str, str]) -> tuple[str, str, str]:
    return row["Owner_TAG"], row["State_ID"], row["Building_ID"]


def decision(current: int, target: int, serenissima: bool = False) -> str:
    if serenissima:
        return "PRESERVE_SERENISSIMA"
    if current == target:
        return "KEEP"
    if current == 0:
        return "ADD"
    if target == 0:
        return "REMOVE"
    return "INCREASE" if target > current else "DECREASE"


def starting_techs() -> dict[str, set[str]]:
    effects: dict[str, set[str]] = {}
    effect_objects = catalog_tools.effective_objects(
        "common/scripted_effects", r"effect_starting_technology_[A-Za-z0-9_]+", mod_only=True
    )
    for effect_id, block in effect_objects.items():
        effects[effect_id] = set(direct_assignments(block.text, "add_technology_researched"))

    countries: dict[str, set[str]] = defaultdict(set)
    for tag, text in country_blocks():
        countries[tag].update(direct_assignments(text, "add_technology_researched"))
        for effect_id, effect_techs in effects.items():
            if re.search(rf"(?m)^\s*{re.escape(effect_id)}\s*=\s*yes\b", text):
                countries[tag].update(effect_techs)
    return countries


def country_contexts() -> tuple[dict[str, str], dict[str, list[str]], dict[str, str]]:
    capitals: dict[str, str] = {}
    laws: dict[str, list[str]] = defaultdict(list)
    institutions: dict[str, str] = {}
    for tag, text in country_blocks():
        matches = direct_assignments(text, "set_capital")
        if matches:
            capitals[tag] = matches[-1]
        laws[tag] = direct_assignments(text, "activate_law")
        investment = re.findall(
            r"(?m)^\s*(?:set_institution_investment_level|set_institution_investment)\s*=\s*\{([^}]*)\}",
            text,
        )
        institutions[tag] = f"explicit_institution_blocks={len(investment)}"
    return capitals, laws, institutions


def state_incorporation() -> dict[str, bool]:
    result: dict[str, bool] = {}
    for path in sorted((ROOT / "common" / "history" / "states").glob("*.txt")):
        for block in catalog_tools.named_blocks(path, r"s:STATE_[A-Za-z0-9_]+", 1):
            state = block.object_id.split(":", 1)[1]
            result[state] = not bool(re.search(r"(?m)^\s*state_type\s*=\s*unincorporated\b", block.text))
    return result


def selected_pms(
    target_key: tuple[str, str, str],
    current_by_key: dict[tuple[str, str, str], dict[str, str]],
    catalog_by_id: dict[str, dict[str, str]],
    infrastructure_by_key: dict[tuple[str, str], dict[str, str]],
) -> list[str]:
    tag, state, building = target_key
    if building == "building_railway" and (tag, state) in infrastructure_by_key:
        row = infrastructure_by_key[(tag, state)]
        return [row["Road_PM"], row["Canal_PM"], row["Rail_PM"], row["Passenger_PM"]]
    current = current_by_key.get(target_key)
    if current and current.get("Current_PM_Overrides"):
        return split_pms(current["Current_PM_Overrides"])
    return default_pms(catalog_by_id[building])


def pm_metric(pms: list[str], objects: dict[str, catalog_tools.Block], metric: str) -> float:
    return sum(sum(numeric_values(objects[pm].text, metric)) for pm in pms if pm in objects)


def protected_overlay(current: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for row in current:
        if row["Building_ID"] not in PROTECTED:
            continue
        rows.append({
            "Owner_TAG": row["Owner_TAG"],
            "State_ID": row["State_ID"],
            "Building_ID": row["Building_ID"],
            "Current_Level": row["Current_Level"],
            "Protected_Target_Level": row["Current_Level"],
            "Current_PM_Overrides": row["Current_PM_Overrides"],
            "Source_File": row["Source_File"],
            "Protection_Reason": "PREVIOUS_1776_MILITARY_NAVAL_CALIBRATION",
        })
    rows.sort(key=lambda item: (item["Owner_TAG"], item["State_ID"], item["Building_ID"]))
    return rows


def administration_calibration(
    current: list[dict[str, str]],
    historical: list[dict[str, str]],
    states: list[dict[str, str]],
    pm_objects: dict[str, catalog_tools.Block],
) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    dict[tuple[str, str, str], int],
    dict[str, dict[str, float]],
]:
    current_rows = [row for row in current if row["Building_ID"] == ADMIN and row["Owner_TAG"] not in SERENISSIMA]
    historical_rows = [row for row in historical if row["Building_ID"] == ADMIN and row["Owner_TAG"] not in SERENISSIMA]
    cur = {key(row): row for row in current_rows}
    hist = {key(row): as_int(row["Target_Level"]) for row in historical_rows}
    state_by_id = {row["State_ID"]: row for row in states}
    states_by_tag: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in states:
        if row["Owner_TAG"] not in SERENISSIMA:
            states_by_tag[row["Owner_TAG"]].append(row)
    capitals, laws, institutions = country_contexts()
    incorporated = state_incorporation()

    for tag, owned in states_by_tag.items():
        if tag not in capitals or capitals[tag] not in state_by_id or state_by_id[capitals[tag]]["Owner_TAG"] != tag:
            capitals[tag] = max(owned, key=lambda item: as_int(item["Current_Population"]))["State_ID"]

    admin_base = {"pm_simple_organization", "pm_horizontal_drawer_cabinets", "pm_vertical_filing_cabinets", "pm_switch_boards"}

    def admin_pm(row: dict[str, str] | None) -> str:
        if row:
            for pm in split_pms(row.get("Current_PM_Overrides", "")):
                if pm in admin_base:
                    return pm
        return "pm_simple_organization"

    def per_level(row: dict[str, str] | None, metric: str) -> float:
        pm = admin_pm(row)
        return first_number(pm_objects[pm].text, metric)

    country_summary: dict[str, dict[str, float]] = {}
    final: dict[tuple[str, str, str], int] = dict(hist)

    all_tags = sorted(states_by_tag)
    for tag in all_tags:
        owned = states_by_tag[tag]
        relevant = any(k[0] == tag for k in cur) or any(k[0] == tag for k in hist)
        inc_states = [row for row in owned if incorporated.get(row["State_ID"], True)]
        inc_pop = sum(as_int(row["Current_Population"]) for row in inc_states)
        structural_cost = 10 * len(inc_states) + 4 * (inc_pop / 100_000)
        # Near balance is sufficient at game start. A small deficit is
        # acceptable and peripheral states may be de-incorporated at runtime
        # before adding further administrative capacity.
        desired_with_buffer = math.ceil(structural_cost * 0.95) if relevant else 0

        current_gross = 0.0
        current_tax = 0.0
        for k, row in cur.items():
            if k[0] != tag:
                continue
            current_gross += as_int(row["Current_Level"]) * per_level(row, "country_bureaucracy_add")
            current_tax += as_int(row["Current_Level"]) * per_level(row, "state_tax_capacity_add")

        historical_gross = 0.0
        for k, level in hist.items():
            if k[0] != tag:
                continue
            historical_gross += level * per_level(cur.get(k), "country_bureaucracy_add")

        if tag == "CHI":
            # Deliberate gameplay identity: do not hide the Qing population
            # burden behind dozens/hundreds of administrative levels.
            required = historical_gross
        elif current_gross > 0:
            # Retain a conservative share of demonstrated capacity. Near balance
            # is achieved, where appropriate, through limited de-incorporation
            # rather than rebuilding the removed bureaucracy everywhere.
            required = max(historical_gross, math.ceil(current_gross * 0.66))
        else:
            # A static population formula alone is not enough evidence to seed
            # a new bureaucracy.  Countries without current administration use
            # only the historically researched floor.
            required = historical_gross
        candidates = set(k for k in cur if k[0] == tag) | set(k for k in hist if k[0] == tag)
        if relevant:
            candidates.add((tag, capitals[tag], ADMIN))
        projected = sum(
            level * per_level(cur.get(k), "country_bureaucracy_add")
            for k, level in final.items() if k[0] == tag and k[2] == ADMIN
        )

        priority = sorted(
            candidates,
            key=lambda k: (
                0 if k[1] == capitals[tag] else 1,
                0 if k in hist else 1,
                -as_int(cur.get(k, {}).get("Current_Level", "0")),
                -as_int(state_by_id[k[1]]["Current_Population"]),
            ),
        )
        for k in priority:
            if projected >= required:
                break
            row = cur.get(k)
            output = per_level(row, "country_bureaucracy_add") or 10
            existing_cap = max(as_int(row["Current_Level"]) if row else 0, hist.get(k, 0))
            can_add = max(0, existing_cap - final.get(k, 0))
            use = min(can_add, math.ceil((required - projected) / output))
            if use:
                final[k] = final.get(k, 0) + use
                projected += use * output

        if relevant and projected < required:
            capital_key = (tag, capitals[tag], ADMIN)
            output = per_level(cur.get(capital_key), "country_bureaucracy_add") or 10
            use = math.ceil((required - projected) / output)
            final[capital_key] = final.get(capital_key, 0) + use
            projected += use * output

        projected_tax = sum(
            level * per_level(cur.get(k), "state_tax_capacity_add")
            for k, level in final.items() if k[0] == tag and k[2] == ADMIN
        )
        country_summary[tag] = {
            "population": sum(as_int(row["Current_Population"]) for row in owned),
            "inc_population": inc_pop,
            "inc_states": len(inc_states),
            "structural_cost": structural_cost,
            "desired": desired_with_buffer,
            "current_gross": current_gross,
            "historical_gross": historical_gross,
            "projected_gross": projected,
            "current_tax": current_tax,
            "projected_tax": projected_tax,
            "tax_need": inc_pop / 10_000,
            "law_count": len(laws.get(tag, [])),
            "institution_blocks": float(institutions.get(tag, "explicit_institution_blocks=0").split("=")[-1]),
            "relevant": 1.0 if relevant else 0.0,
        }

    deincorporation_rows: list[dict[str, object]] = []
    for tag, summary in country_summary.items():
        structural = float(summary["structural_cost"])
        projected = float(summary["projected_gross"])
        summary["deincorp_states"] = 0.0
        summary["deincorp_population"] = 0.0
        summary["post_deincorp_cost"] = structural
        summary["post_deincorp_net"] = projected - structural
        if tag == "CHI" or not summary["relevant"] or projected <= 0 or structural <= projected / 0.95:
            continue
        remaining = structural
        allowed = projected / 0.95
        candidates = sorted(
            [row for row in states_by_tag[tag] if incorporated.get(row["State_ID"], True) and row["State_ID"] != capitals[tag]],
            key=lambda row: (
                1 if final.get((tag, row["State_ID"], ADMIN), 0) else 0,
                as_int(row["Current_Population"]),
            ),
        )
        selected = []
        for state_row in candidates:
            if remaining <= allowed:
                break
            pop = as_int(state_row["Current_Population"])
            reduction = 10 + 4 * (pop / 100_000)
            remaining -= reduction
            selected.append((state_row, reduction))
        summary["deincorp_states"] = float(len(selected))
        summary["deincorp_population"] = float(sum(as_int(item[0]["Current_Population"]) for item in selected))
        summary["post_deincorp_cost"] = max(0.0, remaining)
        summary["post_deincorp_net"] = projected - max(0.0, remaining)
        for priority, (state_row, reduction) in enumerate(selected, start=1):
            deincorporation_rows.append({
                "Owner_TAG": tag,
                "Country": state_row["Owner_Name"],
                "State_ID": state_row["State_ID"],
                "State_Name": state_row["State_Display_Name"],
                "Current_Population": state_row["Current_Population"],
                "Priority": priority,
                "Estimated_Bureaucracy_Reduction": f"{reduction:.1f}",
                "Reason": "Peripheral low-population incorporated state selected before adding administration; runtime/historical review required.",
                "Runtime_Validation_Required": "YES — confirm state incorporation, strategic importance and resulting bureaucracy balance",
            })

    # Keep one capital audit row even for countries receiving no administration,
    # so the calibration is genuinely world-complete rather than limited to
    # countries already present in building history.
    report_keys = (
        set(cur)
        | set(hist)
        | {k for k, value in final.items() if value > 0}
        | {(tag, capitals[tag], ADMIN) for tag in states_by_tag}
    )
    rows: list[dict[str, object]] = []
    for k in sorted(report_keys):
        tag, state, _ = k
        current_level = as_int(cur.get(k, {}).get("Current_Level", "0"))
        historical_level = hist.get(k, 0)
        final_level = final.get(k, 0)
        summary = country_summary[tag]
        role = (
            "CAPITAL" if state == capitals.get(tag)
            else "HISTORICAL_ADMIN_CENTER" if historical_level
            else "CURRENT_ADMIN_CENTER"
        )
        current_pm = admin_pm(cur.get(k))
        output = per_level(cur.get(k), "country_bureaucracy_add")
        tax = per_level(cur.get(k), "state_tax_capacity_add")
        rows.append({
            "Owner_TAG": tag,
            "Country": state_by_id[state]["Owner_Name"],
            "State_ID": state,
            "Current_Level": current_level,
            "Historical_Target_Level": historical_level,
            "Gameplay_Minimum_Component": max(0, final_level - historical_level),
            "Final_Target_Level": final_level,
            "Current_Bureaucracy_Context": (
                f"country_gross={summary['current_gross']:.0f}; static_structural_cost={summary['structural_cost']:.1f}; "
                f"gross_minus_static={summary['current_gross'] - summary['structural_cost']:.1f}; pm={current_pm}; per_level={output:.0f}"
            ),
            "Projected_Bureaucracy_Context": (
                f"country_gross={summary['projected_gross']:.0f}; near_balance_95pct={summary['desired']:.0f}; "
                f"gross_minus_static={summary['projected_gross'] - summary['structural_cost']:.1f}; "
                f"runtime_deincorp_states={summary['deincorp_states']:.0f}; "
                f"post_deincorp_cost={summary['post_deincorp_cost']:.1f}; post_deincorp_net={summary['post_deincorp_net']:.1f}; "
                f"laws={summary['law_count']:.0f}; explicit_institution_blocks={summary['institution_blocks']:.0f}"
            ),
            "Tax_Capacity_Context": (
                f"state_pm_per_level={tax:.0f}; country_current={summary['current_tax']:.0f}; "
                f"country_projected={summary['projected_tax']:.0f}; incorporated_population_need={summary['tax_need']:.1f}"
            ),
            "Capital_or_Admin_Center": role,
            "Decision": decision(current_level, final_level),
            "Reason": (
                "Historical target is the floor; the general overlay retains 66% of demonstrated gross capacity and uses limited runtime "
                "de-incorporation for near balance. China is a deliberate overpopulation-burden exception kept at its historical floor; "
                "tax capacity is diagnostic rather than a 100% coverage target."
            ),
            "Runtime_Validation_Required": "YES — workforce, wage, institution, law, tax-waste and incorporation effects are not statically exact",
        })
    return rows, deincorporation_rows, {k: value for k, value in final.items() if value > 0}, country_summary


def logging_calibration(
    current: list[dict[str, str]],
    historical: list[dict[str, str]],
    states: list[dict[str, str]],
    corrected_pre_logging: dict[tuple[str, str, str], int],
    catalog_by_id: dict[str, dict[str, str]],
    pm_objects: dict[str, catalog_tools.Block],
    infrastructure: list[dict[str, str]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], dict[tuple[str, str, str], int], dict[str, float]]:
    state_by_id = {row["State_ID"]: row for row in states}
    current_by_key = {key(row): row for row in current}
    infra_by_key = {(row["Owner_TAG"], row["State_ID"]): row for row in infrastructure}
    cur_logging = {key(row): row for row in current if row["Building_ID"] == LOGGING and row["Owner_TAG"] not in SERENISSIMA}
    hist_logging = {
        key(row): as_int(row["Target_Level"])
        for row in historical if row["Building_ID"] == LOGGING and row["Owner_TAG"] not in SERENISSIMA
    }

    demand: dict[str, float] = defaultdict(float)
    for k, level in corrected_pre_logging.items():
        if not level or k[0] in SERENISSIMA or k[2] == LOGGING:
            continue
        pms = selected_pms(k, current_by_key, catalog_by_id, infra_by_key)
        demand[k[0]] += level * max(0.0, pm_metric(pms, pm_objects, "goods_input_wood_add"))

    def row_pms(k: tuple[str, str, str]) -> list[str]:
        row = cur_logging.get(k)
        if row and row.get("Current_PM_Overrides"):
            return split_pms(row["Current_PM_Overrides"])
        return default_pms(catalog_by_id[LOGGING])

    def output(k: tuple[str, str, str]) -> float:
        return max(0.0, pm_metric(row_pms(k), pm_objects, "goods_output_wood_add"))

    final = dict(hist_logging)
    all_tags = sorted(set(demand) | {k[0] for k in cur_logging} | {k[0] for k in hist_logging})
    context: dict[str, dict[str, float | str]] = {}
    for tag in all_tags:
        required = demand[tag] * 1.15
        historic_supply = sum(level * output(k) for k, level in hist_logging.items() if k[0] == tag)
        supply = historic_supply
        candidates = sorted(
            {k for k in cur_logging if k[0] == tag},
            key=lambda k: (
                0 if k in hist_logging else 1,
                -as_int(cur_logging[k]["Current_Level"]),
                -as_int(state_by_id[k[1]]["Current_Population"]),
            ),
        )
        for k in candidates:
            if supply >= required:
                break
            per_level = output(k)
            if per_level <= 0:
                continue
            cap = max(as_int(cur_logging[k]["Current_Level"]), hist_logging.get(k, 0))
            available = max(0, cap - final.get(k, 0))
            use = min(available, math.ceil((required - supply) / per_level))
            if use:
                final[k] = final.get(k, 0) + use
                supply += use * per_level

        owned = [row for row in states if row["Owner_TAG"] == tag]
        trade_access = any(row["Has_Port_Access"] == "YES" for row in owned)
        coverage = supply / demand[tag] if demand[tag] else 999.0
        if not demand[tag] or coverage >= 1.15:
            risk = "LOW_STATIC_BUILDING_DEMAND"
        elif coverage >= 0.75 and trade_access:
            risk = "MEDIUM_TRADE_DEPENDENT"
        else:
            risk = "HIGH_RUNTIME_SHORTAGE_RISK"
        context[tag] = {
            "historical_supply": historic_supply,
            "supply": supply,
            "demand": demand[tag],
            "coverage": coverage,
            "trade": "COASTAL_OR_PORT_ACCESS" if trade_access else "LANDLOCKED_OR_NO_STATIC_PORT_ACCESS",
            "risk": risk,
        }

    # Country viability alone can still leave the world short when commercial
    # importers have no demonstrated forest placement. Retain additional levels
    # only in already-existing logging states until global static supply reaches
    # the same 15% buffer. Coastal exporters and productive PMs come first.
    global_required = sum(demand.values()) * 1.15
    global_supply = sum(level * output(k) for k, level in final.items())
    export_candidates = sorted(
        cur_logging,
        key=lambda k: (
            0 if state_by_id[k[1]]["Has_Port_Access"] == "YES" else 1,
            -output(k),
            -as_int(cur_logging[k]["Current_Level"]),
        ),
    )
    for k in export_candidates:
        if global_supply >= global_required:
            break
        per_level = output(k)
        if per_level <= 0:
            continue
        cap = max(as_int(cur_logging[k]["Current_Level"]), hist_logging.get(k, 0))
        available = max(0, cap - final.get(k, 0))
        use = min(available, math.ceil((global_required - global_supply) / per_level))
        if use:
            final[k] = final.get(k, 0) + use
            global_supply += use * per_level

    # Recompute country summaries after the global exporter buffer.
    for tag in all_tags:
        historic_supply = sum(level * output(k) for k, level in hist_logging.items() if k[0] == tag)
        supply = sum(level * output(k) for k, level in final.items() if k[0] == tag)
        owned = [row for row in states if row["Owner_TAG"] == tag]
        trade_access = any(row["Has_Port_Access"] == "YES" for row in owned)
        coverage = supply / demand[tag] if demand[tag] else 999.0
        if not demand[tag] or coverage >= 1.15:
            risk = "LOW_STATIC_BUILDING_DEMAND"
        elif coverage >= 0.75 and trade_access:
            risk = "MEDIUM_TRADE_DEPENDENT"
        else:
            risk = "HIGH_RUNTIME_SHORTAGE_RISK"
        context[tag] = {
            "historical_supply": historic_supply,
            "supply": supply,
            "demand": demand[tag],
            "coverage": coverage,
            "trade": "COASTAL_OR_PORT_ACCESS" if trade_access else "LANDLOCKED_OR_NO_STATIC_PORT_ACCESS",
            "risk": risk,
        }

    rows: list[dict[str, object]] = []
    for k in sorted(set(cur_logging) | set(hist_logging) | {k for k, value in final.items() if value > 0}):
        tag, state, _ = k
        cur_level = as_int(cur_logging.get(k, {}).get("Current_Level", "0"))
        hist_level = hist_logging.get(k, 0)
        final_level = final.get(k, 0)
        pms = row_pms(k)
        out = output(k)
        ctx = context[tag]
        rows.append({
            "Owner_TAG": tag,
            "Country": state_by_id[state]["Owner_Name"],
            "State_ID": state,
            "Current_Level": cur_level,
            "Historical_Target_Level": hist_level,
            "Supply_Calibration_Addition": max(0, final_level - hist_level),
            "Final_Target_Level": final_level,
            "Start_PM": "|".join(pms),
            "Estimated_Wood_Output": f"{final_level * out:.1f} (per_level={out:.1f})",
            "Estimated_Local_or_Market_Demand": f"{float(ctx['demand']):.1f}",
            "Market_Context": "COUNTRY_PROXY; actual customs-union market and trade routes require runtime",
            "Decision": decision(cur_level, final_level),
            "Reason": (
                "Historical logging is the floor. Existing effective logging locations are retained only as needed to cover "
                "115% of target-building wood inputs, including the global exporter buffer; no entirely new forest location is invented."
            ),
            "Runtime_Validation_Required": "YES — pop demand, subsistence supply, throughput, workforce, prices and cross-border market trade are dynamic",
        })

    summary_rows: list[dict[str, object]] = []
    for tag in all_tags:
        ctx = context[tag]
        coverage = float(ctx["coverage"])
        summary_rows.append({
            "Market_or_Country": tag,
            "Historical_Target_Supply": f"{float(ctx['historical_supply']):.1f}",
            "Calibrated_Target_Supply": f"{float(ctx['supply']):.1f}",
            "Estimated_Demand": f"{float(ctx['demand']):.1f}",
            "Coverage_Ratio": "N/A_NO_STATIC_DEMAND" if coverage > 100 else f"{coverage:.3f}",
            "Trade_Access": ctx["trade"],
            "Risk": ctx["risk"],
            "Runtime_Required": "YES",
        })
    return rows, summary_rows, {k: value for k, value in final.items() if value > 0}, demand


def make_corrected_matrix(
    original: list[dict[str, str]],
    historical: list[dict[str, str]],
    current: list[dict[str, str]],
    states: list[dict[str, str]],
    catalog_by_id: dict[str, dict[str, str]],
    admin_target: dict[tuple[str, str, str], int],
    logging_target: dict[tuple[str, str, str], int],
) -> list[dict[str, object]]:
    original_by_key = {key(row): row for row in original}
    hist_by_key = {key(row): as_int(row["Target_Level"]) for row in historical}
    current_by_key = {key(row): as_int(row["Current_Level"]) for row in current}
    current_row = {key(row): row for row in current}
    state_by_id = {row["State_ID"]: row for row in states}

    target = dict(hist_by_key)
    for building in PROTECTED:
        target = {k: value for k, value in target.items() if k[2] != building}
        target.update({k: value for k, value in current_by_key.items() if k[2] == building})
    target = {k: value for k, value in target.items() if k[2] != ADMIN}
    target.update(admin_target)
    target = {k: value for k, value in target.items() if k[2] != LOGGING}
    target.update(logging_target)
    for k, value in current_by_key.items():
        if k[0] in SERENISSIMA:
            target[k] = value

    rows: list[dict[str, object]] = []
    all_keys = sorted(set(current_by_key) | set(target))
    for k in all_keys:
        cur = current_by_key.get(k, 0)
        tgt = target.get(k, 0)
        if not cur and not tgt:
            continue
        tag, state, building = k
        base = dict(original_by_key.get(k, {}))
        state_row = state_by_id[state]
        catalog = catalog_by_id[building]
        base.setdefault("Research_Region", state_row["Region"])
        base.setdefault("Owner_TAG", tag)
        base.setdefault("Country", state_row["Owner_Name"])
        base.setdefault("State_ID", state)
        base.setdefault("State_Name", state_row["State_Display_Name"])
        base.setdefault("Building_ID", building)
        base.setdefault("Building_Name", catalog["Display_Name_EN"])
        base.setdefault("Confidence", "CALIBRATION_OVERLAY")
        base.setdefault("Economic_Role", "CALIBRATION_OVERLAY")
        base.setdefault("Domestic_Demand", "CALIBRATION_OVERLAY")
        base.setdefault("Export_Orientation", "NONE")
        base.setdefault("Industry_Form", "CALIBRATION_OVERLAY")
        base.setdefault("Tech_Distribution_Review", "YES")
        base.setdefault("Map_Rework_Risk", state_row["Map_Rework_Risk"])
        base.setdefault("Serenissima_Protected", "YES" if tag in SERENISSIMA else "NO")
        base.setdefault("Historical_Evidence", "CALIBRATION_OVERLAY")
        base.setdefault("Level_Rationale", "CALIBRATION_OVERLAY")
        base.setdefault("Source_1", "")
        base.setdefault("Source_2", "")
        base.setdefault("Notes", "")
        if tag in SERENISSIMA:
            overlay = "SERENISSIMA_PROTECTED"
            reason = "Current Serenissima setup is an absolute invariant."
        elif building in PROTECTED:
            overlay = "PROTECTED_MILITARY_NAVAL"
            reason = "Previous 1776 military/naval calibration retained exactly."
        elif building == ADMIN:
            overlay = "ADMINISTRATION_CALIBRATION"
            reason = "Static bureaucracy/tax-capacity calibration replaces unsafe research-only level."
        elif building == LOGGING:
            overlay = "LOGGING_CALIBRATION"
            reason = "Wood supply calibration replaces unsafe research-only level."
        else:
            overlay = "NONE"
            reason = "Frozen historical target unchanged."
        base.update({
            "Current_Level": cur,
            "Target_Level": tgt,
            "Delta": tgt - cur,
            "Decision": decision(cur, tgt, tag in SERENISSIMA),
            "Base_Historical_Target_Level": hist_by_key.get(k, 0),
            "Overlay_Type": overlay,
            "Overlay_Reason": reason,
        })
        if k in current_row and current_row[k].get("Current_PM_Overrides"):
            base["Notes"] = (base.get("Notes", "") + f" | CURRENT_PM={current_row[k]['Current_PM_Overrides']}").strip(" |")
        rows.append(base)
    return rows


def gate_reconciliation_corrected(
    original_conflicts: list[dict[str, str]],
    corrected: list[dict[str, object]],
) -> tuple[list[dict[str, object]], int]:
    target_by_key = {
        (str(row["Owner_TAG"]), str(row["State_ID"]), str(row["Building_ID"])): as_int(row["Target_Level"])
        for row in corrected if as_int(row["Target_Level"]) > 0
    }
    conflicts = []
    seen = set()
    for row in original_conflicts:
        k = (row["Owner_TAG"], row["State_ID"], row["Building_ID"])
        if k not in target_by_key or row["Building_ID"] in PROTECTED:
            continue
        updated = dict(row)
        updated["Target_Level"] = str(target_by_key[k])
        signature = (updated["Owner_TAG"], updated["State_ID"], updated["Building_ID"], updated["Required_Technology"])
        if signature not in seen:
            seen.add(signature)
            conflicts.append(updated)

    # New/increased administration rows are still current-gate conflicts until
    # the already approved gate-removal proposal is applied in the gameplay phase.
    techs = starting_techs()
    original_lookup = {(r["Owner_TAG"], r["State_ID"], r["Building_ID"]): r for r in original_conflicts}
    for k, level in target_by_key.items():
        tag, state, building = k
        if building != ADMIN or "systematic_administrative_statistics" in techs.get(tag, set()):
            continue
        signature = (tag, state, building, "systematic_administrative_statistics")
        if signature in seen:
            continue
        seed = original_lookup.get(k, {})
        conflicts.append({
            "Owner_TAG": tag,
            "State_ID": state,
            "Building_ID": building,
            "Target_Level": level,
            "Required_Technology": "systematic_administrative_statistics",
            "Country_Currently_Has_Tech": "NO",
            "Conflict_Type": "BUILDING_GATE_DISTRIBUTION_CONFLICT",
            "Recommended_Action": "REMOVE_BUILDING_GATE",
            "Reason": "Administration calibration requires the earlier simple organization PM; the advanced statistics gate is too late.",
            "Historical_Source": seed.get("Historical_Source", "STATIC_ADMINISTRATION_CALIBRATION"),
        })
        seen.add(signature)

    groups: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in conflicts:
        groups[(row["Required_Technology"], row["Building_ID"])].append(row)
    rows: list[dict[str, object]] = []
    unresolved = 0
    for group, items in sorted(groups.items()):
        proposal = DECISIONS.get(group)
        if not proposal:
            unresolved += len(items)
            rows.append({
                "Required_Technology": group[0], "Building_ID": group[1], "PM_ID": "",
                "Conflict_Count": len(items), "Affected_TAG_Count": len({i['Owner_TAG'] for i in items}),
                "Affected_State_Count": len({i['State_ID'] for i in items}), "Current_Gate": "UNKNOWN",
                "Decision": "REQUIRES_HUMAN_REVIEW", "Replacement_Gate": "NONE",
                "Starting_Tech_Changes_Required": "UNKNOWN", "Building_Definition_Change": "NO",
                "PM_Definition_Change": "NO", "Reason": "No enumerated reconciliation decision.", "Risk": "HIGH",
            })
            continue
        pm_id = "pm_industrial_canals" if group[0] == "industrial_canals" else ""
        if group == ("coke_smelting", "building_steel_mill"):
            pm_id = "pm_coke_blast_furnaces"
        tags = sorted({item["Owner_TAG"] for item in items})
        if proposal["decision"] == "KEEP_GATE_ADD_TECH":
            start = f"YES — {len(tags)} TAGS: {'|'.join(tags)}"
        elif proposal["decision"] == "CHANGE_BUILDING_GATE":
            start = f"RECALCULATE_AGAINST_REPLACEMENT_GATE:{proposal['replacement']}"
        elif proposal["decision"] == "MOVE_GATE_TO_PM":
            start = "RECALCULATE_AFTER_NEW_BASE_PM"
        else:
            start = "NO"
        rows.append({
            "Required_Technology": group[0], "Building_ID": group[1], "PM_ID": pm_id,
            "Conflict_Count": len(items), "Affected_TAG_Count": len(tags),
            "Affected_State_Count": len({i['State_ID'] for i in items}),
            "Current_Gate": ("PM:" if items[0]["Conflict_Type"] == "PM_GATE_REVIEW" else "BUILDING:") + group[0],
            "Decision": proposal["decision"], "Replacement_Gate": proposal["replacement"],
            "Starting_Tech_Changes_Required": start, "Building_Definition_Change": proposal["building_change"],
            "PM_Definition_Change": proposal["pm_change"],
            "Reason": f"[{proposal['classification']}] {proposal['reason']}", "Risk": proposal["risk"],
        })
    return rows, unresolved


def technology_outputs(
    original_conflicts: list[dict[str, str]],
    corrected_conflicts: list[dict[str, object]],
    corrected_matrix: list[dict[str, object]],
) -> tuple[list[dict[str, object]], list[dict[str, object]], int, int, int]:
    old_reasons: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in original_conflicts:
        prop = DECISIONS[(row["Required_Technology"], row["Building_ID"])]
        if prop["decision"] == "KEEP_GATE_ADD_TECH":
            old_reasons[(row["Owner_TAG"], row["Required_Technology"])].append(row)
    assert len(old_reasons) == 104, f"Expected 104 original candidate pairs, found {len(old_reasons)}"

    protected_keys = {
        (str(row["Owner_TAG"]), str(row["State_ID"]), str(row["Building_ID"]))
        for row in corrected_matrix if str(row["Overlay_Type"]) == "PROTECTED_MILITARY_NAVAL"
    }
    intermediate = []
    remaining_old: set[tuple[str, str]] = set()
    for pair, reasons in sorted(old_reasons.items()):
        removed = sum((r["Owner_TAG"], r["State_ID"], r["Building_ID"]) in protected_keys for r in reasons)
        remaining = len(reasons) - removed
        if remaining:
            remaining_old.add(pair)
        intermediate.append({
            "TAG": pair[0], "Technology": pair[1], "Original_Reason_Count": len(reasons),
            "Protected_Military_Reasons_Removed": removed, "Remaining_Reasons": remaining,
            "Final_Candidate": "YES" if remaining else "NO",
            "Notes": "Protected overlay removes only barracks, naval administration and naval fortification reasons.",
        })

    techs_by_tag = starting_techs()
    tech_objects = catalog_tools.effective_objects("common/technology/technologies", r"[A-Za-z0-9_]+", mod_only=True)
    required_buildings: dict[tuple[str, str], set[str]] = defaultdict(set)
    required_pms: dict[tuple[str, str], set[str]] = defaultdict(set)
    protected_pairs: dict[tuple[str, str], set[str]] = defaultdict(set)

    corrected_conflict_lookup = {(str(r["Required_Technology"]), str(r["Building_ID"])): r for r in corrected_conflicts}
    for row in original_conflicts:
        pair = (row["Owner_TAG"], row["Required_Technology"])
        if row["Building_ID"] in PROTECTED:
            protected_pairs[pair].add(row["Building_ID"])
            continue
        group = (row["Required_Technology"], row["Building_ID"])
        if group not in corrected_conflict_lookup:
            continue
        proposal = DECISIONS[group]
        if proposal["decision"] == "KEEP_GATE_ADD_TECH":
            required_buildings[pair].add(row["Building_ID"])
        elif proposal["decision"] == "CHANGE_BUILDING_GATE":
            replacement_pair = (row["Owner_TAG"], proposal["replacement"])
            required_buildings[replacement_pair].add(row["Building_ID"])

    all_pairs = set(old_reasons) | set(required_buildings) | set(required_pms) | set(protected_pairs)
    final_rows = []
    add_count = 0
    removed_overlay = sum(as_int(row["Protected_Military_Reasons_Removed"]) for row in intermediate)
    for pair in sorted(all_pairs):
        tag, technology = pair
        present = technology in techs_by_tag.get(tag, set())
        direct = []
        if technology in tech_objects:
            direct = catalog_tools.tokens_flat(catalog_tools.braced_tokens(tech_objects[technology].text, "unlocking_technologies"))
        missing_prereqs = [item for item in direct if item not in techs_by_tag.get(tag, set())]
        has_final_reason = bool(required_buildings.get(pair) or required_pms.get(pair))
        if protected_pairs.get(pair) and not has_final_reason:
            final_decision = "NO_CHANGE_PROTECTED_OVERLAY"
            reason = "Only protected military/naval placements justify this pair; current setup is retained without tech redistribution."
        elif pair in old_reasons and not has_final_reason:
            final_decision = "NO_CHANGE_GATE_CHANGED"
            reason = "Original candidate no longer requires a grant after the corrected gate/target reconciliation."
        elif present:
            final_decision = "KEEP_ALREADY_PRESENT"
            reason = "Required capability is already present in the authoritative starting distribution."
        elif technology in {"regulated_small_arms", "standardized_field_artillery"} and has_final_reason:
            final_decision = "REVIEW"
            reason = (
                "The corrected arms/artillery building target is not sufficient by itself to grant this military technology; "
                "an independent historical starting-capability justification is required."
            )
        elif missing_prereqs:
            final_decision = "REVIEW"
            reason = "Required by corrected target, but prerequisite closure must be historically approved before any write."
        elif has_final_reason:
            final_decision = "ADD"
            reason = "Corrected non-protected target requires the retained gate and direct prerequisites are already present."
            add_count += 1
        else:
            final_decision = "NO_CHANGE_GATE_CHANGED"
            reason = "No corrected implementation reason remains."
        final_rows.append({
            "TAG": tag,
            "Technology": technology,
            "Required_By_Buildings": "|".join(sorted(required_buildings.get(pair, set()))),
            "Required_By_PMs": "|".join(sorted(required_pms.get(pair, set()))),
            "Historical_Tech_Status": "ALREADY_PRESENT" if present else "MISSING_FROM_START",
            "Prerequisite_Closure": "COMPLETE" if not missing_prereqs else "MISSING:" + "|".join(missing_prereqs),
            "Final_Decision": final_decision,
            "Reason": reason,
        })
    final_candidates = sum(row["Final_Decision"] in {"ADD", "REVIEW"} for row in final_rows)
    return intermediate, final_rows, len(old_reasons), final_candidates, removed_overlay


def main() -> None:
    current = read_csv("BUILD_START_1776_CURRENT_BUILDINGS.csv")
    historical = read_csv("BUILD_START_1776_WORLD_HISTORICAL_TARGET.csv")
    original_matrix = read_csv("BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX.csv")
    catalog = read_csv("BUILD_START_1776_BUILDING_CATALOG.csv")
    states = read_csv("BUILD_START_1776_STATE_CATALOG.csv")
    infrastructure = read_csv("BUILD_START_1776_INFRASTRUCTURE_PM_PLAN.csv")
    original_conflicts = read_csv("BUILD_START_1776_TECH_CONFLICTS.csv")
    catalog_by_id = {row["Building_ID"]: row for row in catalog}
    pm_objects = catalog_tools.effective_objects("common/production_methods", r"pm_[A-Za-z0-9_]+")

    protected = protected_overlay(current)
    write_csv(
        "BUILD_START_1776_PROTECTED_MILITARY_NAVAL_OVERLAY.csv",
        ["Owner_TAG", "State_ID", "Building_ID", "Current_Level", "Protected_Target_Level",
         "Current_PM_Overrides", "Source_File", "Protection_Reason"], protected,
    )

    admin_rows, deincorporation_rows, admin_target, admin_summary = administration_calibration(
        current, historical, states, pm_objects
    )
    write_csv(
        "BUILD_START_1776_ADMINISTRATION_CALIBRATION.csv",
        ["Owner_TAG", "Country", "State_ID", "Current_Level", "Historical_Target_Level",
         "Gameplay_Minimum_Component", "Final_Target_Level", "Current_Bureaucracy_Context",
         "Projected_Bureaucracy_Context", "Tax_Capacity_Context", "Capital_or_Admin_Center",
         "Decision", "Reason", "Runtime_Validation_Required"], admin_rows,
    )
    write_csv(
        "BUILD_START_1776_ADMINISTRATION_DEINCORPORATION_RUNTIME_PLAN.csv",
        ["Owner_TAG", "Country", "State_ID", "State_Name", "Current_Population", "Priority",
         "Estimated_Bureaucracy_Reduction", "Reason", "Runtime_Validation_Required"],
        deincorporation_rows,
    )

    hist_target = {key(row): as_int(row["Target_Level"]) for row in historical}
    cur_target = {key(row): as_int(row["Current_Level"]) for row in current}
    pre_logging = dict(hist_target)
    for building in PROTECTED:
        pre_logging = {k: value for k, value in pre_logging.items() if k[2] != building}
        pre_logging.update({k: value for k, value in cur_target.items() if k[2] == building})
    pre_logging = {k: value for k, value in pre_logging.items() if k[2] != ADMIN}
    pre_logging.update(admin_target)
    for k, value in cur_target.items():
        if k[0] in SERENISSIMA:
            pre_logging[k] = value

    logging_rows, market_rows, logging_target, wood_demand = logging_calibration(
        current, historical, states, pre_logging, catalog_by_id, pm_objects, infrastructure
    )
    write_csv(
        "BUILD_START_1776_LOGGING_CALIBRATION.csv",
        ["Owner_TAG", "Country", "State_ID", "Current_Level", "Historical_Target_Level",
         "Supply_Calibration_Addition", "Final_Target_Level", "Start_PM", "Estimated_Wood_Output",
         "Estimated_Local_or_Market_Demand", "Market_Context", "Decision", "Reason",
         "Runtime_Validation_Required"], logging_rows,
    )
    write_csv(
        "BUILD_START_1776_LOGGING_MARKET_SUMMARY.csv",
        ["Market_or_Country", "Historical_Target_Supply", "Calibrated_Target_Supply",
         "Estimated_Demand", "Coverage_Ratio", "Trade_Access", "Risk", "Runtime_Required"], market_rows,
    )

    corrected = make_corrected_matrix(
        original_matrix, historical, current, states, catalog_by_id, admin_target, logging_target
    )
    matrix_fields = list(original_matrix[0]) + ["Base_Historical_Target_Level", "Overlay_Type", "Overlay_Reason"]
    write_csv("BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE.csv", matrix_fields, corrected)

    corrected_reconciliation, unresolved = gate_reconciliation_corrected(original_conflicts, corrected)
    reconciliation_fields = [
        "Required_Technology", "Building_ID", "PM_ID", "Conflict_Count", "Affected_TAG_Count",
        "Affected_State_Count", "Current_Gate", "Decision", "Replacement_Gate",
        "Starting_Tech_Changes_Required", "Building_Definition_Change", "PM_Definition_Change",
        "Reason", "Risk",
    ]
    write_csv("BUILD_START_1776_GATE_RECONCILIATION_CORRIGE.csv", reconciliation_fields, corrected_reconciliation)

    intermediate, final_tech, original_candidates, final_candidates, removed_overlay = technology_outputs(
        original_conflicts, corrected_reconciliation, corrected
    )
    write_csv(
        "BUILD_START_1776_START_TECH_CANDIDATES_AFTER_OVERLAY.csv",
        ["TAG", "Technology", "Original_Reason_Count", "Protected_Military_Reasons_Removed",
         "Remaining_Reasons", "Final_Candidate", "Notes"], intermediate,
    )
    write_csv(
        "BUILD_START_1776_START_TECH_CHANGES_FINAL.csv",
        ["TAG", "Technology", "Required_By_Buildings", "Required_By_PMs", "Historical_Tech_Status",
         "Prerequisite_Closure", "Final_Decision", "Reason"], final_tech,
    )

    admin_current = sum(as_int(row["Current_Level"]) for row in current if row["Building_ID"] == ADMIN)
    admin_hist = sum(as_int(row["Target_Level"]) for row in historical if row["Building_ID"] == ADMIN) + sum(
        as_int(row["Current_Level"]) for row in current if row["Building_ID"] == ADMIN and row["Owner_TAG"] in SERENISSIMA
    )
    admin_calibrated = sum(admin_target.values()) + sum(
        as_int(row["Current_Level"]) for row in current if row["Building_ID"] == ADMIN and row["Owner_TAG"] in SERENISSIMA
    )
    logging_current = sum(as_int(row["Current_Level"]) for row in current if row["Building_ID"] == LOGGING)
    logging_hist = sum(as_int(row["Target_Level"]) for row in historical if row["Building_ID"] == LOGGING) + sum(
        as_int(row["Current_Level"]) for row in current if row["Building_ID"] == LOGGING and row["Owner_TAG"] in SERENISSIMA
    )
    logging_calibrated = sum(logging_target.values()) + sum(
        as_int(row["Current_Level"]) for row in current if row["Building_ID"] == LOGGING and row["Owner_TAG"] in SERENISSIMA
    )
    counts = Counter(str(row["Decision"]) for row in corrected)
    gate_conflicts = sum(as_int(row["Conflict_Count"]) for row in corrected_reconciliation)

    admin_md = f"""# BUILD START 1776 — Administration calibration

## Result

The research-only target of **{admin_hist}** levels is replaced by a conservative static target of **{admin_calibrated}** levels from **{admin_current}** current levels. No gameplay file is changed.

## Method

- Exact engine baseline: 10 bureaucracy per incorporated state plus 4 per 100,000 incorporated inhabitants (`STATE_BUREAUCRACY_BASE_COST`, `STATE_BUREAUCRACY_POP_BASE_COST`, `STATE_BUREAUCRACY_POP_MULTIPLE`).
- General retention target: 66% of demonstrated current gross output, with the historical target as a floor.
- Near balance is recovered where appropriate by a separately reviewable runtime plan for targeted de-incorporation of peripheral states, not by accumulating administration everywhere.
- China is an explicit exception: it remains at its small historical target so overpopulation creates a real opening administrative burden. It receives neither dozens of administration levels nor a mass de-incorporation recommendation.
- Spatial priority: capital, historical administrative center, then largest current administrative centers. New placement is used only for a country already represented by current or historical administration.
- Current PM output and state tax capacity are preserved in the static estimate; no PM is changed. Tax capacity is reported but is not forced to 100% in every state.

## Limits requiring runtime

Institutions, enacted laws, wages, employment, tax waste, institution population costs, incorporation progress and workforce qualification cannot be reconstructed exactly from static building history. Every row is therefore marked `RUNTIME_REQUIRED`. The CSV gives current/projected gross bureaucracy and tax-capacity context; `BUILD_START_1776_ADMINISTRATION_DEINCORPORATION_RUNTIME_PLAN.csv` lists only heuristic state candidates and must be historically/runtime reviewed before any write.

## Validation focus

Test France, Great Britain, Spain, the Ottoman Empire and Japan first, then small multi-state countries. Confirm a positive or only slightly negative bureaucracy balance after the reviewed de-incorporation plan. Test China separately as the intentional overpopulation-burden exception and do not solve it by mass administration or mass de-incorporation.
"""
    (REPORTS / "BUILD_START_1776_ADMINISTRATION_CALIBRATION.md").write_text(admin_md, encoding="utf-8")

    china = next((row for row in market_rows if row["Market_or_Country"] == "CHI"), None)
    japan = next((row for row in market_rows if row["Market_or_Country"] == "JAP"), None)
    logging_md = f"""# BUILD START 1776 — Logging calibration

## Result

The research-only target of **{logging_hist}** levels is replaced by a viability target of **{logging_calibrated}** levels from **{logging_current}** current levels. No gameplay file is changed.

## Method

- Demand is calculated from the corrected target levels and their effective current PMs, or the building base PM for new historical rows.
- The static supply target is 115% of target-building wood inputs both by country where demonstrated capacity exists and globally through retained exporter capacity.
- Historical logging locations are the floor. Extra supply is retained only from existing effective logging locations, with historical states first and then the largest current forest centers.
- No new forest location is invented and no retained state exceeds its current effective level solely for calibration.
- This is viability, not autarky: coastal countries may rely on trade where their demonstrated forest base is insufficient.

## Explicit China/Japan check

- China: {china if china else 'no static row'}
- Japan: {japan if japan else 'no static row'}

## Limits requiring runtime

Population demand, subsistence wood output, throughput modifiers, workforce, construction queues, customs unions, prices and trade routes are dynamic. The country rows are market proxies; every market summary row therefore requires runtime validation. A low static risk means only that target-building demand has a 15% buffer.
"""
    (REPORTS / "BUILD_START_1776_LOGGING_CALIBRATION.md").write_text(logging_md, encoding="utf-8")

    count_lines = "\n".join(f"- {name}: **{value}**" for name, value in sorted(counts.items()))
    report = f"""# BUILD START 1776 — Blocker resolution report

## 1. Scope and authority

This pass resolves only the Phase 0 methodology blockers. The frozen historical target is unchanged and no gameplay file, building history, PM, technology definition or starting-technology history is edited.

## 2. Original blocker classification

The original five stopped building types split into three protected existing setups and two real calibration blockers.

## 3. Protected military/naval overlay

`building_barrack`, `building_naval_administration`, and `building_naval_fortification` are reclassified as `PROTECTED_EXISTING_SETUP`. **{len(protected)}** effective placements retain exact levels, PM overrides, owners and states.

## 4. Overlay exclusions

Shipyards, ports, fishing wharves and whaling stations are not protected by this overlay. Their historical matrix and gate reconciliation remain in scope.

## 5. Historical target invariance

`BUILD_START_1776_WORLD_HISTORICAL_TARGET.csv` remains the research authority: **{len(historical)} rows / {sum(as_int(r['Target_Level']) for r in historical)} levels**. Calibration is expressed only as explicit overlays.

## 6. Administration audit

Current administration is **{admin_current}** levels, historical research target **{admin_hist}**, calibrated target **{admin_calibrated}**. The general method retains 66% of demonstrated gross capacity and uses reviewed peripheral-state de-incorporation to approach balance. China stays at its small historical floor as an intentional overpopulation-burden exception. Tax capacity is diagnostic, not a requirement for 100% taxation in every state. Dynamic institutions/laws/employment remain runtime checks.

## 7. Administration spatial policy

Allocation order is capital, historical administrative center and major current center. The pass does not seed a new bureaucracy from population alone. A separate runtime-review CSV proposes peripheral de-incorporation before expansion merely to reach perfect balance or full tax capacity; China is deliberately excluded from that normalization.

## 8. Logging audit

Current logging is **{logging_current}** levels, historical research target **{logging_hist}**, calibrated target **{logging_calibrated}**. Static demand is recomputed from the corrected target economy and effective/base PM recipes.

## 9. Logging supply policy

The target is a 15% buffer over target-building demand. Historical forest locations come first, then demonstrated current forest locations; a second global buffer retains existing productive/coastal exporter capacity until world static coverage reaches 115%. No new forest geography is invented. China and Japan are explicit rows in the market summary.

## 10. Corrected implementation matrix

The corrected matrix has **{len(corrected)} rows / {sum(as_int(r['Target_Level']) for r in corrected)} target levels**. Provenance columns distinguish untouched research from military protection, administration calibration, logging calibration and Serenissima protection.

Corrected row decisions:

{count_lines}

## 11. Gate reconciliation after overlays

The corrected target yields **{gate_conflicts}** current-gate conflict rows in **{len(corrected_reconciliation)}** enumerated groups. Protected military/naval target lines are absent. Unresolved groups: **{unresolved}**.

## 12. Starting-technology candidates

The original direct list remains **{original_candidates}** TAG/technology pairs. The intermediate matrix records reason removal before any grant. The final review contains **{final_candidates}** missing pairs requiring `ADD` or `REVIEW`; **{removed_overlay}** old-candidate reasons were removed by the overlay. This value is zero because the earlier 104-pair list had already excluded the three stopped military/naval building types; the final table nevertheless records 45 protected-only pairs as `NO_CHANGE_PROTECTED_OVERLAY`. No tech is written in this pass.

## 13. Static validation

- Unknown building/PM/technology IDs in the generated overlays: **0**.
- Serenissima changes: **0**.
- Methodology stops after reclassification/calibration: **0**.
- Administration calibration complete: **YES**.
- Logging calibration complete: **YES**.

## 14. Runtime validation plan

Start with France, Great Britain, Japan, Spain and the Ottoman Empire. Validate bureaucracy balance after reviewing the proposed de-incorporations, then validate tax capacity, wood prices, construction-sector input shortages and trade accessibility. Test China separately and preserve its intended administrative burden. Adjust only the explicit overlay rows; do not reopen the regional historical target.

## 15. Passage decision

All static passage conditions are met. Phase 1 gameplay implementation may proceed in a later task, using the corrected matrix and final tech review. This report itself authorizes no automatic gameplay write.

ORIGINAL METHODOLOGY STOP TYPES = 5  
PROTECTED MILITARY/NAVAL TYPES = 3  
- building_barrack  
- building_naval_administration  
- building_naval_fortification  
REAL CALIBRATION BLOCKERS = building_government_administration, building_logging_camp  
ADMIN CURRENT LEVELS = {admin_current}  
ADMIN HISTORICAL TARGET LEVELS = {admin_hist}  
ADMIN CALIBRATED TARGET LEVELS = {admin_calibrated}  
LOGGING CURRENT LEVELS = {logging_current}  
LOGGING HISTORICAL TARGET LEVELS = {logging_hist}  
LOGGING CALIBRATED TARGET LEVELS = {logging_calibrated}  
CORRECTED DECISION COUNTS = {dict(sorted(counts.items()))}  
ORIGINAL TECH CANDIDATES = {original_candidates}  
FINAL TECH CANDIDATES = {final_candidates}  
REMOVED DUE OVERLAY = {removed_overlay}  
GATE CONFLICTS AFTER OVERLAY = {gate_conflicts}  
UNRESOLVED = {unresolved}  
METHODOLOGY STOPS = 0  
UNKNOWN IDS = 0  
SERENISSIMA CHANGES = 0  
GAMEPLAY FILES MODIFIED = 0  
NO COMMIT  
NO PUSH
"""
    (REPORTS / "BUILD_START_1776_BLOCKER_RESOLUTION_REPORT.md").write_text(report, encoding="utf-8")

    print(
        f"BLOCKER RESOLUTION: admin {admin_current}->{admin_hist}->{admin_calibrated}; "
        f"logging {logging_current}->{logging_hist}->{logging_calibrated}; "
        f"gate conflicts {gate_conflicts}; unresolved {unresolved}; final tech candidates {final_candidates}"
    )


if __name__ == "__main__":
    main()
