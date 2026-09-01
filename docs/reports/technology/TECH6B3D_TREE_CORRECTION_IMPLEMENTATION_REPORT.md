# TECH6B3D — Tree Correction Implementation

> Mise à jour documentaire TECH6B3E : la matrice d'implémentation conserve les 79 exigences TECH6B3A originales et ajoute 7 lignes `H01–H07` pour les changements humains réalisés après TECH6B3D. Le bloc terminal historique de 79 lignes reste un instantané de clôture, tandis que la matrice courante compte 86 lignes. Les nouveaux owners autoritatifs sont détaillés en section d'addendum ci-dessous; TECH6B3E n'effectue aucune écriture gameplay.

Résultat : **PASS**  
Branche : `tech6b3d-tree-correction-implementation`  
Vanilla canonique : Victoria 3 `1.13.11`, sous `C:/Games/Victoria 3/game`.

## A. Checkpoint

TECH6B3D part de l'état non committé TECH6B1–TECH6B3C, préservé sans reset, clean, restore global, stash ou checkout destructif.

Checkpoint gameplay avant TECH6B3D :

- 970 fichiers sous `common`, `events`, `map_data`, `gui` et `localization` ;
- agrégat SHA-256 déterministe : `23756b95cf9302718563622b61c17ce0a0756495deb918877b1a65b6035cedb5`.

Les cinq livrables autoritatifs TECH6B3A–C ont été lus intégralement avant modification. La matrice TECH6B3A contient 79 exigences, dont exactement 53 candidats mécaniques et 24 arbitrages humains.

## B. État Git

La branche `tech6b3d-tree-correction-implementation` a été créée depuis `tech6b3c-tree-human-review` avec l'état de travail courant intact. Aucun commit ni push n'a été effectué.

Les modifications antérieures TECH6B1–TECH6B3C restent mélangées dans le worktree non committé. L'attribution TECH6B3D repose donc sur une liste fermée de 28 chemins gameplay, enregistrée en section Z, et sur le checkpoint précédent.

## C. Décisions TECH6B3C figées

Les neuf recommandations MEDIUM `P34`, `P35`, `S03`, `S04`, `S07`, `S13`, `S14`, `S16` et `S19` sont acceptées. Les 24 arbitrages sont clos et `USER_DECISIONS_STILL_REQUIRED = 0`.

Une correction utilisateur postérieure s'impose toutefois au design béton :

- `steel_frame_buildings` appartient à la catégorie Society ;
- `reinforced_concrete` et `arc_welding` appartiennent à Production ;
- Victoria 3 n'autorise pas les parents technologiques entre catégories ;
- toute arête `reinforced_concrete -> steel_frame_buildings`, `steel_frame_buildings -> arc_welding` ou inverse équivalent est abandonnée ;
- le lien futur entre les branches passera par les gates et inputs des PM, jamais par une arête technologique inter-catégorie.

La matrice et le rapport TECH6B3C ont reçu cet addendum documentaire. Aucun changement béton n'a été appliqué.

## D. Inventaire des candidats TECH6B3A

La matrice TECH6B3D contient une ligne pour chacune des 79 exigences.

| Périmètre | IMPLEMENTED | ALREADY_CORRECT | SUPERSEDED | DEFERRED_CONCRETE | BLOCKED | Total |
|---|---:|---:|---:|---:|---:|---:|
| 53 candidats mécaniques | 47 | 2 | 3 | 1 | 0 | 53 |
| 24 arbitrages humains clos | 14 | 5 | 2 | 3 | 0 | 24 |
| 2 anciens audits corrects | 0 | 2 | 0 | 0 | 0 | 2 |
| matrice complète | 61 | 9 | 5 | 4 | 0 | 79 |

## E. Candidats implémentés

Les 47 candidats mécaniques implémentés sont :

- Production : `P02–P05`, `P08–P16`, `P18–P27`, `P29`, `P30`, `P36–P40` ;
- Military : `M01–M05`, `M07`, `M08` ;
- Society : `S02`, `S08`, `S09`, `S11`, `S23–S26`, `S28`, `S30`.

Les décisions humaines donnant une écriture gameplay sont `P01`, `M06`, `S01`, `S03`, `S04`, `S05`, `S07`, `S10`, `S13`, `S14`, `S19`, `S20`, `S21` et `S27`.

## F. Candidats superseded

Dans la baseline mécanique :

- `P32` : superseded par la contrainte de catégorie ; aucune arête impliquant Steel-Frame et Production ;
- `S12` : Analytical Philosophy Department reste gaté par `analytical_philosophy` ;
- `S18` : Active Principle Pharmacy reste parallèle à Clinicopathological Medicine.

Dans les arbitrages humains :

- `P06` : aucune nouvelle technologie Electric Sewing ;
- `P07` : `pm_electric_sewing_machines` reste gaté par `electrical_capacitors`.

## G. Candidats béton différés

- `P31` : aucune arête n'est ajoutée pendant TECH6B3D. Une éventuelle relation Production-only `reinforced_concrete -> arc_welding` devra être examinée avec la livraison béton ;
- `P33` : renommage Steel-Frame différé ;
- `P34` : 30 Concrete et Glass 20 différés ;
- `P35` : 40 Concrete et Glass 20 sur `pm_arc_welded_buildings` différés.

P34 et P35 restent `ACCEPTED_DEFERRED_CONCRETE_IMPLEMENTATION`. Leur acceptation ne vaut pas autorisation d'implémenter le bien ou sa chaîne.

## H. Corrections Production

- le `+10` d'économie d'échelle quitte l'alias caché `mechanized_workshops` et passe à `interchangeable_manufacture` ;
- `mechanical_tools` reçoit `puddling_and_rolling` en plus de `precision_boring` ;
- `pm_gas_streetlights` reçoit le gate `coal_gasification` ;
- `pm_dye_workshops` passe à `mechanized_spinning` ;
- `pm_sewing_machines` passe au véritable ID `advanced_spinning` ;
- les six fermes/ranchs organisés passent d'Enclosure à `improved_husbandry` ;
- la plantation de coton passe à `cotton_gin` ;
- les treize compagnies P15–P27 exigent `cotton_gin` dans leur bloc `possible`; `company_dmc` était déjà correcte ;
- les conditions `ai_will_do` distinctes ont été préservées ;
- `traditional_papermaking` reçoit `organized_forestry` ;
- `pm_market_squares` passe à `turnpike_road_networks` ;
- les cinq pompes à condensation conservent seulement `condensing_steam_engines`.

`cotton_gin` reste en `era_4` avec `mechanized_spinning` comme parent. Aucun ID `industrial_spinning` ne subsiste dans le gameplay.

## I. Corrections Military

- `scientific_naval_architecture` passe en `era_2` ;
- `marine_chronometry` reçoit ce nœud comme parent ;
- First Aid passe de `triage` à `permanent_military_hospitals` ;
- `percussion_cap` passe en `era_5` ;
- `general_staff` reçoit `percussion_cap` en conservant ses trois parents ;
- `pm_percussion_caps` reçoit le gate exact `percussion_cap` ;
- `pm_explosive_shells` reste gaté par `dynamite` ;
- le second PM de fortification navale passe à `casemated_fortifications` ;
- `concrete_fortifications` reçoit `casemated_fortifications` en conservant `defense_in_depth`.

Les lignes M04/M05 de TECH6B3A désignaient par erreur le fichier `90_...compatibility.txt`; les objets réels se trouvent dans `common/technology/technologies/20_tech3a_military.txt`, chemin utilisé par le patch.

## J. Corrections Society

- `political_economy` reçoit `commercial_insurance_markets` ;
- l'université passe à `specialized_technical_academies` ;
- Philosophy Department passe à `polytechnical_education` ;
- les responsabilités commerciales mûres passent à `classical_political_economy` ;
- les lois économiques et religieuses reçoivent leurs gates figés ;
- diffusion et plafond d'innovation reçoivent leurs valeurs initiales ;
- les topologies abolitionniste, médicale, policière et financière sont appliquées.

## K. Nouveau PM Professional Faculties

ID canonique choisi selon les conventions voisines : `pm_professional_faculties`.

```text
PROFESSIONAL_FACULTIES_ID = pm_professional_faculties
PROFESSIONAL_FACULTIES_FILE = common/production_methods/07_government.txt
PROFESSIONAL_FACULTIES_GROUP_FILE = common/production_method_groups/07_government.txt
PROFESSIONAL_FACULTIES_GATE = specialized_professional_societies
PROFESSIONAL_FACULTIES_INNOVATION = 1.75
```

Le PM est inséré dans `pmg_base_building_university` entre Philosophy et Analytical. Aucun nouveau groupe n'est créé.

Interpolation économique et d'emploi :

| Palier | Papier | Outils | Coût indicatif | Innovation | Clerks/Laborers/Academics | Qualifications |
|---|---:|---:|---:|---:|---|---:|
| Philosophy | 10 | 0 | 300 | 1.5 | 250/250/0 | 0.15 |
| Professional Faculties | 11 | 1 | 370 | 1.75 | 225/225/50 | 0.175 |
| Analytical | 15 | 0 | 450 | 2.0 | 200/200/100 | 0.20 |

Le coût indicatif utilise les prix de référence déjà commentés dans les scripts : Paper 30 et Tools 40. Professional Faculties coûte donc davantage que Philosophy tout en restant sous Analytical. La texture de Philosophy est réutilisée ; aucune ressource graphique nouvelle n'est créée. Les localisations anglaise et française sont ajoutées aux fichiers TECH3A existants, avec BOM UTF-8 conservé.

## L. Human Rights / Abolition

La chaîne effective est :

```text
constitutional_government
  -> human_rights
  -> organized_reform_movements
  -> abolitionist_mobilization
  -> law_slavery_banned
```

L'arête directe redondante `human_rights -> abolitionist_mobilization` est supprimée. Le nouveau shadow `common/laws/02_slavery.txt` part exactement de vanilla 1.13.11 et ajoute uniquement `abolitionist_mobilization` au bloc `unlocking_technologies` de `law_slavery_banned`. Aucune loi esclavagiste régressive ne reçoit de gate.

## M. Topologie médicale

```text
variolation_networks ─┐
                     ├─> vaccination ───────────────┐
medical_degrees ─────┘                              ├─> organized_immunization_campaigns
medical_degrees ─┬─> clinicopathological_medicine   │
                 └─> active_principle_pharmacy ─────┘
```

`experimental_research_laboratories` reste parent de Clinicopathological Medicine et Active Principle Pharmacy. Aucun lien Clinicopathology → Pharmacy n'est ajouté.

Le libellé `clinicopathological_analysis` du prompt est conceptuel ; l'ID gameplay exact et existant est `clinicopathological_medicine`. Aucun faux ID n'est utilisé.

## N. Topologie policière

```text
professional_civil_policing ─┐
central_statistical_offices ─┴─> identification_documents
                                 -> central_planning
                                 -> mass_surveillance
```

Les deux parents d'Identification Documents sont présents. Aucun parent direct redondant n'est ajouté à Central Planning ou Mass Surveillance.

## O. Finance / Joint Stock

`joint_stock_companies` est maintenant recherchable en `era_6`, sans `can_research = no`.

```text
postal_savings ───────────────┐
commercial_insurance_markets ─┴─> joint_stock_companies
institutionalized_public_credit ─┐
joint_stock_companies ────────────┴─> mutual_funds
stock_exchange ──────────────────┐
mutual_funds ────────────────────┴─> investment_banks
```

Stock Exchange conserve +1 compagnie et +1 charte ; Joint Stock reçoit +1 de chaque. Investment Banks conserve ses deux parents directs et hérite de Joint Stock via Mutual Funds.

## P. Tech spread

`institutionalized_scientific_exchange` reçoit exactement :

```text
country_tech_spread_mult = 0.05
```

```text
TECH_SPREAD_INITIAL_BALANCE_VALUE = 0.05
TECH_SPREAD_REBALANCE_REQUIRED = YES
```

Aucun define n'est modifié et aucune variante +10 % n'est appliquée.

## Q. Innovation

`experimental_research_laboratories` reçoit exactement :

```text
country_weekly_innovation_max_add = 5
```

```text
INNOVATION_MAX_INITIAL_BALANCE_VALUE = 5
INNOVATION_REBALANCE_REQUIRED = YES
```

Aucune variante +10 n'est appliquée.

## R. Gates de lois et responsabilités commerciales

| Objet | Gate final |
|---|---|
| `law_laissez_faire` | `joint_stock_companies` |
| `law_interventionism` | `classical_political_economy` |
| `law_total_separation` | `liberal_constitutionalism` |
| `law_freedom_of_conscience` | `institutionalized_scientific_exchange` |
| `law_slavery_banned` | `abolitionist_mobilization` |
| `law_free_trade` | `classical_political_economy` |
| `no_tariffs` | `classical_political_economy` |
| `no_subventions` | `classical_political_economy` |

Mercantilism, Navigation Acts, embargo, Goods Transfer, Prohibit Trade with Global Market et `je_liberalism` restent associés à `commercial_insurance_markets`.

## S. Contrôle des IDs

Résultats de l'overlay actif fork/vanilla :

- technologies actives du replace-path : 285 ; doublons : 0 ;
- PM actifs : 451 ; doublons : 0 ;
- groupes de PM actifs : 207 ; doublons : 0 ;
- références PM inconnues depuis les groupes : 0 ;
- lois actives : 140 ; doublons : 0 ;
- bâtiments actifs : 120 ; doublons : 0 ;
- `pm_professional_faculties` : exactement une définition et une référence dans le groupe universitaire ;
- `industrial_spinning` dans le gameplay : 0 occurrence.

```text
NEW_TECH_IDS = 0
NEW_PM_IDS = 1
NEW_BUILDING_IDS = 0
NEW_GOOD_IDS = 0
NEW_LAW_IDS = 0
UNKNOWN_TECH_IDS = 0
UNKNOWN_PM_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0
```

## T. Contrôle de topologie

L'audit statique a parsé les 285 technologies actives, leurs catégories et tous leurs parents.

```text
DUPLICATE_TECH_IDS = 0
TECH_TREE_CYCLES = 0
SELF_PARENTS = 0
UNKNOWN_TECH_PREREQUISITES = 0
CROSS_CATEGORY_TECH_EDGES = 0
RESEARCHABLE_TECHS_WITH_ONLY_INACCESSIBLE_PARENTS = 0
```

Steel-Frame reste Society avec `investment_banks` et `modern_sewerage`. Arc Welding reste Production avec `electric_arc_process`. Aucun des deux n'est parent de l'autre.

## U. Contrôle béton hors scope

Une recherche finale ne trouve aucun ID de bien Concrete, Cement Works, PM de production Concrete ou `goods_input_concrete`.

```text
CONCRETE_DESIGN_ACCEPTED = YES
CONCRETE_DESIGN_CATEGORY_SAFE = YES
STEEL_FRAME_CROSS_CATEGORY_PLAN_ABANDONED = YES
CONCRETE_IMPLEMENTATION_DEFERRED = YES
CONCRETE_GOOD_CREATED = NO
CEMENT_WORKS_CREATED = NO
CONCRETE_PRODUCTION_PM_CREATED = NO
CONCRETE_CONSUMPTION_IMPLEMENTED = NO
```

La technologie militaire existante `concrete_fortifications` et son nouveau parent ne constituent pas l'implémentation du bien Concrete.

## V. Contrôle Steam / Starting Technologies

Aucune écriture n'a eu lieu dans un Workshop ou dans le miroir local.

- mod principal Workshop `3617930953` : 909 fichiers, hash `d7a89af3f1943148740ef12dbf14531dac292647abc9720b5f141e955c7a1d78` ;
- miroir local : 909 fichiers, même hash ;
- build Steam du fork `3780935876` : 889 fichiers, hash `e01c5d187e8c7198678dbaab40f2c8c2ff079d7a396d4749872d338b07a272cd`.

Les six fichiers Starting Technologies n'apparaissent pas dans le status ciblé et n'ont pas été touchés.

```text
STEAM_FORWARD_PORT_CHANGES = 0
STARTING_TECH_CHANGES = 0
```

## W. Validation statique

- 83 contrôles objet-scopés : 83 PASS, 0 FAIL ;
- accolades, profondeur négative et parité des guillemets : PASS sur les 28 chemins ;
- gates, topologies et modificateurs exacts : PASS ;
- overlays et doublons : PASS ;
- BOM des deux localisations : `EF-BB-BF` ;
- matrice : 79 lignes, aucun ID manquant ou dupliqué ;
- `git diff --check` : aucune erreur, seulement les avertissements LF/CRLF de la configuration Windows.

`STATIC_VALIDATION = PASS`.

## X. Runtime

Un smoke de 30 secondes a été lancé directement avec `victoria3.exe -debug_mode -mod=".../descriptor.mod"`, sans instance Victoria 3 préalable. Le journal `error.log` a été régénéré pendant le test. Le seul processus créé par le smoke a ensuite été arrêté.

Résultat du filtrage du journal frais :

- erreur parser/technologie/PM ciblée : 0 ;
- occurrence de `pm_professional_faculties` ou d'un chemin TECH6B3D dans une erreur : 0 ;
- les diagnostics présents sont des messages de localisation/DLC préexistants, non liés au patch.

```text
PARSER_LOG_SMOKE = PASS
RUNTIME = NOT_CLAIMED
```

Le menu, le setup 1776, une nouvelle partie et le passage d'un mois n'ont pas été observés ; aucun runtime complet n'est revendiqué.

## Y. Anomalies / blockers

Aucun blocker ne reste.

Anomalies documentaires résolues :

1. `steel_frame_buildings` est Society : la topologie béton TECH6B3C a été corrigée et les arêtes inter-catégories abandonnées ;
2. `industrial_spinning` était un faux ID dérivé d'un libellé : `advanced_spinning` est utilisé ;
3. M04/M05 pointaient vers le mauvais fichier dans TECH6B3A : le fichier réel `20_tech3a_military.txt` est utilisé ;
4. `clinicopathological_analysis` n'est pas l'ID du nœud : l'objet existant est `clinicopathological_medicine`.

Les valeurs +5 % de diffusion, +5 de plafond d'innovation et les valeurs du nouveau PM restent des baselines à rééquilibrer ultérieurement.

## Z. Diff final

Chemins gameplay attribuables à TECH6B3D : 28.

### Nouveaux shadows vanilla 1.13.11

1. `common/buildings/02_agro.txt`
2. `common/buildings/04_plantations.txt`
3. `common/laws/02_slavery.txt`
4. `common/mobilization_options/00_mobilization_option.txt`
5. `common/production_method_groups/07_government.txt`

### Fichiers existants modifiés

6. `common/buildings/07_government.txt`
7. `common/company_types/00_companies_africa.txt`
8. `common/company_types/00_companies_asia.txt`
9. `common/company_types/00_companies_russia.txt`
10. `common/company_types/00_companies_soi.txt`
11. `common/company_types/99_basic_companies.txt`
12. `common/laws/00_church_and_state.txt`
13. `common/laws/01_economic_system.txt`
14. `common/laws/01_trade_policy.txt`
15. `common/production_methods/01_industry.txt`
16. `common/production_methods/03_mines.txt`
17. `common/production_methods/05_military.txt`
18. `common/production_methods/06_urban_center.txt`
19. `common/production_methods/07_government.txt`
20. `common/technology/technologies/10_tech3a_production.txt`
21. `common/technology/technologies/20_tech3a_military.txt`
22. `common/technology/technologies/25_tech3a_naval.txt`
23. `common/technology/technologies/30_tech3a_society.txt`
24. `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`
25. `common/treaty_articles/21_no_tariffs.txt`
26. `common/treaty_articles/26_no_subventions.txt`
27. `localization/english/tech3a_technology_l_english.yml`
28. `localization/french/tech3a_technology_l_french.yml`

Après TECH6B3D, le périmètre gameplay contient 975 fichiers et l'agrégat `a73d7000d11f221196c882a53dd2a43d4626f6524214ac21bfa4c014fd92c8ef`. L'augmentation de cinq fichiers correspond exactement aux cinq nouveaux shadows.

Livrables documentaires :

- `docs/reports/technology/TECH6B3D_TREE_CORRECTION_IMPLEMENTATION_MATRIX.csv` ;
- `docs/reports/technology/TECH6B3D_TREE_CORRECTION_IMPLEMENTATION_REPORT.md` ;
- addendum de contrainte moteur dans les deux livrables TECH6B3C.

## Sortie terminale

```text
TECH6B3D_TREE_CORRECTION_IMPLEMENTATION = PASS
BRANCH = tech6b3d-tree-correction-implementation
TECH6B3A_IMPLEMENTATION_CANDIDATES_BASELINE = 53
IMPLEMENTED = 47
ALREADY_CORRECT = 2
SUPERSEDED_BY_TECH6B3C = 3
DEFERRED_CONCRETE = 1
BLOCKED = 0
TECH6B3C_HUMAN_DECISIONS_TOTAL = 24
TECH6B3C_HUMAN_DECISIONS_ACCEPTED = 24
USER_DECISIONS_STILL_REQUIRED = 0
P01_SCALE_BONUS_OWNER = interchangeable_manufacture
ELECTRIC_SEWING_NEW_TECH_CREATED = NO
ELECTRIC_SEWING_GATE = electrical_capacitors
PERCUSSION_CAPS_GATE = percussion_cap
LAISSEZ_FAIRE_GATE = joint_stock_companies
INTERVENTIONISM_GATE = classical_political_economy
TOTAL_SEPARATION_GATE = liberal_constitutionalism
SLAVERY_BANNED_GATE = abolitionist_mobilization
JOINT_STOCK_COMPANIES_RESEARCHABLE = YES
JOINT_STOCK_COMPANIES_ERA = 6
TECH_SPREAD_BONUS = 0.05
TECH_SPREAD_REBALANCE_REQUIRED = YES
INNOVATION_MAX_BONUS = 5
INNOVATION_REBALANCE_REQUIRED = YES
PROFESSIONAL_FACULTIES_CREATED = YES
PROFESSIONAL_FACULTIES_ID = pm_professional_faculties
PROFESSIONAL_FACULTIES_GATE = specialized_professional_societies
PROFESSIONAL_FACULTIES_INNOVATION = 1.75
MEDICAL_TOPOLOGY = PASS
POLICING_TOPOLOGY = PASS
FINANCIAL_TOPOLOGY = PASS
ABOLITION_TOPOLOGY = PASS
TECH_TREE_CYCLES = 0
UNKNOWN_TECH_PREREQUISITES = 0
CROSS_CATEGORY_TECH_EDGES = 0
CONCRETE_DESIGN_ACCEPTED = YES
CONCRETE_IMPLEMENTATION_DEFERRED = YES
CONCRETE_GOOD_CREATED = NO
CEMENT_WORKS_CREATED = NO
CONCRETE_PRODUCTION_PM_CREATED = NO
CONCRETE_CONSUMPTION_IMPLEMENTED = NO
NEW_TECH_IDS = 0
NEW_PM_IDS = 1
NEW_BUILDING_IDS = 0
NEW_GOOD_IDS = 0
NEW_LAW_IDS = 0
UNKNOWN_TECH_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0
STEAM_FORWARD_PORT_CHANGES = 0
STARTING_TECH_CHANGES = 0
GAMEPLAY_FILES_CHANGED_BY_TECH6B3D = 28
STATIC_VALIDATION = PASS
PARSER_LOG_SMOKE = PASS
RUNTIME = NOT_CLAIMED
COMMIT = NO
PUSH = NO
MATRIX = docs/reports/technology/TECH6B3D_TREE_CORRECTION_IMPLEMENTATION_MATRIX.csv
REPORT = docs/reports/technology/TECH6B3D_TREE_CORRECTION_IMPLEMENTATION_REPORT.md
NEXT_PHASE_READY = YES
```

## Addendum post-validation — affichage de la branche financière

Après constat en jeu, `gui/tech_tree.gui` a reçu un correctif ciblé :

- `stock_exchange` contourne explicitement un rejet éventuel de `Technology.ShouldShow` et sa carte reste affichable ;
- `joint_stock_companies`, désormais recherchable, contourne l'ancien filtre des alias consommés pour sa carte et ses lignes ;
- les autres alias consommés restent masqués ;
- les expressions GUI sont équilibrées et un nouveau smoke test de 30 secondes ne relève aucune erreur ciblée.

Ce suivi ajoute `gui/tech_tree.gui` aux 28 chemins gameplay de la livraison initiale, soit 29 chemins après correctif. La matrice autoritative de 79 exigences reste inchangée.

## Addendum TECH6B3E — décisions humaines autoritatives

La phrase précédente décrit l'état immédiatement après le correctif GUI. La matrice a depuis été réconciliée : elle conserve les 79 exigences initiales et ajoute les sept familles `H01–H07` suivantes.

| ID | Objet | État autoritatif courant |
|---|---|---|
| H01 | `law_protectionism` | `political_economy` |
| H02 | `law_public_health_insurance` | `organized_immunization_campaigns` |
| H03 | droits, travail et aide sociale | `human_rights` : travail des enfants restreint, organismes réglementaires, subventions salariales ; `labor_movement` : école primaire obligatoire, protection des travailleurs, pension de vieillesse |
| H04 | `law_state_atheism` | `socialism` |
| H05 | `law_terakoya` | aucun `unlocking_technologies` |
| H06 | lois d'esclavage | commerce : aucun gate ; dette : `constitutional_government` ; colonial : `human_rights` ; héritage : `organized_reform_movements` ; abolition : `abolitionist_mobilization` |
| H07 | GUI financier | `stock_exchange` explicitement affichable ; `joint_stock_companies` recherchable et exempté du filtre des alias pour sa carte et ses arêtes |

Ces changements sont déjà présents dans l'état gameplay fourni à TECH6B3E. Ils ne sont pas réappliqués par l'audit.
