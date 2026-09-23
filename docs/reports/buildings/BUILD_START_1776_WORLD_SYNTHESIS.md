# BUILD START 1776 — WORLD SYNTHESIS

Target date: **1776-01-01**  
Scope: **synthesis/research only — no gameplay modification, no commit, no push.**

## 1. Executive summary
The canonical partition contains **1043** Owner/State instances, including **8** Serenissima exclusions. All **1035** non-Serenissima pairs are covered; missing, uncertain and unresolved-conflict counts are all zero.
The frozen historical target contains **2118** Owner/State/Building rows, **2924** total levels, and **407** explicitly zero-positive Owner/State pairs.
After the target was frozen, comparison with the supplied current setup produced KEEP=310, ADD=1330, REMOVE=1806, INCREASE=140, DECREASE=338. Serenissima rows are preserved separately and never counted as a redistribution decision.

## 2. Inputs and authority
Authority order used: canonical research partition; corrected coverage/supplemental files; corrected overlap decisions; original regional positive recommendations; technical building catalog. `CURRENT_BUILDINGS` was used only after the historical target was frozen.

## 3. Coverage confirmation
Canonical=1043; excluded Serenissima=8; covered non-Serenissima=1035; missing=0; uncertain=0; unresolved research conflicts=0.

## 4. Methodology
Positive rows from all supplied regional matrices plus the corrected supplemental matrix were remapped to canonical Owner_TAG + State_ID. Exact duplicate target keys were merged. Corrected Hawaii/Tibet overlap decisions were then applied. Zero-positive pairs were derived only after the final target was frozen. No external historical research was added in this synthesis phase.

## 5. Global level calibration
All supplied positive levels fall within L1–L4. The cross-regional calibration pass compared distributions and emblematic sectors against the common L0–L4+ interpretation. No additional level rewrite was made beyond the explicit corrected overlap decisions, because there was no source-grounded basis for arbitrary global rescaling. Large global deltas are flagged in the building-type summary rather than silently normalized.

## 6. Agriculture
Target: **472 rows / 585 levels** across catalog categories AGRICULTURE_COMMERCIAL. Detailed geography and evidence remain row-level in `BUILD_START_1776_WORLD_HISTORICAL_TARGET.csv`.

## 7. Plantations
Target: **114 rows / 187 levels** across catalog categories PLANTATION. Detailed geography and evidence remain row-level in `BUILD_START_1776_WORLD_HISTORICAL_TARGET.csv`.

## 8. Resource extraction
Target: **188 rows / 264 levels** across catalog categories RESOURCE_EXTRACTION. Detailed geography and evidence remain row-level in `BUILD_START_1776_WORLD_HISTORICAL_TARGET.csv`.

## 9. Manufacturing
Target: **338 rows / 468 levels** across catalog categories MANUFACTURING. Detailed geography and evidence remain row-level in `BUILD_START_1776_WORLD_HISTORICAL_TARGET.csv`.

## 10. Textile
Target: **170 rows / 263 levels**. Highest examples: China — Suzhou L4; East India — East Bengal L4; France — Rhône L4; Great Britain — Lancashire L4; Spain — Catalonia L4; Switzerland — East Switzerland L4; Austria — Lombardy L3; Belgium — Flanders L3

## 11. Food industries
Target: **67 rows / 81 levels**. Highest examples: Hamburg — Elbe L3; America — Pennsylvania L2; France — Île-de-France L2; Great Britain — Home Counties L2; Japan — Osaka L2; Kingdom of Ireland — Munster L2; Netherlands — Holland L2; Nueva España — México L2

## 12. Glass / paper / furniture / tools
Target: **94 rows / 111 levels**. Highest examples: Austria — Bohemia L3; Great Britain — Midlands L3; America — Pennsylvania L2; America — Pennsylvania L2; Belgium — Wallonia L2; China — Jiangxi L2; France — Île-de-France L2; France — Île-de-France L2

## 13. Mining / metallurgy
Target: **72 rows / 121 levels**. Highest examples: Brazil — Minas Gerais L4; China — Yunnan L4; Belgium — Wallonia L3; China — Sichuan L3; France — French Low Countries L3; Great Britain — Wales L3; Great Britain — West Country L3; Japan — Hokushin'etsu L3

## 14. Military industries
Target: **43 rows / 55 levels**. Highest examples: Awadh — Oudh L2; Belgium — Wallonia L2; France — Île-de-France L2; France — Rhône L2; Great Britain — Home Counties L2; Great Britain — Home Counties L2; Great Britain — Midlands L2; Hindustan — Delhi L2

## 15. Shipbuilding
Target: **73 rows / 100 levels**. Highest examples: Cuba — Western Cuba L3; Netherlands — Holland L3; Portugal — Estremadura L3; Spain — Lower Andalusia L3; America — Maine L2; America — Massachusetts L2; Brazil — Rio de Janeiro L2; Denmark-Norway — Zealand L2

## 16. Ports
Target: **196 rows / 290 levels**. Highest examples: Netherlands — Holland L4; Austria — Slovenia L3; Brazil — Rio de Janeiro L3; Cuba — Western Cuba L3; East India — West Bengal L3; East Indies — West Java L3; France — Brittany L3; France — Provence L3

## 17. Regional infrastructure
Target: **232 rows / 293 levels**. Highest examples: China — Jiangsu L3; Great Britain — Home Counties L3; Netherlands — Holland L3; Afghanistan — Kabulistan L2; Afghanistan — Kandahar L2; America — Pennsylvania L2; Austria — Lombardy L2; Austria — Slovenia L2
All 232 infrastructure rows use `pm_no_rail_network`; active rail in the 1776 plan = 0. Canal PMs are activated only where the supplied research explicitly supports canals/waterways.

## 18. Trade centers
Target: **239 rows / 366 levels**. Highest examples: East Indies — West Java L4; Great Britain — Home Counties L4; Netherlands — Holland L4; Austria — Slovenia L3; Bhavnagar — Gujarat L3; Brazil — Rio de Janeiro L3; China — Western Guangdong L3; China — Suzhou L3
Trade centers were synthesized separately because they consume infrastructure and merchant marine and can create start-date overcapacity.

## 19. Western Europe
Final historical target: **631 rows / 965 levels**. Coverage gaps after correction: 0.

## 20. Northern/Central/Eastern Europe
Final historical target: **216 rows / 256 levels**. Coverage gaps after correction: 0.

## 21. Middle East/North Africa/Caucasus/Central Asia
Final historical target: **486 rows / 539 levels**. Coverage gaps after correction: 0.

## 22. South Asia
Final historical target: **170 rows / 265 levels**. Coverage gaps after correction: 0.

## 23. East Asia
Final historical target: **112 rows / 186 levels**. Coverage gaps after correction: 0.

## 24. Southeast Asia/Oceania
Final historical target: **62 rows / 92 levels**. Coverage gaps after correction: 0.

## 25. Sub-Saharan Africa
Final historical target: **50 rows / 52 levels**. Coverage gaps after correction: 0.

## 26. North America/Caribbean
Final historical target: **253 rows / 357 levels**. Coverage gaps after correction: 0.

## 27. South America
Final historical target: **138 rows / 212 levels**. Coverage gaps after correction: 0.

## 28. Tech conflicts
**664** target rows retain a historically justified building/PM while requiring distribution review. These are listed in `BUILD_START_1776_TECH_CONFLICTS.csv`; the synthesis does not modify technologies.

## 29. India/Vietnam provisional cases
Provisional map-rework target rows: **182**. Breakdown: {'INDIA_FUTURE_REWORK': 170, 'VIETNAM_FUTURE_REWORK': 12}. Existing state IDs are retained; no future state IDs were invented.

## 30. Serenissima exclusion
VEN/GEN and all `Excluded_Serenissima=YES` pairs are absent from the historical redistribution target. In the implementation matrix their existing rows are set to `PRESERVE_SERENISSIMA`, with zero delta.

## 31. Current-vs-target comparison
Current supplied setup: **2639 rows / 6779 levels**. Frozen historical target (excluding Serenissima): **2118 rows / 2924 levels**. Implementation decisions: KEEP=310, ADD=1330, REMOVE=1806, INCREASE=140, DECREASE=338, PRESERVE_SERENISSIMA=45, REVIEW=0.

## 32. Removal review
**1806** current rows would disappear under the frozen target and are listed individually. Post-1776 catalog cases are explicitly distinguished from ordinary covered-but-unsupported current rows.

## 33. Global building-type deltas
| Building | Current | Target | Delta | Flag |
|---|---:|---:|---:|---|
| `building_government_administration` | 843 | 142 | -701 | LARGE_GLOBAL_DECREASE_REVIEW; PRESERVE_SERENISSIMA_ROWS=2 |
| `building_logging_camp` | 458 | 75 | -383 | LARGE_GLOBAL_DECREASE_REVIEW; PRESERVE_SERENISSIMA_ROWS=1 |
| `building_wheat_farm` | 491 | 141 | -350 | LARGE_GLOBAL_DECREASE_REVIEW; PRESERVE_SERENISSIMA_ROWS=4 |
| `building_railway` | 4 | 293 | 289 | LARGE_GLOBAL_INCREASE_REVIEW |
| `building_tea_plantation` | 268 | 5 | -263 | LARGE_GLOBAL_DECREASE_REVIEW |
| `building_fishing_wharf` | 301 | 64 | -237 | LARGE_GLOBAL_DECREASE_REVIEW; PRESERVE_SERENISSIMA_ROWS=6 |
| `building_naval_administration` | 242 | 45 | -197 | LARGE_GLOBAL_DECREASE_REVIEW; PRESERVE_SERENISSIMA_ROWS=2 |
| `building_rye_farm` | 189 | 18 | -171 | LARGE_GLOBAL_DECREASE_REVIEW |
| `building_rice_farm` | 205 | 40 | -165 | LARGE_GLOBAL_DECREASE_REVIEW; PRESERVE_SERENISSIMA_ROWS=1 |
| `building_livestock_ranch` | 441 | 288 | -153 |  |
| `building_barrack` | 171 | 27 | -144 | LARGE_GLOBAL_DECREASE_REVIEW |
| `building_tobacco_plantation` | 164 | 24 | -140 | LARGE_GLOBAL_DECREASE_REVIEW |
| `building_opium_plantation` | 127 | 2 | -125 | LARGE_GLOBAL_DECREASE_REVIEW |
| `building_silk_plantation` | 156 | 32 | -124 | LARGE_GLOBAL_DECREASE_REVIEW; PRESERVE_SERENISSIMA_ROWS=1 |
| `building_dye_plantation` | 122 | 7 | -115 | LARGE_GLOBAL_DECREASE_REVIEW |

Flagged large-ratio building types: **34**. Flags are diagnostic only; the historical target was not rewritten simply to reduce a large gameplay delta.

## 34. Gameplay risks
Principal implementation risks are: 1806 removals, 664 technology/PM distribution reviews, 239 manual trade-center seeds, 232 regional-infrastructure seeds, and 182 provisional map-rework target rows. These require implementation-side review but do not reopen historical coverage.

## 35. Implementation recommendations
Implement from `BUILD_START_1776_WORLD_IMPLEMENTATION_MATRIX.csv`, not directly from individual regional files. Apply technology/PM changes only after reviewing the dedicated tech and infrastructure plans. Process removal-review rows explicitly. Preserve Serenissima unchanged. Run runtime validation after implementation, with special attention to trade-center profitability/capacity and infrastructure PM gates.

---

## Final summary
CANONICAL OWNER/STATE = 1043
SERENISSIMA EXCLUDED = 8
NON-SERENISSIMA COVERED = 1035
MISSING COVERAGE = 0
UNRESOLVED CONFLICTS = 0
HISTORICAL TARGET ROWS = 2118
HISTORICAL TARGET TOTAL LEVELS = 2924
ZERO-POSITIVE OWNER/STATE = 407
CURRENT BUILDING ROWS = 2639
CURRENT TOTAL LEVELS = 6779
KEEP = 310
ADD = 1330
REMOVE = 1806
INCREASE = 140
DECREASE = 338
TRADE CENTER TARGET ROWS = 239
TRADE CENTER TARGET LEVELS = 366
REGIONAL INFRASTRUCTURE ROWS = 232
TECH DISTRIBUTION REVIEW ROWS = 664
MAP REWORK PROVISIONAL ROWS = 182
UNKNOWN OWNER TAGS = 0
UNKNOWN STATE IDS = 0
UNKNOWN BUILDING IDS = 0
AUTO-GENERATED VIOLATIONS = 0
POST-1776 VIOLATIONS = 0
ACTIVE RAIL IN 1776 = 0
SERENISSIMA CHANGES = 0

NO GAMEPLAY MODIFICATION
NO COMMIT
NO PUSH
