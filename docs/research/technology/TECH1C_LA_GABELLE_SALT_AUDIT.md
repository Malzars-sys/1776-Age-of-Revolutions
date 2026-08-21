# TECH-1C-A — La Gabelle / Salt System Audit

Status: `INPUT_FOR_HUMAN_REVIEW` · `NOT_CANONICAL` · `NOT_IMPLEMENTED`

## Scope and evidence

Installed reference: `La Gabelle`, Workshop `3715913236`, version `1.0.2`, target `1.13.*`, at `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3715913236`. The descriptor has no declared relationship or `replace_path`. The audit covered every text/script file, localization set and salt-related asset path; no third-party content was copied.

The certified vanilla comparator is `C:/Games/Victoria 3/game`, 1.13.9. The project population histories were also parsed for the 1776 projection.

## Actual architecture

The complete material graph is:

`state potential → building_salt_pan | building_salt_mine → production method → one staple good salt → POP basic/luxury food + food PMs + chemical PMs + mobilization supplies + tax/company/prestige/event hooks`.

Solar and rock extraction produce the same `salt` good. There are no separate solar/rock goods, salt state traits, salt laws, institutions, decrees, decisions, map modes or scripted effects.

## The salt good and POP demand

`salt` costs 30, is a `staple`, has traded quantity 10, convoy multiplier 0.5, tax authority cost 200 and no `tradeable = no`; it therefore uses normal tradable-good behavior. No salt obsession or taboo is defined. One generic prestige good uses salt as its base good.

La Gabelle injects salt into:

- `popneed_basic_food`: weight 1, maximum share 20%, minimum share 0%;
- `popneed_luxury_food`: weight 0.5, maximum share 15%, minimum share 5%.

The basic-food weight is ordinary relative to vanilla fish/meat/fruit (1) and groceries (1.15). A zero minimum means basic-food demand can substitute away from salt. The luxury-food minimum is the structurally risky part: affected POPs retain a mandatory salt share even when alternatives exist. Exact purchases depend on engine-only wealth packages, prices, availability and substitution allocation, so a population-to-units conversion cannot be proven statically.

## Solar salt

`building_salt_pan` is a medium-construction, self-owned `bg_mining` building with port visuals. It has no technology gate, but its building potential requires `is_sea_adjacent = yes`. Its sole PM produces 10 salt with 500 shopkeepers and 2,000 laborers per fully employed level and consumes no goods. The map script assigns only selected states a potential, but no climate or geological trigger is evaluated dynamically. There is no technological upgrade path, input cost or pollution.

Verdict: clear dual-resource idea, but the fixed output and zero-input PM need rebalancing/reimplementation for 1776.

## Rock salt

`building_salt_mine` is a medium-construction, self-owned `bg_mining` mine gated by `shaft_mining`. Equipment output progresses from 20 to 35, 45 and 55 salt. Nitroglycerin and dynamite add 15 or 20, giving 20 current, 50 representative mid-tier and 75 maximum output per fully employed level. Inputs progress through tools, coal/oil and explosives. The mine reuses vanilla steam and rail automation PMs. Pollution and the nitroglycerin mortality penalty are real.

Verdict: the technological PM ladder is reusable as an architectural pattern, not as code or balance.

## Resource map

The parser found 159 distinct state regions, 97 with solar potential and 64 with rock potential; Catalonia and Upper Andalusia have both. Totals are:

- solar potential: 2,526;
- rock potential: 1,209;
- combined potential: 3,735.

Potential is only a construction ceiling. It is not output: levels must be constructed, staffed and supplied, and the selected mine PM changes output. At full exploitation, theoretical salt output is 49,440 at current PMs, 85,710 at the representative mid tier and 115,935 at maximum technology. These are capacity ceilings, not market supply predictions.

History files define 102 pan levels and 65 parsed mine levels. `STATE_URALSK` level 3 is duplicated in both `lagab_asia.txt` and `lagab_europe.txt`, so literal starting supply needs runtime confirmation. The corresponding parsed ceiling is 2,320 at current PMs.

## China/Qing stress test

The certified vanilla and 1776 project both contain 366,405,602 CHI population across 43 state scopes. The 1776 world population differs from vanilla, but the CHI population data is unchanged.

Vanilla 1836 CHI-owned state regions hold 179 solar and 102 rock potential. Guangdong is split with Portugal; its state-level potential is included but actual ownership/market allocation remains runtime-sensitive. La Gabelle creates 42 pan levels and 9 mine levels for CHI, giving a fully employed current-PM starting ceiling of 600. Full exploitation yields 3,830 current, 6,890 mid-tier and 9,440 maximum.

Neither test can compute direct POP salt purchases: the engine does not expose the need budget, wealth distribution and substitution allocation as script values. Literal CHI building histories select none of the ten injected industrial consumer PMs at start, so projected initial industrial demand from those PMs is zero. Military salt demand is zero unless the extra/luxurious supply option is selected; its formation scaling is engine-controlled.

Therefore both `LA_GABELLE_VANILLA_START_STATIC_TEST` and `1776_PROJECTED_CHINA_STATIC_TEST` are `INCOMPLETE`, and numeric self-sufficiency ratios or import requirements are `UNKNOWN`. Runtime validation is mandatory.

## World stress test

Certified vanilla population is 1,022,466,685; the 1776 project history totals 1,015,483,064. The known supply ceilings cannot be compared to a defensible world demand number for the same engine-formula reason. Industrial and mobilization demand additionally depend on active PMs and formations. `WORLD_SALT_SUPPLY_SUFFICIENT = UNKNOWN`.

## Hypotheses H1–H10

| Hypothesis | Static result | Reason |
|---|---|---|
| H1 weight too high | Not demonstrated | Basic weight 1 is normal; luxury weight is 0.5. |
| H2 substitution disproportionately penalizes basic food | Partly contradicted | Basic salt has min share 0 and max 20%; aggregate food-security formula still makes it relevant. |
| H3 global potential insufficient | Unknown | Large theoretical capacity exists, but demand cannot be statically derived. |
| H4 China potential insufficient | Unknown | 281 potential levels exist; only 51 are built at start. |
| H5 PM output too low | Plausible at startup | Start ceiling is far below full potential; solar never upgrades. |
| H6 AI under-exploits resources | Plausible/runtime required | No custom salt AI, desired levels or latent bootstrap exist. |
| H7 Food Industries create excessive demand | Plausible later | Six PMs add 10–30 input per level; none is active in literal CHI start. |
| H8 military demand magnifies shortage | Conditional | Only selected extra/luxurious mobilization supplies consume salt. |
| H9 trade cannot compensate | Not demonstrated | Salt is tradable; many countries receive import-subsidy tariffs, but CHI is excluded and route sizing is runtime AI. |
| H10 mechanisms combine | Most plausible | Mandatory luxury share, tax, low initial exploitation, downstream PMs and generic AI can compound. |

Primary static verdict: `MULTIPLE`, with demand quantity and runtime AI still unproven.

## Famine path

Victoria 3 1.13.9 computes starvation from food security: below 0.4 a POP starves, below 0.2 it is severe, and a state becomes a famine at 35% starving or 15% severe. La Gabelle contains no salt-specific starvation/famine trigger. The path is therefore:

`salt shortage/high price → basic-food substitution contribution may fall → aggregate food security may fall → starvation thresholds → state famine thresholds`.

The luxury-food minimum and `gabelle_income` SoL penalties can worsen welfare, but they are not themselves the engine food-security trigger. Because basic salt has a zero minimum, salt alone should be replaceable by other basic foods; mass famine in an otherwise well-fed market is not proven by the scripts and must be reproduced at runtime.

Classification: `SALT_SHORTAGE_CAN_DIRECTLY_TRIGGER_FAMINE = INDIRECTLY`.

## Industry and military demand

Six food PMs consume 10–30 salt per level. Four dye/fertilizer PMs consume 5–20. These injections are workforce-scaled and can create large secondary demand as industries expand. Extra and luxurious supplies add 0.5 and 1 salt upkeep respectively only when selected. The complete consumer list is in `TECH1C_LA_GABELLE_SALT_DEMAND_INDEX.csv`.

## Companies, taxation and JEs

Six companies exist: generic, Salt Union, Groupe Salins, Morton Salt, Kali und Salz and Maldon Sea Salt. They cover the two buildings, have level-based availability/AI triggers, and can unlock the generic prestige salt through an MP1-gated JE. No company charter definition is supplied; vanilla charters govern them.

There is no Chinese salt company object. Simplified-Chinese localization translates the generic/flavor companies but does not define a Chinese company. Consequently the reported “Chinese company requiring a missing JE” is not reproduced in version 1.0.2; it may refer to another/older build.

France receives `je_gabelle` and `gabelle_income` while taxing salt. The JE intentionally never completes and can be deactivated. `lagab_france.2` appears defective: its trigger requires `lagab_gabelle_reformed` before its reform option sets that same variable, making normal first activation unlikely. This is a real visibility/trigger mismatch, not a Chinese-company issue.

Starting consumption taxes apply to FRA, BIC, SPA, AUS, RUS, SIC, PAP and PRU. Most other non-excluded countries receive import-subsidy tariffs; CHI and JAP are explicitly excluded. No salt law or state-monopoly/private-ownership law hook exists.

## AI and trade

La Gabelle adds no AI strategies, scripted construction values or research weights. The two buildings rely on vanilla profitability/resource AI, PM choice relies on vanilla PM scoring, and trade relies on normal trade AI plus starting tariff settings. Company `ai_will_do` tests exist. This is adequate for a reference prototype, but not evidence that large markets exploit supply fast enough.

## 1776 salt architecture options

| Option | Fidelity | Robustness | AI complexity | Famine risk | Trade/map dependence | Implementation |
|---|---|---|---|---|---|---|
| A — primarily food-processing/industrial, tiny or no direct POP use | High for preservation/chemistry | High | Medium | Low | Medium | Medium |
| B — direct POP use with a very low cap and zero minimum | High | Medium-high | Medium | Low-medium | Medium | Low-medium |
| C — dedicated controlled need with explicit safeguards/substitutes | Potentially highest | Medium | High | Controllable but test-heavy | High | High |

Option A best satisfies the current target principle. Option B is viable only with zero minimum share, modest cap and runtime China/world tests. Option C should wait until the engine’s food-security response is measured. La Gabelle’s mandatory luxury minimum should not be adopted.

## Final component verdicts

| Component | Verdict |
|---|---|
| Resource map | `REUSE_IDEA`, rebalance geographically |
| Solar production | `REIMPLEMENT_DIFFERENTLY` |
| Rock production | `REUSE_IDEA` / local reimplementation |
| Salt good | `REIMPLEMENT_DIFFERENTLY` |
| POP consumption | `AVOID` as-is |
| Food input | `ADAPT` |
| Chemical input | `ADOPT_CONCEPT` |
| Military input | `ADAPT` |
| Companies | `ADOPT_CONCEPT` |
| Taxation/JEs | `MOD_SPECIFIC`; French event needs repair if ever reimplemented |
| AI | `INSUFFICIENT_FOR_1776_TARGET` |
| Localization/icons | Presence verified; no reuse |

Runtime tests still required: fresh 1836 and 1776 starts; China weekly supply/demand by need; PM adoption; autonomous construction of both salt buildings; employment/input shortages; imports under isolationism/free trade; full mobilization; Food Industries expansion; famine/food-security response with abundant substitute foods.
