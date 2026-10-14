# Preferred imperial emblem — version 2

The user replaced the first supplied emblem with the darker black-and-gold version on 12 October 2026. Only version 2 is selected for the custom imperial identity. The first generated cutout is not installed.

## Image operation

Built-in image tool, `background-extraction` edit. Prompt: remove only the plain black background outside the emblem and in open gaps; preserve the black feathers, dark black-and-gold filigree, crowns, shield, red gemstones, pearls and original proportions. No redesign, recoloring or extra border. The output was visually inspected against the supplied version. Generated extraction is not claimed to be pixel-identical to the original.

The transparent PNG master is `workshop_assets/source/map2k_hre_emblem_v2.png`. `tools/export_map2k_hre_emblem.cjs` converts it to the native central-identity icon dimensions with complete mipmaps, preserving alpha and logical color values. The result is `gfx/interface/icons/central_identity_pillars_icons/aor1776_imperial_federation_v2.dds`.

## Integration status

The asset is bound to `identity_aor1776_imperial_federation` in the working mod. Its appearance has not been tested in Victoria 3. This asset operation does not imply native-engine validation of elections, imperial pacts, bloc succession or decree preservation. No commit, merge or push accompanies this revision.
