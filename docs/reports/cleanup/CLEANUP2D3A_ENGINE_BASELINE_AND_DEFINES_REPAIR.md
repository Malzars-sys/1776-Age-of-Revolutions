# CLEANUP-2D-3A — Baseline moteur The Great Wave et réparation sûre des defines

## 1. Baseline Git réelle

Baseline relevée avant toute modification :

```text
BRANCH = cleanup-post-release
HEAD = e9481f4a51978f962e5e715fd9a1283564140595
INDEX_STATE = NON_EMPTY_PREEXISTING_PRESERVED
WORKTREE_STATE = DIRTY_PREEXISTING_PRESERVED
BASELINE_GIT_DIFF_CHECK = PASS
```

Inventaire initial exact :

```text
 M docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md
A  docs/reports/cleanup/CLEANUP2D2_V3_HISTORICAL_CONVERSION_AND_GLOBAL_BALANCE_MODEL.md
A  docs/research/military/CLEANUP2D2_FORMATION_RECONSTRUCTION_PLAN_1776.csv
A  docs/research/military/CLEANUP2D2_IMPERIAL_AND_COMPANY_FORCE_ALLOCATION.csv
A  docs/research/military/CLEANUP2D2_STRUCTURAL_FIX_PLAN.csv
A  docs/research/military/CLEANUP2D2_WORLD_LAND_CONVERSION_TARGETS_1776.csv
A  docs/research/military/CLEANUP2D2_WORLD_NAVAL_CONVERSION_TARGETS_1776.csv
?? docs/reports/cleanup/CLEANUP1C1_MARATH_NAVAL_CREW_DIAGNOSTIC.md
?? docs/reports/cleanup/CLEANUP2D3A_ENGINE_BASELINE_AND_DEFINES_REPAIR.md
?? docs/reports/hotfix/_index/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv
?? docs/reports/hotfix/_index/army.md
?? docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
?? docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
?? docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

Les six ajouts 2D-2 étaient déjà stagés. Le brouillon 3A non suivi, fondé sur une ancienne racine 1.13.0, a été remplacé par cet audit de la racine imposée. Aucun autre état préexistant n’a été restauré, stashé, nettoyé ou normalisé.

## 2. Installation vanilla canonique

```text
REFERENCE_GAME_ROOT = C:\Games\Victoria 3
REFERENCE_GAME_VERSION = 1.13.9 (Matcha)
REFERENCE_BASELINE_ACCEPTED = YES
STEAM_INSTALLATION_USED_AS_REFERENCE = NO
HOTFIX_1_13_10_AUDITED = NO
HOTFIX_1_13_10_CHANGES_IMPLEMENTED = 0
```

Aucune autre installation, baseline Internet ou donnée 1.13.10 n’a été inspectée.

## 3. Preuve de version

Preuves locales concordantes :

- `launcher/launcher-settings.json` : `1.13.9 (Matcha)`, `rawVersion = 1.13.9` ;
- `caligula_branch.txt` : `release/1.13.9`, révision `afea32b87c002fe0621f2f732d60a80ba914c14e` ;
- `clausewitz_branch.txt` : `caligula/release/1.13.9`, révision `51e396f1d797a21e1a7a3329b9b65fd7661c2d4c` ;
- marqueur racine `v1.13.9.xxh128`.

```text
REFERENCE_GAME_VERSION_EVIDENCE = launcher version/rawVersion + Caligula branch/revision + Clausewitz branch/revision + v1.13.9 marker
```

## 4. Chemin/hash du define vanilla

```text
REFERENCE_DEFINES_PATH = C:\Games\Victoria 3\game\common\defines\00_defines.txt
REFERENCE_DEFINES_SIZE = 204487
REFERENCE_DEFINES_SHA256 = 398C364C108CE3FFA57FB25E000E3B8BCE50E1F882E37C36A358EEA34E4E1CF0
FORK_DEFINES_SIZE_BEFORE = 173634
FORK_DEFINES_SHA256_BEFORE = 478F6A7DC581C1E4E9C9BA103EE3902401E032E9718E82BD84133326FDDFBF2C
```

## 5. Architecture du define du fork

La référence charge six fichiers sous `common/defines` : `00_ai.txt`, `00_audio.txt`, `00_defines.txt`, `00_graphics.txt`, `00_interfaces.txt`, `00_shaders.txt`. Le fork ne possédait que `00_defines.txt`, au même chemin relatif : cette vieille copie complète masquait le fichier vanilla.

Plusieurs fichiers et blocs d’un même namespace sont bien acceptés (`NGUI` et `NPops` sont répartis en plusieurs blocs), mais la priorité d’une même clé redéfinie tardivement n’est pas démontrée localement. La surcharge partielle de `NGame.START_DATE` n’est donc pas déclarée sûre.

## 6. Comparaison section par section

Le parseur a comparé 1 331 affectations fork à 1 576 affectations de référence, sans clé dupliquée détectée.

| Section | Fork | Réf. | Deltas | Manquantes | Fork seul | Valeurs |
|---|---:|---:|---:|---:|---:|---:|
| NBattle | 21 | 66 | 45 | 45 | 0 | 0 |
| NCharacters | 59 | 103 | 46 | 44 | 0 | 2 |
| NCountry | 40 | 44 | 6 | 5 | 1 | 0 |
| NDebug | 3 | 3 | 0 | 0 | 0 | 0 |
| NDiplomacy | 296 | 351 | 60 | 56 | 1 | 3 |
| NEconomy | 269 | 292 | 36 | 28 | 5 | 3 |
| NEvents | 3 | 3 | 0 | 0 | 0 | 0 |
| NGame | 6 | 6 | 1 | 0 | 0 | 1 |
| NHarvestConditions | 2 | 2 | 0 | 0 | 0 | 0 |
| NJominiMap | 4 | 4 | 0 | 0 | 0 | 0 |
| NMilitary | 101 | 165 | 92 | 76 | 12 | 4 |
| NPolitics | 205 | 208 | 9 | 3 | 0 | 6 |
| NPops | 225 | 225 | 1 | 0 | 0 | 1 |
| NPowerBlocs | 27 | 24 | 3 | 0 | 3 | 0 |
| NTechnology | 4 | 4 | 0 | 0 | 0 | 0 |
| NText | 3 | 6 | 3 | 3 | 0 | 0 |
| NTravelNetwork | 28 | 30 | 2 | 2 | 0 | 0 |
| NWar | 35 | 40 | 5 | 5 | 0 | 0 |
| **Total** | **1331** | **1576** | **309** | **267** | **22** | **20** |

```text
MISSING_REFERENCE_KEY = 257
OBSOLETE_KEY = 12
RENAMED_KEY = 20 (10 paires)
SCENARIO_DATE_DELTA = 1
STALE_VANILLA_VALUE = 19
UNKNOWN_REQUIRES_REVIEW = 0
INTENTIONAL_GAMEPLAY_DELTA_PROVEN = 0
```

Le manifeste CSV contient chaque delta, les valeurs, la classification, la décision et la preuve.

## 7. Deltas nécessaires au scénario 1776

| Delta | Référence | Fork | Requis | Preuve | Décision |
|---|---|---|---|---|---|
| `NGame.START_DATE` | `"1836.1.1"` | `"1776.1.1"` | YES | Unique commit d’import `b602804c...`, descripteur « 1776 », logique datée 1776 | Conserver 1776 |
| `NGame.END_DATE` | `"1936.1.1"` | identique | NO DELTA | Identique | Référence |
| `WORLD_EXTENTS_X/Y/Z` | `8192/24/3615` | identique | NO DELTA | Identique | Référence |
| `WATERLEVEL` | `1.74` | identique | NO DELTA | Identique | Référence |

`git log --follow` ne montre qu’un import initial du vieux fichier. Aucun autre delta ne possède une intention post-import démontrée.

## 8. Audit NMilitary

```text
REFERENCE_NMILITARY_KEYS = 165
FORK_NMILITARY_KEYS_BEFORE = 101
FORK_NMILITARY_MISSING_REFERENCE_KEYS_BEFORE = 76
FORK_NMILITARY_OBSOLETE_KEYS_BEFORE = 12
FORK_NMILITARY_CHANGED_COMMON_VALUES_BEFORE = 4
```

| Clé divergente | Fork | Référence | Action |
|---|---:|---:|---|
| `BLOCKADE_TARGET_STRENGTH_PER_TRADED_UNIT` | 0.1 | 0.05 | Référence |
| `BLOCKADE_TARGET_STRENGTH_PER_PRODUCED_UNIT` | 0.15 | 0.075 | Référence |
| `MILITARY_FORMATION_COMMAND_LIMIT_NO_COMMANDER` | 10 | 20 | Référence |
| `MILITARY_FORMATION_ORGANIZATION_SUPPLY_SHORTAGE_EFFECT_THRESHOLD` | 0.05 | 0.25 | Référence |

```text
INTENTIONAL_DESIGN_PROOF_FOR_4_DIFFERING_NMILITARY_VALUES = NO
FORK_NMILITARY_MISSING_REFERENCE_KEYS_AFTER = 0
FORK_NMILITARY_OBSOLETE_KEYS_AFTER = 0
EFFECTIVE_NMILITARY = REFERENCE_NMILITARY
```

L’annexe `CLEANUP2D3A_NMILITARY_KEY_AUDIT.csv` couvre les 177 clés de l’union : 85 identiques, 76 ajoutées, 12 retirées, 4 remplacées.

## 9. Clés de référence manquantes

Les 267 clés absentes sont restaurées par la baseline complète, dont 76 `NMilitary`. Elles comprennent `SAILORS_PER_ASSIGNMENT_SLOT = 100`, `SAILORS_PER_BUILDING_LEVEL = 1000`, les nouveaux déplacements de commanders, le bombardement, la présence navale, le resupply et les upgrades de formations. La liste exhaustive figure dans les deux CSV.

## 10. Clés obsolètes

Les 12 anciennes clés `NMilitary` retirées sont :

```text
BASE_BATTALION_CONVOY_COST
BLOCKADE_SEA_PRESENCE_TRESHOLD
BLOCKADE_TARGET_STRENGTH_PER_CONVOY
DEFAULT_ORDER_ADMIRAL
DEFAULT_ORDER_GENERAL
GENERAL_AUTO_TRAVEL_MAX_DAYS
GENERAL_INVALID_TRAVEL_DAYS
GENERAL_TRAVEL_AUTO_REASSIGN_INSTANTLY
GENERAL_TRAVEL_CAP
GENERAL_TRAVEL_OVERSEAS_SCALE
GENERAL_TRAVEL_PIXELS_TO_DAYS_SCALE
MAX_NUM_COMMANDERS_PER_FORMATION
```

Cinq sont des sources de renommage démontrées ; sept sont obsolètes. Aucun ancien paramètre n’est conservé par inertie.

## 11. Stratégie A ou B

```text
DEFINES_REPAIR_STRATEGY = B
STRATEGY_A_PARTIAL_OVERRIDE_PROVEN_SAFE = NO
STRATEGY_B_FULL_REFERENCE_PLUS_PROVEN_DELTAS = YES
```

Formule : fichier de référence 1.13.9 complet + `NGame.START_DATE = "1776.1.1"`. Le vieux fichier n’a pas servi de base.

## 12. Fichier(s) define final(aux)

```text
FINAL_DEFINES_PATH = common/defines/00_defines.txt
FINAL_DEFINES_SIZE = 204487
FINAL_DEFINES_SHA256 = 0C3765A9273EE1B34E05E5677DB82518E1296894BA428760EE4492848C415EFF
FINAL_DIFFERENCE_FROM_REFERENCE = NGame.START_DATE only
```

Livrables :

- `CLEANUP2D3A_DEFINES_REFERENCE_DELTA_MANIFEST.csv` : 309 deltas ;
- `CLEANUP2D3A_NMILITARY_KEY_AUDIT.csv` : 177 clés ;
- présent rapport.

## 13. Revalidation des constantes 2D-0

```text
REFERENCE_LAND_UNIT_MAX_MANPOWER = 1000
REFERENCE_COMBAT_UNITS_PER_LEVEL = 1
REFERENCE_NAVAL_ADMIN_CAPACITY = 1000
REFERENCE_NAVAL_ADMIN_EMPLOYMENT = 900 soldiers/sailors + 100 officers
REFERENCE_FRIGATE_CREW = 500
REFERENCE_SHIP_OF_THE_LINE_CREW = 800
LOCKED_2D0_CONSTANTS_MATCH_REFERENCE = YES
LAND_UNIT_MODEL_MATCHES_LOCKED_2D0 = YES
NAVAL_UNIT_MODEL_MATCHES_LOCKED_2D0 = YES
SAILOR_CONSTANTS_MATCH_REFERENCE = YES
```

Les neuf types terrestres actifs ont `max_manpower = 1000`. `pm_simple_sailor_recruitment` donne 900 + 100 emplois et `country_sailors_max_add = 1000`. Les crews sont 500 et 800. La condition d’arrêt n’est pas déclenchée. Aucune cible 2D-2 n’a été implémentée.

## 14. Références building_naval_base

Le vieux define avait `NAVAL_BASE_BUILDING = "building_naval_base"`. La référence a `NAVAL_ADMINISTRATION_BUILDING = "building_naval_administration"`, confirmé par `common/buildings/05_military.txt`.

```text
FINAL_DEFINES_LEGACY_BUILDING_NAVAL_BASE_REFERENCES = 0
NAVAL_BUILDING_IDENTIFIER_MATCHES_REFERENCE = YES
```

L’audit élargi a trouvé 13 références préexistantes hors defines, laissées intactes car hors périmètre :

- `common/ai_strategies/00_default_strategy.txt:5085` ;
- `events/agitators_events/revolution_events_02.txt:786,829,837` ;
- `events/brazil/culture_south_america.txt:444,518,631` ;
- `events/brazil/brazil_navy.txt:358,376` ;
- `events/dreadnought_hoax.txt:26,60` ;
- `events/russo_chinese_events.txt:347,351`.

```text
MOD_WIDE_PREEXISTING_LEGACY_NAVAL_BUILDING_REFERENCES = 13
BUILDING_HISTORY_FILES_CHANGED = 0
```

Elles constituent un risque runtime à surveiller, sans autoriser ici la modification d’événements ou de l’IA.

## 15. Vérification des protections

Hashes protégés initiaux :

```text
315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5  TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410  TECH_TREE_INDUSTRIAL_CHAINS.md
0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596  TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D  TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5  TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A  TECH_TREE_RESOURCE_CANDIDATES.csv
150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA  TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

```text
GAMEPLAY_FILES_CHANGED_OUTSIDE_DEFINES = 0
MILITARY_FORMATION_FILES_CHANGED = 0
BUILDING_HISTORY_FILES_CHANGED = 0
COUNTRY_HISTORY_FILES_CHANGED = 0
MAP_FILES_CHANGED = 0
STATE_REGION_FILES_CHANGED = 0
DIPLOMACY_FILES_CHANGED = 0
TECHNOLOGY_FILES_CHANGED = 0
LOCALISATION_FILES_CHANGED = 0
PROTECTED_TECH_FILES_CHANGED = 0
CLEANUP2C_GAMEPLAY_CHANGED = 0
BJECT_PATH_PRESENT = 0
CODEX_LAUNCHED_VICTORIA3 = NO
GIT_INDEX_MUTATED_BY_CODEX = NO
git diff --check = PASS
```

## 16. Risques runtime

1. Le jeu n’a pas été lancé ; parser et runtime restent à valider par l’utilisateur.
2. La stratégie B fixe volontairement la baseline complète sur 1.13.9 ; la compatibilité ultérieure est hors phase.
3. Les 13 références préexistantes à `building_naval_base` hors defines peuvent produire des erreurs.
4. La capacité marins dépend aussi du plein emploi.
5. Aucune formation, bâtiment historique ou cible 2D-2 n’a changé.

## 17. Checklist runtime utilisateur — une session

1. Lancer le jeu avec la configuration normale du mod.
2. Atteindre le menu sans crash.
3. Vérifier dans les logs frais l’absence de nouvelle erreur parser/define.
4. Démarrer une partie 1776.
5. Confirmer le 1er janvier 1776 et le chargement complet.
6. Vérifier une armée existante, son ordre et son organisation.
7. Vérifier une flotte existante, son ordre, sa présence/readiness et son déplacement.
8. Vérifier qu’une administration navale est reconnue.
9. Contrôler la capacité de marins et les deux constantes restaurées.
10. Rechercher toute erreur `building_naval_base` ou `building_naval_administration`.
11. Laisser passer quelques jours et surveiller supply et blocus.
12. Sauvegarder.
13. Recharger dans la même session.
14. Revérifier une armée, une flotte, une administration navale et les marins.
15. Quitter normalement.
16. Fournir les logs frais complets, notamment les lignes `define`, `NMilitary`, `sailor`, `blockade` et `building_naval_base`.

```text
RUNTIME_CHECKLIST_READY = YES
CODEX_LAUNCHED_VICTORIA3 = NO
```

## 18. Readiness CLEANUP-2D-3B

```text
REFERENCE_GAME_ROOT = C:\Games\Victoria 3
REFERENCE_GAME_VERSION = 1.13.9 (Matcha)
REFERENCE_BASELINE_ACCEPTED = YES
REFERENCE_DEFINES_PATH = C:\Games\Victoria 3\game\common\defines\00_defines.txt
REFERENCE_DEFINES_SHA256 = 398C364C108CE3FFA57FB25E000E3B8BCE50E1F882E37C36A358EEA34E4E1CF0
STEAM_INSTALLATION_USED_AS_REFERENCE = NO
HOTFIX_1_13_10_AUDITED = NO
HOTFIX_1_13_10_CHANGES_IMPLEMENTED = 0

DEFINES_REPAIR_STATIC = PASS
REFERENCE_NMILITARY_KEYS = 165
FORK_NMILITARY_KEYS_BEFORE = 101
FORK_NMILITARY_MISSING_REFERENCE_KEYS_BEFORE = 76
FORK_NMILITARY_OBSOLETE_KEYS_BEFORE = 12
FORK_NMILITARY_MISSING_REFERENCE_KEYS_AFTER = 0
FORK_NMILITARY_OBSOLETE_KEYS_AFTER = 0
SAILOR_CONSTANTS_MATCH_REFERENCE = YES
NAVAL_BUILDING_IDENTIFIER_MATCHES_REFERENCE = YES
LAND_UNIT_MODEL_MATCHES_LOCKED_2D0 = YES
NAVAL_UNIT_MODEL_MATCHES_LOCKED_2D0 = YES

STATIC_PREREQUISITES_FOR_CLEANUP_2D_3B = READY
RUNTIME_USER_SESSION = PENDING
READY_FOR_CLEANUP_2D_3B = NO_PENDING_RUNTIME_LOG_REVIEW
```

CLEANUP-2D-3B n’a pas été commencé.
