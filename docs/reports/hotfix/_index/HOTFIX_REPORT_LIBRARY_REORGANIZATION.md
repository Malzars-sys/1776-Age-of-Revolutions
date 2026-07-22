# HOTFIX — Réorganisation de la bibliothèque des rapports

## 1. Résumé

Les 122 fichiers historiques ont été classés et déplacés sans perte ni changement de contenu. Verdict : `HOTFIX_5_INDIA_COMPLETE_AND_REPORT_LIBRARY_INDEXED`.

## 2. État Git initial

Branche `hotfix-dlc-audit`, HEAD initial `6d6db23`, aucun fichier suivi modifié et seule exception non suivie `docs/research/technology/`.

## 3. Inventaire initial

122 fichiers suivis : 83 Markdown, 39 CSV, aucun autre format.

## 4. Problème de navigation constaté

Tous les rapports se trouvaient à la racine, sans navigation régionale ni statut canonique central.

## 5. Règles de classification

Chaque document a été classé par région, sujet, type autorisé et statut historique après lecture de son résumé, verdict et conclusion.

## 6. Structure cible

La racine contient uniquement `README.md`, `INDEX.md` et les dossiers `_index`, `india`, `japan`, `mamluk_iraq`, `shared`.

## 7. Nombre de rapports par région

Inde : 100 fichiers ; Japon : 13 ; Mamluk/Iraq : 7 ; partagé : 2.

## 8. Nombre de rapports par type

Correction : 52 ; forensic : 2 ; manifeste : 19 ; référence : 5 ; résultats : 15 ; runtime : 18 ; audit/setup statique : 11.

## 9. Nombre de paires Markdown/CSV

39 paires, soit 78 fichiers, sont conservées dans un même dossier.

## 10. Rapports sans compagnon

44 rapports Markdown n’avaient pas de CSV compagnon ; ils restent autonomes.

## 11. Classifications ambiguës

Zéro classification ambiguë ; aucun dossier `other` n’est nécessaire.

## 12. Plan de déplacement

Le plan temporaire couvrait 122 sources et 122 destinations uniques sous `docs/reports/hotfix/`.

## 13. Collisions vérifiées

Zéro collision, destination préexistante, sortie du périmètre ou séparation de paire.

## 14. Déplacements exécutés

Les 122 fichiers suivis ont été déplacés avec `git mv`.

## 15. Préservation des noms

Chaque nom de fichier historique est strictement conservé.

## 16. Préservation des hashes

Les 122 SHA-256 avant/après sont identiques.

## 17. Réparations de liens

Aucune réparation n’était nécessaire : les anciens rapports ne contenaient aucun lien Markdown interne vers leur ancien emplacement.

## 18. Audit des liens

Les liens relatifs de la nouvelle navigation ont été résolus automatiquement ; les références historiques en texte brut sont conservées.

## 19. Index global

`INDEX.md` donne les accès par région, sujet, validations finales et statuts historiques.

## 20. Index CSV

`HOTFIX_REPORT_INDEX.csv` recense chaque rapport Markdown avec métadonnées et chaîne canonique.

## 21. Carte des dépendances

`HOTFIX_REPORT_DEPENDENCY_MAP.csv` décrit les relations autorisées entre audits, corrections et validations.

## 22. Index régionaux

Un README existe pour chaque région effectivement utilisée.

## 23. Organisation Inde

Les 100 fichiers sont répartis entre vue d’ensemble, EIC, infrastructure/famines, Sepoy et setup territorial ; la clôture dispose d’un dossier dédié.

## 24. Organisation Japon

Les 13 rapports HOTFIX-4 restent regroupés sans sur-segmentation.

## 25. Organisation Mamluk Iraq

Les 7 rapports HOTFIX-3 restent regroupés chronologiquement.

## 26. Rapports transversaux

Deux rapports réellement transversaux sont classés dans `shared`.

## 27. Documents other

Aucun document n’exige la catégorie `other`; le dossier n’est donc pas créé.

## 28. Rapports superseded

Les échecs et diagnostics historiques restent accessibles et sont marqués dans l’index sans réécriture.

## 29. Rapports canoniques

Les validations finales B3, E1, G, I, P, T, AB et AG forment la chaîne runtime canonique Inde.

## 30. Clôture Inde

La clôture déclare `HOTFIX_5_INDIA_COMPLETE` et `WEST_BENGAL_RETREAT_TRANSFER_EXPECTED`.

## 31. Contrôles Git

`git diff --check`, état, liste des changements, statistiques, non-suivis et stash sont contrôlés en fin de phase.

## 32. Fichiers créés

Deux index racine, quatre README régionaux, trois CSV d’index, une clôture Inde et son manifeste, ce rapport, le rapport de retrait et son manifeste final.

## 33. Fichiers déplacés

122 fichiers historiques, détaillés individuellement dans la carte de déplacement.

## 34. Fichiers modifiés uniquement pour liens

Aucun ancien rapport n’a été modifié ; zéro réparation de lien.

## 35. Aucun rapport supprimé

`NO_REPORT_DELETED` : le corpus historique avant/après demeure de 122 fichiers, hors nouveaux documents.

## 36. Aucun gameplay modifié

`NO_GAMEPLAY_CHANGED` : aucun fichier sous `common/`, `events/`, `history/` ou `localization/` n’est modifié.

## 37. Verdict

- `HOTFIX_5_INDIA_COMPLETE_AND_REPORT_LIBRARY_INDEXED`
- `HOTFIX_5_INDIA_COMPLETE`
- `REPORT_LIBRARY_REORGANIZED`
- `REPORT_INDEX_COMPLETE`
- `REPORT_LINKS_VALIDATED`
- `NO_REPORT_DELETED`
- `NO_GAMEPLAY_CHANGED`
- `WEST_BENGAL_RETREAT_TRANSFER_EXPECTED`

## 38. Confirmation docs/research/technology/

Le dossier non suivi `docs/research/technology/` est resté hors périmètre et intact.

## 39. Confirmation stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` demeure intact et non appliqué.
