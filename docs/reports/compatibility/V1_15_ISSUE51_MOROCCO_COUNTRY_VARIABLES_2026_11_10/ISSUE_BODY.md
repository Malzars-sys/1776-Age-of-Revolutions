## Delivery — 2026-11-10

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Corrective implementation installed locally; the new engine check remains pending. Project-column movement is separate and requires the applicable authorization. Issue stays open.

Corrected exactly **six variable expressions in one existing file**, `common/journal_entries/06_morocco_lands_of_anarchy.txt`: the initial and monthly `state_of_anarchy_scaled_mod` multipliers for Al Rif, Marrakech and Inner Morocco now read `root.var:<regional_progress_variable>` from the country, matching their six canonical 1.15 counterparts. Previously they read local state variables that the country-level writers do not set.

### Scope and evidence

- Exactly **30 bytes added**: six `root.` prefixes. No new runtime file, variable, default/stub, coefficient, DLC change, history or balancing change. Every other byte remains as captured; all four migrated outcomes, bar writers, dates, events and region selection are preserved.
- Retained logs contain **nine repeated wrong-type `none` messages** across three captured files, covering initialization and monthly regional modifiers. Snapshots predate this fix; no agent engine run or post-fix disappearance is claimed.
- **26/26 installed checks, 6/6 country/state arithmetic fixtures, 8/8 deliberate-regression controls passed.** Initial fixtures have no state variable; monthly fixtures contain conflicting state variables and distinct country values. All six full multiplier payloads match native.
- Existing read-only journal reference/metadata scan: **494 journals, zero findings** in its checked vocabulary; not an engine-scope certification.
- Source protection captured **2,536 existing inputs**: only this journal changed, 2,535 unchanged, no concurrent new runtime path at capture. Canonical source unchanged, installed candidate hash verified. #50's Acre guard, #48/#49 ports/Japan, #27/#39 outcomes and other work are preserved.
- Initial value 260 still computes multiplier 2.55 under the retained formula `progress / -100 + 5.15`. No new cap or balance adjustment.
- Additional native monthly ownership guards/cleanup were not silently imported. Behavior following state transfers remains a separate qualification.
- An initial test-control text pattern did not alter the scalar event-call syntax; the control was corrected. The initial 7/8 control result is retained, followed by final 8/8. No gameplay change was needed for that audit correction.

Evidence: `docs/reports/compatibility/V1_15_ISSUE51_MOROCCO_COUNTRY_VARIABLES_2026_11_10/` — `REPORT.md`, `RUNTIME_PROTOCOL.md`, `CONTRACT.json`, before/candidate/native sources, observed diagnostics/log snapshots, candidate/live checks, journal reference check, installation and source-protection receipts.

Read-only verifier: `tools/compatibility/issue51_morocco_variable_scope_audit.py`, fresh evidence filenames only. No Git write, vanilla edit, new runtime acceptance or release publication.

Next grouped engine check: fresh Morocco game, all three regional modifiers/bars at activation, a month transition, changed regional progress and save/reload; inspect only new log entries for the six wrong-type multiplier errors.

- [x] Trace six readers and country-level writers against canonical sources; capture diagnostics.
- [x] Install only the six justified country-root prefixes.
- [x] Static checks, meaningful scoped fixtures/controls, source protections and grouped protocol.
- [ ] Engine/human acceptance of this new fix.

<details>
<summary>Original assignment — retained</summary>

## Assignment — Hawk, 2026-11-10

Claimed at the maintainer's request “Hop, une nouvelle mission.” Parent compatibility workstream #24; preserve #39 migrated journal contracts and #50's Acre fix.

Qualify and repair the six country-variable reads used by state modifiers in `je_lands_of_anarchy`: three initial and three monthly multipliers. Current mod uses `var:...progress_bar_current_var` inside state scopes, whereas the current canonical 1.15 script explicitly uses `root.var:...`. Player logs contain corresponding wrong-type `none` diagnostics.

Bounded scope: identify writers, owner/root/state scopes, source/log evidence, apply only justified root prefixes, retain exact coefficients, dates, DLC gate, outcomes, initial variables and all other bytes. No rebalance, new variable/stub, country/state/history/ownership change or broad native file replacement. Additional native ownership-cleanup differences must be documented separately rather than silently imported.

The other agent is selecting its next task after #48 ports/#49 Japan; do not touch their paths. #17/#21, deferred #38 and WORLD/SERG are excluded. No Git or vanilla write, no engine/human acceptance implied.

- [ ] Trace six readers and writers against current canonical scopes; capture observed diagnostics.
- [ ] Install narrowly bounded proven corrections.
- [ ] Static checks, semantic fixtures, source protections and grouped engine protocol.
- [ ] Engine/human acceptance of this new fix.

Technical delivery may be marked locally ready for runtime review; a Project status change will require the applicable authorization.
</details>
