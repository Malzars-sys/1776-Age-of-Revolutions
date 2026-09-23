# BUILD START 1776 — Historical criteria for future deincorporation review

Status: **diagnostic rule only — no gameplay write authorized**

The numerical runtime plan must not decide deincorporation solely from population, distance, low administrative output or optimization value. Every proposed state must pass a separate historical-integration review.

## Eligible historical profiles

A state may be considered only when at least one of the following is demonstrated for 1776:

1. **Recent conquest:** the territory was recently conquered and had not yet been fully incorporated into the conqueror's ordinary administrative system.
2. **Recognized high autonomy:** local institutions, estates, legal systems, taxation or representative bodies substantially limited direct central administration.
3. **Indirect or negotiated rule:** the central state governed through local rulers, tribute, special charters or a distinct constitutional settlement.
4. **Weak fiscal-administrative integration:** nominal sovereignty existed, but ordinary taxation and bureaucracy remained materially separate from the central core.

## Ineligible shortcuts

The following are not sufficient by themselves:

- low population;
- high population;
- distance from the capital;
- a negative bureaucracy balance;
- a desire to reach 100% tax capacity;
- a convenient numerical reduction in administrative demand.

## User-authoritative examples

- **Great Britain:** Scotland is a plausible candidate because its historically distinct settlement and institutions can represent weaker direct central integration. It must be reviewed as a deliberate constitutional/autonomy choice, not selected because it is numerically convenient.
- **China:** review recently conquered territories and selected southern territories with long-standing high autonomy. Do not compensate for Chinese overpopulation by adding dozens of administration levels, and do not automatically deincorporate the ordinary central core.

## Consequence for the existing diagnostic CSV

`BUILD_START_1776_ADMINISTRATION_DEINCORPORATION_RUNTIME_PLAN.csv` remains a numerical screening list only. Its current priority order is **not authoritative for state selection**. Before any future write, every row must be classified as:

- `HISTORICALLY_ELIGIBLE_RECENT_CONQUEST`;
- `HISTORICALLY_ELIGIBLE_HIGH_AUTONOMY`;
- `HISTORICALLY_ELIGIBLE_INDIRECT_RULE`;
- `REJECT_CORE_INTEGRATED_STATE`;
- `RESEARCH_REQUIRED`.

No state status, ownership, homeland, incorporation progress or building level was changed when recording this rule.

