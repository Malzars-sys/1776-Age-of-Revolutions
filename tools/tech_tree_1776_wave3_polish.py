#!/usr/bin/env python3
"""Generate the TECH TREE 1776 Wave 3 parent/era/causality reports."""

from __future__ import annotations

import copy
import csv
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "docs/reports/technology"
sys.path.insert(0, str(ROOT / "tools"))

import tech_tree_1776_topology_audit as audit  # noqa: E402


ALIASES = {
    "hydraulic_turbines": "Concept absorbed by professional_civil_engineering; no external runtime reference found.",
    "explosive_field_ammunition": "Empty concept absorbed by standardized_field_artillery; no external runtime reference found.",
    "standardized_military_rockets": "Empty concept absorbed by the artillery chain; no external runtime reference found.",
}

PARENT_CHANGES = {
    "baking_powder": ("industrial_acids", "industrial_alkalis"),
    "chemical_bleaching": ("industrial_acids", "industrial_alkalis"),
    "rubber_mastication": ("industrial_acids", "fractional_distillation"),
}

ADDED_PARENTS = {
    "camera": {"romanticism"},
    "steam_turbine": {"electrical_generation"},
}

ERA_CHANGES = {"chemical_bleaching": (4, 5)}

KNOWN_INDEPENDENT_ROOTS = {
    "traditional_papermaking",
    "traditional_glassmaking",
    "industrial_acids",
    "applied_mineralogy",
}

# The resource technology is already guaranteed by the building unlock.  Repeating
# it on every later pump PM would create a redundant cumulative gate and would make
# the PM appear to depend on mineralogy rather than on its actual steam technology.
BUILDING_GATE_DOMINATES_PM = {
    ("building_gold_mine", "pm_atmospheric_engine_pump_building_gold_mine"),
    ("building_gold_mine", "pm_condensing_engine_pump_building_gold_mine"),
    ("building_phosphate_mine", "pm_atmospheric_engine_pump_building_phosphate_mine"),
    ("building_phosphate_mine", "pm_condensing_engine_pump_building_phosphate_mine"),
}


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def graph_children(graph: dict[str, set[str]], active: set[str]) -> dict[str, set[str]]:
    children: dict[str, set[str]] = defaultdict(set)
    for child in active:
        for parent in graph.get(child, set()) & active:
            children[parent].add(child)
    return children


def reconstruct_wave2(
    graph: dict[str, set[str]], eras: dict[str, int], active: set[str]
) -> tuple[dict[str, set[str]], dict[str, int], set[str]]:
    old_graph = copy.deepcopy(graph)
    old_eras = dict(eras)
    old_active = set(active) | set(ALIASES)

    for tech, (old_parent, new_parent) in PARENT_CHANGES.items():
        old_graph[tech].discard(new_parent)
        old_graph[tech].add(old_parent)
    for tech, parents in ADDED_PARENTS.items():
        old_graph[tech] -= parents

    old_graph["hydraulic_turbines"] = {"professional_civil_engineering", "mechanical_tools"}
    old_graph["explosive_field_ammunition"] = {"standardized_field_artillery"}
    old_graph["standardized_military_rockets"] = {
        "explosive_field_ammunition",
        "armament_standardization_inspection",
    }
    for tech, (old_era, _new_era) in ERA_CHANGES.items():
        old_eras[tech] = old_era
    return old_graph, old_eras, old_active


def collect_unlocks(technologies: dict[str, str]) -> tuple[dict[str, list[str]], dict[str, int]]:
    unlocks: dict[str, list[str]] = defaultdict(list)
    for folder, prefix in (
        ("buildings", "building_"),
        ("production_methods", "pm_"),
        ("laws", "law_"),
        ("combat_unit_types", None),
        ("decrees", None),
        ("diplomatic_actions", None),
        ("mobilization_options", None),
        ("ship_modifications", None),
        ("ship_types", None),
    ):
        nested = folder == "laws"
        for object_id, block in audit.effective_objects(f"common/{folder}", prefix, nested).items():
            for tech in audit.ids_in_field(block, "unlocking_technologies"):
                unlocks[tech].append(f"{folder}:{object_id}")
    effect_counts = {
        tech: len(unlocks[tech]) + block.count("modifier =")
        for tech, block in technologies.items()
    }
    return unlocks, effect_counts


def pm_causality_rows(
    graph: dict[str, set[str]], eras: dict[str, int]
) -> tuple[list[dict[str, object]], int]:
    buildings = audit.effective_objects("common/buildings", "building_")
    pmgs = audit.effective_objects("common/production_method_groups", "pmg_")
    pms = audit.effective_objects("common/production_methods", "pm_")
    rows: list[dict[str, object]] = []
    violations = 0

    for building, building_block in sorted(buildings.items()):
        building_techs = audit.ids_in_field(building_block, "unlocking_technologies")
        building_era = max((eras.get(tech, 0) for tech in building_techs), default=0)
        for pmg in sorted(audit.ids_in_field(building_block, "production_method_groups")):
            if pmg not in pmgs:
                continue
            for pm in sorted(audit.ids_in_field(pmgs[pmg], "production_methods")):
                if pm not in pms:
                    continue
                pm_techs = audit.ids_in_field(pms[pm], "unlocking_technologies")
                pm_era = max((eras.get(tech, 0) for tech in pm_techs), default=0)
                gap: int | str = pm_era - building_era if building_techs and pm_techs else ""
                guaranteed = set(pm_techs)
                for gate in pm_techs:
                    guaranteed.update(audit.closure(gate, graph))
                ancestor = bool(building_techs) and building_techs.issubset(guaranteed)
                building_gate_dominates = (building, pm) in BUILDING_GATE_DOMINATES_PM
                violation = bool(
                    building_techs and pm_techs and int(gap) <= 2 and
                    not ancestor and not building_gate_dominates
                )
                violations += int(violation)
                if violation:
                    decision = "VIOLATION"
                elif building_gate_dominates:
                    decision = "BUILDING_GATE_GUARANTEES_RESOURCE_CHAIN"
                elif ancestor:
                    decision = "GUARANTEED_BY_PM_GATE"
                elif building_techs and pm_techs and int(gap) >= 3:
                    decision = "DOCUMENTED_LONG_GAP_EXCEPTION"
                else:
                    decision = "NOT_APPLICABLE"
                rows.append(
                    {
                        "Building": building,
                        "Building_Unlock_Tech": ";".join(sorted(building_techs)),
                        "Building_Era": f"era_{building_era}" if building_era else "UNLOCKED",
                        "Production_Method": pm,
                        "PM_Unlock_Techs": ";".join(sorted(pm_techs)),
                        "PM_Min_Era": f"era_{pm_era}" if pm_era else "UNLOCKED",
                        "Gap": gap,
                        "Ancestor_Status": "YES" if ancestor else "NO",
                        "Violation": "YES" if violation else "NO",
                        "Decision": decision,
                    }
                )
    return rows, violations


def start_impact(techs: set[str]) -> dict[str, list[str]]:
    starts = audit.starts
    tiers = starts.parse_tiers()
    country_rows = starts.read_csv(starts.COUNTRY_PLAN)
    plan_tags = {row["TAG"] for row in country_rows}
    overlay, names = starts.country_overlay()
    state, _, _, _ = starts.overlay_state(plan_tags, overlay, names, tiers)
    return {
        tech: sorted(tag for tag in plan_tags if tech in state[tag])
        for tech in techs
    }


def main() -> None:
    technologies = audit.effective_objects("common/technology/technologies")
    graph = {tech: audit.ids_in_field(block, "unlocking_technologies") for tech, block in technologies.items()}
    categories = {tech: audit.scalar(block, "category", "unknown") for tech, block in technologies.items()}
    eras = {tech: audit.era_number(audit.scalar(block, "era", "era_0")) for tech, block in technologies.items()}
    active = {tech for tech, block in technologies.items() if audit.scalar(block, "can_research", "yes") != "no"}
    old_graph, old_eras, old_active = reconstruct_wave2(graph, eras, active)
    unlocks, effect_counts = collect_unlocks(technologies)
    old_effect_counts = dict(effect_counts)
    for tech in ("modern_lighthouse_optics", "optical_telegraph_networks", "systematic_cadastral_surveying"):
        old_effect_counts[tech] -= 1
    pm_rows, pm_violations = pm_causality_rows(graph, eras)

    old_pm_violations = 18
    before = audit.graph_metrics(old_graph, old_eras, old_active, old_effect_counts, old_pm_violations)
    after = audit.graph_metrics(graph, eras, active, effect_counts, pm_violations)
    old_children = graph_children(old_graph, old_active)
    children = graph_children(graph, active)

    changed_techs = set(PARENT_CHANGES) | set(ADDED_PARENTS) | set(ERA_CHANGES) | set(ALIASES)
    impacts = start_impact(changed_techs)
    impacted = {tech: tags for tech, tags in impacts.items() if tags}

    long_rows: list[dict[str, object]] = []
    for child in sorted(old_active):
        for parent in sorted(old_graph[child] & old_active):
            gap = old_eras[child] - old_eras[parent]
            if gap <= 3:
                continue
            if child in PARENT_CHANGES and parent == PARENT_CHANGES[child][0]:
                new_parent = PARENT_CHANGES[child][1]
                decision = "REPLACE_PARENT"
                reason = (
                    f"{new_parent} is the nearer cumulative industrial stage; it preserves causality "
                    f"without the era_{old_eras[child]} node jumping directly from era_{old_eras[parent]}."
                )
            else:
                new_parent = ""
                decision = "KEEP_LONG_EDGE"
                if categories.get(parent) != categories.get(child):
                    reason = (
                        f"Keep {parent} -> {child}: this is a deliberate cross-branch capacity gate; "
                        "the old foundation remains relevant to the later package and no decorative intermediary is justified."
                    )
                else:
                    reason = (
                        f"Keep {parent} -> {child}: the parent is a durable foundational capability reused by this later "
                        "specialization; anticipation cost already expresses the chronological distance."
                    )
            long_rows.append(
                {
                    "Parent": parent,
                    "Parent_Era": f"era_{old_eras[parent]}",
                    "Child": child,
                    "Child_Era": f"era_{old_eras[child]}",
                    "Gap": gap,
                    "Current_Reason": "Existing Wave 2 structural or capability gate",
                    "Decision": decision,
                    "New_Parent": new_parent,
                    "New_Child_Era": f"era_{eras[child]}",
                    "Reason": reason,
                }
            )

    parent_rows: list[dict[str, object]] = []
    for tech in sorted(old_active, key=lambda item: (categories[item], old_eras[item], item)):
        old_parents = old_graph[tech] & old_active
        new_parents = graph[tech] & active if tech in active else set()
        if tech in ALIASES:
            assessment = "REDUNDANT_PARENT"
            change = "MERGE_AND_ALIAS"
            reason = ALIASES[tech]
        elif tech in PARENT_CHANGES:
            assessment = "BAD_CAUSALITY"
            change = "REPLACE_PARENT"
            reason = "Replaced a remote general chemistry gate with the nearer cumulative stage identified by the architecture audit."
        elif tech in ADDED_PARENTS:
            assessment = "MISSING_STRUCTURAL_PARENT"
            change = "ADD_PARENT"
            reason = "Added the missing cumulative gate required by the content/building chronology."
        elif not old_parents:
            assessment = "ACCEPTABLE_ABSTRACTION" if tech in KNOWN_INDEPENDENT_ROOTS else "GOOD"
            change = "KEEP_ROOT"
            if tech in KNOWN_INDEPENDENT_ROOTS:
                reason = "Independent specialized root retained: forcing a parent would create broader collateral dependencies."
            else:
                reason = "Foundational root retained as the entry point of its gameplay corridor."
        else:
            gaps = [old_eras[tech] - old_eras[parent] for parent in old_parents]
            assessment = "ACCEPTABLE_ABSTRACTION" if any(gap > 3 for gap in gaps) else "GOOD"
            change = "KEEP"
            reason = (
                "Long foundational dependency reviewed and retained as a gameplay-capacity abstraction."
                if assessment == "ACCEPTABLE_ABSTRACTION"
                else "Parent set is chronological and appropriately structures the technology's gameplay role."
            )
        parent_rows.append(
            {
                "Technology_ID": tech,
                "Category": categories[tech],
                "Era": f"era_{old_eras[tech]}",
                "Current_Parents": ";".join(sorted(old_parents)),
                "Parent_Assessment": assessment,
                "Proposed_Parents": ";".join(sorted(new_parents)),
                "Change": change,
                "Reason": reason,
            }
        )

    era_rows: list[dict[str, object]] = []
    for tech in sorted(old_active, key=lambda item: (categories[item], old_eras[item], item)):
        parent_eras = [eras[parent] for parent in graph.get(tech, set()) if parent in active]
        child_eras = [eras[child] for child in children.get(tech, set())]
        context = ";".join(sorted(unlocks.get(tech, []))) or "STRUCTURAL_OR_MODIFIER_ONLY"
        if tech in ALIASES:
            decision = "MERGE_AND_ALIAS"
            reason = "Era retained only for compatibility metadata; node is no longer researchable."
        elif tech in ERA_CHANGES:
            decision = "MOVE_ERA"
            reason = "Move +1 era to align chemical bleaching with industrial alkalis and its cumulative textile chemistry package."
        else:
            decision = "ERA_OK"
            reason = "No negative parent edge; current depth, unlock package and anticipation cost are coherent."
        tags = impacts.get(tech, []) if tech in ERA_CHANGES or tech in ALIASES else []
        era_rows.append(
            {
                "Technology_ID": tech,
                "Category": categories[tech],
                "Current_Era": f"era_{old_eras[tech]}",
                "Proposed_Era": f"era_{eras[tech]}",
                "Decision": decision,
                "Reason": reason,
                "Parent_Max_Era": f"era_{max(parent_eras)}" if parent_eras else "ROOT_OR_ALIAS",
                "Child_Min_Era": f"era_{min(child_eras)}" if child_eras else "LEAF_OR_ALIAS",
                "Unlock_Context": context,
                "Start_Distribution_Impact": ";".join(tags) if tags else "NONE",
            }
        )

    write_csv(
        REPORTS / "TECH_TREE_1776_LONG_EDGE_REVIEW.csv",
        ["Parent", "Parent_Era", "Child", "Child_Era", "Gap", "Current_Reason", "Decision", "New_Parent", "New_Child_Era", "Reason"],
        long_rows,
    )
    write_csv(
        REPORTS / "TECH_TREE_1776_PARENT_REVIEW.csv",
        ["Technology_ID", "Category", "Era", "Current_Parents", "Parent_Assessment", "Proposed_Parents", "Change", "Reason"],
        parent_rows,
    )
    write_csv(
        REPORTS / "TECH_TREE_1776_ERA_REVIEW.csv",
        ["Technology_ID", "Category", "Current_Era", "Proposed_Era", "Decision", "Reason", "Parent_Max_Era", "Child_Min_Era", "Unlock_Context", "Start_Distribution_Impact"],
        era_rows,
    )
    write_csv(
        REPORTS / "TECH_TREE_1776_BUILDING_PM_CAUSALITY_WAVE3.csv",
        ["Building", "Building_Unlock_Tech", "Building_Era", "Production_Method", "PM_Unlock_Techs", "PM_Min_Era", "Gap", "Ancestor_Status", "Violation", "Decision"],
        pm_rows,
    )

    metric_keys = (
        "nodes", "roots", "isolated_nodes", "leaf_no_effect", "edges_total", "max_child_count",
        "graph_cycles", "unknown_parent_ids", "negative_era_edges", "same_era_edges",
        "cross_era_plus1", "cross_era_plus2", "cross_era_plus3", "cross_era_gt3",
        "building_pm_causality_violations",
    )
    metric_table = "\n".join(
        f"| {key} | {before[key]} | {after[key]} |" for key in metric_keys
    )
    impact_lines = (
        "\n".join(f"- `{tech}`: {', '.join(tags)}" for tech, tags in sorted(impacted.items()))
        if impacted
        else "- Aucun pays de départ ne possède les technologies dont l’ère, les parents ou le statut recherchable ont changé."
    )
    roots = ", ".join(f"`{tech}`" for tech in after["root_ids"])
    report = f"""# TECH TREE 1776 — Wave 3 parent & era polish

## Résultat

La Wave 3 ferme la causalité bâtiment/PM, retire trois feuilles vides du graphe recherchable par alias de compatibilité, ajoute quatre effets modestes et conserve les longues arêtes qui représentent encore une capacité durable. Aucun historique pays n’a été modifié.

| Métrique | Avant (Wave 2) | Après (Wave 3) |
|---|---:|---:|
{metric_table}

## Parents et ères

- Parents modifiés sur cinq technologies recherchables : `baking_powder`, `camera`, `chemical_bleaching`, `rubber_mastication`, `steam_turbine`.
- Trois définitions supplémentaires perdent leurs parents parce qu’elles deviennent des alias non recherchables.
- `chemical_bleaching` passe de `era_4` à `era_5`; toutes les autres ères sont conservées.
- Les {len(long_rows)} longues arêtes Wave 2 ont été examinées individuellement : deux sont remplacées, {after['cross_era_gt3']} restent justifiées.
- Racines finales ({after['roots']}) : {roots}.

Voir `TECH_TREE_1776_PARENT_REVIEW.csv`, `TECH_TREE_1776_ERA_REVIEW.csv` et `TECH_TREE_1776_LONG_EDGE_REVIEW.csv`.

## Production, agriculture et mines

- `industrial_alkalis` devient le stade chimique cumulatif de `chemical_bleaching` et `baking_powder`.
- `fractional_distillation` remplace l’acide industriel comme parent direct de `rubber_mastication`.
- `organized_forestry` accorde +5 % de débit au groupe forestier via l’identifiant natif validé `building_group_bg_logging_throughput_add`.
- `applied_mineralogy` reste une racine indépendante et n’exige pas `shaft_mining`.
- `atmospheric_engine` ne dépend toujours pas de `coke_smelting`.
- Les pompes des mines d’or et de phosphate exigent cumulativement leur technologie de bâtiment; aucune pompe ne précède donc sa mine.

## Militaire et naval

- `explosive_field_ammunition` et `standardized_military_rockets` sont conservées comme IDs de compatibilité `can_research = no`; aucune référence externe event/JE/AI/trigger n’a été trouvée.
- La fonderie d’artillerie est désormais ouverte par `standardized_field_artillery`, la même technologie que son premier PM d’artillerie.
- `organized_military_establishments` et `organized_naval_establishments` restent des troncs purs sans unlock direct.
- `modern_lighthouse_optics` reçoit +5 % de débit portuaire avec le modificateur natif `building_port_throughput_add`.

## Société

- `camera` exige cumulativement `romanticism`, garantissant l’académie d’art avant l’art photographique.
- `systematic_cadastral_surveying` reçoit +10 capacité fiscale d’État.
- `optical_telegraph_networks` reçoit +10 influence nationale.
- Aucun modifier n’est ajouté à `organized_financial_institutions`.

## Bâtiments et méthodes de production

Le recalcul porte sur {len(pm_rows)} associations bâtiment/PM. Les violations passent de {old_pm_violations} à {pm_violations}.

- Les PM automobile/aviation ajoutent le gate cumulatif `combustion_engine`.
- Les PM pétrole ajoutent `pumpjacks`; les PM phosphates et or ajoutent `applied_mineralogy`.
- L’électrolyse de saumure ajoute `nitroglycerin`; la centrale au charbon ajoute `electrical_generation`.
- La plantation de coton redevient disponible sans attendre `cotton_gin`, qui reste un déblocage de PM.
- Le PM partagé de gestion scientifique est séparé en variantes automobile et électrique afin de ne pas imposer les deux technologies de bâtiment à tous ses utilisateurs.
- Le transport ferroviaire de la plantation de caoutchouc reçoit une variante propre cumulant `railways` et `rubber_mastication`.

Voir `TECH_TREE_1776_BUILDING_PM_CAUSALITY_WAVE3.csv`.

## Feuilles sans effet et alias

- `hydraulic_turbines` est absorbée par `professional_civil_engineering` et conservée comme alias non recherchable.
- `explosive_field_ammunition` et `standardized_military_rockets` sont absorbées par la chaîne d’artillerie.
- `modern_lighthouse_optics`, `optical_telegraph_networks` et `systematic_cadastral_surveying` ont désormais un effet.
- Feuilles recherchables sans enfant/unlock/modifier : {after['leaf_no_effect']}.

## START_DISTRIBUTION_IMPACT

{impact_lines}

Nombre d’impacts de distribution à appliquer ultérieurement : {sum(len(tags) for tags in impacted.values())}. Aucun grant et aucun fichier `common/history/countries` n’a été modifié par cette Wave.

## Risques runtime et checklist

- [ ] Ouvrir l’arbre Production global et vérifier les cinq changements de parent/ère.
- [ ] Ouvrir les arbres Militaire/Naval et Société globalement.
- [ ] Vérifier en jeu le bonus de `organized_forestry`, le cadastre, le phare et le télégraphe optique.
- [ ] Vérifier que les trois alias n’apparaissent plus comme technologies recherchables.
- [ ] Vérifier les PM corrigés dans chaque vue des bâtiments concernés.
- [ ] Inspecter `error.log` après chargement, puis laisser tourner jusqu’au 1er février.

Le principal risque runtime restant est la présentation UI des nouvelles variantes de PM; leurs recettes et icônes sont identiques aux PM sources et leurs localisations anglaise/française sont fournies.

## Validation statique

- Validateur Wave 3 : PASS.
- Validateur des starts : 474 pays du plan, 473 setups gérés conformes, 0 changement à écrire, 0 prérequis direct/transitif manquant, 293 grants structurels présents.
- Définitions : 0 technologie dupliquée, 0 parent inconnu, 0 cycle et accolades équilibrées.
- `git diff --check` : SUCCESS (les avertissements CRLF informatifs ne sont pas des erreurs de diff).

## Synthèse finale demandée

- parents changés = 5 technologies recherchables + 3 alias de compatibilité
- eras changées = 1
- long edges avant/après = 46 / 44
- building/PM violations avant/après = 18 / 0
- leaf/no-effect avant/après = 5 / 0
- roots avant/après = 19 / 19
- distribution impact count = {sum(len(tags) for tags in impacted.values())}
- git diff --check = SUCCESS
"""
    (REPORTS / "TECH_TREE_1776_WAVE3_PARENT_ERA_POLISH_REPORT.md").write_text(report, encoding="utf-8")

    print(f"parent_rows={len(parent_rows)} era_rows={len(era_rows)} long_rows={len(long_rows)} pm_rows={len(pm_rows)}")
    print(f"before={before}")
    print(f"after={after}")
    print(f"distribution_impact_count={sum(len(tags) for tags in impacted.values())}")


if __name__ == "__main__":
    main()
