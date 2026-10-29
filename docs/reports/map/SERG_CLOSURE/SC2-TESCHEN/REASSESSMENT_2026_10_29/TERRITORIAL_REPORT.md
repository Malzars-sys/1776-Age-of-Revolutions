# Teschen au 1er janvier 1776 : territoire, fief et domaines

La représentation sous `AUS` est politiquement défendable. Elle ne signifie ni que Marie-Christine et Albert possèdent toutes les seigneuries de la région, ni que le duché central coïncide avec toute la Silésie de Teschen. La preuve d'une correspondance géographique d'ensemble avec le RGB manque encore ; cette réserve dépasse une question de micro-enclaves.

Références : identifiants S1–S6 du [registre des sources](SOURCES.md).

## Autorités et juridictions

| Ensemble | Situation applicable à 1776 | Autorité / propriété à distinguer | Certitude et conséquence pour le mod |
| --- | --- | --- | --- |
| Duché central de Teschen/Cieszyn | Axe de l'Olza et quatre villes : Cieszyn/Teschen, Skoczów/Skotschau, Strumień/Schwarzwasser, Jabłonków/Jablunkau. | Fief attribué à Marie-Christine et Albert le 31 mai 1766, dans le cadre de la couronne de Bohême et de la monarchie habsbourgeoise. Hommage des nobles et des quatre villes le 1er octobre 1766. | Élevée sur le cadre juridique : S1 pp. 13, 78–79. Conserver `AUS` n'oblige pas à créer un pays souverain ducal. Contour de 1776 non numérisé. |
| Domaines de la Chambre de Teschen | Domaine direct distinct de la totalité du duché et de sa noblesse foncière. S1 mentionne les représentants de **48 villages de Chambre** à l'hommage du 2 octobre **1766**. | Propriété et gestion domaniales du couple ; ne pas confondre avec l'administration politique de tous les habitants. | Élevée pour l'événement, incomplète pour l'inventaire exact de 1776 : S1 p. 79. Les 48 villages ne deviennent pas une liste cadastrale complète de 1776. |
| Frýdek / Friedek | Seigneurie distincte issue du démembrement de 1572. Jan Nepomuk Pražma la détient en 1776. | Seigneur particulier relevant du cadre royal bohémien/silésien. Vente au couple ducal en **1797**, pas avant. | Élevée : S1 pp. 13–14 ; S5. Ne pas déclarer Frýdek propriété personnelle du couple en 1776. |
| Fryštát / Freystadt / Frysztat | Seigneurie particulière, avec des domaines voisins ayant leur propre histoire. Rudolf Taafe hérite en 1769 ; vente Larisch en 1792. | Autorité supérieure royale distincte de la propriété Taafe. Les domaines de Raj et de Německá Lutyně ne deviennent pas les domaines personnels d'Albert par proximité. | Élevée pour cette séquence : S1 p. 16 et note 9. Deux dates d'acquisition Taafe 1748/1749 apparaissent dans le récit, sans effet sur le détenteur de 1776 ; ne pas les fusionner artificiellement. |
| Bielsko / Bielitz | Possession Sułkowski depuis 1752 ; principauté de rang inférieur en 1752, puis duché de rang supérieur en 1754. August Sułkowski est le deuxième duc, avant son décès en 1786. | Duché distinct, dans le cadre habsbourgeois et bohémien ; pas propriété personnelle de Marie-Christine et Albert. | Élevée pour la distinction et les changements de rang : S1 pp. 13, 15–16 ; S6. Le seul mot « duché » ne prouve pas une souveraineté internationale indépendante à simuler. |
| Autres domaines nobles de Silésie de Teschen | Rychwałd/Rychvald, Raj/Ráj, Německá Lutyně et propriétés nobles au sein du duché ne se réduisent pas au domaine de Chambre. | Propriété noble, juridiction particulière et autorité habsbourgeoise sont des niveaux différents. | Élevée sur cette distinction, variable pour chaque limite parcellaire : S1 pp. 13–16. Un même propriétaire `AUS` ne certifie pas un domaine ducal unique. |
| Altenburg/Magyaróvár et Bellye | Autres possessions du couple en Hongrie. | Lien patrimonial personnel ; aucun rattachement territorial à Teschen ni justification d'extension impériale par ce seul lien. | Élevée : S1 p. 80. Exclus de l'emprise Teschen et du présent registre. |

L'exercice des institutions royales silésiennes ne se confond pas avec la Chambre domaniale. L'union administrative ultérieure avec la Moravie en 1782–1783 et les districts postérieurs ne définissent pas le départ de 1776 (S3).

## Voisinages à exclure ou à traiter séparément

| Frontière | Ce qui peut être établi | Limite de la preuve |
| --- | --- | --- |
| Nord : Silésie prussienne | Le partage de 1742, confirmé avant 1776, interdit d'intégrer par défaut la Silésie prussienne au duché habsbourgeois. | Les anciens modèles MAP1B/MAP1C ne certifient pas chaque bord du RGB. Aucun transfert de voisin prussien proposé. |
| Ouest : Moravie, Hukvaldy et Místek | L'Ostravice sépare notamment la seigneurie silésienne de Frýdek des domaines moraves de l'évêque d'Olomouc ; accord et bornage de 1668–1669 (S1 p. 14). | Frýdek et Místek ne sont pas une seule juridiction politique parce que leur ville contemporaine est réunie. Toutes les possessions autrichiennes voisines ne sont pas Teschen. |
| Est : Biała et Galicie | La frontière ancienne vers Biała et les territoires polonais doit être réexaminée dans le contexte du partage de 1772. Une autorité habsbourgeoise après 1772 n'en fait pas un territoire de la couronne de Bohême ni un titre impérial Teschen. | Pas de classement de toute `STATE_WEST_GALICIA` dans l'Empire. La Biała proche de Bielsko ne doit pas être confondue avec le faubourg Bělá/Biała de Jablunkov cité par les dénombrements. |
| Sud : Hongrie et Beskides | S1 p. 14 signale un arbitrage de 1766 sur les versants méridionaux, contesté par les Esterházy. | La frontière de crête stabilisée au XIXe siècle ne résout pas rétroactivement cette contestation en 1776. Ni frontière actuelle tchèque/slovaque, ni limite contemporaine ne sont utilisées. |

## Correspondance avec les 179 cellules

Constat vérifiable : `x9061E0` forme **179 cellules**, boîte inclusive `[4520,862,4537,878]`, un seul propriétaire `AUS`, définition physique `STATE_WEST_GALICIA`. La carte du jeu conserve un unique polygone ; elle n'identifie pas par elle-même Frýdek, Fryštát ou Bielsko.

La lecture Seutter distingue bien les ensembles mentionnés ; elle n'est pas recalée de façon probante sur le jeu. Les essais antérieurs sont explicitement rejetés : erreur méridionale Olomouc de **27,864 pixels jeu** dans MAP1B, à comparer à une boîte Teschen de seulement **18 × 17 pixels**. Ce rapport d'échelle n'est ni une marge d'erreur statistique ni une autorisation de transférer les RGB. Sources locales préservées : `MAP1B/.../SILESIA_READING.md` et `MAP1C/.../METHOD_AND_EVIDENCE.md`, avec la ligne `SIL-TECH-01` de `MAP1C_MAPPING_DECISIONS.csv`.

| Élément historique | Correspondance soutenable avec le mod | Ce qui reste inconnu |
| --- | --- | --- |
| Noyau Teschen–Bielsko | Position générale héritée dans le corridor au sud de la Silésie prussienne et à l'est de la Moravie ; étiquette diagnostique MAP1B « Teschen/Bielsko ». | Présence des localités et couverture d'ensemble à l'intérieur des 179 cellules, non certifiées par cette seule étiquette. |
| Frýdek et Fryštát | Juridictions habsbourgeoises identifiées dans les sources. | Leur partage entre ce RGB et les RGB moraves voisins. Aucune liste de cellules n'est fabriquée pour remplir ce manque. |
| Voisins immédiats | Inventaire existant : `x71E080`/`x10DFDF` à l'ouest/sud-ouest, AUS/Moravie ; `x7B2F62` au nord, PRU ; `x906060` et `x1161E0` au nord-est/est, GAL. Propriétés actuelles contrôlées statiquement. | Un voisinage de pixels ne prouve pas le nom historique de chacun de ces polygones. |

La condition nécessaire à une correction ciblée est une correspondance de **quelques localités structurantes et des grands ensembles**, avec des témoins indépendants ; aucun cadastre parfait n'est exigé. En son absence, ni l'ajout de Frýdek au RGB, ni une amputation vers la Galicie ne serait défendable. Aucun ancien recalage improductif n'a été relancé.
