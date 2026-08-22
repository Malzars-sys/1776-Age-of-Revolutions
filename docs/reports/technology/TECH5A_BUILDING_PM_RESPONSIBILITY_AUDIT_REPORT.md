# TECH5A ? Building & Production Method Technology Responsibility Audit

## 1. Baseline

- `BRANCH = tech4c2-audit-snapshot`
- `HEAD = 732363f458bf36361cdd38812e6c63dab5e0818c`
- Initial working tree: clean.
- Audit/research only; no gameplay implementation.

## 2. Vanilla path and version

- `VANILLA_GAME_PATH = C:\Games\Victoria 3\game`
- `VANILLA_GAME_VERSION = 1.13.9` (file version of `C:\Games\Victoria 3\binaries\victoria3.exe`)
- `PREVIOUS_AUDIT_BASELINE = 1.13.11`
- `CURRENT_INSTALLED_VANILLA = 1.13.9`
- `VANILLA_VERSION_MISMATCH = YES`

The user-designated installation is authoritative. The mismatch is recorded and did not stop the audit.

## 3. Files audited

Recursive effective-state inspection covered vanilla and mod `common/buildings/`, `common/production_methods/`, and `common/production_method_groups/`. Effective technology definitions supplied category, era, and dependency data. Technology-bearing scripted triggers were followed only when invoked by a scoped object; no such invocation was found.

| Scope | Vanilla files / objects | Mod files / objects | Effective objects |
| --- | ---: | ---: | ---: |
| Buildings | 14 / 115 | 1 / 2 | 117 |
| Production methods | 15 / 433 | 1 / 2 | 435 |
| Production method groups | 15 / 197 | 1 / 2 | 199 |

Canonical inputs were the final TECH3A/TECH4C4 state, TECH4C2 residual audits, and exact `ASSIGNED` mappings from TECH2H.

## 4. Methodology

Mod top-level IDs override vanilla IDs; otherwise vanilla objects are inherited. Gates were extracted from `unlocking_technologies`, direct `has_technology` / `has_technology_researched`, and context-reachable scripted triggers. PM relations are expanded per effective PMG membership. PMG order comes from each effective `production_methods` list. A later PM is dependent only if every earlier PM gate is identical to, or a transitive ancestor of, a later PM gate in the effective technology graph. Probable mappings were never promoted to frozen decisions.

## 5. Global counters

- `BUILDING_TECH_GATES_TOTAL = 66`
- `PRODUCTION_METHOD_TECH_GATES_TOTAL = 242`
- `PRODUCTION_METHOD_GROUPS_AUDITED = 70`
- `PM_PROGRESSION_RELATIONSHIPS_AUDITED = 197`
- `PM_PROGRESSION_SKIP_RISKS = 46` (`YES = 25`, `POSSIBLE = 21`)
- `REFERENCES_TO_VISIBLE_I_VI_TECHS = 58`
- `REFERENCES_TO_POST1836_TECHS = 186`
- `REFERENCES_TO_HIDDEN_ALIASES = 64`
- `REFERENCES_TO_REGIONAL_EVENT_TECHS = 0`
- `UNKNOWN_TECH_REFERENCES = 0`
- `BROKEN_TECH_REFERENCES = 0`
- `FROZEN_TARGET_AVAILABLE = 37`
- `DESIGN_REVIEW_REQUIRED = 27`
- `READY_MECHANICAL_TRANSFERS = 37`
- `VANILLA_MOD_IDENTICAL = 0`
- `VANILLA_MOD_CHANGED = 0`
- `MOD_ONLY_GATES = 0`
- `VANILLA_ONLY_GATES = 0`
- `INHERITED_VANILLA_GATES = 308`

All 308 gate relations classify exactly once.

## 6. Hidden-alias responsibilities

There are 64 effective hidden-alias building/PM-group relations:

| Alias | References |
| --- | --- |
| academia | 1 |
| admiralty | 1 |
| artillery | 1 |
| central_archives | 1 |
| centralization | 1 |
| dialectics | 1 |
| enclosure | 16 |
| gunsmithing | 2 |
| hydraulic_cranes | 1 |
| intensive_agriculture | 8 |
| lathe | 3 |
| manufacturies | 6 |
| mechanized_workshops | 5 |
| navigation | 3 |
| power_of_the_purse | 1 |
| prospecting | 2 |
| screw_frigate | 2 |
| standing_army | 1 |
| steelworking | 3 |
| tech_bureaucracy | 1 |
| urban_planning | 2 |
| urbanization | 2 |

`corporate_charters` and `pharmaceuticals` have no scoped building/PM responsibility; their known responsibilities are outside TECH5A.

## 7. Frozen mappings already available

These 37 expanded relations have an exact object-specific TECH2H destination:

| Alias | Type | Object | PMG | Buildings | Frozen target |
| --- | --- | --- | --- | --- | --- |
| academia | BUILDING | building_university | NOT_APPLICABLE | building_university | institutionalized_scientific_exchange |
| admiralty | BUILDING | building_naval_administration | NOT_APPLICABLE | building_naval_administration | state_dockyard_systems |
| artillery | PRODUCTION_METHOD | pm_cannons | pmg_foundries | building_artillery_foundry | standardized_field_artillery |
| central_archives | PRODUCTION_METHOD | pm_vertical_filing_cabinets | pmg_base_building_government_administration | building_government_administration | central_statistical_offices |
| centralization | PRODUCTION_METHOD | pm_horizontal_drawer_cabinets | pmg_base_building_government_administration | building_government_administration | systematic_population_registration |
| gunsmithing | BUILDING | building_arms_industry | NOT_APPLICABLE | building_arms_industry | regulated_small_arms |
| gunsmithing | BUILDING | building_artillery_foundry | NOT_APPLICABLE | building_artillery_foundry | regulated_small_arms |
| intensive_agriculture | BUILDING | building_chemical_plant | NOT_APPLICABLE | building_chemical_plant | industrial_acids |
| intensive_agriculture | BUILDING | building_explosives_factory | NOT_APPLICABLE | building_explosives_factory | industrial_acids |
| intensive_agriculture | PRODUCTION_METHOD | pm_sheep_farms | pmg_sheep_ranch | building_livestock_ranch | selective_breeding |
| intensive_agriculture | PRODUCTION_METHOD | pm_soil_enriching_farming | pmg_base_building_maize_farm | building_maize_farm | advanced_crop_rotations |
| intensive_agriculture | PRODUCTION_METHOD | pm_soil_enriching_farming | pmg_base_building_millet_farm | building_millet_farm | advanced_crop_rotations |
| intensive_agriculture | PRODUCTION_METHOD | pm_soil_enriching_farming | pmg_base_building_rye_farm | building_rye_farm | advanced_crop_rotations |
| intensive_agriculture | PRODUCTION_METHOD | pm_soil_enriching_farming | pmg_base_building_wheat_farm | building_wheat_farm | advanced_crop_rotations |
| intensive_agriculture | PRODUCTION_METHOD | pm_soil_enriching_farming_building_rice_farm | pmg_base_building_rice_farm | building_rice_farm | advanced_crop_rotations |
| manufacturies | BUILDING | building_food_industry | NOT_APPLICABLE | building_food_industry | interchangeable_manufacture |
| manufacturies | BUILDING | building_furniture_manufactory | NOT_APPLICABLE | building_furniture_manufactory | interchangeable_manufacture |
| manufacturies | BUILDING | building_glassworks | NOT_APPLICABLE | building_glassworks | pressed_glass |
| manufacturies | BUILDING | building_paper_mill | NOT_APPLICABLE | building_paper_mill | continuous_papermaking |
| manufacturies | BUILDING | building_textile_mill | NOT_APPLICABLE | building_textile_mill | mechanized_weaving |
| manufacturies | BUILDING | building_tooling_workshop | NOT_APPLICABLE | building_tooling_workshop | mechanical_tools |
| mechanized_workshops | PRODUCTION_METHOD | coffee_plantation_mechanical_drying | pmg_drying_coffee_plantation | building_coffee_plantation | interchangeable_manufacture |
| mechanized_workshops | PRODUCTION_METHOD | coffee_plantation_wet_process_mechanical | pmg_base_building_coffee_plantation | building_coffee_plantation | interchangeable_manufacture |
| mechanized_workshops | PRODUCTION_METHOD | pm_mechanized_looms | pmg_automation_building_textile_mill | building_textile_mill | mechanized_weaving |
| mechanized_workshops | PRODUCTION_METHOD | pm_mechanized_workshops | pmg_base_building_furniture_manufactory | building_furniture_manufactory | interchangeable_manufacture |
| mechanized_workshops | PRODUCTION_METHOD | pm_sewing_machines | pmg_base_building_textile_mill | building_textile_mill | mechanized_weaving |
| navigation | BUILDING | building_port | NOT_APPLICABLE | building_port | marine_chronometry |
| navigation | BUILDING | building_shipyard | NOT_APPLICABLE | building_shipyard | marine_chronometry |
| navigation | BUILDING | building_whaling_station | NOT_APPLICABLE | building_whaling_station | marine_chronometry |
| power_of_the_purse | PRODUCTION_METHOD | pm_power_of_the_purse | pmg_naval_theory | NONE_RESOLVED | state_dockyard_systems |
| prospecting | BUILDING | building_gold_field | NOT_APPLICABLE | building_gold_field | applied_mineralogy |
| prospecting | BUILDING | building_gold_mine | NOT_APPLICABLE | building_gold_mine | applied_mineralogy |
| standing_army | BUILDING | building_barrack | NOT_APPLICABLE | building_barrack | corps_organization |
| steelworking | BUILDING | building_steel_mill | NOT_APPLICABLE | building_steel_mill | puddling_and_rolling |
| steelworking | PRODUCTION_METHOD | pm_pig_iron | pmg_base_building_tooling_workshop | building_tooling_workshop | coke_smelting |
| steelworking | PRODUCTION_METHOD | pm_saw_mills | pmg_base_building_logging_camp | building_logging_camp | mechanical_tools |
| tech_bureaucracy | BUILDING | building_government_administration | NOT_APPLICABLE | building_government_administration | systematic_administrative_statistics |

Every populated target cites `docs/reports/technology/TECH2H_VANILLA_SPLIT_UNLOCK_MATRIX.csv` in the matrix.

## 8. Ambiguous mappings

These 27 expanded relations remain undecided:

| Alias | Type | Object | PMG | Buildings |
| --- | --- | --- | --- | --- |
| dialectics | PRODUCTION_METHOD | pm_philosophy_department | pmg_base_building_university | building_university |
| enclosure | BUILDING | building_banana_plantation | NOT_APPLICABLE | building_banana_plantation |
| enclosure | BUILDING | building_coffee_plantation | NOT_APPLICABLE | building_coffee_plantation |
| enclosure | BUILDING | building_cotton_plantation | NOT_APPLICABLE | building_cotton_plantation |
| enclosure | BUILDING | building_dye_plantation | NOT_APPLICABLE | building_dye_plantation |
| enclosure | BUILDING | building_livestock_ranch | NOT_APPLICABLE | building_livestock_ranch |
| enclosure | BUILDING | building_maize_farm | NOT_APPLICABLE | building_maize_farm |
| enclosure | BUILDING | building_millet_farm | NOT_APPLICABLE | building_millet_farm |
| enclosure | BUILDING | building_opium_plantation | NOT_APPLICABLE | building_opium_plantation |
| enclosure | BUILDING | building_rice_farm | NOT_APPLICABLE | building_rice_farm |
| enclosure | BUILDING | building_rye_farm | NOT_APPLICABLE | building_rye_farm |
| enclosure | BUILDING | building_silk_plantation | NOT_APPLICABLE | building_silk_plantation |
| enclosure | BUILDING | building_sugar_plantation | NOT_APPLICABLE | building_sugar_plantation |
| enclosure | BUILDING | building_tea_plantation | NOT_APPLICABLE | building_tea_plantation |
| enclosure | BUILDING | building_tobacco_plantation | NOT_APPLICABLE | building_tobacco_plantation |
| enclosure | BUILDING | building_vineyard | NOT_APPLICABLE | building_vineyard |
| enclosure | BUILDING | building_wheat_farm | NOT_APPLICABLE | building_wheat_farm |
| hydraulic_cranes | PRODUCTION_METHOD | pm_trade_center_trade_quantity_high | pmg_trade_quantity_trade_center | building_trade_center |
| lathe | PRODUCTION_METHOD | pm_dye_workshops | pmg_base_building_textile_mill | building_textile_mill |
| lathe | PRODUCTION_METHOD | pm_lathe | pmg_base_building_furniture_manufactory | building_furniture_manufactory |
| lathe | PRODUCTION_METHOD | pm_leaded_glass | pmg_base_building_glassworks | building_glassworks |
| screw_frigate | PRODUCTION_METHOD | pm_complex_shipbuilding | pmg_base_building_shipyard | building_shipyard |
| screw_frigate | PRODUCTION_METHOD | pm_military_shipbuilding_wooden_2 | pmg_military_base | NONE_RESOLVED |
| urban_planning | PRODUCTION_METHOD | pm_iron_frame_buildings | pmg_base_building_construction_sector | building_construction_sector |
| urban_planning | PRODUCTION_METHOD | pm_market_squares | pmg_amenities | building_urban_center |
| urbanization | BUILDING | building_construction_sector | NOT_APPLICABLE | building_construction_sector |
| urbanization | BUILDING | building_urban_center | NOT_APPLICABLE | building_urban_center |

No target was inferred. In unique-object terms: 16 `enclosure` buildings; three `lathe` PMs; two `urbanization` buildings; two `screw_frigate` PMs; and one PM each for `urban_planning`, `dialectics`, and `hydraulic_cranes`.

## 9. PM progression

70 PMGs contain at least two gated PMs; their full order yields 197 adjacent relations.

- `PM_PROGRESSION_OK = 140`
- `PM_PROGRESSION_INTENTIONAL_PARALLEL = 11`
- `PM_PROGRESSION_SKIP_RISK = 25`
- `DESIGN_REVIEW_REQUIRED = 21` (progression only)

## 10. PM skip risks

There are 25 definite graph-level risks and 21 possible/ambiguous risks. No prerequisite was added.

| PMG | Previous PM | Previous tech | Next PM | Next tech | Risk | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| pmg_amenities | pm_market_squares | urban_planning | pm_covered_markets | steel_frame_buildings | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_automation_building_textile_mill | pm_mechanized_looms | mechanized_workshops | pm_automatic_power_looms | electrical_capacitors | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_art_academy | pm_realist_art | realism | pm_photographic_art | camera | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_construction_sector | pm_iron_frame_buildings | urban_planning | pm_steel_frame_buildings | steel_frame_buildings | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_construction_sector | pm_steel_frame_buildings | steel_frame_buildings | pm_arc_welded_buildings | arc_welding | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_food_industry | pm_sweeteners | distillation | pm_baking_powder | baking_powder | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_furniture_manufactory | pm_lathe | lathe | pm_mechanized_workshops | mechanized_workshops | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_glassworks | pm_leaded_glass | lathe | pm_crystal_glass | crystal_glass | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_glassworks | pm_crystal_glass | crystal_glass | pm_houseware_plastics | plastics | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_government_administration | pm_vertical_filing_cabinets | central_archives | pm_switch_boards | central_planning | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_livestock_ranch | pm_slaughterhouses | mechanical_tools | pm_mechanized_slaughtering | mechanized_farming | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_logging_camp | pm_saw_mills | steelworking | pm_electric_saw_mills | electrical_generation | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_maize_farm | pm_soil_enriching_farming | intensive_agriculture | pm_fertilization | improved_fertilizer | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_millet_farm | pm_soil_enriching_farming | intensive_agriculture | pm_fertilization | improved_fertilizer | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_motor_industry | pm_electric_engines | electric_railway | pm_diesel_engines | compression_ignition | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_naval_fortification | pm_naval_fortification_reinforced | breech_loading_artillery | pm_naval_fortification_advanced | concrete_fortifications | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_paper_mill | pm_sulfite_pulping | mechanical_tools | pm_bleached_paper | chemical_bleaching | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_railway | pm_electric_trains_principle_transport_3 | electric_railway | pm_diesel_trains | compression_ignition | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_rice_farm | pm_soil_enriching_farming_building_rice_farm | intensive_agriculture | pm_fertilization_building_rice_farm | improved_fertilizer | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_rye_farm | pm_soil_enriching_farming | intensive_agriculture | pm_fertilization | improved_fertilizer | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_shipyard | pm_complex_shipbuilding | screw_frigate | pm_metal_shipbuilding | gantry_cranes | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_shipyard | pm_metal_shipbuilding | gantry_cranes | pm_arc_welding_shipbuilding | arc_welding | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_textile_mill | pm_dye_workshops | lathe | pm_sewing_machines | mechanized_workshops | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_textile_mill | pm_sewing_machines | mechanized_workshops | pm_electric_sewing_machines | electrical_capacitors | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_tooling_workshop | pm_pig_iron | steelworking | pm_steel | mechanical_tools | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_tooling_workshop | pm_steel | mechanical_tools | pm_rubber_grips | vulcanization | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_base_building_university | pm_philosophy_department | dialectics | pm_analytical_philosophy_department | analytical_philosophy | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_base_building_wheat_farm | pm_soil_enriching_farming | intensive_agriculture | pm_fertilization | improved_fertilizer | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_canning | pm_cannery_fish | canneries | pm_vacuum_canning | vacuum_canning | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_equipment | pm_steam_donkey_building_logging_camp | steam_donkey | pm_chainsaws | combustion_engine | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_explosives_building_chemical_plant | pm_vacuum_evaporation | dynamite | pm_brine_electrolysis | electrical_capacitors | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_fencing | pm_barbed_wire_fences | field_works | pm_electric_fencing | electrical_generation | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_foundries | pm_cannons | artillery | pm_smoothbores | shell_gun | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_foundries | pm_breech_loaders | breech_loading_artillery | pm_recoiled_barrels | automatic_machine_guns | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_military_base | pm_military_shipbuilding_wooden_2 | screw_frigate | pm_military_shipbuilding_steam | ironclad_tech | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_military_base | pm_military_shipbuilding_steam | ironclad_tech | pm_military_shipbuilding_steam_2 | arc_welding | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_public_transport | pm_public_trams | railways | pm_public_motor_carriages | combustion_engine | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_refinement_building_sugar_plantation | vacuum_pan_sugar | watertube_boiler | steam_powered_evaporation_sugar | fractional_distillation | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_refinement_building_sugar_plantation | steam_powered_evaporation_sugar | fractional_distillation | centrifugal_machine_sugar | rotary_valve_engine | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_refrigeration_building_fishing_wharf | pm_refrigerated_storage_building_fishing_wharf | pasteurization | pm_refrigerated_rail_cars_building_fishing_wharf | electric_railway | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_refrigeration_building_fishing_wharf | pm_refrigerated_rail_cars_building_fishing_wharf | electric_railway | pm_flash_freezing_building_fishing_wharf | flash_freezing | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_refrigeration_building_livestock_ranch | pm_refrigerated_storage_building_livestock_ranch | pasteurization | pm_refrigerated_rail_cars_building_livestock_ranch | electric_railway | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_refrigeration_building_whaling_station | pm_refrigerated_storage_building_whaling_station | pasteurization | pm_refrigerated_rail_cars_building_whaling_station | electric_railway | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_refrigeration_building_whaling_station | pm_refrigerated_rail_cars_building_whaling_station | electric_railway | pm_flash_freezing_building_whaling_station | flash_freezing | YES | PM_PROGRESSION_SKIP_RISK |
| pmg_sheep_ranch | pm_sheep_farms | intensive_agriculture | pm_intensive_grazing_ranch | mechanized_farming | POSSIBLE | DESIGN_REVIEW_REQUIRED |
| pmg_trade_quantity_trade_center | pm_trade_center_trade_quantity_high | hydraulic_cranes | pm_trade_center_trade_quantity_very_high | floating_harbor | POSSIBLE | DESIGN_REVIEW_REQUIRED |

The corrected `industrial_ceramics` + `industrial_acids` ? `chemical_bleaching` case is evaluated by the same transitive-ancestor method and is not a false positive.

## 11. Vanilla/mod differences

All 308 scoped relations are inherited from vanilla. The mod's two monument buildings, two PMs, and two PMGs introduce no technology gates and override no scoped vanilla IDs. Explicit identical overrides, changed overrides, mod-only gates, and standalone vanilla-only rows are therefore zero; inherited vanilla is recorded separately. The Sagrada Familia stage-3 `has_technology_researched = pneumatic_tools` availability check is included explicitly.

## 12. Exact mechanically transferable set

Section 7 and the alias matrix filtered to `READY_MECHANICAL_TRANSFER` are authoritative: 37 expanded relations, 34 unique alias/object assignments.

## 13. Exact design-review set

Section 8 and the matrix filtered to `DESIGN_REVIEW_REQUIRED` are authoritative: 27 expanded relations, 27 unique alias/object responsibilities. The 21 possible progression rows in Section 10 also require review before redesign.

## 14. Scope guard and coverage

- Every encountered technology has a final classification: PASS.
- Every hidden-alias reference is in the matrix: PASS (64/64).
- Every gated PM is in the PM audit: PASS (206 unique PMs; 242 expanded relations).
- Every PMG with at least two gated PMs is in progression: PASS (70).
- Every frozen target cites its exact source: PASS.
- Ambiguous mappings remain `DESIGN_REVIEW_REQUIRED`: PASS.
- Relevant technology-bearing scripted-trigger invocations: 0.
- Gameplay files modified by TECH5A: 0.
- Deliverables: four CSV and this Markdown report only.

## 15. Conclusion

`TECH5A_BUILDING_PM_AUDIT = COMPLETE`

The audit completely maps the effective installed vanilla 1.13.9 plus baseline mod state, separates frozen mechanical transfers from design decisions, and records progression risks without changing gameplay.
