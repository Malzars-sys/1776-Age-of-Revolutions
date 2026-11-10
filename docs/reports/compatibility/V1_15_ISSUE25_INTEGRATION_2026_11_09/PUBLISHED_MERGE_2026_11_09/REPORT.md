# Fusion d'historique publiée — mission 25, 9 novembre 2026

La fusion autorisée par le mainteneur (« Oui, j'autorise. ») est publiée dans **main** au commit [`8722a8a32eb08d63b8c55a6edf530b50ed817b68`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/commit/8722a8a32eb08d63b8c55a6edf530b50ed817b68). La [PR 34](https://github.com/Malzars-sys/1776-Age-of-Revolutions/pull/34) est maintenant fermée et marquée **merged**, avec ce même commit de fusion.

| Contrôle | Résultat |
| --- | --- |
| Premier parent | `0396b1133168c1721b61cee5ae5334f1a4f5e4e1` — ancien main |
| Second parent | `b72dc3584e1225f8c675b7c6c9f295cde122b821` — hotfix/1.15 |
| Arbre publié | `ae449f27b1055c18b9581ee9a4deeb42be4030a2` — identique à l'ancien main |
| Diff contre l'ancien main | **0 fichier modifié** |
| Ascendance | Le head hotfix est désormais un ancêtre de main ; les branches ne divergent plus. |
| Publication | Mise à jour non forcée de main avec contrôle de sa tête attendue |
| Validation de publication | **11/11 contrôles** |

La création du commit et la mise à jour de référence ont utilisé GitHub directement. Les têtes distantes et l'arbre ont été relus avant l'opération ; les deux parents et l'arbre exact du nouveau commit ont été contrôlés avant de déplacer main. Les comparaisons distantes ont ensuite confirmé le diff vide, l'ascendance et le statut fusionné de la PR.

Le checkout local, son HEAD et son index sont préservés. Aucun fichier du jeu, aucune carte, loi ou donnée économique, aucun vanilla n'a été écrit. Les modifications locales non engagées — dont les deux déclarations de version du lanceur — ne sont pas publiées par cette fusion. La branche hotfix n'est ni supprimée ni déplacée.

Le passage par une copie locale isolée n'a pas été nécessaire : l'objet de commit a été construit côté GitHub avec l'arbre déjà approuvé, sans staging ni checkout. Cette méthode conserve le périmètre exact de la proposition autorisée et évite toute interaction avec les travaux locaux concurrents.

**La divergence d'historique est résolue.** La mission 25 reste **In progress** pour la sélection des correctifs locaux à livrer, les diagnostics restants, la mission 39 et les validations moteur manquantes. Aucune nouvelle validation humaine du jeu ni publication de release n'est affirmée. Les anciens rapports de préparation restent conservés ; le présent reçu leur ajoute le résultat de publication.

Preuves : `REMOTE_EVIDENCE.json`, `VALIDATION.json` et `DELIVERY_RECEIPT.json` dans ce dossier.
