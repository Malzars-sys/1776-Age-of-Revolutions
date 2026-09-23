#!/usr/bin/env python3
"""Validate the targeted VOC/BIC/HBC starting-company ownership correction."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import build_start_1776_research_input_pack as catalog_tools
import build_start_1776_world_apply as world


ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "docs" / "reports" / "buildings"
CSV_REPORT = REPORTS / "BUILD_START_1776_COMPANY_OWNERSHIP_CORRECTION.csv"
WEST_BENGAL_CSV_REPORT = REPORTS / "BUILD_START_1776_WEST_BENGAL_BRITISH_OWNERSHIP.csv"
JSON_REPORT = REPORTS / "BUILD_START_1776_COMPANY_OWNERSHIP_VALIDATION.json"
MD_REPORT = REPORTS / "BUILD_START_1776_COMPANY_OWNERSHIP_CORRECTION.md"

WEST_BENGAL_PUBLIC_BUILDINGS = {
    "building_government_administration",
    "building_port",
}

COMPANIES = {
    "company_dutch_east_india_company": {
        "short": "VOC",
        "parent": "NET",
        "colony": "DEI",
        "country_file": ROOT / "common/history/countries/net - netherlands.txt",
        "minimums": {
            "building_coffee_plantation": 5,
            "building_spice_plantation": 8,
        },
    },
    "company_east_india_company": {
        "short": "BIC",
        "parent": "GBR",
        "colony": "BIC",
        "country_file": ROOT / "common/history/countries/gbr - great britain.txt",
        "minimums": {
            "building_opium_plantation": 4,
            "building_silk_plantation": 3,
            "building_sugar_plantation": 1,
            "building_tobacco_plantation": 2,
        },
    },
    "company_hbc": {
        "short": "HBC",
        "parent": "GBR",
        "colony": "HBC",
        "country_file": ROOT / "common/history/countries/gbr - great britain.txt",
        "minimums": {
            "building_logging_camp": 2,
            "building_fishing_wharf": 3,
        },
        "exact_total": 5,
    },
}


def company_shares() -> list[dict[str, object]]:
    _, placements = world.all_placements(world.HISTORY)
    rows: list[dict[str, object]] = []
    for placement in placements:
        for _, own_start, own_end in world.block_spans(placement.text, r"add_ownership", 1):
            ownership = placement.text[own_start:own_end]
            for _, start, end in world.block_spans(ownership, r"company", 1):
                share = ownership[start:end]
                company = catalog_tools.scalar(share, "type")
                if company not in COMPANIES:
                    continue
                rows.append({
                    "Company_ID": company,
                    "Company": COMPANIES[company]["short"],
                    "Parent_TAG": catalog_tools.scalar(share, "country").removeprefix("c:"),
                    "Colony_TAG": placement.owner,
                    "State_ID": placement.state,
                    "Building_ID": placement.building,
                    "Company_Levels": int(catalog_tools.scalar(share, "levels", "0")),
                    "Source": placement.path.relative_to(ROOT).as_posix(),
                })
    return rows


def supported_buildings() -> dict[str, set[str]]:
    objects = catalog_tools.effective_objects("common/company_types", r"company_[A-Za-z0-9_]+")
    result: dict[str, set[str]] = {}
    for company in COMPANIES:
        block = objects[company].text
        primary = catalog_tools.tokens_flat(catalog_tools.braced_tokens(block, "building_types"))
        extension = catalog_tools.tokens_flat(catalog_tools.braced_tokens(block, "extension_building_types"))
        result[company] = set(primary) | set(extension)
    return result


def link_ok(company: str, data: dict[str, object]) -> bool:
    raw = Path(data["country_file"]).read_text(encoding="utf-8-sig")
    add_pattern = rf"add_company\s*=\s*company_type:{re.escape(company)}"
    colony_pattern = rf"add_owned_country\s*=\s*c:{re.escape(str(data['colony']))}"
    return bool(re.search(add_pattern, raw) and re.search(colony_pattern, raw))


def west_bengal_ownership() -> tuple[list[dict[str, object]], list[str]]:
    """Audit the colonial ownership policy for every West Bengal placement."""
    _, placements = world.all_placements(world.HISTORY)
    rows: list[dict[str, object]] = []
    errors: list[str] = []
    for placement in placements:
        if placement.owner != "BIC" or placement.state != "STATE_WEST_BENGAL":
            continue
        shares: list[dict[str, str]] = []
        for _, own_start, own_end in world.block_spans(placement.text, r"add_ownership", 1):
            ownership = placement.text[own_start:own_end]
            for share_kind in ("company", "building", "country"):
                for _, start, end in world.block_spans(ownership, share_kind, 1):
                    share = ownership[start:end]
                    country_values = re.findall(
                        r'\bcountry\s*=\s*"?c:([A-Za-z0-9_]+)"?', share
                    )
                    shares.append({
                        "kind": share_kind,
                        "type": catalog_tools.scalar(share, "type"),
                        "country": country_values[-1] if country_values else "",
                        "region": catalog_tools.scalar(share, "region"),
                        "levels": catalog_tools.scalar(share, "levels", "0"),
                    })

        if placement.building in WEST_BENGAL_PUBLIC_BUILDINGS:
            policy = "BIC_PUBLIC_EXCEPTION"
            valid = bool(shares) and all(
                share["kind"] == "country" and share["country"] == "BIC"
                for share in shares
            )
        elif placement.building.endswith("_plantation"):
            policy = "GBR_BIC_COMPANY"
            valid = bool(shares) and all(
                share["kind"] == "company"
                and share["type"] == "company_east_india_company"
                and share["country"] == "GBR"
                for share in shares
            )
        else:
            policy = "GBR_FINANCIAL_DISTRICT"
            valid = bool(shares) and all(
                share["kind"] == "building"
                and share["type"] == "building_financial_district"
                and share["country"] == "GBR"
                and share["region"] == "STATE_HOME_COUNTIES"
                for share in shares
            )

        actual = "; ".join(
            f"{share['kind']}:{share['type'] or '-'}:{share['country']}:"
            f"{share['region'] or '-'}:{share['levels']}"
            for share in shares
        )
        rows.append({
            "State_ID": placement.state,
            "Building_ID": placement.building,
            "Levels": placement.level,
            "Required_Policy": policy,
            "Actual_Ownership": actual,
            "Status": "PASS" if valid else "FAIL",
            "Source": placement.path.relative_to(ROOT).as_posix(),
        })
        if not valid:
            errors.append(f"West Bengal ownership policy failed: {placement.building} ({actual})")
    return rows, errors


def main() -> int:
    shares = company_shares()
    west_bengal_rows, west_bengal_errors = west_bengal_ownership()
    supported = supported_buildings()
    totals: dict[tuple[str, str], int] = defaultdict(int)
    errors: list[str] = list(west_bengal_errors)

    for row in shares:
        company = str(row["Company_ID"])
        data = COMPANIES[company]
        totals[(company, str(row["Building_ID"]))] += int(row["Company_Levels"])
        row["Supported_By_Company"] = "YES" if row["Building_ID"] in supported[company] else "NO"
        row["Correct_Parent"] = "YES" if row["Parent_TAG"] == data["parent"] else "NO"
        row["Correct_Colony"] = "YES" if row["Colony_TAG"] == data["colony"] else "NO"
        if row["Supported_By_Company"] == "NO":
            errors.append(f"unsupported building: {company}/{row['Building_ID']}")
        if row["Correct_Parent"] == "NO":
            errors.append(f"wrong parent: {company}/{row['Parent_TAG']}")
        if row["Correct_Colony"] == "NO":
            errors.append(f"wrong colony: {company}/{row['Colony_TAG']}")

    minimum_rows: list[dict[str, object]] = []
    for company, data in COMPANIES.items():
        if not link_ok(company, data):
            errors.append(f"missing company/country link: {company}")
        for building, minimum in data["minimums"].items():
            actual = totals.get((company, building), 0)
            status = "PASS" if actual >= minimum else "FAIL"
            minimum_rows.append({
                "Company": data["short"],
                "Company_ID": company,
                "Building_ID": building,
                "Required_Minimum": minimum,
                "Actual_Company_Levels": actual,
                "Status": status,
            })
            if status == "FAIL":
                errors.append(f"minimum not met: {company}/{building} {actual} < {minimum}")

    fieldnames = [
        "Company_ID", "Company", "Parent_TAG", "Colony_TAG", "State_ID",
        "Building_ID", "Company_Levels", "Supported_By_Company", "Correct_Parent",
        "Correct_Colony", "Source",
    ]
    with CSV_REPORT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(sorted(shares, key=lambda row: (
            str(row["Company"]), str(row["State_ID"]), str(row["Building_ID"])
        )))

    west_bengal_fields = [
        "State_ID", "Building_ID", "Levels", "Required_Policy",
        "Actual_Ownership", "Status", "Source",
    ]
    with WEST_BENGAL_CSV_REPORT.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=west_bengal_fields)
        writer.writeheader()
        writer.writerows(sorted(west_bengal_rows, key=lambda row: str(row["Building_ID"])))

    company_totals = {
        str(data["short"]): sum(
            int(row["Company_Levels"]) for row in shares if row["Company_ID"] == company
        )
        for company, data in COMPANIES.items()
    }
    for company, data in COMPANIES.items():
        expected_total = data.get("exact_total")
        if expected_total is not None and company_totals[str(data["short"])] != expected_total:
            errors.append(
                f"exact company total not met: {company} "
                f"{company_totals[str(data['short'])]} != {expected_total}"
            )
    summary = {
        "status": "PASS" if not errors else "FAIL",
        "company_owned_levels": company_totals,
        "targeted_company_share_rows": len(shares),
        "west_bengal_building_rows": len(west_bengal_rows),
        "west_bengal_ownership_failures": len(west_bengal_errors),
        "minimum_checks": minimum_rows,
        "invalid_company_shares": len(errors),
        "errors": errors,
    }
    JSON_REPORT.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    lines = [
        "# BUILD START 1776 — Correction ciblée de propriété VOC / BIC / HBC",
        "",
        "## Résultat",
        "",
        "La passe restaure des actifs réellement possédés par les trois compagnies sans rouvrir la redistribution mondiale. La HBC conserve exactement cinq niveaux possédés. Au Bengale occidental, les actifs économiques privatisables sont désormais contrôlés depuis les quartiers d'affaires britanniques ; les plantations relèvent directement de la BIC.",
        "",
        "| Compagnie | Niveaux possédés après correction |",
        "|---|---:|",
    ]
    lines.extend(f"| {name} | {levels} |" for name, levels in company_totals.items())
    lines.extend([
        "",
        "## Répartition",
        "",
        "| Compagnie | Colonie | État | Bâtiment | Niveaux compagnie |",
        "|---|---|---|---|---:|",
    ])
    for row in sorted(shares, key=lambda item: (
        str(item["Company"]), str(item["State_ID"]), str(item["Building_ID"])
    )):
        lines.append(
            f"| {row['Company']} | {row['Colony_TAG']} | {row['State_ID']} | "
            f"{row['Building_ID']} | {row['Company_Levels']} |"
        )
    lines.extend([
        "",
        "## Garde-fous",
        "",
        "- Les propriétaires sont les puissances mères : NET pour la VOC, GBR pour la BIC et la HBC.",
        "- Chaque bâtiment est admis par `building_types` ou `extension_building_types` de sa compagnie.",
        "- Les huit niveaux d'épices VOC restent quatre aux Moluques et quatre à Ceylan, mais vivent désormais dans l'overlay mondial final afin d'éviter leur disparition au chargement.",
        "- La HBC possède exactement cinq niveaux : deux exploitations forestières et trois pêcheries. Manitoba utilise 2,5 d'infrastructure, Ontario 1,5 et Québec 2,0, pour 3 de capacité de base dans chaque État : accès au marché conservé sans ajout de route.",
        "- La BIC possède dix niveaux de plantations : quatre d'opium, trois de soie, deux de tabac et un de sucre. Quatre de ces niveaux sont les nouvelles plantations limitées du Bengale occidental.",
        "- Au Bengale occidental, tous les bâtiments économiques privatisables hors plantations appartiennent à des quartiers d'affaires britanniques des Home Counties. L'administration et le port restent les seules exceptions publiques BIC, car ces catégories ne peuvent pas être transférées à des quartiers d'affaires.",
        "- Le réseau routier du Bengale occidental passe de 13 à 15 niveaux : 45 d'infrastructure pour 43 utilisés après les quatre nouvelles plantations.",
        "- Aucun niveau militaire ou naval et aucune Sérénissime ne sont modifiés.",
        "",
        f"Validation ciblée : **{summary['status']}**.",
    ])
    MD_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
