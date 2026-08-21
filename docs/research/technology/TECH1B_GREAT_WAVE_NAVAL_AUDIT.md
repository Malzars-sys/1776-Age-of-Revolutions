# TECH-1B — The Great Wave naval system and Ship Designer audit

Status: **PASS — research/audit only; no gameplay implementation performed.**  
Target: **Victoria 3 1.13.9 — The Great Wave / Matcha**  
Canonicality: recommendations are **INPUT_FOR_HUMAN_REVIEW / NOT_CANONICAL**.

## 1. Executive summary

Victoria 3 1.13.9 models a warship as an **entity using a runtime `ship_template` whose base hull/class is a `ship_type` and whose selectable parts are `ship_modification` objects assigned to allowed `ship_modification_slot` objects**. There is no separate scripted `hull`, `weapon`, `armor`, `role`, `design_archetype`, or static `design_template` family. The core index contains **21 ship types + 259 modifications + 7 slots + 4 groups = 291 objects**.

Warships are not market goods. They are built as entities through template-based construction orders using national `country_ship_construction_add` supplied by shipyard PMs. Their design supplies goods-dependent construction and ongoing materiel/upkeep requirements. Civil shipping remains abstract: shipyards produce `clippers`/`steamers`, ports produce convoy capacity, and trade consumes convoys.

The DLC boundary is split: the base 1.13 data model, default templates, ship construction/refit, naval buildings/PMs/combat, core flagships and AI are free-update content; **custom template authoring/editing**, the **ship-transfer treaty article**, three piracy mission types and certain presentation/ornament features are DLC-gated.

Key verdicts:

- `IRON_HULL_AND_IRONCLAD_ARE_MECHANICALLY_DISTINCT = PARTIAL`: type/base goods and armor modifications are separate mechanics, but vanilla gates `ship_type_iron_frigate` with `ironclad_tech` and gives it base armor.
- `COPPER_SHEATHING_VANILLA_SUPPORT = NONE`; best candidate is a utility/range component, with high DLC/default-template/AI risk.
- `DIAGONAL_FRAMING_VANILLA_SUPPORT = NONE`; a shipyard building modifier is safer than a new structural slot.
- The 25 TECH-1A items were recalculated and all are resolved in this research output.

## 2. Scope and methodology

The certified install was parsed directly, not inferred from comments alone. Inspected families include `common/ship_types`, `ship_modifications`, `ship_modification_slots`, `ship_groups`, `ship_veterancy_levels`, technologies, buildings, PM/PMG files, AI strategies/defines/script values, naval mission types, treaty articles, laws, history formations, on-actions/static modifiers, GUI/tooltips, English localization and EP2 package descriptors/assets. Exact paths were discovered before parsing. TECH-1A CSV/Markdown inputs and both Military Naval V1 files under `docs/reports/technology/` were used.

Counts use top-level Clausewitz objects. `SHIP_DESIGNER_OBJECTS_FOUND` intentionally means the four script families that constitute designs; runtime country templates and individual ship instances are not static top-level objects and are not falsely counted.

## 3. Certified version

- Source: `C:\Games\Victoria 3`
- Launcher target: 1.13.9 (Matcha)
- `caligula_branch.txt`: `release/1.13.9`
- `clausewitz_branch.txt`: `caligula/release/1.13.9`
- Audited content root: `C:\Games\Victoria 3\game`

## 4. Great Wave vs free-update separation

| System | Free 1.13 | Great Wave DLC | Gate/fallback |
|---|---:|---:|---|
| Designer definitions, types, modifications, slots, groups | yes | no | Base `common/` data; always loaded |
| Default templates, construction, retrofit | yes | no | Normal fleet controls remain |
| Create/edit/delete custom templates | no | yes | `HasDlcFeature('ship_designer')`; controls hidden |
| Ship sales/purchases | no | yes | `has_dlc_feature = ep2_content`; article absent from choices |
| Flagship status/bonuses/AI | yes | no | Core controls ungated |
| Flagship ornaments/presentation selector | no | yes | `HasDlcFeature('ship_designer')` |
| Hunt pirates / piracy / privateer missions | no | yes | `potential = { has_dlc_feature = ep2_content }` |

The full 18-row classification is in `TECH1B_NAVAL_DLC_MATRIX.csv`. Referencing core ship types/modifications is safe without EP2. Calling custom-designer UI, `ship_transfer`, EP2 mission types, or DLC presentation objects without an equivalent gate is unsafe.

## 5. Ship Designer architecture

```text
TECH (`unlocking_technologies`, OR semantics)
  ↓
`ship_type` + allowed `ship_modification` choices
  ↓
runtime `ship_template` (type + one choice per required slot + optional utility)
  ↓
ship construction order consuming country ship-construction capacity and design goods
  ↓
individual `ship` entity
  ↓
`military_formation` fleet and naval mission
```

```text
VANILLA HULL/CLASS = `ship_type`
  ├─ `ship_mod_slot_propulsion` → PROPULSION modifications
  ├─ `ship_mod_slot_guns`       → WEAPON modifications
  ├─ `ship_mod_slot_armor`      → PROTECTION modifications
  ├─ `ship_mod_slot_range`      → RANGE components
  └─ 0..3 utility slots         → UTILITY modifications
```

**DESIGN_REQUIRED_FIELDS.** A runtime template needs a valid available `ship_type`; the type supplies group, base stats/goods, allowed slots/modification lists and base cost. Non-utility slots exposed by that type receive a valid compatible selection; `default_modifications` seeds engine/default templates.

**DESIGN_OPTIONAL_FIELDS.** Custom name/graphics, utility selections, up to the utility slots exposed by the type, custom replacements of defaults, flagship status (belongs to a ship instance, not template).

**SLOT_RULES.** Seven slot objects exist: armor, guns, propulsion, range, utility 1–3. Each ship type explicitly lists which modifications are compatible in each slot. Utility mods may repeat across hulls but cannot be selected twice in different utility slots. Only slot definitions marked `utility=yes` may be empty.

**COMPATIBILITY_RULES.** Type allow-lists are authoritative. Modifications can declare repeated `incompatible_with`. GUI uses `IsModificationBlocked`; technology locks use `HasRequiredTech`.

**TECH_GATES.** `unlocking_technologies` on a ship type or modification is an OR list per the vanilla schema. The UI disables locked types/modifications and tooltips call `GetTechRequirements`. Hull obsolescence is a separate technology trigger and does not delete the type.

**COST_CALCULATION.** Ship types provide base/progress and per-modification construction cost plus construction goods. Modifications add goods/stats. Total complexity is scaled by `SHIP_CONSTRUCTION_COST_MODIFICATION_LEVEL_FACTOR = 1.05` raised to total modification levels; default balancing level is 2. Ongoing ship goods derive from type `materiel_goods` and global construction-to-upkeep factors (0.002), with docked upkeep multiplier −0.8.

**STAT_CALCULATION.** Base `ship_type.modifier` plus selected modification modifiers plus veterancy, country/fleet/mission/commander modifiers and damage/readiness. Combat-power formulas also use engine defines.

**DEFAULT_DESIGNS.** There is no static `ship_templates` data directory. Defaults are generated from each type and `default_modifications`; custom templates are runtime country data. The AI also generates improved templates dynamically.

**INVALID_DESIGN_BEHAVIOR.** GUI disables locked/incompatible choices; template lists filter on `ShipTemplate.IsValid`. The last template of a type, templates in use and templates under construction have deletion guards. Engine validation and runtime template serialization are not exposed as script schemas.

## 6. Hull system

No separate HULL family exists. All 21 hull/class/base-stat objects are `ship_type` definitions:

| Ship type | Group | Unlock | AI weight | Flagship eligible |
|---|---|---|---:|---:|
| `ship_type_ship_of_the_line` | `ship_group_capital_ships` | drydocks | 2 | yes |
| `ship_type_monitor` | `ship_group_capital_ships` | ironclad_tech | 0.1 | no |
| `ship_type_early_ironclad` | `ship_group_capital_ships` | ironclad_tech | 2 | yes |
| `ship_type_coastal_defense_ship` | `ship_group_capital_ships` | monitor_tech | 0.1 | no |
| `ship_type_modern_ironclad` | `ship_group_capital_ships` | monitor_tech | 2 | yes |
| `ship_type_pre_dreadnought` | `ship_group_capital_ships` | pre_dreadnought_tech | 2 | yes |
| `ship_type_dreadnought` | `ship_group_capital_ships` | dreadnought_tech | 2 | yes |
| `ship_type_super_dreadnought` | `ship_group_capital_ships` | battleship_tech | 2 | yes |
| `ship_type_frigate` | `ship_group_cruisers` | none | 1.5 | yes |
| `ship_type_iron_frigate` | `ship_group_cruisers` | ironclad_tech | 1.5 | yes |
| `ship_type_troop_ship` | `ship_group_cruisers` | ironclad_tech | 2 | no |
| `ship_type_protected_cruiser` | `ship_group_cruisers` | sea_lane_strategies | 1.5 | yes |
| `ship_type_armored_cruiser` | `ship_group_cruisers` | pre_dreadnought_tech | 1.5 | yes |
| `ship_type_light_cruiser` | `ship_group_cruisers` | dreadnought_tech | 1.5 | yes |
| `ship_type_seaplane_tender` | `ship_group_cruisers` | dreadnought_tech | 2 | yes |
| `ship_type_aircraft_carrier` | `ship_group_cruisers` | carrier_tech | 2 | yes |
| `ship_type_torpedo_boat` | `ship_group_torpedo_craft` | self_propelled_torpedoes | 1.5 | no |
| `ship_type_torpedo_boat_destroyer` | `ship_group_torpedo_craft` | sea_lane_strategies | 2 | yes |
| `ship_type_submarine` | `ship_group_torpedo_craft` | submarine | 2 | no |
| `ship_type_destroyer` | `ship_group_torpedo_craft` | destroyer | 2 | yes |
| `ship_type_supply_ship` | `ship_group_supply_ships` | none | engine | no |

Mechanical category findings:

- **COASTAL:** not a formal group; monitor/coastal-defense types have explicit distance-to-port/range penalties, so the role emerges mechanically.
- **BLUE_WATER:** no boolean/category; emerges from supply capacity, max distance, speed and range modifications.
- **RIVERINE:** absent.
- **MERCHANT:** absent from military ship entities; merchant capacity is abstract goods/convoys.
- **AUXILIARY:** partially explicit: `ship_group_supply_ships`, hardcoded `SUPPLY_SHIP_TYPE`, and troop/supply stats. No generic auxiliary role slot.

## 7. Propulsion

There are **63** propulsion modifications: three light/medium/high variants for each of 21 types. Vanilla does not expose universal semantic component IDs named sail, paddle, screw, turbine, diesel or oil. The historical machinery is distributed across hull gates, levelled per-hull propulsion mods, construction/materiel goods and technology.

- Early frigate and ship-of-the-line medium propulsion mods require `atmospheric_engine`; their high mods require `watertube_boiler`.
- `paddle_steamer` gives direct naval damage modifiers and is a prerequisite for `screw_frigate`; it does **not** directly unlock a component.
- `screw_frigate` unlocks active `pm_complex_shipbuilding` and also gates the unreferenced `pm_military_shipbuilding_wooden_2`; it does not unlock a ship type/modification.
- Later propulsion component availability is largely inherited from the gated ship type rather than individually gated.
- Coal/oil are materiel or construction inputs on relevant ship types/designs; there is no separate fuel-tank system.

Thus propulsion technology can affect **multiple systems**: direct modifiers, shipyard PMs, hull/class access and selected components. It is not consistently A, B or C.

## 8. Weapons

There are **61** guns-slot modifications plus weapon-like utility mods. `shell_gun` directly unlocks the high guns mods for frigate and ship-of-the-line, making `Naval Shell Guns → WEAPON_UNLOCK` the strongest exact V1 mapping. `breech_loading_artillery` and `self_propelled_torpedoes` also gate relevant modification/utility content; torpedo-boat hull access is separately tech-gated.

Vanilla weapon stats are aggregate hull damage, crew damage, accuracy, critical chance/multiplier, screening and target-type accuracy. There are no generic designer fields for penetration, reload, primary/secondary battery or ammunition magazine. Carronades exist as a utility modification. Torpedoes span hull types and utility protection/offense, not a universal torpedo weapon slot. Machine-gun, anti-air and missile categories are not separate naval designer families.

## 9. Protection

There are **63** armor-slot modifications. Protection is the sum of ship-type base armor/hit points/vulnerability, selected armor modification and utility systems such as torpedo nets/fire suppression.

Wood, iron and steel are not an enum called `hull_material`; they appear in ship-type identities, base construction/materiel goods and stats. Iron/steel armor is likewise not a single reusable material component.

`IRON_HULL_AND_IRONCLAD_ARE_MECHANICALLY_DISTINCT = PARTIAL`

- Distinct at data-model level: structural class/type and construction goods are separate from the armor slot.
- Not distinct in current early vanilla progression: `ship_type_iron_frigate` requires `ironclad_tech` and has base armor 17.
- Engine capability: a data-driven iron-goods ship type with zero/low base armor and optional armor could precede ironclads.
- Existing content capability: vanilla supplies no civil iron merchant-ship entity and no pre-ironclad iron-hull unlock.

## 10. Shipbuilding pipeline

```text
Production technologies and goods
(wood/hardwood/fabric/iron/steel/engines/coal/electricity…)
        ↓
`building_shipyard` PMs → clippers/steamers + `country_ship_construction_add`
        ↓
Military technology gates `ship_type` and `ship_modification`
        ↓
template-based construction order
        ↓
ship entity → assignment to a fleet
```

Answer: **B + C**. Warships are entities constructed via orders. They are neither a market good nor a converted clipper/steamer good. Shipyard output goods support the civil economy, while its country modifier supplies military ship-construction capacity.

The construction queue and exact weekly advancement are engine/runtime systems exposed to GUI (`QueueShipTemplateConstruction`, template construction progress/cost). Design cost combines type and component goods/cost. Maintenance shortages can damage ships under construction according to defines. Repair occurs by fleet recall/docking and maintenance/supply logic. Retrofit is a queued change from current to target template; AI requires a 2× score improvement.

## 11. Shipyards

Exactly one `building_shipyard` exists. It is coastal, unlocked by `navigation`, references one base PMG and produces both civil ship goods and national military ship-construction capacity.

Nine shipbuilding-labelled PM definitions were found, but only four are wired to the building:

- **Active/wired:** `pm_basic_shipbuilding`, `pm_complex_shipbuilding`, `pm_metal_shipbuilding`, `pm_arc_welding_shipbuilding` (capacity 5/10/15/20 plus clippers/steamers) through `pmg_base_building_shipyard`.
- **Unwired definitions:** `pm_no_military_shipbuilding`, wooden, wooden_2, steam and steam_2 (nominal capacity 0/2/5/10/15). `pmg_military_base` has no reference outside its own definition and the `pm_no` method belongs to no PMG. No runtime hardcoding was evidenced, so these cannot be treated as active.

There is no separate buildable `military_shipyard` or dockyard building. `building_naval_administration` recruits sailors; `building_naval_fortification` protects coast/straits; `building_naval_logistics_center` is an automatically managed supply hub.

The same topology warning applies to `pmg_naval_theory`: its five doctrine PMs exist but the PMG is referenced by no building. Navy doctrine is actively represented by the navy-model laws and AI strategy, not by an evidenced active naval-administration PMG.

V1 mapping: State Dockyard Systems uses building/capacity access; Enclosed Dock Systems remains a separate civil port/trade PM concept and must **not** be merged into military `drydocks`; Mechanized Naval Dockyards aligns with shipyard PM/capacity, especially `gantry_cranes → pm_metal_shipbuilding`.

## 12. Ports

Exactly one `building_port` exists. It is coastal, unlocked by `navigation`, flagged `port=yes`, and has three PMs: `pm_basic_port`, `pm_industrial_port` (`gantry_cranes`) and `pm_modern_port` (`concrete_dockyards`). Ports provide the civil convoy/infrastructure interface and friendly-port supply-distance discount; they do not directly build military ships.

Naval range/supply/repair interactions are engine-mediated by docking, friendly ports, fleet supply and ship design. Lighthouses, hydrographic offices and classification societies are not separate buildings.

## 13. Civil maritime systems

| Concept | Representation | Verdict |
|---|---|---|
| Merchant shipping | clippers/steamers goods, convoys, trade routes | DIRECT/ABSTRACT, not Designer |
| Civil shipyards | `building_shipyard` and base PMG | DIRECT |
| Ports/convoys | `building_port` and port PMs | DIRECT |
| Commercial steamships | `steamers` output after metal shipbuilding | INDIRECT to historical paddle steam |
| Marine chronometry | generic navigation/range only | INDIRECT |
| Classification/surveying | no institution or inspection system | NOT REPRESENTED |
| Hydrography | generic reach/map/mission systems | INDIRECT |
| Maritime safety | generic convoy/ship loss and port systems | INDIRECT |
| Lighthouses | no object | NOT REPRESENTED |

Whaling has wooden/steam whaling PMs but remains an economic resource building, not a ship designer or military construction path.

`NAVAL_PMS_FOUND = 31` uses the audit-wide civil + military scope: 22 core naval-labelled definitions plus 9 civil-maritime PMs for merchant-marine trade quantity, fishing trawlers and whaling vessels. Of the 22 core definitions, 12 are topologically wired and 10 are unreferenced/orphaned (five military shipbuilding and five naval-theory PMs). All 9 civil-maritime PMs are wired; they never supply warship-construction capacity.

## 14. Fleet integration

Fleets are `military_formation` runtime entities. Construction controls select a ship template and queue a ship for a fleet. Individual ships retain their type/template; change-template controls queue retrofit. Obsolete classes remain selectable behind UI toggles, while AI uses obsolescence triggers, bounded decommissioning and retrofit thresholds. Loss replacement is driven by desired group counts and queued construction, not by producing generic naval-unit goods.

Historical setup files under `common/history/military_formations/` use `create_ship = { type = ship_type:ship_type_… }` (and may mark `flagship = yes`). They reference **ship type directly**, not a separate hull or static design ID. This is a migration risk for 1776 starting fleets if type gates/identity change.

Range is mixed: ship supply capacity/max distance and range mods; fleet supply/mission sea-region limits; country modifiers; port distance discounts; mission supply scaling; travel network and strategic-region topology. There is no single `naval_range` technology switch.

## 15. Flagships

Core flagship status is one designated eligible ship per country. Fifteen of 21 ship types have `can_be_flagship=yes`; monitors, coastal-defense ships, troop ships, torpedo boats, submarines and supply ships are ineligible. Assignment/replacement is a ship action with a 60-month cooldown. Transferring or decommissioning a flagship removes/warns about the status.

Static/on-action effects cover battle won, battle lost, flagship destroyed and interest gain. AI scores fleets by projection/size/capital count and ships by projection/capital group, with 1.5× stickiness. No technology directly unlocks flagship status beyond the selected type’s gate. Core logic is free; ornament/figurehead presentation is DLC-feature gated.

## 16. Ship sales/purchases

`common/treaty_articles/31_ship_transfer.txt` defines a directed, giftable, enforced treaty article. It requires a specific non-destroyed ship outside battle; buyer needs a port. Entry force calls `set_ship_owner_multiple`. Price/AI acceptance uses `ai_ship_value`, binding weeks, replacement value and obsolescence for seller/buyer. It is gated by `ep2_content`.

The article has **no buyer technology trigger**. Therefore a country can receive and use a ship whose type/components it could not currently design. Consequences:

- A — use the transferred ship: **YES**, the instance is transferred.
- B — unlock technology: **NO**, no research effect occurs.
- C — unlock/import a reusable design: **NOT SUPPORTED IN SCRIPT; runtime template ownership behavior is engine-sensitive**.
- D — reproduce it without technology: **NO supported path found; creation/UI availability remains tech-gated**.
- E — other: flagship status is removed on transfer.

No license mechanic was found.

## 17. Technology gating

Fifteen unique technologies directly gate Designer objects: `atmospheric_engine, battleship_tech, breech_loading_artillery, carrier_tech, destroyer, dreadnought_tech, drydocks, ironclad_tech, monitor_tech, pre_dreadnought_tech, sea_lane_strategies, self_propelled_torpedoes, shell_gun, submarine, watertube_boiler`. The technology-effect CSV records every type/modification unlock, obsolescence gate, naval building/PM gate, navy-law compatibility gate and direct naval modifier found.

Notable exact patterns:

- `navigation` → shipyard + port building unlock.
- `drydocks` → ship-of-the-line type.
- `shell_gun` → two early high guns modifications.
- `atmospheric_engine` / `watertube_boiler` → early propulsion mods.
- `ironclad_tech`, `monitor_tech`, `pre_dreadnought_tech`, `dreadnought_tech`, `battleship_tech`, `carrier_tech`, `destroyer`, `submarine` → ship types and/or components.
- `screw_frigate`, `gantry_cranes`, `arc_welding` → the active shipyard PM progression. `ironclad_tech` gates an unreferenced legacy military-shipbuilding PM definition, not an evidenced active shipyard PM.
- `power_of_the_purse`, `jeune_ecole`, `sea_lane_strategies`, `battlefleet_tactics` → naval-administration doctrine PMs.

## 18. AI ship design

The AI uses a combined method:

1. engine/default templates exist for every usable type;
2. AI dynamically generates improved templates from available type allow-lists and modification weights;
3. existing/runtime templates are compared by score;
4. historical setup creates types directly, after which runtime templates apply.

```text
AI strategy + navy law + researched tech
        ↓
desired ship groups and maximum design complexity
        ↓
type/modification AI weights × market-input multiplier × random factor
        ↓
valid/compatible candidate; new template only if ≥1.5× current best
        ↓
construction allocation; retrofit only if ≥2× current design
```

Resource sensitivity is explicit through `ship_modification_market_demand_ratio`; technology locks and incompatibility filter choices. There is no explicit coastal-versus-blue-water composition dimension, only ship groups and the individual type scores. This is an important modding limitation.

## 19. AI shipbuilding

Desired navy size, supply-ship count, group ratios, construction output and fleet roles are strategy values. Navy laws shift capital/cruiser/torpedo ratios; `self_propelled_torpedoes` activates torpedo-craft demand. Debt pauses construction; sailor shortage blocks it; existing fleet cost reserves capacity for repair/retrofit. AI expands strategic naval fortifications and relies on general building AI to satisfy shipyard/naval-administration capacity.

Risk audit:

- `AI_HAS_TECH_BUT_DOES_NOT_BUILD`: HIGH if rewired techs lack shipyard PMs or required goods.
- `NO_INPUT_BOOTSTRAP`: HIGH when new component costs require unavailable industrial chains.
- `OBSOLETE_DESIGN_SPAM`: MEDIUM if obsolescence and new unlocks fire too close together.
- `EXPENSIVE_FLAGSHIP_SPAM`: LOW; flagship is designation, not a unique construction order.
- `COASTAL_STATE_BUILDS_BLUE_WATER_ONLY`: MEDIUM because no explicit composition axis exists.
- `AI_BUILDING_LOOP`: MEDIUM if custom wanted-capacity modifiers double-count existing strategy values.

## 20. UI constraints

The popup obtains slots dynamically with `GetModificationSlots`, but its presentation explicitly compares slot IDs for armor, guns, propulsion and range; sound/graphics defines hardcode the propulsion slot. Utility slots use a generic menu. Adding more modifications within existing slots is data-driven. Adding a new slot or category needs custom GUI/tooltips/sounds and is engine-sensitive.

Locked hulls/modifications remain visible but disabled via `HasRequiredTech`, with localized requirements tooltips. Incompatibility uses blocked state. Cost bars expose construction points/weeks and component-level cost. All 291 objects have a resolved name-localization key and an existing icon file. Only 36 have a dedicated description key; the other 255 rely on generated stat/technology/compatibility tooltips. There are 44 unique icon combinations, with 263 objects sharing one of 16 repeated paths, chiefly the low/mid/high designer conventions. The future `gfx/error_manul.dds` policy was observed but not applied.

## 21. Technology-transfer possibilities

| Mechanism | Classification | Basis |
|---|---|---|
| Ship purchase/transfer | SUPPORTED_INDIRECTLY | A foreign-tech ship can be used; no research/design unlock occurs |
| Capture | UNKNOWN | No general scripted capture/reverse-engineering pipeline found |
| Design import | NOT_SUPPORTED | No license/import effect or static design ownership script found |
| Foreign construction | UNKNOWN | Transfer can deliver a ship; no distinct foreign-build order system found |
| Event-based reverse engineering | SUPPORTED_INDIRECTLY | Events/scripted effects can test owned ships and grant research separately, but this would be custom logic |

## 22. Mapping to Military V1

| V1 node | Engine representation | Primary verdict | Risk |
|---|---|---|---|
| `state_dockyard_systems` | MULTIPLE | **KEEP_AS_TECH** | LOW |
| `enclosed_dock_systems` | PORT_PM | **USE_PM_UNLOCK** | MEDIUM |
| `scientific_naval_architecture` | COUNTRY_MODIFIER | **USE_COUNTRY_MODIFIER** | MEDIUM |
| `marine_chronometry` | COUNTRY_MODIFIER | **USE_COUNTRY_MODIFIER** | LOW |
| `ship_classification_surveying` | COUNTRY_MODIFIER | **USE_COUNTRY_MODIFIER** | MEDIUM |
| `copper_sheathing` | COMPONENT | **USE_COMPONENT_UNLOCK** | HIGH |
| `hydrographic_surveying` | COUNTRY_MODIFIER | **USE_COUNTRY_MODIFIER** | LOW |
| `standardized_naval_signals` | FLEET_MODIFIER | **USE_COUNTRY_MODIFIER** | LOW |
| `paddle_steam_navigation` | MULTIPLE | **USE_PROPULSION_UNLOCK** | HIGH |
| `mechanized_naval_dockyards` | SHIPYARD_PM | **USE_PM_UNLOCK** | MEDIUM |
| `diagonal_ship_framing` | COUNTRY_MODIFIER | **USE_BUILDING_MODIFIER** | MEDIUM |
| `naval_shell_guns` | WEAPON | **USE_WEAPON_UNLOCK** | LOW |
| `maritime_safety_standards` | COUNTRY_MODIFIER | **USE_COUNTRY_MODIFIER** | MEDIUM |
| `modern_lighthouse_optics` | COUNTRY_MODIFIER | **USE_BUILDING_MODIFIER** | LOW |
| `iron_hull_construction` | SHIP_TYPE | **REWIRE_VANILLA_TECH** | HIGH |

The full mapping CSV contains vanilla IDs, dependencies and rationale. These verdicts are not canonical and must be human-reviewed before TECH integration.

## 23. TECH-1A deferred items resolved

Recalculated deferred set: **25 expected, 25 found, 25 resolved**.

| Deferred tech | Indexed relations | Evidence sample | Status |
|---|---:|---|---|
| `admiralty` | 1 | BUILDING_UNLOCK:building_naval_administration | RESOLVED |
| `battlefleet_tactics` | 1 | PM_UNLOCK:pm_battlefleet_tactics | RESOLVED |
| `battleship_tech` | 5 | AI_GATE:ship_type_armored_cruiser; AI_GATE:ship_type_dreadnought; AI_GATE:ship_type_pre_dreadnought; AI_GATE:ship_type_protected_cruiser; HULL_UNLOCK:ship_type_super_dreadnought | RESOLVED |
| `breech_loading_artillery` | 2 | PM_UNLOCK:pm_naval_fortification_reinforced; WEAPON_UNLOCK:ship_mod_iron_frigate_guns_high | RESOLVED |
| `carrier_tech` | 2 | AI_GATE:ship_type_seaplane_tender; HULL_UNLOCK:ship_type_aircraft_carrier | RESOLVED |
| `concrete_dockyards` | 2 | MODIFIER:ship_ship_type_supply_ship_supply_capacity_mult; PM_UNLOCK:pm_modern_port | RESOLVED |
| `destroyer` | 3 | AI_GATE:ship_type_torpedo_boat; AI_GATE:ship_type_torpedo_boat_destroyer; HULL_UNLOCK:ship_type_destroyer | RESOLVED |
| `dreadnought_tech` | 8 | AI_GATE:ship_type_armored_cruiser; AI_GATE:ship_type_coastal_defense_ship; AI_GATE:ship_type_modern_ironclad; AI_GATE:ship_type_monitor; AI_GATE:ship_type_pre_dreadnought; HULL_UNLOCK:ship_type_dreadnought … | RESOLVED |
| `drydocks` | 1 | HULL_UNLOCK:ship_type_ship_of_the_line | RESOLVED |
| `floating_harbor` | 1 | PM_UNLOCK:pm_trade_center_trade_quantity_very_high | RESOLVED |
| `gantry_cranes` | 5 | MODIFIER:ship_ship_type_supply_ship_supply_capacity_mult; PM_UNLOCK:pm_industrial_port; PM_UNLOCK:pm_metal_shipbuilding; PM_UNLOCK:pm_steam_trawlers; PM_UNLOCK:pm_steam_whaling_ships | RESOLVED |
| `hydraulic_cranes` | 1 | PM_UNLOCK:pm_trade_center_trade_quantity_high | RESOLVED |
| `ironclad_tech` | 10 | AI_GATE:ship_type_frigate; AI_GATE:ship_type_ship_of_the_line; COMPONENT_UNLOCK:ship_mod_supply_ship_armor_medium; HULL_UNLOCK:ship_type_early_ironclad; HULL_UNLOCK:ship_type_iron_frigate; HULL_UNLOCK:ship_type_monitor … | RESOLVED |
| `landing_craft` | 1 | UNLOCK:combat_unit_type_high_tier_marines | RESOLVED |
| `monitor_tech` | 9 | AI_GATE:ship_type_early_ironclad; AI_GATE:ship_type_frigate; AI_GATE:ship_type_monitor; AI_GATE:ship_type_ship_of_the_line; COMPATIBILITY:law_diplomatic_navy; COMPATIBILITY:law_jeune_ecole … | RESOLVED |
| `navigation` | 2 | BUILDING_UNLOCK:building_port; BUILDING_UNLOCK:building_shipyard | RESOLVED |
| `paddle_steamer` | 2 | MODIFIER:ship_crew_damage_mult; MODIFIER:ship_hull_damage_mult | RESOLVED |
| `pre_dreadnought_tech` | 12 | AI_GATE:ship_type_coastal_defense_ship; AI_GATE:ship_type_early_ironclad; AI_GATE:ship_type_iron_frigate; AI_GATE:ship_type_modern_ironclad; AI_GATE:ship_type_protected_cruiser; COMPATIBILITY:law_diplomatic_navy … | RESOLVED |
| `screw_frigate` | 2 | PM_UNLOCK:pm_complex_shipbuilding; PM_UNLOCK:pm_military_shipbuilding_wooden_2 | RESOLVED |
| `sea_lane_strategies` | 8 | AI_GATE:ship_type_iron_frigate; AI_GATE:ship_type_torpedo_boat; COMPATIBILITY:law_diplomatic_navy; COMPATIBILITY:law_jeune_ecole; COMPATIBILITY:law_professional_navy; HULL_UNLOCK:ship_type_protected_cruiser … | RESOLVED |
| `self_propelled_torpedoes` | 2 | COMPONENT_UNLOCK:utility_mod_torpedo_nets; HULL_UNLOCK:ship_type_torpedo_boat | RESOLVED |
| `shell_gun` | 2 | WEAPON_UNLOCK:ship_mod_frigate_guns_high; WEAPON_UNLOCK:ship_mod_ship_of_the_line_guns_high | RESOLVED |
| `submarine` | 1 | HULL_UNLOCK:ship_type_submarine | RESOLVED |
| `atmospheric_engine` | 2 | PROPULSION_UNLOCK:ship_mod_frigate_propulsion_medium; PROPULSION_UNLOCK:ship_mod_ship_of_the_line_propulsion_medium | RESOLVED |
| `watertube_boiler` | 2 | PROPULSION_UNLOCK:ship_mod_frigate_propulsion_high; PROPULSION_UNLOCK:ship_mod_ship_of_the_line_propulsion_high | RESOLVED |

`landing_craft` is naval-adjacent rather than Designer content: it gates a land combat unit/landing entity and participates in AI invasion logic. `hydraulic_cranes`/`floating_harbor` concern broader logistics/port-like PMs. They remain resolved because their actual subsystem was identified rather than forced into the Designer.

## 24. Hardcoded/engine-sensitive areas

| Area | Classification | Evidence/risk |
|---|---|---|
| Ship types/modifications/groups | DATA_DRIVEN | Script objects and allow-lists |
| Slot definitions | MIXED | Data-driven objects; GUI/sounds explicitly know core IDs |
| Runtime templates/validation | MIXED | Data inputs, engine-owned serialization/actions |
| Combat roles/formulas | MIXED | Script stats plus engine battle calculations/defines |
| Naval range/supply | MIXED | Data modifiers plus engine pathing/topology |
| Construction/orders/repair/refit | MIXED | Script costs/capacity, engine queues/actions |
| Supply ship | HARDCODED | `SUPPLY_SHIP_TYPE`; define warns changes break things |
| Ship purchase/sale | SCRIPTED + ENGINE | Treaty article/effects plus engine ownership/template behavior |
| Flagships | MIXED | Data eligibility/modifiers and engine one-per-country action/cooldown |
| AI design | MIXED | Script weights/strategies/defines and engine generator/scorer |
| DLC gating | MIXED | Script `ep2_content`, GUI `ship_designer`, package loading |
| Historical fleets | SCRIPTED | `create_ship` references `ship_type` directly |

`HARDCODED_OR_ENGINE_SENSITIVE_ITEMS = 10` counts the mixed/hardcoded functional areas above, excluding purely data-driven object definitions and purely scripted history.

## 25. DLC compatibility risks

Five high-level EP2-only feature groups were found. Main risks are: unguarded calls to custom-template UI; references to `ship_transfer`; EP2 piracy mission references; DLC-only ornament/presentation assets; and assuming custom component choice is player-accessible without the Designer DLC. Core type/mod definitions themselves are safe, but a custom component still needs valid default templates and AI behavior for non-DLC users.

## 26. Implementation recommendations

1. Keep all future naval technology nodes in Military; do not add a fourth Naval technology category.
2. Prefer existing slots and exact `ship_modification`/`ship_type` schemas. Avoid new slot categories until a GUI/AI/DLC compatibility prototype proves safe.
3. Treat civil shipping via shipyard/port PMs and country/state modifiers; do not force lighthouses, classification or safety into warship components.
4. Separate Iron Hull Construction from Ironclad Technology by gate/representation during a later implementation phase; do not merge them.
5. Pair every new component/hull gate with default-template, AI-weight, goods-bootstrap, obsolescence and historical-formation tests.
6. Gate EP2 features explicitly and provide a base fallback.
7. Preserve the 15-node mapping as review input only; implement nothing until human approval.

## 27. Open questions

- Runtime ownership/serialization of a transferred foreign ship template is engine-side and cannot be proven from script alone.
- Exact non-DLC custom-modification discoverability should be verified in a controlled in-game run with EP2 disabled.
- Capture and foreign construction lack a documented script path in the certified files.
- New slot/category support cannot be declared safe without UI, AI and save-serialization testing.
- Historical semantics and final dates for V1 nodes remain a human design decision.

## 28. Final verdict

All requested research indices and mappings were produced from the certified 1.13.9 source. All static Designer object families and all relevant technology references, AI systems, civil maritime links, DLC gates and 15 Military V1 nodes were audited. No gameplay, technology, ship, component, PM, building, formation, port, shipyard or AI file was changed.

### Consistency controls

```text
ALL_SHIP_DESIGN_OBJECTS_INDEXED = YES
ALL_NAVAL_TECH_REFERENCES_AUDITED = YES
ALL_TECH1A_DEFERRED_ITEMS_RESOLVED = YES
ALL_MILITARY_V1_NAVAL_NODES_MAPPED = YES
DLC_GATING_AUDITED = YES
AI_DESIGN_AUDITED = YES
AI_SHIPBUILDING_AUDITED = YES
CIVIL_MARITIME_AUDITED = YES
GAMEPLAY_FILES_CHANGED = 0
```

### Machine-count summary

```text
SHIP_DESIGNER_OBJECTS_FOUND = 291
HULLS_FOUND = 21
PROPULSION_COMPONENTS_FOUND = 63
WEAPON_COMPONENTS_FOUND = 61
PROTECTION_COMPONENTS_FOUND = 63
OTHER_COMPONENTS_FOUND = 72
NAVAL_TECHS_REFERENCING_DESIGNER = 15
SHIPYARD_BUILDINGS_FOUND = 1
PORT_BUILDINGS_FOUND = 1
NAVAL_PMS_FOUND = 31
GREAT_WAVE_ONLY_FEATURES = 5
FREE_1_13_FEATURES = 13
OTHER_DLC_FEATURES = 0
```
