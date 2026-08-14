# CLEANUP-2D-5D — Historical Generals 1776 — Northern & Eastern Europe

## Status

- **Project:** Victoria 3 — *1776 – Age of Revolutions*
- **Repository:** `Malzars-sys/1776-Age-of-Revolutions`
- **Branch audited:** `cleanup-post-release`
- **Immutable reference date:** **1776-01-01**
- **Mode:** **historical research only**
- **Gameplay edits:** **none**
- **Commit / push:** **none**
- **Purpose:** identify a historically defensible starting commander for every current land formation in the northern/eastern-European scope, while explicitly preferring a procedural general over a forced historical mapping.

This report deliberately separates three questions that must not be conflated:

1. Was the person alive and militarily active on **1776-01-01**?
2. Did the person hold the relevant command **already on that exact date**?
3. Does that historical command actually map to the mod formation, rather than merely belonging to the same country?

A famous officer can therefore pass (1) and still fail (2) or (3).

---

## 1. Repository scope audit

The current `00_military_formations_europe.txt` on `cleanup-post-release` yields the following in-scope or boundary land formations:

- CRI — `cleanup2d3e_r1_cri_land_1`
- PLC — `cleanup2d3e_r1_plc_land_1`
- RUS — `cleanup2d3b_rus_land_1`
- RUS — `cleanup2d3b_rus_land_2`
- RUS — `cleanup2d3b_rus_land_3`
- RUS — `cleanup2d3b_rus_land_4`
- RUS — `cleanup2d3b_rus_land_5`
- CIR — `cleanup2d3e_r1_cir_land_1`
- CHC — `Murtazeki`
- SWE — `Kungliga_Svenska_Armn`
- DENNOR — `Hren`
- GAL — `cleanup2d3b_gal_land_1` (**boundary case:** Eastern-Europe HQ but Habsburg institutional scope)

### Baltic audit

No independent Baltic land formation requiring a separate general is present in the current branch's European formation setup. The repo does contain a UBD/Baltic political character setup (George Browne as a temporary visible administrator), but that does **not** create a separate current Baltic land formation to populate in this phase.

### Existing starting generals found

- PLC already uses **Franciszek Ksawery Branicki**.
- RUS `land_4` already uses **Pyotr Rumyantsev**.
- The other primary formations above currently use procedural generals.
- The current Russian formation names/scopes are abstractions; they must not be retroactively treated as proof that a historical “II/III/IV/V Corps” with the same identity existed in 1776.

Repository formation source:
https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/00_military_formations_europe.txt

---

## 2. Executive decision matrix

| Tag | Formation | Best candidate | Mapping class | Decision | Mapping confidence |
|---|---|---|---|---|---|
| CRI | `cleanup2d3e_r1_cri_land_1` | PROCEDURAL_GENERAL | NO_DEFENSIBLE_MAPPING | **KEEP_PROCEDURAL** | HIGH |
| PLC | `cleanup2d3e_r1_plc_land_1` | Franciszek Ksawery Branicki | MILITARY_OFFICEHOLDER / HIGHER_COMMAND_ABSTRACTION | **KEEP_EXISTING_HISTORICAL** | MEDIUM-HIGH |
| RUS | `cleanup2d3b_rus_land_1` | Grigory Alexandrovich Potemkin | FORMATION_COMMAND / THEATRE_COMMAND | **IMPLEMENT_HISTORICAL** | MEDIUM-HIGH |
| RUS | `cleanup2d3b_rus_land_2` | PROCEDURAL_GENERAL | NO_DEFENSIBLE_MAPPING | **KEEP_PROCEDURAL** | HIGH |
| RUS | `cleanup2d3b_rus_land_3` | PROCEDURAL_GENERAL | NO_DEFENSIBLE_MAPPING | **KEEP_PROCEDURAL** | HIGH |
| RUS | `cleanup2d3b_rus_land_4` | Pyotr Alexandrovich Rumyantsev | THEATRE_COMMAND / HIGHER_COMMAND_ABSTRACTION | **KEEP_EXISTING_HISTORICAL** | MEDIUM-HIGH |
| RUS | `cleanup2d3b_rus_land_5` | Johann (Ivan) Alexandrovich Clapier de Colongue / Decolong | FORMATION_COMMAND | **IMPLEMENT_HISTORICAL** | HIGH |
| CIR | `cleanup2d3e_r1_cir_land_1` | PROCEDURAL_GENERAL | COLLECTIVE_HIGH_COMMAND / NO_DEFENSIBLE_MAPPING | **KEEP_PROCEDURAL** | HIGH |
| CHC | `Murtazeki` | PROCEDURAL_GENERAL | NO_DEFENSIBLE_MAPPING | **KEEP_PROCEDURAL** | HIGH |
| SWE | `Kungliga_Svenska_Armn` | Georg Magnus Sprengtporten | FORMATION_COMMAND / THEATRE_COMMAND | **IMPLEMENT_HISTORICAL** | MEDIUM-HIGH |
| DENNOR | `Hren` | PROCEDURAL_GENERAL | NO_DEFENSIBLE_MAPPING | **KEEP_PROCEDURAL** | HIGH |
| GAL | `cleanup2d3b_gal_land_1` | DEFER_TO_CLEANUP-2D-5C | OUT_OF_PHASE_HABSBURG_BOUNDARY | **DEFER_TO_CLEANUP-2D-5C** | HIGH |

### Net result

**Implementable historical replacements recommended by research:**

- RUS `land_1` → **Grigory Alexandrovich Potemkin**
- RUS `land_5` → **Johann/Ivan Clapier de Colongue (Decolong)**
- SWE `Kungliga_Svenska_Armn` → **Georg Magnus Sprengtporten**

**Existing historical selections retained, but with stricter classification:**

- PLC → **Franciszek Ksawery Branicki**, only as **high-command/military-officeholder abstraction**
- RUS `land_4` → **Pyotr Rumyantsev**, only as **southern theatre/higher-command abstraction**

**Procedural retained:**

- CRI
- RUS `land_2`
- RUS `land_3`
- CIR
- CHC
- DENNOR

**Boundary:**

- GAL → defer to **CLEANUP-2D-5C Habsburg/Central Europe** rather than double-research it here.

---

# 3. Russian Empire

## 3.1 RUS land_1 — Grigory Alexandrovich Potemkin

### Decision

**IMPLEMENT_HISTORICAL**  
Classification: **FORMATION_COMMAND / THEATRE_COMMAND**  
Historical confidence: **VERY HIGH**  
Mapping confidence: **MEDIUM-HIGH**

### Why Potemkin passes the absolute-date test

The strongest exact-date find in the Russian audit is an order dated **1 January 1776** itself: Potemkin was ordered to command the **Saint Petersburg Division** temporarily while Kirill Razumovsky was on leave. This is not a “later in 1776” inference; the command begins on the immutable reference date.

Potemkin was already deeply embedded in the guard/high-command structure:

- commander of the **Preobrazhensky Life Guards** from March 1774;
- army-inspection responsibilities from 1774;
- temporary command of the Saint Petersburg Division from January 1776.

This makes him much more defensible for the current `gvardeyskiy_korpus_army` / guard-grenadier abstraction than inserting an officer merely because he was famous.

### Biographical record

- Exact name: **Grigory Alexandrovich Potemkin-Tavrichesky**
- Birth: **30 September 1739 Old Style / 11 October 1739 New Style**
- Precision: **DAY**
- Birthplace: **Chizhovo, Smolensk uezd**
- Birth polity: **Russian Empire**
- V3 mapping: **STATE_SMOLENSK**
- Death: **5 October 1791 OS / 16 October 1791 NS**
- Culture: Russian
- Religion: Russian Orthodox
- Social origin: hereditary Russian nobility / officer family

### Gameplay-profile suggestions

These are **mapping proposals, not historical facts**:

- IG: `ig_armed_forces`
- ideology: leave unset rather than impose a modern ideological label
- possible trait: `innovative` — **MEDIUM confidence**, reflecting organizational/reform activity rather than battlefield style

### Portrait / DNA

Multiple late-18th-century portraits survive, including well-known Potemkin portraits in the Lampi tradition. No dedicated Potemkin DNA/template was found in the inspected current-branch DNA or Russian template files.

Sources:
- https://bigenc.ru/c/potiomkin-tavricheskii-grigorii-aleksandrovich-f16459
- https://ru.wikisource.org/wiki/РБС/ВТ/Потемкин,_Григорий_Александрович
- https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/character_templates/country_rus.txt
- https://github.com/Malzars-sys/1776-Age-of-Revolutions/tree/cleanup-post-release/common/dna_data

---

## 3.2 RUS land_2 — keep procedural

### Decision

**KEEP_PROCEDURAL**

The current formation is an artificial aggregation of Oryol/Yaroslavl/Kharkov elements. A senior Russian commander can be found, but no evidence establishes a direct 1776 command equivalent to this specific setup.

### Rejected alternate: Mikhail Nikitich Volkonsky

Volkonsky is a legitimate period officer and was active in the Moscow command system. He therefore passes the general activity test, but fails the **formation mapping** test.

**Decision:** `REJECT_FOR_MAPPING`

This is precisely the kind of case where a procedural general is historically safer than assigning a real name to the wrong force.

---

## 3.3 RUS land_3 — keep procedural

### Decision

**KEEP_PROCEDURAL**

The formation combines Kharkov, Tambov and Kursk components. No one-to-one 1776 formation commander was established with sufficient confidence.

Do **not** use Suvorov here as a generic prestigious substitute.

---

## 3.4 RUS land_4 — Pyotr Alexandrovich Rumyantsev

### Decision

**KEEP_EXISTING_HISTORICAL**  
Classification: **THEATRE_COMMAND / HIGHER_COMMAND_ABSTRACTION**  
Historical confidence: **VERY HIGH**  
Mapping confidence: **MEDIUM-HIGH**

### Re-evaluation of the existing selection

Rumyantsev is fully admissible on **1776-01-01**. The important correction is the *reason* he is admissible.

He should **not** be described as the literal commander of a historical “IV Infantry Corps” corresponding to the mod label. Instead, he held a powerful southern territorial/military complex of offices:

- **Field Marshal** since 1770;
- **Little Russian Governor-General** from 1764;
- president of the **Little Russian Collegium**;
- chief commander of the Little Russian Cossack regiments, Zaporozhians and Ukrainian Division;
- Sloboda-Ukrainian governor-general responsibilities;
- surviving document series explicitly group his command of troops in southern Russia from the mid-1770s.

The current `region_balkans`/southern formation can therefore abstract his theatre-level responsibilities, but only if the implementation documentation says so.

### Biographical record

- Exact name: **Pyotr Alexandrovich Rumyantsev-Zadunaisky**
- Birth: **4 January 1725 OS / 15 January 1725 NS**
- Precision: **DAY**
- Birthplace: **Moscow**
- Birth polity: **Russian Empire**
- V3 state: **STATE_MOSCOW**
- Death: **8 December 1796 OS / 19 December 1796 NS**
- Rank on reference date: **Field Marshal**
- Culture: Russian
- Religion: Russian Orthodox
- Social origin: Russian noble military-diplomatic family

### Gameplay-profile suggestions

- IG: `ig_armed_forces`
- ideology: unset
- possible trait: `innovative` — **MEDIUM**, gameplay interpretation only

### Portrait / DNA

Portrait record: **yes**.  
Dedicated current-branch DNA/template: **none found**.

Sources:
- https://old.bigenc.ru/domestic_history/text/3520474
- https://old.bigenc.ru/domestic_history/text/2169858
- https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/character_templates/country_rus.txt
- https://github.com/Malzars-sys/1776-Age-of-Revolutions/tree/cleanup-post-release/common/dna_data

---

## 3.5 RUS land_5 — Johann/Ivan Clapier de Colongue (Decolong)

### Decision

**IMPLEMENT_HISTORICAL**  
Classification: **FORMATION_COMMAND**  
Historical confidence: **HIGH for office; MEDIUM for dates because authoritative records conflict**  
Mapping confidence: **HIGH**

### Why this is the cleanest Russian formation match

Decolong was commander of the **Siberian Corps from 1771 to 1777**. An academic study of Siberian military administration confirms that this corps covered the large Siberian defensive-line system and East Siberian military space.

That is a substantially better match for the mod's Siberian `land_5` than a general chosen solely by fame.

### Biographical conflict — must be preserved

Two serious reference traditions disagree:

**Erik-Amburger database**
- Johann Clapier de Colongue
- birth: **13 November 1719 OS / 24 November 1719 NS**
- death: **15 February 1789 OS / 26 February 1789 NS**
- culture/origin: **Deutschbalte**
- religion: explicitly **no information**

**Russian archival guide (RGVIA)**
- gives a **1716–1779** lifespan.

Therefore:

- do **not** silently merge the dates;
- if a future implementation needs a single game birth date, the Amburger exact date is the best precise candidate found, but the source conflict must remain documented;
- exact birthplace was **not securely established** in this pass, so no V3 birth state should be invented.

### Office on 1776-01-01

- rank: **Lieutenant General**
- function: **Commander, Siberian Corps**
- command: **1771–1777**
- active on reference date: **YES**

### Profile

- Culture: Baltic German / Deutschbalte
- Religion: **UNKNOWN**
- Social background: Baltic-German military/engineering officer milieu
- IG suggestion: `ig_armed_forces`
- possible trait: `meticulous` — **LOW-MEDIUM**, gameplay interpretation from engineer career

### Portrait / DNA

No reliable portrait was confirmed in this pass.  
No dedicated mod DNA/template was found.

Sources:
- https://guides.rusarchives.ru/terms/15/8321/kancelyariya-general-poruchika-dekolonga-klape-klapir-de-kolonga-ia
- https://journals.rcsi.science/2311-1402/article/view/254286/ru_RU
- https://amburger.ios-regensburg.de/index.php?id=2589

---

## 3.6 Alexander Vasilyevich Suvorov — mandatory rejection at reference date

### Decision

**REJECT_FOR_REFERENCE_DATE**

This rejection is not a judgment on Suvorov's importance. It follows the immutable setup rule.

The Russian biographical record places him at the beginning of 1776 **attached to the Saint Petersburg Division under Potemkin**. He was subsequently transferred to the Moscow Division. His **Crimean Corps** appointment comes only in **November 1776**.

Therefore he is:

- alive: **YES**
- active officer: **YES**
- already holding a qualifying current-formation command on 1776-01-01: **NO**

He must not replace one of the starting procedural generals simply because his career becomes more important later in the same year.

### Birth-date warning

Suvorov's birth year/location has a genuine historiographical dispute. Sources preserve 1729/1730 alternatives and several location hypotheses. The CSV deliberately does **not** fabricate a single clean date.

Sources:
- https://bigenc.ru/c/suvorov-aleksandr-vasil-evich-176290
- https://suvorovmuseum.ru/en/%D0%BE-%D1%81%D1%83%D0%B2%D0%BE%D1%80%D0%BE%D0%B2%D0%B5

---

# 4. Polish–Lithuanian Commonwealth

## 4.1 Franciszek Ksawery Branicki

### Decision

**KEEP_EXISTING_HISTORICAL**  
Classification: **MILITARY_OFFICEHOLDER / HIGHER_COMMAND_ABSTRACTION**  
Historical confidence: **HIGH**  
Mapping confidence: **MEDIUM-HIGH**

Branicki was **Grand Crown Hetman from 8 February 1774**, so he clearly held a major military office on 1 January 1776.

However, this does **not** mean he directly commanded a single unified field army equivalent to the mod's entire PLC formation.

### Essential structural distinction

The Commonwealth's military system was not a single modern national chain of command:

- Crown and Grand Duchy of Lithuania retained distinct military traditions/structures;
- Lithuanian military administration cannot be folded under the Crown hetman without qualification;
- reforms around the Permanent Council and Military Department restricted the old autonomous powers of the hetmans;
- Branicki's own conflict over the scope of hetman authority in 1775–1776 is evidence of this contested structure.

Therefore the correct classification is:

> **high Crown military officeholder represented through a single-game-army abstraction**

—not “direct general of all Polish-Lithuanian troops”.

### Biographical record

- Exact name: **Franciszek Ksawery Branicki h. Korczak**
- Birth: **circa 1730**
- Precision: **YEAR (circa)** — no day/month invented
- Place: **Barwałd**, usually identified as Barwałd Górny
- Birth polity: Polish–Lithuanian Commonwealth, Crown of Poland
- V3 mapping: **STATE_WEST_GALICIA**, medium confidence
- Death: **April 1819**, no day fabricated
- Culture: Polish
- Religion: Roman Catholic, high-confidence contextual identification
- Origin: magnate / szlachta

### Gameplay-profile suggestions

- IG: `ig_landowners`
- ideology: `ideology_traditionalist` — **MEDIUM**, gameplay interpretation of his defense of traditional hetman prerogatives, not a literal self-described ideology
- traits: leave empty unless a later gameplay pass finds a narrowly sourced military trait

### Portrait / DNA

Portrait record: **yes**, with multiple surviving images.  
Dedicated Branicki DNA/template: **none found**.

Sources:
- https://www.ipsb.nina.gov.pl/a/biografia/franciszek-ksawery-branicki-h-korczak-zm-1819-hetman-wielki-koronny
- https://encyklopediakrakowa.pl/slawni-i-zapomniani/86-b/598-branicki-franciszek-ksawery.html
- https://www.ldkistorija.lt/commissions-on-war-and-treasury-of-the-grand-duchy-of-lithuania/
- https://ruj.uj.edu.pl/entities/publication/27f16ecb-6d2e-45ec-b738-8e269ae05479
- https://czasopisma.uni.lodz.pl/pnh/article/view/27290
- https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/character_templates/country_plc.txt

---

# 5. Sweden

## 5.1 Georg Magnus Sprengtporten

### Decision

**IMPLEMENT_HISTORICAL**  
Classification: **FORMATION_COMMAND / THEATRE_COMMAND**  
Historical confidence: **VERY HIGH**  
Mapping confidence: **MEDIUM-HIGH**

The Swedish National Archives' *Svenskt biografiskt lexikon* gives an unusually clean period command:

- **Colonel of the Savolax infantry**
- **Chief of the Savolax Brigade**
- tenure: **9 March 1775 – 27 May 1779**

He is therefore unquestionably in command on **1 January 1776**.

The same biography emphasizes the importance of the Savolax force in Finland, making Sprengtporten a defensible representative commander for the mod's single Swedish land formation, though the game formation is broader than his historical brigade.

### Biographical record

- Name: **Georg (Göran) Magnus Sprengtporten**
- Birth: **16 August 1740**, source-stated SBL date
- Precision: **DAY**
- Place: **Borgå rural parish (Porvoo), Nyland**
- Birth polity: **Kingdom of Sweden**
- V3 state: **STATE_UUSIMAA**
- Death: **19 September OS / 1 October NS 1819**, Saint Petersburg
- Rank on 1776-01-01: **Colonel**
- Culture: Swedish / Finland-Swedish
- Religion: Lutheran
- Origin: noble military family

### Calendar warning

Sweden had not yet adopted the Gregorian calendar at Sprengtporten's birth in 1740. The report preserves the SBL source-stated date and does **not** silently rewrite the day. A future implementation should follow one consistent project-wide calendar convention.

### Gameplay-profile suggestions

- IG: `ig_armed_forces`
- ideology: unset
- traits: `innovative`, `forest_commander` — **MEDIUM-HIGH** thematic fit because his career includes training, maneuvers and Finnish forest/theatre experience

### Portrait / DNA

A portrait by **B. Godenhjelm** is preserved in the Cygnaeus Gallery tradition and has a public-domain reproduction.  
No dedicated Sprengtporten DNA/template was found.

Source:
- https://sok.riksarkivet.se/sbl/Presentation.aspx?id=20013

---

# 6. Denmark–Norway

## 6.1 Formation `Hren`

### Decision

**KEEP_PROCEDURAL**

This conclusion follows from the command evidence, not from lack of research.

## 6.2 Karl of Hesse-Kassel — rejected

SNL distinguishes his long **formal** title from periods when he actually functioned as commanding general in Norway.

- first effective period: **1772–1774**
- returned to Schleswig after 1774
- effective again in **1788**
- therefore **not an effective Norwegian commander on 1776-01-01**

**Decision:** `REJECT_NOT_EFFECTIVE_ON_REFERENCE_DATE`

Sources:
- https://snl.no/kommanderende_general
- https://snl.no/Karl_av_Hessen

## 6.3 Georg Frederik von Krogh — historically strong, mapping weak

The Norwegian Digital Archives preserve a military roll dated **16 December 1775** explicitly identifying the **1st Trondhjemske National Infantry Regiment** as under Major General Georg Frederik von Krogh's command.

This is excellent direct evidence that Krogh was commanding a real unit immediately before the reference date.

However:

- it is a **Trondheim** regimental command;
- the mod's only Denmark–Norway army is a much broader abstraction and is materially based around Eastern Norway;
- Krogh's broader northern commanding-general role belongs to **1788**, not 1776.

Thus:

**Decision:** `REJECT_FOR_MAPPING_GEOGRAPHY`

This is a textbook case for retaining the procedural general.

Sources:
- https://www.digitalarkivet.no/source/100435
- https://nbl.snl.no/Georg_Frederik_von_Krogh

## 6.4 Heinrich Wilhelm von Huth

Huth is an important contemporary general and had over-command responsibilities during the 1772 Norwegian alert, but the research did not establish an exact continuing whole-army effective command on 1776-01-01 sufficient to displace the procedural solution.

Source:
- https://snl.no/Heinrich_Wilhelm_von_Huth

---

# 7. Crimea and the Caucasus

## 7.1 Crimean Khanate

### Decision

**KEEP_PROCEDURAL**

The khanate's military/political system depended heavily on Giray dynastic authority, noble lineages and tribal/qaracı structures. The current mod already has **Devlet IV Giray** as ruler.

No sufficiently strong evidence was found for a distinct non-ruler person who should be represented as commander of the entire current army formation on 1776-01-01.

Using Devlet IV himself as the army general would:

1. duplicate the ruler;
2. imply a direct formation command not demonstrated by the evidence;
3. erase the composite military structure.

Şahin Giray must also not be backdated: his Russian-backed political/military ascendancy belongs to the later 1776/1777 crisis.

Sources:
- https://islamansiklopedisi.org.tr/kirim
- https://islamansiklopedisi.org.tr/sahin-giray
- https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/characters/cleanup2b3%20-%20residual%20europe%20rulers%201776.txt

## 7.2 Circassia

### Decision

**KEEP_PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE**

Academic work on eighteenth-/early-nineteenth-century Circassian governance shows substantial variation among tribal/community structures, with assemblies, aristocratic systems and military/social fraternities rather than a single defensible national commander.

The current broad CIR formation therefore has no safe one-name mapping.

Source:
- https://dergipark.org.tr/en/pub/jocas/article/1215889

## 7.3 CHC — `Murtazeki`

### Decision for the general slot

**KEEP_PROCEDURAL**

### Separate research warning

**FORMATION_NAME_ANACHRONISM_AUDIT_REQUIRED**

The academic study of the **Murtazeki** institution places these salaried warriors/guards in the North Caucasian Imamate context from around **1832 to 1859**.

That makes the current formation name itself anachronistic for 1776. Because this phase is research-only and the user explicitly prohibited gameplay edits, no formation change is proposed here. The correct action is to carry the issue into a later formation-history cleanup.

Source:
- https://caucasushistory.ru/2618-6772/ru/article/view/346

---

# 8. Galicia boundary case

`cleanup2d3b_gal_land_1` has an Eastern-Europe HQ and therefore appears during a mechanical regional scan, but it is a **Habsburg** formation.

To avoid conflicting historical assignments between regional research passes:

**Decision: `DEFER_TO_CLEANUP-2D-5C`**

This is an explicit hand-off, not an omission.

---

# 9. Existing character / DNA / template audit

Inspected current-branch areas include:

- `common/dna_data/`
- `common/character_templates/`
- `common/history/characters/`
- `common/history/military_formations/`
- repository code search for key candidate surnames / event references

### Relevant findings

- No dedicated **Potemkin**, **Rumyantsev**, **Decolong** or **Sprengtporten** DNA/template was found.
- `country_rus.txt` contains many later Russian commanders, but none provides a reusable 1776 template for the proposed men above.
- `country_plc.txt` contains Stanisław August Poniatowski, not Branicki.
- No current `country_swe.txt` or `country_dennor.txt` template file was found.
- The DNA directory contains a small set of bespoke characters, none corresponding to the proposed northern/eastern generals.
- A repository search for “Potemkin” surfaces an unrelated later revolutionary/event context, not a reusable Grigory Potemkin commander asset.
- Suvorov-related repository references do not override the reference-date rejection.

Repository sources:
- https://github.com/Malzars-sys/1776-Age-of-Revolutions/tree/cleanup-post-release/common/dna_data
- https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/character_templates/country_rus.txt
- https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/character_templates/country_plc.txt

---

# 10. Portrait audit

| Candidate | Portrait evidence | Recommendation |
|---|---|---|
| Potemkin | Strong contemporary/near-contemporary portrait corpus | portrait sourcing feasible |
| Rumyantsev | Surviving late-18th-century portrait material | portrait sourcing feasible |
| Branicki | Multiple portraits documented | portrait sourcing feasible |
| Sprengtporten | Godenhjelm/Cygnaeus Gallery portrait available | strong candidate |
| Decolong | No reliable portrait confirmed in this pass | do not invent likeness |
| Suvorov | Extensive portrait corpus | irrelevant to starting implementation because rejected |

A future art/DNA pass should distinguish **“portrait exists”** from **“repo DNA already exists.”** They are not the same thing.

---

# 11. Implementation-facing conclusions — research only

If this packet is later converted into an implementation prompt, the safest historical changes are:

1. Replace RUS `land_1` procedural general with **Potemkin**.
2. Replace RUS `land_5` procedural general with **Decolong**.
3. Replace SWE procedural general with **Sprengtporten**.
4. Keep **Rumyantsev**, but document him as southern theatre/higher-command abstraction.
5. Keep **Branicki**, but document him as Grand Crown Hetman/high-command officeholder abstraction, not direct commander of a unified PLC army.
6. Preserve procedural generals for CRI, RUS `land_2`, RUS `land_3`, CIR, CHC and DENNOR.
7. Preserve the hard rejection of **Suvorov** for the 1776-01-01 setup.
8. Hand GAL back to the Habsburg/Central-Europe phase.
9. Carry the anachronistic **Murtazeki** formation-name finding to a later formation cleanup.

**No implementation has been performed in this phase.**

---

# 12. Source register

## Repository

- Military formations: https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/00_military_formations_europe.txt
- DNA data: https://github.com/Malzars-sys/1776-Age-of-Revolutions/tree/cleanup-post-release/common/dna_data
- Russian templates: https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/character_templates/country_rus.txt
- PLC templates: https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/character_templates/country_plc.txt
- Major 1776 rulers: https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/characters/cleanup2b1%20-%20major%20rulers%201776.txt
- Residual European rulers: https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/characters/cleanup2b3%20-%20residual%20europe%20rulers%201776.txt

## Russia

- Potemkin — Great Russian Encyclopedia: https://bigenc.ru/c/potiomkin-tavricheskii-grigorii-aleksandrovich-f16459
- Potemkin — Russian Biographical Dictionary / Wikisource: https://ru.wikisource.org/wiki/РБС/ВТ/Потемкин,_Григорий_Александрович
- Rumyantsev — Great Russian Encyclopedia: https://old.bigenc.ru/domestic_history/text/3520474
- Little Russian Collegium — Great Russian Encyclopedia: https://old.bigenc.ru/domestic_history/text/2169858
- Decolong — RGVIA archival guide: https://guides.rusarchives.ru/terms/15/8321/kancelyariya-general-poruchika-dekolonga-klape-klapir-de-kolonga-ia
- Decolong — academic study of Siberian Corps: https://journals.rcsi.science/2311-1402/article/view/254286/ru_RU
- Decolong — Erik-Amburger database: https://amburger.ios-regensburg.de/index.php?id=2589
- Suvorov — Great Russian Encyclopedia: https://bigenc.ru/c/suvorov-aleksandr-vasil-evich-176290
- Suvorov Museum: https://suvorovmuseum.ru/en/%D0%BE-%D1%81%D1%83%D0%B2%D0%BE%D1%80%D0%BE%D0%B2%D0%B5

## Polish–Lithuanian Commonwealth

- Branicki — Polski Słownik Biograficzny: https://www.ipsb.nina.gov.pl/a/biografia/franciszek-ksawery-branicki-h-korczak-zm-1819-hetman-wielki-koronny
- Branicki — Encyklopedia Krakowa: https://encyklopediakrakowa.pl/slawni-i-zapomniani/86-b/598-branicki-franciszek-ksawery.html
- Crown/Lithuanian military commissions: https://www.ldkistorija.lt/commissions-on-war-and-treasury-of-the-grand-duchy-of-lithuania/
- Permanent Council / Military Department study: https://ruj.uj.edu.pl/entities/publication/27f16ecb-6d2e-45ec-b738-8e269ae05479
- Military Department article: https://czasopisma.uni.lodz.pl/pnh/article/view/27290

## Sweden

- Georg Magnus Sprengtporten — Svenskt biografiskt lexikon / Swedish National Archives: https://sok.riksarkivet.se/sbl/Presentation.aspx?id=20013

## Denmark–Norway

- Commanding general in Norway — Store norske leksikon: https://snl.no/kommanderende_general
- Karl of Hesse — SNL: https://snl.no/Karl_av_Hessen
- 1775 military roll — Digitalarkivet/Riksarkivet: https://www.digitalarkivet.no/source/100435
- Georg Frederik von Krogh — Norsk biografisk leksikon: https://nbl.snl.no/Georg_Frederik_von_Krogh
- Heinrich Wilhelm von Huth — SNL: https://snl.no/Heinrich_Wilhelm_von_Huth

## Crimea / Caucasus

- Crimean Khanate — TDV İslâm Ansiklopedisi: https://islamansiklopedisi.org.tr/kirim
- Şahin Giray — TDV İslâm Ansiklopedisi: https://islamansiklopedisi.org.tr/sahin-giray
- Murtazeki — academic article: https://caucasushistory.ru/2618-6772/ru/article/view/346
- Circassian governance — Journal of Caucasian Studies: https://dergipark.org.tr/en/pub/jocas/article/1215889

---

# 13. CSV companion

The companion CSV contains:

- one **PRIMARY** row for every formation decision in this phase;
- one **BOUNDARY** row for GAL;
- explicit **REJECTED_CANDIDATE** rows for Suvorov, Volkonsky, von Krogh, Karl of Hesse and Devlet IV Giray;
- historical date precision and source conflicts;
- birth-polity and V3 state mappings;
- mapping classification;
- culture/religion/social origin;
- conservative gameplay-profile suggestions;
- portrait/DNA status;
- source URLs;
- separate historical and mapping confidence;
- final decision.

File: `GENERALS_1776_NORTHERN_EASTERN_EUROPE_IMPLEMENTATION.csv`
