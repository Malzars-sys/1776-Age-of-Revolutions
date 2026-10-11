# MAP-1 — Atlas technique et arbitrages ouverts

10 octobre 2026. Départ historique : 1er janvier 1776. Jeu : Victoria 3 1.13.11.

**L'ingestion et l'indexation technique sont terminées. Le mapping historique
des 410 dossiers n'est pas terminé et aucun transfert n'est prêt pour MAP-2.**
Les livrables consignent les preuves techniques disponibles, les alertes et les
recherches à poursuivre. Ils ne remplacent pas une superposition de carte ancienne.

## Résultats

| Contrôle ou livrable | Résultat |
|---|---:|
| Originaux contrôlés par SHA-256 | 36 / 36 |
| Recommandations uniques | 1 005 |
| Références bibliographiques | 374 |
| Couples State_ID / propriétaire couverts | 1 043 |
| RGB exacts du bitmap | 40 875 |
| Lignes d'attribution conservées, doublons inclus | 40 928 |
| Vues techniques d'États | 280 |
| Aperçus annotés P0 | 20 |
| Fiches individuelles de la file | 410 |
| MAPPING_VERIFIED | 0 |
| MAPPING_PROPOSED au niveau RGB | 0 |
| MAPPING_REQUIRED | 410 |
| Transferts admissibles dans le manifeste | 0 |
| Dossiers interrégionaux, dont DISPUTED | 150, dont 15 |

Les 23 PROPOSED de la recherche initiale ne sont pas devenus VERIFIED. Les
264 REVIEWED_NO_CHANGE de couverture n'ont pas été convertis en provinces vérifiées.
75 demandes de TAG restent des hypothèses de représentation, pas 75 pays à créer.

## Lire les livrables

Ouvrir [l'index des cartes et dossiers](MAP1_REVIEW_INDEX.html) pour les 20 P0,
les 410 cas et les vues RGB zoomables. Les aplats montrent les propriétaires
**écrits actuellement**, pas les frontières historiques proposées.

- [Index pixel / State / propriétaire](MAP1_BASELINE_PROVINCE_INDEX.csv).
- [Correspondances et statuts des 410 cas](MAP1_GEOGRAPHIC_MATCHES.csv).
- [Manifeste de transferts](MAP1_TRANSFER_PROPOSALS.csv) : en-tête seul, intentionnellement vide.
- [80 pistes non admissibles et dépendances](MAP1_TRANSFER_CANDIDATES_NOT_ADMISSIBLE.csv).
- [Incertitudes et interfaces](MAP1_UNRESOLVED_AND_CROSS_REGION.csv) : 410 suivis de file + 150 suivis interrégionaux; pas 560 cas indépendants.
- [Décisions sur le candidat collaborateur](MAP1_COLLABORATOR_MERGE_DECISIONS.md).
- [Barrières avant intégration](MAP1_RELEASE_GATES.md).

Les inventaires démographiques/économiques portent sur 85 États : 748 pops écrites,
487 commandes de création de bâtiments, 8 281 pointeurs de références. Ce sont
des dépendances statiques, pas une simulation des niveaux ou de l'emploi après lancement.

## Arbitrages prioritaires

| Zone | Décision de cette passe | Élément à obtenir |
|---|---|---|
| Luxembourg | Refuser l'absorption en l'état; aucun changement | Contour duché/Chiny/Trèves, maintien du TAG et conservation de 137 881 habitants |
| Lombardie | Refuser le nouveau doublon AUS/VEN; propriétaire non arbitré | Carte Bergame/Brescia/Crema/Mantoue et correspondance des deux RGB |
| Silésie | Séparer scope erroné et souveraineté | Limites austro-prussiennes et rapprochement MORAVIA/WEST_GALICIA |
| Bessarabie | Proposer une réparation syntaxique seule, non appliquée | Périmètres forts/Budjak/Moldavie et décision distincte sur les tokens |
| Bassora | Ne pas anticiper la prise d'avril 1776 | Aire contrôlée pendant le siège au 1er janvier |
| Khorasan | Aucune création de TAG | Étendue afsharide documentée et choix de représentation |
| Bombay | Refuser un transfert du grand RGB au seul nom du port | Plan des îles/Salsette et contrôle de 1774 |
| Circars / Guntur | Ne pas anticiper l'acquisition de 1789 | Clauses 1766/1768 et périmètre du jagir |
| Mandchourie extérieure | Pas de rétroprojection de 1858/1860 | Traité/cartes antérieurs et contrôle local |
| Mindanao | Doubles attributions conservées dans l'audit | Localisation forteresses/sultanats, sans résolution par ordre de chargement |
| Micronésie occidentale | Aucun TAG par défaut | Identifier les îles de xEF50C0; remplacer les références hors zone |
| Kenya / Tanganyika | Pas de transfert colonial ou ethnonymique automatique | Villes, routes, cours d'eau et pouvoirs locaux vers 1776 |
| Alaska / Nunavut | Traite/concession distinctes du contrôle territorial | Postes antérieurs, autorités autochtones et périmètres effectifs |
| Nouveau-Mexique | Pas d'arbitrage des 11 doublons en bloc | Presidios/pueblos et contrôle comanche avant mai 1776 |
| Guyanes | Ne pas généraliser l'administration côtière à l'intérieur | Position de x6C6251, compagnies et autorités locales |
| Rio Grande / Uruguay | Pas de conquêtes de 1776-1777 au départ | Chronologie des places et enclave de Colonia |
| Pastaza | Orphelin SC2 séparé du choix territorial | Missions/districts avant la cédule de 1802 |

Chaque P0 comporte sa question précise et ses références dans le dossier adjacent
à l'aperçu. Ces décisions refusent les inférences non prouvées; elles ne certifient
pas pour autant que les limites actuellement en jeu sont exactes.

## Premiers lots à reprendre, pas à intégrer

1. R1/R2 : Luxembourg, Lombardie et Silésie. Faible nombre de RGB ciblés, dépendances fortes; commencer par les cartes locales.
2. R3/R4 : Bassora puis Bombay/Salsette et Guntur. Chronologie partiellement corroborée, emprise géographique encore manquante.
3. R8/R9 : Nouvelle-Brunswick, La Paz/Ica puis Guyanes/Uruguay. Distinguer correction de juridiction et territoire effectivement contrôlé.

Les autres régions restent suivies dans les fiches. Aucun de ces lots n'a le feu vert
d'intégration. A/B sont à comparer; C n'est pas justifié à ce stade.

## Limites de recherche

13 références originales ont fait l'objet de tentatives d'accès indépendantes;
361 restent bibliographiées sans consultation externe dans cette passe. Les accès
réussis corroborent surtout des chronologies, pas des polygones. Certaines pages
accessibles n'ont pas été intégralement relues. Le
[registre des sources](MAP1_SOURCE_REVIEW.csv) distingue ces situations.
Une source officielle supplémentaire canadienne est conservée séparément.

**Aucune carte historique n'a été calée/superposée.** Certaines archives ont renvoyé
des erreurs d'accès; d'autres références sont uniquement bibliographiques. Cette
limite n'autorise pas à inventer 410 correspondances RGB. Il reste à obtenir les
feuilles/plans, lire les preuves territoriales et confronter les interfaces.

## Protection et tests

Les 1 900 fichiers runtime contrôlés sont inchangés, ainsi que HEAD. Les retouches
préexistantes de version 2.5.0, descriptions Steam et icône chimique sont conservées.
Le worktree collaborateur garde son merge suspendu. Aucun fichier de frontière,
population, bâtiment, armée, diplomatie, technologie ou localisation n'a été modifié
par MAP-1. Aucun lancement de jeu, commit, merge ou push.

Arrêt à cette remise pour lecture/validation. **Ne pas utiliser ce dossier comme
autorisation MAP-2.** La partie historique et géographique fine reste à poursuivre.
