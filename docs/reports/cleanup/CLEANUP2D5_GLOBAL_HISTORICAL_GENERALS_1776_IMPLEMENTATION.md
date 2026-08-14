# CLEANUP-2D-5 — Global historical generals 1776 — implementation report

## Status

`STATIC_VALIDATION = PASS`

`RUNTIME = PASS`

No Victoria 3 session was launched. No commit, push, or staging operation was performed.

## Baseline and result

| Item | Value |
|---|---:|
| Initial HEAD | `66ed0fc4ef838a54a19810496a5b7d005fde120d` |
| Final HEAD | `66ed0fc4ef838a54a19810496a5b7d005fde120d` |
| Canonical land formations | 214 |
| Researched formations | 214 |
| Research gaps | 0 |
| Historical generals before | 18 |
| Historical generals after | 79 |
| Procedural generals before | 196 |
| Procedural generals after | 135 |
| Existing people reused as ruler/general | 20 |
| Duplicate historical people created | 0 |

The final total was calculated from the 214-row global matrix after resolving overlaps and confirming that Victoria 3 1.13 supports `ruler = yes` and `is_general = yes` on the same character. Consequently, none of the selected dual-role cases required a `DUAL_ROLE_ENGINE_BLOCKER` fallback.

## Implementation summary

The eight CLEANUP-2D-4 military formation files retain their formation, unit, fleet, scope, and transfer architecture. Historical profiles replace only the selected general character blocks. Existing governors, rulers, and military-political officeholders are reused through a unique saved character scope and attached to the existing formation scope.

Historical profiles now use source-supported culture, religion, birth information, and origin state where the corresponding Victoria 3 token is valid and the mapping is sufficiently safe. Unknown or disputed data remains unset. Washington alone reuses an exact DNA asset.

## Rebuilt CLEANUP-2D-4 profiles

The same historical person remains selected, but the procedural biography was rebuilt for:

- Franciszek Ksawery Branicki; William Howe; Pyotr Rumyantsev; Antonio Ricardos; George Washington;
- Jassa Singh Ahluwalia; John Clavering; Haripant Phadke; Tukoji Holkar; Mahadji Shinde; Hyder Ali;
- Eustachius De Lannoy; Mirza Najaf Khan; Maha Thiha Thura; Chao Phraya Chakri (Thongduang).

Washington now has `birth_date = 1732.2.22`, `home_region = STATE_VIRGINIA`, `cu:dixie`, `rel:protestant`, `ig_armed_forces`, and `dna = dna_washington_traitor`. His age on 1776-01-01 is therefore 43.

## Replaced or remapped CLEANUP-2D-4 selections

| Record | Before | After | Resolution |
|---|---|---|---|
| `GEN1776-009` | Andreas Hadik | Gabriel Splényi von Miháldy | Bukovina/Balkan formation receives Splényi. |
| `GEN1776-011` | Franz Moritz von Lacy | Andreas Hadik von Futak | Hadik moves to central Austrian higher-command abstraction; Lacy is absent as a starting general. |
| `GEN1776-066` | Alejandro O'Reilly | Félix O'Neille y O'Neille | 1776 Spanish command evidence favors O'Neille. |

## Procedural formations converted to historical

Sixty-one previously procedural formation slots became historical:

- Central/Western Europe: Friedrich Ehrenreich von Ramin, Friedrich Christoph von Saldern, Wichard Joachim Heinrich von Möllendorff, Friedrich Bogislaw von Tauentzien, Joseph Šišković, Giovanni Battista Serbelloni, Claude-Louis-Robert de Saint-Germain, Louis-Georges-Érasme de Contades, Louis-François-Armand de Vignerot du Plessis, Vital-Auguste de Grégoire de Nozières, Jeffery Amherst, George Augustus Eliott, Heinrich Christoph von Baudissin, August Friedrich von Spörcken, Lodewijk Ernst van Brunswijk-Wolfenbüttel, Joseph-Jean-François de Ferraris, Duarte António da Câmara, and José Francisco Antonio Solano y Bote.
- Northern/Eastern Europe: Grigory Potemkin, Johann Clapier de Colongue, and Georg Magnus Sprengtporten.
- Americas: Victor-Thérèse Charpentier d'Ennery, Felipe de Fonsdeviela y Ondeano, Miguel de Muesas, Tempest, João Henrique Böhm, José Diguja, and Manuel de Guirior.
- Africa: Ibrahim Bey of Mascara, Salah Bey, Sidi Tahar ben Abdelhaq Fennich, Wand Bewossen, Ibrahima Sori Mawdo, Sira Bo Kulibali, Ngolo Diarra, and Ngwane III.
- Middle East/Central Asia: Süleyman Ağa, Moḥammad Ṣādeq Khan Zand, Tīmūr Shah Dorrānī, Sharīf Surūr ibn Musāʿid, Daniyal Biy, Muhammad Amin Inaq, and Ablai Khan.
- South Asia: Robert Fletcher, James Stuart, Mudhoji Bhonsle, and Tipu Sultan.
- East/Southeast Asia: Fengshenge, Agūi, Fuyu, Mingliang, Qilikeqi, Wufu, Hailancha, Techenge, Simón de Anda y Salazar, Kuze Hiroaki, and Raja Haji Fisabilillah.
- CLEANUP-2D-5M catch-up: George Browne on UBD, Gu Seon-bok on KOR, and Abhiman Singh Basnyat on NEP.

Two further new identities, Gabriel Splényi and Félix O'Neille, replace previously historical selections as documented above. Hadik is an existing identity remapped between Austrian formations.

## Existing characters reused rather than duplicated

The following 20 existing characters receive the military role and formation attachment directly:

- Daniyal Biy; Muhammad Amin Inaq; Ablai Khan;
- Victor-Thérèse Charpentier d'Ennery; Felipe de Fonsdeviela y Ondeano; Miguel de Muesas; Manuel de Guirior;
- Salah Bey; Tīmūr Shah Dorrānī; Sharīf Surūr ibn Musāʿid;
- Jassa Singh Ahluwalia; Mahadji Shinde; Mudhoji Bhonsle; Hyder Ali;
- Simón de Anda y Salazar; Ibrahima Sori Mawdo; Sira Bo Kulibali; Ngolo Diarra; Ngwane III.
- George Browne, whose existing UBD ruler instance is also the UBD general.

Each has one character definition, one unique character scope, and one transfer to the existing CLEANUP-2D-4 formation. The duplicate/reuse audit records the source file and method for every final historical person.

## Global overlap resolutions

- `GEN1776-018` FRA colonial uses Nozières from 2D5A; d'Ennery is used only by HAI.
- `GEN1776-088` HAI reuses d'Ennery; no French duplicate exists.
- `GEN1776-022` GBR Bahamas remains procedural; Montfort Browne is rejected.
- `GEN1776-067` SPA Caribbean uses José Solano y Bote; Fonsdeviela is used only by CUB.
- `GEN1776-023` GBR South India remains procedural; John Clavering exists only on BIC `Bengal_Army`.
- `GEN1776-046` LUX and `GEN1776-072` GAL remain procedural.
- `GEN1776-029` CIR and `GEN1776-030` CHC remain procedural collective abstractions. `Murtazeki` is reported as nomenclature debt and is not renamed.
- `GEN1776-182` AGC uses the canonical `army_of_angoche` formation and remains procedural collective; the stale Africa key was not recreated.

Rejected/deferred starting identities were not reintroduced: Alexander Suvorov, Montfort Browne, the three old anachronistic Prussian names, Rochambeau, Luo Fangbo on LAN, Kawila on CMI, and Mangkunegara I on SRK. Salah Bey is implemented only on CON under the 2D5F `THEATRE_COMMAND` decision.

## Birth and origin audit

| Encoding outcome | Count |
|---|---:|
| Exact source/existing date encoded | 32 |
| Age used without inventing month/day | 24 |
| Date and age left unset for insufficient precision | 23 |
| Safe `home_region` encoded | 38 |
| Origin state left unset | 41 |
| Fake exact dates | 0 |
| Baptisms used as births | 0 |

John Clavering's 1722 baptism and João Henrique Böhm's 1708 baptism were not encoded as birth dates. Disputed or approximate cases such as Tukoji Holkar, Maha Thiha Thura, Raja Haji, Ablai Khan, Süleyman Ağa, and unknown Central Asian births receive no fabricated exact date. The full historical place and proposed regional mapping remain available in the reconciliation and birth-data audits even when no `home_region` was written.

## CLEANUP-2D-5M catch-up closure

The supplementary closed research packet resolves all nine former gaps:

| Record | Tag | Final research decision | Gameplay result |
|---|---|---|---|
| `GEN1776-051` | WAL | `KEEP_PROCEDURAL` | Existing procedural general retained. |
| `GEN1776-052` | MON | `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE` | Existing procedural clan/tribal abstraction retained. |
| `GEN1776-053` | MOL | `KEEP_PROCEDURAL` | Existing procedural general retained. |
| `GEN1776-068` | UBD | `REUSE_EXISTING_HISTORICAL_CHARACTER_AS_GENERAL` | Existing George Browne ruler reused as the formation general. |
| `GEN1776-069` | BHU | `KEEP_PROCEDURAL_PENDING_STRUCTURE_REWORK` | Existing procedural general retained. |
| `GEN1776-076` | KOR | `IMPLEMENT_NAMED_HISTORICAL_GENERAL` | Gu Seon-bok implemented. |
| `GEN1776-080` | NEP | `IMPLEMENT_NAMED_HISTORICAL_GENERAL` | Abhiman Singh Basnyat implemented. |
| `GEN1776-083` | SIK | `KEEP_PROCEDURAL` | Existing procedural general retained. |
| `GEN1776-085` | TIB | `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE` | Existing procedural collective-high-command abstraction retained. |

George Browne remains one character with `ruler = yes` and `is_general = yes`. His existing `birth_date = 1698.6.15` is preserved as the sourced Old Style date; the Gregorian 1698-06-25 conversion is documented only. His ruler-level `ig_landowners` and `ideology_moderate` remain under `DUAL_ROLE_CHARACTER_LEVEL_PROFILE_CONSTRAINT`, while culture, religion, and origin are corrected to Irish, Catholic, and `STATE_MUNSTER`.

Gu Seon-bok and Abhiman Singh Basnyat use `age = 57` and `age = 31` respectively, preserving their YEAR-only source precision without fabricated month/day. Gu has no invented birthplace; Basnyat uses the validated `STATE_HIMALAYAS` mapping. The research label `experienced_commander` is not a valid Victoria 3 1.13 trait token, so no fictional trait definition or guessed substitute was encoded.

## Static validation

`python tools/cleanup2d5_validate.py` reports:

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
REJECTED_CANDIDATES_REINTRODUCED = 0
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

All 41 fleet blocks and all five admiral character blocks compare unchanged with HEAD after whitespace normalization. The five admiral transfers are still present. No protected technology path appears in the tracked diff, and the index is empty.

## Files changed by CLEANUP-2D-5

Gameplay/history:

- `common/history/military_formations/00_military_formations_europe.txt`
- `common/history/military_formations/01_military_formations_north_america.txt`
- `common/history/military_formations/02_military_formations_south_america.txt`
- `common/history/military_formations/03_military_formations_north_africa.txt`
- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/military_formations/05_military_formations_india.txt`
- `common/history/military_formations/06_military_formations_asia.txt`
- `common/history/military_formations/07_military_formations_subsaharan_africa.txt`
- `common/history/characters/cleanup2b1 - major rulers 1776.txt`
- `common/history/characters/cleanup2b3 - residual europe rulers 1776.txt`
- `common/history/characters/cleanup2c1 - non europe rulers 1776.txt`
- `common/history/characters/dur.txt`
- `localization/english/cleanup2d5_generals_l_english.yml`
- `localization/french/cleanup2d5_generals_l_french.yml`

Required outputs and deterministic controls:

- `docs/reports/cleanup/CLEANUP2D5_GLOBAL_HISTORICAL_GENERALS_1776_IMPLEMENTATION.md`
- `docs/reports/cleanup/CLEANUP2D5N_2D5M_RESEARCH_GAP_IMPLEMENTATION_CATCHUP.md`
- `docs/research/military/CLEANUP2D5_GLOBAL_RECONCILIATION_MATRIX.csv`
- `docs/research/military/CLEANUP2D5_DUPLICATE_PERSON_REUSE_AUDIT.csv`
- `docs/research/military/CLEANUP2D5_BIRTHDATA_IMPLEMENTATION_AUDIT.csv`
- `docs/research/military/CLEANUP2D5_RESEARCH_COVERAGE_GAPS.md`
- `tools/cleanup2d5_build_audits.py`
- `tools/cleanup2d5_apply_profiles.py`
- `tools/cleanup2d5_validate.py`

Closed regional source packet added under `docs/research/military/cleanup2d5_regional_sources/`:

- `CLEANUP2D5A_NORTH_AMERICA_CARIBBEAN_HISTORICAL_GENERALS.md` and `GENERALS_1776_NORTH_AMERICA_CARIBBEAN_IMPLEMENTATION.csv`
- `CLEANUP2D5B_WESTERN_EUROPE_HISTORICAL_GENERALS.md` and `GENERALS_1776_WESTERN_EUROPE_IMPLEMENTATION.csv`
- `CLEANUP2D5C_CENTRAL_EUROPE_HISTORICAL_GENERALS.md` and `GENERALS_1776_CENTRAL_EUROPE_IMPLEMENTATION.csv`
- `CLEANUP2D5D_NORTHERN_EASTERN_EUROPE_HISTORICAL_GENERALS.md` and `GENERALS_1776_NORTHERN_EASTERN_EUROPE_IMPLEMENTATION.csv`
- `CLEANUP2D5E_SOUTH_AMERICA_HISTORICAL_GENERALS.md` and `GENERALS_1776_SOUTH_AMERICA_IMPLEMENTATION.csv`
- `CLEANUP2D5F_AFRICA_HISTORICAL_GENERALS.md` and `GENERALS_1776_AFRICA_IMPLEMENTATION.csv`
- `CLEANUP2D5G_MIDDLE_EAST_CAUCASUS_HISTORICAL_GENERALS.md` and `GENERALS_1776_MIDDLE_EAST_CAUCASUS_IMPLEMENTATION.csv`
- `CLEANUP2D5H_SOUTH_ASIA_HISTORICAL_GENERALS.md` and `GENERALS_1776_SOUTH_ASIA_IMPLEMENTATION.csv`
- `CLEANUP2D5I_CENTRAL_ASIA_HISTORICAL_GENERALS.md` and `GENERALS_1776_CENTRAL_ASIA_IMPLEMENTATION.csv`
- `CLEANUP2D5J_EAST_ASIA_HISTORICAL_GENERALS.md` and `GENERALS_1776_EAST_ASIA_IMPLEMENTATION.csv`
- `CLEANUP2D5K_SOUTHEAST_ASIA_HISTORICAL_GENERALS.md` and `GENERALS_1776_SOUTHEAST_ASIA_IMPLEMENTATION.csv`
- `CLEANUP2D5L_OCEANIA_HISTORICAL_GENERALS.md` and `GENERALS_1776_OCEANIA_IMPLEMENTATION.csv`
- `CLEANUP2D5M_RESEARCH_COVERAGE_GAPS_HISTORICAL_GENERALS.md` and `GENERALS_1776_RESEARCH_COVERAGE_GAPS_IMPLEMENTATION.csv`
- `README.md`

The pre-existing modification to `docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md` and the pre-existing untracked cleanup/hotfix/technology files were preserved and are not part of CLEANUP-2D-5.

## One-session runtime checklist

1. Start one new game on 1776-01-01 and watch character/formation/localization errors.
2. Verify Washington (age 43, Virginia, DNA), the North American/Caribbean overrides, representative French/Prussian/Austrian/Russian/Spanish profiles, and Clavering only on BIC Bengal Army.
3. Verify De Lannoy as Flemish/Catholic, Najaf Khan as Persian/Shiite, Hyder and Tipu as Deccani/Sunni, at least three Qing commanders, Chakri, Maha Thiha Thura, Simón de Anda, and Raja Haji.
4. Verify at least one reused ruler/general in each relevant region and confirm that no duplicate person appears.
5. Verify UBD George Browne as one ruler/general instance with no clone; verify Gu Seon-bok on KOR and Abhiman Singh Basnyat on NEP with their documented ages and formation attachments.
6. Verify procedural controls: GBR Bahamas, DENNOR, SWI, CIR, CHC, an African collective case, KOK, JAP Edo Guard, plus MON or TIB as a researched 2D5M collective structure.
7. Save and reload in the same session; recheck Washington, one French general, one Prussian, Hadik, Clavering, De Lannoy, one Qing commander, Chakri, Browne, Gu or Basnyat, one other reused ruler/general, and one deliberate procedural case.

Runtime 1776-01-01: PASS.
Save/reload: PASS.
Armies and historical characters persisted after reload.
Washington: historical DNA correctly applied; historical wardrobe remains deferred.
George Browne: single ruler/general instance confirmed.
KOR/NEP and representative global sample: PASS.