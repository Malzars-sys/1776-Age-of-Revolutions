# CLEANUP-1E — MARATH Final Acceptance

## 1. Baseline

- Repository: `1776_Age_of_Revolutions_fork`
- Branch: `cleanup-post-release`
- Historical starting HEAD: `1e374f2f40252d229bc249600e3cbbe26085122d`
- CLEANUP-1B, 1B.1, 1C, and 1D remain non-committed working-tree work.
- Protected stash: `stash@{0}` at `518df704fa14599c0f254fae13859210663dd976`.
- Codex did not launch Victoria 3 for CLEANUP-1E. Final runtime evidence was supplied by the user.

## 2. Work recovered from historical stash

CLEANUP-1A audited the historical `WIP NAVY-3C-3 Maratha Konkan Flotilla` stash without applying it. CLEANUP-1B then rebuilt the feature manually from current HEAD, retaining only validated intent: the `Konkan_Flotilla` identity, South India naval HQ, frigate ship type, and EN/FR localization concept. Obsolete ship-level `state_region` syntax and the unvalidated one-frigate balance were not restored.

The protected stash was never popped, applied, or altered. Historical research and vanilla crew scaling independently produced the final two-frigate setup.

## 3. Historical naval reconstruction

The reconstruction represents the documented Peshwa naval establishment at Vijaydurg under Anandrao Dhulap in 1776. Two game frigates are a conservative manpower abstraction, not a claim of exactly two European-pattern historical hulls.

Vanilla 1.13 gives `ship_type_frigate` a 500-sailor requirement. Two frigates therefore require 1,000 sailors, matching one fully supported level of `building_naval_administration` with `pm_simple_sailor_recruitment`.

## 4. Konkan Flotilla final setup

```text
country = MARATH
name = Konkan_Flotilla
type = fleet
hq_region = sr:region_south_india
ship_type = ship_type:ship_type_frigate
ship_count = 2
naval_administration_level = 1
naval_administration_pm = pm_simple_sailor_recruitment
```

No ship of the line, obsolete naval combat-unit ID, `building_naval_base`, or ship-level `state_region` is present. The MARATH land formation remains at `sr:region_north_india`.

## 5. Anandrao Dhulap

`MARATH_anandrao_dhulap` is defined once and instantiated once. He remains:

- an admiral commanding `Konkan_Flotilla`;
- age 40 at the scenario start as a documented technical approximation;
- culture `cu:marathi`;
- home region `STATE_BOMBAY`;
- free of duplicates.

The runtime displayed him as the assigned MARATH naval commander, satisfying the Commander Completeness Rule.

## 6. Naval Administration diagnosis

Vanilla tracing confirmed two separate buildings:

| UI role | Internal ID | Mechanical role |
|---|---|---|
| Naval Administration | `building_naval_administration` | `recruits_sailors = yes`; 1,000 sailors and ten 100-sailor assignments per fully supported level |
| Naval Logistics Center | `building_naval_logistics_center` | Auto-placed fleet logistics; no sailor-capacity PM and no ship-crew assignments |

The MARATH history script always used the correct Naval Administration ID and `pm_simple_sailor_recruitment`. The earlier runtime inspected the auto-placed logistics building while the true recruitment building had failed to materialize/function.

## 7. Admiralty runtime A/B result

### Without Admiralty

- new MARATH campaign loaded;
- Konkan Flotilla, two frigates, South India HQ, and Anandrao Dhulap were present;
- the separate auto-placed Naval Logistics Center was visible;
- the true Naval Administration was absent/non-functional;
- fleet crew remained `0 / 1,000` after 49 days;
- the fleet Building/Crew table was empty.

Historical CLEANUP-1C verdict: **FAIL** for naval recruitment.

### With Admiralty

The user added exactly:

```text
add_technology_researched = admiralty
```

and started another new MARATH campaign on 1 January 1776. Runtime then showed:

- Admiralty researched;
- true Naval Administration present at level 1;
- Naval Logistics Center still present separately;
- Konkan Flotilla at South India HQ with exactly two frigates/Cruisers;
- Anandrao Dhulap still assigned;
- fleet crew `1,000 / 1,000`;
- both frigates fully crewed;
- MARATH land HQ still North India.

Final runtime verdict: **PASS**.

## 8. Temporary technology compromise

The country-history diff adds one and only one technology line, `add_technology_researched = admiralty`, beside the existing tier-5 and `international_trade` initialization. No other country-history line changed.

This grant is accepted temporarily because the runtime A/B test proved that a `create_building` history entry does not bypass the current vanilla 1.13 unlock in this MARATH setup. It is a compatibility compromise, not a claim that MARATH possessed the same naval institution as the leading European powers.

## 9. Future technology-overhaul requirement

The `Naval Progression Access Rule` in `docs/design/1776_PROJECT_INVARIANTS.md` remains binding. The future technology overhaul must replace this temporary Admiralty grant with progressive access that lets regional naval powers:

- maintain an existing navy;
- recruit sailors;
- develop limited coastal infrastructure;
- expand an appropriate regional fleet;

without placing them at the institutional naval level of Britain, France, Spain, or the Netherlands.

```text
MARATH_TEMPORARY_ADMIRALTY_GRANT = YES
FUTURE_NAVAL_TECH_REWORK_REQUIRED = YES
```

## 10. Static validation

Final static validation covers the MARATH country diff, building level and PM, formation and ship count, commander definition and transfer, naval and land HQs, absence of legacy syntax, character/localization BOMs, EN/FR keys, balanced braces, Git whitespace, and index state.

The audited manual country change consists solely of one Admiralty line. No technology definition, scripted tier effect, production method, building definition, or technology-tree file is modified.

Final results:

- MARATH country history: 3/3 braces; tier-5 effect once, `international_trade` once, `admiralty` once; diff `+1/-0`;
- MARATH Bombay history: exactly one Naval Administration, level 1, with `pm_simple_sailor_recruitment`; no scripted Logistics Center;
- MARATH formation: one Konkan fleet, one South India naval HQ, exactly two frigates, one North India land HQ;
- no ship of the line, legacy naval combat-unit ID, `building_naval_base`, or `state_region` inside the ship block;
- Anandrao template creation and transfer each occur once;
- brace counts: buildings 704/704, formations 141/141, character template 2/2;
- character template and both localization files begin with `EF BB BF`;
- EN/FR `Konkan_Flotilla`, `Anandrao`, and `Dhulap` keys each occur once;
- `git diff --check` passes and the Git index is empty.

`V13_STATIC_VALIDATION = PASS`.

## 11. Runtime acceptance

The user-provided final runtime is accepted as the decisive A/B result:

```text
MARATH_FINAL_RUNTIME = PASS
KONKAN_FLOTILLA_FINAL = PASS
NAVAL_ADMIN_LEVEL = 1
NAVAL_ADMIN_CREW = 1000/1000
ADMIRALTY_REQUIRED_BY_CURRENT_V13_SETUP = YES
```

Codex did not launch or relaunch Victoria 3 during CLEANUP-1E.

## 12. Protected-state verification

The final protection audit checks:

- protected stash hash unchanged;
- all seven technology-research files still untracked, unstaged, and byte-identical;
- `bject` absent;
- BIC retaining `activate_law = law_type:law_frontier_colonization` and not containing `law_colonial_exploitation`;
- no staged file and no prohibited Git mutation.

Final protection results:

- `stash@{0}` remains `518df704fa14599c0f254fae13859210663dd976`;
- all seven protected files remain `??` untracked, unstaged, and retain their recorded SHA-256 hashes;
- `bject` is absent;
- BIC contains `activate_law = law_type:law_frontier_colonization` and no `law_colonial_exploitation`;
- no file is staged.

## 13. Final verdict

CLEANUP-1 is accepted. The final setup combines the historically supported two-frigate Konkan force, the historically attested Anandrao Dhulap, the correct vanilla Naval Administration and PM, and the minimum current-version technology concession proven necessary by the runtime A/B test.

The concession is explicitly temporary and leaves the future progressive naval-technology requirement open. Subject to the final protection and static checks recorded in this phase, the complete CLEANUP-1 change set is safe to commit as one intentional unit. CLEANUP-2 has not begun.
