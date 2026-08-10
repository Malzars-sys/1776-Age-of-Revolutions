# Steam package size and exclusion report

Snapshot date: `2026-08-10`  
Build path: `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\workshop_build\Age_of_Revolution_Fork`

The source snapshot includes the Git repository metadata and all development material. The Steam payload contains only the runtime files selected by `WORKSHOP_SHIPPING_MANIFEST.csv`. The statistics were captured by the final reproducible build before this prose report was added.

## Summary

| Measure | Files | Bytes | MiB |
|---|---:|---:|---:|
| Full working directory | 5,425 | 326,604,028 | 311.47 |
| Steam payload | 855 | 112,723,605 | 107.50 |
| Excluded total / reduction | 4,570 | 213,880,423 | 203.97 |

```text
SPACE_REDUCTION_PERCENT = 65.4862
FILES_HASH_MISMATCH = 0
```

## Excluded categories

Categories are mutually exclusive in this report, so their sizes add cleanly to the excluded total.

| Category | Files | Bytes | MiB |
|---|---:|---:|---:|
| Documentation, reports and research | 315 | 7,852,953 | 7.49 |
| Workshop source assets | 8 | 27,316,677 | 26.05 |
| Workshop previews | 9 | 16,165,226 | 15.42 |
| Development scripts | 3 | 26,977 | 0.03 |
| Git metadata | 4,226 | 161,762,141 | 154.27 |
| Other excluded development data | 9 | 756,449 | 0.72 |

The four Markdown files found inside `common/` are documentation, not Victoria 3 runtime data, and are included in the excluded documentation total:

- `common/amendments/amendments.md`
- `common/dynamic_country_names/dynamic_country_names.md`
- `common/journal_entries/journal_entries.md`
- `common/objectives/objectives.md`

## Top 30 source files by size

| Path | Bytes | MiB | Classification | Ship |
|---|---:|---:|---|:---:|
| `music/age_of_revolution/cantus_firmus_monks_menu_30m.ogg` | 43598540 | 41.58 | REQUIRED_RUNTIME | YES |
| `.git/objects/e6/6ddec72d0ee706f1226b28f2890b0fd878467e` | 43467700 | 41.45 | GIT_METADATA | NO |
| `gfx/loadingscreens/aor_trafalgar_loading.dds` | 11060752 | 10.55 | REQUIRED_RUNTIME | YES |
| `gfx/interface/illustrations/frontend/age_of_revolution_frontend_bg.dds` | 11060752 | 10.55 | REQUIRED_RUNTIME | YES |
| `workshop_assets/source/prise_de_la_bastille_houel_gallica.jpg` | 8520313 | 8.13 | WORKSHOP_SOURCE_ASSET | NO |
| `.git/objects/99/d3c51f8500ad8e2f6468064061090e7c72564b` | 8491523 | 8.10 | GIT_METADATA | NO |
| `workshop_assets/source/canaletto_bucintoro_google_art_project.jpg` | 5729621 | 5.46 | WORKSHOP_SOURCE_ASSET | NO |
| `.git/objects/87/6a7758e866d066ebbd56bf4428ced206d414db` | 5716052 | 5.45 | GIT_METADATA | NO |
| `gfx/interface/icons/objectives/aor_battle_for_india_illu.dds` | 5508516 | 5.25 | REQUIRED_RUNTIME | YES |
| `gfx/interface/icons/objectives/aor_imperial_rivalries_illu.dds` | 5508516 | 5.25 | REQUIRED_RUNTIME | YES |
| `gfx/interface/icons/objectives/aor_age_of_revolutions_illu.dds` | 5508516 | 5.25 | REQUIRED_RUNTIME | YES |
| `gfx/interface/icons/objectives/aor_mercantile_republics_illu_dis.dds` | 5508516 | 5.25 | REQUIRED_RUNTIME | YES |
| `gfx/interface/icons/objectives/aor_mercantile_republics_illu.dds` | 5508516 | 5.25 | REQUIRED_RUNTIME | YES |
| `.git/objects/17/a1fb7b193f1f2042901aa41c1792f7568384de` | 5476567 | 5.22 | GIT_METADATA | NO |
| `.git/objects/cf/941a6e8628c4f3e0d1a618291d2cd004be03f3` | 5237138 | 4.99 | GIT_METADATA | NO |
| `.git/objects/2f/128b90050bee1d8d5175dd0bf1d46e1187bab3` | 5140039 | 4.90 | GIT_METADATA | NO |
| `.git/objects/e6/4f0988dfa63c651c16ae7db7a130bbf41a0d40` | 5127355 | 4.89 | GIT_METADATA | NO |
| `workshop_assets/source/washington_crossing_delaware.png` | 4846473 | 4.62 | WORKSHOP_SOURCE_ASSET | NO |
| `.git/objects/84/bc12f1bd0decdb06d0433a0df89e9f81861bd2` | 4835084 | 4.61 | GIT_METADATA | NO |
| `workshop_assets/source/Cantus_Firmus_Monks_Doug_Maxwell.mp3` | 4022020 | 3.84 | WORKSHOP_SOURCE_ASSET | NO |
| `.git/objects/6d/f06a6b266a2724c7ecab4d3eabf0f77dd24fe1` | 3721073 | 3.55 | GIT_METADATA | NO |
| `.git/objects/00/dd8ce3827ce97146e8feacea16b2b2cae77281` | 3720272 | 3.55 | GIT_METADATA | NO |
| `.git/objects/a4/ed2772f98bf444d2bcf4f42161faf0dd7e9e2b` | 3585173 | 3.42 | GIT_METADATA | NO |
| `workshop_assets/previews/age_of_revolution_frontend_bg_mirrored_preview.png` | 3485915 | 3.32 | WORKSHOP_PREVIEW | NO |
| `.git/objects/d8/21ba8b79e0201366044f8750f54478612d37cd` | 3482232 | 3.32 | GIT_METADATA | NO |
| `.git/objects/a1/526e720d9c77d2d125865a28207d98fe2c28d9` | 3426791 | 3.27 | GIT_METADATA | NO |
| `.git/objects/2a/77b85272a80aa9c8d7b1a4fce86f250e70609b` | 3356560 | 3.20 | GIT_METADATA | NO |
| `workshop_assets/previews/aor_trafalgar_loading_preview.png` | 3300377 | 3.15 | WORKSHOP_PREVIEW | NO |
| `.git/objects/e8/451b3f8d881928e86b9822796baa450b6e0e79` | 3292410 | 3.14 | GIT_METADATA | NO |
| `.git/objects/9c/6118b8e8b14c8613174c393ae8b31a8165a7f3` | 3078866 | 2.94 | GIT_METADATA | NO |

## Top 30 Steam files by size

| Path | Bytes | MiB | Classification |
|---|---:|---:|---|
| `music/age_of_revolution/cantus_firmus_monks_menu_30m.ogg` | 43598540 | 41.58 | REQUIRED_RUNTIME |
| `gfx/loadingscreens/aor_trafalgar_loading.dds` | 11060752 | 10.55 | REQUIRED_RUNTIME |
| `gfx/interface/illustrations/frontend/age_of_revolution_frontend_bg.dds` | 11060752 | 10.55 | REQUIRED_RUNTIME |
| `gfx/interface/icons/objectives/aor_mercantile_republics_illu.dds` | 5508516 | 5.25 | REQUIRED_RUNTIME |
| `gfx/interface/icons/objectives/aor_imperial_rivalries_illu.dds` | 5508516 | 5.25 | REQUIRED_RUNTIME |
| `gfx/interface/icons/objectives/aor_age_of_revolutions_illu.dds` | 5508516 | 5.25 | REQUIRED_RUNTIME |
| `gfx/interface/icons/objectives/aor_battle_for_india_illu.dds` | 5508516 | 5.25 | REQUIRED_RUNTIME |
| `gfx/interface/icons/objectives/aor_mercantile_republics_illu_dis.dds` | 5508516 | 5.25 | REQUIRED_RUNTIME |
| `music/age_of_revolution/cantus_firmus_monks.ogg` | 2437765 | 2.32 | REQUIRED_RUNTIME |
| `gfx/coat_of_arms/textured_emblems/te_peacock_india_mod.dds` | 1659008 | 1.58 | REQUIRED_RUNTIME |
| `gfx/coat_of_arms/textured_emblems/te_coa_portugal_india.dds` | 1383484 | 1.32 | REQUIRED_RUNTIME |
| `thumbnail.png` | 970481 | 0.93 | REQUIRED_RUNTIME |
| `gfx/coat_of_arms/colored_emblems/ce_letter_a_serif.dds` | 844536 | 0.81 | REQUIRED_RUNTIME |
| `gfx/coat_of_arms/textured_emblems/te_peacock_mayurbhanj.dds` | 524448 | 0.50 | REQUIRED_RUNTIME |
| `gfx/interface/icons/law_icons/regulation_acts.dds` | 485828 | 0.46 | REQUIRED_RUNTIME |
| `common/history/states/00_states.txt` | 478466 | 0.46 | REQUIRED_RUNTIME |
| `gfx/interface/icons/law_icons/merchant_banks.dds` | 427060 | 0.41 | REQUIRED_RUNTIME |
| `gfx/interface/icons/law_icons/merchant_republic.dds` | 364944 | 0.35 | REQUIRED_RUNTIME |
| `gfx/interface/icons/company_icons/historical_company_icons/nl_voc.dds` | 262272 | 0.25 | REQUIRED_RUNTIME |
| `common/flag_definitions/00_flag_definitions.txt` | 239536 | 0.23 | REQUIRED_RUNTIME |
| `common/history/buildings/00_west_europe.txt` | 192655 | 0.18 | REQUIRED_RUNTIME |
| `common/defines/00_defines.txt` | 173634 | 0.17 | REQUIRED_RUNTIME |
| `common/on_actions/00_code_on_actions.txt` | 169700 | 0.16 | REQUIRED_RUNTIME |
| `common/ai_strategies/00_default_strategy.txt` | 159512 | 0.15 | REQUIRED_RUNTIME |
| `events/agitators_events/agitators_election_events.txt` | 153305 | 0.15 | REQUIRED_RUNTIME |
| `common/history/buildings/01_south_europe.txt` | 143873 | 0.14 | REQUIRED_RUNTIME |
| `events/agitators_events/revolution_events_02.txt` | 127480 | 0.12 | REQUIRED_RUNTIME |
| `events/soi_events/00_lobbies_events_04.txt` | 120362 | 0.11 | REQUIRED_RUNTIME |
| `common/history/buildings/11_east_asia.txt` | 102539 | 0.10 | REQUIRED_RUNTIME |
| `common/history/military_formations/00_military_formations_europe.txt` | 98089 | 0.09 | REQUIRED_RUNTIME |

## Duplicate and pollution audit

- Source MP3: excluded; final OGG files only are shipped.
- Source PNG/JPG and final DDS: source images excluded; final DDS files only are shipped.
- Original thumbnail and preview derivatives: excluded; only final root `thumbnail.png` ships.
- Development scripts: excluded.
- Documentation and protected technology research: excluded.
- External launcher `.mod` descriptor: excluded.

```text
DEVELOPMENT_POLLUTION_FOUND = 0
RUNTIME_FILE_HASH_MISMATCHES = 0
```
