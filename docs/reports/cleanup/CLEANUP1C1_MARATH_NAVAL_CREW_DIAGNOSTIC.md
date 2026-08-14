# CLEANUP-1C.1 — Maratha Naval Crew Diagnostic

```text
STATUS = HISTORICAL_DIAGNOSTIC_SUPPLEMENT
```

This supplement follows the CLEANUP-1C runtime failure and predates the canonical correction. [CLEANUP-1D](CLEANUP1D_MARATH_NAVAL_ADMIN_CORRECTION.md) and [CLEANUP-1E](CLEANUP1E_MARATH_FINAL_ACCEPTANCE.md) are authoritative for the final repository correction and runtime acceptance.

## 1. CLEANUP-1C failure reproduced from evidence

CLEANUP-1C.1 did not launch Victoria 3, Steam, the Paradox Launcher, `dowser.exe`, or any other runtime. The CLEANUP-1C screenshots and recorded observations are treated as the runtime evidence.

The formation side of CLEANUP-1B passed: MARATH loaded, `Konkan Flotilla` existed once at South India HQ with two frigates, and Anandrao Dhulap was its correctly configured admiral. The crew side failed: the fleet showed `0 / 1.00K` crew after 49 days and its Buildings/Crew table stayed empty.

The key correction to the CLEANUP-1C interpretation is that the inspected building was **Naval Logistics Center**, not **Naval Administration**. Its exact workforce — 10 officers, 30 bureaucrats, and 60 laborers — uniquely matches `pm_basic_naval_logistics_center`. Its supplied-fleet list is a logistics/supply association. It does not establish the presence of `building_naval_administration`, activation of `pm_simple_sailor_recruitment`, or 1,000 available sailors.

The fleet's `0 / 1.00K` display is the crew currently aboard versus crew required by its ships: two `ship_type_frigate` objects at 500 crew each. It was not proof that the logistics center supplied a 1,000-sailor country pool.

## 2. Vanilla 1.13 naval crew architecture

The local read-only Victoria 3 1.13 / The Great Wave tree at `C:\Games\Victoria 3 The Great Wave\game` establishes this chain:

1. `building_naval_administration` is the naval recruitment building. In `common/buildings/05_military.txt` it has `recruits_sailors = yes`, belongs to `bg_naval_administration`, is marked `naval = yes`, uses `pmg_base_building_naval_administration`, and is unlocked by `admiralty`.
2. `pmg_base_building_naval_administration` contains only `pm_simple_sailor_recruitment`.
3. At each building level, that PM creates employment for 900 soldiers and 100 officers. Its workforce-scaled country modifier is `country_sailors_max_add = 1000`. Sailors are therefore not a separate employee profession in the building UI; they are soldiers/officers recruited through the naval administration and assigned as ship crew.
4. `common/defines/00_defines.txt` hard-codes `NAVAL_ADMINISTRATION_BUILDING = "building_naval_administration"`, `SAILORS_PER_ASSIGNMENT_SLOT = 100`, and `SAILORS_PER_BUILDING_LEVEL = 1000`.
5. `ship_type_frigate` has `ship_crew_max_add = 500`. A two-frigate fleet therefore requires 1,000 crew. From the 100-sailor slot define, each frigate consumes five assignment slots and the pair consumes ten; this slot count is a direct arithmetic inference from the definitions.
6. Initial `ship` history blocks contain `type` and `count`; vanilla working fleets do not add `state_region`, `home_base`, `building`, `formation`, `support`, or an assignment ID to a ship. The engine assigns ships to naval-administration slots and records the contributing building/state in the fleet crew breakdown.
7. Vanilla localization confirms that undermanned ships are remedied by building or expanding `building_naval_administration`, that sailors are provided by buildings for crewing ships, and that the crew UI resolves a contributing state to that state's `building_naval_administration`.

The separate `building_naval_logistics_center` is non-buildable, non-expandable, and non-downsizeable. It uses `pm_basic_naval_logistics_center`, whose only effects are 60 laborers, 30 bureaucrats, and 10 officers per level. It has neither `recruits_sailors = yes` nor `country_sailors_max_add`. Its appearance and supplied-fleet list are automatic consequences of the fleet/logistics architecture, not a crew link.

Recruitment speed is a building mechanic. The generic building defines provide positive default weekly hiring bounds; naval-model laws may add a hiring-rate bonus, but `law_merchant_navy` has no zeroing or blocking modifier. No scripted sailor-recruitment effect or explicit formation-to-building command exists in the audited initial OOB architecture.

## 3. Working vanilla comparisons

| COUNTRY | FLEET | HQ | SHIP_COUNT | NAVAL_ADMIN_STATE | NAVAL_ADMIN_LEVEL | CREW/SUPPORT_LINK_METHOD | ACTUAL SCRIPT DIFFERENCES VS MARATH |
|---|---|---|---:|---|---:|---|---|
| GBR | 10 fleets, including Portsmouth, Plymouth, Sheerness, and Chatham Stations | Multiple HQs | 196 total | Home Counties, Lancashire, Wales, Yorkshire, Midlands, East Anglia, West Country | 136 total | Implicit engine assignment to `building_naval_administration`; no ship-level building/state field | Tier-1 technology effect includes Admiralty; many ships and seven recruitment states |
| DEN | `Kongelige_Danske_Marine` | Northern Europe | 14 | Jutland | 15 | Same implicit assignment; history building uses `pm_simple_sailor_recruitment` | Tier-2 technology effect includes Admiralty; one recruitment state |
| BIC | `Indian_Navy` | South India | 1 frigate | Bombay | 1 | Same implicit assignment; no explicit ship link | Closest one-level India control; tier-2 technology effect includes Admiralty |
| MARATH (mod) | `Konkan_Flotilla` | South India | 2 frigates | Bombay in history script | 1 requested | Same vanilla-shaped implicit link was expected | Tier-5 technology effect does **not** include Admiralty; runtime exposed only the automatic logistics center and no crew assignment |

The vanilla GBR, DEN, and BIC formation blocks use the same relevant shape as MARATH: country scope, `create_military_formation`, `type = fleet`, an HQ, a name, and one or more `ship` blocks containing a ship type and a count. None supplies an additional link field that MARATH omitted.

The closest scope-only comparison, Travancore, creates a one-frigate South India fleet in a princely-state country scope, but its vanilla OOB has no own naval-administration history block. It is useful for validating MARATH's formation syntax, not as a self-contained crew control, and is therefore not presented as proof of a working one-building recruitment link.

## 4. MARATH structural difference

The MARATH building history block is textually correct relative to vanilla examples: it requests `building_naval_administration`, assigns one country-owned level to `c:MARATH`, sets reserves, and activates `pm_simple_sailor_recruitment`. The formation block is also valid: two frigates at South India HQ need no explicit state or building property.

The decisive difference is country technology initialization:

- MARATH executes `effect_starting_technology_tier_5_tech` plus `international_trade`.
- The vanilla tier-5 effect includes Navigation but not Admiralty.
- Admiralty appears in vanilla starting tiers 1 through 4 and is the declared unlock of `building_naval_administration`.
- All three self-contained working controls above receive Admiralty through their starting tier.
- CLEANUP-1C directly confirmed MARATH did not have Admiralty and that the technology UI identified Naval Administration as its unlock.

Hypotheses were ranked as follows:

| HYPOTHESIS | EVIDENCE_FOR | EVIDENCE_AGAINST | CONFIDENCE |
|---|---|---|---|
| The runtime building was misidentified | Exact 10/30/60 workforce and “Naval Logistics Center” label match only the logistics PM/building | None | HIGH |
| The historical naval administration failed availability/initialization because Admiralty is absent | Building definition declares Admiralty; MARATH tier lacks it; working controls have it; no actual admin appeared in the fleet crew table | Engine-side rejection is not emitted as a targeted script error | HIGH |
| A ship-level `state_region`, base, building, or assignment field is missing | Empty crew table might superficially suggest a missing link | Working vanilla initial ships have none; MARATH formation loaded correctly | REJECTED / HIGH |
| `pm_simple_sailor_recruitment` is the wrong PM | Zero sailors might suggest a PM error | It is the sole vanilla PM in the naval-administration PMG and is used by all starting admins | REJECTED / HIGH |
| The 10/30/60 workforce should recruit sailors | The inspected building was fully employed | Those jobs are the logistics-center PM and it has no sailor modifier | REJECTED / HIGH |
| Population, wages, or navy law alone caused zero hiring | Such factors can affect hiring speed | They cannot explain the total absence of a contributing building/assignment after 49 days; laws only add rate bonuses | LOW |
| `count = 2` or `ship_type_frigate` is invalid | Two objects require a full 1,000 crew | Runtime created both ships; the type is vanilla and each object has 500 maximum crew | REJECTED / HIGH |

## 5. Root cause

```text
ROOT_CAUSE = MARATH has no valid active building_naval_administration instance for ship assignments because the building is Admiralty-unlocked; CLEANUP-1C inspected the separately auto-created building_naval_logistics_center.
ROOT_CAUSE_CONFIDENCE = HIGH
MISSING_OR_WRONG_SCRIPT = No ship-link field is missing. The missing runtime object is the exact hard-coded building_naval_administration recruitment building.
WHY_CAPACITY_WORKED = It was not demonstrated. 0/1.00K was current/required fleet crew (2 x 500), not logistics-center sailor capacity.
WHY_RECRUITMENT_FAILED = pm_simple_sailor_recruitment was not running on an available naval administration; the logistics-center PM cannot recruit sailors.
WHY_BUILDING_CREW_TABLE_WAS_EMPTY = The engine had no building_naval_administration assignment source to list.
ADMIRALTY_CAUSAL = YES for building availability; NO for any hidden sailor modifier.
PROPOSED_MINIMAL_FIX = The direct vanilla fix is Admiralty, but granting it is forbidden. No speculative gameplay workaround is implemented.
```

This diagnosis also corrects two conclusions in CLEANUP-1C: the inherited administration was not proven to survive, and the 1,000 display was not proven to be a country sailor capacity. The evidence instead shows an automatic logistics center alongside an unmet 1,000-crew requirement.

## 6. Admiralty analysis

Admiralty's technology definition has an empty effective modifier block. It grants no `country_sailors_max_add`, no sailor hiring rate, no assignment slots, and no crew-growth modifier. Its documented role is to unlock `building_naval_administration`; Navigation is its prerequisite.

Admiralty is therefore causal only through availability of the recruitment building. Once a valid, staffed naval administration exists with `pm_simple_sailor_recruitment`, sailor capacity and hiring are building/PM mechanics. There is no second hidden Admiralty effect that could explain a valid administration recruiting zero sailors.

Granting Admiralty to MARATH would be the smallest vanilla-supported mechanical correction, but it violates the explicit historical and project constraints and would also broaden MARATH's naval progression. It was not done.

## 7. Diagnostic disposition

No gameplay crew fix was implemented in CLEANUP-1C.1. This is intentional, not an incomplete speculative edit.

The engine define names the exact recruitment type `building_naval_administration`; a country-specific clone would not be the defined naval-administration building. Redirecting that define, changing the logistics center's PM, or removing Admiralty from the building definition would affect the global naval architecture. A delayed on-action that force-creates a locked building is not demonstrated by a vanilla no-Admiralty control and would require runtime experimentation. Modifying technology tiers or adding a technology exception would modify progression. All of those exceed the authorized minimal MARATH-only link repair.

The existing CLEANUP-1B history block remains unchanged for a future design decision. The fleet remains two frigates, South India HQ, and Anandrao Dhulap; the land army is unchanged. No ship of the line, Admiralty, technology-tree edit, global naval rebalance, or late startup effect was added.

At the time of this diagnostic, an encoding-only BOM edit was recorded beside the report. That edit is not the final repository correction and is not present in current HEAD. The canonical final correction is documented by CLEANUP-1D and CLEANUP-1E: the true Naval Administration, one temporary `admiralty` grant, a user-run A/B validation, and final CLEANUP-1 acceptance.

## 8. Historical UTF-8 BOM observation

The convention check found:

- vanilla `common/character_templates`: 210/210 `.txt` files begin with UTF-8 BOM;
- mod `common/character_templates` before correction: 26/27 begin with UTF-8 BOM;
- the sole exception was `common/character_templates/country_marath.txt`.

The diagnostic session recorded a temporary state in which the file began with `EF BB BF`. A SHA-256 hash of all bytes after that BOM was `6CDE4A23E655B61EFC114E9F0BB18F274CD02D6FDBB8FA99F85AE5A60591F7AA`, exactly equal to the complete pre-edit hash.

This is historical evidence, not a description of current HEAD. The current `common/character_templates/country_marath.txt` begins with `23 20 4D`, not `EF BB BF`; no BOM change from this diagnostic survives as the final correction.

## 9. Static validation

The historical static validation passed for the retained CLEANUP-1B structure and the then-observed BOM-only diagnostic edit:

- braces: `10_india.txt` 704/704, `05_military_formations_india.txt` 141/141, `country_marath.txt` 2/2;
- vanilla IDs resolved: `building_naval_administration`, `pm_simple_sailor_recruitment`, `ship_type_frigate`, and `region_south_india`;
- MARATH formation remains one `Konkan_Flotilla`, two frigates, South India HQ;
- Anandrao template and transfer scopes remain present;
- MARATH land formation remains North India HQ;
- no `admiralty` was added to the inspected MARATH files;
- the diagnostic snapshot had UTF-8 BOM prefix `EF BB BF` and an unchanged functional-content hash; current HEAD does not retain that prefix;
- no technology-tree file was edited;
- `git diff --check` passes and the index is empty.

Compared with vanilla BIC, the MARATH fleet and building history retain the same supported formation/building/PM vocabulary. The remaining difference is deliberately unresolved technology availability, not syntax.

## 10. USER-RUN runtime validation plan

Use one manual Victoria 3 launch and one new 1776 MARATH campaign. Do not rely on an old save. The purpose is to confirm the corrected interpretation and capture the exact engine state before choosing a future progression-compatible design exception.

1. Launch the game manually with the mod enabled, start as Maratha Confederacy, and pause immediately on 1 January 1776. Record whether the campaign loads.
2. Open Military, select `Konkan Flotilla`, and capture its Information screen. Record HQ, total ships, Cruiser/frigate count, Capital Ship count, Torpedo Craft count, organization, and the exact crew fraction. Expected formation values: South India, 2, 2, 0, 0, 100%, and `0 / 1.00K` crew.
3. Open Anandrao Dhulap from that panel. Capture name, country, rank/role, assigned fleet, age, culture, religion, and home state. Expected: Commodore/Admiral, Konkan Flotilla, age 40, Marathi, Hindu, Maharashtra/Bombay region.
4. In the fleet panel open the `Buildings` tab (the crew-source table). Capture the entire table even if empty. If any row exists, record the exact building name, state, assigned ships/slots, and crew contribution.
5. Open the Maharashtra/Bombay state Buildings list. Search separately for the exact names `Naval Administration` and `Naval Logistics Center`. Capture the list and then each building panel that exists. Do not treat the two names as interchangeable.
6. For `Naval Logistics Center`, record level, PM name, employees by profession, and supplied fleets. Expected diagnostic values: level 1, 60 laborers, 30 bureaucrats, 10 officers, and Konkan Flotilla listed as supplied.
7. For `Naval Administration`, if present, record level, PM, employees by profession, current/max sailors, construction/expansion button state, and take a screenshot. A fully employed level should show the Simple Recruitment architecture (900 soldiers and 100 officers), not 10/30/60. If absent, explicitly record `NAVAL_ADMINISTRATION_PRESENT = NO`.
8. Open the Military technology tree and select Admiralty. Capture its researched/unresearched state, prerequisite, and Naval Administration unlock. Do not research it. Expected: unresearched, Navigation prerequisite satisfied.
9. Without queuing construction, hover the Naval Administration build/expand control from the state or military lens. Record the exact lock/tooltip. If the administration is absent, record whether construction is unavailable specifically because of Admiralty.
10. Return to Konkan Flotilla and record the crew fraction at the paused start. Then run exactly 28 days and pause on 29 January 1776. Re-record crew, Buildings/Crew table, logistics supplied-fleet association, ship count, organization, and Anandrao assignment.
11. Open the MARATH land formation and capture `Stationed at North India HQ`; record its unit count to detect any regression.
12. Exit normally. Preserve `Documents\Paradox Interactive\Victoria 3\logs\error.log`, `game.log`, and `debug.log` from this session. Search/copy every line containing `MARATH`, `Konkan_Flotilla`, `Konkan Flotilla`, `Anandrao`, `Dhulap`, `building_naval_administration`, `building_naval_logistics_center`, `pm_simple_sailor_recruitment`, `ship_type_frigate`, `region_south_india`, `sailor`, `crew`, `Error`, or `Warning`. Report the attributable count and attach the screenshots/values above.

The decisive branch is simple: if Naval Administration is absent while the Logistics Center is present with 10/30/60 workers, this diagnosis is confirmed. If a true Naval Administration is present, the screenshots of its PM, 900/100 workforce, sailor values, and fleet Buildings table are required before any further fix is designed.

## 11. Protected-state verification

Final read-only Git and filesystem checks found:

- branch `cleanup-post-release` and HEAD `1e374f2f40252d229bc249600e3cbbe26085122d` unchanged;
- no staged files and no Git mutation performed;
- `git diff --check` passes;
- protected `stash@{0}` still resolves to `518df704fa14599c0f254fae13859210663dd976`;
- no new stash was created;
- `bject` is absent;
- BIC retains `activate_law = law_type:law_frontier_colonization` and contains no `law_colonial_exploitation`;
- all seven protected technology-research files remain untracked, unstaged, and byte-identical.

| Protected file | SHA-256 |
|---|---|
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410` |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` |

## 12. Verdict

The historical diagnostic identified the root cause with high confidence: CLEANUP-1C conflated two separate buildings, while MARATH lacked the technology that unlocks the exact engine-defined sailor-recruitment building. There is no missing property in the fleet script and no hidden Admiralty recruitment modifier.

At this diagnostic point, a crew fix could not be implemented within the then-current constraints using a demonstrated vanilla MARATH-only mechanism. The block below records that historical verdict and is superseded for final repository status by CLEANUP-1D and CLEANUP-1E.

```text
NAVAL_CREW_ROOT_CAUSE_IDENTIFIED = YES
NAVAL_CREW_ROOT_CAUSE_CONFIDENCE = HIGH
MARATH_CREW_FIX_IMPLEMENTED = NO
MARATH_ADMIRALTY_GRANTED = NO
TECH_TREE_MODIFIED = NO
COUNTRY_MARATH_UTF8_BOM = PASS
V13_STATIC_VALIDATION = PASS
CODEX_LAUNCHED_VICTORIA3 = NO
USER_RUNTIME_REQUIRED = YES
STASH_INTACT = YES
SAFE_FOR_USER_RUNTIME = YES
SAFE_TO_COMMIT_CLEANUP1B = NO
```

## 13. Canonical later resolution

CLEANUP-1D and CLEANUP-1E subsequently established and validated the final solution: MARATH's history already requested the correct Naval Administration and PM; one temporary `add_technology_researched = admiralty` made the true building materialize; the user's A/B runtime reached `1,000 / 1,000` crew; and CLEANUP-1 closed with `RUNTIME = PASS`.

```text
FINAL_CORRECTION_AUTHORITY = CLEANUP1D_MARATH_NAVAL_ADMIN_CORRECTION.md + CLEANUP1E_MARATH_FINAL_ACCEPTANCE.md
CURRENT_HEAD_CHARACTER_TEMPLATE_PREFIX = 23 20 4D
HISTORICAL_DIAGNOSTIC_SUPERSEDED_FOR_FINAL_STATUS = YES
```
