# TECH-1C-D — Independent AI Requirements for 1776

Status: `INPUT_FOR_HUMAN_REVIEW` · `NOT_CANONICAL` · `NOT_IMPLEMENTED`

## Purpose

This specification states what the 1776 AI must be able to do. It does not create a dependency on La Gabelle, Tech & Res or Kuromi’s AI and does not prescribe copying their scripts. All implementation must be local, minimal and validated against Victoria 3 1.13.9.

## Core design contract

Every added economic chain must register:

`unlock technology → potential/producer building → available PM → output good → first consumer → mature consumers → AI bootstrap → shortage recovery → overproduction brake → trade policy`.

A chain fails review if any link is absent or relies only on a comment/localization. Every new good must have explicit tradability, price, producer, sink, first-demand cause and runtime test.

## Critical requirements

| ID | Priority | Capability | Required inputs | Acceptance criterion | Failure prevented |
|---|---|---|---|---|---|
| AI-TECH-01 | P0 | Research every new technology | prerequisites era ahead penalty country state | In a long hands-off test each eligible tech can be selected; no zero/absent weight makes it unreachable | dead technologies |
| AI-TECH-02 | P0 | Contextual research weights | resources prices shortages buildings literacy universities strategy | Coal/iron/mineral/naval/agricultural contexts measurably change relevant rankings without overriding prerequisites | static one-size research |
| AI-TECH-03 | P0 | Respect geography | coast landlocked rivers hydro resource potential | Landlocked countries suppress maritime weights; major coasts/navies raise navigation/naval architecture; hydro-rich coal-poor countries value hydraulic alternatives | irrational research |
| AI-TECH-04 | P1 | Safety and mortality research | workplace mortality pollution accident modifiers | Persistent elevated mortality raises safety/medical technology value | ignored social cost |
| AI-RES-01 | P0 | Detect newly unlocked potential | on-acquired-tech event potential type amount states | Within a bounded interval an eligible AI recognizes and can queue the new extractor | undiscovered/dead resource |
| AI-RES-02 | P0 | Select extraction states | price potential infrastructure workforce market access strategic status | Chosen state is viable or explicitly strategic; AI does not blindly choose largest potential | unstaffed mines |
| AI-RES-03 | P0 | Build all new resource types | resource-building registry | Salt copper industrial minerals chemicals/phosphates/petroleum candidates each pass a first-building test | unsupported custom type |
| AI-RES-04 | P1 | Avoid resource overproduction | current demand price reserves utilization exports | Expansion stops when price/utilization crosses a defined low-demand threshold | infinite low-price expansion |
| AI-CHAIN-01 | P0 | Bootstrap before mature demand | chain graph future downstream unlocks first PM | AI can create one upstream level and one downstream demand source in correct order under an empty market | no supply/no demand loop |
| AI-CHAIN-02 | P0 | Activate chain-creating PMs | PM profitability shortage risk technology input availability | AI may perform a bounded experiment when an input is absent and can roll it back if supply does not appear | permanent deadlock or self-harm |
| AI-CHAIN-03 | P0 | Sequence upstream/downstream | explicit dependency graph | Test logs show upstream capacity before or concurrently with downstream activation | cascading shortages |
| AI-CHAIN-04 | P0 | Recover from shortages | price shortage ratio potential imports PM alternatives | AI chooses at least one effective action: expand supply switch PM import or reduce demand | persistent shortages |
| AI-CHAIN-05 | P0 | Detect orphan objects | parsed database graph | CI/static audit reports zero producer zero consumer missing PMG and absent building links | android-like dead goods |
| AI-PM-01 | P0 | Choose all custom PM groups | PMG membership technology inputs outputs labor | Every custom PM appears in an AI decision test and can be selected when economically dominant | unused PMs |
| AI-PM-02 | P1 | Account for employment/infrastructure | qualifications workforce infrastructure | AI avoids a technically profitable PM that cannot staff or connect its inputs | paper profitability |
| AI-TRADE-01 | P0 | Import missing new goods | tradability market access price shortage strategic value | AI creates/expands an import when domestic supply cannot meet a material shortage and a foreign source exists | geographic famine/dead industry |
| AI-TRADE-02 | P0 | Protect strategic domestic supply | domestic price shortage military/food role | Export posture is suppressed while the domestic good is expensive or scarce | exporting through shortage |
| AI-TRADE-03 | P1 | Support temporarily unprofitable strategic imports | food security military readiness critical downstream | AI may accept bounded loss for an essential good and exits when no longer needed | market-only blindness |
| AI-FOOD-01 | P0 | Prevent single-minor-good famine | basic-food share caps substitutes food security | Removing salt alone while calories remain abundant never creates mass famine in benchmark markets | salt famine |
| AI-FOOD-02 | P0 | Balance salt demand | POP need food industry chemistry military | Direct POP demand is small/zero-minimum; industry is primary sink; stress tests remain stable in China | oversized mandatory demand |
| AI-FOOD-03 | P0 | Monitor food-security thresholds | food security starvation share severe share | Automated tests record thresholds and attribute which need caused deterioration | hidden famine path |
| AI-RESEARCH-01 | P0 | Build future Research Centers | literacy urban/university prerequisites knowledge supply budget | Qualified AI obtains a center without forced annual spawning and can staff/supply it | inaccessible applied research |
| AI-RESEARCH-02 | P0 | Sustain Industrial Knowledge loop | technical records/knowledge producers and center sinks | At least one producer precedes center activation; supply/demand stay bounded over 20 years | knowledge deadlock |
| AI-RESEARCH-03 | P1 | Separate university and applied roles | education innovation spread applied research | Universities remain education/basic science; centers consume industrial knowledge for applied effects | duplicated building roles |
| AI-NAVY-01 | P0 | Research naval technologies contextually | coast fleet ambition shipyards rivals resources | Major navies prioritize navigation/architecture; landlocked minors do not | naval misresearch |
| AI-NAVY-02 | P0 | Build and supply TECH-1B ships | designer objects naval bases crews inputs supply ships | AI fields legal designs and maintains crews/supply without persistent strategic-good shortage | unusable naval tree |
| AI-NAVY-03 | P1 | Coordinate naval industry | ship technologies PMs armaments engines fuels ports | Ship demand causes the right upstream PM/building response | isolated naval unlocks |
| AI-COMPANY-01 | P2 | Support relevant companies | building levels location prosperity charters | Company choice never serves as the only bootstrap for a core good | company dependency |
| AI-OBS-01 | P0 | Explain decisions in audit logs | selected tech/building/PM/trade action and scores | Runtime harness records first cause and alternatives for each representative chain | unreviewable behavior |
| AI-OBS-02 | P0 | Versioned regression suite | 1.13.9 static and hands-off scenarios | China/world salt plus five industrial chains have reproducible baselines | balance regressions |

## Required situational research rules

At minimum, local weights must support these relationships without hard-locking research:

- coal/iron and mining base → steam, pumps, metallurgy and mine-safety weights increase;
- coal-poor plus river/hydro potential → waterpower/hydraulic/electrical alternatives increase;
- major navy, long coast, shipyards or maritime strategy → navigation, naval architecture, logistics and naval weapons increase;
- landlocked and no realistic coast acquisition → maritime weights decrease;
- large livestock/agricultural economy → veterinary, agricultural chemistry and mechanization increase;
- chemical/fertilizer/pharmaceutical shortage → chemistry and relevant process tech increase;
- newly added geological potential → extraction building and enabling technology/PM weights increase;
- high industrial mortality → safety, inspection and occupational medicine increase;
- missing strategic naval inputs → the appropriate upstream industrial/research response increases.

Weights must remain additive and bounded. A situational rule must not bypass prerequisites, era constraints or ahead penalties.

## Salt-specific acceptance suite

Required scenarios:

1. China/1776 normal consumption, current PMs, initial buildings.
2. China high consumption with abundant grain/fish/meat/fruit/groceries but zero salt.
3. China full Food Industries and chemical expansion.
4. China full mobilization with salt supplies.
5. World current/mid/max PM capacity.
6. Salt-rich exporter and salt-poor importer connected by trade.
7. Isolationist salt-poor major.
8. AI with unused solar and rock potential.

For every scenario record direct POP, food industry, chemical, military and total demand; output by source; price/shortage; food security; starving shares; construction; PM changes; imports; and self-sufficiency. Static `UNKNOWN` values in TECH-1C become runtime measurements, not guessed constants.

Target principle: salt may increase preservation costs, lower SoL moderately, hurt chemistry and military supply, but cannot by itself cause mass famine in an otherwise well-fed country.

## Industrial chain acceptance suite

At least five representative chains must pass:

- primary geological resource: copper or industrial minerals;
- intermediate: copper wire/alloy/cement analogue;
- final custom good: pharmaceuticals or consumer good;
- chemical chain: industrial chemicals/fertilizer/pharmaceuticals;
- knowledge chain: industrial records/knowledge → Research Center.

Each test begins with an empty market where practical and asks `WHY DOES AI BUILD THE FIRST BUILDING?`. The accepted cause must be one of explicit latent demand, bounded strategic bootstrap, starting demand, event/decision with reviewed safeguards, or a contextual strategy. “Current profit despite no market” is not an explanation.

## Implementation guardrails

- No external mod dependency for core AI behavior.
- No copied third-party code, assets, localization or maps.
- No forced yearly building creation as the normal solution; use only as a temporary diagnostic fallback if human-approved.
- No mandatory POP minimum for a minor food good without famine tests.
- No `traded_quantity = 0` as a substitute for an explicit tradability decision.
- No global resource mutation without idempotence, save migration and multiplayer tests.
- No new technology without an AI weight and prerequisite audit.
- No new PM/PMG without membership and selection tests.
- No company as the sole source of essential supply.

## Review gate

Implementation may begin only after human approval of:

1. the salt architecture option;
2. the initial resource/good catalog;
3. explicit per-chain bootstrap causes;
4. contextual research rules;
5. runtime metrics and pass thresholds;
6. TECH-1B naval integration scope.

This document defines capability requirements only; it changes no gameplay.
