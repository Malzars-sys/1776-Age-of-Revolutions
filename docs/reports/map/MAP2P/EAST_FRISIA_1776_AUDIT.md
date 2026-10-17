# Analyse territoriale ciblée

## Distinguer les niveaux de preuve

La [notice administrative du GStA PK](https://archivdatenbank.gsta.spk-berlin.de/midosasearch-gsta/MidosaSEARCH/i_ha_gr_rep_68/xml/inhalt/26660658-9b9a-407e-afde-5d107466323a.htm) établit la période prussienne de 1744 à 1806. Cette certitude politique ne donne pas automatiquement les pixels des villes ou les contours des bailliages. Les catégories A/B/C portent ici sur un **correctif complet**, pas sur la seule chronologie du souverain.

| Ensemble historique | Lecture de la pièce Coldewey et du corpus | Correspondance native vérifiée | Décision |
|---|---|---|---|
| Emden, Aurich, Norden | Villes et ensembles différenciés sur la carte ; souveraineté prussienne en 1776 | xF9DCA2 : enveloppe côtière PRU, 319 cellules ; emplacement individuel des centres non certifié | Conserver la généralisation B ; absence de noms dans le jeu ne signifie pas absence de territoire |
| Esens et Wittmund | Harlingerland, distinct de Jever | Jonction orientale de xF9DCA2 avec xECC3B4 ; pas de nouvelle correspondance ville/pixel certifiée | Maintien ; détail frontalier C |
| Leer / Leerort | Le complexe méridional n'est pas réductible au point urbain de Leer ; la carte distingue les ensembles de part et d'autre de l'Ems | x784B8E : 107 cellules HAN à examiner ; inclusion ou exclusion exacte de Leer non prouvée | Aucun transfert global ; intersection C |
| Rheiderland | Territoire figuré à l'ouest de l'Ems, avec le Dollard et les secteurs endigués | xC0C021 : 331 cellules NET, dont le hub de Groningen ; tout ce RGB ne peut pas devenir prussien | Subdivision éventuellement nécessaire, sous-ensemble non délimité ; C |
| Marge rurale sud | Dépendances méridionales à distinguer des territoires voisins | x784B8E ; x8080E0 (327 cellules HAN) comme enveloppe de contrôle, pas comme acquisition proposée | C ; ne pas défaire les noyaux de Münster/Lingen déjà corrigés |
| Jever | Autorité d'Anhalt-Zerbst en 1776, différente de la Frise prussienne | xECC3B4/xC00161 : enveloppes OLD voisines, pas des polygones historiques certifiés de Jever | Une représentation séparée manque au niveau juridique ; contour C, aucune annexion à PRU |
| Oldenburg / Delmenhorst | Maison de Holstein-Gottorp après 1773 ; souveraineté distincte | Enveloppes OLD conservées | Pas de transfert à PRU |
| Varel / Kniphausen | Droits et gouvernement Bentinck à distinguer de l'autorité d'Oldenburg et de la souveraineté prussienne | Aucun sous-polygone natif suffisamment prouvé | C pour le découpage et la représentation exacte des rapports juridiques |

La [documentation de l'IEG](https://www.hgisg-ekompendium.ieg-mainz.de/Dokumentation_Datensaetze/Multimedia/Staaten/Oldenburg.php) et le [fonds NLA de Jever](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails?fondsId=2640) servent à contrôler ces distinctions. La vente prussienne du secteur de Wilhelmshaven au XIXe siècle et le passage de Jever à la Russie en 1793 ne sont pas importés en 1776.

## Contrôle des trois sous-secteurs de xF9DCA2

1. **Nord, Y ≤ 749 : 104 cellules.** Noyau côtier et direction du Harlingerland compatibles à grande échelle ; pas de restitution des îles séparées démontrée par ce seul RGB.
2. **Centre, 750 ≤ Y ≤ 756 : 153 cellules.** Intérieur de la grande enveloppe ; absence de preuve positive d'un territoire voisin absorbé. Aucun point de ville déplacé pour obtenir ce résultat.
3. **Sud, Y ≥ 757 : 62 cellules.** Interface à comparer au sud historique. Cette bande signale un contrôle nécessaire : elle ne signifie pas que 62 cellules sont étrangères ou doivent retourner à HAN.

Le découpage en bandes est purement technique et reproductible. Le relevé de 1745/1746 Wittmund–Jever décrit par le [Schlossmuseum](https://www.schlossmuseum.de/sammlungen/virtuelle-sammlungen/regionalgeschichte/landkarten-und-plaene/) constitue une source locale future pertinente ; sa simple notice ne permet pas de tracer le contour dans le bitmap. Aucun résultat métrique d'un modèle balte n'est transposé à cet endroit.

Le nouveau diagnostic du relief tient compte du facteur deux entre les dimensions du heightmap et celles des provinces. L'ancien aperçu non redimensionné n'est pas réutilisé comme repère. La correction d'échelle des indices d'image ne constitue ni un géoréférencement historique ni une amélioration démontrée de l'erreur de localisation des villes.

## Îles et estuaires

La pièce distingue Borkum, Juist, Norderney, Baltrum, Langeoog et Spiekeroog de Wangerooge, située du côté de Jever. Un nom moderne d'« îles frisonnes orientales » ne suffit donc pas à rendre chaque île prussienne en 1776. Les plans urbains d'Emden et d'Aurich, en cartouches, ne sont pas des îles géographiques à importer.

Le parent xF9DCA2 est une enveloppe continentale ; son contrôle ne démontre pas que les îles sont correctement représentées, ni que chaque terre émergée manquante doit être créée. Aucune restitution de côte, digue, île ou chenal n'est proposée sans calage local défendable. Les endiguements postérieurs à 1730 restent un risque chronologique explicite.

## Réfutations utiles

- « Leer n'est pas affichée, donc elle est hanovrienne » : non démontré.
- « Le RGB sud touche Emden, donc ses 107 cellules sont prussiennes » : non démontré.
- « Le voisin OLD prouve que toute cellule de Jever est hors du parent PRU » : non démontré.
- « La carte historique a des contours, donc leur superposition native est acquise » : faux sans correspondance locale vérifiée.
- « Aucun débordement n'est confirmé, donc le transfert des 319 est géographiquement parfait » : conclusion non autorisée.

Le maintien de MAP2O respecte son acceptation manuelle sans transformer celle-ci en certification historique. Les décisions territoriales supplémentaires attendent une pièce qui modifie réellement la correspondance source/bitmap, pas une nouvelle optimisation sur les mêmes points.
