## Current assignment — Codex, 2026-11-09

**Claimed at the maintainer's request to take the next mission and keep the board current. Requested Project status: In progress.**

Canonical `common/on_actions/_on_actions.md` allows additive on_action definitions but forbids multiple effect blocks on the same named hook. The effective mod has two `effect` blocks for `on_yearly_pulse`: the existing Manila earthquake branch in `00_code_on_actions.txt` and the Japan progression branch in `phase1_japan_tenpo_on_actions.txt`.

### Bounded correction
- Preserve the main hook and Manila file completely.
- Move the existing Japanese effect body, unchanged, into one uniquely named child on_action.
- Make the Japanese contribution to `on_yearly_pulse` an additive `on_actions = { child }` dispatcher, following the installed native documentation.
- Preserve all Japanese date windows, variables, laws, DLC guard, six event calls and root/country scope.
- Verify additive provider semantics, exact body preservation, no new missing reference, controls and source/index/native protections.

The supporting list audit also records six pre-existing missing targets (five events and `on_memento_mori`). These are outside this one-file conflict fix and must remain visible; no historical event or obsolete mortality handler is silently reactivated.

- [ ] Document provider conflict and native append contract.
- [ ] Install one bounded file correction, preserving both effects.
- [ ] Candidate/live checks, controls, list inventory and source protection.
- [ ] Engine/human acceptance; no claimed runtime order or reproduced last-provider-wins behavior.

Related workstream #25. No #39 journal edits, law/technology/history/map/economy rewrite, Git write, native modification, branch operation, merge or publication. Local evidence will use a task-specific `V1_15_ISSUE<number>_YEARLY_DISPATCH_2026_11_09/` directory.
