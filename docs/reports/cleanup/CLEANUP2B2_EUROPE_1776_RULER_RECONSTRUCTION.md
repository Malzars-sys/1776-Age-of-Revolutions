# CLEANUP-2B-2 — Europe 1776 Ruler Reconstruction

## 1. Baseline

- Branch: `cleanup-post-release`
- HEAD: `61f12eeacff1fd32379855477610290d6bc17874`
- Index: empty
- Initial `git diff --check`: PASS
- Pre-existing untracked files: `CLEANUP1C1_MARATH_NAVAL_CREW_DIAGNOSTIC.md` and the seven protected technology research files.
- Git mutation performed by Codex: none.
- Victoria 3 launched by Codex: no.

## 2. Batch-1 runtime closure

The user's Batch-1 runtime was successful for the rulers that were inspected. The Mughal Empire was not found visually before the game was closed, so Shah Alam II remains statically validated and is carried into the single Batch-2 runtime checklist.

```text
BATCH1_RUNTIME = PASS_WITH_ONE_DEFERRED_VISUAL_CHECK
MUG_SHAH_ALAM_II_STATIC = PASS
MUG_SHAH_ALAM_II_VISUAL_CHECK = DEFERRED
```

The same closure markers were added to `CLEANUP2B1_MAJOR_1776_RULER_RECONSTRUCTION.md` without claiming an unobserved visual PASS.

## 3. Historical research packet

The following files were read in full and used as the exclusive historical source of truth for Batch 2:

- `docs/research/characters/RULERS_1776_BATCH2_EUROPE_MASTER.csv`
- `docs/research/characters/RULERS_1776_BATCH2_EUROPE_SOURCES.md`
- `docs/research/characters/RULERS_1776_BATCH2_EUROPE_DESIGN_NOTES.md`

The MASTER contains 28 rows representing 27 distinct polity tag hints after `MEI_SECONDARY` is merged into MEI. No external historical research was performed. The fork and local vanilla 1.13 were consulted only for tags, country identity, laws, government syntax, regencies, personal unions, technical IDs, character loading and localisation.

## 4. Tag mapping

| Research polity | Tag hint | Actual fork tag | Country name | Exists 1776 | Country status | Current government | Current subject status | Status |
|---|---|---|---|---:|---|---|---|---|
| Electorate of Bavaria | BAV | BAV | Bavaria | YES | ACTIVE | monarchy / oligarchy | independent | RESOLVED |
| Electorate of Saxony | SAX | SAX | Saxony | YES | ACTIVE | monarchy / oligarchy | independent | RESOLVED |
| Duchy of Württemberg | WUR | WUR | Württemberg | YES | ACTIVE | monarchy / autocracy | independent | RESOLVED |
| Margraviate of Baden | BAD | BAD | Baden | YES | ACTIVE | monarchy / oligarchy | independent | RESOLVED |
| Brunswick-Wolfenbüttel | BRA | BRA | Brunswick | YES | ACTIVE | monarchy / oligarchy | independent | RESOLVED |
| Hesse-Kassel | HEK | HEK | Hesse-Kassel | YES | ACTIVE | monarchy / oligarchy | independent | RESOLVED |
| Hesse-Darmstadt | HES | HES | Hesse | YES | ACTIVE | monarchy / oligarchy | independent | RESOLVED |
| Mecklenburg-Schwerin | MEC | MEC | Mecklenburg | YES | ACTIVE | monarchy / autocracy | Swedish puppet | RESOLVED |
| Mecklenburg-Strelitz | MST | MST | Mecklenburg-Strelitz | YES | ACTIVE | monarchy / oligarchy | Swedish puppet | RESOLVED |
| Saxe-Weimar-Eisenach | WEI | WEI | Saxe-Weimar | YES | ACTIVE | monarchy / oligarchy | independent | RESOLVED |
| Saxe-Meiningen regent | MEI | MEI | Saxe-Meiningen | YES | ACTIVE | monarchy / regency | independent | RESOLVED_REGENCY |
| Saxe-Meiningen duke | MEI_SECONDARY | MEI | Saxe-Meiningen | YES | SECONDARY_NOT_COUNTRY | monarchy / regency | independent | RESOLVED_REGENCY |
| Saxe-Coburg-Saalfeld | COB | COB | Saxe-Coburg-Gotha | YES | ACTIVE | monarchy / oligarchy | independent | RESOLVED |
| Lippe-Detmold | LIP | LIP | Lippe | YES | ACTIVE | monarchy / oligarchy | independent | RESOLVED |
| Duchy of Oldenburg | OLD | OLD | Oldenburg | YES | ACTIVE | monarchy / oligarchy | independent | RESOLVED |
| Sardinia-Piedmont | SAR | SAR | Sardinia-Piedmont | YES | ACTIVE | monarchy / autocracy | independent | RESOLVED |
| Grand Duchy of Tuscany | TUS | TUS | Tuscany | YES | ACTIVE | monarchy / autocracy | independent | RESOLVED |
| Papal States | PAP | PAP | Rome | YES | ACTIVE | theocracy / oligarchy | independent | RESOLVED |
| Parma and Piacenza | PAR | PAR | Parma | YES | ACTIVE | monarchy / autocracy | French protectorate | RESOLVED |
| Modena and Reggio | MOD | MOD | Modena | YES | ACTIVE | monarchy / autocracy | independent | RESOLVED |
| Order of Malta | MLT | MLT | Malta | YES | ACTIVE | theocracy / autocracy | independent | RESOLVED |
| Republic of Venice | VEN | VEN | Venice | YES | ACTIVE | presidential merchant republic | independent | RESOLVED |
| Republic of Genoa | GEN | GEN | Most Serene Republic of Genoa | YES | ACTIVE | presidential merchant republic | independent | RESOLVED |
| Principality of Moldavia | MOL | MOL | Moldavia | YES | ACTIVE | monarchy / organic regulation | Ottoman protectorate | RESOLVED |
| Principality of Wallachia | WAL | WAL | Wallachia | YES | ACTIVE | monarchy / organic regulation | Ottoman protectorate | RESOLVED |
| Electorate of Hanover | HAN | HAN | Hanover | YES | ACTIVE | monarchy / oligarchy | personal union under GBR | RESOLVED_SHARED_MONARCH |
| Holstein | HOL | HOL | Holstein | YES | ACTIVE | monarchy / oligarchy | personal union under DENNOR | RESOLVED_SHARED_MONARCH |
| Schleswig | SCH | SCH | Schleswig | YES | ACTIVE | monarchy / oligarchy | personal union under DENNOR | RESOLVED_SHARED_MONARCH |

HES is technically confirmed as the fork's Hesse-Darmstadt abstraction: HEK separately owns the Hesse-Kassel provinces and vanilla's HES templates explicitly identify the dynasty as Hesse-Darmstadt.

## 5. Existing ruler audit

No Batch-2 direct tag had a surviving scripted ruler in the active replaced `common/history/characters` VFS directory. Twenty-four executive slots were therefore engine-generated. The three personal-union subjects inherit their senior partner's already scripted monarch.

| Tags | Current ruler/source | Generated | Current title before Batch 2 | Classification |
|---|---|---:|---|---|
| BAV, SAX | engine-generated | YES | King from kingdom tier | REPLACE_GENERATED + TITLE_FIX |
| WUR | engine-generated | YES | King from kingdom tier | REPLACE_GENERATED + TITLE_FIX |
| BAD | engine-generated | YES | Grand Duke from tier | REPLACE_GENERATED + TITLE_FIX |
| BRA, MEC, MST, WEI, COB, OLD, PAR, MOD | engine-generated | YES | generic Prince/Grand Duke/Duke depending tier | REPLACE_GENERATED + TITLE_FIX |
| HEK, HES | engine-generated | YES | generic Prince/Grand Duke | REPLACE_GENERATED + TITLE_FIX |
| MEI | engine-generated | YES | generic Prince | SPECIAL_REGENCY |
| LIP | engine-generated | YES | generic Prince | REPLACE_GENERATED + TITLE_FIX |
| SAR | engine-generated | YES | King | REPLACE_GENERATED |
| TUS | engine-generated | YES | generic Prince | REPLACE_GENERATED + TITLE_FIX |
| PAP | engine-generated | YES | Pope | REPLACE_GENERATED |
| MLT | engine-generated | YES | generic theocratic title | REPLACE_GENERATED + TITLE_FIX |
| VEN, GEN | engine-generated | YES | Doge government already available | SPECIAL_REPUBLIC |
| MOL, WAL | engine-generated | YES | generic Prince | REPLACE_GENERATED + TITLE_FIX |
| HAN | George III from GBR | NO | country-side generic monarchy title | SPECIAL_SHARED_MONARCH |
| HOL, SCH | Christian VII from DENNOR | NO | country-side generic monarchy title | SPECIAL_SHARED_MONARCH |

Existing historical rulers corrected in this batch: 0. Existing Batch-1 identities reused through personal unions: George III once and Christian VII twice.

## 6. Direct dynastic rulers

The batch creates the following historical executives from exact packet dates: Maximilian III Joseph, Frederick Augustus III, Karl Eugen, Karl Friedrich, Karl I, Friedrich II of Hesse-Kassel, Ludwig IX, Friedrich II the Pious, Adolf Friedrich IV, Karl August, Ernst Friedrich, Simon August, Friedrich August of Oldenburg, Victor Amadeus III, Pietro Leopoldo, Pius VI, Ferdinand of Bourbon-Parma, Francesco III d'Este, Alvise IV Mocenigo and Brixio Giustiniani.

The three approximate cases use only packet ages: Emmanuel de Rohan-Polduc `age = 50`, Grigore III Ghica `age = 51`, and Alexandru Ipsilanti `age = 50`. No exact date was fabricated. All new portraits are procedural because no matching local historical DNA was found by exact-date audit.

## 7. Saxe-Meiningen regency

Charlotte Amalie is the single `ruler = yes`, with `female = yes`, exact birth date `1730.8.11`, and a `designate_character_as_regent` effect. `YEARS = 13` records completed tenure since 1763; vanilla 1.13 increments this variable annually rather than treating it as a future duration.

Karl Wilhelm is a separate adult `heir = yes`, born `1754.11.19`, and is displayed as Duke by the MEI regency government. There are never two starting rulers. The existing landowners ruling group receives the standard regency modifier.

```text
MEI_STARTING_RULER_COUNT = 1
MEI_REGENCY_RESOLVED = YES
```

## 8. Venice and Genoa republics

VEN and GEN retain `law_presidential_republic` and `law_merchant_republic`; neither country history file was edited. Alvise IV Mocenigo and Brixio Giustiniani occupy the single ruler abstraction. A narrow early-loading government selects the existing Doge title without changing transfer of power or republican laws.

```text
VEN_REPUBLIC_PRESERVED = YES
GEN_REPUBLIC_PRESERVED = YES
```

## 9. Papacy and Malta

Pius VI uses the vanilla PAP-scoped `gov_papacy`, which displays Pope and preserves the theocracy. Malta remains a theocracy and receives a country-scoped Grand Master government. Emmanuel uses the required approximate age 50.

## 10. Moldavia and Wallachia

Grigore III Ghica and Alexandru Ipsilanti are created with approximate ages 51 and 50. A shared country-scoped government displays Hospodar while retaining each country's monarchy and organic-regulation laws. The existing Ottoman protectorates, liberty desire, territorial ownership and diplomacy were not modified.

## 11. Shared monarch cases

- HAN is an active personal-union subject of GBR. George III is created only by GBR from the Batch-1 template and appears on the Hanover side with the Elector title.
- HOL and SCH are active personal-union subjects of DENNOR. Christian VII is created only by DENNOR and appears on each duchy side with the Duke title.
- No technical duplicate character was necessary, so `ENGINE_SHARED_MONARCH_LIMITATION = NO`.

```text
HAN_GEORGE_III_SHARED_OR_EQUIVALENT = YES
HOL_SCH_CHRISTIAN_VII_SHARED_OR_EQUIVALENT = YES
```

## 12. Titles and governments

The early-loading `00_mod_gov_types.txt` now contains narrow governments for: Electorates (BAV, SAX, HAN); duchies; BAD Margrave; HEK/HES Landgrave; LIP Count; TUS Grand Duke; MEI regency; MLT Grand Master; VEN/GEN Doge; MOL/WAL Hospodar. SAR's existing kingdom and PAP's existing papacy already provide the correct titles.

These governments do not change laws, country tiers, subjects or territory. They only select the 1776 title and transfer-of-power presentation already compatible with the country's laws.

## 13. Localisation

English and French character-name, title and government keys were added to the existing project localisation files. Both retain UTF-8 BOM, the correct language header and unique per-file keys. No GFX, clothing, accessory or DNA asset was added.

## 14. Static validation

- Clausewitz braces balanced after comments are excluded.
- MASTER rows parsed: 28; result rows: 28.
- Active country tags represented: 27.
- New characters: 25, comprising 24 effective rulers and one MEI secondary heir.
- New direct ruler count per active direct tag: exactly one.
- MEI `ruler = yes`: exactly one; MEI `heir = yes`: exactly one.
- Shared-monarch duplicate characters: 0.
- Duplicate template IDs added: 0; the batch uses direct history rather than templates.
- Negative ages: 0.
- Birth dates after `1776.1.1`: 0.
- Packet deaths before start: 0.
- Approximate ages converted to exact dates: 0.
- Vanilla 1836 ruler reintroduction: 0.
- EN/FR duplicate localisation keys: 0; BOM and headers retained.
- `git diff --check`: PASS.
- Staged paths: 0.
- Metadata, map, states, ownership, military formations, armies, navies and technology changes: 0.
- Victoria 3 was not launched; runtime UI/title/portrait confirmation remains required.

For every result row, `DISPLAY_AGE_STATIC` equals `expected_age`: the 22 newly encoded exact dates were recalculated against `1776.1.1`, the three approximate characters use their explicit `age` values, and the three shared-monarch rows reuse the already validated Batch-1 dates.

```text
V13_STATIC_VALIDATION = PASS
SAFE_FOR_USER_RUNTIME = YES
```

## 15. USER runtime checklist

Use one new 1776 game with only the fork enabled. First check the deferred Batch-1 item: **Mughal Empire — Shah Alam II — age 47 — Emperor**.

Priority checks in the same session:

1. Electorate of Bavaria — Maximilian III Joseph — 48 — Elector.
2. Electorate of Saxony — Frederick Augustus III — 25 — Elector.
3. Margraviate of Baden — Karl Friedrich — 47 — Margrave.
4. Hesse-Kassel — Friedrich II — 55 — Landgrave.
5. Hesse-Darmstadt — Ludwig IX — 56 — Landgrave.
6. Saxe-Weimar-Eisenach — Karl August — 18 — Duke.
7. Saxe-Meiningen — Charlotte Amalie — 45 — Regent; Karl Wilhelm — 21 — secondary dynastic Duke; exactly one ruler.
8. Kingdom of Sardinia-Piedmont — Victor Amadeus III — 49 — King.
9. Grand Duchy of Tuscany — Pietro Leopoldo — 28 — Grand Duke, never Emperor.
10. Papal States — Pius VI — 58 — Pope.
11. Duchy of Modena and Reggio — Francesco III d'Este — 77 — Duke.
12. Order of Malta — Emmanuel de Rohan-Polduc — approximately 50 — Grand Master.
13. Republic of Venice — Alvise IV Mocenigo — 74 — Doge; republic preserved.
14. Republic of Genoa — Brixio Giustiniani — 62 — Doge; republic preserved.
15. Principality of Moldavia — Grigore III Ghica — approximately 51 — Hospodar; Ottoman relationship preserved.
16. Principality of Wallachia — Alexandru Ipsilanti — approximately 50 — Hospodar; Ottoman relationship preserved.

Spot-check next, without restarting: Duchy of Württemberg — Karl Eugen 47; Brunswick-Wolfenbüttel — Karl I 62; Mecklenburg-Schwerin — Friedrich II the Pious 58; Mecklenburg-Strelitz — Adolf Friedrich IV 37; Saxe-Coburg-Saalfeld — Ernst Friedrich 51; County of Lippe-Detmold — Simon August 48; Duchy of Oldenburg — Friedrich August 64; Duchy of Parma and Piacenza — Ferdinand 24.

Finally check the active shared crowns: Electorate of Hanover — George III 37, Elector; Holstein — Christian VII 26, Duke; Schleswig — Christian VII 26, Duke. Confirm no unrelated duplicate monarch appears.

Let several days pass, exit normally, then inspect `error.log`, `debug.log` and `game.log` once for attributable character, government or localisation errors.

## 16. Deferred tags

No MASTER country is deferred. The following explicitly out-of-scope tags remain untouched: SWI, ANH, NAS, SER, LUC, HAM, BRE, FRM, LUB and CRI. They require later constitutional, collective-executive, map or regional work. The only carried visual observation is Batch-1 MUG.

No CLEANUP-2B-3, VFS-2, military rebalance, technology refactor or map refactor was started.

## 17. Protected-state verification

- The seven technology research files remain untracked, unstaged and untouched.
- BIC retains `activate_law = law_type:law_frontier_colonization` and does not contain `law_colonial_exploitation` in its country history.
- No entry named exactly `bject` exists outside Git internals.
- `.metadata/metadata.json` remains unchanged.
- No map, state, ownership, army, navy or military-formation file changed.
- Konkan Flotilla, Anandrao Dhulap and Real Armada Española were not edited.
- The index is empty; no Git mutation was performed.

## 18. Verdict

All 27 distinct Batch-2 country tags are resolved. Twenty-four generated executive rulers are replaced by historical characters, MEI receives one additional secondary dynastic heir, and three personal-union tags reuse their existing Batch-1 monarch without duplication. All 28 research rows have a PASS or SPECIAL_CASE_PASS result and the batch is statically safe for the user's single condensed runtime session.

```text
HISTORICAL_RESEARCH_PACKET_USED = YES
CODEX_EXTERNAL_HISTORICAL_RESEARCH_PERFORMED = NO

BATCH2_RESEARCH_ROWS = 28
BATCH2_DISTINCT_POLITY_TAG_HINTS = 27

BATCH2_COUNTRY_TAGS_RESOLVED = 27
BATCH2_RULERS_IMPLEMENTED = 27
BATCH2_EXISTING_RULERS_CORRECTED = 0
BATCH2_RANDOM_RULERS_REPLACED = 24

BATCH2_SHARED_MONARCH_CASES = 3
BATCH2_SPECIAL_REGENCY_CASES = 1

BATCH2_NEGATIVE_AGES = 0
BATCH2_BORN_AFTER_START = 0
BATCH2_DEAD_BEFORE_START = 0
BATCH2_DUPLICATE_RULERS = 0

MEI_REGENCY_RESOLVED = YES

VEN_REPUBLIC_PRESERVED = YES
GEN_REPUBLIC_PRESERVED = YES

HAN_GEORGE_III_SHARED_OR_EQUIVALENT = YES
HOL_SCH_CHRISTIAN_VII_SHARED_OR_EQUIVALENT = YES

MUG_DEFERRED_VISUAL_CHECK_INCLUDED = YES

V13_STATIC_VALIDATION = PASS
CODEX_LAUNCHED_VICTORIA3 = NO
USER_RUNTIME_REQUIRED = YES
SAFE_FOR_USER_RUNTIME = YES
```

## 19. CLEANUP-2B-2.5 runtime closure (2026-08-11)

This closure preserves the historical static implementation result above. The user visually confirmed MUG (Shah Alam II, age 47, Emperor), every Batch-2 priority check and spot-check, all shared monarchs, the checked governments and titles, VEN/GEN republics, and MOL/WAL protectorate status.

Runtime log inspection nevertheless found one Batch-2-attributable parser error in `debug.log`: `Unknown effect designate_character_as_regent` at `common/history/characters/cleanup2b2 - europe rulers 1776.txt:157`. The MEI Regent display can pass through the custom government/title setup while this unsupported designation effect is rejected. `debug.log` also records UTF-8 BOM warnings for the Batch-2 character file and `00_mod_gov_types.txt`; these warnings are attributable but are not counted as runtime errors.

For completeness, the same unsupported effect also occurs in the Batch-1 character file at line 142 and is attributed to Batch 1, not Batch 2. No attributable duplicate ruler/character, invalid template, culture, religion, ideology, government title/type, localisation, personal-union ruler, or `create_character` error was found.

No gameplay correction is made in CLEANUP-2B-2.5.

```text
MUG_SHAH_ALAM_II_VISUAL_CHECK = PASS
BATCH2_VISUAL_CHECKLIST = PASS
BATCH2_ATTRIBUTABLE_RUNTIME_ERRORS = 1
BATCH2_RUNTIME = FAIL

CODEX_LAUNCHED_VICTORIA3 = NO
USER_RUNTIME_REQUIRED = NO
```

STOP.
