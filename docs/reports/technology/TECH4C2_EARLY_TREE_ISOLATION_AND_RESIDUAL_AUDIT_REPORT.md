# TECH-4C2 — Early Tree Category Isolation and Residual Audit

## Scope and authority

- Branch: `tech4c2-audit-snapshot`
- Absolute baseline: `27cb446646d1f8906764aed5a59bbe21b2a04b55`
- Baseline conditions verified before work: matching branch and HEAD; clean working tree.
- Authority order used: TECH2H frozen architecture → TECH1A vanilla responsibility audit → TECH3A implemented index → effective runtime graph.
- Part A is a mechanical prerequisite edit. Part B is documentary audit only.
- No commit or push was performed.

## PART A — EXECUTED FIX

### Exact implementation

Only `unlocking_technologies` was changed for the following 14 targets:

`precision_boring`, `permanent_military_hospitals`, `armament_standardization_inspection`, `rifling`, `logistics`, `military_veterinary_services`, `state_dockyard_systems`, `paddle_steamer`, `mechanized_naval_dockyards`, `modern_lighthouse_optics`, `iron_hull_construction`, `systematic_cadastral_surveying`, `mechanized_printing`, and `active_principle_pharmacy`.

The exact before/after lists are recorded in [TECH4C2_EXACT_EARLY_TREE_ISOLATION_CHANGE_LOG.csv](TECH4C2_EXACT_EARLY_TREE_ISOLATION_CHANGE_LOG.csv).

| Counter | Expected | Actual |
|---|---:|---:|
| `CROSS_TREE_EDGES_REMOVED` | 18 | 18 |
| `SAME_TREE_EDGES_ADDED` | 7 | 7 |
| `PREREQUISITE_LISTS_CHANGED` | 14 | 14 |
| `NET_EDGE_CHANGE` | -11 | -11 |
| Cross-category edges before | 18 | 18 |
| `ACTIVE_CROSS_CATEGORY_EDGES_I_XII` after | 0 | 0 |
| `PRODUCTION_TARGET_WITH_NON_PRODUCTION_PREREQ` | 0 | 0 |
| `MILITARY_TARGET_WITH_NON_MILITARY_PREREQ` | 0 | 0 |
| `SOCIETY_TARGET_WITH_NON_SOCIETY_PREREQ` | 0 | 0 |

Military and Naval remain the same engine category, `military`, and are therefore treated as same-tree.

### Graph validation

| Check | Result |
|---|---:|
| Active technologies, full graph | 238 |
| Active prerequisite edges before | 307 |
| Active prerequisite edges after | 296 |
| `BROKEN_REFERENCES` | 0 |
| Compatibility-alias prerequisite references in the active graph | 0 |
| `CYCLES` | 0 |
| `ERA_INVERSIONS` | 0 |
| `DUPLICATE_ACTIVE_IDS` | 0 |
| `POST1836_CROSS_CATEGORY_EDGES` | 0 |
| `PRE1836_CROSS_CATEGORY_EDGES` | 0 |
| `FULL_TREE_CROSS_CATEGORY_EDGES` | 0 |

The sole new root is `state_dockyard_systems` in Era I. It is classified `ERA_I_INTENTIONAL_ROOT`. The matrix creates no other new root in Eras II–VI.

### Scope guard

- Gameplay edits are limited to the four authorized early-tree files.
- `90_tech3a_vanilla_post1836_compatibility.txt` is unchanged.
- No era, category, unlock, AI weight, localization, description, icon, modifier, GUI, or post-1836 gameplay definition was changed.
- The only non-gameplay additions are the five `TECH4C2_*` audit deliverables in this directory.

Final tracked `git diff --stat`:

```text
common/technology/technologies/10_tech3a_production.txt |  2 +-
common/technology/technologies/20_tech3a_military.txt   |  8 +++-----
common/technology/technologies/25_tech3a_naval.txt      | 12 ++----------
common/technology/technologies/30_tech3a_society.txt    |  6 +-----
4 files changed, 7 insertions(+), 21 deletions(-)
```

The five report files are new and therefore appear separately as untracked files until the user chooses to commit them.

## PART B — DOCUMENTARY AUDIT

No residual cleanup was implemented. No old node was deleted, hidden, retimed, reclassified, or given a different gameplay responsibility.

### Effective Era I–VI universe

The effective graph contains 127 Era I–VI technologies:

- 126 normal researchable and visible technologies;
- one legitimate regional/event-only non-researchable technology, `mysorean_iron_cased_rocketry`;
- 118 entries present in the TECH3A implemented index;
- 9 active definitions absent from that index.

The complete inventory, effective definition source, graph relationships, researchability, visibility, authority disposition, and responsibility counts are recorded in [TECH4C2_EFFECTIVE_ERA_I_VI_TECH_UNIVERSE.csv](TECH4C2_EFFECTIVE_ERA_I_VI_TECH_UNIVERSE.csv).

### Residual vanilla definitions

The nine Era I–VI definitions not present in the TECH3A index are:

| Primary classification | Count | Technologies |
|---|---:|---|
| `INTENDED_VISIBLE_SURVIVOR` | 1 | `colonization` |
| `INTENDED_DISTINCT_PARALLEL` | 2 | `distillation`, `crystal_glass` |
| `REWIRE_SOURCE_STILL_VISIBLE` | 1 | `enclosure` |
| `SPLIT_SOURCE_STILL_VISIBLE` | 3 | `intensive_agriculture`, `manufacturies`, `pharmaceuticals` |
| `MERGE_SOURCE_STILL_VISIBLE` | 2 | `lathe`, `corporate_charters` |

Six nodes also carry the tag `UNLOCK_TRANSFER_INCOMPLETE`: `enclosure`, `intensive_agriculture`, `manufacturies`, `lathe`, `corporate_charters`, and `pharmaceuticals`. `lathe` additionally carries `DESIGN_REVIEW_REQUIRED` because TECH2H did not freeze its individual responsibility transfer.

The detailed evidence is in [TECH4C2_PRE1836_VANILLA_RESIDUAL_AUDIT.csv](TECH4C2_PRE1836_VANILLA_RESIDUAL_AUDIT.csv).

### Mandatory cases and findings

#### Agriculture

`enclosure` and `intensive_agriculture` currently form a second visible agricultural chain beside the TECH3A family. This is `PARALLEL_BRANCH_DUPLICATION`, not useful density.

- `enclosure`: 17 audited unlocks and 28 references, including 16 farm/plantation building gates. Future work should transfer the building and decree responsibilities to `improved_husbandry`, resolve remaining land-reform triggers, and only then hide the compatibility source.
- `intensive_agriculture`: 6 audited unlocks and 17 references. TECH2H already froze nine relationship assignments across `advanced_crop_rotations`, `selective_breeding`, `industrial_acids`, and `deep_mine_engineering`. Those transfers are not yet implemented.

#### Glass

`crystal_glass` and `pressed_glass` are classified `LEGITIMATE_SPECIALIZATION`, not automatic duplicates. `crystal_glass` retains one distinct lead/crystal-glass production-method responsibility; `pressed_glass` represents a different mechanized process. The future phase should keep both concepts, add `crystal_glass` to the formal index, and review whether their Era VI placement should be parallel or sequential.

#### Manufacturies

`manufacturies` is an Era IV root with 9 audited unlocks and 17 references, creating a broad shortcut beside specialized TECH3A factory chains. TECH2H froze twelve relationships among `interchangeable_manufacture`, `mechanized_weaving`, `pressed_glass`, `continuous_papermaking`, and `mechanical_tools`. The node cannot be hidden until those assignments and remaining references are implemented.

#### Lathe

`lathe` overlaps strongly with `precision_boring` and `mechanical_tools`. It still owns three production-method responsibilities and has 10 audited references. The likely structure is to move lathe/dye production-method gates to `mechanical_tools`, review the leaded-glass responsibility against `crystal_glass`, then hide the old source. This remains a design review because TECH2H did not freeze the individual mapping.

#### Distillation

`distillation` is a legitimate batch-distillation precursor, not a removable duplicate. The current graph is explicitly sequential:

`manufacturies` → `distillation` → `fractional_distillation`

`fractional_distillation` also requires `mechanical_tools` and `industrial_acids`. Future work should preserve the `distillation` prerequisite and formalize the old ID in the index rather than consume it without a rewire.

#### Colonization

`colonization` is an intended visible survivor. TECH2H explicitly preserved it as the vanilla successor of restored `international_relations`. Its 11 audited unlocks and 59 references cover colonial responsibilities distinct from domestic cadastral administration. It should remain visible and be added to the formal TECH3A index.

#### Other discovered cases

- `corporate_charters`: strong merge/functional duplication with `stock_exchange`; 8 unlocks and 21 references, including seven company requirements. Transfer those gates and modifiers before hiding the old ID.
- `pharmaceuticals`: broad split source surviving beside the specialized public-health chain; 2 unlocks and 20 references. TECH2H froze five relationships to `active_principle_pharmacy`; they remain untransferred.

### Responsibility census for residuals

| Technology | Unlocks | References | Main untransferred responsibility classes |
|---|---:|---:|---|
| `enclosure` | 17 | 28 | 16 building gates; agricultural decree/land-reform references |
| `intensive_agriculture` | 6 | 17 | 2 building, 3 PM, 1 event, 1 journal, 1 history reference |
| `manufacturies` | 9 | 17 | 6 building, 1 law, 1 journal, other broad factory references |
| `lathe` | 3 | 10 | 3 PM and 1 history reference |
| `distillation` | 2 | 7 | 2 PM; prerequisite of `fractional_distillation` |
| `crystal_glass` | 1 | 4 | 1 distinct PM |
| `colonization` | 11 | 59 | 1 building, 4 laws, 1 institution, 5 events, 4 journals, 1 history reference |
| `corporate_charters` | 8 | 21 | 7 company requirements and corporate modifiers |
| `pharmaceuticals` | 2 | 20 | 2 laws and 4 event references |

### Family duplication result

Eight families were compared in [TECH4C2_PRE1836_FAMILY_DUPLICATION_AUDIT.csv](TECH4C2_PRE1836_FAMILY_DUPLICATION_AUDIT.csv):

- parallel branch duplication: Agriculture, Factory Mechanization, Pharmacy/Public Health;
- functional duplication: Machine Tools, Corporate Finance;
- legitimate specialization: Glass, Distillation/Chemistry;
- no duplicate: Colonial Administration.

### Era I–VI graph shape after isolation

- `ACTIVE_TECHS_I_VI = 127`
- `ACTIVE_EDGES_I_VI = 156`
- `FAN_IN_DISTRIBUTION = {0: 23, 1: 59, 2: 38, 3: 7}`
- `FAN_OUT_DISTRIBUTION = {0: 32, 1: 44, 2: 26, 3: 10, 4: 6, 5: 3, 7: 6}`

Researchable roots by era:

- Era I: `atmospheric_engine`, `coke_smelting`, `enclosed_dock_systems`, `improved_husbandry`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `international_relations`, `periodical_print_networks`, `scientific_fortification_siegecraft`, `shaft_mining`, `state_dockyard_systems`.
- Era II: `industrial_acids`, `systematic_administrative_statistics`, `turnpike_road_networks`, `variolation_networks`.
- Era III: `industrial_ceramics`, `marine_chronometry`, `mechanized_spinning`, `organized_elementary_schooling`, `standardized_field_artillery`.
- Era IV: `enclosure`, `manufacturies`.

The Era IV residual roots are direct evidence of the parallel Agriculture and Factory Mechanization branches.

`mysorean_iron_cased_rocketry` is a separate Era IV event/regional-only non-researchable root.

Dead ends by era, measured against successors in the full active graph:

- Era I: `commercial_insurance_markets`.
- Era II: none.
- Era III: `selective_breeding`, `veterinary_science`.
- Era IV: `abolitionist_mobilization`, `chemical_bleaching`, `colonization`, `copper_sheathing`, `corporate_charters`, `mysorean_iron_cased_rocketry`, `optical_telegraph_networks`, `scientific_metrology`, `systematic_cadastral_surveying`.
- Era V: `active_principle_pharmacy`, `canneries`, `casemated_fortifications`, `coal_gasification`, `continuous_papermaking`, `field_engineering_pontoon_trains`, `mechanized_weaving`, `military_veterinary_services`, `mine_safety_engineering`, `paddle_steamer`, `standardized_military_rockets`, `standardized_naval_signals`, `systematic_field_drainage`.
- Era VI: `crystal_glass`, `geological_surveying`, `hydraulic_turbines`, `liberal_constitutionalism`, `maritime_safety_standards`, `modern_lighthouse_optics`, `professional_civil_policing`.

There are 32 such Era I–VI nodes. The main high fan-out bundles are `industrial_acids`, `scientific_naval_architecture`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `systematic_administrative_statistics`, and `experimental_research_laboratories` (7 successors each). Seven nodes have fan-in 3: `railways`, `pressed_glass`, `fractional_distillation`, `general_staff`, `mechanized_naval_dockyards`, `iron_hull_construction`, and `liberal_constitutionalism`.

### Recommended next phase

1. Implement only the TECH2H-frozen responsibility transfers for `intensive_agriculture`, `manufacturies`, and `pharmaceuticals`.
2. Freeze mappings for the unresolved `enclosure`, `lathe`, and `corporate_charters` responsibilities before any visibility change.
3. Formalize `colonization`, `distillation`, and `crystal_glass` as retained indexed concepts.
4. Re-run full reference, history, setup, cycle, era, and runtime visibility validation before hiding any consumed compatibility ID.
5. Preserve `distillation` → `fractional_distillation` unless a separately approved rewire replaces it.

## Final validation

| Required result | Actual |
|---|---|
| `CROSS_CATEGORY_EDGES_I_XII` | 0 |
| `CROSS_TREE_EDGES_REMOVED` | 18 |
| `SAME_TREE_EDGES_ADDED` | 7 |
| `PREREQUISITE_LISTS_CHANGED` | 14 |
| `BROKEN_REFERENCES` | 0 |
| `CYCLES` | 0 |
| `ERA_INVERSIONS` | 0 |
| `POST1836_GAMEPLAY_CHANGES` | 0 |
| `ERA_CHANGES` | 0 |
| `UNLOCK_CHANGES` | 0 |
| `CATEGORY_CHANGES` | 0 |
| `LOCALIZATION_CHANGES` | 0 |
| `GUI_CHANGES` | 0 |
| `RESIDUAL_AUDIT_COMPLETE` | YES |
| `RESIDUAL_CLEANUP_IMPLEMENTED` | NO |

`TECH4C2_EARLY_TREE_ISOLATION_STATIC_PASS_RESIDUAL_AUDIT_COMPLETE`
