# Recherche technologique — Asie du Sud et sous-continent indien — 1er janvier 1776

> **Objet : recherche historique uniquement.** Aucun fichier de gameplay n’est modifié et aucun code Victoria 3 n’est produit. La date de coupure est strictement le **1er janvier 1776**.

## 1. Périmètre

**59 TAG étudiés.** Le périmètre prend tous les TAG classés `North India` et `South India` dans le CSV, ainsi que les États himalayens explicitement rattachés au sous-continent (Bhoutan, Népal, Sikkim, Cachemire, Ladakh). `TIB` (Tibet) est signalé dans le CSV sous `Himalayas` mais exclu ici : son centre politique appartient au plateau tibétain et il doit éviter le doublon avec une recherche est/centre-asiatique.

- **North India (43)** : `ALW` Alwar, `ASM` Assam, `AWA` Awadh, `BAG` Rewah, `BAS` Bastar, `BER` Baroda, `BHO` Bhopal, `BHV` Bhavnagar, `BHW` Bahawalpur, `BIC` East India, `BIK` Bikaner, `BUN` Orchha, `COO` Cooch Behar, `DHA` Dharampur, `GAR` Garhwal, `GWA` Gwalior, `IDA` Idar, `IND` Indore, `JAI` Dhundhar, `JAS` Jaisalmer, `JEY` Jeypore, `JHN` Jhansi, `JOD` Marwar, `JUN` Junagadh, `KKI` Kuki, `KOT` Kotah, `KUT` Kutch, `MEW` Mewar, `MGH` Khasi, `MNP` Manipur, `MUG` Hindustan, `MYB` Mayurbhanj, `NAG` Nagpur, `NAR` Narsinghpur, `NAW` Nawanagar, `NGA` Naga, `PAN` Punjab, `PLP` Palanpur, `PTA` Patiala, `PTN` Patna, `SIN` Sindh, `SUR` Surguja, `TIP` Tipperah.
- **South India (11)** : `BCE` Ceylon, `COC` Cochin, `HYD` Hyderabad, `KHP` Kolhapur, `KNO` Kurnool, `MARATH` Maratha Confederacy, `MLD` Maldives, `MYS` Mysore, `PUD` Pudukottai, `SAT` Satara, `TRA` Travancore.
- **Himalayas (5)** : `BHU` Bhutan, `KAS` Kashmir, `LAD` Ladakh, `NEP` Nepal, `SIK` Sikkim.

**Bengale :** aucun TAG `Bengal` distinct n’apparaît dans ce périmètre du CSV. La réalité bengalie de 1776 est donc surtout pertinente pour `BIC — East India` (diwani et domination territoriale depuis 1765), sans propager automatiquement ces capacités aux autres États.

## 2. Méthode et sources

La matrice part de **toutes les technologies effectivement distribuées** aux 59 TAG dans le CSV pays/technologies. Chaque relation actuelle reçoit KEEP, REMOVE ou REVIEW; les ADD/REVIEW absents sont réservés aux capacités régionales réellement pertinentes. Les noms des nœuds ne sont jamais pris au pied de la lettre : le contenu gameplay du CSV sert d’interprétation. Les prérequis manquants ne sont jamais réparés automatiquement.

Principales familles de sources : Cambridge University Press (économie, textiles, États successeurs, Awadh, Hyderabad, Sikhs, Népal), articles académiques sur Mysore/Marathes, British Library (Rennell), Royal Museums Greenwich (Bombay Dockyard), UNESCO (Galle), sources gouvernementales indiennes sur charbon/papier, et études archéométallurgiques sur Zawar/wootz. Les URL complètes figurent dans la matrice CSV.

## 3. Diagnostic régional

L’Asie du Sud de 1776 est **fortement asymétrique**. Les grands pôles cotonniers, soyeux, lainiers et châles ont des chaînes artisanales/proto-industrielles puissantes; cela justifie largement `organized_textile_production`, mais **pas** `mechanized_spinning` ou `mechanized_weaving`. La mécanisation textile britannique ne doit pas être rétro-projetée sur une industrie indienne pourtant très productive.

La métallurgie impose la même distinction : le **wootz** du sud et le zinc/plomb-argent de **Zawar** témoignent de capacités techniques sophistiquées, mais ne sont pas du `coke_smelting`. Le nœud coke est donc refusé comme simple synonyme d’« acier avancé ». Les mines ne sont conservées que lorsque l’échelle et l’organisation correspondent raisonnablement au très large `shaft_mining`; ailleurs elles sont retirées ou laissées en REVIEW.

Militairement, quelques foyers se détachent : la Compagnie des Indes orientales dispose de sepoys drillés et d’artillerie structurée; Awadh a, avant la mort de Shuja-ud-Daula en 1775, renforcé infanterie disciplinée et artillerie; Mysore bénéficie déjà d’ingénieurs/experts européens sous Hyder Ali. En revanche, l’existence d’armes à feu ou de canons chez un petit État ne suffit pas à justifier les nœuds `regulated_small_arms`, `light_infantry_tactics` et surtout `standardized_field_artillery`.

Navalement, les capacités sont très localisées : **Vijaydurg** justifie le `state_dockyard_systems` marathe; **Bombay Dockyard** justifie des ajouts locaux à `BIC`; les infrastructures VOC de Ceylan sont sectorielles. Le chantier de Cochin démontre un savoir-faire local, mais son institution était VOC : il ne doit donc pas être copié automatiquement dans l’État natif `COC`.

Administration et finance doivent également être dissociées des formes européennes : les systèmes de recettes moghols et successeurs peuvent représenter `systematic_administrative_statistics` comme **ABSTRACT**, alors que hundi, banquiers marchands et crédit commercial ne suffisent pas à établir `institutionalized_public_credit`, `stock_exchange` ou `commercial_insurance_markets`. Enfin, une presse d’imprimerie n’est pas un réseau périodique : Ceylan imprime dès 1737, mais `periodical_print_networks` est retiré; le premier journal de Calcutta arrive en 1780, après la coupure.

## 4. Analyse pays par pays

### ALW — Alwar

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### ASM — Assam

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`, `shaft_mining`, `mechanized_spinning`
- **Technologies frontière/sectorielles:** `regulated_small_arms`, `shaft_mining`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Strong hand/proto-industrial textile production does not demonstrate machine spinning by 1 January 1776; this row exists to prevent conflating textile sophistication with mechanization.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/silk-in-northeastern-and-eastern-india-the-indigenous-tradition/8DB15E866AB2C38486C0F68388A3855A
- **Confiance générale:** MEDIUM

### AWA — Awadh

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `traditional_food_processing`
- **Technologies à REMOVE:** `shaft_mining`
- **Technologies à REVIEW:** `mechanized_spinning`
- **Technologies frontière/sectorielles:** `light_infantry_tactics`, `standardized_field_artillery`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. The parent scientific_fortification_siegecraft is absent in the tier and is assessed separately; do not add it mechanically.
- **Justification historique:** Shuja-ud-Daula had transformed Awadh’s army by his death in 1775, with disciplined infantry and field artillery supported by expanded fiscal capacity. Awadh’s dense agrarian and urban economy supports organized traditional processing. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/journals/modern-asian-studies/article/it-all-comes-from-me-bahu-begam-and-the-making-of-the-awadh-nawabi-circa-17651815/D7AEE97EA7821335A01B32B82AAB3FB0; https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5
- **Confiance générale:** MEDIUM

### BAG — Rewah

- **Current tier:** `tier_5`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `shaft_mining`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions.
- **Justification historique:** Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node. Court, revenue, legal and artisanal knowledge systems justify the abstract node without implying the European print/scientific institutions used as its game-tree parents. Established agrarian systems make the broad husbandry node plausible; this is not a claim of European agricultural-revolution techniques.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### BAS — Bastar

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`
- **Technologies à REVIEW:** `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **Technologies frontière/sectorielles:** `shaft_mining`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### BCE — Ceylon

- **Current tier:** `tier_2`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `distillation`, `enclosed_dock_systems`, `improved_husbandry`, `international_relations`, `organized_forestry`, `organized_textile_production`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `traditional_food_processing`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `atmospheric_engine`, `coke_smelting`, `commercial_insurance_markets`, `institutionalized_public_credit`, `periodical_print_networks`, `precision_boring`, `shaft_mining`, `stock_exchange`
- **Technologies à REVIEW:** `institutionalized_scientific_exchange`, `traditional_papermaking`
- **Technologies frontière/sectorielles:** `enclosed_dock_systems`, `institutionalized_scientific_exchange`, `organized_forestry`, `organized_textile_production`, `state_dockyard_systems`, `traditional_papermaking`
- **Prérequis problématiques:** organized_forestry is currently present; the uncertainty is local paper manufacture, not the prerequisite.
- **Justification historique:** No locally deployed Newcomen-type mine-pumping engine is evidenced in Dutch Ceylon by 1776. No evidence supports coke-based iron smelting in Ceylon by 1776; maritime/fortification sophistication is not evidence for this process. Printing existed, but the node is a periodical press network; South Asian newspaper publication begins after the reference date.
- **Sources:** https://whc.unesco.org/en/list/451; https://pure.knaw.nl/portal/en/publications/the-company-fortress-military-engineering-and-the-dutch-east-indi/; https://www.christies.com/lot/lot-dutch-east-india-company-singaleesch-4747745/?from=siteindex&intobjectid=4747745&lid=1; https://indianexpress.com/article/explained/explained-history/world-press-freedom-day-india-first-newspaper-9306034/
- **Confiance générale:** MEDIUM

### BER — Baroda

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `regulated_small_arms`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### BHO — Bhopal

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `regulated_small_arms`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### BHU — Bhutan

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`, `urbanization`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/journals/itinerario/article/friendship-and-international-relations-in-the-himalayas-bhutan-britain-and-the-1910-treaty-of-punakha/84B58A6909F14A5B6D609B825777A0D1; https://www.cambridge.org/core/books/narratives-of-the-mission-of-george-bogle-to-tibet/8997BDBC1D0B36920B3D5F86FE0597A5
- **Confiance générale:** MEDIUM

### BHV — Bhavnagar

- **Current tier:** `tier_4;tier_5`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### BHW — Bahawalpur

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `regulated_small_arms`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### BIC — East India

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `colonization`, `distillation`, `improved_husbandry`, `institutionalized_scientific_exchange`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `state_dockyard_systems`, `enclosed_dock_systems`, `military_topographic_surveying`, `traditional_food_processing`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `systematic_cadastral_surveying`, `mechanized_spinning`, `coke_smelting`, `atmospheric_engine`, `precision_boring`
- **Technologies frontière/sectorielles:** `institutionalized_scientific_exchange`, `light_infantry_tactics`, `military_topographic_surveying`, `shaft_mining`, `standardized_field_artillery`, `systematic_cadastral_surveying`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. The parent scientific_fortification_siegecraft is absent in the tier and is assessed separately; do not add it mechanically.
- **Justification historique:** Company armies in Bengal and the presidencies combined European-style fortification, artillery and trained sepoy establishments before 1776. Bombay Dockyard is documented well before 1776 and was a local Company naval-production institution. Bombay’s established dockyard/harbour infrastructure supports the port-enabling dock node locally.
- **Sources:** https://www.cambridge.org/core/books/abs/ideology-and-empire-in-eighteenthcentury-india/colonial-encounters-and-the-crisis-in-bengal-17651772/7E01A04973FE339B0AB74603A58A1C39; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://journals.sagepub.com/doi/10.1177/096834450000700102; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** HIGH

### BIK — Bikaner

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### BUN — Orchha

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### COC — Cochin

- **Current tier:** `tier_5`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** `traditional_food_processing`
- **Technologies à REMOVE:** `shaft_mining`
- **Technologies à REVIEW:** `systematic_administrative_statistics`, `state_dockyard_systems`
- **Technologies frontière/sectorielles:** `state_dockyard_systems`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions.
- **Justification historique:** Malabar’s commercial agrarian economy and spice-processing trades support this traditional node. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node. Cochin hosted an important VOC shipyard relying on local labour and timber, but the institution belonged to the Dutch Company rather than automatically to the native Cochin state.
- **Sources:** https://www.tandfonline.com/doi/abs/10.1080/00856401.2025.2487347; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5
- **Confiance générale:** MEDIUM

### COO — Cooch Behar

- **Current tier:** `tier_5`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `shaft_mining`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions.
- **Justification historique:** Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node. Some court/revenue administration existed, but evidence is insufficient to equate it confidently with the durable tax-record bureaucracy represented by this gameplay node. Court, revenue, legal and artisanal knowledge systems justify the abstract node without implying the European print/scientific institutions used as its game-tree parents.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### DHA — Dharampur

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### GAR — Garhwal

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`, `urbanization`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### GWA — Gwalior

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `regulated_small_arms`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### HYD — Hyderabad

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `regulated_small_arms`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `traditional_papermaking`, `traditional_food_processing`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`, `mechanized_spinning`
- **Technologies frontière/sectorielles:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. The parent scientific_fortification_siegecraft is absent and is assessed separately.
- **Justification historique:** The Nizam’s state had fortifications, artillery and long exposure to French military contingents; the capability is established though uneven. The Mughal-Deccan paper industry around Aurangabad/Kaghazipura remained relevant to Hyderabad’s administrative sphere. Hyderabad’s agrarian and urban craft economy supports the traditional-processing node.
- **Sources:** https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/at-empires-end-the-nizam-hyderabad-and-eighteenthcentury-india/A19C9D4C7DD0313FCDAA25F27E745585; https://www.iranicaonline.org/articles/hyderabad/
- **Confiance générale:** MEDIUM

### IDA — Idar

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### IND — Indore

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `regulated_small_arms`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### JAI — Dhundhar

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `traditional_papermaking`
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** Sanganer/Jaipur paper manufacture is associated with the Kachhwaha court and predates the reference date. The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D; https://handmadeinrajasthan.rajasthan.gov.in/content/industries/handmadeinrajasthandepartment/artandcraft/papercraft0/handmadepaperprocess.html
- **Confiance générale:** MEDIUM

### JAS — Jaisalmer

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### JEY — Jeypore

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### JHN — Jhansi

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### JOD — Marwar

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### JUN — Junagadh

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### KAS — Kashmir

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `traditional_papermaking`
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`, `shaft_mining`, `mechanized_spinning`
- **Technologies frontière/sectorielles:** `regulated_small_arms`, `shaft_mining`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** Kashmir had a paper-manufacturing tradition dating back centuries; the node is strongly justified. The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node.
- **Sources:** https://www.cambridge.org/core/books/abs/kashmir/producing-paradise-kashmirs-shawl-economy-the-quest-for-authenticity-and-the-politics-of-representation-in-europe-c-17701870/8BABCECA4EAFA3E3D2A8C98B82D85783; https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.nature.com/articles/s40494-024-01360-9; https://cppri.res.in/en/paper-museum-kagaj-sangralya/historical-perspective
- **Confiance générale:** MEDIUM

### KHP — Kolhapur

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `regulated_small_arms`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### KKI — Kuki

- **Current tier:** `tier_6`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `improved_husbandry`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `urbanization`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Aucun cas majeur au-delà des abstractions générales de l’arbre.
- **Justification historique:** The generic tier overstates the settlement/administrative infrastructure implied by the game node for this decentralized upland society in 1776. Established agrarian systems make the broad husbandry node plausible; this is not a claim of European agricultural-revolution techniques.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5
- **Confiance générale:** HIGH

### KNO — Kurnool

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### KOT — Kotah

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### KUT — Kutch

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`
- **Technologies à REVIEW:** `shaft_mining`
- **Technologies frontière/sectorielles:** `shaft_mining`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### LAD — Ladakh

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`
- **Technologies à REVIEW:** `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `shaft_mining`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### MARATH — Maratha Confederacy

- **Current tier:** `tier_5`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `state_dockyard_systems`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `traditional_papermaking`, `traditional_food_processing`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `shaft_mining`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `institutionalized_public_credit`, `mechanized_spinning`, `coke_smelting`, `atmospheric_engine`, `precision_boring`
- **Technologies frontière/sectorielles:** `institutionalized_public_credit`, `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete.
- **Justification historique:** The Confederacy inherited a mature fortified-war tradition and maintained major fortified/naval bases; this low military parent is more plausible than forcing later European-style doctrine. Paper manufacture and expanding Peshwa bureaucratic demand are documented in the late Mughal/Maratha Deccan. The Confederacy’s large agrarian and urban economies support organized traditional food-processing capacity.
- **Sources:** https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/slow-conquest-administrative-integration-of-malwa-into-the-maratha-empire-17201760/3203253507F66BB5E5A1E4AA75BDF915; https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/books/naval-resistance-to-britains-growing-power-in-india-16601800/vijaydurg-the-strongest-place-in-all-india/535FB47298F24987A39228B5DA9466F2
- **Confiance générale:** MEDIUM

### MEW — Mewar

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `regulated_small_arms`, `shaft_mining`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Firearms were used, but evidence for the regulated production/standardization implied by the arms-industry unlock is insufficient for a confident KEEP.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D; https://www.tandfonline.com/doi/abs/10.1080/00438243.1983.9979899
- **Confiance générale:** MEDIUM

### MGH — Khasi

- **Current tier:** `tier_6`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `improved_husbandry`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `urbanization`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Aucun cas majeur au-delà des abstractions générales de l’arbre.
- **Justification historique:** The generic tier overstates the settlement/administrative infrastructure implied by the game node for this decentralized upland society in 1776. Established agrarian systems make the broad husbandry node plausible; this is not a claim of European agricultural-revolution techniques.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5
- **Confiance générale:** HIGH

### MLD — Maldives

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`, `urbanization`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### MNP — Manipur

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `regulated_small_arms`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/silk-in-northeastern-and-eastern-india-the-indigenous-tradition/8DB15E866AB2C38486C0F68388A3855A
- **Confiance générale:** MEDIUM

### MUG — Hindustan

- **Current tier:** `tier_5`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `international_relations`, `traditional_papermaking`, `traditional_food_processing`
- **Technologies à REMOVE:** `shaft_mining`
- **Technologies à REVIEW:** `institutionalized_public_credit`, `mechanized_spinning`, `industrial_canals`
- **Technologies frontière/sectorielles:** `institutionalized_public_credit`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions.
- **Justification historique:** Even in political decline, the Mughal court remained embedded in interstate diplomacy and successor-state relations. Established Mughal paper-manufacturing centres such as Kaghazipura support local production, not merely paper consumption. The large urban/agrarian economy sustained extensive organized food-processing crafts.
- **Sources:** https://www.cambridge.org/core/journals/journal-of-the-royal-asiatic-society/article/development-of-the-landrevenue-system-of-the-mogul-empire/46A2A48B81790FCFD2950F8CF0123A63; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### MYB — Mayurbhanj

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### MYS — Mysore

- **Current tier:** `tier_5`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `international_relations`, `scientific_fortification_siegecraft`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `traditional_food_processing`, `distillation`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `shaft_mining`, `state_dockyard_systems`, `scientific_naval_architecture`, `institutionalized_scientific_exchange`, `mysorean_iron_cased_rocketry`, `mechanized_spinning`, `coke_smelting`, `atmospheric_engine`, `precision_boring`
- **Technologies frontière/sectorielles:** `institutionalized_scientific_exchange`, `light_infantry_tactics`, `mysorean_iron_cased_rocketry`, `regulated_small_arms`, `scientific_naval_architecture`, `shaft_mining`, `standardized_field_artillery`, `state_dockyard_systems`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. scientific_fortification_siegecraft is independently justified and recommended ADD. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete.
- **Justification historique:** Hyder Ali maintained active diplomacy and military relations with the French, Dutch, Marathas and Company powers before 1776. French engineers and imported European military expertise were already present under Hyder Ali before 1776. Hyder’s European-assisted army and arms production justify an organized arms capability, though standardization was uneven.
- **Sources:** https://www.cambridge.org/core/books/monopolizing-knowledge/roots-of-company-science-in-asia/D5E74759162645817343BE03CCDDD25F; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/mrs-online-proceedings-library-archive/article/abs/crucible-steel-in-south-indiapreliminary-investigations-on-crucibles-from-some-newly-identified-sites/0C7F9DB996F0DD5758502D8F62201947; https://www.persee.fr/doc/rharm_0035-3299_1993_num_190_1_4214
- **Confiance générale:** MEDIUM

### NAG — Nagpur

- **Current tier:** `tier_5`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `shaft_mining`
- **Technologies frontière/sectorielles:** `shaft_mining`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions.
- **Justification historique:** Documented metallurgy or mineral extraction existed, but the gameplay node unlocks a broad suite of organized shaft mines; equivalence is uncertain. Court, revenue, legal and artisanal knowledge systems justify the abstract node without implying the European print/scientific institutions used as its game-tree parents. Established agrarian systems make the broad husbandry node plausible; this is not a claim of European agricultural-revolution techniques.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### NAR — Narsinghpur

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### NAW — Nawanagar

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### NEP — Nepal

- **Current tier:** `tier_5`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `international_relations`, `scientific_fortification_siegecraft`
- **Technologies à REMOVE:** `shaft_mining`
- **Technologies à REVIEW:** `regulated_small_arms`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `regulated_small_arms`, `scientific_fortification_siegecraft`, `standardized_field_artillery`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete.
- **Justification historique:** The newly unified Gorkha/Nepal state conducted active Himalayan diplomacy and warfare under Prithvi Narayan Shah and his immediate successors. Fortified warfare, cannon and locally supplied gunpowder/firearms are documented; the node is best treated sectorally. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/books/history-of-nepal/340C4E78125368B8D0623201D61E5A9E/listing; https://api.repository.cam.ac.uk/server/api/core/bitstreams/f72a7ab9-6ec8-430d-9143-9054f6882d59/content
- **Confiance générale:** MEDIUM

### NGA — Naga

- **Current tier:** `tier_6`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `improved_husbandry`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `urbanization`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Aucun cas majeur au-delà des abstractions générales de l’arbre.
- **Justification historique:** The generic tier overstates the settlement/administrative infrastructure implied by the game node for this decentralized upland society in 1776. Established agrarian systems make the broad husbandry node plausible; this is not a claim of European agricultural-revolution techniques.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5
- **Confiance générale:** HIGH

### PAN — Punjab

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `traditional_papermaking`
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `regulated_small_arms`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** Punjab/Sialkot had established handmade paper traditions; this is local production rather than imported print culture. The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node.
- **Sources:** https://www.cambridge.org/core/books/abs/sikhs-of-the-punjab/rise-to-political-power-17081799/832A55666B8A8966093418C4CB1190BD; https://www.cambridge.org/core/journals/comparative-studies-in-society-and-history/article/mahzarnamas-in-the-mughal-and-british-empires-the-uses-of-an-indoislamic-legal-form/043DCAAC39A0EF07816B80BB63349BE3; https://www.nature.com/articles/s40494-024-01360-9; https://cppri.res.in/en/paper-museum-kagaj-sangralya/historical-perspective
- **Confiance générale:** MEDIUM

### PLP — Palanpur

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### PTA — Patiala

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `regulated_small_arms`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/books/abs/sikhs-of-the-punjab/rise-to-political-power-17081799/832A55666B8A8966093418C4CB1190BD; https://www.cambridge.org/core/journals/comparative-studies-in-society-and-history/article/mahzarnamas-in-the-mughal-and-british-empires-the-uses-of-an-indoislamic-legal-form/043DCAAC39A0EF07816B80BB63349BE3
- **Confiance générale:** MEDIUM

### PTN — Patna

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### PUD — Pudukottai

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### SAT — Satara

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `regulated_small_arms`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### SIK — Sikkim

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`, `urbanization`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### SIN — Sindh

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`, `shaft_mining`
- **Technologies frontière/sectorielles:** `regulated_small_arms`, `shaft_mining`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. Do not add scientific_fortification_siegecraft solely to repair the game prerequisite.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Firearms were used, but evidence for the regulated production/standardization implied by the arms-industry unlock is insufficient for a confident KEEP.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### SUR — Surguja

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `systematic_administrative_statistics`, `urbanization`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. scientific_fortification_siegecraft is the game parent; assess it historically, not as an automatic prerequisite repair.
- **Justification historique:** The generic tier projects standardized light-infantry doctrine too broadly; local forces could be effective without this specific frontier system. Owning cannon or siege guns does not establish the standardized field-artillery organization implied by this frontier node. Possession of matchlocks or artillery is not enough to establish the regulated arms-industry capability represented by this node in 1776.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D
- **Confiance générale:** MEDIUM

### TIP — Tipperah

- **Current tier:** `tier_6`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `improved_husbandry`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `urbanization`
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** Aucun cas majeur au-delà des abstractions générales de l’arbre.
- **Justification historique:** Court or market centres existed, but the game node also unlocks a construction-sector/urban-centre system; local equivalence at start is uncertain. Established agrarian systems make the broad husbandry node plausible; this is not a claim of European agricultural-revolution techniques.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5
- **Confiance générale:** MEDIUM

### TRA — Travancore

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `regulated_small_arms`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`
- **Technologies à REMOVE:** `shaft_mining`
- **Technologies à REVIEW:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`
- **Prérequis problématiques:** Do not auto-add institutionalized_scientific_exchange or periodical_print_networks; the tree compresses different knowledge traditions. regulated_small_arms is the game parent; do not add/remove solely to make the graph visually complete. The parent scientific_fortification_siegecraft is absent and is assessed separately.
- **Justification historique:** De Lannoy’s long service in Travancore produced European-style fortification and military reorganization before his death in 1777. Local quarrying, salt, gems or artisanal extraction do not by themselves justify the broad organized shaft-mining system unlocked by this node. European-trained forces existed, but their scale and continuity do not clearly justify a state-wide frontier tactics node.
- **Sources:** https://www.cambridge.org/core/books/abs/indian-princes-and-their-states/princely-states-prior-to-1800/8205D5368645057EA899F9AEAF323BF5; https://www.cambridge.org/core/books/abs/cambridge-economic-history-of-india/mideighteenthcentury-background/364CC8EA015BAFBE8B0A2EEDAA0FD3C5; https://www.cambridge.org/core/journals/modern-asian-studies/article/from-negotiation-to-coercion-textile-manufacturing-in-india-in-the-eighteenth-century/9ECA84ADA531FC112E225221E773267D; https://fr.wikipedia.org/wiki/Eustache_de_Lannoy
- **Confiance générale:** MEDIUM

## 5. Comparaison régionale

- **BIC / Awadh / Mysore** concentrent les cas les plus convaincants d’organisation militaire de type régulier/frontière avant 1776; leur proximité technologique sur certains nœuds militaires ne signifie pas des institutions identiques.
- **Marathes** : capacité navale d’État clairement supérieure à la plupart des États intérieurs, administration intégratrice, mais doctrine/artillerie européenne tardive à ne pas rétro-projeter depuis les réformes postérieures.
- **Moghol/Hindustan** : forte profondeur administrative, artisanale et urbaine, mais empire politiquement fragmenté; ses acquis ne sont pas distribués automatiquement à Hyderabad, Awadh, Bengale/Company ou autres successeurs.
- **Punjab sikh** : puissance militaire réelle des misls, mais l’arbre générique tier 4 sur-interprète cette puissance comme standardisation industrielle/tactique; plusieurs nœuds militaires passent donc en REVIEW/REMOVE.
- **Himalaya et uplands du Nord-Est** : agriculture, artisanat, armes et diplomatie peuvent être solides localement sans correspondre aux nœuds de mine/urbanisation/artillerie standardisée du tier 4.
- **Ceylan** : exemple le plus net d’un palier générique trompeur. Fortifications, ports, VOC et imprimerie sont réels, mais vapeur minière, coke, precision boring, stock exchange et réseau périodique ne le sont pas localement en 1776.

## 6. Technologies frontière 1776

| Technologie | Recommandation régionale | Motif |
|---|---|---|
| `mechanized_spinning` | Aucun ADD; REVIEW explicite pour grands pôles textiles | Excellence du coton/soie ≠ machine spinning. |
| `atmospheric_engine` | Aucun ADD; REMOVE à BCE; REVIEW négatif BIC/MYS/MARATH | Aucun déploiement local établi de moteur atmosphérique minier avant la coupure. |
| `precision_boring` | Aucun ADD; REMOVE à BCE | Nœud lié à une chaîne vapeur/métallurgie qui n’est pas attestée localement. |
| `coke_smelting` | Aucun ADD; REMOVE à BCE | Wootz, zinc et autres métallurgies ne sont pas la fonte au coke. |
| `standardized_field_artillery` | KEEP BIC/AWA; ADD MYS (MEDIUM); REVIEW HYD/TRA/MARATH/NEP; REMOVE dans la plupart des autres tier 4 | Capacité très inégalement institutionnalisée. |
| `military_topographic_surveying` | ADD BIC | Rennell : survey Bengal 1764, Surveyor-General 1767. |
| `systematic_cadastral_surveying` | REVIEW BIC | Relevés systématiques, mais pas nécessairement cadastre mature. |
| `state_dockyard_systems` | KEEP MARATH/BCE; ADD BIC; REVIEW MYS/COC | Dockyards réels mais localisés et institutionnellement différents. |
| `mysorean_iron_cased_rocketry` | REVIEW MYS | Rockets sous Hyder avant 1776 plausibles; système avancé le mieux documenté surtout dans les guerres des années 1780–1790. |
| `improved_agricultural_implements` / `industrial_canals` | Aucun ADD automatique | Irrigation/agriculture intensive ne suffisent pas à ces nœuds gameplay spécifiques. |

## 7. Anachronismes et attributions à retirer

Aucun des 59 TAG n’a actuellement de technologie classée **C/D** dans l’audit global. Les principaux retraits sont donc des **mauvaises équivalences locales**, pas des anachronismes mondiaux : `BCE` perd notamment coke, vapeur atmosphérique, precision boring, stock exchange, assurance commerciale et periodical press; de nombreux petits tier 4 perdent `light_infantry_tactics`, `standardized_field_artillery`, parfois `regulated_small_arms`, et `shaft_mining`. Ces technologies peuvent exister ailleurs en 1776 tout en étant injustifiées pour le pays concerné.

## 8. Prérequis

Le cas le plus fréquent est `codified_practical_knowledge`, dont les parents de l’arbre (`institutionalized_scientific_exchange`, `periodical_print_networks`) ne décrivent pas correctement les traditions manuscrites, administratives et artisanales indiennes. La recommandation est donc de **tolérer l’abstraction**, pas d’ajouter automatiquement les parents. Même logique pour `regulated_small_arms` et ses enfants : lorsqu’un enfant est retiré, on ne répare pas le graphe; lorsqu’un parent est historiquement justifié (BIC, AWA, Mysore, Hyderabad, Travancore), il reçoit sa propre justification. Pour `military_topographic_surveying` à BIC, le parent `permanent_engineer_services` reste une dette d’arbre, car la preuve historique du survey est directe.

## 9. Incertitudes

1. **Mysorean rocketry** : la continuité sous Hyder est réelle, mais la datation exacte du système iron-cased standardisé avant le 1er janvier 1776 reste moins solide que les preuves des années 1780; REVIEW conservateur.
2. **`systematic_administrative_statistics`** : le nœud du jeu fusionne bureau fiscal, collecte de données et administration; son équivalence varie fortement entre cour moghole, successeurs et petites principautés.
3. **`shaft_mining`** : les traditions minières/métallurgiques indiennes sont réelles, mais le déblocage gameplay couvre une gamme de mines beaucoup plus large; d’où plusieurs REVIEW.
4. **Cochin** : fortes compétences de construction navale locales, mais chantier institutionnel VOC; ne pas transférer mécaniquement au TAG natif.
5. **BHV** : le CSV agrège deux fichiers actifs et deux tiers (`tier_4;tier_5`); `REVIEW_TIER` est obligatoire jusqu’à résolution de cette duplication hors de cette recherche.
6. **Bengale** : faute de TAG Bengali séparé dans le périmètre, ne pas généraliser les capacités de Bengal Presidency à tous les États orientaux.

## 10. Recommandations pour l’implémentation

- **KEEP_TIER : 1 pays.** Le palier peut rester si les ADD explicites proposés sont appliqués séparément.
- **REVIEW_TIER : 6 pays.** Le palier contient au moins une capacité dont l’équivalence historique reste ambiguë.
- **REPLACE_WITH_EXPLICIT_SETUP : 52 pays.** Le palier générique accorde au moins une technologie qui doit être retirée; un setup explicite est plus sûr qu’un changement global de tier.
- **CHANGE_TIER : 0 pays.** Aucun changement de tier entier n’est recommandé : les conséquences groupées sont trop grossières pour cette région technologiquement asymétrique.
- Les dossiers à traiter en premier lors de la synthèse mondiale sont `BCE`, `BIC`, `MYS`, `MARATH`, `MUG`, `AWA`, `HYD`, `PAN/PTA`, `NEP`, plus `BHV` pour sa duplication de setup.

## Contrôle final

- TAG étudiés : **59**
- ADD : **30**
- REMOVE : **165**
- REVIEW : **91**
- KEEP : **360**
- Pays pour lesquels le tier doit changer (`CHANGE_TIER`) : **0**
- Lignes pays-technologie dans la matrice : **646**
- Toutes les technologies explicites actuelles des 59 TAG ont une décision. Tous les IDs recommandés existent dans `TECH_START_1776_TECHNOLOGIES.csv`. Aucun fichier de gameplay n’a été modifié.
