# CLEANUP-2D-3D — Mobilisation, conscription, milices et levées (1776)

## 1. Baseline Git

- `BRANCH = cleanup-post-release`
- `HEAD = f5e28c466e527ce33197ccd1a3f98e7f17ae62dd`
- `INDEX_STATE = CLEAN`
- `WORKTREE_STATE = DIRTY_PREEXISTING_PRESERVED`
- `GIT_INDEX_MUTATED_BY_CODEX = NO`

The pre-existing modified/untracked files recorded before 3D were preserved. No Git mutation command was run.

## 2. Inputs

The complete 2D-1, 2D-2, 3B and 3C research/report packets named in the task were used. The 210-row 2D-2 target CSV remains the historical/gameplay authority; the critical complement makes the native 1.13.9 ceiling the implementation authority. Canonical executable data came from `C:\Games\Victoria 3` (`1.13.9 (Matcha)`). No external historical research was performed.

## 3. Vanilla 1.13.9 conscription system

`V13_1_13_9_NATIVE_CONSCRIPTION_MODEL = scripted conscript combat units remain potential battalions; raising them creates/activates state conscription centers sized from workforce × state conscription rate, subject to the army-law per-state absolute cap.`

The canonical sources are `building_conscription_center`, `NBuildings.CONSCRIPTION_CENTER_LEVEL_POPULATION_DIVISOR = 1000`, `NMilitary.COMBAT_UNITS_PER_LEVEL = 1`, army-model law modifiers, technology modifiers, and the 1.13.9 game concepts. The state formula used here is:

`floor(workforce × army_law_rate × (1 + additive state_conscription_rate_mult modifiers) / 1000)`, capped by `state_building_conscription_center_max_level_add`.

## 4. Unraised conscript behavior

- `CONSCRIPT_UNIT_STARTS_UNRAISED = YES`
- `CONSCRIPT_UNIT_HAS_PEACETIME_MANPOWER_COST = NO`
- `CONSCRIPT_UNIT_HAS_PEACETIME_BUDGET_COST = NO`
- `PEACETIME_MOBILIZATION_BUDGET_RISK = LOW; CONFIRM_IN_3E`

The concepts define conscript battalions as temporary and maintained only when activated. They do not count against command limit before being raised.

## 5. Conscript / conscription-center relationship

- `CONSCRIPT_UNIT_MATERIALIZES_CONSCRIPTION_CENTER = WHEN_RAISED`
- `EXPLICIT_CONSCRIPTION_CENTERS_ADDED = 0`
- `BUILDING_HISTORY_CHANGED = 0`

The center appears when a state is conscripted and deactivates after war. The formation history reserves unit capacity; it does not add a permanent building.

## 6. Law constraints

The active law supplies both a rate and a per-state cap: Peasant Levies 4%/25, Warrior Caste 1%/10, Professional Army 1%/50, National Militia 5%/100, Mass Conscription 3%/100. Peasant Levies and Warrior Caste also restrict conscripts to the infantry combat-unit group. No law was changed.

`CONSCRIPTION_LIMIT_MODEL = workforce × law rate × additive technology/local modifier factor, floor to battalions, then per-state law cap`

## 7. Implementation method

`CONSCRIPT_UNIT_CAN_BE_ATTACHED_TO_EXISTING_FORMATION = YES`

All 1470 implemented battalions use `service_type = conscript` inside existing 3B armies. Recruitment states are directly owned. No reserve-only formation was necessary. `DIRECT_STATE_OWNERSHIP_REQUIRED = YES` for this safe history implementation. Subjects/companies retain and use their own state capacity.

## 8. Composition model

Base models were conservative: European/revolutionary/company reserves 90/5/5 infantry/cavalry/artillery; Qing 100/0/0; Ottoman 70/25/5; Maratha 55/40/5; Persian 60/35/5; Central Asian 60/35/5; African 75/20/5; South Asian 80/15/5; Southeast Asian 85/15/0; other 90/10/0. A non-infantry share was used only when the current law allowed it and an already materialized 3B unit proved the unit group/type available. Otherwise it was shifted to infantry and documented. Thus historically cavalry-heavy cases under Peasant Levies are explicitly law-constrained, not silently reinterpreted.

## 9. World totals

- `TOTAL_DESIRED_MOBILIZATION_2D2 = 2929`
- `TOTAL_NATIVE_CAPACITY_AVAILABLE = 2883`
- `TOTAL_IMPLEMENTED_NATIVE_OR_SAFE_MODIFIED = 1470`
- `TOTAL_SHORTFALL_LAW = 463`
- `TOTAL_SHORTFALL_TECH = 305`
- `TOTAL_SHORTFALL_POPULATION = 611`
- `TOTAL_SHORTFALL_STRUCTURAL = 80`
- `TOTAL_SHORTFALL_OTHER = 0`

| Cause | Battalions |
|---|---:|
| LAW | 463 |
| TECH | 305 |
| POPULATION | 611 |
| STRUCTURAL | 80 |
| OTHER | 0 |

Reconciliation: `1470 + 1459 = 2929`.

## 10. Great Britain

`GBR_REGULAR_UNITS = 49`; desired/native/implemented/shortfall = `60/29/29/31`. BIC territory was not used. East Indies naval arrangements were untouched.

## 11. France

`FRA_REGULAR_UNITS = 165`; desired/native/implemented/shortfall = `80/40/40/40`. The Professional Army rate and state-religion penalty explain the documented current-law deficit.

## 12. Spain

`SPA_REGULAR_UNITS = 95`; desired/native/implemented/shortfall = `70/65/65/5`. Structural colonial tags received no duplicate pool.

## 13. Habsburg system

`HABSBURG_MOBILIZATION_DOUBLE_COUNT = 0`. Structural HUN/GAL/TRS/BEO targets remain deferred; AUS alone receives its independently owned native capacity. No overlord/sub-tag capacity is counted twice.

## 14. Prussia

`PRU_REGULAR_UNITS = 158`; desired/native/implemented/shortfall = `60/14/14/46`. No naval data changed.

## 15. Russia

`RUS_REGULAR_UNITS = 215`; desired/native/implemented/shortfall = `120/183/120/0`. Only directly owned Russian region-states were allocated.

## 16. USA

`USA_REGULAR_UNITS = 20`; `USA_DESIRED_MOBILIZATION_CAPACITY = 80`; `USA_NATIVE_MAX_CONSCRIPTION_CAPACITY = 58`; `USA_IMPLEMENTED_MOBILIZATION = 58`; `USA_NATIVE_SHORTFALL = 22`. The militia layer is dormant and distinct from the Continental standing army.

## 17. Qing

`CHI_REGULAR_UNITS = 290`; desired/native/implemented/shortfall = `150/766/150/0`. The 150 target is a local surge representation, not the administrative establishment.

## 18. Ottoman Empire

`TUR_REGULAR_UNITS = 65`; desired/native/implemented/shortfall = `150/140/140/10`. Provincial capacity is allocated only in directly owned Ottoman states.

## 19. Maratha

`MARATH_REGULAR_UNITS = 45`; desired/native/implemented/shortfall = `100/65/65/35`. The research cavalry model is retained in the audit, but current Peasant Levies safely permits only infantry-group conscripts; no cavalry was forced through an incompatible law.

## 20. Persia / Durrani / Mysore

| Tag | Desired | Native | Implemented | Shortfall | Cause |
|---|---:|---:|---:|---:|---|
| PER | 60 | 38 | 38 | 22 | TECH |
| DUR | 120 | 63 | 63 | 57 | TECH |
| MYS | 55 | 6 | 6 | 49 | POPULATION |

Tribal/confederal qualitative evidence is not converted to standing forces. Law/engine shortfalls remain explicit.

## 21. BIC / DEI / HBC

Each company uses only its own directly owned states. `GBR_BIC_MOBILIZATION_DOUBLE_COUNT = 0`; `COMPANY_METROPOLITAN_DOUBLE_COUNT = 0`. BIC desired/native/implemented = `45/143/45`.

## 22. Other non-European systems

The allocation CSV records every implemented state, formation, unit mix and historical role. Conservative infantry dominates where 2D-1 is qualitative. No artillery reserve was invented without both research-model support and an already valid 3B artillery type.

## 23. Structural defer

All 34 structural-defer tags remain unchanged. Their desired total is `80` and their implemented total is `0`. `STRUCTURAL_DEFER_FAKE_MOBILIZATION_CREATED = 0`.

## 24. Decentralized nations

The 165 decentralized tags are outside the 210-row implementation target set and were not changed. The nine pre-existing native-conscription exceptions ABB/JBB/KBB/MBB/NBB/SD1/SKH/ULT/ZWY were not edited. `DECENTRALIZED_TAGS_CHANGED = 0`.

## 25. Law-, tech- and population-limited cases

The capacity audit attributes every country residual once and the country result gives the governing reason. No residual is hidden. Key cases:

| Tag | Desired | Native | Implemented | Shortfall | Cause |
|---|---:|---:|---:|---:|---|
| GBR | 60 | 29 | 29 | 31 | LAW |
| FRA | 80 | 40 | 40 | 40 | LAW |
| SPA | 70 | 65 | 65 | 5 | LAW |
| AUS | 70 | 39 | 39 | 31 | LAW |
| PRU | 60 | 14 | 14 | 46 | LAW |
| RUS | 120 | 183 | 120 | 0 | NONE |
| USA | 80 | 58 | 58 | 22 | TECH |
| CHI | 150 | 766 | 150 | 0 | NONE |
| TUR | 150 | 140 | 140 | 10 | LAW |
| MARATH | 100 | 65 | 65 | 35 | LAW |
| PER | 60 | 38 | 38 | 22 | TECH |
| DUR | 120 | 63 | 63 | 57 | TECH |
| MYS | 55 | 6 | 6 | 49 | POPULATION |
| BIC | 45 | 143 | 45 | 0 | NONE |
| DEI | 18 | 87 | 18 | 0 | NONE |
| HBC | 1 | 0 | 0 | 1 | LAW |
| OYO | 35 | 9 | 9 | 26 | POPULATION |

`MOBILIZATION_TARGET_EXCEEDS_CURRENT_LAW = YES` where `shortfall_reason=LAW`. No temporary modifier was applied; these cases remain for technology/law/map review.

## 26. Budget risk

Unraised conscripts have no standing manpower employment, military wage bill or military-goods input flow because their centers appear/activate only when raised. Mobilized affordability—especially GBR—must be measured in 3E. No money, tax, wage, goods or budget modifier was added.

## 27. Invariants

- `REGULAR_LAND_UNITS_BEFORE_3D = 2557`
- `REGULAR_LAND_UNITS_AFTER_3D = 2557`
- `NONDEFERRED_REGULAR_UNITS = 2431`
- `STRUCTURAL_DEFER_FROZEN_REGULAR_UNITS = 126`
- `REGULAR_UNIT_DELTA_3D = 0`
- `CONSCRIPT_OR_MOBILIZABLE_UNITS = 1470`
- `MILITIA_CONVERTED_TO_REGULAR = 0`
- `LEVIES_CONVERTED_TO_REGULAR = 0`
- `TRIBAL_CONTINGENTS_CONVERTED_TO_REGULAR = 0`
- `NO_CONSCRIPTION_UNIT_CREATED_ABOVE_ENGINE_NATIVE_OR_EXPLICIT_SAFE_CAPACITY = YES`
- `UNEXPLAINED_MOBILIZATION_SHORTFALL = 0`
- `HABSBURG_MOBILIZATION_DOUBLE_COUNT = 0`
- `GBR_BIC_MOBILIZATION_DOUBLE_COUNT = 0`
- `SPANISH_COLONIAL_MOBILIZATION_DOUBLE_COUNT = 0`
- `PORTUGUESE_COLONIAL_MOBILIZATION_DOUBLE_COUNT = 0`
- `COMPANY_METROPOLITAN_DOUBLE_COUNT = 0`

## 28. Files modified

Only existing land formation files containing allocations and the five 3D deliverables were changed/created. No building, country, define, map, state-region, ownership, diplomacy, technology, commander, portrait, DNA or naval formation data was changed. Formation files touched: `00_military_formations_europe.txt, 01_military_formations_north_america.txt, 03_military_formations_north_africa.txt, 04_military_formations_middle_east.txt, 05_military_formations_india.txt, 06_military_formations_asia.txt, 07_military_formations_subsaharan_africa.txt`.

- `DEFINES_CHANGED = 0`
- `REGULAR_FORMATION_COMPOSITION_CHANGED = 0`
- `NAVAL_FORMATIONS_CHANGED = 0`
- `BUILDING_HISTORY_CHANGED = 0`
- `NAVAL_ADMIN_LEVELS_CHANGED = 0`
- `EXPLICIT_BARRACK_LEVELS_CHANGED = 0`
- `COUNTRY_HISTORY_CHANGED = 0`
- `MAP_FILES_CHANGED = 0`
- `STATE_REGION_FILES_CHANGED = 0`
- `OWNERSHIP_FILES_CHANGED = 0`
- `DIPLOMACY_FILES_CHANGED = 0`
- `TECHNOLOGY_FILES_CHANGED = 0`
- `COMMANDER_CHARACTER_FILES_CHANGED = 0`
- `PORTRAIT_FILES_CHANGED = 0`
- `DNA_FILES_CHANGED = 0`
- `PROTECTED_TECH_FILES_CHANGED = 0`

The unrelated dirty files already present in the baseline worktree were preserved unchanged by 3D; the Git index remains clean.

## 29. Static validation

- `ALL_CONSCRIPT_UNIT_TYPES_EXIST_1_13_9 = YES`
- `ALL_CONSCRIPT_RECRUITMENT_STATES_VALID = YES`
- `ALL_CONSCRIPT_RECRUITMENT_STATES_DIRECTLY_OWNED = YES`
- `INCORPORATED_STATE_REQUIRED = NO` (unincorporated states remain eligible with the canonical -50% multiplier)
- `NEW_BROKEN_FORMATION_SCOPES = 0`
- `NEW_DUPLICATE_FORMATION_SCOPES = 0`
- `NEW_INVALID_HQ = 0`
- `NEW_INVALID_SERVICE_TYPE = 0`
- `NEW_INVALID_BUILDING_REFERENCE = 0`
- `DEFINES_CHANGED = 0`; `BUILDING_HISTORY_CHANGED = 0`; `COUNTRY_HISTORY_CHANGED = 0`; `TECHNOLOGY_FILES_CHANGED = 0`
- `NAVAL_FORMATIONS_CHANGED = 0`; `REGULAR_FORMATION_COMPOSITION_CHANGED = 0`
- `POPULATION_CHANGED_FOR_CONSCRIPTION = 0`; `LAW_CHANGED_FOR_CONSCRIPTION = 0`; `TECH_CHANGED_FOR_CONSCRIPTION = 0`
- `TEMPORARY_CONSCRIPTION_MODIFIERS = 0`
- `ALL_TEMPORARY_MODIFIERS_MARKED_FOR_TECH_REWORK_REVIEW = YES` (vacuous; register has zero data rows)
- `PROTECTED_TECH_FILES_CHANGED = 0` (the seven protected files remain untracked, unstaged and hash-identical)
- `BJECT_PATH_PRESENT = 0`
- `BIC_FRONTIER_COLONIZATION_PRESERVED = YES`; `BIC_COLONIAL_EXPLOITATION_PRESENT = NO`
- `GBR_EAST_INDIES_STATION_HQ_PRESERVED = region_south_india`
- `IDENTICAL_REAL_ARMADA_DUPLICATE = 0`; `PRU_COMBAT_NAVY = 0`
- `git diff --check = PASS`
- `CODEX_LAUNCHED_VICTORIA3 = NO`
- `CONFIDENCE = HIGH` for Gate A; `MEDIUM_HIGH_STATIC` for calculated start-state ceilings pending consolidated runtime confirmation.

## 30. Readiness for CLEANUP-2D-3E

`RUNTIME_BLOCKER = NO`. Static architecture and ceilings are demonstrated without permanent military employment or infrastructure edits. Recommended next phase: **CLEANUP-2D-3E — consolidated military/naval/mobilization runtime QA**, including raising/demobilizing conscripts, actual state center levels, command limits, GBR budget, save/load, and fresh logs. 3E was not started.
