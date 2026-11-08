# Issue 28 — migrate event exhaustion calls to native 1.15 support changes

Date: 2026-11-08 (Europe/Paris). Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Local installation and static checks are complete; engine acceptance remains pending. Delivery extends `hotfix/1.15` / PR #34. No main merge or automatic issue closure.

## Problem and resulting behavior

Two event files retained four commands removed from the current engine: two `add_war_exhaustion` effects in **Anger at the Front** (`revolution_pulse1_events.2`) and two `has_war_exhaustion` predicates in **Pacifist Condemns the War** (`election_contextual_events.3`). The installed native 1.15 versions provide the current equivalents, target scopes and calibration.

The corrected effects reduce the event contribution to the owning country's **support change** in the selected war. The electoral event now checks for a support change strictly below −5, using the same condition to choose the saved war. These values concern change, not the current support level; they must not be replaced with an instantaneous support-level effect.

Two companion support-level gates in the revolutionary event also move from `< 10` to `< 55`, matching native 1.15. Leaving these gates at 10 after #26 changed the support range would alter the event's eligibility band. The former −100…100 level scale maps to 0…100 via `(old + 100) / 2`, so 10 maps to 55. The four obsolete calls remain the main issue scope; these two directly related gates complete the same event's migration.

## Reviewed site mapping

All modified fields match the corresponding installed native payloads. Mod line numbers remain unchanged.

| File and line | Role | Before | After | Native line |
| --- | --- | --- | --- | ---: |
| `events/agitators_events/revolution_events_01.txt:188` | Option `.2.a`, one random branch | `add_war_exhaustion`, `value = 10` | `add_war_support_change`, `value = -5` | 209 |
| Same file, 213 | Option `.2.b`, guaranteed effect | Same positive exhaustion addition | Same negative support-change addition | 234 |
| Same file, 152 | Event eligibility, war level | `has_war_support`, `value < 10` | `has_war_support`, `value < 55` | 163 |
| Same file, 172 | Saved-war selection, war level | Same old level threshold | Same new level threshold | 183 |
| `events/election_events/election_contextual_events.txt:253` | Electoral event eligibility | `has_war_exhaustion`, `value > 10` | `has_war_support_change`, `value < -5` | 261 |
| Same file, 294 | Saved-war selection | Same old exhaustion threshold | Same new change threshold | 303 |

Every site retains `target = ROOT`. The effects remain inside `scope:anger_at_front_war`; the country event remains the recipient. The election still requires `attacker_warleader = ROOT` in both eligibility and selection. The stored scopes `anger_at_front_war` and `pacifist_war` are preserved.

Option `.2.a` still has three equal random branches: the support-change effect is one of them. Option `.2.b` applies that effect before its unchanged two-way random consequence. Option `.2.c` has no migrated war effect. Civil-war progress, morale modifiers, parties, momentum, cooldowns, cancellation, AI choices, titles, pictures and unrelated events retain their original token streams. Additional differences in the current native event files, including cooldown/AI/temporary-immortality changes, are not imported.

The functional diff is **two files, 11 replaced lines**: four command/parameter pairs, two level thresholds and one explanatory comment. No law, technology, recipe, country setup, map, journal or localization gameplay edit is included.

## Sources and compatibility evidence

- Canonical installed Victoria 3 `C:/Games/Victoria 3/game`, executable FileVersion/ProductVersion **1.15.0**. The existing code-revision log identifies `release/1.15.0 / 6338547985`; reading it is not a new engine run.
- Native versions of the two event files at the lines mapped above are the decisive payload/scope references. Local before-files and the remote branch at `9f9df1ee0a5724e61787de241578e5544cd60a2d` are token-equivalent before migration; each candidate is patched from its own current bytes.
- Native `common/effect_localization/00_diplomatic_play_effects_loc.txt:52` and `common/trigger_localization/00_trigger_localization.txt:3444` map the new API names. Native English/French effect labels describe support gain/change. These mapping files and effect-localization files are inherited, not masked by same-path mod files.
- Native `common/script_values/war_support_values.txt:508–510` adds `additional_war_support_change(scope:war.diplomatic_play)` to the support-change calculation. This distinguishes the event contribution from the support level itself.
- Existing on-action callers retain the revolutionary event in `common/on_actions/00_code_on_actions.txt:5904,5948`. The electoral caller is inherited from native `00_on_actions_election.txt:19`; this patch does not change either event's scheduling.
- [Official Victoria 3 announcements, Dev Diary 196 / 1.15 patch notes](https://steamcommunity.com/app/529340/announcements/), published 2026-11-05, confirm the removed exhaustion API and its support-change replacements. The installed event scripts supply the exact signed values used here.

[MAPPING.json](MAPPING.json) contains the before/after/native fragments and source lines. [CONTRACT.json](CONTRACT.json) retains native payload tokens and hashes of all code outside the six allowed sites, so the audit can be reproduced without private full-file snapshots.

## Verification actually executed

```powershell
python -B tools/compatibility/issue28_war_support_events_audit.py --self-test
```

- Installed local files: **38/38 checks, PASS_STATIC_ONLY**.
- Separate remote delivery candidate: **38/38 checks, PASS_STATIC_ONLY**.
- **10/10 negative controls rejected**: reversed effect sign, wrong target, instantaneous-level effect, reversed electoral comparison, inclusive boundary, mismatched selector threshold, unmigrated level gate, wrong war leader, reintroduced old API and changed random weight.
- The parsed electoral conditions accept −6 and −5.001, reject exactly −5 and higher values; both selectors agree. The level gates accept 54.99 and reject 55/55.01. These are bounded logic checks, not an engine simulation.
- All tokens outside the six approved nodes match the captured source. Native payloads and `ROOT` targets match at all sites. Full functional scanning of mod `events/` and `common/` finds no remaining `add_war_exhaustion` or `has_war_exhaustion` occurrence.
- **2,487 other protected functional and canonical tracking files retain their hashes**; no concurrent difference is found in that capture. Native source hashes and local Git HEAD, branch and index are unchanged. Previously accepted #26 defines and group labels, Ottoman/Russian follow-up, SERG/WORLD tracking, historical map, law and economic work remain outside the write scope.
- The existing parser helper used by the new audit matches the branch's published helper after BOM/line-ending normalization; no helper edit is needed. Source bytes, candidates, installation hashes and the scoped manifest are retained locally.

The static receipt is [VALIDATION.json](VALIDATION.json). No engine effect was executed, no eligibility fixture was observed in game and no new parser/runtime log is claimed. The command removal fixes a demonstrated script incompatibility; it is not presented as the cause of a reproduced startup crash.

## Acceptance and next action

The fix is installed directly in the regular local mod previously verified under playset **hhhh**. Fully restart before testing. [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md) covers both revolutionary options, the electoral trigger and selector, false/boundary cases, multiple wars and save/reload. A normal first day alone does not exercise these sites.

Issue #28 stays open / In review until the maintainer reports the targeted engine tests. The completed #26 acceptance does not automatically certify this event migration. No merge into `main`, PR draft removal, #27/#29/#30/#31/#32 migration or broader balance change is included.
