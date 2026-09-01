# TECH6B3H â€” Starting Tech Reconciliation Implementation

## A. Git checkpoint

- Branche de travail : `tech6b3h-starting-tech-reconciliation-implementation`.
- Checkpoint de dÃ©part : `ed8351d5daf3fdcf65a67643ff4ef87e95c0231d`.
- Branche prÃ©cÃ©dente : `tech6b3g-starting-tech-reconciliation-audit`.
- Vanilla canonique relue : `C:\Games\Victoria 3\game`, Victoria 3 `1.13.11`.
- Date historique absolue : `1776-01-01`.
- Aucun commit ni push n'a Ã©tÃ© crÃ©Ã©.

Le worktree Ã©tait dÃ©jÃ  fortement modifiÃ© avant TECH6B3H. Les hashes agrÃ©gÃ©s prÃ©-phase des technologies, bÃ¢timents, production methods, lois et GUI ont Ã©tÃ© conservÃ©s comme sentinelles; ils sont tous byte-identiques aprÃ¨s l'implÃ©mentation.

La copie locale sÃ©parÃ©e du mod principal, `1776_Age_of_Revolutions_hotfix_source`, avait dÃ©jÃ  Ã©tÃ© mise Ã  jour depuis le Workshop `3617930953` aprÃ¨s la demande utilisateur. Une nouvelle comparaison finale confirme 909 fichiers de chaque cÃ´tÃ©, 0 chemin exclusif et 0 diffÃ©rence de contenu; aucune rÃ©Ã©criture supplÃ©mentaire du miroir n'Ã©tait nÃ©cessaire.

## B. Fichiers modifiÃ©s

Le pÃ©rimÃ¨tre gameplay TECH6B3H comprend 107 chemins :

- 104 country histories effectives;
- suppression des deux anciens chemins concurrents `hbc - hubson bay company.txt` et `vnz - venezula.txt`;
- crÃ©ation du shadow `common/scripted_effects/00_starting_inventions.txt`.

Dans `common/history/countries`, le status final compte 68 fichiers suivis modifiÃ©s, 2 supprimÃ©s et 36 nouveaux. Ces 36 nouveaux chemins comprennent 35 shadows vanilla exacts et le nouveau chemin canonique `vnz - venezuela.txt`. La matrice AFTER donne le chemin effectif exact de chacune des 229 dÃ©cisions.

Documentation et contrÃ´le :

- `TECH6B3G_STARTING_TECH_RECONCILIATION_MATRIX.csv` : les huit arbitrages humains ont Ã©tÃ© remplacÃ©s par leurs dÃ©cisions verrouillÃ©es;
- `TECH6B3G_STARTING_TECH_RECONCILIATION_REPORT.md` : addendum START-01/02/03 ajoutÃ©;
- `TECH6B3H_STARTING_TECH_RECONCILIATION_AFTER.csv` : 229 lignes de rÃ©sultat effectif;
- `tools/tech6b3h_validate.py` : validateur reproductible;
- prÃ©sent rapport.

## C. MÃ©thode de reconstruction des tiers

Le fichier vanilla 1.13.11 a Ã©tÃ© shadowÃ© au mÃªme chemin relatif. Chaque effet a Ã©tÃ© reconstruit comme une liste explicite, sans substitution globale hidden-vers-successor et sans toucher aux dÃ©finitions technologiques.

| Tier | Technologies finales | Nombre |
|---|---|---:|
| 1 | frozen era-1 set + `atmospheric_engine`, `advanced_crop_rotations`, `precision_boring`, `scientific_naval_architecture`, `systematic_administrative_statistics` | 22 |
| 2 | frozen era-1 set + `atmospheric_engine`, `precision_boring` | 19 |
| 3 | profil rÃ©conciliÃ© production/military/society, incluant `urbanization` temporaire | 16 |
| 4 | profil rÃ©conciliÃ© production/military/society, incluant `urbanization` temporaire | 11 |
| 5 | profil rÃ©duit, incluant `urbanization` temporaire | 6 |
| 6 | `improved_husbandry`, `urbanization` | 2 |
| 7 | vide | 0 |

Les listes exactes et leur ordre sont vÃ©rifiÃ©s par le validateur. Aucun appel implicite `add_era_researched` ne reste.

## D. Traitement des 165 direct grants

Les dÃ©cisions finales de la matrice, aprÃ¨s incorporation des arbitrages utilisateur, sont :

| Action | Lignes directes |
|---|---:|
| `REPLACE_WITH_EARLIER_VISIBLE_TECH` | 75 |
| `REPLACE_WITH_VISIBLE_TECH` | 56 |
| `ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH` | 12 |
| `REMOVE_STARTING_GRANT` | 22 |
| `HUMAN_REVIEW_REQUIRED` | 0 |

Sur ces 165 entrÃ©es, 161 Ã©taient actives dans l'overlay et ont Ã©tÃ© rÃ©conciliÃ©es; 4 lignes vanilla PRG Ã©taient dÃ©jÃ  inactives Ã  cause du shadow Windows insensible Ã  la casse `prg - Paraguay.txt`. Aucun grant historique supplÃ©mentaire n'a Ã©tÃ© ajoutÃ©.

## E. Traitement des 64 tier grants

| Action | Lignes tier |
|---|---:|
| `REPLACE_WITH_VISIBLE_TECH` | 18 |
| `REPLACE_WITH_EARLIER_VISIBLE_TECH` | 8 |
| `REMOVE_STARTING_GRANT` | 26 |
| `ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH` | 8 |
| `KEEP_HIDDEN_ALIAS_COMPATIBILITY_ONLY` | 4 |

Les 64 lignes ont toutes un rÃ©sultat final vÃ©rifiÃ©. Les quatre seules lignes hidden conservÃ©es sont les occurrences tier 3 Ã  6 de `urbanization`.

## F. Traitement des 18 grants visibles hors compteur principal

Les 18 dÃ©cisions visibles de TECH6B3G ont Ã©tÃ© appliquÃ©es pendant la reconstruction :

- tier 1 : retrait de `railways`, `general_staff`, `percussion_cap`; remplacement de `mechanical_tools` par `precision_boring`; conservation de `atmospheric_engine`;
- tier 2 : remplacement de `mechanical_tools` par `precision_boring`; conservation de `atmospheric_engine`;
- tier 3 : conservation de `shaft_mining`, `distillation`, `international_relations`, `medical_degrees`; retrait de `cotton_gin`, `romanticism`, `colonization`;
- tier 4 : conservation de `shaft_mining`, `distillation`, `international_relations`;
- tier 5 : conservation de `shaft_mining`.

RÃ©sultat : 18 dÃ©cisions appliquÃ©es, 0 non classifiÃ©e.

## G. RÃ©solution START-01 HBC

Les deux fichiers ont Ã©tÃ© comparÃ©s intÃ©gralement avant fusion. Le fichier autoritaire est dÃ©sormais `hbc - hudson bay company.txt`; le fichier fautif `hubson` est supprimÃ©.

Ã‰lÃ©ments conservÃ©s ou fusionnÃ©s :

- tier 4 et politique conservatrice;
- une seule capacitÃ© Ã©ducative : `institutionalized_scientific_exchange`;
- une seule capacitÃ© militaire : `regulated_small_arms`, fournie par le tier 4 rÃ©conciliÃ©;
- `colonization`;
- lois canoniques du fichier `hudson`, avec les ajouts uniques non conflictuels `law_hereditary_bureaucrats`, `law_no_migration_controls`, `law_slave_trade`, `law_religious_schools`;
- institution scolaire niveau 1 et institution coloniale valide niveau 2;
- Industrialists au gouvernement avec idÃ©ologie colonialiste, Landowners au gouvernement et taxe sur le grain.

Les lois conflictuelles de l'ancien fichier `hubson` (`state_religion`, `cultural_exclusion`, `extraction_economy`) n'ont pas Ã©crasÃ© les choix canoniques `total_separation`, `racial_segregation`, `interventionism`. Le pseudo-ID d'institution `colonial_affairs` n'a pas Ã©tÃ© repris. `mandatory_service` est absent.

RÃ©sultat runtime rapportÃ© par l'utilisateur : HBC se comporte normalement.

## H. RÃ©solution START-02 VNZ

Le contenu gameplay du setup mod `venezula` a servi de base, puis a Ã©tÃ© placÃ© sous le chemin canonique exact `vnz - venezuela.txt`. Ce shadow neutralise le setup vanilla concurrent et l'ancien chemin mal orthographiÃ© a Ã©tÃ© supprimÃ©.

- un seul setup effectif VNZ;
- tier 4 uniquement;
- `institutionalized_scientific_exchange` comme unique capacitÃ© de connaissance issue du conflit;
- aucune attribution `empiricism` ou `academia`;
- aucun cumul tier 3 + tier 4.

Observation runtime utilisateur : le Venezuela n'existe pas comme pays au lancement 1776, car la Nouvelle-Grenade possÃ¨de ses territoires. Cette absence est cohÃ©rente avec le setup historique et n'est pas une erreur TECH6B3H.

## I. RÃ©solution START-03 PER

Dans le setup de la Sublime Zand (`PER`), `admiralty` a Ã©tÃ© remplacÃ©e exactement par `state_dockyard_systems`. Aucun autre grant naval n'a Ã©tÃ© ajoutÃ©.

Observation runtime utilisateur en debug : `state_dockyard_systems` est bien possÃ©dÃ©e par PER.

## J. Traitement de `add_era_researched = era_1`

Les appels implicites des tiers 1 et 2 ont Ã©tÃ© supprimÃ©s. Ils sont remplacÃ©s par le set visible era 1 exact observÃ© pendant TECH6B3G, puis complÃ©tÃ©s uniquement par les anciennes lignes explicites validÃ©es. Un futur ajout de technologie era 1 ne changera donc plus silencieusement les starts.

```text
ADD_ERA_RESEARCHED_AFTER = 0
FROZEN_ERA_1_VISIBLE_SET = 17
```

## K. Traitement `urbanization`

`urbanization` reste uniquement dans les tiers 3, 4, 5 et 6, conformÃ©ment aux quatre dÃ©cisions `KEEP_HIDDEN_ALIAS_COMPATIBILITY_ONLY`. Aucun country history ne l'accorde directement.

Cette exception maintient temporairement les gates de `building_urban_center` et `building_construction_sector`. Les bÃ¢timents et leurs gates n'ont pas Ã©tÃ© modifiÃ©s.

```text
URBANIZATION_TIER_GRANT_LINES = 4
URBANIZATION_DIRECT_COUNTRY_GRANTS = 0
URBANIZATION_ALIAS_REMOVED_GLOBALLY = NO
```

## L. DÃ©duplication finale

L'expansion rÃ©elle des tiers a rÃ©vÃ©lÃ© 35 grants directs redondants dans 33 fichiers, principalement `regulated_small_arms` et trois occurrences de `systematic_administrative_statistics`. Les copies directes ont Ã©tÃ© supprimÃ©es lorsque le tier final fournissait dÃ©jÃ  exactement la mÃªme technologie.

Le contrÃ´le est effectuÃ© sur les 476 country history setups effectifs vanilla+mod :

```text
FINAL_DUPLICATE_VISIBLE_GRANTS = 0
FILES_WITH_EXPANDED_DUPLICATES = 0
UNKNOWN_EFFECTIVE_COUNTRY_GRANTS = 0
```

## M. Validation statique

`python tools/tech6b3h_validate.py` vÃ©rifie et rÃ©gÃ©nÃ¨re la matrice AFTER.

- 229 entrÃ©es : 165 directes + 64 tier;
- 221 entrÃ©es hidden actives supprimÃ©es ou remplacÃ©es;
- 4 lignes PRG dÃ©jÃ  inactives par shadow casefold;
- 4 grants `urbanization` conservÃ©s;
- 18 dÃ©cisions visibles tier validÃ©es;
- 285 IDs technologiques effectifs, tous les targets connus;
- 476 setups pays effectifs;
- HBC = 1 setup; VNZ = 1 setup;
- HBC `mandatory_service` aprÃ¨s expansion = 0;
- PER `state_dockyard_systems` direct = 1;
- accolades et chaÃ®nes Ã©quilibrÃ©es;
- `git diff --check` = PASS, hors avertissements de normalisation LF/CRLF;
- hashes protÃ©gÃ©s technologies, bÃ¢timents, PM, lois et GUI = PASS.

```text
STATIC_VALIDATION = PASS
UNCLASSIFIED_STARTING_GRANTS = 0
UNKNOWN_COUNTRY_TAGS = 0
UNKNOWN_TECH_IDS = 0
INVENTED_TECH_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0
TECH_TREE_DEFINITIONS_CHANGED = 0
TECH_PREREQUISITES_CHANGED = 0
TECH_ERAS_CHANGED = 0
```

## N. Smoke test

Victoria 3 a Ã©tÃ© lancÃ© directement avec `victoria3.exe -debug_mode -mod=".../descriptor.mod"`. Le menu puis une partie 1776 ont Ã©tÃ© atteints sans crash. L'utilisateur a vÃ©rifiÃ© HBC et PER en debug et n'a constatÃ© aucun bug d'interface.

Le passage contrÃ´lÃ© d'un mois complet n'a pas Ã©tÃ© explicitement confirmÃ©; il n'est donc pas revendiquÃ©.

```text
SMOKE_LAUNCH = PASS
GAME_1776_START = PASS
ONE_MONTH_SMOKE = NOT_RUN
```

## O. Logs

Les journaux frais `error.log`, `game.log` et `debug.log` ont Ã©tÃ© lus pendant que le jeu restait ouvert. RÃ©sultat du filtre ciblÃ© :

- erreur `00_starting_inventions` : 0;
- erreur country history HBC/VNZ/PER : 0;
- unknown/duplicate technology attribuable : 0;
- malformed tier ou parser error attribuable : 0;
- erreur sur `institutionalized_scientific_exchange`, `regulated_small_arms` ou `state_dockyard_systems` : 0.

Deux avertissements lexer demandaient un BOM UTF-8 pour les nouveaux fichiers HBC et VNZ. Les deux fichiers ont Ã©tÃ© normalisÃ©s en `EF-BB-BF`; la validation statique repasse aprÃ¨s cette correction. Leur disparition runtime sera observable au prochain lancement.

Les diagnostics restants sont hors pÃ©rimÃ¨tre et prÃ©existants : localisations dupliquÃ©es, achievements invalides, appels GUI `interest_group_top`, lois initiales incompatibles de plusieurs tags, et erreur rÃ©pÃ©tÃ©e `common/journal_entries/02_acre_dispute.txt:8`. Aucun ne rÃ©fÃ©rence un fichier ou objet TECH6B3H.

```text
PARSER_LOG_SMOKE = PASS
NEW_ATTRIBUTABLE_ERRORS = 0
```

## P. Ã‰carts et diffÃ©rÃ©s

- distribution technologique nationale complÃ¨te : diffÃ©rÃ©e jusqu'au gel de l'arbre;
- retrait global de `urbanization` : diffÃ©rÃ© jusqu'Ã  la validation des owners visibles des deux bÃ¢timents;
- concrete/cement : non implÃ©mentÃ©, conformÃ©ment Ã  la dÃ©cision utilisateur; cette phase prÃ©pare seulement l'architecture future;
- one-month smoke : non revendiquÃ©;
- avertissements BOM HBC/VNZ : corrigÃ©s statiquement, Ã  confirmer au prochain lancement;
- diagnostics gÃ©nÃ©raux des logs : documentÃ©s, non corrigÃ©s hors pÃ©rimÃ¨tre.

## Q. Bilan final

```text
TECH6B3H_STARTING_TECH_RECONCILIATION_IMPLEMENTATION = PASS

BRANCH = tech6b3h-starting-tech-reconciliation-implementation

VANILLA_CANONICAL_VERSION = 1.13.11
REFERENCE_DATE = 1776-01-01

INPUT_STARTING_GRANTS = 229
INPUT_DIRECT_COUNTRY_GRANTS = 165
INPUT_SCRIPTED_TIER_GRANTS = 64

START_01_HBC_RESOLVED = YES
START_02_VNZ_RESOLVED = YES
START_03_PER_RESOLVED = YES

HBC_EFFECTIVE_SETUP_COUNT = 1
VNZ_EFFECTIVE_SETUP_COUNT = 1

HBC_MANDATORY_SERVICE_AFTER = 0
PER_STATE_DOCKYARD_SYSTEMS_AFTER = 1

HIDDEN_STARTING_GRANTS_REMOVED = 221
HIDDEN_STARTING_GRANTS_RETAINED_FOR_RUNTIME_COMPATIBILITY = 4

FINAL_DUPLICATE_VISIBLE_GRANTS = 0

UNCLASSIFIED_STARTING_GRANTS = 0
UNKNOWN_COUNTRY_TAGS = 0
UNKNOWN_TECH_IDS = 0
INVENTED_TECH_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0

NEW_COUNTRY_TECH_DISTRIBUTION_ADDED = 0
HISTORICAL_COMPLETION_PASS_PERFORMED = NO

TECH_TREE_DEFINITIONS_CHANGED = 0
TECH_PREREQUISITES_CHANGED = 0
TECH_ERAS_CHANGED = 0

URBANIZATION_ALIAS_REMOVED_GLOBALLY = NO

NEW_ATTRIBUTABLE_ERRORS = 0

SMOKE_LAUNCH = PASS
ONE_MONTH_SMOKE = NOT_RUN

GAMEPLAY_CHANGED_FILES = 107

REPORT_CREATED = YES

COMMIT = NO
PUSH = NO

NEXT_PHASE = STOP_AFTER_RECONCILIATION

STARTING_TECH_FULL_DISTRIBUTION = DEFERRED_UNTIL_TECH_TREE_FROZEN
```
