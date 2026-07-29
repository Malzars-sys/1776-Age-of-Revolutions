# Prompt autonome — HOTFIX-6A.11F Alignement de deux pinning du colonialisme portugais

Nous poursuivons le portage du mod Victoria 3 :

`1776_Age_of_Revolutions_fork`

# Phase HOTFIX-6A.11F — Alignement Victoria 3 1.13 de deux pinning du colonialisme portugais

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Nature de la phase

Cette phase applique exactement deux substitutions d'API dans un fichier de
journal entries, effectue tous les contrôles statiques, puis prépare un seul
runtime humain condensé. Codex ne doit jamais lancer Victoria 3, lancer ou
piloter le launcher, cliquer dans le jeu, utiliser la console, ouvrir une
sauvegarde, créer un commit automatique, ni étendre le périmètre.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, strictement en lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, strictement en lecture seule :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d'entrée requis

- `HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

6A.11 doit être commitée manuellement avant de commencer. Ne jamais commencer
depuis son worktree documentaire non commité.

## Objectif unique

Dans `common/journal_entries/06_portuguese_colonialism.txt`, remplacer
exactement :

```txt
should_be_pinned_by_default = yes
```

par :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

une fois dans `je_portuguese_colonialism` et une fois dans
`je_the_pink_map`. Ne modifier aucun autre octet gameplay.

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
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
```

Exiger :

- racine exacte et branche `hotfix-dlc-audit`;
- rapport et verdicts 6A.11 présents dans `HEAD`;
- fichiers suivis propres et index staged vide;
- seuls `bject` et les sept fichiers de `docs/research/technology/` non suivis;
- stash exact
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`;
- aucun processus Victoria 3, `dowser` ou Paradox.

Arrêter avec le verdict précis en cas d'écart :

- `BLOCKED_WRONG_BRANCH`
- `BLOCKED_6A11_NOT_COMMITTED`
- `BLOCKED_DIRTY_TREE`
- `BLOCKED_STAGED_FILES`
- `BLOCKED_UNEXPECTED_UNTRACKED_FILES`
- `BLOCKED_PROTECTED_STASH_MISSING`
- `BLOCKED_GAME_PROCESS_RUNNING`

Interdictions Git : reset, restore, checkout de fichier, clean, merge, rebase,
amend, commit automatique, stash apply/pop/drop et inspection du stash.

## Hashes de référence obligatoires

| Preuve | SHA-256 |
| --- | --- |
| Fork `06_portuguese_colonialism.txt` avant correction | `6FEF16A90E2E133CC82A912F40944E50E26B65FD524B5898086CF47557DA2894` |
| Source hotfix | `04CCCCF13E9D7B4EA1DBBB29F86861CA8B1DB7F77B635175A39D889B9234EE7A` |
| Vanilla 1.13 | `15834E8FE1DBA56ADD9D970F9CECDF8AD1FB45100585770A457DF96BDF65FDF4` |
| Fork après les deux seules substitutions | `DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20` |
| BIC fork | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` |

Vérifier aussi les sept hashes technologie consignés dans 6A.11. Tout écart
avant correction impose `BLOCKED_THREE_WAY_EVIDENCE_CHANGED`. Source et
vanilla restent strictement inchangées.

## Sources obligatoires

Lire intégralement :

- le rapport 6A.11;
- les rapports 6A.10F et 6A.10;
- roadmap, block status et report index;
- les trois versions du fichier cible;
- les localisations vanilla anglaises et françaises
  `ip4_portuguese_colonialism`;
- les nouveaux logs 6A.10F et rotations, en lecture seule.

Ne pas lancer le jeu pour créer une preuve.

## Snapshot pré-correction obligatoire

Exiger exactement :

| Ligne fork | Objet | Ancienne propriété |
| ---: | --- | --- |
| 6 | `je_portuguese_colonialism` | `should_be_pinned_by_default = yes` |
| 181 | `je_the_pink_map` | `should_be_pinned_by_default = yes` |

Exiger exactement deux anciennes occurrences dans le fichier, et aucune
propriété moderne avant correction. Enregistrer le hash et le contexte des
deux blocs.

## Périmètre d'écriture fermé

Seuls ces six fichiers peuvent être modifiés ou créés :

1. `common/journal_entries/06_portuguese_colonialism.txt`
2. `docs/reports/hotfix/_index/HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT.md`
3. `docs/reports/hotfix/INDEX.md`
4. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
6. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`

Ne pas modifier ce prompt pendant 6A.11F. Tout autre changement impose
`BLOCKED_SCOPE_VIOLATION`.

## Hunks exacts

Hunk 1, objet `je_portuguese_colonialism`, ancienne ligne 6 :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Hunk 2, objet `je_the_pink_map`, ancienne ligne 181 :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Diff attendu : un fichier, deux objets, deux hunks, deux additions et deux
suppressions. Ne jamais remplacer le fichier complet.

## Exclusions adjacentes absolues

Ne pas importer depuis la source :

- `region_equatorial_africa`;
- `region_east_africa`;
- le filtre de culture portugaise;
- `geographic_region_iberia_old`;
- la prise en charge de `c:IBE` dans le lobby;
- espaces, commentaires ou changements de formatage adjacents.

Ne modifier aucun scope, trigger, rôle, tooltip, visibilité, DLC, géographie,
poids, transfert, progression, localisation ou autre journal entry.

## Protections absolues

Ne toucher à aucun élément DEI/VOC, Java, NAVY, MARATH, SAT, KHP, Travancore,
Inde/BIC/Sepoy/Bombay, ADMIN, Japon, Russie, Autriche/Croatie/Suisse,
révolutions américaine ou française, technologies, recherche, agriculture,
alimentation, industrie générale, descripteur, launcher, sauvegarde, `bject`,
Tanzimat, Sick Man, Grande Crise orientale, Balkans clos ou Romania.

BIC doit conserver :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer `law_colonial_exploitation`.

## Validations statiques obligatoires

Après correction, exiger :

1. hash cible
   `DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20`;
2. zéro ancienne propriété dans le fichier;
3. exactement deux propriétés modernes;
4. objets propriétaires exacts;
5. diff limité à deux hunks et `2/2`;
6. accolades équilibrées;
7. BOM et fins de ligne préservés;
8. les quatre clés de titre/raison disponibles en anglais et français;
9. aucune modification source/vanilla;
10. hashes BIC, `bject`, technologie et stash inchangés;
11. aucun processus de jeu;
12. `git diff --check` propre et index staged vide.

Si le hash cible n'est pas atteint, ne pas reformater : annuler les deux
substitutions puis diagnostiquer.

## Rollback exact

Dans les deux objets seulement, remplacer :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

par :

```txt
should_be_pinned_by_default = yes
```

Le rollback doit restaurer le hash
`6FEF16A90E2E133CC82A912F40944E50E26B65FD524B5898086CF47557DA2894`.

## Runtime humain obligatoire

Après tous les contrôles statiques et la fiche opérateur rédigée, Codex doit
s'arrêter avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

La fiche humaine doit demander un seul lancement avec le fork monté et
`dlc014_ip3`, une nouvelle partie avec le Portugal au 1er janvier 1776, puis
une progression au 2 janvier 1776. Vérifier :

- chargement sans anomalie;
- journal potentiel lisible;
- titres portugais sans clé brute;
- aucune anomalie de pinning ou visibilité;
- fermeture complète du jeu et du launcher;
- compte rendu humain explicite.

Codex ne lance et ne pilote rien. Après confirmation de fermeture, lire les
nouveaux logs seulement. Le PASS attendu est :

- erreurs ciblées dans le fichier : `2 → 0`;
- baseline globale attendue : `376 → 374`;
- fichiers uniques attendus : `141 → 140`;
- zéro rejet de la propriété moderne cible;
- montage du fork et de `dlc014_ip3` prouvé.

Aucun PASS runtime ne peut être déclaré sans compte rendu humain.

## Livrables

Le rapport 6A.11F doit contenir préflight, hashes, snapshot, comparaison trois
voies, diff exact, exclusions, validations statiques, fiche humaine, compte
rendu humain, logs post-runtime, évolution parser, montage, protections,
rollback, état Git initial/final et décision de commit manuel.

Mettre à jour les quatre documents de navigation autorisés. Ne créer aucun
commit.

## Verdicts

Après statique :

- `HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_STATIC_PASS`
- `PORTUGUESE_COLONIALISM_TWO_JE_PINNING_TWO_HUNK_1_13_ALIGNMENT_COMPLETE`
- `PORTUGUESE_COLONIALISM_VISIBILITY_GEOGRAPHY_AND_PROGRESSION_UNCHANGED`
- `RUNTIME_OPERATOR_ACTION_REQUIRED`

Après runtime humain et analyse des logs :

- `HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_RUNTIME_PASS`
- `PORTUGUESE_COLONIALISM_TWO_JE_PINNING_PARSER_ERRORS_2_TO_0`
- `PORTUGUESE_COLONIALISM_1776_VISIBILITY_GEOGRAPHY_AND_PROGRESSION_UNCHANGED`
- `HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

En cas d'échec :

- `HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT_FAIL`
- verdict de blocage précis.

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

Confirmer un seul fichier gameplay, exactement cinq documents, aucun autre
fichier, source/vanilla intactes, BIC intact, huit hashes protégés intacts,
stash intact, aucun processus de jeu, aucun lancement par Codex et aucun
commit automatique.
