# LOG-CLEANUP-12 — Global legacy region and eventtarget closure

Status: `PASS`

Branch: `post-2.3.0-log-cleanup`

Baseline commit: `09990afc05da7af68c44436ecb9613753d459c3b`

Target: Victoria 3 `release/1.13.9`, hash `afea32b87`

## Baseline and runtime source

LOG-CLEANUP-11 passed its human runtime with B01 and B02 at zero and no
attributable regression. Its 113 country-law diagnostics remain strictly
`KNOWN_FORK_DESIGN_DEBT_DEFERRED` and were not modified.

Only the fresh Netherlands session played through 14 January was used. Its
current-session eventtarget pass is in `error.1.log` at 18:43:47 and contains
exactly:

- 207 invalid legacy-region database links;
- 27 invalid non-region database links;
- 2 other eventtarget scope failures.

The seven Script System `Invalid right side during comparison 'sr'` identities
are included in the 207 region rows. Their 2,149 occurrences are runtime
frequency, not additional identities.

The original 214 corrections then passed a fresh human runtime on Victoria 3
`release/1.13.9`, hash `afea32b87`, using only the local fork and a new
Netherlands 1776 game through 20 January (session approximately 19:42:27 to
19:49:06). There was no crash, no raw localization key, and shutdown was
normal. The original region, technical-key, and scope targets all reached zero,
with no attributable diagnostic from that patch.

That runtime exposed 23 pre-existing operational errors outside the original
matrix: 22 removed strategic-region arguments in
`has_interest_marker_in_region` and one Brazil parent/variant API error.
Because these belong to LOG-CLEANUP-12's technical families, they are patched
as a runtime extension. The targeted human retest subsequently passed.

The final extension retest used Victoria 3 `release/1.13.9`, hash
`afea32b87`, continued the Netherlands game through 21 January 1776, and
ended with `Quit: Quit from inside game` followed by
`Transition Game->Empty`. No visual problem or crash was reported.

## Preflight

- `BRANCH = post-2.3.0-log-cleanup`
- `HEAD = 09990afc05da7af68c44436ecb9613753d459c3b`
- `WORKTREE_BEFORE = CLEAN`
- `INDEX_BEFORE = EMPTY`
- `LOG_CLEANUP_11_COMMITTED = YES`

No stash, reset, checkout, add, commit or push was performed.

## Family A — legacy regions

- `GLOBAL_REGION_MIGRATION_SAFE = YES`
- `LEGACY_REGION_RUNTIME_REFERENCES_ORIGINAL = 207`
- `LEGACY_INTEREST_MARKER_RUNTIME_EXTENSION = 22`
- `REGION_REFERENCE_MATRIX_ROWS = 229`
- `REGION_REFERENCES_ATTRIBUTED = 229`
- `REGION_FORK_FIXABLE = 229`
- `REGION_DEFERRED = 0`
- `REGION_NONACTIONABLE = 0`
- `REGION_UNKNOWN = 0`

The static sweep built the set of removed strategic-region keys by subtracting
the current 1.13.9 strategic-region definitions from the keys represented by
`common/geographic_regions/06_old_strategic_regions.txt`. It found 207 active
fork references plus one commented reference. The 207 active references match
the runtime matrix completely:

- `LEGACY_REGION_ADDITIONAL_STATIC_REFERENCES = 0`
- `LEGACY_REGION_TOTAL_PROVEN_REFERENCES = 229`
- `LEGACY_REMOVED_STRATEGIC_REGION_ACTIVE_REFERENCES_AFTER = 0`

### Typed migrations

The 207 rows were not migrated by a blind text rule:

- 167 direct state/capital comparisons use
  `is_in_geographic_region = geographic_region_*_old`;
- 6 `capital.region` comparisons use an explicit capital-state scope and the
  exact old geographic footprint;
- 1 Paris Commune state-region comparison was rewritten onto
  `building.state` with `geographic_region_france_old`;
- 5 `random_state_region` comparisons retain the strategic-region API and use
  current `west_africa`, `east_africa`, or `equatorial_africa` objects;
- 11 original interest-marker triggers and 22 runtime-extension triggers use
  current strategic regions;
- 17 legacy strategic-region scope blocks use exact vanilla current scopes,
  generated geographic iterators, or removal where the saved scope was proven
  unused and the vanilla homologue had already removed it.

Interest-marker mappings:

| Legacy | Current strategic region |
| --- | --- |
| Senegal, Niger | `sr:region_west_africa` |
| Ethiopia, Zanj | `sr:region_east_africa` |
| Congo | `sr:region_equatorial_africa` |
| Persia | `sr:region_greater_persia` |
| Dixie | `sr:region_atlantic_coast` |
| Arabic | `sr:region_arabia` |
| Italy | `sr:region_southern_europe` |
| Manchuria | `sr:region_northeast_asia` |

Important structural homologues include Siberia/Northeast Asia in
`events/major_railways.txt`, Balkans in the Austrian federation events, Near
East in the Balkan wars, current African strategic regions in the Spanish
Africa event, and geographic iterators for Caucasus, Persia and Poland. The
row-level evidence is in `LOG_CLEANUP_12_REGION_MATRIX.csv`.

### Seven runtime identities

All seven are present once in the 207-row matrix and patched:

| Path | Previous occurrences |
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

### Runtime extension: interest-marker API

The global extension sweep tested every
`has_interest_marker_in_region` argument against the 41 removed keys obtained
from the same 51-old-key minus 142-current-key strategic-region set. It found
exactly the 22 runtime rows and no latent additional reference:

- 17 × `region_persia` → `sr:region_greater_persia`;
- 2 × `region_arabic` → `sr:region_arabia`;
- 1 × `region_dixie` → `sr:region_atlantic_coast`;
- 1 × `region_italy` → `sr:region_southern_europe`;
- 1 × `region_manchuria` → `sr:region_northeast_asia`.

The Italy and Manchuria choices are exact vanilla 1.13.9 homologues in,
respectively, `events/italian_unification.txt:895` and
`common/on_actions/00_code_on_actions.txt:5373`. The API itself was retained;
only each invalid strategic-region argument changed.

- `LEGACY_INTEREST_MARKER_REGION_ERRORS = 22`
- `LEGACY_INTEREST_MARKER_ADDITIONAL_STATIC_REFERENCES = 0`
- `LEGACY_INTEREST_MARKER_ERRORS_PATCHED = 22`
- `LEGACY_INTEREST_MARKER_REMOVED_KEYS_AFTER = 0`

## Family B — non-region database objects

- `NON_REGION_MATRIX_ROWS = 28`
- `NON_REGION_REFERENCES_ATTRIBUTED = 28`
- `NON_REGION_FORK_FIXABLE = 6`
- `NON_REGION_DEFERRED = 18`
- `NON_REGION_NONACTIONABLE = 4`
- `NON_REGION_UNKNOWN = 0`

Five exact technical key migrations were applied:

- 3 × `law_per_capita_taxation` → `law_per_capita_based_taxation`;
- 1 × `law_charity_hospitals` → `law_charitable_health_system`;
- 1 × `law_tenent_farmers` → `law_tenant_farmers`.

The runtime extension adds one independently counted technical API correction
in `events/brazil/misc_events.txt:116`:
`has_law_or_variant = law_type:law_homesteading` now supplies its proven
parent, `law_type:law_peasant_proprietorship`. No other law in the block was
changed, and this error is not part of the 113 deferred country-law
diagnostics.

- `BRAZIL_PARENT_API_ERROR = 1`
- `BRAZIL_PARENT_API_ERROR_PATCHED = 1`

Eighteen runtime rows for `law_type:state_religion` are deferred. They resolve
to 17 unique case-insensitive physical country-history files because the log
reports the Paraguay path twice with different casing. Correcting those
starting-law assignments is explicitly deferred to `LAW-SYSTEM-1776`:

- `OTHER_DESIGN_DEBT_DEFERRED_LOG_ROWS = 18`
- `OTHER_DESIGN_DEBT_DEFERRED_UNIQUE_PHYSICAL = 17`

Four references to `amendment_frugal_ordinance` remain
`ALREADY_ACCOUNTED_FOR`. Vanilla defines the amendment, but the fork's Japan
override omits it. The canonical hotfix audit already classifies this as a
Japan-protected diagnostic, so LOG-CLEANUP-12 did not import a definition or
alter Japanese gameplay.

The fresh log also prints `je_meiji_imperial_marriage` Script System
diagnostics outside the canonical 27 eventtarget rows. The prior global hotfix
inventory already classifies them as `ALREADY_ACCOUNTED_FOR` in the protected
Japan system. They are recorded here but excluded from the fixed 236-entry
eventtarget pool and receive no LOG-CLEANUP-12 patch.

## Family C — scope failures

- `SCOPE_MATRIX_ROWS = 2`
- `SCOPE_FAILURES_ATTRIBUTED = 2`
- `SCOPE_FAILURES_FORK_FIXABLE = 2`
- `SCOPE_FAILURES_DEFERRED = 0`
- `SCOPE_FAILURES_NONACTIONABLE = 0`
- `SCOPE_FAILURES_UNKNOWN = 0`

Corrections:

- `ig:ig_devot` → `ig:ig_devout` in the Iranian troubles event;
- removal of only the dead DWI diplomatic pact. `DWI` has no country
  definition in vanilla 1.13.9, the current fork, or the initial fork import.
  The adjacent Dutch East Indies relationship remains unchanged.

The two scope rows are recorded in `LOG_CLEANUP_12_NON_REGION_MATRIX.csv` with
the `EVENTTARGET_SCOPE_FAILURE` family. With the Brazil extension row, the
same CSV contains 28 non-region/API rows and 2 separately counted scope rows.

## Combined attribution and counters

- `KNOWN_FORK_ERRORS_OPERATIONAL_AT_LOG11_CLOSE = 0`
- `KNOWN_FORK_DESIGN_DEBT_DEFERRED = 113`
- `ORIGINAL_PENDING_REGION_PHYSICAL_REFERENCES = 207`
- `ORIGINAL_PENDING_NON_REGION_OBJECT_REFERENCES = 27`
- `ORIGINAL_PENDING_SCOPE_FAILURES = 2`
- `ORIGINAL_TOTAL_PENDING_PHYSICAL_ANOMALIES = 236`
- `ORIGINAL_NON_REGION_OR_SCOPE_IN_SCOPE = 29`
- `ORIGINAL_NON_REGION_OR_SCOPE_ATTRIBUTED = 29`
- `ORIGINAL_NON_REGION_OR_SCOPE_FORK_FIXABLE = 7`
- `ORIGINAL_NON_REGION_OR_SCOPE_SEMANTIC = 0`
- `ORIGINAL_NON_REGION_OR_SCOPE_NONACTIONABLE = 4`
- `ORIGINAL_NON_REGION_OR_SCOPE_DEFERRED = 18`
- `ORIGINAL_NON_REGION_OR_SCOPE_UNKNOWN = 0`

- `LOG12_ORIGINAL_CONFIRMED_ERRORS_PATCHED = 214`
- `LOG12_EXTENSION_CONFIRMED_ERRORS_PATCHED = 23`
- `LOG12_ORIGINAL_PATCH_RUNTIME = PASS`
- `ORIGINAL_214_RUNTIME_PASS = YES`
- `EXTENSION_23_RUNTIME_PASS = YES`
- `NEW_PREEXISTING_OPERATIONAL_ERRORS_DISCOVERED = 23`
- `LEGACY_INTEREST_MARKER_REGION_ERRORS = 22`
- `BRAZIL_PARENT_API_ERROR = 1`
- `KNOWN_FORK_ERRORS_OPERATIONAL_BEFORE_EXTENSION = 23`
- `LEGACY_INTEREST_MARKER_ERRORS_PATCHED = 22`
- `BRAZIL_PARENT_API_ERROR_PATCHED = 1`
- `TOTAL_EXTENSION_ERRORS_PATCHED = 23`
- `TOTAL_CONFIRMED_ERRORS_PATCHED = 237`
- `NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_EXTENSION = 0`
- `KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 0`
- `OTHER_DESIGN_DEBT_DEFERRED_LOG_ROWS = 18`
- `OTHER_DESIGN_DEBT_DEFERRED_UNIQUE_PHYSICAL = 17`
- `JAPAN_NONACTIONABLE = 4`

The value 214 is derived from 207 region references + 5 fixable non-region
references + 2 scope failures. It is never calculated as 207 + the seven
Script System identities.

The extension value 23 is derived independently from 22 interest-marker
arguments + 1 Brazil parent API error. The 18 deferred law rows, 4 protected
Japan rows, and 113 deferred country-law diagnostics are not counted as fixed.

## Dynamic gameplay allowlist

`GAMEPLAY_ALLOWLIST_FILES = 48`

Every file below has a runtime-matrix row and at least one proven patch:

```text
common/dynamic_country_names/00_dynamic_country_names.txt
common/flag_definitions/00_flag_definitions.txt
common/history/diplomacy/00_subject_relationships.txt
common/journal_entries/00_establish_colonial_administration.txt
common/journal_entries/00_major_railroads.txt
common/journal_entries/00_player_objectives_great_game.txt
common/journal_entries/00_poland.txt
common/journal_entries/00_reunify_china.txt
common/journal_entries/03_afghanistan.txt
common/journal_entries/03_russia.txt
common/journal_entries/05_balkan_wars.txt
common/journal_entries/05_danubian_federation.txt
common/journal_entries/05_the_grand_collapse.txt
common/journal_entries/06_economic_regeneration.txt
common/journal_entries/06_new_imperialism.txt
common/journal_entries/06_spanish_africa.txt
common/journal_entries/07_american_mod_jes.txt
common/journal_entries/07_hindustan_is_durrani_mod.txt
common/on_actions/00_code_on_actions.txt
common/scripted_buttons/00_new_colonial_admins.txt
common/scripted_buttons/00_scripted_buttons_modSX.txt
common/scripted_progress_bars/01_mod76_progress_bars.txt
events/agitators_events/historic_agitator_events.txt
events/agitators_events/natural_borders.txt
events/agitators_events/paris_commune_events.txt
events/balkans_events/austria_federalism.txt
events/balkans_events/balkan_wars_events.txt
events/balkans_events/eastern_question.txt
events/brazil/brazilian_slavery.txt
events/brazil/misc_events.txt
events/brazil/south_america_migration.txt
events/dei_breakup.txt
events/egyptian_crisis_events.txt
events/french_revolution_mod_events.txt
events/iberia_events/cuba_events.txt
events/iberia_events/dominican_events.txt
events/iberia_events/spanish_africa_events.txt
events/iberia_events/spanish_new_world_events.txt
events/india_events/sepoy_mutiny_events.txt
events/iran_troubles_events_mod.txt
events/italian_unification.txt
events/krakatoa_events.txt
events/major_railways.txt
events/manifest_destiny_events.txt
events/misc_unifications.txt
events/new_imperialism_events_mod.txt
events/oscar_wilde.txt
events/soi_events/00_ep1_persia_events.txt
```

- `GAMEPLAY_CHANGED_FILES = 48`
- `GAMEPLAY_CHANGED_HUNKS = 186`
- `TECH_TREE_FILES_CHANGED = 0`
- `COUNTRY_LAW_FILES_CHANGED = 0`
- `MAP_DATA_FILES_CHANGED = 0`
- `MILITARY_OR_NAVAL_FORMATION_FILES_CHANGED = 0`

## Static validation

- all 229 region-matrix rows attributed, safe, and patched;
- all seven runtime identities present exactly once in the region matrix;
- all 28 non-region/API rows and both scope rows attributed;
- active references to removed `sr:region_*` objects: 207 → 0;
- active removed strategic-region arguments in
  `has_interest_marker_in_region`: 22 → 0;
- additional active static references: 0;
- all introduced geographic regions exist in Victoria 3 1.13.9;
- all introduced current strategic regions exist in Victoria 3 1.13.9;
- all introduced law and interest-group keys exist;
- braces balanced in all 48 changed gameplay files;
- `git diff --check = PASS`;
- index remains empty;
- `NEW_ATTRIBUTABLE_DIAGNOSTICS_STATIC = 0`.

## Final runtime validation

Victoria 3 was not launched by Codex. Human runtime validated both the original
214 corrections and the 23-error extension:

- `LEGACY_INTEREST_MARKER_REGION_ERRORS_AFTER = 0`;
- `LEGACY_INTEREST_MARKER_REGION_IDENTITIES_AFTER = 0`;
- `BRAZIL_PARENT_API_ERROR_AFTER = 0`;
- `NEW_RUNTIME_SR_SCRIPT_IDENTITIES_AFTER = 0`;
- `LEGACY_REGION_EVENTTARGET_PHYSICAL_REFERENCES_AFTER = 0`;
- no `Invalid strategic region`;
- no `Invalid right side during comparison 'sr'`;
- no `Given law is a variant, we expect the parent`;
- `NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_EXTENSION = 0`;
- `KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 0`.

The loader reproduced exactly the canonical residuals: 18
`state_religion` rows across 17 unique physical files, 4 protected-Japan
`amendment_frugal_ordinance` rows, and 113 deferred country-law diagnostics.
Their existing classifications remain unchanged.

- `LOG_CLEANUP_12 = PASS`
- `ORIGINAL_214_RUNTIME_PASS = YES`
- `EXTENSION_23_RUNTIME_PASS = YES`
- `TOTAL_CONFIRMED_ERRORS_PATCHED = 237`
- `RUNTIME_HUMAN_REQUIRED = NO`
- `NEXT_PHASE = LOG-CLEANUP-13-FINAL-GLOBAL-REINDEX-QA`
- `ESTIMATED_PHASES_REMAINING_MIN = 1`
- `ESTIMATED_PHASES_REMAINING_LIKELY = 1`
- `ESTIMATED_PHASES_REMAINING_MAX = 1`
