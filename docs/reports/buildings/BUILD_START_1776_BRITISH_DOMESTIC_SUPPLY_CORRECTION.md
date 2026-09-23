# BUILD START 1776 — British market correction V2

## Runtime evidence

The supplied British-market capture showed red shortages for fruit (398), lead (174), furniture (162), luxury clothes (117), fertilizer (250), groceries (464), dye (20), and salt (172). Only those red-marked goods are treated as shortages.

## Placement policy

- No resource potential was added to the British Isles or anywhere else.
- Colonial extraction and plantations use existing potential outside BIC.
- British manufacturing remains in Lancashire, the Midlands and the West Country.
- The previously added ten tooling-workshop levels are retained to create the intended Indian dependence on British tools.
- The erroneous East Anglia dye, sugar and salt placements were removed. Apple-orchard PMs on the five added rye-farm blocks were disabled, restoring their grain focus.

## Capacity correction

- Fruit: 8 banana levels in Jamaica and 6 in the British West Indies (420 theoretical output).
- Dye: Florida raised from 1 to 2 levels (60 theoretical output).
- Lead: 4 levels in Newfoundland and 5 in the West Country (180 theoretical output).
- Furniture: 4 handcrafted levels in the West Country (180 theoretical output).
- Luxury clothes: 4 craftsman-sewing textile levels in the West Country (120 theoretical output).
- Fertilizer: 7 early fertilizer lines in Lancashire (280 theoretical output).
- Groceries: the 12 Home Counties bakery levels are retained (500 theoretical output from the ten-level runtime increase).
- Salt: 24 levels in Senegal (240 theoretical output), within its pre-existing 30-level salt potential. A level-1 anchorage connects the colonial state to the British market. The salt works are owned by British capitalists.
- Inputs: 3 limestone levels in the Bahamas, 2 in Florida, and 3 logging levels in Jamaica support the new chains. No BIC building was used.
- The prior HBC fishery addition receives one traditional-road level in Manitoba, Ontario and Quebec; this closes the three infrastructure gaps created after Wave 1.

## Chemical consolidation (Tech & Res pattern)

The local subscribed `[1.13] Tech & Res` mod at `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3472248460` was used as the structural reference: fertilizer and industrial-chemical production now coexist as separate PM groups in the canonical `building_chemical_plant`. The inspected reference blocks were `common/buildings/ztr_vanilla_modified_buildings.txt`, `common/production_method_groups/ztr_vanilla_production_method_groups.txt`, and `common/production_methods/ztr_vanilla_production_methods.txt`.

The complex unlocks at `industrial_acids`, which Great Britain already possesses. `artificial_fertilizers` now improves complex throughput instead of gating the whole building. The early fertilizer PM uses limestone and tools; the fork's phosphate input is preserved in the improved and nitrogen-fixation PMs, where the advanced mining chain is appropriate. The obsolete separate `building_chemical_works` definition and placement were removed/migrated.

The consolidated building is presented in game as **Usine chimique** / **Chemical Works**. Its building illustration is a local copy of Tech & Res' `building_pharmaceuticals_industry.dds`, and `industrial_chemicals` uses a local copy of Tech & Res' `fertilizer.dds`. Both assets are namespaced inside this fork, so the runtime does not require Tech & Res to remain enabled.

## Infrastructure

Road levels were recalculated after the supply write against effective building-group usage and the +2 AI surplus target: BAHAMAS=2, BERMUDA=1, EAST_ANGLIA=7, FLORIDA=2, JAMAICA=6, LANCASHIRE=19, MIDLANDS=15, NEWFOUNDLAND=4, WEST_COUNTRY=14, WEST_INDIES=3, SENEGAL=16. No rail or passenger PM was introduced.

## Required runtime retest

Reload the mod and inspect the British market after employment stabilizes. Static capacity resolves the captured orders, but final prices and the BIC dependence score remain runtime outcomes.
