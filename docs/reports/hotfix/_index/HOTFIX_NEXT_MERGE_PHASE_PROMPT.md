# Prompt autonome — HOTFIX-6A.16R audit fonctionnel des API d'événements Coup

Nous poursuivons le portage du mod Victoria 3 :

`1776_Age_of_Revolutions_fork`

# Phase HOTFIX-6A.16R — Audit fonctionnel 1.13 des API d'événements Coup

## 1. Nature et objectif unique

Auditer en lecture seule les diagnostics d'API obsolète dans :

- `events/iberia_events/ip4_coup_events.txt`;
- `events/agitators_events/coup_events.txt`.

Comparer chaque groupe fonctionnel du fork à la source hotfix et à vanilla
1.13. Classer chaque groupe sans modifier le gameplay. Sélectionner au plus une
future correction atomique uniquement si son périmètre exact est démontré.

Cette phase ne corrige rien, ne lance aucun runtime, ne stage rien et ne crée
aucun commit automatique.

## 2. Chemins

Fork :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

Source hotfix, lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

Vanilla 1.13, lecture seule :

`C:\Games\Victoria 3 The Great Wave\game`

Logs, lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs`

Branche obligatoire :

`hotfix-dlc-audit`

## 3. État d'entrée

Exiger que le rapport 6A.16 soit présent dans `HEAD` après commit manuel :

`docs/reports/hotfix/_index/HOTFIX_6A16_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

Verdicts d'entrée obligatoires :

```text
HOTFIX_6A16_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE
POST_6A15F_RESIDUAL_DIAGNOSTICS_REINDEXED
RESIDUAL_CANDIDATE_PRIORITY_MATRIX_COMPLETE
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
COUP_EVENT_APIS_1_13_AUDIT_SELECTED
NEXT_EXECUTION_PHASE = HOTFIX_6A16R_COUP_EVENT_APIS_1_13_FUNCTIONAL_AUDIT
```

Ne jamais commencer depuis un worktree documentaire 6A.16 non commité.

## 4. Préflight Git

Exécuter :

```powershell
git rev-parse --show-toplevel
git branch --show-current
git status --short
git log -5 --oneline --decorate
git diff --check
git diff --cached --name-only
git stash list
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A16_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
```

Exiger :

- racine et branche exactes;
- rapport et dix verdicts 6A.16 dans `HEAD`;
- fichiers suivis propres;
- index staged vide;
- uniquement `bject` et les sept recherches technologiques non suivis;
- aucun processus Victoria 3, dowser ou Paradox;
- stash exact
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`;
- objet du stash
  `518df704fa14599c0f254fae13859210663dd976`.

Arrêts :

```text
BLOCKED_WRONG_BRANCH
BLOCKED_6A16_NOT_COMMITTED
BLOCKED_DIRTY_TREE
BLOCKED_STAGED_FILES
BLOCKED_UNEXPECTED_UNTRACKED_FILES
BLOCKED_PROTECTED_STASH_MISSING
BLOCKED_GAME_PROCESS_RUNNING
BLOCKED_THREE_WAY_EVIDENCE_CHANGED
```

## 5. Preuves d'entrée

### `ip4_coup_events.txt`

| Version | SHA-256 |
| --- | --- |
| Fork | `8DD5A07F60A3E1C623CF48495B062AFE0388602E256CBA8384CD8540067B5AD2` |
| Source | `F806A772F86EB379EBC7ED05F7808A5B16C0CACFC0CD784E94B6AA1FB9C8C9D4` |
| Vanilla | `22A7B94EE4A0CB4DA7C31DA2F488CEB845473EBDF44EB32ED649F56200886E92` |

Huit diagnostics PostValidate `has_role` sont attendus aux lignes fork 30,
31, 56, 57, 321, 332, 426 et 432, dans `ip4_coup.1` et `ip4_coup.2`.

### `coup_events.txt`

| Version | SHA-256 |
| --- | --- |
| Fork | `88D1B0AE45F296A84FBB997C3F089423A2240790742291DDE359A9509DA5F3CE` |
| Source | `AEE3D155D3C347AC5338468F5814CC5DAAFCBB9862E801D3287643587D525990` |
| Vanilla | `F1CD65506555E45D1C08C27EAA96EE6939F94D313DC44DFC2B20DD4E3106CB7F` |

Deux diagnostics PostValidate `has_role` et six
`Unknown trigger type: is_ruler` sont attendus dans `coup_pulse_events.1` et
`coup_aftermath_events.1` à `.4`.

Total courant attendu : 16 diagnostics, deux fichiers, sept objets et environ
neuf groupes API à résoudre.

## 6. Lecture obligatoire

Lire intégralement avant toute conclusion :

- `HOTFIX_6A16_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`;
- `HOTFIX_6A15R_COUP_JOURNAL_ENTRY_1_13_FUNCTIONAL_AUDIT.md`;
- `HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT.md`;
- les trois versions des deux fichiers événementiels;
- les entrypoints Coup hérités pertinents :
  scripted effects, triggers, progress bars, on_actions, lobby et action
  diplomatique `orchestrate_coup`;
- les changelogs complets du fork et de la source;
- la roadmap et les deux CSV de navigation;
- les journaux courants et leurs rotations, sans les additionner aveuglément.

## 7. Méthode d'audit

Pour chaque occurrence obsolète :

1. identifier événement, scope exact, branche et effet aval;
2. comparer fork/source/vanilla au niveau du plus petit groupe fonctionnel;
3. relever le remplacement moderne éventuel;
4. distinguer convergence exacte, convergence partielle et divergence;
5. compter additions, suppressions, objets et hunks théoriques;
6. calculer le hash théorique uniquement pour tout candidat atomique;
7. documenter rollback et critères statiques futurs;
8. classer exclusivement le groupe.

Classes autorisées :

```text
VANILLA_1_13_ALIGNMENT_REQUIRED
REQUIRED_HOTFIX_DELTA
INTENTIONAL_FORK_DIVERGENCE
OBSOLETE_HOTFIX_CONTENT
POST_MERGE_DESIGN_BACKLOG
PROTECTED_CONCURRENT_WORK
UNKNOWN_REQUIRES_REVIEW
ALREADY_MERGED
```

## 8. Séparations fonctionnelles obligatoires

Ne jamais traiter comme une seule masse :

- `has_role` vers `has_role_of_type`;
- `is_ruler` vers `is_ruler_of_own_country`;
- `is_heir_of_own_country`;
- `character_is_valid_for_events`;
- groupe d'intérêt optionnel;
- formules de pondération et sélection de personnage;
- retrait ou conservation de rôle;
- `ip4_coup.11`;
- sponsor et `coup_lobby`;
- scopes, variables et cleanup;
- lois, cooldowns et invalidations.

La source et vanilla ne convergent pas sur tout `ip4_coup_events.txt`.
L'existence d'un remplacement moderne ne prouve donc pas que toutes les
conditions voisines doivent être copiées.

## 9. Interdictions absolues

Ne modifier aucun fichier gameplay, notamment les deux fichiers audités,
`common/journal_entries/01_coup.txt`, les dépendances Coup, lois,
localisations, personnages et histoires pays.

Ne pas toucher à HBC, Navigation Acts, NAVY, MARATH, ADMIN, technologies,
Inde/BIC/Sepoy/Bombay/Travancore, Japon, Russie,
Autriche/Croatie/Suisse, DEI/VOC/Java, révolutions américaine et française,
Merchant Banking, Portugal, Tanzimat, descripteurs, sauvegardes, `bject`,
recherches technologiques ou stash.

BIC doit conserver `law_frontier_colonization`. Ne jamais restaurer
`law_colonial_exploitation`.

Ne jamais exécuter `git add`, reset, restore, checkout de fichier, clean,
merge, rebase, amend, commit, stash apply/pop/drop ou toute modification du
stash.

## 10. Fichiers documentaires autorisés

Créer :

`docs/reports/hotfix/_index/HOTFIX_6A16R_COUP_EVENT_APIS_1_13_FUNCTIONAL_AUDIT.md`

Puis, si nécessaire, mettre à jour uniquement :

- `docs/reports/hotfix/INDEX.md`;
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Si aucune future correction atomique n'est suffisamment prouvée, ne pas
remplacer le prompt par une phase corrective.

## 11. Sortie exigée

Le rapport doit contenir :

- préflight et hashes;
- comptage actuel des 16 diagnostics;
- carte des sept objets et des groupes API;
- comparaison trois voies par groupe;
- dépendances et effets aval;
- classement exclusif de chaque groupe;
- périmètre, diff, hash théorique et rollback de toute future correction
  éventuellement sélectionnée;
- liste explicite des deltas différés;
- confirmation qu'aucun gameplay et aucun runtime n'ont été nécessaires;
- état Git, staging, stash et processus final.

Sélectionner au plus une future phase. Ne pas la commencer.

Verdicts minimaux :

```text
HOTFIX_6A16R_COUP_EVENT_APIS_1_13_FUNCTIONAL_AUDIT_COMPLETE
COUP_EVENT_APIS_THREE_WAY_COMPARISON_COMPLETE
COUP_EVENT_API_GROUPS_CLASSIFIED
COUP_LOBBY_SPONSOR_CLEANUP_DELTAS_SEPARATED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
```

Ajouter soit :

```text
NO_NEXT_EXECUTION_PHASE_SELECTED
```

soit exactement une ligne :

```text
NEXT_EXECUTION_PHASE = <phase corrective atomique prouvée>
```
