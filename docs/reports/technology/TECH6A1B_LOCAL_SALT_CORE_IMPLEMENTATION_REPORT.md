# TECH6A-1B — Local Salt Core Implementation Report

Date: 2026-08-26  
Branch: `tech4c2-audit-snapshot`  
Victoria 3 reference: 1.13.9 (`C:\Games\Victoria 3\game`)  
Reference mod: La Gabelle 1.0.2 (local Workshop copy)  
Asset redistribution permission: **GRANTED** by Tokugawa_Mori on 2026-08-28.

## 1. Scope and result

This phase implements the minimal salt economic core: one good, two producer buildings, five PMGs, seven new producer PMs, ten productive consumers, luxury-only POP demand, the required salt modifier types, minimal English/French localization, and three test-only local DDS files.

No salt resource geography, discovery system, initial buildings, companies, Journal Entries, events, tax system, prestige-good system, or mobilization consumption was implemented.

## 2. Gameplay files

Created:

- `common/goods/10_tech6a1b_salt.txt`
- `common/modifier_type_definitions/10_tech6a1b_salt_modifier_types.txt`
- `common/buildings/10_tech6a1b_salt_buildings.txt`
- `common/production_method_groups/10_tech6a1b_salt_pmgs.txt`
- `common/production_methods/10_tech6a1b_salt_producers.txt`
- `common/pop_needs/00_pop_needs.txt` — full same-relative-path vanilla 1.13.9 shadow, changed only by the salt luxury-food entry

Modified:

- `common/production_methods/01_industry.txt` — the ten existing PM objects received only their audited salt inputs; existing 1776 technology changes were preserved

`GAMEPLAY_FILES_CHANGED = 7` (six created gameplay files and one modified gameplay file).

Localization created:

- `localization/english/tech6a1b_salt_l_english.yml`
- `localization/french/tech6a1b_salt_l_french.yml`

Local repository metadata modified:

- `.git/info/exclude` — contenait initialement les exclusions temporaires des assets, retirées dans TECH6A-3F après l’autorisation explicite de Tokugawa_Mori ; le `.gitignore` partagé n’a pas été modifié

All new Clausewitz text and localization files use UTF-8 with BOM, as required by the 1.13.9 parser.

## 3. IDs created

Good:

- `salt`

Buildings:

- `building_salt_mine`
- `building_salt_pan`

Production method groups:

- `pmg_mining_equipment_building_salt_mine`
- `pmg_explosives_building_salt_mine`
- `pmg_steam_automation_building_salt_mine`
- `pmg_train_automation_building_salt_mine`
- `pmg_base_building_salt_pan`

Producer production methods:

- `pm_picks_and_shovels_building_salt_mine`
- `pm_atmospheric_engine_pump_building_salt_mine`
- `pm_condensing_engine_pump_building_salt_mine`
- `pm_diesel_pump_building_salt_mine`
- `pm_nitroglycerin_building_salt_mine`
- `pm_dynamite_building_salt_mine`
- `default_building_salt_pan`

Modifier types required by the new good:

- `goods_input_salt_add`
- `goods_output_salt_add`
- `goods_input_salt_mult`
- `goods_output_salt_mult`

## 4. Salt good and producers

The `salt` definition matches the audited La Gabelle values:

- texture: `gfx/interface/icons/goods_icons/salt.dds`
- cost: `30`
- category: `staple`
- prestige factor: `5`
- traded quantity: `10`
- consumption-tax cost: `200`
- convoy-cost multiplier: `0.5`

Building architecture:

- `building_salt_mine`: `bg_mining`, mine city type, mining terrain manipulator, medium construction, self ownership, unlocked by `shaft_mining`, with four salt-mine PMGs.
- `building_salt_pan`: `bg_mining`, port city type, coastal potential (`is_sea_adjacent = yes`), medium construction, self ownership, and the saline base PMG. It has no construction technology gate.

Producer chain:

| PM | Technology | Inputs | Salt output |
|---|---|---|---:|
| `pm_picks_and_shovels_building_salt_mine` | none | tools 2 | 20 |
| `pm_atmospheric_engine_pump_building_salt_mine` | `atmospheric_engine` | tools 5, coal 10 | 35 |
| `pm_condensing_engine_pump_building_salt_mine` | `watertube_boiler` | tools 10, coal 15 | 45 |
| `pm_diesel_pump_building_salt_mine` | `compression_ignition` | tools 10, oil 5 | 55 |
| `pm_nitroglycerin_building_salt_mine` | `nitroglycerin` | explosives 5 | 15 |
| `pm_dynamite_building_salt_mine` | `dynamite` | explosives 10 | 20 |
| `default_building_salt_pan` | none | none | 10 |

Employment, pollution, and mortality modifiers match the audited La Gabelle objects. The following existing 1776/vanilla PMs are referenced and not redefined: `pm_no_explosives`, `pm_no_steam_automation`, `pm_steam_donkey_mine`, `pm_road_carts`, and `pm_rail_transport_mine`. The existing gates on the latter two automation PMs resolve to `steam_donkey` and `railways`.

## 5. Existing productive consumers modified

The ten existing objects remain uniquely defined in the existing same-relative-path shadow `common/production_methods/01_industry.txt`:

| Existing PM | Salt input |
|---|---:|
| `pm_sweeteners` | 10 |
| `pm_artificial_fertilizers` | 5 |
| `pm_cannery` | 10 |
| `pm_cannery_fish` | 10 |
| `pm_baking_powder` | 30 |
| `pm_vacuum_canning` | 15 |
| `pm_vacuum_canning_principle_3` | 15 |
| `pm_dye_production` | 10 |
| `pm_improved_fertilizer` | 10 |
| `pm_nitrogen_fixation` | 20 |

The early productive sink is `pm_sweeteners`. Its pre-existing 1776 `sugar_refining` gate was preserved.

## 6. POP demand

Final 1776 role:

```text
SALT_POP_ROLE = LUXURY_ONLY
BASIC_FOOD_INTEGRATION = NO
weight = 0.5
min_supply_share = 0.0
max_supply_share = 0.15
```

No buy package was changed. A direct diff against vanilla 1.13.9 shows that the full `00_pop_needs.txt` shadow differs only by this one salt entry in `popneed_luxury_food`.

## 7. Temporary local assets

Copied only for personal local testing:

| Local asset | SHA-256 | Bytes |
|---|---|---:|
| `gfx/interface/icons/goods_icons/salt.dds` | `B124F77814F443B40F23467EC3D66B51007BE2AAE4ECB5E1E0660DC00779AD21` | 87,556 |
| `gfx/interface/icons/building_icons/building_salt_mine.dds` | `9320B1C3B7DAD0F985D4C91851C447C9A16DA2DBD1830C36242E8414AF238CC5` | 87,556 |
| `gfx/interface/icons/building_icons/building_salt_pan.dds` | `A26FC319D035B77EAE39A146E2AFD9A5195F3391E19739E4DAD15415AFE18219` | 87,556 |

Each destination hash equals its La Gabelle source hash. The source files were read/copy sources only and were not modified.

Git verification — statut actuel après TECH6A-3F :

```text
SALT_LOCAL_ASSETS_GIT_IGNORED = NO
SALT_LOCAL_ASSETS_GIT_TRACKED = NO
SALT_LOCAL_ASSETS_GIT_STAGED = NO
SALT_LOCAL_ASSETS_GIT_TRACKABLE = YES
LA_GABELLE_PERMISSION = GRANTED
ALL_STAGED_FILES = 0
```

No commit, push, release, archive, or Workshop publication was performed.

## 8. Static tests

| Test | Result |
|---|---|
| A. New IDs unique in 1776 and absent from vanilla | PASS |
| B. Ten existing vanilla PMs each defined once in the mod | PASS |
| C. All technology references resolve | PASS |
| D. All building PMG references resolve | PASS |
| E. All PMs referenced by the new PMGs resolve | PASS |
| F. `salt` good is defined | PASS |
| G. No salt in `popneed_basic_food` | PASS |
| H. Luxury-food salt entry has weight 0.5, minimum 0, maximum 0.15 | PASS |
| I. Three local DDS files exist and match source hashes | PASS |
| J. Three DDS files are visible to Git, trackable, and not staged | PASS |
| K. No `map_data/state_regions` status or diff | PASS |
| L. No salt resource geography or discovery data imported | PASS |

Additional checks passed: exact consumer quantities, balanced braces in all affected gameplay files, UTF-8 BOM on all new parser-sensitive files, no staged files, no duplicate new definitions, and semantic equality with the audited La Gabelle good/building/PMG/producer objects (apart from comments/formatting and the explicit 1776 POP-demand decision).

## 9. Runtime test

The user performed an interactive corrected launch with the 1776 fork mounted and La Gabelle absent. The first launch had exposed five non-fatal UTF-8 BOM warnings on new salt files; all five were corrected before the final launch.

| Runtime test | Result | Evidence |
|---|---|---|
| T6A1B-01 — menu reached without fatal error | PASS | user-confirmed interactive launch; process remained responsive |
| T6A1B-02 — new game starts | PASS | user launched France; fresh `game.log` initialized |
| T6A1B-03 — `salt` recognized | PASS | market panel displays localized `Sel`, base price 30, and its local icon |
| T6A1B-04 — local icons render | PASS | user visual confirmation and screenshot for the salt good/building interface |
| T6A1B-05 — both buildings parse | PASS | mine visible in the building UI; both definitions have no parser error |
| T6A1B-06 — no `unknown good salt` | PASS | zero targeted matches in fresh `error.log`, `game.log`, and `debug.log` |
| T6A1B-07 — no unknown PM/PMG/technology | PASS | zero targeted matches in all three fresh logs |
| T6A1B-08 — productive consumer PMs load | PASS | no error for `01_industry.txt` or salt inputs |
| T6A1B-09 — luxury pop need loads | PASS | no error for `00_pop_needs.txt` or `salt` |
| T6A1B-10 — no basic-food salt demand | PASS | static scoped-block verification plus successful runtime load |

The visual test shows the base mine PM producing `+20.0` salt per level and consuming `+2.00` tools, with the expected employment. No salt resource deposit exists yet, so the salt mine remains locked/unavailable by location; this is expected and confirms that resource geography was not imported prematurely.

Final fresh-log counters:

```text
error.log TECH6A1B_TARGETED_MATCHES = 0
game.log TECH6A1B_TARGETED_MATCHES = 0
debug.log TECH6A1B_TARGETED_MATCHES = 0
TECH6A1B_BOM_WARNINGS = 0
GAME_RUNTIME_TEST = PASS
```

The runtime logs still contain pre-existing errors elsewhere in the total-conversion repository (notably legacy localization duplication, events, history, and Journal Entries). None references a TECH6A1B file or salt ID, and none was introduced or addressed by this scoped phase.

## 10. Remaining and deferred work

Deferred to TECH6A-2:

- KNOWN_1776 / HIDDEN_DISCOVERABLE classification
- salt-mine discoverable building group
- state-region resource blocks and potentials
- discovered/undiscovered amounts
- discovery events and initial buildings

Deferred to TECH6C:

- salt inputs for `mobilization_option_extra_supplies`
- salt inputs for `mobilization_option_luxurious_supplies`

Explicitly outside this phase: La Gabelle companies, Journal Entries, global/on-action code, events, gabelle/tax mechanics, prestige good, political setup, and historical owner buildings.

## 11. Mandatory summary

```text
TECH6A1B_LOCAL_SALT_CORE = PASS

SALT_GOOD_IMPLEMENTED = YES

SALT_MINE_IMPLEMENTED = YES
SALT_PAN_IMPLEMENTED = YES

NEW_SALT_PMG_IMPLEMENTED = 5
NEW_SALT_PM_IMPLEMENTED = 7

PRODUCTIVE_SALT_CONSUMERS_IMPLEMENTED = 10

EARLY_PRODUCTIVE_SINK_ACTIVE = pm_sweeteners

SALT_BASIC_FOOD_INTEGRATION = NO

SALT_LUXURY_FOOD_INTEGRATION = YES

SALT_LUXURY_MIN_SUPPLY_SHARE = 0

SALT_LOCAL_ASSETS_COPIED = YES
SALT_LOCAL_ASSETS_GIT_TRACKED = NO
SALT_LOCAL_ASSETS_GIT_STAGED = NO
SALT_LOCAL_ASSETS_GIT_IGNORED = NO
SALT_LOCAL_ASSETS_GIT_TRACKABLE = YES
LA_GABELLE_PERMISSION = GRANTED
PERMISSION_DATE = 2026-08-28
ORIGINAL_AUTHOR = Tokugawa_Mori

RESOURCE_MAP_CHANGED = NO
DISCOVERY_IMPLEMENTED = NO

MOBILIZATION_SALT = DEFERRED_TO_TECH6C

GAME_RUNTIME_TEST = PASS

GAMEPLAY_FILES_CHANGED = 7

REPORT_CREATED = YES

COMMITS_CREATED = 0
PUSH_PERFORMED = NO

READY_FOR_TECH6A2 = YES
```
