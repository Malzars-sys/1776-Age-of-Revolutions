# CLEANUP-2A — Global 1776 Character & Ruler Audit

Audit date: 2026-08-11  
Scenario reference date: 1776-01-01  
Scope: static start setup only; no Victoria 3 runtime; no gameplay correction.

## 1. Baseline

| Check | Result |
|---|---|
| Current branch | `cleanup-post-release` |
| Current HEAD | `25e346efd7c9ea247ad5946e8a756c2467c21ea2` |
| Expected commit | `Complete Maratha Konkan flotilla cleanup` |
| `git diff --check` before audit | PASS |
| Staged files before audit | none |
| Tracked gameplay diff before audit | none |
| Project invariants read | YES |
| Baseline clean for this audit | YES |

`BASELINE_CLEAN = YES` means no tracked or staged gameplay change was present. The pre-existing untracked CLEANUP-1D report and the seven protected technology research files were retained as-is and were not treated as audit output.

## 2. Character system architecture

The fork sets `START_DATE = "1776.1.1"` in `common/defines/00_defines.txt`.

The effective script inventory was reconstructed using Victoria 3 virtual-file-system filename precedence against the read-only vanilla 1.13 installation at `C:\Games\Victoria 3 The Great Wave\game`:

| Path | Fork files | Vanilla files | Exact-name overrides | Effective files |
|---|---:|---:|---:|---:|
| `common/history/characters` | 13 | 262 | 3 | 272 |
| `common/character_templates` | 27 | 210 | 24 | 213 |
| `common/history/military_formations` | 9 | 9 | 9 | 9 |

The descriptor has no `replace_path`. Consequently, a fork file such as `gbr.txt` does not replace vanilla `gbr - great britain.txt`; both are loaded. This filename mismatch is the main route by which 1836 characters enter the 1776 start.

The initial static system actually uses:

- country-scoped `create_character` in effective character history;
- `template = ...` resolved through the effective template set;
- `ruler = yes`, `ig_leader = yes`, `is_general = yes`, `is_admiral = yes`, and heir/other fields;
- `birth_date` or `age` for start age;
- `save_scope_as` plus `transfer_to_formation` for commanders;
- `create_character` inside military formation history.

No effective start-history use of `create_ruler` or `death_date` was found. Events and on-actions can create later characters, but are not deterministic 1776-start instances and are excluded from the starting total.

## 3. Global inventory

The machine-readable inventory is `docs/research/characters/STARTING_CHARACTERS_1776_AUDIT.csv`.

| Inventory measure | Count |
|---|---:|
| Deterministic scripted character instances | 611 |
| Unresolved/engine-generated ruler slots | 205 |
| Total audited entries | 816 |
| Countries detected from effective 1776 state ownership | 375 |
| Scripted ruler instances | 172 |
| Ruler audit rows | 377 |
| Countries with multiple scripted rulers | 2 (`AUS`, `SIC`) |
| Fork-sourced scripted instances | 75 |
| Vanilla-sourced scripted instances | 536 |

`TOTAL_INITIAL_CHARACTERS = 816` is therefore an audit-entry total: 611 deterministic scripted people plus 205 country ruler slots whose holder cannot be determined statically. `TOTAL_STARTING_RULERS = 377` represents 375 country slots plus two extra scripted ruler instances created by the Austrian and Sicilian duplicates.

Role rows are not mutually exclusive. The principal row labels are: 205 unresolved rulers, 138 ruler-only, 21 ruler/general, 13 ruler/IG leader, 167 IG-leader-only, 85 general-only, 24 admiral-only, 101 heir-only, and 49 other.

## 4. Automated chronological anomalies

Age was computed at 1776-01-01 from every available `birth_date`. The CSV preserves both the script date and computed value.

| Check | Count |
|---|---:|
| `NEGATIVE_AGE` | 285 |
| `BORN_AFTER_START` | 285 |
| `DEAD_BEFORE_START` | 0 |
| `AGE_FIELD_CONFLICT` | 0 |
| `IMPOSSIBLE_BIRTH_DEATH_ORDER` | 0 |
| `EXTREME_AGE` | 0 |

The same 285 rows account for both negative ages and post-start births. No `death_date` was present in the effective starting-character blocks, so zero dead-before-start findings means “none expressed in the audited start scripts,” not a universal biographical claim.

The worst computed ruler examples include:

| Country | Current scripted ruler | Script birth | Computed age | Actual 1776 holder / finding |
|---|---|---:|---:|---|
| `YOG` | Gathot Menol Hamengkubuwono | 1820-01-24 | -45 | inherited 1836 ruler; replacement research required |
| `POR` | Maria II | 1819-04-04 | -44 | José I |
| `MON` | Petar II Petrović-Njegoš | 1813-11-13 | -38 | inherited 1836 ruler; replacement research required |
| `RYU` | Shō Iku | 1813-08-19 | -38 | inherited 1836 ruler; replacement research required |
| `TRA` | Rama Varma | 1813-04-16 | -38 | inherited 1836 ruler; replacement research required |
| `SIC` | Ferdinand II | 1810-01-12 | -35 | Ferdinand IV/III already also scripted by the fork |
| `POR` | Maria II | 1819-04-04 | -44 | explicit major-power P0 |
| `CHI` | Daoguang | 1782-09-16 | -7 | Qianlong Emperor |
| `TUR` | Mahmud II | 1785-07-20 | -10 | Abdülhamid I |

## 5. Country rulers audit

Every one of the 375 country tags owning a state in the effective 1776 setup has a ruler row in the CSV. Static script tracing found:

- 170 countries with at least one explicit scripted ruler;
- 205 countries with no deterministic `ruler = yes` character, recorded as `NO_SCRIPTED_RULER` rather than assigned an invented person;
- `AUS` with Maria Theresa and Joseph II both marked ruler;
- `SIC` with the correct fork Ferdinand IV/III and the inherited vanilla Ferdinand II both marked ruler.

The audit classifies all 160 vanilla-sourced scripted ruler rows as `ANACHRONISTIC` at 1776 because they come directly from the unoverridden 1836 ruler setup. Of those, 66 are independently impossible by birth date; the remaining 94 are P1 replacement/research cases because being alive in 1776 does not make their later office valid.

The 66 post-start-born ruler tags are:

`AIT, ANK, ARB, AWA, BAL, BHN, BHV, BLG, BNJ, BRZ, BTN, BUR, CHC, CHI, CON, COO, CUB, DAI, GAR, GWA, HAI, HUN, HYD, JEY, JOH, KHP, KNO, KON, KOR, KTI, MAS, MGD, MLD, MON, MOR, NAG, NVS, ONT, ORA, PAN, PAR, PCO, PHI, PON, POR, PRK, PUD, QUE, RYU, SAK, SAR, SAT, SIC, SLW, SOK, SRK, STG, TID, TRA, TRN, TRS, TUG, TUR, UBD, WTU, YOG`.

Important ruler findings not caught by the negative-age test alone include:

| Country | Scripted holder | Why anachronistic or problematic | Expected 1776 representation |
|---|---|---|---|
| `PRU` | Friedrich Wilhelm, born 1770 | a later Hohenzollern generation, alive but not ruler | Frederick II |
| `SWE` | Karl Johan Bernadotte, born 1763 | did not become Swedish king until the nineteenth century | Gustav III |
| `JAP` | Tokugawa Ienari, age 2 | became shōgun later | Tokugawa Ieharu as shōgun |
| `MUG` | Akbar II, born 1760 | later Mughal emperor | Shah Alam II, with nominal/effective-power caveat |
| `USA` | George Washington as ruler | commander-in-chief in January 1776, not a civil president | John Hancock nominally headed Congress; Washington remains the military leader |
| `AUS` | Maria Theresa and Joseph II | co-regency is defensible, but both fork birth dates are wrong by decades | Maria Theresa dominant ruler; Joseph II junior co-regent |

For chartered companies, confederations, regencies, and composite states, `actual_1776_holder` deliberately distinguishes nominal and effective power where the evidence supports it. The 205 unresolved ruler slots remain `RESEARCH_REQUIRED`; no European-style monarch was silently invented.

## 6. Likely 1836 inheritance

`LIKELY_1836_INHERITANCE = YES` is assigned to all 536 scripted rows whose effective source is an unoverridden vanilla character-history file. This is a provenance classification, not merely a birth-date guess:

1. the vanilla installation is the 1836 setup;
2. the fork has no `replace_path` for character history;
3. only three of the fork's thirteen character-history filenames actually override a vanilla filename;
4. 285 inherited rows were not even born by 1776;
5. additional recognizable 1836 holders such as Bernadotte, Ienari, Akbar II, and the later Friedrich Wilhelm survive the simple birth test.

The 536 count includes 160 ruler rows and 376 secondary characters. A secondary person who was alive in 1776 is still marked for role research because the inherited 1836 office cannot be assumed valid sixty years earlier.

## 7. Historical research findings

The CSV carries per-row source URLs for confirmed major cases. Priority sources and conclusions:

| Current character | Expected 1776 character / office | Birth–death and office window | Finding | Sources | Confidence |
|---|---|---|---|---|---|
| Daoguang (`CHI`) | Qianlong Emperor | 1711–1799; reign 1735/36–1796 | P0 replacement | [Versailles](https://www.chateauversailles.fr/resources/pdf/en/presse/dp_trones_en.pdf); [Harvard](https://dash.harvard.edu/bitstreams/7126a52f-eca7-403c-a307-43e48186cdb5/download) | HIGH |
| Mahmud II (`TUR`) | Abdülhamid I | 1725–1789; sultan 1774–1789 | P0 replacement | [TDV İslâm Ansiklopedisi](https://islamansiklopedisi.org.tr/abdulhamid-i) | HIGH |
| Maria II (`POR`) | José I | 1714–1777; king 1750–1777 | P0 replacement | [Portuguese Parliament](https://www.parlamento.pt/VisitaParlamento/Paginas/BiogDJose.aspx); [Encyclopedia.com](https://www.encyclopedia.com/humanities/encyclopedias-almanacs-transcripts-and-maps/jose-i-portugal-1714-1777) | HIGH |
| Ferdinand II (`SIC`) | Ferdinand IV of Naples / III of Sicily | 1751–1825; king from 1759 | inherited duplicate; keep the fork's Ferdinand identity, remove duplicate in 2B | [British Museum](https://www.britishmuseum.org/collection/term/BIOG69450); [Prado](https://www.museodelprado.es/en/the-collection/art-work/fernando-iv-king-of-naples/08c55f28-8cd3-4947-bfaa-41a97f7d7773) | HIGH |
| Friedrich Wilhelm (`PRU`) | Frederick II | 1712–1786; king 1740–1786 | alive-but-wrong-generation inheritance | [University of Oxford](https://frederick.mml.ox.ac.uk/history); [Oxford timeline](https://frederick.mml.ox.ac.uk/timeline) | HIGH |
| Karl Johan Bernadotte (`SWE`) | Gustav III | 1746–1792; reign 1771–1792 | alive but anachronistic ruler | [Swedish Royal Court](https://www.kungahuset.se/sveriges-monarki/monarkins-historia) | HIGH |
| Akbar II (`MUG`) | Shah Alam II, nominal emperor | reign 1759–1806 | wrong Mughal generation | [British Library](https://searcharchives.bl.uk/catalog/040-003270088) | HIGH |
| Maria Theresa and Joseph II (`AUS`) | same co-regency identities | Maria Theresa 1717–1780, ruler 1740–1780; Joseph II 1741–1790, co-regent 1765–1780 | identities fit; script dates 1743 and 1764 do not | [Maria Theresa](https://www.habsburger.net/en/persons/habsburg-emperor/maria-theresa); [Joseph II and co-regency](https://www.habsburger.net/en/chapter/joseph-ii-co-regent) | HIGH |
| George III (`GBR`) | same ruler | born 1738; reign 1760–1820 | identity fits; exact script birth date is wrong | [Royal Family](https://www.royal.uk/george-iii) | HIGH |
| Louis XVI (`FRA`) | same ruler | 1754–1793; reign from 1774 | identity fits; exact script birth date is wrong | [Château de Versailles](https://www.chateauversailles.fr/decouvrir/histoire/grands-personnages/louis-xvi) | HIGH |
| Catherine II (`RUS`) | same ruler | 1729–1796; reign 1762–1796 | identity fits; exact script birth date is wrong | [British Museum](https://www.britishmuseum.org/collection/term/BIOG22234); [Metropolitan Museum](https://www.metmuseum.org/art/collection/search/198159) | HIGH |
| George Washington (`USA`) | John Hancock nominal civil head; Washington commander-in-chief | Hancock president of Congress 1775–1777; Washington presidency begins 1789 | country/office modeling decision, not an age-only fix | [U.S. House History](https://history.house.gov/People/Continental-Congress/Presidents/); [National Archives](https://www.archives.gov/legislative/features/washington) | HIGH |

These findings establish the major P0/P1 pattern. Regional batches must complete holder-level research for the remaining inherited rulers before changing gameplay.

## 8. Unknown / uncertain dates

| Date-quality class | Count |
|---|---:|
| `EXACT_DATE_CONFLICT_WITH_SOURCE` | 8 |
| `EXACT_DATE_WEAKLY_SOURCED` | 351 |
| `APPROXIMATION_NOT_DOCUMENTED` | 194 |
| `APPROXIMATE_AGE_DOCUMENTED` | 1 |
| `UNKNOWN` | 262 |

Only Anandrao Dhulap currently qualifies as `APPROXIMATE_AGE_DOCUMENTED`: `age = 40` is explicitly preserved because no reliable exact birth date was established. Karim Khan Zand is flagged for false-precision risk: a documented approximate age should be preferred to the exact `1705.1.5` unless a strong source is found. Timur Shah Durrani and the Mamluk Iraq identity also require focused research.

The weak/unknown classifications are intentionally conservative. Exact-looking script dates were not promoted to “well sourced” merely because they parse correctly.

## 9. Military commander inventory

The effective military history creates 148 armies and 49 fleets. Role-aware template resolution plus `save_scope_as`/`transfer_to_formation` tracing finds 111 armies without a general and 44 fleets without an admiral. These are inventory findings only; no commander was added.

### Armies without general

- `AGC`: `army_of_angoche`
- `ARB`: unnamed army
- `AUS`: `generalkommando_agram`, `generalkommando_lemberg`, `generalkommando_wien`, `armee_in_italien`
- `AWA`: `OudhRoyalArmy`
- `BAD`: `Groherzoglich_Badische_Armee`
- `BAV`: `I_ArmeeKorps`, `II_ArmeeKorps`
- `BEO`: `Armee_Belge`
- `BHV`: `BhavnagarArmy`
- `BRE`: `Bremer_Stadtmilitar`
- `BRZ`: `Exrcito_Imperial_Brasileiro`
- `BUR`: `tatmadaw`
- `CHC`: `Murtazeki`, `Milishia`
- `CHI`: `Zhili_Green_Standard_Army`, `LiangJiang_Green_Standard_Army`, `ShaanGan_Green_Standard_Army`, `MinZhe_Green_Standard_Army`, `LiangHu_Green_Standard_Army`, `LiangGuang_Green_Standard_Army`, `YunGui_Green_Standard_Army`, `Sichuan_Green_Standard_Army`
- `CIR`: two unnamed armies
- `COC`: `CochinArmy`
- `COO`: `CoochBeharArmy`
- `CUB`: `MiliciasdeCuba`
- `DEI`: `Koninklijk_Nederlandsch_Indisch_Leger`
- `DENNOR`: `Hren`
- `DUR`: eight unnamed armies
- `FRM`: `Linienbataillon_Frankfurt`
- `GAR`: `GarhwalArmy`
- `GBR`: `Army_of_the_Mediterranean`
- `GEN`: unnamed army
- `GWA`: `GwaliorArmy`
- `HAI`: `ArmeeIndigene`
- `HAM`: `Hamburger_Burgermilitar`
- `HAN`: `Kniglich_Hannoversche_Armee`
- `HEK`: `Kurfrstlich_Hessische_Armee`
- `HES`: `Groherzoglich_Hessische_Armee`
- `HOL`: `Holsteinische_Armee`
- `HUN`: `generalkommando_ofen`
- `HYD`: `sarf_e_khas`
- `JAP`: `Edo_Guard_Army`, `Kinai_Guard_Army`, `Kyushu_Guard_Army`
- `JEY`: `JeyporeArmy`
- `KHP`: `KolhapurArmy`
- `KNO`: `KurnoolArmy`
- `LUB`: `Lubecker_Militar`
- `LUC`: `Esercito_Ducale`
- `LUX`: `Luxemburger_Miliz`
- `MARATH`: `OudhRoyalArmy`
- `MAS`: `Jaish_alMohammadi`
- `MEC`: `Groherzoglich_MecklenburgischSchwerinsche_Armee`
- `MOD`: `Esercito_del_Ducato_di_Modena_e_Reggio`
- `MOL`: `Armata_Principatului_Moldovei`
- `MON`: `Montengrin_Raiders`
- `MUG`: `MughalArmy`
- `MYS`: `MysoreArmy`
- `NAG`: `NagpurArmy`
- `NAS`: `Herzoglich_Nassauische_Armee`
- `NET`: `Koninklijk_Nederlands_Leger`, `korps_mariniers`
- `OLD`: `Groherzoglich_Oldenburgische_Armee`
- `OMA`: unnamed army
- `PAN`: `FaujiKhas`, `FaujiAin`
- `PAP`: `Esercito_dello_Stato_della_Chiesa`
- `PAR`: `Truppe_Reali_Parmensi`
- `PCO`: `MiliciasDiciplinadas`
- `PER`: two unnamed armies
- `PHI`: `ejercito_de_filipinas`
- `POR`: `Exercito_Portugues`
- `PRU`: `1_Armee`
- `PUD`: `PudukottaiArmy`
- `RUS`: `1y_Pekhotniy_Korpus`
- `SAR`: `I_Corpo_dArmata`, `II_Corpo_dArmata`
- `SAT`: `SataraArmy`
- `SAX`: `Kniglich_Schsische_Armee`
- `SC2`: `Ejrcito_del_Ecuador`, `Ejrcito_de_la_Nueva_Granada`, `Ejrcito_de_Venezuela`
- `SC4`: `Ejrcito_Argentino`
- `SCH`: `Schleswigsche_Armee`
- `SIC`: `Reale_Esercito_di_SM_il_Re_del_Regno_delle_Due_Sicilie`, `Guardia_Reale`
- `SIN`: `SindhArmy`
- `SWE`: `Kungliga_Svenska_Armn`
- `TRA`: `TravancoreArmy`
- `TRS`: `generalkommando_hermannstadt`
- `TUR`: `Konstantiniyye_Ordusu`, `Anadolu_Ordusu`
- `TUS`: `Esercito_del_Granducato_di_Toscana`
- `UBD`: unnamed army
- `VEN`: unnamed army
- `WAL`: `Armata_rii_Romneti`
- `WLD`: `Waldecksches_Bataillon`
- `WUR`: `Kniglich_Wrttembergische_Armee`

### Fleets without admiral

- `AUS`: unnamed fleet
- `BEO`: `Marine_Royale`
- `BRZ`: `Armada_Nacional`
- `DEI`: `Koloniale_Marine`
- `DENNOR`: `Kongelige_Danske_Marine`
- `FRA`: `Escadre_de_la_Mditerrane`, `Escadre_du_Nord`, `Station_des_Antilles`, `Station_de_latlantique_sud`
- `GBR`: `Mediterranean_Station`, `Lisbon_Station`, `North_America_and_West_Indies_Station`, `Cape_of_Good_Hope_Station`, `East_Indies_and_China_Station`, `South_America_Station`, `Portsmouth_Station`, `Plymouth_Station`, `Sheerness_Station`, `Chatham_Station`
- `GEN`: `merchant_venice_fleet`
- `HAN`: `Elbzollstation`
- `NET`: `Koninklijke_Marine`
- `OMA`: `Bahriat_alMasqat`
- `PAP`: `Marina_Pontificia`
- `POR`: `Marinha_Real_Portuguesa`
- `PRU`: `Kniglich_Preuische_Marine`
- `RUS`: `Baltiyskiy_Flot`, `Chernomorskiy_Flot`
- `SAR`: `Marina_del_Regno_di_Sardegna`
- `SC4`: `Armada_Argentina`
- `SIC`: `Armata_di_Mare_di_SM_il_Re_del_Regno_delle_Due_Sicilie`
- `SWE`: `Hgsjflottan`
- `TRA`: `TravancoreNavy`
- `TRI`: `Escadre_de_Tripoli`
- `TUN`: `Bahriat_alTuwnusia`
- `TUR`: `Donanmay_Humyn`
- `TUS`: `Marina_del_Granducato_di_Toscana`
- `USA`: `Navy_Yard_Gosport`, `Navy_Yard_New_York`, `Navy_Yard_Boston`, `Mediterranean_Squadron`, `Pacific_Squadron`, `West_Indies_Squadron`
- `VEN`: `merchant_venice_fleet`

### Maratha technology/commander distinction

`Konkan_Flotilla` is not in the missing-admiral list. `MARATH_anandrao_dhulap` resolves from its template as an admiral and is transferred to `scope:konkan_flotilla`.

The previously observed absence/non-function of the true `building_naval_administration` without `admiralty` is separately documented in `docs/reports/cleanup/CLEANUP1E_MARATH_FINAL_ACCEPTANCE.md`, sections 6–9. The project invariant also records MARATH's temporary inherited naval-administration-without-`admiralty` state and the future progressive naval-technology requirement. Therefore, if that building does not appear, the documented technology gate/dilemma must be checked before treating it as a missing formation, missing character, or missing building-history definition. CLEANUP-2A performed no runtime test and made no technology change.

## 10. Priority matrix

| Priority | Count | Meaning in this audit |
|---|---:|---|
| `P0_CRITICAL` | 285 | impossible post-1776 birth / negative computed age |
| `P1_HIGH` | 102 | inherited ruler alive but in anachronistic office, major ruler date/office error, or duplicate ruler |
| `P2_MEDIUM` | 365 | unresolved ruler slot, inherited secondary role, or targeted identity/date research |
| `P3_LOW` | 1 | documented false-precision risk (Karim Khan) |
| `OK` | 63 | no anomaly established by this audit |

The 102 P1 rows comprise 94 inherited vanilla rulers not already P0, the three duplicate/co-ruler rows already exposed by static multiplicity, and five fork-authored major-ruler date/office cases (`FRA`, `GBR`, `RUS`, `SPA`, `USA`). P0 takes precedence when a row satisfies both anachronistic provenance and impossible birth.

## 11. Proposed CLEANUP-2B batches

No batch was started. Recommended correction sequence:

1. **2B-1 — impossible dates:** remove or replace all 285 post-start-born instances; add regression checks for negative ages.
2. **2B-2 — major powers and duplicate rulers:** `CHI`, `TUR`, `POR`, `PRU`, `SWE`, `JAP`, `MUG`, `AUS`, `SIC`, plus exact-date repairs for `FRA`, `GBR`, `RUS`, `SPA` and the `USA` representation decision.
3. **2B-3 — character-history loading fix:** choose explicit effective-file overrides or a deliberate replacement strategy so vanilla 1836 character files cannot silently load. Validate scope before editing because broad `replace_path` can also remove required templates/history.
4. **2B-4 — Europe:** remaining P1/P2 rulers, composite Habsburg tags, colonies, and regencies.
5. **2B-5 — India and South Asia:** nominal versus effective rulers, charter-company governance, Maratha/Peshwa representation, Mughal/Company relations.
6. **2B-6 — Middle East and Central Asia:** Ottoman dependencies, Persia, Durrani, Mamluk Iraq, khanates.
7. **2B-7 — East and Southeast Asia:** Qing, Tokugawa, Korea, Ryukyu, Vietnamese and Indonesian polities.
8. **2B-8 — Americas and Africa:** January-versus-July 1776 USA mapping, colonial governors, confederations and decentralized authorities.
9. **2B-9 — secondary characters:** inherited IG leaders, heirs, generals, admirals, and false-precision cleanup.
10. **Future military rebalance:** separately assign commanders to the 111 armies and 44 fleets under the Commander Completeness Rule; do not mix it into character chronology fixes.

## 12. Protected-state verification

Final validation confirms:

- no gameplay file was modified by CLEANUP-2A;
- no file is staged;
- `git diff --check` passes;
- the seven protected technology research files remain untracked, byte-identical to their baseline hashes, and unstaged;
- `bject` remains absent;
- BIC still contains `activate_law = law_type:law_frontier_colonization`;
- BIC does not contain `law_colonial_exploitation`;
- the only new CLEANUP-2A outputs are this report and the character audit CSV;
- Codex did not launch Victoria 3.

## 13. Final verdict

The global static audit is complete enough to begin scoped CLEANUP-2B work. It is not a claim that all 205 engine-generated ruler identities have already been historically resolved. Rather, every 1776 country slot and every deterministic initial character has an auditable row, all impossible dates are enumerated, inherited 1836 provenance is exposed, major ruler cases are sourced, and the remaining research is explicitly batched.

```text
TOTAL_INITIAL_CHARACTERS = 816
TOTAL_STARTING_RULERS = 377
NEGATIVE_AGE_COUNT = 285
BORN_AFTER_START_COUNT = 285
DEAD_BEFORE_START_COUNT = 0
ANACHRONISTIC_RULER_COUNT = 160
LIKELY_1836_INHERITANCE_COUNT = 536
ARMIES_WITHOUT_GENERAL = 111
FLEETS_WITHOUT_ADMIRAL = 44
P0_CRITICAL_COUNT = 285
P1_HIGH_COUNT = 102
GLOBAL_CHARACTER_AUDIT_COMPLETE = YES
GAMEPLAY_FILES_MODIFIED = NO
CODEX_LAUNCHED_VICTORIA3 = NO
SAFE_TO_BEGIN_CLEANUP2B = YES
```
