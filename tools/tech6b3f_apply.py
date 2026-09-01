#!/usr/bin/env python3
"""Apply the TECH6B3F matrix as narrowly scoped, auditable rewrites."""

from __future__ import annotations

import argparse
import csv
import re
import shutil
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VANILLA = Path(r"C:\Games\Victoria 3\game")
MATRIX = ROOT / "docs/reports/technology/TECH6B3E_HIDDEN_TECH_RESPONSIBILITY_MATRIX.csv"
OUT_MATRIX = ROOT / "docs/reports/technology/TECH6B3F_HIDDEN_TECH_RESPONSIBILITY_IMPLEMENTATION_MATRIX.csv"
OUT_STARTING = ROOT / "docs/reports/technology/TECH6B3F_STARTING_TECH_DEFERRED_MATRIX.csv"
TECH_COMPAT = "common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt"

IMPL_HEADERS = [
    "hidden_tech_id", "responsibility_type", "object_id", "source_file",
    "old_owner", "approved_target", "implementation_action",
    "implementation_status", "actual_file_changed", "validation", "notes",
]
START_HEADERS = [
    "hidden_tech_id", "responsibility_type", "country_or_effect", "source_file",
    "current_grant", "recommended_successor_from_tech6b3e", "reason_deferred",
    "future_phase",
]


class Store:
    def __init__(self, apply: bool):
        self.apply = apply
        self.data: dict[str, str] = {}
        self.meta: dict[str, tuple[bool, str]] = {}
        self.original: dict[str, str] = {}
        self.created: set[str] = set()

    def load(self, rel: str) -> str:
        if rel in self.data:
            return self.data[rel]
        local = ROOT / rel
        source = local if local.exists() else VANILLA / rel
        if not source.exists():
            raise RuntimeError(f"missing effective source: {rel}")
        raw = source.read_bytes()
        bom = raw.startswith(b"\xef\xbb\xbf")
        payload = raw[3:] if bom else raw
        try:
            text = payload.decode("utf-8")
            encoding = "utf-8"
        except UnicodeDecodeError:
            text = payload.decode("cp1252")
            encoding = "cp1252"
        self.data[rel] = text
        self.original[rel] = text
        self.meta[rel] = (bom, encoding)
        if not local.exists():
            self.created.add(rel)
        return text

    def set(self, rel: str, text: str) -> None:
        self.data[rel] = text

    def changed(self, rel: str) -> bool:
        return self.data.get(rel) != self.original.get(rel)

    def write(self) -> list[str]:
        changed = sorted(rel for rel in self.data if self.changed(rel))
        if not self.apply:
            return changed
        for rel in changed:
            dst = ROOT / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            bom, encoding = self.meta[rel]
            raw = self.data[rel].encode(encoding)
            if bom:
                raw = b"\xef\xbb\xbf" + raw
            dst.write_bytes(raw)
        return changed


def block_range(text: str, name: str, start: int = 0) -> tuple[int, int]:
    pattern = re.compile(rf"(?m)^[ \t]*{re.escape(name)}[ \t]*=[ \t]*\{{")
    match = pattern.search(text, start)
    if not match:
        raise RuntimeError(f"block not found: {name}")
    opening = text.find("{", match.start(), match.end())
    depth = 0
    quoted = False
    escaped = False
    comment = False
    i = opening
    while i < len(text):
        ch = text[i]
        if comment:
            if ch in "\r\n":
                comment = False
            i += 1
            continue
        if quoted:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                quoted = False
            i += 1
            continue
        if ch == "#":
            comment = True
        elif ch == '"':
            quoted = True
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return match.start(), i + 1
        i += 1
    raise RuntimeError(f"unterminated block: {name}")


def child_range(text: str, parent: tuple[int, int], name: str) -> tuple[int, int] | None:
    p0, p1 = parent
    match = re.search(rf"(?m)^[ \t]+{re.escape(name)}[ \t]*=[ \t]*\{{", text[p0:p1])
    if not match:
        return None
    return block_range(text, name, p0 + match.start())


def active_count(text: str, token: str) -> int:
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(token)}(?![A-Za-z0-9_])")
    total = 0
    for line in text.splitlines():
        active = line.split("#", 1)[0]
        total += len(pattern.findall(active))
    return total


def active_replace(text: str, old: str, new: str) -> tuple[str, int]:
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(old)}(?![A-Za-z0-9_])")
    out: list[str] = []
    total = 0
    for line in text.splitlines(keepends=True):
        body, marker, comment = line.partition("#")
        body, count = pattern.subn(new, body)
        total += count
        out.append(body + (marker + comment if marker else ""))
    return "".join(out), total


def replace_at_lines(text: str, line_numbers: list[int], old: str, new: str) -> tuple[str, int, int]:
    """Replace active token occurrences only on the exact audited source lines."""
    pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(old)}(?![A-Za-z0-9_])")
    target_pattern = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(new)}(?![A-Za-z0-9_])")
    lines = text.splitlines(keepends=True)
    replaced = 0
    already = 0
    for number in line_numbers:
        if number < 1 or number > len(lines):
            raise RuntimeError(f"audited line outside file: {number}/{len(lines)}")
        line = lines[number - 1]
        body, marker, comment = line.partition("#")
        body, count = pattern.subn(new, body)
        if count == 0:
            already += len(target_pattern.findall(body))
        replaced += count
        lines[number - 1] = body + (marker + comment if marker else "")
    return "".join(lines), replaced, already


def expected_occurrences(rows: list[dict[str, str]]) -> int:
    total = 0
    for row in rows:
        match = re.search(r"occurrences=(\d+)", row["current_effect"])
        total += int(match.group(1)) if match else 1
    return total


def replace_inside_object(text: str, obj: str, old: str, new: str) -> tuple[str, int]:
    start, end = block_range(text, obj)
    replaced, count = active_replace(text[start:end], old, new)
    return text[:start] + replaced + text[end:], count


def remove_modifier_block(text: str, tech: str) -> tuple[str, str | None]:
    parent = block_range(text, tech)
    child = child_range(text, parent, "modifier")
    if child is None:
        return text, None
    c0, c1 = child
    removed = text[c0:c1]
    while c1 < len(text) and text[c1] in " \t":
        c1 += 1
    if text[c1:c1 + 2] == "\r\n":
        c1 += 2
    elif text[c1:c1 + 1] == "\n":
        c1 += 1
    return text[:c0] + text[c1:], removed


def modifier_values(text: str, tech: str) -> dict[str, str]:
    parent = block_range(text, tech)
    child = child_range(text, parent, "modifier")
    if child is None:
        return {}
    block = text[child[0]:child[1]]
    return dict(re.findall(r"(?m)^[ \t]+([A-Za-z0-9_]+)[ \t]*=[ \t]*([^\s#}]+)", block))


def add_modifiers(text: str, tech: str, entries: list[tuple[str, str]]) -> tuple[str, list[str]]:
    parent = block_range(text, tech)
    existing = modifier_values(text, tech)
    missing: list[tuple[str, str]] = []
    for key, value in entries:
        if key in existing and existing[key] != value:
            raise RuntimeError(f"modifier mismatch on {tech}: {key}={existing[key]}, expected {value}")
        if key not in existing:
            missing.append((key, value))
    if not missing:
        return text, []
    child = child_range(text, parent, "modifier")
    if child:
        closing_brace = child[1] - 1
        insert = text.rfind("\n", child[0], closing_brace) + 1
        addition = "".join(f"\t\t{k} = {v}\n" for k, v in missing)
        text = text[:insert] + addition + text[insert:]
    else:
        p0, p1 = parent
        anchor = re.search(r"(?m)^[ \t]+(?:unlocking_technologies|ai_weight)[ \t]*=", text[p0:p1])
        insert = p0 + anchor.start() if anchor else p1 - 1
        addition = "\tmodifier = {\n" + "".join(f"\t\t{k} = {v}\n" for k, v in missing) + "\t}\n\n"
        text = text[:insert] + addition + text[insert:]
    return text, [k for k, _ in missing]


def move_child_block(source: str, source_tech: str, target: str, target_tech: str, child_name: str) -> tuple[str, str, bool]:
    sp = block_range(source, source_tech)
    sc = child_range(source, sp, child_name)
    tp = block_range(target, target_tech)
    tc = child_range(target, tp, child_name)
    if sc is None:
        if tc is None:
            raise RuntimeError(f"{child_name} absent from source and target")
        return source, target, False
    if tc is not None:
        raise RuntimeError(f"{child_name} already exists on target {target_tech}")
    c0, c1 = sc
    payload = source[c0:c1]
    while c1 < len(source) and source[c1] in " \t":
        c1 += 1
    if source[c1:c1 + 2] == "\r\n":
        c1 += 2
    elif source[c1:c1 + 1] == "\n":
        c1 += 1
    source = source[:c0] + source[c1:]
    tp = block_range(target, target_tech)
    anchor = re.search(r"(?m)^[ \t]+ai_weight[ \t]*=", target[tp[0]:tp[1]])
    insert = tp[0] + anchor.start() if anchor else tp[1] - 1
    target = target[:insert] + payload + "\n\n" + target[insert:]
    return source, target, True


def row_record(row: dict[str, str], target: str, action: str, status: str, files: str, validation: str, notes: str = "") -> dict[str, str]:
    return {
        "hidden_tech_id": row["hidden_tech_id"],
        "responsibility_type": row["responsibility_type"],
        "object_id": row["object_id"],
        "source_file": row["source_file"],
        "old_owner": row["hidden_tech_id"],
        "approved_target": target,
        "implementation_action": action,
        "implementation_status": status,
        "actual_file_changed": files,
        "validation": validation,
        "notes": notes,
    }


def write_csv(path: Path, headers: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    with MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))

    store = Store(args.apply)
    records: dict[tuple[str, str, str, str], dict[str, str]] = {}
    key_for = lambda r: (r["hidden_tech_id"], r["responsibility_type"], r["object_id"], r["source_file"])

    starting = [r for r in rows if r["responsibility_type"] == "starting_technology_grant"]
    nonstarting = [r for r in rows if r["responsibility_type"] != "starting_technology_grant"]
    direct = [r for r in nonstarting if r["responsibility_type"] == "direct_modifier"]
    on_researched = [r for r in nonstarting if r["responsibility_type"] == "on_researched"]
    urban_deferred_ids = {"building_urban_center", "building_construction_sector"}

    for row in nonstarting:
        key = key_for(row)
        if row["responsibility_type"] == "none":
            records[key] = row_record(row, "NONE", "RETAIN_COMPATIBILITY_ALIAS", "COMPATIBILITY_REFERENCE_ALLOWED", "NONE", "alias definition retained; no active responsibility")
        elif row["object_id"] in urban_deferred_ids:
            records[key] = row_record(row, row["recommended_target_tech"], "NO_CHANGE_PENDING_URBAN_GATE_REVIEW", "DEFERRED_URBAN_BUILDING", "NONE", "current hidden gate intentionally retained", "Paved Roads is era 10 and cannot be applied automatically to a fundamental building")

    generic = [r for r in nonstarting if key_for(r) not in records and r not in direct and r not in on_researched]
    for row in generic:
        old = row["hidden_tech_id"]
        rel = row["source_file"]
        target = row["recommended_target_tech"]
        if old == "psychiatry" and rel == "common/journal_entries/02_positivism.txt":
            target = "philosophical_pragmatism"
        match = re.search(r"lines=([0-9,]+)", row["current_effect"])
        if not match:
            raise RuntimeError(f"audited line list missing: {old} {rel} {row['object_id']}")
        line_numbers = [int(value) for value in match.group(1).split(",")]
        expected = expected_occurrences([row])
        text = store.load(rel)
        text, count, already = replace_at_lines(text, line_numbers, old, target)
        if count == expected:
            status = "IMPLEMENTED"
            store.set(rel, text)
        elif count == 0 and already == expected:
            status = "ALREADY_CORRECT"
        else:
            raise RuntimeError(
                f"audited-line mismatch {rel}:{line_numbers} {old}->{target}; "
                f"replaced={count} already={already} expected={expected}"
            )
        records[key_for(row)] = row_record(
            row, target, "REPLACE_AUDITED_TECH_REFERENCE", status,
            rel if status == "IMPLEMENTED" else "NONE",
            f"exact audited lines {','.join(map(str, line_numbers))}; old owner removed; target present",
        )

    # Taxation: the hidden proportional-tax row is handled above; capitation is an
    # additional visible-owner correction mandated directly by the TECH6B3F prompt.
    tax_rel = "common/laws/01_taxation.txt"
    tax_text = store.load(tax_rel)
    tax_text, tax_count = replace_inside_object(tax_text, "law_per_capita_based_taxation", "scientific_metrology", "systematic_population_registration")
    if tax_count not in (0, 2):
        raise RuntimeError(f"per-capita taxation expected 2 owner/availability refs, got {tax_count}")
    tax_block = tax_text[slice(*block_range(tax_text, "law_per_capita_based_taxation"))]
    if active_count(tax_block, "systematic_population_registration") != 2:
        raise RuntimeError("per-capita taxation target gate/AI reference is incomplete")
    store.set(tax_rel, tax_text)

    direct_specs = {
        "army_reserves": ("corps_organization", "common/technology/technologies/20_tech3a_military.txt"),
        "mandatory_service": ("corps_organization", "common/technology/technologies/20_tech3a_military.txt"),
        "dialectics": ("polytechnical_education", "common/technology/technologies/30_tech3a_society.txt"),
        "military_drill": ("light_infantry_tactics", "common/technology/technologies/20_tech3a_military.txt"),
        "power_of_the_purse": ("state_dockyard_systems", "common/technology/technologies/25_tech3a_naval.txt"),
        "psychiatry": ("philosophical_pragmatism", TECH_COMPAT),
        "sericulture": ("selective_breeding", "common/technology/technologies/10_tech3a_production.txt"),
        "urban_planning": ("modern_sewerage", TECH_COMPAT),
        "urbanization": ("paved_roads", TECH_COMPAT),
    }
    by_hidden: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in direct:
        by_hidden[row["hidden_tech_id"]].append(row)
    for hidden, group in sorted(by_hidden.items()):
        target, target_rel = direct_specs[hidden]
        entries = []
        for row in group:
            match = re.fullmatch(r"\s*([A-Za-z0-9_]+)\s*=\s*([^\s]+)\s*", row["current_effect"])
            if not match:
                raise RuntimeError(f"cannot parse exact modifier: {row['current_effect']}")
            entries.append((match.group(1), match.group(2)))
        source_text = store.load(TECH_COMPAT)
        target_text = source_text if target_rel == TECH_COMPAT else store.load(target_rel)
        target_text, added = add_modifiers(target_text, target, entries)
        source_text, removed = remove_modifier_block(source_text, hidden)
        if removed is None:
            current = modifier_values(target_text, target)
            if any(current.get(k) != v for k, v in entries):
                raise RuntimeError(f"modifier source absent but target incomplete: {hidden}->{target}")
            status = "ALREADY_CORRECT"
        else:
            status = "IMPLEMENTED"
        if target_rel == TECH_COMPAT:
            store.set(TECH_COMPAT, target_text if target_text != store.load(TECH_COMPAT) else source_text)
            # Both edits are in one cached file; reapply source removal after target insertion.
            combined = target_text
            combined, removed_again = remove_modifier_block(combined, hidden)
            if removed_again is not None:
                source_text = combined
            else:
                source_text = target_text
            store.set(TECH_COMPAT, source_text)
        else:
            store.set(TECH_COMPAT, source_text)
            store.set(target_rel, target_text)
        changed_files = sorted({TECH_COMPAT, target_rel}) if status == "IMPLEMENTED" else []
        for row in group:
            records[key_for(row)] = row_record(row, target, "REMOVE_SOURCE_MODIFIER_AND_ENSURE_EXACT_TARGET_VALUE", status, ";".join(changed_files) if changed_files else "NONE", f"exact {row['current_effect']}; added_to_target={'YES' if row['object_id'] in added else 'NO_ALREADY_IDENTICAL'}")

    # Move the single egalitarianism on_researched responsibility indivisibly.
    for row in on_researched:
        source_text = store.load(TECH_COMPAT)
        target_rel = "common/technology/technologies/30_tech3a_society.txt"
        target_text = store.load(target_rel)
        source_text, target_text, moved = move_child_block(source_text, "egalitarianism", target_text, "liberal_constitutionalism", "on_researched")
        store.set(TECH_COMPAT, source_text)
        store.set(target_rel, target_text)
        status = "IMPLEMENTED" if moved else "ALREADY_CORRECT"
        records[key_for(row)] = row_record(row, "liberal_constitutionalism", "MOVE_ON_RESEARCHED_BLOCK_INDIVISIBLY", status, f"{TECH_COMPAT};{target_rel}" if moved else "NONE", "source block absent and target block present" if not moved else "exact Springtime involvement effect moved")

    if len(records) != len(nonstarting):
        missing = [key_for(r) for r in nonstarting if key_for(r) not in records]
        raise RuntimeError(f"implementation matrix incomplete: {len(records)}/{len(nonstarting)}; {missing[:5]}")

    changed = store.write()
    if args.apply:
        impl_rows = [records[key_for(row)] for row in nonstarting]
        start_rows = [{
            "hidden_tech_id": r["hidden_tech_id"],
            "responsibility_type": r["responsibility_type"],
            "country_or_effect": r["object_id"],
            "source_file": r["source_file"],
            "current_grant": r["current_effect"],
            "recommended_successor_from_tech6b3e": r["recommended_target_tech"],
            "reason_deferred": "Historical or tier grant requires country-by-country reconciliation; no automatic successor grant is authorized.",
            "future_phase": "TECH6B3G_STARTING_TECH_RECONCILIATION",
        } for r in starting]
        write_csv(OUT_MATRIX, IMPL_HEADERS, impl_rows)
        write_csv(OUT_STARTING, START_HEADERS, start_rows)

    print(f"MODE={'APPLY' if args.apply else 'CHECK'}")
    print(f"NON_STARTING_ROWS={len(nonstarting)}")
    print(f"STARTING_ROWS_DEFERRED={len(starting)}")
    print(f"GAMEPLAY_FILES_TO_CHANGE={len(changed)}")
    print(f"VANILLA_SHADOWS_TO_CREATE={len([p for p in changed if p in store.created])}")
    print(f"PER_CAPITA_TAX_REPLACEMENTS={tax_count}")
    for rel in changed:
        print(rel)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
