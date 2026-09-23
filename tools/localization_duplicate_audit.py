#!/usr/bin/env python3
"""Audit duplicate English/French localization keys without changing text."""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VANILLA = Path(r"C:\Games\Victoria 3\game\localization")
KEY = re.compile(r'^\s*([A-Za-z0-9_.-]+):(?:\d+)?\s+"(.*)"\s*(?:#.*)?$')


def entries(language: str, root: Path = ROOT / "localization", replacement: bool | None = None):
    definitions = defaultdict(list)
    for path in sorted((root / language).rglob("*.yml")):
        if replacement is not None and ("replace" in path.parts) != replacement:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
            match = KEY.match(line)
            if match:
                definitions[match.group(1)].append((path, number, match.group(2)))
    return definitions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--details", action="store_true")
    args = parser.parse_args()
    for language in ("english", "french"):
        regular = entries(language, replacement=False)
        overrides = entries(language, replacement=True)
        vanilla = entries(language, root=VANILLA)
        duplicates = {key: values for key, values in regular.items() if len(values) > 1}
        duplicated_overrides = {key: values for key, values in overrides.items() if len(values) > 1}
        misplaced = {
            key for key in set(regular) & set(vanilla)
            if any(
                mod_path.relative_to(ROOT / "localization" / language)
                != game_path.relative_to(VANILLA / language)
                for mod_path, _, _ in regular[key]
                for game_path, _, _ in vanilla[key]
            )
        }
        pairs = Counter()
        different = 0
        for key, values in duplicates.items():
            if len({value for _, _, value in values}) > 1:
                different += 1
            pairs[tuple(path.name for path, _, _ in values)] += 1
        print(
            f"{language}: regular duplicates={len(duplicates)}, "
            f"replacement duplicates={len(duplicated_overrides)}, "
            f"vanilla collisions outside replace={len(misplaced)}, "
            f"conflicting regular values={different}"
        )
        if misplaced:
            print(f"  Outside replace: {', '.join(sorted(misplaced)[:20])}")
        for pair, count in pairs.most_common():
            print(f"  {count:3} {' | '.join(pair)}")
        if args.details:
            for key, values in sorted(duplicates.items()):
                print(f"  {key}")
                for path, number, value in values:
                    print(f"    {path.name}:{number}: {value}")


if __name__ == "__main__":
    main()
