# Phase HOTFIX-6A.10 — Sélection du prochain résidu global

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Nature de la phase

Phase strictement documentaire. Aucun gameplay ne doit être modifié et aucun
runtime ne doit être produit.

Codex ne doit jamais :

- lancer Victoria 3 ;
- lancer le launcher Paradox ;
- piloter l’interface ;
- utiliser la console ;
- ouvrir une sauvegarde ;
- produire de nouveaux logs ;
- corriger un candidat ;
- créer un commit automatique.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, STRICTEMENT EN LECTURE SEULE :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA VICTORIA 3 1.13, STRICTEMENT EN LECTURE SEULE :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d’entrée requis

- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_STATIC_PASS`
- `SICK_MAN_EIGHT_JE_PINNING_EIGHT_HUNK_1_13_ALIGNMENT_COMPLETE`
- `OTTOMAN_TANZIMAT_START_DISABLED_IN_1776_PRESERVED`
- `NO_TANZIMAT_ACTIVATION_CHANGED`
- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_RUNTIME_PASS`
- `SICK_MAN_EIGHT_JE_PINNING_PARSER_ERRORS_8_TO_0`
- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT_COMPLETE`
- `OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md`

6A.9F doit avoir été commitée manuellement. Ne commence jamais 6A.10 depuis
son worktree non commité.

## Objectif unique

Sélectionner exactement un prochain sous-bloc atomique parmi les résidus
globaux encore ouverts.

Cette phase doit uniquement :

1. actualiser l’inventaire documentaire après 6A.9F ;
2. analyser les 378 diagnostics de pinning restants sans les corriger ;
3. comparer en trois voies les candidats sérieux ;
4. publier exactement trois meilleurs candidats ;
5. sélectionner exactement un candidat ;
6. produire le prompt autonome de sa future exécution.

Ne modifier aucun gameplay et ne commencer aucun candidat.

## Préflight Git obligatoire

Exécuter :

```powershell
Set-Location "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork"

git rev-parse --show-toplevel
git branch --show-current
git status --short
git log -5 --oneline --decorate
git diff --check
git diff --cached --name-only
git stash list
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md
```

Exiger :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.9F et tous ses verdicts dans le HEAD ;
- 6A.9F commitée manuellement ;
- worktree suivi propre et index staged vide ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` non suivis ;
- stash exact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- aucun processus Victoria 3, dowser ou Paradox.

Verdicts bloquants :

- `BLOCKED_WRONG_BRANCH`
- `BLOCKED_6A9F_NOT_COMMITTED`
- `BLOCKED_DIRTY_TREE`
- `BLOCKED_STAGED_FILES`
- `BLOCKED_UNEXPECTED_UNTRACKED_FILES`
- `BLOCKED_PROTECTED_STASH_MISSING`
- `BLOCKED_GAME_PROCESS_RUNNING`

Interdictions Git : aucun reset, restore, checkout de fichier, clean, merge,
rebase, amend, commit automatique, stash apply/pop/drop ou inspection du
contenu du stash.

## Hashes obligatoires

Vérifier avant toute analyse :

| Preuve | SHA-256 |
| --- | --- |
| Fork `00_sick_man.txt` corrigé | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` |
| Source hotfix `00_sick_man.txt` | `E48405BFABB52F6CE757880E436C8D44C67111E246AF3215FD3F96EC4F3477F9` |
| Vanilla `00_sick_man.txt` | `1EAD43BE40DAF22D585712442AFD379C893C3075007CDA0AADDB126CCF1DCA41` |
| Histoire TUR fork | `81ABC8DEA9DE93EC6A4DD417FD05FD6859F3122758D2B27E712B1880013F9CA9` |
| Grande Crise orientale fork | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` |
| Événements Sick Man | `D110D1FD83CD98E131D4C2769B606CC908F17844EFF88EF65F51FEBF313A0C2B` |
| Événements Tanzimat | `F5DAABC9D36BEAE714E5BDFC3B156995B3EAE7758004CE3C7B8C3512BA80AD30` |

Enregistrer aussi les SHA-256 de `bject` et des sept fichiers de
`docs/research/technology/` et les comparer à 6A.9F.

Arrêter avec `BLOCKED_THREE_WAY_EVIDENCE_CHANGED` si une preuve imposée
diffère.

## Sources obligatoires

Lire intégralement :

- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md` ;
- `HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les changelogs complets du fork et de la source hotfix ;
- les nouveaux logs et rotations 6A.9F, uniquement en lecture seule.

Ne lancer le jeu pour aucune preuve supplémentaire.

## Base canonique après 6A.9F

Actualiser les 161 anciennes lignes `PENDING_REVIEW` avec cette répartition
effective :

- 7 `REQUIRED_HOTFIX_DELTA` ;
- 17 `VANILLA_1_13_ALIGNMENT_REQUIRED` ;
- 17 `ALREADY_MERGED` ;
- 3 `INTENTIONAL_FORK_DIVERGENCE` ;
- 1 `OBSOLETE_HOTFIX_CONTENT` ;
- 10 `POST_MERGE_DESIGN_BACKLOG` ;
- 19 `PROTECTED_CONCURRENT_WORK` ;
- 87 `UNKNOWN_REQUIRES_REVIEW`.

Somme obligatoire : 161.

Il reste 111 lignes directement exploitables par une revue :

- 7 deltas hotfix requis ;
- 17 alignements vanilla 1.13 ;
- 87 inconnus.

Ces 111 lignes ne représentent pas 111 correctifs. Le total historique de 26
deltas à haute confiance reste `UNVERIFIED`.

## Baseline parser 6A.9F

Le nouveau `debug.log` contient :

- 378 erreurs exactes
  `Unexpected token: should_be_pinned_by_default,` ;
- 142 fichiers uniques ;
- zéro erreur de pinning dans `00_sick_man.txt` ;
- zéro diagnostic de la nouvelle propriété contextuelle dans ce fichier ;
- trois diagnostics d’événements Tanzimat connus et indépendants.

Recalculer ces nombres depuis les logs sans les présumer.

Regrouper par :

- chemin ;
- nombre d’occurrences ;
- objet ;
- statut d’inventaire ;
- présence source hotfix ;
- présence vanilla ;
- protection ;
- dette fonctionnelle adjacente.

Publier au minimum les vingt-cinq fichiers les plus représentés et les familles
principales. Une occurrence parser ne constitue jamais à elle seule
l’autorisation de corriger.

## Blocs clos interdits comme candidats

Ne jamais rouvrir ni sélectionner :

- `common/journal_entries/05_balkan_national_awakening.txt` ;
- `common/journal_entries/05_creation_of_yugoslavia.txt` ;
- `common/journal_entries/00_italian_unification.txt` ;
- `common/journal_entries/00_greek_nationalism.txt` ;
- `common/journal_entries/05_great_eastern_crisis.txt` ;
- les huit pinning de `common/journal_entries/00_sick_man.txt`.

Les trois diagnostics `tanzimat_events.5`, `.9` et `.10` ne peuvent être
sélectionnés qu’après preuve qu’une correction reste indépendante du design
d’activation différée, des pulses et de la chaîne événementielle. Ils ne
doivent pas être mélangés aux pinning déjà clos.

## Comparaison trois voies obligatoire

Pour chaque candidat sérieux, documenter :

- chemin et objet exacts ;
- comportement du fork ;
- comportement de la source hotfix ;
- comportement vanilla ;
- preuve changelog éventuelle ;
- diagnostic runtime éventuel ;
- fichiers, objets, hunks, additions et suppressions ;
- dépendances et dette adjacente ;
- localisations ;
- collision avec travail protégé ;
- compatibilité 1776 ;
- rollback exact ;
- priorité P0, P1 ou inférieure ;
- besoin de runtime humain futur.

Ne jamais remplacer un fichier complet. Ne jamais sélectionner un candidat
quand source hotfix et vanilla divergent sans justification claire.

## Pistes obligatoires

### Merchant Banking GEN/VEN

Revalider séparément :

- `common/history/countries/gen - genoa.txt` ;
- `common/history/countries/ven - venetia.txt` ;
- `law_traditionalism` dans le fork ;
- `law_merchant_banking` dans la source hotfix ;
- loi, icône et localisations existantes ;
- changelog 2.3 ;
- exclusion du nom source-only des propriétaires terriens ;
- préservation absolue de `law_merchant_navy`.

### Navigation Acts

Revalider GBR, HBC, NBS, ONT et ORA :

- absence actuelle de `law_mercantilism_navigation_acts` ;
- présence dans la source hotfix ;
- preuve changelog ;
- comportement vanilla 1.13 ;
- autres écarts dans chaque fichier ;
- collision GBR/NAVY ;
- BIC strictement hors périmètre.

### Diagnostics Tanzimat

Analyser séparément `.5`, `.9` et `.10` :

- déclaration et namespace des événements ;
- disponibilité DLC ;
- on-actions et pulses ;
- convergence source/vanilla ;
- effet de la chaîne inactive ;
- possibilité ou non d’un correctif autonome.

Ne pas sélectionner une activation Tanzimat et ne modifier aucun événement.

### Petits alignements 1.13

Revoir notamment, sans présumer leur sélection :

- `01_coup.txt` ;
- `04_imperialism_of_promise.txt` ;
- autres fichiers à une ou deux erreurs dont source hotfix et vanilla
  convergent.

Écarter tout candidat avec changements adjacents non résolus, portée massive,
localisation manquante ou protection active.

### Inconnus

Examiner un `UNKNOWN_REQUIRES_REVIEW` uniquement lorsqu’un log, un changelog ou
une comparaison trois voies fournit une preuve précise.

## Protections absolues

Ne sélectionner ni modifier :

- DEI/VOC, Java et économie post-compagnie ;
- Balkan National Awakening, Yugoslavia, Risorgimento, nationalisme grec,
  Grande Crise orientale et pinning Sick Man ;
- NAVY, lois navales, formations et événements navals ;
- MARATH, SAT, KHP et Travancore ;
- Inde, BIC, Sepoy et Bombay ;
- ADMIN ;
- Japon, Russie, Autriche, Croatie, Slavonie et Suisse ;
- révolutions américaine et française ;
- lettres de Kew ;
- technologies et recherches technologiques ;
- localisations françaises générales ;
- agriculture, alimentation et industrie générales ;
- descripteurs, launcher, sauvegardes et `bject`.

Préserver dans BIC :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer `law_colonial_exploitation`.

## Top 3 obligatoire

Publier exactement :

| Rang | Phase candidate | Fichiers | Objets | Hunks | Priorité | Preuve | Collision | Runtime |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |

Pour chacun, expliquer :

- comparaison trois voies ;
- preuve ;
- taille exacte ;
- dépendances ;
- collision ;
- raison de sélection ou report ;
- besoin de runtime humain.

Sélectionner exactement un candidat et publier :

`NEXT_EXECUTION_PHASE = <phase atomique sélectionnée>`

## Périmètre d’écriture fermé

Uniquement :

1. `docs/reports/hotfix/_index/HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`
2. `docs/reports/hotfix/INDEX.md`
3. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
4. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
6. `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Aucun gameplay n’est modifiable.

## Rapport requis

Créer :

`docs/reports/hotfix/_index/HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

Inclure :

1. date, branche, HEAD initial/final ;
2. préflight et état Git ;
3. hashes de référence et protections ;
4. sources ;
5. inventaire actualisé et somme 161 ;
6. 111 lignes directement exploitables ;
7. analyse des 378 erreurs et 142 fichiers ;
8. familles, dépendances et protections ;
9. comparaisons trois voies ;
10. exactement trois candidats ;
11. exactement un candidat sélectionné ;
12. futur périmètre fermé ;
13. collision, localisation et rollback ;
14. besoin de runtime humain futur ;
15. documents modifiés ;
16. contrôles finaux ;
17. décision de commit manuel ;
18. verdicts.

## Prompt autonome futur

Remplacer ce fichier par le prompt complet de la phase atomique sélectionnée.

Si un runtime futur est nécessaire :

- Codex ne lance jamais Victoria 3 ou le launcher ;
- tous les contrôles statiques précèdent le lancement ;
- une seule fiche condensée est préparée ;
- Codex s’arrête à `RUNTIME_OPERATOR_ACTION_REQUIRED` ;
- les logs ne sont analysés qu’après fermeture humaine confirmée ;
- aucun PASS runtime sans compte rendu humain.

Ne commencer pas la phase sélectionnée pendant 6A.10.

## Contrôles finaux

Vérifier :

- zéro gameplay modifié ;
- exactement six documents de phase ;
- exactement trois candidats ;
- exactement un candidat sélectionné ;
- aucun bloc clos réintroduit ;
- catégories exclusives et somme 161 ;
- baseline 378/142 recalculée ;
- prompt futur autonome ;
- huit hashes protégés inchangés ;
- BIC et stash intacts ;
- source hotfix et vanilla inchangées ;
- CSV valides ;
- `git diff --check` propre ;
- index staged vide ;
- aucun processus Victoria 3, dowser ou Paradox ;
- aucun commit automatique ;
- aucune phase suivante commencée.

Exécuter :

```powershell
git diff --check
git status --short
git diff --name-only
git diff --name-status
git diff --stat
git diff --cached --name-only
git stash list
```

## Verdicts

- `HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = <phase atomique sélectionnée>`

Ne committe rien automatiquement.
