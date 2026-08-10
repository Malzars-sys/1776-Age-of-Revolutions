# WORKSHOP_PREP_1B_LOADING_SCREEN_OBJECTIVE_ART AND REMEDIATION RUNTIME QA

## Status

- Phase: `WORKSHOP_PREP_1B_LOADING_SCREEN_OBJECTIVE_ART_AND_REMEDIATION_RUNTIME_QA`
- Branch: `workshop-prep-frontend-objectives`
- Base HEAD: `56941940bc0d716f5d3d6fcd5d5d5bf54acb8858`
- Predecessor PREP1 present in HEAD: `PASS`
- Human runtime launches: `1 / 1` — quota consumed
- Runtime result: `FAIL_WITH_STATIC_REMEDIATIONS_APPLIED`
- Second runtime required to verify remediations: `YES`
- Second runtime performed in this phase: `NO` — forbidden by the one-launch constraint
- Automatic commit/push: `NO / NO`

## Delivered frontend changes

- Startup loading background: public-domain Clarkson Stanfield `The Battle of Trafalgar`, `3840x2160`, DXT5, 12 mip levels.
- Main-menu background: `Washington Crossing the Delaware` mirrored horizontally so Washington remains clear of the left panel.
- Subtitle: `Age of Revolution` in pure white with the existing italic font and shadow.
- Four objective-card paintings, `779x1327`, opaque RGBA, uncompressed BGRA payload, 11 mip levels.
- Full Bourbon royal standard for the France base flag: white field, semé-de-lis and central royal arms.
- All four selectable frontend theme slots point to `cantus_firmus_monks.ogg` through exact base/DLC virtual filenames encoded as UTF-8 BOM.

No AI-generated image and no Pinterest binary is included.

## Vanilla startup-loading architecture

| Field | Victoria 3 1.13 finding |
|---|---|
| GUI | `gui/frontend/frontend_loadingscreen.gui`, widget `load_screen` / `widget_loading_screen` |
| Vanilla background | `[GetCurrentLoadingScreen]`, with base and DLC candidates |
| PREP1B override | Only the background texture expression is fixed to `gfx/loadingscreens/aor_trafalgar_loading.dds` |
| Fit | `centercrop`; the source is prepared at exact 16:9 |
| Overlay/logo preservation | Loading status, masks, version widget and `gfx/frontend/interface/frontend/loading_logos.dds` remain unchanged |
| DLC behavior | Fixing the GUI background prevents a DLC-selected painting from displacing Trafalgar without removing any overlay |

## Objective illustration architecture

| Field | Finding |
|---|---|
| Dimensions | `779x1327` |
| UI fit | `centercrop` |
| DDS layout | 32-bit uncompressed BGRA with alpha mask, matching audited vanilla cards |
| Mip levels | 11, from `779x1327` to `1x1` |
| Alpha | Fully opaque |
| Disabled behavior | Only `objective_mercantile_republics` declares a disabled background, so exactly one desaturated disabled DDS is provided |

Only `enabled_background` / `disabled_background` paths changed in the four objective definitions. IDs, icons, `recommended_tags`, subgoals, final subgoals and `on_start` remain unchanged. Tutorial and sandbox art remain untouched.

## Final visual mappings

| Internal objective | Visible role | Final art | Runtime state |
|---|---|---|---|
| `objective_battle_for_india` | Bataille pour l'Inde | Khem Karan, `A Mounted Prince Hunting Lion in a Rocky Landscape` (1595), CC0 digitization | First runtime failed on the photo; painting substituted statically afterward |
| `objective_hegemon` | Rivalités impériales | Gudin, `Battle of Ushant (1778)`, public domain | `PASS`, explicitly judged perfect |
| `objective_egalitarian_society` | Âge des Révolutions | Houël, `Prise de la Bastille`, Gallica/BnF reproduction, public domain | First runtime exposed a frame; borderless reproduction substituted statically afterward |
| `objective_mercantile_republics` | Républiques marchandes | Canaletto, `The Bucintoro at the Molo on Ascension Day`, Google Art Project reproduction, public domain | First runtime exposed a frame; borderless reproduction substituted statically afterward |

Source pages, hashes, licenses and exact deterministic crops are recorded in `docs/credits/WORKSHOP_VISUAL_ASSETS_LICENSES.md`. Reproducible transformations are in `workshop_assets/build_objective_art.ps1`.

## Single-runtime observations

Passed during the sole human run:

- Trafalgar startup background, proportional crop and official loading overlays.
- Mirrored Delaware main-menu composition and pure-white subtitle.
- Tutorial and sandbox cards unchanged.
- Imperial Rivalries card.
- USA objective flag with thirteen stripes and thirteen stars, retained British/PLC/Prussian flags, French localization with no raw keys.
- Game entry and stability.
- Frontend audio stopped on game entry; later vanilla music in the in-game music player is expected gameplay music and is not an overlap failure.
- Clean shutdown of Victoria 3 and the launcher.

Failed during the sole human run:

- Frontend music remained vanilla/DLC instead of Cantus Firmus.
- Battle for India used a modern photograph and did not match the painted visual set.
- Bastille and Venice sources showed physical picture frames.
- France used an oversimplified three-fleur base flag instead of the Bourbon royal standard.

Spain and Russia were visible but did not receive an explicit operator verdict; their static Cross-of-Burgundy and imperial-eagle definitions are retained and require confirmation in the later second runtime.

## Music root cause and remediation

Fresh `debug.log` lines 444-447 are directly attributable to PREP1:

```text
File 'music/main_themes/music.txt' should be in utf8-bom encoding
Duplicated key main_theme_track_2 will not be created from file: music/main_themes/music.txt:11
Duplicated key main_theme_track_3 will not be created from file: music/main_themes/music.txt:16
Duplicated key main_theme_track_4 will not be created from file: music/main_themes/music.txt:21
```

The DLC packages registered keys 2-4 before the mod's combined file, so the mod duplicates were rejected. Static remediation:

| Slot | Exact mod virtual file |
|---|---|
| `main_theme_track` | `music/main_themes/music.txt` |
| `main_theme_track_2` | `music/main_themes/mp1_main_theme.txt` |
| `main_theme_track_3` | `music/main_themes/mp2_main_theme.txt` |
| `main_theme_track_4` | `music/main_themes/ep2_main_theme.txt` |

Each file shadows the matching base/DLC virtual filename, contains only its own key, preserves the original DLC gate where applicable, points to `file:/music/age_of_revolution/cantus_firmus_monks.ogg`, and begins with UTF-8 BOM.

## Runtime evidence files

- Expected sequence: `WORKSHOP_PREP_1B_RUNTIME_TEST_MATRIX.csv`
- Human results, root causes and proposed fixes: `WORKSHOP_PREP_1B_RUNTIME_RESULTS.csv`
- Before/after log hashes: `WORKSHOP_PREP_1B_LOG_MANIFEST.csv`
- After-runtime `debug.log` SHA-256: `0EB100C2FA09C54DF9A0388A01459C8A10705D8C3B34ADF66E949FA3513DE495`

## Static remediation QA

Result: `PASS` (`64 / 64` checks).

- All five objective DDS files are `779x1327`, use the expected uncompressed 32-bit BGRA masks, contain 11 mip levels, are `5,508,516` bytes and have alpha `255` throughout every mip.
- Every objective-art reference resolves and objective mechanics remain byte-equivalent to HEAD after removing only background-path lines.
- The loading GUI is byte-equivalent to vanilla 1.13 after normalizing the single Trafalgar texture line and removing the identifying comment.
- Each of the four main-theme files has UTF-8 BOM, contains exactly one unique slot key and points to the Cantus Firmus OGG.
- FRA contains 33 semé-de-lis instances plus the central royal arms; USA retains 13 star instances; SPA and RUS retain the Cross of Burgundy and crowned imperial eagle definitions.
- Replacement source hashes match the license register; the three superseded source images were removed.
- The runtime results contain 24 rows; all five runtime failures include a root cause, proposed fix and `second_runtime_required=YES`.
- The log manifest contains 60 before rows and 60 after rows.
- `git diff --check` passes; the game and launcher remain closed.

The second runtime remains required for the music, replacement art, France flag, Spain flag and Russia flag, but it must occur in a later authorized phase. No relaunch was performed after the failures.

## Protected state

- `thumbnail.png`, descriptor/Workshop ID metadata, description, tags and changelog remain untouched.
- The seven protected untracked technology-research files remain present.
- `stash@{0}` must remain `518df704fa14599c0f254fae13859210663dd976`.
- Automatic commit and push remain forbidden and were not performed.
