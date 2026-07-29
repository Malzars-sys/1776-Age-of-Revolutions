# Phase HOTFIX-6A.9F — Alignement Victoria 3 1.13 des huit pinning Sick Man

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Nature de la phase

Phase de correction API atomique, limitée à un fichier, huit objets et huit
substitutions exactes.

Codex ne doit jamais lancer Victoria 3, lancer le launcher Paradox, piloter
l’interface, utiliser la console, ouvrir une sauvegarde, produire lui-même des
logs ou créer un commit automatique.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, STRICTEMENT EN LECTURE SEULE :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA VICTORIA 3 1.13, STRICTEMENT EN LECTURE SEULE :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d’entrée requis

- `HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT_COMPLETE`
- `OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_DECISION_RECORDED`
- `SICK_MAN_EIGHT_JE_PINNING_1_13_DECISION_RECORDED`
- `OTTOMAN_TANZIMAT_START_DISABLED_IN_1776_PRESERVED`
- `OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`
- `SICK_MAN_EIGHT_JE_PINNING_CAN_BE_ALIGNED_INDEPENDENTLY`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md`

6A.9R doit avoir été commitée manuellement. Ne commence jamais 6A.9F depuis
son worktree non commité.

## Objectif unique

Dans :

`common/journal_entries/00_sick_man.txt`

remplacer exactement huit occurrences de :

```txt
should_be_pinned_by_default = yes
```

par :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

Ne modifier aucune autre ligne et ne changer aucune activation.

## Préflight Git obligatoire

Exécute :

```powershell
Set-Location "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork"

git rev-parse --show-toplevel
git branch --show-current
git status --short
git log -5 --oneline --decorate
git diff --check
git diff --cached --name-only
git stash list
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md
```

Exige :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.9R et tous ses verdicts dans le HEAD ;
- 6A.9R commitée manuellement ;
- worktree suivi propre et index staged vide ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` non suivis ;
- stash exact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- aucun processus Victoria 3, dowser ou Paradox.

Avant écriture, enregistrer les SHA-256 de `bject` et des sept fichiers de
`docs/research/technology/`.

Verdicts bloquants :

- `BLOCKED_WRONG_BRANCH`
- `BLOCKED_6A9R_NOT_COMMITTED`
- `BLOCKED_DIRTY_TREE`
- `BLOCKED_STAGED_FILES`
- `BLOCKED_UNEXPECTED_UNTRACKED_FILES`
- `BLOCKED_PROTECTED_STASH_MISSING`
- `BLOCKED_GAME_PROCESS_RUNNING`

Interdictions Git : aucun reset, restore, checkout de fichier, clean, merge,
rebase, amend, commit automatique, stash apply/pop/drop ou inspection du
contenu du stash.

## Hashes obligatoires

Avant correction :

| Arbre | SHA-256 de `00_sick_man.txt` |
| --- | --- |
| Fork | `DC6AC302555035C574CFC61A91FBF667BE981FEFA2C1D8FA271A6F530B3054D8` |
| Source hotfix | `E48405BFABB52F6CE757880E436C8D44C67111E246AF3215FD3F96EC4F3477F9` |
| Vanilla 1.13 | `1EAD43BE40DAF22D585712442AFD379C893C3075007CDA0AADDB126CCF1DCA41` |

Hash fork exact attendu après les huit substitutions :

`B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A`

Recalcule les trois hashes avant écriture et arrête avec
`BLOCKED_THREE_WAY_EVIDENCE_CHANGED` au moindre écart.

Vérifie aussi, avant et après :

- histoire ottomane :
  `81ABC8DEA9DE93EC6A4DD417FD05FD6859F3122758D2B27E712B1880013F9CA9` ;
- Grande Crise orientale :
  `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` ;
- événements Sick Man :
  `D110D1FD83CD98E131D4C2769B606CC908F17844EFF88EF65F51FEBF313A0C2B` ;
- événements Tanzimat :
  `F5DAABC9D36BEAE714E5BDFC3B156995B3EAE7758004CE3C7B8C3512BA80AD30`.

## Huit objets et substitutions exactes

| Objet | Ligne fork avant correction |
| --- | ---: |
| `je_sick_man_main` | 91 |
| `je_sick_man_syria` | 178 |
| `je_sick_man_egypt` | 222 |
| `je_sick_man_economy` | 258 |
| `je_sick_man_education` | 306 |
| `je_sick_man_separatism` | 388 |
| `je_sick_man_army` | 449 |
| `je_sick_man_bureaucracy` | 499 |

Chaque objet doit recevoir exactement la même nouvelle propriété. Aucun objet
ne doit être omis et aucune neuvième occurrence ne doit être touchée.

## Exclusions absolues du diff gameplay

Ne pas :

- restaurer ou déclencher `sick_man.1` ;
- décommenter les deux modificateurs ;
- modifier `common/history/countries/tur - ottoman empire.txt` ;
- modifier une condition, variable, pulse, événement, timeout, poids,
  visibilité, transfert ou progression ;
- importer le modificateur Syrie ;
- ajouter les vérifications `subject_type_puppet` ;
- commenter ou décommenter `egyptian_crisis_events.1` ;
- corriger les diagnostics `tanzimat_events.5`, `.9` ou `.10` ;
- modifier `05_great_eastern_crisis.txt` ou Grand Collapse ;
- ajouter une localisation ;
- commencer le backlog d’activation différée ;
- importer le fichier source ou vanilla complet.

Tout changement gameplay hors des huit lignes impose
`BLOCKED_SCOPE_VIOLATION`.

## Méthode d’édition

Éditer uniquement les huit lignes ciblées. Préserver :

- UTF-8 avec BOM ;
- LF uniquement ;
- saut final ;
- 117 accolades ouvrantes et 117 fermantes ;
- toute ligne blanche et indentation hors substitution.

Snapshot attendu après :

- 8 879 octets ;
- 501 LF ;
- zéro CRLF ;
- saut final présent ;
- 117 accolades ouvrantes et 117 fermantes ;
- ancien champ : zéro occurrence ;
- nouveau champ : huit occurrences.

## Validations statiques

Prouver :

1. hash final exact ;
2. un fichier gameplay modifié ;
3. huit objets ;
4. huit substitutions ;
5. ancien champ absent du fichier ;
6. nouveau champ présent exactement huit fois ;
7. diff limité aux huit lignes ;
8. aucune activation changée ;
9. zéro localisation requise ;
10. histoire ottomane, Grande Crise et événements inchangés ;
11. source hotfix et vanilla inchangées ;
12. `git diff --check` propre ;
13. index staged vide ;
14. protections et stash intacts.

Le diff attendu est un fichier, huit suppressions et huit additions, dans huit
objets. Les regroupements exacts du diff unifié doivent être consignés; ne pas
forcer artificiellement le nombre de blocs `@@`.

## Baseline parser et smoke humain

Le `debug.log` historique 6A.8F contient exactement huit erreurs ciblées :

```text
00_sick_man.txt near line 91
00_sick_man.txt near line 178
00_sick_man.txt near line 222
00_sick_man.txt near line 258
00_sick_man.txt near line 306
00_sick_man.txt near line 388
00_sick_man.txt near line 449
00_sick_man.txt near line 499
```

Après le PASS statique, préparer une fiche pour un seul smoke parser humain :

1. confirmer que Victoria 3 et le launcher sont fermés ;
2. noter les timestamps/hashes des logs existants ;
3. demander à l’opérateur de monter le fork et `dlc014_ip3` ;
4. lancer une partie neuve 1776, sans console ;
5. atteindre l’écran de jeu puis fermer normalement jeu et launcher ;
6. confirmer explicitement la fermeture ;
7. transmettre les observations.

Codex s’arrête alors avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

Codex ne lance ni jeu ni launcher. Il n’analyse les nouveaux logs qu’après
confirmation humaine de fermeture. Aucun PASS runtime sans compte rendu humain.

Après le smoke, prouver :

- fork et `dlc014_ip3` montés ;
- huit erreurs ciblées avant, zéro après ;
- aucun nouveau diagnostic de pinning dans `00_sick_man.txt`.

Les diagnostics d’ID Tanzimat déjà connus sont hors périmètre et ne doivent pas
être présentés comme causés ou corrigés par le pinning.

## Périmètre documentaire

Après le fichier gameplay unique, seuls les six documents de phase suivants
peuvent être modifiés ou créés :

1. `docs/reports/hotfix/_index/HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md`
2. `docs/reports/hotfix/INDEX.md`
3. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
4. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
6. `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Le futur prompt doit sélectionner la phase suivante sans la commencer.

## Rapport requis

Le rapport 6A.9F doit contenir :

- date, branche, HEAD initial/final et état Git ;
- préflight et hashes protégés ;
- hashes trois voies et hash final ;
- snapshot encodage/structure ;
- tableau des huit objets ;
- diff exact ;
- comptage parser 8 → 0 ;
- preuve de montage et compte rendu humain ;
- exclusions et non-régressions ;
- rollback ;
- documents modifiés ;
- état Git final ;
- décision de commit manuel ;
- verdicts.

## Rollback exact

Remplacer exactement les huit occurrences de :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

par :

```txt
should_be_pinned_by_default = yes
```

Le rollback doit restaurer le hash :

`DC6AC302555035C574CFC61A91FBF667BE981FEFA2C1D8FA271A6F530B3054D8`

Ne jamais restaurer le fichier complet.

## Protections

Ne rouvrir aucun bloc clos ni aucun élément DEI/VOC, Java, Balkan National
Awakening, Yugoslavia, Risorgimento, nationalisme grec, Grande Crise orientale,
Merchant Banking, Navigation Acts, NAVY, formations, MARATH, Inde, BIC, Sepoy,
ADMIN, Japon, Russie, Autriche, Croatie, Suisse, révolutions, technologies,
recherche, agriculture, alimentation, industrie, localisations générales,
descripteurs, launcher, sauvegardes ou `bject`.

Préserver dans BIC :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer :

```txt
law_colonial_exploitation
```

## Contrôles finaux

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

Confirmer :

- un fichier gameplay et six documents de phase seulement ;
- huit lignes gameplay seulement ;
- aucun staged ;
- huit hashes protégés inchangés ;
- stash exact intact ;
- aucun processus interdit ;
- aucun commit automatique ;
- aucune activation Tanzimat ;
- aucune phase suivante commencée.

## Verdicts attendus

Avant runtime humain :

- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_STATIC_PASS`
- `SICK_MAN_EIGHT_JE_PINNING_EIGHT_HUNK_1_13_ALIGNMENT_COMPLETE`
- `OTTOMAN_TANZIMAT_START_DISABLED_IN_1776_PRESERVED`
- `NO_TANZIMAT_ACTIVATION_CHANGED`
- `RUNTIME_OPERATOR_ACTION_REQUIRED`

Après compte rendu et logs humains conformes :

- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_RUNTIME_PASS`
- `SICK_MAN_EIGHT_JE_PINNING_PARSER_ERRORS_8_TO_0`
- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT_COMPLETE`
- `OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = <phase documentaire sélectionnée>`

Ne committe rien automatiquement.
