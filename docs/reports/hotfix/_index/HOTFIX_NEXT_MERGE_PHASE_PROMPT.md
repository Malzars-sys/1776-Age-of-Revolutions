# Phase HOTFIX-6A.5 — Sélection du prochain résidu global

FORK : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, LECTURE SEULE : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, LECTURE SEULE : `C:\Games\Victoria 3 The Great Wave\game`

MODÈLE RECOMMANDÉ : GPT-5.6 Thinking avec raisonnement élevé.

## Verdicts d’entrée

- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_COMPLETE`
- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_RUNTIME_PASS`
- `HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`
- `MILITARY_FORMATIONS_1_13_RUNTIME_QA_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Rapport canonique d’entrée :

`docs/reports/hotfix/_index/HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md`

## Objectif unique

Sélectionner exactement **un** prochain sous-bloc atomique parmi les résidus
globaux encore ouverts. Cette phase est une phase d’audit et de sélection :
elle ne doit modifier aucun gameplay.

Publier :

1. une mesure actualisée des résidus et des erreurs runtime ;
2. un classement motivé des candidats réellement exploitables ;
3. les trois meilleurs candidats, avec taille, priorité, confiance, risque de
   collision et besoin de runtime ;
4. un seul sous-bloc sélectionné ;
5. son périmètre fermé, ses sources, ses fichiers et objets exacts ;
6. un prompt d’exécution ultérieur.

Ne commencer ni Merchant Banking, ni Navigation Acts, ni une autre correction
pendant cette phase de sélection.

## État Git requis

Exécuter avant toute modification :

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
- rapport 6A.4F présent dans le HEAD après commit manuel ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` peuvent
  être non suivis ;
- stash exact
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- Victoria 3 et le launcher fermés.

Arrêter avec un verdict bloquant précis si une condition manque. Ne faire
aucun reset, restore, checkout de fichier, clean, merge, commit automatique,
stash apply/pop/drop ou inspection du contenu du stash.

## Sources obligatoires

Lire intégralement :

- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les changelogs pertinents du fork et de la source hotfix.

Consulter les derniers `error.log`, `game.log`, `debug.log` et leurs rotations
de la session 6A.4F. Enregistrer séparément :

- les erreurs déjà fermées par 6A.4F ;
- les erreurs provenant d’autres fichiers ;
- les familles les plus répétées ;
- les diagnostics qui appartiennent à des blocs protégés ou à des backlogs.

Comparer chaque candidat retenu en trois voies : fork, source hotfix et vanilla
Victoria 3 1.13. Le nom identique d’un fichier ou une différence de hash ne
suffisent jamais à autoriser un import.

## Base de sélection

La revue 6A.4 a classé les 161 anciennes lignes `PENDING_REVIEW` :

- 7 `REQUIRED_HOTFIX_DELTA` ;
- 22 `VANILLA_1_13_ALIGNMENT_REQUIRED`, dont le fichier balkanique désormais
  clos ;
- 12 `ALREADY_MERGED` ;
- 3 `INTENTIONAL_FORK_DIVERGENCE` ;
- 1 `OBSOLETE_HOTFIX_CONTENT` ;
- 10 `POST_MERGE_DESIGN_BACKLOG` ;
- 19 `PROTECTED_CONCURRENT_WORK` ;
- 87 `UNKNOWN_REQUIRES_REVIEW`.

Actualiser ces nombres sans réintroduire le fichier balkanique dans les
résidus. L’ancien total annoncé de 26 deltas à haute confiance reste
`UNVERIFIED` tant qu’aucun registre exact ne le démontre.

Les pistes connues comprennent :

- les autres migrations de pinning de journal entries vers l’API 1.13 ;
- Merchant Banking pour GEN/VEN ;
- Navigation Acts pour GBR et ses colonies ;
- les 87 unités encore `UNKNOWN_REQUIRES_REVIEW`.

Ces pistes sont des candidats à comparer, pas des corrections autorisées dans
la présente phase.

## Méthode obligatoire

1. Recalculer l’inventaire résiduel à partir des registres canoniques.
2. Rapprocher les erreurs runtime actuelles des chemins inventoriés.
3. Exclure les blocs clos, les divergences intentionnelles, les backlogs et les
   travaux protégés.
4. Inspecter en trois voies les meilleurs candidats restants.
5. Classer chaque candidat dans une catégorie exclusive.
6. Évaluer pour chacun :
   - importance ;
   - preuve fonctionnelle ;
   - taille du diff ;
   - nombre de fichiers et d’objets ;
   - dépendances ;
   - risque de collision ;
   - besoin de runtime ;
   - rollback possible.
7. Publier les trois meilleurs candidats.
8. Choisir exactement un sous-bloc atomique.
9. Définir une liste fermée de fichiers et d’objets pour sa future exécution.
10. Ne modifier aucun fichier gameplay.

Préférer un correctif petit, prouvé, réversible et sans collision. Une erreur
runtime répétée ne doit être sélectionnée que si sa cause et son correctif sont
prouvés par la comparaison trois voies.

## Protections absolues

Ne modifier aucun fichier ou objet relatif à :

- DEI/VOC, dissolution, drapeau Java ou économie post-compagnie ;
- `05_balkan_national_awakening.txt`, désormais clos ;
- NAVY, lois navales, formations militaires ou événements technologiques
  navals ;
- MARATH, SAT, KHP ou Travancore ;
- Inde, BIC, Sepoy, Bombay ou noms dynamiques des présidences ;
- ADMIN ;
- Japon ;
- Russie ;
- Autriche, Croatie, Slavonie ou Suisse ;
- Révolution américaine ou française et lettres de Kew ;
- technologies et `docs/research/technology/` ;
- localisations françaises générales ;
- agriculture, alimentation ou industrie générale ;
- descripteurs, launcher, sauvegardes et `bject`.

Préserver notamment :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer `law_colonial_exploitation` pour BIC.

## Liste fermée des fichiers modifiables

Documentation uniquement :

- `docs/reports/hotfix/_index/HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`
- `docs/reports/hotfix/INDEX.md`
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Aucun fichier gameplay n’est modifiable.

## Rapport requis

Créer :

`docs/reports/hotfix/_index/HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

Le rapport doit contenir :

- état Git initial et HEAD ;
- sources consultées ;
- inventaire actualisé ;
- mesure et regroupement des erreurs runtime ;
- exclusions et protections ;
- classement des candidats ;
- tableau des trois meilleurs candidats ;
- choix unique et justification ;
- périmètre futur fermé ;
- validations statiques documentaires ;
- fichiers modifiés ;
- état Git final ;
- décision de commit manuel ultérieur.

Le prompt suivant doit être un prompt d’exécution de la phase sélectionnée. Ne
pas exécuter cette phase dans la même session.

## Contrôles

Vérifier :

1. zéro fichier gameplay modifié ;
2. un seul prochain sous-bloc sélectionné ;
3. aucun résidu clos réintroduit ;
4. chaque candidat classé une seule fois ;
5. les chiffres du rapport cohérents avec les CSV ;
6. les protections explicites ;
7. le prompt futur limité à un périmètre fermé ;
8. `git diff --check` propre ;
9. index Git vide ;
10. modifications limitées aux six documents autorisés.

## Verdicts

Après sélection valide :

- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Publier également :

`NEXT_EXECUTION_PHASE = <phase atomique sélectionnée>`

En cas d’échec :

- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION_FAIL`

Ne rien committer automatiquement.

## Vérifications finales

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

- uniquement les six documents autorisés modifiés ;
- aucun fichier staged ;
- aucun commit automatique ;
- `bject` intact ;
- les sept fichiers de `docs/research/technology/` intacts ;
- stash NAVY-3C-3 intact ;
- DEI/VOC, Balkans 6A.4F, formations militaires, NAVY et MARATH inchangés ;
- Victoria 3 et le launcher fermés.
