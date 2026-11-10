# Issue #27 — first bounded journal-outcome migration

Date: 2026-11-06. Coordination #19; baseline #20; workstream #24; migration #27.
Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. This batch is ready for code review, not Done.
Issue #36's local crash acceptance is retained; its investigation was not reopened.

## Scope and sources

Exactly the six gameplay files named in #27, containing eight journal definitions, are migrated.
The candidate is based on remote `hotfix/1.15` commit `a6bd353d9195c0a17afd095dccb5fe305f844f84`.
Each source matches the current dirty working mod after normalizing Git line endings. Candidate
preparation is separate from that working mod; no local checkout, reset, map change or main merge is involved.

The installed game identifies itself as `release/1.15.0`, revision
`6338547985dbc271523e149f362a6fd93dc62975` in `code_revisions.log`.
Canonical game data was consulted read-only in `C:/Games/Victoria 3/game`.

Authoritative references:

- [Official developer announcements, Dev Diary #194, Journal Entry Outcomes](https://steamcommunity.com/app/529340/announcements): the new outcomes system replaces the legacy conclusion mechanism.
- Installed `common/journal_entries/journal_entries.md:134–197`: outcome fields, country-context scopes, hidden invalidation and timeout flags.
- Installed `common/journal_entries/00_urbanization.txt:28–51`: standard completion header, conclusion text, predicate and effect.
- Installed `common/journal_entries/00_acw_entries.txt:36–62`: visible failure presentation without extra outcome flags.
- Installed `common/journal_entries/00_canals.txt:34–57`: hidden invalidation with cleanup effect.
- Installed `common/journal_entries/00_sick_man.txt:14–40`: distinct completion and timeout outcomes. This batch has no JE-level timeout to convert.
- Installed `localization/english/journal_entries_l_english.yml:57–62` and French equivalent `:48–53`: all six reused standard localization keys exist. The working mod does not mask these base files or redefine the six keys. No new player prose or localization files are introduced.

## Explicit conclusion mapping

All predicates and effect bodies are preserved token-for-token, including nested scopes and effect order.
Non-conclusion fields retain their tokens and order: activation conditions, immediate effects, weekly/monthly
pulses, modifiers, buttons, widgets, progress values, inheritance/transfer flags, weights and pinning.

| File under `common/journal_entries/` | Journal | Old fields/lines | New outcome lines, in declaration order | Preserved behavior |
| --- | --- | --- | --- | --- |
| `1776_usa_french_support.txt` | `je_aor1776_french_support` | complete 15; on_complete 17 | 15: complete | `us_revolt` conclusion; stop-support effect; weekly support pulse unchanged. |
| `1776_usa_revolutionary_spirit.txt` | `je_aor1776_revolutionary_spirit` | complete 7; on_complete 8 | 7: complete | `us_revolt` conclusion; finish-content cleanup; initialization/refresh unchanged. |
| `1776_ottoman_reforms.txt` | `je_1776_porte_burden` | complete 19; on_complete 32; on_invalid 41 | 19: complete; 47: dormant invalidation | Twelve administrative months and all ten goals; completion variable, relief cleanup and event `.1`; dormant invalidation cleanup retained. |
| `1776_ottoman_reforms.txt` | `je_1776_many_masters` | complete 76; on_complete 81; fail 85; on_fail 96; invalid 101 | 92: complete; 107: fail; 129: invalid | Thirty-six stability points before 1836; failure deadline or 120 crisis points with current severe pressure; `.3` event still delayed one day; silent Sick Man supersession. |
| `1776_imperial_centralization.txt` | `je_aor1776_hre_centralization` | invalid 5; complete 6 | 5: invalid; 13: complete | Loss of emperor status; global unification flag; no invented reward; cooldown, popup and reform buttons unchanged. |
| `1776_imperial_situation.txt` | `je_aor1776_hre_situation` | invalid 6; complete 7 | 6: invalid; 14: complete | Leaving imperial membership silently invalidates; completion remains `always = no`; widget and all voting buttons unchanged. |
| `1776_imperial_situation.txt` | `je_aor1776_hre_vote` | complete 116; invalid 117 | 132: complete; 142: invalid | Election closure concludes; loss of elector status invalidates; no invented effects. |
| `10_1776_birth_quota_trial.txt` | `je_birth_quota_trial` | complete 12; fail 17; on_complete 25; on_fail 37 | 12: complete; 35: fail | Progress >=200 succeeds; repeal or progress <=0 fails; interest-group/ideology/demography effects, conditional law rollback and both events unchanged. |

Completion outcomes use the native gold completion presentation; failures use native blue failure presentation.
The five invalidation outcomes use `flags = { hidden invalid_outcome }`, as documented. Empty handlers become
empty effect blocks, rather than invented rewards. No historical flag or new objective/subgoal relationship is added.

### Dormant Ottoman cleanup

The administrative journal originally declared `on_invalid = { ottoman_1776_remove_relief = yes }` but no
`invalid` predicate. Legacy documentation states that an absent invalidation trigger cannot automatically
invalidate the entry. Its cleanup is therefore retained in a hidden invalid outcome with `trigger = { always = no }`.
Inventing a country, date, law or eligibility test here would change gameplay. Forced external removal and
country destruction are separate engine behaviors that still need runtime verification; token preservation does
not certify those callbacks. No additional invalidation condition has been asserted as historically intended.

### Competing conclusions and timing

The original relative declaration order of predicates is retained, including invalidation-before-completion in
centralization and the permanent imperial situation. No guards are inserted and no conditions are reordered
inside a predicate. The old/new engine's precedence when two predicates are simultaneously true has not been
independently measured: preserve this as a review/runtime gate rather than claiming behavioral proof.
The 1836 Ottoman deadline remains a failure predicate; converting it to a day-count timeout would change its meaning.

## Static validation

Command, using the six original files exported from the recorded parent as `BEFORE`:

```text
python tools/compatibility/issue27_journal_outcomes_audit.py --mod-root CANDIDATE --baseline-root BEFORE --vanilla-root "C:/Games/Victoria 3/game" --inventory-root ORIGINAL_MOD
```

Actual results:

- **6 files, 8 journal definitions, 22 legacy fields replaced by 15 outcomes; zero legacy conclusion fields left in this batch.**
- All 14 original predicates are unchanged; the fifteenth outcome is the explicitly dormant orphan handler.
- Every original completion/failure/invalidation handler is retained, with unchanged nested scopes and effect order.
- All non-conclusion fields compare equal as ordered token streams. No JE-level timeout was added or removed.
- All six standard text keys resolve in English and French from the unmasked canonical base files.
- The baseline is rejected for all eight journals; the candidate reports **PASS_STATIC_ONLY**, zero audit errors.
- Eight negative controls are detected: changed threshold, lost cleanup, changed journal-entry scope, changed pulse
  frequency, visible invalidation, swapped competing conclusions, unbalanced braces, and reintroduced legacy fields.
- Original source files were reread after candidate generation and still match the recorded inputs; the dirty
  working mod was not patched or replaced. Remote publication is a scoped commit on `hotfix/1.15` with a head lease.

The audit is read-only. It checks field structure, semantics-preserving token movement and required metadata;
it does **not** run the Paradox parser, execute triggers/effects, certify GUI layout or simulate a game.
The adjacent validation JSON records input/output hashes, the mapping and negative-control results.

## Remaining journal errors and recommended next batch

A fresh, depth-aware inventory finds **1,451 direct legacy fields in 171 other journal files**. This is an
inventory of fields, not 1,451 distinct bugs or 171 confirmed active entries. It uses a different definition
from the earlier lexical 1,395/175 inventory; no growth/regression trend should be inferred.

Priorities after this batch's review and runtime test:

1. `common/journal_entries/00_sick_man.txt` (26 legacy fields): it is the Ottoman failure continuation reached
   from this batch. Migrate it as a separately reviewed dependency batch before certifying that entire path.
2. `00_suffragists.txt` (3 legacy fields) and `00_urbanization.txt` (4): parser failures are already captured in #20.
   Urbanization also has independent invalid-pop-type scopes; changing outcome wrappers alone does not fix those.
3. American initialization: the preserved mod log reports unset `aor1776_fervour` at
   `common/scripted_effects/1776_usa_content_r1.txt:10`, called by the revolutionary-spirit journal's original
   `immediate` at line 6. The initializer is unchanged here; verify ordering in a new USA game before proposing a targeted fix.
4. Imperial duplicate `add_journal_entry` messages remain initialization debt. This batch does not rewrite on-actions
   or substitute new activation logic merely to silence them.

No post-migration runtime log has been captured. Removed source fields predict removal of their specific legacy
parser complaints; actual error reduction and any new engine errors must be measured on the published candidate.
Raw baseline logs stay private. The northern Scandinavia symptom #37 is independently Ready under parent #24;
its geographic cause remains unconfirmed and no map file was modified.

## Required in-game acceptance

Use a fresh 1776 game with an isolated installation of the reviewed revision, the same build/DLC settings and
all unrelated mods disabled. Record content load, exact revision/dirty manifest, speed/debug state and final date.

| Test | Required observation | Status |
| --- | --- | --- |
| USA support and commitment | Entries activate once; `us_revolt` concludes both; support/fervour cleanup and pulse cessation occur once. | Not run |
| Ottoman administration | All ten goals plus 12 months complete; relief/active modifiers disappear correctly; `.1` fires once. Explicit external-removal check for dormant cleanup. | Not run |
| Ottoman politics | Success, prolonged-crisis failure, 1836 deadline and Sick Man supersession; `.3` delayed by one day; no duplicate continuation. | Not run; continuation journal still legacy |
| Imperial centralization | Unification and loss-of-emperor paths, including both true on one evaluation; cooldown/buttons unchanged. | Not run |
| Imperial situation/vote | Permanent entry never completes; leaving membership/losing elector status invalidates silently; election closure concludes; competing triggers tested. | Not run |
| Birth-quota trial | Success >=200, failure <=0 and law-repeal failure; rollback/event only while the law still exists; simultaneous conditions. | Not run |
| Persistence and logs | Save/reload active and concluded entries, advance again, confirm no duplicate effects; compare all rotated logs against #20. | Not run |

Human acceptance of these journal paths is still required. Existing player prose is preserved; any later immersive
editorial pass follows human validation of the migrated behavior. #27 must not be marked Done from this static audit.
