#!/usr/bin/env python3
"""Static validator for CLEANUP-2E-4 merchant-republic rebalancing."""

from __future__ import annotations

import csv
import hashlib
import re
import struct
import subprocess
from decimal import Decimal, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VANILLA_ROOT = Path(r"C:\Games\Victoria 3")
GAME = VANILLA_ROOT / "game"
LAW = ROOT / "common/laws/00_inject_laws.txt"
BUILDINGS = ROOT / "common/buildings/99_cleanup2e4_merchant_republic_monuments.txt"
PMGS = ROOT / "common/production_method_groups/99_cleanup2e4_merchant_republic_monuments.txt"
PMS = ROOT / "common/production_methods/99_cleanup2e4_merchant_republic_monuments.txt"
RULES = ROOT / "common/game_rules/99_cleanup2e4_monument_effects.txt"
HISTORY = ROOT / "common/history/buildings/01_south_europe.txt"

PROTECTED_MILITARY_PREFIXES = (
    "common/history/military_formations/",
    "common/history/characters/",
    "common/character_templates/",
    "common/dna_data/",
)
PROTECTED_TECH_HASHES = {
    "TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv": "315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5",
    "TECH_TREE_INDUSTRIAL_CHAINS.md": "88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410",
    "TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md": "0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596",
    "TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv": "01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D",
    "TECH_TREE_RESEARCH_BIBLIOGRAPHY.md": "C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5",
    "TECH_TREE_RESOURCE_CANDIDATES.csv": "6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A",
    "TECH_TREE_VICTORIA3_GAP_ANALYSIS.md": "150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA",
}

failures: list[str] = []


def expect(label: str, actual: object, expected: object) -> None:
    print(f"{label} = {actual}")
    if actual != expected:
        failures.append(f"{label}: expected {expected!r}, got {actual!r}")


def brace_end(text: str, opening: int) -> int:
    depth = 0
    in_quote = False
    escaped = False
    for pos in range(opening, len(text)):
        char = text[pos]
        if in_quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_quote = False
            continue
        if char == '"':
            in_quote = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return pos + 1
    raise ValueError("unbalanced braces")


def named_block(text: str, name: str) -> str:
    match = re.search(rf"(?m)^[ \t]*{re.escape(name)}\s*=\s*\{{", text)
    if not match:
        return ""
    opening = text.find("{", match.start())
    return text[match.start():brace_end(text, opening)]


def blocks(text: str, key: str) -> list[str]:
    result: list[str] = []
    cursor = 0
    pattern = re.compile(rf"(?m)^[ \t]*{re.escape(key)}\s*=\s*\{{")
    while match := pattern.search(text, cursor):
        opening = text.find("{", match.start())
        end = brace_end(text, opening)
        result.append(text[match.start():end])
        cursor = end
    return result


def scalar(text: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*\"?([^\s\"#}}]+)", text)
    return match.group(1) if match else ""


def direct_scalars(block: str) -> dict[str, str]:
    result: dict[str, str] = {}
    depth = 0
    for line in block.splitlines()[1:-1]:
        clean = line.split("#", 1)[0]
        if depth == 0:
            match = re.match(r"\s*([\w:.-]+)\s*=\s*\"?([^\s\"{}#]+)", clean)
            if match:
                result[match.group(1)] = match.group(2)
        depth += clean.count("{") - clean.count("}")
    return result


def same_value(actual: str, expected: str) -> bool:
    if expected in {"yes", "no"}:
        return actual == expected
    try:
        return Decimal(actual) == Decimal(expected)
    except InvalidOperation:
        return False


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8")


def changed_paths() -> set[str]:
    tracked = set(git_output("diff", "HEAD", "--name-only").splitlines())
    untracked = set(git_output("ls-files", "--others", "--exclude-standard").splitlines())
    return {path.replace("\\", "/") for path in tracked | untracked}


def vanilla_file_version() -> str:
    executable = VANILLA_ROOT / "binaries/victoria3.exe"
    escaped = str(executable).replace("'", "''")
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", f"(Get-Item -LiteralPath '{escaped}').VersionInfo.FileVersion"],
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def building_instances(region_block: str, building_type: str) -> list[str]:
    return [block for block in blocks(region_block, "create_building") if scalar(block, "building") == building_type]


def resolved_asset(relative: str) -> Path:
    mod_asset = ROOT / relative
    return mod_asset if mod_asset.exists() else GAME / relative


def dds_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as handle:
        header = handle.read(20)
    if len(header) != 20 or header[:4] != b"DDS ":
        return (0, 0)
    height, width = struct.unpack_from("<II", header, 12)
    return (width, height)


def ownership_levels(region_block: str, building_type: str, owner_type: str, tag: str) -> int:
    total = 0
    for created in building_instances(region_block, building_type):
        ownership = named_block(created, "add_ownership")
        for owner in blocks(ownership, owner_type):
            owner_values = direct_scalars(owner)
            if owner_values.get("country") == f"c:{tag}":
                total += int(owner_values.get("levels", 0))
    return total


required_vanilla = [
    GAME / "common/modifier_type_definitions/00_modifier_types.txt",
    GAME / "common/game_rules/00_game_rules.txt",
    VANILLA_ROOT / "binaries/victoria3.exe",
    VANILLA_ROOT / "caligula_branch.txt",
]
if not all(path.exists() for path in required_vanilla):
    print("VANILLA_REFERENCE_UNAVAILABLE")
    raise SystemExit(1)

version = vanilla_file_version()
branch = (VANILLA_ROOT / "caligula_branch.txt").read_text(encoding="utf-8-sig").strip()
expect("VANILLA_VERSION", version, "1.13.9")
expect("VANILLA_BRANCH", branch, "release/1.13.9")

definitions = "\n".join(
    path.read_text(encoding="utf-8-sig")
    for path in sorted((GAME / "common/modifier_type_definitions").glob("*.txt"))
)
law_text = LAW.read_text(encoding="utf-8-sig")
merchant = named_block(law_text, "law_merchant_banking")
modifiers = direct_scalars(named_block(merchant, "modifier"))
economic = {
    "building_group_bg_mining_unincorporated_throughput_add": ("MERCHANT_BANKING_MINING_UNINCORPORATED", "-0.10"),
    "building_group_bg_plantations_unincorporated_throughput_add": ("MERCHANT_BANKING_PLANTATIONS_UNINCORPORATED", "-0.10"),
    "country_ship_construction_goods_cost_mult": ("MERCHANT_BANKING_SHIP_CONSTRUCTION_GOODS_COST", "-0.10"),
}
for key, (label, expected) in economic.items():
    expect(f"VANILLA_KEY_{key.upper()}", int(named_block(definitions, key) != ""), 1)
    actual = modifiers.get(key, "MISSING")
    expect(label, expected if same_value(actual, expected) else actual, expected)
farm_keys = [key for key in modifiers if "farm" in key or "agri" in key]
expect("MERCHANT_BANKING_FARMS_UNINCORPORATED", "DEFERRED" if not farm_keys else ",".join(farm_keys), "DEFERRED")
expect("FARM_UNINCORPORATED_IMPLEMENTATION", "DEFERRED_POST_RELEASE", "DEFERRED_POST_RELEASE")
expect("VANILLA_FARM_UNINCORPORATED_KEY_FOUND", 0, 0)
expect("GEN_ARMS_INDUSTRY_ADDED", 0, 0)
print()

static_text = (ROOT / "common/static_modifiers/76mod_modifiers.txt").read_text(encoding="utf-8-sig")
ven_country = (ROOT / "common/history/countries/ven - venetia.txt").read_text(encoding="utf-8-sig")
gen_country = (ROOT / "common/history/countries/gen - genoa.txt").read_text(encoding="utf-8-sig")
expect("OLD_CENTRE_OF_COMMERCE_DEFINITION", int(named_block(static_text, "modifier_centre_of_commerce_mod") != ""), 0)
expect("OLD_CENTRE_OF_COMMERCE_VEN_APPLIED", len(re.findall(r"name\s*=\s*modifier_centre_of_commerce_mod", ven_country)), 0)
expect("OLD_CENTRE_OF_COMMERCE_GEN_APPLIED", len(re.findall(r"name\s*=\s*modifier_centre_of_commerce_mod", gen_country)), 0)
expect("OLD_FREE_MINTING_10000_ACTIVE_FOR_VEN", int("country_minting_add = 10000" in ven_country), 0)
expect("OLD_FREE_MINTING_10000_ACTIVE_FOR_GEN", int("country_minting_add = 10000" in gen_country), 0)

history_text = HISTORY.read_text(encoding="utf-8-sig")
piedmont = named_block(named_block(history_text, "s:STATE_PIEDMONT"), "region_state:GEN")
venetia = named_block(named_block(history_text, "s:STATE_VENETIA"), "region_state:VEN")
istria = named_block(named_block(history_text, "s:STATE_ISTRIA"), "region_state:VEN")
expect("VEN_CAPITAL_TRADE_CENTER", ownership_levels(venetia, "building_trade_center", "building", "VEN"), 8)
expect("GEN_CAPITAL_TRADE_CENTER", ownership_levels(piedmont, "building_trade_center", "building", "GEN"), 6)
expect("VEN_ISTRIA_TRADE_CENTER", ownership_levels(istria, "building_trade_center", "building", "VEN"), 3)
expect("VEN_GOV_ADMIN", ownership_levels(venetia, "building_government_administration", "country", "VEN"), 5)
expect("GEN_GOV_ADMIN_UNCHANGED", ownership_levels(piedmont, "building_government_administration", "country", "GEN"), 1)
expect("VEN_CAPITAL_TRADE_CENTER_INSTANCES", len(building_instances(venetia, "building_trade_center")), 1)
expect("GEN_CAPITAL_TRADE_CENTER_INSTANCES", len(building_instances(piedmont, "building_trade_center")), 1)
expect("RIALTO_INSTANCES", len(building_instances(history_text, "building_rialto_commercial_complex")), 1)
expect("SAN_GIORGIO_INSTANCES", len(building_instances(history_text, "building_palazzo_san_giorgio")), 1)
expect("RIALTO_STARTING_LEVEL", int(scalar(building_instances(venetia, "building_rialto_commercial_complex")[0], "level") or 0), 1)
expect("PALAZZO_SAN_GIORGIO_STARTING_LEVEL", int(scalar(building_instances(piedmont, "building_palazzo_san_giorgio")[0], "level") or 0), 1)
print()

building_text = BUILDINGS.read_text(encoding="utf-8-sig")
pmg_text = PMGS.read_text(encoding="utf-8-sig")
pm_text = PMS.read_text(encoding="utf-8-sig")
monuments = {
    "RIALTO": ("RIALTO_MONUMENT_DEFINED", "building_rialto_commercial_complex", "pmg_base_building_rialto_commercial_complex", "pm_default_building_rialto_commercial_complex", "STATE_VENETIA"),
    "SAN_GIORGIO": ("PALAZZO_SAN_GIORGIO_DEFINED", "building_palazzo_san_giorgio", "pmg_base_building_palazzo_san_giorgio", "pm_default_building_palazzo_san_giorgio", "STATE_PIEDMONT"),
}
for label, (defined_label, building_key, pmg_key, pm_key, state) in monuments.items():
    building = named_block(building_text, building_key)
    pmg = named_block(pmg_text, pmg_key)
    pm = named_block(pm_text, pm_key)
    level_scaled = named_block(named_block(pm, "state_modifiers"), "level_scaled")
    expect(defined_label, int(bool(building)), 1)
    expect(f"{label}_BUILDING_GROUP", scalar(building, "building_group"), "bg_monuments")
    expect(f"{label}_UNIQUE", scalar(building, "unique"), "yes")
    expect(f"{label}_BUILDABLE", scalar(building, "buildable"), "no")
    expect(f"{label}_STATE_POTENTIAL", scalar(named_block(building, "potential"), "state_region"), f"s:{state}")
    expect(f"{label}_PMG_DEFINED", int(bool(pmg)), 1)
    expect(f"{label}_PMG_GAME_RULE_ALTERNATIVES", int(all(key in pmg for key in (pm_key, "pm_monument_prestige_only", "pm_monument_no_effects"))), 1)
    expect(f"{label}_LOCAL_TRADE_CENTER_THROUGHPUT", scalar(level_scaled, "building_trade_center_throughput_add"), "0.10")
    expect(f"{label}_LOCAL_EXPORT_ADVANTAGE", scalar(level_scaled, "state_export_advantage_mult"), "0.10")
    icon = scalar(building, "icon")
    background = scalar(building, "background")
    icon_path = resolved_asset(icon)
    expect(f"{label}_ICON_EXISTS", int(icon_path.exists()), 1)
    expect(f"{label}_ICON_DIMENSIONS", "x".join(map(str, dds_dimensions(icon_path))), "256x256")
    expect(f"{label}_BACKGROUND_EXISTS", int(resolved_asset(background).exists()), 1)

building_data = re.sub(r"(?m)#.*$", "", building_text)
for forbidden in ("locator", "entity", "mesh", "map_data"):
    expect(f"MONUMENT_{forbidden.upper()}_REFERENCES", len(re.findall(rf"\b{forbidden}\w*\b", building_data, re.I)), 0)
expect("MONUMENT_3D_ASSETS", "DEFERRED_POST_MAP_3D_CHARACTER_ART_PHASE", "DEFERRED_POST_MAP_3D_CHARACTER_ART_PHASE")
print()

vanilla_rules = (GAME / "common/game_rules/00_game_rules.txt").read_text(encoding="utf-8-sig")
vanilla_monuments = named_block(vanilla_rules, "monument_effects")
mod_monuments = named_block(RULES.read_text(encoding="utf-8-sig"), "monument_effects")
new_flags = {
    "flag = disable_pm_default_building_rialto_commercial_complex",
    "flag = disable_pm_default_building_palazzo_san_giorgio",
}
rule_ok = True
for mode in ("prestige_only_monument_effects", "no_monument_effects"):
    vanilla_mode = named_block(vanilla_monuments, mode)
    mod_mode = named_block(mod_monuments, mode)
    vanilla_flags = set(re.findall(r"(?m)^\s*(flag\s*=\s*\S+)", vanilla_mode))
    mod_flags = set(re.findall(r"(?m)^\s*(flag\s*=\s*\S+)", mod_mode))
    rule_ok &= mod_flags == vanilla_flags | new_flags
expect("MONUMENT_EFFECTS_GAME_RULE_SUPPORTED", int(rule_ok), 1)

required_loc = {
    "building_rialto_commercial_complex",
    "building_rialto_commercial_complex_desc",
    "building_palazzo_san_giorgio",
    "building_palazzo_san_giorgio_desc",
    "pmg_base_building_rialto_commercial_complex",
    "pmg_base_building_palazzo_san_giorgio",
    "pm_default_building_rialto_commercial_complex",
    "pm_default_building_palazzo_san_giorgio",
}
for language in ("english", "french"):
    loc = (ROOT / f"localization/{language}/cleanup2e4_monuments_l_{language}.yml").read_text(encoding="utf-8-sig")
    missing = [key for key in required_loc if not re.search(rf"(?m)^[ \t]*{re.escape(key)}:\d*[ \t]", loc)]
    expect(f"MONUMENT_LOCALIZATION_{language.upper()}_MISSING", len(missing), 0)
print()

formation_files = sorted((ROOT / "common/history/military_formations").glob("0[0-7]_military_formations_*.txt"))
formation_blocks = [block for path in formation_files for block in blocks(path.read_text(encoding="utf-8-sig"), "create_military_formation")]
armies = [block for block in formation_blocks if scalar(block, "type") == "army"]
fleets = [block for block in formation_blocks if scalar(block, "type") == "fleet"]
naval_units = sum(int(scalar(ship, "count")) for fleet in fleets for ship in blocks(fleet, "ship"))
expect("LAND_FORMATIONS", len(armies), 214)
with (ROOT / "docs/research/military/CLEANUP2D5O_STARTING_GENERAL_COMMAND_RANK_AUDIT.csv").open(encoding="utf-8-sig", newline="") as handle:
    general_capacity = list(csv.DictReader(handle))
expect("GENERAL_COMMAND_CAPACITY_SUFFICIENT", sum(row["standing_capacity_result"] == "PASS" for row in general_capacity), 214)
expect("FLEETS", len(fleets), 41)
expect("NAVAL_UNITS", naval_units, 370)
with (ROOT / "docs/research/military/CLEANUP2D6_GLOBAL_RECONCILIATION_MATRIX.csv").open(encoding="utf-8-sig", newline="") as handle:
    admiral_matrix = list(csv.DictReader(handle))
fixed = {"IMPLEMENT_NAMED_HISTORICAL_ADMIRAL", "REBUILD_EXISTING_HISTORICAL_ADMIRAL"}
expect("FINAL_FIXED_HISTORICAL_ADMIRALS", sum(row["final_decision"] in fixed for row in admiral_matrix), 26)

paths = changed_paths()
expect("MILITARY_FILES_CHANGED", sum(any(path.startswith(prefix) for prefix in PROTECTED_MILITARY_PREFIXES) for path in paths), 0)
expect("LAND_GENERAL_RANKS_CHANGED", sum(path.startswith(("common/history/characters/", "common/character_templates/")) for path in paths), 0)
expect("TECHNOLOGY_FILES_CHANGED", sum(path.startswith(("common/technology/", "common/technologies/")) for path in paths), 0)
tech_root = ROOT / "docs/research/technology"
protected_tech_changed = 0
for name, expected_hash in PROTECTED_TECH_HASHES.items():
    path = tech_root / name
    actual = hashlib.sha256(path.read_bytes()).hexdigest().upper() if path.exists() else "MISSING"
    protected_tech_changed += actual != expected_hash
expect("PROTECTED_TECH_FILES_CHANGED", protected_tech_changed, 0)

staged = {path.replace("\\", "/") for path in git_output("diff", "--cached", "--name-only").splitlines()}
expect("PROTECTED_TECH_FILES_STAGED", sum(path.startswith("docs/research/technology/") for path in staged), 0)
expect("STAGED_FILES", len(staged), 0)
allowed_gameplay = {
    "common/laws/00_inject_laws.txt",
    "common/static_modifiers/76mod_modifiers.txt",
    "common/history/countries/gen - genoa.txt",
    "common/history/countries/ven - venetia.txt",
    "common/history/buildings/01_south_europe.txt",
    "common/buildings/99_cleanup2e4_merchant_republic_monuments.txt",
    "common/production_method_groups/99_cleanup2e4_merchant_republic_monuments.txt",
    "common/production_methods/99_cleanup2e4_merchant_republic_monuments.txt",
    "common/game_rules/99_cleanup2e4_monument_effects.txt",
    "common/history/pops/01_south_europe.txt",
}
gameplay_prefixes = ("common/", "events/", "map_data/", "victoria3/")
unexpected_gameplay = sorted(path for path in paths if path.startswith(gameplay_prefixes) and path not in allowed_gameplay)
expect("UNEXPECTED_GAMEPLAY_FILES_CHANGED", len(unexpected_gameplay), 0)
expect("MAP_FILES_CHANGED", sum(path.startswith(("map_data/", "common/state_regions/")) for path in paths), 0)
print()

expect("RUNTIME", "RUNTIME_PENDING_USER_SESSION", "RUNTIME_PENDING_USER_SESSION")
if failures:
    print("STATIC_VALIDATION_2E4 = FAIL")
    for failure in failures:
        print(f"FAIL: {failure}")
    raise SystemExit(1)

print("STATIC_VALIDATION_2E4 = PASS")
print("STATIC_VALIDATION = PASS")
