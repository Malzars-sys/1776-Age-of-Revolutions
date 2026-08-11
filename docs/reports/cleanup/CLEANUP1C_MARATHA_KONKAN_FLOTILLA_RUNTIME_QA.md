# CLEANUP-1C — Maratha Konkan Flotilla Runtime QA

## 1. Baseline

- Repository: `1776_Age_of_Revolutions_fork`
- Branch: `cleanup-post-release`
- HEAD: `1e374f2f40252d229bc249600e3cbbe26085122d`
- CLEANUP-1B and CLEANUP-1B.1 were present as unstaged/untracked working-tree changes before launch.
- `git diff --check` passed before launch.
- No file was staged and no Git mutation was performed.
- Protected `stash@{0}` resolved to `518df704fa14599c0f254fae13859210663dd976` before launch.

## 2. Runtime environment

- Game: Victoria 3, Matcha `1.13.0` / The Great Wave, modified checksum `bc7e`.
- Launch: one direct `victoria3.exe -gdpr-compliant -debug_mode` process; no second game launch occurred.
- Session start: 2026-08-10 20:16:48 Europe/Paris.
- Session end: 2026-08-10 20:54:15 Europe/Paris.
- The active VFS mount was confirmed in `debug.log`: `Mounted Data: C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.
- Scenario start: 1 January 1776.
- Inspected country: MARATH / Maratha Confederacy.
- MARATH loaded successfully and was playable.

## 3. Konkan Flotilla

Observed at scenario start and again at the end of the session:

| Check | Runtime observation | Result |
|---|---|---|
| Formation name | `Konkan Flotilla` | PASS |
| Formation type | Fleet | PASS |
| HQ | `South India HQ` | PASS |
| Total ships | 2 | PASS |
| Frigate-class ships | 2, displayed by the 1.13 UI in the `Cruisers` category | PASS |
| Capital ships / ships of the line | 0 | PASS |
| Torpedo craft | 0 | PASS |
| Duplicate MARATH fleets | None; the outliner showed one MARATH navy formation | PASS |
| Ghost or empty MARATH fleet | None; the only fleet retained its two ships | PASS |

The formation remained present with the same two units throughout the observation period. Its organization remained at 100%. The formation's sailor display was `0 / 1.00K` at the start and remained `0 / 1.00K` at the end.

## 4. Anandrao Dhulap

The character panel and fleet panel established all of the following:

- name: Anandrao Dhulap;
- country: Maratha Confederacy;
- rank: Commodore;
- role: Admiral;
- assigned formation: Konkan Flotilla;
- assignment UI: `Unassign Anandrao Dhulap` / `Already assigned`;
- displayed age at scenario start: 40;
- culture: Marathi;
- religion: Hindu;
- home state: Maharashtra, the runtime name for the relevant Bombay-region state;
- generated portrait: coherent South Asian male naval portrait;
- duplicate character: none observed.

The age of 40 is the documented technical approximation used by the implementation. It is not treated as a historically certain birth-date calculation.

The MARATH fleet therefore satisfies the Commander Completeness Rule at runtime:

`Konkan Flotilla -> Anandrao Dhulap`

## 5. Naval administration

The scripted `building_naval_administration` loaded successfully. In the 1.13 English UI it appeared as **Naval Logistics Center**, a government building in **Maharashtra**, corresponding to MARATH's Bombay-region state.

Observed runtime state:

| Check | Runtime observation | Result |
|---|---|---|
| Building present | Yes | PASS |
| Level | 1 | PASS |
| Configured history PM | `pm_simple_sailor_recruitment` | PRESENT |
| Building active | Yes | PASS |
| Employment state | Fully employed | PASS |
| Total displayed employees | `0.10K` / 100 | OBSERVED |
| Officers | 10 | OBSERVED |
| Bureaucrats | 30 | OBSERVED |
| Laborers | 60 | OBSERVED |
| Sailor capacity | `1.00K` / 1,000 | PASS |
| Actual sailors | 0 at start; 0 at end | FAIL |
| Supplied-fleet link | Konkan Flotilla listed by the building | PASS |
| Fleet building/crew table | Empty | FAIL |

The source activation of `pm_simple_sailor_recruitment` was retained, and the runtime `1.00K` ceiling demonstrates that its capacity effect resolved. The 1.13 workforce panel did not display sailors as building employees; it displayed 10 officers, 30 bureaucrats, and 60 laborers instead. More importantly, the country/fleet sailor counter never rose above zero even though the building was fully employed.

The inherited building therefore survives, remains active, pays military wages, reaches full displayed employment, links to Konkan Flotilla, and supplies a nominal capacity of 1,000. It did **not** demonstrate actual sailor recruitment. On the criteria defined for CLEANUP-1C, the inherited naval administration is not fully functional.

## 6. Technology-gating observation

MARATH did not have `admiralty` researched. The military technology tree showed:

- `Admiralty` available but not researched;
- cost displayed as 7.50K innovation / approximately 35 months;
- prerequisite `Navigation` satisfied;
- explicit unlock: `Naval Administration (Building)`.

This confirms both sides of the temporary inherited-building arrangement:

1. the pre-existing level survives without `admiralty`;
2. construction or expansion remains gated behind `admiralty`.

No advanced European naval technology was granted artificially. No UI script error appeared when inspecting the inherited building. The technology gate is accepted as the documented temporary limitation, but it does not explain away the failed sailor recruitment.

## 7. MARATH land formation regression check

The existing `Oudh Royal Army` remained a land formation with 40 units. Its formation panel explicitly displayed:

`Stationed at North India HQ`

The map also placed the formation at `North India HQ`. No naval change moved the land formation to South India.

`MARATH_LAND_HQ_PRESERVED = YES`

## 8. Time-passage observations

The intended observation window was approximately 7–14 days. The first reliable pause command was accepted on 19 February 1776, so the actual observation covered 49 days from the 1 January start. This exceeded the ideal short window but remained within the same single launch and did not require a reload.

Across that period:

- Konkan Flotilla remained present;
- both frigate-class units remained present;
- Anandrao Dhulap remained assigned;
- fleet organization remained at 100%;
- the Naval Logistics Center remained level 1 and fully employed;
- the nominal sailor capacity remained 1,000;
- actual sailors remained 0;
- the fleet's Buildings/Crew association table remained empty;
- no commander or formation disappearance occurred.

The longer-than-planned observation strengthens, rather than weakens, the negative recruitment finding: the zero value was not merely a first-day hiring delay.

## 9. Logs

All session `debug*.log`, `game*.log`, and `error*.log` files written from the 20:16:48 launch through closure were inspected for:

- `MARATH`;
- `Konkan_Flotilla` / `Konkan Flotilla`;
- `Anandrao` / `Dhulap`;
- `ship_type_frigate`;
- `region_south_india`;
- `building_naval_administration`;
- `pm_simple_sailor_recruitment`;
- related character, military-formation, and building errors.

Results:

- attributable script/runtime errors: **0**;
- one attributable non-fatal debug warning: `common/character_templates/country_marath.txt` should be UTF-8 BOM encoded, followed by `will try to use it anyways`;
- one `tag MARATH` debug-console line came from the manual QA console attempt and is not an implementation error;
- no error-log reference named the MARATH building history, military formation history, Anandrao/Dhulap, the frigate type, South India HQ, or the sailor-recruitment PM.

The session's rotated error logs contained 13,504 `Script system error` entries, but their locations were unrelated to CLEANUP-1B. The dominant pre-existing source was `common/journal_entries/01_natural_borders_of_france.txt` (invalid `sr` comparisons), followed by unrelated American journal-entry, interest-group, colonial-administration, AI-strategy, and event files. These are not counted against CLEANUP-1C.

The UTF-8 BOM warning is not counted as an attributable runtime **error**, but it should be cleaned before the eventual commit.

## 10. Protected-state verification

Post-closure verification found:

- branch still `cleanup-post-release`;
- HEAD still `1e374f2f40252d229bc249600e3cbbe26085122d`;
- no staged files;
- `git diff --check` passed;
- no new stash;
- `stash@{0}` still resolved to `518df704fa14599c0f254fae13859210663dd976`;
- `bject` remained absent;
- BIC retained `activate_law = law_type:law_frontier_colonization`;
- BIC contained no `law_colonial_exploitation`;
- no gameplay file was modified by CLEANUP-1C;
- this report is the only new CLEANUP-1C repository file.

The seven protected untracked technology-research files remained unstaged and byte-identical:

| File | SHA-256 |
|---|---|
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410` |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` |

## 11. Post-CLEANUP-1C diagnosis / resolution

This section records later evidence and does not rewrite the historical CLEANUP-1C result. CLEANUP-1C remains a FAIL because its no-Admiralty campaign had `0 / 1,000` sailors after 49 days and no functional Naval Administration crew source.

Subsequent vanilla-file tracing established that the inspected **Naval Logistics Center** was a distinct auto-placed logistics building, not the scripted sailor-recruitment **Naval Administration**. The MARATH history block already used the correct internal ID, `building_naval_administration`, with the correct PM, `pm_simple_sailor_recruitment`.

The user then performed a controlled runtime A/B resolution:

- **without Admiralty:** true Naval Administration absent/non-functional; crew `0 / 1,000`;
- **with exactly one `add_technology_researched = admiralty`:** a new 1 January 1776 campaign showed Admiralty researched, the true Naval Administration separately present at level 1, and Konkan Flotilla fully crewed at `1,000 / 1,000`.

This confirms that the current vanilla 1.13 setup does not let this MARATH history building bypass its technology unlock. Admiralty is therefore granted temporarily for CLEANUP-1 acceptance. The future technology overhaul must replace that compromise under the `Naval Progression Access Rule`.

## 12. Historical final verdict

The core formation reconstruction passed runtime validation: MARATH loads, Konkan Flotilla contains exactly two frigate-class units at South India HQ, Anandrao Dhulap is a coherent 40-year-old admiral assigned to the fleet, the land army remains at North India HQ, and the inherited level-1 naval administration survives without granting `admiralty`.

CLEANUP-1C nevertheless fails as a final acceptance gate because the fully employed inherited building provides a nominal 1,000-sailor ceiling but recruits zero actual sailors, leaving the fleet's building/crew table empty after 49 days. The non-fatal UTF-8 BOM warning is a second cleanup item. No fix was attempted during this runtime-only phase.

```text
MARATH_RUNTIME_LOAD = PASS
KONKAN_FLOTILLA_RUNTIME = PASS
KONKAN_FRIGATE_COUNT = 2
ANANDRAO_DHULAP_RUNTIME = PASS
ANANDRAO_DHULAP_COMMANDS_KONKAN = YES
ANANDRAO_DISPLAYED_AGE = 40
NAVAL_ADMIN_RUNTIME = FAIL
NAVAL_ADMIN_SAILOR_CAPACITY = 1000
MARATH_HAS_ADMIRALTY = NO
INHERITED_NAVAL_ADMIN_FUNCTIONAL = NO
NAVAL_ADMIN_EXPANSION_TECH_GATED = YES
MARATH_LAND_HQ_PRESERVED = YES
ATTRIBUTABLE_RUNTIME_ERRORS = 0
COMMANDER_COMPLETENESS_RULE_RUNTIME = PASS
STASH_INTACT = YES
CLEANUP1C_FINAL_VERDICT = FAIL
SAFE_TO_COMMIT_CLEANUP1B = NO
```
