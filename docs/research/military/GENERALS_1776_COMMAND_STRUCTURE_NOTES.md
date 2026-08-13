# GENERALS_1776_COMMAND_STRUCTURE_NOTES

## Recovered architecture

- Reference date: **1776-01-01**.
- Regional research batches.
- One **cumulative MASTER**.
- No gameplay implementation before the complete packet is closed.
- Strictly distinguish ruler, governor, general and admiral.
- A sovereign/governor is not a general unless independent military command evidence supports it.
- Prefer formation command; use higher command only when the current V3 formation is a theatre abstraction.
- Never invent exact dates, offices or identities to fill a row.
- Collective/decentralized structures stay collective rather than receiving a fabricated European-style commander.
- Admirals are outside this package.

## Post-2D3 target

The old pre-reconstruction audit found 111 armies without generals. That count is retained only as historical traceability.
The current implementation target is the **214 post-2D3 land formations across 175 tags**.

- Fixed named historical assignments: **18**
- Procedural / collective / structural closures: **196**
- Total documented decisions: **214/214**

## Regional batches

- `00_EUROPE_POST_2D3`: 143 formations
- `01_AMERICAS`: 11 formations
- `02_AFRICA`: 0 formations
- `03_MIDDLE_EAST_CAUCASUS`: 15 formations
- `04_SOUTH_ASIA`: 29 formations
- `05_CENTRAL_ASIA`: 5 formations
- `06_EAST_ASIA`: 11 formations
- `07_SOUTHEAST_ASIA`: 0 formations
- `08_OCEANIA`: **0** current post-2D3 land formations; closed structurally, no invented force.

## Meaning of procedural closure

`PROCEDURAL_ALLOWED`:
the formation still needs a playable general in CLEANUP-2D-4, but the starting character must not be presented as a
researched historical identity. Prefer culture-native generation and do not set `historical = yes`.

`PROCEDURAL_REQUIRED_COLLECTIVE_STRUCTURE`:
same rule, with an additional warning that forcing a single named commander would misrepresent a confederal/decentralized
military structure.

`PROCEDURAL_ALLOWED_PENDING_STRUCTURE_REWORK`:
the current runtime formation needs a general even though the polity/map representation is already structurally deferred.
The placeholder must not harden into a historical claim.

## Higher-command abstractions

Hadik, Lacy, Branicki, Rumyantsev, O'Reilly, Ricardos and Clavering are deliberately marked as higher-command or
military-office mappings where appropriate. Their use does not assert that an army with the generated post-2D3 formation
name literally existed under their field command.

## Known legacy debt for 2D-4

- GBR: `colborne_gen` / `aylmer_gen` debt.
- BIC: `maitland_gen` / `madras_army` debt.
- PRU: anachronistic/unvalidated legacy military identities.
- Any army character already in the scripts but not accepted by this MASTER remains **unvalidated legacy**, not
  automatically historical.

## Closure

CLEANUP-2D-4 can now be implemented from the full 214-row MASTER.
Every current land formation must end with at least one valid general, but only the **18** accepted rows in this version
may receive fixed historical identities.
