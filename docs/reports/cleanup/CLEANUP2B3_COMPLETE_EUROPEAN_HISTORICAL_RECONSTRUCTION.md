# CLEANUP-2B-3 — Complete European Historical Reconstruction

## 1. Baseline

CLEANUP-2B-3 started from the following real state:

```text
BRANCH = cleanup-post-release
HEAD = 8d7afe256ec55c14c6064f7e26f284e8a6ec4ad9
INDEX_EMPTY = YES
PRE_EXISTING_CHANGED_PATHS = 20
GIT_DIFF_CHECK_BASELINE = PASS
```

The dirty worktree was expected and retained. The baseline contained five tracked modifications and fifteen untracked files from CLEANUP-2B-1, CLEANUP-2B-2, CLEANUP-2B-2.5, one earlier naval report, and the seven protected technology research files. No file was cleaned, restored, stashed, staged, or otherwise mutated through Git.

## 2. Historical research packet

The three packet files were read in full:

- `RULERS_1776_EUROPE_RESIDUAL_MASTER.csv`
- `RULERS_1776_EUROPE_RESIDUAL_SOURCES.md`
- `RULERS_1776_EUROPE_RESIDUAL_CONSTITUTIONAL_NOTES.md`

The MASTER contains exactly 20 rows: 19 residual generated-ruler cases and the IREK shared-monarch verification. The packet supplied identity, date/age, office, title, constitutional role, mapping cautions, and source-quality flags. No general Internet research was performed.

```text
HISTORICAL_RESEARCH_PACKET_USED = YES
CODEX_EXTERNAL_HISTORICAL_RESEARCH_PERFORMED = NO
PACKET_ROWS_READ = 20
```

## 3. Runtime-error baseline

The previous user runtime was reconfirmed in the local logs:

- Batch 1: `Unknown effect designate_character_as_regent` in `cleanup2b1 - major rulers 1776.txt:142`.
- Batch 2: the same unknown effect in `cleanup2b2 - europe rulers 1776.txt:157`.
- UTF-8 BOM warnings for both character files and `common/government_types/00_mod_gov_types.txt`.

Unrelated post-validation and setup errors already separated by CLEANUP-2B-2.5 were not reassigned to this work.

## 4. Victoria 3 1.13 regency technical audit

The authoritative local target was `C:\Games\Victoria 3 The Great Wave\game`, the build whose runtime rejected the effect. It does not define `designate_character_as_regent`.

Multiple target-build examples prove the supported start-regency mechanism:

| Example | Ruler/heir structure | History mechanism |
|---|---|---|
| Spain | Maria Cristina `ruler = yes`; Isabel `heir = yes` | `set_variable = { name = regency_years value = 3 }` |
| Korea | Queen Sunwon `ruler = yes`; Yi Hwan `heir = yes` | `set_variable = { name = regency_years value = 2 }` |
| Jaipur | Major Alves `ruler = yes`; Ram Singh `heir = yes` | `set_variable = { name = regency_years value = 1 }` |
| Brazil | Diogo Feijó `ruler = yes`; Pedro II `heir = yes` | direct `regency_years` variable |

The target on-actions increment `regency_years` for a ruler while `has_gov_regency = yes`; target government types select Regency titles using that trigger. A newer Steam installation does contain the scripted effect, but it is not the build proven by the user's runtime and was not used as authority.

## 5. MARATH regency fix

Only the unsupported wrapper was replaced:

```text
set_variable = { name = regency_years value = 1 }
```

Sakharam Bapu Bokil remains the unique `ruler = yes`, age 60, and receives the proven regency variable. Madhavrao II remains the sole child `heir = yes`, born 1774-04-18, with Peshwa heir title through `gov_maratha_peshwa_regency`. The existing regency modifier remains. Anandrao Dhulap and the Konkan Flotilla were not edited.

```text
MARATH_RULER_COUNT = 1
MARATH_REGENT_STATIC = PASS
```

## 6. MEI regency fix

Charlotte Amalie remains the unique `ruler = yes`, born 1730-08-11. Her unsupported wrapper was replaced by:

```text
set_variable = { name = regency_years value = 13 }
```

Karl Wilhelm remains one secondary `heir = yes`, born 1754-11-19, never a second ruler. `gov_1776_meiningen_regency` still selects Regent for Charlotte and Duke for Karl Wilhelm.

```text
MEI_RULER_COUNT = 1
MEI_REGENT_STATIC = PASS
```

## 7. UTF-8 BOM fixes

The following files now begin with the real bytes `EF BB BF`:

1. `common/history/characters/cleanup2b1 - major rulers 1776.txt`
2. `common/history/characters/cleanup2b2 - europe rulers 1776.txt`
3. `common/history/characters/cleanup2b3 - residual europe rulers 1776.txt`
4. `common/government_types/00_mod_gov_types.txt`

The edited EN and FR localisation files also retain UTF-8 BOM and their required language headers.

## 8. Direct residual rulers

Twelve packet cases were directly implementable and were added without custom DNA, traits, art, succession events, diplomacy changes, or map changes:

| Tag | Implemented executive | Age | Title/role |
|---|---|---:|---|
| BEO | Charles Alexander of Lorraine | 63 | Governor-General |
| BRE | Hermann von Line | 70 | Bürgermeister |
| CRI | Devlet IV Giray | 47 | Khan |
| FRM | Hieronymus Maximilian von Glauburg | 60 | Senior Mayor |
| GAL | Heinrich Joseph Johann von Auersperg | 78 | Governor |
| HAM | Nicolaus Schuback | 75 | Bürgermeister |
| HUN | Albert Casimir of Saxony-Teschen | 37 | Royal Governor / Lieutenant |
| LUB | Bernhard von Wickede | 70 | Bürgermeister |
| SCM | Wilhelm Friedrich Ernst of Schaumburg-Lippe | 51 | Count |
| SWI | Johann Konrad Heidegger | 65 | Mayor of Zürich (Vorort) |
| TRS | Samuel von Brukenthal | 54 | President of the Transylvanian Gubernium |
| WLD | Friedrich Carl August | 32 | Prince |

George Browne for UBD was additionally implemented after the technical decision documented in section 16.

## 9. Conditional German tag mappings

| Tag | Local fork intent | Packet candidate | Confidence | Decision |
|---|---|---|---|---|
| ANH | Generic `Anhalt`; principality; capital STATE_ANHALT; no branch localisation or comment | Leopold III of Anhalt-Dessau | Insufficient | ABSTRACTION_DEFERRED |
| HOH | Generic `Hohenzollern`; one STATE_WURTTEMBERG province; PRU puppet; no Sigmaringen/Hechingen discriminator | Karl Friedrich of Hohenzollern-Sigmaringen | Insufficient | ABSTRACTION_DEFERRED |
| NAS | Generic `Nassau`; principality in STATE_HESSE; no Usingen/Weilburg discriminator | Karl Wilhelm of Nassau-Usingen | Insufficient | ABSTRACTION_DEFERRED |
| SCW | Generic `Schwarzburg`; principality in STATE_SAXONY; no Rudolstadt/Sondershausen discriminator | Ludwig Günther II of Schwarzburg-Rudolstadt | Insufficient | ABSTRACTION_DEFERRED |

Country definitions, history, state ownership, diplomacy, localisation, flags, capitals, and comments were checked. None prove the required branch. No candidate was forced and no subject or territory relation changed.

## 10. Free-city executives

BRE, FRM, HAM, and LUB retain `law_presidential_republic` and their existing voting laws. Their custom governments use `presidential_elective`, never hereditary transfer.

- BRE/HAM/LUB use the title `Bürgermeister` / `Bourgmestre`.
- FRM uses `Senior Mayor` / `Premier bourgmestre`.
- LUB remains a SWE puppet; this historically suspect pact is outside the authorised scope.

Each historical character is documented as a single-character abstraction of a collective city executive.

## 11. Lucca republican reconstruction

LUC now overrides the reactionary macro with:

```text
activate_law = law_type:law_presidential_republic
activate_law = law_type:law_oligarchy
```

The narrow `gov_1776_lucca_republic` uses presidential-elective transfer and the title `Gonfaloniere di Giustizia`. No historical name was invented because the packet does not securely identify the holder on 1776-01-01. The engine-generated short-term officeholder is intentional.

```text
LUC_REPUBLIC_RESTORED = YES
LUC_ABSOLUTE_DUCHY = NO
LUC_DUKE_TITLE = NO
LUC_GONFALONIERE_TITLE = YES
LUC_JUSTIFIED_PROCEDURAL_OFFICEHOLDER = YES
```

## 12. Switzerland confederal abstraction

SWI retains `law_parliamentary_republic` and `law_census_voting`. Johann Konrad Heidegger is represented as the Zürich/Vorort executive abstraction, age 65. The narrow government uses parliamentary-elective transfer and the title:

- EN: `Mayor of Zürich (Vorort)`
- FR: `Bourgmestre de Zurich (Vorort)`

No `President of Switzerland` title was introduced.

## 13. Habsburg delegated executives

BEO, GAL, HUN, and TRS remain `crown_land` subjects of AUS. Their narrow governments use dictatorial/appointed transfer, matching the target vanilla's crown-land governor model rather than hereditary sovereign transfer.

| Tag | Character | Display title | Sovereign preserved |
|---|---|---|---|
| BEO | Charles Alexander of Lorraine | Governor-General | Maria Theresa |
| GAL | Heinrich Joseph Johann von Auersperg | Governor | Maria Theresa |
| HUN | Albert Casimir of Saxony-Teschen | Royal Governor / Lieutenant | Maria Theresa, Queen of Hungary |
| TRS | Samuel von Brukenthal | President of the Transylvanian Gubernium | Maria Theresa |

Albert is never titled King. Brukenthal is not given his later 1777 Governor title.

## 14. Crimea

Devlet IV Giray is implemented as Khan, approximate age 47, under `gov_1776_crimean_khanate`. No territory, state ownership, subject status, Russian/Ottoman diplomacy, or map data changed. The regional map context remains future work, but the ruler is historically resolved.

## 15. Luxembourg map defer

LUX remains `MAP_REWORK_DEFERRED`. It receives no new character and no duplicate Maria Theresa. The current independent tag is not legitimised with a fictional sovereign. Map, ownership, subject, and diplomatic setup are untouched.

## 16. Baltic UBD decision

The target vanilla already defines `gov_guberniya` specifically for a grand-principality-tier UBD subject of monarchical RUS. It uses:

- `transfer_of_power = dictatorial`
- `RULER_TITLE_GOVERNOR_GENERAL`
- no sovereign king/duke/prince title.

This makes a safe temporary representation possible. George Browne, born 1698-06-15 and age 77, is implemented as the visible Governor-General. UBD remains a RUS puppet and its territory/diplomacy are unchanged.

```text
UBD_TEMPORARY_MAP_ABSTRACTION = YES
UBD_MAP_REWORK_DEFERRED = NO
```

## 17. Ireland verification / law audit

`common/history/diplomacy/00_subject_relationships.txt` establishes IREK as a personal union under GBR. The effective character VFS creates George III only once for GBR, so IREK reuses that shared monarch without a duplicate.

The malformed line `law_type:state_religion` was checked against the target laws. The only intended and valid church/state law ID is `law_state_religion`; the line was minimally corrected to:

```text
activate_law = law_type:law_state_religion
```

```text
IREK_SHARED_GEORGE_III = YES
IREK_LAW_FIX = FIXED
```

## 18. Europe 62-country final classification

The prior exhaustive 62-country inventory is retained. The 19 residual generated cases now resolve as eight new historical scripted rulers, five delegated executives, one justified procedural officeholder, one map-rework defer, and four branch-abstraction defers.

```text
EUROPE_ACTIVE_COUNTRIES_TOTAL = 62
EUROPE_HISTORICAL_SCRIPTED_TOTAL = 46
EUROPE_SHARED_HISTORICAL_MONARCH_TOTAL = 5
EUROPE_HISTORICAL_DELEGATED_EXECUTIVE_TOTAL = 5
EUROPE_JUSTIFIED_PROCEDURAL_TOTAL = 1
EUROPE_MAP_REWORK_DEFERRED_TOTAL = 1
EUROPE_ABSTRACTION_DEFERRED_TOTAL = 4
EUROPE_UNJUSTIFIED_PROCEDURAL_TOTAL = 0
```

The categories total 62. LUC is procedural by evidence-based design; LUX and the four ambiguous German abstractions are deliberately classified rather than forgotten.

## 19. Static validation

Validation results:

- Packet result rows / unique tags: 20 / 20.
- New residual character countries: 13; each has exactly one `ruler = yes`.
- MARATH and MEI ruler counts: one each.
- Negative ages: 0.
- Born after 1776-01-01: 0.
- Dead before start: 0.
- Duplicate rulers: 0.
- Duplicate character instantiations: 0.
- Duplicate template IDs introduced: 0 (the residual file uses direct characters, not templates).
- Invalid tags: 0.
- Invalid culture IDs: 0; only `primary_culture` is used.
- Invalid religion IDs: 0; no unsupported explicit religion is added.
- Invalid government IDs: 0.
- Missing EN/FR government or ruler-title localisation IDs: 0.
- Duplicate keys inside either edited localisation file: 0.
- Active parsed `designate_character_as_regent` occurrences: 0.
- Braces are balanced in all three cleanup character files and the government file.
- Daoguang, Mahmud II, Maria II, and other 1836 ruler identities were not introduced.
- `git diff --check`: PASS.

```text
MARATH_REGENT_STATIC = PASS
MEI_REGENT_STATIC = PASS
UTF8_BOM_STATIC = PASS
V13_STATIC_VALIDATION = PASS
```

## 20. USER condensed runtime checklist

Use one new 1776 game with only this fork enabled.

### A. Critical regency regression

1. MARATH — Sakharam Bapu Bokil — approximately 60 — Regent.
2. MARATH — Madhavrao II — age 1 — Peshwa/heir.
3. Confirm Anandrao Dhulap and Konkan Flotilla remain present.
4. MEI — Charlotte Amalie von Hesse-Philippsthal — 45 — Regent.
5. MEI — Karl Wilhelm von Saxe-Meiningen — 21 — secondary Duke/heir.
6. Confirm exactly one MEI ruler.

### B. Direct and delegated residuals

1. BEO — Charles Alexander of Lorraine — 63 — Governor-General — AUS crown land.
2. BRE — Hermann von Line — about 70 — Bürgermeister — republic.
3. CRI — Devlet IV Giray — about 47 — Khan.
4. FRM — Hieronymus Maximilian von Glauburg — about 60 — Senior Mayor — republic.
5. GAL — Heinrich Joseph Johann von Auersperg — 78 — Governor — AUS crown land.
6. HAM — Nicolaus Schuback — 75 — Bürgermeister — republic.
7. HUN — Albert Casimir of Saxony-Teschen — 37 — Royal Governor / Lieutenant — never King — AUS crown land.
8. LUB — Bernhard von Wickede — about 70 — Bürgermeister — republic.
9. SCM — Wilhelm Friedrich Ernst of Schaumburg-Lippe — 51 — Count.
10. SWI — Johann Konrad Heidegger — about 65 — Mayor of Zürich (Vorort) — never President of Switzerland.
11. TRS — Samuel von Brukenthal — 54 — President of the Transylvanian Gubernium — not later Governor.
12. UBD — George Browne — 77 — Governor-General — not monarch — RUS puppet.
13. WLD — Friedrich Carl August — 32 — Prince.

No ANH, HOH, NAS, or SCW character check is requested because all four mappings are deferred.

### C. Lucca, Ireland, and map defer

1. LUC — government is Republic of Lucca; Absolute Duchy and Duke are absent; Gonfaloniere di Giustizia is visible. A procedural personal name is expected and is not a failure.
2. IREK — George III — 37 — shared with GBR, with no duplicate independent George III.
3. LUX — no new sovereign is expected.

### D. Single log pass

Let several game days pass, quit normally, then inspect `error.log`, `debug.log`, and `game.log` once. Required results:

```text
UNKNOWN_DESIGNATE_CHARACTER_AS_REGENT = 0
BOM_WARNING_CLEANUP2B1 = 0
BOM_WARNING_CLEANUP2B2 = 0
BOM_WARNING_CLEANUP2B3 = 0
BOM_WARNING_MOD_GOV_TYPES = 0
ATTRIBUTABLE_CHARACTER_ERRORS = 0
ATTRIBUTABLE_GOVERNMENT_ERRORS = 0
ATTRIBUTABLE_LOCALIZATION_ERRORS = 0
```

## 21. Protected-state verification

The seven protected technology research files retain their baseline SHA-256 hashes and remain untracked and unstaged. BIC retains `law_frontier_colonization` and does not contain `law_colonial_exploitation`. No entry named exactly `bject` exists outside Git internals.

The baseline hashes of `.metadata/metadata.json`, `common/history/states/00_states.txt`, and the checked European/India military-formation files are unchanged. No map, state-region, state/ownership, province, front, army, navy, formation, Konkan Flotilla, Anandrao Dhulap, Real Armada Española, technology, or metadata file was edited. The Git index remains empty.

CLEANUP-2B-3 expected paths:

- modified: the Batch-1 and Batch-2 character files, `00_mod_gov_types.txt`, IREK and LUC country history, and EN/FR localisation;
- created: the residual character file, 20-row implementation result CSV, and this report.

All remaining status paths are accounted for by the photographed pre-existing baseline or CLEANUP-2B-2.5 documentation. Unexpected paths: 0.

## 22. Verdict

CLEANUP-2B-3 resolves every historically and technically implementable residual European case without forcing ambiguous branches or map structures. The two regencies now use the mechanism proven in the actual target build, all four required files have real UTF-8 BOM, and the 62-country classification contains no unexplained procedural ruler. The final condensed user runtime was completed successfully; its closure is recorded below.

```text
PACKET_ROWS_READ = 20
DIRECT_IMPLEMENTABLE_CASES = 12
CONDITIONAL_MAPPING_CASES = 4
JUSTIFIED_PROCEDURAL_CASES = 1
MAP_DEFERRED_CASES = 1
SHARED_MONARCH_VERIFICATION_CASES = 1

MARATH_REGENT_FIX = DIRECT_REGENCY_YEARS_VARIABLE
MEI_REGENT_FIX = DIRECT_REGENCY_YEARS_VARIABLE
BOM_FILES_FIXED = 4

ANH_MAPPING = ABSTRACTION_DEFERRED
HOH_MAPPING = ABSTRACTION_DEFERRED
NAS_MAPPING = ABSTRACTION_DEFERRED
SCW_MAPPING = ABSTRACTION_DEFERRED

LUC_REPUBLIC_RESTORED = YES
LUC_JUSTIFIED_PROCEDURAL_OFFICEHOLDER = YES
LUX_MAP_REWORK_DEFERRED = YES
UBD_TEMPORARY_MAP_ABSTRACTION = YES
UBD_MAP_REWORK_DEFERRED = NO
IREK_SHARED_GEORGE_III = YES
IREK_LAW_FIX = FIXED

EUROPE_UNJUSTIFIED_PROCEDURAL_TOTAL = 0
CODEX_LAUNCHED_VICTORIA3 = NO
USER_RUNTIME_REQUIRED = NO
SINGLE_FINAL_EUROPE_RUNTIME = COMPLETED
```

## 23. Final user runtime closure

The user completed the single condensed runtime and advanced the session normally to `1776-01-20` before quitting the game normally. The fresh logs contained no attributable regency, BOM, character, government, ruler-title, or localisation error.

Runtime observations:

- Sakharam Bapu Bokil: `PASS`;
- Charlotte Amalie: `PASS`;
- Lucca: `PASS`;
- Ireland: `PASS`;
- residual rulers: `PASS`.

Karl Wilhelm remains statically valid but was not visually verified. The supplied Baden screenshot showed Charles-Frederick von Zahringen, age 47, not Karl Wilhelm; this does not require another runtime.

```text
RUNTIME_SESSION_END_DATE = 1776-01-20
RUNTIME_QUIT_NORMAL = YES
FRESH_LOG_ATTRIBUTABLE_ERRORS = 0

MEI_KARL_WILHELM_STATIC = PASS
MEI_KARL_WILHELM_VISUAL = NOT_VERIFIED
KARL_WILHELM_RETEST_REQUIRED = NO

CLEANUP2B3_RUNTIME_VERDICT = PASS_WITH_KARL_WILHELM_SCREENSHOT_MISSING
CLEANUP2B3_RUNTIME = PASS
USER_RUNTIME_REQUIRED = NO
```

STOP.
