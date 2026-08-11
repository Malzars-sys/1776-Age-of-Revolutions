# CLEANUP-1D — MARATH Naval Administration Correction

## 1. Runtime failure from CLEANUP-1C

The user runtime found `Konkan Flotilla` with two frigates and Anandrao Dhulap intact, but crew remained `0 / 1,000` after 49 days and the fleet Building/Crew table was empty. The inspected level-one state building was displayed as **Naval Logistics Center**, whereas Britain's working crew building was displayed as **Naval Administration**.

Codex did not launch Victoria 3. The runtime observations above are user evidence.

## 2. Wrong building identified

Vanilla French localization maps `building_naval_logistics_center` to **Centre logistique naval**. Its definition uses `bg_naval_logistics_center`, is non-buildable, non-expandable, and non-downsizeable, and uses `pm_basic_naval_logistics_center`.

That PM employs 60 laborers, 30 bureaucrats, and 10 officers per level. It has no `country_sailors_max_add`. The building lacks `recruits_sailors = yes`. Its building group has `auto_place_buildings = yes`, so its runtime presence is an automatic logistics consequence and not evidence that the MARATH history block requested it.

## 3. Correct vanilla naval administration

The trace starts from Britain's real Home Counties building in vanilla 1.13:

```text
common/history/buildings/00_west_europe.txt
building = "building_naval_administration"
levels = 20
activate_production_methods = { "pm_simple_sailor_recruitment" }
```

Vanilla French localization maps `building_naval_administration` to **Administration navale**. Its building definition uses `bg_naval_administration`, declares `recruits_sailors = yes` and `naval = yes`, and contains only `pmg_base_building_naval_administration`. That PM group contains only `pm_simple_sailor_recruitment`.

```text
UI_NAME = Administration navale
INTERNAL_BUILDING_ID = building_naval_administration

UI_NAME = Centre logistique naval
INTERNAL_BUILDING_ID = building_naval_logistics_center
```

## 4. Mechanical difference

| Field | Naval Logistics Center | Naval Administration |
|---|---|---|
| INTERNAL_BUILDING_ID | `building_naval_logistics_center` | `building_naval_administration` |
| BUILDING_GROUP | `bg_naval_logistics_center` | `bg_naval_administration` |
| EMPLOYMENT_PER_LEVEL | 100: 60 laborers + 30 bureaucrats + 10 officers | 1,000: 900 soldiers + 100 officers |
| RECRUITS_SAILORS | No | Yes |
| SAILORS_MAX_PER_LEVEL | 0 | 1,000 at full employment |
| SHIP_ASSIGNMENT_SLOTS_PER_LEVEL | 0 | 10 |
| PRODUCTION_METHOD | `pm_basic_naval_logistics_center` | `pm_simple_sailor_recruitment` |
| ROLE | Auto-placed fleet supply/logistics hub | Sailor recruitment and ship-crew assignment source |

The assignment count follows directly from the vanilla defines: `SAILORS_PER_BUILDING_LEVEL = 1000` and `SAILORS_PER_ASSIGNMENT_SLOT = 100`, hence ten assignment slots per fully supported level. The two MARATH frigates require `2 × 500 = 1,000` sailors, or all ten slots.

## 5. Root cause

```text
WRONG_BUILDING_ID = building_naval_logistics_center
CORRECT_BUILDING_ID = building_naval_administration
ROOT_CAUSE = MARATH lacked the admiralty unlock required by current vanilla 1.13 to materialize/functionally activate building_naval_administration; CLEANUP-1C separately inspected the auto-placed logistics center.
ROOT_CAUSE_CONFIDENCE = HIGH
```

The source audit also establishes an important boundary: the current CLEANUP-1B diff never requests `building_naval_logistics_center`. It already requests the correct `building_naval_administration`. Therefore there is no wrong history ID to replace in `10_india.txt`, and an ID-only rewrite would be a no-op. The runtime absence of a contributing Naval Administration is not repaired merely by renaming the auto-placed logistics building.

There are consequently two distinct findings, now both confirmed by the final runtime A/B test:

1. **Confirmed at HIGH confidence:** the building inspected in CLEANUP-1C was the wrong runtime object for sailor recruitment.
2. **Confirmed root cause:** MARATH's tier-5 starting package grants `navigation` but not `admiralty`, while the building declares `admiralty` as its unlock. Without Admiralty the true building did not materialize/function; after the grant it appeared and supplied full crew.

The correct history building ID alone therefore does not bypass the current vanilla 1.13 technology gate.

## 6. Correction implemented

The MARATH history block is preserved in its already-correct vanilla form:

```text
create_building = {
	building = "building_naval_administration"
	add_ownership = {
		country = {
			country = "c:MARATH"
			levels = 1
		}
	}
	reserves = 1
	activate_production_methods = { "pm_simple_sailor_recruitment" }
}
```

The requested correct building and PM were already present before CLEANUP-1D, so no building-ID rewrite was required. The final user runtime A/B test then justified one additional country-history line, `add_technology_researched = admiralty`. No fleet, ship, admiral, HQ, PM, building level, or technology-tree definition was changed.

## 7. Production method

`pm_simple_sailor_recruitment` is not a PM of the wrong building. It is the sole vanilla PM in the real Naval Administration PM group and is used by the Home Counties control.

```text
CORRECT_NAVAL_ADMIN_PM = pm_simple_sailor_recruitment
SAILOR_SUPPORT_PER_LEVEL = 1000 at full employment
ASSIGNMENT_SLOTS_PER_LEVEL = 10
```

No advanced European naval PM exists in that PM group or was granted to MARATH.

## 8. Admiralty / technology status

The vanilla building definition lists `admiralty` as its unlock technology. MARATH's `effect_starting_technology_tier_5_tech` grants `navigation` but not `admiralty`. This is the exact technology dilemma already governed by `docs/design/1776_PROJECT_INVARIANTS.md` under **Naval Progression Access Rule**:

- MARATH must ultimately be able to maintain sailors and limited coastal capability without being raised to British/French/Dutch naval technology;
- the exact progressive technologies and unlocks belong to the future technology overhaul;
- an inherited MARATH naval administration without `admiralty` is the explicitly accepted temporary design state.

CLEANUP-1D does not pre-empt that overhaul. The final user-run A/B test nevertheless proved that the current setup requires the building unlock. MARATH therefore receives exactly one country-history grant, `add_technology_researched = admiralty`, as a temporary CLEANUP-1 compromise. No technology definition, tier effect, PM, or tree file is modified.

```text
MARATH_ADMIRALTY_GRANTED = YES_TEMPORARY
TECH_TREE_MODIFIED = NO
```

## 9. UTF-8 BOM correction

`common/character_templates/country_marath.txt` currently begins with `EF BB BF`. Its logical Anandrao Dhulap definition was not changed during CLEANUP-1D.

## 10. Static validation

Static validation results:

- `building_naval_logistics_center` is absent from `common/history/buildings/10_india.txt`;
- MARATH requests `building_naval_administration`, country ownership level 1, and `pm_simple_sailor_recruitment`;
- both building IDs, both building groups, and both PM IDs resolve in the local vanilla 1.13 tree;
- brace counts pass: `10_india.txt` 704/704, formations 141/141, character template 2/2;
- `Konkan_Flotilla` occurs once, is a South India fleet, and retains exactly `count = 2` frigates;
- the Anandrao template creation and transfer each occur once; age 40, Marathi culture, and admiral role remain present;
- the MARATH land army remains at North India HQ;
- exactly one Admiralty grant exists in MARATH country history; its file diff contains no other added technology or unrelated edit;
- the character template prefix is `EF BB BF`;
- `git diff --check` passes and the Git index is empty;
- BIC retains `law_frontier_colonization`; `bject` is absent;
- all seven protected research-file SHA-256 values are unchanged and the files remain untracked/unstaged;
- `stash@{0}` still resolves to `518df704fa14599c0f254fae13859210663dd976`.

`V13_STATIC_VALIDATION = PASS`. The user runtime A/B test has now settled the engine behavior that static validation could not prove.

## 11. Historical user runtime checklist

Use one new MARATH campaign on 1 January 1776:

1. Search separately for **Administration navale** and **Centre logistique naval**; do not infer one from the other.
2. If **Administration navale** exists, confirm level 1, `pm_simple_sailor_recruitment`, about 1,000 maximum sailors, visible assignments, and actual sailors above zero after recruitment.
3. If **Administration navale** is absent, record that exact result and the Admiralty lock/tooltip; this selects the technology-gate branch of the diagnosis.
4. Confirm the Logistics Center is not treated as the crew source, then verify two frigates, Anandrao Dhulap, South India fleet HQ, North India land HQ, and the historical no-Admiralty state of that diagnostic run.
5. Preserve the session logs and report any MARATH/naval errors.

The decisive values are:

```text
NAVAL_ADMIN_SHIP_ASSIGNMENTS_VISIBLE = YES
FLEET_BUILDING_CREW_TABLE_NONEMPTY = YES
ACTUAL_SAILORS_GT_ZERO = YES
```

### Final user runtime result

The user started a new MARATH campaign on 1 January 1776 after adding the single Admiralty grant. Admiralty was researched; the true Naval Administration appeared separately from the Naval Logistics Center at level 1; Konkan Flotilla remained at South India HQ with exactly two frigates/Cruisers and Anandrao Dhulap assigned; crew reached `1,000 / 1,000`; and the MARATH land HQ remained North India.

```text
NAVAL_ADMIN_SHIP_ASSIGNMENTS_VISIBLE = YES
FLEET_BUILDING_CREW_TABLE_NONEMPTY = YES
ACTUAL_SAILORS_GT_ZERO = YES
ACTUAL_SAILORS = 1000/1000
```

## 12. Protected-state verification

`Konkan_Flotilla` remains a fleet at `sr:region_south_india` with exactly two `ship_type:ship_type_frigate` objects. Anandrao Dhulap remains a single Marathi admiral, age 40, created once and transferred once to that fleet. MARATH's land formation remains at `sr:region_north_india`.

Exactly one temporary Admiralty grant is present in MARATH country history. No technology-tree definition, legacy naval syntax, other-country gameplay, Git staging operation, or Codex Victoria 3 launch was performed. BIC's `law_frontier_colonization`, the protected research files, `bject` absence, and the protected stash are checked separately in final validation.

## 13. Verdict

The two internal IDs and their mechanics are confirmed at HIGH confidence. The observed Logistics Center is the wrong building to inspect for crew, but it was not created by the MARATH history block: that block already names the true Naval Administration and its sole basic PM. Documentation is corrected without inventing a false source replacement.

The final A/B runtime removes the remaining uncertainty. Without Admiralty the true Administration was absent/non-functional and crew remained `0 / 1,000`; with Admiralty the true level-one Administration appeared and crew reached `1,000 / 1,000`. The current vanilla 1.13 setup therefore requires the unlock.

The temporary country-history grant closes CLEANUP-1 runtime acceptance but does not replace the future `Naval Progression Access Rule` solution.
