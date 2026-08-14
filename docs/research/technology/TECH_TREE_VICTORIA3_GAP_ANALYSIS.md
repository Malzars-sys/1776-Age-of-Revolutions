# Analyse des écarts Victoria 3 — industrie et technologies

## Portée et constat d'audit

Audit en lecture seule effectué le 14 juillet 2026 sur la copie locale indiquée. La vanilla définit cinq ères: pré-1836, 1836-1861, 1862-1886, 1887-1911 et 1911-1936. Les définitions principales se trouvent dans `common/technology/technologies/{10_production,20_military,30_society}.txt`; les goods dans `common/goods/00_goods.txt`; les industries dans `common/buildings/01_industry.txt`; les PM dans `common/production_methods/*.txt`.

Le fork ne contient aucun fichier dans `common/technology`, `common/goods`, `common/buildings`, `common/production_methods`, `common/production_method_groups` ou `common/institutions`. Il hérite donc la vanilla dans ces domaines. Il possède une définition de compagnies et une injection de lois, sans représentation alternative des chaînes étudiées. «current_fork_representation = inherits vanilla» est une conclusion de comparaison de fichiers, pas une supposition.

## Table d'écarts

| Historical innovation | Current vanilla representation | Current fork representation | Historical gap | Gameplay gap | Recommended action | Risk | Priority |
|---|---|---|---|---|---|---|---|
| Industrial water power | manufacturies/sericulture and implicit traditional PMs | inherits vanilla | No explicit power-system lineage | Weak pre-steam differentiation | keep_existing + represent_with_modifier | low | B |
| Coke smelting | steelworking/blister steel; no named coke node | inherits vanilla | Mineral-fuel transition condensed | Coal-to-iron choice weak | add_production_method | low | A |
| Watt rotative steam | atmospheric_engine then watertube_boiler | inherits vanilla | Watt/Newcomen stages conflated | 1776 frontier unclear | split_technology | medium | A |
| Puddling and rolling | steelworking/blister steel PM | inherits vanilla | 1784 bridge unnamed | Gap between cast iron and mass steel | add_technology + add_production_method | low | A |
| Industrial canals | canals mostly monuments; no general canal building | inherits vanilla | Canal age absent | Pre-rail transport choice absent | add_technology + represent_with_modifier | high | A |
| Improved roads | paved_roads located at end of society file/late era | inherits vanilla | Chronology too late for 1750-1830 roads | 1776-1836 infrastructure missing | move_era + split_technology | medium | A |
| Spinning jenny/water frame/mule | manufacturies and mechanized looms PM | inherits vanilla | Multiple stages condensed | 1776 textile race weak | split_technology + add_production_method | medium | A |
| Power loom | mechanized_looms PM | inherits vanilla | PM exists but node too broad | Unlock chronology opaque | add_technology | low | B |
| Cotton gin | cotton_gin technology | inherits vanilla | Represented | Adequate; slavery effect external | keep_existing | low | B |
| Chlorine bleaching | chemical_bleaching technology | inherits vanilla | Represented | Good but industrial chemicals absent | keep_existing + add_good | medium | B |
| Leblanc/Solvay alkali | leblanc_process; vacuum_evaporation/brine_electrolysis PMs | inherits vanilla | Solvay lineage unnamed/condensed | No competing pollution/input route | split_technology + add_production_method | medium | A |
| Machine tools and metrology | lathe; mechanical_tools; mechanized_workshops | inherits vanilla | Three broad/overlapping nodes | Precision/interchangeability unclear | rename + split_technology | medium | A |
| Interchangeable parts | implicit in mechanized workshops/assembly lines | inherits vanilla | Organizational step absent | No capital-good quality ladder | add_technology | medium | A |
| Metric/industrial standards | international_exchange_standards late society | inherits vanilla | Domestic metrology and international standards conflated | Repair/trade standards lack bridge | split_technology + move_era | medium | B |
| Atmospheric mine pumping | atmospheric_engine tech and mine PM | inherits vanilla | Good representation | Start ownership may need 1776 history | keep_existing | low | A |
| Mine ventilation/safety | mostly throughput PMs; no ventilation node | inherits vanilla | Safety engineering absent | No cost-versus-mortality choice | add_production_method | low | B |
| Geological survey | prospecting generic | inherits vanilla | Survey; assaying; drilling condensed | Exploration too abstract | split_technology | medium | A |
| Ore concentration/flotation | absent | inherits vanilla | Low-grade ores after 1900 absent | Late metals supply lacks technology | add_technology + add_production_method | medium | A |
| Bessemer | bessemer_process tech and PM | inherits vanilla | Represented | Adequate; ore constraint absent | keep_existing | low | A |
| Siemens-Martin | open_hearth_process tech/PM | inherits vanilla | Represented | Scrap/quality route can be clearer | keep_existing + revise_PM | low | B |
| Thomas basic process | absent as named route | inherits vanilla | Phosphoric ore route absent | No steel/fertilizer byproduct link | add_production_method | low | A |
| Alloy steels | electric_arc_process only | inherits vanilla | Nickel/chrome/tungsten metallurgy absent | Strategic materials absent | add_technology + add_production_method | high | B |
| Portland cement | reinforced_concrete but no cement good/industry | inherits vanilla | Material chain skipped | Construction has no cement price | add_good + add_building + add_technology | medium | A |
| Reinforced concrete | reinforced_concrete tech | inherits vanilla | Represented | Needs cement input | keep_existing | low | A |
| Mechanical refrigeration | refrigerated_storage/rail PMs; flash_freezing late | inherits vanilla | Foundational compression node absent | Cold chain unlocks appear disconnected | add_technology | low | A |
| Canning | canneries and vacuum_canning | inherits vanilla | Represented | Good progression | keep_existing | low | B |
| Pasteurization | pasteurization tech | inherits vanilla | Represented | Could connect health institution | keep_existing | low | B |
| Germ theory | pharmaceuticals/modern_sewerage; no clear core node | inherits vanilla | Science/urban systems conflated | Health chain lacks prerequisite spine | add_technology | medium | A |
| Water filtration/chloration | modern_sewerage broad | inherits vanilla | Two eras condensed | No progressive urban sanitation PM | split_technology + add_production_method | medium | B |
| Vaccination | no prominent industrial tech node in audited production/society list | inherits vanilla | 1776-1836 medical transition weak | Public-health institution lacks early route | add_technology or represent_with_institution | medium | B |
| Telegraph | electric_telegraph military tech | inherits vanilla | Civil infrastructure placed primarily military | Economic effects underplayed | move_or_crosslink_era + modifier | medium | A |
| Telephone | telephone production tech; telephone good/PM | inherits vanilla | Represented | Network aspect abstract but acceptable | keep_existing | low | B |
| Radio | radio tech; radio good/PM | inherits vanilla | Represented | Attribution irrelevant to mechanics | keep_existing | low | B |
| Electrical generation | electrical_generation; power plant | inherits vanilla | Generation; grids; motors condensed | Electrification too nearly instantaneous | split_technology | medium | A |
| AC grids/transformers | implicit | inherits vanilla | Transmission system absent | No regional grid maturation | add_technology | medium | A |
| Electric motors | electric engines PM and electrification PMs | inherits vanilla | Adoption stage implicit | Lighting-to-motor lag absent | add_technology + add_production_method | medium | A |
| Hydroelectricity | power plant abstraction | inherits vanilla | Geographic generation route weak | No cheap-power/aluminum nexus | add_production_method + state_trait | medium | B |
| Petroleum refining | fractional_distillation; oil consumed directly in many PMs | inherits vanilla | Refinery industry and refined fuel absent | Oil lacks transformation market | add_good + add_building + split_technology | high | A |
| Internal combustion | combustion_engine; compression_ignition | inherits vanilla | Core represented | Needs refined fuel input | keep_existing + revise_PM | medium | A |
| Aluminum | absent as good/industry; electric_arc not enough | inherits vanilla | Entire Bayer/Hall-Héroult chain absent | No power-intensive light metal | add_good + add_building + add_technology | high | A |
| Copper | not a vanilla good; electricals use generic inputs | inherits vanilla | Key electrical material absent | Grid expansion has weak resource geography | add_good + add_building | high | A |
| Phosphates/nitrates | fertilizer good; sulfur input; nitrogen_fixation | inherits vanilla | Natural fertilizer geographies condensed | Pre-Haber strategic trade absent | add_good + add_production_method | high | A |
| Aniline dyes | aniline tech; dye_production PM creates existing dye | inherits vanilla | Represented | Good use of existing dye good | keep_existing | low | A |
| Industrial pharmaceuticals | pharmaceuticals abstract tech; no good/building | inherits vanilla | Fine-chemical market absent | Health improvements lack material demand | add_good + add_building | medium | A |
| Industrial R&D | academia/university; corporate_management | inherits vanilla | Firm laboratories absent | Second revolution lacks organizational prerequisite | represent_with_institution + company | medium | A |
| Scientific management | corporate_management/shift_work | inherits vanilla | Management methods condensed | No social/input tradeoff | add_production_method | low | B |
| Assembly line | assembly_lines PM unlocked across sectors; conveyors tech | inherits vanilla | Represented broadly | Should require precision and standardized demand | keep_existing + tighten_prerequisites | medium | A |
| Pulp and cellulose | pulp_pressing/sulfite_pulping PM; paper existing good | inherits vanilla | Represented without new pulp good | Adequate; adding pulp may be redundant | keep_existing | low | B |
| Bakelite/plastics | plastics tech; houseware plastics PM | inherits vanilla | Represented | Could use industrial chemicals input | keep_existing + revise_PM | low | B |
| Penicillin/antibiotics | antibiotics tech before 1936 scope end | inherits vanilla | Discovery represented as mass capability too early | Historical timing overstated | rename_or_move_terminal | low | C |

## Goods et bâtiments réutilisables

Les goods existants `coal`, `iron`, `sulfur`, `lead`, `oil`, `rubber`, `steel`, `glass`, `fertilizer`, `tools`, `explosives`, `engines`, `electricity` et `dye` absorbent déjà de nombreuses chaînes. Les bâtiments les plus extensibles sont chemical plant, steel mill, tooling workshop, food industry, paper mill, glassworks, motor industry, electrics industry, mines, farms, urban center, power plant, railway et port. C'est pourquoi colorants synthétiques, verre industriel, pâte, abattoirs, briques, téléphonie et froid doivent d'abord être des PM, non des bâtiments.

## Limites techniques et risques

- Un good exige définition, localisation, icône, besoins, PM, prix, IA et répartition; les minerais nouveaux sont donc à haut risque cartographique et économique.
- Les réseaux continus (pipeline, télégraphe, téléphone, égouts, grille électrique) ne sont pas naturellement modélisés comme graphes physiques; préférer bâtiments existants, PM, infrastructure, modifiers d'État et institutions.
- Les sous-produits et coproduits sont faisables via PM mais peuvent créer des prix instables; Thomas slag et raffinage chimique doivent être testés.
- Les PM transversaux répétés augmentent maintenance et charge IA; les groupes communs d'électrification et de sécurité sont préférables.
- L'héritage du fork réduit les doublons immédiats mais toute refonte future qui remplace un fichier vanilla augmente le risque de compatibilité de version.

## Conclusion d'écart

Le besoin principal n'est pas d'ajouter des dizaines de biens. Il est de réparer la chronologie 1776-1836, rendre visibles cinq systèmes manquants (canaux/routes, précision, ciment, raffinage, froid) et décomposer l'électricité en génération-réseau-moteurs. Les chaînes déjà fortes de vanilla — Bessemer, dynamite, caoutchouc, canning, téléphone, radio, plastiques — doivent surtout être conservées et mieux raccordées.





