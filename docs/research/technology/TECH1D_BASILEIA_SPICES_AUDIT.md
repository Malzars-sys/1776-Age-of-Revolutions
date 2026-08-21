# TECH-1D — Basileia Romaion 1736 Spices Reference Audit

Status: `REFERENCE_ONLY` · `NOT_CANONICAL` · `NO_THIRD_PARTY_CONTENT_COPIED`

## 1. Identity and scope

The locally installed reference is `[1.13] Basileia Romaion 1736`, version `1.5.0`, Workshop ID `2880120246`, targeting Victoria 3 `1.13.*`. Its metadata declares Community Mod Framework `1.*` as a dependency and replaces several history/map paths. This audit reads its salt-independent spice implementation only. No script, value, asset or localization is adopted automatically.

## 2. Good definition

`spices` is a luxury good with base cost 60, traded quantity 10, convoy multiplier 0.25, obsession chance 3.0 and prestige factor 10. It has no explicit `tradeable = no`, so the implementation expects normal trade. These values belong to the reference mod and remain non-canonical for 1776.

## 3. POP demand

The mod replaces `popneed_luxury_food` and adds spices at weight 0.75, maximum supply share 0.50 and minimum supply share 0.01. This proves a direct luxury-food demand route. The 1% mandatory floor must not be inherited without a world supply, affordability and famine/SoL stress test; TECH-2 therefore leaves all spice need weights and minimums deferred.

## 4. Production building and PMs

`building_spices_plantation` is an arable plantation gated by `br_tech_plantation_system`. It uses one base PMG and the normal train-automation PMG. The basic PM outputs 15 spices per workforce-scaled level. Automatic irrigation, gated by vanilla `pumpjacks`, consumes 5 engines and outputs 45 spices while changing employment and adding pollution. The plantation technology is an era-1 production technology with static AI weight 2 and a prerequisite on `br_tech_new_world_crops`.

For 1776, spices are an established regional crop rather than an invention. Initial regional production must therefore be setup/potential based; technology may improve plantation organization, transport or processing but must not make spices appear ex nihilo worldwide.

## 5. Intermediate consumption

The Food Industries base PMG is replaced to add `pm_spiced_food`. That PM consumes 40 grain, 5 spices and 2 sugar for 75 groceries. The mod also injects spices into later grocery PMs at 5 and 10 units. This is a valid proof that an intermediate food-processing sink can complement direct POP demand, but the replacement scope and quantities are not suitable for direct reuse.

## 6. Geography and starting supply

Static parsing finds 131 state regions whose `arable_resources` include `building_spices_plantation`: 43 in Sub-Saharan Africa, 26 in South America, 26 in India, 17 in Indonesia, 11 in North America, 5 in Central America, 2 in the Middle East and 1 in North Africa. Three parsed state blocks also contain `state_trait_spice_islands`.

History contains 22 scripted `create_building` blocks for spice plantations and 63 summed ownership `levels` declarations. Some blocks contain multiple owners/regions or scenario-dependent setup, so 63 is an index total rather than a guaranteed runtime building total.

The breadth of the 131-state eligibility map is not accepted as historical evidence for 1776. A dedicated commodity/geography review must distinguish true spice-producing ecologies and specific crops from broad tropical cash-crop eligibility.

## 7. Trade, companies and AI

Administrative strategies explicitly set `spices = { stance = wants_export }` in three locations. Three default-strategy conditions also react to a spice-trade modifier. Several trade companies include the plantation and one exposes a prestige spice good. This supports an exporter-oriented colonial trade loop, but no spice-specific general import planner, shortage recovery rule or first-plantation bootstrap was found.

For 1776, producer AI must recognize ecological eligibility, retain adequate domestic supply, expand only against demand, and importer AI must respond to luxury/industrial shortage. A blanket export stance is insufficient.

## 8. Technology placement for TECH-2

Spices are `REQUIRED` for public V1, but no standalone “invention of spices” technology is added. The integrated tree attaches:

- traditional/regional production to starting setup and ecological eligibility;
- early plantation improvement to `improved_husbandry` and `improved_agricultural_implements`;
- global commercial integration to Society finance/trade nodes;
- processed-food demand to `hermetic_food_preservation` and its successors.

Economic values, exact POP need shares, PM quantities, state eligibility, initial building levels and trade balance remain `DEFERRED_PENDING_1776_SPICE_DESIGN`.

## 9. Verdict

`SPICE_REFERENCE_MOD_AVAILABLE = YES`

`BASILEIA_SPICE_REFERENCE_AUDITED = YES`

`BASILEIA_IMPLEMENTATION_CANONICAL_FOR_1776 = NO`

`SPICES_TECH_POSITION_PREPARED = YES`

`SPICE_ECONOMY_AND_MAP_VALUES = DEFERRED_PENDING_1776_SPICE_DESIGN`

