# 1776 — politique des points de restauration GitHub

Branche distante réservée : `backup/1776-checkpoints`.

Ce premier point conserve l'état courant après MAP-2D, incluant les travaux antérieurs MAP-2A/B/C et toutes les autres modifications locales retenues dans le manifeste. Il ne prétend pas être un test de chargement en jeu. MAP-2D attend encore la validation du joueur.

## Règles

- Préparer les sauvegardes dans un dépôt temporaire indépendant ou un worktree séparé. Ne pas changer de branche, ajouter à l'index, committer ou nettoyer le workspace principal.
- Conserver les états importants avec des commits successifs sur cette branche de sauvegarde. Partir du dernier point distant lors des envois suivants ; ne jamais réécrire l'historique.
- Aucun push sur `main`, aucun merge, force-push ou suppression de branche distante.
- Inclure fichiers de gameplay, scripts, bitmap, sources nécessaires, fichiers nouveaux et modifications/suppressions pertinentes. Vérifier les contenus par empreintes SHA-256.
- Exclure caches, logs, sauvegardes de parties, configurations personnelles, secrets et ZIP complets redondants. Les trois petites archives originales des portraits sont des sources uniques conservées, pas des snapshots complets du mod.
- Vérifier les limites GitHub avant chaque envoi. Pas de configuration Git LFS ni de stockage payant sans accord explicite.
- Après chaque push, vérifier la référence distante, l'accessibilité du commit et une restauration réelle depuis GitHub dans un dossier indépendant. Conserver un manifeste des fichiers et exclusions par catégorie.
- Ne supprimer un snapshot local redondant qu'après validation en jeu du lot et preuve que ses données nécessaires sont couvertes par un point distant vérifié. Conserver les anciens états distincts non couverts.
- Retirer ensuite les worktrees/branches temporaires utilisés uniquement pour cette préparation, sans toucher au dépôt principal ni à la branche distante.

## Restaurer sans toucher au développement

Cloner la branche `backup/1776-checkpoints` dans un **nouveau dossier vide**, avec `core.autocrlf=false` pour préserver les octets. Pour un ancien point, utiliser son identifiant de commit dans cette copie indépendante. Ne jamais restaurer en écrasant le workspace de développement.

Le manifeste `docs/backups/CURRENT_CHECKPOINT_MANIFEST.json` contient les chemins relatifs, tailles et SHA-256 de tous les fichiers retenus. Comparer chaque fichier restauré à cette liste. Les exclusions sont intentionnelles : le checkpoint restaure l'état du mod, pas les caches ou les parties locales.

Les données historiques de baseline conservées permettent de préparer ultérieurement des points séparés MAP-2A/B/C lorsque leur reconstruction exacte est démontrable. Ne pas inventer de commits historiques à partir d'une baseline seulement partielle.

## MAP-2L Rhine-Westphalia and Swabia user-validated checkpoint

CURRENT_CHECKPOINT_MANIFEST.json now contains the current full source manifest and matches _checkpoint/MAP2L_RHINE_SWABIA_MANIFEST.json. The backup metadata files do not hash themselves. Gameplay is identical to the independently restored 0a66418 snapshot. Only metadata and the checkpoint-helper safety checks changed afterward. The later Swabia continuation is deliberately not included. Restore sources using this manifest; never overwrite the development workspace.
