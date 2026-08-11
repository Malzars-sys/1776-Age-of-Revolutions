# CLEANUP-2C-1B — Runtime names, titles and chartered-company hotfix

## Result

`CLEANUP2C1B_STATIC = PASS`

`CLEANUP2C1B_RUNTIME = USER_RETEST_REQUIRED`

The hotfix corrects the systemic historical-name construction, makes the 106 non-company start offices eligible at government selection time, and replaces the BIC/DEI/HBC country-ruler workarounds with historical candidates in Victoria 3 1.13's native company executive pool. Victoria 3 was not launched.

## Repository baseline

- Branch: `cleanup-post-release`
- HEAD before and after the hotfix: `fd092a03a5d6cc105e522e2c4bb38e4bc111cce6`
- Index: empty before and after the hotfix
- Initial `git diff --check`: pass
- Final `git diff --check`: pass

Initial worktree, preserved rather than cleaned or normalized:

```text
 M common/character_templates/country_dei.txt
 M common/character_templates/country_usa.txt
 M "common/history/characters/bic - british india.txt"
 M "common/history/characters/dei - dutch east indies.txt"
 M common/history/characters/dur.txt
 M "common/history/characters/ir1 - mamluk iraq.txt"
 M common/history/characters/usa.txt
 M docs/reports/cleanup/CLEANUP2B3_COMPLETE_EUROPEAN_HISTORICAL_RECONSTRUCTION.md
?? common/government_types/00_cleanup2c1_non_europe.txt
?? "common/history/characters/cleanup2c1 - non europe rulers 1776.txt"
?? docs/reports/cleanup/CLEANUP1D_MARATH_NAVAL_CREW_DIAGNOSTIC_AND_FIX.md
?? docs/reports/cleanup/CLEANUP2C0_COMPLETE_NON_EUROPE_ACTIVE_COUNTRY_AUDIT.md
?? docs/reports/cleanup/CLEANUP2C1_COMPLETE_NON_EUROPE_HISTORICAL_RULER_RECONSTRUCTION.md
?? docs/reports/cleanup/CLEANUP2C_RESEARCH_COMPLETE_NON_EUROPE_RULERS_1776.md
?? docs/reports/cleanup/RULERS_1776_NON_EUROPE_CONSTITUTIONAL_NOTES.md
?? docs/reports/cleanup/RULERS_1776_NON_EUROPE_SOURCES.md
?? docs/research/characters/CLEANUP2C1_NON_EUROPE_IMPLEMENTATION_RESULT.csv
?? docs/research/characters/NON_EUROPE_1776_REMAINING_RULER_RESEARCH_QUEUE.csv
?? docs/research/characters/NON_EUROPE_ACTIVE_COUNTRIES_1776_AUDIT.csv
?? docs/research/characters/NON_EUROPE_DECENTRALIZED_TAGS_1776.csv
?? docs/research/characters/NON_EUROPE_GENERATED_RULER_CANDIDATES.csv
?? docs/research/technology/
?? localization/english/cleanup2c1_non_europe_rulers_l_english.yml
?? localization/french/cleanup2c1_non_europe_rulers_l_french.yml
```

All entries above belong to the pre-existing CLEANUP worktree. This phase edited only the files listed under “Hotfix files”. It did not discard or normalize any existing work.

## Runtime evidence received

The first user test showed three systematic classes of failure:

1. Fixed identities loaded, but a culture-generated surname or dynastic component was appended: Osei Kwadwo **Bonsu**, Daniyal Biy Ataliq **Bahadur**, Taksin **Rabibadhana**, Pakubuwono III **Salihin**, Hamengkubuwono I **Alaeddin**, John Hancock **Claggett**, Timur Shah Durrani **Babaian**, Omar Pasha **Razikashvili**, plus generated material for Demo Tulku.
2. Generic governments won over the intended offices: King instead of Asantehene, Emir instead of Ataliq, Sunan instead of Susuhunan, Emperor instead of Shah, and Dalai Lama instead of Regent.
3. BIC and DEI displayed randomly selected native company cadres while the forced country rulers and raw `gov_cleanup2c1_bic` / `gov_cleanup2c1_dei` government keys represented the wrong architectural layer.

The same runtime established that the existing Maratha regency works and must remain untouched. DAI and TRN procedural rulers are expected.

## Technical authority inspected

The implementation was checked against the installed Victoria 3 1.13 / The Great Wave files, notably:

- `common/character_templates/00_default_template.txt`;
- the vanilla historical character templates, including BIC and HBC executive examples;
- `common/government_types/01_colonial_administrations.txt`;
- the complete local government-type directory and its regency conditions.

No newer-version syntax was assumed.

## Root cause 1 — generated surnames

The default character template supplies both `first_name = culture` and `last_name = culture`. Every inspected vanilla historical template that fixes a historical identity also explicitly supplies `last_name`; the CLEANUP-2C-1 definitions supplied only `first_name`, even though that localization already contained the complete researched identity. The omitted field therefore remained eligible for cultural completion.

The systemic fix is:

```text
first_name = CLEANUP2C1_NAME_<TAG>
last_name = CLEANUP2C1_EMPTY_NAME
```

`CLEANUP2C1_EMPTY_NAME` is explicitly localized to an empty value in English and French. This preserves the complete packet-authorized identity already stored in `first_name` while preventing the engine from filling an omitted component. It does not split, reinterpret or invent surnames, dynasties or regnal elements.

The audit found 111 relevant character definitions: the 109 tag-level representations plus the NAG and TIB heirs. All 111 now have an explicit last-name component.

Tibet's visible localization was also narrowed to the requested identities:

- effective ruler: `Demo Tulku`;
- nominal child authority/heir: `Jamphel Gyatso`.

## Root cause 2 — government and title selection

The previous `gov_cleanup2c1_*` definitions required:

```text
ruler ?= { has_variable = cleanup2c1_historical_office }
```

That variable was set inside the new character's `on_created` block. At initial government resolution the condition could therefore be false or unresolved, causing the engine to continue to a generic eligible government. Having a ruler-title localization key did not make the corresponding government win.

Three local observations corroborate this timing diagnosis:

- BIC and DEI custom definitions, which did not depend on the marker, did win and exposed their raw government keys;
- the other marker-gated definitions lost to generic governments in the user's runtime;
- the already-working Maratha government uses tag plus `has_gov_regency`, not a late character marker.

The target 1.13 government definitions expose no supported arbitrary `priority` or `weight` field. The smallest supported fix is therefore to remove the late marker from the 106 non-company definitions and retain:

- the exact tag condition;
- `has_gov_regency = yes` for NAG and TIB;
- `has_gov_regency = no` elsewhere;
- the existing domain-alliance exclusion and transfer-of-power method.

The custom file loads before the generic `01_*` government definitions, so the exact tag office is the first eligible definition. Government IDs and descriptions are now localized in both languages, avoiding raw keys.

This makes the office tag-specific rather than character-variable-specific. It is a deliberate initialization-safe tradeoff: the historical office title remains the country's specialized office after a later succession unless another government condition supersedes it.

TIB retains only the proven 1.13 regency mechanism:

```text
set_variable = { name = regency_years value = 1 }
```

There is no active `designate_character_as_regent` effect.

## Root cause 3 — chartered-company cadre override

The target company system does not obtain its senior cadre from a direct `create_character` country-history ruler. It selects a historical template through `executive_usage`, constrained by the owning country and `company_type`, and associates that character with the actual company using `company = company:<instance>`.

The previous BIC and DEI candidates lacked that explicit company association, while HBC was created as an ordinary country ruler. The native executive pool therefore remained free to choose generated cadres such as Alasdair Arnott and Luuk Heldring.

## Company architecture selected

All three companies now use the native target-1.13 architecture:

| Tag | Historical company candidate | Historical corporate capacity | Native company type |
|---|---|---|---|
| BIC | John Harrison | Chairman of the East India Company / Court of Directors | `company_east_india_company` |
| HBC | Sir Bibye Lake Jr. | Governor of the Hudson's Bay Company | `company_hbc` |
| DEI | Egbert de Vrij Temminck | VOC bewindhebber/director, Amsterdam Chamber | `company_dutch_east_india_company` |

Each candidate is historical, explicitly tied to its company, constrained to the correct owner (GBR or NET), and guaranteed in the 1775–1776 usage window by omitting the optional chance roll, following vanilla guaranteed-executive examples.

The following wrong architecture was removed:

- no direct Warren Hastings BIC country-ruler creation;
- no direct Jeremias van Riemsdijk DEI country-ruler creation;
- no direct Sir Bibye Lake Jr. HBC country-ruler creation;
- no `gov_cleanup2c1_bic`, `gov_cleanup2c1_dei` or `gov_cleanup2c1_hbc` definition.

BIC, DEI and HBC therefore fall back to the target engine's `gov_chartered_company`. The company layer itself promotes its executive into the tag's ruler representation; no monarch, president, CEO or fake territorial government is scripted by this hotfix.

The engine's native country-government ruler label remains standardized by `gov_chartered_company`; the historically precise Chairman / Governor / Bewindhebber capacities above describe the selected corporate figures and are not implemented as fake sovereign government titles. The user runtime should verify the exact historical name in the company/cadre layer.

VOC governance by the Heeren XVII was collective. Egbert de Vrij Temminck is explicitly a one-character Victoria 3 corporate abstraction of the Amsterdam Chamber's senior director layer, not a President, CEO, monarch or Governor-General of the Dutch East Indies.

ALK remains `MAP_REWORK_DEFERRED`; no Russian-American Company executive is projected backward into 1776.

## Hotfix files

Content edited or added by CLEANUP-2C-1B:

- `common/character_templates/country_bic.txt`
- `common/character_templates/country_dei.txt`
- `common/character_templates/country_usa.txt`
- `common/character_templates/cleanup2c1b_company_executives.txt`
- `common/history/characters/bic - british india.txt`
- `common/history/characters/dei - dutch east indies.txt`
- `common/history/characters/dur.txt`
- `common/history/characters/ir1 - mamluk iraq.txt`
- `common/history/characters/cleanup2c1 - non europe rulers 1776.txt`
- `common/government_types/00_cleanup2c1_non_europe.txt`
- `localization/english/cleanup2c1_non_europe_rulers_l_english.yml`
- `localization/french/cleanup2c1_non_europe_rulers_l_french.yml`

Outputs added:

- `docs/research/characters/CLEANUP2C1B_RUNTIME_HOTFIX_RESULT.csv`
- `docs/reports/cleanup/CLEANUP2C1B_RUNTIME_NAMES_TITLES_AND_CHARTERED_COMPANIES_HOTFIX.md`

Pre-existing changes to USA history and the European reconstruction report were not edited by this hotfix.

## Deferred cases

All 31 cases remain procedural or structurally deferred, with zero forced historical identities:

```text
AGC AIT ALK ARB BAL BRG BST CHC CIR DAI FTR HAU HAW IQU JMB KAU
LAN MAD MJT NBS ONT ORA PHL SHS SIL SOK TGI TRN UNT UZH WTU
```

## Static validation

```text
CLEANUP2C1B_PACKET_AUTHORIZED_HISTORICAL_CASES = 109
DEFERRED_CASES_PRESERVED = 31
DEFERRED_CASES_FORCED_TO_HISTORICAL_IDENTITY = 0

RANDOM_SURNAME_CAPABLE_HISTORICAL_DEFINITIONS = 0
HISTORICAL_EXACT_NAME_STATIC_PASS = 109
RELEVANT_CHARACTER_NAME_ASSIGNMENTS = 111
EXPLICIT_LAST_NAME_ASSIGNMENTS = 111

ASH_EXPECTED_NAME = Osei Kwadwo
ASH_EXPECTED_TITLE = Asantehene
BUK_EXPECTED_NAME = Daniyal Biy Ataliq
BUK_EXPECTED_TITLE = Ataliq
SIA_EXPECTED_NAME = Taksin
SRK_EXPECTED_NAME = Pakubuwono III
SRK_EXPECTED_TITLE = Susuhunan
YOG_EXPECTED_NAME = Hamengkubuwono I
YOG_EXPECTED_TITLE = Sultan
USA_EXPECTED_NAME = John Hancock
USA_EXPECTED_TITLE = President of the Continental Congress
DUR_EXPECTED_NAME = Timur Shah Durrani
DUR_EXPECTED_TITLE = Shah
IR1_EXPECTED_NAME = Omar Pasha
IR1_EXPECTED_TITLE = Pasha
TIB_EFFECTIVE_RULER = Demo Tulku
TIB_EFFECTIVE_RULER_TITLE = Regent
TIB_DALAI_LAMA = Jamphel Gyatso

MARATH_EXISTING_REGENCY_UNCHANGED = YES
ACTIVE_DESIGNATE_CHARACTER_AS_REGENT = 0

BIC_FORCED_WARREN_HASTINGS_COUNTRY_RULER = NO
DEI_FORCED_VAN_RIEMSDIJK_COUNTRY_RULER = NO
BIC_COMPANY_HISTORY_TARGET = John Harrison
HBC_COMPANY_HISTORY_TARGET = Sir Bibye Lake Jr.
DEI_COMPANY_HISTORY_TARGET = Egbert de Vrij Temminck
ALK_HISTORICAL_COMPANY_EXECUTIVE = NONE
NATIVE_COMPANY_LINKS = 3

DELEGATED_EXECUTIVE_PROMOTED_TO_MONARCH = 0
COLLECTIVE_COMPANY_EXECUTIVE_MISREPRESENTED_AS_MONARCH = 0
RAW_GOV_CLEANUP2C1_BIC_VISIBLE_RISK = 0
RAW_GOV_CLEANUP2C1_DEI_VISIBLE_RISK = 0

NON_COMPANY_CUSTOM_GOVERNMENTS = 106
LATE_CHARACTER_MARKER_GOVERNMENT_TESTS = 0
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

RESULT_CSV_ROWS = 140
CODEX_LAUNCHED_VICTORIA3 = NO
GIT_INDEX_MUTATED_BY_CODEX = NO
git diff --check = PASS
```

Protected technology hashes were unchanged:

```text
315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5  TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410  TECH_TREE_INDUSTRIAL_CHAINS.md
0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596  TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D  TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5  TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A  TECH_TREE_RESOURCE_CANDIDATES.csv
150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA  TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

Static validation proves construction and eligibility, not actual rendered runtime behavior. The next gate is the single user session below.

## One-session user runtime checklist

Start one ordinary session without debug mode. Check these tags and French country names:

- **BIC — Compagnie des Indes orientales**: John Harrison appears as the historical corporate cadre selected by the native company architecture; no forced Warren Hastings workaround; no raw `gov_cleanup2c1_bic`.
- **DEI — Compagnie néerlandaise des Indes orientales**: Egbert de Vrij Temminck appears in the corporate cadre layer; no forced Jeremias van Riemsdijk country ruler; no raw `gov_cleanup2c1_dei`.
- **HBC — Compagnie de la Baie d'Hudson**: Sir Bibye Lake Jr. appears through native company logic.
- **USA — Treize Colonies**: John Hancock; President of the Continental Congress; no Claggett; George Washington is not President.
- **ASH — Ashanti**: Osei Kwadwo; Asantehene; no Bonsu appended.
- **BUK — Boukhara**: Daniyal Biy Ataliq; Ataliq; no Bahadur appended.
- **SIA — Siam**: Taksin; no Rabibadhana.
- **SRK — Surakarta**: Pakubuwono III; Susuhunan; no Salihin.
- **YOG — Yogyakarta**: Hamengkubuwono I; Sultan; no Alaeddin.
- **DUR — Empire durrani**: Timur Shah Durrani; Shah; no Babaian; not Emperor.
- **IR1 — Irak mamelouk**: Omar Pasha; Pasha; no Razikashvili.
- **TIB — Tibet**: Demo Tulku is Regent; Jamphel Gyatso remains the Dalai Lama / nominal child authority.
- **MARATH — Confédération marathe**: Sakharam Bapu Bokil remains Regent; Madhavrao II remains the child Peshwa/heir.
- **DAI — Dai Nam**: a procedural ruler remains acceptable; no custom unitary 1776 monarch.
- **TRN — Potchefstroom**: a procedural ruler remains acceptable; no false 1776 Boer president.

Let several game days pass, quit normally once, then inspect fresh `error.log`, `debug.log` and `game.log` for:

```text
ATTRIBUTABLE_CHARACTER_ERRORS = 0
ATTRIBUTABLE_GOVERNMENT_ERRORS = 0
ATTRIBUTABLE_LOCALISATION_ERRORS = 0
UNKNOWN_EFFECT_OR_TRIGGER_CLEANUP2C1B = 0
RAW_GOV_KEY_VISIBLE = 0
```

Stop after reporting that single runtime result. Do not begin map, commander, portrait/DNA or technology work from this checklist.
