# TECH6B3H — Starting Tech Reconciliation Implementation

## A. Git checkpoint

- Branche de travail : `tech6b3h-starting-tech-reconciliation-implementation`.
- Checkpoint de départ : `ed8351d5daf3fdcf65a67643ff4ef87e95c0231d`.
- Branche précédente : `tech6b3g-starting-tech-reconciliation-audit`.
- Vanilla canonique relue : `C:\Games\Victoria 3\game`, Victoria 3 `1.13.11`.
- Date historique absolue : `1776-01-01`.
- Aucun commit ni push n'a été créé.

Le worktree était déjà fortement modifié avant TECH6B3H. Les hashes agrégés pré-phase des technologies, bâtiments, production methods, lois et GUI ont été conservés comme sentinelles; ils sont tous byte-identiques après l'implémentation.

La copie locale séparée du mod principal, `1776_Age_of_Revolutions_hotfix_source`, avait déjà été mise à jour depuis le Workshop `3617930953` après la demande utilisateur. Une nouvelle comparaison finale confirme 909 fichiers de chaque côté, 0 chemin exclusif et 0 différence de contenu; aucune réécriture supplémentaire du miroir n'était nécessaire.

## B. Fichiers modifiés

Le périmètre gameplay TECH6B3H comprend 107 chemins :

- 104 country histories effectives;
- suppression des deux anciens chemins concurrents `hbc - hubson bay company.txt` et `vnz - venezula.txt`;
- création du shadow `common/scripted_effects/00_starting_inventions.txt`.

Dans `common/history/countries`, le status final compte 68 fichiers suivis modifiés, 2 supprimés et 36 nouveaux. Ces 36 nouveaux chemins comprennent 35 shadows vanilla exacts et le nouveau chemin canonique `vnz - venezuela.txt`. La matrice AFTER donne le chemin effectif exact de chacune des 229 décisions.

Documentation et contrôle :

- `TECH6B3G_STARTING_TECH_RECONCILIATION_MATRIX.csv` : les huit arbitrages humains ont été remplacés par leurs décisions verrouillées;
- `TECH6B3G_STARTING_TECH_RECONCILIATION_REPORT.md` : addendum START-01/02/03 ajouté;
- `TECH6B3H_STARTING_TECH_RECONCILIATION_AFTER.csv` : 229 lignes de résultat effectif;
- `tools/tech6b3h_validate.py` : validateur reproductible;
- présent rapport.

## C. Méthode de reconstruction des tiers

Le fichier vanilla 1.13.11 a été shadowé au même chemin relatif. Chaque effet a été reconstruit comme une liste explicite, sans substitution globale hidden-vers-successor et sans toucher aux définitions technologiques.

| Tier | Technologies finales | Nombre |
|---|---|---:|
| 1 | frozen era-1 set + `atmospheric_engine`, `advanced_crop_rotations`, `precision_boring`, `scientific_naval_architecture`, `systematic_administrative_statistics` | 22 |
| 2 | frozen era-1 set + `atmospheric_engine`, `precision_boring` | 19 |
| 3 | profil réconcilié production/military/society, incluant `urbanization` temporaire | 16 |
| 4 | profil réconcilié production/military/society, incluant `urbanization` temporaire | 11 |
| 5 | profil réduit, incluant `urbanization` temporaire | 6 |
| 6 | `improved_husbandry`, `urbanization` | 2 |
| 7 | vide | 0 |

Les listes exactes et leur ordre sont vérifiés par le validateur. Aucun appel implicite `add_era_researched` ne reste.

## D. Traitement des 165 direct grants

Les décisions finales de la matrice, après incorporation des arbitrages utilisateur, sont :

| Action | Lignes directes |
|---|---:|
| `REPLACE_WITH_EARLIER_VISIBLE_TECH` | 75 |
| `REPLACE_WITH_VISIBLE_TECH` | 56 |
| `ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH` | 12 |
| `REMOVE_STARTING_GRANT` | 22 |
| `HUMAN_REVIEW_REQUIRED` | 0 |

Sur ces 165 entrées, 161 étaient actives dans l'overlay et ont été réconciliées; 4 lignes vanilla PRG étaient déjà inactives à cause du shadow Windows insensible à la casse `prg - Paraguay.txt`. Aucun grant historique supplémentaire n'a été ajouté.

## E. Traitement des 64 tier grants

| Action | Lignes tier |
|---|---:|
| `REPLACE_WITH_VISIBLE_TECH` | 18 |
| `REPLACE_WITH_EARLIER_VISIBLE_TECH` | 8 |
| `REMOVE_STARTING_GRANT` | 26 |
| `ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH` | 8 |
| `KEEP_HIDDEN_ALIAS_COMPATIBILITY_ONLY` | 4 |

Les 64 lignes ont toutes un résultat final vérifié. Les quatre seules lignes hidden conservées sont les occurrences tier 3 à 6 de `urbanization`.

## F. Traitement des 18 grants visibles hors compteur principal

Les 18 décisions visibles de TECH6B3G ont été appliquées pendant la reconstruction :

- tier 1 : retrait de `railways`, `general_staff`, `percussion_cap`; remplacement de `mechanical_tools` par `precision_boring`; conservation de `atmospheric_engine`;
- tier 2 : remplacement de `mechanical_tools` par `precision_boring`; conservation de `atmospheric_engine`;
- tier 3 : conservation de `shaft_mining`, `distillation`, `international_relations`, `medical_degrees`; retrait de `cotton_gin`, `romanticism`, `colonization`;
- tier 4 : conservation de `shaft_mining`, `distillation`, `international_relations`;
- tier 5 : conservation de `shaft_mining`.

Résultat : 18 décisions appliquées, 0 non classifiée.

## G. Résolution START-01 HBC

Les deux fichiers ont été comparés intégralement avant fusion. Le fichier autoritaire est désormais `hbc - hudson bay company.txt`; le fichier fautif `hubson` est supprimé.

Éléments conservés ou fusionnés :

- tier 4 et politique conservatrice;
- une seule capacité éducative : `institutionalized_scientific_exchange`;
- une seule capacité militaire : `regulated_small_arms`, fournie par le tier 4 réconcilié;
- `colonization`;
- lois canoniques du fichier `hudson`, avec les ajouts uniques non conflictuels `law_hereditary_bureaucrats`, `law_no_migration_controls`, `law_slave_trade`, `law_religious_schools`;
- institution scolaire niveau 1 et institution coloniale valide niveau 2;
- Industrialists au gouvernement avec idéologie colonialiste, Landowners au gouvernement et taxe sur le grain.

Les lois conflictuelles de l'ancien fichier `hubson` (`state_religion`, `cultural_exclusion`, `extraction_economy`) n'ont pas écrasé les choix canoniques `total_separation`, `racial_segregation`, `interventionism`. Le pseudo-ID d'institution `colonial_affairs` n'a pas été repris. `mandatory_service` est absent.

Résultat runtime rapporté par l'utilisateur : HBC se comporte normalement.

## H. Résolution START-02 VNZ

Le contenu gameplay du setup mod `venezula` a servi de base, puis a été placé sous le chemin canonique exact `vnz - venezuela.txt`. Ce shadow neutralise le setup vanilla concurrent et l'ancien chemin mal orthographié a été supprimé.

- un seul setup effectif VNZ;
- tier 4 uniquement;
- `institutionalized_scientific_exchange` comme unique capacité de connaissance issue du conflit;
- aucune attribution `empiricism` ou `academia`;
- aucun cumul tier 3 + tier 4.

Observation runtime utilisateur : le Venezuela n'existe pas comme pays au lancement 1776, car la Nouvelle-Grenade possède ses territoires. Cette absence est cohérente avec le setup historique et n'est pas une erreur TECH6B3H.

## I. Résolution START-03 PER

Dans le setup de la Sublime Zand (`PER`), `admiralty` a été remplacée exactement par `state_dockyard_systems`. Aucun autre grant naval n'a été ajouté.

Observation runtime utilisateur en debug : `state_dockyard_systems` est bien possédée par PER.

## J. Traitement de `add_era_researched = era_1`

Les appels implicites des tiers 1 et 2 ont été supprimés. Ils sont remplacés par le set visible era 1 exact observé pendant TECH6B3G, puis complétés uniquement par les anciennes lignes explicites validées. Un futur ajout de technologie era 1 ne changera donc plus silencieusement les starts.

```text
ADD_ERA_RESEARCHED_AFTER = 0
FROZEN_ERA_1_VISIBLE_SET = 17
```

## K. Traitement `urbanization`

`urbanization` reste uniquement dans les tiers 3, 4, 5 et 6, conformément aux quatre décisions `KEEP_HIDDEN_ALIAS_COMPATIBILITY_ONLY`. Aucun country history ne l'accorde directement.

Cette exception maintient temporairement les gates de `building_urban_center` et `building_construction_sector`. Les bâtiments et leurs gates n'ont pas été modifiés.

```text
URBANIZATION_TIER_GRANT_LINES = 4
URBANIZATION_DIRECT_COUNTRY_GRANTS = 0
URBANIZATION_ALIAS_REMOVED_GLOBALLY = NO
```

## L. Déduplication finale

L'expansion réelle des tiers a révélé 35 grants directs redondants dans 33 fichiers, principalement `regulated_small_arms` et trois occurrences de `systematic_administrative_statistics`. Les copies directes ont été supprimées lorsque le tier final fournissait déjà exactement la même technologie.

Le contrôle est effectué sur les 476 country history setups effectifs vanilla+mod :

```text
FINAL_DUPLICATE_VISIBLE_GRANTS = 0
FILES_WITH_EXPANDED_DUPLICATES = 0
UNKNOWN_EFFECTIVE_COUNTRY_GRANTS = 0
```

## M. Validation statique

`python tools/tech6b3h_validate.py` vérifie et régénère la matrice AFTER.

- 229 entrées : 165 directes + 64 tier;
- 221 entrées hidden actives supprimées ou remplacées;
- 4 lignes PRG déjà inactives par shadow casefold;
- 4 grants `urbanization` conservés;
- 18 décisions visibles tier validées;
- 285 IDs technologiques effectifs, tous les targets connus;
- 476 setups pays effectifs;
- HBC = 1 setup; VNZ = 1 setup;
- HBC `mandatory_service` après expansion = 0;
- PER `state_dockyard_systems` direct = 1;
- accolades et chaînes équilibrées;
- `git diff --check` = PASS, hors avertissements de normalisation LF/CRLF;
- hashes protégés technologies, bâtiments, PM, lois et GUI = PASS.

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

Victoria 3 a été lancé directement avec `victoria3.exe -debug_mode -mod=".../descriptor.mod"`. Le menu puis une partie 1776 ont été atteints sans crash. L'utilisateur a vérifié HBC et PER en debug et n'a constaté aucun bug d'interface.

Le passage contrôlé d'un mois complet n'a pas été explicitement confirmé; il n'est donc pas revendiqué.

```text
SMOKE_LAUNCH = PASS
GAME_1776_START = PASS
ONE_MONTH_SMOKE = NOT_RUN
```

## O. Logs

Les journaux frais `error.log`, `game.log` et `debug.log` ont été lus pendant que le jeu restait ouvert. Résultat du filtre ciblé :

- erreur `00_starting_inventions` : 0;
- erreur country history HBC/VNZ/PER : 0;
- unknown/duplicate technology attribuable : 0;
- malformed tier ou parser error attribuable : 0;
- erreur sur `institutionalized_scientific_exchange`, `regulated_small_arms` ou `state_dockyard_systems` : 0.

Deux avertissements lexer demandaient un BOM UTF-8 pour les nouveaux fichiers HBC et VNZ. Les deux fichiers ont été normalisés en `EF-BB-BF`; la validation statique repasse après cette correction. Leur disparition runtime sera observable au prochain lancement.

Les diagnostics restants sont hors périmètre et préexistants : localisations dupliquées, achievements invalides, appels GUI `interest_group_top`, lois initiales incompatibles de plusieurs tags, et erreur répétée `common/journal_entries/02_acre_dispute.txt:8`. Aucun ne référence un fichier ou objet TECH6B3H.

```text
PARSER_LOG_SMOKE = PASS
NEW_ATTRIBUTABLE_ERRORS = 0
```

## P. Écarts et différés

- distribution technologique nationale complète : différée jusqu'au gel de l'arbre;
- retrait global de `urbanization` : différé jusqu'à la validation des owners visibles des deux bâtiments;
- concrete/cement : non implémenté, conformément à la décision utilisateur; cette phase prépare seulement l'architecture future;
- one-month smoke : non revendiqué;
- avertissements BOM HBC/VNZ : corrigés statiquement, à confirmer au prochain lancement;
- diagnostics généraux des logs : documentés, non corrigés hors périmètre.

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
