# Issue 26 — native 1.15 war support with preserved 1776 scenario deltas

Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Static evidence only; no engine run or human acceptance is claimed. Delivery extends `hotfix/1.15` and PR #34. Issue #26 stays open. The maintainer explicitly requested implementation through review on 2026-11-07; this authorizes this bounded delivery, not integration into `main`.

## Problem and result

The mod's complete `common/defines/00_defines.txt` masked the canonical 1.15 file with an inherited 1.13.9 baseline. It retained a negative support minimum, obsolete exhaustion/automatic-capitulation keys and omitted the new support model. The old file is removed. `common/defines/zz_1776_scenario.txt` now contains only the proven 1776 start date, base working-adult ratio and existing demographic formulas. All other primary defines come from the installed native 1.15 file.

This deliberately restores current native defaults outside warfare too: the old values in those sections were inherited vanilla, not authored 1776 balance. No production recipe, technology graph, law, country, population placement, military formation or journal mechanic is changed by this lot. A separately requested localization addition renames the French expansion journal group; see below.

## Provenance and preservation

1. Commit `e5d97261` restored a complete 1.13.9 baseline with `START_DATE = "1776.1.1"`. The earlier [baseline report](../../cleanup/CLEANUP2D3A_ENGINE_BASELINE_AND_DEFINES_REPAIR.md) records that choice. Replacing that single date with 1836 reproduces its documented native SHA-256: `398c364c108ce3ffa57fb25e000e3b8bce50e1f882e37c36a358eea34e4e1cf0`.
2. The only subsequent committed defines change, `756e6c130ef97c41e03a4959eca67c81b57e1d89`, authored the workforce/demographic adjustments. The captured local file and `hotfix/1.15` file at `6d2d9f7684f1c5618b9c17ec6e558b44b6f7deab` match those committed semantics, including macro values. Byte-level BOM/line-ending differences are not treated as tuning.
3. The resulting override retains 18 effective definitions: date, workforce ratio, and all 16 demographic fields. Thirteen differ from current native; five retain unchanged thresholds/formula context. Original macro arithmetic is preserved with a distinct `aor1776_` prefix, including bare names inside arithmetic expressions.

| Authored input | Preserved value |
| --- | --- |
| Start date | 1776.1.1 |
| Working-adult base ratio | 0.30 |
| Monthly minimum/maximum birthrate | 0.00110 / 0.00510 |
| Monthly minimum/maximum mortality | 0.00095 / 0.00620 |
| Mortality multiplier at peak growth | 0.50 |

[AUTHORED_CONTRACT.json](AUTHORED_CONTRACT.json) contains the original demographic source fragment and its 18 resolved values. It makes the read-only audit reproducible without shipping the full historical vanilla file or private workspace captures. All ten sampled points on the original birth/mortality curves agree before and after migration.

## Complete define mapping

[DEFINE_MAPPING.csv](DEFINE_MAPPING.csv) maps every primary key in the union of the old and current native files, including values and source lines. Counts use parsed engine definitions, excluding preprocessor macros; the earlier issue's 263-name lexical inventory was not a bug count and used a different counting method.

| Action | Definitions |
| --- | ---: |
| Inherit unchanged native default | 1,390 |
| Inherit changed 1.15 native default | 23 |
| Inherit newly introduced native default | 262 |
| Remove obsolete inherited 1.13 defaults | 143 |
| Retain proven 1776 deviation | 13 |
| Retain demographic formula context | 5 |
| Total mapped keys | 1,836 |

The old primary file has 1,574 effective definitions; the current native primary file has 1,693. All 1,693 are available after migration. No obsolete primary definition remains in the audited effective set. The map covers the entire old file, not only `NWar`.

## War behavior inherited from the installed engine data

| Old configuration | Current native behavior/configuration |
| --- | --- |
| `NDiplomacy.MIN_WAR_SUPPORT = -100` | Minimum 0; maximum 100 |
| Old support initialization assumptions | Base 100, drift target 50, initial floors 50 / 75 for negotiators; actual initial support depends on circumstances |
| `NWar.AUTO_CAPITULATE_WAR_SUPPORT` | Removed; zero support alone does not force the old automatic surrender |
| `WAR_EXHAUSTION_*`, including the old casualty/turmoil factors | Removed; native `WAR_SUPPORT_CHANGE_*` factors and ramps apply. These are a new model, not numerical renames of the old factors |
| No current low-support model | Native confidence/radicalization thresholds 75 / 25 and associated native modifiers |
| Old war conclusion assumptions | Native war-goal enforcement and peace mechanics; `WAR_STALEMATE_MONTHS = 6` |

Native casualties, battles, occupation, devastation, turmoil, finances, duration, subject and lobby factors are inherited without a 1776-specific override. Stalemate applies under native eligibility rules; revolutions, secessions and uprisings are exceptions. Do not demand the ordinary-war stalemate behavior from the American conflict if the engine classifies it as such an exception. The second test conflict must cover an ordinary war.

## Local delivery, concurrence and boundaries

The change is installed directly in the regular local mod, enabled in the active launcher playset **hhhh**, verified by a read-only launcher database query. Fully restart the game before testing; no extra registered mod copy or playset switch is needed. Old full-file bytes are backed up in the local delivery inputs, outside the active defines folder.

The initial protected inventory contains 6,677 files across functional directories and SERG/WORLD tracking. During the task one unrelated Russian-law file changed: `common/laws/1776_v115_russian_laws.txt`, SHA-256 `b9f9973470a175ab0be11d4fc61fd14a17556515c6040f52079dc82f41a4e283` → `7266d230ff7bda663afd63071a1393381e9ad0389ee62522c0b6b81c4cc4a740`. This task did not write it. The exact observed concurrent version is retained and excluded from publication. No earlier baseline was restored. The preservation check explicitly records this exception rather than claiming that no concurrent change occurred.

The Russia/Cossack override `zz_1776_world_russia01.txt`, map work, other laws, technology/economic work and SERG/WORLD tracking retain their captured hashes. Local HEAD, branch and index are unchanged; no local Git metadata writes or vanilla edits occurred. Remote publication changes only the explicit delivery paths and uses the current remote head as parent with an expected-head guard. No merge is authorized or performed.

The legacy event/status work (#28), initial-law investigation (#29), remaining journal migrations (#27), war-goal scripting (#32) and engine acceptance remain separate. This lot does not claim to fix their parser/runtime errors.

## Requested journal-group label

Two dedicated UTF-8-BOM replacement files override only `je_group_france_expansion`:

- French: **Guerres napoléoniennes**.
- English: **Napoleonic Wars**.

The entry `je_french_natural_borders` keeps the native **Les frontières naturelles de la France / The Natural Borders of France** title. Group membership, triggers, effects and the entry script are unchanged; the existing other members of the same group inherit the renamed heading too. No new local duplicate key is introduced. Rendering is pending the maintainer's test. See [LOCALIZATION.json](LOCALIZATION.json).

## Verification and limitations

- Local installed audit: **1,732 / 1,732**, `PASS_STATIC_ONLY`.
- Isolated remote delivery candidate: **1,732 / 1,732**, `PASS_STATIC_ONLY`.
- Nine deliberately incorrect virtual variants are all rejected: negative support minimum, obsolete automatic capitulation, obsolete exhaustion, altered stalemate duration, reset workforce, reset birthrate, wrong start date, reversed turmoil factor and an obsolete travel key. No mutation is written to gameplay files.
- Exact scenario-key allowlist, all native primary values outside that allowlist, complete demographic formulas, native loading-path resolution and scoped preservation are checked.
- French/English group consumers, key uniqueness and encoding are checked separately.

The static loader model assumes the canonical primary file followed by alphabetically later mod overrides; it does not substitute for the Paradox loader. Native float rounding and actual initialization/war behavior require engine observation. No Paradox parser, new game, save/reload or human result is represented as passed. [RUNTIME_PROTOCOL.md](RUNTIME_PROTOCOL.md) defines the acceptance steps.

Read-only reproduction from the repository root (Python 3, canonical local game required):

```powershell
python -B tools/compatibility/issue26_war_support_audit.py --mod-root . --vanilla-root 'C:/Games/Victoria 3/game' --output "$env:TEMP/1776_issue26_audit.json"
```

The explicit `--prepare`, `--install` and delivery-only `--validate` modes use local delivery captures; they are not needed to reproduce the published read-only audit.

## Sources

- Canonical local Victoria 3 **1.15.0 / 6338547985**, build 2026-11-03: `game/common/defines/00_defines.txt`, read only; SHA-256 `a970ab21532a2ac0536240d8369d76351819976e89aad6d3995edf350b2ab591`.
- Native `game/common/journal_entry_groups/00_journal_entries.txt` and English/French `journal_entries_l_*.yml` / `agitators_3_l_*.yml`, plus the mod's `01_natural_borders_of_france.txt`, for the exact group and entry consumers.
- Repository commits `e5d97261` and `756e6c130ef97c41e03a4959eca67c81b57e1d89`, the earlier baseline report and the captured pre-migration file, SHA-256 `d4cae45a9677ac6e1bf17b9e02dfb470f1decd921fe8d7d633aa75dfd58cbcac`.
- [Official Victoria 3 announcements](https://steamcommunity.com/app/529340/announcements/), Dev Diary 196, published 2026-11-05: explanation of the current support, peace and stalemate model. Installed native data remains the exact coefficient reference for this delivery.

Next action: maintainer runtime tests and review under #22/#26. Do not mark Done, close #26, remove draft status or merge solely because these static checks pass.
