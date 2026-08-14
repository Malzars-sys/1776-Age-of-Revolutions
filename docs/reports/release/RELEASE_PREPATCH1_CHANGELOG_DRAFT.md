# 2.3.0

## Compatibility

- Updated the mod's engine baseline for Victoria 3 1.13 while preserving the January 1, 1776 start date.
- Isolated the 1776 character and diplomatic setup so vanilla 1836 history no longer leaks into a new campaign.
- Reconciled military, naval, commander-rank, and sailor systems with the current 1.13 script model.

## Historical setup

- Rebuilt the starting rulers of major powers, European states, and non-European countries around the political situation of 1776.
- Added historically grounded regents, governors, mayors, company executives, and shared monarchs, with dedicated English and French titles.
- Corrected the starting leadership of the British East India Company, Dutch East India Company, Hudson's Bay Company, Tibet, Bukhara, Lucca, Ireland, and many other states.
- Kept uncertain identities procedural rather than presenting unsupported names as historical fact.

## Map and countries

- Improved country laws, governments, and historical setup without changing province or state-region geometry in this update.
- Restored Lucca's republican government and improved the representation of chartered companies, Habsburg dependencies, free cities, and regional governments.
- Documented remaining political and map abstractions for later work instead of forcing anachronistic rulers or borders.

## Military and navies

- Rebuilt the global 1776 starting order of battle: 214 land formations and 41 fleets with valid starting headquarters and infrastructure.
- Rebalanced the largest armies and navies to better represent their peacetime 1776 establishments.
- Added 79 historical starting generals and 26 fixed historical admirals, while retaining procedural commanders where evidence was insufficient.
- Corrected commander ranks, conscription capacity, recruitment regions, empty formations, and Spain's blocked militia reserve.
- Restored the Maratha Konkan Flotilla with Anandrao Dhulap, two frigates, a working Naval Administration, and full starting crew.

## Economy

- Reworked Merchant Banking around trade, credit, private investment, and ship construction while removing the old free-minting bonus.
- Expanded the starting trade and administration setup of Venice and Genoa.
- Added the Rialto Commercial Complex and Palazzo San Giorgio as unique commercial monuments with local trade effects and real employment.
- Adjusted Genoa's starting population and monument workforce after runtime testing.

## Fixes

- Fixed unsupported regency setup, duplicate or incorrect titles, chartered-company executive initialization, and several raw localization issues.
- Corrected fleet headquarters and recruitment-state problems that prevented formations from materializing correctly.
- Removed obsolete military define keys, a duplicate Spanish armada name, a dead Prussian fleet scope, and the legacy Centre of Commerce modifier.
- Improved English and French localization for rulers, governments, formations, commanders, and monuments.

## Documentation / internal research

- Added reproducible audit matrices and validation reports for rulers, formations, generals, admirals, and merchant-republic balance.
- Added preliminary technology and industrial research for a future Tech Tree overhaul. This research does not change the current release's gameplay.
