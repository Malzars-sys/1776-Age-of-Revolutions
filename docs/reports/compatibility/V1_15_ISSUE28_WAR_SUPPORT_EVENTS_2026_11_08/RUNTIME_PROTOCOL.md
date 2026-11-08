# Issue 28 — targeted engine acceptance

Status: **NOT RUN**. The two event files are installed in the regular local mod used with playset **hhhh**. Fully restart Victoria 3, start a new 1776 campaign and record the actual build/DLCs. Use separate controlled saves where an insurrection or an electoral campaign is required. Preserve the original saves; no permanent gameplay test controls are added to the mod.

## 1. Initialization and logs

Advance past the first simulated day. Check fresh/rotated logs against the #20 baseline for unknown `add_war_exhaustion`, unknown `has_war_exhaustion`, scope errors or new support-change errors. Successful startup is necessary but does not validate the event branches below.

## 2. Anger at the Front — `revolution_pulse1_events.2`

French title: **Colère sur le front**. The country must have an ongoing insurrection and participate in a war with its own support **below 55**. Preserve the existing insurrection/war setup; directly forcing a popup without valid war and civil-war scopes does not prove its natural trigger.

- Verify that a country with no qualifying war or no ongoing insurrection does not satisfy eligibility. Test a clearly lower level (for example 54) and level 55; exactly 55 must not qualify. The saved `anger_at_front_war` must satisfy the same `< 55` condition.
- From independent controlled cases, choose **Arrêtez les mécontents et continuez le combat.** (`.2.a`). The war effect is only one of three equal random branches. When that branch is selected, the event contribution to the root country's **support change** in the saved war decreases by **5**. Other branches retain their civil-war-progress or morale effect. If the war branch was not selected, record it as not exercised; do not infer success from a different random outcome.
- Choose **Nous ne pouvons pas nous permettre d’arrêter des soldats.** (`.2.b`). Its support-change contribution is **−5 regardless of the following random consequence**. Check the root country and the selected war, including the named event contribution in the war-support tooltip where available.
- Use **Nous devons arrêter et laisser les hommes se reposer.** (`.2.c`) as a control: it has no new support-change effect. Other pre-existing consequences still apply.

Observe the support-change calculation, not a supposed instant loss of five support-level points at the moment of clicking. Normal changes in the war can affect the total; compare paused before/after event contributions where possible. With multiple wars, confirm the effect stays on the selected qualifying war and affects the event country, not its opponent or another participant.

## 3. Pacifist Condemns the War — `election_contextual_events.3`

French title: **Un pacifiste dénonce la guerre**. Required existing setup: an active electoral campaign, no Single-Party State variant, no active electoral/mute cooldown, an opposition interest group with a party and a pacifist leader, at least one party-aligned governing group, and a war where the country is the **attacking war leader**.

- With support change clearly below **−5** (for example −5.1), the war condition should qualify. At exactly −5, at −4.9, zero and positive values it must not qualify. A low support **level** by itself is insufficient.
- Confirm the `pacifist_war` selected during initialization is also an attacking-war-leader war with support change `< -5`. With several wars, a defending war or a war with a weaker decline must not be selected instead.
- Exercise the existing event choices and check that the intended party momentum/character consequences still apply, without missing saved-scope errors. These consequences are preserved by the patch; the two migrated sites are the event trigger and its war selector.

Debug inspection or event tools may help establish controlled cases, but forcing an event bypasses eligibility and does not validate the threshold by itself. Record any fixture that could not be established as **not exercised**. This protocol does not claim that a specific ordinary 1776 country already has every electoral prerequisite.

## 4. Persistence and evidence

Save/reload before a qualifying event and, where supported, while its popup is open. Advance and complete the choice, checking that saved war/country scopes still resolve and the effect is not duplicated. Retain fresh logs and report any new scoped error.

Return passed/failed/not-exercised results for both revolution effect sites and both electoral condition sites. Useful evidence: build/DLCs, test country, save names, selected options/random branch, selected war, support level versus change, before/after event contribution, boundary cases, save/reload and relevant log excerpts. Engine and human acceptance remain pending until reported; no measurements or fixtures are inferred from a generic launch alone.
