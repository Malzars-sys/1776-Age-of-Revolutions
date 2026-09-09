"""Static validation for TECH6C5B copper implementation."""

from __future__ import annotations

import csv
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def fail(message: str) -> None:
    ERRORS.append(message)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def brace_end(text: str, opening: int) -> int:
    depth = 0
    for pos in range(opening, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return pos + 1
    raise ValueError("unbalanced braces")


def blocks(text: str, pattern: str) -> list[tuple[str, str]]:
    result = []
    for match in re.finditer(pattern, text, re.M):
        opening = text.find("{", match.start())
        result.append((match.group(1), text[match.start() : brace_end(text, opening)]))
    return result


def definition_count(folder: str, object_id: str) -> int:
    pattern = re.compile(rf"(?m)^{re.escape(object_id)}\s*=\s*\{{")
    return sum(len(pattern.findall(read(path))) for path in (ROOT / folder).glob("*.txt"))


def check_braces() -> None:
    changed = subprocess.run(
        ["git", "diff", "--name-only", "--", "common", "map_data/state_regions"],
        cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "--", "common", "map_data/state_regions"],
        cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.splitlines()
    for rel in sorted(set(changed + untracked)):
        path = ROOT / rel
        if path.suffix == ".txt":
            text = read(path)
            if text.count("{") != text.count("}"):
                fail(f"Unbalanced braces: {rel}")


def check_objects() -> None:
    expected = {
        ("common/goods", "copper"): 1,
        ("common/buildings", "building_copper_mine"): 1,
        ("common/production_method_groups", "pmg_mining_equipment_building_copper_mine"): 1,
        ("common/production_method_groups", "pmg_explosives_building_copper_mine"): 1,
        ("common/production_method_groups", "pmg_steam_automation_building_copper_mine"): 1,
        ("common/production_method_groups", "pmg_train_automation_building_copper_mine"): 1,
        ("common/production_method_groups", "pmg_ore_concentration_building_copper_mine"): 1,
        ("common/production_method_groups", "pmg_copper_sheathing_building_shipyard"): 1,
    }
    pm_ids = [
        "pm_picks_and_shovels_building_copper_mine",
        "pm_atmospheric_engine_pump_building_copper_mine",
        "pm_condensing_engine_pump_building_copper_mine",
        "pm_diesel_pump_building_copper_mine",
        "pm_nitroglycerin_building_copper_mine",
        "pm_dynamite_building_copper_mine",
        "pm_no_ore_concentration_building_copper_mine",
        "pm_ore_concentration_building_copper_mine",
        "pm_no_copper_sheathing_building_shipyard",
        "pm_copper_sheathing_building_shipyard",
    ]
    expected.update({("common/production_methods", object_id): 1 for object_id in pm_ids})
    for (folder, object_id), count in expected.items():
        actual = definition_count(folder, object_id)
        if actual != count:
            fail(f"{object_id}: expected {count} definition, found {actual}")

    support = read(ROOT / "common/modifier_type_definitions/12_tech6c_custom_goods_modifier_types.txt")
    for modifier in ("goods_input_copper_add", "goods_input_copper_mult", "goods_output_copper_add", "goods_output_copper_mult"):
        if len(re.findall(rf"(?m)^{modifier}\s*=", support)) != 1:
            fail(f"Modifier registration missing or duplicated: {modifier}")

    texticon = read(ROOT / "gui/tech6c_goods_texticons.gui")
    if len(re.findall(r"(?m)^\s*icon\s*=\s*copper\s*$", texticon)) != 1:
        fail("Copper texticon missing or duplicated")

    all_common = "\n".join(read(path) for path in (ROOT / "common").rglob("*.txt"))
    malformed_patterns = {
        "ggoods_": r"\bggoods_",
        "orphan oods_": r"(?<!g)\boods_",
        "goods_copper_add": r"\bgoods_copper_add\b",
    }
    for label, pattern in malformed_patterns.items():
        if re.search(pattern, all_common):
            fail(f"Malformed modifier token present: {label}")

    copper_file = read(ROOT / "common/goods/13_tech6c5b_copper.txt")
    for required in ("cost = 50", "category = industrial", "tradeable = yes", 'texture = "gfx/error_deer.dds"'):
        if required not in copper_file:
            fail(f"Copper good missing: {required}")

    copper_building = read(ROOT / "common/buildings/13_tech6c5b_copper_mine.txt")
    for required in (
        "building_group = bg_mining", "city_type = mine", "required_construction = construction_cost_medium",
        "terrain_manipulator = mining", "ownership_type = self", "ai_value = 1000", "shaft_mining",
    ):
        if required not in copper_building:
            fail(f"Copper mine architecture missing: {required}")

    copper_pms = read(ROOT / "common/production_methods/13_tech6c5b_copper_production_and_consumers.txt")
    for pm_id, block in blocks(copper_pms, r"(?m)^([a-zA-Z0-9_]+)\s*=\s*\{"):
        if 'texture = "gfx/error_deer.dds"' not in block:
            fail(f"New PM does not use error_deer: {pm_id}")

    # Every input/output good used by the changed PM files must exist in local or canonical goods.
    goods = set()
    for goods_root in (ROOT / "common/goods", Path(r"C:/Games/Victoria 3/game/common/goods")):
        for path in goods_root.glob("*.txt"):
            goods.update(name for name, _ in blocks(read(path), r"(?m)^([a-zA-Z0-9_]+)\s*=\s*\{"))
    for rel in (
        "common/production_methods/01_industry.txt",
        "common/production_methods/06_urban_center.txt",
        "common/production_methods/13_tech6c5b_copper_production_and_consumers.txt",
    ):
        for good in re.findall(r"goods_(?:input|output)_([a-zA-Z0-9_]+)_(?:add|mult)", read(ROOT / rel)):
            if good not in goods:
                fail(f"Unknown good {good} used in {rel}")


def check_pmg_resolution() -> None:
    pms = set()
    for path in (ROOT / "common/production_methods").glob("*.txt"):
        pms.update(name for name, _ in blocks(read(path), r"(?m)^([a-zA-Z0-9_\-]+)\s*=\s*\{"))
    target = read(ROOT / "common/production_method_groups/13_tech6c5b_copper_pmgs.txt")
    refs = re.findall(r"(?m)^\s+(pm_[a-zA-Z0-9_]+)\s*$", target)
    for ref in refs:
        if ref not in pms:
            fail(f"Unresolved production method in copper PMG: {ref}")


def check_consumers() -> None:
    industry = read(ROOT / "common/production_methods/01_industry.txt")
    urban = read(ROOT / "common/production_methods/06_urban_center.txt")
    copper_pms = read(ROOT / "common/production_methods/13_tech6c5b_copper_production_and_consumers.txt")
    checks = [
        (industry, r"pm_telephones\s*=.*?goods_input_copper_add\s*=\s*15", "telephone copper input"),
        (industry, r"pm_telephones\s*=.*?goods_output_telephones_add\s*=\s*60", "telephone output"),
        (industry, r"pm_electric_engines\s*=.*?goods_input_copper_add\s*=\s*10", "electric-engine copper input"),
        (industry, r"pm_radios\s*=.*?goods_input_copper_add\s*=\s*2", "radio copper input"),
        (copper_pms, r"pm_copper_sheathing_building_shipyard\s*=.*?goods_input_copper_add\s*=\s*5.*?goods_output_clippers_add\s*=\s*5", "copper sheathing recipe"),
        (copper_pms, r"pm_ore_concentration_building_copper_mine\s*=.*?geological_surveying", "concentration technology gate"),
        (copper_pms, r"pm_diesel_pump_building_copper_mine\s*=.*?goods_input_refined_fuels_add\s*=\s*3", "diesel refined-fuels input"),
    ]
    for text, pattern, label in checks:
        if not re.search(pattern, text, re.S):
            fail(f"Consumer or PM invariant failed: {label}")

    early_has_copper = bool(re.search(r"pm_early_power_plant\s*=.*?goods_input_copper_add\s*=\s*2", urban, re.S))
    aluminium_integration = ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt"
    conductor_has_copper = False
    if aluminium_integration.exists():
        conductor_has_copper = bool(re.search(
            r"pm_copper_conductors_building_power_plant\s*=.*?goods_input_copper_add\s*=\s*2",
            read(aluminium_integration), re.S,
        ))
    if early_has_copper == conductor_has_copper:
        fail("Power-plant copper baseline must exist exactly once, embedded or in the TECH6C5C conductor PMG")
    telephone = dict(blocks(industry, r"(?m)^(pm_telephones)\s*=\s*\{"))["pm_telephones"]
    if "goods_input_lead_add" in telephone:
        fail("Telephone PM still consumes lead")


def check_map() -> tuple[int, int, int, Counter[str], int]:
    matrix_path = ROOT / "docs/reports/industry/TECH6C5B_COPPER_GLOBAL_RESOURCE_MATRIX.csv"
    with matrix_path.open(encoding="utf-8-sig", newline="") as stream:
        rows = list(csv.DictReader(stream))
    ids = [row["state_id"] for row in rows]
    if len(rows) != 675 or len(set(ids)) != 675:
        fail(f"Matrix cardinality: {len(rows)} rows / {len(set(ids))} unique")
    expected = {row["state_id"]: int(row["potential"]) for row in rows}
    actual: dict[str, int] = {}
    files_with_copper = set()
    duplicates = 0
    for path in sorted((ROOT / "map_data/state_regions").glob("*.txt")):
        for state_id, block in blocks(read(path), r"(?m)^(STATE_[A-Z0-9_]+)\s*=\s*\{"):
            values = [int(value) for value in re.findall(r"(?m)^\s*building_copper_mine\s*=\s*(\d+)\s*$", block)]
            if len(values) > 1:
                duplicates += len(values) - 1
            if values:
                actual[state_id] = values[0]
                files_with_copper.add(path)
    if duplicates:
        fail(f"Duplicate copper capped-resource entries: {duplicates}")
    mismatches = [state_id for state_id, value in expected.items() if value != actual.get(state_id, 0)]
    if mismatches:
        fail(f"Matrix/map mismatches: {len(mismatches)}")
    extras = sorted(set(actual) - set(expected))
    if extras:
        fail(f"Map states absent from matrix: {extras}")

    diff = subprocess.run(
        ["git", "diff", "--unified=0", "--", "map_data/state_regions"],
        cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.splitlines()
    resource_changes = []
    for line in diff:
        if not line.startswith(("+", "-")) or line.startswith(("+++", "---")):
            continue
        if "building_copper_mine" not in line:
            resource_changes.append(line)
    if resource_changes:
        fail(f"Non-copper map lines changed: {len(resource_changes)}")

    counts = Counter(row["tier"] for row in rows)
    nonzero = sum(1 for value in expected.values() if value > 0)
    return nonzero, 675 - nonzero, sum(expected.values()), counts, len(files_with_copper)


def check_technology_graph() -> int:
    techs: dict[str, set[str]] = {}
    for path in (ROOT / "common/technology/technologies").glob("*.txt"):
        for tech_id, block in blocks(read(path), r"(?m)^([a-zA-Z0-9_]+)\s*=\s*\{"):
            match = re.search(r"unlocking_technologies\s*=\s*\{([^}]*)\}", block, re.S)
            parents = set(re.findall(r"\b[a-z][a-z0-9_]*\b", match.group(1))) if match else set()
            techs[tech_id] = parents
    if "ore_concentration" in techs:
        fail("A dedicated ore_concentration technology was created despite the zero-new-tech decision")
    expected_parents = {
        "geological_surveying": {"applied_mineralogy", "professional_civil_engineering"},
        "copper_sheathing": {"scientific_naval_architecture"},
    }
    for tech_id, parents in expected_parents.items():
        if techs.get(tech_id) != parents:
            fail(f"Unexpected topology for {tech_id}: {sorted(techs.get(tech_id, set()))}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            fail(f"Technology cycle detected at {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for parent in techs.get(node, set()):
            if parent in techs:
                visit(parent)
        visiting.remove(node)
        visited.add(node)

    for node in techs:
        visit(node)
    return len(techs)


def check_localization() -> None:
    for language, suffix in (("english", "l_english"), ("french", "l_french")):
        paths = list((ROOT / "localization" / language).glob("*.yml"))
        counts: Counter[str] = Counter()
        for path in paths:
            for key in re.findall(r"(?m)^\s+([A-Za-z0-9_\-.]+):\d+\s+", read(path)):
                counts[key] += 1
        new_keys = re.findall(
            r"(?m)^\s+([A-Za-z0-9_\-.]+):\d+\s+",
            read(ROOT / f"localization/{language}/tech6c5b_copper_{suffix}.yml"),
        )
        for key in new_keys:
            if counts[key] != 1:
                fail(f"Duplicate {language} localization key: {key} ({counts[key]})")
    for rel in (
        "localization/english/tech6c5b_copper_l_english.yml",
        "localization/french/tech6c5b_copper_l_french.yml",
        "localization/english/tech6c_goods_modifiers_l_english.yml",
        "localization/french/tech6c_goods_modifiers_l_french.yml",
    ):
        if not (ROOT / rel).read_bytes().startswith(b"\xef\xbb\xbf"):
            fail(f"Localization lacks UTF-8 BOM: {rel}")


def main() -> None:
    check_braces()
    check_objects()
    check_pmg_resolution()
    check_consumers()
    nonzero, zero, total, tiers, files = check_map()
    tech_count = check_technology_graph()
    check_localization()
    print(f"map: states=675 nonzero={nonzero} zero={zero} total={total} files={files}")
    print("tiers: " + ", ".join(f"{key}={tiers[key]}" for key in ("NONE", "LOW", "MODEST", "MEDIUM", "HIGH", "VERY_HIGH", "WORLD_CLASS")))
    print(f"technology_graph: nodes={tech_count} cycles=0 new_copper_techs=0")
    if ERRORS:
        print(f"FAIL ({len(ERRORS)} errors)")
        for error in ERRORS:
            print(f"- {error}")
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
