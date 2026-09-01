#!/usr/bin/env python3
"""Validate TECH6B3H and regenerate its row-by-row AFTER matrix."""

from __future__ import annotations

import csv
import hashlib
import re
import subprocess
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VANILLA = Path(r"C:\Games\Victoria 3\game")
REPORTS = ROOT / "docs/reports/technology"
MATRIX = REPORTS / "TECH6B3G_STARTING_TECH_RECONCILIATION_MATRIX.csv"
AFTER = REPORTS / "TECH6B3H_STARTING_TECH_RECONCILIATION_AFTER.csv"
TIER_FILE = ROOT / "common/scripted_effects/00_starting_inventions.txt"

EXPECTED_TIERS = {
    1: "shaft_mining coke_smelting improved_husbandry distillation organized_forestry traditional_papermaking traditional_food_processing organized_textile_production scientific_fortification_siegecraft state_dockyard_systems enclosed_dock_systems institutionalized_scientific_exchange international_relations institutionalized_public_credit stock_exchange commercial_insurance_markets periodical_print_networks atmospheric_engine advanced_crop_rotations precision_boring scientific_naval_architecture systematic_administrative_statistics".split(),
    2: "shaft_mining coke_smelting improved_husbandry distillation organized_forestry traditional_papermaking traditional_food_processing organized_textile_production scientific_fortification_siegecraft state_dockyard_systems enclosed_dock_systems institutionalized_scientific_exchange international_relations institutionalized_public_credit stock_exchange commercial_insurance_markets periodical_print_networks atmospheric_engine precision_boring".split(),
    3: "improved_husbandry organized_textile_production shaft_mining distillation coke_smelting applied_mineralogy light_infantry_tactics regulated_small_arms standardized_field_artillery urbanization codified_practical_knowledge systematic_administrative_statistics medical_degrees specialized_technical_academies commercial_insurance_markets international_relations".split(),
    4: "improved_husbandry organized_textile_production shaft_mining distillation light_infantry_tactics regulated_small_arms standardized_field_artillery urbanization codified_practical_knowledge systematic_administrative_statistics international_relations".split(),
    5: "improved_husbandry organized_textile_production shaft_mining urbanization codified_practical_knowledge systematic_administrative_statistics".split(),
    6: "improved_husbandry urbanization".split(),
    7: [],
}

VISIBLE_TIER_DECISIONS = [
    (1, "railways", "REMOVE", ""),
    (1, "mechanical_tools", "REPLACE", "precision_boring"),
    (1, "atmospheric_engine", "KEEP", "atmospheric_engine"),
    (1, "general_staff", "REMOVE", ""),
    (1, "percussion_cap", "REMOVE", ""),
    (2, "mechanical_tools", "REPLACE", "precision_boring"),
    (2, "atmospheric_engine", "KEEP", "atmospheric_engine"),
    (3, "shaft_mining", "KEEP", "shaft_mining"),
    (3, "distillation", "KEEP", "distillation"),
    (3, "cotton_gin", "REMOVE", ""),
    (3, "romanticism", "REMOVE", ""),
    (3, "international_relations", "KEEP", "international_relations"),
    (3, "colonization", "REMOVE", ""),
    (3, "medical_degrees", "KEEP", "medical_degrees"),
    (4, "shaft_mining", "KEEP", "shaft_mining"),
    (4, "distillation", "KEEP", "distillation"),
    (4, "international_relations", "KEEP", "international_relations"),
    (5, "shaft_mining", "KEEP", "shaft_mining"),
]

PROTECTED_FAMILIES = {
    "common/technology/technologies": "32e458e57bf6ab3bb0b0e3eccaed4368fae9d4d69cd3ea229a4bcb0b2d12fd86",
    "common/buildings": "32fb95920b2165a1ac78572087a0c914720b0a4a1d4569ed281d13feb726256c",
    "common/production_methods": "0195e42b9bf06756d6ea868622c37c102514d16b6a12f9167912be96c2b2a4a5",
    "common/laws": "e1e90e150f6e1911d64efc7cd4266acc621c4c952b597e3d0f1d885ae623eb6c",
    "gui": "2d7fb11f331f8247df15299ad237c4023e00699f23502f5bd8977aedcee128e6",
}

GRANT_RE = re.compile(r"(?m)^\s*add_technology_researched\s*=\s*([A-Za-z0-9_]+)\s*(?:#.*)?$")
TIER_CALL_RE = re.compile(r"(?m)^\s*effect_starting_technology_tier_([1-7])_tech\s*=\s*yes\s*(?:#.*)?$")
TOP_OBJECT_RE = re.compile(r"(?m)^([A-Za-z0-9_.:-]+)\s*=\s*\{")


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("cp1252")


def clean(text: str) -> str:
    return "\n".join(line.split("#", 1)[0] for line in text.splitlines())


def grants(path: Path) -> list[str]:
    return GRANT_RE.findall(clean(read_text(path)))


def balanced(text: str) -> bool:
    depth = 0
    quote = False
    escape = False
    comment = False
    for char in text:
        if comment:
            if char in "\r\n":
                comment = False
            continue
        if quote:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                quote = False
            continue
        if char == "#":
            comment = True
        elif char == '"':
            quote = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth < 0:
                return False
    return depth == 0 and not quote


def tier_blocks() -> dict[int, list[str]]:
    text = read_text(TIER_FILE)
    result: dict[int, list[str]] = {}
    for tier in range(1, 8):
        marker = f"effect_starting_technology_tier_{tier}_tech"
        start_match = re.search(rf"(?m)^{re.escape(marker)}\s*=\s*\{{", text)
        assert start_match, marker
        depth = 0
        end = None
        for index in range(start_match.end() - 1, len(text)):
            if text[index] == "{":
                depth += 1
            elif text[index] == "}":
                depth -= 1
                if depth == 0:
                    end = index + 1
                    break
        assert end is not None
        result[tier] = GRANT_RE.findall(clean(text[start_match.start():end]))
    return result


def effective_country_files() -> dict[str, Path]:
    result: dict[str, Path] = {}
    rel = Path("common/history/countries")
    for base in (VANILLA, ROOT):
        for path in sorted((base / rel).glob("*.txt")):
            result[path.name.casefold()] = path
    return result


def family_hash(rel: str) -> str:
    digest = hashlib.sha256()
    for path in sorted(p for p in (ROOT / rel).rglob("*") if p.is_file()):
        digest.update(path.relative_to(ROOT).as_posix().encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def tech_ids() -> set[str]:
    result: set[str] = set()
    for path in sorted((ROOT / "common/technology/technologies").glob("*.txt")):
        result.update(TOP_OBJECT_RE.findall(clean(read_text(path))))
    return result


def explicit_and_expanded(path: Path, tiers: dict[int, list[str]]) -> tuple[list[str], list[str]]:
    text = clean(read_text(path))
    explicit = GRANT_RE.findall(text)
    tier_calls = [int(value) for value in TIER_CALL_RE.findall(text)]
    raw = [f"tier_{tier}_tech" for tier in tier_calls] + explicit
    expanded: list[str] = []
    for tier in tier_calls:
        expanded.extend(tiers[tier])
    expanded.extend(explicit)
    return raw, expanded


def actual_source(row: dict[str, str], countries: dict[str, Path]) -> Path:
    if row["country_tag"] == "HBC":
        return countries["hbc - hudson bay company.txt"]
    if row["country_tag"] == "VNZ":
        return countries["vnz - venezuela.txt"]
    return countries[Path(row["source_file"]).name.casefold()]


def main() -> int:
    with MATRIX.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 229
    assert Counter(row["grant_type"] for row in rows) == Counter({"DIRECT_COUNTRY": 165, "SCRIPTED_TIER": 64})
    # TECH6B3H backports START-01/02/03 into the former audit matrix.
    assert sum(row["human_review_required"] == "YES" for row in rows) == 0

    tiers = tier_blocks()
    assert tiers == EXPECTED_TIERS, {key: (tiers[key], EXPECTED_TIERS[key]) for key in tiers if tiers[key] != EXPECTED_TIERS[key]}
    tier_text = read_text(TIER_FILE)
    assert "add_era_researched" not in clean(tier_text)
    assert balanced(tier_text)
    assert sum(tech == "urbanization" for values in tiers.values() for tech in values) == 4
    assert all("urbanization" not in tiers[tier] for tier in (1, 2, 7))

    assert len(VISIBLE_TIER_DECISIONS) == 18
    for tier, old, action, target in VISIBLE_TIER_DECISIONS:
        if action == "REMOVE":
            assert old not in tiers[tier], (tier, old)
        elif action == "KEEP":
            assert old in tiers[tier], (tier, old)
        else:
            assert old not in tiers[tier] and target in tiers[tier], (tier, old, target)

    countries = effective_country_files()
    assert sum(name.startswith("hbc - ") for name in countries) == 1
    assert sum(name.startswith("vnz - ") for name in countries) == 1
    assert not (ROOT / "common/history/countries/hbc - hubson bay company.txt").exists()
    assert not (ROOT / "common/history/countries/vnz - venezula.txt").exists()
    hbc = countries["hbc - hudson bay company.txt"]
    vnz = countries["vnz - venezuela.txt"]
    hbc_raw, hbc_expanded = explicit_and_expanded(hbc, tiers)
    vnz_raw, vnz_expanded = explicit_and_expanded(vnz, tiers)
    assert hbc_expanded.count("institutionalized_scientific_exchange") == 1
    assert hbc_expanded.count("regulated_small_arms") == 1
    assert hbc_expanded.count("mandatory_service") == 0
    assert "tier_4_tech" in hbc_raw
    assert vnz_expanded.count("institutionalized_scientific_exchange") == 1
    assert "tier_4_tech" in vnz_raw and "tier_3_tech" not in vnz_raw
    assert "empiricism" not in vnz_expanded and "academia" not in vnz_expanded

    per = countries["per - persia.txt"]
    per_raw, per_expanded = explicit_and_expanded(per, tiers)
    assert per_raw.count("state_dockyard_systems") == 1
    assert "admiralty" not in per_expanded

    known = tech_ids()
    assert len(known) == 285
    targets = {row["recommended_target_tech"] for row in rows if row["recommended_target_tech"]}
    assert targets <= known, sorted(targets - known)
    assert all(tech in known for values in tiers.values() for tech in values)

    hidden = {row["hidden_tech_id"] for row in rows}
    hidden_active: list[tuple[str, str]] = []
    duplicate_files: list[tuple[str, list[str]]] = []
    unknown_country_grants: list[tuple[str, str]] = []
    country_cache: dict[Path, tuple[list[str], list[str]]] = {}
    for name, path in countries.items():
        raw, expanded = explicit_and_expanded(path, tiers)
        country_cache[path] = (raw, expanded)
        duplicates = sorted(tech for tech, count in Counter(expanded).items() if count > 1)
        if duplicates:
            duplicate_files.append((name, duplicates))
        for tech in expanded:
            if tech in hidden:
                hidden_active.append((name, tech))
            if not tech.startswith("tier_") and tech not in known:
                unknown_country_grants.append((name, tech))
    assert not duplicate_files, duplicate_files
    assert not unknown_country_grants, unknown_country_grants
    assert Counter(tech for _, tech in hidden_active) == Counter({"urbanization": 397}), Counter(tech for _, tech in hidden_active)
    # The alias appears in four tier definitions and expands across 397 effective country setups.
    assert all(tech == "urbanization" for _, tech in hidden_active)

    after_rows: list[dict[str, str]] = []
    inactive = 0
    removed_active = 0
    retained = 0
    for row in rows:
        old = row["hidden_tech_id"]
        target = row["recommended_target_tech"]
        if row["grant_type"] == "SCRIPTED_TIER":
            tier = int(re.search(r"tier_([1-7])", row["tier_effect"]).group(1))
            final = tiers[tier]
            effective = TIER_FILE.relative_to(ROOT).as_posix()
            provider = row["tier_effect"] if target and target in final else ""
            old_after = final.count(old)
            target_after = final.count(target) if target else 0
            if row["recommended_action"] == "KEEP_HIDDEN_ALIAS_COMPATIBILITY_ONLY":
                assert old_after == 1
                status = "COMPATIBILITY_RETAINED"
                retained += 1
            else:
                assert old_after == 0
                if target:
                    assert target_after == 1
                status = "IMPLEMENTED"
                removed_active += 1
        else:
            path = actual_source(row, countries)
            _, final = country_cache[path]
            effective = path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else path.relative_to(VANILLA).as_posix()
            old_after = final.count(old)
            target_after = final.count(target) if target else 0
            provider = "DIRECT_OR_EXPANDED_TIER" if target_after else ""
            if row["effective_layer"] == "vanilla_shadowed_by_mod_casefold":
                assert old_after == 0
                status = "ALREADY_INACTIVE_CASEFOLD_SHADOW"
                inactive += 1
            else:
                assert old_after == 0, (row["index"], row["country_tag"], old, path)
                if target:
                    assert target_after == 1, (row["index"], row["country_tag"], target, path, final)
                status = "IMPLEMENTED"
                removed_active += 1
        after_rows.append({
            "index": row["index"],
            "hidden_tech_id": old,
            "grant_type": row["grant_type"],
            "country_tag": row["country_tag"],
            "tier_effect": row["tier_effect"],
            "source_file_before": row["source_file"],
            "effective_file_after": effective,
            "approved_action": row["recommended_action"],
            "approved_target": target,
            "implementation_status": status,
            "old_grant_after": str(old_after),
            "target_grant_after_expansion": str(target_after),
            "final_provider": provider,
            "expanded_duplicate_count": "0",
            "validation": "PASS",
            "notes": "START-01" if row["country_tag"] == "HBC" else "START-02" if row["country_tag"] == "VNZ" else "START-03" if row["country_tag"] == "PER" and old == "admiralty" else "",
        })
    assert Counter(row["implementation_status"] for row in after_rows) == Counter({"IMPLEMENTED": 221, "ALREADY_INACTIVE_CASEFOLD_SHADOW": 4, "COMPATIBILITY_RETAINED": 4})
    assert removed_active == 221 and inactive == 4 and retained == 4

    for path in {TIER_FILE, *country_cache}:
        assert balanced(read_text(path)), path
    for rel, expected in PROTECTED_FAMILIES.items():
        assert family_hash(rel) == expected, (rel, family_hash(rel), expected)

    branch = subprocess.run(["git", "branch", "--show-current"], cwd=ROOT, check=True, text=True, capture_output=True).stdout.strip()
    assert branch == "tech6b3h-starting-tech-reconciliation-implementation"
    diff_check = subprocess.run(["git", "diff", "--check"], cwd=ROOT, text=True, capture_output=True)
    assert diff_check.returncode == 0, diff_check.stdout + diff_check.stderr

    with AFTER.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(after_rows[0]))
        writer.writeheader()
        writer.writerows(after_rows)

    print("TECH6B3H_STATIC_VALIDATION = PASS")
    print(f"BRANCH = {branch}")
    print(f"INPUT_ROWS = {len(rows)}")
    print("DIRECT_ROWS = 165")
    print("TIER_ROWS = 64")
    print("VISIBLE_TIER_DECISIONS = 18")
    print(f"EFFECTIVE_COUNTRY_SETUPS = {len(countries)}")
    print("HBC_EFFECTIVE_SETUP_COUNT = 1")
    print("VNZ_EFFECTIVE_SETUP_COUNT = 1")
    print("HIDDEN_STARTING_GRANTS_REMOVED = 221")
    print("INPUT_ROWS_ALREADY_INACTIVE = 4")
    print("HIDDEN_STARTING_GRANTS_RETAINED_FOR_RUNTIME_COMPATIBILITY = 4")
    print("FINAL_DUPLICATE_VISIBLE_GRANTS = 0")
    print("UNKNOWN_TECH_IDS = 0")
    print("PROTECTED_FAMILY_HASHES = PASS")
    print(f"AFTER_MATRIX_ROWS = {len(after_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
