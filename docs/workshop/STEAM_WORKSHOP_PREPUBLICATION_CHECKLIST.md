# Steam Workshop pre-publication checklist

## Static preparation complete

- [x] Workshop title fixed as `Age of revolution /Fork`.
- [x] Original mod and author credited before the fork repository.
- [x] Unofficial-fork disclosure appears near the beginning of both descriptions.
- [x] Original Workshop URL identified and reachable.
- [x] Original public file-reuse permission documented without inventing approval.
- [x] English description complete and paste-ready.
- [x] French description complete and paste-ready.
- [x] Current features separated from partial work and long-term roadmap.
- [x] Known player-facing limitations documented.
- [x] Tested compatibility restricted to Victoria 3 1.13 / The Great Wave.
- [x] No hard DLC dependency declared; DLC audit wording is conservative.
- [x] Suggested tags verified against the current Victoria 3 Workshop vocabulary.
- [x] Root thumbnail retains the existing artwork and carries a visible `FORK` badge.
- [x] Badge is readable at 512 and 256 px and identifiable at 128 px.
- [x] Original thumbnail preserved byte-for-byte in `workshop_assets/source/`.
- [x] No AI-generated image used.
- [x] Cantus Firmus attribution and CC BY 3.0 link present.
- [x] Integrated historical artwork rights reviewed and credited.
- [x] No placeholder, `TODO`, invented Workshop ID or `remote_file_id` added.
- [x] Shipping manifest excludes development assets, QA reports and protected research.
- [x] Seven protected technology-research files remain untracked and excluded.
- [x] Protected NAVY-3C-3 stash remains intact and unapplied.
- [x] No Victoria 3 runtime required or performed during PREP2.
- [x] No Steam upload, Workshop item creation, GitHub release or visibility change performed.

## Human actions at publication time

- [ ] Open the Victoria 3 launcher publishing workflow with the intended Steam account.
- [ ] Confirm the title is exactly `Age of revolution /Fork`.
- [ ] Paste the English description as the primary Workshop text.
- [ ] Add the French description through Steam's language-specific description workflow if available.
- [ ] Select only tags exposed by the launcher/Workshop at publication time.
- [ ] Confirm no DLC is marked required unless the launcher forces a dependency discovered during manual packaging.
- [ ] Use `thumbnail.png` as the primary preview image.
- [ ] Ensure the shipping payload follows `WORKSHOP_SHIPPING_MANIFEST.csv`.
- [ ] Do not include `docs/`, `workshop_assets/`, `.git/`, `.metadata/` or protected research in the player payload.
- [ ] Review the uploaded preview and description before changing visibility.
- [ ] Accept the Steam Workshop legal agreement if prompted.
- [ ] Publish manually; record the generated Workshop item ID only after Steam creates it.
- [ ] Add the fork GitHub link only after an unauthenticated browser can access it.

## Suggested tags

Select at publication time from the current Victoria 3 Workshop list:

- `Alternative History`
- `Historical`
- `Total Conversion`
- `Journal Entries`
- `New Nations`
- `Events`
- `Map`
- `Flags`
- `Translation`
- `Sound`
- `1.13`

`STEAM_TAG_SELECTION = HUMAN_AT_PUBLICATION`
