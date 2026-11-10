# #50 — Acre lobby country scope, 2026-11-10

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** The single installed fix has not been tested in the engine. Canonical version read from `C:\Games\Victoria 3\binaries\victoria3.exe`: **1.15.0**. Parent workstream #24; preserved journal migration #39.

## Observed problem and bounded selection

The current player error log was read and snapshotted without launching, stopping, rotating or clearing the game/logs. The captured bytes contain **six messages** pointing to `common/journal_entries/02_acre_dispute.txt:8`: unset `c` scope / invalid comparison left side. These are repeated diagnostics, not six distinct defects or a post-fix test. The full local byte snapshot and extracted messages are in `CAPTURED_ERROR_LOG.bin` and `OBSERVED_DIAGNOSTICS.json`.

An inventory of **494 effective journals** found **22 strict scalar country comparisons in lobby blocks**. In the unconditional explicit province-allocation model, two target countries have no initial province tokens: BOL and TIS. This is a limited source model, not proof of all runtime country existence. The TIS comparison is already in an explicit existence-guarded branch and has no selected observed diagnostic; it is retained. The other twenty comparisons, all optional comparisons and all non-lobby consumers remain unchanged. No bulk optional-operator conversion was performed.

The single selected case is `je_acre_dispute`. Its country definition exists, but that alone does not establish a runtime Bolivian country scope in the 1776 lobby. The canonical Acre script also uses the strict comparison; this is a scenario-availability compatibility correction, not proof that the native 1.15 script is universally broken.

## Installed change

Only `common/journal_entries/02_acre_dispute.txt`, inside `je_acre_dispute.is_shown_in_lobby`:

```diff
-        c:BOL = THIS
+        exists = c:BOL
+        c:BOL ?= THIS
```

The existing `has_dlc_feature = rp1_content` gate stays intact. The explicit existence condition makes the whole positive identity gate false when BOL is absent; the optional comparison avoids requiring an unset scope while evaluating it. With a matching existing Bolivia and the DLC active, the gate remains true. For another existing country or without the DLC it remains false. The fixture tests both possible absent-target defaults of the optional comparison, so this intended result does not depend on assuming that default.

This country-trigger pattern is demonstrated in canonical `common/journal_entries/01_natural_borders_of_france.txt`, in its `is_shown_when_inactive` block (`exists = c:FRA`, `c:FRA ?= THIS`). Its source hash, field and exact excerpt are recorded in `NATIVE_PATTERN.json`. This witness establishes the native trigger syntax; it is not a lobby-engine test.

The delivery adds **19 bytes**, preserves BOM/line endings and is exactly reversible to the captured original. Every byte outside this lobby block is identical. No country, initial history, border, population, law, technology, journal activation, outcome, reward, event, localization or art was added or altered.

## Tests and protection

- Candidate and installed file: **13/13 contract/preservation checks**, **6/6 context cases**, **6/6 deliberate-regression controls**.
- Cases cover target absent / target is current country / target is another country, each with DLC off/on. These are conservative three-predicate fixtures, not engine simulation.
- Controls detect missing existence guard, restored strict comparison, wrong country, altered DLC requirement, altered outcome and an unauthorized trailing-byte change. The outcome control is caught independently of the full-file equality check.
- The existing read-only journal dependency audit ran against the installed workspace: **494 journals, zero findings** within its typed-reference and metadata checks. It does not certify scope types or runtime behavior.
- `SOURCE_PROTECTION.json`: **2,533 existing inputs captured; the Acre file is the only changed input; 2,532 unchanged; no concurrent new runtime path at that capture.** Target matches its contract; canonical Acre source unchanged. Existing #27/#39 outcomes, all other journals, #46 events and the other agent's #48/#49 work were preserved.
- No Git write, vanilla write, game launch or human acceptance. Source snapshots and earlier evidence remain intact.

An initial audit-control exception was corrected before installation: the intentionally wrong-country fixture used a predicate outside the small model's vocabulary. That unsupported predicate now produces a failed equivalence check instead of terminating the run. Details remain in `INITIAL_AUDIT_ERROR.md`; final results are `CANDIDATE_VALIDATION_R2.json` and `LIVE_VALIDATION.json`.

Reproduce from the repository root with a fresh result filename:

```powershell
& 'C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B tools/compatibility/issue50_lobby_country_scope_audit.py --controls --output docs/reports/compatibility/V1_15_ISSUE50_LOBBY_COUNTRY_SCOPES_2026_11_10/LIVE_NEW_TIMESTAMP.json
```

The audit refuses existing output paths, writes only new evidence and has no installer. Its contract does not relax or rewrite the older #39 tests. A prior whole-file preservation witness covering Acre will correctly report this newly authorized, separately receipted lobby change; that must not be misattributed to an outcome regression.

Next: grouped engine review using `RUNTIME_PROTOCOL.md`. The fix's actual removal of the repeated diagnostic remains unverified; no global clean-log or journal-chain acceptance is claimed.
