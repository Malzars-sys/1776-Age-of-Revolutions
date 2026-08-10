# WORKSHOP_PREP_1_FRONTEND_MUSIC_AND_OBJECTIVES

## Status

- Phase: `WORKSHOP_PREP_1_FRONTEND_MUSIC_AND_OBJECTIVES`
- Branch: `workshop-prep-frontend-objectives`
- Base/HEAD: `12ae520dd6b7fbfd2651bfffb604e9dd43ea469e`
- Static QA: `PASS`
- Human runtime launches: `1 / 1`
- Runtime QA: `PARTIAL_FAIL_REMEDIATED_STATICALLY`
- Fresh-log QA: `NEW_WORKSHOP_PREP_ATTRIBUTABLE_ERRORS = 0`
- Next phase: do not start `WORKSHOP_PREP_2_THUMBNAIL_METADATA_AND_DESCRIPTION` until the post-runtime remediation is accepted without a second launch.

## VANILLA_1_13_FRONTEND_ARCHITECTURE

| Field | Victoria 3 1.13 finding |
|---|---|
| `background_source` | `gui/frontend/frontend_main.gui` creates a 1920×1080 `video_icon` backed by `[FrontEndMainView.GetMainMenuImage]`; the base movie is `gfx/interface/illustrations/frontend/menu_video.bk2`. Vanilla also ships `gfx/frontend/interface/illustrations/frontend/frontend_bg.dds`, a 3840×2160 DXT5 texture with 12 mip levels. |
| `gui_source` | `gui/frontend/frontend_main.gui`, root widget `mainmenu_panel_bottom`; both background and UI use a 1920×1080 canvas with `ScaleToFitElementInside`. |
| `logo_source` | `v3_logo_animation` at position `{ 0 35 }` in `frontend_main.gui`; the type is defined in `gui/in_game_menu_logo.gui` and uses the existing Victoria 3 logo textures. |
| Continue position | The first single-player button group starts at `margin_top = 210`; the subtitle is placed at Y=158 in the gap below the logo and above this group. |
| `music_source` | `music/main_themes/music.txt` defines the base `main_theme_track` separately from the in-game tracks in `music/music.txt`. Three owned DLCs additionally register `main_theme_track_2`, `_3` and `_4`; The Great Wave supplies `_4`. All use `can_be_interrupted = yes`. |
| playlist/triggers | The title theme uses the dedicated `main_theme_track`; regular soundtrack entries remain in `music/music.txt`. No global playlist was replaced. |
| image format | Vanilla reference DDS: 3840×2160, RGBA decode, DXT5, 12 mip levels, 11,060,752 bytes. |
| audio format | The engine accepts file-backed OGG/Vorbis main themes; the local 1.13 mod example confirmed `music = "file:/music/...ogg"`. |
| resolution behavior | The vanilla 1920×1080 `ScaleToFitElementInside` canvas is preserved. 1920×1080 and 2560×1440 are exact 16:9 scales; 2560×1600 and 3440×1440 keep the painting proportional under the same vanilla fit behavior, without stretching. |

### Override strategy

`frontend_main.gui` offers no proven additive hook for replacing only its code-driven background or inserting a new child in the legacy root widget. The safe override is therefore an exact same-path copy of the 1.13 file with only two changes: the `video_icon` becomes one static `icon`, and one localized `text_single` is inserted. A no-index comparison against vanilla confirms only these two hunks.

The initial runtime proved that shadowing the base `music/main_themes/music.txt` was insufficient: the active Great Wave DLC could still select `main_theme_track_4`. The corrected file defines all four known frontend slots and points each to the same Cantus Firmus OGG. The engine already selects one title slot rather than playing all DLC themes concurrently; covering every selectable key prevents a DLC theme from taking precedence. The in-game soundtrack remains untouched.

- `files_to_override`:
  - `gui/frontend/frontend_main.gui`
  - `music/main_themes/music.txt`
  - `common/objectives/01_player_objectives.txt` (existing fork file; two `recommended_tags` lines only)
  - `common/coat_of_arms/coat_of_arms/03_new.txt` (period base flags for recommended country definitions)
  - `common/flag_definitions/00_flag_definitions.txt` (preserve the French republican tricolor transition)
- `files_to_create`:
  - `gfx/interface/illustrations/frontend/age_of_revolution_frontend_bg.dds`
  - `music/age_of_revolution/cantus_firmus_monks.ogg`
  - dedicated English and French localization files
  - source-asset archive and music credit document

## Background

Human source: `workshop_assets/source/washington_crossing_delaware.png` (exact SHA-256 copy of the operator-provided PNG: `C8B1D6C637E4945BFF574F3CFF226B5E3637DEC115BCC89EE13BBD79D0E4BCD9`). No other image was downloaded or generated.

The 1920×1230 source was cropped to 1920×1080 by removing 75 pixels from both top and bottom, then resized proportionally to 3840×2160. This keeps Washington, the flag and finial, the boat, principal figures, horses, water and foreground ice. The final DDS reuses the exact 128-byte vanilla header and contains a complete DXT5 mip chain:

`3840×2160, 1920×1080, 960×540, 480×270, 240×135, 120×67, 60×33, 30×16, 15×8, 7×4, 3×2, 1×1`.

Final DDS SHA-256: `6AD0A5D97CE497FA097BB2856DF89C7A56376517CD84A6ACDF29B2B2A0814857`.

## Frontend subtitle

- Localization key: `age_of_revolution_frontend_subtitle`
- English and French value: `Age of Revolution`
- Existing game font: `EBGaramond`, italic, size 30
- Existing formatting: gold with shadow
- Position: centered at Y=158 in the left main-menu panel
- The Victoria 3 logo and button definitions are otherwise unchanged.

## Frontend music and credits

Human source: `workshop_assets/source/Cantus_Firmus_Monks_Doug_Maxwell.mp3` (exact SHA-256 copy of the operator-provided MP3: `FA8E7548A1FD1A70ADA7C58E4D39CA6331025D28239DC10EF951C25FFEACFE56`). No alternate copy was downloaded.

Final audio: OGG/Vorbis, stereo, 44.1 kHz, nominal 192 kb/s, 100.301 seconds. The OGG has 543 structurally complete pages and SHA-256 `F2BB4A6509159AAC26DEA6CC2BF118636942EE72894BDAD571DF9946C4105B34`.

`main_theme_track`, `_2`, `_3` and `_4` now all point to `file:/music/age_of_revolution/cantus_firmus_monks.ogg` and retain `can_be_interrupted = yes`. This covers the base game plus Melodies for the Masses, Songs of the Homeland and The Great Wave title selectors while leaving `music/music.txt` untouched. The first runtime confirmed that frontend music stops cleanly after entering a game; selection of the custom track after covering all four slots is statically remediated but cannot be relaunched under the one-launch cap.

Credits and the mandatory pre-publication license recheck are recorded in `docs/credits/CANTUS_FIRMUS_MONKS_LICENSE.md`. The track is attributed as CC BY 3.0; it is not described as public domain.

## Objective architecture and compatibility decision

The internal IDs remain:

- `objective_egalitarian_society`
- `objective_hegemon`

Renaming them would unnecessarily risk journal-entry/subgoal wiring, tutorial lessons, the `hegemon` and egalitarian achievements, UI lookups and existing saves. Their icons and full mechanical chains are unchanged. The tutorial lesson IDs also remain, while their visible welcome/completion localization now uses the new themes.

Only these gameplay-script lines changed:

- `objective_egalitarian_society`: `{ FRA USA PLC }`
- `objective_hegemon`: `{ GBR SPA RUS PRU }`

`objective_battle_for_india`, `objective_mercantile_republics`, tutorial, sandbox, all subgoal lists, final subgoals and `on_start` effects are byte-for-byte unchanged relative to the branch base apart from those two lines.

Visible presentation:

- `Age of Revolutions` / `Âge des Révolutions`
  - France
  - dynamic `$dyn_c_thirteen_colonies$` (Thirteen Colonies / Treize Colonies) on the real `USA` tag
  - Polish-Lithuanian Commonwealth / République des Deux Nations (`PLC`)
- `Imperial Rivalries` / `Rivalités impériales`
  - Great Britain / Grande-Bretagne
  - Spain / Espagne
  - Russia / Russie
  - Prussia / Prusse

The final `sg_the_hegemon` remains internal; its visible journal title is localized as `Imperial Supremacy` / `Suprématie impériale`. The old objective names were also removed from the two tutorial welcome and completion messages without altering lesson scripts.

### Period flags in objective cards

Runtime showed that recommended-country cards use `CountryDefinition.GetBaseFlag`, not the date-, law- and country-aware dynamic flag. The default tag blazons therefore exposed later designs. Existing scriptable Victoria 3 coat-of-arms components were reused; no image was generated or downloaded.

- `FRA`: Bourbon white field with gold fleurs-de-lis; a separate `FRA_revolutionary_tricolor` is selected by the existing republican trigger.
- `USA`: thirteen stripes and thirteen stars for the Thirteen Colonies / early United States.
- `SPA`: Bourbon Cross of Burgundy on white.
- `RUS`: eighteenth-century imperial eagle banner.
- `GBR`: the vanilla base definition already represents the 1707–1800 Union Flag.
- `PRU`: the vanilla base Prussian eagle is suitable for 1776.
- `PLC`: the existing Commonwealth base banner is retained.

## Localization

Created:

- `localization/english/age_of_revolution_frontend_l_english.yml`
- `localization/french/age_of_revolution_frontend_l_french.yml`

Both files have an UTF-8 BOM, the correct language header, 33 unique keys, balanced quoting and no duplicate key in the fork's other localization files. All operator-provided global and country texts are present; the USA objective name uses the existing dynamic-country localization key.

## Static QA

Final result: `PASS`.

- 47 structural/content checks passed after correcting two Unicode literals in the QA harness itself.
- Source PNG and MP3 are exact copies of the operator assets.
- DDS header, dimensions, DXT5 compression, byte size and 12 mip levels match vanilla 1.13; Pillow successfully decodes the result as 3840×2160 RGBA.
- OGG container, Vorbis identification header, stereo/44.1 kHz/192 kb/s properties, all pages and duration passed.
- GUI, objectives and music definitions have balanced braces and terminated strings.
- Both localization files pass BOM/header/key/quote/duplicate checks.
- `FRA`, `USA`, `PLC`, `GBR`, `SPA`, `RUS` and `PRU` all exist in the fork country definitions.
- GUI texture, localized subtitle, existing `EBGaramond` font and main-theme file links resolve.
- `git diff --check` reports no whitespace error.
- Static painting preview shows no non-proportional distortion and retains the requested composition.
- `thumbnail.png`, Workshop metadata/description and all unrelated gameplay remain untouched.
- Post-runtime remediation: four unique frontend theme keys, four identical valid OGG links, four interruptible definitions, five unique new/overridden CoA keys, thirteen USA star instances, required texture resolution, Clausewitz brace/string balance and the French republican flag redirect all pass.
- The seven protected technology-research files still match their pre-runtime SHA-256 hashes.

## Runtime QA

Status: `PARTIAL_FAIL_REMEDIATED_STATICALLY`.

| Runtime check | Result |
|---|---|
| Delaware painting and proportional crop | `PASS` |
| Victoria 3 logo and `Age of Revolution` subtitle | `PASS` |
| No raw localization keys | `PASS` |
| `Âge des Révolutions` and `Rivalités impériales` cards | `PASS` |
| Required recommended countries and French descriptions | `PASS` |
| Battle for India, Mercantile Republics, Tutorial and Sandbox visible/intact | `PASS` |
| Frontend music stops after entering a game | `PASS` |
| Custom title track selected instead of DLC theme | `FAIL` in runtime; remediated by covering `main_theme_track_2`, `_3`, `_4` |
| Period flags on recommended-country cards | `FAIL` for obvious base tags such as FRA and USA; remediated with 1776 base CoAs |

The operator closed both game and launcher after this single session. Screenshots document the successful visual/localization checks and the anachronistic pre-remediation flags.

Fresh `error.log`, `debug.log`, `gui.log` and `warning.log` contain no reference to the new GUI path, DDS, OGG, subtitle key, objective IDs or new asset paths. The large legacy diagnostic families (`sr`, old triggers/effects and the known construction-panel localization issue) remain unrelated. Result: `NEW_WORKSHOP_PREP_ATTRIBUTABLE_ERRORS = 0`.

## Remaining limits

- The one authorized human launch has been consumed. The music-slot and period-flag corrections made from runtime evidence are statically validated but deliberately not relaunched.
- A full-file GUI override is sensitive to future Victoria 3 updates; it is intentionally pinned to the audited 1.13 file and limited to two hunks.
- License metadata must be rechecked by the operator immediately before Steam Workshop publication.
- Final state: successful runtime presentation/objective QA, zero attributable log errors, and static remediation of the two runtime defects. A strict all-runtime-pass completion verdict is not issued because a second launch is forbidden.
