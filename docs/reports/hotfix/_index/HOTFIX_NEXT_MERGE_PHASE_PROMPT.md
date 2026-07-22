# Phase HOTFIX-6A.2R — Résolution des hunks Suisse et NAVY

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé.

## Verdict d’entrée

`NEXT_MERGE_BLOCK = HOTFIX-6A_GLOBAL_SCRIPT_DELTAS`  
`NEXT_EXECUTION_PHASE = HOTFIX_6A2R_TARGET_HUNK_RESOLUTION`
`BLOCKED_TARGET_HUNKS_UNVERIFIED`

## Chemins

- Fork : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`
- Source hotfix, lecture seule : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`
- Vanilla 1.13, lecture seule : `C:\Games\Victoria 3 The Great Wave\game`

## Objectif unique

Résoudre statiquement les deux blockers laissés par HOTFIX-6A.2 avant toute correction territoriale :

1. déterminer si le `region_state:AUS` de 30 000 South Germans dans `STATE_EAST_SWITZERLAND` est un transfert légitime ou une inflation de population;
2. définir un hunk NAVY compatible avec le fork actuel pour le shipyard Croatia, la flotte AUS et l’armée `generalkommando_agram`, sans copier le bloc hotfix.

Ne modifier aucun gameplay pendant 6A.2R.

## Contrôles initiaux

Exécuter `git rev-parse --show-toplevel`, `git branch --show-current`, `git status --short`, `git log -1 --oneline`, `git diff --check`, `git diff --cached --name-only` et `git stash list`. Exiger `hotfix-dlc-audit`, arbre suivi propre, seul `docs/research/technology/` non suivi, stash MARATH intact, Victoria 3 et launcher fermés.

## Sources prioritaires

- `docs/reports/hotfix/_index/HOTFIX_6A2_AUSTRIA_CROATIA_WEST_SWITZERLAND_AUDIT.md`
- `docs/reports/hotfix/_index/HOTFIX_6A2_AUSTRIA_CROATIA_WEST_SWITZERLAND_DELTA_MAP.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
- rapports sous `docs/reports/navy/`
- les trois versions de `common/history/pops/00_west_europe.txt`
- les trois versions de `common/history/buildings/01_south_europe.txt`
- les trois versions de `common/history/military_formations/00_military_formations_europe.txt`

Utiliser `Get-ChildItem`, `Get-FileHash`, `Get-Content`, `Compare-Object`, `Select-String`, `git log` et `git blame`. Ne pas utiliser `rg`.

## Audit population suisse

Confirmer les totaux SWI avant et après, le lien exact de `x90C0E0` avec `STATE_EAST_SWITZERLAND`, et rechercher une preuve source expliquant les 30 000 South Germans. Choisir exactement :

- transfert de 30 000 depuis un groupe SWI existant avec réduction correspondante;
- ajout hotfix intentionnel prouvé;
- omission du hunk population avec justification de compatibilité;
- `BLOCKED_SWISS_POPULATION_UNVERIFIED`.

Documenter valeurs avant/après et conservation de la population totale.

## Audit NAVY

Comparer la source aux commits NAVY du fork. Ne jamais remplacer `00_military_formations_europe.txt` ou `01_south_europe.txt`. Définir séparément :

- nécessité du shipyard et ownership compatible;
- nécessité et composition de la flotte AUS;
- migration ou suppression du bloc CRO;
- conservation des types, comptes, HQ et state regions compatibles 1.13;
- absence de doublon avec les flottes/armées existantes.

Toute proposition doit être un hunk minimal reconstruit depuis le fork, avec rollback exact.

## Protections absolues

Ne toucher ni à MARATH/SAT/KHP, NAVY existant, ADMIN, BIC, Travancore, Russie, Mamluk Iraq, Japon, Inde, localisations françaises, `docs/research/technology/`, stash ou sauvegardes. Conserver `law_frontier_colonization`; ne jamais restaurer `law_colonial_exploitation`.

Interdictions : aucun `stash apply/pop/drop`, `git reset`, `git restore`, `git checkout` de fichier, `git clean`, `git add .`, import complet ou commit automatique.

## Fichiers modifiables

Documentation uniquement :

- créer `docs/reports/hotfix/_index/HOTFIX_6A2R_TARGET_HUNK_RESOLUTION.md`;
- mettre à jour `docs/reports/hotfix/_index/HOTFIX_6A2_AUSTRIA_CROATIA_WEST_SWITZERLAND_DELTA_MAP.csv`;
- mettre à jour uniquement la navigation/roadmap sous `docs/reports/hotfix/`.

Aucun fichier sous `common/`, `events/`, `map_data/` ou `localization/` n’est modifiable.

## Sortie attendue

Publier exactement un verdict :

- `READY_FOR_AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX` si les deux blockers sont résolus;
- `BLOCKED_SWISS_POPULATION_UNVERIFIED`;
- `BLOCKED_NAVY_ARCHITECTURE_CONFLICT`;
- `BLOCKED_TARGET_HUNKS_UNVERIFIED`.

Si READY, produire le prompt de correction avec liste fermée des fichiers et hunks, ordre exact, tests statiques, rollback et un seul runtime planifié après tous les tests. Ne pas appliquer la correction pendant 6A.2R.

## Runtime

Zéro lancement pendant 6A.2R. Le futur correctif devra préparer un lancement unique couvrant ownership, sujets, pops, bâtiments, flotte/armée, accès côtier et logs.

## Vérifications finales

Exiger zéro staged, uniquement les documents autorisés, aucun gameplay, `git diff --check` propre, fichier Russie inchangé, stash et recherche intacts, Victoria 3 non lancé. Ne pas committer automatiquement.
