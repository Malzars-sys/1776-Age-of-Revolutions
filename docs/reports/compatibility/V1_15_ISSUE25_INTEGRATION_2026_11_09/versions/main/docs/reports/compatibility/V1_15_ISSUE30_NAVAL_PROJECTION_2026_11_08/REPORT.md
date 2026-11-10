# Issue 30 — five naval projection modifiers

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, 2026-11-08. Installed in the regular local mod. Runtime impact has not been measured and engine acceptance is pending.

The maintainer asked for another mission while a different agent handles #29. This lot claims #30 only; the two #29 treaty files and its tracking remain reserved to that agent.

## Correction and unit choice

Five exact modifier identifiers become `ship_power_projection_mult`, retaining their signed values and enclosing scopes:

| Object | Scope | Value retained |
| --- | --- | --- |
| `law_merchant_navy` | `modifier` | −0.1 / −10% |
| `law_diplomatic_navy` | `modifier` | +0.2 / +20% |
| `principle_navy_1` | `member_modifier` | +0.1 / +10% |
| `principle_navy_2` | `member_modifier` | +0.1 / +10% |
| `principle_navy_3` | `member_modifier` | +0.1 / +10% |

The current native definitions use the same multiplier at these same five sites with exactly these values. Native `00_modifier_types.txt` marks the multiplicative type `percent = yes`; its additive counterpart supplies flat projection instead. Using the additive type with these fractions would change the unit and intended scaling. Both the native scripts and the [official 1.15 release notes](https://steamcommunity.com/app/529340/announcements/) explicitly support the replacement. The executable was checked as version **1.15.0**.

The three principle definitions retain their existing level structure; this migration does not add three separately stacked bonuses. Existing `country_flagship_interest_gain_mult` entries remain untouched: they are distinct supported modifiers, despite sharing part of the old identifier's spelling.

## Exact scope and sources

Only **five lines in two gameplay files** change:

- `common/laws/00_navy_model.txt`: lines 17 and 154, corresponding to native lines 18 and 155.
- `common/power_bloc_principles/00_power_bloc_principles.txt`: lines 2069, 2098 and 2120, corresponding to native lines 1803, 1830 and 1848.

`MAPPING.json` records the five object/block/value pairs. The current local and branch files matched after BOM/line-ending normalization before installation. Original local BOM and line-ending conventions are preserved. No complete native file is imported.

All other tokens are preserved, including starting-law assignments, unlocking technologies, visibility, AI weights, enactment effects, imperial-federation exclusions, DLC gates, principle benefits, flagship bonuses and other bloc definitions. There are no new player-facing strings. Native English/French modifier labels and type definitions are inherited without same-path mod masks; their effective source content is part of the audit contract.

Canonical read-only sources are the two same-path native gameplay files, `C:/Games/Victoria 3/game/common/modifier_type_definitions/00_modifier_types.txt:2830,2838`, and `localization/english/modifiers_l_english.yml:547–550` / French counterpart `:506–509`. The release notes' modding section identifies the removed key and both replacement forms. Local definitions determine the precise values and units.

## Actual checks

- Local audit: **16/16**, `PASS_STATIC_ONLY`.
- Isolated remote-candidate audit: **16/16**, `PASS_STATIC_ONLY`.
- **7/7 negative controls detected** in each run: five wrong additive substitutions, a reversed merchant-navy penalty and an accidental flagship rename.
- Reviewed diff: only the five intended key substitutions; exact removed-key search in gameplay scripts is empty.
- **2,518 other captured files** are unchanged at the protection check. The two actively reserved #29 treaty files are tracked separately, excluded from this unchanged-file count and never written by this lot. The #28/#32 changes, accepted #26 setup, #17 law work and map/SERG/WORLD work are preserved.
- Local Git HEAD/branch/index and the five captured native source files are unchanged. No engine run, human attestation, local Git metadata write, vanilla write or main merge.

The read-only audit uses `CONTRACT.json` and the repository's existing parser; private input captures are unnecessary to repeat it. Run `python -B tools/compatibility/issue30_naval_projection_audit.py --self-test`. `VALIDATION.json` records the actual commands and output. These checks do not establish rendered tooltips or measured projection/involvement in the engine.

Keep #30 open / In review and the existing PR draft for the [targeted engine protocol](RUNTIME_PROTOCOL.md). #29 and its runtime validation remain owned by the other agent. Starting-law historical choices and technology prerequisites are outside this mechanical fix.
