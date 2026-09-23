# BUILD START 1776 — Administration calibration

## Result

The research-only target of **142** levels is replaced by a conservative static target of **470** levels from **843** current levels. No gameplay file is changed.

## Method

- Exact engine baseline: 10 bureaucracy per incorporated state plus 4 per 100,000 incorporated inhabitants (`STATE_BUREAUCRACY_BASE_COST`, `STATE_BUREAUCRACY_POP_BASE_COST`, `STATE_BUREAUCRACY_POP_MULTIPLE`).
- General retention target: 66% of demonstrated current gross output, with the historical target as a floor.
- Near balance is recovered where appropriate by a separately reviewable runtime plan for targeted de-incorporation of peripheral states, not by accumulating administration everywhere.
- China is an explicit exception: it remains at its small historical target so overpopulation creates a real opening administrative burden. It receives neither dozens of administration levels nor a mass de-incorporation recommendation.
- Spatial priority: capital, historical administrative center, then largest current administrative centers. New placement is used only for a country already represented by current or historical administration.
- Current PM output and state tax capacity are preserved in the static estimate; no PM is changed. Tax capacity is reported but is not forced to 100% in every state.

## Limits requiring runtime

Institutions, enacted laws, wages, employment, tax waste, institution population costs, incorporation progress and workforce qualification cannot be reconstructed exactly from static building history. Every row is therefore marked `RUNTIME_REQUIRED`. The CSV gives current/projected gross bureaucracy and tax-capacity context; `BUILD_START_1776_ADMINISTRATION_DEINCORPORATION_RUNTIME_PLAN.csv` lists only heuristic state candidates and must be historically/runtime reviewed before any write. The authoritative eligibility rule for that later review is now `BUILD_START_1776_DEINCORPORATION_HISTORICAL_CRITERIA.md`: recent conquest, demonstrated high autonomy, indirect rule or weak fiscal-administrative integration—not numerical convenience.

## Validation focus

Test France, Great Britain, Spain, the Ottoman Empire and Japan first, then small multi-state countries. Confirm a positive or only slightly negative bureaucracy balance after the reviewed de-incorporation plan. Test China separately as the intentional overpopulation-burden exception and do not solve it by mass administration or mass de-incorporation.
