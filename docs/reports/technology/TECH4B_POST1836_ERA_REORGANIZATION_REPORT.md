# TECH-4B — Post-1836 Era Reorganization Report

**Static status:** `TECH4B_POST1836_ERA_REORGANIZATION_STATIC_PASS_RUNTIME_PENDING`

## 1. Baseline and scope

- Branch: `technology-rework`
- Git baseline: `518eb670d0e594ab5137ac5050276dd299f98171`
- Working tree at phase start: clean
- Vanilla reference: Victoria 3 `release/1.13.11`
- Active Era VII-XII technologies confirmed: **111**
- Compatibility aliases excluded and unchanged: **38**
- Implementation file: `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`

TECH-4B changes only the `era` assignment of selected active post-1836 technologies. It does not implement TECH-4C prerequisite corrections.

## 2. Implementation summary

- Technologies moved: **33**
- Moved earlier: **26**
- Moved later: **7**
- Kept in current era: **78**
- `ERA_VII_BOUNDARY_COMPROMISE`: **1** (`romanticism`)
- `BLOCKED_BY_CURRENT_PREREQUISITE_GRAPH`: **0**
- `EVENT_TECH_KEEP`: **1** (`sericulture`)

All proposed moves were checked against the unchanged prerequisite graph before implementation. No move creates a later-era prerequisite inversion.

## 3. Density before and after

| Era | Production before/after | Military before/after | Naval before/after | Society before/after | Total before | Total after |
|---|---:|---:|---:|---:|---:|---:|
| era_7 | 5 / 7 | 0 / 3 | 0 / 1 | 5 / 8 | 10 | 19 |
| era_8 | 11 / 10 | 6 / 3 | 3 / 3 | 11 / 6 | 31 | 22 |
| era_9 | 4 / 6 | 3 / 5 | 3 / 2 | 1 / 4 | 11 | 17 |
| era_10 | 11 / 9 | 4 / 2 | 5 / 3 | 10 / 9 | 30 | 23 |
| era_11 | 3 / 3 | 2 / 5 | 1 / 4 | 4 / 4 | 10 | 16 |
| era_12 | 5 / 4 | 6 / 3 | 4 / 3 | 4 / 4 | 19 | 14 |

The extreme `10 / 31 / 11 / 30 / 10 / 19` alternation becomes `19 / 22 / 17 / 23 / 16 / 14`. Both overloaded peaks are reduced, all former troughs are raised by historically supported moves, and every era falls within the requested soft range of 14-23 technologies.

Era VII gains an historically justified Naval entry through `ironclad_tech` (1850s) and three Military-category nodes through mid-century communications, medicine, and field fortification. Era IX Society rises from one to four nodes through late-19th-century corporatism, steel-frame urbanization, and elevator adoption. Era X retains a lower Military count because later military developments fit the 1910s better; no artificial filler move was introduced.

## 4. Chronology decisions

The three TECH-4A `TOO_EARLY` cases move later: `steam_donkey`, `corporatism`, and `steel_frame_buildings` all move from Era VIII to Era IX.

Seventeen of the 24 TECH-4A `TOO_LATE` cases move earlier. `romanticism` remains in Era VII as the earliest legal post-1836 compromise, while `sericulture` remains an event/non-researchable technology. Five final-era nodes are retained after individual re-evaluation: `mobile_armor`, `chemical_warfare`, `flamethrowers`, `arc_welding`, and `dough_rollers`; their matrix rows explain the adoption/gameplay rationale.

Additional moves marked `GOOD` or `BORDERLINE` in TECH-4A were made only where their historical adoption window and family sequence support the change. The detailed 111-row matrix records every keep or move decision.

## 5. Family continuity

All **36** TECH-4A conceptual families remain represented. The family audit records eras and chronological summaries before and after the reorganization.

Important improvements include:

- telecommunications now progresses through Era VII electric telegraph, Era IX telephone, and Era XI radio;
- naval hull development begins with Era VII ironclads, followed by Era VIII monitors and later capital-ship families;
- industrial materials place rubber mastication in Era VII, aniline/vulcanization in Era VIII, and later synthetic materials in Era X-XII;
- internal combustion moves to Era IX, compression ignition to Era XI, and retains later interwar development space;
- urban infrastructure places steel frames/elevators in Era IX and paved roads in Era X;
- military organization moves wargaming to Era IX and NCO training/stormtroopers to Era XI.

A family marked `REVIEW_IN_TECH4C` is not chronologically broken by TECH-4B; it retains a weak or arbitrary semantic edge that must be reviewed in the dedicated graph phase.

## 6. Static graph and gameplay validation

| Validation | Result |
|---|---:|
| `ACTIVE_TECHS_BEFORE` | 111 |
| `ACTIVE_TECHS_AFTER` | 111 |
| `TECH_IDS_ADDED` | 0 |
| `TECH_IDS_REMOVED` | 0 |
| `PREREQUISITE_EDGES_BEFORE` | 152 |
| `PREREQUISITE_EDGES_AFTER` | 152 |
| `PREREQUISITE_LISTS_CHANGED` | 0 |
| `BROKEN_PREREQUISITE_REFERENCES` | 0 |
| `PREREQUISITE_CYCLES` | 0 |
| `LATER_ERA_PREREQUISITE_INVERSIONS` | 0 |
| `DUPLICATE_TECH_IDS` | 0 |
| `UNLOCK_CHANGES` | 0 |
| `EFFECT_CHANGES` | 0 |
| `COST_CHANGES` | 0 |
| `CATEGORY_CHANGES` | 0 |
| `LOCALIZATION_CHANGES` | 0 |
| `GUI_CHANGES` | 0 |
| `ERA_I_VI_CHANGES` | 0 |
| `COMPATIBILITY_ALIAS_CHANGES` | 0 |

The implementation diff contains exactly 33 removed `era = era_N` lines and 33 replacement `era = era_N` lines. No other technology field is modified.

## 7. Problems deliberately reserved for TECH-4C

TECH-4B preserves all prerequisite semantics, including the **9 arbitrary edges**, **29 weak edges**, **22 pre-final-era dead ends**, cross-family links, and excessive fan-in cases documented by TECH-4A.

The nine arbitrary edges left unchanged are:

- `realism` -> `camera`
- `vulcanization` -> `automatic_bottle_blowers`
- `monitor_tech` -> `landing_craft`
- `handcranked_machine_gun` -> `military_aviation`
- `reinforced_concrete` -> `plastics`
- `military_aviation` -> `dreadnought_tech`
- `electrical_capacitors` -> `pasteurization`
- `elevator` -> `paved_roads`
- `concrete_fortifications` -> `mobile_armor`

No edge was added to fill a column, suppress a root, or reduce a dead-end count. TECH-4C must re-evaluate the complete 152-edge topology independently.

## 8. Runtime checklist

The user runtime test should verify:

- visual density of Eras VII-XII;
- removal of the extreme dense/sparse alternation;
- family continuity and sensible columns;
- all 111 active technologies remain visible where expected;
- no TECH-3B compatibility alias reappears;
- no broken lines or raw localization keys;
- no unexpected gameplay behavior.

No runtime PASS is claimed in this phase.

**Final static status:** `TECH4B_POST1836_ERA_REORGANIZATION_STATIC_PASS_RUNTIME_PENDING`
