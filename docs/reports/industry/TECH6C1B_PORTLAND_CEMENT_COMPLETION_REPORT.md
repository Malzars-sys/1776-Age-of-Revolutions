# TECH6C1B — Portland Cement + Cement Works Completion

## 1. Checkpoint Git et canon vanilla

- Branche de départ et finale : `tech6c-goods-buildings-pm-implementation`.
- HEAD de départ et final : `08614a7 TECH6B phase 1: finalize technology tree and gameplay gate refactor`.
- Vanilla canonique : Victoria 3 `1.13.11`, sous `C:/Games/Victoria 3/game`.
- TECH6C1 était présent comme travail non commité et a été conservé.
- Aucun changement de branche, commit, push, merge, rebase ou reset.

## 2. Résultat

`TECH6C1B_PORTLAND_CEMENT_COMPLETION = PASS`.

Le blocage de TECH6C1 est levé par une technologie dédiée `portland_cement`. La chaîne productive `limestone + coal -> cement` est complète, la cimenterie est verrouillée par cette technologie et les deux méthodes de construction approuvées créent une demande immédiate de ciment.

## 3. Technologie Portland Cement

La technologie ajoutée est :

```text
ID = portland_cement
CATEGORY = production
ERA = era_7
DIRECT_PARENT = hydraulic_cements
TEXTURE = gfx/error_manul.dds (TEMP_ASSET)
```

`hydraulic_cements` reste inchangée en `era_6`. `era_7` est la première ère postérieure au socle 1776–1836 dans l'architecture actuelle du fork. Aucun second prérequis artificiel, modificateur national ou lien vers une technologie sans rapport n'est ajouté. Aucun fichier de positionnement GUI n'est requis par l'architecture actuelle.

Le déverrouillage est matérialisé par `building_cement_works`, qui requiert `portland_cement`. Le PM de base n'ajoute pas un deuxième verrou redondant.

Les noms de technologie `Portland Cement` et `Ciment Portland`, ainsi que leurs descriptions, existent déjà dans les localisations vanilla 1.13.11 et sont réutilisés sans doublon.

## 4. Bien Cement

```text
ID = cement
cost = 40
category = industrial
tradeable = yes
prestige_factor = 5
traded_quantity = 5
convoy_cost_multiplier = 0.5
texture = gfx/error_deer.dds (TEMP_ASSET)
```

Le prix, le prestige et le débit commercial reprennent le benchmark direct de `glass` (`40 / 5 / 5`, lot commercial de valeur 200). Le multiplicateur de convois `0.5` reprend le charbon afin de représenter un fret minéral lourd et volumineux. Le bien n'est inscrit dans aucun besoin POP ni buy package. Aucun bien `concrete` n'est créé.

## 5. Cement Works

`building_cement_works` suit l'architecture des industries lourdes actuelles :

- groupe existant `bg_heavy_industry` ;
- `city_type = city` et `levels_per_mesh = 50` ;
- coût `construction_cost_very_high` ;
- verrou `portland_cement` ;
- PMG `pmg_base_building_cement_works` ;
- `ownership_type = self` ;
- fond de panneau `building_panel_bg_heavy_industry.dds` ;
- restrictions standard des industries lourdes sous `law_industry_banned` et `law_extraction_economy` ;
- logique IA héritée du groupe industriel, sans valeur spéciale inventée.

## 6. PMG, PM, main-d'œuvre et bilan matière

Le PMG `pmg_base_building_cement_works` contient un unique PM de base : `pm_portland_cement_process` (`Portland Cement Process` / `Procédé du ciment Portland`). Aucun ladder de fours avancés n'est ajouté.

Par niveau :

```text
INPUT limestone = 30
INPUT coal = 15
OUTPUT cement = 40
POLLUTION = 15
SHOPKEEPERS = 500
LABORERS = 3000
MACHINISTS = 1000
ENGINEERS = 500
TOTAL WORKFORCE = 5000
```

La composition de main-d'œuvre et la pollution reprennent exactement le modèle lourd de `pm_bessemer_process` et `pm_leblanc_process`. Aux prix de base, les inputs valent `30 × 20 + 15 × 30 = 1 050` et la sortie `40 × 40 = 1 600`, soit une marge brute de 550 avant salaires. Elle reste entre la verrerie baseline (600) et Bessemer (750), sans outils ni produits chimiques ajoutés arbitrairement.

## 7. Icône de la cimenterie

L'asset indiqué par l'utilisateur a été retrouvé dans le canon vanilla :

```text
gfx/interface/icons/building_icons/unused/foundries.dds
```

Il est référencé directement par `building_cement_works`. Le DDS n'est ni copié ni modifié. `CEMENT_WORKS_ICON` n'est donc pas un `TEMP_ASSET`. Les textures de la technologie, du bien et du PM restent des placeholders valides et explicitement signalés ; elles n'affectent pas l'icône de bâtiment demandée.

## 8. Demande des Construction Sectors

Dans `common/production_methods/13_construction.txt` :

- `pm_steel_frame_buildings` reçoit `goods_input_cement_add = 30` ;
- `pm_arc_welded_buildings` reçoit `goods_input_cement_add = 40`.

Les inputs existants sont préservés, notamment `glass = 40` dans les deux PM. Aucun autre bâtiment d'infrastructure ou PM de construction n'est modifié.

## 9. Localisation

Deux fichiers UTF-8 BOM ajoutent les noms et descriptions English/French du bien, de la cimenterie, du PM et les clés dynamiques input/output de `cement`. Les clés de technologie vanilla existantes sont réutilisées afin d'éviter les doublons.

Noms effectifs requis :

- English : `Portland Cement`, `Cement`, `Cement Works`, `Portland Cement Process` ;
- Français : `Ciment Portland`, `Ciment`, `Cimenterie`, `Procédé du ciment Portland`.

## 10. Fichiers TECH6C1B changés

Gameplay :

1. `common/technology/technologies/11_tech6c1b_portland_cement.txt`
2. `common/goods/11_tech6c1b_cement.txt`
3. `common/buildings/11_tech6c1b_cement_works.txt`
4. `common/production_method_groups/11_tech6c1b_cement_pmgs.txt`
5. `common/production_methods/11_tech6c1b_cement_production.txt`
6. `common/production_methods/13_construction.txt`

Localisation :

7. `localization/english/tech6c1b_portland_cement_l_english.yml`
8. `localization/french/tech6c1b_portland_cement_l_french.yml`

Documentation :

9. `docs/reports/industry/TECH6C1B_PORTLAND_CEMENT_COMPLETION_REPORT.md`
10. `docs/reports/industry/TECH6C1B_PORTLAND_CEMENT_COMPLETION_MATRIX.csv`

Les neuf fichiers non suivis de TECH6C1 restent présents et inchangés. Aucun potentiel de ressource, fichier de sel ou autre topologie technologique existante n'est touché.

## 11. Validation statique

```text
UNKNOWN_TECH_IDS = 0
UNKNOWN_GOOD_IDS = 0
UNKNOWN_BUILDING_IDS = 0
UNKNOWN_PM_IDS = 0
UNKNOWN_PMG_IDS = 0
DUPLICATE_DEFINITIONS_INTRODUCED = 0
DUPLICATE_LOCALIZATION_KEYS_INTRODUCED = 0
INVALID_TEXTURE_PATHS = 0
BRACE_BALANCE_FAILURES = 0
CONCRETE_GOOD_REFERENCES = 0
CEMENT_DIRECT_POP_CONSUMPTION = 0
LIMESTONE_DIRECT_POP_CONSUMPTION = 0
STATE_LIMESTONE_POTENTIALS_CHANGED = 0
SALT_FILES_CHANGED = 0
UNRELATED_EXISTING_TECH_FILES_CHANGED = 0
STEEL_FRAME_CEMENT_INPUT = 30
ARC_WELDED_CEMENT_INPUT = 40
GIT_DIFF_CHECK = PASS
STATIC_VALIDATION = PASS
```

## 12. Smoke parser

Victoria 3 `1.13.11` a été lancé en `-debug_mode` avec le mod monté pendant 40 secondes, puis seul le processus créé a été arrêté. Le journal frais donne :

```text
TARGETED_TECH6C1B_ERROR_WARNING_HITS = 0
GENERIC_PARSE_UNKNOWN_TEXTURE_HITS = 0
PARSER_SMOKE = PASS
RUNTIME = NOT_CLAIMED
```

Le log complet conserve des doublons de localisation historiques hors périmètre déjà présents dans le mod et les contenus vanilla/hotfix ; aucune clé TECH6C1B n'apparaît parmi eux.

## 13. Travail différé

TECH6C2 reste seul responsable de la distribution mondiale des potentiels de `building_limestone_quarry`, à partir de la matrice différée TECH6C1. Les échelles de fours avancés, autres demandes d'infrastructure et remplacements des placeholders du bien/PM/technologie restent hors de cette phase.

```text
NEXT_PHASE = TECH6C2_LIMESTONE_RESOURCE_DISTRIBUTION
NEXT_PHASE_READY = YES
```
