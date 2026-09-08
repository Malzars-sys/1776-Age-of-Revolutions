# TECH6C3D — Downstream Industrial Chemistry Implementation Report

## Result

TECH6C3D is implemented and passes static validation and the Victoria 3 1.13.11 parser smoke test. It adds productive `industrial_chemicals` demand to exactly three audited existing PMs while preserving each PM’s gross base-price margin.

## Repository baseline

- Branch: `tech6c-goods-buildings-pm-implementation`
- Starting HEAD: `08614a77209e8c111d4dc5ba41d42e961d62844b`
- Canonical game: `C:\Games\Victoria 3\game`, version `1.13.11`
- Existing uncommitted TECH6C1–TECH6C3C work was preserved.
- No branch switch, commit, push, merge, rebase, reset, or discard operation was performed.

## Required pre-edit verification

All three current definitions matched the TECH6C3C audit before editing.

| PM | Definition | PMG | Building | Effective gate | Workforce | Pollution | Texture | Margin |
|---|---|---|---|---|---:|---:|---|---:|
| `pm_dye_production` | `common/production_methods/01_industry.txt` | `pmg_synthetic_dyes` | `building_synthetics_plant` | `aniline` through the building | 5,000 | 5 | `synthetic_dyes.dds` | 1,000 |
| `pm_rubber_grips` | `common/production_methods/01_industry.txt` | `pmg_base_building_tooling_workshop` | `building_tooling_workshop` | explicit `vulcanization`; building requires `coke_smelting` | 5,000 | 0 | `steel_tools.dds` | 2,500 |
| `pm_houseware_plastics` | `common/production_methods/01_industry.txt` | `pmg_base_building_glassworks` | `building_glassworks` | explicit `plastics`; building requires `traditional_glassmaking` | 5,000 | 15 | `houseware_plastics.dds` | 2,000 |

The effective prices also matched the audit: industrial chemicals 40, sulfur 50, fertilizer 30, salt 30, dye 40, rubber 40, steel 50, tools 40, oil 40, lead 40, and glass 40. No stop condition was triggered.

## Implemented changes

The complete before/after matrix is in [TECH6C3D_DOWNSTREAM_CHEMISTRY_IMPLEMENTATION_MATRIX.csv](TECH6C3D_DOWNSTREAM_CHEMISTRY_IMPLEMENTATION_MATRIX.csv).

### Synthetic dyes

`pm_dye_production` now uses:

```text
sulfur = 20
fertilizer = 30
salt = 10
industrial_chemicals = 10
-> dye = 90
```

The added chemical input abstracts coal-tar intermediates, acids, alkalis, aniline processing, and standardized reagents without creating separate intermediate goods.

### Rubber chemistry

`pm_rubber_grips` now uses:

```text
rubber = 10
steel = 30
industrial_chemicals = 5
-> tools = 115
```

The chemical input abstracts sulfur treatment, accelerants, compounding chemistry, and processing additives. No separate vulcanization good was created.

### Plastics and housewares

`pm_houseware_plastics` now uses:

```text
oil = 20
lead = 30
industrial_chemicals = 10
-> glass = 110
```

The current PM continues to use `glass` as its houseware/plastics output abstraction. No plastic good, refined fuel, or petroleum-refinery object was introduced.

## Economic verification

| PM | Input before | Output before | Margin before | Input after | Output after | Margin after |
|---|---:|---:|---:|---:|---:|---:|
| `pm_dye_production` | 2,200 | 3,200 | 1,000 | 2,600 | 3,600 | 1,000 |
| `pm_rubber_grips` | 1,900 | 4,400 | 2,500 | 2,100 | 4,600 | 2,500 |
| `pm_houseware_plastics` | 2,000 | 4,000 | 2,000 | 2,400 | 4,400 | 2,000 |

In each case, the added output value exactly offsets the added industrial-chemicals input value. Workforce, pollution, textures, gates, buildings, PMGs, and unrelated modifiers remain unchanged.

## Demand effect

Per active level:

- `pm_dye_production`: +10 industrial chemicals
- `pm_rubber_grips`: +5 industrial chemicals
- `pm_houseware_plastics`: +10 industrial chemicals

The conceptual one-level-each sum is 25 industrial chemicals. This is not a claim about world market demand.

## Protected content verification

Pre/post SHA-256 block comparisons confirm that these PMs are byte-identical through TECH6C3D:

- `pm_artificial_fertilizers`
- `pm_improved_fertilizer`
- `pm_nitrogen_fixation`
- `pm_leblanc_process`
- `pm_ammonia-soda_process`
- `pm_vacuum_evaporation`
- `pm_brine_electrolysis`
- `pm_leaded_glass`
- `pm_bleached_paper`

Whole-file pre/post hashes also match for the Chemical Works PM and PMG files, Chemical Works building, salt/limestone/cement/industrial-chemicals definitions, limestone quarry and PM, cement building and PM, construction PMs, and technology definitions. The combined state-region resource hash also remains identical.

Consequently:

- fertilizer and explosives chemistry are unchanged
- the legacy explosives `pm_leblanc_process` is unchanged
- Leaded Glass is unchanged after TECH6C3C
- Bleached Paper and textile chemical bleaching are unchanged
- Chemical Works and both producer PMs are unchanged
- goods definitions, state resources, and technology topology are unchanged
- no localization or asset file changed

## Future-hook update

[TECH6C3A_CHEMISTRY_FUTURE_HOOKS.csv](TECH6C3A_CHEMISTRY_FUTURE_HOOKS.csv) now marks `pm_dye_production`, `pm_rubber_grips`, and `pm_houseware_plastics` as `TECH6C3D_IMPLEMENTED` and records their exact final recipes. Fertilizer chemistry, explosives modernization, pharmaceuticals, petroleum refining, and additional Glassworks integration remain deferred.

## Static validation

Validation found:

- exactly one definition of each target PM
- exactly one existing PMG reference for each target PM
- all expected goods and technologies resolve in the effective mod/vanilla data
- zero duplicate target PM IDs
- zero invalid texture paths
- balanced braces in the modified PM file
- all protected block and file hashes unchanged
- state-resource hash unchanged
- three implementation-matrix records and three updated future hooks
- `git diff --check` passes

No new good, building, PM, PMG, technology, localization, or graphical asset was created.

## Parser smoke

Parser smoke: **PASS**. Victoria 3 `release/1.13.11` mounted the current mod during the approximately 40-second debug-mode run. Fresh `error.log` and `warning.log` scans returned zero targeted hits for the three PM IDs, industrial chemicals, dye, rubber, tools, glass, unknown goods/PMs, invalid modifiers, duplicate definitions, texture failures, and parser failures. No Victoria 3 process remained afterward. Full campaign runtime is not claimed.

## Git footprint

TECH6C3D changes one gameplay file: `common/production_methods/01_industry.txt`. Within it, only the three authorized PM material-balance hunks changed. It also creates this report and the implementation matrix, and updates the existing future-hook CSV.

## Machine-readable completion summary

```text
TECH6C3D_DOWNSTREAM_CHEMISTRY_IMPLEMENTATION = PASS

BRANCH = tech6c-goods-buildings-pm-implementation

VANILLA_CANONICAL_VERSION = 1.13.11

IMPLEMENTED_PMS =
- pm_dye_production
- pm_rubber_grips
- pm_houseware_plastics

DYE_FINAL =
- sulfur = 20
- fertilizer = 30
- salt = 10
- industrial_chemicals = 10
- dye = 90

DYE_MARGIN_BEFORE = 1000
DYE_MARGIN_AFTER = 1000

RUBBER_GRIPS_FINAL =
- rubber = 10
- steel = 30
- industrial_chemicals = 5
- tools = 115

RUBBER_GRIPS_MARGIN_BEFORE = 2500
RUBBER_GRIPS_MARGIN_AFTER = 2500

HOUSEWARE_PLASTICS_FINAL =
- oil = 20
- lead = 30
- industrial_chemicals = 10
- glass = 110

HOUSEWARE_PLASTICS_MARGIN_BEFORE = 2000
HOUSEWARE_PLASTICS_MARGIN_AFTER = 2000

NEW_INDUSTRIAL_CHEMICALS_DEMAND =
- dye = +10
- rubber_grips = +5
- houseware_plastics = +10

ONE_LEVEL_EACH_TOTAL_CHEMICAL_DEMAND = 25

FERTILIZER_CHEMISTRY_CHANGED = NO
EXPLOSIVES_CHEMISTRY_CHANGED = NO
LEGACY_PM_LEBLANC_PROCESS_CHANGED = NO

LEADED_GLASS_CHANGED = NO
CHEMICAL_WORKS_CHANGED = NO

GOODS_DEFINITIONS_CHANGED = NO
STATE_RESOURCE_FILES_CHANGED = 0
TECHNOLOGY_TOPOLOGY_CHANGED = NO
LOCALIZATION_FILES_CHANGED = 0
ASSET_FILES_CHANGED = 0

UNKNOWN_IDS = 0
DUPLICATE_PM_IDS = 0
INVALID_TEXTURE_PATHS = 0

STATIC_VALIDATION = PASS
PARSER_SMOKE = PASS
RUNTIME = NOT_CLAIMED

GAMEPLAY_FILES_CHANGED_BY_TECH6C3D = 1

COMMIT = NO
PUSH = NO

NEXT_PHASE =
TECH6C4_REFINED_FUELS_FOUNDATION

NEXT_PHASE_READY = YES
```
