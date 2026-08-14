# CLEANUP-2D-6K — Maratha Konkan historical admiral coverage gap

## 1. Status

`RESEARCH_COMPLETE`

Reference date: `1776-01-01`.

This phase is research-only. It changes no gameplay file, formation, template, localization, rank, portrait, or DNA.

```text
FORMATIONS_AUDITED = 1
CURRENT_FLEETS_RESEARCHED = 1
FINAL_DECISIONS = 1
MISSING_DECISIONS = 0
```

## 2. Why this gap exists

The regional 2D-6G packet concluded that MARATH had no current fleet and consequently did not audit either `Konkan_Flotilla` or `MARATH_anandrao_dhulap`. The later 2D-6J direct parse of all eight current formation files corrected the canonical scope: NAV1776-037 is an active two-frigate fleet with one attached admiral. This packet overrides only that missing 2D-6G coverage row; it does not alter the old 2D-6G CSV.

## 3. Current repo formation

Direct branch inspection confirms:

- record: `NAV1776-037`;
- country: `MARATH`;
- file: `common/history/military_formations/05_military_formations_india.txt`;
- formation: `Konkan_Flotilla`;
- type: fleet;
- HQ: `sr:region_south_india`;
- standing force: `2 x ship_type_frigate`;
- saved formation scope: `konkan_flotilla`;
- character template: `MARATH_anandrao_dhulap`;
- saved character scope: `anandrao_dhulap_admiral`;
- transfer: the character is transferred to `konkan_flotilla`.

The two frigates are Victoria 3 unit equivalents, not a claim that the historical Peshwa establishment possessed exactly two European frigates.

## 4. Current `MARATH_anandrao_dhulap` audit

The sole template is `common/character_templates/country_marath.txt`.

| Field | Current encoding | Audit |
|---|---|---|
| role | `is_admiral = yes` | historically defensible |
| name | `Anandrao Dhulap` | correct normalized identity |
| historical | `yes` | correct |
| culture | `cu:marathi` | defensible V3 mapping |
| age | `40` | explicitly technical; no sourced birth year/date was found |
| home region | `STATE_BOMBAY` | acceptable broad Konkan mapping, not a sourced birthplace |
| religion | absent | preserve as unknown; do not invent |
| traits | empty | no issue |
| ideology / interest group | absent | no issue |
| `commander_rank` | absent | engine initial rank 1; naval limit 20 in vanilla 1.13.10 |
| DNA / portrait | absent | correct because no authenticated likeness was found |

Repo-wide searches across character templates, character history, DNA, events, military formations, localization, naval reports, and research files found no second Dhulap character, no DNA id, and no other gameplay use. English and French localization provide only the fleet and name strings. If implemented later, the existing person must be reused/reconstructed, never cloned.

## 5. Maratha naval command structure in 1776

The evidence does not support flattening every Maratha coastal force into one modern national navy.

After Tulaji Angre's defeat in 1756, the Peshwa established an independent `Subha Armar`. Its chief was styled `सुभेदार निसबत/निसवत सुभा आरमार` (`Subhedar Nisbat/Nisavat Subha Armar`); the consulted institutional article uses both Marathi spellings. Madhavrao appointed Anandrao Dhulap on 25 May 1763, and the institutional account places him formally in that office from 1764. Vijaydurg became this establishment's principal base.

Alongside it remained the Angre house's semi-autonomous Kolaba command. Raghoji/Raghuji Angre I succeeded Manaji in 1759 and ruled at Kolaba until 1793, paid tribute to the Peshwa, and owed military service. This was a real maritime power but not the same office or base as Dhulap's Peshwa-controlled Vijaydurg establishment.

`Konkan_Flotilla` is therefore acceptable only as a compact gameplay abstraction. Because it is owned by MARATH, based in the south-India strategic region, and inherited from the mod's Vijaydurg/Konkan reconstruction, the strongest mapping is the Peshwa naval subha under Dhulap. Classification: `HIGHER_NAVAL_COMMAND_ABSTRACTION`.

## 6. Candidate dossier — Anandrao Dhulap

- Canonical name: Anandrao Dhulap.
- Original name: `आनंदराव धुळप`.
- Romanization: `Ānandarāv Dhuḷap`.
- Useful variants: Anand Rao Dhulap, Anandráo Dhulap, Anandrao Rudrajirao Dhulap, and the More-family form.
- Family: the Marathi Vishwakosh describes the family's earlier surname as More and links it to the More house of Jawali; it later settled at Panhale/Dhavade port in the Konkan.
- Birth date and place: unknown. No false year, month, or day is assigned.
- Death: exact date unknown; the institutional account says he died at Vijaydurg.
- Title at cutoff: `सुभेदार निसबत/निसवत सुभा आरमार`.
- Function: chief of the Peshwa's independent naval subha headquartered at Vijaydurg.
- Command start: appointed 25 May 1763; formally in title from 1764.
- Command end: exact date unknown; active span is conventionally given as 1764–1795.
- Cutoff activity: yes. A National Archives of India descriptive list identifies Anandrao Dhulap as the Peshwa's naval officer in April 1776 and separately records harassment by the Maratha navy in that same operational context.
- Command area: Vijaydurg and the Peshwa's south-Konkan/Arabian-Sea establishment.

The Marathi Vishwakosh also documents major naval activity under this establishment in 1772 and 1775, including subordinate operational commanders. These events establish that Dhulap held a genuine higher naval command rather than merely a fort, court, or honorific office. Identity confidence is `HIGH`; cutoff eligibility is `HIGH`.

## 7. Candidate dossier — Raghoji/Raghuji Angre I

Raghoji Angre I is a genuine and eligible 1776 maritime ruler. The Kolaba Gazetteer states that he succeeded Manaji in 1759, lived and ruled until 1793, resided at Kolaba, paid tribute to the Peshwa, and held his lands on military tenure. A 1771 visitor found him at the island fort of Kolaba.

His weakness is not identity but formation mapping. He headed the semi-autonomous Kolaba/Angre polity, whereas NAV1776-037 is the mod's surviving Peshwa/Vijaydurg-oriented Konkan abstraction and already uses the historically correct Peshwa naval-subha commander. Raghoji should be reserved for a distinct future Angre/Kolaba formation if that structure is ever modeled.

- identity confidence: `HIGH`;
- active on 1776-01-01: `YES`;
- classification if separately represented: `HEREDITARY_NAVAL_COMMAND`;
- mapping to current `Konkan_Flotilla`: `MEDIUM_LOW`;
- outcome: rejected as the final mapping, not rejected as a historical person.

## 8. Other candidates examined

- Janrao/Janoji Dhulap: documented as an operational leader in the 1772 action against the Portuguese squadron, but subordinate to Anandrao's higher establishment command. Not a better sole starting admiral.
- Krishnaji Naik Jaitapurkar: likewise an operational commander in 1772, but no evidence found that he displaced Anandrao as chief at the cutoff.
- Damaji Naik Kuveskar: a substantive naval commander associated with the loss of `Samsherjang` on 1 February 1775; the account records his death in that action, making him ineligible on 1776-01-01.
- Gangadhar Bhanu: associated with the Vijaydurg district administration in 1775, but this does not supersede Dhulap's documented naval office and is not evidence of fleet command.

No third candidate is more directly compatible with the current single higher-command abstraction than Anandrao Dhulap.

## 9. Birth/death date conflicts

No reliable birth date or birth year was recovered. The current `age = 40` implies only an engine-facing approximation around 1735–1736 and must not be cited as historical evidence. Birth place is also unknown; `STATE_BOMBAY` is a home-region mapping, not proof of birthplace.

The appointment chronology needs two fields rather than forced harmonization: Madhavrao's appointment is dated 25 May 1763, while the formal title is placed in 1764. The recommended command-start representation is therefore `1764` with `YEAR` precision, with the 1763 appointment preserved in notes.

No exact death date was found. `1764–1795` is an attested active span, not a birth/death range. The only retained death-place statement is Vijaydurg.

## 10. Portrait/DNA/template audit

- authenticated contemporary portrait: none located;
- near-contemporary portrait: none authenticated;
- posthumous visual: no reliable portrait selected;
- modern reconstruction/statue: unsuitable for historical DNA;
- existing exact mod DNA: none;
- existing template: `MARATH_anandrao_dhulap`, biographically incomplete but identity-correct.

Portrait status is `NONE`. A later implementation must not construct exact historical DNA from a modern statue, web illustration, family-member portrait, or unattributed painting.

## 11. Final decision

`REBUILD_EXISTING_HISTORICAL_ADMIRAL`

Anandrao Dhulap is real, alive and naval-command active on 1776-01-01, held the correct Peshwa naval office, and commanded from the most compatible south-Konkan base. The current character is therefore correct in identity but biographically under-specified: the age is technical, the exact title and tenure are absent, and no rank is explicit. This is a future reconstruction decision, not an authorization to edit gameplay in 2D-6K.

The formation is an acceptable `HIGHER_NAVAL_COMMAND_ABSTRACTION`, not a literal two-frigate order of battle. Identity confidence is `HIGH`; formation-mapping confidence is `HIGH_WITH_EXPLICIT_ABSTRACTION`.

## 12. Rejected candidates

| Candidate | Result | Reason |
|---|---|---|
| Raghoji/Raghuji Angre I | reject for this formation | correct 1776 maritime ruler, wrong Kolaba/Angre command structure for the Peshwa/Vijaydurg abstraction |
| Janrao/Janoji Dhulap | reject as sole higher commander | documented subordinate operational command; Anandrao held the superior office |
| Krishnaji Naik Jaitapurkar | reject as sole higher commander | documented operational commander, not proven chief of the naval subha |
| Damaji Naik Kuveskar | ineligible | died in the 1775 `Samsherjang` action |
| Gangadhar Bhanu | reject role mismatch | district/fort administrative association does not establish command of the naval force |

## 13. Sources

1. Marathi Vishwakosh, [आनंदराव धुळप (Anandrao Dhulap)](https://marathivishwakosh.org/74035/): institutional title, 1763 appointment, formal 1764 tenure, family background, Vijaydurg base, operations, and unknown exact death date.
2. National Archives of India, [Descriptive List of Secret Department Records, vol. II](https://upload.wikimedia.org/wikipedia/commons/2/27/Descriptive_List_Of_Secret_Department_Records_Vol._2_%28IA_in.ernet.dli.2015.44172%29.pdf): April–May 1776 records naming Anandrao as the Peshwa's naval officer and reporting Maratha-navy operations.
3. Maharashtra Gazetteers, [Vijaydurg](https://gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/RATNAGIRI/places_Vijaydurg.html): Vijaydurg as the seat of Admiral Anandrao Dhulap.
4. B. K. Apte, [A History of the Maratha Navy and Merchantships](https://sahitya.marathi.gov.in/ebooks/A%20HISTORY%20OF%20THE%20MARATHA%20NAVY%20AND%20MERCHANTSHIPS.pdf): Peshwa fleet, Dhulap command, and operational context.
5. Maharashtra Gazetteers, [Kolaba — Maratha period](https://gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/KOLABA/his_maratha_period.html): Raghoji's Kolaba tenure, residence, tribute, and military-tenure relationship.
6. Maharashtra Gazetteers, [History of the Konkan, section 8](https://gazetteers.maharashtra.gov.in/cultural.maharashtra.gov.in/english/gazetteer/Gazetteer%20of%20Bombay%20Presidency/history_of_the_konkan/section_8.pdf): separate Kolaba Angre succession and command context.

## 14. Global fusion instructions

Use the A–I packets unchanged, this row as the NAV1776-037 coverage override, and 2D-6J as the canonical 41-fleet inventory. Do not modify the old 2D-6G CSV.

```text
GLOBAL_COVERAGE_TARGET:
NAV1776-037 = REBUILD_EXISTING_HISTORICAL_ADMIRAL
```

```text
READY_FOR_2D6_GLOBAL_RECONCILIATION = YES
```

## 15. Commander-rank capacity safeguard

Local Victoria 3 1.13.10 data, not memory, establishes the naval relationship:

| rank | naval `character_command_limit_add` |
|---|---:|
| `commander_rank_1` | 20 |
| `commander_rank_2` | 40 |
| `commander_rank_3` | 60 |
| `commander_rank_4` | 80 |
| `commander_rank_5` | 100 |
| `commander_rank_ruler` | 30 |

Sources inspected locally:

- `Victoria 3/game/common/commander_ranks/00_commander_ranks.txt`;
- `Victoria 3/game/common/defines/00_defines.txt` (`COMMANDER_START_RANK = 1`, `RULER_COMMANDER_START_RANK = 6`, and `MILITARY_FORMATION_COMMAND_LIMIT_NO_COMMANDER = 20`).

For NAV1776-037, an admiral created without explicit rank starts at rank 1 and deterministically commands 20 ships. No trait or temporary modifier is credited. Therefore `20 >= 2`, and the smallest sufficient final rank remains `commander_rank_1`. This finding does not modify the template in the research phase.

The companion 41-row audit applies the same rule to the full canonical inventory. No researched decision assigns multiple admirals to one starting formation, so no capacity sharing assumption is used. Only four sole-admiral formations exceed 20 ships: NAV1776-005 (22), NAV1776-011 (50), NAV1776-012 (28), and NAV1776-014 (25). Their smallest sufficient recommendations are respectively rank 2, rank 3, rank 2, and rank 2. Every other selected or procedural sole admiral remains at rank 1; rows intentionally retaining no fixed admiral use the deterministic vanilla formation fallback of 20.

```text
FLEETS = 41
FLEET_COMMAND_CAPACITY_ROWS = 41
FLEETS_WITH_INSUFFICIENT_ADMIRAL_CAPACITY = 0
LAND_GENERAL_RANKS_CHANGED_BY_2D6 = 0
GENERAL_COMMAND_CAPACITY_SUFFICIENT = 214
```
