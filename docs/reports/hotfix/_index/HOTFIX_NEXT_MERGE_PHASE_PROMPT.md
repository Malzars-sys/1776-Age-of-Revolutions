# Prompt autonome — HOTFIX-6A.15F pinning de `je_ip4_coup`

Nous poursuivons le portage du mod Victoria 3 :

`1776_Age_of_Revolutions_fork`

# Phase HOTFIX-6A.15F — Alignement 1.13 du pinning de la journal entry Coup

## 1. Nature et objectif unique

Appliquer exactement une substitution de propriété dans
`common/journal_entries/01_coup.txt`, objet `je_ip4_coup` :

```txt
should_be_pinned_by_default = yes
```

vers :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

La phase ne doit absorber aucun delta adjacent d'événement, scope, lobby, loi,
cooldown, cleanup, invalidation, personnage ou équilibre.

Codex ne lance ni ne pilote Victoria 3 ou le launcher, n'utilise pas la
console, n'ouvre aucune sauvegarde, ne crée aucun commit automatique et ne
commence aucune autre correction Coup.

## 2. Chemins

Fork :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

Source hotfix, lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

Vanilla 1.13, lecture seule :

`C:\Games\Victoria 3 The Great Wave\game`

Branche obligatoire :

`hotfix-dlc-audit`

## 3. État d'entrée

Exiger que le rapport suivant soit présent dans `HEAD`, après commit manuel de
6A.15R :

`docs/reports/hotfix/_index/HOTFIX_6A15R_COUP_JOURNAL_ENTRY_1_13_FUNCTIONAL_AUDIT.md`

Verdicts d'entrée obligatoires :

```text
HOTFIX_6A15R_COUP_JOURNAL_ENTRY_1_13_FUNCTIONAL_AUDIT_COMPLETE
COUP_JOURNAL_ENTRY_THREE_WAY_COMPARISON_COMPLETE
COUP_PINNING_SCOPE_LOBBY_LAW_COOLDOWN_AUDITED
COUP_JOURNAL_ENTRY_PINNING_ISOLATABLE_ADJACENT_DELTAS_DEFERRED
NEXT_EXECUTION_PHASE = HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT
```

Ne jamais commencer depuis le worktree documentaire non commit de 6A.15R.

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
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A15R_COUP_JOURNAL_ENTRY_1_13_FUNCTIONAL_AUDIT.md
```

Exiger :

- racine et branche exactes;
- 6A.15R dans `HEAD`;
- fichiers suivis propres;
- index staged vide;
- uniquement `bject` et `docs/research/technology/` non suivis;
- aucun processus Victoria 3, dowser ou Paradox;
- stash exact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`;
- hash objet du stash :
  `518df704fa14599c0f254fae13859210663dd976`.

Arrêts :

```text
BLOCKED_WRONG_BRANCH
BLOCKED_6A15R_NOT_COMMITTED
BLOCKED_DIRTY_TREE
BLOCKED_STAGED_FILES
BLOCKED_UNEXPECTED_UNTRACKED_FILES
BLOCKED_PROTECTED_STASH_MISSING
BLOCKED_GAME_PROCESS_RUNNING
BLOCKED_THREE_WAY_EVIDENCE_CHANGED
```

## 5. Hashes et hunk exacts

| Preuve | SHA-256 |
| --- | --- |
| fork avant | `3AB98023990198A9871FAEE3CF459558B36FECC11B927F1FCF34982A39E5FB2F` |
| source | `F39D26651A3200B1044A2E79D070A8BFEEBB205183079A9BB993EF6D520C5665` |
| vanilla 1.13 | `3E4705DFC02785CED86F9C5967CDDC0D5AC0E411E30974F82052ACD4004C7ACB` |
| fork attendu après | `37C2669619CD26C30450F41082716BF30CA12949AA5FEE59BA0D25D498339602` |

Hunk autorisé :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Diff gameplay attendu : un fichier, un objet, un hunk, une addition et une
suppression. Taille attendue : `2954` octets.

Préserver exactement BOM UTF-8, LF, saut final, indentation, accolades et
toutes les lignes adjacentes.

## 6. Fichiers modifiables

Avant runtime humain :

1. `common/journal_entries/01_coup.txt`;
2. `docs/reports/hotfix/_index/HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT.md`.

Après runtime et fermeture explicite du jeu/launcher, les documents de
navigation suivants peuvent être mis à jour :

3. `docs/reports/hotfix/INDEX.md`;
4. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`;
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`;
6. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`.

Ne pas modifier ce prompt pendant 6A.15F sauf nécessité documentaire prouvée.

## 7. Interdictions absolues

Ne modifier aucun des fichiers suivants :

- `events/iberia_events/ip4_coup_events.txt`;
- `events/agitators_events/coup_events.txt`;
- scripted effects, triggers, progress bars ou on_actions Coup;
- lobbies et action diplomatique `orchestrate_coup`;
- lois, modificateurs, localisations ou fichiers pays;
- HBC, Navigation Acts, NAVY, MARATH, ADMIN;
- Inde, BIC, Sepoy, Bombay, Travancore;
- Japon, Russie, Autriche/Croatie/Suisse, DEI/VOC/Java;
- révolutions américaine et française;
- Merchant Banking, technologies, descripteurs et sauvegardes;
- `bject`, recherches technologiques et stash.

BIC doit conserver `law_frontier_colonization`. Ne jamais restaurer
`law_colonial_exploitation`.

Ne jamais exécuter `git add`, reset, restore, checkout de fichier, clean,
merge, rebase, amend, stash apply/pop/drop ou commit automatique.

## 8. Application et rollback

Appliquer la substitution avec une édition chirurgicale. Vérifier immédiatement
le hash cible.

Si le hash cible échoue, remplacer uniquement :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

par :

```txt
should_be_pinned_by_default = yes
```

Le rollback doit restaurer exactement le hash initial. Si ce hash n'est pas
restauré :

`BLOCKED_ROLLBACK_MISMATCH`

## 9. Validations statiques

Exiger :

1. ancienne propriété : `0` occurrence dans l'objet;
2. nouvelle propriété : `1` occurrence;
3. hash cible exact;
4. taille `2954`;
5. un fichier, un objet, un hunk, `1+/1-`;
6. aucun changement adjacent;
7. BOM UTF-8, LF, saut final et accolades `49/49`;
8. hashes source et vanilla inchangés;
9. deux fichiers d'événements Coup inchangés;
10. aucune loi, scope, lobby, variable, cooldown ou cleanup modifié;
11. `git diff --check` PASS;
12. index staged vide;
13. stash exact;
14. aucun processus du jeu/launcher.

Baseline connue avant correction :

- 374 diagnostics legacy dans 140 fichiers;
- 1 diagnostic ciblé dans `01_coup.txt:139`;
- diagnostics distincts des événements Coup toujours présents et hors scope.

Après PASS statique, publier :

```text
HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_STATIC_PASS
COUP_JOURNAL_ENTRY_PINNING_ONE_FILE_ONE_OBJECT_ONE_HUNK_ALIGNED
COUP_EVENT_SCOPE_LOBBY_LAW_COOLDOWN_UNCHANGED
RUNTIME_OPERATOR_ACTION_REQUIRED
```

Puis s'arrêter. Ne pas lancer le jeu.

## 10. Runtime humain

Après le PASS statique, demander un seul lancement humain avec le fork et
`dlc014_ip3` montés :

1. lancer une nouvelle partie avec un pays non protégé;
2. confirmer un chargement normal au 1er janvier 1776;
3. avancer au moins jusqu'au 2 janvier;
4. relever toute clé brute ou anomalie politique visible;
5. fermer normalement Victoria 3 puis le launcher;
6. confirmer explicitement leur fermeture.

La journal entry Coup n'a pas besoin d'être forcée ou déclenchée. La preuve
principale est le chargement parser et l'absence du diagnostic ciblé dans les
nouveaux logs. Ne pas utiliser la console.

Après confirmation de fermeture, analyser les nouveaux logs et rotations.
Exiger :

- `01_coup.txt` : `0` erreur
  `Unexpected token: should_be_pinned_by_default`;
- baseline globale attendue : `373` diagnostics dans `139` fichiers, sous
  réserve que le même ensemble de mods soit monté;
- les diagnostics d'API de `ip4_coup_events.txt` et `coup_events.txt` restent
  explicitement hors périmètre et ne doivent pas être revendiqués comme
  corrigés.

## 11. Verdicts finaux attendus

```text
HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_STATIC_PASS
COUP_JOURNAL_ENTRY_PINNING_ONE_FILE_ONE_OBJECT_ONE_HUNK_ALIGNED
COUP_EVENT_SCOPE_LOBBY_LAW_COOLDOWN_UNCHANGED
HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_RUNTIME_PASS
COUP_JOURNAL_ENTRY_PINNING_PARSER_ERROR_1_TO_0
HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT_COMPLETE
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
```

Finaliser le rapport et les quatre documents de navigation autorisés. Confirmer
aucun commit automatique, aucun staging et aucune autre phase commencée.
