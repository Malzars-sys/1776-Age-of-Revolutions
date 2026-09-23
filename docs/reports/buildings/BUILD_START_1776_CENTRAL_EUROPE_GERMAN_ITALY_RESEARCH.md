# BUILD START 1776 — Europe centrale, monde germanique et Italie

**Date absolue : 1776-01-01. Recherche uniquement. Aucun fichier gameplay modifié.**

## 1. Périmètre et discipline technique

- Instances Owner_TAG + State_ID dans le périmètre historique : **81**.
- Instances actives après exclusion intégrale de VEN/GEN : **73**.
- Instances Sérénissime ignorées : **8**.
- L’unité de recherche est toujours `Owner_TAG + State_ID`; aucune ligne de State_ID partagé n’est fusionnée.
- Le catalogue positif utilisé comprend les statuts `YES`, `YES_TECH_DISTRIBUTION_REVIEW`, `YES_ROADS_CANALS_ONLY_NO_RAIL` et `YES_CASE_BY_CASE_TRADE_SEED`; tous les `NO_AUTO_GENERATED`, `NO_POST_1776` et systèmes spéciaux sont exclus.
- `building_railway` représente uniquement la capacité routière/canaux au départ; toutes les lignes gardent `pm_no_rail_network`.

## 2. Méthode

Les niveaux sont attribués uniquement lorsqu’un secteur organisé, durable et significatif est attesté. Les activités domestiques ou artisanales isolées restent abstraites. Les centres de commerce sont traités séparément et de façon conservatrice. Les technologies ne servent jamais de preuve historique : si le bâtiment est justifié mais que son gate technologique n’est pas actuellement présent, `Tech_Distribution_Review = YES`.

## 3. Diagnostic régional

- **Allemagne centrale et orientale** : très forte asymétrie entre Saxe/Silésie (textile, mines), Prusse administrative et militaire, ports hanséatiques et petits territoires.
- **Habsbourg** : pôles distincts — Vienne administrative, Bohême verrière et manufacturière, Moravie textile émergente, Styrie minière, Tyrol salin, Lombardie soyeuse, Trieste entrepôt maritime.
- **Suisse** : puissance manufacturière textile sans équivalent proportionnel à sa taille politique; East Switzerland reçoit donc un niveau textile élevé.
- **Italie** : fortes spécialisations : soie piémontaise/lombarde, Livourne et Ancone comme ports francs, Naples comme complexe naval/militaire, Sicile céréalière; aucune homogénéisation par « niveau italien ».

## 4. Centres de commerce proposés

- **AUS / STATE_AUSTRIA — Austria** : level 2 (HIGH) — Vienna functioned as the political and consumption center of the monarchy and a major redistribution market.
- **AUS / STATE_LOMBARDY — Lombardy** : level 2 (HIGH) — Milan was a major regional commercial and financial center tied to the silk economy.
- **AUS / STATE_SLOVENIA — Slovenia** : level 3 (HIGH) — Trieste’s free-port regime, merchant immigration, exchange institutions and long-distance trade make it a clear international entrepôt.
- **BAV / STATE_FRANCONIA — Franconia** : level 1 (LOW) — Nuremberg/Franconia remained a regional commercial and craft redistribution center, though below Frankfurt/Leipzig/Hamburg scale.
- **BRE / STATE_ELBE — Elbe** : level 1 (MEDIUM) — Bremen was a merchant city with established long-distance trade, but its eighteenth-century port access was constrained by Weser silting.
- **FRM / STATE_HESSE — Hesse** : level 2 (HIGH) — Frankfurt’s twice-yearly fairs had centuries of international significance and made the city a major German marketplace.
- **GR3 / STATE_SICILY — Sicily** : level 2 (MEDIUM) — Sicily’s export economy required major merchant/redistribution centers at Palermo and Messina.
- **HAM / STATE_ELBE — Elbe** : level 3 (HIGH) — Foreign trade dominated Hamburg’s economy; merchants connected inland Germany with Atlantic and European markets.
- **LUB / STATE_SCHLESWIG_HOLSTEIN — Schleswig-Holstein** : level 1 (MEDIUM) — Lübeck retained a regional Baltic redistribution role.
- **PAP / STATE_ROMAGNA — Romagna** : level 2 (HIGH) — Ancona’s free-port privileges attracted merchant houses, Levantine and western traders and transit cargoes from distant markets.
- **PRU / STATE_BRANDENBURG — Brandenburg** : level 1 (MEDIUM) — Berlin was the central consumption and redistribution market of Prussia, but not an international entrepôt on Hamburg’s scale.
- **PRU / STATE_EAST_PRUSSIA — East Prussia** : level 1 (MEDIUM) — Königsberg was a Baltic redistribution and export center for the East Prussian hinterland.
- **PRU / STATE_POMERANIA — Pomerania** : level 1 (HIGH) — Stettin handled overseas imports and redistribution into the Prussian hinterland, but merchants still judged Hamburg superior.
- **SAR / STATE_PIEDMONT — Piedmont** : level 1 (MEDIUM) — Turin was the central market and administrative-commercial node of Piedmont, but not an international entrepôt like Livorno or Trieste.
- **SAX / STATE_SAXONY — Saxony** : level 2 (HIGH) — Leipzig’s fairs were a longstanding supra-regional commercial hub connecting central/eastern European trade.
- **SIC / STATE_CAMPANIA — Campania** : level 2 (HIGH) — Naples was the kingdom’s dominant urban market and a substantial Mediterranean commercial center, though not a free-port entrepôt on Livorno/Trieste scale.
- **SWI / STATE_EAST_SWITZERLAND — East Switzerland** : level 2 (HIGH) — Zurich and related merchant-manufacturer centers organized production, finance and export networks across the Rhine and into western Europe.
- **SWI / STATE_WEST_SWITZERLAND — West Switzerland** : level 1 (MEDIUM) — Western Swiss cities participated in long-distance textile/luxury-goods commerce; one level reflects a regional hub rather than a global entrepôt.
- **TUS / STATE_TUSCANY — Tuscany** : level 3 (HIGH) — Livorno’s free-depot system, foreign merchant colonies and re-export trade made it an international entrepôt.

## 5. Infrastructure régionale

Chaque ligne `building_railway` de la matrice contient séparément `ROAD_LEVEL_JUSTIFICATION` et `CANAL_LEVEL_JUSTIFICATION`. Aucun rail actif n’est proposé. Les cas de canal les plus solides sont Brandenburg (connexions Oder–Havel–Spree) et Lombardie (Navigli); Bologna/Trieste sont explicitement refusés comme réseaux de canaux régionaux malgré leurs ouvrages urbains.

## 6. Principaux pôles productifs

- **SAX / Saxony** : textile 3, mines métalliques 2, tooling 1, universités/academies 2, trade center Leipzig 2.
- **PRU / Lower & Upper Silesia** : textile 3/2; extraction lourde maintenue très prudente avant l’accélération post-1777.
- **AUS / Bohemia** : glassworks 3, textile 2; **Moravia** textile 2; **Lombardy** textile 3 + sericulture/rice; **Slovenia/Trieste** port 3 + trade center 3.
- **SWI / East Switzerland** : textile 4 en raison de la concentration proto-industrielle et exportatrice documentée.
- **HAM / Elbe** : port 3, trade 3, shipyards 2, food/refining 3.
- **SAR / Piedmont** : textile 3, sericulture 2; **TUS / Tuscany** : Livorno port/trade 3; **PAP / Romagna** : Bologna silk + Ancona port/trade; **SIC / Campania** : Naples port 3, naval/shipyard 2.

## 7. IMPORTANT_NON_RECOMMENDATIONS

| State | Industry | Decision | Reason | Source |
|---|---|---|---|---|
| GR3 / STATE_SICILY | building_sulfur_mine | NO_BUILDING | The large commercial sulfur-mining complex is characteristic of the early nineteenth century; do not backdate the boom to 1776. | https://iris.unipa.it/handle/10447/48232 |
| All regional states | rail PMs | NO_BUILDING | No active rail network is permitted at the 1776 cutoff; every infrastructure row keeps pm_no_rail_network. |  |
| PRU / STATE_UPPER_SILESIA | high-level coal/iron/steel complex | NO_BUILDING | The major state-led Upper Silesian heavy-industry acceleration associated with Heynitz/Reden begins after 1777; only conservative extraction levels are retained. | https://journals.iaepan.pl/khkm/article/view/926 |
| SIC / STATE_CAMPANIA | San Leucio-scale silk complex | NO_BUILDING | The royal silk colony/manufactory expansion at San Leucio belongs after the cutoff (from 1778 onward); Campania textile level is kept minimal. | https://www.treccani.it/enciclopedia/san-leucio_%28Enciclopedia-Italiana%29/ |
| TUS / STATE_TUSCANY | high road levels based on later Leopoldine works | NO_BUILDING | Road improvements accelerated from the 1770s; level 2 is retained, but later network extent is not backdated. | https://usiena-air.unisi.it/handle/11365/1079260 |
| BRE / STATE_ELBE | large ocean-port level | NO_BUILDING | Weser silting forced overseas goods to be lightered; Bremen remains an organized port but not a level-3 ocean harbor in 1776. | https://www.bremen.de/tourismus/erlebnisse/spazieren-wandern/bauwerke-erzaehlen-geschichte |
| All ordinary German/Italian states | building_steel_mill | NO_BUILDING | No ordinary start placement is recommended without evidence of a coke-smelting industrial complex at 1776 scale; bloomery/charcoal ironworking is not automatically this building. | https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49 |
| All ordinary German/Italian states | building_chemical_works / building_alloys_plant | NO_BUILDING | Scattered chemical/metallurgical practice does not establish the organized industrial-scale sectors represented by these fork buildings at the cutoff. |  |
| AUS / STATE_SLOVENIA | industrial canal PM for Trieste urban canal | NO_BUILDING | Trieste’s canal/harbor works are treated as port infrastructure, not a state-scale industrial canal network. | https://archiviodistatotrieste.it/documento-del-mese/marzo-2019-anniversario-del-porto-franco-di-trieste/ |
| PAP / STATE_ROMAGNA | industrial canal PM from Bologna urban waterways | NO_BUILDING | Bologna’s canals powered silk mills, but the evidence supports an urban power/water system rather than a regional transport canal network. | https://www.unibo.it/en/university/who-we-are/our-history/bologna-art-and-history |

## 8. Notes de prudence

- Les micro-États partageant un même State_ID ne reçoivent jamais automatiquement les grands équipements du propriétaire voisin. Lorsque le contexte proto-industriel couvre un district plus large que la frontière du fork, le niveau reste 1 et la confiance est abaissée.
- Les États sans ligne positive dans la matrice ont tout de même été couverts : l’absence de recommandation signifie que la recherche n’a pas trouvé de secteur dépassant le seuil LEVEL 1 avec une preuve suffisante.
- Les niveaux 3+ sont réservés aux concentrations internationales clairement documentées : verre de Bohême, textile saxon/suisse, Hambourg, Trieste, Livourne, Naples, grain sicilien.

## 9. Contrôle final

- STATES COVERED = **73** Owner_TAG + State_ID instances (dont 67 avec au moins une ligne positive)
- POSITIVE BUILDING ROWS = **201**
- TRADE CENTERS = **19**
- LEVEL 1 = **137**
- LEVEL 2 = **49**
- LEVEL 3 = **14**
- LEVEL 4-5 = **1**
- LEVEL 6+ = **0**
- TECH_DISTRIBUTION_REVIEW = **44**
- REVIEW CASES = **0**
- SERENISSIMA STATES SKIPPED = **8**

Aucun fichier gameplay modifié. Aucun code produit. Aucun commit/push.
