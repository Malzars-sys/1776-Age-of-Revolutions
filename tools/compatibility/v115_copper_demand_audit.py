"""Read-only copper-demand comparison against the installed 1.15 game data.

Checks all 28 native consumer recipes, effective file/ID resolution, PM group
reachability, narrowly allowed edits, and preservation of the mod's mine supply.
No quantities in this audit are a measured national market balance.
"""
import argparse
from collections import defaultdict
from dataclasses import replace
import hashlib
import json
from pathlib import Path
import re

import issue27_journal_outcomes_audit as parser

EXPECTED = {
    "pm_pot_stills": 2, "pm_patent_stills": 4, "pm_automated_bakery": 1,
    "pm_electric_sewing_machines": 2, "pm_automatic_power_looms": 2,
    "pm_assembly_lines_building_furniture_manufactory": 1,
    "pm_assembly_lines_building_tooling_workshop": 1,
    "pm_electric_engines": 10, "pm_assembly_lines_building_motor_industry": 1,
    "pm_assembly_lines_building_automotive_industry": 1, "pm_telephones": 30,
    "pm_bronze_cannons": 10, "pm_bronze_smoothbores": 20,
    "pm_assembly_lines_building_arms_industry": 1, "pm_percussion_caps": 5,
    "pm_explosive_shells": 10, "pm_assembly_lines_building_munition_plant": 1,
    "pm_arcades": 1, "pm_early_power_plant": 2, "pm_coal-fired_plant": 4,
    "pm_oil-fired_plant": 5,
    "pm_refrigerated_storage_building_fishing_wharf": 1,
    "pm_refrigerated_rail_cars_building_fishing_wharf": 1,
    "pm_flash_freezing_building_fishing_wharf": 1,
    "pm_refrigerated_storage_building_whaling_station": 1,
    "pm_refrigerated_rail_cars_building_whaling_station": 1,
    "pm_flash_freezing_building_whaling_station": 1,
    "pm_arc_welded_buildings": 10,
}
PM_FILES = (
    "01_industry.txt", "06_urban_center.txt", "09_misc_resource.txt", "13_construction.txt",
    "13_tech6c5b_copper_production_and_consumers.txt",
    "14_tech6c5c_aluminium_production_and_consumers.txt",
)
GROUP_FILE = "common/production_method_groups/01_industry.txt"
NEW_FILE = "common/production_methods/1776_v115_bronze_artillery.txt"
NEW_PMS = {"pm_bronze_cannons", "pm_bronze_smoothbores"}
COPPER_CONDUCTOR = "pm_copper_conductors_building_power_plant"
ALUMINIUM_CONDUCTOR = "pm_aluminium_conductors_building_power_plant"
ICONS = {
    "pm_no_ore_concentration_building_copper_mine": '"gfx/interface/icons/production_method_icons/1776_manual_ore_sorting.dds"',
    "pm_ore_concentration_building_copper_mine": '"gfx/interface/icons/production_method_icons/1776_ore_concentration.dds"',
}
INPUT = re.compile(r"\bgoods_input_copper_add\s*=\s*[-+]?\d+(?:\.\d+)?")


def one(fields, key, optional=False):
    return parser.one(fields, key, optional)


def workforce(pm):
    building = one(parser.fields(pm.body), "building_modifiers", True)
    return one(parser.fields(building.body), "workforce_scaled", True) if building else None


def quantity(pm):
    block = workforce(pm)
    field = one(parser.fields(block.body), "goods_input_copper_add", True) if block else None
    return float(field.value) if field else 0.0


def content_path(mod, relative, overlay=None):
    return overlay / relative if overlay and (overlay / relative).exists() else mod / relative


def effective(mod, vanilla, category, overlay=None):
    """Resolve same-path masking and explicit REPLACE_OR_CREATE directives."""
    local = {p.name: p for p in (mod / "common" / category).glob("*.txt")}
    if overlay:
        local.update({p.name: p for p in (overlay / "common" / category).glob("*.txt")})
    files = [p for p in (vanilla / "common" / category).glob("*.txt") if p.name not in local]
    files += list(local.values())
    normal, directives = defaultdict(list), defaultdict(list)
    for path in sorted(files):
        for node in parser.fields(path.read_text(encoding="utf-8-sig")):
            if not node.block:
                continue
            prefix, _, name = node.key.partition(":")
            if prefix == "REPLACE_OR_CREATE":
                directives[name].append((path, replace(node, key=name)))
            else:
                normal[node.key].append((path, node))
    normal.update(directives)
    return normal


def unique(objects, key):
    parser.check(len(objects.get(key, [])) == 1, "Missing or ambiguous effective object: " + key)
    return objects[key][0]


def remove_field(body, key):
    field = one(parser.fields(body), key)
    return body[:field.start] + body[field.end:]


def verify_existing(before, after):
    key = before.key
    if key in EXPECTED:
        parser.check(quantity(after) == EXPECTED[key], "Native copper quantity differs: " + key)
        parser.check(parser.signature(INPUT.sub("", before.body)) == parser.signature(INPUT.sub("", after.body)),
                     "Non-copper recipe changed: " + key)
    elif key == COPPER_CONDUCTOR:
        parser.check(quantity(after) == 0, "Power plant copper counted twice")
        parser.check(parser.signature(INPUT.sub("", before.body)) == parser.signature(INPUT.sub("", after.body)),
                     "Copper conductor changed outside its redundant input")
    elif key == ALUMINIUM_CONDUCTOR:
        old_fields, new_fields = parser.fields(before.body), parser.fields(after.body)
        old_building = one(old_fields, "building_modifiers")
        new_building = one(new_fields, "building_modifiers")
        unscaled = one(parser.fields(new_building.body), "unscaled")
        parser.check(parser.signature(unscaled.body) == ("goods_input_copper_mult", "=", "-1"),
                     "Aluminium conductor must remove the base copper demand")
        normalized = replace(new_building, body=remove_field(new_building.body, "unscaled"))
        replacement = "building_modifiers = {" + normalized.body + "}"
        normalized_body = after.body[:new_building.start] + replacement + after.body[new_building.end:]
        parser.check(parser.signature(before.body) == parser.signature(normalized_body),
                     "Aluminium alternative changed beyond copper substitution")
    elif key in ICONS:
        parser.check(one(parser.fields(after.body), "texture").value == ICONS[key], "Wrong concentration icon")
        parser.check(parser.signature(remove_field(before.body, "texture")) == parser.signature(remove_field(after.body, "texture")),
                     "Mine output or other non-visual field changed")
    else:
        parser.check(before.body == after.body, "Untargeted PM changed: " + key)


def audit(mod, baseline, vanilla, overlay=None):
    errors, matrix, untouched, changed = [], [], [], []
    native = effective(vanilla, vanilla, "production_methods")
    current = effective(mod, vanilla, "production_methods", overlay)
    groups = effective(mod, vanilla, "production_method_groups", overlay)
    buildings = effective(mod, vanilla, "buildings", overlay)
    references = {key: quantity(unique(native, key)[1]) for key in EXPECTED}
    parser.check(references == EXPECTED, "Installed vanilla copper coefficients changed; review the reference")
    discovered = {key for key, values in native.items() if any(quantity(pm) > 0 for _, pm in values)}
    parser.check(discovered == set(EXPECTED), "Installed vanilla copper consumer inventory changed")
    for name in PM_FILES:
        rel = Path("common/production_methods") / name
        old = parser.fields((baseline / rel).read_bytes().decode("utf-8-sig"))
        new = parser.fields(content_path(mod, rel, overlay).read_bytes().decode("utf-8-sig"))
        try:
            parser.check([x.key for x in old] == [x.key for x in new], "PM inventory/order changed in " + name)
            for before, after in zip(old, new):
                verify_existing(before, after)
                (untouched if before.body == after.body else changed).append(before.key)
        except ValueError as exc:
            errors.append(str(exc))
    try:
        bronze = parser.fields(content_path(mod, NEW_FILE, overlay).read_text(encoding="utf-8-sig"))
        parser.check({x.key for x in bronze} == NEW_PMS and len(bronze) == 2, "Wrong new PM inventory")
        for node in bronze:
            source = unique(native, node.key)[1]
            if node.key == "pm_bronze_cannons":
                field = one(parser.fields(source.body), "unlocking_technologies")
                source = replace(source, body=source.body[:field.start] + "unlocking_technologies = { organized_military_establishments }" + source.body[field.end:])
            parser.check(parser.signature(source.body) == parser.signature(node.body), "Bronze PM differs beyond the documented tech mapping")
        rel = Path(GROUP_FILE)
        before_groups = parser.fields((baseline / rel).read_bytes().decode("utf-8-sig"))
        after_groups = parser.fields(content_path(mod, rel, overlay).read_bytes().decode("utf-8-sig"))
        parser.check([x.key for x in before_groups] == [x.key for x in after_groups], "PMG inventory changed")
        for old, new in zip(before_groups, after_groups):
            if old.key != "pmg_foundries":
                parser.check(old.body == new.body, "Untargeted PMG changed")
            else:
                normalized = re.sub(r"\bpm_bronze_(?:cannons|smoothbores)\b", "", new.body)
                parser.check(parser.signature(old.body) == parser.signature(normalized), "Foundry group changed beyond the two new options")
                methods = one(parser.fields(new.body), "production_methods")
                ids = parser.signature(methods.body)
                parser.check(ids[0] == "pm_cannons" and all(ids.count(x) == 1 for x in NEW_PMS), "Foundry default/order or new membership invalid")
    except ValueError as exc:
        errors.append(str(exc))
    technologies = set()
    for path in (mod / "common/technology/technologies").glob("*.txt"):
        technologies.update(node.key for node in parser.fields(path.read_text(encoding="utf-8-sig")) if node.block)
    for key, expected in EXPECTED.items():
        try:
            path, pm = unique(current, key)
            parser.check(quantity(pm) == expected, "Wrong effective copper demand: " + key)
            techs = one(parser.fields(pm.body), "unlocking_technologies", True)
            if techs:
                parser.check(set(parser.signature(techs.body)) <= technologies, "Unresolved consumer technology: " + key)
            member_groups = []
            for group_key, definitions in groups.items():
                for _, definition in definitions:
                    field = one(parser.fields(definition.body), "production_methods", True)
                    if field and key in parser.signature(field.body):
                        unique(groups, group_key)
                        member_groups.append(group_key)
            member_buildings = []
            for building_key, definitions in buildings.items():
                for _, definition in definitions:
                    field = one(parser.fields(definition.body), "production_method_groups", True)
                    if field and set(member_groups) & set(parser.signature(field.body)):
                        member_buildings.append(building_key)
            parser.check(member_groups and member_buildings, "Consumer not reachable from a building: " + key)
            old_quantity = None
            for filename in PM_FILES:
                for old in parser.fields((baseline / "common/production_methods" / filename).read_text(encoding="utf-8-sig")):
                    if old.key == key:
                        old_quantity = quantity(old)
            matrix.append({"pm": key, "before_copper": old_quantity, "vanilla_copper": expected,
                           "after_copper": quantity(pm), "groups": member_groups, "buildings": sorted(set(member_buildings)),
                           "effective_definition": str(path)})
        except ValueError as exc:
            errors.append(str(exc))
    try:
        copper = unique(current, COPPER_CONDUCTOR)[1]
        aluminium = unique(current, ALUMINIUM_CONDUCTOR)[1]
        building = one(parser.fields(aluminium.body), "building_modifiers")
        multiplier = float(one(parser.fields(one(parser.fields(building.body), "unscaled").body), "goods_input_copper_mult").value)
        stacks = []
        for key in ("pm_early_power_plant", "pm_coal-fired_plant", "pm_oil-fired_plant"):
            amount = quantity(unique(current, key)[1]) + quantity(copper)
            parser.check(amount == EXPECTED[key] and amount * (1 + multiplier) == 0, "Power plant stack/substitution differs")
            stacks.append({"base_pm": key, "copper_conductors": amount, "aluminium_conductors": 0})
        for key, texture in ICONS.items():
            icon = mod / texture.strip('"')
            parser.check(icon.is_file() and icon.read_bytes()[:4] == b"DDS ", "Missing/invalid existing mine icon")
        for language in ("english", "french"):
            rel = Path("localization") / language / ("production_methods_l_" + language + ".yml")
            loc = content_path(mod, rel, overlay)
            if not loc.exists():
                loc = vanilla / rel
            text = loc.read_text(encoding="utf-8-sig")
            for key in NEW_PMS:
                parser.check(re.search(r"^\s*" + key + r":", text, re.M), "New bronze PM localization missing: " + key)
    except ValueError as exc:
        errors.append(str(exc))
        stacks = []
    return {"status": "PASS_STATIC_ONLY" if not errors else "FAIL_STATIC", "runtime_tested": False,
            "native_consumers": len(matrix), "matrix": matrix, "changed_existing_pms": changed,
            "untargeted_pms_unchanged": len(untouched), "power_plant_stacks": stacks, "errors": errors,
            "limits": ["Coefficients per building level at full staffing, before other modifiers; not observed market demand.",
                       "The aluminium alternative applies -100% copper input on the building; verify effective modifiers in game.",
                       "Existing copper good/mining-group duplicate definitions are separate inherited debt, unchanged here."]}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--mod-root", type=Path, required=True)
    ap.add_argument("--baseline-root", type=Path, required=True)
    ap.add_argument("--vanilla-root", type=Path, required=True)
    ap.add_argument("--overlay-root", type=Path)
    args = ap.parse_args()
    result = audit(args.mod_root, args.baseline_root, args.vanilla_root, args.overlay_root)
    print(json.dumps(result, indent=2))
    return bool(result["errors"])


if __name__ == "__main__":
    raise SystemExit(main())
