# 1776 Project Invariants

These rules are durable design constraints for future work on the 1776 project. They do not authorize unrelated changes in a narrowly scoped phase.

## Commander Completeness Rule

Every initial military formation created or maintained by the mod must have at least one commander.

- Army -> at least one general is required.
- Fleet -> at least one admiral is required.
- Historical commanders are preferred when they can be identified reliably.
- If no reliable historical commander is available, a plausible generic commander may be used, but all documentation must clearly identify that character as generic rather than historical.
- Formation size is never an exemption. A formation containing only one unit still requires a commander.

This rule applies immediately to newly created or deliberately reviewed formations. Existing formations will be brought into compliance during the future global army, fleet, and commander audit; this document does not silently expand the scope of the current phase.

## Naval Progression Access Rule

Countries with historically demonstrated naval capability must have a plausible technological path for maintaining and expanding that capability.

The future technology overhaul must avoid a binary model in which a state must possess a high-level European naval institution such as `admiralty` before it can perform any naval expansion. Naval access should support progressive levels of capability, including:

- maintenance of an existing navy;
- recruitment of sailors;
- limited expansion of coastal or regional naval infrastructure;
- construction and development of forces appropriate to local technology and institutions.

Countries such as MARATH must eventually be able to develop limited coastal or regional naval infrastructure and forces without being placed at the same technological level as Britain, France, Spain, or the Netherlands.

Exact technologies, tiers, production methods, and unlocks are not decided here. This rule is a binding design requirement for the future technology overhaul. MARATH's current inherited naval administration without `admiralty` is an acceptable temporary state until that overhaul.

## Historical Character Date Rule

No historical character should knowingly start with:

- a negative age;
- a birth after the scenario start;
- a death before the scenario start;
- a clearly anachronistic office.

Unknown dates must not be silently invented as exact historical facts. If the engine requires an age or date that reliable sources do not preserve, use the least misleading supported approximation permitted by the engine and document both the uncertainty and the technical choice.
