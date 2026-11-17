# Issue 54 — interactive investigation and retained history

> **Latest results, 12 November 2026:** the controlled A1–B1–B2–A2 series is complete,
> with 20 actual UI captures and 44/44 technical checks passing. See
> [the measured comparison](AUTHORIZED_RETRY_2026_11_12/REPORT.md).
> Current GUI: approximately 7–9 FPS in the tree; vanilla-GUI witness: 27–42 FPS.
> No performance correction is installed; diagnostic C remains engine-untested.
> The handoff and stopped attempts below are retained history, not current status.

Historical attempt: continuation began 11 November 2026; handoff followed the maintainer's stop
instruction on 12 November, Europe/Paris. Investigation remains incomplete.
No technology-tree performance result or verified fix is claimed.

## Available interface and observed limitation

The supported bundled `@oai/sky` controller through `mcp__node_repl__js` is
available. Initialization, app/window enumeration and a screenshot request
succeeded. Victoria 3 window metadata was selected, but its captured image
showed another foreground application. No keyboard, click, drag or scroll
input was sent. Reliable foreground game capture/input remains unvalidated.

The maintainer replied: “Stop the interactive test and give me the manual
steps.” The owned launch session was stopped. A subsequent read-only inventory
showed zero remaining Victoria 3 windows. No further launch or input was sent.

AutoHotkey was not found on PATH or inspected common installation paths.
Power Automate Desktop was not found in the inspected paths, but Appx inventory
was access-denied, so its installed status is not established. Windows
Performance Recorder exists but no trace was started; PresentMon was not found
in inspected locations. No installation, elevation, raw input-injection or
security/authorization workaround was attempted. The native debug GUI exposes
`3dstats` as an FPS/performance display candidate, not yet observed in-game.

## Controlled preparation, no comparative measurements

Four separate user profiles are prepared for A1–B1–B2–A2, using the same Steam
1.15.1 executable, SHA-256:
`fb4ec0698afd3d3b1a785926d57bd5d68c95a4afd04b56f6bd45abd7a5672b15`.
All four current settings files are identical. No normal launcher database,
settings, mod registration or playset was changed.

The first A1 helper ended before a persistent UI session was available. The
helper was corrected to hold its own tool launch session open. The second
attempt produced the enumerated game window. Fresh logs confirm 1.15.1,
revision `7a630cdf29e`, the A copy and only the preorder soundtrack. Direct
launch still reports failed Steam API initialization, so this is not an
authenticated-Steam reproduction. B1/B2/A2 were not launched in this continuation.
Local 1.15.0 + DLC remains a separate environment.

**Zero startup CPU benchmarks, UI CPU samples, FPS samples, frame-time samples
or A/B comparisons were performed in this continuation.** No responsiveness
is inferred from a window, Responding flag, CPU startup activity or screenshot
call duration. All 28 handoff result rows remain NOT_MEASURED.

## Separate visibility diagnostic

`C_simplified_gui` is an isolated copy of A. Only `gui/tech_tree.gui` changes;
reversing its two changed expression spans reconstructs A's GUI bytes exactly.
No technology, prerequisite, era, unlock, country or historical definition changes.

| Predicate | Expression characters | GetTechnology tokens | Maximum parenthesis depth |
| --- | --- | --- | --- |
| Edges | 3,713 → 3,521 | 42 → 40 | 44 → 9 |
| Cards | 3,158 → 3,078 | 43 → 42 | 45 → 11 |

Counts above exclude the visible-property wrapper counted in the prior report.
The diagnostic balances OR chains and removes redundant identity checks,
preserving compatibility hiding and the two force-shown cards in the model.
Each predicate matches across 584 cases: all 291 defined technology identities
plus an unknown identity and both ShouldShow states. Total: 1,168 comparisons.
Both deliberately wrong-alias counterexamples are detected. Referenced IDs exist.

Boolean equivalence assumes distinct valid technology identities. It does not
prove engine binding validity, evaluation order, caching, calls per frame or
speed. C has not been launched, benchmarked or installed as a permanent fix.
If B repeatedly improves, A versus C is the separate predicate-isolation test.

## Verification and preservation

FINAL_STATIC_VALIDATION.json passes **25/25 static checks**, covering 3,776 A
files, 3,775 B files and 3,776 C files. Only the intended GUI omission or two
expression spans differ. Technology definitions are byte-identical. Captured
normal mod files, launcher database/settings/content-load and Git index are
unchanged, as is the pinned executable. Both helper scripts pass PowerShell
syntax parsing; neither was run as an additional benchmark.

No Git write, native edit, normal playset change or In review/Done transition.
Prior startup reports and ZIPs remain historical, not tree measurements.

## Next actionable test

Follow MANUAL_TEST.md, also copied to the prepared lab's runtime_ui_controlled
folder. Launch each label serially; establish the same paused France save on
1 January 1776 and visible settings; open/warm all three tabs; observe stationary
and identical left-drag panning behavior at fixed zoom; repeat A1–B1–B2–A2.
The launcher uses isolated profiles without normal registration/playset edits.

The CPU wrapper starts only after a person declares an established UI state,
allows five seconds to return focus, then collects fifteen seconds of CPU.
It never launches a game, measures startup, produces FPS or verifies UI state.
Opening latency/FPS need actual UI observations. Leave frame times unmeasured
unless a trustworthy display/capture exposes them. Copy the test save only
between isolated profiles. Keep authenticated/direct-launch Steam conditions
and the local 1.15.0 + DLC environment separate.

Evidence: PREPARATION, CAPABILITIES_AND_STOP, VISIBILITY_DIAGNOSTIC,
FINAL_STATIC_VALIDATION, POWERSHELL_SYNTAX, stopped-launch logs and
UI_RESULTS_TO_FILL. Root cause and performance improvement remain unestablished.
