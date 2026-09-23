# BUILD START 1776 — Europe du Nord et Europe orientale — recherche historique

**Date absolue : 1776-01-01.** Recherche uniquement. Aucun fichier gameplay modifié, aucun code Victoria 3, aucun commit/push.

## 1. Périmètre et unité de recherche

L'unité est strictement **`Owner_TAG + State_ID`**. Deux lignes portant le même `State_ID` mais des propriétaires différents ne sont jamais fusionnées.

Cette passe couvre **67 instances Owner/State** du périmètre historique déjà attribué à cette recherche. Les propriétaires actifs rencontrés sont : SWE, DENNOR, RUS, PLC, UBD et CRI.

- `DEN`, `NOR`, `FIN` et `KRA` sont des setups alternatifs pertinents technologiquement, mais n'ont pas d'instance propriétaire active dans le catalogue d'États fourni ; aucune implantation bâtiment n'est donc inventée pour eux.
- Les possessions extra-européennes de DENNOR sont laissées aux régions correspondant à leur emplacement, conformément au pack.
- `STATE_KUBAN` est exclu ici comme Caucase.
- L'Oural russe (`RUS + STATE_URAL`, ainsi que Perm/Chelyabinsk/Ufa) est conservé comme exception de continuité avec le périmètre précédent, car la métallurgie de l'Oural faisait explicitement partie des priorités historiques de cette région.
- Toute possession `VEN`/`GEN` reste totalement exclue ; aucune n'est présente dans les recommandations ci-dessous.

## 2. Méthode technique

Seuls les bâtiments marqués comme pertinents dans le catalogue sont utilisés : `YES`, `YES_TECH_DISTRIBUTION_REVIEW`, `YES_ROADS_CANALS_ONLY_NO_RAIL` ou `YES_CASE_BY_CASE_TRADE_SEED`. Aucun bâtiment `Auto_Generated = YES`, `NO_ENGINE_GENERATED`, `NO_POST_1776` ou système spécial n'est proposé.

Le CSV de sortie est volontairement une **liste positive de seeds manuels** : l'absence de ligne pour un couple Owner/State/Bâtiment signifie qu'aucun niveau manuel n'est recommandé par cette première recherche historique. Les fermes de subsistance et centres urbains générés par le moteur ne sont donc jamais reproduits à la main.

Pour `building_railway`, l'ID est utilisé comme réseau terrestre régional unifié. Toutes les lignes conservent **`pm_no_rail_network`**. Les routes et canaux sont justifiés séparément dans `ROAD_LEVEL_JUSTIFICATION` et `CANAL_LEVEL_JUSTIFICATION`.

Pour chaque bâtiment à porte technologique, `Tech_Distribution_Review = YES` lorsque la technologie nécessaire est absente de la distribution actuellement implémentée selon l'audit technologique précédent. La recommandation historique du bâtiment n'est pas supprimée pour cette raison.

## 3. Centres de commerce — approche conservatrice

Un centre de commerce n'est proposé que pour un véritable entrepôt/entrepôt de redistribution ou un marché de longue distance. Les niveaux restent bas par rapport à l'importance historique afin d'éviter la surcapacité.

- **SWE + STATE_SVEALAND (Svealand)** : niveau **2** — Stockholm was a major Baltic capital and redistribution/export market; two levels are conservative for a true long-distance commercial hub.
- **SWE + STATE_GOTALAND (Götaland)** : niveau **2** — Gothenburg had become a major shipping and trading town through iron/wood exports and the Swedish East India Company.
- **DENNOR + STATE_ZEALAND (Zealand)** : niveau **2** — Copenhagen was the monarchy's dominant administrative, naval and long-distance commercial center.
- **DENNOR + STATE_WESTERN_NORWAY (Western Norway)** : niveau **1** — Bergen remained Norway's largest city and the central redistribution/export market for northern fish.
- **RUS + STATE_INGRIA (Ingria)** : niveau **3** — St Petersburg had become a principal Russian export outlet and major Baltic commercial hub by the mid-eighteenth century.
- **RUS + STATE_MOSCOW (Moscow)** : niveau **2** — Moscow remained a major internal redistribution, craft and mercantile center despite the move of the capital.
- **RUS + STATE_NIZHNY_NOVGOROD (Nizhny Novgorod)** : niveau **1** — The Volga/Oka confluence made Nizhny Novgorod a significant redistribution point even before the later nineteenth-century fair peak.
- **RUS + STATE_KAZAN (Kazan)** : niveau **1** — Kazan was a major Volga regional market and administrative center.
- **RUS + STATE_ARKHANGELSK (Arkhangelsk)** : niveau **1** — Arkhangelsk remained an established northern foreign-trade outlet despite St Petersburg's rise.
- **PLC + STATE_GREATER_POLAND (Warszawa)** : niveau **2** — Warsaw had become the Commonwealth's dominant political and growing commercial center by the reign of Stanisław August.
- **UBD + STATE_RIGA (South Livonia)** : niveau **3** — Riga was one of the eastern Baltic's great long-distance export entrepôts, especially for flax, hemp, timber and seeds.
- **UBD + STATE_TALINN (Talinn)** : niveau **1** — Reval/Tallinn remained an established Baltic port market, but at distinctly smaller scale than Riga.
- **CRI + STATE_CRIMEA (Crimea)** : niveau **1** — Crimea possessed genuine long-distance commercial centers and Black Sea markets, with Caffa/Kefe historically a major port market.

Cas crucial : **`UBD + STATE_RIGA` reçoit le seed commercial de Riga ; `RUS + STATE_RIGA` ne reçoit pas un second centre de commerce.** Les deux instances restent distinctes dans la matrice.

## 4. Infrastructure régionale

Deux réseaux artificiels russes sont assez solidement établis pour recevoir un PM canal au départ :
- **RUS + STATE_INGRIA** — Level 2 canal justification: the Ladoga bypass canal opened in 1731 and functioned as part of the Volga–Baltic supply route.
- **RUS + STATE_TVER** — Level 1 canal justification for the Vyshny Volochyok water system, modernized before 1776.

Le Dnieper–Bug/Brest est traité différemment : les travaux commencent en 1775, mais l'ouvrage n'est pas considéré comme un réseau industriel actif au 1er janvier 1776. La ligne `PLC + STATE_BREST` garde donc `pm_no_canal_network`.

## 5. Production, mines et manufactures

### Suède

Bergslagen reçoit une concentration minière et sidérurgique dans `SWE + STATE_SVEALAND`. Le bâtiment `building_steel_mill` y représente les **ironworks** organisés : historiquement, l'énergie est au charbon de bois, pas au coke. Le conflit avec la porte `coke_smelting` est donc signalé à la synthèse technologique plutôt que de supprimer le bâtiment.

Kosta justifie un `building_glassworks` dans Götaland dès 1742. Klippan et la longue tradition papetière suédoise justifient un niveau de papier en Scanie et un seed modeste à Svealand. Aucun textile mécanisé du XIXe siècle n'est projeté rétroactivement.

### Danemark-Norvège

Copenhague/Zealand concentre les institutions navales et une partie de l'industrie militaire. Frederiksværk fournit une justification directe au canon-foundry, et les manufactures de laine militaires à un textile mill. En Norvège, Røros justifie un copper mine ; Kongsberg n'est **pas** converti artificiellement en `building_gold_mine`, car le catalogue ne possède pas de mine d'argent adaptée.

Nøstetangen/Hurdal justifie un glassworks en Norvège orientale. Bergen reçoit le seul centre de commerce norvégien de cette passe.

### Russie

La distribution est fortement géographique : Tula (`STATE_ORYOL`) reçoit l'industrie d'armes ; l'Oural reçoit la concentration minière/métallurgique ; St Petersburg/Ingria reçoit le complexe naval, commercial, administratif et les grands travaux. Ces concentrations ne sont pas diffusées artificiellement à toutes les provinces russes.

### Pologne-Lituanie

La passe maintient une économie globalement agricole mais reconnaît les concentrations réelles de manufactures : Warsaw et surtout Grodno/Horodnica. Les implantations Tyzenhaus commencent vers 1767 et justifient textile et ateliers dans `PLC + STATE_BREST`, sans projeter les développements de la fin des années 1770 sur tout le Commonwealth.

### Baltique

Riga est traitée comme un véritable entrepôt baltique international ; Tallinn reste un port/marché secondaire. Les flux de lin, chanvre et bois justifient des capacités de transformation/logging modestes, sans convertir automatiquement tout Livonia en industrie urbaine.

### Crimée

Les recommandations sont volontairement basses : un seul centre de commerce, un port, des salines, élevage, vigne/tabac et transformation alimentaire. Le sel bénéficie de la preuve la plus forte ; les niveaux agricoles restent prudents.

## 6. Militaire et marine

- **SWE/Uusimaa** : Sveaborg = fortification navale + administration + chantier naval + port.
- **SWE/Götaland** : Karlskrona est représentée à échelle modérée ; les grands programmes navals de Gustav III postérieurs à 1776 ne servent pas à gonfler les niveaux de départ.
- **DENNOR/Zealand** : Holmen/Nyholm et Frederiksværk justifient le plus fort cluster naval/militaire danois.
- **RUS/Ingria** : Admiralty/Kronstadt = cluster naval principal.
- **RUS/Tula** : production réglementée d'armes, mais pas propagation nationale du même niveau.

## 7. Monuments

Le seul monument du catalogue pertinent explicitement recommandé dans cette région est `building_saint_basils_cathedral` à `RUS + STATE_MOSCOW`. Les monuments postérieurs à 1776 et les systèmes spéciaux restent exclus.

## 8. Principales recommandations

1. **RUS + STATE_INGRIA** — St Petersburg/Kronstadt : trade center 3, port 2, shipyard 2, naval administration 2, fortification 2, roads 2 + canals 2.
2. **RUS + STATE_ORYOL** — Tula : arms industry 2 + tooling workshop 1, based on the state arms factory founded in 1712.
3. **RUS + STATE_URAL** — Urals : iron mine 3, copper mine 2, steel/ironworks 2, logging 2; charcoal metallurgy, not coke.
4. **SWE + STATE_SVEALAND** — Stockholm/Bergslagen : trade center 2, iron mine 2, ironworks 2, government 2, university 1.
5. **SWE + STATE_GOTALAND** — Gothenburg/Karlskrona/Kosta abstraction : trade 2, port 2, naval/shipyard capacity, glassworks 1.
6. **SWE + STATE_UUSIMAA** — Sveaborg : naval fortification 2, shipyard 1, naval administration 1, port 1.
7. **DENNOR + STATE_ZEALAND** — Copenhagen/Holmen/Frederiksværk : trade 2, port 2, shipyard 2, naval administration 2, arms/artillery/textiles.
8. **DENNOR + STATE_NORTHERN_NORWAY** — Røros + northern fisheries : copper mine 1, fishing 2.
9. **DENNOR + STATE_WESTERN_NORWAY** — Bergen : trade center 1, port 2, fishing 2, shipyard 1.
10. **PLC + STATE_BREST** — Grodno/Horodnica : textile 2 plus diversified workshops and administration; no active canal despite works beginning in 1775.
11. **PLC + STATE_GREATER_POLAND** — Warsaw : trade 2, government 2, construction/manufacturing seed.
12. **UBD + STATE_RIGA** — Riga : trade center 3, port 2; this is the Riga-city commercial seed.
13. **RUS + STATE_RIGA** — No duplicate trade center: only a hinterland logging seed on the Russian partition.
14. **CRI + STATE_CRIMEA** — Crimea : trade 1, port 1, salt pans 2, vineyard/tobacco/livestock; deliberately conservative.
15. **RUS + STATE_TVER** — Imperial route + Vyshny Volochyok: road level 2 and industrial-canal PM 1.
16. **RUS + STATE_INGRIA** — Ladoga canal active since 1731: explicit industrial-canal justification, rail remains disabled.
17. **SWE + STATE_GOTALAND** — Kosta glassworks receives one glassworks level from a documented 1742 foundation.
18. **DENNOR + STATE_EASTERN_NORWAY** — Nøstetangen/Hurdal gives one glassworks level; Kongsberg silver is NOT misrepresented as a gold mine.
19. **RUS + STATE_MOSCOW** — Moscow : trade/government/construction 2; university and diversified manufactories 1–2.
20. **RUS + STATE_MOSCOW** — St Basil's Cathedral explicitly seeded as a pre-1776 monument.

## 9. États du périmètre sans seed manuel positif

- `RUS + STATE_NENETSIA` — Nenetsia: aucun bâtiment manuel suffisamment justifié à ce stade ; la subsistance/urbanisation générée par le moteur couvre le fond économique.
- `PLC + STATE_WEST_PRUSSIA` — West Prussia: aucun bâtiment manuel suffisamment justifié à ce stade ; la subsistance/urbanisation générée par le moteur couvre le fond économique.

## 10. Contrôle final

- Instances Owner/State dans le périmètre explicite : **67**
- Recommandations positives Owner/State/Building : **237**
- `Tech_Distribution_Review = YES` : **70**
- Centres de commerce proposés : **13**
- Réseaux terrestres régionaux (`building_railway`) proposés : **27**
- Réseaux avec canal actif (`pm_industrial_canals`) : **2**
- Réseau ferroviaire actif : **0** — toutes les lignes `building_railway` gardent `pm_no_rail_network`.
- Bâtiments auto-générés proposés manuellement : **0**.
- Bâtiments `NO_POST_1776` proposés : **0**.
- Possessions VEN/GEN traitées : **0**.

## 11. Sources historiques principales

- bergen: https://snl.no/Bergen_-_historie
- crimea_salt: https://wiki.crimea-is-ukraine.org/en/wiki/concepts/zaporozko-krymski-torgovelni-vidnosyny-xviii/
- crimea_trade: https://dergipark.org.tr/en/pub/odusobiad/article/290158
- danish_military: https://natmus.dk/historisk-viden/temaer/militaerhistorie/den-hvervede-haer/krigen-og-dens-forberedelse/militaerindustrien/
- danish_navy: https://www.navalhistory.dk/Danish/Tidslinie/Aarligt/1700.htm
- engelsberg: https://www.raa.se/evenemang-och-upplevelser/upplev-kulturarvet/varldsarv-i-sverige/alla-varldsarv-i-sverige/engelsbergs-bruk/
- gothenburg: https://www.stage.goteborg.com/en/guides/gothenburgs-history-and-heritage
- kongsberg: https://snl.no/Kongsberg_s%C3%B8lvverk
- kosta: https://glasriket.se/stories/kosta-275-ar/
- ladoga: https://history.milportal.ru/primenenie-vojsk-na-stroitelstve-ladozhskogo-kanala-1719-1731-gg/?print=print
- norway_mining: https://snl.no/norsk_bergindustrihistorie
- norway_shipping: https://snl.no/Norsk_skipsfartshistorie_f%C3%B8r_1940
- plc_canal: https://www.encyclopediaofukraine.com/display.asp?linkpath=pages%5CD%5CN%5CDniproRiver.htm
- plc_grodno: https://www.lazienki-krolewskie.pl/pl/edukacja/baza-wiedzy/ekonomie-krolewskie-za-panowania-stanislawa-augusta
- plc_trade: https://www.ldkistorija.lt/the-role-of-riga-konigsberg-and-gdansk-in-the-trade-of-the-grand-duchy-of-lithuania/
- riga_trade: https://www.tandfonline.com/doi/pdf/10.1080/03585522.1981.10407958
- russia_admiralty: https://admship.ru/en/about/history/
- russia_archives: https://guides.rusarchives.ru/terms/10/2911/oruzheynaya-kontora
- russia_arms: https://museum-arms.ru/exhibitions/e/vystavka-oruzeinaia-kuznica-rossiiskoi-imperii-1721-1917-k-3
- russia_riga_trade: https://journals.sagepub.com/doi/10.1177/08438714231169583
- russia_road: https://museum.tverlib.ru/yamschickoe-delo-pochtovye-trakty
- russia_ural: https://digitalcommons.kennesaw.edu/thegeographicalbulletin/vol10/iss1/5/
- sveaborg: https://suomenlinna.fi/en/explore/history/
- sveaborg_dock: https://suomenlinna.fi/en/sights/
- swedish_iron: https://www.jernkontoret.se/en/the-steel-industry/the-history-of-swedish-steel-industry/
- swedish_paper: https://www.tekniskamuseet.se/lar-dig-mer/100-innovationer/papper/
- Suomenlinna / Sveaborg: https://suomenlinna.fi/en/explore/history/
- Suomenlinna dock: https://suomenlinna.fi/en/sights/
- Tula Arms Museum: https://museum-arms.ru/exhibitions/e/vystavka-oruzeinaia-kuznica-rossiiskoi-imperii-1721-1917-k-3
- Tyzenhaus/Grodno: https://www.lazienki-krolewskie.pl/pl/edukacja/baza-wiedzy/ekonomie-krolewskie-za-panowania-stanislawa-augusta
- Crimean/Caffa trade: https://dergipark.org.tr/en/pub/odusobiad/article/290158

## 12. Fichiers

- `BUILD_START_1776_NORTHERN_EASTERN_EUROPE_RECOMMENDATIONS.csv`
- `BUILD_START_1776_NORTHERN_EASTERN_EUROPE_RESEARCH.md`

Aucun fichier gameplay n'a été modifié.