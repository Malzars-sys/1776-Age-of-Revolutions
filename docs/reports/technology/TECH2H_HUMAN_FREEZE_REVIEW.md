# TECH-2H — Human Freeze Review

Status: `PASS` · Scope: documentary design audit only · Baseline: Victoria 3 1.13.9 · Gameplay files changed: `0`

## 1. Freeze decision

The 1700–1836 architecture is ready to freeze after three documentary corrections:

1. Diagonal Ship Framing now gates the two existing vanilla Seppings-Braced Hull modifications directly. The planned duplicate shipyard/building modifier is removed.
2. Copper Sheathing moves from proposed `ship_mod_slot_utility_1` to existing `ship_mod_slot_utility_2`, subject to implementation-time type/default/runtime validation. The copper good remains deferred.
3. Vanilla `international_relations` is restored as its own Society node. TECH-1A classified the former match to scientific exchange as `NAME_COLLISION_ONLY`, so its diplomatic unlocks cannot be transferred to a science node.

All 21 original SPLIT actions, all 277 indexed relationships carried by their 34 vanilla source technologies, all 30 proposed cross-branch edges and all 19 Era VI nodes were reviewed. The matrix assigns every indexed relationship exactly once.

## 2. Diagonal Ship Framing / Seppings

Direct vanilla 1.13.9 inspection found two distinct object IDs sharing the localization key `ship_mod_seppings_braced_hull` (“Seppings-Braced Hull”; French: “Coque aux renforts de Seppings”):

| Vanilla object | Slot | Compatible ship type | Effects | Construction cost | Current technology gate |
|---|---|---|---|---|---|
| `ship_mod_frigate_armor_medium` | `ship_mod_slot_armor` | `ship_type_frigate` | `ship_armor_add = 7`; `ship_hit_points_max_add = 150` | hardwood 10 | none |
| `ship_mod_ship_of_the_line_armor_medium` | `ship_mod_slot_armor` | `ship_type_ship_of_the_line` | `ship_armor_add = 13`; `ship_hit_points_max_add = 400` | hardwood 15 | none |

Both objects have AI weight base 2 multiplied by `ship_mod_market_multiplier`. They are present in the armor allow-lists of the corresponding ship types. Neither object declares `unlocking_technologies`; the ship of the line itself is unlocked by vanilla `drydocks`, while the frigate is a base wooden type.

The relevant vanilla sources are:

- `C:/Games/Victoria 3/game/common/ship_modifications/00_ship_modifications.txt`
- `C:/Games/Victoria 3/game/common/ship_types/00_ship_types.txt`
- `C:/Games/Victoria 3/game/common/ship_modification_slots/00_ship_modification_slots.txt`
- `C:/Games/Victoria 3/game/localization/english/ship_designer_l_english.yml`
- `C:/Games/Victoria 3/game/localization/french/ship_designer_l_french.yml`

Historically, this is not merely adjacent to Diagonal Ship Framing: it is the same structural family. Royal Museums Greenwich describes Seppings’ improved construction as diagonal wood riders, longitudinal/truss pieces and diagonal deck work, and identifies him with experiments in diagonal stressing. See the [Caledonia sectional model](https://www.rmg.co.uk/collections/objects/rmgc-object-68492), the [circa-1812 frigate model](https://www.rmg.co.uk/collections/objects/rmgc-object-68264), and the [Seppings collection biography](https://www.rmg.co.uk/collections/objects/rmgc-object-14492).

Verdict: **A — Diagonal Ship Framing directly unlocks both existing vanilla medium-armor Seppings objects.** It is no longer a separate shipyard modifier. This avoids duplicate mechanics and preserves vanilla vocabulary.

## 3. Copper Sheathing

`ship_mod_slot_utility_1` is not safe for Copper Sheathing on the two wooden types. It already contains patrol boats and large carronades on frigates, plus landing skiffs on ships of the line. Copper sheathing would therefore become mutually exclusive with unrelated operational fittings. The armor slot is reserved for Seppings bracing, while the range slot must remain available for stowage/range selection.

The selected design is:

- real `ship_modification`;
- existing `ship_mod_slot_utility_2` definition;
- add that existing slot and the Copper Sheathing object only to the wooden frigate and ship-of-the-line allow-lists;
- no new slot definition;
- no hard dependency between Copper Sheathing and Diagonal Ship Framing;
- validate empty/locked-slot behavior, defaults, custom templates, AI weights and non-DLC behavior during implementation.

This keeps copper sheathing compatible with Seppings reinforcement and avoids conflicts with range and utility-1 fittings. It is a frozen design direction, not a runtime certification. The future cost is `UNRESOLVED_PENDING_IMPLEMENTATION_DESIGN`; the copper good remains `DEFERRED`.

## 4. Audit of the 21 SPLIT actions

The 21 actions originally referenced 34 vanilla technologies. TECH-2H audited 277 indexed relationships: 173 `UNLOCK`, 65 `PREREQUISITE`, 38 `MODIFIER`, and 1 `EVENT_EFFECT`. The row-level authority is `TECH2H_VANILLA_SPLIT_UNLOCK_MATRIX.csv`.

| Integrated SPLIT action | Original vanilla sources reviewed | Indexed relationships | Freeze disposition |
|---|---|---:|---|
| `coke_smelting` | `steelworking` | 11 | early coke/pig-iron content transferred; steel mill content goes to Puddling & Rolling; Bessemer remains a later bridge |
| `advanced_crop_rotations` | `intensive_agriculture` | 9 | rotations/soil PMs retained here; chemical/fertilizer descendants go to Industrial Acids; sheep content to Selective Breeding |
| `applied_mineralogy` | `prospecting` | 3 | gold/prospecting objects transferred to applied mineral knowledge |
| `interchangeable_manufacture` | `manufacturies`; `mechanized_workshops` | 20 | generic manufacture retained; textile, paper, glass and machinery relationships routed to their closest material descendants |
| `state_dockyard_systems` | `admiralty`; `drydocks`; `power_of_the_purse` | 10 | naval administration/wooden capital-ship responsibility retained; steam/mechanized successors routed forward |
| `regulated_small_arms` | `gunsmithing`; `line_infantry` | 13 | arms buildings/line equipment retained; artillery, percussion and drill relations routed to their own nodes |
| `standardized_field_artillery` | `artillery` | 4 | cannon unit/PM retained; shell and corps-era successors stay distinct |
| `marine_chronometry` | `navigation` | 6 | navigation responsibility retained; dockyard/port objects remain with naval infrastructure descendants |
| `corps_organization` | `army_reserves`; `mandatory_service`; `napoleonic_warfare`; `standing_army` | 23 | organizational objects retained; logistics, general staff, horse artillery and drill routed to their closer nodes |
| `battlefield_evacuation` | `triage` | 3 | war nursing and first aid retained; Modern Nursing prerequisite routed to Medical Degrees |
| `institutionalized_scientific_exchange` | `academia`; `empiricism`; original `international_relations` bundle | 36 | 18 science/education relationships split normally; all 18 diplomatic relationships restored to vanilla `international_relations` |
| `institutionalized_public_credit` | `banking`; `central_banking` | 12 | public-finance relationships retained; stock-market successors routed to Stock Exchange |
| `commercial_insurance_markets` | `international_trade` | 11 | commercial/trade institutions retained; currency/stock relations routed to their own nodes |
| `periodical_print_networks` | `mass_communication` | 5 | early communication/print responsibility retained; later mechanization remains distinct |
| `systematic_administrative_statistics` | `central_archives`; `tech_bureaucracy` | 16 | administrative objects distributed among statistics, registration, archives and professional policing |
| `codified_practical_knowledge` | `rationalism` | 7 | intellectual content retained; formal school relationships routed to Organized Elementary Schooling |
| `systematic_population_registration` | `centralization` | 9 | registration/filing content retained; general state-capacity objects routed to Administrative Statistics |
| `constitutional_government` | `democracy` | 10 | constitutional/law content retained; rights and mass-communication successors routed separately |
| `national_sovereignty` | `nationalism`; `pan-nationalism` | 58 | mature unlocks remain on the original post-1836 vanilla nodes; the new node is only the early antecedent |
| `scientific_metrology` | `currency_standards` | 2 | standards/currency responsibility retained |
| `active_principle_pharmacy` | `pharmaceuticals`; `quinine` | 9 | early chemical/medical capability retained; colonial/mature quinine content stays on post-1836 vanilla `quinine` |

Matrix validation:

- source vanilla technologies reviewed: 34;
- relationships emitted: 277;
- targets missing from the integrated tree or an explicit `VANILLA_PRESERVED:` bridge: 0;
- unassigned rows: 0;
- duplicate source relationships: 0;
- orphan building, PM, law, unit, ship, modifier or other indexed object: 0.

## 5. Review of the 30 cross-branch dependencies

`WEAKEN` means the relationship may remain in AI context, descriptions, adoption weighting or implementation notes, but no longer blocks research. `CROSS_BRANCH_CHANGED` counts these 11 weakenings. The final hard graph contains 14 cross-branch edges.

| # | Proposed edge | Verdict | Human-review reason |
|---:|---|---|---|
| 1 | Scientific Exchange → Industrial Acids | REMOVE | acids do not materially require an international scientific institution |
| 2 | Public Credit → Industrial Canals | WEAKEN | finance accelerates canals but is not a universal technical prerequisite |
| 3 | Administrative Statistics → Industrial Canals | WEAKEN | state survey capacity helps execution but private/local canals existed without it |
| 4 | Scientific Exchange → Applied Mineralogy | WEAKEN | exchange aids diffusion but practical mineralogy can develop locally |
| 5 | Scientific Exchange → Industrial Ceramics | REMOVE | craft and industrial ceramic advances do not require the institution |
| 6 | Standardized Field Artillery → Precision Boring | KEEP | artillery demand is a genuine driver for reproducible boring |
| 7 | Polytechnical Education → Professional Civil Engineering | WEAKEN | professional engineers existed through apprenticeship and societies as well as schools |
| 8 | Cadastral Surveying → Geological Surveying | WEAKEN | land cadastre supplies useful maps but is not a scientific prerequisite |
| 9 | Scientific Metrology → Geological Surveying | WEAKEN | standards improve comparability without being required for field geology |
| 10 | Precision Boring → Armament Inspection | KEEP | reproducible precision gives the material basis for systematic gauges/inspection |
| 11 | Technical Academies → Permanent Engineer Services | WEAKEN | military engineer corps can predate specialized technical academies |
| 12 | Administrative Statistics → Military Topographic Surveying | WEAKEN | state information capacity helps but military survey services can be autonomous |
| 13 | Coke Smelting → Mysorean Iron-Cased Rocketry | REMOVE | Mysorean iron rockets did not require coke smelting; the edge was Eurocentric and artificial |
| 14 | Mechanical Tools → Rifling | KEEP | reproducible precision manufacture is a material dependency |
| 15 | Veterinary Science → Military Veterinary Services | KEEP | direct professional/scientific dependency |
| 16 | Cadastral Surveying → Hydrographic Surveying | REMOVE | a land-tax cadastre is not required for marine surveying |
| 17 | Rotative Steam Power → Paddle Steamer | KEEP | practical rotary power is a material propulsion dependency |
| 18 | High-Pressure Steam → Paddle Steamer | REMOVE | early paddle vessels also used low-pressure condensing machinery |
| 19 | Mechanical Tools → Mechanized Naval Dockyards | KEEP | mechanized yard capacity requires machine-tool capability |
| 20 | Rotative Steam Power → Mechanized Naval Dockyards | KEEP | powered yard machinery requires rotary power |
| 21 | Pressed Glass → Modern Lighthouse Optics | KEEP | optical material is a direct material input |
| 22 | Puddling & Rolling → Iron Hull Construction | KEEP | structural wrought iron is a direct material dependency |
| 23 | Mechanical Tools → Iron Hull Construction | KEEP | fabrication and repeatable machining are direct industrial dependencies |
| 24 | Industrial Ceramics → Optical Telegraph Networks | WEAKEN | ceramics may support components but optical semaphore systems do not require industrial ceramics |
| 25 | Mechanical Tools → Mechanized Printing | KEEP | press manufacture requires machine-tool capability |
| 26 | Rotative Steam Power → Mechanized Printing | KEEP | powered rotary operation is a direct machinery dependency |
| 27 | Continuous Papermaking → Mechanized Printing | KEEP | continuous paper supply is the relevant scaling/feedstock convergence |
| 28 | Industrial Acids → Experimental Laboratories | WEAKEN | chemical reagents help, but a general experimental laboratory is not dependent on industrial acid production |
| 29 | Industrial Acids → Active-Principle Pharmacy | KEEP | chemical isolation and reagent supply form a direct scientific/material dependency |
| 30 | Mechanized Weaving → Labor Movement | WEAKEN | industrial concentration changes adoption pressure but must not hard-lock political organization |

Static validation after correction: `PREREQUISITE_CYCLES = 0`, `BROKEN_GRAPH_REFERENCES = 0`.

## 6. Era VI and post-1836 bridge review

All 19 Era VI technologies were checked against the rule “bridge, do not rebuild later vanilla.”

| Era VI technology | Protected later responsibility | Verdict |
|---|---|---|
| Interchangeable Manufacture | later mass-production/tooling successors | KEEP BRIDGE |
| Railways | later engines, rail systems and `steel_railway_cars` | KEEP BRIDGE |
| Geological Surveying | Coal/Ore/Industrial-Minerals/Petroleum geology families | KEEP BRIDGE |
| Hot Blast Smelting | `bessemer_process` and later steelmaking | KEEP BRIDGE |
| Hydraulic Cements | `reinforced_concrete` | KEEP DISTINCT |
| Hydraulic Turbines | later turbine/power developments | KEEP BRIDGE |
| Pressed Glass | later glass/optical industrial developments | KEEP BRIDGE |
| Fractional Distillation | later chemical/refining developments | KEEP BRIDGE |
| Percussion Cap | `repeaters`; `bolt_action_rifles` | KEEP BRIDGE |
| General Staff | later staff, planning and operational doctrine | KEEP BRIDGE |
| Shell Gun | `breech_loading_artillery` | KEEP BRIDGE |
| Maritime Safety Standards | later maritime/electrical safety systems | KEEP BRIDGE |
| Modern Lighthouse Optics | later electrical lighting | KEEP BRIDGE |
| Iron Hull Construction | `ironclad_tech` | KEEP DISTINCT |
| Professional Civil Policing | later police/surveillance institutions | KEEP BRIDGE |
| Mass-Circulation Press | later mass communication/propaganda | KEEP BRIDGE |
| Liberal Constitutionalism | later liberal/party developments | KEEP BRIDGE |
| Labor Movement | later mass labor and party organization | KEEP BRIDGE |
| Early Socialism & Cooperativism | mature `socialism` and `anarchism` | KEEP DISTINCT |

The specifically requested transition checks also pass:

- Optical Telegraph Networks remains an early optical/semaphore network and points to, but does not replace, `electric_telegraph`.
- Iron Hull Construction remains distinct from armor doctrine and `ironclad_tech`.
- Hydraulic Cements does not unlock or rename Reinforced Concrete early.
- Hot Blast Smelting leaves Bessemer/open-hearth and other later steelmaking in vanilla.
- Railways leaves later rolling stock and electrical railway families in vanilla.
- Percussion Cap does not absorb repeaters or bolt-action weapons.
- Early Socialism & Cooperativism is an antecedent, not a backdated mature socialist/anarchist node.
- Geological Surveying opens later specialization without revealing all resources everywhere.

`POST_1836_BRIDGE_ISSUES = 0`.

## 7. Names and ID preservation

The strong vanilla-name default is retained. No cosmetic rename is proposed.

One real problem was found and corrected: `international_relations` had been treated as a source equivalent for Institutionalized Scientific Exchange even though TECH-1A marked it `NAME_COLLISION_ONLY`. Its vanilla name and ID are now restored on a distinct node. `Early Socialism & Cooperativism`, `National Sovereignty`, `Iron Hull Construction`, `Hydraulic Cements` and `Optical Telegraph Networks` remain justified distinct concepts rather than cosmetic replacements for later vanilla names.

After correction: `UNJUSTIFIED_RENAMES = 0`.

## 8. Salt and spices invariants

No contradiction was found in TECH-1C or TECH-1D.

- `SPICES = REQUIRED`, with regional/ecological production present from setup; no “invention of spices” technology; exact map and values remain deferred; TECH-1D remains `REFERENCE_ONLY`.
- `SALT = REQUIRED` and `SALT_POP_MINIMUM_SHARE = 0`.
- early military supply = salt + cereals;
- advanced processed-food supply = groceries/processed food without direct salt double-counting.

## 9. Validation and scope control

- integrated nodes: 118;
- Era VI nodes: 19;
- retained hard cross-branch edges: 14;
- broken graph references: 0;
- prerequisite cycles: 0;
- orphan technologies: 0 (`international_relations` is a direct-unlock foundational node);
- missing AI context metadata: 0;
- gameplay files changed: 0;
- TECH-3 started: no;
- commit created: no;
- push performed: no.

TECH2H_FREEZE_REVIEW = PASS

DIAGONAL_FRAMING_VERDICT = A_DIRECTLY_UNLOCK_BOTH_VANILLA_SEPPINGS_BRACED_HULL_OBJECTS
SEPPINGS_VANILLA_OBJECT = ship_mod_frigate_armor_medium;ship_mod_ship_of_the_line_armor_medium
COPPER_SHEATHING_SLOT_VERDICT = CHANGE_TO_EXISTING_SHIP_MOD_SLOT_UTILITY_2_PENDING_RUNTIME_TEMPLATE_VALIDATION

VANILLA_SPLITS_REVIEWED = 21
VANILLA_UNLOCKS_UNASSIGNED = 0
VANILLA_UNLOCKS_DUPLICATED = 0

CROSS_BRANCH_EDGES_REVIEWED = 30
CROSS_BRANCH_KEEP = 14
CROSS_BRANCH_CHANGED = 11
CROSS_BRANCH_REMOVED = 5

ERA_VI_TECHS_REVIEWED = 19
POST_1836_BRIDGE_ISSUES = 0

UNJUSTIFIED_RENAMES = 0
PREREQUISITE_CYCLES = 0
ORPHAN_TECHS = 0
BROKEN_GRAPH_REFERENCES = 0

GAMEPLAY_FILES_CHANGED = 0

TREE_READY_TO_FREEZE = YES
