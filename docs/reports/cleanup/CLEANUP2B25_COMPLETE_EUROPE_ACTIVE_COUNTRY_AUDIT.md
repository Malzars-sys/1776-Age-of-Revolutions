# CLEANUP-2B-2.5 — Complete Europe Active-Country Audit

## 1. Baseline

The audit started on branch `cleanup-post-release` at `61f12eeacff1fd32379855477610290d6bc17874`.

```text
BRANCH = cleanup-post-release
HEAD = 61f12eeacff1fd32379855477610290d6bc17874
INDEX_EMPTY = YES
WORKTREE_CHANGED_PATHS = 16
GIT_DIFF_CHECK_BASELINE = PASS
```

The 16 pre-audit paths were five tracked Batch-1/Batch-2 modifications and eleven untracked files: the Batch-2 character/history deliverables, one prior naval report, and the seven protected technology research files. These paths are treated as the immutable audit baseline. No Git mutation was performed.

## 2. Batch-2 runtime log verification

The user runtime ended normally on 2026-08-11. `error.log`, `debug.log`, and `game.log` were read. Broad pre-existing setup errors were not attributed to Batch 2 merely because they appear in the same session.

| Log location | Error text | Source file | Likely origin | Pre-existing or new | Batch 1 | Batch 2 | Severity | Action required |
|---|---|---|---|---|---:|---:|---|---|
| debug.log:1086 | File should be in utf8-bom encoding | `cleanup2b1 - major rulers 1776.txt` | Batch-1 file encoding | New attributable warning | YES | NO | LOW | Add BOM in a later gameplay implementation phase. |
| debug.log:1087 | Unknown effect `designate_character_as_regent` at line 142 | `cleanup2b1 - major rulers 1776.txt` | Batch-1 MARATH regency designation | New attributable error | YES | NO | Replace with a Victoria 3 1.13-supported regency mechanism later. |
| debug.log:1088 | File should be in utf8-bom encoding | `cleanup2b2 - europe rulers 1776.txt` | Batch-2 file encoding | New attributable warning | NO | YES | LOW | Add BOM in a later gameplay implementation phase. |
| debug.log:1089 | Unknown effect `designate_character_as_regent` at line 157 | `cleanup2b2 - europe rulers 1776.txt` | Batch-2 MEI regency designation | New attributable error | NO | YES | HIGH | Replace the unsupported effect later; do not alter history in this audit. |
| debug.log:917 | File should be in utf8-bom encoding | `common/government_types/00_mod_gov_types.txt` | Batch-2 government file encoding | New attributable warning | NO | YES | LOW | Add BOM in a later gameplay implementation phase. |
| debug.log, 18:52:47 | `PostValidate of effect 'create_character' returned false` | `common/history/military_formations/05_military_formations_india.txt:206` | Existing India military-formation content | Pre-existing / outside Batch 1–2 ruler packets | NO | NO | MEDIUM | Track separately if that formation is later audited; protected and untouched here. |
| debug.log, 18:52:47 (five entries) | `PostValidate of effect 'create_character' returned false` | Base/DLC event files (`soi_events`, `dreyfus_events`) | Installed game event validation | Pre-existing external content | NO | NO | LOW FOR THIS MOD AUDIT | No action in this fork phase. |

No attributable duplicate character/ruler, invalid character template, culture, religion, ideology, government type/title, localisation key, personal-union ruler, or `create_character` failure was found. The unrelated post-validation entries are explicitly separated above. The Batch-2 error count is one: warnings are reported but are not counted as runtime errors.

## 3. Batch-2 runtime closure

The user confirms MUG — Shah Alam II — age 47 — Emperor, every priority check and spot-check, the three Batch-2 shared crowns, government/title checks, VEN/GEN republics, and MOL/WAL protectorates as visually passing.

The visual result does not erase the parser result. MEI can appear as a Regent through the custom government/title setup while the unsupported designation effect is still rejected. Consequently the historical Batch-2 implementation result remains preserved, the visual checklist closes as PASS, and the overall runtime closes as FAIL with one Batch-2-attributable error.

```text
MUG_SHAH_ALAM_II_VISUAL_CHECK = PASS
BATCH2_VISUAL_CHECKLIST = PASS
BATCH2_ATTRIBUTABLE_RUNTIME_ERRORS = 1
BATCH2_RUNTIME = FAIL
```

## 4. Method for determining active countries

The active set was rebuilt from scenario data rather than from a hand-written country list:

1. Parse every `create_state` owner in `common/history/states/00_states.txt` (375 worldwide owner tags).
2. Map owned state keys to the effective West, South, and East Europe state-region definitions and the politically European portion of the Russia state-region definition.
3. Add scenario polities materialised by `common/history/diplomacy/00_subject_relationships.txt`, including crown lands, personal unions, protectorates, and puppets.
4. Resolve country capitals and tiers from `common/country_definitions`.
5. Subtract tags that are only defined, future/releasable, or neither territorial nor diplomatic at start.
6. Diff active European tags against effective explicit rulers under the character-history VFS, then subtract valid shared monarchs and the scripted regency.

The automatic difference is recorded in `EUROPE_GENERATED_RULER_CANDIDATES.csv`. `SER` is a defined country-history tag but owns no start territory and appears in no start subject pact, so it is not an active 1776 polity.

## 5. Definition of Europe

Europe includes the British Isles, France/Benelux, Iberia, Scandinavia, central Europe and all active German tags, Italy, Switzerland, Poland-Lithuania, the Balkans, Danubian principalities, eastern Europe, and politically European Mediterranean islands. Active country-tag dependencies located there are included.

`RUS` and `TUR` are retained and marked transcontinental. `CRI` is retained as `EUROPE_BORDER_CASE`. `UBD` is retained as an eastern-European dependency. Greenland's `GR7` and the Central Asian `KZH`/`OZH` fragments at Chelyabinsk are not treated as European polities because their political capitals and primary scenario identities lie outside this scope.

## 6. Complete active-country inventory

The authoritative row-level inventory is `docs/research/characters/EUROPE_ACTIVE_COUNTRIES_1776_AUDIT.csv`.

| Non-overlapping audit group | Tags | Count |
|---|---|---:|
| British Isles | GBR, IREK | 2 |
| France / Benelux | FRA, NET, BEO, LUX | 4 |
| Iberia | SPA, POR | 2 |
| Scandinavia and Danish duchies | SWE, DENNOR, HOL, SCH | 4 |
| German / central polities (excluding rows grouped elsewhere) | ANH, BAD, BAV, BRA, BRE, COB, FRM, HAM, HAN, HEK, HES, HOH, LIP, LUB, MEC, MEI, MST, NAS, OLD, PRU, SAX, SCM, SCW, WEI, WLD, WUR | 26 |
| Habsburg core and crown lands | AUS, GAL, HUN, TRS | 4 |
| Italy | GEN, GR3, LUC, MLT, MOD, PAP, PAR, SAR, SIC, TUS, VEN | 11 |
| Alpine confederation | SWI | 1 |
| Poland-Lithuania | PLC | 1 |
| Balkans / Danubian / Ottoman | TUR, MOL, WAL, MON | 4 |
| Eastern Europe / Baltic / Black Sea | RUS, UBD, CRI | 3 |
| **Total** | **All audited tags** | **62** |

```text
EUROPE_ACTIVE_TAG_COUNT = 62
EUROPE_AUDITED_TAG_COUNT = 62
EUROPE_UNAUDITED_ACTIVE_TAG_COUNT = 0
```

## 7. Ruler source classification

| Ruler source | Count |
|---|---:|
| BATCH1_SCRIPTED | 14 |
| BATCH2_SCRIPTED | 23 |
| REGENCY_SCRIPTED | 1 |
| PERSONAL_UNION_SHARED | 5 |
| ENGINE_GENERATED | 19 |
| PRE_EXISTING_HISTORICAL_SCRIPTED / OTHER_SCRIPTED | 0 |
| NO_VISIBLE_RULER / UNKNOWN | 0 |

Thus 38 countries have a direct scripted starting ruler (including MEI's scripted regent), five reuse a shared monarch, and 43 are non-procedural. The generated candidates are exactly the active-set difference after explicit rulers and shared crowns.

## 8. Remaining generated rulers

The 19 tags are:

`ANH, BEO, BRE, CRI, FRM, GAL, HAM, HOH, HUN, LUB, LUC, LUX, NAS, SCM, SCW, SWI, TRS, UBD, WLD`.

BEO, LUC, and SCW are runtime-confirmed by the user. The remaining 16 are high-confidence static inferences: each active tag has no explicit ruler in the effective VFS, no valid shared monarch, and no scripted regency.

P0: `LUC, LUX, SWI, UBD`.

P1: `ANH, BEO, BRE, CRI, FRM, GAL, HAM, HOH, HUN, LUB, NAS, SCM, SCW, TRS, WLD`.

## 9. Scripted but unverified rulers

`IREK` is the sole scripted-but-unverified European ruler case. It has a start personal union under GBR and therefore should share George III. This relation is statically present, but Ireland was not part of the Batch-1/Batch-2 runtime checklist. Its country history also contains `activate_law = law_type:state_religion`, lacking the normal `law_` prefix; this is a static implementation anomaly, not an attributable Batch-2 log error.

No direct scripted European ruler outside the validated Batch-1/Batch-2 packets survives the VFS, so there is no separately identified 1836/anachronistic scripted character candidate.

## 10. Government / constitutional anomalies

Nineteen active tags require historical government/title research before a ruler implementation:

- Generic dynastic/title model: ANH, HOH, NAS, SCM, SCW, WLD.
- Free-city or collective executive: BRE, FRM, HAM, LUB.
- Habsburg crown-land/representative model: BEO, GAL, HUN, TRS.
- Manifest constitutional or territorial abstraction: LUC, LUX, SWI, UBD.
- Border-region khanate model: CRI.

The presence of republican laws for BRE/FRM/HAM/LUB is positive evidence; their anomaly is the single executive/title abstraction, not a claim that their current laws are monarchic. The validated VEN and GEN merchant republics are not reopened.

## 11. German microstates

The German-polity count uses political/country identity, not merely direct membership lines in the HRE-themed power bloc. It includes AUS, LUX, HOL, and SCH as German-system polities and excludes the bloc's Italian members.

```text
GERMAN_ACTIVE_POLITIES_TOTAL = 30
GERMAN_GENERATED_RULERS = 11
GERMAN_GOVERNMENT_RESEARCH_REQUIRED = 11
GERMAN_ABSTRACTION_CASES = 3
```

Generated German tags: `ANH, BRE, FRM, HAM, HOH, LUB, LUX, NAS, SCM, SCW, WLD`. The principal abstraction cases are HOH (which polity), SCW (which Schwarzburg branch or combined tag), and LUX (territorial/subject representation).

The HRE-themed start bloc directly creates AUS as leader and lists 27 members. Austrian crown lands are pulled into the bloc by subject mechanics; the user runtime specifically confirms BEO appears in it. This bloc setup contains explicit post-1776 gameplay abstractions in comments and is not used as the sole geographic test.

## 12. Italian states

```text
ITALIAN_ACTIVE_POLITIES_TOTAL = 11
ITALIAN_GENERATED_RULERS = 1
ITALIAN_GOVERNMENT_RESEARCH_REQUIRED = 1
ITALIAN_REPUBLIC_CASES = 3
```

The active Italian tags are GEN, GR3, LUC, MLT, MOD, PAP, PAR, SAR, SIC, TUS, and VEN. VEN and GEN are validated merchant republics. LUC is the only generated case and is historically a republic case whose current absolute-duchy representation requires research.

## 13. Crown lands and dependencies

Seventeen of the 62 rows are subject polities:

- Personal unions: GR3→SIC, HAN→GBR, HOL→DENNOR, IREK→GBR, SCH→DENNOR.
- Austrian crown lands: BEO, GAL, HUN, TRS→AUS.
- Protectorates: MOL and WAL→TUR; PAR→SPA.
- Puppets: HOH→PRU; LUB, MEC, MST→SWE; UBD→RUS.

The five personal-union tags are classified as shared-monarch cases. Crown lands are not assumed to need an unrelated hereditary monarch: the correct governor/shared-sovereign abstraction is part of the research question.

## 14. Austrian Netherlands

```text
TAG = BEO
OVERLORD = AUS
SUBJECT_TYPE = crown_land
CURRENT_RULER = procedural character; name not captured
RULER_GENERATED = YES
CURRENT_GOVERNMENT = law_monarchy + law_landed_voting; displayed Crown Land
HISTORICAL_RESEARCH_REQUIRED = YES
```

The localisation and tutorial text explicitly say that BEO/Belgium represents the Austrian Netherlands in 1776. It owns territory in Wallonia, Flanders, and Gelre and is materialised as an Austrian crown land. Research must decide whether the visible character represents a governor-general or another delegated executive under Maria Theresa; no subject or map change is made here.

## 15. Schwarzburg

```text
TAG = SCW
ACTIVE_1776 = YES
CURRENT_RULER = procedural character; name not captured
CURRENT_GOVERNMENT = law_monarchy + law_oligarchy; displayed Duchy
CLASSIFICATION = COUNTRY_ABSTRACTION_RESEARCH_REQUIRED
PRIORITY = P1
```

The tag owns territory in `STATE_SAXONY`, appears in the HRE-themed bloc, and has no explicit ruler. Research must establish whether it represents Schwarzburg-Rudolstadt, Schwarzburg-Sondershausen, a combined abstraction, or something else; the displayed Duchy title is not accepted as historically settled.

## 16. Lucca

```text
TAG = LUC
ACTIVE_1776 = YES
ACTUAL_RULER = Duke Ambrogio di Boglio, age 32
GENERATED = YES
ACTUAL_GOVERNMENT = Absolute Duchy (law_monarchy + law_autocracy)
HISTORICAL_STRUCTURE_RESEARCH_REQUIRED = YES
PRIORITY = P0
```

This is the clearest residual European mismatch: a procedural hereditary duke appears where the historical polity requires republican/collective-executive research. No opportunistic correction was made.

## 17. Previously deferred tags

| Tag | Active 1776 | Current ruler/source | Current government | Why deferred | Research | Map dependency |
|---|---:|---|---|---|---:|---:|
| SWI | YES | Engine-generated | Parliamentary republic / census voting | 1776 confederal/collective executive | YES | NO |
| ANH | YES | Engine-generated | Monarchy / oligarchy | Branch, ruler, title and constitution | YES | NO |
| NAS | YES | Engine-generated | Monarchy / autocracy | Nassau branch and constitution | YES | NO |
| SER | **NO** | None; inactive tag | Traditional setup file only | No territory, subject pact, or other start materialisation | Future regional setup only | YES |
| LUC | YES | Ambrogio di Boglio, generated | Absolute Duchy | Republican constitution mismatch | YES | NO |
| HAM | YES | Engine-generated | Presidential republic / wealth voting | Collective/free-city executive | YES | NO |
| BRE | YES | Engine-generated | Presidential republic / wealth voting | Collective/free-city executive | YES | NO |
| FRM | YES | Engine-generated | Presidential republic / wealth voting | Collective/free-city executive | YES | NO |
| LUB | YES | Engine-generated | Presidential republic / wealth voting; SWE puppet | Free-city executive plus subject abstraction | YES | NO |
| CRI | YES | Engine-generated | Monarchy / oligarchy | Khanate and Black Sea regional context | YES | YES |

All nine active deferred tags appear in the 62-row audit. SER is explicitly documented but correctly excluded from the active count.

## 18. Map-dependent cases

Three active cases are marked map-dependent:

- CRI: Black Sea/Crimean khanate context and future regional batch.
- LUX: separate territorial and subject abstraction inside the former Austrian Netherlands area.
- UBD: Russian Baltic puppet/country abstraction whose 1776 identity cannot be settled by adding a ruler alone.

No map, state-region, state-history, ownership, or province file was modified.

## 19. Research batches recommended

| Batch | Scope | Tags |
|---|---|---|
| EUROPE-RESIDUAL-A | German dynastic microstates and exact title families | ANH, HOH, NAS, SCM, SCW, WLD |
| EUROPE-RESIDUAL-B | Free cities and collective/confederal republics | BRE, FRM, HAM, LUB, SWI |
| EUROPE-RESIDUAL-C | Italian residual constitution | LUC |
| EUROPE-RESIDUAL-D | Habsburg crown lands and Austrian territorial dependencies | BEO, GAL, HUN, LUX, TRS |
| EUROPE-RESIDUAL-E | Baltic and Black Sea border abstractions | CRI, UBD |

These batches arise from the actual 19-row queue. Historical research should precede any implementation prompt.

## 20. Protected-state verification

Final static checks establish:

- Only audit/report CSV/Markdown files were created or edited by this phase.
- The Git index is empty and no Git mutation was performed.
- The seven protected technology files remain untracked, unstaged, and byte-unchanged relative to the audit baseline.
- `bject` remains absent outside Git internals.
- BIC retains `activate_law = law_type:law_frontier_colonization` and does not contain `law_colonial_exploitation`.
- `.metadata/metadata.json`, map, state regions, ownership, provinces, fronts, armies, fleets, military formations, Konkan Flotilla, Anandrao Dhulap, and both Real Armada Española formations were not modified by this audit.
- `git diff --check` passes.

## 21. Verdict

The Europe set is closed with zero unaudited active tags. Nineteen procedurally ruled countries remain for external historical and constitutional research, including four P0 cases. One additional shared-monarch case, IREK, is scripted but not covered by the prior runtime checklist. The Batch-2 visual result passes, but the unsupported MEI regent effect makes the Batch-2 runtime result fail. This audit deliberately performs no ruler, government, law, localisation, diplomacy, or map implementation.

```text
BATCH2_VISUAL_CHECKLIST = PASS
MUG_SHAH_ALAM_II_VISUAL_CHECK = PASS

BATCH2_ATTRIBUTABLE_RUNTIME_ERRORS = 1
BATCH2_RUNTIME = FAIL

EUROPE_ACTIVE_COUNTRIES_TOTAL = 62
EUROPE_AUDITED_COUNTRIES_TOTAL = 62
EUROPE_UNAUDITED_ACTIVE_COUNTRIES = 0

EUROPE_GENERATED_RULERS_TOTAL = 19
EUROPE_SCRIPTED_UNVERIFIED_TOTAL = 1
EUROPE_SHARED_MONARCH_TOTAL = 5
EUROPE_UNKNOWN_RULER_TOTAL = 0

EUROPE_GOVERNMENT_RESEARCH_REQUIRED = 19
EUROPE_HISTORICAL_RESEARCH_REQUIRED = 19
EUROPE_MAP_DEPENDENT_CASES = 3

GERMAN_ACTIVE_POLITIES_TOTAL = 30
GERMAN_GENERATED_RULERS = 11

ITALIAN_ACTIVE_POLITIES_TOTAL = 11
ITALIAN_GENERATED_RULERS = 1

SCHWARZBURG_AUDITED = YES
AUSTRIAN_NETHERLANDS_AUDITED = YES
LUCCA_AUDITED = YES

EUROPE_UNAUDITED_ACTIVE_TAG_COUNT = 0

GAMEPLAY_FILES_CHANGED_BY_AUDIT = 0

V13_STATIC_AUDIT_VALIDATION = PASS
CODEX_LAUNCHED_VICTORIA3 = NO
USER_RUNTIME_REQUIRED = NO

SAFE_TO_BEGIN_HISTORICAL_RESEARCH_FROM_QUEUE = YES
```

STOP.
