# CLEANUP-2D-5I — CENTRAL ASIA HISTORICAL GENERALS, 1776

**Project:** *1776 – Age of Revolutions* (Victoria 3)  
**Repository:** `Malzars-sys/1776-Age-of-Revolutions`  
**Reference branch:** `cleanup-post-release`  
**Absolute historical reference date:** **1776-01-01**  
**Phase:** historical research only  
**Implementation performed:** **NO**

---

## 1. Executive conclusion

The repository audit closes the Central Asian land-formation scope at **five formations**, all located in `common/history/military_formations/00_military_formations_europe.txt` despite their Central Asian geography. No additional land formation using `sr:region_central_asia` was found in the Middle East, India, or Asia formation files checked for this phase.

| Tag | Formation | Current repo general status | Historical recommendation | Confidence |
|---|---|---|---|---|
| BUK | `Buxoro Qoʻshini` | `PROCEDURAL_ALLOWED` | **REUSE_EXISTING_RULER_AS_HISTORICAL_GENERAL — Daniyal Biy** | Medium |
| KHI | `Xiva Qoʻshini` | `PROCEDURAL_ALLOWED` | **REUSE_EXISTING_RULER_AS_HISTORICAL_GENERAL — Muhammad Amin Inaq** | High |
| KOK | `Qoʻqon Qoʻshini` | `PROCEDURAL_ALLOWED` | **KEEP_PROCEDURAL** | High for the conservative conclusion |
| KZH | `Kişi Jüz Sarbazdary` | `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE` | **COLLECTIVE_STRUCTURE** | High |
| OZH | `Orta Jüz Sarbazdary` | `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE` | **REUSE_EXISTING_RULER_AS_HISTORICAL_GENERAL — Ablai Khan** | High |

The result is intentionally asymmetric. The audit **does not equate sovereignty with generalship**. A ruler is selected only when separate evidence establishes substantial personal military command. That threshold is met very strongly by **Muhammad Amin Inaq** and **Ablai Khan**, and more cautiously by **Daniyal Biy**. It is not met for **Narbuta Biy** at the level necessary to attach him to the mod’s single Kokand formation. For the **Junior Zhuz**, contemporary evidence positively demonstrates that Nuraly Khan could not control the autonomous war parties of the polity; the correct representation is collective, not personal.

A structural warning is essential: Yuri Bregel’s synthesis for *Encyclopaedia Iranica* stresses that eighteenth-century Central Asian governments did **not** resemble nineteenth-century European standing-army systems. Tribal forces and chieftains retained major autonomy, while permanent troops under centrally appointed commanders emerged only later in Khiva and Kokand, and later still in Bukhara. Therefore a Victoria 3 formation is necessarily an abstraction; a named character must represent documented field authority, not a fictional modern command post.  
Source: [Yuri Bregel, “CENTRAL ASIA vii. In the 18th-19th Centuries,” Encyclopaedia Iranica](https://www.iranicaonline.org/articles/central-asia-vii/).

---

## 2. Repository scope audit

### 2.1 Files checked

Primary formation file containing the five Central Asian formations:

- [`common/history/military_formations/00_military_formations_europe.txt`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/00_military_formations_europe.txt)

Additional formation files checked to make sure a regionally relevant formation had not been hidden elsewhere:

- [`04_military_formations_middle_east.txt`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/04_military_formations_middle_east.txt)
- [`05_military_formations_india.txt`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/05_military_formations_india.txt)
- [`06_military_formations_asia.txt`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/06_military_formations_asia.txt)

Localization / existing-character context:

- [`localization/english/cleanup2d3b_formations_l_english.yml`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/localization/english/cleanup2d3b_formations_l_english.yml)
- [`localization/english/cleanup2c1_non_europe_rulers_l_english.yml`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/localization/english/cleanup2c1_non_europe_rulers_l_english.yml)
- [`common/history/characters/cleanup2c1 - non europe rulers 1776.txt`](https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/characters/cleanup2c1%20-%20non%20europe%20rulers%201776.txt)

### 2.2 Exact formation set

1. **BUK** — `cleanup2d3b_buk_land_1` — localized **Buxoro Qoʻshini** — HQ `sr:region_central_asia` — first formation state anchor `STATE_MERZ` — current general marker `GEN1776-070`, `PROCEDURAL_ALLOWED`.
2. **KHI** — `cleanup2d3b_khi_land_1` — localized **Xiva Qoʻshini** — HQ `sr:region_central_asia` — first anchor `STATE_KHIVA` — `GEN1776-074`, `PROCEDURAL_ALLOWED`.
3. **KOK** — `cleanup2d3b_kok_land_1` — localized **Qoʻqon Qoʻshini** — HQ `sr:region_central_asia` — first anchor `STATE_FERGANA` — `GEN1776-075`, `PROCEDURAL_ALLOWED`.
4. **KZH** — `cleanup2d3b_kzh_land_1` — localized **Kişi Jüz Sarbazdary** — HQ `sr:region_central_asia` — first anchor `STATE_AKTOBE` — `GEN1776-077`, `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE`.
5. **OZH** — `cleanup2d3b_ozh_land_1` — localized **Orta Jüz Sarbazdary** — HQ `sr:region_central_asia` — first anchor `STATE_AKMOLINSK` — `GEN1776-081`, `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE`.

The current ruler layer already contains historical characters for these five tags:

- BUK — **Daniyal Biy**, Ataliq;
- KHI — **Muhammad Amin Inaq**, Inaq;
- KOK — **Narbuta Biy**, Biy;
- KZH — **Nuraly Khan**, Khan;
- OZH — **Ablai Khan**, Khan.

The existing Central Asian ruler records contain **no explicit `dna =` field and no person-specific `template =` field**. By contrast, the current procedural generals use `template = default`. This matters for later implementation: a selected ruler should preferably be reused rather than duplicated, but that is an implementation question outside this research phase.

### 2.3 Scope exclusions

This phase uses the repository’s actual Central Asian formation architecture rather than a modern geographical wish-list. States such as Afghanistan/Durrani, Persia, Tibet, Qing China, or the Caucasus may border or overlap broader historical conceptions of Central Asia, but they are not additional land formations in the audited `sr:region_central_asia` formation set. They should stay with their own regional cleanup phases unless a later global reconciliation explicitly reassigns scope.

---

## 3. Methodology and evidence threshold

### 3.1 Selection rule

A historical ruler is **not** automatically accepted as a general. A candidate is attached only if one or more of the following can be established for the period around 1776:

- personal leadership of a campaign or armed force;
- a contemporary or near-contemporary description as military commander / sardar / field leader;
- direct responsibility for subduing armed rivals in a way that clearly exceeds ceremonial sovereignty;
- a military office that can reasonably map onto Victoria 3’s singular general slot without inventing a Western rank.

Where evidence proves only that a ruler **ordered** troops or benefited from military victories, but does not establish personal field command, the default is `KEEP_PROCEDURAL`.

Where armed authority was genuinely distributed among clans, tribal leaders, batyrs, sultans, or autonomous war parties, and no single commander controlled the represented force, use `COLLECTIVE_STRUCTURE`.

### 3.2 Date rule

The absolute eligibility date is **1776-01-01**. Later fame is irrelevant. No candidate is accepted merely because he became a military figure later in 1776 or in subsequent years.

No date is reverse-engineered from a repo `age` field. Existing mod ages are treated as implementation data, not historical sources.

### 3.3 Source hierarchy

Highest weight:

1. academic encyclopedias and specialist scholarship — *Encyclopaedia Iranica*, Cambridge scholarship, Brill-edited primary chronicles;
2. national institutes and major encyclopedias — Sh. Sh. Ualikhanov Institute, Big Russian Encyclopedia, Uzbekistan National Encyclopedia material;
3. published primary documents / scholarly editions — Vostlit/DrevLit reproductions of archival correspondence, Efremov’s eighteenth-century account;
4. national historical portals and government historical summaries — useful especially for chronology and local historiography, but cross-checked where possible.

Low-quality genealogy pages, unsourced biography aggregators, and image-search identifications were not accepted as evidence for precise dates.

---

# 4. Detailed dossiers

## 4.1 BUK — Bukhara — `Buxoro Qoʻshini`

### Recommendation

**REUSE_EXISTING_RULER_AS_HISTORICAL_GENERAL — Daniyal Biy — MEDIUM confidence.**

This is the one deliberately cautious named selection. Daniyal is not selected because he was the political ruler alone. He is selected because national-encyclopedia and academic evidence connects him personally to armed confrontation with rebel elites and to the subjugation of rebellious Uzbek tribes. Nevertheless, the evidence does **not** establish a European-style office of “commander-in-chief,” and a stricter future implementation policy could legitimately downgrade this row to `KEEP_PROCEDURAL`.

### Identity and transliteration

**Canonical working name:** Daniyal Biy.  
Variants:

- **Dāniāl Bī** — Persianate scholarly transliteration;
- **Daniyal Biy** — practical English/Latin rendering;
- **Doniyolbiy** — modern Uzbek spelling;
- **Даниял-бий** — Russian;
- **Daniar-bek** — form used in annotations to Filipp Efremov’s account.

These are spelling/transliteration variants of the same person.

### Birth

- **Birth date:** unknown.
- **Precision:** `UNKNOWN`.
- **Birth place:** unknown in the consulted authoritative sources.
- **V3 birth state:** `UNRESOLVED`.

The repo’s existing ruler has `age = 55`. That value must **not** be transformed into a historical birth year without an independent source.

### Death

- **1785**, year only.

Sources consistently place the end of Daniyal’s rule in 1785. The exact day was not established in the consulted high-confidence material.

### Office and military role

The Big Russian Encyclopedia gives Daniyal as ataliq in **1758–1785**. *Encyclopaedia Iranica* explains that after Muhammad Rahim’s death in 1758, Daniyal became ataliq and actual ruler, and later notes that rebellious tribes in Bukhara had been subdued under Muhammad Rahim and Daniyal.  
Sources:

- [Encyclopaedia Iranica — Central Asia vii](https://www.iranicaonline.org/articles/central-asia-vii/)
- [Big Russian Encyclopedia — Uzbekistan](https://old.bigenc.ru/geography/text/4216211)

The Uzbekistan National Encyclopedia biography (Qomus mirror) is more specific. It describes provincial governors and tribal amirs rebelling against centralization and arming **10,000 men** for a march on Bukhara; Daniyal is described as going out against them before reaching an agreement. This is enough to establish more than purely ceremonial military involvement.  
Source: [Qomus / Uzbekistan National Encyclopedia — Doniyolbiy](https://qomus.info/oz/encyclopedia/d/doniyolbiy/).

### Structure warning

This must not be retrofitted into a permanent Western staff command. Bregel explicitly warns that Central Asian military organization remained heavily dependent on tribal forces; centrally appointed standing troops of the later sarbaz type were a later development. For Bukhara, such regular formations emerged only in the nineteenth century. Thus “Daniyal as general” is best understood as Victoria 3’s abstraction of **personal supreme military leadership**, not as a claim that he held a modern general rank.

### Activity on 1776-01-01

**Eligible.** Daniyal was alive, in office, and actual ruler. Military-centralizing conflict with provincial and tribal opponents was a defining part of his regime. No source consulted places him in a uniquely named campaign exactly on 1 January 1776, so confidence is medium rather than high.

### Culture / religion / social origin

- **Culture:** Uzbek, Manghit.
- **Religion:** Sunni Islam — contextual classification; no individual confessional declaration was located.
- **Origin:** Manghit tribal aristocracy; uncle of Muhammad Rahim.

### Portrait / DNA

- **Authenticated contemporary portrait:** none found.
- **Existing repo character:** yes — ruler Daniyal Biy.
- **Explicit DNA/person-specific template:** none in the existing ruler record.
- **Current procedural general template:** `default`.

### Alternative checked — Filipp Sergeyevich Efremov

Efremov is a genuine and unusually interesting military subordinate, but he is **not safe for 1776-01-01**. The Uzbekistan National Encyclopedia records that he was captured in 1774, entered Daniyal’s service, and later rose through **onboshi / ellikboshi / yuzboshi** ranks and participated in campaigns. His own account is an important primary witness to Bukharan military organization. However, the consulted chronology does not securely establish that he had already reached command rank by the exact reference date. Therefore he is **REJECT_FOR_REFERENCE_DATE / INSUFFICIENT_CHRONOLOGY**, not a replacement for GEN1776-070.  
Sources:

- [Uzbekistan National Encyclopedia — Filipp Efremov](https://qomus.info/oz/encyclopedia/y/yefremov-filipp-sergeevich/)
- [Efremov’s eighteenth-century account, Vostlit edition](https://www.vostlit.info/Texts/rus8/Efremov_2/text1.htm)

---

## 4.2 KHI — Khiva — `Xiva Qoʻshini`

### Recommendation

**REUSE_EXISTING_RULER_AS_HISTORICAL_GENERAL — Muhammad Amin Inaq — HIGH confidence.**

This is the strongest Uzbek-khanate individual case in the phase.

### Identity and transliteration

**Canonical working name:** Muhammad Amin Inaq.  
Variants:

- **Moḥammad-Amīn Inaq / Moḥammad-Amīn Īnāq** — Iranica scholarly transliteration;
- **Muhammad Amin Inaq** — practical English;
- **Muhammad Amin-biy / Muhammad Amin inoq** — Uzbek-oriented forms;
- **Мухаммад Амин-бий / Мухаммад Амин-инак** — Russian forms.

Tribal-name variants:

- **Qongrat / Qungrat / Kungrat / Qoʻngʻirot**.

These are transliteration/orthography variants of the same Uzbek tribal name. They must not be treated as different ethnic or dynastic groups in the CSV.

### Birth

- **Birth date:** unknown.
- **Precision:** `UNKNOWN`.
- **Birth place:** unknown.
- **V3 birth state:** `UNRESOLVED`.

Important: dates such as **1762/1763** in some accounts refer to the rise of Qongrat power or Muhammad Amin’s political position, not to his birth. No birth year has been invented.

### Death / end-of-rule chronology

- *Encyclopaedia Iranica* places the end of his rule as inaq at **1204/1790**.
- Urgench State University catalog metadata for an Agahi edition gives the span **1175–1205 / 1762–1791**.

The safe research output is therefore **1790/1791 — source conflict**, not an exact death day.  
Sources:

- [Encyclopaedia Iranica — Central Asia vii](https://www.iranicaonline.org/articles/central-asia-vii/)
- [Urgench State University catalog — Agahi material](https://akbt.urdu.uz/uz/books/25827)

### Military function

This is direct, not inferred. Bregel states that Muhammad Amin, leader of the Qongrats, **defeated and banished the Yomuts in 1770** and had to fight numerous rivals from other tribes throughout his rule as inaq. The Big Russian Encyclopedia similarly states that Muhammad Amin-biy defeated the Yomuts in 1770 and became the actual ruler. Cambridge scholarship, citing Bregel’s edition of *Firdaws al-Iqbal*, describes the Qungrat dynasty as established in **1770–71 when Muhammad Amin Inaq recaptured the khanate from the Yomut Turkmen**.  
Sources:

- [Encyclopaedia Iranica — Central Asia vii](https://www.iranicaonline.org/articles/central-asia-vii/)
- [Big Russian Encyclopedia — Uzbekistan](https://old.bigenc.ru/geography/text/4216211)
- [Cambridge, *Modern Asian Studies* — “Twin Imperial Disasters”](https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/twin-imperial-disasters-the-invasions-of-khiva-and-afghanistan-in-the-russian-and-british-official-mind-18391842/6B67892623A65A5DC86F900BBA03B6F9)
- [Brill edition metadata — *Firdaws al-iqbāl: History of Khorezm*](https://books.google.com/books/about/Firdaws_al_iqb%C4%81l.html?id=jytVEAAAQBAJ)

### Activity on 1776-01-01

**Clearly eligible.** He was the Qongrat inaq/de facto ruler, and his military contest with tribal rivals continued across the entire period of his rule. The selection is based on **personal documented military leadership**, not on his political title.

### Culture / religion / social origin

- **Culture:** Uzbek, Qongrat/Qungrat.
- **Religion:** Sunni Islam — contextual classification.
- **Origin:** Qongrat tribal chief, non-Chinggisid elite. This is significant: the Qongrat inaqs still installed Chinggisid puppet khans because the Qongrats themselves lacked Chinggisid descent.

### Portrait / DNA

- **Authenticated contemporary portrait:** none verified.
- **False-positive risk:** searches for “Muhammad Amin Khan” frequently return other rulers of the same/similar name, including later Khivan khans or entirely unrelated figures. None should be used without provenance.
- **Existing repo character:** yes — ruler Muhammad Amin Inaq.
- **Explicit DNA/person-specific template:** none.
- **Current procedural general template:** `default`.

### Implementation note for later phase

If Victoria 3 permits the existing ruler character to carry general status cleanly, **reuse is preferable to creating a duplicate person**. That is not performed here.

---

## 4.3 KOK — Kokand — `Qoʻqon Qoʻshini`

### Recommendation

**KEEP_PROCEDURAL.**  
Reviewed historical candidate: **Narbuta Biy**.  
Confidence in the conservative decision: **high**.

### Identity and transliteration

**Candidate:** Narbuta Biy.  
Variants:

- **Nārbūta Bī** — Iranica;
- **Narbuta Biy** — common Latin form;
- **Нарбута-бий** — Russian.

`Biy/Bī` is a Central Asian title and should not be translated mechanically as a European military rank.

### Birth

- **Birth date:** unknown.
- **Birth place:** unknown in the preferred sources consulted.
- **V3 birth state:** `UNRESOLVED`.

Conflicting birth years found on low-grade secondary sites were rejected.

### Death / end-of-reign chronology

Authoritative and national summaries differ on the end of his rule:

- Bregel’s Iranica synthesis: approximately **1770–1798**;
- newer Iranica Kokand article: **1770–1799**;
- Uzbekistan government history: **1770–1800**.

Therefore the report does **not** manufacture a death date from an end-of-reign year.

### Military-political activity

Narbuta was undoubtedly a real political consolidator. Bregel states that Fergana was finally united under the Mings during his reign. The Uzbekistan government historical summary states that he suppressed separatism in **Chust, Namangan, and Khujand**, and **sent troops** toward Tashkent.  
Sources:

- [Encyclopaedia Iranica — Kokand Khanate](https://www.iranicaonline.org/articles/kokand-khanate/)
- [Encyclopaedia Iranica — Central Asia vii](https://www.iranicaonline.org/articles/central-asia-vii/)
- [Government of Uzbekistan — History](https://gov.uz/en/mfa/sections/view/14508)

The problem is the exact threshold required by this phase: these sources do not securely show that Narbuta **personally commanded** the single force abstracted as `Qoʻqon Qoʻshini` on or around 1776-01-01. “Suppressed” and “sent troops” demonstrate military state action, but not enough personal field command to turn the ruler into a general without risk of circular reasoning.

### Activity on 1776-01-01

- alive and ruling;
- actively centralizing Fergana;
- military activity attributable to his government;
- **personal formation command insufficiently documented**.

Hence `KEEP_PROCEDURAL` is the safer historical result.

### Culture / religion / social origin

- **Culture:** Uzbek, Ming.
- **Religion:** Sunni Islam — contextual classification.
- **Origin:** Ming ruling lineage / tribal aristocracy. Iranica identifies him as Nārbūta Biy b. ʿAbd-al-Raḥmān Biy b. ʿAbd-al-Karim Biy.

### Portrait / DNA

- **Authenticated contemporary portrait:** none verified.
- **Image-search warning:** search results often return later nineteenth-century Kokand princes/rulers; they are not Narbuta.
- **Existing repo character:** yes — ruler Narbuta Biy.
- **Explicit DNA/person-specific template:** none.
- **Current procedural general template:** `default`.

### Reopening condition

This row should be reopened only if a stronger primary or specialist source can document that Narbuta himself led a specific campaign or force in a period covering 1776. Mere sovereignty is insufficient.

---

## 4.4 KZH — Junior Zhuz — `Kişi Jüz Sarbazdary`

### Recommendation

**COLLECTIVE_STRUCTURE.**  
Reviewed ruler: **Nuraly Khan — do not attach as unified formation commander.**  
Confidence: **high**.

This is not a “no source found” fallback. It is a **positive historical conclusion** supported by contemporary documentation.

### Identity and transliteration

- **Nuraly Khan** — common English/Latin;
- **Нуралы хан** — Russian;
- **Нұралы хан** — modern Kazakh.

`Junior Zhuz`, `Lesser Horde`, and `Kişi Jüz` are alternative labels for the broader political-social grouping. None should imply a centrally disciplined standing army.

### Birth

A current e-history biographical article gives **1710/1711**. The Ualikhanov Institute’s Bukey Khan biography uses **1710–1790** for Nuraly. A separate e-history chronology page gives **1704–1790**, showing that even national educational material is internally inconsistent.  
Sources:

- [E-history — Nuraly Khan](https://e-history.kz/ru/seo-materials/show/29535)
- [Ualikhanov Institute — Bukey Khan biography, discussion of Nuraly](https://iie.kz/?p=25591)

Research value:

- **Birth date:** `1710/1711` preferred, with explicit source conflict.
- **Precision:** `DISPUTED_YEAR`.
- **Birth place:** not securely established in consulted preferred sources.
- **V3 birth state:** `UNRESOLVED`.

The repo’s existing ruler has `age = 71`, which would imply roughly 1704/1705 at the 1776 start. That matches the weaker chronology page more than the newer biography, but **repo age is not historical evidence**. Do not hard-code a birth date from it.

### Death

E-history material places his death in **spring 1790 in Ufa**. No exact day should be invented.  
Source: [E-history — archival/national-encyclopedia based note](https://e-history.kz/kz/amp/news/show/2856).

### Why Nuraly is not the general

The decisive evidence is Nuraly’s own letter of **6 August 1774**, preserved in a published document collection. He reports that the Kazakhs were inclined toward war against Russia, that he was unable to turn them back, and that **his strength was insufficient to stop them**. He asks the Russian commander to deal with the raiders.  
Primary-source edition: [Vostlit — documents on the Kazakhs and the Pugachev movement, Document No. 16](https://www.vostlit.info/Texts/Dokumenty/Russ/XVIII/1760-1780/Pugachev/Mat_kazach_vojna_pugacev/text1.htm).

The same dossier identifies multiple autonomous raid leaders and groups. Levshin’s historical account, drawing on Russian administrative material, likewise depicts the Lesser/Junior Zhuz as difficult for the khan to control during the crisis.  
Source: [A. I. Levshin, Vostlit edition](https://www.vostlit.info/Texts/Dokumenty/M.Asien/XIX/1820-1840/Levschin/text11.htm).

This evidence is almost tailor-made for the user’s methodological warning. Nuraly may be a khan and may have raised forces in other contexts, but on the eve of 1776 he **did not command the Junior Zhuz as a single military formation**.

### Activity on 1776-01-01

- active khan;
- politically recognized but weak authority across the steppe;
- armed action fragmented among autonomous sultans, elders, batyrs, and clan war parties;
- no single formation-level commander defensible.

### Culture / religion / social origin

- **Culture:** Kazakh.
- **Religion:** Sunni Islam — contextual classification.
- **Origin:** Chinggisid/Töre aristocracy, eldest son of Abulkhair Khan and Bopay Khanım.

### Portrait / DNA

- **Authenticated contemporary portrait of Nuraly:** none verified.
- **Existing repo character:** yes — Nuraly Khan.
- **Explicit DNA/person-specific template:** none.
- **Current procedural general template:** `default`.

### Correct implementation concept for later phase

Keep the current **collective/procedural representation**. If a later flavor system wants named batyrs or sultans, they should be modeled as **specific war-party leaders**, not retroactively as a unified general of all `Kişi Jüz Sarbazdary`.

---

## 4.5 OZH — Middle Zhuz — `Orta Jüz Sarbazdary`

### Recommendation

**REUSE_EXISTING_RULER_AS_HISTORICAL_GENERAL — Ablai Khan — HIGH confidence.**

This recommendation intentionally **overrides the present repository comment** `PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE` for OZH. The reason is not fame or sovereign status; it is direct evidence of personal military command.

### Identity and transliteration

- **Abylai Khan** — common modern Kazakh/English form;
- **Ablai Khan** — common Russian/European rendering and current repo form;
- **Абылай хан** — Kazakh/Russian modern spelling;
- **Аблай** — older Russian scholarly/archival rendering;
- **Abilmansur / Әбілмансұр** — birth name.

These are one person.

### Birth

The Sh. Sh. Ualikhanov Institute gives:

- heading chronology: **1711/12–1780/81**;
- biography: born **1711**, with **1713** as an alternative;
- birthplace **Turkestan**, with **Tashkent** as an alternative.

Source: [Sh. Sh. Ualikhanov Institute — Ablai Khan](https://iie.kz/?p=25528).

Research output:

- **Birth date:** `1711 (alternative 1713)`;
- **Precision:** `SOURCE_CONFLICT`;
- **Birth place:** `Turkestan (alternative Tashkent)`;
- **V3 birth state:** `UNRESOLVED` because the historical birthplace itself is disputed and no confident repository state mapping was established during this research-only audit.

### Death — important source conflict

There is a real conflict even among reputable Kazakh historical portals:

- e-history gives **23 May 1781**;
- the Ualikhanov Institute’s archival reconstruction states that Ablai died near Tashkent in **late autumn 1780**, and quotes a March 1781 archival letter showing that his death had already occurred and had been deliberately concealed.

Sources:

- [E-history — Abylai Khan](https://e-history.kz/en/prominent-figures/show/12717)
- [Ualikhanov Institute — Ablai Khan](https://iie.kz/?p=25528)

Because the phase explicitly forbids invented precision, the CSV records **1780/1781 — SOURCE_CONFLICT** and does **not** choose an exact day. This conflict does not affect eligibility on 1776-01-01.

### Explicit military function

The Ualikhanov Institute calls Ablai a **военачальник (сардар)** — military commander / sardar — and senior khan. It states that he remained with warriors and participated in campaigns to the end of his life. More importantly, it documents concrete field activity around the reference period.

For **1774**, a report by Semipalatinsk fortress commander Colonel I. T. Titov states that Ablai, Abulfeiz, and Karabarak assembled a very large force and **went to war against the Kyrgyz**. The English version of the Institute biography likewise describes this campaign.  
Sources:

- [Ualikhanov Institute — Russian biography](https://iie.kz/?p=25528)
- [Ualikhanov Institute — English biography](https://iie.kz/?p=26133)

The same biography documents campaigns in **1773**, **1774**, and again in **1779**, as well as earlier evidence that Ablai personally gathered military forces for operations against neighboring groups.

This is precisely the evidentiary distinction the project requires: Ablai is not accepted because “khan = general”; he is accepted because **Ablai is independently documented as sardar and personal campaign leader**.

### Activity on 1776-01-01

**Clearly eligible.** He was senior khan from 1771 and an active military commander. Russian recognition of his khanship was delayed until 1778, but that diplomatic recognition issue does not negate his actual Kazakh political and military position in 1776.  
Supporting source: [Big Russian Encyclopedia — Kazakh Khanate](https://bigenc.ru/c/kazakhskoe-khanstvo-3b4db9).

### Culture / religion / social origin

- **Culture:** Kazakh.
- **Religion:** Muslim education is directly attested by the Ualikhanov Institute; **Sunni** is the contextual historical classification.
- **Origin:** Chinggisid/Töre ruling lineage, descendant of Zhangir Khan; birth name Abilmansur.

### Portrait / DNA

- **Authenticated contemporary portrait:** none verified during this audit.
- e-history and other Kazakh historical sites display familiar **posthumous/modern representations** of Ablai. They can be used only as iconographic references unless provenance is independently established; they should not be presented as life portraits.
- **Existing repo character:** yes — ruler Ablai Khan.
- **Explicit DNA/person-specific template:** none.
- **Current procedural general template:** `default`.

### Alternatives

Named batyrs such as **Bogenbay Batyr** are obvious military candidates, but available online chronologies around his death/reference-date status are inconsistent enough that they do not improve on Ablai’s exceptionally strong evidence. Do not introduce a more uncertain subordinate merely to avoid using a ruler when the ruler himself is independently proven to be a field commander.

---

# 5. Comparative interpretation of military structures

## 5.1 Uzbek khanates

Bukhara, Khiva, and Kokand in the 1770s combined court/central authority with powerful tribal military structures. Bregel’s synthesis is explicit that the central government historically lacked a Western-style independent army in the earlier eighteenth century and had to maneuver among tribal chieftains; later standing troops under appointed commanders were a nineteenth-century development.

Therefore:

- **Muhammad Amin Inaq** can represent Khiva because he is a tribal leader whose direct military success created the Qongrat political order;
- **Daniyal Biy** can cautiously represent Bukhara as the actual political-military authority personally confronting armed rebels, but should never be described as a modern professional general;
- **Narbuta Biy** stays unassigned because the evidence is presently stronger for state military action than for personal field command.

## 5.2 Kazakh zhuzes

The two Kazakh cases demonstrate why a single rule cannot be applied mechanically.

- **Junior Zhuz:** Nuraly’s own correspondence shows that he could not restrain war parties. A collective command model is historically correct.
- **Middle Zhuz:** Ablai is separately and explicitly documented as **sardar** and campaign commander. Although Kazakh armed society remained decentralized, this particular person had enough direct personal military authority to justify a named general abstraction.

The correct standard is therefore not “tribal = procedural” or “khan = named,” but **evidence of actual command at the reference date**.

---

# 6. Transliteration conventions for implementation

The later implementation phase should keep a dedicated comment or research note for name variants so future maintainers do not “correct” historically valid spellings into a different person.

| Person | Recommended display form | Important variants |
|---|---|---|
| Daniyal Biy | Daniyal Biy | Dāniāl Bī; Doniyolbiy; Даниял-бий; Daniar-bek |
| Muhammad Amin Inaq | Muhammad Amin Inaq | Moḥammad-Amīn Inaq/Īnāq; Muhammad Amin-biy; Muhammad Amin inoq; Мухаммад Амин-бий/инак |
| Narbuta Biy | Narbuta Biy | Nārbūta Bī; Нарбута-бий |
| Nuraly Khan | Nuraly Khan | Нуралы хан; Нұралы хан |
| Ablai Khan | Ablai Khan | Abylai Khan; Абылай хан; Аблай; Abilmansur/Әбілмансұр |

For the tribal names:

- Qongrat = Qungrat = Kungrat = modern Uzbek Qoʻngʻirot;
- Ming should remain **Ming** in this context and must not be confused with the Chinese Ming dynasty;
- Jüz / Zhuz are romanization variants of Kazakh жүз.

No diacritic-heavy scholarly transliteration needs to be forced into gameplay localization unless the project adopts that style globally. The research report retains scholarly forms for identification, while practical display names match recognizable forms already used by the mod.

---

# 7. Portrait and visual-identity audit

## Daniyal Biy
No authenticated contemporary portrait verified.

## Muhammad Amin Inaq
No authenticated contemporary portrait verified. Strong false-positive risk from other rulers named “Muhammad Amin Khan.”

## Narbuta Biy
No authenticated contemporary portrait verified. Search results can incorrectly surface later Kokand princes.

## Nuraly Khan
No authenticated contemporary portrait verified in the consulted sources.

## Ablai Khan
Modern/posthumous painted representations are widely available on Kazakh historical portals, including e-history. The consulted material does **not** establish them as life portraits. Treat them as posthumous iconography only.  
Reference page: [E-history — Abylai Khan](https://e-history.kz/en/prominent-figures/show/12717).

### Repo DNA/template conclusion

For all five existing ruler records:

- existing historical ruler character: **YES**;
- explicit `dna = ...`: **not present** in the audited ruler file;
- explicit person-specific `template = ...`: **not present**;
- current procedural general: `template = default`.

No DNA should be fabricated from a later painting.

---

# 8. Rejected / non-selected candidates and negative findings

### Filipp Sergeyevich Efremov — Bukhara
Real later military subordinate, eventually a yuzboshi, but promotion chronology is not secure enough for **1776-01-01**. Do not use.

### Narbuta Biy — Kokand
Real ruler with military state activity, but preferred sources do not cross the project’s threshold for **personal command of the represented formation**. Keep procedural unless stronger evidence is found.

### Nuraly Khan — Junior Zhuz
Explicitly rejected as unified formation commander because contemporary correspondence demonstrates inadequate control over armed groups.

### Bogenbay Batyr — Middle Zhuz
Famous and relevant, but online chronology around his final years/death is sufficiently inconsistent that he is unnecessary when Ablai already has direct, high-confidence command evidence.

### Generic khans / tribal leaders
No individual is selected merely because he occupied the highest political office. This is especially important for the Kazakh zhuzes and for the Uzbek states where tribal militias remained institutionally important.

---

# 9. Final implementation matrix for later Codex phase

**Research decision only — no file modification in this phase.**

| Tag | Current GEN | Action for later implementation | Historical person | Reuse existing ruler? | Historical caveat |
|---|---:|---|---|---|---|
| BUK | 070 | `REUSE_EXISTING_RULER_AS_HISTORICAL_GENERAL` | Daniyal Biy | Yes | Medium-confidence abstraction of personal political-military authority; downgrade to procedural if project requires a distinct military office |
| KHI | 074 | `REUSE_EXISTING_RULER_AS_HISTORICAL_GENERAL` | Muhammad Amin Inaq | Yes | Direct military leadership strongly attested |
| KOK | 075 | `KEEP_PROCEDURAL` | — | No | Narbuta reviewed but personal field command insufficiently proven |
| KZH | 077 | `COLLECTIVE_STRUCTURE` | — | No | Nuraly explicitly lacked control over autonomous war parties |
| OZH | 081 | `REUSE_EXISTING_RULER_AS_HISTORICAL_GENERAL` | Ablai Khan | Yes | Directly attested sardar and campaign leader; current repo collective flag should be reconsidered |

**Net result:**

- named historical individual: **3**;
- keep procedural: **1**;
- collective structure: **1**.

If the project adopts a stricter rule requiring a separately titled military office distinct from rulership, BUK becomes `KEEP_PROCEDURAL`; KHI and OZH remain named because their personal field command is independently explicit.

---

# 10. Source bibliography

## Academic / specialist

1. Yuri Bregel, **“CENTRAL ASIA vii. In the 18th-19th Centuries,” Encyclopaedia Iranica**.  
   https://www.iranicaonline.org/articles/central-asia-vii/
2. Timur K. Beĭsembiev & Scott C. Levi, **“KOKAND KHANATE,” Encyclopaedia Iranica**.  
   https://www.iranicaonline.org/articles/kokand-khanate/
3. Scott C. Levi, **The Rise and Fall of Khoqand, 1709–1876**. JSTOR edition/catalog reference.  
   https://www.jstor.org/stable/j.ctt21c4t0x
4. Alexander Morrison, **“Twin Imperial Disasters: The invasions of Khiva and Afghanistan in the Russian and British official mind, 1839–1842,” Modern Asian Studies** — relevant note cites Bregel’s *Firdaws al-Iqbal* for Muhammad Amin’s 1770–71 reconquest.  
   https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/twin-imperial-disasters-the-invasions-of-khiva-and-afghanistan-in-the-russian-and-british-official-mind-18391842/6B67892623A65A5DC86F900BBA03B6F9
5. Shir Muhammad Mirab Munis & Muhammad Riza Mirab Agahi; Yuri Bregel ed./trans., **Firdaws al-iqbāl: History of Khorezm**, Brill.  
   https://books.google.com/books/about/Firdaws_al_iqb%C4%81l.html?id=jytVEAAAQBAJ

## National institutes / encyclopedias

6. Sh. Sh. Ualikhanov Institute of History and Ethnology, **Ablai Khan** (Russian).  
   https://iie.kz/?p=25528
7. Sh. Sh. Ualikhanov Institute, **Abylai Khan** (English).  
   https://iie.kz/?p=26133
8. Sh. Sh. Ualikhanov Institute, **Bukey Khan** biography containing Nuraly chronology/context.  
   https://iie.kz/?p=25591
9. Big Russian Encyclopedia, **Uzbekistan**.  
   https://old.bigenc.ru/geography/text/4216211
10. Big Russian Encyclopedia, **Khiva Khanate**.  
    https://old.bigenc.ru/world_history/text/4664981
11. Big Russian Encyclopedia, **Kazakh Khanate**.  
    https://bigenc.ru/c/kazakhskoe-khanstvo-3b4db9
12. Uzbekistan National Encyclopedia material via Qomus, **Doniyolbiy**.  
    https://qomus.info/oz/encyclopedia/d/doniyolbiy/
13. Uzbekistan National Encyclopedia material via Qomus, **Filipp Sergeyevich Yefremov**.  
    https://qomus.info/oz/encyclopedia/y/yefremov-filipp-sergeevich/
14. Government of Uzbekistan, **History — Khanate of Kokand**.  
    https://gov.uz/en/mfa/sections/view/14508
15. E-history Kazakhstan, **Nuraly Khan**.  
    https://e-history.kz/ru/seo-materials/show/29535
16. E-history Kazakhstan, **Abylai Khan (Abilmansur)**.  
    https://e-history.kz/en/prominent-figures/show/12717

## Primary / documentary editions

17. **1774 letter of Nuraly Khan**, published in the documentary collection on the Kazakhs and the Pugachev movement, Vostlit, Document No. 16.  
    https://www.vostlit.info/Texts/Dokumenty/Russ/XVIII/1760-1780/Pugachev/Mat_kazach_vojna_pugacev/text1.htm
18. A. I. Levshin, historical material on the Kazakh hordes, Vostlit edition.  
    https://www.vostlit.info/Texts/Dokumenty/M.Asien/XIX/1820-1840/Levschin/text11.htm
19. Filipp Efremov, **Nine-Year Journey / Stranstvovanie**, eighteenth-century eyewitness account, Vostlit edition.  
    https://www.vostlit.info/Texts/rus8/Efremov_2/text1.htm
20. Urgench State University catalog, Agahi material with Qongrat chronology.  
    https://akbt.urdu.uz/uz/books/25827

---

# 11. Historical uncertainties that must survive implementation

Do **not** erase the following uncertainties in a future code pass:

- Daniyal Biy — no reliable exact birth date; no authenticated portrait; military attachment is **medium**, not high, confidence.
- Muhammad Amin Inaq — no reliable birth date/place; end/death chronology **1790 vs 1791**.
- Narbuta Biy — no secure birth date; end-of-reign chronology **1798/1799/1800**; remains procedural.
- Nuraly Khan — birth chronology **1710/1711 vs a weaker 1704 tradition**; repo `age=71` is not authoritative; collective command conclusion is strong.
- Ablai Khan — birth **1711/1713**, birthplace **Turkestan/Tashkent**, death **late 1780 vs 23 May 1781** depending reputable source; no exact death date should be encoded without resolving the conflict.

---

# 12. Phase status

**CLEANUP-2D-5I research complete.**

No gameplay file was modified.  
No character was created or edited.  
No localization was changed.  
No commit was created.  
No push was performed.
