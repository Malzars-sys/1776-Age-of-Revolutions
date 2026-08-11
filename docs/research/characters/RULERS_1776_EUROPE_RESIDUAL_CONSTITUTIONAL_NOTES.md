# RULERS_1776_EUROPE_RESIDUAL_CONSTITUTIONAL_NOTES

## Purpose

Companion to:
- `RULERS_1776_EUROPE_RESIDUAL_MASTER.csv`
- `RULERS_1776_EUROPE_RESIDUAL_SOURCES.md`

Target implementation phase:

**CLEANUP-2B-3 — Complete European Historical Reconstruction**

After that phase, every one of the 62 active European tags must be explicitly classified as one of:
1. `HISTORICAL_SCRIPTED`
2. `SHARED_HISTORICAL_MONARCH`
3. `HISTORICAL_DELEGATED_EXECUTIVE`
4. `JUSTIFIED_PROCEDURAL_OFFICEHOLDER`
5. `MAP_REWORK_DEFERRED`

No procedural ruler should remain merely because a tag was forgotten.

## 1. Conditional German abstractions

The following generic fork tags must be mapped from local fork evidence before scripting:

- `ANH` — candidate Leopold III Friedrich Franz of Anhalt-Dessau.
- `HOH` — candidate Karl Friedrich of Hohenzollern-Sigmaringen.
- `NAS` — candidate Karl Wilhelm of Nassau-Usingen.
- `SCW` — candidate Ludwig Günther II of Schwarzburg-Rudolstadt.

Use:
- country definitions;
- start ownership/capital;
- localisations;
- flags;
- comments;
- imported setup;
- subject relationships.

If local evidence does not identify the intended historical branch with high confidence, do not force the supplied candidate. Mark `ABSTRACTION_DEFERRED`.

Codex should **not browse externally** to resolve these; the historical candidates are already supplied.

## 2. Free cities

Keep these republics:

- `BRE` Bremen — Hermann von Line — Bürgermeister.
- `FRM` Frankfurt — Hieronymus Maximilian von Glauburg — Älterer Bürgermeister / Senior Mayor.
- `HAM` Hamburg — Nicolaus Schuback — Bürgermeister.
- `LUB` Lübeck — Bernhard von Wickede — Bürgermeister.

Each visible character is a gameplay abstraction of a collective urban executive.

Do not:
- create hereditary succession;
- turn the city into a monarchy;
- alter unrelated subject/diplomatic arrangements.

## 3. Switzerland

`SWI` must not be represented as a modern historical “President of Switzerland”.

Recommended V3 abstraction:
- Johann Konrad Heidegger;
- `Bürgermeister of Zürich (Vorort)` / `Bourgmestre de Zurich (Vorort)`;
- approximate age 65;
- republican/confederal laws preserved.

The character is an abstraction of Zürich's leading federal/Vorort role, not a claim that the Old Confederacy had a unitary national president.

## 4. Lucca — deliberate procedural exception

Research firmly establishes:
- Republic of Lucca;
- Collegio degli Anziani;
- two-month terms;
- rotating `Gonfaloniere di Giustizia`;
- system surviving until 1799.

Research does **not** securely identify the exact Gonfaloniere holding office on 1 January 1776.

Therefore:
- remove monarchy/autocracy from `LUC`;
- use an appropriate existing republican/oligarchic law combination;
- visible title = `Gonfaloniere di Giustizia`;
- allow the engine to generate the short-term officeholder.

Mark:
`LUC_JUSTIFIED_PROCEDURAL_OFFICEHOLDER = YES`

Do not fabricate a historical name merely to eliminate a procedural portrait.

## 5. Habsburg crown lands

These are delegated executives, **not sovereign monarchs**:

- `BEO` — Charles Alexander of Lorraine — Governor-General.
- `GAL` — Heinrich Joseph Johann von Auersperg — Governor.
- `HUN` — Albert Casimir of Saxony-Teschen — Royal Governor / Lieutenant.
- `TRS` — Samuel von Brukenthal — President of the Gubernium / Imperial Plenipotentiary Commissioner in 1776.

For all four:
- Maria Theresa remains the Habsburg sovereign;
- keep `AUS` crown-land relationship;
- no new independent hereditary monarchy;
- use narrow country-scoped government/title logic.

### TRS chronology trap
Brukenthal became actual Governor only in 1777.
On `1776-01-01`, do **not** display Governor if a more accurate pre-governor title can be implemented.

## 6. Luxembourg

`LUX` is a map/setup problem, not a missing-dynasty problem.

Historical structure:
- Luxembourg under Austrian Habsburg rule within the Austrian/Southern Netherlands framework.

Fork structure:
- separate independent monarchy.

Default:
`LUX_MAP_REWORK_DEFERRED = YES`

Do not give the current independent tag a fake standalone prince merely to remove the generated ruler.

No map, ownership, subject or diplomacy change in CLEANUP-2B-3.

## 7. Crimea

`CRI` has a historical starting ruler independent of the future regional map solution:

- Devlet IV Giray;
- Khan;
- approximate age 47.

Implement ruler/title only.

Do not alter:
- borders;
- subject status;
- state ownership;
- Russian/Ottoman diplomacy.

## 8. UBD

`UBD` is an anachronistic Baltic polity abstraction.

Historically grounded administrator:
- George Browne;
- born 1698-06-15;
- age 77;
- Governor-General of Livonia and Estonia.

Decision tree:

1. If Browne can be represented as a delegated governor while:
   - preserving `UBD -> RUS`;
   - not altering territory/diplomacy;
   - not implying sovereign monarchy;
   then implement and mark:
   `UBD_TEMPORARY_MAP_ABSTRACTION = YES`.

2. Otherwise:
   `UBD_MAP_REWORK_DEFERRED = YES`.

Never title Browne King, Duke, Prince or equivalent sovereign ruler.

## 9. IREK

`IREK` is a verification/fix case, not new ruler research.

Historical sovereign:
- George III shared with Great Britain.

Required:
- verify personal union reuses Batch-1 George III;
- no duplicate character;
- runtime-check Ireland.

Audit anomaly:
`activate_law = law_type:state_religion`

Codex must inspect actual local Victoria 3 1.13 law IDs and identify the intended valid key before changing it. If ambiguous, do not guess.

## 10. Mandatory regency runtime hotfix before residual implementation

Previous runtime found:
- MARATH: `designate_character_as_regent` unknown.
- MEI: `designate_character_as_regent` unknown.

Visual government/title output can look correct even though the parser rejects the effect.

CLEANUP-2B-3 must start by auditing actual local vanilla 1.13 regency mechanics.

Rules:
- never invent an effect name;
- search local vanilla for proven supported usage;
- preserve:
  - MARATH: Sakharam Bapu effective Regent; Madhavrao II child heir/Peshwa;
  - MEI: Charlotte Amalie effective Regent; Karl Wilhelm secondary heir/Duke.
- If custom government + modifier + normal ruler/heir flags are sufficient and the invalid effect is unnecessary, remove only the invalid effect.
- Otherwise use only a mechanism demonstrated in actual local vanilla 1.13.

## 11. UTF-8 BOM warnings

Runtime identified BOM warnings for:
- `common/history/characters/cleanup2b1 - major rulers 1776.txt`
- `common/history/characters/cleanup2b2 - europe rulers 1776.txt`
- `common/government_types/00_mod_gov_types.txt`

Convert these to the encoding required by the local game/project without unrelated semantic changes.

## 12. Traits / ideologies

This packet establishes identity, chronology, office, title and constitutional role.

It does not establish psychological personality traits.

Do not mass-invent traits or ideologies.

## 13. Art

Out of scope:
- custom DNA;
- clothing;
- accessories;
- meshes;
- textures;
- GFX.

Procedural portraits are acceptable until the post-map 3D character-art phase.

## 14. One-session runtime strategy

One game launch only.

Check:
1. MARATH regency, and no regency parser error.
2. MEI regency, and no regency parser error.
3. No BOM warning from the three fixed files.
4. All newly scripted unambiguous residual rulers.
5. Free cities remain republics.
6. Lucca is a republic with `Gonfaloniere di Giustizia`; procedural person is acceptable by design.
7. Habsburg crown lands show delegated executives, not sovereign kings.
8. Switzerland has no fictional national presidency.
9. IREK shares George III without duplicate.
10. LUX remains explicitly deferred/unmodified.
11. UBD matches the documented static decision.
12. After several in-game days, inspect logs once.
