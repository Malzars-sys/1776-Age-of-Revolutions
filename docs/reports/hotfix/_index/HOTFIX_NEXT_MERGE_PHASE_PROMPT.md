# Phase HOTFIX-6A.1 — Alignement Russie / Subjecthood

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé.

## Verdict d’entrée

`NEXT_MERGE_BLOCK = HOTFIX-6A_GLOBAL_SCRIPT_DELTAS`  
`NEXT_EXECUTION_PHASE = HOTFIX_6A_RUSSIA_SUBJECTHOOD_ALIGNMENT`

## Chemins

- Fork : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`
- Source hotfix, lecture seule : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`
- Vanilla 1.13, lecture seule : `C:\Games\Victoria 3 The Great Wave\game`
- Copie jetable, lecture seule : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_sepoy_test`
- Sauvegarde de collision, lecture seule : `C:\Users\simeo\Documents\1776_C1AI_collision_20260722_225312`

## Objectif unique

Auditer puis, si la preuve reste confirmée, remplacer uniquement dans `common/history/countries/rus - russia.txt` l’activation russe de `law_national_supremacy` par `activate_law = law_type:law_subjecthood`, conformément à la source hotfix et à vanilla 1.13. Ne jamais importer le fichier complet.

## Contrôles initiaux

Utiliser `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git log -1 --oneline`, `git stash list` et vérifier que Victoria 3 et le launcher sont fermés. Exiger la branche `hotfix-dlc-audit`, l’état attendu après commit manuel C1AI et le stash MARATH intact.

## Sources et preuves

Lire en priorité :

- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
- `docs/reports/hotfix/_index/HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_REMAINING_WORK.csv`
- `docs/reports/hotfix/shared/HOTFIX_DLC_UPSTREAM_CHANGE_AUDIT.md`
- les trois versions exactes de `common/history/countries/rus - russia.txt`.

Utiliser `Get-ChildItem`, `Get-FileHash`, `Compare-Object` et `Select-String`. Ne pas utiliser `rg`.

## Protections absolues

Ne toucher ni au stash MARATH, ni aux blocs MARATH concurrents, ni à NAVY, ni à ADMIN, ni à `docs/research/technology/`, ni au setup 1776 hors ligne russe ciblée, ni aux localisations françaises, ni au workflow BIC, ni à Travancore/`STATE_TRAVANCORE`. NAVY et ADMIN sont exclus de cette sous-phase.

Conserver impérativement `activate_law = law_type:law_frontier_colonization`. Ne jamais restaurer `activate_law = law_type:law_colonial_exploitation`.

Interdictions : aucun `stash apply`, `pop` ou `drop`; aucun `git add .`; aucun commit automatique; aucune sauvegarde modifiée; aucun descripteur, harnais ou localisation modifié.

## Audit statique avant correction

1. Comparer le bloc Laws de RUS dans fork/source/vanilla.
2. Confirmer une occurrence active de `law_national_supremacy` dans le fork et de `law_subjecthood` dans source/vanilla.
3. Vérifier que `law_subjecthood` existe et est compatible avec le setup 1.13.
4. Vérifier l’historique Git du fichier et les interactions avec les lois navales russes.
5. Planifier tous les tests avant tout lancement éventuel.

## Modification autorisée

Un hunk minimal dans `common/history/countries/rus - russia.txt`, plus `docs/reports/hotfix/_index/HOTFIX_6A_RUSSIA_SUBJECTHOOD_ALIGNMENT.md`, `docs/reports/hotfix/INDEX.md` et la ligne correspondante de `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`. Aucun autre fichier n’est modifiable. Aucun autre gameplay.

## Tests statiques

Vérifier occurrences, accolades, diff minimal, `git diff --check`, absence de `law_national_supremacy` active pour RUS, présence unique de `law_subjecthood`, et absence de changement aux autres lois/technologies/modifiers de RUS.

## Runtime

Victoria 3 sera nécessaire sauf si la phase décide explicitement de reporter ce contrôle au runtime global consolidé. Préparer tous les contrôles avant lancement et condenser en un seul lancement : charger 1776 avec le mod seul, inspecter RUS, confirmer Subjecthood et l’absence d’erreur `law_subjecthood`/`rus - russia.txt` dans `error.log`. Ne créer ou modifier aucune sauvegarde persistante.

Nombre minimal de lancements : 1.

## Verdicts explicites

Succès statique : `RUSSIA_SUBJECTHOOD_ALIGNMENT_STATIC_PASS`.

Succès runtime : `RUSSIA_SUBJECTHOOD_ALIGNMENT_RUNTIME_PASS`.

Report au runtime global : `RUSSIA_SUBJECTHOOD_RUNTIME_DEFERRED_TO_GLOBAL`.

Blocage : `BLOCKED_RUSSIA_LAW_CONFLICT`, `BLOCKED_CONCURRENT_WORK_COLLISION` ou `BLOCKED_DIRTY_TREE`.

Fin réussie du bloc : ligne russe ciblée conforme, aucun autre hunk gameplay, tests statiques propres, runtime passé ou explicitement consolidé, stash et recherche intacts, aucun commit automatique.
