# BUILD START 1776 — Steel base PM blocker

Date: 2026-09-17  
Game version: Victoria 3 1.13.11  
Result: **STEEL PREFLIGHT = BLOCKED — CASE B**

## 1. Stop condition

No appropriate traditional pre-coke production method currently exists for `building_steel_mill`.

The final implementation prompt explicitly forbids inventing a recipe silently. Consequently, no worldwide building redistribution, gate edit, starting-technology addition or history rewrite was performed.

## 2. Baseline before writing

- Effective manual building placements reconstructed directly from `common/history/buildings`: **2650**.
- Effective manual building levels: **6801**.
- Corrected matrix: **3913 rows / 3824 target levels / 2287 positive rows**.
- Matrix decisions: **1274 ADD / 1626 REMOVE / 140 INCREASE / 325 DECREASE / 503 KEEP / 45 PRESERVE_SERENISSIMA**.
- Administration target: **470**.
- Logging target: **235**.
- Protected military/naval baseline: **65 placements / 414 levels**.

Semantic baselines:

- VEN/GEN effective building hash: `c6e707d08c25efd9c1feb0aa70c24c8f51f963f22da565f0d5e4628a73032fcd`
- Protected military/naval effective building hash: `8ff3398fb8a6e464cdd14dfc60df53f8977c7a9d0e8030b7b0895711c9232eb8`

Protected breakdown:

| Building | Placements | Levels |
|---|---:|---:|
| `building_barrack` | 28 | 171 |
| `building_naval_administration` | 36 | 242 |
| `building_naval_fortification` | 1 | 1 |

The difference between the 2650 effective placements and the 2639-row current-building report is the already documented set of **11 orphan history entries**. They were not used to validate the target and were not deleted.

## 3. Current steel architecture

`building_steel_mill` currently:

- requires `coke_smelting` at building level;
- uses `pmg_steelmaking_process` as its base process group;
- therefore cannot represent a traditional ironworks before coke smelting.

`pmg_steelmaking_process` currently lists, in default order:

1. `pm_coke_blast_furnaces`
2. `pm_blister_steel_process`
3. `pm_bessemer_process`
4. `pm_thomas_process`
5. `pm_open_hearth_process`
6. `pm_electric_arc_process`

Because no method has `is_default = yes`, the first method is the effective default.

## 4. Available PM recipes and gates

| PM | Inputs per level | Outputs per level | Technology gate | Suitable as 1776 pre-coke base? |
|---|---|---|---|---|
| `pm_coke_blast_furnaces` | 35 iron, 35 coal | 55 steel | **none currently** | No — explicitly coke-based and intended to require `coke_smelting` |
| `pm_blister_steel_process` | 40 iron, 30 coal, 5 tools | 65 steel | `puddling_and_rolling` | No — later process |
| `pm_bessemer_process` | 60 iron, 30 coal | 90 steel | `bessemer_process` | No |
| `pm_thomas_process` | 65 iron, 25 coal, 10 limestone | 90 steel, 5 fertilizer | `bessemer_process` | No |
| `pm_open_hearth_process` | 90 iron, 30 coal | 120 steel | `open_hearth_process` | No |
| `pm_electric_arc_process` | 100 iron, 30 coal, 30 electricity | 150 steel | `electric_arc_process` | No |

`pm_pig_iron` is not a solution: it belongs to tooling workshops, consumes wood and iron, produces **tools rather than steel**, and requires `precision_boring`.

## 5. Additional defect confirmed

`pm_coke_blast_furnaces` currently has no `unlocking_technologies` block. The approved architecture requires it to be gated by `coke_smelting` after the building-level gate is moved.

## 6. Minimal proposal requiring approval

Create one explicit traditional PM, provisionally named:

`pm_charcoal_ironworks`

Proposed identity:

- first/default PM of `pmg_steelmaking_process`;
- texture: `gfx/error_deer.dds`;
- no post-1776 technology requirement;
- represents charcoal ironworks, bloomery/finery practice and other pre-coke merchant-iron production aggregated into the existing `steel` good;
- deliberately less productive than coke blast furnaces.

Minimal balance proposal per building level:

| Component | Proposed value |
|---|---:|
| Iron input | 25 |
| Wood input | 25 |
| Steel output | 35 |
| Shopkeepers | 500 |
| Laborers | 4500 |
| Pollution | 5 |

At base-price proportions this preserves a small operating margin comparable to, but below, the coke method. The values are a proposal only and were **not written**.

Required structural edits after approval:

1. Insert `pm_charcoal_ironworks` before `pm_coke_blast_furnaces` in `pmg_steelmaking_process`.
2. Change the building existence gate from `coke_smelting` to `organized_workshops`, as already specified by `MOVE_GATE_TO_PM` reconciliation.
3. Add `coke_smelting` to `pm_coke_blast_furnaces.unlocking_technologies`.
4. Add English and French localization for the new PM.
5. Rerun the steel preflight, gate reconciliation and static economic estimates before any world history rewrite.

## 7. Work deliberately not performed

- Gate groups applied: **0**.
- Starting technologies added: **0**.
- Building history redistributed: **0**.
- Infrastructure PMs changed: **0**.
- Deincorporation writes: **0**.
- Gameplay files modified by this task: **0**.

No commit. No push. No PR.

