# Mise à jour locale du Steam Build — 10 octobre 2026

Les deux copies allégées ont été reconstruites depuis le dossier de développement courant, sur la base de `c891b1d9bb2a21bc42409acbdccc268518110260`, avec la nouvelle icône chimique non encore commitée.

- Paquet utilisé par le lanceur : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/workshop_build/Age_of_Revolution_Fork`.
- Autre copie locale synchronisée : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/Age of revolution Fork [Steam Build]`.
- Anciennes copies et anciens inventaires conservés dans `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/workshop_build/backups/steam-refresh-20261010-141250-3b81d6c7`.
- 1 915 fichiers par paquet ; 293 003 279 octets pour le paquet principal, soit environ 293 Mo.
- Par rapport à l'ancien inventaire principal : 144 fichiers ajoutés, 102 modifiés, aucun fichier retiré.

## Vérifications

- Manifest de livraison existant appliqué ; dossiers Git, documentation, outils, recherches et sources d'images exclus.
- Tous les fichiers livrés vérifiés par SHA-256 contre les sources et après installation ; zéro écart. Seul le nom d'affichage de la copie locale secondaire est conservé ; ses autres métadonnées sont identiques au paquet principal.
- Nouvelle icône `1776_chemical_plant.dds` identique dans les sources et les deux copies installées.
- Métadonnées, miniature, chemins de remplacement et absence de fichiers de développement, secrets potentiels ou chemins locaux dans le contenu livrable : PASS.
- `tools/validate_diplomacy_ottoman_1776.py` : PASS.
- `tools/validate_ai_regional_infrastructure_1776.py` : PASS.
- Contrôles statiques uniquement ; aucun lancement ni test économique en jeu effectué pour cette mise à jour.

Le candidat cartographique du worktree `map-0-collaborator-integration` n'a pas été intégré. Aucun autre changement de gameplay n'a été réalisé pour préparer ce paquet. Les constats de l'audit MAP-0 restent à traiter dans la phase cartographique suivante ; cette préparation n'est pas une certification complète de la carte.

Aucune publication Steam, aucun commit, push ou merge. L'article Workshop existant reste `3780935876` ; sa publication devra être mise à jour manuellement, et non créée à nouveau.

Le script `tools/workshop/refresh_local_steam_build.ps1` permet désormais d'installer un paquet préalablement validé, avec sauvegarde récupérable des deux anciennes copies et contrôle des fichiers avant et après installation.

## Numérotation de publication

Après approbation explicite, la version est passée de **2.4.0 à 2.5.0** dans le dossier de travail et les deux Steam Build. Aucun identifiant Workshop, nom d'affichage local ou réglage de compatibilité n'a été changé. Les anciennes métadonnées sont sauvegardées sous `workshop_build/backups/version-2.5.0-20261010-154821` et `version-2.5.0-20261010-154958` ; l'inventaire de publication a été actualisé. Le dev blog anglais est conservé dans `docs/workshop/STEAM_DEV_BLOG_2.5.0_EN.md`, avec une version BBCode dédiée à Steam.
