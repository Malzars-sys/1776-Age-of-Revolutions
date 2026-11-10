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
