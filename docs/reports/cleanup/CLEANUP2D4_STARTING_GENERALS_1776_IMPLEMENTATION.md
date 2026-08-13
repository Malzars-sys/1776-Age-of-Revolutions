# CLEANUP-2D-4 — Starting Generals 1776

## Résultat

Le paquet de recherche fermé a été implémenté sur les 214 formations terrestres post-2D-3. Chaque formation possède désormais exactement un général créé et transféré par un couple de scopes résoluble.

```text
CLEANUP2D4_STATIC = PASS
LAND_FORMATIONS = 214
LAND_TAGS = 175
NAMED_HISTORICAL_ASSIGNMENTS = 18
PROCEDURAL_ASSIGNMENTS = 196
FORMATIONS_WITH_EXACTLY_ONE_GENERAL = 214
FORMATIONS_WITHOUT_GENERAL = 0
FORMATIONS_WITH_MULTIPLE_GENERALS = 0
```

Les 18 identités fixes sont exactement celles du MASTER. Les 196 autres lignes utilisent le template actif `default` avec `is_general = yes`, sans nom fixe, sans `historical = yes`, sans âge, date de naissance, office, idéologie, trait ou biographie ajouté par 2D-4.

Le template `default` du mod génère un nom culturel, une culture primaire appropriée, l'âge, le groupe d'intérêt, le rang de commandement, le portrait et les traits. Il fournit donc la génération culturelle/native demandée sans fabriquer une identité historique.

## Baseline Git et état de travail

```text
BRANCH_INITIAL = cleanup-post-release
HEAD_INITIAL = 5cc8d8b572fedbfa0e5006e56f48422d8f521894
HEAD_FINAL = 5cc8d8b572fedbfa0e5006e56f48422d8f521894
COMMIT_CREATED = NO
PUSH_PERFORMED = NO
GIT_INDEX_MUTATED_BY_CODEX = NO
STAGED_FILES = 0
```

Le working tree contenait avant 2D-4 des documents modifiés/non suivis et les sept fichiers technologiques protégés non suivis. Ils ont été préservés.

## Paquet de recherche intégré

Les six fichiers fournis ont été copiés sans altération dans leurs emplacements canoniques :

- `docs/research/military/GENERALS_1776_MASTER.csv`;
- `docs/research/military/GENERALS_1776_SOURCES.md`;
- `docs/research/military/GENERALS_1776_COMMAND_STRUCTURE_NOTES.md`;
- `docs/research/military/GENERALS_1776_REJECTED_CANDIDATES.csv`;
- `docs/research/military/CLEANUP2D4_GENERALS_1776_RESEARCH_COMPLETE.md`;
- `docs/prompts/CLEANUP2D4_GENERALS_CODEX_PROMPT.md`.

Le MASTER contient 214 couples `(tag, formation)` uniques. Les 214 ont une correspondance exacte dans le setup post-2D-3 et une décision d'implémentation. Aucune nouvelle recherche ou identité extérieure n'a été ajoutée.

## Matrice AVANT/APRÈS

La matrice complète se trouve dans :

`docs/research/military/GENERALS_1776_IMPLEMENTATION_MATRIX.csv`

Elle consigne pour chaque formation : scopes avant, commandants avant, décision MASTER, action, scope de formation après, scope de personnage après, commandant après, caractère historique ou procédural, transfert et verdict statique.

```text
MATRIX_ROWS = 214
MATRIX_PASS = 214
FORMATIONS_WITH_COMMANDERS_BEFORE = 31
FORMATIONS_WITHOUT_COMMANDERS_BEFORE = 183
FORMATIONS_WITHOUT_SCOPE_BEFORE = 181

ADD_NAMED = 11
ADD_PROCEDURAL = 172
REPLACE_LEGACY_WITH_NAMED = 7
REPLACE_LEGACY_WITH_PROCEDURAL = 24
```

Les 33 formations qui possédaient déjà un ou plusieurs scopes les conservent intégralement. Un scope `cleanup2d4_formation_NNN` unique a été ajouté aux 181 autres. Pour les six formations possédant plusieurs alias de scope, le premier scope existant est utilisé comme cible et tous les alias sont conservés.

## Affectations historiques fixes

| Tag | Formation | Général |
|---|---|---|
| PLC | `cleanup2d3e_r1_plc_land_1` | Franciszek Ksawery Branicki |
| AUS | `cleanup2d3b_aus_land_3` | Andreas Hadik |
| AUS | `cleanup2d3b_aus_land_1` | Franz Moritz von Lacy |
| GBR | `cleanup2d3b_gbr_land_2` | William Howe |
| RUS | `cleanup2d3b_rus_land_4` | Pyotr Rumyantsev |
| SPA | `cleanup2d3b_spa_land_2` | Antonio Ricardos |
| SPA | `cleanup2d3b_spa_land_1` | Alejandro O'Reilly |
| USA | `cleanup2d3b_usa_land_1` | George Washington |
| PAN | `FaujiKhas` | Jassa Singh Ahluwalia |
| BIC | `Bengal_Army` | John Clavering |
| MARATH | `cleanup2d3b_marath_land_2` | Haripant Phadke |
| MARATH | `cleanup2d3b_marath_land_1` | Tukoji Holkar |
| GWA | `GwaliorArmy` | Mahadji Shinde |
| MYS | `cleanup2d3b_mys_land_2` | Hyder Ali |
| TRA | `TravancoreArmy` | Eustachius De Lannoy |
| MUG | `MughalArmy` | Mirza Najaf Khan |
| BUR | `tatmadaw` | Maha Thiha Thura |
| SIA | `cleanup2d3b_sia_land_1` | Chao Phraya Chakri (Thongduang) |

Les commentaires d'implémentation citent uniquement l'identifiant MASTER, la formation de gameplay et la décision. Ils ne prétendent pas qu'une abstraction `HIGHER_COMMAND_ABSTRACTION` ou `NAMED_MILITARY_OFFICEHOLDER` correspondait littéralement à une formation portant le nom généré en 2D-3.

## Nettoyage de la dette legacy terrestre

```text
LEGACY_GENERAL_CHARACTER_BLOCKS_REMOVED = 49
LEGACY_LAND_TRANSFER_BLOCKS_REMOVED = 50
LEGACY_FORMATIONS_REPLACED = 31
```

Le détail exact avant/après se trouve dans la matrice. Les dettes explicitement exigées sont closes :

- GBR : `colborne_gen` et le transfert orphelin `aylmer_gen` sont absents;
- BIC : `maitland_gen` et la cible inexistante `madras_army` sont absents;
- PRU : Wilhelm von Krauseneck, Helmuth von Moltke et Hans Ernst Karl von Zieten sont remplacés par trois généraux procéduraux distincts;
- RUS : aucun Suvorov n'est créé au 1er janvier 1776;
- FRA : Rochambeau n'est pas introduit;
- CON : Salah Bey n'est pas transformé en général.

La recherche des candidats rejetés et des scopes legacy interdits dans les huit fichiers de formations retourne zéro occurrence.

## Localisation

Deux fichiers nouveaux contiennent les noms fixes :

- `localization/english/cleanup2d4_generals_l_english.yml`;
- `localization/french/cleanup2d4_generals_l_french.yml`.

Chaque langue contient 36 clés, soit prénom et nom pour chacune des 18 identités. Les valeurs reproduisent exactement le nom recommandé par le MASTER.

```text
EN_LOCALIZATION_KEYS = 36
FR_LOCALIZATION_KEYS = 36
MISSING_LOCALIZATION_KEYS = 0
DUPLICATE_LOCALIZATION_KEYS = 0
```

## Fichiers gameplay modifiés

Liste exacte :

- `common/history/military_formations/00_military_formations_europe.txt`;
- `common/history/military_formations/01_military_formations_north_america.txt`;
- `common/history/military_formations/02_military_formations_south_america.txt`;
- `common/history/military_formations/03_military_formations_north_africa.txt`;
- `common/history/military_formations/04_military_formations_middle_east.txt`;
- `common/history/military_formations/05_military_formations_india.txt`;
- `common/history/military_formations/06_military_formations_asia.txt`;
- `common/history/military_formations/07_military_formations_subsaharan_africa.txt`;
- les deux fichiers de localisation 2D-4 ci-dessus.

Aucun fichier de pays, loi, diplomatie, bâtiment, technologie, population, carte, ownership ou define n'a été modifié.

## Contrôle des scopes et invariants

Un parseur à accolades équilibrées a relu le setup avant/après et le MASTER.

```text
MASTER_FORMATIONS_MATCHED = 214/214
FORMATION_SCOPES_DUPLICATED = 0
CHARACTER_SCOPES_DUPLICATED = 0
GENERAL_TRANSFERS_RESOLVABLE = 214/214
TRANSFER_TO_NONEXISTENT_FORMATION_SCOPE = 0
TRANSFER_FROM_NONEXISTENT_CHARACTER_SCOPE = 0
FIXED_HISTORICAL_GENERAL_ABSENT_FROM_MASTER = 0
REJECTED_CANDIDATE_REINTRODUCED = 0

LAND_FORMATION_COUNT_BEFORE = 214
LAND_FORMATION_COUNT_AFTER = 214
FLEET_COUNT_BEFORE = 41
FLEET_COUNT_AFTER = 41

REGULAR_TOTAL_BEFORE = 2557
REGULAR_TOTAL_AFTER = 2557
CONSCRIPT_TOTAL_BEFORE = 1705
CONSCRIPT_TOTAL_AFTER = 1705
NAVAL_TOTAL_BEFORE = 370
NAVAL_TOTAL_AFTER = 370
EMPTY_FORMATIONS_AFTER = 0
```

La projection structurelle de chaque formation — type, nom, HQ, unités régulières, conscrits, États, types, `count`, navires et options de mobilisation — est identique avant/après : zéro divergence sur 255 formations.

## Protection navale et technologique

Les comparaisons brutes contre HEAD donnent :

```text
FLEET_BLOCKS_EXACTLY_UNCHANGED = 41/41
ADMIRAL_CHARACTER_BLOCKS_EXACTLY_UNCHANGED = 5/5
ADMIRAL_TRANSFER_BLOCKS_EXACTLY_UNCHANGED = 5/5
FLEET_OR_ADMIRAL_MODIFIED = 0
```

Les sept fichiers technologiques protégés conservent leurs empreintes SHA-256 de référence, restent non suivis et non indexés :

```text
PROTECTED_TECH_FILES_CHANGED = 0
PROTECTED_TECH_FILES_STAGED = 0
```

## Validation statique finale

```text
CLEANUP2D4_STATIC = PASS
BRACE_PARSE = PASS
MASTER_COVERAGE = PASS
GENERAL_ATTACHMENT_COVERAGE = PASS
SCOPE_INTEGRITY = PASS
REJECTED_CANDIDATE_AUDIT = PASS
LOCALIZATION_EN_FR = PASS
LAND_FORMATION_INVARIANTS = PASS
FLEET_ADMIRAL_PROTECTION = PASS
TECH_PROTECTION = PASS
git diff --check = PASS
```

## Runtime QA condensé

```text
RUNTIME_EXECUTED_BY_CODEX = NO
RUNTIME_STATUS = PENDING_SINGLE_USER_SESSION
```

Plan préparé pour une seule ouverture de Victoria 3 :

1. lancer une nouvelle partie au 1er janvier 1776 et attendre la stabilisation;
2. contrôler USA, GBR, AUS, RUS, SPA, PLC, BIC, MYS, PAN, MARATH, GWA, TRA, MUG, SIA et BUR;
3. contrôler des cas procéduraux répartis entre Europe, Afrique et Asie : PRU, FRA, CIR, TUR, CHI, ASH et BRG;
4. confirmer un général par formation inspectée et l'absence de changement d'amiral;
5. surveiller `create_character`, `transfer_to_formation`, scopes inexistants et clés de localisation brutes dans les logs;
6. sauvegarder, recharger dans la même session, puis reconfirmer USA, GBR, SPA, BIC, CHI et un cas africain procédural.

Aucune seconde relance du jeu n'est nécessaire si cette session passe.
