# Icône des fortifications terrestres

Mode : **outil intégré image_gen**, édition de l’image fournie, `transparent_background = true`. Aucun recours à l’API ou à une clé personnelle. L’exporteur Python effectue seulement l’encodage DDS et la réduction au format canonique, sans détourage ni redessin.

Sources conservées dans le dépôt :

- [Image fournie originale](../../../../workshop_assets/source/aor1776_land_fortification_original.png)
- [Résultat transparent retenu](../../../../workshop_assets/source/aor1776_land_fortification_transparent.png)
- [DDS utilisé](../../../../gfx/interface/icons/building_icons/building_aor1776_land_fortification.dds)
- [Aperçu décodé du DDS](ICON_PREVIEW.png)

Original et résultat : 1 254 × 1 254 pixels. Export : 256 × 256, BGRA8 non compressé, neuf mipmaps, 349 652 octets. Les quatre coins ont un alpha nul ; l’alpha original du détourage est conservé. L’intérieur de la peinture est presque opaque (principalement 252–253 sur 255), sans masque repeint par le convertisseur.

## Consigne exacte utilisée

Use case: background-extraction. Asset type: Victoria 3 building icon. Input image 1 is the exact edit target supplied by the user. Remove ONLY the white background outside the rounded rectangular dark bronze frame and make that outside area genuinely transparent with a clean alpha edge. Preserve the complete frame, all four rounded corners, the existing painting of the star fort, buildings, cannons, surrounding grass, original colors, composition and square proportions as closely as possible. Keep the inside of the framed illustration fully opaque. Do not redraw, restyle, add, remove or replace any element within the frame. No white matte or white halo; no checkerboard baked into the image; no added text. Return a transparent PNG suitable for conversion to an in-game DDS icon.

L’image a été inspectée après détourage et après décodage du DDS. L’export ne remplace aucune icône navale ni autre ressource existante.
