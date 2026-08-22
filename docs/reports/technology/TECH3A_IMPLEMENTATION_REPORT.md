# TECH-3A — Implementation Report

Status: `PASS_STATIC_AND_PARSER_SMOKE` · Branch: `technology-rework` · Baseline HEAD: `50d0ee9`

## 1. Implemented scope

TECH-3A implements the frozen 118-node 1700–1836 technology skeleton without adding economic unlocks, goods, buildings, PM/PMG, country grants, resource discovery, ship modifications or setup changes.

Implemented:

- twelve technology eras, with the frozen 118 nodes in eras I–VI;
- 42 Production, 21 Military, 15 Naval and 40 Society conceptual branches;
- the complete frozen prerequisite graph, including exactly 14 hard cross-branch edges;
- provisional era costs;
- valid base AI weights on every integrated definition and safe general context for Production and Naval nodes;
- English and French names and descriptions;
- valid technology textures;
- explicit compatibility bridges into later vanilla technologies;
- preservation of all other vanilla 1.13.9 technology definitions under directory replacement;
- the three required TECH-3A CSV registers/indexes.

Not implemented, as required: salt, spices, copper or other goods; buildings; economic PM/PMG; full redistribution of the 277 vanilla relationships; Seppings gating; Copper Sheathing component; setup/grants; economic AI; discovery; companies; Industrial Knowledge; final pacing.

## 2. Engine architecture and replacement semantics

Victoria 3 1.13.9 exposes only three engine technology categories: `production`, `military`, and `society`. There is no valid `category = naval` enum in the vanilla database. The frozen Naval branch is therefore retained as a distinct conceptual branch, a separate definition file and separate report/index classification, while its 15 nodes use the engine category `military`. This is a demonstrated engine constraint, not a change to TECH-2H's historical architecture.

Technology definitions do not expose manual position coordinates. The Technology Tree derives layout from category, era and prerequisites. No GUI override was introduced; the four conceptual branches remain identifiable through the separate Naval subgraph inside the engine's Military view. Visual overlap and readability require the human runtime checklist below.

The mod now declares:

```text
replace_path="common/technology/eras"
replace_path="common/technology/technologies"
```

This prevents the game and mod from defining the same vanilla-preserved ID twice. Because replacement removes the vanilla directories as mounted sources, TECH-3A includes:

- 118 integrated definitions for eras I–VI;
- 158 other vanilla 1.13.9 definitions, copied without removing their modifiers, effects or AI logic and provisionally remapped into eras VII–XII;
- 276 unique database definitions in total;
- 0 duplicate IDs.

The 21 integrated rows with `vanilla_id_preserved = YES` reuse the exact ID and vanilla icon. Their existing vanilla `modifier` and `on_researched` blocks are retained byte-for-content inside the new definition. Their era, prerequisites and AI base are intentionally supplied by the frozen TECH-2H skeleton. This is the least destructive method compatible with a complete early-tree replacement.

Original vanilla era-I nodes not selected by TECH-2H remain as era-VII compatibility nodes until their 277 unlock relationships are redistributed in a later phase. Vanilla eras II–V are provisionally mapped to VII, IX, XI and XII respectively, preserving their definitions and approximate original costs without pretending that later-tree pacing is frozen.

## 3. Definition files

| File | Responsibility |
|---|---|
| `common/technology/eras/00_tech3a_eras.txt` | twelve era definitions and costs |
| `common/technology/technologies/10_tech3a_production.txt` | 42 integrated Production nodes |
| `common/technology/technologies/20_tech3a_military.txt` | 21 integrated Military nodes |
| `common/technology/technologies/25_tech3a_naval.txt` | 15 integrated Naval nodes using engine category `military` |
| `common/technology/technologies/30_tech3a_society.txt` | 40 integrated Society nodes |
| `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt` | 158 preserved vanilla compatibility definitions |

All six script files use UTF-8 with BOM and balanced braces.

## 4. Eras and provisional costs

The early cost curve is deliberately test-only:

| Era | Window | Nodes | Band | Temporary cost |
|---|---|---:|---|---:|
| I | c.1690–1719 | 13 | `BAND_A_LOWEST` | 2,500 |
| II | 1720–1749 | 6 | `BAND_B_LOW` | 3,500 |
| III | 1750–1774 | 19 | `BAND_C_LOW_MEDIUM` | 4,500 |
| IV | 1775–1799 | 28 | `BAND_D_MEDIUM` | 6,000 |
| V | 1800–1824 | 33 | `BAND_E_MEDIUM_HIGH` | 7,500 |
| VI | 1825–1849 | 19 | `BAND_F_HIGH` | 9,000 |

Compatibility infrastructure uses era VII 10,000; VIII 11,250; IX 12,500; X 13,750; XI 15,000; XII 17,500. The mapped vanilla cost anchors remain 10,000, 12,500, 15,000 and 17,500. All numeric values remain `PROVISIONAL_RUNTIME_TEST_REQUIRED`.

`INDUSTRIAL_KNOWLEDGE_STATUS = DEFERRED_PACING_TEST`.

## 5. Frozen prerequisite graph

The generated prerequisites match the canonical CSV exactly for all 118 integrated nodes:

- hard cross-branch edges: 14;
- unexpected hard cross-branch edges: 0;
- broken prerequisites: 0;
- prerequisite cycles: 0;
- `BASELINE_*` prerequisite placeholders: 0.

The rejected TECH-2 edges were not reintroduced. In particular:

- Scientific Exchange does not gate Industrial Acids;
- High-Pressure Steam does not gate Paddle Steamer;
- Coke Smelting does not gate Mysorean Iron-Cased Rocketry;
- Mechanized Weaving does not gate Labor Movement.

`international_relations` remains a distinct Society technology with its vanilla ID and localization. It is not merged with Institutionalized Scientific Exchange.

Mysorean Iron-Cased Rocketry is present and visible as a regional/event-acquired definition with `can_research = no`. No country receives it in TECH-3A.

## 6. Post-1836 compatibility bridges

The preserved vanilla compatibility definitions receive the required direct bridge prerequisites without pulling their content into eras I–VI:

- Optical Telegraph Networks → `electric_telegraph`;
- Iron Hull Construction → `ironclad_tech`;
- Hydraulic Cements → `reinforced_concrete`;
- Hot Blast Smelting → `bessemer_process`;
- Percussion Cap → `repeaters` → `bolt_action_rifles`;
- Early Socialism & Cooperativism → `socialism` and `anarchism`;
- Railways remains the prerequisite for `steel_railway_cars` through its preserved vanilla definition.

Geological Surveying remains a terminal era-VI bridge for future specialized geology; no resource-discovery objects are introduced.

## 7. AI weights

Every integrated definition contains a valid `ai_weight` block.

- safe roots receive base 2;
- other universal nodes receive base 1;
- Mysorean Iron-Cased Rocketry receives base 0.25 but is not directly researchable;
- Production technologies add 1 for the existing vanilla industrial/resource expansion strategies;
- Naval technologies add 1 when `navy_size >= 5`, using syntax already present in vanilla technology AI;
- Military and Society retain safe base weights where a generic context could not be added without inventing the future AI Core.

No country-specific research AI was added. Advanced geography, literacy, university, bureaucracy, army and adoption weighting remains `TECH-3F` work.

## 8. Localization and icons

The two TECH-3A localization files contain all 118 names and all 118 description keys in English and French, plus the revised twelve-era concept description. There are no `TODO`, `TBD`, `TEMP DESCRIPTION` or placeholder-description strings.

The 21 preserved vanilla IDs reuse their vanilla names, descriptions and technology icons where semantically valid. New technologies use the canonical `gfx/error_manul.dds`. This path resolves to the already tracked mod copy, whose SHA-256 matches vanilla `gfx/interface/error_manul.dds` exactly. No technology uses `gfx/error_deer.dds`.

Validation:

- missing English names/descriptions: 0;
- missing French names/descriptions: 0;
- missing icon declarations: 0;
- invalid icon paths: 0;
- building placeholder used for technology: 0.

## 9. Deferred-resource reevaluation

The mandatory reevaluation rule promotes two formerly deferred goods:

1. `copper` → `REQUIRED_PRE_1836`: Copper Sheathing's defining construction cost is copper plate. Iron or hardwood would create the wrong material and market pressure.
2. `industrial_chemicals` → `REQUIRED_PRE_1836`: Industrial Acids, Alkalis, Chemical Bleaching and Active-Principle Pharmacy require an intermediate chemical/reagent layer. Fertilizer or explosives are downstream goods and would reverse the chain.

These promotions are documentary and binding for later pre-1836 economic phases. Neither good is implemented in TECH-3A.

Salt and spices were already required and remain `REQUIRED_PRE_1836_NOT_IMPLEMENTED_IN_3A`. Cement, pharmaceuticals and specialized resource potentials remain deferred because TECH-3A does not yet demonstrate a necessary standalone market good/system for them.

## 10. Static validation

Independent parsing of the generated files produced:

```text
DATABASE_TECH_DEFINITIONS = 276
DATABASE_TECH_IDS_UNIQUE = 276
INTEGRATED_TECH_DEFINITIONS = 118
EARLY_NON_INTEGRATED_TECHS = 0

PRODUCTION = 42
MILITARY = 21
NAVAL = 15
SOCIETY = 40

ERA_I = 13
ERA_II = 6
ERA_III = 19
ERA_IV = 28
ERA_V = 33
ERA_VI = 19

DUPLICATE_TECH_IDS = 0
MISSING_TECH_DEFINITIONS = 0
MISSING_REQUIRED_FIELDS = 0
BROKEN_PREREQUISITES = 0
PREREQUISITE_CYCLES = 0
INTEGRATED_CSV_PREREQUISITE_MISMATCHES = 0
HARD_CROSS_BRANCH_EDGES = 14
UNEXPECTED_HARD_CROSS_BRANCH_EDGES = 0
BASELINE_PLACEHOLDERS_USED_AS_GAMEPLAY_TECHS = 0
MISSING_TECH_LOCALIZATION = 0
MISSING_TECH_DESCRIPTIONS = 0
MISSING_TECH_ICONS = 0
INVALID_ICON_PATHS = 0
NEW_TECH_WITHOUT_AI_WEIGHT = 0
```

## 11. Parser/log smoke test

A fresh hidden debug launch was run directly against Victoria 3 1.13.9 with:

```text
victoria3.exe -debug_mode -mod=".../1776_Age_of_Revolutions_fork/descriptor.mod"
```

The launch rotated the logs, mounted the mod, enumerated `common/technology/eras`, continued through database and technology-event loading, and produced:

```text
FRESH_ERROR_LOG_BYTES = 0
FRESH_TECH3A_ERROR_MATCHES = 0
TECH3A_ATTRIBUTABLE_ERRORS = 0
UNKNOWN_ERRORS = 0
PARSER_LOG_SMOKE = PASS
```

The process was launched only for this smoke test and was closed after parser/event loading. Because it ran hidden and no automated Victoria 3 UI controller is available, the Technology screen, active research and save/load checks remain `HUMAN_REQUIRED`, not falsely reported as passes.

Human checklist:

1. Start a new game with only this mod enabled and open Technology.
2. Confirm eras I–VI render and that badges VII–XII remain reachable by horizontal scrolling.
3. Count/spot-check the early branches: 42 Production; 36 engine-Military entries consisting of 21 Military plus the separate 15-node Naval subgraph; 40 Society.
4. Confirm nodes do not overlap critically and prerequisite lines remain readable, especially the 14 cross-branch links.
5. Select a directly researchable new node such as `coke_smelting`, start research and advance at least one week.
6. Confirm `mysorean_iron_cased_rocketry` is visible but cannot be selected directly.
7. Save, return to menu, reload, and verify the active research plus completed prerequisites are unchanged.
8. Inspect `error.log`, `game.log`, `debug.log`, `gui.log` and `graphics.log` for new TECH-3A-attributable diagnostics.

## 12. Scope and changed files

Authorized gameplay changes are limited to technology era/definition files, technology localization, and the two replacement declarations needed to load them. Documentation consists of this report and the three required CSVs.

No good, building, economic PM/PMG, country/state setup, ship modification, company, trade system, resource potential, economic AI bootstrap or interface file was created or modified.

No commit or push was performed.

TECH3A_IMPLEMENTATION = PASS

BRANCH = technology-rework
HEAD_BEFORE = 50d0ee9

TOTAL_TECHS_EXPECTED = 118
TOTAL_TECHS_IMPLEMENTED = 118

PRODUCTION_TECHS = 42
MILITARY_TECHS = 21
NAVAL_TECHS = 15
SOCIETY_TECHS = 40

ERA_I = 13
ERA_II = 6
ERA_III = 19
ERA_IV = 28
ERA_V = 33
ERA_VI = 19

HARD_CROSS_BRANCH_EDGES = 14
EXPECTED_HARD_CROSS_BRANCH_EDGES = 14

DUPLICATE_TECH_IDS = 0
MISSING_TECH_DEFINITIONS = 0
BROKEN_PREREQUISITES = 0
PREREQUISITE_CYCLES = 0

MISSING_TECH_LOCALIZATION = 0
MISSING_TECH_DESCRIPTIONS = 0
MISSING_TECH_ICONS = 0
INVALID_ICON_PATHS = 0
NEW_TECH_WITHOUT_AI_WEIGHT = 0

TECH_PLACEHOLDER_ICON = gfx/error_manul.dds
BUILDING_PLACEHOLDER_ICON_USED_FOR_TECH = 0

VANILLA_IDS_PRESERVED = 21
VANILLA_IDS_ACCIDENTALLY_DUPLICATED = 0

PRE1836_RESOURCE_PROMOTIONS = 2
PRE1836_RESOURCE_REVIEW_REQUIRED = 0

SALT_STATUS = REQUIRED_PRE_1836_NOT_IMPLEMENTED_IN_3A
SPICES_STATUS = REQUIRED_PRE_1836_NOT_IMPLEMENTED_IN_3A
COPPER_STATUS = REQUIRED_PRE_1836_NOT_IMPLEMENTED_IN_3A

TECH3A_ATTRIBUTABLE_ERRORS_AFTER = 0

TECHNOLOGY_SCREEN_RUNTIME = HUMAN_REQUIRED
RESEARCH_RUNTIME = HUMAN_REQUIRED
SAVE_LOAD_RUNTIME = HUMAN_REQUIRED

OUT_OF_SCOPE_GAMEPLAY_FILES_CHANGED = 0

REPORT =
docs/reports/technology/TECH3A_IMPLEMENTATION_REPORT.md

INDEX =
docs/reports/technology/TECH3A_IMPLEMENTED_TECH_INDEX.csv

RESOURCE_PROMOTION_REGISTER =
docs/reports/technology/TECH3A_PRE1836_RESOURCE_PROMOTION_REGISTER.csv

TEMP_COSTS =
docs/reports/technology/TECH3A_TEMPORARY_TECH_COSTS.csv

COMMIT_CREATED = NO
PUSH_PERFORMED = NO

TECH3A_READY_FOR_HUMAN_REVIEW = YES
