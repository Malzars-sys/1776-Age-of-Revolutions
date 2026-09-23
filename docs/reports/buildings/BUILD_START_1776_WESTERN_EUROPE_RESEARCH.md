# BUILD START 1776 — Europe occidentale — Recherche historique régionale

**Date absolue : 1776-01-01**

Recherche uniquement. Aucun fichier gameplay modifié, aucun code produit, aucun commit/push.

## 1. Périmètre

Unité de recherche : **Owner_TAG + State_ID**. Les États partagés restent donc séparés. Le périmètre historique conservé est celui de la recherche Europe occidentale précédente : GBR, FRA, NET, BEO, LUX, IREK, SPA et POR dans la partition cartographique `R1_WESTERN_EUROPE`.

- Instances Owner_TAG + State_ID couvertes : **64**.
- `BEL` et `SPC` n'ont pas d'instance d'État propriétaire dans cette partition actuelle et ne génèrent donc aucune ligne bâtiment.
- Aucune possession `VEN` ou `GEN` n'est recommandée.
- Les lignes potentiellement partagées (par exemple Gelre, Wallonia, Balearic Islands, Upper Andalusia) restent distinctes par propriétaire.

## 2. Sources et méthode

Seuls les bâtiments autorisés par le catalogue pour la recherche de départ 1776 ont été utilisés. Aucun bâtiment auto-généré ou `NO_ENGINE_GENERATED` n'est proposé. Un niveau représente une capacité agrégée d'État, pas nécessairement une usine unique.

Les niveaux ont été calibrés conservativement : 1 = secteur organisé identifiable ; 2 = industrie/activité régionale importante ; 3 = grand centre national ; 4–5 = concentration internationale exceptionnelle. Aucun niveau 6+ n'est utilisé.

Les centres de commerce ont été recherchés séparément des ports. Ils ne sont proposés que pour des places marchandes/entrepôts à fonction régionale, nationale ou internationale démontrable.

`building_railway` est utilisé uniquement comme **infrastructure régionale unifiée**. Toutes ses lignes conservent `pm_no_rail_network`; les justifications ROAD/CANAL figurent dans `Notes`.

Si le bâtiment ou son canal historiquement justifié exige une technologie absente de la distribution actuelle, la recommandation reste dans la matrice avec `Tech_Distribution_Review = YES`.

## 3. Diagnostic régional

### Grande-Bretagne
Les concentrations les plus fortes sont Londres, Lancashire-Manchester/Liverpool, Yorkshire-Sheffield, Midlands-Birmingham et le bassin minier du West Country/Wales. L'avance britannique est surtout visible dans les textiles mécanisants, le charbon, les métaux, les outils, les dockyards et les réseaux de transport pré-ferroviaires. Londres est l'un des rares cas justifiant un centre de commerce niveau 4.

### France
Le profil français est plus polycentrique : Paris pour administration et consommation, Bordeaux/Nantes/Marseille pour le grand commerce, Lyon pour la soie, Normandie et Languedoc pour les textiles, Saint-Étienne/nord pour charbon et armement, et plusieurs arsenaux royaux. Le Canal du Midi justifie explicitement une capacité canal en Languedoc.

### Provinces-Unies et Pays-Bas méridionaux
Holland/Amsterdam reste une concentration mondiale exceptionnelle de commerce, ports, shipyards et canaux. Flandres et Wallonie ont des profils très différents : textile/commerce/roads en Flandres, charbon-métaux-armes-verre en Wallonie.

### Irlande
Dublin est le principal pôle administratif/commercial ; Cork/Munster se distingue par les provisions et le beurre exporté ; Ulster par le lin. Le Grand Canal n'est pas traité comme réseau opérationnel au cutoff.

### Espagne
Le poids des arsenaux de Ferrol, Cádiz/La Carraca et Cartagena est conservé. Barcelone/Catalogne reçoit la plus forte concentration textile espagnole ; Valencia la soie ; Cádiz un grand centre de commerce ; La Granja/Segovia des manufactures royales spécialisées.

### Portugal
Lisbonne concentre port, commerce, arsenal et administration ; Porto/Douro le vin d'exportation ; Madeira et les Açores des économies atlantiques spécialisées ; Coimbra justifie l'université. Le monument proposé à Sintra est uniquement `building_pena_convent`, pas le palais du XIXe siècle.

## 4. Matrice positive

| Owner | State | Building | Level | Conf. | Tech review | Rôle |
|---|---|---|---:|---|---|---|
| GBR | STATE_BALEARIC_ISLANDS | `building_barrack` | 1 | MEDIUM | YES | MILITARY_GARRISON |
| GBR | STATE_BALEARIC_ISLANDS | `building_naval_fortification` | 1 | MEDIUM | YES | NAVAL_DEFENCE |
| GBR | STATE_EAST_ANGLIA | `building_port` | 1 | MEDIUM | YES | COASTAL_COMMERCE |
| GBR | STATE_EAST_ANGLIA | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| GBR | STATE_EAST_ANGLIA | `building_textile_mill` | 2 | MEDIUM | NO | WOOL_TEXTILES |
| GBR | STATE_EAST_ANGLIA | `building_wheat_farm` | 2 | MEDIUM | NO | COMMERCIAL_AGRICULTURE |
| GBR | STATE_HIGHLANDS | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| GBR | STATE_HIGHLANDS | `building_livestock_ranch` | 2 | MEDIUM | NO | COMMERCIAL_LIVESTOCK |
| GBR | STATE_HIGHLANDS | `building_logging_camp` | 2 | MEDIUM | NO | TIMBER_EXTRACTION |
| GBR | STATE_HIGHLANDS | `building_port` | 1 | MEDIUM | YES | COASTAL_PORT |
| GBR | STATE_HOME_COUNTIES | `building_arms_industry` | 2 | MEDIUM | NO | STATE_ARMAMENT |
| GBR | STATE_HOME_COUNTIES | `building_artillery_foundry` | 2 | MEDIUM | NO | STATE_ARTILLERY |
| GBR | STATE_HOME_COUNTIES | `building_barrack` | 2 | MEDIUM | YES | MILITARY_GARRISON |
| GBR | STATE_HOME_COUNTIES | `building_construction_sector` | 2 | MEDIUM | YES | URBAN_CONSTRUCTION |
| GBR | STATE_HOME_COUNTIES | `building_food_industry` | 2 | MEDIUM | YES | URBAN_FOOD_PROCESSING |
| GBR | STATE_HOME_COUNTIES | `building_furniture_manufactory` | 2 | MEDIUM | YES | URBAN_MANUFACTURE |
| GBR | STATE_HOME_COUNTIES | `building_government_administration` | 3 | HIGH | NO | CAPITAL_ADMINISTRATION |
| GBR | STATE_HOME_COUNTIES | `building_naval_administration` | 2 | MEDIUM | YES | NAVAL_ADMINISTRATION |
| GBR | STATE_HOME_COUNTIES | `building_observatorygreenwich` | 1 | HIGH | NO | SCIENTIFIC_INSTITUTION |
| GBR | STATE_HOME_COUNTIES | `building_paper_mill` | 1 | MEDIUM | YES | PRINT_SUPPLY |
| GBR | STATE_HOME_COUNTIES | `building_port` | 3 | HIGH | YES | OCEANIC_PORT |
| GBR | STATE_HOME_COUNTIES | `building_railway` | 3 | HIGH | NO | REGIONAL_TRANSPORT |
| GBR | STATE_HOME_COUNTIES | `building_shipyard` | 2 | MEDIUM | YES | NAVAL_SHIPBUILDING |
| GBR | STATE_HOME_COUNTIES | `building_trade_center` | 4 | HIGH | NO | GLOBAL_ENTREPOT |
| GBR | STATE_LANCASHIRE | `building_coal_mine` | 2 | MEDIUM | NO | FUEL_EXTRACTION |
| GBR | STATE_LANCASHIRE | `building_port` | 3 | HIGH | YES | OCEANIC_PORT |
| GBR | STATE_LANCASHIRE | `building_railway` | 2 | HIGH | YES | REGIONAL_TRANSPORT |
| GBR | STATE_LANCASHIRE | `building_textile_mill` | 4 | HIGH | NO | COTTON_TEXTILES |
| GBR | STATE_LANCASHIRE | `building_tooling_workshop` | 1 | MEDIUM | YES | INDUSTRIAL_TOOLS |
| GBR | STATE_LANCASHIRE | `building_trade_center` | 3 | HIGH | NO | ATLANTIC_TRADE |
| GBR | STATE_LOWLANDS | `building_coal_mine` | 2 | MEDIUM | NO | COAL_EXTRACTION |
| GBR | STATE_LOWLANDS | `building_port` | 2 | MEDIUM | YES | COMMERCIAL_PORT |
| GBR | STATE_LOWLANDS | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| GBR | STATE_LOWLANDS | `building_shipyard` | 1 | MEDIUM | YES | SHIPBUILDING |
| GBR | STATE_LOWLANDS | `building_textile_mill` | 2 | MEDIUM | NO | LINEN_WOOL_TEXTILES |
| GBR | STATE_LOWLANDS | `building_trade_center` | 2 | MEDIUM | NO | NATIONAL_TRADE_HUB |
| GBR | STATE_LOWLANDS | `building_university` | 1 | MEDIUM | NO | HIGHER_EDUCATION |
| GBR | STATE_MIDLANDS | `building_arms_industry` | 2 | MEDIUM | NO | ARMS_METALWARE |
| GBR | STATE_MIDLANDS | `building_coal_mine` | 2 | MEDIUM | NO | COAL_EXTRACTION |
| GBR | STATE_MIDLANDS | `building_glassworks` | 1 | MEDIUM | YES | GLASS_MANUFACTURE |
| GBR | STATE_MIDLANDS | `building_railway` | 2 | MEDIUM | YES | REGIONAL_TRANSPORT |
| GBR | STATE_MIDLANDS | `building_tooling_workshop` | 3 | MEDIUM | YES | METALWARE_TOOLS |
| GBR | STATE_UPPER_ANDALUSIA | `building_barrack` | 2 | HIGH | YES | FORTRESS_GARRISON |
| GBR | STATE_UPPER_ANDALUSIA | `building_naval_administration` | 1 | MEDIUM | YES | NAVAL_STATION |
| GBR | STATE_UPPER_ANDALUSIA | `building_naval_fortification` | 2 | MEDIUM | YES | NAVAL_FORTRESS |
| GBR | STATE_UPPER_ANDALUSIA | `building_port` | 2 | MEDIUM | YES | STRATEGIC_PORT |
| GBR | STATE_UPPER_ANDALUSIA | `building_trade_center` | 2 | HIGH | NO | MEDITERRANEAN_ENTREPOT |
| GBR | STATE_WALES | `building_coal_mine` | 3 | MEDIUM | NO | COAL_EXTRACTION |
| GBR | STATE_WALES | `building_iron_mine` | 2 | MEDIUM | NO | IRON_EXTRACTION |
| GBR | STATE_WALES | `building_port` | 1 | MEDIUM | YES | COASTAL_EXPORT |
| GBR | STATE_WALES | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| GBR | STATE_WALES | `building_tooling_workshop` | 1 | MEDIUM | YES | IRONWORKING |
| GBR | STATE_WEST_COUNTRY | `building_copper_mine` | 3 | HIGH | NO | COPPER_EXTRACTION |
| GBR | STATE_WEST_COUNTRY | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| GBR | STATE_WEST_COUNTRY | `building_naval_administration` | 2 | MEDIUM | YES | NAVAL_ADMINISTRATION |
| GBR | STATE_WEST_COUNTRY | `building_port` | 2 | MEDIUM | YES | OCEANIC_PORT |
| GBR | STATE_WEST_COUNTRY | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| GBR | STATE_WEST_COUNTRY | `building_shipyard` | 2 | MEDIUM | YES | NAVAL_SHIPBUILDING |
| GBR | STATE_WEST_COUNTRY | `building_trade_center` | 2 | MEDIUM | NO | ATLANTIC_TRADE |
| GBR | STATE_YORKSHIRE | `building_coal_mine` | 2 | MEDIUM | NO | COAL_EXTRACTION |
| GBR | STATE_YORKSHIRE | `building_iron_mine` | 1 | MEDIUM | NO | IRON_EXTRACTION |
| GBR | STATE_YORKSHIRE | `building_railway` | 2 | MEDIUM | YES | REGIONAL_TRANSPORT |
| GBR | STATE_YORKSHIRE | `building_steel_mill` | 2 | HIGH | YES | CRUCIBLE_STEEL |
| GBR | STATE_YORKSHIRE | `building_textile_mill` | 3 | HIGH | NO | WOOL_TEXTILES |
| GBR | STATE_YORKSHIRE | `building_tooling_workshop` | 2 | MEDIUM | YES | STEEL_TOOLS |
| GBR | STATE_YORKSHIRE | `building_trade_center` | 1 | MEDIUM | NO | INLAND_MARKET |
| FRA | STATE_ALSACE_LORRAINE | `building_glassworks` | 1 | MEDIUM | YES | GLASS |
| FRA | STATE_ALSACE_LORRAINE | `building_iron_mine` | 1 | MEDIUM | NO | IRON_EXTRACTION |
| FRA | STATE_ALSACE_LORRAINE | `building_paper_mill` | 1 | MEDIUM | YES | PAPER |
| FRA | STATE_ALSACE_LORRAINE | `building_textile_mill` | 2 | MEDIUM | NO | TEXTILES |
| FRA | STATE_AQUITAINE | `building_food_industry` | 1 | MEDIUM | NO | FOOD_PROCESSING |
| FRA | STATE_AQUITAINE | `building_port` | 2 | HIGH | YES | ATLANTIC_PORT |
| FRA | STATE_AQUITAINE | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| FRA | STATE_AQUITAINE | `building_trade_center` | 3 | HIGH | NO | ATLANTIC_EXPORT_TRADE |
| FRA | STATE_AQUITAINE | `building_vineyard` | 3 | HIGH | NO | WINE_EXPORTS |
| FRA | STATE_AUVERGNE_LIMOUSIN | `building_livestock_ranch` | 2 | MEDIUM | NO | COMMERCIAL_LIVESTOCK |
| FRA | STATE_AUVERGNE_LIMOUSIN | `building_logging_camp` | 1 | MEDIUM | NO | TIMBER |
| FRA | STATE_AUVERGNE_LIMOUSIN | `building_paper_mill` | 1 | LOW | YES | PAPER |
| FRA | STATE_BRITTANY | `building_fishing_wharf` | 2 | MEDIUM | YES | FISHERIES |
| FRA | STATE_BRITTANY | `building_food_industry` | 1 | MEDIUM | NO | FOOD_PROCESSING |
| FRA | STATE_BRITTANY | `building_naval_administration` | 2 | HIGH | YES | NAVAL_ADMINISTRATION |
| FRA | STATE_BRITTANY | `building_naval_fortification` | 1 | MEDIUM | YES | NAVAL_DEFENCE |
| FRA | STATE_BRITTANY | `building_port` | 3 | HIGH | YES | ATLANTIC_PORTS |
| FRA | STATE_BRITTANY | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| FRA | STATE_BRITTANY | `building_shipyard` | 2 | HIGH | YES | NAVAL_SHIPBUILDING |
| FRA | STATE_BRITTANY | `building_textile_mill` | 1 | MEDIUM | NO | LINEN_TEXTILES |
| FRA | STATE_BRITTANY | `building_trade_center` | 3 | HIGH | NO | ATLANTIC_TRADE |
| FRA | STATE_BURGUNDY | `building_food_industry` | 1 | MEDIUM | NO | FOOD_PROCESSING |
| FRA | STATE_BURGUNDY | `building_iron_mine` | 1 | LOW | NO | IRON_EXTRACTION |
| FRA | STATE_BURGUNDY | `building_vineyard` | 3 | HIGH | NO | WINE |
| FRA | STATE_CHAMPAGNE | `building_textile_mill` | 2 | MEDIUM | NO | WOOL_TEXTILES |
| FRA | STATE_CHAMPAGNE | `building_vineyard` | 2 | HIGH | NO | WINE |
| FRA | STATE_CORSICA | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| FRA | STATE_CORSICA | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| FRA | STATE_CORSICA | `building_port` | 1 | MEDIUM | YES | COASTAL_PORT |
| FRA | STATE_CORSICA | `building_vineyard` | 1 | MEDIUM | NO | WINE |
| FRA | STATE_FRANCHE_COMTE | `building_glassworks` | 1 | MEDIUM | YES | GLASS |
| FRA | STATE_FRANCHE_COMTE | `building_iron_mine` | 1 | MEDIUM | NO | IRON_EXTRACTION |
| FRA | STATE_FRANCHE_COMTE | `building_logging_camp` | 1 | MEDIUM | NO | TIMBER |
| FRA | STATE_FRANCHE_COMTE | `building_salt_mine` | 2 | HIGH | NO | SALT_EXTRACTION |
| FRA | STATE_FRENCH_LOW_COUNTRIES | `building_coal_mine` | 3 | HIGH | NO | COAL_EXTRACTION |
| FRA | STATE_FRENCH_LOW_COUNTRIES | `building_port` | 1 | MEDIUM | YES | CHANNEL_PORT |
| FRA | STATE_FRENCH_LOW_COUNTRIES | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| FRA | STATE_FRENCH_LOW_COUNTRIES | `building_textile_mill` | 3 | HIGH | NO | TEXTILES |
| FRA | STATE_FRENCH_LOW_COUNTRIES | `building_trade_center` | 1 | MEDIUM | NO | REGIONAL_TRADE |
| FRA | STATE_GUYENNE | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| FRA | STATE_GUYENNE | `building_vineyard` | 2 | MEDIUM | NO | WINE |
| FRA | STATE_GUYENNE | `building_wheat_farm` | 1 | MEDIUM | NO | GRAIN |
| FRA | STATE_LANGUEDOC | `building_port` | 1 | MEDIUM | YES | MEDITERRANEAN_PORT |
| FRA | STATE_LANGUEDOC | `building_railway` | 2 | HIGH | YES | REGIONAL_TRANSPORT |
| FRA | STATE_LANGUEDOC | `building_textile_mill` | 3 | HIGH | NO | WOOL_TEXTILES |
| FRA | STATE_LANGUEDOC | `building_trade_center` | 1 | MEDIUM | NO | REGIONAL_TRADE |
| FRA | STATE_LANGUEDOC | `building_university` | 1 | HIGH | NO | HIGHER_EDUCATION |
| FRA | STATE_LANGUEDOC | `building_vineyard` | 2 | MEDIUM | NO | WINE |
| FRA | STATE_LORRAINE | `building_glassworks` | 2 | MEDIUM | YES | GLASS |
| FRA | STATE_LORRAINE | `building_iron_mine` | 2 | MEDIUM | NO | IRON_EXTRACTION |
| FRA | STATE_LORRAINE | `building_logging_camp` | 1 | MEDIUM | NO | TIMBER |
| FRA | STATE_LORRAINE | `building_salt_mine` | 2 | HIGH | NO | SALT_EXTRACTION |
| FRA | STATE_LORRAINE | `building_tooling_workshop` | 1 | MEDIUM | YES | METALWORKING |
| FRA | STATE_MAINE_ANJOU | `building_food_industry` | 1 | MEDIUM | NO | FOOD_PROCESSING |
| FRA | STATE_MAINE_ANJOU | `building_textile_mill` | 1 | MEDIUM | NO | TEXTILES |
| FRA | STATE_MAINE_ANJOU | `building_wheat_farm` | 1 | MEDIUM | NO | GRAIN |
| FRA | STATE_NORMANDY | `building_food_industry` | 1 | MEDIUM | NO | FOOD_PROCESSING |
| FRA | STATE_NORMANDY | `building_paper_mill` | 1 | MEDIUM | YES | PAPER |
| FRA | STATE_NORMANDY | `building_port` | 2 | HIGH | YES | CHANNEL_PORT |
| FRA | STATE_NORMANDY | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| FRA | STATE_NORMANDY | `building_shipyard` | 1 | MEDIUM | YES | SHIPBUILDING |
| FRA | STATE_NORMANDY | `building_textile_mill` | 3 | HIGH | NO | COTTON_WOOL_TEXTILES |
| FRA | STATE_NORMANDY | `building_trade_center` | 2 | HIGH | NO | EXPORT_TRADE |
| FRA | STATE_ORLEANS | `building_food_industry` | 1 | MEDIUM | NO | FOOD_PROCESSING |
| FRA | STATE_ORLEANS | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| FRA | STATE_ORLEANS | `building_wheat_farm` | 2 | MEDIUM | NO | GRAIN |
| FRA | STATE_PICARDY | `building_port` | 1 | MEDIUM | YES | CHANNEL_PORT |
| FRA | STATE_PICARDY | `building_textile_mill` | 2 | MEDIUM | NO | TEXTILES |
| FRA | STATE_PICARDY | `building_trade_center` | 1 | LOW | NO | REGIONAL_TRADE |
| FRA | STATE_PICARDY | `building_wheat_farm` | 1 | MEDIUM | NO | GRAIN |
| FRA | STATE_POITOU | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| FRA | STATE_POITOU | `building_naval_administration` | 2 | HIGH | YES | NAVAL_ADMINISTRATION |
| FRA | STATE_POITOU | `building_port` | 2 | HIGH | YES | ATLANTIC_PORT |
| FRA | STATE_POITOU | `building_salt_pan` | 2 | MEDIUM | NO | SALT_WORKS |
| FRA | STATE_POITOU | `building_shipyard` | 2 | HIGH | YES | ROYAL_SHIPYARD |
| FRA | STATE_PROVENCE | `building_food_industry` | 1 | MEDIUM | NO | FOOD_PROCESSING |
| FRA | STATE_PROVENCE | `building_naval_administration` | 2 | HIGH | YES | NAVAL_ADMINISTRATION |
| FRA | STATE_PROVENCE | `building_naval_fortification` | 1 | MEDIUM | YES | NAVAL_DEFENCE |
| FRA | STATE_PROVENCE | `building_port` | 3 | HIGH | YES | MEDITERRANEAN_PORT |
| FRA | STATE_PROVENCE | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| FRA | STATE_PROVENCE | `building_shipyard` | 2 | HIGH | YES | ROYAL_SHIPYARD |
| FRA | STATE_PROVENCE | `building_textile_mill` | 1 | MEDIUM | NO | TEXTILES |
| FRA | STATE_PROVENCE | `building_trade_center` | 3 | HIGH | NO | MEDITERRANEAN_ENTREPOT |
| FRA | STATE_RHONE | `building_arms_industry` | 2 | HIGH | NO | ARMS_PRODUCTION |
| FRA | STATE_RHONE | `building_coal_mine` | 1 | MEDIUM | NO | COAL_EXTRACTION |
| FRA | STATE_RHONE | `building_food_industry` | 1 | MEDIUM | NO | FOOD_PROCESSING |
| FRA | STATE_RHONE | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| FRA | STATE_RHONE | `building_textile_mill` | 4 | HIGH | NO | LYON_SILK |
| FRA | STATE_RHONE | `building_tooling_workshop` | 1 | MEDIUM | YES | METALWORKING |
| FRA | STATE_RHONE | `building_trade_center` | 2 | HIGH | NO | INLAND_LONG_DISTANCE_TRADE |
| FRA | STATE_ILE_DE_FRANCE | `building_arms_industry` | 1 | HIGH | NO | STATE_ARMAMENT |
| FRA | STATE_ILE_DE_FRANCE | `building_artillery_foundry` | 2 | HIGH | NO | STATE_ARTILLERY |
| FRA | STATE_ILE_DE_FRANCE | `building_barrack` | 2 | MEDIUM | YES | MILITARY_GARRISON |
| FRA | STATE_ILE_DE_FRANCE | `building_construction_sector` | 2 | MEDIUM | YES | CAPITAL_CONSTRUCTION |
| FRA | STATE_ILE_DE_FRANCE | `building_food_industry` | 2 | MEDIUM | NO | URBAN_FOOD |
| FRA | STATE_ILE_DE_FRANCE | `building_furniture_manufactory` | 2 | MEDIUM | YES | LUXURY_MANUFACTURE |
| FRA | STATE_ILE_DE_FRANCE | `building_glassworks` | 1 | MEDIUM | YES | GLASS |
| FRA | STATE_ILE_DE_FRANCE | `building_government_administration` | 3 | HIGH | NO | CAPITAL_ADMINISTRATION |
| FRA | STATE_ILE_DE_FRANCE | `building_paper_mill` | 2 | MEDIUM | YES | PRINT_PAPER |
| FRA | STATE_ILE_DE_FRANCE | `building_railway` | 2 | HIGH | NO | REGIONAL_TRANSPORT |
| FRA | STATE_ILE_DE_FRANCE | `building_trade_center` | 2 | HIGH | NO | INLAND_NATIONAL_MARKET |
| FRA | STATE_ILE_DE_FRANCE | `building_university` | 2 | HIGH | NO | HIGHER_EDUCATION |
| NET | STATE_FRIESLAND | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| NET | STATE_FRIESLAND | `building_food_industry` | 1 | MEDIUM | YES | FOOD_PROCESSING |
| NET | STATE_FRIESLAND | `building_livestock_ranch` | 2 | MEDIUM | NO | DAIRY_LIVESTOCK |
| NET | STATE_FRIESLAND | `building_port` | 1 | MEDIUM | YES | COASTAL_PORT |
| NET | STATE_FRIESLAND | `building_railway` | 1 | MEDIUM | YES | REGIONAL_TRANSPORT |
| NET | STATE_FRIESLAND | `building_shipyard` | 1 | MEDIUM | YES | SHIPBUILDING |
| NET | STATE_GELRE | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| NET | STATE_GELRE | `building_logging_camp` | 1 | MEDIUM | NO | TIMBER |
| NET | STATE_GELRE | `building_paper_mill` | 1 | MEDIUM | YES | PAPER |
| NET | STATE_GELRE | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| NET | STATE_GELRE | `building_wheat_farm` | 2 | MEDIUM | NO | GRAIN |
| NET | STATE_HOLLAND | `building_construction_sector` | 2 | MEDIUM | YES | URBAN_PORT_CONSTRUCTION |
| NET | STATE_HOLLAND | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| NET | STATE_HOLLAND | `building_food_industry` | 2 | MEDIUM | YES | FOOD_PROCESSING |
| NET | STATE_HOLLAND | `building_furniture_manufactory` | 1 | MEDIUM | YES | URBAN_MANUFACTURE |
| NET | STATE_HOLLAND | `building_glassworks` | 1 | MEDIUM | YES | GLASS |
| NET | STATE_HOLLAND | `building_government_administration` | 2 | MEDIUM | NO | STATE_URBAN_ADMINISTRATION |
| NET | STATE_HOLLAND | `building_naval_administration` | 2 | HIGH | YES | ADMIRALTY_DOCKYARD |
| NET | STATE_HOLLAND | `building_paper_mill` | 2 | MEDIUM | YES | PAPER_PRINT |
| NET | STATE_HOLLAND | `building_port` | 4 | HIGH | YES | GLOBAL_PORT |
| NET | STATE_HOLLAND | `building_railway` | 3 | HIGH | YES | REGIONAL_TRANSPORT |
| NET | STATE_HOLLAND | `building_shipyard` | 3 | HIGH | YES | SHIPBUILDING |
| NET | STATE_HOLLAND | `building_textile_mill` | 2 | HIGH | NO | TEXTILES |
| NET | STATE_HOLLAND | `building_tooling_workshop` | 1 | MEDIUM | YES | TOOLS_SHIP_SUPPLY |
| NET | STATE_HOLLAND | `building_trade_center` | 4 | HIGH | NO | GLOBAL_ENTREPOT |
| NET | STATE_HOLLAND | `building_university` | 1 | HIGH | NO | HIGHER_EDUCATION |
| BEO | STATE_FLANDERS | `building_construction_sector` | 1 | MEDIUM | YES | URBAN_CONSTRUCTION |
| BEO | STATE_FLANDERS | `building_food_industry` | 1 | MEDIUM | YES | FOOD_PROCESSING |
| BEO | STATE_FLANDERS | `building_government_administration` | 2 | MEDIUM | NO | PROVINCIAL_ADMINISTRATION |
| BEO | STATE_FLANDERS | `building_paper_mill` | 1 | MEDIUM | YES | PAPER |
| BEO | STATE_FLANDERS | `building_port` | 2 | MEDIUM | YES | NORTH_SEA_PORT |
| BEO | STATE_FLANDERS | `building_railway` | 2 | HIGH | YES | REGIONAL_TRANSPORT |
| BEO | STATE_FLANDERS | `building_textile_mill` | 3 | HIGH | NO | LINEN_TEXTILES |
| BEO | STATE_FLANDERS | `building_trade_center` | 2 | MEDIUM | NO | REGIONAL_EXPORT_TRADE |
| BEO | STATE_FLANDERS | `building_university` | 1 | MEDIUM | NO | HIGHER_EDUCATION |
| BEO | STATE_WALLONIA | `building_arms_industry` | 2 | HIGH | NO | ARMS_PRODUCTION |
| BEO | STATE_WALLONIA | `building_coal_mine` | 3 | HIGH | NO | COAL_EXTRACTION |
| BEO | STATE_WALLONIA | `building_construction_sector` | 1 | MEDIUM | YES | INDUSTRIAL_CONSTRUCTION |
| BEO | STATE_WALLONIA | `building_glassworks` | 2 | MEDIUM | YES | GLASS |
| BEO | STATE_WALLONIA | `building_iron_mine` | 2 | MEDIUM | NO | IRON_EXTRACTION |
| BEO | STATE_WALLONIA | `building_paper_mill` | 1 | MEDIUM | YES | PAPER |
| BEO | STATE_WALLONIA | `building_railway` | 2 | HIGH | YES | REGIONAL_TRANSPORT |
| BEO | STATE_WALLONIA | `building_steel_mill` | 2 | MEDIUM | YES | IRON_STEEL_WORKING |
| BEO | STATE_WALLONIA | `building_tooling_workshop` | 1 | MEDIUM | YES | METALWORKING |
| LUX | STATE_WALLONIA | `building_barrack` | 2 | HIGH | YES | FORTRESS_GARRISON |
| LUX | STATE_WALLONIA | `building_government_administration` | 1 | MEDIUM | NO | FORTRESS_ADMINISTRATION |
| IREK | STATE_CONNAUGHT | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| IREK | STATE_CONNAUGHT | `building_livestock_ranch` | 1 | MEDIUM | NO | COMMERCIAL_LIVESTOCK |
| IREK | STATE_LEINSTER | `building_barrack` | 1 | MEDIUM | YES | MILITARY_GARRISON |
| IREK | STATE_LEINSTER | `building_construction_sector` | 1 | MEDIUM | YES | CAPITAL_CONSTRUCTION |
| IREK | STATE_LEINSTER | `building_food_industry` | 1 | MEDIUM | YES | FOOD_PROCESSING |
| IREK | STATE_LEINSTER | `building_government_administration` | 2 | MEDIUM | NO | CAPITAL_ADMINISTRATION |
| IREK | STATE_LEINSTER | `building_paper_mill` | 1 | MEDIUM | YES | PAPER_PRINT |
| IREK | STATE_LEINSTER | `building_port` | 2 | HIGH | YES | NATIONAL_PORT |
| IREK | STATE_LEINSTER | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| IREK | STATE_LEINSTER | `building_textile_mill` | 1 | MEDIUM | NO | TEXTILES |
| IREK | STATE_LEINSTER | `building_trade_center` | 2 | HIGH | NO | NATIONAL_TRADE_HUB |
| IREK | STATE_LEINSTER | `building_university` | 1 | HIGH | YES | HIGHER_EDUCATION |
| IREK | STATE_MUNSTER | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| IREK | STATE_MUNSTER | `building_food_industry` | 2 | HIGH | YES | BUTTER_FOOD_PROCESSING |
| IREK | STATE_MUNSTER | `building_livestock_ranch` | 2 | MEDIUM | NO | DAIRY_LIVESTOCK |
| IREK | STATE_MUNSTER | `building_port` | 2 | MEDIUM | YES | ATLANTIC_PORT |
| IREK | STATE_MUNSTER | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| IREK | STATE_MUNSTER | `building_textile_mill` | 1 | MEDIUM | NO | TEXTILES |
| IREK | STATE_MUNSTER | `building_trade_center` | 2 | HIGH | NO | ATLANTIC_EXPORT_TRADE |
| IREK | STATE_ULSTER | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| IREK | STATE_ULSTER | `building_port` | 1 | MEDIUM | YES | COMMERCIAL_PORT |
| IREK | STATE_ULSTER | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| IREK | STATE_ULSTER | `building_textile_mill` | 3 | MEDIUM | NO | LINEN_TEXTILES |
| IREK | STATE_ULSTER | `building_trade_center` | 1 | MEDIUM | NO | REGIONAL_EXPORT_TRADE |
| SPA | STATE_ARAGON | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| SPA | STATE_ARAGON | `building_paper_mill` | 1 | LOW | YES | PAPER |
| SPA | STATE_ARAGON | `building_textile_mill` | 1 | MEDIUM | NO | WOOL_TEXTILES |
| SPA | STATE_ARAGON | `building_wheat_farm` | 2 | MEDIUM | NO | GRAIN |
| SPA | STATE_ASTURIAS | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| SPA | STATE_ASTURIAS | `building_iron_mine` | 1 | MEDIUM | NO | IRON_EXTRACTION |
| SPA | STATE_ASTURIAS | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| SPA | STATE_ASTURIAS | `building_logging_camp` | 1 | MEDIUM | NO | TIMBER |
| SPA | STATE_BALEARIC_ISLANDS | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| SPA | STATE_BALEARIC_ISLANDS | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| SPA | STATE_BALEARIC_ISLANDS | `building_port` | 1 | MEDIUM | YES | MEDITERRANEAN_PORT |
| SPA | STATE_BALEARIC_ISLANDS | `building_vineyard` | 1 | MEDIUM | NO | WINE |
| SPA | STATE_BASQUE_COUNTRY | `building_arms_industry` | 2 | HIGH | NO | ARMS_PRODUCTION |
| SPA | STATE_BASQUE_COUNTRY | `building_iron_mine` | 2 | HIGH | NO | IRON_EXTRACTION |
| SPA | STATE_BASQUE_COUNTRY | `building_port` | 2 | HIGH | YES | ATLANTIC_PORT |
| SPA | STATE_BASQUE_COUNTRY | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| SPA | STATE_BASQUE_COUNTRY | `building_shipyard` | 2 | HIGH | YES | SHIPBUILDING |
| SPA | STATE_BASQUE_COUNTRY | `building_tooling_workshop` | 2 | HIGH | YES | IRONWORKING |
| SPA | STATE_BASQUE_COUNTRY | `building_trade_center` | 2 | MEDIUM | NO | ATLANTIC_TRADE |
| SPA | STATE_CANARY_ISLANDS | `building_fishing_wharf` | 1 | MEDIUM | YES | FISHERIES |
| SPA | STATE_CANARY_ISLANDS | `building_port` | 1 | MEDIUM | YES | ATLANTIC_PORT |
| SPA | STATE_CANARY_ISLANDS | `building_trade_center` | 1 | MEDIUM | NO | ATLANTIC_TRADE |
| SPA | STATE_CANARY_ISLANDS | `building_vineyard` | 2 | HIGH | NO | WINE_EXPORTS |
| SPA | STATE_CATALONIA | `building_construction_sector` | 1 | MEDIUM | YES | URBAN_CONSTRUCTION |
| SPA | STATE_CATALONIA | `building_food_industry` | 2 | MEDIUM | YES | FOOD_PROCESSING |
| SPA | STATE_CATALONIA | `building_glassworks` | 1 | MEDIUM | YES | GLASS |
| SPA | STATE_CATALONIA | `building_paper_mill` | 2 | MEDIUM | YES | PAPER |
| SPA | STATE_CATALONIA | `building_port` | 2 | HIGH | YES | MEDITERRANEAN_PORT |
| SPA | STATE_CATALONIA | `building_railway` | 2 | MEDIUM | NO | REGIONAL_TRANSPORT |
| SPA | STATE_CATALONIA | `building_textile_mill` | 4 | HIGH | NO | COTTON_TEXTILES |
| SPA | STATE_CATALONIA | `building_tooling_workshop` | 1 | MEDIUM | YES | TOOLS |
| SPA | STATE_CATALONIA | `building_trade_center` | 3 | HIGH | NO | MEDITERRANEAN_TRADE |
| SPA | STATE_CATALONIA | `building_vineyard` | 2 | MEDIUM | NO | WINE |
| SPA | STATE_EXTREMADURA | `building_livestock_ranch` | 2 | MEDIUM | NO | TRANSHUMANT_LIVESTOCK |
| SPA | STATE_EXTREMADURA | `building_wheat_farm` | 1 | MEDIUM | NO | GRAIN |
| SPA | STATE_GALICIA | `building_fishing_wharf` | 3 | HIGH | YES | FISHERIES |
| SPA | STATE_GALICIA | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| SPA | STATE_GALICIA | `building_naval_administration` | 2 | HIGH | YES | NAVAL_ADMINISTRATION |
| SPA | STATE_GALICIA | `building_port` | 2 | HIGH | YES | ATLANTIC_PORT |
| SPA | STATE_GALICIA | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| SPA | STATE_GALICIA | `building_shipyard` | 2 | HIGH | YES | ROYAL_SHIPYARD |
| SPA | STATE_GALICIA | `building_textile_mill` | 1 | MEDIUM | NO | LINEN_TEXTILES |
| SPA | STATE_GALICIA | `building_trade_center` | 1 | MEDIUM | NO | ATLANTIC_TRADE |
| SPA | STATE_LEON | `building_livestock_ranch` | 2 | MEDIUM | NO | LIVESTOCK |
| SPA | STATE_LEON | `building_textile_mill` | 1 | MEDIUM | NO | WOOL_TEXTILES |
| SPA | STATE_LEON | `building_university` | 1 | MEDIUM | NO | HIGHER_EDUCATION |
| SPA | STATE_LEON | `building_wheat_farm` | 1 | MEDIUM | NO | GRAIN |
| SPA | STATE_LOWER_ANDALUSIA | `building_food_industry` | 2 | MEDIUM | YES | FOOD_PROCESSING |
| SPA | STATE_LOWER_ANDALUSIA | `building_naval_administration` | 2 | HIGH | YES | NAVAL_ADMINISTRATION |
| SPA | STATE_LOWER_ANDALUSIA | `building_port` | 3 | HIGH | YES | ATLANTIC_PORT |
| SPA | STATE_LOWER_ANDALUSIA | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| SPA | STATE_LOWER_ANDALUSIA | `building_salt_pan` | 2 | MEDIUM | NO | SALT_EXPORTS |
| SPA | STATE_LOWER_ANDALUSIA | `building_shipyard` | 3 | HIGH | YES | ROYAL_ARSENAL |
| SPA | STATE_LOWER_ANDALUSIA | `building_trade_center` | 3 | HIGH | NO | ATLANTIC_ENTREPOT |
| SPA | STATE_LOWER_ANDALUSIA | `building_university` | 1 | MEDIUM | NO | HIGHER_EDUCATION |
| SPA | STATE_LOWER_ANDALUSIA | `building_vineyard` | 2 | HIGH | NO | WINE_EXPORTS |
| SPA | STATE_LOWER_ANDALUSIA | `building_wheat_farm` | 2 | MEDIUM | NO | GRAIN |
| SPA | STATE_MURCIA | `building_naval_administration` | 2 | HIGH | YES | NAVAL_ADMINISTRATION |
| SPA | STATE_MURCIA | `building_port` | 2 | HIGH | YES | MEDITERRANEAN_PORT |
| SPA | STATE_MURCIA | `building_salt_pan` | 1 | MEDIUM | NO | SALT |
| SPA | STATE_MURCIA | `building_shipyard` | 2 | HIGH | YES | ROYAL_ARSENAL |
| SPA | STATE_MURCIA | `building_textile_mill` | 1 | MEDIUM | NO | SILK_TEXTILES |
| SPA | STATE_MURCIA | `building_vineyard` | 1 | MEDIUM | NO | WINE |
| SPA | STATE_NEW_CASTILE | `building_arms_industry` | 1 | MEDIUM | NO | STATE_ARMAMENT |
| SPA | STATE_NEW_CASTILE | `building_artillery_foundry` | 1 | MEDIUM | NO | STATE_ARTILLERY |
| SPA | STATE_NEW_CASTILE | `building_construction_sector` | 1 | MEDIUM | YES | CAPITAL_CONSTRUCTION |
| SPA | STATE_NEW_CASTILE | `building_furniture_manufactory` | 1 | MEDIUM | YES | LUXURY_MANUFACTURE |
| SPA | STATE_NEW_CASTILE | `building_government_administration` | 3 | HIGH | NO | CAPITAL_ADMINISTRATION |
| SPA | STATE_NEW_CASTILE | `building_railway` | 2 | MEDIUM | NO | REGIONAL_TRANSPORT |
| SPA | STATE_NEW_CASTILE | `building_textile_mill` | 2 | MEDIUM | NO | ROYAL_TEXTILES |
| SPA | STATE_NEW_CASTILE | `building_trade_center` | 2 | MEDIUM | NO | INLAND_NATIONAL_MARKET |
| SPA | STATE_NEW_CASTILE | `building_university` | 1 | MEDIUM | NO | HIGHER_EDUCATION |
| SPA | STATE_OLD_CASTILE | `building_glassworks` | 2 | HIGH | YES | ROYAL_GLASS |
| SPA | STATE_OLD_CASTILE | `building_livestock_ranch` | 2 | MEDIUM | NO | LIVESTOCK |
| SPA | STATE_OLD_CASTILE | `building_paper_mill` | 1 | MEDIUM | YES | PAPER |
| SPA | STATE_OLD_CASTILE | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| SPA | STATE_OLD_CASTILE | `building_textile_mill` | 2 | MEDIUM | NO | WOOL_TEXTILES |
| SPA | STATE_OLD_CASTILE | `building_wheat_farm` | 2 | MEDIUM | NO | GRAIN |
| SPA | STATE_UPPER_ANDALUSIA | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| SPA | STATE_UPPER_ANDALUSIA | `building_textile_mill` | 1 | LOW | NO | TEXTILES |
| SPA | STATE_UPPER_ANDALUSIA | `building_wheat_farm` | 2 | MEDIUM | NO | GRAIN |
| SPA | STATE_VALENCIA | `building_food_industry` | 1 | MEDIUM | YES | FOOD_PROCESSING |
| SPA | STATE_VALENCIA | `building_paper_mill` | 1 | MEDIUM | YES | PAPER |
| SPA | STATE_VALENCIA | `building_port` | 2 | HIGH | YES | MEDITERRANEAN_PORT |
| SPA | STATE_VALENCIA | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| SPA | STATE_VALENCIA | `building_rice_farm` | 2 | MEDIUM | NO | RICE |
| SPA | STATE_VALENCIA | `building_textile_mill` | 3 | HIGH | NO | SILK_TEXTILES |
| SPA | STATE_VALENCIA | `building_trade_center` | 2 | HIGH | NO | MEDITERRANEAN_TRADE |
| SPA | STATE_VALENCIA | `building_vineyard` | 2 | MEDIUM | NO | WINE |
| POR | STATE_ALENTEJO | `building_livestock_ranch` | 2 | MEDIUM | NO | LIVESTOCK |
| POR | STATE_ALENTEJO | `building_vineyard` | 1 | MEDIUM | NO | WINE |
| POR | STATE_ALENTEJO | `building_wheat_farm` | 2 | MEDIUM | NO | GRAIN |
| POR | STATE_AZORES | `building_livestock_ranch` | 1 | MEDIUM | NO | LIVESTOCK |
| POR | STATE_AZORES | `building_port` | 1 | MEDIUM | YES | ATLANTIC_PORT |
| POR | STATE_AZORES | `building_trade_center` | 1 | MEDIUM | NO | ATLANTIC_ISLAND_TRADE |
| POR | STATE_AZORES | `building_vineyard` | 1 | MEDIUM | NO | WINE_EXPORTS |
| POR | STATE_AZORES | `building_wheat_farm` | 1 | MEDIUM | NO | GRAIN |
| POR | STATE_BEIRA | `building_glassworks` | 1 | MEDIUM | YES | GLASS |
| POR | STATE_BEIRA | `building_logging_camp` | 1 | MEDIUM | NO | TIMBER |
| POR | STATE_BEIRA | `building_paper_mill` | 1 | MEDIUM | YES | PAPER |
| POR | STATE_BEIRA | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| POR | STATE_BEIRA | `building_textile_mill` | 2 | MEDIUM | NO | WOOL_TEXTILES |
| POR | STATE_BEIRA | `building_university` | 2 | HIGH | NO | HIGHER_EDUCATION |
| POR | STATE_BEIRA | `building_wheat_farm` | 1 | MEDIUM | NO | GRAIN |
| POR | STATE_CAPE_VERDE | `building_port` | 1 | MEDIUM | YES | ATLANTIC_WAYPOINT |
| POR | STATE_CAPE_VERDE | `building_salt_pan` | 1 | MEDIUM | NO | SALT_EXPORT |
| POR | STATE_CAPE_VERDE | `building_trade_center` | 1 | MEDIUM | NO | ATLANTIC_REEXPORT |
| POR | STATE_ENTRE_DOURO_E_MINHO | `building_food_industry` | 1 | MEDIUM | YES | FOOD_PROCESSING |
| POR | STATE_ENTRE_DOURO_E_MINHO | `building_paper_mill` | 1 | MEDIUM | YES | PAPER |
| POR | STATE_ENTRE_DOURO_E_MINHO | `building_port` | 2 | HIGH | YES | ATLANTIC_PORT |
| POR | STATE_ENTRE_DOURO_E_MINHO | `building_railway` | 1 | MEDIUM | NO | REGIONAL_TRANSPORT |
| POR | STATE_ENTRE_DOURO_E_MINHO | `building_shipyard` | 1 | MEDIUM | YES | SHIPBUILDING |
| POR | STATE_ENTRE_DOURO_E_MINHO | `building_textile_mill` | 2 | MEDIUM | NO | TEXTILES |
| POR | STATE_ENTRE_DOURO_E_MINHO | `building_trade_center` | 2 | HIGH | NO | ATLANTIC_EXPORT_TRADE |
| POR | STATE_ENTRE_DOURO_E_MINHO | `building_vineyard` | 3 | HIGH | NO | PORT_WINE |
| POR | STATE_ESTREMADURA | `building_construction_sector` | 2 | MEDIUM | YES | CAPITAL_CONSTRUCTION |
| POR | STATE_ESTREMADURA | `building_food_industry` | 2 | MEDIUM | YES | FOOD_PROCESSING |
| POR | STATE_ESTREMADURA | `building_furniture_manufactory` | 1 | MEDIUM | YES | FURNITURE |
| POR | STATE_ESTREMADURA | `building_glassworks` | 1 | MEDIUM | YES | GLASS |
| POR | STATE_ESTREMADURA | `building_government_administration` | 3 | HIGH | NO | CAPITAL_ADMINISTRATION |
| POR | STATE_ESTREMADURA | `building_naval_administration` | 2 | HIGH | YES | NAVAL_ADMINISTRATION |
| POR | STATE_ESTREMADURA | `building_paper_mill` | 1 | MEDIUM | YES | PAPER |
| POR | STATE_ESTREMADURA | `building_pena_convent` | 1 | HIGH | NO | RELIGIOUS_MONUMENT |
| POR | STATE_ESTREMADURA | `building_port` | 3 | HIGH | YES | ATLANTIC_PORT |
| POR | STATE_ESTREMADURA | `building_railway` | 2 | MEDIUM | NO | REGIONAL_TRANSPORT |
| POR | STATE_ESTREMADURA | `building_shipyard` | 3 | HIGH | YES | ROYAL_SHIPYARD |
| POR | STATE_ESTREMADURA | `building_textile_mill` | 2 | MEDIUM | NO | TEXTILES |
| POR | STATE_ESTREMADURA | `building_trade_center` | 3 | HIGH | NO | ATLANTIC_ENTREPOT |
| POR | STATE_MADEIRA | `building_food_industry` | 1 | MEDIUM | YES | WINE_FOOD_PROCESSING |
| POR | STATE_MADEIRA | `building_port` | 1 | MEDIUM | YES | ATLANTIC_PORT |
| POR | STATE_MADEIRA | `building_trade_center` | 1 | HIGH | NO | ATLANTIC_WINE_TRADE |
| POR | STATE_MADEIRA | `building_vineyard` | 3 | HIGH | NO | MADEIRA_WINE |

## 5. IMPORTANT_NON_RECOMMENDATIONS

| State | Industry | Decision | Reason | Source |
|---|---|---|---|---|
| GBR / STATE_BALEARIC_ISLANDS | `building_port` | NO_BUILDING | Historical Port Mahon is important, but this exact Owner_TAG+State_ID line has Has_Port_Access=NO in the authoritative map catalogue; no port is invented against the pack. | https://www.islahospitalmenorca.org/en/historical-texts/?v=073cc70932ad |
| GBR / all states | `active railway PM` | NO_BUILDING | No active rail network is permitted on 1776-01-01. Any building_railway row is roads/canals only and must use pm_no_rail_network. |  |
| FRA / all states | `active railway PM` | NO_BUILDING | No active rail network in 1776; infrastructure recommendations represent roads/canals only. |  |
| NET / all states | `active railway PM` | NO_BUILDING | No active rail network in 1776; Holland's high infrastructure level is canal/road capacity. |  |
| SPA / all states | `active railway PM` | NO_BUILDING | No active rail network in 1776. |  |
| POR / all states | `active railway PM` | NO_BUILDING | No active rail network in 1776. |  |
| IREK / STATE_LEINSTER | `industrial canal PM` | NO_BUILDING | The Grand Canal was under construction; an operating industrial-canal network is not justified at the strict cutoff. | https://archive.waterwaysireland.org/history-of-the-waterways/9/the-history-of-the-grand-canal |
| SPA / STATE_ARAGON | `industrial canal PM` | NO_BUILDING | Large canal projects were not yet complete enough at 1776-01-01 to seed an operating industrial-canal PM. |  |
| SPA / STATE_ASTURIAS | `building_coal_mine` | NO_BUILDING | Coal was known, but evidence in this pass is insufficient for a state-scale organized commercial coal sector by the strict cutoff; keep extraction abstract pending stronger quantitative proof. |  |
| SPA / STATE_VALENCIA | `post-1776 Vinalesa mechanized factory` | NO_BUILDING | The later factory must not be used to justify the 1776 level. The textile recommendation rests on the broader pre-1776 Valencian silk economy. | https://hispania.revistas.csic.es/index.php/hispania/article/view/698 |
| BEO / STATE_GELRE | `specialized building` | NO_BUILDING | This is a very small BEO-owned Gelre fragment in the current map; no state-scale specialized sector is supported strongly enough to seed manually. |  |
| LUX / STATE_WALLONIA | `building_arms_industry` | NO_BUILDING | A major fortress/garrison does not by itself establish a state-scale local arms-manufacturing industry. | https://whc.unesco.org/en/list/699 |
| BEO / STATE_WALLONIA | `coke-dependent industrial expansion` | NO_BUILDING | The strong pre-1776 Walloon coal/iron district is represented conservatively; British-style coke-smelting diffusion is not assumed. | https://connaitrelawallonie.wallonie.be/histoire/timeline/18-janvier-1721-installation-de-la-toute-premiere-pompe-feu-du-continent-jemeppe |
| POR / STATE_ESTREMADURA | `Pena Palace` | NO_BUILDING | The nineteenth-century Pena Palace is post-cutoff. Only the catalogue's distinct pre-existing building_pena_convent is recommended. | https://www.parquesdesintra.pt/en/parks-monuments/park-and-national-palace-of-pena/history/ |
| Western Europe | `building_chemical_works` | NO_BUILDING | Acid and chemical crafts existed, but this pass did not find state-scale evidence strong enough to map the fork's Chemical Works building conservatively at 1776-01-01. |  |
| Western Europe | `building_alloys_plant` | NO_BUILDING | The fork building represents a much broader advanced alloys system; no ordinary 1776 placement is proposed without a dedicated catalogue justification. |  |

## 6. États sans ligne positive

- **BEO + STATE_GELRE — Gelre** : aucune activité spécialisée n'a franchi le seuil de preuve/échelle dans cette passe ; ne pas remplir par analogie.

## 7. Contrôle final

STATES COVERED = 64
POSITIVE BUILDING ROWS = 370
TRADE CENTERS = 32
LEVEL 1 = 180
LEVEL 2 = 145
LEVEL 3 = 39
LEVEL 4-5 = 6
LEVEL 6+ = 0
TECH_DISTRIBUTION_REVIEW = 160
REVIEW CASES = 0
SERENISSIMA STATES SKIPPED = 8

Validation automatique : aucun State_ID inventé, aucun Building_ID absent du catalogue, aucun bâtiment auto-généré/NO_ENGINE_GENERATED, aucun port placé dans une instance sans `Has_Port_Access=YES`, aucune ligne VEN/GEN, aucun rail actif.
