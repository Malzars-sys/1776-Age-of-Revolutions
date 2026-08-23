# TECH5B2 — Manual Technology / Gameplay Responsibility Reconciliation

## 1. Canonical checkpoint

- Repository: `Malzars-sys/1776-Age-of-Revolutions`
- Branch: `tech4c2-audit-snapshot`
- Commit: `6021df7d17363dc315691804993cdecf32693594`
- Commit message: `Rework early production technology and industry gates`
- Parent: `e26279bf32c3dae3359c32d68de9343f11a4883e`
- This report documents the **current gameplay state at the checkpoint above**.
- Earlier TECH4C / TECH5A / TECH5B1 reports remain historical snapshots and are not rewritten.

## 2. Purpose

This reconciliation records the manual prerequisite and gameplay-gate decisions made after TECH5B1, synchronizes the current TECH3A index, and isolates the next remaining design problem without pretending that a complete global parser re-audit has already been rerun.

## 3. New early Production technologies

Three active Production technologies are now part of the current tree:

| Technology | Era | Prerequisites | Current responsibility |
|---|---:|---|---|
| `organized_forestry` | I | none | gates `building_logging_camp`; participates in the forestry/industrial branch |
| `traditional_papermaking` | I | none | gates `building_paper_mill`; prerequisite of `continuous_papermaking` |
| `traditional_glassmaking` | II | `organized_forestry` | gates `building_glassworks`; prerequisite of `industrial_ceramics` |

All three have English and French localization and use `gfx/error_manul.dds` as the project placeholder texture.

## 4. Current early Production causal chains

### Forestry / tools

`organized_forestry` → `building_logging_camp`

`precision_boring` + `organized_forestry` → `mechanical_tools` → `pm_saw_mills`

The direct `organized_forestry` prerequisite on `mechanical_tools` is **current accepted checkpoint state**. Because it propagates forestry into a broad industrial node, it can be revisited later as a semantic design choice, but it is not changed by this reconciliation.

### Paper

`traditional_papermaking` → `building_paper_mill`

`precision_boring` + `traditional_papermaking` → `continuous_papermaking`

The base PM chain is still:

`pm_pulp_pressing` → `pm_sulfite_pulping (mechanical_tools)` → `pm_bleached_paper (chemical_bleaching)`

The final transition is the next known cleanup target because `mechanical_tools` is Era V while `chemical_bleaching` is Era IV and neither gate is an ancestor of the other.

### Glass / ceramics

`organized_forestry` → `traditional_glassmaking` → `industrial_ceramics` → `crystal_glass`

Current building / PM responsibilities:

- `building_glassworks` → `traditional_glassmaking`
- `pm_ceramics` → `industrial_ceramics`
- `pm_leaded_glass` → `industrial_ceramics`
- `pm_crystal_glass` → `crystal_glass`
- `pm_bone_china` remains → `chemical_bleaching`
- `pm_houseware_plastics` remains → `plastics`; `plastics` is intentionally **not** made dependent on `crystal_glass`

This gives a causal Forest Glass → Leaded Glass → Crystal Glass progression without making the general plastics technology derive from crystal glass.

### Steam / engines

- `atmospheric_engine`: Era II; requires `shaft_mining` + `coke_smelting`
- `building_tooling_workshop` → `coke_smelting`
- `pm_pig_iron` → `precision_boring`
- `pm_steel` → `mechanical_tools`
- `building_motor_industry` → `rotative_steam_power`
- `high_pressure_steam` requires `atmospheric_engine` + `mechanical_tools` + `rotative_steam_power`
- medium frigate and ship-of-the-line propulsion modifications now require `high_pressure_steam`

## 5. Other prerequisite corrections at the checkpoint

- `standardized_field_artillery` now requires `regulated_small_arms`.
- `commercial_insurance_markets` requires `institutionalized_public_credit` + `international_relations`.
- `organized_elementary_schooling` requires `periodical_print_networks`.
- `experimental_research_laboratories` also requires `scientific_metrology`.
- `antibiotics` also requires `organized_immunization_campaigns`.
- `civilizing_mission` also requires `colonization`.
- `gantry_cranes` requires `mechanized_naval_dockyards` + `maritime_safety_standards`.
- `malaria_prevention` requires `civilizing_mission` + `organized_immunization_campaigns` + `quinine`.
- `modern_sewerage` is active/researchable in Era VIII after `organized_immunization_campaigns` and is removed from the GUI hidden-alias filters.
- `steel_frame_buildings` also requires `modern_sewerage`.
- `steam_donkey` requires `watertube_boiler` + `organized_forestry` + `mechanical_tools`.

## 6. Current building responsibility changes relevant to this reconciliation

- `building_logging_camp` → `organized_forestry`
- `building_paper_mill` → `traditional_papermaking`
- `building_glassworks` → `traditional_glassmaking`
- `building_tooling_workshop` → `coke_smelting`
- `building_motor_industry` → `rotative_steam_power`
- `building_shipyard` → `scientific_naval_architecture`
- `building_barrack` → `scientific_fortification_siegecraft`
- `building_naval_fortification` → `scientific_fortification_siegecraft`

The Barracks gate above is the current file state and supersedes the older TECH5B1 snapshot for current gameplay documentation.

## 7. Targeted structural validation

The edited subgraph was checked against the current checkpoint state used for this report:

| Check | Result |
|---|---|
| New/changed prerequisite IDs resolve to active technologies | PASS |
| Added prerequisite edges stay inside their effective technology category | PASS |
| Added prerequisite edges introduce an obvious era inversion | PASS — none found |
| Added prerequisite targets are hidden compatibility aliases | PASS — none |
| New technology localizations EN/FR | PASS |
| `modern_sewerage` still present in GUI hidden alias filters | PASS — removed |
| Known edited PM chains reviewed | PASS WITH ONE OPEN PAPER RISK |

Important scope note: this is a **targeted reconciliation audit**, not a replacement for the complete global parser-based TECH4C/TECH5A audit. A full global parser re-audit should be rerun after the remaining manual design cleanup is frozen.

## 8. Runtime evidence status

Manual runtime screenshots before commit confirmed the new forestry/paper/glass technologies load and localize, the Logging Camp / Paper Mill unlocks are visible, `continuous_papermaking` shows both intended prerequisites, and `steam_donkey` shows its three current prerequisites. Other previously tested gates remain outside the scope of a new complete runtime pass.

Therefore:

- `TARGETED_STATIC_VALIDATION = PASS`
- `TARGETED_RUNTIME_EVIDENCE = PARTIAL_PASS`
- `GLOBAL_PARSER_REAUDIT = PENDING`
- `GLOBAL_RUNTIME_RETEST = PENDING`

## 9. Open design item

### PAPER PM PROGRESSION

Current:

`pm_pulp_pressing (NONE)` → `pm_sulfite_pulping (mechanical_tools, Era V)` → `pm_bleached_paper (chemical_bleaching, Era IV)`

Classification: `PM_PROGRESSION_SKIP_AND_ERA_RISK`.

This should be the next manual design task. No automatic prerequisite or PM gate is imposed by this report.

## 10. Deliverables

- `TECH3A_IMPLEMENTED_TECH_INDEX.csv` — synchronized current index for the edited TECH3A rows plus the three new technologies.
- `TECH5B2_MANUAL_RECONCILIATION_CHANGE_LOG.csv` — current manual change register.
- `TECH5B2_CURRENT_TARGETED_GATE_AUDIT.csv` — targeted current building/PM/ship-mod gate audit.
- `TECH5B2_CURRENT_TARGETED_PM_PROGRESSION_AUDIT.csv` — focused PM progression audit for the edited chains.
- `TECH5B2_MANUAL_RECONCILIATION_REPORT.md` — this report.

`TECH5B2_MANUAL_RECONCILIATION = COMPLETE_AT_6021DF7`
