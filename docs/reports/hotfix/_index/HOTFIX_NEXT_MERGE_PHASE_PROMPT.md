# Phase HOTFIX-6A.6F — Alignement Victoria 3 1.13 du pinning de `je_risorgimento`

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, STRICTEMENT EN LECTURE SEULE :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA VICTORIA 3 1.13, STRICTEMENT EN LECTURE SEULE :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d'entrée requis

- `HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT`

Rapport canonique d'entrée :

`docs/reports/hotfix/_index/HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

La phase 6A.6 doit avoir été commitée manuellement avant de commencer.

## Règle absolue concernant Victoria 3

Les règles suivantes sont littérales :

- Codex ne lance jamais Victoria 3.
- Codex ne lance jamais le launcher Paradox.
- Codex ne clique jamais dans le jeu.
- Codex ne tente jamais d'automatiser ou de piloter l'interface.
- Codex n'ouvre jamais une sauvegarde.
- Codex n'utilise jamais la console du jeu.
- Codex ne tourne jamais en boucle pour essayer d'interagir.
- Codex ne déclare jamais avoir réalisé une observation visuelle.
- Codex ne déclare jamais le runtime PASS sans observations humaines.
- Codex prépare tous les contrôles avant le lancement humain.
- Codex fournit une fiche condensée permettant un seul lancement.
- Codex attend le compte rendu de l'opérateur.
- Codex analyse les logs seulement après fermeture confirmée du jeu et du
  launcher.

Après le PASS statique, Codex s'arrête obligatoirement avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

L'opérateur humain réalise l'unique lancement, ferme ensuite Victoria 3 et le
launcher, puis transmet son compte rendu. Codex ne peut analyser les nouveaux
logs qu'après cette confirmation de fermeture.

## Objectif unique

Dans l'objet exact `je_risorgimento` du fichier exact
`common/journal_entries/00_italian_unification.txt`, remplacer uniquement :

```txt
should_be_pinned_by_default = yes
```

par :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

Le changement doit rester limité à :

- 1 fichier gameplay ;
- 1 objet ;
- 1 hunk ;
- 1 ligne supprimée ;
- 1 ligne ajoutée.

Ne commencer aucun autre correctif. Ne traiter aucune autre journal entry.

## Préflight Git obligatoire

Exécuter avant toute modification :

```powershell
Set-Location "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork"

git rev-parse --show-toplevel
git branch --show-current
git status --short
git log -5 --oneline --decorate
git diff --check
git diff --cached --name-only
git stash list
```

Exiger :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.6 présent dans le HEAD ;
- phase 6A.6 déjà commitée manuellement ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls les éléments suivants non suivis :
  - `bject` ;
  - les sept fichiers de `docs/research/technology/` ;
- stash exact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- Victoria 3 fermé ;
- launcher Paradox fermé.

Avant toute modification, enregistrer les hashes SHA-256 de `bject` et des sept
fichiers technologiques afin de les comparer à la fin.

En cas d'écart, arrêter immédiatement avec le verdict précis :

- `BLOCKED_WRONG_BRANCH`
- `BLOCKED_6A6_NOT_COMMITTED`
- `BLOCKED_DIRTY_TREE`
- `BLOCKED_STAGED_FILES`
- `BLOCKED_UNEXPECTED_UNTRACKED_FILES`
- `BLOCKED_PROTECTED_STASH_MISSING`
- `BLOCKED_GAME_PROCESS_RUNNING`

Interdictions :

- aucun `git reset` ;
- aucun `git restore` ;
- aucun `git checkout` de fichier ;
- aucun `git clean` ;
- aucun merge ;
- aucun rebase ;
- aucun amend ;
- aucun commit automatique ;
- aucun `stash apply`, `pop` ou `drop` ;
- aucune inspection du contenu du stash.

## Sources obligatoires

Lire intégralement :

- `HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les changelogs pertinents du fork et de la source hotfix.

Lire en trois voies :

1. fork :
   `common/journal_entries/00_italian_unification.txt` ;
2. source hotfix, lecture seule :
   `common/journal_entries/00_italian_unification.txt` ;
3. vanilla 1.13, lecture seule :
   `common/journal_entries/00_italian_unification.txt`.

Consulter en lecture seule les logs et rotations existants :

- `error.log`, `error.1.log`, etc. ;
- `game.log` et rotations ;
- `debug.log` et rotations ;
- `dedicated_server.log` et rotations.

Ne lancer ni le jeu ni le launcher pour produire des logs.

## Preuve trois voies attendue

Avant modification, confirmer :

| Arbre | Pinning dans `je_risorgimento` |
| --- | --- |
| Fork | `should_be_pinned_by_default = yes` |
| Source hotfix | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| Vanilla 1.13 | `should_be_pinned_by_default_uninvolved_or_context = yes` |

Confirmer aussi dans les logs de référence une erreur directe :

```text
Unexpected token: should_be_pinned_by_default,
```

visant `common/journal_entries/00_italian_unification.txt`, une occurrence dans
la session 6A.5F.

Si source hotfix et vanilla ne convergent plus sur la propriété et la valeur,
arrêter avec :

`BLOCKED_THREE_WAY_EVIDENCE_CHANGED`

## Liste fermée des fichiers modifiables

Gameplay :

- `common/journal_entries/00_italian_unification.txt`.

Documentation :

- `docs/reports/hotfix/_index/HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md` ;
- `docs/reports/hotfix/INDEX.md` ;
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun autre fichier n'est autorisé.

## Objet et hunk exacts

Objet autorisé :

```txt
je_risorgimento = {
```

Hunk autorisé :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Le remplacement complet du fichier est interdit. Aucun reformatage, déplacement
de ligne, correction adjacente ou nettoyage d'espaces n'est autorisé.

## Divergence 1776 à préserver

La ligne suivante du bloc `possible` est intentionnelle et doit rester
strictement identique :

```txt
year >= 1836
```

La source hotfix et vanilla l'omettent. Cette différence ne doit pas être
importée. Elle explique que l'entrée puisse rester seulement potentielle en
1776.

## Géographie à préserver

Ne pas importer depuis la source hotfix :

```txt
is_in_geographic_region = geographic_region_italy_old
```

Cette ligne apparaît dans la source hotfix sous `is_shown_in_lobby` et
`is_shown_when_inactive`, mais pas dans vanilla 1.13. Les deux blocs de
visibilité du fork doivent rester byte-for-byte identiques.

## Protections absolues

Ne sélectionner et ne modifier aucun élément relatif à :

- DEI/VOC, Java et économie post-compagnie ;
- Balkan National Awakening ;
- `05_creation_of_yugoslavia.txt` ;
- NAVY, lois navales, formations militaires et événements navals ;
- MARATH, SAT, KHP, Travancore ;
- Inde, BIC, Sepoy et Bombay ;
- ADMIN ;
- Japon ;
- Russie ;
- Autriche, Croatie, Slavonie et Suisse ;
- Révolution américaine ;
- Révolution française et lettres de Kew ;
- technologies et `docs/research/technology/` ;
- localisations françaises générales ;
- agriculture, alimentation et industrie générale ;
- descripteurs, launcher et sauvegardes ;
- `bject`.

Préserver impérativement pour BIC :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer :

```txt
law_colonial_exploitation
```

Ne pas modifier Merchant Banking, Navigation Acts, `00_greek_nationalism.txt`,
`01_coup.txt`, `04_imperialism_of_promise.txt`,
`05_great_eastern_crisis.txt`, les tutoriels, objectifs joueur, prestige goods,
Russie ou `sick_man`.

## Application

1. Enregistrer les hashes du fichier fork, source hotfix et vanilla.
2. Compter dans `je_risorgimento` :
   - exactement une ancienne propriété dans le fork ;
   - exactement une nouvelle propriété dans la source hotfix ;
   - exactement une nouvelle propriété dans vanilla.
3. Appliquer uniquement le hunk autorisé avec `apply_patch`.
4. Ne toucher à aucune autre ligne.
5. Créer le rapport de phase et actualiser uniquement les index autorisés.

## Validations statiques

Après modification, vérifier :

1. `should_be_pinned_by_default = yes` : 0 occurrence dans
   `je_risorgimento` ;
2. `should_be_pinned_by_default_uninvolved_or_context = yes` : exactement
   1 occurrence dans `je_risorgimento` ;
3. `year >= 1836` : exactement 1 occurrence et ligne inchangée ;
4. `is_in_geographic_region = geographic_region_italy_old` : 0 occurrence
   dans le fichier fork ;
5. le diff gameplay contient exactement le remplacement autorisé ;
6. 1 fichier gameplay, 1 objet, 1 hunk ;
7. accolades équilibrées ;
8. aucun changement de localisation ;
9. aucun autre fichier gameplay modifié ;
10. source hotfix et vanilla inchangés ;
11. `git diff --check` propre ;
12. index Git vide ;
13. stash NAVY-3C-3 intact ;
14. hashes de `bject` et des sept recherches technologiques inchangés ;
15. Victoria 3 et le launcher toujours fermés.

Si tous ces contrôles passent, publier :

`HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_STATIC_PASS`

Puis préparer la fiche ci-dessous et s'arrêter avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

Ne pas poursuivre vers un runtime automatique.

## Fiche condensée pour l'opérateur humain

Un seul lancement doit couvrir tout le test.

### Avant le lancement

- Confirmer que Codex a publié le PASS statique.
- Monter le fork et ses dépendances habituelles.
- Préparer une partie neuve au 1er janvier 1776.

### Dans le jeu

1. Choisir un pays de culture principale nord-italienne ou sud-italienne,
   par exemple Naples si ce pays est disponible dans le scénario.
2. Ouvrir `Journal > Potentiel`.
3. Rechercher l'entrée Risorgimento ou l'entrée d'unification italienne.
4. Confirmer :
   - texte et conditions lisibles ;
   - aucune clé brute ;
   - aucune anomalie visible de pinning ;
   - la condition de date 1836 peut rester non remplie en 1776 sans constituer
     un échec.
5. Avancer d'au moins un jour.
6. Noter la date finale.
7. Prendre une capture de l'entrée ou du panneau pertinent si possible.
8. Fermer Victoria 3.
9. Fermer le launcher Paradox.

### Compte rendu à transmettre

- pays joué ;
- date initiale et date finale ;
- entrée visible ou non dans `Potentiel` ;
- conditions lisibles ou non ;
- présence d'une clé brute ;
- anomalie de pinning ;
- capture éventuelle ;
- confirmation explicite que le jeu et le launcher sont fermés.

Si le pays choisi ne satisfait pas les cultures d'affichage, le signaler :
ne pas transformer cette absence en échec parser.

## Analyse après retour humain

Seulement après confirmation de fermeture :

1. identifier les logs et rotations produits par l'unique lancement ;
2. confirmer positivement que le fork et ses dépendances attendues ont été
   montés ;
3. comparer le diagnostic ciblé :
   - avant : 1 erreur visant `00_italian_unification.txt` et l'ancienne
     propriété ;
   - après : 0 ;
4. confirmer qu'aucune erreur ne vise la nouvelle propriété 1.13 ;
5. distinguer les autres erreurs globales préexistantes du verdict ciblé ;
6. intégrer fidèlement les observations humaines au rapport ;
7. ne jamais inventer une observation visuelle.

## Rollback exact

En cas d'échec imputable au hunk, et seulement dans le fichier autorisé :

```diff
-	should_be_pinned_by_default_uninvolved_or_context = yes
+	should_be_pinned_by_default = yes
```

Ne pas utiliser `git restore`, `git checkout`, `git reset` ou un remplacement
de fichier complet. Rejouer ensuite les contrôles statiques. Tout rollback
runtime éventuel exige un nouveau test humain ; Codex ne lance jamais le jeu.

## Livrables

Créer :

`docs/reports/hotfix/_index/HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md`

Le rapport doit contenir :

1. date, branche, HEAD initial et final ;
2. état Git initial ;
3. sources consultées ;
4. preuve trois voies ;
5. erreur runtime de référence ;
6. fichier, objet et hunk exacts ;
7. divergence `year >= 1836` préservée ;
8. géographie préservée ;
9. diff gameplay exact ;
10. validations statiques ;
11. fiche remise à l'opérateur ;
12. compte rendu humain ;
13. analyse ciblée des logs après fermeture ;
14. erreurs avant/après ;
15. protections ;
16. fichiers modifiés ;
17. état Git final ;
18. décision de commit manuel ;
19. verdicts.

Actualiser uniquement les cinq index documentaires autorisés.

## Verdicts

Après PASS statique, avant runtime :

- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_STATIC_PASS`
- `RUNTIME_OPERATOR_ACTION_REQUIRED`

Après observations humaines et logs ciblés conformes :

- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_RUNTIME_PASS`
- `ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNED`
- `ITALIAN_1776_YEAR_GATE_PRESERVED`
- `GEOGRAPHY_UNCHANGED`
- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

En cas d'échec :

- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_FAIL`

Ne jamais émettre le PASS runtime sur la seule base des contrôles statiques.

## Vérifications finales

Après clôture humaine, exécuter :

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

- exactement un fichier gameplay modifié ;
- exactement les six documents autorisés modifiés ou créés au maximum ;
- aucun autre fichier modifié ;
- aucun fichier staged ;
- aucun commit automatique ;
- `bject` intact ;
- les sept fichiers de `docs/research/technology/` intacts ;
- stash NAVY-3C-3 intact ;
- DEI/VOC intact ;
- Balkan National Awakening intact ;
- Yugoslavia 6A.5F intacte ;
- formations militaires intactes ;
- NAVY intact ;
- MARATH intact ;
- BIC intact ;
- source hotfix et vanilla intacts ;
- Victoria 3 fermé ;
- launcher Paradox fermé ;
- aucun lancement ou contrôle du jeu effectué par Codex.

Ne commence aucune autre phase et ne committe rien automatiquement.
