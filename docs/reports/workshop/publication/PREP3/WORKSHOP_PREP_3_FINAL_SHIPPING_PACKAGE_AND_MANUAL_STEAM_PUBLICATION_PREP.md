# WORKSHOP PREP 3 — Final shipping package and manual Steam publication preparation

Date: `2026-08-10`  
Branch: `workshop-prep-frontend-objectives`  
Baseline HEAD: `bc65900483ceeb39070878668cb732bf96580339`  
Steam publication performed: `NO`

## Outcome

A minimal player-facing copy was built outside the development repository at:

```text
C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\workshop_build\Age_of_Revolution_Fork
```

It contains only the runtime directories selected by the PREP2 shipping manifest, `descriptor.mod` and the final `thumbnail.png`. The Git repository remains the development source of truth and was not copied wholesale.

## Preconditions and protected state

PREP2 was manually committed as `bc65900483ceeb39070878668cb732bf96580339`. Its report contains every required ready verdict, including `PUBLICATION_READY = YES`, descriptions EN/FR, source credit, license checks, thumbnail QA and shipping manifest completion.

The PREP3 preflight found a clean tracked worktree, an empty index and exactly the seven protected technology-research files as untracked content.

```text
PREFLIGHT_BRANCH = workshop-prep-frontend-objectives
PREFLIGHT_HEAD = bc65900483ceeb39070878668cb732bf96580339
PREFLIGHT_TRACKED_WORKTREE = clean
PREFLIGHT_INDEX = empty
PREFLIGHT_UNTRACKED_NON_PROTECTED = 0
```

The NAVY-3C-3 stash was neither read nor modified:

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
STASH_NAVY_3C_3_HASH = 518df704fa14599c0f254fae13859210663dd976
```

## Build safety and source manifest

`docs/workshop/WORKSHOP_SHIPPING_MANIFEST.csv` remained the authority for ship/no-ship decisions. The target directory did not exist at the first audit, so no unknown existing content required operator review.

The reproducible builder is `tools/workshop/build_steam_package.ps1`. It:

- validates that the destination is exactly under `workshop_build\Age_of_Revolution_Fork`;
- refuses to clean an existing build without a matching external owner marker;
- records the previous generated build before targeted cleanup;
- reads only manifest entries marked `YES`;
- rejects documentation, sources, previews, scripts, archives and protected research;
- copies files without content transformation;
- validates every source/destination SHA-256;
- verifies the descriptor and exact PREP2 thumbnail hash;
- scans text payload files for credential patterns, personal paths and Workshop IDs;
- creates no upload and executes no mutating Git command.

Four `.md` documentation files physically located inside `common/` were excluded under the explicit no-documentation rule. No runtime extension or asset was excluded from a ship directory.

## Package inventory

Package root:

```text
common/
events/
gfx/
gui/
localization/
map_data/
music/
descriptor.mod
thumbnail.png
```

`Changelog.txt`, `Source.txt`, `.gitignore`, `.metadata`, the external launcher registration and every repository-only directory are absent.

The exact 855-file inventory is `docs/workshop/WORKSHOP_FINAL_SHIPPING_FILELIST.csv`.

## Size and exclusions

The measured source snapshot includes Git metadata and development material. Values were captured by the final build before this narrative report was added.

```text
SOURCE_REPO_SIZE = 326604028 bytes (311.47 MiB)
STEAM_PACKAGE_SIZE = 112723605 bytes (107.50 MiB)
REDUCTION_PERCENT = 65.4862

SOURCE_FILE_COUNT = 5425
STEAM_FILE_COUNT = 855

DOCS_EXCLUDED_SIZE = 7852953 bytes (7.49 MiB)
WORKSHOP_SOURCES_EXCLUDED_SIZE = 27316677 bytes (26.05 MiB)
PREVIEWS_EXCLUDED_SIZE = 16165226 bytes (15.42 MiB)
SCRIPTS_EXCLUDED_SIZE = 26977 bytes (0.03 MiB)
GIT_EXCLUDED_SIZE = 161762141 bytes (154.27 MiB)
OTHER_EXCLUDED_DEVELOPMENT_SIZE = 756449 bytes (0.72 MiB)
EXCLUDED_TOTAL_SIZE = 213880423 bytes (203.97 MiB)
```

The full category accounting and both top-30 tables are in `docs/workshop/WORKSHOP_PACKAGE_SIZE_REPORT.md`.

## Byte identity and reproducibility

Every copied file was rehashed independently after the script completed:

```text
FILES_COPIED = 855
FILES_HASH_MATCH = 855
FILES_HASH_MISMATCH = 0
RUNTIME_FILE_HASH_MISMATCHES = 0
```

The final script was executed twice against the same source. Both runs produced the same relative file list, SHA-256 values and byte total:

```text
FINAL_FILELIST_SHA256_PASS_1 = 66985993b4175d1e32d3582925d3a94287a597520a7938e1672fad0249c744c1
FINAL_FILELIST_SHA256_PASS_2 = 66985993b4175d1e32d3582925d3a94287a597520a7938e1672fad0249c744c1
PACKAGE_BUILD_REPRODUCIBLE = yes
```

## Victoria 3 structure and PREP1 assets

All expected PREP1 runtime assets are present, including:

- Trafalgar loading DDS;
- mirrored Delaware frontend DDS and frontend GUI override;
- five objective DDS states;
- 30-minute Cantus Firmus menu OGG and its main-theme definitions;
- English/French frontend and objective localization;
- period coat-of-arms and flag definitions, including the VOC icon.

A direct reference scan found 127 literal `gfx/` or `music/` references. Eleven are mod-local assets and all eleven exist in the package. The remaining 116 point to inherited vanilla assets supplied by Victoria 3 rather than duplicated by the mod.

```text
PREP1_EXPECTED_MISSING = 0
SOURCE_LOCAL_DIRECT_REFERENCES = 11
SOURCE_LOCAL_MISSING_FROM_PACKAGE = 0
VANILLA_INHERITED_REFERENCES = 116
```

No new Victoria 3 runtime was necessary because every shipped runtime file is byte-identical to the already runtime-validated source.

## Descriptor and thumbnail

```text
DESCRIPTOR_PRESENT = yes
DESCRIPTOR_SUPPORTED_VERSION = 1.13.*
REMOTE_FILE_ID_PRESENT = no
PUBLISHEDFILEID_PRESENT = no
EXTERNAL_LAUNCHER_DESCRIPTOR_COPIED = no

THUMBNAIL_PRESENT = yes
THUMBNAIL_FORMAT = PNG
THUMBNAIL_DIMENSIONS = 600x600
THUMBNAIL_SHA256 = c1d4a6d56849182a00b2474b3ba71c745216fb6a23c498b7fea0efde57c3cf5c
THUMBNAIL_FINAL_PASS
DESCRIPTOR_FINAL_PASS
```

## Pollution, credentials and identifiers

The package was independently searched for prohibited extensions and directory names. Text files were scanned for credential-assignment patterns, authorization headers, private-user markers, local `C:\Users\` paths and Workshop ID fields. The benign game comment `token concessions` was not a credential assignment and does not constitute a secret hit.

```text
DEVELOPMENT_POLLUTION_FOUND = 0
POTENTIAL_SECRET_HITS = 0
LOCAL_DEVELOPER_PATH_LEAKS = 0
NEW_FORK_WORKSHOP_ID_PRESENT = no
ORIGINAL_WORKSHOP_ID_IN_RUNTIME_PAYLOAD = no
```

## Manual launcher preparation

The installed launcher currently registers the development mod through `mod\1776_age_of_revolutions_fork.mod`, which points to the repository. That descriptor was not changed or copied.

`docs/workshop/MANUAL_STEAM_PUBLICATION_STEPS.md` instructs the operator to create a separate local-only `.mod` registration pointing to the external build. The local entry uses `[Steam Build]` for distinction, while the public title remains exactly `Age of revolution /Fork`. If the launcher cannot confirm the external content path, publication must stop rather than repointing the development registration.

The canonical PREP2 English/French descriptions and concise changelog remain unchanged. The original source credit remains `Tsar` and Workshop item `3617930953`. The private fork GitHub link remains absent.

## Git and publication boundary

PREP3 creates documentation and the packaging tool in Git, but does not stage, commit or push them. The physical build and its generated sidecar audit files are outside the repository. No Steam, launcher, SteamCMD or Workshop upload action occurred.

## Final verdict

```text
WORKSHOP_PREP_3_FINAL_SHIPPING_PACKAGE_AND_MANUAL_STEAM_PUBLICATION_PREP_COMPLETE

STEAM_PACKAGE_CREATED
STEAM_PACKAGE_MINIMAL
STEAM_PACKAGE_HASH_VALIDATED
STEAM_PACKAGE_REPRODUCIBLE

DOCUMENTATION_EXCLUDED
SOURCE_ASSETS_EXCLUDED
PREVIEWS_EXCLUDED
BUILD_SCRIPTS_EXCLUDED
GIT_METADATA_EXCLUDED
TECH_RESEARCH_EXCLUDED

DEVELOPMENT_POLLUTION_FOUND = 0
FILES_HASH_MISMATCH = 0
POTENTIAL_SECRET_HITS = 0
LOCAL_DEVELOPER_PATH_LEAKS = 0

THUMBNAIL_FINAL_PASS
DESCRIPTOR_FINAL_PASS

PUBLICATION_TEXTS_READY
ORIGINAL_SOURCE_CREDIT_READY

NO_AUTOMATIC_STEAM_UPLOAD
NO_AUTOMATIC_COMMIT
NO_AUTOMATIC_PUSH

STASH_NAVY_3C_3_INTACT
TECH_RESEARCH_FILES_INTACT
BJECT_ABSENT = yes

READY_FOR_MANUAL_STEAM_PUBLICATION = YES

NEXT_ACTION =
MANUAL_STEAM_WORKSHOP_PUBLICATION_BY_OPERATOR
```
