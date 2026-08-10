# Manual Steam Workshop publication steps

These instructions prepare the operator to publish the already validated external build. They do not authorize an automatic upload.

## Paths that must not be confused

- Development repository: `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`
- Steam build to upload: `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\workshop_build\Age_of_Revolution_Fork`
- Existing development registration: `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_age_of_revolutions_fork.mod`

Never repoint or overwrite the existing development registration for publication. Never select the repository directory in an uploader.

## Create a separate local launcher registration

With Victoria 3 and the Paradox Launcher closed, manually create:

```text
C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\age_of_revolution_fork_steam_build.mod
```

with exactly this local-only content:

```text
name="Age of revolution /Fork [Steam Build]"
path="C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/workshop_build/Age_of_Revolution_Fork"
supported_version="1.13.*"
tags={
    "Total Conversion"
}
```

The `[Steam Build]` suffix distinguishes the local launcher entry. The public Workshop title must still be exactly `Age of revolution /Fork`. This temporary `.mod` registration is outside the build and must never be uploaded.

## Verify the separate entry

1. Open the Paradox Launcher.
2. Open the Victoria 3 mod-management page (`Mods`, then `All installed mods`, wording may vary slightly by launcher language).
3. Confirm that both the development entry and the distinct `[Steam Build]` entry are visible.
4. Select the `[Steam Build]` entry only.
5. Confirm its version is `1.13.*` and its thumbnail shows the large `FORK` badge.
6. If the launcher cannot distinguish the two entries or does not point the new entry to the external build, stop. Do not repoint the development descriptor and do not publish.

## Open the uploader without publishing yet

1. Open the launcher's mod tools/upload workflow (`Mod tools` / `Upload mod`, depending on launcher language).
2. Choose `Age of revolution /Fork [Steam Build]` as the local source.
3. Verify that the selected content path is the external `workshop_build\Age_of_Revolution_Fork` directory, not the Git repository.
4. Verify the displayed public title is exactly `Age of revolution /Fork`; remove the local `[Steam Build]` suffix from the public title field.
5. Verify the 600×600 preview is `thumbnail.png` and the `FORK` badge is visible.
6. Do not invent or enter a Workshop item ID. Steam must create the real ID.

## Paste canonical publication content

- Primary English description: `docs/workshop/STEAM_WORKSHOP_DESCRIPTION_EN.txt`
- French description: `docs/workshop/STEAM_WORKSHOP_DESCRIPTION_FR.txt`
- Initial change note: `docs/workshop/STEAM_WORKSHOP_CHANGELOG_INITIAL.txt`
- Original source credit: `https://steamcommunity.com/sharedfiles/filedetails/?id=3617930953`
- Original author: `Tsar`

Do not add the fork GitHub link while it remains inaccessible to unauthenticated visitors.

Select only tags actually offered by the current Victoria 3 Workshop interface. PREP2 suggestions are `Alternative History`, `Historical`, `Total Conversion`, `Journal Entries`, `New Nations`, `Events`, `Map`, `Flags`, `Translation`, `Sound`, and `1.13`.

## Final human review and publication

1. Review the complete title, description, thumbnail, compatibility, tags and credits in the upload preview.
2. Confirm that the uploader is using the external build and that no `docs`, `workshop_assets`, `.git`, `.metadata`, scripts, sources or previews appear in its file list.
3. Choose the intended visibility deliberately; use a non-public visibility first if the interface offers it and a private validation pass is desired.
4. Accept the Steam Workshop legal agreement if prompted.
5. Click publish/upload manually.
6. Record the real Workshop item ID returned by Steam.
7. Only after Steam creates the item may its real ID be recorded in the launcher-managed publication metadata.
8. Inspect the live Workshop page from an unauthenticated view before making it broadly visible.

## After publication

The temporary `age_of_revolution_fork_steam_build.mod` registration may be removed manually after publication if it is no longer needed. Removing that registration does not remove the external build or the development repository. Do not delete either directory as part of this instruction.

```text
MANUAL_STEAM_PUBLICATION_ONLY = YES
AUTOMATIC_UPLOAD_PERFORMED = NO
DEVELOPMENT_REGISTRATION_OVERWRITTEN = NO
```
