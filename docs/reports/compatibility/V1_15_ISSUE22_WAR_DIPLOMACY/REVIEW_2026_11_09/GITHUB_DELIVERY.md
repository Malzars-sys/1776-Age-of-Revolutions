## Review delivery — Hawk, 2026-11-09

**Project #1: In review — IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Issue remains open. No new engine or human acceptance is claimed.

Installed locally against canonical Victoria 3 **1.15.0**:
- Corrected 13 remaining native war-support calibrations in six files: pacifist gates, national-identity bands, election event .7, aviation, technology event .30, and both retained Taiping branches. Commands/scopes match current native data; all other bytes/BOM are preserved.
- Restored four exact native play definitions hidden by the old same-path override: return a claim to a subject, release as subject, Russian unification and Polish uprising. Existing 1776 plays and starting wars remain unchanged.
- Inventoried 45 effective war goals and 60 plays; checked references, mirrors, native coverage and declared peace hooks. No blanket mirrors were added to custom political/partial-territory goals.

Executed evidence:
- #22: **276/276 static checks; 17/17 deliberate regressions detected**.
- #26: **1,732/1,732**; #32: **27/27**, plus 12/12 negative controls.
- #28: raw old whole-file contract 37/38, because #22 changes two unrelated event-.7 thresholds. Scoped comparison, reversing only those two values in memory: **38/38**. The old audit/contract is unchanged.
- 2,483 pre-intervention source hashes checked: only six authorized files changed and one play-definition file was added. HEAD and Git index unchanged. No Git write or vanilla write.
- Raw whitespace check flags one pre-existing space-tab indent on the changed aviation line; retained unchanged, documented.

Evidence is in the local workspace (not committed/pushed):
`docs/reports/compatibility/V1_15_ISSUE22_WAR_DIPLOMACY/REVIEW_2026_11_09/`
See `REPORT.md`, `RUNTIME_PROTOCOL.md`, `CONTRACT.json`, `VALIDATION.json`, `PREDECESSORS_FINAL.json`, and `PROTECTIONS.json`.

**Engine review still required:** two NEW games, American independence and IR1/Persia; observe initial subjects/participants/fronts, mid-war enforcement and mirror effects, peace callbacks/results, then save/reload. Static hook declarations do not prove callbacks fire.

Documented limits: canonical native `war_exhaustion_values.txt` still contains old function references (recorded upstream residue; engine consumption undetermined); American journal global-peace gate is pre-existing design under deferred #38. Russian/Polish scenarios and #32 territorial unification have no new runtime acceptance. The Nov-8 receipt is preserved with its original partial scope.

Boundaries preserved: #21, other agents' work, map/law/tech/economy changes, loans, Minutemen and Join Ongoing War. No further American redesign under this issue.

---

## Goal
Test modded wars and diplomacy against the substantially reworked 1.15 mechanics.

## Checklist
- [x] Inspect any custom war support, war exhaustion, capitulation, peace and war goal scripts for obsolete assumptions.
- [ ] Check whether war goals can be enforced mid-war and whether associated events/on_actions still fire correctly.
- [ ] Test the 1776 American Revolutionary War setup and at least one additional representative conflict using **new games**.
- [ ] Check subject relationships, war participants, fronts and peace results for unexpected behavior.
- [x] Separate 1.15 regression findings from existing historical-design changes; report reproducible cases with steps.

## Acceptance criteria
Representative war flows can start, progress and conclude without confirmed mod-specific critical failures; unresolved issues documented.

Original suggested Project status: **Backlog** (now **In review**, as recorded above). Suggested priority: **P0** if war gameplay is broken, otherwise **P1**.

Parent tracking issue: #19.

Scope: **Victoria 3 1.15 / State and Revolution compatibility only.** Do not mix with the ongoing historical map overhaul (#18) or Yekatarina's separate historical law audit (#17). No blanket edits or ahistorical data changes without evidence. Reference the exact game build, file paths, and test results.
