# TECH-1A — Vanilla Technology Overlap & Effect Audit

## 1. Executive summary

Direct audit of the certified Victoria 3 1.13.9 copy at C:/Games/Victoria 3 found 179 vanilla technology definitions: 57 Production, 58 Military and 64 Society. The expected 179 baseline is confirmed. The scan indexed 3476 relevant source occurrences and 1236 distinct technology-to-gate, prerequisite, modifier or on-research relations. No gameplay file was edited.

The six frozen V1 inputs were read from docs/reports/technology. They are research baselines, not implemented nodes. Recommendations remain non-canonical until human review.

## 2. Baseline validation

| Check | Result |
|---|---|
| Certified source | 1.13.9 (Matcha), release/1.13.9 |
| Production | 57 / expected 57 |
| Military | 58 / expected 58 |
| Society | 64 / expected 64 |
| Total | 179 / expected 179 |
| VANILLA_TECH_BASELINE_MISMATCH | NO |
| Explicit ai_weight blocks | 179 |
| Research-disabled definitions | sericulture |

The active Steam install is 1.13.11, but its three technology definition files are SHA-256-identical to the certified 1.13.9 copy. All indexed paths come from the certified copy.

## 3. Counts by category / era

| Era | Production | Military | Society | Total |
|---|---:|---:|---:|---:|
| era_1 | 9 | 12 | 18 | 39 |
| era_2 | 13 | 10 | 15 | 38 |
| era_3 | 15 | 13 | 13 | 41 |
| era_4 | 15 | 13 | 10 | 38 |
| era_5 | 5 | 10 | 8 | 23 |
| Total | 57 | 58 | 64 | 179 |

## 4. Complete vanilla technology map

| Technology | Category | Era | Current prerequisites | Indexed relations | References |
|---|---|---|---|---:|---:|
| admiralty | Military | era_1 | navigation | 1 | 11 |
| army_reserves | Military | era_1 | line_infantry | 1 | 8 |
| artillery | Military | era_1 | gunsmithing | 2 | 91 |
| drydocks | Military | era_1 | navigation | 1 | 6 |
| gunsmithing | Military | era_1 | standing_army | 5 | 20 |
| line_infantry | Military | era_1 | mandatory_service;military_drill | 4 | 14 |
| mandatory_service | Military | era_1 | standing_army | 3 | 13 |
| military_drill | Military | era_1 | standing_army | 3 | 10 |
| napoleonic_warfare | Military | era_1 | line_infantry;artillery | 4 | 21 |
| navigation | Military | era_1 | ROOT | 4 | 13 |
| paddle_steamer | Military | era_1 | admiralty | 0 | 3 |
| standing_army | Military | era_1 | ROOT | 3 | 12 |
| field_works | Military | era_2 | napoleonic_warfare | 1 | 5 |
| general_staff | Military | era_2 | army_reserves | 6 | 43 |
| hydraulic_cranes | Military | era_2 | drydocks | 3 | 8 |
| logistics | Military | era_2 | napoleonic_warfare;army_reserves | 2 | 12 |
| percussion_cap | Military | era_2 | gunsmithing | 2 | 14 |
| power_of_the_purse | Military | era_2 | admiralty | 3 | 7 |
| rifling | Military | era_2 | percussion_cap | 3 | 69 |
| screw_frigate | Military | era_2 | paddle_steamer | 4 | 16 |
| shell_gun | Military | era_2 | artillery | 5 | 10 |
| triage | Military | era_2 | logistics | 2 | 6 |
| breech_loading_artillery | Military | era_3 | rifling;shell_gun | 5 | 24 |
| electric_telegraph | Military | era_3 | logistics | 2 | 15 |
| enlistment_offices | Military | era_3 | logistics | 1 | 12 |
| floating_harbor | Military | era_3 | gantry_cranes | 1 | 4 |
| gantry_cranes | Military | era_3 | hydraulic_cranes;screw_frigate | 11 | 24 |
| handcranked_machine_gun | Military | era_3 | repeaters;breech_loading_artillery | 0 | 9 |
| ironclad_tech | Military | era_3 | screw_frigate | 15 | 49 |
| jeune_ecole | Military | era_3 | self_propelled_torpedoes | 2 | 6 |
| military_statistics | Military | era_3 | electric_telegraph;general_staff | 3 | 78 |
| modern_nursing | Military | era_3 | triage | 2 | 11 |
| monitor_tech | Military | era_3 | ironclad_tech;breech_loading_artillery | 9 | 14 |
| repeaters | Military | era_3 | rifling | 1 | 28 |
| self_propelled_torpedoes | Military | era_3 | power_of_the_purse | 3 | 10 |
| automatic_machine_guns | Military | era_4 | handcranked_machine_gun;bolt_action_rifles | 3 | 58 |
| bolt_action_rifles | Military | era_4 | repeaters | 3 | 117 |
| concrete_dockyards | Military | era_4 | floating_harbor | 2 | 11 |
| defense_in_depth | Military | era_4 | trench_works;handcranked_machine_gun | 1 | 9 |
| dreadnought_tech | Military | era_4 | pre_dreadnought_tech;sea_lane_strategies;concrete_dockyards;military_aviation | 9 | 15 |
| landing_craft | Military | era_4 | jeune_ecole;monitor_tech | 1 | 5 |
| military_aviation | Military | era_4 | handcranked_machine_gun | 2 | 16 |
| pre_dreadnought_tech | Military | era_4 | ironclad_tech | 12 | 15 |
| sea_lane_strategies | Military | era_4 | jeune_ecole | 8 | 14 |
| submarine | Military | era_4 | self_propelled_torpedoes | 1 | 19 |
| trench_works | Military | era_4 | general_staff;electric_telegraph | 2 | 14 |
| war_propaganda | Military | era_4 | enlistment_offices | 0 | 4 |
| wargaming | Military | era_4 | military_statistics | 3 | 14 |
| battlefleet_tactics | Military | era_5 | battleship_tech;sea_lane_strategies | 1 | 6 |
| battleship_tech | Military | era_5 | dreadnought_tech | 5 | 11 |
| carrier_tech | Military | era_5 | dreadnought_tech | 2 | 5 |
| chemical_warfare | Military | era_5 | automatic_machine_guns | 1 | 25 |
| concrete_fortifications | Military | era_5 | defense_in_depth | 1 | 10 |
| destroyer | Military | era_5 | monitor_tech | 3 | 31 |
| flamethrowers | Military | era_5 | trench_works;automatic_machine_guns | 1 | 9 |
| mobile_armor | Military | era_5 | concrete_fortifications;nco_training | 7 | 25 |
| nco_training | Military | era_5 | wargaming;trench_works | 4 | 17 |
| stormtroopers | Military | era_5 | wargaming;trench_works | 0 | 14 |
| cotton_gin | Production | era_1 | manufacturies | 6 | 13 |
| distillation | Production | era_1 | manufacturies | 2 | 7 |
| enclosure | Production | era_1 | ROOT | 17 | 28 |
| lathe | Production | era_1 | cotton_gin | 3 | 10 |
| manufacturies | Production | era_1 | ROOT | 9 | 17 |
| prospecting | Production | era_1 | shaft_mining | 2 | 7 |
| sericulture | Production | era_1 | ROOT | 0 | 10 |
| shaft_mining | Production | era_1 | enclosure;manufacturies | 5 | 13 |
| steelworking | Production | era_1 | shaft_mining | 9 | 21 |
| atmospheric_engine | Production | era_2 | shaft_mining | 9 | 23 |
| baking_powder | Production | era_2 | fractional_distillation | 1 | 3 |
| bessemer_process | Production | era_2 | steelworking | 6 | 14 |
| canneries | Production | era_2 | lathe | 3 | 7 |
| chemical_bleaching | Production | era_2 | crystal_glass | 5 | 10 |
| crystal_glass | Production | era_2 | lathe | 1 | 4 |
| fractional_distillation | Production | era_2 | distillation | 3 | 8 |
| intensive_agriculture | Production | era_2 | enclosure | 6 | 17 |
| mechanical_tools | Production | era_2 | lathe;steelworking | 9 | 20 |
| mechanized_workshops | Production | era_2 | canneries;mechanical_tools | 5 | 9 |
| nitroglycerin | Production | era_2 | intensive_agriculture;prospecting | 6 | 11 |
| railways | Production | era_2 | mechanical_tools;atmospheric_engine | 34 | 93 |
| watertube_boiler | Production | era_2 | atmospheric_engine | 13 | 19 |
| aniline | Production | era_3 | rubber_mastication | 2 | 6 |
| dynamite | Production | era_3 | nitroglycerin | 7 | 13 |
| electrical_generation | Production | era_3 | rotary_valve_engine | 12 | 25 |
| improved_fertilizer | Production | era_3 | intensive_agriculture | 5 | 9 |
| open_hearth_process | Production | era_3 | bessemer_process | 4 | 10 |
| pumpjacks | Production | era_3 | steam_donkey;dynamite | 23 | 39 |
| reinforced_concrete | Production | era_3 | bessemer_process | 7 | 14 |
| rotary_valve_engine | Production | era_3 | watertube_boiler | 8 | 15 |
| rubber_mastication | Production | era_3 | fractional_distillation;chemical_bleaching | 3 | 12 |
| shift_work | Production | era_3 | mechanized_workshops | 1 | 9 |
| steam_donkey | Production | era_3 | intensive_agriculture | 5 | 11 |
| steel_railway_cars | Production | era_3 | railways | 4 | 15 |
| threshing_machine | Production | era_3 | steam_donkey | 4 | 8 |
| vacuum_canning | Production | era_3 | mechanized_workshops | 2 | 5 |
| vulcanization | Production | era_3 | rubber_mastication | 2 | 9 |
| art_silk | Production | era_4 | aniline | 1 | 5 |
| automatic_bottle_blowers | Production | era_4 | vulcanization | 1 | 3 |
| combustion_engine | Production | era_4 | rotary_valve_engine | 10 | 23 |
| conveyors | Production | era_4 | vulcanization;shift_work;electrical_generation | 6 | 9 |
| electric_arc_process | Production | era_4 | open_hearth_process | 1 | 4 |
| electric_railway | Production | era_4 | electrical_capacitors;steel_railway_cars | 7 | 13 |
| electrical_capacitors | Production | era_4 | electrical_generation | 3 | 8 |
| mechanized_farming | Production | era_4 | threshing_machine | 3 | 7 |
| nitrogen_fixation | Production | era_4 | improved_fertilizer | 3 | 5 |
| pasteurization | Production | era_4 | vacuum_canning;electrical_capacitors | 3 | 11 |
| plastics | Production | era_4 | reinforced_concrete | 1 | 7 |
| pneumatic_tools | Production | era_4 | rotary_valve_engine;reinforced_concrete | 5 | 8 |
| radio | Production | era_4 | telephone | 2 | 15 |
| steam_turbine | Production | era_4 | electrical_generation | 1 | 8 |
| telephone | Production | era_4 | shift_work;electrical_generation | 5 | 15 |
| arc_welding | Production | era_5 | electric_arc_process;pneumatic_tools | 4 | 6 |
| compression_ignition | Production | era_5 | combustion_engine | 10 | 13 |
| dough_rollers | Production | era_5 | conveyors | 1 | 3 |
| flash_freezing | Production | era_5 | pasteurization | 2 | 4 |
| oil_turbine | Production | era_5 | steam_turbine | 1 | 3 |
| academia | Society | era_1 | rationalism | 4 | 21 |
| banking | Society | era_1 | currency_standards | 0 | 10 |
| centralization | Society | era_1 | tech_bureaucracy | 4 | 15 |
| colonization | Society | era_1 | international_relations | 11 | 59 |
| currency_standards | Society | era_1 | international_trade;centralization | 1 | 8 |
| democracy | Society | era_1 | rationalism | 7 | 24 |
| empiricism | Society | era_1 | academia | 4 | 38 |
| international_relations | Society | era_1 | tech_bureaucracy | 16 | 30 |
| international_trade | Society | era_1 | tech_bureaucracy | 9 | 43 |
| law_enforcement | Society | era_1 | tech_bureaucracy;urban_planning | 4 | 17 |
| mass_communication | Society | era_1 | democracy | 1 | 21 |
| medical_degrees | Society | era_1 | academia | 1 | 24 |
| rationalism | Society | era_1 | ROOT | 3 | 14 |
| romanticism | Society | era_1 | academia | 6 | 25 |
| stock_exchange | Society | era_1 | international_trade | 3 | 15 |
| tech_bureaucracy | Society | era_1 | urbanization | 2 | 13 |
| urban_planning | Society | era_1 | urbanization | 2 | 14 |
| urbanization | Society | era_1 | ROOT | 30 | 38 |
| central_archives | Society | era_2 | centralization | 4 | 15 |
| central_banking | Society | era_2 | banking | 3 | 8 |
| corporate_charters | Society | era_2 | stock_exchange | 8 | 21 |
| dialectics | Society | era_2 | empiricism | 1 | 18 |
| egalitarianism | Society | era_2 | democracy | 6 | 38 |
| joint_stock_companies | Society | era_2 | banking;corporate_charters | 2 | 7 |
| labor_movement | Society | era_2 | mass_communication;egalitarianism | 5 | 22 |
| modern_sewerage | Society | era_2 | urban_planning | 1 | 13 |
| nationalism | Society | era_2 | mass_communication;international_relations | 34 | 170 |
| organized_sports | Society | era_2 | nationalism | 0 | 3 |
| pharmaceuticals | Society | era_2 | medical_degrees | 2 | 20 |
| postal_savings | Society | era_2 | stock_exchange | 0 | 3 |
| psychiatry | Society | era_2 | empiricism | 1 | 11 |
| quinine | Society | era_2 | colonization;pharmaceuticals | 1 | 26 |
| realism | Society | era_2 | romanticism | 7 | 33 |
| anarchism | Society | era_3 | egalitarianism | 8 | 32 |
| camera | Society | era_3 | realism | 5 | 69 |
| civilizing_mission | Society | era_3 | quinine;nationalism | 16 | 47 |
| corporatism | Society | era_3 | labor_movement;nationalism | 7 | 61 |
| feminism | Society | era_3 | human_rights | 4 | 23 |
| human_rights | Society | era_3 | egalitarianism | 23 | 27 |
| identification_documents | Society | era_3 | central_archives | 1 | 7 |
| investment_banks | Society | era_3 | joint_stock_companies;mutual_funds | 0 | 7 |
| mutual_funds | Society | era_3 | central_banking;postal_savings | 3 | 11 |
| pan-nationalism | Society | era_3 | nationalism | 14 | 121 |
| philosophical_pragmatism | Society | era_3 | psychiatry | 2 | 19 |
| socialism | Society | era_3 | labor_movement;dialectics | 10 | 60 |
| steel_frame_buildings | Society | era_3 | modern_sewerage | 8 | 15 |
| central_planning | Society | era_4 | identification_documents | 8 | 16 |
| corporate_management | Society | era_4 | investment_banks | 0 | 3 |
| elevator | Society | era_4 | steel_frame_buildings | 1 | 4 |
| film | Society | era_4 | camera | 3 | 32 |
| international_exchange_standards | Society | era_4 | mutual_funds | 1 | 8 |
| malaria_prevention | Society | era_4 | civilizing_mission | 2 | 40 |
| multilateral_alliances | Society | era_4 | pan;nationalism | 0 | 4 |
| political_agitation | Society | era_4 | anarchism;socialism;corporatism | 8 | 59 |
| psychoanalysis | Society | era_4 | philosophical_pragmatism | 0 | 11 |
| zeppelins | Society | era_4 | steel_frame_buildings | 2 | 6 |
| analytical_philosophy | Society | era_5 | psychoanalysis | 1 | 3 |
| antibiotics | Society | era_5 | malaria_prevention | 0 | 19 |
| behaviorism | Society | era_5 | psychoanalysis | 0 | 3 |
| macroeconomics | Society | era_5 | international_exchange_standards;corporate_management | 0 | 2 |
| mass_propaganda | Society | era_5 | political_agitation;film | 2 | 23 |
| mass_surveillance | Society | era_5 | central_planning | 2 | 8 |
| modern_financial_instruments | Society | era_5 | international_exchange_standards | 0 | 2 |
| paved_roads | Society | era_5 | elevator | 0 | 3 |

## 5. Exact methodology

1. Parsed the three top-level 1.13.9 technology files and extracted definition file/line, era, category, icon, researchability, prerequisites, direct modifiers, on-researched effects, other properties and complete ai_weight logic.
2. Resolved English names/descriptions and verified DDS files.
3. Reconstructed the complete DAG from technology unlocking_technologies blocks.
4. Scanned base-game and installed-DLC script families across common, events, decisions, history, GUI, GFX triggers and English technology localization. Script comments and unrelated localization prose were excluded.
5. Classified occurrences by semantic context. The reference index is occurrence-level; the unlock index is relation-level.
6. Scanned the mod outside docs and .git for same-ID definitions, localization overrides and references.
7. Compared code-grounded mechanics and concepts with Production V1.1, Military V1 and Society V1; name similarity alone was rejected.

### DAG diagnostics

- Roots: 7 — enclosure, manufacturies, navigation, rationalism, sericulture, standing_army, urbanization
- Isolated definitions: 1 — sericulture
- Multiple-era or reverse-era edges: 3 — trench_works->general_staff (2->4); destroyer->monitor_tech (3->5); multilateral_alliances->nationalism (2->4)
- Cross-category prerequisite edges: 0 — none

### Readable 1700-1836 dependency/action view

| Vanilla tech | Current prerequisites | Current unlocks (IDs) | Matching V1 node(s) | Recommended action |
|---|---|---|---|---|
| admiralty | navigation | building_naval_administration | state_dockyard_systems; standardized_naval_signals;scientific_naval_architecture | SPLIT |
| army_reserves | line_infantry | mobilization_option_extra_supplies | corps_organization | RETIME |
| artillery | gunsmithing | combat_unit_type_cannon_artillery;pm_cannons | standardized_field_artillery; horse_artillery | SPLIT |
| drydocks | navigation | ship_type_ship_of_the_line | state_dockyard_systems; enclosed_dock_systems;mechanized_naval_dockyards | SPLIT |
| gunsmithing | standing_army | building_arms_industry;building_artillery_foundry;company_famae;company_trubia;company_zastava | regulated_small_arms; armament_standardization_inspection | REPLACE |
| line_infantry | mandatory_service;military_drill | combat_unit_type_cuirassiers;combat_unit_type_dragoons;combat_unit_type_line_infantry;combat_unit_type_low_tier_marines | regulated_small_arms; light_infantry_tactics | SPLIT |
| mandatory_service | standing_army | decree_enlistment_efforts;je_british_dictate_military;law_national_militia | corps_organization | REWIRE |
| military_drill | standing_army | law_diplomatic_navy;law_professional_army;law_professional_navy | light_infantry_tactics; corps_organization | REWIRE |
| napoleonic_warfare | line_infantry;artillery | combat_unit_type_lancers;combat_unit_type_mobile_artillery;je_meiji_army;je_sick_man_army | corps_organization; military_supply_services;field_engineering_pontoon_trains;standardized_field_artillery | SPLIT |
| navigation | ROOT | building_port;building_shipyard;building_whaling_station;je_portugal_and_brazil | marine_chronometry; hydrographic_surveying;ship_classification_surveying | SPLIT |
| paddle_steamer | admiralty | NO_DIRECT_UNLOCK | paddle_steam_navigation | RETIME |
| standing_army | ROOT | building_barrack;combat_unit_type_hussars;decree_violent_suppression | corps_organization; permanent_engineer_services;military_supply_services | REWIRE |
| field_works | napoleonic_warfare | pm_barbed_wire_fences | field_engineering_pontoon_trains; casemated_fortifications | REWIRE |
| general_staff | army_reserves | combat_unit_type_skirmish_infantry;law_mass_conscription;law_professional_army;pm_general_training;pm_general_training_conscription;military_assistance | professional_general_staff | RETIME |
| hydraulic_cranes | drydocks | company_imperial_arsenal;company_john_brown;pm_trade_center_trade_quantity_high | mechanized_naval_dockyards | RETIME |
| logistics | napoleonic_warfare;army_reserves | law_mass_conscription;law_professional_army | military_supply_services | REPLACE |
| percussion_cap | gunsmithing | building_munition_plant;company_oevg | percussion_ignition | RETIME |
| power_of_the_purse | admiralty | combat_unit_type_mid_tier_marines;je_brazil_navy;pm_power_of_the_purse | state_dockyard_systems | RENAME |
| rifling | percussion_cap | company_izhevsk_arms_plant;je_great_reforms_military;pm_rifles | rifle_troops; regulated_small_arms | REWIRE |
| screw_frigate | paddle_steamer | company_sudamericana_de_vapores;je_brazil_navy;pm_complex_shipbuilding;pm_military_shipbuilding_wooden_2 | iron_hull_construction | KEEP |
| shell_gun | artillery | company_la_rosada;company_skoda;pm_smoothbores;ship_mod_frigate_guns_high;ship_mod_ship_of_the_line_guns_high | naval_shell_guns | RETIME |
| triage | logistics | je_war_nursing;mobilization_option_first_aid | battlefield_evacuation; permanent_military_hospitals | SPLIT |
| electric_telegraph | logistics | company_siemens_and_halske;je_portugal_regeneration_public_works | optical_telegraph_networks | KEEP |
| enlistment_offices | logistics | law_mass_conscription | NONE | KEEP |
| military_statistics | electric_telegraph;general_staff | mobilization_option_luxurious_supplies;pm_advanced_tactics_training;pm_advanced_tactics_training_conscription | central_statistical_offices; systematic_administrative_statistics | KEEP |
| modern_nursing | triage | je_war_nursing;mobilization_option_field_hospitals | clinical_medical_education; permanent_military_hospitals | KEEP |
| cotton_gin | manufacturies | company_bombay_dyeing_company;company_dmc;company_espana_industrial;company_j_p_coats;company_madura_mills;company_mitsui | cotton_gin | RETIME |
| distillation | manufacturies | pm_pot_stills;pm_sweeteners | continuous_distillation; industrial_acids | SPLIT |
| enclosure | ROOT | building_banana_plantation;building_coffee_plantation;building_cotton_plantation;building_dye_plantation;building_livestock_ranch;building_maize_farm;building_millet_farm;building_opium_plantation; +9 more | improved_husbandry; advanced_crop_rotations | REWIRE |
| lathe | cotton_gin | pm_dye_workshops;pm_lathe;pm_leaded_glass | precision_machine_tools; precision_boring | MERGE |
| manufacturies | ROOT | building_food_industry;building_furniture_manufactory;building_glassworks;building_paper_mill;building_textile_mill;building_tooling_workshop;decree_encourage_manufacturing_industry;je_spa_economic_regeneration_light_industry; +1 more | interchangeable_manufacture; mechanized_spinning;mechanized_weaving;precision_machine_tools | SPLIT |
| prospecting | shaft_mining | building_gold_field;building_gold_mine | applied_mineralogy; geological_surveying | SPLIT |
| sericulture | ROOT | NO_DIRECT_UNLOCK | NONE | KEEP |
| shaft_mining | enclosure;manufacturies | building_coal_mine;building_iron_mine;building_lead_mine;building_sulfur_mine;decree_encourage_resource_industry | shaft_mining | RETIME |
| steelworking | shaft_mining | building_steel_mill;company_altos_hornos_de_vizcaya;company_duro_y_compania;company_john_brown;company_krupp;company_lilpop;company_schneider_creusot;pm_pig_iron; +1 more | coke_smelting; puddling_and_rolling;hot_blast_smelting | SPLIT |
| atmospheric_engine | shaft_mining | building_motor_industry;company_nokia;pm_atmospheric_engine_pump_building_coal_mine;pm_atmospheric_engine_pump_building_gold_mine;pm_atmospheric_engine_pump_building_iron_mine;pm_atmospheric_engine_pump_building_lead_mine;pm_atmospheric_engine_pump_building_sulfur_mine;ship_mod_frigate_propulsion_medium; +1 more | atmospheric_steam_engines | RETIME |
| canneries | lathe | company_ramirez;pm_cannery;pm_cannery_fish | hermetic_food_preservation | RETIME |
| chemical_bleaching | crystal_glass | company_jiangnan_weaving_bureaus;company_jingdezhen;company_konigliche_porzellan_manufaktur_meissen;pm_bleached_paper;pm_bone_china | chlorine_bleaching | RETIME |
| crystal_glass | lathe | pm_crystal_glass | pressed_glass; industrial_ceramics | RETIME |
| fractional_distillation | distillation | pm_patent_stills;pm_sugar_beets;steam_powered_evaporation_sugar | continuous_distillation | KEEP |
| intensive_agriculture | enclosure | building_chemical_plant;building_explosives_factory;je_agricultural_development;pm_sheep_farms;pm_soil_enriching_farming;pm_soil_enriching_farming_building_rice_farm | advanced_crop_rotations; selective_breeding;systematic_field_drainage;improved_agricultural_implements | SPLIT |
| mechanical_tools | lathe;steelworking | building_pena_palace;company_kablin;company_kouppas;je_pena_palace;coffee_plantation_wet_process_manual;pm_precision_tools;pm_slaughterhouses;pm_steel; +1 more | precision_machine_tools; precision_boring | MERGE |
| mechanized_workshops | canneries;mechanical_tools | coffee_plantation_mechanical_drying;coffee_plantation_wet_process_mechanical;pm_mechanized_looms;pm_mechanized_workshops;pm_sewing_machines | interchangeable_manufacture; precision_machine_tools;mechanized_weaving | SPLIT |
| railways | mechanical_tools;atmospheric_engine | building_railway;company_ansaldo;company_basileiades;company_cfr;company_cordoba_railway;company_csfa;company_fiat;company_great_indian_railway; +26 more | railway_systems | RETIME |
| watertube_boiler | atmospheric_engine | pm_condensing_engine_pump_building_coal_mine;pm_condensing_engine_pump_building_gold_mine;pm_condensing_engine_pump_building_iron_mine;pm_condensing_engine_pump_building_lead_mine;pm_condensing_engine_pump_building_sulfur_mine;pm_watertube_boiler_building_furniture_manufactory;pm_watertube_boiler_building_motor_industry;pm_watertube_boiler_building_paper_mill; +5 more | high_pressure_steam | KEEP |
| improved_fertilizer | intensive_agriculture | je_portugal_regeneration_agriculture;je_spa_economic_regeneration_master;pm_fertilization;pm_fertilization_building_rice_farm;pm_improved_fertilizer | industrial_acids; advanced_crop_rotations | KEEP |
| reinforced_concrete | bessemer_process | building_kaiserforum_1;building_manila_cathedral_monument;building_sagrada_familia_cathedral_1;je_cristo_redentor;je_kaiserforum;je_manila_cathedral;je_sagrada_familia | hydraulic_cements | KEEP |
| rotary_valve_engine | watertube_boiler | centrifugal_machine_sugar;pm_rotary_valve_engine_building_arms_industry;pm_rotary_valve_engine_building_furniture_manufactory;pm_rotary_valve_engine_building_motor_industry;pm_rotary_valve_engine_building_munition_plant;pm_rotary_valve_engine_building_paper_mill;pm_rotary_valve_engine_building_steel_mill;pm_rotary_valve_engine_building_tooling_workshop | high_pressure_steam; rotative_steam_power | KEEP |
| steam_donkey | intensive_agriculture | company_kaiping_mining;company_kirgizian_mining_company;pm_steam_donkey_building_coal_mine;pm_steam_donkey_building_logging_camp;pm_steam_donkey_mine | deep_mine_engineering | KEEP |
| threshing_machine | steam_donkey | je_portugal_regeneration_agriculture;je_spa_economic_regeneration_modernise_agriculture;pm_steam_threshers;pm_steam_threshers_building_rice_farm | mechanized_threshing | RETIME |
| academia | rationalism | building_university;je_british_dictate_universities;law_private_schools;law_terakoya | institutionalized_scientific_exchange; specialized_technical_academies;polytechnical_education;experimental_research_laboratories | SPLIT |
| banking | currency_standards | NO_DIRECT_UNLOCK | institutionalized_public_credit; commercial_insurance_markets;joint_stock_capital_markets;popular_savings_institutions | SPLIT |
| centralization | tech_bureaucracy | decree_emergency_relief;decree_road_maintenance;je_age_of_princes;pm_horizontal_drawer_cabinets | systematic_population_registration; systematic_administrative_statistics;systematic_cadastral_surveying;systematic_legal_codification | SPLIT |
| colonization | international_relations | building_suez_canal;institution_colonial_affairs;je_colonial_administration;je_conquest_of_tetouan;je_earn_recognition;je_spa_economic_regeneration_ultramar;law_colonial_exploitation;law_colonial_resettlement; +3 more | systematic_cadastral_surveying | REWIRE |
| currency_standards | international_trade;centralization | law_per_capita_based_taxation | scientific_metrology; institutionalized_public_credit | SPLIT |
| democracy | rationalism | je_liberalism_1;law_census_voting;law_landed_voting;law_parliamentary_republic;law_poor_laws;law_presidential_republic;law_wealth_voting | constitutional_government; national_sovereignty;universal_rights_discourse;liberal_constitutionalism | SPLIT |
| empiricism | academia | law_public_schools;law_state_atheism;law_total_separation;liberal_party | institutionalized_scientific_exchange; codified_practical_knowledge;experimental_research_laboratories | SPLIT |
| international_relations | tech_bureaucracy | rivalry;abandon_piracy;alliance;defensive_pact;guarantee_independence;host_power_bloc_embassy;law_commitment;military_access; +8 more | institutionalized_scientific_exchange | KEEP |
| international_trade | tech_bureaucracy | embargo;je_liberalism_1;law_free_trade;law_laissez_faire;law_mercantilism;goods_transfer;no_subventions;no_tariffs; +1 more | commercial_insurance_markets; joint_stock_capital_markets;institutionalized_public_credit | SPLIT |
| law_enforcement | tech_bureaucracy;urban_planning | law_censorship;law_dedicated_police;law_national_guard;law_shinsengumi | professional_civil_policing | RETIME |
| mass_communication | democracy | je_springtime_of_the_peoples | periodical_print_networks; mechanized_printing;mass_circulation_press | SPLIT |
| medical_degrees | academia | law_charitable_health_system | clinical_medical_education | REPLACE |
| rationalism | ROOT | je_romanticism;law_freedom_of_conscience;law_religious_schools | codified_practical_knowledge; institutionalized_scientific_exchange;experimental_research_laboratories | SPLIT |
| romanticism | academia | building_art_academy;decree_greener_grass_campaign;je_realism;je_romanticism;law_agrarianism;law_industry_banned | NONE | KEEP |
| stock_exchange | international_trade | law_protectionism;free_trade_party;foreign_investment_rights | joint_stock_capital_markets | MERGE |
| tech_bureaucracy | urbanization | building_government_administration;law_local_police | systematic_administrative_statistics; central_statistical_offices;systematic_population_registration;systematic_legal_codification | SPLIT |
| urban_planning | urbanization | pm_iron_frame_buildings;pm_market_squares | professional_civil_engineering; systematic_cadastral_surveying | REWIRE |
| urbanization | ROOT | bg_agriculture;bg_army_logistics_center;bg_canals;bg_company_headquarter;bg_company_regional_headquarter;bg_conscription;bg_construction;bg_financial_districts; +22 more | professional_civil_engineering; turnpike_road_networks | RETIME |
| central_archives | centralization | je_technocracy;law_secret_police;law_technocracy;pm_vertical_filing_cabinets | systematic_administrative_statistics; systematic_population_registration;central_statistical_offices;systematic_legal_codification | SPLIT |
| central_banking | banking | fund_lobbies;money_transfer;take_on_debt | institutionalized_public_credit | MERGE |
| corporate_charters | stock_exchange | company_egyptian_rail;company_guinness;company_imperial_tobacco;company_misr;company_nam_dinh;company_san_miguel;company_united_tobacco_factories;acquire_monopoly_for_company | joint_stock_capital_markets | MERGE |
| dialectics | empiricism | pm_philosophy_department | early_socialism_cooperativism | RETIME |
| egalitarianism | democracy | je_donghak_movement;je_spanish_anarchism;je_springtime_of_the_peoples;law_proportional_taxation;law_universal_suffrage;radical_party | universal_rights_discourse; constitutional_government;national_sovereignty;abolitionist_mobilization | SPLIT |
| joint_stock_companies | banking;corporate_charters | company_cgv;company_savva_morozov | joint_stock_capital_markets | MERGE |
| labor_movement | mass_communication;egalitarianism | je_sol_1;law_regulatory_bodies;law_restricted_child_labor;law_wage_subsidies;social_democrat_party | organized_labor_movements | RETIME |
| modern_sewerage | urban_planning | je_sol_1 | professional_civil_engineering | KEEP |
| nationalism | mass_communication;international_relations | decree_promote_national_values;support_separatism;je_alaska;je_australia_aus;je_australia_gbr;je_autocracy;je_balkan_national_awakenings;je_boxer_rebellion; +26 more | national_sovereignty; liberal_constitutionalism | SPLIT |
| organized_sports | nationalism | NO_DIRECT_UNLOCK | NONE | KEEP |
| pharmaceuticals | medical_degrees | law_private_health_insurance;law_public_health_insurance | active_principle_pharmacy; clinicopathological_medicine;organized_immunization_campaigns | SPLIT |
| postal_savings | stock_exchange | NO_DIRECT_UNLOCK | popular_savings_institutions | RETIME |
| psychiatry | empiricism | je_positivist_movement | clinical_medical_education | RETIME |
| quinine | colonization;pharmaceuticals | je_scramble_for_africa | active_principle_pharmacy | RETIME |
| anarchism | egalitarianism | je_communism_1;je_nihilist_movement;je_populist_unrest;je_prohibition;je_spanish_anarchism;je_the_paris_commune_display;law_anarchy;anarchist_party | early_socialism_cooperativism | KEEP |
| feminism | human_rights | je_liberalism_1;je_suffragists;law_women_in_the_workplace;law_womens_suffrage | universal_rights_discourse | KEEP |
| human_rights | egalitarianism | je_donghak_movement;je_dravidian_movement;je_sol_1;je_strike;je_suffragists;lawgroup_childrens_rights;lawgroup_free_speech;lawgroup_labor_rights; +15 more | universal_rights_discourse | REPLACE |
| socialism | labor_movement;dialectics | je_communism_1;je_nihilist_movement;je_populist_unrest;je_prohibition;je_the_paris_commune_display;law_collectivized_agriculture;law_council_republic;law_factory_councils; +2 more | early_socialism_cooperativism; organized_labor_movements | RETIME |

## 6. Audit Production

| Tech | Era | Relevance | Best V1 match | Overlap | Action | Target |
|---|---|---|---|---|---|---|
| cotton_gin | era_1 | DIRECT_1700_1836 | cotton_gin | EXACT | RETIME | ERA IV |
| distillation | era_1 | DIRECT_1700_1836 | continuous_distillation | VANILLA_BROADER | SPLIT | ERA VI |
| enclosure | era_1 | DIRECT_1700_1836 | improved_husbandry | PARTIAL | REWIRE | ERA I |
| lathe | era_1 | DIRECT_1700_1836 | precision_machine_tools | STRONG | MERGE | ERA V |
| manufacturies | era_1 | DIRECT_1700_1836 | interchangeable_manufacture | VANILLA_BROADER | SPLIT | ERA VI |
| prospecting | era_1 | DIRECT_1700_1836 | applied_mineralogy | VANILLA_BROADER | SPLIT | ERA III |
| sericulture | era_1 | DIRECT_1700_1836 | NONE | NONE | KEEP | ERA I / REGIONAL LEGACY START |
| shaft_mining | era_1 | DIRECT_1700_1836 | shaft_mining | EXACT | RETIME | ERA I |
| steelworking | era_1 | DIRECT_1700_1836 | coke_smelting | VANILLA_BROADER | SPLIT | ERA I |
| atmospheric_engine | era_2 | DIRECT_1700_1836 | atmospheric_steam_engines | EXACT | RETIME | ERA I |
| baking_powder | era_2 | POST_1836_ONLY | NONE | NONE | KEEP | era_2 (preserve post-1836) |
| bessemer_process | era_2 | POST_1836_ONLY | NONE | NONE | KEEP | era_2 (preserve post-1836) |
| canneries | era_2 | DIRECT_1700_1836 | hermetic_food_preservation | EXACT | RETIME | ERA V |
| chemical_bleaching | era_2 | DIRECT_1700_1836 | chlorine_bleaching | EXACT | RETIME | ERA IV |
| crystal_glass | era_2 | DIRECT_1700_1836 | pressed_glass | PARTIAL | RETIME | ERA VI |
| fractional_distillation | era_2 | CROSS_PERIOD | continuous_distillation | STRONG | KEEP | ERA VI |
| intensive_agriculture | era_2 | DIRECT_1700_1836 | advanced_crop_rotations | VANILLA_BROADER | SPLIT | ERA III |
| mechanical_tools | era_2 | DIRECT_1700_1836 | precision_machine_tools | STRONG | MERGE | ERA V |
| mechanized_workshops | era_2 | CROSS_PERIOD | interchangeable_manufacture | VANILLA_BROADER | SPLIT | ERA VI |
| nitroglycerin | era_2 | POST_1836_ONLY | NONE | NONE | KEEP | era_2 (preserve post-1836) |
| railways | era_2 | DIRECT_1700_1836 | railway_systems | EXACT | RETIME | ERA VI |
| watertube_boiler | era_2 | CROSS_PERIOD | high_pressure_steam | PARTIAL | KEEP | ERA V |
| aniline | era_3 | POST_1836_ONLY | industrial_alkalis | PARTIAL | KEEP | ERA V |
| dynamite | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| electrical_generation | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| improved_fertilizer | era_3 | CROSS_PERIOD | industrial_acids | PARTIAL | KEEP | ERA II |
| open_hearth_process | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| pumpjacks | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| reinforced_concrete | era_3 | CROSS_PERIOD | hydraulic_cements | PARTIAL | KEEP | ERA VI |
| rotary_valve_engine | era_3 | CROSS_PERIOD | high_pressure_steam | V1_BROADER | KEEP | ERA V |
| rubber_mastication | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| shift_work | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| steam_donkey | era_3 | CROSS_PERIOD | deep_mine_engineering | SAME_UNLOCK_DIFFERENT_CONCEPT | KEEP | ERA IV |
| steel_railway_cars | era_3 | POST_1836_ONLY | railway_systems | PARTIAL | KEEP | ERA VI |
| threshing_machine | era_3 | DIRECT_1700_1836 | mechanized_threshing | EXACT | RETIME | ERA IV |
| vacuum_canning | era_3 | POST_1836_ONLY | hermetic_food_preservation | V1_BROADER | KEEP | ERA V |
| vulcanization | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| art_silk | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| automatic_bottle_blowers | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| combustion_engine | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| conveyors | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| electric_arc_process | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| electric_railway | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| electrical_capacitors | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| mechanized_farming | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| nitrogen_fixation | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| pasteurization | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| plastics | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| pneumatic_tools | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| radio | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| steam_turbine | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| telephone | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| arc_welding | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| compression_ignition | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| dough_rollers | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| flash_freezing | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| oil_turbine | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |

## 7. Audit Military

| Tech | Era | Relevance | Best V1 match | Overlap | Action | Target |
|---|---|---|---|---|---|---|
| admiralty | era_1 | DIRECT_1700_1836 | state_dockyard_systems | VANILLA_BROADER | SPLIT | ERA I |
| army_reserves | era_1 | DIRECT_1700_1836 | corps_organization | PARTIAL | RETIME | ERA V |
| artillery | era_1 | DIRECT_1700_1836 | standardized_field_artillery | STRONG | SPLIT | ERA III |
| drydocks | era_1 | DIRECT_1700_1836 | state_dockyard_systems | VANILLA_BROADER | SPLIT | ERA I |
| gunsmithing | era_1 | DIRECT_1700_1836 | regulated_small_arms | V1_BROADER | REPLACE | ERA II |
| line_infantry | era_1 | DIRECT_1700_1836 | regulated_small_arms | PARTIAL | SPLIT | ERA II |
| mandatory_service | era_1 | DIRECT_1700_1836 | corps_organization | PARTIAL | REWIRE | ERA V |
| military_drill | era_1 | DIRECT_1700_1836 | light_infantry_tactics | PARTIAL | REWIRE | ERA III |
| napoleonic_warfare | era_1 | DIRECT_1700_1836 | corps_organization | VANILLA_BROADER | SPLIT | ERA V |
| navigation | era_1 | DIRECT_1700_1836 | marine_chronometry | VANILLA_BROADER | SPLIT | ERA III |
| paddle_steamer | era_1 | DIRECT_1700_1836 | paddle_steam_navigation | EXACT | RETIME | ERA V |
| standing_army | era_1 | DIRECT_1700_1836 | corps_organization | V1_BROADER | REWIRE | ERA V |
| field_works | era_2 | DIRECT_1700_1836 | field_engineering_pontoon_trains | STRONG | REWIRE | ERA V |
| general_staff | era_2 | DIRECT_1700_1836 | professional_general_staff | EXACT | RETIME | ERA VI |
| hydraulic_cranes | era_2 | DIRECT_1700_1836 | mechanized_naval_dockyards | STRONG | RETIME | ERA V |
| logistics | era_2 | DIRECT_1700_1836 | military_supply_services | EXACT | REPLACE | ERA V |
| percussion_cap | era_2 | DIRECT_1700_1836 | percussion_ignition | EXACT | RETIME | ERA VI |
| power_of_the_purse | era_2 | DIRECT_1700_1836 | state_dockyard_systems | PARTIAL | RENAME | ERA I |
| rifling | era_2 | DIRECT_1700_1836 | rifle_troops | PARTIAL | REWIRE | ERA V |
| screw_frigate | era_2 | CROSS_PERIOD | iron_hull_construction | SAME_UNLOCK_DIFFERENT_CONCEPT | KEEP | ERA VI |
| shell_gun | era_2 | DIRECT_1700_1836 | naval_shell_guns | EXACT | RETIME | ERA VI |
| triage | era_2 | DIRECT_1700_1836 | battlefield_evacuation | VANILLA_BROADER | SPLIT | ERA V |
| breech_loading_artillery | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| electric_telegraph | era_3 | CROSS_PERIOD | optical_telegraph_networks | CROSS_BRANCH | KEEP | ERA IV |
| enlistment_offices | era_3 | CROSS_PERIOD | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| floating_harbor | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| gantry_cranes | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| handcranked_machine_gun | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| ironclad_tech | era_3 | POST_1836_ONLY | iron_hull_construction | STRONG | KEEP | ERA VI |
| jeune_ecole | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| military_statistics | era_3 | CROSS_PERIOD | central_statistical_offices | CROSS_BRANCH | KEEP | ERA V |
| modern_nursing | era_3 | CROSS_PERIOD | clinical_medical_education | CROSS_BRANCH | KEEP | ERA III |
| monitor_tech | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| repeaters | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| self_propelled_torpedoes | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| automatic_machine_guns | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| bolt_action_rifles | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| concrete_dockyards | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| defense_in_depth | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| dreadnought_tech | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| landing_craft | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| military_aviation | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| pre_dreadnought_tech | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| sea_lane_strategies | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| submarine | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| trench_works | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| war_propaganda | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| wargaming | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| battlefleet_tactics | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| battleship_tech | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| carrier_tech | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| chemical_warfare | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| concrete_fortifications | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| destroyer | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| flamethrowers | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| mobile_armor | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| nco_training | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| stormtroopers | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |

## 8. Audit Society

| Tech | Era | Relevance | Best V1 match | Overlap | Action | Target |
|---|---|---|---|---|---|---|
| academia | era_1 | DIRECT_1700_1836 | institutionalized_scientific_exchange | VANILLA_BROADER | SPLIT | ERA I |
| banking | era_1 | DIRECT_1700_1836 | institutionalized_public_credit | VANILLA_BROADER | SPLIT | ERA I |
| centralization | era_1 | DIRECT_1700_1836 | systematic_population_registration | VANILLA_BROADER | SPLIT | ERA III |
| colonization | era_1 | DIRECT_1700_1836 | systematic_cadastral_surveying | PARTIAL | REWIRE | ERA IV |
| currency_standards | era_1 | DIRECT_1700_1836 | scientific_metrology | PARTIAL | SPLIT | ERA IV |
| democracy | era_1 | DIRECT_1700_1836 | constitutional_government | VANILLA_BROADER | SPLIT | ERA IV |
| empiricism | era_1 | DIRECT_1700_1836 | institutionalized_scientific_exchange | VANILLA_BROADER | SPLIT | ERA I |
| international_relations | era_1 | DIRECT_1700_1836 | institutionalized_scientific_exchange | NAME_COLLISION_ONLY | KEEP | ERA I |
| international_trade | era_1 | DIRECT_1700_1836 | commercial_insurance_markets | VANILLA_BROADER | SPLIT | ERA I |
| law_enforcement | era_1 | DIRECT_1700_1836 | professional_civil_policing | STRONG | RETIME | ERA VI |
| mass_communication | era_1 | DIRECT_1700_1836 | periodical_print_networks | VANILLA_BROADER | SPLIT | ERA I |
| medical_degrees | era_1 | DIRECT_1700_1836 | clinical_medical_education | EXACT | REPLACE | ERA III |
| rationalism | era_1 | DIRECT_1700_1836 | codified_practical_knowledge | VANILLA_BROADER | SPLIT | ERA III |
| romanticism | era_1 | DIRECT_1700_1836 | NONE | NONE | KEEP | ERA I-IV differentiated |
| stock_exchange | era_1 | DIRECT_1700_1836 | joint_stock_capital_markets | EXACT | MERGE | ERA I |
| tech_bureaucracy | era_1 | DIRECT_1700_1836 | systematic_administrative_statistics | VANILLA_BROADER | SPLIT | ERA II |
| urban_planning | era_1 | DIRECT_1700_1836 | professional_civil_engineering | CROSS_BRANCH | REWIRE | ERA V |
| urbanization | era_1 | DIRECT_1700_1836 | professional_civil_engineering | CROSS_BRANCH | RETIME | ERA V |
| central_archives | era_2 | DIRECT_1700_1836 | systematic_administrative_statistics | VANILLA_BROADER | SPLIT | ERA II |
| central_banking | era_2 | DIRECT_1700_1836 | institutionalized_public_credit | STRONG | MERGE | ERA I |
| corporate_charters | era_2 | DIRECT_1700_1836 | joint_stock_capital_markets | STRONG | MERGE | ERA I |
| dialectics | era_2 | DIRECT_1700_1836 | early_socialism_cooperativism | PARTIAL | RETIME | ERA VI |
| egalitarianism | era_2 | DIRECT_1700_1836 | universal_rights_discourse | VANILLA_BROADER | SPLIT | ERA IV |
| joint_stock_companies | era_2 | DIRECT_1700_1836 | joint_stock_capital_markets | EXACT | MERGE | ERA I |
| labor_movement | era_2 | DIRECT_1700_1836 | organized_labor_movements | EXACT | RETIME | ERA VI |
| modern_sewerage | era_2 | CROSS_PERIOD | professional_civil_engineering | CROSS_BRANCH | KEEP | ERA V |
| nationalism | era_2 | DIRECT_1700_1836 | national_sovereignty | VANILLA_BROADER | SPLIT | ERA IV |
| organized_sports | era_2 | CROSS_PERIOD | NONE | NONE | KEEP | era_2 (preserve post-1836) |
| pharmaceuticals | era_2 | DIRECT_1700_1836 | active_principle_pharmacy | VANILLA_BROADER | SPLIT | ERA V |
| postal_savings | era_2 | DIRECT_1700_1836 | popular_savings_institutions | EXACT | RETIME | ERA V |
| psychiatry | era_2 | DIRECT_1700_1836 | clinical_medical_education | PARTIAL | RETIME | ERA III |
| quinine | era_2 | DIRECT_1700_1836 | active_principle_pharmacy | STRONG | RETIME | ERA V |
| realism | era_2 | POST_1836_ONLY | NONE | NONE | KEEP | era_2 (preserve post-1836) |
| anarchism | era_3 | CROSS_PERIOD | early_socialism_cooperativism | PARTIAL | KEEP | ERA VI |
| camera | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| civilizing_mission | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| corporatism | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| feminism | era_3 | CROSS_PERIOD | universal_rights_discourse | PARTIAL | KEEP | ERA IV |
| human_rights | era_3 | DIRECT_1700_1836 | universal_rights_discourse | EXACT | REPLACE | ERA IV |
| identification_documents | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| investment_banks | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| mutual_funds | era_3 | POST_1836_ONLY | popular_savings_institutions | PARTIAL | KEEP | ERA V |
| pan-nationalism | era_3 | POST_1836_ONLY | national_sovereignty | PARTIAL | KEEP | ERA IV |
| philosophical_pragmatism | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| socialism | era_3 | DIRECT_1700_1836 | early_socialism_cooperativism | STRONG | RETIME | ERA VI |
| steel_frame_buildings | era_3 | POST_1836_ONLY | NONE | NONE | KEEP | era_3 (preserve post-1836) |
| central_planning | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| corporate_management | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| elevator | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| film | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| international_exchange_standards | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| malaria_prevention | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| multilateral_alliances | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| political_agitation | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| psychoanalysis | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| zeppelins | era_4 | POST_1836_ONLY | NONE | NONE | KEEP | era_4 (preserve post-1836) |
| analytical_philosophy | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| antibiotics | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| behaviorism | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| macroeconomics | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| mass_propaganda | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| mass_surveillance | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| modern_financial_instruments | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |
| paved_roads | era_5 | POST_1836_ONLY | NONE | NONE | KEEP | era_5 (preserve post-1836) |

## 9. High-risk overlaps

- admiralty: VANILLA_BROADER with Military V1 / state_dockyard_systems; SPLIT. VANILLA_BROADER overlap with state_dockyard_systems: Naval administration is broader than a technical node.
- artillery: STRONG with Military V1 / standardized_field_artillery; SPLIT. STRONG overlap with standardized_field_artillery: Broad artillery gateway versus standardized systems and specialization.
- drydocks: VANILLA_BROADER with Military V1 / state_dockyard_systems; SPLIT. VANILLA_BROADER overlap with state_dockyard_systems: State arsenals, commercial docks and later mechanization are conflated.
- gunsmithing: V1_BROADER with Military V1 / regulated_small_arms; REPLACE. V1_BROADER overlap with regulated_small_arms: V1 frames regulated and inspected arms supply rather than generic craft.
- napoleonic_warfare: VANILLA_BROADER with Military V1 / corps_organization; SPLIT. VANILLA_BROADER overlap with corps_organization: Several operational and organizational reforms are compressed.
- navigation: VANILLA_BROADER with Military V1 / marine_chronometry; SPLIT. VANILLA_BROADER overlap with marine_chronometry: Generic navigation bundles chronometry, hydrography and surveying.
- paddle_steamer: EXACT with Military V1 / paddle_steam_navigation; RETIME. EXACT overlap with paddle_steam_navigation: Same early steam-navigation transition.
- standing_army: V1_BROADER with Military V1 / corps_organization; REWIRE. V1_BROADER overlap with corps_organization: Standing armies are an institutional baseline; V1 models later services.
- field_works: STRONG with Military V1 / field_engineering_pontoon_trains; REWIRE. STRONG overlap with field_engineering_pontoon_trains: Same engineering family, with field/permanent works split.
- general_staff: EXACT with Military V1 / professional_general_staff; RETIME. EXACT overlap with professional_general_staff: Same professional general-staff institution.
- hydraulic_cranes: STRONG with Military V1 / mechanized_naval_dockyards; RETIME. STRONG overlap with mechanized_naval_dockyards: Same dockyard mechanization/logistics family.
- logistics: EXACT with Military V1 / military_supply_services; REPLACE. EXACT overlap with military_supply_services: Same organized supply-services role.
- percussion_cap: EXACT with Military V1 / percussion_ignition; RETIME. EXACT overlap with percussion_ignition: Same ignition technology.
- shell_gun: EXACT with Military V1 / naval_shell_guns; RETIME. EXACT overlap with naval_shell_guns: Same naval explosive-shell gun transition.
- triage: VANILLA_BROADER with Military V1 / battlefield_evacuation; SPLIT. VANILLA_BROADER overlap with battlefield_evacuation: Evacuation/triage and permanent care are combined.
- electric_telegraph: CROSS_BRANCH with Society V1 / optical_telegraph_networks; KEEP. CROSS_BRANCH overlap with optical_telegraph_networks: Same communication role, later electrical technology.
- military_statistics: CROSS_BRANCH with Society V1 / central_statistical_offices; KEEP. CROSS_BRANCH overlap with central_statistical_offices: Military statistics depends on state statistical capacity.
- modern_nursing: CROSS_BRANCH with Society V1 / clinical_medical_education; KEEP. CROSS_BRANCH overlap with clinical_medical_education: Military healthcare overlaps Society medical professionalization.
- cotton_gin: EXACT with Production V1.1 / cotton_gin; RETIME. EXACT overlap with cotton_gin: Same machine and plantation-processing role.
- distillation: VANILLA_BROADER with Production V1.1 / continuous_distillation; SPLIT. VANILLA_BROADER overlap with continuous_distillation: Old stills and later continuous industrial separation are conflated.
- lathe: STRONG with Production V1.1 / precision_machine_tools; MERGE. STRONG overlap with precision_machine_tools: Lathe is one member of the precision machine-tool transition.
- manufacturies: VANILLA_BROADER with Production V1.1 / interchangeable_manufacture; SPLIT. VANILLA_BROADER overlap with interchangeable_manufacture: Broad factory-building gateway covering distinct production transitions.
- prospecting: VANILLA_BROADER with Production V1.1 / applied_mineralogy; SPLIT. VANILLA_BROADER overlap with applied_mineralogy: Resource discovery combines practical mineralogy and state survey capacity.
- shaft_mining: EXACT with Production V1.1 / shaft_mining; RETIME. EXACT overlap with shaft_mining: Same mining-depth concept and general PM/building role.
- steelworking: VANILLA_BROADER with Production V1.1 / coke_smelting; SPLIT. VANILLA_BROADER overlap with coke_smelting: Generic steelworking compresses multiple iron and steel process ruptures.
- atmospheric_engine: EXACT with Production V1.1 / atmospheric_steam_engines; RETIME. EXACT overlap with atmospheric_steam_engines: Same Newcomen-type practical steam-pumping concept.
- canneries: EXACT with Production V1.1 / hermetic_food_preservation; RETIME. EXACT overlap with hermetic_food_preservation: Same Appert-style preservation transition and canning role.
- chemical_bleaching: EXACT with Production V1.1 / chlorine_bleaching; RETIME. EXACT overlap with chlorine_bleaching: Same chlorine bleaching transition.
- fractional_distillation: STRONG with Production V1.1 / continuous_distillation; KEEP. STRONG overlap with continuous_distillation: Closely related continuous/fractionating industrial separation.
- intensive_agriculture: VANILLA_BROADER with Production V1.1 / advanced_crop_rotations; SPLIT. VANILLA_BROADER overlap with advanced_crop_rotations: Vanilla combines several agronomic transitions.
- mechanical_tools: STRONG with Production V1.1 / precision_machine_tools; MERGE. STRONG overlap with precision_machine_tools: Same machine-tool capability at different granularity.
- mechanized_workshops: VANILLA_BROADER with Production V1.1 / interchangeable_manufacture; SPLIT. VANILLA_BROADER overlap with interchangeable_manufacture: Broad workshop mechanization overlaps several mechanisms.
- railways: EXACT with Production V1.1 / railway_systems; RETIME. EXACT overlap with railway_systems: Same railway-system frontier concept.
- rotary_valve_engine: V1_BROADER with Production V1.1 / high_pressure_steam; KEEP. V1_BROADER overlap with high_pressure_steam: V1 separates high-pressure and rotative steam transitions.
- threshing_machine: EXACT with Production V1.1 / mechanized_threshing; RETIME. EXACT overlap with mechanized_threshing: Same agricultural machine and role.
- academia: VANILLA_BROADER with Society V1 / institutionalized_scientific_exchange; SPLIT. VANILLA_BROADER overlap with institutionalized_scientific_exchange: Generic academia spans several institutional stages.
- banking: VANILLA_BROADER with Society V1 / institutionalized_public_credit; SPLIT. VANILLA_BROADER overlap with institutionalized_public_credit: Generic banking collapses several institutions.
- centralization: VANILLA_BROADER with Society V1 / systematic_population_registration; SPLIT. VANILLA_BROADER overlap with systematic_population_registration: Centralization is an outcome composed of administrative technologies.
- democracy: VANILLA_BROADER with Society V1 / constitutional_government; SPLIT. VANILLA_BROADER overlap with constitutional_government: Constitutional form, sovereignty, citizenship and later liberal politics are combined.
- empiricism: VANILLA_BROADER with Society V1 / institutionalized_scientific_exchange; SPLIT. VANILLA_BROADER overlap with institutionalized_scientific_exchange: Philosophy label carries distinct institutional roles.
- international_trade: VANILLA_BROADER with Society V1 / commercial_insurance_markets; SPLIT. VANILLA_BROADER overlap with commercial_insurance_markets: Broad trade node bundles market institutions.
- law_enforcement: STRONG with Society V1 / professional_civil_policing; RETIME. STRONG overlap with professional_civil_policing: Same policing professionalization role.
- mass_communication: VANILLA_BROADER with Society V1 / periodical_print_networks; SPLIT. VANILLA_BROADER overlap with periodical_print_networks: Several print and mass-media stages are combined.
- medical_degrees: EXACT with Society V1 / clinical_medical_education; REPLACE. EXACT overlap with clinical_medical_education: Same credentialed clinical medical education.
- rationalism: VANILLA_BROADER with Society V1 / codified_practical_knowledge; SPLIT. VANILLA_BROADER overlap with codified_practical_knowledge: Philosophical label carries broad knowledge-system effects.
- stock_exchange: EXACT with Society V1 / joint_stock_capital_markets; MERGE. EXACT overlap with joint_stock_capital_markets: V1 explicitly merges Stock Exchange into this node.
- tech_bureaucracy: VANILLA_BROADER with Society V1 / systematic_administrative_statistics; SPLIT. VANILLA_BROADER overlap with systematic_administrative_statistics: Distinct administrative information capacities are compressed.
- urban_planning: CROSS_BRANCH with Production V1.1 / professional_civil_engineering; REWIRE. CROSS_BRANCH overlap with professional_civil_engineering: Planning depends on engineering and cadastral administration.
- urbanization: CROSS_BRANCH with Production V1.1 / professional_civil_engineering; RETIME. CROSS_BRANCH overlap with professional_civil_engineering: Urban growth infrastructure overlaps Production civil engineering.
- central_archives: VANILLA_BROADER with Society V1 / systematic_administrative_statistics; SPLIT. VANILLA_BROADER overlap with systematic_administrative_statistics: Archives support several information systems.
- central_banking: STRONG with Society V1 / institutionalized_public_credit; MERGE. STRONG overlap with institutionalized_public_credit: Same public-credit and bank-of-issue family.
- corporate_charters: STRONG with Society V1 / joint_stock_capital_markets; MERGE. STRONG overlap with joint_stock_capital_markets: Same chartered/joint-stock institutional family.
- egalitarianism: VANILLA_BROADER with Society V1 / universal_rights_discourse; SPLIT. VANILLA_BROADER overlap with universal_rights_discourse: Broad ideology gateway overlaps political concepts.
- joint_stock_companies: EXACT with Society V1 / joint_stock_capital_markets; MERGE. EXACT overlap with joint_stock_capital_markets: Same institutional concept.
- labor_movement: EXACT with Society V1 / organized_labor_movements; RETIME. EXACT overlap with organized_labor_movements: Same organized labor concept.
- modern_sewerage: CROSS_BRANCH with Production V1.1 / professional_civil_engineering; KEEP. CROSS_BRANCH overlap with professional_civil_engineering: Sanitary infrastructure depends on engineering but is distinct.
- nationalism: VANILLA_BROADER with Society V1 / national_sovereignty; SPLIT. VANILLA_BROADER overlap with national_sovereignty: Sovereignty, identity and later mass nationalism are combined.
- pharmaceuticals: VANILLA_BROADER with Society V1 / active_principle_pharmacy; SPLIT. VANILLA_BROADER overlap with active_principle_pharmacy: Drug isolation, medical science and public-health diffusion are bundled.
- postal_savings: EXACT with Society V1 / popular_savings_institutions; RETIME. EXACT overlap with popular_savings_institutions: Same popular savings institution.
- quinine: STRONG with Society V1 / active_principle_pharmacy; RETIME. STRONG overlap with active_principle_pharmacy: Key active-principle case; malaria systems extend beyond it.
- human_rights: EXACT with Society V1 / universal_rights_discourse; REPLACE. EXACT overlap with universal_rights_discourse: Same rights-and-citizenship discourse.
- socialism: STRONG with Society V1 / early_socialism_cooperativism; RETIME. STRONG overlap with early_socialism_cooperativism: Same early socialist/cooperative family, extending into later socialism.

## 10. Retiming candidates

- army_reserves -> ERA V: Broad or inherited capability needs differentiated pre-1836 timing.
- paddle_steamer -> ERA V: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- general_staff -> ERA VI: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- hydraulic_cranes -> ERA V: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- percussion_cap -> ERA VI: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- shell_gun -> ERA VI: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- cotton_gin -> ERA IV: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- shaft_mining -> ERA I: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- atmospheric_engine -> ERA I: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- canneries -> ERA V: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- chemical_bleaching -> ERA IV: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- crystal_glass -> ERA VI: Broad or inherited capability needs differentiated pre-1836 timing.
- railways -> ERA VI: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- threshing_machine -> ERA IV: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- law_enforcement -> ERA VI: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- urbanization -> ERA V: Historical dependency crosses the current vanilla category boundary.
- dialectics -> ERA VI: Broad or inherited capability needs differentiated pre-1836 timing.
- labor_movement -> ERA VI: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- postal_savings -> ERA V: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- psychiatry -> ERA III: Broad or inherited capability needs differentiated pre-1836 timing.
- quinine -> ERA V: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- socialism -> ERA VI: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.

## 11. Merge candidates

- lathe -> ERA V: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- mechanical_tools -> ERA V: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- stock_exchange -> ERA I: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- central_banking -> ERA I: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- corporate_charters -> ERA I: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- joint_stock_companies -> ERA I: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.

## 12. Split candidates

- admiralty -> ERA I: Vanilla framing compresses several historically distinct transitions.
- artillery -> ERA III: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- drydocks -> ERA I: Vanilla framing compresses several historically distinct transitions.
- line_infantry -> ERA II: Broad or inherited capability needs differentiated pre-1836 timing.
- napoleonic_warfare -> ERA V: Vanilla framing compresses several historically distinct transitions.
- navigation -> ERA III: Vanilla framing compresses several historically distinct transitions.
- triage -> ERA V: Vanilla framing compresses several historically distinct transitions.
- distillation -> ERA VI: Vanilla framing compresses several historically distinct transitions.
- manufacturies -> ERA VI: Vanilla framing compresses several historically distinct transitions.
- prospecting -> ERA III: Vanilla framing compresses several historically distinct transitions.
- steelworking -> ERA I: Vanilla framing compresses several historically distinct transitions.
- intensive_agriculture -> ERA III: Vanilla framing compresses several historically distinct transitions.
- mechanized_workshops -> ERA VI: Vanilla framing compresses several historically distinct transitions.
- academia -> ERA I: Vanilla framing compresses several historically distinct transitions.
- banking -> ERA I: Vanilla framing compresses several historically distinct transitions.
- centralization -> ERA III: Vanilla framing compresses several historically distinct transitions.
- currency_standards -> ERA IV: Broad or inherited capability needs differentiated pre-1836 timing.
- democracy -> ERA IV: Vanilla framing compresses several historically distinct transitions.
- empiricism -> ERA I: Vanilla framing compresses several historically distinct transitions.
- international_trade -> ERA I: Vanilla framing compresses several historically distinct transitions.
- mass_communication -> ERA I: Vanilla framing compresses several historically distinct transitions.
- rationalism -> ERA III: Vanilla framing compresses several historically distinct transitions.
- tech_bureaucracy -> ERA II: Vanilla framing compresses several historically distinct transitions.
- central_archives -> ERA II: Vanilla framing compresses several historically distinct transitions.
- egalitarianism -> ERA IV: Vanilla framing compresses several historically distinct transitions.
- nationalism -> ERA IV: Vanilla framing compresses several historically distinct transitions.
- pharmaceuticals -> ERA V: Vanilla framing compresses several historically distinct transitions.

## 13. Replace candidates

- gunsmithing -> ERA II: Broad or inherited capability needs differentiated pre-1836 timing.
- logistics -> ERA V: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- medical_degrees -> ERA III: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.
- human_rights -> ERA IV: Usable concept; timing and granularity must be reconciled with the 1700-1836 V1 node.

## 14. Remove candidates

None. REMOVE is intentionally not recommended without a strongly evidenced redundant node.

## 15. Regionalization candidates

- sericulture: Ancient regional legacy; differentiated starting knowledge by 1700. Candidate only; no conversion is applied.
- quinine: 1803–1820s. Candidate only; no conversion is applied.

## 16. Mod overrides already present

| Status | Count |
|---|---:|
| REFERENCED_BY_MOD | 127 |
| UNTOUCHED | 52 |

No same-ID technology definition was found under the mod common/technology path. REFERENCED_BY_MOD means an occurrence elsewhere in mod gameplay script.

## 17. AI-weight observations

- MILITARY_CONDITIONAL: 17
- OTHER: 13
- POLITICAL_CONDITIONAL: 8
- RESOURCE_CONDITIONAL: 14
- STATIC: 127

21 non-static AI logics require revalidation after RETIME/MERGE/SPLIT/REPLACE. No final numeric weights are proposed.

## 18. Great Wave deferred items

25 technologies have Ship Designer/ship-object references or an explicit naval role. All are DEFER_TO_TECH_1B=YES; TECH-1A records gates, not hull/component architecture.

- admiralty: naval role
- atmospheric_engine: ship_modifications
- battlefleet_tactics: naval role
- battleship_tech: ship_types
- breech_loading_artillery: ship_modifications
- carrier_tech: ship_types
- concrete_dockyards: naval role
- destroyer: ship_types
- dreadnought_tech: ship_types
- drydocks: ship_types
- floating_harbor: naval role
- gantry_cranes: naval role
- hydraulic_cranes: naval role
- ironclad_tech: ship_modifications, ship_types
- landing_craft: naval role
- monitor_tech: ship_types
- navigation: naval role
- paddle_steamer: naval role
- pre_dreadnought_tech: ship_modifications, ship_types
- screw_frigate: naval role
- sea_lane_strategies: ship_types
- self_propelled_torpedoes: ship_modifications, ship_types
- shell_gun: ship_modifications
- submarine: ship_types
- watertube_boiler: ship_modifications

## 19. Implementation-risk summary

- LOW: 59
- MEDIUM: 40
- HIGH: 52
- VERY_HIGH: 28

Icon/localization validation: missing names = 0, missing descriptions = 0, missing icons = 0, shared-icon definitions = 0.
The artillery technology name resolves through the shared goods localization key artillery, while its description remains in inventions_l_english.yml; this is recorded as SHARED_KEY_WITH_GOOD, not as missing localization.

## 20. Final decision table

| Tech | Relevance | V1 branch/node | Overlap | Action | Secondary | Risk | Confidence |
|---|---|---|---|---|---|---|---|
| admiralty | DIRECT_1700_1836 | Military V1 / state_dockyard_systems | VANILLA_BROADER | SPLIT | REWIRE;RETIME | VERY_HIGH | MEDIUM |
| army_reserves | DIRECT_1700_1836 | Military V1 / corps_organization | PARTIAL | RETIME | REWIRE | MEDIUM | MEDIUM |
| artillery | DIRECT_1700_1836 | Military V1 / standardized_field_artillery | STRONG | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| drydocks | DIRECT_1700_1836 | Military V1 / state_dockyard_systems | VANILLA_BROADER | SPLIT | REWIRE;RETIME | VERY_HIGH | MEDIUM |
| gunsmithing | DIRECT_1700_1836 | Military V1 / regulated_small_arms | V1_BROADER | REPLACE | REWIRE;RETIME | HIGH | MEDIUM |
| line_infantry | DIRECT_1700_1836 | Military V1 / regulated_small_arms | PARTIAL | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| mandatory_service | DIRECT_1700_1836 | Military V1 / corps_organization | PARTIAL | REWIRE | NONE | MEDIUM | MEDIUM |
| military_drill | DIRECT_1700_1836 | Military V1 / light_infantry_tactics | PARTIAL | REWIRE | NONE | MEDIUM | MEDIUM |
| napoleonic_warfare | DIRECT_1700_1836 | Military V1 / corps_organization | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| navigation | DIRECT_1700_1836 | Military V1 / marine_chronometry | VANILLA_BROADER | SPLIT | REWIRE;RETIME | VERY_HIGH | MEDIUM |
| paddle_steamer | DIRECT_1700_1836 | Military V1 / paddle_steam_navigation | EXACT | RETIME | REWIRE | VERY_HIGH | HIGH |
| standing_army | DIRECT_1700_1836 | Military V1 / corps_organization | V1_BROADER | REWIRE | NONE | MEDIUM | MEDIUM |
| field_works | DIRECT_1700_1836 | Military V1 / field_engineering_pontoon_trains | STRONG | REWIRE | NONE | MEDIUM | MEDIUM |
| general_staff | DIRECT_1700_1836 | Military V1 / professional_general_staff | EXACT | RETIME | REWIRE | HIGH | HIGH |
| hydraulic_cranes | DIRECT_1700_1836 | Military V1 / mechanized_naval_dockyards | STRONG | RETIME | REWIRE | VERY_HIGH | MEDIUM |
| logistics | DIRECT_1700_1836 | Military V1 / military_supply_services | EXACT | REPLACE | REWIRE;RETIME | HIGH | HIGH |
| percussion_cap | DIRECT_1700_1836 | Military V1 / percussion_ignition | EXACT | RETIME | REWIRE | MEDIUM | HIGH |
| power_of_the_purse | DIRECT_1700_1836 | Military V1 / state_dockyard_systems | PARTIAL | RENAME | REWIRE | MEDIUM | MEDIUM |
| rifling | DIRECT_1700_1836 | Military V1 / rifle_troops | PARTIAL | REWIRE | NONE | HIGH | MEDIUM |
| screw_frigate | CROSS_PERIOD | Military V1 / iron_hull_construction | SAME_UNLOCK_DIFFERENT_CONCEPT | KEEP | NONE | VERY_HIGH | MEDIUM |
| shell_gun | DIRECT_1700_1836 | Military V1 / naval_shell_guns | EXACT | RETIME | REWIRE | VERY_HIGH | HIGH |
| triage | DIRECT_1700_1836 | Military V1 / battlefield_evacuation | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| breech_loading_artillery | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| electric_telegraph | CROSS_PERIOD | Society V1 / optical_telegraph_networks | CROSS_BRANCH | KEEP | NONE | MEDIUM | MEDIUM |
| enlistment_offices | CROSS_PERIOD | NONE | NONE | KEEP | NONE | LOW | MEDIUM |
| floating_harbor | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| gantry_cranes | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| handcranked_machine_gun | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| ironclad_tech | POST_1836_ONLY | Military V1 / iron_hull_construction | STRONG | KEEP | NONE | VERY_HIGH | MEDIUM |
| jeune_ecole | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| military_statistics | CROSS_PERIOD | Society V1 / central_statistical_offices | CROSS_BRANCH | KEEP | NONE | HIGH | MEDIUM |
| modern_nursing | CROSS_PERIOD | Society V1 / clinical_medical_education | CROSS_BRANCH | KEEP | NONE | LOW | MEDIUM |
| monitor_tech | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| repeaters | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| self_propelled_torpedoes | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| automatic_machine_guns | POST_1836_ONLY | NONE | NONE | KEEP | NONE | HIGH | HIGH |
| bolt_action_rifles | POST_1836_ONLY | NONE | NONE | KEEP | NONE | HIGH | HIGH |
| concrete_dockyards | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| defense_in_depth | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| dreadnought_tech | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| landing_craft | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| military_aviation | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| pre_dreadnought_tech | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| sea_lane_strategies | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| submarine | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| trench_works | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| war_propaganda | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| wargaming | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| battlefleet_tactics | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| battleship_tech | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| carrier_tech | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| chemical_warfare | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| concrete_fortifications | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| destroyer | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |
| flamethrowers | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| mobile_armor | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| nco_training | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| stormtroopers | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| cotton_gin | DIRECT_1700_1836 | Production V1.1 / cotton_gin | EXACT | RETIME | REWIRE | MEDIUM | HIGH |
| distillation | DIRECT_1700_1836 | Production V1.1 / continuous_distillation | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| enclosure | DIRECT_1700_1836 | Production V1.1 / improved_husbandry | PARTIAL | REWIRE | NONE | HIGH | MEDIUM |
| lathe | DIRECT_1700_1836 | Production V1.1 / precision_machine_tools | STRONG | MERGE | REWIRE;RETIME | HIGH | MEDIUM |
| manufacturies | DIRECT_1700_1836 | Production V1.1 / interchangeable_manufacture | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| prospecting | DIRECT_1700_1836 | Production V1.1 / applied_mineralogy | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| sericulture | DIRECT_1700_1836 | NONE | NONE | KEEP | NONE | LOW | MEDIUM |
| shaft_mining | DIRECT_1700_1836 | Production V1.1 / shaft_mining | EXACT | RETIME | REWIRE | MEDIUM | HIGH |
| steelworking | DIRECT_1700_1836 | Production V1.1 / coke_smelting | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| atmospheric_engine | DIRECT_1700_1836 | Production V1.1 / atmospheric_steam_engines | EXACT | RETIME | REWIRE | VERY_HIGH | HIGH |
| baking_powder | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| bessemer_process | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| canneries | DIRECT_1700_1836 | Production V1.1 / hermetic_food_preservation | EXACT | RETIME | REWIRE | MEDIUM | HIGH |
| chemical_bleaching | DIRECT_1700_1836 | Production V1.1 / chlorine_bleaching | EXACT | RETIME | REWIRE | MEDIUM | HIGH |
| crystal_glass | DIRECT_1700_1836 | Production V1.1 / pressed_glass | PARTIAL | RETIME | REWIRE | MEDIUM | MEDIUM |
| fractional_distillation | CROSS_PERIOD | Production V1.1 / continuous_distillation | STRONG | KEEP | NONE | LOW | MEDIUM |
| intensive_agriculture | DIRECT_1700_1836 | Production V1.1 / advanced_crop_rotations | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| mechanical_tools | DIRECT_1700_1836 | Production V1.1 / precision_machine_tools | STRONG | MERGE | REWIRE;RETIME | HIGH | MEDIUM |
| mechanized_workshops | CROSS_PERIOD | Production V1.1 / interchangeable_manufacture | VANILLA_BROADER | SPLIT | REWIRE | HIGH | MEDIUM |
| nitroglycerin | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| railways | DIRECT_1700_1836 | Production V1.1 / railway_systems | EXACT | RETIME | REWIRE | HIGH | HIGH |
| watertube_boiler | CROSS_PERIOD | Production V1.1 / high_pressure_steam | PARTIAL | KEEP | NONE | VERY_HIGH | MEDIUM |
| aniline | POST_1836_ONLY | Production V1.1 / industrial_alkalis | PARTIAL | KEEP | NONE | LOW | MEDIUM |
| dynamite | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| electrical_generation | POST_1836_ONLY | NONE | NONE | KEEP | NONE | HIGH | HIGH |
| improved_fertilizer | CROSS_PERIOD | Production V1.1 / industrial_acids | PARTIAL | KEEP | NONE | LOW | MEDIUM |
| open_hearth_process | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| pumpjacks | POST_1836_ONLY | NONE | NONE | KEEP | NONE | HIGH | HIGH |
| reinforced_concrete | CROSS_PERIOD | Production V1.1 / hydraulic_cements | PARTIAL | KEEP | NONE | LOW | MEDIUM |
| rotary_valve_engine | CROSS_PERIOD | Production V1.1 / high_pressure_steam | V1_BROADER | KEEP | NONE | MEDIUM | MEDIUM |
| rubber_mastication | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| shift_work | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| steam_donkey | CROSS_PERIOD | Production V1.1 / deep_mine_engineering | SAME_UNLOCK_DIFFERENT_CONCEPT | KEEP | NONE | LOW | MEDIUM |
| steel_railway_cars | POST_1836_ONLY | Production V1.1 / railway_systems | PARTIAL | KEEP | NONE | MEDIUM | MEDIUM |
| threshing_machine | DIRECT_1700_1836 | Production V1.1 / mechanized_threshing | EXACT | RETIME | REWIRE | MEDIUM | HIGH |
| vacuum_canning | POST_1836_ONLY | Production V1.1 / hermetic_food_preservation | V1_BROADER | KEEP | NONE | LOW | MEDIUM |
| vulcanization | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| art_silk | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| automatic_bottle_blowers | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| combustion_engine | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| conveyors | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| electric_arc_process | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| electric_railway | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| electrical_capacitors | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| mechanized_farming | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| nitrogen_fixation | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| pasteurization | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| plastics | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| pneumatic_tools | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| radio | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| steam_turbine | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| telephone | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| arc_welding | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| compression_ignition | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| dough_rollers | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| flash_freezing | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| oil_turbine | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| academia | DIRECT_1700_1836 | Society V1 / institutionalized_scientific_exchange | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| banking | DIRECT_1700_1836 | Society V1 / institutionalized_public_credit | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| centralization | DIRECT_1700_1836 | Society V1 / systematic_population_registration | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| colonization | DIRECT_1700_1836 | Society V1 / systematic_cadastral_surveying | PARTIAL | REWIRE | NONE | HIGH | MEDIUM |
| currency_standards | DIRECT_1700_1836 | Society V1 / scientific_metrology | PARTIAL | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| democracy | DIRECT_1700_1836 | Society V1 / constitutional_government | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| empiricism | DIRECT_1700_1836 | Society V1 / institutionalized_scientific_exchange | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| international_relations | DIRECT_1700_1836 | Society V1 / institutionalized_scientific_exchange | NAME_COLLISION_ONLY | KEEP | NONE | HIGH | MEDIUM |
| international_trade | DIRECT_1700_1836 | Society V1 / commercial_insurance_markets | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| law_enforcement | DIRECT_1700_1836 | Society V1 / professional_civil_policing | STRONG | RETIME | REWIRE | MEDIUM | MEDIUM |
| mass_communication | DIRECT_1700_1836 | Society V1 / periodical_print_networks | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| medical_degrees | DIRECT_1700_1836 | Society V1 / clinical_medical_education | EXACT | REPLACE | REWIRE;RETIME | HIGH | HIGH |
| rationalism | DIRECT_1700_1836 | Society V1 / codified_practical_knowledge | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| romanticism | DIRECT_1700_1836 | NONE | NONE | KEEP | NONE | MEDIUM | MEDIUM |
| stock_exchange | DIRECT_1700_1836 | Society V1 / joint_stock_capital_markets | EXACT | MERGE | REWIRE;RETIME | HIGH | HIGH |
| tech_bureaucracy | DIRECT_1700_1836 | Society V1 / systematic_administrative_statistics | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| urban_planning | DIRECT_1700_1836 | Production V1.1 / professional_civil_engineering | CROSS_BRANCH | REWIRE | NONE | MEDIUM | MEDIUM |
| urbanization | DIRECT_1700_1836 | Production V1.1 / professional_civil_engineering | CROSS_BRANCH | RETIME | REWIRE | HIGH | MEDIUM |
| central_archives | DIRECT_1700_1836 | Society V1 / systematic_administrative_statistics | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| central_banking | DIRECT_1700_1836 | Society V1 / institutionalized_public_credit | STRONG | MERGE | REWIRE;RETIME | HIGH | MEDIUM |
| corporate_charters | DIRECT_1700_1836 | Society V1 / joint_stock_capital_markets | STRONG | MERGE | REWIRE;RETIME | HIGH | MEDIUM |
| dialectics | DIRECT_1700_1836 | Society V1 / early_socialism_cooperativism | PARTIAL | RETIME | REWIRE | MEDIUM | MEDIUM |
| egalitarianism | DIRECT_1700_1836 | Society V1 / universal_rights_discourse | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| joint_stock_companies | DIRECT_1700_1836 | Society V1 / joint_stock_capital_markets | EXACT | MERGE | REWIRE;RETIME | HIGH | HIGH |
| labor_movement | DIRECT_1700_1836 | Society V1 / organized_labor_movements | EXACT | RETIME | REWIRE | MEDIUM | HIGH |
| modern_sewerage | CROSS_PERIOD | Production V1.1 / professional_civil_engineering | CROSS_BRANCH | KEEP | NONE | LOW | MEDIUM |
| nationalism | DIRECT_1700_1836 | Society V1 / national_sovereignty | VANILLA_BROADER | SPLIT | REWIRE;RETIME | VERY_HIGH | MEDIUM |
| organized_sports | CROSS_PERIOD | NONE | NONE | KEEP | NONE | LOW | MEDIUM |
| pharmaceuticals | DIRECT_1700_1836 | Society V1 / active_principle_pharmacy | VANILLA_BROADER | SPLIT | REWIRE;RETIME | HIGH | MEDIUM |
| postal_savings | DIRECT_1700_1836 | Society V1 / popular_savings_institutions | EXACT | RETIME | REWIRE | MEDIUM | HIGH |
| psychiatry | DIRECT_1700_1836 | Society V1 / clinical_medical_education | PARTIAL | RETIME | REWIRE | MEDIUM | MEDIUM |
| quinine | DIRECT_1700_1836 | Society V1 / active_principle_pharmacy | STRONG | RETIME | REWIRE | MEDIUM | MEDIUM |
| realism | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| anarchism | CROSS_PERIOD | Society V1 / early_socialism_cooperativism | PARTIAL | KEEP | NONE | MEDIUM | MEDIUM |
| camera | POST_1836_ONLY | NONE | NONE | KEEP | NONE | HIGH | HIGH |
| civilizing_mission | POST_1836_ONLY | NONE | NONE | KEEP | NONE | HIGH | HIGH |
| corporatism | POST_1836_ONLY | NONE | NONE | KEEP | NONE | HIGH | HIGH |
| feminism | CROSS_PERIOD | Society V1 / universal_rights_discourse | PARTIAL | KEEP | NONE | MEDIUM | MEDIUM |
| human_rights | DIRECT_1700_1836 | Society V1 / universal_rights_discourse | EXACT | REPLACE | REWIRE;RETIME | HIGH | HIGH |
| identification_documents | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| investment_banks | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| mutual_funds | POST_1836_ONLY | Society V1 / popular_savings_institutions | PARTIAL | KEEP | NONE | LOW | MEDIUM |
| pan-nationalism | POST_1836_ONLY | Society V1 / national_sovereignty | PARTIAL | KEEP | NONE | VERY_HIGH | MEDIUM |
| philosophical_pragmatism | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| socialism | DIRECT_1700_1836 | Society V1 / early_socialism_cooperativism | STRONG | RETIME | REWIRE | HIGH | MEDIUM |
| steel_frame_buildings | POST_1836_ONLY | NONE | NONE | KEEP | NONE | HIGH | HIGH |
| central_planning | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| corporate_management | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| elevator | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| film | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| international_exchange_standards | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| malaria_prevention | POST_1836_ONLY | NONE | NONE | KEEP | NONE | HIGH | HIGH |
| multilateral_alliances | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| political_agitation | POST_1836_ONLY | NONE | NONE | KEEP | NONE | HIGH | HIGH |
| psychoanalysis | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| zeppelins | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| analytical_philosophy | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| antibiotics | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| behaviorism | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| macroeconomics | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| mass_propaganda | POST_1836_ONLY | NONE | NONE | KEEP | NONE | MEDIUM | HIGH |
| mass_surveillance | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| modern_financial_instruments | POST_1836_ONLY | NONE | NONE | KEEP | NONE | LOW | HIGH |
| paved_roads | POST_1836_ONLY | NONE | NONE | KEEP | NONE | VERY_HIGH | HIGH |

## 21. Open questions

- Human review must decide whether broad vanilla institutional nodes survive as umbrellas or split fully across V1.
- Same-unlock/different-concept cases need integrated-tree assignment without duplicated gates.
- Starting-tech differentiation is outside TECH-1A; sericulture and quinine are candidates only.
- Post-1836 nodes retain vanilla timing and roles; their 1836-1936 redesign is not attempted.
- Ship Designer architecture and DLC/free-patch boundaries remain reserved for TECH-1B.

### Consistency controls

- AUDITED_TECHS == VANILLA_TECH_TOTAL: 179 == 179
- TECH_AUDIT_ROWS: 179
- VANILLA_TECH_WITHOUT_ACTION: 0
- VANILLA_TECH_WITHOUT_REFERENCE_AUDIT: 0
- Reference-index rows: 3476
- Unlock-index rows: 1236
- GAMEPLAY_FILES_CHANGED: 0
- COMMITS_CREATED: 0
- PUSH_PERFORMED: NO

All recommendations are research outputs only and remain non-canonical pending human review.
