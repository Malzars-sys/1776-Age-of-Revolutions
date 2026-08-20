# LOG-CLEANUP-11 — Human runtime checklist

Final status: `PASS`

This checklist validates only the B01 geography and B02 Landowners patches.
The 113 country-law diagnostics are known design debt deferred to
`LAW-SYSTEM-1776`; their presence does not fail LOG-CLEANUP-11.

## Test setup

- [x] Confirm Victoria 3 is `release/1.13.9`, hash `afea32b87`.
- [x] Enable only the local mod `1776_Age_of_Revolutions_fork`.
- [x] Start a new 1776 game as the Netherlands.
- [x] Play through 14 January, exceeding the one-week minimum.
- [x] Observe that loading and play do not crash.
- [x] Check that no raw localization key is visible.
- [x] Quit normally from inside the game.
- [x] Preserve and check the fresh debug, error, system and game rotations.

Do not reuse an old session as validation. Record the game version, executable
hash if available, session timestamps, chosen country, elapsed game time, and
normal shutdown marker.

## B01 — Geography

Search all retained rotations for:

- `Invalid right side during comparison 'sr'`
- `common/journal_entries/01_natural_borders_of_france.txt`
- `common/journal_entries/02_south_america_migration.txt`
- `common/journal_entries/06_cuba.txt`
- `common/journal_entries/07_american_mod_jes.txt`
- `common/dynamic_country_names/00_dynamic_country_names.txt`
- `common/scripted_buttons/00_new_colonial_admins.txt`
- each of the seven canonical identities `RR-01`, `RR-02`, `RR-03`,
  `RR-04`, `RR-05`, `RR-07`, and `RR-08` using the paths and original
  lines recorded in `LOG_CLEANUP_11_PATCH_MATRIX.csv`

Observed:

- `B01_AFTER = 0`
- no Natural Borders error loop saturating the rotations
- `LEGACY_GEOGRAPHIC_PHYSICAL_REFERENCES_RUNTIME_AFTER = 0`

## B02 — Landowners

Search all retained rotations for:

- `common/interest_groups/00_landowners.txt`
- `has_law_or_variant trigger`
- `Given law is a variant, we expect the parent`

Observed:

- `B02_AFTER = 0`
- canonical identity `RR-06` absent

## Deferred country-law diagnostics

Preserve any initialization diagnostics from:

- `CL-G01_TECH_PREREQUISITES`
- `CL-G02_VARIANT_VISIBILITY`
- `CL-G03_CONFLICTING_LAWS`

If visible, count and archive them for `LAW-SYSTEM-1776`. Do not classify
them as LOG-CLEANUP-11 regressions, fixes, vanilla/external errors, false
positives, or non-errors.

Observed cleanup classification:

- `COUNTRY_LAW_DIAGNOSTICS_TOTAL = 113`
- `COUNTRY_LAW_DEFERRED_DESIGN_DEPENDENCY = 113`
- `COUNTRY_LAW_CURRENT_CLEANUP_BLOCKERS = 0`

## Regression check

Search all rotations for any new error whose path or call stack points to one
of the seven changed gameplay files. Also confirm the already closed families
do not return:

- `country_convoys_capacity_mult`
- `country_law_enactment_time_mult`
- legacy `dreadnought` Hegemon reference
- `region_caucasus`
- the 49 LOG-CLEANUP-7 AI residuals
- `commander_leader_chance`
- `executive_leader_chance`
- `lands_of_anarchy_tribe_recieved_medicine_mod`
- `ig_law_enactment_time_good`
- `ig_law_enactment_time_stall`

Observed:

- `NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_PATCH = 0`
- `KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 0`
- `KNOWN_FORK_DESIGN_DEBT_DEFERRED = 113`

## Recorded result

```text
VICTORIA_3_VERSION = release/1.13.9
VICTORIA_3_HASH = afea32b87
SESSION_START = fresh new-game session
SESSION_END = 14 January
COUNTRY = Netherlands
IN_GAME_DURATION = through 14 January
SHUTDOWN = normal quit from inside game

CRASH = NO
RAW_LOCALIZATION_KEY = NO

B01_AFTER = 0
B02_AFTER = 0
NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_PATCH = 0

COUNTRY_LAW_DIAGNOSTICS_OBSERVED = 113
COUNTRY_LAW_CLASSIFICATION = KNOWN_FORK_DESIGN_DEBT_DEFERRED

KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 0
KNOWN_FORK_DESIGN_DEBT_DEFERRED = 113

LOG_CLEANUP_11 = PASS
```

## Newly exposed residual — not a LOG-CLEANUP-11 regression

The disappearance of the Natural Borders loop exposed a pre-existing legacy
geographic family in the retained rotations:

- `NEW_RUNTIME_SR_SCRIPT_IDENTITIES = 7`
- `NEW_RUNTIME_SR_OCCURRENCES = 2149`
- `LEGACY_REGION_EVENTTARGET_PHYSICAL_REFERENCES = 207`
- `LEGACY_REGION_EVENTTARGET_FILES = 39`

The seven Script System identities are included in the 207 physical
references; they are not additive.

Exact runtime identities:

- `common/journal_entries/00_major_railroads.txt:12` — 1048
- `common/journal_entries/00_major_railroads.txt:13` — 1048
- `common/journal_entries/07_hindustan_is_durrani_mod.txt:15` — 13
- `common/journal_entries/07_hindustan_is_durrani_mod.txt:41` — 13
- `common/journal_entries/07_hindustan_is_durrani_mod.txt:42` — 13
- `common/journal_entries/07_hindustan_is_durrani_mod.txt:43` — 13
- `common/journal_entries/03_afghanistan.txt:1834` — 1

The same session also recorded, pending attribution:

- `INVALID_NON_REGION_DATABASE_OBJECT_REFERENCES = 27`
- `OTHER_EVENTTARGET_SCOPE_FAILURES = 2`

No item in this newly exposed residual was corrected or classified during
LOG-CLEANUP-11.

`NEXT_PHASE = LOG-CLEANUP-12-GLOBAL-LEGACY-REGION-EVENTTARGET-CLOSURE`

Do not stage, commit or push before the finalized result is reviewed.
