# CLEANUP-2D-1 — Military/Naval Constitutional and Organizational Notes

## Governing rule

Historical personnel totals are not V3 unit counts. Permanent establishments, effective field strength, garrisons, militia/levies, company forces, colonial forces and naval inventories are separate layers. CLEANUP-2D-2 must apply the engine constants (1,000 per land unit; 500 per frigate abstraction; 800 per ship-of-the-line abstraction) only after those layers are reconciled.

## Great Britain (GBR)

The British regular Army was a global crown establishment of almost 50,000 by 1775. The ~7,000 regulars in North America in 1775 are a deployment subset, not an additional national army. The 1776 New York concentration of ~30,000 reflects wartime reinforcement and auxiliaries. The Royal Navy had about 270 warships in 1776, but total hull inventory and ships actually at sea/in condition are different measures; Dull's 82 SOL at sea or in condition in June 1776 is the better readiness anchor.

## France (FRA)

France is in the middle of Saint-Germain's reform in 1776. SHD holds exact 1776 troop-location and composition tables, while accessible synthesis gives reform endpoints rather than a single January total. The naval baseline must be peace/rearmament, not the 1778–83 wartime peak: 23 SOL were in condition on 1 January 1776, rising to 37 one year later.

## Spain (SPA)

Spanish naval power was distributed among European and American stations. The 2D-0 duplicate Real Armada is not historically justified as two identical fleets, but multiple distinct Spanish squadrons **are** historically defensible. Near-date evidence distinguishes 17 SOL in full commission in March 1776 from 59 SOL in the February 1777 inventory and 28 then in armament.

## Russia (RUS)

Russia should not be modeled from a single postwar field-army figure. The 1768–74 war ended immediately before the scenario and the army was geographically dispersed. The navy was a major Baltic force with recent Mediterranean expeditionary experience; a ship-list reconstruction is still needed before numeric V3 conversion. The fork's zero naval-administration levels are a structural implementation bug, not historical evidence of no navy.

## Austria (AUS)

The Habsburg establishment is about 220,000 in the 1777 comparison table. HUN, BEO, GAL and TRS must not each receive independent full national establishments on top of Austria unless the mod deliberately splits the Habsburg military system and proportionally transfers forces.

## Prussia (PRU)

The near-date 1777 army strength is 158,000. No meaningful Prussian state battle fleet was established for 1776 in this pass. The empty `Kniglich_Preuische_Marine` should therefore not be populated merely to preserve a formation object; implementation should remove/disable it unless new evidence proves a combat flotilla worth representing.

## Ottoman Empire (TUR)

Central corps were only part of Ottoman military power. Provincial and semi-autonomous forces and warrior populations were essential to wartime mobilization. The 1768–74 war is too close to the start date to treat peak campaign totals as the permanent 1776 establishment. V3 should separate a smaller standing core from wider mobilization potential.

## Qing China (CHI)

The approximately 800,000 mid-eighteenth-century establishment consists of about 200,000 Bannermen and 600,000 Green Standard troops. The systems had different functions, and Green Standard forces were dispersed across provincial security and garrison duties. The figure is a paid administrative establishment, not 800,000 simultaneously deployable field soldiers.

## United States / Continental Congress (USA)

The 1776 Continental Army plan was about 20,372; effective field returns fluctuated. State militia, the Flying Camp and short-term enlistments are mobilization capacity and must not be frozen into a 164-unit permanent starting army. Naval power must distinguish the Continental Navy, state navies and privateers. The annual 1776 Continental Navy personnel total is 3,090; the 27-warship figure is a whole-year/"by 1776" scale and not a 1 January commissioned inventory.

## Maratha Confederacy (MARATH)

The Confederacy is not a unitary European-style standing establishment. Cavalry, infantry and artillery coexist with chief-controlled contingents and a very large support/bazaar/logistics footprint. Campaign headcounts cannot be converted directly to permanent V3 battalions. 2D-2 should model a confederal core plus mobilizable/subject capacity.

## East India Company (BIC)

The Presidency armies (Bengal, Madras and Bombay) must be reconstructed separately. Company Europeans, sepoys and Company artillery belong to BIC; British Crown regiments merely attached to Company campaigns belong to GBR and must not be double-counted. The accessible evidence brackets rather than pins 1776: a 1760s Coromandel return and a much larger 1778 India-wide return cannot be linearly interpolated without false precision.

## Dutch East India Company (DEI)

The VOC was simultaneously a commercial, governmental and military institution. A sizeable part of its workforce was military, but company soldiers, fortress garrisons, armed merchantmen and VOC shipping are not the same thing as a sovereign national army or battle fleet. Conversion must use a company-specific abstraction and must not copy the Netherlands' state navy.

## Hudson's Bay Company (HBC)

HBC forts, armed employees and supply vessels are corporate security/logistics. No evidence supports treating HBC as a sovereign blue-water naval power. Any represented force should be small, corporate and local unless a specific historical armed formation is documented.

## Denmark–Norway (DENNOR)

The Danish-Norwegian army combined enlisted and nationally conscripted soldiers. In 1776 about 70% of Danish foot troops were in the conscripted/national category, but these were real army units, not simply an emergency militia. A strict V3 standing-vs-conscription dichotomy therefore needs a hybrid interpretation.

## Sweden (SWE)

Sweden remained a meaningful regional Baltic power. The line fleet had 22 ships in service in 1772, six of them old/obsolete, and a major renewal plan was being developed at the end of 1776. Nominal hull count therefore overstates battle-ready quality.

## Netherlands (NET)

The Dutch Navy was no longer the seventeenth-century first-rank force. Typical peacetime activity after the War of the Spanish Succession required only a few thousand seamen annually, with Amsterdam responsible for most vessels. The Republic still requires a real navy in V3, but active 1776 force should not be derived from Golden Age reputation.

## Persia / Zand Iran (PER)

Karim Khan maintained the only standing Iranian army of the period, combining tribal cavalry, musketeers and limited artillery. Surviving ledger totals around the 1774 Basra mobilization materially overstate fit-for-service strength and must be reduced by at least half. This is a direct warning against treating the current 85 V3 units as a validated standing army.

## Korea (KOR)

Late Joseon defense combined five central camps and local forces. Later quantitative evidence identifies a relatively modest on-duty central component alongside much larger support/obligation registers. 2D-2 should not convert all registered military obligations into full-time battalions.

## Structural / colonial tags

A number of fork tags are not independent 1776 national military polities (colonial administrations, Habsburg subregions, anachronistic later states, or overlapping abstractions). These are explicitly marked `STRUCTURAL_DEFER` in both master CSVs. Their personnel must first be attributed to the historical sovereign/company/local structure before any V3 target is calculated.
