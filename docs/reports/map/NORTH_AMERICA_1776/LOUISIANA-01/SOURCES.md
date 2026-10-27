# LOUISIANA-01 — sources et portée, 27 octobre 2026

Date du scénario : **1er janvier 1776**. Les implantations sont sourcées ; les polygones de provinces et les corridors restent des arbitrages de représentation, pas des limites cadastrales.

## Recherches réutilisées

- `MAP1/MAP1_CASE_DOSSIERS/R8_NORTH_AMERICA_CARIBBEAN-0056.md`, notamment lignes 1–23 et 37–45 : Saint-Louis, Sainte-Geneviève et autorités autochtones du Missouri ; état initial `MAPPING_REQUIRED`, aucun RGB déjà homologué.
- Fiches R8-0008, R8-0055 et dossier `R8-CORRECTIONS-01` : absence de contrôle colonial uniforme ; Quapaws, Caddos, Osages ; postes espagnols laissés ouverts lors de la passe précédente.
- `GAMEPLAY_CONSTRAINTS.md` : concession explicite du joueur pour relier les postes par des cellules incorporées ; cette règle ne prouve pas une souveraineté continue historique.

## Documents consultés

1. **Library of Congress, Before Lewis & Clark**, section « Louisiana Purchase » et « Boundary between British and Spanish Territories », lignes 278–288 de la page consultée : succession de 1763, Mississippi comme limite impériale, Nouvelle-Orléans espagnole. La page présente la carte de John Ross, relevé de 1765 publié en 1772. Le texte et la notice ont été lus ; aucune superposition cadastrale de cette carte n'est revendiquée. [Page](https://loc.gov/exhibits/lewisandclark/lewis-before.html#28B).
2. **Missouri Secretary of State, Timeline 1673–1820**, lignes 128–141 : Saint-Louis 1764, Saint-Charles 1769, prise en charge espagnole en Haute-Louisiane en 1770. New Madrid 1789 et Cape Girardeau 1793 sont postérieurs au départ : les cellules de corridor proches de ces lieux ne sont pas des postes coloniaux nouvellement inventés. [Document](https://www.sos.mo.gov/archives/history/timeline/1).
3. **NPS, Ste. Geneviève Foundation Document**, lignes 139–150 : administration espagnole, population créole francophone, présence et influence autochtones persistantes. Les recensements de 1766/1776 ne couvrent pas toute la colonie et ne servent pas à certifier les chiffres conservés du mod. [Document](https://www.nps.gov/stge/learn/management/foundation-document.htm).
4. **NPS, The Arkansas Post Story**, appendice 2, version conservée par NPSHistory, lignes 49–60 : poste de 1756–1779 en aval du site actuel, proximité du Mississippi, relocalisation de 1779. La localisation a fait débat. Le point utilisé est une **zone approximative en province**, pas une identification archéologique du fort. [Document](https://www.npshistory.com/publications/arpo/history/app2.htm). Le site NPS courant confirme l'histoire générale et les déplacements : [History & Culture](https://www.nps.gov/arpo/learn/historyculture/index.htm).
5. **Cane River National Heritage Area, Historical Overview**, lignes 47–52 : établissements caddos, fondation de Natchitoches, voisinage de Los Adaes et échanges. Sert à conserver le poste et à rétablir un arrière-pays caddo régional, pas à certifier chacun des six RGB du nord-ouest. [Document](https://www.canerivernha.org/historical-overview).
6. **Louisiana State Museums, Gálvez on the Move**, passages de la campagne de septembre 1779, notamment lignes 324–331 : Baton Rouge, Manchac et Natchez sont encore britanniques avant leur conquête. Les trois cellules de la bande Baton Rouge–nord des lacs sont transférées à la Floride occidentale ; Natchez n'est pas prétendu corrigé dans cette passe. [Document](https://louisianastatemuseum.org/galvez-move).
7. **Texas State Historical Association, Boundaries**, lignes 8–9 : limite administrative de l'Arroyo Hondo et maintien de la distinction Texas/Louisiane sous la même couronne. Pas de revendication louisianaise ajoutée sur tout le Texas ; pas de projection du règlement de 1819 sur 1776. [Document](https://www.tshaonline.org/handbook/entries/boundaries).

Les essais LOC « Louisiana as a Spanish Colony » et « A Question of Boundaries », déjà cités par les anciens dossiers, ont renvoyé 403 à l'ouverture. Leurs extraits indexés ont été examinés comme compléments ; ils ne sont pas présentés comme des pages intégralement accessibles. Le second souligne justement l'imprécision des limites occidentales : [notice](https://www.loc.gov/collections/louisiana-european-explorations-and-the-louisiana-purchase/articles-and-essays/a-question-of-boundaries/).

## Géométrie et décisions

Réutilisation de `R8-CORRECTIONS-01/GEODETIC_MODEL.json`, modèle régional empirique issu de hubs natifs contrôlés. Les coordonnées de lieux contemporains servent à repérer les zones, pas à démontrer une possession. Les sites et RGB réellement échantillonnés figurent dans `PLAN.json`. Nouvelle-Orléans reprend le port natif vérifié, préférable au décalage local de projection ; Saint-Louis garde son hub natif.

Les corridors sont construits avec des adjacences par côtés, contrôlées contre les passages interdits natifs, puis vérifiés par des chemins de pixels. Une cellule de rive supplémentaire, `xBA821E`, évite d'enfermer une poche quapaw derrière le corridor : concession de jouabilité documentée séparément. Les Caddos restent un regroupement régional existant, sans nouvelle prétention à un découpage de chaque communauté.

## Revendications : portée et limites

Les claims sont portés par **State Region**, pas par province. Arkansas, Missouri, Iowa, Nebraska, Kansas et le bassin des plaines reçoivent une priorité louisianaise ; les claims USA systématiques situés à l'ouest du Mississippi sont retirés. Les limites des montagnes et des sources du Mississippi ne sont pas définies par une frontière précise de 1819. Montana, Wyoming, Colorado et Minnesota comprennent des morceaux extérieurs au bassin : les claims entiers sont une approximation technique publiée, **pas une certification de leur contour moderne**.

Le double claim Louisiane/Nouvelle-Espagne du Colorado est conservé comme réserve des deux domaines dans une région mixte. Il ne signifie pas que tout le Colorado était un contentieux frontalier établi en 1776. Le Texas et le Nouveau-Mexique restent dans le domaine de revendication de la Nouvelle-Espagne. Les claims LOU/SC1 du Mississippi oriental sont retirés ; le domaine britannique et les droits autochtones ne sont pas assimilés à des possessions louisianaises.

Le texte moteur local `localization/english/interfaces_l_english.yml:7937` confirme qu'un claim étranger entretenu par un intérêt peut empêcher une colonisation. L'effet exact des doubles claims, des intérêts et des décisions ultérieures reste à tester dans le moteur. Aucun verrou universel permanent sur la colonisation n'a été créé.

## ColGrep

Un seul appel tenté à `C:/Users/simeo/.cargo/bin/colgrep.exe --agent`, question de localisation des dossiers et définitions de Louisiane, chemin `.`. Échec immédiat sur la création du verrou de l'index dans AppData : accès refusé. Durée observée : **1,099 seconde**. Aucun résultat de recherche et **aucune exécution du modèle 2B attestée** pour cette passe. Repli sur `rg` et lecture ciblée, sans changement d'intégration ni reconstruction d'index. Aucune économie de quota mesurable ou revendiquée.
