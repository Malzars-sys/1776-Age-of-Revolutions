# Phase HOTFIX-6A.3R — Résolution ciblée DEI Cape/Ceylon et vanilla 1.13

FORK : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, LECTURE SEULE : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, LECTURE SEULE : `C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d’entrée

- `HOTFIX_6A3_DEI_TARGETED_AUDIT_COMPLETE`
- `NO_REQUIRED_HOTFIX_DELTA_IDENTIFIED`
- `DEI_CAPE_CEYLON_OUTCOME_UNVERIFIED`
- `DEI_VANILLA_1_13_ALIGNMENT_REQUIRES_RESOLUTION`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

## Objectif unique

Résoudre statiquement deux décisions fermées sans modifier le gameplay : déterminer le mécanisme exact et les bénéficiaires valides permettant à DEI de perdre Cape Colony et Ceylon lors de `dei_breakup.1`, puis admettre ou rejeter chacun des sept hunks DEI identiques hotfix/vanilla 1.13. Ne publier une phase de correction que si chaque hunk retenu, ses dépendances et son rollback sont exacts.

## État Git requis

Exiger branche `hotfix-dlc-audit`, zéro staged, stash MARATH intact, `docs/research/technology/` intact et aucun processus Victoria/launcher. Le paquet 6A.2 et ses documents sont protégés. Le fichier non suivi `bject` et les recherches technologiques ont été déclarés travaux ultérieurs normaux par l’opérateur : les ignorer et ne pas les suivre.

Ne faire aucun reset, restore, checkout de fichier, clean, stash apply/pop/drop ou commit automatique. Ne pas inspecter le contenu du stash.

## Sources obligatoires

Lire `HOTFIX_6A3_DEI_TARGETED_AUDIT.md` et sa delta map, puis les rapports C1AI, roadmap, upstream DLC, Inde/BIC closure et NAVY-2B-bis. Utiliser les lignes et hashes 6A.3 comme périmètre initial. Ne pas rouvrir une revue globale.

## Décision A — Cape Colony et Ceylon

Tracer exactement, dans le setup 1776 courant :

- owners et provinces des blocs `STATE_CEYLON`, `STATE_EASTERN_CAPE`, `STATE_CAPE_COLONY` ;
- pays voisins admissibles, cultures primaires, relations de sujet et existence des tags ;
- effet réel de la boucle lignes fork 42–102 ;
- effet de `change_tag`, `make_independent` et `independence.2` ;
- bâtiments, pops, claims, traités et journal entries qui deviendraient orphelins après transfert.

Produire un hunk minimal par territoire avec bénéficiaire explicite, ou conclure `UNVERIFIED_NO_SAFE_HUNK`. Ne pas inventer un tag, ne pas importer de fichier complet et ne pas déplacer de province sans preuve.

## Décision B — alignement vanilla 1.13

Statuer séparément sur les sept groupes de la delta map :

- Ulema sunnite pour JAV ;
- nettoyage générique des cultures/personnages pour JAV ;
- délai `independence.2` pour JAV ;
- Ulema sunnite pour IDN ;
- nettoyage générique, religion sunnite et personnages pour IDN ;
- délai `independence.2` pour IDN ;
- délai de l’option de refus.

Pour chaque groupe, vérifier les APIs 1.13, l’effet fonctionnel, les dépendances de localisation et l’absence de collision 1776. Classer `ADMIT_VANILLA_1_13_ALIGNMENT`, `INTENTIONAL_1776_DIVERGENCE` ou `UNVERIFIED`.

## Protections absolues

Ne modifier aucun gameplay. Ne pas toucher NAVY, ADMIN, BIC, Travancore, Inde close, MARATH, Japon, Mamluk Iraq, Russie, localisations françaises, descripteurs, launcher, sauvegardes ou recherches technologiques. Préserver les six fichiers gameplay 6A.2 et `activate_law = law_type:law_frontier_colonization`. Ne jamais restaurer `law_colonial_exploitation` pour BIC.

Le bloc `alk_breakup.1` du même fichier est hors périmètre. La `Koloniale_Marine` trois frégates est `NAVY_PROTECTED`.

## Livrables

Créer `docs/reports/hotfix/_index/HOTFIX_6A3R_DEI_BREAKUP_HUNK_RESOLUTION.md`, mettre à jour la delta map 6A.3 et seulement les index/roadmap canoniques nécessaires. Aucun runtime et aucun gameplay.

## Verdicts attendus

- `HOTFIX_6A3R_DEI_BREAKUP_HUNK_RESOLUTION_COMPLETE` si les deux décisions sont fermées ;
- `READY_FOR_DEI_TARGETED_FIX` seulement si tous les hunks retenus sont exacts ;
- sinon `BLOCKED_DEI_TARGET_HUNKS_UNVERIFIED` avec blockers précis ;
- toujours `NO_GAMEPLAY_CHANGED` pendant 6A.3R.

## Vérifications finales

Exécuter `git diff --check`, `git status --short`, diff name/status/stat, staged vide, `git stash list` et contrôle des processus. Confirmer zéro gameplay supplémentaire, protections 6A.2 intactes, `bject` et recherches technologiques intacts. Ne pas committer automatiquement.
