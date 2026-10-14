# MAP2L — Rework territorial du Saint-Empire, 1er janvier 1776

## Choix confirmés par l’utilisateur

- Saint-Empire uniquement, pas de reprise de toute la carte mondiale.
- Redessiner les provinces pour représenter davantage de petits États et d’enclaves.
- Garder les proportions : les micro-enclaves trop petites sont abstraites dans un territoire voisin, jamais artificiellement agrandies.
- Inclure les territoires impériaux de l’actuelle Belgique dans cette passe.

Le périmètre belge n’est pas celui d’un État belge indépendant en 1776. Il faut distinguer les Pays-Bas autrichiens des principautés impériales autonomes, notamment Liège et Stavelot-Malmedy. Bouillon, les enclaves françaises et les frontières contestées doivent être examinés séparément, sans conclusion tirée des frontières contemporaines.

## État réel du travail

La sauvegarde initiale `BASELINE.json` et `SOURCE/provinces_before.png` est immuable. Les confirmations de périmètre sont consignées ici, sans réécrire cette sauvegarde.

Le 13 octobre 2026, le premier lot belge a été appliqué aux fichiers du mod : Liège (`LGE`) et Stavelot-Malmedy (`STM`), 37 nouvelles identités de provinces, frontières locales redessinées, démographie et bâtiments répartis à totaux conservés, intégration au bloc et au registre impérial. Le résultat est une approximation à la résolution du jeu, pas une reconstruction cadastrale. Voir `BELGIUM/VALIDATION.json` et `BELGIUM/IMPLEMENTATION.md` pour les vérifications et limites.

Une extension politique distincte, autorisée ensuite le même jour, ajoute le Piémont-Sardaigne (`SAR`) au bloc impérial, mais uniquement ses neuf provinces de `STATE_PIEDMONT` au registre de jure. Le registre actif compte maintenant 324 RGB ; les 315 précédents sont conservés. L'île de Sardaigne et les autres possessions de SAR restent hors de cette extension territoriale. La carte principale et celle du journal ont été mises à jour. Voir `PIEDMONT/REPORT.md` et `PIEDMONT/VALIDATION.json`.

Le lot principal de Franconie a ensuite été appliqué : Ansbach-Bayreuth (`ANS`), Bamberg (`FBM`), Würzburg (`WZB`), Nuremberg (`NUR`), un fragment septentrional d'Eichstätt (`EIC`) et un fragment attribué au Cobourg existant (`COB`). Les huit provinces natives de `STATE_FRANCONIA` deviennent 43 identités RGB, dont 35 nouvelles. Le registre actif atteint 359 RGB, sans changement de l'étendue jaune dans cette région. Voir `FRANCONIA/REPORT.md` et `FRANCONIA/VALIDATION.json`.

Ce lot est une approximation documentée à la résolution du jeu, pas une résolution de toutes les souverainetés franconiennes : 662 pixels sur 1 984 restent provisoirement à BAV, avec le statut explicite de frange non résolue. Les autres territoires détaillés de l'Empire ne sont pas encore achevés. Les fichiers `GEOMETRY/*_before.png` représentent toujours la sauvegarde initiale ; les sources de recherche ne sont pas des assets runtime. Le chargement de ce nouveau lot dans le moteur reste à tester.

Le registre impérial initial contenait déjà les quatorze provinces natives de Flandre et de Wallonie, toutes affectées à `BEO`, qui représente les Pays-Bas autrichiens dans le mod. Leur présence dans la carte jaune ne résolvait pas leur souveraineté locale. Ce registre MAP2K reste immuable ; le lot belge a porté le registre actif versionné `IMPERIAL_DE_JURE_REGISTRY.json` de MAP2L à 315 identités impériales, dont les descendants des provinces belges, avec leurs nouveaux titulaires, sans changer l'étendue géographique jaune. L'extension piémontaise ultérieure le porte à 324 identités et ajoute exactement les neuf polygones approuvés au masque jaune.

## Ordre de travail territorial

1. Lots appliqués : Belgique (Liège et Stavelot-Malmedy), extension piémontaise, puis principales enveloppes franconiennes. Leurs limites ouvertes restent consignées dans les rapports de chaque lot.
2. Prochain lot retenu : Rhin central, Mayence et Palatinat d'abord, avec examen du raccord occidental de la Franconie et des possessions autour d'Aschaffenburg. Choix de priorité seulement : aucun découpage de ce lot n'a encore été appliqué.
3. Puis extensions mosanes encore ouvertes, Cologne/Trèves, possessions prussiennes occidentales et Westphalie, Souabe et autres dossiers impériaux : ne pas considérer les électorats approximatifs de MAP2K comme des frontières historiques définitives. Le redécoupage prussien n'est pas abandonné, mais n'a pas été fait dans le lot franconien.

Pour chaque lot : bitmap candidat, identités de provinces et terrains, propriétaires, capitales, populations conservées, bâtiments et recrutements valides, intégration constitutionnelle, registre de jure et carte jaune, puis contrôles différentiels et essai dans le moteur.

Consigne de test du 13 octobre 2026 : le joueur ne lancera le jeu qu'après la fin de tous les lots du Saint-Empire. Les contrôles différentiels et statiques restent obligatoires après chaque lot ; le test moteur est reporté à la fin de l'ensemble et son absence doit rester explicite. La préparation du Rhin central (baseline post-Franconie et inspection des sources) est consignée dans `RHINE_CENTRAL/WORK.md` ; l'état actuel de son application figure ci-dessous.

Après cette préparation, un **premier sous-lot du Neckar** a été appliqué : noyau Heidelberg–Ladenburg à KPF et fragment de Viernheim à KMZ, quatre nouveaux RGB dans deux parents de `STATE_BADEN`. Le registre actif atteint 363 RGB, sans changement de l'étendue jaune. Les contrôles de conservation et non-régression passent ; le Rhin central reste partiel (Mayence/Rheingau, Aschaffenburg, Palatinat occidental, Mosbach et possessions éloignées encore ouverts). Voir `RHINE_CENTRAL/REPORT.md` et `RHINE_CENTRAL/UNRESOLVED.csv`.

## Sources et limites

- [BSB, carte détaillée de Franconie, Le Rouge](https://www.bavarikon.de/object/bav%3ABSB-MAP-00000BSB00090735?cq=&lang=en&p=1) : cataloguée 1743, publiée après 1764 ; la concordance avec 1776 reste à contrôler.
- [Stadtarchiv Nürnberg, Homann, A4/IV nº 74, hébergée par BR](https://www.br.de/br-fernsehen/sendungen/1806/circuli-franconiae-fraenkischer-reichskreis-100.html) : carte détaillée, date non précisée dans la notice consultée ; comparaison, pas visa chronologique automatique.
- [KBR, carte de cabinet de Ferraris](https://opac.kbr.be/BIBFEDERALE/doc/SYRACUSE/16992733/carte-de-cabinet-des-pays-bas-autrichiens-levee-a-l-initiative-du-comte-de-ferraris?_lg=fr-BE) : relevés et planches de 1771–1778, à examiner pour la situation de 1776.
- [SPW, Ferraris géoréférencé](https://geoportail.wallonie.be/catalogue/b8b9e555-a4d1-49bf-940d-31bbbf7613fc.html) : aide au calage ; lacunes dans Bouillon et certaines enclaves françaises. La carte topographique n’arbitre pas à elle seule les droits contestés.

La carte générale moderne de 1789 et Cliopatria regroupent une partie des petits territoires. Elles ne suffisent pas pour dessiner leurs frontières individuelles. Aucun découpage par proximité du nom d’une ville ne sera présenté comme une frontière historique.
