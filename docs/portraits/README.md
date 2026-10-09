# Frederick II portrait (1776)

The face DNA is an interpretation of the Anton Graff (1781) and Johann Georg
Ziesenis (1763) portraits. `frederick_ii_1776_editor.txt` is the persistent editor
DNA; the runtime definition is `common/dna_data/00_frederick_great_pru.txt`.
The existing character history, birth date, and clothing remain unchanged.

## Wig attribution

**WIG** by [hype404](https://sketchfab.com/hype404), supplied through
[Sketchfab](https://sketchfab.com/3d-models/wig-79cae6a6a01143808e94ab33aba03136),
is licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
Changes: position/scale adaptation, native head-rig skinning, PDX export, and
native DDS texture packing, opaque-body/strand separation, cutout mipmap
coverage adaptation, and local powdered-colour/roughness calibration.
No endorsement by the author is implied.
Attribution is also included beside the runtime mesh in `LICENSE.txt`.

Only the author's original FBX/TGA archive is preserved in
`sources/wig_hype404_original.zip` (SHA-256
`fa5c2d3a49663acca307f775b40a67cb797b00994ee3e3e79388a76cc5b6f37c`).
It contains two supplied mesh variants; the full-quality `SM_Wig_01a` is used.
Do not add extracted duplicates, tiny previews, or test renders to version control.

## Rebuild

Requires Python with Pillow, Blender, an installed `io_pdx_mesh` extension,
and the user's own Victoria 3 installation. For example, from the repository:

```powershell
python tools/build_frederick_wig.py --game "C:/Games/Victoria 3/game" --blender "C:/Program Files/Blender Foundation/Blender 5.2/blender.exe" --pdx "C:/Users/simeo/AppData/Roaming/Blender Foundation/Blender/5.2/extensions/user_default/io_pdx_mesh"
```

Adjust the three installation paths for your computer. The default output is
`.asset-cache/portraits/frederick_wig_build/runtime`; add `--integrate` only to
replace the five runtime mesh/texture files. Generated previews are not required
for rebuilding.

Run `python tools/test_frederick_wig.py` for portable opacity, coverage, normal
packing and material-channel regression tests. Only Pillow is required.

The local `02_genes_accessories_hairstyles.txt` preserves all installed vanilla
templates unchanged and appends template 33. It does not add the wig to random
hair lists: selected historical rulers use explicit DNA or a character-local
portrait modifier, as documented below. When updating the game,
merge any new vanilla templates and recheck template-index uniqueness.

## Other historical rulers (1776)

The same mesh, accessory, textures and licence are reused; no separate models
or texture copies are needed. Only the `hairstyles` gene was changed in the DNA
of Louis XVI (FRA), George III (GBR), and Charles III (SPA). All other genes,
including facial morphs, skin colour, age effects and body proportions, remain
unchanged.

For rulers without explicit DNA, their own `on_created` marks the character
with `aor1776_historical_powdered_wig`. The additive, namespaced portrait group
in `gfx/portraits/portrait_modifiers/zz_aor1776_historical_powdered_wigs.txt`
replaces only their hairstyle. It has no fallback or positive default weight,
like vanilla's accessories group. Unmarked characters and pops receive no
modifier; generated successors do not inherit a country-wide rule. Adult,
male and historical-character guards protect unrelated characters.

The selected starting rulers are:

| Tag | Historical ruler | Selection |
| --- | --- | --- |
| PRU | Frederick II | Existing explicit DNA; unchanged by this expansion |
| FRA | Louis XVI | Explicit hairstyle DNA |
| GBR | George III | Explicit hairstyle DNA |
| SPA | Charles III | Explicit hairstyle DNA |
| SWE | Gustav III | Character-local marker |
| DENNOR | Christian VII | Character-local marker; covers Denmark and Norway |
| BAV | Maximilian III Joseph | Character-local marker |
| SAX | Frederick Augustus III | Character-local marker |
| WUR | Karl Eugen | Character-local marker |
| BAD | Karl Friedrich | Character-local marker |
| BRA | Karl I of Brunswick | Character-local marker |
| HEK | Friedrich II of Hesse-Kassel | Character-local marker |
| HES | Ludwig IX of Hesse-Darmstadt | Character-local marker |
| MEC | Friedrich of Mecklenburg-Schwerin | Character-local marker |
| MST | Adolf Friedrich IV of Mecklenburg-Strelitz | Character-local marker |
| COB | Ernst Friedrich of Saxe-Coburg-Saalfeld | Character-local marker |

This is shared period styling, not a claim that these men wore identical wigs.
Painted powdered hair alone does not establish whether the hair was a wig or
natural hair. The already-approved Frederick model is a visual approximation
of this court style, not an individual reconstruction for every ruler.

Historical references consulted on 6 October 2026:

- [Louis XVI, Callet, Versailles](https://www.chateauversailles.fr/ressources-pedagogiques/rois-reines-versailles/louis-xvi/louis-xvi-roi-france-navarre): powdered court coiffure visible in the official portrait.
- [George III, Royal Collection](https://www.rct.uk/collection/stories/royal-portraiture/george-iii-1738-1820) and its [Style & Society catalogue script](https://media.rct.uk/sites/default/files/2024-04/Style%20%26%20Society%20Plain%20English%20Script.pdf): explicitly identifies his queue wig.
- [Charles III, Mengs, 1767, Prado P002200](https://www.museodelprado.es/coleccion/obra-de-arte/carlos-iii/1e754324-0855-42b8-8430-732df3b54b5c): powdered side curls and a tied queue visible; the catalogue also records a circa-1774 version. Spain is therefore included, not excluded by a blanket nationality rule.
- [Gustav III and his brothers, Roslin, 1771, Nationalmuseum NM 1010](https://collection.nationalmuseum.se/en/collection/item/18013/): period powdered court hairstyles visible.
- [Christian VII, Royal Danish Collection](https://denkongeligesamling.dk/en/the-collection/persons/christian-vii-1749-1808/): portrait shows powdered side curls and a black queue bow.
- [Maximilian III Joseph, 1775 bust, Bayerisches Nationalmuseum R 5383](https://www.bayerisches-nationalmuseum.de/sammlung/00035752), [Frederick Augustus III, Graff, Dresden](https://skd-online-collection.skd.museum/Details/Index/304542), [Karl Eugen, Landesmedienzentrum via LEO-BW](https://www.leo-bw.de/en/detail/-/Detail/details/DOKUMENT/lmz_bilddatenbank/LMZ020165/Herzog%2BCarl%2BEugen%2Bvon%2BW%C3%BCrttemberg%2Bum%2B1740%2B-%2BKupferstich%2Bdes%2BJugendbildnisses), [Karl Friedrich, Landesarchiv BW](https://www.landesarchiv-bw.de/de/themen/praesentationen---themenzugaenge/47599), [Karl I, Herzog August Bibliothek collection record](https://www.deutsche-digitale-bibliothek.de/item/7PJPEZTRKAPOTSY5MIPZWA6ZVPPVHYPA), [Friedrich II, Kassel](https://altemeister.museum-kassel.de/30085/), [Ludwig IX, Schlossmuseum Darmstadt](https://freunde-des-schlossmuseum-darmstadt.de/adventskalender-2022/), [Friedrich, Schwerin museum catalogue](https://www.museum-schwerin.de/export/sites/museum/.galleries/Publikationen/Katalog-Lisiewska.pdf), [Adolf Friedrich IV, Woge collection record](https://www.kulturgutschutz-deutschland.de/DE/3_Datenbank/Kulturgut/MecklenburgVorpommern/08801_086.html), and [Ernst Friedrich, Saalfeld Stadtmuseum print, circa 1764](https://www.saalfeld.de/files/1929F09D2C7/Ausgabe_09-10_2024web.pdf): individual iconographic references for the selected imperial rulers. Some references are earlier or later than 1776; selection of one shared 3D coiffure is a period-style inference, not an exact 1776 wig identification.

Women (including Maria Theresa and the Meiningen regent), child heirs,
non-European rulers and unselected princes are unchanged. No general beard,
clothing or headgear rule is introduced. This expansion does not attach the
pending tricorne or change the approved wig material calibration.

Run `python tools/test_historical_wigs.py` to check the curated character list,
scope guards and the DNA-to-gene-to-accessory-to-entity bindings. The material
tests remain in `tools/test_frederick_wig.py`. These are static tests: visual fit
on the additional faces still needs an in-game check. The twelve history
markers require a new campaign; an old save does not re-run `on_created`.
A restart is recommended to load the new portrait-modifier definition.

## Frederick II tricorne — fit approved; finishes awaiting in-game review

The separate headgear model is extracted from the supplied bust archive, not
from the wig or a vanilla hat. Source, licence, measured native references,
runtime bindings and the current verification limits are recorded in
`../reports/AOR1776_FREDERICK_TRICORNE_ASSET_REPORT.md`.

Rebuild with `python tools/blender/extract_frederick_tricorne.py --mode build`;
add `--integrate` to replace the runtime hat mesh/textures and work blend.
Use `--mode preview` for ignored, offline diagnostic renders only. The defaults
refer to this workstation; `--game`, `--blender` and `--pdx` can be overridden.
Only the original bust/ribbon zips, work blend, scripts and runtime files are retained
as deliverables; extracted copies and previews remain in `.asset-cache/`.
`--mode work` restores only the work blend from the local build cache, using
the current runtime textures, without rewriting the game-facing mesh/DDSs.

Run `python tools/test_frederick_tricorne.py` for static checks. It accepts
optional `--game`, `--pdx` and `--blender` paths for native mesh/shader and work
blend checks. Neither
these tests nor offline renders establish that the hat appears in the game.

On 7 October 2026 the custom special-gene modifier was corrected from
`mode = replace` to the installed vanilla headgear convention `mode = add`.
The approved wig, face DNA, hat geometry and textures were not changed by that
binding correction. The engine had loaded the hat mesh, but the user's
screenshots showed no hat. The latest on-disk exit save also has no tricorne
marker on Frederick. It is not known whether the screenshots show that save
or a new campaign. Restart with the fork enabled and start a new 1776 campaign
for an unambiguous test; simply loading an old save does not execute the new
`on_created` marker. No existing save was edited.

The user's subsequent screenshot confirms that the hat appears with the wig.
That first in-game fit was rejected as perched too high and too small in
height and side reach. The subsequent 25/33/18 fit with a 50cm base was still
too high. Following the supplied painting and requests for more width and a
sharper point, the model now uses source scale 27.5/36/24, a 44.5cm base, a
3.5cm depth offset and no automatic lift. Its central forehead opening stays
at approximately 49.6cm, just above the neutral native brow. A tapered 4cm
central rise sharpens the crown without raising that opening.
It is approximately 46.25cm wide, 34.17cm deep and 22.69cm tall. A small local
crown-clearance correction surrounds the unchanged upper wig; the visible
curl piercing the felt is gone in the offline diagnostics. The neutral head
has no surface intersection; remaining wig contacts lie near the low side
rim at 47.48–49.03cm, not the upper crown. Face, side curls and queue remain
visible in front/profile/back/top diagnostics. Neither the wig nor its DNA
was changed. Normals were rebaked for the new shape. The approved felt body is
2,888 triangles. Tests guard its exact position/UV fingerprint, bounding dimensions,
raised apex and preserved low forehead seam in the work blend.

The user approved the enlarged, lowered and sharpened fit in the screenshot
`codex-clipboard-106ccde6-522a-456d-8dda-a16b49be95f1.png`. Later changes are
additive finishes only: a pale fringe with 432 irregular tapered fibres, and
the supplied ribbon bow, black and turned upright over the scanned bump.
The initial smooth white piping candidate was rejected as insufficiently furry.
The fringe is actual opaque geometry, not a transparent hair shell.
Both front and rear raised edges are fringed; the approved 232 rear fibres are
preserved, with 200 added on the front edge and coincident sections not doubled.
The combined hat has 6,378 triangles, one material and the existing three DDSs.

**Ribbon Bow** by [Maggatron / MaggaModels](https://sketchfab.com/MaggaModels),
[Sketchfab model](https://sketchfab.com/3d-models/ribbon-bow-4df59dfe3a474b07a408c037eacb6a6f),
is [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), verified from its
public Sketchfab API record on 7 October 2026. Source ZIP:
`sources/ribbon_bow_original.zip`, SHA-256
`aecdf0cdfdf19e822e40bed034d94392e01e9ee920de7045cc681ee6df88b239`.
Its 48,212 triangles are reduced to **898** for runtime, with real loop depth
retained. Changes also include black matte atlas materials, sizing, orientation,
backing adaptation and attachment to the hat. Both artists are credited beside
the mesh. The combined hat derivative remains CC BY-SA 4.0; the original ribbon
archive remains CC BY 4.0. No endorsement is implied.

**The new finishes still need in-game review.** Restart/reload portrait assets
and inspect the existing marked character again. A new campaign is not needed
for these mesh/texture-only additions. Offline diagnostics use a neutral head,
not Frederick's facial morphs or Victoria 3's renderer. No game or save was
controlled during this finishing pass. Cache renders remain ignored.

## Frederick II original cane

The maintainer chose an original reconstruction from the painting instead of
the BlenderKit Royalty Free Walking Stick. No BlenderKit model or addon is
included. The original cane has a dark wooden shaft, a light curved handle
and small aged-metal fittings: 1,808 triangles, one material, three 512px DDSs.
Editable source: `frederick_cane_work.blend`; runtime and provenance:
`gfx/models/portraits/attachments/props/aor1776_frederick_cane/`.

Rebuild: `python tools/blender/build_frederick_cane.py --integrate`; use
`--mode preview` for ignored cane/hand-grip renders and
`python tools/test_frederick_cane.py` for seven static/native checks.
The rigid prop is attached to `bn_r_prop`. A Frederick-only animation rule uses
the installed native walking-cane head/body pose, with our own prop, not the
vanilla cane. No character DNA or wig is changed by the cane. Offline grip
checks cover frames 1, 76 and 151; actual in-game selection/rendering is pending.

`gfx/portraits/portrait_animations/animations.txt` preserves the installed
1.13.11 definition and adds one scoped idle entry. This full definition override
must be merged when the native file changes or another mod overrides it. The
test compares all other rules against the installed native file. Native mesh,
texture and animation binary files are only local references, not redistributed.

## Wig verification status

The exported mesh was read back successfully (9,932 triangles, two materials,
5,889 UV/normal-split vertices). Native inverse-bind matrices are preserved and
the four-influence skin weights are normalized. All four 1024px DDS textures
have complete mip chains. Existing vanilla hair templates remain unchanged.

The user's cold-start screenshots confirmed that the gene, accessory and mesh
load in Victoria 3, but the wig was translucent. Treating both source shells as
native cutout hair was also visually rejected: the source mask is a pattern of
very fine fibres, and its low alpha values made the structural curl volumes
almost disappear. The source coverage above the native 0.5 cutoff is 15.74%;
an ordinary reduction to 1024px reduced it to approximately 10.02% even before
the game sampled coarser levels.

The inner `MI_Wig_01a` shell is now used as the opaque wig body, with
`portrait_hair_opaque` and a separate base diffuse whose alpha is 255 at every
pixel and mip level. Only the expanded `MI_Wig_01b` shell uses `portrait_hair`
and the fine strand mask. Strand mipmaps preserve source cutout coverage while
accounting for the native shader's mip-dependent alpha boost; zero-mask gaps
remain zero. RGB is filtered independently from the strand mask. No game-wide
shader is overridden. The opacity correction left face DNA, geometry, skin
weights, base-level normal packing and material properties unchanged.
The coverage-preservation approach follows the principle documented by
[Microsoft DirectXTex](https://github.com/microsoft/DirectXTex/wiki/ScaleMipMapsAlphaForCoverage);
the build tool implements it locally and does not require that library.

The user's subsequent in-game screenshots confirmed that transparency is fixed,
but showed an overly bright wig. The source albedo averaged approximately
218/219/222 in 8-bit RGB and used constant roughness 146/255; the local native
European hair reference averages about 199/255 roughness. There is no added
emissive effect: both materials use native `PS_hair`, with a zero SSS mask and
zero metalness. The native normal decoder was checked directly: it reads X
from G and negates Y from A, matching the existing packing.

The lighting revision scales source RGB values by 0.88 (mean approximately
192/193/196) and raises perceptual roughness to at least 198/255, retaining the
native hair specular value of 56/255. The wig remains light powdered grey, with
headroom for highlights. These are local material calibrations, not a change to
portrait lighting or the other characters. Normal and material mipmaps now
filter all four channels independently: their A channel is data, not opacity,
and must not premultiply the other channels. The mesh, face DNA, skinning and
every diffuse alpha mip remain identical to the confirmed opaque revision.

The rebuilt bindings, DDS mipmaps and portable regression tests were checked.
The lighting adjustment still needs visual confirmation in Victoria 3; offline
geometry/material diagnostics do not establish its actual in-game appearance.
Reload assets/textures in the portrait editor, or restart the game with this
mod enabled, then inspect Frederick II. The hairstyles gene itself is already
loaded, so it is not necessary to start a new campaign just for this material
change. No commit or push was performed.
