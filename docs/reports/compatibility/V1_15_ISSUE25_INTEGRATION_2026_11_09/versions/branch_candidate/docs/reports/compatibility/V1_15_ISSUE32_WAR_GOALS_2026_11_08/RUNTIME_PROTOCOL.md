# Issue 32 — engine acceptance, grouped with issue 28

Status: **NOT RUN**. Fully restart Victoria 3, keep the regular mod/playset `hhhh`, then start a new 1776 game. Record the actual version, DLCs, countries and save names. Keep separate saves before enforcement, after enforcement and before peace; controlled debug fixtures are test-only and must not be saved into mod files.

## 1. Initialization and original American war

- USA and Great Britain must still begin their existing independence war. Spain must remain neutral initially. Inspect the generated goals, participants, ownership, subjects and fronts; the patch does not replace this setup.
- Advance beyond day one and several weekly updates, then save/reload. Compare fresh/rotated logs with the accepted startup baseline. Check particularly for unknown infamy values, missing scopes or mirror errors.
- Play or use a separate controlled test save to conclude the American war. Check that the enforced result matches the chosen outcome and that no new country/subject/front anomaly appears. If a generated Annex Country goal is present, use it for the annexation test below; otherwise establish a separate valid controlled annexation conflict. Do not count an unexercised branch as passed.

## 2. Conquer State: enforcement, retaking and infamy

The existing Iraq/Persia conflict has Conquer State goals and offers a second start-date case. A separate ordinary conquest outside the imperial protections is also suitable.

- Before enforcement, inspect the state's conquest-infamy breakdown. It must use the current state-based components, not the old fixed-base/population-scaling formula twice. The exact amount depends on the actual state, world economy, aggressor and modifiers; no fixed number is prescribed.
- Occupy the full required objective and watch the displayed enforcement timer. When it fills, the state should transfer **while the war continues**. Check its owner, ongoing war participants, fronts and the goal list.
- Verify the dispossessed side receives the appropriate retake goal, with no additional infamy from that mirror. A claim may make it a Return State goal rather than Conquer State; this is native behavior.
- From a separate save, retake/control the objective long enough for the reverse goal to enforce. Confirm ownership and fronts update correctly. Conclude the war and verify the peace summary agrees with the actual result, including a goal already enforced mid-war.
- Save/reload before and after enforcement. No duplicated transfer or mirror, lost scope, or restored old owner merely because of reload.
- For an imperial target with the existing conquest-infamy modifier, verify its surcharge still appears once and applies after the native calculation. Compare with a valid non-imperial target. Check that a claimed state follows the existing Return State path rather than receiving a new Conquer State discount twice.

## 3. Annex Country

- Use a valid non-imperial target in a controlled conflict. Inspect current country infamy and its constituent state-based calculation; the subject multipliers, if applicable, should still affect the result.
- Meet the goal's displayed territorial-control requirement, wait for enforcement and inspect annexation while the war continues. Preserve at least one eligible continuing opponent/ally for a useful liberation-mirror test; if annexation ends all fighting, record that mirror continuation branch as not exercised.
- Check the engine-selected liberation/retake goal, its holder/target and its lack of mirror infamy. An annexed subject whose overlord is still fighting may produce state-retake goals instead of the same liberation presentation as an independent country.
- Exercise the counter-goal where possible, then peace and save/reload. Inspect territorial ownership, any restored subject relationship, participants and fronts; these are engine behaviors to verify, not new subject scripts authored by this patch.
- An imperial native bond must still fail the existing direct-annexation guard. Do not weaken this guard to manufacture a test target.

## 4. Unification

An ordinary January 1776 game does not necessarily expose a valid unification play. Use a separate controlled save with legitimate formation-candidate prerequisites; forcing only a popup/goal with missing scopes does not prove normal eligibility.

- A valid state unification goal remains zero-infamy and uses its existing target, sole-candidate and conflict checks.
- Hold the objective through enforcement; confirm the state transfers before peace and a territorial retake mirror is generated when an eligible opponent continues fighting.
- Exercise reversal if possible, check the final peace result and save/reload.
- The existing imperial-bond restrictions in both availability and validity must remain. Never count a deliberately blocked imperial case as a failed generic unification test.

## 5. Complete the pending issue 28 checks in the same test pass

Follow [the #28 protocol](../V1_15_ISSUE28_WAR_SUPPORT_EVENTS_2026_11_08/RUNTIME_PROTOCOL.md): **Colère sur le front** and **Un pacifiste dénonce la guerre**. In particular, inspect support **change**, distinguish the random first revolutionary option from the guaranteed second effect, and test the strict electoral `< -5` threshold. A successful war-goal test does not validate those event branches.

Return passed / failed / not exercised for the three goals and the four #28 API sites. Include enforcement/retake/peace observations, infamy, parties/subjects/fronts where relevant, save/reload and fresh error excerpts. A generic launch-only success cannot close the unexercised cases. #32 and #28 remain open until the maintainer reports their actual engine results.
