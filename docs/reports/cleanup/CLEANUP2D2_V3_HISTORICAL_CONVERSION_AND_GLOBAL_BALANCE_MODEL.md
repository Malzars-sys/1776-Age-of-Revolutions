# CLEANUP-2D-2 — V3 historical conversion and global balance model

## 1. Repository baseline

```text
BRANCH = cleanup-post-release
HEAD = e9481f4a51978f962e5e715fd9a1283564140595
INDEX_STATE = EMPTY
WORKTREE_STATE = DIRTY_PRESERVED
BASELINE_GIT_DIFF_CHECK = PASS
TARGET_MODEL = Victoria 3 1.13.9 / The Great Wave
```

Pre-existing paths were preserved:

```text
M  docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md
?? docs/reports/cleanup/CLEANUP1D_MARATH_NAVAL_CREW_DIAGNOSTIC_AND_FIX.md
?? docs/reports/hotfix/_index/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv
?? docs/reports/hotfix/_index/army.md
?? docs/research/technology/
```

The installed executable changed after the 2D-0 audit and is now 1.13.10. It was inspected only to identify this environment drift; no 1.13.10 value was substituted for a locked 1.13.9 engine constant. CLEANUP-2D-3 must use an authenticated, pinned 1.13.9 baseline for the defines repair.

## 2. Inputs

The eleven mandatory 2D-0 and 2D-1 inputs were read and reconciled. The 2D-1 land and naval masters remain the historical authority. No broad web research was repeated. The seven protected technology research files were not used.

The input coverage is:

```text
CENTRALIZED_TAGS = 210
LAND_QUANTITATIVE_HIGH = 8
LAND_QUANTITATIVE_MEDIUM = 1
LAND_QUANTITATIVE_LOW = 4
LAND_QUALITATIVE_ONLY = 163
LAND_STRUCTURAL_DEFER = 34
NAVAL_QUANTITATIVE_HIGH = 4
NAVAL_QUANTITATIVE_MEDIUM = 2
NAVAL_QUANTITATIVE_LOW = 2
NAVAL_QUALITATIVE_ONLY = 168
NAVAL_STRUCTURAL_DEFER = 34
```

## 3. Conversion methodology

The model applies five layers in order:

1. Establish whether the historical figure is a permanent/effective force, paper ceiling, administrative establishment, campaign concentration, or mobilization pool.
2. Remove or separately allocate garrisons, imperial deployments, company forces, provincial forces, militia, levies, and auxiliaries.
3. Apply the locked 1,000-person V3 unit scale only to the remaining standing representation.
4. Select composition from exact personnel, documented organizational units, a visible regional model, or a qualitative model.
5. Reconcile every standing target with barracks and every fleet target with crew and naval-administration capacity.

For the 163 land `QUALITATIVE_ONLY` rows, the reproducible fallback is visible in every CSV row: a standing-core center point equal to 90% of current scripted units in Europe, 75% outside Europe, or 40% of existing barracks where a country currently has capacity but no formation. Regional composition and non-standing mobilization multipliers are then applied separately. This is a balance model, not a claim that the resulting integer is a newly discovered historical headcount.

The regional mobilization multipliers are 0.5 times standing for ordinary European regular systems, 1.5 for South and East Asian systems, 2 for Southeast Asian, Middle Eastern, and American systems, and 3 for Central Asian, African, and Oceanian levy-heavy systems. Named special cases override this fallback.

## 4. Engine constants

```text
1 LAND UNIT = 1000 maximum personnel
1 BARRACKS LEVEL = capacity for 1 land unit
1 NAVAL ADMINISTRATION LEVEL = up to 1000 sailors at full employment
1 FRIGATE UNIT = 500 crew
1 SHIP-OF-THE-LINE UNIT = 800 crew
```

All proposed land categories use unit types already effective in the current technical baseline. No technology file or unlock was changed. Rows using modeled composition are marked `tech_dependent_review_later=YES`.

The implementation mapping is: European regular infantry to `combat_unit_type_line_infantry`; systems modeled as irregular/court/levy cores to `combat_unit_type_irregular_infantry` unless the existing technical baseline already supports their documented drilled component; cavalry shares to the already active cuirassier, dragoon, hussar, or lancer type appropriate to the current regional organization; and artillery shares to `combat_unit_type_cannon_artillery`. `combat_unit_type_mobile_artillery` and `combat_unit_type_low_tier_marines` require explicit row-level review rather than automatic preservation. No unavailable unit type is proposed.

## 5. Handling of uncertainty

Blank structural targets are deliberate. They mean that implementing an independent national force would be less accurate than waiting for a map, overlord, or polity decision. A numeric low-confidence target is always labeled as modeled; it is not presented as an exact historical fact.

The most consequential uncertainties are Russia's exact January fleet, the exact all-Presidency BIC total, Ottoman and Maratha permanent cores, most small-polity headcounts, and the location/quality mix of registered versus commissioned hulls. These do not invalidate the relative model, but they must remain review gates in implementation.

## 6. European regular-army conversion

Near-date permanent establishments use the 1,000-person scale after role and allocation review. France remains within its cautious 150,000–180,000 research range. Prussia uses 158 units from the near-date 158,000 establishment. Saxony uses 22 from 21,840; Hanover 21 from 21,000; Bavaria 8 from 8,000. Poland-Lithuania is set to 16, between the approximately 12,000 effective return and 24,000 paper ceiling.

Britain is the decisive counterexample to preserving current script scale: 121 units become 49 global Crown regular units. The North American deployment, West Indies, Mediterranean, Ireland, and India Crown detachments are allocations within those 49, not additional armies.

## 7. Non-European military-system conversion

Ottoman, Persian, Maratha, Central Asian, African, Arabian, Southeast Asian, and similar systems use a smaller permanent/core force plus a larger mobilization capacity. Their notes explicitly contain `MODELED_FROM_QUALITATIVE_EVIDENCE=YES` where applicable.

Key modeled recommendations are:

| Tag | Standing low–high | Recommended | Mobilizable capacity | Interpretation |
|---|---:|---:|---:|---|
| TUR | 55–75 | 65 | 150 | Central corps and garrison core; provincial forces mobilizable |
| MARATH | 35–55 | 45 | 100 | Confederal core; chiefly contingents mobilizable |
| PER | 25–40 | 32 | 60 | Zand standing core; tribal/provincial capacity separate |
| MYS | 25–40 | 32 | 55 | Haidar Ali centralizing core, not later Tipu totals |
| DUR | 35–55 | 45 | 120 | Durrani core plus tribal-confederal mobilization |
| OYO | 8–16 | 12 | 35 | Cavalry-heavy royal core |

## 8. Mobilization and conscription model

The target mobilization column is capacity, not starting battalions. Later implementation should use conscription centers, laws, events, subject contingents, or polity-specific mechanics. No militia, levy, tribal contingent, state militia, or short-term service total has been automatically turned into barracks.

The United States illustrates the separation: 20 standing Continental units plus modeled capacity for 80 state-militia/short-term units. The Ottoman recommendation is 65 standing plus 150 provincial/warrior capacity. Maratha is 45 plus 100 confederal/subject capacity.

## 9. Imperial allocation model

The allocation CSV establishes a single owner for every shared pool. Colonial deployment rows remain parent-tag formations unless a future reviewed transfer subtracts the same units from the parent.

```text
HABSBURG_REPRESENTED_POOL = 200
AUS_ALLOCATION = 140
HUN_ALLOCATION = 28
BEO_ALLOCATION = 12
GAL_ALLOCATION = 12
TRS_ALLOCATION = 8
TOTAL_ALLOCATED = 200
UNALLOCATED_FROM_220K_PARENT_AS_ABSTRACTED_ADMIN_GARRISON_SUPPORT = 20
```

British Crown land allocations sum to 49. BIC's 55 Company units are separate, and eight India Crown units remain inside GBR's 49. Spanish colonial garrisons sum inside the 95-unit Spanish Crown model and are represented geographically under SPA rather than duplicated as independent colonial armies. Portugal likewise has a 24-unit global Crown target: 20 metropolitan and four Brazil-theatre units, all represented once under POR.

## 10. Company-force model

BIC receives a low-confidence 45–65 range, recommended 55: Bengal 30, Madras 16, Bombay 9. Company Europeans, sepoys, and Company artillery are included. British Crown regiments are excluded.

DEI receives 12 company-garrison units and two frigate-equivalent patrol/escort units. VOC merchant hulls and the Netherlands state navy are excluded. HBC receives one corporate/local-security land unit and no combat fleet.

## 11. Global land targets

| Tag | Current | Low | High | Recommended | Infantry | Cavalry | Artillery | Mobilizable | Confidence |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| GBR | 121 | 48 | 50 | 49 | 42 | 5 | 2 | 60 | HIGH |
| FRA | 187 | 150 | 180 | 165 | 138 | 19 | 8 | 80 | MEDIUM |
| SPA | 102 | 85 | 105 | 95 | 73 | 14 | 8 | 70 | LOW |
| AUS | 152 | 130 | 150 | 140 | 105 | 20 | 15 | 70 | HIGH |
| PRU | 122 | 150 | 160 | 158 | 116 | 30 | 12 | 60 | HIGH |
| RUS | 176 | 190 | 240 | 215 | 155 | 42 | 18 | 120 | LOW |
| TUR | 78 | 55 | 75 | 65 | 43 | 17 | 5 | 150 | LOW |
| CHI | 485 | 260 | 320 | 290 | 230 | 60 | 0 | 150 | HIGH |
| USA | 164 | 18 | 21 | 20 | 17 | 2 | 1 | 80 | HIGH |
| BIC | 80 | 45 | 65 | 55 | 42 | 8 | 5 | 45 | LOW |
| MARATH | 59 | 35 | 55 | 45 | 27 | 15 | 3 | 100 | LOW |
| MYS | 7 | 25 | 40 | 32 | 22 | 6 | 4 | 55 | LOW |

The complete 210-row disposition is in the land target CSV. Target barracks equal recommended standing units under the locked 1:1 rule.

## 12. Global naval conversion methodology

Hull-based and crew-based calculations are reported separately where evidence permits. Registered inventory is never treated as commissioned capacity. The reconciliation then applies readiness/quality, geographic station needs, and V3 combat abstraction.

For each non-deferred fleet:

```text
TARGET_CREW = frigates × 500 + ships_of_the_line × 800 + other crew
TARGET_NAVAL_ADMIN = ceil(TARGET_CREW / 1000)
```

National ceilings are rounded separately, so the 239-level world requirement is correctly nine levels above the simple global crew/1,000 quotient.

## 13. Britain

The approximately 270 registered warships are an inventory constraint, while 82 SOL at sea or in condition by June is the readiness anchor. The target is 42 frigate-equivalents and 78 SOL-equivalents, 120 units and 83,400 crew. This applies a 0.90–1.00 readiness range to the SOL anchor and does not activate all registered hulls.

Seven distinct commands preserve global distribution: Channel Fleet, Western Approaches Fleet, Mediterranean Station, North America and West Indies Station, East Indies Station, Cape and South Atlantic Station, and Home Reserve and Coastal Station. Britain remains the unique global first-rank navy.

## 14. France

France starts with 18 frigates and 23 SOL, 41 units and 27,400 crew. The exact 1 January 1776 23-SOL condition figure is preserved. Brest, Toulon, and Rochefort/overseas commands replace the current wartime-heavy 74-unit arrangement. No 1778–83 expansion is imported into the start.

## 15. Spain / Real Armada

Spain starts with 18 frigates and 22 SOL, 40 units and 26,600 crew. The model reconciles 17 SOL fully commissioned in March 1776 with 28 in armament and 59 in the near-date inventory.

The two identical `Real_Armada_Espaola` blocks do not survive. They are replaced by three distinct commands:

- Escuadra de Cádiz: 7 frigates, 10 SOL; Atlantic/Cádiz-Ferrol role.
- Escuadra de Cartagena: 4 frigates, 6 SOL; Mediterranean role.
- Escuadra de América: 7 frigates, 6 SOL; Havana, South Atlantic, and Pacific imperial role.

The formation plan contains an explicit zero-unit `REMOVE` tombstone for the duplicate block.

## 16. Russia

Russia's land establishment range of 300,000–350,000 is converted with a 0.62–0.70 standing field-representation factor, producing 190–240 units and a recommended 215. The discount covers garrison/frontier dispersion and the post-1774 transition.

The navy remains low confidence: 14 frigates and 18 SOL, 32 units and 21,400 crew. A 25-unit Baltic Fleet and seven-unit Archipelago-return squadron preserve meaningful regional power while remaining below Atlantic first-rank navies.

## 17. Netherlands

The Netherlands receives 8 frigates and 6 SOL, 14 units and 8,800 crew. This is a real but reduced peacetime fleet, split between Amsterdam/North Sea and convoy/Mediterranean roles. It does not use the Republic's approximately 60,000-person national maritime labour pool as active payroll.

## 18. Sweden

The 22 nominal SOL in 1772, including six obsolete ships, yield 16 recommended SOL plus six frigates. The 22-unit, 15,800-crew target preserves a significant Baltic navy while applying a 16/22 quality/readiness factor. A line fleet and an archipelago/coastal command are distinct.

## 19. Denmark-Norway

Denmark-Norway retains a 14-unit mix: eight frigates and six SOL, requiring 8,800 crew and nine naval-administration levels. The approximately 40,000-person maritime labour pool is not converted into active naval payroll.

## 20. Portugal

Portugal receives eight frigates and four SOL, 12 units and 7,200 crew. Lisbon and the documented South Atlantic/Santa Catarina presence are represented as distinct squadrons. Brazil does not receive a duplicate national fleet.

## 21. USA

The Continental Navy receives five frigate-equivalent units, no SOL, 2,500 crew, and three naval-administration levels. The 3,090 annual personnel figure permits at most 6.18 frigate-only crew equivalents; the recommendation leaves a readiness/shore margin. The thirteen authorized frigates, state navies, and privateers are excluded from the standing January fleet.

```text
TARGET_USA_SHIP_OF_THE_LINE_UNITS_AT_START = 0
```

## 22. Qing

```text
QING_ADMINISTRATIVE_ESTABLISHMENT = approximately 800000
QING_BANNER_ESTABLISHMENT = approximately 200000
QING_GREEN_STANDARD_ESTABLISHMENT = approximately 600000
QING_V3_STANDING_REPRESENTATION_FACTOR = 0.325-0.400; recommended 0.3625
QING_TARGET_FIELD_CAPACITY = 260-320; recommended 290
QING_GARRISON_ABSTRACTION = approximately 510000 personnel outside field units at recommendation
QING_MOBILIZATION_ABSTRACTION = 150 units of surge/local capacity, not standing barracks
```

The target divides into four Banner commands and four consolidated Green Standard commands. Composition is 230 irregular-infantry equivalents and 60 cavalry equivalents. The current 485 standing units fall to 290; the 800,000 administrative establishment is not converted one-for-one.

## 23. Austria / Habsburg allocation

The 220,000 parent establishment produces a 200-unit represented pool. The allocation is AUS 140, HUN 28, BEO 12, GAL 12, and TRS 8. The 20-unit difference is administrative/garrison/support abstraction, not a hidden sixth allocation. Recommended allocations sum exactly to 200, so Habsburg double count is zero.

## 24. Prussia and empty fleet

Prussia rises from 122 to 158 land units, matching the near-date establishment anchor. Its naval target is zero frigates, zero SOL, zero combat fleets, zero crew, and zero naval administration. `Kniglich_Preuische_Marine` is explicitly marked `REMOVE`; it is not populated.

## 25. BIC / DEI / HBC

BIC is split into Bengal 30, Madras 16, and Bombay 9. Eight British India Crown units remain in GBR and are excluded from BIC. DEI receives company garrison and patrol abstractions only. HBC receives local corporate security only and no blue-water fleet.

## 26. Structural-defer countries

All 34 structural-defer tags have one of the required dispositions: `ALLOCATE_FROM_OVERLORD_POOL`, `LOCAL_GARRISON_ONLY`, `LOCAL_MILITIA_ONLY`, `COMPANY_FORCE`, `NO_INDEPENDENT_1776_FORCE`, or `MAP_REWORK_DEFERRED`. Habsburg component tags receive explicit parent-pool land allocations. Other map-dependent independent-force numbers are blank or zero, not invented.

No structural-defer tag is forced to possess a fake national army or fleet. Existing formations attached to unresolved tags are marked `STRUCTURAL_DEFER` in the formation plan, except clearly unsupported BEO naval capacity, which is marked for removal within the Habsburg allocation.

## 27. Stale defines repair plan

The active `common/defines/00_defines.txt` is the untouched initial-import full-file copy. Git history shows no later intentional edits to it. The 2D-0 1.13.9 comparison found 101 fork `NMilitary` keys versus 165 target keys, 76 missing target keys, and 12 obsolete extras. It also found the obsolete `NAVAL_BASE_BUILDING = "building_naval_base"` reference instead of target naval administration.

CLEANUP-2D-3A must proceed in this exact order:

1. Obtain and hash an authenticated 1.13.9 `00_defines.txt`; do not use the now-installed 1.13.10 file as the target.
2. Produce a section/key/value manifest for the imported fork file against that pinned target.
3. Classify only scenario deltas as candidates: `START_DATE`, `END_DATE`, and custom-map extents/water level. Verify each against map/runtime needs.
4. Replace the full-file shadow with a late-loading minimal scenario-delta define file if the define loader supports additive files; otherwise generate a 1.13.9 full baseline with only the audited deltas applied.
5. Inherit target `NMilitary` wholesale. Restore all 76 missing 1.13.9 keys, including both sailor constants. Remove all 12 obsolete extras.
6. Replace the obsolete naval-base building key with the target naval-administration key. Do not carry the inherited blockade-strength, no-commander-limit, or supply-shortage deviations without a separate documented design decision.
7. Run parser, start/load, sailor-capacity, fleet-order, blockade, formation-order, and save/load tests before implementing any numeric rebalance.

This direction is safer than copying either the stale file or the current 1.13.10 file wholesale.

## 28. All 2D-0 P0/P1 issue dispositions

All 34 queue rows are copied into the structural-fix plan with a resolution phase and proposed direction. The disposition totals are:

```text
2D0_ROWS_CONSUMED = 34
ADDITIONAL_2D2_ROWS = 3
STRUCTURAL_FIX_PLAN_ROWS = 37
```

The Real Armada and Prussian empty fleet go to `CLEANUP-2D-3B_FORMATIONS`; stale defines to `CLEANUP-2D-3A_ENGINE_BASELINE`; sailor-capacity rows to `CLEANUP-2D-3C_INFRASTRUCTURE`; commander scope, transfer, and ideology rows to `CLEANUP-2D-4_COMMANDERS`; decentralized exceptions remain in a future decentralized/map-military phase.

## 29. Global before/after comparison

```text
CURRENT_WORLD_LAND_UNITS = 2948
TARGET_WORLD_LAND_UNITS_LOW = 2005
TARGET_WORLD_LAND_UNITS_HIGH = 2876
TARGET_WORLD_LAND_UNITS_RECOMMENDED = 2431

CURRENT_WORLD_NAVAL_UNITS = 603
CURRENT_WORLD_NAVAL_CREW = 369300
TARGET_WORLD_FRIGATES = 174
TARGET_WORLD_SHIPS_OF_THE_LINE = 178
TARGET_WORLD_OTHER_SHIPS = 0
TARGET_WORLD_NAVAL_UNITS = 352
TARGET_WORLD_NAVAL_CREW = 229400

CURRENT_EXPLICIT_BARRACKS_LEVELS = 894
TARGET_REQUIRED_BARRACKS_LEVELS = 2431
CURRENT_NAVAL_ADMIN_LEVELS = 159
TARGET_REQUIRED_NAVAL_ADMIN_LEVELS = 239

COUNTRIES_LAND_REDUCED = 48
COUNTRIES_LAND_INCREASED = 91
COUNTRIES_LAND_UNCHANGED = 37
COUNTRIES_LAND_STRUCTURAL_DEFER = 34

COUNTRIES_NAVY_REDUCED = 13
COUNTRIES_NAVY_INCREASED = 3
COUNTRIES_NAVY_UNCHANGED = 160
COUNTRIES_NAVY_STRUCTURAL_DEFER = 34
```

The balance sanity checks pass: USA's 20 standing units are far below France's 165; Prussia has no navy; Britain has 120 combat units and an 83,400 crew requirement versus the next first-rank starts at 41/27,400 (France) and 40/26,600 (Spain); Qing fields 290 rather than 800; and the Habsburg allocations sum to one parent-derived pool.

## 30. Uncertainty register

1. Low-evidence country targets are balance-model values, not exact historical discoveries.
2. Russia requires ship-list reconstruction if implementation review challenges the 32-unit regional model.
3. BIC Presidency values should be revisited only with same-scope 1775–77 returns; linear interpolation remains forbidden.
4. Ottoman, Persian, Maratha, Central Asian, African, and Arabian mobilization values require polity-appropriate mechanics.
5. Naval crew capacity assumes full employment; state placement and qualifications remain runtime risks.
6. Thirty structural-defer tags retain blank independent land targets; map/overlord decisions precede force creation.
7. The local install is now 1.13.10; defines implementation must pin 1.13.9 explicitly.
8. Commander candidates were not invented where the packet supplied none.

## 31. Implementation sequencing recommendation

Begin with **CLEANUP-2D-3**, decomposed as follows:

1. `CLEANUP-2D-3A_ENGINE_BASELINE`: pin 1.13.9, repair/minimize stale defines, and runtime-test the military/naval engine baseline.
2. `CLEANUP-2D-3B_FORMATIONS`: implement reviewed land/fleet targets, Habsburg and imperial ownership, BIC Presidency armies, Spanish squadrons, Qing consolidation, USA reduction, and PRU fleet removal. Do not touch buildings yet.
3. `CLEANUP-2D-3C_INFRASTRUCTURE`: make barracks equal standing units and naval administration equal or exceed each national crew ceiling; place buildings by recruiting/base evidence.
4. `CLEANUP-2D-3D_MOBILIZATION`: implement conscription/event/subject capacity separately from standing barracks.
5. `CLEANUP-2D-3E_RUNTIME_QA`: verify all 210 dispositions, formation ownership, capacity, recruitment, fleet deployment, and save/load.
6. `CLEANUP-2D-4_COMMANDERS`: only after scopes stabilize, give every army at least one general and every fleet at least one admiral.

## 32. Readiness for CLEANUP-2D-3

```text
ALL_210_TAGS_ACCOUNTED = YES
USA_STARTING_SOL = 0
PRU_STARTING_COMBAT_NAVY = 0
IDENTICAL_REAL_ARMADA_DUPLICATE_PRESERVED = NO
MULTIPLE_SPANISH_SQUADRONS_ALLOWED_IF_DISTINCT = YES
GBR_UNIQUE_GLOBAL_NAVAL_FIRST_RANK = YES
FRA_STARTING_NAVY_NOT_1778_WARTIME_PEAK = YES
HABSBURG_FORCE_DOUBLE_COUNT = 0
BIC_CROWN_FORCE_DOUBLE_COUNT = 0
COLONIAL_FORCE_DOUBLE_COUNT = 0
QING_800K_ADMIN_ESTABLISHMENT_CONVERTED_1_TO_1 = NO
MILITIA_AUTOMATICALLY_CONVERTED_TO_STANDING = NO
STRUCTURAL_DEFER_TAGS_FORCED_TO_FAKE_NATIONAL_FORCE = 0
TARGET_NAVAL_ADMIN_CAPACITY_SHORTFALLS = 0

GAMEPLAY_FILES_CHANGED = 0
MILITARY_FORMATION_FILES_CHANGED = 0
BUILDING_HISTORY_FILES_CHANGED = 0
COUNTRY_HISTORY_FILES_CHANGED = 0
DEFINES_FILES_CHANGED = 0
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

The design phase is complete. Do not begin implementation automatically.
