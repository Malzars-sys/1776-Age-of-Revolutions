# TECH-4A — Post-1836 Technology Preparatory Audit

**Status:** `TECH4A_POST1836_PREPARATORY_AUDIT_COMPLETE`

## 1. Baseline and scope

- Repository branch: `technology-rework`
- Required baseline: `9f42434`
- Audited commit: `9f42434cef058bd9fd40330f9a597218c4e335fc`
- Working tree at phase start: clean
- Vanilla reference: Victoria 3 `release/1.13.11`
- Phase type: documentary audit only
- Gameplay, GUI, localization, history, setup, and compatibility implementation: untouched

This phase inventories and evaluates the active Era VII-XII technology graph. It does not implement the future TECH-4B chronology rebalance or TECH-4C prerequisite-graph changes.

## 2. Source resolution and audit method

The mod descriptor replaces both `common/technology/eras` and `common/technology/technologies`. Consequently, the active technology universe is resolved from the mod definitions; the vanilla 1.13.11 files are used to determine whether an ID is a mod override or a genuinely new technology.

The TECH-3B compatibility-alias register was used to exclude non-playable bridge aliases from the active research inventory. Prerequisite edges, successor counts, localization coverage, direct unlock references, era placement, conceptual families, graph roles, dead ends, and layout risks were then calculated from the effective working tree.

Chronology triage uses the following documentary date windows. These are audit heuristics, not engine-defined era dates:

| Era | Audit window |
|---|---:|
| VII | 1836-1859 |
| VIII | 1860-1879 |
| IX | 1880-1894 |
| X | 1895-1909 |
| XI | 1910-1922 |
| XII | 1923-1936 |

## 3. Active universe inventory

| Counter | Result |
|---|---:|
| Active Era VII-XII technologies | 111 |
| Researchable technologies | 110 |
| Legitimate non-researchable technologies | 1 (`sericulture`) |
| Mod overrides of vanilla IDs | 111 |
| Mod-new IDs | 0 |
| Vanilla-inherited active IDs | 0 |
| Compatibility aliases excluded | 38 |
| Missing English name entries | 0 |
| Missing French name entries | 0 |
| External direct unlock references | 205 |

All 111 inventoried technologies have a resolved English and French display name. `sericulture` is retained because it is a legitimate event/non-researchable technology, not a compatibility alias.

## 4. Density by era and branch

| Era | Production | Military | Naval | Society | Total |
|---|---:|---:|---:|---:|---:|
| VII | 5 | 0 | 0 | 5 | 10 |
| VIII | 11 | 6 | 3 | 11 | 31 |
| IX | 4 | 3 | 3 | 1 | 11 |
| X | 11 | 4 | 5 | 10 | 30 |
| XI | 3 | 2 | 1 | 4 | 10 |
| XII | 5 | 6 | 4 | 4 | 19 |

The graph alternates sharply between dense and sparse eras. Era VIII (31 nodes) and Era X (30 nodes) contain more than half of the post-1836 universe, while Eras VII, IX, and XI contain only 10-11 nodes each. Era VII has no active Military or Naval node, Era IX has only one Society node, and Era XII is weighted toward Military/Naval technologies (10 of 19). These are preparation findings for TECH-4B/4C, not automatic evidence that every uneven distribution is incorrect.

## 5. Graph structure

| Graph role | Count |
|---|---:|
| Root | 1 |
| Branch node | 26 |
| Merge node | 21 |
| Normal | 42 |
| Dead-end role | 21 |

There is one true in-universe root: `sericulture`, which is non-researchable and event-facing. Thirty-five Era VII-XII technologies enter from Era VI prerequisites. The graph contains 152 direct prerequisite edges.

The mutually exclusive graph-role count assigns `sericulture` the role `ROOT`. Under the separate dead-end definition (zero successors), it is also one of the 22 registered dead ends.

## 6. Dead-end register

| Classification | Count |
|---|---:|
| `JUSTIFIED_DEAD_END` | 7 |
| `LIKELY_MISSING_SUCCESSOR` | 12 |
| `POSSIBLE_BRANCH_TERMINAL` | 3 |
| **Total** | **22** |

Dead ends by era are: Era VII 3, Era VIII 3, Era IX 1, Era X 9, and Era XI 6. By branch they are: Production 10, Society 8, Naval 2, and Military 2.

The twelve likely missing-successor candidates are:

- `baking_powder`
- `modern_nursing`
- `mechanized_farming`
- `feminism`
- `pumpjacks`
- `war_propaganda`
- `submarine`
- `electric_railway`
- `radio`
- `behaviorism`
- `mass_propaganda`
- `paved_roads`

The three possible branch terminals are `landing_craft`, `multilateral_alliances`, and `zeppelins`. The detailed register records each node's unlock count, chronology, family, and recommendation; it does not prescribe implementation.

## 7. Prerequisite-edge audit

| Classification | Count |
|---|---:|
| `STRONG` | 93 |
| `PLAUSIBLE` | 19 |
| `WEAK` | 29 |
| `ARBITRARY` | 9 |
| `ANACHRONISTIC` | 0 |
| `CROSS_BRANCH_JUSTIFIED` | 2 |
| `CROSS_BRANCH_SUSPICIOUS` | 0 |
| **Total** | **152** |

The nine highest-priority arbitrary edges for TECH-4C review are:

| Prerequisite | Technology | Audit concern |
|---|---|---|
| `vulcanization` | `automatic_bottle_blowers` | Material processing is not a clear prerequisite for bottle-forming machinery. |
| `realism` | `camera` | An artistic movement is not a technical prerequisite for photography. |
| `military_aviation` | `dreadnought_tech` | Aviation is not a necessary precursor to dreadnought construction. |
| `monitor_tech` | `landing_craft` | Monitor warship design is not a necessary precursor to landing craft. |
| `handcranked_machine_gun` | `military_aviation` | Machine-gun development is not a sufficient conceptual gate for aviation. |
| `concrete_fortifications` | `mobile_armor` | Fortification construction is not a direct precursor to armored mobility. |
| `electrical_capacitors` | `pasteurization` | Electrical storage is not a necessary precursor to pasteurization. |
| `elevator` | `paved_roads` | Vertical transport is not a credible prerequisite for modern road paving. |
| `reinforced_concrete` | `plastics` | Structural concrete is not a direct precursor to polymer chemistry. |

These classifications are documentary judgments. The edge CSV retains the current graph and supplies a reason and recommendation for every audited edge.

## 8. Cross-branch edges

Five edges cross the assigned conceptual branches:

| Prerequisite | Technology | Branch transition | Result |
|---|---|---|---|
| `optical_telegraph_networks` | `electric_telegraph` | Society -> Military | `STRONG` |
| `medical_degrees` | `modern_nursing` | Society -> Military | `STRONG` |
| `professional_civil_engineering` | `steel_frame_buildings` | Society -> Production | `CROSS_BRANCH_JUSTIFIED` |
| `breech_loading_artillery` | `monitor_tech` | Military -> Naval | `CROSS_BRANCH_JUSTIFIED` |
| `military_aviation` | `dreadnought_tech` | Military -> Naval | `ARBITRARY` |

No edge was classified `CROSS_BRANCH_SUSPICIOUS`; the one problematic cross-branch edge is already classified more strongly as `ARBITRARY`.

## 9. Concept-family matrix

The 111 technologies are assigned to 36 families, with no unassigned node. Families cover food processing, steel, explosives, steam systems, agriculture, materials, civil construction, factory organization, extraction, combustion, railways, electricity, telecommunications, artillery, military organization, fortifications, naval logistics, naval hulls, naval weapons, naval doctrine, medicine, infantry weapons, amphibious warfare, aviation, armor, nationalism/imperialism, arts/media, sports, public health, political ideologies, rights, administration/surveillance, finance, philosophy/psychology, urban infrastructure, and mass politics/media.

The family matrix records the current sequence, missing links, over-dependencies, chronology gaps, and a recommendation of either `KEEP` or `RELAYOUT_FAMILY`. It is a planning document and does not change positions or prerequisites.

## 10. Chronology audit

| Era-fit result | Count |
|---|---:|
| `GOOD` | 68 |
| `BORDERLINE` | 16 |
| `TOO_EARLY` | 3 |
| `TOO_LATE` | 24 |
| `REVIEW_REQUIRED` | 0 |

Technologies assessed as too early for their current era:

- `steam_donkey`
- `corporatism`
- `steel_frame_buildings`

Technologies assessed as too late for their current era:

- `aniline`
- `arc_welding`
- `bolt_action_rifles`
- `chemical_warfare`
- `compression_ignition`
- `concrete_fortifications`
- `destroyer`
- `dough_rollers`
- `electric_railway`
- `electric_telegraph`
- `elevator`
- `flamethrowers`
- `mobile_armor`
- `monitor_tech`
- `nco_training`
- `pasteurization`
- `paved_roads`
- `romanticism`
- `rubber_mastication`
- `sericulture`
- `stormtroopers`
- `telephone`
- `vulcanization`
- `wargaming`

The `sericulture` result reflects its ancient historical maturity relative to the Era VII audit window. Because it is an event/non-researchable root, that flag does not by itself recommend moving it into the normal research progression.

## 11. Layout and position preparation

The active definitions contain no explicit technology coordinates, so exact card overlap and line crossing cannot be measured statically. All 111 positions are therefore recorded as `NOT_EXPLICIT_AUTO_LAYOUT`. The family recommendations produce 46 `KEEP` and 65 `RELAYOUT_FAMILY` records.

Principal layout risks for later implementation and runtime inspection are:

- empty Military and Naval Era VII columns;
- alternating dense and sparse era columns;
- a single Society node in Era IX;
- 22 pre-final-era zero-successor endpoints, which can appear isolated;
- high fan-in nodes such as `dreadnought_tech` (four prerequisites), and `conveyors`, `trench_works`, and `political_agitation` (three each);
- long paths created by arbitrary or cross-branch edges, especially `military_aviation` -> `dreadnought_tech`.

No coordinates are proposed in TECH-4A.

## 12. Compatibility-bridge preservation

All 38 TECH-3B compatibility aliases are excluded from the playable Era VII-XII inventory and remain untouched. The audit includes the active target technologies referenced by those bridges, but makes no changes to bridge IDs, prerequisites, localization, or post-1836 compatibility logic.

## 13. Priorities for TECH-4B

Recommended chronology/density priorities, in order:

1. Review the 27 `TOO_EARLY`/`TOO_LATE` placements against gameplay pacing and the intended 1836-1936 progression.
2. Address the Era VIII and Era X concentration without assuming that equal era sizes are required.
3. Review the absence of Era VII Military/Naval entry nodes and the single-node Society Era IX column.
4. Treat `sericulture` separately as an event/non-researchable technology.
5. Preserve IDs, unlock behavior, and compatibility bridges while evaluating any era moves.

## 14. Priorities for TECH-4C

Recommended graph/layout priorities, in order:

1. Review the nine `ARBITRARY` prerequisite edges.
2. Review the 29 `WEAK` edges and the twelve likely missing-successor nodes.
3. Re-evaluate branch continuity using the 36-family matrix before changing individual edges.
4. Reduce avoidable long cross-family paths and high-fan-in congestion.
5. Runtime-test the automatic layout after each bounded family-level change; static analysis cannot confirm crossings or truncation.

## 15. Documentary observations and limits

- Chronology and semantic classifications are preparatory recommendations, not implemented changes.
- Unlock counts measure direct references in the effective `common` data and do not replace runtime validation.
- Automatic layout prevents exact coordinate or crossing validation from source alone.
- The resolved localization inventory records `dreadnought_tech` as English “Dreadnought” and French “Frégate”. This is documented for a future localization review only; TECH-4A does not alter it.
- No runtime PASS is claimed by this audit.

## 16. Deliverables

- `TECH4A_POST1836_TECHNOLOGY_INVENTORY.csv` — one row per active technology.
- `TECH4A_POST1836_PREREQUISITE_EDGE_AUDIT.csv` — one row per current direct prerequisite edge.
- `TECH4A_POST1836_TECH_FAMILY_MATRIX.csv` — family-level sequencing and layout preparation.
- `TECH4A_POST1836_DEAD_END_REGISTER.csv` — all Era VII-XI zero-successor nodes.
- `TECH4A_POST1836_PREPARATORY_AUDIT_REPORT.md` — methodology, findings, and future priorities.

## 17. Scope confirmation

- Gameplay files changed: **0**
- GUI files changed: **0**
- Localization files changed: **0**
- History/setup files changed: **0**
- Technology definitions changed: **0**
- Compatibility aliases changed: **0**
- Commits or pushes performed: **0**

**Final static status:** `TECH4A_POST1836_PREPARATORY_AUDIT_COMPLETE`
