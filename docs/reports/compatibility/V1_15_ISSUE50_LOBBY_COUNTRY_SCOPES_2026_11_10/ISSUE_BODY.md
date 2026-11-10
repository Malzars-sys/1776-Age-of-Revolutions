## Delivery — 2026-11-10

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Requested Project status: In review. Issue remains open pending the targeted engine check.**

The observed Acre lobby error is corrected locally. **Only one runtime file changed**: `common/journal_entries/02_acre_dispute.txt`, inside `je_acre_dispute.is_shown_in_lobby`.

```diff
- c:BOL = THIS
+ exists = c:BOL
+ c:BOL ?= THIS
```

The Colossus of the South requirement is preserved. Bolivia must exist before this positive country-identity gate can be true; the optional comparison avoids requiring an unset scope. Matching/nonmatching existing-country behavior is preserved.

### Evidence and limits

- Captured six repeated unset-scope / invalid-comparison messages at the original Acre lobby line from the current player log. Snapshot only: no game launch, log clearing or post-fix engine result.
- Inventoried 494 effective journals and 22 strict country comparisons in lobby blocks. The two targets without unconditional initial province declarations are BOL and TIS; TIS already sits in an existence-guarded branch and is retained. Other countries, negative comparisons, optional comparisons and non-lobby contexts remain untouched.
- **13/13 installed contract checks, 6/6 context cases, 6/6 deliberate-regression controls passed.** Cases cover absent/matching/other country with DLC off/on, conservatively checking both possible defaults of an absent optional comparison. These fixtures are not an engine interpreter.
- Existing journal reference/metadata audit: **494 entries, zero findings** in its checked vocabulary.
- **2,533 existing inputs captured; the Acre file is the only changed input; 2,532 unchanged at the protection capture.** No new runtime file. Exact 19-byte addition, reversible to the original; every byte outside the lobby block, including all migrated outcomes, remains unchanged. No Git or vanilla write.
- Native syntax witness is the existence/optional-comparison pair in the French natural-borders journal's `is_shown_when_inactive` field. It establishes the country-trigger pattern, not tested lobby behavior.
- #27/#39 outcomes and the other agent's #48 ports / #49 Japan content are preserved. This does not reactivate Acre, create Bolivia, change geography, laws, technology, history, rewards or localization.
- Other fresh diplomacy, Morocco and naval-connection diagnostics remain separate; no global clean-log claim.

Local evidence (not committed/pushed): `docs/reports/compatibility/V1_15_ISSUE50_LOBBY_COUNTRY_SCOPES_2026_11_10/` — `REPORT.md`, `RUNTIME_PROTOCOL.md`, `CONTRACT.json`, candidate/live checks, log snapshot/extraction, lobby inventory, native witness, journal-reference check and source protection.

Read-only verifier: `tools/compatibility/issue50_lobby_country_scope_audit.py`. An initial unsupported negative-fixture exception was corrected before installation and documented; final evidence is `CANDIDATE_VALIDATION_R2.json` and `LIVE_VALIDATION.json`.

Next engine check: fresh 1776 country-selection/journal previews, new error-log lines, a short simulation and save/reload; DLC-off and an existing-Bolivia positive case only where available. The previous grouped acceptance does not cover this new fix.

- [x] Snapshot observed diagnostics, effective providers, initial-presence model and source hashes.
- [x] Install the single justified lobby guard; preserve exact non-lobby bytes.
- [x] Run static checks/controls and prepare a grouped engine protocol.
- [ ] Human runtime acceptance of this new fix.

<details>
<summary>Original assignment — retained</summary>

## Assignment — Hawk, 2026-11-10

Parent workstream: #24; journal preservation witness: #39. Claimed at the maintainer's request “Prends une autre mission.” Requested Project status: In progress.

Qualify and fix strict country-scope comparisons in journal `is_shown_in_lobby` blocks where countries can be absent in the 1776 scenario. The fresh log contains `c` unset-scope/invalid-left-side errors at `common/journal_entries/02_acre_dispute.txt:8` (Bolivia).

Scope: inventory effective lobby blocks and startup presence; select demonstrated positive country-identity cases, preserve DLC/other predicates and every byte outside narrowly authorized spans. Use canonical 1.15 existence-guard/optional-comparison patterns. No blanket `?=` conversion, manufactured country, geography, initial history, journal outcome, activation or reward change. Model absent/matching/nonmatching cases; static modeling does not constitute engine testing.

Preserve #27/#39 migrated outcomes and all accepted #42–#47 work. The other agent's Japanese-famine and Mosquitor-port work is outside this lot, as are #17/#21 and deferred #38. No Git write or vanilla edit.

- [ ] Reproduce/snapshot the observed diagnostics, resolve current providers and source hashes.
- [ ] Install bounded justified lobby guards with exact preservation contracts.
- [ ] Run focused preservation and semantic control cases, prepare a grouped engine protocol.
- [ ] Human runtime acceptance; no inferred or invented test.

</details>
