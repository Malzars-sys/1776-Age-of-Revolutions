# BUILD START 1776 — Recherche historique — Amériques et Caraïbes

**Date absolue : 1776-01-01. Recherche uniquement. Aucun fichier gameplay modifié, aucun code, commit ou push.**

## 1. Périmètre et méthode

- **188 instances `Owner_TAG + State_ID`** examinées dans `R8_NORTH_AMERICA_CARIBBEAN` et `R9_SOUTH_AMERICA`.
- Les lignes d'un même `State_ID` sous des propriétaires différents sont conservées séparément.
- Aucune ligne VEN/GEN n'entre dans ce périmètre américain.
- Seuls les bâtiments du catalogue marqués pertinents pour la recherche 1776 et plaçables manuellement sont utilisés.
- Les activités domestiques, artisanales isolées ou de faible densité restent abstraites ; la matrice ne contient que des recommandations positives.
- `building_railway` est exclusivement le réseau terrestre régional unifié : **routes/canaux seulement, `pm_no_rail_network` obligatoire**.
- Un bâtiment historiquement justifié n'est pas supprimé pour une porte technologique absente : le conflit apparaît dans `Tech_Distribution_Review`.

## 2. Principes de calibration retenus

Les niveaux 1–2 sont volontairement dominants. Les niveaux 3+ sont réservés aux concentrations dont l'importance dépasse clairement le cadre local : Chesapeake tobacco, South Carolina rice, Jamaica/Saint-Domingue sugar, Havana naval complex, Veracruz/Cartagena/Rio de Janeiro as imperial ports, Minas Gerais gold, and Buenos Aires cattle/hides. Les centres de commerce sont plus conservateurs encore : un port n'en reçoit pas automatiquement un.

## 3. Diagnostic régional — Amérique du Nord britannique et Treize Colonies

La matrice distingue les économies exportatrices spécialisées : tabac du Chesapeake, riz/indigo du Lowcountry, grains du Mid-Atlantic, pêche/bois/construction navale de la Nouvelle-Angleterre. Philadelphie reçoit plusieurs manufactures de niveau 1–2 parce que les papeteries et ateliers y formaient une concentration exceptionnelle pour l'Amérique britannique ; les colonies de frontière restent largement sans bâtiments spécialisés.

## 4. Canada et Atlantique nord

Terre-Neuve est traitée comme un cas exceptionnel de pêche commerciale : l'industrie britannique atteint un sommet dans les années 1760–1775. Québec reçoit le noyau portuaire, marchand et administratif du Saint-Laurent. Les postes HBC ne sont pas convertis en une constellation de centres de commerce : seuls les principaux nœuds sont retenus au niveau 1.

## 5. Caraïbes

La hiérarchie plantation/commerce est fortement asymétrique : Jamaica et Saint-Domingue sont les plus fortes concentrations sucrières ; Cuba reste pré-boom sucrier au 1er janvier 1776 mais La Havane constitue déjà un complexe naval et portuaire majeur. St Eustatius justifie exceptionnellement un centre de commerce de niveau 3 comme free port/entrepôt. Porto Rico est surtout traité comme place fortifiée et garnison avec agriculture commerciale plus modeste.

## 6. Nouvelle-Espagne et Amérique centrale

Mexico, Veracruz et Acapulco structurent respectivement l'administration/marché intérieur, la façade atlantique et la liaison transpacifique. Le Camino Real justifie des niveaux routiers ciblés. Les grands districts argentifères de Guanajuato/Zacatecas sont **explicitement non convertis en `building_gold_mine`** : l'absence de bâtiment argent dans le catalogue ne doit pas produire une fausse implantation.

## 7. Amérique du Sud

Minas Gerais reçoit la plus forte concentration minière aurifère. Rio de Janeiro est le principal port d'import-export de l'économie minière et capitale depuis 1763. Pernambuco/Bahia restent de grands centres sucriers. Cartagena, Lima-Callao et Buenos Aires forment d'autres nœuds commerciaux majeurs, mais avec des fonctions différentes. Potosí est représenté par son commerce/administration/infrastructure, **pas par une mine d'or**. Le Río de la Plata est calibré autour du bétail, des cuirs et de la circulation intérieure plutôt que d'une industrialisation inexistante.

## 8. Centres de commerce retenus

| Owner | State | Level | Rationale |
|---|---|---:|---|
| BRZ | STATE_RIO_DE_JANEIRO — Rio de Janeiro | 3 | Port/trade/admin level 3; roads/shipyard 2; other sectors 1. |
| HAI | STATE_HAITI — Haiti | 3 | Level 3 reflects exceptional plantation/export concentration. |
| NET | STATE_WEST_INDIES — West Indies | 3 | Trade level 3 is exceptional but justified by the dense warehouse/free-port system. |
| SC1 | STATE_VERACRUZ — Veracruz | 3 | Port/trade level 3; road level 2; crops/fortification 1–2. |
| SC2 | STATE_BOLIVAR — Bolívar | 3 | Port/trade/fortification level 3; administration 2; garrison/shipyard 1. |
| SC3 | STATE_LIMA — Lima | 3 | Administration/trade 3; port/fortification/roads 2; institutions/manufactures 1. |
| BRZ | STATE_BAHIA — Bahia | 2 | Level 2, with Pernambuco/Bahia above secondary captaincies. |
| BRZ | STATE_PERNAMBUCO — Pernambuco | 2 | Level 2, with Pernambuco/Bahia above secondary captaincies. |
| CUB | STATE_WESTERN_CUBA — Western Cuba | 2 | Shipyard/port exceptionally high; other imperial functions level 1–2. |
| FRA | STATE_WEST_INDIES — West Indies | 2 | Level 2; kept below named exceptional hubs. |
| GBR | STATE_JAMAICA — Jamaica | 2 | Sugar level 4, port/trade 2; coffee/fort/admin 1. |
| GBR | STATE_NEWFOUNDLAND — Newfoundland | 2 | Fishing level 4; port/trade level 2. |
| GBR | STATE_WEST_INDIES — West Indies | 2 | Level 2; kept below named exceptional hubs. |
| NET | STATE_GUAYANA — Guyana | 2 | Level 2. |
| QUE | STATE_QUEBEC — Quebec | 2 | Port/trade/admin level 2; other sectors level 1. |
| SC1 | STATE_GUERRERO — Guerrero | 2 | Level 2 port/trade; level 1 road link. |
| SC1 | STATE_MEXICO — México | 2 | Level 3 administration, level 2 trade/roads/textiles, level 1 other sectors. |
| SC2 | STATE_MIRANDA — Miranda | 2 | Level 2. |
| SC2 | STATE_PANAMA — Panama | 2 | Port/trade/fort level 2; road level 1. |
| SC4 | STATE_BUENOS_AIRES — Buenos Aires | 2 | Ranching level 3, port/trade 2. |
| USA | STATE_MASSACHUSETTS — Massachusetts | 2 | Level 2 reflects a major colonial commercial hub. |
| USA | STATE_NEW_YORK — New York | 2 | Level 2 only for port/trade/grain; other sectors level 1. |
| USA | STATE_PENNSYLVANIA — Pennsylvania | 2 | Level 2 for nationally prominent sectors; firearms remains REVIEW at level 1. |
| USA | STATE_SOUTH_CAROLINA — South Carolina | 2 | Rice level 3, indigo/port/trade level 2. |
| BRZ | STATE_MARANHAO — Maranhão | 1 | Conservative level 1 at the 1776 cutoff. |
| BRZ | STATE_PARA — Pará | 1 | Level 1 only. |
| BRZ | STATE_PARAIBA — Paraíba | 1 | Level 1, with Pernambuco/Bahia above secondary captaincies. |
| BRZ | STATE_RIO_GRANDE_DO_NORTE — Rio Grande do Norte | 1 | Level 1, with Pernambuco/Bahia above secondary captaincies. |
| BRZ | STATE_SAO_PAULO — São Paulo | 1 | Level 1 only. |
| DENNOR | STATE_WEST_INDIES — West Indies | 1 | Level 1; kept below named exceptional hubs. |
| FRA | STATE_GUAYANA — Guyana | 1 | Level 1 only. |
| GBR | STATE_BAHAMAS — Bahamas | 1 | Level 2 only for salt extraction. |
| GBR | STATE_BERMUDA — Bermuda | 1 | Level 1 each. |
| GBR | STATE_FLORIDA — Florida | 1 | Level 1 only. |
| GR5 | STATE_SANTO_DOMINGO — Santo Domingo | 1 | Level 1 only. |
| HBC | STATE_MANITOBA — Manitoba | 1 | One level only because a V3 trade center is already substantial. |
| HBC | STATE_ONTARIO — Ontario | 1 | One level only because a V3 trade center is already substantial. |
| LOU | STATE_LOUISIANA — Louisiana | 1 | Level 1: substantial regionally but not yet a top Atlantic entrepôt. |
| NVS | STATE_NEW_BRUNSWICK — Maritimes | 1 | Conservative 1–2 levels. |
| PCO | STATE_PUERTO_RICO — Porto Rico | 1 | Level 1 is conservative. |
| SC1 | STATE_GUATEMALA — Guatemala | 1 | Level 1 only. |
| SC1 | STATE_SAN_SALVADOR — San Salvador | 1 | Indigo level 2; other sectors 1. |
| SC1 | STATE_YUCATAN — Yucatán | 1 | Level 1 only. |
| SC2 | STATE_CUNDINAMARCA — Cundinamarca | 1 | Level 1. |
| SC2 | STATE_ECUADOR — Ecuador | 1 | Textile level 2; admin/trade 1. |
| SC2 | STATE_ZULIA — Zulia | 1 | Level 1 only. |
| SC3 | STATE_AREQUIPA — Arequipa | 1 | Level 1. |
| SC3 | STATE_ICA — Ica | 1 | Level 1. |
| SC3 | STATE_POTOSI — Potosí | 1 | Level 1; silver extraction itself is intentionally not represented by building_gold_mine. |
| SC3 | STATE_SANTIAGO — Santiago | 1 | Level 1. |
| SC4 | STATE_URUGUAY — Uruguay | 1 | Level 1. |
| SPA | STATE_WEST_INDIES — West Indies | 1 | Level 1; kept below named exceptional hubs. |
| USA | STATE_GEORGIA — Georgia | 1 | Conservative level 1. |
| USA | STATE_MAINE — Maine | 1 | Level 1 reflects regional specialization rather than a single establishment. |
| USA | STATE_MARYLAND — Maryland | 1 | Tobacco warrants level 3; other organized sectors remain 1. |
| USA | STATE_NEW_HAMPSHIRE — New Hampshire | 1 | Level 1 reflects regional specialization rather than a single establishment. |
| USA | STATE_NORTH_CAROLINA — North Carolina | 1 | Conservative level 1. |
| USA | STATE_RHODE_ISLAND — Rhode Island | 1 | Conservative level 1. |
| USA | STATE_VIRGINIA — Virginia | 1 | Tobacco level 4; Norfolk/Chesapeake port capacity level 2. |

## 9. Infrastructure régionale

Toutes les lignes `building_railway` portent dans `Notes` leur justification routes/canaux. Aucun rail actif n'est recommandé. Les canaux ne sont retenus positivement que pour la Guyane néerlandaise/Suriname, où le système de plantations dépendait de voies d'eau et canaux ; ailleurs les grands ouvrages hydrauliques spécialisés (par exemple Potosí) ne sont pas automatiquement assimilés à un réseau régional de canaux.

## 10. Principales concentrations de bâtiments positifs

| Owner | State | Positive rows |
|---|---|---:|
| CUB | STATE_WESTERN_CUBA | 11 |
| USA | STATE_PENNSYLVANIA | 11 |
| USA | STATE_MASSACHUSETTS | 9 |
| SC1 | STATE_MEXICO | 8 |
| USA | STATE_NEW_YORK | 8 |
| USA | STATE_VIRGINIA | 8 |
| SC3 | STATE_LIMA | 8 |
| PCO | STATE_PUERTO_RICO | 7 |
| USA | STATE_MARYLAND | 7 |
| USA | STATE_SOUTH_CAROLINA | 7 |
| BRZ | STATE_RIO_DE_JANEIRO | 7 |
| NET | STATE_GUAYANA | 7 |
| SC3 | STATE_SANTIAGO | 7 |
| GBR | STATE_JAMAICA | 6 |
| HAI | STATE_HAITI | 6 |
| NVS | STATE_NEW_BRUNSWICK | 6 |
| QUE | STATE_QUEBEC | 6 |
| SC1 | STATE_VERACRUZ | 6 |
| USA | STATE_CONNECTICUT | 6 |
| USA | STATE_MAINE | 6 |

## 11. IMPORTANT_NON_RECOMMENDATIONS

| State | Industry | Decision | Reason | Source |
|---|---|---|---|---|
| USA / STATE_DISTRICT_OF_COLUMBIA | all ordinary specialized buildings | NO_BUILDING | The District of Columbia did not exist as a federal district on 1776-01-01; do not import Washington-era institutions into this state slot. | https://www.archives.gov/founding-docs/constitution-transcript |
| ALK / STATE_ALASKA | Russian colonial port/trade/shipyard | NO_BUILDING | The first permanent Russian settlement in Alaska dates to 1784, after the cutoff. | https://www.nps.gov/articles/000/russian-america.htm |
| HAW / STATE_HAWAIIAN_ISLANDS | sandalwood export / large trade center | NO_BUILDING | The large sandalwood export economy belongs to the post-contact late-18th/early-19th century, not 1776-01-01. | https://www.nps.gov/puhe/learn/historyculture/sandalwood-trade.htm |
| GBR / STATE_SOUTH_ATLANTIC_ISLANDS | British port/garrison | NO_BUILDING | Port Egmont was abandoned by Britain in 1774; a normal active British starting port/garrison in 1776 would be misleading. | https://www.britannica.com/place/Falkland-Islands/History |
| SC1 / STATE_BAJIO | silver mine represented as building_gold_mine | NO_BUILDING | Guanajuato's major mining output was silver; the catalog's gold mine must not be repurposed as a generic precious-metal mine. | https://whc.unesco.org/en/list/482 |
| SC1 / STATE_ZACATECAS | silver mine represented as building_gold_mine | NO_BUILDING | Zacatecas was a major silver-mining centre; no matching silver-mine Building_ID is supplied in the allowed catalog. | https://whc.unesco.org/en/list/676 |
| SC3 / STATE_POTOSI | building_gold_mine | NO_BUILDING | Potosí's industrial complex was overwhelmingly silver. The positive matrix represents its supporting trade/admin/road capacity, not a fake gold mine. | https://whc.unesco.org/en/list/420 |
| R9 South America | building_machu_picchu | NO_BUILDING | The catalog contains building_machu_picchu, but the supplied American Owner_TAG + State_ID partition contains no matching Cusco state instance. No State_ID is invented. | https://whc.unesco.org/en/list/274 |
| all American states | active railway PM | NO_BUILDING | building_railway is used only as the fork's regional road/canal infrastructure. Every recommendation retains pm_no_rail_network at start. |  |
| ABS / STATE_MONTANA (Montana) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ABS / STATE_WYOMING (Wyoming) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ALK / STATE_ALASKA (Alaska) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| AP7 / STATE_ACRE (Acre) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| AP7 / STATE_AMAZONAS (Amazonas) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| AP7 / STATE_GUAYANA (Guyana) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| AP7 / STATE_LA_PAZ (La Paz) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| AP7 / STATE_MATO_GROSSO (Mato Grosso) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| APC / STATE_ARIZONA (Arizona) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| APC / STATE_CALIFORNIA (California) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| APC / STATE_NEW_MEXICO (New Mexico) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ARP / STATE_COLORADO (Colorado) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ARP / STATE_WYOMING (Wyoming) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ATB / STATE_ALASKA (Alaska) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ATB / STATE_BRITISH_COLUMBIA (Northern Columbia) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ATB / STATE_NORTHWEST_TERRITORIES (Northwest Territories) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ATB / STATE_NUNAVUT (Nunavut) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ATB / STATE_OREGON (Oregon) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ATB / STATE_WASHINGTON (Southern Columbia) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ATB / STATE_YUKON_TERRITORY (Yukon Territory) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| BLF / STATE_ALBERTA (Alberta) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| BLF / STATE_MONTANA (Montana) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| BNN / STATE_IDAHO (Idaho) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| BNN / STATE_NEVADA (Nevada) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| BNN / STATE_WYOMING (Wyoming) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| BRZ / STATE_PARANA (Paraná) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| COM / STATE_ALABAMA (Alabama) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| COM / STATE_ARKANSAS (Arkansas) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| COM / STATE_KANSAS (Kansas) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| COM / STATE_KENTUCKY (Kentucky) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| COM / STATE_MISSISSIPPI (Mississippi) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| COM / STATE_MISSOURI (Missouri) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| COM / STATE_NEW_MEXICO (New Mexico) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| COM / STATE_OKLAHOMA (Oklahoma) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| COM / STATE_TENNESSEE (Tennessee) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| COM / STATE_TEXAS (Texas) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| GBR / STATE_GUATEMALA (Guatemala) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| GBR / STATE_SOUTH_ATLANTIC_ISLANDS (South Atlantic Islands) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| GNI / STATE_ALTO_PARAGUAY (Alto Paraguay) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| GNI / STATE_CHACO (Chaco) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| GNI / STATE_SANTA_FE (Santa Fe) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| HAW / STATE_HAWAIIAN_ISLANDS (Hawaiian Islands) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| HBC / STATE_NUNAVUT (Nunavut) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| HBC / STATE_QUEBEC (Quebec) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| HBC / STATE_SASKATCHEWAN (Saskatchewan) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| IQU / STATE_ICA (Ica) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| IRC / STATE_ALBERTA (Alberta) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| IRC / STATE_MANITOBA (Manitoba) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| IRC / STATE_SASKATCHEWAN (Saskatchewan) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| LKT / STATE_IOWA (Iowa) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| LKT / STATE_MINNESOTA (Minnesota) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| LKT / STATE_MONTANA (Montana) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| LKT / STATE_NEBRASKA (Nebraska) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| LKT / STATE_NORTH_DAKOTA (North Dakota) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| LKT / STATE_SOUTH_DAKOTA (South Dakota) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| LKT / STATE_WYOMING (Wyoming) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| MICC / STATE_ILLINOIS (Illinois) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| MICC / STATE_INDIANA (Indiana) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| MICC / STATE_MICHIGAN (Michigan) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| MICC / STATE_OHIO (Ohio) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| MICC / STATE_WISCONSIN (Wisconsin) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| MKT / STATE_NICARAGUA (Nicaragua) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| NVJ / STATE_ARIZONA (Arizona) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| NVJ / STATE_NEW_MEXICO (New Mexico) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| NVJ / STATE_UTAH (Utah) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| NZP / STATE_IDAHO (Idaho) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| ONT / STATE_ONTARIO (Ontario) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| PAT / STATE_BUENOS_AIRES (Buenos Aires) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| PAT / STATE_PATAGONIA (Patagonia) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| PAT / STATE_RIO_NEGRO (Mendoza) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| PWN / STATE_KANSAS (Kansas) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| PWN / STATE_NEBRASKA (Nebraska) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SC1 / STATE_BAJA_CALIFORNIA (Baja California) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SC1 / STATE_CHIAPAS (Chiapas) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SC1 / STATE_ZACATECAS (Zacatecas) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SC2 / STATE_GUAVIARE (Guaviare) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SC3 / STATE_ANTOFAGASTA (Antofagasta) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SC3 / STATE_ARAUCANIA (Araucania) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SC3 / STATE_PASTAZA (Pastaza) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SC3 / STATE_TARAPACA (Tarapacá) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SC4 / STATE_CHACO (Chaco) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SLK / STATE_ARAUCANIA (Araucania) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SLS / STATE_MONTANA (Montana) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SLS / STATE_WYOMING (Wyoming) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| SML / STATE_FLORIDA (Florida) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| THL / STATE_ARAUCANIA (Araucania) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| THL / STATE_PATAGONIA (Patagonia) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| USA / STATE_DISTRICT_OF_COLUMBIA (District of Columbia) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| USA / STATE_WEST_VIRGINIA (West Virginia) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| UTE / STATE_COLORADO (Colorado) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |
| UTE / STATE_UTAH (Utah) | ordinary specialized starting building | NO_BUILDING | No organized sector above the Victoria-3 level-1 threshold was established from the evidence used in this pass; subsistence, household craft, mobile trade or low-density extraction remains abstracted. |  |

## 12. Contrôle final

- STATES COVERED = **188**
- POSITIVE BUILDING ROWS = **388**
- TRADE CENTERS = **59**
- LEVEL 1 = **250**
- LEVEL 2 = **105**
- LEVEL 3 = **27**
- LEVEL 4-5 = **6**
- LEVEL 6+ = **0**
- TECH_DISTRIBUTION_REVIEW = **125**
- REVIEW CASES = **2**
- SERENISSIMA STATES SKIPPED = **0 in the American partition**

### Validation technique

- Tous les `Owner_TAG + State_ID` des lignes positives existent dans le catalogue d'État fourni.
- Tous les `Building_ID` existent dans le catalogue et appartiennent au filtre de recherche 1776.
- Aucun bâtiment auto-généré / `NO_ENGINE_GENERATED` n'est proposé.
- Aucun rail actif n'est proposé.
- Les conflits de technologie sont signalés, jamais utilisés pour supprimer une capacité historiquement retenue.
