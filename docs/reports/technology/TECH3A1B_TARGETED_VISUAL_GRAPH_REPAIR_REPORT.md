# TECH-3A.1b — Targeted Visual Graph Repair

## Verdict

`TECH3A1B_TARGETED_VISUAL_GRAPH_REPAIR = PASS`

The static repair is complete and ready for a new human visual review. It does not claim that the native auto-layout is visually validated: a fresh in-game capture is still required.

## Scope and evidence

- Branch: `technology-rework`
- Baseline: the uncommitted TECH-3A.1 technology tree present before this phase.
- Technology definitions inspected: every file below `common/technology/`.
- Required reports and TECH-3A indexes were read before editing.
- Visual evidence used: only the newest screenshots from `C:\Users\simeo\Pictures\Screenshots`, dated 2026-08-22 from 11:08:57 through 11:14:59. Older screenshots from 02:00 and 2026-08-21 were excluded.
- No GUI file, custom editor, technology ID, category, gameplay effect, modifier, texture or gameplay unlock was changed.
- No commit and no push were performed.

The recent screenshots confirm four concrete classes of defect: the broken Distillation family, extreme vertical edges, a Military standing-army lobe joined by an artificial medical bridge, and a completely empty Society era 11 producing a full-width blank band.

## Targeted correction set

This phase changes 13 technology eras and 9 prerequisite lists across 21 unique technologies. The full row-level register is in `TECH3A1B_CHANGES.csv`; visual diagnoses are in `TECH3A1B_VISUAL_ISSUE_REGISTER.csv`.

### Production

1. Repaired the required chain as `manufacturies (era 4) -> distillation (era 5) -> fractional_distillation (era 6)`.
2. Preserved the protected `mechanical_tools` and `industrial_acids` prerequisites on `fractional_distillation`, then added the objectively missing `distillation` prerequisite. This is the one protected baseline list changed.
3. Retimed `enclosure` to era 4 and `intensive_agriculture` to era 5, matching their historical/start-period role and making their two-node family adjacent.
4. Replaced the four six-era Production relations with closer semantic predecessors or targeted retiming:
   - `atmospheric_engine -> watertube_boiler` became `high_pressure_steam -> watertube_boiler`;
   - `shaft_mining -> steelworking` became `hot_blast_smelting -> steelworking`;
   - `shaft_mining -> prospecting` became `geological_surveying -> prospecting`;
   - `mechanized_farming` moved from era 10 to era 8 while retaining `threshing_machine`.
5. Verified `cotton_gin (era 4) -> lathe (era 5) -> crystal_glass (era 6)` and left it unchanged because it is already a compact adjacent progression.

The starting-invention scripted effects grant `manufacturies`, `distillation` and `enclosure` to multiple country tiers. Their early placement therefore describes the chronology of the graph without removing the already configured 1776 starting knowledge.

### Military

1. Removed the TECH-3A.1 artificial `standing_army -> triage` prerequisite.
2. Kept `logistics -> triage`, which is the direct medical-logistics relation.
3. Integrated the standing-army family through `enlistment_offices`, which now depends on `logistics`, `mandatory_service` and `army_reserves`. The formerly separated lobe now has two logical recruitment-family connections rather than one medical bridge.
4. Moved `field_works` from era 7 to era 8 and `trench_works` from era 10 to era 9, then added `field_works -> trench_works`.
5. Left Military eras 2 and 11 sparse. Filling them would require arbitrary movement of protected/custom nodes not tied to a demonstrated capture defect.

The two Military large single-bridge subgraphs caused by `logistics -> triage` and `standing_army -> triage` disappear. Military large bridges fall from 4 to 2.

### Society

1. Filled the empty era 11 with four individually justified terminal technologies: `analytical_philosophy`, `behaviorism`, `mass_propaganda` and `paved_roads`. The late distribution changes from era 11/12 = 0/8 to 4/4.
2. Moved `colonization` from era 7 to era 4. Its retained `international_relations` edge now spans three eras instead of six, eliminating the large empty rectangle visible around Colonization.
3. Replaced `international_relations -> nationalism` with `national_sovereignty -> nationalism`.
4. Moved `corporate_charters` from era 7 to era 4, reducing its `stock_exchange` edge from six eras to three and positioning it between the early exchange and later joint-stock branch.
5. Added `professional_civil_policing -> law_enforcement`. This provides a second semantic entry to the administration subgraph; `nationalism -> centralization` no longer separates a 30-node subgraph as a bridge.
6. Preserved the designed hubs `periodical_print_networks`, `institutionalized_scientific_exchange` and `systematic_administrative_statistics`.

## Global metrics

| Metric | Before | After | Result |
|---|---:|---:|---|
| Technologies | 276 | 276 | preserved |
| Connected components | 6 | 6 | unchanged; three one-node legacy isolates remain |
| Empty category eras | 1 | 0 | improved |
| Sparse category eras (1-3 nodes) | 7 | 7 | unchanged and documented |
| Era-gap 2 edges | 108 | 102 | improved |
| Era-gap 3 edges | 36 | 48 | increased as former extreme edges were shortened |
| Era-gap 4+ edges | 19 | 12 | improved by 36.8% |
| Era-gap 6 edges | 7 | 0 | eliminated |
| Large single-bridge subgraphs | 21 | 18 | improved |
| Duplicate IDs | 0 | 0 | pass |
| Missing prerequisite references | 0 | 0 | pass |
| Cycles | 0 | 0 | pass |
| Era inversions | 0 | 0 | pass |

The increase in three-era edges is intentional: multiple six-era edges were converted into historically defensible three-era progressions. This phase prioritizes removal of the visually extreme edges rather than optimizing a single aggregate count.

## Per-category structural metrics

| Category | Nodes | Articulation points before/after | Bridges before/after | Large bridges before/after | Hubs degree 5+ before/after | Roots before/after | Terminals before/after |
|---|---:|---:|---:|---:|---:|---:|---:|
| Production | 90 | 31 / 29 | 31 / 29 | 6 / 6 | 4 / 5 | 11 / 11 | 27 / 25 |
| Military | 88 | 17 / 14 | 23 / 19 | 4 / 2 | 9 / 9 | 11 / 11 | 24 / 22 |
| Society | 98 | 31 / 32 | 34 / 35 | 11 / 10 | 7 / 7 | 9 / 9 | 27 / 25 |

Society gains one articulation point because the shortened Colonization/Quinine chain is now explicit in the middle eras, while its problematic 30-node `nationalism -> centralization` cut ceases to be a bridge. The large-bridge count, not articulation count alone, is the relevant improvement.

### Long edges by category

| Category | Gap 2 before/after | Gap 3 before/after | Gap 4+ before/after | Gap 6 before/after |
|---|---:|---:|---:|---:|
| Production | 29 / 31 | 13 / 16 | 8 / 5 | 4 / 0 |
| Military | 33 / 30 | 12 / 16 | 3 / 2 | 0 / 0 |
| Society | 46 / 41 | 11 / 16 | 8 / 5 | 3 / 0 |

## Era occupancy, roots and terminals

Each cell is `technologies / roots / terminals`.

### Production

| Era | Before | After |
|---|---:|---:|
| 1 | 4 / 4 / 0 | 4 / 4 / 0 |
| 2 | 3 / 2 / 0 | 3 / 2 / 0 |
| 3 | 6 / 2 / 1 | 6 / 2 / 1 |
| 4 | 10 / 0 / 0 | 12 / 2 / 0 |
| 5 | 12 / 0 / 5 | 14 / 0 / 5 |
| 6 | 11 / 2 / 5 | 9 / 0 / 4 |
| 7 | 10 / 1 / 3 | 8 / 1 / 2 |
| 8 | 10 / 0 / 0 | 11 / 0 / 1 |
| 9 | 4 / 0 / 1 | 4 / 0 / 1 |
| 10 | 12 / 0 / 5 | 11 / 0 / 4 |
| 11 | 3 / 0 / 2 | 3 / 0 / 2 |
| 12 | 5 / 0 / 5 | 5 / 0 / 5 |

Sparse Production eras remain 2 and 11. Era 9 contains four technologies and is not sparse under the required threshold.

### Military

| Era | Before | After |
|---|---:|---:|
| 1 | 3 / 3 / 0 | 3 / 3 / 0 |
| 2 | 1 / 0 / 0 | 1 / 0 / 0 |
| 3 | 6 / 3 / 0 | 6 / 3 / 0 |
| 4 | 6 / 1 / 2 | 6 / 1 / 2 |
| 5 | 14 / 2 / 7 | 14 / 2 / 7 |
| 6 | 6 / 0 / 2 | 6 / 0 / 2 |
| 7 | 16 / 2 / 2 | 15 / 2 / 0 |
| 8 | 8 / 0 / 1 | 9 / 0 / 1 |
| 9 | 5 / 0 / 0 | 6 / 0 / 0 |
| 10 | 10 / 0 / 3 | 9 / 0 / 3 |
| 11 | 3 / 0 / 0 | 3 / 0 / 0 |
| 12 | 10 / 0 / 7 | 10 / 0 / 7 |

Sparse Military eras remain 1, 2 and 11. Era 1 is a legitimate root band; era 2 and era 11 are retained as narrow transition bands rather than filled by non-targeted remapping.

### Society

| Era | Before | After |
|---|---:|---:|
| 1 | 6 / 4 / 1 | 6 / 4 / 1 |
| 2 | 2 / 2 / 0 | 2 / 2 / 0 |
| 3 | 7 / 1 / 1 | 7 / 1 / 1 |
| 4 | 12 / 0 / 5 | 14 / 0 / 4 |
| 5 | 8 / 0 / 4 | 8 / 0 / 4 |
| 6 | 6 / 0 / 3 | 6 / 0 / 2 |
| 7 | 27 / 2 / 2 | 25 / 2 / 2 |
| 8 | 11 / 0 / 1 | 11 / 0 / 1 |
| 9 | 1 / 0 / 0 | 1 / 0 / 0 |
| 10 | 10 / 0 / 2 | 10 / 0 / 2 |
| 11 | 0 / 0 / 0 | 4 / 0 / 4 |
| 12 | 8 / 0 / 8 | 4 / 0 / 4 |

Society no longer has an empty era. Its sparse eras remain 2 and 9; neither was responsible for the captured full-width late-game gap.

## Remaining bridge and layout risks

- Production still has six large single-bridge chains. In particular, `geological_surveying -> prospecting` and `nitroglycerin -> prospecting` delimit a large mining/chemistry chain. The new prerequisite is semantically correct and adjacent, but visual placement still requires inspection.
- Military retains two large naval/survey bridges through `hydrographic_surveying`; they were not part of the captured standing-army defect and were left unchanged.
- Society retains ten large bridges, including `banking -> currency_standards` separating a 14-node finance section. The demonstrated 30-node `nationalism -> centralization` bridge was removed; broader finance rewiring was deliberately avoided.
- Three legacy isolated technologies remain: `sericulture`, `military_veterinary_services` and `mysorean_iron_cased_rocketry`. They predate this repair and were not connected with decorative edges.
- Horizontal ordering is controlled entirely by the vanilla auto-layout. Static graph improvement cannot substitute for a new in-game screenshot.

## Integrity validation

- Parsed technology definitions: PASS.
- Technology count: 276 before and after.
- Unique IDs: PASS, 0 duplicates.
- Existing prerequisite references: PASS, 0 missing.
- Valid categories and eras: PASS.
- Directed cycles: PASS, 0.
- Era inversions: PASS, 0.
- Distillation order: era 4 -> era 5 -> era 6, PASS.
- Distillation direct line: prerequisite present, PASS.
- Non-layout definition hashes: 276/276 identical before and after. This proves that technology effects, modifiers, textures, AI blocks and gameplay unlock content inside the definitions are unchanged.
- Gameplay files outside the targeted technology definitions: unchanged by this phase.
- GUI files: 0 changed by this phase.
- Change register: 21/21 changed technology IDs recorded.

An automated noninteractive Victoria 3 runtime smoke-test mode is not available in this workspace, so runtime validation is `NOT_RUN`. Static validation is `PASS`. Human visual validation remains `REQUIRED` using new screenshots produced after the game reloads these definitions.

## Deliverables

- `TECH3A1B_GRAPH_BEFORE.csv`: exact 276-node TECH-3A.1 baseline.
- `TECH3A1B_GRAPH_AFTER.csv`: exact repaired graph.
- `TECH3A1B_CHANGES.csv`: all 21 changed technology definitions with individual justification.
- `TECH3A1B_VISUAL_ISSUE_REGISTER.csv`: capture-grounded issue diagnoses and expected visual effects.
- `TECH3A1B_TARGETED_VISUAL_GRAPH_REPAIR_REPORT.md`: this report.

## Human review checklist

1. Reload the mod and open Production around eras 4-7. Confirm a visible direct line from Distillation to Distillation fractionnée and no era reversal.
2. Confirm Enclosure/Agriculture intensive and the metallurgy/geology nodes occupy compact neighboring bands.
3. Open Military eras 7-9. Confirm the standing-army branch is integrated around Enlistment offices and no longer hangs from Triage.
4. Confirm Field works leads into Trench works.
5. Open Society. Confirm Colonization no longer sits below a six-era empty rectangle and era 11 contains four terminal nodes.
6. Capture the three full trees again. The final visual verdict must be based on those new images, not this static report.
