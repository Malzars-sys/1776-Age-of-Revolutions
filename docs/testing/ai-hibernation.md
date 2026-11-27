# Dynamic AI Hibernation 0.4.2-dev

This branch is an experimental build for collaborator testing on **Victoria 3 Steam 1.15.2**. It contains the full 1776 Age of Revolutions mod. Use a fresh 1776 solo campaign with Ironman off. Keep separate saves for tests.

## Switch branches

Run these commands from your existing clone. Commit or stash any work you want to keep before switching.

```sh
git fetch origin
git switch --track origin/beta/ai-hibernation
```

Use the local testing branch to retrieve subsequent updates.

```sh
git switch beta/ai-hibernation
git pull --ff-only
git rev-parse --short HEAD
```

Use the existing local 1776 Age of Revolutions entry in the launcher. Enable that entry in a test playset, and disable earlier hibernation overlays and other UI or AI mods for the initial comparison. Launch from the mod checkout that you switched to the testing branch. If Git reports a long Windows path inherited from production, enable long paths for this clone with `git config core.longpaths true`.

Close Victoria 3 before switching back to production.

```sh
git switch main
git pull --ff-only
```

## Compare the two AI settings

In the new-game rules, **Minor Country AI** defaults to **Hibernation**. The rule permits eligible countries in the 266-tag cohort to sleep after initialization. The number actually placed in hibernation depends on campaign conditions and protected countries. On the previous 1.15.2 overlay trial as France, the February autosave showed 385 active and 261 dormant controllers. Use that result as a reference for the same starting conditions.

For a control run, start another new campaign and choose **Full AI** under **Minor Country AI**. The mod should leave the native AI running in this campaign. Use the same country, date, DLC, game settings, launcher playset and autosave interval in both runs.

Record the wall-clock seconds to advance 14, 28, 56 and 180 simulated days from a common start date. Do a paired run at speed 4 and a separate pair at speed 5. Alternate which rule you run first and repeat both settings before drawing a conclusion. Record unexpected pauses, autosave stalls, crashes, and any FPS or interface symptoms separately. Keep startup time separate from simulation time. Include hardware, OS, game version, branch commit, and the speed and rule used in each run. Any performance benefit still needs to be reproduced.

## Exercise diplomatic and military interactions

1. Start with Hibernation and let the initial batches finish. Preserve a test save before interacting with a country that was put to sleep. Use the game log or inspect the save to confirm that it was dormant.
2. Initiate a diplomatic play against that country through the game interface, or join a side involving it. Record the countries, start date, and type of play. Let time advance. Check the controller in a second save and look for an accepted `enable_ai <TAG>` in `logs/debug.log` if available.
3. Play separate cases where the target backs down and where the play becomes a war. Observe whether the target wakes when it needs to participate and stays active through the conflict. Record cooldown or re-hibernation observations after the conflict ends. The cooldown is 12 months.
4. If a protected country remains dormant, save again after the seven-day first deferred retry and any later 30-day intervals it survives. Collect saves before and after a reload if it changes the behavior. An order in the log records a dispatch. The native save's controller flag shows the actual AI state.

## Test the emergency button

Run the game in debug mode, open the native console in a Hibernation campaign, and click **Restore All Country AI**. The action requests activation for managed countries that could have been put to sleep and saves a campaign-wide suspension of hibernation. Let time advance so the requests can complete. Save and reload the campaign in normal mode, then check that the suspension persists and previously dormant controllers remain active. In a separate launch with debug mode off, verify the normal interface and confirm that the rescue control is unavailable.

Use a separate test campaign for this step. Once saved, the emergency suspension remains in effect for that campaign.

## Report findings

Use [Issue #57](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/57) for hibernation findings. Include the branch commit, game version, language, DLC, playset, debug status, AI rule, and exact in-game dates and tags. Share a short reproduction, what you expected, and what happened. When available, keep the relevant portions of `logs/error.log`, `logs/game.log`, and `logs/debug.log` with the before and after saves. Share saves through the team's agreed channel and omit unrelated logs and personal paths from public comments. Include all runs in benchmark reports, including slow runs and failures.

The branch is experimental. A permanently rejected engine command can leave a protected country dormant despite deferred attempts. Current coverage leaves some startup conflicts, country formation and release, and native console interaction to be exercised by collaborators.
