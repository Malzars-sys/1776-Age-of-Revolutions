# CLEANUP-2D-5C — Historical Generals 1776 — Central Europe

## Status

- **Project:** Victoria 3 — *1776 – Age of Revolutions*
- **Repository:** `Malzars-sys/1776-Age-of-Revolutions`
- **Reference branch:** `cleanup-post-release`
- **Absolute reference date:** **1776-01-01**
- **Mode:** **historical research only**
- **Implementation performed:** **none**
- **Commit/push performed:** **none**

## Executive conclusion

The repository audit identifies **46 land formations** in the Central-European scope used for this phase.

Recommended result:

- **10 formations** receive a defensible named historical commander;
- **36 formations** remain procedural because no sufficiently documented army-level holder active on **1776-01-01** was established, or because the historical command structure was collective/militia/microstate rather than a modern national generalship;
- all three explicitly rejected Prussian anachronisms remain rejected;
- **Andreas Hadik is retained, but remapped** from the Bukovina/Balkan formation to the central Austrian formation as an explicitly labelled `HIGHER_COMMAND_ABSTRACTION`;
- **Franz Moritz von Lacy is not recommended as a starting formation commander** on the cutoff date because the Hofkriegsrat presidency he formerly held ended in 1774.

The companion CSV is the authoritative one-row-per-formation implementation research matrix.

## 1. Repository scope audit

Primary formation file:

- `https://github.com/Malzars-sys/1776-Age-of-Revolutions/blob/cleanup-post-release/common/history/military_formations/00_military_formations_europe.txt`

### Prussia — 4 formations

| Slot | Formation | Current |
|---|---|---|
| GEN1776-003 | `cleanup2d3b_pru_land_4` | procedural |
| GEN1776-004 | `cleanup2d3b_pru_land_1` / `2_Armee` | procedural |
| GEN1776-005 | `cleanup2d3b_pru_land_2` / `main_Armee` | procedural |
| GEN1776-006 | `cleanup2d3b_pru_land_3` / `Elbe_Armee` | procedural |

### Habsburg complex

AUS has four separate armies:

| Slot | Formation | Current |
|---|---|---|
| GEN1776-009 | `cleanup2d3b_aus_land_3` — Bukovina/Balkans | Andreas Hadik |
| GEN1776-010 | `cleanup2d3b_aus_land_4` / `generalkommando_lemberg` | procedural |
| GEN1776-011 | `cleanup2d3b_aus_land_1` — central Austria | Franz Moritz von Lacy |
| GEN1776-012 | `cleanup2d3b_aus_land_2` / `armee_in_italien_scope` | procedural |

The file also represents Habsburg-space formations separately as:

- HUN — `generalkommando_ofen`
- TRS — `generalkommando_hermannstadt`
- GAL — `cleanup2d3b_gal_land_1`

Those tags must **not** be interpreted automatically as modern independent national armies.

### German/HRE formations

The file contains separate land formations for BAD, WUR, SAX, BAV, HEK, HES, NAS, HAN, MEC, OLD, HAM, BRE, LUB, FRM, WLD, LUX, SCH, HOL, COB, HOH, MEI, MST, SCW and WEI.

Many are one-battalion forces, city militia or tiny court contingents. A named “general” is therefore not automatically more historical than a procedural commander.

### Switzerland

SWI has a real land formation (`cleanup2d3b_swi_land_1`), but the Old Confederacy's military structure remained fundamentally cantonal rather than a unified national standing command.

### Italian formations included by current architecture

GEN, VEN, SIC (two land formations), SAR, PAP, TUS, LUC, MOD and PAR all possess land formations in the same Europe file and are included in the matrix.

## 2. Method

A candidate is accepted only when the relevant command or military office can be placed **on or before 1776-01-01**.

The following are not sufficient by themselves:

- later promotion during 1776;
- fame in later wars;
- being a ruler, governor or court official;
- holding a military rank without evidence of a current command useful for the formation;
- a plausible age generated from an unsourced birth date.

Four mapping classes are distinguished:

1. `DIRECT_HIGH_COMMAND` — actual army-wide command;
2. `DIRECT_TERRITORIAL_COMMAND` — actual territorial/general-command appointment;
3. `TERRITORIAL/INSPECTORATE_ABSTRACTION` — historical senior command whose jurisdiction is the closest defensible abstraction for a synthetic in-game army;
4. `HIGHER_COMMAND_ABSTRACTION` — central military leadership mapped to one in-game formation only because Victoria 3 requires a formation commander. This classification must be explicit.

## 3. Prussian audit — substantive Frederician search

### Recommended four

| Formation | Candidate | 1776 office | Mapping |
|---|---|---|---|
| `cleanup2d3b_pru_land_4` | **Friedrich Ehrenreich von Ramin** | Generalleutnant; Governor of Berlin since 1767 | territorial-command abstraction |
| `2_Armee` | **Friedrich Christoph von Saldern** | Generalleutnant; infantry inspector for Magdeburg/Altmark | inspectorate abstraction |
| `main_Armee` | **Wichard Joachim Heinrich von Möllendorff** | active senior Frederician general in inspectorate service | inspectorate abstraction |
| `Elbe_Armee` | **Friedrich Bogislaw von Tauentzien** | General der Infanterie; Governor of Breslau; Silesian infantry inspector | strong territorial/inspectorate abstraction |

### Friedrich Ehrenreich von Ramin

- **Born:** 1709-04-10, Brüssow, Uckermark.
- **Died:** 1782-12-02, Berlin.
- **Rank:** Generalleutnant.
- **Current 1776 office:** Governor of Berlin, appointed July 1767.
- **Social origin:** old landed nobility.
- **Use:** defensible for the broad central/Brandenburg slot, but not as a falsely labelled field-army commander.

Source: Deutsche Biographie — Friedrich Ehrenreich von Ramin — https://www.deutsche-biographie.de/gnd124458947.html

### Friedrich Christoph von Saldern

- **Born:** 1719-06-02, Kolberg.
- **Died:** 1785-03-14.
- **Religion:** Evangelical.
- **Rank:** Generalleutnant.
- **Current office:** inspector of the infantry stationed in Magdeburg and the Altmark, established after the Seven Years' War.
- **Use:** strong fit for the Anhalt/Magdeburg-oriented formation.

Source: Deutsche Biographie — Friedrich Christoph von Saldern — https://www.deutsche-biographie.de/gnd100202284.html

### Wichard Joachim Heinrich von Möllendorff

- **Born:** 1724-01-07, Lindenberg in the Prignitz.
- **Died:** 1816-01-28.
- **Religion:** Evangelical.
- **Background:** old Prignitz landed nobility.
- **1776 status:** active senior Frederician general in the post-war infantry-inspectorate system.
- **Caution:** the exact January-1776 rank and the exact inspectorate-transfer date should be checked against a contemporary Prussian `Rangliste` before final coding.

Source: Deutsche Biographie — Wichard Joachim Heinrich von Möllendorff — https://www.deutsche-biographie.de/gnd117081051.html

### Friedrich Bogislaw von Tauentzien

- **Born:** 1710-04-18, Tauentzien/Tawecino in Hinterpommern.
- **Died:** 1791-03-21, Breslau.
- **Rank:** General der Infanterie from 1775.
- **1776 office:** Governor of Breslau and Silesian infantry inspector.
- **Use:** strongest Prussian geographic match because `Elbe_Armee` is substantially based in Lower Silesia.

Source: Deutsche Biographie — Friedrich Bogislaw von Tauentzien — https://www.deutsche-biographie.de/gnd117250686.html

### Explicitly rejected Prussian anachronisms

**Wilhelm Johann von Krauseneck**

- born **1775-10-13**;
- did not enter military service until **1791**;
- therefore impossible as a starting general on 1776-01-01.

Source: Deutsche Biographie — Wilhelm Johann von Krauseneck — https://www.deutsche-biographie.de/gnd11640034X.html

**Helmuth Karl Bernhard von Moltke**

- born **1800-10-26**;
- impossible in 1776.

Source: Deutsche Biographie — Helmuth Karl Bernhard von Moltke — https://www.deutsche-biographie.de/gnd118583387.html

**Hans Ernst Karl Graf von Zieten**

- born **1770-03-05**;
- entered the army only in **1785**;
- impossible as a 1776 general.

Source: Deutsche Biographie — Hans Ernst Karl Graf von Zieten — https://www.deutsche-biographie.de/gnd116989890.html

These names **must not be restored**.

The older, famous hussar general **Hans Joachim von Zieten** is a different person. He was alive in 1776, but the four candidates above offer better evidence for active 1776 command/inspection functions tied to the synthetic formations. He is therefore not needed merely for name recognition.

## 4. Habsburg audit

### Why the command categories matter

The Habsburg army cannot be mapped historically by treating every high official as a field general. In 1776 there is a real distinction between:

- territorial `Generalkommando` structures;
- regional/field responsibility;
- the central `Hofkriegsrat`;
- State Council and conference functions.

The Austrian State Archives' institutional history confirms the key 1774 transition: Lacy left the Hofkriegsrat presidency and Hadik became president.

Source: Österreichisches Staatsarchiv / Archivinformationssystem — Hofkriegsrat administrative history — https://www.archivinformationssystem.at/archivplansuche.aspx?ID=2351669

### Recommended AUS mapping

| Formation | Recommendation | 1776 basis | Class |
|---|---|---|---|
| AUS-009 Bukovina/Balkans | **Gabriel Splényi** | appointed for Bukovina organization before cutoff | DIRECT_TERRITORIAL_COMMAND |
| AUS-010 `generalkommando_lemberg` | **Joseph/Josip Šišković** | commander in Galicia from 1775 | DIRECT_TERRITORIAL_COMMAND |
| AUS-011 central Austria | **Andreas Hadik** | Hofkriegsrat president since 1774 | HIGHER_COMMAND_ABSTRACTION |
| AUS-012 Italy/Lombardy | **Giovanni Battista Serbelloni** | commander general of imperial army in Italy from 1762 | DIRECT_REGIONAL_HIGH_COMMAND |

### Andreas Hadik — accepted, but remapped

- **Born:** 1710-10-16, Csallóköz / Große Schüttinsel, Kingdom of Hungary.
- **Died:** 1790-03-12, Vienna.
- **Religion:** Catholic.
- **Rank:** Feldmarschall from 1774.
- **1776 office:** President of the Hofkriegsrat.
- **Office start:** May 1774.
- **Why current mapping is weak:** by 1776 Hadik's relevant office is central, not command of the Bukovina/Balkan formation.
- **Decision:** retain him, but move him conceptually to the central Austrian formation as `HIGHER_COMMAND_ABSTRACTION`.

Sources:
- Deutsche Biographie — Andreas Hadik von Futak — https://www.deutsche-biographie.de/gnd129786578.html
- Österreichisches Staatsarchiv / Archivinformationssystem — Hofkriegsrat administrative history — https://www.archivinformationssystem.at/archivplansuche.aspx?ID=2351669

### Franz Moritz von Lacy — historically important, rejected for a starting formation

- **Born:** 1725-10-21, Saint Petersburg.
- **Died:** 1801-11-24, Vienna.
- **Religion:** Catholic.
- **Rank:** Field Marshal.
- **Army General Inspector:** from 1765.
- **Hofkriegsrat president:** 1766–1774.
- **After 1774:** State Council / conference role and continuing major influence.

The cutoff rule is decisive. His most directly relevant central military presidency had ended in 1774. Hadik actually held that office on 1776-01-01.

**Decision:** `REJECT_FOR_STARTING_FORMATION / HISTORICALLY_IMPORTANT_NOT_CURRENT_COMMAND`.

This does **not** mean that Lacy was militarily irrelevant in 1776. It means that using him as one of four formation commanders is less historically precise than using the officers who held current territorial commands plus Hadik as the current head of the Hofkriegsrat.

Sources:
- Deutsche Biographie — Franz Moritz von Lacy — https://www.deutsche-biographie.de/gnd118778404.html
- Österreichisches Staatsarchiv / Archivinformationssystem — Hofkriegsrat administrative history — https://www.archivinformationssystem.at/archivplansuche.aspx?ID=2351669

### Gabriel Freiherr Splényi von Miháldy

- **Born:** 1734-10-02, Ternyn, Upper Hungary.
- **Rank in period:** Generalmajor.
- **Appointment:** May 1773 to organize the newly acquired Bukovina; occupation/administrative command followed before 1776.
- **Direct fit:** AUS-009's permanent troops are based in Bukovina.
- **Death-date caution:** Deutsche Biographie/ADB gives **1814-04-01**; some older biographical traditions give **1818-04-01**. This must remain flagged until a primary record is checked.

Source: Deutsche Biographie — Gabriel Freiherr Splényi von Miháldy — https://www.deutsche-biographie.de/gnd121754561.html

### Joseph / Josip / József Šišković

- **Born:** 1719-07-02, Szeged.
- **Rank:** Feldzeugmeister.
- **1776 office:** military commander in Galicia.
- **Appointment:** 1775, before the reference date.
- **Transfer:** to Bohemia in 1779.
- **Portrait:** an eighteenth-century portrait is catalogued on Wikimedia Commons.
- **Death-date caution:** the Croatian Encyclopedia gives **1783-02-04, Prague**; December 1783 dates circulate in other databases.

Sources:
- Hrvatska enciklopedija — Josip Šišković — https://www.enciklopedija.hr/clanak/siskovic-josip
- Wikimedia Commons — Category: Josip Šišković — https://commons.wikimedia.org/wiki/Category:Josip_%C5%A0i%C5%A1kovi%C4%87

### Giovanni Battista Serbelloni

- **Born:** **1696**, exact day/month not established in this audit; some secondary traditions give 1697.
- **Background:** major Milanese aristocratic family.
- **Rank:** Imperial Field Marshal.
- **Command:** appointed commanding general of the Imperial Army in Italy in **1762**.
- **1776 fit:** direct Lombardy/Italy mapping.
- **Death:** 1778; exact day/month not asserted here.

Sources:
- Elena Riva, Università Cattolica, study on Giovanni Battista Serbelloni (2023) — https://publicatt.unicatt.it/handle/10807/273548
- Wienbibliothek Digital — Giovanni Battista Serbelloni — https://www.digital.wienbibliothek.at/name/view/5434297
- Treccani, Dizionario Biografico context for the Serbelloni family — https://www.treccani.it/enciclopedia/gian-galeazzo-serbelloni_%28Dizionario-Biografico%29/

### HUN, TRS and GAL

- **HUN / Ofen:** do not reuse Hadik's earlier Buda/Ofen role as if it were current in 1776; by then he is Hofkriegsrat president.
- **TRS / Hermannstadt:** no sufficiently verified 1776 military commander was established. A civil governor must not be promoted into an army general by inference.
- **GAL:** Šišković is already used for the explicit Lemberg command. Do not duplicate him across a second synthetic Galician formation without evidence of two independent commands.

Result: keep these three procedural for this phase.

### Laudon

Ernst Gideon von Laudon is deliberately **rejected for the reference date** despite his fame. His Moravian command ended in 1773 and he was not holding the required equivalent current command on 1776-01-01.

## 5. German states and HRE

### Saxony — Heinrich Christoph Graf von Baudissin

- **Born:** 1709-07-09, Schleswig.
- **1776 office:** military governor of Dresden, Neustadt and Königstein.
- **Rank:** senior Saxon general; archival/catalogue records use General der Infanterie while some summaries preserve lower historical rank wording.
- **Portrait:** contemporary portrait tradition, including an Anton Graff portrait engraved by C. G. Rasp in Dresden in 1777.
- **Decision:** accept for SAX as `TERRITORIAL_COMMAND_ABSTRACTION`.
- **Death-date caution:** catalogue traditions differ between 1786-06-04 and 1786-07-04.

Source: Deutsche Digitale Bibliothek — Heinrich Christoph Graf von Baudissin portrait/biographical record — https://www.deutsche-digitale-bibliothek.de/item/A3AN2XABQCQA3KJ6MIG3IOEJDYSUILBX

### Hanover — August Friedrich von Spörcken

- **Born:** 1698-08-28.
- **Rank:** Feldmarschall.
- **1776 office:** commanding general of Hanoverian/German forces.
- **Died:** night of 12/13 June 1776.
- **Decision:** accept. He is unquestionably still the command holder on **1 January 1776**.
- **Successor rule:** any successor taking command after his June death is a later-1776 appointment and cannot replace him at game start.
- **Birthplace caution:** the exact town of birth was not pinned down securely enough in the consulted biography to encode a precise V3 state without another primary/authority check.

Source: Deutsche Biographie — August Friedrich von Spörcken — https://www.deutsche-biographie.de/gnd117485225.html

### Hesse-Kassel

Officers associated with the Hessian expeditionary contingent to North America in 1776 — notably Leopold Philipp von Heister and later Wilhelm von Knyphausen — are not automatically admissible. The relevant expeditionary appointments/deployment fall later in 1776 unless a pre-1-January appointment can be proven.

Result: **keep HEK procedural** for this phase.

### Other German microstates

BAD, WUR, BAV, HES, NAS, MEC, OLD, HAM, BRE, LUB, FRM, WLD, LUX, SCH, HOL, COB, HOH, MEI, MST, SCW and WEI remain procedural.

This is intentional. Many current formations are single battalions, city militia or very small contingents. Replacing every procedural commander with a titled noble who merely possessed a military rank would create false historical precision.

## 6. Switzerland

SWI exists as a real in-game formation, but the Old Swiss Confederacy did not possess a modern centralized standing army with a permanent national commander in 1776.

The later federal military framework still preserved substantial cantonal responsibility, illustrating the persistence of the decentralized structure.

Source: Historisches Lexikon der Schweiz — Militärwesen / federal-cantonal military organization — https://hls-dhs-dss.ch/fr/articles/024638/

**Decision:** `KEEP_PROCEDURAL / NO_UNIFIED_COMMAND_1776`.

A later redesign toward cantonal/collective representation would be more historically faithful than inventing a single Swiss national general.

## 7. Italian states

The following formations were audited and retained procedural:

- Genoa
- Venice
- Two Sicilies — Royal Army
- Two Sicilies — Royal Guard
- Sardinia-Piedmont
- Papal States
- Tuscany
- Lucca
- Modena
- Parma

No ruler or governor was promoted to “general” merely because of political authority. No named candidate was accepted without a command appointment established by the cutoff.

The Habsburg Lombardy formation is the exception because Serbelloni has a documented imperial army command in Italy.

## 8. Repository DNA / template / event audit

Searched:

- `common/dna_data/`
- `common/character_templates/`
- `common/history/characters/`
- `common/history/military_formations/`
- `events/`

Findings:

- no candidate-specific reusable DNA was found for Hadik, Lacy, the four accepted Prussian officers, Splényi, Šišković, Serbelloni, Baudissin or Spörcken;
- `common/character_templates/country_aus.txt` contains primarily later nineteenth-century Austrian commanders and does not provide Hadik/Lacy;
- no `country_pru.txt` template file exists in the inspected branch;
- `common/history/characters/aus.txt` contains the 1776 Habsburg rulers but no hidden reusable profiles for these commanders;
- no relevant existing event hook was found that would supply the accepted candidates.

Therefore any future implementation should assume **new character definitions** unless a separate portrait/DNA phase deliberately creates reusable visual assets.

## 9. Portrait audit

| Candidate | Portrait result |
|---|---|
| Hadik | contemporary engraving tradition identified |
| Šišković | eighteenth-century portrait identified on Commons |
| Baudissin | contemporary portrait/engraving record identified |
| Ramin | not verified in this audit |
| Saldern | not verified in this audit |
| Möllendorff | not verified in this audit |
| Tauentzien | not verified in this audit |
| Splényi | not verified in this audit |
| Serbelloni | not verified in this audit |
| Spörcken | not verified in this audit |

“Not verified” means **do not invent DNA from a presumed likeness**. A dedicated portrait-source pass can be done later.

## 10. Final coverage

| Group | Formations |
|---|---:|
| Prussia | 4 |
| Italy — Genoa/Venice | 2 |
| AUS | 4 |
| Habsburg component formations | 3 |
| German/HRE core | 16 |
| Schleswig/Holstein | 2 |
| Italian states | 8 |
| German minor tags | 6 |
| Switzerland | 1 |
| **Total** | **46** |

**Named accepted:** 10  
**Procedural retained:** 36

Accepted names:

1. Friedrich Ehrenreich von Ramin
2. Friedrich Christoph von Saldern
3. Wichard Joachim Heinrich von Möllendorff
4. Friedrich Bogislaw von Tauentzien
5. Gabriel Freiherr Splényi von Miháldy
6. Joseph/Josip/József Šišković
7. Andreas Hadik von Futak
8. Giovanni Battista Serbelloni
9. Heinrich Christoph Graf von Baudissin
10. August Friedrich Freiherr von Spörcken

## 11. Data issues that must remain explicit before implementation

1. **Möllendorff:** confirm exact January-1776 rank and inspectorate chronology against a contemporary Prussian `Rangliste`.
2. **Splényi:** resolve 1814 vs 1818 death-year tradition and geolocate historical Ternyn precisely for the V3 birth state.
3. **Šišković:** resolve February vs December 1783 death-date traditions; verify exact mod state key for Szeged.
4. **Serbelloni:** keep birth precision at `YEAR` until an exact birth/baptism record is found; do not convert 1696/1697 conflict into an invented full date.
5. **Baudissin:** resolve June vs July 1786 death-date catalogue conflict.
6. **Spörcken:** verify exact birthplace before encoding a V3 birth state.
7. **Portraits/DNA:** no new DNA should be authored from an unverified image in this research phase.

## 12. Final implementation decision

This research phase supports a future implementation that would:

- replace all four procedural Prussian starting generals with genuine Frederician senior officers active in 1776;
- remap Hadik to the central Austrian formation as a clearly documented higher-command abstraction;
- remove Lacy from the starting-formation role while preserving his historical importance in documentation;
- fill the Bukovina, Lemberg, Lombardy, Saxony and Hanover slots with current 1776 officeholders;
- keep the remaining formations procedural rather than create false precision.

**No implementation has been performed in this conversation.**
