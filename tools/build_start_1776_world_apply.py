#!/usr/bin/env python3
"""Apply the validated 1776 world building target.

The transformation is intentionally narrow:
- existing surviving placements keep their active PMs and ownership topology;
- target levels are applied by rescaling existing ownership shares;
- new placements use an existing building template and base PMs;
- regional infrastructure always uses the exact 232-row PM plan;
- Serenissima and protected military/naval rows are never rewritten;
- orphan history rows are left in their original source files.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import textwrap
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

import build_start_1776_research_input_pack as catalog_tools


ROOT = Path(__file__).resolve().parents[1]
VANILLA = Path(r"C:\Games\Victoria 3\game")
REPORTS = ROOT / "docs" / "reports" / "buildings"
HISTORY = ROOT / "common" / "history" / "buildings"
OVERLAY = HISTORY / "98_build_start_1776_world_redistribution.txt"
MATRIX = REPORTS / "BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv"
CATALOG = REPORTS / "BUILD_START_1776_BUILDING_CATALOG.csv"
INFRA = REPORTS / "BUILD_START_1776_INFRASTRUCTURE_PM_PLAN.csv"

SERENISSIMA = {"VEN", "GEN"}
PROTECTED = {
    "building_barrack",
    "building_naval_administration",
    "building_naval_fortification",
}


@dataclass
class Placement:
    path: Path
    start: int
    end: int
    state: str
    owner: str
    building: str
    level: int
    pms: tuple[str, ...]
    text: str

    @property
    def key(self) -> tuple[str, str, str]:
        return self.owner, self.state, self.building


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def integer(value: str | int) -> int:
    return int(float(value or 0))


def block_spans(text: str, identifier: str, depth: int) -> list[tuple[str, int, int]]:
    cleaned = catalog_tools.clean_comments(text)
    depths, pairs = catalog_tools.brace_maps(cleaned)
    pattern = re.compile(rf"(?m)^[ \t]*(?P<id>{identifier})[ \t]*=[ \t]*\{{")
    result = []
    for match in pattern.finditer(cleaned):
        if depths[match.start()] != depth:
            continue
        opening = cleaned.find("{", match.start(), match.end())
        result.append((match.group("id"), match.start(), pairs[opening] + 1))
    return result


def parse_file(path: Path) -> tuple[str, list[Placement]]:
    raw = path.read_text(encoding="utf-8-sig")
    states = block_spans(raw, r"s:STATE_[A-Za-z0-9_]+", 1)
    regions = block_spans(raw, r"region_state:[A-Za-z0-9_]+", 2)
    created = block_spans(raw, r"create_building", 3)
    result: list[Placement] = []
    for _, start, end in created:
        state_match = next((item for item in states if item[1] < start < item[2]), None)
        region_match = next((item for item in regions if item[1] < start < item[2]), None)
        if not state_match or not region_match:
            raise ValueError(f"Cannot resolve state/owner context in {path}:{start}")
        block = raw[start:end]
        building = catalog_tools.scalar(block, "building")
        levels = sum(int(value) for value in re.findall(
            r"\blevels\s*=\s*(\d+)", catalog_tools.clean_comments(block)
        ))
        if not levels:
            levels = integer(catalog_tools.scalar(block, "level", "0"))
        pms = tuple(catalog_tools.tokens_flat(
            catalog_tools.braced_tokens(block, "activate_production_methods")
        ))
        result.append(Placement(
            path=path,
            start=start,
            end=end,
            state=state_match[0].split(":", 1)[1],
            owner=region_match[0].split(":", 1)[1],
            building=building,
            level=levels,
            pms=pms,
            text=block,
        ))
    return raw, result


def all_placements(folder: Path, exclude_overlay: bool = False) -> tuple[dict[Path, str], list[Placement]]:
    raws: dict[Path, str] = {}
    rows: list[Placement] = []
    for path in sorted(folder.glob("*.txt")):
        if exclude_overlay and path.resolve() == OVERLAY.resolve():
            continue
        raw, parsed = parse_file(path)
        raws[path] = raw
        rows.extend(parsed)
    return raws, rows


def allocate(weights: list[int], total: int) -> list[int]:
    if not weights:
        return []
    order = sorted(range(len(weights)), key=lambda index: (-weights[index], index))
    if total < len(weights):
        chosen = set(order[:total])
        return [1 if index in chosen else 0 for index in range(len(weights))]
    base = [1] * len(weights)
    remaining = total - len(weights)
    weight_sum = sum(weights) or len(weights)
    exact = [remaining * (weight or 1) / weight_sum for weight in weights]
    floors = [math.floor(value) for value in exact]
    for index, value in enumerate(floors):
        base[index] += value
    left = remaining - sum(floors)
    fractions = sorted(
        range(len(weights)), key=lambda index: (-(exact[index] - floors[index]), -weights[index], index)
    )
    for index in fractions[:left]:
        base[index] += 1
    return base


def rescale_ownership(block: str, target: int) -> str:
    ownership = block_spans(block, r"add_ownership", 1)
    if not ownership:
        if re.search(r"(?m)^\s*level\s*=", block):
            return re.sub(r"(?m)^(\s*level\s*=\s*)\d+", rf"\g<1>{target}", block, count=1)
        if re.search(r"(?m)^\s*levels\s*=", block):
            return re.sub(r"(?m)^(\s*levels\s*=\s*)\d+", rf"\g<1>{target}", block, count=1)
        raise ValueError("Placement has no ownership or direct level field")
    parsed: list[tuple[int, int, str, list[tuple[str, int, int]], list[int]]] = []
    all_weights: list[int] = []
    for _, own_start, own_end in ownership:
        own = block[own_start:own_end]
        shares = block_spans(own, r"(?:country|building|company)", 1)
        weights: list[int] = []
        if shares:
            for _, start, end in shares:
                match = re.search(r"(?m)^\s*levels\s*=\s*(\d+)", own[start:end])
                if not match:
                    raise ValueError("Ownership share has no levels")
                weights.append(int(match.group(1)))
            kind = "blocks"
        else:
            inline_levels = list(re.finditer(r"\blevels\s*=\s*(\d+)", own))
            if len(inline_levels) != 1:
                raise ValueError("add_ownership has no parseable ownership share")
            weights = [int(inline_levels[0].group(1))]
            kind = "inline"
        parsed.append((own_start, own_end, kind, shares, weights))
        all_weights.extend(weights)

    allocations = allocate(all_weights, target)
    cursor = 0
    replacements: list[tuple[int, int, str]] = []
    for own_start, own_end, kind, shares, weights in parsed:
        own = block[own_start:own_end]
        local = allocations[cursor:cursor + len(weights)]
        cursor += len(weights)
        if kind == "inline":
            replacement = "" if local[0] == 0 else re.sub(
                r"(\blevels\s*=\s*)\d+", rf"\g<1>{local[0]}", own, count=1
            )
        else:
            replacement = own
            for (_, start, end), level in reversed(list(zip(shares, local))):
                share = "" if level == 0 else re.sub(
                    r"(?m)^(\s*levels\s*=\s*)\d+",
                    rf"\g<1>{level}",
                    own[start:end],
                    count=1,
                )
                replacement = replacement[:start] + share + replacement[end:]
            if not any(local):
                replacement = ""
        replacements.append((own_start, own_end, replacement))

    transformed = block
    for start, end, replacement in reversed(replacements):
        transformed = transformed[:start] + replacement + transformed[end:]
    return transformed


def replace_active_pms(block: str, pms: list[str]) -> str:
    spans = block_spans(block, r"activate_production_methods", 1)
    if len(spans) > 1:
        raise ValueError("Multiple activate_production_methods blocks")
    replacement = ""
    if pms:
        replacement = "\tactivate_production_methods = { " + " ".join(f'\"{pm}\"' for pm in pms) + " }"
    if spans:
        _, start, end = spans[0]
        indentation = re.match(r"[ \t]*", block[start:]).group(0)
        replacement = replacement.lstrip("\t")
        replacement = indentation + replacement if replacement else ""
        return block[:start] + replacement + block[end:]
    if not replacement:
        return block
    closing = block.rfind("}")
    return block[:closing] + "\n" + replacement + "\n" + block[closing:]


def base_pms(catalog_row: dict[str, str]) -> list[str]:
    value = catalog_row.get("Base_PM", "")
    if not value or value == "NONE":
        return []
    return [item.split(":", 1)[-1] for item in value.split("|") if item and item != "NONE"]


def transform_template(
    placement: Placement,
    owner: str,
    state: str,
    target: int,
    pms: list[str],
) -> str:
    block = textwrap.dedent(placement.text).strip()
    block = re.sub(r'(?m)(country\s*=\s*\"?)c:[A-Z0-9_]+', rf'\g<1>c:{owner}', block)
    block = re.sub(r'(?m)(region\s*=\s*\"?)STATE_[A-Z0-9_]+', rf'\g<1>{state}', block)
    block = rescale_ownership(block, target)
    block = replace_active_pms(block, pms)
    return block


def indent(text: str, tabs: int) -> str:
    prefix = "\t" * tabs
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def build_overlay(rows: list[tuple[str, str, str, int, str]]) -> str:
    grouped: dict[str, dict[str, list[tuple[str, str]]]] = defaultdict(lambda: defaultdict(list))
    for owner, state, building, _, block in rows:
        grouped[state][owner].append((building, block))
    lines = ["# Generated from BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX_CORRIGE_V2.csv", "BUILDINGS = {"]
    for state, owners in sorted(grouped.items()):
        lines.append(f"\ts:{state} = {{")
        for owner, blocks in sorted(owners.items()):
            lines.append(f"\t\tregion_state:{owner} = {{")
            for _, block in sorted(blocks):
                lines.append(indent(block, 3))
            lines.append("\t\t}")
        lines.append("\t}")
    lines.append("}")
    return "\n".join(lines) + "\n"


def semantic(rows: list[Placement], predicate) -> dict[tuple[str, str, str], tuple[int, tuple[str, ...]]]:
    result: dict[tuple[str, str, str], tuple[int, tuple[str, ...]]] = {}
    grouped: dict[tuple[str, str, str], list[Placement]] = defaultdict(list)
    for row in rows:
        if predicate(row):
            grouped[row.key].append(row)
    for key, items in grouped.items():
        result[key] = (
            sum(item.level for item in items),
            tuple(sorted({pm for item in items for pm in item.pms})),
        )
    return result


def apply() -> dict[str, object]:
    if OVERLAY.exists():
        raise SystemExit(f"Overlay already exists: {OVERLAY}")

    matrix = read_csv(MATRIX)
    catalog = {row["Building_ID"]: row for row in read_csv(CATALOG)}
    infrastructure = {
        (row["Owner_TAG"], row["State_ID"]): row for row in read_csv(INFRA)
    }
    target = {
        (row["Owner_TAG"], row["State_ID"], row["Building_ID"]): integer(row["Target_Level"])
        for row in matrix
    }
    decisions = Counter(row["Decision"] for row in matrix)
    if len(matrix) != 3913 or sum(target.values()) != 3813:
        raise SystemExit("V2 matrix count/level preflight failed")
    if decisions != Counter({
        "REMOVE": 1626, "ADD": 1268, "KEEP": 509,
        "DECREASE": 325, "INCREASE": 140, "PRESERVE_SERENISSIMA": 45,
    }):
        raise SystemExit(f"V2 decision preflight failed: {decisions}")
    if len(infrastructure) != 232:
        raise SystemExit("Infrastructure plan must contain 232 rows")

    raws, placements = all_placements(HISTORY, exclude_overlay=True)
    by_key: dict[tuple[str, str, str], list[Placement]] = defaultdict(list)
    for row in placements:
        by_key[row.key].append(row)

    protected_before = semantic(
        placements, lambda row: row.owner in SERENISSIMA or row.building in PROTECTED
    )
    if len(semantic(placements, lambda row: row.building in PROTECTED)) != 65:
        raise SystemExit("Protected placement baseline changed")
    if sum(value[0] for value in semantic(placements, lambda row: row.building in PROTECTED).values()) != 414:
        raise SystemExit("Protected level baseline changed")

    replacements: dict[Path, list[tuple[int, int, str]]] = defaultdict(list)
    additions: list[tuple[str, str, str, int, str]] = []

    # Rebuild the template map by Building_ID, preferring mod history.
    template_by_building: dict[str, Placement] = {}
    for placement in placements:
        template_by_building.setdefault(placement.building, placement)
    _, vanilla_rows = all_placements(VANILLA / "common" / "history" / "buildings")
    for placement in vanilla_rows:
        template_by_building.setdefault(placement.building, placement)
    # These unique monuments are either DLC-conditional in vanilla history or
    # have no ordinary history placement.  Their definitions use a direct
    # level field and need no ownership fabrication.
    for building in {
        "building_manila_cathedral_original",
        "building_observatorygreenwich",
        "building_pena_convent",
    }:
        template_by_building.setdefault(building, Placement(
            path=ROOT,
            start=0,
            end=0,
            state="",
            owner="",
            building=building,
            level=1,
            pms=(),
            text=f'create_building = {{\n\tbuilding = "{building}"\n\tlevel = 1\n}}',
        ))

    for key, current_blocks in sorted(by_key.items()):
        if key not in target:
            continue  # explicitly preserve orphan history rows
        owner, state, building = key
        wanted = target[key]
        if owner in SERENISSIMA or building in PROTECTED:
            continue
        for index, placement in enumerate(current_blocks):
            if wanted == 0 or index > 0:
                replacements[placement.path].append((placement.start, placement.end, ""))
                continue
            changed = rescale_ownership(placement.text, wanted)
            if building == "building_railway":
                plan = infrastructure[(owner, state)]
                changed = replace_active_pms(changed, [
                    plan["Road_PM"], plan["Canal_PM"], plan["Rail_PM"], plan["Passenger_PM"]
                ])
            replacements[placement.path].append((placement.start, placement.end, changed))

    for row in matrix:
        if row["Decision"] != "ADD":
            continue
        owner, state, building = row["Owner_TAG"], row["State_ID"], row["Building_ID"]
        if owner in SERENISSIMA or building in PROTECTED:
            raise SystemExit(f"Protected key marked ADD: {(owner, state, building)}")
        wanted = integer(row["Target_Level"])
        template = template_by_building.get(building)
        if not template:
            raise SystemExit(f"No history template for {building}")
        if building == "building_railway":
            plan = infrastructure[(owner, state)]
            pms = [plan["Road_PM"], plan["Canal_PM"], plan["Rail_PM"], plan["Passenger_PM"]]
        else:
            pms = base_pms(catalog[building])
        block = transform_template(template, owner, state, wanted, pms)
        additions.append((owner, state, building, wanted, block))

    transformed_raws = dict(raws)
    for path, changes in replacements.items():
        raw = transformed_raws[path]
        for start, end, replacement in sorted(changes, reverse=True):
            raw = raw[:start] + replacement + raw[end:]
        catalog_tools.brace_maps(catalog_tools.clean_comments(raw))
        transformed_raws[path] = raw
    overlay_text = build_overlay(additions)
    catalog_tools.brace_maps(catalog_tools.clean_comments(overlay_text))

    # Write only after every transformed file has passed brace validation.
    for path, raw in transformed_raws.items():
        if raw != raws[path]:
            path.write_text(raw, encoding="utf-8")
    OVERLAY.write_text(overlay_text, encoding="utf-8")

    _, after = all_placements(HISTORY)
    protected_after = semantic(
        after, lambda row: row.owner in SERENISSIMA or row.building in PROTECTED
    )
    if protected_after != protected_before:
        raise SystemExit("Protected/Serenissima semantic content changed")

    actual: dict[tuple[str, str, str], int] = defaultdict(int)
    for placement in after:
        actual[placement.key] += placement.level
    mismatch = [key for key, level in target.items() if level > 0 and actual.get(key, 0) != level]
    missing = [key for key, level in target.items() if level > 0 and actual.get(key, 0) == 0]
    if mismatch or missing:
        raise SystemExit(f"Post-write target failure: mismatch={len(mismatch)} missing={len(missing)}")

    infra_actual = {
        row.key: row for row in after if row.building == "building_railway" and row.key in target and target[row.key] > 0
    }
    infra_bad = []
    for (owner, state), plan in infrastructure.items():
        key = (owner, state, "building_railway")
        placement = infra_actual.get(key)
        expected = {
            plan["Road_PM"], plan["Canal_PM"], plan["Rail_PM"], plan["Passenger_PM"]
        }
        if not placement or set(placement.pms) != expected:
            infra_bad.append(key)
    if infra_bad:
        raise SystemExit(f"Infrastructure PM mismatch: {len(infra_bad)}")

    return {
        "source_files_changed": sum(transformed_raws[path] != raws[path] for path in raws),
        "new_overlay_rows": len(additions),
        "target_positive_rows": sum(level > 0 for level in target.values()),
        "target_levels": sum(target.values()),
        "target_mismatch": len(mismatch),
        "target_missing": len(missing),
        "protected_semantic_changes": 0,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    if not args.apply:
        raise SystemExit("Use --apply to perform the validated bulk rewrite")
    print(json.dumps(apply(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
