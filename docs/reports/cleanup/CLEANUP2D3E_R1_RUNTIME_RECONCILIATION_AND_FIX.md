# CLEANUP-2D-3E-R1 — Réconciliation runtime et correctif

## Verdict

`CLEANUP2D3E_R1_STATIC_FIX = PASS`

Le save 3E du 3 janvier 1776 a été fondu et lu en mode diagnostic, sans modifier le save source et sans lancer Victoria 3. Les écarts réguliers majeurs viennent de concentrations dépassant le plafond de casernes de la loi militaire; les excès conscrits FRA/PRU/MARATH/RUS/CHI/BIC sont des recrutements de test utilisateur postérieurs au démarrage, pas des blocs pré-3D oubliés.

## Formule moteur 1.13.9

`OLD_3D_CONSCRIPTION_FORMULA = min(law_state_cap, ceil(workforce * state_conscription_rate_add * state_conscription_rate_mult / 1000))`

`ACTUAL_1_13_9_CONSCRIPTION_FORMULA = min(state_building_conscription_center_max_level_add, ceil(workforce * state_conscription_rate_add / CONSCRIPTION_CENTER_LEVEL_POPULATION_DIVISOR))`, avec `CONSCRIPTION_CENTER_LEVEL_POPULATION_DIVISOR = 1000` et un bataillon par niveau.

`ROOT_CAUSE_OF_3D_UNDERCOUNT = state_conscription_rate_mult a été appliqué à tort à la capacité de niveaux du centre; ce multiplicateur n'entre pas dans le Y natif affiché par Recruter des conscrits.`

La cible écrite est un total final: `min(DESIRED_2D2, TRUE_NATIVE_MAX)`, jamais ancien total + nouvelle cible. Aucun changement de loi, technologie, population ou modificateur artificiel.

| Pays | Cible 2D-2 | Plafond natif réel | Total scripté R1 |
|---|---:|---:|---:|
| GBR | 60 | 58 | 58 |
| FRA | 80 | 98 | 80 |
| SPA | 70 | 132 | 70 |
| PRU | 60 | 37 | 37 |
| RUS | 120 | 369 | 120 |
| USA | 80 | 118 | 80 |
| CHI | 150 | 804 | 150 |
| TUR | 150 | 279 | 150 |
| MARATH | 100 | 87 | 87 |
| BIC | 45 | 149 | 45 |
| MYS | 55 | 11 | 11 |

GBR atteint 58 sur une cible 60; les neuf États britanniques visibles totalisent 43 et les autres États directement GBR portent le plafond national à 58. USA atteint sa cible 80 sur un plafond 118.

## Formations et runtime

Les 255 formations scriptées sont conservées: 214 armées et 41 flottes. Les unités régulières restent à 2557; seules leurs régions de recrutement ont été redistribuées pour respecter les plafonds de casernes. L'Espagne passe d'une concentration 65+30 plafonnée à 25+25 à des recrutements répartis; la Russie, la Chine, la Prusse, les Ottomans et les autres violations mondiales suivent la même règle. Le dernier cas, Afghanistan, est réparti entre Balkh (23) et Hérat (22).

Le save contient 435 formations, dont 180 formations automatiques ou créées par l'utilisateur. Elles ne changent pas le périmètre statique des 255 formations. Les 13 formations qui dépendaient encore d'un nom automatique ont reçu une clé R1; elles ne peuvent donc pas être appariées par cette nouvelle clé au save 3E antérieur. `India Crown Detachment` a un potentiel scripté de 9 réguliers: elle n'est pas une formation initiale structurellement vide, même si le save 3E montre un recrutement non staffé.

| Pays | Réguliers 3B | Objets réguliers 3E | Réguliers avec manpower 3E | Conscrits scriptés 3D | Objets conscrits 3E | Diagnostic |
|---|---:|---:|---:|---:|---:|---|
| SPA | 95 | 50 | 30 | 65 | 0 | 45 réguliers rejetés par les deux concentrations plafonnées; conscrits 3D non matérialisés |
| RUS | 215 | 75 | 50 | 120 | 123 | 140 réguliers rejetés; trois conscrits ajoutés par le test utilisateur |
| TUR | 65 | 50 | 50 | 140 | 138 | 15 réguliers rejetés; deux conscrits 3D non matérialisés |

Le nombre d'objets distingue la création moteur de l'effectif réellement staffé (`current_manpower > 0`). La colonne formation par formation du CSV runtime donne le détail lorsque la clé de nom permet une corrélation certaine. Après R1, SPA est répartie sur des États directement espagnols pour 95 réguliers et 70 conscrits; RUS pour 215/120; TUR pour 65/150.

`REGULAR_TARGET_MISMATCHES_AFTER_ACCOUNTING_FOR_RECRUITMENT_QUEUE = 0` est un verdict statique R1: chaque recrutement final respecte désormais le plafond de son État. Il doit être confirmé par le runtime R2, car Codex n'a pas lancé le jeu.

Nouvelle-Espagne (SC1) n'a aucune formation parmi les 255 créées par 3B; son armée visible est générée automatiquement par le moteur et ne porte aucune clé localisable. R1 ne crée donc pas artificiellement une nouvelle formation pour la renommer. Joséon porte désormais `Joseon O Gunyeong`.

## Nommage et localisation

Les 87 libellés `Modeled 1776 Field Force` ont été remplacés par des noms nationaux propres ou romanisés; les 13 formations finales encore dépourvues de clé explicite ont également été nommées. Les noms propres restent identiques en EN/FR. Les sept noms russes sont en cyrillique. Les fichiers de localisation modifiés gardent leur BOM UTF-8. Le doublon `Bahriat_alMasqat` a été retiré des deux fichiers `phase_navy_3b_oman_fleet`; la définition historique unique reste active.

## Audit ciblé des logs 3E

- `RUSSIA_BUILDING_ERROR_PREEXISTING = YES`
- `RUSSIA_BUILDING_ERROR_LINE_TOUCHED_BY_3C = NO`
- `RUSSIA_BUILDING_ERROR_BLOCK_TOUCHED_BY_3C = NO`
- `RUSSIA_BUILDING_ERROR_CLASSIFICATION = PREEXISTING_KNOWN_LOG_DEBT`
- `SUBSAHARAN_SCOPE_ERROR_PREEXISTING = YES`
- `SUBSAHARAN_SCOPE_ERROR_LINE_TOUCHED_BY_3C = NO`
- `SUBSAHARAN_SCOPE_ERROR_BLOCK_TOUCHED_BY_3C = NO`
- `SUBSAHARAN_BUILDING_ERROR_CLASSIFICATION = PREEXISTING_KNOWN_LOG_DEBT`
- `INDIA_CREATE_CHARACTER_ERROR_TAG = BIC`
- `INDIA_CREATE_CHARACTER_ERROR_FORMATION = bengal_army`
- `INDIA_CREATE_CHARACTER_ERROR_CHARACTER = bane_bengal_gen`
- `INDIA_CREATE_CHARACTER_ERROR_PREEXISTING = YES`
- `INDIA_CREATE_CHARACTER_ERROR_AFFECTS_FORMATION_MATERIALIZATION = NO`
- `INDIA_CREATE_CHARACTER_ERROR_CLASSIFICATION = PREEXISTING_COMMANDER_DEBT_DEFER_2D4`
- `NEW_CONSCRIPT_PARSER_ERRORS_FOUND = 0`
- `NEW_SERVICE_TYPE_ERRORS_FOUND = 0`
- `NEW_FORMATION_PARSER_ERRORS_FOUND = 0`
- `PREEXISTING_GLOBAL_LOG_DEBT_LEFT_UNTOUCHED = YES`

La ligne russe fautive (`type` dans `add_ownership`) et le scope éthiopien sans enveloppe `region_state:ETH` existaient avant 3C; leurs blocs n'ont pas été modifiés par 3C. Ils n'expliquent pas les rejets militaires, entièrement reproduits par les plafonds de casernes. `maitland_gen`, `madras_army`, `aylmer_gen` et les BOM des anciennes localisations d'amiraux restent explicitement différés à 2D-4.

## Invariants finaux

- `TRUE_NATIVE_CONSCRIPTION_GLOBAL_CAPACITY = 4627`
- `FINAL_TARGET_CONSCRIPTS = 2146`
- `OLD_3D_UNDERCOUNTED_COUNTRIES = 208`
- `OLD_3D_OVERCOUNTED_COUNTRIES = 1`
- `EFFECTIVE_CONSCRIPT_TOTAL_MISMATCHES_AFTER = 0`
- `INITIAL_EMPTY_LAND_FORMATIONS_AFTER = 0`
- `GENERIC_MODELED_FORMATION_NAMES_AFTER = 0`
- `FORMATIONS_WITHOUT_EXPLICIT_NAME_AFTER = 0`
- `FORMATION_NAME_LOCALIZATION_DUPLICATES_AFTER = 0`
- `RUSSIAN_FORMATIONS_WITH_NON_RUSSIAN_NAMES_AFTER = 0`
- `LATIN_OR_CYRILLIC_NATIVE_LANGUAGE_NAMING_VIOLATIONS_AFTER = 0`
- `REGULAR_STATE_CAP_VIOLATIONS_AFTER = 0`
- `CONSCRIPT_STATE_CAP_VIOLATIONS_AFTER = 0`
- `REGULAR_TARGET_MISMATCHES_AFTER_ACCOUNTING_FOR_RECRUITMENT_QUEUE = 0`
- `USA_REGULAR = 20`
- `USA_SOL = 0`
- `PRU_COMBAT_NAVY = 0`
- `GBR_NAVY = 120`
- `GBR_FLEETS = 7`
- `EAST_INDIES_STATION_PRESENT_EXPECTED = YES`
- `EVERY_TARGET_FORMATION_HQ_VALIDATED_FOR_STARTING_COUNTRY_PRESENCE = YES`
- `IDENTICAL_REAL_ARMADA_DUPLICATE = 0`
- `DEFINES_CHANGED = 0`
- `BUILDING_HISTORY_CHANGED = 0`
- `TECH_CHANGED = 0`
- `LAW_CHANGED = 0`
- `POP_CHANGED = 0`
- `MAP_CHANGED = 0`
- `PROTECTED_TECH_FILES_CHANGED = 0`
- `BJECT_PATH_PRESENT = 0`
- `CODEX_LAUNCHED_VICTORIA3 = NO`
- `GIT_INDEX_MUTATED_BY_CODEX = NO`
- `git diff --check = PASS`

## Runtime utilisateur R2 condensé

1. Nouvelle partie au 1776-01-01, attendre la stabilisation des recrutements puis sauvegarder/recharger.
2. Vérifier SPA 95 réguliers / 70 conscrits, RUS 215 / 120, TUR 65 / 150 et l'absence de file rejetée permanente.
3. Vérifier USA 20 / 80 / 5 frégates / 0 SOL; GBR 49 / 58 / 7 flottes / 120 navires et East Indies Station présente.
4. Contrôler Joséon, les sept formations russes, l'absence de noms `Modeled`, et l'absence de formation terrestre 0+0 parmi les formations scriptées.
5. Joindre `debug.log`, `error.log`, `game.log` et les totaux après stabilisation.

STOP après R2. Ne pas commencer CLEANUP-2D-4.
