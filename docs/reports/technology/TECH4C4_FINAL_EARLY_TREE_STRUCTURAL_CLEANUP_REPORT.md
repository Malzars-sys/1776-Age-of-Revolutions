# TECH-4C4 — Final Early-Tree Structural Cleanup

## Baseline

- Branch: `tech4c2-audit-snapshot`
- Baseline: `ed0dfd5e78fe0e0bf0b025ee1c06d606c2e253d6`
- Baseline branch and HEAD matched before modification.
- Working tree was clean before modification.
- No commit or push was performed.

## Files changed

Gameplay and GUI:

- `common/technology/technologies/10_tech3a_production.txt`
- `common/technology/technologies/30_tech3a_society.txt`
- `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`
- `gui/tech_tree.gui`

Documentation:

- `docs/reports/technology/TECH3A_IMPLEMENTED_TECH_INDEX.csv`
- `docs/reports/technology/TECH4C4_FINAL_EARLY_TREE_CHANGE_LOG.csv`
- `docs/reports/technology/TECH4C4_FINAL_VISIBLE_I_VI_UNIVERSE.csv`
- `docs/reports/technology/TECH4C4_PRE1836_COMPATIBILITY_ALIAS_REGISTER.csv`
- `docs/reports/technology/TECH4C4_FINAL_EARLY_TREE_STRUCTURAL_CLEANUP_REPORT.md`

No other file was changed.

## Mechanical changes

### Retained visible survivors

| Technology | Destination | Era | Category | Prerequisites |
|---|---|---|---|---|
| `distillation` | `10_tech3a_production.txt` | I | Production | none |
| `crystal_glass` | `10_tech3a_production.txt` | IV | Production | `industrial_ceramics` |
| `colonization` | `30_tech3a_society.txt` | IV | Society | `international_relations` |

`distillation` and `crystal_glass` retain their original textures, AI weights, and comments. `colonization` retains its original modifier, texture, prerequisite, AI weight, category, and era. Each ID remains defined exactly once.

`pressed_glass` remains unchanged in Production Era VI with prerequisites `industrial_ceramics`, `industrial_alkalis`, and `mechanical_tools`. No direct edge was added between `crystal_glass` and `pressed_glass`.

`fractional_distillation` remains Production Era VI and retains prerequisites `mechanical_tools`, `industrial_acids`, and `distillation`.

### Hidden compatibility aliases

The following six definitions remain in `90_tech3a_vanilla_post1836_compatibility.txt` and now have `can_research = no` with the required TECH4C4 compatibility comment:

- `enclosure`
- `intensive_agriculture`
- `manufacturies`
- `lathe`
- `corporate_charters`
- `pharmaceuticals`

Their modifiers, textures, AI weights, existing internal alias relationships, and external gameplay/script references remain unchanged. Gameplay responsibility transfer is deferred to TECH5.

### Active prerequisite rewires

Six final active prerequisite changes are present:

- `distillation`: `manufacturies` → none.
- `crystal_glass`: `lathe` → `industrial_ceramics`.
- `improved_fertilizer`: `intensive_agriculture` → `industrial_acids`.
- `quinine`: `pharmaceuticals` → `active_principle_pharmacy`.
- `antibiotics`: `pharmaceuticals` → `active_principle_pharmacy`; `experimental_research_laboratories` remains unchanged.
- `chemical_bleaching`: `industrial_acids` → `industrial_acids`, `industrial_ceramics`.

### GUI filters

Both existing TECH3B1 compatibility filters were extended with exactly the same six TECH4C4 IDs:

- line-target alias filter: 44 unique IDs;
- technology-card alias filter: 44 unique IDs.

Each new ID appears once in each filter. No layout, position, dimension, zoom, era-line, or category behavior was changed.

### TECH3A index

`TECH3A_IMPLEMENTED_TECH_INDEX.csv` now contains 121 unique technology rows:

- three exact survivor rows added for `distillation`, `crystal_glass`, and `colonization`;
- the 14 TECH4C2 prerequisite rows synchronized;
- `fractional_distillation` synchronized to include `distillation`;
- all synchronized `hard_cross_branch_count` values are 0.

## Static counters

| Counter | Result |
|---|---:|
| `VISIBLE_I_VI_BEFORE` | 127 |
| `VISIBLE_I_VI_AFTER` | 121 |
| `VISIBLE_RESEARCHABLE_I_VI` | 120 |
| `VISIBLE_NONRESEARCHABLE_REGIONAL_OR_EVENT_I_VI` | 1 |
| `ALIASES_ADDED` | 6 |
| `TOTAL_GUI_HIDDEN_ALIASES` | 44 |
| `SURVIVORS_MOVED_TO_TECH3A` | 3 |
| `DISTILLATION_ERA` | I |
| `CRYSTAL_GLASS_ERA` | IV |
| `COLONIZATION_ERA` | IV |
| `CROSS_CATEGORY_EDGES` | 0 |
| `BROKEN_REFERENCES` | 0 |
| `CYCLES` | 0 |
| `ERA_INVERSIONS` | 0 |
| `DUPLICATE_TECH_IDS` | 0 |
| `ACTIVE_TECHS_DEPENDING_ON_HIDDEN_ALIAS` | 0 |
| `VISIBLE_CONSUMED_RESIDUALS` | 0 |
| `GAMEPLAY_GATE_TRANSFERS` | 0 |
| `STARTING_TECH_CHANGES` | 0 |

The effective parser found 276 definitions in total, 232 non-hidden concepts across the complete tree, and 291 active prerequisite edges. All 121 visible Era I–VI concepts are present in the 121-row TECH3A index.

## Scope guards

- No change to `20_tech3a_military.txt` or `25_tech3a_naval.txt`.
- No building, production method, good, law, institution, company, unit, ship, event, journal entry, decree, history, or starting-technology file changed.
- No gameplay responsibility was transferred.
- No modifier or `on_researched` effect was added, removed, or changed.
- The only era changes are `distillation` Era V → I and `crystal_glass` Era VI → IV.

## Manual runtime validation

The full runtime review passed except for one isolated Production-tree defect: `crystal_glass` appeared as an orphan-like Era I root. The targeted correction moves it to Era IV behind `industrial_ceramics`.

- Production: no cards for Enclosure, Intensive Agriculture, Manufacturies, or Lathe.
- Production: Distillation remains visible in Era I.
- Production: Crystal Glass is now defined in Era IV after Industrial Ceramics.
- Production: Chemical Bleaching now requires both Industrial Acids and Industrial Ceramics.
- Production: Pressed Glass and Fractional Distillation remain visible in Era VI.
- Production: no line is rendered from a hidden compatibility alias.
- Society: no cards for Corporate Charters or Pharmaceuticals.
- Society: Colonization is visible in Era IV after International Relations.
- Society: Quinine and Antibiotics have no visible dependency on a hidden alias.
- Military: no structural or visual anomaly was observed.

`TECH4C4_FINAL_EARLY_TREE_STRUCTURE_RUNTIME_PASS_WITH_TARGETED_FIX`
