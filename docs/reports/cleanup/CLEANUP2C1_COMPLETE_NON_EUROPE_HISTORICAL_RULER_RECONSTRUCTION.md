# CLEANUP-2C-1 — Complete Non-Europe Historical Ruler Reconstruction

## 1. Baseline

```text
BRANCH = cleanup-post-release
HEAD = fd092a03a5d6cc105e522e2c4bb38e4bc111cce6
INDEX_EMPTY = YES
PRE_EXISTING_CHANGED_OR_UNTRACKED_PATHS = 17
GIT_DIFF_CHECK_BASELINE = PASS
```

The baseline contained one tracked modification, `docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md`, plus 16 untracked paths: the earlier CLEANUP-1D report; the CLEANUP-2C-0 report; the non-Europe research completion report; the SOURCES and CONSTITUTIONAL_NOTES documents; four CLEANUP-2C-0 audit CSVs; and the seven protected technology research files. All were retained. No Git mutation was performed.

## 2. Historical authority packet

The following authority files were read completely before gameplay edits:

- `docs/research/characters/RULERS_1776_NON_EUROPE_MASTER.csv`;
- `docs/reports/cleanup/RULERS_1776_NON_EUROPE_SOURCES.md`;
- `docs/reports/cleanup/RULERS_1776_NON_EUROPE_CONSTITUTIONAL_NOTES.md`.

The task named the latter two under `docs/research/characters`, but those paths did not exist. The supplied same-named untracked files under `docs/reports/cleanup` were used without moving or rewriting them. The CLEANUP-2C research completion report confirms that these files form the intended three-file packet.

Also read were CLEANUP-2C-0, CLEANUP-2B-3, the effective Batch-1 character history, the five existing P0/P2 character/template paths, the target 1.13 colonial-government definitions, and the target regency examples for Spain, Korea, Jaipur, and Brazil.

No external historical research was repeated.

## 3. Packet closure

```text
RESEARCH_PACKET_ROWS_READ = 140
RESEARCH_PACKET_UNIQUE_TAGS = 140
RESEARCH_PACKET_MISSING_TAGS = 0

P0_ROWS_ACCOUNTED = 2
P1_ROWS_ACCOUNTED = 135
P2_ROWS_ACCOUNTED = 3

PACKET_AUTHORIZED_DIRECT_REPRESENTATIONS = 109
INTENTIONAL_PROCEDURAL_OR_STRUCTURAL_DEFERS = 31
```

The eight Batch-1 countries `CHI, JAP, KOR, MUG, MARATH, HYD, MYS, PER` were preserved. All 165 decentralized tags remained outside this phase.

## 4. Implementation architecture

One effective history file contains the 104 direct rulers not already represented by the five critical P0/P2 paths. Each direct person uses the MASTER's exact date when fully supplied, the MASTER's approximate age when only that precision is supported, or no date/age when the packet supplies neither. No exact birthday was reconstructed from an approximate age.

Every direct start character receives the marker `cleanup2c1_historical_office`. A new government file defines 109 tag-specific, marker-gated start governments. The definitions disappear naturally when the packet character leaves office, allowing ordinary engine government selection afterward.

Transfer methods are 78 hereditary, 20 dictatorial/appointed, and 11 presidential-elective. The elective set includes the Continental Congress, Druk Desi, Almamy, Sikh confederal abstraction, HBC company governor, and packet-described royal/confederal selections. No delegated executive is given a royal title.

EN and FR localisation contain 109 ruler names, 109 ruler titles, and the two NAG/TIB heir names and titles. All four newly loaded history/government/localisation files have UTF-8 BOM.

## 5. P0 outcomes

### DEI

The copied `DEI_reinier_exec` template was replaced by `DEI_jeremias_van_riemsdijk`. It now creates Jeremias van Riemsdijk, born `1712.10.18`, as a VOC delegated company executive. The copied BIC DNA, comment, reckless trait, false birth date, and Reinier de Klerk identity are absent. The visible office is `Governor-General of the Dutch East Indies`, with dictatorial/appointed transfer, never monarchy.

### USA

`USA_washington_traitor` was replaced by `USA_john_hancock_continental_congress`. George Washington is no longer instantiated as civil ruler or President. John Hancock, born `1737.1.23`, is the temporary packet-authorized visible abstraction titled `President of the Continental Congress`, with presidential-elective transfer. USA's British-colony/map contradiction remains untouched and deferred.

## 6. P2 outcomes

- `BIC`: Warren Hastings remains the existing company executive. His history creation receives only the start-office marker; the visible title is `Governor-General of Fort William`. BIC country laws were not edited.
- `DUR`: the ruler is now `Timur Shah Durrani`, age 29 from the packet's month-only chronology, titled `Shah`. The previous false exact `1746.8.6` date is removed.
- `IR1`: `Omar Ahmad` is replaced by `Omar Pasha`, titled `Pasha`, with appointed/dictatorial transfer under the existing Ottoman subject context. No birth date or age was invented.

## 7. Direct regional reconstruction

The remaining 104 direct packet decisions were implemented in `cleanup2c1 - non europe rulers 1776.txt`. They include sovereigns, nominal sovereigns, effective ataliq/inaq rulers, appointed governors and viceroys, company executives, local monarchs, religious executives, chiefs, confederal abstractions expressly authorized by the packet, and two regencies.

Specific local offices are retained instead of generic royal titles, including `Asantehene`, `Oba`, `Mbang`, `Omugabe`, `Omukama`, `Mwami`, `Kabaka`, `Mai`, `Faama`, `Kolak`, `Ahosu`, `Almamy`, `Manikongo`, `Ngwenyama`, `Ataliq`, `Inaq`, `Druk Desi`, `Chogyal`, `Jathedar`, `Nawab-Wazir`, `Susuhunan`, `Chhatrapati`, `Garaad`, and `Kaptyn`.

## 8. Delegated executives

Colonial/company and provincial executives use non-hereditary transfer unless the packet identifies a genuinely dynastic delegated office. Examples include van Riemsdijk, Hastings, the Spanish/French/Portuguese/British colonial governors and viceroys, Salah Bey, Ibrahim Bey, Nasr al-Madhkur, Omar Pasha, and Phraya Wichianprakarn.

Hereditary but non-sovereign dynastic dependencies such as Ali I Qaramanli, Ali II ibn Hussein, and Surur ibn Musa'id retain hereditary continuity while their Pasha/Bey/Sharif-Emir titles prevent promotion to king.

## 9. Regencies

NAG and TIB use the target-1.13-proven mechanism only:

```text
set_variable = { name = regency_years value = 1 }
```

The value is a technical start-regency sentinel, not an invented biographical date.

- `NAG`: Mudhoji Bhonsle is the visible Regent; Raghoji II is the historical child heir/nominal Chhatrapati. The packet supplied no exact age or birth date, so none was invented.
- `TIB`: Demo Tulku is the visible Regent; Jamphel Gyatso, 8th Dalai Lama, is the nominal heir. No unsupported birth data was added.

`designate_character_as_regent` has zero active occurrences.

## 10. Exact deferred cases

The following 31 tags deliberately retain engine-generated/procedural officeholders or their existing representation. No historical identity was forced:

| Tag | Packet decision | Deferred reason |
|---|---|---|
| AGC | IDENTITY_RESEARCH_DEFERRED_PROCEDURAL_ALLOWED | Exact Sultan unresolved. |
| AIT | IDENTITY_MAP_REWORK_DEFERRED | Exact Mokrani holder and territorial abstraction unresolved. |
| ALK | MAP_REWORK_DEFERRED | No centralized Russian-American company government in 1776. |
| ARB | MAP_DIPLOMACY_REWORK_DEFERRED | Exact Banu Ka'b holder and false French-vassal abstraction unresolved. |
| BAL | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Multiple Balinese kingdoms; no unitary king. |
| BRG | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Multiple Borgu kingdoms; no unitary king. |
| BST | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Centralized Basotho state is anachronistic. |
| CHC | POLITICAL_STRUCTURE_REWORK_DEFERRED | Collective teip/community authority. |
| CIR | POLITICAL_STRUCTURE_REWORK_DEFERRED | Multiple Circassian princes and communities. |
| DAI | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Multiple Vietnamese regimes during the Tay Son wars. |
| FTR | TRANSITION_1776_IDENTITY_DEFERRED | Day-specific 1776 revolutionary transition unresolved. |
| HAU | IDENTITY_CHRONOLOGY_DEFERRED | Bawa/Gambai accession chronology conflicts. |
| HAW | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Multiple island chiefdoms; no unified kingdom. |
| IQU | MAP_REWORK_DEFERRED | The Iquicha political tag is later than 1776. |
| JMB | IDENTITY_CHRONOLOGY_DEFERRED | Competing Jambi ruler chronologies. |
| KAU | POLITICAL_STRUCTURE_REWORK_DEFERRED | Collective Kaurna local authority. |
| LAN | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Lanfang post-dates the start. |
| MAD | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Multiple Malagasy kingdoms. |
| MJT | IDENTITY_RESEARCH_DEFERRED_PROCEDURAL_ALLOWED | Exact Majeerteen holder unresolved. |
| NBS | MAP_REWORK_DEFERRED | No separate New Brunswick government in 1776. |
| ONT | MAP_REWORK_DEFERRED | No separate Ontario/Upper Canada government in 1776. |
| ORA | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Orange Free State is anachronistic. |
| PHL | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Philippolis polity is anachronistic. |
| SHS | POLITICAL_STRUCTURE_REWORK_DEFERRED | Multiple Shan saophas; no unitary ruler. |
| SIL | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | British Sierra Leone colony post-dates 1776. |
| SOK | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Sokoto Caliphate post-dates 1776. |
| TGI | IDENTITY_RESEARCH_DEFERRED_PROCEDURAL_ALLOWED | Exact Tungi Sultan unresolved. |
| TRN | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | South African Republic is anachronistic. |
| UNT | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | United Tribes government post-dates 1776. |
| UZH | POLITICAL_STRUCTURE_REWORK_DEFERRED | Collective Senior Zhuz authority. |
| WTU | MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED | Witu Sultanate is a later polity. |

## 11. Files modified and created

Modified narrowly:

- `common/character_templates/country_dei.txt`;
- `common/character_templates/country_usa.txt`;
- `common/history/characters/bic - british india.txt`;
- `common/history/characters/dei - dutch east indies.txt`;
- `common/history/characters/dur.txt`;
- `common/history/characters/ir1 - mamluk iraq.txt`;
- `common/history/characters/usa.txt`.

Created:

- `common/history/characters/cleanup2c1 - non europe rulers 1776.txt`;
- `common/government_types/00_cleanup2c1_non_europe.txt`;
- `localization/english/cleanup2c1_non_europe_rulers_l_english.yml`;
- `localization/french/cleanup2c1_non_europe_rulers_l_french.yml`;
- `docs/research/characters/CLEANUP2C1_NON_EUROPE_IMPLEMENTATION_RESULT.csv`;
- this report.

The pre-existing B3 modification and all earlier untracked reports/audits remain outside the new gameplay scope.

## 12. Static validation

```text
RESEARCH_PACKET_ROWS_READ = 140
RESEARCH_PACKET_UNIQUE_TAGS = 140
RESEARCH_PACKET_MISSING_TAGS = 0

P0_ROWS_ACCOUNTED = 2
P1_ROWS_ACCOUNTED = 135
P2_ROWS_ACCOUNTED = 3

BATCH1_VALIDATED_COUNTRIES_PRESERVED = 8
DECENTRALIZED_TAGS_EDITED = 0

DUPLICATE_RULERS_INTRODUCED = 0
DUPLICATE_CHARACTER_INSTANTIATIONS_INTRODUCED = 0
BORN_AFTER_1776_01_01 = 0
DEAD_BEFORE_START = 0
NEGATIVE_AGES = 0

DELEGATED_EXECUTIVE_PROMOTED_TO_MONARCH = 0
DEFERRED_CASES_FORCED_TO_HISTORICAL_IDENTITY = 0
COLLECTIVE_POLITY_FICTIONAL_MONARCHS = 0

ACTIVE_DESIGNATE_CHARACTER_AS_REGENT = 0
INVALID_GOVERNMENT_IDS = 0
MISSING_EN_FR_RULER_TITLE_LOCALISATION = 0
DUPLICATE_LOCALISATION_KEYS_INTRODUCED = 0

DIRECT_CHARACTER_SCOPES = 104
TAG_SPECIFIC_GOVERNMENT_TYPES = 109
EN_FR_LOCALISATION_KEYS_PER_LANGUAGE = 222
FULL_EXACT_BIRTH_DATES_USED = 17
PACKET_APPROXIMATE_AGES_USED = 29
DIRECT_IDENTITIES_WITHOUT_INVENTED_DATE_OR_AGE = 63

V13_STATIC_VALIDATION = PASS
```

The implementation result contains 140 unique rows and marks every row `PASS` for static validation.

## 13. Protected-state verification

The seven technology research files retain their baseline SHA-256 hashes and remain untracked and unstaged. `bject` remains absent. BIC country history retains exactly one `law_frontier_colonization` activation and no `law_colonial_exploitation`.

Metadata retains SHA-256 `F58606B22D954BCACB8FDCEE5ED1CD309A44E6D0F03FF006AFBFD948B100D8DC`; starting states retain `FD9F5F1BFBC7FE47E63C91CFCD29DD357A1B411E58FE80572BADC599A79D941C`. No map, state-region, ownership, province, diplomacy, military-formation, commander, Konkan Flotilla, Anandrao Dhulap, Real Armada Espanola, technology gameplay, or metadata file was changed. The index remains empty.

```text
PROTECTED_TECH_FILES_CHANGED = 0
BJECT_PATH_PRESENT = 0
BIC_FRONTIER_COLONIZATION_PRESERVED = YES
BIC_COLONIAL_EXPLOITATION_PRESENT = NO

MAP_FILES_CHANGED = 0
STATE_REGION_FILES_CHANGED = 0
OWNERSHIP_FILES_CHANGED = 0
MILITARY_FORMATION_FILES_CHANGED = 0

GIT_INDEX_MUTATED_BY_CODEX = NO
CODEX_LAUNCHED_VICTORIA3 = NO
GIT_DIFF_CHECK = PASS
```

## 14. One-session user runtime checklist

Launch one fresh 1776 game with only this fork enabled. Codex did not launch the game.

### Critical corrections

1. `DEI`: Jeremias van Riemsdijk — Governor-General of the Dutch East Indies; no Reinier de Klerk or copied BIC presentation.
2. `USA`: John Hancock — President of the Continental Congress; George Washington must not be President or civil ruler.
3. `BIC`: Warren Hastings — Governor-General of Fort William; delegated company executive, not monarch.
4. `DUR`: Timur Shah Durrani — age about 29 — Shah.
5. `IR1`: Omar Pasha — Pasha; never Omar Ahmad or sovereign monarch.
6. `NAG`: Mudhoji Bhonsle — Regent; Raghoji II present as child heir/nominal Chhatrapati.
7. `TIB`: Demo Tulku — Regent; Jamphel Gyatso, 8th Dalai Lama, present as nominal heir.

### Representative delegated executives

1. `QUE`: Guy Carleton — Governor of Quebec.
2. `SC1`: Antonio Maria de Bucareli y Ursua — Viceroy of New Spain.
3. `PHI`: Simon de Anda y Salazar — Governor-General of the Philippines.
4. `HBC`: Sir Bibye Lake Jr. — Governor of the Hudson's Bay Company.
5. Confirm none is displayed as King, Emperor, Sultan, or other sovereign monarch.

### Representative direct rulers

1. Africa: `ASH` Osei Kwadwo/Asantehene; `ETH` Tekle Haymanot II/Emperor; `OYO` Abiodun/Alaafin; `SWZ` Ngwane III/Ngwenyama.
2. Central Asia: `BUK` Daniyal Biy Ataliq/Ataliq; `KHI` Muhammad Amin Inaq/Inaq; `KZH` Nuraly Khan/Khan.
3. South Asia: `AWA` Asaf-ud-Daula/Nawab-Wazir; `BHU` Kunga Rinchen/Druk Desi; `SAT` Rajaram II/Chhatrapati; `PAN` Jassa Singh Ahluwalia/Jathedar.
4. Southeast Asia: `SIA` Taksin/King; `BUR` Hsinbyushin/King; `SRK` Pakubuwono III/Susuhunan; `YOG` Hamengkubuwono I/Sultan.

### Representative intentional defers

1. `AGC`, `MJT`, or `TGI`: a procedural ruler may exist, but no custom historical identity from CLEANUP-2C-1 should appear.
2. `CHC`, `CIR`, `BRG`, `DAI`, `BAL`, and `SHS`: no CLEANUP-2C-1 fictional unitary monarch.
3. `ALK`, `NBS`, `ONT`, `IQU`, `SIL`, `SOK`, `LAN`, `WTU`: no later historical governor/founder projected into 1776.
4. `HAW`, `KAU`, and `UNT`: no custom unified monarch created by this phase.

Let several days pass. Reload countries or a save within the same session if useful, then quit normally once. Inspect fresh `error.log`, `debug.log`, and `game.log` for:

```text
UNKNOWN_EFFECT_OR_TRIGGER_CLEANUP2C1 = 0
UNKNOWN_GOVERNMENT_ID_CLEANUP2C1 = 0
MISSING_LOCALISATION_CLEANUP2C1 = 0
BOM_WARNING_CLEANUP2C1_CHARACTER = 0
BOM_WARNING_CLEANUP2C1_GOVERNMENT = 0
BOM_WARNING_CLEANUP2C1_EN = 0
BOM_WARNING_CLEANUP2C1_FR = 0
ATTRIBUTABLE_CHARACTER_ERRORS = 0
ATTRIBUTABLE_GOVERNMENT_ERRORS = 0
ATTRIBUTABLE_LOCALISATION_ERRORS = 0
```

## 15. Verdict

CLEANUP-2C-1 implements every packet-authorized historical ruler/executive and preserves every explicit uncertainty. The 31 unresolved identities/structures remain classified, procedural, and ready for later map/political work. The implementation is statically ready for the user's one condensed runtime; no commit, push, runtime, map rework, commander phase, portrait work, or technology work was performed.

```text
CLEANUP2C1_STATIC = PASS
USER_RUNTIME_REQUIRED = YES
SAFE_FOR_SINGLE_FINAL_NON_EUROPE_RUNTIME = YES
CODEX_LAUNCHED_VICTORIA3 = NO
GIT_INDEX_MUTATED_BY_CODEX = NO
```

STOP.
