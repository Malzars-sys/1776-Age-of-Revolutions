# LOG-CLEANUP-11 — Grouped residual corrections

Status: `PASS`

Branch: `post-2.3.0-log-cleanup`

Baseline commit: `9b588c52630b0ccaccff5aaa559999a899a086ab`

Target runtime: Victoria 3 `release/1.13.9`, hash `afea32b87`

## Upstream Tsar 2.3.0.1 audit

The previously completed upstream audit remains canonical:

- `TSAR_UPSTREAM_VERSION_AUDITED = 2.3.0.1`
- `GLOBAL_UPSTREAM_MERGE_REQUIRED = NO`
- `UPSTREAM_TECHNICAL_FIX_REQUIRED = NO`

No upstream audit or merge was repeated. The Tsar replacements, the upstream
Iraq–Persia diplomatic-play deletion, the Count of Gálvez addition, the three
Japanese armies, and the already-integrated colonial classifications remain
outside LOG-CLEANUP-11.

## Canonical country-law deferral

The COUNTRY-LAW DESIGN DEFERRAL addendum overrides the original B03, B04 and
B05 implementation instructions. The 113 diagnostics remain known fork debt,
but are not current cleanup blockers:

- `COUNTRY_LAW_DIAGNOSTICS_TOTAL = 113`
- `COUNTRY_LAW_DEFERRED_DESIGN_DEPENDENCY = 113`
- `COUNTRY_LAW_CURRENT_CLEANUP_BLOCKERS = 0`
- `CL_G01_TECH_PREREQUISITES = DEFERRED_DESIGN_DEPENDENCY` (105)
- `CL_G02_VARIANT_VISIBILITY = DEFERRED_DESIGN_DEPENDENCY` (7)
- `CL_G03_CONFLICTING_LAWS = DEFERRED_DESIGN_DEPENDENCY` (1)
- canonical classification: `KNOWN_FORK_DESIGN_DEBT_DEFERRED`
- future phase: `LAW-SYSTEM-1776`

They are not classified as `FIXED`, `VANILLA_OR_EXTERNAL`,
`FALSE_POSITIVE` or `NON_ERROR`. No country-history law setup, starting
technology, law definition, law variant, or Bavaria law set was modified.

The deferral is required until the 1776 technology tree, political-map
architecture, period-specific laws, and final historical country-law
assignments have been designed together.

## Preflight

The worktree and index were clean before the phase. LOG-CLEANUP-10 was already
committed at `9b588c5`. The expected branch was active. No stash, reset,
checkout, add, commit or push was performed.

## B01 — Geography

`GEOGRAPHY_MIGRATION_SAFE = YES`

LOG-CLEANUP-10 observed 17 physical runtime manifestations representing seven
canonical identities. A complete static sweep of the same root cause in the
six allowlisted files found another 64 latent references:

- `B01_CANONICAL_ERRORS_BEFORE = 7`
- `B01_RUNTIME_PHYSICAL_MANIFESTATIONS_BEFORE = 17`
- `B01_LATENT_STATIC_REFERENCES_DISCOVERED = 64`
- `B01_STATIC_REFERENCES_BEFORE = 81`
- `B01_PHYSICAL_REFERENCES_PATCHED = 81`
- `B01_STATIC_REFERENCES_AFTER = 0`
- `B01_ERRORS_PATCHED = 7` (runtime confirmed)

The count of 17 remains the runtime-observed baseline, not the full static
footprint. Fixing only those 17 sites would have left the same invalid API in
reachable sibling blocks, so the entire proven cause was corrected inside the
existing six-file allowlist.

Every state-scope expression was migrated from
`region = sr:region_legacy` to
`is_in_geographic_region = geographic_region_*_old`. The exact mappings are:

| Legacy strategic region | Exact geographic object |
| --- | --- |
| `region_madras` | `geographic_region_madras_old` |
| `region_bombay` | `geographic_region_bombay_old` |
| `region_bengal` | `geographic_region_bengal_old` |
| `region_rhine` | `geographic_region_rhine_old` |
| `region_north_germany` | `geographic_region_north_germany_old` |
| `region_south_germany` | `geographic_region_south_germany_old` |
| `region_mexico` | `geographic_region_mexico_old` |
| `region_central_america` | `geographic_region_central_america_old` |
| `region_iberia` | `geographic_region_iberia_old` |
| `region_dixie` | `geographic_region_dixie_old` |
| `region_persia` | `geographic_region_persia_old` |
| `region_arabic` | `geographic_region_arabic_old` |

All objects are defined by Victoria 3 1.13.9 in
`game/common/geographic_regions/06_old_strategic_regions.txt`. In particular,
`geographic_region_central_america_old` is intentional: the current
`region_central_america` has a broader footprint and would change the old
Mexico/Central America checks.

Static references patched by file:

| File | References |
| --- | ---: |
| `common/dynamic_country_names/00_dynamic_country_names.txt` | 10 |
| `common/journal_entries/01_natural_borders_of_france.txt` | 18 |
| `common/journal_entries/02_south_america_migration.txt` | 8 |
| `common/journal_entries/06_cuba.txt` | 1 |
| `common/journal_entries/07_american_mod_jes.txt` | 2 |
| `common/scripted_buttons/00_new_colonial_admins.txt` | 42 |

The per-reference evidence and decisions are recorded in
`LOG_CLEANUP_11_PATCH_MATRIX.csv`.

## B02 — Landowners

`LANDOWNERS_PARENT_API_FIX_SAFE = YES`

Only the argument at
`common/interest_groups/00_landowners.txt:459` changed:

`law_homesteading` → `law_peasant_proprietorship`

`law_homesteading` is a variant of that parent, and the Victoria 3 1.13.9
homologue passes the parent to `has_law_or_variant`. No adjacent farmer,
owner, or interest-group logic changed.

- `LOG8_REGRESSION = NO`
- `B02_ERRORS_BEFORE = 1`
- `B02_ERRORS_PATCHED = 1` (runtime confirmed)
- `LANDOWNERS_STATIC_INVALID_REFERENCES_AFTER = 0`

## Counters after the addendum

The original LOG-CLEANUP-10 audit pool remains 121 diagnostics, but the
addendum reclassifies 113 as deferred design debt:

- `TOTAL_AUDITED_FORK_DIAGNOSTICS_BEFORE = 121`
- `KNOWN_FORK_ERRORS_OPERATIONAL_BEFORE = 8`
- `KNOWN_FORK_DESIGN_DEBT_DEFERRED = 113`
- `TOTAL_ERRORS_PATCHED = 8`
- `KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 0`
- `KNOWN_FORK_DESIGN_DEBT_DEFERRED = 113`

Batch counters:

- `B03_ERRORS_BEFORE = 105`
- `B03_ERRORS_PATCHED = 0`
- `B03_ERRORS_DEFERRED = 105`
- `COUNTRY_LAW_TECH_MIGRATION_SAFE = DEFERRED_DESIGN_DEPENDENCY`
- `B04_ERRORS_BEFORE = 7`
- `B04_ERRORS_PATCHED = 0`
- `B04_ERRORS_DEFERRED = 7`
- `VARIANT_VISIBILITY_MIGRATION_SAFE = DEFERRED_DESIGN_DEPENDENCY`
- `B05_ERRORS_BEFORE = 1`
- `B05_ERRORS_PATCHED = 0`
- `B05_ERRORS_DEFERRED = 1`
- `BAVARIA_LAW_SET_DECISION_SAFE = DEFERRED_DESIGN_DEPENDENCY`

This avoids the misleading original arithmetic `121 - 8 = 113` as an
operational-error result. The 113 remainder is design debt, not a current
cleanup blocker.

## Changed gameplay files

`GAMEPLAY_CHANGED_FILES = 7`

`GAMEPLAY_CHANGED_HUNKS = 67` Git diff hunks, containing 82 semantic
replacement points (81 geography and one parent-law argument).

| File | SHA-256 before | SHA-256 after |
| --- | --- | --- |
| `common/dynamic_country_names/00_dynamic_country_names.txt` | `788B02DEF9C6E16125DC33024E701B0BAB14B4B00569E36ABB050944028DD7C4` | `3E862EBDB9FE3FE59EB043F634701B0027D96A2CFF3E3FBA7FFEA40150445EA6` |
| `common/journal_entries/01_natural_borders_of_france.txt` | `EA2E2C86BFB8DC7E887E3522193A8AE316F80C8F4329AA31384CBFB03AC60985` | `BA92EA2A367E8C0C5AC8BAA9AA81BFAAB0AB94722F5A91BE06DDF1D6925D4FEA` |
| `common/journal_entries/02_south_america_migration.txt` | `27D8ABA5F6EACC63CA945E23D15BC7DB90BDFBBD793FF6592CDCBBEA3BDF3EF5` | `9FB17A5A0F2D3AD771B0DE73851110BCF9104A397C3E3CC5A315714541D885E4` |
| `common/journal_entries/06_cuba.txt` | `B928FFEA1898F5E2E0C3B920C715921C85D30A7DC559BA356A374CDDE1574E3D` | `A07D5D82853D57B7BDCC6BB10DEAE3864925DA4AFFBB2DB9B1C47B1B48CF8598` |
| `common/journal_entries/07_american_mod_jes.txt` | `46847DFD2E296CA34DBD7E2811992A5DEC64EB415B50E6E842C45C8AB678C1DB` | `B254DCEFEE543B9688262DFB305DA76C55B0A5718C433AEE4BF0C43505F18D13` |
| `common/scripted_buttons/00_new_colonial_admins.txt` | `3574AE93E49D777788D0C311D19848A6EF8A98C312D36D74A237A65BDB16712B` | `A85A4A35C91444BEB70B9A04E7927212BC184057BB558B32AED3D799F3E64B6F` |
| `common/interest_groups/00_landowners.txt` | `E0A4473DC85842382CC0F34088EDE4C07575BBF96BB87E78E68E3189FFE29B5C` | `E92E2A31A80DED85505A526B9825B8E633617BAB6252F0B7167E283ED9E33F2B` |

## Protected systems and static result

- `COUNTRY_STARTING_TECH_ASSIGNMENTS_CHANGED = 0`
- `TECH_TREE_DEFINITION_FILES_CHANGED = 0`
- `TECH_TREE_FILES_CHANGED = 0`
- `COUNTRY_HISTORY_LAW_FILES_CHANGED = 0`
- `LAW_DEFINITION_OR_VARIANT_FILES_CHANGED = 0`
- `BAVARIA_LAW_SET_CHANGED = 0`
- `NEW_ATTRIBUTABLE_DIAGNOSTICS_STATIC = 0`
- `DOCUMENTATION_FILES_CREATED = 4`

No closed diagnostic site from LOG-CLEANUP-2 through LOG-CLEANUP-9 was changed
or reintroduced by this diff; the targeted legacy keys remain absent from
their previously corrected roots. The Iraq–Persia diplomatic play, upstream
reference, tech tree, military formations, characters, portraits/DNA, ADMIN,
and protected company systems were not changed.

## Human runtime result

The human runtime was completed with Victoria 3 `release/1.13.9`, hash
`afea32b87`, using only the local `1776_Age_of_Revolutions_fork` mod. A new
1776 game was played as the Netherlands through 14 January. The game did not
crash, no raw localization key was observed, and shutdown was performed
normally from inside the game. Fresh debug, error, system and game log
rotations were retained and checked.

- `B01_AFTER = 0`
- `B02_AFTER = 0`
- `NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_PATCH = 0`
- `COUNTRY_LAW_DIAGNOSTICS_OBSERVED = 113`
- `COUNTRY_LAW_CLASSIFICATION = KNOWN_FORK_DESIGN_DEBT_DEFERRED`
- `KNOWN_FORK_DESIGN_DEBT_DEFERRED = 113`
- `KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 0`
- `LOG_CLEANUP_11 = PASS`

The eight operational blockers targeted by LOG-CLEANUP-11 are therefore
closed. The 113 country-law diagnostics remain known design debt and do not
alter this PASS.

## Newly exposed residual outside LOG-CLEANUP-11

Removing the Natural Borders log loop allowed the same fresh rotations to
expose a substantially wider legacy geographic family that pre-existed this
patch. It is not a LOG-CLEANUP-11 regression and was not corrected during
finalization.

Seven Script System identities materialized as
`Invalid right side during comparison 'sr'`:

| Script identity | Occurrences |
| --- | ---: |
| `common/journal_entries/00_major_railroads.txt:12` | 1048 |
| `common/journal_entries/00_major_railroads.txt:13` | 1048 |
| `common/journal_entries/07_hindustan_is_durrani_mod.txt:15` | 13 |
| `common/journal_entries/07_hindustan_is_durrani_mod.txt:41` | 13 |
| `common/journal_entries/07_hindustan_is_durrani_mod.txt:42` | 13 |
| `common/journal_entries/07_hindustan_is_durrani_mod.txt:43` | 13 |
| `common/journal_entries/03_afghanistan.txt:1834` | 1 |

- `NEW_RUNTIME_SR_SCRIPT_IDENTITIES = 7`
- `NEW_RUNTIME_SR_OCCURRENCES = 2149`

The parallel eventtargetlinks pass found:

- `LEGACY_REGION_EVENTTARGET_PHYSICAL_REFERENCES = 207`
- `LEGACY_REGION_EVENTTARGET_FILES = 39`

The seven runtime identities are included in those 207 physical references.
They must not be added to produce 214 errors. The family includes legacy keys
such as `region_persia`, `region_south_germany`, `region_danubia`,
`region_poland`, `region_manchuria`, `region_central_india`, `region_punjab`,
`region_rhine`, `region_north_germany`, `region_east_siberia`, `region_dixie`,
`region_congo`, `region_niger`, `region_west_siberia`, `region_zanj` and
`region_senegal`.

The same runtime also exposed 29 anomalies not yet attributed as confirmed
fork errors:

- `INVALID_NON_REGION_DATABASE_OBJECT_REFERENCES = 27`
- `OTHER_EVENTTARGET_SCOPE_FAILURES = 2`
- `PENDING_ATTRIBUTION_NON_REGION_OR_SCOPE = 29`

These items are recorded for the next phase without classification or gameplay
change.

## Roadmap

- `NEXT_PHASE = LOG-CLEANUP-12-GLOBAL-LEGACY-REGION-EVENTTARGET-CLOSURE`
- following correction and runtime: `LOG-CLEANUP-13-FINAL-GLOBAL-REINDEX-QA`
- `ESTIMATED_PHASES_REMAINING_MIN = 2`
- `ESTIMATED_PHASES_REMAINING_LIKELY = 2`
- `ESTIMATED_PHASES_REMAINING_MAX = 3`
