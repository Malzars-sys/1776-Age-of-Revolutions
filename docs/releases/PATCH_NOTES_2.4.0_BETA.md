# Version 2.4.0 Beta

This is the mod's largest update so far. It rebuilds technological progress for a 1776 start, adds new production chains, gives land transport a historical path from roads and canals to railways, and revisits the world's starting economy. This is a beta: the final in-game effect of some starting-building changes still needs verification (see **Known beta issues**).

## Highlights

- A redesigned early technology tree covers the transition from eighteenth-century crafts and institutions to industrial production. Later technologies have been repositioned and reconnected to that earlier progression.
- Starting technologies have been reassessed across 471 country tags to reflect specific historical capabilities rather than a generic national tier. Three poorly documented tags retain their previous setup pending research.
- Sixteen new market goods and ten new building types add salt, spices, stone and cement, chemicals, petroleum refining, non-ferrous metals, phosphates, precision machinery, and pharmaceuticals.
- The former railway building now represents **Regional Infrastructure**: roads and canals can provide access before railway technology exists, while rail and passenger services arrive later.
- A worldwide 1776 starting-building target redistributes farms, workshops, mines, trade centers, administration, and infrastructure toward historically plausible regions. Starting populations were also adjusted conservatively in many states.
- Steel mills now represent coke-based industrial metallurgy. Earlier ironworking remains part of the broader mine, workshop, and manufacturing economy rather than appearing as premature steel mills.
- Company assets and selected AI technology checks have been updated for the new economy and technology tree.

## Technology overhaul

### Early technology tree

The Production, Military, and Society trees now give the 1776 start its own early progression. Naval technologies form a distinct historical line within the game's Military category. Technologies such as **Organized Workshops**, **Atmospheric Engine**, **Scientific Exchange**, **Regulated Small Arms**, and **Naval Architecture** represent particular capabilities, not interchangeable country-wide advancement tiers.

Prerequisites, eras, building unlocks, and production-method unlocks have been reviewed together. Technologies inherited from the later game have been kept where needed, but their place in the 1700–1836 sequence and their connections to post-1836 research have been reworked. Obsolete technology IDs needed for compatibility remain non-researchable rather than interrupting the normal tree.

### Production technologies

Early workshops, husbandry, forestry, mining, glassmaking, papermaking, food preparation, and land infrastructure now precede more specialized industrial methods. Later advances in coke smelting, chemical production, machine tools, textiles, cement, electrical production, and petroleum processing open the corresponding buildings or production methods. Construction sectors no longer depend on an obsolete hidden technology gate.

### Military and naval technologies

Weapons, artillery, formations, shipbuilding, navigation, and dockyard development have a more period-specific sequence. Selected unit and ship unlocks now follow the appropriate technology, including a chronological cavalry progression and later naval construction methods. This changes research and equipment availability; it does **not** claim a new starting army or fleet size.

### Society technologies

Education, medical practice, scientific exchange, commercial institutions, administration, and political ideas have more distinct prerequisites and unlocks. Related laws and institutional content have been aligned with the rebuilt tree. English and French technology descriptions were revised, and displayed technology names were shortened where necessary to fit the interface.

### Starting technologies and the later transition

Country starts now use historically reviewed technology lists. The final starting-technology audit covers 471 country tags and checks that granted technologies have their prerequisites. A small number of uncertain historical capabilities were deliberately not granted. The post-1836 eras and prerequisite links were also adjusted so the new early tree leads into later industrial and political developments without a disconnected jump.

## Economy and new goods

The following are new **market goods** in this update, not renamed vanilla goods. Early availability, later industrial use, and actual market prices depend on technologies, employment, and trade.

| Good | Production and main role |
| --- | --- |
| Salt | Early salt mines and salt pans supply food processing and later industry. |
| Spices | Early plantations supply luxury consumption and spiced food preparation. |
| Fine food | Food industries prepare a separate luxury food for population demand. |
| Limestone | Quarries provide raw material for cement and other industrial recipes. |
| Cement | Cement works supply construction and later infrastructure methods. |
| Industrial chemicals | Chemical-plant methods supply bleaching and other downstream industrial processes. |
| Refined fuels | Later oil refining supplies mechanized extraction and transport. |
| Lubricants | Oil refining supplies later machinery-intensive production. |
| Heavy petroleum products | Oil refining supplies later heavy-industry and transport methods. |
| Copper | Copper mines supply ship sheathing, metalworking, and electrical production. |
| Bauxite | Bauxite mines supply aluminium production. |
| Alloys | Non-ferrous metallurgy supplies advanced industrial and construction methods. |
| Aluminium | Later metallurgy supplies aircraft, electrical, and selected consumer or transport methods. |
| Phosphates | Phosphate mines supply improved fertilizer production. |
| Precision machinery | Specialized tooling methods supply advanced factories and public services. |
| Pharmaceuticals | Chemical-plant methods supply organized medical services. |

### New industries and production methods

The ten new building types are **salt mines, salt pans, spice plantations, limestone quarries, cement works, oil refineries, copper mines, bauxite mines, alloys plants, and phosphate mines**. Resource potential is distributed by state; the new mines and plantations do not imply that every country begins with an operating example.

Existing industries have also been reworked. The **chemical plant** now combines separate production-method choices for industrial chemicals, fertilizer, and pharmaceuticals rather than requiring a second chemical-works building. Precision machinery is produced through specialized tooling methods, not a separate factory. Food, textile, furniture, glass, paper, and tool production has more clearly differentiated traditional and industrial methods. Early recipes and later mechanized upgrades use different labor and inputs, with technology gates tied to the required equipment or process.

### Resources, steel, and metallurgy

New salt, limestone, copper, bauxite, and phosphate deposits support the new chains. Commercial logging and organized forestry are distinguished from more diffuse pre-industrial wood production. Iron, coal, sulfur, and other established resources have also been reconsidered in the starting economy.

Steel mills are reserved for industrial **coke smelting**. The historical starting target has a limited Yorkshire steel mill; earlier bloomery, forge, and charcoal activity is represented through other parts of the economy. Copper, alloys, and aluminium provide a separate non-ferrous path rather than being folded into steel.

## Regional infrastructure and trade

The old railway building has been broadened into **Regional Infrastructure**. One building carries independent road, canal, railway, and passenger-service method groups. Roads can provide early access; selected 1776 commercial waterways can operate before railways; actual rail networks and passenger trains require later research. The starting infrastructure plan assigns no active rail or passenger-train method in 1776.

Trade centers have been redistributed toward historical commercial hubs and entrepôts. This is intended to better support regional exchange and long-distance imports and exports, but trade throughput and world-market prices still depend on employment, access, and demand in a running campaign.

## The historical 1776 start

Starting buildings have been reviewed worldwide to reduce anachronistic factory concentration and better reflect regional agriculture, extraction, craft production, administration, and commerce. The static target records **2,584 positive building placements**, but the present beta cannot claim that all of them load correctly: duplicate state-history blocks remain in the shipped files. The protected Venice and Genoa setups and the previously calibrated military and naval building sizes were not intentionally redistributed.

Administration has been recalibrated for the 1776 population and revised starting economy. Forestry, trade, and road capacity received separate passes. A conservative state-by-state population pass changed many regions while leaving Venice, Genoa, and areas awaiting map work untouched; Qing China received a separate later population correction. Chartered companies, including the Dutch East India Company, British East India Company, and Hudson's Bay Company, have selected colonial assets assigned to them in the intended setup.

## AI, fixes, and compatibility

- Selected AI military and supply preferences now check technologies that exist in the new tree. Imported compatibility strategy files do not constitute a general AI overhaul.
- Technology and production-method gates have been corrected where old or hidden prerequisites could block construction or upgrades.
- The chemical plant, industrial chemicals, and pharmaceuticals received updated icons and production-method artwork. Some other new goods still use placeholder art.
- Technology names and descriptions received an English and French readability pass.

## Known beta issues

- **Starting buildings need a fresh-game validation.** The current HEAD contains multiple building-history blocks for 458 state IDs, despite an earlier consolidation report. The game may ignore or override some intended placements; the 2,584 figure above is a static target, not a verified in-game total.
- **Some starting buildings may be rejected or capped.** The last diagnostic game log before the final files recorded 87 rejected or reduced building cases caused by disagreement between placements and state resource definitions. A new log is needed to establish the remaining count. Separate arable-land overages are outside this beta pass.
- **Economic balance is provisional.** Administration, market access, hiring, trade-center capacity, and local/world prices need measurement after a new 1776 start. In particular, recent salt, fertilizer, chemical, and British-market supply changes have not been shown to meet every intended price target in a fresh campaign.
- **Some goods still use placeholder icons.** The three petroleum products and phosphates are among the affected definitions.

Please report bugs, economic imbalances, historical inconsistencies, and English or French localization problems with a new-game save and the relevant game log where possible.
