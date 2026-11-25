"""Build four nested candidate cohorts from the 1776 country inventory."""
import argparse
import csv
import json
from pathlib import Path
import re

HRE_KEY_COUNTRIES = set("AUS KPF KTR KMZ KCL PRU SAX HAN BAV HES WUR BAD LGE SAR TUS".split())
CHINESE_ADMINISTRATIONS = {"YUN", "XIN", "MGL"}
BALKAN_MINOR_POWERS = {"MON", "RAG", "MOL", "WAL", "TRS"}
KEY_COUNTRIES = set("PAP SWI NET VEN GEN POR GRE SER RUM EIC BIC MUG USA GBR FRA SPA CHI RUS TUR HUN KZH".split())
PREFERRED_REGIONS = set("""
region_east_africa region_west_africa region_equatorial_africa region_southern_africa
region_north_africa region_nile_basin region_balkans region_near_east region_arabia
region_greater_persia region_north_india region_south_india region_himalayas
""".split())
THRESHOLDS = ((50_000, 4, 2), (100_000, 8, 3), (250_000, 16, 4), (500_000, 25, 6))


def membership():
    raw = Path("common/scripted_triggers/1776_imperial_constitution.txt").read_text(encoding="utf-8-sig")
    first_trigger = raw.split("\naor1776_hre_emperor =", 1)[0]
    return set(re.findall(r"\bc:([A-Z0-9]{3})\b", first_trigger))


def classify(row, hre):
    tag = row["tag"]
    region = row["capital_region"]
    priority_region = tag in hre or region in PREFERRED_REGIONS
    population = int(row["population"])
    provinces = int(row["province_count"])
    fragments = int(row["state_fragments"])
    if tag in HRE_KEY_COUNTRIES:
        return None, "Saint-Empire : électorat, gouvernement majeur ou rôle impérial"
    if tag in KEY_COUNTRIES:
        return None, "Protégé : puissance ou contenu national structurant"
    if tag in CHINESE_ADMINISTRATIONS:
        return 50_000, "Administration chinoise nommément ciblée"
    if tag in BALKAN_MINOR_POWERS:
        return 50_000, "Entité balkanique nommément ciblée"
    if row["controller"] != "yes" or not provinces:
        return None, "Contrôleur ou territoire absent"
    for threshold, max_provinces, max_fragments in THRESHOLDS:
        if population > threshold or provinces > max_provinces or fragments > max_fragments:
            continue
        if priority_region or threshold >= 250_000 or provinces == 1:
            label = "Saint-Empire" if tag in hre else ("Région prioritaire" if priority_region else "Autre région")
            return threshold, label + " : limite de population, de provinces et de fragments"
    return None, "Hors seuils de population ou de territoire"


def run(source, output):
    hre = membership()
    with source.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        threshold, reason = classify(row, hre)
        row.update(first_threshold=threshold, gameplay_relevance=reason)
    output.mkdir()
    with (output / "INVENTAIRE_PAYS.csv").open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    active = sum(row["controller"] == "yes" for row in rows)
    cohorts = {}
    for threshold, _, _ in THRESHOLDS:
        affected = [dict(tag=row["tag"], name=row["name"], reason=row["gameplay_relevance"])
                    for row in rows if row["first_threshold"] and row["first_threshold"] <= threshold]
        cohorts[threshold] = dict(affected=affected, disabled=len(affected), active_if_disabled=active-len(affected))
    (output / "COHORTES.json").write_text(json.dumps(cohorts, indent=2, ensure_ascii=False), encoding="utf-8")
    print({threshold: (record["disabled"], record["active_if_disabled"]) for threshold, record in cohorts.items()})


if __name__ == "__main__":
    cli = argparse.ArgumentParser()
    cli.add_argument("source", type=Path)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    run(args.source, args.output)

