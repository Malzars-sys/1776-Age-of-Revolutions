# CLEANUP-2D-4 — 1776 Generals Historical Research Completion

Status: **RESEARCH COMPLETE / IMPLEMENTATION NOT STARTED**

## Baseline

- Reference date: **1776-01-01**
- Current post-2D3 land formations: **214**
- Tags represented: **175**
- Fixed named historical assignments: **18**
- Procedural / collective / structural closures: **196**
- Naval commanders: **out of scope**
- Gameplay files modified: **NO**
- Commit/push: **NO**

## Accepted named assignments

- `PLC` `cleanup2d3e_r1_plc_land_1` → **Franciszek Ksawery Branicki** — `HIGHER_COMMAND_ABSTRACTION`; mapping MEDIUM
- `AUS` `cleanup2d3b_aus_land_3` → **Andreas Hadik** — `HIGHER_COMMAND_ABSTRACTION`; mapping MEDIUM_LOW
- `AUS` `cleanup2d3b_aus_land_1` → **Franz Moritz von Lacy** — `HIGHER_COMMAND_ABSTRACTION`; mapping MEDIUM_LOW
- `GBR` `cleanup2d3b_gbr_land_2` → **William Howe** — `THEATRE_COMMAND`; mapping HIGH
- `RUS` `cleanup2d3b_rus_land_4` → **Pyotr Rumyantsev** — `HIGHER_COMMAND_ABSTRACTION`; mapping MEDIUM
- `SPA` `cleanup2d3b_spa_land_2` → **Antonio Ricardos** — `NAMED_MILITARY_OFFICEHOLDER`; mapping MEDIUM_LOW
- `SPA` `cleanup2d3b_spa_land_1` → **Alejandro O'Reilly** — `NAMED_MILITARY_OFFICEHOLDER`; mapping MEDIUM_LOW
- `USA` `cleanup2d3b_usa_land_1` → **George Washington** — `FORMATION_COMMAND`; mapping HIGH
- `PAN` `FaujiKhas` → **Jassa Singh Ahluwalia** — `COLLECTIVE_HIGH_COMMAND`; mapping MEDIUM
- `BIC` `Bengal_Army` → **John Clavering** — `HIGHER_COMMAND_ABSTRACTION`; mapping MEDIUM_HIGH
- `MARATH` `cleanup2d3b_marath_land_2` → **Haripant Phadke** — `FORMATION_COMMAND`; mapping HIGH
- `MARATH` `cleanup2d3b_marath_land_1` → **Tukoji Holkar** — `HOUSEHOLD_FORCE_HIGH_COMMAND`; mapping MEDIUM
- `GWA` `GwaliorArmy` → **Mahadji Shinde** — `FORMATION_COMMAND`; mapping HIGH
- `MYS` `cleanup2d3b_mys_land_2` → **Hyder Ali** — `FORMATION_COMMAND`; mapping HIGH
- `TRA` `TravancoreArmy` → **Eustachius De Lannoy** — `FORMATION_COMMAND`; mapping HIGH
- `MUG` `MughalArmy` → **Mirza Najaf Khan** — `FORMATION_COMMAND`; mapping HIGH
- `BUR` `tatmadaw` → **Maha Thiha Thura** — `THEATRE_COMMAND`; mapping HIGH
- `SIA` `cleanup2d3b_sia_land_1` → **Chao Phraya Chakri (Thongduang)** — `THEATRE_COMMAND`; mapping HIGH

## Completion test

- 214 current formations found in recovered post-2D3 audit.
- 214 unique `(tag, formation)` rows written.
- 214/214 rows contain an implementation decision.
- 18/214 fixed historical identities.
- 196/214 non-named closures, explicitly marked procedural/collective/structural rather than fabricated.
- Oceania closed with zero current land formations.
- Admirals intentionally excluded.

## Git staging commands

```powershell
Set-Location "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork"
git switch cleanup-post-release
git status --short

New-Item -ItemType Directory -Force "docs\research\military" | Out-Null
New-Item -ItemType Directory -Force "docs\prompts" | Out-Null

# Copy the generated files, then:
git add docs/research/military/GENERALS_1776_MASTER.csv `
        docs/research/military/GENERALS_1776_SOURCES.md `
        docs/research/military/GENERALS_1776_COMMAND_STRUCTURE_NOTES.md `
        docs/research/military/GENERALS_1776_REJECTED_CANDIDATES.csv `
        docs/research/military/CLEANUP2D4_GENERALS_1776_RESEARCH_COMPLETE.md `
        docs/prompts/CLEANUP2D4_GENERALS_CODEX_PROMPT.md

git diff --cached --name-only
git diff --cached --check
git status --short
```

Do not commit or push automatically.
