## Desktop capability check and manual handoff — 2026-11-12 (Europe/Paris)

**Interactive attempt stopped at the maintainer's request. No new startup-only CPU benchmark was run, and no technology-tree performance comparison was completed. Issue remains open / investigation incomplete.**

### Capabilities actually checked
- The supported **bundled `@oai/sky` Windows interface through `mcp__node_repl__js` is available**: initialization, app/window enumeration and a screenshot request succeeded. This supersedes the earlier blanket statement that no desktop interface was exposed.
- Reliable game capture/input is **not yet validated**. Victoria 3 window metadata was selected, but the captured image showed a different foreground application. **No keyboard/mouse input was sent.** The maintainer then requested: “Stop the interactive test and give me the manual steps.” The owned launch session was stopped; a subsequent read-only inventory showed **zero Victoria 3 windows**.
- AutoHotkey was not found on PATH or in inspected common installation locations. Power Automate Desktop was not found in inspected common locations; Appx inventory was access-denied, so its installed status is not established. No installation, elevation or security/authorization workaround was attempted.
- Windows Performance Recorder is present, but no trace was started. PresentMon was not found in the inspected locations. Native `gui/debug_menues.gui` exposes the `3dstats` command as an FPS/performance-display candidate; its running output was not verified.

### Reversible preparation and diagnostic copy
Four separate user profiles are prepared for **A1–B1–B2–A2**, pinned to the same Steam **1.15.1 executable** (SHA-256 `fb4ec0698afd3d3b1a785926d57bd5d68c95a4afd04b56f6bd45abd7a5672b15`). No normal playset/mod registration was edited. The new A1 launch confirmed the intended A mod and only the preorder soundtrack; B was not newly launched in this continuation. Direct launch still logs failed Steam API initialization, so this is not an authenticated-Steam reproduction. Keep local 1.15.0 + DLC as a separate series.

A new **`C_simplified_gui` diagnostic copy** changes only the two visibility-expression spans. It balances the OR chains and removes redundant identity tests while retaining the force-show/compatibility-filter logic in the static model:
- Edge predicate: **42 → 40** textual technology lookups; maximum parenthesis depth **44 → 9**.
- Card predicate: **43 → 42** lookups; depth **45 → 11**.
- **584 truth-table cases per predicate / 1,168 total**, including all 291 technology identities plus an unknown identity and both ShouldShow states, match the original logic.

These are syntax/model results, **not measured calls per frame, engine-binding validation or a verified speed improvement**. C was not launched or installed into the normal mod; technology definitions remain unchanged.

### Actual results and next actionable test
**Tree opening latency, tree/scroll FPS, frame timings, UI CPU and repeated A/B results remain NOT MEASURED.** No responsiveness claim is inferred from window existence, a Responding flag, CPU startup activity or screenshot-call duration.

Minimum manual handoff:
1. Launch each prepared label serially; use the same paused France save on 1 January 1776, settings and actual DLC configuration.
2. Record 15 seconds with the tree closed; open/warm all three tabs; record stationary and identical left-drag panning observations at fixed zoom. Use `3dstats` only if it exposes useful values; leave unavailable frame timings unmeasured.
3. Run the supplied CPU collector **after** each declared UI state is established; it provides a five-second focus handoff and fifteen-second CPU-only capture.
4. Repeat **A1–B1–B2–A2** and keep first/warm opening delays separate. If B repeatedly improves, A versus C is the subsequent predicate-isolation test.

Local handoff: `C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111/runtime_ui_controlled/MANUAL_TEST.md`, `Start_UI_Trial.ps1`, `Measure_UI_CPU.ps1`, `UI_RESULTS_TO_FILL.csv`. All 28 result rows remain NOT_MEASURED. Evidence/source checks: `docs/reports/compatibility/V1_15_ISSUE54_INTERACTIVE_2026_11_11/`.

**No root cause or permanent correction is established. No In review/Done transition, Git write or normal-installation modification is claimed.**

---

## Authorized resumption / DLC control — 2026-11-11, 23:37–23:41 Europe/Paris

**The maintainer authorized resuming launches and clarified that Steam 1.15.1 has no gameplay DLC, unlike local 1.15.0. The earlier telemetry-approval blocker is resolved for this continuation. Both corrected profiles now actually mount their intended mod. Technology-tree performance remains unmeasured because no supported desktop/game-interface control is available.**

### Verified environment
- Both arms used the same installed Steam **1.15.1** executable, revision `7a630cdf29e`.
- Steam's installed DLC folder inventory contains only `dlc001_preorder`. Fresh logs in **both** arms list exactly **Victoria 2 Remastered Soundtrack**; no gameplay expansion is mounted.
- Local `C:/Games/Victoria 3` has the other DLC folders and remains a separate **1.15.0 + DLC** environment. Folder presence alone is not an entitlement/activation test. No DLC assets were transferred between installations.
- The engine now accepts the corrected object/path `enabledMods` entries. Fresh logs confirm `A_current` / `B_vanilla_gui` mounted and the mod's supported version matching 1.15.1. The previous `Missing path for dlc/mod` error is absent.
- Settings-file hashes match between arms and the captured normal settings. Actual resolution, country/date and tree state could not be verified visually. Logs report settings fallbacks (including language/resolution), so identical settings files must not be represented as visually verified settings.
- Both direct executable launches log **Failed to initialize Steam**. They test the installed Steam build without a successfully initialized Steam-client API; they are not proof of an authenticated Steam-session reproduction.

### New measurements — mod-mounted STARTUP ONLY
One 120-second observation window was run per arm. No country was selected and no technology tree was opened. CPU uses first/last cumulative deltas, excludes the initial interval, and is normalized across the machine's 16 logical processors.

| Arm | Samples | Measured CPU-delta interval | CPU consumed | Mean whole-machine CPU | Peak observed working set | Maximum observed threads |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A, current mod GUI | 188 | 119.69 s | 337.77 CPU-s | 17.64% | 2,976.13 MiB | 54 |
| B, inherited native GUI | 199 | 119.86 s | 527.73 CPU-s | 27.52% | 3,644.36 MiB | 54 |

**These are uncontrolled startup diagnostics, not a technology-tree benchmark.** They establish functioning launch/monitor/log collection with the mod mounted; neither a GUI improvement nor a GUI regression can be inferred. Startup stage, asset caching and background work were not held at a measured tree state. Repeating such startups would not substitute for the requested tree comparisons, so no repeated-tree experiment is claimed.

Both windows were reported Responding at the end; that flag is not a frame-rate measurement. Each script then closed/stopped only its own test child. Opening time, tree FPS, scrolling FPS, paused closed-tree baseline and per-thread tree activity remain unmeasured.

### Fresh log comparison and preservation
- Both current `error.log` files contain **35 nonempty lines**, with identical error multisets after timestamps are removed. They include duplicate localizations/BOM issues and shared journal-widget/menu issues; no unrelated fixes were attempted.
- No `tech_tree` / `TechTree` / `GetTechnology` matches occur in those error logs. Since the technology tree was never opened, this is not a clean in-tree runtime validation.
- Full post-launch A/B integrity check passed again: **3,776 / 3,775 files, only the intended GUI omission**. Normal launcher database, settings and content-load hashes are unchanged; normal mod descriptor and source Git index are unchanged.
- No normal mod/native installation, technology data, historical progression, branch, PR or merge was changed.

### Evidence and remaining work
Same local lab folder: `C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111/`.

New definitive receipts: `runtime_151/RESUMPTION_CONTEXT.json`, `AUTHORIZED_RESUME_RESULTS.json`, `MOD_MOUNTED_STARTUP_DIAGNOSTICS.csv`, and `AB_INTEGRITY_AFTER_AUTHORIZED_RESUME.txt`. Mod-mounted trials: A `trial_20261111T223701114Z`; B `trial_20261111T223925167Z`. Earlier ZIPs/reports are historical snapshots and do not contain this new continuation.

Remaining minimum UI work is selecting the same new game/country/date, pausing, opening all three technology tabs and scrolling in each arm. Once that state is established, CPU/log capture can run automatically; reliable FPS/opening-time collection and repeat A/B comparisons still need supported instrumentation/interaction. A local 1.15.0 + DLC series, if used, must remain separate from this 1.15.1 no-expansion series.

**Issue remains open / investigation incomplete. Root cause unestablished; no verified correction or review transition. Project-field changes still unavailable through current tools.**


<details>
<summary>Earlier launch/preparation history — retained; the authorization, DLC and corrected-mount status above supersede earlier blockers</summary>

## Autonomous execution follow-up — 2026-11-11

**Investigation remains open. Steam 1.15.1 was actually launched and monitored, but no valid technology-tree A/B benchmark or improvement has been measured. Root cause remains unestablished. Not ready for In review or Done.**

### Version clarification for this continuation
The latest maintainer instruction says Sarah's reproduction used **1.15.1**. The canonical local installation is **1.15.0**; Steam separately supplies **1.15.1**. This supersedes the earlier reproduction-version clarification retained below. All launch attempts in this continuation used the **same Steam 1.15.1 executable**, not local 1.15.0. Fresh system logs confirm `release/1.15.1`, revision `7a630cdf29e`. The native GUI files remain byte-identical; that does not equate engine performance.

### What was actually automated
- Reverified the frozen A/B copies after the launch attempts: **3,776 files in A / 3,775 in B; the sole internal difference is B omitting `gui/tech_tree.gui`**. All historical technology/gameplay data remain unchanged.
- Tried to register the prepared descriptors in the ordinary user mod directory; Windows denied access. No escalation, overwrite or change to existing normal playsets was attempted.
- Created independent user directories under `runtime_151/A/user_data` and `runtime_151/B/user_data`. Copied the launcher database and added the two dedicated test playsets **in those copies only**. SQL verifies one selected enabled test mod per profile; this is not a verified launcher-UI registration in the normal profile.
- Copied identical graphics/settings to both profiles (SHA-256 `c39acfe87c3614a0887633db917dd37c88442107e72fa5e75b2f45ac1b0b2803`).
- Launched the Steam executable with the corresponding isolated `--userdir`; obtained native window handles, real CPU/memory/thread samples, and fresh logs in those isolated directories. The first two monitored test processes were stopped by their own launcher script after the observation window; no unrelated game process was targeted.

### Actual measurements — startup diagnostics, NOT A/B tree results
Fresh logs exposed an invalid `enabledMods` schema: bare strings were rejected with **`Missing path for dlc/mod`**. Neither intended mod was mounted. Therefore these startup traces cannot compare modded technologies or GUI implementations.

| Requested arm / attempt | Samples | Interval between first and last samples | Process CPU consumed over interval | Mean CPU, whole 16-logical-CPU machine | Peak observed working set | Maximum observed threads |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| A startup attempt 1, mod NOT loaded | 38 | 25.37 s | 75.33 CPU-s | 18.56% | 776.24 MiB | 54 |
| B startup attempt 1, mod NOT loaded | 89 | 59.26 s | 181.77 CPU-s | 19.17% | 1,586.83 MiB | 54 |

CPU is computed from cumulative process CPU deltas between first/last samples, excluding the first potentially biased interval. Different observation windows and uncontrolled startup phases prohibit performance comparison. Window-handle creation / Windows Responding flags are not technology-tree responsiveness metrics. A third A launch produced partial logs with the same schema failure; no final sampler receipt survived, so no duration or CPU metric is assigned to it.

**Tree opening time: unmeasured. Tree FPS / scrolling FPS: unmeasured. Closed-tree paused baseline / per-thread tree CPU: unmeasured. No country/date/tree state was selected.**

### Preparation correction, not a permanent mod fix
The isolated profiles and preparation script now use `"enabledMods":[{"path":"<frozen mod directory>"}]`, matching a preserved launcher-generated configuration. A bare directory string and a bare descriptor string were both rejected. This corrected object/path format is **not yet engine-verified in this continuation**.

The isolated launch helper now rejects the wrong schema/arm and records whether the expected mod mount is confirmed in fresh logs. Script syntax checks pass. No change to the working mod GUI, technology definitions, native installations or historical progression was made. No branch, commit, PR or merge was created.

### Remaining execution blockers
1. **No supported Windows desktop/game-input tool is exposed.** Process launching works, but country selection, pause, opening the tech tree, scrolling and functional checks cannot be automated with the available tools. No reliable FPS capture is available. Browser tools do not control a native game window; no input-injection workaround was attempted.
2. **Automatic approval review rejected resuming the asynchronous third launch** because the game triggered an external telemetry request to `dc.services.visualstudio.com`, whose payload/disclosure was not authorized or verified. No further launch or indirect workaround was attempted after that rejection. Local evidence collection and preparation checks continued. Further launches require resolving that approval rejection.

Even after launch approval is resolved, minimum human input remains selecting the same new game/country/date, pausing, opening each tree tab and scrolling in each arm. Existing CPU/thread collection can automate those measurements once the UI state is established. First confirm the corrected profile really mounts the intended mod; only then run repeated same-version/same-state A/B measurements. Do not interpret the failed startup attempts as the planned repeated A/B experiment.

### Accessible files
Verified local folder (open with Windows **Win+R**):
`C:\\Users\\simeo\\AppData\\Local\\Temp\\aor1776_techperf54_20261111`

Complete copies are already in `A_current` / `B_vanilla_gui`. Current report: `CURRENT_STATUS_FR.md`. Actual receipts, CSVs, log copies and preservation checks: `runtime_151/`, especially `AUTONOMOUS_ATTEMPT_RESULTS.json`. The v2 ZIP exists locally (286,430 bytes); its older instructions are superseded by this report. The full copies are not inside the small evidence ZIP. The new local archive is **`1776_TechTree_Performance_AB_Kit_v3.zip`** (351,974 bytes, 118 entries; ZIP integrity passed; SHA-256 `f34072045628efa648d42df9c1a502f9a33409dab4ece5c88019620c2fb09ac8`). It includes the new launch evidence and corrected scripts, without user launcher databases or the full mod copies.

Final read-only preservation check: all **3,776 captured working-mod files match the frozen source manifest**, the source Git index and normal mod descriptor hashes are unchanged, and the ordinary launcher database/settings/content-load hashes match their pre-launch values. Steam's native GUI SHA-256 remains `64f73e90f7b263054efadea5ed5bda9ff3857cde76e2a5ebc7cb27060648ea80`. The earlier ChatGPT download link is not relied on for access.

### Coordination / decision
Issue remains assigned to **Malzars-sys**. Project **P1 / In progress** remains requested; available tools still lack Project-field mutation, so no dashboard-field update is claimed. The original visibility predicates remain a hypothesis; neither GUI responsibility nor a permanent correction is established. Initial six-month simulation slowdown remains outside this experiment.


<details>
<summary>Earlier preparation and investigation record — retained; version/status statements are historical</summary>

## Current investigation — 2026-11-11

**In progress / P1 requested. A/B configurations are prepared and hash-verified; runtime experiment is NOT executed. Root cause is NOT established. Not ready for correction review or Done.**

**Version correction from the maintainer:** the reported reproduction is on **local 1.15.0**. Steam separately has **1.15.1**. Both executables/launcher versions were checked, and the two native `tech_tree.gui` files are byte-identical (SHA-256 `64f73e90f7b263054efadea5ed5bda9ff3857cde76e2a5ebc7cb27060648ea80`). This does not make their engines or timings equivalent; both arms of a series must use the same executable. The originally requested issue title is retained.

### Reported observations, not benchmark measurements
Sarah Rose / Yekatarina reports a smooth vanilla tech tree, severe persistent modded-tree lag even while paused, and an initially slow simulation that mostly recovers after about six months while tree lag persists. The remembered historical Paradox fixes are a research lead, not proof of today's mechanism.

### Completed: static inspection
| Item | Current mod | Native local 1.15.0 |
| --- | ---: | ---: |
| Technologies | 291 | 179 |
| Prerequisite edges | 392 | 221 |
| Eras | 12 | 5 |
| Cycles / missing parents / duplicate IDs / missing eras | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| Missing-texture candidates in inspected mounted paths | 0 | 0 |
| GUI size | 43,739 bytes | 35,715 bytes |

The mod's card visibility expression is **3,178 characters / 43 textual GetTechnology calls**; its edge expression is **3,733 characters / 42 calls**. They hide 40 non-researchable compatibility IDs while allowing `joint_stock_companies`; cards also force `stock_exchange`. Their purpose must be preserved by any eventual permanent fix. The count is static syntax, **not measured calls per frame**: update frequency, caching, short-circuiting and culling are unknown.

Both implementations use native category item/line models, opaque native node/line positions and spline points. Card size, global graph margins and zoom parameters match. Header/search placement and progress-text/tooltip/layout differences are other candidates, not proven defects. No specific removed GUI property or invalid binding has been demonstrated. Existing unsynchronised logs show no matches for the inspected tech-tree identifiers; this is not a fresh clean-log test.

### Completed: isolated A/B preparation
Local experiment folder:
`C:/Users/simeo/AppData/Local/Temp/aor1776_techperf54_20261111/`

- **A_current:** 3,776 frozen files, 1,551,406,875 bytes; existing mod GUI.
- **B_vanilla_gui:** 3,775 files; only `gui/tech_tree.gui` is omitted, inheriting the selected native GUI.
- **3,775 other files are identical** between arms and the captured source: technologies, dependencies, costs, unlocks, starting-country data, other GUI and assets. Development/Git roots are excluded from copying.
- External registration descriptors differ only in test names/paths; no internal metadata was changed between copies.
- Full independent PowerShell verification passed. All 3,776 captured source files, source Git index and normal registration remain unchanged at final check.
- Two new mod descriptors and a non-overwriting registration script are prepared. Only `-WhatIf` was run: no user mod registration, existing playset or launcher database was modified. **The maintainer still needs to register the two test mods and create the distinct playsets.**

B may expose compatibility aliases/cards/lines which the current GUI intentionally hides. Record that functional incompatibility; do not alter technology data to make B look correct or promote B directly into a permanent fix.

### Instrumentation and human work remaining
No interactive game control/reliable frame capture is exposed in this session. **No opening-time, FPS, scrolling-FPS, CPU-game or thread-game benchmark exists.**

The delivered kit includes:
- `README_TESTS_FR.md`: exact registration/playset instructions and A1–B1–B2–A2–A3–B3 repeat order, same save/country/date/graphics/resolution/DLC and executable.
- `RESULTATS_A_REMPLIR.csv`: every measurement remains NON_MESURE.
- `Measure_CPU.ps1`: optional 15-second process CPU and thread capture; no FPS claim. Syntax and a PowerShell-only HARNESS self-test passed; that is not a game measurement.
- Structured comparison, complete GUI diff, source/native snapshots, graph/binding inventories and manifests.
- `NEXT_EXPERIMENT_FILTERS_ONLY.diff`: **unapplied diagnostic-only** next experiment if B wins, replacing only the two predicates in the old GUI. It regresses alias hiding and is not a prepared permanent correction.

Human checks: first/warm opening delay; paused closed-tree baseline; stationary/scrolling FPS for all three tabs; CPU/thread activity if available; zoom/search/tooltips; all active technologies/12 eras, prerequisite lines, research queue/selection and unlocks; new GUI errors. Exact data preservation is verified; **working in-game display/functionality is not yet verified**.

### Decision gates
- [x] Structured current/native comparison and graph audit.
- [x] Isolated copies, intended sole GUI difference and complete hash verification.
- [x] Reproducible instructions and instrumentation fallback.
- [ ] Run the controlled game experiment and record real measurements.
- [ ] Identify the actual bottleneck or retain an inconclusive outcome.
- [ ] Prepare the smallest isolated correction/PR only when justified; preserve historical data and alias visibility.
- [ ] In-game validation and integration approval before Done.

If B is consistently faster, isolate predicates versus other GUI differences before choosing a correction. If both remain slow, profile layout, rendered connections, tooltips and unlock calculations while keeping technology data fixed. No permanent GUI patch, branch, commit, PR or merge is made in this investigation.

### Separate simulation observation
Initial simulation lag recovering after roughly six months remains separate. Initialization/caches, market or periodic-script work are hypotheses for later profiling only. No POP, market, AI, country, economic, historical-map, hotfix or Yekatarina-law change.

### Coordination limitation
The issue is created and assigned to **Malzars-sys**. Current tools expose issue updates but **no GitHub Projects field mutation or browser control**. Project **P1 / In progress** is requested and documented; it is **not claimed as an actual Project-field update**. No In review/Done transition is justified.

<details>
<summary>Initial investigation record — retained</summary>

## Investigation started — 2026-11-11

**Status: In progress. Requested Project priority: P1. Assignee: Malzars-sys.**

### Reproduction version correction
The maintainer clarified that Sarah Rose / Yekatarina's reported tests were run on the **local Victoria 3 1.15.0** installation. **Steam has 1.15.1** installed separately. The requested issue title is retained, but the primary A/B comparison must use the same local 1.15.0 executable for both arms.

### Contributor observations (reported, not instrumented)
- Vanilla's technology tree is smooth; the 1776 tree causes severe persistent lag.
- While paused, the rest of the interface is relatively smooth but the tree remains slow.
- Initial unpaused simulation slowdown mostly recedes after roughly six months; the tree remains slow.
- Sarah recalls similar technology-tree problems in earlier game versions later improved by Paradox.

No FPS, opening-time, CPU or thread benchmark has been collected in this investigation yet.

### Scope and current evidence
- Compare the normal mod's `gui/tech_tree.gui`, canonical local 1.15.0 GUI and secondary Steam 1.15.1 GUI.
- The two installed vanilla GUI files currently have the **same SHA-256**. The executable versions differ.
- The mod adds large visibility expressions for each technology card and each dependency line (42/43 technology lookups per expression). They hide compatibility aliases; this is a hypothesis to measure, not a confirmed bottleneck.
- Historical technology definitions, dependencies, costs, unlocks, starting technologies, layouts and all other GUI/assets must remain identical between isolated A/B copies.

### Controlled experiment
- A: frozen copy of current mod, including current technology-tree override.
- B: identical frozen copy, with only `gui/tech_tree.gui` omitted so the selected executable inherits its native GUI.
- Do not edit the working mod, existing worktrees, native installations, existing playsets or uncommitted work.
- Record full runtime file manifests, the sole in-mod difference, registration metadata separately, and any functional incompatibility exposed by B.
- Use the same save/country/date/graphics/resolution/DLC/mod list; separate cold and warm opening, steady tree FPS, scrolling FPS and closed-tree paused baseline. Record actual measurements only.

### Acceptance
- [ ] Static comparison and technology-graph audit.
- [ ] Isolated A/B preparation and hash verification.
- [ ] Reliable runtime measurements and visual/functionality checks.
- [ ] Establish actual bottleneck or document inconclusive result.
- [ ] Minimal verified isolated correction/PR, if evidence supports one.
- [ ] Human in-game validation and required integration approval before Done.

The initial simulation slowdown is a separate observation: no POP, market, AI, country or economic changes in this mission. Preserve the 1.15 hotfix, historical map work and Yekatarina's laws.

**GitHub Projects limitation:** the current connector exposes issue operations but no Project-field mutation or browser control. P1 / In progress above are requested Project values, not claimed field updates. No PR, verified correction or benchmark result exists yet.

</details>

</details>

</details>

