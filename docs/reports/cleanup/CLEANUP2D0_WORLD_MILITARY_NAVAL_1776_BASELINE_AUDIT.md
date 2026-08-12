# CLEANUP-2D-0 — World military and naval 1776 baseline audit

## 1. Repository baseline

```text
BRANCH = cleanup-post-release
HEAD = 58edae83b1c329c957772b2b6fabfa5baa1a6d17
INDEX_STATE = EMPTY
WORKTREE_STATE = DIRTY_PRESERVED
BASELINE_GIT_DIFF_CHECK = PASS
INSTALLED_TARGET = Victoria 3 1.13.9
```

Every pre-existing changed or untracked path was preserved:

```text
M docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md
?? docs/reports/cleanup/CLEANUP1D_MARATH_NAVAL_CREW_DIAGNOSTIC_AND_FIX.md
?? docs/reports/hotfix/_index/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv
?? docs/reports/hotfix/_index/army.md
?? docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
?? docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
?? docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

The seven technology files were read only for final hash verification, not used as military research sources.

## 2. Scope and exclusions

This is a static inventory of the fork's active 1776 military buildings, formations, units, ships and commander presence. It covers the 62 European plus 148 non-European centralized territorial countries from the completed active-country audits: **210 countries**. The 165 decentralized tags are excluded from quantitative rows. No decentralized tag owns an active army/fleet formation; 9 decentralized tags with explicit native-conscription effects are recorded separately as `INFO` exceptions.

No historical force research, rebalance, gameplay edit, commander creation, map change, localization change, or runtime test was performed.

## 3. Exact V3 1.13 military abstraction

The installed executable is 1.13.9. Target building, combat-unit, ship and production-method definitions remain effective because the fork has no corresponding definition directories. The exception is `common/defines/00_defines.txt`: the fork shadows the target file with an older full copy.

The exact target model is:

- a land combat unit has `max_manpower = 1000` for every unit type actually used by the fork;
- active fork `COMBAT_UNITS_PER_LEVEL = 1`, matching target 1.13.9;
- a naval-administration level employs 900 soldier/sailor-category workers and 100 officers and grants up to 1,000 sailors at full employment;
- ships consume type-specific crew, not one generic naval unit slot;
- one V3 unit/ship therefore represents game combat capacity, not necessarily one historical regiment or hull.

The active stale defines override omits 76 target `NMilitary` keys, notably the two sailor constants, and still names obsolete `building_naval_base`. This is queued P0; it was not repaired.

## 4. Barracks/unit manpower relationship

`NMilitary.COMBAT_UNITS_PER_LEVEL = 1` proves one barracks or conscription-center level supports exactly one combat unit. Each used land unit has 1,000 maximum manpower. The default `pm_no_organization` ratio is 97% soldiers / 3% officers; unlocked training PMs change that split and training rate, not the 1,000-person unit ceiling.

Country CSV `barracks_levels` is the literal building-history total. Because formation history independently creates units with a recruiting state, each row's notes also record the state-by-state unit-required capacity floor. This separates literal files from engine-required association without double-counting uncertain initialization behavior.

```text
TOTAL_EXPLICIT_BARRACK_LEVELS = 894
TOTAL_FORMATION_REQUIRED_LAND_LEVELS = 2948
TOTAL_STATEWISE_LAND_CAPACITY_FLOOR = 3842
TOTAL_EXPLICIT_CONSCRIPTION_CENTER_LEVELS = 0
```

Standing formations are kept separate from mobilization. No centralized starting formation uses `service_type = conscript`; the only explicit native-conscription effects found belong to the decentralized exception queue.

## 5. Naval-base/naval-unit manpower relationship

Target `building_naval_administration` replaces the old naval-base building. Its only base PM provides 1,000 total military employees and up to 1,000 sailors per fully staffed level. Target defines specify 100 sailors per assignment slot and 1,000 sailors per building level. A fleet is supported when the sum of ship crew requirements fits the national sailor ceiling; there is no exact one-level/one-ship rule.

```text
TOTAL_EXPLICIT_NAVAL_ADMINISTRATION_LEVELS = 159
TARGET_SAILOR_CAPACITY_AT_FULL_EMPLOYMENT = 159000
TOTAL_INITIAL_NAVAL_CREW_REQUIREMENT = 369300
COUNTRIES_WITH_NAVAL_CAPACITY_SHORTFALL = 17
```

The sailor ceiling is a theoretical full-employment maximum. Actual employment can make effective capacity lower.

## 6. Exact frigate manpower

`ship_type_frigate` has `ship_crew_max_add = 500`. One fully staffed naval-administration level can therefore cover two frigate units, absent other ships.

## 7. Exact ship-of-the-line manpower

`ship_type_ship_of_the_line` has `ship_crew_max_add = 800`. One level covers 1.25 such units mathematically; mixed fleets must be calculated by summed crew and integer ship units.

## 8. All other relevant 1776 unit types

| Game ID | Units | Personnel/unit | Personnel equivalent |
|---|---|---|---|
| combat_unit_type_cannon_artillery | 199 | 1000 | 199000 |
| combat_unit_type_cuirassiers | 74 | 1000 | 74000 |
| combat_unit_type_dragoons | 108 | 1000 | 108000 |
| combat_unit_type_hussars | 277 | 1000 | 277000 |
| combat_unit_type_irregular_infantry | 1009 | 1000 | 1009000 |
| combat_unit_type_lancers | 124 | 1000 | 124000 |
| combat_unit_type_line_infantry | 1154 | 1000 | 1154000 |
| combat_unit_type_low_tier_marines | 1 | 1000 | 1000 |
| combat_unit_type_mobile_artillery | 2 | 1000 | 2000 |
| ship_type_frigate | 377 | 500 | 188500 |
| ship_type_ship_of_the_line | 226 | 800 | 180800 |

All active references resolve in target 1.13.9. No pre-Great-Wave land or ship unit ID is active.

## 9. Global land baseline

```text
CENTRALIZED_COUNTRIES_AUDITED = 210
COUNTRIES_WITH_STANDING_ARMIES = 88
TOTAL_INITIAL_LAND_FORMATIONS = 148
TOTAL_INITIAL_LAND_UNITS = 2948
TOTAL_INITIAL_LAND_MANPOWER_EQUIVALENT = 2948000
GENERALS_CREATED_IN_FORMATION_HISTORY = 49
```

Largest current scripted land establishments (descriptive only, not historical approval):

| Tag | Country | Armies | Units | Personnel equivalent |
|---|---|---|---|---|
| CHI | China | 16 | 485 | 485000 |
| FRA | France | 4 | 187 | 187000 |
| RUS | Russia | 7 | 176 | 176000 |
| USA | America | 3 | 164 | 164000 |
| AUS | Austria | 4 | 152 | 152000 |
| PRU | Prussia | 4 | 122 | 122000 |
| GBR | Great Britain | 4 | 121 | 121000 |
| SPA | Spain | 3 | 102 | 102000 |
| PAN | Punjab | 3 | 86 | 86000 |
| PER | Persia | 2 | 85 | 85000 |
| BIC | East India | 1 | 80 | 80000 |
| TUR | Ottoman Empire | 4 | 78 | 78000 |

## 10. Global naval baseline

```text
COUNTRIES_WITH_NAVIES = 28
TOTAL_INITIAL_FLEETS = 49
TOTAL_INITIAL_NAVAL_UNITS = 603
TOTAL_FRIGATE_UNITS = 377
TOTAL_SHIP_OF_THE_LINE_UNITS = 226
TOTAL_INITIAL_NAVAL_MANPOWER_EQUIVALENT = 369300
ADMIRALS_CREATED_IN_FORMATION_HISTORY = 5
```

Largest current scripted naval crew requirements (descriptive only):

| Tag | Country | Fleets | Ship units | Crew requirement | Naval-admin levels |
|---|---|---|---|---|---|
| GBR | Great Britain | 10 | 196 | 123800 | 33 |
| RUS | Russia | 2 | 76 | 50900 | 0 |
| SPA | Spain | 2 | 80 | 46000 | 24 |
| FRA | France | 4 | 74 | 45100 | 24 |
| NET | Netherlands | 1 | 24 | 13800 | 13 |
| SWE | Sweden | 1 | 15 | 10500 | 10 |
| USA | America | 6 | 15 | 9300 | 0 |
| OMA | Oman | 1 | 15 | 9000 | 4 |
| DENNOR | Denmark-Norway | 1 | 14 | 8800 | 9 |
| CHI | China | 2 | 15 | 7500 | 0 |
| TUR | Ottoman Empire | 1 | 12 | 7200 | 9 |
| VEN | Venice | 1 | 10 | 6200 | 5 |

## 11. Spain / Real Armada diagnostic

Spain has 2 fleets, of which **2** use `Real_Armada_Espaola`. The two Real Armada entries are separate adjacent formation objects at lines 4037 and 4054 of the active fork Europe file. Each has southern-Europe HQ, 10 ship-of-the-line units and 30 frigates. They save to different scopes (`spanishnavy1`, `spanishnavy2`) and receive different separately created admirals. The same mod file shadows vanilla; this is not VFS coexistence or a single object instantiated twice.

```text
REAL_ARMADA_FORMATIONS = 2
REAL_ARMADA_DUPLICATE_ROOT_CAUSE = TWO_SEPARATE_ADJACENT_EXACT_DUPLICATE_CREATE_MILITARY_FORMATION_BLOCKS_IN_THE_ACTIVE_FORK_FILE
REAL_ARMADA_VERDICT = PURE_SCRIPT_DUPLICATE_UNLESS_2D1_PROVES_TWO_DISTINCT_HISTORICAL_SQUADRONS
```

No change was made.

## 12. Other duplicate/structural bugs

```text
DUPLICATE_ARMY_NAME_CASES = 0
DUPLICATE_FLEET_NAME_CASES = 1
EMPTY_ARMY_FORMATIONS = 0
EMPTY_FLEETS = 1
INVALID_LAND_UNIT_REFERENCES = 0
INVALID_NAVAL_UNIT_REFERENCES = 0
EXACT_DUPLICATE_FORMATION_SIGNATURES = 1
STRUCTURAL_BUG_QUEUE_ROWS = 34
P0_QUEUE_ROWS = 12
P1_QUEUE_ROWS = 13
INFO_QUEUE_ROWS = 9
```

Empty fleet(s): `PRU:Kniglich_Preuische_Marine@common/history/military_formations/00_military_formations_europe.txt:478`.

Commander validation also found one duplicated GBR commander scope (`colborne_gen`), a missing GBR transfer source (`aylmer_gen`), a missing BIC transfer source and target (`maitland_gen` -> `madras_army`), and BIC's invalid explicit ideology identifier `moderate`. The queue records each condition separately.

The remaining rows cover every national sailor-capacity shortfall and the 9 decentralized native-conscription exceptions. Commander absence itself is not treated as a bug because commander completeness belongs to a later phase.

## 13. VFS/effective-file findings

- Metadata replace paths cover only character, diplomatic-play and diplomacy history.
- All 9 fork military-formation filenames match target filenames, so each mod file shadows its vanilla counterpart; there is no formation-directory coexistence causing Real Armada.
- All 16 fork building-history filenames match target filenames and shadow them file by file.
- Target combat-unit, ship, building and production-method definitions remain effective because the fork has no corresponding definition directories.
- Fork `common/defines/00_defines.txt` shadows target 1.13.9 and is structurally stale: 101 versus 165 `NMilitary` keys, 76 missing target keys and 12 obsolete/renamed extras.
- No inactive or decentralized formation block exists in the effective fork formation files: all 197 physical active blocks belong to the 210 centralized countries.

## 14. Countries requiring special treatment in historical research

- **SPA**: distinguish one accidental duplicate from any evidence for historically distinct squadrons before naming or sizing fleets.
- **GBR commander scopes**: resolve duplicated `colborne_gen` and absent `aylmer_gen` before later commander reconstruction.
- **BIC formation history**: resolve invalid `moderate`, absent `maitland_gen`, and missing `madras_army` target scope without disturbing the completed company-executive architecture.
- **Naval-capacity shortfall tags (17)**: AUS, BEO, BRZ, CHI, FRA, GBR, HAN, NET, OMA, RUS, SAR, SC4, SIC, SPA, SWE, USA, VEN.
- **Empty fleet**: PRU:Kniglich_Preuische_Marine@common/history/military_formations/00_military_formations_europe.txt:478.
- **Decentralized conscription exceptions (9)**: ABB, JBB, KBB, MBB, NBB, SD1, SKH, ULT, ZWY; keep separate from centralized reconstruction.
- **Marine special case**: the single `combat_unit_type_low_tier_marines` unit remains valid but should not be silently counted as ordinary infantry in historical composition research.
- Countries with literal barracks but no standing formation represent capacity without a scripted standing force and must not be interpreted as historical army strength without 2D-1 evidence.

## 15. Uncertainty register

1. The engine's compiled fallback behavior for 1.13 sailor defines omitted by the active stale mod override is not statically observable; this is why the constants CSV distinguishes target value from effective uncertainty.
2. Formations without explicit `name` keys may receive generated/localized visible names; exact visible-name duplication cannot be proven statically for those entries.
3. Literal building-history barracks and formation-required levels are reported separately. The exact startup merge/materialization order is engine-internal, while the 1:1 support rule is explicit.
4. Naval capacity assumes full employment. Actual pop qualifications/employment can reduce sailors below the ceiling.
5. No runtime was launched; all commander attachments are based on explicit save-scope/transfer syntax only.

## 16. Files created

- `docs/research/military/CLEANUP2D0_V13_MILITARY_NAVAL_ENGINE_CONSTANTS.csv`
- `docs/research/military/CLEANUP2D0_WORLD_MILITARY_NAVAL_BASELINE_1776.csv`
- `docs/research/military/CLEANUP2D0_FORMATION_LEVEL_AUDIT_1776.csv`
- `docs/research/military/CLEANUP2D0_MILITARY_NAVAL_STRUCTURAL_BUG_QUEUE.csv`
- `docs/reports/cleanup/CLEANUP2D0_WORLD_MILITARY_NAVAL_1776_BASELINE_AUDIT.md`

No gameplay file was edited.

## 17. Protected-state verification

```text
GAMEPLAY_FILES_CHANGED = 0
MILITARY_FORMATION_FILES_CHANGED = 0
BUILDING_HISTORY_FILES_CHANGED = 0
COUNTRY_HISTORY_FILES_CHANGED = 0
MAP_FILES_CHANGED = 0
STATE_REGION_FILES_CHANGED = 0
DIPLOMACY_FILES_CHANGED = 0
TECHNOLOGY_FILES_CHANGED = 0
LOCALISATION_FILES_CHANGED = 0
PROTECTED_TECH_FILES_CHANGED = 0
CLEANUP2C_GAMEPLAY_CHANGED = 0
BJECT_PATH_PRESENT = 0
CODEX_LAUNCHED_VICTORIA3 = NO
GIT_INDEX_MUTATED_BY_CODEX = NO
git diff --check = PASS
```

Mandatory constants:

```text
V13_BARRACKS_EMPLOYMENT_PER_LEVEL = 1000 MAXIMUM MILITARY PERSONNEL PER SUPPORTED UNIT/LEVEL
V13_LAND_UNIT_MANPOWER = 1000 FOR EVERY LAND UNIT TYPE ACTIVE IN THE 1776 FORK
V13_NAVAL_BASE_EMPLOYMENT_PER_LEVEL = 1000 (900 SOLDIER/SAILOR CATEGORY + 100 OFFICERS)
V13_FRIGATE_MANPOWER = 500
V13_SHIP_OF_THE_LINE_MANPOWER = 800
```

The seven protected technology hashes remain the established CLEANUP-2C values. The index remained empty.

## 18. Recommended CLEANUP-2D-1 research scope

Research historical permanent forces and mobilization potential separately for all 210 centralized countries, prioritized by current strategic weight and structural risk. For navies, collect commissioned active hulls, ship classes, crew establishments, geographic squadrons and reserve/decommissioned status; convert only after evidence is assembled. For land forces, collect permanent personnel and composition separately from levy/militia potential. Begin with the first-rank naval powers (GBR, FRA, SPA), the stale-define/capacity-shortfall implications, and every P0/P1 queue entry. Preserve broad relative strategic hierarchy, but do not assign replacement numbers until the research matrix is complete.

STOP: CLEANUP-2D-1 was not started.
