# Machines de précision — révision 2

Mode : **imagegen intégré**, une image générée avec quatre références de sujet fournies par le joueur. Pas de CLI/API de secours.

## Entrées

1. `C:/Users/simeo/AppData/Local/Temp/codex-clipboard-48d4be2b-ad2e-485c-9183-967e3d1ccef7.png` — construction et vue principale.
2. `C:/Users/simeo/AppData/Local/Temp/codex-clipboard-f279ab19-cd11-4a03-a509-d73ecfb68241.png` — silhouette de la même machine.
3. `C:/Users/simeo/AppData/Local/Temp/codex-clipboard-5f6713dc-4e74-45e4-909c-279421357db8.png` — construction d'une machine apparentée.
4. `C:/Users/simeo/AppData/Local/Temp/codex-clipboard-5d162b94-2280-4141-8404-8434843ae583.png` — autre angle d'une machine apparentée.

Les quatre références ont été inspectées avant génération. Elles ne sont pas intégrées dans le mod. Aucune datation ni attribution précise à un fabricant n'est revendiquée.

## Prompt exact

```text
Use case: historical-scene
Asset type: one painted goods icon for Precision Machinery in the Victoria 3 mod 1776 Age of Revolutions.
Primary request: Create an original painterly game goods icon of the historic brass machine for cutting gear teeth shown in the four supplied reference photos. Use the actual machine rather than a generic assembly of huge gears.
Input images: Image 1 and Image 2 are primary subject and construction references of the same machine from the front and three-quarter view. Image 3 and Image 4 are supporting construction references for related gear-cutting machines; do not combine all four into a fanciful hybrid. Follow the silhouette and arrangement of Image 1/2.
Scene/backdrop: truly transparent alpha, including every open space between legs, supports and spindles. No tabletop or room.
Subject: a single small historic precision gear-cutting machine, warm patinated brass body, broad circular horizontal indexing plate, three splayed curved grey-black steel feet, a brass horizontal slide bed above the plate, horizontal spindle and small gear-cutting/workpiece apparatus with fine adjustment wheels, square upright dark steel column on the right with a brass sliding clamp and thumb screws, a long hand crank projecting left with a dark handle. Keep the visible architecture coherent and supported. Adjustment wheels are small, not enormous loose gears.
Style/medium: refined painted and volumetric object illustration like native Victoria 3 goods icons, realistic natural material colours and restrained weathered texture, crisp readable silhouette and simplified small details. Not a flat PM pictogram, not a photo, not a glossy modern 3D app icon.
Composition/framing: square 1024x1024 or greater, full machine in front-left three-quarter view matching reference 1/2, generously framed with transparent margin, no clipping of crank or feet. Clear enough to be recognized at 32 and 48 pixels.
Lighting: soft neutral warm light from upper left, restrained highlights, shading on the object only, no external cast shadow.
Materials: muted aged yellow brass and natural dark grey steel, no global blue/cyan cast, no uniform sepia filter.
Constraints: no text, labels, arrows, border, roundel, background, watermark, paper, glass, unrelated extra objects, giant paired spur gears, disconnected impossible parts. Preserve the reference machine's distinctive circular plate, arched feet, crank and vertical column. Deliver a single isolated transparent painted icon.
```

## Sortie

Original conservé : `C:/Users/simeo/.codex/generated_images/01a080b1-616e-71b2-85c3-0d7759724725/exec-56bcf5a0-1314-4722-b4ad-60e76307985e.png`.

Copie projet : [master original](previews/precision_machinery_source.png). Le registre `docs/reports/assets/source_registry.json` indique la marge transparente de 151 px par côté avant réduction et export DDS. Aucun changement artistique programmatique. Le master avec marge, les miniatures et les candidats DDS ne sont pas conservés : l'outil commun les reconstruit en mémoire. Le concept précédent et ses dérivés ont été retirés du dépôt lors du nettoyage.
