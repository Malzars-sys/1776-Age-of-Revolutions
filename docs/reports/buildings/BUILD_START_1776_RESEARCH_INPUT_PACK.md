# BUILD START 1776 — Research Input Pack

Date : 2026-09-16  
Autorité : working tree local actuel  
Référence moteur : Victoria 3 1.13.11 (`C:\Games\Victoria 3\game`)

## Résumé quantitatif

- États possédés actuels : **1043** instances État/propriétaire, couvrant **675** identifiants de région d’État.
- Bâtiments effectivement disponibles : **127**.
- Bâtiments pertinents pour une première recherche 1776 : **73**.
- Entrées de bâtiments de départ actuelles : **2584** couples propriétaire/État/bâtiment.
- Sérénissimes exclues : **8** instances État/propriétaire appartenant à VEN ou GEN.
- Risque Inde : **60** instances ; risque Vietnam : **13** instances.

Les lignes d’États divisés sont conservées séparément par propriétaire. C’est indispensable pour la population, l’accès au port et l’exclusion exacte de VEN/GEN.

## Exclusion VEN / GEN

Toutes les lignes possédées par `VEN` ou `GEN` portent `Excluded_Serenissima = YES`. Elles sont affectées à `EXCLUDED_SERENISSIMA` dans la partition de recherche. Aucun de ces États ne doit recevoir de recommandation issue de la redistribution mondiale générale.

## Risques de refonte cartographique

- `INDIA_FUTURE_REWORK` : toutes les régions d’État du fichier cartographique actuel `10_india.txt`.
- `VIETNAM_FUTURE_REWORK` : Cambodge, Tonkin, Annam, Mékong et Laos dans la carte actuelle.
- La carte Tsar mise à jour n’est jamais utilisée comme cible dans ce pack.

## Bâtiments automatiquement générés

Les chercheurs ne doivent pas proposer manuellement les bâtiments suivants :

- `building_army_logistics_center`
- `building_company_headquarter`
- `building_company_regional_headquarter`
- `building_conscription_center`
- `building_financial_district`
- `building_gold_field`
- `building_manor_house`
- `building_naval_logistics_center`
- `building_subsistence_farm`
- `building_subsistence_fishing_village`
- `building_subsistence_orchard`
- `building_subsistence_pasture`
- `building_subsistence_rice_farm`
- `building_urban_center`

Le catalogue les marque `Auto_Generated = YES`, `History_Placeable = NO_ENGINE_GENERATED` et `Relevant_For_1776_Start_Research = NO_AUTO_GENERATED`.

## Filtre chronologique et bâtiments spéciaux

Les bâtiments suivants sont explicitement exclus de la recherche de départ parce que leur forme représentée est postérieure au 1er janvier 1776 :

- `building_big_ben`
- `building_capitol_hill`
- `building_central_park`
- `building_cristo_redentor`
- `building_eiffel_tower`
- `building_estacion_de_madrid_atocha`
- `building_gran_teatro_de_la_habana`
- `building_kaiserforum_1`
- `building_kaiserforum_2`
- `building_kaiserforum_3`
- `building_kaiserforum_4`
- `building_manila_cathedral_monument`
- `building_mosque_of_djenne`
- `building_pena_palace`
- `building_sagrada_familia_cathedral_1`
- `building_sagrada_familia_cathedral_2`
- `building_sagrada_familia_cathedral_3`
- `building_skyscraper`
- `building_statue_of_liberty`
- `building_victoria_terminus`
- `building_white_house`

Les bâtiments suivants relèvent d’un système spécial ou événementiel et ne sont pas des candidats ordinaires à implanter au départ :

- `building_halloween_castledracula`
- `building_manila_cathedral_ruins`
- `building_power_bloc_statue`

## Centres de commerce

`building_trade_center` est un bâtiment manuel/construit dans Victoria 3 1.13.11, et non un bâtiment généré niveau par niveau par des routes commerciales. Les niveaux historiques sont conservés, fournissent emplois et capacité commerciale, consomment marine marchande et infrastructure, et peuvent créer une surcapacité. Voir `BUILD_START_1776_TRADE_CENTER_MECHANICS.md`.

## REGIONAL_INFRASTRUCTURE_STARTING_LEVELS

| Champ | Valeur effective |
|---|---|
| Building_ID | `building_railway` |
| Alias | `building_land_transport_network` |
| PMGs | `pmg_base_building_land_transport_network`, `pmg_land_transport_canals`, `pmg_base_building_railway`, `pmg_passenger_trains` |
| Routes | `pm_traditional_road_network` (défaut), `pm_turnpike_road_network` → `turnpike_road_networks`, `pm_engineered_road_network` → `improved_road_engineering`, `pm_paved_road_network` → `paved_roads` |
| Canaux | `pm_no_canal_network` (défaut), `pm_industrial_canals` → `industrial_canals`, `pm_engineered_canals` → `professional_civil_engineering` |
| Rail | `pm_no_rail_network` (défaut), `pm_early_trains` → `railways`, puis PM vapeur/électriques/diesel avec leurs technologies supplémentaires |
| Gate du bâtiment | aucune : les portes sont portées par les PM |
| Placement historique | `create_building` avec l’ID canonique `building_railway`; routes actives par défaut, aucun canal et aucun rail par défaut |
| Règle 1776 | rechercher séparément routes et canaux ; conserver obligatoirement `pm_no_rail_network` car le rail est anachronique |

Les trois PMG routes/canaux/rail sont simultanés : leurs infrastructures et effets s’additionnent. Le quatrième PMG, `pmg_passenger_trains`, ne devient matériellement pertinent qu’avec un réseau ferroviaire actif.

## Technologies et gates

Le champ `Technology_Gates` du catalogue contient les technologies nécessaires au bâtiment lui-même. Le champ `Notes` ajoute les `PM_Gates` de toutes ses méthodes. Si la recherche historique exige un bâtiment dont le pays ne possède pas la porte correspondante, la future synthèse doit inscrire **`TECH_DISTRIBUTION_REVIEW`** et ne pas supprimer artificiellement le bâtiment.

Cas structurants :

- ports : `enclosed_dock_systems` ;
- bâtiment régional TECH7A : aucune porte globale, portes distinctes pour routes, canaux et rail ;
- industries et ressources avancées : vérifier leur porte et leur ère dans le catalogue ;
- bâtiments marqués `NO_POST_1776` : ne pas rechercher comme implantation initiale ordinaire.

## Discipline anti-ancrage

`BUILD_START_1776_CURRENT_BUILDINGS.csv` est réservé à la seconde passe de synthèse et au calcul du delta. Il ne doit pas être transmis aux chercheurs pendant leur première recherche historique : leur première proposition doit partir des sources de 1776, du catalogue des bâtiments et de la partition régionale, sans connaître le setup existant.

Le parseur a également ignoré **11** entrées de bâtiments orphelines, dont le couple propriétaire/État ne correspond plus à la carte effective du working tree :

- `FRA / STATE_ALGIERS (common/history/buildings/03_north_africa.txt:358)`
- `FRA / STATE_ALGIERS (common/history/buildings/03_north_africa.txt:369)`
- `FRA / STATE_ALGIERS (common/history/buildings/03_north_africa.txt:380)`
- `FRA / STATE_ALGIERS (common/history/buildings/03_north_africa.txt:393)`
- `FRA / STATE_CONSTANTINE (common/history/buildings/03_north_africa.txt:450)`
- `FRA / STATE_CONSTANTINE (common/history/buildings/03_north_africa.txt:461)`
- `FRA / STATE_ORAN (common/history/buildings/03_north_africa.txt:557)`
- `FRA / STATE_ORAN (common/history/buildings/03_north_africa.txt:568)`
- `FRA / STATE_ORAN (common/history/buildings/03_north_africa.txt:581)`
- `RUS / STATE_BREST (common/history/buildings/15_russia.txt:522)`
- `RUS / STATE_BREST (common/history/buildings/15_russia.txt:535)`

Elles restent intactes dans les fichiers de gameplay ; elles ne sont simplement pas présentées comme bâtiments de départ effectifs dans ce pack technique.

## Neuf régions de recherche

1. `R1_WESTERN_EUROPE`
2. `R2_NORTHERN_CENTRAL_EASTERN_EUROPE`
3. `R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA`
4. `R4_SOUTH_ASIA`
5. `R5_EAST_ASIA`
6. `R6_SOUTHEAST_ASIA_OCEANIA`
7. `R7_SUBSAHARAN_AFRICA`
8. `R8_NORTH_AMERICA_CARIBBEAN`
9. `R9_SOUTH_AMERICA`

Les possessions coloniales sont classées par emplacement de l’État, jamais par métropole.

## Fichiers livrés

- `BUILD_START_1776_STATE_CATALOG.csv`
- `BUILD_START_1776_BUILDING_CATALOG.csv`
- `BUILD_START_1776_CURRENT_BUILDINGS.csv`
- `BUILD_START_1776_RESEARCH_REGIONS.csv`
- `BUILD_START_1776_TRADE_CENTER_MECHANICS.md`
- présent rapport

Aucun fichier de gameplay n’a été modifié. Aucun commit et aucun push.
