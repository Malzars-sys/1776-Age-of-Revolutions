# HOTFIX-6A.29 — Runtime global final et QA de préparation au merge

Date : 10 août 2026  
Branche : `hotfix-dlc-audit`  
HEAD testé : `3c47e523668002576cc30c16d3c7d707ea15b137` (`Classify final residual merge blockers`)  
Version : `release/1.13.0 : d9ade554e`  
Runtime : une ouverture humaine unique

## Verdict final

```text
HOTFIX_6A29_FINAL_GLOBAL_RUNTIME_AND_MERGE_READINESS_QA_COMPLETE
FINAL_STATIC_BRANCH_AUDIT_PASS
FINAL_GLOBAL_RUNTIME_PASS
FINAL_GLOBAL_RUNTIME_SINGLE_LAUNCH_CONFIRMED
FINAL_1776_SMOKE_PASS
FINAL_RUNTIME_NO_NEW_ATTRIBUTABLE_DIAGNOSTICS
FINAL_RUNTIME_NO_GAMEPLAY_CHANGE
FINAL_PROTECTED_WORK_INTACT
FINAL_STASH_NAVY_3C_3_INTACT
FINAL_TECH_RESEARCH_INTACT
FINAL_RESIDUAL_CLASSIFICATION_REMAINS_VALID
TRUE_MERGE_BLOCKERS_REMAINING = 0
TRUE_MERGE_BLOCKER_GROUPS = 0
MINIMUM_CORRECTION_PHASES_REQUIRED = 0
FINAL_MERGE_READINESS = READY
HOTFIX_GLOBAL_SCRIPT_DELTAS_COMPLETE
HOTFIX_MERGE_RUNTIME_VALIDATION_COMPLETE
NO_FURTHER_GAMEPLAY_CORRECTION_SELECTED
NO_AUTOMATIC_COMMIT
NEXT_ACTION = MANUAL_FINAL_6A29_COMMIT_AND_GIT_BRANCH_FINALIZATION
```

Le fork testé est suffisamment validé pour être déclaré prêt. Aucune nouvelle phase gameplay du merge n’est sélectionnée.

## Audit statique avant runtime

Le pré-vol a confirmé la racine, la branche, le message exact du commit 6A.28, un arbre suivi initialement propre, un index vide, les sept recherches technologiques comme seuls non-suivis, l’absence de `bject`, le stash NAVY intact et zéro processus Victoria 3/Dowser/Launcher.

La réconciliation documentaire finale a supprimé un décalage de registre : 98 lignes conservaient encore d’anciens labels `P1_REVIEW`, `P1_RUNTIME_PENDING`, `UNKNOWN_REQUIRES_REVIEW` ou `VANILLA_1_13_ALIGNMENT_REQUIRED` alors que 6A.28 les avait déjà classées non bloquantes. Aucun gameplay n’était manquant ou modifié. Ces lignes portent désormais leur décision 6A.28 effective : déjà comptabilisé, exception bornée ou travail protégé.

```text
FINAL_STATIC_BRANCH_AUDIT = PASS
REMAINING_WORK_ROWS = 513
REMAINING_WORK_UNIQUE_PATHS = 513
ACTIVE_UNRESOLVED_P0_P1 = 0
BLOCKING_UNKNOWN_REQUIRES_REVIEW = 0
REQUIRED_HOTFIX_FILES_ABSENT_FROM_FORK = 0
TRUE_MERGE_BLOCKERS_BEFORE_RUNTIME = 0
TRUE_MERGE_BLOCKER_GROUPS = 0
MINIMUM_CORRECTION_PHASES_REQUIRED = 0
```

Le fichier `common/scripted_progress_bars/01_mod76_progress_bars.txt` reste indexé. Les seules portes encore actives avant le lancement étaient le runtime global lui-même et la finalisation manuelle de branche.

## Préparation de la session

La matrice a été entièrement écrite avant l’ouverture. Elle contient 19 contrôles statiques, runtime et post-runtime. Les 60 fichiers du répertoire de logs ont été hashés avant lancement. Une empreinte déterministe a été calculée sur les 845 fichiers suivis hors documentation, complétée par 94 hashes sensibles couvrant Afghanistan, Pologne, BIC, Russie et les 87 fichiers 6A.27.

```text
PRE_RUNTIME_LOG_FILES = 60
PRE_RUNTIME_GAMEPLAY_FILES = 845
PRE_RUNTIME_SENSITIVE_HASHES = 94
PRE_RUNTIME_GAMEPLAY_TREE_SHA256 = F1B3BC42881C9E06F167C93C4B2C416AE3B92528C955AEFF4A7C975BC8847F79
```

## Session humaine unique

L’opérateur a ouvert Victoria 3 une seule fois. Une partie Vietnam 1776 a servi de smoke initial. La sauvegarde `HOTFIX_6A29_FINAL_SMOKE.v3` a été créée, puis rechargée sans fermer Victoria 3. Dans la même session, l’opérateur a joué successivement le Japon, BIC, l’Irak mamelouk, l’État zand et la Russie. Aucun crash, popup cassée, clé brute évidente ou autre anomalie majeure n’a été observé.

Une capture opérateur confirme visuellement que la Russie possède bien `Sujétion` comme loi de citoyenneté. Le menu de chargement montrait les nombreuses anciennes sauvegardes Sepoy, mais leur volume empêchait d’identifier raisonnablement les sauvegardes QA demandées. Elles n’ont pas été forcées et aucun second lancement n’a été effectué.

```text
FINAL_GLOBAL_RUNTIME_LAUNCHES = 1
FINAL_1776_BASELINE_SMOKE = PASS
FINAL_GLOBAL_SMOKE = PASS
SAVE_RELOAD = PASS
RAW_KEYS_OBSERVED = 0
MAJOR_RUNTIME_ANOMALIES_OBSERVED = 0
FORBIDDEN_PROCESS_COUNT_AFTER_CLOSE = 0
```

## Résultats fonctionnels

| Contrôle | Résultat | Preuve ou limite |
|---|---|---|
| Vietnam 1776 | `PASS` | Partie créée, sauvegardée et rechargée ; aucune anomalie évidente. |
| Russie | `PASS` | Partie chargée ; capture de `Sujétion` active. |
| Japon | `PASS` | Partie chargée ; aucune clé brute ou régression évidente. |
| BIC / Inde | `PASS` | Partie chargée ; aucune régression évidente. Le panneau de lois BIC n’a pas été photographié séparément ; les preuves canoniques de `law_frontier_colonization` restent applicables et les hashes sont inchangés. |
| Mamluk Iraq / IR1 | `PASS` | Partie chargée ; aucune clé brute ou régression évidente. Le comportement du secret goal sur plusieurs mois n’est pas revendiqué. |
| Perse / État zand | `PASS` | Partie chargée ; aucune clé brute ou régression évidente. |
| TUR / Grande Crise orientale | `NOT_OBSERVED` | Pas d’observation TUR séparée explicitement rapportée ; 6A8F conserve ses preuves statiques et runtime. |
| Sepoy détaillé | `NOT_OBSERVED` | Sauvegarde historique non retrouvée dans la liste ; aucun événement forcé. Les QA antérieures restent canoniques. |
| NAVY / formations | `PREVIOUS_RUNTIME_EVIDENCE_ONLY` | Sauvegarde dédiée non chargée ; preuves `3b02b2a` conservées, stash non appliqué, hashes inchangés. |
| ADMIN | `PREVIOUS_STATIC_EVIDENCE_PLUS_GLOBAL_SMOKE` | Travail protégé inchangé et aucune régression administrative évidente dans le smoke multi-pays. |
| Autriche/Croatie/Suisse | `NOT_OBSERVED` | Preuve runtime ciblée antérieure conservée. |
| DEI/VOC/Java | `NOT_OBSERVED` | Sauvegarde dédiée non chargée ; validation ciblée antérieure conservée. |
| GEN/VEN Merchant Banking | `NOT_OBSERVED` | Contrôle non répété ; PASS runtime antérieur conservé. |
| Cohorte JE/API fermée | `PASS` | Zéro diagnostic nouveau dans la génération finale. |

Les `NOT_OBSERVED` ne sont pas convertis en `PASS`. Ils ne bloquent pas READY parce que les blocs concernés possèdent déjà des preuves antérieures suffisantes, aucun nouveau diagnostic ne les affecte et aucun fichier gameplay n’a changé.

## Manifestes et génération fraîche

Après fermeture complète du jeu et du launcher, 49 des 60 fichiers de logs avaient tourné ou changé. `debug.1.log` porte le montage exact du fork et `debug.log` porte les diagnostics frais.

```text
debug.1.log SHA256 = 75261C672147D6BEE014DAD829BCAFA7CE1BD69D5CA129D211D4023D50323DCB
debug.log   SHA256 = B89E52F16639618E1251B227375D21928F43BEACDD9E1AE8799E948322BD00BC
error.log   SHA256 = 900E33F4170D244E015F676F5F92850D093A1127FFFD49205FBD49C2E0F26961
game.log    SHA256 = 2E557657EE7748915407209D5FE2A03F71D7860214451BBEE79B08938B88F27D
system.log  SHA256 = E5BBEE6C900A817ED76797DE8B009543E9F0B80F8BF1F10031A8D16410FADB0A
```

`system.log` confirme `release/1.13.0 : d9ade554e`. `debug.1.log` confirme le montage de `1776_Age_of_Revolutions_fork`. Les rotations fraîches d’`error.log` ne contiennent aucun signal `Unhandled exception`, `Assertion failed`, `Fatal error`, `Crash`, `corrupt` ou `stack trace`.

La normalisation `generation + normalized_message + path + line` donne :

```text
FINAL_FRESH_TOTAL_DIAGNOSTICS = 420
FINAL_FRESH_PARSER_DIAGNOSTICS = 98
FINAL_FRESH_POSTVALIDATE_DIAGNOSTICS = 322
FINAL_FRESH_PATHS = 113
FINAL_FRESH_NORMALIZED_MESSAGES = 65

KNOWN_IDENTITIES_REPRODUCED = 420
KNOWN_IDENTITIES_NOT_REPRODUCED = 0
NEW_IDENTITIES = 0
NEW_ATTRIBUTABLE_DIAGNOSTICS = 0
```

Les 420 identités correspondent exactement, clé par clé, à l’inventaire 6A.28. Leur classification reste donc valide :

```text
CLASS_TRUE_MERGE_BLOCKER = 0
CLASS_PROTECTED_WORK = 54
CLASS_INTENTIONAL_FORK_DIVERGENCE = 17
CLASS_POST_MERGE_BACKLOG = 4
CLASS_SEMANTIC_REWRITE_REQUIRED = 43
CLASS_BOUNDED_EXCEPTION = 129
CLASS_ALREADY_ACCOUNTED_FOR = 173
CLASSIFICATION_TOTAL = 420
```

Le fait qu’`error.log` ne soit pas vide n’est pas un échec : aucun diagnostic nouveau ou nouvellement bloquant n’est présent.

## Intégrité gameplay et protections

L’empreinte post-runtime des 845 fichiers gameplay est identique à l’empreinte pré-runtime. Les 94 fichiers sensibles correspondent également tous.

```text
POST_RUNTIME_GAMEPLAY_TREE_SHA256 = F1B3BC42881C9E06F167C93C4B2C416AE3B92528C955AEFF4A7C975BC8847F79
GAMEPLAY_TREE_HASH_MATCH = yes
SENSITIVE_HASHES_MATCH = 94/94
GAMEPLAY_CHANGED_DURING_FINAL_RUNTIME = 0
```

Le stash reste :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

Les sept chemins de recherche technologique protégés restent les seuls non-suivis hors livrables 6A.29. Leur contenu n’a pas été ouvert ni inspecté. `bject` reste absent. Aucun stash n’a été créé, appliqué ou supprimé.

```text
PROTECTED_WORK_INTACT = yes
STASH_NAVY_3C_3_INTACT = yes
TECH_RESEARCH_FILES_INTACT = yes
BJECT_ABSENT = yes
```

## Conclusion et action humaine

Tous les critères READY sont satisfaits : audit statique PASS, une seule ouverture, smoke et sauvegarde/rechargement PASS, zéro diagnostic attribuable nouveau, zéro modification gameplay et protections intactes.

La prochaine action est exclusivement humaine : commit documentaire final 6A.29, vérification de branche, puis éventuelle finalisation Git vers `main`, création du dépôt GitHub et push selon décision explicite. Aucun de ces actes n’est commencé ici.
