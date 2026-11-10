## Current delivery — installed locally, 2026-11-08
**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Mission selected from the dashboard at the maintainer's request; Project status **In progress**. Mission **32 remains with the other agent**.

Two local gameplay files, three bounded blocks each (`visible`, `possible`, `ai`). All eight removed `strait_trade_importance_by` expressions are replaced by canonical 1.15 acceptance/dependence logic. Native toll-grievance and Free Trade preferences are retained per article. Six pre-existing visibility/possibility sites also used unavailable `scope:source_country`; existing logs show their type errors, and the installed treaty contract confirms source `root` instead. These gates now match native hierarchy/control checks.

Preserved byte-for-byte outside those blocks: 1776 `commercial_insurance_markets` prerequisite, article IDs, cost, involvement, flags, icons, ratification restrictions, effects and entire article `wargoal` blocks. No map, initial law, country technology or mission-32 war-goal file changed. Native `international_relations` prerequisite and `show_in_lens` flag were not imported.

**86/86 static checks on the candidate and installed files; 10 negative controls detected; 2,482 other script/data files retain their baseline hashes.** Synthetic formula checks cover both country directions, the dependence threshold and opposed Free Trade preferences. This is not engine acceptance or a final diplomatic-acceptance simulation.

Installed SHA-256:
- `common/treaty_articles/31_toll_exemption.txt`: `ac37db9568b72269c7438d58a0d6d6bb9e2aadd54c049dc878805b6e0fee1671`
- `common/treaty_articles/32_no_tolls.txt`: `d00f28122231f15797a761d1d6529fa5e9929da8d2b73009a9a4daf3d9a076d2`

Local evidence: `docs/reports/compatibility/V1_15_ISSUE29_TOLL_TREATIES_2026_11_08/` (`REPORT.md`, `RUNTIME_PROTOCOL.md`, `CHANGES.patch`, `BASELINE.json`, `INSTALLATION.json`, `VALIDATION.json`). Read-only validator: `tools/compatibility/issue29_toll_treaties_audit.py`. These files have not been committed/pushed; no remote publication, branch change or merge was performed.

**Still required:** fresh 1776 game, request/offer exemption, request no-tolls, Free Trade branches, actual strait effects, save/reload and post-fix logs, followed by maintainer acceptance before Done. The numbered acceptance checklist below remains pending.

## Original assessment and acceptance scope (retained)
## Classification and priority
**Confirmed removed script-link usage; gameplay impact unverified. P1.** Parent #21; treaty regressions #22; coordination #19. Backlog pending #20.

## Affected files and evidence
- `common/treaty_articles/31_toll_exemption.txt:133,139,163,169`.
- `common/treaty_articles/32_no_tolls.txt:131,137,161,167`.
All eight expressions use `strait_trade_importance_by(scope:source_country)`. The 1.15 API replaces the old link with dependency/grievance concepts; current vanilla treaty scripts use the new toll/access acceptance logic.

## Expected behavior and correction
Compute acceptance from the correct source/target country and current strait dependence/toll/access grievance semantics. Diff each clause against vanilla 1.15; do not substitute one guessed link into every expression.

## Testing and acceptance
- [ ] Explain the replacement for each of the eight expressions and retain the intended treaty direction.
- [ ] Test offering/requesting toll exemption and no-tolls agreements, including free-trade branches.
- [ ] Inspect AI acceptance and treaty effects and compare errors against #20.
- [ ] Reviewed changes and actual runtime evidence supplied before Done.

## Delivery safeguards
Use `hotfix/1.15`. Preserve the dirty local workspace, historical map work (#18) and Yekatarina's law audit (#17). Do not merge into main without explicit authorization. Static success is not runtime acceptance. General implementation is queued behind the initial #20 runtime comparison; planning this task does not authorize a bulk migration.

Evidence: [initial assessment](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/hotfix/1.15/docs/reports/compatibility/V1_15_INITIAL_ASSESSMENT_2026_11_06.md), local Victoria 3 `1.15.0 / 6338547985`, compared with the canonical read-only game files. No full modded first-day test has yet been accepted.
