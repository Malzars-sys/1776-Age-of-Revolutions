"""Static validation for the TECH6C5C alloys, bauxite and aluminium integration."""

from __future__ import annotations

import hashlib
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
        ("common/goods", "bauxite"): 1,
        ("common/goods", "alloys"): 1,
        ("common/goods", "aluminium"): 1,
        ("common/buildings", "building_bauxite_mine"): 1,
        ("common/buildings", "building_alloys_plant"): 1,
        ("common/technology/technologies", "alloysworking"): 1,
        ("common/technology/technologies", "bauxite_processing"): 1,
        ("common/technology/technologies", "bayer_process"): 1,
        ("common/production_method_groups", "pmg_alloys_process"): 1,
        ("common/production_method_groups", "pmg_aluminiummaking_process"): 1,
        ("common/production_method_groups", "pmg_electrical_conductors_building_power_plant"): 1,
        ("common/production_method_groups", "pmg_passenger_trains"): 1,
        ("common/production_method_groups", "pmg_mining_equipment_building_bauxite_mine"): 1,
        ("common/production_method_groups", "pmg_mine_ventilation_building_bauxite_mine"): 1,
        ("common/production_methods", "pm_hall_heroult_process"): 1,
        ("common/production_methods", "pm_wohler_deville_process"): 1,
        ("common/production_methods", "pm_basic_smelting_process"): 1,
        ("common/production_methods", "pm_electric_arc_process_alloying"): 1,
        ("common/production_methods", "pm_no_aluminium_production"): 1,
        ("common/production_methods", "pm_all_metal_aircraft"): 1,
        ("common/production_methods", "pm_aluminium_housewares"): 1,
        ("common/production_methods", "pm_aluminium_passenger_carriages"): 1,
        ("common/production_methods", "pm_copper_conductors_building_power_plant"): 1,
        ("common/production_methods", "pm_aluminium_conductors_building_power_plant"): 1,
        ("common/production_methods", "pm_steam_donkey_building_bauxite_mine"): 1,
        ("common/production_methods", "pm_rail_transport_building_bauxite_mine"): 1,
        ("common/production_methods", "pm_steam_mine_ventilation_building_bauxite_mine"): 1,
        ("common/production_methods", "pm_electric_mine_ventilation_building_bauxite_mine"): 1,
    }
    for (folder, object_id), wanted in expected.items():
        actual = definition_count(folder, object_id)
        if actual != wanted:
            fail(f"{object_id}: expected {wanted} definition, found {actual}")

    good = read(ROOT / "common/goods/14_tech6c5c_aluminium.txt")
    for required in ('bauxite = {', 'cost = 30', 'alloys = {', 'aluminium = {', 'cost = 50', 'category = industrial', 'tradeable = yes'):
        if required not in good:
            fail(f"Bauxite/aluminium goods file missing {required}")

    modifiers = read(ROOT / "common/modifier_type_definitions/12_tech6c_custom_goods_modifier_types.txt")
    for key in (
        "goods_input_alloys_add", "goods_input_alloys_mult", "goods_output_alloys_add", "goods_output_alloys_mult",
        "goods_input_bauxite_add", "goods_input_bauxite_mult", "goods_output_bauxite_add", "goods_output_bauxite_mult",
        "goods_input_aluminium_add", "goods_input_aluminium_mult", "goods_output_aluminium_add", "goods_output_aluminium_mult",
        "building_bauxite_mine_throughput_add",
    ):
        if len(re.findall(rf"(?m)^{key}\s*=", modifiers)) != 1:
            fail(f"Modifier definition missing or duplicated: {key}")
    if len(re.findall(r"(?m)^\s*icon\s*=\s*aluminium\s*$", read(ROOT / "gui/tech6c_goods_texticons.gui"))) != 1:
        fail("Aluminium texticon missing or duplicated")
    if len(re.findall(r"(?m)^\s*icon\s*=\s*alloys\s*$", read(ROOT / "gui/tech6c_goods_texticons.gui"))) != 1:
        fail("Alloys texticon missing or duplicated")
    if len(re.findall(r"(?m)^\s*icon\s*=\s*bauxite\s*$", read(ROOT / "gui/tech6c_goods_texticons.gui"))) != 1:
        fail("Bauxite texticon missing or duplicated")

    for rel in (
        "gfx/interface/icons/goods_icons/bauxite.dds",
        "gfx/interface/icons/goods_icons/alloys.dds",
        "gfx/interface/icons/goods_icons/aluminium.dds",
        "gfx/interface/icons/building_icons/building_bauxite_mine.dds",
        "gfx/interface/icons/building_icons/building_alloys_plant.dds",
        "gfx/interface/icons/invention_icons/alloysworking.dds",
        "gfx/interface/icons/invention_icons/bauxite_processing.dds",
        "gfx/interface/icons/invention_icons/bayer_process.dds",
        "gfx/interface/icons/production_method_icons/pm_hall_heroult_process.dds",
        "gfx/interface/icons/production_method_icons/pm_basic_smelting_process.dds",
        "gfx/interface/icons/production_method_icons/pm_electric_arc_process_alloying.dds",
        "gfx/interface/icons/production_method_icons/pm_no_aluminium_production.dds",
        "gfx/interface/icons/production_method_icons/pm_aluminium_inox_houseware.dds",
        "gfx/interface/icons/production_method_icons/pm_aluminium_passenger_carriages.dds",
        "gfx/interface/icons/state_trait_icons/bauxite_field_low.dds",
        "gfx/interface/icons/state_trait_icons/bauxite_field.dds",
    ):
        if not (ROOT / rel).is_file():
            fail(f"Missing imported asset: {rel}")


def check_gates_and_recipes() -> None:
    foundation = {"alloysworking"}
    early = {"bauxite_processing"}
    late = {"bayer_process"}
    bauxite_mine = get_block(ROOT / "common/buildings/14_tech6c5c_bauxite_mine.txt", "building_bauxite_mine")
    building = get_block(ROOT / "common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt", "building_alloys_plant")
    basic_alloys = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_basic_smelting_process")
    electric_alloys = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_electric_arc_process_alloying")
    wohler = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_wohler_deville_process")
    hall = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_hall_heroult_process")
    aircraft = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_all_metal_aircraft")
    aluminium_conductors = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_aluminium_conductors_building_power_plant")
    copper_conductors = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_copper_conductors_building_power_plant")
    housewares = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_aluminium_housewares")
    passenger = get_block(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt", "pm_aluminium_passenger_carriages")

    tech_path = ROOT / "common/technology/technologies/95_tech6r1_aluminium_metallurgy.txt"
    tech_eras = {
        "alloysworking": "era_2",
        "bauxite_processing": "era_6",
        "bayer_process": "era_10",
    }
    for tech_id, era in tech_eras.items():
        tech_block = get_block(tech_path, tech_id)
        if not re.search(rf"\bera\s*=\s*{era}\b", tech_block):
            fail(f"{tech_id} is not placed in {era}")

    for object_id, block in (("building_bauxite_mine", bauxite_mine), ("pm_wohler_deville_process", wohler), ("pm_aluminium_housewares", housewares)):
        if technology_requirements(block) != early:
            fail(f"{object_id} is not unlocked by bauxite_processing")
    for object_id, block in (("building_alloys_plant", building), ("pm_basic_smelting_process", basic_alloys)):
        if technology_requirements(block) != foundation:
            fail(f"{object_id} is not unlocked by alloysworking")
    if technology_requirements(electric_alloys) != {"electric_arc_process"}:
        fail("Electric arc alloying is not unlocked by electric_arc_process")
    if technology_requirements(hall) != late:
        fail("Hall-Heroult PM is not unlocked by bayer_process")
    if technology_requirements(aircraft) != late | {"military_aviation", "combustion_engine"}:
        fail("All-metal aircraft gate is not the required three-tech conjunction")
    if technology_requirements(aluminium_conductors) != late:
        fail("Aluminium conductors are not unlocked by bayer_process")
    if technology_requirements(passenger) != late:
        fail("Aluminium passenger carriages are not unlocked by bayer_process")

    wohler_invariants = {
        "goods_input_bauxite_add": 50,
        "goods_input_explosives_add": 3,
        "goods_input_sulfur_add": 3,
        "goods_output_alloys_add": -10,
        "goods_output_aluminium_add": 55,
    }
    for key, value in wohler_invariants.items():
        if not re.search(rf"\b{key}\s*=\s*{value}\b", wohler):
            fail(f"Wohler-Deville invariant failed: {key}={value}")

    hall_invariants = {
        "goods_input_bauxite_add": 40,
        "goods_input_industrial_chemicals_add": 10,
        "goods_input_electricity_add": 20,
        "goods_output_alloys_add": -15,
        "goods_output_aluminium_add": 80,
        "state_pollution_generation_add": 15,
        "building_employment_engineers_add": 250,
    }
    for key, value in hall_invariants.items():
        if not re.search(rf"\b{key}\s*=\s*{value}\b", hall):
            fail(f"Hall-Heroult invariant failed: {key}={value}")

    for block, invariants, label in (
        (basic_alloys, {"goods_input_iron_add": 25, "goods_input_copper_add": 15, "goods_input_lead_add": 10, "goods_input_coal_add": 10, "goods_output_alloys_add": 60}, "basic alloying"),
        (electric_alloys, {"goods_input_steel_add": 25, "goods_input_copper_add": 20, "goods_input_lead_add": 10, "goods_input_industrial_chemicals_add": 5, "goods_input_electricity_add": 10, "goods_output_alloys_add": 90}, "electric alloying"),
    ):
        for key, value in invariants.items():
            if not re.search(rf"\b{key}\s*=\s*{value}\b", block):
                fail(f"{label} invariant failed: {key}={value}")

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
    glass_pmg = get_block(ROOT / "common/production_method_groups/01_industry.txt", "pmg_base_building_glassworks")
    if "pm_aluminium_housewares" not in glass_pmg:
        fail("Aluminium housewares not attached to glassworks base PMG")
    passenger_pmg = get_block(ROOT / "common/production_method_groups/14_tech6c5c_aluminium_pmgs.txt", "pmg_passenger_trains")
    if "pm_aluminium_passenger_carriages" not in passenger_pmg:
        fail("Aluminium passenger carriages not attached to passenger-train PMG")
    for key, value in (("goods_input_aluminium_add", 5), ("goods_output_transportation_add", 20)):
        if not re.search(rf"\b{key}\s*=\s*{value}\b", passenger):
            fail(f"Aluminium passenger-carriage invariant failed: {key}={value}")

    alloy_consumers = {
        ROOT / "common/production_methods/01_industry.txt": {
            "pm_mechanized_workshops": 10,
            "pm_steel": 2,
            "pm_rubber_grips": 5,
            "pm_metal_shipbuilding": 10,
            "pm_arc_welding_shipbuilding": 10,
            "pm_automobile_production": 5,
            "pm_mass_automobile_production": 10,
            "pm_repeaters": 5,
            "pm_bolt_action_rifles": 10,
            "pm_smoothbores": 5,
            "pm_breech_loaders": 5,
            "pm_recoiled_barrels": 10,
        },
        ROOT / "common/production_methods/06_urban_center.txt": {
            "pm_arcades": 1,
            "pm_gas_streetlights": 0.5,
            "pm_electric_streetlights": 0.5,
        },
        ROOT / "common/production_methods/13_construction.txt": {
            "pm_steel_frame_buildings": 10,
            "pm_arc_welded_buildings": 10,
        },
    }
    for path, consumers in alloy_consumers.items():
        for pm_id, amount in consumers.items():
            block = get_block(path, pm_id)
            if not re.search(rf"\bgoods_input_alloys_add\s*=\s*{amount}\b", block):
                fail(f"Source-compatible alloy consumer missing or changed: {pm_id}={amount}")

    mine_recipes = {
        "pm_picks_and_shovels_building_bauxite_mine": ("goods_output_bauxite_add", 20),
        "pm_atmospheric_engine_pump_building_bauxite_mine": ("goods_output_bauxite_add", 40),
        "pm_condensing_engine_pump_building_bauxite_mine": ("goods_output_bauxite_add", 60),
        "pm_diesel_pump_building_bauxite_mine": ("goods_output_bauxite_add", 85),
        "pm_nitroglycerin_building_bauxite_mine": ("goods_output_bauxite_add", 12),
        "pm_dynamite_building_bauxite_mine": ("goods_output_bauxite_add", 20),
        "pm_ore_concentration_building_bauxite_mine": ("goods_output_bauxite_add", 16),
    }
    recipe_path = ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt"
    for pm_id, (key, value) in mine_recipes.items():
        block = get_block(recipe_path, pm_id)
        if not re.search(rf"\b{key}\s*=\s*{value}\b", block):
            fail(f"Bauxite mine recipe invariant failed: {pm_id} {key}={value}")

    gated_bauxite_mine_pms = {
        "pm_atmospheric_engine_pump_building_bauxite_mine",
        "pm_condensing_engine_pump_building_bauxite_mine",
        "pm_diesel_pump_building_bauxite_mine",
        "pm_nitroglycerin_building_bauxite_mine",
        "pm_dynamite_building_bauxite_mine",
        "pm_ore_concentration_building_bauxite_mine",
        "pm_steam_donkey_building_bauxite_mine",
        "pm_rail_transport_building_bauxite_mine",
        "pm_steam_mine_ventilation_building_bauxite_mine",
        "pm_electric_mine_ventilation_building_bauxite_mine",
    }
    for pm_id in gated_bauxite_mine_pms:
        block = get_block(recipe_path, pm_id)
        if "bauxite_processing" not in technology_requirements(block):
            fail(f"Bauxite mine PM can predate its building unlock: {pm_id}")


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
        "localization/english/tech6r1_aluminium_metallurgy_l_english.yml",
        "localization/french/tech6r1_aluminium_metallurgy_l_french.yml",
        "localization/english/replace/tech3a_arc_welding_replace_l_english.yml",
        "localization/french/replace/tech3a_arc_welding_replace_l_french.yml",
    ):
        if not (ROOT / rel).read_bytes().startswith(b"\xef\xbb\xbf"):
            fail(f"Localization lacks UTF-8 BOM: {rel}")

    required = {
        "bauxite", "alloys", "aluminium", "building_bauxite_mine", "building_alloys_plant",
        "pmg_alloys_process", "pmg_aluminiummaking_process", "pm_basic_smelting_process",
        "pm_electric_arc_process_alloying", "pm_no_aluminium_production", "alloysworking",
        "pm_wohler_deville_process", "pm_hall_heroult_process", "pm_aluminium_housewares",
        "pm_aluminium_passenger_carriages",
        "pmg_mine_ventilation_building_bauxite_mine",
        "pm_steam_donkey_building_bauxite_mine", "pm_rail_transport_building_bauxite_mine",
        "pm_steam_mine_ventilation_building_bauxite_mine", "pm_electric_mine_ventilation_building_bauxite_mine",
        "bauxite_processing", "bayer_process", "bauxite_mining_deposits_visible_tt",
    }
    for language in ("english", "french"):
        localized: set[str] = set()
        for path in (ROOT / "localization" / language).rglob("*.yml"):
            localized.update(re.findall(r"(?m)^\s+([A-Za-z0-9_\-.]+):\d+\s+", read(path)))
        missing = required - localized
        if missing:
            fail(f"Missing {language} aluminium localization: {sorted(missing)}")


def check_state_regions() -> str:
    parts = []
    paths = sorted((ROOT / "map_data/state_regions").glob("*.txt"))
    for path in paths:
        parts.append(f"{path.name}:{hashlib.sha256(path.read_bytes()).hexdigest().upper()}")
        text = read(path)
        if re.search(r"(?m)^\s*building_(?:aluminium|aluminum|bauxite|alumina)", text):
            fail(f"Forbidden aluminium-chain state resource in {path.name}")
    aggregate = hashlib.sha256("|".join(parts).encode()).hexdigest().upper()
    return aggregate


def check_dynamic_distribution() -> int:
    effect_path = ROOT / "common/scripted_effects/14_tech6c5c_bauxite_deposits.txt"
    text = read(effect_path)
    tiers = {
        "tech6c_bauxite_nano_add_deposits": (53, 10, None),
        "tech6c_bauxite_small_add_deposits": (72, 25, None),
        "tech6c_bauxite_medium_add_deposits": (24, 50, "state_trait_medium_bauxite_mine"),
        "tech6c_bauxite_big_add_deposits": (9, 120, "state_trait_big_bauxite_mine"),
        "tech6c_bauxite_huge_add_deposits": (3, 200, "state_trait_huge_bauxite_mine"),
    }
    all_distributed: list[str] = []
    for effect_id, (wanted_count, amount, trait) in tiers.items():
        block = dict(blocks(text, rf"(?m)^({effect_id})\s*=\s*\{{")).get(effect_id, "")
        if not block:
            fail(f"Missing bauxite distribution effect: {effect_id}")
            continue
        states = re.findall(r"\bthis\s*=\s*s:(STATE_[A-Z0-9_]+)", block)
        if len(states) != wanted_count:
            fail(f"{effect_id}: expected {wanted_count} states, found {len(states)}")
        if not re.search(rf"\btype\s*=\s*building_bauxite_mine\b.*?\bamount\s*=\s*{amount}\b", block, re.S):
            fail(f"{effect_id}: expected resource amount {amount}")
        if trait and not re.search(rf"\badd_state_trait\s*=\s*{trait}\b", block):
            fail(f"{effect_id}: missing {trait}")
        all_distributed.extend(states)

    duplicates = sorted(state for state, count in Counter(all_distributed).items() if count > 1)
    if duplicates:
        fail(f"Bauxite states occur in more than one tier: {duplicates}")

    known_states: set[str] = set()
    for path in (ROOT / "map_data/state_regions").glob("*.txt"):
        known_states.update(re.findall(r"(?m)^(STATE_[A-Z0-9_]+)\s*=\s*\{", read(path)))
    unknown = sorted(set(all_distributed) - known_states)
    if unknown:
        fail(f"Unknown state IDs in bauxite distribution: {unknown}")

    orchestrator = dict(blocks(text, r"(?m)^(tech6c_reveal_bauxite_deposits)\s*=\s*\{")).get("tech6c_reveal_bauxite_deposits", "")
    for effect_id in tiers:
        if not re.search(rf"\b{effect_id}\s*=\s*yes\b", orchestrator):
            fail(f"Bauxite orchestrator does not invoke {effect_id}")
    if "has_global_variable = tech6c_bauxite_deposits_revealed" not in orchestrator or "set_global_variable = tech6c_bauxite_deposits_revealed" not in orchestrator:
        fail("Bauxite distribution is not protected by its one-shot global variable")
    return len(all_distributed)


def check_technology_graph() -> int:
    techs: dict[str, set[str]] = {}
    for path in (ROOT / "common/technology/technologies").glob("*.txt"):
        for tech_id, block in blocks(read(path), r"(?m)^([a-zA-Z0-9_]+)\s*=\s*\{"):
            techs[tech_id] = technology_requirements(block)
    expected = {
        "industrial_alkalis": {"industrial_acids"},
        "electrical_capacitors": {"advanced_spinning", "electrical_generation", "mechanized_weaving"},
        "military_aviation": {"wargaming"},
        "alloysworking": {"shaft_mining"},
        "bauxite_processing": {"alloysworking", "industrial_alkalis"},
        "bayer_process": {"bauxite_processing", "electrical_capacitors"},
        "arc_welding": {"electric_arc_process", "pneumatic_tools", "reinforced_concrete"},
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
    state_hash = check_state_regions()
    distributed_states = check_dynamic_distribution()
    nodes = check_technology_graph()
    check_copper_preserved()
    print(f"technology_graph: nodes={nodes} cycles=0 alloy_aluminium_techs=3")
    print(f"bauxite_distribution: states={distributed_states} tiers=5 duplicates=0 unknown_states=0")
    print(f"state_regions: files=16 aggregate_sha256={state_hash} direct_bauxite_entries=0")
    if ERRORS:
        print(f"FAIL ({len(ERRORS)} errors)")
        for error in ERRORS:
            print(f"- {error}")
        raise SystemExit(1)
    print("PASS")


if __name__ == "__main__":
    main()
