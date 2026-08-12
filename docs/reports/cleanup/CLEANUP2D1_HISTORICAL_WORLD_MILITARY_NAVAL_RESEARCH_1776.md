# CLEANUP-2D-1 — Historical World Military & Naval Research, 1776

## 1. Repository baseline

This research package inherits the CLEANUP-2D-0 audited repository baseline (`cleanup-post-release`, HEAD recorded there as `58edae83b1c329c957772b2b6fabfa5baa1a6d17`). This assistant-side research phase did not modify the user's repository, gameplay files, Git index or Victoria 3 installation.

## 2. Methodology

The target date is 1 January 1776. Evidence from 1775–1777 is preferred. Older/later evidence is admitted only when explicitly marked and never silently treated as exact. Standing/permanent personnel, paper establishment, effective strength, garrisons, militia/levies and mobilization are separate. Naval inventory, commissioned/readiness status, reserve/ordinary, construction and maritime labour pools are separate.

All 210 centralized tags from CLEANUP-2D-0 receive an explicit research status. Low-evidence cases are **not** assigned invented troop totals.

## 3. Source-quality policy

Priority: primary/near-contemporary records; national military/naval archives; peer-reviewed academic work; academic monographs; institutional historical references. Low-evidence polities use regional scholarship only for organization/qualitative scale.

## 4. Date policy

Primary: 1776. Preferred window: 1775–1777. Exact figures from 1764, 1772 or 1794 are retained only as labelled anchors and never converted automatically.

## 5. Coverage

- CENTRALIZED_COUNTRIES_RESEARCHED = 210
- LAND_HIGH_CONFIDENCE = 8
- LAND_MEDIUM_CONFIDENCE = 1
- LAND_LOW_CONFIDENCE = 4
- LAND_QUALITATIVE_ONLY = 163
- LAND_STRUCTURAL_DEFER = 34
- NAVAL_HIGH_CONFIDENCE = 4
- NAVAL_MEDIUM_CONFIDENCE = 2
- NAVAL_LOW_CONFIDENCE = 2
- NAVAL_QUALITATIVE_ONLY = 168
- NAVAL_STRUCTURAL_DEFER = 34
- COUNTRIES_WITH_EXPLICIT_QUANTITATIVE_STANDING_ARMY_ANCHOR = 13
- COUNTRIES_WITH_EXPLICIT_QUANTITATIVE_NAVAL_ANCHOR = 13
- COUNTRIES_WITH_MILITIA_OR_LEVY_SEPARATION_EXPLICIT = 153
- CURRENT_VS_HISTORY_GAP_ROWS = 210

The nine decentralized native-conscription exceptions from 2D-0 remain outside the 210-row masters: ABB, JBB, KBB, MBB, NBB, SD1, SKH, ULT, ZWY.

## 6. Great Britain

The British Army peacetime establishment had reached almost 50,000 by 1775. Roughly 7,000 regulars were in North America in 1775; that is a subset of the global establishment. British planning for the 1776 New York campaign envisaged an expedition of about 30,000 and must be treated as wartime concentration rather than a Jan-1776 global baseline.

Royal Navy scale is much larger: about 270 warships in 1776, while Dull records 82 ships of the line at sea or in condition in June 1776. Inventory and readiness are therefore deliberately separate in the naval master.

## 7. France

The SHD catalogue contains exact January–May 1776 troop-location material and 1776–78 composition material. Accessible synthesis demonstrates major Saint-Germain reform changes around the target date; consequently 150,000–180,000 is retained only as a cautious conversion range, not an invented exact January total.

At sea, 23 French ships of the line were in condition on 1 January 1776, rising to 37 one year later. France starts below Britain and below its own later American-war mobilized strength.

## 8. Spain

The Spanish Navy is the clearest structural result of 2D-1. Near-date evidence gives 17 ships of the line in full commission in March 1776. A February 1777 inventory lists 59 SOL, 28 in armament, geographically divided between Europe and American stations.

**SPA_REAL_ARMADA_DUPLICATE_HISTORICAL_VERDICT = TWO_IDENTICAL_REAL_ARMADAS_UNJUSTIFIED; MULTIPLE_DISTINCT_SPANISH_SQUADRONS_HISTORICALLY_JUSTIFIED.**

The current duplicate must therefore be removed in implementation, but Spain may still receive multiple differently named/composed fleets in 2D-2/3.

## 9. Russia

A 1764 scholarly anchor gives approximately 350,000 army personnel; because the Russo-Ottoman War ended only in 1774, the Jan-1776 effective/establishment relationship is uncertain. A 300,000–350,000 establishment-scale working range is LOW confidence.

Russia remains a significant Baltic naval power, but a trustworthy Jan-1776 ship total was not extracted. The current 76 V3 naval units are therefore unvalidated, and the zero naval-administration infrastructure remains a separate P0 implementation problem.

## 10. Austria

Near-date 1777 strength: 220,000. Habsburg component tags (Hungary, Austrian Netherlands, Galicia-Lodomeria, Transylvania) cannot each receive independent full military establishments without double-counting.

## 11. Prussia

Near-date 1777 army strength: 158,000. No meaningful Prussian state battle fleet was established for 1776 in this pass.

**PRU_EMPTY_FLEET_HISTORICAL_VERDICT = DO_NOT_POPULATE_BY_DEFAULT; REMOVE/DISABLE EMPTY FLEET UNLESS NEW EVIDENCE APPEARS.**

## 12. Ottoman Empire

No single standing total is accepted. Central corps coexisted with semi-autonomous provincial forces and wider warrior mobilization. The immediate post-1768–74 context makes wartime campaign totals especially unsafe as permanent starting strength.

## 13. Qing China

Mid-18th-century paid establishment scale is about 800,000: roughly 200,000 Bannermen and 600,000 Green Standard. The systems had different roles and much of the Green Standard was dispersed in provincial security/garrison duty. This is not an 800-unit V3 target.

## 14. United States

The 1776 Continental Army plan was 20,372; a March return gives 18,410 officers and men. Militia and short-term service must be modeled as mobilization rather than as a 164,000-man standing army.

NHHC gives 3,090 Continental Navy personnel for 1776 and about 27 colonial warships by 1776, while thirteen frigates had only been authorized in December 1775. No Continental ship of the line belongs at the January start; the first 74 was authorized only in November 1776.

## 15. Major Indian powers

BIC has direct quantitative brackets but no safe all-Presidency Jan-1776 total: a 1760s Coromandel return and a much larger 1778 India-wide return use different scopes. MARATH is confederal and cavalry/logistics heavy; MYS under Haidar Ali is centralizing and proto-modernizing. HYD, AWA, GWA, NAG and other states remain qualitative unless near-date national returns can be sourced.

## 16. Remaining European powers

The Hewitson table anchors Saxony (21,840), Hanover (21,000) and Bavaria (8,000) in 1777. Denmark-Norway has a well-documented hybrid recruitment structure; the Netherlands a reduced peacetime navy; Sweden a 22-SOL nominal line fleet in 1772 with six obsolete and a renewal program emerging in 1776. Smaller states remain qualitative rather than assigned invented exact totals.

## 17. Middle East and Central Asia

Zand Iran has unusually useful qualitative/quantitative evidence: paper strength around the 1774 Basra mobilization must be reduced by at least half; Shiraz garrison evidence and the 1,400-man guard show the difference between paper and effective strength. Durrani, Central Asian khanates and Caucasian polities remain confederal/tribal or low-evidence and are not forced into a European establishment model.

## 18. East / Southeast Asia

Joseon combined five central military camps with local forces. Southeast Asian states used polity-specific combinations of court troops, manpower levies, mercenaries, firearms, riverine and maritime warfare. DAI remains structurally deferred because the 1776 Vietnamese political order is not a single unitary Dai Nam state.

## 19. Africa

Oyo is a major cavalry power near its eighteenth-century peak; Ashanti is a powerful expanding centralized empire under Osei Kwadwo; Dahomey is an established military kingdom. Accessible scholarship does not provide trustworthy Jan-1776 national headcounts for most African tags, so the master deliberately records qualitative structure rather than fictional numbers.

## 20. Americas

USA is separated from militia/state navies/privateers. Spanish, Portuguese, French and British colonial tags are marked structural where their forces are imperial rather than independent. Haiti, New Brunswick, Ontario and several Boer/later-colonial tags are structurally invalid as independent 1776 national military establishments.

## 21. Chartered/company militaries

BIC, DEI and HBC are not sovereign national-force copies of their owners. BIC Presidency armies require Company-vs-Crown separation. VOC combined commercial, governmental and military functions and a large military workforce, but armed shipping is not automatically V3 line-of-battle capacity. HBC corporate security should remain local/small absent specific contrary evidence.

## 22. Naval hierarchy

Research-supported qualitative hierarchy for the start:
1. GBR — unique global first rank.
2. FRA / SPA — first-rank challengers but at lower 1776 readiness than later wartime peaks.
3. RUS — significant regional Baltic great-power navy.
4. NET / SWE / DENNOR / POR — meaningful but second-tier/regional naval powers, each with distinct readiness constraints.
5. OMA and other regional maritime powers — important locally, not comparable hull-for-hull with Atlantic line fleets.

This is a sanity hierarchy, not a V3 target table.

## 23. Land-power hierarchy

European establishment anchors confirm very large Habsburg, Russian, French and Prussian military systems, but their organization differs. Qing's administrative establishment is larger still but is not directly comparable with a European field army. Britain's peacetime regular Army is much smaller relative to its naval power. USA is a mobilization-heavy revolutionary case, not a 164,000-man standing force.

## 24. Spain / Real Armada historical verdict

**COMPLETE = YES.** The duplicate is a script bug. Multiple distinct squadrons may be reconstructed historically.

## 25. Prussian empty-fleet historical verdict

**COMPLETE = YES at current evidence standard.** No meaningful 1776 blue-water state battle fleet was established; the empty formation should not be filled merely to avoid emptiness.

## 26. Major current-vs-history discrepancies

- USA standing land force: current 164,000 V3 equivalent vs ~18–21k Continental standing/effective scale → strongly inflated if militia is meant to be separate.
- RUS land: current 176,000 vs ~300–350k establishment-scale anchor → likely underrepresented in raw personnel, subject to dispersion/garrison adjustment.
- PRU: current 122,000 vs 158,000 near-date establishment → moderately low.
- AUS: current 152,000 vs 220,000 near-date establishment → low.
- SPA navy: exact duplicate inflates active fleet regardless of final conversion.
- CHI: current 485,000 vs ~800,000 administrative establishment is **not directly comparable** due to role dispersion.
- BIC/PER/MARATH/TUR: current raw headcounts cannot be approved or rejected without structural separation.

## 27. Uncertainty register

1. Many small polities lack accessible Jan-1776 quantitative returns.
2. Campaign army strengths are often far above permanent paid establishments.
3. Naval registered hulls overstate commissioned readiness.
4. Colonial/company forces can be double-counted with metropolitan armies/navies.
5. Habsburg and Spanish-imperial fork sub-tags require attribution rules.
6. Qing, Ottoman, Maratha and other non-European systems require role-aware conversion rather than one universal soldier multiplier.
7. Russia's exact Jan-1776 fleet still needs ship-list reconstruction if 2D-2 cannot balance it from broader evidence.
8. French exact Jan troop total would benefit from direct archival transcription, but the conversion range is sufficient to avoid false precision.

## 28. Low-evidence countries

Every low-evidence country is explicitly `QUALITATIVE_ONLY` or `STRUCTURAL_DEFER`; no blank research status remains. This is intentional. The conversion phase may use relative regional tiers and current infrastructure/population constraints, but must preserve the uncertainty flag and avoid fake exactness.

## 29. Bibliography summary

See `CLEANUP2D1_MILITARY_NAVAL_1776_SOURCES.md`. Major claims rely on SHD, NHHC, U.S. Army/CMH, Cambridge University Press journals/books, War in History, Encyclopaedia Iranica, Portuguese Naval Archives and Swedish archival/institutional evidence.

## 30. Readiness for CLEANUP-2D-2

**CLEANUP2D1_RESEARCH = COMPLETE_FOR_CONVERSION_MODEL_WITH_EXPLICIT_UNCERTAINTY**

Mandatory closure:
- CENTRALIZED_COUNTRIES_RESEARCHED = 210
- FIRST_RANK_NAVIES_RESEARCH_COMPLETE = YES
- REAL_ARMADA_HISTORICAL_VERDICT_COMPLETE = YES
- PRU_EMPTY_FLEET_HISTORICAL_VERDICT_COMPLETE = YES
- CURRENT_VS_HISTORY_GAP_ROWS = 210
- GAMEPLAY_FILES_CHANGED_BY_RESEARCH = 0
- VICTORIA3_LAUNCHED_BY_RESEARCH = NO
- GIT_MUTATION_BY_RESEARCH = NO

Next phase: **CLEANUP-2D-2 — V3 Historical Conversion & Global Military/Naval Balance Model**. It must assign proposed V3 target values, but still avoid gameplay edits until the conversion table is reviewed.
