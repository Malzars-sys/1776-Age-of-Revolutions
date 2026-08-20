# LOG-CLEANUP-10 — Runtime residuals & country-law consolidated audit

## État

`LOG_CLEANUP_10 = PASS`

Cette phase est un audit d’attribution et de regroupement uniquement. Aucun fichier gameplay n’est modifié. Les 8 identités runtime canoniques LOG-9 sont attribuées, les 113 diagnostics country-law historiques sont reconstruits exactement et l’ensemble est réduit à cinq lots correctifs raisonnables.

## Upstream Tsar 2.3.0.1

- `TSAR_UPSTREAM_VERSION_AUDITED = 2.3.0.1`
- `GLOBAL_UPSTREAM_MERGE_REQUIRED = NO`
- `UPSTREAM_TECHNICAL_FIX_REQUIRED = NO`

L’audit upstream canonique n’a pas été refait. Aucun fichier Tsar n’est importé et le diplomatic play Irak–Perse reste intact.

## Prévol Git et baseline

- `BRANCH = post-2.3.0-log-cleanup`
- `HEAD = 26272d37567c444f444466a1a226adc0a10b5139`
- `HEAD_SUBJECT = Fix residual Caucasus and modifier API diagnostics`
- `WORKTREE_INITIAL = CLEAN`
- `INDEX_INITIAL = EMPTY`
- `CONFIRMED_FORK_ERRORS_BEFORE = 0`
- `LOG_CLEANUP_9 = PASS`
- `VICTORIA_3_VERSION = release/1.13.9`
- `VICTORIA_3_HASH = afea32b87`
- `VANILLA_ROOT = C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game`

Les inventaires LOG-CLEANUP-1/4, les livrables LOG-CLEANUP-9 et toutes les rotations fraîches LOG-9 ont été relus. Les familles déjà fermées ne sont pas rouvertes.

## Runtime LOG-9 utilisé

- date : `2026-08-20` ;
- session : `17:33:20` à environ `17:40:55` ;
- scénario : nouvelle partie 1776, Pays-Bas, environ une semaine ;
- résultat humain : aucun crash, aucune clé brute observée, partie jouable ;
- fermeture : `Quit: Quit from inside game`, puis `Transition Game->Empty`.

Les occurrences sont comptées dans `error.5.log` à `error.log`. Les miroirs `game.*.log` ne sont pas recomptés.

## Partie A — huit identités runtime

### Réconciliation de la canonisation

`NEW_RUNTIME_IDENTITIES_IN_SCOPE = 8`

`NEW_RUNTIME_IDENTITIES_ATTRIBUTED = 8`

Le résumé LOG-9 imprimait six représentants de ligne et indiquait deux identités non imprimées. La reconstruction identifie ces deux dernières à :

- `common/journal_entries/02_south_america_migration.txt:154` ;
- `common/journal_entries/07_american_mod_jes.txt:118`.

Le balayage brut de toutes les rotations trouve également dix manifestations path/line associées à la même famille géographique :

| Manifestations associées | Occurrences |
|---|---:|
| `common/dynamic_country_names/00_dynamic_country_names.txt:1385,1410,1435` | 18 |
| `common/journal_entries/01_natural_borders_of_france.txt:92,93,94` | 75 |
| `common/journal_entries/01_natural_borders_of_france.txt:106,107,108` | 105 |
| `common/journal_entries/06_cuba.txt:225` | 1 |
| Total associé | 199 |

Ainsi, le comptage physique brut donne 18 couples message/path/line, tandis que le compteur canonique demandé reste 8. Les dix manifestations associées ne sont ni masquées ni promues artificiellement dans le pool de 121 : elles sont attribuées à la même cause et incluses dans le sweep du lot géographique LOG11-B01.

### Résultat d’attribution

| Groupe | Identités canoniques | Cause | Attribution |
|---|---:|---|---|
| `RR-G01_LEGACY_GEOGRAPHIC_COMPARISON` | 7 | comparaison moderne d’un scope state/capital à un ancien objet `sr:` supprimé | `FORK_ATTRIBUTABLE_FIXABLE` |
| `RR-G02_LAW_VARIANT_PARENT_API` | 1 | `has_law_or_variant` reçoit `law_homesteading`, un variant, au lieu de son parent | `FORK_ATTRIBUTABLE_FIXABLE` |

- `NEW_RUNTIME_FORK_ERRORS = 8`
- `NEW_RUNTIME_NON_ACTIONABLE = 0`
- `NEW_RUNTIME_NEEDS_MORE_RUNTIME = 0`
- `NEW_RUNTIME_UNKNOWN = 0`

### Géographie legacy

La même règle prouvée dans LOG-CLEANUP-6/7 s’applique : sur un scope d’État, l’ancienne comparaison `region = sr:region_x` devient un prédicat `is_in_geographic_region` utilisant l’objet géographique qui conserve l’empreinte historique.

Les homologues locaux vanilla 1.13.9 confirment notamment :

- Madras/Bombay/Bengal : `geographic_region_*_old` dans `00_dynamic_country_names.txt` ;
- confédération germanique : `geographic_region_german_confederation` et `any_state_in_german_confederation` ;
- Amérique centrale : `geographic_region_central_america` ;
- Ibérie : `geographic_region_iberia_old` ;
- Dixie, Perse et région arabe : objets `geographic_region_*_old` définis avec les empreintes des anciennes strategic regions.

Les sept identités géographiques canoniques totalisent 14 612 occurrences. Avec les 199 manifestations associées, la famille géographique fraîche totalise 14 811 occurrences. L’occurrence n’est jamais confondue avec l’identité.

### Landowners ligne 459

- `LANDOWNERS_459_PREEXISTED_BEFORE_LOG8 = YES`
- `LANDOWNERS_459_ROOT_CAUSE = law_homesteading is a variant; has_law_or_variant expects law_peasant_proprietorship, its parent`
- `LANDOWNERS_459_FORK_ATTRIBUTION = FORK_ATTRIBUTABLE_FIXABLE`

La ligne actuelle est déjà présente à l’identique dans le commit `820b1c2`, parent de LOG-CLEANUP-8, et son blame remonte à l’import initial `b602804`. LOG-CLEANUP-8 a modifié un autre bloc Landowners. Vanilla 1.13.9 emploie exactement `has_law_or_variant = law_type:law_peasant_proprietorship` dans le bloc farmer homologue.

## Partie B — 113 country-law historiques

### Reconstruction exacte

- `COUNTRY_LAW_HISTORICAL_IDENTITIES_IN_SCOPE = 113`
- `COUNTRY_LAW_HISTORICAL_IDENTITIES_RECONSTRUCTED = 113`
- `COUNTRY_LAW_HISTORICAL_OCCURRENCES = 113`
- génération : `release_2.3.0_20260814_184942` ;
- timestamp historique : `2026-08-14T19:00:05+02:00` ;
- sources : 110 lignes `error.log`, 3 lignes `error.1.log`.

Les noms à espaces de Hudson’s Bay Company et Russian-American Company sont reparsés depuis `raw_message`; ils ne reposent pas sur la normalisation historique imparfaite. Chaque ligne possède un identifiant stable `CL-001` à `CL-113`.

### Observation dans le runtime LOG-9

- `COUNTRY_LAW_IDENTITIES_REPRODUCED_CURRENT = 0`
- `COUNTRY_LAW_IDENTITIES_NOT_REPRODUCED_CURRENT = 113`

Cette absence ne vaut pas correction. Les six rotations fraîches ont été saturées par la boucle Natural Borders et ne conservent que la fin de session, essentiellement `17:40:32` à `17:40:38`; les validations country-law se produisent normalement à l’initialisation antérieure de la nouvelle partie. La matrice marque donc chaque ligne `current_reproduced = NO`, sans transformer ce `NO` en preuve de disparition.

L’attribution reste possible sans nouveau runtime : le runtime historique est déjà un runtime Victoria 3 1.13.9, et aucun fichier `common/history/countries` ou `common/history/global` impliqué n’a changé depuis la baseline LOG-CLEANUP-1. Le seul diff de loi entre `a7055c1` et HEAD est la migration indépendante `country_law_enactment_time_mult` vers `country_law_enactment_speed_mult` dans Merchant Banking/autocracy injection.

### Trois causes racines

`COUNTRY_LAW_ROOT_CAUSE_GROUPS = 3`

| Groupe | Diagnostics | Structure | Attribution | Correction sûre au stade audit | Runtime après patch |
|---|---:|---|---|---|---|
| `CL-G01_TECH_PREREQUISITES` | 105 | loi active explicite ou implicite sans la technologie exigée par la définition 1.13.9 | `FORK_ATTRIBUTABLE_SEMANTIC_REWRITE` | décision historique par pays : loi fallback explicite ou technologie réellement justifiée | YES |
| `CL-G02_VARIANT_VISIBILITY` | 7 | parent/variant non visible pour le pays, sujet, culture ou espace concerné | `FORK_ATTRIBUTABLE_SEMANTIC_REWRITE` | choisir le parent ou le variant historiquement et contextuellement valide | YES |
| `CL-G03_CONFLICTING_LAWS` | 1 | Bavaria active Traditionalism alors que Per-Capita Taxation est incompatible | `FORK_ATTRIBUTABLE_SEMANTIC_REWRITE` | décider la paire économique/fiscale 1776 cohérente | YES |

Le groupe technologie contient 28 activations explicites, 69 valeurs implicites associées à un fichier d’histoire country et 8 valeurs implicites pour quatre pays custom sans fichier d’histoire country. Ses 13 lois sont :

| Loi 1.13.9 | Diagnostics | Prérequis principal |
|---|---:|---|
| `law_censorship` | 45 | `law_enforcement` |
| `law_per_capita_based_taxation` | 34 | `currency_standards` |
| `law_mercantilism` | 7 | `international_trade` |
| `law_outlawed_dissent` | 5 | `political_agitation` |
| `law_charitable_health_system` | 3 | `medical_degrees` |
| `law_religious_schools` | 3 | `rationalism` |
| `law_national_militia` | 2 | `mandatory_service` |
| `law_public_schools` | 1 | `empiricism` |
| `law_extraction_economy` | 1 | `colonization` |
| `law_agrarianism` | 1 | `romanticism` |
| `law_total_separation` | 1 | `empiricism` |
| `law_colonial_resettlement` | 1 | `colonization` |
| `law_freedom_of_conscience` | 1 | `rationalism` |

Le groupe variants est exact : CIR/CHC/SWI avec `law_homesteading`, BEO/GAL avec `law_serfdom`, FRA avec `law_manorialism` et CRI avec `law_millet_system`. Vanilla 1.13.9 définit notamment Homesteading comme variant de `law_peasant_proprietorship`, Manorialism comme variant de Serfdom et Millet System comme variant de State Religion.

### Attribution fork / vanilla par groupe

| Groupe | FORK_CUSTOM | FORK_OVERRIDE | VANILLA_PRESENT | VANILLA_HAS_SAME_ERROR_FORM | OLD_VANILLA_INHERITED | MODERN_VANILLA_DIFFERS |
|---|---|---|---|---|---|---|
| `CL-G01` | YES pour 4 tags custom et le cutoff 1776 | YES | YES, définitions de lois et nombreux historiques homologues | NO dans le setup standard 1836 | MIXED | YES, surtout par les tiers technologiques de départ |
| `CL-G02` | YES, choix de setup 1776 | YES | YES, règles parent/variant | NO | MIXED | YES, la visibilité moderne invalide les choix listés |
| `CL-G03` | YES, paire bavaroise 1776 | YES | YES, règle `disallowing_laws` | NO | MIXED | YES, le moteur 1.13.9 refuse la paire |

Ces diagnostics sont attribuables au fork, mais leur correction n’est pas une substitution mécanique par le fallback proposé par le moteur. Elle exige une décision de country setup 1776, d’où la classe `FORK_ATTRIBUTABLE_SEMANTIC_REWRITE`.

- `COUNTRY_LAW_FORK_ERRORS = 113`
- `COUNTRY_LAW_NON_ACTIONABLE = 0`
- `COUNTRY_LAW_NEEDS_MORE_RUNTIME = 0`
- `COUNTRY_LAW_UNKNOWN = 0`

## Plan correctif groupé

Le plan comporte cinq lots, dont le conflit bavarois doit être plié dans le batch country-law lors de l’implémentation. Il n’y a pas une phase par diagnostic :

1. migration géographique complète, avec sweep des 10 manifestations associées ;
2. parent API Landowners ;
3. alignement technologies/lois de départ par pays ;
4. visibilité des variants ;
5. conflit de lois Bavaria, coordonné avec le lot 3.

`TARGETED_RUNTIME_REQUIRED = NO` pour terminer l’audit. Un runtime humain post-correction sera requis dans LOG-CLEANUP-11, après suppression de la boucle Natural Borders afin que les rotations couvrent aussi l’initialisation country-law.

## Compteurs finaux

- `CONFIRMED_FORK_ERRORS_BEFORE = 0`
- `NEW_RUNTIME_IDENTITIES_IN_SCOPE = 8`
- `NEW_RUNTIME_IDENTITIES_ATTRIBUTED = 8`
- `NEW_RUNTIME_FORK_ERRORS = 8`
- `NEW_RUNTIME_NON_ACTIONABLE = 0`
- `NEW_RUNTIME_NEEDS_MORE_RUNTIME = 0`
- `NEW_RUNTIME_UNKNOWN = 0`
- `COUNTRY_LAW_HISTORICAL_IDENTITIES_IN_SCOPE = 113`
- `COUNTRY_LAW_HISTORICAL_IDENTITIES_RECONSTRUCTED = 113`
- `COUNTRY_LAW_IDENTITIES_REPRODUCED_CURRENT = 0`
- `COUNTRY_LAW_IDENTITIES_NOT_REPRODUCED_CURRENT = 113`
- `COUNTRY_LAW_ROOT_CAUSE_GROUPS = 3`
- `COUNTRY_LAW_FORK_ERRORS = 113`
- `COUNTRY_LAW_NON_ACTIONABLE = 0`
- `COUNTRY_LAW_NEEDS_MORE_RUNTIME = 0`
- `COUNTRY_LAW_UNKNOWN = 0`
- `TOTAL_AUDIT_POOL = 121`
- `TOTAL_NEW_CONFIRMED_FORK_ERRORS = 121`
- `TARGETED_RUNTIME_REQUIRED = NO`

Le total 121 n’est établi comme compteur correctif qu’après cette attribution ; il ne s’agit plus du pool non classé initial. Il reste regroupé en cinq lots et non en 121 micro-corrections.

## Livrables et suite

- `GAMEPLAY_FILES_CHANGED = 0`
- `TECH_TREE_FILES_CHANGED = 0`
- `DOCUMENTATION_FILES_CREATED = 4`
- `ESTIMATED_PHASES_REMAINING_MIN = 2`
- `ESTIMATED_PHASES_REMAINING_LIKELY = 2`
- `ESTIMATED_PHASES_REMAINING_MAX = 3`
- `NEXT_PHASE = LOG-CLEANUP-11-GROUPED-RESIDUAL-CORRECTIONS`

LOG-CLEANUP-11 n’est pas commencé. Aucun `git add`, commit ou push n’est effectué.
