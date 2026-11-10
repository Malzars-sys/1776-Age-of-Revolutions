# #46 — Annual event targets, 2026-11-09

Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Engine not launched; no human acceptance recorded. Canonical installation: `C:\Games\Victoria 3\game`, version 1.15.0.

The five absent annual event IDs identified by #45 now have providers. Their directly scheduled follow-up and required definitions were restored in six new runtime files. No pre-existing gameplay file, annual list or dispatch was edited. #45 was delivered before installation; its receipt is copied in `PEER45_COMPLETED_BEFORE_INSTALL.json`.

## Installed scope

| Runtime path | Objects and purpose |
| --- | --- |
| `events/zz_1776_v115_event46_marx.txt` | `marx_events.3` and its scheduled follow-up `.4` |
| `events/zz_1776_v115_event46_japan.txt` | `japan_events.32/.33/.34/.35` |
| `common/ideologies/zz_1776_v115_event46_state_socialist.txt` | Native `ideology_state_socialist` required by Marx.4 |
| `common/laws/zz_1776_v115_event46_labour_suffrage.txt` | Native law required by that ideology's law stances |
| `common/ideologies/zz_1776_v115_event46_communist_compatibility_alias.txt` | Nonrandom modern-ID compatibility definition required by the socialist helper |
| `common/scripted_triggers/zz_1776_v115_event46_communist_validity.txt` | Native validity predicate required by that compatibility definition |

Ten definitions, six files. No country created, no initial law/technology assigned, no event registration appended, no new localization or art.

## Qualification, sources and gates

Pinned source copies are under `native/`; source and installed SHA-256 values are in `CANDIDATE_MANIFEST_R4.json` and `SOURCE_PROTECTION.json`. These are technical porting sources, not new historical research.

| Object | Canonical source | Retained conditions and behavior |
| --- | --- | --- |
| Marx.3 | `events/karl_marx_events.txt` | Existing annual registration, `marx_happened`, `peoples_springtime_happened`, relevant author country/exile context, once-only flag. The two delayed branches remain 16 and 8 years. Added explicit author-global existence guard, explained below. |
| Marx.4 | Same | Exact native follow-up: publisher/author selection, socialist movement, alternative descriptions, literary trait, reward or suppression options and generated-name cleanup. |
| Japan.32 | `events/japan_events/ep2_japan_events_03.txt` | `dlc018`/`ep2_content`, JAP, foreign-trade/art-academy conditions; ukiyo-e state scope; prestige or temporary academy output branch. |
| Japan.33 | Same | Same DLC gate; Japanese culture, adult Meiji/Showa template ruler/emperor and cultural-majority movement. Temporary immortality and after-event cleanup retained. |
| Japan.34 | Same | Same DLC gate; JAP famine in an incorporated state with at least two whaling levels; selected state and native mortality/radical/loyalist effects. |
| Japan.35 | Same | Same DLC gate; Edo hierarchy, native hierarchy-law restrictions, absent Meiji variable, expensive grain and Kanto unrest/rice-farm/landowner-government conditions. |
| State socialist | `common/ideologies/01_character_ideologies.txt` | Exact native payload; socialism gates and law opinions preserved. It can participate later under native eligibility; no initial assignment. |
| Labour suffrage | `common/laws/00_distribution_of_power.txt` | Exact native payload, requiring socialism AND council republic; election and party-emergence behavior preserved, including native date check for electoral-confidence initialization. |
| Modern communist alias | `common/ideologies/01_character_ideologies.txt` | All native fields except the two random-selection weight bodies, both explicitly zero. |
| Communist validity | `common/scripted_triggers/00_victoria_scripted_triggers.txt` | Exact native predicate; eligible interest-group types and militant armed-forces condition retained. |

## Two intentional compatibility deviations

1. **Marx.3 requires `has_global_variable = big_communism_builder`.** The old authored Marx.1 sets `marx_happened` but does not establish this author global. The native optional `global_var:... ?=` block is insufficient as an existence prerequisite. The added guard prevents an authorless popup. No writer, fabricated author, automatic bootstrap, altered character template or change to the legacy Marx/Karla/Charlie choices was introduced. Therefore this delivery restores providers, not the complete natural reachability of the new Marx story. That separate integration remains unvalidated and outside this bounded lot.
2. **`ideology_communist_leader` has both random weights set to zero.** The mod already uses its legacy character `ideology_communist`. Adding the full native modern character weight would introduce another equivalent random selection. The modern ID is provided for explicit consumers, while legacy actors retain their IDs. This does not repair the broader pre-existing collision between the legacy character ID and native IG ID; whole-catalogue ideological parity is not claimed.

## Verification

Final authoritative result: `LIVE_VALIDATION_R4_INSTALLED.json`: **391/391 checks; 16/16 deliberate-regression controls**.

- Unique providers and typed dependencies of the ten definitions; one additional helper level. Dependency evidence contains 248 consumer/reference rows, including repeats, not 248 unique objects.
- Retained five annual registrations; no effect/trigger dispatch collision.
- Six events, ideology/law payload comparisons, with only the explicitly permitted deviations above.
- 45 French and 48 English unique required localization keys resolve, including aliases and conditional descriptions; no new text needed.
- Icon resources and event GUI-window names resolve statically. Actual DLC media playback and scope-dependent text rendering require the engine.
- 749 explicit `trigger_event` calls across the five audited script families have no missing literal target. This does not cover dynamic expansion or prove runtime reachability.
- Deliberate regressions: each of the ten definitions missing; removed DLC gate; wrong delayed-event duration; removed council-republic gate; missing French title; nonzero alias random weight; missing author-global guard. Each is detected.
- The existing annual action-list finding `on_memento_mori` remains outside #46. It was not hidden, stubbed or removed. No claim that all on_actions are clean.
- `SOURCE_PROTECTION.json`: **2,526/2,526 existing inputs unchanged**, five distinct canonical source files unchanged, all six installed files match final manifest. This protects authored Marx/Japan events, #45 dispatch/tool, map, TECH, laws and economy inputs captured in the baseline.
- No Git writes, vanilla changes, game launch, release or publication.

Reproduction from repository root:

```powershell
& 'C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -B tools/compatibility/issue46_yearly_event_targets_audit.py --controls --output docs/reports/compatibility/V1_15_ISSUE46_YEARLY_EVENT_TARGETS_2026_11_09/LIVE_NEW_TIMESTAMP.json
```

Use a fresh output name. The audit refuses evidence overwrites and writes only its own evidence; it does not install files or launch the game.

## Preserved investigation history

- R1: 303/306; two wrapper-key false positives corrected in the reader, plus one real missing modern communist dependency.
- R2: remaining missing communist-validity predicate; all 14 then-defined regression controls passed. Predicate restored in R3.
- R3: 390/390, 15/15 before the additional semantic author-context review.
- R4: the strengthened author requirement correctly rejected the unguarded installed revision (389/391). The first candidate overlay double-counted the same installed paths; the reader was corrected to replace only providers from the same path, preserving genuine duplicate detection. Candidate then passed 391/391 and 16/16.
- The first R4 installation attempt stopped on a Windows text-decoding error before any write. `LIVE_VALIDATION_R4.json` consequently still records the expected unguarded failure. Explicit UTF-8 reading fixed the installer invocation; `INSTALLATION_R4_RECEIPT.json` and final live evidence document the actual installed revision. Earlier evidence is retained.

Next action: grouped runtime review using `RUNTIME_PROTOCOL.md`. No acceptance, task closure or transition to a new mission is implied by this report.
