# Historical journal groups - expanded local delivery

Date: 2026-11-07. Refs #27/#24, PR #34. Parent branch revision: `6d2d9f7684f1c5618b9c17ec6e558b44b6f7deab`.
Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. This is presentation grouping, not a broad outcome migration.

The maintainer expanded the Ottoman grouping request to two further categories and specified their art.
All three categories are installed directly in the regular local mod. **36 existing journal definitions**
now belong to these three illustrated groups. English/French group titles are supplied; existing entry
names, historical setups, activation conditions and conclusion effects are retained.

## Category mapping

### Ottoman Decline / Déclin ottoman - 11 entries

Reuse `je_group_1776_imperial_crises` with `themed = yes`. The two 1776 Ottoman journals already used this
key; their journal file needed no change. Add the eight Sick Man entries and Great Eastern Crisis.
The bazaar/mosque illustration is the existing native `je_group_illu_great_game.dds`.
See the companion Ottoman-only receipt for its exact mapping and preservation checks.

### Destiny of the Americas / Destin des Amériques - 11 entries

New group: `je_group_aor1776_american_destiny`, in `common/journal_entry_groups/1776_historical_arcs.txt`.

| Journal file | Explicit selected definitions |
| --- | --- |
| `06_usa_independence_mod.txt` | `je_usa_independence`, `je_usa_independence_fra` |
| `1776_usa_french_support.txt` | `je_aor1776_french_support` |
| `1776_usa_revolutionary_spirit.txt` | `je_aor1776_revolutionary_spirit` |
| `00_canada_australia.txt` | `je_canada_can`, `je_canada_gbr`; Australian definitions remain unchanged. |
| `06_spanish_new_world.txt` | `je_spanish_new_world_dummy`, `je_reconquista`, `je_hispanoamerica`, `je_spanish_american_independence` |
| `06_cuba.txt` | `je_cuba_independencia`; other definitions are retained. |

This covers the existing American revolutionary chain, Canadian formation views, Spanish-American
independence/reconquest chain and the existing Cuban independence entry. It does not move unrelated
metropolitan Spanish anarchism, Philippines, Australian or generic American territorial-expansion content.

### State and Revolution / État et révolution - 14 entries

New group: `je_group_aor1776_state_and_revolution`, in the same new category file.

| Journal file | Explicit selected definitions |
| --- | --- |
| `09_forest_of_bayonets.txt` | `je_forest_of_bayonets` |
| `00_peoples_springtime_je.txt` | `je_springtime_of_the_peoples` |
| `05_hungry_forties.txt` | `je_the_hungry_forties`, addressing the maintainer's earlier question about its separate potential placement. |
| `06_french_revolution_mod.txt` | `je_fr_rev_summon_estates`, the existing French revolutionary entry. |
| `07_poland_lithuania_mod.txt` | `je_plc_reform`, industry, trade, education, railways, farming, military and great-power reform entries. |
| `00_poland.txt` | `je_christ_of_nations`, `je_poland_lithuania`, the existing Polish restoration chain. |

The Forest of Bayonets file was previously inherited directly from the installed canonical game. The
new mod override copies that exact current file and changes only its one group field; its existing
explicit `context = none` stays unchanged. This override must be re-compared on future game updates.
No 1776 gates or effects are invented to adapt the underlying vanilla situation in this presentation task.

## Mixed contexts and inactive rows

Native `common/journal_entries/journal_entries.md:8-13` permits a journal's explicit context to override
the category default. Both new groups default to country context; global entries retain **none/global**.
The Springtime entry gains an explicit `context = none`, the Forest retains its original one, and the
Great Eastern Crisis has the same explicit override from the Ottoman step. No global crisis is cloned
into a per-country entry, and involved-country/observer predicates remain unchanged.

Native `gui/journal.gui:663,697` lists active and inactive entries inside each illustrated category.
The generic Potential section (`725-769`) is for ungrouped entries. Grey rows therefore remain previews,
not evidence that an 1840s crisis has already started in 1776. Existing date/technology/DLC conditions
are retained. Gründerzeit and unrelated international situations remain in their existing category.

## Artwork and reproducible exports

- Americas: the mod's existing Washington Crossing the Delaware frontend texture,
  `gfx/interface/illustrations/frontend/age_of_revolution_frontend_bg.dds`, is the unchanged source.
- State and Revolution: a panoramic adaptation of the maintainer's supplied barricade illustration.
  The preserved adapted master is `assets/journal_groups/masters/state_and_revolution_adapted.png`.
  This is a reference-based adaptation, **not a byte-identical copy of the attachment**. Direct attachment
  transfer was unavailable; the original reference item was not modified.
- Only two new banner DDS files are exported in `gfx/interface/illustrations/journal/`. The Ottoman
  category references its native asset directly.
- `tools/build_historical_journal_banners.py` preserves the native banner contract: **1108 × 200,
  DXT5, eleven mip levels, 297,120 bytes**. It uses the current native Great Game header and validates
  every compressed mip's size. The default verifies without writing; `--write` installs only these two
  explicitly named derivatives. Source art is never overwritten.

```text
python tools/build_historical_journal_banners.py --mod-root MOD --vanilla-root "C:/Games/Victoria 3/game"
```

Export/readback checks passed, and the two banner previews were visually inspected. Banner crop, title
contrast, UI scale and clipping still require actual game rendering. No new DLC requirement is added.

## Static evidence and preservation

The expanded step changed **25 journal definitions in twelve explicitly named journal files**, added
one group file and two small localization files, and exported two banner DDS files plus the adapted
source master. The preceding Ottoman step changed nine journal assignments, for 34 changed assignments
and two existing members: **36 grouped definitions overall**.

All ordered fields except the explicit group/context edits compare equal as token streams. Every
untargeted definition in shared files remains byte-identical as a definition body. Existing outcomes,
legacy conclusion blocks, pulses, scopes, counters, dates, cleanup and visibility predicates are unchanged.
Localized group keys are unique and use UTF-8 BOM. Source hashes and exact mappings are in the validation JSON.

For the expanded step, **1,081 protected game-data files** retain their hashes, including the completed
Ottoman grouping, map/history/strategic data, ship definitions and unrelated journals. Every pre-existing
Git status entry is preserved. Private backups/manifests remain outside the mod. There is no local Git
checkout/reset/commit, main merge, historical map change or law-audit change.
The earlier Ottoman-only receipt describes its own earlier validation stage, not a cumulative final hash set.

## Missing Polish partition definitions

The existing localization file `mod_journal_entries_l_french.yml:52,110,113,116` supplies titles for
`je_polish_partitions`, `je_polish_partition_russia`, `je_polish_partition_prussia` and
`je_polish_partition_austria`; corresponding English titles also exist. A literal repository script
search and definition inventory found **no active definitions or script consumers for those four keys**.
Their absence is confirmed in the inspected workspace; its historical cause and whether it is intentional
are unconfirmed. There is consequently no such active journal object to assign to the new group.

The existing reform/restoration chains are grouped above. Recreating partition conditions/effects is a
separate gameplay/historical task; this change does not fabricate missing entries or silently delete titles.

## Acceptance remaining

Fully restart the game using the regular local playset and inspect a fresh 1776 Ottoman, USA/British
Canadian, Spanish-American and Polish/French view as available. Verify localized group headers, expected
active/potential entries, the three illustrations, and the absence of duplicate rows. Check that the
Australian and unrelated international entries retain their categories. Verify the global Forest,
Springtime and Eastern Crisis still share involvement/observer behavior; save/reload and inspect new logs.
All existing journal runtime/migration debt under #27 remains open. Grouping does not establish that
legacy French, Polish, American or Eastern Crisis conclusions already work under 1.15.
