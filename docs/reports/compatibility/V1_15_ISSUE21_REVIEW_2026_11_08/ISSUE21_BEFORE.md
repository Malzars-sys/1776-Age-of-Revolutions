## Current bounded delivery — population-ratio triggers, 2026-11-08
**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. Project status: In progress.** The maintainer asked the agent to take another mission; this continuation addresses four remaining legacy `pop_type_percent_country` payloads. The broader issue remains open.

Exactly **eight source lines in three local files** now use native `target = pop_type:...` and `value` comparisons:
- `common/political_movements/00_ideological_movements.txt`: anti-slavery radicalism (`slaves > 0`) and land-reform creation (`peasants > 0.25`). Existing logs reproduce invalid-pop-type errors at both sites.
- `events/agitators_events/agitators_election_events.txt`: event `.13`, `peasants >= 0.35`.
- `common/journal_entries/00_player_objectives_egalitarian_society.txt`: egalitarian objective condition, `peasants < 0.1`.

Each payload matches its corresponding canonical 1.15 native example. Thresholds, operators, country scopes, all other conditions/effects and 1776 technology mappings are preserved. Inverse substitutions reproduce the three original files byte-for-byte. Inventory finds **seven non-commented calls**, all with current arguments; the three already-correct urbanization calls are untouched. **2,482 other script/data files retain their entry hashes.**

**Journal limitation:** the egalitarian objective file still has 14 direct legacy conclusion fields. This delivery fixes its trigger arguments only; outcome migration and actual journal conclusion remain a separate #27 dependency. No fully functional journal or engine-error disappearance is claimed.

Local evidence: `docs/reports/compatibility/V1_15_ISSUE21_POPULATION_RATIO_TRIGGERS_2026_11_08/` (`REPORT.md`, `BASELINE.json`, `CHANGES.patch`, `VALIDATION.json`, native/before snapshots). Status is static only. New-game movement/event checks, post-restart logs and save/reload remain pending. No vanilla change, Git write, commit, push, branch switch or merge performed.

## Original workstream and acceptance criteria (retained)
## Goal
Identify mod scripts that are incompatible with the updated 1.15 scripting API and fix confirmed failures with targeted changes.

## Checklist
- [ ] Compare the 1.15 patch notes and modding digest with script files and the findings in the baseline issue.
- [ ] Audit references to old war exhaustion commands; 1.15 introduces war support equivalents such as `add_war_support_change`, `has_war_support_change` and `additional_war_support_change`.
- [ ] Review other removed or changed triggers, modifiers, scope requirements and obsolete script arguments.
- [ ] Avoid blind search-and-replace: evaluate each scope, sign, effect and gameplay meaning before migration.
- [ ] Record each changed key, file path, reason, and relevant vanilla 1.15 equivalent.
- [ ] Retest startup and check whether the relevant error-log entries disappear without creating new ones.

## Acceptance criteria
No known **mod-caused** critical script parser errors from the audited files; linked PR with documented migration decisions.

Suggested Project status: **Backlog** (begin after baseline triage). Suggested priority: **P0**.

Parent tracking issue: #19.

Scope: **Victoria 3 1.15 / State and Revolution compatibility only.** Do not mix with the ongoing historical map overhaul (#18) or Yekatarina's separate historical law audit (#17). No blanket edits or ahistorical data changes without evidence. Reference the exact game build, file paths, and test results.
