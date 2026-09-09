# TECH6C5B — Rapport d’implémentation de la fondation cuivre

## 1. Résultat

**TECH6C5B RESULT: PASS (validation statique).**

Le cuivre est désormais un bien industriel marchand produit par une mine dédiée, distribué mondialement selon une matrice exhaustive de 675 États et consommé par cinq usages prioritaires. Aucun bien `copper_ore`, aluminium, bauxite ou alumine n’a été créé.

La consigne la plus récente de minimiser les technologies dédiées a été appliquée : **TECH6C5B crée zéro technologie**. La concentration avancée est rattachée à `geological_surveying`, technologie existante qui n’avait pas de déblocage direct de bâtiment ou de méthode de production. `copper_sheathing` reçoit également enfin un déblocage réel.

## 2. Bien cuivre et infrastructure d’interface

`copper` est défini avec :

- prix de base : `50` ;
- catégorie : `industrial` ;
- commerce : `tradeable = yes` ;
- consommation directe des POP : aucune ;
- visuel temporaire : `gfx/error_deer.dds`.

Les quatre modificateurs dynamiques sont enregistrés une seule fois dans le propriétaire unifié des biens TECH6C :

- `goods_input_copper_add` ;
- `goods_input_copper_mult` ;
- `goods_output_copper_add` ;
- `goods_output_copper_mult`.

Le texticon `@copper!`, les libellés directs et les libellés `modifier_` sont présents en anglais et en français. Les nouveaux fichiers de localisation et les fichiers unifiés modifiés sont encodés en UTF-8 avec BOM.

## 3. Mine de cuivre

`building_copper_mine` suit l’architecture minière locale :

```text
building_group = bg_mining
city_type = mine
required_construction = construction_cost_medium
terrain_manipulator = mining
ownership_type = self
ai_value = 1000
unlocking_technologies = shaft_mining
```

Il s’agit d’une ressource plafonnée indépendante de `building_lead_mine`.

Les cinq familles de méthodes sont :

1. `pmg_mining_equipment_building_copper_mine` ;
2. `pmg_explosives_building_copper_mine` ;
3. `pmg_steam_automation_building_copper_mine` ;
4. `pmg_train_automation_building_copper_mine` ;
5. `pmg_ore_concentration_building_copper_mine`.

Les familles d’automatisation réemploient les méthodes minières sûres déjà présentes : `pm_no_steam_automation`, `pm_steam_donkey_mine`, `pm_road_carts` et `pm_rail_transport_mine`. Elles conservent donc les réductions normales d’emploi et leurs technologies existantes.

### Échelle d’extraction

| Méthode | Déblocage | Intrants | Production | Marge brute | Emploi | Pollution |
|---|---|---:|---:|---:|---:|---:|
| Pics et pelles | mine ouverte par `shaft_mining` | 5 outils = 200 | 15 cuivre = 750 | 550 | 5 000 | 0 |
| Pompe atmosphérique | `atmospheric_engine` | 10 outils + 10 charbon = 700 | 30 cuivre = 1 500 | 800 | 5 000 | 5 |
| Pompe à condensation | `condensing_steam_engines` | 15 outils + 15 charbon = 1 050 | 45 cuivre = 2 250 | 1 200 | 5 000 | 15 |
| Pompe Diesel | `compression_ignition` | 15 outils + 3 carburants raffinés = 780 | 55 cuivre = 2 750 | 1 970 | 5 000 | 10 |

Le Diesel consomme bien `refined_fuels`, jamais du pétrole brut.

Les additifs explosifs sont calibrés pour le prix supérieur du cuivre :

- nitroglycérine : `5 explosives -> +8 copper`, marge additive 150, pollution 5 et pénalités de mortalité minières existantes ;
- dynamite : `10 explosives -> +15 copper`, marge additive 250 et pollution 10.

Tous les nouveaux PM et PMG sans DDS final utilisent `gfx/error_deer.dds`.

## 4. Concentration des minerais sans nouvelle technologie

La technologie dédiée `ore_concentration` demandée dans le prompt anglais n’a pas été créée, conformément à l’instruction utilisateur plus récente de réduire les nœuds dédiés et de remplir les technologies vides du fork.

Le PMG contient :

- `pm_no_ore_concentration_building_copper_mine`, neutre et disponible par défaut ;
- `pm_ore_concentration_building_copper_mine`, débloqué par `geological_surveying`.

La méthode avancée consomme `5 tools + 5 industrial_chemicals` et ajoute `10 copper`. Aux prix de base, l’intrant vaut 400 et le cuivre récupéré 500, soit une marge additive de 100. C’est une recette minimale à nombres entiers, utile sans ajouter de bien « concentré » ni d’acide sulfurique marchand.

`geological_surveying` reste en `era_6` avec ses parents actuels `applied_mineralogy` et `professional_civil_engineering`. La topologie n’a pas été modifiée.

## 5. Distribution mondiale

La matrice finale est `TECH6C5B_COPPER_GLOBAL_RESOURCE_MATRIX.csv`. Elle contient exactement les colonnes demandées et une décision explicite pour chacun des 675 États.

Échelle déterministe :

```text
NONE = 0
LOW = 8
MODEST = 16
MEDIUM = 24
HIGH = 36
VERY_HIGH = 48
WORLD_CLASS = 60
```

Résultat :

| Indicateur | Valeur |
|---|---:|
| États examinés | 675 |
| Potentiel non nul | 302 |
| Potentiel nul | 373 |
| Potentiel cumulé | 5 924 |
| NONE | 373 |
| LOW | 73 |
| MODEST | 120 |
| MEDIUM | 64 |
| HIGH | 28 |
| VERY_HIGH | 12 |
| WORLD_CLASS | 5 |
| Fichiers de régions modifiés | 16 |

La distribution représente le potentiel géologiquement exploitable, y compris les grands districts reconnus après la période du jeu, tout en réservant les valeurs 48 et 60 aux provinces de rang mondial. Les catégories de preuve de la matrice privilégient les évaluations mondiales USGS, les services géologiques nationaux, Geoscience Australia et les districts historiques robustes.

Références méthodologiques principales :

- USGS, *Global Copper Assessment*: https://pubs.usgs.gov/publication/fs20143004
- USGS, *A Global Database of Porphyry Copper Deposits and Prospects*: https://www.usgs.gov/data/a-global-database-porphyry-copper-deposits-and-prospects
- USGS, *Central African Copperbelt assessment*: https://www.usgs.gov/publications/descriptive-models-grade-tonnage-relations-and-databases-assessment-sediment-hosted
- USGS, *Where Does Copper Come From?*: https://pubs.usgs.gov/fs/2009/3031/FS2009-3031.pdf

## 6. Migrations des anciennes abstractions

- Ashio, dans `common/history/buildings/11_east_asia.txt`, est actif dans le fork : son niveau de `building_lead_mine` a été converti en `building_copper_mine`, avec le PM manuel cuivre et le PM neutre de concentration.
- Besshi n’est pas instancié comme mine de plomb dans le fichier local courant : aucune mine inexistante n’a été inventée. Son État, `STATE_SHIKOKU`, reçoit toutefois un potentiel cuivre géologique.
- `state_trait_copper_coast` remplace le bonus de débit de la mine de plomb par `building_copper_mine_throughput_add = 0.1`. Le bonus distinct de mine de fer est conservé.
- La mention « Copper trade » du traité de Nagasaki est commentée/morte ; elle n’a pas été modifiée.

## 7. Cinq consommateurs prioritaires

1. **Chantier naval** — nouveau PMG optionnel. `pm_copper_sheathing_building_shipyard`, débloqué par `copper_sheathing`, consomme 5 cuivre et ajoute 5 clippers. Valeur : 250 d’intrants pour 300 de production, marge additive 50. Une méthode neutre permet de fonctionner sans cuivre.
2. **Téléphones** — `20 lead` est remplacé par `15 copper`; fer, caoutchouc, outils, production et emplois sont inchangés. Marge : 1 400 avant, 1 450 après.
3. **Moteurs électriques** — ajout de `10 copper`, sans rééquilibrage de la production. Marge : 1 900 avant, 1 400 après.
4. **Radios** — ajout de `2 copper`; la conversion de téléphones est conservée. Marge additive : 300 avant, 200 après.
5. **Première centrale électrique** — ajout de `2 copper`; les 4 moteurs, 5 charbon, 5 bois et 25 électricité sont conservés. Marge : 260 avant, 160 après.

Les calculs détaillés figurent dans les deux matrices économiques livrées.

## 8. Validation

Le validateur `tools/tech6c5b_validate.py` donne **PASS** :

- bien cuivre défini exactement une fois ;
- bâtiment cuivre défini exactement une fois ;
- chaque nouveau PM et PMG défini exactement une fois ;
- toutes les références PM des PMG résolues ;
- quatre modificateurs de bien résolus ;
- zéro bien inconnu dans les fichiers de PM concernés ;
- zéro nouvelle clé de localisation dupliquée ;
- zéro forme mal orthographiée `ggoods_`, `oods_` orpheline ou `goods_copper_add` ;
- accolades équilibrées dans tous les fichiers gameplay modifiés ou créés ;
- 675 lignes uniques dans la matrice ;
- zéro État manquant ;
- zéro doublon `building_copper_mine` par État ;
- zéro divergence matrice/carte ;
- zéro ligne de ressource non-cuivre changée dans le diff de carte ;
- graphe technologique : 285 nœuds analysés, zéro cycle, zéro nouvelle technologie cuivre ;
- parents de `geological_surveying` et `copper_sheathing` inchangés ;
- `gui/tech_tree.gui` inchangé ;
- `git diff --check` réussi ; seuls les avertissements informatifs LF/CRLF de Git sont affichés.

Aucun démarrage du jeu ni contrôle interactif du marché/tooltip n’a été effectué. La réussite statique ne constitue donc pas une preuve d’exécution dans l’interface.

## 9. Fichiers créés

- `common/goods/13_tech6c5b_copper.txt`
- `common/buildings/13_tech6c5b_copper_mine.txt`
- `common/production_method_groups/13_tech6c5b_copper_pmgs.txt`
- `common/production_methods/13_tech6c5b_copper_production_and_consumers.txt`
- `common/state_traits/12_oceania_traits.txt` — copie locale canonique du fichier vanilla avec migration ciblée de `state_trait_copper_coast`
- `localization/english/tech6c5b_copper_l_english.yml`
- `localization/french/tech6c5b_copper_l_french.yml`
- `docs/reports/industry/TECH6C5B_COPPER_IMPLEMENTATION_REPORT.md`
- `docs/reports/industry/TECH6C5B_COPPER_GLOBAL_RESOURCE_MATRIX.csv`
- `docs/reports/industry/TECH6C5B_COPPER_CONSUMER_IMPLEMENTATION_MATRIX.csv`
- `docs/reports/industry/TECH6C5B_COPPER_ECONOMIC_VALIDATION.csv`
- `tools/tech6c5b_build_copper_distribution.py`
- `tools/tech6c5b_validate.py`

## 10. Fichiers modifiés

- `common/buildings/01_industry.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/modifier_type_definitions/12_tech6c_custom_goods_modifier_types.txt`
- `common/production_methods/01_industry.txt`
- `common/production_methods/06_urban_center.txt`
- `gui/tech6c_goods_texticons.gui`
- `localization/english/tech6c_goods_modifiers_l_english.yml`
- `localization/french/tech6c_goods_modifiers_l_french.yml`
- les 16 fichiers `map_data/state_regions/00_west_europe.txt` à `15_russia.txt`.

Les changements de ciment et les documents TECH6C5A déjà présents dans le worktree ont été préservés et ne sont pas revendiqués comme créations TECH6C5B.

## 11. Éléments explicitement différés

Restent inchangés : éclairage public électrique, trains électriques, amorces à percussion, obus explosifs, automobile, automobile de masse, secteur de construction et sidérurgie à arc électrique.

L’aluminium, l’alumine, la bauxite, Hall-Héroult et le bâtiment de métallurgie non ferreuse restent exclus de TECH6C5B.

## 12. Portée proposée pour TECH6C5C

Pour respecter la nouvelle politique de réduction des technologies dédiées, TECH6C5C devrait d’abord tenter une implémentation **sans nouvelle technologie** :

1. créer uniquement le bien marchand `aluminium` ;
2. créer `building_non_ferrous_metallurgy_works` ;
3. créer un PM Hall-Héroult agrégé consommant beaucoup d’électricité et des produits chimiques industriels ;
4. rattacher ses conditions aux technologies existantes `electrical_capacitors` et `industrial_alkalis` si leur combinaison est mécaniquement sûre ;
5. ajouter seulement deux demandes structurantes : construction aéronautique métallique tardive et conducteurs de réseau en aluminium ;
6. ne créer ni bauxite, ni alumine, ni mine dédiée, ni distribution mondiale supplémentaire ;
7. ne créer `aluminium_metallurgy` qu’en dernier recours si les technologies existantes ne peuvent pas exprimer proprement le double verrou électrochimie/chimie.

Les modifications ne sont ni commitées ni poussées.
