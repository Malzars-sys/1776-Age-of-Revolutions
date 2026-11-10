## Current ownership — Hawk, 2026-11-09

**Project status: In progress.** Selected from the live Backlog at the maintainer's request after delivering #22 to In review.

First bounded pass completed: built a reproducible inventory of every effective journal ID/provider, legacy fields, outcome metadata, masks, duplicates and DLC-dependent entries. This pass is read-only for gameplay files and preserves #25's immediate integration preparation. No bulk rewrite starts in parallel with that preparation.

Subsequent migrations must use per-entry mappings and bounded batches, preserving accepted #27 paths. No new runtime acceptance is claimed by ownership. #21 remains excluded; #38's comprehensive American redesign and concurrent map/law/economy work are outside this task.

### Initial inventory delivered — 2026-11-09

**In progress; inventory-only phase complete, no gameplay migration or engine acceptance.**

- 490 effective journal IDs in 201 effective files, including 162 same-path native masks and one explicit replacement directive. No ambiguous providers or parse errors in this inventory.
- 400 entries across 166 files still contain 1,381 direct legacy conclusion fields. These are structural migration findings, not 400 reproduced in-game failures.
- 87 entries have outcomes without the inspected minimum-metadata defects; 3 have no outcome and are explicitly held for permanent/disabled-intent review.
- 526 static add-journal consumers inventoried. Two literal targets lack a definition: native button -> `je_five_year_plan` (the mod retains `je_5_year_plan`) and a local Meiji event -> `je_meiji_imperial_marriage`. One `$JE$` parameter is not misreported as a missing literal ID.
- Eight masked native IDs and sixteen missing title-key candidates in both FR/EN are listed individually. No automatic restoration, alias, reactivation or invented conclusion was applied.
- Six classification control cases passed; all 2,484 captured gameplay/data sources and the journal-provider hashes remained unchanged. HEAD/index unchanged. No Git or vanilla write.

Read-only reproducible tool: `tools/compatibility/issue39_journal_catalogue.py`.

Local evidence (not committed/pushed): `docs/reports/compatibility/V1_15_ISSUE39_JOURNAL_CATALOGUE_2026_11_09/`, including `REPORT.md`, `NEXT_ACTION.md`, `INVENTORY.json`, `CATALOGUE.csv`, `ADD_JOURNAL_CONSUMERS.json`, `SOURCE_PROTECTION.json` and `VALIDATION.json`.

**Remaining:** per-entry semantic/dependency review, authored permanent/disabled exceptions, bounded migrations, localization resolution, DLC checks and human runtime acceptance. The original exhaustive acceptance checklist remains unchecked. Preserve #25 integration preparation before bulk gameplay edits, #27 accepted witnesses, #21 exclusion and #38 deferral.

---

## Objective

Audit **the complete effective journal-entry catalogue** for Victoria 3 1.15 and migrate every confirmed incompatibility, including entries that still fail to display completion or failure criteria.

The maintainer reports that additional journals remain broken after the bounded #27 batches were accepted. #27 is closed for those delivered lots; it was **not** an exhaustive migration. #24 is the broad map/journal/DLC workstream, but no separate exhaustive journal mission was found in the issue search on 2026-11-09.

**Parent workstream: #24. Release dependency: #25. Coordination: #19.**
**Priority: P1 overall; escalate entries active at the 1776 start or blocking a chain to P0.**
**Requested Project status: Backlog. Work order: mission #25 and its branch-integration preparation remain the maintainer's immediate priority.** Creating this issue does not start a bulk rewrite in parallel with #25.

## Scope

- Enumerate all journal definitions effectively loaded from the mod, same-path overrides, replacement directives and inherited native providers, with file/ID resolution.
- Cover the 1776-specific entries, inherited later-game entries, objectives/tutorials and DLC-dependent chains, including communist content and their consumers.
- Inspect activation, inactive visibility, progress bars, completion, failure, invalidation, deadlines, effects, continuations, buttons and required scripted dependencies.
- Investigate missing player-visible criteria as an actual journal/outcome contract issue; adding explanatory prose alone does not repair a rejected trigger.
- Distinguish intended permanent/inactive/hidden entries from genuinely broken conclusions. Document deliberate exceptions per entry rather than manufacturing success/failure conditions.

## Implementation checklist

- [ ] Produce a complete, reproducible inventory of effective IDs and providers; record duplicates, shadowed definitions, native masks and intentionally disabled/permanent entries.
- [ ] Review every entry against the canonical local 1.15 journal contract and its actual scripted consumers; classify migrated, compatible, broken, intentionally disabled, permanent, or awaiting engine verification.
- [ ] For each confirmed legacy conclusion, prepare a per-entry mapping to current outcomes preserving predicates, country/state/journal scopes, trigger ordering, simultaneous-condition priority, duration, progress and effects.
- [ ] Migrate in bounded batches; preserve success/failure/timeout/invalidation cleanup, rewards, claims, variables, inheritance/transfer behavior and delayed follow-up events. No blanket regex migration.
- [ ] Verify displayed headers, criteria and effect lists; resolve missing IDs/scopes/dependencies that prevent those outcomes from loading.
- [ ] Check French/English localization, dynamic references and raw-key failures. Keep technical explanations internally; perform the immersive text pass after human functional acceptance as required by the repository guide.
- [ ] Reuse and preserve accepted #27 paths as regression witnesses; do not reopen their accepted scope without a new, identified regression.
- [ ] Add representative engine tests for each migrated family: success, failure, deadline, invalidation, competing outcomes, continuation and active/concluded save/reload. Record unavailable scenarios explicitly.
- [ ] Compare new/rotated logs against an identified vanilla/reference configuration; separate prior debt, native-provider failures and new defects.
- [ ] Deliver the final inventory with every entry accounted for, remaining exceptions and human runtime acceptance; link the exact revision/candidate tested under #25.

## Preservation boundaries

The canonical vanilla installation is read-only. Preserve concurrent map/law/economy work and the original 1776 scenario. Do not reactivate the deferred Spanish chains, removed forced Polish partitions or other intentionally disabled historical content merely to remove a warning. Missing or optional DLC must not become an accidental mandatory dependency.

This is compatibility work, not the deferred comprehensive American Revolution redesign in #38.

## Acceptance

Every effective journal ID is accounted for. All confirmed broken outcome contracts in scope are fixed or explicitly blocked with a concrete dependency; no additional affected entry silently lacks its intended success/failure criteria. Authored mechanics and cleanup are preserved, relevant engine paths are accepted by the maintainer, and unresolved branches are visible to #25. A clean static scan alone does not certify all journals in game.

