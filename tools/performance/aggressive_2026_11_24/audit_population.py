"""Independently verify conservation and direct culture references in the overlay."""
from collections import Counter
import argparse
import json
from pathlib import Path
import re

from consolidate import BASE, CULTURE_DIR, POP_DIR, TOKENS, effective_files, replacements
from inventory import atom, objects, parse, walk


def populations(files, religions):
    values = Counter()
    counts = 0
    for path in files:
        for state in walk(parse(path.read_text(encoding="utf-8-sig"))):
            if not state.key.startswith("s:STATE_"):
                continue
            for province_owner in state.children():
                for pop in province_owner.children("create_pop"):
                    culture = atom(pop, "culture")
                    religion = atom(pop, "religion") or religions[culture]
                    identity = state.key, province_owner.key, religion, atom(pop, "pop_type")
                    values[identity] += int(atom(pop, "size"))
                    counts += 1
    return values, counts


def check(overlay):
    code = replacements()
    assets = effective_files()
    merged = {name: overlay / name if (overlay / name).is_file() else path
              for name, path in assets.items()}
    old_cultures = objects("common/cultures", BASE)
    new_cultures = {node.key for relative, path in merged.items() if relative.startswith(CULTURE_DIR)
                    for node in parse(path.read_text(encoding="utf-8-sig")) if node.key}
    assert new_cultures == old_cultures.keys() - code.keys()
    religions = {name: atom(node, "religion") for name, node in old_cultures.items()}
    original, original_count = populations((p for name, p in assets.items() if name.startswith(POP_DIR)), religions)
    adjusted, adjusted_count = populations((p for name, p in merged.items() if name.startswith(POP_DIR)), religions)
    assert original == adjusted
    assert original_count > adjusted_count
    typed = re.compile(r"\bcu:(" + "|".join(code) + r")\b")
    broken = {}
    for name, path in merged.items():
        if path.suffix != ".txt":
            continue
        text = path.read_text(encoding="utf-8-sig")
        active = "".join(match[0] for match in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\r\n]*|[^"#]+', text)
                         if not match[0].startswith("#"))
        keys = set(typed.findall(active))
        if keys:
            broken[name] = sorted(keys)
    assert not broken, broken
    print(json.dumps(dict(before=original_count, after=adjusted_count, conserved=sum(original.values()),
                          groups_verified=len(original), removed=len(code), culture_references_broken=broken)))


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("overlay", type=Path)
    check(cli.parse_args().overlay)
