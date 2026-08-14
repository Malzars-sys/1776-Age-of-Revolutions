# CLEANUP-2E-3 — Merchant Republic Economic Identity Expansion Audit

## Scope and verdict

This phase is research-only. It changes no law, modifier, building, history, localization, asset, or gameplay file. Victoria 3 was not launched. Baseline inspected: local vanilla 1.13.9 at `C:\Games\Victoria 3`, fork branch `cleanup-post-release`, starting HEAD `61ee9578c65b505e662805c7da251308edc0f1a3`.

The coherent target remains:

> **Merchant Republic = own the trade, finance the powers, build the ships — not conquer every mine and plantation.**

Recommended future package:

- penalize unincorporated mining and plantations by 10% with exact vanilla keys;
- retain a numerical 10% farm penalty as the design target, but defer implementation because vanilla 1.13.9 exposes no exact agriculture-unincorporated key;
- reduce ship-construction goods cost by 10%, not 15%;
- remove the free national `modifier_centre_of_commerce_mod` and re-home only reduced, local trade effects in historical monuments;
- use the Rialto commercial complex for VEN and Palazzo San Giorgio for GEN;
- target capital-state trade centers at VEN 8 and GEN 6 only after the national free modifier is removed.

## 1. Evidence boundary and capital-state correction

The VEN/GEN comparison counts **only their capital states**, following the user's correction. It does not aggregate VEN's other states.

Two measurements are deliberately kept separate:

- static history seed: VEN/STATE_VENETIA 6; GEN/STATE_PIEDMONT 3;
- user-observed runtime capital-state level after initialization: VEN 10; GEN 6.

The runtime values were not independently reproduced because the task explicitly forbids launching the game. They are useful observations, but they are not evidence that the history files seed 10/6. The comparison CSV therefore shows both measures rather than silently replacing one with the other.

Detailed evidence tables:

- `docs/research/economy/CLEANUP2E3_UNINCORPORATED_RESOURCE_MODIFIER_AUDIT.csv`
- `docs/research/economy/CLEANUP2E3_NAVAL_CONSTRUCTION_MODIFIER_AUDIT.csv`
- `docs/research/economy/CLEANUP2E3_TRADE_CENTER_1776_COMPARISON.csv`
- `docs/research/economy/CLEANUP2E3_MONUMENT_HISTORICAL_AUDIT.csv`

## 2. Unincorporated resource extraction

### Exact vanilla 1.13.9 keys

Confirmed in `game/common/modifier_type_definitions/99_todo_sort_into_other_files.txt`:

- `building_group_bg_plantations_unincorporated_throughput_add` at line 3589;
- `building_group_bg_mining_unincorporated_throughput_add` at line 3598;
- parallel keys for manufacturing, logging, and rubber;
- **no** `building_group_bg_agriculture_unincorporated_throughput_add` anywhere in the audited vanilla `game/common` tree.

The sign is confirmed by vanilla `game/common/laws/00_colonial_affairs.txt:287-295`: Colonial Extraction grants `+0.20` to plantation, rubber, logging, and mining throughput in unincorporated states while applying `-0.10` to manufacturing. Negative values therefore implement the intended penalty.

### Why the global key is rejected

`building_unincorporated_throughput_add` exists (`01_building_modifier_types.txt:1148`) but targets every affected building in an unincorporated state. A `-0.10` use would violate the brief by penalizing ports, trade centers, naval administration, shipyards, and urban manufacturing alongside resources.

### Farms: valid solutions when the direct key does not exist

1. **First implementation — recommended:** ship mines and plantations only; keep farms at a documented `-0.10` design target until an exact mechanism is proven.
2. **Scripted state modifier:** apply a normal agriculture throughput penalty only while an eligible state is unincorporated. This can target farms, but requires robust application and removal on ownership, incorporation, and law changes plus save/load reconciliation. Risk: high.
3. **Custom modifier type:** do not infer engine support from a plausible name. This is invalid until a minimal isolated prototype proves that the engine can register and evaluate a custom building-group/unincorporated modifier type.

The farm target is therefore numeric but explicitly **deferred**, not silently dropped and not implemented with an invented key.

## 3. Naval construction audit

### Existing Merchant Navy stack

Vanilla `game/common/laws/00_navy_model.txt:13-18` gives `law_merchant_navy`:

- `country_ship_group_supply_ships_construction_efficiency_add = 0.30`;
- `country_ship_type_troop_ship_construction_efficiency_add = 0.30`;
- `country_ship_construction_efficiency_add = -0.10`;
- `ship_interest_gain_mult = -0.10`.

On an additive reading of the efficiency modifiers, supply ships and troop ships receive a net +20 percentage points while generic military construction keeps the -10% global efficiency profile. A new positive construction-efficiency modifier would partially or wholly erase this intended asymmetry.

### Correct key for the requested effect

`country_ship_construction_goods_cost_mult` is defined in `game/common/modifier_type_definitions/00_modifier_types.txt:2592`. Its localization describes ship-construction material necessities. It is the closest exact expression of “-10% construction cost” and is distinct from:

- `country_ship_construction_efficiency_add`: total construction required per progress unit;
- `country_ship_construction_add`: weekly construction amount;
- `country_ship_construction_progress_max_add/mult`: per-project progress cap or speed ceiling;
- shipyard throughput: simultaneous input/output change;
- `country_navy_goods_cost_mult`: active navy operating cost.

The goods-cost key is global to ship construction, so it is the best candidate for both military and supply/merchant shipping. The audited definitions do not prove that ship modification/refit consumes this exact modifier path; refit coverage must be runtime-tested before it is promised in UI text.

### -10% versus -15%

`-0.10` is recommended for the first implementation. It produces a real cost identity without undoing Merchant Navy's efficiency tradeoff. `-0.15` is 50% stronger than the proposed value, lacks an observed vanilla balancing precedent in the audited usage search, and would be premature before comparative runtime tests of construction queues, goods demand, and refits.

## 4. `modifier_centre_of_commerce_mod`

Current fork definition (`common/static_modifiers/76mod_modifiers.txt:343-347`):

| Current effect | Audit | Future action |
| --- | --- | --- |
| `building_trade_center_throughput_add = 0.50` | Very large free national throughput increase; affects both inputs and outputs and compounds the dedicated merchant stack. | `MOVE_TO_MONUMENT + REDUCE`: local capital-state `+0.10`. |
| `country_minting_add = 10000` | Flat minting is not a good proxy for private merchant finance; the scale is extreme for compact GEN/VEN. | `REMOVE`: no automatic replacement. |
| `state_export_advantage_mult = 0.20` | Thematic, but free and stacked with trade-law/banking advantages. | `MOVE_TO_MONUMENT + REDUCE`: local capital-state `+0.10`. |

The overall action is **remove the national static modifier**. In a future gameplay phase, monument production methods can supply bounded local effects. They should not recreate the same country-wide package under another name.

## 5. Historical monument choice at the 1776 cutoff

### Venice

The Doge's Palace is unquestionably valid for government, justice, and state symbolism. Its institutional chambers housed the Great Council, Senate, Collegio, judicial bodies, Council of Ten, chancery, and a chamber of navy captains ([Musei Civici di Venezia](https://palazzoducale.visitmuve.it/en/layout-and-collections/institutional-chambers/)). It is therefore an excellent **political/administrative** monument, but an indirect container for a specifically commercial-financial replacement.

The Rialto is the stronger economic choice. Research describes it as a continuing major commercial center in eighteenth-century Venice, while the city remained the principal Adriatic port and a significant regional market; the same evidence documents an organized, diverse credit market ([Cambridge University Press](https://www.cambridge.org/core/journals/continuity-and-change/article/borrowing-in-a-preindustrial-city-financial-behaviour-and-economic-rationality-in-eighteenthcentury-venice/A3F420B07CEED5B4B5486048FD6B2C39)). The broader institutional complex connected merchants, intermediaries, insurers, notaries, banks, information, and merchant justice ([CNR IRIS record](https://iris.cnr.it/handle/20.500.14243/500422)).

Decision: `VEN_MONUMENT = RIALTO_COMMERCIAL_COMPLEX`. The name must make clear that this represents a district/institutional complex, not a fictitious single palace.

### Genoa

Palazzo San Giorgio is the exact fit. The Casa delle Compere e dei Banchi di San Giorgio existed from 1407 to 1805 and combined taxation, public debt, territorial prerogatives, and a public deposit/giro/credit bank ([Casa di San Giorgio archival project](https://www.lacasadisangiorgio.eu/main.php?do=home)). Scholarship characterizes it as a creditors' protection institution that reduced Genoa's financing cost ([Review of Finance](https://academic.oup.com/rof/article/10/4/487/1578656)). The institution's own archive includes commercial, loan, and diplomatic records around the 1770s, supporting continued activity at the cutoff ([archival inventory example](https://www.lacasadisangiorgio.eu/main.php?do=scheda&idscheda=85760&page=68&ricerca=1)).

Decision: `GEN_MONUMENT = PALAZZO_SAN_GIORGIO`.

## 6. Technical monument audit

Vanilla 1.13.9's visible monuments in `game/common/buildings/08_monuments.txt` establish the normal pattern:

- `building_group = bg_monuments`;
- `expandable = no`, normally `unique = yes`;
- `buildable = no` for an already-existing start monument;
- a state `potential` tied to the correct `state_region`;
- history placement via `create_building` at level 1 in the state owner;
- a monument-specific production-method group and base production method;
- modifier blocks in the production method, permitting country, state, or building effects with appropriate scaling;
- building and production-method localization plus an icon.

The normal ownership route is the state/building owner; no separate history owner is required for ordinary start monuments unless a specific ownership mechanic demands it.

The first comments in `game/common/production_method_groups/08_monuments.txt` are important: new monuments should include `pm_monument_prestige_only` and `pm_monument_no_effects`, and the `monument_effects` game rule must be amended with flags that disable/force the new base method correctly. Omitting that work would make the new monuments ignore player game-rule choice.

### Graphics risk

Ordinary visible vanilla monuments normally have map locator/entity support. The dynamic power-bloc statue is a special subsystem and is not a clean generic fallback precedent. No dependable ordinary “missing 3D asset” fallback was proven by this audit.

Recommended first-patch sequence:

1. implement the data/UI/effect definition with a reused generic interface icon;
2. keep the monument non-buildable, unique, level 1, and state-locked;
3. test an asset-free prototype in isolation for map errors and visibility before merging;
4. if the asset-free visible monument is not clean, use a deliberately hidden institutional building/state modifier as an interim implementation rather than shipping a broken or misleading 3D object.

This avoids treating “no crash in text parsing” as proof of a clean graphical fallback.

## 7. Capital-state trade-center comparison

The CSV contains the requested fields and the static values parsed from fork history. Historical labels are qualitative rather than a false-precision one-to-eight ranking: port functions were not directly commensurable across imperial gateways, entrepôts, regional markets, and financial centers.

Useful anchors:

- London handled about two-thirds of England's trade value in the 1770s ([Cambridge University Press](https://www.cambridge.org/core/books/abs/early-modern-atlantic-economy/property-versus-commerce-in-the-mideighteenthcentury-port-of-london/5667C6E6DBFF561D77DDC664AB05630A)).
- Hamburg is described as Europe's third-largest port after London and Amsterdam, competing as the Central Europe–Atlantic gateway ([Journal of Global History](https://www.cambridge.org/core/journals/journal-of-global-history/article/free-ports-political-economy-and-early-globalization-evidence-from-1750s-hamburg/E3596B4ADCD382B83B434CF83413573A)).
- Marseille played a fundamental eighteenth-century role distributing colonial goods to the Mediterranean ([CNR/RiMe](https://rime.cnr.it/index.php/rime/article/view/547)).
- A 1771 Genoese consular report emphasized the scale of Brazil/India goods moving from Lisbon toward Genoa, and contemporaries observed a large Genoese merchant presence in Lisbon ([Cahiers de la Méditerranée](https://journals.openedition.org/cdlm/18054?lang=en)).

The static setup is not a literal historical ranking: London 5 and Hamburg 3 sit below Lisbon 10, while Cádiz 2 is low despite its imperial gateway role. It should be treated as a gameplay seed shaped by ownership and initialization systems.

### Three proposals

| Proposal | VEN capital state | GEN capital state | Interpretation |
| --- | ---: | ---: | --- |
| `CONSERVATIVE` | 6 | 3 | Preserve the static history seeds; safest if the national modifier remains temporarily. |
| `HISTORICAL_TARGET` | 6 | 5 | Venice remains the larger Adriatic regional market; Genoa's finance/shipping specialization rises without matching current runtime VEN 10. |
| `GAMEPLAY_STRONG_MERCHANT_REPUBLIC` | 8 | 6 | Strong identity after removal of the free national modifier; above Amsterdam's seed for VEN but below current runtime 10. |

Final recommendation: **VEN 8 / GEN 6 in the capital states**, conditional on removing `modifier_centre_of_commerce_mod` and validating the initialization delta. If the runtime system automatically adds four levels to VEN and three to GEN, the future patch must adjust the source that produces the final result rather than simply writing 8/6 into static history.

Therefore, the user-observed runtime `VEN = 10`, `GEN = 6` is not accepted as a balanced pair: GEN 6 is supportable as a specialized merchant republic, but VEN 10 plus the existing +50% national throughput and +20% export advantage is excessive against the audited seed benchmarks.

## 8. Final numeric proposal

```text
UNINCORPORATED_MINING = -0.10
UNINCORPORATED_FARMS = -0.10 DESIGN TARGET; IMPLEMENTATION DEFERRED (NO EXACT VANILLA KEY)
UNINCORPORATED_PLANTATIONS = -0.10

NAVAL_CONSTRUCTION_BONUS = country_ship_construction_goods_cost_mult = -0.10

VEN_MONUMENT = RIALTO_COMMERCIAL_COMPLEX
GEN_MONUMENT = PALAZZO_SAN_GIORGIO

VEN_TRADE_CENTER_LEVELS = 8 (CAPITAL STATE FINAL TARGET)
GEN_TRADE_CENTER_LEVELS = 6 (CAPITAL STATE FINAL TARGET)

CENTRE_OF_COMMERCE_MODIFIER_ACTION = REMOVE NATIONAL MODIFIER;
  MOVE building_trade_center_throughput_add TO MONUMENT AND REDUCE +0.50 -> +0.10 LOCAL;
  REMOVE country_minting_add = 10000 WITHOUT AUTOMATIC REPLACEMENT;
  MOVE state_export_advantage_mult TO MONUMENT AND REDUCE +0.20 -> +0.10 LOCAL.
```

## STOP condition

Audit complete. No gameplay implementation, staging, commit, push, or game launch was performed.
