# HOTFIX-3C - Armée minimale IR1 / Mamluk Iraq

## 1. Résumé

Cette phase importe uniquement la formation militaire terrestre minimale de `IR1` / Mamluk Iraq depuis le hotfix upstream. Le bloc ajouté donne à IR1 une armée initiale cohérente avec les quatre states activés en HOTFIX-3B, sans importer diplomatie, guerre, secret goals IA, flotte ou modifications d'autres pays.

## 2. Pourquoi cette phase est limitée à l'armée IR1

HOTFIX-3A a créé le tag IR1 et HOTFIX-3B l'a activé territorialement. Cette phase se limite donc à éviter qu'IR1 existe sur la carte sans armée propre. Les changements plus larges du hotfix, notamment diplomatiques ou géopolitiques, restent exclus pour garder une migration contrôlée.

## 3. Fichier hotfix consulté

- `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source\common\history\military_formations\04_military_formations_middle_east.txt`

## 4. Fichiers modifiés

- `common/history/military_formations/04_military_formations_middle_east.txt`
- `docs/reports/hotfix/HOTFIX_3C_IMPORT_IR1_ARMY.md`

## 5. Formation IR1 importée

| Élément | Valeur |
|---|---|
| Pays | `c:IR1` |
| Nom interne sauvegardé | `mamluk_army` |
| Type | `army` |
| HQ | `sr:region_near_east` |
| Général | `mamluk_gen`, général terrestre uniquement |

Composition importée :

| State | Unité | Nombre |
|---|---|---:|
| `STATE_BASRA` | `combat_unit_type_irregular_infantry` | 5 |
| `STATE_BAGHDAD` | `combat_unit_type_irregular_infantry` | 5 |
| `STATE_DEIR_EZ_ZOR` | `combat_unit_type_hussars` | 2 |
| `STATE_MOSUL` | `combat_unit_type_cannon_artillery` | 2 |

Général importé :

- `is_general = yes`
- culture `cu:georgian`
- religion `rel:sunni`
- interest group `ig_armed_forces`
- ideology `ideology_royalist`
- age `29`
- rank `commander_rank_2`
- HQ `region_near_east`
- traits `meticulous`, `charismatic`, `experienced_offensive_planner`
- transféré vers `scope:mamluk_army`

Le général a été importé car il est contenu dans le même bloc `c:IR1`, terrestre, et ne dépend pas d'un fichier séparé ou d'une flotte.

## 6. Vérification du hq_region

`region_near_east` existe dans la vanilla The Great Wave locale :

- `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\west_south_asia_strategic_regions.txt`
- références associées dans `common/geographic_regions`.

Les unités utilisées sont également présentes dans la vanilla 1.13 :

- `combat_unit_type_irregular_infantry`
- `combat_unit_type_hussars`
- `combat_unit_type_cannon_artillery`

## 7. Ce qui n'a pas été importé

- Aucune modification des formations `TUR`.
- Aucune modification des formations `PER`.
- Aucune modification des formations `OMA`.
- Aucune modification des formations `ARB`.
- Aucune flotte.
- Aucun navire.
- Aucun amiral.
- Aucun changement Oman / Bahriat al-Masqat.
- Aucune diplomatie `TUR -> IR1`.
- Aucun diplomatic play `PER / IR1 / ARB / OMA`.
- Aucun secret goal IA.
- Aucun state, pop ou bâtiment.

## 8. Vérifications effectuées

Commandes de contrôle exécutées :

- `git status --short`
- `git branch --show-current`
- `git log --oneline -5`
- `git stash list`
- recherche ciblée `c:IR1`, `mamluk_army`, `mamluk_gen`, `region_near_east`
- recherche de références navales obsolètes : `building_military_shipyard`, `building_naval_base`, `pm_military_shipbuilding`

Résultat :

- `c:IR1`, `mamluk_army` et `mamluk_gen` apparaissent uniquement dans le fichier militaire Middle East.
- `region_near_east` apparaît dans le nouveau bloc IR1 et existait déjà ailleurs dans le fichier.
- Aucun `building_military_shipyard` ni `pm_military_shipbuilding` n'a été trouvé.
- Les références `building_naval_base` trouvées existent déjà dans `common/ai_strategies/00_default_strategy.txt` et `common/defines/00_defines.txt`; elles ne viennent pas de cette phase.

## 9. Risques restants

- IR1 n'a toujours pas de relation diplomatique explicite avec `TUR`.
- IR1 n'a pas de diplomatic play ou guerre initiale.
- Le général est générique et sans nom localisé, car le hotfix le fournit ainsi dans le bloc militaire.
- L'équilibrage exact de 14 unités devra être testé en jeu.

## 10. Tests à faire en jeu

1. Lancer le mod seul.
2. Démarrer une partie en 1776.
3. Vérifier qu'IR1 existe sur Basra, Baghdad, Mosul et Deir ez-Zor.
4. Vérifier qu'IR1 possède une formation terrestre en `region_near_east`.
5. Vérifier que le général IR1 est présent et assigné à l'armée.
6. Observer un mois de jeu et surveiller `error.log`.
7. Rechercher dans les logs : `IR1`, `mamluk_army`, `mamluk_gen`, `create_military_formation`, `create_character`, `region_near_east`.

## 11. Liste exacte des fichiers modifiés

- `common/history/military_formations/04_military_formations_middle_east.txt`
- `docs/reports/hotfix/HOTFIX_3C_IMPORT_IR1_ARMY.md`

## 12. Confirmation de périmètre

- Aucune formation `TUR`, `PER`, `OMA` ou `ARB` modifiée.
- Aucune flotte modifiée.
- Aucun state modifié.
- Aucune pop modifiée.
- Aucun bâtiment modifié.
- Aucune diplomatie modifiée.
- Aucun diplomatic play importé.
- Aucun secret goal IA importé.
- Aucun changement BIC, Japon, Inde ou NAVY.
- Aucun changement aux lois HOTFIX-2.
- Le stash MARATH n'a pas été appliqué ni modifié.
