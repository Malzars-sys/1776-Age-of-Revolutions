# HOTFIX-6A.28 — Réindexation finale des bloqueurs de merge résiduels

Date : 9 août 2026  
Branche : `hotfix-dlc-audit`  
HEAD d’entrée : `24f6b0cd86dfed0ef765c511eaa91fc9556f466f` (`Validate global script API runtime for 1.13`)  
Mode : `STATIC / DOCUMENTARY / READ_ONLY_GAMEPLAY`

## Verdict

```text
HOTFIX_6A28_FINAL_RESIDUAL_MERGE_BLOCKER_REINDEX_COMPLETE
POST_6A27Q_FRESH_420_DIAGNOSTICS_REINDEXED
FINAL_RESIDUAL_420_DIAGNOSTICS_CLASSIFIED
FINAL_RESIDUAL_CLASSIFICATION_COMPLETE
NO_UNCLASSIFIED_RESIDUAL_DIAGNOSTICS
NO_DUPLICATE_RESIDUAL_CLASSIFICATIONS
GLOBAL_MULTI_API_SWEEP_REMAINS_CLOSED
GLOBAL_PINNING_FAMILY_REMAINS_CLOSED
PROTECTED_WORK_PRESERVED
POST_MERGE_BACKLOG_SEPARATED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_EXECUTED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
TRUE_MERGE_BLOCKERS_REMAINING = 0
TRUE_MERGE_BLOCKER_GROUPS = 0
MINIMUM_CORRECTION_PHASES_REQUIRED = 0
FINAL_GLOBAL_RUNTIME_READY
NEXT_EXECUTION_PHASE = HOTFIX_6A29_FINAL_GLOBAL_RUNTIME_AND_MERGE_READINESS_QA
```

La présence d’un diagnostic n’est pas assimilée à une obligation de merge. Les 420 identités fraîches sont toutes expliquées par un périmètre protégé, une divergence intentionnelle, un backlog explicite, une réécriture sémantique non requise par le hotfix, une exception bornée ou une décision déjà comptabilisée. Aucune correction n’est sélectionnée.

## Pré-vol et provenance

Le dépôt, la branche et le commit d’entrée correspondent à l’état canonique 6A.27Q. L’index était vide et l’arbre suivi propre. Les seuls non-suivis étaient les sept documents de recherche technologique protégés ; `bject` était absent. Aucun processus Victoria 3, Dowser ou Paradox Launcher n’était actif.

Le stash est resté inchangé :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

Les deux segments frais ont été relus sans lancer le jeu :

```text
debug.1.log SHA256 = D2A5C169C60D4F21DD2399088C9478ABB552D1C4DFD35E2AF26912B3759AC2EE
debug.log   SHA256 = AF31A9F15398F729AF9816043869F889CA31B8934FD0BD94FBCB6A7917DA2CAF
```

La clé `generation + normalized_message + path + line` reproduit exactement la baseline canonique :

```text
FRESH_TOTAL_DIAGNOSTICS = 420
FRESH_PARSER_DIAGNOSTICS = 98
FRESH_POSTVALIDATE_DIAGNOSTICS = 322
FRESH_POSTVALIDATE_TRIGGER = 289
FRESH_POSTVALIDATE_EFFECT = 33
FRESH_PATHS = 113
FRESH_NORMALIZED_MESSAGES = 65
IDENTITIES_DISAPPEARED_SINCE_6A25Q = 609
IDENTITIES_APPEARED = 0
IDENTITIES_UNCHANGED = 420
```

Les 609 diagnostics supprimés par 6A.27 ne sont pas réintroduits. Les six familles atomiques restent fermées statiquement et en runtime.

## Classification finale

| Classe primaire | Diagnostics | Bloqueurs de merge |
|---|---:|---:|
| `TRUE_MERGE_BLOCKER` | 0 | 0 |
| `PROTECTED_WORK` | 54 | 0 |
| `INTENTIONAL_FORK_DIVERGENCE` | 17 | 0 |
| `POST_MERGE_BACKLOG` | 4 | 0 |
| `SEMANTIC_REWRITE_REQUIRED` | 43 | 0 |
| `BOUNDED_EXCEPTION` | 129 | 0 |
| `ALREADY_ACCOUNTED_FOR` | 173 | 0 |
| **Total** | **420** | **0** |

```text
CLASS_TRUE_MERGE_BLOCKER = 0
CLASS_PROTECTED_WORK = 54
CLASS_INTENTIONAL_FORK_DIVERGENCE = 17
CLASS_POST_MERGE_BACKLOG = 4
CLASS_SEMANTIC_REWRITE_REQUIRED = 43
CLASS_BOUNDED_EXCEPTION = 129
CLASS_ALREADY_ACCOUNTED_FOR = 173
CLASSIFICATION_TOTAL = 420
TRUE_MERGE_BLOCKERS_REMAINING = 0
TRUE_MERGE_BLOCKER_GROUPS = 0
```

Chaque ligne de l’inventaire porte exactement une `final_classification`. Les sept indicateurs de contexte ne créent aucune seconde classification primaire. Aucun plan de correction `HOTFIX_6A28_TRUE_MERGE_BLOCKER_PLAN.csv` n’est créé, car `N = 0`.

### Lecture des classes

- Les 129 diagnostics `BOUNDED_EXCEPTION` sont les occurrences runtime actuelles des exceptions API/pinning déjà bornées. Ils ne doivent pas être confondus avec les nombres statiques documentés `BOUNDED_API_EXCEPTIONS = 127` et `BOUNDED_PINNING_EXCEPTIONS = 14`.
- Les 54 `PROTECTED_WORK` croisent les protections explicites, notamment intérêts déclarés, NAVY, ADMIN, Inde/BIC/Sepoy et autres périmètres fermés ou concurrents.
- Les 43 `SEMANTIC_REWRITE_REQUIRED` concernent des formes sans substitution atomique sûre : clés de régions stratégiques, chances de leader d’IG, création de personnage, `value` et `has_port` dépendant du scope. Leur correction exige une décision de gameplay et ne fait pas partie du merge hotfix courant.
- Les 173 `ALREADY_ACCOUNTED_FOR` comprennent 154 diagnostics provenant de 55 fichiers vanilla chargés mais absents du fork. Ces fichiers ne peuvent pas représenter un delta hotfix du fork encore à fusionner.

## Comparaison trois voies ciblée

Les drapeaux de présence source et vanilla de l’inventaire 6A.26 ont été revérifiés physiquement pour les 420 lignes : aucune divergence de présence n’a été trouvée. Sur les 113 chemins frais :

```text
FORK_PRESENT_DIAGNOSTICS = 266
FORK_PRESENT_PATHS = 58
FORK_ABSENT_DIAGNOSTICS = 154
FORK_ABSENT_PATHS = 55
SOURCE_OR_VANILLA_PRESENCE_FLAG_MISMATCHES = 0
```

L’égalité source/vanilla n’a jamais été utilisée comme autorisation de remplacement de fichier. La comparaison sert uniquement à déterminer si une identité représente réellement du contenu hotfix non fusionné.

## Les 23 diagnostics indépendants dans les fichiers 6A.27

```text
SWEEP_FILES_WITH_INDEPENDENT_DIAGNOSTICS = 7
INDEPENDENT_DIAGNOSTICS_IN_SWEEP_FILES = 23
INDEPENDENT_PARSER = 1
INDEPENDENT_POSTVALIDATE = 22
```

Distribution :

| Classe | Nombre |
|---|---:|
| `ALREADY_ACCOUNTED_FOR` | 10 |
| `INTENTIONAL_FORK_DIVERGENCE` | 9 |
| `POST_MERGE_BACKLOG` | 2 |
| `BOUNDED_EXCEPTION` | 1 |
| `PROTECTED_WORK` | 1 |
| `SEMANTIC_REWRITE_REQUIRED` | 0 |
| `TRUE_MERGE_BLOCKER` | 0 |

Ces 23 identités étaient déjà présentes avant 6A.27 ; elles ne sont ni des régressions du sweep ni une raison de rouvrir ses six familles.

## Décisions de frontière

### HBC / Navigation Acts

L’intention canonique HBC reste inconnue, mais ce choix de design n’est plus un bloqueur du merge hotfix. Le runtime canonique montre un composite stable `hubson + hudson`, sans clé brute ni mutation temporelle de loi ou de gouvernement. Aucune histoire HBC/GBR n’est modifiée. La décision humaine est conservée dans un backlog de design séparé, admissible après le merge.

### Declared interests / Égypte

Le legacy `add_declared_interest` reste invalide et aucun remplacement jour 1 n’est démontré. Les rapports canoniques avaient déjà différé la validation sémantique de la crise égyptienne : ces identités sont protégées ou déjà comptabilisées, pas rouvertes comme nouveaux bloqueurs.

### Mamluk Iraq, Japon et ADMIN

Aucun bloqueur nouveau n’est établi. Mamluk Iraq et Japon passent au statut documentaire `FINAL_GLOBAL_RUNTIME_REQUIRED` : leur vérification restante est `ALREADY_ACCOUNTED_FOR` et doit être consolidée dans 6A.29, sans runtime spécifique. ADMIN reste du travail protégé et ne reçoit aucune correction 6A.

## Réconciliation du registre de 513 chemins

Le registre conserve exactement 513 lignes et le fichier custom `common/scripted_progress_bars/01_mod76_progress_bars.txt` reste indexé, même sans diagnostic frais.

```text
REMAINING_WORK_ROWS = 513
FRESH_PATHS_MATCHED_IN_REGISTRY = 55
FRESH_PATHS_OUTSIDE_REGISTRY = 58
OUTSIDE_REGISTRY_FORK_ABSENT = 53
OUTSIDE_REGISTRY_FORK_PRESENT = 5
```

Les cinq chemins présents dans le fork mais historiquement hors registre sont :

```text
common/history/characters/aus.txt
common/history/countries/hbc - hubson bay company.txt
common/history/countries/org -oregan.txt
common/journal_entries/00_battle_for_india_mod.txt
events/battle_for_india_events.txt
```

Ils ne sont pas ajoutés artificiellement : l’inventaire diagnostique les couvre déjà et leur statut est explicite. Les 53 autres chemins hors registre sont absents du fork. Aucun chemin existant n’a été supprimé à cause de l’absence d’un diagnostic runtime.

## Livrables et suite exclusive

- `HOTFIX_6A28_FINAL_RESIDUAL_DIAGNOSTIC_INVENTORY.csv` : 420 lignes, une identité et une classe primaire par ligne.
- `HOTFIX_6A28_FINAL_RESIDUAL_FAMILY_MATRIX.csv` : 31 familles présentes dans la génération actuelle, recalculées sans reprendre les comptes historiques.
- Aucun fichier de plan de bloqueur : zéro groupe et zéro phase corrective minimale.

La seule prochaine phase sélectionnée est `HOTFIX_6A29_FINAL_GLOBAL_RUNTIME_AND_MERGE_READINESS_QA`. Elle doit préparer un unique runtime final consolidé couvrant le smoke 1776, RUS, TUR/PER, Japon, Mamluk Iraq si accessible, BIC/Sepoy, les non-régressions NAVY/ADMIN, les principaux pays et États corrigés, puis sauvegarde/rechargement si réalisable dans la même session et collecte de l’`error.log` final.

6A.29 n’est ni lancée ni commencée dans cette phase.
