# Issue #37 - Russian Northern Norway impassable flags

Date: 2026-11-07. Parent #24; coordination #19; runtime baseline #20.
Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Severity: **major / P1**.

## Identified defect and scope

The maintainer clarified the location as a northern Scandinavian state shared between Norway and Russia.
The actual 1776 setup identifies **STATE_NORTHERN_NORWAY**: 129 provinces belong to `c:DENNOR` and four to
`c:RUS`. Kola and Oulu are not shared this way in the local setup. The four Russian provinces are
`x2495FE`, `xFEC50D`, `x7005BB` and `x6480A4`.

Before correction, **every Russian province in this split state was explicitly impassable**. The mod's
`map_data/state_regions/00_west_europe.txt:177` retained the vanilla 37-province impassable list, including
all four. The existing `common/history/states/00_states.txt:4774` block assigns the four provinces to Russia;
`common/history/pops/00_west_europe.txt:102` also initializes the Russian state part with 7,028 people
(5,936 Norwegian, 834 Sami, 258 Finnish). These are existing authored mod values, not new historical claims.

The installed canonical contract explicitly defines `impassable` as provinces within the region that are
impassable (`map_data/state_regions/state_regions.md:44`). Canonical 1.15
`map_data/state_regions/00_west_europe.txt:185` includes the same four IDs. Retaining these flags is
inconsistent with the mod's separately owned and populated Russian state part. This is a **confirmed
configuration defect and a strong match to the reported location**, not proof that 1.15 newly introduced
the flags. The observed screen and engine movement behavior still require verification after the fix.

## Targeted correction

Remove **only these four IDs** from this state's `impassable` list, on its existing line 177. The list
shrinks from 37 to 33; Russian passable provinces increase from 0 to 4. The Danish-Norwegian part retains
129 provinces, 33 impassable and 96 passable. No ownership, population, border, province raster, terrain,
hub/locator, strategic-region, resource capacity or historical country setup is changed.

This is a one-line gameplay edit. The existing local map file has substantial independent modifications;
it was patched in place against its fresh source hash, with an exact source backup kept outside the mod.
The remote branch receives the same four-ID removal applied to its own source, **not a replacement with
the dirty local file**. No checkout/reset/local Git metadata write or main merge is performed.

The old flags and byte-equivalent non-target content are checked by
`tools/compatibility/issue37_northern_norway_audit.py`. The tool only reads files and outputs JSON.
The source backup is required as `--before-file`; it must be the actual pre-edit file, not a newly
downloaded remote version of the dirty local map.

## Static verification on the installed local correction

Command:

```text
python tools/compatibility/issue37_northern_norway_audit.py --mod-root MOD --vanilla-root "C:/Games/Victoria 3/game" --before-file BEFORE/00_west_europe_before.txt
```

Results: **PASS_STATIC_ONLY**, zero audit errors.

| Province | Existing owner | Raster pixels | Before | After | Passable pixel-edge path to Kola |
| --- | --- | ---: | --- | --- | --- |
| `x2495FE` | RUS | 170 | Impassable | Passable | Yes |
| `x6480A4` | RUS | 275 | Impassable | Passable | Yes |
| `x7005BB` | RUS | 251 | Impassable | Passable | Yes |
| `xFEC50D` | RUS | 142 | Impassable | Passable | Yes |

- The entire local gameplay file equals the exact pre-edit bytes after only the four authorized token
  removals. Line endings and all unrelated historical modifications are retained.
- All 133 state provinces exist in the raster and have unique, complete DENNOR/RUS ownership. Earlier
  effective-map inspection found no duplicate province assignments or state IDs in these candidate regions.
- The four target provinces cover **838 pixels**, identical to canonical vanilla at those coordinates.
  No raster edit is necessary. A bounded four-neighbor pixel graph connects each unblocked province to
  a passable Kola province. This is a topological check, **not engine pathfinding or military access**.
- All four retain the existing `tundra` terrain. Kola, Oulu, Norrland and Northern Norway have identical
  mod/vanilla province pixels in the inspected state footprints; absent/renamed target RGBs are excluded.
- Northern Norway has exactly one effective strategic-region assignment: `region_northern_europe`.
- **1,089 protected local files** were hashed before and after, including other map data, histories,
  strategic regions, hub locators, ship types and journals. No protected file changed. Every pre-existing
  Git status entry and the local branch/HEAD were preserved. The accepted #36 and new #27 changes remain.

Local source SHA-256: `419975df05becc5b1949fcee318d31396669cc359dac073fed99c663b31b8787`.
Installed SHA-256: `16fb8e542d78814c26541397932bf7a2d253b452232570a87986ed2330fa93c3`.
See the adjacent `V1_15_ISSUE37_NORTHERN_NORWAY_VALIDATION_2026_11_07.json` for measured coordinates,
preservation checks and limits. Private backups/manifests and unrelated dirty-file contents are not published.

## Distinguishing other errors

All available rotated `error*.log` files were searched for the target state and province IDs. They contain
no direct Northern Norway/four-province diagnostic. The existing Kola port-anchor mismatch in
`error.3.log:3267` concerns `xF2B2C8` versus `xD98ED6`, a **different state and different provinces**;
it is not evidence that the four Northern Norway provinces should remain impassable and is not changed here.
Other world strategic-region and journal errors remain separate compatibility debt.

## Required runtime acceptance

The correction is already installed in the regular local mod used by playset **hhhh**. No new mod copy,
download or playset switch is needed. Fully restart the game and start a fresh 1776 Sandbox Russia game:

1. Inspect the Russian part of Northern Norway at the Kola border, recording its tooltip and map mode.
   Confirm the four provinces are selectable/represented as traversable rather than wasteland.
2. Check Russian land connectivity/movement toward Kola where access rules permit; distinguish a lack
   of military access or an absent valid army destination from an impassable-terrain marker.
3. Check nearby Danish-Norwegian territory and the 33 deliberately impassable provinces remain as intended.
4. Advance the simulation and save/reload; preserve fresh rotated logs and record any remaining visible
   or movement symptom with a screenshot/location. Reproduce in clean vanilla if an unrelated symptom remains.

No new game run, engine pathfinding test, screenshot acceptance or full 1.15 compatibility is claimed.
Issue #37 stays open until visual/gameplay acceptance and applicable review/integration. Project editing
tools are unavailable in this session; work and the blocker are documented in the issue, without claiming
a dashboard field change. The historical map overhaul and Yekatarina's law audit remain untouched.
