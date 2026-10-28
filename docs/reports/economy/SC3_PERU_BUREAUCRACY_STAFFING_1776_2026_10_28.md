# SC3 — Bureaucracy and staffing correction (1776)

Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, 28 October 2026. Draft PR against `main`, not merged.

## Observation

The player observed **−100 bureaucracy** for the Viceroyalty of Peru (`SC3`) in a new game, with about **2.19 million inhabitants**, **11.5% literacy**, and a negative weekly balance. This is a screenshot, not a saved game read; it does **not** prove the exact administrative staffing per building.

The baseline has only **six** government-administration levels: Lima 3, Potosí 2, Santiago 1. All select `pm_simple_organization`, which gives **10 bureaucracy per full-employed level**. Thus baseline *maximum nominal* administrative bureaucracy is 60, insufficient to cover a −100 deficit even if already fully staffed.

Potosí also started on `pm_hereditary_bureaucrats`, which requires an hereditary-bureaucracy/crownland law, but SC3's actual law is `law_appointed_bureaucrats`. Therefore the historical PM declaration was inconsistent with the country's starting laws.

## Changes

### Administrative buildings

| State (SC3) | Original levels | New levels | Added |
|---|---:|---:|---:|
| `STATE_LIMA` | 3 | **12** | +9 |
| `STATE_POTOSI` | 2 | **2** | 0 |
| `STATE_SANTIAGO` | 1 | **6** | +5 |
| **TOTAL** | **6** | **20** | **+14** |

- Baseline upper bound 60 bureaucracy at full staffing → **200** after these changes at full staffing. This is *not* a claim of +140 actual displayed bureaucracy.
- All buildings remain owned by `c:SC3`; existing government organization and religious administrative PMs preserved.
- Potosí `pm_hereditary_bureaucrats` replaced by `pm_professional_bureaucrats` (consistent with `law_appointed_bureaucrats`). No laws or technology grants have been changed.
- No paper cost added to `pm_simple_organization`; using third-era `systematic_population_registration` / `pm_horizontal_drawer_cabinets` would be an ahistorical shortcut and was intentionally avoided.

### Staff using already-present populations

Only the existing non-slave `south_andean` POP groups in the three affected states are **partially reclassified**. Their culture, religion, province and total size are unchanged. All other POP groups (including Indigenous populations) remain unchanged.

| State | Clerks | Bureaucrats | Clergy | Reclassified residents |
|---|---:|---:|---:|---:|
| Lima | 5,400 | 8,100 | 2,700 | 16,200 |
| Potosí | 900 | 1,350 | 450 | 2,700 |
| Santiago | 2,700 | 4,050 | 1,350 | 8,100 |
| **TOTAL** | **9,000** | **13,500** | **4,500** | **27,000** |

The qualified cohorts target ~90% of the corresponding government-administration job types at the new starting building sizes. Initial training/literacy floors scoped to those occupations in only the three states: bureaucrats **55%**, clerks and clergy **40%**, if below. These are gameplay calibration values and **not** historical education measurements.

**Population-preservation checks:** Lima 353,726 before/after, Potosí 112,271 before/after, Santiago 460,878 before/after. No new people, immigration or cultural assimilation.

### Limitations

- The 200 figure is a theoretical **full-employment capacity**, not guaranteed effective bureaucracy. As staffing scales, output is reduced and worker reassignment may occur after the first day. At 80% employment, the *indicative* output is 160; at 90% it is 180.
- The screenshot's −100 is a snapshot of the current budget, not a diagnosis that net bureaucratic demand stays fixed. Laws, institutions, tax capacity, buildings and recruitment may cause changes after game initialization.
- **Adding 14 government buildings entails higher wages**. The baseline already has a fiscal deficit of approx £2.97k/week on the screenshot. This PR prioritizes solving the reported bureaucracy deficit but must be checked for worsening the budget; if necessary adjust levels in another balancing pass, not by fabricating money.
- Coarse initialization of administrative professions is a gameplay calibration and should not be interpreted as an individual-period headcount of the Spanish colonial civil service.

## Verification and in-game plan

Static checks passed for the three administrative state blocks, PM-law compatibility, professions and populations, literacy floors, and script bracket balance. All edits limited to SC3 starting building/pops + one state- and country-scoped qualifications file.

New game 1776:
1. Read SC3 bureaucracy at game initialization and after 1–4 weeks, compare against the observed −100.
2. Inspect `building_government_administration` in Lima (12), Potosí (2) and Santiago (6): staff by occupation, unfilled jobs, qualifications, wages and output.
3. Inspect wages, budget balance and new government expenses. Avoid resolving bureaucratic deficit at the cost of unplayable debt.
4. Confirm no population increase or unwanted cultural changes, and check Potosí government PM selection.
5. Advance one month and save/reload; verify stability and AI behavior.

**No engine runtime test has been performed automatically.**
