# TECH-3B Vanilla Seam Reconnection Report

## Status

`TECH3B_VANILLA_SEAM_STATIC_PASS_RUNTIME_PENDING`

Runtime has not been executed. The user remains responsible for the in-game validation listed at the end of this report.

## Baseline and scope

- Working-tree baseline commit: `09204a4e45ed852b03f67fc46253caa67d1bede7`
- Branch: `technology-rework`
- Vanilla inventory/design reference: Victoria 3 `1.13.9`
- Canonical design references: `TECH_TREE_1700_1836_INTEGRATED_V1`, `TECH2H_HUMAN_FREEZE_REVIEW`, `TECH2H_VANILLA_SPLIT_UNLOCK_MATRIX`, `TECH_0_VANILLA_TECHNOLOGY_INVENTORY`, and `TECH3A_IMPLEMENTED_TECH_INDEX`
- Era I-VI implementation: 118 technologies, unchanged by TECH-3B
- Era VII definitions audited: 48

The implementation changes only prerequisite topology and research visibility in `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`. It does not modify technology effects, gameplay unlocks, costs, eras, icons, localization, descriptions, starting technologies, or Era I-VI definitions.

## Audit outcome

| Measure | Before | After |
|---|---:|---:|
| Era VII definitions audited | 48 | 48 |
| Researchable unintended Era VII roots | 4 | 0 |
| Consumed pre-1836 IDs found in Era VII | 38 | 38 compatibility aliases |
| Consumed IDs active in research progression | 38 | 0 |
| Active prerequisite edges targeting consumed IDs | 54 | 0 |
| Active prerequisite lists rewired | 0 | 19 |
| Retained researchable Era VII technologies | 10 candidates | 9 |
| Explicit nonresearchable root allowlist | 1 | 1 (`sericulture`) |

The four unintended researchable roots before correction were `navigation`, `rationalism`, `standing_army`, and `urbanization`. All are now nonresearchable compatibility aliases. `sericulture` remains a justified vanilla regional/event technology with its pre-existing `can_research = no`; it is not counted as an unintended root.

The 38 consumed IDs were not deleted because repository-wide history, events, journal entries, and AI content still reference several of them. Deleting their definitions without modifying those out-of-scope consumers would introduce compatibility failures. Instead, each consumed definition is retained under its original ID with `can_research = no`, while every active technology dependency is moved to its canonical TECH-3A owner. Their existing effects and unlock payloads are untouched. Runtime must confirm that Victoria 3's `Technology.ShouldShow` behavior removes these nonresearchable aliases from the visible tree.

## Classification summary

| Classification | Count | Result |
|---|---:|---|
| `CONSUMED_SPLIT` | 27 | Neutralized; active dependents rewired |
| `CONSUMED_REWIRE` | 4 | Neutralized; active dependents rewired |
| `CONSUMED_MERGE` | 4 | Neutralized; active dependents rewired |
| `CONSUMED_REPLACE` | 3 | Neutralized; active dependents rewired |
| `PRESERVED_POST1836_BRIDGE` | 9 | Retained and connected |
| `LEGITIMATE_ROOT` | 1 | `sericulture`, pre-existing nonresearchable allowlist |

The complete per-technology classification is recorded in `TECH3B_ERA_VI_VII_SEAM_AUDIT.csv`.

## Rewires implemented

| Active technology | Implemented prerequisites |
|---|---|
| `anarchism` | `early_socialism_cooperativism` |
| `bessemer_process` | `hot_blast_smelting` |
| `enlistment_offices` | `logistics`; `corps_organization` |
| `field_works` | `corps_organization` |
| `gantry_cranes` | `mechanized_naval_dockyards`; `iron_hull_construction` |
| `identification_documents` | `central_statistical_offices` |
| `investment_banks` | `stock_exchange`; `mutual_funds` |
| `ironclad_tech` | `iron_hull_construction` |
| `modern_nursing` | `medical_degrees` |
| `mutual_funds` | `institutionalized_public_credit`; `postal_savings` |
| `nationalism` | `periodical_print_networks`; `national_sovereignty` |
| `nitroglycerin` | `industrial_acids` |
| `philosophical_pragmatism` | `medical_degrees` |
| `romanticism` | `institutionalized_scientific_exchange` |
| `self_propelled_torpedoes` | `state_dockyard_systems` |
| `shift_work` | `interchangeable_manufacture` |
| `socialism` | `labor_movement`; `early_socialism_cooperativism` |
| `steel_frame_buildings` | `professional_civil_engineering` |
| `vacuum_canning` | `interchangeable_manufacture` |

## Mandatory cases

### Rationalism

`rationalism` is classified `CONSUMED_SPLIT`, not a preserved post-1836 bridge. It therefore received no invented Era VI prerequisite. It is now a nonresearchable compatibility alias.

The canonical split remains authoritative:

- the former `rationalism -> academia` responsibility belongs to `institutionalized_scientific_exchange`;
- the former `rationalism -> democracy` responsibility belongs to `constitutional_government`;
- the remaining educational and knowledge responsibilities stay distributed across `organized_elementary_schooling` and `codified_practical_knowledge` as documented by TECH2H.

No active technology depends on `rationalism`, `academia`, or `democracy` after the reconnection. The surviving mature branch is connected through the canonical owners; for example, `romanticism` now requires `institutionalized_scientific_exchange`.

### Urbanization, Urban Planning, and Modern Sewerage

`urbanization`, `urban_planning`, and `modern_sewerage` are all classified `CONSUMED_REWIRE`. They remain only as nonresearchable compatibility aliases because out-of-scope scripted content still references their IDs.

`professional_civil_engineering` remains the canonical owner of this former vanilla cluster. The active post-1836 dependency was moved from `steel_frame_buildings -> modern_sewerage` to `steel_frame_buildings -> professional_civil_engineering`. No new autonomous urbanization branch was created.

## Bridge validation

All required families pass or have a canonical no-direct-target justification. Detailed before/after paths are recorded in `TECH3B_VANILLA_BRIDGE_MATRIX.csv`.

- Optical Telegraph Networks -> Electric Telegraph: direct bridge retained.
- Iron Hull Construction -> Ironclad Technology: direct canonical bridge retained; consumed `screw_frigate` removed from the active path.
- Hydraulic Cements -> Reinforced Concrete: direct bridge retained.
- Hot Blast Smelting -> Bessemer Process: direct canonical bridge retained; consumed `steelworking` removed from the active path.
- Railways -> Steel Railway Cars -> later railway technologies: bridge retained.
- Percussion Cap -> Repeaters -> Bolt-Action Rifles: bridge retained.
- Early Socialism & Cooperativism -> Socialism / Anarchism: both mature branches now directly use the canonical Era VI owner.
- Geological Surveying: the current vanilla 1.13.9 compatibility inventory contains no distinct later specialized geology technology. `prospecting` is itself a consumed split alias, so no decorative or arbitrary direct link was introduced. This is a justified `PASS` with future specialized geology deferred.

## Static validation

| Validation | Result |
|---|---:|
| `BROKEN_PREREQUISITE_REFERENCES` | 0 |
| `PREREQUISITE_CYCLES` | 0 |
| `ERA_VII_UNINTENDED_ROOTS` | 0 |
| `CONSUMED_PRE1836_TECHS_VISIBLE_IN_ERA_VII` | 0 statically researchable; runtime visibility pending |
| `CONSUMED_TECHS_USED_AS_ACTIVE_PREREQUISITES` | 0 |
| `LATER_ERA_PREREQUISITE_INVERSIONS` | 0 |
| `DUPLICATE_TECH_IDS` | 0 |
| `TECH3A_ERA_I_VI_GAMEPLAY_CHANGES` | 0 |
| `LOCALIZATION_CHANGES` | 0 |
| `UNLOCK_CHANGES` | 0 |

Additional guards:

- all 276 technology definitions parse with a valid era and category;
- all 48 Era VII definitions were classified;
- all 38 consumed IDs have `can_research = no`;
- all nine retained active Era VII nodes have valid prerequisites;
- a normalized before/after comparison excluding only `can_research` and `unlocking_technologies` reports zero technology-body differences;
- the hashes of `10_tech3a_production.txt`, `20_tech3a_military.txt`, `25_tech3a_naval.txt`, and `30_tech3a_society.txt` are unchanged from the working-tree baseline;
- English and French localization hashes are unchanged from the working-tree baseline.

## Files changed by TECH-3B

- `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`
- `docs/reports/technology/TECH3B_ERA_VI_VII_SEAM_AUDIT.csv`
- `docs/reports/technology/TECH3B_VANILLA_BRIDGE_MATRIX.csv`
- `docs/reports/technology/TECH3B_VANILLA_SEAM_RECONNECTION_REPORT.md`

No localization, graphics, building, production-method, law, goods, history, starting-technology, or Era I-VI file was modified by this phase.

## Runtime checklist

- Confirm that all consumed compatibility aliases are absent from the visible technology tree.
- Confirm that `rationalism` is not visible as an autonomous technology.
- Confirm that `urbanization`, `urban_planning`, and `modern_sewerage` are not visible as redundant technologies.
- Confirm that no Era VII technology floats without a line from a valid predecessor.
- Inspect the visual continuity from Era VI into Era VII in Production, Military, Naval, and Society.
- Confirm that bridge lines are historically sensible and do not cross branches absurdly.
- Confirm that the tree has no visual cycles.
- Confirm normal progression from Era VII through Eras VIII-XII.
- Confirm that event/history-granted compatibility technologies still resolve without raw IDs or script errors.

Do not promote the status to runtime pass until these checks are completed in game.
