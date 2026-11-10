# Issue #36 — unpause crash: naval AI category diagnosis and targeted candidate

Date: 2026-11-06. Parent: #20; coordination: #19. Severity: **blocking / P0**.
Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Issue #36 stays **In progress**.
This is a high-confidence causal diagnosis with a targeted candidate, not a passed first-day test.

## Finding

All **25 effective mod ship types** lack the 1.15 field `ai_ship_category`. The canonical 1.15 documentation requires every ship type to belong to exactly one AI category (`common/ai_ship_categories/ai_ship_categories.md:9`; membership syntax in `common/ship_types/ship_types.md:8`). A ship's existing `ship_group` is a separate classification and does not satisfy this requirement.

The preserved minidump places the access violation inside **CNavyAI::UpdateAssignedFleetsWantedShips**. This name was recovered from an allocator's MSVC RTTI string in the captured stack, not from unavailable private PDB symbols. The captured allocator pointer has exactly the corruption expected when a category counter is incremented at index **-1**, immediately before its inline integer buffer.

These findings provide a substantially stronger explanation than the last journal error or the number of log messages. The first discriminating in-game test is the category-only candidate, preserving the complete dirty runtime content.

## Reproduction and exact evidence

User-confirmed path: fresh game → Sandbox → Russia → fixed mod start in 1776 → unpause only → Crash Reporter. The configured start is 1776-01-01 (`common/defines/00_defines.txt:2`). Default speed, actual debug state and whether the displayed date changed are not independently measured.

- Game 1.15.0, revision `6338547985dbc271523e149f362a6fd93dc62975`.
- Captured launch begins 15:10:30 UTC. Exception reports 2026-11-06 16:30:15 local time.
- Exception: `C0000005`; fault RVA `victoria3.exe+0x166730f`.
- Fault instruction bytes: `ff 50 10` (indirect virtual call through `[rax+0x10]`).
- Minidump SHA-256: `21eb08f55613427534270eb631f20414878ee8fd1ad8b6ebd388180648af2afd`.
- Examined executable SHA-256: `473186e8d8deba993651e0ae4cf02a003b02f5accb99b096a6a0a8bd9506cbaa`.
- Executable timestamp and fault bytes agree with the dump. Canonical installation is read only.
- Only the dirty local mod is listed in the captured content load; State and Revolution is listed in crash metadata.

The evidence archive already contains the complete dump, active and rotated logs, content-load record and workspace manifest. Raw dumps/logs remain private; no Crash Reporter submission was made.

## Dump analysis and causal inference

Measured evidence:

1. The object addressed by the captured RDI has RTTI `.?AVCNavyAI@@`.
2. A stack allocator's RTTI includes `SGroupAllocation` and `UpdateAssignedFleetsWantedShips@CNavyAI`.
3. The faulting virtual table pointer is `0x00008004901c3ce8`. The corresponding valid in-image integer allocator table is `0x00007ff6901c3ce8`, whose RTTI is `CPdxHybridInlineBufferAllocator<int,21,int>`.
4. The low 32 bits are unchanged; the high 32 bits have increased by **14**. The integer buffer begins eight bytes after that allocator's virtual-table pointer. Incrementing a 32-bit counter at buffer index -1 therefore increments the high 32 bits of that pointer.
5. The nearby fleet-counting helper contains an unchecked indexed increment at RVA `0x1667528`. The preceding loads obtain the classification object and its signed index before incrementing the category array.
6. A bounded arithmetic replay of fourteen index -1 increments produces the **exact captured pointer**. Replaying fourteen increments at valid category indices preserves the pointer. This is a memory-layout/model check, not execution of the game.
7. As an independent consistency check, the unchanged Netherlands setup contains fourteen ships across two fleets: 3 caravels + 2 galleys, then 1 frigate + 4 caravels + 1 ship of the line + 3 galleys (`common/history/military_formations/00_military_formations_europe.txt:3854` onward). All those types are uncategorized in the captured mod. The precise ownership interpretation of every binary object is not needed to establish the schema defect.

**Inference:** missing AI categories lead to an invalid/default category index during the first naval AI update; its unchecked counter update corrupts an adjacent allocator pointer and the subsequent cleanup crashes. The dump identifies the subsystem, method and characteristic corruption, and the scripts independently violate its documented input contract. A controlled first-day run is still required to confirm that the candidate removes this observed crash and to detect any subsequent blocker.

A read-only reproducer is included at `tools/compatibility/issue36_naval_ai_audit.py`. Its optional dump probe records measured registers/RTTI and explicitly labels interpretation as inference. It requires the matching executable and uses offsets specific to this captured build/frame; it is not a general debugger.

## All rotated errors reviewed

The retained `crash_comparison.json` selects logs by launch timestamp, not rotation suffix alone:

| File | Bytes | Attribution |
| --- | ---: | --- |
| error.1.log | 524139 | Current launch |
| error.2.log | 524265 | Current launch |
| error.3.log | 524150 | Current launch |
| error.4.log | 278302 | Current launch |
| error.log | 48162 | Current launch |
| error.5.log | 245830 | Earlier run; predates this launch and is excluded from its counts |

Current run: **11242 messages / 8353 exact signatures**. Preserved vanilla: **350 / 340**. There are **296 shared**, **8057 captured-mod-only**, and **44 vanilla-only** signatures. Scenarios and stages differ; mod-only does not mean newly introduced in 1.15 or responsible for this crash. Rotations of different log families are not paired just by suffix.

| Lead | Evidence and relevant source | Assessment for this exception / next test |
| --- | --- | --- |
| Missing naval AI categories | 25/25 mod ship types; canonical documentation requires one; dump identifies CNavyAI and category-counter-compatible corruption | **Highest-confidence cause, blocking/P0, #36.** Add only valid categories and repeat fresh Sandbox/Russia/unpause. |
| Missing strategic-region assignments and invalid AI region scopes | `error.2.log:287–291`: unassigned province xBD5671 and STATE_TARTARIA, STATE_CHUKOTKA, STATE_KAUNAS, STATE_GALICH without strategic regions. Definitions at `map_data/state_regions/09_central_asia.txt:144`, `14_siberia.txt:155`, `15_russia.txt:78,593`. 1912 invalid `region` links at mod `common/ai_strategies/00_default_strategy.txt:5119`; 76 each at inherited `common/scripted_triggers/00_ai_triggers.txt:1000,1001`, consumed at strategy line 2018 | Confirmed data defects and plausible independent AI risks, **major**, #24. The same `region` syntax remains in native 1.15 strategy line 7373, so it is not itself a removed command. No assignment/map edit is included. Retest after the naval fix; if another crash remains, compare its fault signature before a separate four-state assignment isolation. |
| Invalid-country relation assertion | `error.2.log:2267`, 16:28:32: “Attempted to create relations for invalid countries!” | Confirmed assertion, responsible relation not attributed; **major suspected**, #20/#24. It occurs during setup and execution continues into country selection. The dump does not identify a relation routine. Trace effective country/relationship inputs separately if still reproduced; do not add historical countries to silence it. |
| Legacy journal initialization/outcomes and duplicates | Unexpected old conclusion fields; 97 duplicate additions, including imperial situation entries. Last errors at 16:29:37 precede exception by about 38 seconds | Confirmed compatibility debt, **major**, #27/#24. No dump evidence connecting it to this naval allocator failure. Do not use the last log entry as a cause or migrate all journals during #36. |
| Naval AI planning overrides | Old default strategy has no `ai_ship_category_weights` / `fleet_compositions` blocks found in native 1.15 | **Unverified functional risk**, #21/#24. Category membership fixes the invalid input; it does not certify future AI fleet composition. Observe AI behavior after the first-day gate before expanding scope. |

## Smallest targeted correction

Gameplay delta: **25 added lines in three files**, no removed lines.

| File | Relevant old locations | 1.15 correction |
| --- | --- | --- |
| `common/ship_types/00_ship_types.txt` | 21 type definitions, line 2 through line 1808; first group at line 3 | Copy the category for each identical vanilla type key. Final first category is line 4. All 21 match canonical 1.15. |
| `common/ship_types/10_1776_early_ships.txt` | Caravel line 6, galley line 79, cog line 156 | Final category lines 8, 82, 160 respectively: battle_line, screens, transports. |
| `common/ship_types/1776_usa_armed_merchantman.txt` | Type line 2, group line 3 | Final line 4: battle_line, preserving its existing capital-ship role. |

Custom mappings use the existing gameplay roles: caravels/armed merchantman retain the line role; galleys retain cruiser/screen classification; cogs have transport-oriented carrying capacity. The native coastal-defense AI category is gated by ironclad technology, so assigning preindustrial galleys to it would introduce an unrelated AI construction restriction.

No stats, recipes, tech gates, ships, formations, laws, states, strategic assignments, sovereignty, POPs, copper capacities or journal outcomes are changed. No disable-AI workaround is shipped.

Correction commits on `hotfix/1.15`:

- `bbde2dba3c93685f4703981e77d55a405ad2a2c7` — 21 inherited types.
- `73328c5442983668dcdb2ddc3f33e6d66bdd6690` — three early hulls.
- `f5a24b06e703a9e6a66a340374c1fe33e6c96609` — armed merchantman.

Draft PR #34 now includes this candidate alongside the earlier copper-icon changes and assessment. Its title/body must describe that combined scope. No merge is authorized or performed.

## Executed checks

- Baseline effective-file audit: **FAIL_STATIC**, 25 missing categories, exit 1.
- Candidate effective-file audit: **PASS_STATIC_ONLY**, 25 types with exactly one category each, all references defined, exit 0.
- 21 native mappings independently compared with the canonical definitions; four custom mappings reviewed as above.
- Negative control: one candidate category changed to a nonexistent reference in a disposable fixture; audit detects exactly that undefined-reference failure.
- Removing the 25 new category lines restores each source file byte-for-byte in the local candidate; remote files were separately checked after commit.
- The original three source blobs match the captured local files and remote pre-fix files. No dirty historical content is imported into GitHub by this correction.
- **2465** captured runtime-script/map/localization files rehashed: **zero changes**. Local Git status remains exactly the original **1121** porcelain lines, on local main HEAD `52c42808bdb0748e69fbde3423bb5004b5b1f20a`.
- A separate local runtime snapshot was prepared outside the workspace: **2887 runtime files** checked. Only the three gameplay files differ; launcher display names are separately labeled for the test. Neither a playset change nor a game launch has been performed for it.
- Project #1 was read in the UI after implementation: #36 remains **In progress / P0**, with #19 and #20 still In progress. No issue was marked Done.

## Controlled runtime test still required

Use the separately prepared full dirty-runtime snapshot with the three patched ship files. Do not replace the dirty workspace with the clean remote branch or pull into it: that would change the historical/runtime baseline. The category-only snapshot intentionally omits the unrelated remote copper-icon edits.

1. Preserve current logs before launch. Select only the isolated test snapshot and the same DLC set; avoid loading the original mod simultaneously.
2. Record content-load path, build, actual debug state and speed. Start a **new** game through **Sandbox → Russia**, fixed 1776-01-01.
3. Unpause without other actions. Observe the displayed date pass January 1, pause on January 2 or later, and preserve active plus rotated logs.
4. Repeat with another fresh Sandbox/Russia game on the same candidate. If it crashes, preserve the new dump and compare module-relative fault address / RTTI before changing any other subsystem.
5. Once the first-day gate passes, simulate a week, save/reload, then advance again; inspect naval fleets and remaining critical errors. Longer #25 regression and human acceptance remain separate gates.

**Current runtime result: NOT RUN.** A prepared snapshot and passing static checks are not first-day success. Issue #36 stays open and In progress, and #20 remains open.

## Reproduction commands (read only)

```powershell
python tools/compatibility/issue36_naval_ai_audit.py --mod-root "<isolated candidate>" --vanilla-root "C:\Games\Victoria 3\game"
python tools/compatibility/issue36_naval_ai_audit.py --mod-root "<captured original>" --vanilla-root "C:\Games\Victoria 3\game" --dump "<preserved minidump.dmp>" --exe "C:\Games\Victoria 3\binaries\victoria3.exe"
```

Python 3 is required; on this host the WindowsApps Python alias does not run, so the installed runtime Python 3.12.14 was used. No third-party Python package was needed. Missing debugger binaries and unavailable package-network access did not prevent direct read-only minidump/PE inspection.

Microsoft format references consulted: [exception stream](https://learn.microsoft.com/en-us/windows/win32/api/minidumpapiset/ns-minidumpapiset-minidump_exception_stream), [AMD64 context](https://learn.microsoft.com/en-us/windows/win32/api/winnt/ns-winnt-context), [x64 unwind metadata](https://learn.microsoft.com/en-us/cpp/build/exception-handling-x64). These document binary layouts, not the game's private implementation. Game-specific conclusions above come from the preserved evidence and local 1.15 files.
