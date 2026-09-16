# Second pass complet — Technologies de départ 1776 — Asie orientale et Asie du Sud-Est

> **Date absolue : 1er janvier 1776. Recherche historique uniquement.** Aucun fichier gameplay n’a été modifié; aucun code Victoria 3, commit ou push n’a été produit.

## 1. Périmètre

Le périmètre comporte **45 TAG**. Sont inclus North China, Northeast Asia, Indochina et Indonesia, avec `TIB` comme cas frontière est-asiatique; `PPU` est exclu conformément à l’exclusion du Pacifique. La première matrice ne contenait effectivement que 40 TAG: cette seconde passe ajoute bien `AIN`, `SKH`, `ULT`, `MND` et `SLW`.

**North China:** `CHI` — China.
**Northeast Asia:** `AIN` — Ainu Mosir, `EZO` — Ezochi, `JAP` — Japan, `KOR` — Korea, `RYU` — Ryukyu, `SKH` — Evenki, `ULT` — Ulta.
**Indochina:** `BUR` — Burma, `CAM` — Cambodia, `CHP` — Champasak, `CMI` — Chiang Mai, `DAI` — Dai Nam, `DGR` — Degar, `JOH` — Johore, `KLO` — Khmer Loeu, `LUA` — Luang Prabang, `PRK` — Perak, `SCT` — Sip Song Chau Tai, `SEL` — Selangor, `SHS` — Shan, `SIA` — Siam.
**Indonesia:** `ACE` — Aceh, `BAL` — Bali, `BLG` — Bulungan, `BNJ` — Banjar, `BRU` — Brunei, `BTN` — Buton, `DEI` — East Indies, `JMB` — Jambi, `KTI` — Kutai, `LAN` — Lanfang, `MGD` — Maguindanao, `MND` — Mindanao, `PHI` — Philippines, `PON` — Pontianak, `SAK` — Siak, `SLW` — Sulawesi, `SMB` — Sambas, `SRK` — Surakarta, `STG` — Sintang, `SUL` — Sulu, `TID` — Tidore, `YOG` — Yogyakarta.
**Himalayas:** `TIB` — Tibet.

## 2. Sources et méthode

La matrice impose une ligne pour chaque **TAG × technologie A/B**: 25 A et 36 B, soit 61 nœuds obligatoires par TAG. Elle ajoute les E à effet direct ou à institution historique identifiable qui ont été réellement examinées, plus `joint_stock_companies` pour DEI. `KEEP` signifie ici **conserver l’état actuel**: pour une ligne `ABSENT`, KEEP signifie donc « rester absent », ce qui est indispensable dans une matrice exhaustive.

Les prérequis sont examinés seulement après le verdict historique. `TREE_STRUCTURE_REVIEW` signale donc une capacité historique réelle dont la chaîne de parents encode une autre trajectoire. `traditional_papermaking`, `traditional_glassmaking` et `traditional_furniture_making` sont explicitement traitées comme découplées de `organized_forestry`, conformément à la nouvelle définition fournie. Le CSV joint conserve encore cet ancien parent dans ses notes: le rapport signale cette divergence sans modifier le fichier.

Sources pivots: JPX/Dojima pour finance japonaise; NDL/MEXT/archives japonaises pour rangaku, éducation et cadastre; KCI/PMC pour Joseon; Oxford/Cambridge et sources Qing pour impression, mines, administration et médecine; Isis pour Ryukyu; Nationaal Archief/Atlas of Mutual Heritage/Utrecht pour la VOC; PARES/Cambridge pour les Philippines; Cambridge/Burma Library pour l’Asie du Sud-Est.

## 3. Production

- **Papier:** la suppression du faux verrou forestier change fortement le résultat. Chine, Japon, Corée, Ryukyu, Tibet et plusieurs traditions continentales d’Asie du Sud-Est reçoivent `traditional_papermaking` lorsqu’une production locale organisée est plausible/attestée.
- **Verre:** `CHI` reçoit `traditional_glassmaking` grâce à la verrerie impériale Qing fondée en 1696; `JAP` est sectoriel. DEI/PHI restent REVIEW faute de preuve suffisante d’une industrie locale comparable.
- **Meuble/alimentation:** plusieurs grands États précédemment bloqués par les tiers reçoivent les nœuds traditionnels sans exiger une sylviculture rationalisée.
- **Acides/sucre:** `industrial_acids` est marqué `CLASSIFICATION_TOO_EARLY` parce que son gameplay débloque une industrie chimique/explosifs intégrée. `sugar_refining` est également trop précoce sous sa forme actuelle: l’existence de raffineries traditionnelles ne justifie pas centrifugeuse, vapeur et vacuum pan.

## 4. Agriculture

L’agriculture intensive chinoise, japonaise et coréenne impose de sortir d’une lecture « révolution agricole britannique = progrès universel ». `improved_agricultural_implements` et surtout `advanced_crop_rotations` sont historiquement établis sous des formes locales anciennes; plusieurs lignes portent `CLASSIFICATION_TOO_LATE`. La dépendance de `advanced_crop_rotations` à `selective_breeding` est un cas net de `TREE_STRUCTURE_REVIEW` en Asie orientale.

Les trois grants actuels `selective_breeding` de `CAM`, `DAI` et `SIA` sont retirés faute de preuve d’un système de sélection animale correspondant réellement au nœud: agriculture avancée ou sériciculture ne suffit pas.

## 5. Mines/métallurgie

Le principal changement est Qing: les sources sur la métallurgie chinoise montrent une trajectoire autonome, avec usage historique du charbon/coke et une sidérurgie sophistiquée. `CHI` reçoit donc `coke_smelting` comme capacité **sectorielle**, avec problème d’arbre si l’ancien parent `organized_forestry` demeure. `shaft_mining` est conservé pour CHI, mais les grants génériques de nombreux petits tier 4 sont retirés ou mis en REVIEW: une mine n’implique pas un puits minier avancé.

## 6. Infrastructure

`organized_forestry` change radicalement de sens dans cette passe. `JAP`, `RYU`, `DEI` et, plus prudemment, `CHI` présentent de vraies institutions/règles d’exploitation forestière organisée. Ryukyu est un cas presque littéral avec Yamabugyōsho, quotas, règlements et afforestation au XVIIIe siècle.

`industrial_canals` est un cas majeur de biais de classification: le réseau du Grand Canal Qing est une infrastructure économique et fiscale mature bien avant 1776. `CHI` reçoit ADD + `CLASSIFICATION_TOO_LATE` + `TREE_STRUCTURE_REVIEW`, puisque les canaux chinois n’ont évidemment pas pour préalable les turnpikes britanniques. Le Japon reçoit une attribution sectorielle pour les réseaux de canaux urbains/commerciaux Edo–Osaka.

## 7. Finance et économie

Le **Japon** est le changement financier majeur. Dojima, officiellement autorisée en **1730**, possède marché au comptant des billets de riz, futures, adhésion et compensation; `stock_exchange` devient ADD/HIGH. Les domaines et le shogunat recourent aussi structurellement aux emprunts marchands et aux titres/recettes fiscales, ce qui justifie `institutionalized_public_credit` en 1776.

Pour **Qing**, commerce et crédit privé sophistiqués ne sont pas confondus avec dette publique institutionnalisée: `institutionalized_public_credit` reste absent. Pour **DEI**, financement corporatif VOC et assurance sont distingués du crédit public souverain et d’un marché local général.

## 8. Commerce

Les puissances maritimes d’Asie du Sud-Est gardent/obtiennent `international_relations` lorsqu’un commerce diplomatique et interétatique structuré est attesté. En revanche, commerce international, compagnie à charte ou grands marchands ne suffisent jamais à produire `stock_exchange`, `commercial_insurance_markets` ou `institutionalized_public_credit`.

## 9. Administration

`systematic_population_registration` est nettement sous-évalué par l’ancienne distribution: ADD pour `CHI`, `JAP`, `KOR` et `PHI`. Qing dispose de registres de ménages/rapports démographiques; Japon d’enquêtes nationales dès 1721; Joseon compile nationalement les registres tous les trois ans; les Philippines disposent d’un ordre de recensement tributaire provincial en 1762.

La codification est également réévaluée hors Europe: `KOR` (Sokdaejeon, 1746) et `DAI` (code Lê/Hồng Đức encore en vigueur au XVIIIe siècle) reçoivent `systematic_legal_codification`.

## 10. Science/éducation

`JAP` conserve `institutionalized_scientific_exchange` grâce au rangaku et au *Kaitai Shinsho* (1774). `CHI` obtient une capacité sectorielle pour les institutions savantes de cour et échanges techniques. L’enseignement primaire organisé est ajouté à `CHI`, `JAP` et `KOR`: écoles communautaires/charitables Qing, terakoya Tokugawa, seodang Joseon. Dans les trois cas, le parent `periodical_print_networks` est historiquement artificiel et déclenche `TREE_STRUCTURE_REVIEW`.

## 11. Médecine

La définition de `medical_degrees` fournie par la consigne change le diagnostic. `CHI` dispose d’une Académie impériale de médecine et de statuts/formation officiels; `KOR` possède un système national de formation et d’examens médicaux (uigwa). Les deux deviennent ADD/HIGH et `CLASSIFICATION_TOO_LATE`. `JAP` reste REVIEW: l’Igakkan existe en 1765, mais les examens officiels documentés sont postérieurs à 1776.

`variolation_networks` devient ADD/HIGH pour `CHI`, où la pratique est codifiée et institutionnellement documentée avant 1776; au Japon elle reste sectorielle et trop peu diffusée pour un réseau national.

## 12. Militaire

La seconde passe supprime de nombreux artefacts du tier 4: `light_infantry_tactics` et `standardized_field_artillery` ne sont plus conservés automatiquement dans de petits sultanats ou Ezochi. La simple possession de fusils/canons ne prouve ni doctrine d’infanterie légère ni standardisation d’artillerie.

À l’inverse, Qing, Joseon, Japon, Burma, Đại Việt, Siam, DEI et Philippines reçoivent/conservent les capacités d’armes/fortification lorsqu’elles sont réellement attestées, avec statut SECTORAL quand la standardisation nationale serait exagérée.

## 13. Marine

Les capacités navales sont concentrées sur les véritables systèmes locaux: DEI et Philippines pour dockyards/fortifications/architecture navale, Qing pour systèmes de chantiers et construction navale sectorielle, Ryukyu pour un appareil de construction/approvisionnement de navires de tribut. `marine_chronometry`, `copper_sheathing` et autres frontières européennes spécialisées restent absentes en 1776 dans la région.

## 14. Analyse pays par pays

### ACE — Aceh

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **ADD A/B:** `traditional_food_processing`
- **REMOVE A/B:** `standardized_field_artillery`
- **REVIEW A/B:** `regulated_small_arms`, `shaft_mining`, `sugar_refining`, `light_infantry_tactics`
- **TREE_STRUCTURE_REVIEW:** `regulated_small_arms`, `artillery`, `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### AIN — Ainu Mosir

Structure politique/économique plus décentralisée ou agrégée: la seconde passe évite de convertir échanges, artisanat domestique ou armes individuelles en institutions nationales A/B.

- **KEEP présents A/B:** —
- **ADD A/B:** —
- **REMOVE A/B:** —
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### BAL — Bali

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **ADD A/B:** `distillation`, `traditional_food_processing`
- **REMOVE A/B:** —
- **REVIEW A/B:** `shaft_mining`, `sugar_refining`
- **TREE_STRUCTURE_REVIEW:** `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### BLG — Bulungan

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### BNJ — Banjar

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### BRU — Brunei

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **ADD A/B:** —
- **REMOVE A/B:** `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `regulated_small_arms`
- **TREE_STRUCTURE_REVIEW:** `regulated_small_arms`, `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### BTN — Buton

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### BUR — Burma

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **ADD A/B:** `regulated_small_arms`, `scientific_fortification_siegecraft`, `distillation`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_papermaking`, `international_relations`
- **REMOVE A/B:** —
- **REVIEW A/B:** `state_dockyard_systems`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`, `improved_agricultural_implements`
- **TREE_STRUCTURE_REVIEW:** `artillery`, `intensive_agriculture`, `centralization`, `law_enforcement`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### CAM — Cambodia

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **ADD A/B:** `distillation`, `traditional_food_processing`, `traditional_papermaking`, `international_relations`
- **REMOVE A/B:** `shaft_mining`, `selective_breeding`
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** `intensive_agriculture`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### CHI — China

Qing est fortement revalorisé en production traditionnelle, agriculture, administration, médecine, hydraulique/canaux et certaines capacités minières/militaires, sans lui importer les trajectoires mécanisées européennes.

- **KEEP présents A/B:** `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`, `systematic_legal_codification`
- **ADD A/B:** `scientific_fortification_siegecraft`, `state_dockyard_systems`, `coke_smelting`, `distillation`, `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `institutionalized_scientific_exchange`, `advanced_crop_rotations`, `improved_agricultural_implements`, `industrial_canals`, `industrial_ceramics`, `medical_degrees`, `organized_elementary_schooling`, `systematic_population_registration`, `variolation_networks`
- **REMOVE A/B:** —
- **REVIEW A/B:** `enclosed_dock_systems`, `scientific_naval_architecture`, `sugar_refining`, `periodical_print_networks`, `military_topographic_surveying`, `permanent_engineer_services`, `permanent_military_hospitals`, `standardized_field_artillery`, `systematic_cadastral_surveying`
- **TREE_STRUCTURE_REVIEW:** `coke_smelting`, `advanced_crop_rotations`, `industrial_canals`, `medical_degrees`, `organized_elementary_schooling`, `intensive_agriculture`, `academia`, `centralization`, `international_trade`, `law_enforcement`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `improved_agricultural_implements:CLASSIFICATION_TOO_LATE`, `industrial_canals:CLASSIFICATION_TOO_LATE`, `industrial_ceramics:CLASSIFICATION_TOO_LATE`, `medical_degrees:CLASSIFICATION_TOO_LATE`, `organized_elementary_schooling:CLASSIFICATION_TOO_LATE`, `systematic_population_registration:CLASSIFICATION_TOO_LATE`

### CHP — Champasak

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### CMI — Chiang Mai

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** `traditional_papermaking`
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### DAI — Dai Nam

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **ADD A/B:** `regulated_small_arms`, `scientific_fortification_siegecraft`, `distillation`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_papermaking`, `international_relations`, `systematic_legal_codification`
- **REMOVE A/B:** `selective_breeding`
- **REVIEW A/B:** `scientific_naval_architecture`, `state_dockyard_systems`, `shaft_mining`, `sugar_refining`, `light_infantry_tactics`, `standardized_field_artillery`, `advanced_crop_rotations`, `improved_agricultural_implements`, `industrial_canals`
- **TREE_STRUCTURE_REVIEW:** `advanced_crop_rotations`, `industrial_canals`, `intensive_agriculture`, `academia`, `centralization`, `international_trade`, `law_enforcement`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`, `systematic_legal_codification:CLASSIFICATION_TOO_LATE`

### DEI — East Indies

La colonie VOC est évaluée localement: ingénierie, dockyards, fortifications et forêt sont réels; finance corporative n’équivaut ni à crédit public local ni au nœud tardif joint_stock_companies.

- **KEEP présents A/B:** `regulated_small_arms`, `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`, `light_infantry_tactics`, `standardized_field_artillery`
- **ADD A/B:** `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`, `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `permanent_engineer_services`
- **REMOVE A/B:** —
- **REVIEW A/B:** `shaft_mining`, `sugar_refining`, `traditional_glassmaking`, `commercial_insurance_markets`, `institutionalized_public_credit`, `periodical_print_networks`, `military_topographic_surveying`, `permanent_military_hospitals`, `systematic_population_registration`
- **TREE_STRUCTURE_REVIEW:** `commercial_insurance_markets`, `centralization`, `international_trade`, `law_enforcement`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### DGR — Degar

Structure politique/économique plus décentralisée ou agrégée: la seconde passe évite de convertir échanges, artisanat domestique ou armes individuelles en institutions nationales A/B.

- **KEEP présents A/B:** `improved_husbandry`
- **ADD A/B:** —
- **REMOVE A/B:** —
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### EZO — Ezochi

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### JAP — Japan

Tokugawa est revalorisé en finance (Dojima/public credit), forêt, éducation, population et cadastre, mais reste volontairement sans technologies Meiji et perd les grants militaires/coloniaux trop génériques.

- **KEEP présents A/B:** `regulated_small_arms`, `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `institutionalized_scientific_exchange`, `international_relations`, `systematic_administrative_statistics`, `systematic_cadastral_surveying`
- **ADD A/B:** `scientific_fortification_siegecraft`, `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `institutionalized_public_credit`, `stock_exchange`, `advanced_crop_rotations`, `improved_agricultural_implements`, `industrial_canals`, `organized_elementary_schooling`, `systematic_population_registration`
- **REMOVE A/B:** `light_infantry_tactics`
- **REVIEW A/B:** `scientific_naval_architecture`, `shaft_mining`, `periodical_print_networks`, `military_topographic_surveying`, `standardized_field_artillery`, `industrial_ceramics`, `medical_degrees`, `systematic_legal_codification`, `variolation_networks`
- **TREE_STRUCTURE_REVIEW:** `scientific_naval_architecture`, `military_topographic_surveying`, `advanced_crop_rotations`, `industrial_canals`, `organized_elementary_schooling`, `gunsmithing`, `military_drill`, `intensive_agriculture`, `academia`, `centralization`, `international_trade`, `law_enforcement`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `improved_agricultural_implements:CLASSIFICATION_TOO_LATE`, `industrial_canals:CLASSIFICATION_TOO_LATE`, `organized_elementary_schooling:CLASSIFICATION_TOO_LATE`, `systematic_cadastral_surveying:CLASSIFICATION_TOO_LATE`, `systematic_population_registration:CLASSIFICATION_TOO_LATE`

### JMB — Jambi

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### JOH — Johore

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **ADD A/B:** `traditional_food_processing`
- **REMOVE A/B:** `shaft_mining`, `standardized_field_artillery`
- **REVIEW A/B:** `regulated_small_arms`, `light_infantry_tactics`
- **TREE_STRUCTURE_REVIEW:** `regulated_small_arms`, `artillery`, `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### KLO — Khmer Loeu

Structure politique/économique plus décentralisée ou agrégée: la seconde passe évite de convertir échanges, artisanat domestique ou armes individuelles en institutions nationales A/B.

- **KEEP présents A/B:** `improved_husbandry`
- **ADD A/B:** —
- **REMOVE A/B:** —
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### KOR — Korea

Joseon est nettement revalorisé en impression, registres, éducation, médecine licenciée, codification, agriculture et armes à feu; l’arbre européen crée plusieurs faux prérequis.

- **KEEP présents A/B:** `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **ADD A/B:** `scientific_fortification_siegecraft`, `distillation`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_papermaking`, `international_relations`, `advanced_crop_rotations`, `improved_agricultural_implements`, `medical_degrees`, `organized_elementary_schooling`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `systematic_population_registration`
- **REMOVE A/B:** —
- **REVIEW A/B:** `shaft_mining`, `periodical_print_networks`, `standardized_field_artillery`, `industrial_ceramics`
- **TREE_STRUCTURE_REVIEW:** `advanced_crop_rotations`, `industrial_ceramics`, `medical_degrees`, `organized_elementary_schooling`, `intensive_agriculture`, `academia`, `centralization`, `international_trade`, `law_enforcement`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `improved_agricultural_implements:CLASSIFICATION_TOO_LATE`, `medical_degrees:CLASSIFICATION_TOO_LATE`, `organized_elementary_schooling:CLASSIFICATION_TOO_LATE`, `systematic_cadastral_surveying:CLASSIFICATION_TOO_LATE`, `systematic_legal_codification:CLASSIFICATION_TOO_LATE`, `systematic_population_registration:CLASSIFICATION_TOO_LATE`

### KTI — Kutai

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### LAN — Lanfang

Cas anachronique: la république de Lanfang n’est fondée qu’en 1777. Tous les grants nationaux présents au 1776-01-01 sont donc retirés; l’anachronisme du TAG doit être arbitré séparément.

- **KEEP présents A/B:** —
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `distillation`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `codified_practical_knowledge`, `institutionalized_scientific_exchange`, `international_relations`, `systematic_administrative_statistics`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### LUA — Luang Prabang

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** `traditional_papermaking`
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### MGD — Maguindanao

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **ADD A/B:** —
- **REMOVE A/B:** `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `regulated_small_arms`
- **TREE_STRUCTURE_REVIEW:** `regulated_small_arms`, `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### MND — Mindanao

Structure politique/économique plus décentralisée ou agrégée: la seconde passe évite de convertir échanges, artisanat domestique ou armes individuelles en institutions nationales A/B.

- **KEEP présents A/B:** —
- **ADD A/B:** —
- **REMOVE A/B:** —
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### PHI — Philippines

Manille/Cavite justifient fortifications, chantiers et recensements coloniaux locaux; le TAG ne reçoit pas automatiquement les institutions de la métropole et perd colonization comme capacité souveraine locale.

- **KEEP présents A/B:** `regulated_small_arms`, `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`, `light_infantry_tactics`, `standardized_field_artillery`
- **ADD A/B:** `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`, `traditional_food_processing`, `traditional_furniture_making`, `systematic_population_registration`
- **REMOVE A/B:** —
- **REVIEW A/B:** `shaft_mining`, `sugar_refining`, `traditional_glassmaking`, `permanent_engineer_services`, `permanent_military_hospitals`
- **TREE_STRUCTURE_REVIEW:** `centralization`, `international_trade`, `law_enforcement`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### PON — Pontianak

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### PRK — Perak

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### RYU — Ryukyu

Ryukyu se distingue par gestion forestière et cadastre extraordinairement institutionnalisés avant 1776; ses grants militaires génériques sont en revanche fortement réduits.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **ADD A/B:** `state_dockyard_systems`, `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_papermaking`, `systematic_cadastral_surveying`
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### SAK — Siak

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### SCT — Sip Song Chau Tai

Structure politique/économique plus décentralisée ou agrégée: la seconde passe évite de convertir échanges, artisanat domestique ou armes individuelles en institutions nationales A/B.

- **KEEP présents A/B:** `improved_husbandry`
- **ADD A/B:** —
- **REMOVE A/B:** —
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### SEL — Selangor

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### SHS — Shan

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** `traditional_papermaking`
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### SIA — Siam

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `improved_husbandry`
- **ADD A/B:** `regulated_small_arms`, `scientific_fortification_siegecraft`, `distillation`, `organized_textile_production`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_papermaking`, `international_relations`, `systematic_administrative_statistics`
- **REMOVE A/B:** `selective_breeding`
- **REVIEW A/B:** `state_dockyard_systems`, `sugar_refining`, `light_infantry_tactics`, `standardized_field_artillery`, `advanced_crop_rotations`, `improved_agricultural_implements`, `industrial_canals`
- **TREE_STRUCTURE_REVIEW:** `advanced_crop_rotations`, `industrial_canals`, `intensive_agriculture`, `centralization`, `international_trade`, `law_enforcement`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### SKH — Evenki

Structure politique/économique plus décentralisée ou agrégée: la seconde passe évite de convertir échanges, artisanat domestique ou armes individuelles en institutions nationales A/B.

- **KEEP présents A/B:** —
- **ADD A/B:** —
- **REMOVE A/B:** —
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### SLW — Sulawesi

Structure politique/économique plus décentralisée ou agrégée: la seconde passe évite de convertir échanges, artisanat domestique ou armes individuelles en institutions nationales A/B.

- **KEEP présents A/B:** —
- **ADD A/B:** —
- **REMOVE A/B:** —
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### SMB — Sambas

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### SRK — Surakarta

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **ADD A/B:** `traditional_food_processing`
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `sugar_refining`
- **TREE_STRUCTURE_REVIEW:** `intensive_agriculture`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### STG — Sintang

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### SUL — Sulu

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **ADD A/B:** —
- **REMOVE A/B:** `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `regulated_small_arms`
- **TREE_STRUCTURE_REVIEW:** `regulated_small_arms`, `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### TIB — Tibet

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `improved_husbandry`
- **ADD A/B:** `distillation`, `traditional_food_processing`, `traditional_papermaking`, `codified_practical_knowledge`, `international_relations`
- **REMOVE A/B:** —
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** `codified_practical_knowledge`, `academia`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### TID — Tidore

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `international_relations`
- **ADD A/B:** —
- **REMOVE A/B:** `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `regulated_small_arms`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **TREE_STRUCTURE_REVIEW:** `regulated_small_arms`, `international_trade`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### ULT — Ulta

Structure politique/économique plus décentralisée ou agrégée: la seconde passe évite de convertir échanges, artisanat domestique ou armes individuelles en institutions nationales A/B.

- **KEEP présents A/B:** —
- **ADD A/B:** —
- **REMOVE A/B:** —
- **REVIEW A/B:** —
- **TREE_STRUCTURE_REVIEW:** —
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

### YOG — Yogyakarta

Le setup est évalué par capacités locales (agriculture/artisanat, commerce, administration, armes) et non par le tier; les technologies spécialisées restent REVIEW/absentes si l’évidence n’atteint pas le niveau institutionnel du nœud.

- **KEEP présents A/B:** `distillation`, `improved_husbandry`, `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **ADD A/B:** `traditional_food_processing`
- **REMOVE A/B:** `regulated_small_arms`, `shaft_mining`, `light_infantry_tactics`, `standardized_field_artillery`
- **REVIEW A/B:** `sugar_refining`
- **TREE_STRUCTURE_REVIEW:** `intensive_agriculture`
- **Classification issues:** `industrial_acids:CLASSIFICATION_TOO_EARLY`, `sugar_refining:CLASSIFICATION_TOO_EARLY`

## 15. TREE_STRUCTURE_REVIEW

Les cas les plus importants sont: `advanced_crop_rotations` en Chine/Japon/Corée sans `selective_breeding`; `industrial_canals` en Chine/Japon sans `turnpike_road_networks`; `medical_degrees` en Chine/Corée sans dépendance nécessaire à l’`institutionalized_scientific_exchange` de type européen; `organized_elementary_schooling` sans `periodical_print_networks`. Ces capacités ne sont pas supprimées pour satisfaire l’arbre.

Le CSV technologies joint conserve encore `organized_forestry` comme parent de papier/verre/meuble. La consigne de seconde passe est prioritaire pour l’interprétation historique: ces trois liens sont explicitement ignorés dans les verdicts et signalés comme divergence technique à réconcilier dans une synthèse ultérieure.

## 16. CLASSIFICATION_REVIEW

**CLASSIFICATION_REVIEW (C réellement pré-1776) : 0.** Aucun nœud C examiné ici ne justifie finalement un reclassement certain: `joint_stock_companies` reste trop large pour être sauvé par la seule existence de la VOC.

En revanche, la matrice contient **90** lignes `CLASSIFICATION_TOO_EARLY` (principalement `industrial_acids` et `sugar_refining`) et **21** lignes `CLASSIFICATION_TOO_LATE`, concentrées sur des capacités asiatiques anciennes que la classification B traitait comme frontières de 1776: registres de population, éducation élémentaire, médecine institutionnelle, rotations culturales, cadastre et canaux.

## 17. Principales différences avec la première passe

1. Passage d’un audit de quelques relations pertinentes à un **cross-product exhaustif des 61 technologies A/B pour chacun des 45 TAG**.
2. Ajout effectif des cinq TAG manquants de l’ancienne matrice (`AIN`, `SKH`, `ULT`, `MND`, `SLW`).
3. Papier/verre/meuble ne sont plus bloqués artificiellement par `organized_forestry`.
4. `organized_forestry` est réinterprété strictement comme gestion/exploitation rationalisée: Ryukyu, Japon et VOC-Java deviennent des cas positifs forts.
5. Finance Tokugawa profondément réévaluée: `stock_exchange` + `institutionalized_public_credit`.
6. Médecine non européenne réévaluée: `medical_degrees` en Chine et Corée, `variolation_networks` en Chine.
7. Infrastructure non européenne réévaluée: `industrial_canals` Qing/Japon et TREE_STRUCTURE_REVIEW face au parent turnpike.
8. `selective_breeding` CAM/DAI/SIA n’est plus accepté sans preuve et est retiré.
9. Les grants militaires tier-4 (`light_infantry_tactics`, `standardized_field_artillery`, parfois `regulated_small_arms`) sont fortement nettoyés.
10. `colonization` n’est plus copié comme propriété du Japon ou des Philippines; la réalité locale de DEI est distinguée de la métropole.

## 18. Recommandations finales

- Ne pas remplacer ces résultats par un nouveau système de tiers. Les résultats sont volontairement asymétriques par domaine.
- Implémenter en priorité les ADD/REMOVE à confiance HIGH, puis arbitrer les REVIEW et les `TREE_STRUCTURE_REVIEW` dans la synthèse mondiale.
- Traiter les `CLASSIFICATION_TOO_EARLY/TOO_LATE` comme questions de conception globale de l’arbre, pas comme prétexte pour fausser une distribution nationale.
- Revoir séparément le problème de date de `LAN` (fondation 1777) et la sémantique locale de colonies comme DEI/PHI.

### Contrôle final

- **TAG étudiés:** 45
- **Technologies A auditées:** 25
- **Technologies B auditées:** 36
- **Lignes totales:** 3736
- **ADD:** 107
- **REMOVE:** 110
- **KEEP:** 3414
- **REVIEW:** 105
- **TREE_STRUCTURE_REVIEW:** 82
- **CLASSIFICATION_REVIEW:** 0
- **CLASSIFICATION_TOO_EARLY:** 90
- **CLASSIFICATION_TOO_LATE:** 21

### 20 changements les plus importants par rapport à la distribution actuelle

1. **JAP — `stock_exchange` — ADD** (HIGH, ESTABLISHED): Dojima est officiellement autorisée en 1730, avec marché au comptant, marché à terme, adhésion et compensation; les billets de riz émis par les domaines sont activement négociés.
2. **JAP — `institutionalized_public_credit` — ADD** (HIGH, ESTABLISHED): Les domaines et le shogunat s’appuient sur emprunts marchands, riz fiscal, billets de riz et dettes; le crédit public est une composante normale des finances des daimyō au milieu du XVIIIe siècle.
3. **DEI — `joint_stock_companies` — REMOVE** (HIGH, ABSTRACT): La VOC est bien une corporation à capital permanent et actions transférables, mais le nœud gameplay généralise compagnies, free charters/laissez-faire et dépend d’institutions financières plus tardives. L’existence de la VOC ne suffit pas à conserver ce nœud à DEI.
4. **CHI — `industrial_canals` — ADD** (HIGH, ESTABLISHED): Le Grand Canal et les réseaux hydrauliques Qing supportent transport fiscal et commercial à très grande échelle; si le nœud signifie une infrastructure de canal économique, la capacité est ancienne.
5. **CHI — `coke_smelting` — ADD** (MEDIUM, SECTORAL): Les sources sur la métallurgie chinoise attestent l’emploi historique du charbon et du coke dans la sidérurgie bien avant l’Europe industrielle; la capacité doit être reconnue comme sectorielle plutôt que filtrée par un schéma Darby-only.
6. **CHI — `medical_degrees` — ADD** (HIGH, ESTABLISHED): L’Académie impériale de médecine Qing comporte médecins classés et étudiants stipendiés; selon la définition du nœud (formation/certification institutionnelle), la capacité est établie.
7. **KOR — `medical_degrees` — ADD** (HIGH, ESTABLISHED): Joseon possède formation médicale institutionnelle et examen national de licence médicale (uigwa) des siècles avant 1776.
8. **CHI — `systematic_population_registration` — ADD** (HIGH, ESTABLISHED): Le Qing utilise enregistrement des ménages, rapports démographiques et réformes baojia avant 1776; la capacité est institutionnalisée à l’échelle impériale.
9. **JAP — `systematic_population_registration` — ADD** (HIGH, ESTABLISHED): Les registres religieux/de population sont anciens et les enquêtes nationales de population commencent en 1721; la capacité est établie avant 1776.
10. **KOR — `systematic_population_registration` — ADD** (HIGH, ESTABLISHED): Joseon compile des registres de ménages à l’échelle nationale tous les trois ans pour fiscalité, corvée et service militaire.
11. **PHI — `systematic_population_registration` — ADD** (HIGH, ESTABLISHED): Le décret royal de 1762 ordonne des recensements de tribut dans toutes les provinces, avec mise en œuvre documentée avant 1776.
12. **CHI — `organized_elementary_schooling` — ADD** (HIGH, ESTABLISHED): Le Qing encourage écoles communautaires/charitables; l’enseignement élémentaire institutionnel existe avant 1776, même si sa couverture varie.
13. **JAP — `organized_elementary_schooling` — ADD** (HIGH, ESTABLISHED): Les terakoya et écoles de domaines sont établies; les écoles de temple deviennent communes parmi les gens du peuple dès la période Genroku.
14. **KOR — `organized_elementary_schooling` — ADD** (HIGH, ESTABLISHED): Les seodang sont des écoles villageoises privées d’enseignement élémentaire bien établies sous Joseon.
15. **JAP — `organized_forestry` — ADD** (HIGH, ESTABLISHED): La réglementation forestière Tokugawa, les magistrats forestiers, les registres, restrictions de coupe et programmes de reboisement correspondent à la nouvelle définition de gestion forestière organisée. 
16. **RYU — `organized_forestry` — ADD** (HIGH, ESTABLISHED): Ryukyu dispose avant 1776 du Yamabugyōsho, de quotas, règlements de 1737 et procédures d’afforestation/administration forestière: cas presque littéral du nœud.
17. **DEI — `organized_forestry` — ADD** (HIGH, SECTORAL): La VOC contrôle et administre des ressources forestières de teck à Java au XVIIIe siècle pour construction et chantiers navals; il s’agit d’une exploitation organisée, pas de simple coupe.
18. **JAP — `colonization` — REMOVE** (HIGH, ABSENT): Le Japon Tokugawa de 1776 ne possède pas le paquet institutionnel de colonisation/exploitation outre-mer du nœud; l’expansion d’Ezo ne suffit pas à justifier les lois coloniales générales.
19. **PHI — `colonization` — REMOVE** (HIGH, ABSENT): Les Philippines sont une colonie espagnole, non une entité locale disposant des institutions souveraines de colonisation débloquées par ce nœud. Ne pas copier la capacité de la métropole.
20. **KOR — `systematic_legal_codification` — ADD** (HIGH, ESTABLISHED): Joseon dispose de codes nationaux et promulgue le Sokdaejeon en 1746; la codification systématique est clairement antérieure à 1776.

**Aucun fichier gameplay modifié. Aucun code Victoria 3. Aucun commit. Aucun push.**
