#!/usr/bin/env python3
"""Static validator for CLEANUP-2E-4B runtime balance correction."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VANILLA_ROOT = Path(r"C:\Games\Victoria 3")
GAME = VANILLA_ROOT / "game"
POP_DIR = ROOT / "common/history/pops"
POP_FILE = POP_DIR / "01_south_europe.txt"
PM_FILE = ROOT / "common/production_methods/99_cleanup2e4_merchant_republic_monuments.txt"
HISTORY_FILE = ROOT / "common/history/buildings/01_south_europe.txt"
AUDIT_POP = ROOT / "docs/research/economy/CLEANUP2E4B_GENOA_POPULATION_SCALING_AUDIT.csv"
AUDIT_WORKFORCE = ROOT / "docs/research/economy/CLEANUP2E4B_MONUMENT_WORKFORCE_AUDIT.csv"

TARGET = 510000
FROZEN_TEXT_HASHES = {
    "common/laws/00_inject_laws.txt": "6182CA45CD89E6651C443C9FAEB7F0BD6DC0D47010B6D950FEF0DA057A6EE560",
    "common/static_modifiers/76mod_modifiers.txt": "93129E82242CFCC28DE3D2D580C6BF8862892DAF4DCAE889A9901F730CD3ACE9",
    "common/history/countries/gen - genoa.txt": "7DF9A5EB273F6C46A4C2215E4D46DEE8ABFFF00869596164CB7ACD23A6992C11",
    "common/history/countries/ven - venetia.txt": "D1D3F31A74AA33FF1CFD9FD3CE9994F22877BEF0E0347287A67FD968562A1E12",
    "common/history/buildings/01_south_europe.txt": "0FCF9897E6978B47D336C766169526175B5858DBD4E56048A0F8220242462F45",
    "common/buildings/99_cleanup2e4_merchant_republic_monuments.txt": "9D4C9E42D185DC30EBEDDCF6086BA991A707E6D280EC802DFE48F34C53C125D4",
    "common/production_method_groups/99_cleanup2e4_merchant_republic_monuments.txt": "1366D7DFC0CB97BC3315D0D49B5F660DBA7F580F60F09DFBFEACCFD500AC1DEC",
    "common/game_rules/99_cleanup2e4_monument_effects.txt": "2655B0D3FA5C4F59337000196A408F6AF748C53103B3EAC67C3D14D3C641C10A",
}
ICON_HASHES = {
    "RIALTO": ("gfx/interface/icons/building_icons/cleanup2e4/building_rialto_commercial_complex.dds", "A314B4B98EB25C1EB722AA9FDFCC1CA92CA1A55F42ADD7A65164BDD374B35156"),
    "SAN_GIORGIO": ("gfx/interface/icons/building_icons/cleanup2e4/building_palazzo_san_giorgio.dds", "7C064501A9B9ACFC32E51F8C0BF5F3910BFCB1D0170FB8274C79D2D20F0DEF31"),
}
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


def keyed_blocks(text: str, key_pattern: str) -> list[tuple[str, str]]:
    result: list[tuple[str, str]] = []
    cursor = 0
    pattern = re.compile(rf"(?m)^[ \t]*({key_pattern})\s*=\s*\{{")
    while match := pattern.search(text, cursor):
        opening = text.find("{", match.start())
        end = brace_end(text, opening)
        result.append((match.group(1), text[match.start():end]))
        cursor = end
    return result


def scalar(text: str, key: str) -> str:
    match = re.search(rf"(?m)^[ \t]*{re.escape(key)}\s*=\s*\"?([^\s\"#}}]+)", text)
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


def normalize(text: str) -> str:
    return text.lstrip("\ufeff").replace("\r\n", "\n").replace("\r", "\n")


def without_gen_regions(text: str) -> str:
    result = normalize(text)
    while region := named_block(result, "region_state:GEN"):
        result = result.replace(region, "<REGION_STATE_GEN>", 1)
    return result


def text_hash(path: Path) -> str:
    return hashlib.sha256(normalize(path.read_text(encoding="utf-8-sig")).encode()).hexdigest().upper()


def git_output(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8")


def pop_rows(texts: dict[str, str], culture_text: str) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source, text in texts.items():
        for state_key, state_block in keyed_blocks(text, r"s:STATE_[A-Z0-9_]+"):
            region = named_block(state_block, "region_state:GEN")
            for pop in blocks(region, "create_pop"):
                values = direct_scalars(pop)
                culture = values["culture"]
                religion = values.get("religion") or scalar(named_block(culture_text, culture), "religion")
                rows.append({
                    "source": source,
                    "state": state_key.removeprefix("s:"),
                    "culture": culture,
                    "religion": religion,
                    "profession": values.get("profession", "unspecified_history_pop"),
                    "size": int(values["size"]),
                })
    return rows


def shares(rows: list[dict[str, object]], field: str) -> dict[str, Decimal]:
    totals: dict[str, int] = defaultdict(int)
    total = sum(int(row["size"]) for row in rows)
    for row in rows:
        totals[str(row[field])] += int(row["size"])
    return {key: Decimal(value) * 100 / Decimal(total) for key, value in totals.items()}


def max_share_drift(before: list[dict[str, object]], after: list[dict[str, object]], field: str) -> Decimal:
    left = shares(before, field)
    right = shares(after, field)
    return max(abs(left.get(key, Decimal(0)) - right.get(key, Decimal(0))) for key in left.keys() | right.keys())


def building_instances(region_block: str, building_type: str) -> list[str]:
    return [block for block in blocks(region_block, "create_building") if scalar(block, "building") == building_type]


def ownership_levels(region_block: str, building_type: str, owner_type: str, tag: str) -> int:
    total = 0
    for created in building_instances(region_block, building_type):
        ownership = named_block(created, "add_ownership")
        for owner in blocks(ownership, owner_type):
            values = direct_scalars(owner)
            if values.get("country") == f"c:{tag}":
                total += int(values.get("levels", 0))
    return total


def pm_workforce(pm: str) -> dict[str, int]:
    scaled = named_block(named_block(pm, "building_modifiers"), "level_scaled")
    result: dict[str, int] = {}
    for key, value in direct_scalars(scaled).items():
        match = re.fullmatch(r"building_employment_(\w+)_add", key)
        if match:
            result[match.group(1)] = int(value)
    return result


if not (GAME.exists() and (VANILLA_ROOT / "caligula_branch.txt").exists()):
    print("VANILLA_REFERENCE_UNAVAILABLE")
    raise SystemExit(1)
expect("VANILLA_BRANCH", (VANILLA_ROOT / "caligula_branch.txt").read_text(encoding="utf-8-sig").strip(), "release/1.13.9")

culture_text = "\n".join(path.read_text(encoding="utf-8-sig") for path in sorted((GAME / "common/cultures").glob("*.txt")))
tracked_pop_paths = [path for path in git_output("ls-files", "common/history/pops/*.txt").splitlines() if path]
current_pop_texts = {path: (ROOT / path).read_text(encoding="utf-8-sig") for path in tracked_pop_paths}
baseline_pop_texts = {path: git_output("show", f"HEAD:{path}") for path in tracked_pop_paths}
before_rows = pop_rows(baseline_pop_texts, culture_text)
after_rows = pop_rows(current_pop_texts, culture_text)
before_total = sum(int(row["size"]) for row in before_rows)
after_total = sum(int(row["size"]) for row in after_rows)
expect("GEN_POPULATION_STATIC_BEFORE", before_total, 463988)
expect("GEN_POPULATION_STATIC_AFTER", after_total, 510000)
expect("GEN_POPULATION_TARGET_MIN", 509500, 509500)
expect("GEN_POPULATION_TARGET_MAX", 510500, 510500)

culture_drift = max_share_drift(before_rows, after_rows, "culture")
religion_drift = max_share_drift(before_rows, after_rows, "religion")
culture_drift_text = f"{culture_drift:.6f}"
religion_drift_text = f"{religion_drift:.6f}"
print(f"GEN_CULTURE_SHARE_DRIFT_MAX_PP = {culture_drift_text}")
print(f"GEN_RELIGION_SHARE_DRIFT_MAX_PP = {religion_drift_text}")
if culture_drift > Decimal("0.20"):
    failures.append("GEN_CULTURE_SHARE_DRIFT_MAX_PP exceeds 0.20")
if religion_drift > Decimal("0.20"):
    failures.append("GEN_RELIGION_SHARE_DRIFT_MAX_PP exceeds 0.20")

factor = Decimal(TARGET) / Decimal(before_total)
expected_sizes = [int((Decimal(int(row["size"])) * factor).quantize(Decimal("1"), rounding=ROUND_HALF_UP)) for row in before_rows]
actual_sizes = [int(row["size"]) for row in after_rows]
same_dimensions = [tuple(row[key] for key in ("source", "state", "culture", "religion", "profession")) for row in before_rows] == [tuple(row[key] for key in ("source", "state", "culture", "religion", "profession")) for row in after_rows]
expect("GEN_POP_SCALING_PROPORTIONAL", "PASS" if same_dimensions and actual_sizes == expected_sizes else "FAIL", "PASS")

ven_or_other_changed = 0
for path in tracked_pop_paths:
    current_without_gen = without_gen_regions(current_pop_texts[path])
    baseline_without_gen = without_gen_regions(baseline_pop_texts[path])
    ven_or_other_changed += current_without_gen != baseline_without_gen
expect("VEN_POPULATION_CHANGED", ven_or_other_changed, 0)

with AUDIT_POP.open(encoding="utf-8-sig", newline="") as handle:
    pop_audit = list(csv.DictReader(handle))
expect("GEN_POPULATION_AUDIT_ROWS", len(pop_audit), 4)
expect("GEN_POPULATION_AUDIT_TOTAL_BEFORE", int(pop_audit[-1]["before_pop"]), before_total)
expect("GEN_POPULATION_AUDIT_TOTAL_AFTER", int(pop_audit[-1]["final_pop"]), after_total)
print()

pm_text = PM_FILE.read_text(encoding="utf-8-sig")
rialto_pm = named_block(pm_text, "pm_default_building_rialto_commercial_complex")
san_pm = named_block(pm_text, "pm_default_building_palazzo_san_giorgio")
rialto_workforce = pm_workforce(rialto_pm)
san_workforce = pm_workforce(san_pm)
rialto_total = sum(rialto_workforce.values())
san_total = sum(san_workforce.values())
expect("RIALTO_CLERKS", rialto_workforce.get("clerks", 0), 500)
expect("RIALTO_SHOPKEEPERS", rialto_workforce.get("shopkeepers", 0), 200)
expect("RIALTO_TOTAL_WORKFORCE", rialto_total, 700)
expect("SAN_GIORGIO_CLERKS", san_workforce.get("clerks", 0), 500)
expect("SAN_GIORGIO_BUREAUCRATS", san_workforce.get("bureaucrats", 0), 100)
expect("SAN_GIORGIO_TOTAL_WORKFORCE", san_total, 600)
expect("RIALTO_TOTAL_WORKFORCE_LE_700", int(rialto_total <= 700), 1)
expect("SAN_GIORGIO_TOTAL_WORKFORCE_LE_700", int(san_total <= 700), 1)
expect("RIALTO_HAS_REAL_EMPLOYMENT", int(rialto_total > 0), 1)
expect("SAN_GIORGIO_HAS_REAL_EMPLOYMENT", int(san_total > 0), 1)

expected_effects = {"building_trade_center_throughput_add": "0.10", "state_export_advantage_mult": "0.10"}
for label, pm in (("RIALTO", rialto_pm), ("SAN_GIORGIO", san_pm)):
    effects = direct_scalars(named_block(named_block(pm, "state_modifiers"), "level_scaled"))
    expect(f"{label}_EFFECTS_UNCHANGED", int(effects == expected_effects), 1)

vanilla_pm_text = (GAME / "common/production_methods/08_monuments.txt").read_text(encoding="utf-8-sig")
references = {
    "pm_default_building_big_ben": {"machinists": 100},
    "pm_default_building_vatican_city": {"clergymen": 500},
    "pm_default_building_forbidden_city": {"bureaucrats": 800, "clergymen": 200},
    "pm_power_bloc_statue_trade_league": {"clerks": 500},
}
reference_ok = all(pm_workforce(named_block(vanilla_pm_text, key)) == expected for key, expected in references.items())
modifier_definitions = "\n".join(path.read_text(encoding="utf-8-sig") for path in sorted((GAME / "common/modifier_type_definitions").glob("*.txt")))
reference_ok &= all(named_block(modifier_definitions, key) for key in ("building_employment_clerks_add", "building_employment_shopkeepers_add", "building_employment_bureaucrats_add"))
expect("VANILLA_MONUMENT_WORKFORCE_REFERENCE_AUDIT", "PASS" if reference_ok else "FAIL", "PASS")
with AUDIT_WORKFORCE.open(encoding="utf-8-sig", newline="") as handle:
    workforce_audit = list(csv.DictReader(handle))
expect("MONUMENT_WORKFORCE_AUDIT_ROWS", len(workforce_audit), 12)
print()

for label, (relative, expected_hash) in ICON_HASHES.items():
    actual_hash = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest().upper()
    expect(f"{label}_ICON_CHANGED", int(actual_hash != expected_hash), 0)

frozen_changed = 0
for relative, expected_hash in FROZEN_TEXT_HASHES.items():
    frozen_changed += text_hash(ROOT / relative) != expected_hash
expect("FROZEN_2E4_FILES_CHANGED_BY_2E4B", frozen_changed, 0)
expect("MERCHANT_BANKING_CHANGED_BY_2E4B", int(text_hash(ROOT / "common/laws/00_inject_laws.txt") != FROZEN_TEXT_HASHES["common/laws/00_inject_laws.txt"]), 0)

history_text = HISTORY_FILE.read_text(encoding="utf-8-sig")
piedmont = named_block(named_block(history_text, "s:STATE_PIEDMONT"), "region_state:GEN")
venetia = named_block(named_block(history_text, "s:STATE_VENETIA"), "region_state:VEN")
istria = named_block(named_block(history_text, "s:STATE_ISTRIA"), "region_state:VEN")
expect("GEN_TRADE_CENTER", ownership_levels(piedmont, "building_trade_center", "building", "GEN"), 6)
expect("VEN_TRADE_CENTER", ownership_levels(venetia, "building_trade_center", "building", "VEN"), 8)
expect("VEN_ISTRIA_TRADE_CENTER", ownership_levels(istria, "building_trade_center", "building", "VEN"), 3)
expect("VEN_GOV_ADMIN", ownership_levels(venetia, "building_government_administration", "country", "VEN"), 5)
expect("GEN_GOV_ADMIN", ownership_levels(piedmont, "building_government_administration", "country", "GEN"), 1)
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

tracked = set(git_output("diff", "HEAD", "--name-only").splitlines())
untracked = set(git_output("ls-files", "--others", "--exclude-standard").splitlines())
changed_paths = {path.replace("\\", "/") for path in tracked | untracked}
military_prefixes = ("common/history/military_formations/", "common/history/characters/", "common/character_templates/", "common/dna_data/")
expect("MILITARY_FILES_CHANGED", sum(any(path.startswith(prefix) for prefix in military_prefixes) for path in changed_paths), 0)
expect("LAND_GENERAL_RANKS_CHANGED", sum(path.startswith(("common/history/characters/", "common/character_templates/")) for path in changed_paths), 0)
expect("TECHNOLOGY_FILES_CHANGED", sum(path.startswith(("common/technology/", "common/technologies/")) for path in changed_paths), 0)
tech_root = ROOT / "docs/research/technology"
protected_tech_changed = 0
for name, expected_hash in PROTECTED_TECH_HASHES.items():
    path = tech_root / name
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest().upper() if path.exists() else "MISSING"
    protected_tech_changed += actual_hash != expected_hash
expect("PROTECTED_TECH_FILES_CHANGED", protected_tech_changed, 0)
staged = {path.replace("\\", "/") for path in git_output("diff", "--cached", "--name-only").splitlines()}
expect("PROTECTED_TECH_FILES_STAGED", sum(path.startswith("docs/research/technology/") for path in staged), 0)
expect("STAGED_FILES", len(staged), 0)
expect("MAP_FILES_CHANGED", sum(path.startswith(("map_data/", "common/state_regions/")) for path in changed_paths), 0)
print()

expect("RUNTIME", "RUNTIME_PENDING_USER_SESSION", "RUNTIME_PENDING_USER_SESSION")
if failures:
    print("STATIC_VALIDATION_2E4B = FAIL")
    for failure in failures:
        print(f"FAIL: {failure}")
    raise SystemExit(1)

print("STATIC_VALIDATION_2E4B = PASS")
print("STATIC_VALIDATION = PASS")
