# TECH-1C-C — Kuromi's AI Dependency Audit

Status: `INPUT_FOR_HUMAN_REVIEW` · `NOT_CANONICAL` · `NOT_IMPLEMENTED`

## Identity

The installed dependency actually called by Tech & Res is `Kuromi's AI`, Workshop `3227982912`, version `7.5`, target `1.13.*`, path `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3227982912`. Its metadata declares no relationships or `replace_path`. The package/README identity implies author “Kuromi”; no separate author field is present.

Dependency proof does not rely on memory: Tech & Res contains 62 calls to `kai_has_high_supply`, a comment explicitly names Kuromi AI, and the installed Kuromi package is the only audited source defining that trigger. Both descriptors omit the relationship, making it a hidden content/load-order dependency.

## Architecture inventory

Kuromi’s AI contains:

- one full `ai_strategy_default` definition in the same relative file as vanilla;
- six replaced administrative strategies;
- eight injected diplomatic and eight political strategy objects;
- three building injections;
- one `NAI` define block;
- five script values plus three replacements of army/marines/navy targets;
- two scripted triggers;
- five research-tech injections;
- five ship-type injections;
- eleven law files with 26 injected laws;
- modifier-value injections, treaty/diplomatic action changes and two Meiji button injections.

No scripted effects, company types or company-charter logic are present. It is not exclusively economic: politics, diplomacy, institutions, laws, army/navy sizing, ship choices and country-specific content are also changed.

## Vanilla 1.13.9 diff

`common/ai_strategies/00_default_strategy.txt` is a 8,739-line full object replacing vanilla’s 8,790-line object; line similarity is 97.4%. This is an override even though `replace_path` is absent. The README/changelog confirms the switch to full-file modification in 7.4 because `subsidies` and `fleet_compositions` were not injectable.

The principal implementation methods are:

- `OVERRIDE`: default strategy and knowledge-sharing file collisions;
- `REPLACE`: administrative strategies and wanted military size values;
- `INJECT`: buildings, laws, tech weights, ship types, modifier valuations and strategy additions;
- `DEFINE_CHANGE`: construction, production-building and PM evaluation constants;
- `SCRIPTED_AUXILIARY_LOGIC`: market-supply and institution-affordability helpers.

No `replace_path` is declared.

## Building and construction AI

Most building selection remains engine-driven: candidate profitability/output value, desired goods stances, price, workforce, infrastructure and `ai_value`. Kuromi changes the scoring constants and strategy context rather than scripting a universal construction queue.

Only government administration, construction sectors and power-bloc statues receive explicit building injections. Government administration placement uses tax-capacity usage/capacity ratios; construction sectors get a bonus in populous states with iron potential. Resource and industrial strategies modify goods stances, which then feed the engine’s building evaluation.

Expected profitability and current output prices remain central. There is no general multi-step forecast that calculates future downstream demand. Future-oriented behavior is limited to declared `wants_*` stances, technology gates and the PM experiment mechanism.

## PM selection AI

Kuromi’s most relevant new-chain change is in defines. It lowers the PM base score, weakens employment and favored-output distortions, and changes the penalty for a candidate PM creating shortages to 0.95. Because an absent good has no market price, the untradeable expensive-input penalty does not fire initially. This lets the AI activate a PM that creates the first demand for a new good. If supply never appears, reduced stickiness allows a later reversal.

The AI can therefore:

- activate a PM that creates demand: `YES`, via less punitive shortage scoring;
- wait for upstream supply before downstream: `PARTIAL`, current shortage/price discourages bad choices but does not enforce ordering;
- build upstream before downstream: `PARTIAL`, goods stances/current prices can prioritize upstream but no topological planner exists;
- exit an input shortage: `PARTIAL/YES`, shortage-relief factor 5 and lower stickiness help.

This is controlled experimentation, not anticipation of an entire future chain.

## Resource extraction AI

There is no function that enumerates all unexploited resource potentials. Resource buildings are scored through the vanilla engine, desired/high-supply stances and current price. `kai_has_high_supply` only decides whether an export stance is safe; it does not detect or build deposits. Workforce, infrastructure, colonies and profitability remain engine inputs.

Consequently new potential added by technology is usable only if the building is correctly registered and demand/stance makes it competitive. Poor but strategic states receive no generic special treatment. This is insufficient as the sole 1776 solution for salt, copper, industrial minerals, phosphates or petroleum.

## Trade AI

Kuromi changes goods stances in the default/admin strategies and prevents export-oriented strategies from overriding domestic high-supply objectives while a good is expensive. No direct replacement of trade-route creation/size algorithms was found. Imports remain governed by engine behavior plus wants/import stances.

Salt is absent from Kuromi’s scripts and La Gabelle supplies no compatibility strategy. Therefore a Chinese salt shortage may trigger generic vanilla trade responses, but this dependency provides no salt-specific guarantee of sufficient imports. Runtime validation is required.

## Research AI

Only five vanilla technologies receive injected weights: atmospheric engine, mechanical tools, steam turbine, radio and telephone. The first gains an industrial/resource-strategy condition; the other four are static priority boosts. The system does not inspect owned coal, hydro potential, current shortages, unbuilt new industries, landlocked status, navy ambition or sector-specific market prices in a general way.

Tech & Res’s 260 added technology weights are internal to Tech & Res and do not call Kuromi. Kuromi improves several prerequisite orderings but is not a generalized research planner for an extended tree.

## Company AI

`AI_COMPANY_LOGIC = NOT_MODIFIED`. No company or charter file exists. Company creation, choices, expansion, prosperity and prestige goods remain vanilla/mod-specific. La Gabelle companies receive no special Kuromi support.

## Construction bootstrap conclusions

The dependency’s reusable conceptual mechanisms are:

1. allow a low-risk PM experiment to create initial demand;
2. penalize persistent expensive/untradeable shortages;
3. make PM reversal possible;
4. declare desired/high-supply goods by strategy and technology;
5. protect domestic supply before adopting export stances.

Missing mechanisms for 1776 are a chain graph, multi-step upstream/downstream ordering, newly unlocked potential queue, explicit strategic imports, contextual extended-tech research and company support.

## Dependency necessity for Tech & Res

The 62 unresolved calls affect only export guards in three Tech & Res strategy objects. The database does not use Kuromi symbols for buildings, PMs, goods, resources, events or technology definitions.

Static verdicts:

- `MOD_LOADS = YES_EXPECTED`, with an error-log runtime test required;
- `GAMEPLAY_FUNCTIONS = PARTIAL` without Kuromi;
- `AI_RESEARCH_FUNCTIONS = YES/PARTIAL` because Tech & Res owns its weights;
- `AI_NEW_CHAINS_FUNCTION = PARTIAL`;
- `DEAD_CHAINS_EXPECTED = YES` (at least the orphan `androids`, independent of Kuromi).

For 1776, dependency code should not be copied and the mod should not become dependent on Kuromi. Reimplement only the narrow behaviors justified by local runtime tests.
