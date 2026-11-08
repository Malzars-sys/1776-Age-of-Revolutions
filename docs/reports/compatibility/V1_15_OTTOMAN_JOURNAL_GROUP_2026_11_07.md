# Ottoman Decline journal group - presentation follow-up

Date: 2026-11-07. Refs #27/#24, draft PR #34. Remote parent: `6d2d9f7684f1c5618b9c17ec6e558b44b6f7deab`.
Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. No new in-game acceptance is claimed.

This receipt records the Ottoman-only step, before the maintainer expanded the request to American and
State and Revolution groups. Its protected-file hashes describe that step, not the final cumulative
workspace. See `V1_15_HISTORICAL_JOURNAL_GROUPS_2026_11_07.md` for the expanded delivery.

## Requested result

The maintainer requested a visible **Declin ottoman** group (localized as **Déclin ottoman** in French,
**Ottoman Decline** in English), gathering The Burden of the Sublime Porte, An Empire of Many Masters,
and The Sick Man of Europe. The Great Eastern Crisis is included while preserving its international
behavior. The requested illustration is the native bazaar scene with a mosque associated with
Sphere of Influence content.

The existing `je_group_1776_imperial_crises` key is reused rather than creating a competing category.
It already held the two 1776 Ottoman entries, but its definition only declared `context = country`.
Canonical `common/journal_entry_groups/00_journal_entries.txt:7` documents that `themed` defaults to no,
which places entries individually outside illustrated groups. This explains their location in the
maintainer's screenshot; the journal assignment itself was present.

## Five bounded file changes

| File | Change |
| --- | --- |
| `common/journal_entry_groups/1776_ottoman_reforms.txt:1` | Add `themed = yes`, native illustration and `updates_strategic_region_stances = yes`; retain country context. The latter metadata matches both former native Sick Man and international groups. |
| `common/journal_entries/00_sick_man.txt:4` | Change only the eight existing group fields, including the main entry and seven reform entries. |
| `common/journal_entries/05_great_eastern_crisis.txt:3` | Change the group and add explicit `context = none` so it remains global. |
| `localization/french/1776_diplomacy_ottoman_l_french.yml:9` | Rename the existing group title to `Déclin ottoman`. |
| `localization/english/1776_diplomacy_ottoman_l_english.yml:9` | Rename the corresponding title to `Ottoman Decline`. |

The two entries in `1776_ottoman_reforms.txt` need **no journal-file edits**: their group fields already
use this key. All eleven mod journal definitions now use the illustrated category. Reusing the group
key also preserves existing references rather than renaming journal or localization identifiers.

The 1.15 contract `common/journal_entries/journal_entries.md:8-13` explicitly allows a journal to override
its group's default context, so one group can contain global and country entries. Thus the Great
Eastern Crisis keeps its former effective **none/global** context even though the group's default is
country. Its involved-country predicates, observer visibility, DLC gates, progress, effects and variables
are unchanged. It remains one shared international crisis; this is not a separate Ottoman-only copy.
Other countries seeing the crisis will see it under the same Ottoman Decline theme.

## Existing illustration reused

The selected asset is `gfx/interface/illustrations/journal/je_group_illu_great_game.dds`, already present
in canonical vanilla. Visual inspection confirms a bazaar with awnings and a mosque in the background.
It was compared with the Tanzimat cafe and generic historical-content banners before selection.
The native journal-shaped texture is referenced directly: no image generation, edited texture, new DDS,
DLC file copy or new paid-content requirement is introduced by the illustration reference.

## Why grey international entries appear in 1776

These are visible **potential** entries, not evidence that their crisis has activated. Native
`gui/journal.gui:663` lists a themed group's active entries; line 697 lists its inactive entries in the
same group. Lines 725-769 define the separate potential list for **ungrouped** entries. Consequently,
international potential entries do not move into the generic Potential list shown below the groups.

The mod's `00_peoples_springtime_je.txt:27` shows the Springtime entry when no prior springtime global
flag exists and a European country has `periodical_print_networks`; it has no calendar cutoff in that
visibility block. Activation separately requires `liberal_constitutionalism` and the underway global flag.
`05_grunderzeit.txt:79` shows its potential entry when `ip3_content` is enabled and it has not happened;
activation separately requires `grunderzeit_possible_global_var`. The Great Eastern Crisis's existing
inactive block requires `ip3_content` and no prior crisis flag. These conditions explain early grey
previews. No new date gates, arbitrary 1840 cutoff, or suppression of alternate-history content is added.

## Verification and preservation

- Exact pre-edit backups and fresh SHA-256 guards were used for all six inspected files; only five needed writes.
- The two Ottoman entries' existing membership was confirmed, and the original 1776 reform file
  remains byte-identical. Nine other definitions change category, yielding **eleven group members**.
- All ordered direct fields of the eight Sick Man entries are token-equivalent except `group`.
  All Great Eastern Crisis fields are likewise unchanged except its group and explicit context override.
  Completion/failure/invalidation effects, scopes, deadlines, conditions, pulses and cleanup are untouched.
- Both localization files retain UTF-8 BOM, their language headers and every other localization line.
  The group title has exactly one definition in each language; no duplicate key is introduced.
- Existing line endings are preserved; the Great Eastern Crisis gains only the one necessary context line.
- **1,087 protected files** retain their hashes, including map data, histories, ship types, strategic
  regions, locators and unrelated journals. Every pre-existing Git status entry is preserved.
- The earlier #36 naval correction and #37 passability correction are untouched. No local Git metadata
  write, main merge, map overhaul, law-audit change or historical setup adjustment is performed.

The adjacent validation JSON records the local before/after hashes, explicit mapping and static results.
The original #27 migration audits deliberately compare group fields too; their earlier dated results
describe the earlier layout. This follow-up explicitly permits only the listed presentation changes and
verifies all other fields against the immediately preceding installed revision.
The Great Eastern Crisis's **existing legacy outcome migration remains separate debt**; regrouping does
not certify that its effects work under 1.15.

## Runtime acceptance still required

The changes are installed in the regular local mod. On a **full restart**, load a fresh 1776 Ottoman
game and check the localized illustrated group, title, banner crop and its active/potential rows.
Verify both starting Ottoman entries, then the Sick Man entry/reforms when their existing conditions
make them available. Check the Great Eastern Crisis remains inactive until its real activation criteria,
retains international involvement/visibility and appears under the same theme for other observers.
Save/reload and inspect fresh logs for group/context/localization errors. No screenshot after this
installation or engine execution was obtained; issue #27 remains open for its outstanding runtime tests.
