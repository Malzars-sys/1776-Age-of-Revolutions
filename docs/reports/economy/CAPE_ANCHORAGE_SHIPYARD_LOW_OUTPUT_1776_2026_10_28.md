# Cape Colony anchorage and 1776 low-output shipbuilding

Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** — 28 October 2026. Separate draft PR against `main`.

## Historical context

The VOC established the Cape as a ship-replenishment station in **1652**, routinely anchored in **Table Bay**, and designated **Simon's Bay** as the winter anchorage in **1743**. This was primarily an open roadstead and provisioning station rather than a modern stone-walled harbor. A minimal `building_port` at the 1776 start is thus historically justified. The state already has a coast/port province and `state_trait_natural_harbors`.

- South African History Online: https://sahistory.org.za/place/dutch-and-british-coastal-fortifications-cape-good-hope-1665-1829
- Cape Town harbor history (wooden jetties in 1665 and 1767): https://maritimesa.org/grade-10/the-history-of-cape-town-harbour/

Dutch and other European shipbuilding already had large, three-masted square-rigged vessels well before 1776, but smaller and more labor-intensive merchant-ship production was also possible. The new low-output PM is **a gameplay abstraction**, not a claim that three-masted ships first appeared after 1776.

- Cambridge University Press, J. R. Bruijn on the Dutch fluyt and varying costs: https://www.cambridge.org/core/books/abs/rise-of-merchant-empires/productivity-profitability-and-costs-of-private-and-corporate-dutch-ship-owning-in-the-seventeenth-and-eighteenth-centuries/1FFEF5EF43A094A91A8FD560B7ADBB71
- Mariners' Museum on Dutch fluyt: https://exploration.marinersmuseum.org/watercraft/fluit/

## Implemented changes

### Cape Colony
In `common/history/buildings/04_subsaharan_africa.txt`, **`s:STATE_CAPE_COLONY.region_state:DEI`** receives 1 government-owned `building_port`, using `pm_anchorage` and `reserves=1`. No existing farms, roads, livestock ranches, POPs or state ownership were modified.

### Shipyard PM progression
A new `pm_1776_artisanal_shipbuilding` comes **first** in `pmg_base_building_shipyard`, before `pm_basic_shipbuilding`, `pm_complex_shipbuilding`, `pm_metal_shipbuilding` and `pm_arc_welding_shipbuilding`. The original PMs' recipes, technology gates, icons and IDs are unchanged.

| Level | Localized French label | Inputs, at full employment | Outputs | Employment | Naval construction |
|---|---|---|---|---|---|
| New | Construction navale artisanale | **20 wood + 10 fabric** | **20 clippers** | 500 shopkeepers + 2,000 laborers | +5 (same as former start PM) |
| Former `pm_basic_shipbuilding` | Trois-mâts à voiles carrées | 40 wood + 20 fabric | 40 clippers | Former existing composition | +5 |
| Former `pm_complex_shipbuilding` | Navires renforcés à propulsion auxiliaire | 20 wood + 20 hardwood + 20 fabric + 5 engines | 70 clippers | Former existing composition | +10 |

New PM uses the existing `gfx/error_deer.dds` placeholder, as requested. Future artwork may replace it. New localizations cover French and English.

New low-output PM has **no tech unlock gate**; shipyards themselves retain the existing `state_dockyard_systems` building unlock. The two later PMs remain gated as before.

The base shipyard group now uses `ai_selection = most_profitable` instead of `most_productive`. This is deliberate: when clipper demand is too low, AI should consider profit instead of automatically chasing output. The engine's actual choice still needs runtime confirmation.

### Historical start migration
Existing `building_shipyard` entries that explicitly activated `pm_basic_shipbuilding` were migrated to `pm_1776_artisanal_shipbuilding`. This leaves **all historical shipyard building levels and owners intact**.

| History file | Shipyards migrated |
|---|---:|
| 00_west_europe | 15 |
| 01_south_europe | 12 |
| 03_north_africa | 5 |
| 05_north_america | 12 |
| 06_central_america | 1 |
| 07_south_america | 2 |
| 08_middle_east | 6 |
| 10_india | 6 |
| 11_east_asia | 7 |
| 12_indonesia | 4 |
| 15_russia | 6 |
| **Total** | **76** |

Historical entries are changed only within the affected `create_building` shipyard blocks. All other initial building PMs and levels are left unchanged.

## Static verification

- Cape DEI has exactly one added port, owner DEI, `pm_anchorage`.
- New PM's only material inputs: 20 wood, 10 fabric. Only goods output: 20 clippers.
- `gfx/error_deer.dds` placeholder bound; 2,500 baseline jobs in new method (2,000 laborers + 500 shopkeepers).
- `country_ship_construction_add=5` avoids an unintended naval construction penalty at the new initial setting.
- New PM listed before four existing methods; `ai_selection=most_profitable`.
- All 76 targeted historic shipyards migrated, with IDs and owners unchanged.
- French/English names available for all three discussed methods; braces balanced in modified script files.

## Not runtime-validated
- The actual market linkage of Cape to the Dutch market also depends on employment, shipping access and the current market/convoy mechanics.
- Starting revenue, deficit and hiring of shipyards, especially in other countries at 1776 launch.
- AI switching behavior immediately and after 4 weeks (it may still choose more productive methods if those are genuinely more profitable).
- Tooltip icon and translations in the current game version, one-month simulation and save/reload.

Test on a **new 1776 game**; do not merge before player validation.
