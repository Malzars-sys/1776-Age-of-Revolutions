# Issue 23 — economic reference audit, Hawk

**AUDIT_STATIC_COMPLETE_RUNTIME_PENDING — 8 November 2026.** Mission #23 was selected from the live Backlog column and moved to **In progress**. The maintainer expressly excluded #21; that mission, its scripts and its tracking are not modified here. This is a read-only audit of gameplay data, with a new repeatable audit tool and evidence. It is not an engine acceptance or an economic rebalance.

Audited local revision: `0396b1133168c1721b61cee5ae5334f1a4f5e4e1` (`beta hotfix stat and revolution`). Canonical executable version checked: **1.15.0**. No new game, engine session or market simulation was run by this agent.

## Results and practical limits

The effective-file model accounts for same-path mod masks, the descriptor's technology `replace_path`, and explicit `REPLACE` / `REPLACE_OR_CREATE` declarations. It inventories **77 same-path overrides**, **72 goods**, **134 buildings**, **273 PM groups** and **623 PM identifiers**. Definitions with multiple ordinary providers are reported rather than resolved by an assumed engine load order.

- **26,230 mod references checked; zero missing target identifiers.** Coverage: building groups, building/PM technologies, PM groups and methods, PM input/output goods, required input goods, law prerequisites, local PM prerequisites, state resource potentials and initial building/PM declarations.
- **Zero unsupported initial PMs** and **zero PM prerequisites absent from their host building's PM set** in this model.
- **39 explicit starting-trade state/good references resolve.** This does not establish ownership of every scoped state part, successful initialization, route profitability, market access or actual imports/exports.
- Native control: **18,181 references**, no missing or ambiguous target, no parse failure, and no unsupported initial PM/local prerequisite.
- Every good consumed by a building-reachable PM has at least one output PM in the all-date graph. This excludes a simple missing-producer-identifier dead end; it does not prove production in 1776, sufficient quantity, staffing, affordability or availability within a particular market.
- **278 audited source files retain their captured hashes** at the source check. Gameplay files, recipes, technology gates, ownership, population and map data were not written.

`MOD_REFERENCES.json`, `NATIVE_REFERENCES.json` and `OVERRIDE_INVENTORY.json` contain the actual scope and findings. The reference count includes repeated historical and state-resource uses; it is not a number of independent test cases or bugs. The graph's definition inventory and the older copper validator's technology-node count are different inventories, not contradictory engine measurements.

## Seven ordinary same-ID overrides: preserve intended TECH behavior

Seven references have multiple providers because these authored files coexist with an unmasked native file. Their payloads demonstrate deliberate changes; no wrong effective payload has been observed in the engine.

| IDs | Mod provider | Difference from native and consequence to verify |
| --- | --- | --- |
| `pmg_base_building_logging_camp` | `common/production_method_groups/99_tech_tree_wood_rework_pmgs.txt` | Adds `pm_organized_forestry` between simple forestry and sawmills. Verify the extra choice remains listed in game. |
| `pmg_train_automation_building_rubber_plantation` | `common/production_method_groups/99_tech_tree_wave3_causality_pmgs.txt` | Uses the building-specific steam rail PM rather than the generic native steam rail PM. Verify its intended gate and recipe. |
| Five `pm_home_workshops_building_subsistence_*` IDs: farm, orchard, pasture, fishing village and rice farm | `common/production_methods/99_tech_start_1776_subsistence_tools.txt` | Adds **0.10 tools per workforce-scaled level**, retaining the three native 0.25 outputs. Verify the mod's small tool supply actually loads; do not infer it from the filename alone. |

These are **seven duplicate-ID references, not seven reproduced gameplay failures**. No definition is deleted, renamed or copied from native in this pass. Any later explicit replacement/merge decision must preserve the authored PM lists, tool output, laws and technology graph, and coordinate the TECH interface. The current audit does not take over #21 or declare how the engine resolves ordinary duplicate objects.

## Copper and preserved custom chains

The delivered #31 native alignment is retained. Its scoped audit was run on the installed data: **155/155 checks**, all **six negative controls detected**. Native copper base price 40 and standard PM payloads pass their existing contract; the mod's deposits remain **675 states, 302 nonzero potentials, 5,924 potential mine levels across 16 files**. Those are potential levels, not constructed levels or weekly copper production.

`tools/tech6c5b_validate.py` also reports PASS, preserving the copper matrix and its 290-node graph check. The #31 protection snapshot reports three later differences outside its copper contract: the egalitarian objective journal, ideological movements and agitator election events. They are not changed by this audit, reclassified as copper failures or reverted.

The reference pass includes custom alloys/hardware, spices, refined fuels, chemicals and transport. It does not change their coefficients, prices, resource distribution, initial selections or employment. Their graph references resolve, which alone says nothing about whole-building profit or market balance.

## Ports, trade and representative cases

`COUNTRY_INFRASTRUCTURE.json` inventories initialization declarations for France, Great Britain, the USA, Russia, Prussia, the Netherlands (`NET`), Spain, the Ottoman Empire and China. Counts are explicitly **create-building records and declared ownership levels**, not employed levels or engine totals. Conditional initialization and the redistribution layer can change them; a declaration does not prove that the named country owns that state part at runtime.

The canonical [1.15 release notes (Dev Diary #196, 5 November 2026)](https://steamcommunity.com/app/529340/announcements/?l=french) describe the new cold effects and up to four world-market hubs per area. Therefore, counting ports or finding a valid input good cannot validate the new market connections. The actual regional hubs, seasonal access, convoy supply, route switching, trade-center activity and prices remain engine checks. No native 1836 trade or deposit distribution is imported into 1776.

## Repeat and continue

Run `python -B tools/compatibility/issue23_economy_reference_audit.py --output <new JSON path>` and repeat with `--native` for the control. The audit only writes the requested evidence JSON. Existing copper commands and actual results are recorded in `VALIDATION.json`; source protection details are in `SOURCE_PROTECTIONS.json`.

Issue #23 stays **In progress**, with the broad market-flow and visual acceptance criteria open. Use [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md) in the grouped engine pass. No human receipt, full compatibility claim, local Git metadata write, commit, push, branch switch, main merge or vanilla change is created by this lot. The #31/#33 deliveries and all other agents' work retain their status.
