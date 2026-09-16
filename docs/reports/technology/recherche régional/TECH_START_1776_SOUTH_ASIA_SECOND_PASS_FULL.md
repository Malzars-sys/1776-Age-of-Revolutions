# Recherche technologique — Asie du Sud — SECOND PASS FULL — 1er janvier 1776

> **Recherche uniquement.** Aucun fichier gameplay n’a été modifié, aucun code Victoria 3 n’a été produit, aucun commit/push n’a été effectué. La date de coupure est strictement **1776-01-01**.

## 1. Périmètre

**59 TAG** ont été réaudités : `ALW` (Alwar), `ASM` (Assam), `AWA` (Awadh), `BAG` (Rewah), `BAS` (Bastar), `BCE` (Ceylon), `BER` (Baroda), `BHO` (Bhopal), `BHU` (Bhutan), `BHV` (Bhavnagar), `BHW` (Bahawalpur), `BIC` (East India), `BIK` (Bikaner), `BUN` (Orchha), `COC` (Cochin), `COO` (Cooch Behar), `DHA` (Dharampur), `GAR` (Garhwal), `GWA` (Gwalior), `HYD` (Hyderabad), `IDA` (Idar), `IND` (Indore), `JAI` (Dhundhar), `JAS` (Jaisalmer), `JEY` (Jeypore), `JHN` (Jhansi), `JOD` (Marwar), `JUN` (Junagadh), `KAS` (Kashmir), `KHP` (Kolhapur), `KKI` (Kuki), `KNO` (Kurnool), `KOT` (Kotah), `KUT` (Kutch), `LAD` (Ladakh), `MARATH` (Maratha Confederacy), `MEW` (Mewar), `MGH` (Khasi), `MLD` (Maldives), `MNP` (Manipur), `MUG` (Hindustan), `MYB` (Mayurbhanj), `MYS` (Mysore), `NAG` (Nagpur), `NAR` (Narsinghpur), `NAW` (Nawanagar), `NEP` (Nepal), `NGA` (Naga), `PAN` (Punjab), `PLP` (Palanpur), `PTA` (Patiala), `PTN` (Patna), `PUD` (Pudukottai), `SAT` (Satara), `SIK` (Sikkim), `SIN` (Sindh), `SUR` (Surguja), `TIP` (Tipperah), `TRA` (Travancore).

Le périmètre conserve Hindustan/Moghol, Marathes, Mysore, Awadh/Bengale sous administration locale de BIC, Hyderabad, Punjab/Sikh, Rajputana, principautés, Népal, Bhoutan, Ceylan et les compagnies centrées localement dans le sous-continent. Afghanistan, Birmanie, Malaisie et DEI restent exclus. `TIB` n’est pas repris : son centre politique relève de l’audit tibétain/himalayen extérieur plutôt que du sous-continent au sens de ce lot.

## 2. Sources et méthode

La matrice repart de zéro sur les capacités historiques : le statut actuellement implémenté sert uniquement à déterminer `PRESENT/ABSENT`, jamais à prouver une capacité. Les **25 technologies A** et **36 technologies B** du CSV technique sont évaluées pour chacun des 59 TAG, soit **3 599 relations obligatoires**. S’ajoutent les nœuds E à effet direct (`field_works`, `colonization`, `urbanization`, `multilateral_alliances`, `political_agitation`), l’alias fusées de Mysore, et des C soumis à révision (`cotton_gin`, `standardized_military_rockets`, plus `joint_stock_companies` pour documenter le cas des compagnies).

Principe : 1) déterminer la capacité historique indépendamment de l’arbre ; 2) seulement ensuite contrôler les prérequis ; 3) signaler les divergences via `TREE_STRUCTURE_REVIEW` ; 4) signaler les classifications chronologiques douteuses sans forcer une technologie C dans le setup.

Sources structurantes : Cambridge Economic History of India pour économie/agriculture/manufactures ; K. N. Chaudhuri et travaux sur les textiles pour la proto-industrie ; études Cambridge sur finance moghole/marathe ; PMC pour variolisation et services médicaux de la Compagnie ; travaux navals sur Bombay, Mysore et Marathes ; sources UNESCO/institutionnelles pour Jaipur et Ceylan. Chaque ligne CSV conserve les URL complètes.

## 3. Production

La seconde passe sépare nettement artisanat avancé et industrialisation. L’Inde de 1776 est un centre mondial de production textile manuelle/proto-industrielle ; cela justifie `organized_textile_production` dans de nombreux centres, mais **pas** `mechanized_spinning`, `mechanized_weaving` ou `advanced_spinning`. Papier, verre et meuble sont désormais évalués indépendamment de `organized_forestry`.

- `organized_textile_production` — ADD: — ; REMOVE: `ALW`, `BAG`, `BAS`, `BCE`, `BHO`, `BHU`, `BIK`, `BUN`, `DHA`, `GAR`, `IDA`, `JAS` (+12) ; REVIEW: —.
- `traditional_papermaking` — ADD: `ALW`, `ASM`, `AWA`, `BER`, `BHU`, `BHV`, `BIC`, `GWA`, `IND`, `JUN`, `KOT`, `KUT` (+3) ; REMOVE: `BCE` ; REVIEW: —.
- `traditional_glassmaking` — ADD: `AWA`, `BIC`, `MUG`, `PTN` ; REMOVE: — ; REVIEW: `HYD`, `JAI`.
- `traditional_furniture_making` — ADD: `AWA`, `BCE`, `BER`, `BIC`, `GWA`, `HYD`, `IND`, `JAI`, `JOD`, `KAS`, `MARATH`, `MEW` (+5) ; REMOVE: — ; REVIEW: —.
- `traditional_food_processing` — ADD: `ALW`, `ASM`, `BAG`, `BAS`, `BER`, `BHO`, `BHU`, `BHV`, `BHW`, `BIK`, `BUN`, `COO` (+35) ; REMOVE: — ; REVIEW: `KKI`, `MGH`, `NGA`, `TIP`.
- `distillation` — ADD: `BAG`, `COC`, `COO`, `MARATH`, `MUG`, `NAG`, `NEP` ; REMOVE: — ; REVIEW: `KKI`, `MGH`, `NGA`, `TIP`.
- `sugar_refining` — ADD: — ; REMOVE: — ; REVIEW: `ALW`, `ASM`, `AWA`, `BAG`, `BAS`, `BCE`, `BER`, `BHO`, `BHU`, `BHV` (+49).

`sugar_refining` reçoit **CLASSIFICATION_TOO_EARLY** : son nom pourrait évoquer un artisanat ancien, mais le nœud débloque notamment vacuum pan, évaporation vapeur et centrifugation. Le vacuum pan de Howard date de **1813** ; le nœud A ne doit donc pas servir à représenter le simple raffinage traditionnel.

## 4. Agriculture

Les sources sur l’agriculture moghole décrivent seed-drill, irrigation et rotations culturales. `improved_husbandry` reste une abstraction agricole de base largement plausible. `improved_agricultural_implements` demeure REVIEW dans les grands espaces agrariens car l’existence d’outils avancés ne correspond pas nécessairement au PM global. En revanche, `advanced_crop_rotations` est historiquement antérieure à 1776 dans une part importante du sous-continent et reçoit **CLASSIFICATION_TOO_LATE** dans les cas retenus.

- `improved_husbandry` — ADD: — ; REMOVE: — ; REVIEW: —.
- `improved_agricultural_implements` — ADD: — ; REMOVE: — ; REVIEW: `ASM`, `AWA`, `BIC`, `GWA`, `HYD`, `IND`, `JAI`, `MARATH`, `MEW`, `MUG` (+5).
- `advanced_crop_rotations` — ADD: `ASM`, `AWA`, `BER`, `BIC`, `COC`, `GWA`, `HYD`, `IND`, `JAI`, `JOD`, `KOT`, `MARATH` (+9) ; REMOVE: — ; REVIEW: —.
- `selective_breeding` — ADD: — ; REMOVE: — ; REVIEW: `BIK`, `JOD`, `MARATH`, `MYS`, `PAN`, `PTA`.

## 5. Mines/métallurgie

L’audit distingue désormais strictement **métallurgie sophistiquée** et **filière industrielle au coke**. Le wootz/crucible steel ne justifie pas `coke_smelting`. Les mines de Zawar soutiennent `shaft_mining`/`applied_mineralogy` au Mewar ; à BIC, Raniganj commence commercialement en 1774 et reste un cas sectoriel. Aucune pompe `atmospheric_engine` locale n’est accordée.

- `shaft_mining` — ADD: — ; REMOVE: `ASM`, `BAS`, `HYD`, `KAS`, `KUT`, `LAD`, `MARATH`, `MYS`, `NAG`, `SIN` ; REVIEW: —.
- `applied_mineralogy` — ADD: `MEW` ; REMOVE: — ; REVIEW: `BIC`, `MYS`.
- `coke_smelting` — ADD: — ; REMOVE: — ; REVIEW: —.
- `atmospheric_engine` — ADD: — ; REMOVE: — ; REVIEW: —.
- `precision_boring` — ADD: — ; REMOVE: — ; REVIEW: —.

## 6. Infrastructure

`organized_forestry` utilise la **nouvelle définition : sylviculture/exploitation rationalisée**. La coupe de bois ordinaire n’est plus une preuve. Résultat : aucune attribution positive dans le lot, et l’ancien grant de Ceylan est retiré. Routes impériales, péages et irrigation ne sont pas convertis mécaniquement en `turnpike_road_networks` ou `industrial_canals`.

- `organized_forestry` — ADD: — ; REMOVE: `BCE` ; REVIEW: —.
- `turnpike_road_networks` — ADD: — ; REMOVE: — ; REVIEW: `BIC`, `MUG`.
- `industrial_canals` — ADD: — ; REMOVE: — ; REVIEW: —.

## 7. Finance et économie

C’est l’une des plus fortes corrections. Les réseaux de banquiers, hundis, avances fiscales et prêts au souverain justifient `institutionalized_public_credit` dans plusieurs grands États. Les Marathes sont particulièrement nets : des collecteurs avançaient une fraction des recettes au Peshwa et empruntaient sur le marché de Poona. À l’inverse, **aucune bourse organisée** n’est attribuée : `stock_exchange` reste distinct du crédit public et des maisons de banque.

- `institutionalized_public_credit` — ADD: `AWA`, `BER`, `BIC`, `HYD`, `MARATH`, `MUG` ; REMOVE: — ; REVIEW: `GWA`, `IND`, `KUT`, `SIN`.
- `commercial_insurance_markets` — ADD: `BER`, `BIC`, `KUT`, `MARATH`, `MUG`, `SIN` ; REMOVE: — ; REVIEW: `AWA`, `BHV`, `GWA`, `HYD`, `IND`, `JUN`, `NAW`.
- `stock_exchange` — ADD: — ; REMOVE: — ; REVIEW: —.
- `political_economy` — ADD: — ; REMOVE: — ; REVIEW: —.
- `classical_political_economy` — ADD: — ; REMOVE: — ; REVIEW: —.

## 8. Commerce

`international_relations` est évalué comme capacité régulière de diplomatie/traités et non comme simple souveraineté. Les marchés d’assurance sont attribués seulement là où les réseaux marchands/financiers permettent de défendre une véritable capacité de couverture du risque. Le fait qu’une compagnie soit juridiquement une joint-stock company ne suffit toujours pas à donner le nœud C `joint_stock_companies` à son territoire indien.

## 9. Administration

Les anciens tiers avaient trop diffusé `systematic_administrative_statistics` et `codified_practical_knowledge`. Cette passe les réserve aux appareils fiscaux et documentaires suffisamment solides. Deux révisions de classification sont majeures pour le Moghol : le système de revenu mesuré/zabt rend `systematic_cadastral_surveying` historiquement précoce, et la tradition de compilation juridique impériale rend `systematic_legal_codification` trop tardive comme B si le nœud est interprété génériquement.

- `systematic_administrative_statistics` — ADD: `BCE` ; REMOVE: `ALW`, `BAG`, `BAS`, `BHO`, `BHU`, `BHV`, `BHW`, `BIK`, `BUN`, `COC`, `COO`, `DHA` (+23) ; REVIEW: —.
- `codified_practical_knowledge` — ADD: `BCE` ; REMOVE: `ALW`, `BAG`, `BAS`, `BHO`, `BHU`, `BHV`, `BHW`, `BIK`, `BUN`, `COC`, `COO`, `DHA` (+23) ; REVIEW: —.
- `systematic_population_registration` — ADD: — ; REMOVE: — ; REVIEW: —.
- `systematic_cadastral_surveying` — ADD: `MUG` ; REMOVE: — ; REVIEW: `AWA`, `BIC`, `HYD`, `MARATH`.
- `systematic_legal_codification` — ADD: `MUG` ; REMOVE: — ; REVIEW: `AWA`, `BIC`, `HYD`.

## 10. Science/éducation

`periodical_print_networks` est absent partout : une presse ou des presses missionnaires ne constituent pas un réseau périodique, et le premier journal imprimé en Inde apparaît en **1780**. Jaipur constitue en revanche un cas positif pour `institutionalized_scientific_exchange` grâce à son dispositif astronomique et aux échanges de traditions scientifiques. `organized_elementary_schooling` reste REVIEW dans les grands États : l’existence d’écoles indigènes ne suffit pas à démontrer une institution nationale correspondant au nœud.

- `institutionalized_scientific_exchange` — ADD: `JAI` ; REMOVE: — ; REVIEW: `HYD`, `MUG`, `MYS`.
- `periodical_print_networks` — ADD: — ; REMOVE: — ; REVIEW: —.
- `specialized_technical_academies` — ADD: — ; REMOVE: — ; REVIEW: —.
- `organized_elementary_schooling` — ADD: — ; REMOVE: — ; REVIEW: `AWA`, `BCE`, `BIC`, `HYD`, `JAI`, `MARATH`, `MUG`, `MYS`, `NEP`, `PAN` (+1).

## 11. Médecine

La variolisation est réévaluée nettement à la hausse : Holwell décrit en 1767 des inoculateurs itinérants au Bengale, et les synthèses médicales la donnent comme pratique largement connue en Inde. BIC obtient aussi `permanent_military_hospitals` et `medical_degrees` au sens fonctionnel défini par la consigne : services médicaux de Bengal (1764) et Madras (1767), hiérarchie et nomination de chirurgiens, hôpitaux militaires permanents. Il ne s’agit pas de projeter le Calcutta Medical College de 1835 en arrière.

- `variolation_networks` — ADD: `AWA`, `BER`, `BHV`, `BIC`, `JUN`, `KUT`, `MARATH`, `MUG`, `NAW`, `PTN`, `SIN` ; REMOVE: — ; REVIEW: `BCE`, `COC`, `HYD`, `JAI`, `MYS`, `PAN`, `TRA`.
- `medical_degrees` — ADD: `BIC` ; REMOVE: — ; REVIEW: `AWA`, `BCE`, `HYD`, `MUG`.
- `veterinary_science` — ADD: — ; REMOVE: — ; REVIEW: —.

## 12. Militaire

Les grands États ne reçoivent plus automatiquement tout le paquet militaire. `regulated_small_arms` exige des arsenaux/production organisée ; `standardized_field_artillery` exige davantage que la possession de canons ; les corps permanents d’ingénieurs et hôpitaux sont étudiés séparément. BIC est le cas le plus institutionnalisé : établissement régulier d’ingénieurs à Madras dès 1718, Corps organisé militairement en 1770, services médicaux avant 1776. Mysore conserve ses capacités sous Haidar Ali mais aucune innovation de Tipu postérieure n’est importée.

- `regulated_small_arms` — ADD: `MARATH` ; REMOVE: `ASM`, `BER`, `BHO`, `BHW`, `GWA`, `IND`, `KAS`, `KHP`, `MEW`, `MNP`, `PTA`, `SAT` (+1) ; REVIEW: `MUG`, `PAN`, `TRA`.
- `light_infantry_tactics` — ADD: — ; REMOVE: — ; REVIEW: `HYD`, `MARATH`.
- `standardized_field_artillery` — ADD: — ; REMOVE: — ; REVIEW: `MARATH`, `MUG`, `PAN`.
- `permanent_engineer_services` — ADD: `BIC` ; REMOVE: — ; REVIEW: `BCE`, `MYS`, `TRA`.
- `permanent_military_hospitals` — ADD: `BCE`, `BIC` ; REMOVE: — ; REVIEW: —.
- `military_topographic_surveying` — ADD: — ; REMOVE: — ; REVIEW: `MYS`.

### Fusées de Mysore

La tradition de fusées sous Haidar Ali est bien antérieure à 1776, mais la standardisation et les performances les mieux documentées appartiennent surtout aux guerres des années 1780–1790. `standardized_military_rockets` (C) est donc **CLASSIFICATION_REVIEW** et reste `REVIEW`, pas ADD. L’alias E `mysorean_iron_cased_rocketry` reste lui aussi REVIEW et n’est pas utilisé pour contourner l’arbre.

## 13. Marine

Les capacités navales sont fortement concentrées. BIC et Ceylan conservent des infrastructures de dockyard localement déployées. La tradition navale marathe justifie `state_dockyard_systems` sans donner automatiquement docks fermés/chronométrie. Mysore reçoit `state_dockyard_systems` comme capacité sectorielle sous Haidar Ali ; `scientific_naval_architecture` y reste REVIEW. `copper_sheathing` n’est attribué à personne.

- `state_dockyard_systems` — ADD: `MYS` ; REMOVE: — ; REVIEW: `COC`, `TRA`.
- `enclosed_dock_systems` — ADD: — ; REMOVE: — ; REVIEW: `COC`.
- `scientific_naval_architecture` — ADD: `BCE`, `BIC` ; REMOVE: — ; REVIEW: `MARATH`, `MYS`.
- `ship_classification_surveying` — ADD: — ; REMOVE: — ; REVIEW: `BCE`, `BIC`.
- `marine_chronometry` — ADD: — ; REMOVE: — ; REVIEW: `BCE`, `BIC`.
- `copper_sheathing` — ADD: — ; REMOVE: — ; REVIEW: —.

## 14. Analyse pays par pays

### ALW — Alwar
- **Sous-région :** Rajputana
- **ADD (2) :** `traditional_food_processing`, `traditional_papermaking`
- **REMOVE (3) :** `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### ASM — Assam
- **Sous-région :** Northeast & eastern uplands
- **ADD (3) :** `traditional_food_processing`, `traditional_papermaking`, `advanced_crop_rotations`
- **REMOVE (2) :** `shaft_mining`, `regulated_small_arms`
- **REVIEW (3) :** `sugar_refining`, `improved_agricultural_implements`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (3) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### AWA — Awadh
- **Sous-région :** Gangetic Plain & Bengal
- **ADD (6) :** `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `advanced_crop_rotations`, `institutionalized_public_credit`, `variolation_networks`
- **REMOVE (0) :** —
- **REVIEW (9) :** `sugar_refining`, `improved_agricultural_implements`, `industrial_ceramics`, `cotton_gin`, `commercial_insurance_markets`, `medical_degrees`, `organized_elementary_schooling`, `systematic_cadastral_surveying`, `systematic_legal_codification`
- **TREE_STRUCTURE_REVIEW (5) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`, `medical_degrees`, `organized_elementary_schooling`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### BAG — Rewah
- **Sous-région :** Central India
- **ADD (2) :** `distillation`, `traditional_food_processing`
- **REMOVE (3) :** `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### BAS — Bastar
- **Sous-région :** Central India
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `shaft_mining`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### BCE — Ceylon
- **Sous-région :** Indian Ocean islands
- **ADD (7) :** `traditional_furniture_making`, `scientific_naval_architecture`, `permanent_military_hospitals`, `codified_practical_knowledge`, `systematic_administrative_statistics`, `colonization`, `urbanization`
- **REMOVE (3) :** `organized_forestry`, `organized_textile_production`, `traditional_papermaking`
- **REVIEW (7) :** `sugar_refining`, `marine_chronometry`, `permanent_engineer_services`, `ship_classification_surveying`, `medical_degrees`, `organized_elementary_schooling`, `variolation_networks`
- **TREE_STRUCTURE_REVIEW (3) :** `codified_practical_knowledge`, `organized_elementary_schooling`, `joint_stock_companies`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** les capacités doivent rester celles effectivement déployées dans la Ceylan néerlandaise; la nouvelle définition de `organized_forestry` entraîne son retrait malgré l’existence évidente de coupe de bois.

### BER — Baroda
- **Sous-région :** Gujarat & Kathiawar
- **ADD (7) :** `traditional_food_processing`, `traditional_furniture_making`, `traditional_papermaking`, `advanced_crop_rotations`, `commercial_insurance_markets`, `institutionalized_public_credit`, `variolation_networks`
- **REMOVE (1) :** `regulated_small_arms`
- **REVIEW (2) :** `sugar_refining`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (3) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### BHO — Bhopal
- **Sous-région :** Central India
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `regulated_small_arms`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### BHU — Bhutan
- **Sous-région :** Himalayas
- **ADD (2) :** `traditional_food_processing`, `traditional_papermaking`
- **REMOVE (3) :** `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### BHV — Bhavnagar
- **Sous-région :** Gujarat & Kathiawar
- **ADD (3) :** `traditional_food_processing`, `traditional_papermaking`, `variolation_networks`
- **REMOVE (2) :** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (3) :** `sugar_refining`, `cotton_gin`, `commercial_insurance_markets`
- **TREE_STRUCTURE_REVIEW (2) :** `cotton_gin`, `commercial_insurance_markets`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### BHW — Bahawalpur
- **Sous-région :** Punjab & Indus
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (3) :** `regulated_small_arms`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (2) :** `sugar_refining`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (1) :** `cotton_gin`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### BIC — East India
- **Sous-région :** Gangetic Plain & Bengal
- **ADD (11) :** `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `advanced_crop_rotations`, `scientific_naval_architecture`, `permanent_engineer_services`, `permanent_military_hospitals`, `commercial_insurance_markets`, `institutionalized_public_credit`, `medical_degrees`, `variolation_networks`
- **REMOVE (0) :** —
- **REVIEW (12) :** `sugar_refining`, `applied_mineralogy`, `improved_agricultural_implements`, `turnpike_road_networks`, `cotton_gin`, `armament_standardization_inspection`, `marine_chronometry`, `ship_classification_surveying`, `organized_elementary_schooling`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `multilateral_alliances`
- **TREE_STRUCTURE_REVIEW (6) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`, `organized_elementary_schooling`, `multilateral_alliances`, `joint_stock_companies`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** administration fiscale et militaire de Compagnie très institutionnalisée localement; médecine, ingénieurs, dockyards et topographie sont de vrais points forts. Ne pas importer automatiquement toutes les capacités britanniques métropolitaines.

### BIK — Bikaner
- **Sous-région :** Rajputana
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (3) :** `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (2) :** `sugar_refining`, `selective_breeding`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### BUN — Orchha
- **Sous-région :** Central India
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### COC — Cochin
- **Sous-région :** Malabar & Travancore
- **ADD (3) :** `distillation`, `advanced_crop_rotations`, `international_relations`
- **REMOVE (2) :** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (5) :** `sugar_refining`, `cotton_gin`, `enclosed_dock_systems`, `state_dockyard_systems`, `variolation_networks`
- **TREE_STRUCTURE_REVIEW (2) :** `advanced_crop_rotations`, `cotton_gin`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### COO — Cooch Behar
- **Sous-région :** Gangetic Plain & Bengal
- **ADD (2) :** `distillation`, `traditional_food_processing`
- **REMOVE (2) :** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (2) :** `sugar_refining`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (1) :** `cotton_gin`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### DHA — Dharampur
- **Sous-région :** Gujarat & Kathiawar
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### GAR — Garhwal
- **Sous-région :** Gangetic Plain & Bengal
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (3) :** `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### GWA — Gwalior
- **Sous-région :** Central India
- **ADD (4) :** `traditional_food_processing`, `traditional_furniture_making`, `traditional_papermaking`, `advanced_crop_rotations`
- **REMOVE (1) :** `regulated_small_arms`
- **REVIEW (6) :** `sugar_refining`, `improved_agricultural_implements`, `cotton_gin`, `scientific_fortification_siegecraft`, `commercial_insurance_markets`, `institutionalized_public_credit`
- **TREE_STRUCTURE_REVIEW (4) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`, `commercial_insurance_markets`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### HYD — Hyderabad
- **Sous-région :** Deccan & Mysore
- **ADD (3) :** `traditional_furniture_making`, `advanced_crop_rotations`, `institutionalized_public_credit`
- **REMOVE (1) :** `shaft_mining`
- **REVIEW (14) :** `sugar_refining`, `traditional_glassmaking`, `improved_agricultural_implements`, `industrial_ceramics`, `cotton_gin`, `light_infantry_tactics`, `commercial_insurance_markets`, `institutionalized_scientific_exchange`, `medical_degrees`, `organized_elementary_schooling`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `variolation_networks`, `multilateral_alliances`
- **TREE_STRUCTURE_REVIEW (7) :** `advanced_crop_rotations`, `industrial_ceramics`, `cotton_gin`, `codified_practical_knowledge`, `medical_degrees`, `organized_elementary_schooling`, `multilateral_alliances`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### IDA — Idar
- **Sous-région :** Gujarat & Kathiawar
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### IND — Indore
- **Sous-région :** Central India
- **ADD (4) :** `traditional_food_processing`, `traditional_furniture_making`, `traditional_papermaking`, `advanced_crop_rotations`
- **REMOVE (1) :** `regulated_small_arms`
- **REVIEW (5) :** `sugar_refining`, `improved_agricultural_implements`, `cotton_gin`, `commercial_insurance_markets`, `institutionalized_public_credit`
- **TREE_STRUCTURE_REVIEW (4) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`, `commercial_insurance_markets`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### JAI — Dhundhar
- **Sous-région :** Rajputana
- **ADD (4) :** `traditional_food_processing`, `traditional_furniture_making`, `advanced_crop_rotations`, `institutionalized_scientific_exchange`
- **REMOVE (0) :** —
- **REVIEW (8) :** `sugar_refining`, `traditional_glassmaking`, `improved_agricultural_implements`, `industrial_ceramics`, `cotton_gin`, `scientific_fortification_siegecraft`, `organized_elementary_schooling`, `variolation_networks`
- **TREE_STRUCTURE_REVIEW (5) :** `advanced_crop_rotations`, `industrial_ceramics`, `cotton_gin`, `codified_practical_knowledge`, `organized_elementary_schooling`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### JAS — Jaisalmer
- **Sous-région :** Rajputana
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### JEY — Jeypore
- **Sous-région :** Northeast & eastern uplands
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### JHN — Jhansi
- **Sous-région :** Central India
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### JOD — Marwar
- **Sous-région :** Rajputana
- **ADD (3) :** `traditional_food_processing`, `traditional_furniture_making`, `advanced_crop_rotations`
- **REMOVE (2) :** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (3) :** `sugar_refining`, `selective_breeding`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (2) :** `advanced_crop_rotations`, `cotton_gin`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### JUN — Junagadh
- **Sous-région :** Gujarat & Kathiawar
- **ADD (3) :** `traditional_food_processing`, `traditional_papermaking`, `variolation_networks`
- **REMOVE (2) :** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (3) :** `sugar_refining`, `cotton_gin`, `commercial_insurance_markets`
- **TREE_STRUCTURE_REVIEW (2) :** `cotton_gin`, `commercial_insurance_markets`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### KAS — Kashmir
- **Sous-région :** Himalayas
- **ADD (2) :** `traditional_food_processing`, `traditional_furniture_making`
- **REMOVE (2) :** `shaft_mining`, `regulated_small_arms`
- **REVIEW (2) :** `sugar_refining`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (2) :** `cotton_gin`, `codified_practical_knowledge`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### KHP — Kolhapur
- **Sous-région :** Deccan & Mysore
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (3) :** `regulated_small_arms`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (2) :** `sugar_refining`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (1) :** `cotton_gin`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### KKI — Kuki
- **Sous-région :** Northeast & eastern uplands
- **ADD (0) :** —
- **REMOVE (0) :** —
- **REVIEW (3) :** `distillation`, `sugar_refining`, `traditional_food_processing`
- **TREE_STRUCTURE_REVIEW (1) :** `sugar_refining`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** petite société montagnarde/décentralisée : les anciens effets génériques surestiment fortement urbanisation, bureaucratie et manufactures institutionnalisées.

### KNO — Kurnool
- **Sous-région :** Deccan & Mysore
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### KOT — Kotah
- **Sous-région :** Rajputana
- **ADD (3) :** `traditional_food_processing`, `traditional_papermaking`, `advanced_crop_rotations`
- **REMOVE (3) :** `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (2) :** `sugar_refining`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (2) :** `advanced_crop_rotations`, `cotton_gin`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### KUT — Kutch
- **Sous-région :** Gujarat & Kathiawar
- **ADD (4) :** `traditional_food_processing`, `traditional_papermaking`, `commercial_insurance_markets`, `variolation_networks`
- **REMOVE (3) :** `shaft_mining`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (3) :** `sugar_refining`, `cotton_gin`, `institutionalized_public_credit`
- **TREE_STRUCTURE_REVIEW (2) :** `cotton_gin`, `commercial_insurance_markets`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### LAD — Ladakh
- **Sous-région :** Himalayas
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `shaft_mining`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### MARATH — Maratha Confederacy
- **Sous-région :** Deccan & Mysore
- **ADD (7) :** `distillation`, `traditional_furniture_making`, `advanced_crop_rotations`, `regulated_small_arms`, `commercial_insurance_markets`, `institutionalized_public_credit`, `variolation_networks`
- **REMOVE (1) :** `shaft_mining`
- **REVIEW (10) :** `sugar_refining`, `improved_agricultural_implements`, `selective_breeding`, `cotton_gin`, `scientific_naval_architecture`, `light_infantry_tactics`, `standardized_field_artillery`, `organized_elementary_schooling`, `systematic_cadastral_surveying`, `multilateral_alliances`
- **TREE_STRUCTURE_REVIEW (5) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`, `organized_elementary_schooling`, `multilateral_alliances`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** combinaison particulière de finance publique/marché du crédit, administration fiscale, armée et tradition navale; ne pas confondre cette force avec une industrialisation mécanique.

### MEW — Mewar
- **Sous-région :** Rajputana
- **ADD (4) :** `traditional_food_processing`, `traditional_furniture_making`, `advanced_crop_rotations`, `applied_mineralogy`
- **REMOVE (1) :** `regulated_small_arms`
- **REVIEW (4) :** `sugar_refining`, `improved_agricultural_implements`, `cotton_gin`, `scientific_fortification_siegecraft`
- **TREE_STRUCTURE_REVIEW (3) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### MGH — Khasi
- **Sous-région :** Northeast & eastern uplands
- **ADD (0) :** —
- **REMOVE (0) :** —
- **REVIEW (3) :** `distillation`, `sugar_refining`, `traditional_food_processing`
- **TREE_STRUCTURE_REVIEW (1) :** `sugar_refining`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** petite société montagnarde/décentralisée : les anciens effets génériques surestiment fortement urbanisation, bureaucratie et manufactures institutionnalisées.

### MLD — Maldives
- **Sous-région :** Indian Ocean islands
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (3) :** `organized_textile_production`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### MNP — Manipur
- **Sous-région :** Northeast & eastern uplands
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (3) :** `regulated_small_arms`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (2) :** `sugar_refining`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (1) :** `cotton_gin`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### MUG — Hindustan
- **Sous-région :** Gangetic Plain & Bengal
- **ADD (9) :** `distillation`, `traditional_furniture_making`, `traditional_glassmaking`, `advanced_crop_rotations`, `commercial_insurance_markets`, `institutionalized_public_credit`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `variolation_networks`
- **REMOVE (0) :** —
- **REVIEW (12) :** `sugar_refining`, `improved_agricultural_implements`, `industrial_ceramics`, `turnpike_road_networks`, `cotton_gin`, `regulated_small_arms`, `scientific_fortification_siegecraft`, `standardized_field_artillery`, `institutionalized_scientific_exchange`, `medical_degrees`, `organized_elementary_schooling`, `multilateral_alliances`
- **TREE_STRUCTURE_REVIEW (8) :** `advanced_crop_rotations`, `cotton_gin`, `regulated_small_arms`, `standardized_field_artillery`, `codified_practical_knowledge`, `medical_degrees`, `organized_elementary_schooling`, `multilateral_alliances`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`, `systematic_cadastral_surveying:CLASSIFICATION_TOO_LATE`, `systematic_legal_codification:CLASSIFICATION_TOO_LATE`
- **Diagnostic :** l’héritage moghol reste très fort en fiscalité, crédit, papier, textiles, droit et mesure foncière; il ne doit cependant pas être propagé automatiquement aux États successeurs.

### MYB — Mayurbhanj
- **Sous-région :** Northeast & eastern uplands
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### MYS — Mysore
- **Sous-région :** Deccan & Mysore
- **ADD (3) :** `traditional_furniture_making`, `advanced_crop_rotations`, `state_dockyard_systems`
- **REMOVE (1) :** `shaft_mining`
- **REVIEW (15) :** `sugar_refining`, `applied_mineralogy`, `improved_agricultural_implements`, `selective_breeding`, `cotton_gin`, `scientific_naval_architecture`, `armament_standardization_inspection`, `military_topographic_surveying`, `permanent_engineer_services`, `mysorean_iron_cased_rocketry`, `standardized_military_rockets`, `institutionalized_scientific_exchange`, `organized_elementary_schooling`, `variolation_networks`, `multilateral_alliances`
- **TREE_STRUCTURE_REVIEW (8) :** `advanced_crop_rotations`, `applied_mineralogy`, `cotton_gin`, `military_topographic_surveying`, `standardized_military_rockets`, `codified_practical_knowledge`, `organized_elementary_schooling`, `multilateral_alliances`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`, `standardized_military_rockets:CLASSIFICATION_REVIEW`
- **Diagnostic :** armée sous Haidar déjà réformée et artillerie/armes organisées; effort naval réel mais sectoriel; fusées pré-1776 attestées sans importer les perfectionnements de Tipu des années 1780–1790.

### NAG — Nagpur
- **Sous-région :** Deccan & Mysore
- **ADD (4) :** `distillation`, `traditional_food_processing`, `advanced_crop_rotations`, `international_relations`
- **REMOVE (1) :** `shaft_mining`
- **REVIEW (2) :** `sugar_refining`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (3) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### NAR — Narsinghpur
- **Sous-région :** Central India
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### NAW — Nawanagar
- **Sous-région :** Gujarat & Kathiawar
- **ADD (3) :** `traditional_food_processing`, `traditional_papermaking`, `variolation_networks`
- **REMOVE (2) :** `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (3) :** `sugar_refining`, `cotton_gin`, `commercial_insurance_markets`
- **TREE_STRUCTURE_REVIEW (2) :** `cotton_gin`, `commercial_insurance_markets`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### NEP — Nepal
- **Sous-région :** Himalayas
- **ADD (4) :** `distillation`, `traditional_food_processing`, `traditional_papermaking`, `advanced_crop_rotations`
- **REMOVE (1) :** `organized_textile_production`
- **REVIEW (2) :** `sugar_refining`, `organized_elementary_schooling`
- **TREE_STRUCTURE_REVIEW (3) :** `advanced_crop_rotations`, `codified_practical_knowledge`, `organized_elementary_schooling`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### NGA — Naga
- **Sous-région :** Northeast & eastern uplands
- **ADD (0) :** —
- **REMOVE (0) :** —
- **REVIEW (3) :** `distillation`, `sugar_refining`, `traditional_food_processing`
- **TREE_STRUCTURE_REVIEW (1) :** `sugar_refining`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** petite société montagnarde/décentralisée : les anciens effets génériques surestiment fortement urbanisation, bureaucratie et manufactures institutionnalisées.

### PAN — Punjab
- **Sous-région :** Punjab & Indus
- **ADD (3) :** `traditional_food_processing`, `traditional_furniture_making`, `advanced_crop_rotations`
- **REMOVE (0) :** —
- **REVIEW (9) :** `sugar_refining`, `improved_agricultural_implements`, `selective_breeding`, `cotton_gin`, `regulated_small_arms`, `scientific_fortification_siegecraft`, `standardized_field_artillery`, `organized_elementary_schooling`, `variolation_networks`
- **TREE_STRUCTURE_REVIEW (6) :** `advanced_crop_rotations`, `cotton_gin`, `regulated_small_arms`, `standardized_field_artillery`, `codified_practical_knowledge`, `organized_elementary_schooling`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### PLP — Palanpur
- **Sous-région :** Gujarat & Kathiawar
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### PTA — Patiala
- **Sous-région :** Punjab & Indus
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `regulated_small_arms`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (2) :** `sugar_refining`, `selective_breeding`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### PTN — Patna
- **Sous-région :** Gangetic Plain & Bengal
- **ADD (6) :** `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `advanced_crop_rotations`, `variolation_networks`
- **REMOVE (0) :** —
- **REVIEW (3) :** `sugar_refining`, `improved_agricultural_implements`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (3) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### PUD — Pudukottai
- **Sous-région :** Deccan & Mysore
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (3) :** `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (2) :** `sugar_refining`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (1) :** `cotton_gin`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### SAT — Satara
- **Sous-région :** Deccan & Mysore
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (3) :** `regulated_small_arms`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **REVIEW (2) :** `sugar_refining`, `cotton_gin`
- **TREE_STRUCTURE_REVIEW (1) :** `cotton_gin`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### SIK — Sikkim
- **Sous-région :** Himalayas
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### SIN — Sindh
- **Sous-région :** Punjab & Indus
- **ADD (4) :** `traditional_food_processing`, `advanced_crop_rotations`, `commercial_insurance_markets`, `variolation_networks`
- **REMOVE (2) :** `shaft_mining`, `regulated_small_arms`
- **REVIEW (4) :** `sugar_refining`, `improved_agricultural_implements`, `cotton_gin`, `institutionalized_public_credit`
- **TREE_STRUCTURE_REVIEW (4) :** `advanced_crop_rotations`, `cotton_gin`, `codified_practical_knowledge`, `commercial_insurance_markets`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### SUR — Surguja
- **Sous-région :** Central India
- **ADD (1) :** `traditional_food_processing`
- **REMOVE (4) :** `organized_textile_production`, `codified_practical_knowledge`, `international_relations`, `systematic_administrative_statistics`
- **REVIEW (1) :** `sugar_refining`
- **TREE_STRUCTURE_REVIEW (0) :** —
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

### TIP — Tipperah
- **Sous-région :** Northeast & eastern uplands
- **ADD (0) :** —
- **REMOVE (1) :** `urbanization`
- **REVIEW (3) :** `distillation`, `sugar_refining`, `traditional_food_processing`
- **TREE_STRUCTURE_REVIEW (1) :** `sugar_refining`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`
- **Diagnostic :** petite société montagnarde/décentralisée : les anciens effets génériques surestiment fortement urbanisation, bureaucratie et manufactures institutionnalisées.

### TRA — Travancore
- **Sous-région :** Malabar & Travancore
- **ADD (3) :** `traditional_food_processing`, `traditional_furniture_making`, `advanced_crop_rotations`
- **REMOVE (0) :** —
- **REVIEW (8) :** `sugar_refining`, `improved_agricultural_implements`, `cotton_gin`, `regulated_small_arms`, `state_dockyard_systems`, `permanent_engineer_services`, `organized_elementary_schooling`, `variolation_networks`
- **TREE_STRUCTURE_REVIEW (6) :** `advanced_crop_rotations`, `cotton_gin`, `light_infantry_tactics`, `standardized_field_artillery`, `codified_practical_knowledge`, `organized_elementary_schooling`
- **Classification :** `sugar_refining:CLASSIFICATION_TOO_EARLY`, `advanced_crop_rotations:CLASSIFICATION_TOO_LATE`, `cotton_gin:CLASSIFICATION_REVIEW`
- **Diagnostic :** setup traité asymétriquement par domaine; les suppressions visent surtout les paquets administratifs/militaires des tiers génériques et les ajouts les savoir-faire artisanaux, agricoles ou financiers réellement documentés.

## 15. TREE_STRUCTURE_REVIEW

**115 relations** sont signalées. Les plus structurantes sont :

- `advanced_crop_rotations` peut être historiquement justifié alors que `selective_breeding` ne l’est pas : la rotation des cultures indienne n’a pas besoin de suivre ce chemin d’arbre.
- `cotton_gin` dépend de `mechanized_spinning`, alors que le churka/charki indien à rouleaux est antérieur à la filature mécanisée : divergence nette de filiation technologique.
- `medical_degrees` à BIC peut être justifié par les services/certifications médicales de Compagnie alors que `institutionalized_scientific_exchange` n’est pas toujours le meilleur parent causal.
- `systematic_cadastral_surveying` moghol est historiquement ancien et ne doit pas être nié parce que le nœud administratif parent est une abstraction différente.
- Les technologies de fusées de Mysore suivent dans l’arbre une chaîne explosive/inspection postérieure qui ne reproduit pas la trajectoire locale.

## 16. CLASSIFICATION_REVIEW

- **CLASSIFICATION_REVIEW : 32 lignes.** Elles concernent principalement `cotton_gin` dans les régions cotonnières et `standardized_military_rockets` à Mysore.
- **CLASSIFICATION_TOO_EARLY : 59 lignes.** `sugar_refining` est le cas systémique : le contenu gameplay réel inclut des procédés du XIXe siècle.
- **CLASSIFICATION_TOO_LATE : 23 lignes.** Principalement `advanced_crop_rotations`, plus les capacités cadastrales/juridiques mogholes.

## 17. Principales différences avec la première passe

La première passe régionale avait surtout corrigé les grants arbitraires des tiers. La seconde passe est plus profonde : elle réintroduit des capacités fondamentales que l’ancienne logique de prérequis ou de comparaison eurocentrée avait sous-évaluées, et elle retire certains faux positifs qui avaient survécu parce qu’un tier était pratique à implémenter.

### 20 changements les plus importants par rapport à la distribution actuellement implémentée

| # | TAG | Pays | Technologie | Changement | Pourquoi |
|---:|---|---|---|---|---|
| 1 | `BIC` | East India | `institutionalized_public_credit` | ABSENT → **ADD** | Les réseaux de banquiers, avances fiscales et crédit politique documentés dans l'économie successorale indienne justifient la capacité fondamentale de crédit public/commercial organisé, sans impliquer une bourse moderne. |
| 2 | `MUG` | Hindustan | `institutionalized_public_credit` | ABSENT → **ADD** | Les grandes maisons bancaires indigènes fournissaient fonds de roulement et crédit à l'État moghol et à ses agents, finançaient campagnes et karkhanas et opéraient le réseau des hundis: la capacité est institutionnalisée avant 1776. |
| 3 | `BIC` | East India | `permanent_military_hospitals` | ABSENT → **ADD** | Le dispositif médical militaire de Madras est centralisé autour d'un General Hospital en 1760, avec plusieurs hôpitaux de garnison et services médicaux de présidence avant 1776: capacité permanente établie. |
| 4 | `BIC` | East India | `permanent_engineer_services` | ABSENT → **ADD** | Un établissement régulier d'ingénieurs existe à Madras depuis 1718 et le Corps of Madras Engineers est organisé sur une base strictement militaire en 1770: capacité permanente clairement établie. |
| 5 | `MARATH` | Maratha Confederacy | `institutionalized_public_credit` | ABSENT → **ADD** | Le système marathe reposait sur avances de recettes au Peshwa, emprunts des collecteurs sur le marché monétaire de Poona et maisons bancaires au service de l'État: crédit public institutionnalisé au sens fonctionnel du nœud. |
| 6 | `BIC` | East India | `medical_degrees` | ABSENT → **ADD** | La Compagnie dispose avant 1776 de services médicaux institutionnalisés: Bengal Medical Service dès 1764, Madras en 1767, avec nomination et hiérarchie de chirurgiens. Le nœud est interprété comme certification/formation institutionnelle et non comme faculté du XIXe siècle. |
| 7 | `MUG` | Hindustan | `systematic_legal_codification` | ABSENT → **ADD** | L'État moghol dispose bien avant 1776 de grandes compilations juridiques impériales (dont la tradition de la Fatawa-i Alamgiri); le nœud B est trop tardif s'il représente la codification juridique systématique en général. |
| 8 | `AWA` | Awadh | `institutionalized_public_credit` | ABSENT → **ADD** | Les réseaux de banquiers, avances fiscales et crédit politique documentés dans l'économie successorale indienne justifient la capacité fondamentale de crédit public/commercial organisé, sans impliquer une bourse moderne. |
| 9 | `HYD` | Hyderabad | `institutionalized_public_credit` | ABSENT → **ADD** | Les réseaux de banquiers, avances fiscales et crédit politique documentés dans l'économie successorale indienne justifient la capacité fondamentale de crédit public/commercial organisé, sans impliquer une bourse moderne. |
| 10 | `MUG` | Hindustan | `systematic_cadastral_surveying` | ABSENT → **ADD** | Le système zabt et l'administration du revenu reposaient de longue date sur mesure, assiette et barèmes territoriaux systématiques; le nœud B paraît trop tardif pour cette capacité administrative préexistante. |
| 11 | `BIC` | East India | `advanced_crop_rotations` | ABSENT → **ADD** | Les sources décrivent en Inde précoloniale la rotation des cultures et la connaissance de cultures préparant/enrichissant les sols. La capacité est antérieure à 1776; le classement B paraît trop tardif, même si le parent selective_breeding ne décrit pas le même chemin historique. |
| 12 | `BCE` | Ceylon | `permanent_military_hospitals` | ABSENT → **ADD** | Des soins de campagne ad hoc ne suffisent pas; le nœud exige des hôpitaux/services militaires permanents documentés. |
| 13 | `BER` | Baroda | `institutionalized_public_credit` | ABSENT → **ADD** | Les réseaux de banquiers, avances fiscales et crédit politique documentés dans l'économie successorale indienne justifient la capacité fondamentale de crédit public/commercial organisé, sans impliquer une bourse moderne. |
| 14 | `BIC` | East India | `commercial_insurance_markets` | ABSENT → **ADD** | Les réseaux marchands indiens utilisaient des mécanismes d'assurance/prime sur marchandises et fonds en transit et des instruments hundi; cela justifie une capacité de marché d'assurance commerciale, sans présumer les compagnies d'assurance corporatives des années 1780. |
| 15 | `MUG` | Hindustan | `advanced_crop_rotations` | ABSENT → **ADD** | Les sources décrivent en Inde précoloniale la rotation des cultures et la connaissance de cultures préparant/enrichissant les sols. La capacité est antérieure à 1776; le classement B paraît trop tardif, même si le parent selective_breeding ne décrit pas le même chemin historique. |
| 16 | `MUG` | Hindustan | `commercial_insurance_markets` | ABSENT → **ADD** | Les réseaux marchands indiens utilisaient des mécanismes d'assurance/prime sur marchandises et fonds en transit et des instruments hundi; cela justifie une capacité de marché d'assurance commerciale, sans présumer les compagnies d'assurance corporatives des années 1780. |
| 17 | `MYS` | Mysore | `advanced_crop_rotations` | ABSENT → **ADD** | Les sources décrivent en Inde précoloniale la rotation des cultures et la connaissance de cultures préparant/enrichissant les sols. La capacité est antérieure à 1776; le classement B paraît trop tardif, même si le parent selective_breeding ne décrit pas le même chemin historique. |
| 18 | `MARATH` | Maratha Confederacy | `advanced_crop_rotations` | ABSENT → **ADD** | Les sources décrivent en Inde précoloniale la rotation des cultures et la connaissance de cultures préparant/enrichissant les sols. La capacité est antérieure à 1776; le classement B paraît trop tardif, même si le parent selective_breeding ne décrit pas le même chemin historique. |
| 19 | `BIC` | East India | `traditional_papermaking` | ABSENT → **ADD** | La fabrication artisanale du papier est attestée dans plusieurs centres indiens bien avant 1776; Sanganer/Jaipur en est un exemple documenté. Elle est évaluée indépendamment de organized_forestry conformément au nouvel arbre. |
| 20 | `MARATH` | Maratha Confederacy | `commercial_insurance_markets` | ABSENT → **ADD** | Les réseaux marchands indiens utilisaient des mécanismes d'assurance/prime sur marchandises et fonds en transit et des instruments hundi; cela justifie une capacité de marché d'assurance commerciale, sans présumer les compagnies d'assurance corporatives des années 1780. |

Les différences les plus structurantes sont donc : crédit public/assurance indigènes réévalués à la hausse; médecine et ingénieurs BIC renforcés; papier/verre/meuble libérés du faux verrou forestier; rotations culturales et gin de coton reconnus comme capacités pré-industrielles; `organized_forestry` resserré; paquets militaires/administratifs génériques encore réduits là où les institutions ne sont pas démontrées.

## 18. Recommandations finales

- Utiliser la matrice CSV comme **nouvelle base de recherche**, pas comme patch automatique : les `REVIEW` et `CLASSIFICATION_*` doivent être arbitrés lors de la synthèse mondiale.
- Ne pas fermer automatiquement les prérequis. Toute ligne `TREE_STRUCTURE_REVIEW` indique précisément que l’arbre doit être dissocié de la question historique.
- Revoir mondialement `sugar_refining`, `advanced_crop_rotations`, `cotton_gin`, et la paire cadastral/codification afin d’éviter une chronologie implicitement européenne.
- Pour les compagnies européennes, conserver le principe local : BIC/BCE obtiennent seulement les capacités effectivement déployées dans les présidences, forts, hôpitaux, services et dockyards régionaux.
- Mysore : ne pas importer les innovations documentées surtout sous Tipu; garder la frontière 1776 explicite.
- Marathes : préserver l’asymétrie finance + administration fiscale + naval/militaire sans les faire basculer vers la mécanisation industrielle.
- Moghol/Hindustan : conserver ses propres institutions historiques sans les recopier automatiquement aux États successeurs.

### Contrôle final

- TAG : **59**
- Technologies A auditées : **25**
- Technologies B auditées : **36**
- Lignes totales : **3929** (dont E=296, C=34)
- ADD : **152**
- REMOVE : **134**
- KEEP : **3436**
- REVIEW : **207**
- TREE_STRUCTURE_REVIEW : **115**
- CLASSIFICATION_REVIEW : **32**
- CLASSIFICATION_TOO_EARLY : **59**
- CLASSIFICATION_TOO_LATE : **23**

**Aucun fichier gameplay modifié. Aucun code Victoria 3. Aucun commit. Aucun push.**
