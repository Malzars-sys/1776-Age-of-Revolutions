# TECH5B1-R2 ? Full Same-Path Building & Production Method Transfer Repair

## 1. Baseline

- `BRANCH = tech4c2-audit-snapshot`
- `HEAD = e26279bf32c3dae3359c32d68de9343f11a4883e`
- Initial WIP scope: exactly the four TECH5B1 snapshot reports, the R1 same-path test file, and the R1 report.
- Canonical mappings: `TECH5A_HIDDEN_ALIAS_BUILDING_PM_RESPONSIBILITY_MATRIX.csv` filtered strictly to `READY_MECHANICAL_TRANSFER`.
- `READY_MECHANICAL_TRANSFER_RELATIONS = 37`
- `UNIQUE_OBJECT_TYPE_PLUS_OBJECT_ID = 34`

## 2. Vanilla source and version

- `VANILLA_GAME_PATH = C:\Games\Victoria 3\game`
- `VANILLA_EXECUTABLE = C:\Games\Victoria 3\binaries\victoria3.exe`
- `VANILLA_VERSION = 1.13.9`
- All Vanilla sources were treated as read-only.
- Every R2 source is UTF-8 with BOM and LF line endings.

## 3. Failed late-file architecture

The original TECH5B1 implementation used late `99_tech5b1_frozen_technology_gate_overrides.txt` files. Runtime reported `Duplicated key ... will not be created`, so Vanilla objects remained effective.

- `LATE_99_TOP_LEVEL_OVERRIDE = INVALID`
- `FAILED_99_FILES_PRESENT = NO`
- The frozen TECH5A mapping design remains valid.

## 4. R1 runtime validation

Evidence source: `MANUAL_USER_RUNTIME_EVIDENCE`; Codex did not execute the game runtime.

- University required ?changes scientifiques.
- ?changes scientifiques displayed D?verrouille universit?.
- The user's post-restart error-log search returned no line for `building_university`, `common/buildings/07_government.txt`, or `Duplicated key building_university`.
- `R1_MANUAL_RUNTIME = PASS`
- `R1_ARCHITECTURE = VALID`
- `SAME_PATH_FILE_SHADOWING = VALID`
- `DUPLICATE_KEY_BUILDING_UNIVERSITY = 0`

## 5. Same-path architecture retained

Each destination was reconstructed from the complete binary Vanilla 1.13.9 file at the identical relative path. Only the authorized technology token inside each target object's `unlocking_technologies` gate was substituted. The R1 `07_government.txt` was rebuilt from Vanilla before both final mappings were applied.

No `replace_path`, descriptor edit, partial object override, or late `99_...` file is used.

## 6. Twelve same-path gameplay files

| Relative path | Changes | Vanilla SHA-256 | Mod SHA-256 | Normalized match |
| --- | ---: | --- | --- | --- |
| `common/buildings/01_industry.txt` | 12 | `7e41e84ab11ab85715badbea648f1ce938f989b00761f47882c65de986fcf25c` | `444e9ee511f0adfa28aacd718bcb712a8fcfa2020556fe3de3e6c83c84dad8ed` | YES |
| `common/buildings/03_mines.txt` | 2 | `54a725975ab9581af9ed28c49f2678bfdf6ff90f00deeb9e7f7afe3910819e6f` | `1d4a367f7fe58cf4098acae05f3a74354bf49e1969221c56f3318442794bbe78` | YES |
| `common/buildings/05_military.txt` | 2 | `087a66be18b234a8db58bbb3055a404296b47733fdb091f893c100961ecd1c3e` | `092f3796aa3358be24fcd6aeeaba1520d1666867c6af49c6f738c122e6ff787f` | YES |
| `common/buildings/07_government.txt` | 2 | `3c83d9f86d2d986e02749fc438959227012dccda54411f211c1cd7c8b3118954` | `d52f4b25dd8b953c16275972fffe8a89dbfae99a1da081420389e9b1a46dd836` | YES |
| `common/buildings/09_misc_resource.txt` | 1 | `35cd32a26048973da45b79c00c30fb473dcbf4e57591a436dc769ec6d8f2f6b7` | `3bc883527c44335d7cdebfecf0b53662f3f72bb11b6a6ca37d501546fd76a984` | YES |
| `common/buildings/11_private_infrastructure.txt` | 1 | `6e3a9f21fec99e13158a4ee10d6a92ce9cdc78e35e1ee0bc9bce6c6632165ae0` | `a711202365e76539a2c5a886131bd97a043353357f7cacf8b2dc1aa9feec36c7` | YES |
| `common/production_methods/01_industry.txt` | 5 | `d0abb71f6ba922f46e1e512810053d1206a3cbfd8a2ff419d8a66c87b8a36886` | `f318d8250938c1f1c2372fa9f63b54ccce60063df7d7076f46fe7fb85afd0f7f` | YES |
| `common/production_methods/02_agro.txt` | 3 | `40d5d3d776783624e004321a66dc45848f1d8c3d3cb264c612e3521ae11829e5` | `e7555db8724e4daf18bb86611a0183763a0ac79bcb744cad1e28145fbe808455` | YES |
| `common/production_methods/04_plantations.txt` | 2 | `a63a20209fa5d70c18cbd7a51c53d13bc4968bf8a94ae618b237487cda321390` | `70f4bdc649012e32d1fe3b83e8031b6847ec24489193d484b6de650b75df4b77` | YES |
| `common/production_methods/05_military.txt` | 1 | `7ff5cd54ae6ba592a44b49231547fce54d93f6060663891394a88fe315c5b3b1` | `c5c4ce51a3a56f7c1669119b65b3c410d82675684beb5b9da0e265813b60068b` | YES |
| `common/production_methods/07_government.txt` | 2 | `f74d57845a75e7568c211646366c1e809aa7242aebc712f42af4a728fb07d80d` | `542e81e0efafa1439644eada4287786ffcfee3f2151c5768566aa357519c9228` | YES |
| `common/production_methods/09_misc_resource.txt` | 1 | `e2aadd13e1b7042fc0ce85fb66ba016db0b3a06248e7a9d1eb5efa228d2bde0d` | `65d1a29ffe503c3bceb9f1d7ab7b753f22f723e2c315849a69ea48529edd0856` | YES |

- `SAME_PATH_GAMEPLAY_FILES = 12`
- `BUILDING_SAME_PATH_FILES = 6`
- `PRODUCTION_METHOD_SAME_PATH_FILES = 6`

## 7. Building transfers (20)

| Object | Same-path file | Old technology | New technology |
| --- | --- | --- | --- |
| `building_university` | `common/buildings/07_government.txt` | `academia` | `institutionalized_scientific_exchange` |
| `building_government_administration` | `common/buildings/07_government.txt` | `tech_bureaucracy` | `systematic_administrative_statistics` |
| `building_naval_administration` | `common/buildings/05_military.txt` | `admiralty` | `state_dockyard_systems` |
| `building_barrack` | `common/buildings/05_military.txt` | `standing_army` | `corps_organization` |
| `building_arms_industry` | `common/buildings/01_industry.txt` | `gunsmithing` | `regulated_small_arms` |
| `building_artillery_foundry` | `common/buildings/01_industry.txt` | `gunsmithing` | `regulated_small_arms` |
| `building_chemical_plant` | `common/buildings/01_industry.txt` | `intensive_agriculture` | `industrial_acids` |
| `building_explosives_factory` | `common/buildings/01_industry.txt` | `intensive_agriculture` | `industrial_acids` |
| `building_food_industry` | `common/buildings/01_industry.txt` | `manufacturies` | `interchangeable_manufacture` |
| `building_furniture_manufactory` | `common/buildings/01_industry.txt` | `manufacturies` | `interchangeable_manufacture` |
| `building_glassworks` | `common/buildings/01_industry.txt` | `manufacturies` | `pressed_glass` |
| `building_paper_mill` | `common/buildings/01_industry.txt` | `manufacturies` | `continuous_papermaking` |
| `building_textile_mill` | `common/buildings/01_industry.txt` | `manufacturies` | `mechanized_weaving` |
| `building_tooling_workshop` | `common/buildings/01_industry.txt` | `manufacturies` | `mechanical_tools` |
| `building_shipyard` | `common/buildings/01_industry.txt` | `navigation` | `marine_chronometry` |
| `building_port` | `common/buildings/11_private_infrastructure.txt` | `navigation` | `marine_chronometry` |
| `building_whaling_station` | `common/buildings/09_misc_resource.txt` | `navigation` | `marine_chronometry` |
| `building_gold_field` | `common/buildings/03_mines.txt` | `prospecting` | `applied_mineralogy` |
| `building_gold_mine` | `common/buildings/03_mines.txt` | `prospecting` | `applied_mineralogy` |
| `building_steel_mill` | `common/buildings/01_industry.txt` | `steelworking` | `puddling_and_rolling` |

## 8. Production-method transfers (14)

| Object | Same-path file | Old technology | New technology |
| --- | --- | --- | --- |
| `pm_cannons` | `common/production_methods/01_industry.txt` | `artillery` | `standardized_field_artillery` |
| `pm_vertical_filing_cabinets` | `common/production_methods/07_government.txt` | `central_archives` | `central_statistical_offices` |
| `pm_horizontal_drawer_cabinets` | `common/production_methods/07_government.txt` | `centralization` | `systematic_population_registration` |
| `pm_sheep_farms` | `common/production_methods/02_agro.txt` | `intensive_agriculture` | `selective_breeding` |
| `pm_soil_enriching_farming` | `common/production_methods/02_agro.txt` | `intensive_agriculture` | `advanced_crop_rotations` |
| `pm_soil_enriching_farming_building_rice_farm` | `common/production_methods/02_agro.txt` | `intensive_agriculture` | `advanced_crop_rotations` |
| `coffee_plantation_mechanical_drying` | `common/production_methods/04_plantations.txt` | `mechanized_workshops` | `interchangeable_manufacture` |
| `coffee_plantation_wet_process_mechanical` | `common/production_methods/04_plantations.txt` | `mechanized_workshops` | `interchangeable_manufacture` |
| `pm_mechanized_looms` | `common/production_methods/01_industry.txt` | `mechanized_workshops` | `mechanized_weaving` |
| `pm_mechanized_workshops` | `common/production_methods/01_industry.txt` | `mechanized_workshops` | `interchangeable_manufacture` |
| `pm_sewing_machines` | `common/production_methods/01_industry.txt` | `mechanized_workshops` | `mechanized_weaving` |
| `pm_power_of_the_purse` | `common/production_methods/05_military.txt` | `power_of_the_purse` | `state_dockyard_systems` |
| `pm_pig_iron` | `common/production_methods/01_industry.txt` | `steelworking` | `coke_smelting` |
| `pm_saw_mills` | `common/production_methods/09_misc_resource.txt` | `steelworking` | `mechanical_tools` |

`pm_soil_enriching_farming` remains one physical definition shared by four PMGs.

## 9. Byte/text parity

For each file, every authorized new technology was normalized back to its frozen old technology inside the target object and the complete bytes were compared with Vanilla.

- `NORMALIZED_FILES_IDENTICAL_TO_VANILLA = 12`
- `UNAUTHORIZED_FILE_DIFFERENCES = 0`
- `NON_GATE_FIELD_DIFFERENCES = 0`
- BOM preserved in all 12 files: YES.
- Line endings preserved in all 12 files: YES.
- Object order, comments, indentation, whitespace, fields, and non-target objects preserved: YES.

## 10. Physical and expanded relations

- `BUILDING_OBJECTS_CHANGED = 20`
- `PRODUCTION_METHOD_OBJECTS_CHANGED = 14`
- `PHYSICAL_OBJECT_GATE_CHANGES = 34`
- `EXPANDED_RELATIONS_TRANSFERRED = 37`

The 37/34 difference is entirely due to `pm_soil_enriching_farming` expanding across four TECH5A PMG relations while remaining defined once.

## 11. Hidden aliases before and after

- `SCOPED_GATE_RELATIONS_TOTAL = 308`
- `HIDDEN_ALIAS_RELATIONS_BEFORE = 64`
- `HIDDEN_ALIAS_RELATIONS_REMOVED = 37`
- `HIDDEN_ALIAS_RELATIONS_AFTER = 27`

Remaining aliases:

- `dialectics = 1`
- `enclosure = 16`
- `hydraulic_cranes = 1`
- `lathe = 3`
- `screw_frigate = 2`
- `urban_planning = 2`
- `urbanization = 2`

Transferred aliases `academia`, `admiralty`, `artillery`, `central_archives`, `centralization`, `gunsmithing`, `intensive_agriculture`, `manufacturies`, `mechanized_workshops`, `navigation`, `power_of_the_purse`, `prospecting`, `standing_army`, `steelworking`, and `tech_bureaucracy` each have zero remaining scoped relations.

## 12. Exact 27 preserved design responsibilities

| Alias | Type | Object | PMG | Building | Requirement |
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

- `DESIGN_REVIEW_RELATIONS_PRESERVED = 27`
- Every row remains `DESIGN_REVIEW_REQUIRED`.

## 13. PM progression recalculation

The full 197-row TECH5A progression audit was recalculated on the effective R2 gates. It reproduced the previous semantic simulation with zero row/field difference.

- `PM_PROGRESSION_RELATIONSHIPS_AUDITED = 197`
- `PM_PROGRESSION_RISKS_BEFORE = 46`
- `PM_PROGRESSION_RISKS_AFTER = 42`
- `PM_PROGRESSION_RESOLVED_BY_TRANSFER = 4`
- Post-transfer: 144 OK, 33 confirmed risks, 9 design reviews, and 11 intentional parallel/ownership relations.
- Change classes: 25 unchanged risks, 9 unchanged design reviews, 8 other classification changes, and 4 resolutions.

No prerequisite was added and no PM was reordered.

## 14. Scope guard

- `DISTINCT_TARGET_TECHNOLOGIES = 20`
- `UNKNOWN_TARGET_TECHNOLOGIES = 0`
- `BROKEN_TECH_REFERENCES = 0`
- `TECHNOLOGY_DEFINITIONS_CHANGED = 0`
- `TECHNOLOGY_PREREQUISITES_CHANGED = 0`
- `TECHNOLOGY_ERAS_CHANGED = 0`
- `PRODUCTION_METHOD_GROUPS_CHANGED = 0`
- `PM_ORDER_CHANGED = 0`
- `STARTING_TECH_CHANGES = 0`
- The four original TECH5B1 snapshot reports remain unchanged.
- The R1 report was modified only to record the supplied manual runtime PASS.
- New R2 files: 12 gameplay files and 5 reports.
- Commit: NONE. Push: NONE.

## 15. Manual runtime checklist R2

Close Victoria 3 completely, relaunch it, and verify at minimum:

Buildings:

- University ? ?changes scientifiques.
- Government Administration ? Systematic Administrative Statistics.
- Naval Administration ? State Dockyard Systems.
- Barracks ? Corps Organization.
- Arms Industry and Artillery Foundry ? Regulated Small Arms.
- Chemical Plant and Explosives Factory ? Industrial Acids.
- Food Industry and Furniture Manufactory ? Interchangeable Manufacture.
- Glassworks ? Pressed Glass.
- Paper Mill ? Continuous Papermaking.
- Textile Mill ? Mechanized Weaving.
- Tooling Workshop ? Mechanical Tools.
- Shipyard, Port, and Whaling Station ? Marine Chronometry.
- Gold Field and Gold Mine ? Applied Mineralogy.
- Steel Mill ? Puddling and Rolling.

Production methods:

- Cannons ? Standardized Field Artillery.
- Horizontal Drawer Cabinets ? Systematic Population Registration.
- Vertical Filing Cabinets ? Central Statistical Offices.
- Sheep Farms ? Selective Breeding.
- Soil Enriching Farming and its rice-specific variant ? Advanced Crop Rotations.
- Mechanical coffee processing ? Interchangeable Manufacture.
- Mechanized Looms and Sewing Machines ? Mechanized Weaving.
- Mechanized Workshops ? Interchangeable Manufacture.
- Power of the Purse ? State Dockyard Systems.
- Pig Iron ? Coke Smelting.
- Saw Mills ? Mechanical Tools.

Error-log command:

```powershell
Select-String `
  -Path "$env:USERPROFILE\Documents\Paradox Interactive\Victoria 3\logs\error.log" `
  -Pattern "Duplicated key building_|Duplicated key pm_|TECH5B1|07_government|01_industry|03_mines|05_military|09_misc_resource|11_private_infrastructure" `
  -Context 1,1
```

Confirm that none of the 34 objects reports `Duplicated key ... will not be created` because of the same-path files. Distinguish unrelated historical log errors.

### Runtime R2 — manual validation result

Evidence source: `MANUAL_USER_RUNTIME_EVIDENCE`; Codex did not execute the game runtime.

Observed in-game confirmations:

- `building_university` requires Échanges scientifiques (`institutionalized_scientific_exchange`).
- `building_steel_mill` requires Puddlage et laminage (`puddling_and_rolling`).
- `building_port` requires Chronométrie marine (`marine_chronometry`).
- `building_artillery_foundry` requires Armes réglementaires (`regulated_small_arms`).
- `standardized_field_artillery` displays that it unlocks `pm_cannons` for artillery foundries.
- After a complete game restart, the user's `Select-String` search for `Duplicated key building_`, `Duplicated key pm_`, and `TECH5B1` returned no lines.

Runtime closure counters:

- `MANUAL_USER_RUNTIME_EVIDENCE = YES`
- `RUNTIME_R2 = PASS`
- `DUPLICATE_KEY_ERRORS_R2 = 0`
- `SAME_PATH_FILE_SHADOWING = VALID`
- `TECH5B1R2_RUNTIME = PASS`
- `TECH5B1 = COMPLETE`

## 16. Final status

- `TECH5B1R2_FULL_SAME_PATH_TRANSFER = COMPLETE`
- `STATIC_VALIDATION = PASS`
- `MANUAL_USER_RUNTIME_EVIDENCE = YES`
- `RUNTIME_R2 = PASS`
- `DUPLICATE_KEY_ERRORS_R2 = 0`
- `SAME_PATH_FILE_SHADOWING = VALID`
- `TECH5B1R2_RUNTIME = PASS`
- `TECH5B1 = COMPLETE`

`TECH5B1R2_STATIC_AND_RUNTIME_PASS`

No commit and no push were performed.
