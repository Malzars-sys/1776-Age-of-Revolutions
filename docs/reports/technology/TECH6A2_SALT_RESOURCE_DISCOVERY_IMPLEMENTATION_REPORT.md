# TECH6A-2 — Salt Resource Map, Native Discovery and Technology Requirements

Date: 2026-08-27  
Branch: `tech4c2-audit-snapshot`  
Victoria 3 reference: 1.13.9 (`C:\Games\Victoria 3\game`)  
La Gabelle reference: 1.0.2 (`3715913236`)  
Status: **PASS (implementation and static validation)**  
Runtime status: **NOT RUN BY CODEX**

## 1. Authoritative scope and overrides

The replacement section 3 supplied by the user is authoritative over conflicting text remaining in the original brief.

Consequently:

- country starting technologies were not audited;
- country starting technologies were not modified;
- `TECH6A2_SALT_STARTING_TECH_AUDIT.csv` was intentionally not created;
- the mine requirement remains `shaft_mining`, but the question of which countries possess it on `1776-01-01` is deferred to the later global setup phase;
- the discovery architecture is native only.

The user's later explicit request to import the La Gabelle salt companies overrides the former exclusion of companies in section 25. Only the companies and their direct functional dependencies were added; no Gabelle tax mechanics, salt protest events, military salt, naval salt, or custom resource-discovery system was imported.

```text
COUNTRY_STARTING_TECH_AUDIT = DEFERRED
COUNTRY_STARTING_TECH_GRANTS = DEFERRED
STARTING_TECH_GRANTS_ADDED = 0
STARTING_TECH_CONFLICTS = DEFERRED_NOT_COUNTED
```

## 2. Frozen TECH6A-1B baseline

The five required TECH6A-1/1B reports were read before implementation. The salt core was preserved:

- `cost = 30`
- `category = staple`
- `prestige_factor = 5`
- `traded_quantity = 10`
- `consumption_tax_cost = 200`
- `convoy_cost_multiplier = 0.5`
- basic-food role: absent
- luxury-food weight: `0.5`
- luxury-food minimum supply share: `0.0`
- luxury-food maximum supply share: `0.15`
- productive consumer modifiers: 10 occurrences

No TECH6A-1B economic value was changed by TECH6A-2. The only change to the salt-building definition was the mine's building group.

## 3. Native resource architecture

### 3.1 Salt pans

All 97 `building_salt_pan` relations are represented as visible capped resources inside `capped_resources`.

```text
VISIBLE = LA_GABELLE_TOTAL
HIDDEN = 0
```

No salt pan has an `undiscovered_amount`.

### 3.2 Rock-salt mines

All 64 `building_salt_mine` relations use the native 1.13.9 structure:

```text
resource = {
    type = "building_salt_mine"
    discovered_amount = KNOWN_1776
    undiscovered_amount = HIDDEN_DISCOVERABLE
}
```

For every relation:

```text
KNOWN_1776 + HIDDEN_DISCOVERABLE = LA_GABELLE_TOTAL
```

No `change_resource_potential`, hidden variable, custom discovery event, forced discovery, parallel counter, or monthly discovery scan was added.

### 3.3 Totals

| Measure | Result | Target |
|---|---:|---:|
| Salt-pan relations | 97 | 97 |
| Salt-mine relations | 64 | 64 |
| Total relations | 161 | 161 |
| Distinct State Regions | 159 | 159 |
| Salt-pan potential | 2526 | 2526 |
| Salt-mine potential | 1209 | 1209 |
| Total salt potential | 3735 | 3735 |
| Known rock salt | 849 | — |
| Hidden rock salt | 360 | — |

`STATE_CATALONIA` and `STATE_UPPER_ANDALUSIA` retain both salt resource types. No new salt-bearing State Region was introduced.

## 4. Historical 1776 classification

The detailed row-level decisions, sources, confidence and exact amounts are in `TECH6A2_SALT_1776_RESOURCE_CLASSIFICATION.csv`.

The V1 split is deliberately binary. A deposit reliably known by 1776 is fully discovered; a deposit not reliably known or exploited by then is fully hidden. No arbitrary 20/50/75-percent splits were invented.

| Classification | Relations |
|---|---:|
| `KNOWN_AND_EXPLOITED_BY_1776` | 27 |
| `KNOWN_BY_1776_BUT_NOT_SIGNIFICANTLY_EXPLOITED` | 19 |
| `NOT_RELIABLY_KNOWN_OR_EXPLOITED_BY_1776` | 18 |
| `UNRESOLVED` | 0 |

Institutional and academic anchors include:

- Ontario Geological Survey: Goderich's first solid salt bed was discovered in 1866 — <https://www.geologyontario.mndm.gov.on.ca/mndmfiles/mdi/data/records/MDI40P12NE00005.html>
- USGS: Onondaga salt springs and the Syracuse salt industry — <https://pubs.usgs.gov/fs/2000/0139/report.pdf>
- British Geological Survey: Cheshire salt history and the 1670 rock-salt discovery — <https://webapps.bgs.ac.uk/Memoirs/docs/B01555.html>
- UNESCO: Wieliczka and Bochnia mines operating since the thirteenth century — <https://whc.unesco.org/en/list/32/>
- UNESCO: Hallstatt salt exploitation extending back to the second millennium BCE — <https://whc.unesco.org/en/list/806>
- UNESCO: Salins-les-Bains and its long salt-production history — <https://whc.unesco.org/en/list/203/>
- Cambridge University Press: ancient Sichuan salt production — <https://www.cambridge.org/core/books/abs/salt-production-and-social-hierarchy-in-ancient-china/ancient-salt-production-in-sichuan/D0ED3D6489F398FFC9FC81AF553F1C1E>
- UNESCO: Khewra and the Salt Range — <https://whc.unesco.org/en/tentativelists/6118/>
- Smithsonian National Museum of the American Indian: Inka salt landscapes in Collasuyu — <https://americanindian.si.edu/inkaroad/inkauniverse/suyus/collasuyu.html>
- UNESCO: Timbuktu and the trans-Saharan salt trade — <https://whc.unesco.org/en/list/119>

Most mine rows are marked `MEDIUM` confidence because a Victoria 3 State Region is broader than a historical mine or basin. Conservative decisions are documented in the CSV rather than presented as false precision.

## 5. Building group and technology gates

`bg_mining` was not overridden or made discoverable. A dedicated child group was added:

```text
bg_salt_mining = {
    parent_group = bg_mining
    discoverable_resource = yes
    depletable_resource = no
    default_building = building_salt_mine
}
```

Inheritance preserves the mining lens, slave eligibility, urbanization, infrastructure, automatic expansion, economy-of-scale AI and foreign-investment AI semantics.

The mine now uses `bg_salt_mining` and still requires `shaft_mining`.

The salt pan retains no technology gate. The audited 1776 production tree contains no defensible prerequisite for an ancient surface/coastal industry without imposing an anachronistic delay.

```text
SALT_MINE_TECH_GATE = shaft_mining
SALT_PAN_TECH_GATE = NONE
SALT_PAN_GATE_REASON = ANCIENT_BASELINE_TECHNOLOGY
```

No `BASELINE_*` identifier is used as a gameplay prerequisite.

## 6. State-region shadowing

The following complete same-relative-path shadows were created or merged:

- `00_west_europe.txt`
- `01_south_europe.txt`
- `02_east_europe.txt`
- `03_north_africa.txt`
- `04_subsaharan_africa.txt`
- `05_north_america.txt`
- `06_central_america.txt`
- `07_south_america.txt`
- `08_middle_east.txt`
- `09_central_asia.txt`
- `10_india.txt`
- `11_east_asia.txt`
- `12_indonesia.txt`
- `13_australasia.txt`
- `15_russia.txt`

For the 13 previously absent shadows, the source is vanilla 1.13.9. For `08_middle_east.txt` and `13_australasia.txt`, the source is the pre-existing 1776 version. A reverse comparison removed only the new salt entries and confirmed all 15 results are otherwise byte-content equivalent after line-ending normalization and terminal-newline normalization.

## 7. Starting salt production in 1776

La Gabelle's 1836 setup contained 63 starting-building relations, 167 total levels and two `STATE_URALSK` mine entries. It was not copied.

A restrained 1776 bootstrap was created in `common/history/buildings/99_tech6a2_salt_starting_buildings.txt`:

| State Region | Owner | Building | Level |
|---|---|---|---:|
| `STATE_JALISCO` | `SC1` | salt pan | 1 |
| `STATE_RIO_GRANDE_DO_NORTE` | `BRZ` | salt pan | 1 |
| `STATE_LIMA` | `SC3` | salt pan | 1 |
| `STATE_BRITTANY` | `FRA` | salt pan | 1 |
| `STATE_LANGUEDOC` | `FRA` | salt pan | 1 |
| `STATE_LOWER_EGYPT` | `TUR` | salt pan | 1 |
| `STATE_FUJIAN` | `CHI` | salt pan | 1 |
| `STATE_BEIJING` | `CHI` | salt pan | 3 |
| `STATE_CHUGOKU` | `JAP` | salt pan | 1 |
| `STATE_LA_PAMPA` | `SC4` | salt mine | 1 |
| `STATE_LANCASHIRE` | `GBR` | salt mine | 2 |
| `STATE_WEST_GALICIA` | `GAL` | salt mine | 2 |
| `STATE_SICHUAN` | `CHI` | salt mine | 2 |
| `STATE_ANKARA` | `TUR` | salt mine | 1 |
| `STATE_PUNJAB` | `PAN` | salt mine | 1 |
| `STATE_SHANXI` | `CHI` | salt mine | 2 |
| `STATE_POTOSI` | `SC3` | salt mine | 1 |
| `STATE_FRANCHE_COMTE` | `FRA` | salt mine | 1 |
| `STATE_BAVARIA` | `BAV` | salt mine | 1 |
| `STATE_TYROL` | `AUS` | salt mine | 1 |
| `STATE_LESSER_POLAND` | `PLC` | salt mine | 2 |
| `STATE_QINGHAI` | `CHI` | salt mine | 1 |

Totals:

- starting salt-pan relations: 9; levels: 11;
- starting salt-mine relations: 13; levels: 18;
- starting buildings above known potential: 0;
- `STATE_URALSK` starting entries: 0.

The owners were verified against the actual 1776 state-history setup. `STATE_PUNJAB` is split between `PAN` and `DUR`; the salt building is intentionally placed in `region_state:PAN`.

Technology ownership was not evaluated. This is a deliberate scope boundary, not a claim that all 13 mine owners already possess `shaft_mining`.

## 8. La Gabelle salt companies

Six definitions were imported:

| Company ID | Type |
|---|---|
| `company_basic_salt` | generic, dynamic naming |
| `company_salt_union` | flavored |
| `company_groupe_salins` | flavored |
| `company_morton_salt` | flavored |
| `company_kali_und_salz_ag` | flavored |
| `company_maldon_sea_salt` | flavored |

Direct dependencies also imported:

- `prestige_good_generic_salt`;
- `je_prestige_goods_salt`;
- `prestige_goods_salt_unlocked` notification;
- English and French company/prestige localization;
- six company DDS icons and one prestige-good DDS icon.

The erroneous French La Gabelle references to prestige **fish** were corrected to prestige **salt**. The journal entry's `on_monthly_pulse` tracks company prosperity for the prestige-good feature; it does not discover resources and does not alter `discovered_amount` or `undiscovered_amount`.

No general Gabelle journal entry, tax system, event set, or modifier set was imported.

All seven additional DDS files are exact local copies of the La Gabelle assets. Redistribution permission was granted by Tokugawa_Mori on 2026-08-28; the former local Git exclusions were removed during TECH6A-3F so these files may now be tracked and distributed with attribution.

## 9. Static validation

| Test | Result | Evidence |
|---|---|---|
| T6A2-S01 | PASS | 97 salt-pan relations |
| T6A2-S02 | PASS | 64 salt-mine relations |
| T6A2-S03 | PASS | 161 total relations |
| T6A2-S04 | PASS | 159 distinct State Regions |
| T6A2-S05 | PASS | salt-pan potential = 2526 |
| T6A2-S06 | PASS | mine discovered + undiscovered = 1209 |
| T6A2-S07 | PASS | 64/64 per-row invariants match CSV |
| T6A2-S08 | PASS | no pan `undiscovered_amount` |
| T6A2-S09 | PASS | zero extra salt-bearing State Regions |
| T6A2-S10 | PASS | `bg_mining` unchanged and not discoverable |
| T6A2-S11 | PASS | valid `bg_salt_mining` definition present |
| T6A2-S12 | PASS | salt mine uses `bg_salt_mining` |
| T6A2-S13 | PASS | salt mine retains `shaft_mining` |
| T6A2-S14 | PASS | pan gate documented as `NONE` |
| T6A2-S15 | PASS | no `BASELINE_*` prerequisite |
| T6A2-S16 | PASS | one resource relation per state/type |
| T6A2-S17 | PASS | no starting `STATE_URALSK` duplicate |
| T6A2-S18 | PASS | all La Gabelle DDS visible to Git, trackable, and unstaged after permission grant |
| T6A2-S19 | PASS | HEAD remains `907940e5ec94399afd14ddb5fa5ab82c3b7dbf61`; no commit created |
| T6A2-S20 | PASS | no push performed |

Additional static checks:

- 28 changed/new script `.txt` files checked; brace errors: 0;
- 4 localization files checked; UTF-8 BOM/header errors: 0;
- `git diff --check`: no whitespace errors;
- map-vs-CSV mismatches: 0;
- map reverse-shadow mismatches: 0/15;
- 22 starting-building blocks; duplicates: 0;
- company definitions: 6/6;
- company/prestige DDS assets present and source-hash identical: 7/7;
- prestige-good, journal and notification definitions present: 3/3;
- company referenced strategic regions and modifiers found in vanilla 1.13.9;
- country starting-technology files modified: 0;
- custom salt discovery scripts/events/scans: 0.

## 10. Runtime checklist for the user

Codex did not launch Victoria 3 or the Paradox launcher. The user should perform these checks on a **new game**:

1. Confirm the game reaches the main menu and starts a new 1776 campaign without a TECH6A-2 error.
2. Confirm at least one historical salt pan is visible and constructible in a state with salt-pan potential.
3. Confirm a salt mine with `discovered_amount > 0` is visible.
4. Confirm a state with `discovered_amount = 0` and only `undiscovered_amount > 0` does not expose its full mine potential immediately.
5. Confirm `building_salt_mine` requires `shaft_mining`.
6. Confirm `building_salt_pan` has no technology requirement.
7. Confirm the listed starting salt pans and mines appear under their intended 1776 owners; record any mine disabled by missing technology for the deferred global technology-setup phase.
8. Let the simulation run until a native rock-salt discovery occurs, or use a non-destructive test method.
9. Confirm discovery increases visible mine potential without exceeding the CSV total.
10. Save the game.
11. Reload the save.
12. Confirm discovered potential was not duplicated.
13. Confirm the remaining `undiscovered_amount` did not reset to its initial value.
14. Confirm no salt resource exceeds its La Gabelle total.
15. Open the company list and confirm the generic salt company and five flavored salt companies appear when their normal conditions are met.
16. Confirm all company and prestige-salt icons render correctly.
17. If the relevant DLC feature is enabled, confirm the fine-salt prestige journal can appear and its French text refers to salt, not fish.
18. Inspect logs for: `unknown building`, `unknown building group`, `unknown good`, `unknown technology`, `unknown company`, `unknown prestige good`, `resource`, `discoverable_resource`, `building_salt_mine`, `building_salt_pan`, `bg_salt_mining` and `prestige_good_generic_salt`.
19. Report any attributable error together with the complete log line and the state/company involved.

```text
RUNTIME_TEST_REQUIRED_BY_USER = YES
RUNTIME_TEST_PERFORMED_BY_CODEX = NO
RUNTIME_STATUS = NOT_RUN_BY_CODEX
```

## 11. Final result

```text
TECH6A2_SALT_RESOURCE_DISCOVERY = PASS

SALT_PAN_RELATIONS = 97/97
SALT_MINE_RELATIONS = 64/64

SALT_PAN_TOTAL_POTENTIAL = 2526/2526
SALT_MINE_TOTAL_POTENTIAL = 1209/1209
SALT_TOTAL_POTENTIAL = 3735/3735

NEW_SALT_REGIONS_ADDED = 0

SALT_MINE_BUILDING_GROUP = bg_salt_mining
SALT_MINE_DISCOVERABLE = YES
SALT_MINE_TECH_GATE = shaft_mining
SALT_PAN_TECH_GATE = NONE

KNOWN_ROCK_SALT_TOTAL = 849
HIDDEN_ROCK_SALT_TOTAL = 360

NATIVE_DISCOVERY_ONLY = YES
CUSTOM_DISCOVERY_SCRIPT_CREATED = NO
CUSTOM_DISCOVERY_EVENT_CREATED = NO
CUSTOM_MONTHLY_SCAN_CREATED = NO

STARTING_SALT_PANS_CREATED = 9
STARTING_SALT_PAN_LEVELS = 11
STARTING_SALT_MINES_CREATED = 13
STARTING_SALT_MINE_LEVELS = 18

COUNTRY_STARTING_TECH_AUDIT = DEFERRED
COUNTRY_STARTING_TECH_GRANTS = DEFERRED
STARTING_TECH_GRANTS_ADDED = 0
STARTING_TECH_CONFLICTS = DEFERRED_NOT_COUNTED

LA_GABELLE_SALT_COMPANIES_IMPORTED = 6/6
LA_GABELLE_COMPANY_DIRECT_DEPENDENCIES_IMPORTED = YES

STATIC_TESTS = PASS

RUNTIME_TEST_REQUIRED_BY_USER = YES
RUNTIME_TEST_PERFORMED_BY_CODEX = NO
RUNTIME_STATUS = NOT_RUN_BY_CODEX

SALT_LOCAL_ASSETS_GIT_TRACKED = NO
SALT_LOCAL_ASSETS_GIT_STAGED = NO
SALT_LOCAL_ASSETS_GIT_IGNORED = NO
SALT_LOCAL_ASSETS_GIT_TRACKABLE = YES
LA_GABELLE_PERMISSION = GRANTED
PERMISSION_DATE = 2026-08-28
ORIGINAL_AUTHOR = Tokugawa_Mori

COMMITS_CREATED = 0
PUSH_PERFORMED = NO

READY_FOR_USER_RUNTIME_TEST = YES
```
