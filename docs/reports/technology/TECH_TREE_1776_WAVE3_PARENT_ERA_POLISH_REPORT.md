# TECH TREE 1776 — Wave 3 parent & era polish

## Résultat

La Wave 3 ferme la causalité bâtiment/PM, retire trois feuilles vides du graphe recherchable par alias de compatibilité, ajoute quatre effets modestes et conserve les longues arêtes qui représentent encore une capacité durable. Aucun historique pays n’a été modifié.

| Métrique | Avant (Wave 2) | Après (Wave 3) |
|---|---:|---:|
| nodes | 247 | 244 |
| roots | 19 | 19 |
| isolated_nodes | 0 | 0 |
| leaf_no_effect | 5 | 0 |
| edges_total | 343 | 340 |
| max_child_count | 8 | 7 |
| graph_cycles | 0 | 0 |
| unknown_parent_ids | 0 | 0 |
| negative_era_edges | 0 | 0 |
| same_era_edges | 38 | 39 |
| cross_era_plus1 | 121 | 120 |
| cross_era_plus2 | 88 | 87 |
| cross_era_plus3 | 50 | 50 |
| cross_era_gt3 | 46 | 44 |
| building_pm_causality_violations | 18 | 0 |

## Parents et ères

- Parents modifiés sur cinq technologies recherchables : `baking_powder`, `camera`, `chemical_bleaching`, `rubber_mastication`, `steam_turbine`.
- Trois définitions supplémentaires perdent leurs parents parce qu’elles deviennent des alias non recherchables.
- `chemical_bleaching` passe de `era_4` à `era_5`; toutes les autres ères sont conservées.
- Les 46 longues arêtes Wave 2 ont été examinées individuellement : deux sont remplacées, 44 restent justifiées.
- Racines finales (19) : `applied_mineralogy`, `codified_practical_knowledge`, `improved_husbandry`, `industrial_acids`, `institutionalized_scientific_exchange`, `international_relations`, `organized_financial_institutions`, `organized_military_establishments`, `organized_naval_establishments`, `organized_textile_production`, `organized_workshops`, `periodical_print_networks`, `shaft_mining`, `systematic_administrative_statistics`, `traditional_food_processing`, `traditional_glassmaking`, `traditional_papermaking`, `turnpike_road_networks`, `variolation_networks`.

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

Le recalcul porte sur 704 associations bâtiment/PM. Les violations passent de 18 à 0.

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
- Feuilles recherchables sans enfant/unlock/modifier : 0.

## START_DISTRIBUTION_IMPACT

- Aucun pays de départ ne possède les technologies dont l’ère, les parents ou le statut recherchable ont changé.

Nombre d’impacts de distribution à appliquer ultérieurement : 0. Aucun grant et aucun fichier `common/history/countries` n’a été modifié par cette Wave.

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
- distribution impact count = 0
- git diff --check = SUCCESS
