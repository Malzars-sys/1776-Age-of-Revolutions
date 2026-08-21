# TECH-1C — External Economy, Resource & AI Reference Audit

Status: `INPUT_FOR_HUMAN_REVIEW` · `NOT_CANONICAL` · `NOT_IMPLEMENTED`

## 1. Executive Summary

All three installed references were found and audited. La Gabelle implements one tradable staple salt good from coastal salt pans and shaft-gated salt mines, then injects it into two POP needs, ten industrial PMs and two mobilization options. Its mandatory 5% luxury-food share, low initial exploitation, taxes and secondary demand can compound, but the scripts do not prove that salt alone causes famine; the path is indirect through aggregate food security.

Tech & Res loads an overlay of 439 technologies across 11 eras and adds 39 goods, 38 buildings, 601 PMs and 137 PMGs. Its economy uses 1,447 extracted new-good supply/demand endpoints, technology-triggered resource discovery, market stances, POP demand, explicit AI values and special event/JE bootstraps. `androids` is orphaned.

Tech & Res makes 62 hidden calls to `kai_has_high_supply`, defined by Kuromi’s AI 7.5. This dependency guards export stances; it is not required to define/load the economic objects, but it materially affects AI behavior. Kuromi improves current-market building/PM behavior and controlled PM experimentation; it does not implement a general future-demand or chain-ordering planner.

The 1776 target should reimplement narrowly: explicit per-chain bootstrap, idempotent resource discovery, contextual research weights, shortage/import recovery, bounded PM experiments and runtime observability. No external mechanism is canonical.

## 2. Installed Mod Identification

| Mod | Path | Workshop ID |
|---|---|---:|
| La Gabelle | `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3715913236` | 3715913236 |
| [1.13] Tech & Res | `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3472248460` | 3472248460 |
| Kuromi's AI | `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3227982912` | 3227982912 |

## 3. Versions / Dependencies

La Gabelle is 1.0.2; Tech & Res stores version literal `1.6'`; Kuromi’s AI is 7.5. All target 1.13.*. All metadata relationship arrays are empty and no `replace_path` is declared. The actual Tech & Res → Kuromi relationship is proven only by scripts/comments and installed symbol resolution. The launcher database contains Tech & Res followed by Kuromi at positions 0 and 1 in the disabled playset `tech et res`; La Gabelle has no launcher row, and none of the three appears in the active playset `hhhh`. This is load-order evidence, not proof of an active runtime configuration.

## 4. Methodology

The audit parsed installed descriptors, top-level objects, resource effects, building history, population history, PM input/output modifiers, strategy calls and localization/assets. It overlaid IDs against certified vanilla 1.13.9 at `C:/Games/Victoria 3/game`. Static capacity assumes full employment/inputs; engine-hidden POP purchase formulas are explicitly `UNKNOWN`. Existing TECH-1A/1B and 1776 technology baselines were read but not modified.

## 5. La Gabelle Architecture

The implemented graph is `potential → pan/mine → PM → salt → POP/industry/military`, with tax, event, company and prestige side systems. Solar and rock sources produce the same good. No salt-specific law, institution, decree, decision, state trait or map mode exists.

## 6. Salt Resource Map

There are 159 state regions: 97 solar, 64 rock, two with both. World totals are 2,526 solar and 1,209 rock. The map CSV preserves vanilla 1836 owners, split states, starting buildings and current/max capacity estimates.

## 7. Salt Supply

Salt pans output 10 per fully employed level with no inputs and no upgrade. Mines output 20 current, 50 representative mid and 75 max when equipment/explosives PMs are combined. Full-world theoretical ceilings are 49,440, 85,710 and 115,935. Starting-history capacity is about 2,320, with a duplicated Uralsk mine entry requiring runtime verification.

## 8. Salt Demand

Direct demand comes from basic and luxury food. Six food PMs add 10–30 salt/level; four chemical PMs add 5–20; two mobilization options add 0.5/1 engine-scaled upkeep. Direct POP units and world totals cannot be derived without runtime wealth/substitution data.

## 9. POP Need Behavior

Basic food: weight 1, max 20%, min 0. Luxury food: weight 0.5, max 15%, min 5%. The ordinary basic weight and zero minimum contradict a simple “unavoidable 20% basic salt” reading. The luxury minimum is unavoidable for eligible POP needs and should not be reused as-is.

## 10. China Salt Stress Test

CHI population is 366,405,602 in both certified vanilla and the project history. CHI has 179 solar and 102 rock potential; 42 pan and 9 mine starting levels yield 600 current capacity. Full exploitation gives 3,830 current, 6,890 mid and 9,440 max. Demand and self-sufficiency are `UNKNOWN`; static result is `PARTIAL/INCOMPLETE` and runtime validation is required.

## 11. World Salt Stress Test

Certified vanilla population is 1,022,466,685; 1776 history totals 1,015,483,064. Supply ceilings are known, demand is not. `WORLD_SALT_SUPPLY_SUFFICIENT = UNKNOWN`.

## 12. Famine Risk

Vanilla 1.13.9 food security drives starvation below 0.4 and severe starvation below 0.2; state famine uses 35% starving or 15% severe. La Gabelle defines no salt-specific trigger. Salt can affect the aggregate basic-food calculation, so classification is `INDIRECTLY`. Abundant substitutes should mitigate it, but only runtime measurement can confirm engine allocation.

## 13. La Gabelle Companies / Laws / JEs

Six salt companies exist; none is Chinese. Simplified-Chinese localization is not a company definition. The MP1 prestige JE uses company prosperity and top-three salt rank. France’s Gabelle JE applies tax/SoL modifiers. The reform event appears unreachable normally because it requires the variable it is meant to set. No salt law exists.

## 14. La Gabelle AI

No strategy, building value or research AI is added. Vanilla construction, PM and trade logic is used; companies alone have explicit `ai_will_do`. This does not prove timely exploitation in China or other large markets.

## 15. Tech & Res Baseline

Loaded: 439 technologies (177 production, 144 society, 118 military), 11 eras. Added: 260 techs, 39 goods, 38 buildings, 601 PMs, 137 PMGs. The prior PMG estimate of 136 is off by one in the installed version.

## 16. Tech & Res Goods

Goods cover geological resources, metals, chemicals/fuels, electrical/electronic chains, consumer goods, digital services/data, research inputs and strategic outputs. Zero `traded_quantity` is used without explicit `tradeable = no` for several goods. `androids` has no PM edge and is a dead-chain risk.

## 17. Tech & Res Buildings / PMs

The 38 buildings span extractors, power, heavy/light/digital industry, transport, research and special facilities. The PM graph is dense and often modifies vanilla buildings. AI support varies from engine default to high `ai_value`; all links still need load/runtime PMG validation.

## 18. Tech & Res Resource Potential System

Initialization adds water, hydro, copper and common ores through centralized effects. Acquisition of bauxite processing, quartz glass, modern physics, gas extraction and rare earths triggers idempotent global deposit additions. The architecture is reusable; state lists and values are mod-specific.

## 19. Tech & Res Research System

Research Centers are government-only, site-gated buildings. They consume data, paper, prints, electronics, robotics, computers and AI systems for innovation/education/research modifiers. A decision/JE selects the site; a yearly AI fallback creates the building. The loop is conceptually useful but over-scripted for direct adoption.

## 20. Tech & Res AI Calls

Exactly 62 external calls target only `kai_has_high_supply`. They occur in Tech & Res resource expansion, industrial expansion, colonial extraction and injected default-strategy content. No added technology body calls KAI.

## 21. AI Dependency Identity

Kuromi’s AI 7.5 is a broad AI overhaul, not a narrow Tech & Res addon. It changes economy, politics, diplomacy, laws, institutions, military/naval targets and selected technologies.

## 22. AI Dependency Building Logic

It changes building scoring constants and goods stances, and injects explicit values for administration, construction and statues. Most selection remains current-price/profitability engine logic. No generic multi-step forecast exists.

## 23. AI Dependency PM Logic

It lowers PM base score, allows temporary shortages at a 0.95 factor, reduces stickiness, rewards shortage relief and adjusts military/favored goods. This permits first-demand experiments and rollback, but does not guarantee upstream-first ordering.

## 24. AI Dependency Resource Logic

Resource strategies and current prices influence engine scoring. `kai_has_high_supply` protects domestic supply before export. It does not enumerate unexploited potential or strategically build arbitrary new resource types.

## 25. AI Dependency Trade Logic

Trade influence is through goods stances and export guards. No direct route-size/creation algorithm replacement was found. Salt is absent, so Chinese salt imports remain unguaranteed.

## 26. AI Dependency Research Logic

Five vanilla technologies get priority injections. There is no general resource/shortage/geography-aware research planner. Tech & Res’s extensive weights are its own.

## 27. AI Dependency Company Logic

No company files or company AI changes exist. `NOT_MODIFIED`.

## 28. Bootstrap Case Studies

Copper uses initial potential plus downstream demand; bauxite/gas use technology events; pharmaceuticals use POP demand; digital/data chains use stances and dense PM sinks; Research Centers use decision/JE/AI fallback; androids have no bootstrap. Mechanisms found: `STARTING_RESOURCE`, `TECH_EVENT`, `POP_DEMAND`, `LATENT_DOWNSTREAM_DEMAND`, `STRATEGY_STANCE`, `EXPLICIT_AI_VALUE`, `AI_SCRIPT`, `EVENT_JE`, and `NO_BOOTSTRAP_FOUND`.

## 29. External Dependency Necessity

Tech & Res is expected to load without Kuromi because no descriptor dependency exists and only trigger calls are unresolved. Its functional economy is `PARTIAL` without Kuromi: objects and internal weights remain, while 62 export guards and Kuromi’s global PM/building behavior disappear. Runtime error-log verification is required.

## 30. Comparative Matrix

The detailed matrix is `TECH1C_EXTERNAL_MOD_COMPARISON.csv`. Vanilla supplies engine foundations; La Gabelle demonstrates a compact commodity; Tech & Res demonstrates breadth and discovery/bootstrap mixtures; Kuromi demonstrates scoring changes. 1776 must implement only reviewed local concepts.

## 31. Lessons for Salt

Prefer salt primarily as food-processing/chemical/military input, or direct POP use with zero minimum and a small cap. Separate solar/rock production architecture is useful. Never accept a salt design before China/world food-security tests.

## 32. Lessons for Industrial Chemicals

Use explicit primary feedstocks, intermediate chemicals, multiple industrial sinks and safety/environment technologies. Register the first demand cause and AI shortage response. Avoid a new chemical that exists only as a PM output.

## 33. Lessons for Geological Resources

Use evidence-backed maps, idempotent tech discovery, explicit building registration and AI recognition tests. Potential is not supply; track construction, employment, inputs and infrastructure separately.

## 34. Lessons for Research Centers / Industrial Knowledge

Separate universities/basic education from applied centers. Industrial buildings should produce a clearly defined knowledge/records good; centers should consume it with bounded demand. Build upstream first, define tradability, and avoid annual forced creation as normal AI behavior.

## 35. 1776 AI Requirements

The independent specification in `TECH1C_1776_AI_REQUIREMENTS.md` defines 30 capabilities across research, resources, chains, PMs, trade, food safety, applied research, TECH-1B naval support, companies and observability.

## 36. Reuse / Adapt / Reject Decisions

Adopt concepts: dual salt sources, technological mine ladder, idempotent discovery, chain registry, controlled PM experiments, domestic-supply export guard and applied research separation. Adapt: industrial/military salt demand, data loops, desired goods stances and event bootstraps. Reject: mandatory luxury salt minimum, hidden dependency, orphan goods, ambiguous trade settings, huge unexplained AI values and forced yearly construction as normal design.

The 22-row comparison inventory contains 5 `ADOPT_CONCEPT`, 8 `REIMPLEMENT_LOCALLY`, 7 `ADAPT`, 2 `REJECT`, and 0 `NEEDS_RUNTIME_TEST` decisions. The zero in the last category means no reuse decision is deferred; it does **not** remove the runtime validations listed in section 37.

## 37. Runtime Tests Still Required

Fresh 1836/1776 starts; error log with and without Kuromi; salt food-security/wealth purchases; China/world demand; solar/rock AI construction; Food Industries and chemicals; mobilization; imports; resource discovery/save migration; PM experiments/rollback; five chain bootstrap cases; Research Center ordering; long hands-off research; TECH-1B naval supply/research.

## 38. Final Verdict

`TECH_1C_EXTERNAL_ECONOMY_AI_AUDIT = PASS` as a static reference audit. It is ready for human review, not implementation. Static China/world tests are intentionally partial because hidden engine formulas prevent defensible numeric demand and self-sufficiency values. Gameplay changes: 0. Third-party code/assets copied: 0.
