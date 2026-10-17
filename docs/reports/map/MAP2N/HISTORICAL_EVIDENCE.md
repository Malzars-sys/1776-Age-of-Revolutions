# Éléments de preuve — MAP2N

## Souveraineté et dates

Le [musée régional de Mecklembourg-Poméranie](https://www.landesmuseum-mv.de/en/historic-atlas/) et la [ville de Wismar](https://www.wismar.de/Tourismus-Welterbe/Kultur-und-Hansestadt/Schwedenzeit/) établissent l'attribution suédoise de Wismar, Poel et Neukloster en 1648 et le règlement postérieur de 1803. Ils justifient la présence suédoise en 1776, pas un tracé cadastral sur le bitmap.

La fiche [HGISG Mecklenburg-Schwerin](https://www.hgisg-ekompendium.ieg-mainz.de/Dokumentation_Datensaetze/Multimedia/Staaten/Mecklenburg-Schwerin.php) est une référence complémentaire. Ses descriptions territoriales du XIXe siècle ne sont pas projetées sans contrôle sur 1776.

## Poel : réserve essentielle

La [fiche municipale de Seedorf](https://www.ostseebad-insel-poel.de/verzeichnis/visitenkarte.php?mandat=262174) situe Seedorf, Weitendorf, Wangern et Brandenhusen dans les possessions lübeckoises jusqu'à l'échange de 1802. La [chronologie locale](https://www.poel-ahnen.de/DatenFakten.html) mentionne leur exclusion de la cession suédoise. Cela interdit de présumer que toute Poel revient à SWE. Il faut encore distinguer biens de l'hôpital, administration et juridiction territoriale : aucune nouvelle propriété économique ou souveraineté RGB n'est déduite automatiquement de cette seule mention.

## Images conservées

### EVIDENCE/ATLAS_1720.png

Source : musée régional, [carte de synthèse 1720](https://www.landesmuseum-mv.de/data/bilder/karten-mecklenburg-pommern/map-mecklenburg-pomerania-1720-01-891.png). Carte moderne de synthèse historique ; utile à l'emprise générale et à la séparation des possessions, insuffisante pour les petites limites de 1776. Image conservée comme preuve uniquement, pas comme ressource du jeu.

### EVIDENCE/WISMAR_COMPARISON_2022.svg et .png

[Swedish Wismar map, Fenn-O-maniC, 5 mai 2022](https://commons.wikimedia.org/wiki/File:Swedish_Wismar_map.svg), licence **CC BY-SA 3.0**. Copies originales non modifiées, conservées pour comparaison ; pas d'intégration au jeu. Toute adaptation graphique diffusée doit conserver attribution, provenance et obligations de partage à l'identique.

La notice de l'auteur cite une carte du duché de Mecklembourg de 1800 pour les frontières et une carte moderne pour l'hydrographie. Elle montre notamment le territoire étendu de Neukloster, distinct de la ville actuelle. Ce n'est **pas** une carte primaire de 1776 et elle ne suffit pas seule à valider chaque cellule. La [notice Deutsche Fotothek citée](https://www.deutschefotothek.de/documents/obj/90010441) a présenté un contrôle d'accès ; le document primaire n'a pas été consulté et ne doit pas être présenté comme vérifié.

## Correspondance au bitmap

Le modèle natif gelé R5 est réutilisé comme diagnostic seulement. Points R2 approximatifs : Wismar (11.466 E, 53.893 N), Poel (11.433 E, 54.000 N), Neukloster (11.683 E, 53.867 N). POSITION_DIAGNOSTICS.json conserve leurs résultats et l'indicateur Certified_position=false. Aucune nouvelle optimisation de projection, aucun ajustement arbitraire de quelques pixels.

Les locators existants sont un contrôle technique de compatibilité, pas une preuve des limites politiques ni de la position exacte des villes de 1776.

## Reconstruction installée de Poel

La côte moderne généralisée déjà conservée dans MAP2M/R3/EVIDENCE/NE_COASTLINE.geojson (Natural Earth, feature 1283, anneau fermé de 18 points, longitude 11.375662–11.497895, latitude 53.961127–54.030951) fournit la géométrie physique. SHA-256 et anneau dans POEL_DIAGNOSTIC.json. Ce n'est pas une preuve cadastrale du littoral de 1776 ; aucun nouveau recalage n'a été effectué.

Les dépendances hospitalières lübeckoises sont abstraites par une cellule sud-ouest, pas leurs quatre contours exacts. Le regroupement de l'île dans STATE_POMERANIA est une décision technique du joueur, pas une conclusion historique.

## Dépendances techniques du relief

Sources primaires : fichiers natifs Victoria 3 1.13 heightmap.heightmap, default.map, PNG de relief/indirection, common/defines/00_defines.txt, et [HeightMapConverter.cs du projet AzgaarToCK3](https://github.com/pryvyd9/AzgaarToCK3/blob/master/Converter/HeightMapConverter.cs), notamment WritePackedHeightMap. Ce code décrit la structure des tuiles ; ses paramètres CK3 ne sont pas copiés comme paramètres Victoria 3.

Le format et l'orientation de cette installation ont été vérifiés numériquement : tailles 65/33, offsets, pas d'échantillonnage et décalage vertical d'un échantillon dans RELIEF_PLAN.json. Les deux tuiles sont référencées une seule fois chacune, leurs bords communs sont modifiés ensemble. Pas de compression mondiale ni de modification du dossier du jeu.

## Continuation Wismar–Neukloster : éléments croisés

La [pièce parlementaire suédoise1903:75](https://data.riksdagen.se/dokument/D03075), désormais consultée, rappelle les titres impériaux acquis en1648, les restitutions dont celle de1720 et reproduit la convention de1803. Elle appuie la continuité de la possession suédoise avant le nantissement, mais ne fournit pas un parcellaire de1776. Les cartes postérieures ne sont pas utilisées pour anticiper le transfert de souveraineté de1803.

La carte comparative conservée distingue les dépendances de Wismar, notamment Benz, et l'Amt Neukloster. Elle est confrontée à l'aperçu1720 du musée, sans confondre leur précision avec celle d'une carte cadastrale. Les petits contours de Martensdorf et les franges nord/est sont généralisés, pas inventés.

Le gazetteer déjà conservé dans MAP1C/MAP1C_GEOGRAPHIC_EVIDENCE/cities1000.zip (GeoNames, CC BY4.0 ; [attribution](https://www.geonames.org/), [licence](https://creativecommons.org/licenses/by/4.0/)) fournit les repères modernes. Le calage utilise les symboles SVG des localités, pas les positions de leurs libellés. Coordonnées, identifiants GeoNames, rôles FIT/CHECK, matrice et empreintes sont dans COMPLETION/SOURCE_TRACING.json.

Trois points bien répartis servent à l'alignement ; quatre sont réservés au contrôle. L'écart de correspondance moyen0,107pixel, maximum0,150, ne mesure **pas** l'erreur absolue de la projection du jeu. La projection R5 reste inchangée et aucune ville n'est qualifiée de position native certifiée.

La règle d'attribution mesure225 points de couverture par cellule avec une majorité de50%, uniquement sur la terre MEC existante. Deux cellules projetées sur la mer restent intactes. Le relevé de la carte source et son adaptation géographique sont attribués à Fenn-O-maniC sous CC BY-SA3.0 ; la licence du relevé dérivé est [CC BY-SA3.0](https://creativecommons.org/licenses/by-sa/3.0/). Aucune copie du SVG n'est utilisée comme texture du jeu. Les coordonnées et la subdivision discrète des pixels sont documentées comme une généralisation de gameplay.
