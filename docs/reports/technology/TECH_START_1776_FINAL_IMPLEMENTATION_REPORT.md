# TECH START 1776 — Rapport final d’implémentation

Date cible : 1776-01-01  
Version cible : Victoria 3 1.13.11  
Branche locale : `tech6c-goods-buildings-pm-implementation`

## 1. Fichiers modifiés

- Arbre : `10_tech3a_production.txt`, `20_tech3a_military.txt`, `25_tech3a_naval.txt`, `30_tech3a_society.txt`, `90_tech3a_vanilla_post1836_compatibility.txt`.
- Bâtiments : `01_industry.txt`, `06_urban_center.txt` et nouvel override ciblé `99_tech_start_1776_construction_sector.txt`.
- PM et paliers : `02_agro.txt`, `00_starting_inventions.txt`.
- Localisation : fichiers technologiques anglais et français.
- Pays : 411 fichiers de setup effectif réécrits pour représenter la cible exacte des 471 TAG recherchés.
- Outils et rapports : validateur final, sanity cases et distribution finale.

Les changements préexistants TECH6D, TECH7A et runtime n’ont pas été modifiés par cette implémentation.

## 2. Relations d’arbre

Les 26 résolutions canoniques ont été appliquées : 24 `REMOVE_EDGE`, 1 `REPLACE_EDGE` et 1 `REDEFINE_TECH`. Le contrôle exact du CSV ne trouve aucune arête signalée encore présente. Le graphe final contient 0 cycle et 0 prérequis inconnu.

## 3. `organized_workshops`

`traditional_furniture_making` est remplacée par `organized_workshops`, en `era_1`, sans parent. Elle ouvre la manufacture de meubles et l’atelier d’outils. `precision_boring` dépend désormais de `coke_smelting`, `atmospheric_engine` et `organized_workshops`. `coke_smelting` continue de gater l’aciérie, mais plus l’atelier d’outils.

## 4. Migration de `traditional_furniture_making`

La migration pays a été faite 1:1 vers `organized_workshops`. Le scan du mod et des références vanilla chargées ne trouve plus aucune référence résiduelle à l’ancien ID. Distribution finale : 217 TAG.

## 5. Nettoyage atomique de `urbanization`

- Gate retiré du centre urbain.
- Gate vanilla du secteur de construction neutralisé par un override local ciblé.
- Arêtes vers `tech_bureaucracy` et `urban_planning` retirées.
- 267 grants pays et 4 grants de paliers retirés.
- Alias conservé avec `can_research = no`, sans parent, enfant, unlock ni modifier actif.
- Aucun trigger actif `has_technology = urbanization` ou `technology = urbanization` détecté.

## 6. Chimie

`building_chemical_works` reste sur `industrial_acids`. `building_chemical_plant` passe sur `improved_fertilizer` et `building_explosives_factory` sur `nitroglycerin`. Aucun nouveau nœud technologique n’a été créé.

## 7. Sucre

`pm_sugar_beets` passe de `sugar_refining` à `improved_fertilizer`. `pm_sweeteners` reste sur `sugar_refining`. Les PM vide, vapeur et centrifuge conservent leurs doubles verrous technologiques.

## 8. Classifications et définitions

Les décisions documentaires A/B/C ont été appliquées uniquement là où elles ont une traduction réelle : arbre, unlocks, distribution et localisation. Aucun champ Clausewitz artificiel n’a été ajouté et les eras n’ont pas été déplacées sans décision explicite. Les textes EN/FR de `organized_workshops`, `industrial_canals`, `advanced_spinning` et des nœuds institutionnels concernés ont été révisés.

## 9. ADD pays

Le plan déterministe contient 1 915 lignes `COUNTRY_TECH_ADD`, toutes prises en compte.

## 10. REMOVE pays

Le plan déterministe contient 474 lignes `COUNTRY_TECH_REMOVE`, auxquelles s’ajoute le nettoyage atomique agrégé de `urbanization`.

## 11. Relations pays-technologie finales

La cible effective est de **3 649 relations** sur 471 TAG recherchés. L’écart de 49 avec le contrôle documentaire proche de 3 698 correspond exactement aux 49 relations cibles qui portaient encore l’alias `urbanization`; elles sont volontairement exclues de la cible finale inerte. Aucun chiffre n’a été forcé.

Neuf pays dont l’ancien palier générique ne pouvait plus représenter exactement la cible ont reçu un setup explicite : ATB, BEL, BEO, BNN, IRC, NOR, NZP, POR et SLK.

## 12. Distribution des technologies sensibles

Le relevé exhaustif des TAG est dans `TECH_START_1776_FINAL_DISTRIBUTIONS.csv`.

| Technologie | TAG |
|---|---:|
| organized_workshops | 217 |
| traditional_papermaking | 78 |
| traditional_glassmaking | 62 |
| organized_forestry | 30 |
| traditional_food_processing | 357 |
| sugar_refining | 104 |
| industrial_acids | 4 |
| improved_agricultural_implements | 138 |
| advanced_crop_rotations | 43 |
| shaft_mining | 53 |
| applied_mineralogy | 30 |
| atmospheric_engine | 8 |
| coke_smelting | 2 |
| industrial_canals | 10 |
| institutionalized_public_credit | 24 |
| commercial_insurance_markets | 23 |
| stock_exchange | 8 |
| political_economy | 17 |
| medical_degrees | 56 |
| variolation_networks | 69 |
| organized_elementary_schooling | 26 |
| regulated_small_arms | 74 |
| light_infantry_tactics | 107 |
| standardized_field_artillery | 72 |
| scientific_naval_architecture | 29 |
| urbanization | 0 |
| railways | 0 |
| romanticism | 0 |
| joint_stock_companies | 0 |

Cas sensibles : `industrial_acids` = BEL, BEO, FRA, GBR ; `atmospheric_engine` = AUS, BEL, BEO, FRA, GBR, HUN, SPA, SPC ; `coke_smelting` = CHI, GBR. JAP et PLC possèdent `medical_degrees`, tandis que CLM, PER et SC2 ne la possèdent pas. MYS ne reçoit pas `mysorean_iron_cased_rocketry`.

## 13. Fermeture directe

Résultat : **0 prérequis direct manquant** sur les 471 TAG recherchés.

## 14. Fermeture transitive

Résultat : **0 prérequis transitif manquant** sur les 471 TAG recherchés.

## 15. Validateur

Le validateur final lit le graphe technologique réellement chargé et n’utilise plus les anciens prérequis forcés. Résultats : 471/471 MATCH, 0 décision historique non résolue, 0 technologie inconnue, 0 définition technologique dupliquée, 0 grant explicite dupliqué, 0 technologie C/D interdite, 0 technologie de départ interdite, 0 erreur structurelle et 0 erreur d’accolades.

Le fichier `TECH_START_1776_SANITY_CASES.csv` couvre GBR, FRA, NET, BEL, BEO, HUN, TUR, VEN, GEN, JAP, CHI, MUG, PLC et MYS.

## 16. GAL / MLT / PPU

GAL, MLT et PPU restent `RESEARCH_GAP / PRESERVE_CURRENT_PENDING_RESEARCH`. Leur état effectif local est inchangé et aucune technologie historique ne leur a été inventée.

## 17. Risques runtime

La validation statique ne peut pas confirmer le comportement de l’interface, l’apparition effective des centres urbains, la constructibilité dans toutes les situations, les tooltips de gates cumulés ni la réaction de l’IA. Ces points restent à vérifier dans le jeu avec la checklist opérateur.

Les anciens validateurs TECH6C5D/TECH6C6B signalent encore des attentes devenues obsolètes par rapport aux changements runtime déjà validés (notamment `error_deer`, les ancres aluminium et les recettes phosphates). Aucun fichier de ces chaînes n’a été modifié par cette passe TECH START.

## 18. `git diff --check`

**PASS (code retour 0).** Seuls les avertissements de conversion LF/CRLF préexistants ont été affichés ; ils ne constituent pas des erreurs de contenu.
