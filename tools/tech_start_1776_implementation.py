#!/usr/bin/env python3
"""Apply and validate the final SECOND PASS 1776 technology distribution."""

from __future__ import annotations

import argparse
import csv
import difflib
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VANILLA = Path(r"C:\Games\Victoria 3\game")
COUNTRIES_REL = Path("common/history/countries")
COUNTRY_PLAN = ROOT / "docs/reports/technology/TECH_START_1776_SECOND_PASS_COUNTRY_PLAN.csv"
POST_PLAN = ROOT / "docs/reports/technology/TECH_START_1776_POST_RESOLUTION_IMPLEMENTATION_PLAN.csv"
UNRESOLVED = ROOT / "docs/reports/technology/TECH_START_1776_UNRESOLVED_RESOLUTIONS.csv"
TECH_AUDIT = ROOT / "docs/reports/technology/TECH_START_1776_TECHNOLOGIES.csv"
CLASS_RESOLUTIONS = ROOT / "docs/reports/technology/TECH_START_1776_CLASSIFICATION_RESOLUTIONS.csv"
TECHNOLOGY_DIR = ROOT / "common/technology/technologies"
TIER_FILE = ROOT / "common/scripted_effects/00_starting_inventions.txt"
SANITY_CASES = ROOT / "docs/reports/technology/TECH_START_1776_SANITY_CASES.csv"
DISTRIBUTIONS = ROOT / "docs/reports/technology/TECH_START_1776_FINAL_DISTRIBUTIONS.csv"
SUBSISTENCE_PM_FILE = ROOT / "common/production_methods/99_tech_start_1776_subsistence_tools.txt"
STRUCTURAL_GRANT_REVIEW = ROOT / "docs/reports/technology/TECH_TREE_1776_STRUCTURAL_GRANT_REVIEW.csv"
GLOBAL_NODE_AUDIT = ROOT / "docs/reports/technology/TECH_TREE_1776_GLOBAL_NODE_AUDIT.csv"

STRUCTURAL_TRUNK_COUNTS = {
    "organized_military_establishments": 138,
    "organized_financial_institutions": 34,
}

WAVE2_STRUCTURAL_GRANT_COUNTS = {
    "traditional_food_processing": 39,
    "turnpike_road_networks": 8,
    "permanent_engineer_services": 1,
    "ship_classification_surveying": 1,
}

COMPATIBILITY_ALIASES = {
    "codified_practical_knowledge",
    "traditional_glassmaking",
    "organized_naval_establishments",
}

# These graph debts are intentionally reported instead of being hidden by a broad grant.
# Glass currently creates no debt because every affected start already has organized_workshops.
SENSITIVE_START_DEBT_EDGES = {
    ("applied_mineralogy", "shaft_mining"),
    ("industrial_ceramics", "organized_workshops"),
    ("crystal_glass", "organized_workshops"),
}

RESEARCH_GAPS = {"GAL", "MLT", "PPU"}
FORBIDDEN_START_TECHS = {"railways", "romanticism", "joint_stock_companies"}
TAG_RE = re.compile(r"^\s*c:([A-Z0-9_]{3,})\s*\?=\s*\{", re.MULTILINE)
TIER_RE = re.compile(r"^\s*effect_starting_technology_tier_([1-7])_tech\s*=\s*yes(?:\s*#.*)?\s*$")
TECH_GRANT_RE = re.compile(r"^\s*add_technology_researched\s*=\s*([A-Za-z0-9_-]+)(?:\s*#.*)?\s*$")
EFFECT_RE = re.compile(r"^effect_starting_technology_tier_([1-7])_tech\s*=\s*\{", re.MULTILINE)


def read_text(path: Path) -> tuple[str, bool]:
    raw = path.read_bytes()
    bom = raw.startswith(b"\xef\xbb\xbf")
    if bom:
        raw = raw[3:]
    return raw.decode("utf-8"), bom


def write_text(path: Path, text: str, bom: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = text.encode("utf-8")
    path.write_bytes((b"\xef\xbb\xbf" if bom else b"") + payload)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def split_ids(value: str) -> list[str]:
    return [item.strip() for item in (value or "").split(";") if item.strip()]


def extract_braced_block(text: str, opening_brace: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    in_comment = False
    for index in range(opening_brace, len(text)):
        char = text[index]
        if in_comment:
            if char in "\r\n":
                in_comment = False
            continue
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == "#":
            in_comment = True
        elif char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[opening_brace + 1:index]
    raise ValueError("Bloc non fermé")


def named_block(path: Path, object_id: str) -> str:
    text, _ = read_text(path)
    match = re.search(rf"(?m)^{re.escape(object_id)}\s*=\s*\{{", text)
    if not match:
        raise ValueError(f"{object_id} absent de {path.relative_to(ROOT)}")
    return extract_braced_block(text, text.find("{", match.start()))


def listed_technologies(block: str) -> set[str]:
    match = re.search(r"\bunlocking_technologies\s*=\s*\{", block)
    if not match:
        return set()
    body = extract_braced_block(block, block.find("{", match.start()))
    body = re.sub(r"#.*", "", body)
    return set(re.findall(r"[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*", body))


def listed_treaty_unlock_technologies(block: str) -> set[str]:
    match = re.search(r"\bunlocked_by_technologies\s*=\s*\{", block)
    if not match:
        return set()
    body = extract_braced_block(block, block.find("{", match.start()))
    body = re.sub(r"#.*", "", body)
    return set(re.findall(r"[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*", body))


def parse_graph_and_classifications() -> tuple[dict[str, set[str]], dict[str, str]]:
    classifications = {
        row["Technology ID"].strip(): row["Classification"].strip()
        for row in read_csv(TECH_AUDIT)
    }
    for row in read_csv(CLASS_RESOLUTIONS):
        match = re.match(r"[ABCD]", row["Final_Classification"].strip())
        if match:
            classifications[row["Technology_ID"].strip()] = match.group(0)
    classifications.pop("traditional_furniture_making", None)
    classifications["organized_workshops"] = "A"

    graph: dict[str, set[str]] = {}
    tech_re = re.compile(r"^([A-Za-z0-9_-]+)\s*=\s*\{", re.MULTILINE)
    for path in sorted(TECHNOLOGY_DIR.glob("*.txt")):
        text, _ = read_text(path)
        for match in tech_re.finditer(text):
            tech = match.group(1)
            block = extract_braced_block(text, text.find("{", match.start()))
            graph[tech] = listed_technologies(block)
    return graph, classifications


def parse_tiers() -> dict[int, set[str]]:
    text, _ = read_text(TIER_FILE)
    tiers: dict[int, set[str]] = {}
    for match in EFFECT_RE.finditer(text):
        tier = int(match.group(1))
        body = extract_braced_block(text, text.find("{", match.start()))
        tiers[tier] = set(re.findall(
            r"^\s*add_technology_researched\s*=\s*([A-Za-z0-9_-]+)", body, re.MULTILINE
        ))
    if set(tiers) != set(range(1, 8)):
        raise ValueError(f"Paliers incomplets: {sorted(tiers)}")
    return tiers


def country_overlay() -> tuple[dict[str, tuple[Path, bool]], dict[str, list[str]]]:
    by_name: dict[str, tuple[Path, bool]] = {}
    for base, is_mod in ((VANILLA, False), (ROOT, True)):
        for path in sorted((base / COUNTRIES_REL).glob("*.txt")):
            by_name[path.name.lower()] = (path, is_mod)
    names_by_tag: dict[str, list[str]] = defaultdict(list)
    for name, (path, _) in by_name.items():
        text, _ = read_text(path)
        tags = TAG_RE.findall(text)
        if not tags:
            raise ValueError(f"{path}: aucune définition de pays")
        # Generated additive overlays can legitimately contain several
        # country scopes in one file.  Keep the shared path indexed for every
        # contained tag; parse_country_tech isolates the matching scope.
        for tag in tags:
            names_by_tag[tag].append(name)
    return by_name, names_by_tag


def parse_country_tech(
    path: Path,
    tiers: dict[int, set[str]],
    tag: str | None = None,
) -> tuple[set[str], list[int], list[str]]:
    text, _ = read_text(path)
    if tag is not None:
        matches = [match for match in TAG_RE.finditer(text) if match.group(1) == tag]
        if len(matches) != 1:
            raise ValueError(f"{path}: expected one c:{tag} scope, got {len(matches)}")
        opening = text.find("{", matches[0].start(), matches[0].end())
        text = extract_braced_block(text, opening)
    tier_ids: list[int] = []
    explicit: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            continue
        tier_match = TIER_RE.match(line)
        if tier_match:
            tier_ids.append(int(tier_match.group(1)))
        tech_match = TECH_GRANT_RE.match(line)
        if tech_match:
            explicit.append(tech_match.group(1))
    effective = set(explicit)
    for tier in tier_ids:
        effective.update(tiers[tier])
    return effective, tier_ids, explicit


def overlay_state(plan_tags, overlay, names_by_tag, tiers):
    effective_by_tag: dict[str, set[str]] = {}
    tiers_by_tag: dict[str, list[int]] = {}
    explicit_by_tag: dict[str, list[str]] = {}
    duplicates: list[str] = []
    for tag in sorted(plan_tags):
        effective: set[str] = set()
        tier_ids: list[int] = []
        explicit: list[str] = []
        counts: dict[str, int] = defaultdict(int)
        for name in names_by_tag[tag]:
            values, file_tiers, file_explicit = parse_country_tech(overlay[name][0], tiers, tag)
            effective.update(values)
            tier_ids.extend(file_tiers)
            explicit.extend(file_explicit)
            for tech in file_explicit:
                counts[tech] += 1
        effective_by_tag[tag] = effective
        tiers_by_tag[tag] = sorted(tier_ids)
        explicit_by_tag[tag] = sorted(explicit)
        duplicates.extend(f"{tag}:{tech}x{count}" for tech, count in counts.items() if count > 1)
    return effective_by_tag, tiers_by_tag, explicit_by_tag, duplicates


def final_targets(rows, current, graph):
    resolutions = {
        (row["TAG"], row["Technology_ID"]): row["Final_Status"]
        for row in read_csv(UNRESOLVED)
    }
    targets: dict[str, list[str]] = {}
    researched: set[str] = set()
    for row in rows:
        tag = row["TAG"]
        if row["Research_Status"] == "RESEARCH_GAP":
            targets[tag] = sorted(current[tag])
            continue
        researched.add(tag)
        ordered: list[str] = []
        for tech in split_ids(row["Historical_Target_Technologies"]):
            if tech == "traditional_furniture_making":
                tech = "organized_workshops"
            if tech != "urbanization" and tech not in COMPATIBILITY_ALIASES and tech not in ordered:
                ordered.append(tech)
        for (decision_tag, tech), status in resolutions.items():
            if decision_tag != tag:
                continue
            if status == "PRESENT" and tech not in ordered:
                ordered.append(tech)
            elif status == "ABSENT" and tech in ordered:
                ordered.remove(tech)
        targets[tag] = ordered

    grants = all_structural_grants()
    for tag, technologies in grants.items():
        if tag not in targets:
            raise ValueError(f"Grant de tronc attribué à un TAG absent du plan: {tag}")
        for tech in technologies:
            if tech not in targets[tag]:
                targets[tag].append(tech)

    # Close the real graph for migrations caused by this pass.  No prerequisite is
    # invented here: every addition is read from unlocking_technologies.  The few
    # explicitly sensitive edges remain visible as reportable debt.
    for tag, technologies in targets.items():
        changed = True
        while changed:
            changed = False
            for tech in list(technologies):
                for parent in sorted(graph.get(tech, set())):
                    if parent in COMPATIBILITY_ALIASES:
                        continue
                    if (tech, parent) in SENSITIVE_START_DEBT_EDGES:
                        continue
                    if parent not in technologies:
                        technologies.append(parent)
                        changed = True
    return targets, researched


def structural_trunk_grants() -> dict[str, list[str]]:
    rows = read_csv(STRUCTURAL_GRANT_REVIEW)
    grants: dict[str, list[str]] = defaultdict(list)
    counts: dict[str, int] = defaultdict(int)
    seen: set[tuple[str, str]] = set()
    for row in rows:
        tech = row["Technology"]
        if tech not in STRUCTURAL_TRUNK_COUNTS:
            continue
        key = (row["TAG"], tech)
        if key in seen:
            raise ValueError(f"Grant structurel dupliqué dans le CSV canonique: {key}")
        if row["Decision_Type"] != "GAMEPLAY_ABSTRACTION":
            raise ValueError(f"Type de grant inattendu pour {key}: {row['Decision_Type']}")
        if row["Final_Decision"] != "REDEFINE_PARENT":
            raise ValueError(f"Décision finale inattendue pour {key}: {row['Final_Decision']}")
        seen.add(key)
        grants[row["TAG"]].append(tech)
        counts[tech] += 1
    if dict(counts) != STRUCTURAL_TRUNK_COUNTS:
        raise ValueError(f"Comptes de grants structurels inattendus: {dict(counts)}")
    if len(seen) != sum(STRUCTURAL_TRUNK_COUNTS.values()):
        raise ValueError(f"Total de grants structurels inattendu: {len(seen)}")
    return {tag: values for tag, values in sorted(grants.items())}


def wave2_structural_grants() -> dict[str, list[str]]:
    rows = read_csv(STRUCTURAL_GRANT_REVIEW)
    grants: dict[str, list[str]] = defaultdict(list)
    counts: dict[str, int] = defaultdict(int)
    seen: set[tuple[str, str]] = set()
    expected_decisions = {
        "traditional_food_processing": "ACCEPT",
        "turnpike_road_networks": "REDEFINE_PARENT",
        "permanent_engineer_services": "ACCEPT",
        "ship_classification_surveying": "ACCEPT",
    }
    for row in rows:
        tech = row["Technology"]
        if tech not in WAVE2_STRUCTURAL_GRANT_COUNTS:
            continue
        key = (row["TAG"], tech)
        if key in seen:
            raise ValueError(f"Grant Wave 2 dupliqué dans le CSV canonique: {key}")
        if row["Decision_Type"] != "STRUCTURAL_REQUIRED":
            raise ValueError(f"Type de grant Wave 2 inattendu pour {key}: {row['Decision_Type']}")
        if row["Final_Decision"] != expected_decisions[tech]:
            raise ValueError(f"Décision Wave 2 inattendue pour {key}: {row['Final_Decision']}")
        seen.add(key)
        grants[row["TAG"]].append(tech)
        counts[tech] += 1
    if dict(counts) != WAVE2_STRUCTURAL_GRANT_COUNTS:
        raise ValueError(f"Comptes de grants Wave 2 inattendus: {dict(counts)}")
    if len(seen) != sum(WAVE2_STRUCTURAL_GRANT_COUNTS.values()):
        raise ValueError(f"Total de grants Wave 2 inattendu: {len(seen)}")
    return {tag: values for tag, values in sorted(grants.items())}


def all_structural_grants() -> dict[str, list[str]]:
    grants: dict[str, list[str]] = defaultdict(list)
    for source in (structural_trunk_grants(), wave2_structural_grants()):
        for tag, technologies in source.items():
            for tech in technologies:
                if tech not in grants[tag]:
                    grants[tag].append(tech)
    return {tag: values for tag, values in sorted(grants.items())}


def canonical_name(tag, names, overlay):
    special = {"BHV": "bhv - bhavnagar.txt", "ORG": "org - oregon.txt"}
    if tag in special and special[tag] in names:
        return special[tag]
    mod_names = sorted(name for name in names if overlay[name][1])
    return mod_names[0] if mod_names else sorted(names)[0]


def rewrite_country(text: str, tag: str, remove_tiers: bool, explicit: list[str]) -> str:
    lines = text.splitlines(keepends=True)
    newline = "\r\n" if "\r\n" in text else "\n"
    kept: list[str] = []
    for line in lines:
        bare = line.rstrip("\r\n")
        if TECH_GRANT_RE.match(bare) or (remove_tiers and TIER_RE.match(bare)):
            continue
        kept.append(line)
    opening = next((i for i, line in enumerate(kept) if re.match(
        rf"^\s*c:{re.escape(tag)}\s*\?=\s*\{{", line
    )), None)
    if opening is None:
        raise ValueError(f"Définition c:{tag} introuvable")
    insertion = opening + 1
    if not remove_tiers:
        positions = [i for i, line in enumerate(kept) if TIER_RE.match(line.rstrip("\r\n"))]
        if positions:
            insertion = max(positions) + 1
    additions = [f"\t\tadd_technology_researched = {tech}{newline}" for tech in explicit]
    if additions:
        additions.append(newline)
        kept[insertion:insertion] = additions
    return "".join(kept)


def transitive_closure(tech: str, graph: dict[str, set[str]]) -> set[str]:
    result: set[str] = set()
    pending = list(graph.get(tech, set()))
    while pending:
        parent = pending.pop()
        if parent in result:
            continue
        result.add(parent)
        pending.extend(graph.get(parent, set()))
    return result


def graph_cycles(graph: dict[str, set[str]]) -> list[str]:
    cycles: set[str] = set()
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(node: str, path: list[str]) -> None:
        if node in visiting:
            cycles.add("->".join(path[path.index(node):] + [node]))
            return
        if node in visited:
            return
        visiting.add(node)
        path.append(node)
        for parent in graph.get(node, set()):
            if parent in graph:
                visit(parent, path)
        path.pop()
        visiting.remove(node)
        visited.add(node)

    for tech in graph:
        visit(tech, [])
    return sorted(cycles)


def brace_balance(text: str) -> int:
    depth = 0
    in_string = False
    escaped = False
    in_comment = False
    for char in text:
        if in_comment:
            if char in "\r\n":
                in_comment = False
            continue
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == "#":
            in_comment = True
        elif char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
    return depth


def structural_errors(graph: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    industry = ROOT / "common/buildings/01_industry.txt"
    expected_building_gates = {
        "building_furniture_manufactory": {"organized_workshops"},
        "building_tooling_workshop": {"organized_workshops"},
        "building_glassworks": {"organized_workshops"},
        "building_steel_mill": {"coke_smelting"},
        # Tech & Res-style consolidation: the canonical chemical complex is
        # available with industrial acids; fertilizer progression is handled
        # by its PMs and the artificial-fertilizers throughput effect.
        "building_chemical_plant": {"industrial_acids"},
        "building_explosives_factory": {"nitroglycerin"},
    }
    for building, expected in expected_building_gates.items():
        actual = listed_technologies(named_block(industry, building))
        if actual != expected:
            errors.append(f"{building}: gates {sorted(actual)} != {sorted(expected)}")
    urban = ROOT / "common/buildings/06_urban_center.txt"
    construction = ROOT / "common/buildings/13_construction.txt"
    if listed_technologies(named_block(urban, "building_urban_center")):
        errors.append("building_urban_center conserve un gate")
    if listed_technologies(named_block(construction, "building_construction_sector")) != {
        "organized_financial_institutions"
    }:
        errors.append("building_construction_sector: gate organized_financial_institutions absent")
    if (ROOT / "common/buildings/12_tech6c3a_chemical_works.txt").exists():
        errors.append("obsolete separate building_chemical_works definition still present")
    suez_canal = ROOT / "common/buildings/10_canals.txt"
    if listed_technologies(named_block(suez_canal, "building_suez_canal")) != {"quinine"}:
        errors.append("building_suez_canal gate incorrect")
    if listed_technologies(named_block(suez_canal, "building_panama_canal")) != {"civilizing_mission"}:
        errors.append("building_panama_canal gate incorrect")
    if listed_technologies(named_block(suez_canal, "building_kiel_canal")) != {"ironclad_tech"}:
        errors.append("building_kiel_canal gate incorrect")

    military_buildings = ROOT / "common/buildings/05_military.txt"
    if listed_technologies(named_block(military_buildings, "building_barrack")) != {"organized_military_establishments"}:
        errors.append("building_barrack gate incorrect")

    mines = ROOT / "common/buildings/03_mines.txt"
    if listed_technologies(named_block(mines, "building_gold_mine")) != {"applied_mineralogy"}:
        errors.append("building_gold_mine gate incorrect")

    mine_pms = ROOT / "common/production_methods/03_mines.txt"
    expected_gold_pumps = {
        "pm_atmospheric_engine_pump_building_gold_mine": {"atmospheric_engine"},
        "pm_condensing_engine_pump_building_gold_mine": {"condensing_steam_engines"},
        "pm_diesel_pump_building_gold_mine": {"compression_ignition"},
    }
    for pm, expected in expected_gold_pumps.items():
        if listed_technologies(named_block(mine_pms, pm)) != expected:
            errors.append(f"{pm}: gates incorrects")

    phosphate_pms = ROOT / "common/production_methods/16_tech6r1_mine_processing.txt"
    expected_phosphate_pumps = {
        "pm_atmospheric_engine_pump_building_phosphate_mine": {"atmospheric_engine"},
        "pm_condensing_engine_pump_building_phosphate_mine": {"condensing_steam_engines"},
    }
    for pm, expected in expected_phosphate_pumps.items():
        if listed_technologies(named_block(phosphate_pms, pm)) != expected:
            errors.append(f"{pm}: gates incorrects")

    trade_laws = ROOT / "common/laws/01_trade_policy.txt"
    if listed_technologies(named_block(trade_laws, "law_mercantilism")) != {
        "commercial_insurance_markets", "international_relations"
    }:
        errors.append("law_mercantilism: gates incorrects")
    if listed_technologies(named_block(ROOT / "common/production_methods/02_agro.txt", "pm_sugar_beets")) != {"improved_fertilizer"}:
        errors.append("pm_sugar_beets gate incorrect")
    late_sugar = {
        "vacuum_pan_sugar": {"high_pressure_steam", "sugar_refining"},
        "steam_powered_evaporation_sugar": {"watertube_boiler", "sugar_refining"},
        "centrifugal_machine_sugar": {"rotary_valve_engine", "sugar_refining"},
    }
    plantations = ROOT / "common/production_methods/04_plantations.txt"
    for pm, expected in late_sugar.items():
        if listed_technologies(named_block(plantations, pm)) != expected:
            errors.append(f"{pm}: multi-gate incorrect")
    if graph.get("organized_workshops"):
        errors.append("organized_workshops conserve un parent")
    if graph.get("precision_boring", set()) != {"coke_smelting", "atmospheric_engine", "organized_workshops"}:
        errors.append("precision_boring: parents incorrects")
    if "traditional_furniture_making" in graph:
        errors.append("traditional_furniture_making encore définie")

    logging_pms = ROOT / "common/production_methods/09_misc_resource.txt"
    expected_wood_outputs = {
        "pm_organized_forestry": 40,
        "pm_saw_mills": 80,
        "pm_electric_saw_mills": 160,
    }
    for pm, expected in expected_wood_outputs.items():
        block = named_block(logging_pms, pm)
        if not re.search(rf"(?m)^\s*goods_output_wood_add\s*=\s*{expected}\s*(?:#.*)?$", block):
            errors.append(f"{pm}: production de bois attendue {expected}")

    always_available_treaty_articles = {
        "06_transfer_state.txt": "state_transfer",
        "09_join_power_bloc.txt": "join_power_bloc",
        "11_offer_embassy.txt": "offer_embassy",
        "27_amend_succession.txt": "amend_succession",
        "28_free_text.txt": "free_text",
        "29_recognize_independence.txt": "recognize_independence",
        "30_transfer_subject.txt": "transfer_subject",
        "31_ship_transfer.txt": "ship_transfer",
    }
    for filename, article in always_available_treaty_articles.items():
        path = ROOT / "common/treaty_articles" / filename
        if listed_treaty_unlock_technologies(named_block(path, article)) != {"international_relations"}:
            errors.append(f"{article}: gate international_relations absent")

    specialized_treaty_articles = {
        "04_take_on_debt.txt": "take_on_debt",
        "05_transfer_money.txt": "money_transfer",
        "07_foreign_investment_rights.txt": "foreign_investment_rights",
        "12_military_assistance.txt": "military_assistance",
        "13_goods_transfer.txt": "goods_transfer",
        "17_prohibit_trade_with_global_market.txt": "prohibit_trade_with_global_market",
        "18_acquire_monopoly_for_company.txt": "acquire_monopoly_for_company",
        "21_no_tariffs.txt": "no_tariffs",
        "26_no_subventions.txt": "no_subventions",
    }
    for filename, article in specialized_treaty_articles.items():
        article_block = named_block(ROOT / "common/treaty_articles" / filename, article)
        possible_match = re.search(r"(?m)^\s*possible\s*=\s*\{", article_block)
        if not possible_match:
            errors.append(f"{article}: bloc possible absent")
            continue
        possible = extract_braced_block(article_block, article_block.find("{", possible_match.start()))
        if not re.search(r"(?m)^\s*has_technology_researched\s*=\s*international_relations\s*$", possible):
            errors.append(f"{article}: contrôle international_relations initiateur absent")
        if not re.search(
            r"scope:other_country\s*=\s*\{\s*has_technology_researched\s*=\s*international_relations\s*\}",
            possible,
        ):
            errors.append(f"{article}: contrôle international_relations partenaire absent")

    compatibility = ROOT / "common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt"
    urbanization = named_block(compatibility, "urbanization")
    active_urban = re.sub(r"(?m)#.*$", "", urbanization)
    if "can_research = no" not in active_urban:
        errors.append("urbanization n'est pas can_research=no")
    if re.search(r"(?m)^\s*modifier\s*=", active_urban):
        errors.append("urbanization conserve un modifier")
    if listed_technologies(urbanization):
        errors.append("urbanization conserve un parent")
    children = sorted(tech for tech, parents in graph.items() if "urbanization" in parents)
    if children:
        errors.append(f"urbanization conserve des enfants: {','.join(children)}")
    country_grants = 0
    for path in (ROOT / COUNTRIES_REL).glob("*.txt"):
        text, _ = read_text(path)
        country_grants += len(re.findall(r"(?m)^\s*add_technology_researched\s*=\s*urbanization\b", text))
    tier_text, _ = read_text(TIER_FILE)
    tier_grants = len(re.findall(r"(?m)^\s*add_technology_researched\s*=\s*urbanization\b", tier_text))
    if country_grants:
        errors.append(f"urbanization: {country_grants} grants pays")
    if tier_grants:
        errors.append(f"urbanization: {tier_grants} grants tiers")

    for folder, suffix in ((ROOT / "common", "*.txt"), (ROOT / "events", "*.txt"), (ROOT / "localization", "*.yml")):
        for path in folder.rglob(suffix):
            text, _ = read_text(path)
            if re.search(r"\btraditional_furniture_making\b", text):
                errors.append(f"référence résiduelle traditional_furniture_making: {path.relative_to(ROOT)}")

    # Compatibility aliases may remain defined and localized, but nowhere else
    # may they influence starts, scripts, triggers, unlocks, events or AI.
    for folder in (ROOT / "common", ROOT / "events"):
        for path in folder.rglob("*.txt"):
            relative = path.relative_to(ROOT).as_posix()
            if relative.startswith("common/technology/technologies/"):
                continue
            text, _ = read_text(path)
            active_text = re.sub(r"(?m)#.*$", "", text)
            for alias in COMPATIBILITY_ALIASES:
                if re.search(rf"\b{re.escape(alias)}\b", active_text):
                    errors.append(f"référence active alias {alias}: {relative}")
    for locale in ("english", "french"):
        text, _ = read_text(ROOT / f"localization/{locale}/tech3a_technology_l_{locale}.yml")
        for key in ("organized_workshops", "organized_workshops_desc"):
            count = len(re.findall(rf"(?m)^\s*{key}:\d*\s+", text))
            if count != 1:
                errors.append(f"localisation {locale} {key}: {count} occurrence(s)")
    trigger_re = re.compile(r"(?m)^\s*(?:has_technology|technology)\s*=\s*urbanization\b")
    for folder in (ROOT / "common", ROOT / "events"):
        for path in folder.rglob("*.txt"):
            text, _ = read_text(path)
            if trigger_re.search(re.sub(r"(?m)#.*$", "", text)):
                errors.append(f"trigger urbanization résiduel: {path.relative_to(ROOT)}")
    return errors


def validate_subsistence_pm() -> list[str]:
    expected = {
        "pm_home_workshops_building_subsistence_farm": "0.10",
        "pm_home_workshops_building_subsistence_orchard": "0.10",
        "pm_home_workshops_building_subsistence_pasture": "0.10",
        "pm_home_workshops_building_subsistence_fishing_village": "0.10",
        "pm_home_workshops_building_subsistence_rice_farm": "0.20",
    }
    errors: list[str] = []
    if not SUBSISTENCE_PM_FILE.exists():
        return ["fichier PM de subsistance absent"]
    for pm, value in expected.items():
        try:
            block = named_block(SUBSISTENCE_PM_FILE, pm)
        except ValueError:
            errors.append(f"{pm} absent")
            continue
        if not re.search(rf"(?m)^\s*goods_output_tools_add\s*=\s*{re.escape(value)}\s*$", block):
            errors.append(f"{pm}: sortie outils {value} absente")
    return errors


def validate_structural_trunks(
    graph: dict[str, set[str]], final: dict[str, set[str]],
) -> list[str]:
    errors: list[str] = []
    expected_children = {
        "organized_military_establishments": {
            "scientific_fortification_siegecraft", "regulated_small_arms",
            "light_infantry_tactics", "standardized_field_artillery",
            "permanent_engineer_services", "permanent_military_hospitals",
        },
        "organized_financial_institutions": {
            "institutionalized_public_credit", "commercial_insurance_markets", "stock_exchange",
        },
    }
    expected_categories = {
        "organized_military_establishments": "military",
        "organized_financial_institutions": "society",
    }
    children: dict[str, set[str]] = defaultdict(set)
    for child, parents in graph.items():
        for parent in parents:
            children[parent].add(child)

    definition_blocks: dict[str, list[str]] = defaultdict(list)
    for path in TECHNOLOGY_DIR.glob("*.txt"):
        text, _ = read_text(path)
        for tech in STRUCTURAL_TRUNK_COUNTS:
            match = re.search(rf"(?m)^{re.escape(tech)}\s*=\s*\{{", text)
            if match:
                definition_blocks[tech].append(extract_braced_block(text, text.find("{", match.start())))

    for tech, expected_count in STRUCTURAL_TRUNK_COUNTS.items():
        blocks = definition_blocks.get(tech, [])
        if len(blocks) != 1:
            errors.append(f"{tech}: {len(blocks)} définition(s), 1 attendue")
            continue
        block = blocks[0]
        if graph.get(tech, set()):
            errors.append(f"{tech}: le tronc conserve un parent")
        if children.get(tech, set()) != expected_children[tech]:
            errors.append(
                f"{tech}: enfants {sorted(children.get(tech, set()))} != {sorted(expected_children[tech])}"
            )
        if not re.search(r"(?m)^\s*era\s*=\s*era_1\s*$", block):
            errors.append(f"{tech}: era_1 absente")
        if not re.search(rf"(?m)^\s*category\s*=\s*{expected_categories[tech]}\s*$", block):
            errors.append(f"{tech}: catégorie incorrecte")
        if not re.search(r'(?m)^\s*texture\s*=\s*"gfx/error_deer\.dds"\s*$', block):
            errors.append(f"{tech}: texture error_deer absente")
        if re.search(r"(?m)^\s*(?:modifier|unlocking_technologies)\s*=", block):
            errors.append(f"{tech}: le tronc n'est pas structurellement pur")

        expected_tags = {tag for tag, values in structural_trunk_grants().items() if tech in values}
        actual_tags = {tag for tag, values in final.items() if tech in values}
        if actual_tags != expected_tags or len(actual_tags) != expected_count:
            errors.append(
                f"{tech}: grants effectifs {len(actual_tags)} != {expected_count}; "
                f"manquants={sorted(expected_tags - actual_tags)}; extras={sorted(actual_tags - expected_tags)}"
            )

    # A pure trunk may only appear in technology dependencies and country history.
    for path in (ROOT / "common").rglob("*.txt"):
        relative = path.relative_to(ROOT).as_posix()
        if relative.startswith("common/technology/") or relative.startswith("common/history/countries/"):
            continue
        text, _ = read_text(path)
        for tech in STRUCTURAL_TRUNK_COUNTS:
            if (
                (tech == "organized_military_establishments" and relative == "common/buildings/05_military.txt")
                or (
                    tech == "organized_financial_institutions"
                    and relative == "common/buildings/13_construction.txt"
                )
            ):
                # Targeted runtime corrections: these foundation technologies
                # deliberately unlock their associated foundational building.
                continue
            if re.search(
                rf"unlocking_technologies\s*=\s*\{{[^}}]*\b{re.escape(tech)}\b",
                text,
                re.DOTALL,
            ):
                errors.append(f"{tech}: déblocage gameplay direct dans {relative}")

    for locale in ("english", "french"):
        path = ROOT / f"localization/{locale}/tech_tree_wave1_structural_trunks_l_{locale}.yml"
        if not path.exists():
            errors.append(f"localisation Wave 1 absente: {locale}")
            continue
        text, _ = read_text(path)
        for tech in STRUCTURAL_TRUNK_COUNTS:
            for key in (tech, f"{tech}_desc"):
                count = len(re.findall(rf"(?m)^\s*{re.escape(key)}:\d+\s+", text))
                if count != 1:
                    errors.append(f"localisation {locale} {key}: {count} occurrence(s)")
    return errors


def validate_wave2_graph(graph: dict[str, set[str]]) -> list[str]:
    expected = {
        "coke_smelting": {"organized_workshops", "shaft_mining"},
        "crystal_glass": {"industrial_ceramics", "organized_workshops"},
        "deep_mine_engineering": {"applied_mineralogy", "atmospheric_engine", "shaft_mining"},
        "distillation": {"traditional_food_processing"},
        "industrial_canals": {"turnpike_road_networks"},
        "industrial_ceramics": {"organized_workshops"},
        "iron_hull_construction": {"diagonal_ship_framing", "mechanized_naval_dockyards", "paddle_steamer"},
        "marine_chronometry": {"ship_classification_surveying"},
        "medical_degrees": {"institutionalized_scientific_exchange"},
        "military_topographic_surveying": {"permanent_engineer_services"},
        "military_veterinary_services": {"horse_artillery", "veterinary_science"},
        "organized_elementary_schooling": {"periodical_print_networks"},
        "political_economy": {"periodical_print_networks", "systematic_administrative_statistics"},
        "standardized_naval_signals": {"ship_classification_surveying"},
        "sugar_refining": {"traditional_food_processing"},
        "systematic_cadastral_surveying": {"systematic_administrative_statistics"},
        "systematic_legal_codification": {"systematic_administrative_statistics"},
        "variolation_networks": {"institutionalized_scientific_exchange"},
        "applied_mineralogy": {"shaft_mining"},
        "advanced_crop_rotations": {"improved_husbandry", "selective_breeding"},
        "artificial_fertilizers": {"advanced_crop_rotations", "industrial_acids"},
        "improved_fertilizer": {"artificial_fertilizers"},
        "arc_welding": {"electric_arc_process", "pneumatic_tools", "reinforced_concrete"},
        "quinine": {"active_principle_pharmacy", "colonization"},
        "electrical_capacitors": {"advanced_spinning", "electrical_generation", "mechanized_weaving"},
        "casemated_fortifications": {"scientific_fortification_siegecraft"},
        "state_dockyard_systems": set(),
        "enclosed_dock_systems": {"state_dockyard_systems"},
        "scientific_naval_architecture": {"state_dockyard_systems"},
        "ship_classification_surveying": {"state_dockyard_systems"},
    }
    errors: list[str] = []
    for tech, parents in expected.items():
        if graph.get(tech, set()) != parents:
            errors.append(f"{tech}: parents {sorted(graph.get(tech, set()))} != {sorted(parents)}")
    for alias in COMPATIBILITY_ALIASES:
        if graph.get(alias, set()):
            errors.append(f"{alias} conserve un parent")
        children = sorted(tech for tech, parents in graph.items() if alias in parents)
        if children:
            errors.append(f"{alias} conserve des enfants: {','.join(children)}")
    if graph.get("turnpike_road_networks", set()):
        errors.append("turnpike_road_networks conserve un parent")
    return errors


def wave1_topology_metrics(graph: dict[str, set[str]]) -> dict[str, int]:
    inactive: set[str] = set()
    era: dict[str, int] = {}
    for path in TECHNOLOGY_DIR.glob("*.txt"):
        text, _ = read_text(path)
        for match in re.finditer(r"(?m)^([A-Za-z0-9_-]+)\s*=\s*\{", text):
            tech = match.group(1)
            block = extract_braced_block(text, text.find("{", match.start()))
            if re.search(r"(?m)^\s*can_research\s*=\s*no(?:\s*#.*)?$", block):
                inactive.add(tech)
            era_match = re.search(r"(?m)^\s*era\s*=\s*era_(\d+)\s*$", block)
            era[tech] = int(era_match.group(1)) if era_match else 0
    active = set(graph) - inactive
    children: dict[str, set[str]] = defaultdict(set)
    edges: list[tuple[str, str]] = []
    for child in active:
        for parent in graph.get(child, set()) & active:
            children[parent].add(child)
            edges.append((child, parent))
    roots = {tech for tech in active if not (graph.get(tech, set()) & active)}
    isolated = {tech for tech in roots if not children.get(tech)}
    no_effect_nodes = {
        row["Technology_ID"]
        for row in read_csv(GLOBAL_NODE_AUDIT)
        if "LEAF_NO_EFFECT" in row["Problem_Flags"].split(";")
    }
    return {
        "roots": len(roots),
        "isolated": len(isolated),
        "leaf_no_effect": sum(tech in no_effect_nodes and not children.get(tech) for tech in active),
        "edges": len(edges),
        "max_fanout": max((len(children.get(tech, set())) for tech in active), default=0),
        "cycles": len(graph_cycles({tech: graph.get(tech, set()) & active for tech in active})),
        "unknown_parents": sum(parent not in graph for tech in active for parent in graph.get(tech, set())),
        "negative_era_edges": sum(era.get(child, 0) < era.get(parent, 0) for child, parent in edges),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="écrit les setups pays finaux")
    parser.add_argument("--emit-patch", action="store_true", help="émet un patch apply_patch sans écrire")
    parser.add_argument("--patch-limit", type=int, default=0, help="limite le nombre de fichiers du patch émis")
    parser.add_argument("--validate-only", action="store_true", help="valide l'overlay présent")
    parser.add_argument("--write-sanity", action="store_true", help="écrit le relevé des pays de contrôle")
    args = parser.parse_args()
    if sum((args.apply, args.emit_patch, args.validate_only)) > 1:
        parser.error("--apply, --emit-patch et --validate-only sont incompatibles")

    graph, classifications = parse_graph_and_classifications()
    expected_structural_grants = all_structural_grants()
    unknown_prerequisites = sorted({
        f"{tech}->{parent}" for tech, parents in graph.items() for parent in parents
        if parent not in graph
    })
    definition_counts: dict[str, int] = defaultdict(int)
    for path in TECHNOLOGY_DIR.glob("*.txt"):
        text, _ = read_text(path)
        for tech in re.findall(r"(?m)^([A-Za-z0-9_-]+)\s*=\s*\{", text):
            definition_counts[tech] += 1
    duplicate_tech_definitions = sorted(tech for tech, count in definition_counts.items() if count > 1)
    tiers = parse_tiers()
    rows = read_csv(COUNTRY_PLAN)
    plan_tags = {row["TAG"] for row in rows}
    if len(rows) != 474 or len(plan_tags) != 474:
        raise ValueError(f"Plan pays inattendu: {len(rows)} lignes, {len(plan_tags)} TAG")
    gaps = {row["TAG"] for row in rows if row["Research_Status"] == "RESEARCH_GAP"}
    if gaps != RESEARCH_GAPS:
        raise ValueError(f"Liste RESEARCH_GAP inattendue: {sorted(gaps)}")
    post_rows = read_csv(POST_PLAN)
    post_adds = [row for row in post_rows if row["Change_Type"] == "COUNTRY_TECH_ADD"]
    post_removes = [row for row in post_rows if row["Change_Type"] == "COUNTRY_TECH_REMOVE"]
    if len(post_adds) != 1915 or len(post_removes) != 474:
        raise ValueError(f"Plan déterministe inattendu: ADD={len(post_adds)} REMOVE={len(post_removes)}")

    overlay, names_by_tag = country_overlay()
    missing_tags = sorted(tag for tag in plan_tags if tag not in names_by_tag)
    if missing_tags:
        raise ValueError(f"TAG sans fichier effectif: {missing_tags}")
    before, _, _, _ = overlay_state(plan_tags, overlay, names_by_tag, tiers)
    targets, researched = final_targets(rows, before, graph)
    managed_tags = researched | set(expected_structural_grants)
    writes: dict[Path, tuple[str, bool]] = {}
    fallback_tags: list[str] = []
    for tag in sorted(managed_tags):
        target_order = targets[tag]
        target = set(target_order)
        if before[tag] == target:
            continue
        names = names_by_tag[tag]
        canonical = canonical_name(tag, names, overlay)
        active_tiers: list[int] = []
        for name in names:
            _, file_tiers, _ = parse_country_tech(overlay[name][0], tiers, tag)
            active_tiers.extend(file_tiers)
        tier_base: set[str] = set()
        for tier in active_tiers:
            tier_base.update(tiers[tier])
        remove_tiers = not tier_base.issubset(target)
        if remove_tiers and active_tiers:
            fallback_tags.append(tag)
            tier_base.clear()
        explicit = [tech for tech in target_order if tech not in tier_base]
        for name in names:
            source, source_is_mod = overlay[name]
            destination = source if source_is_mod else ROOT / COUNTRIES_REL / source.name
            text, bom = read_text(source)
            rewritten = rewrite_country(text, tag, remove_tiers, explicit if name == canonical else [])
            if rewritten != text or not source_is_mod:
                writes[destination] = (rewritten, bom)
    if args.apply:
        for path, (text, bom) in writes.items():
            write_text(path, text, bom)
    if args.emit_patch:
        print("*** Begin Patch")
        patch_items = sorted(writes.items())
        if args.patch_limit:
            patch_items = patch_items[:args.patch_limit]
        for path, (rewritten, _bom) in patch_items:
            if not path.exists():
                raise ValueError(f"--emit-patch ne gère pas un nouveau fichier: {path.relative_to(ROOT)}")
            original, _ = read_text(path)
            diff = list(difflib.unified_diff(
                original.splitlines(), rewritten.splitlines(),
                fromfile=str(path), tofile=str(path), lineterm="",
            ))
            if len(diff) <= 2:
                continue
            print(f"*** Update File: {path}")
            for line in diff[2:]:
                if line == " COUNTRIES = {":
                    # Country history files carry a UTF-8 BOM; do not use their
                    # first physical line as an apply_patch context anchor.
                    continue
                print("@@" if line.startswith("@@") else line)
        print("*** End Patch")
        return

    actual_validation = args.apply or args.validate_only
    if actual_validation:
        overlay, names_by_tag = country_overlay()
    final, tiers_by_tag, explicit_by_tag, duplicate_explicit = overlay_state(plan_tags, overlay, names_by_tag, tiers)
    if not actual_validation:
        final = {tag: set(targets[tag]) for tag in plan_tags}
        duplicate_explicit = []
    mismatches = sorted(tag for tag in managed_tags if final[tag] != set(targets[tag]))
    gap_changes = sorted(
        tag for tag in RESEARCH_GAPS
        if final[tag] != before[tag] | set(expected_structural_grants.get(tag, []))
    )
    unknown = sorted({tech for tag in managed_tags for tech in final[tag] if tech not in graph})
    missing_direct = sorted({
        f"{tag}:{tech}->{parent}" for tag in managed_tags for tech in final[tag]
        for parent in graph.get(tech, set()) - final[tag]
    })
    missing_transitive = sorted({
        f"{tag}:{tech}->{parent}" for tag in managed_tags for tech in final[tag]
        for parent in transitive_closure(tech, graph) - final[tag]
    })
    acknowledged_missing_direct = sorted({
        item for item in missing_direct
        if tuple(item.split(":", 1)[1].split("->", 1)) in SENSITIVE_START_DEBT_EDGES
    })
    acknowledged_debt_tags = {item.split(":", 1)[0] for item in acknowledged_missing_direct}
    acknowledged_missing_transitive = sorted({
        item for item in missing_transitive
        if item.split(":", 1)[0] in acknowledged_debt_tags and item.endswith("->shaft_mining")
    })
    unapproved_missing_direct = sorted(set(missing_direct) - set(acknowledged_missing_direct))
    unapproved_missing_transitive = sorted(set(missing_transitive) - set(acknowledged_missing_transitive))
    c_or_d = sorted({
        f"{tag}:{tech}" for tag in managed_tags for tech in final[tag]
        if classifications.get(tech) in {"C", "D"}
    })
    forbidden = sorted({
        f"{tag}:{tech}" for tag in managed_tags for tech in final[tag]
        if tech in FORBIDDEN_START_TECHS
    })
    cycles = graph_cycles(graph)
    structural = structural_errors(graph)
    structural.extend(validate_structural_trunks(graph, final))
    structural.extend(validate_wave2_graph(graph))
    subsistence = validate_subsistence_pm()
    # Recompute topology and building/PM causality from the live merged game+mod
    # objects.  Historical CSV flags are intentionally not authoritative here.
    tools_path = str(ROOT / "tools")
    if tools_path not in sys.path:
        sys.path.insert(0, tools_path)
    import tech_tree_1776_topology_audit as topology_audit
    import tech_tree_1776_wave3_polish as wave3_audit

    runtime_technologies = topology_audit.effective_objects("common/technology/technologies")
    runtime_graph = {
        tech: topology_audit.ids_in_field(block, "unlocking_technologies")
        for tech, block in runtime_technologies.items()
    }
    runtime_eras = {
        tech: topology_audit.era_number(topology_audit.scalar(block, "era", "era_0"))
        for tech, block in runtime_technologies.items()
    }
    runtime_active = {
        tech for tech, block in runtime_technologies.items()
        if topology_audit.scalar(block, "can_research", "yes") != "no"
    }
    _, runtime_effect_counts = wave3_audit.collect_unlocks(runtime_technologies)
    runtime_pm_rows, runtime_pm_violations = wave3_audit.pm_causality_rows(
        runtime_graph, runtime_eras
    )
    topology_metrics = topology_audit.graph_metrics(
        runtime_graph, runtime_eras, runtime_active,
        runtime_effect_counts, runtime_pm_violations,
    )
    brace_errors: list[str] = []
    if actual_validation:
        check_paths = set(writes)
        for folder in (TECHNOLOGY_DIR, ROOT / "common/buildings", ROOT / "common/production_methods", ROOT / "common/production_method_groups"):
            check_paths.update(folder.glob("*.txt"))
        check_paths.add(TIER_FILE)
        for path in sorted(check_paths):
            # In --validate-only mode, vanilla-backed country rewrites may be
            # represented by a not-yet-created destination path.  Validate
            # the computed payload instead of attempting to read that path.
            if path in writes and not path.exists():
                text = writes[path][0]
            else:
                text, _ = read_text(path)
            if brace_balance(text) != 0:
                brace_errors.append(str(path.relative_to(ROOT)))

    smoke_ids = [
        "organized_military_establishments", "organized_naval_establishments",
        "organized_financial_institutions",
        "organized_workshops", "traditional_papermaking", "traditional_glassmaking",
        "organized_forestry", "traditional_food_processing", "sugar_refining",
        "industrial_acids", "improved_agricultural_implements", "advanced_crop_rotations",
        "shaft_mining", "applied_mineralogy", "atmospheric_engine", "coke_smelting",
        "industrial_canals", "international_relations", "institutionalized_public_credit", "commercial_insurance_markets",
        "stock_exchange", "political_economy", "medical_degrees", "variolation_networks",
        "organized_elementary_schooling", "regulated_small_arms", "light_infantry_tactics",
        "standardized_field_artillery", "scientific_naval_architecture", "urbanization",
        "railways", "romanticism", "joint_stock_companies",
    ]
    smoke = {tech: sorted(tag for tag in managed_tags if tech in final[tag]) for tech in smoke_ids}
    current_relations = sum(len(before[tag]) for tag in managed_tags)
    final_relations = sum(len(final[tag]) for tag in managed_tags)
    actual_adds = sum(len(final[tag] - before[tag]) for tag in managed_tags)
    actual_removes = sum(len(before[tag] - final[tag]) for tag in managed_tags)
    mode = "APPLY" if args.apply else ("VALIDATE" if args.validate_only else "DRY-RUN")
    print(f"mode={mode}")
    print(f"plan_tags={len(plan_tags)}")
    print(f"managed_match={len(managed_tags) - len(mismatches)}/{len(managed_tags)}")
    print(f"research_gaps={';'.join(sorted(RESEARCH_GAPS))}")
    print(f"files_to_write={len(writes)}")
    print(f"tier_fallback_tags={len(fallback_tags)}:{','.join(fallback_tags)}")
    print(f"current_researched_relations={current_relations}")
    print(f"final_researched_relations={final_relations}")
    print(f"actual_adds={actual_adds}")
    print(f"actual_removes={actual_removes}")
    print(f"post_plan_add_rows={len(post_adds)}")
    print(f"post_plan_remove_rows={len(post_removes)}")
    print(f"mismatches={len(mismatches)}:{','.join(mismatches[:20])}")
    print(f"research_gap_changes={len(gap_changes)}:{','.join(gap_changes)}")
    print(f"duplicate_explicit={len(duplicate_explicit)}:{','.join(duplicate_explicit[:20])}")
    print(f"unknown_technologies={len(unknown)}:{','.join(unknown)}")
    print(f"unknown_prerequisites={len(unknown_prerequisites)}:{','.join(unknown_prerequisites[:20])}")
    print(f"duplicate_technology_definitions={len(duplicate_tech_definitions)}:{','.join(duplicate_tech_definitions[:20])}")
    print(f"brace_errors={len(brace_errors)}:{','.join(brace_errors[:20])}")
    print(f"graph_cycles={len(cycles)}:{','.join(cycles[:10])}")
    print(f"missing_direct_prerequisite={len(missing_direct)}:{','.join(missing_direct[:20])}")
    print(f"missing_transitive_prerequisite={len(missing_transitive)}:{','.join(missing_transitive[:20])}")
    print(f"acknowledged_missing_direct={len(acknowledged_missing_direct)}:{','.join(acknowledged_missing_direct[:20])}")
    print(f"acknowledged_missing_transitive={len(acknowledged_missing_transitive)}:{','.join(acknowledged_missing_transitive[:20])}")
    print(f"class_c_or_d={len(c_or_d)}:{','.join(c_or_d[:20])}")
    print(f"forbidden_start_techs={len(forbidden)}:{','.join(forbidden[:20])}")
    print(f"structural_errors={len(structural)}:{','.join(structural)}")
    print(f"subsistence_pm_errors={len(subsistence)}:{','.join(subsistence)}")
    print(f"structural_grants_cumulative_expected={sum(len(values) for values in expected_structural_grants.values())}")
    print(f"wave1_expected_grants={sum(STRUCTURAL_TRUNK_COUNTS.values())}")
    for tech, expected in STRUCTURAL_TRUNK_COUNTS.items():
        actual = sum(tech in final[tag] for tag in final)
        print(f"wave1_grants_{tech}={actual}/{expected}")
    print(f"wave2_expected_grants={sum(WAVE2_STRUCTURAL_GRANT_COUNTS.values())}")
    for tech, expected in WAVE2_STRUCTURAL_GRANT_COUNTS.items():
        reviewed_tags = {tag for tag, values in wave2_structural_grants().items() if tech in values}
        actual = sum(tech in final[tag] for tag in reviewed_tags)
        print(f"wave2_grants_{tech}={actual}/{expected}")
    print(f"runtime_nodes={topology_metrics['nodes']}")
    print(f"wave1_roots={topology_metrics['roots']}")
    print(f"wave1_isolated_nodes={topology_metrics['isolated_nodes']}")
    print(f"wave1_leaf_no_effect={topology_metrics['leaf_no_effect']}")
    print(f"wave1_edges={topology_metrics['edges_total']}")
    print(f"wave1_max_fanout={topology_metrics['max_child_count']}")
    print(f"wave1_cycles={topology_metrics['graph_cycles']}")
    print(f"wave1_unknown_parents={topology_metrics['unknown_parent_ids']}")
    print(f"wave1_negative_era_edges={topology_metrics['negative_era_edges']}")
    print(f"runtime_pm_rows={len(runtime_pm_rows)}")
    print(f"runtime_pm_causality_violations={runtime_pm_violations}")
    for tech in smoke_ids:
        print(f"smoke_{tech}={';'.join(smoke[tech]) or '-'}")

    if args.write_sanity:
        with SANITY_CASES.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=[
                "TAG", "Research_Status", "Effective_Tiers", "Explicit_Technologies", "Final_Technologies"
            ])
            writer.writeheader()
            for tag in "GBR FRA NET BEL BEO HUN TUR VEN GEN JAP CHI MUG PLC MYS".split():
                writer.writerow({
                    "TAG": tag,
                    "Research_Status": "RESEARCHED",
                    "Effective_Tiers": ";".join(f"tier_{tier}" for tier in tiers_by_tag[tag]),
                    "Explicit_Technologies": ";".join(explicit_by_tag[tag]),
                    "Final_Technologies": ";".join(sorted(final[tag])),
                })
        with DISTRIBUTIONS.open("w", encoding="utf-8-sig", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=["Technology_ID", "TAG_Count", "TAGs"])
            writer.writeheader()
            for tech in smoke_ids:
                writer.writerow({
                    "Technology_ID": tech,
                    "TAG_Count": len(smoke[tech]),
                    "TAGs": ";".join(smoke[tech]),
                })
    if actual_validation and (
        mismatches or gap_changes or duplicate_explicit or unknown or unknown_prerequisites or
        duplicate_tech_definitions or brace_errors or cycles or
        unapproved_missing_direct or unapproved_missing_transitive or
        c_or_d or forbidden or structural or subsistence or
        topology_metrics['isolated_nodes'] or topology_metrics['leaf_no_effect'] or
        topology_metrics['graph_cycles'] or topology_metrics['unknown_parent_ids'] or
        topology_metrics['negative_era_edges'] or runtime_pm_violations
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
