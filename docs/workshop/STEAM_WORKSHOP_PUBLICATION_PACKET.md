# Steam Workshop publication packet

## Workshop title

```text
Age of revolution /Fork
```

This exact capitalization and slash placement were supplied by the operator. The internal mod name and file identifiers remain unchanged.

## Short description

```text
An unofficial Victoria 3 1.13 fork restoring a 1776 start, period countries, objectives, flags, events and a custom revolutionary frontend.
```

## Full English description

Paste the complete contents of [`STEAM_WORKSHOP_DESCRIPTION_EN.txt`](STEAM_WORKSHOP_DESCRIPTION_EN.txt). It is the recommended primary Workshop description.

## Full French description

Paste the complete contents of [`STEAM_WORKSHOP_DESCRIPTION_FR.txt`](STEAM_WORKSHOP_DESCRIPTION_FR.txt) into Steam's French-language description field if that workflow is available.

## Original mod and source

- Original mod: [1776 - Age of Revolutions, Total Conversion Mod](https://steamcommunity.com/sharedfiles/filedetails/?id=3617930953)
- Original author: **Tsar**
- Original Workshop item: `3617930953`
- Separate original source repository: not established.
- The original Workshop description publicly permitted reuse of its files; no separate formal license file was found.

## Fork repository

- Intended link: `https://github.com/Malzars-sys/1776-Age-of-Revolutions`
- Current unauthenticated status: `HTTP 404 / NOT PUBLICLY ACCESSIBLE`
- Publication action: omit this link from the public Steam description until the repository is public. PREP2 does not change repository visibility.

## Compatibility

- Tested game version: `Victoria 3 1.13 / The Great Wave`
- Internal descriptor: `supported_version="1.13.*"`
- Launcher metadata: `supported_game_version = 1.13.0`
- Later versions: not claimed.
- Other overhaul mods: not recommended without a dedicated compatibility patch.

## DLC requirements

- `REQUIRED_DLC = NONE_DECLARED`
- `.metadata/metadata.json` contains no relationships.
- `descriptor.mod` contains no dependency field.
- DLC-gated upstream content is protected by game feature checks.
- Validation occurred in the maintainer's current DLC environment; a complete no-DLC runtime matrix was not performed.

## Suggested Steam tags

Verified current Victoria 3 categories suitable for this fork:

`Alternative History`, `Historical`, `Total Conversion`, `Journal Entries`, `New Nations`, `Events`, `Map`, `Flags`, `Translation`, `Sound`, `1.13`

Tags are suggestions only and must be selected manually from the actual publication UI.

## Thumbnail

- Final Workshop path: `thumbnail.png`
- Format: PNG
- Dimensions: `600x600`
- Size: `970481` bytes
- SHA-256: `c1d4a6d56849182a00b2474b3ba71c745216fb6a23c498b7fea0efde57c3cf5c`
- Badge: enlarged burgundy `FORK` panel with double gold border at upper right.
- Original preserved at: `workshop_assets/source/thumbnail_before_fork_badge.png`
- QA previews: `workshop_assets/previews/thumbnail_preview_512.png`, `thumbnail_preview_256.png`, `thumbnail_preview_128.png`
- Transformation: deterministic local System.Drawing script; no AI generation.

## Credits

Use the compact credits already embedded in both descriptions. The full register is [`STEAM_WORKSHOP_CREDITS.md`](STEAM_WORKSHOP_CREDITS.md), supported by the detailed visual and music records under `docs/credits/`.

## Known limitations

- Flavor depth remains uneven between countries.
- Some legacy material still originates from older Victoria 3 versions.
- A complete 1776 technology-tree redesign is not yet delivered.
- Some historical flags and systems require practical engine approximations.
- Future Victoria 3 updates may require compatibility work.

## Long-term roadmap

The public roadmap is deliberately separated from implemented features:

- deeper political and historical setup;
- more country-specific journals, events and situations;
- a genuinely 1776-oriented technology and industrial progression;
- more coherent and differentiated historical navies;
- continued economic, institutional and military balancing;
- continued English/French localization and visual polish.

No date or delivery promise is attached to these directions.

## Initial changelog

Paste the contents of [`STEAM_WORKSHOP_CHANGELOG_INITIAL.txt`](STEAM_WORKSHOP_CHANGELOG_INITIAL.txt) into the initial change note where appropriate.

## Shipping manifest

Follow [`WORKSHOP_SHIPPING_MANIFEST.csv`](WORKSHOP_SHIPPING_MANIFEST.csv). The player payload should contain runtime directories and the two root runtime files only; repository documents, sources, build scripts, QA previews, `.git`, `.metadata` and protected research should not ship.

## Publication checklist

Follow [`STEAM_WORKSHOP_PREPUBLICATION_CHECKLIST.md`](STEAM_WORKSHOP_PREPUBLICATION_CHECKLIST.md). PREP2 performs no upload and creates no Workshop ID.
