# LOG-CLEANUP-13 — Final global reindex and QA

## Status

`LOG_CLEANUP_13 = PASS`

`CLEANUP_TECHNICAL = CLOSED`

`RUNTIME_HUMAN_REQUIRED = NO`

The final fresh LOG-12 runtime was globally reindexed and every runtime and additional static identity was attributed. The LOG-13 runtime through 23 January 1776 validated metadata, the SER/EGY optional scopes and the complete `00_subject_relationships.txt` family while proving that the five absent-target pact guards were defensive static fixes rather than the cause of the remaining assertion. The local audit then reattributed that assertion to 20 active `set_relations` calls whose 1776 parent exists while their target does not. The final post-patch human runtime validates that correction: the assertion is absent, neither diplomacy file emits a diagnostic, and no new attributable diagnostic appears. LOG-CLEANUP-13 is closed.

`ERROR_LOG_ZERO_REQUIRED = NO`

Closure means `FORK_ATTRIBUTABLE_ACTIONABLE_ERRORS = 0`; it does not mean an empty `error.log`.

## Canonical baseline and preflight

- Branch: `post-2.3.0-log-cleanup`
- HEAD: `37a252d48a5dbfbd93d94ac75e11be6fb7391277`
- LOG-CLEANUP-12 gameplay closure commit: `37a252d Close legacy region and eventtarget compatibility diagnostics`
- `LOG_CLEANUP_12_COMMITTED = YES`
- Index at preflight: empty
- Worktree at preflight: not fully clean because the four LOG-CLEANUP-12 documentation deliverables supplied by the preceding phase were untracked; they were preserved unchanged.

No stash, reset, checkout, staging, commit or push was performed.

## Canonical runtime isolation

Only the final human LOG-12 session was used:

- Victoria 3 `release/1.13.9`, hash `afea32b87`
- Netherlands, continued through 21 January 1776
- session window approximately `20:44:52`–`20:52:21`
- normal termination: `Quit: Quit from inside game`, then `Transition Game->Empty`
- no crash and no reported visual issue

The canonical diagnostic stream is `error.log`. `debug.log`, `game.log` and `system.log` prove provenance and normal termination. Older `.1` rotations belong to previous sessions and were excluded.

The final human LOG-13 runtime used the same Victoria 3 release/hash and Netherlands scenario through 23 January 1776. It had no crash or reported visual problem and terminated normally. Its targeted result was:

- metadata mismatch: 0 (`METADATA_PATCH_RUNTIME_PASS = YES`);
- SER unset/wrong-scope identities: 0 (`SER_SCOPE_RUNTIME_PASS = YES`);
- EGY unset/wrong-scope identities: 0 (`EGY_SCOPE_RUNTIME_PASS = YES`);
- all `00_subject_relationships.txt` unset/wrong-liberty-scope identities: 0 (`SUBJECT_RELATIONSHIPS_RUNTIME_PASS = YES`);
- invalid-country-relations assertion: 1;
- regressions LOG-2 through LOG-12: 0.

The subsequent final post-relations runtime used the local fork on Victoria 3 `release/1.13.9`, hash `afea32b87`, and terminated normally with `Quit: Quit from inside game` followed by `Transition Game->Empty`. It confirms:

- invalid-country-relations assertion: 0 (`FINAL_RELATIONS_RUNTIME_PASS = YES`);
- diagnostics pointing to `00_relations.txt`: 0;
- diagnostics pointing to `00_subject_relationships.txt`: 0;
- new diagnostics attributable to the final patch: 0;
- regressions LOG-2 through LOG-12: 0.

## Identity method

An identity is the exact combination of subsystem, diagnostic type, normalized message, script path and script line. Raw occurrences remain separate. This yields:

- `FINAL_RUNTIME_TOTAL_IDENTITIES = 1649`
- `FINAL_RUNTIME_TOTAL_OCCURRENCES = 1684`

PostValidate mirrors remain visible as log identities because the subsystem and diagnostic type differ, but the matrix explicitly links them to the same physical root. For example, 91 physical legacy `has_role` sites produce 182 log identities; they are not 182 independent corrections.

## Attribution gate before patch

- `RUNTIME_IDENTITIES_ATTRIBUTED = 1649`
- `RUNTIME_IDENTITIES_UNKNOWN = 0`
- `ADDITIONAL_STATIC_IDENTITIES_FOUND = 6`
- `ADDITIONAL_STATIC_IDENTITIES_ATTRIBUTED = 6`
- `ADDITIONAL_STATIC_UNKNOWN = 0`
- `FINAL_PENDING_ATTRIBUTION = 0`

The six additional static identities are five `hq = region_italy` references and one `hq = region_caucasus` reference in closed character-template content. They are `PROTECTED_SYSTEM`. Six apparent additional `has_role` matches were comments in `events/test_events.txt` and were correctly rejected as non-identities.

## Historical discovery classifications and closure

| Final classification | Identities | Occurrences |
|---|---:|---:|
| `FIXED_AND_RUNTIME_VALIDATED` (historically `FORK_ATTRIBUTABLE_FIXABLE`) | 6 | 6 |
| `FORK_ATTRIBUTABLE_SEMANTIC_REWRITE` | 0 | 0 |
| `KNOWN_FORK_DESIGN_DEBT_DEFERRED` | 243 | 244 |
| `ALREADY_ACCOUNTED_FOR` | 314 | 316 |
| `PROTECTED_SYSTEM` | 614 | 614 |
| `INTENTIONAL_FORK_DIVERGENCE` | 121 | 121 |
| `VANILLA_OR_EXTERNAL` | 270 | 302 |
| `VALID_CURRENT_API_OR_BENIGN` | 81 | 81 |
| `UNKNOWN` | 0 | 0 |

The identity total is 1,649 and the occurrence total is 1,684. The six historically fixable identities are one metadata identity, four SER/EGY scope identities and one invalid-relations assertion identity. All six are now `FIXED_AND_RUNTIME_VALIDATED`; none remains open. The six static-only protected identities are reported separately and are not added to the runtime class table. The five guarded absent-target pact sites are also static defensive fixes and own no runtime identity. The 20 invalid `set_relations` sites are physical roots linked to the single historical assertion identity; they are not 20 additional runtime identities.

- `FINAL_FORK_ATTRIBUTABLE_FIXABLE_DISCOVERED = 6`
- `FINAL_FORK_ATTRIBUTABLE_FIXABLE_REMAINING = 0`
- `FINAL_FORK_ATTRIBUTABLE_SEMANTIC_REMAINING = 0`

## Proved technical corrections

### Supported game metadata

The runtime reported that the fork metadata advertised 1.13.0 while the target is 1.13.9. `descriptor.mod` already used `1.13.*`; only `.metadata/metadata.json` was stale. The patch changes `supported_game_version` from `1.13.0` to `1.13.9` and leaves the public content version `2.3.0` unchanged.

This root accounts for one fixable runtime identity.

The first LOG-13 human runtime confirms `METADATA_PATCH_RUNTIME_PASS = YES`; the mismatch is absent and the metadata requires no further change.

### OZH/UZH defensive compatibility guards

The initial attribution of the four diplomacy scope identities to OZH/UZH was incorrect because it used pre-patch line numbers instead of the local non-committed file. The local 1776 state setup instantiates OZH in four state ownership sites and UZH in one. Their pact existence guards and optional liberty-desire scopes are valid and do not alter current behavior because both targets exist.

`OZH_UZH_GUARDS = KEEP`

`OZH_UZH_GUARDS_CLASSIFICATION = VALID_DEFENSIVE_COMPATIBILITY_GUARD`

These guards account for no runtime error identity and are preserved.

### SER/EGY optional country scopes

The post-patch runtime lines map in the local worktree to:

- SER: unset `c` at 436 and wrong-scope `add_liberty_desire = 20` at 437;
- EGY: unset `c` at 448 and wrong-scope `add_liberty_desire = 45` at 449.

The local 1776 state setup instantiates neither tag. Local vanilla 1.13.9 proves `c:SER ?=` and `c:EGY ?=` for the exact corresponding liberty-desire blocks. The corrected patch changes only `=` to `?=` and preserves both values.

`SER_EGY_SCOPE_ROOT_HISTORICAL = FORK_ATTRIBUTABLE_FIXABLE`

`SER_EGY_SCOPE_CLOSURE = FIXED_AND_RUNTIME_VALIDATED`

This root accounts for four runtime identities: two SER and two EGY.

- `SER_SCOPE_IDENTITIES_PATCHED = 2`
- `EGY_SCOPE_IDENTITIES_PATCHED = 2`

### Invalid-country-relations assertion

The 23 January runtime contains exactly one assertion identity, but all `00_subject_relationships.txt` unset/wrong-scope diagnostics are zero. The earlier causal link to DUR-KAF, USA-SEQ, USA-LIB, GBR-ORG and PER-ARM is therefore withdrawn. Those five guards remain technically valid static defensive fixes and preserve every parent, target and pact type.

A fresh audit of the local 1776 setup parsed all 232 active `set_relations` calls. It found 20 calls with an existing parent, an absent target and no target guard. Every one has an exact current-vanilla 1.13.9 homologue; the divergence is the fork's 1776 country presence, not the relation tuple. The active invalid set is:

- AUS -> KRA;
- BRZ -> ARG, PRA and PNI;
- FRA -> BEL;
- GBR -> ION and ABU;
- MON -> SER;
- NET -> BEL;
- SPA -> EGY, MEX, UCA, CHL and BOL;
- SWE -> NOR;
- USA -> LIB, SEQ, UCA and VNZ;
- WAL -> SER.

The targeted sweep also found 88 `create_diplomatic_pact` calls. Its only five active absent targets are the five already guarded defensive sites, so no unguarded pact candidate remains. Rivalries use present parents and targets, and `00_truces.txt` contains no relation effect.

The canonical runtime root is `ACTIVE_SET_RELATIONS_TO_ABSENT_1776_TARGETS`. Each of the 20 physical calls is now wrapped in `if = { limit = { exists = c:TARGET } ... }`. This form is established by current vanilla 1.13.9 effect scripts; every parent, target and value is unchanged, and each original relation still executes exactly when its target exists.

- `INVALID_RELATIONS_RUNTIME_IDENTITIES_BEFORE = 1`
- `SET_RELATIONS_TOTAL_ACTIVE = 232`
- `SET_RELATIONS_PARENT_EXIST_TARGET_ABSENT_BEFORE = 20`
- `INVALID_RELATIONS_STATIC_CANDIDATE_SITES = 20`
- `INVALID_RELATIONS_STATIC_SITES_PATCHED = 20`
- `INVALID_RELATIONS_ROOT_CONFIDENCE = HIGH`
- `SAFE_PATCH_PROVEN = YES`
- `FIVE_ABSENT_TARGET_PACT_GUARDS = KEEP_AS_STATIC_DEFENSIVE_FIXES`

The 20 physical sites are not counted as 20 runtime assertions.

The final post-patch runtime closes this root:

- `INVALID_COUNTRY_RELATIONS_ASSERT_AFTER = 0`
- `FINAL_RELATIONS_RUNTIME_PASS = YES`
- `ACTIVE_ABSENT_TARGET_SET_RELATIONS_AFTER = 0`
- `INVALID_RELATIONS_RUNTIME_IDENTITIES_BEFORE = 1`
- `INVALID_RELATIONS_RUNTIME_IDENTITIES_AFTER = 0`
- `NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_FINAL_PATCH = 0`

## Explicit family audit

- Character role API: all 91 physical `has_role` sites match the bounded canonical character audits; classification remains `ALREADY_ACCOUNTED_FOR`. No global substitution was made.
- Legacy `building_naval_base`: all 12 physical typed sites are covered by prior intentional/accounted naval dispositions. No shipyard guess was made.
- Character templates: current-invalid templates were reconciled with prior canonical template/character decisions and current vanilla ownership. No historical character was recreated.
- Localization duplicates: 506 Japan hotfix override identities are protected; 96 other fork override identities are intentional.
- Encoding warnings: loader-accepted warnings in protected content remain protected; the other accepted warnings are benign after the successful visual/runtime result. No protected historical file was rewritten for encoding alone.
- Acre dispute: both `c:BOL = THIS` diagnostics at line 8 reproduce from the same current vanilla 1.13.9 file, so they are `VANILLA_OR_EXTERNAL`, not fork-actionable.
- Metadata: runtime pass.
- OZH/UZH: valid defensive guards retained, with no runtime identity assigned to them.
- SER/EGY and all `00_subject_relationships.txt` scope targets: runtime pass.
- Five absent-target pact guards: retained as static defensive fixes with no causal link to the assertion.
- Active `set_relations` absent targets: corrected as described above.

## Canonical deferred and protected debt

- Country-law diagnostics: 113 identities / 113 occurrences, `KNOWN_FORK_DESIGN_DEBT_DEFERRED`.
- `state_religion`: 17 identities / 18 occurrences / 17 physical country-history files, `KNOWN_FORK_DESIGN_DEBT_DEFERRED`.
- `amendment_frugal_ordinance`: 4 identities / 4 occurrences, `ALREADY_ACCOUNTED_FOR`, protected Japan.

All other nonactionable families and their non-overlapping counts are preserved in `LOG_CLEANUP_13_DEFERRED_NONACTIONABLE_REGISTER.csv`.

No country law, law variant, starting technology, map data, state region, historical formation, ruler, portrait/DNA, protected Japan design, Iraq–Persia play or Tsar upstream file was changed.

## Non-regression LOG-2 through LOG-12

`REGRESSIONS_LOG2_TO_LOG12 = 0`.

The canonical runtime contains zero recurrence of the closed targeted families, including the convoy/law modifiers, Caucasus and `sr:` comparison families, removed interest-marker regions, legacy law/IG identifiers, DWI scope, Brazil and Landowners variant-parent diagnostics, leader-chance keys, Morocco modifier, and lobby enactment modifiers listed in the phase prompt.

## Static validation

- attribution gate: pass
- JSON metadata parse: pass (`supported_game_version = 1.13.9`)
- targeted legacy-family sweep: pass with six protected static-only identities
- corrected diplomacy audit: 232 active `set_relations` calls reviewed; 20 active absent-target sites guarded
- pact sweep: 88 pact calls reviewed; five active absent-target sites already guarded and zero unguarded remain
- diplomacy brace balance: pass
- relation parent/target/value tuples preserved: pass
- pact parents, targets and types preserved: pass
- `git diff --check`: pass
- gameplay files changed: 2
- localization files changed: 0
- metadata files changed: 1
- documentation files created: 5

## Closure decision

The final human runtime validates metadata, SER, EGY, the complete subject-relationships family and the 20-site `set_relations` correction. The invalid-country-relations assertion is absent and no new attributable diagnostic is present. Consequently:

- `LOG_CLEANUP_13 = PASS`
- `KNOWN_FORK_ACTIONABLE_ERRORS_FINAL = 0`
- `FINAL_FORK_ATTRIBUTABLE_FIXABLE_REMAINING = 0`
- `FINAL_FORK_ATTRIBUTABLE_SEMANTIC_REMAINING = 0`
- `FINAL_UNKNOWN = 0`
- `FINAL_PENDING_ATTRIBUTION = 0`
- `REGRESSIONS_LOG2_TO_LOG12 = 0`
- `ERROR_LOG_ZERO_REQUIRED = NO`
- `RUNTIME_HUMAN_REQUIRED = NO`
- `CLEANUP_TECHNICAL = CLOSED`
- `NEXT_PHASE = NONE`

No LOG-CLEANUP-14 is created and no additional runtime is required.

## Exhaustive `set_relations` site audit

This table records all 232 active calls from the local pre-patch file. `target_guard_present = YES (PATCHED)` identifies the 20 sites guarded by the final relations patch; all other rows were unchanged. `current_vanilla_homologue` compares the exact parent/target/value tuple with local vanilla 1.13.9.

| source_line_before_patch | parent_tag | target_tag | relation_value | parent_scope_optional | parent_exists_1776 | target_exists_1776 | target_guard_present | current_vanilla_homologue | runtime_candidate | classification | safe_fix |
|---:|---|---|---:|---|---|---|---|---|---|---|---|
| 3 | ARG | SPA | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 4 | ARG | BRZ | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 7 | PLC | AUS | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 8 | PLC | PRU | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 9 | PLC | RUS | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 12 | AUS | KRA | -30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 13 | AUS | TUR | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 14 | AUS | BAV | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 15 | AUS | BAD | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 16 | AUS | WUR | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 17 | AUS | SAR | 10 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 18 | AUS | SIC | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 19 | AUS | MOD | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 20 | AUS | PAR | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 21 | AUS | LUC | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 22 | AUS | PAP | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 25 | BAV | WUR | 50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 28 | BOL | NPU | 10 | YES | NO | NO | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 29 | BOL | SPU | 30 | YES | NO | NO | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 30 | BOL | IQU | 60 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 31 | BOL | CHL | -50 | YES | NO | NO | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 32 | BOL | ARG | -30 | YES | NO | NO | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 35 | BRZ | POR | 10 | YES | YES | YES | NO | DIFFERENT_VALUE | NO | VALID_ACTIVE | NONE |
| 36 | BRZ | ARG | -20 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 37 | BRZ | PRA | -50 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 38 | BRZ | PNI | -50 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 41 | BIC | BUR | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 42 | BIC | CHI | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 43 | BIC | JAP | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 44 | BIC | PAN | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 45 | BIC | MARATH | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 46 | BIC | HYD | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 47 | BIC | MYS | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 49 | BIC | BIC | 30 | YES | YES | YES | NO | EXACT | NO | VALID_DYNAMIC_SCOPE | NONE |
| 53 | MARATH | HYD | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 54 | MARATH | MYS | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 57 | MYS | HYD | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 60 | BUR | GBR | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 63 | CHI | TIB | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 64 | CHI | LAN | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 65 | CHI | KOR | 50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 66 | CHI | JAP | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 67 | CHI | DAI | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 68 | CHI | SIA | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 71 | CLM | SPA | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 72 | CLM | SPU | -20 | YES | NO | NO | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 73 | CLM | NPU | -20 | YES | NO | NO | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 76 | DAI | CAM | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 77 | DAI | SIA | -50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 80 | DEN | GBR | 20 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 81 | DEN | HOL | 30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 82 | DEN | SWE | -50 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 83 | DEN | RUS | -20 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 84 | DEN | PRU | -20 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 87 | EGY | HDJ | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 88 | EGY | TUR | -50 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 89 | EGY | RUS | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 90 | EGY | FRA | 10 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 91 | EGY | GBR | 10 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 92 | EGY | GRE | -30 | YES | NO | NO | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 95 | FIN | SWE | 20 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 96 | FIN | RUS | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 99 | FRA | PLY | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 100 | FRA | GBR | -40 | YES | YES | YES | NO | DIFFERENT_VALUE | NO | VALID_ACTIVE | NONE |
| 101 | FRA | PRU | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 102 | FRA | AUS | 20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 103 | FRA | NET | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 104 | FRA | BEL | -1 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 105 | FRA | SPA | -20 | YES | YES | YES | NO | DIFFERENT_VALUE | NO | VALID_ACTIVE | NONE |
| 106 | FRA | MAS | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 107 | FRA | PAP | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 108 | FRA | TUR | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 109 | FRA | USA | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 110 | FRA | CON | -50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 111 | FRA | MAS | -50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 112 | FRA | AIT | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 113 | FRA | TUG | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 116 | GBR | TUR | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 117 | GBR | POR | 50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 118 | GBR | BIC | 80 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 119 | GBR | ION | 30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 120 | GBR | SIL | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 121 | GBR | ORA | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 122 | GBR | HAN | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 123 | GBR | ABU | 30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 124 | GBR | HAM | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 125 | GBR | OLD | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 126 | GBR | BRE | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 127 | GBR | BRA | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 128 | GBR | SPA | -30 | YES | YES | YES | NO | DIFFERENT_VALUE | NO | VALID_ACTIVE | NONE |
| 129 | GBR | SCM | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 132 | GRE | TUR | -50 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 133 | GRE | RUS | 30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 134 | GRE | FRA | 10 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 135 | GRE | GBR | 20 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 138 | HAI | USA | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 139 | HAI | SPA | -10 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 140 | HAI | FRA | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 143 | JAP | NET | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 146 | KTI | NET | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 149 | LAN | NET | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 152 | MEX | USA | -50 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 155 | MOL | TUR | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 156 | MOL | WAL | 50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 157 | MOL | RUS | 40 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 158 | MOL | AUS | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 161 | MON | TUR | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 162 | MON | RUS | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 163 | MON | AUS | -15 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 164 | MON | SER | 30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 167 | MOR | SPA | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 168 | MOR | MAS | 20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 171 | BEL | GBR | 30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 174 | NET | BEL | -30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 175 | NET | LUX | 50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 176 | NET | GBR | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 177 | NET | TUR | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 178 | NET | BIC | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 179 | NET | BRU | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 180 | NET | ACE | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 181 | NET | BLG | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 182 | NET | DEI | 80 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 185 | ONT | GBR | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 188 | ORA | NET | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 191 | PER | RUS | -10 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 192 | PER | GBR | 30 | YES | YES | YES | NO | DIFFERENT_VALUE | NO | VALID_ACTIVE | NONE |
| 193 | PER | TUR | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 194 | PER | DUR | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 197 | SPU | SPA | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 200 | NPU | SPA | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 203 | PRG | SPA | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 206 | PRU | AUS | 20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 207 | PRU | RUS | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 208 | PRU | BRA | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 209 | PRU | LIP | 20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 210 | PRU | LUB | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 211 | PRU | SCW | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 212 | PRU | SCM | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 213 | PRU | COB | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 214 | PRU | MEI | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 215 | PRU | WEI | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 216 | PRU | HOH | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 217 | PRU | HEK | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 218 | PRU | MST | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 219 | PRU | WLD | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 220 | PRU | SAX | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 221 | PRU | ANH | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 222 | PRU | MEC | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 223 | PRU | HES | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 224 | PRU | NAS | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 225 | PRU | FRM | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 226 | PRU | HAN | 20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 227 | PRU | BAV | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 228 | PRU | BAD | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 229 | PRU | WUR | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 230 | PRU | GBR | 20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 233 | QUE | GBR | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 236 | RUS | AUS | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 237 | RUS | TUR | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 238 | RUS | CRI | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 239 | RUS | SWE | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 240 | RUS | CHI | 20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 241 | RUS | CHC | -50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 242 | RUS | CIR | -50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 243 | RUS | UZH | 10 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 244 | RUS | KZH | 10 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 245 | RUS | OZH | 10 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 248 | TUS | SIC | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 251 | SAR | SIC | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 252 | SAR | PAP | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 253 | SAR | FRA | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 256 | PAP | SAR | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 257 | PAP | SIC | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 258 | PAP | AUS | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 259 | PAP | SWI | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 262 | SER | TUR | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 263 | SER | AUS | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 264 | SER | RUS | 40 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 267 | SIA | CHP | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 268 | SIA | CMI | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 269 | SIA | LUA | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 272 | SPA | CUB | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 273 | SPA | GBR | -30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 274 | SPA | POR | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 275 | SPA | EGY | -1 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 276 | SPA | TUR | -1 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 277 | SPA | USA | 20 | YES | YES | YES | NO | DIFFERENT_VALUE | NO | VALID_ACTIVE | NONE |
| 278 | SPA | MEX | -30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 279 | SPA | UCA | -30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 280 | SPA | CHL | -30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 281 | SPA | BOL | -30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 284 | SWE | NOR | 30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 285 | SWE | PRU | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 288 | TUR | WAL | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 289 | TUR | TRI | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 292 | VNZ | SPA | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 295 | URU | SPA | -30 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 298 | USA | LIB | 30 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 299 | USA | SEQ | -20 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 300 | USA | UCA | 10 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 301 | USA | BRZ | 10 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 302 | USA | VNZ | 10 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 303 | USA | FRA | 30 | YES | YES | YES | NO | NONE | NO | VALID_ACTIVE | NONE |
| 304 | USA | GBR | -50 | YES | YES | YES | NO | DIFFERENT_VALUE | NO | VALID_ACTIVE | NONE |
| 307 | WAL | SER | 20 | YES | YES | NO | YES (PATCHED) | EXACT | YES | INVALID_ACTIVE_ABSENT_TARGET | APPLIED_IF_EXISTS_TARGET_GUARD |
| 308 | WAL | AUS | -10 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 309 | WAL | RUS | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 312 | HAN | HAM | 60 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 313 | HAN | OLD | 60 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 314 | HAN | BRE | 60 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 315 | HAN | BRA | 60 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 316 | HAN | SCM | 60 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 319 | CON | TUR | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 320 | CON | AIT | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 321 | CON | MAS | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 322 | CON | FRA | -50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 325 | MAS | AIT | 10 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 326 | MAS | CON | -20 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 327 | MAS | FRA | -50 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 330 | AIT | MAS | 10 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 331 | AIT | CON | 30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 332 | AIT | FRA | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 335 | KAB | GBR | -20 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 336 | KAB | BIC | -20 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 337 | KAB | RUS | 20 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 338 | KAB | HER | -10 | YES | NO | NO | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 339 | KAB | KAN | -20 | YES | NO | NO | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 342 | KAN | RUS | 10 | YES | NO | YES | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 343 | KAN | HER | -20 | YES | NO | NO | NO | EXACT | NO | INACTIVE_OPTIONAL_PARENT | NONE |
| 347 | WTU | OMA | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 348 | WTU | GLD | 40 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
| 352 | MBS | OMA | -30 | YES | YES | YES | NO | EXACT | NO | VALID_ACTIVE | NONE |
