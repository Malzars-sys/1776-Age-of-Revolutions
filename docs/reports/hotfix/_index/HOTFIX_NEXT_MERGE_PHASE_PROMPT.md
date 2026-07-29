# Phase HOTFIX-6A.6 — Sélection du prochain résidu global

FORK :
`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, LECTURE SEULE :
`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, LECTURE SEULE :
`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d’entrée

- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_COMPLETE`
- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_RUNTIME_PASS`
- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md`

## Objectif unique

Sélectionner exactement un prochain sous-bloc atomique parmi les résidus
globaux encore ouverts. Cette phase est strictement documentaire : ne modifier
aucun gameplay et ne commencer aucun correctif.

Comparer notamment :

- les 20 migrations de pinning 1.13 restantes ;
- Merchant Banking pour GEN/VEN ;
- Navigation Acts pour GBR/HBC/NBS/ONT/ORA ;
- les 87 lignes `UNKNOWN_REQUIRES_REVIEW`.

Publier exactement trois candidats et en sélectionner un seul.

## Préflight obligatoire

Exécuter :

```powershell
git rev-parse --show-toplevel
git branch --show-current
git status --short
git log -5 --oneline --decorate
git diff --check
git diff --cached --name-only
git stash list
```

Exiger :

- branche `hotfix-dlc-audit` ;
- rapport 6A.5F présent dans HEAD après commit manuel ;
- aucun fichier suivi modifié ou staged ;
- seuls `bject` et les sept fichiers de
  `docs/research/technology/` non suivis ;
- stash exact NAVY-3C-3 intact ;
- Victoria 3 et le launcher fermés.

En cas d’écart, s’arrêter avec un verdict bloquant précis. Ne faire aucun
reset, restore, checkout, clean, merge, rebase, amend, commit automatique,
stash apply/pop/drop ou inspection du stash.

## Sources obligatoires

Lire intégralement :

- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les changelogs fork et source hotfix ;
- les journaux existants de 6A.5F, sans lancer le jeu.

Comparer tout candidat sérieux dans le fork, la source hotfix et le vanilla
1.13. Une égalité de nom ou une différence de hash ne suffit pas.

## Base actualisée

Après clôture de 6A.5F, les 161 anciennes lignes `PENDING_REVIEW` se
répartissent ainsi :

- 7 `REQUIRED_HOTFIX_DELTA` ;
- 20 `VANILLA_1_13_ALIGNMENT_REQUIRED` ;
- 14 `ALREADY_MERGED` ;
- 3 `INTENTIONAL_FORK_DIVERGENCE` ;
- 1 `OBSOLETE_HOTFIX_CONTENT` ;
- 10 `POST_MERGE_DESIGN_BACKLOG` ;
- 19 `PROTECTED_CONCURRENT_WORK` ;
- 87 `UNKNOWN_REQUIRES_REVIEW`.

Il reste 114 lignes directement exploitables par une revue, sans que cela
signifie 114 correctifs. L’ancien total de 26 deltas à haute confiance reste
`UNVERIFIED`.

## Critères de sélection

Le sous-bloc choisi doit avoir :

- un problème unique et prouvé ;
- un petit nombre de fichiers, objets et hunks ;
- une comparaison trois voies claire ;
- aucun chevauchement protégé ;
- un rollback exact ;
- des contrôles statiques précis ;
- un protocole humain si un runtime est nécessaire.

Ne pas créer de lot massif de pinning et ne pas combiner plusieurs candidats.

## Protections absolues

Ne sélectionner ni modifier DEI/VOC, Java, Balkan National Awakening,
`05_creation_of_yugoslavia.txt`, NAVY, formations, MARATH/SAT/KHP,
Travancore, Inde/BIC/Sepoy/Bombay, ADMIN, Japon, Russie,
Autriche/Croatie/Suisse, Révolutions américaine ou française, lettres de Kew,
technologies, recherches technologiques, localisations françaises générales,
agriculture, alimentation, industrie, descripteurs, launcher, sauvegardes ou
`bject`.

Préserver `law_frontier_colonization` pour BIC et ne jamais restaurer
`law_colonial_exploitation`.

## Fichiers modifiables

Documentation uniquement :

- `docs/reports/hotfix/_index/HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`
- `docs/reports/hotfix/INDEX.md`
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Aucun fichier gameplay n’est modifiable.

## Tests en jeu

Ne jamais lancer, piloter ou automatiser Victoria 3 ou le launcher. Aucun
runtime n’est nécessaire pendant cette sélection.

Toute future phase nécessitant un runtime doit préparer une fiche humaine puis
s’arrêter à :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

## Livrables et verdicts

Créer le rapport 6A.6 avec l’inventaire actualisé, les erreurs existantes, les
exclusions, la comparaison des candidats, un tableau de trois candidats, un
choix unique, son périmètre fermé et son rollback.

Après sélection valide :

- `HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = <phase sélectionnée>`

Remplacer ce prompt par celui de la phase sélectionnée. Ne pas exécuter cette
phase dans la même session et ne rien committer automatiquement.
