# TECH_START_1776_MIDDLE_EAST_SECOND_PASS_FULL

**Date absolue : 1776-01-01**  

**Statut : recherche historique uniquement — aucun changement gameplay, aucun code, aucun commit, aucun push.**

## 1. Périmètre

Cette seconde passe conserve le périmètre régional de la première étude : Empire ottoman, Balkans, Égypte, Levant/Irak, péninsule Arabique, Perse/Iran, Caucase, Asie centrale et espace afghan. Le Maghreb à l’ouest de l’Égypte et le sous-continent indien sont exclus. `CHT` reste un cas frontière à dédoublonner lors de la synthèse mondiale si nécessaire.

- TAG audités : **49**
- Technologies A : **25**
- Technologies B : **36**
- Relations A/B effectivement examinées : **2989**
- Technologies E significatives examinées : **5** × 49 = **245** relations
- Relations totales de la matrice de travail : **3234**

TAG : `ABB`, `ABU`, `ARB`, `ARM`, `BHN`, `BUK`, `CHC`, `CHT`, `CIR`, `CRO`, `DUR`, `EGY`, `GRE`, `HDJ`, `HER`, `HUN`, `ION`, `IR1`, `JAB`, `JBB`, `KAB`, `KAF`, `KAL`, `KAN`, `KAT`, `KBB`, `KHI`, `KOK`, `KUN`, `KZH`, `LAH`, `MAH`, `MAI`, `MAK`, `MBB`, `MOL`, `MON`, `NBB`, `NEJ`, `OMA`, `OZH`, `PER`, `SER`, `TRM`, `TRS`, `TUR`, `UZH`, `WAL`, `ZAI`.

## 2. Sources et méthode

Le second passage **ne repart pas des tiers comme hypothèse historique**. Pour chacune des 61 technologies A/B, les 49 TAG ont été examinés, puis les décisions ont été comparées à la distribution réellement implémentée sur la branche de réconciliation. Les prérequis ne servent jamais à nier une capacité historiquement attestée : ils sont évalués après la décision historique et produisent, lorsque nécessaire, `TREE_STRUCTURE_REVIEW`. Les quatre problèmes globaux de classification explicitement conservés sont `sugar_refining`, `mechanized_weaving`, `advanced_spinning` et `medical_degrees`.

Le CSV différentiel ne reproduit pas les milliers de relations triviales : il contient les `ADD`, `REMOVE`, `REVIEW`, les `TREE_STRUCTURE_REVIEW`, les `CLASSIFICATION_REVIEW`, ainsi que les quelques `PRESENT + KEEP` sectoriels/frontière dont la conservation est historiquement importante ou contestable. `COVERAGE.csv` fournit la preuve exhaustive 61 × 49.

## 3. Production et artisanat

Le changement principal est la séparation effective des artisanats traditionnels. La première passe restait trop dépendante de `organized_textile_production` et de l’ancien rôle fourre-tout de `organized_forestry`. Le second passage traite séparément `traditional_food_processing`, `traditional_papermaking`, `traditional_glassmaking` et `traditional_furniture_making`.

- `traditional_food_processing` : **28 ADD**, **21 REVIEW**. La transformation alimentaire traditionnelle est largement plus répandue que ce que la première distribution laissait entendre.
- En Perse, dans plusieurs centres d’Asie centrale et dans les espaces habsbourgeois, papier, verre et meuble sont reconnus comme capacités artisanales indépendantes; aucune nécessité d’`organized_forestry` n’est présumée.
- `industrial_acids`, `industrial_ceramics`, `mechanized_spinning`, `precision_boring` et autres nœuds industriels ne sont ajoutés que lorsqu’une preuve spécifique l’exige; l’existence d’artisans compétents ne suffit pas à les distribuer.

`sugar_refining` est laissé absent là où son contenu gameplay n’est pas établi, mais surtout il devient un **CLASSIFICATION_REVIEW global** : le nœud A débloque des procédés tels que la vacuum pan (Howard, 1813) et l’évaporation à vapeur. Il ne peut donc pas servir de simple alias au raffinage du sucre traditionnel du XVIIIe siècle.

## 4. Agriculture

`improved_husbandry` reste largement plausible, mais le second passage évite de transformer toute agriculture ou tout élevage en preuve de `selective_breeding`, `advanced_crop_rotations` ou `improved_agricultural_implements`. Les pratiques améliorées sont conservées en `REVIEW` lorsqu’elles sont expérimentales, domaniales ou sectorielles. Les économies pastorales kazakhes et turkmènes sont traitées comme des systèmes techniques propres et non comme des versions incomplètes d’un modèle agricole européen.

## 5. Mines et métallurgie

`shaft_mining` est l’un des nœuds les plus corrigés : 19 `REMOVE` et 22 `REVIEW`. La présence de mines ou de métallurgie ne suffit pas à établir une extraction par puits au sens du nœud.

L’Empire ottoman conserve une capacité minière sectorielle solide (Keban–Ergani, Gümüşhane et autres centres administrés). La Hongrie/les terres habsbourgeoises disposent d’un cas beaucoup plus avancé : enseignement minier, minéralogie appliquée et surtout machine atmosphérique de Nová Baňa dès 1722. **HUN `atmospheric_engine = ADD`** est donc maintenu. Son parent `coke_smelting` n’étant pas historiquement nécessaire à cette installation, le cas reste explicitement `TREE_STRUCTURE_REVIEW`.

À l’inverse, `coke_smelting` est retiré d’EGY/GRE/ION lorsque le tier 3 l’avait attribué sans base locale suffisante. `applied_mineralogy` est également retiré lorsque la seule preuve porte sur l’existence de mines, pas sur une science minéralogique appliquée.

## 6. Infrastructure

`organized_forestry` utilise désormais sa nouvelle définition stricte : gestion forestière organisée/rationalisée. La coupe de bois ou la présence de métiers du bois ne suffisent plus. HUN est un cas positif fort grâce au règlement forestier général de 1769; CRO/TRS sont évalués séparément selon leur raccordement institutionnel habsbourgeois.

`turnpike_road_networks`, `industrial_canals` et les autres nœuds B d’infrastructure restent généralement absents dans la région sauf preuve institutionnelle spécifique. Le second passage évite d’inférer ces réseaux depuis le simple commerce à longue distance.

## 7. Finance et économie

La finance est l’un des domaines que la première passe sous-évaluait. Le cas le plus important ici est **TUR `institutionalized_public_credit = ADD`** : le système d’eshām est introduit en 1775 comme mécanisme de financement public intérieur. Au 1er janvier 1776, la capacité est donc réelle, quoique très récente (`FRONTIER`).

Le second passage distingue systématiquement crédit public, assurance commerciale et bourse. Une économie marchande active ne reçoit pas automatiquement `commercial_insurance_markets` ou `stock_exchange`. HUN reste en `REVIEW` pour le crédit public propre au royaume parce que l’institution impériale viennoise ne doit pas être convertie sans nuance en institution nationale hongroise.

`political_economy` reçoit un traitement institutionnel : HUN est `ADD` grâce aux formations politico-camérales des années 1760, mais la chaîne de prérequis commerciale/statistique du jeu ne correspond pas proprement à ce chemin historique et produit un `TREE_STRUCTURE_REVIEW`.

## 8. Commerce et relations internationales

`international_relations` est conservé lorsqu’un appareil diplomatique ou une insertion interétatique structurée est attesté, y compris pour des États non européens. Le second passage ne l’assimile pas à la diplomatie moderne du XIXe siècle. En revanche, les institutions commerciales spécialisées restent séparées : assurance, bourse et crédit public exigent chacune leur preuve.

Oman, le Golfe, l’Irak, la Perse et l’Asie centrale sont évalués comme des espaces de commerce à longue distance réels sans que ce commerce entraîne mécaniquement des `stock_exchange` ou des marchés d’assurance comparables aux places financières européennes.

## 9. Administration

`systematic_administrative_statistics` connaît **29 REMOVE** et **9 REVIEW** : c’est l’un des principaux faux positifs des anciens tiers. Une fiscalité ou une bureaucratie écrite ne suffit pas à prouver des statistiques administratives systématiques.

HUN constitue à nouveau une exception documentée avec des opérations d’enregistrement démographique avant 1776; `systematic_population_registration` y est `ADD`. En Transylvanie, cartographie/cadastre restent plus prudents (`REVIEW`). En Wallachie/Moldavie et dans les provinces ottomanes, les registres administratifs sont reconnus sans les convertir automatiquement en cadastre ou statistique uniforme.

## 10. Science et éducation

La distinction entre université traditionnelle, société savante, académie technique et enseignement élémentaire organisé est maintenue. TUR conserve `specialized_technical_academies` comme capacité FRONTIER grâce à l’école du chantier impérial de 1775; le même établissement justifie `scientific_naval_architecture = ADD`, sans prétendre à une diffusion générale de l’ingénierie européenne.

HUN est nettement réévaluée : académie minière de Selmecbánya et formations camérales justifient `specialized_technical_academies`. CRO reçoit également une reconnaissance spécifique pour Varaždin. À l’inverse, EGY/GRE/ION perdent les académies techniques héritées du tier 3 lorsqu’aucune institution comparable n’est établie au 1er janvier 1776.

## 11. Médecine

La définition de `medical_degrees` est appliquée telle qu’amendée : facultés, collèges, titres et formation institutionnalisée des praticiens, et non diplôme médical moderne du XIXe siècle. Cela produit deux effets simultanés :

- **HUN = ADD** : la faculté de médecine de Nagyszombat ouvre en 1770.
- **TUR = ADD** : la formation médicale institutionnalisée ottomane dans les darüşşifa et la madrasa médicale de Süleymaniye précède largement 1776.
- **EGY/GRE/ION = REMOVE** lorsque le tier 3 projetait une institution locale non démontrée en 1776.

Le nœud est en même temps marqué **CLASSIFICATION_REVIEW: CLASSIFICATION_TOO_LATE** : des facultés médicales pleinement institutionnalisées existent bien avant 1776 (Édimbourg 1726, Vienne depuis des siècles, Nagyszombat 1770). La distribution pays et la classification globale sont donc deux questions distinctes.

`variolation_networks` est `ADD` pour TUR : la variolisation est attestée et pratiquée à Constantinople bien avant 1776. HUN reste plus prudente lorsque la pratique existe sans preuve suffisante d’un réseau public systématique à la date de coupure.

## 12. Militaire terrestre

`standardized_field_artillery` est le plus gros retrait militaire : **35 REMOVE** sur 49. Les tiers avaient confondu possession de pièces, artillerie occasionnelle et système de campagne standardisé. Les khanats d’Asie centrale, plusieurs entités arabiques et caucasiennes, ainsi que la Perse zand, sont fortement corrigés.

`regulated_small_arms` totalise **33 REVIEW** et **7 REMOVE**. La diffusion massive de mousquets en Arabie, Afghanistan ou Caucase est reconnue, mais le nœud gameplay est plus fort que la simple possession d’armes car il représente également réglementation/industrie. Les cas ambigus restent donc en `REVIEW` plutôt que d’être forcés.

L’Empire ottoman conserve son artillerie et ses armes réglementaires; les Balkans habsbourgeois bénéficient d’un véritable appareil d’ingénieurs et de fortification. HUN/CRO/TRS obtiennent plusieurs `ADD` liés aux ingénieurs, inspections et fortifications quand la capacité impériale est effectivement disponible territorialement.

## 13. Marine

La marine est traitée comme un domaine hautement discriminant. **TUR** reçoit `state_dockyard_systems` et `scientific_naval_architecture`; le Tersâne-i Âmire est un arsenal d’État ancien, et l’école technique navale existe depuis avril 1775. **IR1** reçoit `state_dockyard_systems` sectoriellement pour Bassora, où des constructions navales d’État sont attestées au XVIIIe siècle.

**PER**, au contraire, perd `state_dockyard_systems`: la flotte de Nāder Shah des années 1730–1740 ne survit pas comme système naval zand durable en 1776. **OMA** est retenu comme puissance maritime régionale et obtient un profil naval plus fort, mais les nœuds de chronométrie, classification des navires et docks fermés restent réservés aux cas réellement documentés.

## 14. Analyse pays par pays

### ABB — Arab Emirates

- **ADD:** 4 — `codified_practical_knowledge`, `distillation`, `international_relations`, `organized_textile_production`
- **REMOVE:** 0 — —
- **REVIEW:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### ABU — Trucial States

- **ADD:** 1 — `traditional_food_processing`
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 3 — `light_infantry_tactics`, `regulated_small_arms`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### ARB — Arabistan

- **ADD:** 4 — `distillation`, `international_relations`, `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 1 — `systematic_administrative_statistics`
- **REVIEW:** 2 — `shaft_mining`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 1 — `codified_practical_knowledge`
- **Diagnostic:** Profil artisanal et commercial significatif, mais les capacités d'État centralisées doivent être distinguées des réseaux marchands et des métiers locaux; le second passage favorise les artisanats établis et réduit les extrapolations militaires.

### ARM — Armenia

- **ADD:** 2 — `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 2 — `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 5 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `traditional_papermaking`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Profil artisanal et commercial significatif, mais les capacités d'État centralisées doivent être distinguées des réseaux marchands et des métiers locaux; le second passage favorise les artisanats établis et réduit les extrapolations militaires.

### BHN — Bahrain

- **ADD:** 1 — `traditional_food_processing`
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 3 — `light_infantry_tactics`, `regulated_small_arms`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### BUK — Bukhara

- **ADD:** 4 — `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`
- **REMOVE:** 3 — `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`
- **REVIEW:** 3 — `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 1 — `codified_practical_knowledge`
- **Diagnostic:** Bukhara combine agriculture irriguée, textile, papier, métiers urbains et commerce, mais les sarbāz permanents et l'artillerie régulière appartiennent surtout au XIXe siècle. L'artisanat est revalorisé, les nœuds militaires retirés.

### CHC — Chechnya

- **ADD:** 0 — —
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 5 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le Caucase du Nord possède des traditions militaires et artisanales propres; présence d'armes à feu ne signifie ni industrie réglementaire, ni artillerie standardisée, ni bureaucratie statistique. Plusieurs nœuds restent sectoriels/REVIEW.

### CHT — Chitral

- **ADD:** 0 — —
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 5 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le sous-espace afghan/hindou-kouchien combine artisanats, circulation d'armes et structures politiques locales sans justifier automatiquement les standards d'une armée régulière ou d'une administration statistique. Les décisions restent volontairement asymétriques.

### CIR — Circassia

- **ADD:** 0 — —
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `codified_practical_knowledge`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 3 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`
- **Diagnostic:** Le Caucase du Nord possède des traditions militaires et artisanales propres; présence d'armes à feu ne signifie ni industrie réglementaire, ni artillerie standardisée, ni bureaucratie statistique. Plusieurs nœuds restent sectoriels/REVIEW.

### CRO — Croatia

- **ADD:** 8 — `armament_standardization_inspection`, `organized_forestry`, `periodical_print_networks`, `permanent_engineer_services`, `scientific_fortification_siegecraft`, `specialized_technical_academies`, `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 0 — —
- **REVIEW:** 4 — `shaft_mining`, `traditional_glassmaking`, `traditional_papermaking`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 0 — —
- **Diagnostic:** Le raccordement à l'appareil habsbourgeois justifie ingénieurs, fortification, formation camérale et plusieurs artisanats; il ne faut cependant pas transformer toute capacité impériale en diffusion uniforme locale.

### DUR — Afghanistan

- **ADD:** 2 — `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 0 — —
- **REVIEW:** 4 — `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** L'État durrani possède une diplomatie et une administration persanophone réelles et des armes à feu diffusées, mais pas une armée régulière/artillerie standardisée de type XIXe siècle; plusieurs capacités restent sectorielles.

### EGY — Egypt

- **ADD:** 3 — `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`
- **REMOVE:** 5 — `applied_mineralogy`, `coke_smelting`, `commercial_insurance_markets`, `medical_degrees`, `specialized_technical_academies`
- **REVIEW:** 6 — `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`, `variolation_networks`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** L'Égypte de 1776 est riche et manufacturière au sens artisanal, mais le tier 3 projette trop de capacités industrielles, médicales et académiques associées aux réformes postérieures de Muḥammad ʿAlī.

### GRE — Greece

- **ADD:** 2 — `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 8 — `applied_mineralogy`, `coke_smelting`, `commercial_insurance_markets`, `medical_degrees`, `periodical_print_networks`, `specialized_technical_academies`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le setup tier 3 est nettement surévalué pour 1776. Artisanat et réseaux commerciaux sont réels, mais coke, minéralogie appliquée, diplômes médicaux, académie technique et presse périodique locale sont retirés.

### HDJ — Hedjaz

- **ADD:** 1 — `traditional_food_processing`
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 3 — `light_infantry_tactics`, `regulated_small_arms`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### HER — Herat

- **ADD:** 2 — `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 1 — `standardized_field_artillery`
- **REVIEW:** 4 — `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 3 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`
- **Diagnostic:** Le sous-espace afghan/hindou-kouchien combine artisanats, circulation d'armes et structures politiques locales sans justifier automatiquement les standards d'une armée régulière ou d'une administration statistique. Les décisions restent volontairement asymétriques.

### HUN — Hungary

- **ADD:** 16 — `applied_mineralogy`, `armament_standardization_inspection`, `atmospheric_engine`, `medical_degrees`, `organized_forestry`, `periodical_print_networks`, `permanent_engineer_services`, `political_economy`, `scientific_fortification_siegecraft`, `specialized_technical_academies`, `systematic_population_registration`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `veterinary_science`
- **REMOVE:** 0 — —
- **REVIEW:** 8 — `advanced_crop_rotations`, `commercial_insurance_markets`, `improved_agricultural_implements`, `institutionalized_public_credit`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `urbanization`, `variolation_networks`
- **TREE_STRUCTURE_REVIEW:** 3 — `advanced_crop_rotations`, `atmospheric_engine`, `political_economy`
- **Diagnostic:** Révision majeure à la hausse dans les capacités institutionnelles habsbourgeoises : médecine universitaire (1770), formation camérale, académie minière, réglementation forestière, enregistrement démographique et machine atmosphérique de Nová Baňa (1722). atmospheric_engine reste un TREE_STRUCTURE_REVIEW à cause de coke_smelting.

### ION — Ionian Islands

- **ADD:** 3 — `scientific_fortification_siegecraft`, `state_dockyard_systems`, `traditional_food_processing`
- **REMOVE:** 6 — `applied_mineralogy`, `coke_smelting`, `medical_degrees`, `specialized_technical_academies`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 6 — `commercial_insurance_markets`, `light_infantry_tactics`, `regulated_small_arms`, `scientific_naval_architecture`, `shaft_mining`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `commercial_insurance_markets`
- **Diagnostic:** Les îles Ioniennes disposent d'un profil maritime et artisanal plus fort que la Grèce continentale, mais le tier 3 reste trop généreux sur industrie, administration et institutions savantes; plusieurs capacités maritimes restent en REVIEW.

### IR1 — Mamluk Iraq

- **ADD:** 3 — `state_dockyard_systems`, `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 1 — `institutionalized_scientific_exchange`
- **REVIEW:** 5 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`, `traditional_glassmaking`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** L'Irak mamelouk conserve une base ottomane commerciale et militaire; le chantier de Bassora justifie state_dockyard_systems sectoriellement, mais institutionalized_scientific_exchange n'est pas démontré localement.

### JAB — Jabal Shammar

- **ADD:** 0 — —
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### JBB — Jabal

- **ADD:** 4 — `codified_practical_knowledge`, `distillation`, `international_relations`, `organized_textile_production`
- **REMOVE:** 0 — —
- **REVIEW:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### KAB — Kabul

- **ADD:** 2 — `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 1 — `standardized_field_artillery`
- **REVIEW:** 4 — `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 3 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`
- **Diagnostic:** Le sous-espace afghan/hindou-kouchien combine artisanats, circulation d'armes et structures politiques locales sans justifier automatiquement les standards d'une armée régulière ou d'une administration statistique. Les décisions restent volontairement asymétriques.

### KAF — Kafiristan

- **ADD:** 0 — —
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 5 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le sous-espace afghan/hindou-kouchien combine artisanats, circulation d'armes et structures politiques locales sans justifier automatiquement les standards d'une armée régulière ou d'une administration statistique. Les décisions restent volontairement asymétriques.

### KAL — Kalat

- **ADD:** 0 — —
- **REMOVE:** 2 — `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 5 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le sous-espace afghan/hindou-kouchien combine artisanats, circulation d'armes et structures politiques locales sans justifier automatiquement les standards d'une armée régulière ou d'une administration statistique. Les décisions restent volontairement asymétriques.

### KAN — Kandahar

- **ADD:** 2 — `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 1 — `standardized_field_artillery`
- **REVIEW:** 4 — `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 3 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`
- **Diagnostic:** Le sous-espace afghan/hindou-kouchien combine artisanats, circulation d'armes et structures politiques locales sans justifier automatiquement les standards d'une armée régulière ou d'une administration statistique. Les décisions restent volontairement asymétriques.

### KAT — Kathiri

- **ADD:** 0 — —
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 5 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### KBB — Kathiri

- **ADD:** 3 — `distillation`, `international_relations`, `organized_textile_production`
- **REMOVE:** 0 — —
- **REVIEW:** 5 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### KHI — Khiva

- **ADD:** 3 — `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`
- **REMOVE:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 3 — `shaft_mining`, `traditional_papermaking`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 1 — `codified_practical_knowledge`
- **Diagnostic:** Khiva est réévaluée vers davantage d'artisanat traditionnel mais moins de capacités militaires régulières : armes réglementaires, infanterie légère standardisée et artillerie de campagne ne sont pas établies en 1776.

### KOK — Kokand

- **ADD:** 3 — `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`
- **REMOVE:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 3 — `shaft_mining`, `traditional_papermaking`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 1 — `codified_practical_knowledge`
- **Diagnostic:** Kokand dispose d'une base artisanale et commerciale, mais la professionnalisation militaire associée à son expansion est surtout postérieure à 1799; les nœuds de tier 4 militaires sont donc retirés.

### KUN — Kunduz

- **ADD:** 0 — —
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le sous-espace afghan/hindou-kouchien combine artisanats, circulation d'armes et structures politiques locales sans justifier automatiquement les standards d'une armée régulière ou d'une administration statistique. Les décisions restent volontairement asymétriques.

### KZH — Kishi Zhuz

- **ADD:** 0 — —
- **REMOVE:** 5 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `codified_practical_knowledge`, `organized_textile_production`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 1 — `codified_practical_knowledge`
- **Diagnostic:** Société pastorale/commerciale à capacités propres; le second passage retire les faux standards militaires et administratifs hérités du tier 4 tout en conservant ou réexaminant textile, élevage et savoirs pratiques selon les preuves.

### LAH — Lahej

- **ADD:** 1 — `traditional_food_processing`
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### MAH — Mahra

- **ADD:** 0 — —
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 5 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### MAI — Maimana

- **ADD:** 0 — —
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le sous-espace afghan/hindou-kouchien combine artisanats, circulation d'armes et structures politiques locales sans justifier automatiquement les standards d'une armée régulière ou d'une administration statistique. Les décisions restent volontairement asymétriques.

### MAK — Makran

- **ADD:** 0 — —
- **REMOVE:** 2 — `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 5 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le sous-espace afghan/hindou-kouchien combine artisanats, circulation d'armes et structures politiques locales sans justifier automatiquement les standards d'une armée régulière ou d'une administration statistique. Les décisions restent volontairement asymétriques.

### MBB — Mahra

- **ADD:** 3 — `distillation`, `international_relations`, `organized_textile_production`
- **REMOVE:** 0 — —
- **REVIEW:** 5 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### MOL — Moldavia

- **ADD:** 2 — `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 1 — `standardized_field_artillery`
- **REVIEW:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le second passage distingue institutions locales, accès à l'appareil ottoman/habsbourgeois et capacités réellement territoriales. Les artisanats traditionnels sont mieux reconnus tandis que plusieurs standards militaires/administratifs restent en REVIEW ou sont retirés.

### MON — Montenegro

- **ADD:** 1 — `traditional_food_processing`
- **REMOVE:** 2 — `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 5 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le second passage distingue institutions locales, accès à l'appareil ottoman/habsbourgeois et capacités réellement territoriales. Les artisanats traditionnels sont mieux reconnus tandis que plusieurs standards militaires/administratifs restent en REVIEW ou sont retirés.

### NBB — Nejd

- **ADD:** 2 — `codified_practical_knowledge`, `organized_textile_production`
- **REMOVE:** 0 — —
- **REVIEW:** 3 — `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### NEJ — Nejd

- **ADD:** 2 — `distillation`, `international_relations`
- **REMOVE:** 2 — `shaft_mining`, `systematic_administrative_statistics`
- **REVIEW:** 3 — `regulated_small_arms`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

### OMA — Oman

- **ADD:** 3 — `state_dockyard_systems`, `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 1 — `standardized_field_artillery`
- **REVIEW:** 4 — `scientific_naval_architecture`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Oman est une puissance maritime régionale réelle avec armes à feu et savoir-faire naval; state_dockyard_systems est retenu, mais la standardisation de l'artillerie et plusieurs institutions administratives restent limitées.

### OZH — Orta Zhuz

- **ADD:** 0 — —
- **REMOVE:** 5 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `codified_practical_knowledge`, `organized_textile_production`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 1 — `codified_practical_knowledge`
- **Diagnostic:** Société pastorale/commerciale à capacités propres; le second passage retire les faux standards militaires et administratifs hérités du tier 4 tout en conservant ou réexaminant textile, élevage et savoirs pratiques selon les preuves.

### PER — Persia

- **ADD:** 4 — `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`
- **REMOVE:** 2 — `standardized_field_artillery`, `state_dockyard_systems`
- **REVIEW:** 4 — `medical_degrees`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 3 — `codified_practical_knowledge`, `medical_degrees`, `regulated_small_arms`
- **Diagnostic:** La Perse zand conserve armes à feu, artisanats et administration, mais le système naval de Nāder Shah n'est plus un dockyard d'État fonctionnel en 1776 et l'artillerie de campagne standardisée est surévaluée. Le second passage renforce surtout papier/verre/meuble/alimentation.

### SER — Serbia

- **ADD:** 2 — `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 2 — `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le second passage distingue institutions locales, accès à l'appareil ottoman/habsbourgeois et capacités réellement territoriales. Les artisanats traditionnels sont mieux reconnus tandis que plusieurs standards militaires/administratifs restent en REVIEW ou sont retirés.

### TRM — Turkmenia

- **ADD:** 0 — —
- **REMOVE:** 5 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `codified_practical_knowledge`, `organized_textile_production`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 1 — `codified_practical_knowledge`
- **Diagnostic:** Société pastorale/commerciale à capacités propres; le second passage retire les faux standards militaires et administratifs hérités du tier 4 tout en conservant ou réexaminant textile, élevage et savoirs pratiques selon les preuves.

### TRS — Transylvania

- **ADD:** 7 — `applied_mineralogy`, `armament_standardization_inspection`, `permanent_engineer_services`, `scientific_fortification_siegecraft`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`
- **REMOVE:** 0 — —
- **REVIEW:** 5 — `organized_forestry`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `traditional_papermaking`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 1 — `codified_practical_knowledge`
- **Diagnostic:** La Transylvanie bénéficie de l'appareil militaire, minier et administratif habsbourgeois; plusieurs capacités sont établies ou sectorielles, tandis que cadastre et codification restent à réexaminer.

### TUR — Turkey

- **ADD:** 9 — `institutionalized_public_credit`, `medical_degrees`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `variolation_networks`
- **REMOVE:** 0 — —
- **REVIEW:** 6 — `armament_standardization_inspection`, `colonization`, `organized_forestry`, `permanent_engineer_services`, `traditional_papermaking`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 3 — `codified_practical_knowledge`, `medical_degrees`, `specialized_technical_academies`
- **Diagnostic:** Capacités impériales très asymétriques mais réelles : arsenaux, artillerie, crédit public (eshām), formation médicale et école navale de 1775 doivent être reconnus sans projeter les réformes du XIXe siècle. Plusieurs chaînes de prérequis restent structurellement inadéquates.

### UZH — Uly Zhuz

- **ADD:** 0 — —
- **REMOVE:** 5 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `codified_practical_knowledge`, `organized_textile_production`, `traditional_food_processing`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 1 — `codified_practical_knowledge`
- **Diagnostic:** Société pastorale/commerciale à capacités propres; le second passage retire les faux standards militaires et administratifs hérités du tier 4 tout en conservant ou réexaminant textile, élevage et savoirs pratiques selon les preuves.

### WAL — Wallachia

- **ADD:** 2 — `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE:** 2 — `selective_breeding`, `standardized_field_artillery`
- **REVIEW:** 4 — `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Le second passage distingue institutions locales, accès à l'appareil ottoman/habsbourgeois et capacités réellement territoriales. Les artisanats traditionnels sont mieux reconnus tandis que plusieurs standards militaires/administratifs restent en REVIEW ou sont retirés.

### ZAI — Azal

- **ADD:** 1 — `traditional_food_processing`
- **REMOVE:** 3 — `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **REVIEW:** 4 — `codified_practical_knowledge`, `light_infantry_tactics`, `regulated_small_arms`, `urbanization`
- **TREE_STRUCTURE_REVIEW:** 2 — `codified_practical_knowledge`, `regulated_small_arms`
- **Diagnostic:** Les armes à feu et les réseaux commerciaux arabiques sont réels, mais ne doivent pas être assimilés à une industrie d'armes réglementaires, à une artillerie standardisée ou à des statistiques d'État. Les métiers traditionnels sont revalorisés lorsqu'ils sont attestés.

## 15. TREE_STRUCTURE_REVIEW

Le second passage compte **94 relations** marquées `TREE_STRUCTURE_REVIEW`. Ce nombre est un nombre de relations TAG × technologie; un même défaut structurel peut donc apparaître dans plusieurs pays. Les cas ne doivent pas être résolus en retirant silencieusement la capacité historique.

- `advanced_crop_rotations` — 1 TAG : `HUN`.

- `atmospheric_engine` — 1 TAG : `HUN`.

- `codified_practical_knowledge` — 47 TAG : `ABB`, `ABU`, `ARB`, `ARM`, `BHN`, `BUK`, `CHC`, `CHT`, `CIR`, `DUR`, `EGY`, `GRE`, `HDJ`, `HER`, `ION`, `IR1`, `JAB`, `JBB`, `KAB`, `KAF`, `KAL`, `KAN`, `KAT`, `KBB`, `KHI`, `KOK`, `KUN`, `KZH`, `LAH`, `MAH`, `MAI`, `MAK`, `MBB`, `MOL`, `MON`, `NBB`, `NEJ`, `OMA`, `OZH`, `PER`, `SER`, `TRM`, `TRS`, `TUR`, `UZH`, `WAL`, `ZAI`.

- `commercial_insurance_markets` — 1 TAG : `ION`.

- `light_infantry_tactics` — 4 TAG : `CIR`, `HER`, `KAB`, `KAN`.

- `medical_degrees` — 2 TAG : `PER`, `TUR`.

- `political_economy` — 1 TAG : `HUN`.

- `regulated_small_arms` — 36 TAG : `ABB`, `ABU`, `ARM`, `BHN`, `CHC`, `CHT`, `CIR`, `DUR`, `EGY`, `GRE`, `HDJ`, `HER`, `IR1`, `JAB`, `JBB`, `KAB`, `KAF`, `KAL`, `KAN`, `KAT`, `KBB`, `KUN`, `LAH`, `MAH`, `MAI`, `MAK`, `MBB`, `MOL`, `MON`, `NBB`, `NEJ`, `OMA`, `PER`, `SER`, `WAL`, `ZAI`.

- `specialized_technical_academies` — 1 TAG : `TUR`.


**Cas de référence HUN — `atmospheric_engine`:** Nová Baňa possède en 1722 une machine atmosphérique de type Newcomen, première du genre en Europe continentale selon les sources slovaques. Le parent `coke_smelting` ne décrit pas une condition historique nécessaire à cette installation. Décision : `ADD`; `Prerequisite_Status = TREE_STRUCTURE_REVIEW`.

## 16. CLASSIFICATION_REVIEW

**196 relations** sont signalées dans le CSV parce que **4 technologies** portent un problème global de classification. Le nombre de relations est 4 × 49; le problème lui-même est technologique, pas national.

- `sugar_refining` — **CLASSIFICATION_TOO_EARLY** : le nœud A débloque notamment vacuum pan et évaporation à vapeur; la vacuum pan de Howard date de 1813.
- `mechanized_weaving` — **CLASSIFICATION_TOO_EARLY** : le power loom de Cartwright est breveté en 1785, après la date de référence.
- `advanced_spinning` — **CLASSIFICATION_TOO_EARLY** : le nœud débloque les machines à coudre, technologie du XIXe siècle (Hunt 1833; Howe 1845–1846).
- `medical_degrees` — **CLASSIFICATION_TOO_LATE** : avec la définition institutionnelle du nœud, des facultés médicales existent bien avant 1776; la capacité ne doit pas être traitée comme une simple frontière tardive.

Aucune technologie C n’a été ajoutée silencieusement; aucune anomalie D supplémentaire n’a été distribuée dans cette région.

## 17. Principales différences avec la première passe

La première passe portait surtout sur les technologies actuellement distribuées et quelques candidats évidents. La seconde passe examine exhaustivement les 61 A/B pour chaque TAG. Les différences majeures sont donc structurelles :

1. les quatre artisanats traditionnels sont désormais dissociés d’`organized_forestry`;
2. la finance publique ottomane (`institutionalized_public_credit`) est reconnue;
3. la médecine institutionnelle est réévaluée selon la définition historique réelle du nœud;
4. HUN reçoit une réévaluation beaucoup plus complète de ses institutions minières, médicales, camérales, forestières et statistiques;
5. l’Asie centrale reçoit davantage d’artisanats mais beaucoup moins de militaires réguliers;
6. `urbanization`, E de compatibilité, passe systématiquement en `REVIEW` plutôt que d’être interprétée comme une capacité historique nationale;
7. des défauts d’arbre sont explicitement conservés au lieu d’ajouter/supprimer des parents pour fermer artificiellement les chaînes;
8. quatre classifications technologiques sont envoyées à l’arbitrage mondial.

Décisions explicitement modifiées sur des relations déjà présentes dans la première matrice (hors `urbanization`) :

- `CIR` `light_infantry_tactics` : REVIEW → **KEEP**.

- `HER` `regulated_small_arms` : KEEP → **REVIEW**.

- `HUN` `specialized_technical_academies` : REVIEW → **ADD**.

- `HUN` `systematic_legal_codification` : KEEP → **REVIEW**.

- `KAB` `regulated_small_arms` : KEEP → **REVIEW**.

- `KAN` `regulated_small_arms` : KEEP → **REVIEW**.

- `KZH` `organized_textile_production` : KEEP → **REVIEW**.

- `OMA` `state_dockyard_systems` : REVIEW → **ADD**.

- `OZH` `organized_textile_production` : KEEP → **REVIEW**.

- `TRM` `organized_textile_production` : KEEP → **REVIEW**.

- `TRS` `systematic_legal_codification` : KEEP → **REVIEW**.

- `UZH` `organized_textile_production` : KEEP → **REVIEW**.

## 18. Recommandations finales

1. Utiliser `CHANGES.csv` comme matrice d’arbitrage/implémentation : il ne contient que les relations non triviales ou historiquement contestables.
2. Utiliser `COVERAGE.csv` pour vérifier l’exhaustivité : chaque A/B doit afficher 49/49 et `YES`.
3. Utiliser `COUNTRIES.csv` pour la lecture par TAG et la priorisation des setups explicites.
4. Ne pas résoudre les `TREE_STRUCTURE_REVIEW` en ajoutant mécaniquement les parents. Traiter la structure de l’arbre lors d’une phase globale dédiée.
5. Traiter les quatre `CLASSIFICATION_REVIEW` mondialement avant toute nouvelle distribution automatique.
6. Pour l’implémentation future, privilégier des setups explicites quand le paquet de tier mélange des domaines historiquement incompatibles.

### 20 changements les plus importants par rapport à la distribution actuellement implémentée

1. **HUN — `atmospheric_engine` → ADD** : Machine atmosphérique à Nová Baňa en 1722; conserver malgré le parent `coke_smelting` non justifié historiquement.

2. **TUR — `institutionalized_public_credit` → ADD** : Le système d’eshām est introduit en 1775 : crédit public institutionnalisé présent à la date de coupure.

3. **TUR — `medical_degrees` → ADD** : Formation médicale institutionnalisée ottomane antérieure à 1776; problème d’arbre avec le parent scientifique.

4. **TUR — `scientific_naval_architecture` → ADD** : Hendesehâne du chantier impérial créée le 29 avril 1775 : capacité FRONTIER mais réelle.

5. **TUR — `state_dockyard_systems` → ADD** : Le Tersâne-i Âmire constitue un véritable système d’arsenal d’État.

6. **PER — `state_dockyard_systems` → REMOVE** : Le projet naval de Nāder Shah ne constitue plus un système durable d’arsenal zand en 1776.

7. **PER — `standardized_field_artillery` → REMOVE** : L’artillerie de campagne zand est insuffisamment standardisée; les zanburaks ne valent pas le nœud.

8. **EGY — `medical_degrees` → REMOVE** : Ne pas projeter les institutions médicales de Muḥammad ʿAlī sur l’Égypte de 1776.

9. **EGY — `specialized_technical_academies` → REMOVE** : Pas d’académie technique comparable au nœud avant les réformes du XIXe siècle.

10. **EGY — `coke_smelting` → REMOVE** : Le paquet industriel du tier 3 est anachronique pour l’Égypte de 1776.

11. **EGY — `applied_mineralogy` → REMOVE** : Mines existantes ≠ minéralogie appliquée institutionnalisée.

12. **BUK — `regulated_small_arms` → REMOVE** : Les corps permanents de sarbāz armés et disciplinés sont surtout une évolution du XIXe siècle.

13. **BUK — `standardized_field_artillery` → REMOVE** : Artillerie régulière standardisée non établie en 1776.

14. **BUK — `traditional_papermaking` → ADD** : Papier de Samarqand/Bukhara et métiers urbains justifient une capacité artisanale sectorielle.

15. **HUN — `medical_degrees` → ADD** : Faculté de médecine de Nagyszombat ouverte en 1770.

16. **HUN — `political_economy` → ADD** : Formation politico-camérale institutionnalisée avant 1776; arbre à revoir.

17. **HUN — `organized_forestry` → ADD** : Règlement forestier général de 1769 et responsables forestiers à partir de 1770.

18. **HUN — `specialized_technical_academies` → ADD** : Académie minière et formations spécialisées établies avant 1776.

19. **IR1 — `state_dockyard_systems` → ADD** : Le chantier de Bassora construit des navires d’État, notamment ordre de deux frégates en 1766.

20. **GRE — `periodical_print_networks` → REMOVE** : Le réseau périodique grec local retenu par l’implémentation est postérieur; Ephimeris est 1791–1797.

## 19. Bibliographie régionale structurée

### Empire ottoman — économie, institutions, marine, médecine

- Şevket Pamuk — Ottoman Empire, 1700–1870: https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/ottoman-empire-17001870/959242AE1899EE1E65604E39DE555F80

- Rhoads Murphey — Westernisation in the eighteenth-century Ottoman Empire: https://www.cambridge.org/core/journals/byzantine-and-modern-greek-studies/article/abs/westernisation-in-the-eighteenthcentury-ottoman-empire-how-far-how-fast/1B61F340FB3AA2A6150F4B92A604909A

- Hendesehâne du Tersâne-i Âmire, 1775: https://dergipark.org.tr/en/pub/iuoba/article/14178

- Eshām — dette publique ottomane: https://islamansiklopedisi.org.tr/esham

- Financial institutions in the Ottoman Empire: https://www.cambridge.org/core/journals/financial-history-review/article/abs/evolution-of-financial-institutions-in-the-ottoman-empire-16001914/DA131E135E305DBE11BA5C0093C24D5E

- Mining registers, 1766–1802: https://dergipark.org.tr/tr/pub/iutarih/article/1139633

- Ottoman copper mines: https://dergipark.org.tr/en/pub/juhis/article/599233

- Ottoman medical education / Süleymaniye: https://pmc.ncbi.nlm.nih.gov/articles/PMC7590537/

- Variolation / smallpox — NLM: https://www.nlm.nih.gov/exhibition/smallpox/sp_variolation.html?lang=en

### Égypte et Irak

- Cambridge History of Egypt — Egypt in the eighteenth century: https://www.cambridge.org/core/books/abs/cambridge-history-of-egypt/egypt-in-the-eighteenth-century/D758288694AE203CDF5A78CD9A5CAE56

- Cambridge History of Egypt — era of Muhammad Ali: https://www.cambridge.org/core/books/abs/cambridge-history-of-egypt/era-of-muhammad-ali-pasha-18051848/68D161C75F9EB1BC63E28C3148AD5DBD

- Library of Congress — Būlāq press context: https://www.loc.gov/collections/arabic-language-rare-materials-collection/about-this-collection/

- Ottoman shipping and Basra shipyard: https://www.cambridge.org/core/journals/international-journal-of-middle-east-studies/article/ottoman-shipping-in-the-indian-ocean-circa-16501900/434125ABA76399828893476152D21D8E

### Perse, Caucase, Afghanistan

- Iranica — Army IV, Afsharid and Zand periods: https://www.iranicaonline.org/articles/army-iv/

- Iranica — Navy I, Nāder Shah: https://www.iranicaonline.org/articles/navy-i-nader-shah/

- Iranica — Firearms I: https://www.iranicaonline.org/articles/firearms-i-history/

- Iranica — Afghanistan XI, Administration: https://www.iranicaonline.org/articles/afghanistan-xi-admin/

- Iranica — Afghanistan X, Political history: https://www.iranicaonline.org/articles/afghanistan-x-political-history/

- Iranica — Armenia: https://www.iranicaonline.org/articles/armenia/

### Asie centrale

- Iranica — Central Asia VII: https://www.iranicaonline.org/articles/central-asia-vii/

- Iranica — Central Asia XI, economy: https://www.iranicaonline.org/articles/central-asia-xi/

- Iranica — Kokand Khanate: https://www.iranicaonline.org/articles/kokand-khanate/

### Arabie et Golfe

- Arabians for Guns — Wahhabi matchlocks and world trade: https://www.cambridge.org/core/journals/journal-of-the-royal-asiatic-society/article/arabians-for-guns-wahhabi-matchlocks-world-trade-and-the-rise-of-the-first-saudi-state/3606B23BB80F31DF6FF46C8ACC0BE651

- Tolerated Terror — Gulf maritime world: https://www.cambridge.org/core/journals/itinerario/article/tolerated-terror-rahmah-bin-jabir-and-the-age-of-revolutions-in-the-gulf-17601830/4C332006F7B0981A66C3728281C458F9

### Balkans et monarchie habsbourgeoise

- Varaždin Studium politico-camerale, 1769–1776: https://hrcak.srce.hr/en/clanak/302415

- Transylvania, cartography and enlightened absolutism: https://www.cambridge.org/core/journals/austrian-history-yearbook/article/abs/putting-transylvania-on-the-map-cartography-and-enlightened-absolutism-in-the-habsburg-monarchy/409D737C58ADAEE026CF4DBC39229CB4

- Carpathian mining/mineralogy: https://real.mtak.hu/12663/1/Kazmer_Papp_1999_Minerals_from_the_Carpathians__Annales.pdf

- Semmelweis University — Nagyszombat medical faculty: https://semmelweis.hu/english/about-semmelweis-university/history/

- National Bank of Slovakia — Nová Baňa atmospheric engine, 1722: https://nbs.sk/en/banknotes-and-coins/euro-coins/commemorative-coins/300th-anniversary-of-the-construction-of-continental-europes-first-atmospheric-steam-engine-for-draining-mines/

- Nová Baňa mining trail — Potter fire engine: https://stolne.novabana.sk/sk/

- Hungarian forestry regulation, 1769: https://mnl.gov.hu/mnl/ol/hirek/az_elso_magyarorszagi_erdorendtartas

- Greek periodical press chronology: https://books.openedition.org/efa/9085

### Révisions globales de classification

- Sugar history — Howard vacuum pan, 1813: https://www.sugar.org/sugar/history/

- Science Museum Group — Cartwright power loom, 1785: https://collection.sciencemuseumgroup.org.uk/people/ap13666/cartwright-edmund

- Metropolitan Museum — power loom chronology: https://www.metmuseum.org/pt/essays/nineteenth-century-european-textile-production

- Smithsonian — Howe sewing machine, 1846: https://www.si.edu/object/nmah_630930

- Smithsonian — Walter Hunt sewing machine, 1833: https://americanhistory.si.edu/collections/object/nmah_1070410

- University of Edinburgh — Faculty of Medicine, 1726: https://medicine-vet-medicine.ed.ac.uk/about/history/medicine

## 20. Contrôle final

- **49/49 TAG audités**
- **25 technologies A auditées**
- **36 technologies B auditées**
- **2 989 relations A/B effectivement examinées**
- **61/61 technologies A/B couvertes**
- **49/49 TAG couverts pour chacune des 61 technologies**
- **ADD : 112**
- **REMOVE : 115**
- **REVIEW : 209**
- **KEEP : 2798**
- **TREE_STRUCTURE_REVIEW : 94 relations**
- **CLASSIFICATION_REVIEW : 196 relations, correspondant à 4 technologies globales**
- **Aucun changement gameplay. Aucun code. Aucun commit. Aucun push.**
