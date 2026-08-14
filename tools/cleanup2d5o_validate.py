#!/usr/bin/env python3
"""Static audit and validator for CLEANUP-2D-5O starting general capacity."""

from __future__ import annotations

import argparse
import csv
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game")
BASELINE = "bbeb8b7"
FORM_DIR = ROOT / "common/history/military_formations"
FORM_FILES = sorted(FORM_DIR.glob("0[0-7]_military_formations_*.txt"))
GLOBAL_MATRIX = ROOT / "docs/research/military/CLEANUP2D5_GLOBAL_RECONCILIATION_MATRIX.csv"
IMPLEMENTATION_MATRIX = ROOT / "docs/research/military/GENERALS_1776_IMPLEMENTATION_MATRIX.csv"
DEFAULT_CSV = ROOT / "docs/research/military/CLEANUP2D5O_STARTING_GENERAL_COMMAND_RANK_AUDIT.csv"


def fail(message: str) -> None:
    raise AssertionError(message)


def check(condition: bool, label: str, detail: object = "") -> None:
    if not condition:
        fail(f"{label}: {detail}")
    suffix = f" = {detail}" if detail != "" else ""
    print(f"PASS {label}{suffix}")


def active_blocks(text: str, needle: str) -> list[str]:
    """Return balanced active blocks beginning with *needle*."""
    result: list[str] = []
    for match in re.finditer(re.escape(needle), text):
        line_start = text.rfind("\n", 0, match.start()) + 1
        if text[line_start:match.start()].lstrip().startswith("#"):
            continue
        opening = text.find("{", match.start())
        depth = 0
        for pos in range(opening, len(text)):
            if text[pos] == "{":
                depth += 1
            elif text[pos] == "}":
                depth -= 1
                if depth == 0:
                    result.append(text[match.start() : pos + 1])
                    break
    return result


def normalized(block: str) -> str:
    return re.sub(r"\s+", " ", block).strip()


def field(block: str, key: str) -> str | None:
    match = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*([^\s#]+)", block)
    return match.group(1) if match else None


def git_text(revision: str, path: Path) -> str:
    relative = path.relative_to(ROOT).as_posix()
    data = subprocess.check_output(["git", "show", f"{revision}:{relative}"], cwd=ROOT)
    return data.decode("utf-8-sig")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


@dataclass(frozen=True)
class Rank:
    key: str
    value: int
    general_limit: int


def parse_ranks(game: Path) -> tuple[dict[str, Rank], int, int]:
    rank_path = game / "common/commander_ranks/00_commander_ranks.txt"
    define_path = game / "common/defines/00_defines.txt"
    if not rank_path.is_file() or not define_path.is_file():
        fail(f"Vanilla rank/define files not found below {game}")
    rank_text = rank_path.read_text(encoding="utf-8-sig")
    define_text = define_path.read_text(encoding="utf-8-sig")
    ranks: dict[str, Rank] = {}
    for key in re.findall(r"(?m)^(commander_rank_[A-Za-z0-9_]+)\s*=\s*\{", rank_text):
        block = active_blocks(rank_text, f"{key} = {{")[0]
        value_match = re.search(r"(?m)^\s*rank_value\s*=\s*(\d+)", block)
        general_blocks = active_blocks(block, "general_modifier = {")
        limit_match = (
            re.search(r"(?m)^\s*character_command_limit_add\s*=\s*(-?\d+)", general_blocks[0])
            if general_blocks
            else None
        )
        if value_match and limit_match:
            ranks[key] = Rank(key, int(value_match.group(1)), int(limit_match.group(1)))
    start = int(re.search(r"(?m)^\s*COMMANDER_START_RANK\s*=\s*(\d+)", define_text).group(1))
    ruler = int(re.search(r"(?m)^\s*RULER_COMMANDER_START_RANK\s*=\s*(\d+)", define_text).group(1))
    return ranks, start, ruler


def rank_for_value(ranks: dict[str, Rank], value: int) -> Rank:
    matches = [rank for rank in ranks.values() if rank.value == value]
    if len(matches) != 1:
        fail(f"Expected exactly one commander rank with rank_value={value}, found {len(matches)}")
    return matches[0]


def character_blocks(texts: dict[Path, str]) -> dict[str, tuple[Path, str]]:
    found: dict[str, tuple[Path, str]] = {}
    for path, text in texts.items():
        for block in active_blocks(text, "create_character = {"):
            scope = field(block, "save_scope_as")
            if scope and re.fullmatch(r"cleanup2d(?:4_general|5_reuse)_\d{3}", scope):
                if scope in found:
                    fail(f"Duplicate character scope {scope}")
                found[scope] = (path, block)
    return found


def formation_data(texts: dict[Path, str]) -> dict[str, tuple[Path, int, int, str]]:
    result: dict[str, tuple[Path, int, int, str]] = {}
    for path, text in texts.items():
        for block in active_blocks(text, "create_military_formation = {"):
            if field(block, "type") != "army":
                continue
            name = field(block, "name")
            if not name:
                fail(f"Army without name in {path}")
            standing = conscripts = 0
            for unit in active_blocks(block, "combat_unit = {"):
                count = int(field(unit, "count") or fail(f"Unit without count in {name}"))
                if field(unit, "service_type") == "conscript":
                    conscripts += count
                else:
                    standing += count
            result[name] = (path, standing, conscripts, block)
    return result


def resolve_rank(block: str, ranks: dict[str, Rank], start_value: int, ruler_value: int) -> Rank:
    explicit = field(block, "commander_rank")
    if explicit and explicit != "default":
        if explicit not in ranks:
            fail(f"Unknown explicit commander rank {explicit}")
        return ranks[explicit]
    return rank_for_value(ranks, ruler_value if field(block, "ruler") == "yes" else start_value)


def explicit_traits(block: str) -> list[str]:
    trait_blocks = active_blocks(block, "traits = {")
    if not trait_blocks:
        return []
    body = trait_blocks[0].split("{", 1)[1].rsplit("}", 1)[0]
    return re.findall(r"(?m)^\s*([A-Za-z0-9_]+)\s*$", re.sub(r"#.*", "", body))


def trait_command_modifiers(game: Path) -> dict[str, tuple[float, float]]:
    result: dict[str, tuple[float, float]] = {}
    trait_dir = game / "common/character_traits"
    for path in sorted(trait_dir.glob("*.txt")):
        text = path.read_text(encoding="utf-8-sig")
        # Trait keys are the only unindented database blocks in these files.
        for match in re.finditer(r"(?m)^([A-Za-z0-9_]+)\s*=\s*\{", text):
            key = match.group(1)
            blocks = active_blocks(text[match.start() :], f"{key} = {{")
            if not blocks:
                continue
            block = blocks[0]
            add = sum(float(value) for value in re.findall(r"character_command_limit_add\s*=\s*(-?[0-9.]+)", block))
            mult = sum(float(value) for value in re.findall(r"character_command_limit_mult\s*=\s*(-?[0-9.]+)", block))
            result[key] = (add, mult)
    return result


def deterministic_capacity(rank: Rank, traits: list[str], trait_mods: dict[str, tuple[float, float]]) -> tuple[int, str]:
    add = sum(trait_mods.get(trait, (0.0, 0.0))[0] for trait in traits)
    mult = sum(trait_mods.get(trait, (0.0, 0.0))[1] for trait in traits)
    # All audited deterministic modifiers are zero. int() documents the observed
    # whole-battalion UI representation if a future explicit modifier is added.
    capacity = int((rank.general_limit + add) * (1.0 + mult))
    details = "NONE" if add == 0 and mult == 0 else f"add={add:g};mult={mult:g}"
    return capacity, details


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--game", type=Path, default=DEFAULT_GAME)
    parser.add_argument("--write-csv", action="store_true")
    parser.add_argument("--csv", type=Path, default=DEFAULT_CSV)
    args = parser.parse_args()

    check(len(FORM_FILES) == 8, "FORMATION_FILES", len(FORM_FILES))
    current_form_texts = {path: path.read_text(encoding="utf-8-sig") for path in FORM_FILES}
    baseline_form_texts = {path: git_text(BASELINE, path) for path in FORM_FILES}
    current_formations = formation_data(current_form_texts)
    baseline_formations = formation_data(baseline_form_texts)
    check(len(current_formations) == 214, "LAND_FORMATIONS", len(current_formations))
    check(set(current_formations) == set(baseline_formations), "FORMATION_SET_UNCHANGED", 214)
    check(sum(data[1] for data in current_formations.values()) == 2557, "STANDING_BATTALIONS", 2557)
    check(sum(data[2] for data in current_formations.values()) == 1705, "POTENTIAL_CONSCRIPTS", 1705)

    # The only allowed military-history mutation is commander rank. Unit blocks,
    # including standing battalions and potential conscripts, must be byte-content equivalent.
    current_units = [normalized(block) for text in current_form_texts.values() for block in active_blocks(text, "combat_unit = {")]
    baseline_units = [normalized(block) for text in baseline_form_texts.values() for block in active_blocks(text, "combat_unit = {")]
    check(current_units == baseline_units, "COMBAT_UNITS_UNCHANGED", len(current_units))
    current_rank_declarations = sum(len(re.findall(r"(?m)^\s*commander_rank\s*=", text)) for text in current_form_texts.values())
    baseline_rank_declarations = sum(len(re.findall(r"(?m)^\s*commander_rank\s*=", text)) for text in baseline_form_texts.values())
    check(baseline_rank_declarations == 0, "BASELINE_EXPLICIT_FORMATION_RANKS", 0)
    check(current_rank_declarations == 29, "FINAL_EXPLICIT_FORMATION_RANKS", 29)

    global_rows = read_csv(GLOBAL_MATRIX)
    implementation_rows = read_csv(IMPLEMENTATION_MATRIX)
    check(len(global_rows) == 214 and len(implementation_rows) == 214, "SOURCE_MATRIX_ROWS", 214)
    check(sum(bool(row["final_historical_character"]) for row in global_rows) == 79, "HISTORICAL_GENERALS", 79)
    check(sum(not bool(row["final_historical_character"]) for row in global_rows) == 135, "PROCEDURAL_GENERALS", 135)
    check(sum(row["reuse_existing_character"] == "YES" for row in global_rows) == 20, "REUSED_RULER_GENERALS", 20)

    history_paths = sorted((ROOT / "common/history").rglob("*.txt"))
    current_history = {path: path.read_text(encoding="utf-8-sig") for path in history_paths}
    baseline_history = {path: git_text(BASELINE, path) for path in history_paths}
    current_characters = character_blocks(current_history)
    baseline_characters = character_blocks(baseline_history)
    ranks, start_value, ruler_value = parse_ranks(args.game)
    trait_mods = trait_command_modifiers(args.game)
    regular_ranks = sorted((rank for rank in ranks.values() if 1 <= rank.value <= 5), key=lambda rank: rank.value)

    audit: list[dict[str, object]] = []
    promotions = historical_promotions = procedural_promotions = 0
    for implementation, global_row in zip(implementation_rows, global_rows):
        record_id = implementation["record_id"]
        check(record_id == global_row["record_id"], f"MATRIX_ORDER_{record_id}")
        number = int(record_id[-3:])
        scope = f"cleanup2d5_reuse_{number:03d}" if global_row["reuse_existing_character"] == "YES" else implementation["character_scope_after"]
        check(scope in current_characters and scope in baseline_characters, f"CHARACTER_SCOPE_{record_id}")
        current_path, current_block = current_characters[scope]
        _, baseline_block = baseline_characters[scope]
        without_rank = lambda block: re.sub(r"(?m)^\s*commander_rank\s*=\s*[^\s#]+\s*(?:#.*)?$", "", block)
        check(normalized(without_rank(current_block)) == normalized(without_rank(baseline_block)), f"CHARACTER_PROFILE_UNCHANGED_{record_id}")
        formation_name = global_row["formation"]
        check(formation_name in current_formations, f"FORMATION_{record_id}")
        formation_path, standing, conscripts, _ = current_formations[formation_name]

        before_rank = resolve_rank(baseline_block, ranks, start_value, ruler_value)
        final_rank = resolve_rank(current_block, ranks, start_value, ruler_value)
        traits = explicit_traits(current_block)
        before_capacity, modifier_detail = deterministic_capacity(before_rank, traits, trait_mods)
        final_capacity, final_modifier_detail = deterministic_capacity(final_rank, traits, trait_mods)
        check(modifier_detail == final_modifier_detail, f"DETERMINISTIC_MODIFIER_UNCHANGED_{record_id}")

        sufficient_before = before_capacity >= standing
        if sufficient_before:
            action = "KEEP_CURRENT_RANK"
            check(final_rank.key == before_rank.key, f"NO_UNNECESSARY_PROMOTION_{record_id}")
        else:
            candidates = []
            for rank in regular_ranks:
                candidate_capacity, _ = deterministic_capacity(rank, traits, trait_mods)
                if rank.value > before_rank.value and candidate_capacity >= standing:
                    candidates.append(rank)
            check(bool(candidates), f"SUFFICIENT_HIGHER_RANK_EXISTS_{record_id}")
            expected = candidates[0]
            action = f"PROMOTE_TO_{expected.key.upper()}"
            check(final_rank.key == expected.key, f"MINIMAL_PROMOTION_{record_id}", final_rank.key)
            promotions += 1
            if global_row["final_historical_character"]:
                historical_promotions += 1
            else:
                procedural_promotions += 1

        check(final_capacity >= standing, f"FINAL_CAPACITY_{record_id}", f"{final_capacity}>={standing}")
        audit.append(
            {
                "record_id": record_id,
                "tag": global_row["tag"],
                "formation": formation_name,
                "source_file": formation_path.name,
                "character_scope": scope,
                "general_category": "HISTORICAL" if global_row["final_historical_character"] else "PROCEDURAL",
                "reused_ruler_general": global_row["reuse_existing_character"],
                "starting_standing_battalions": standing,
                "potential_conscript_battalions": conscripts,
                "rank_before": before_rank.key,
                "base_command_limit_before": before_rank.general_limit,
                "explicit_traits": "|".join(traits) if traits else "NONE",
                "deterministic_command_limit_modifier": modifier_detail,
                "reliable_command_limit_before": before_capacity,
                "status_before": "SUFFICIENT" if sufficient_before else "INSUFFICIENT",
                "action": action,
                "final_rank": final_rank.key,
                "final_base_command_limit": final_rank.general_limit,
                "final_reliable_command_limit": final_capacity,
                "standing_capacity_result": "PASS",
                "conscripts_used_to_select_rank": "NO",
                "character_source_file": str(current_path.relative_to(ROOT)).replace("\\", "/"),
            }
        )

    check(len(audit) == 214, "AUDIT_ROWS", len(audit))
    check(promotions == 29, "PROMOTIONS", promotions)
    check(historical_promotions == 26, "HISTORICAL_PROMOTIONS", historical_promotions)
    check(procedural_promotions == 3, "PROCEDURAL_PROMOTIONS", procedural_promotions)
    check(sum(row["reused_ruler_general"] == "YES" and row["action"] != "KEEP_CURRENT_RANK" for row in audit) == 0, "RULER_PROMOTIONS", 0)
    check(sum(row["deterministic_command_limit_modifier"] != "NONE" for row in audit) == 0, "DETERMINISTIC_COMMAND_MODIFIERS", 0)
    check(sum(row["standing_capacity_result"] != "PASS" for row in audit) == 0, "FINAL_FAILURES", 0)

    if args.write_csv:
        args.csv.parent.mkdir(parents=True, exist_ok=True)
        with args.csv.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(audit[0]))
            writer.writeheader()
            writer.writerows(audit)
        print(f"WROTE {args.csv.relative_to(ROOT)} ({len(audit)} rows)")
    else:
        check(args.csv.is_file(), "AUDIT_CSV_EXISTS", args.csv.relative_to(ROOT))
        csv_rows = read_csv(args.csv)
        check(len(csv_rows) == 214, "AUDIT_CSV_ROWS", len(csv_rows))
        expected = [{key: str(value) for key, value in row.items()} for row in audit]
        check(csv_rows == expected, "AUDIT_CSV_CURRENT", 214)

    print("CLEANUP2D5O_STATIC_VALIDATION=PASS")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (AssertionError, OSError, subprocess.CalledProcessError) as error:
        print(f"FAIL {error}", file=sys.stderr)
        raise SystemExit(1)
