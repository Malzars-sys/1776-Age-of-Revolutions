# TECH-1C-B — Tech & Res System Audit

Status: `INPUT_FOR_HUMAN_REVIEW` · `NOT_CANONICAL` · `NOT_IMPLEMENTED`

## Identity and method

Installed reference: `[1.13] Tech & Res`, Workshop `3472248460`, descriptor version literal `1.6'`, target `1.13.*`, path `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3472248460`. The descriptor declares no dependencies or `replace_path`.

Counts were obtained by parsing top-level database objects and overlaying their IDs on certified vanilla 1.13.9. “Added” means an ID absent from vanilla; injected/replaced vanilla IDs are not double-counted. Economic edges were extracted from every `goods_output_*` and `goods_input_*` modifier in Tech & Res PM definitions.

## Revalidated baseline

| Metric | Installed result | Prior approximate result | Explanation |
|---|---:|---:|---|
| Loaded technologies | 439 | 439 | 179 vanilla IDs + 260 added IDs |
| Tech definitions in mod files | 285 | — | 260 added + 25 overlapping vanilla IDs |
| Production techs loaded | 177 | — | category overlay |
| Society techs loaded | 144 | — | category overlay |
| Military techs loaded | 118 | — | category overlay |
| Eras | 11 | 11 | 5 vanilla IDs + 6 added IDs |
| Added goods | 39 | 39 | confirmed |
| Added buildings | 38 | 38 | confirmed |
| Added PMs | 601 | 601 | 689 unique mod PM IDs, 88 overlap vanilla |
| Added PMGs | 137 | 136 | installed version contains one more added ID than the old approximation |

The mod’s technology files contain 230 plain creates, 33 `REPLACE_OR_CREATE`, 14 `INJECT` and 8 `REPLACE` definitions. Two added technologies lack an explicit `ai_weight`: `hydrogen_bomb` and `nuclear_fusion_reactor`. The remaining 258 have explicit weights, but most are static or generic conditions rather than resource-aware planning.

## Goods architecture

The 39 new goods form several layers:

- primary/resource: water, copper, bauxite, common ores, advanced ores, rare earths, natural gas and uranium;
- industrial intermediates: alloys, aluminium, plastics, fuels, lubricant, wire, batteries, electronics, processors, robotics and AI systems;
- final/POP-facing: pharmaceuticals, appliances, televisions, cosmetics, software, communications, entertainment, print/music/instruments, civil planes and on-demand goods;
- knowledge/data: raw data, organized data and business data;
- strategic/military: space assets;
- national infrastructure: global electricity.

All omit `tradeable = no`, including `raw_data`, `organized_data`, `on_demand_goods` and `global_electricity`, whose `traded_quantity` is zero. A zero traded-quantity field is not the same as a proven non-tradable flag. This ambiguity is a runtime/schema risk.

`androids` has no producing or consuming PM relation in the installed files and is a dead-chain candidate. Other goods have at least a producer and consumer or POP need. The complete good/building inventory is in `TECH1C_TECH_RES_OBJECT_INDEX.csv`; all 1,447 extracted supply/demand endpoints are in `TECH1C_TECH_RES_CHAIN_INDEX.csv`.

## Resource potential system

Tech & Res assigns deposits through `common/scripted_effects/ztr_resource_creation_scripts.txt` rather than one static state-history file. `common/history/global/ztr_global.txt` calls `create_tech_and_res_resource_deposits` at initialization. That initial effect adds water classes, hydroelectric traits, copper and common-ore deposits to explicit state lists.

`on_acquired_technology_deposits` then adds once-per-world deposits using global variables:

| Technology | Added potential |
|---|---|
| `bauxite_processing` | bauxite mine potential |
| `quartz_glass` | advanced-ore potential |
| `verrier_modern_physics_tech` | uranium potential |
| `natural_gas_extraction` | natural-gas potential |
| `rare_earths` | rare-earth potential |

The technology `on_researched` blocks often contain only explanatory tooltips; the actual mutation is centralized in the technology on-action. This separation is reusable as an architecture: map knowledge, discovery timing and building availability remain distinct. It also creates global-order and save-migration risks; the global variable prevents repeated addition, but runtime validation must test old saves and simultaneous acquisition.

Once potential exists, corresponding buildings use normal resource-building logic. The mod adds desired/high-supply/export stances for many new resources, but does not add a general scripted “build every newly revealed resource” routine. AI success still depends on engine profitability, current/anticipated market demand, workforce and infrastructure.

For 1776 geology, the reusable concept is `technology/on-action → idempotent local effect → resource potential → normal building`. The explicit state lists and balance are mod-specific and must not be copied.

## Buildings, PMs and bootstrap

The 38 added buildings include six mines/rigs, water and power systems, intermediate factories, digital industries, airports, a research center and special strategic buildings. Some use large explicit `ai_value` values: research center and nuclear silo 50,000; digital industries around 2,000; several plants 1,600–2,500. Others rely on engine defaults and goods stances.

Representative bootstrap cases:

| Chain | First real cause | Classification | Risk |
|---|---|---|---|
| Copper → copper wire → electronics | copper potential at global init; downstream PM inputs; AI high-supply/export stances | `BOOTSTRAP_STARTING_RESOURCE` + `BOOTSTRAP_LATENT_DEMAND` | Engine must build first mine/factory |
| Bauxite → aluminium → aircraft/appliances | deposit appears on `bauxite_processing`; downstream tech/PM demand | `BOOTSTRAP_TECH_EVENT` | Global one-time discovery plus current-market AI |
| Natural gas → fuels/chemistry/power | deposit appears on extraction tech; multiple downstream PMs | `BOOTSTRAP_TECH_EVENT` + `BOOTSTRAP_LATENT_DEMAND` | Input/output timing |
| Pharmaceuticals | dedicated industry plus POP household/intoxicant/luxury uses | `BOOTSTRAP_POP_DEMAND` | Minimum luxury share 1% adds robust demand but needs balance |
| Raw/organized/business data | offices/datacenters produce; many digital PMs and research center consume | `BOOTSTRAP_LATENT_DEMAND` + strategy stance | zero traded quantity fields and ordering |
| Research center | AI-selectable decision → 24-month JE/site → high AI value; yearly JE forcibly creates it for AI if absent | `BOOTSTRAP_AI_SCRIPT` + `BOOTSTRAP_EVENT` | Highly scripted, non-generic |
| Androids | no PM producer/consumer found | `NO_BOOTSTRAP_FOUND` | dead chain |

Tech & Res avoids the no-supply/no-demand loop through a mixture rather than a single solution: POP needs, dense downstream PM demand, AI goods stances, explicit building values, starting/global deposit creation and special event/JE construction. This is effective breadth, but it is difficult to reason about and several chains remain engine-dependent.

## Research and knowledge loop

`building_research_center` is a non-expandable, government-only `bg_technology` building gated by modern physics and a `research_center_site` modifier. The site is obtained through a decision requiring literacy above 60%, bureaucracy above 1,000, an incorporated unsplit state, urban center 50 and university 5. The AI strongly prefers the decision under industrial expansion and will not take it at war.

The base/medium/advanced PMs consume data plus paper, prints, electronics, robotics, computers and AI systems, and produce innovation/education effects rather than a new research output good. Specialization PMs grant category research speed, spread or innovation cap. The construction JE includes an explicit yearly AI fallback that creates the building in the capital when the AI has not built it.

Data flow is broadly:

`universities/offices → business data` and `datacenters → raw/organized data` → `research center and digital/industrial optimization PMs` → innovation/research modifiers.

This is `TECH_RES_RESEARCH_LOOP_REUSABLE_AS_IDEA = PARTIAL`. Reusable: separate applied-research building, knowledge inputs, specialization PMs and an explicit bootstrap. Not reusable as-is: very high fixed inputs/employment, event-forced construction, mixed data semantics, and direct research-speed multipliers. 1776 should design a smaller, auditable Industrial Knowledge loop with explicit producers, sinks, tradability and AI ordering.

## Technology AI weights

Of 260 added technologies, 258 have `ai_weight`. Static classification of their AI blocks found 170 static, 43 economy-oriented conditional, 42 other conditional, 2 explicitly military conditional, 1 resource/market conditional and 2 absent. This is a token-based classification, not proof of runtime decisions.

The dominant pattern is a base `value` with contextual additions for strategy, development modifiers, country conditions or prerequisites. It does not implement the full target rules such as coal ownership increasing steam research, landlocked status reducing naval research, chemical shortages raising chemistry, or newly revealed deposits raising exploitation technologies. No `kai_*` call occurs inside added technology definitions.

## AI strategies and external dependency

Tech & Res replaces the resource, industrial and colonial-extraction administrative strategies and injects into the default strategy. These sections add stances for new goods and technology-gated wants. Exactly 62 calls to the external scripted trigger `kai_has_high_supply` occur in three strategy files/objects. The symbol is defined only by installed `Kuromi's AI` version 7.5 and tests whether a good is cheap enough before an export stance applies.

The descriptor does not declare Kuromi’s AI, so the relationship is a hidden script dependency. Evidence is direct and unambiguous:

- prefix: `kai_`;
- sole external symbol: `kai_has_high_supply`;
- definition: Kuromi `common/scripted_triggers/kai_scripted_triggers.txt`;
- explicit Tech & Res comment naming Kuromi AI;
- 62 call sites listed in `TECH1C_TECH_RES_EXTERNAL_CALL_INDEX.csv`.

Without Kuromi:

- `MOD_LOADS = YES` is the expected Paradox behavior for unresolved scripted triggers, but a runtime error-log test is still required;
- core technologies, buildings, PMs and economic relations remain defined;
- export-stance trigger clauses cannot function correctly;
- `AI_RESEARCH_FUNCTIONS = PARTIAL` because research weights are internal and independent;
- `AI_NEW_CHAINS_FUNCTION = PARTIAL` because internal stances/demand remain, but export gating and Kuromi’s PM/define changes are lost;
- `DEAD_CHAINS_EXPECTED = YES` at least for the already orphaned `androids`; additional weak chains are plausible.

Thus `TECH_RES_REQUIRES_AI_DEPENDENCY_TO_LOAD = NO` statically, while `TECH_RES_REQUIRES_AI_DEPENDENCY_FOR_FUNCTIONAL_ECONOMY = PARTIAL`. This is not a recommendation for 1776 to depend on Kuromi. All required behavior should be reimplemented locally and narrowly.

## Lessons for 1776

- Adopt the concept of idempotent technology-triggered resource discovery.
- Reimplement every map list, balance value and AI rule locally.
- Give every good a documented first producer, first consumer, tradability rule and recovery path.
- Prefer explicit small bootstraps over global high `ai_value` or forced yearly creation.
- Treat research goods as a closed, measured loop; avoid unexplained zero-trade settings.
- Add contextual technology weights from 1776’s actual resources, shortages, industrial base and naval geography.
- Add automated integrity tests for orphan goods, missing PMG links, absent AI weights and unresolved external symbols.

No gameplay file was changed and no third-party code, localization or asset was copied.
