# TECH-4C — Post-1836 Prerequisite Graph Reconstruction

**Static status:** `TECH4C_POST1836_PREREQUISITE_GRAPH_STATIC_PASS_RUNTIME_PENDING`

## 1. Baseline and scope

- Branch: `technology-rework`
- Git baseline: `c8958b9020d3b97247a776d0e079ecb9f156e4e2`
- Working tree at phase start: clean
- Vanilla reference: Victoria 3 `release/1.13.11`
- Active post-1836 technologies: **111**
- TECH-3B compatibility aliases excluded: **38**
- Concept families retained: **36**
- Era changes: **0**

TECH-4C changes only `unlocking_technologies` lists on active Era VII-XII technologies. IDs, eras, categories, costs, icons, effects, unlock ownership, localization, GUI, Era I-VI definitions and compatibility aliases remain untouched.

## 2. Graph reconstruction summary

- Edges before: **152**
- Edges after: **149**
- `KEEP`: **98**
- `REMOVE`: **19**
- `ADD`: **16**
- `REPLACE`: **35**
- Families with at least one reconstructed list: **28 / 36**

The lower final edge count is intentional: false fan-in and decorative links were removed instead of being replaced mechanically. Every final edge is independently classified and justified.

## 3. Final semantic classifications

| Classification | Count |
|---|---:|
| `ESSENTIAL` | 73 |
| `STRONG` | 36 |
| `PLAUSIBLE` | 18 |
| `CROSS_BRANCH_JUSTIFIED` | 22 |
| `WEAK` | 0 |
| `ARBITRARY` | 0 |
| `ANACHRONISTIC` | 0 |
| `CROSS_BRANCH_SUSPICIOUS` | 0 |

## 4. Resolution of the nine former arbitrary edges

| Former edge | Resolution |
|---|---|
| `realism` -> `camera` | replaced/rewired with `pressed_glass`; former edge retained: no |
| `vulcanization` -> `automatic_bottle_blowers` | replaced/rewired with `pressed_glass`; former edge retained: no |
| `monitor_tech` -> `landing_craft` | replaced/rewired with `floating_harbor`; former edge retained: no |
| `handcranked_machine_gun` -> `military_aviation` | replaced/rewired with `combustion_engine`; former edge retained: no |
| `reinforced_concrete` -> `plastics` | replaced/rewired with `art_silk`; former edge retained: no |
| `military_aviation` -> `dreadnought_tech` | replaced/rewired with `steam_turbine`; former edge retained: no |
| `electrical_capacitors` -> `pasteurization` | removed; former edge retained: no |
| `elevator` -> `paved_roads` | replaced/rewired with `professional_civil_engineering`; former edge retained: no |
| `concrete_fortifications` -> `mobile_armor` | replaced/rewired with `military_aviation`, `compression_ignition`, `stormtroopers`; former edge retained: no |

All nine former arbitrary edges are absent from the final graph.

## 5. Resolution of the 29 former weak edges

- Revalidated as `PLAUSIBLE` or stronger: **5**
- Removed or replaced: **24**

The five retained weak-audit candidates are:

- `nationalism` -> `organized_sports`: National associations, standardized institutions and public competition plausibly prepare organized mass sport; this is institutional rather than merely chronological.
- `institutionalized_scientific_exchange` -> `romanticism`: Transnational learned and publishing networks enabled circulation and contestation of the intellectual currents from which Romanticism emerged.
- `quinine` -> `civilizing_mission`: Reliable tropical medicine materially enabled sustained imperial administration and the expansionist doctrine represented by the civilizing mission.
- `self_propelled_torpedoes` -> `jeune_ecole`: Jeune École doctrine was explicitly built around torpedo craft, making torpedo mastery a direct doctrinal foundation.
- `enlistment_offices` -> `war_propaganda`: Mass recruitment bureaucracy supplies the audience, records and mobilization machinery used by state war-propaganda campaigns.

The other 24 are removed or replaced. The edge-change log records every individual resolution.

## 6. Roots and `modern_nursing`

- Researchable roots before: **0**
- Researchable roots after: **0**
- Separate non-researchable root: `sericulture`

`modern_nursing` was re-read from the effective technology definition. It still has the real prerequisite `medical_degrees`; this edge is retained and classified `CROSS_BRANCH_JUSTIFIED`. The technology has no direct successor after reconstruction. That terminal is deliberate: professional nursing unlocks field hospitals but does not technically enable antibiotic discovery. If the incoming line remains invisible at runtime, the source data is present and the remaining issue is rendering/layout rather than a missing prerequisite.

## 7. Dead ends VII-XI

- TECH-4A dead ends before: **22**
- Dead ends after reconstruction: **27**
- `MISSING_SUCCESSOR`: **0**
- `GRAPH_ERROR`: **0**
- `AVOIDABLE_DEAD_ENDS`: **0**

The raw terminal count rises because several false successor links are removed. This is preferable to preserving artificial topology. Every remaining terminal has an explicit human justification in the final register; no successor was invented solely to reduce the count.

## 8. Cross-branch edges after reconstruction

Final cross-branch edges: **22**.

| Source | Target | Branches | Classification |
|---|---|---|---|
| `pressed_glass` | `camera` | Production -> Society | `CROSS_BRANCH_JUSTIFIED` |
| `optical_telegraph_networks` | `electric_telegraph` | Society -> Military | `CROSS_BRANCH_JUSTIFIED` |
| `medical_degrees` | `modern_nursing` | Society -> Military | `CROSS_BRANCH_JUSTIFIED` |
| `interchangeable_manufacture` | `breech_loading_artillery` | Production -> Military | `CROSS_BRANCH_JUSTIFIED` |
| `shell_gun` | `breech_loading_artillery` | Naval -> Military | `CROSS_BRANCH_JUSTIFIED` |
| `breech_loading_artillery` | `monitor_tech` | Military -> Naval | `CROSS_BRANCH_JUSTIFIED` |
| `nitroglycerin` | `self_propelled_torpedoes` | Production -> Naval | `CROSS_BRANCH_JUSTIFIED` |
| `professional_civil_engineering` | `steel_frame_buildings` | Production -> Society | `CROSS_BRANCH_JUSTIFIED` |
| `electric_telegraph` | `telephone` | Military -> Production | `CROSS_BRANCH_JUSTIFIED` |
| `reinforced_concrete` | `concrete_dockyards` | Production -> Naval | `CROSS_BRANCH_JUSTIFIED` |
| `combustion_engine` | `military_aviation` | Production -> Military | `CROSS_BRANCH_JUSTIFIED` |
| `professional_civil_engineering` | `paved_roads` | Production -> Society | `CROSS_BRANCH_JUSTIFIED` |
| `political_agitation` | `war_propaganda` | Society -> Military | `CROSS_BRANCH_JUSTIFIED` |
| `combustion_engine` | `zeppelins` | Production -> Society | `CROSS_BRANCH_JUSTIFIED` |
| `pneumatic_tools` | `concrete_fortifications` | Production -> Military | `CROSS_BRANCH_JUSTIFIED` |
| `reinforced_concrete` | `concrete_fortifications` | Production -> Military | `CROSS_BRANCH_JUSTIFIED` |
| `steam_turbine` | `dreadnought_tech` | Production -> Naval | `CROSS_BRANCH_JUSTIFIED` |
| `radio` | `mass_propaganda` | Production -> Society | `CROSS_BRANCH_JUSTIFIED` |
| `war_propaganda` | `mass_propaganda` | Military -> Society | `CROSS_BRANCH_JUSTIFIED` |
| `military_aviation` | `carrier_tech` | Military -> Naval | `CROSS_BRANCH_JUSTIFIED` |
| `nitrogen_fixation` | `chemical_warfare` | Production -> Military | `CROSS_BRANCH_JUSTIFIED` |
| `compression_ignition` | `mobile_armor` | Production -> Military | `CROSS_BRANCH_JUSTIFIED` |

Every cross-branch edge has an explicit technical, institutional or doctrinal reason in the final edge audit.

## 9. Prerequisite-count distribution

| Prerequisites | Technologies |
|---:|---:|
| 0 | 1 |
| 1 | 76 |
| 2 | 29 |
| 3 | 5 |

Only five technologies retain three prerequisites: `conveyors`, `mass_propaganda`, `mobile_armor`, `battlefleet_tactics`, and `concrete_fortifications`. Their final edge rows separately justify each input. No technology has four or more prerequisites.

## 10. Family validation

All 36 TECH-4A families remain represented. The reconstruction favors direct sequences inside rail, telecommunications, electricity, steam, steel, materials, food, agriculture, military organization, fortifications, naval hulls/logistics/doctrine, finance, public health, mass media and psychology. Parallel ideological and specialist branches are allowed to terminate rather than being joined through false AND-gates.

## 11. Static validation

| Counter | Result |
|---|---:|
| `ACTIVE_TECHS` | 111 |
| `BROKEN_PREREQUISITE_REFERENCES` | 0 |
| `PREREQUISITE_CYCLES` | 0 |
| `LATER_ERA_PREREQUISITE_INVERSIONS` | 0 |
| `DUPLICATE_TECH_IDS` | 0 |
| `UNINTENDED_RESEARCHABLE_ROOTS` | 0 |
| `ACTIVE_PREREQUISITES_TO_COMPATIBILITY_ALIASES` | 0 |
| `ARBITRARY_EDGES_AFTER` | 0 |
| `WEAK_EDGES_AFTER` | 0 |
| `AVOIDABLE_DEAD_ENDS` | 0 |
| `ERA_CHANGES` | 0 |
| `UNLOCK_CHANGES` | 0 |
| `EFFECT_CHANGES` | 0 |
| `COST_CHANGES` | 0 |
| `CATEGORY_CHANGES` | 0 |
| `LOCALIZATION_CHANGES` | 0 |
| `GUI_CHANGES` | 0 |
| `ERA_I_VI_CHANGES` | 0 |

## 12. Historical spot checks

The highest-risk replacements were checked against institutional historical sources:

- National Science and Media Museum on glass photographic plates: https://blog.scienceandmediamuseum.org.uk/a-brief-guide-to-photographs-on-glass/
- National Air and Space Museum on aircraft propulsion and early aero engines: https://airandspace.si.edu/explore/stories/power-and-control-air
- Royal Museums Greenwich on steam turbines leading to HMS Dreadnought: https://www.rmg.co.uk/collections/objects/rmgc-object-67214

## 13. Runtime checklist

The user should verify:

- no visually absurd lines and no lines toward empty space;
- readable family progression through Eras VII-XII;
- `medical_degrees` -> `modern_nursing` renders correctly;
- no researchable technology is isolated without an incoming line;
- no TECH-3B alias or ghost card reappears;
- remaining terminals look intentional;
- normal progression reaches Era XII without unexpected gameplay behavior.

No runtime PASS is claimed.

**Final static status:** `TECH4C_POST1836_PREREQUISITE_GRAPH_STATIC_PASS_RUNTIME_PENDING`
