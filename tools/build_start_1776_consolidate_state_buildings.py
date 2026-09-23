#!/usr/bin/env python3
"""Fold generated building-history overlays into each state's regional block.

The game should see one s:STATE_* block per state and one region_state:* block
per owner within it. This is a mechanical migration: create_building bodies are
copied without changing their levels, ownership, or production methods.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path

import build_start_1776_world_apply as world


HISTORY = world.HISTORY
OVERLAY_PREFIXES = ("97", "98", "99")
REGIONAL_FOR_NEW = {
    "s:STATE_CENTRAL_HIGHLANDS": "09_central_asia.txt",
    "s:STATE_NORTHERN_BALUCHISTAN": "09_central_asia.txt",
    "s:STATE_PERSIAN_KURDISTAN": "08_middle_east.txt",
    "s:STATE_QUETTA": "09_central_asia.txt",
    "s:STATE_WEST_SAHARA": "03_north_africa.txt",
}
PREFERRED_FOR_OLD_DUPLICATES = {
    "s:STATE_BREST": "02_east_europe.txt",
    "s:STATE_JETISY": "09_central_asia.txt",
}


def state_blocks(raws: dict[Path, str]):
    grouped = defaultdict(list)
    for path, raw in raws.items():
        for state_id, start, end in world.block_spans(raw, r"s:STATE_[A-Za-z0-9_]+", 1):
            grouped[state_id].append((path, start, end, raw[start:end]))
    return grouped


def child_blocks(text: str):
    return world.block_spans(text, r"region_state:[A-Za-z0-9_]+", 1)


def splice_inside(block: str, extra: str) -> str:
    closing = block.rfind("}")
    if closing < 0:
        raise ValueError("Block has no closing brace")
    indentation = re.search(r"(?m)^([ \t]*)\}", block[: closing + 1].splitlines(keepends=True)[-1])
    indent = indentation.group(1) if indentation else ""
    return block[:closing].rstrip() + "\n" + extra.strip("\n") + "\n" + indent + block[closing:]


def combine_state(parts: list[str]) -> str:
    combined = parts[0]
    for additional in parts[1:]:
        for owner, start, end in child_blocks(additional):
            region = additional[start:end]
            matches = [item for item in child_blocks(combined) if item[0] == owner]
            if len(matches) > 1:
                raise ValueError(f"Duplicate owner {owner} within combined state")
            if matches:
                _, existing_start, existing_end = matches[0]
                existing = combined[existing_start:existing_end]
                body = region[region.find("{") + 1 : region.rfind("}")]
                replacement = splice_inside(existing, body)
                combined = combined[:existing_start] + replacement + combined[existing_end:]
            else:
                combined = splice_inside(combined, region)
    return combined


def semantic_snapshot():
    _, placements = world.all_placements(HISTORY)
    return Counter(
        (
            row.state,
            row.owner,
            row.building,
            row.level,
            row.pms,
            re.sub(r"\s+", "", world.catalog_tools.clean_comments(row.text)),
        )
        for row in placements
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    raws = {path: path.read_text(encoding="utf-8-sig") for path in sorted(HISTORY.glob("*.txt"))}
    grouped = state_blocks(raws)
    duplicates = {key: parts for key, parts in grouped.items() if len(parts) > 1}
    print(f"States: {len(grouped)}; repeated state blocks: {len(duplicates)}")

    replacements = defaultdict(list)
    for state_id, parts in grouped.items():
        regional = [part for part in parts if not part[0].name.startswith(OVERLAY_PREFIXES)]
        if state_id in PREFERRED_FOR_OLD_DUPLICATES:
            chosen_name = PREFERRED_FOR_OLD_DUPLICATES[state_id]
        elif regional:
            chosen_name = regional[0][0].name
        else:
            chosen_name = REGIONAL_FOR_NEW[state_id]
        primary_path = HISTORY / chosen_name
        existing_primary = next((part for part in parts if part[0] == primary_path), None)
        ordered = ([existing_primary] if existing_primary else []) + [part for part in parts if part != existing_primary]
        combined = combine_state([part[3] for part in ordered])
        if existing_primary:
            replacements[primary_path].append((existing_primary[1], existing_primary[2], combined))
        else:
            outer = world.block_spans(raws[primary_path], "BUILDINGS", 0)
            if len(outer) != 1:
                raise ValueError(f"Expected one BUILDINGS wrapper in {primary_path}")
            insert_at = outer[0][2] - 1
            replacements[primary_path].append((insert_at, insert_at, "\n" + combined + "\n"))
        for path, start, end, _ in parts:
            if existing_primary and (path, start, end) == existing_primary[:3]:
                continue
            replacements[path].append((start, end, ""))

    updated = {}
    for path, edits in replacements.items():
        raw = raws[path]
        for start, end, replacement in sorted(edits, key=lambda item: item[0], reverse=True):
            raw = raw[:start] + replacement + raw[end:]
        world.catalog_tools.brace_maps(world.catalog_tools.clean_comments(raw))
        updated[path] = raw
    overlay_paths = [path for path in raws if path.name.startswith(OVERLAY_PREFIXES)]
    for path in overlay_paths:
        if world.block_spans(updated.get(path, raws[path]), r"s:STATE_[A-Za-z0-9_]+", 1):
            raise ValueError(f"Overlay still has state blocks: {path}")
    print(f"Files to rewrite: {len(updated)}; generated overlays to remove: {len(overlay_paths)}")
    if not args.apply:
        return

    before = semantic_snapshot()
    for path, raw in updated.items():
        if path not in overlay_paths:
            path.write_text(raw, encoding="utf-8", newline="")
    for path in overlay_paths:
        path.unlink()
    after = semantic_snapshot()
    if before != after:
        raise AssertionError(f"Building placements changed: removed={sum((before-after).values())}, added={sum((after-before).values())}")
    final = state_blocks({path: path.read_text(encoding="utf-8-sig") for path in HISTORY.glob("*.txt")})
    repeated = [key for key, parts in final.items() if len(parts) > 1]
    owner_duplicates = [
        (key, owner)
        for key, parts in final.items()
        for owner, count in Counter(region[0] for region in child_blocks(parts[0][3])).items()
        if count > 1
    ]
    if repeated or owner_duplicates:
        raise AssertionError(f"Repeated states={repeated[:5]}, owners={owner_duplicates[:5]}")
    print(f"PASS: {len(final)} unique state blocks, no duplicate owner blocks, all {sum(after.values())} placements preserved")


if __name__ == "__main__":
    main()
