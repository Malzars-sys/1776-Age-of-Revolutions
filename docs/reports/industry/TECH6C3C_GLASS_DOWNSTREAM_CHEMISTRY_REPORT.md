# TECH6C3C — Glass and Downstream Chemistry Integration Report

## Result

TECH6C3C is implemented and passes static validation and the Victoria 3 1.13.11 parser smoke test. Its sole gameplay change is the approved material integration in `pm_leaded_glass`; all other chemistry sectors remain audit-only.

## Repository baseline

- Branch: `tech6c-goods-buildings-pm-implementation`
- Starting HEAD: `08614a77209e8c111d4dc5ba41d42e961d62844b`
- Canonical vanilla: `C:\Games\Victoria 3\game`, version `1.13.11`
- Existing uncommitted TECH6C1–TECH6C3B work was preserved.
- No commit, push, branch switch, merge, rebase, reset, or discard operation was performed.

## Pre-edit audit

The current file matched the TECH6C3B baseline exactly before editing:

| Property | Value |
|---|---|
| PM | `pm_leaded_glass` |
| Building | `building_glassworks` |
| PMG | `pmg_base_building_glassworks` |
| Gate | `industrial_ceramics` |
| Inputs | wood 20; lead 10 |
| Output | glass 40 |
| Workforce | 500 shopkeepers; 4,000 laborers; 500 machinists; total 5,000 |
| Pollution | 5 |
| Texture | `gfx/interface/icons/production_method_icons/leaded_glass.dds` |

The effective base prices were also unchanged: wood 20, lead 40, limestone 20, industrial chemicals 40, and glass 40. The approved balance therefore remained mechanically valid.

## Implemented recipe

The final `pm_leaded_glass` recipe is:

```text
wood = 20
lead = 10
limestone = 10
industrial_chemicals = 5
-> glass = 50
```

The technology gate, texture, PMG placement, workforce composition, and pollution were preserved.

### Economic verification

Before TECH6C3C:

- inputs: `(20 × 20) + (10 × 40) = 800`
- output: `40 × 40 = 1,600`
- gross pre-wage margin: `1,600 - 800 = 800`

After TECH6C3C:

- inputs: `(20 × 20) + (10 × 40) + (10 × 20) + (5 × 40) = 1,200`
- output: `50 × 40 = 2,000`
- gross pre-wage margin: `2,000 - 1,200 = 800`

Per level using the PM, the phase adds 10 limestone demand, 5 industrial-chemicals demand, and 10 glass output.

## Glassworks progression audit

The full table is in [TECH6C3C_GLASS_INTEGRATION_MATRIX.csv](TECH6C3C_GLASS_INTEGRATION_MATRIX.csv).

| PM | Gate | Inputs | Outputs | Workforce/delta | Pollution | Margin | Action |
|---|---|---|---|---:|---:|---:|---|
| `pm_forest_glass` | building: `traditional_glassmaking` | wood 30 | glass 30 | 5,000 | 0 | 600 | `KEEP_UNCHANGED` |
| `pm_leaded_glass` | `industrial_ceramics` | wood 20; lead 10; limestone 10; chemicals 5 | glass 50 | 5,000 | 5 | 800 | `IMPLEMENTED_TECH6C3C` |
| `pm_crystal_glass` | `crystal_glass` | lead 35 | glass 60 | 5,000 | 10 | 1,000 | `REVIEW_REQUIRED` |
| `pm_houseware_plastics` | `plastics` | oil 20; lead 30 | glass 100 | 5,000 | 15 | 2,000 | `FUTURE_CANDIDATE` |
| `pm_disabled_ceramics` | none | none | none | 0 | 0 | 0 | `KEEP_UNCHANGED` |
| `pm_ceramics` | `industrial_ceramics` | dye 5 | glass -10; porcelain 10 | shopkeepers +250 | 0 | 100 | `REVIEW_REQUIRED` |
| `pm_bone_china` | `chemical_bleaching` plus advanced base PM | dye 10 | glass -20; porcelain 30 | shopkeepers +500 | 0 | 900 | `KEEP_UNCHANGED` |
| `pm_manual_glassblowing` | none | none | none | 0 | 0 | 0 | `KEEP_UNCHANGED` |
| `pm_automatic_bottle_blowers` | `automatic_bottle_blowers` | tools 2; engines 2; oil 5 | none | laborers -2,500 | 5 | -400 operating cost | `NOT_RECOMMENDED` |

Only Leaded Glass receives new material inputs. Early forest glass remains chemistry-independent; automation remains an operating-cost versus wage-saving choice; the advanced and luxury tiers require a dedicated whole-PMG review before any later integration.

## Downstream chemistry audit

The complete 24-record audit is in [TECH6C3C_DOWNSTREAM_CHEMISTRY_AUDIT.csv](TECH6C3C_DOWNSTREAM_CHEMISTRY_AUDIT.csv). It records exact current recipes, gates, base-price margins, candidate inputs, recommended future recipes, confidence, and implementation status.

### Synthetic dyes

`pm_dye_production` is gated by `aniline` through `building_synthetics_plant`. The verified recipe is sulfur 20, fertilizer 30, salt 10 → dye 80, with 5,000 workers, pollution 5, and margin 1,000.

Recommended future test: add 10 industrial chemicals and raise dye output from 80 to 90. Both sides gain 400 value, preserving the margin at 1,000. Implementation remains deferred.

### Fertilizers

| PM | Gate | Inputs | Output | Workforce | Pollution | Margin |
|---|---|---|---|---:|---:|---:|
| `pm_artificial_fertilizers` | building: `industrial_acids` | sulfur 30; iron 10; salt 5 | fertilizer 90 | 5,000 | 5 | 650 |
| `pm_improved_fertilizer` | `improved_fertilizer` | sulfur 30; iron 30; salt 10 | fertilizer 140 | 5,000 | 10 | 1,200 |
| `pm_nitrogen_fixation` | `nitrogen_fixation` | sulfur 40; oil 20; iron 30; salt 20 | fertilizer 200 | 5,000 | 15 | 1,400 |

The foundation tier should remain unchanged. Later tests may replace part of raw sulfur with 5 industrial chemicals in Improved Fertilizer and 10 in Nitrogen Fixation. Natural/synthetic fertilizer geography and hypothetical phosphate/nitrate goods remain outside scope.

### Explosives

| PM | Gate | Inputs | Output | Margin |
|---|---|---|---|---:|
| `pm_leblanc_process` | building: `industrial_acids` | sulfur 20; fertilizer 20 | explosives 50 | 900 |
| `pm_ammonia-soda_process` | `nitroglycerin` | sulfur 30; fertilizer 30; paper 10 | explosives 80 | 1,300 |
| `pm_vacuum_evaporation` | `dynamite` | sulfur 40; fertilizer 40; paper 20 | explosives 110 | 1,700 |
| `pm_brine_electrolysis` | `electrical_capacitors` | sulfur 40; fertilizer 50; paper 30; electricity 20 | explosives 150 | 2,500 |

The legacy `pm_leblanc_process`, its inputs/output/gate, PMG membership, localizations, and history activations remain unchanged. Compatibility-aware modernization is deferred.

### Rubber and plastics

`pm_rubber_grips` is the strongest first rubber-chemistry candidate: rubber 10 + steel 30 → tools 110, gate `vulcanization`, workforce 5,000, margin 2,500. A later test adding 5 industrial chemicals and raising tools to 115 preserves that margin.

`pm_houseware_plastics` is the strongest existing plastics candidate: oil 20 + lead 30 → glass 100, gate `plastics`, workforce 5,000, pollution 15, margin 2,000. Adding 10 industrial chemicals and raising glass to 110 would preserve the margin.

Related rubber consumers (`pm_elastics`, automobile PMs, and `pm_telephones`) were inspected. Their final-assembly or additive-PMG roles make them weaker direct chemistry targets; no changes were made.

### Pharmaceuticals and petroleum refining

No dedicated pharmaceutical building/PM or petroleum-refinery building/PM exists in the current worktree. Both remain `FUTURE_NEW_INDUSTRY`; no IDs were invented.

## Future-hook update

[TECH6C3A_CHEMISTRY_FUTURE_HOOKS.csv](TECH6C3A_CHEMISTRY_FUTURE_HOOKS.csv) now records `pm_leaded_glass` as `TECH6C3C_IMPLEMENTED` with limestone 10, industrial chemicals 5, and glass 50. The `pm_leblanc_alkali_process` entry remains `TECH6C3B_IMPLEMENTED`, and deferred sectors remain deferred.

## Graphics and localization

The verified existing `leaded_glass.dds` texture is preserved. No DDS file or other asset changed. No new gameplay object was created, so no localization change was needed; the effective names remain “Leaded Glass” and “Verre plombé”.

## Validation

Static validation found:

- exactly one `pm_leaded_glass` definition and no duplicate PM IDs
- exact gate `industrial_ceramics`
- exact final inputs and output
- workforce 5,000 and pollution 5 preserved
- before and after gross margins both 800
- all referenced good, PM, and technology IDs resolve
- the existing texture path is valid
- no new good, building, PM, or PMG
- no localization file changed
- the tracked diff in `common/production_methods/01_industry.txt` contains only the approved Leaded Glass hunk plus the already-existing TECH6C3A Bleached Paper input
- `git diff --check` passes

Protected salt, limestone, quarry, state-region, cement, Chemical Works, producer PM, downstream consumer, technology, and explosives content was rechecked. No protected object was modified by TECH6C3C.

Parser smoke: **PASS**. Victoria 3 `release/1.13.11` mounted the current mod during the approximately 40-second debug-mode run. Fresh `error.log` and `warning.log` scans found zero targeted hits for `pm_leaded_glass`, limestone, industrial chemicals, `building_glassworks`, unknown goods/PMs, malformed or unknown modifiers, invalid/missing textures, and parser errors. No Victoria 3 process remained afterward. Full campaign runtime is not claimed.

## Git footprint

TECH6C3C changes one gameplay file: `common/production_methods/01_industry.txt`. It also creates this report and two CSV audits, and updates the existing future-hook CSV. No commit or push was performed.

## Machine-readable completion summary

```text
TECH6C3C_GLASS_AND_DOWNSTREAM_CHEMISTRY_INTEGRATION = PASS

BRANCH = tech6c-goods-buildings-pm-implementation

VANILLA_CANONICAL_VERSION = 1.13.11

IMPLEMENTED_PM =
- pm_leaded_glass

LEADED_GLASS_GATE =
- industrial_ceramics

LEADED_GLASS_INPUTS =
- wood = 20
- lead = 10
- limestone = 10
- industrial_chemicals = 5

LEADED_GLASS_OUTPUT =
- glass = 50

LEADED_GLASS_WORKFORCE = 5000
LEADED_GLASS_POLLUTION = 5

LEADED_GLASS_MARGIN_BEFORE = 800
LEADED_GLASS_MARGIN_AFTER = 800

DELTA_LIMESTONE_DEMAND = +10
DELTA_INDUSTRIAL_CHEMICALS_DEMAND = +5
DELTA_GLASS_OUTPUT = +10

DYE_CHEMISTRY =
- DEFERRED

FERTILIZER_CHEMISTRY =
- DEFERRED

EXPLOSIVES_CHEMISTRY =
- DEFERRED

RUBBER_CHEMISTRY =
- DEFERRED

PLASTICS_CHEMISTRY =
- DEFERRED

PHARMACEUTICALS =
- FUTURE_NEW_INDUSTRY

PETROLEUM_REFINING =
- FUTURE_NEW_INDUSTRY

LEGACY_EXPLOSIVES_PM_CHANGED = NO

SALT_CHANGED = NO
LIMESTONE_DEFINITION_CHANGED = NO
LIMESTONE_RESOURCE_FILES_CHANGED = 0
INDUSTRIAL_CHEMICALS_DEFINITION_CHANGED = NO
CHEMICAL_WORKS_CHANGED = NO
CEMENT_CHAIN_CHANGED = NO
TECHNOLOGY_TOPOLOGY_CHANGED = NO

UNKNOWN_IDS = 0
DUPLICATE_PM_IDS = 0
INVALID_TEXTURE_PATHS = 0

STATIC_VALIDATION = PASS
PARSER_SMOKE = PASS
RUNTIME = NOT_CLAIMED

GAMEPLAY_FILES_CHANGED_BY_TECH6C3C = 1

COMMIT = NO
PUSH = NO

NEXT_PHASE =
TECH6C3D_DOWNSTREAM_CHEMISTRY_IMPLEMENTATION

NEXT_PHASE_READY = YES
```
