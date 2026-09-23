# BUILD START 1776 — Pre-implementation audit

Date: 2026-09-17  
Authority: current local working tree, Victoria 3 1.13.11  
Phase status: **STOP — METHODOLOGY_STOP_BUILDING_TYPES > 0**

## 1. Result

The **664** gate conflicts are accounted for in `BUILD_START_1776_GATE_RECONCILIATION.csv`; no conflict row is missing and no unknown gate/building/PM identifier was found. However, Phase 1 gameplay implementation is forbidden because **5** complete building types fail the methodology guard or are explicitly protected by the user.

No gameplay file was modified. The historical target remains frozen; this audit does not rewrite regional research.

## 2. Gate reconciliation

| Decision | Conflict rows covered |
|---|---:|
| `CHANGE_BUILDING_GATE` | 31 |
| `KEEP_CURRENT_GATE` | 62 |
| `KEEP_GATE_ADD_TECH` | 179 |
| `MOVE_GATE_TO_PM` | 7 |
| `REMOVE_BUILDING_GATE` | 385 |

- Reconciled conflict rows: **664**.
- Unresolved gate conflict rows: **0**.
- Proposed building-gate change groups: **17**.
- Proposed PM-gate change groups: **1**.
- Candidate starting-tech grants, before prerequisite closure: **104** unique TAG/technology pairs.

These are proposals only. They were not written because the Phase 0 methodology condition failed.

## 3. Structural gate conclusions

- **Ports:** `building_port` must not require `enclosed_dock_systems`; its default PM is `pm_anchorage`. Remove the building gate and retain later dock improvements behind their PM technologies.
- **Traditional shipyards:** `building_shipyard` must not require `state_dockyard_systems`; its default PM is basic shipbuilding. `building_naval_administration` remains gated and protected.
- **Fishing and whaling:** simple coastal fishing/whaling predates `marine_chronometry`; remove the building gates, while later equipment stays gated.
- **Agriculture:** basic farms, ranches, vineyards and plantations must not require `improved_husbandry`; their advanced PMs already carry later technologies.
- **Traditional manufactures:** `traditional_food_processing`, `traditional_papermaking`, `organized_workshops` and `organized_textile_production` remain valid era-1 existence gates. Historically justified target countries would need explicit grants.
- **Universities:** replace `specialized_technical_academies` with the earlier `institutionalized_scientific_exchange` existence gate; specialized academy content remains later.
- **Construction:** keep `organized_financial_institutions`, respecting the prior tree decision; explicit target countries would require grants.
- **Mines:** retain `shaft_mining` for commercial mines; lower the gold-mine existence gate from `applied_mineralogy` to `shaft_mining`.
- **Steel:** move `coke_smelting` from the building to `pm_coke_blast_furnaces`, but first create/identify a traditional pre-coke base PM. This is a high-risk proposal and was not implemented.
- **Regional canals:** `industrial_canals` is correctly a PM gate. The ten historical canal rows justify targeted grants plus prerequisite closure; rail and passenger rail remain disabled.
- **Military gates:** remain unchanged because army, fleet and fortification setup is outside this redistribution.

## 4. Methodology stops

| Building type | Current levels | Matrix target | REMOVE rows | DECREASE rows | Stop reason |
|---|---:|---:|---:|---:|---|
| `building_government_administration` | 843 | 142 | 157 | 39 | Systematic research omission: 843→142 levels and 157 current rows removed; dedicated gameplay calibration required. |
| `building_logging_camp` | 458 | 75 | 148 | 21 | Critical-input omission: 458→75 levels and 148 current rows removed; wood supply must be recalibrated against the reduced economy. |
| `building_barrack` | 171 | 27 | 28 | 0 | User-protected: army sizing has already been calibrated for the period; do not redistribute or reduce. |
| `building_naval_administration` | 242 | 45 | 16 | 15 | User-protected: fleet sizing has already been calibrated for the period; do not redistribute or reduce. |
| `building_naval_fortification` | 1 | 40 | 1 | 0 | User-protected military infrastructure; do not replace the existing setup from an industry-centered matrix. |

### Administration

The matrix would reduce government administration from **843** to **142** levels, remove **157** current state placements and decrease another **39**. Major centralized states lose most regional capacity (notably China, France, Britain, Spain, the Ottoman Empire and Japan). This is consistent with an industry-focused omission, not a safe gameplay target. `building_government_administration` requires a dedicated gameplay calibration; no levels are invented here.

### Wood

The matrix would reduce logging from **458** to **75** levels, remove **148** current placements and decrease another **21**. It also removes all target logging from China and Japan and most of several major economies. Because wood feeds construction and early industry, this cannot be accepted merely as commercial-specialization cleanup. `building_logging_camp` requires a dedicated supply/demand calibration against the reduced building economy.

### Military

The army/navy matrix is incompatible with the explicit user constraint. For example, all **28** current barracks rows are removed and **19** different rows are added; naval administrations fall from **242** to **45**, while naval fortifications are almost entirely reseeded. These building types remain byte-semantically untouched.

## 5. Large-delta controls outside the stops

Strong reductions in commercial farms, plantations and fishing can be methodologically valid because the target represents specialized market production, not subsistence output. Industrial and mining reductions have positive regional research rows and may be applied only after the two critical input/state-capacity stops are resolved and the static economic sanity check is rerun. Regional infrastructure growth is governed separately by the exact 232-row PM plan.

## 6. Frozen-matrix validations

- Historical target: **2118 rows / 2924 levels**.
- Implementation matrix: **3969 rows / 3034 levels**, including **110** protected Serenissima levels.
- Infrastructure: **232 rows**, active rail violations **0**, passenger-rail violations **0**.
- Trade centers: **239 non-Serenissima rows / 366 levels**.
- Auto-generated target violations: **0**.
- Post-1776 target violations: **0**.
- Unknown IDs: **0**.
- Serenissima protected rows: **45**.
- Serenissima semantic baseline SHA-256: `6ea855d69a536d40c14f4e1f424f1db02525ec2ff7493ee5e24af960bbfa7e34`.

## 7. Candidate starting-tech changes (not applied)

The following **104** direct candidate grants come only from groups where the existing gate is retained. Replacement-gate cases and prerequisites must be recalculated before Phase 1.

- `ADR` → `shaft_mining`
- `AUS` → `organized_workshops`
- `AUS` → `shaft_mining`
- `BAD` → `organized_workshops`
- `BAV` → `traditional_food_processing`
- `BEO` → `industrial_canals`
- `BEO` → `organized_financial_institutions`
- `BEO` → `organized_workshops`
- `BEO` → `traditional_food_processing`
- `BEO` → `traditional_papermaking`
- `BRZ` → `traditional_food_processing`
- `BUK` → `organized_workshops`
- `BUK` → `traditional_food_processing`
- `BUK` → `traditional_papermaking`
- `CAUC` → `organized_textile_production`
- `CAUC` → `organized_workshops`
- `CHC` → `organized_workshops`
- `CHI` → `regulated_small_arms`
- `CHI` → `traditional_papermaking`
- `CON` → `traditional_food_processing`
- `CRI` → `traditional_food_processing`
- `DAI` → `traditional_papermaking`
- `DUR` → `organized_textile_production`
- `DUR` → `traditional_food_processing`
- `FRA` → `industrial_canals`
- `FRA` → `organized_financial_institutions`
- `FRA` → `organized_workshops`
- `FRA` → `traditional_papermaking`
- `GBR` → `industrial_canals`
- `GBR` → `organized_financial_institutions`
- `GBR` → `organized_workshops`
- `GBR` → `traditional_food_processing`
- `GBR` → `traditional_papermaking`
- `HAM` → `traditional_food_processing`
- `HDJ` → `traditional_food_processing`
- `IR1` → `traditional_food_processing`
- `IREK` → `organized_financial_institutions`
- `IREK` → `traditional_food_processing`
- `IREK` → `traditional_papermaking`
- `JAP` → `traditional_food_processing`
- `JAP` → `traditional_papermaking`
- `KBB` → `traditional_food_processing`
- `KOR` → `traditional_papermaking`
- `KZM` → `shaft_mining`
- `LAH` → `traditional_food_processing`
- `LBA` → `shaft_mining`
- `LND` → `shaft_mining`
- `MARATH` → `organized_workshops`
- `MARATH` → `regulated_small_arms`
- `MARATH` → `standardized_field_artillery`
- `MAS` → `traditional_food_processing`
- `MBB` → `traditional_food_processing`
- `MOR` → `organized_workshops`
- `MOR` → `traditional_food_processing`
- `MUG` → `regulated_small_arms`
- `MUG` → `standardized_field_artillery`
- `MYS` → `organized_workshops`
- `NET` → `industrial_canals`
- `NET` → `organized_financial_institutions`
- `NET` → `organized_workshops`
- `NET` → `traditional_food_processing`
- `NET` → `traditional_papermaking`
- `OMA` → `traditional_food_processing`
- `PAN` → `shaft_mining`
- `PAP` → `traditional_papermaking`
- `PER` → `organized_workshops`
- `PER` → `traditional_food_processing`
- `PLC` → `traditional_food_processing`
- `PLC` → `traditional_papermaking`
- `POR` → `organized_financial_institutions`
- `POR` → `organized_workshops`
- `POR` → `traditional_food_processing`
- `POR` → `traditional_papermaking`
- `QUE` → `traditional_food_processing`
- `RUS` → `industrial_canals`
- `RUS` → `traditional_food_processing`
- `RUS` → `traditional_papermaking`
- `SAX` → `organized_workshops`
- `SC1` → `organized_workshops`
- `SC1` → `traditional_food_processing`
- `SC1` → `traditional_papermaking`
- `SC2` → `traditional_food_processing`
- `SC3` → `traditional_food_processing`
- `SIA` → `regulated_small_arms`
- `SIA` → `standardized_field_artillery`
- `SIC` → `traditional_food_processing`
- `SPA` → `organized_financial_institutions`
- `SPA` → `organized_workshops`
- `SPA` → `traditional_food_processing`
- `SPA` → `traditional_papermaking`
- `SWE` → `traditional_papermaking`
- `SWI` → `traditional_papermaking`
- `TIB` → `organized_textile_production`
- `TRS` → `shaft_mining`
- `TUN` → `organized_textile_production`
- `TUN` → `traditional_food_processing`
- `TUR` → `organized_workshops`
- `TUR` → `traditional_food_processing`
- `USA` → `organized_workshops`
- `USA` → `shaft_mining`
- `USA` → `traditional_food_processing`
- `USA` → `traditional_papermaking`
- `WUR` → `organized_workshops`
- `ZAI` → `traditional_food_processing`

## 8. Passage condition

- `UNRESOLVED_GATE_CONFLICTS = 0`
- `METHODOLOGY_STOP_BUILDING_TYPES = 5`
- `UNKNOWN_IDS = 0`
- `SERENISSIMA_CHANGES = 0`

Result: **STOP**. The prompt forbids a partial worldwide redistribution while a complete category is methodologically doubtful. Resolve the administration and wood calibration and confirm the military-preservation overlay before rerunning this tool.

## 9. Phase summary

PHASE 0 GATE CONFLICTS = 664  
GATE CONFLICTS RESOLVED = 664  
UNRESOLVED GATE CONFLICTS = 0

BUILDING GATES CHANGED = 0 (proposed groups: 17)  
PM GATES CHANGED = 0 (proposed groups: 1)  
START TECH GRANTS ADDED = 0 (candidate direct pairs: 104)  
START TECH GRANTS REMOVED = 0

METHODOLOGY STOP BUILDING TYPES = 5

TARGET BUILDING ROWS = 2118  
TARGET BUILDING LEVELS = 2924

KEEP = 310  
ADD = 1330  
REMOVE = 1806  
INCREASE = 140  
DECREASE = 338  
PRESERVE_SERENISSIMA = 45

INFRASTRUCTURE ROWS = 232  
CANAL PM ACTIVE = 25  
ACTIVE RAIL PM = 0  
TRADE CENTER ROWS = 239  
TRADE CENTER LEVELS = 366

AUTO-GENERATED VIOLATIONS = 0  
POST-1776 VIOLATIONS = 0  
SERENISSIMA CHANGES = 0

UNKNOWN TECH = 0  
DIRECT PREREQUISITE DEBT = NOT RUN — NO TECH WRITES  
TRANSITIVE PREREQUISITE DEBT = NOT RUN — NO TECH WRITES

BUILD TARGET MATCH = NOT RUN — IMPLEMENTATION STOPPED  
BUILD TARGET MISMATCH = NOT RUN — IMPLEMENTATION STOPPED  
EXTRA BUILDINGS = NOT RUN — IMPLEMENTATION STOPPED

`git diff --check` = run separately after report generation.

NO COMMIT  
NO PUSH
