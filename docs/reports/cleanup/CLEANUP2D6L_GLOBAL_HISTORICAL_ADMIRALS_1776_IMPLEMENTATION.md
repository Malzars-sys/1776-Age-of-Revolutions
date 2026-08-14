# CLEANUP-2D-6L — Global historical admirals 1776 implementation

## Status

```text
STATIC_VALIDATION = PASS
RUNTIME = RUNTIME_PENDING_USER_SESSION
```

No Victoria 3 runtime was launched. Nothing was staged, committed, or pushed.

## Baseline and scope

Implementation started on branch `cleanup-post-release` at exact HEAD `d91bbdbdc5778e259fa9648eca5e0df8d710c30d`, with an empty index. Pre-existing unrelated tracked and untracked work was preserved.

The eight production formation files were parsed before editing:

```text
CURRENT_FLEETS = 41
NAVAL_UNITS = 370
LAND_FORMATIONS = 214
REGULAR_TOTAL = 2557
CONSCRIPT_TOTAL = 1705
```

The supplied global reconciliation matrix is the final authority. It supersedes the obsolete 2D-6J documentary-coverage status and the older regional disagreements explicitly identified in the matrix.

## Research coverage and decisions

```text
GLOBAL_RECONCILIATION_ROWS = 41
GLOBAL_RECONCILIATION_UNIQUE_FLEETS = 41
RESEARCH_COVERED_FLEETS = 41
RESEARCH_GAP_FLEETS = 0

FINAL_FIXED_HISTORICAL_ADMIRALS = 26
IMPLEMENT_NAMED_HISTORICAL_ADMIRALS = 25
REBUILT_EXISTING_HISTORICAL_ADMIRALS = 1

KEEP_NO_FIXED_STARTING_ADMIRAL = 12
COLLECTIVE_COMMAND_NO_SINGLE_ADMIRAL = 1
DEFER_STRUCTURE_REWORK = 2
```

The 12 no-fixed formations remain genuinely without a scripted admiral: GEN, AUS, the French Central-America abstraction, the British East-Africa abstraction, SIC, PAP, POR Lisbon, both Spanish home fleets, TUN, TRI, and TRA. NAV1776-024 remains collective Dutch command without an individual. BRZ and SC4 remain deferred and receive neither Robert MacDouall nor Juan Antonio Camino.

## Implemented historical admirals

| ID | Formation | Historical commander | Final rank |
|---|---|---|---|
| NAV1776-002 | VEN `merchant_venice_fleet` | Antonio Renier | rank 1 |
| NAV1776-004 | FRA `cleanup2d3b_fra_naval_2` | Paul-Hippolyte de Beauvilliers, marquis de La Ferté-Saint-Aignan | rank 1 |
| NAV1776-005 | FRA `cleanup2d3b_fra_naval_1` | Louis Guillouet, comte d'Orvilliers | rank 2 |
| NAV1776-007 | GBR `Mediterranean_Station` | Robert Man (elder) | rank 1 |
| NAV1776-008 | GBR `North_America_and_West_Indies_Station` | Samuel Graves | rank 1 |
| NAV1776-010 | GBR `cleanup2d3b_gbr_naval_5` | Edward Hughes | rank 1 |
| NAV1776-011 | GBR `cleanup2d3b_gbr_naval_1` | Sir James Douglas | rank 3 |
| NAV1776-012 | GBR `cleanup2d3b_gbr_naval_2` | John Amherst | rank 2 |
| NAV1776-013 | GBR `cleanup2d3b_gbr_naval_7` | George Mackenzie | rank 1 |
| NAV1776-014 | RUS `cleanup2d3b_rus_naval_1` | Samuil Karlovich Greig | rank 2 |
| NAV1776-015 | RUS `cleanup2d3b_rus_naval_2` | Alexei Naumovich Senyavin | rank 1 |
| NAV1776-016 | SWE `cleanup2d3b_swe_naval_2` | Henrik af Trolle | rank 1 |
| NAV1776-017 | SWE `cleanup2d3b_swe_naval_1` | Carl Tersmeden | rank 1 |
| NAV1776-018 | DENNOR `Kongelige_Danske_Marine` | Frederik Christian Kaas | rank 1 |
| NAV1776-020 | SAR `Marina_del_Regno_di_Sardegna` | Francesco Maria De Nobili | rank 1 |
| NAV1776-022 | TUS `Marina_del_Granducato_di_Toscana` | John Francis Edward Acton | rank 1 |
| NAV1776-023 | NET `cleanup2d3b_net_naval_2` | Andries Hartsinck | rank 1 |
| NAV1776-025 | POR `cleanup2d3b_por_naval_2` | Roberto Macdouall | rank 1 |
| NAV1776-027 | SPA `cleanup2d3b_spa_naval_3` | Juan Bautista Bonet Arniaud | rank 1 |
| NAV1776-030 | USA `cleanup2d3b_usa_naval_1` | Esek Hopkins | rank 1 |
| NAV1776-035 | TUR `Donanmay_Humyn` | Cezayirli Gazi Hasan Paşa | rank 1 |
| NAV1776-036 | OMA `Bahriat_alMasqat` | Hilāl ibn Aḥmad ibn Saʿīd al-Būsaʿīdī | rank 1 |
| NAV1776-037 | MARATH `Konkan_Flotilla` | Anandrao Dhulap | rank 1 |
| NAV1776-039 | CHI `cleanup2d3b_chi_naval_1` | Li Fengyao | rank 1 |
| NAV1776-040 | CHI `cleanup2d3b_chi_naval_2` | Zhang Shen | rank 1 |
| NAV1776-041 | DEI `Koloniale_Marine` | Assuerus van den Bergh | rank 1 |

Each final historical person has one character instance, one character scope, and one formation transfer. No fleet receives multiple fixed admirals.

## Treatment of the five initial attachments

- NAV1776-028: the unnamed Spanish procedural admiral aged 35, its transfer, and obsolete scopes were removed. No replacement was created.
- NAV1776-029: the unnamed Spanish procedural admiral aged 31, its transfer, and obsolete scopes were removed. No replacement was created.
- NAV1776-037: the existing `MARATH_anandrao_dhulap` template and existing transfer were reused exactly once. The template now pins naval rank 1. Its age and `STATE_BOMBAY` remain explicitly documented as technical gameplay mappings, not sourced birth data.
- NAV1776-039: Guan Tianpei was removed from the starting setup and replaced once by Li Fengyao.
- NAV1776-040: Chen Huacheng was removed from the starting setup and replaced once by Zhang Shen.

```text
STARTING_GUAN_TIANPEI = 0
STARTING_CHEN_HUACHENG = 0
SPANISH_PROCEDURAL_STARTING_ADMIRALS = 0
ANANDRAO_DHULAP_INSTANCES = 1
```

## Edward Hughes reuse/create preflight

A repo-wide gameplay search found no active exact Edward Hughes character or reusable exact template/DNA. The only older material was research/localization provenance, while the canonical setup had no Hughes attachment. One inline historical instance was therefore created and transferred only to NAV1776-010. No BIC/Bombay Marine mapping was introduced.

## Birth data and precision

Exact supported dates were encoded for NAV1776-004, 005, 008, 014, 015, 016, 017, 018, 023, and 030. Greig and Senyavin retain their documented Old Style date in script, with the calendar conflict preserved in comments and the audit.

Year-only, approximate-year, month-only, and circa evidence was represented only by the already validated conservative age convention. No artificial January 1 or first day of a month was created. Terminus-ante-quem and unknown records received no derived exact date. Dhulap's existing age 40 remains a clearly labelled technical approximation.

```text
BIRTHDATA_IMPLEMENTATION_AUDIT_ROWS = 26
FAKE_EXACT_BIRTH_DATES = 0
BAPTISM_AS_BIRTH_DATE = 0
```

## Culture, religion, traits, DNA, and portraits

Only culture/religion values locked by the supplied profile matrix were encoded as historical fields. When culture was `UNSET`, the character uses `primary_culture` with the explicit comment `TECHNICAL_GAMEPLAY_FALLBACK_NOT_HISTORICAL_CLAIM`. Unsupported religion, ideology, interest-group, and birthplace claims were omitted.

No traits were added. Consequently no unverified research label was converted into a script token, and no trait contributes to command capacity.

No DNA was created or reused. Documented portrait references remain research/audit information only; no statue, later illustration, relative's portrait, or speculative reconstruction was converted into DNA.

All 26 names have dedicated English and French localization, including the final Qing romanizations and required diacritics.

## Naval ranks and deterministic capacity

The audit builder and validator reread local Victoria 3 1.13.10 commander-rank definitions and the no-commander fallback. No remembered constants or trait bonuses are used.

Only four fixed admirals require more than rank 1:

- NAV1776-005: 22 ships, rank 2, guaranteed limit 40;
- NAV1776-011: 50 ships, rank 3, guaranteed limit 60;
- NAV1776-012: 28 ships, rank 2, guaranteed limit 40;
- NAV1776-014: 25 ships, rank 2, guaranteed limit 40.

All other historical admirals use rank 1. The 15 formations without an individual commander contain at most 20 ships and are covered by the deterministic vanilla no-commander limit.

```text
ADMIRAL_COMMAND_CAPACITY_ROWS = 41
ADMIRAL_COMMAND_CAPACITY_SUFFICIENT = 41
ADMIRAL_COMMAND_CAPACITY_INSUFFICIENT = 0
NAVAL_RANK_2_ASSIGNMENTS = 3
NAVAL_RANK_3_ASSIGNMENTS = 1
NAVAL_RANK_4_ASSIGNMENTS = 0
NAVAL_RANK_5_ASSIGNMENTS = 0
```

## Naval and land invariants

All fleet blocks were compared with `d91bbdb` after removing only `save_scope_as`; their HQ, name, ship type, count, and service structure remain identical.

The protected land proof compares every one of the 214 army formation blocks and every `is_general = yes` character block byte-for-byte with `d91bbdb`. This avoids the legacy 2D-5O validator's global commander-rank token count, which necessarily sees the new naval ranks, while preserving a stricter land-only comparison.

```text
CURRENT_FLEETS = 41
NAVAL_UNITS = 370
FLEET_STRUCTURE_CHANGES = 0

LAND_FORMATIONS = 214
LAND_GENERAL_RANKS_CHANGED_BY_2D6 = 0
GENERAL_COMMAND_CAPACITY_SUFFICIENT = 214
GENERAL_COMMAND_CAPACITY_INSUFFICIENT = 0
REGULAR_TOTAL = 2557
CONSCRIPT_TOTAL = 1705
```

The seven protected untracked technology-research files remained byte-identical and unstaged.

## Deterministic tools and audits

- `tools/cleanup2d6_apply_profiles.py` rebuilds the authorized gameplay output from the immutable `d91bbdb` baseline and is idempotent.
- `tools/cleanup2d6_build_audits.py` reparses gameplay, rereads vanilla naval limits, and regenerates all three implementation audits.
- `tools/cleanup2d6_validate.py` regenerates the audits and proves the complete static invariant set.

Generated audit cardinalities:

```text
GLOBAL_RECONCILIATION_ROWS = 41
GLOBAL_HISTORICAL_ADMIRAL_PROFILE_ROWS = 26
DUPLICATE_PERSON_REUSE_AUDIT_ROWS = 26
BIRTHDATA_IMPLEMENTATION_AUDIT_ROWS = 26
ADMIRAL_COMMAND_CAPACITY_ROWS = 41
```

## Files changed by CLEANUP-2D-6L

Gameplay and localization:

- `common/character_templates/country_marath.txt`
- `common/history/military_formations/00_military_formations_europe.txt`
- `common/history/military_formations/01_military_formations_north_america.txt`
- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/military_formations/06_military_formations_asia.txt`
- `localization/english/cleanup2d6_admirals_l_english.yml`
- `localization/french/cleanup2d6_admirals_l_french.yml`

Tools:

- `tools/cleanup2d6_apply_profiles.py`
- `tools/cleanup2d6_build_audits.py`
- `tools/cleanup2d6_validate.py`

Research and reporting:

- `docs/research/military/CLEANUP2D6_GLOBAL_RECONCILIATION_MATRIX.csv`
- `docs/research/military/CLEANUP2D6_GLOBAL_HISTORICAL_ADMIRAL_PROFILES.csv`
- `docs/research/military/CLEANUP2D6_ADMIRAL_COMMAND_RANK_CAPACITY_AUDIT.csv`
- `docs/research/military/CLEANUP2D6_DUPLICATE_PERSON_REUSE_AUDIT.csv`
- `docs/research/military/CLEANUP2D6_BIRTHDATA_IMPLEMENTATION_AUDIT.csv`
- `docs/reports/cleanup/CLEANUP2D6L_GLOBAL_HISTORICAL_ADMIRALS_1776_IMPLEMENTATION.md`

No formation files for South America, North Africa, or Sub-Saharan Africa changed. No technology, event, fleet composition, HQ, building, state, ownership, law, government, diplomacy, or DNA file changed.

## Static validation

Run:

```powershell
python tools/cleanup2d6_validate.py
```

Final result:

```text
STATIC_VALIDATION = PASS
git diff --check = PASS
GIT_INDEX_EMPTY = YES
```

## One-session runtime checklist

Do not split this test across independently initialized sessions.

1. Start Victoria 3 with the mod and begin a new 1776 game.
2. Check FRA NAV1776-005: 22 ships, Louis Guillouet d'Orvilliers, rank 2, no capacity deficit.
3. Check GBR NAV1776-011: 50 ships, James Douglas, rank 3.
4. Check GBR NAV1776-012: 28 ships, John Amherst, rank 2.
5. Check RUS NAV1776-014: 25 ships, Samuil Greig, rank 2.
6. Check USA: Esek Hopkins is attached exactly once.
7. Check SPA naval 1 and 2: no fixed admiral; check naval 3: Bonet is attached.
8. Check MARATH: one Anandrao Dhulap attached to `Konkan_Flotilla`.
9. Check northern CHI: Li Fengyao and no Guan Tianpei.
10. Check southern CHI: Zhang Shen and no Chen Huacheng.
11. Check TUR, OMA, and DEI: Hasan Paşa, Hilāl ibn Aḥmad, and Assuerus van den Bergh respectively.
12. Check NET collective, BRZ, and SC4: no individual admiral.
13. Save, reload in the same session, and recheck at least FRA-005, GBR-011, SPA naval 1, MARATH, CHI north, and OMA.
14. Inspect `error.log` for invalid trait, commander rank, culture/religion, home region, `create_character`, `transfer_to_formation`, and localization errors.

```text
RUNTIME = RUNTIME_PENDING_USER_SESSION
```
RUNTIME = PASS
SAVE_RELOAD = PASS

Runtime note:
The first inspection used an already-initialized game state and therefore
still displayed the pre-2D-6L naval setup. After starting/reinitializing the
1776 setup, the historical admirals loaded correctly. Save/reload preserved
the new assignments.