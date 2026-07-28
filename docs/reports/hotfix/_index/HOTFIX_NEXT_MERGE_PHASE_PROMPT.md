# Phase HOTFIX-6A.5F — Alignement 1.13 du pinning de `je_yugoslavia`

FORK :
`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, LECTURE SEULE :
`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, LECTURE SEULE :
`C:\Games\Victoria 3 The Great Wave\game`

MODÈLE RECOMMANDÉ : GPT-5.6 Thinking avec raisonnement élevé.

## Verdicts d’entrée

- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

## Objectif unique

Corriger l’ancienne API de pinning de `je_yugoslavia` par un seul remplacement
de propriété compatible Victoria 3 1.13, valider statiquement, puis s’arrêter
pour confier tous les tests en jeu à l’opérateur humain.

## Préflight Git obligatoire

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
- rapport 6A.5 présent dans HEAD après commit manuel ;
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

- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- le fichier cible dans le fork, la source hotfix et le vanilla 1.13 ;
- les journaux existants de la dernière session, sans lancer le jeu.

## Périmètre gameplay fermé

Seul fichier gameplay modifiable :

```text
common/journal_entries/05_creation_of_yugoslavia.txt
```

Seul objet modifiable :

```text
je_yugoslavia
```

Seul hunk gameplay autorisé :

```diff
-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
```

Appliquer ce hunk avec `apply_patch`.

## Liste fermée des fichiers modifiables

Gameplay :

- `common/journal_entries/05_creation_of_yugoslavia.txt`

Documentation :

- `docs/reports/hotfix/_index/HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md`
- `docs/reports/hotfix/INDEX.md`
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Aucun autre fichier n’est modifiable.

## Interdictions spécifiques

Ne pas importer la condition hotfix :

```txt
is_in_geographic_region = geographic_region_balkans
```

Ne modifier aucune condition d’activation, visibilité, durée, effet,
localisation ou autre propriété. Ne pas remplacer le fichier complet.

Ne toucher ni Merchant Banking, ni Navigation Acts, ni une autre journal
entry. Ne rouvrir aucun bloc clos ou protégé : DEI/VOC, Balkan National
Awakening, NAVY, formations, MARATH, Inde/BIC/Sepoy, ADMIN, Japon, Russie,
Autriche/Croatie/Suisse, Révolutions américaine ou française, technologies,
localisations françaises, agriculture, alimentation ou industrie.

Préserver :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer `law_colonial_exploitation` pour BIC.

## Validation statique obligatoire

Vérifier :

1. une seule définition de `je_yugoslavia` ;
2. accolades équilibrées ;
3. zéro `should_be_pinned_by_default =` dans l’objet ;
4. exactement un
   `should_be_pinned_by_default_uninvolved_or_context = yes` ;
5. présence du nouveau champ dans la source hotfix et le vanilla 1.13 ;
6. aucune modification de la géographie ;
7. diff gameplay réduit au hunk exact ;
8. aucun autre fichier gameplay modifié ;
9. `git diff --check` propre ;
10. index Git vide ;
11. stash et fichiers non suivis protégés intacts ;
12. jeu et launcher toujours fermés.

Créer le rapport 6A.5F et mettre à jour uniquement les cinq documents
canoniques autorisés, puis publier le contrôle statique.

## Tests en jeu exclusivement réalisés par l’opérateur

Codex ne doit jamais lancer, piloter, cliquer dans, sauvegarder depuis ou
fermer Victoria 3 ou le launcher Paradox.

Codex ne doit pas tenter d’automatiser l’interface, utiliser la souris ou le
clavier dans le jeu, tourner en boucle pour trouver un moyen d’interagir, ni
déclarer un runtime PASS sans résultat communiqué par l’opérateur.

Après réussite de la validation statique, arrêter immédiatement avec le
verdict :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

Ne pas déclarer la phase complète et ne pas poursuivre automatiquement.
Attendre le compte rendu de l’opérateur humain.

## Fiche de test à remettre à l’opérateur humain

1. Lancer Victoria 3 avec le launcher habituel et le fork actif.
2. Confirmer visuellement que le fork est monté.
3. Démarrer une partie neuve en 1776.
4. Choisir un pays balkanique valide permettant d’observer l’entrée ; utiliser
   la Valachie seulement si les conditions affichées la rendent pertinente.
5. Ouvrir Journal > Potentiel et rechercher « Création de la Yougoslavie ».
6. Si elle est visible, vérifier :
   - aucune clé brute ;
   - conditions lisibles ;
   - aucune anomalie de pinning ;
   - aucun effet visible inattendu.
7. Laisser passer au moins un jour en jeu.
8. Fermer le jeu et le launcher.
9. Communiquer à Codex :
   - pays choisi ;
   - entrée accessible ou inaccessible ;
   - résultat des quatre contrôles ;
   - date atteinte ;
   - capture si possible.

Aucune commande console n’est requise ou autorisée pour le scénario minimal.
Si une future observation exigeait une commande, elle devrait être proposée
dans un nouveau périmètre et vérifiée avant d’être confiée à l’opérateur.

Si l’entrée est inaccessible dans ce scénario ou pour ce pays, le signaler
simplement. Ne pas demander un élargissement du correctif.

## Reprise après le compte rendu opérateur

Seulement après confirmation que le jeu et le launcher sont fermés :

1. analyser `error.log`, `game.log`, `debug.log` et leurs rotations ;
2. prouver que le fork était monté ;
3. compter les occurrences ciblant
   `common/journal_entries/05_creation_of_yugoslavia.txt` et
   `should_be_pinned_by_default` ;
4. séparer les erreurs hors périmètre ;
5. si la preuve est suffisante, finaliser le rapport et les index ;
6. sinon publier un verdict précis sans élargir le scope.

Preuve runtime minimale : fork positivement monté, progression d’au moins un
jour et disparition de l’erreur de parsing ciblée. L’inaccessibilité de
l’entrée n’annule pas cette preuve minimale si elle est clairement documentée.

## Livrables

Avant l’arrêt statique :

1. hunk gameplay unique appliqué ;
2. rapport 6A.5F créé avec état Git, comparaison trois voies, diff exact et
   résultats statiques ;
3. index documentaires cohérents ;
4. fiche de test humain condensée ;
5. verdict `RUNTIME_OPERATOR_ACTION_REQUIRED`.

Après le compte rendu humain, dans une reprise distincte :

1. analyse des observations et journaux ;
2. correction d’une éventuelle régression seulement dans le périmètre fermé ;
3. rapport et index finalisés ;
4. préparation du commit manuel, sans l’exécuter.

## Rollback

En cas de régression, inverser uniquement le hunk autorisé. Ne jamais restaurer
le fichier complet depuis la source ou le vanilla.

## Verdicts

Après validation statique, uniquement :

- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_STATIC_PASS`
- `RUNTIME_OPERATOR_ACTION_REQUIRED`

Après reprise et runtime humain concluant :

- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_RUNTIME_PASS`
- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

En cas d’échec :

- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_FAIL`

Ne rien committer automatiquement.

## Vérifications finales

Exécuter avant l’arrêt statique puis après la reprise runtime :

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

- uniquement les sept fichiers autorisés modifiés ou créés ;
- diff gameplay réduit au hunk exact ;
- aucun fichier staged ;
- aucun commit automatique ;
- `bject` et les sept recherches technologiques intacts ;
- stash NAVY-3C-3 intact ;
- tous les blocs clos et protégés intacts ;
- Victoria 3 et le launcher fermés au moment où Codex intervient.
