## Review delivery — Hawk, 2026-11-09

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. [Development Roadmap](https://github.com/users/Malzars-sys/projects/1/views/1): In review, verified in the issue sidebar. The issue remains open; engine and human acceptance are pending.**

Installed locally against canonical Victoria 3 **1.15.0**; no code commit/push, native edit or historical population redistribution.

- Restored **two actual compatibility culture definitions**, `north_caucasian` and `siberian`, in five new runtime files. They are not aliases to one current native culture. Exact prior colors, default religions, name pools (54 entries), graphics and ethnicity weights are retained.
- Provenance: the two definitions and FR/EN names were read at the pinned game-data-mirror commit [fc8143b](https://github.com/tjysdsg/Victoria-3-files/blob/fc8143b83f54f8abed97fc556b556e4085b6e691/game/common/cultures/00_cultures.txt), identified there as the 1.9.0 update. This is a versioned mirror, not an official Paradox source or proof of the exact 1.13/1.14 payload.
- Adapted the obsolete trait fields to current native regional heritages, the Caucasian tradition where appropriate, and two explicitly geographic aggregate language traits/groups. These preserve the legacy categories without assigning every Siberian to Yakut/Evenki or every North Caucasian to one modern ethnicity. Other native cultures remain untouched.
- Acceptance limitation: North Caucasian heritage now follows the native regional **European** grouping, rather than the old Middle Eastern trait. The aggregate languages grant no invented linguistic affinity with distinct native cultures. No laws, assimilation rates, homelands or thresholds were changed; runtime behavior still requires testing.

### Reproduced population and reference evidence
- **109 typed consumers across 16 effective files**, including all 72 population records, 11 primary-culture references, 11 homelands, character/history/event consumers, and two native Russian customizable-localization branches.
- **591,979** authored North Caucasian persons and **150,297** Siberian persons: **742,276 before and after, difference zero**. Every affected record retains its complete block, size, owner/state, religion and other properties.
- All **6,815** effective authored population records and **18** population-source files are unchanged. Authored sums remain **837,328,654** globally, with identical totals for **677 states** and **644 owners**. These are script sums, not observed in-game population or a claim of measured prior loss.
- All 646 tags appearing in initial ownership instructions have nonempty, resolving primary-culture definitions in the static model. No dormant country was activated.

### Validation and protections
- Final live audit: **1,794/1,794 PASS_STATIC_ONLY**; **15/15** negative controls detected.
- Existing #24 audit: **324 effective cultures**, zero unresolved culture references, zero absent-culture population candidates and zero parser errors. Its overall result remains findings-only for the pre-existing 14 allocation candidates and four absent inherited native tags; those are not changed by #40.
- Existing population reader fails identically before/after on 108 pre-existing compact one-line records. Failure evidence is retained, its code and frozen baseline are unchanged, and the new parsed-record audit independently compares every record and state/country/world sum. No false green result is claimed for that old tool.
- All **2,509 pre-existing runtime inputs** captured by #40 remain byte-identical at the final source check. #39 journals, accepted #21/#27 inputs, map work, laws, starting technologies and common recipes are preserved. Two concurrent mine/subsistence files are explicitly recorded and retained, outside this delivery. HEAD/index and native inputs are unchanged.

Local evidence, **not committed/published**:
`docs/reports/compatibility/V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09/`

Start with `REPORT.md`, `STRATEGY.md`, `RUNTIME_PROTOCOL.md`, `LIVE_VALIDATION.json`, `MAP24_POST_INSTALL.json`, `FINAL_SOURCE_PROTECTION.json`, the installation/provenance manifests and population/reference CSVs.

### Remaining acceptance
Fresh 1776 game; Sakhalin/Chukotka and Caucasus examples; Russia and Poland-Lithuania witnesses; first tick and short simulation; fresh logs; save/reload; DLC-disabled configuration if available. No human/runtime box is checked by this delivery.

<details>
<summary>Initial assignment retained</summary>

## Current assignment — Hawk, 2026-11-09

**Claimed at the maintainer's request: “Prenez une mission.” Work begins with the migration strategy and source inventory. No gameplay correction or runtime acceptance is claimed yet.**

- Bounded scope: resolve the missing `siberian` and `north_caucasian` culture providers/consumers for 1776 while preserving authored population amounts and unrelated properties.
- First step: verify the complete consumer inventory and recover documented prior definitions before choosing between a compatibility definition and a historically supported per-record migration. No blanket replacement with one current culture or native 1836 distribution.
- Preserve the installed #24 structural fixes, #39 journal migration, accepted #21/#27 scopes, historical borders and other agents' work. No Git write or vanilla modification.
- Requested Project #1 status: **In progress**. The issue remains open; this body update does not itself confirm a Project-field transition.
- Local ownership record: `docs/reports/compatibility/V1_15_ISSUE40_REMOVED_CULTURES_2026_11_09/CLAIM.md`.


</details>

---

## Problem and evidence

Canonical Victoria 3 **1.15.0** registers neither `siberian` nor `north_caucasian`, while the 1776 mod still uses both.

The #24 effective-provider audit records:
- **22 unresolved country-primary-culture / homeland references**.
- **72 authored create_pop records** across seven population files: 54 `north_caucasian` records totaling **591,979**, and 18 `siberian` records totaling **150,297**; **742,276 authored persons in total**. This is a sum of script values, **not measured in-game population loss**.
- Five country IDs using these cultures also appear in initial state-ownership scripts: **SKH, ULT, CKC, ABK, CAUC**. Other affected country definitions may be dormant.
- Additional literal culture consumers are inventoried in non-journal scripted effects/events. No automatic substitutions or population edits were made by #24.

Local reproducible evidence, not committed/published: `docs/reports/compatibility/V1_15_ISSUE24_MAP_DLC_2026_11_09/FINAL_AUDIT_RESUMED.json` (`initial_pop_culture_candidates`, `findings`, `script_literal_dependency_candidates`), plus the final findings report.

**Parent workstream: #24. Release dependency: #25. Suggested priority: P0 for initial population/country loading; runtime impact still requires reproduction. Requested Project status: Backlog.**

## Scope

Resolve the missing culture providers/consumers without silently changing the 1776 demographic design. First select and document a defensible migration strategy:
1. A narrowly scoped legacy compatibility definition is possible only with a verified prior definition/provenance and a review of current traits, names, graphics, acceptance and assimilation behavior.
2. Mapping to current native cultures requires a per-record/state review appropriate to **1776**, supported by relevant historical evidence. Do not copy the native **1836** proportions or assign an aggregate group wholesale to one modern culture.

Absence of a provider is confirmed statically; the exact runtime failure mode is not yet accepted. Do not invent aliases or suppress the audit to report success.

## Acceptance checklist

- [x] Inventory every definition, primary culture, homeland, population record, event/effect consumer and necessary FR/EN localization using the two IDs.
- [x] Document the chosen technical/historical strategy and its provenance before installation.
- [x] Preserve each authored population record's size, owner/state scope, religion, profession and all unrelated properties, unless an independently authorized historical correction explicitly changes them.
- [x] Keep existing total/region/country population checks, and publish any approved classification changes separately from numerical changes.
- [x] Verify effective providers are unique, all references resolve, and no starting country has an empty/invalid primary-culture set.
- [x] Use bounded patches and source hashes; include meaningful negative controls.
- [ ] Test a fresh 1776 game: representative affected populations/countries, Russia and Poland-Lithuania witnesses, initial/first-tick data, fresh logs and save/reload. Keep static and human acceptance separate.

## Boundaries

Canonical vanilla is read-only. Preserve #39's journal work, accepted #21/#27 scopes, historical borders/resources/ownership, the map overhaul #18 and law audit #17. Do not create the four missing inherited 1836 country IDs or grant technologies as part of this culture task. Do not launch this implementation merely because the issue was created.

Follow repository instructions for territory/demography, historical sources and localization; no Git write or publication is authorized by this tracking entry.

