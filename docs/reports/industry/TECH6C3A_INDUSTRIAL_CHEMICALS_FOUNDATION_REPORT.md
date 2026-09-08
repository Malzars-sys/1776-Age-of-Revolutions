# TECH6C3A — Industrial Chemicals Foundation Report

## Result

TECH6C3A is implemented and passes the targeted static and parser-smoke checks. The phase introduces one industrial good, one heavy-industry building, one producer production method, one production-method group, and two productive downstream consumers. It does not change technology topology, state resources, salt, limestone, or cement.

## Repository baseline

- Branch: `tech6c-goods-buildings-pm-implementation`
- Baseline HEAD: `08614a77209e8c111d4dc5ba41d42e961d62844b`
- Pre-existing TECH6C1–TECH6C2B worktree changes were preserved.
- The existing salt content, limestone good and quarry, 675-state limestone distribution (674 nonzero, Iceland zero, total potential 21,520), cement chain, and `portland_cement` technology remain untouched by TECH6C3A.
- No commit, push, branch switch, reset, or destructive Git operation was performed.

## Implemented IDs

| Type | ID | Status |
|---|---|---|
| Good | `industrial_chemicals` | New |
| Building | `building_chemical_works` | New |
| PMG | `pmg_base_building_chemical_works` | New |
| Producer PM | `pm_lead_chamber_process` | New |
| Consumer PM | `pm_bleached_paper` | Existing PM, one new input only |
| Consumer PM | `pm_chemical_bleaching_textile_mill` | New |

The detailed object/file mapping is in [TECH6C3A_INDUSTRIAL_CHEMICALS_FOUNDATION_MATRIX.csv](TECH6C3A_INDUSTRIAL_CHEMICALS_FOUNDATION_MATRIX.csv).

## Good definition

`industrial_chemicals` is a tradeable industrial good with:

- base cost `40`
- traded quantity `5`, producing a trade-lot value of `200`
- prestige factor `5`
- convoy-cost multiplier `0.5`
- no direct POP need or consumption

The values align with established intermediate industrial goods such as dye, glass, and tools rather than with a direct-consumption commodity.

## Chemical Works foundation

`building_chemical_works` is a city-based `bg_heavy_industry` building. It uses `construction_cost_very_high`, the standard industry ownership restrictions, self-ownership, and the existing heavy-industry building-panel background.

Its economic-scale AI behavior is inherited from `bg_heavy_industry`, matching comparable current industry buildings; no unsupported building-specific AI block was added.

Its sole foundation PM is `pm_lead_chamber_process`:

| Metric | Value |
|---|---:|
| Sulfur input | 10 |
| Coal input | 10 |
| Tools input | 5 |
| Industrial chemicals output | 40 |
| Workforce | 5,000 |
| Pollution | 15 |
| Laborer mortality multiplier | 0.10 |
| Machinist mortality multiplier | 0.05 |
| Engineer mortality multiplier | 0.02 |

The workforce composition is 500 shopkeepers, 3,000 laborers, 1,000 machinists, and 500 engineers. The mortality modifiers intentionally represent the dangerous acid-industry working environment while using existing valid modifier IDs.

## Technology gates

- `building_chemical_works` is unlocked by `industrial_acids`.
- `pm_lead_chamber_process` inherits that building gate.
- `pm_bleached_paper` retains its existing `industrial_paper_bleaching` gate.
- `pm_chemical_bleaching_textile_mill` is gated by `chemical_bleaching`.

The requested name `chlorine_bleaching` does not exist in the current fork or the checked vanilla data. The exact existing equivalent is `chemical_bleaching`; it was reused instead of inventing a new technology ID. The existing chain remains `industrial_acids` → `chemical_bleaching` → `industrial_paper_bleaching`. No technology definition, parent, era, unlock block, or topology was changed.

## Economic balance

All values below use base good prices and are gross pre-wage margins per building level.

| PM or benchmark | Input value | Output value | Gross margin | Workforce | Pollution |
|---|---:|---:|---:|---:|---:|
| Lead Chamber Process | 1,000 | 1,600 | 600 | 5,000 | 15 |
| Cement foundation | 1,050 | 1,600 | 550 | 5,000 | 15 |
| Forest Glass | 600 | 1,200 | 600 | 5,000 | 0 |
| Artificial Fertilizers | 2,050 | 2,700 | 650 | 5,000 | 5 |
| Blister Steel Process | 2,500 | 3,250 | 750 | 5,000 | 10 |
| Bleached Paper, after TECH6C3A | 1,900 | 3,000 | 1,100 | 5,000 | 5 |
| Chemical Bleaching, Textile Mill | 1,400 | 2,400 | 1,000 | 5,000 | 5 |

The producer margin of `600` is competitive with adjacent foundation industries without exceeding the stronger steel benchmark. Producer pollution is intentionally high, while both consumer PMs retain moderate pollution.

## Productive demand

The new good has one producer and two industrial consumers at phase completion:

1. `pm_bleached_paper` now consumes 10 industrial chemicals while retaining its existing output, workforce, gate, and unrelated inputs.
2. `pm_chemical_bleaching_textile_mill` consumes 10 industrial chemicals and upgrades fabric and dye into clothes under `chemical_bleaching`.

This prevents a dead good at introduction. No POP need was added.

## Asset reuse

No new art was generated. Existing, validated game assets are reused:

- good: `gfx/interface/icons/goods_icons/fertilizer.dds`
- building: `gfx/interface/icons/building_icons/chemicals_industry.dds`
- building background: `gfx/interface/icons/building_icons/backgrounds/building_panel_bg_heavy_industry.dds`
- PMG: `gfx/interface/icons/generic_icons/mixed_icon_base.dds`
- producer PM: `gfx/interface/icons/production_method_icons/leblanc_process.dds`
- textile consumer PM: `gfx/interface/icons/production_method_icons/bleached_paper.dds`

## Deferred chemistry hooks

The future-hook audit is recorded in [TECH6C3A_CHEMISTRY_FUTURE_HOOKS.csv](TECH6C3A_CHEMISTRY_FUTURE_HOOKS.csv). It covers the existing explosives, fertilizer, dye, glass, rubber, plastic, paper, and textile objects, and explicitly records the absence of current pharmaceutical and dedicated petroleum-refinery objects without inventing IDs.

The existing `pm_leblanc_process` currently belongs to the explosives chain and produces explosives from sulfur and fertilizer. TECH6C3A does not modify it. A future historically explicit Leblanc chemistry phase must resolve that legacy ID/meaning conflict before introducing salt- and limestone-based alkali chemistry.

## Validation

Static validation found:

- exactly one definition for every new good, building, PM, and PMG
- exactly one industrial-chemicals producer
- exactly two industrial-chemicals consumers
- zero direct POP consumers
- zero missing or duplicate required English/French localization keys
- zero missing referenced texture files
- balanced braces in all new common-data files
- UTF-8 BOM present in both localization files
- zero `concrete` references in TECH6C3A implementation files
- only the intended one-line additions in the two existing PM/PMG files
- clean `git diff --check`

A Victoria 3 `release/1.13.11` debug-mode parser smoke test mounted the mod successfully. The targeted fresh-log scan found zero occurrences for the new IDs and zero matching unknown-good, unknown-PM, unknown-building, invalid-modifier, invalid-texture, or parser-failure diagnostics. The game process was then stopped and no process was left running. This is a parser/load smoke test, not a claim of full campaign runtime validation.

## Change footprint

TECH6C3A changes eight gameplay files:

- four new `common/` files
- two minimal edits to existing PM/PMG files
- two new localization files

It also adds this report and two CSV audit artifacts. No map/state-region, technology, salt, limestone, or cement file was changed by TECH6C3A.

## Machine-readable completion summary

```text
TECH6C3A_INDUSTRIAL_CHEMICALS_FOUNDATION = PASS

BRANCH = tech6c-goods-buildings-pm-implementation

VANILLA_CANONICAL_VERSION = 1.13.11

NEW_GOODS =
- industrial_chemicals

NEW_BUILDINGS =
- building_chemical_works

NEW_PMS =
- pm_lead_chamber_process
- pm_chemical_bleaching_textile_mill

NEW_PMGS =
- pmg_base_building_chemical_works

CHEMICAL_WORKS_GATE = industrial_acids

BASE_CHEMICAL_PM =
- pm_lead_chamber_process

BASE_INPUTS =
- sulfur = 10
- coal = 10
- tools = 5

BASE_OUTPUT =
- industrial_chemicals = 40

BASE_WORKFORCE = 5000
BASE_POLLUTION = 15

INDUSTRIAL_CHEMICALS_PRODUCERS = 1
INDUSTRIAL_CHEMICALS_CONSUMERS = 2

DOWNSTREAM_CONSUMERS =
- pm_bleached_paper
- pm_chemical_bleaching_textile_mill

INDUSTRIAL_CHEMICALS_DIRECT_POP_CONSUMPTION = 0

SALT_CHANGED = NO
LIMESTONE_CHANGED = NO
LIMESTONE_RESOURCE_FILES_CHANGED = 0
CEMENT_CHAIN_CHANGED = NO
TECHNOLOGY_TOPOLOGY_CHANGED = NO

LEBLANC_IMPLEMENTATION = DEFERRED

UNKNOWN_IDS = 0
DUPLICATE_DEFINITIONS = 0
DUPLICATE_LOCALIZATION_KEYS = 0
INVALID_TEXTURE_PATHS = 0

STATIC_VALIDATION = PASS
PARSER_SMOKE = PASS
RUNTIME = NOT_CLAIMED

GAMEPLAY_FILES_CHANGED_BY_TECH6C3A = 8

COMMIT = NO
PUSH = NO

NEXT_PHASE = TECH6C3B_LEBLANC_AND_ALKALI_CHEMISTRY
NEXT_PHASE_READY = YES
```
