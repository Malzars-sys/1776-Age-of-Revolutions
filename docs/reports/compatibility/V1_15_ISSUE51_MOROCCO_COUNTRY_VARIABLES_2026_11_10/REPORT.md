# #51 — Moroccan anarchy country-variable readers

2026-11-10. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, not engine tested. Canonical executable version: **1.15.0**, `C:\Games\Victoria 3`. No Git or vanilla write.

The mod reads three country variables from state scope when calculating the regional `state_of_anarchy_scaled_mod`. The selected source contains three initial and three monthly reads. All six canonical counterparts explicitly qualify the variable as `root.var:`. Country-level writers initialize all three variables to 260, then refresh them from the respective journal bars each month; neither writer writes to the nested states.

## Installed scope

Only `common/journal_entries/06_morocco_lands_of_anarchy.txt`, six expressions:

| Variable | Readers changed |
| --- | --- |
| `al_rif_progress_bar_current_var` | Initial modifier and monthly modifier |
| `marrakech_progress_bar_current_var` | Initial modifier and monthly modifier |
| `inner_morocco_progress_bar_current_var` | Initial modifier and monthly modifier |

Each `value = var:<name>` becomes `value = root.var:<name>`. The whole file is reconstructible from its captured original by these six additions only: **30 bytes added**, no new runtime file, original BOM and line endings retained. Variable writers, all four migrated outcomes, coefficients, dates, DLC/lobby condition, journal bars/buttons, regional selection, event calls, modifiers, localization, history, provinces, population, laws and technologies are unchanged.

The multiplier remains `country_progress / -100 + 5.15`. An initial value of 260 therefore yields **2.55**. This is a source-level arithmetic result, not a measured in-game effect. The inherited static modifier applies -0.1 to state construction, infrastructure and education access per multiplier unit; its definition is not edited.

## Evidence and verification

- `OBSERVED_DIAGNOSTICS.json`: **nine repeated wrong-type `none` messages across three retained player error logs**, corresponding to initial and monthly modifier blocks. Snapshots are under `logs/`. They predate this correction and are not a post-fix engine test. Line numbers differ as older versions rotated through logs; both contexts and their current locations are recorded by the verifier.
- `CONTRACT.json`, `before/`, `candidate/`, `native/`: exact SHA-256 and source bytes. Current canonical file contains the same six `root.var:` reads. All six selected multiplier payloads match native after correction; the whole journal is deliberately not replaced with native.
- Candidate and installed checks: **26/26**, six country/state fixtures **6/6**, deliberate regressions **8/8**. Initial fixtures omit state variables; monthly fixtures deliberately place conflicting values on states and different values on the three country variables. Correct readers use the corresponding country values in both contexts.
- Controls independently remove each of the six root prefixes, alter a multiplier coefficient and alter an unrelated outcome. The expected scope, native-payload or outcome-preservation check rejects each case.
- The first candidate's source checks and six fixtures passed; one negative control did not mutate its intended text because that event call uses scalar syntax rather than an `id` block. The control was corrected; its initial **7/8** result remains in `CANDIDATE_VALIDATION.json`. Final results are `CANDIDATE_VALIDATION_R2.json` and `LIVE_VALIDATION.json`. No gameplay alteration was needed for that audit issue.
- `JOURNAL_REFERENCE_CHECK.json`: the existing read-only #39 typed-reference/metadata scan finds **494 journals and zero findings** in its vocabulary. This does not validate engine scopes or complete story reachability.
- `SOURCE_PROTECTION.json` records current preservation and any concurrent drift. Only this mission's one approved journal file is written; no other source or old evidence is restored or rewritten. In particular #50's Acre guard and #48/#49 ports/Japan work are preserved.

Reproduction with a fresh output name:

```powershell
& 'C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B tools/compatibility/issue51_morocco_variable_scope_audit.py --controls --output docs/reports/compatibility/V1_15_ISSUE51_MOROCCO_COUNTRY_VARIABLES_2026_11_10/LIVE_NEW_TIMESTAMP.json
```

The verifier is read-only except for a new evidence result and refuses to overwrite existing results.

## Limits and next action

The canonical monthly callback also has ownership checks and cleanup if a selected state changes owner. Those additional native differences were not imported: this pass fixes only demonstrated variable-reader scope errors. Territorial transfers and that cleanup remain a separate qualification, not a certified behavior of #51.

No new variables/default values, stubs, state variables or balancing changes were used to silence warnings. No game launch, log clearing, historical/map decision, human acceptance or parent-task closure. Follow `RUNTIME_PROTOCOL.md` during the next grouped engine review; actual removal of the observed errors is still to verify.
