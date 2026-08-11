# CLEANUP-2B-1 — Major 1776 Ruler Reconstruction

## 1. Baseline

- Branch: `cleanup-post-release`
- HEAD at baseline: `2018c8990eec783fa0be4ce8b0fc6aaf8f7c93f1`
- Index at baseline: empty
- Initial `git diff --check`: PASS
- Pre-existing untracked files: the seven protected technology research files and `CLEANUP1D_MARATH_NAVAL_CREW_DIAGNOSTIC_AND_FIX.md`.
- Active VFS metadata: exactly `common/history/characters`, `common/history/diplomatic_plays`, and `common/history/diplomacy`.
- Git mutation performed by Codex: none.

The prior VFS-1 user session has been recorded in `CLEANUP2B_VFS1_INITIAL_DIPLOMATIC_SETUP_ISOLATION.md` as runtime PASS. The duplicate Spanish formation name `Real Armada Española` is documented there and remains untouched.

## 2. Historical research packet

The following local files were read in full and used as the primary historical source of truth:

- `docs/research/characters/RULERS_1776_MASTER.csv`
- `docs/research/characters/RULERS_1776_SOURCES.md`
- `docs/research/characters/RULERS_1776_DESIGN_NOTES.md`

The packet contains 23 entries. At the user's explicit request, one narrow external research pass was performed for Sakharam Bapu after the packet proved insufficient to assign him a safe age. The Marathi Vishwakosh and Maharashtra State Gazetteer establish his period and role but do not supply a birth year; NDHistories cautiously proposes circa 1716. That estimate is implemented only as `age = 60`, not as a fabricated exact birth date. Fork, vanilla 1.13 and local logs were otherwise consulted only for Victoria 3 IDs, syntax, VFS behavior, governments, personal unions and regencies.

Sakharam research references:

- Marathi Vishwakosh: <https://vishwakosh.marathi.gov.in/33877/>
- Maharashtra State Gazetteer: <https://gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/Poona%20District/Poona-II/history_marathas.html>
- NDHistories, approximate 1716 estimate: <https://ndhistories.wordpress.com/tag/sakharam-bhagwant-bokil/>

## 3. Tag mapping

| Research polity | Tag hint | Actual fork tag | Country exists 1776 | Status |
|---|---|---|---:|---|
| Great Britain | GBR | GBR | YES | RESOLVED |
| Kingdom of France | FRA | FRA | YES | RESOLVED |
| Spain | SPA | SPA | YES | RESOLVED |
| Kingdom of Portugal | POR | POR | YES | RESOLVED |
| Russian Empire | RUS | RUS | YES | RESOLVED |
| Prussia | PRU | PRU | YES | RESOLVED |
| Habsburg Monarchy | AUS | AUS | YES | RESOLVED |
| Joseph II secondary | AUS_SECONDARY | AUS | YES | SECONDARY_NOT_COUNTRY |
| Sweden | SWE | SWE | YES | RESOLVED |
| Denmark–Norway | DEN | DENNOR | YES | RESOLVED |
| Polish–Lithuanian Commonwealth | PLC | PLC | YES | RESOLVED |
| Ottoman Empire | TUR | TUR | YES | RESOLVED |
| Qing Empire | CHI | CHI | YES | RESOLVED |
| Tokugawa Shogunate | JAP | JAP | YES | RESOLVED |
| Joseon | KOR | KOR | YES | RESOLVED |
| Mughal Empire | MUG | MUG | YES | RESOLVED |
| Maratha Confederacy | MARATH | MARATH | YES | RESOLVED_REGENCY |
| Hyderabad | HYD | HYD | YES | RESOLVED |
| Mysore | MYS | MYS | YES | RESOLVED |
| Zand Persia | PER | PER | YES | RESOLVED |
| Dutch Republic | NET | NET | YES | RESOLVED |
| Naples and Sicily | NAP/SIC | SIC (Naples) + GR3 (Sicily) | YES + YES | RESOLVED_PERSONAL_UNION |
| Montenegro | MON | MON | YES | RESOLVED |

There are 23 distinct country tags after expanding the two-country NAP/SIC row and excluding `AUS_SECONDARY` as an additional country.

## 4. Existing ruler audit

| Tag | Current ruler before batch | Source / generated | Age before | Role / title before | Classification |
|---|---|---|---:|---|---|
| GBR | George III | template / NO | 37 | ruler / King | KEEP_IDENTITY_FIX_DATA |
| FRA | Louis XVI | template / NO | 21 | ruler / Emperor from generic empire government | KEEP_IDENTITY_FIX_DATA + TECHNICAL_CONFLICT |
| SPA | Charles III | template / NO | 59 | ruler / King | KEEP_IDENTITY_FIX_DATA |
| POR | runtime-generated identity | engine / YES | runtime-generated | ruler / King | REPLACE_GENERATED |
| RUS | Catherine II | direct history / NO | 46 | ruler / Tsarina | KEEP_IDENTITY_FIX_DATA |
| PRU | generated child Friedrich Wilhelm observed by user | engine / YES | child | ruler / King | REPLACE_ANACHRONISTIC |
| AUS | Maria Theresa plus Joseph II | direct history / NO | 32 and 11 | two simultaneous rulers | SPECIAL_CASE |
| SWE | runtime-generated identity | engine / YES | runtime-generated | ruler / King | REPLACE_GENERATED |
| DENNOR | runtime-generated identity | engine / YES | runtime-generated | ruler / King | REPLACE_GENERATED |
| PLC | Stanislaw August | template / NO | 43 | ruler / elective King and Grand Duke | KEEP_IDENTITY_FIX_DATA |
| TUR | runtime-generated identity | engine / YES | runtime-generated | ruler / Sultan | REPLACE_GENERATED |
| CHI | runtime-generated identity | engine / YES | runtime-generated | ruler / Emperor | REPLACE_GENERATED |
| JAP | runtime-generated identity | engine / YES | runtime-generated | ruler / Shogun | REPLACE_GENERATED |
| KOR | runtime-generated identity | engine / YES | runtime-generated | ruler under anachronistic 1836 regency modifier | REPLACE_GENERATED + TECHNICAL_CONFLICT |
| MUG | runtime-generated identity | engine / YES | runtime-generated | ruler / Emperor | REPLACE_GENERATED |
| MARATH | runtime-generated identity | engine / YES | runtime-generated | ruler / generic monarchy title | SPECIAL_CASE |
| HYD | runtime-generated identity | engine / YES | runtime-generated | ruler / Nizam | REPLACE_GENERATED |
| MYS | runtime-generated identity | engine / YES | runtime-generated | ruler / Maharaja | REPLACE_GENERATED + TECHNICAL_CONFLICT |
| PER | Karim Khan Zand | template / NO | 70 | ruler and existing general / Shah | KEEP_IDENTITY_FIX_DATA + TECHNICAL_CONFLICT |
| NET | runtime-generated identity | engine / YES | runtime-generated | ruler / King under monarchy | REPLACE_GENERATED + TECHNICAL_CONFLICT |
| SIC | Ferdinand de Bourbon | direct history / NO | 24 | ruler / King | SPECIAL_CASE_KEEP |
| GR3 | Ferdinand through SIC personal union | engine relationship / NO | 24 | shared monarch | SPECIAL_CASE_KEEP |
| MON | runtime-generated identity | engine / YES | runtime-generated | ruler / Prince-Bishop | REPLACE_GENERATED |

The age of engine-generated rulers is intentionally reported as runtime-generated rather than reconstructed from unavailable save-state data.

## 5. Implemented rulers

Fourteen explicit starting executive rulers replace engine-generated identities:

`POR Joseph I`, `PRU Frederick II`, `SWE Gustav III`, `DENNOR Christian VII`, `TUR Abdülhamid I`, `CHI Hongli`, `JAP Tokugawa Ieharu`, `KOR Yeongjo`, `MUG Shah Alam II`, `MARATH Sakharam Bapu Bokil`, `HYD Nizam Ali Khan`, `MYS Hyder Ali`, `NET William V`, and `MON Sava II Petrović-Njegoš`. MARATH also receives the historical child heir Madhavrao II.

New characters use the packet's exact birth date or documented approximate age. No new general/admiral assignment or military formation was created. New portraits use the game's procedural system.

## 6. Corrected existing rulers

- George III: `1738.6.4`; existing DNA retained.
- Louis XVI: `1754.8.23`; existing DNA retained; specific 1776 King government added.
- Charles III: `1716.1.20`; existing DNA retained.
- Catherine II: `1729.5.2` new-style date.
- Maria Theresa: `1717.5.13`; single ruler.
- Stanislaw August: `1732.1.17`; existing DNA retained.
- Karim Khan Zand: fabricated `1705.1.5` removed and replaced with `age = 70`; existing DNA and pre-existing general role retained.

No second template or duplicate instantiation was added for these identities.

## 7. Austria co-regency

Maria Theresa is the only `ruler = yes` character for AUS, with displayed age 58. Joseph II is preserved as the historical `heir = yes`, age 34, making him a visible secondary dynastic character without occupying a second ruler slot. His obsolete `child` trait was removed. A ruler-scoped government type displays Maria Theresa as Archduchess and Joseph as Archduke instead of presenting her as Holy Roman Emperor.

```text
AUS_STARTING_RULER_COUNT = 1
AUSTRIA_SINGLE_PRIMARY_RULER = YES
JOSEPH_II_SECONDARY_ONLY = YES
```

## 8. Maratha regency

The Victoria 3 1.13 scripts provide a clean regency mechanism: a historical character is created as ruler and designated as regent, the nominal child remains heir, and a regency modifier selects a regency government. Vanilla Korea, Jaipur, Idar, Manipur and Brazil demonstrate this pattern.

The user-authorized Sakharam pass found no reliable exact birth date. The institutional references confirm his senior political role, while NDHistories cautiously places his birth around 1716. The implementation therefore uses `age = 60` on 1 January 1776 and deliberately does not encode an exact date. Sakharam Bapu Bokil is the effective `ruler = yes`, designated regent with `YEARS = 1`; Madhavrao II is the nominal `heir = yes`, born `1774.4.18`, with the child trait. In vanilla 1.13, `YEARS` records completed tenure already served and is incremented annually; it is not a future duration. One completed year is the conservative start-of-1776 encoding for the early regency that followed Madhavrao's 1774 installation.

A country-specific regency government displays Sakharam as `Regent` and Madhavrao as `Peshwa`. A non-regency Peshwa government is available if a later succession script removes the modifier. The landowners regency modifier follows the existing ruling interest group and activates the engine regency trigger.

`Anandrao Dhulap` and `Konkan Flotilla` remain untouched.

```text
MARATH_REGENCY_RESOLVED = YES
```

## 9. Effective vs nominal ruler cases

- MUG uses the historically nominal Shah Alam II because the packet explicitly recommends him for the single ruler slot.
- MYS uses effective ruler Hyder Ali, not the Wodeyar figurehead. A ruler-scoped government displays `Sarvadhikari` and no commander role was added.
- JAP uses Tokugawa Ieharu as Shogun, not the nominal emperor.
- NET uses William V as the single executive abstraction. The inherited anachronistic monarchy and wealth voting were replaced by presidential republic and oligarchy laws; a dedicated hereditary-transfer government displays `Stadtholder`.
- PER retains Karim Khan as ruler and displays `Vakil` only while his historical template is the ruler, avoiding a global Persian-government rewrite.

## 10. Approximate-date cases

No precise date was invented for uncertain cases:

| Tag | Character | Implemented data |
|---|---|---|
| MUG | Shah Alam II | `age = 47` |
| MARATH | Sakharam Bapu Bokil | `age = 60` (external circa 1716 estimate) |
| MYS | Hyder Ali | `age = 55` |
| PER | Karim Khan Zand | `age = 70` |
| MON | Sava II Petrović-Njegoš | `age = 74` |

Montenegro remains marked `RESEARCH_REVISIT_LATER = YES` because the packet's confidence is MEDIUM.

## 11. Naples/Sicily personal-union case

The fork represents mainland Naples with `SIC` and the island of Sicily with `GR3`. In `common/history/diplomacy/00_subject_relationships.txt`, SIC creates a `personal_union` pact with GR3. The character directory contains one Ferdinand, created for SIC with the already correct `1751.1.12` birth date. This matches vanilla's Sweden/Norway pattern: the senior partner creates the monarch, while the personal-union subject does not instantiate a duplicate ruler.

No second Ferdinand was created. The existing single engine-shared monarch resolves both country tags.

```text
NAPLES_SICILY_PERSONAL_UNION_RESOLVED = YES
PERSONAL_UNION_DUPLICATE_CHARACTER_CREATED = NO
```

## 12. Localisation and portraits

English and French name/title/government keys were appended to the existing project localization files. Both files retain UTF-8 BOM and the correct `l_english:` / `l_french:` header. Proper names are transliterated or localized only where the packet already supplies the form.

Existing historical DNA was retained for George III, Louis XVI, Charles III, Stanislaw August and Karim Khan. No compatible local DNA was found for the newly added rulers, so they use procedural portraits. Adult/child visual coherence remains in the condensed user runtime checklist.

## 13. Static validation

- Changed Clausewitz files: balanced braces after comments are excluded.
- Referenced tags, religions, ideologies, law types, government title keys and template IDs exist locally or are defined in this batch.
- Explicit batch rulers: one per implemented independent/senior country; AUS has one; GR3 shares SIC by personal union; MARATH has one effective regent plus one nominal child heir.
- Duplicate template IDs added: 0.
- Duplicate character instantiations added: 0.
- Negative ages: 0.
- Birth dates after `1776.1.1`: 0.
- Packet characters dead before start: 0.
- Vanilla 1836 ruler reintroduction: 0.
- `git diff --check`: PASS.
- Staged paths: 0.
- Metadata, map, army, navy and technology changes attributable to this batch: 0.
- Victoria 3 was not launched by Codex; post-change parser/runtime verification remains required.

The static verdict is PASS. Runtime-dependent displayed titles, procedural portraits and actual one-ruler UI state remain explicitly unclaimed until the user session.

### Batch-1 runtime closure

The user completed the condensed Batch-1 runtime session and confirmed the rulers that were inspected. The Mughal Empire could not be found visually before the game was closed, so its character remains statically validated but its visual/UI observation is explicitly carried into the Batch-2 runtime session.

```text
BATCH1_RUNTIME = PASS_WITH_ONE_DEFERRED_VISUAL_CHECK

MUG_SHAH_ALAM_II_STATIC = PASS
MUG_SHAH_ALAM_II_VISUAL_CHECK = DEFERRED
```

## 14. USER runtime checklist

Use one fresh 1776 session with only the fork enabled:

1. Check the starting ruler, displayed age and adult portrait for: GBR George III 37; FRA Louis XVI 21 and not Emperor; SPA Charles III 59; POR Joseph I 61; RUS Catherine II 46; PRU Frederick II 63; AUS Maria Theresa 58 with Joseph II only as secondary/heir; SWE Gustav III 29; DENNOR Christian VII 26; PLC Stanislaw August 43; TUR Abdülhamid I 50; CHI Hongli/Qianlong 64; JAP Tokugawa Ieharu 38; KOR Yeongjo 81; MUG Shah Alam II 47; HYD Nizam Ali Khan 41; MYS Hyder Ali 55; PER Karim Khan 70; NET William V 27.
2. Check special titles: FRA King, AUS Archduchess, PLC King and Grand Duke, JAP Shogun, MYS Sarvadhikari, PER Vakil, NET Stadtholder, MON Prince-Bishop.
3. Check Naples and Sicily: one Ferdinand, age 24, governing SIC and personal-union subject GR3 without a duplicate character.
4. Check MON Sava II, age 74, and a coherent adult portrait.
5. Check MARATH: Sakharam Bapu Bokil is the Regent at approximate age 60; Madhavrao II is the child heir/Peshwa at age 1; confirm Anandrao Dhulap and Konkan Flotilla still exist.
6. Let several days pass, exit normally, then inspect `error.log`, `debug.log` and `game.log` once for errors attributable to the new character history, government types or localization.

## 15. Deferred issues

- MARATH follow-up: any dynamic succession, exact office transition, majority trigger or Sakharam death handling belongs to a later event/succession batch; `regency_years` only tracks elapsed tenure.
- KOR succession: Yeongjo dies later in 1776; no succession event was created in this starting-ruler batch.
- MON biography: revisit Sava II in a later deep research pass.
- Procedural portraits: visual runtime check only; no custom GFX in this batch.
- Spanish duplicate `Real Armada Española`: documented and deferred to military rebalance.

No CLEANUP-2B-2 work was started.

## 16. Protected-state verification

- The seven technology research files remain untracked, unstaged and untouched.
- BIC retains `activate_law = law_type:law_frontier_colonization` and has no `law_colonial_exploitation` in its country history.
- No entry named exactly `bject` exists outside Git internals.
- `.metadata/metadata.json` is unchanged and still lists exactly the three approved replacement paths.
- No map, army, navy or formation file changed.
- `Anandrao Dhulap`, `Konkan Flotilla`, and the Spanish duplicate naval formations were not edited.
- The index is empty; no Git mutation was performed.

## 17. Verdict

All 23 resolved country tags now have the packet's correct starting ruler representation, including the MARATH regency and the engine-shared SIC/GR3 monarch. No starting-ruler case remains deferred. The batch is statically safe for the single user runtime session, subject to the explicit runtime-only checks above.

```text
HISTORICAL_RESEARCH_PACKET_USED = YES
CODEX_EXTERNAL_HISTORICAL_RESEARCH_PERFORMED = YES

BATCH1_RESEARCH_ENTRIES = 23
BATCH1_COUNTRY_TAGS_RESOLVED = 23
BATCH1_RULERS_IMPLEMENTED = 23
BATCH1_EXISTING_RULERS_CORRECTED = 7
BATCH1_RANDOM_RULERS_REPLACED = 14

BATCH1_NEGATIVE_AGES = 0
BATCH1_BORN_AFTER_START = 0

AUSTRIA_SINGLE_PRIMARY_RULER = YES
JOSEPH_II_SECONDARY_ONLY = YES

MARATH_REGENCY_RESOLVED = YES
NAPLES_SICILY_PERSONAL_UNION_RESOLVED = YES
MONTENEGRO_IMPLEMENTED = YES

V13_STATIC_VALIDATION = PASS

BATCH1_RUNTIME = PASS_WITH_ONE_DEFERRED_VISUAL_CHECK
MUG_SHAH_ALAM_II_STATIC = PASS
MUG_SHAH_ALAM_II_VISUAL_CHECK = DEFERRED

CODEX_LAUNCHED_VICTORIA3 = NO
USER_RUNTIME_REQUIRED = YES

SAFE_FOR_USER_RUNTIME = YES
```

STOP.
