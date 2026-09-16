# TECH TREE 1776 — Wave 2 Global Structural Skeleton Report

Date: 2026-09-14

Target: Victoria 3 1.13.11

Scope: production, military/naval, and society structural skeleton only

## Outcome

Wave 2 is implemented on top of the runtime-validated Wave 1. The three Wave 1 pure trunks and their 226 grants were preserved unchanged. This wave adds the accepted internal structural links, redefines `turnpike_road_networks` as a general land-infrastructure concept, and applies exactly 67 reviewed structural grants.

No era, gameplay modifier, building, production method, law, alias/merge, or broad historical redistribution was added by this wave.

## Files affected by Wave 2

Technology graph:

- `common/technology/technologies/10_tech3a_production.txt`
- `common/technology/technologies/20_tech3a_military.txt`
- `common/technology/technologies/25_tech3a_naval.txt`
- `common/technology/technologies/30_tech3a_society.txt`

Localization:

- `localization/english/tech3a_technology_l_english.yml`
- `localization/french/tech3a_technology_l_french.yml`

Validation/application support:

- `tools/tech_start_1776_implementation.py`

Country history:

- 65 distinct country-history files received the 67 grants listed below. France and Japan each received two grants; every other affected TAG received one.

Report:

- `docs/reports/technology/TECH_TREE_1776_WAVE2_GLOBAL_SKELETON_REPORT.md`

## Exact structural relations applied

Notation: `parent -> child`.

### Production

Added:

1. `organized_workshops -> coke_smelting`
2. `traditional_food_processing -> distillation`
3. `traditional_food_processing -> sugar_refining`
4. `traditional_glassmaking -> industrial_ceramics`
5. `traditional_glassmaking -> crystal_glass` (in addition to `industrial_ceramics`)
6. `turnpike_road_networks -> industrial_canals`
7. `applied_mineralogy -> deep_mine_engineering` (in addition to `shaft_mining` and `atmospheric_engine`)

Explicitly preserved:

- `atmospheric_engine` requires `shaft_mining`, not `coke_smelting`.
- `applied_mineralogy` remains a useful specialized root; it does not require `shaft_mining`.
- `advanced_crop_rotations` and `selective_breeding` remain sibling branches under `improved_husbandry`.
- `traditional_papermaking`, `traditional_glassmaking`, and `industrial_acids` do not require `organized_workshops`.

### Military

Added:

1. `permanent_engineer_services -> military_topographic_surveying`
2. `veterinary_science -> military_veterinary_services` (alongside `horse_artillery`)

The six direct children of `organized_military_establishments` remain unchanged.

### Naval

Replaced:

1. `marine_chronometry`: `scientific_naval_architecture` replaced by `ship_classification_surveying`.
2. `standardized_naval_signals`: `scientific_naval_architecture` replaced by `ship_classification_surveying`.

Removed:

3. `scientific_naval_architecture -> iron_hull_construction`; its remaining parents are `diagonal_ship_framing`, `mechanized_naval_dockyards`, and `paddle_steamer`.

The four direct children of `organized_naval_establishments` remain unchanged.

### Society

Added from `codified_practical_knowledge`:

1. `organized_elementary_schooling`
2. `medical_degrees`
3. `systematic_cadastral_surveying`
4. `systematic_legal_codification`
5. `political_economy`

`codified_practical_knowledge` remains a pure structural root with no restored parent. The three branches of `organized_financial_institutions` remain siblings.

## Infrastructure concept localization

The ID `turnpike_road_networks` is retained for compatibility, while its displayed meaning is broadened:

- English: **Organized Land Infrastructure**
- French: **Infrastructure terrestre organisée**

Its existing road PM content is preserved. The new parent link to `industrial_canals` represents general organized land-infrastructure capacity rather than a literal historical dependency on toll roads.

## Exact Wave 2 grants

### `traditional_food_processing` — 39

`BLG`, `BNJ`, `BRU`, `BTN`, `CHC`, `CHP`, `CHT`, `CIR`, `CMI`, `EZO`, `GAL`, `JAB`, `JBB`, `JMB`, `KAF`, `KAL`, `KKI`, `KTI`, `KZH`, `LUA`, `MAK`, `MGD`, `MGH`, `MLT`, `NEJ`, `NGA`, `OZH`, `PON`, `PRK`, `SAK`, `SEL`, `SHS`, `SMB`, `STG`, `SUL`, `TID`, `TIP`, `TRM`, `UZH`

### `codified_practical_knowledge` — 16

`CHL`, `CRO`, `CUB`, `ECU`, `GR3`, `GR5`, `HUN`, `MEX`, `MOD`, `NPU`, `PAR`, `PEU`, `SC1`, `SC3`, `SPU`, `VNZ`

### `turnpike_road_networks` — 8

`BEL`, `BEO`, `CHI`, `FRA`, `IREK`, `JAP`, `NET`, `RUS`

### `traditional_glassmaking` — 2

`KOR`, `LUX`

### `permanent_engineer_services` — 1

`JAP`

### `ship_classification_surveying` — 1

`FRA`

Wave 2 total: **67**.

Wave 1 total preserved: **226**.

Cumulative structural-grant total: **293**.

No `organized_workshops` or `shaft_mining` closure grant was added.

## Global graph metrics

| Metric | Before Wave 2 | After Wave 2 | Expected/documentary target |
|---|---:|---:|---:|
| Researchable nodes | 247 | 247 | unchanged |
| Roots | 29 | 19 | approximately 19 |
| Isolated nodes | 3 | 0 | 0 |
| Leaf nodes without direct effect | 7 | 5 | 0 after later deferred work |
| Edges | 330 | 343 | approximately 340 |
| Maximum child count | 8 | 8 | at most 7 after later cleanup |
| Cycles | 0 | 0 | 0 |
| Unknown parents | 0 | 0 | 0 |
| Negative-era edges | 0 | 0 | 0 |
| Cross-era edges greater than 3 eras | 47 | 46 | later dedicated cleanup |

Edge delta: **16 additions, 3 removals, net +13**.

The final edge count is three above the approximate documentary target because all accepted Wave 2 relations are present while the explicitly deferred cleanup/alias actions have not been used to force the metric.

The maximum fanout of 8 belongs to `industrial_acids`, an existing production node not changed in this wave. None of the structural trunks exceeds the intended visual fanout.

The five remaining leaf/no-effect nodes are exactly the deferred cases:

- `hydraulic_turbines`
- `modern_lighthouse_optics`
- `optical_telegraph_networks`
- `standardized_military_rockets`
- `systematic_cadastral_surveying`

## Metrics by branch

| Branch | Roots before | Roots after | Edges before | Edges after | Isolated before/after | Leaf/no-effect before/after |
|---|---:|---:|---:|---:|---:|---:|
| Production | 14 | 10 | 119 | 126 | 1 / 0 | 1 / 1 |
| Military + Naval | 3 | 2 | 103 | 104 | 0 / 0 | 2 / 2 |
| Society | 12 | 7 | 108 | 113 | 2 / 0 | 4 / 2 |

Fanouts after Wave 2:

- `organized_military_establishments`: 6
- `organized_naval_establishments`: 4
- `codified_practical_knowledge`: 5
- `organized_financial_institutions`: 3

Branch edge operations:

- Production: 7 additions, 0 removals.
- Military + Naval: 4 additions, 3 removals, net +1.
- Society: 5 additions, 0 removals.

## Starting-technology closure

Final deterministic validation over all 474 planned TAGs:

- country overlays matching their target: 473 / 473 managed setups;
- research gaps preserved: `GAL`, `MLT`, `PPU`;
- missing direct prerequisites: 0;
- missing transitive prerequisites: 0;
- duplicate explicit grants: 0;
- unknown technologies in starts: 0;
- forbidden start technologies: 0;
- unexpected removals: 0.

The only country-history changes are the 67 approved grants. No additional grant was inferred to repair closure.

## Static validation

- Technology definitions duplicated: 0.
- Unknown parent IDs: 0.
- Graph cycles: 0.
- Brace-balance errors: 0.
- Wave 1 pure-trunk validation errors: 0.
- Wave 2 exact-parent validation errors: 0.
- Subsistence-tool validation errors: 0.
- English and French infrastructure localization updated under the existing ID.

## Deferred work left untouched

- Mass era changes and era polish.
- The 46 remaining cross-era edges greater than three eras.
- Small modifiers for organized forestry, cadastral surveying, lighthouse optics, and optical telegraphy.
- Alias/merge work for hydraulic turbines and the two military rocket/ammunition nodes.
- Full building/PM causality pass.
- Final historical technology redistribution.
- Opportunistic graph changes not present in the accepted plan.

## Runtime checklist

Production:

- [ ] Inspect the global era 1–4 view.
- [ ] Confirm food processing branches into sugar refining and distillation.
- [ ] Confirm organized land infrastructure branches into canals.
- [ ] Confirm traditional glassmaking routes to ceramics and crystal glass.
- [ ] Inspect mining/metallurgy and agriculture corridors.

Military:

- [ ] Confirm the single military trunk remains readable with six direct children.
- [ ] Confirm military topography follows permanent engineer services.
- [ ] Confirm no new collateral gameplay content appears on the trunk.

Naval:

- [ ] Confirm the four initial naval branches remain visible.
- [ ] Confirm marine chronometry and standardized signals route through ship classification.

Society:

- [ ] Confirm codified practical knowledge is a five-child trunk.
- [ ] Confirm education, medicine, law, cadastre, and political economy are readable.
- [ ] Confirm finance remains an independent three-child trunk.

Runtime:

- [ ] Inspect `error.log`.
- [ ] Run to 1 February.
- [ ] Confirm no crash or broken interface.

No commit, push, or pull request was performed.
