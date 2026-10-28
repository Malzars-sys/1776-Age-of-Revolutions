# HORN-01 — Empire éthiopien et Corne de l'Afrique

27 octobre 2026. Date cible : **1er janvier 1776**. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Passe cartographique autorisée après [SAHEL-GEOCHECK-01](../SAHEL-GEOCHECK-01/REPORT.md). Le joueur reporte la finition des courbes et autorise les vassalités/autonomies nécessaires. Aucun nouveau test moteur de cette version, aucune attestation humaine inventée.

## Résultat territorial

- ETH conserve la cour impériale et son noyau de Gondar/Begemder autour du lac Tana. TGR (Tigré), GJM (Godjam) et WLO (Wollo/Lasta agrégé) deviennent des pouvoirs provinciaux autonomes **tributaires** de la couronne. Ce lien moteur représente l'appartenance impériale nominale, pas une administration uniforme ou un tribut exactement quantifié dans une archive. L'hégémonie Yejju de 1786 n'est pas préinstallée.
- SHW retrouve le noyau Choa/Ankober-Menz-Yifat, sans les conquêtes du XIXe siècle. HAR (Harar/Charcar), AWS (Awsa et basse vallée de l'Awash), KFA (Kaffa), WLT (Wolayta) et YJR (Yem/Janjero) sont distincts et indépendants. Les îlots de domination impériale prématurée au sud sont supprimés. Aucun souverain exact de janvier reconstitué pour du flavor.
- Le noyau haut-plateau d'Asmara/Hamasien-Seraye rejoint TGR. Les ports ottomans dont Massawa restent TUR ; les communautés de l'Ouest/Bedja (BJA) et afar côtières et désertiques (AFR) sont distinguées. AFR est **un agrégat de pouvoirs locaux**, dont une portion septentrionale séparée, pas un grand royaume afar unique annexé à Awsa. Ni Djibouti français ni Érythrée coloniale créés.
- Les communautés de Wallaga/Gibe (WLG), Oromo de l'Est (ARS), Borana/Guji (BRN), Hadiya/Kambata (HDY), Omo (OMO) et communautés somalies (OGD) restent autonomes sous agrégats décentralisés. Ces étiquettes ne signifient ni absence d'institutions ni population ethniquement homogène. Pas de royaumes de Jimma, Leqa-Naqamte ou Limmu-Enarya du XIXe siècle préinstallés.
- HRI représente l'enveloppe confédérale hiraab et Mogadishu, distincte du noyau riverain Geledi GLD conservé à l'intérieur. L'extension prématurée du MJT dans le centre côtier/Hobyo est retirée ; noyaux nord-est MJT, Warsangali WSG et Isaaq ISQ préservés. La double occurrence MJT de x2D75F4 est supprimée. Aucun sultanat ultérieur de Hobyo créé, aucune annexion omanaise directe déduite de relations commerciales.

**280 provinces natives réattribuées, 27 groupes de transfert ; un doublon interne résolu. Aucun nouveau RGB, aucun pixel, terrain, ressource ou hub modifié.** Énumération et motifs : [PLAN.json](PLAN.json), [GEOGRAPHIC_CROSSWALK.json](GEOGRAPHIC_CROSSWALK.json). Les indices de la carte d'inspection sont des repères, les RGB sont canoniques. Cartes : [avant](BEFORE.png), [après](AFTER.png). Courbes et angles non lissés, conformément au report demandé.

## Initialisation minimale et compatibilité

3 nouveaux TAG (AFR/HRI/YJR), 15 TAG natifs activés. Les capitales régionales sont adaptées aux portions réellement possédées, notamment TGR/GJM/WLO vers GONDER. Monarchie/oligarchie est une approximation des cours et notables ; trois liens tributaires seulement. Aucune monarchie future attribuée aux communautés Gadaa. Les anciennes définitions culturelles/religieuses sont conservées sauf changements explicites de type et religions de certains agrégats ; elles restent des proxies de catalogue, **pas un audit ethnographique certifié**. Harari, Yem ou certaines langues omotiques n'ont pas d'identifiant propre : cette limite n'autorise pas à convertir les cohortes POP.

| TAG | Type moteur | Technologies minimales | Capitale régionale |
|---|---|---:|---|
| TGR | unrecognized | 7 | GONDER |
| GJM | unrecognized | 7 | GONDER |
| WLO | unrecognized | 6 | GONDER |
| SHW | unrecognized | 7 | OROMIA |
| KFA | unrecognized | 7 | AMHARA |
| WLT | unrecognized | 7 | AMHARA |
| AWS | unrecognized | 6 | GONDER |
| HAR | unrecognized | 7 | OROMIA |
| YJR | unrecognized | 7 | AMHARA |
| HRI | unrecognized | 7 | SOMALILAND |
| WLG | decentralized | 4 | AMHARA |
| ARS | decentralized | 4 | OROMIA |
| BRN | decentralized | 4 | AMHARA |
| OMO | decentralized | 4 | AMHARA |
| BJA | decentralized | 4 | ERITREA |
| OGD | decentralized | 4 | OROMIA |
| AFR | decentralized | 5 | ERITREA |
| HDY | decentralized | 4 | AMHARA |

Les connaissances sont des profils minimaux explicitement justifiés dans [COUNTRY_PROFILES.json](COUNTRY_PROFILES.json), 4 à 7 par pays : agriculture, élevage, ateliers/alimentation, textile, échanges et organisation militaire traditionnelle selon la société. Ce n'est pas une certification exhaustive de tout le savoir local. Pas de paquet technologique par âge. Une variante privée de coutumes commerciales reprend les coefficients du mercantilisme et sa gate locale d'échanges ; aucune assurance maritime ou autre technologie ajoutée pour masquer un défaut de loi.

Les 18 contrats statiques passent sans constat. Sur neuf pays existants, aucun nouveau P0/P1 ; dettes techniques héritées conservées : [STARTING_TECH_NEW_COUNTRIES.json](STARTING_TECH_NEW_COUNTRIES.json), [TECH_NON_REGRESSION.json](TECH_NON_REGRESSION.json). Aucun graphe TECH-R1/R2/R3, recette ECON-ALLOYS/quincaillerie ou PM commun retouché.

Sept fichiers de personnages natifs 1836 sont neutralisés par surcharge homonyme pour les TAG réactivés ; **aucun nouveau personnage**. L'empereur et le général ETH déjà présents sont conservés. Les références des 4 dragons, 12 irréguliers et 23 conscrits ETH recrutés dans AMHARA passent à GONDER, seule correction nécessaire à la perte de cette portion ; les 25 conscrits GONDER antérieurs restent identiques. Types, comptes, services et formations conservés. Les administrations impériales existantes d'AMHARA sont replacées à la cour de GONDER, à niveaux et PM strictement constants ; autres installations et recettes conservées dans leurs nouvelles portions. Aucun raffinement de bâtiments ou nouvelle troupe.

## Population

**837,328,539 → 837,328,539, delta 0.** Chacune des cinq régions conserve son total ; chaque cohorte conserve ses attributs culturels, religieux et serviles. Partage technique par provinces uniques de chaque portion source, avec restes entiers : **pas un recensement ni une estimation de densité historique**. Le poids du doublon MJT est exclu. Les zéros initiaux désignent des TAG inactifs, pas des terres historiquement vides.

| TAG | Avant | Après |
|---|---:|---:|
| AFR | 0 | 123 102 |
| ARS | 0 | 438 802 |
| AWS | 0 | 208 569 |
| BJA | 0 | 71 771 |
| BRN | 0 | 393 716 |
| ETH | 6 614 938 | 871 059 |
| GJM | 0 | 358 672 |
| GLD | 208 943 | 36 338 |
| HAR | 0 | 109 700 |
| HDY | 0 | 98 429 |
| HRI | 0 | 299 134 |
| KFA | 0 | 131 241 |
| MJT | 341 634 | 78 838 |
| OGD | 0 | 904 173 |
| OMO | 0 | 459 337 |
| SD1 | 1 174 109 | 1 039 539 |
| SHW | 0 | 127 983 |
| TGR | 0 | 822 411 |
| WLG | 0 | 1 057 566 |
| WLO | 0 | 512 388 |
| WLT | 0 | 131 237 |
| YJR | 0 | 65 619 |

[POPULATION_BEFORE_AFTER.csv](POPULATION_BEFORE_AFTER.csv) et [POPULATION_LEDGER.json](POPULATION_LEDGER.json). Ressources/hubs partagés, choix implicites de PM, emplois, budgets et rendu des capitales/flags ne sont pas prouvés par ces totaux.

## Sources, portée et incertitudes

[SOURCES.md](SOURCES.md) distingue sources lues, cartes vues et références seulement consultées en extrait. La carte Bahru c.1800 fournit les voisinages et localités ; elle n'est pas un contour de 1776 à recopier. Les cartes Haberland c.1500/c.1700 ne prouvent pas une possession de 1776. Aucun partage automatisé par distance à une capitale, aucune frontière rectangulaire générée.

Les pouvoirs provinciaux de l'ère des Princes, limites Semien/Tigré/Wollo, confins bas-pays de Wallaga, emprises de Kaffa/Yem/Wolayta, contacts oromo-somalis et ressorts afar restent approximatifs. Les affiliations de clans varient ; HRI n'est pas une administration centralisée de tous les villages de la côte. **Merca/Barawe et les autres pouvoirs locaux du Benaadir méridional restent agrégés aux communautés locales : leurs emprises urbaines séparées ne sont pas certifiées ici.** OGD est nommé « Communautés somalies » et ne prétend pas que toute la côte de la Jubba appartient au seul groupe ogaden. Le proxy Afgooye est la portion riveraine voisine du RGB partagé du site natif de Mogadishu ; il ne certifie pas la limite urbaine entre les deux villes. Ces limites empêchent une clôture régionale complète.

Le doublon MJT est résolu ; les deux conflits hérités de KENYA x9A78B7 / x5C1ADA restent explicitement **hors de ces cinq nœuds**, pour le lot côtier/oriental suivant. Aucun arbitrage de ces cellules sans rapprochement historique. La finition esthétique du Sahel et des frontières américaines est différée par le joueur, sans écrire dans les lots américains ou SERG.

## Contrôles, concurrence et suite

**458/458 contrôles territoriaux statiques**, 18 profils compatibles, contrôle de livraison/localisation séparé dans DELIVERY_VALIDATION.json. Commandes : `world1776_horn01.py --preflight`, `--apply --tech --validate`, puis `--validate` après corrections bornées. Premier contrôle archivé : 445/458, treize retours à la ligne hors nœud corrigés sans changement sémantique ; nouvelle allocation POP par provinces uniques et libellés pluriels documentés dans leurs reçus. Les vérifications finales portent sur la version effectivement livrée.

38 fichiers fonctionnels : 20 fichiers existants ciblés, 18 nouveaux. [FILES_DELIVERED.json](FILES_DELIVERED.json), [DELIVERY_MANIFEST.json](DELIVERY_MANIFEST.json). Comparaison des blocs extérieurs et empreintes des autres fichiers : [CONCURRENT_CHANGES.json](CONCURRENT_CHANGES.json). SAHEL-01/02-05/06-07, Maghreb, Balkans, Siwa/Fezzan/Gibraltar, SERG, TECH/ECON et versions américaines courantes préservés. Aucun retour à une ancienne baseline, aucune écriture Git/vanilla/SERG.

Test de cette version **NOT_RUN** ; protocole [GROUPED_RUNTIME_ITEMS.md](GROUPED_RUNTIME_ITEMS.md), aucun test intermédiaire demandé. Le retour joueur sur la présence du lot Tchad/Nil ne valide pas HORN-01. WORLD **10/320 (3,13 %)** inchangé, aucun crédit pour régions partielles. Suite déjà autorisée : Congo/Kongo et Angola, puis possessions portugaises et Afrique australe/VOC, en lots distincts ; la finition des courbes reste une passe ultérieure.
