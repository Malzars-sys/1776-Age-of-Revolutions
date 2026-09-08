# TECH6C2A — Global Limestone Resource Distribution Audit

## Audit result

**Status: PASS — research and design only; no gameplay implementation.**

- Starting branch: `tech6c-goods-buildings-pm-implementation`
- Starting HEAD: `08614a77209e8c111d4dc5ba41d42e961d62844b` (`08614a7`)
- Canonical game version supplied by the phase brief: Victoria 3 `1.13.11`
- Baseline: `TECH6C1_LIMESTONE_RESOURCE_POTENTIAL_DEFERRED_MATRIX.csv`
- Baseline states: **675**
- Output states: **675**
- Missing / duplicate states: **0 / 0**
- Gameplay footprint from TECH6C2A: **0 files**

The implementation-ready recommendations are in:

- `TECH6C2A_LIMESTONE_GLOBAL_DISTRIBUTION_MATRIX.csv` — one auditable row per state;
- `TECH6C2A_LIMESTONE_REGIONAL_EVIDENCE.csv` — the regional evidence register and translation rules.

## Methodology

The audit used a hierarchical method rather than attempting to identify 675 individual quarries.

1. The TECH6C1 deferred matrix was treated as the state identity and resource-context authority.
2. Existing fork/vanilla capped-resource distributions were measured to establish the numerical order of magnitude.
3. States were assigned to 28 geological evidence regions. The required 23 world regions are all represented, with additional categories for the Sahel/Nile transition, Central Asia/Himalaya, Siberia/Arctic, Pacific islands, and Atlantic volcanic islands.
4. National geological surveys, government geological agencies, USGS-equivalent sources, and regional geological compilations established whether carbonates are extensive, mixed, local, deeply covered, volcanic, shield-hosted, or difficult to access.
5. Regional conclusions were translated to state rows and then adjusted for major carbonate provinces, chalk belts, karst belts, shields, volcanic arcs, deep alluvium, land area, and accessibility.
6. Each row received a numeric potential, class, confidence, region, rationale, source URLs, and implementation status.

`current_relevant_resources` was preserved as context only. Coal, iron, sulfur, logging, or salt presence was never used as proof of limestone. Population, capital status, and current industrial demand were also excluded from the geological classification.

## Source hierarchy and uncertainty policy

The evidence hierarchy was:

1. **Tier A:** national geological surveys, geological ministries, USGS and equivalents, geological map services, government resource inventories, and regional survey collaborations;
2. **Tier B:** official industrial-mineral reports and historical geological/resource surveys;
3. **Tier C:** secondary geological references only as navigation or cross-checks.

No commercial quarry directory, retailer listing, or Wikipedia page is a primary source. Broad global compilations were used to bridge gaps, not to manufacture deposit-level certainty.

Confidence means evidence resolution, not resource abundance:

- `HIGH_CONFIDENCE`: national or subnational mapping/inventory gives a strong translation basis;
- `MEDIUM_CONFIDENCE`: authoritative regional or national mapping supports the classification but not precise state capacity;
- `LOW_CONFIDENCE`: broad mapping, coarse state aggregation, remote terrain, or small islands require targeted follow-up;
- `ZERO_JUSTIFIED`: the zero is supported by unusually unfavorable regional geology;
- `NO_EVIDENCE`: permitted by the schema but unused because every state was covered by at least regional evidence.

All `LOW_CONFIDENCE` and `ZERO_JUSTIFIED` rows are `REVIEW_REQUIRED`.

## Existing resource-capacity benchmark

Numeric capped values were parsed from `current_relevant_resources` across the 675-state baseline. Discoverable entries without a numeric cap were not treated as numeric observations.

| Existing resource | States with numeric cap | Minimum | Median | P75 | P90 | Maximum | Mean |
|---|---:|---:|---:|---:|---:|---:|---:|
| Coal | 257 | 3 | 36 | 56 | 80 | 140 | 40.3 |
| Iron | 296 | 2 | 24 | 33 | 48 | 104 | 26.8 |
| Lead | 123 | 3 | 24 | 30 | 45 | 90 | 24.2 |
| Sulfur | 108 | 3 | 32 | 40 | 48 | 100 | 30.7 |
| Salt pan | 97 | 2 | 25 | 35 | 40 | 80 | 26.0 |
| Logging | 618 | 1 | 10 | 17 | 25 | 100 | 13.4 |

These values are benchmarks, not templates. Limestone is more geographically widespread than metallic ores, but a single state's cap should remain within familiar Victoria 3 magnitudes.

## Limestone potential scale

| Class | Potential | Calibration | Baseline industrial interpretation |
|---|---:|---|---|
| `NONE` | 0 | Reserved for a strongly justified geological exception | No local quarry level |
| `LOW` | 8 | One-half of `MODEST`, close to the logging median of 10 | Up to about 8 baseline Cement Works levels |
| `MODEST` | 16 | One-half of the sulfur median of 32 | Up to about 16 baseline Cement Works levels |
| `MEDIUM` | 28 | Midpoint of the 24 median for iron/lead and the 32 sulfur median | Up to about 28 baseline Cement Works levels |
| `HIGH` | 48 | The measured P90 for both iron and sulfur | Up to about 48 baseline Cement Works levels |
| `VERY_HIGH` | 80 | Coal P90 and salt-pan maximum | Up to about 80 baseline Cement Works levels |

This deliberately non-linear scale creates useful differentiation without copying coal. It also avoids effectively infinite caps: the worldwide proposed total is **21,520** levels, with a state mean of **31.88**, but actual use still requires construction, labor, tools, and downstream demand.

## Economic calibration

The implemented baseline production methods establish:

- 1 Limestone Quarry level produces **30 limestone**;
- 1 Cement Works level consumes **30 limestone** and 15 coal to produce 40 cement;
- therefore **1 quarry level approximately feeds 1 Cement Works level** at baseline.

The numeric scale is consequently legible as an approximate local upper bound on baseline Cement Works supply. The broad nonzero footprint prevents a common geological input from becoming an artificial global choke point, while the 8–80 range preserves local scarcity, trade incentives, construction decisions, and headroom for later approved uses such as chemistry, glass, and metallurgical fluxes.

## Worldwide geological conclusion

Limestone, dolomite, chalk, marl, and other carbonate raw materials occur in sedimentary and fold-belt settings on every inhabited continent. Victoria 3's state-resource model therefore benefits from limestone being present in a very large fraction of states. Absence of a famous modern quarry is not evidence of geological absence.

The recommendation gives **674 of 675 states (99.85%)** a nonzero potential. This does not make states identical: 298 states are `LOW` or `MODEST`, 106 are `MEDIUM`, and 270 are `HIGH` or `VERY_HIGH`. The single zero is Iceland, where young basaltic/volcanic bedrock provides a materially stronger absence case than the mixed or incompletely documented geology found elsewhere. Even other volcanic islands retain `LOW` rather than zero when marine or reef carbonates may plausibly occur.

## Regional review

| Evidence region | States | Recommended conclusion |
|---|---:|---|
| British Isles | 13 | Very high chalk potential in southern/eastern England; high or medium in English/Welsh limestone belts; modest in more crystalline or mixed Irish/Scottish states. |
| France and Benelux | 24 | Paris/Anglo-Paris chalk and French carbonate basins justify high values; Belgian Paleozoic limestone is very strong; covered Dutch/Flemish lowlands are low. |
| Iberia | 18 | Widespread mapped limestone, dolomite, and marl; Castilian and Andalusian basins are the strongest, while western crystalline areas are moderate. |
| Atlantic volcanic islands | 4 | Volcanic dominance limits state-scale quarry potential; all remain low and review-required rather than receiving unsupported zeros. |
| Italy | 17 | Carbonate Alps, Apennines, and southern/island successions are strong; Po alluvium and crystalline/volcanic areas reduce selected states. |
| German states and Central Europe | 34 | Broad Alpine, Carpathian, and Mesozoic carbonate belts support medium/high values; northern cover and basin states are lower. |
| Scandinavia and North Atlantic | 21 | Danish chalk, Gotland, and Scania contrast with shield/igneous terrain; Greenland is low and Iceland is the sole zero. |
| Balkans | 25 | Extensive Dinaric and Hellenic karst makes this one of the world's strongest continuous carbonate regions. |
| Poland and Baltic | 21 | Polish limestone/marl/chalk districts are medium/high; Baltic and northern covered states are low/modest. |
| Russia and Ukraine | 34 | Platform carbonates support widespread modest potential, with higher values in Ukraine, Crimea, Volga, and southern sedimentary belts. |
| Anatolia and Caucasus | 19 | Extensive folded marine carbonate sequences justify consistently high potential, subject to later state-level verification. |
| Middle East | 29 | Arabian platform, Levant, and Zagros carbonates are abundant; alluvial and sand-covered areas are reduced. |
| North Africa | 22 | Atlas, Mediterranean, Egyptian, and Libyan carbonate strata are widespread; Saharan cover and crystalline massifs reduce interior values. |
| Sahel and Nile transition | 10 | Local carbonate basins exist, but coarse mapping, shield terrain, dunes, and alluvium produce low/modest review-required values. |
| Sub-Saharan Africa | 60 | Carbonate resources are widespread but discontinuous across large shields; South African, East African coastal, and selected Congo/Madagascar provinces are stronger. |
| India | 26 | Government inventories support high and very high capacity in western, central, and southern cement-limestone states; delta/alluvial states are lower. |
| China | 38 | Southwest karst is very high; northern carbonate provinces are high; deltas, deserts, loess-covered, and plateau states are lower. |
| Japan and Korea | 16 | Carbonates are meaningful but discontinuous amid volcanic, plutonic, and metamorphic geology, so values are mainly modest. |
| Southeast Asia | 15 | Major karst belts from Burma through Indochina and Malaya support medium/high potential; deltas and granitic uplands are lower. |
| Indonesia and Philippines | 17 | Official Indonesian evidence shows broad limestone distribution, with high values on major carbonate-bearing islands and lower values in selected volcanic/covered areas. |
| Australia and New Zealand | 9 | Nullarbor and Canterbury are strong; other sedimentary provinces are medium and volcanic/crystalline areas modest. |
| North America | 61 | Central/eastern US and Canadian sedimentary basins are high to very high; Shield, Pacific volcanic, Arctic, and small urban states are reduced. |
| Mexico, Central America and Caribbean | 31 | Yucatan and Greater Antillean carbonates are strong; Mexican belts are mixed; volcanic Central America is mostly low/modest. |
| Andes | 22 | Colombia and Peru have strongly documented industrial limestone; volcanic high Andes and Amazonian margins are reduced. |
| Brazil and Southern Cone | 31 | Carbonate basins and belts produce selected high values, but shields, Amazon cover, Pampas, and Patagonia keep the region mainly modest. |
| Central Asia and Himalaya | 27 | Carbonate-bearing orogenic belts are plausible, but coarse state units, desert/plateau cover, and access make every row review-required. |
| Siberia and Arctic | 20 | Platform carbonates exist, but permafrost, remoteness, shields, and volcanic arcs justify only low/modest review-required caps. |
| Pacific Islands | 11 | Reef or uplifted limestone can be locally important (especially Nauru), but small land area and volcanic basement justify conservative review-required values. |

## Distribution and confidence totals

### Potential classes

| Class | States | Share |
|---|---:|---:|
| `NONE` | 1 | 0.15% |
| `LOW` | 89 | 13.19% |
| `MODEST` | 209 | 30.96% |
| `MEDIUM` | 106 | 15.70% |
| `HIGH` | 222 | 32.89% |
| `VERY_HIGH` | 48 | 7.11% |
| **Total** | **675** | **100.00%** |

### Evidence status

| Evidence status | States |
|---|---:|
| `HIGH_CONFIDENCE` | 252 |
| `MEDIUM_CONFIDENCE` | 348 |
| `LOW_CONFIDENCE` | 74 |
| `ZERO_JUSTIFIED` | 1 |
| `NO_EVIDENCE` | 0 |
| **Total** | **675** |

`REVIEW_REQUIRED` totals **75**: 74 low-confidence rows plus Iceland's explicitly justified zero. The review queue is concentrated in the Atlantic and Pacific islands, Sahel/Nile transition, Central Asia/Himalaya, Siberia/Arctic, Greenland, and the Indian Ocean Territory. The matrix retains exact row-level reasons and source links for that follow-up.

## Principal source register

The complete URL set is repeated by evidence region in the regional evidence CSV and copied into every state row that relies on it. Principal sources include:

- Global/regional compilation: [OneGeology portal documentation](https://onegeology.github.io/documentation/using/portal.html), [USGS World Geologic Maps](https://www.usgs.gov/centers/central-energy-resources-science-center/science/world-geologic-maps), [BGR OneGeology project](https://www.bgr.bund.de/EN/Themen/Sammlungen-Grundlagen/GG_geol_Info/Projekte/abgeschlossen/OneGeology/onegeology_inhalt_en.html).
- Europe: [BGS Chalk aquifer map](https://www2.bgs.ac.uk/groundwater/shaleGas/aquifersAndShales/maps/aquifers/Chalk.html), [BRGM France lithological map](https://www.brgm.fr/fr/reference-projet-acheve/premiere-version-carte-lithologique-france-metropolitaine-au-150-000e), [IGME Spain lithological legend](https://mapas.igme.es/gis/rest/services/oneGeology/IGME_EN_Geology/MapServer/legend), [ISPRA Italian geological maps](https://www.isprambiente.gov.it/en/databases/data-base-collection/soil-and-territory/geological-and-geotematics-map), [BGR Germany GÜK250](https://www.bgr.bund.de/DE/Themen/Sammlungen-Grundlagen/GG_geol_Info/Karten/Deutschland/GUEK250/guek250_inhalt.html?nn=1840614), [Polish Geological Institute mineral-resource maps](https://www.pgi.gov.pl/en/mineral-resources/maps/), [EuroGeoSurveys GEMAS calcium mapping](https://gemas.eurogeosurveys.org/image/GEMAS_Brochure.pdf).
- Africa and Middle East: [BRGM Geological Map of Africa](https://www.brgm.fr/en/reference-completed-project/new-edition-110000000-geological-map-africa), [BRGM African hydrogeology synthesis](https://infoterre.brgm.fr/rapports/RP-54404-FR.pdf), [Council for Geoscience South Africa downloadable maps](https://www.geoscience.org.za/cgs/systems/publications/downloadable-material/), [USGS Arabian Peninsula map](https://www.usgs.gov/maps/geologic-map-arabian-peninsula), [Egyptian Mineral Resources Authority maps](https://emra.gov.eg/ca/geological-maps), [Morocco geoscientific map portal](https://cartesgeoscientifiques.mem.gov.ma/?tc=gp).
- South and East Asia: [Indian Bureau of Mines Limestone 2018](https://ibm.gov.in/writereaddata/files/08062019095529Limestone_2018.pdf), [China Geological Survey southwest karst](https://en.cgs.gov.cn/Achievement/tci/gws/201603/t20160309_265903.html), [China Geological Survey northern karst](https://en.cgs.gov.cn/Achievement/tci/gws/201603/t20160309_266042.html), [Geological Survey of Japan online map](https://www.gsj.jp/en/education/geomap-e/online-geological-map-of-japan/index.html), [KIGAM Korea geological map](https://data.kigam.re.kr/data/d1a66b54-0541-4830-9b7f-0ea847430643?lang=en), [China Geological Survey Southeast Asia compilation](https://en.cgs.gov.cn/achievements/201601/t20160112_35416.html), [Geological Agency of Indonesia 2024 report](https://geologi.esdm.go.id/storage/publikasi/kcVEQXADi0eq4J94sT1N1Ri8BgnURtxdEFTrvwO7.pdf).
- Australasia: [Geoscience Australia geological provinces](https://services.ga.gov.au/gis/rest/services/Australian_Geological_Provinces/MapServer), [Geoscience Australia landforms and Nullarbor](https://www.ga.gov.au/scientific-topics/national-location-information/landforms/australian-landforms-and-their-history), [GNS New Zealand 1:1M geology](https://gis.gns.cri.nz/server/rest/services/Geological_Map_of_New_Zealand_1_Million/NZL_GNS_1M_geology_FeatureService/MapServer/4), [GNS QMAP](https://www.gns.cri.nz/data-and-resources/digital-qmap-geological-maps-at-1250000/).
- Americas: [USGS natural aggregates map](https://www.usgs.gov/publications/natural-aggregates-conterminous-united-states), [Natural Resources Canada major rock categories](https://geoappext.nrcan.gc.ca/arcgis/rest/services/MMS/GMRC_E/MapServer/0), [Servicio Geológico Mexicano GeoInfoMex](https://www.sgm.gob.mx/GeoInfoMexGobMx/), [USGS Greater Antilles map](https://www.usgs.gov/maps/geologic-map-greater-antilles-and-virgin-islands), [Servicio Geológico Colombiano limestone report](https://www2.sgc.gov.co/Publicaciones/Cientificas/NoSeriadas/Documents/Caliza-en-Colombia-geologia.PDF), [INGEMMET Peru limestone layer](https://geocatmin.ingemmet.gob.pe/arcgis/rest/services/SERV_ROCAS_MINERALES_INDUSTRIALES/MapServer/17), [Geological Survey of Brazil national map](https://rigeo.sgb.gov.br/items/32bb9679-e245-49d8-ba89-3fd9d68b59ea), [SEGEMAR Argentina industrial-mineral mapping](https://repositorio.segemar.gov.ar/bitstream/handle/308849217/2825/CMIRyG_2766II_SM_Tucuman_M.pdf?isAllowed=y&sequence=1).
- Former Soviet Union and North Atlantic: [USGS Former Soviet Union geology](https://pubs.usgs.gov/publication/ofr97470E), [Iceland geological maps](https://www.ni.is/en/resources/publications/maps/geological-maps), [GEUS Greenland geological maps](https://dataverse.geus.dk/dataverse/geological_maps_greenland%3Bjsessionid%3D151af2eba7d729abaef59babbf5c.proddataverse02?order=asc&page=1&q=&sort=nameSort&types=files).

## Proposed TECH6C2B gameplay footprint

TECH6C2B should implement the approved matrix by adding `building_limestone_quarry = <candidate_limestone_potential>` only to the following existing state-region files:

1. `map_data/state_regions/00_west_europe.txt`
2. `map_data/state_regions/01_south_europe.txt`
3. `map_data/state_regions/02_east_europe.txt`
4. `map_data/state_regions/03_north_africa.txt`
5. `map_data/state_regions/04_subsaharan_africa.txt`
6. `map_data/state_regions/05_north_america.txt`
7. `map_data/state_regions/06_central_america.txt`
8. `map_data/state_regions/07_south_america.txt`
9. `map_data/state_regions/08_middle_east.txt`
10. `map_data/state_regions/09_central_asia.txt`
11. `map_data/state_regions/10_india.txt`
12. `map_data/state_regions/11_east_asia.txt`
13. `map_data/state_regions/12_indonesia.txt`
14. `map_data/state_regions/13_australasia.txt`
15. `map_data/state_regions/14_siberia.txt`
16. `map_data/state_regions/15_russia.txt`

No goods, buildings, PMs, PMGs, technologies, laws, localization, GUI, country history, or starting-technology file is proposed for TECH6C2B. Before implementation, the 75 review-required rows should be accepted, revised, or explicitly waived; TECH6C2B must also preserve existing resources byte-for-byte except for the new limestone cap entries.

## Static quality controls

- Baseline identities are preserved: 675 rows in and 675 unique state IDs out.
- Every nonzero row has a regional geological rationale, evidence status, evidence region, and source URL set.
- The sole zero has an explicit state-level justification.
- Every evidence status and implementation status is from the permitted vocabulary.
- Numeric potentials are restricted to `0, 8, 16, 28, 48, 80` and match their named classes.
- The regional evidence register covers all 28 region names used by the global matrix.
- No `map_data/state_regions` file or other gameplay file was edited by TECH6C2A.

## Required phase summary

```text
TECH6C2A_LIMESTONE_GLOBAL_DISTRIBUTION_AUDIT = PASS

BRANCH = tech6c-goods-buildings-pm-implementation

BASELINE_STATES = 675
OUTPUT_STATES = 675
MISSING_STATES = 0
DUPLICATE_STATES = 0

POTENTIAL_NONE = 1
POTENTIAL_LOW = 89
POTENTIAL_MODEST = 209
POTENTIAL_MEDIUM = 106
POTENTIAL_HIGH = 222
POTENTIAL_VERY_HIGH = 48

HIGH_CONFIDENCE = 252
MEDIUM_CONFIDENCE = 348
LOW_CONFIDENCE = 74
REVIEW_REQUIRED = 75

NUMERIC_SCALE =
- LOW = 8
- MODEST = 16
- MEDIUM = 28
- HIGH = 48
- VERY_HIGH = 80

GAMEPLAY_FILES_CHANGED = 0
STATE_REGION_FILES_CHANGED = 0

STATIC_DOCUMENT_VALIDATION = PASS

COMMIT = NO
PUSH = NO

NEXT_PHASE = TECH6C2B_LIMESTONE_RESOURCE_DISTRIBUTION_IMPLEMENTATION
NEXT_PHASE_READY = YES
```
