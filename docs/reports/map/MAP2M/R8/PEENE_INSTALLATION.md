# Installation de la généralisation politique approuvée

## Autorité et périmètre

La demande utilisateur R8 accepte la variante B de R7 sous réserve des vérifications préalables. Les six documents/image demandés de R7 ont été lus/examinés intégralement avant installation. Leur statut ancien « en attente » est conservé dans les fichiers R7 immuables ; la décision appliquée est enregistrée ici et dans `PEENE_TERRITORIAL_CHANGES.csv`.

La carte Mayer/Lotter 1763 conservée établit la souveraineté suédoise du continent occidental du Peenestrom, par opposition à Usedom prussienne. La rive actuelle LUNG et ses quatre projections R5 figées sont une aide de dessin, pas une frontière cadastrale de 1776. Aucun ajustement de projection, nouvelle recherche générale ou importation des candidats C n'est effectué.

## Vérification puis installation

Avant le remplacement du bitmap, `prepare` vérifie les 41 RGB prussiens actuels, le propriétaire et le State_ID des RGB source/cible, l'absence d'eau, l'appartenance au support R5, le retrait du bord droit à l'ouest de chaque variante de rive, la continuité par côtés et l'exclusion des lignes Y≥740. Les empreintes de tous les fichiers fonctionnels correspondent alors à R7. Le bitmap avant installation est conservé dans `provinces_before.png`.

| Y natif, origine en haut | X inclusifs transférés | Nombre |
| ---: | --- | ---: |
| 732 | 4407–4408 | 2 |
| 733 | 4406–4409 | 4 |
| 734 | 4405–4409 | 5 |
| 735 | 4405–4408 | 4 |
| 736 | 4405–4409 | 5 |
| 737 | 4405–4410 | 6 |
| 738 | 4405–4411 | 7 |
| 739 | 4404–4411 | 8 |
| Total | xE1A03A PRU → x567452 SWE | 41 |

La superficie de 417,9 km² est l'estimation de dessin déjà donnée par R7. Elle ne certifie pas la superficie de la possession historique. Les trois cellules A sont incluses dans ces 41. Le fichier candidat puis le fichier installé sont comparés pixel par pixel au bitmap capturé ; aucun autre pixel ne change.

La redistribution démographique est appliquée après examen du patch préparé, puis le candidat raster est installé avec vérification des empreintes et du texte. Le résultat suédois compte 398 cellules ; le parent prussien en compte 292. Les deux RGB restent d'un seul tenant et correctement référencés. Il n'y a aucun nouveau pays, RGB ou State_ID.

## Limites maintenues

- **Wolgast :** le repère provisoire `(4410,735)` reste `xE1A03A`, PRU. Il n'est pas un centre historique certifié et aucun locator n'est déplacé.
- **Peendamm/Anklam :** toutes les lignes Y≥740 sont inchangées. Aucune enclave urbaine n'est agrandie artificiellement.
- **Demmin :** aucun transfert, secteur extérieur au rectangle retenu.
- **Usedom/Wollin :** aucune cellule insulaire transférée ; les emprises orientales sont comparées et inchangées.
- **Netze :** aucun transfert nouveau, aucune nouvelle optimisation des mêmes points.

Le statut reste **B_APPROVED_APPROXIMATION**. Une bonne conservation technique n'est ni une certification géodésique ni une clôture historique de toute la Peene.
