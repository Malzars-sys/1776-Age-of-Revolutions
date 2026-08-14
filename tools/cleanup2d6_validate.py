#!/usr/bin/env python3
"""Static validator for CLEANUP-2D-6L global historical admirals."""

from __future__ import annotations

import csv
import hashlib
import os
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "d91bbdbdc5778e259fa9648eca5e0df8d710c30d"
DOCS = ROOT / "docs/research/military"
FORMATION_DIR = ROOT / "common/history/military_formations"
FORMATION_FILES = sorted(FORMATION_DIR.glob("0[0-7]_military_formations_*.txt"))
FIXED_DECISIONS = {
    "IMPLEMENT_NAMED_HISTORICAL_ADMIRAL",
    "REBUILD_EXISTING_HISTORICAL_ADMIRAL",
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def expect(label: str, actual: object, expected: object) -> None:
    print(f"{label} = {actual}")
    if actual != expected:
        failures.append(f"{label}: expected {expected!r}, got {actual!r}")


def brace_end(text: str, opening: int) -> int:
    depth = 0
    for pos in range(opening, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return pos + 1
    raise ValueError("Unclosed brace block")


def blocks(text: str, key: str) -> list[str]:
    result = []
    for match in re.finditer(rf"(?m)^\s*{re.escape(key)}\s*=\s*\{{", text):
        opening = text.find("{", match.start(), match.end())
        result.append(text[match.start():brace_end(text, opening)])
    return result


def scalar(block: str, key: str) -> str:
    found = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*([^\s#{{}}]+)", block)
    return found.group(1) if found else ""


def git_blob(relative: str) -> str:
    data = subprocess.check_output(["git", "show", f"{BASELINE}:{relative}"], cwd=ROOT)
    return data.decode("utf-8-sig")


def find_game_path() -> Path:
    candidates = []
    if os.environ.get("VICTORIA3_GAME_PATH"):
        candidates.append(Path(os.environ["VICTORIA3_GAME_PATH"]))
    candidates.extend(
        [
            Path(r"C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game"),
            Path(r"C:\Program Files\Steam\steamapps\common\Victoria 3\game"),
        ]
    )
    for candidate in candidates:
        if (candidate / "common/commander_ranks/00_commander_ranks.txt").exists():
            return candidate
    raise FileNotFoundError("Victoria 3 game path not found; set VICTORIA3_GAME_PATH")


# Audits are outputs, not hand-maintained tables. Regenerate before validating.
build = subprocess.run(
    [sys.executable, str(ROOT / "tools/cleanup2d6_build_audits.py")],
    cwd=ROOT,
    text=True,
    capture_output=True,
)
if build.returncode:
    print(build.stdout)
    print(build.stderr, file=sys.stderr)
    raise SystemExit(build.returncode)

matrix = read_csv(DOCS / "CLEANUP2D6_GLOBAL_RECONCILIATION_MATRIX.csv")
profiles = read_csv(DOCS / "CLEANUP2D6_GLOBAL_HISTORICAL_ADMIRAL_PROFILES.csv")
capacity = read_csv(DOCS / "CLEANUP2D6_ADMIRAL_COMMAND_RANK_CAPACITY_AUDIT.csv")
duplicate = read_csv(DOCS / "CLEANUP2D6_DUPLICATE_PERSON_REUSE_AUDIT.csv")
birth = read_csv(DOCS / "CLEANUP2D6_BIRTHDATA_IMPLEMENTATION_AUDIT.csv")

texts = {path.name: path.read_text(encoding="utf-8-sig") for path in FORMATION_FILES}
all_text = "\n".join(texts.values())

fleet_blocks = []
army_blocks = []
character_blocks = []
for text in texts.values():
    for block in blocks(text, "create_military_formation"):
        if re.search(r"(?m)^\s*type\s*=\s*fleet\s*$", block):
            fleet_blocks.append(block)
        elif re.search(r"(?m)^\s*type\s*=\s*army\s*$", block):
            army_blocks.append(block)
    character_blocks.extend(blocks(text, "create_character"))

naval_units = 0
for fleet in fleet_blocks:
    naval_units += sum(int(scalar(ship, "count")) for ship in blocks(fleet, "ship"))

baseline_fleets = []
for path in FORMATION_FILES:
    baseline = git_blob(path.relative_to(ROOT).as_posix())
    baseline_fleets.extend(
        block for block in blocks(baseline, "create_military_formation")
        if re.search(r"(?m)^\s*type\s*=\s*fleet\s*$", block)
    )

def without_scope(block: str) -> str:
    block = re.sub(r"(?m)^\s*save_scope_as\s*=\s*[^\s{}]+\s*\n?", "", block)
    block = re.sub(r"#.*", "", block)
    return re.sub(r"\s+", " ", block).strip()

fleet_structure_changes = sum(
    without_scope(current) != without_scope(baseline)
    for current, baseline in zip(fleet_blocks, baseline_fleets)
) + abs(len(fleet_blocks) - len(baseline_fleets))

expect("CURRENT_FLEETS", len(fleet_blocks), 41)
expect("NAVAL_UNITS", naval_units, 370)
expect("FLEET_STRUCTURE_CHANGES", fleet_structure_changes, 0)
print()

ids = [row["nav_record_id"] for row in matrix]
unique_fleets = {(row["tag"], row["source_file"], row["formation"]) for row in matrix}
expect("GLOBAL_RECONCILIATION_ROWS", len(matrix), 41)
expect("GLOBAL_RECONCILIATION_UNIQUE_FLEETS", len(unique_fleets), 41)
expect("RESEARCH_COVERED_FLEETS", sum(bool(row["final_decision"]) for row in matrix), 41)
expect("RESEARCH_GAP_FLEETS", sum(not bool(row["final_decision"]) for row in matrix), 0)
if ids != [f"NAV1776-{number:03d}" for number in range(1, 42)]:
    failures.append("Global matrix IDs are not NAV1776-001..041 in canonical order")
print()

decision_counts = Counter(row["final_decision"] for row in matrix)
fixed_rows = [row for row in matrix if row["final_decision"] in FIXED_DECISIONS]
expect("FINAL_FIXED_HISTORICAL_ADMIRALS", len(fixed_rows), 26)
expect("IMPLEMENT_NAMED_HISTORICAL_ADMIRALS", decision_counts["IMPLEMENT_NAMED_HISTORICAL_ADMIRAL"], 25)
expect("REBUILT_EXISTING_HISTORICAL_ADMIRALS", decision_counts["REBUILD_EXISTING_HISTORICAL_ADMIRAL"], 1)
expect("KEEP_NO_FIXED_STARTING_ADMIRAL", decision_counts["KEEP_NO_FIXED_STARTING_ADMIRAL"], 12)
expect("COLLECTIVE_COMMAND_NO_SINGLE_ADMIRAL", decision_counts["COLLECTIVE_COMMAND_NO_SINGLE_ADMIRAL"], 1)
expect("DEFER_STRUCTURE_REWORK", decision_counts["DEFER_STRUCTURE_REWORK"], 2)
expect("GLOBAL_HISTORICAL_ADMIRAL_PROFILE_ROWS", len(profiles), 26)
print()

# Concrete implementation scopes and transfers.
admiral_scopes = []
for block in character_blocks:
    template = scalar(block, "template")
    if re.search(r"(?m)^\s*is_admiral\s*=\s*yes\s*$", block) or template == "MARATH_anandrao_dhulap":
        scope = scalar(block, "save_scope_as")
        if scope:
            admiral_scopes.append(scope)

transfer_pairs = []
for match in re.finditer(r"(?m)^\s*scope:([^\s{}]+)\s*=\s*\{", all_text):
    opening = all_text.find("{", match.start(), match.end())
    block = all_text[match.start():brace_end(all_text, opening)]
    target = re.search(r"transfer_to_formation\s*=\s*scope:([^\s{}]+)", block)
    if target and match.group(1) in admiral_scopes:
        transfer_pairs.append((match.group(1), target.group(1)))

fleet_scopes = {scalar(block, "save_scope_as") for block in fleet_blocks if scalar(block, "save_scope_as")}
source_counts = Counter(source for source, _ in transfer_pairs)
target_counts = Counter(target for _, target in transfer_pairs)
orphan = sum(source not in admiral_scopes or target not in fleet_scopes for source, target in transfer_pairs)
orphan += sum(scope not in source_counts for scope in admiral_scopes)

expect("FIXED_STARTING_ADMIRAL_ASSIGNMENTS", len(transfer_pairs), 26)
expect("FORMATIONS_WITH_MULTIPLE_FIXED_ADMIRALS", sum(count > 1 for count in target_counts.values()), 0)
expect("DUPLICATE_HISTORICAL_PERSONS", sum(row["duplicate_detected"] != "NO" for row in duplicate), 0)
expect("ORPHAN_ADMIRAL_TRANSFERS", orphan, 0)
expect("DUPLICATE_CHARACTER_SCOPES", sum(count > 1 for count in Counter(admiral_scopes).values()), 0)
expect("DUPLICATE_PERSON_REUSE_AUDIT_ROWS", len(duplicate), 26)
print()

expect("STARTING_GUAN_TIANPEI", len(re.findall(r"(?m)^\s*first_name\s*=\s*Tianpei\s*$", all_text)), 0)
expect("STARTING_CHEN_HUACHENG", len(re.findall(r"(?m)^\s*first_name\s*=\s*Huacheng\s*$", all_text)), 0)
expect("SPANISH_PROCEDURAL_STARTING_ADMIRALS", len(re.findall(r"spanishnavy[12](?:_gen)?", all_text)), 0)
expect("ANANDRAO_DHULAP_INSTANCES", len(re.findall(r"(?m)^\s*template\s*=\s*MARATH_anandrao_dhulap\s*$", all_text)), 1)
print()

non_day_precisions = {"YEAR_ONLY", "YEAR", "APPROXIMATE_YEAR", "MONTH_ONLY", "CIRCA_YEAR / RANGE", "TERMINUS_ANTE_QUEM", "UNKNOWN"}
fake_dates = sum(row["source_precision"] in non_day_precisions and bool(row["implemented_birth_date"]) for row in birth)
baptism = sum(row["baptism_as_birth_date"] != "NO" for row in birth)
expect("BIRTHDATA_IMPLEMENTATION_AUDIT_ROWS", len(birth), 26)
expect("FAKE_EXACT_BIRTH_DATES", fake_dates, 0)
expect("BAPTISM_AS_BIRTH_DATE", baptism, 0)
print()

expect("ADMIRAL_COMMAND_CAPACITY_ROWS", len(capacity), 41)
expect("ADMIRAL_COMMAND_CAPACITY_SUFFICIENT", sum(row["capacity_sufficient"] == "YES" for row in capacity), 41)
expect("ADMIRAL_COMMAND_CAPACITY_INSUFFICIENT", sum(row["capacity_sufficient"] != "YES" for row in capacity), 0)
rank_counts = Counter(row["final_rank"] for row in capacity)
expect("NAVAL_RANK_2_ASSIGNMENTS", rank_counts["commander_rank_2"], 3)
expect("NAVAL_RANK_3_ASSIGNMENTS", rank_counts["commander_rank_3"], 1)
expect("NAVAL_RANK_4_ASSIGNMENTS", rank_counts["commander_rank_4"], 0)
expect("NAVAL_RANK_5_ASSIGNMENTS", rank_counts["commander_rank_5"], 0)
print()

# Army formation and general blocks must be byte-equivalent to d91bbdb.
baseline_armies = []
baseline_generals = []
for path in FORMATION_FILES:
    relative = path.relative_to(ROOT).as_posix()
    baseline = git_blob(relative)
    for block in blocks(baseline, "create_military_formation"):
        if re.search(r"(?m)^\s*type\s*=\s*army\s*$", block):
            baseline_armies.append(block)
    for block in blocks(baseline, "create_character"):
        if re.search(r"(?m)^\s*is_general\s*=\s*yes\s*$", block):
            baseline_generals.append(block)

land_changed = 0 if army_blocks == baseline_armies and [b for b in character_blocks if re.search(r"(?m)^\s*is_general\s*=\s*yes\s*$", b)] == baseline_generals else 1
regular_total = 0
conscript_total = 0
for army in army_blocks:
    for unit in blocks(army, "combat_unit"):
        count = int(scalar(unit, "count") or "0")
        if re.search(r"(?m)^\s*service_type\s*=\s*conscript\s*$", unit):
            conscript_total += count
        else:
            regular_total += count

# d91bbdb is the already-passing 2D-5O baseline. The legacy 2D-5O validator
# counts every commander_rank token in formation files and therefore cannot be
# run unchanged after naval ranks are added. Prove preservation directly:
# every army formation and every is_general character block must be byte-equal
# to d91bbdb, with the same 2557/1705 totals. This is stricter for the protected
# land scope than filtering the legacy validator's global token count.
general_sufficient = 214 if land_changed == 0 and len(army_blocks) == 214 and regular_total == 2557 and conscript_total == 1705 else 0

expect("LAND_FORMATIONS", len(army_blocks), 214)
expect("LAND_GENERAL_RANKS_CHANGED_BY_2D6", land_changed, 0)
expect("GENERAL_COMMAND_CAPACITY_SUFFICIENT", general_sufficient, 214)
expect("GENERAL_COMMAND_CAPACITY_INSUFFICIENT", 214 - general_sufficient, 0)
expect("REGULAR_TOTAL", regular_total, 2557)
expect("CONSCRIPT_TOTAL", conscript_total, 1705)
print()

# Protected concurrent technology research remains byte-identical and unstaged.
tech_root = ROOT / "docs/research/technology"
tech_changed = 0
for name, expected_hash in PROTECTED_TECH_HASHES.items():
    path = tech_root / name
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest().upper() if path.exists() else "MISSING"
    if actual_hash != expected_hash:
        tech_changed += 1
staged = subprocess.check_output(["git", "diff", "--cached", "--name-only"], cwd=ROOT, text=True)
expect("PROTECTED_TECH_FILES_CHANGED", tech_changed, 0)
expect("PROTECTED_TECH_FILES_STAGED", sum(line.startswith("docs/research/technology/") for line in staged.splitlines()), 0)
print()

# No raw localization keys and every final person appears once in both languages.
localization_ok = True
for language in ("english", "french"):
    path = ROOT / f"localization/{language}/cleanup2d6_admirals_l_{language}.yml"
    text = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    for row in fixed_rows:
        number = row["nav_record_id"][-3:]
        expected = f'cleanup2d6_name_{number}:0 "{row["final_candidate"]}"'
        localization_ok &= text.count(expected) == 1
    localization_ok &= text.count("cleanup2d6_empty_name:0") == 1
expect("LOCALIZATION_EN_FR", "PASS" if localization_ok else "FAIL", "PASS")

# Validate explicit culture/religion ids against local vanilla definitions.
game = find_game_path()
culture_defs = "\n".join(path.read_text(encoding="utf-8-sig") for path in (game / "common/cultures").glob("*.txt"))
religion_defs = "\n".join(path.read_text(encoding="utf-8-sig") for path in (game / "common/religions").glob("*.txt"))
new_blocks = [block for block in character_blocks if scalar(block, "save_scope_as").startswith("cleanup2d6_admiral_")]
invalid_cultures = 0
invalid_religions = 0
for block in new_blocks:
    culture = scalar(block, "culture")
    religion = scalar(block, "religion")
    if culture.startswith("cu:") and not re.search(rf"(?m)^\s*{re.escape(culture[3:])}\s*=\s*\{{", culture_defs):
        invalid_cultures += 1
    if religion.startswith("rel:") and not re.search(rf"(?m)^\s*{re.escape(religion[4:])}\s*=\s*\{{", religion_defs):
        invalid_religions += 1
if invalid_cultures or invalid_religions:
    failures.append(f"Invalid culture/religion ids: cultures={invalid_cultures} religions={invalid_religions}")

# Forbidden formation files and structures are unchanged from the baseline.
for relative in (
    "common/history/military_formations/02_military_formations_south_america.txt",
    "common/history/military_formations/03_military_formations_north_africa.txt",
    "common/history/military_formations/07_military_formations_subsaharan_africa.txt",
):
    if (ROOT / relative).read_text(encoding="utf-8-sig") != git_blob(relative):
        failures.append(f"Forbidden formation file changed: {relative}")

diff_check = subprocess.run(["git", "diff", "--check"], cwd=ROOT, text=True, capture_output=True)
expect("git diff --check", "PASS" if diff_check.returncode == 0 else "FAIL", "PASS")
expect("GIT_INDEX_EMPTY", "YES" if not staged.strip() else "NO", "YES")
print()

if failures:
    print("STATIC_VALIDATION = FAIL")
    for failure in failures:
        print(f"FAIL: {failure}")
    raise SystemExit(1)

print("STATIC_VALIDATION = PASS")
