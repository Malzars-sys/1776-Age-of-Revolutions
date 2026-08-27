# TECH6A-2C — French Gabelle Integration

Date: 2026-08-27  
Project: Victoria 3 — 1776 Age of Revolutions  
Branch: `tech4c2-audit-snapshot`  
Vanilla reference: Victoria 3 1.13.9 (`C:\Games\Victoria 3\game`)  
Source mod: La Gabelle 1.0.2 (`3715913236`)  
Redistribution permission: **PENDING**  
Runtime status: **USER RETEST REQUIRED AFTER MONTHLY-CONTROLLER FIX**

## 1. Result

TECH6A-2C is statically complete; the latest runtime correction still requires user confirmation.

France starts on 1776-01-01 with its already existing consumption tax on `g:salt` and now receives the French Gabelle Journal Entry. While that tax is active, the Gabelle applies the exact fiscal and standard-of-living values found in La Gabelle 1.0.2. Two France-only events provide the crisis, abolition, reform, and suppression paths.

The inaccessible reform-event bug in La Gabelle 1.0.2 is confirmed and corrected locally. The implementation uses a country variable and two mutually exclusive active Journal Entry phases so that the original and reformed modifiers do not remain stacked.

A runtime issue subsequently reported by the user was also addressed: repeatedly removing and restoring the salt tax caused `modifiers_while_active` to propagate another Gabelle modifier instance every time the same Journal Entry reactivated. A first country-modifier workaround removed the duplication but failed its runtime return test because JE reactivation did not replay `immediate` as expected. A second suspended-JE state machine also failed because the engine retained a hidden suspended instance and rejected attempts to add it again.

The current architecture never transitions from a disappearing JE. Removing the tax invalidates and destroys the active phase. Each live phase now exposes its already-existing inactive database instance only when France, the salt tax, and the correct reform state match. The canonical `on_monthly_pulse_country` controller adds a fresh phase only when neither an active nor an inactive instance exists. `je_gabelle_suspended` remains only as a save-cleanup definition for saves produced by the superseded second fix; no current script creates it.

Codex did not launch the game. The user performed four runtime iterations; the latest inactive-entry activation correction is statically validated but not yet runtime-confirmed.

## 2. Required baseline read before implementation

The following project reports were read before editing:

- `docs/reports/technology/TECH6A1_LA_GABELLE_SALT_AUDIT.md`
- `docs/reports/technology/TECH6A1B_LOCAL_SALT_CORE_IMPLEMENTATION_REPORT.md`
- `docs/reports/technology/TECH6A2_SALT_RESOURCE_DISCOVERY_IMPLEMENTATION_REPORT.md`

The already implemented salt good, buildings, production methods, resource geography, starting production, prestige good, and salt companies were treated as frozen baseline. Salt companies were therefore not re-imported in TECH6A-2C.

## 3. La Gabelle files inspected directly

### French mechanism

- `common/journal_entries/lagab_fra.txt`
- `common/static_modifiers/lagab_static_modifiers.txt`
- `events/lagab_france.txt`
- `common/on_actions/lagab_on_actions.txt`
- `common/history/global/lagab_global.txt`
- `localization/english/lagab_journal_entries_l_english.yml`
- `localization/english/lagab_modifiers_l_english.yml`
- `localization/english/lagab_events_l_english.yml`
- corresponding French localization files
- `gfx/interface/icons/event_icons/gabelle.dds`

### Rejected neighboring systems checked for closure

- `events/lagab_generic.txt`
- `events/lagab_india.txt`
- `common/mobilization_options/lagab_mobilization_option.txt`
- `common/scripted_triggers/lagab_community_mod_triggers.txt`
- `gui/lagab_salt_texticons.gui`

The relevant triggers, effects, political movements, laws, modifier types, media aliases, and icons were also checked against vanilla 1.13.9.

## 4. Minimal dependency inventory

| Category | ID | Source | Direct dependencies | Localization / linked objects | Decision |
|---|---|---|---|---|---|
| Existing good | `salt` / `g:salt` | Existing TECH6A baseline | Salt good already loaded | `$salt$`, `@salt!` | Reused unchanged |
| Existing setup tax | `add_taxed_goods = g:salt` | Existing French country history | France setup | Salt good | Reused exactly once |
| Journal Entry | `je_gabelle` | `common/journal_entries/lagab_fra.txt` | `c:FRA`, `has_consumption_tax = g:salt`, `gabelle_income_active` | JE title/reason/description/header | Adapted as non-reactivated active phase |
| Journal Entry phase | `je_gabelle_reformed` | Local 1776 adaptation | country variable, salt tax, `gabelle_income_reformed_active` | Reformed JE title/reason/description | Added as minimal state-transition support |
| Legacy Journal Entry | `je_gabelle_suspended` | Superseded runtime correction | France; completion on restored salt tax | Suspended cleanup text | Retained only to close stale save instances; no creation path |
| Static modifier | `gabelle_income` | `common/static_modifiers/lagab_static_modifiers.txt` | vanilla modifier types and coin icon | `gabelle_income` | Imported with exact values |
| Static modifier | `gabelle_income_reformed` | same | vanilla modifier types and coin icon | `gabelle_income_reformed` | Imported with exact values |
| Active JE modifier | `gabelle_income_active` | Local runtime adaptation of `gabelle_income` | vanilla modifier types and coin icon | `gabelle_income_active` | Exact-value live ID, separated from legacy timed save data |
| Active JE modifier | `gabelle_income_reformed_active` | Local runtime adaptation of `gabelle_income_reformed` | vanilla modifier types and coin icon | `gabelle_income_reformed_active` | Exact-value live ID, separated from legacy timed save data |
| Timed modifier | `modifier_suppress_dissent` | same | political movement scope, vanilla fist icon | `modifier_suppress_dissent` | Imported with exact value |
| Event | `lagab_france.1` | `events/lagab_france.txt` | French salt tax, revolution, civil-war effects | title/description/flavor/options | Adapted |
| Event | `lagab_france.2` | same | French salt tax, active original JE, eligible movement, country variable | title/description/flavor/options | Adapted and bug-fixed |
| Variable | `lagab_gabelle_reformed` | source event | set by reform option, checked by event and JEs | none | Changed from global to country scope |
| Monthly hook | `lagab_france.1`, `.2` | `common/on_actions/lagab_on_actions.txt` | `on_monthly_pulse_country` | both events | Manually integrated into existing mod hook |
| Monthly controller | original/reformed JE restoration | Local runtime correction | France, salt tax, reform variable, absence of both active phases | active JEs | Integrated into the canonical monthly `effect` block |
| Start hook | `je_gabelle` | source global history architecture | French country history | existing French salt tax | Adapted to 1776 country setup |

No external scripted trigger or scripted effect is required by this closure.

## 5. Journal Entry behavior

### Initial phase: `je_gabelle`

- Restricted to `c:FRA` and possible only with `has_consumption_tax = g:salt`.
- Added directly to the 1776 French setup after the existing salt tax.
- Applies exactly one locked `gabelle_income_active` while active.
- Invalidates without an `on_invalid` transition when the salt tax disappears.
- Completes when the country variable `lagab_gabelle_reformed` is set; that variable makes the already-existing inactive reformed phase eligible for native activation.

### Reformed phase: `je_gabelle_reformed`

- Restricted to `c:FRA` and requires both the reform variable and salt tax.
- Applies exactly one locked `gabelle_income_reformed_active` while active.
- Invalidates without an `on_invalid` transition when the salt tax disappears.
- Does not complete by itself.

### Canonical monthly controller

The controller is inside the existing `effect` of `common/on_actions/00_code_on_actions.txt`. The separate extension file contains only `events` and `random_events`; it no longer defines a second `effect` field.

On each monthly country pulse, France is handled as follows:

1. legacy timed country modifiers are cleaned once; obsolete marker variables are left unread and harmless to avoid false used-without-set validation errors;
2. if the salt tax is absent, no active Gabelle JE is created;
3. if the correct phase already exists inactive, it is left to the native JE lifecycle and is never added a second time;
4. if neither an active nor an inactive instance of the correct phase exists, exactly one fresh phase is created;
5. the three-consecutive-month reform timer is evaluated here as well, preserving the later local refinement without introducing a second `effect` field.

This prevents `add_journal_entry` from colliding with a database entry that is already inactive. A previously absent phase is restored on the monthly pulse; a pre-existing inactive phase activates through its `is_shown_when_inactive` and `possible` conditions, checked by the engine at most every 14 days.

### Legacy suspended phase

`je_gabelle_suspended` is retained solely so saves produced by the superseded second fix can resolve and complete that stale object. It has no modifier and no `on_complete`, `on_invalid`, or JE-creation effect. No current path creates it.

### Runtime evidence behind the correction

The second test produced 458 repeated missing-modifier errors from the earlier timed-country workaround. The third test produced `Royaume de France already has a journal entry of type je_gabelle_suspended`, proving that the suspended object existed internally even though it was not visible. The same log reported `There is more than one 'effect' defined using most recent: common/on_actions/06_mod_on_actions.txt:2`, proving that the separate monthly cleanup/controller field displaced the canonical monthly effect instead of merging safely.

The fourth runtime test then produced `Royaume de France already has a journal entry of type je_gabelle_reformed`. Direct save inspection confirmed `definition="FRA"` is country `4`, `lagab_gabelle_reformed` is true, and France's `je_gabelle_reformed` object exists with `active=no` and `date_added=1776.1.1`. The cause was therefore not a missing reform variable: `is_shown_when_inactive = { always = no }` permanently hid the existing inactive instance while the controller incorrectly tried to add it again.

The current correction removes all three failure sources: active JEs have no disappearing-JE transitions, all controller effects are merged into the single canonical monthly effect, and inactive instances are both eligible for native activation and explicitly excluded from `add_journal_entry` paths.

Central relation:

`France + active g:salt tax + monthly pulse -> exactly one active Gabelle JE -> exactly one Gabelle effect`

## 6. Exact modifiers

### `gabelle_income`

| Modifier type | Source value | Gameplay meaning |
|---|---:|---|
| `state_tax_collection_mult` | `0.15` | +15% general tax collection |
| `state_lower_strata_standard_of_living_add` | `-1.5` | -1.5 Lower Strata SoL |
| `state_middle_strata_standard_of_living_add` | `-0.5` | -0.5 Middle Strata SoL |

The live original JE uses `gabelle_income_active`, an exact-value duplicate with a separate technical ID. The source ID `gabelle_income` is retained only so older saves can resolve and remove the superseded timed modifier cleanly.

### `gabelle_income_reformed`

| Modifier type | Source value | Gameplay meaning |
|---|---:|---|
| `state_tax_collection_mult` | `0.10` | +10% general tax collection |
| `state_lower_strata_standard_of_living_add` | `-1` | -1 Lower Strata SoL |

No Middle or Upper Strata SoL effect is defined for the reformed modifier.

The live reformed JE likewise uses the exact-value duplicate `gabelle_income_reformed_active`; `gabelle_income_reformed` remains as the migration-compatible legacy ID.

### `modifier_suppress_dissent`

| Modifier type | Source value | Duration |
|---|---:|---:|
| `political_movement_radicalism_add` | `0.15` | 1 year |

`GABELLE_REVENUE_MECHANIC = GENERAL_TAX_COLLECTION_MODIFIER`

The fiscal bonus is general tax collection, as in La Gabelle 1.0.2. It is not an isolated multiplier on salt-tax revenue.

## 7. French events

### Imported and adapted: 2

#### `lagab_france.1` — Crisis of Legitimacy

- Trigger: France, active salt tax, one of the two Gabelle JE phases, and a revolution at medium progress.
- Immediate: saves a revolutionary civil-war scope.
- Option A: enforce order; revolution advances.
- Option B: empty promises; random retreat or large advance.
- Option C: abolish the Gabelle; adds Lower Strata loyalists, removes `g:salt` taxation, and slightly reduces revolution progress.
- Adaptation: explicit Gabelle JE requirement added so the event belongs only to the implemented French chain.

#### `lagab_france.2` — Voices of Reform

- Trigger: France, active salt tax, unreformed `je_gabelle`, reform variable absent, and at least one eligible political movement.
- Immediate: saves one eligible political movement.
- Option A: sets the country variable `lagab_gabelle_reformed`; the original JE completes and the reformed JE replaces it.
- Option B: gives the selected movement `modifier_suppress_dissent` for one year.
- Adaptation: broken global-variable prerequisite removed; variable localized to France; modifier transition moved into the explicit JE state machine.

### Rejected events: 5

- `lagab_generic.1`
- `lagab_generic.2`
- `lagab_generic.3`
- `lagab_generic.4`
- `lagab_india.1`

They are not necessary to the French Gabelle and would broaden the phase into global salt-tax, black-market, interventionism, or Indian protest systems.

The generic and India monthly on-action pools were rejected with them.

## 8. Confirmed reform bug and correction

La Gabelle 1.0.2 contains only two references to `lagab_gabelle_reformed`:

1. the trigger of `lagab_france.2` requires `has_global_variable = lagab_gabelle_reformed`;
2. option A of that same event executes `set_global_variable = lagab_gabelle_reformed`.

Therefore the event requires the variable before the only source path can create it. The bug is confirmed.

The local correction is:

1. the event requires `NOT = { has_variable = lagab_gabelle_reformed }`;
2. reform option A executes `set_variable = lagab_gabelle_reformed` on France;
3. `je_gabelle` completes on that country variable;
4. the reform variable makes the inactive `je_gabelle_reformed` phase visible and possible, allowing the native JE lifecycle to activate it;
5. the reformed JE applies `gabelle_income_reformed_active` instead of stacking it with `gabelle_income_active`.

Expected reachable flow:

`active Gabelle -> eligible reform movement -> lagab_france.2 -> reform option -> country variable -> reformed Gabelle JE`

## 9. 1776 compatibility

- The Gabelle already existed in France in 1776, so direct addition in the French 1776 setup is appropriate.
- No event contains a fixed date.
- No Louis-Philippe, July Monarchy, 1836, 1790, or 1806 dependency was imported.
- Event descriptions were rewritten to avoid later-period framing.
- All referenced movements, laws, civil-war effects, videos, icons, modifier types, triggers, and effects were found in vanilla 1.13.9.
- No decision was made about France's temporary administrative starting technologies.

`COUNTRY_STARTING_TECH_AUDIT = DEFERRED_TO_GLOBAL_SETUP_PHASE`

## 10. Imported, adapted, and rejected scope

### Implemented locally

- 2 live Journal Entry phases: original and reformed, plus one legacy cleanup definition for old saves.
- 5 modifier definitions: 2 live JE IDs, 2 legacy cleanup IDs, and 1 suppression modifier.
- 2 French events.
- 1 France-specific monthly event pool and 1 restoration controller integrated into the existing monthly country on-action.
- English and French localizations.
- 1 French starting-JE reference beside the existing salt tax.

### Explicitly not imported

- other countries' starting salt taxes;
- global history from La Gabelle;
- four generic events and the India event;
- generic and India on-action pools;
- black-market, Gandhi, and interventionism modifiers;
- new salt resources, buildings, goods, production methods, needs, prestige goods, or companies;
- military and mobilization systems;
- La Gabelle text-icon GUI;
- custom `gabelle.dds` event icon.

The implementation uses the existing vanilla `event_protest.dds`, so TECH6A-2C adds no new graphical asset.

## 11. Files changed or created

### Existing project files modified with small integration references

- `common/history/countries/fra - france.txt`
  - adds the starting `je_gabelle` after the pre-existing `add_taxed_goods = g:salt`;
  - does not add or change any starting technology.
- `common/on_actions/06_mod_on_actions.txt`
  - adds only `lagab_france.1` and `lagab_france.2` to the existing monthly event pool;
  - deliberately contains no `effect` field.
- `common/on_actions/00_code_on_actions.txt`
  - adds the France-only restoration controller to the already existing canonical monthly `effect` block;
  - performs one-time cleanup of legacy timed country modifiers.

### Local-only La Gabelle-derived files created

- `common/journal_entries/11_tech6a2c_french_gabelle.txt`
- `common/static_modifiers/10_tech6a2c_french_gabelle.txt`
- `events/tech6a2c_french_gabelle.txt`
- `localization/english/tech6a2c_french_gabelle_l_english.yml`
- `localization/french/tech6a2c_french_gabelle_l_french.yml`

### Report created

- `docs/reports/technology/TECH6A2C_FRENCH_GABELLE_IMPLEMENTATION_REPORT.md`

## 12. Local Git exclusion and rights status

The five La Gabelle-derived gameplay/localization files above are listed exactly in `.git/info/exclude`.

Validation result:

- derived files tracked: `0`;
- derived files staged: `0`;
- derived files locally excluded: `5/5`;
- previously imported La Gabelle salt/building/company/prestige assets still tracked: `0/10`;
- those ten existing local assets staged: `0/10` and locally excluded: `10/10`;
- public `.gitignore` modified: no;
- commit created: no;
- push performed: no;
- Steam publication or release: none.

The three small integration edits in existing project files also remain uncommitted and unstaged.

## 13. Static validation

| Test | Result | Evidence |
|---|---|---|
| GAB-S01 | PASS | exact `je_gabelle` definition count = 1 |
| GAB-S02 | PASS | exact `gabelle_income` definition count = 1 |
| GAB-S03 | PASS | all required keys exist in both English and French |
| GAB-S04 | PASS | both monthly event references resolve exactly once |
| GAB-S05 | PASS | checked reform variable has a reachable setter |
| GAB-S06 | PASS | reform event requires variable absence and its option creates it |
| GAB-S07 | PASS | all salt-tax chain references use `g:salt` |
| GAB-S08 | PASS | no invalid `add_taxed_goods = salt` in TECH6A history |
| GAB-S09 | PASS | French country history contains exactly one `add_taxed_goods = g:salt` |
| GAB-S10 | PASS | global history contains zero salt-tax grants |
| GAB-S11 | PASS | all six frozen salt-system SHA-256 hashes unchanged |
| GAB-S12 | PASS | 15-file State Region manifest unchanged |
| GAB-S13 | PASS | resource potentials covered by unchanged State Region manifest |
| GAB-S14 | PASS | industry file / existing `pm_bakery` hash unchanged |
| GAB-S15 | PASS | existing salt pop-needs hash unchanged |
| GAB-S16 | PASS | both active JE phases, legacy cleanup phase, controller, and events are restricted to `c:FRA` |
| GAB-S17 | PASS | no anachronistic marker; all used 1.13.9 dependencies verified |
| GAB-S18 | PASS | five new derived files and ten pre-existing source assets are untracked, unstaged, and locally excluded |

### Runtime duplication/return regression fix — static checks

| Test | Result | Evidence |
|---|---|---|
| GAB-FIX-S01 | PASS | active JEs contain no `can_deactivate`, so an instance cannot reactivate in place |
| GAB-FIX-S02 | PASS | original and reformed active phases each contain exactly one distinct `*_active` modifier ID |
| GAB-FIX-S03 | PASS | both active phases invalidate when the salt tax is absent |
| GAB-FIX-S04 | PASS | active phases contain no `on_invalid`; a disappearing JE cannot initiate a transition |
| GAB-FIX-S05 | PASS | the canonical monthly controller requires `g:salt` taxation and absence of both active phases |
| GAB-FIX-S06 | PASS | each add path also requires absence of its matching inactive JE, preventing `already has` collisions |
| GAB-FIX-S07 | PASS | `common/on_actions/06_mod_on_actions.txt` contains no competing `effect` field |
| GAB-FIX-S08 | PASS | the legacy suspended phase has no modifier or JE-creation effect |
| GAB-FIX-S09 | PASS | migration is FRA-only, removes only legacy timed modifier IDs, and records a new controller marker |
| GAB-FIX-S10 | PASS | invalid event AI field `multiply = 2` was replaced by valid `add = 1` |
| GAB-FIX-S11 | PASS | both live phases expose inactive instances only for France, with salt taxation and the matching reform state |
| GAB-FIX-S12 | PASS | the three-month reform timer is preserved inside the one canonical monthly `effect` block |

Additional validation:

- braces balanced in the two modified integration files and three new script files;
- English and French localization files have valid language headers and UTF-8 BOM;
- no duplicated French starting salt tax;
- no duplicated event or modifier definition;
- current HEAD remains `907940e5ec94399afd14ddb5fa5ab82c3b7dbf61`.

### Frozen baseline hashes

| Baseline object/file | SHA-256 after TECH6A-2C |
|---|---|
| salt good | `3A7BBC678AD86E99712308CD33C2FCBF82AC988BC3948C8CBB889CA24E52BC32` |
| pop needs | `F365D9E22C3DAA8096E717E6FBEE8DB2419CBEC303F48B5740BF9CE44134D346` |
| industry PMs | `60368105DA9D0D33D6F4919961B2316D0316914CA90E417F7F4EDB8464C8C3D5` |
| salt buildings | `5C25D068798426DC867663E5B79C1F8E72FD21BE5D5CBE06382E067DE5202305` |
| salt producer PMs | `F36F146CC27B26F349493FCCC78779347A236C4770361DA97B6AA7B615F52933` |
| starting salt buildings | `8C34A0381B58C4D97C5DE402A4DABF79F09BBD3ABDE59744EBD3457BD24134E9` |
| 15 State Region manifest | `FC854FE0EB69DE76001D010C44E6C87070E86303F9BAE42906FA31197A7A6F07` |

## 14. User runtime checklist

Codex did not launch Victoria 3. The user must perform these checks:

- [ ] **RUNTIME-GAB-01** — Start a new France game on 1776-01-01.
- [ ] **RUNTIME-GAB-02** — Confirm that the salt consumption tax is present immediately.
- [ ] **RUNTIME-GAB-03** — Confirm that it shows a real revenue value and the correct salt icon.
- [ ] **RUNTIME-GAB-04** — Confirm that `je_gabelle` is present.
- [ ] **RUNTIME-GAB-05** — Confirm that `gabelle_income` is active while expected.
- [ ] **RUNTIME-GAB-06** — Compare general tax income with and without the Gabelle effect.
- [ ] **RUNTIME-GAB-07** — Confirm the `-1.5` Lower Strata SoL effect.
- [ ] **RUNTIME-GAB-08** — Confirm the `-0.5` Middle Strata SoL effect.
- [ ] **RUNTIME-GAB-09** — Confirm that Upper Strata receives no unexpected SoL penalty.
- [ ] **RUNTIME-GAB-10** — From the current 30 May 1776 save, leave the restored salt tax active and advance beyond 1 June. Confirm that `La Gabelle` returns with exactly one modifier icon/effect.
- [ ] **RUNTIME-GAB-10B** — Remove the salt tax and let the active JE disappear. Restore the tax, pass the next first day of a month, and confirm that one fresh active phase returns. Repeat this cycle at least three times; no suspended phase is expected in new cycles.
- [ ] **RUNTIME-GAB-11** — Create the political conditions required by the reform event.
- [ ] **RUNTIME-GAB-12** — Confirm that `lagab_france.2` can actually fire.
- [ ] **RUNTIME-GAB-13** — From the 6 May save, choose reform, unpause, and advance up to 14 days. Confirm that `La Gabelle réformée` activates with exactly one reformed modifier and without an `already has ... je_gabelle_reformed` error.
- [ ] **RUNTIME-GAB-14** — Save and reload.
- [ ] **RUNTIME-GAB-15** — Confirm that the JE phase and reform variable persist correctly.
- [ ] **RUNTIME-GAB-16** — Inspect `error.log`, `game.log`, and `debug.log` for `je_gabelle`, `gabelle_income`, `lagab_france`, `lagab_gabelle_reformed`, `salt`, `unknown modifier`, `unknown event`, `unknown journal entry`, `invalid trigger`, and `invalid effect`.
- [ ] **RUNTIME-GAB-17** — Confirm that no other country receives the French Gabelle.

`RUNTIME_STATUS = USER_RETEST_REQUIRED_AFTER_CONTROLLER_FIX`

## 15. Mandatory final summary

```text
TECH6A2C_FRENCH_GABELLE = STATIC_PASS_RUNTIME_RETEST_REQUIRED

JE_GABELLE_IMPLEMENTED = YES
GABELLE_INCOME_MODIFIER_IMPLEMENTED = YES
GABELLE_MODIFIER_DUPLICATION_FIX_IMPLEMENTED = YES
GABELLE_MODIFIER_RETURN_FIX_IMPLEMENTED = YES
GABELLE_MODIFIER_RETURN_RUNTIME_CONFIRMED = NO
GABELLE_REFORMED_JE_ACTIVATION_FIX_IMPLEMENTED = YES
GABELLE_REFORMED_JE_ACTIVATION_RUNTIME_CONFIRMED = NO
GABELLE_ONLY_APPLIES_TO_FRA = YES
FRA_STARTS_WITH_SALT_TAX = YES

SALT_TAX_SCOPE = g:salt

GABELLE_TAX_MECHANIC = GENERAL_TAX_COLLECTION
GABELLE_TAX_COLLECTION_VALUE = +15%
GABELLE_LOWER_STRATA_SOL_EFFECT = -1.5
GABELLE_MIDDLE_STRATA_SOL_EFFECT = -0.5

GABELLE_EVENTS_IMPORTED = 2
GABELLE_EVENTS_ADAPTED_FOR_1776 = 2

LAGAB_GABELLE_REFORMED_TRIGGER_BUG = CONFIRMED
LAGAB_GABELLE_REFORMED_BUG_FIXED = YES

SALT_BALANCE_VALUES_CHANGED = NO
SALT_RESOURCE_MAP_CHANGED = NO
SALT_POTENTIAL_CHANGED = NO

COUNTRY_STARTING_TECH_AUDIT = DEFERRED

STATIC_TESTS = PASS

RUNTIME_TEST_REQUIRED_BY_USER = YES
RUNTIME_TEST_PERFORMED_BY_CODEX = NO
RUNTIME_STATUS = USER_RETEST_REQUIRED_AFTER_CONTROLLER_FIX

LA_GABELLE_PERMISSION = PENDING
LA_GABELLE_DERIVED_FILES_GIT_TRACKED = NO
LA_GABELLE_DERIVED_FILES_GIT_STAGED = NO

COMMITS_CREATED = 0
PUSH_PERFORMED = NO

READY_FOR_USER_RUNTIME_TEST = YES
```
