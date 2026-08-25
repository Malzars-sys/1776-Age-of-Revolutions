# TECH4C4 ? Final Production Method Technology Gate Audit

## 1. P?rim?tre

- Projet : Victoria 3 ? 1776 Age of Revolutions
- Branche : `tech4c2-audit-snapshot`
- Base : ?tat courant valid? apr?s TECH4C3
- R?f?rence vanilla : Victoria 3 1.13.9 (`C:\Games\Victoria 3\game`)
- Livrable : audit et propositions uniquement ; aucun fichier gameplay modifi? par TECH4C4

Cet audit ne relance pas l?inventaire global des 433 PM vanilla. L??chantillon cibl? r?unit les gates d?plac?es lors des refontes, les anciens cas non r?solus, les PM appartenant aux PMG d?automatisation et les gates ?lectriques explicitement gel?es.

## 2. R?sum?

| Indicateur | Total |
|---|---:|
| PM examin?s | 87 |
| PM modifi?s par TECH4C4 | 0 |
| PM inchang?s | 87 |
| `KEEP_VANILLA` | 35 |
| `ALREADY_FIXED` | 52 |
| `CHANGE_REQUIRED` | 0 |
| `REVIEW_REQUIRED` | 0 |

Conclusion : aucune nouvelle modification de `unlocking_technologies` n?est n?cessaire. Les rattachements d?plac?s avant TECH4C4 sont actifs et coh?rents ; les m?thodes d?automatisation post?rieures conservent leurs technologies vanilla actives ; les gates `electrical_generation` et `electrical_capacitors` restent inchang?es.

## 3. Table des PM examin?s

| PM | B?timent | PMG | Gate actuelle | Gate propos?e | D?cision |
|---|---|---|---|---|---|
| `automatic_irrigation_building_banana_plantation` | `building_banana_plantation` | `pmg_base_building_banana_plantation` | `{ mechanized_irrigation }` | `{ mechanized_irrigation }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `automatic_irrigation_building_cotton_plantation` | `building_cotton_plantation` | `pmg_base_building_cotton_plantation` | `{ mechanized_irrigation }` | `{ mechanized_irrigation }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `automatic_irrigation_building_dye_plantation` | `building_dye_plantation` | `pmg_base_building_dye_plantation` | `{ mechanized_irrigation }` | `{ mechanized_irrigation }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `automatic_irrigation_building_opium_plantation` | `building_opium_plantation` | `pmg_base_building_opium_plantation` | `{ mechanized_irrigation }` | `{ mechanized_irrigation }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `automatic_irrigation_building_rubber_plantation` | `building_rubber_plantation` | `pmg_base_building_rubber_plantation` | `{ mechanized_irrigation }` | `{ mechanized_irrigation }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `automatic_irrigation_building_silk_plantation` | `building_silk_plantation` | `pmg_base_building_silk_plantation` | `{ mechanized_irrigation }` | `{ mechanized_irrigation }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `automatic_irrigation_building_sugar_plantation` | `building_sugar_plantation` | `pmg_base_building_sugar_plantation` | `{ mechanized_irrigation }` | `{ mechanized_irrigation }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `automatic_irrigation_building_tea_plantation` | `building_tea_plantation` | `pmg_base_building_tea_plantation` | `{ mechanized_irrigation }` | `{ mechanized_irrigation }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `automatic_irrigation_building_tobacco_plantation` | `building_tobacco_plantation` | `pmg_base_building_tobacco_plantation` | `{ mechanized_irrigation }` | `{ mechanized_irrigation }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `automatic_irrigation_building_vineyard` | `building_vineyard` | `pmg_base_building_vineyard` | `{ mechanized_irrigation }` | `{ mechanized_irrigation }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `centrifugal_machine_sugar` | `building_sugar_plantation` | `pmg_refinement_building_sugar_plantation` | `{ rotary_valve_engine; sugar_refining }` | `{ rotary_valve_engine; sugar_refining }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `coffee_plantation_mechanical_drying` | `building_coffee_plantation` | `pmg_drying_coffee_plantation` | `{ high_pressure_steam }` | `{ high_pressure_steam }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `coffee_plantation_wet_process_manual` | `building_coffee_plantation` | `pmg_base_building_coffee_plantation` | `{ precision_boring }` | `{ precision_boring }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `coffee_plantation_wet_process_mechanical` | `building_coffee_plantation` | `pmg_base_building_coffee_plantation` | `{ rotative_steam_power }` | `{ rotative_steam_power }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `electric_rollers` | `building_tobacco_plantation` | `pmg_manufacture_tobacco` | `{ electrical_generation }` | `{ electrical_generation }` | KEEP_VANILLA ? gate ?lectrique gel?e ; aucune erreur critique. |
| `molds` | `building_tobacco_plantation` | `pmg_manufacture_tobacco` | `{ precision_boring }` | `{ precision_boring }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_assembly_lines_building_arms_industry` | `building_arms_industry`<br>`building_artillery_foundry` | `pmg_automation_building_arms_industry` | `{ conveyors }` | `{ conveyors }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_assembly_lines_building_automotive_industry` | `building_automotive_industry` | `pmg_automation_building_automotive_industry` | `{ conveyors }` | `{ conveyors }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_assembly_lines_building_furniture_manufactory` | `building_furniture_manufactory` | `pmg_automation_building_furniture_manufactory` | `{ conveyors }` | `{ conveyors }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_assembly_lines_building_motor_industry` | `building_motor_industry` | `pmg_automation_building_motor_industry` | `{ conveyors }` | `{ conveyors }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_assembly_lines_building_munition_plant` | `building_munition_plant` | `pmg_automation_building_munition_plant` | `{ conveyors }` | `{ conveyors }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_assembly_lines_building_tooling_workshop` | `building_tooling_workshop` | `pmg_automation_building_tooling_workshop` | `{ conveyors }` | `{ conveyors }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_automated_bakery` | `building_food_industry` | `pmg_automation_building_food_industry` | `{ dough_rollers }` | `{ dough_rollers }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_automatic_power_looms` | `building_textile_mill` | `pmg_automation_building_textile_mill` | `{ electrical_capacitors }` | `{ electrical_capacitors }` | KEEP_VANILLA ? gate ?lectrique gel?e ; aucune erreur critique. |
| `pm_automation_disabled` | 9 b?timents effectifs | 8 PMG effectifs | `{ }` | `{ }` | KEEP_VANILLA ? PM de base ou de d?sactivation ; absence de gate intentionnelle. |
| `pm_bleached_paper` | `building_paper_mill` | `pmg_base_building_paper_mill` | `{ industrial_paper_bleaching }` | `{ industrial_paper_bleaching }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_brine_electrolysis` | `building_explosives_factory` | `pmg_explosives_building_chemical_plant` | `{ electrical_capacitors }` | `{ electrical_capacitors }` | KEEP_VANILLA ? gate ?lectrique gel?e ; aucune erreur critique. |
| `pm_cannons` | `building_artillery_foundry` | `pmg_foundries` | `{ standardized_field_artillery }` | `{ standardized_field_artillery }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_ceramics` | `building_glassworks` | `pmg_luxury_building_glassworks` | `{ industrial_ceramics }` | `{ industrial_ceramics }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_complex_shipbuilding` | `building_shipyard` | `pmg_base_building_shipyard` | `{ paddle_steamer }` | `{ paddle_steamer }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_condensing_engine_pump_building_coal_mine` | `building_coal_mine` | `pmg_mining_equipment_building_coal_mine` | `{ condensing_steam_engines; deep_mine_engineering }` | `{ condensing_steam_engines; deep_mine_engineering }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_condensing_engine_pump_building_gold_mine` | `building_gold_mine` | `pmg_mining_equipment_building_gold_mine` | `{ condensing_steam_engines; deep_mine_engineering }` | `{ condensing_steam_engines; deep_mine_engineering }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_condensing_engine_pump_building_iron_mine` | `building_iron_mine` | `pmg_mining_equipment_building_iron_mine` | `{ condensing_steam_engines; deep_mine_engineering }` | `{ condensing_steam_engines; deep_mine_engineering }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_condensing_engine_pump_building_lead_mine` | `building_lead_mine` | `pmg_mining_equipment_building_lead_mine` | `{ condensing_steam_engines; deep_mine_engineering }` | `{ condensing_steam_engines; deep_mine_engineering }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_condensing_engine_pump_building_sulfur_mine` | `building_sulfur_mine` | `pmg_mining_equipment_building_sulfur_mine` | `{ condensing_steam_engines; deep_mine_engineering }` | `{ condensing_steam_engines; deep_mine_engineering }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_craftsman_sewing` | `building_textile_mill` | `pmg_luxury_building_textile_mill` | `{ organized_textile_production }` | `{ organized_textile_production }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_dye_workshops` | `building_textile_mill` | `pmg_base_building_textile_mill` | `{ organized_textile_production }` | `{ organized_textile_production }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_electric_fencing` | `building_livestock_ranch` | `pmg_fencing` | `{ electrical_generation }` | `{ electrical_generation }` | KEEP_VANILLA ? gate ?lectrique gel?e ; aucune erreur critique. |
| `pm_electric_saw_mills` | `building_logging_camp` | `pmg_base_building_logging_camp` | `{ electrical_generation }` | `{ electrical_generation }` | KEEP_VANILLA ? gate ?lectrique gel?e ; aucune erreur critique. |
| `pm_electric_sewing_machines` | `building_textile_mill` | `pmg_base_building_textile_mill` | `{ electrical_capacitors }` | `{ electrical_capacitors }` | KEEP_VANILLA ? gate ?lectrique gel?e ; aucune erreur critique. |
| `pm_electric_streetlights` | `building_urban_center` | `pmg_street_lighting` | `{ electrical_generation }` | `{ electrical_generation }` | KEEP_VANILLA ? gate ?lectrique gel?e ; aucune erreur critique. |
| `pm_horizontal_drawer_cabinets` | `building_government_administration` | `pmg_base_building_government_administration` | `{ systematic_population_registration }` | `{ systematic_population_registration }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_iron_frame_buildings` | `building_construction_sector` | `pmg_base_building_construction_sector` | `{ professional_civil_engineering }` | `{ professional_civil_engineering }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_lathe` | `building_furniture_manufactory` | `pmg_base_building_furniture_manufactory` | `{ mechanical_tools }` | `{ mechanical_tools }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_leaded_glass` | `building_glassworks` | `pmg_base_building_glassworks` | `{ industrial_ceramics }` | `{ industrial_ceramics }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_manual_dough_processing` | `building_food_industry` | `pmg_automation_building_food_industry` | `{ }` | `{ }` | KEEP_VANILLA ? PM de base ou de d?sactivation ; absence de gate intentionnelle. |
| `pm_market_squares` | `building_urban_center` | `pmg_amenities` | `{ professional_civil_engineering }` | `{ professional_civil_engineering }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_mechanized_looms` | `building_textile_mill` | `pmg_automation_building_textile_mill` | `{ mechanized_weaving }` | `{ mechanized_weaving }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_mechanized_workshops` | `building_furniture_manufactory` | `pmg_base_building_furniture_manufactory` | `{ interchangeable_manufacture }` | `{ interchangeable_manufacture }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_military_shipbuilding_wooden_2` | NON_R?SOLU | `pmg_military_base` | `{ paddle_steamer }` | `{ paddle_steamer }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_no_steam_automation` | 5 b?timents effectifs | 5 PMG effectifs | `{ }` | `{ }` | KEEP_VANILLA ? PM de base ou de d?sactivation ; absence de gate intentionnelle. |
| `pm_philosophy_department` | `building_university` | `pmg_base_building_university` | `{ codified_practical_knowledge }` | `{ codified_practical_knowledge }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_pig_iron` | `building_tooling_workshop` | `pmg_base_building_tooling_workshop` | `{ precision_boring }` | `{ precision_boring }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_power_of_the_purse` | NON_R?SOLU | `pmg_naval_theory` | `{ state_dockyard_systems }` | `{ state_dockyard_systems }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_rail_transport_mine` | 5 b?timents effectifs | 5 PMG effectifs | `{ railways }` | `{ railways }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_road_carts` | 18 b?timents effectifs | 18 PMG effectifs | `{ }` | `{ }` | KEEP_VANILLA ? PM de base ou de d?sactivation ; absence de gate intentionnelle. |
| `pm_rotary_valve_engine_building_arms_industry` | `building_arms_industry`<br>`building_artillery_foundry` | `pmg_automation_building_arms_industry` | `{ rotary_valve_engine }` | `{ rotary_valve_engine }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_rotary_valve_engine_building_furniture_manufactory` | `building_furniture_manufactory` | `pmg_automation_building_furniture_manufactory` | `{ rotary_valve_engine }` | `{ rotary_valve_engine }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_rotary_valve_engine_building_motor_industry` | `building_motor_industry` | `pmg_automation_building_motor_industry` | `{ rotary_valve_engine }` | `{ rotary_valve_engine }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_rotary_valve_engine_building_munition_plant` | `building_munition_plant` | `pmg_automation_building_munition_plant` | `{ rotary_valve_engine }` | `{ rotary_valve_engine }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_rotary_valve_engine_building_paper_mill` | `building_paper_mill` | `pmg_automation_building_paper_mill` | `{ rotary_valve_engine }` | `{ rotary_valve_engine }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_rotary_valve_engine_building_steel_mill` | `building_steel_mill` | `pmg_automation_building_steel_mill` | `{ rotary_valve_engine }` | `{ rotary_valve_engine }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_rotary_valve_engine_building_tooling_workshop` | `building_tooling_workshop` | `pmg_automation_building_tooling_workshop` | `{ rotary_valve_engine }` | `{ rotary_valve_engine }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_saw_mills` | `building_logging_camp` | `pmg_base_building_logging_camp` | `{ mechanical_tools }` | `{ mechanical_tools }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_sewing_machines` | `building_textile_mill` | `pmg_base_building_textile_mill` | `{ mechanized_spinning }` | `{ mechanized_spinning }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_sheep_farms` | `building_livestock_ranch` | `pmg_sheep_ranch` | `{ selective_breeding }` | `{ selective_breeding }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_soil_enriching_farming` | 4 b?timents effectifs | 4 PMG effectifs | `{ advanced_crop_rotations }` | `{ advanced_crop_rotations }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_soil_enriching_farming_building_rice_farm` | `building_rice_farm` | `pmg_base_building_rice_farm` | `{ advanced_crop_rotations }` | `{ advanced_crop_rotations }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_steam_donkey_building_coal_mine` | `building_coal_mine` | `pmg_steam_automation_building_coal_mine` | `{ steam_donkey }` | `{ steam_donkey }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_steam_donkey_mine` | 4 b?timents effectifs | 4 PMG effectifs | `{ steam_donkey }` | `{ steam_donkey }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_steam_rail_transport` | 11 b?timents effectifs | 11 PMG effectifs | `{ railways }` | `{ railways }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_steam_trawlers` | `building_fishing_wharf` | `pmg_base_building_fishing_wharf` | `{ watertube_boiler }` | `{ watertube_boiler }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_steam_whaling_ships` | `building_whaling_station` | `pmg_base_building_whaling_station` | `{ watertube_boiler }` | `{ watertube_boiler }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_sugar_beets` | `building_rye_farm`<br>`building_wheat_farm` | `pmg_secondary_building_rye_farm`<br>`pmg_secondary_building_wheat_farm` | `{ sugar_refining }` | `{ sugar_refining }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_sulfite_pulping` | `building_paper_mill` | `pmg_base_building_paper_mill` | `{ continuous_papermaking }` | `{ continuous_papermaking }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_sweeteners` | `building_food_industry` | `pmg_base_building_food_industry` | `{ sugar_refining }` | `{ sugar_refining }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_tools` | 4 b?timents effectifs | 4 PMG effectifs | `{ improved_agricultural_implements }` | `{ improved_agricultural_implements }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_trade_center_trade_quantity_high` | `building_trade_center` | `pmg_trade_quantity_trade_center` | `{ mechanized_naval_dockyards }` | `{ mechanized_naval_dockyards }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_traditional_looms` | `building_textile_mill` | `pmg_automation_building_textile_mill` | `{ }` | `{ }` | KEEP_VANILLA ? PM de base ou de d?sactivation ; absence de gate intentionnelle. |
| `pm_vertical_filing_cabinets` | `building_government_administration` | `pmg_base_building_government_administration` | `{ central_statistical_offices }` | `{ central_statistical_offices }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `pm_watertube_boiler_building_furniture_manufactory` | `building_furniture_manufactory` | `pmg_automation_building_furniture_manufactory` | `{ watertube_boiler }` | `{ watertube_boiler }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_watertube_boiler_building_motor_industry` | `building_motor_industry` | `pmg_automation_building_motor_industry` | `{ watertube_boiler }` | `{ watertube_boiler }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_watertube_boiler_building_paper_mill` | `building_paper_mill` | `pmg_automation_building_paper_mill` | `{ watertube_boiler }` | `{ watertube_boiler }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_watertube_boiler_building_steel_mill` | `building_steel_mill` | `pmg_automation_building_steel_mill` | `{ watertube_boiler }` | `{ watertube_boiler }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `pm_watertube_boiler_building_tooling_workshop` | `building_tooling_workshop` | `pmg_automation_building_tooling_workshop` | `{ watertube_boiler }` | `{ watertube_boiler }` | KEEP_VANILLA ? gate active et adapt?e au stade d?automatisation. |
| `steam_powered_evaporation_sugar` | `building_sugar_plantation` | `pmg_refinement_building_sugar_plantation` | `{ watertube_boiler; sugar_refining }` | `{ watertube_boiler; sugar_refining }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |
| `vacuum_pan_sugar` | `building_sugar_plantation` | `pmg_refinement_building_sugar_plantation` | `{ high_pressure_steam; sugar_refining }` | `{ high_pressure_steam; sugar_refining }` | ALREADY_FIXED ? gate active et coh?rente avec la cha?ne du proc?d?. |

## 4. Cat?gories

### KEEP_VANILLA

Les 35 PM de cette cat?gorie conservent leur gate vanilla ou leur absence de gate. Cela comprend les m?thodes de base/d?sactivation, les automatismes ? chaudi?res, moteurs rotatifs, convoyeurs et chemins de fer, ainsi que les sept PM utilisant directement electrical_generation ou electrical_capacitors.

### ALREADY_FIXED

Les 52 PM de cette cat?gorie diff?rent de la gate vanilla 1.13.9, mais leur rattachement courant a d?j? ?t? corrig? avant TECH4C4. Sont notamment confirm?es les familles textile, papier, verre/c?ramique, pompage minier, irrigation, raffinage du sucre, administration, g?nie civil et construction navale.

### CHANGE_REQUIRED

Aucun PM. Aucune gate absente, supprim?e, inconnue ou non recherchable n?est utilis?e dans l??chantillon cibl?.

### REVIEW_REQUIRED

Aucun PM. Les correspondances indirectes examin?es restent justifi?es par les intrants et la position dans leur PMG : precision_boring pour les premiers ?quipements outill?s du caf? et les moules ? tabac, mechanized_spinning avant la couture m?canis?e, puis mechanized_weaving pour les m?tiers m?caniques.

## 5. Liste finale des modifications n?cessaires

**Aucune modification gameplay propos?e.**

En particulier :

- ne pas modifier les PM ?lectriques ;
- ne pas modifier les PM d?j? valid?s par TECH4C3 ;
- ne pas ajouter de pr?requis aux PM d?automatisation vanilla actifs ;
- ne pas toucher aux b?timents, PMG, recettes ou IDs.

## 6. Validation

- IDs PM de l??tat post-TECH4C3 perdus : 0
- PM cr??s par TECH4C4 : 0
- PM supprim?s par TECH4C4 : 0
- R?f?rences technologiques invalides dans l??chantillon : 0
- Technologies can_research = no utilis?es dans l??chantillon : 0
- Fichiers gameplay modifi?s par TECH4C4 : 0
- Validation runtime : non ex?cut?e ; aucune modification gameplay ? tester

`TECH4C4_AUDIT_PASS`

