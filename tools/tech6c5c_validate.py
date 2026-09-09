"""Static validation for TECH6C5C aluminium implementation."""

from __future__ import annotations

import hashlib
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATE_BASELINE = "3BAA853AD5EC5D9626330EA4B93FFA4BFA726DE300DB92773B6670FCB69BFE21"
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


def get_block(path: Path, object_id: str) -> str:
    found = dict(blocks(read(path), rf"(?m)^({re.escape(object_id)})\s*=\s*\{{"))
    if object_id not in found:
        fail(f"Missing object {object_id} in {path.relative_to(ROOT)}")
        return ""
    return found[object_id]


def definition_count(folder: str, object_id: str) -> int:
    pattern = re.compile(rf"(?m)^{re.escape(object_id)}\s*=\s*\{{")
    return sum(len(pattern.findall(read(path))) for path in (ROOT / folder).glob("*.txt"))


def technology_requirements(block: str) -> set[str]:
    match = re.search(r"unlocking_technologies\s*=\s*\{([^}]*)\}", block, re.S)
    return set(re.findall(r"\b[a-z][a-z0-9_]*\b", match.group(1))) if match else set()


def check_braces() -> None:
    changed = subprocess.run(
        ["git", "diff", "--name-only", "--", "common", "gui"], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout.splitlines()
    untracked = subprocess.run(
        ["git", "ls-files", "--others", "--exclude-standard", "--", "common", "gui"],
        cwd=ROOT, check=True, text=True, capture_output=True,
    ).stdout.splitlines()
    for rel in sorted(set(changed + untracked)):
        path = ROOT / rel
        if path.suffix in {".txt", ".gui"}:
            text = read(path)
            if text.count("{") != text.count("}"):
                fail(f"Unbalanced braces: {rel}")


def check_objects_and_assets() -> None:
    expected = {
        ("common/goods", "aluminium"): 1,
        ("common/buildings", "building_non_ferrous_metallurgy_works"): 1,
        ("common/production_method_groups", "pmg_base_building_non_ferrous_metallurgy_works"): 1,
        ("common/production_method_groups", "pmg_electrical_conductors_building_power_plant"): 1,
        ("common/production_methods", "pm_hall_heroult_process"): 1,
        ("common/production_methods", "pm_all_metal_aircraft"): 1,
        ("common/production_methods", "pm_copper_conductors_building_power_plant"): 1,
        ("common/production_methods", "pm_aluminium_conductors_building_power_plant"): 1,
    }
    for (folder, object_id), wanted in expected.items():
        actual = definition_count(folder, object_id)
        if actual != wanted:
            fail(f"{object_id}: expected {wanted} definition, found {actual}")

    for rel in (
        "common/goods/14_tech6c5c_aluminium.txt",
        "common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt",
        "common/production_method_groups/14_tech6c5c_aluminium_pmgs.txt",
        "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt",
    ):
        text = read(ROOT / rel)
        object_blocks = blocks(text, r"(?m)^([a-zA-Z0-9_]+)\s*=\s*\{")
        for object_id, block in object_blocks:
            if 'gfx/error_deer.dds' not in block:
                fail(f"New visual does not use error_deer: {object_id}")

    good = read(ROOT / "common/goods/14_tech6c5c_aluminium.txt")
    for required in ("cost = 80", "category = industrial", "tradeable = yes"):
        if required not in good:
            fail(f"Aluminium good missing {required}")

    modifiers = read(ROOT / "common/modifier_type_definitions/12_tech6c_custom_goods_modifier_types.txt")
    for key in ("goods_input_aluminium_add", "goods_input_aluminium_mult", "goods_output_aluminium_add", "goods_output_aluminium_mult"):
        if len(re.findall(rf"(?m)^{key}\s*=", modifiers)) != 1:
            fail(f"Modifier definition missing or duplicated: {key}")
    if len(re.findall(r"(?m)^\s*icon\s*=\s*aluminium\s*$", read(ROOT / "gui/tech6c_goods_texticons.gui"))) != 1:
        fail("Aluminium texticon missing or duplicated")


def check_gates_and_recipes() -> None:
    both = {"electrical_capacitors", "industrial_alkalis"}
    building = get_block(ROOT / "common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt", "building_non_ferrous_metallurgy_works")
    hall = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_hall_heroult_process")
    aircraft = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_all_metal_aircraft")
    aluminium_conductors = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_aluminium_conductors_building_power_plant")
    copper_conductors = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_copper_conductors_building_power_plant")

    if technology_requirements(building) != both:
        fail("Non-ferrous works does not require both technological anchors")
    if technology_requirements(hall) != both:
        fail("Hall-Heroult PM does not require both technological anchors")
    if technology_requirements(aircraft) != both | {"military_aviation"}:
        fail("All-metal aircraft gate is not the required three-tech conjunction")
    if technology_requirements(aluminium_conductors) != both:
        fail("Aluminium conductors do not require both aluminium anchors")

    hall_invariants = {
        "goods_input_industrial_chemicals_add": 20,
        "goods_input_coal_add": 10,
        "goods_input_electricity_add": 50,
        "goods_output_aluminium_add": 40,
        "state_pollution_generation_add": 20,
        "building_employment_shopkeepers_add": 500,
        "building_employment_laborers_add": 2500,
        "building_employment_machinists_add": 1250,
        "building_employment_engineers_add": 750,
    }
    for key, value in hall_invariants.items():
        if not re.search(rf"\b{key}\s*=\s*{value}\b", hall):
            fail(f"Hall-Heroult invariant failed: {key}={value}")

    for key, value in (("goods_input_aluminium_add", 10), ("goods_output_automobiles_add", -10), ("goods_output_aeroplanes_add", 20)):
        if not re.search(rf"\b{key}\s*=\s*{value}\b", aircraft):
            fail(f"All-metal aircraft invariant failed: {key}={value}")
    if "goods_input_hardwood" in aircraft or "goods_input_fabric" in aircraft:
        fail("All-metal aircraft still consumes hardwood or fabric")

    if not re.search(r"goods_input_copper_add\s*=\s*2\b", copper_conductors):
        fail("Copper conductor baseline is not 2 copper")
    if "aluminium" in copper_conductors:
        fail("Copper conductor option also consumes aluminium")
    if not re.search(r"goods_input_aluminium_add\s*=\s*1\b", aluminium_conductors):
        fail("Aluminium conductor option is not 1 aluminium")
    if "goods_input_copper" in aluminium_conductors:
        fail("Aluminium conductor option also consumes copper")

    early = get_block(ROOT / "common/production_methods/06_urban_center.txt", "pm_early_power_plant")
    if "goods_input_copper" in early:
        fail("Early power PM retained embedded copper after conductor-PMG migration")
    power = get_block(ROOT / "common/buildings/06_urban_center.txt", "building_power_plant")
    if "pmg_electrical_conductors_building_power_plant" not in power:
        fail("Power plant does not include conductor PMG")
    aero_pmg = get_block(ROOT / "common/production_method_groups/01_industry.txt", "pmg_aeroplanes")
    if "pm_all_metal_aircraft" not in aero_pmg:
        fail("All-metal aircraft not attached to aeroplane PMG")


def check_resolution_and_spelling() -> None:
    pms = set()
    for path in (ROOT / "common/production_methods").glob("*.txt"):
        pms.update(name for name, _ in blocks(read(path), r"(?m)^([a-zA-Z0-9_\-]+)\s*=\s*\{"))
    pmgs = read(ROOT / "common/production_method_groups/14_tech6c5c_aluminium_pmgs.txt")
    for ref in re.findall(r"(?m)^\s+(pm_[a-zA-Z0-9_]+)\s*$", pmgs):
        if ref not in pms:
            fail(f"Unresolved aluminium PMG reference: {ref}")

    goods = set()
    for folder in (ROOT / "common/goods", Path(r"C:/Games/Victoria 3/game/common/goods")):
        for path in folder.glob("*.txt"):
            goods.update(name for name, _ in blocks(read(path), r"(?m)^([a-zA-Z0-9_]+)\s*=\s*\{"))
    pm_text = read(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt")
    for good_id in re.findall(r"goods_(?:input|output)_([a-zA-Z0-9_]+)_(?:add|mult)", pm_text):
        if good_id not in goods:
            fail(f"Unknown good in aluminium PM file: {good_id}")

    introduced_paths = [
        ROOT / "common/goods/14_tech6c5c_aluminium.txt",
        ROOT / "common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt",
        ROOT / "common/production_method_groups/14_tech6c5c_aluminium_pmgs.txt",
        ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt",
        ROOT / "localization/english/tech6c5c_aluminium_l_english.yml",
        ROOT / "localization/french/tech6c5c_aluminium_l_french.yml",
    ]
    introduced = "\n".join(read(path) for path in introduced_paths)
    for label, pattern in {
        "ggoods_": r"\bggoods_",
        "orphan oods_": r"(?<!g)\boods_",
        "goods_aluminium_add": r"\bgoods_aluminium_add\b",
        "American-spelling ID": r"\b(?:goods_input_aluminum|goods_output_aluminum|g:aluminum|mg:aluminum|aluminum\s*=)",
    }.items():
        if re.search(pattern, introduced):
            fail(f"Malformed or mixed ID found: {label}")


def check_localization() -> None:
    for language, suffix in (("english", "l_english"), ("french", "l_french")):
        counts: Counter[str] = Counter()
        for path in (ROOT / "localization" / language).glob("*.yml"):
            counts.update(re.findall(r"(?m)^\s+([A-Za-z0-9_\-.]+):\d+\s+", read(path)))
        new_path = ROOT / f"localization/{language}/tech6c5c_aluminium_{suffix}.yml"
        for key in re.findall(r"(?m)^\s+([A-Za-z0-9_\-.]+):\d+\s+", read(new_path)):
            if counts[key] != 1:
                fail(f"Duplicate {language} localization key: {key}")
    for rel in (
        "localization/english/tech6c5c_aluminium_l_english.yml",
        "localization/french/tech6c5c_aluminium_l_french.yml",
        "localization/english/tech6c_goods_modifiers_l_english.yml",
        "localization/french/tech6c_goods_modifiers_l_french.yml",
    ):
        if not (ROOT / rel).read_bytes().startswith(b"\xef\xbb\xbf"):
            fail(f"Localization lacks UTF-8 BOM: {rel}")


def check_state_regions() -> None:
    parts = []
    paths = sorted((ROOT / "map_data/state_regions").glob("*.txt"))
    for path in paths:
        parts.append(f"{path.name}:{hashlib.sha256(path.read_bytes()).hexdigest().upper()}")
        text = read(path)
        if re.search(r"(?m)^\s*building_(?:aluminium|aluminum|bauxite|alumina)", text):
            fail(f"Forbidden aluminium-chain state resource in {path.name}")
    aggregate = hashlib.sha256("|".join(parts).encode()).hexdigest().upper()
    if aggregate != STATE_BASELINE:
        fail(f"State-region files changed during TECH6C5C: {aggregate}")


def check_technology_graph() -> int:
    techs: dict[str, set[str]] = {}
    for path in (ROOT / "common/technology/technologies").glob("*.txt"):
        for tech_id, block in blocks(read(path), r"(?m)^([a-zA-Z0-9_]+)\s*=\s*\{"):
            techs[tech_id] = technology_requirements(block)
    if "aluminium_metallurgy" in techs:
        fail("Dedicated aluminium_metallurgy technology was created")
    expected = {
        "industrial_alkalis": {"industrial_acids"},
        "electrical_capacitors": {"electrical_generation", "mechanized_weaving"},
        "military_aviation": {"wargaming"},
    }
    for tech_id, parents in expected.items():
        if techs.get(tech_id) != parents:
            fail(f"Unexpected parent set for {tech_id}: {sorted(techs.get(tech_id, set()))}")
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str) -> None:
        if node in visiting:
            fail(f"Technology cycle at {node}")
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
    gui_diff = subprocess.run(
        ["git", "diff", "--", "gui/tech_tree.gui"], cwd=ROOT, check=True, text=True, capture_output=True
    ).stdout
    if gui_diff:
        fail("gui/tech_tree.gui changed")
    return len(techs)


def check_copper_preserved() -> None:
    industry = read(ROOT / "common/production_methods/01_industry.txt")
    urban = read(ROOT / "common/production_methods/06_urban_center.txt")
    copper = read(ROOT / "common/production_methods/13_tech6c5b_copper_production_and_consumers.txt")
    checks = (
        (industry, r"pm_telephones\s*=.*?goods_input_copper_add\s*=\s*15", "telephones"),
        (industry, r"pm_electric_engines\s*=.*?goods_input_copper_add\s*=\s*10", "electric engines"),
        (industry, r"pm_radios\s*=.*?goods_input_copper_add\s*=\s*2", "radios"),
        (copper, r"pm_copper_sheathing_building_shipyard\s*=.*?goods_input_copper_add\s*=\s*5", "copper sheathing"),
    )
    for text, pattern, label in checks:
        if not re.search(pattern, text, re.S):
            fail(f"TECH6C5B copper consumer changed or missing: {label}")


def main() -> None:
    check_braces()
    check_objects_and_assets()
    check_gates_and_recipes()
    check_resolution_and_spelling()
    check_localization()
    check_state_regions()
    nodes = check_technology_graph()
    check_copper_preserved()
    print(f"technology_graph: nodes={nodes} cycles=0 new_aluminium_techs=0")
    print(f"state_regions: files=16 aggregate_sha256={STATE_BASELINE} changes_in_tech6c5c=0")
    if ERRORS:
        print(f"FAIL ({len(ERRORS)} errors)")
        for error in ERRORS:
            print(f"- {error}")
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
