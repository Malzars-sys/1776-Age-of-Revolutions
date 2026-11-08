# Réserves occidentales — arbitrage borné pour la V1

Décision de travail du 5 novembre 2026, prise par l'agent sur l'autorisation explicite : « Continue sur ta lancée, arbitre les réserves occidentales. » **Ce document n'est pas une attestation humaine de fonctionnement, ni une validation cadastrale.** Périmètre : `SC5-PRUSSIAN-WEST`, sans autre région ou Bavière.

## Décisions opérationnelles

| Réserve | Décision | Portée et limite |
| --- | --- | --- |
| Venlo et Beesel encore BEO | Corriger deux noyaux vers NET, quatre cellules chacun. | Souveraineté néerlandaise établie ; approximation politique B aux limites. Pas la totalité de l'ancien Staats-Opper-Gelre, ni les acquisitions de 1785. |
| Droit impérial enregistré sur ces cellules | Exclure les huit cellules du domaine de restitution BEO ; ne créer aucun titre NET. | Le traité cède les possessions aux États généraux ; la restitution automatique à BEO contredirait cette souveraineté. Aucune adhésion nationale NET, aucun élargissement d'une exception suédoise. Les 599 titres existants restent identiques, leur étendue enregistrée diminue seulement de huit cellules. |
| Clèves/Emmerich | Maintenir la limite existante pour la V1. | Les discordances de lecture ne déterminent pas une correction de cellules suffisamment étayée. Ce maintien B ne certifie pas toutes les limites ni les petites juridictions. |
| Mark : Unna/Meinerzhagen | Maintenir la représentation actuelle pour la V1. | Aucun transfert fondé uniquement sur une ville projetée ; voisins protégés conservés. Pas de reprise de noyaux KCL ou KPF validés. |
| Berg : ancien candidat de 39 cellules | Écarter l'installation de ce candidat ; maintien actuel pour la V1. | Le désaccord ancien entre modèles n'est pas une erreur démontrée. Aucun nouveau recalage ni transfert artificiel. |

Ces réserves de précision cessent de bloquer la **préparation de la réception moteur occidentale**. Elles restent des limites historiques déclarées, sans statut terminal ni point. L'agent ne prétend pas que le joueur a approuvé individuellement ces frontières. Le report des micro-États par le joueur et la priorité aux écarts visibles restent applicables ; aucune obligation canonique n'est supprimée.

## Sources décisives effectivement consultées

1. [Université de Maastricht, Staats Opper-Gelre](https://www.maastrichtuniversity.nl/nl/nl/over-de-um/faculteiten/rechtsgeleerdheid/capaciteitsgroepen/privaatrecht/projecten/limburgse-rechtsgeschiedenis/onderzoek/staats-opper-gelre), rubrique institutionnelle et carte `LRG_Ovkw4`. Le partage de 1715 comprend Venlo/Fort Saint-Michel et Beesel/Belfeld dans le ressort des États généraux ; leur gouvernement et leur législation relèvent de ceux-ci et du Conseil d'État. Les ajouts de 1785 sont explicitement ultérieurs à la cible. Cache et image de la passe précédente conservés dans `../CLEVE_GUELDRE_MARK_2026_11_05/EVIDENCE/MAASTRICHT_*`.
2. [Traité de la Barrière, 15 novembre 1715, article XVIII, transcription](https://fr.wikipedia.org/wiki/Trait%C3%A9_de_la_Barri%C3%A8re_%281715%29). La transcription cède en souveraineté et propriété Venlo et le ressort de Montfort, dont Beesel/Belfeld, tout en réservant Swalmen/Elmpt et les droits prussiens. **Transcription secondaire, pas nouvel original numérisé vérifié** ; elle est utilisée avec la source universitaire, pas comme seule preuve.
3. Bohn, *Cleve, Geldern, Moers und Mark*, Hambourg, 1793, UB Berne MUE Ryh 5106:3 B, [notice et reproduction primaire](https://doi.org/10.3931/e-rara-124818). La poche de Venlo est distincte de la Gueldre prussienne. La reproduction et sa lecture locale ont déjà été examinées dans les passes précédentes ; elles sont réutilisées, sans nouvel audit général ni attribution automatique de toutes les couleurs de 1793 à 1776.
4. [Gemeentearchief Roermond, Hoofdstad van Gelderland](https://www.archiefroermond.nl/verleden/verhalen/een-andere-geschiedenis/gouden-tijden/hoofdstad-van-gelderland), illustration rétrospective Hantsche du partage après 1715. Corrobore les ensembles prussien, néerlandais et autrichien ; le trait de frontière contemporaine n'est pas repris comme limite historique.

La [synthèse précédente](../CLEVE_GUELDRE_MARK_2026_11_05/SOURCES.md) et les preuves des anciennes passes Clèves/Mark/Berg sont réutilisées sans les réécrire. Aucun fait historique ponctuel ne devient une instruction permanente.

Une piste supplémentaire, `https://law.maastrichtuniversity.nl/lrg/wp-content/uploads/2014/01/limburg.pdf`, n'a pas pu être obtenue : échec de récupération web puis certificat HTTPS ne correspondant pas au nom d'hôte. Le PDF n'a pas été lu ; ses extraits de moteur de recherche ne fondent **aucune conclusion**. L'arbitrage de restitution ne prétend donc pas résoudre toute la doctrine du lien entre Pays-Bas, cercle de Bourgogne et Empire : il retire seulement un droit BEO incompatible avec la souveraineté néerlandaise attestée sur ces noyaux.

## Géométrie et arrondis assumés

La transformation image→carte de la passe précédente est réutilisée **sans recalage**. `TRACING.json` conserve les deux contours et les cellules choisies ; les contrôles de l'image ne sont pas une certification de position des villes dans le jeu.

- **PW-VENLO-NET-B4** : poche de quatre cellules, `xEEC700`, entièrement prise dans le parent BEO restant. Une sélection trop intérieure de deux puis trois cellules laissait un résidu BEO artificiel de deux puis une cellule au nord. L'arbitrage B retient le petit bloc complet ; chaque cellule intersecte le contour de la poche, avec un seuil exploratoire déclaré de 25 % de couverture échantillonnée. Cette règle locale d'arrondi ne garantit pas la frontière cadastrale et n'est pas généralisée à d'autres territoires.
- **PW-BEESEL-NET-B4** : quatre cellules, `xEEC701`, représentant la bande continue Beesel/Belfeld. Échantillonnage 16×16 et seuil local de 40 % ; la cellule de jonction est effectivement intersectée par le contour. Cela évite de représenter la bande par deux fragments diagonaux sans créer un corridor hors de son voisinage historique.

Les brouillons non installés sont consignés dans `PREPARATION_DIAGNOSTICS.json`. **Aucune ancienne cellule PRU, aucun noyau validé, aucun pixel d'un autre parent n'est repris pour réaliser ces arrondis.** Roermond reste BEO, le parent conserve 157 cellules continues. Le domaine enregistré de restitution impériale perd exactement les huit cellules NET ; aucun autre titre ou membre n'est changé.

La population transférée est une redistribution technique des profils BEO/Gueldre existants, jamais la population historique complète de ces villes ou ressorts. Les bâtiments, PM, détenteurs et unités restent conservés. Les deux noyaux doivent être vérifiés dans la prochaine session moteur groupée ; l'arbitrage documentaire ne remplace pas ce test.
