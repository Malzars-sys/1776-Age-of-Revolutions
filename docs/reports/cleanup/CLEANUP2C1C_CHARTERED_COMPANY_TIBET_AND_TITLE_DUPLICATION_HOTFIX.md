# CLEANUP-2C-1C — Chartered-company initial executives, Tibet and title duplication

## Result

```text
CLEANUP2C1C_STATIC = PASS
CLEANUP2C1C_RUNTIME = USER_RETEST_REQUIRED
```

This phase implements three narrowly scoped corrections:

1. deterministic startup creation of the BIC, DEI and HBC historical company executives through the native company-character path;
2. a startup-safe Tibet regency government plus packet-authorized approximate age for Jamphel Gyatso;
3. removal of the confirmed Bukhara title duplication, with nine uncertain identity/title overlaps deliberately preserved.

Victoria 3 was not launched. No Git mutation was performed.

## 1. Real repository baseline

```text
BRANCH = cleanup-post-release
HEAD = fd092a03a5d6cc105e522e2c4bb38e4bc111cce6
INDEX_EMPTY = YES
GIT_DIFF_CHECK_BASELINE = PASS
```

Initial worktree:

```text
 M common/character_templates/country_bic.txt
 M common/character_templates/country_dei.txt
 M common/character_templates/country_usa.txt
 M "common/history/characters/bic - british india.txt"
 M "common/history/characters/dei - dutch east indies.txt"
 M common/history/characters/dur.txt
 M "common/history/characters/ir1 - mamluk iraq.txt"
 M common/history/characters/usa.txt
 M docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md
?? common/character_templates/cleanup2c1b_company_executives.txt
?? common/government_types/00_cleanup2c1_non_europe.txt
?? "common/history/characters/cleanup2c1 - non europe rulers 1776.txt"
?? docs/reports/cleanup/CLEANUP1C1_MARATH_NAVAL_CREW_DIAGNOSTIC.md
?? docs/reports/cleanup/CLEANUP2C0_COMPLETE_NON_EUROPE_ACTIVE_COUNTRY_AUDIT.md
?? docs/reports/cleanup/CLEANUP2C1B_RUNTIME_NAMES_TITLES_AND_CHARTERED_COMPANIES_HOTFIX.md
?? docs/reports/cleanup/CLEANUP2C1_COMPLETE_NON_EUROPE_HISTORICAL_RULER_RECONSTRUCTION.md
?? docs/reports/cleanup/CLEANUP2C_RESEARCH_COMPLETE_NON_EUROPE_RULERS_1776.md
?? docs/reports/cleanup/RULERS_1776_NON_EUROPE_CONSTITUTIONAL_NOTES.md
?? docs/reports/cleanup/RULERS_1776_NON_EUROPE_SOURCES.md
?? docs/research/characters/CLEANUP2C1B_RUNTIME_HOTFIX_RESULT.csv
?? docs/research/characters/CLEANUP2C1_NON_EUROPE_IMPLEMENTATION_RESULT.csv
?? docs/research/characters/NON_EUROPE_1776_REMAINING_RULER_RESEARCH_QUEUE.csv
?? docs/research/characters/NON_EUROPE_ACTIVE_COUNTRIES_1776_AUDIT.csv
?? docs/research/characters/NON_EUROPE_DECENTRALIZED_TAGS_1776.csv
?? docs/research/characters/NON_EUROPE_GENERATED_RULER_CANDIDATES.csv
?? docs/research/technology/
?? localization/english/cleanup2c1_non_europe_rulers_l_english.yml
?? localization/french/cleanup2c1_non_europe_rulers_l_french.yml
```

Every pre-existing path was preserved. The CLEANUP-2C-1B gameplay changes remain unstaged and runtime-partial; the technology research directory remains untracked, unstaged and unchanged.

## 2. Second-runtime evidence

The user's completely fresh 1776 start established:

- `USA`: President of the Continental Congress John Hancock — pass, no Claggett;
- `ASH`: Asantehene Osei Kwadwo — pass, no Bonsu;
- `SIA`: King Taksin — pass, no Rabibadhana;
- `SRK`: Susuhunan Pakubuwono III — pass, no Salihin;
- `YOG`: Sultan Hamengkubuwono I — pass, no Alaeddin;
- BIC, DEI and HBC correctly use **Chartered Company**, with no raw 2C-1 government key, but still received generated cadres Alasdair Arnott, Luuk Heldring and Daniel Macdonald;
- TIB displayed **Dalai Lama Demo Tulku**, while the separate Jamphel Gyatso existed with generated age 28;
- BUK displayed the now-correct office and fixed identity but redundantly combined them as **Ataliq Daniyal Biy Ataliq**.

The systemic empty-last-name construction and the general non-company government correction are therefore preserved, not reopened.

## 3. Complete company initialization trace

The relevant local Victoria 3 1.13 startup path is:

1. The owner-country history creates the company with `add_company`.
   - GBR creates `company_hbc` and `company_east_india_company`.
   - NET creates the fork's `company_dutch_east_india_company`.
2. The resulting company scope receives its establishment date, headquarters state and owned-country link through `add_owned_country` (`HBC`, `BIC`, or `DEI`).
3. The exposed `on_company_established` on-action is empty. No target scripted effect appoints an initial historical executive.
4. Character history is processed after country law/company setup. A target 1.13 history comment explicitly documents the broader setup sequence as country laws, government determination, then character setup.
5. Vanilla's deterministic BIC and HBC startup examples explicitly call `create_character` in the **owner's** character-history scope:

   ```text
   c:GBR ?= {
       create_character = { template = HBC_george_simpson }
       create_character = { template = BIC_george_eden }
   }
   ```

6. Those templates carry `company = company:<company instance>`. That field assigns the created character to the already-created company; the native company/owned-country system then exposes the executive as the chartered country's cadre/ruler representation.
7. `executive_usage` is the historical-candidate metadata used by the engine's executive selection/replacement system. It is not a startup command and does not itself execute `create_character`.
8. When no company-bound historical character is explicitly instantiated during startup, the engine supplies a generic cadre. The generic fallback is engine-side rather than an exposed scripted on-action; its operation is directly confirmed by the three fresh-start runtime results.

Other target examples reinforce the distinction: historical company-bound templates such as John Cockerill, Jean Dollfus and Alfred Krupp are also explicitly instantiated in character history when required at scenario start.

### Why CLEANUP-2C-1B failed

1B correctly supplied three eligible, company-bound templates, but never instantiated them. Omitting an optional `chance` field did not make a dormant template execute. The companies were therefore created with no assigned 1776 historical character, and the engine retained generated fallback cadres.

## 4. Deterministic company solution

The target supports Case A: explicit native assignment through character history. A new history file creates exactly three templates:

```text
c:GBR ?= {
    create_character = { template = BIC_john_harrison }
    create_character = { template = CLEANUP2C1B_HBC_sir_bibye_lake_jr }
}

c:NET ?= {
    create_character = { template = DEI_egbert_de_vrij_temminck }
}
```

The existing 1B templates retain their exact company bindings and narrow 1775–1776 `executive_usage` windows. No custom company government was restored.

| Tag | Owner scope | Explicit template | Company binding | Expected initial cadre |
|---|---|---|---|---|
| BIC | GBR | `BIC_john_harrison` | `company_east_india_company` | John Harrison |
| DEI | NET | `DEI_egbert_de_vrij_temminck` | `company_dutch_east_india_company` | Egbert de Vrij Temminck |
| HBC | GBR | `CLEANUP2C1B_HBC_sir_bibye_lake_jr` | `company_hbc` | Sir Bibye Lake Jr. |

All three continue to use target `gov_chartered_company`. Warren Hastings and Jeremias van Riemsdijk are not restored as forced country rulers. HBC's Governor remains a corporate capacity, not territorial sovereignty. The VOC representation remains an explicit one-character gameplay abstraction of collective Heeren XVII / Amsterdam Chamber governance.

ALK remains deferred and receives no 1776 Russian-American Company executive.

## 5. Tibet diagnosis

### Title root cause

The previous TIB government required:

```text
has_gov_regency = yes
```

But the relevant regency sentinel was set later, in Demo Tulku's character `on_created` block:

```text
set_variable = { name = regency_years value = 1 }
```

Government determination precedes character setup. The custom definition therefore depended on state that was not yet available at its initial eligibility check. At the same time, Tibet starts with `law_theocracy`, making vanilla `gov_dalai_lama` immediately eligible and producing the observed Dalai Lama title for Demo Tulku.

The working Maratha case is not changed. Its monarchy and already-validated regency structure remain byte-identical to baseline.

### Startup-safe correction

The TIB government is now bootstrapped by conditions available before character creation:

```text
c:TIB ?= this
has_law_or_variant = law_type:law_theocracy
is_domain_alliance_gov = no
```

Because the 2C-1 government file loads before vanilla `04_theocracies.txt`, `gov_cleanup2c1_tib` becomes the exact eligible tag government and renders:

- ruler title: `Regent`;
- heir title: `Dalai Lama`.

The existing `regency_years` variable remains on Demo Tulku. `designate_character_as_regent` remains absent.

### Jamphel Gyatso age

The earlier packet left both birth date and age blank, so the engine generated age 28. The CLEANUP-2C-1C authority supplied only approximate 1776 precision: about 17 years old. The implementation therefore uses:

```text
age = 17
```

No exact birthday is fabricated. Jamphel Gyatso remains a separate historical heir/nominal authority with the Dalai Lama title; this is a Victoria 3 abstraction and not a claim of hereditary Tibetan succession.

## 6. Narrow title-duplication audit

A case-insensitive exact-word comparison of the 109 fixed identities against their government title found ten candidates:

| Tag | Fixed identity before audit | Title | Action |
|---|---|---|---|
| BUK | Daniyal Biy Ataliq | Ataliq | **Changed to Daniyal Biy**; the packet and 1C instruction separate the office. |
| CON | Salah Bey | Bey | Preserved: packet-authorized conventional identity form. |
| DUR | Timur Shah Durrani | Shah | Preserved: complete packet-authorized historical name. |
| IR1 | Omar Pasha | Pasha | Preserved: packet recommends Omar Pasha and does not authorize Omar alone. |
| KHI | Muhammad Amin Inaq | Inaq | Preserved: complete packet identity. |
| KOK | Narbuta Biy | Biy | Preserved: complete packet identity. |
| KZH | Nuraly Khan | Khan | Preserved: complete packet identity. |
| MAS | Ibrahim Bey of Miliana | Bey | Preserved: complete packet identity. |
| OZH | Ablai Khan | Khan | Preserved: complete packet identity. |
| WSG | Garaad Ali | Garaad | Preserved: complete packet identity and approximate styling chronology. |

Only BUK had explicit authority to separate person and office. Its EN/FR fixed identity is now `Daniyal Biy`, while the government still supplies `Ataliq`, yielding the target display **Ataliq Daniyal Biy**.

No uncertain candidate was automatically rewritten. `Shah Timur Shah Durrani` and `Pasha Omar Pasha` are retained as authorized identity/title combinations pending any future explicit historical naming decision.

## 7. Files changed by CLEANUP-2C-1C

Gameplay/localization:

- added `common/history/characters/cleanup2c1c - initial company executives 1776.txt`;
- updated `common/history/characters/cleanup2c1 - non europe rulers 1776.txt` only for Jamphel Gyatso's approximate age;
- updated `common/government_types/00_cleanup2c1_non_europe.txt` only for TIB startup eligibility;
- updated `localization/english/cleanup2c1_non_europe_rulers_l_english.yml` only for BUK's visible identity;
- updated `localization/french/cleanup2c1_non_europe_rulers_l_french.yml` only for BUK's visible identity.

Outputs:

- added `docs/research/characters/CLEANUP2C1C_RUNTIME_HOTFIX_RESULT.csv`;
- added this report.

The BIC/DEI/HBC templates were inspected and reused without further 1C edits.

## 8. Static validation

```text
CLEANUP2C1C_SCOPE_COMPANY_TAGS = 3
CLEANUP2C1C_SCOPE_TIBET = 1
RESULT_CSV_ROWS = 140

DEFERRED_CASES_PRESERVED = 31
DEFERRED_CASES_FORCED_TO_HISTORICAL_IDENTITY = 0

SYSTEMIC_EMPTY_LAST_NAME_ARCHITECTURE_PRESERVED = YES
RELEVANT_FIXED_FIRST_NAME_ASSIGNMENTS = 111
RELEVANT_EXPLICIT_EMPTY_LAST_NAME_ASSIGNMENTS = 111
RANDOM_SURNAME_CAPABLE_HISTORICAL_DEFINITIONS = 0

USA_RUNTIME_PASS_STRUCTURE_PRESERVED = YES
ASH_RUNTIME_PASS_STRUCTURE_PRESERVED = YES
SIA_RUNTIME_PASS_STRUCTURE_PRESERVED = YES
SRK_RUNTIME_PASS_STRUCTURE_PRESERVED = YES
YOG_RUNTIME_PASS_STRUCTURE_PRESERVED = YES
MARATH_RUNTIME_PASS_STRUCTURE_PRESERVED = YES

BIC_GOVERNMENT = gov_chartered_company
DEI_GOVERNMENT = gov_chartered_company
HBC_GOVERNMENT = gov_chartered_company
BIC_FORCED_COUNTRY_RULER = NO
DEI_FORCED_COUNTRY_RULER = NO
HBC_FORCED_COUNTRY_RULER = NO
BIC_TARGET_COMPANY_EXECUTIVE = John Harrison
DEI_TARGET_COMPANY_EXECUTIVE = Egbert de Vrij Temminck
HBC_TARGET_COMPANY_EXECUTIVE = Sir Bibye Lake Jr.
COMPANY_INITIAL_EXECUTIVE_SELECTION_MECHANISM_IDENTIFIED = YES
EXPLICIT_INITIAL_COMPANY_EXECUTIVE_CREATIONS = 3
BIC_DETERMINISTIC_COMPANY_EXECUTIVE_STATIC = PASS
DEI_DETERMINISTIC_COMPANY_EXECUTIVE_STATIC = PASS
HBC_DETERMINISTIC_COMPANY_EXECUTIVE_STATIC = PASS

TIB_EFFECTIVE_RULER = Demo Tulku
TIB_EFFECTIVE_RULER_TITLE = Regent
TIB_NOMINAL_DALAI_LAMA = Jamphel Gyatso
TIB_JAMPHEL_GYATSO_AGE_SOURCE = CLEANUP2C1C_PACKET_APPROXIMATE_AGE
TIB_JAMPHEL_GYATSO_AGE = 17
TIB_JAMPHEL_GYATSO_EXACT_BIRTH_DATE_INVENTED = NO
TIB_DALAI_LAMA_TITLE_ON_DEMO_TULKU = NO
ACTIVE_DESIGNATE_CHARACTER_AS_REGENT = 0

BUK_VISIBLE_NAME_TARGET = Daniyal Biy
BUK_VISIBLE_TITLE_TARGET = Ataliq
TITLE_DUPLICATION_CANDIDATES_AUDITED = 10
TITLE_DUPLICATION_CANDIDATES_CHANGED = 1
UNCERTAIN_TITLE_DUPLICATIONS_AUTO_REWRITTEN = 0

INVALID_GOVERNMENT_IDS = 0
MISSING_EN_LOCALISATION = 0
MISSING_FR_LOCALISATION = 0
DUPLICATE_LOCALISATION_KEYS_INTRODUCED = 0
SCRIPT_BRACE_IMBALANCES = 0

PROTECTED_TECH_FILES_CHANGED = 0
BJECT_PATH_PRESENT = 0
BIC_FRONTIER_COLONIZATION_PRESERVED = YES
BIC_COLONIAL_EXPLOITATION_PRESENT = NO
MAP_FILES_CHANGED = 0
STATE_REGION_FILES_CHANGED = 0
OWNERSHIP_FILES_CHANGED = 0
DIPLOMACY_FILES_CHANGED = 0
MILITARY_FORMATION_FILES_CHANGED = 0
COMMANDER_FILES_CHANGED = 0

CODEX_LAUNCHED_VICTORIA3 = NO
GIT_INDEX_MUTATED_BY_CODEX = NO
git diff --check = PASS
```

The known 1B runtime-pass structures were compared before and after the targeted edit. USA's template; the ASH, SIA, SRK and YOG history/government blocks; their visible EN name/title localizations; and all four Maratha history/government/localization files retain their baseline hashes.

Static validation proves the scripted path and exact startup inputs. The actual engine assignment and rendered title still require the one fresh user runtime below.

## 9. One-session user runtime checklist

Start one completely fresh 1776 session in ordinary mode. Debug mode is not required.

- **BIC — Compagnie des Indes orientales**
  - company cadre/executive: **John Harrison**;
  - government remains **Compagnie à charte**;
  - no forced Warren Hastings country ruler;
  - no raw `gov_cleanup2c1_bic`.
- **DEI — Compagnie néerlandaise des Indes orientales**
  - company cadre: **Egbert de Vrij Temminck**;
  - government remains **Compagnie à charte**;
  - no Jeremias van Riemsdijk country-ruler workaround;
  - no raw `gov_cleanup2c1_dei`.
- **HBC — Compagnie de la Baie d'Hudson**
  - company cadre: **Sir Bibye Lake Jr.**;
  - government remains **Compagnie à charte**.
- **TIB — Tibet**
  - visible ruler: **Regent Demo Tulku**;
  - never Dalai Lama Demo Tulku;
  - Jamphel Gyatso remains separately present as Dalai Lama/nominal heir authority;
  - Jamphel Gyatso displays age **17** on 1776-01-01.
- **BUK — Boukhara**
  - expected display: **Ataliq Daniyal Biy**;
  - no trailing duplicated Ataliq.

Regression spot checks:

- **USA — Treize Colonies**: President of the Continental Congress John Hancock.
- **ASH — Ashanti**: Asantehene Osei Kwadwo.
- **SIA — Siam**: King Taksin.
- **SRK — Surakarta**: Susuhunan Pakubuwono III.
- **YOG — Yogyakarta**: Sultan Hamengkubuwono I.
- **MARATH — Confédération marathe**: Regent Sakharam Bapu Bokil; Madhavrao II remains Peshwa/heir.
- **DAI — Dai Nam**: procedural ruler remains acceptable.
- **TRN — Potchefstroom**: procedural ruler remains acceptable.

Let several days pass, quit normally once, then inspect fresh `error.log`, `debug.log` and `game.log`:

```text
ATTRIBUTABLE_CHARACTER_ERRORS = 0
ATTRIBUTABLE_GOVERNMENT_ERRORS = 0
ATTRIBUTABLE_LOCALISATION_ERRORS = 0
UNKNOWN_EFFECT_OR_TRIGGER_CLEANUP2C1C = 0
RAW_GOV_KEY_VISIBLE = 0
```

Stop after reporting that single runtime result. Do not begin map, commander, portrait/DNA or technology work.

## CLEANUP-2C-1D — Final static log-hygiene closure

The completed visual runtime supersedes the earlier retest gate. The two 2C company files now carry UTF-8 BOM. A repository-wide and engine-wide audit found no active consumer of `cleanup2c1_historical_office`; its 106 obsolete startup assignments were therefore removed without changing any remaining character, government, company, title or succession logic. No further runtime is required.

```text
VISUAL_RUNTIME = PASS
BIC = PASS
DEI = PASS
HBC = PASS
TIB = PASS
BUK = PASS
CLEANUP2C_ATTRIBUTABLE_GAMEPLAY_ERRORS = 0
CLEANUP2C_BOM_WARNINGS_FIXED = 2
CLEANUP2C_DEAD_VARIABLE_WARNING_FIXED = 1
```
