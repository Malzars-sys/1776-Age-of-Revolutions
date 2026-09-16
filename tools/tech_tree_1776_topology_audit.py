#!/usr/bin/env python3
"""Generate the TECH TREE 1776 topology/design audit without editing gameplay."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VANILLA = Path(r"C:\Games\Victoria 3\game")
REPORTS = ROOT / "docs/reports/technology"

NODE_AUDIT = REPORTS / "TECH_TREE_1776_GLOBAL_NODE_AUDIT.csv"
PM_AUDIT = REPORTS / "TECH_TREE_1776_BUILDING_PM_CAUSALITY.csv"
ARCHITECTURE = REPORTS / "TECH_TREE_1776_PROPOSED_ARCHITECTURE.csv"
GENERAL_NODES = REPORTS / "TECH_TREE_1776_PROPOSED_GENERAL_NODES.csv"
DISTRIBUTION = REPORTS / "TECH_TREE_1776_ARCHITECTURE_DISTRIBUTION_IMPACT.csv"
METRICS = REPORTS / "TECH_TREE_1776_TOPOLOGY_METRICS.json"

sys.path.insert(0, str(ROOT / "tools"))
import tech_start_1776_implementation as starts  # noqa: E402


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    return raw.decode("utf-8")


def extract_block(text: str, opening: int) -> str:
    depth = 0
    in_string = False
    escaped = False
    in_comment = False
    for index in range(opening, len(text)):
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
                return text[opening + 1:index]
    raise ValueError("Bloc non fermé")


def blocks_in_file(path: Path, prefix: str | None = None, nested: bool = False) -> dict[str, str]:
    text = read_text(path)
    lead = r"^\s*" if nested else r"^"
    pattern = re.compile(lead + r"([A-Za-z0-9_-]+)\s*=\s*\{", re.MULTILINE)
    result: dict[str, str] = {}
    for match in pattern.finditer(text):
        object_id = match.group(1)
        if prefix and not object_id.startswith(prefix):
            continue
        result[object_id] = extract_block(text, text.find("{", match.start()))
    return result


def effective_objects(relative: str, prefix: str | None = None, nested: bool = False) -> dict[str, str]:
    result: dict[str, str] = {}
    for base in (VANILLA, ROOT):
        folder = base / relative
        if not folder.exists():
            continue
        for path in sorted(folder.rglob("*.txt")):
            result.update(blocks_in_file(path, prefix, nested))
    return result


def ids_in_field(block: str, field: str) -> set[str]:
    match = re.search(rf"\b{re.escape(field)}\s*=\s*\{{", block)
    if not match:
        return set()
    body = extract_block(block, block.find("{", match.start()))
    body = re.sub(r"(?m)#.*$", "", body)
    return set(re.findall(r"[A-Za-z][A-Za-z0-9_-]*", body))


def scalar(block: str, field: str, default: str = "") -> str:
    match = re.search(rf"(?m)^\s*{re.escape(field)}\s*=\s*([A-Za-z0-9_.-]+)", block)
    return match.group(1) if match else default


def era_number(value: str) -> int:
    match = re.search(r"(\d+)$", value or "")
    return int(match.group(1)) if match else 0


def closure(node: str, graph: dict[str, set[str]]) -> set[str]:
    found: set[str] = set()
    pending = list(graph.get(node, set()))
    while pending:
        parent = pending.pop()
        if parent in found:
            continue
        found.add(parent)
        pending.extend(graph.get(parent, set()))
    return found


def graph_metrics(
    graph: dict[str, set[str]],
    eras: dict[str, int],
    active: set[str],
    effect_counts: dict[str, int],
    pm_violations: int,
) -> dict[str, float | int]:
    active_graph = {tech: graph.get(tech, set()) & active for tech in active}
    cycles = starts.graph_cycles(active_graph)
    children: dict[str, set[str]] = defaultdict(set)
    for child, parents in graph.items():
        if child not in active:
            continue
        for parent in parents:
            if parent in active:
                children[parent].add(child)
    roots = [tech for tech in active if not (graph.get(tech, set()) & active)]
    isolated = [tech for tech in active if tech in roots and not children.get(tech)]
    leaf_no_effect = [
        tech for tech in active
        if not children.get(tech) and effect_counts.get(tech, 0) == 0
    ]
    edges = [(child, parent) for child in active for parent in graph.get(child, set()) if parent in active]
    gaps = [eras.get(child, 0) - eras.get(parent, 0) for child, parent in edges]
    return {
        "nodes": len(active),
        "roots": len(roots),
        "isolated_nodes": len(isolated),
        "leaf_no_effect": len(leaf_no_effect),
        "average_parent_count": round(len(edges) / len(active), 3) if active else 0,
        "average_child_count": round(len(edges) / len(active), 3) if active else 0,
        "max_child_count": max((len(children.get(tech, set())) for tech in active), default=0),
        "edges_total": len(edges),
        "graph_cycles": len(cycles),
        "unknown_parent_ids": sum(
            parent not in graph for tech in active for parent in graph.get(tech, set())
        ),
        "negative_era_edges": sum(gap < 0 for gap in gaps),
        "same_era_edges": sum(gap == 0 for gap in gaps),
        "cross_era_plus1": sum(gap == 1 for gap in gaps),
        "cross_era_plus2": sum(gap == 2 for gap in gaps),
        "cross_era_plus3": sum(gap == 3 for gap in gaps),
        "cross_era_gt3": sum(gap > 3 for gap in gaps),
        "building_pm_causality_violations": pm_violations,
        "orphan_unlock_chains": pm_violations,
        "root_ids": sorted(roots),
        "isolated_ids": sorted(isolated),
        "leaf_no_effect_ids": sorted(leaf_no_effect),
    }


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    technologies = effective_objects("common/technology/technologies")
    graph = {tech: ids_in_field(block, "unlocking_technologies") for tech, block in technologies.items()}
    categories = {tech: scalar(block, "category", "unknown") for tech, block in technologies.items()}
    era_labels = {tech: scalar(block, "era", "era_0") for tech, block in technologies.items()}
    eras = {tech: era_number(value) for tech, value in era_labels.items()}
    active = {tech for tech, block in technologies.items() if scalar(block, "can_research", "yes") != "no"}

    children: dict[str, set[str]] = defaultdict(set)
    for child, parents in graph.items():
        for parent in parents:
            children[parent].add(child)

    buildings = effective_objects("common/buildings", "building_")
    pmgs = effective_objects("common/production_method_groups", "pmg_")
    pms = effective_objects("common/production_methods", "pm_")
    laws = effective_objects("common/laws", "law_", nested=True)
    other_unlocks: dict[str, list[str]] = defaultdict(list)
    for folder in (
        "combat_unit_types", "decrees", "diplomatic_actions", "mobilization_options",
        "parties", "ship_modifications", "ship_types",
    ):
        for object_id, block in effective_objects(f"common/{folder}").items():
            for tech in ids_in_field(block, "unlocking_technologies"):
                other_unlocks[tech].append(f"{folder}:{object_id}")

    building_unlocks: dict[str, list[str]] = defaultdict(list)
    pm_unlocks: dict[str, list[str]] = defaultdict(list)
    law_unlocks: dict[str, list[str]] = defaultdict(list)
    for object_id, block in buildings.items():
        for tech in ids_in_field(block, "unlocking_technologies"):
            building_unlocks[tech].append(object_id)
    for object_id, block in pms.items():
        for tech in ids_in_field(block, "unlocking_technologies"):
            pm_unlocks[tech].append(object_id)
    for object_id, block in laws.items():
        for tech in ids_in_field(block, "unlocking_technologies"):
            law_unlocks[tech].append(object_id)

    modifier_counts = {
        tech: len(re.findall(r"(?m)^\s*modifier\s*=\s*\{", block))
        for tech, block in technologies.items()
    }
    direct_effect_counts = {
        tech: len(building_unlocks[tech]) + len(pm_unlocks[tech]) + len(law_unlocks[tech])
        + len(other_unlocks[tech]) + modifier_counts[tech]
        for tech in technologies
    }

    tiers = starts.parse_tiers()
    country_rows = starts.read_csv(starts.COUNTRY_PLAN)
    plan_tags = {row["TAG"] for row in country_rows}
    overlay, names_by_tag = starts.country_overlay()
    country_state, _, _, _ = starts.overlay_state(plan_tags, overlay, names_by_tag, tiers)
    start_tags: dict[str, list[str]] = {
        tech: sorted(tag for tag in plan_tags if tech in country_state[tag])
        for tech in technologies
    }

    mandatory = {
        "organized_forestry", "organized_workshops", "traditional_papermaking",
        "traditional_glassmaking", "industrial_ceramics", "sugar_refining",
        "industrial_acids", "shaft_mining", "applied_mineralogy", "coke_smelting",
        "atmospheric_engine", "precision_boring", "advanced_crop_rotations",
        "selective_breeding", "improved_agricultural_implements", "industrial_canals",
        "codified_practical_knowledge", "political_economy",
        "institutionalized_public_credit", "commercial_insurance_markets", "stock_exchange",
        "medical_degrees", "organized_elementary_schooling", "regulated_small_arms",
        "light_infantry_tactics", "standardized_field_artillery",
        "scientific_naval_architecture", "state_dockyard_systems", "enclosed_dock_systems",
    }
    leaf_resolutions = {
        "standardized_military_rockets": "MERGE dans explosive_field_ammunition; conserver l’ID comme alias non recherchable tant qu’aucun contenu fusée n’existe",
        "hydraulic_turbines": "MERGE dans professional_civil_engineering; conserver l’ID comme alias non recherchable jusqu’à un vrai PM hydraulique",
        "modern_lighthouse_optics": "ADD_MODIFIER: building_port_throughput_add = 0.05",
        "optical_telegraph_networks": "ADD_MODIFIER: country_influence_add = 25",
        "systematic_cadastral_surveying": "ADD_MODIFIER: state_tax_capacity_add = 10",
        "veterinary_science": "ADD_EDGE comme parent de military_veterinary_services",
        "codified_practical_knowledge": "KEEP_AS_TRUNK pour éducation, médecine, droit et économie politique",
    }

    node_rows: list[dict[str, object]] = []
    for tech in sorted(technologies, key=lambda item: (categories[item], eras[item], item)):
        parents = graph[tech]
        tech_children = children.get(tech, set())
        unlock_count = (
            len(building_unlocks[tech]) + len(pm_unlocks[tech]) + len(law_unlocks[tech])
            + len(other_unlocks[tech])
        )
        flags: list[str] = []
        researchable = tech in active
        if not researchable:
            flags.append("COMPATIBILITY_ALIAS")
        elif not parents and not tech_children:
            flags.append("ISOLATED")
        if researchable and not parents and (eras[tech] > 1 or tech in mandatory):
            flags.append("ROOT_OVER_SPECIALIZED")
        if researchable and not tech_children and unlock_count == 0 and modifier_counts[tech] == 0:
            flags.append("LEAF_NO_EFFECT")
        if researchable and len(tech_children) == 0 and direct_effect_counts[tech] <= 1:
            flags.append("LOW_VALUE")
        if len(tech_children) >= 8:
            flags.extend(["TOO_MANY_CHILDREN", "VISUAL_SPAGHETTI"])
        bad_gaps = [eras[child] - eras[tech] for child in tech_children]
        parent_gaps = [eras[tech] - eras[parent] for parent in parents if parent in eras]
        if any(gap < 0 or gap > 3 for gap in bad_gaps + parent_gaps):
            flags.append("BAD_ERA_CHAIN")
        if not flags:
            flags.append("OK")

        if not researchable:
            role = "Alias de compatibilité non recherchable"
            recommendation = "KEEP_COMPATIBILITY_ALIAS"
        elif building_unlocks[tech] or pm_unlocks[tech] or law_unlocks[tech] or other_unlocks[tech]:
            kinds = []
            if building_unlocks[tech]:
                kinds.append("bâtiment")
            if pm_unlocks[tech]:
                kinds.append("PM")
            if law_unlocks[tech]:
                kinds.append("loi")
            if other_unlocks[tech]:
                kinds.append("contenu militaire/diplomatique")
            role = "Déblocage " + "/".join(kinds)
            recommendation = "REVIEW_TOPOLOGY" if set(flags) - {"OK", "LOW_VALUE"} else "KEEP"
        elif tech_children:
            role = "Nœud structurel"
            recommendation = "KEEP_AS_TRUNK" if not parents else "KEEP"
        elif modifier_counts[tech]:
            role = "Bonus technologique"
            recommendation = "KEEP"
        else:
            role = "Aucun rôle gameplay direct"
            recommendation = "MERGE_OR_ADD_EFFECT"
        if tech == "organized_forestry":
            recommendation = "ADD_MODIFIER: building_logging_camp_throughput_add = 0.05"
        if tech in leaf_resolutions:
            recommendation = leaf_resolutions[tech]

        node_rows.append({
            "Technology_ID": tech,
            "Category": categories[tech],
            "Era": era_labels[tech],
            "Parent_Count": len(parents),
            "Parents": ";".join(sorted(parents)),
            "Child_Count": len(tech_children),
            "Children": ";".join(sorted(tech_children)),
            "Building_Unlocks": ";".join(sorted(building_unlocks[tech])),
            "PM_Unlocks": ";".join(sorted(pm_unlocks[tech])),
            "Law_Unlocks": ";".join(sorted(law_unlocks[tech])),
            "Modifier_Count": modifier_counts[tech],
            "Start_Country_Count": len(start_tags[tech]),
            "Role": role,
            "Problem_Flags": ";".join(dict.fromkeys(flags)),
            "Recommendation": recommendation,
        })

    pm_rows: list[dict[str, object]] = []
    pm_violation_keys: set[tuple[str, str]] = set()
    for building, building_block in sorted(buildings.items()):
        building_techs = ids_in_field(building_block, "unlocking_technologies")
        building_era = max((eras.get(tech, 0) for tech in building_techs), default=0)
        for pmg in sorted(ids_in_field(building_block, "production_method_groups")):
            if pmg not in pmgs:
                continue
            for pm in sorted(ids_in_field(pmgs[pmg], "production_methods")):
                if pm not in pms:
                    continue
                pm_techs = ids_in_field(pms[pm], "unlocking_technologies")
                pm_era = max((eras.get(tech, 0) for tech in pm_techs), default=0)
                gap: int | str = pm_era - building_era if building_techs and pm_techs else ""
                guarantee_set = set(pm_techs)
                for gate in pm_techs:
                    guarantee_set.update(closure(gate, graph))
                ancestor = bool(building_techs) and building_techs.issubset(guarantee_set)
                per_gate = {
                    gate: building_techs.issubset({gate} | closure(gate, graph))
                    for gate in pm_techs
                }
                other_gate = len(pm_techs) > 1 and ancestor and not all(per_gate.values())
                violation = bool(building_techs and pm_techs and int(gap) <= 2 and not ancestor)
                if violation:
                    pm_violation_keys.add((building, pm))
                    if int(gap) < 0:
                        recommendation = "MOVE_UNLOCK vers une technologie au moins aussi tardive que le bâtiment"
                    else:
                        recommendation = "ADD_ANCESTRY via le tronc du bâtiment ou un parent commun structurant"
                elif building_techs and pm_techs and int(gap) > 2 and not ancestor:
                    recommendation = "EXCEPTION >3 eras: documenter; anticipation et autres gates suffisants"
                elif ancestor:
                    recommendation = "KEEP"
                else:
                    recommendation = "N/A: bâtiment ou PM sans gate technologique"
                pm_rows.append({
                    "Building": building,
                    "Building_Unlock_Tech": ";".join(sorted(building_techs)),
                    "Building_Era": f"era_{building_era}" if building_era else "UNLOCKED",
                    "Production_Method": pm,
                    "PM_Unlock_Techs": ";".join(sorted(pm_techs)),
                    "PM_Min_Era": f"era_{pm_era}" if pm_era else "UNLOCKED",
                    "Era_Gap": gap,
                    "Building_Tech_Is_Ancestor": "YES" if ancestor else "NO",
                    "Guaranteed_By_Other_Gate": "YES" if other_gate else "NO",
                    "Violation": "YES" if violation else "NO",
                    "Recommendation": recommendation,
                })

    # Minimal global redesign: reuse broad existing trunks; introduce only three
    # genuinely cross-branch foundations where no current ID is sufficiently broad.
    added_parents: dict[str, set[str]] = {
        "traditional_papermaking": {"organized_workshops"},
        "traditional_glassmaking": {"organized_workshops"},
        "industrial_ceramics": {"traditional_glassmaking"},
        "sugar_refining": {"traditional_food_processing"},
        "industrial_acids": {"organized_workshops"},
        "applied_mineralogy": {"shaft_mining"},
        "coke_smelting": {"shaft_mining", "organized_workshops"},
        "industrial_canals": {"turnpike_road_networks"},
        "distillation": {"traditional_food_processing"},
        "crystal_glass": {"traditional_glassmaking"},
        "deep_mine_engineering": {"applied_mineralogy"},
        "steam_turbine": {"electrical_generation"},
        "camera": {"romanticism"},
        "military_veterinary_services": {"veterinary_science"},
        "chemical_bleaching": {"industrial_alkalis"},
        "baking_powder": {"industrial_alkalis"},
        "rubber_mastication": {"fractional_distillation"},
        "standardized_naval_signals": {"ship_classification_surveying"},
        "marine_chronometry": {"ship_classification_surveying"},
        "organized_elementary_schooling": {"codified_practical_knowledge"},
        "medical_degrees": {"codified_practical_knowledge"},
        "systematic_cadastral_surveying": {"codified_practical_knowledge"},
        "systematic_legal_codification": {"codified_practical_knowledge"},
        "political_economy": {"codified_practical_knowledge"},
        "stock_exchange": {"organized_financial_institutions"},
        "commercial_insurance_markets": {"organized_financial_institutions"},
        "institutionalized_public_credit": {"organized_financial_institutions"},
        "scientific_fortification_siegecraft": {"organized_military_establishments"},
        "regulated_small_arms": {"organized_military_establishments"},
        "light_infantry_tactics": {"organized_military_establishments"},
        "standardized_field_artillery": {"organized_military_establishments"},
        "permanent_engineer_services": {"organized_military_establishments"},
        "permanent_military_hospitals": {"organized_military_establishments"},
        "military_topographic_surveying": {"permanent_engineer_services"},
        "state_dockyard_systems": {"organized_naval_establishments"},
        "enclosed_dock_systems": {"organized_naval_establishments"},
        "scientific_naval_architecture": {"organized_naval_establishments"},
        "ship_classification_surveying": {"organized_naval_establishments"},
    }
    removed_parents: dict[str, set[str]] = {
        "chemical_bleaching": {"industrial_acids"},
        "baking_powder": {"industrial_acids"},
        "rubber_mastication": {"industrial_acids"},
        "iron_hull_construction": {"scientific_naval_architecture"},
        "standardized_naval_signals": {"scientific_naval_architecture"},
        "marine_chronometry": {"scientific_naval_architecture"},
    }
    new_nodes = {
        "organized_financial_institutions": {
            "category": "society", "era": 1, "parents": set(),
            "concept": "Institutions financières organisées",
            "children": {"stock_exchange", "commercial_insurance_markets", "institutionalized_public_credit"},
            "effect": "Petit bonus natif proposé: country_loan_interest_rate_add = -0.01",
            "abstraction": "Capacité générale de tenue des comptes, crédit et intermédiation; pas une bourse moderne.",
            "why": "Les trois IDs existants sont trop spécialisés pour servir de parent neutre aux deux autres.",
            "risk": "MEDIUM: nouveau grant abstrait nécessaire pour les starts financiers.",
        },
        "organized_military_establishments": {
            "category": "military", "era": 1, "parents": set(),
            "concept": "Établissements militaires organisés",
            "children": {"scientific_fortification_siegecraft", "regulated_small_arms", "light_infantry_tactics", "standardized_field_artillery", "permanent_engineer_services", "permanent_military_hospitals"},
            "effect": "Déplacer ici le déblocage du bâtiment de caserne; pas de bonus numérique nécessaire.",
            "abstraction": "Capacité d’entretenir des forces permanentes et des services spécialisés.",
            "why": "Fortification, armes, tactique et artillerie ne doivent pas être parents les uns des autres.",
            "risk": "MEDIUM: vérifier les pays irréguliers et décentralisés avant les grants.",
        },
        "organized_naval_establishments": {
            "category": "military", "era": 1, "parents": set(),
            "concept": "Établissements navals organisés",
            "children": {"state_dockyard_systems", "enclosed_dock_systems", "scientific_naval_architecture", "ship_classification_surveying"},
            "effect": "Déplacer ici le socle shipyard/naval administration commun; garder les spécialisations séparées.",
            "abstraction": "Administration, savoirs et chantiers capables de soutenir une marine organisée.",
            "why": "Aucun des trois roots navals actuels n’est assez neutre sans accorder son contenu spécialisé.",
            "risk": "LOW-MEDIUM: union de grants navals à contrôler.",
        },
    }

    proposed_graph = {tech: set(parents) for tech, parents in graph.items()}
    proposed_eras = dict(eras)
    proposed_categories = dict(categories)
    proposed_eras["chemical_bleaching"] = 5
    for tech, data in new_nodes.items():
        proposed_graph[tech] = set(data["parents"])
        proposed_eras[tech] = int(data["era"])
        proposed_categories[tech] = str(data["category"])
    for tech, parents in removed_parents.items():
        if tech in proposed_graph:
            proposed_graph[tech].difference_update(parents)
    for tech, parents in added_parents.items():
        if tech in proposed_graph:
            proposed_graph[tech].update(parents)
    proposed_active = active | set(new_nodes)
    merged_aliases = {
        "standardized_military_rockets", "explosive_field_ammunition", "hydraulic_turbines"
    }
    proposed_active.difference_update(merged_aliases)

    building_gate_overrides = {
        "building_artillery_foundry": {"standardized_field_artillery"},
        "building_cotton_plantation": set(),
    }
    pm_gate_additions = {
        ("building_automotive_industry", "pm_aeroplane_production"): {"combustion_engine"},
        ("building_automotive_industry", "pm_all_metal_aircraft"): {"combustion_engine"},
        ("building_automotive_industry", "pm_assembly_lines_building_automotive_industry"): {"combustion_engine"},
        ("building_automotive_industry", "pm_scientific_management"): {"combustion_engine"},
        ("building_electrics_industry", "pm_scientific_management"): {"telephone"},
        ("building_explosives_factory", "pm_brine_electrolysis"): {"nitroglycerin"},
        ("building_glassworks", "pm_bone_china"): {"traditional_glassmaking"},
        ("building_gold_mine", "pm_atmospheric_engine_pump_building_gold_mine"): {"applied_mineralogy"},
        ("building_gold_mine", "pm_condensing_engine_pump_building_gold_mine"): {"applied_mineralogy"},
        ("building_phosphate_mine", "pm_atmospheric_engine_pump_building_phosphate_mine"): {"applied_mineralogy"},
        ("building_phosphate_mine", "pm_condensing_engine_pump_building_phosphate_mine"): {"applied_mineralogy"},
        ("building_oil_rig", "pm_combustion_derricks"): {"pumpjacks"},
        ("building_oil_rig", "pm_rail_transport_building_oil_rig"): {"pumpjacks"},
        ("building_oil_rig", "pm_tanker_cars"): {"pumpjacks"},
        # Requires a building-specific PM variant because the generic rail PM is shared.
        ("building_rubber_plantation", "pm_steam_rail_transport"): {"rubber_mastication"},
    }

    # Simulate country prerequisite closure under the proposal.
    proposed_country = {tag: set(values) for tag, values in country_state.items()}
    distribution_rows: list[dict[str, object]] = []
    changed = True
    while changed:
        changed = False
        for tag, values in proposed_country.items():
            missing: set[str] = set()
            for tech in list(values):
                missing.update(proposed_graph.get(tech, set()) - values)
            for tech in sorted(missing):
                if tech not in proposed_active:
                    continue
                values.add(tech)
                changed = True
                decision = "GAMEPLAY_ABSTRACTION" if tech in new_nodes else "STRUCTURAL_REQUIRED"
                distribution_rows.append({
                    "TAG": tag,
                    "Technology": tech,
                    "Current_Start_Status": "ABSENT",
                    "Proposed_Start_Status": "PRESENT",
                    "Reason": "Fermeture du nouveau tronc requis par une technologie déjà présente au départ.",
                    "Decision_Type": decision,
                })
    # Deduplicate additions reached in multiple closure passes.
    unique_distribution = {
        (row["TAG"], row["Technology"]): row for row in distribution_rows
        if row["Technology"] not in country_state[row["TAG"]]
    }
    distribution_rows = [unique_distribution[key] for key in sorted(unique_distribution)]

    # The proposed trunks resolve topology, while PM causality changes remain a
    # separate implementation wave; simulate only violations removed by new ancestry.
    proposed_pm_violations = 0
    for row in pm_rows:
        building = str(row["Building"])
        pm = str(row["Production_Method"])
        building_techs = building_gate_overrides.get(
            building, set(str(row["Building_Unlock_Tech"]).split(";")) - {""}
        )
        pm_techs = set(str(row["PM_Unlock_Techs"]).split(";")) - {""}
        pm_techs.update(pm_gate_additions.get((building, pm), set()))
        if not building_techs or not pm_techs:
            continue
        building_era = max((proposed_eras.get(tech, 0) for tech in building_techs), default=0)
        pm_era = max((proposed_eras.get(tech, 0) for tech in pm_techs), default=0)
        if pm_era - building_era > 2:
            continue
        guarantee = set(pm_techs)
        for gate in pm_techs:
            guarantee.update(closure(gate, proposed_graph))
        if not building_techs.issubset(guarantee):
            proposed_pm_violations += 1

    current_metrics = graph_metrics(graph, eras, active, direct_effect_counts, len(pm_violation_keys))
    proposed_effects = dict(direct_effect_counts)
    proposed_effects["organized_financial_institutions"] = 1
    proposed_effects["organized_military_establishments"] = 1
    proposed_effects["organized_naval_establishments"] = 1
    proposed_effects["organized_forestry"] = proposed_effects.get("organized_forestry", 0) + 1
    proposed_effects["modern_lighthouse_optics"] = proposed_effects.get("modern_lighthouse_optics", 0) + 1
    proposed_effects["optical_telegraph_networks"] = proposed_effects.get("optical_telegraph_networks", 0) + 1
    proposed_effects["systematic_cadastral_surveying"] = proposed_effects.get("systematic_cadastral_surveying", 0) + 1
    proposed_metrics = graph_metrics(
        proposed_graph, proposed_eras, proposed_active, proposed_effects, proposed_pm_violations
    )
    proposed_metrics["new_general_nodes"] = len(new_nodes)
    proposed_metrics["redefined_nodes"] = 4
    proposed_metrics["merged_nodes"] = len(merged_aliases)
    proposed_metrics["countries_needing_gameplay_abstraction_grants"] = len({
        row["TAG"] for row in distribution_rows if row["Decision_Type"] == "GAMEPLAY_ABSTRACTION"
    })
    proposed_metrics["total_added_structural_grants"] = len(distribution_rows)
    proposed_metrics["total_removed_structural_grants"] = 0

    architecture_rows: list[dict[str, object]] = []
    for tech in sorted(set(technologies) | set(new_nodes)):
        current_parents = graph.get(tech, set())
        proposed_parents = proposed_graph.get(tech, set())
        if tech in new_nodes:
            change_type = "NEW_GENERAL_NODE"
            reason = new_nodes[tech]["why"]
            proposed_role = new_nodes[tech]["concept"]
            compromise = new_nodes[tech]["abstraction"]
            benefit = "Crée un tronc neutre et évite de transformer une spécialité en super-parent."
            risk = new_nodes[tech]["risk"]
        elif tech in merged_aliases:
            change_type = "MERGE"
            target = (
                "standardized_field_artillery"
                if tech in {"standardized_military_rockets", "explosive_field_ammunition"}
                else "professional_civil_engineering"
            )
            reason = f"Le nœud n’a aucun enfant, unlock ou modifier; fusion proposée dans {target}."
            proposed_role = "Alias de compatibilité non recherchable après migration"
            compromise = "Le concept reste localisable et référencable, mais cesse d’occuper un nœud vide."
            benefit = "Supprime une feuille sans effet sans inventer un bonus artificiel."
            risk = "LOW: scanner les références externes avant implémentation."
        elif tech in {
            "organized_forestry", "modern_lighthouse_optics",
            "optical_telegraph_networks", "systematic_cadastral_surveying",
        }:
            change_type = "ADD_MODIFIER"
            modifier_design = {
                "organized_forestry": ("building_logging_camp_throughput_add = 0.05", "Organisation forestière et rendement des camps de bûcherons"),
                "modern_lighthouse_optics": ("building_port_throughput_add = 0.05", "Sécurité et efficacité portuaire"),
                "optical_telegraph_networks": ("country_influence_add = 25", "Communication administrative et diplomatique rapide"),
                "systematic_cadastral_surveying": ("state_tax_capacity_add = 10", "Capacité fiscale fondée sur le cadastre"),
            }
            modifier, proposed_role = modifier_design[tech]
            reason = "Le nœud est actuellement une feuille sans effet ou de trop faible valeur."
            compromise = "Bonus institutionnel limité, directement lié au concept."
            benefit = f"Ajout proposé : {modifier}."
            risk = "LOW: valeur à confirmer en runtime économique."
        elif proposed_parents != current_parents:
            added = proposed_parents - current_parents
            removed = current_parents - proposed_parents
            if added and removed:
                change_type = "REPLACE_EDGE"
            elif removed:
                change_type = "REMOVE_EDGE"
            else:
                change_type = "ADD_EDGE"
            reason = "Rattachement à un socle général ou à la chaîne productive du bâtiment."
            proposed_role = "Spécialisation rattachée à un tronc identifiable"
            compromise = "L’arête représente une capacité générale de gameplay, pas une causalité littérale."
            benefit = "Réduit les roots spécialisés et améliore la lecture de la branche."
            risk = "MEDIUM: vérifier les grants structurels calculés."
        else:
            change_type = "KEEP"
            reason = "Aucun changement architectural prioritaire proposé dans cette passe."
            proposed_role = next((row["Role"] for row in node_rows if row["Technology_ID"] == tech), "Nœud technologique")
            compromise = "Aucun"
            benefit = "Préserve une branche déjà cohérente."
            risk = "LOW"
        current_role = next((row["Role"] for row in node_rows if row["Technology_ID"] == tech), "Nouveau nœud")
        impact_count = sum(row["Technology"] == tech for row in distribution_rows)
        architecture_rows.append({
            "Technology_ID": tech,
            "Current_Parents": ";".join(sorted(current_parents)),
            "Proposed_Parents": ";".join(sorted(proposed_parents)),
            "Current_Era": era_labels.get(tech, "N/A"),
            "Proposed_Era": f"era_{proposed_eras[tech]}",
            "Current_Role": current_role,
            "Proposed_Role": proposed_role,
            "Change_Type": change_type,
            "Reason": reason,
            "Historical_Compromise": compromise,
            "Gameplay_Benefit": benefit,
            "Distribution_Impact": f"{impact_count} grant(s) structurel(s) simulé(s)",
            "Risk": risk,
        })

    content_changes = [
        ("CONTENT:building_artillery_foundry", "MOVE_UNLOCK", "regulated_small_arms", "standardized_field_artillery", "Le bâtiment et son PM de base doivent devenir disponibles ensemble."),
        ("CONTENT:building_cotton_plantation", "MOVE_UNLOCK", "cotton_gin", "aucun gate bâtiment; cotton_gin reste un progrès de PM", "La plantation précède l’égreneuse et ne doit pas bloquer les PM ferroviaires."),
    ]
    for (building, pm), gates in sorted(pm_gate_additions.items()):
        detail = ";".join(sorted(gates))
        if (building, pm) in {
            ("building_electrics_industry", "pm_scientific_management"),
            ("building_automotive_industry", "pm_scientific_management"),
            ("building_rubber_plantation", "pm_steam_rail_transport"),
        }:
            reason = "Créer une variante PM propre au bâtiment avant d’ajouter le gate, car le PM générique est partagé."
        else:
            reason = "Ajouter le gate cumulatif du bâtiment au PM sans modifier la technologie générale."
        content_changes.append((f"CONTENT:{building}:{pm}", "MOVE_UNLOCK", "gates actuels", f"gates actuels + {detail}", reason))
    for object_id, change_type, current, proposed, reason in content_changes:
        architecture_rows.append({
            "Technology_ID": object_id,
            "Current_Parents": current,
            "Proposed_Parents": proposed,
            "Current_Era": "N/A",
            "Proposed_Era": "N/A",
            "Current_Role": "Gate de contenu",
            "Proposed_Role": "Causalité bâtiment → PM garantie",
            "Change_Type": change_type,
            "Reason": reason,
            "Historical_Compromise": "Aucun; correction de disponibilité gameplay.",
            "Gameplay_Benefit": "Supprime une violation de causalité sans transformer une technologie générale en dépendance sectorielle.",
            "Distribution_Impact": "Aucun grant pays attendu",
            "Risk": "MEDIUM: vérifier les PM partagés et l’interface runtime.",
        })
    layout_changes = [
        ("LAYOUT:production_eras_1_4", "Aligner six troncs en couloirs: manufactures, alimentation, agriculture, mines, textile et transport."),
        ("LAYOUT:society_eras_1_5", "Placer savoirs codifiés, administration, presse, finance et médecine sur des lignes distinctes."),
        ("LAYOUT:military_eras_1_5", "Faire diverger doctrine, armements et services depuis le nouveau tronc militaire."),
        ("LAYOUT:naval_eras_1_6", "Faire diverger arsenaux, bassins et connaissances depuis le nouveau tronc naval."),
    ]
    for object_id, reason in layout_changes:
        architecture_rows.append({
            "Technology_ID": object_id,
            "Current_Parents": "N/A",
            "Proposed_Parents": "N/A",
            "Current_Era": "N/A",
            "Proposed_Era": "N/A",
            "Current_Role": "Disposition runtime actuelle",
            "Proposed_Role": "Couloir visuel hiérarchique",
            "Change_Type": "LAYOUT_ONLY",
            "Reason": reason,
            "Historical_Compromise": "Aucun",
            "Gameplay_Benefit": "Réduit les croisements sans créer de dépendance décorative.",
            "Distribution_Impact": "Aucun",
            "Risk": "LOW: la disposition est dérivée du graphe et doit être recontrôlée en jeu.",
        })

    general_rows: list[dict[str, object]] = []
    for tech, data in new_nodes.items():
        grants = sum(row["Technology"] == tech for row in distribution_rows)
        general_rows.append({
            "Proposed_ID": tech,
            "Category": data["category"],
            "Era": f"era_{data['era']}",
            "Concept": data["concept"],
            "Parents": ";".join(sorted(data["parents"])),
            "Children": ";".join(sorted(data["children"])),
            "Gameplay_Effect": data["effect"],
            "Historical_Abstraction": data["abstraction"],
            "Why_Existing_Node_Cannot_Do_It": data["why"],
            "Estimated_Country_Grants": grants,
            "Risk": data["risk"],
        })

    checks = {
        "node rows": (len(node_rows), len(technologies)),
        "unique node IDs": (len({row["Technology_ID"] for row in node_rows}), len(node_rows)),
        "unique building/PM rows": (
            len({(row["Building"], row["Production_Method"]) for row in pm_rows}), len(pm_rows)
        ),
        "unique architecture rows": (
            len({row["Technology_ID"] for row in architecture_rows}), len(architecture_rows)
        ),
        "general nodes": (len(general_rows), 3),
        "unique distribution rows": (
            len({(row["TAG"], row["Technology"]) for row in distribution_rows}),
            len(distribution_rows),
        ),
    }
    failed_checks = [name for name, (actual, expected) in checks.items() if actual != expected]
    if failed_checks:
        raise ValueError("Contrôles CSV en échec: " + ", ".join(failed_checks))
    if current_metrics["graph_cycles"] or proposed_metrics["graph_cycles"]:
        raise ValueError("Cycle détecté dans le graphe actuel ou proposé")
    if proposed_metrics["unknown_parent_ids"] or proposed_metrics["negative_era_edges"]:
        raise ValueError("Parent inconnu ou arête d’era négative dans la proposition")

    write_csv(NODE_AUDIT, [
        "Technology_ID", "Category", "Era", "Parent_Count", "Parents", "Child_Count",
        "Children", "Building_Unlocks", "PM_Unlocks", "Law_Unlocks", "Modifier_Count",
        "Start_Country_Count", "Role", "Problem_Flags", "Recommendation",
    ], node_rows)
    write_csv(PM_AUDIT, [
        "Building", "Building_Unlock_Tech", "Building_Era", "Production_Method",
        "PM_Unlock_Techs", "PM_Min_Era", "Era_Gap", "Building_Tech_Is_Ancestor",
        "Guaranteed_By_Other_Gate", "Violation", "Recommendation",
    ], pm_rows)
    write_csv(ARCHITECTURE, [
        "Technology_ID", "Current_Parents", "Proposed_Parents", "Current_Era",
        "Proposed_Era", "Current_Role", "Proposed_Role", "Change_Type", "Reason",
        "Historical_Compromise", "Gameplay_Benefit", "Distribution_Impact", "Risk",
    ], architecture_rows)
    write_csv(GENERAL_NODES, [
        "Proposed_ID", "Category", "Era", "Concept", "Parents", "Children",
        "Gameplay_Effect", "Historical_Abstraction", "Why_Existing_Node_Cannot_Do_It",
        "Estimated_Country_Grants", "Risk",
    ], general_rows)
    write_csv(DISTRIBUTION, [
        "TAG", "Technology", "Current_Start_Status", "Proposed_Start_Status", "Reason",
        "Decision_Type",
    ], distribution_rows)
    METRICS.write_text(json.dumps({
        "current": current_metrics,
        "proposed": proposed_metrics,
        "audit": {
            "technology_definitions": len(technologies),
            "researchable_technologies": len(active),
            "compatibility_aliases": len(technologies) - len(active),
            "building_definitions": len(buildings),
            "production_method_definitions": len(pms),
            "building_pm_rows": len(pm_rows),
        },
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps({
        "technology_definitions": len(technologies),
        "researchable": len(active),
        "current": current_metrics,
        "proposed": proposed_metrics,
        "pm_rows": len(pm_rows),
        "distribution_rows": len(distribution_rows),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
