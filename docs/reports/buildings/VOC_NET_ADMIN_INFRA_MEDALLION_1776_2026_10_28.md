# VOC et Pays-Bas — ajustements de départ 1776

Date : 28 octobre 2026. Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. PR à laisser non fusionnée.

## Observations du joueur

La VOC/DEI affiche un déficit de bureaucratie d'environ 105, les Pays-Bas/NET de 19. Les administrations ne recrutent pas intégralement. Java central DEI : infrastructure utilisée 10, disponible 9, accès au marché 82 % sur capture. La fraction DEI des îles de la Sonde n'a aucun port. Le nouveau logo indépendant de la PR #9 ne convient pas.

## Implémentation ciblée

- Java central DEI : réseau régional de type building_railway (PM pm_traditional_road_network) de 2 à **3 niveaux**, propriété inchangée (district financier local DEI).
- Îles de la Sonde, région DEI : **port niveau 1** appartenant à DEI, avec pm_anchorage ; aucune modification BAL/POR.
- Hollande NET : administration gouvernementale **3 à 4 niveaux**.
- Java occidental DEI : **2 000 bureaucrates néerlandais** reclassés depuis les 17 729 Néerlandais déjà présents (15 729 autres). Population totale et culture inchangées.
- Ceylan DEI : **1 250 bureaucrates cinghalais** reclassés depuis le groupe de 696 034 Cinghalais (694 784 autres). Population totale et culture inchangées.
- Hollande NET : **600 bureaucrates néerlandais** reclassés depuis les 624 825 Néerlandais du premier groupe (624 225 autres).
- Nouveau fichier de population zz_1776_dutch_admin_staff_qualifications.txt : l'alphabétisation des **seuls bureaucrates** des États administratifs ciblés DEI (Java occidental, Ceylan) et NET (Hollande) bénéficie d'un plancher de 55 % au départ si inférieur. Les autres métiers, cultures et territoires sont inchangés.
- Logo VOC : l'icône affiche désormais nl_voc_medallion_1776.dds, découpé depuis l'ancien nl_voc.dds, pour conserver son sceau circulaire plutôt que l'emblème précédent avec couronne, lions et volutes. Le fichier ancien et le monogramme de PR #9 sont conservés en historiques Git.

## Preuves statiques

- Les effectifs totaux des POPs de Java occidental (2 900 028), Ceylan (1 438 948, toutes fractions), et Hollande (919 416) sont inchangés.
- Nouveau port DEI + réseau régional central + niveau administratif NET présents dans les fichiers d'histoire ; blocs de code et accolades vérifiés.
- Aucune modification des plantations d'épices 3/2/1 ni de leur propriété VOC.
- Nouveau logo DDS 256x256, 32 bits avec alpha ; changement de référence limité à la VOC.

## Prudence / contrôles en jeu

L'alphabétisation et l'occupation initiale ne suffisent pas à démontrer que tous les emplois seront pourvus. Les niveaux de bureaucratie effectivement produits dépendent des recrutements, lois, salaires et intrants. La liaison au marché par le nouveau port dépend de son emploi et des convois. Les ajustements de populations sont des abstractions de gameplay, pas des recensements documentés d'employés au 1er janvier 1776.

Nouvelle partie : (1) relever le déficit de bureaucratie DEI/NET à J0 puis après quelques semaines ; (2) vérifier les recrutements en Java occidental, Ceylan, Hollande ; (3) vérifier infrastructure DEI Java central et YOG/SRK inchangés ; (4) vérifier port DEI Sonde, connectivité effective et convois ; (5) inspecter la lisibilité et la découpe du médaillon VOC ; (6) avancer un mois, sauvegarder et recharger.

**Aucun démarrage de Victoria 3 ni test de recrutement ou de liaison de marché n'a été effectué automatiquement.**
