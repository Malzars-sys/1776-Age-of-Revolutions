# TECH5B1 ? Frozen Building & Production Method Responsibility Transfers

## 1. Baseline

- `BRANCH = tech4c2-audit-snapshot`
- `HEAD = e26279bf32c3dae3359c32d68de9343f11a4883e`
- Initial working tree: clean.
- Implementation source: `TECH5A_HIDDEN_ALIAS_BUILDING_PM_RESPONSIBILITY_MATRIX.csv`, filtered strictly to `READY_MECHANICAL_TRANSFER`.
- Canonical selection validation: 37 expanded rows and 34 unique `object_type + object_id` pairs.

## 2. Vanilla source and version

- `VANILLA_GAME_PATH = C:\Games\Victoria 3\game`
- `VANILLA_EXECUTABLE = C:\Games\Victoria 3\binaries\victoria3.exe`
- `VANILLA_VERSION = 1.13.9` (file version and product version).
- `VANILLA_BASELINE_MISMATCH = NO`
- Vanilla files were read only.

## 3. Override strategy

The mod descriptor replaces only `common/technology/eras` and `common/technology/technologies`; it does not replace `common/buildings` or `common/production_methods`. Late-loading `99_...` files therefore provide targeted top-level ID overrides in the current architecture.

Each overridden object is the complete Vanilla 1.13.9 definition. Object normalization replaces only the authorized `unlocking_technologies` value with a sentinel before comparison; all remaining text is identical.

## 4. Gameplay files created

- `common/buildings/99_tech5b1_frozen_technology_gate_overrides.txt`
- `common/production_methods/99_tech5b1_frozen_technology_gate_overrides.txt`

## 5. Building transfers (20)

| Object | Old technology | New technology |
| --- | --- | --- |
| `building_university` | `academia` | `institutionalized_scientific_exchange` |
| `building_government_administration` | `tech_bureaucracy` | `systematic_administrative_statistics` |
| `building_naval_administration` | `admiralty` | `state_dockyard_systems` |
| `building_barrack` | `standing_army` | `corps_organization` |
| `building_arms_industry` | `gunsmithing` | `regulated_small_arms` |
| `building_artillery_foundry` | `gunsmithing` | `regulated_small_arms` |
| `building_chemical_plant` | `intensive_agriculture` | `industrial_acids` |
| `building_explosives_factory` | `intensive_agriculture` | `industrial_acids` |
| `building_food_industry` | `manufacturies` | `interchangeable_manufacture` |
| `building_furniture_manufactory` | `manufacturies` | `interchangeable_manufacture` |
| `building_glassworks` | `manufacturies` | `pressed_glass` |
| `building_paper_mill` | `manufacturies` | `continuous_papermaking` |
| `building_textile_mill` | `manufacturies` | `mechanized_weaving` |
| `building_tooling_workshop` | `manufacturies` | `mechanical_tools` |
| `building_shipyard` | `navigation` | `marine_chronometry` |
| `building_port` | `navigation` | `marine_chronometry` |
| `building_whaling_station` | `navigation` | `marine_chronometry` |
| `building_gold_field` | `prospecting` | `applied_mineralogy` |
| `building_gold_mine` | `prospecting` | `applied_mineralogy` |
| `building_steel_mill` | `steelworking` | `puddling_and_rolling` |

## 6. Production-method transfers (14)

| Object | Old technology | New technology |
| --- | --- | --- |
| `pm_cannons` | `artillery` | `standardized_field_artillery` |
| `pm_vertical_filing_cabinets` | `central_archives` | `central_statistical_offices` |
| `pm_horizontal_drawer_cabinets` | `centralization` | `systematic_population_registration` |
| `pm_sheep_farms` | `intensive_agriculture` | `selective_breeding` |
| `pm_soil_enriching_farming` | `intensive_agriculture` | `advanced_crop_rotations` |
| `pm_soil_enriching_farming_building_rice_farm` | `intensive_agriculture` | `advanced_crop_rotations` |
| `coffee_plantation_mechanical_drying` | `mechanized_workshops` | `interchangeable_manufacture` |
| `coffee_plantation_wet_process_mechanical` | `mechanized_workshops` | `interchangeable_manufacture` |
| `pm_mechanized_looms` | `mechanized_workshops` | `mechanized_weaving` |
| `pm_mechanized_workshops` | `mechanized_workshops` | `interchangeable_manufacture` |
| `pm_sewing_machines` | `mechanized_workshops` | `mechanized_weaving` |
| `pm_power_of_the_purse` | `power_of_the_purse` | `state_dockyard_systems` |
| `pm_pig_iron` | `steelworking` | `coke_smelting` |
| `pm_saw_mills` | `steelworking` | `mechanical_tools` |

`pm_soil_enriching_farming` is defined once and remains shared by four PMGs.

## 7. Expanded relations

- `PHYSICAL_OBJECT_GATE_CHANGES = 34`
- `EXPANDED_RELATIONS_TRANSFERRED = 37`
- `READY_MECHANICAL_TRANSFER_RELATIONS_IMPLEMENTED = 37`
- The three-row difference is the single shared `pm_soil_enriching_farming` definition expanding to four PMGs.

## 8. Object parity and technology validation

- `NON_TECH_GATE_FIELD_DIFFERENCES = 0`
- All 34 override blocks match their Vanilla source block outside the one frozen technology gate value.
- Automatic target count: `DISTINCT_TARGET_TECHNOLOGIES = 20` (the request's textual count of 17 is superseded by its explicit automatic-counter rule).
- All 20 target technology IDs exist in the effective mod technology definitions.
- `UNKNOWN_TECH_REFERENCES = 0`
- `BROKEN_TECH_REFERENCES = 0`

## 9. Hidden aliases before and after

- `SCOPED_GATE_RELATIONS_TOTAL = 308`
- `HIDDEN_ALIAS_RELATIONS_BEFORE = 64`
- `HIDDEN_ALIAS_RELATIONS_REMOVED = 37`
- `HIDDEN_ALIAS_RELATIONS_AFTER = 27`
- `DESIGN_REVIEW_RELATIONS_PRESERVED = 27`

Remaining alias counts:

- `dialectics = 1`
- `enclosure = 16`
- `hydraulic_cranes = 1`
- `lathe = 3`
- `screw_frigate = 2`
- `urban_planning = 2`
- `urbanization = 2`

The following formerly scoped transferable aliases are all zero after override evaluation:

- `academia = 0`
- `admiralty = 0`
- `artillery = 0`
- `central_archives = 0`
- `centralization = 0`
- `gunsmithing = 0`
- `intensive_agriculture = 0`
- `manufacturies = 0`
- `mechanized_workshops = 0`
- `navigation = 0`
- `power_of_the_purse = 0`
- `prospecting = 0`
- `standing_army = 0`
- `steelworking = 0`
- `tech_bureaucracy = 0`

## 10. Exact remaining 27 responsibilities

| Alias | Type | Object | PMG | Building | Current requirement |
| --- | --- | --- | --- | --- | --- |
| `dialectics` | PRODUCTION_METHOD | `pm_philosophy_department` | `pmg_base_building_university` | `building_university` | `unlocking_technologies = { dialectics }` |
| `enclosure` | BUILDING | `building_banana_plantation` | `NOT_APPLICABLE` | `building_banana_plantation` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_coffee_plantation` | `NOT_APPLICABLE` | `building_coffee_plantation` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_cotton_plantation` | `NOT_APPLICABLE` | `building_cotton_plantation` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_dye_plantation` | `NOT_APPLICABLE` | `building_dye_plantation` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_livestock_ranch` | `NOT_APPLICABLE` | `building_livestock_ranch` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_maize_farm` | `NOT_APPLICABLE` | `building_maize_farm` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_millet_farm` | `NOT_APPLICABLE` | `building_millet_farm` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_opium_plantation` | `NOT_APPLICABLE` | `building_opium_plantation` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_rice_farm` | `NOT_APPLICABLE` | `building_rice_farm` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_rye_farm` | `NOT_APPLICABLE` | `building_rye_farm` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_silk_plantation` | `NOT_APPLICABLE` | `building_silk_plantation` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_sugar_plantation` | `NOT_APPLICABLE` | `building_sugar_plantation` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_tea_plantation` | `NOT_APPLICABLE` | `building_tea_plantation` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_tobacco_plantation` | `NOT_APPLICABLE` | `building_tobacco_plantation` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_vineyard` | `NOT_APPLICABLE` | `building_vineyard` | `unlocking_technologies = { enclosure }` |
| `enclosure` | BUILDING | `building_wheat_farm` | `NOT_APPLICABLE` | `building_wheat_farm` | `unlocking_technologies = { enclosure }` |
| `hydraulic_cranes` | PRODUCTION_METHOD | `pm_trade_center_trade_quantity_high` | `pmg_trade_quantity_trade_center` | `building_trade_center` | `unlocking_technologies = { hydraulic_cranes }` |
| `lathe` | PRODUCTION_METHOD | `pm_dye_workshops` | `pmg_base_building_textile_mill` | `building_textile_mill` | `unlocking_technologies = { lathe }` |
| `lathe` | PRODUCTION_METHOD | `pm_lathe` | `pmg_base_building_furniture_manufactory` | `building_furniture_manufactory` | `unlocking_technologies = { lathe }` |
| `lathe` | PRODUCTION_METHOD | `pm_leaded_glass` | `pmg_base_building_glassworks` | `building_glassworks` | `unlocking_technologies = { lathe }` |
| `screw_frigate` | PRODUCTION_METHOD | `pm_complex_shipbuilding` | `pmg_base_building_shipyard` | `building_shipyard` | `unlocking_technologies = { screw_frigate }` |
| `screw_frigate` | PRODUCTION_METHOD | `pm_military_shipbuilding_wooden_2` | `pmg_military_base` | `NONE_RESOLVED` | `unlocking_technologies = { screw_frigate }` |
| `urban_planning` | PRODUCTION_METHOD | `pm_iron_frame_buildings` | `pmg_base_building_construction_sector` | `building_construction_sector` | `unlocking_technologies = { urban_planning }` |
| `urban_planning` | PRODUCTION_METHOD | `pm_market_squares` | `pmg_amenities` | `building_urban_center` | `unlocking_technologies = { urban_planning }` |
| `urbanization` | BUILDING | `building_construction_sector` | `NOT_APPLICABLE` | `building_construction_sector` | `unlocking_technologies = { urbanization }` |
| `urbanization` | BUILDING | `building_urban_center` | `NOT_APPLICABLE` | `building_urban_center` | `unlocking_technologies = { urbanization }` |

Every row above remains `DESIGN_REVIEW_REQUIRED` and is unchanged.

## 11. Post-transfer PM progression

The 197 TECH5A relations were recalculated against the effective technology graph after substituting only the 14 frozen PM gates.

- `PM_PROGRESSION_RELATIONSHIPS_AUDITED = 197`
- `PM_PROGRESSION_RISKS_BEFORE = 46` (25 confirmed, 21 design review).
- `PM_PROGRESSION_RISKS_AFTER = 42` (33 confirmed, 9 design review).
- `PM_PROGRESSION_RESOLVED_BY_TRANSFER = 4`
- `UNCHANGED_RISK = 25`
- `UNCHANGED_DESIGN_REVIEW = 9`
- `CLASSIFICATION_CHANGED_OTHER = 8` (previous hidden-alias design reviews now measurable as confirmed skip risks).
- Post-transfer totals: 144 OK, 33 `PM_PROGRESSION_SKIP_RISK`, 9 `DESIGN_REVIEW_REQUIRED`, and 11 intentional parallel/ownership relations.

No PM progression relationship was edited or reordered.

## 12. Scope guard

- `BUILDING_OBJECTS_OVERRIDDEN = 20`
- `PRODUCTION_METHOD_OBJECTS_OVERRIDDEN = 14`
- `PHYSICAL_OBJECT_GATE_CHANGES = 34`
- `EXPANDED_RELATIONS_TRANSFERRED = 37`
- `SCOPED_GATE_RELATIONS_TOTAL = 308`
- `HIDDEN_ALIAS_RELATIONS_BEFORE = 64`
- `HIDDEN_ALIAS_RELATIONS_REMOVED = 37`
- `HIDDEN_ALIAS_RELATIONS_AFTER = 27`
- `DESIGN_REVIEW_RELATIONS_PRESERVED = 27`
- `UNKNOWN_TECH_REFERENCES = 0`
- `BROKEN_TECH_REFERENCES = 0`
- `NON_TECH_GATE_FIELD_DIFFERENCES = 0`
- `TECHNOLOGY_DEFINITIONS_CHANGED = 0`
- `TECHNOLOGY_PREREQUISITES_CHANGED = 0`
- `TECHNOLOGY_ERAS_CHANGED = 0`
- `PRODUCTION_METHOD_GROUPS_CHANGED = 0`
- `PM_ORDER_CHANGED = 0`
- `STARTING_TECH_CHANGES = 0`
- TECH5A snapshot files changed: 0.
- Gameplay files created: 2.
- Report files created: 4.

## 13. Runtime checklist

Buildings:

- University requires Institutionalized Scientific Exchange.
- Government Administration requires Systematic Administrative Statistics.
- Naval Administration requires State Dockyard Systems.
- Barracks require Corps Organization.
- Arms Industry and Artillery Foundry require Regulated Small Arms.
- Chemical Plant and Explosives Factory require Industrial Acids.
- Food Industry and Furniture Manufactory require Interchangeable Manufacture.
- Glassworks requires Pressed Glass.
- Paper Mill requires Continuous Papermaking.
- Textile Mill requires Mechanized Weaving.
- Tooling Workshop requires Mechanical Tools.
- Shipyard, Port and Whaling Station require Marine Chronometry.
- Gold Field and Gold Mine require Applied Mineralogy.
- Steel Mill requires Puddling and Rolling.

Production methods:

- Cannons requires Standardized Field Artillery.
- Horizontal Drawer Cabinets requires Systematic Population Registration.
- Vertical Filing Cabinets requires Central Statistical Offices.
- Sheep Farms requires Selective Breeding.
- Soil Enriching Farming requires Advanced Crop Rotations.
- Rice-specific Soil Enriching Farming requires Advanced Crop Rotations.
- Mechanical coffee processes require Interchangeable Manufacture.
- Mechanized Looms and Sewing Machines require Mechanized Weaving.
- Mechanized Workshops requires Interchangeable Manufacture.
- Power of the Purse requires State Dockyard Systems.
- Pig Iron requires Coke Smelting.
- Saw Mills requires Mechanical Tools.

Runtime execution was not automated; manual in-game validation remains pending.

## 14. Final status

`TECH5B1_FROZEN_BUILDING_PM_TRANSFER = COMPLETE`

`STATUS = TECH5B1_STATIC_PASS_RUNTIME_PENDING`

No commit and no push were performed.
