# RULERS_1776_BATCH2_EUROPE_DESIGN_NOTES

## Purpose

This packet is the historical source of truth for **CLEANUP-2B-2 — Europe Batch 2**.

Codex should not redo general web research. It should use this packet for historical identity/date/title decisions and consult the local fork, vanilla 1.13, hotfix source and logs only for Victoria 3 implementation details.

## Batch scope

The CSV contains:
- straightforward dynastic rulers;
- two republican heads of state (Venice and Genoa);
- the Pope and the Grand Master of Malta;
- Moldavian and Wallachian Phanariot princes;
- one regency/co-government case (Saxe-Meiningen);
- three shared-monarch structural cases (Hanover, Holstein, Schleswig).

## Global rules

1. Reference date is **1776-01-01**.
2. Exact date means exact date. Approximate chronology stays approximate.
3. Never invent a day/month from a birth year.
4. Never upgrade a 1776 title to a later Napoleonic/19th-century title.
5. Do not transform republics into monarchies just to make the character system convenient.
6. Shared monarch means the same historical person. Avoid duplicate unrelated identities.
7. Do not alter map borders, ownership or subject status merely to fit a character.
8. If a tag’s political meaning in the fork conflicts with the packet’s historical polity, stop that tag and report it instead of forcing the ruler.

## Critical title traps

- BAV: **Elector**, not King.
- SAX: **Elector Frederick Augustus III**, not later King Frederick Augustus I.
- BAD: **Margrave**, not Grand Duke.
- HEK/HES: **Landgrave**, not Grand Duke.
- LIP: **Count**, not Prince.
- TUS: **Grand Duke Pietro Leopoldo**, not Emperor Leopold II.
- MOD: Francesco III, not Ercole III.
- GEN/VEN: **Doge**, keep republican laws.
- PAP: **Pope Pius VI**.
- MLT: **Grand Master**.
- MOL/WAL: Prince/Hospodar under Ottoman suzerainty, if the fork represents that relationship.

## Saxe-Meiningen special case

Evidence indicates:
- Karl Wilhelm is the dynastic Duke and is already participating in government by the mid-1770s.
- His mother Charlotte Amalie remains a governing regent/co-governor in this period.

Recommended Victoria 3 abstraction:
- Charlotte Amalie = effective ruler/regent if a single executive slot is required;
- Karl Wilhelm = visible nominal Duke/secondary/heir/co-governor;
- never two ordinary `ruler = yes` characters.

Codex must audit vanilla 1.13 regency mechanics already used successfully for MARATH before implementing MEI.

If the engine cannot represent this without a misleading constitutional fiction:
`MEI_REGECY = DEFERRED_FOR_USER_DECISION`.

## Republic special cases

### Venice
Alvise IV Mocenigo is Doge on 1 January 1776.
Keep Venice republican/oligarchic.

### Genoa
Brixio Giustiniani is Doge on 1 January 1776.
His dogate runs from 31 January 1775 to January 1777.
Keep Genoa republican/oligarchic.

## Shared-monarch cases

### HAN
George III is the same historical person as Batch-1 GBR George III.
Preferred outcome:
- one shared character if the engine relationship supports it;
- otherwise a technically duplicated instance may be unavoidable, but it must reference the same name/date/DNA and be documented as an engine limitation rather than a second historical person.

### HOL / SCH
Christian VII is the same historical sovereign already used for DENNOR.
Codex must first determine whether HOL/SCH are:
- independent start countries;
- subjects;
- dormant tags;
- merely historical definitions.

Do not create new characters until that is known.

## Approximate-date cases

Use `age`, not exact `birth_date`, for:
- MLT Emmanuel de Rohan-Polduc: `age = 50`;
- MOL Grigore III Ghica: `age = 51`;
- WAL Alexandru Ipsilanti: `age = 50`.

These ages are conservative historical approximations for scenario-start representation.

## Out of scope

- Successions after 1 January 1776.
- New succession events.
- Military command assignments.
- Spanish duplicate navy.
- Technology and naval progression.
- Map changes.
- Character DNA/custom 3D clothing.
- SWI/ANH/NAS/SER/LUC/free-city constitutional remapping.
- Crimean Khanate and Caucasus.

## Runtime strategy

One Victoria 3 launch only.

Check a representative/high-risk set first:
BAV, SAX, BAD, HEK, WEI, MEI, SAR, TUS, PAP, MOD, VEN, GEN, MOL, WAL.

Then spot-check the remaining straightforward rulers in the same session.

Also use that same session to perform the previously deferred:
`MUG -> Shah Alam II, age 47`.

After several in-game days, exit normally and inspect logs once.
