# WORKSHOP PREP 2 — Thumbnail, metadata, description and publication packet

Date: `2026-08-10`  
Branch: `workshop-prep-frontend-objectives`  
Baseline HEAD: `37cbfdb45499911178344fa981d4b0f9e04431ca`  
Steam publication performed: `NO`

## Scope and result

PREP2 prepares the already runtime-validated fork for a later manual Steam Workshop publication. It does not change gameplay, create a Workshop item, upload files, assign a `publishedfileid`, change GitHub visibility, commit or push.

The operator-selected public title is exactly:

```text
Age of revolution /Fork
```

The internal mod name and file identifiers remain unchanged.

## PREP1 closure

The final PREP1E report was reviewed and the validated frontend/objective baseline was not reopened.

```text
WORKSHOP_PREP_1_FRONTEND_OBJECTIVES_FULLY_RUNTIME_VALIDATED = YES

BEO_BASE_COA_RUNTIME_PASS
TRAFALGAR_LOADING_SCREEN_REMAINS_PASS
DELAWARE_FRONTEND_REMAINS_PASS
CANTUS_FIRMUS_REMAINS_PASS
BIC_FLAG_REMAINS_PASS
VOC_FLAG_REMAINS_PASS
OBJECTIVE_ART_REMAINS_PASS
TUTORIAL_TEXTS_REMAIN_PASS

NEW_WORKSHOP_PREP_1E_ATTRIBUTABLE_ERRORS = 0
```

No Victoria 3 runtime was required or performed in PREP2.

## Git preflight and protected state

The preflight established the requested branch, a clean tracked baseline and an empty index before PREP2 changes. The only pre-existing untracked files were the seven protected technology-research files.

```text
PREFLIGHT_BRANCH = workshop-prep-frontend-objectives
PREFLIGHT_TRACKED_WORKTREE = clean
PREFLIGHT_INDEX = empty
PREFLIGHT_HEAD = 37cbfdb45499911178344fa981d4b0f9e04431ca
PROTECTED_TECH_RESEARCH_COUNT = 7
```

The protected stash was neither read, applied nor modified:

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
STASH_NAVY_3C_3_HASH = 518df704fa14599c0f254fae13859210663dd976
```

## Thumbnail audit and transformation

The effective Workshop thumbnail is the root `thumbnail.png`. Its original state was preserved byte-for-byte at `workshop_assets/source/thumbnail_before_fork_badge.png` before transformation.

### Original

```text
CURRENT_THUMBNAIL_PATH = thumbnail.png
CURRENT_THUMBNAIL_DIMENSIONS = 600x600
CURRENT_THUMBNAIL_FORMAT = PNG
CURRENT_THUMBNAIL_SIZE_BYTES = 720154
CURRENT_THUMBNAIL_SHA256 = 125b59b90abdc758bfd9e3068698d4c1089a2011b050756f2d98917943a75659
```

### Final

```text
FINAL_THUMBNAIL_PATH = thumbnail.png
FINAL_THUMBNAIL_DIMENSIONS = 600x600
FINAL_THUMBNAIL_FORMAT = PNG
FINAL_THUMBNAIL_SIZE_BYTES = 970481
FINAL_THUMBNAIL_SHA256 = c1d4a6d56849182a00b2474b3ba71c745216fb6a23c498b7fea0efde57c3cf5c
```

The historical artwork and square composition remain intact. A burgundy Victoria-style `FORK` panel with a double gold border was added at upper right. Following operator feedback that the first badge was not visible enough, the badge was enlarged while remaining clear of the main title and central subject. The transformation is deterministic and reproducible through `workshop_assets/build_workshop_thumbnail.ps1`; no generative AI was used.

Local QA previews were generated but are development-only:

| Preview | Size | SHA-256 | Result |
|---|---:|---|---|
| `thumbnail_preview_512.png` | 728236 bytes | `ab70b45ad754883bec3b241380b8a80ddb73eb39c5d2ae58afaae5586ea59798` | badge readable |
| `thumbnail_preview_256.png` | 191156 bytes | `3d9adb6f75f269c7d0ce9e05573b034c1d710373b684540c266dc5879ceb780a` | badge readable |
| `thumbnail_preview_128.png` | 50587 bytes | `d9116d287cfa4e7d98a1fd6b0962d42787e86180ffab5b330896b38992db3a82` | badge identifiable |

```text
THUMBNAIL_LOADABLE = yes
THUMBNAIL_FORK_BADGE_PRESENT = yes
THUMBNAIL_NO_AI_GENERATION = yes
THUMBNAIL_COMPOSITION_PRESERVED = yes
FORK_BADGE_READABLE_512 = yes
FORK_BADGE_READABLE_256 = yes
FORK_BADGE_IDENTIFIABLE_128 = yes
THUMBNAIL_SMALL_SIZE_READABILITY = PASS
```

## Metadata and descriptor audit

- `descriptor.mod` keeps the internal name `1776 - Age of Revolutions Fork` and narrows `supported_version` from the over-broad `1.*` to `1.13.*`.
- The external launcher descriptor `../1776_age_of_revolutions_fork.mod` receives the same supported-version correction without an internal rename.
- Ignored launcher metadata `.metadata/metadata.json` uses the exact operator-selected public title and `supported_game_version: 1.13.0`.
- `.metadata/metadata.json` has no relationship/dependency entry and no Workshop identifier.
- No `remote_file_id` or `publishedfileid` was added.

```text
INTERNAL_BRANDING_ARBITRARILY_CHANGED = no
SUPPORTED_VERSION = 1.13.*
WORKSHOP_ID_CREATED = no
REMOTE_FILE_ID_ADDED = no
```

## Original mod, permission and fork link

```text
ORIGINAL_MOD_NAME = 1776 - Age of Revolutions, Total Conversion Mod
ORIGINAL_AUTHOR = Tsar
ORIGINAL_WORKSHOP_URL = https://steamcommunity.com/sharedfiles/filedetails/?id=3617930953
ORIGINAL_WORKSHOP_ITEM_ID = 3617930953
ORIGINAL_SOURCE_URL_IF_DIFFERENT = not established
ORIGINAL_PERMISSION_STATUS = PUBLIC_REUSE_PERMISSION_DOCUMENTED
FORMAL_STANDALONE_LICENSE_FILE = not found
```

The original Workshop description explicitly stated that the mod was open source and its files could be used for another mod. The public texts report that permission conservatively and do not imply endorsement. The original source and author appear before any fork link in the credits.

The original Workshop URL and item identity were verified. The fetched Steam page currently displays a removed/restricted/incompatible availability banner; this does not alter the established attribution target, but the operator should review the link in Steam immediately before publication.

```text
ORIGINAL_SOURCE_LINK_VERIFIED = yes
ORIGINAL_MOD_CREDIT_PRESENT = yes
ORIGINAL_AUTHOR_PERMISSION_STATUS = PUBLIC_REUSE_PERMISSION_DOCUMENTED; NO_SEPARATE_FORMAL_LICENSE_FOUND
PUBLICATION_LEGAL_ATTRIBUTION_REVIEW_REQUIRED = no additional blocker identified from the documented permission and complete attribution
```

Fork repository intended URL:

```text
https://github.com/Malzars-sys/1776-Age-of-Revolutions
GITHUB_LINK_PUBLICLY_ACCESSIBLE = no
```

An unauthenticated request returned HTTP 404. The inaccessible GitHub link is therefore documented internally but omitted from both public Steam descriptions. It may be added manually only after the repository is publicly reachable.

## Content and feature audit

The audit covered runtime directories, localization, frontend assets, reports and merge documentation. The publication descriptions present only implemented content as current and clearly isolate partial work and future direction. The detailed classification is in `docs/workshop/WORKSHOP_FEATURE_STATUS.csv`.

Current presentation includes:

- a 1776 start and period-remodelled world setup;
- the port to Victoria 3 1.13 / The Great Wave and accumulated compatibility corrections;
- restored and corrected map, countries, scripts, events, selected journal content and localization;
- historically adapted flags and objective presentation;
- the five validated objectives: Battle for India, Age of Revolutions, Imperial Rivalries, Mercantile Republics and Learn the Game;
- the Trafalgar loading screen, mirrored Washington Crossing the Delaware menu, Age of Revolution subtitle, Cantus Firmus Monks menu theme and historical objective artwork;
- improved French and English narrative presentation.

The technology overhaul, deeper historical flavor, broader journal/event coverage, naval differentiation and long-term balance work are explicitly described as roadmap directions without dates or delivery promises.

```text
CURRENT_FEATURES_ACCURATELY_DOCUMENTED = yes
LONG_TERM_ROADMAP_SEPARATED_FROM_IMPLEMENTED_FEATURES = yes
KNOWN_LIMITATIONS_DOCUMENTED = yes
```

## Compatibility and DLC audit

```text
TESTED_VERSION = Victoria 3 1.13 / The Great Wave
LATER_VERSION_COMPATIBILITY_CLAIMED = no
REQUIRED_DLC = NONE_DECLARED
NO_DLC_REQUIRED = not asserted beyond absence of a declared hard dependency
OPTIONAL_DLC = upstream DLC-gated content may be used when available
```

Neither descriptor nor launcher metadata declares a hard DLC dependency. DLC-gated upstream behavior is guarded through feature checks. Runtime validation occurred in the maintainer's installed-DLC environment, not as a complete no-DLC matrix; the public wording preserves that distinction.

## Publication texts and packet

The following paste-ready deliverables were created:

- `docs/workshop/STEAM_WORKSHOP_DESCRIPTION_EN.txt` — recommended primary description;
- `docs/workshop/STEAM_WORKSHOP_DESCRIPTION_FR.txt` — complete French translation;
- `docs/workshop/STEAM_WORKSHOP_CHANGELOG_INITIAL.txt`;
- `docs/workshop/STEAM_WORKSHOP_CREDITS.md`;
- `docs/workshop/STEAM_WORKSHOP_PREPUBLICATION_CHECKLIST.md`;
- `docs/workshop/STEAM_WORKSHOP_PUBLICATION_PACKET.md`;
- `docs/workshop/WORKSHOP_FEATURE_STATUS.csv`;
- `docs/workshop/WORKSHOP_SHIPPING_MANIFEST.csv`.

Both descriptions disclose the unofficial fork near the beginning, credit the original author and source, distinguish implemented features from roadmap work, state the exact tested baseline, give conservative DLC wording, disclose limitations and include compact art/music credits. English is the recommended primary language; French remains a separate complete version.

Suggested tags were checked against the current Victoria 3 Workshop vocabulary and remain a human choice at publication:

```text
Alternative History
Historical
Total Conversion
Journal Entries
New Nations
Events
Map
Flags
Translation
Sound
1.13
STEAM_TAG_SELECTION = HUMAN_AT_PUBLICATION
```

## Credits and licensing QA

The detailed registers are `docs/credits/CANTUS_FIRMUS_MONKS_LICENSE.md` and `docs/credits/WORKSHOP_VISUAL_ASSETS_LICENSES.md`. The Cantus Firmus source page and its CC BY 3.0 link were rechecked on `2026-08-10`. The music is never described as public domain.

```text
CANTUS_LICENSE_VERIFIED = yes
TRAFALGAR_LICENSE_VERIFIED = yes
DELAWARE_LICENSE_VERIFIED = yes
BATTLE_FOR_INDIA_ART_LICENSE_VERIFIED = yes
AGE_OF_REVOLUTIONS_ART_LICENSE_VERIFIED = yes
IMPERIAL_RIVALRIES_ART_LICENSE_VERIFIED = yes
MERCANTILE_REPUBLICS_ART_LICENSE_VERIFIED = yes
THUMBNAIL_LICENSE_VERIFIED = yes
MUSIC_CREDITS_PASS
VISUAL_CREDITS_PASS
```

## Steam shipping recommendation

`docs/workshop/WORKSHOP_SHIPPING_MANIFEST.csv` distinguishes repository content from the later player payload. Runtime directories plus `descriptor.mod` and `thumbnail.png` ship. `.git`, `.metadata`, `docs`, `workshop_assets`, build scripts, QA material and protected research do not ship. Nothing was deleted during PREP2.

```text
WORKSHOP_SHIPPING_MANIFEST_COMPLETE = yes
TECH_RESEARCH_SHIPPING_STATUS = excluded
WORKSHOP_ASSET_PREVIEWS_SHIPPING_STATUS = excluded
REPOSITORY_DOCUMENTATION_SHIPPING_STATUS = excluded
```

## Static text and tree QA

The publication material was checked for unresolved placeholders, TODO markers, invented Workshop identifiers, unsupported compatibility claims, inaccessible public GitHub links and roadmap items presented as implemented. UTF-8 publication files are kept separate by language. The public title is reproduced exactly as supplied by the operator.

PREP2 changes are limited to the root thumbnail, supported-version metadata, credits, publication documentation and deterministic thumbnail work assets. No gameplay script, history, event, localization, GUI, map or music file was changed.

## Manual actions still required

Steam publication remains entirely manual. The operator must package only the manifest-approved payload, review the original source link, paste the descriptions and changelog, select available tags, inspect the uploaded thumbnail, accept Steam terms if prompted, publish with the intended account and record the real Workshop item ID only after Steam creates it. The private GitHub link must remain absent until publicly accessible.

## Final verdict

```text
WORKSHOP_PREP_2_THUMBNAIL_METADATA_DESCRIPTION_AND_PUBLICATION_PACKET_COMPLETE

THUMBNAIL_FORK_BADGE_PASS
THUMBNAIL_SMALL_SIZE_QA_PASS

STEAM_DESCRIPTION_EN_COMPLETE
STEAM_DESCRIPTION_FR_COMPLETE
ORIGINAL_MOD_CREDIT_COMPLETE
ORIGINAL_SOURCE_LINK_VERIFIED
FORK_GITHUB_LINK_STATUS_DOCUMENTED

CURRENT_FEATURES_ACCURATELY_DOCUMENTED
LONG_TERM_ROADMAP_SEPARATED_FROM_IMPLEMENTED_FEATURES
KNOWN_LIMITATIONS_DOCUMENTED
COMPATIBILITY_DOCUMENTED
DLC_DEPENDENCIES_AUDITED

MUSIC_CREDITS_PASS
VISUAL_CREDITS_PASS
PUBLICATION_PACKET_COMPLETE
PREPUBLICATION_CHECKLIST_COMPLETE
WORKSHOP_SHIPPING_MANIFEST_COMPLETE

NO_AUTOMATIC_STEAM_UPLOAD
NO_AUTOMATIC_COMMIT
NO_AUTOMATIC_PUSH
STASH_NAVY_3C_3_INTACT
TECH_RESEARCH_FILES_INTACT

PUBLICATION_READY = YES
NEXT_PHASE = WORKSHOP_PREP_3_FINAL_SHIPPING_PACKAGE_AND_MANUAL_STEAM_PUBLICATION
```
