#!/usr/bin/env python3
"""Validation QA non interactive de TECH6C5D.

Ce script ne lance pas Victoria 3. Il rejoue les validateurs cuivre/aluminium,
controle le diff Git, quelques invariants d'integration et le dernier journal
de demarrage disponible. Les controles d'interface et d'economie restent a la
charge de l'operateur.
"""

from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Games\Victoria 3\game")
LOGS = Path.home() / "Documents/Paradox Interactive/Victoria 3/logs"

ERROR_TERMS = (
    "copper",
    "aluminium",
    "industrial_chemicals",
    "refined_fuels",
    "lubricants",
    "heavy_petroleum_products",
    "building_copper_mine",
    "building_non_ferrous_metallurgy_works",
    "pm_hall_heroult_process",
    "pm_all_metal_aircraft",
    "pmg_electrical_conductors_building_power_plant",
)

EXPECTED_SAMPLES = {
    "STATE_KATANGA": (60, "WORLD_CLASS"),
    "STATE_UTAH": (48, "VERY_HIGH"),
    "STATE_WEST_COUNTRY": (36, "HIGH"),
    "STATE_SVEALAND": (24, "MEDIUM"),
    "STATE_GOTALAND": (16, "MODEST"),
    "STATE_LOWLANDS": (8, "LOW"),
    "STATE_SCANIA": (0, "NONE"),
}

failures: list[str] = []


def check(label: str, condition: bool, detail: str = "") -> None:
    status = "PASS" if condition else "FAIL"
    suffix = f" - {detail}" if detail else ""
    print(f"{label}: {status}{suffix}")
    if not condition:
        failures.append(label)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def run_validator(filename: str) -> None:
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / filename)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        encoding="utf-8",
    )
    output = (result.stdout + result.stderr).strip()
    check(filename, result.returncode == 0 and output.endswith("PASS"), output)


def state_block(text: str, state_id: str) -> str:
    match = re.search(rf"(?m)^{re.escape(state_id)}\s*=\s*\{{", text)
    if not match:
        return ""
    opening = text.find("{", match.start(), match.end())
    depth = 0
    for pos in range(opening, len(text)):
        if text[pos] == "{":
            depth += 1
        elif text[pos] == "}":
            depth -= 1
            if depth == 0:
                return text[match.start() : pos + 1]
    return ""


run_validator("tech6c5b_validate.py")
run_validator("tech6c5c_validate.py")

diff_check = subprocess.run(
    ["git", "diff", "--check"],
    cwd=ROOT,
    text=True,
    capture_output=True,
    encoding="utf-8",
)
check("git diff --check", diff_check.returncode == 0, diff_check.stdout.strip())

branch = subprocess.check_output(
    ["git", "branch", "--show-current"], cwd=ROOT, text=True, encoding="utf-8"
).strip()
check(
    "branche attendue",
    branch == "tech6c-goods-buildings-pm-implementation",
    branch,
)

copper_pm = read(ROOT / "common/production_methods/13_tech6c5b_copper_production_and_consumers.txt")
aluminium_pm = read(ROOT / "common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt")
aluminium_building = read(ROOT / "common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt")
power_building = read(ROOT / "common/buildings/06_urban_center.txt")
east_asia_history = read(ROOT / "common/history/buildings/11_east_asia.txt")
copper_coast = read(ROOT / "common/state_traits/12_oceania_traits.txt")

check(
    "diesel cuivre utilise refined_fuels",
    "goods_input_refined_fuels_add = 3" in copper_pm
    and "pm_diesel_pump_building_copper_mine" in copper_pm,
)
check(
    "concentration du minerai",
    all(
        token in copper_pm
        for token in (
            "geological_surveying",
            "goods_input_tools_add = 5",
            "goods_input_industrial_chemicals_add = 5",
            "goods_output_copper_add = 10",
        )
    ),
)
check(
    "double verrou batiment aluminium",
    all(token in aluminium_building for token in ("electrical_capacitors", "industrial_alkalis")),
)
check(
    "recette Hall-Heroult",
    all(
        token in aluminium_pm
        for token in (
            "goods_input_industrial_chemicals_add = 20",
            "goods_input_coal_add = 10",
            "goods_input_electricity_add = 50",
            "goods_output_aluminium_add = 40",
            "state_pollution_generation_add = 20",
        )
    ),
)
check(
    "avion tout metal",
    all(
        token in aluminium_pm
        for token in (
            "military_aviation",
            "goods_input_aluminium_add = 10",
            "goods_output_automobiles_add = -10",
            "goods_output_aeroplanes_add = 20",
            "building_employment_engineers_add = 500",
        )
    )
    and "goods_input_hardwood_add" not in aluminium_pm
    and "goods_input_fabric_add" not in aluminium_pm,
)
check(
    "PMG conducteurs rattache a la centrale",
    "pmg_electrical_conductors_building_power_plant" in power_building,
)
check(
    "conducteurs mutuellement exclusifs",
    "goods_input_copper_add = 2" in aluminium_pm
    and "goods_input_aluminium_add = 1" in aluminium_pm,
)
check(
    "Ashio migre vers le cuivre",
    'building="building_copper_mine"' in east_asia_history
    and 'type="building_copper_mine"' in east_asia_history,
)
check(
    "trait Copper Coast",
    "building_copper_mine_throughput_add = 0.1" in copper_coast
    and "building_iron_mine_throughput_add = 0.1" in copper_coast,
)

matrix_path = ROOT / "docs/reports/industry/TECH6C5B_COPPER_GLOBAL_RESOURCE_MATRIX.csv"
with matrix_path.open(encoding="utf-8-sig", newline="") as handle:
    matrix = {row["state_id"]: row for row in csv.DictReader(handle)}

region_texts = {
    path.relative_to(ROOT).as_posix(): read(path)
    for path in (ROOT / "map_data/state_regions").glob("*.txt")
}
for state_id, (expected_potential, expected_tier) in EXPECTED_SAMPLES.items():
    row = matrix.get(state_id)
    matrix_ok = bool(
        row
        and int(row["potential"]) == expected_potential
        and row["tier"] == expected_tier
    )
    map_ok = False
    if row:
        block = state_block(region_texts.get(row["state_region_file"], ""), state_id)
        match = re.search(r"building_copper_mine\s*=\s*(\d+)", block)
        actual = int(match.group(1)) if match else 0
        map_ok = actual == expected_potential
    check(f"ressource echantillon {state_id}", matrix_ok and map_ok, f"{expected_tier}={expected_potential}")

ai_defines = read(GAME / "common/defines/00_ai.txt") if GAME.exists() else ""
check(
    "selection IA fondee sur l'economie",
    all(
        token in ai_defines
        for token in (
            "PRODUCTION_METHOD_PROFIT_FACTOR",
            "PRODUCTION_METHOD_DEFICIT_FACTOR",
            "PRODUCTION_METHOD_UNDESIRABLE_GOODS_PRICE_THRESHOLD",
            "PRODUCTION_METHOD_CHANCE_TO_CHANGE",
        )
    ),
)

scoped_hits: list[str] = []
for filename in ("error.log", "warning.log"):
    path = LOGS / filename
    if not path.exists():
        continue
    for line_number, line in enumerate(read(path).splitlines(), 1):
        lowered = line.lower()
        if any(term in lowered for term in ERROR_TERMS):
            scoped_hits.append(f"{filename}:{line_number}:{line}")
check("journal cible TECH6C", not scoped_hits, f"occurrences={len(scoped_hits)}")
for hit in scoped_hits[:20]:
    print(hit)

print("USER_RUNTIME_REQUIRED: interface, portes technologiques, IA et mesures economiques")
if failures:
    print(f"FAIL ({len(failures)} controle(s))")
    raise SystemExit(1)
print("PASS_STATIC_STARTUP_LOG")
