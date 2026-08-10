# HOTFIX-6A.26 — Réindexation globale non-pinning et audit des familles d’API

Date : 9 août 2026  
Branche : `hotfix-dlc-audit`  
HEAD audité : `9fb4324a60bcc6a155710888caca2016c84dd0ef` — `Validate global journal entry pinning runtime for 1.13`  
Nature : statique et documentaire  
Ouvertures de Victoria 3 : **0**

## 1. Résultat

La génération canonique post-6A.25Q a été reparsée intégralement depuis les deux segments prouvés par manifeste. Les 1 029 identités fraîches se répartissent en 33 familles d’API ou de syntaxe. Six familles possèdent une transformation atomique prouvée ; quatre sont `FAMILY_B` parce que des chemins explicitement protégés sont exclus, deux sont `FAMILY_A` sans exception.

```text
RESIDUAL_DIAGNOSTICS_TOTAL = 1029
RESIDUAL_PARSER_DIAGNOSTICS = 257
RESIDUAL_POSTVALIDATE_DIAGNOSTICS = 772
RESIDUAL_PATHS = 189
RESIDUAL_NORMALIZED_MESSAGES = 67

BOUNDED_PINNING_EXCEPTIONS = 14

API_FAMILIES_TOTAL = 33
API_FAMILIES_FAMILY_A = 2
API_FAMILIES_FAMILY_B = 4
API_FAMILIES_FAMILY_C = 4
API_FAMILIES_FAMILY_D = 16
API_FAMILIES_FAMILY_E = 7
API_FAMILIES_FAMILY_F = 0

ATOMIC_SWEEP_CANDIDATE_DIAGNOSTICS = 609
ATOMIC_SWEEP_CANDIDATE_OCCURRENCES = 695
ATOMIC_SWEEP_CANDIDATE_FILES = 87
ATOMIC_SWEEP_BOUNDED_EXCEPTIONS = 127
```

**Réponse opératoire : 609 des 1 029 diagnostics actuels peuvent potentiellement être supprimés par le prochain sweep mécanique global sans choix humain de gameplay.** Le plan comporte 695 substitutions sûres, car il inclut aussi des occurrences legacy statiques actuellement masquées ou non diagnostiquées, et exclut 127 occurrences protégées.

## 2. Préflight et génération canonique

Le préflight a confirmé la racine attendue, la branche exacte, le HEAD manuel 6A.25Q, un arbre suivi propre, un index vide, seulement les huit non-suivis protégés, aucun processus Victoria 3/Dowser/Launcher et le stash intact :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

Les hashes courants correspondent exactement au manifeste `after` 6A.25Q :

```text
debug.1.log = 158B750AEB15C5C00F13A97CEEA5B72E7EBFD22FC8AA880425F783AB5FFF9467
debug.log   = BE0139EC81778539952845672F3F065B9403575E71EF5FE402615D9623ADF40C
```

Le parse suit `generation + normalized_message + path + line`. Les continuations multilignes sont ignorées. `debug.1.log` apporte le montage ; les 257 erreurs parser et 772 lignes `PostValidate` qualifiées se trouvent dans `debug.log`. L’union reproduit 189 chemins et 67 messages normalisés. Aucune rotation ancienne n’a été promue en génération courante.

## 3. Pinning fermé

Les 355 diagnostics corrigés restent à zéro. Les quatorze occurrences résiduelles sont exactement la cohorte `PINNING_ATOMICITY_EXCEPTION` : douze contradictions booléennes et deux protections BIC. Elles sont classées séparément `FAMILY_D`, ne participent à aucun plan 6A.27 et ne rouvrent pas le bloc global.

```text
BOUNDED_PINNING_EXCEPTION = 14
GLOBAL_JE_PINNING_FAMILY_REMAINS_CLOSED
```

## 4. Matrice globale des 33 familles

| Famille | Diagnostics | Legacy statiques | Candidats sûrs | Exceptions | Fichiers runtime | Classe | Diagnostics supprimables |
|---|---:|---:|---:|---:|---:|---|---:|
| `API_HAS_ROLE` | 525 | 525 | 434 | 91 | 76 | FAMILY_B | 434 |
| `API_IS_RULER` | 170 | 217 | 190 | 27 | 45 | FAMILY_B | 149 |
| `API_HAS_JOURNAL_ENTRY` | 79 | 79 | 0 | 79 | 36 | FAMILY_E | 0 |
| `API_HAS_TEMPLATE` | 51 | 51 | 0 | 51 | 10 | FAMILY_E | 0 |
| `SYNTAX_STRATEGIC_REGION_LEGACY_KEYS` | 32 | 32 | 0 | 32 | 1 | FAMILY_C | 0 |
| `API_IS_INVOLVED_IN_JOURNAL_ENTRY` | 28 | 28 | 0 | 28 | 9 | FAMILY_E | 0 |
| `API_HAS_INTEREST_MARKER_IN_REGION` | 23 | 23 | 0 | 23 | 6 | FAMILY_D | 0 |
| `API_ADD_JOURNAL_ENTRY` | 14 | 14 | 0 | 14 | 7 | FAMILY_E | 0 |
| `PINNING_ATOMICITY_EXCEPTION` | 14 | 14 | 0 | 14 | 12 | FAMILY_D | 0 |
| `API_HAS_AMENDMENT` | 13 | 13 | 12 | 1 | 7 | FAMILY_B | 12 |
| `API_IS_BUILDING_TYPE` | 11 | 11 | 0 | 11 | 5 | FAMILY_D | 0 |
| `API_IS_HEIR` | 10 | 57 | 49 | 8 | 7 | FAMILY_B | 8 |
| `API_FORMATION_NAVY_UNIT_TYPE_FRACTION` | 10 | 10 | 0 | 10 | 1 | FAMILY_D | 0 |
| `API_HAS_PORT` | 7 | 7 | 0 | 7 | 2 | FAMILY_D | 0 |
| `API_CREATE_CHARACTER` | 7 | 7 | 0 | 7 | 4 | FAMILY_C | 0 |
| `API_COUNTRY_NAVY_UNIT_TYPE_FRACTION` | 6 | 6 | 0 | 6 | 2 | FAMILY_D | 0 |
| `API_IS_IN_GEOGRAPHIC_REGION` | 4 | 4 | 4 | 0 | 1 | FAMILY_A | 4 |
| `API_POST_NOTIFICATION` | 3 | 3 | 0 | 3 | 2 | FAMILY_E | 0 |
| `API_CUSTOM_TOOLTIP` | 3 | 3 | 0 | 3 | 2 | FAMILY_D | 0 |
| `API_ANY_COUNTRY_IN_IBERIA` | 2 | 6 | 6 | 0 | 1 | FAMILY_A | 2 |
| `SYNTAX_INTEREST_GROUP_LEADER_CHANCE_KEYS` | 2 | 2 | 0 | 2 | 1 | FAMILY_C | 0 |
| `API_HAS_OBJECTIVE` | 2 | 2 | 0 | 2 | 2 | FAMILY_E | 0 |
| `API_ADD_MODIFIER` | 2 | 2 | 0 | 2 | 2 | FAMILY_D | 0 |
| `API_SET_INSTITUTION_INVESTMENT_LEVEL` | 2 | 2 | 0 | 2 | 2 | FAMILY_D | 0 |
| `API_ADD_CONTEXTLESS_JOURNAL_ENTRY` | 1 | 1 | 0 | 1 | 1 | FAMILY_E | 0 |
| `API_VALUE` | 1 | 1 | 0 | 1 | 1 | FAMILY_C | 0 |
| `API_ADD_AMENDMENT` | 1 | 1 | 0 | 1 | 1 | FAMILY_D | 0 |
| `API_COUNTRY_CONVOYS_CAPACITY_MULT` | 1 | 1 | 0 | 1 | 1 | FAMILY_D | 0 |
| `API_CREATE_BUILDING` | 1 | 1 | 0 | 1 | 1 | FAMILY_D | 0 |
| `API_HAS_BUILDING` | 1 | 1 | 0 | 1 | 1 | FAMILY_D | 0 |
| `API_HAS_TECHNOLOGY_RESEARCHED` | 1 | 1 | 0 | 1 | 1 | FAMILY_D | 0 |
| `API_REMOVE_MODIFIER` | 1 | 1 | 0 | 1 | 1 | FAMILY_D | 0 |
| `API_TYPE` | 1 | 1 | 0 | 1 | 1 | FAMILY_D | 0 |

La matrice exhaustive, avec messages, objets, régions/features, correspondances source/vanilla, protections, règle, risque et justification, est `HOTFIX_6A26_API_FAMILY_MATRIX.csv`. L’inventaire de chaque identité, avec ligne parser et ligne script responsable séparées, est `HOTFIX_6A26_RESIDUAL_DIAGNOSTIC_INVENTORY.csv`.

## 5. Familles atomiques prouvées

| Famille | Diagnostics | Legacy | Candidats | Exceptions | Diagnostics supprimables | Transformation exacte |
|---|---:|---:|---:|---:|---:|---|
| `API_HAS_ROLE` | 525 | 525 | 434 | 91 | 434 | `has_role = <general|admiral|agitator|politician|executive> -> has_role_of_type = <same value>` |
| `API_IS_RULER` | 170 | 217 | 190 | 27 | 149 | `is_ruler = <yes|no> -> is_ruler_of_own_country = <same bool>` |
| `API_HAS_AMENDMENT` | 13 | 13 | 12 | 1 | 12 | `has_amendment = amendment_X -> has_amendment = amendment_type:amendment_X` |
| `API_IS_HEIR` | 10 | 57 | 49 | 8 | 8 | `is_heir = <yes|no> -> is_heir_of_own_country = <same bool>` |
| `API_IS_IN_GEOGRAPHIC_REGION` | 4 | 4 | 4 | 0 | 4 | `is_in_geographic_region = geographic_region_iberia -> is_in_geographic_region = geographic_region_iberia_old` |
| `API_ANY_COUNTRY_IN_IBERIA` | 2 | 6 | 6 | 0 | 2 | `any_country_in_iberia = { -> any_country_in_iberia_old = {` |

Les preuves communes sont : absence des formes legacy correspondantes dans la vanilla 1.13, présence massive des formes modernes dans source hotfix et vanilla, scopes et valeurs inchangés, et convergence directe d’objets homologues. `has_role_of_type` conserve le même personnage et la même valeur de rôle ; `is_ruler_of_own_country` et `is_heir_of_own_country` conservent le booléen et le pays propre du personnage. Les deux règles Iberia ne font qu’ajouter le suffixe 1.13 `_old`. `has_amendment` ajoute le type de base de données `amendment_type:` sans changer l’amendement ni le scope de loi.

692 des 695 occurrences sûres possèdent une ligne moderne homologue exacte dans la source hotfix ou la vanilla. Les trois autres sont néanmoins bornées par leur scope : deux `has_role` se trouvent dans le filtre `any_scope_character` d’une barre de progression custom et ont un couple vanilla identique general/admiral dans `00_victoria_progress_bars.txt`; le `is_heir` restant se trouve sous `on_character_death`, explicitement `Root = Character`. Le plan enregistre cette preuve de scope par occurrence.

Les anciens audits Coup et Imperialism servent de preuves historiques de signature, mais la sélection présente dépend de la reproduction fraîche 6A.25Q et du sweep global. Aucun import de bloc source/vanilla, aucun changement de sélection, de rôle, de ruler, de sponsor, de prominence ou de vivier n’est inclus.

## 6. Patch théorique et inversion

`HOTFIX_6A26_ATOMIC_API_PATCH_PLAN.csv` contient une ligne par occurrence legacy, y compris chaque exception explicitement exclue, les syntaxes avant/après, la reproduction runtime, les correspondances exactes source/vanilla et les SHA-256 avant/après par famille et pour le sweep global.

```text
PATCH_PLAN_SHA256 = D8C6DA5830C38B81348197141258F31BA8B5451E232E4ACD1C11A9FFE4B47466
THEORETICAL_CHANGED_FILES = 87
THEORETICAL_CHANGED_LINES = 695
THEORETICAL_NUMSTAT = 695 insertions(+), 695 deletions(-)
THEORETICAL_INVERSE_VALIDATION = PASS
OTHER_REQUIRED_HUNKS = 0
```

L’inversion remplace uniquement les six formes modernes planifiées par leurs formes legacy et restitue byte-for-byte chacun des 87 fichiers. Les hashes sont théoriques : aucun fichier gameplay n’a été écrit pendant 6A.26.

## 7. Familles non mécaniques

Les familles `FAMILY_C` nécessitent une réécriture de structure, de scope ou de création/sélection de personnage : notamment la table `strategic_region_scores`, les poids de dirigeants d’IG, `create_character` et le trigger `value` mal contextualisé. Les familles `FAMILY_D` croisent pinning, intérêts déclarés, NAVY, ADMIN, Inde, Japon, Russie, Pologne, technologie ou d’autres périmètres clos. Les familles `FAMILY_E` utilisent encore une API 1.13 valide mais référencent un objet absent (journal entry, template, notification ou objective) ; recréer/importer cet objet serait du contenu, pas un renommage d’API. Aucune famille ne reste `FAMILY_F` après la comparaison globale.

Les 127 exceptions du plan sont des occurrences statiques protégées des quatre familles B ; elles ne sont pas des permissions de correction ultérieure. Les 14 exceptions pinning sont en plus séparées et ne figurent jamais comme candidates.

## 8. Sélection de 6A.27

Les six règles indépendantes satisfont les critères d’atomicité et doivent être regroupées dans une seule phase, avec exclusion stricte des 127 occurrences bornées :

```text
NEXT_EXECUTION_PHASE = HOTFIX_6A27_GLOBAL_SCRIPT_API_ATOMIC_SWEEP
```

6A.27 devra appliquer exactement le plan CSV, recalculer tous les hashes, vérifier l’inversion et ne modifier aucun autre hunk. Aucun runtime n’est autorisé avant le commit manuel de 6A.27 et une future QA consolidée 6A.27Q.

## 9. Protections et validation documentaire

Aucun gameplay, aucune localisation, aucune technologie, aucun metadata/descripteur, aucune sauvegarde et aucun fichier protégé n’a été modifié. BIC conserve `activate_law = law_type:law_frontier_colonization`; `law_colonial_exploitation` n’a pas été restauré. Le registre de travail restant conserve 512 chemins uniques et 20 colonnes ; l’index des rapports conserve 22 colonnes ; la matrice des blocs conserve 17 colonnes et des `block_id` uniques. Les doublons historiques `INDEX` et `S` ne sont pas modifiés.

## 10. Verdicts

```text
HOTFIX_6A26_GLOBAL_NON_PINNING_DIAGNOSTIC_REINDEX_AND_API_FAMILY_AUDIT_COMPLETE
POST_6A25Q_FRESH_1029_DIAGNOSTICS_REINDEXED
GLOBAL_PINNING_FAMILY_REMAINS_CLOSED
PINNING_14_BOUNDED_EXCEPTIONS_PRESERVED
RESIDUAL_DIAGNOSTICS_GROUPED_BY_API_FAMILY
GLOBAL_API_FAMILY_THREE_WAY_AUDIT_COMPLETE
ATOMIC_AND_SEMANTIC_API_FAMILIES_SEPARATED
PROTECTED_WORK_EXCLUDED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_EXECUTED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
GLOBAL_MULTI_API_ATOMIC_SWEEP_CANDIDATES_PROVEN
NEXT_EXECUTION_PHASE = HOTFIX_6A27_GLOBAL_SCRIPT_API_ATOMIC_SWEEP
```
