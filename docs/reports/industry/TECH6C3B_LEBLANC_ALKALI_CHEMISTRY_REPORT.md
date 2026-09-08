# TECH6C3B — Leblanc Process and Industrial Alkali Chemistry Report

## Result

TECH6C3B implements a second, technology-gated Chemical Works production method without changing the legacy explosives chain. The new `pm_leblanc_alkali_process` connects salt, limestone, sulfur, coal, and tools to higher-throughput industrial-chemicals production under `industrial_alkalis`.

## Repository baseline

- Branch: `tech6c-goods-buildings-pm-implementation`
- Starting HEAD: `08614a77209e8c111d4dc5ba41d42e961d62844b`
- Canonical game version: Victoria 3 `1.13.11`
- Existing uncommitted TECH6C1–TECH6C3A work was preserved.
- No branch switch, commit, push, merge, rebase, reset, or discard operation was performed.

TECH6C3B does not edit the salt or limestone definitions, the limestone quarry, state-region files, the cement chain, construction PMs, downstream industrial-chemicals consumers, or technology definitions.

## Industrial Alkalis audit

The exact existing technology is `industrial_alkalis` in `common/technology/technologies/10_tech3a_production.txt`.

| Property | Current value |
|---|---|
| Era | `era_5` |
| Category | `production` |
| Parent | `industrial_acids` |
| AI behavior | Standard industrial/resource-expansion weight |
| Existing responsibility before TECH6C3B | One of the prerequisites of `pressed_glass` |
| New responsibility | Gate for `pm_leblanc_alkali_process` |

No era, parent, AI weight, research property, or topology was changed.

## Legacy Leblanc ID audit

The full machine-readable audit is in [TECH6C3B_LEGACY_LEBLANC_ID_AUDIT.csv](TECH6C3B_LEGACY_LEBLANC_ID_AUDIT.csv).

The existing `pm_leblanc_process` is defined in `common/production_methods/01_industry.txt`. It is the first member of `pmg_explosives_building_chemical_plant`, consumes 20 sulfur and 20 fertilizer, produces 50 explosives, employs 5,000 workers, and generates 10 pollution.

It has no explicit PM-level technology gate. Its effective availability is inherited from `building_explosives_factory`, which is gated by `industrial_acids`.

Its PMG progression is:

1. `pm_leblanc_process` — no explicit PM gate
2. `pm_ammonia-soda_process` — `nitroglycerin`
3. `pm_vacuum_evaporation` — `dynamite`
4. `pm_brine_electrolysis` — `electrical_capacitors`

The separately defined `pm_no_explosives_production` is not currently a member of that PMG. Therefore, `pm_leblanc_process` has no active predecessor inside the group.

Current fork references to the legacy ID are:

- its definition in `common/production_methods/01_industry.txt:1354`
- its PMG membership in `common/production_method_groups/01_industry.txt:172`
- two activations in `common/history/buildings/00_west_europe.txt:3006` and `:7605`
- one activation in `common/history/buildings/05_north_america.txt:1064`

English and French names are inherited from vanilla as “Leblanc Process” and “Procédé Leblanc”. Mechanically, the object is a live explosives baseline with starting-history dependencies. Semantically, its historical name is inaccurate for its current function. TECH6C3B records this as technical/historical debt and preserves the definition, inputs, output, gate, PMG membership, localizations, and history activations exactly.

## New Chemical Works PM

The safe internal ID is `pm_leblanc_alkali_process`; the display name remains historically correct:

- English: `Leblanc Process`
- French: `Procédé Leblanc`

It is the second member of `pmg_base_building_chemical_works`, after `pm_lead_chamber_process`, and is unavailable until `industrial_alkalis`.

### Final production values

| Metric | Value |
|---|---:|
| Salt input | 15 |
| Limestone input | 15 |
| Sulfur input | 12 |
| Coal input | 15 |
| Tools input | 5 |
| Industrial chemicals output | 65 |
| Workforce | 5,000 |
| Pollution | 20 |
| Laborer mortality multiplier | 0.15 |
| Machinist mortality multiplier | 0.10 |
| Engineer mortality multiplier | 0.05 |

The workforce is 500 shopkeepers, 2,500 laborers, 1,250 machinists, and 750 engineers. Total employment stays at 5,000 while shifting 500 jobs from laborers toward machinists and engineers, matching existing higher-tier industrial compositions.

Pollution rises from 15 to 20. The mortality modifiers use the same verified modifier keys as the Lead Chamber foundation, with values between that baseline and the substantially harsher existing mine benchmarks.

## Economic candidates

Base prices used are salt 30, limestone 20, sulfur 50, coal 30, tools 40, and industrial chemicals 40.

| Candidate | Salt | Limestone | Sulfur | Coal | Tools | Output | Input value | Output value | Margin | Assessment |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| A — conservative | 10 | 10 | 10 | 15 | 5 | 55 | 1,650 | 2,200 | 550 | Viable, but creates relatively modest salt and limestone demand |
| B — balanced | 15 | 15 | 12 | 15 | 5 | 65 | 2,000 | 2,600 | 600 | Selected |
| C — high-throughput | 18 | 18 | 12 | 18 | 5 | 70 | 2,240 | 2,800 | 560 | Viable, but materially heavier inputs for limited additional output |

Candidate B doubles the base-price input value and raises output by 62.5% while retaining the Lead Chamber’s gross margin of 600. This creates significant mineral demand without turning the upgrade into a free-money PM.

### Final comparison

| Process | Input value | Output value | Gross pre-wage margin |
|---|---:|---:|---:|
| Lead Chamber | 1,000 | 1,600 | 600 |
| Selected Leblanc alkali | 2,000 | 2,600 | 600 |
| Cement foundation | 1,050 | 1,600 | 550 |
| Forest Glass | 600 | 1,200 | 600 |
| Leaded Glass | 800 | 1,600 | 800 |
| Artificial Fertilizers | 2,050 | 2,700 | 650 |
| Bessemer Process | 3,300 | 4,500 | 1,200 |

### Incremental demand versus Lead Chamber

| Good | Delta per Chemical Works level |
|---|---:|
| Salt | +15 |
| Limestone | +15 |
| Sulfur | +2 |
| Coal | +5 |
| Tools | 0 |
| Industrial chemicals output | +25 |

## PMG progression

`pmg_base_building_chemical_works` now contains exactly, in order:

1. `pm_lead_chamber_process`
2. `pm_leblanc_alkali_process`

Both output industrial chemicals. The existing two consumers, `pm_bleached_paper` and `pm_chemical_bleaching_textile_mill`, are unchanged by TECH6C3B.

## Graphics audit

- Current Lead Chamber texture: `gfx/interface/icons/production_method_icons/leblanc_process.dds`
- Legacy explosives Leblanc texture: the same verified path
- New actual Leblanc alkali texture: the same verified path, explicitly marked `TECH6C3B REUSED_ASSET`
- Related verified alternative: `gfx/interface/icons/production_method_icons/ammonia_soda_process.dds`

The historically correct existing Leblanc icon is reused for the new PM. No icon was moved, deleted, or replaced; the Lead Chamber and legacy explosives assignments remain untouched. The shared use and the Lead Chamber’s temporary historical mismatch are documented asset debt.

## Optional Glassworks integration audit

`GLASS_LIMESTONE_INTEGRATION = RECOMMENDED_NEXT`.

The exact candidate is `pm_leaded_glass` in `common/production_methods/01_industry.txt`. It is gated by `industrial_ceramics`, currently consumes 20 wood and 10 lead, produces 40 glass, employs 5,000, and has a gross base-price margin of 800.

For TECH6C3C, the recommended test is to add 10 limestone and 5 industrial chemicals. Adding only those inputs would increase input value from 800 to 1,200 and reduce the margin from 800 to 400. Raising glass output from 40 to 50 in the same dedicated balance pass would restore output value to 2,000 and the margin to 800. No Glassworks gameplay was changed in TECH6C3B.

## Future chemistry hooks

[TECH6C3A_CHEMISTRY_FUTURE_HOOKS.csv](TECH6C3A_CHEMISTRY_FUTURE_HOOKS.csv) now records the implemented salt, limestone, sulfur, and `industrial_alkalis` connection under `pm_leblanc_alkali_process`. Glassworks, fertilizer and explosives modernization, synthetic dyes, pharmaceuticals, rubber chemistry, petroleum refining, and plastics/petrochemistry remain deferred. Missing pharmaceutical and refinery objects remain explicitly recorded as absent; no IDs were invented.

## Validation and protected-content integrity

Static validation verifies:

- one definition of `pm_leblanc_alkali_process`
- no duplicate `pm_leblanc_process` definition
- exactly two PMs in the Chemical Works PMG, each occurring once
- two industrial-chemicals producer options and two consumers
- all required salt, limestone, sulfur, coal, tools, technology, PM, and PMG IDs resolve
- the new PM consumes all four mandatory raw materials
- English and French localization keys are unique and both files retain UTF-8 BOM
- the reused texture exists in canonical vanilla 1.13.11
- all edited common-data files have balanced braces
- `git diff --check` passes

Pre/post SHA-256 checks are used for the salt definition, limestone definition and quarry, limestone PM, complete state-region set, cement building and PM, construction PMs, technology definition file, legacy explosives PM file, explosives PMG file, explosives building file, and history files. This establishes that their TECH6C3A-complete contents remain byte-identical through TECH6C3B.

Parser smoke: **PASS**. Victoria 3 `release/1.13.11` was launched in debug mode with the current mod content. The fresh `error.log` and `warning.log` scans returned zero targeted hits for `pm_leblanc_alkali_process`, the legacy `pm_leblanc_process`, `industrial_alkalis`, `industrial_chemicals`, `salt`, `limestone`, `building_chemical_works`, duplicate PM IDs, unknown goods or technologies, missing textures, invalid modifiers, PMG errors, localization errors, and parser failures. No Victoria 3 process remained after the run. This is not a claim of full campaign runtime testing.

## Change footprint

TECH6C3B changes four gameplay files:

- the existing TECH6C3A Chemical Works PM file
- the existing TECH6C3A Chemical Works PMG file
- the existing TECH6C3A English localization file
- the existing TECH6C3A French localization file

It creates this report, the implementation matrix, the legacy-ID audit, and updates the existing future-hook CSV. No protected gameplay directory or object is changed.

The detailed change matrix is in [TECH6C3B_LEBLANC_ALKALI_CHEMISTRY_MATRIX.csv](TECH6C3B_LEBLANC_ALKALI_CHEMISTRY_MATRIX.csv).

## Machine-readable completion summary

```text
TECH6C3B_LEBLANC_ALKALI_CHEMISTRY = PASS

BRANCH = tech6c-goods-buildings-pm-implementation

VANILLA_CANONICAL_VERSION = 1.13.11

INDUSTRIAL_ALKALIS_ID =
- industrial_alkalis

NEW_PM =
- pm_leblanc_alkali_process

DISPLAY_NAME_EN = Leblanc Process
DISPLAY_NAME_FR = Procédé Leblanc

LEBLANC_GATE =
- industrial_alkalis

LEBLANC_INPUTS =
- salt = 15
- limestone = 15
- sulfur = 12
- coal = 15
- tools = 5

LEBLANC_OUTPUT =
- industrial_chemicals = 65

LEBLANC_WORKFORCE = 5000
LEBLANC_POLLUTION = 20
LEBLANC_GROSS_MARGIN = 600

CHEMICAL_WORKS_PMS =
- pm_lead_chamber_process
- pm_leblanc_alkali_process

LEGACY_PM_LEBLANC_PROCESS =
- PRESERVED

LEGACY_EXPLOSIVES_BEHAVIOR_CHANGED = NO

LEBLANC_CONSUMES_SALT = YES
LEBLANC_CONSUMES_LIMESTONE = YES

SALT_DEFINITION_CHANGED = NO
LIMESTONE_DEFINITION_CHANGED = NO
LIMESTONE_RESOURCE_FILES_CHANGED = 0
CEMENT_CHAIN_CHANGED = NO
TECHNOLOGY_TOPOLOGY_CHANGED = NO

GLASS_LIMESTONE_INTEGRATION =
- RECOMMENDED_NEXT

UNKNOWN_IDS = 0
DUPLICATE_PM_IDS = 0
DUPLICATE_LOCALIZATION_KEYS = 0
INVALID_TEXTURE_PATHS = 0

STATIC_VALIDATION = PASS
PARSER_SMOKE = PASS
RUNTIME = NOT_CLAIMED

GAMEPLAY_FILES_CHANGED_BY_TECH6C3B = 4

COMMIT = NO
PUSH = NO

NEXT_PHASE =
TECH6C3C_GLASS_AND_DOWNSTREAM_CHEMISTRY_INTEGRATION

NEXT_PHASE_READY = YES
```
