# Join Ongoing Wars

Integrated and adapted from **Join Ongoing Wars**, by **The Lizerd King**.

- Original publication: https://steamcommunity.com/sharedfiles/filedetails/?id=3015811655
- Local source: Steam Workshop item `529340/3015811655`, version 1.0, advertised for Victoria 3 1.12.
- Permission: the author's public description explicitly permits integration into other mods. Attribution is appreciated; this fork includes it at the user's request.
- Permission checked: 17 October 2026. This is documented permission, not an invented standalone license.
- Imported asset: `gfx/interface/icons/lens_toolbar_icons/intervene_in_war.dds`, unchanged.
- Adapted scripts: diplomatic action `intervene_in_war`, treaty article `join_war`, and their common scripted implementation in `1776_join_ongoing_wars.txt`.
- New French translation and updated English text accompany the adaptation.
- Source hashes, including all original scripts and the icon, are recorded in `docs/reports/military/AMERICAN_REVOLUTION_R3/BASELINE.json`.

The adaptation allows coastal intervention, checks truces with actual enemies,
permits support of the American independence war while America is a subject,
and uses one common joining implementation for the action, treaty and campaign
events. The French and Spanish campaign probabilities, objectives and AI
investment targets are additions by this fork. They are not attributed to the
original author. The author is not represented as supporting or maintaining
this adaptation. The separate original mod should be disabled when playing
this fork, since it defines the same action and article identifiers.
