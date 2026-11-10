## Current assignment — Codex, 2026-11-09

**Claimed at the maintainer's request: “Prends une nouvelle mission.” Requested Project status: In progress.**

A fresh read-only scan finds two `add_modifier` calls naming `scandalous` in `events/agitators_events/agitator_law_events_2.txt`, in `agitator_legal_events.5` and `.12`. The current native event options use `modifier_scandalous`, a registered temporary popularity modifier. `scandalous` is separately a character trait, not that static modifier.

### Bounded scope
- Verify both exact options, current native targets and effective provider resolution.
- Change only those two modifier-name values to `modifier_scandalous` if confirmed.
- Preserve recipient scopes, durations, all other effects, traits, conditions, event routing, localization and event payload bytes.
- Verify native FR/EN text/icon inheritance and typed references.
- Deliver bounded diff, meaningful regressions, source/index/native protections and an engine protocol.

### Acceptance
- [ ] Exact before/after and provider evidence.
- [ ] Two-reference correction installed without unrelated edits.
- [ ] Controls distinguish modifier IDs from trait IDs and detect wrong recipient/duration changes.
- [ ] Fresh reference audit and source protection.
- [ ] Runtime/human acceptance; static checks alone do not close the task.

Compatibility child of #25 / coordination #19. Hawk's AI-context delivery, #39 journals, #40 cultures, accepted #41, current economic adjustments and historical law/map work remain outside this task. The separate missing legacy communist reward modifier discovered by the scan is retained as an independent finding; it is not silently restored here.

No Git write, native edit, branch operation, merge, publication, law/technology grant or historical rewrite. Local evidence will use a task-specific `V1_15_ISSUE<number>_AGITATOR_MODIFIERS_2026_11_09/` directory.
