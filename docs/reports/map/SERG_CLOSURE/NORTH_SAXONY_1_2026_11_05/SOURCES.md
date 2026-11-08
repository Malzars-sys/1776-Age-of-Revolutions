# Nord saxon 1 — sources, décision et limites

Référence politique : **1er janvier 1776**. Lecture et décision de cette passe : 5 novembre 2026. Les dates de collecte ne sont pas des dates de test joueur.

## Carte primaire effectivement examinée

**Petrus Schenk, Neue Karte des Kuhrfürstenthums Sachsen und sämtlicher incorporirter Lande**, Amsterdam, **1758**, Universitätsbibliothek Bern, Sammlung Ryhiner, **MUE Ryh 5301:30**, environ 1:480 000, 49 × 72 cm. [Notice institutionnelle](https://ryhiner.ub.unibe.ch/de/world/volume/147/image/16241), [DOI](https://doi.org/10.3931/e-rara-124790).

La notice conservée dans `EVIDENCE/SCHENK_SAXONY_CATALOG.html` indique 1758, et non 1776. L'image IIIF réellement obtenue est `EVIDENCE/SCHENK_SAXONY.jpg`, **3000 × 2376**, via [l'API institutionnelle](https://www.e-rara.ch/i3f/v20/29647539/full/3000,/0/default.jpg). Les essais du serveur v30 ont échoué ; la page de protection de Deutsche Fotothek et les refus Gallica ne sont pas des cartes examinées. Ils ne constituent aucune preuve supplémentaire.

La feuille distingue le Kurkreis, les régions de Meissen et Leipzig, les Stifter de Mersebourg/Naumbourg/Zeitz, Anhalt, la marche de Brandebourg et les Lusaces. Les couleurs des districts ne sont pas assimilées à des souverainetés indépendantes. Baruth figure dans le territoire saxon ; la poche brandebourgeoise de Cottbus/Peitz reste une exception à préserver.

`SCHENK_NORTH_GRID.jpg`, `SCHENK_KURKREIS_GRID.jpg`, `SCHENK_NORTH_DETAIL.jpg`, `SCHENK_BITTERFELD_GRID.jpg`, `SYMBOL_DETAIL.jpg` et `SOURCE_TRACE_REVIEW.jpg` rendent les lectures révisables. La polyligne dépasse le périmètre installé : seules les cellules des six parents déclarés, actuellement PRU et appartenant aux deux régions techniques autorisées, peuvent changer.

## Contrôle chronologique

- [Sächsisches Staatsarchiv, structure des anciennes possessions](https://www.archiv.sachsen.de/archiv/bestand.jsp?bestandid=10012&oid=01.03) : Jüterbog et Dahme dans l'apanage de Saxe-Weissenfels jusqu'à son extinction en 1746 ; ne pas prolonger cet apanage distinct en 1776.
- [Sächsisches Staatsarchiv, dossiers de limites de Belzig](https://www.archiv.sachsen.de/archiv/bestand.jsp?bestandid=10025&oid=01.05.01&syg_id=365909) : dossiers de frontière Saxe–Brandebourg, dont des pièces de 1708–1777. La notice confirme le contexte frontalier ; les plans d'archives non ouverts ne servent pas à certifier un tracé par cellule.
- [Sächsisches Staatsarchiv, changements territoriaux de 1815](https://www.archiv.sachsen.de/orts-und-heimatgeschichte-8293.html) : les cessions du Kurkreis et d'autres régions saxonnes sont postérieures au départ de 1776. Leur attribution prussienne de 1836 ne doit pas être projetée sur 1776.

La combinaison de ces notices et de la carte antérieure fonde l'attribution saxonne du noyau. Il s'agit d'une **inférence de continuité politique jusqu'en 1776**, pas d'une carte datée de 1776 ni d'une vérification exhaustive de chaque juridiction.

## Décision installable, catégorie B

Deux sous-lots contrôlables séparément :

1. **NS1-KURKREIS** : Wittenberg–Torgau–Annaburg et raccord Bitterfeld/Düben/Delitzsch/Eilenburg, dans la région économique native `STATE_ANHALT`.
2. **NS1-FLAMING-MEISSEN** : Belzig, Jüterbog, Dahme, Baruth, Herzberg et raccord Liebenwerda/Elsterwerda, dans `STATE_BRANDENBURG`.

Les noms des régions techniques ne deviennent pas des affirmations historiques. Aucun déplacement de leurs limites économiques, aucun pays nouveau. Les populations sont une redistribution technique exacte des profils existants de PRU ; les parts de cellules sont des poids de scénario, **pas des effectifs historiques mesurés**.

Le modèle natif Miller existant est figé. Seule la feuille ancienne est ajustée par une transformation affine ; sept points de lecture donnent des résidus de **0,73 à 1,85 cellule native**. Ce sont des résidus d'ajustement, **pas une précision validée par des points indépendants**. Les quatorze diagnostics de villes sont des repères géographiques grossiers, non des locators certifiés du jeu.

Deux généralisations explicites complètent le tracé : **une cellule adjacente à Baruth**, compte tenu du résidu local d'environ 1,55 cellule ; **30 cellules de raccord interne saxon** entre ce tracé Schenk et le tracé Lotter des Lusaces déjà installé. Les deux poches de 27 et 3 cellules ne représentent pas une souveraineté prussienne attestée. `SEAM_REVIEW.json`, `TRACING.json` et `GEOMETRY.json` conservent les coordonnées exactes de ces décisions B.

## Hors périmètre et incertitudes conservées

Les noyaux validés d'Anhalt et les **811 cellules lusaciennes précédentes** restent strictement identiques. L'enclave Cottbus/Peitz de **86 cellules** demeure prussienne. Halle, Magdebourg et Potsdam sont conservées. Aucun pixel non prussien n'est recoloré ou réattribué.

Les secteurs de Gommern/Barby, les parts de Mansfeld et la frontière occidentale de la Saale, dont Mersebourg/Naumbourg, **ne sont pas clôturés par Nord saxon 1**. Une petite frange PRU de onze cellules près d'Anhalt, hors de la lecture saxonne et déjà présente dans le parent d'origine, n'est pas assimilée à une possession prussienne historiquement prouvée ; son arbitrage reste ouvert. Le diagnostic grossier de Zeitz tombe sur une cellule WEI : il ne suffit pas à autoriser un transfert depuis un noyau non prussien.

La carte n'est donc pas déclarée cadastrale ou entièrement exacte. La prochaine passe demandée concerne la frontière polonaise ; elle n'est pas exécutée ici. Aucune Bavière, aucun micro-État, aucune révision démographique historique autonome.
