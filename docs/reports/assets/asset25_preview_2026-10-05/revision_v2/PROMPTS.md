# Forts casematés — révision du canon et des ouvertures

Outil : imagegen intégré, deux retouches successives ; aucun appel CLI/API direct. Les deux autres icônes restent inchangées.

## Passe 1 — ouvertures et premier réalignement

Entrée : `../previews/casemated_fortifications.png`. Sortie conservée, non sélectionnée : `iterations/casemated_fortifications_pass1.png`.

```text
Use case: precise-object-edit.
Asset type: revised TECHNOLOGY icon for Victoria 3 / 1776 Age of Revolutions, preview only.
Input image 1 is the EDIT TARGET: the existing isolated masonry artillery casemate cutaway. Preserve the elevated three-quarter composition, single brick barrel vault, warm pale stone walls, brown earth and muted olive grass covering, stone floor, wooden garrison carriage, matte hand-painted volumetric technology-icon style, natural colors and overall silhouette.
Primary request: correct the cannon geometry and add masonry openings.
Cannon correction: rebuild the existing one cannon as ONE continuous rigid tapered cylindrical dark-iron tube, from the rounded breech and small cascabel INSIDE at the left of the carriage to the muzzle THROUGH the wall at the right. The hidden segment passing through the embrasure must lie on precisely the same straight centerline as the visible interior barrel and the short exterior muzzle. The exterior end must NOT be a disconnected shifted piece, a separate tube, or bend. Let enough of the muzzle project beyond the wall to reveal its open dark circular bore, viewed as a perspective ellipse perpendicular to the same barrel axis. Match its diameter, taper, bands and lighting to the interior barrel. Keep the wooden carriage under the tube and trunnions mechanically coherent. No second cannon.
Additional openings: retain the main splayed cannon embrasure in the intact right-hand firing wall, adjusting it only enough for the corrected barrel. Add TWO clearly readable small secondary rectangular embrasures/loopholes in the intact masonry walls, separated from the gun aperture. Each is a genuine recessed passage with stone jambs, lintel and sill, coherent wall thickness, dark interior and visible perspective; not painted black squares, glass windows, random cracks or extra cannon mouths. Place them without undermining the brick vault, keeping thick masonry between all openings. Do not add a second room or turn this into an entire fortress.
Background: genuine transparent alpha around the entire subject. No black/white/checkerboard background baked in, no landscape, external ground, frame, medallion, plaque, display pedestal or cast shadow outside the object. Keep generous uncut margins.
Constraints: change only the faulty cannon/embrasure alignment and the two added openings; preserve the rest of the approved visual concept. No people, flags, text, logos, watermark, cannonballs, modern reinforced concrete, modern gun, glossy 3D finish or global blue/teal cast. ONE square high-resolution isolated icon, readable at 48/64 pixels.
```

## Passe 2 — correction finale de la continuité du tube

Entrée : résultat de la passe 1. Sortie sélectionnée : `previews/casemated_fortifications.png` (avant marges transparentes).

```text
Use case: precise-object-edit.
Input image 1: EDIT TARGET, current revised casemate technology icon.
Make ONLY the correction to the cannon axis and its main firing embrasure described below. Keep the two newly added secondary rectangular openings, the vault, masonry, roof covering, wooden carriage, cutaway camera, all material colors and illustration style unchanged.
CRITICAL geometric correction: the external muzzle on the far right is still LOWER than a straight continuation of the interior barrel. The same gun cannot bend inside the stone wall. This must be a single continuous rigid straight tube. Its axis runs from the breech inside at approximately image-coordinate (520, 715), through the inner barrel center at (795, 690), toward the exterior muzzle at approximately (1205, 650) in this 1254-pixel square reference. These are not annotations to draw, they describe one straight line rising gently to the right. Rebuild the cannon tube from breech to muzzle along that ONE axis, with a naturally tapered bore and outer diameter. RAISE the main wall embrasure AND the external muzzle as necessary to meet that centerline; do not lower, kink, rotate or split the external segment. The exterior muzzle is the open hollow END of the same long barrel, with dark bore ellipse perpendicular to the same axis and consistent rim thickness. The visible tube on both sides of the wall must be in direct straight-line continuation. Widen the main embrasure if useful to visibly see the aligned barrel crossing its depth, while keeping the surrounding masonry coherent. Keep the tube supported by the original wooden garrison carriage.
Do not alter the two secondary openings or add more objects. No second gun, no independent short tube outside, no bent barrel, no floating disconnected iron section, no writing or arrows. Preserve generous margins, native-compatible matte hand-painted volumetric technology-icon style and genuine TRANSPARENT alpha background. No global blue/teal cast, no modern gun, no frame, no landscape, no fake black/white/checkerboard backdrop. Return ONE isolated square icon.
```
