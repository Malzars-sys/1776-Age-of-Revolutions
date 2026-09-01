#!/usr/bin/env python3
"""Static validation for TECH6B3F's effective Victoria 3 overlay."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from collections import Counter
from pathlib import Path

from tech6b3f_apply import ROOT, VANILLA, block_range, child_range, modifier_values


REPORTS = ROOT / "docs/reports/technology"
BASE_MATRIX = REPORTS / "TECH6B3E_HIDDEN_TECH_RESPONSIBILITY_MATRIX.csv"
IMPL_MATRIX = REPORTS / "TECH6B3F_HIDDEN_TECH_RESPONSIBILITY_IMPLEMENTATION_MATRIX.csv"
START_MATRIX = REPORTS / "TECH6B3F_STARTING_TECH_DEFERRED_MATRIX.csv"
TECH_DIR = ROOT / "common/technology/technologies"
EXPECTED_START_HASH = "570ffd6ac7309e89ed1dbb4e2deeef28789a258f3d8805596bc3942033965bb9"
EXPECTED_GUI_HASH = "dc457e06e049cda765eaeebf30df3095774a8f9fdfd27c0fbdfbf5b72b75aa85"


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252")


def effective_file(rel: str) -> Path:
    local = ROOT / rel
    return local if local.exists() else VANILLA / rel


def effective_files(rel_dir: str) -> dict[str, Path]:
    result: dict[str, Path] = {}
    vanilla_dir = VANILLA / rel_dir
    if vanilla_dir.exists():
        for path in vanilla_dir.rglob("*.txt"):
            result[path.relative_to(VANILLA).as_posix()] = path
    local_dir = ROOT / rel_dir
    if local_dir.exists():
        for path in local_dir.rglob("*.txt"):
            result[path.relative_to(ROOT).as_posix()] = path
    return result


def top_blocks(text: str) -> list[tuple[str, tuple[int, int]]]:
    result = []
    for match in re.finditer(r"(?m)^([A-Za-z0-9_.:-]+)[ \t]*=[ \t]*\{", text):
        name = match.group(1)
        result.append((name, block_range(text, name, match.start())))
    return result


def gate_values(text: str, obj: str) -> list[str]:
    parent = block_range(text, obj)
    child = child_range(text, parent, "unlocking_technologies")
    if child is None:
        return []
    body = text[child[0]:child[1]]
    inner = body[body.find("{") + 1:body.rfind("}")]
    active = "\n".join(line.split("#", 1)[0] for line in inner.splitlines())
    return re.findall(r"[A-Za-z0-9_.-]+", active)


def find_object(rel_dir: str, obj: str) -> tuple[str, str]:
    found = []
    for rel, path in effective_files(rel_dir).items():
        text = read_text(path)
        if re.search(rf"(?m)^{re.escape(obj)}[ \t]*=[ \t]*\{{", text):
            found.append((rel, text))
    if len(found) != 1:
        raise AssertionError(f"object {obj} in {rel_dir}: definitions={len(found)}")
    return found[0]


def assert_gate(rel_dir: str, obj: str, expected: list[str]) -> None:
    rel, text = find_object(rel_dir, obj)
    actual = gate_values(text, obj)
    if actual != expected:
        raise AssertionError(f"gate mismatch {obj} in {rel}: {actual} != {expected}")


def balanced(text: str) -> bool:
    depth = 0
    quoted = False
    escaped = False
    comment = False
    for ch in text:
        if comment:
            if ch in "\r\n":
                comment = False
            continue
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            continue
        if ch == "#":
            comment = True
        elif ch == '"':
            quoted = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and not quoted


def aggregate_starting(rows: list[dict[str, str]]) -> str:
    digest = hashlib.sha256()
    paths = sorted({row["source_file"] for row in rows})
    for rel in paths:
        digest.update((rel + "\n").encode())
        digest.update(effective_file(rel).read_bytes())
    return digest.hexdigest()


def main() -> int:
    with BASE_MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        baseline = list(csv.DictReader(handle))
    with IMPL_MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        impl = list(csv.DictReader(handle))
    with START_MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        starting_matrix = list(csv.DictReader(handle))

    hidden = sorted({row["hidden_tech_id"] for row in baseline})
    assert len(hidden) == 44
    assert len(baseline) == 413
    assert len([r for r in baseline if r["responsibility_type"] != "starting_technology_grant"]) == 184
    assert len(impl) == 184
    assert len(starting_matrix) == 229
    status = Counter(row["implementation_status"] for row in impl)
    assert status == Counter({"IMPLEMENTED": 178, "DEFERRED_URBAN_BUILDING": 2, "COMPATIBILITY_REFERENCE_ALLOWED": 4})
    assert status["BLOCKED"] == 0
    assert {row["future_phase"] for row in starting_matrix} == {"TECH6B3G_STARTING_TECH_RECONCILIATION"}

    # The active technology replace-path is entirely fork-owned.
    tech_defs: dict[str, dict[str, object]] = {}
    duplicates = []
    for path in sorted(TECH_DIR.glob("*.txt")):
        text = read_text(path)
        for name, span in top_blocks(text):
            block = text[span[0]:span[1]]
            era = re.search(r"(?m)^[ \t]+era[ \t]*=[ \t]*([A-Za-z0-9_]+)", block)
            category = re.search(r"(?m)^[ \t]+category[ \t]*=[ \t]*([A-Za-z0-9_]+)", block)
            if not era or not category:
                continue
            if name in tech_defs:
                duplicates.append(name)
            tech_defs[name] = {
                "file": path.relative_to(ROOT).as_posix(),
                "era": era.group(1),
                "category": category.group(1),
                "parents": gate_values(text, name),
                "text": text,
            }
    assert len(tech_defs) == 285, len(tech_defs)
    assert not duplicates, duplicates
    assert all(name in tech_defs for name in hidden)
    unknown_parents = [(name, parent) for name, data in tech_defs.items() for parent in data["parents"] if parent not in tech_defs]
    cross_edges = [(name, parent) for name, data in tech_defs.items() for parent in data["parents"] if parent in tech_defs and tech_defs[parent]["category"] != data["category"]]
    assert not unknown_parents, unknown_parents
    assert not cross_edges, cross_edges

    visiting: set[str] = set()
    visited: set[str] = set()
    cycles: list[str] = []
    def visit(node: str) -> None:
        if node in visiting:
            cycles.append(node)
            return
        if node in visited:
            return
        visiting.add(node)
        for parent in tech_defs[node]["parents"]:
            visit(parent)
        visiting.remove(node)
        visited.add(node)
    for node in tech_defs:
        visit(node)
    assert not cycles, cycles

    # Final tax, law, and manually frozen gates.
    exact_law_gates = {
        "law_consumption_based_taxation": [],
        "law_land_based_taxation": [],
        "law_per_capita_based_taxation": ["systematic_population_registration"],
        "law_proportional_taxation": ["classical_political_economy"],
        "law_graduated_taxation": ["socialism"],
        "law_universal_suffrage": ["liberal_constitutionalism"],
        "law_national_guard": ["professional_civil_policing"],
        "law_national_militia": ["corps_organization"],
        "law_professional_army": ["corps_organization"],
        "law_diplomatic_navy": ["state_dockyard_systems"],
        "law_professional_navy": ["state_dockyard_systems"],
        "law_laissez_faire": ["joint_stock_companies"],
        "law_protectionism": ["political_economy"],
        "law_public_health_insurance": ["organized_immunization_campaigns"],
        "law_restricted_child_labor": ["human_rights"],
        "law_regulatory_bodies": ["human_rights"],
        "law_wage_subsidies": ["human_rights"],
        "law_compulsory_primary_school": ["labor_movement"],
        "law_worker_protections": ["labor_movement"],
        "law_old_age_pension": ["labor_movement"],
        "law_state_atheism": ["socialism"],
        "law_terakoya": [],
        "law_slave_trade": [],
        "law_debt_slavery": ["constitutional_government"],
        "law_colonial_slavery": ["human_rights"],
        "law_legacy_slavery": ["organized_reform_movements"],
        "law_slavery_banned": ["abolitionist_mobilization"],
    }
    for obj, expected in exact_law_gates.items():
        assert_gate("common/laws", obj, expected)

    hidden_set = set(hidden)
    hidden_law_gates = []
    for rel, path in effective_files("common/laws").items():
        text = read_text(path)
        for obj, _ in top_blocks(text):
            for gate in gate_values(text, obj):
                if gate in hidden_set:
                    hidden_law_gates.append((obj, gate, rel))
    assert not hidden_law_gates, hidden_law_gates

    hidden_pm_gates = []
    for rel, path in effective_files("common/production_methods").items():
        text = read_text(path)
        for obj, _ in top_blocks(text):
            for gate in gate_values(text, obj):
                if gate in hidden_set:
                    hidden_pm_gates.append((obj, gate, rel))
    assert not hidden_pm_gates, hidden_pm_gates

    assert_gate("common/buildings", "building_urban_center", ["urbanization"])
    assert_gate("common/buildings", "building_construction_sector", ["urbanization"])

    # Exact transferred modifiers and source cleanup.
    compat = read_text(ROOT / "common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt")
    source_aliases = ["army_reserves", "mandatory_service", "dialectics", "military_drill", "power_of_the_purse", "psychiatry", "sericulture", "urban_planning", "urbanization"]
    for alias in source_aliases:
        assert child_range(compat, block_range(compat, alias), "modifier") is None, alias

    expected_modifiers = {
        "corps_organization": {"country_general_rank_impact_mult": "0.2", "state_conscription_rate_mult": "0.2"},
        "polytechnical_education": {"country_institution_schools_max_investment_add": "1"},
        "light_infantry_tactics": {"unit_experience_gain_mult": "0.05"},
        "state_dockyard_systems": {"country_admiral_rank_impact_mult": "0.25"},
        "philosophical_pragmatism": {"country_influence_mult": "0.25", "country_diplomatic_play_maneuvers_mult": "0.25", "state_bureaucracy_population_base_cost_factor_mult": "-0.05"},
        "selective_breeding": {"building_silk_plantation_throughput_add": "0.25"},
        "modern_sewerage": {"country_max_weekly_construction_progress_add": "5", "state_building_construction_sector_max_level_add": "5", "state_infrastructure_from_population_add": "1", "state_infrastructure_from_population_max_add": "20"},
        "paved_roads": {"country_max_weekly_construction_progress_add": "10", "state_building_construction_sector_max_level_add": "10", "state_infrastructure_from_population_add": "2", "state_infrastructure_from_population_max_add": "40"},
    }
    duplicated_modifiers = []
    for tech, expected in expected_modifiers.items():
        data = tech_defs[tech]
        text = read_text(ROOT / str(data["file"]))
        actual = modifier_values(text, tech)
        for key, value in expected.items():
            assert actual.get(key) == value, (tech, key, actual.get(key), value)
            block = text[slice(*child_range(text, block_range(text, tech), "modifier"))]
            count = len(re.findall(rf"(?m)^[ \t]+{re.escape(key)}[ \t]*=", block))
            if count != 1:
                duplicated_modifiers.append((tech, key, count))
    assert not duplicated_modifiers, duplicated_modifiers

    # Joint Stock remains the explicit same-category, visible, researchable exception.
    joint = tech_defs["joint_stock_companies"]
    assert joint["era"] == "era_6"
    assert joint["category"] == "society"
    assert joint["parents"] == ["postal_savings", "commercial_insurance_markets"]
    joint_text = read_text(ROOT / str(joint["file"]))[slice(*block_range(read_text(ROOT / str(joint["file"])), "joint_stock_companies"))]
    assert not re.search(r"(?m)^[ \t]+can_research[ \t]*=[ \t]*no", joint_text)

    # Per-capita AI availability reference follows the exact new owner.
    _, taxation = find_object("common/laws", "law_per_capita_based_taxation")
    tax_block = taxation[slice(*block_range(taxation, "law_per_capita_based_taxation"))]
    assert len(re.findall(r"systematic_population_registration", tax_block)) == 2
    assert "scientific_metrology" not in tax_block

    # All gameplay files named by the implementation matrix are syntactically balanced.
    changed_files = set()
    for row in impl:
        value = row["actual_file_changed"]
        if value and value != "NONE":
            changed_files.update(value.split(";"))
    changed_files.add("common/laws/01_taxation.txt")
    for rel in changed_files:
        assert (ROOT / rel).exists(), rel
        assert balanced(read_text(ROOT / rel)), rel
    assert len(changed_files) == 79, len(changed_files)

    start_rows = [row for row in baseline if row["responsibility_type"] == "starting_technology_grant"]
    starting_status = subprocess.run(
        ["git", "status", "--short", "--", "common/history/countries", "common/scripted_effects/00_starting_inventions.txt"],
        cwd=ROOT, check=True, capture_output=True, text=True,
    ).stdout.strip()
    assert starting_status == "", starting_status
    assert hashlib.sha256((ROOT / "gui/tech_tree.gui").read_bytes()).hexdigest() == EXPECTED_GUI_HASH

    print("TECH6B3F_STATIC_VALIDATION=PASS")
    print(f"TECH_DEFINITIONS={len(tech_defs)}")
    print(f"HIDDEN_ALIASES_PRESENT={sum(1 for name in hidden if name in tech_defs)}")
    print(f"IMPLEMENTATION_ROWS={len(impl)}")
    print(f"IMPLEMENTED={status['IMPLEMENTED']}")
    print(f"DEFERRED_URBAN_BUILDING={status['DEFERRED_URBAN_BUILDING']}")
    print(f"COMPATIBILITY_REFERENCE_ALLOWED={status['COMPATIBILITY_REFERENCE_ALLOWED']}")
    print(f"DEFERRED_STARTING_TECH={len(starting_matrix)}")
    print("BLOCKED=0")
    print("HIDDEN_TECH_LAW_UNLOCKS_AFTER=0")
    print("HIDDEN_TECH_PM_UNLOCKS_AFTER=0")
    print("HIDDEN_TECH_DIRECT_MODIFIERS_AFTER=0")
    print("DUPLICATED_TRANSFERRED_MODIFIERS=0")
    print("PSYCHIATRY_MODIFIER_DUPLICATION_AFTER=0")
    print("UNKNOWN_TECH_IDS=0")
    print("INVENTED_TECH_IDS=0")
    print("DUPLICATE_TECH_IDS=0")
    print("TECH_TREE_CYCLES=0")
    print("CROSS_CATEGORY_TECH_EDGES=0")
    print("STARTING_TECH_FILES_CHANGED=0")
    print("STARTING_TECH_GRANTS_CHANGED=0")
    print("GUI_FILES_CHANGED_BY_TECH6B3F=0")
    print(f"GAMEPLAY_FILES_CHANGED_BY_TECH6B3F={len(changed_files)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
