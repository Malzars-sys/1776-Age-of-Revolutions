# CLEANUP-2C-0 — Complete Non-Europe Active-Country Audit

## 1. Baseline

```text
BRANCH = cleanup-post-release
HEAD = 68b777d31f673fea264776cd2d7ffef33e47b61f
INDEX_EMPTY = YES
WORKTREE_CHANGED_PATHS = 8
GIT_DIFF_CHECK = PASS
```

The eight baseline paths were the untracked `CLEANUP1D_MARATH_NAVAL_CREW_DIAGNOSTIC_AND_FIX.md` report and the seven protected technology research files. They were preserved. The complete CLEANUP-2B-3, CLEANUP-2B-2.5, Europe audit, generated-candidate file, Batch 1 result, Batch 2 result, and residual result were read before classification.

## 2. Europe runtime closure

The user runtime is closed as `PASS`. Sakharam Bapu Bokil, Charlotte Amalie, Lucca, Ireland, and the residual rulers passed. The session reached `1776-01-20`, ended normally, and fresh logs contained no attributable regency, BOM, character, government, ruler-title, or localisation error.

Karl Wilhelm is `STATIC = PASS` and `VISUAL = NOT_VERIFIED`. The screenshot showed Baden's Charles-Frederick von Zahringen, age 47, rather than Karl Wilhelm. No retest is required. The final verdict is `PASS_WITH_KARL_WILHELM_SCREENSHOT_MISSING`.

## 3. Method for world active-country reconstruction

The active set was reconstructed from every `country = c:TAG` owner materialised in `common/history/states/00_states.txt`, including split states with multiple owners. Effective country definitions were resolved target-first and then fork overrides, consistent with the fork metadata. Subject relationships were used to classify active territorial tags, not to revive absent tags.

Six optional subject-pact targets have no starting territory and are not otherwise materialised: `ARM`, `DWI`, `KAF`, `LIB`, `ORG`, and `SEQ`. They are dormant/non-materialised references, not active entities. `DWI` also lacks an effective country definition. No future, revolt-only, event-only, or merely defined tag was admitted.

## 4. Europe exclusion method

The 62 tags in `EUROPE_ACTIVE_COUNTRIES_1776_AUDIT.csv` are the exclusive Europe source. All 62 resolve to centralized country types. `RUS` and `TUR` remain wholly excluded as already audited transcontinental countries, while their separately materialised dependencies remain eligible.

The non-Europe centralized set is therefore the effective territorial centralized set minus exactly those 62 tags. Europe was not geographically redefined.

## 5. World totals

```text
ALL_ACTIVE_1776_ENTITIES = 375
WORLD_ACTIVE_CENTRALIZED_COUNTRIES_TOTAL = 210
EUROPE_ACTIVE_CENTRALIZED_COUNTRIES_TOTAL = 62
NON_EUROPE_ACTIVE_CENTRALIZED_COUNTRIES_TOTAL = 148
WORLD_ACTIVE_DECENTRALIZED_TAGS_TOTAL = 165
NON_EUROPE_DECENTRALIZED_TAGS_TOTAL = 165
```

The identities close exactly: `375 = 210 + 165` and `210 = 62 + 148`. Effective entity types are 61 recognized, 127 unrecognized, 22 colonial, and 165 decentralized.

For compatibility with the requested legacy output variables, `WORLD_ACTIVE_COUNTRIES_TOTAL` and `NON_EUROPE_ACTIVE_COUNTRIES_TOTAL` below mean centralized countries only. Decentralized entities are always reported separately.

The 165 decentralized tags are recorded in `NON_EUROPE_DECENTRALIZED_TAGS_1776.csv`. They receive no ruler audit, age audit, character search, starting-ruler requirement, generated-ruler classification, or historical-research-queue row. `DECENTRALIZED_EXCEPTION_REVIEW_TOTAL = 0`: no local evidence met any force-majeure condition. Their only recommended future phase is `MAP / POPULATION / POLITICAL STRUCTURE REWORK`.

## 6. Complete non-Europe inventory

`NON_EUROPE_ACTIVE_COUNTRIES_1776_AUDIT.csv` contains one row for each of the 148 active centralized non-Europe countries and all required source, government, dependency, ruler, status, priority, and map fields.

| Audit region | Countries |
|---|---:|
| NORTH_AMERICA | 8 |
| CARIBBEAN | 4 |
| CENTRAL_AMERICA | 2 |
| SOUTH_AMERICA | 5 |
| NORTH_AFRICA | 8 |
| WEST_AFRICA | 14 |
| CENTRAL_AFRICA | 3 |
| EAST_AFRICA | 11 |
| SOUTHERN_AFRICA | 6 |
| HORN_OF_AFRICA | 5 |
| MIDDLE_EAST | 4 |
| ARABIAN_PENINSULA | 5 |
| CAUCASUS | 2 |
| CENTRAL_ASIA | 6 |
| SOUTH_ASIA | 4 |
| INDIA | 21 |
| EAST_ASIA | 5 |
| SOUTHEAST_ASIA | 31 |
| OCEANIA | 4 |
| **Total** | **148** |

No centralized audit row has `world_region = UNKNOWN`.

## 7. Already validated Batch-1 countries

`NON_EUROPE_ALREADY_HISTORICALLY_VALIDATED` contains eight rows, none of which enters the new research queue:

| Tag | Country | Source batch | Ruler | Status |
|---|---|---|---|---|
| CHI | China | Batch 1 | Qianlong (Hongli) | ALREADY_VALIDATED_BATCH1 |
| JAP | Japan | Batch 1 | Tokugawa Ieharu | ALREADY_VALIDATED_BATCH1 |
| KOR | Korea | Batch 1 | Yeongjo | ALREADY_VALIDATED_BATCH1 |
| MUG | Hindustan | Batch 1 | Shah Alam II | ALREADY_VALIDATED_BATCH1 |
| MARATH | Maratha Confederacy | Batch 1 | Sakharam Bapu Bokil / Madhavrao II | ALREADY_VALIDATED_BATCH1 |
| HYD | Hyderabad | Batch 1 | Nizam Ali Khan | ALREADY_VALIDATED_BATCH1 |
| MYS | Mysore | Batch 1 | Hyder Ali | ALREADY_VALIDATED_BATCH1 |
| PER | Persia | Batch 1 | Karim Khan Zand | ALREADY_VALIDATED_BATCH1 |

## 8. Ruler source classification

The exclusive historical-source classification closes as `135 + 8 + 3 + 2 = 148`: 135 engine-generated rulers, eight Batch-1 validated rulers, three scripted but unverified rulers, and two scripted anachronistic candidates. Shared-monarch, no-visible-ruler, and unknown totals are all zero. MARATH is the one scripted regency and overlaps the validated group.

## 9. Generated rulers

`NON_EUROPE_GENERATED_RULER_CANDIDATES.csv` contains 135 rows. Each is an active centralized tag with no explicit effective starting ruler, shared monarch, special regency, or delegated executive. Static confidence in engine generation is `HIGH`; the current runtime-generated name and age were not captured and are not invented by this audit.

## 10. Scripted but unverified rulers

| Tag | Scripted person | Static age | Office | Required action |
|---|---|---:|---|---|
| BIC | Warren Hastings | 43 | Governor-General | Verify identity, office, age, company constitution, and delegated sovereignty. |
| DUR | Timur Durrani | 29 | Engine-selected monarchical title | Verify identity, title, succession, and 1776 constitution. |
| IR1 | Omar Ahmad | 27 | Pasha | Verify identity, title, political relationship, and 1776 constitution. |

These ages are static start-date calculations only. Script presence is not treated as historical validation.

## 11. Scripted anachronistic candidates

`DEI` and `USA` are the two P0 scripted candidates. DEI's delegated-executive template contains visible copied BIC artifacts, so Reinier de Klerk's identity, age, office, and company constitution require correction research. USA scripts George Washington as president while the same start setup makes USA a British colony; that local contradiction requires a ruler/government/subject-resolution decision. No external historical claim was used.

## 12. Government/title anomalies

Only the eight Batch-1 countries are closed as `GOVERNMENT_OK`. The remaining 140 countries require joint ruler/government work, and the same 140 require title and constitutional verification. These are overlapping audit dimensions, not additive populations.

The principal static risk patterns are generic monarchy/autocracy defaults, unverified emirate/sultanate/khanate titles, princely-subject constitutions, colonial tags receiving sovereign-style presentation, delegated company executives, and the USA/DEI contradictions. No gameplay law or government type was changed.

## 13. Colonies and companies

There are 22 active tagged colonies or chartered companies requiring historical executive research:

- chartered companies: `ALK/RUS`, `BIC/GBR`, `DEI/NET`, `HBC/GBR`;
- colonies: `BRZ/POR`, `CUB/SPA`, `GR5/SPA`, `HAI/FRA`, `IQU/SPA`, `LOU/SPA`, `NBS/GBR`, `NVS/GBR`, `ONT/GBR`, `PCO/SPA`, `PHI/SPA`, `QUE/GBR`, `SC1/SPA`, `SC2/SPA`, `SC3/SPA`, `SC4/SPA`, `SIL/GBR`, `USA/GBR`.

For every one, research must distinguish a delegated governor/executive from a sovereign ruler. The audit does not promote any governor into a monarch.

## 14. North America

Eight centralized tags are audited. British and Russian company/colonial relations are retained as setup facts; native decentralized polities are excluded into the separate 165-tag registry. USA is the region's P0 contradiction, not silently normalized.

## 15. Caribbean / Central America

Four Caribbean and two Central American centralized tags are audited. Spanish and French colonial administrations are marked for executive, constitution, and overlord research. Decentralized tags, where present, remain outside the ruler corpus.

## 16. South America

Five centralized tags are audited. Brazil and the Spanish colonial/viceroyal abstractions remain tagged as delegated-executive questions. The scenario setup, rather than an external historical country list, determines inclusion.

## 17. Africa

Forty-seven centralized tags are audited across North (8), West (14), Central (3), East (11), Southern (6), and Horn (5) regions. Every technically decentralized African polity is in the separate exclusion registry. The centralized rows retain dynasty, title, religious-polity, commercial-state, dependency, and colonial questions for later research without guessing their rulers.

## 18. Middle East / Arabia / Caucasus

Eleven centralized tags are audited: Middle East (4), Arabian Peninsula (5), and Caucasus (2). `TUR` and `RUS` are not duplicated. Separately materialised dependencies are retained. Chechnya and Circassia are classified as Caucasus even though their target strategic states belong to the broad `region_russia` container.

## 19. South Asia / India

Twenty-five centralized tags are audited: 21 India and four South Asia/Himalayas. The eight Batch-1 successes remain closed, while princely subjects, regional states, BIC, and all other generated rulers remain in the research corpus. No decentralized polity is admitted.

## 20. Central Asia

Six centralized tags are audited. All generated khanate/emirate-style rulers and generic government/title combinations remain explicit research questions. Technically decentralized confederations are reserved for the future political-structure rework.

## 21. East Asia

Five centralized tags are audited. CHI, JAP, and KOR remain Batch-1 validated. The remaining centralized tags require research; distinct decentralized entities do not.

## 22. Southeast Asia

Thirty-one centralized tags are audited, including regional states, dependencies, the Philippines, and the DEI company abstraction. DEI is P0; all generated rulers remain P1. No vanilla-1836 identity or dynasty is presumed valid for 1776.

## 23. Oceania / Pacific

Four centralized tags are audited. Their existence and political form are retained from the actual setup and marked for ruler/government research. The numerous decentralized Pacific tags remain excluded from this character phase. No later Australian colony was inferred from external history.

## 24. Map-dependent cases

There are 55 map-dependent centralized cases: 22 `MAJOR` colonies/companies and 33 `MINOR` protectorate, puppet, tributary, or vassal relationships. None is removed from the research queue. There are no `TOTAL` cases in this static audit.

The 165 decentralized tags are not counted in this number because their whole category is reserved for a separate map/population/political-structure phase.

## 25. P0 cases

The complete P0 list is:

- `DEI` — Reinier de Klerk delegated-executive template with copied BIC artifacts;
- `USA` — George Washington presidential script conflicts with USA's start classification as a GBR colony.

No correction was implemented.

## 26. P1 cases

The complete 135-tag P1 generated-ruler list is:

`ACE, AGC, AIT, ALK, ANK, ARB, ASH, AWA, BAL, BEN, BGI, BHN, BHU, BHV, BLG, BNJ, BNY, BOR, BRD, BRG, BRU, BRZ, BST, BTN, BUG, BUK, BUR, CAM, CHC, CHP, CIR, CMI, COC, CON, COO, CUB, DAH, DAI, DFR, ETH, EZO, FTJ, FTR, GAR, GLD, GR5, GWA, HAI, HAU, HAW, HBC, HDJ, IQU, ISQ, JEY, JMB, JOH, KAU, KHI, KHP, KNO, KOK, KON, KRG, KRT, KTI, KZH, LAH, LAN, LOU, LUA, MAD, MAS, MBS, MGD, MJT, MKT, MLD, MOR, MSN, NAG, NBS, NEP, NVS, OMA, ONT, ORA, OYO, OZH, PAN, PCO, PHI, PHL, PLY, PON, PRK, PUD, QUE, RWD, RYU, SAK, SAT, SC1, SC2, SC3, SC4, SEL, SGU, SHS, SIA, SIK, SIL, SIN, SMB, SOK, SRK, STG, SUL, SWZ, TGI, TIB, TID, TRA, TRI, TRN, TUG, TUN, UNT, UZH, WAD, WBL, WSG, WTU, YOG, ZAI`.

P2 is `BIC, DUR, IR1`. P3 is `CHI, HYD, JAP, KOR, MARATH, MUG, MYS, PER`.

## 27. Research groups

Eight organizational groups are recommended: `AMERICAS`, `AFRICA`, `MIDDLE_EAST_CAUCASUS`, `SOUTH_ASIA`, `CENTRAL_ASIA`, `EAST_ASIA`, `SOUTHEAST_ASIA`, and `OCEANIA`. These organize research only and do not prescribe eight implementation phases.

## 28. Historical research queue

`NON_EUROPE_1776_REMAINING_RULER_RESEARCH_QUEUE.csv` contains 140 rows: two P0, 135 P1, and three P2. It excludes all eight Batch-1 validated rows and all 165 decentralized tags. Each row asks for the effective ruler on `1776-01-01`, verified life dates and succession context, government/distribution/title, and—where relevant—the delegated executive/sovereignty relationship.

No external research was performed during this audit.

## 29. Exhaustiveness proof

```text
NON_EUROPE_ACTIVE_CENTRALIZED_TAG_COUNT = 148
NON_EUROPE_AUDITED_CENTRALIZED_TAG_COUNT = 148
NON_EUROPE_UNAUDITED_ACTIVE_CENTRALIZED_TAG_COUNT = 0

NON_EUROPE_DECENTRALIZED_TAGS_TOTAL = 165
DECENTRALIZED_TAGS_IN_RULER_AUDIT = 0
DECENTRALIZED_TAGS_IN_RESEARCH_QUEUE = 0
DECENTRALIZED_EXCEPTION_REVIEW_TOTAL = 0

NON_EUROPE_ENGINE_GENERATED_TOTAL = 135
NON_EUROPE_SCRIPTED_VALIDATED_TOTAL = 8
NON_EUROPE_SCRIPTED_UNVERIFIED_TOTAL = 3
NON_EUROPE_SCRIPTED_ANACHRONISTIC_CANDIDATES = 2
NON_EUROPE_SHARED_MONARCH_TOTAL = 0
NON_EUROPE_REGENCY_TOTAL = 1
NON_EUROPE_NO_VISIBLE_RULER_TOTAL = 0
NON_EUROPE_UNKNOWN_RULER_TOTAL = 0
```

## 30. Protected-state verification

No gameplay path was edited. The seven technology research files remained untracked, unstaged, and byte-identical to baseline. Their SHA-256 values remained:

- `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5`;
- `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410`;
- `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596`;
- `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D`;
- `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5`;
- `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A`;
- `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA`.

Metadata remained at SHA-256 `F58606B22D954BCACB8FDCEE5ED1CD309A44E6D0F03FF006AFBFD948B100D8DC`, and the state setup remained at `FD9F5F1BFBC7FE47E63C91CFCD29DD357A1B411E58FE80572BADC599A79D941C`. BIC retains `law_frontier_colonization`, does not contain `law_colonial_exploitation`, and no `bject` path exists. Map/state regions, ownership, character gameplay, country gameplay, laws, governments, diplomacy, localisation gameplay, military formations, technology gameplay, Konkan, Anandrao, and the duplicate Real Armada Espanola issue were untouched. The index remained empty.

## 31. Verdict

CLEANUP-2C-0 passes the static audit. The centralized non-Europe corpus is exhaustive at 148/148; the research queue is closed at 140; the eight validated cases are excluded from repeat research; and all 165 decentralized entities are cleanly separated for their future structural phase. The audit is safe to hand to ChatGPT for historical research, but no ruler implementation should begin until that research is complete.

```text
NON_EUROPE_GOVERNMENT_OK_TOTAL = 8
NON_EUROPE_GOVERNMENT_RESEARCH_REQUIRED_TOTAL = 140
NON_EUROPE_TITLE_RESEARCH_REQUIRED_TOTAL = 140
NON_EUROPE_CONSTITUTIONAL_RESEARCH_REQUIRED_TOTAL = 140
NON_EUROPE_MAP_DEPENDENT_TOTAL = 55
COLONIAL_OR_COMPANY_EXECUTIVE_RESEARCH_REQUIRED_TOTAL = 22
RESEARCH_GROUP_COUNT = 8
GAMEPLAY_FILES_CHANGED_BY_AUDIT = 0
CODEX_LAUNCHED_VICTORIA3 = NO
USER_RUNTIME_REQUIRED = NO
V13_STATIC_AUDIT_VALIDATION = PASS
SAFE_TO_BEGIN_NON_EUROPE_HISTORICAL_RESEARCH = YES
```

STOP.
