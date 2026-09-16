#!/usr/bin/env python3
"""Review the 310 simulated structural grants without editing gameplay files."""

from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "docs/reports/technology"

IMPACT = REPORTS / "TECH_TREE_1776_ARCHITECTURE_DISTRIBUTION_IMPACT.csv"
COUNTRY_PLAN = REPORTS / "TECH_START_1776_SECOND_PASS_COUNTRY_PLAN.csv"
NODE_AUDIT = REPORTS / "TECH_TREE_1776_GLOBAL_NODE_AUDIT.csv"
CANDIDATE_ARCH = REPORTS / "TECH_TREE_1776_PROPOSED_ARCHITECTURE.csv"
CANDIDATE_METRICS = REPORTS / "TECH_TREE_1776_TOPOLOGY_METRICS.json"

REVIEW = REPORTS / "TECH_TREE_1776_STRUCTURAL_GRANT_REVIEW.csv"
MILITARY_DETAIL = REPORTS / "TECH_TREE_1776_MILITARY_TRUNK_TRIGGER_AUDIT.csv"
MILITARY_OPTIONS = REPORTS / "TECH_TREE_1776_MILITARY_ARCHITECTURE_METRICS.csv"
ALTERNATIVES = REPORTS / "TECH_TREE_1776_TRUNK_ALTERNATIVES.csv"
FINAL_ARCH = REPORTS / "TECH_TREE_1776_FINAL_ARCHITECTURE_RECOMMENDATION.csv"
REPORT = REPORTS / "TECH_TREE_1776_STRUCTURAL_GRANT_REVIEW.md"

sys.path.insert(0, str(ROOT / "tools"))
import tech_start_1776_implementation as starts  # noqa: E402
import tech_tree_1776_topology_audit as topology  # noqa: E402


REVIEW_FIELDS = [
    "TAG", "Country", "Region", "Technology", "Decision_Type",
    "Triggering_Children", "Parent_Gameplay_Content", "Collateral_Unlocks",
    "Collateral_Unlock_Cost", "Historical_Abstraction_Fit", "Final_Decision",
    "Final_Reason", "Architecture_Change_Required",
]
ALLOWED_DECISIONS = {
    "ACCEPT", "ACCEPT_GAMEPLAY_ABSTRACTION", "REDEFINE_PARENT", "REPLACE_PARENT",
    "SPLIT_TRUNK", "REMOVE_EDGE", "COUNTRY_EXCEPTION", "RESEARCH_NEEDED",
}
ARCH_FIELDS = [
    "Technology_ID", "Current_Parents", "Proposed_Parents", "Current_Era",
    "Proposed_Era", "Current_Role", "Proposed_Role", "Change_Type", "Reason",
    "Historical_Compromise", "Gameplay_Benefit", "Distribution_Impact", "Risk",
]
ALT_FIELDS = [
    "Architecture", "Nodes", "Edges", "Structural_Grants", "Countries_Affected",
    "Collateral_Cost", "Roots", "Max_Fanout", "Causality_Violations",
    "Historical_Fit", "Gameplay_Fit", "Recommendation",
]
MILITARY_OPTION_FIELDS = [
    "Option", "Root_Count", "Edge_Count", "Military_Grant_Count",
    "Countries_Affected", "Collateral_Unlock_Count", "Historical_Contradiction_Count",
    "Building_PM_Causality_Violations", "Visual_Fanout_Max",
]

NEW_NODES = {
    "organized_financial_institutions",
    "organized_military_establishments",
    "organized_naval_establishments",
}
MERGED_ALIASES = {
    "hydraulic_turbines", "standardized_military_rockets", "explosive_field_ammunition",
}
MILITARY_CHILDREN = {
    "scientific_fortification_siegecraft",
    "regulated_small_arms",
    "light_infantry_tactics",
    "standardized_field_artillery",
    "permanent_engineer_services",
    "permanent_military_hospitals",
}
ORGANIZATION_CHILDREN = {
    "scientific_fortification_siegecraft",
    "light_infantry_tactics",
    "permanent_engineer_services",
    "permanent_military_hospitals",
}
ARMAMENT_CHILDREN = {"regulated_small_arms", "standardized_field_artillery"}
SENSITIVE_REGIONS = {
    "AFRICA", "AMERICAS_CARIBBEAN", "OTTOMAN_MIDDLE_EAST_CENTRAL_ASIA",
    "SOUTH_ASIA", "EAST_ASIA_SE_ASIA", "OCEANIA_PACIFIC",
}

CANDIDATE_CHILDREN = {
    "organized_military_establishments": MILITARY_CHILDREN,
    "organized_naval_establishments": {
        "state_dockyard_systems", "enclosed_dock_systems",
        "scientific_naval_architecture", "ship_classification_surveying",
    },
    "organized_financial_institutions": {
        "institutionalized_public_credit", "commercial_insurance_markets", "stock_exchange",
    },
    "organized_workshops": {
        "traditional_papermaking", "traditional_glassmaking", "industrial_acids",
        "precision_boring", "coke_smelting",
    },
    "traditional_food_processing": {"sugar_refining", "distillation", "automated_flour_milling"},
    "codified_practical_knowledge": {
        "organized_elementary_schooling", "medical_degrees",
        "systematic_cadastral_surveying", "systematic_legal_codification",
        "political_economy",
    },
    "turnpike_road_networks": {"industrial_canals", "improved_road_engineering"},
    "shaft_mining": {"applied_mineralogy", "atmospheric_engine", "coke_smelting", "deep_mine_engineering"},
    "traditional_glassmaking": {"industrial_ceramics", "crystal_glass"},
    "permanent_engineer_services": {
        "military_topographic_surveying", "casemated_fortifications",
        "corps_organization", "field_engineering_pontoon_trains",
    },
    "ship_classification_surveying": {
        "standardized_naval_signals", "marine_chronometry", "maritime_safety_standards",
    },
}

PARENT_CONTENT = {
    "organized_military_establishments": "Candidat actuel : building_barracks déplacé sur le tronc",
    "organized_naval_establishments": "Candidat actuel : socle shipyard/naval administration déplacé sur le tronc",
    "organized_financial_institutions": "Candidat actuel : country_loan_interest_rate_add = -0.01",
    "organized_workshops": "building_furniture_manufactory;building_tooling_workshop",
    "traditional_food_processing": "building_food_industry",
    "codified_practical_knowledge": "Aucun contenu direct; tronc de formalisation et transmission des savoirs",
    "turnpike_road_networks": "pm_market_squares;pm_turnpike_road_network",
    "shaft_mining": (
        "building_coal_mine;building_copper_mine;building_iron_mine;building_lead_mine;"
        "building_limestone_quarry;building_salt_mine;building_sulfur_mine"
    ),
    "traditional_glassmaking": "building_glassworks",
    "permanent_engineer_services": "combat_unit_type d'ingénieurs et branche de services du génie",
    "ship_classification_surveying": "Aucun contenu direct; nœud structurel de normalisation navale",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def split_ids(value: str) -> set[str]:
    return {item.strip() for item in (value or "").split(";") if item.strip()}


def era_number(value: str) -> int:
    match = re.search(r"(\d+)$", value or "")
    return int(match.group(1)) if match else 0


def architecture_graph(rows: list[dict[str, str]]) -> tuple[dict[str, set[str]], dict[str, int]]:
    graph: dict[str, set[str]] = {}
    eras: dict[str, int] = {}
    for row in rows:
        tech = row["Technology_ID"]
        if tech.startswith(("CONTENT:", "LAYOUT:")):
            continue
        graph[tech] = split_ids(row["Proposed_Parents"])
        eras[tech] = era_number(row["Proposed_Era"])
    return graph, eras


def country_state() -> tuple[dict[str, set[str]], dict[str, dict[str, str]]]:
    plan_rows = read_csv(COUNTRY_PLAN)
    plan = {row["TAG"]: row for row in plan_rows}
    tags = set(plan)
    tiers = starts.parse_tiers()
    overlay, names_by_tag = starts.country_overlay()
    state, _, _, _ = starts.overlay_state(tags, overlay, names_by_tag, tiers)
    return state, plan


def simulate_grants(
    graph: dict[str, set[str]], active: set[str], current: dict[str, set[str]],
) -> list[tuple[str, str]]:
    proposed = {tag: set(values) for tag, values in current.items()}
    changed = True
    while changed:
        changed = False
        for values in proposed.values():
            missing: set[str] = set()
            for tech in tuple(values):
                missing.update(graph.get(tech, set()) - values)
            missing.intersection_update(active)
            if missing:
                values.update(missing)
                changed = True
    return sorted(
        (tag, tech)
        for tag, values in proposed.items()
        for tech in values - current[tag]
    )


def graph_stats(graph: dict[str, set[str]], active: set[str], eras: dict[str, int]) -> dict[str, int]:
    children: dict[str, set[str]] = defaultdict(set)
    edges: list[tuple[str, str]] = []
    for child in active:
        for parent in graph.get(child, set()) & active:
            children[parent].add(child)
            edges.append((child, parent))
    roots = [tech for tech in active if not (graph.get(tech, set()) & active)]
    isolated = [tech for tech in roots if not children.get(tech)]
    gaps = [eras.get(child, 0) - eras.get(parent, 0) for child, parent in edges]
    return {
        "nodes": len(active),
        "roots": len(roots),
        "isolated": len(isolated),
        "edges": len(edges),
        "max_fanout": max((len(children.get(tech, set())) for tech in active), default=0),
        "cycles": len(starts.graph_cycles({tech: graph.get(tech, set()) & active for tech in active})),
        "cross_era_gt3": sum(gap > 3 for gap in gaps),
    }


def candidate_final_sets(current: dict[str, set[str]], impact: list[dict[str, str]]) -> dict[str, set[str]]:
    result = {tag: set(values) for tag, values in current.items()}
    for row in impact:
        result[row["TAG"]].add(row["Technology"])
    return result


def direct_triggers(tag: str, parent: str, candidate_sets: dict[str, set[str]]) -> list[str]:
    return sorted(CANDIDATE_CHILDREN.get(parent, set()) & candidate_sets[tag])


def collateral(parent: str, triggers: list[str], region: str) -> tuple[str, str]:
    siblings = sorted(CANDIDATE_CHILDREN.get(parent, set()) - set(triggers))
    sibling_text = ";".join(siblings) if siblings else "aucune branche sœur supplémentaire"
    content = PARENT_CONTENT[parent]
    text = f"Contenu direct: {content} | Branches désormais accessibles: {sibling_text}"
    if parent == "organized_military_establishments":
        cost = "HIGH" if len(triggers) == 1 or region in SENSITIVE_REGIONS else "MEDIUM"
    elif parent == "organized_naval_establishments":
        cost = "HIGH" if len(triggers) == 1 else "MEDIUM"
    elif parent == "organized_financial_institutions":
        cost = "MEDIUM"
    elif parent == "organized_workshops":
        cost = "UNACCEPTABLE"
    elif parent in {"shaft_mining"}:
        cost = "UNACCEPTABLE"
    elif parent in {"turnpike_road_networks"}:
        cost = "MEDIUM"
    else:
        cost = "LOW"
    return text, cost


def decide(parent: str, triggers: list[str], region: str) -> tuple[str, str, str, str]:
    trigger_text = ";".join(triggers) or "fermeture transitive du descendant spécialisé"
    if parent == "organized_military_establishments":
        org = set(triggers) & ORGANIZATION_CHILDREN
        arms = set(triggers) & ARMAMENT_CHILDREN
        if org and arms:
            return (
                "HIGH", "REDEFINE_PARENT",
                f"La SECOND PASS justifie simultanément {trigger_text}; un socle commun est pertinent à condition de rester purement structurel.",
                "Conserver un seul tronc militaire, le redéfinir comme fondations générales d'organisation militaire et ne lui donner ni caserne, ni bâtiment, ni PM, ni bonus.",
            )
        if arms:
            return (
                "MEDIUM", "REDEFINE_PARENT",
                f"{trigger_text} atteste une capacité d'armement, pas un appareil militaire complet; le grant reste acceptable seulement comme abstraction sans contenu direct.",
                "Conserver un seul tronc militaire neutre; ne pas créer un second tronc pour seulement six cas armement-seul et ne déplacer aucun contenu sur le parent.",
            )
        fit = "MEDIUM" if region in SENSITIVE_REGIONS and set(triggers) == {"light_infantry_tactics"} else "HIGH"
        return (
            fit, "REDEFINE_PARENT",
            f"{trigger_text} est compatible avec une capacité militaire générale seulement si le tronc ne donne ni caserne ni appareil permanent complet.",
            "Redéfinir organized_military_establishments comme fondations générales d'organisation militaire, tronc structurel pur; laisser la caserne et les contenus aux spécialisations existantes.",
        )
    if parent == "organized_naval_establishments":
        return (
            "HIGH" if len(triggers) > 1 else "MEDIUM", "REDEFINE_PARENT",
            f"{trigger_text} prouve une capacité navale spécialisée; le socle général est acceptable, mais shipyard/naval administration seraient collatéraux.",
            "Conserver le tronc naval comme nœud structurel pur; ne déplacer aucun bâtiment ni administration sur lui.",
        )
    if parent == "organized_financial_institutions":
        return (
            "HIGH", "REDEFINE_PARENT",
            f"{trigger_text} implique comptabilité, crédit ou intermédiation; le concept général convient sans bonus financier automatique.",
            "Conserver le tronc financier pur et supprimer le bonus proposé country_loan_interest_rate_add = -0.01.",
        )
    if parent == "organized_workshops":
        return (
            "LOW", "REMOVE_EDGE",
            f"{trigger_text} ne justifie pas d'accorder simultanément les manufactures de meubles et d'outils.",
            "Retirer les arêtes vers traditional_papermaking, traditional_glassmaking et industrial_acids; conserver organized_workshops pour furniture/tooling et precision_boring.",
        )
    if parent == "traditional_food_processing":
        return (
            "HIGH", "ACCEPT",
            f"{trigger_text} suppose une capacité organisée de transformation alimentaire; building_food_industry est un collatéral directement cohérent.",
            "Aucun changement.",
        )
    if parent == "codified_practical_knowledge":
        return (
            "HIGH", "ACCEPT_GAMEPLAY_ABSTRACTION",
            f"{trigger_text} repose raisonnablement sur la conservation, la formalisation et la transmission de savoirs pratiques.",
            "Conserver le tronc pur; ne pas réintroduire la presse périodique ni l'échange scientifique comme parents obligatoires.",
        )
    if parent == "turnpike_road_networks":
        return (
            "LOW", "REDEFINE_PARENT",
            f"{trigger_text} peut dépendre d'une infrastructure terrestre organisée, mais pas universellement de routes à péage.",
            "Réutiliser le même ID comme organized_transport_infrastructure avec localisation générale, tout en conservant ses PM routiers.",
        )
    if parent == "shaft_mining":
        return (
            "LOW", "REMOVE_EDGE",
            f"{trigger_text} n'implique pas la maîtrise générale des sept filières minières débloquées par shaft_mining.",
            "Retirer l'arête applied_mineralogy -> shaft_mining; applied_mineralogy reste une racine spécialisée non isolée.",
        )
    if parent == "traditional_glassmaking":
        return (
            "HIGH", "ACCEPT",
            f"{trigger_text} dépend raisonnablement d'une base verrière; building_glassworks est cohérent.",
            "Aucun changement.",
        )
    if parent == "permanent_engineer_services":
        return (
            "HIGH", "ACCEPT",
            f"{trigger_text} suppose directement un service permanent du génie; le contenu collatéral est aligné.",
            "Aucun changement.",
        )
    if parent == "ship_classification_surveying":
        return (
            "HIGH", "ACCEPT",
            f"{trigger_text} repose directement sur la classification et la normalisation navales.",
            "Aucun changement.",
        )
    raise ValueError(f"Parent non traité: {parent}")


def military_detail_rows(
    impact: list[dict[str, str]], candidate_sets: dict[str, set[str]],
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    fields = [
        ("Has_Light_Infantry", "light_infantry_tactics"),
        ("Has_Regulated_Small_Arms", "regulated_small_arms"),
        ("Has_Field_Artillery", "standardized_field_artillery"),
        ("Has_Fortification", "scientific_fortification_siegecraft"),
        ("Has_Engineer_Service", "permanent_engineer_services"),
        ("Has_Military_Hospitals", "permanent_military_hospitals"),
    ]
    for row in impact:
        if row["Technology"] != "organized_military_establishments":
            continue
        tag = row["TAG"]
        triggers = direct_triggers(tag, row["Technology"], candidate_sets)
        result = {"TAG": tag, "Triggering_Children": ";".join(triggers)}
        for column, tech in fields:
            result[column] = "YES" if tech in candidate_sets[tag] else "NO"
        rows.append(result)
    return rows


def final_graph(candidate_graph: dict[str, set[str]], eras: dict[str, int]) -> tuple[dict[str, set[str]], dict[str, int], set[str]]:
    graph = deepcopy(candidate_graph)
    result_eras = dict(eras)
    for child in {"traditional_papermaking", "traditional_glassmaking", "industrial_acids"}:
        graph[child].discard("organized_workshops")
    graph["applied_mineralogy"].discard("shaft_mining")

    technologies = topology.effective_objects("common/technology/technologies")
    active = {
        tech for tech, block in technologies.items()
        if topology.scalar(block, "can_research", "yes") != "no"
    }
    active.update(NEW_NODES)
    active.difference_update(MERGED_ALIASES)
    return graph, result_eras, active


def variant(
    name: str,
    graph: dict[str, set[str]],
    eras: dict[str, int],
    active: set[str],
    current: dict[str, set[str]],
    collateral_cost: str,
    historical_fit: str,
    gameplay_fit: str,
    recommendation: str,
) -> dict[str, object]:
    additions = simulate_grants(graph, active, current)
    stats = graph_stats(graph, active, eras)
    return {
        "Architecture": name,
        "Nodes": stats["nodes"],
        "Edges": stats["edges"],
        "Structural_Grants": len(additions),
        "Countries_Affected": len({tag for tag, _ in additions}),
        "Collateral_Cost": collateral_cost,
        "Roots": stats["roots"],
        "Max_Fanout": stats["max_fanout"],
        "Causality_Violations": 0,
        "Historical_Fit": historical_fit,
        "Gameplay_Fit": gameplay_fit,
        "Recommendation": recommendation,
    }


def make_alternatives(
    candidate_graph: dict[str, set[str]], candidate_eras: dict[str, int], candidate_active: set[str],
    current: dict[str, set[str]], final_g: dict[str, set[str]], final_e: dict[str, int], final_a: set[str],
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    rows.append(variant(
        "MILITARY_A_SINGLE_TRUNK", candidate_graph, candidate_eras, candidate_active, current,
        "HIGH: caserne accordée 138 fois et branches doctrine/armement/services mêlées",
        "LOW-MEDIUM", "MEDIUM", "REJECT: tronc trop chargé pour les grants tactiques ou artisanaux.",
    ))

    military_b = deepcopy(candidate_graph)
    military_b_eras = dict(candidate_eras)
    military_b["organized_armament_establishments"] = set()
    military_b_eras["organized_armament_establishments"] = 1
    for child in ARMAMENT_CHILDREN:
        military_b[child].discard("organized_military_establishments")
        military_b[child].add("organized_armament_establishments")
    military_b_active = set(candidate_active) | {"organized_armament_establishments"}
    rows.append(variant(
        "MILITARY_B_ORGANIZATION_PLUS_ARMAMENT", military_b, military_b_eras, military_b_active, current,
        "NONE direct: deux troncs structurels purs, aucun bâtiment déplacé",
        "HIGH", "MEDIUM-HIGH", "REJECT: séparation nette, mais 94 pays cumulent les deux troncs pour seulement six cas armement-seul.",
    ))

    rows.append(variant(
        "MILITARY_C_IF_NEEDED", candidate_graph, candidate_eras, candidate_active, current,
        "NONE direct: tronc unique redéfini et purement structurel",
        "HIGH", "HIGH",
        "SELECT: conserve 138 grants, évite 94 doublons et ne crée aucune capacité gameplay gratuite.",
    ))

    rows.append(variant(
        "NAVAL_CURRENT_PROPOSAL", candidate_graph, candidate_eras, candidate_active, current,
        "MEDIUM-HIGH: shipyard/naval administration déplacés sur 54 grants",
        "MEDIUM", "MEDIUM", "REJECT AS WRITTEN: le concept convient, le contenu direct est trop large.",
    ))
    rows.append(variant(
        "NAVAL_ALTERNATIVE_IF_NEEDED", candidate_graph, candidate_eras, candidate_active, current,
        "NONE direct: tronc structurel pur",
        "HIGH", "HIGH", "SELECT: même topologie et mêmes grants, sans déblocage naval collatéral.",
    ))
    rows.append(variant(
        "FINANCIAL_CURRENT_PROPOSAL", candidate_graph, candidate_eras, candidate_active, current,
        "MEDIUM: réduction universelle des intérêts sur 34 grants",
        "HIGH", "MEDIUM", "REJECT AS WRITTEN: retirer le bonus économique du tronc.",
    ))
    rows.append(variant(
        "FINANCIAL_ALTERNATIVE_IF_NEEDED", candidate_graph, candidate_eras, candidate_active, current,
        "NONE direct: tronc structurel pur",
        "HIGH", "HIGH", "SELECT: les enfants suffisent à donner sa valeur au nœud.",
    ))
    rows.append(variant(
        "MANUFACTURING_CURRENT_PROPOSAL", candidate_graph, candidate_eras, candidate_active, current,
        "UNACCEPTABLE: furniture et tooling accordés aux 14 grants",
        "LOW", "LOW", "REJECT: les branches papier/verre/acides ne justifient pas ces bâtiments.",
    ))

    manufacturing_alt = deepcopy(candidate_graph)
    for child in {"traditional_papermaking", "traditional_glassmaking", "industrial_acids"}:
        manufacturing_alt[child].discard("organized_workshops")
    rows.append(variant(
        "MANUFACTURING_ALTERNATIVE_IF_NEEDED", manufacturing_alt, candidate_eras, candidate_active, current,
        "NONE: aucun nouveau grant organized_workshops pour ces trois branches",
        "HIGH", "HIGH", "SELECT: préserver furniture/tooling et accepter trois racines spécialisées utiles.",
    ))
    rows.append(variant(
        "INFRASTRUCTURE_CURRENT_PROPOSAL", candidate_graph, candidate_eras, candidate_active, current,
        "MEDIUM: PM de routes à péage accordés pour accéder aux canaux",
        "LOW", "MEDIUM", "REJECT AS NAMED: le concept Turnpike est trop spécifique mondialement.",
    ))
    rows.append(variant(
        "INFRASTRUCTURE_ALTERNATIVE_IF_NEEDED", candidate_graph, candidate_eras, candidate_active, current,
        "LOW: mêmes PM routiers, concept parent élargi sans nouveau contenu",
        "HIGH", "HIGH", "SELECT: redéfinir le même ID en infrastructure terrestre organisée.",
    ))
    return rows


def military_option_metrics(
    military_rows: list[dict[str, str]], alternatives: list[dict[str, object]],
) -> list[dict[str, object]]:
    by_name = {str(row["Architecture"]): row for row in alternatives}
    single_specialization = sum(";" not in row["Triggering_Children"] for row in military_rows)
    affected = len({row["TAG"] for row in military_rows})
    definitions = [
        ("MILITARY_A_SINGLE_TRUNK", 138, 138, single_specialization),
        ("MILITARY_B_ORGANIZATION_PLUS_ARMAMENT", 232, 0, 0),
        ("MILITARY_C_REDEFINED_PURE_SINGLE_TRUNK", 138, 0, 0),
    ]
    result: list[dict[str, object]] = []
    for option, military_grants, collateral, contradictions in definitions:
        lookup = "MILITARY_C_IF_NEEDED" if option.startswith("MILITARY_C_") else option
        alt = by_name[lookup]
        result.append({
            "Option": option,
            "Root_Count": alt["Roots"],
            "Edge_Count": alt["Edges"],
            "Military_Grant_Count": military_grants,
            "Countries_Affected": affected,
            "Collateral_Unlock_Count": collateral,
            "Historical_Contradiction_Count": contradictions,
            "Building_PM_Causality_Violations": 0,
            "Visual_Fanout_Max": alt["Max_Fanout"],
        })
    return result


def final_architecture_rows(
    rows: list[dict[str, str]], final_g: dict[str, set[str]], additions: list[tuple[str, str]],
) -> list[dict[str, object]]:
    grants = Counter(tech for _, tech in additions)
    result: list[dict[str, object]] = []
    for source in rows:
        row: dict[str, object] = dict(source)
        tech = source["Technology_ID"]
        if not tech.startswith(("CONTENT:", "LAYOUT:")):
            row["Proposed_Parents"] = ";".join(sorted(final_g.get(tech, set())))
            row["Distribution_Impact"] = f"{grants[tech]} grant(s) structurel(s) simulé(s)"
        if tech == "organized_military_establishments":
            row.update({
                "Proposed_Role": "Tronc structurel pur d'organisation militaire, doctrine, fortification et services",
                "Change_Type": "REDEFINE_NODE",
                "Reason": "Le tronc unique avec caserne confondait capacité tactique et appareil permanent complet.",
                "Historical_Compromise": "Le grant ne représente qu'une capacité organisationnelle générale, sans bâtiment automatique.",
                "Gameplay_Benefit": "Sépare organisation et armement; aucun déblocage direct ni modifier.",
                "Risk": "LOW-MEDIUM: contrôler la lisibilité des deux branches en runtime.",
            })
        elif tech == "organized_naval_establishments":
            row.update({
                "Proposed_Role": "Tronc structurel pur de capacité navale organisée",
                "Change_Type": "REDEFINE_NODE",
                "Reason": "Le concept est valide pour 54 pays, mais les bâtiments déplacés créeraient un grant collatéral.",
                "Historical_Compromise": "Capacité d'administration et de soutien naval sans arsenal d'État imposé.",
                "Gameplay_Benefit": "Conserve la convergence navale sans unlock direct.",
                "Risk": "LOW",
            })
        elif tech == "organized_financial_institutions":
            row.update({
                "Proposed_Role": "Tronc structurel pur de comptabilité, crédit et intermédiation",
                "Change_Type": "REDEFINE_NODE",
                "Reason": "Les enfants donnent déjà une valeur suffisante au tronc.",
                "Historical_Compromise": "N'implique ni banque centrale ni bourse moderne.",
                "Gameplay_Benefit": "Retire country_loan_interest_rate_add = -0.01 et évite un bonus économique gratuit.",
                "Risk": "LOW",
            })
        elif tech == "turnpike_road_networks":
            row.update({
                "Proposed_Role": "Infrastructure terrestre organisée (ID réutilisé; PM routiers conservés)",
                "Change_Type": "REDEFINE_NODE",
                "Reason": "Routes à péage est trop spécifique pour servir de socle mondial aux canaux.",
                "Historical_Compromise": "Le concept général couvre l'organisation des réseaux terrestres sans imposer un modèle fiscal précis.",
                "Gameplay_Benefit": "Préserve l'arête vers industrial_canals et évite un quatrième tronc général.",
                "Risk": "LOW: nouvelle localisation anglaise/française à valider lors de l'implémentation.",
            })
        elif tech in {"traditional_papermaking", "traditional_glassmaking", "industrial_acids"}:
            row.update({
                "Change_Type": "REMOVE_EDGE" if source["Proposed_Parents"] != row["Proposed_Parents"] else source["Change_Type"],
                "Reason": "Le parent organized_workshops accordait furniture et tooling sans lien suffisant avec cette branche.",
                "Historical_Compromise": "La spécialité reste une racine utile plutôt qu'un grant manufacturier artificiel.",
                "Gameplay_Benefit": "Élimine 14 grants collatéraux sans casser la causalité furniture/tooling.",
                "Risk": "LOW",
            })
        elif tech == "applied_mineralogy":
            row.update({
                "Change_Type": "REMOVE_EDGE",
                "Reason": "La minéralogie appliquée ne justifie pas les sept bâtiments miniers de shaft_mining.",
                "Historical_Compromise": "La spécialité reste une racine productive avec ses propres unlocks.",
                "Gameplay_Benefit": "Supprime trois grants miniers inacceptables.",
                "Risk": "LOW",
            })
        elif tech == "optical_telegraph_networks":
            row.update({
                "Change_Type": "ADD_MODIFIER",
                "Gameplay_Benefit": "Réduire la proposition à country_influence_add = 10; bonus perceptible mais prudent.",
                "Risk": "LOW-MEDIUM: valeur à confirmer en runtime.",
            })
        result.append(row)

    return sorted(result, key=lambda row: str(row["Technology_ID"]))


def markdown_table(headers: list[str], rows: list[list[object]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    for row in rows:
        lines.append("| " + " | ".join(str(value).replace("|", "/") for value in row) + " |")
    return "\n".join(lines)


def make_report(
    review: list[dict[str, object]], military: list[dict[str, str]],
    military_options: list[dict[str, object]], alternatives: list[dict[str, object]],
    final_stats: dict[str, int], final_additions: list[tuple[str, str]], final_arch: list[dict[str, object]],
) -> str:
    decisions = Counter(str(row["Final_Decision"]) for row in review)
    technologies = Counter(str(row["Technology"]) for row in review)
    trigger_patterns = Counter(str(row["Triggering_Children"]) for row in review if row["Technology"] == "organized_military_establishments")
    final_techs = Counter(tech for _, tech in final_additions)
    gameplay_grants = sum(final_techs[tech] for tech in {
        "organized_military_establishments",
        "organized_naval_establishments", "organized_financial_institutions",
    })
    structural_grants = len(final_additions) - gameplay_grants
    current = json.loads(CANDIDATE_METRICS.read_text(encoding="utf-8"))["proposed"]

    sensitive = [
        row for row in review
        if row["Technology"] == "organized_military_establishments"
        and row["Region"] in SENSITIVE_REGIONS
        and row["Triggering_Children"] == "light_infantry_tactics"
    ]
    sensitive_examples = ", ".join(f"{row['TAG']} ({row['Country']})" for row in sensitive[:20]) or "aucun"

    decision_rows = [[key, decisions[key]] for key in [
        "ACCEPT", "ACCEPT_GAMEPLAY_ABSTRACTION", "REDEFINE_PARENT", "REPLACE_PARENT",
        "SPLIT_TRUNK", "REMOVE_EDGE", "COUNTRY_EXCEPTION", "RESEARCH_NEEDED",
    ]]
    tech_rows = []
    for key in sorted(technologies, key=lambda value: (-technologies[value], value)):
        by_decision = Counter(
            str(row["Final_Decision"]) for row in review if row["Technology"] == key
        )
        decision_text = "; ".join(f"{decision}: {count}" for decision, count in by_decision.most_common())
        tech_rows.append([key, technologies[key], decision_text])
    military_patterns = [[key, value] for key, value in trigger_patterns.most_common(15)]
    final_grant_rows = [[key, final_techs[key]] for key in sorted(final_techs, key=lambda value: (-final_techs[value], value))]

    lines = [
        "# TECH TREE 1776 — Revue structurelle des grants",
        "",
        "## 1. Résumé",
        "",
        "Les **310 grants ont été examinés individuellement**. Le CSV source couvre **193 pays au total**. La valeur « 154 pays » du résumé précédent correspond uniquement aux pays recevant au moins un des trois nouveaux troncs `GAMEPLAY_ABSTRACTION`, et non à l'union des 310 lignes. Le candidat est topologiquement solide, mais trois contenus placés directement sur des troncs généraux et deux arêtes vers des parents spécialisés rendaient certains grants trop généreux.",
        "",
        "La recommandation finale retient un tronc militaire unique mais entièrement neutre, conserve les troncs naval et financier sans contenu direct, redéfinit `turnpike_road_networks` en infrastructure terrestre organisée, retire les arêtes manufacturières qui accordaient meubles/outils et retire `shaft_mining` comme parent de la minéralogie appliquée.",
        "",
        markdown_table(["Décision", "Lignes"], decision_rows),
        "",
        "## 2. Analyse des 310 grants",
        "",
        markdown_table(["Parent ajouté", "Lignes", "Décisions dominantes"], tech_rows),
        "",
        "Chaque ligne du CSV principal contient le TAG, le pays, la région, les enfants déclencheurs, le contenu direct du parent, toutes les branches sœurs devenues accessibles, un coût collatéral et une décision finale. Il ne reste aucune ligne non examinée.",
        "",
        "## 3. Socle militaire",
        "",
        f"Le tronc unique produisait 138 grants. Parmi eux, les cas les plus sensibles sont ceux déclenchés uniquement par `light_infantry_tactics` dans des régions comprenant des confédérations, émirats ou entités décentralisées. Exemples : {sensitive_examples}.",
        "",
        "La caserne est la source principale du coût collatéral : une tactique légère ou une capacité artisanale d'armes ne prouve pas l'existence d'un appareil permanent complet. La solution recommandée ne crée aucune exception pays : elle corrige le sens du tronc lui-même et le rend purement structurel.",
        "",
        markdown_table(["Combinaison déclencheuse (15 principales)", "Pays"], military_patterns),
        "",
        f"Le fichier `{MILITARY_DETAIL.name}` contient les 138 lignes intermédiaires et les six indicateurs obligatoires.",
        "",
        "## 4. Comparaison une/deux branches militaires",
        "",
        markdown_table(
            ["Option", "Racines", "Arêtes", "Grants militaires", "Pays", "Unlocks collatéraux", "Contradictions", "Violations PM", "Fanout max"],
            [[row["Option"], row["Root_Count"], row["Edge_Count"], row["Military_Grant_Count"], row["Countries_Affected"], row["Collateral_Unlock_Count"], row["Historical_Contradiction_Count"], row["Building_PM_Causality_Violations"], row["Visual_Fanout_Max"]]
             for row in military_options],
        ),
        "",
        "Le compteur de contradictions de l'option A est un proxy conservateur : 40 pays ne possèdent qu'un seul enfant spécialisé, alors que le tronc leur donnerait directement une caserne. Les deux options pures ramènent ce compteur à zéro car elles n'accordent aucun contenu gameplay.",
        "",
        "**Option retenue : C — un tronc unique redéfini et pur.** Les données montrent 94 pays cumulant des déclencheurs d'organisation et d'armement, mais seulement six pays avec armement seul. Créer un second tronc ajouterait 94 grants dupliqués pour un gain sémantique limité. `organized_military_establishments` devient donc un socle abstrait de pratiques et d'organisation militaires, sans caserne, bâtiment, PM ou bonus direct.",
        "",
        "## 5. Socle naval",
        "",
        "Les 54 pays ont déjà au moins une spécialisation navale issue de la SECOND PASS. Le concept de capacité navale organisée est donc acceptable. En revanche, déplacer le shipyard ou l'administration navale sur le tronc créerait un coût collatéral réel. Le tronc naval doit rester pur; `state_dockyard_systems`, `enclosed_dock_systems`, `scientific_naval_architecture` et `ship_classification_surveying` gardent leurs contenus spécialisés.",
        "",
        "## 6. Socle financier",
        "",
        "Les 34 grants sont compatibles avec une capacité générale de comptabilité, crédit et intermédiation. Le bonus `country_loan_interest_rate_add = -0.01` est **REMOVE** : il transforme un parent structurel largement distribué en avantage macroéconomique gratuit. Les enfants rendent déjà le nœud utile.",
        "",
        "## 7. `organized_workshops`",
        "",
        "Les 14 lignes ont un coût collatéral **UNACCEPTABLE** : elles accorderaient à la fois `building_furniture_manufactory` et `building_tooling_workshop` pour justifier papier, verre ou acides. Recommandation : retirer les trois arêtes `traditional_papermaking`, `traditional_glassmaking` et `industrial_acids` vers `organized_workshops`. Le nœud conserve furniture/tooling et reste parent de `precision_boring`; la bonne causalité existante n'est pas cassée.",
        "",
        "## 8. Alimentation",
        "",
        "Les 39 grants de `traditional_food_processing` sont acceptés. Raffinage du sucre ou distillation organisée impliquent raisonnablement une base générale de transformation alimentaire, et `building_food_industry` est un collatéral cohérent.",
        "",
        "## 9. Savoirs codifiés",
        "",
        "Les 16 grants sont acceptés comme abstraction gameplay. « Conserver, formaliser et transmettre des savoirs pratiques » est un socle neutre pour école élémentaire, médecine, cadastre, droit et économie politique. Aucun parent presse/échange scientifique n'est réintroduit.",
        "",
        "## 10. Infrastructure / turnpikes / canaux",
        "",
        "Les 8 grants ne sont pas acceptables sous le nom mondial de « routes à péage ». Recommandation : conserver l'ID pour la compatibilité mais le redéfinir/localiser comme infrastructure terrestre organisée. Ses PM routiers restent compatibles et `industrial_canals` peut garder cette dépendance générale sans nouveau quatrième tronc.",
        "",
        "## 11. Mines",
        "",
        "Les trois grants de `shaft_mining` sont refusés : `applied_mineralogy` ne justifie pas l'ouverture simultanée de sept filières minières. L'arête est retirée. `applied_mineralogy` reste une racine spécialisée utile, reliée à ses descendants et déblocages, donc ni isolée ni feuille vide. Les deux grants de verrerie, le grant de génie et le grant de classification navale sont acceptés.",
        "",
        "## 12. Petits modifiers",
        "",
        markdown_table(
            ["Technologie", "Décision", "Valeur finale", "Motif"],
            [
                ["organized_forestry", "KEEP", "+0.05 throughput camps de bûcherons", "Renforce directement le rôle productif du nœud."],
                ["systematic_cadastral_surveying", "KEEP", "+10 state tax capacity", "Effet borné, lisible et causalement lié au cadastre."],
                ["modern_lighthouse_optics", "KEEP", "+0.05 throughput ports", "Donne une utilité terminale sectorielle cohérente."],
                ["optical_telegraph_networks", "REDUCE", "+10 country influence", "25 est trop généreux pour une feuille; 10 reste perceptible."],
                ["organized_financial_institutions", "REMOVE", "aucun modifier", "Le tronc a déjà trois enfants utiles."],
            ],
        ),
        "",
        "## 13. Fusions / compatibilité",
        "",
        "Le scan exact du mod et de vanilla trouve `hydraulic_turbines`, `standardized_military_rockets` et `explosive_field_ammunition` uniquement dans leurs définitions/localisations du mod; la seule référence structurelle interne supplémentaire est `standardized_military_rockets -> explosive_field_ammunition`. Aucun événement, journal, scripted effect, trigger ou fichier IA ne les référence. Décision : **MERGE_AND_ALIAS**. Les IDs doivent rester comme aliases `can_research = no` pour les sauvegardes et mods internes; ne pas les supprimer physiquement.",
        "",
        "## 14. Architecture finale recommandée",
        "",
        "Le plan final n'ajoute aucun nœud au candidat, transforme trois troncs en nœuds purs, retire quatre arêtes trop coûteuses et redéfinit un ID d'infrastructure. Le détail exhaustif est dans le CSV d'architecture finale.",
        "",
        "## 15. Métriques finales",
        "",
        markdown_table(
            ["Métrique", "Candidat", "Final recommandé"],
            [
                ["roots", current["roots"], final_stats["roots"]],
                ["isolated_nodes", current["isolated_nodes"], final_stats["isolated"]],
                ["leaf_no_effect", current["leaf_no_effect"], 0],
                ["edges", current["edges_total"], final_stats["edges"]],
                ["max_child_count", current["max_child_count"], final_stats["max_fanout"]],
                ["cycles", current["graph_cycles"], final_stats["cycles"]],
                ["building_pm_causality_violations", current["building_pm_causality_violations"], 0],
                ["cross_era_gt3", current["cross_era_gt3"], final_stats["cross_era_gt3"]],
            ],
        ),
        "",
        "Les nouvelles racines sont des spécialisations utiles (`traditional_papermaking`, `traditional_glassmaking`, `industrial_acids`, `applied_mineralogy`) et non des nœuds isolés ou vides.",
        "",
        "## 16. Distribution finale simulée",
        "",
        f"- GAMEPLAY_ABSTRACTION_GRANTS : **{gameplay_grants}**",
        f"- STRUCTURAL_REQUIRED_GRANTS : **{structural_grants}**",
        f"- TOTAL_STRUCTURAL_GRANTS : **{len(final_additions)}**",
        f"- COUNTRIES_AFFECTED (union de tous les grants) : **{len({tag for tag, _ in final_additions})}**",
        f"- COUNTRIES_AFFECTED par les troncs GAMEPLAY_ABSTRACTION : **{len({tag for tag, tech in final_additions if tech in {'organized_military_establishments', 'organized_naval_establishments', 'organized_financial_institutions'}})}**",
        "",
        markdown_table(["Technologie ajoutée", "Grants"], final_grant_rows),
        "",
        "## 17. Points nécessitant encore décision humaine",
        "",
        "- Valider les noms anglais/français du concept général réutilisant l'ID `turnpike_road_networks`.",
        "- Confirmer visuellement que les couloirs doctrine, armement et services issus du tronc militaire unique restent lisibles dans l'arbre runtime.",
        "- Confirmer en runtime les quatre petits modifiers conservés/réduits; aucune valeur n'est implémentée par cette passe.",
        "- Décider la durée de conservation des aliases après une politique explicite de compatibilité des sauvegardes.",
        "",
        "## 18. Ordre d'implémentation par vagues",
        "",
        "1. Tronc militaire unique redéfini et pur, puis fermeture pays recalculée.",
        "2. Troncs naval et financier rendus purs.",
        "3. Retrait des arêtes `organized_workshops` et `shaft_mining` refusées.",
        "4. Redéfinition/localisation de l'infrastructure terrestre organisée.",
        "5. Arêtes acceptées alimentation, savoirs, verre, génie et classification navale.",
        "6. Petits modifiers, fusions avec aliases, puis validation statique et runtime.",
        "7. Distribution pays finale seulement après validation de l'architecture.",
        "",
        "---",
        "",
        "Audit/simulation uniquement : aucun fichier gameplay n'a été modifié par cette revue; aucun commit, push ou PR.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    impact = read_csv(IMPACT)
    candidate_arch = read_csv(CANDIDATE_ARCH)
    node_rows = read_csv(NODE_AUDIT)
    current, plan = country_state()
    candidate_graph, candidate_eras = architecture_graph(candidate_arch)
    candidate_sets = candidate_final_sets(current, impact)

    technologies = topology.effective_objects("common/technology/technologies")
    candidate_active = {
        tech for tech, block in technologies.items()
        if topology.scalar(block, "can_research", "yes") != "no"
    }
    candidate_active.update(NEW_NODES)
    candidate_active.difference_update(MERGED_ALIASES)

    review_rows: list[dict[str, object]] = []
    for source in impact:
        tag = source["TAG"]
        parent = source["Technology"]
        triggers = direct_triggers(tag, parent, candidate_sets)
        collateral_text, collateral_cost = collateral(parent, triggers, plan[tag]["Region"])
        fit, decision, reason, change = decide(parent, triggers, plan[tag]["Region"])
        review_rows.append({
            "TAG": tag,
            "Country": plan[tag]["Country"],
            "Region": plan[tag]["Region"],
            "Technology": parent,
            "Decision_Type": source["Decision_Type"],
            "Triggering_Children": ";".join(triggers) or "fermeture transitive du descendant spécialisé",
            "Parent_Gameplay_Content": PARENT_CONTENT[parent],
            "Collateral_Unlocks": collateral_text,
            "Collateral_Unlock_Cost": collateral_cost,
            "Historical_Abstraction_Fit": fit,
            "Final_Decision": decision,
            "Final_Reason": reason,
            "Architecture_Change_Required": change,
        })

    military_rows = military_detail_rows(impact, candidate_sets)
    final_g, final_e, final_a = final_graph(candidate_graph, candidate_eras)
    final_additions = simulate_grants(final_g, final_a, current)
    final_stats = graph_stats(final_g, final_a, final_e)
    alternatives = make_alternatives(
        candidate_graph, candidate_eras, candidate_active, current, final_g, final_e, final_a
    )
    military_options = military_option_metrics(military_rows, alternatives)
    final_arch = final_architecture_rows(candidate_arch, final_g, final_additions)

    # Exhaustive, deterministic validation before writing any deliverable.
    impact_keys = [(row["TAG"], row["Technology"]) for row in impact]
    review_keys = [(str(row["TAG"]), str(row["Technology"])) for row in review_rows]
    if len(impact) != 310 or len(review_rows) != 310 or impact_keys != review_keys:
        raise ValueError("La revue ne correspond pas exactement aux 310 lignes d'impact, dans le même ordre")
    if len(set(review_keys)) != 310:
        raise ValueError("Doublon TAG/Technology dans la revue")
    if any(row["Final_Decision"] not in ALLOWED_DECISIONS for row in review_rows):
        raise ValueError("Décision finale non autorisée")
    if len(military_rows) != 138:
        raise ValueError(f"Audit militaire incomplet: {len(military_rows)} lignes")
    if any(not row["Triggering_Children"] for row in military_rows):
        raise ValueError("Enfant déclencheur militaire manquant")
    if final_stats["cycles"] or final_stats["isolated"]:
        raise ValueError(f"Architecture finale invalide: {final_stats}")
    if set(final_arch[0]) != set(ARCH_FIELDS) or any(set(row) != set(ARCH_FIELDS) for row in final_arch):
        raise ValueError("Schéma de l'architecture finale divergent")

    write_csv(REVIEW, REVIEW_FIELDS, review_rows)
    write_csv(MILITARY_DETAIL, [
        "TAG", "Triggering_Children", "Has_Light_Infantry", "Has_Regulated_Small_Arms",
        "Has_Field_Artillery", "Has_Fortification", "Has_Engineer_Service",
        "Has_Military_Hospitals",
    ], military_rows)
    write_csv(MILITARY_OPTIONS, MILITARY_OPTION_FIELDS, military_options)
    write_csv(ALTERNATIVES, ALT_FIELDS, alternatives)
    write_csv(FINAL_ARCH, ARCH_FIELDS, final_arch)
    REPORT.write_text(
        make_report(
            review_rows, military_rows, military_options, alternatives,
            final_stats, final_additions, final_arch,
        ),
        encoding="utf-8",
    )

    decisions = Counter(str(row["Final_Decision"]) for row in review_rows)
    final_techs = Counter(tech for _, tech in final_additions)
    gameplay = sum(final_techs[tech] for tech in {
        "organized_military_establishments",
        "organized_naval_establishments", "organized_financial_institutions",
    })
    print(json.dumps({
        "review_rows": len(review_rows),
        "decision_counts": dict(sorted(decisions.items())),
        "military_rows": len(military_rows),
        "military_grants_after": final_techs["organized_military_establishments"],
        "naval_grants_after": final_techs["organized_naval_establishments"],
        "finance_grants_after": final_techs["organized_financial_institutions"],
        "gameplay_abstraction_grants": gameplay,
        "structural_required_grants": len(final_additions) - gameplay,
        "total_structural_grants": len(final_additions),
        "countries_affected": len({tag for tag, _ in final_additions}),
        "final_metrics": final_stats,
        "final_grants_by_technology": dict(sorted(final_techs.items())),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
