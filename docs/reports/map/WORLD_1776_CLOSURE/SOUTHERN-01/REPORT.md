# SOUTHERN-01 — Afrique australe au 1er janvier 1776

**Installation du 28 octobre 2026, livraison vérifiée le 29 octobre 2026 — IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Consigne directe : «tu peux passé à l'afrique austral». Passe cartographique et initialisation nécessaire ; aucun nouveau personnage, flavor, recette ou raffinement des bâtiments. Test africain groupé, sans demande intermédiaire.

## Corrections installées

**126 provinces natives réattribuées dans 4 régions moteur**, sans nouveau RGB ni pixel redessiné. Détail intégral : PLAN.json et GEOGRAPHIC_CROSSWALK.json ; illustrations BEFORE.png et AFTER.png. Les indices de travail sont ceux de GEOMETRY_CELLS.json, pas de nouveaux identifiants moteur.

- ORA/Orange et TRN/Transvaal cessent d'être des propriétaires initiaux : leurs territoires reviennent aux ensembles locaux sotho, tswana et du Haut-Veld.
- PHL/Philippolis et WBL/Waterboer cessent d'être des États initiaux. Un agrégat autonome des **communautés de l'Orange** (KQO) distingue les pouvoirs locaux de ces formations ultérieures.
- Les 22 cellules tswana du Natal passent aux **chefferies nguni** (NST). Aucun empire de Shaka n'est installé.
- 38 cellules du Karoo passent de TSW aux communautés SAN ; deux cellules riveraines supplémentaires passent à KQO. Les 18 cellules tswana au nord du secteur NorthernCape sont conservées.
- Les **chefferies du Haut-Veld** HVD reçoivent les 11 cellules de TRN et 21 de l'enveloppe MTB. MTB conserve 7 cellules du secteur Pretoria/Wonderboom, devient explicitement un agrégat ndébélé et a désormais une capitale dans TRANSVAAL. La culture nationale shona de ce proxy est retirée ; aucune culture de POP n'est convertie.
- BST représente des **chefferies sotho autonomes**, et non un État national de Moshoeshoe anticipé. SWZ conserve son noyau politique sous le nom **Ngwane**.
- MSH représente le pouvoir royal **Rozvi**, avec un lien tributaire vers MNC/Manyika ; Mutapa reste distinct. Ses 60 RGB ne changent pas de propriétaire. L'enveloppe large inclut des marges et des autorités tributaires : elle n'est pas une certification d'administration directe uniforme.

**Cap/VOC :** les 48 cellules DEI de CAPE_COLONY/EASTERN_CAPE sont conservées. La progression des fermes et la juridiction effective ne sont pas synonymes ; les sources ne justifient pas une nouvelle ligne cadastrale automatique. DEI reste le proxy politique VOC avec ses autres possessions ; aucun redécoupage de Java ou changement de souveraineté néerlandaise.

Les frontières Xhosa/Rharhabe/Gcaleka ne sont pas artificiellement alignées sur le Kei en1776 : Peires2012 montre des implantations et une chronologie plus mobiles. Thembu/Mpondo, Venda/Pedi, nord du noyau Ngwane, Chobe/Luyana et subdivisions namibiennes restent des limites à préciser, sans nouveaux partages conjecturaux. Cela interdit une clôture exhaustive de P3-08.

## Population

Monde courant : **837 328 654 → 837 328 654**, delta **0**. La baseline capturée dès le début vaut déjà837 328 654, soit 115 de plus que le précédent reçu Madagascar ; cet écart est antérieur à cette passe, non attribué ici et non compensé. Aucune variation mondiale n'est produite par SOUTHERN-01.

| Région moteur | Avant | Après |
|---|---:|---:|
| STATE_NORTHERN_CAPE | 264 144 | 264 144 |
| STATE_TRANSVAAL | 790 904 | 790 904 |
| STATE_VRYSTAAT | 95 504 | 95 504 |
| STATE_ZULULAND | 385 302 | 385 302 |

| Pays ou agrégat | Avant | Après |
|---|---:|---:|
| BST | 126 990 | 148 497 |
| HVD | 0 | 273 579 |
| KQO | 0 | 96 209 |
| MSH | 188 000 | 188 000 |
| MTB | 289 332 | 72 333 |
| NST | 0 | 283 786 |
| ORA | 40 627 | 0 |
| PHL | 29 403 | 0 |
| SAN | 34 780 | 161 033 |
| SWZ | 60 532 | 60 532 |
| TRN | 56 580 | 0 |
| TSW | 544 170 | 146 605 |
| WBL | 60 160 | 0 |

Toutes les cohortes culturelles/religieuses/serviles sont conservées. La ventilation par nombre de provinces natives, avec restes entiers conservatifs, est technique ; elle n'est pas un recensement de1776. Des populations boers/griqua héritées subsistent dans les pools : aucun peuplement de1776 de ces proportions n'est attesté par ce transfert. Pas d'assimilation ni de compensation démographique cachée.

## Institutions, technologies et armées

**3 TAG nouveaux** NST/HVD/KQO et 4 profils existants ajustés : MSH, BST, MTB, SWZ. Agrégats autonomes en catégorie décentralisée ; pouvoir royal rozvi et noyau ngwane non reconnus, avec monarchie. Catégorie décentralisée ne signifie pas absence de chefs, de rois locaux ou d'organisation. Les cours précises ne sont pas inventées. Les modèles natifs1836 de personnages BST/MTB sont neutralisés ; NgwaneIII déjà présent est conservé. Les demandes initiales du journal ultérieur du Haut-Veld de BST/SWZ sont retirées dans leurs seules histoires.

Connaissances anciennes conservées, explicitement résolues pour les4profils réinitialisés. Ajouts ciblés : international_relations pour MSH/SWZ ; organized_military_establishments pour MSH et, après contrôle des casernes héritées, HVD/KQO/BST/TSW. Les premières capacités représentent échanges et cadres armés locaux, pas une industrie d'armement. Les autres nouveautés ont leurs profils agricoles, pastoraux et artisanaux motivés dans COUNTRY_PROFILES.json.

Le premier contrôle de compatibilité a détecté les casernes conservées sans leur gate chez 4 destinataires. COMPATIBILITY_REPAIR.json trace la correction ; COMPATIBILITY_REPAIR_R2.json retire un grant NST involontaire issu d'une liste de capacités partagée dans l'outil. Les échecs et le premier contrôle statique sont archivés, pas présentés comme résultats finaux. **3 profils nouveaux PASS_STATIC_ONLY, aucune connaissance antérieure retirée et aucun nouveau P0/P1 sur 16 témoins.** Dettes techniques anciennes non masquées ; aucun graphe TECH ou recette commune modifié.

Niveaux des bâtiments, PM et pools mondiaux conservés. Un seul bataillon régulier irrégulier de WBL est retiré avec ce gouvernement territorial ultérieur ; aucun transfert artificiel vers un chef local. Toutes les autres unités explicites sont identiques et les appels de conscription MSH/MTB conservés. MILITARY_DELTA.json donne les comptes réels. Emploi, coûts, marchés, mobilisation et viabilité ne sont pas des observations moteur.

## Contrôles et concurrence

**202/202 contrôles statiques**, plus les vérifications finales de livraison dans DELIVERY_VALIDATION.json : propriétaires et unicité des RGB, conservation des cohortes/niveaux/PM, capitales, contiguïté des pouvoirs centralisés et voisinage centralisé de SWZ/MSH, technologies et fichiers témoins. Les agrégats tswana peuvent avoir plusieurs composantes : ce sont des communautés distinctes, pas une nouvelle enclave centralisée. Aucun corridor arbitraire créé.

**22 fichiers fonctionnels livrés : 10 existants ciblés, 12 ajouts.** Préimages immédiates et empreintes dans apply_inputs/, repair_inputs/ et FILES_DELIVERED.json. Hors nœuds autorisés, les fichiers partagés sont conservés. Madagascar, INTERIOR-01, autres passes WORLD, SERG, TECH/ECON et Amériques sont protégés ; aucun changement extérieur entre survey et installation. Pas d'écriture Git, vanilla, bitmap, terrain, ressource, hub/locator ou suiviSERG. Les anciens reçus restent historiques et ne sont pas rejoués comme des tests actuels.

Sources et limites : SOURCES.md, GEOGRAPHIC_LIMITATIONS.md. Les noms de hubs sont des repères natifs, certains ultérieurs ; leur présence ne prouve pas une souveraineté de1776. Drapeaux, capitales/hubs rendus, lois effectives, budgets, fronts et sauvegarde restent à observer au test africain groupé.

**WORLD :10/320(3,13%),0 validation humaine créditée.** Aucun critère entier gagné sur un noyau partiel. Prochaine action : contrôle cartographique africain groupé et reprise des seuls points concrets qui en résultent. Aucun autre continent ni lissage général lancé automatiquement.
