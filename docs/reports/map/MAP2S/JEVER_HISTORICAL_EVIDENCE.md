# Jever — preuves acquises et géométrie manquante

## Corpus ciblé, pas de reprise générale

- [NLA OL Best90](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails?fondsId=2640) : autorité d’Anhalt-Zerbst1667–1793 et fonds de l’administration de Jever. Forte preuve de souveraineté, pas un contour raster.
- [Archives urbaines Dep25JEV](https://www.arcinsys.niedersachsen.de/arcinsys/showFondsDetails.action?fondsId=2873&request_locale=en) : portée urbaine à distinguer de toute la seigneurie.
- [Schlossmuseum Jever, cartes et plans](https://www.schlossmuseum.de/sammlungen/virtuelle-sammlungen/regionalgeschichte/landkarten-und-plaene/) : Königshaven vers1725 Ka92 ; limite Wittmund–Jever1745/46 Ka226 ; Kunstenbach1798 Ka94. Six reproductions avec empreintes dans MAP_SOURCES.json. La carte1798 montre une souveraineté russe postérieure, pas celle1776.
- Coldewey/Homann1730 déjà conservée dans MAP2P/COLDEWEY_1730.png et sa provenance : grandes distinctions Jever/Kniphausen/Oldenburg, pas de transformation locale indépendante validée.
- MAP2R/JEVER_AUDIT.md, MAP2O/JEVER_VAREL_KNIPHAUSEN_AUDIT.md et MAP2P : exclusions déjà établies, réutilisées sans écraser leurs baselines.
- [NLA, catalogue Jever](https://www.arcinsys.niedersachsen.de/arcinsys/list.action?nodeid=g182576&page=1) : Siebeck1777 Best298Z31 identifié au catalogue. Notice seule, image non obtenue, aucune frontière extraite.

## Localisation et juridictions

Jever est dans l’ensemble côtier Jeverland, à l’ouest de la Jade et au nord d’Oldenburg. Les cartes distinguent Wangerland, Östringen et les secteurs de Rüstringen ; Kniphausen reste distincte. Les droits Bentinck et Varel ne deviennent pas automatiquement des possessions de Zerbst. Wangerooge est un problème séparé de correspondance insulaire. Ni Wilhelmshaven1853, ni la Russie1793, ni l’intégration à Oldenburg1818 ne sont rétroprojetées.

Le bitmap8192×3616 contient les grandes enveloppes OLD xECC3B4 (184 cellules) et xC00161 (229), STATE_HANNOVER69. Leurs bornes et les trois fragments OLD plus méridionaux sont relevés dans le CSV. Ce sont des transporteurs techniques d’investigation et non des provinces historiques de Jever. Aucun pixel unique de centre urbain de Jever n’est certifié. La position d’un bâtiment ou un profil baltique/thuringien hors domaine n’a pas été employé.

Le seul locator inventorié dans la fenêtre locale est le port de STATE_ELBE58, en RGB BRE x68BE66, X4286.373535/Y742.575195. Ce locator n’est ni un port de Jever ni une preuve de sa frontière. Aucun hub/locator n’est déplacé. OLD conserve146803 habitants de sa subdivision économique69 ; AZR conserve30687 dans son noyau62. Ces chiffres sont techniques, pas la population historique de Jever.

## Pourquoi C et non B

Une généralisation B est autorisée par le prompt, mais doit rester fondée sur une juridiction identifiable dans le raster. Les images obtenues sont petites (420×500,375×528 et813×500 pour les trois vues complètes) ; la limite sud et l’exclusion Kniphausen ne peuvent pas être transposées de manière vérifiable. Le littoral natif schématise la Jade et les terres endiguées. Aucun jeu de repères homologues indépendant n’est présent. Déplacer sept pixels, couper une moitié ou prendre un petit noyau nord-ouest donnerait une règle numérique sans preuve supplémentaire. Cela resterait C, même avec un tracé visuellement propre.

## Arbitrage opérationnel

Conserver les transporteurs OLD pour cette passe. Reprendre seulement avec une image lisible de Ka92 / Siebeck1777 / Ka94, une comparaison de la frontière avec la pièce1745/46, et des repères physiques locaux explicitement identifiés côté source et bitmap. Délimiter alors un noyau généralisé en excluant Varel/Kniphausen, mesurer l’incertitude sans prétention cadastrale, puis créer une possession éloignée directe AZR sans corridor ni pays indépendant.

Il faut ensuite répartir la démographie par un périmètre comparable : donnée historique datée si disponible, sinon redistribution déterministe. Tester marché, capacité portuaire réelle et accès maritime sans créer artificiellement des bâtiments. Aucun correctif géométrique n’est implicitement autorisé par ce rapport.
