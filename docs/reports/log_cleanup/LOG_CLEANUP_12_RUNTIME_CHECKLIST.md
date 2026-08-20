# LOG-CLEANUP-12 — Final human runtime record

Status: `PASS`

## Session

- Victoria 3: `release/1.13.9`
- Hash: `afea32b87`
- Country: Netherlands
- End date: 21 January 1776
- Visual problems: none reported
- Crash: no
- Shutdown: normal from inside the game
- Final log markers: `Quit: Quit from inside game`, then
  `Transition Game->Empty`

## Runtime result

- `ORIGINAL_214_RUNTIME_PASS = YES`
- `EXTENSION_23_RUNTIME_PASS = YES`
- `LEGACY_INTEREST_MARKER_REGION_ERRORS_AFTER = 0`
- `LEGACY_INTEREST_MARKER_REGION_IDENTITIES_AFTER = 0`
- `BRAZIL_PARENT_API_ERROR_AFTER = 0`
- `NEW_RUNTIME_SR_SCRIPT_IDENTITIES_AFTER = 0`
- `LEGACY_REGION_EVENTTARGET_PHYSICAL_REFERENCES_AFTER = 0`
- `NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_EXTENSION = 0`
- `KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 0`

No fresh diagnostic reproduced any of the 22 former
`has_interest_marker_in_region` arguments for `region_persia`,
`region_arabic`, `region_italy`, `region_manchuria`, or
`region_dixie`. No corrected extension site emitted a replacement-object
diagnostic.

The original technical targets also remained at zero:

- `law_per_capita_taxation = 0`
- `law_charity_hospitals = 0`
- `law_tenent_farmers = 0`
- `ig_devot = 0`
- targeted DWI diagnostic = 0
- `Invalid strategic region = 0`
- `Invalid right side during comparison 'sr' = 0`
- `Given law is a variant, we expect the parent = 0`

## Canonical residuals

The fresh loader reproduced exactly:

- `state_religion = 18` runtime rows;
- `OTHER_DESIGN_DEBT_DEFERRED_UNIQUE_PHYSICAL = 17`;
- `amendment_frugal_ordinance = 4`;
- `COUNTRY_LAW_DIAGNOSTICS_OBSERVED = 113`.

Classifications remain:

- the 18 `state_religion` rows and 113 country-law diagnostics:
  `KNOWN_FORK_DESIGN_DEBT_DEFERRED`, for future `LAW-SYSTEM-1776`;
- the 4 amendment rows: `ALREADY_ACCOUNTED_FOR`, `PROTECTED_JAPAN`.

## Final counters

```text
LOG12_ORIGINAL_CONFIRMED_ERRORS_PATCHED = 214
LOG12_EXTENSION_CONFIRMED_ERRORS_PATCHED = 23
TOTAL_CONFIRMED_ERRORS_PATCHED = 237

ORIGINAL_214_RUNTIME_PASS = YES
EXTENSION_23_RUNTIME_PASS = YES

NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_EXTENSION = 0
KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 0
KNOWN_FORK_DESIGN_DEBT_DEFERRED = 113

OTHER_DESIGN_DEBT_DEFERRED_LOG_ROWS = 18
OTHER_DESIGN_DEBT_DEFERRED_UNIQUE_PHYSICAL = 17
JAPAN_NONACTIONABLE = 4

LOG_CLEANUP_12 = PASS
RUNTIME_HUMAN_REQUIRED = NO
NEXT_PHASE = LOG-CLEANUP-13-FINAL-GLOBAL-REINDEX-QA

ESTIMATED_PHASES_REMAINING_MIN = 1
ESTIMATED_PHASES_REMAINING_LIKELY = 1
ESTIMATED_PHASES_REMAINING_MAX = 1
```

No staging, commit, or push is part of this finalization.
