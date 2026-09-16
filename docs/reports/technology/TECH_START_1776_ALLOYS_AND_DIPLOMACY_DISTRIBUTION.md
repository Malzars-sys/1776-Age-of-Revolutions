# TECH START 1776 — Alliages et relations internationales

## Élaboration des alliages

`alloysworking` représente une production industrielle fiable d'alliages par contrôle méthodique des charges et des proportions métalliques. Le simple travail artisanal du bronze, du laiton ou de l'acier ne suffit donc pas à justifier cette technologie et son usine dédiée.

La technologie est attribuée au départ aux neuf pôles métallurgiques suivants :

- `AUS` — Autriche
- `BEO` — Pays-Bas autrichiens
- `CHI` — Chine
- `FRA` — France
- `GBR` — Grande-Bretagne
- `PRU` — Prusse
- `RUS` — Russie
- `SAX` — Saxe
- `SWE` — Suède

Tous possèdent déjà `shaft_mining`, directement ou par leur effet de palier initial. Aucun prérequis supplémentaire n'est ajouté artificiellement pour distribuer `alloysworking`.

La technologie n'est pas placée dans un effet de palier global : cela l'aurait aussi accordée à des pays dont la capacité minière, métallurgique ou industrielle ne justifie pas l'usine d'alliages en 1776.

## Relations internationales

Le critère retenu est l'existence d'un appareil politique capable d'entretenir des relations diplomatiques formalisées et d'utiliser le système de traités du jeu. La taille ou le statut de puissance reconnue ne suffisent pas à eux seuls.

- `BEO` récupère `international_relations`. Les Pays-Bas autrichiens sont jouables et disposent d'institutions administratives et commerciales assez développées pour que l'absence du nœud soit incohérente en jeu.
- La technologie est retirée des onze tags dont la définition active porte `country_type = decentralized` : `ABB`, `COM`, `GNI`, `JBB`, `KBB`, `MBB`, `MICC`, `SD1`, `SML`, `TNG` et `TRM`.
- Les petits États centralisés africains ne sont pas retirés automatiquement. Plusieurs disposent de relations interétatiques, commerciales ou tributaires documentées ; leur petite taille ne les assimile pas à une puissance décentralisée.

Cette passe ne modifie aucune autre technologie de départ.
