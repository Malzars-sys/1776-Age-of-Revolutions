## Current assignment — Codex, 2026-11-09

**Claimed at the maintainer's request: “Prends une autre mission.” Requested Project status: In progress.**

A fresh effective-provider scan finds **four literal trigger_event calls to three missing event IDs**:
- `russia_monarchy.12`: native Russian royal-succession helper.
- `ip4_coup.11`: native foreign-backed coup helper; this event is generic despite its source file residing under iberia_events.
- `set_hierarchy_event.3`: native Meiji button and the mod's existing Japan decision.

Canonical 1.15.0 supplies all three events, but the mod's same-path files omit them. Their immediately named journal/helper providers currently resolve; no restoration is installed by this claim.

### Bounded scope
- Recover exactly these native event definitions into isolated files, only after checking their effective dependencies, caller scopes and FR/EN presentation.
- Preserve every existing event, caller, condition, delay, effect helper and journal outcome. No automatic activation or country-history wiring.
- Add only demonstrably missing localization keys, if required; do not overwrite authored texts.
- Verify native equivalence, unique event providers, typed dependencies, reference before/after, negative controls and source protections.
- Document the six dynamic event calls and any other excluded cases without inventing targets.

The coup restoration does not start Spanish colonial/American content work; no historical country, law, technology, map, population, recipe or balance rewrite. #39 journal migration and other agents' delivered inputs remain intact. No Git write, native edit, branch operation, merge or publication.

- [ ] Exact provider/mask/caller evidence.
- [ ] Scoped restoration and dependent text/icon resolution.
- [ ] Controls, installed audit and source protection.
- [ ] Engine/human acceptance; static findings do not certify actual succession, coup or reform behavior.

Related workstream: #25. Local evidence will use a task-specific `V1_15_ISSUE<number>_EVENT_TARGETS_2026_11_09/` directory.
