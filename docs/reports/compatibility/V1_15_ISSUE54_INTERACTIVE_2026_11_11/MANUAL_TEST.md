# Issue 54 — minimum manual actions

> Superseded by [the resumed manual protocol](RESUMED_2026_11_12/MANUAL_TEST_FR.md).
> The resumed attempt reached a paused France session but did not establish a
> reliable tree measurement. Its rejected Russia 1870 save copies are archived.
> The earlier preparation below is retained as history.

The interactive attempt was stopped at your request. No tree, FPS, frame-time
or UI CPU comparison was measured. Normal mod files and playsets remain intact.
Do not rerun the old startup-observation helper.

## Start the prepared profiles

Use Steam **1.15.1** for every run, with no gameplay DLC; keep the separate local
1.15.0 + DLC installation out of this series. Close other 3D applications first.
In PowerShell set:

```powershell
$ui = 'C:\Users\simeo\AppData\Local\Temp\aor1776_techperf54_20261111\runtime_ui_controlled'
```

Run these **one at a time**, quitting Victoria 3 between lines:

```powershell
& "$ui\Start_UI_Trial.ps1" -Trial A1
& "$ui\Start_UI_Trial.ps1" -Trial B1
& "$ui\Start_UI_Trial.ps1" -Trial B2
& "$ui\Start_UI_Trial.ps1" -Trial A2
```

The launch terminal stays open until its game exits. It refuses to start while
another Victoria 3 process exists. Each attempt keeps separate receipts/output.
No normal mod registration or playset edits are needed. Direct launches still
show the Steam API initialization warning: this is not an authenticated-Steam
reproduction. Keep that launch condition identical between arms.

## Minimum actions in each game

1. **A1 only:** start France on 1 January 1776, pause and save as `TECHPERF54`.
   Use this exact save in the other runs: copy its `.v3` from A1's isolated
   `user_data\save games` into B1/B2/A2's `user_data\save games` directories.
   Never overwrite a campaign save. The stopped loading attempt is not A1 data.
2. Verify identical resolution, UI scale, graphics, VSync/FPS cap and language.
   Settings files started identical; their visible values remain unverified.
   Debug mode is already enabled. In the **game's debug console**, run
   `3dstats`, then close the console. The command is referenced by the native
   GUI; its running display has not been verified by this investigation.
3. Observe the paused map with the tree **closed** for 15 seconds. Record FPS
   and the first tree-opening delay. Use a video/stopwatch if available; CPU
   and automation-call durations cannot substitute for click-to-render latency.
4. Open Production, Military and Society once to warm them. For each tab,
   observe 15 seconds stationary, then repeat the same left-drag pan down/up
   at fixed zoom. The wheel changes zoom, so it is not an equivalent pan test.
   Record FPS and frame times only if the display actually exposes them;
   otherwise leave frame times **NOT MEASURED**.
5. Close/reopen the tree three times; record warm delays separately. Quit and
   repeat with the next label: **A1, B1, B2, A2**, always loading the same save.
   Two runs per arm are a minimum comparison, not statistical certification.

## CPU after the UI state is established

In a second PowerShell window, set `$ui` as above. Run one command for the
state already prepared, then return to Victoria 3 within five seconds. The
capture lasts 15 seconds. Run each line separately:

```powershell
& "$ui\Measure_UI_CPU.ps1" -Trial A1 -Phase closed_paused -Category none
& "$ui\Measure_UI_CPU.ps1" -Trial A1 -Phase tree_stationary -Category production
& "$ui\Measure_UI_CPU.ps1" -Trial A1 -Phase tree_scroll -Category production
```

Use `military` / `society` for the other tabs and `B1`, `B2`, `A2` for subsequent
runs. The collector requires exactly one Victoria 3 process at the same Steam
executable path. It does not verify the declared UI state, produce FPS, infer
frame timings or start the game. Results are written under
`runtime_ui_controlled\<trial>\measurements`. Mark a sample invalid if focus,
a popup or other foreground work interrupts it.

Fill `UI_RESULTS_TO_FILL.csv` with the visible FPS, frame-time availability,
opening delays and matching CPU CSV. Missing observations stay NOT MEASURED.

## Diagnostic C is a separate test

`C_simplified_gui` changes only the two visibility expressions. All technology
definitions remain identical; force-show and compatibility hiding match the
original logic in the static model. C has not been launched or benchmarked.
Complete A/B first. If B repeatedly improves, compare A versus C separately to
isolate the predicates from other GUI changes. Do not install C as a verified fix.
