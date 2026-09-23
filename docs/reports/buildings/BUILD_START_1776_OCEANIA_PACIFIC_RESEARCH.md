# Recherche bâtiments de départ — Océanie et Pacifique — 1er janvier 1776

## 1. Périmètre et discipline technique

Cette recherche conserve la région historique **Océanie et Pacifique** de l’audit technologique précédent, mais utilise désormais l’unité technique obligatoire **Owner_TAG + State_ID**. Les lignes d’un même State_ID possédées par des TAG différents ne sont jamais fusionnées. La ligne `PHI + STATE_WEST_MICRONESIA` est exclue conformément au périmètre historique précédent qui excluait les Philippines; `TID + STATE_WESTERN_NEW_GUINEA` est conservée parce que la Nouvelle-Guinée faisait explicitement partie du périmètre. `HAW + STATE_HAWAIIAN_ISLANDS` est conservée même si le pack technique la classe dans R8.

Instances Owner/State couvertes : **58**.

- `HLA + STATE_BOUGAINVILLE` — Halia / Bougainville
- `PPU + STATE_EASTERN_NEW_GUINEA` — Papua / Eastern New Guinea
- `MCR + STATE_EAST_MICRONESIA` — Micronesia / East Micronesia
- `FJI + STATE_FIJI` — Fiji / Fiji
- `HAW + STATE_HAWAIIAN_ISLANDS` — Hawaii / Hawaiian Islands
- `KNK + STATE_KANAK` — Kanak / Kanak
- `NRU + STATE_NAURU` — Nauru / Nauru
- `KLN + STATE_NEW_SOUTH_WALES` — Kulin / New South Wales
- `KNC + STATE_NEW_SOUTH_WALES` — Karna / New South Wales
- `KRI + STATE_NEW_SOUTH_WALES` — Douriango / New South Wales
- `PAA + STATE_NEW_SOUTH_WALES` — Paakintyi / New South Wales
- `WDJ + STATE_NEW_SOUTH_WALES` — Wiradjuri / New South Wales
- `YUR + STATE_NEW_SOUTH_WALES` — Yura / New South Wales
- `ARH + STATE_NORTHERN_TERRITORY` — Arnhem / Northern Territory
- `ARR + STATE_NORTHERN_TERRITORY` — Arrernte / Northern Territory
- `GRW + STATE_NORTHERN_TERRITORY` — Garawa / Northern Territory
- `KNC + STATE_NORTHERN_TERRITORY` — Karna / Northern Territory
- `LRR + STATE_NORTHERN_TERRITORY` — Larrakia / Northern Territory
- `NYP + STATE_NORTHERN_TERRITORY` — Ngumpin-Yapa / Northern Territory
- `WRR + STATE_NORTHERN_TERRITORY` — Worrorra / Northern Territory
- `WTI + STATE_NORTHERN_TERRITORY` — Anangu / Northern Territory
- `YGU + STATE_NORTHERN_TERRITORY` — Yolngu / Northern Territory
- `NTO + STATE_NORTH_ISLAND` — Ngāti Toa / North Island
- `UNT + STATE_NORTH_ISLAND` — United Tribes / North Island
- `ARR + STATE_QUEENSLAND` — Arrernte / Queensland
- `GRW + STATE_QUEENSLAND` — Garawa / Queensland
- `KNC + STATE_QUEENSLAND` — Karna / Queensland
- `MRA + STATE_QUEENSLAND` — Mara / Queensland
- `PAA + STATE_QUEENSLAND` — Paakintyi / Queensland
- `PMA + STATE_QUEENSLAND` — Pama / Queensland
- `WDJ + STATE_QUEENSLAND` — Wiradjuri / Queensland
- `WKB + STATE_QUEENSLAND` — Waka-Gabi / Queensland
- `BLA + STATE_SOLOMON_ISLANDS` — Bilua / Solomon Islands
- `KAU + STATE_SOUTH_AUSTRALIA` — Kaurna / South Australia
- `KLN + STATE_SOUTH_AUSTRALIA` — Kulin / South Australia
- `KNC + STATE_SOUTH_AUSTRALIA` — Karna / South Australia
- `MRN + STATE_SOUTH_AUSTRALIA` — Mirning / South Australia
- `PAA + STATE_SOUTH_AUSTRALIA` — Paakintyi / South Australia
- `WTI + STATE_SOUTH_AUSTRALIA` — Anangu / South Australia
- `YUR + STATE_SOUTH_AUSTRALIA` — Yura / South Australia
- `NTO + STATE_SOUTH_ISLAND` — Ngāti Toa / South Island
- `NTU + STATE_SOUTH_ISLAND` — Ngāi Tahu / South Island
- `PLY + STATE_TAHITI` — Tahiti / Tahiti
- `WTI + STATE_TASMANIA` — Anangu / Tasmania
- `TNG + STATE_TONGA` — Tonga / Tonga
- `VNT + STATE_VANUATU` — Vanuatu / Vanuatu
- `KLN + STATE_VICTORIA` — Kulin / Victoria
- `KRI + STATE_VICTORIA` — Douriango / Victoria
- `KTU + STATE_WESTERN_AUSTRALIA` — Kartu / Western Australia
- `KYN + STATE_WESTERN_AUSTRALIA` — Pilbara / Western Australia
- `MRN + STATE_WESTERN_AUSTRALIA` — Mirning / Western Australia
- `NNG + STATE_WESTERN_AUSTRALIA` — Noongar / Western Australia
- `NYP + STATE_WESTERN_AUSTRALIA` — Ngumpin-Yapa / Western Australia
- `WRR + STATE_WESTERN_AUSTRALIA` — Worrorra / Western Australia
- `WTI + STATE_WESTERN_AUSTRALIA` — Anangu / Western Australia
- `PPU + STATE_WESTERN_NEW_GUINEA` — Papua / Western New Guinea
- `TID + STATE_WESTERN_NEW_GUINEA` — Tidore / Western New Guinea
- `MCR + STATE_WEST_MICRONESIA` — Micronesia / West Micronesia

## 2. Règles utilisées

- seuls les bâtiments dont `Relevant_For_1776_Start_Research` commence par `YES` ont été considérés;
- aucun bâtiment `Auto_Generated = YES`, `History_Placeable = NO_ENGINE_GENERATED` ou `NO_POST_1776` n’est proposé;
- un artisanat domestique, un village isolé, une simple route, un simple mouillage ou une extraction ponctuelle ne suffit pas;
- le seuil d’un `building_trade_center` reste particulièrement sévère;
- `building_railway` signifie ici le réseau terrestre régional unifié : **routes éventuellement actives, canaux seulement si justifiés, rail toujours `pm_no_rail_network`**;
- une porte technologique manquante ne supprime pas une capacité historique : elle produit `Tech_Distribution_Review = YES`.

## 3. Résultat principal

La région produit seulement **5 recommandations positives**. Ce faible nombre est volontaire : les économies océaniennes de 1776 possèdent de nombreuses technologies et infrastructures complexes, mais une grande partie relève de la production domestique, de la redistribution lignagère/tributaire ou de catégories que le catalogue de bâtiments ne représente pas correctement.

### Hawaii

Trois bâtiments passent le seuil. Les systèmes d’aquaculture à fishponds sont suffisamment nombreux et organisés pour justifier `building_fishing_wharf` **LEVEL 2** comme abstraction de la production halieutique, mais avec `Tech_Distribution_Review = YES` car la porte `marine_chronometry` ne correspond pas à cette capacité. Les salines traditionnelles en bassins artificiels justifient `building_salt_pan` **LEVEL 1**. Enfin le réseau pré-contact de chemins `ala loa`/mauka-makai — 175 miles documentés sur Hawaiʻi Island et plus de 200 ahupuaʻa traversés — justifie prudemment `building_railway` **LEVEL 1** comme réseau routier traditionnel, sans canal et sans rail.

### Tahiti

`building_trade_center` **LEVEL 1** est retenu. Matavai est déjà un mouillage récurrent après 1767; Cook revient en 1773, et les échanges de provisions contre produits européens sont suffisamment réguliers et organisés pour représenter une petite capacité commerciale intercontinentale. Le niveau reste 1 : aucun entrepôt international comparable aux grandes places marchandes européennes n’est démontré.

### Tonga

`building_shipyard` **LEVEL 1** est retenu malgré la porte technologique manquante. Les témoignages de 1773 décrivent des canoës tongiens d’une qualité exceptionnelle et un grand double canoë en construction dans un boat-house sous patronage chiefly. Il s’agit d’une véritable capacité organisée de construction navale, même si elle ne ressemble pas à un chantier européen de clippers. `Tech_Distribution_Review = YES`.

## 4. Centres de commerce — contrôle conservateur

Un seul centre de commerce est recommandé : **Tahiti LEVEL 1**. Tonga, Fidji, Micronésie, Nouvelle-Zélande et Nouvelle-Guinée avaient des réseaux d’échange parfois très étendus, mais les sources utilisées ne montrent pas pour le 1er janvier 1776 une place marchande/entrepôt permanent répondant au seuil du bâtiment. L’étude ANU sur les échanges Fidji–Tonga–Samoa est particulièrement utile : elle décrit des échanges bien établis et des biens rassemblés sous la direction de chefs, tout en précisant l’absence de stockage ou d’installations portuaires permanentes.

## 5. Infrastructure régionale

Une seule implantation positive de `building_railway` est retenue : **HAW + STATE_HAWAIIAN_ISLANDS, LEVEL 1**.

- `ROAD_LEVEL_JUSTIFICATION = YES` : réseau ancien de pistes/trails construit et interconnecté;
- `CANAL_LEVEL_JUSTIFICATION = NO`;
- `pm_no_rail_network` obligatoire.

Les gigantesques canaux d’irrigation kanak ne sont **pas** convertis en canaux de transport.

## 6. IMPORTANT_NON_RECOMMENDATIONS

| State / Owner | Industry | Decision | Reason | Source |
|---|---|---|---|---|
| HAW / STATE_HAWAIIAN_ISLANDS | `building_trade_center` | NO_BUILDING | Chiefly tribute and inter-island redistribution were substantial, but the evidence used here does not establish a permanent merchant/warehouse hub at the conservative one-level threshold. | https://www.nps.gov/locations/hawaii/social-structure.htm |
| PLY / STATE_TAHITI | `building_port` | NO_BUILDING | Matavai was a repeatedly used anchorage and provisioning market, but an anchorage is not an organized dock/port installation. | https://www.museetahiti.pf/evenements/lancre-dite-de-cook/ |
| TNG / STATE_TONGA | `building_trade_center` | NO_BUILDING | Tonga participated in well-established Fiji-Tonga-Samoa exchange, but sources describe goods gathered under chiefs and temporary receiving arrangements rather than permanent warehouses or harbour facilities. | https://openresearch-repository.anu.edu.au/bitstreams/e3cc7459-0dc1-4e3d-99f3-7e7ea1cc7e1b/download |
| FJI / STATE_FIJI | `building_trade_center` | NO_BUILDING | Long-distance exchange was real, but the evidence emphasizes kinship/chiefly regulation and temporary receiving structures rather than a fixed merchant centre. | https://openresearch-repository.anu.edu.au/bitstreams/e3cc7459-0dc1-4e3d-99f3-7e7ea1cc7e1b/download |
| FJI / STATE_FIJI | `building_salt_pan` | NO_BUILDING | A prehistoric salt industry is archaeologically attested, but the excavated industry discussed by Antiquity is seventh-century and had disappeared; later analogues are nineteenth/twentieth century, so it cannot prove a 1776 salt-works sector. | https://www.cambridge.org/core/journals/antiquity/article/abs/an-archaeology-of-salt-production-in-fiji/AF13B954AD3F4495C5C292E6AE90C2D0 |
| FJI / STATE_FIJI | `building_shipyard` | NO_BUILDING | Fijian oceanic shipbuilding was sophisticated, but the classic plank-built drua complex and its specialist migration are dated broadly to the second half of the eighteenth century; evidence found here is not precise enough to prove the sector by 1776-01-01. | https://maa.cam.ac.uk/sea-islands |
| MCR / STATE_WEST_MICRONESIA | `building_limestone_quarry` | NO_BUILDING | Yapese stone money depended on limestone quarrying, but the quarries were in Palau, across roughly 400 km of open sea, not in the Yap/Micronesia state instance. | https://whc.unesco.org/en/tentativelists/1994 |
| MCR / STATE_WEST_MICRONESIA | `building_trade_center` | NO_BUILDING | Long-distance exchange and stone-money institutions are well established, but the source does not establish a permanent merchant/warehouse centre equivalent to a Victoria 3 trade-center level. | https://whc.unesco.org/en/tentativelists/1994 |
| MCR / STATE_EAST_MICRONESIA | `building_trade_center` | NO_BUILDING | Micronesian long-distance interaction existed, but Nan Madol was primarily a ceremonial/political complex of an earlier period and does not prove a 1776 commercial hub. | https://whc.unesco.org/en/list/1503 |
| NTO / STATE_NORTH_ISLAND; UNT / STATE_NORTH_ISLAND; NTO / STATE_SOUTH_ISLAND; NTU / STATE_SOUTH_ISLAND | `building_trade_center` | NO_BUILDING | Pre-European Maori had regular long-distance barter in stone, food and other goods, but evidence describes inter-hapu/iwi exchange rather than a fixed merchant entrepot. | https://teara.govt.nz/en/nga-umanga-maori-business-enterprise/page-1 |
| NTO / STATE_NORTH_ISLAND; UNT / STATE_NORTH_ISLAND; NTO / STATE_SOUTH_ISLAND; NTU / STATE_SOUTH_ISLAND | `building_railway` | NO_BUILDING | Freight moved by waka or on foot and narrow tracks linked settlements; this does not reach the threshold for a regional road-network building. | https://teara.govt.nz/en/freight-and-warehousing/page-1 |
| NTU / STATE_SOUTH_ISLAND; NTO / STATE_NORTH_ISLAND | `industrial mine IDs (gold/coal/iron/etc.)` | NO_BUILDING | Maori quarrying of pounamu, obsidian and argillite was real and long-distance traded, but these materials do not match the industrial resource buildings available in the catalogue. | https://teara.govt.nz/en/mining-and-underground-resources/page-2 |
| KNK / STATE_KANAK | `building_railway (canal PM)` | NO_BUILDING | Kanak irrigation works were enormous and technically sophisticated, including terraced taro fields and canals over kilometres, but these are irrigation channels, not transport canals. | https://www.ird.fr/en-nouvelle-caledonie-leau-cest-le-lien |
| KNK / STATE_KANAK | `commercial farm/plantation IDs` | NO_BUILDING | Large taro and yam systems are strongly attested, but the 1776 building catalogue has no taro/yam commercial building; do not force them into rice/banana/spice plantations. | https://museenouvellecaledonie-collections.gouv.nc/fr/notice/mnc-86-5-444-pierre-a-magie-culture-du-taro-collection-mnc-510786bc-83bc-4df4-8531-b6ca6d8fb093 |
| PPU / STATE_EASTERN_NEW_GUINEA; PPU / STATE_WESTERN_NEW_GUINEA | `building_trade_center` | NO_BUILDING | Long-distance maritime exchange networks around New Guinea are ancient and substantial, but no fixed 1776 commercial hub is demonstrated for these exact owner/state instances. | https://openresearch-repository.anu.edu.au/items/ad780e72-176f-4503-b056-4e5ea3c7cf85/full |
| TID / STATE_WESTERN_NEW_GUINEA | `building_trade_center` | NO_BUILDING | Tidore-linked bird-of-paradise trade clearly reached the Bird’s Head/Raja Ampat network, but the collecting/credit chain fed emporia outside this state; no fixed trade centre inside the current Western New Guinea state is established. | https://www.cambridge.org/core/journals/journal-of-southeast-asian-studies/article/flights-of-fancy-the-bird-of-paradise-and-its-cultural-impact/4622573F050E7B15FF75485C28AC9678 |
| Australian Owner_TAG + State_ID instances | `industrial mine IDs` | NO_BUILDING | Large and technically significant ochre mines existed and participated in exchange networks, but ochre is not a resource building in the supplied catalogue; do not mis-map it to iron/gold/copper/lead mines. | https://journals.australian.museum/paterson-and-lampert-1985-rec-aust-mus-371-19/ |
| Australian Owner_TAG + State_ID instances | `building_railway` | NO_BUILDING | No evidence used in this pass supports a state-scale engineered road or transport-canal network before 1776; local tracks and routes remain abstracted outside the building system. | https://journals.australian.museum/paterson-and-lampert-1985-rec-aust-mus-371-19/ |
| PLY / STATE_TAHITI | `building_easter_island_heads` | NO_BUILDING | The landmark is historically pre-1776, but the supplied state catalogue exposes no dedicated Easter Island Owner_TAG + State_ID. This pass will not silently assume that STATE_TAHITI contains the correct map province for manual placement. | https://whc.unesco.org/en/list/715/ |


## 7. Matrice positive

La matrice complète est fournie dans `BUILD_START_1776_OCEANIA_PACIFIC_RESEARCH.csv` avec les colonnes exactes demandées.

## 8. Contrôle final

- STATES COVERED = **58**
- POSITIVE BUILDING ROWS = **5**
- TRADE CENTERS = **1**
- LEVEL 1 = **4**
- LEVEL 2 = **1**
- LEVEL 3 = **0**
- LEVEL 4-5 = **0**
- LEVEL 6+ = **0**
- TECH_DISTRIBUTION_REVIEW = **2**
- REVIEW CASES = **0**
- SERENISSIMA STATES SKIPPED = **0** (aucune instance VEN/GEN dans ce périmètre historique)

Aucun State_ID ni Building_ID n’a été inventé. Aucun bâtiment postérieur au cutoff n’est proposé. Aucun fichier de gameplay n’a été modifié.
