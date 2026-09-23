# BUILD START 1776 — RESEARCH COVERAGE AUDIT — CORRIGE

Target date: **1776-01-01**  
Method: canonical `Owner_TAG + State_ID` partition; supplemental historical research performed only to close the 266 missing and 6 uncertain pairs from the first audit. No gameplay file was modified.

## Result

All **1,035 non-Serenissima** canonical Owner/State instances now have an explicit research conclusion. A pair may be `COVERED_ZERO_POSITIVE`; this means it was researched but the available evidence did not justify a manually-placeable positive building at the exact owner/state resolution. The **8 Serenissima exclusions** remain excluded.

| Research region | Expected_Owner_State | Covered | Covered_Zero_Positive | Missing | Multi_Researched | Conflicts | Serenissima_Excluded |
|---|---:|---:|---:|---:|---:|---:|---:|
| R1_WESTERN_EUROPE | 165 | 165 | 18 | 0 | 0 | 0 | 0 |
| R2_NORTHERN_CENTRAL_EASTERN_EUROPE | 105 | 105 | 18 | 0 | 0 | 0 | 0 |
| R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA | 154 | 154 | 4 | 0 | 3 | 0 | 0 |
| R4_SOUTH_ASIA | 60 | 60 | 26 | 0 | 0 | 0 | 0 |
| R5_EAST_ASIA | 90 | 90 | 49 | 0 | 0 | 0 | 0 |
| R6_SOUTHEAST_ASIA_OCEANIA | 102 | 102 | 71 | 0 | 0 | 0 | 0 |
| R7_SUBSAHARAN_AFRICA | 171 | 171 | 131 | 0 | 0 | 0 | 0 |
| R8_NORTH_AMERICA_CARIBBEAN | 125 | 125 | 67 | 0 | 1 | 0 | 0 |
| R9_SOUTH_AMERICA | 63 | 63 | 23 | 0 | 0 | 0 | 0 |

## Supplemental pass

- Previously unresolved pairs audited: **272** (266 missing + 6 uncertain).
- Supplemental pairs with at least one positive building: **90**.
- Supplemental explicit zero-positive conclusions: **182**.
- Supplemental positive building rows: **107**.
- Evidence URLs and the per-pair evidence class are preserved in `BUILD_START_1776_SUPPLEMENTAL_OWNER_STATE_COVERAGE_CORRIGE.csv`; individual positive recommendations and their sources are in `BUILD_START_1776_SUPPLEMENTAL_RESEARCH_CORRIGE.csv`.

## Overlaps and conflicts

The four multi-researched Owner/State pairs remain flagged `Multi_Researched=YES` for provenance. Their building-level disagreements were rechecked in the supplemental pass; the corrected overlap table records the resolution and has `Needs_Human_Review=NO` for every row. Therefore the corrected unresolved conflict count is **0**.

## Controls

- Canonical rows: **1,043** exactly.
- `EXCLUDED_SERENISSIMA`: **8** exactly.
- Non-Serenissima rows: **1,035** exactly.
- Remaining `Needs_Supplement=YES`: **0**.
- Remaining `MISSING_RESEARCH`: **0**.
- Remaining `UNCERTAIN_COVERAGE`: **0**.
- Corrected gaps CSV contains header only, as required by the definition “only Needs_Supplement = YES”.
- No Owner_TAG or State_ID outside the canonical partition was introduced.
- Every supplemental positive Building_ID exists in the supplied building catalog, is history-placeable, is not auto-generated, and is marked relevant for 1776 research.
- Port recommendations were validated against `Has_Port_Access=YES`.

## Final totals

TOTAL OWNER/STATE = 1043
SERENISSIMA EXCLUDED = 8
COVERED = 1035
MISSING = 0
UNCERTAIN = 0
MULTI_RESEARCHED = 4
CONFLICTS = 0

R1 MISSING = 0
R2 MISSING = 0
R3 MISSING = 0
R4 MISSING = 0
R5 MISSING = 0
R6 MISSING = 0
R7 MISSING = 0
R8 MISSING = 0
R9 MISSING = 0
