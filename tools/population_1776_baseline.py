#!/usr/bin/env python3
"""Read the current 1776 pop history without changing game data."""

from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

import build_start_1776_research_input_pack as parser


ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "common/history/pops"


def rows():
    for path in sorted(HISTORY.glob("*.txt")):
        for state in parser.named_blocks(path, r"s:STATE_[A-Za-z0-9_]+", 1):
            for region in parser.subblocks(state, r"region_state:[A-Za-z0-9_]+"):
                pops = parser.subblocks(region, "create_pop")
                total = sum(int(parser.scalar(pop.text, "size")) for pop in pops)
                yield {
                    "file": path.name,
                    "state": state.object_id.removeprefix("s:"),
                    "owner": region.object_id.removeprefix("region_state:"),
                    "population": total,
                    "groups": len(pops),
                }


def main():
    data = list(rows())
    owners = Counter()
    for row in data:
        owners[row["owner"]] += row["population"]
    print(f"states={len(data)}, tags={len(owners)}, population={sum(owners.values()):,}")
    for tag, count in owners.most_common(40):
        print(f"{tag:8} {count:>12,}")
    output = ROOT / "docs/research/population/POPULATION_1776_BASELINE.csv"
    if output.exists():
        raise SystemExit(f"Frozen pre-pass baseline already exists; refusing to overwrite: {output}")
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "state", "owner", "population", "groups"])
        writer.writeheader()
        writer.writerows(data)
    print(output)


if __name__ == "__main__":
    main()
