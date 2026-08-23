# TECH5B1-R1 — Runtime Override Architecture Test

## 1. Git baseline

- `BRANCH = tech4c2-audit-snapshot`
- `HEAD = e26279bf32c3dae3359c32d68de9343f11a4883e`
- The initial working tree contained exactly the six untracked TECH5B1 files expected by the R1 specification and no other changes.

## 2. Vanilla source and version

- `VANILLA_GAME_PATH = C:\Games\Victoria 3\game`
- `VANILLA_EXECUTABLE = C:\Games\Victoria 3\binaries\victoria3.exe`
- `VANILLA_VERSION = 1.13.9` (file version and product version).
- Canonical source: `C:\Games\Victoria 3\game\common\buildings\07_government.txt`
- Source SHA-256: `3c83d9f86d2d986e02749fc438959227012dccda54411f211c1cd7c8b3118954`

## 3. Runtime diagnostic for the failed late-file strategy

The preceding TECH5B1 static implementation used late files named `99_tech5b1_frozen_technology_gate_overrides.txt`. Runtime testing reported `Duplicated key ... will not be created` for TECH5B1 buildings and production methods, including `building_university`, `building_steel_mill`, and `pm_cannons`. The engine retained the previously parsed Vanilla objects; University therefore continued to require `academia`.

- `TECH5B1_MAPPING_DESIGN = VALID`
- `TECH5B1_LATE_FILE_OVERRIDE_STRATEGY = INVALID`

This R1 phase does not reinterpret any frozen mapping. It tests only same-relative-path file shadowing.

## 4. Failed files removed

The following failed gameplay files were removed from the working tree and are absent during R1:

- `common/buildings/99_tech5b1_frozen_technology_gate_overrides.txt`
- `common/production_methods/99_tech5b1_frozen_technology_gate_overrides.txt`

The four TECH5B1 reports remain present and unchanged as documentary snapshots.

## 5. Vanilla source tested

- `R1_VANILLA_FILE = common/buildings/07_government.txt`
- Absolute source: `C:\Games\Victoria 3\game\common\buildings\07_government.txt`
- Source encoding: UTF-8 with BOM.
- Source line endings: LF (`134` line-feed characters, `0` CRLF sequences).
- Source size: `2631` bytes.

## 6. Same-path mod file created

- `R1_MOD_FILE = common/buildings/07_government.txt`
- Mod encoding: UTF-8 with BOM.
- Mod line endings: LF (`134` line-feed characters, `0` CRLF sequences).
- Mod size: `2660` bytes.
- `FILES_DIFFERENT = YES`

The mod file contains the complete Vanilla file: all three top-level objects remain present, in identical order, with no truncation.

## 7. Isolated test object

- `R1_TEST_OBJECT = building_university`
- `building_university` top-level definitions in mod file: `1`.
- `building_government_administration` top-level definitions in mod file: `1`.
- Top-level objects in Vanilla file: `3`.
- Top-level objects in mod file: `3`.
- Top-level ID order identical: `YES`.
- Braces balanced: `YES`.

## 8. Gate under test

- `OLD_GATE = academia`
- `TEST_GATE = institutionalized_scientific_exchange`

Only `building_university.unlocking_technologies` was changed.

## 9. Byte/text parity validation

- Vanilla SHA-256: `3c83d9f86d2d986e02749fc438959227012dccda54411f211c1cd7c8b3118954`
- Mod SHA-256: `a6f909f856ef4852fbbb1cbc2dee16ce9d96bbcb21f155805fabc3829a479d53`
- Replacing the single test token in the mod bytes with `academia` reproduces the Vanilla bytes exactly.
- Normalized mod SHA-256: `3c83d9f86d2d986e02749fc438959227012dccda54411f211c1cd7c8b3118954`
- `AUTHORIZED_GATE_DIFFERENCES = 1`
- `UNAUTHORIZED_DIFFERENCES = 0`
- `STATIC_ARCHITECTURE_TEST = PASS`

## 10. Theoretical effective graph for R1

If same-path shadowing works at runtime, only this scoped relation changes relative to TECH5A:

- `academia → building_university` is replaced by `institutionalized_scientific_exchange → building_university`.

Expected theoretical counters:

- `HIDDEN_ALIAS_RELATIONS_BASELINE = 64`
- `HIDDEN_ALIAS_RELATIONS_FOR_R1 = 63`
- `ACADEMIA_SCOPED_BUILDING_REFERENCES_FOR_R1 = 0`
- All other 33 TECH5B1 physical transfers: `REVERTED_TO_VANILLA_FOR_TEST`.

These are static expectations only; they are not a claim of runtime success.

## 11. Other objects intentionally left Vanilla

- `building_government_administration` remains gated by `tech_bureaucracy`.
- No production-method same-path file was created.
- `pm_cannons` and every other TECH5B1 production-method transfer intentionally use Vanilla behavior during R1.
- No technology, prerequisite, era, alias, descriptor, `replace_path`, PMG, PM order, starting technology, localization, or unrelated gameplay file was changed.

## 12. Runtime checklist

1. Close Victoria 3 completely if it is running.
2. Relaunch the game so all databases are loaded again.
3. Open a game with a country that does not yet possess `institutionalized_scientific_exchange`, if possible.
4. Open the construction menu.
5. Hover University.
6. Confirm that University requires **Échanges scientifiques**, not **Études universitaires**.
7. Close the game or inspect `error.log`.
8. Search for `building_university`, `07_government`, and `Duplicated key`.
9. Confirm that no `Duplicated key building_university will not be created` entry originates from the mod same-path file.

Decision rule:

- If University requires Échanges scientifiques and there is no duplicate-key error for `building_university`, record `R1_ARCHITECTURE = VALID` and stop. Do not apply the other 33 transfers.
- If University still requires Études universitaires or a duplicate-key error appears, record `R1_ARCHITECTURE = INVALID` and stop. Do not try a third architecture automatically.

### Manual runtime result

Evidence source: `MANUAL_USER_RUNTIME_EVIDENCE`. Codex did not execute this runtime test.

- University requires **Échanges scientifiques**.
- Échanges scientifiques displays **Déverrouille université**.
- After a complete game restart, the user's `Select-String` search for `building_university`, `common/buildings/07_government.txt`, and `Duplicated key building_university` returned no line in `error.log`.
- `DUPLICATE_KEY_BUILDING_UNIVERSITY = 0`
- `MANUAL_RUNTIME_VALIDATION = PASS`
- `RUNTIME_ARCHITECTURE_TEST = PASS`
- `R1_ARCHITECTURE = VALID`
- `SAME_PATH_FILE_SHADOWING = VALID`

## 13. Status

- `R1_TEST_OBJECT = building_university`
- `R1_VANILLA_FILE = common/buildings/07_government.txt`
- `R1_MOD_FILE = common/buildings/07_government.txt`
- `AUTHORIZED_GATE_DIFFERENCES = 1`
- `UNAUTHORIZED_DIFFERENCES = 0`
- `STATIC_ARCHITECTURE_TEST = PASS`
- `MANUAL_RUNTIME_VALIDATION = PASS`
- `RUNTIME_ARCHITECTURE_TEST = PASS`
- `R1_ARCHITECTURE = VALID`
- `SAME_PATH_FILE_SHADOWING = VALID`
- `DUPLICATE_KEY_BUILDING_UNIVERSITY = 0`

`TECH5B1R1_MANUAL_RUNTIME_PASS`

No commit and no push were performed.
