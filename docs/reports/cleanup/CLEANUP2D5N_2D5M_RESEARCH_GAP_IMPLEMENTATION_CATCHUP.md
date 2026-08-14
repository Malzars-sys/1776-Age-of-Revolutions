# CLEANUP-2D-5N — 2D5M research-gap implementation catch-up

## Status

`STATIC_VALIDATION = PASS`

`RUNTIME = RUNTIME_PENDING_USER_SESSION`

Victoria 3 was not launched. No commit, push, or staging operation was performed.

## Before and after

| Metric | Before | After |
|---|---:|---:|
| Research coverage | 205/214 | 214/214 |
| Research gaps | 9 | 0 |
| Historical generals | 76 | 79 |
| Procedural generals | 138 | 135 |
| Procedural-to-historical conversions | 58 | 61 |
| Existing ruler/general people reused | 19 | 20 |
| Duplicate historical people | 0 | 0 |
| Exact source/existing birth dates | 31 | 32 |
| YEAR/range profiles encoded with `age` | 22 | 24 |
| Safe `home_region` profiles | 36 | 38 |

The canonical matrix remains exactly 214 rows and 214 unique formations.

## Nine 2D5M decisions

| Record | Tag | Research decision | Final gameplay |
|---|---|---|---|
| `GEN1776-051` | WAL | `KEEP_PROCEDURAL` | Existing procedural unchanged. |
| `GEN1776-052` | MON | `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE` | Existing procedural unchanged. |
| `GEN1776-053` | MOL | `KEEP_PROCEDURAL` | Existing procedural unchanged. |
| `GEN1776-068` | UBD | `REUSE_EXISTING_HISTORICAL_CHARACTER_AS_GENERAL` | George Browne reused. |
| `GEN1776-069` | BHU | `KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK` | Existing procedural unchanged. |
| `GEN1776-076` | KOR | `IMPLEMENT_NAMED_HISTORICAL_GENERAL` | Gu Seon-bok implemented. |
| `GEN1776-080` | NEP | `IMPLEMENT_NAMED_HISTORICAL_GENERAL` | Abhiman Singh Basnyat implemented. |
| `GEN1776-083` | SIK | `KEEP_PROCEDURAL` | Existing procedural unchanged. |
| `GEN1776-085` | TIB | `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE` | Existing procedural unchanged. |

WAL, MON, MOL, BHU, SIK, and TIB retain their exact CLEANUP-2D-4 procedural character creation and attachment blocks. Only their research status and audit documentation changed.

## Three gameplay changes

### UBD — George Browne

The existing George Browne in `cleanup2b3 - residual europe rulers 1776.txt` is the sole instance. It now has `is_general = yes`, one saved reuse scope, and one transfer to `cleanup2d4_formation_068`, while retaining `ruler = yes`. The old procedural `cleanup2d4_general_068` is absent.

- `birth_date = 1698.6.15` preserved as Old Style;
- Gregorian 1698-06-25 documented without silent substitution;
- `culture = cu:irish`;
- `religion = rel:catholic`;
- `home_region = STATE_MUNSTER`;
- ruler `ig_landowners` and `ideology_moderate` preserved under `DUAL_ROLE_CHARACTER_LEVEL_PROFILE_CONSTRAINT`;
- no clone and no invented DNA.

### KOR — Gu Seon-bok / 구선복 (具善復)

`cleanup2d3b_kor_land_1` now receives one historical Gu Seon-bok character with `culture = cu:korean`, `age = 57`, `ig_armed_forces`, and no fixed religion, birthplace, or DNA. The YEAR-only source `1718` is not converted to a fake exact date.

### NEP — Abhiman Singh Basnyat / अभिमान सिंह बस्न्यात

`cleanup2d3b_nep_land_1` now receives one historical Abhiman Singh Basnyat character with `culture = cu:nepali`, `home_region = STATE_HIMALAYAS`, `age = 31`, `ig_armed_forces`, and no fixed religion or DNA. The YEAR-only source `1744` is not converted to a fake exact date.

The 2D5M research label `experienced_commander` is not a valid Victoria 3 1.13 character-trait token. It remains documented rather than being encoded as an invalid token or replaced by an unsupported guess.

## Deterministic sources and outputs

The two user-provided 2D5M files were copied byte-for-byte into `docs/research/military/cleanup2d5_regional_sources/`; SHA-256 hashes match their originals in Downloads. The regional README, global matrix, duplicate/reuse audit, birth-data audit, research-coverage closure document, and both CLEANUP-2D-5 reports were updated.

The deterministic tools now regenerate the closed state:

- `tools/cleanup2d5_build_audits.py` reads 2D5M and produces 214/214 coverage;
- `tools/cleanup2d5_apply_profiles.py` applies Browne reuse and the Gu/Basnyat profiles;
- `tools/cleanup2d5_validate.py` enforces the global and targeted invariants.

Gameplay/localization changes specific to this catch-up are limited to:

- `common/history/military_formations/00_military_formations_europe.txt`;
- `common/history/characters/cleanup2b3 - residual europe rulers 1776.txt`;
- `localization/english/cleanup2d5_generals_l_english.yml`;
- `localization/french/cleanup2d5_generals_l_french.yml`.

No other regional formation receives a new catch-up delta.

## Static validation

```text
GLOBAL_RECONCILIATION_ROWS = 214
GLOBAL_RECONCILIATION_UNIQUE_FORMATIONS = 214
RESEARCH_COVERED_FORMATIONS = 214
RESEARCH_GAP_FORMATIONS = 0
LAND_FORMATIONS = 214
FORMATIONS_WITH_EXACTLY_ONE_GENERAL = 214
FORMATIONS_WITHOUT_GENERAL = 0
FORMATIONS_WITH_MULTIPLE_GENERALS = 0
HISTORICAL_GENERALS = 79
PROCEDURAL_GENERALS = 135
PROCEDURAL_TO_HISTORICAL_CONVERSIONS = 61
EXISTING_PEOPLE_REUSED_AS_RULER_GENERAL = 20
DUPLICATE_HISTORICAL_PERSONS = 0
ORPHAN_TRANSFERS = 0
DUPLICATE_CHARACTER_SCOPES = 0
FAKE_EXACT_BIRTH_DATES = 0
BAPTISM_AS_BIRTH_DATE = 0
WASHINGTON_DNA = dna_washington_traitor
FLEETS = 41
ADMIRALS = 5
ADMIRAL_TRANSFERS = 5
REGULAR_TOTAL = 2557
CONSCRIPT_TOTAL = 1705
NAVAL_TOTAL = 370
PROTECTED_TECH_FILES_CHANGED = 0
PROTECTED_TECH_FILES_STAGED = 0
LOCALIZATION_EN_FR = PASS
STATIC_VALIDATION = PASS
git diff --check = PASS
```

All 41 fleet blocks, all five admiral character blocks, and all five admiral transfers remain unchanged. The seven protected technology files remain outside the tracked diff, and the Git index remains empty.

## One-session runtime checklist

1. Start one new game on 1776-01-01 and monitor character, formation, and localization errors.
2. Confirm UBD George Browne is the same ruler/general character, attached to the UBD formation, with no clone.
3. Confirm KOR Gu Seon-bok has the correct visible name, Korean culture, coherent age, and formation.
4. Confirm NEP Abhiman Singh Basnyat has the correct visible name, coherent age, formation, and Himalayan origin.
5. Confirm one researched procedural structural control, preferably MON or TIB, remains procedural.
6. Execute the broader CLEANUP-2D-5 checklist, save, reload in the same session, and repeat representative checks.

Until that user-run session succeeds: `RUNTIME = RUNTIME_PENDING_USER_SESSION`.
