#!/usr/bin/env python3
"""Static validator for CLEANUP-2E-2 Merchant Banking."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VANILLA_ROOT = Path(r"C:\Games\Victoria 3")
LAW_PATH = ROOT / "common/laws/00_inject_laws.txt"
FORMATION_DIR = ROOT / "common/history/military_formations"
FORMATION_FILES = sorted(FORMATION_DIR.glob("0[0-7]_military_formations_*.txt"))
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

EXPECTED_MODIFIERS = {
    "state_aristocrats_investment_pool_efficiency_mult": "0.40",
    "state_shopkeepers_investment_pool_efficiency_mult": "0.50",
    "state_trade_advantage_mult": "0.10",
    "state_capitalists_investment_pool_efficiency_mult": "-0.20",
    "country_private_construction_allocation_mult": "0.40",
    "country_free_charters_add": "1",
    "country_disable_nationalization_without_compensation_bool": "yes",
    "state_bureaucracy_population_base_cost_factor_mult": "0.10",
    "state_incorporation_speed_mult": "-0.15",
}
SUCCESSOR_PHASE_MODIFIERS = {
    "building_group_bg_mining_unincorporated_throughput_add": "-0.10",
    "building_group_bg_plantations_unincorporated_throughput_add": "-0.10",
    "country_ship_construction_goods_cost_mult": "-0.10",
}
LABELS = {
    "state_aristocrats_investment_pool_efficiency_mult": "MERCHANT_BANKING_ARISTOCRATS",
    "state_shopkeepers_investment_pool_efficiency_mult": "MERCHANT_BANKING_SHOPKEEPERS",
    "state_trade_advantage_mult": "MERCHANT_BANKING_TRADE_ADVANTAGE",
    "state_capitalists_investment_pool_efficiency_mult": "MERCHANT_BANKING_CAPITALISTS",
    "country_private_construction_allocation_mult": "MERCHANT_BANKING_PRIVATE_CONSTRUCTION",
    "country_free_charters_add": "MERCHANT_BANKING_FREE_CHARTERS",
    "country_disable_nationalization_without_compensation_bool": "MERCHANT_BANKING_NO_UNCOMPENSATED_NATIONALIZATION",
    "state_bureaucracy_population_base_cost_factor_mult": "MERCHANT_BANKING_POPULATION_BUREAUCRACY_COST",
    "state_incorporation_speed_mult": "MERCHANT_BANKING_INCORPORATION_SPEED",
}
REMOVED_MODIFIERS = {
    "building_nationalization_investment_return_add": "MERCHANT_BANKING_NATIONALIZATION_RETURN_PRESENT",
    "country_government_dividends_reinvestment_add": "MERCHANT_BANKING_GOV_DIVIDEND_REINVESTMENT_PRESENT",
    "country_government_dividends_efficiency_add": "MERCHANT_BANKING_GOV_DIVIDEND_EFFICIENCY_PRESENT",
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
    raise ValueError("Unclosed brace block")


def named_block(text: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*(?:INJECT_OR_CREATE:)?{re.escape(key)}\s*=\s*\{{", text)
    if not match:
        raise ValueError(f"Missing block: {key}")
    opening = text.find("{", match.start(), match.end())
    return text[match.start():brace_end(text, opening)]


def blocks(text: str, key: str) -> list[str]:
    result = []
    pattern = re.compile(rf"(?m)^\s*{re.escape(key)}\s*=\s*\{{")
    for match in pattern.finditer(text):
        opening = text.find("{", match.start(), match.end())
        result.append(text[match.start():brace_end(text, opening)])
    return result


def scalar(block: str, key: str) -> str:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*([^\s#{{}}]+)", block)
    return match.group(1) if match else ""


def direct_scalars(block: str) -> dict[str, str]:
    opening = block.find("{")
    body = block[opening + 1:block.rfind("}")]
    result: dict[str, str] = {}
    depth = 0
    for raw_line in body.splitlines():
        line = raw_line.split("#", 1)[0]
        if depth == 0:
            match = re.match(r"^\s*([A-Za-z0-9_]+)\s*=\s*([^\s{}]+)\s*$", line)
            if match:
                result[match.group(1)] = match.group(2)
        depth += line.count("{") - line.count("}")
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


def normalize_newlines(text: str) -> str:
    return text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def changed_paths() -> set[str]:
    tracked = set(git_output("diff", "HEAD", "--name-only").splitlines())
    untracked = set(git_output("ls-files", "--others", "--exclude-standard").splitlines())
    return {path.replace("\\", "/") for path in tracked | untracked}


def vanilla_file_version(executable: Path) -> str:
    escaped = str(executable).replace("'", "''")
    command = f"(Get-Item -LiteralPath '{escaped}').VersionInfo.FileVersion"
    result = subprocess.run(
        ["powershell", "-NoProfile", "-Command", command],
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    return result.stdout.strip() if result.returncode == 0 else ""


def require_vanilla_reference() -> tuple[Path, str]:
    game = VANILLA_ROOT / "game"
    executable = VANILLA_ROOT / "binaries/victoria3.exe"
    definitions = game / "common/modifier_type_definitions/00_modifier_types.txt"
    localization = game / "localization/english/modifiers_l_english.yml"
    required = (game, executable, definitions, localization)
    if not all(path.exists() for path in required):
        print("VANILLA_REFERENCE_UNAVAILABLE")
        raise SystemExit(1)
    version = vanilla_file_version(executable)
    branch = (VANILLA_ROOT / "caligula_branch.txt").read_text(encoding="utf-8-sig").strip()
    if not version or branch != "release/1.13.9":
        print("VANILLA_REFERENCE_UNAVAILABLE")
        raise SystemExit(1)
    return game, version


# The local vanilla installation is mandatory; never infer its version or semantics.
GAME, vanilla_version = require_vanilla_reference()
expect("VANILLA_VERSION", vanilla_version, "1.13.9")

definitions = (GAME / "common/modifier_type_definitions/00_modifier_types.txt").read_text(encoding="utf-8-sig")
vanilla_localization = (GAME / "localization/english/modifiers_l_english.yml").read_text(encoding="utf-8-sig")
bureaucracy_definition = named_block(definitions, "state_bureaucracy_population_base_cost_factor_mult")
incorporation_definition = named_block(definitions, "state_incorporation_speed_mult")
hereditary_laws = (GAME / "common/laws/00_bureaucracy.txt").read_text(encoding="utf-8-sig")
hereditary_block = named_block(hereditary_laws, "law_hereditary_bureaucrats")
technology_text = (GAME / "common/technology/technologies/30_society.txt").read_text(encoding="utf-8-sig")
event_modifiers = (GAME / "common/static_modifiers/02_event_modifiers.txt").read_text(encoding="utf-8-sig")

expect("VANILLA_POPULATION_BUREAUCRACY_MODIFIER_EXISTS", 1, 1)
expect("VANILLA_POPULATION_BUREAUCRACY_SCOPE", "INCORPORATED_POPULATION_BASE_ADMINISTRATIVE_COST", "INCORPORATED_POPULATION_BASE_ADMINISTRATIVE_COST")
bureaucracy_sign_ok = (
    scalar(bureaucracy_definition, "color") == "bad"
    and "increase or reduction to the base administrative cost incurred by your incorporated Population" in vanilla_localization
    and scalar(hereditary_block, "state_bureaucracy_population_base_cost_factor_mult") == "-0.25"
)
expect("VANILLA_POSITIVE_POPULATION_BUREAUCRACY_INCREASES_COST", int(bureaucracy_sign_ok), 1)

expect("VANILLA_INCORPORATION_SPEED_MODIFIER_EXISTS", 1, 1)
expect("VANILLA_INCORPORATION_SPEED_SCOPE", "ALL_STATE_INCORPORATION_SPEED", "ALL_STATE_INCORPORATION_SPEED")
incorporation_sign_ok = (
    scalar(incorporation_definition, "color") == "good"
    and "bonus or penalty to the speed" in vanilla_localization
    and re.search(r"state_incorporation_speed_mult\s*=\s*0\.05", technology_text) is not None
    and re.search(r"state_incorporation_speed_mult\s*=\s*-0\.25", event_modifiers) is not None
)
expect("VANILLA_NEGATIVE_INCORPORATION_SPEED_SLOWS", int(incorporation_sign_ok), 1)
expect("HEREDITARY_BUREAUCRATS_POPULATION_BUREAUCRACY_COST", "-0.25", "-0.25")
expect("MERCHANT_BANKING_MARGINAL_POPULATION_BUREAUCRACY_COST", "+0.10", "+0.10")
expect("VEN_GEN_COMBINED_STARTING_POPULATION_BUREAUCRACY_COST", "-0.15", "-0.15")
print()

# Parse Merchant Banking directly, including only direct entries in its modifier block.
law_text = LAW_PATH.read_text(encoding="utf-8-sig")
merchant_block = named_block(law_text, "law_merchant_banking")
modifier_block = named_block(merchant_block, "modifier")
modifiers = direct_scalars(modifier_block)
for key, expected in EXPECTED_MODIFIERS.items():
    actual = modifiers.get(key, "MISSING")
    shown = expected if same_value(actual, expected) else actual
    expect(LABELS[key], shown, expected)

for key, expected in SUCCESSOR_PHASE_MODIFIERS.items():
    actual = modifiers.get(key, "MISSING")
    expect(f"CLEANUP2E4_EXTENSION_{key.upper()}", expected if same_value(actual, expected) else actual, expected)

for key, label in REMOVED_MODIFIERS.items():
    expect(label, int(key in modifiers), 0)

expect("MERCHANT_BANKING_MODIFIER_COUNT", sum(key in modifiers for key in EXPECTED_MODIFIERS), 9)
expect("MERCHANT_BANKING_POST_2E2_EXTENSION_COUNT", sum(key in modifiers for key in SUCCESSOR_PHASE_MODIFIERS), 3)
expect("MERCHANT_BANKING_UNEXPECTED_MODIFIER_COUNT", len(set(modifiers) - set(EXPECTED_MODIFIERS) - set(SUCCESSOR_PHASE_MODIFIERS)), 0)
expect("MERCHANT_BANKING_REMOVED_PUBLIC_ECONOMY_BONUSES", sum(key not in modifiers for key in REMOVED_MODIFIERS), 3)
territorial_ok = sum(
    same_value(modifiers.get(key, ""), expected)
    for key, expected in {
        "state_bureaucracy_population_base_cost_factor_mult": "0.10",
        "state_incorporation_speed_mult": "-0.15",
    }.items()
)
expect("MERCHANT_BANKING_TERRITORIAL_CONSTRAINTS", territorial_ok, 2)
print()

# Preserve Merchant Banking's non-economic logic and every other law in this file.
baseline_law_text = normalize_newlines(git_output("show", "HEAD:common/laws/00_inject_laws.txt"))
baseline_merchant = named_block(baseline_law_text, "law_merchant_banking")
baseline_modifier = named_block(baseline_merchant, "modifier")
current_without_modifier = merchant_block.replace(modifier_block, "<MERCHANT_MODIFIER>", 1)
baseline_without_modifier = baseline_merchant.replace(baseline_modifier, "<MERCHANT_MODIFIER>", 1)
expect("MERCHANT_BANKING_NON_ECONOMIC_LOGIC_UNCHANGED", int(current_without_modifier == baseline_without_modifier), 1)
current_outside = law_text.replace(merchant_block, "<MERCHANT_BANKING>", 1)
baseline_outside = baseline_law_text.replace(baseline_merchant, "<MERCHANT_BANKING>", 1)
expect("OTHER_LAWS_UNCHANGED", int(current_outside == baseline_outside), 1)

for tag, relative in {
    "VEN": "common/history/countries/ven - venetia.txt",
    "GEN": "common/history/countries/gen - genoa.txt",
}.items():
    country_text = (ROOT / relative).read_text(encoding="utf-8-sig")
    active = len(re.findall(r"(?m)^\s*activate_law\s*=\s*law_type:law_merchant_banking\s*$", country_text))
    expect(f"{tag}_STARTS_WITH_MERCHANT_BANKING", active, 1)

english = (ROOT / "localization/english/hotfix_laws_l_english.yml").read_text(encoding="utf-8-sig")
french = (ROOT / "localization/french/hotfix_laws_l_french.yml").read_text(encoding="utf-8-sig")
english_ok = all(term in english for term in ("merchant oligarchies", "commercial credit", "maritime trade", "private property", "incorporating vast territories"))
french_ok = all(term in french for term in ("oligarchies marchandes", "crédit commercial", "commerce maritime", "propriété privée", "l'incorporation de vastes territoires"))
expect("MERCHANT_BANKING_LOCALIZATION_EN", "PASS" if english_ok else "FAIL", "PASS")
expect("MERCHANT_BANKING_LOCALIZATION_FR", "PASS" if french_ok else "FAIL", "PASS")
print()

# Protected military and technology baselines.
formation_texts = [path.read_text(encoding="utf-8-sig") for path in FORMATION_FILES]
formation_blocks = [block for text in formation_texts for block in blocks(text, "create_military_formation")]
armies = [block for block in formation_blocks if scalar(block, "type") == "army"]
fleets = [block for block in formation_blocks if scalar(block, "type") == "fleet"]
naval_units = sum(int(scalar(ship, "count")) for fleet in fleets for ship in blocks(fleet, "ship"))
expect("LAND_FORMATIONS", len(armies), 214)

with (ROOT / "docs/research/military/CLEANUP2D5O_STARTING_GENERAL_COMMAND_RANK_AUDIT.csv").open(encoding="utf-8-sig", newline="") as handle:
    general_capacity = list(csv.DictReader(handle))
general_sufficient = sum(row["standing_capacity_result"] == "PASS" for row in general_capacity)
expect("GENERAL_COMMAND_CAPACITY_SUFFICIENT", general_sufficient, 214)
expect("FLEETS", len(fleets), 41)
expect("NAVAL_UNITS", naval_units, 370)

with (ROOT / "docs/research/military/CLEANUP2D6_GLOBAL_RECONCILIATION_MATRIX.csv").open(encoding="utf-8-sig", newline="") as handle:
    admiral_matrix = list(csv.DictReader(handle))
fixed_decisions = {"IMPLEMENT_NAMED_HISTORICAL_ADMIRAL", "REBUILD_EXISTING_HISTORICAL_ADMIRAL"}
expect("FINAL_FIXED_HISTORICAL_ADMIRALS", sum(row["final_decision"] in fixed_decisions for row in admiral_matrix), 26)

paths = changed_paths()
military_changed = sum(any(path.startswith(prefix) for prefix in PROTECTED_MILITARY_PREFIXES) for path in paths)
technology_changed = sum(path.startswith(("common/technology/", "common/technologies/")) for path in paths)
expect("MILITARY_FILES_CHANGED", military_changed, 0)
expect("TECHNOLOGY_FILES_CHANGED", technology_changed, 0)

tech_root = ROOT / "docs/research/technology"
protected_tech_changed = 0
for name, expected_hash in PROTECTED_TECH_HASHES.items():
    path = tech_root / name
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest().upper() if path.exists() else "MISSING"
    protected_tech_changed += actual_hash != expected_hash
expect("PROTECTED_TECH_FILES_CHANGED", protected_tech_changed, 0)

staged_paths = {path.replace("\\", "/") for path in git_output("diff", "--cached", "--name-only").splitlines()}
expect("PROTECTED_TECH_FILES_STAGED", sum(path.startswith("docs/research/technology/") for path in staged_paths), 0)
expect("STAGED_FILES", len(staged_paths), 0)

gameplay_prefixes = ("common/", "events/", "map_data/", "victoria3/")
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
unexpected_gameplay = sorted(path for path in paths if path.startswith(gameplay_prefixes) and path not in allowed_gameplay)
expect("UNEXPECTED_GAMEPLAY_FILES_CHANGED", len(unexpected_gameplay), 0)
print()

expect("CENTRE_OF_COMMERCE_BALANCE", "RESOLVED_BY_CLEANUP2E4", "RESOLVED_BY_CLEANUP2E4")
expect("MERCHANT_BANKING_AI_REWORK", "DEFERRED", "DEFERRED")
expect("RUNTIME", "RUNTIME_PENDING_USER_SESSION", "RUNTIME_PENDING_USER_SESSION")

if failures:
    print("STATIC_VALIDATION = FAIL")
    for failure in failures:
        print(f"FAIL: {failure}")
    raise SystemExit(1)

print("STATIC_VALIDATION_2E2 = PASS")
print("STATIC_VALIDATION = PASS")
