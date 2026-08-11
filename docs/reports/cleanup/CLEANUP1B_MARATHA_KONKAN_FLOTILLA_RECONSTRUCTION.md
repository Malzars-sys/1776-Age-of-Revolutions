# CLEANUP-1B — Maratha Konkan Flotilla Reconstruction

## 1. Baseline

- Repository: `1776 - Age of Revolutions Fork`.
- Target: Victoria 3 1.13 / The Great Wave.
- Branch checked before editing: `cleanup-post-release`.
- Starting HEAD checked before editing: `1e374f2f40252d229bc249600e3cbbe26085122d`.
- Starting tracked and staged diff: empty.
- Protected stash: `stash@{0}`, hash `518df704fa14599c0f254fae13859210663dd976`.
- Vanilla reference tree: `C:\Games\Victoria 3 The Great Wave\game`.
- No runtime launch is part of CLEANUP-1B.

## 2. CLEANUP-1A constraints inherited

The full CLEANUP-1A forensic report was read first. Its binding conclusions were followed:

- the stash was not applied, popped, dropped, or otherwise mutated;
- the work was reconstructed from the current HEAD;
- `Konkan_Flotilla`, the EN/FR names, `type = fleet`, and `hq_region = sr:region_south_india` were retained;
- no `state_region` was put in a `ship` block;
- the MARATH land formation remains at `region_north_india`;
- neither one frigate nor one naval-administration level was accepted merely because it appeared in the WIP;
- `admiralty` was not added during the initial CLEANUP-1B reconstruction; the later CLEANUP-1E runtime A/B result required a documented temporary grant;
- no commander was invented.

## 3. Victoria 3 naval abstraction

### 3.1 Local vanilla evidence

| GAME_SHIP_TYPE | CREW_OR_EMPLOYMENT_REQUIREMENT | SUPPORT_BUILDING | SUPPORT_CAPACITY_PER_LEVEL | NOTES |
|---|---:|---|---:|---|
| `ship_type_frigate` | 500 sailors per game ship | `building_naval_administration` | 1,000 sailors with `pm_simple_sailor_recruitment` | Two frigate objects consume the full nominal capacity of one fully employed level. |
| `ship_type_ship_of_the_line` | 800 sailors per game ship | `building_naval_administration` | 1,000 sailors with `pm_simple_sailor_recruitment` | The type is mechanically possible but historically rejected for MARATH in 1776. |

The values are defined locally in:

- `common/ship_types/00_ship_types.txt`: `ship_crew_max_add = 500` for frigates and `800` for ships of the line;
- `common/buildings/05_military.txt`: `building_naval_administration`, `recruits_sailors = yes`, unlock technology `admiralty`;
- `common/production_methods/05_military.txt`: `pm_simple_sailor_recruitment`, 900 soldiers plus 100 officers of employment per level, and `country_sailors_max_add = 1000` when fully staffed;
- `common/defines/00_defines.txt`: `SAILORS_PER_ASSIGNMENT_SLOT = 100` and `SAILORS_PER_BUILDING_LEVEL = 1000`.

`reserves = 1` in building history is a generic building reserve setting. It is not a second sailor pool and does not increase naval capacity.

### 3.1.1 Naval Administration is not the Naval Logistics Center

The two vanilla 1.13 buildings must not be conflated:

| UI name | Internal ID | PM | Naval function |
|---|---|---|---|
| Naval Administration | `building_naval_administration` | `pm_simple_sailor_recruitment` | Has `recruits_sailors = yes`; at full employment one level supports 1,000 sailors and ten 100-sailor assignment slots. |
| Naval Logistics Center | `building_naval_logistics_center` | `pm_basic_naval_logistics_center` | Auto-placed supply/logistics building with 60 laborers, 30 bureaucrats, and 10 officers per level; it has no sailor-capacity modifier and no ship-crew assignment slots. |

The runtime appearance of a level-one Naval Logistics Center does not prove that the history script created the wrong building. Its building group has `auto_place_buildings = yes`, while the CLEANUP-1B history block explicitly requests `building_naval_administration`. The fleet's `0 / 1.00K` crew figure is current crew versus the two frigates' combined requirement, not sailor capacity supplied by the logistics center.

### 3.2 Meaning of `count`

In the history script, `count = 1` creates one game ship object. Each object receives the selected ship type's mechanical crew ceiling. Vanilla initial formations use these objects as OOB abstractions, with name distribution and crew mechanics applied per object. Nothing in the script equates one object to exactly one historical hull.

Therefore the conversion in this report is by represented manpower, not by copying the historical hull count. A game frigate is a 500-sailor naval unit that can aggregate several smaller grabs, ketches, gallivats, or other coastal craft.

### 3.3 Initial support scaling

The local vanilla OOB contains small one-frigate fleets commonly paired with one naval-administration level, while larger fleets generally receive more capacity. The relationship is not a perfect historical hull-for-hull formula, but the hard manpower requirement remains. No other vanilla starting building or production method found in the audit grants the required `country_sailors_max_add`.

For the selected setup:

`2 frigates × 500 sailors = 1,000 sailors = 1 naval-administration level × 1,000 capacity`.

## 4. Historical research

### 4.1 Situation around 1 January 1776

The destruction of Tulaji Angre's major force at Vijaydurg/Gheria in 1756 did not end all Maratha naval activity. The Peshwa government subsequently maintained a distinct establishment at Vijaydurg under Anandrao Dhulap. This Peshwa/Dhulap establishment is the relevant force for MARATH; the separate Kolaba/Angre force is not silently added to it.

Official Maharashtra gazetteer material describes a large Peshwa fleet action off Gheria in December 1774. Its enumeration comprises an admiral's ship of 44 guns, three vessels of 24–32 guns, five ketches of 12–14 guns, and ten gallivats of 6–10 guns. The admiral's ship burned and exploded after engaging the Bombay Marine; only 34 of the 420 aboard were reportedly saved, while the other Maratha vessels withdrew under the fort. An institutional Marathi encyclopedia describes what is evidently the same loss on 1 February 1775, names the flagship `Samsherjang`, gives it 46 guns, and identifies Damaji Naik Kuveskar as its commander. The date and exact gun figure conflict slightly, so the event is treated as securely attested but not assigned a falsely exact date here.

Most importantly for the scenario date, the National Archives of India's descriptive list for Secret Department records contains April–May 1776 entries on the proceedings and harassment conducted by the Maratha fleet, and identifies Anandrao Dhulap as a Peshwa naval officer. This is direct evidence that a force remained operational after the flagship loss and during 1776.

The exact strength on 1 January 1776 is not preserved in the consulted evidence. A modern web article reporting Portuguese letters gives a 1772 force of three three-masted `pals`, two grabs, seventeen smaller vessels, and 1,500–2,000 men. Because the archival letters were not inspected directly and because this precedes the flagship loss, that number is LOW-confidence corroboration only. It is not used as an exact 1776 OOB.

### 4.2 Ports and role

- Vijaydurg/Gheria was the documented seat of the Peshwa naval establishment and of Anandrao Dhulap.
- The force operated on the Konkan coast, contested shipping, attacked or captured enemy vessels, and made Company convoy protection necessary.
- Its craft mix and operations support a coastal/cruising abstraction, not a surviving European-style line-of-battle squadron.
- `STATE_BOMBAY` is the mod's map-level representation for MARATH's Konkan coastal infrastructure. It already contains MARATH ports and a shipyard. The fleet itself is correctly attached to `region_south_india`; ships do not take a `state_region` field in the 1.13 syntax.

### 4.3 Retained claims and confidence

| CLAIM | DATE | SOURCE | SOURCE_TYPE | CONFIDENCE |
|---|---|---|---|---|
| The major Angre force at Vijaydurg was destroyed in 1756, but later Peshwa naval activity continued. | 1756 and after | Amarendra Kumar; B. K. Apte; Maharashtra Gazetteers | Academic overview, scholarly monograph, institutional gazetteer | HIGH |
| The Peshwa maintained a naval establishment at Vijaydurg under Anandrao Dhulap. | 1760s–1790s | Maharashtra Gazetteers; Marathi Vishwakosh | Institutional secondary sources | HIGH |
| A salaried administrative apparatus existed under Dhulap. | 1765–1766 | chapter evidence in *Wage Earners in India 1500–1900* | Academic edited volume drawing on Maratha records | MEDIUM-HIGH |
| A substantial Peshwa fleet fought off Gheria; its large flagship was destroyed and the smaller vessels withdrew. | December 1774 / February 1775 | Bombay Presidency Gazetteer; John D. Grainger; Marathi Vishwakosh | Institutional gazetteer and modern scholarly synthesis | HIGH for the event; MEDIUM for the exact date/details |
| The Maratha fleet was active and harassing shipping in April 1776. | April–May 1776 | National Archives of India, Secret Department records descriptive list | Primary-archive finding aid | HIGH |
| The 1772 force may have totalled 1,500–2,000 personnel across roughly twenty-two craft. | 1772 | NDHistories summary of Portuguese correspondence | Tertiary web summary of claimed primary letters | LOW |
| Exact ship and crew totals on 1 January 1776 are not established by the consulted sources. | 1 January 1776 | Synthesis of all sources | Research conclusion | HIGH |

### 4.4 Command

`HISTORICAL_ADMIRAL_FOUND = YES`.

- Identity: Anandrao Dhulap.
- Function: Peshwa naval officer/subhedar associated with the Vijaydurg establishment.
- Active dates: institutional sources place his naval activity broadly from 1764 to 1795; British records identify him in 1776.
- Confidence: HIGH that he is a real and relevant commander.

The permanent `Commander Completeness Rule`, adopted before CLEANUP-1B was committed, requires every initial fleet to have at least one admiral regardless of formation size. Anandrao Dhulap is therefore implemented and assigned to `Konkan_Flotilla`.

No reliable consulted source supplies his birth date. The local vanilla 1.13 audit found that all 81 inspected historical admiral templates provide either `birth_date` or `age`, and that vanilla uses `age` for uncertain biographies. The template therefore uses `age = 40` at the 1 January 1776 start as an explicitly documented technical approximation, not as an asserted historical birth year. It gives a plausible approximate age of 28 at the start of his attested command in 1764 and 59 at its end in 1795. No exact day or year of birth is invented.

## 5. Sources

1. **Amarendra Kumar**, “Maratha Navy,” *Oxford Bibliographies in Military History*, Oxford University Press, 2023. Academic orientation on the rise, coastal character, and 1756 destruction of the earlier major force.  
   https://academic.oup.com/reference/62399/reference-article-abstract/555376418

2. **B. K. Apte**, *A History of the Maratha Navy and Merchantships*, Maharashtra State Board for Literature and Culture, Government of Maharashtra, 1973. Standard monograph and bibliographic anchor; no inaccessible page was used as the sole support for a numerical claim.  
   https://books.google.com/books/about/A_History_of_the_Maratha_Navy_and_Mercha.html?id=bgHlAAAAMAAJ

3. **Government of Maharashtra, Gazetteers Department**, *Gazetteer of the Bombay Presidency*, Volume I, Part II, and “History of the Konkan,” section 9. Retained for the Gheria action, the Peshwa fleet at Vijaydurg, Dhulap, and coastal operations.  
   https://ocrdigitalfile.nvli.in/snarepository/other/Watermarked-Gazetteer_of_Bombay_Presidency-Vol-1_Part-II_compressed-ocr.pdf  
   https://www.gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/Gazetteer%20of%20Bombay%20Presidency/history_of_the_konkan/section_9.pdf

4. **Government of Maharashtra, Gazetteers Department**, *Ratnagiri District Gazetteer*, history and Vijaydurg entries. Retained for Vijaydurg as the post-1756 Peshwa naval seat and for later Dhulap operations.  
   https://www.gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/RATNAGIRI/his_english.html  
   https://gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/RATNAGIRI/places_Vijaydurg.html

5. **John D. Grainger**, *The British Navy in Eastern Waters: The Indian and Pacific Oceans*, Boydell & Brewer, 2022. Modern scholarly synthesis corroborating the 1774/1775 encounter and describing a Maratha fleet of twenty-three craft ranging from gallivats to the 46-gun `Shumsher Jung`.  
   https://www.cambridge.org/core/books/british-navy-in-eastern-waters/9221C0596BE457DE3895CC96991C5F1D

6. **Marathi Vishwakosh / Maharashtra Rajya Marathi Vishwakosh Nirmiti Mandal**, “Anandrao Dhulap.” Institutional encyclopedia entry retained for Dhulap's office and career and the `Samsherjang` action; its date variant is reported rather than reconciled by invention.  
   https://marathivishwakosh.org/74035/

7. **National Archives of India**, K. D. Bhargava (ed.), *Descriptive List of Secret Department Records, Volume II, 1776–1780*, Government of India, 1969. Archive finding aid retained for the April–May 1776 records on the proceedings and harassment by the Maratha fleet and the identification of Dhulap.  
   https://upload.wikimedia.org/wikipedia/commons/2/27/Descriptive_List_Of_Secret_Department_Records_Vol._2_%28IA_in.ernet.dli.2015.44172%29.pdf

8. **Jan Lucassen and Radhika Seshan (eds.)**, *Wage Earners in India 1500–1900: Regional Approaches in an International Context*, Sage, 2022. Retained for evidence from 1765–1766 accounts of a salaried officer assigned to naval administration under Dhulap.  
   https://pure.knaw.nl/portal/files/443773278/Wage_Earners_in_India_1500_1900.SAGE_Spectrum.pdf

9. **Government of Maharashtra, Gazetteers Department**, *Greater Bombay District Gazetteer*, history entry. Retained as corroboration that the Bombay government regarded exported European naval stores as strengthening Maratha naval power in 1771.  
   https://www.gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/greater_bombay/history.html

10. **NDHistories**, April 2026 article summarizing Portuguese correspondence from 1772. Used only as LOW-confidence corroboration for a broad pre-loss manpower range, never as the sole basis for the final count.  
    https://ndhistories.wordpress.com/2026/04/

## 6. Translation to Victoria 3

The securely established facts are an active Peshwa fleet in 1776, a surviving group of medium and small craft after the loss of the flagship, and a formal naval establishment. The uncertain fact is the exact 1 January complement.

The rejected low-confidence 1772 estimate would correspond to roughly three or four frigate crew-equivalents before the loss. Subtracting the reported flagship casualties and assuming all other crews remained would be false precision. A conservative lower translation is therefore used:

`plausible organized surviving naval manpower >= approximately 1,000`

`1,000 / 500 sailors per frigate object = 2 frigate objects`

This is an order-of-magnitude abstraction, not a claim that MARATH owned two historical European frigates.

## 7. Options considered

| OPTION | HISTORICAL_FIT | GAMEPLAY_FIT | MANPOWER_FIT | CONFIDENCE | VERDICT |
|---|---|---|---|---|---|
| A — no initial fleet | Poor: contradicted by April 1776 activity | Safe but erases documented capability | Represents 0 sailors | HIGH | REJECT |
| B — one frigate | Partial: acknowledges presence | Minimal and easy to support | 500 sailors; likely below the surviving multi-vessel establishment | MEDIUM | REJECT |
| C — more than one frigate | Good at two; increasingly speculative above two | Two objects fit one support level exactly | 1,000 sailors at count 2 | MEDIUM | ACCEPT AT COUNT 2 |
| D — include ship of the line | Poor: the 44–46-gun flagship was lost before 1776 and no surviving line-of-battle ship is attested | Mechanically heavier and misleading | At least 800 sailors for the line unit, plus escorts | HIGH | REJECT |

## 8. Final implementation decision

```text
MARATH_NAVAL_HISTORICAL_ASSESSMENT = ACTIVE_PESHWA_COASTAL_FLEET_AT_VIJAYDURG_IN_1776
MARATH_RECOMMENDED_SHIP_TYPE = ship_type_frigate
MARATH_RECOMMENDED_SHIP_COUNT = 2
MARATH_RECOMMENDED_NAVAL_ADMIN_LEVEL = 1
MARATH_RECOMMENDED_ADMIRAL = Anandrao Dhulap
MARATH_TEMPORARY_ADMIRALTY_GRANT = YES
CONFIDENCE = MEDIUM
```

Implemented setup:

- one `Konkan_Flotilla` formation for MARATH;
- `type = fleet`;
- `hq_region = sr:region_south_india`;
- two `ship_type:ship_type_frigate` objects;
- no `state_region` inside the ship block;
- one `building_naval_administration` level in MARATH's `STATE_BOMBAY` region state;
- `pm_simple_sailor_recruitment` active;
- one temporary `add_technology_researched = admiralty` grant, accepted only after the final runtime A/B test proved it necessary for the current vanilla 1.13 setup;
- Anandrao Dhulap created as a historical admiral and transferred to `Konkan_Flotilla`;
- `age = 40` used as a documented technical approximation because his birth date is unknown;
- `culture = cu:marathi` and `home_region = STATE_BOMBAY`; religion and portrait are not forced;
- EN `Konkan Flotilla` and FR `Flottille du Konkan` localizations.

Following the exact 1.13 history syntax, the new formation is nested inside `c:MARATH ?= { ... }`. Vanilla formations in this scope do not repeat a `country = c:MARATH` field inside `create_military_formation`.

The fleet is saved as `scope:konkan_flotilla`. A character created from `MARATH_anandrao_dhulap` is saved as `scope:anandrao_dhulap_admiral`, then attached with `transfer_to_formation = scope:konkan_flotilla`. This is the template-and-scope pattern used by vanilla 1.13 initial fleets.

### Naval-administration legitimacy and limitation

The building is necessary: no alternate vanilla sailor-capacity source was found, and two frigates require its full 1,000-sailor capacity. It is also historically substantive rather than a synthetic workaround: Vijaydurg had a Peshwa naval command and salaried administration under Dhulap.

The history command requests a starting building directly, but CLEANUP-1C did not prove that the engine accepts and activates this inherited building when its declared unlock technology is absent. MARATH uses `effect_starting_technology_tier_5_tech`, which grants `navigation` but not `admiralty`; the vanilla definition of `building_naval_administration` explicitly lists `admiralty` as its unlock. The level-one Naval Logistics Center observed at runtime is auto-placed and cannot answer whether the requested Naval Administration survived initialization.

This was the documented pre-A/B-test MARATH technology dilemma. The project's `Naval Progression Access Rule` deliberately sought an inherited MARATH naval administration without `admiralty` as a temporary design state, while reserving a progressive non-European solution for the future technology overhaul. The final runtime result below supersedes that provisional no-grant position for current vanilla 1.13.

### CLEANUP-1E final runtime resolution

The provisional no-Admiralty conclusion above is superseded by the final user runtime A/B test. Without `admiralty`, the history request did not materialize a functional true Naval Administration: the separately auto-placed Naval Logistics Center appeared, crew remained `0 / 1,000`, and the real recruitment building was absent. After adding `add_technology_researched = admiralty` and starting a new 1 January 1776 campaign, the true level-one Naval Administration appeared separately and Konkan Flotilla reached `1,000 / 1,000` sailors.

The temporary grant is required by the current vanilla 1.13 initialization path, but it is not the intended final technology design. The project's `Naval Progression Access Rule` still requires a future progressive solution for regional naval powers such as MARATH.

## 9. Files modified

- `common/history/buildings/10_india.txt`
- `common/history/countries/marath - maratha empire.txt`
- `common/character_templates/country_marath.txt`
- `common/history/military_formations/05_military_formations_india.txt`
- `localization/english/phase_navy_3c_maratha_fleet_l_english.yml`
- `localization/french/phase_navy_3c_maratha_fleet_l_french.yml`
- `docs/design/1776_PROJECT_INVARIANTS.md`
- `docs/reports/cleanup/CLEANUP1B_MARATHA_KONKAN_FLOTILLA_RECONSTRUCTION.md`

The absent legacy report `docs/reports/navy/PHASE_NAVY_3C_3_MARATHA_KONKAN_FLOTILLA.md` was not restored from the stash. This report supersedes the WIP conclusions.

## 10. Static validation

Static validation passed:

- `common/history/buildings/10_india.txt`: 704 opening and 704 closing braces;
- `common/history/military_formations/05_military_formations_india.txt`: 141 opening and 141 closing braces;
- `common/character_templates/country_marath.txt`: 2 opening and 2 closing braces;
- local vanilla 1.13 contains `ship_type_frigate`, `building_naval_administration`, `pm_simple_sailor_recruitment`, and `region_south_india`;
- the MARATH block contains one unchanged land HQ at `region_north_india`, one fleet HQ at `region_south_india`, and a ship count of 2;
- the new MARATH block contains none of `combat_unit_type_frigate`, `combat_unit_type_man_o_war`, `building_naval_base`, or `state_region = s:STATE_BOMBAY`;
- `MARATH_anandrao_dhulap` is defined once and instantiated once;
- `is_admiral = yes`, `age = 40`, `culture = cu:marathi`, and `home_region = STATE_BOMBAY` are present exactly as intended;
- `konkan_flotilla` and `anandrao_dhulap_admiral` are each saved once, and exactly one `transfer_to_formation = scope:konkan_flotilla` attaches the admiral;
- no other Anandrao/Dhulap character or conflicting name key was found in the fork or local vanilla localization;
- no negative age, future birth date, or pre-start death date was introduced;
- `Konkan_Flotilla`, `Anandrao`, and `Dhulap` occur exactly once in each intended language localization file;
- both new localization files begin with UTF-8 BOM bytes `EF BB BF`;
- MARATH's country history contains exactly one `add_technology_researched = admiralty`; its diff contains no other technology or unrelated change;
- the full diff was inspected and `git diff --check` returned no error;
- `git diff --cached --name-only` remained empty.

## 11. Historical runtime test plan

This was the historical test plan used before final acceptance:

1. start the scenario on 1 January 1776 as or while observing MARATH;
2. confirm `Konkan Flotilla` / `Flottille du Konkan` loads without formation errors;
3. confirm its HQ is South India and it contains exactly two frigate-type game ships;
4. confirm the land formation remains assigned to North India;
5. inspect the MARATH `STATE_BOMBAY` naval administration: level 1, correct PM, hiring, and a 1,000-sailor ceiling;
6. confirm the inherited building survives despite MARATH lacking `admiralty`, while construction/expansion remains technology-gated as expected;
7. confirm exactly one Anandrao Dhulap exists, has the admiral role, and is attached to `Konkan Flotilla`;
8. confirm his displayed age is coherent at the 1776 start and that culture, religion, and generated portrait resolve without anachronism;
9. let several days pass and inspect character, commander, formation, employment, and recruitment errors attributable to the new setup.

### Final runtime acceptance

The historical plan above first produced the CLEANUP-1C FAIL without Admiralty. The final user-run new campaign with Admiralty passed:

- true Naval Administration present at level 1;
- Naval Logistics Center also present as a separate auto-placed building;
- Konkan Flotilla at South India HQ with exactly two frigates/Cruisers;
- Anandrao Dhulap still assigned as admiral;
- sailor count `1,000 / 1,000`;
- MARATH land HQ still North India.

## 12. Protected-state verification

Final verification results:

- `stash@{0}` is still `On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` and still resolves to `518df704fa14599c0f254fae13859210663dd976`;
- branch and HEAD remain `cleanup-post-release` and `1e374f2f40252d229bc249600e3cbbe26085122d`;
- `bject` is absent;
- BIC still contains `activate_law = law_type:law_frontier_colonization`; its file does not contain `law_colonial_exploitation`;
- no file is staged;
- the tracked diff contains only the three intended gameplay history files: MARATH building, country, and formation history; the new MARATH template, localizations, design invariant document, and CLEANUP reports remain intended untracked additions;
- the seven protected technology files remain untracked and unstaged, with their baseline SHA-256 values unchanged:

| PROTECTED FILE | SHA-256 |
|---|---|
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410` |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` |

## 13. Final verdict

CLEANUP-1B supports a small but real MARATH starting naval presence. Two frigate objects are the least overconfident translation of the documented surviving Konkan force into Victoria 3's 500-sailor unit scale. One inherited naval-administration level is both mechanically required and historically grounded. The permanent commander-completeness rule requires the historically attested Anandrao Dhulap to command the formation. A ship of the line remains unjustified.

The final runtime A/B result makes one temporary exception necessary: current vanilla 1.13 requires MARATH to have `admiralty` for the scripted Naval Administration to materialize and crew the fleet. This grant is accepted for CLEANUP-1 finalization only and must be replaced by the future progressive naval-technology design.
