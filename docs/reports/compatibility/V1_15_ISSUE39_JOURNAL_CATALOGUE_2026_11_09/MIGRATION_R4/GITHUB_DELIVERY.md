## Current implementation — Hawk, 2026-11-09

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Installed locally; the issue remains open / In progress pending the full review and engine acceptance. No runtime result or complete DLC-parity acceptance is claimed.

### Installed
- Migrated **400 journal entries in 166 files** to **856 explicit outcomes** using per-entry parsed mappings, not a blanket regex conversion. All **1,381** original direct legacy conclusion fields are gone.
- Predicates, effect bodies/scopes, delays (including seven computed deadlines), progress, activation/disabled guards, callbacks and original predicate order are preserved. Custom headers and event/effect previews are moved into the appropriate outcomes.
- Restored exact native definitions `je_five_year_plan`, `je_meiji_imperial_marriage`, `je_state_and_revolution`, plus native `communism.12/.13` required by the plan's bound button and continuation. No new automatic activation/history wiring, ID alias or replacement of authored communist choices.
- Added missing names/reasons for 16 retained IDs in French and English: **32 keys per language**, without overwriting existing keys.
- Removed four unresolved Niger/Ethiopia button references from the old colonial hub; retained its eight other buttons. No new colonial action, country, geography or law change.

**Delivered footprint: 167 existing files changed + 4 new files, 171 files total.** Initial installation used nine independently verified batches of at most twenty mapping files. R1/R2/R3 evidence is retained; final installed hashes are in **MIGRATION_R4/INSTALLATION.json**.

### Fresh verification
- **11,117/11,117** mapping/preservation checks pass; **14/14** deliberate regressions detected by the expected semantic checks.
- **65/65** auxiliary checks pass: exact native objects, referenced laws/modifiers/known helpers, bilingual key validity, native JE GUI inheritance, bound-button references and exact reproduction from captured sources.
- Final catalogue: **493 effective IDs**, **zero legacy fields**, no ambiguous provider or parse finding. Direct typed reference/metadata audit: **zero findings**. **491** bound-button bindings and **527** static journal additions checked; no unresolved literal target remains in those checked paths.
- Eight accepted #27 witness files retain their exact hashes.
- Immutable #21 audit: raw **480/485**, because four old whole-file preservation assertions now cover migrated journals; scoped comparison reversing only #39 spans IN MEMORY returns the original **484/485**, with the pre-existing technology-events drift from #22. No #21 validator, contract or tracking was changed.
- Raw whitespace check remains nonzero: 87 diagnostics traced to original payload lines or exactly preserved indentation. Initial introduced blank-line artifacts were corrected; raw results and attribution are preserved.

### Limits and review
- No engine/GUI/DLC simulation or fresh-log acceptance was performed. Use the grouped **RUNTIME_PROTOCOL.md**; save/reload, competing conclusions, timeout/forced-removal cleanup and all-involved execution remain runtime gates.
- Three entries without authored outcomes are individually retained rather than given invented conclusions. Six orphan/deadline presentation cases are documented as dormant.
- Five native IDs remain masked by retained older families: Australia, Canada, Extraordinary Commission, Paris Commune and Social Revolution. Full new DLC-chain adaptation needs #24 content review; the restored State and Revolution definition does not recable the old communism.2 choices. This compatibility pass is not a claim of complete new-DLC feature integration.
- Preserved the frozen #25 integration proposal, accepted #27 content, #21 exclusion, #17 law work and #38 deferral. A concurrent Indonesia map-file edit was recorded and left intact. HEAD/index unchanged; no Git or vanilla write.

Local evidence, **not committed/pushed**:
`docs/reports/compatibility/V1_15_ISSUE39_JOURNAL_CATALOGUE_2026_11_09/MIGRATION_R4/`
See `REPORT.md`, `RUNTIME_PROTOCOL.md`, `MANIFEST.json`, `ENTRY_ACCOUNTING.json/.csv`, `INSTALLATION.json`, `LIVE_VALIDATION.json`, `AUXILIARY_FINAL_VALIDATION.json`, `DEPENDENCIES_FINAL.json`, `INVENTORY_FINAL.json` and protection/non-regression evidence.

The checked original checklist items below refer to inventory/mapping/migration/preservation. Unchecked runtime/full-content items are not waived.


<details>
<summary>Initial ownership and read-only inventory — retained history</summary>

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


</details>

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

- [x] Produce a complete, reproducible inventory of effective IDs and providers; record duplicates, shadowed definitions, native masks and intentionally disabled/permanent entries.
- [ ] Review every entry against the canonical local 1.15 journal contract and its actual scripted consumers; classify migrated, compatible, broken, intentionally disabled, permanent, or awaiting engine verification.
- [x] For each confirmed legacy conclusion, prepare a per-entry mapping to current outcomes preserving predicates, country/state/journal scopes, trigger ordering, simultaneous-condition priority, duration, progress and effects.
- [x] Migrate in bounded batches; preserve success/failure/timeout/invalidation cleanup, rewards, claims, variables, inheritance/transfer behavior and delayed follow-up events. No blanket regex migration.
- [ ] Verify displayed headers, criteria and effect lists; resolve missing IDs/scopes/dependencies that prevent those outcomes from loading.
- [ ] Check French/English localization, dynamic references and raw-key failures. Keep technical explanations internally; perform the immersive text pass after human functional acceptance as required by the repository guide.
- [x] Reuse and preserve accepted #27 paths as regression witnesses; do not reopen their accepted scope without a new, identified regression.
- [ ] Add representative engine tests for each migrated family: success, failure, deadline, invalidation, competing outcomes, continuation and active/concluded save/reload. Record unavailable scenarios explicitly.
- [ ] Compare new/rotated logs against an identified vanilla/reference configuration; separate prior debt, native-provider failures and new defects.
- [ ] Deliver the final inventory with every entry accounted for, remaining exceptions and human runtime acceptance; link the exact revision/candidate tested under #25.

## Preservation boundaries

The canonical vanilla installation is read-only. Preserve concurrent map/law/economy work and the original 1776 scenario. Do not reactivate the deferred Spanish chains, removed forced Polish partitions or other intentionally disabled historical content merely to remove a warning. Missing or optional DLC must not become an accidental mandatory dependency.

This is compatibility work, not the deferred comprehensive American Revolution redesign in #38.

## Acceptance

Every effective journal ID is accounted for. All confirmed broken outcome contracts in scope are fixed or explicitly blocked with a concrete dependency; no additional affected entry silently lacks its intended success/failure criteria. Authored mechanics and cleanup are preserved, relevant engine paths are accepted by the maintainer, and unresolved branches are visible to #25. A clean static scan alone does not certify all journals in game.

