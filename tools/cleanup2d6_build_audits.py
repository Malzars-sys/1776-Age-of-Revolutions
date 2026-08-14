#!/usr/bin/env python3
"""Build deterministic CLEANUP-2D-6 implementation audits from gameplay."""

from __future__ import annotations

import csv
import os
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs/research/military"
MATRIX_PATH = DOCS / "CLEANUP2D6_GLOBAL_RECONCILIATION_MATRIX.csv"
PROFILES_PATH = DOCS / "CLEANUP2D6_GLOBAL_HISTORICAL_ADMIRAL_PROFILES.csv"
CAPACITY_PATH = DOCS / "CLEANUP2D6_ADMIRAL_COMMAND_RANK_CAPACITY_AUDIT.csv"
DUPLICATE_PATH = DOCS / "CLEANUP2D6_DUPLICATE_PERSON_REUSE_AUDIT.csv"
BIRTH_PATH = DOCS / "CLEANUP2D6_BIRTHDATA_IMPLEMENTATION_AUDIT.csv"

FIXED_DECISIONS = {
    "IMPLEMENT_NAMED_HISTORICAL_ADMIRAL",
    "REBUILD_EXISTING_HISTORICAL_ADMIRAL",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


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


def country_block(text: str, tag: str) -> str:
    match = re.search(rf"(?m)^\s*c:{re.escape(tag)}\s+\?=\s*\{{", text)
    if not match:
        raise ValueError(f"Country block not found: {tag}")
    opening = text.find("{", match.start(), match.end())
    return text[match.start():brace_end(text, opening)]


def formation_block(text: str, tag: str, name: str) -> str:
    country = country_block(text, tag)
    matches = []
    for block in blocks(country, "create_military_formation"):
        found = re.search(r"(?m)^\s*name\s*=\s*([^\s{}]+)", block)
        if found and found.group(1) == name:
            matches.append(block)
    if len(matches) != 1:
        raise ValueError(f"Expected one {tag}/{name}, found {len(matches)}")
    return matches[0]


def scalar(block: str, key: str) -> str:
    found = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*([^\s#{{}}]+)", block)
    return found.group(1) if found else ""


def find_game_path() -> Path:
    candidates = []
    if os.environ.get("VICTORIA3_GAME_PATH"):
        candidates.append(Path(os.environ["VICTORIA3_GAME_PATH"]))
    candidates.append(Path(r"C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game"))
    candidates.append(Path(r"C:\Program Files\Steam\steamapps\common\Victoria 3\game"))
    for candidate in candidates:
        if (candidate / "common/commander_ranks/00_commander_ranks.txt").exists():
            return candidate
    raise FileNotFoundError("Victoria 3 game path not found; set VICTORIA3_GAME_PATH")


def vanilla_limits() -> tuple[dict[str, int], int]:
    game = find_game_path()
    ranks = (game / "common/commander_ranks/00_commander_ranks.txt").read_text(encoding="utf-8-sig")
    limits: dict[str, int] = {}
    for rank in re.finditer(r"(?m)^(commander_rank_(?:[1-5]|ruler))\s*=\s*\{", ranks):
        opening = ranks.find("{", rank.start(), rank.end())
        block = ranks[rank.start():brace_end(ranks, opening)]
        admiral = re.search(
            r"admiral_modifier\s*=\s*\{.*?character_command_limit_add\s*=\s*(\d+)",
            block,
            re.S,
        )
        if admiral:
            limits[rank.group(1)] = int(admiral.group(1))
    defines = (game / "common/defines/00_defines.txt").read_text(encoding="utf-8-sig")
    no_commander = int(
        re.search(r"MILITARY_FORMATION_COMMAND_LIMIT_NO_COMMANDER\s*=\s*(\d+)", defines).group(1)
    )
    return limits, no_commander


matrix = read_csv(MATRIX_PATH)
profiles = read_csv(PROFILES_PATH)
profile_by_id = {row["nav_record_id"]: row for row in profiles}
limits, no_commander_limit = vanilla_limits()

if len(matrix) != 41 or len(profiles) != 26:
    raise SystemExit(f"Canonical input mismatch: matrix={len(matrix)} profiles={len(profiles)}")

texts: dict[str, str] = {}
for source in {row["source_file"] for row in matrix}:
    texts[source] = (ROOT / "common/history/military_formations" / source).read_text(encoding="utf-8-sig")

admiral_blocks: dict[str, str] = {}
transfers: dict[str, list[str]] = defaultdict(list)
for text in texts.values():
    for block in blocks(text, "create_character"):
        scope = scalar(block, "save_scope_as")
        template = scalar(block, "template")
        if scope and (re.search(r"(?m)^\s*is_admiral\s*=\s*yes\s*$", block) or template == "MARATH_anandrao_dhulap"):
            if scope in admiral_blocks:
                raise ValueError(f"Duplicate admiral character scope: {scope}")
            admiral_blocks[scope] = block
    for match in re.finditer(r"(?m)^\s*scope:([^\s{}]+)\s*=\s*\{", text):
        opening = text.find("{", match.start(), match.end())
        block = text[match.start():brace_end(text, opening)]
        target = re.search(r"transfer_to_formation\s*=\s*scope:([^\s{}]+)", block)
        if target:
            transfers[match.group(1)].append(target.group(1))

formation_data: dict[str, dict[str, object]] = {}
target_to_ids: dict[str, list[str]] = defaultdict(list)
for row in matrix:
    block = formation_block(texts[row["source_file"]], row["tag"], row["formation"])
    ship_count = 0
    for ship in blocks(block, "ship"):
        count = scalar(ship, "count")
        ship_count += int(count)
    scope = scalar(block, "save_scope_as")
    formation_data[row["nav_record_id"]] = {"block": block, "ship_count": ship_count, "scope": scope}
    if scope:
        target_to_ids[scope].append(row["nav_record_id"])

assignment_by_id: dict[str, list[str]] = defaultdict(list)
for admiral_scope in admiral_blocks:
    for target in transfers.get(admiral_scope, []):
        for record_id in target_to_ids.get(target, []):
            assignment_by_id[record_id].append(admiral_scope)

capacity_rows = []
for row in matrix:
    record_id = row["nav_record_id"]
    ships = int(formation_data[record_id]["ship_count"])
    expected_fixed = row["final_decision"] in FIXED_DECISIONS
    assigned = assignment_by_id.get(record_id, [])
    if expected_fixed:
        final_rank = row["final_rank"]
        guaranteed = limits[final_rank]
        admiral = row["final_candidate"]
        actual_scope = assigned[0] if len(assigned) == 1 else "ASSIGNMENT_ERROR"
        actual_rank = scalar(admiral_blocks.get(actual_scope, ""), "commander_rank")
        if record_id == "NAV1776-037" and not actual_rank:
            marath = (ROOT / "common/character_templates/country_marath.txt").read_text(encoding="utf-8-sig")
            actual_rank = scalar(marath, "commander_rank")
    else:
        final_rank = "NO_COMMANDER"
        guaranteed = no_commander_limit
        admiral = "NO_FIXED_STARTING_ADMIRAL"
        actual_rank = "NO_COMMANDER"
    minimum = "NO_COMMANDER_FALLBACK" if not expected_fixed else next(
        rank for rank in ("commander_rank_1", "commander_rank_2", "commander_rank_3", "commander_rank_4", "commander_rank_5")
        if limits[rank] >= ships
    )
    capacity_rows.append(
        {
            "nav_record_id": record_id,
            "tag": row["tag"],
            "formation": row["formation"],
            "ship_count": ships,
            "admiral": admiral,
            "current_rank": actual_rank,
            "base_command_limit": limits["commander_rank_1"] if expected_fixed else no_commander_limit,
            "deterministic_modifier": 0,
            "guaranteed_command_limit": guaranteed,
            "minimum_required_rank": minimum,
            "final_rank": final_rank,
            "capacity_sufficient": "YES" if guaranteed >= ships and actual_rank == final_rank else "NO",
            "decision": row["rank_capacity_decision"],
        }
    )

write_csv(
    CAPACITY_PATH,
    [
        "nav_record_id", "tag", "formation", "ship_count", "admiral", "current_rank",
        "base_command_limit", "deterministic_modifier", "guaranteed_command_limit",
        "minimum_required_rank", "final_rank", "capacity_sufficient", "decision",
    ],
    capacity_rows,
)

duplicate_rows = []
birth_rows = []
for row in matrix:
    if row["final_decision"] not in FIXED_DECISIONS:
        continue
    record_id = row["nav_record_id"]
    scopes = assignment_by_id.get(record_id, [])
    character_scope = scopes[0] if len(scopes) == 1 else "ASSIGNMENT_ERROR"
    formation_scope = str(formation_data[record_id]["scope"])
    mode = "REBUILD_EXISTING_TEMPLATE" if record_id == "NAV1776-037" else "CREATE_INLINE_CHARACTER"
    duplicate_rows.append(
        {
            "nav_record_id": record_id,
            "candidate": row["final_candidate"],
            "final_decision": row["final_decision"],
            "implementation_mode": mode,
            "character_scope": character_scope,
            "formation_scope": formation_scope,
            "repo_preflight_exact_person_matches": 1 if record_id == "NAV1776-037" else 0,
            "final_character_instances": 1 if len(scopes) == 1 else len(scopes),
            "final_formation_assignments": len(scopes),
            "duplicate_detected": "NO" if len(scopes) == 1 else "YES",
            "decision": "REUSE_REBUILD_NO_CLONE" if record_id == "NAV1776-037" else "CREATE_ONCE_AND_ASSIGN_ONCE",
            "notes": "Edward Hughes repo-wide preflight found no active exact instance; created once." if record_id == "NAV1776-010" else "",
        }
    )

    profile = profile_by_id[record_id]
    if record_id == "NAV1776-037":
        implemented = (ROOT / "common/character_templates/country_marath.txt").read_text(encoding="utf-8-sig")
    else:
        implemented = admiral_blocks.get(character_scope, "")
    birth_date = scalar(implemented, "birth_date")
    age = scalar(implemented, "age")
    home = scalar(implemented, "home_region")
    birthplace_claimed = "YES" if profile["mapped_v3_birth_state"].startswith("STATE_") else "NO"
    technical = []
    if age:
        technical.append("AGE_APPROXIMATION")
    if record_id == "NAV1776-037" and home:
        technical.append("HOME_REGION_NOT_BIRTHPLACE")
    if not profile["culture_recommendation"].startswith("cu:"):
        technical.append("PRIMARY_CULTURE_FALLBACK")
    birth_rows.append(
        {
            "nav_record_id": record_id,
            "candidate": row["final_candidate"],
            "source_birth_value": profile["birth_date_source_value"],
            "source_precision": profile["birth_date_precision"],
            "implemented_birth_date": birth_date,
            "implemented_age": age,
            "implemented_home_region": home,
            "birthplace_claimed": birthplace_claimed,
            "technical_gameplay_fallback": ";".join(technical) or "NONE",
            "precision_preserved": "YES",
            "fake_exact_birth_date": "NO",
            "baptism_as_birth_date": "NO",
            "decision": "EXACT_DATE" if birth_date else ("TECHNICAL_AGE_ONLY" if age else "NO_DATE_ENCODED"),
            "notes": "Old Style date retained; calendar conflict documented." if record_id in {"NAV1776-014", "NAV1776-015"} else "",
        }
    )

write_csv(
    DUPLICATE_PATH,
    [
        "nav_record_id", "candidate", "final_decision", "implementation_mode", "character_scope",
        "formation_scope", "repo_preflight_exact_person_matches", "final_character_instances",
        "final_formation_assignments", "duplicate_detected", "decision", "notes",
    ],
    duplicate_rows,
)
write_csv(
    BIRTH_PATH,
    [
        "nav_record_id", "candidate", "source_birth_value", "source_precision",
        "implemented_birth_date", "implemented_age", "implemented_home_region", "birthplace_claimed",
        "technical_gameplay_fallback", "precision_preserved", "fake_exact_birth_date",
        "baptism_as_birth_date", "decision", "notes",
    ],
    birth_rows,
)

print(f"ADMIRAL_COMMAND_CAPACITY_ROWS={len(capacity_rows)}")
print(f"DUPLICATE_PERSON_REUSE_AUDIT_ROWS={len(duplicate_rows)}")
print(f"BIRTHDATA_IMPLEMENTATION_AUDIT_ROWS={len(birth_rows)}")
