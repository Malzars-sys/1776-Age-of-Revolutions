#!/usr/bin/env python3
"""Targeted static validation for TECH TREE 1776 Wave 3."""

from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VANILLA = Path(r"C:\Games\Victoria 3\game")
REPORTS = ROOT / "docs/reports/technology"
sys.path.insert(0, str(ROOT / "tools"))

import tech_tree_1776_topology_audit as audit  # noqa: E402
import tech_tree_1776_wave3_polish as wave3  # noqa: E402


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    errors: list[str] = []
    techs = audit.effective_objects("common/technology/technologies")
    graph = {tech: audit.ids_in_field(block, "unlocking_technologies") for tech, block in techs.items()}
    eras = {tech: audit.era_number(audit.scalar(block, "era", "era_0")) for tech, block in techs.items()}
    active = {tech for tech, block in techs.items() if audit.scalar(block, "can_research", "yes") != "no"}
    _unlocks, effects = wave3.collect_unlocks(techs)
    pm_rows, pm_violations = wave3.pm_causality_rows(graph, eras)
    metrics = audit.graph_metrics(graph, eras, active, effects, pm_violations)

    expected = {
        "nodes": 244,
        "roots": 19,
        "isolated_nodes": 0,
        "leaf_no_effect": 0,
        "edges_total": 340,
        "graph_cycles": 0,
        "unknown_parent_ids": 0,
        "negative_era_edges": 0,
        "cross_era_gt3": 44,
        "building_pm_causality_violations": 0,
    }
    for key, value in expected.items():
        require(metrics[key] == value, f"metric {key}: expected {value}, got {metrics[key]}", errors)

    for alias in wave3.ALIASES:
        require(alias not in active, f"alias still researchable: {alias}", errors)
        require(not graph[alias], f"alias still has parents: {alias}", errors)

    expected_tech_parents = {
        "baking_powder": {"industrial_alkalis", "sugar_refining"},
        "camera": {"experimental_research_laboratories", "romanticism"},
        "chemical_bleaching": {"industrial_alkalis", "industrial_ceramics"},
        "rubber_mastication": {"fractional_distillation"},
        "steam_turbine": {"rotary_valve_engine", "electrical_generation"},
        "applied_mineralogy": set(),
        "atmospheric_engine": {"shaft_mining"},
    }
    for tech, parents in expected_tech_parents.items():
        require(graph[tech] == parents, f"unexpected parents for {tech}: {sorted(graph[tech])}", errors)
    require(eras["chemical_bleaching"] == 5, "chemical_bleaching is not era_5", errors)

    pms = audit.effective_objects("common/production_methods", "pm_")
    expected_pm_gates = {
        "pm_brine_electrolysis": {"electrical_capacitors", "nitroglycerin"},
        "pm_assembly_lines_building_automotive_industry": {"conveyors", "combustion_engine"},
        "pm_aeroplane_production": {"military_aviation", "combustion_engine"},
        "pm_all_metal_aircraft": {"military_aviation", "bayer_process", "combustion_engine"},
        "pm_atmospheric_engine_pump_building_gold_mine": {"atmospheric_engine", "applied_mineralogy"},
        "pm_condensing_engine_pump_building_gold_mine": {"condensing_steam_engines", "applied_mineralogy"},
        "pm_combustion_derricks": {"combustion_engine", "pumpjacks"},
        "pm_rail_transport_building_oil_rig": {"railways", "pumpjacks"},
        "pm_tanker_cars": {"steel_railway_cars", "pumpjacks"},
        "pm_coal-fired_plant": {"steam_turbine", "electrical_generation"},
        "pm_atmospheric_engine_pump_building_phosphate_mine": {"atmospheric_engine", "applied_mineralogy"},
        "pm_condensing_engine_pump_building_phosphate_mine": {"condensing_steam_engines", "applied_mineralogy"},
        "pm_scientific_management_automotive_industry": {"corporate_management", "combustion_engine"},
        "pm_scientific_management_electrics_industry": {"corporate_management", "telephone"},
        "pm_steam_rail_transport_building_rubber_plantation": {"railways", "rubber_mastication"},
    }
    for pm, gates in expected_pm_gates.items():
        require(pm in pms, f"missing PM: {pm}", errors)
        if pm in pms:
            require(audit.ids_in_field(pms[pm], "unlocking_technologies") == gates, f"unexpected gates for {pm}", errors)

    buildings = audit.effective_objects("common/buildings", "building_")
    require(audit.ids_in_field(buildings["building_artillery_foundry"], "unlocking_technologies") == {"standardized_field_artillery"}, "artillery foundry gate is wrong", errors)
    require(not audit.ids_in_field(buildings["building_cotton_plantation"], "unlocking_technologies"), "cotton plantation still has a building gate", errors)
    require("pmg_scientific_management_automotive_industry" in audit.ids_in_field(buildings["building_automotive_industry"], "production_method_groups"), "automotive scientific-management PMG missing", errors)
    require("pmg_scientific_management_electrics_industry" in audit.ids_in_field(buildings["building_electrics_industry"], "production_method_groups"), "electrics scientific-management PMG missing", errors)

    native_text = "\n".join(path.read_text(encoding="utf-8-sig", errors="ignore") for path in (VANILLA / "common/modifier_type_definitions").glob("*.txt"))
    for modifier in (
        "building_group_bg_logging_throughput_add",
        "state_tax_capacity_add",
        "building_port_throughput_add",
        "country_influence_add",
    ):
        require(f"{modifier}=" in native_text or f"{modifier} =" in native_text, f"native modifier not found: {modifier}", errors)

    parent_rows = rows(REPORTS / "TECH_TREE_1776_PARENT_REVIEW.csv")
    era_rows = rows(REPORTS / "TECH_TREE_1776_ERA_REVIEW.csv")
    long_rows = rows(REPORTS / "TECH_TREE_1776_LONG_EDGE_REVIEW.csv")
    report_pm_rows = rows(REPORTS / "TECH_TREE_1776_BUILDING_PM_CAUSALITY_WAVE3.csv")
    require(len(parent_rows) == 247, f"parent review row count: {len(parent_rows)}", errors)
    require(len(era_rows) == 247, f"era review row count: {len(era_rows)}", errors)
    require(len(long_rows) == 46, f"long-edge review row count: {len(long_rows)}", errors)
    require(len(report_pm_rows) == len(pm_rows) == 704, f"PM report row count: {len(report_pm_rows)}", errors)
    require(not any(row["Violation"] == "YES" for row in report_pm_rows), "PM report contains a violation", errors)

    for loc in (
        ROOT / "localization/english/tech3a_technology_l_english.yml",
        ROOT / "localization/french/tech3a_technology_l_french.yml",
        ROOT / "localization/english/tech6d_wave_d_l_english.yml",
        ROOT / "localization/french/tech6d_wave_d_l_french.yml",
    ):
        require(loc.read_bytes().startswith(b"\xef\xbb\xbf"), f"localization file lacks UTF-8 BOM: {loc}", errors)

    if errors:
        print("WAVE3 STATIC VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)
    print("WAVE3 STATIC VALIDATION: PASS")
    print(f"researchable={metrics['nodes']} roots={metrics['roots']} edges={metrics['edges_total']} long={metrics['cross_era_gt3']}")
    print(f"cycles={metrics['graph_cycles']} unknown={metrics['unknown_parent_ids']} negative={metrics['negative_era_edges']} isolated={metrics['isolated_nodes']} leaves={metrics['leaf_no_effect']} pm_violations={pm_violations}")


if __name__ == "__main__":
    main()
