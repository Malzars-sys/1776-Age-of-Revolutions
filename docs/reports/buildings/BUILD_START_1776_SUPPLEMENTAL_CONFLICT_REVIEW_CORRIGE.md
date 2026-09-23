# BUILD START 1776 — Supplemental overlap/conflict review — CORRIGE

Target date: **1776-01-01**  
Scope: source review only; no gameplay files modified.

## Resolution principle

The original audit correctly retained four Owner_TAG + State_ID pairs as multi-researched. This supplemental pass compares the divergent building-level conclusions against additional evidence. `Multi_Researched` remains `YES` for provenance, but `Conflict_Present` is cleared because every listed discrepancy now has an explicit resolution.

## Hawaii — HAW + STATE_HAWAIIAN_ISLANDS

- `building_fishing_wharf`: **keep level 2** from the Oceania audit. Pre-contact Hawaiian fishpond/aquaculture systems provide direct evidence of organized fishing capacity. Source: https://www.nps.gov/places/huilua-fishpond.htm
- `building_railway`: **keep level 1 only as the mod's road/trail infrastructure abstraction with `pm_no_rail_network`**. The Alakaʻi/major trail literature documents substantial pre-contact/early historic trail systems; no rail technology is implied. Source: https://home.nps.gov/alka/learn/historyculture/index.htm
- `building_salt_pan`: **keep level 1** from the Oceania audit. Traditional Hawaiian salt harvesting used purpose-built shallow clay ponds on a larger scale, directly matching the salt-pan abstraction. Source: https://manoa.hawaii.edu/sealearning/grade-5/physical-science/matter-sea/traditional-ways-knowing-salt-harvesting

## Tibet

Primary near-contemporary source: George Bogle's 1774 mission/trade account, which describes substantial Tibetan foreign trade, wool, salt, gold, woollen cloth/serge and foreign merchants in Lhasa/principal towns: https://www.cambridge.org/core/books/abs/narratives-of-the-mission-of-george-bogle-to-tibet/trade-of-tibet/9B11E89C4A170CD2B4DB5544656947DF

- `TIB + STATE_EASTERN_HIMALAYAS / building_livestock_ranch`: keep **level 1**.
- `TIB + STATE_LHASA / building_government_administration`: keep **level 1** from the old East Asia audit; the capital status is compatible with the 1774 description, but no higher level is inferred.
- `TIB + STATE_LHASA / building_livestock_ranch`: resolve to **level 1**, reducing the stronger R3 level 2 claim conservatively.
- `TIB + STATE_LHASA / building_railway`: resolve to **no positive recommendation**. Trade evidence does not by itself prove a qualifying 1776 road/canal network under the fork's infrastructure abstraction.
- `TIB + STATE_LHASA / building_textile_mill`: keep **level 1**; Bogle explicitly describes Tibetan woollen cloth/serge.
- `TIB + STATE_LHASA / building_trade_center`: **level 1 confirmed compatible** across both audits.
- `TIB + STATE_NGARI / building_livestock_ranch`: resolve to **level 1**, conservatively retaining livestock/wool evidence without R3's level 2 scale.

## Outcome

- Multi-researched Owner/State pairs retained for provenance: **4**.
- Unresolved owner/state conflicts after this review: **0**.
- Human review required by the corrected overlap table: **0**.
