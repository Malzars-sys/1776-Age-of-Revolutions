# Ottoman inactive journal visibility and Russian starting Caesaropapism

Date: 2026-11-08 (Europe/Paris). Status: **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Installed in the regular local mod. No engine run, human acceptance, local Git write, remote publication or vanilla modification is claimed for this follow-up.

## Requested behavior and diagnosis

The maintainer requested that the Sick Man of Europe be visible as a future entry in the Ottoman Decline group, and reported that Russia lacked its specific native state-religion law at game start.

The current `je_sick_man_main` already belongs to `je_group_1776_imperial_crises`, localized as **Déclin ottoman**. Its lack of an `is_shown_when_inactive` block meant it was not presented before the scripted political-failure continuation. The canonical 1.15 journal documentation states that this visibility defaults to no, while automatic eligibility defaults to yes. Adding only visibility would therefore activate it prematurely. The existing Ottoman introductions also document that an already precreated inactive entry must be activated through eligibility rather than added a second time.

For Russia, the mod's same-path `00_church_and_state.txt` masked native `law_caesaropapism`. The prior November 7 Russian-law audit correctly identified this missing definition and its suitability for review, but the subsequent restored Russian-law file contains only Third Section and Official Nationality. Russia's current country history still explicitly selected generic `law_state_religion`. The new request authorizes restoration and starting adoption of Caesaropapism, without adopting the entire native 1836 profile.

## Installed changes

1. `common/journal_entries/00_sick_man.txt`: the main entry becomes visible while inactive for initialized Ottoman campaigns, unless the political path has succeeded or the Sick Man path has already been completed. Activation is explicitly gated by `ottoman_1776_sick_man_started`, set by the existing delayed failure event. Its condition has a short localized explanation in French and English. The inactive counter returns zero while `sick_man_var` does not exist, and the original counter value once initialized.
2. `common/scripted_effects/1776_ottoman_reform_effects.txt`: retain the original initializer, modifier, counters, flags and reform subentry additions. The main entry's manual addition is now a fallback only when neither an active nor an inactive instance exists. This preserves the old-save/manual path while letting a precreated entry activate through its new eligibility gate.
3. `common/laws/1776_v115_caesaropapism.txt`: restore the complete native 1.15 Caesaropapism definition in a separate file. It is token-equivalent to the installed native definition, including parent, modifiers, visibility, callbacks, AI and imposition rules. No technology or DLC gate is invented.
4. `common/laws/00_church_and_state.txt`: add the exact native `NAND` visibility clause to generic State Religion, so eligible Russia and eligible Orthodox Russian subjects see the specific variant in its place. The existing Millet/People of the Book exclusions and all other generic-law fields remain unchanged. All other laws in this shared file are unchanged.
5. `common/history/countries/rus - russia.txt`: replace the single generic State Religion activation with `law_caesaropapism`. Every other byte in the profile is retained, including military bureaucrats, the noble amendment, technologies, internal colonization, Cossacks and colonial investment.
6. Two UTF-8-BOM localization files, `localization/{french,english}/1776_ottoman_sick_man_visibility_l_*.yml`, supply only `aor1776_sick_man_activation_tt`. Native Caesaropapism names, description and icon are inherited without duplication.

There are seven changed/added gameplay/localization files. The main journal's original completion/timeout outcomes, four-reform goal and 10,950-day duration are unchanged. Its seven sibling reform definitions are token-identical. Political success/failure conditions and the one-day delayed event are unchanged. No reform starts merely because its future heading is visible. No subject is automatically assigned the Russian law by this lot; the copied native subject eligibility remains available for normal play.

## Historical and technical sources

- Canonical local Victoria 3 `C:/Games/Victoria 3/game`, current local 1.15 installation: `common/laws/00_church_and_state.txt`, `common/history/countries/rus - russia.txt`, `common/scripted_triggers/00_ip5_victoria_scripted_triggers.txt`, English/French `laws_l_*.yml` and the native Caesaropapism icon.
- Native `common/journal_entries/journal_entries.md:25–68`: inactive visibility, automatic eligibility, manually added journals, inactive-instance lifecycle and activation callbacks. Native `00_player_objectives_great_game.txt` uses a guarded variable read in its current-value block; script-value conditionals are also used in `08_tsarpoints.txt`.
- Existing `V1_15_RUSSIAN_LAWS_AUDIT_2026_11_07/REPORT.md`, H1 and catalogue: this was an audit-only finding, not evidence that the law had already been installed or observed active.
- [Presidential Library, The Synod in Russian state history](https://www.prlib.ru/node/1827019), collection description, consulted 2026-11-08: the 1721 Spiritual Regulation/Synod and the 1722 chief procurator directly subordinate to the monarch support using the game's Caesaropapism abstraction in 1776. This is an interpretation of the game's category, not a claim that a Russian statute in 1776 bore that name.

The state confession is not changed by the law copy. The request concerns the native law variant governing the relationship between the Orthodox Church and the state.

## Checks actually executed

Command, from the repository root:

```powershell
python -B docs/reports/compatibility/V1_15_OTTOMAN_VISIBILITY_RUSSIAN_RELIGION_2026_11_08/CHECKS.py
```

Result: **76 checks passed, PASS_STATIC_ONLY**. The receipt is [VALIDATION.json](VALIDATION.json).

- Independent syntax readers parse the changed definitions. The original main fields/outcomes, seven sibling journals, original starter behavior except the explicit instance guard, other scripted effects and other shared church/state laws are preserved.
- Predicate fixtures cover early Ottoman visibility, pre-initialization, another country, failure before the delayed event, initializer completion, political success and concluded reforms. Inactive visibility alone does not satisfy activation.
- Counter fixtures cover an unset variable and reform values 0–4. The counter is safe before initialization and preserves active reform counts.
- Four active/inactive-instance combinations verify that the manual fallback is available only when no instance exists.
- Native law token equivalence, unique effective definition, parent resolution, inherited subject helper, native icon and English/French localization are checked. Visibility fixtures cover Russia, another independent country, eligible and ineligible Russian subjects, a theocracy and Ottoman Millet.
- The Russian profile differs by exactly the requested activation identifier; all other profile content matches the captured current version.
- New tooltip keys are unique, UTF-8-BOM encoded and reference existing journal-title keys.
- **4,823 protected functional/tracking text files** retain their hashes. No concurrent differences were found in that checked set. Archived research images/PDFs and old experiment copies are not part of the final rehash; they were not written. Local HEAD/index and both checked native source files are unchanged.

Initial current bytes, hashes and installation scope are recorded in `before/`, `BEFORE.json` and `INSTALLATION.json`. The installer verified all shared source bytes immediately before its bounded writes. No earlier baseline was restored. Previously installed war-support fixes, maps, SERG/WORLD tracking, other Russian-law work and technology/economic work remain outside the write scope.

## Engine acceptance still required

1. Fully restart the game. Start a fresh 1776 Ottoman game, pass the introductory choices and inspect **Déclin ottoman**. The Sick Man must appear as an inactive grey entry, with a readable activation condition and no running reform deadline or active Sick Man modifier.
2. Check the political-failure continuation: after the existing delayed event, the main entry should become active once, with its original duration, zero initial progress and original reform subentries. There must be no duplicate-add or missing-variable error. Successful completion of the preceding political path should remove the future crisis from the inactive list.
3. Start a fresh Russian game. In Church and State, verify **Césaropapisme** is active from the start and generic State Religion does not appear as a competing selectable equivalent. Verify the existing military-bureaucrat, noble-amendment and Cossack/internal-colonization setup remains present.
4. Save/reload the inactive Ottoman stage and a running reform stage, then advance. Confirm visibility/activation persists and the continuation does not initialize twice. Retain any new relevant log errors.

These tests have not been performed. The predicate fixtures do not model the Paradox journal scheduler or certify how quickly automatic eligibility refreshes after the delayed event. A previous save is not automatically assigned a newly changed starting law; the Russian starting-profile check requires a new campaign. No retroactive law change or save edit is included.
