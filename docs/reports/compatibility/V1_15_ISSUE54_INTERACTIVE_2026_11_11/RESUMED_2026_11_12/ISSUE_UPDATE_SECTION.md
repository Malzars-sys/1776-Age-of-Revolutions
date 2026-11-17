## 2026-11-12 continuation — partial desktop control; no valid A/B results

**Issue remains open. No technology-tree performance fix or speedup has been verified.**

The supported Windows controller was resumed with the maintainer's authorization. It could launch Steam/Paradox, capture the real game, and reach **France paused on 1 January 1776** in isolated profile A1. This supersedes the earlier capability note that no game input had been sent.

The available automation was insufficient for a controlled tree trial:
- Keyboard commands did not produce reliable in-game results, including menu/console access; mouse interaction did not establish a repeatable tree-opening/tab sequence. The windowed game also extended above the screen.
- A fullscreen world-initialization capture stopped returning frames (`FrameArrived timed out`). A later windowed session was capturable; this is an observation, not proof of a rendering/performance fix.
- Ordinary process enumeration from the command tool could not see the Steam-launched game. A direct-launch helper could read only its owned child, but no CPU capture was requested in an established tree state.
- Task Manager reported higher Windows integrity than the controller. No input, elevation, installation, or access workaround was attempted there.
- Native low-FPS text was seen on changing map views, **not a controlled technology-tree sample**. `3dstats` is referenced by the native debug GUI but was not activated and verified in a measured tree session. Controller call durations are not click-to-render latency.

**Results: zero new startup CPU benchmarks; zero valid tree CPU, FPS/frame-time, opening-latency, or repeated A/B captures.** The normal game installation has no speculative GUI optimization installed.

Direct launches reported Steam API initialization failure. A subsequent launch through the actual Steam and Paradox interfaces used the same pinned Steam 1.15.1 executable and isolated A1 user directory without that warning in its current log. These setup attempts must not be compared as A/B arms; the actual DLC mask still needs to be fixed and checked for all measured runs.

Cleanup is complete: Steam launch options were restored to their original empty value and verified in Properties. No Victoria 3 game window remained at final observation. The seven existing playsets, eleven mod associations and fifty-one DLC association rows retain their contents; only the playset sync timestamp changed. Normal settings now explicitly contain the application's display defaults (fullscreen, display 0, VSync true); no old database/settings copy was restored over current data. The source autosave remains byte-identical.

The copied autosave candidate was identified as **Russia 1870** and rejected. Only its four isolated copies were archived outside the selectable save folders. A common France-1776 save still needs to be created. A1/B1/B2/A2 settings have been aligned, with their previous settings retained.

### Separate predicate diagnostic

`C_simplified_gui` still changes only two visibility expressions in `gui/tech_tree.gui`; technology definitions are unchanged. The static boolean model compared 584 cases per predicate (1,168 total) without divergence. Parenthesis depth drops 44→9 and 45→11; textual `GetTechnology` calls drop 42→40 and 43→42. **This is neither engine verification nor a measured optimization, and C has not been promoted to the normal mod.**

### Next actionable test

Use the prepared **A1–B1–B2–A2** profiles with manual in-game actions, the same Steam 1.15.1 executable, the same actual DLC mask/settings, and one France-1776 paused save copied among profiles. Record closed-map and Production/Military/Society stationary/pan phases for 15 seconds each, then three warm reopenings. Use fixed zoom and left-drag panning. Capture actual click-to-render transitions with video and native FPS/frame-time output where exposed. The existing UI-only CPU collector can be run from the maintainer's ordinary Windows session, with no elevation; failed access stays unmeasured.

Exact Steam user-directory options, `3dstats`, save-copy commands and CPU capture commands are in:
- `docs/reports/compatibility/V1_15_ISSUE54_INTERACTIVE_2026_11_11/RESUMED_2026_11_12/MANUAL_TEST_FR.md`
- Findings and limits: `.../RESUMED_2026_11_12/REPORT.md`
- Cleanup/preservation receipts: `STEAM_RESTORATION.json`, `PREPARED_HANDOFF_CLEANUP.json`, `NORMAL_PRESERVATION_REVIEW.json`, `NORMAL_SETTINGS_DELTA.json` in that directory.

Do not resume startup-only benchmarks. Compare A versus C separately after an exploitable A/B series; a possible B improvement would not by itself isolate the predicates.

---

## Earlier investigation and prepared artifacts (retained as history)

