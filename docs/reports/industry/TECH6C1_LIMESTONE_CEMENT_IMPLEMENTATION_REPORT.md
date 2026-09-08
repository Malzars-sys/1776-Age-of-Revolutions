# TECH6C1 — Limestone + Cement Foundation Implementation

## 1. Checkpoint Git et canon vanilla

- Branche : `tech6c-goods-buildings-pm-implementation`.
- HEAD initial et final : `08614a7 TECH6B phase 1: finalize technology tree and gameplay gate refactor`.
- Vanilla canonique : Victoria 3 `1.13.11`, sous `C:/Games/Victoria 3/game`.
- Worktree initial : propre.
- Aucun changement de branche, commit, push, merge, rebase ou reset.

Le descripteur remplace uniquement `common/technology/eras` et `common/technology/technologies`. Les nouveaux objets économiques peuvent donc être ajoutés dans des fichiers dédiés sans shadow d'un fichier vanilla entier.

## 2. Résultat de phase

`TECH6C1_LIMESTONE_CEMENT_IMPLEMENTATION = PARTIAL`.

La fondation calcaire est implémentée et valide. Le volet ciment est bloqué par l'absence d'une technologie Portland Cement dans l'arbre effectif. Conformément à l'instruction autoritative, aucun nouvel ID technologique n'a été inventé et ni `hydraulic_cements` ni `reinforced_concrete` n'ont été substitués.

## 3. Audit pré-édition

Constats effectifs :

- les biens du mod utilisent des fichiers dédiés sous `common/goods` ;
- les bâtiments de ressource 1.13.11 utilisent `bg_mining` et les potentiels d'État utilisent directement les IDs `building_*` sous `capped_resources` ;
- `ownership_type = self` est la convention actuelle des mines ;
- les mines de charbon, fer, plomb, soufre et sel sont gatées par `shaft_mining` ;
- `pm_steel_frame_buildings` et `pm_arc_welded_buildings` existent dans `common/production_methods/13_construction.txt` ;
- leurs inputs courants sont respectivement `steel 50 / glass 40 / explosives 10 / tools 20` et `steel 50 / glass 40 / explosives 20 / tools 40 / electricity 40` ;
- `hydraulic_cements` existe en `era_6` ;
- `reinforced_concrete` existe en `era_8` ;
- aucun ID ou nom localisé contenant Portland Cement n'existe dans l'arbre technologique effectif ;
- le bien sel existant porte exactement l'ID `salt`, défini dans `common/goods/10_tech6a1b_salt.txt`.

## 4. IDs ajoutés

```text
GOOD = limestone
BUILDING = building_limestone_quarry
PMG = pmg_base_building_limestone_quarry
PM = pm_picks_and_shovels_building_limestone_quarry
BUILDING_GROUPS_ADDED = 0
```

Le bâtiment réutilise `bg_mining`; aucun groupe artificiel n'a été créé.

## 5. Définition du bien Limestone

```text
cost = 20
category = industrial
tradeable = yes
prestige_factor = 3
traded_quantity = 10
convoy_cost_multiplier = 0.5
texture = gfx/error_deer.dds
```

Le prix 20 suit le bien brut volumineux `wood` (prix 20) plutôt que les minerais plus concentrés `coal` (30), `iron` (40) ou `sulfur` (50). Le débit commercial `10` donne une unité de lot de valeur 200, identique à la convention observée pour `wood`, `iron`, `steel`, `glass` et `explosives`. Le multiplicateur de convois `0.5` suit le charbon et représente un fret lourd et volumineux.

Le calcaire n'est ajouté à aucun besoin POP ni buy package.

## 6. Définition de Limestone Quarry

`building_limestone_quarry` est un bâtiment extractif :

- groupe existant `bg_mining` ;
- `city_type = mine` ;
- `construction_cost_medium` ;
- `terrain_manipulator = mining` ;
- gate `shaft_mining` ;
- `ownership_type = self` ;
- fond de panneau minier vanilla ;
- `ai_value = 1000`, identique aux mines industrielles comparables ;
- icône provisoire utilisateur `gfx/error_deer.dds`.

Le gate `shaft_mining` est un ID Production existant en `era_1` et suit la convention effective des mines du fork. Aucun prérequis ni ère technologique n'a été modifié.

## 7. PMG et PM de carrière

Le PMG `pmg_base_building_limestone_quarry` contient uniquement `pm_picks_and_shovels_building_limestone_quarry`.

Le PM baseline consomme `2 tools`, produit `30 limestone` et emploie 500 shopkeepers et 4 500 laborers. À prix de base, la sortie vaut `30 × 20 = 600` et les outils `2 × 40 = 80`, soit une marge brute de 520 avant salaires. C'est exactement l'échelle du PM baseline de la mine de sel du fork (`20 salt × 30 - 2 tools × 40 = 520`) et une main-d'œuvre de 5 000 comparable aux mines et industries vanilla.

Aucune échelle mécanisée, explosive, vapeur ou rail supplémentaire n'est créée dans TECH6C1.

## 8. Blocage Portland Cement

La lignée souhaitée était `hydraulic_cements -> Portland Cement -> Cement Works`. L'audit ne trouve aucune technologie Portland Cement effective. En conséquence :

```text
PORTLAND_CEMENT_GATE = BLOCKED_MISSING_TECH_ID
CEMENT_GOOD = NOT_CREATED
BUILDING_CEMENT_WORKS = NOT_CREATED
CEMENT_PM = NOT_CREATED
CEMENT_PMG = NOT_CREATED
```

Créer `cement` sans producteur ni demande valide aurait introduit un bien mort. Créer Cement Works sans gate aurait contredit la décision de design. Le rattacher à `hydraulic_cements` ou `reinforced_concrete` aurait constitué une substitution explicitement interdite.

## 9. Demande Construction Sector

`common/production_methods/13_construction.txt` est inchangé. Les quantités approuvées `30` pour `pm_steel_frame_buildings` et `40` pour `pm_arc_welded_buildings` restent enregistrées comme future migration, mais ne sont pas appliquées tant que la chaîne d'offre Cement Works ne possède pas de gate Portland Cement valide.

Tous les inputs existants, notamment le verre à 40 dans les deux PM, restent intacts. Aucune référence à un bien Concrete n'a été ajoutée.

## 10. Assets temporaires

Conformément à l'instruction utilisateur, `gfx/error_deer.dds` est utilisé comme `TEMP_ASSET` pour l'icône de `building_limestone_quarry`. Le même fichier existant sert temporairement à la texture du bien `limestone`. Le PM et le PMG réutilisent les textures vanilla existantes `picks_and_shovels.dds` et `mixed_icon_base.dds`.

Aucun DDS n'a été créé ou modifié.

## 11. Localisation

Deux nouveaux fichiers UTF-8 BOM fournissent :

- English : `Limestone`, `Limestone Quarry`, `Picks and Shovels` ;
- Français : `Calcaire`, `Carrière de calcaire`, `Pics et pelles` ;
- les clés dynamiques input/output `limestone` nécessaires aux tooltips.

Les noms Cement et Cement Works ne sont pas ajoutés, car leurs objets restent bloqués et absents. Aucun doublon de clé introduit n'a été détecté.

## 12. Future Limestone Hook Table

| Objet courant | Fichier | Inputs actuels | Rôle historique futur | Recommandation | Confiance | Phase |
|---|---|---|---|---|---|---|
| `pm_leblanc_process` | `common/production_methods/01_industry.txt` | sulfur 20; fertilizer 20 | charge calcaire du procédé Leblanc | ajouter limestone après révision de la chimie et du sel | HIGH | TECH6C postérieur |
| `pm_leaded_glass` | `common/production_methods/01_industry.txt` | wood 20; lead 10 | stabilisant calcique et charge verrière | ajouter un input limestone calibré | HIGH | TECH6C postérieur |
| `pm_bessemer_process` | `common/production_methods/01_industry.txt` | iron 60; coal 30 | flux basique selon filière métallurgique | auditer la filière avant ajout | MEDIUM | TECH6C postérieur |
| `pm_steel_frame_buildings` | `common/production_methods/13_construction.txt` | steel 50; glass 40; explosives 10; tools 20 | demande de ciment de construction | ajouter cement 30 après déblocage du producteur | HIGH | achèvement Cement |
| `pm_arc_welded_buildings` | `common/production_methods/13_construction.txt` | steel 50; glass 40; explosives 20; tools 40; electricity 40 | demande avancée de ciment | ajouter cement 40 après déblocage du producteur | HIGH | achèvement Cement |
| `pm_modern_port` | `common/production_methods/11_private_infrastructure.txt` | steamers 5; oil 10 | ouvrages portuaires en béton | auditer une demande secondaire de cement | HIGH | infrastructure ultérieure |

Aucun de ces hooks n'est modifié dans TECH6C1.

## 13. Potentiels de ressource différés

Les 675 États terrestres de l'overlay effectif sont inventoriés dans `TECH6C1_LIMESTONE_RESOURCE_POTENTIAL_DEFERRED_MATRIX.csv`, avec leurs ressources courantes. Les 675 cellules `candidate_limestone_potential` restent vides, toutes marquées `NOT_RESEARCHED` et `DEFERRED_TECH6C2`.

Aucun fichier sous `map_data/state_regions` n'a été modifié. Le parser accepte la définition structurelle sans potentiel ; la carrière est donc valide mais non constructible en économie normale jusqu'à TECH6C2.

## 14. Validation statique

```text
STATIC_VALIDATION = PASS
NEW_GOODS = 1
NEW_BUILDINGS = 1
NEW_PMGS = 1
NEW_PMS = 1
UNKNOWN_IDS_INTRODUCED = 0
DUPLICATE_DEFINITIONS_INTRODUCED = 0
DUPLICATE_LOCALIZATION_KEYS_INTRODUCED = 0
INVALID_TEXTURE_PATHS_INTRODUCED = 0
CONCRETE_GOOD_REFERENCES = 0
CEMENT_DIRECT_POP_CONSUMPTION = 0
LIMESTONE_DIRECT_POP_CONSUMPTION = 0
SALT_CHANGED = NO
UNRELATED_TECHNOLOGY_FILES_CHANGED = 0
MAP_RESOURCE_POTENTIAL_FILES_CHANGED = 0
CONSTRUCTION_PM_FILES_CHANGED = 0
GIT_DIFF_CHECK = PASS
```

## 15. Smoke parser/log

Un smoke de 40 secondes a lancé Victoria 3 1.13.11 avec `-debug_mode` et le descripteur du mod, puis arrêté uniquement le processus créé. Le journal frais contient zéro diagnostic ciblant `limestone`, les trois IDs de bâtiment/PMG/PM, les fichiers TECH6C1, une texture invalide, un bien/bâtiment/PM/PMG inconnu ou une erreur de parsing.

Les doublons de localisation historiques et trois avertissements GUI préexistants restent hors périmètre.

```text
PARSER_SMOKE = PASS
RUNTIME = NOT_CLAIMED
```

## 16. Fichiers changés et résumé Git

Fichiers gameplay/localisation ajoutés :

1. `common/goods/10_tech6c1_limestone.txt`
2. `common/buildings/10_tech6c1_limestone_quarry.txt`
3. `common/production_method_groups/10_tech6c1_limestone_pmgs.txt`
4. `common/production_methods/10_tech6c1_limestone_production.txt`
5. `localization/english/tech6c1_limestone_l_english.yml`
6. `localization/french/tech6c1_limestone_l_french.yml`

Documentation ajoutée :

1. `docs/reports/industry/TECH6C1_LIMESTONE_CEMENT_IMPLEMENTATION_REPORT.md`
2. `docs/reports/industry/TECH6C1_LIMESTONE_CEMENT_IMPLEMENTATION_MATRIX.csv`
3. `docs/reports/industry/TECH6C1_LIMESTONE_RESOURCE_POTENTIAL_DEFERRED_MATRIX.csv`

Le status final ne contient que ces neuf nouveaux fichiers. `git diff --name-only` et `git diff --stat` sont vides parce que les fichiers sont non suivis ; `git status --short` constitue donc le relevé autoritatif de cette phase. Aucun fichier préexistant n'a été modifié.

## 17. Suite

TECH6C2 peut rechercher puis attribuer les potentiels de `building_limestone_quarry`. L'achèvement du volet ciment nécessite séparément une décision autorisée créant ou identifiant une vraie technologie Portland Cement ; seulement après cela pourront être ajoutés `cement`, Cement Works et les demandes Construction Sector 30/40.
