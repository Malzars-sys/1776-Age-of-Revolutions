# TECH-0P — 12-Era Runtime Validation

## Phase status

```text
PHASE = TECH-0P
MODE = TEMPORARY_TECHNICAL_PROTOTYPE
HISTORICAL_DESIGN = NONE
RUNTIME_HUMAN_REQUIRED = NO
CURRENT_STATUS = COMPLETE_CLEANUP_PASS
```

Ce document enregistre la validation statique, les résultats des runtimes humains et la suppression finale du harnais temporaire TECH0P.

## 1. Git baseline

Baseline capturée avant la création du prototype :

```text
BRANCH = post-2.3.0-log-cleanup
HEAD = 1e9d90e2450b16a37d8851e789d9e43db35414fb
WORKTREE_STATUS = ?? docs/reports/technology/
```

Le dossier de rapports technologie était déjà non suivi. Aucun document TECH-0 ou TECH-0R existant n'a été modifié.

## 2. Prototype créé

Le fork ne possédait aucun fichier `common/technology` : il héritait entièrement des cinq ères vanilla. Le prototype ajoute donc les définitions minimales `era_6` à `era_12`.

### Ères

| ID | Coût temporaire |
|---|---:|
| era_6 | 17 000 |
| era_7 | 20 000 |
| era_8 | 23 500 |
| era_9 | 26 500 |
| era_10 | 30 000 |
| era_11 | 35 000 |
| era_12 | 40 000 |

Les coûts VI–XI reprennent uniquement le modèle technique observé dans Tech & Res. Le coût XII de 40 000 produit des pénalités faciles à contrôler.

### Technologies

Onze technologies temporaires sont définies :

- Production : gap `era_1`, gap `era_7`, puis chaîne `era_10 -> era_11 -> era_12` ;
- Military : chaîne `era_10 -> era_11 -> era_12` ;
- Society : chaîne `era_10 -> era_11 -> era_12`.

Chaque technologie possède :

```text
ID_PREFIX = TECH0P_TEST_
ERA = EXPLICIT
CATEGORY = EXPLICIT
TEXTURE = EXISTING_VANILLA_TEXTURE
LOCALIZATION_ENGLISH = PRESENT
LOCALIZATION_FRENCH = PRESENT
PREREQUISITE = VALID
AI_WEIGHT = EXPLICIT
```

Les trois technologies `era_12` ont temporairement `ai_weight = 100`. Toutes les autres ont `ai_weight = 1`.

## 3. Contrôles statiques

```text
ERA_DEFINITIONS = 7
TECH_DEFINITIONS = 11
TECHS_WITH_VALID_PREREQUISITE = 11
TECHS_WITH_AI_WEIGHT = 11
UNIQUE_VANILLA_TEXTURES_REUSED = 10
MISSING_TEXTURES = 0
MISSING_TECH_LOCALIZATION_EN = 0
MISSING_TECH_LOCALIZATION_FR = 0
INVALID_TECH_GRANTS = 0
VANILLA_PRODUCTION_TECHS_IN_CASE_BASELINE = 57_OF_57
BRACE_BALANCE = PASS
STATIC_PROTOTYPE_RESULT = PASS
```

Ces contrôles ne prouvent pas que le moteur accepte `era_12`; ils prouvent seulement la cohérence interne du prototype avant lancement.

## 4. Harnais de test

Neuf décisions temporaires sont visibles. Chacune doit être utilisée sur une nouvelle partie ou après rechargement de la même sauvegarde propre, car une technologie recherchée ne peut pas être retirée par le harnais.

### Cas de pénalité

La cible est toujours `TECH0P_TEST_PRODUCTION_ERA12`.

| Décision | Technologies manquantes | Somme des distances | Coût attendu |
|---|---|---:|---:|
| `TECH0P_SETUP_CASE_A` | aucune dans les ères antérieures | 0 | 40 000 |
| `TECH0P_SETUP_CASE_B` | une en era_11 | 1 | 50 000 |
| `TECH0P_SETUP_CASE_C` | une en era_7 | 5 | 90 000 |
| `TECH0P_SETUP_CASE_D` | une en era_1 | 11 | 150 000 |
| `TECH0P_SETUP_CASE_E` | une en era_1, era_7 et era_11 | 17 | 210 000 |

Calcul :

```text
ERA_12_BASE_COST = 40000
AHEAD_FACTOR = 0.25

DISTANCE_1 = 0.25 * 40000 * 1 = 10000
DISTANCE_5 = 0.25 * 40000 * 5 = 50000
DISTANCE_11 = 0.25 * 40000 * 11 = 110000

CASE_A_EXPECTED_COST = 40000
CASE_B_EXPECTED_COST = 50000
CASE_C_EXPECTED_COST = 90000
CASE_D_EXPECTED_COST = 150000
CASE_E_EXPECTED_COST = 210000
```

### Joueur

- `TECH0P_SETUP_PLAYER_QUEUE` recherche uniquement les trois ancrages vanilla. Sélectionner ensuite une technologie d'ère XII avec « queue with unlocks » doit ajouter X, XI et XII.
- `TECH0P_SETUP_PLAYER_DIRECT` recherche X et XI dans les trois catégories et laisse XII directement sélectionnable.

### IA

`TECH0P_SETUP_AI` recherche les ancrages et les nœuds X/XI, puis applique pendant dix ans :

```text
country_weekly_innovation_add = 100000
country_weekly_innovation_max_add = 100000
country_tech_research_speed_mult = 10
```

Après avoir pris la décision, confier ce pays à l'IA. Le poids 100 des trois cibles XII doit permettre de vérifier sélection et complétion sans conclure sur un équilibrage réel.

#### Résultat du test IA avec pénalité normale

Le runtime humain de janvier à avril 1776 a confirmé que l'accélération était active et que l'IA recherchait normalement. Comme le pays restait massivement en retard sur les technologies anciennes, l'IA a préféré des technologies d'ère I malgré `ai_weight = 100` sur les trois cibles d'ère XII. Ce comportement correspond à la formule vérifiée :

```text
AI_TENDENCY_AFTER_AHEAD_PENALTY =
AI_TENDENCY / (1 + 5 * ahead_penalty / era_base_cost)

AI_RUNTIME_BONUS_ACTIVE = PASS
AI_RESEARCH_SYSTEM_ACTIVE = PASS
AI_AHEAD_PENALTY_BEHAVIOR = PASS
AI_PREFERS_OLD_TECHS_WHEN_MASSIVELY_BEHIND = PASS
```

Ce résultat n'est pas un échec de l'ère XII. La capacité isolée de l'IA à sélectionner une cible XII a ensuite été validée séparément.

#### Test IA final isolé

`TECH0P_SETUP_AI_FINAL` conserve les trois technologies XII à `ai_weight = 100`, accorde seulement leurs ancrages et leurs nœuds X/XI, puis applique le modificateur existant :

```text
country_weekly_innovation_add = 100000
country_weekly_innovation_max_add = 100000
country_tech_research_speed_mult = 10
```

Aucun catalogue de technologies vanilla n'est accordé par cette décision. Le moteur ne fournit pas de modificateur country permettant de neutraliser la pénalité d'avance. Le fichier séparé `common/defines/TECH0P_ai_final_test_defines.txt` applique donc l'override temporaire fiable :

```text
NTechnology = {
    TECH_AHEAD_OF_TIME_PENALTY_FACTOR = 0
}
```

Différence exacte : la valeur normale `0.25` devient `0` pour tous les pays et toutes les catégories tant que ce fichier est chargé. Cet override ne représente aucun comportement normal et sert exclusivement au dernier test de capacité IA. Retirer ce fichier restaure la valeur `0.25` déjà présente dans `common/defines/00_defines.txt`, identique à vanilla.

Le runtime final isolé a confirmé que l'IA sélectionne et termine `TECH0P_TEST_PRODUCTION_ERA12` lorsque cette pénalité est neutralisée :

```text
AI_RECOGNIZES_ERA_12 = PASS
AI_CAN_SELECT_ERA_12 = PASS
AI_CAN_COMPLETE_ERA_12 = PASS
```

## 5. Protocole runtime humain

### Session

```text
GAME_VERSION = release/1.13.9
GAME_HASH = afea32b87
MOD = 1776_Age_of_Revolutions_fork
NEW_GAME = YES
FRESH_LOG_ROTATION = YES
NORMAL_IN_GAME_QUIT = YES
SHUTDOWN = Quit: Quit from inside game
FINAL_TRANSITION = Game->Empty
```

### Chargement moteur

```text
ERA_12_LOADS = PASS
ERA_12_ID_ACCEPTED = PASS
TECH_ERA_12_LOADS = PASS
```

### GUI

```text
ERA_10_BADGE = PASS
ERA_11_BADGE = PASS
ERA_12_BADGE = PASS
ERA_12_NODE_RENDERING = PASS
ERA_12_PREREQUISITE_LINES = PASS
ERA_12_TOOLTIP = PASS
ERA_12_SELECTION = PASS
ERA_12_QUEUE = PASS
ERA_12_SCROLL_NAVIGATION = PASS
ERA_12_ZOOM = PASS
ERA_12_CLIPPING = PASS
ERA_12_OVERLAP = PASS
```

### Ahead penalty

| Cas | Expected cost | Runtime cost | Formula match |
|---|---:|---:|---|
| A | 40 000 | 40 000 | PASS |
| B | 50 000 | NOT_RUN | NOT_RUN |
| C | 90 000 | NOT_RUN | NOT_RUN |
| D | 150 000 | 150 000 | PASS |
| E | 210 000 | NOT_RUN | NOT_RUN |

```text
CASE_A_FORMULA_MATCH = PASS
CASE_D_FORMULA_MATCH = PASS
ERA_DISTANCE_11_SUPPORTED = PASS
LONG_DISTANCE_AHEAD_PENALTY = PASS
```

### Player research et sauvegarde

```text
RESEARCH_ERA_12 = PASS
WEEKLY_PROGRESS_APPLIED = PASS
SAVE_LOAD_ERA_12_PROGRESS = PASS

QUEUE_WITH_UNLOCKS_TO_ERA_12 = PASS
PREREQUISITE_CHAIN_X_XI_XII = PASS
QUEUE_ORDER = PASS
CANCEL_AND_REQUEUE = NOT_REPORTED
```

### AI research

```text
AI_RUNTIME_BONUS_ACTIVE = PASS
AI_RESEARCH_SYSTEM_ACTIVE = PASS
AI_AHEAD_PENALTY_BEHAVIOR = PASS
AI_PREFERS_OLD_TECHS_WHEN_MASSIVELY_BEHIND = PASS

AI_RECOGNIZES_ERA_12 = PASS
AI_CAN_SELECT_ERA_12 = PASS
AI_CAN_COMPLETE_ERA_12 = PASS
```

Avec `TECH_AHEAD_OF_TIME_PENALTY_FACTOR = 0` uniquement pour le test final isolé, l'IA a sélectionné et terminé la technologie Production d'ère XII. Ce test valide seulement l'acceptation d'une technologie `era_12` par le moteur et l'IA ; le comportement normal avec pénalité a été validé séparément.

### Performance et UX

```text
TECH_TREE_OPEN_TIME = NOT_MEASURED
PAN_RESPONSIVENESS = PASS
ZOOM_RESPONSIVENESS = PASS
LINES_RENDERING = PASS

439_TECH_STATIC_REFERENCE_FROM_TECH_RES = KNOWN
12_ERA_RUNTIME_RESULT = PASS
LIKELY_250_300_NODE_RISK = UNKNOWN
```

## 6. Logs à attribuer

```text
FRESH_LOGS_INSPECTED = debug/error/game/system
ERA_12_ENGINE_GUI_TECH_ERRORS = 0
TECH0P_DECISION_PARSER_ERRORS = 9
TECH0P_UTF8_BOM_WARNINGS = 6
PROTOTYPE_ERRORS = 9
PROTOTYPE_WARNINGS = 6
VISUAL_ISSUES = 0
```

Les neuf erreurs sont les neuf occurrences de `Unexpected token: base` causées par la forme temporaire `ai_chance = { base = 0 }` dans le fichier de décisions. Les six avertissements indiquent que les fichiers script TECH0P correspondants n'avaient pas de BOM. Le moteur a néanmoins chargé et exécuté les décisions nécessaires aux résultats observés.

Ces diagnostics appartiennent exclusivement au harnais jetable et disparaissent avec sa suppression. Aucun diagnostic frais ne met en cause `era_12`, ses technologies, le rendu GUI, les prérequis ou les textures réutilisées. Les autres diagnostics sans référence TECH0P ne sont pas attribués à cette phase.

## 7. Verdict final

```text
PHASE = TECH-0P

ERA_12_ENGINE_SUPPORT = PASS
ERA_12_GUI_SUPPORT = PASS
TWO_DIGIT_BADGES = PASS
PLAYER_RESEARCH = PASS
AI_RESEARCH = PASS
SAVE_LOAD = PASS
LONG_DISTANCE_AHEAD_PENALTY = PASS
LOG_RESULT = PASS_WITH_TEMPORARY_HARNESS_DIAGNOSTICS_REMOVED

HUMAN_RUNTIME_VERDICT = TWELVE_ERAS_SUPPORTED
TWELVE_ERAS_VERDICT = SUPPORTED
RECOMMENDED_ENGINE_ERA_LIMIT_FOR_1776 = 12
```

Ce verdict est strictement technique. Il ne constitue aucune recommandation historique ni aucun choix définitif de pacing ou d'architecture de l'arbre.

## 8. Fichiers temporaires TECH0P

```text
common/technology/eras/TECH0P_00_eras.txt
common/technology/technologies/TECH0P_test_technologies.txt
common/defines/TECH0P_ai_final_test_defines.txt
common/scripted_effects/TECH0P_test_effects.txt
common/decisions/TECH0P_test_decisions.txt
common/static_modifiers/TECH0P_test_modifiers.txt
localization/english/TECH0P_test_l_english.yml
localization/french/TECH0P_test_l_french.yml
```

```text
TEMPORARY_RUNTIME_FILES_CREATED = 8
TEMPORARY_RUNTIME_FILES_REMOVED_AT_CLOSURE = 8
TECH_AHEAD_OF_TIME_PENALTY_FACTOR_OVERRIDE_REMAINING = NO
ACTIVE_TECH_AHEAD_OF_TIME_PENALTY_FACTOR = 0.25
RUNTIME_TREE_TECH0P_FILES_REMAINING = 0
RUNTIME_TREE_TECH0P_REFERENCES_REMAINING = 0
```

Le présent rapport `TECH_0P_12_ERA_RUNTIME_VALIDATION.md`, exigé comme livrable de phase, est conservé. Aucun asset n'a été créé ou copié.
