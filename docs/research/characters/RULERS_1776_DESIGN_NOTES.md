# RULERS_1776_DESIGN_NOTES

## Purpose
This packet is the historical source of truth for the first major 1776 ruler reconstruction batch. Codex should **not perform web research** for these entries unless it detects a direct contradiction inside the supplied research packet.

## Implementation rules

1. **Reference date:** 1776-01-01.
2. **Historical Character Date Rule**
   - exact, well-sourced birth date -> use `birth_date` if compatible with the established project syntax;
   - uncertain exact date -> use a documented `age = X`;
   - never invent an exact day/month to make the engine happy.
3. **Nominal vs effective ruler**
   - A single Victoria 3 ruler slot should normally represent the person exercising the state's executive authority.
   - Exceptions must be documented, especially child rulers, co-regencies and composite monarchies.
4. **Do not infer game IDs from historical prose.**
   - Culture, religion, home state, ideology and portrait DNA must be mapped to IDs already available in the fork/vanilla.
5. **Do not use generated/random rulers** where this packet supplies a historically identified ruler.
6. **Do not silently convert titles.**
   - Louis XVI = king, not emperor.
   - Karim Khan = Vakil/regent, not formally shah.
   - William V = stadtholder, not king.
   - Tokugawa Ieharu = shōgun, not emperor.
7. **No mass military role assignment in this batch.**
   - If a ruler was also a commander, preserve/implement that only when already structurally necessary and historically well supported.
   - Global Commander Completeness remains a later military cleanup.

## Special cases requiring careful implementation

### Austria / Habsburg Monarchy
- Primary V3 ruler on 1776-01-01: **Maria Theresa**, age 58.
- **Joseph II**, age 34, was Holy Roman Emperor and co-regent from 1765.
- Maria Theresa nevertheless continued to rule the Habsburg Monarchy until 1780.
- Recommendation: one ruler = Maria Theresa; Joseph II as a secondary historical political character, **not a second simultaneous country ruler**.

### Maratha Confederacy
- Nominal Peshwa: **Madhavrao II**, born 1774-04-18, therefore age 1 on 1776-01-01.
- The Maharashtra Gazetteer describes the infant as formally installed Peshwa and identifies **Sakharam Bapu** as head of government, with **Nana Fadnavis** supporting him in the early regency.
- Recommendation: do not simply replace the infant Peshwa with Nana Fadnavis and call Nana "Peshwa".
- Codex must inspect whether the current government/character system can represent a regency cleanly. If not, stop on MARATH and request user choice instead of inventing a constitutional fiction.

### Mysore
- The Wodeyar monarch remained a dynastic figurehead.
- **Hyder Ali** exercised de facto power.
- For a one-ruler Victoria 3 abstraction, use Hyder Ali as ruler unless the fork already models a separate figurehead system.

### Naples and Sicily
- **Ferdinand** was simultaneously Ferdinand IV of Naples and Ferdinand III of Sicily.
- If the fork keeps Naples and Sicily as separate tags, the same real sovereign governs both.
- Codex must inspect whether one character can legally be shared across country scopes. If not, do not fabricate two unrelated Ferdinands without documenting the engine limitation.

### Dutch Republic
- **William V** was hereditary stadtholder, not monarch.
- Keep the republican/oligarchic structure in laws/government type; the ruler character is an abstraction of executive leadership.

### Joseon
- **Yeongjo** is still king on 1776-01-01.
- He dies later in 1776; Jeongjo does not belong at scenario start.

### Montenegro
- **Sava Petrović** is the first-pass recommendation, but this row is MEDIUM confidence for exact biographical dates.
- Implement identity only with approximate age unless a later dedicated research pass upgrades the evidence.

## First-batch acceptance rule
A country is PASS when:
- the correct 1776 person is the starting ruler;
- displayed age is historically coherent;
- no 1836/random ruler remains where this packet supplies an identity;
- title/government representation is not obviously anachronistic;
- no duplicate starting ruler is created;
- the change introduces no attributable parser/runtime errors.

## Out of scope
- Full ideology/trait balancing.
- Global generals/admirals.
- Army/navy size rebalance.
- Technology-tree overhaul.
- Map overhaul.
