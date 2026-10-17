# Peene — Deux variantes exclusives, aucune installée

Les deux variantes sont de **catégorie B : approximation politique proposée**. La « variante A » n'est pas une correction de « catégorie A ».

| Choix | Pixels nouveaux | Surface ajoutée approximative | Nombre futur de pixels x567452, si approuvé | Compromis |
| --- | ---: | ---: | ---: | --- |
| A : conservatrice | 3 | 30,6 km² | 360 | Retouche minimale, laisse l'essentiel de l'approche de Wolgast ouvert |
| B : généralisation politique | 41, dont les 3 de A | 417,9 km² | 398 | Meilleure continuité continentale, tracé assumé comme simplifié |

État actuel réellement installé : **357 pixels x567452 SWE**. Les deux propositions prennent uniquement des cellules de `xE1A03A`, PRU, dans `STATE_POMERANIA`, pour les rattacher ultérieurement au RGB suédois déjà existant. Aucun TAG, State_ID ou RGB n'est inventé.

## Fondement historique et aide de dessin

Mayer/Lotter 1763 distingue le continent suédois à l'ouest du Peenestrom de l'Usedom prussienne. Le plan d'Anklam et l'hydrographie conservée ne donnent pas une limite cadastrale exacte de chaque petite possession. La souveraineté régionale et la géométrie des cellules restent deux objets distincts.

Le dessin proposé suit le côté occidental d'une enveloppe de quatre projections figées de la rive actuelle LUNG, sans prétendre qu'elle soit identique à celle de 1776. La géométrie n'est pas réajustée. Les pixels d'une variante doivent former des extensions reliées par un côté à la Suède existante. Toutes les cellules proposées sont dans le support du profil ; aucun point extrapolé n'est caché.

**A** exige en outre l'accord des anciennes hypothèses pour les candidates héritées, une marge de 3,19 pixels sur le bord droit et une seule couche adjacente au pays actuel. Cette marge est une convention prudente, pas un intervalle de confiance. Le résultat exact est (4405,736), (4405,737), (4405,738).

**B** retient les terres prussiennes de la fenêtre X [4404,4412[, Y [732,740[ dont la cellule entière reste à l'ouest de toutes les variantes de rive projetées. Elle comprend les 18 anciennes candidates et 23 autres cellules du même corridor, par une règle explicite, et non par importation de tous les candidats R5.

## Liste de B par ligne

| Y | X concernés, bornes incluses | Nombre |
| ---: | --- | ---: |
| 732 | 4407–4408 | 2 |
| 733 | 4406–4409 | 4 |
| 734 | 4405–4409 | 5 |
| 735 | 4405–4408 | 4 |
| 736 | 4405–4409 | 5 |
| 737 | 4405–4410 | 6 |
| 738 | 4405–4411 | 7 |
| 739 | 4404–4411 | 8 |

Le CSV donne une ligne par pixel et par variante, avec propriétaires avant/proposés, RGB, statut d'approbation et mesure du retrait. Ne pas additionner les lignes des deux variantes comme une seule opération.

## Déformations et exclusions

Pour B, le bord oriental proposé reste à environ 0,05–1,92 pixel à l'ouest de l'aide de dessin moderne selon le modèle et la ligne ; pour A, le retrait est beaucoup plus grand, environ 4,05–7,41 pixels sur ses trois lignes. Ces nombres ne mesurent pas un écart certifié à une frontière historique. Les distances de chaque pixel intérieur ne doivent pas être confondues avec celles de la frontière extérieure : le fichier de déformation les sépare.

Les 418 km² de B représentent un corridor d'arrière-pays, pas le territoire urbain de Wolgast ni Peendamm. La surface historique exacte à comparer manque ; aucun rapport de superficie historique n'est fabriqué. Le point urbain provisoire R5 de Wolgast reste hors des deux variantes : le positionnement exact de ce centre n'est pas résolu et n'est pas forcé par un transfert transchenal.

Usedom et Wollin ne sont pas transférées comme ensembles politiques. Demmin est hors fenêtre. Toute nouvelle cellule à Y≥740 est exclue : Anklam prussienne, le voisinage immédiat du moulin et Peendamm ne sont pas remodelés. Cela conserve des secteurs non terminés mais évite de transformer un repère urbain subpixel en enclave de plusieurs kilomètres carrés.

## Pourquoi pas de variante C ?

Une troisième configuration de provinces n'apporterait pas d'espace subpixel : changer les RGB ou ajouter une province ne rétablit pas le chenal absent et augmenterait les dépendances historiques/démographiques. Une refonte de résolution est hors périmètre. Deux choix utiles suffisent ; aucune troisième variante artificielle n'est produite.

**Recommandation : B pour avancer sur le territoire continental ; A pour limiter au maximum le changement. Dans les deux cas : approbation explicite avant installation.**
