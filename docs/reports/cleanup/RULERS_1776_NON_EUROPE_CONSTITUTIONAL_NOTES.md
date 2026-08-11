# RULERS 1776 — NON-EUROPE CONSTITUTIONAL NOTES

## Purpose

This file separates three questions which must not be collapsed during implementation:

1. **Historical identity** — who actually held the relevant office on 1776-01-01?
2. **Constitutional role** — sovereign, regent, delegated governor, company executive, elected/confederal officer, or collective authority?
3. **Victoria 3 mapping** — can the fork tag honestly represent that polity without a later map/political-structure rework?

## Implementation doctrine

- `IMPLEMENT_*` means the historical person/office can be represented now, subject to technical validation in Victoria 3 1.13.
- `*_DEFERRED` means Codex must **not invent a replacement**. It may preserve a procedural placeholder if the engine requires one, but the report must classify the placeholder as intentional and unresolved.
- Map-dependent rows may receive a historically valid ruler only when the ruler identity itself is safe; territory, ownership, subject pacts and state regions remain outside this character phase unless the MASTER explicitly says otherwise.
- Colonies and chartered companies use the historical governor/company executive as the visible delegated executive where appropriate; the overlord remains the nominal sovereign framework.
- Collective polities must not be converted into hereditary monarchies merely to avoid an engine-generated character.
- For regencies, use the already validated Victoria 3 1.13 `regency_years` variable mechanism. Never reintroduce `designate_character_as_regent`.

## High-risk constitutional patterns

### Delegated colonial/company executives
DEI, BIC and the colonial governor tags must distinguish sovereign from executive. A Governor-General, governor or company officer is not a king.

### Child ruler / regency structures
NAG and TIB require a distinction between nominal ruler and effective regent. The historical packet supplies the identities; the technical implementation must follow the target 1.13 regency pattern already proven elsewhere in the fork.

### Nominal sovereign versus effective ruler
BUK, KHI, SAT, ETH and several Ottoman/Persian dependencies contain a real split between formal sovereignty and practical executive authority. The visible character choice must be explained, not silently flattened.

### Collective or fragmented structures
USA, CHC, CIR, HAW, KAU, UNT, PAN, DAI, BAL, SHS, BRG and similar rows cannot honestly be modeled as ordinary unitary hereditary monarchies. USA is the special exception where John Hancock can serve only as a temporary Congress-presiding abstraction while map/subject reconstruction remains deferred.

### Anachronistic tags
Examples include ALK, NBS, ONT, IQU, UNT, LAN, BST, ORA, PHL, SIL, SOK, TRN and WTU. Their later historical identities must not be projected backward into 1776.

## Per-tag constitutional register

### ARABIAN_PENINSULA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| BHN | Persian/Zand delegated rule through the Al-Madhkur family / **Sheikh / Governor** | Karim Khan Zand | Nasr al-Madhkur | Family/governorial succession under Persian paramountcy | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| HDJ | Hereditary sharifate under Ottoman suzerainty / **Sharif and Emir of Mecca** | Abdülhamid I | Surur ibn Musa'id | Succession within the Hashemite sharifian house, subject to Ottoman confirmation | `IMPLEMENT_DELEGATED_DYNASTIC_RULER` | HIGH |
| LAH | Abdali hereditary sultanate / **Sultan** |  | Fadl II ibn Abd al-Karim al-Abdali | Hereditary Abdali succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| OMA | Ibadi imamate with increasingly dynastic Al Bu Said rule / **Imam** |  | Ahmad bin Said al-Busaidi | Imamate selection evolved into dynastic rule within Al Bu Said | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| ZAI | Zaidi imamate under Qasimid dynasty / **Imam** |  | al-Mansur Ali I | Dynastic competition mediated by imamate legitimacy | `IMPLEMENT_HISTORICAL_RULER` | HIGH |

### CARIBBEAN

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| CUB | Spanish colonial captaincy general / **Governor and Captain General of Cuba** | Charles III of Spain | Felipe de Fonsdeviela | Appointed by Spanish Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| GR5 | Spanish colonial captaincy general / **Governor and Captain General of Santo Domingo** | Charles III of Spain | José Solano y Bote | Appointed by Spanish Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| HAI | French slave-plantation colony under royal administration / **Governor-General of Saint-Domingue** | Louis XVI of France | d'Ennery | Appointed by French Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| PCO | Spanish colonial captaincy / **Governor and Captain General of Puerto Rico** | Charles III of Spain | Miguel de Muesas | Appointed by Spanish Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |

### CAUCASUS

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| CHC | Decentralized clan/teip and local community structure / **Collective teip/community leadership** |  | Collective local elites | Distributed customary authority | `POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| CIR | Confederated/decentralized mixture of aristocratic principalities and communities / **Collective princely/community leadership** |  | Collective Circassian elites | Local princely and communal succession; no unitary executive | `POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |

### CENTRAL_AFRICA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| BGI | Centralized Bagirmi monarchy with Islamic court institutions / **Mbang / Sultan** |  | Muhammad al-Amin | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| KON | Kongo elective-dynastic monarchy after civil conflict / **Manikongo / King** |  | Álvaro XI | Royal election/selection among competing dynastic houses | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| WAD | Centralized Wadai monarchy/sultanate / **Kolak / Sultan** |  | Muhammad Jawda | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |

### CENTRAL_AMERICA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| MKT | Hereditary indigenous monarchy with British alliance/protectorate influence / **King of the Miskito** |  | George I | Hereditary; George II succeeded later in 1776 | `IMPLEMENT_HISTORICAL_RULER` | MEDIUM |
| SC1 | Spanish viceroyal monarchy/colonial administration / **Viceroy of New Spain** | Charles III of Spain | Bucareli | Appointed by Spanish Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |

### CENTRAL_ASIA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| BUK | Manghit de facto rule under a nominal Chinggisid khan / **Ataliq / de facto ruler** | Abu'l-Ghazi Khan | Daniyal Biy Ataliq | Dynastic Manghit succession in effective office; Chinggisid puppet khan retained | `IMPLEMENT_EFFECTIVE_HISTORICAL_RULER` | HIGH |
| KHI | Qongrat de facto rule behind a nominal khan / **Inaq / de facto ruler** | Abu'l Fayz Khan | Muhammad Amin Inaq | Qongrat household succession in effective office; puppet khan system | `IMPLEMENT_EFFECTIVE_HISTORICAL_RULER` | HIGH |
| KOK | Central Asian dynastic principality/khanate under Ming house / **Biy / ruler** |  | Narbuta Biy | Hereditary-dynastic succession, with chronology varying slightly by source | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| KZH | Kazakh khanate confederation with Russian protectorate influence / **Khan** |  | Nuraly Khan | Khan selected within Chinggisid elite with aristocratic support | `IMPLEMENT_HISTORICAL_RULER` | MEDIUM |
| OZH | Kazakh khanate/confederation / **Khan** |  | Ablai Khan | Election/recognition among Kazakh elites; Chinggisid dynasty | `IMPLEMENT_HISTORICAL_RULER` | MEDIUM |
| UZH | Kazakh confederal political structure / **Collective khan/chief structure** |  | Collective Senior Zhuz elites | Distributed authority among clans, sultans and Chinggisid claimants | `POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |

### EAST_AFRICA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| AGC | Swahili-Islamic coastal sultanate with local lineage politics / **Sultan** |  | Exact holder unresolved | Dynastic/lineage succession within Angoche ruling elite | `IDENTITY_RESEARCH_DEFERRED_PROCEDURAL_ALLOWED` | HIGH |
| ANK | Hereditary Hima monarchical polity / **Omugabe** |  | Rwabirere | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BNY | Hereditary Babiito monarchy / **Omukama** |  | Duhaga | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BRD | Hereditary sacral monarchy / **Mwami** |  | Mwambutsa III Syarushambo Butama | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BUG | Hereditary but clan-mediated Buganda monarchy / **Kabaka** |  | Kyabaggu Kabinuli | Dynastic succession conditioned by clan and court politics | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| KRG | Hereditary Haya monarchy / **Omugabe** |  | Ntare V Kiitabanyoro | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| MAD | Multiple Malagasy kingdoms and chiefdoms, including Imerina and others / **Multiple sovereign kingdoms** |  | Multiple regional rulers | Separate dynastic successions | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| MBS | Independent/semi-independent Mazrui coastal polity / **Sultan / ruler of Mombasa** |  | Abdallah ibn Muhammad al-Mazru'i | Dynastic succession in the Mazrui house | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| RWD | Hereditary/sacral Rwandan monarchy / **Mwami** |  | Kigeli III Ndabarasa | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| TGI | Swahili coastal sultanate/polity / **Sultan** |  | Exact holder unresolved | Dynastic/lineage succession | `IDENTITY_RESEARCH_DEFERRED_PROCEDURAL_ALLOWED` | MEDIUM |
| WTU | Coastal mainland communities before the 19th-century Witu state / **No Witu Sultanate in 1776** |  | No 1776 executive | Not applicable | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |

### EAST_ASIA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| EZO | Tokugawa feudal domain controlling trade/access in southern Ezo / **Daimyō** | Tokugawa Ieharu | Matsumae Michihiro | Hereditary daimyō succession under Tokugawa bakufu | `IMPLEMENT_HISTORICAL_RULER_WITH_MAP_CAVEAT` | MEDIUM |
| RYU | Hereditary monarchy with dual tributary/subordinate relations / **King** | Qianlong Emperor; Satsuma domain also exercised control | Shō Boku | Hereditary Shō dynasty | `IMPLEMENT_HISTORICAL_RULER` | HIGH |

### HORN_OF_AFRICA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| ETH | Solomonic monarchy during the Zemene Mesafint / Age of Princes / **Emperor** |  | Tekle Haymanot II | Dynastic imperial succession heavily constrained by regional nobles | `IMPLEMENT_HISTORICAL_NOMINAL_SOVEREIGN` | HIGH |
| GLD | Geledi dynastic sultanate / **Sultan** |  | Mahamud Ibrahim | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| ISQ | Clan-confederal sultanate / **Sultan** |  | Guled Abdi | Selection/hereditary continuity within the founding Guled line | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| MJT | Somali clan-state/sultanate with developing centralized authority / **Boqor / Sultan** |  | Exact holder unresolved | Dynastic/clan leadership | `IDENTITY_RESEARCH_DEFERRED_PROCEDURAL_ALLOWED` | MEDIUM |
| WSG | Somali clan sultanate / **Garaad / Sultan** |  | Garaad Ali | Dynastic/clan succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |

### INDIA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| AWA | Hereditary nawabi with Mughal-derived legitimacy and growing Company influence / **Nawab-Wazir** | Shah Alam II (nominal Mughal imperial framework) | Asaf-ud-Daula | Dynastic succession in the Nishapuri house | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BHV | Hereditary princely state of the Gohil dynasty / **Thakur Sahib / ruler** |  | Wakhatsinhji Akherajji | Hereditary dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| COC | Hereditary Cochin royal house under strong Dutch/VOC influence / **Raja / Maharaja** |  | Rama Varma VIII | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER_WITH_DIPLOMACY_DEFER` | LOW |
| COO | Hereditary monarchy under increasing East India Company/British protection / **Maharaja** |  | Dhairyendra Narayan | Dynastic succession restored after Bhutanese captivity | `IMPLEMENT_HISTORICAL_RULER` | MEDIUM |
| GAR | Hereditary Himalayan monarchy / **Raja** |  | Lalit Shah | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| GWA | Maratha dynastic chiefship within the wider confederacy / **Maharaja / Sardar** | Maratha Peshwa/Confederacy framework | Mahadji Shinde | Dynastic succession within Scindia house | `IMPLEMENT_HISTORICAL_RULER` | MEDIUM |
| JEY | Hereditary zamindari/kingdom under shifting regional and Company pressure / **Raja** |  | Vikram Dev | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | MEDIUM |
| KHP | Maratha Bhonsle hereditary monarchy / **Raja / Chhatrapati** |  | Shivaji II | Hereditary dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| KNO | Hereditary nawabi/princely state / **Nawab** |  | Munawar Khan | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| MLD | Hereditary sultanate / **Sultan** |  | Muhammad Mu'izz al-Din | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| NAG | Bhonsle dynastic state with child ruler/regency / **Regent / Senadhurandhar** | Raghoji II (minor nominal ruler) | Mudhoji Bhonsle | Dynastic succession with regency | `IMPLEMENT_REGENCY_STRUCTURE` | HIGH |
| PAN | Sikh misls confederacy, not a unified Punjab monarchy / **Jathedar / leading Sardar** |  | Dal Khalsa / misl chiefs; Jassa Singh Ahluwalia as leading figure | Confederal selection and misl leadership; no hereditary king of unified Punjab | `POLITICAL_STRUCTURE_REWORK_DEFERRED_WITH_HISTORICAL_ABSTRACTION` | LOW |
| PUD | Hereditary Tondaiman principality / **Raja** |  | Raghunatha Tondaiman | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| SAT | Maratha hereditary monarchy with effective Peshwa dominance / **Chhatrapati** | Rajaram II | Peshwa/Maratha confederate executive | Bhonsle dynastic succession; effective confederate administration by Peshwa | `IMPLEMENT_NOMINAL_HISTORICAL_SOVEREIGN` | HIGH |
| SIN | Hereditary Kalhora state under Durrani-era regional pressure / **Mian / ruler** |  | Ghulam Nabi Kalhoro | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| TRA | Hereditary Travancore monarchy / **Maharaja** |  | Karthika Thirunal Rama Varma | Matrilineal royal succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BIC | Chartered-company government under British Crown/Parliamentary framework / **Governor-General of Fort William** | George III of Great Britain | Warren Hastings | Company appointment under regulating legislation; not hereditary sovereignty | `VERIFY_AND_IMPLEMENT_DELEGATED_COMPANY_EXECUTIVE` | HIGH |

### MIDDLE_EAST

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| ARB | Arab tribal sheikhdom in Khuzestan under shifting Zand/Persian influence / **Sheikh** | Karim Khan Zand (regional Persian paramountcy) | Exact 1776 Banu Ka'b holder unresolved | Dynastic/tribal sheikhly succession | `MAP_DIPLOMACY_REWORK_DEFERRED` | LOW |
| DUR | Durrani hereditary monarchy / **Shah** |  | Timur Shah Durrani | Dynastic succession from Ahmad Shah Durrani | `FIX_SCRIPTED_UNVERIFIED_HISTORICAL_RULER` | HIGH |
| IR1 | Ottoman province with semi-autonomous Mamluk household administration / **Pasha / Wali** | Abdülhamid I | Omar Pasha | Appointment and household power within Ottoman sovereignty | `FIX_SCRIPTED_UNVERIFIED_DELEGATED_EXECUTIVE` | MEDIUM |

### NORTH_AFRICA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| AIT | Kabyle mountain principality/confederated lordship around the Mokrani house / **Sheikh of Medjana / Mokrani chief** |  | Mokrani house | Dynastic-clan succession amid fragmented Kabyle authority | `IDENTITY_MAP_REWORK_DEFERRED` | LOW |
| CON | Provincial beylik of the Regency of Algiers / **Bey** | Dey Muhammad V of Algiers | Salah Bey | Appointment by the Dey; not hereditary sovereign monarchy | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| DFR | Keira dynastic sultanate / **Sultan** |  | Muhammad Tayrab | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| MAS | Provincial beylik under the Dey of Algiers / **Bey** | Dey Muhammad V of Algiers | Ibrahim Bey of Miliana | Appointment by the Dey | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| MOR | Alaouite hereditary monarchy / **Sultan** |  | Mohammed ben Abdallah | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| TRI | Qaramanli hereditary-autonomous dynasty under nominal Ottoman sovereignty / **Pasha** | Abdülhamid I | Ali I Qaramanli | Hereditary dynastic rule with Ottoman recognition | `IMPLEMENT_DELEGATED_DYNASTIC_RULER` | HIGH |
| TUG | Beni Djellab hereditary oasis sultanate under Regency of Algiers suzerainty/tribute / **Sultan** | Dey of Algiers | Ahmed VIII ben Amrane | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER_WITH_DEPENDENCY` | HIGH |
| TUN | Husainid hereditary beylik under nominal Ottoman sovereignty / **Bey** | Abdülhamid I | Ali II ibn Hussein | Hereditary Husainid succession with Ottoman suzerainty | `IMPLEMENT_DELEGATED_DYNASTIC_RULER` | HIGH |

### NORTH_AMERICA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| USA | Revolutionary intercolonial congress; no U.S. presidency existed / **President of the Continental Congress** | George III of Great Britain | Continental Congress (collective), chaired by John Hancock | Congress elected its president; executive authority collective/committee-based | `MAP_REWORK_DEFERRED_WITH_TEMPORARY_CONGRESS_EXECUTIVE` | LOW |
| ALK | No centralized Russian-American Company government existed / **** | Catherine II of Russia |  | N/A | `MAP_REWORK_DEFERRED` | LOW |
| HBC | Chartered joint-stock company under royal charter / **Governor of the Hudson's Bay Company** | George III of Great Britain | Sir Bibye Lake Jr. and the Company Committee | Governor/committee elected by company proprietors | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| LOU | Spanish colonial province / **Governor of Louisiana** | Charles III of Spain | Luis de Unzaga | Appointed by Spanish Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| NBS | Part of the British colony of Nova Scotia / **** | George III of Great Britain | Francis Legge as governor of Nova Scotia | N/A | `MAP_REWORK_DEFERRED` | LOW |
| NVS | British royal colony / **Governor of Nova Scotia** | George III of Great Britain | Francis Legge | Appointed by British Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| ONT | Province of Quebec and indigenous polities; Upper Canada did not exist / **** | George III of Great Britain | Guy Carleton for the Province of Quebec where applicable | N/A | `MAP_REWORK_DEFERRED` | LOW |
| QUE | British royal province under Quebec Act / **Governor of Quebec** | George III of Great Britain | Guy Carleton | Appointed by British Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |

### OCEANIA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| HAW | Multiple island chiefdoms / **Multiple aliʻi nui** |  | Multiple high chiefs, including Kalaniʻōpuʻu on Hawaiʻi | Hereditary chiefly succession by island/district | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| KAU | Kaurna clan/local-group social structure / **Clan/community elders** |  | Collective Kaurna local groups | Kinship and local customary leadership | `POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| PLY | Tahitian chiefdoms with increasing paramountcy, not yet the later unified Pōmare kingdom / **Paramount chief** |  | Tū (Otoo) | Hereditary chiefly succession within elite lineages | `IMPLEMENT_HISTORICAL_CHIEF_WITH_DIPLOMACY_DEFER` | LOW |
| UNT | Independent iwi and hapū / **No United Tribes executive** |  | Multiple rangatira | Distributed chiefly authority | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |

### SOUTHEAST_ASIA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| DEI | Dutch East India Company delegated colonial government / **Governor-General of the Dutch East Indies** | Dutch Republic / VOC directors | Jeremias van Riemsdijk | VOC appointment by company institutions; not hereditary sovereignty | `FIX_P0_HISTORICAL_EXECUTIVE` | HIGH |
| ACE | Hereditary Acehnese sultanate / **Sultan** |  | Alauddin Mahmud Syah I | Dynastic succession with elite contestation | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BAL | Multiple Balinese kingdoms with Klungkung holding ritual/prestige primacy / **Dewa Agung / multiple rajas** |  | Dewa Agung of Klungkung plus other Balinese rajas | Hereditary rulers in separate kingdoms | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| BLG | Hereditary sultanate with regional dependency ties / **Sultan** |  | Wira Amir (Amiril Mukminin) | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | MEDIUM |
| BNJ | Hereditary Banjar sultanate / **Sultan** |  | Tahmidullah II | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BRU | Hereditary Bruneian sultanate / **Sultan** |  | Omar Ali Saifuddin I | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BTN | Butonese sultanate with elite/elective elements / **Sultan** |  | La Jampi (Kaimuddin) | Selection within ruling elite/dynastic structure | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BUR | Konbaung hereditary monarchy / **King** |  | Hsinbyushin | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| CAM | Khmer monarchy amid Siamese/Vietnamese rivalry / **King** |  | Ang Non II | Dynastic succession heavily conditioned by regional intervention | `IMPLEMENT_HISTORICAL_RULER_WITH_DIPLOMACY_DEFER` | MEDIUM |
| CHP | Lao hereditary kingdom / **King / Chao** |  | Sayakumane | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER_WITH_DIPLOMACY_DEFER` | LOW |
| CMI | Lan Na city-state in a highly unstable Burmese/Siamese frontier transition / **Ruler / governor of Chiang Mai** |  | Phraya Wichianprakarn | Appointed/local princely leadership amid warfare | `IMPLEMENT_HISTORICAL_EXECUTIVE_WITH_MAP_DIPLOMACY_DEFER` | LOW |
| DAI | Fragmented north/south Vietnamese political order during Tây Sơn rebellion / **Multiple rulers: Lê Hiển Tông / Trịnh Sâm / Nguyễn Phúc Thuần / Tây Sơn leadership** |  | Multiple competing executives | Separate dynastic and military regimes | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| JMB | Hereditary Malay sultanate / **Sultan** |  | Chronology disputed between Ahmad Zainuddin Anom and Masud Badaruddin | Dynastic succession | `IDENTITY_CHRONOLOGY_DEFERRED` | HIGH |
| JOH | Hereditary Malay sultanate with Bugis/Yamtuan Muda power-sharing / **Sultan** |  | Mahmud Riayat Shah III | Dynastic succession alongside powerful Bugis officeholders | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| KTI | Hereditary Kutai sultanate / **Sultan** |  | Aji Kado (Sultan Aji Muhammad Aliyeddin) | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| LAN | Chinese mining/community organizations in western Borneo before the Lanfang polity / **No 1776 ruler** |  | No 1776 Lanfang executive | Not applicable before founding | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| LUA | Lao hereditary monarchy under changing Burmese/Siamese pressure / **King** |  | Surinyavong II | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER_WITH_DIPLOMACY_DEFER` | LOW |
| MGD | Hereditary Maguindanao sultanate / **Sultan** |  | Pahar Ud-Din | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| PHI | Spanish colonial captaincy/governor-generalship / **Governor-General of the Philippines** | Charles III of Spain | Simón de Anda y Salazar | Royal appointment | `IMPLEMENT_DELEGATED_COLONIAL_EXECUTIVE` | HIGH |
| PON | Emerging Malay-Arab riverine principality / **Sharif / founding prince** |  | Syarif Abdurrahman Alkadrie | Dynastic founder; formal sultanate title consolidated later | `IMPLEMENT_HISTORICAL_CHIEF` | HIGH |
| PRK | Hereditary Malay sultanate / **Sultan** |  | Alauddin Mansur Shah Iskandar Muda | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| SAK | Hereditary Malay sultanate / **Sultan** |  | Muhammad Ali Abdul Jalil Muazzam Shah | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| SEL | Hereditary Bugis-Malay sultanate / **Sultan** |  | Salahuddin Shah (Raja Lumu) | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| SHS | Multiple hereditary Shan principalities / **Multiple saophas** |  | Multiple saophas | Hereditary saopha succession in individual states | `POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| SIA | Centralizing Thai monarchy after the fall of Ayutthaya / **King** |  | Taksin | Monarchical succession established by military/political conquest | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| SMB | Hereditary Malay sultanate / **Sultan** |  | Umar Akamuddin II | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| SRK | Javanese court monarchy under strong VOC influence / **Susuhunan** |  | Pakubuwono III | Dynastic court succession conditioned by VOC intervention | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| STG | Hereditary Bornean sultanate / **Sultan** |  | Abdurrahman Muhammad Jalaluddin | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| SUL | Hereditary Sulu sultanate / **Sultan** |  | Mohammad Israel | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| TID | Hereditary Malukan sultanate under VOC pressure / **Sultan** |  | Jamaluddin | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| YOG | Javanese hereditary sultanate under VOC treaty framework / **Sultan** |  | Hamengkubuwono I | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |

### SOUTHERN_AFRICA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| BST | Pre-Moshoeshoe Sotho communities / **No 1776 Basotho state ruler** |  | Multiple local chiefs | Distributed local/chiefly authority | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| ORA | Region inhabited by indigenous communities before the 19th-century Boer republic / **No 1776 state ruler** |  | No 1776 executive | Not applicable | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| PHL | Pre-19th-century Khoekhoe/Griqua communities; Philippolis settlement not yet founded / **No 1776 Philippolis polity** |  | No 1776 executive | Not applicable | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| SWZ | Hereditary Dlamini monarchy with dual royal institutions / **King / Ngwenyama** |  | Ngwane III | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| TRN | Indigenous polities and communities before 19th-century Boer republic formation / **No 1776 state ruler** |  | No 1776 executive | Not applicable | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| WBL | Khoekhoe/Griqua community leadership before later territorial Griqualand states / **Kaptyn / community leader** |  | Adam Kok I | Community/chiefly succession | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED_WITH_HISTORICAL_LEADER` | LOW |

### SOUTH_AMERICA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| BRZ | Portuguese colonial viceroyal administration / **Viceroy of Brazil** | Joseph I of Portugal | Marquis of Lavradio | Appointed by Portuguese Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| IQU | Spanish colonial district/local indigenous communities / **** | Charles III of Spain |  | N/A | `MAP_REWORK_DEFERRED` | LOW |
| SC2 | Spanish viceroyal administration / **Viceroy of New Granada** | Charles III of Spain | Manuel de Guirior | Appointed by Spanish Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| SC3 | Spanish viceroyal administration / **Viceroy of Peru** | Charles III of Spain | Manuel de Amat | Appointed by Spanish Crown | `IMPLEMENT_DELEGATED_EXECUTIVE` | MEDIUM |
| SC4 | Spanish colonial governorate; Río de la Plata viceroyalty not yet operational / **Governor of Buenos Aires** | Charles III of Spain | Juan José de Vértiz y Salcedo | Appointed by Spanish Crown | `MAP_REWORK_DEFERRED_WITH_TEMPORARY_EXECUTIVE` | LOW |

### SOUTH_ASIA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| BHU | Bhutanese dual system of government / **Druk Desi** | Zhabdrung institution (religious sovereignty) | Kunga Rinchen | Druk Desi office selected within dual religious-secular polity | `IMPLEMENT_HISTORICAL_EXECUTIVE` | HIGH |
| NEP | Shah hereditary monarchy / **King** |  | Pratap Singh Shah | Hereditary Shah succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| SIK | Hereditary Namgyal monarchy / **Chogyal** |  | Phuntsog Namgyal II | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| TIB | Ganden Phodrang theocratic government under a regency and Qing imperial influence / **Regent / Desi** | Jamphel Gyatso, 8th Dalai Lama | Demo Tulku | Dalai Lama reincarnation with appointed regent during minority | `IMPLEMENT_REGENCY_STRUCTURE` | HIGH |

### WEST_AFRICA

| Tag | 1776 government / office | Nominal sovereign | Effective executive | Succession / selection | V3 decision | Mapping confidence |
|---|---|---|---|---|---|---|
| ASH | Asante centralized monarchy with matrilineal dynastic selection and council constraints / **Asantehene** |  | Osei Kwadwo | Selection from eligible royal matrilineages with political approval | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BEN | Hereditary Benin monarchy / **Oba** |  | Akengbuda | Dynastic succession within the royal house | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BOR | Sefuwa dynastic monarchy / **Mai** |  | Ali IV | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| BRG | Cluster/confederation of related Bariba/Borgu kingdoms / **Multiple rulers (Nikki, Bussa, Illo and others)** |  | Multiple Borgu potentates | Separate dynastic successions in multiple capitals | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| DAH | Centralized Fon monarchy / **Ahosu / King** |  | Kpengla | Dynastic royal succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| FTJ | Islamic confederation/theocratic state / **Almamy** |  | Ibrahima Sori | Elective/alternating elite arrangements rather than simple hereditary monarchy | `IMPLEMENT_ELECTIVE_HISTORICAL_EXECUTIVE` | HIGH |
| FTR | Political revolution and formation of the Almamate of Futa Toro / **Transitional 1776 leadership** |  | Sulayman Bal / Abdul Kader emerge during the 1776 transition | Denianke dynastic rule replaced by elective Islamic almamy system during 1776 | `TRANSITION_1776_IDENTITY_DEFERRED` | MEDIUM |
| HAU | Hausa hereditary/elite monarchy / **Sarkin Gobir** |  | Bawa Jan Gwarzo | Dynastic and elite succession | `IDENTITY_CHRONOLOGY_DEFERRED` | HIGH |
| KRT | Bambara dynastic kingdom / **Faama** |  | Sira Bo | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| MSN | Fulbe polity under the broader political dominance/tributary framework of Segou / **Ardo Mawdo / Fondoko** | Segou/Bambara paramountcy | Hamadou-Amina III | Local dynastic/chiefly succession | `IMPLEMENT_HISTORICAL_RULER_WITH_DEPENDENCY_CAVEAT` | MEDIUM |
| OYO | Yoruba imperial monarchy with strong constitutional checks by Oyo Mesi/Bashorun / **Alaafin** |  | Abiodun | Dynastic royal selection constrained by council institutions | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| SGU | Bambara dynastic monarchy / **Faama** |  | Ngolo Diarra | Dynastic succession | `IMPLEMENT_HISTORICAL_RULER` | HIGH |
| SIL | West African societies; British-sponsored settlement had not yet been founded / **No British Sierra Leone colony in 1776** |  | No 1776 colonial executive | Not applicable | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
| SOK | Hausa/Fulani societies before Usman dan Fodio's jihad / **No Sokoto state in 1776** |  | No 1776 Sokoto executive | Not applicable | `MAP_POLITICAL_STRUCTURE_REWORK_DEFERRED` | LOW |
