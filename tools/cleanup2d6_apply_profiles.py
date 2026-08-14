#!/usr/bin/env python3
"""Apply the closed CLEANUP-2D-6 global admiral profiles.

The transform is deliberately idempotent: authorized gameplay files are rebuilt
from the immutable d91bbdb baseline, then only fleet scopes, admiral creation
blocks, the existing Dhulap template, and dedicated localization are changed.
"""

from __future__ import annotations

import csv
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASELINE = "d91bbdbdc5778e259fa9648eca5e0df8d710c30d"
MATRIX_PATH = ROOT / "docs/research/military/CLEANUP2D6_GLOBAL_RECONCILIATION_MATRIX.csv"
PROFILES_PATH = ROOT / "docs/research/military/CLEANUP2D6_GLOBAL_HISTORICAL_ADMIRAL_PROFILES.csv"

FIXED_DECISIONS = {
    "IMPLEMENT_NAMED_HISTORICAL_ADMIRAL",
    "REBUILD_EXISTING_HISTORICAL_ADMIRAL",
}

# Calendar-bearing exact dates are intentionally explicit. Greig and Senyavin
# retain the documented Old Style date; the source conflict remains in comments
# and in the birth-data audit.
EXACT_BIRTH_DATES = {
    "NAV1776-004": "1712.12.26",
    "NAV1776-005": "1710.3.26",
    "NAV1776-008": "1713.4.17",
    "NAV1776-014": "1735.11.30",
    "NAV1776-015": "1722.10.5",
    "NAV1776-016": "1730.11.24",
    "NAV1776-017": "1715.4.23",
    "NAV1776-018": "1725.12.1",
    "NAV1776-023": "1720.4.25",
    "NAV1776-030": "1718.4.26",
}

# CLEANUP-2D-5 convention: when only a year/circa/month is available, encode a
# conservative age and never manufacture a first day of a month/year.
APPROXIMATE_AGES = {
    "NAV1776-002": (67, "YEAR_ONLY"),
    "NAV1776-010": (59, "APPROXIMATE_YEAR"),
    "NAV1776-011": (72, "YEAR"),
    "NAV1776-012": (57, "APPROXIMATE_YEAR"),
    "NAV1776-022": (39, "MONTH_ONLY"),
    "NAV1776-027": (68, "YEAR"),
    "NAV1776-035": (61, "CIRCA_YEAR / RANGE"),
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


MATRIX = read_csv(MATRIX_PATH)
PROFILES = read_csv(PROFILES_PATH)
PROFILE_BY_ID = {row["nav_record_id"]: row for row in PROFILES}

if len(MATRIX) != 41 or len(PROFILES) != 26:
    raise SystemExit(f"Unexpected canonical inputs: matrix={len(MATRIX)} profiles={len(PROFILES)}")
if len(PROFILE_BY_ID) != 26:
    raise SystemExit("Duplicate nav_record_id in historical-admiral profiles")


def git_blob(relative: str) -> str:
    data = subprocess.check_output(["git", "show", f"{BASELINE}:{relative}"], cwd=ROOT)
    return data.decode("utf-8-sig")


def safe_write(path: Path, desired: str, allowed_existing: set[str], *, bom: bool = False) -> None:
    current = path.read_text(encoding="utf-8-sig") if path.exists() else ""
    if current not in allowed_existing and current != desired:
        raise RuntimeError(f"Refusing to overwrite non-baseline concurrent changes: {path.relative_to(ROOT)}")
    path.write_text(desired, encoding="utf-8-sig" if bom else "utf-8", newline="\n")


def brace_end(text: str, opening_brace: int) -> int:
    depth = 0
    for pos in range(opening_brace, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return pos + 1
    raise ValueError("Unclosed brace block")


def enclosing_block_for_token(text: str, block_key: str, token_pattern: str) -> tuple[int, int]:
    token = re.search(token_pattern, text, re.M)
    if not token:
        raise ValueError(f"Token not found: {token_pattern}")
    starts = list(re.finditer(rf"(?m)^\s*{re.escape(block_key)}\s*=\s*\{{", text[: token.start()]))
    if not starts:
        raise ValueError(f"No {block_key} block encloses {token_pattern}")
    start = starts[-1].start()
    opening = text.find("{", starts[-1].start(), starts[-1].end())
    end = brace_end(text, opening)
    if end < token.end():
        raise ValueError(f"Wrong {block_key} block selected for {token_pattern}")
    return start, end


def country_span(text: str, tag: str) -> tuple[int, int]:
    match = re.search(rf"(?m)^\s*c:{re.escape(tag)}\s+\?=\s*\{{", text)
    if not match:
        raise ValueError(f"Country block not found: {tag}")
    opening = text.find("{", match.start(), match.end())
    return match.start(), brace_end(text, opening)


def formation_span(text: str, tag: str, formation: str) -> tuple[int, int]:
    c_start, c_end = country_span(text, tag)
    country = text[c_start:c_end]
    candidates: list[tuple[int, int]] = []
    for match in re.finditer(r"(?m)^\s*create_military_formation\s*=\s*\{", country):
        opening = country.find("{", match.start(), match.end())
        end = brace_end(country, opening)
        block = country[match.start():end]
        name = re.search(r"(?m)^\s*name\s*=\s*([^\s{}]+)", block)
        if name and name.group(1) == formation:
            candidates.append((c_start + match.start(), c_start + end))
    if len(candidates) != 1:
        raise ValueError(f"Expected one {tag}/{formation} formation, found {len(candidates)}")
    return candidates[0]


def remove_scoped_character(text: str, scope: str) -> str:
    start, end = enclosing_block_for_token(
        text,
        "create_character",
        rf"^\s*save_scope_as\s*=\s*{re.escape(scope)}\s*$",
    )
    text = text[:start] + text[end:]
    match = re.search(rf"(?m)^\s*scope:{re.escape(scope)}\s*=\s*\{{", text)
    if not match:
        raise ValueError(f"Transfer scope not found: {scope}")
    opening = text.find("{", match.start(), match.end())
    end = brace_end(text, opening)
    return text[: match.start()] + text[end:]


def remove_formation_scope(text: str, tag: str, formation: str) -> str:
    start, end = formation_span(text, tag, formation)
    block = text[start:end]
    block, count = re.subn(r"(?m)^\s*save_scope_as\s*=\s*[^\s{}]+\s*\n?", "", block, count=1)
    if count != 1:
        raise ValueError(f"Expected one obsolete formation scope on {tag}/{formation}")
    return text[:start] + block + text[end:]


def profile_lines(record_id: str) -> list[str]:
    profile = PROFILE_BY_ID[record_id]
    lines: list[str] = []
    culture = profile["culture_recommendation"]
    religion = profile["religion_recommendation"]
    home = profile["mapped_v3_birth_state"]

    if culture.startswith("cu:"):
        lines.append(f"\t\t\tculture = {culture}")
    else:
        lines.append("\t\t\tculture = primary_culture # TECHNICAL_GAMEPLAY_FALLBACK_NOT_HISTORICAL_CLAIM")
    if religion.startswith("rel:"):
        lines.append(f"\t\t\treligion = {religion}")
    if home.startswith("STATE_"):
        lines.append(f"\t\t\thome_region = {home}")

    source_value = profile["birth_date_source_value"]
    precision = profile["birth_date_precision"]
    lines.append(f"\t\t\t# Birth evidence: {source_value}; precision: {precision}")
    if record_id in EXACT_BIRTH_DATES:
        lines.append(f"\t\t\tbirth_date = {EXACT_BIRTH_DATES[record_id]}")
    elif record_id in APPROXIMATE_AGES:
        age, age_precision = APPROXIMATE_AGES[record_id]
        lines.append(
            f"\t\t\tage = {age} # {age_precision} / supported technical approximation; no fabricated month/day"
        )
    else:
        lines.append("\t\t\t# No exact birth_date or derived age encoded.")
    return lines


def admiral_block(row: dict[str, str], fleet_scope: str) -> str:
    record_id = row["nav_record_id"]
    number = record_id[-3:]
    candidate = row["final_candidate"]
    lines = [
        f"\t\t# BEGIN CLEANUP-2D-6L {record_id} — {candidate}",
        "\t\tcreate_character = {",
        f"\t\t\tfirst_name = cleanup2d6_name_{number}",
        "\t\t\tlast_name = cleanup2d6_empty_name",
        "\t\t\thistorical = yes",
        *profile_lines(record_id),
        "\t\t\tis_admiral = yes",
        f"\t\t\tcommander_rank = {row['final_rank']}",
        f"\t\t\tsave_scope_as = cleanup2d6_admiral_{number}",
        "\t\t}",
        f"\t\tscope:cleanup2d6_admiral_{number} = {{",
        f"\t\t\ttransfer_to_formation = scope:{fleet_scope}",
        "\t\t}",
        f"\t\t# END CLEANUP-2D-6L {record_id}",
    ]
    return "\n".join(lines)


def implement_row(text: str, row: dict[str, str]) -> str:
    record_id = row["nav_record_id"]
    number = record_id[-3:]
    start, end = formation_span(text, row["tag"], row["formation"])
    block = text[start:end]
    scope_match = re.search(r"(?m)^\s*save_scope_as\s*=\s*([^\s{}]+)", block)
    if scope_match:
        fleet_scope = scope_match.group(1)
    else:
        fleet_scope = f"cleanup2d6_fleet_{number}"
        closing = block.rfind("}")
        block = block[:closing].rstrip() + f"\n\t\t\tsave_scope_as = {fleet_scope}\n\t\t" + block[closing:]
        text = text[:start] + block + text[end:]
        start, end = formation_span(text, row["tag"], row["formation"])

    insertion = "\n\n" + admiral_block(row, fleet_scope)
    return text[:end] + insertion + text[end:]


selected = [row for row in MATRIX if row["final_decision"] in FIXED_DECISIONS]
if len(selected) != 26:
    raise SystemExit(f"Expected 26 fixed historical admirals, found {len(selected)}")

by_source: dict[str, list[dict[str, str]]] = {}
for row in selected:
    if row["nav_record_id"] == "NAV1776-037":
        continue
    by_source.setdefault(row["source_file"], []).append(row)

for source_file, rows in by_source.items():
    relative = f"common/history/military_formations/{source_file}"
    baseline_text = git_blob(relative)
    text = baseline_text

    if source_file == "00_military_formations_europe.txt":
        text = remove_scoped_character(text, "spanishnavy1_gen")
        text = remove_scoped_character(text, "spanishnavy2_gen")
        text = remove_formation_scope(text, "SPA", "cleanup2d3b_spa_naval_1")
        text = remove_formation_scope(text, "SPA", "cleanup2d3b_spa_naval_2")
    if source_file == "06_military_formations_asia.txt":
        text = remove_scoped_character(text, "bohai_gulf_admiral")
        text = remove_scoped_character(text, "guangdong_admiral")

    for row in rows:
        text = implement_row(text, row)
    safe_write(ROOT / relative, text, {baseline_text})

# Rebuild, but do not clone, the one existing historical admiral template.
marath_template = """# Maratha Confederacy - MARATH

MARATH_anandrao_dhulap = {
\tis_admiral = yes
\tfirst_name = Anandrao
\tlast_name = Dhulap
\thistorical = yes
\tculture = cu:marathi
\t# Historical birth date and birth place are unknown.
\t# Age and home region are technical gameplay mappings, not historical claims.
\tage = 40
\thome_region = STATE_BOMBAY
\tcommander_rank = commander_rank_1
\ttraits = {
\t}
}
"""
marath_path = ROOT / "common/character_templates/country_marath.txt"
safe_write(marath_path, marath_template, {git_blob("common/character_templates/country_marath.txt")})


def localization(language: str) -> str:
    lines = [f"l_{language}:", ' cleanup2d6_empty_name:0 ""']
    for row in selected:
        number = row["nav_record_id"][-3:]
        name = row["final_candidate"].replace('"', '\\"')
        lines.append(f' cleanup2d6_name_{number}:0 "{name}"')
    return "\n".join(lines) + "\n"


for language in ("english", "french"):
    path = ROOT / f"localization/{language}/cleanup2d6_admirals_l_{language}.yml"
    safe_write(path, localization(language), {""}, bom=True)

print(f"FIXED_STARTING_ADMIRAL_ASSIGNMENTS={len(selected)}")
print("REBUILT_EXISTING_HISTORICAL_ADMIRALS=1")
print("NEW_HISTORICAL_ADMIRAL_BLOCKS=25")
print("REMOVED_SPANISH_PROCEDURAL_ADMIRALS=2")
print("REMOVED_QING_ANACHRONISTIC_ADMIRALS=2")
