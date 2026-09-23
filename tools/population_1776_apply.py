#!/usr/bin/env python3
"""Apply an auditable, conservative 1776 population pass to existing pop blocks.

The script only changes ``size`` values. It does not add state definitions, tags,
pop groups, cultures, religions or pop types. Targets and protected exceptions are
deliberately explicit; see docs/research/population for the resulting matrix.
"""

from __future__ import annotations

import csv
import argparse
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import build_start_1776_research_input_pack as parser


ROOT = Path(__file__).resolve().parents[1]
HISTORY = ROOT / "common/history/pops"
REPORT = ROOT / "docs/research/population/POPULATION_1776_STATE_TARGETS.csv"
CLIO = "https://clio-infra.eu/Indicators/TotalPopulation.html"
CENSUS = "https://www2.census.gov/prod2/statcomp/documents/CT1970p2-13.pdf"
CANADA = "https://www150.statcan.gc.ca/n1/pub/98-187-x/4064810-eng.htm"
FINLAND = "https://stat.fi/tup/suoluk/suoluk_vaesto_en.html"

# 1776 = 1770 + 0.6 * (1780 - 1770), using US Census colonial series.
# Maryland's colonial total includes present DC; Virginia's includes present WV.
USA_STATE_TARGETS = {
    "STATE_CONNECTICUT": 197_573,
    "STATE_DELAWARE": 41_429,
    "STATE_DISTRICT_OF_COLUMBIA": 5_000,
    "STATE_GEORGIA": 42_993,
    "STATE_MAINE": 41_983,
    "STATE_MARYLAND": 223_324,
    "STATE_MASSACHUSETTS": 255_299,
    "STATE_NEW_HAMPSHIRE": 77_640,
    "STATE_NEW_JERSEY": 130_749,
    "STATE_NEW_YORK": 191_493,
    "STATE_NORTH_CAROLINA": 240_960,
    "STATE_PENNSYLVANIA": 292_406,
    "STATE_RHODE_ISLAND": 55_046,
    "STATE_SOUTH_CAROLINA": 157_698,
    "STATE_VERMONT": 32_572,
    "STATE_VIRGINIA": 476_609,
    "STATE_WEST_VIRGINIA": 25_000,
}

# Target for exact owner, across all files. The source is an anchor, not a claim
# that a modern border matches the 1776 realm perfectly.
OWNER_TARGETS = {
    "RUS": (27_000_000, CLIO, "low estimate; Russian Empire footprint"),
    "PRU": (5_100_000, CLIO, "low estimate; Prussian realm"),
    "PLC": (8_500_000, CLIO, "post-1772 Polish-Lithuanian footprint"),
    "AUS": (11_400_000, CLIO, "Austrian holdings excluding Hungary and Galicia tags"),
    "HUN": (7_000_000, CLIO, "Hungary under Habsburg crown"),
    "GAL": (2_650_000, CLIO, "Galicia after first partition"),
    "TUR": (22_000_000, CLIO, "conservative Ottoman estimate; territorial uncertainty"),
    "PER": (5_760_000, CLIO, "Iran anchor applied to Persian territory"),
}

# Exact owner within a geographical history file; colonial populations elsewhere
# are intentionally not pulled into European mainland targets.
FILE_OWNER_TARGETS = {
    ("00_west_europe.txt", "GBR"): (8_000_000, "https://www.census.gov/library/stories/2023/12/boston-tea-party.html", "Great Britain 1775/1776"),
    ("00_west_europe.txt", "IREK"): (4_170_000, CLIO, "Ireland 1750-1800 interpolation"),
    ("00_west_europe.txt", "FRA"): (26_600_000, CLIO, "metropolitan France 1750-1800 interpolation"),
    ("00_west_europe.txt", "BEO"): (2_770_000, CLIO, "Belgium-area anchor"),
    ("00_west_europe.txt", "NET"): (2_000_000, CLIO, "Netherlands-area anchor"),
    ("00_west_europe.txt", "SWE"): (2_154_880, CLIO, "Sweden excluding Finland"),
    ("15_russia.txt", "SWE"): (635_000, FINLAND, "Finland 1750-1800 interpolation, rounded low"),
    ("00_west_europe.txt", "DENNOR"): (1_740_000, CLIO, "Denmark and Norway combined; overseas separate"),
    ("01_south_europe.txt", "SPA"): (10_540_000, CLIO, "metropolitan Spain"),
    ("01_south_europe.txt", "POR"): (2_510_000, CLIO, "metropolitan Portugal"),
    ("05_north_america.txt", "SC1"): (4_465_000, CLIO, "Mexico-area low anchor"),
    ("06_central_america.txt", "SC1"): (1_000_000, CLIO, "Central America low estimate"),
    ("05_north_america.txt", "QUE"): (90_000, CANADA, "Canadian 1775 total used as conservative cap"),
    ("05_north_america.txt", "ONT"): (8_000, "https://www65.statcan.ca/acyb02/1867/acyb02_1867001803-eng.htm", "Upper Canada 1775"),
    ("05_north_america.txt", "NVS"): (20_000, CANADA, "Nova Scotia/Atlantic low settler estimate"),
    ("05_north_america.txt", "HBC"): (100_000, CLIO, "conservative fur-trade territory estimate"),
    ("06_central_america.txt", "CUB"): (224_000, CLIO, "Cuba-area interpolation"),
    ("06_central_america.txt", "HAI"): (351_000, CLIO, "Saint-Domingue low anchor"),
    ("07_south_america.txt", "BRZ"): (2_020_000, CLIO, "Brazil-area interpolation"),
    ("07_south_america.txt", "SC2"): (2_150_000, CLIO, "New Granada/Quito/Venezuela low estimate"),
    ("07_south_america.txt", "SC3"): (2_100_000, CLIO, "Peru/Chile low estimate"),
    ("07_south_america.txt", "SC4"): (700_000, CLIO, "Rio de la Plata low estimate"),
    ("11_east_asia.txt", "JAP"): (28_480_000, CLIO, "Japan 1750-1800 interpolation"),
    ("11_east_asia.txt", "KOR"): (13_740_000, CLIO, "Korea low estimate"),
    ("11_east_asia.txt", "SIA"): (2_880_000, CLIO, "Thailand-area interpolation"),
    ("12_indonesia.txt", "DEI"): (6_800_000, CLIO, "Java/outer islands low estimate; disputed historical series"),
    ("12_indonesia.txt", "PHI"): (2_000_000, CLIO, "Philippines low estimate"),
    ("09_central_asia.txt", "NEP"): (3_760_000, CLIO, "Nepal 1750-1800 interpolation"),
}

# Modern-border historical series cannot identify every 1776 state precisely.
# These *provisional lower-bound* regional factors are intentionally marked as
# estimates in the output, pending dedicated regional research/map phase.
FILE_FACTORS = {
    "00_west_europe.txt": 0.78,
    "01_south_europe.txt": 0.78,
    "02_east_europe.txt": 0.80,
    "03_north_africa.txt": 0.94,
    "04_subsaharan_africa.txt": 0.94,
    "05_north_america.txt": 0.72,
    "06_central_america.txt": 0.72,
    "07_south_america.txt": 0.72,
    "08_middle_east.txt": 0.85,
    "09_central_asia.txt": 0.80,
    "11_east_asia.txt": 0.85,
    "12_indonesia.txt": 0.75,
    "14_siberia.txt": 0.80,
    "15_russia.txt": 0.78,
}

# These are reserved for a human or a cartographic follow-up, not rescaled.
PROTECTED_OWNERS = {"CHI", "GEN", "VEN"}
DEFERRED_STATES = {"STATE_TONKIN", "STATE_ANNAM", "STATE_MEKONG", "STATE_LAOS"}
DEFERRED_FILES = {"13_australasia.txt"}


@dataclass
class Pop:
    file: str
    state: str
    owner: str
    start: int
    end: int
    before: int
    after: int = 0
    decision: str = ""
    evidence: str = ""
    note: str = ""


def blocks(raw: str, pattern: str, depth: int):
    clean = parser.clean_comments(raw)
    depths, pairs = parser.brace_maps(clean)
    for match in re.finditer(pattern, clean, re.M):
        if depths[match.start()] != depth:
            continue
        opening = clean.index("{", match.start(), match.end())
        yield match.group(1), match.start(), pairs[opening] + 1


def scan_file(path: Path) -> tuple[str, list[Pop]]:
    raw = path.read_bytes().decode("utf-8")  # retain BOM and original CRLF/LF
    result = []
    for state, s0, s1 in blocks(raw, r"^[ \t]*(s:STATE_[A-Za-z0-9_]+)[ \t]*=[ \t]*\{", 1):
        state = state[2:]
        for owner, r0, r1 in blocks(raw[s0:s1], r"^[ \t]*(region_state:[A-Za-z0-9_]+)[ \t]*=[ \t]*\{", 1):
            owner = owner.split(":", 1)[1]
            for _, p0, p1 in blocks(raw[s0 + r0:s0 + r1], r"^[ \t]*(create_pop)[ \t]*=[ \t]*\{", 1):
                absolute = s0 + r0 + p0
                fragment = raw[absolute: s0 + r0 + p1]
                size = re.search(r"(?m)^[ \t]*size[ \t]*=[ \t]*(\d+)", fragment)
                if not size:
                    raise ValueError(f"No size: {path.name} {state} {owner}")
                result.append(Pop(path.name, state, owner, absolute + size.start(1), absolute + size.end(1), int(size.group(1))))
    return raw, result


def allocate(pops: list[Pop], target: int, decision: str, evidence: str, note: str):
    if not pops:
        raise ValueError(f"Empty target group: {decision}")
    if target < len(pops):
        raise ValueError(f"Target too small: {decision}")
    before = sum(p.before for p in pops)
    if before <= 0:
        raise ValueError(f"Zero baseline: {decision}")
    # Give every extant pop at least one person; use largest remainders for exact sum.
    remaining = target - len(pops)
    weights = [p.before for p in pops]
    floor = [remaining * n // before for n in weights]
    remainders = [remaining * n % before for n in weights]
    leftover = remaining - sum(floor)
    order = sorted(range(len(pops)), key=lambda i: (-remainders[i], i))
    for i, pop in enumerate(pops):
        pop.after = floor[i] + 1
        pop.decision, pop.evidence, pop.note = decision, evidence, note
    for i in order[:leftover]:
        pops[i].after += 1
    assert sum(p.after for p in pops) == target


def main():
    options = argparse.ArgumentParser(description=__doc__)
    options.add_argument("--apply", action="store_true", help="Apply targets once to the pre-pass pop files")
    args = options.parse_args()
    if not args.apply:
        validate()
        return
    if REPORT.exists():
        raise SystemExit(f"Refusing to re-apply an already recorded population pass: {REPORT}")
    files = {}
    all_pops = []
    for path in sorted(HISTORY.glob("*.txt")):
        raw, pops = scan_file(path)
        files[path.name] = (path, raw)
        all_pops.extend(pops)

    for pop in all_pops:
        if pop.owner in PROTECTED_OWNERS or pop.state in DEFERRED_STATES or pop.file in DEFERRED_FILES:
            pop.after = pop.before
            pop.decision = "PROTECTED" if pop.owner in PROTECTED_OWNERS else "DEFERRED_MAP"
            pop.note = "China/Genoa/Venice protected" if pop.owner in PROTECTED_OWNERS else "border/map rework"

    def pending(predicate):
        return [p for p in all_pops if not p.decision and predicate(p)]

    for state, target in USA_STATE_TARGETS.items():
        allocate(pending(lambda p, s=state: p.owner == "USA" and p.state == s), target, "US_STATE_CENSUS", CENSUS, "1770/1780 colonial interpolation; DC/WV apportioned conservatively")
    assert not pending(lambda p: p.owner == "USA"), "Uncovered USA states"

    for owner, (target, evidence, note) in OWNER_TARGETS.items():
        allocate(pending(lambda p, o=owner: p.owner == o), target, "COUNTRY_TARGET", evidence, note)
    for (file, owner), (target, evidence, note) in FILE_OWNER_TARGETS.items():
        allocate(pending(lambda p, f=file, o=owner: p.file == f and p.owner == o), target, "FILE_COUNTRY_TARGET", evidence, note)

    indian = pending(lambda p: p.file == "10_india.txt")
    allocate(indian, 190_000_000, "INDIA_LOW_REGIONAL_TARGET", CLIO, "conservative subcontinent estimate; provincial proportions inherited and provisional")

    # Apply conservative proxies state by state, not as a file-wide edit.
    buckets = defaultdict(list)
    for pop in pending(lambda p: True):
        buckets[(pop.file, pop.state, pop.owner)].append(pop)
    for (file, state, owner), pops in sorted(buckets.items()):
        factor = FILE_FACTORS[file]
        target = max(len(pops), round(sum(p.before for p in pops) * factor))
        allocate(pops, target, "PROVISIONAL_REGIONAL_LOW", CLIO, f"{file} regional lower-bound factor {factor}; revise with local census")
    assert all(p.decision for p in all_pops)

    summary = defaultdict(lambda: {"before": 0, "after": 0, "groups": 0, "decision": "", "evidence": "", "note": ""})
    for pop in all_pops:
        row = summary[(pop.file, pop.state, pop.owner)]
        row["before"] += pop.before
        row["after"] += pop.after
        row["groups"] += 1
        row["decision"] = pop.decision
        row["evidence"] = pop.evidence
        row["note"] = pop.note

    for file, (path, raw) in files.items():
        replacement = [p for p in all_pops if p.file == file and p.after != p.before]
        new = raw
        for pop in sorted(replacement, key=lambda p: p.start, reverse=True):
            assert new[pop.start:pop.end] == str(pop.before)
            new = new[:pop.start] + str(pop.after) + new[pop.end:]
        parser.brace_maps(parser.clean_comments(new))
        if new != raw:
            path.write_bytes(new.encode("utf-8"))

    REPORT.parent.mkdir(parents=True, exist_ok=True)
    with REPORT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["file", "state", "owner", "before", "target_1776", "delta", "groups", "decision", "evidence", "note"])
        for (file, state, owner), data in sorted(summary.items()):
            writer.writerow([file, state, owner, data["before"], data["after"], data["after"] - data["before"], data["groups"], data["decision"], data["evidence"], data["note"]])

    print(f"rows={len(summary)} groups={len(all_pops)} before={sum(p.before for p in all_pops):,} after={sum(p.after for p in all_pops):,}")
    print(f"changed_rows={sum(v['before'] != v['after'] for v in summary.values())} protected_rows={sum(v['decision'] == 'PROTECTED' for v in summary.values())} deferred_rows={sum(v['decision'] == 'DEFERRED_MAP' for v in summary.values())}")
    print(REPORT)


def validate():
    if not REPORT.exists():
        raise SystemExit(f"Missing target matrix: {REPORT}; use --apply on the pre-pass history")
    expected = {}
    with REPORT.open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = row["file"], row["state"], row["owner"]
            expected[key] = row
    baseline = defaultdict(lambda: {"population": 0, "groups": 0})
    with (REPORT.parent / "POPULATION_1776_BASELINE.csv").open(encoding="utf-8", newline="") as handle:
        for row in csv.DictReader(handle):
            key = row["file"], row["state"], row["owner"]
            baseline[key]["population"] += int(row["population"])
            baseline[key]["groups"] += int(row["groups"])
    if expected.keys() != baseline.keys():
        raise ValueError("Pre-pass baseline does not cover the same state-owner keys")
    observed = defaultdict(lambda: {"population": 0, "groups": 0})
    for path in sorted(HISTORY.glob("*.txt")):
        raw, pops = scan_file(path)
        parser.brace_maps(parser.clean_comments(raw))
        for pop in pops:
            if pop.before < 1:
                raise ValueError(f"Nonpositive pop in {path.name}: {pop.state}/{pop.owner}")
            row = observed[(pop.file, pop.state, pop.owner)]
            row["population"] += pop.before
            row["groups"] += 1
    if expected.keys() != observed.keys():
        raise ValueError(f"State-owner key mismatch: missing={expected.keys() - observed.keys()}, extra={observed.keys() - expected.keys()}")
    for key, row in expected.items():
        if observed[key]["population"] != int(row["target_1776"]):
            raise ValueError(f"Population target mismatch: {key}")
        if observed[key]["groups"] != int(row["groups"]):
            raise ValueError(f"Pop-group count mismatch: {key}")
        if baseline[key]["population"] != int(row["before"]) or baseline[key]["groups"] != int(row["groups"]):
            raise ValueError(f"Frozen pre-pass baseline mismatch: {key}")
        if row["decision"] in {"PROTECTED", "DEFERRED_MAP"} and row["before"] != row["target_1776"]:
            raise ValueError(f"Protected/deferred population changed: {key}")
    print(f"PASS: {len(expected)} state-owner targets, {sum(v['groups'] for v in observed.values())} pop groups, total {sum(v['population'] for v in observed.values()):,}")
    print(f"Protected/deferred rows: {sum(r['decision'] in {'PROTECTED', 'DEFERRED_MAP'} for r in expected.values())}")


if __name__ == "__main__":
    main()
