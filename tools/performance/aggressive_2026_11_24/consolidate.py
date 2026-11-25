"""Build a Steam 1.15.2 culture and POP overlay from the checked 1776 scenario."""
from collections import Counter, defaultdict
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re

from inventory import BASE, STEAM, atom, child, objects, parse, walk

SCRIPT_EXTENSIONS = {".txt", ".gui", ".yml"}
ROOTS = ("common", "events", "map_data", "gui", "localization")
POP_DIR = "common/history/pops/"
CULTURE_DIR = "common/cultures/"
CULTURE_HISTORY_DIR = "common/history/cultures/"
LIST_KEYS = {"cultures", "primary_cultures", "possible_cultures"}
TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|#[^\r\n]*|[A-Za-z_][A-Za-z0-9_]*')


def replacements():
    with (Path(__file__).resolve().parents[3] / "docs/reports/performance/AGGRESSIVE_2026_11_24/FUSIONS_CULTURELLES.tsv").open(encoding="utf-8-sig", newline="") as handle:
        return {row["source"]: row["target"] for row in csv.DictReader(handle, delimiter="\t")}


def effective_files():
    metadata = json.loads((BASE / ".metadata/metadata.json").read_text(encoding="utf-8-sig"))
    shadowed = metadata["game_custom_data"]["replace_paths"]
    paths = {}
    for tree in (STEAM, BASE):
        for folder in ROOTS:
            for path in (tree / folder).rglob("*"):
                if path.suffix not in SCRIPT_EXTENSIONS or not path.is_file():
                    continue
                relative = path.relative_to(tree).as_posix()
                if tree == STEAM and any(relative.startswith(prefix + "/") for prefix in shadowed):
                    continue
                paths[relative] = path
    return paths


def splice(text, edits):
    last = len(text)
    fragments = []
    for start, end, new in sorted(edits, key=lambda x: x[0], reverse=True):
        if end > last:
            raise ValueError("Overlapping edits")
        fragments.extend((text[end:last], new))
        last = start
    return text[:last] + "".join(reversed(fragments))


def consolidate_pops(text, code, religions, stats):
    edits = []
    for region in walk(parse(text)):
        if not region.key.startswith("region_state:"):
            continue
        groups = defaultdict(list)
        originals = Counter()
        processed = Counter()
        for node in region.children("create_pop"):
            source = atom(node, "culture")
            old_size = int(atom(node, "size"))
            old_religion = atom(node, "religion") or religions[source]
            old_type = atom(node, "pop_type")
            target = code.get(source, source)
            fields = {n.key for n in node.children()}
            if fields - {"size", "culture", "religion", "pop_type"}:
                raise ValueError(f"Unmodelled POP history fields in {region.key}: {fields}")
            groups[(target, old_religion, old_type)].append((source, node, old_size))
            originals[(old_religion, old_type)] += old_size
        for (target, religion, pop_type), rows in groups.items():
            total = sum(row[2] for row in rows)
            processed[(religion, pop_type)] += total
            stats["size_before"] += total
            stats["size_after"] += total
            stats["groups_before"] += len(rows)
            stats["groups_after"] += 1
            if len(rows) == 1 and rows[0][0] == target:
                continue
            fields = [f"culture = {target}"]
            if religion != religions[target] or rows[0][1].one("religion") is not None:
                fields.append(f"religion = {religion}")
            if pop_type:
                fields.append(f"pop_type = {pop_type}")
            fields.append(f"size = {total}")
            _, first, _ = rows[0]
            edits.append((first.start, first.end, "create_pop = { " + " ".join(fields) + " }"))
            edits.extend((node.start, node.end, "") for _, node, _ in rows[1:])
        assert originals == processed
    return splice(text, edits)


def dedupe_culture_lists(text, targets):
    edits = []
    for node in walk(parse(text)):
        if node.key in LIST_KEYS and node.children():
            seen = set()
            for item in node.children():
                if not item.key and item.value in targets:
                    if item.value in seen:
                        edits.append((item.start, item.end, ""))
                    seen.add(item.value)
    return splice(text, edits)


def change_script(text, code, matches):
    def replace(token):
        word = token.group()
        if word in code:
            matches[word] += 1
            return code[word]
        return word
    return TOKENS.sub(replace, text)


def remove_culture_history(text, code):
    edits = []
    for root in parse(text):
        for node in root.children():
            if node.key.startswith("cu:") and node.key[3:] in code:
                if any(item.key != "set_fervor" for item in node.children()):
                    raise ValueError(f"Culture has additional history settings: {node.key}")
                edits.append((node.start, node.end, ""))
    return splice(text, edits)


def generate(output):
    replacement = replacements()
    cultures = objects("common/cultures", BASE)
    assert replacement.keys() <= cultures.keys()
    assert set(replacement.values()) <= cultures.keys() - replacement.keys()
    religions = {name: atom(node, "religion") for name, node in cultures.items()}
    output.mkdir()
    (output / ".metadata").mkdir()
    metadata = {"name": "1776 Culture and POP Consolidation (Experiment)",
                "version": "0.1.0", "supported_game_version": "1.15.*",
                "game_custom_data": {"multiplayer_synchronized": True, "replace_paths": []}}
    (output / ".metadata/metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    edges = "|".join(re.escape(word) for word in replacement)
    match_candidate = re.compile(r"(?<![A-Za-z0-9_])(?:" + edges + r")(?![A-Za-z0-9_])")
    loc_forms = re.compile(r"(\$|GetCulture\(')(" + edges + r")(?=[|$'])")
    receipt = {}
    totals = Counter()
    matched_names = Counter()
    removed = set()
    for relative, path in sorted(effective_files().items()):
        raw = path.read_bytes()
        text = raw.decode("utf-8-sig")
        changed = text
        occurrences = Counter()
        if relative.startswith(POP_DIR):
            changed = consolidate_pops(text, replacement, religions, totals)
        elif not match_candidate.search(text):
            continue
        elif relative.startswith(CULTURE_DIR):
            obsolete = [n for n in parse(text) if n.key in replacement]
            changed = splice(text, [(n.start, n.end, "") for n in obsolete])
            removed.update(n.key for n in obsolete)
        elif relative.startswith(CULTURE_HISTORY_DIR):
            changed = change_script(remove_culture_history(text, replacement), replacement, occurrences)
        elif path.suffix == ".yml":
            changed = loc_forms.sub(lambda m: m[1] + replacement[m[2]], text)
        elif path.suffix == ".gui":
            changed = loc_forms.sub(lambda m: m[1] + replacement[m[2]], text)
        else:
            changed = change_script(text, replacement, occurrences)
            if occurrences and any(key in changed for key in LIST_KEYS):
                changed = dedupe_culture_lists(changed, set(replacement.values()))
        if changed == text:
            continue
        if path.suffix == ".txt" and (relative.startswith(CULTURE_DIR) or relative.startswith(POP_DIR)):
            parse(changed)
        bom = b"\xef\xbb\xbf" if raw.startswith(b"\xef\xbb\xbf") else b""
        result = bom + changed.encode("utf-8")
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(result)
        receipt[relative] = dict(source="mod" if path.is_relative_to(BASE) else "Steam 1.15.2",
                                 original_sha256=hashlib.sha256(raw).hexdigest(),
                                 changed_sha256=hashlib.sha256(result).hexdigest(), replacements=occurrences)
        matched_names.update(occurrences)
    assert removed == replacement.keys(), replacement.keys() - removed
    assert totals["size_before"] == totals["size_after"]
    assert totals["groups_before"] > totals["groups_after"]
    report = dict(culture_map=replacement, history=totals, culture_definitions_before=len(cultures),
                  culture_definitions_after=len(cultures)-len(removed),
                  rewrite_count=len(receipt), references=matched_names, files=receipt)
    with output.with_name(output.name + "_build.json").open("x", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, ensure_ascii=False)
    print({k: v for k, v in report.items() if k in ("history", "culture_definitions_before",
                                                    "culture_definitions_after", "rewrite_count")})


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("overlay", type=Path)
    args = cli.parse_args()
    generate(args.overlay)

