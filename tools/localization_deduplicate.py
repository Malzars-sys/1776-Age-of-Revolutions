#!/usr/bin/env python3
"""Move vanilla-key overrides to localization/<language>/replace.

Uses an observed game log to identify active vanilla/mod collisions. This
preserves each mod translation exactly while preventing the engine from treating
the override as an ordinary duplicate key.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LOG = Path.home() / "Documents" / "Paradox Interactive" / "Victoria 3" / "logs" / "error.1.log"
LOG_PAIR = re.compile(
    r"Duplicate localization key\. Key '([^']+)' is defined in both '([^']+)' and '([^']+)'\."
)
KEY = re.compile(r'^\s*([A-Za-z0-9_.-]+):(?:\d+)?\s+".*"\s*(?:#.*)?$')


def key_for(line: str) -> str | None:
    match = KEY.match(line)
    return match.group(1) if match else None


def read_text(path: Path) -> tuple[str, bool]:
    data = path.read_bytes()
    return data.decode("utf-8-sig"), data.startswith(b"\xef\xbb\xbf")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log", type=Path, default=DEFAULT_LOG)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    override_keys: dict[Path, set[str]] = defaultdict(set)
    internal_pairs = []
    for line in args.log.read_text(encoding="utf-8", errors="replace").splitlines():
        match = LOG_PAIR.search(line)
        if not match:
            continue
        key, first, second = match.groups()
        paths = [ROOT / first, ROOT / second]
        local = [path for path in paths if path.exists()]
        if len(local) == 1:
            override_keys[local[0]].add(key)
        elif len(local) == 2:
            internal_pairs.append((key, paths[0], paths[1]))

    # Wave C supersedes the older Wave A labels. The two repeated English
    # mechanized-weaving entries in tech3a keep their earlier, fuller wording.
    removal_keys: dict[Path, set[str]] = defaultdict(set)
    self_later = {"mechanized_weaving", "mechanized_weaving_desc"}
    for key, first, second in internal_pairs:
        if first == second and first.name == "tech3a_technology_l_english.yml" and key in self_later:
            continue
        if first.name.startswith("tech7a_wave_a_l_") and second.name.startswith("tech7a_wave_c_l_"):
            removal_keys[first].add(key)
            continue
        raise ValueError(f"Unreviewed internal duplicate: {key} in {first} and {second}")

    files = sorted(set(override_keys) | set(removal_keys) | {
        ROOT / "localization" / "english" / "tech3a_technology_l_english.yml"
    })
    edits: dict[Path, tuple[str, bool]] = {}
    extracted: dict[str, list[tuple[Path, str]]] = defaultdict(list)
    removed_internal = 0
    for path in files:
        raw, bom = read_text(path)
        seen_self = set()
        kept = []
        for line in raw.splitlines(keepends=True):
            key = key_for(line.rstrip("\r\n"))
            if key in override_keys[path]:
                extracted[path.parent.name].append((path, line.rstrip("\r\n")))
                continue
            if key in removal_keys[path]:
                removed_internal += 1
                continue
            if path.name == "tech3a_technology_l_english.yml" and key in self_later:
                if key in seen_self:
                    removed_internal += 1
                    continue
                seen_self.add(key)
            kept.append(line)
        found = {key for _, line in extracted[path.parent.name] if _ == path for key in [key_for(line)]}
        if found != override_keys[path]:
            raise ValueError(f"Missing expected override keys in {path}: {override_keys[path] - found}")
        edits[path] = ("".join(kept), bom)

    output = {}
    for language, lines in extracted.items():
        target = ROOT / "localization" / language / "replace" / f"1776_overrides_l_{language}.yml"
        if target.exists():
            raise ValueError(f"Refusing to overwrite existing replacement file: {target}")
        grouped: dict[Path, list[str]] = defaultdict(list)
        for source, line in lines:
            grouped[source].append(line)
        text = f"l_{language}:\n"
        for source, source_lines in sorted(grouped.items()):
            text += f"\n # From {source.name}\n" + "\n".join(source_lines) + "\n"
        output[target] = text

    print(f"Vanilla overrides to relocate: {sum(map(len, extracted.values()))}")
    print(f"Internal duplicate entries to remove: {removed_internal}")
    print(f"Source files to edit: {len(edits)}; replacement files to create: {len(output)}")
    if not args.apply:
        return

    for path, (text, bom) in edits.items():
        path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + text.encode("utf-8"))
    for path, text in output.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))
    print("PASS: relocated translations retain their original key/value lines")


if __name__ == "__main__":
    main()
