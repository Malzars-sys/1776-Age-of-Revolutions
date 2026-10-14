# Franconie — fondement géographique du lot appliqué

## Références conservées, pas de reprise de la recherche

Le tracé réutilise les sources et décisions de MAP2L. La carte Homann conservée dans `../GEOMETRY/Homann_reading.jpg` est une dérivée de lecture de 2 263 × 2 600 pixels de l'image d'archives de 2 704 × 3 107 pixels. Sa signature est Stadtarchiv Nürnberg A4/IV nº 74. La [notice portant le crédit d'archives](https://www.br.de/br-fernsehen/sendungen/1806/circuli-franconiae-fraenkischer-reichskreis-100.html) ne donne pas une date suffisamment précise pour certifier à elle seule l'état du 1er janvier 1776.

La [carte Le Rouge conservée à la BSB](https://www.bavarikon.de/object/bav%3ABSB-MAP-00000BSB00090735?cq=&lang=en&p=1), cataloguée 1743 et publiée après 1764, sert de confrontation des grandes juridictions. Elle n'a pas été indépendamment calée par un second modèle quantitatif. Les pages de lecture déjà conservées du dossier d'Endres sur le cercle franconien sont réutilisées pour les estates et les unions personnelles. La carte générale de 1789 et les agrégats de Cliopatria ont été écartés pour l'attribution fine : ils regroupent les petits territoires.

## Calage mesurable

Les coordonnées source désignent la dérivée Homann, les coordonnées de destination le PNG natif du jeu, origine en haut à gauche. `ALIGNMENT.json` contient la matrice et tous les contrôles ; `TRACING.json` contient les enveloppes dessinées dans la source ; `HISTORICAL_OVERLAY.png` les montre sur cette source.

| Repère | Source x, y | Jeu x, y | Rôle |
| --- | --- | --- | --- |
| Würzburg | 209, 1245 | 4322.240, 861.541 | Ajustement |
| Nuremberg | 1223, 1598 | 4351.554, 877.180 | Ajustement |
| Bayreuth | 1563, 985 | 4362.608, 862.394 | Ajustement |
| Ratisbonne | 2058, 2170 | 4373.729, 892.864 | Contrôle indépendant |

L'ajustement affine sur trois points donne par construction un résidu nul sur ceux-ci : cela ne démontre pas une précision historique parfaite. Le contrôle indépendant de Ratisbonne donne un écart de **5,121 pixels du jeu**, qui impose de conserver l'incertitude des franges.

Le locator natif de ferme nommé auparavant Coburg est à 2,095 pixels du Bamberg projeté, contre 12,386 pixels du Coburg historique projeté. Ce nom a donc été rejeté comme point de calage. Le locator et son RGB `x648AD1` ne sont pas déplacés ; le libellé est corrigé en Bamberg et le territoire attribué à FBM. Cette correction ne sert pas à attribuer toute une province par proximité d'un nom.

## Attribution à la résolution du jeu

Les enveloppes de juridictions sont manuellement retracées dans la source, puis projetées et intersectées avec les huit polygones natifs de `STATE_FRANCONIA` uniquement. Il ne s'agit pas d'un partage par rayons de villes ou d'un diagramme de Voronoï. Chaque composante à quatre voisins reçoit une identité RGB ; l'identité ancienne est conservée aux locators ou sur une composante retenue. Les minuscules fragments isolés d'un pixel sont abstraits dans un voisin du même parent, sans agrandissement ; leur liste est conservée dans `GEOMETRY.json`.

`STATE_FRANCONIA`, ID numérique natif **72**, demeure une région économique partagée. Un RGB est une identité technique de polygone, pas un identifiant d'État historique. Les correspondances exactes parent/enfant/propriétaire sont dans `TERRITORIAL_CHANGES.csv`, avec les cellules exactes dans `GEOMETRY.json`.

## Situation politique retenue

- Ansbach et Bayreuth ont deux enveloppes distinctes mais un seul pays ANS, conformément à l'union personnelle de 1769. Ils ne sont pas prussiens au démarrage : la [notice officielle de la résidence d'Ansbach](https://schloesser.bayern.de/deutsch/schloss/objekte/ansbach.htm) place la cession en 1791 ; les [portraits conservés](https://schloesser.bayern.de/deutsch/presse/archiv10/kulmbach/gemaeld1.htm) documentent le margrave Alexander.
- Bamberg et Würzburg demeurent deux estates distincts, gouvernés par Adam Friedrich von Seinsheim. La [fiche Germania Sacra](https://personendatenbank.germania-sacra.de/index/gsn/082-01199-001) documente Würzburg depuis 1755 et Bamberg depuis 1757. Deux instances du personnage sont une abstraction technique, pas deux évêques historiques différents.
- Nuremberg est représentée comme ville libre à conseil patricien ; aucun titre électoral supplémentaire n'est créé.
- Eichstätt ne reçoit ici que le fragment septentrional représentable dans cette région. Raymund Anton von Strasoldo est bien évêque en 1776 selon l'[historique officiel du diocèse](https://www.bistum-eichstaett.de/wir-sind/das-bistum/geschichte-des-bistums-eichstaett/). La capitale économique du jeu ne certifie pas la position de la ville historique dans le fragment.
- Le pays COB déjà présent reçoit le fragment retracé sans changement de sa capitale ni de son organisation existante.

Ces contrôles de titulaires ne transforment pas chaque limite du scan en frontière cadastrale certifiée au jour près. **662 pixels sur 1 984 restent à BAV sans souveraineté bavaroise certifiée.** Les franges, les juridictions secondaires et les prolongements hors région sont explicitement recensés dans `UNRESOLVED.csv`.
