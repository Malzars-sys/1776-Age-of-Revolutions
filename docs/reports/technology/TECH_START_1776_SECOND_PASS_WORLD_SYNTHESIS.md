# TECH START 1776 — Synthèse mondiale du second passage

Date de synthèse : 13 septembre 2026  
Cible historique : **1776-01-01**  
Cible technique : Victoria 3 **1.13.11**  
Statut : **audit et plan uniquement — aucune implémentation gameplay**.

## 1. Méthodologie

Les huit matrices FULL et le couple CHANGES/COVERAGE du Moyen-Orient ont été normalisés. `Local_Current_Status` a été recalculé depuis le working tree chargé (paliers plus grants explicites), sans reprendre aveuglément les snapshots régionaux. ADD/REMOVE fixent directement la cible historique; KEEP conserve le sens présent/absent du baseline régional. Les REVIEW ont été arbitrés à partir du statut historique, de la confiance, du motif, des sources, du seuil gameplay et d’une comparaison mondiale. La cible reste volontairement **non fermée** par les prérequis.

## 2. Couverture mondiale

- 9 régions chargées; 471 TAG recherchés uniques; aucune intersection régionale.
- 25 technologies A et 36 technologies B, soit 61 technologies.
- **28 731 relations A/B uniques** (471 × 61).
- Format Moyen-Orient : 49 TAG × 61 = 2 989 relations, dont 637 lignes explicites et 2 352 KEEP reconstruits grâce au COVERAGE certifié; **0 SOURCE_FORMAT_GAP**.
- Décisions brutes : KEEP 22,559, ADD 1,672, REMOVE 2,882, REVIEW 1,618.

## 3. État des 471 TAG

La cible historique contient **3,696 relations pays-technologie** sur les technologies effectivement retenues dans le plan pays, contre 2,573 dans le working tree pour les 471 TAG. Le delta brut est de **1,913 ADD** et **790 REMOVE**. Les prérequis ne sont pas ajoutés artificiellement : 26 relations structurelles distinctes restent à examiner.

## 4. GAL, MLT et PPU

Ces trois TAG sont inscrits `RESEARCH_GAP` et `PRESERVE_CURRENT_PENDING_RESEARCH`. Leur état local est conservé sans décision historique inventée; ils ne figurent pas dans les 28 731 relations synthétisées.

## 5. Résultats A

Les A ont été traitées comme capacités potentiellement largement pré-1776, mais jamais comme grants automatiques. Les corrections les plus importantes concernent les manufactures traditionnelles, le crédit public, la médecine institutionnelle, la variolisation et la suppression des dépendances forestières artificielles.

## 6. Résultats B

Les B restent sélectives. Les capacités réellement anciennes (cadastre, enregistrement, médecine, rotations, écoles, génie) peuvent être présentes, tandis que les nœuds dont le contenu principal est postérieur au cutoff restent absents ou bloqués par une décision de classification.

## 7. Technologies E retenues

Les nœuds E ne sont pas propagés automatiquement. `colonization` et les rares E à effet gameplay sont conservés seulement lorsque la matrice les justifie. `urbanization` est traité comme alias vide; `multilateral_alliances` et `political_agitation` représentent des paquets modernes et restent absents. `mysorean_iron_cased_rocketry` demeure non résolu pour MYS.

- `colonization` : 34 relations → PRESENT.
- `multilateral_alliances` : 412 relations → ABSENT.
- `mysorean_iron_cased_rocketry` : 1 relations → UNRESOLVED.
- `political_agitation` : 412 relations → ABSENT.
- `urbanization` : 422 relations → ABSENT.

## 8. Arbitrage des REVIEW

- REVIEW → PRESENT : **359**.
- REVIEW → ABSENT : **1,253**.
- REVIEW → UNRESOLVED : **6**.

Le seuil adopté distingue une capacité institutionnelle/productive établie d’un simple savoir artisanal, d’une expérience isolée ou d’une analogie abstraite. Les seuls cas A/B laissés ouverts sont ceux où les sources confirment une institution ou une pratique, mais pas sa continuité exacte au cutoff ou son équivalence avec le nœud.

## 9. Production et artisanat

Papier et verre sont évalués selon l’existence d’une production locale, non selon l’accès à `organized_forestry`. Le meuble reste un nœud manufacturier : le simple travail du bois ne suffit pas. Le textile organisé et la transformation alimentaire exigent une échelle d’atelier défendable.

## 10. Agriculture

Les systèmes non européens ne sont pas mesurés à l’aune de la seule révolution agricole britannique. `advanced_crop_rotations` peut être historiquement présent sans `selective_breeding`; cette arête est une révision structurelle prioritaire.

## 11. Mines et métallurgie

`shaft_mining` exige des travaux souterrains structurés et non la seule métallurgie. `coke_smelting` reste rare. La nouvelle dépendance `coke_smelting → shaft_mining` est plus cohérente que l’ancienne dépendance forestière.

## 12. Infrastructure

`industrial_canals` est reconnu comme capacité mondiale préindustrielle dans plusieurs régions. Sa dépendance à `turnpike_road_networks` reste artificielle; la cible historique ne rajoute pas les turnpikes pour la fermer.

## 13. Finance

Le crédit public est distingué du crédit privé et de la simple fiscalité. TUR est positif grâce à l’eshām de 1775. Les grandes places européennes sont comparées sur les institutions effectives : dette publique, assurance et marché organisé de titres ne sont pas fusionnés en un seul indicateur.

## 14. Commerce

`international_relations` représente une capacité diplomatique/commerciale structurée. Une compagnie, une foire ou un port actif ne suffit pas automatiquement à justifier assurance commerciale, crédit public et bourse.

## 15. Administration

Statistiques, enregistrement de population, cadastre et codification juridique sont séparés. Les administrations fiscales ou coutumières ne sont pas converties automatiquement en systèmes statistiques modernes.

## 16. Science et éducation

`codified_practical_knowledge` reste historiquement plus large que ses deux parents actuels. Les savoirs codifiés peuvent circuler par manuscrits, ateliers, écoles et archives sans presse périodique ni réseau savant institutionnalisé simultané.

## 17. Médecine

`medical_degrees` est interprété comme facultés, collèges, examens, titres ou certifications reconnues — pas comme diplôme médical moderne. La synthèse recommande une classe A sélective. FRA est positive dans la cible; cinq cas de continuité/certification au cutoff restent ouverts. Les réseaux de variolisation sont évalués séparément.

## 18. Militaire terrestre

L’usage d’armes importées ne suffit pas à `regulated_small_arms`, mais une industrie d’arsenal attestée ne doit pas dépendre artificiellement de la fortification scientifique. Artillerie standardisée, génie, hôpitaux et topographie gardent des seuils institutionnels distincts.

## 19. Marine

Arsenaux d’État, bassins fermés, architecture navale scientifique, chronométrie et classification des navires ne sont pas déduits de la seule navigation. Les puissances maritimes sont comparées par capacité précise.

## 20. Problèmes d’arbre

| Technologie | Problème | Pays affectés | Recommandation |
|---|---|---:|---|
| `codified_practical_knowledge → periodical_print_networks` | OVERBROAD_PREREQUISITE | 77 | REPLACE_EDGE : imprimerie/archives ou branche OU |
| `codified_practical_knowledge → institutionalized_scientific_exchange` | OVERBROAD_PREREQUISITE | 66 | REPLACE_EDGE : parent alternatif ou branche OU |
| `light_infantry_tactics → regulated_small_arms` | MISSING_PREREQUISITE | 49 | RESEARCH_NEEDED : — |
| `advanced_crop_rotations → selective_breeding` | ARTIFICIAL_PREREQUISITE | 32 | REMOVE_EDGE : improved_husbandry |
| `regulated_small_arms → scientific_fortification_siegecraft` | ARTIFICIAL_PREREQUISITE | 24 | REMOVE_EDGE : — |
| `standardized_field_artillery → regulated_small_arms` | MISSING_PREREQUISITE | 24 | RESEARCH_NEEDED : — |
| `medical_degrees → institutionalized_scientific_exchange` | OVERBROAD_PREREQUISITE | 13 | REPLACE_EDGE : parent éducatif/médical plus ancien |
| `political_economy → commercial_insurance_markets` | MISSING_PREREQUISITE | 10 | RESEARCH_NEEDED : — |
| `commercial_insurance_markets → institutionalized_public_credit` | MISSING_PREREQUISITE | 9 | RESEARCH_NEEDED : — |
| `industrial_canals → turnpike_road_networks` | ARTIFICIAL_PREREQUISITE | 8 | REPLACE_EDGE : hydraulic engineering / improved waterways |
| `traditional_furniture_making → organized_textile_production` | ARTIFICIAL_PREREQUISITE | 8 | REPLACE_EDGE : parent artisanal général; conserver le nœud connecté |
| `atmospheric_engine → coke_smelting` | ARTIFICIAL_PREREQUISITE | 7 | REPLACE_EDGE : shaft_mining |
| `organized_elementary_schooling → periodical_print_networks` | OVERBROAD_PREREQUISITE | 7 | REPLACE_EDGE : codified_practical_knowledge ou parent éducatif |
| `permanent_engineer_services → scientific_fortification_siegecraft` | MISSING_PREREQUISITE | 5 | RESEARCH_NEEDED : — |
| `scientific_naval_architecture → state_dockyard_systems` | MISSING_PREREQUISITE | 5 | RESEARCH_NEEDED : — |
| `sugar_refining → traditional_food_processing` | MISSING_PREREQUISITE | 4 | RESEARCH_NEEDED : — |
| `applied_mineralogy → shaft_mining` | MISSING_PREREQUISITE | 3 | RESEARCH_NEEDED : — |
| `industrial_ceramics → traditional_glassmaking` | MISSING_PREREQUISITE | 2 | RESEARCH_NEEDED : — |
| `permanent_military_hospitals → scientific_fortification_siegecraft` | MISSING_PREREQUISITE | 2 | RESEARCH_NEEDED : — |
| `commercial_insurance_markets → international_relations` | MISSING_PREREQUISITE | 1 | RESEARCH_NEEDED : — |

Les anciennes alertes `traditional_papermaking/glassmaking/furniture_making → organized_forestry` sont marquées `RESOLVED_BY_CURRENT_TREE`. `traditional_furniture_making` n’est pas isolée : elle possède actuellement `organized_textile_production` comme parent, mais cette liaison sémantique reste à améliorer sans recréer un nœud orphelin.

## 21. Problèmes de classification

| Technologie | Classe actuelle | Action proposée | Motif |
|---|---|---|---|
| `advanced_crop_rotations` | B | RECLASSIFY → A sélective | CLASSIFICATION_TOO_LATE |
| `advanced_spinning` | B | MOVE_UNLOCKS → B pour la filature avancée; D pour les machines à coudre | MIXED_CONCEPT |
| `casemated_fortifications` | C | RECLASSIFY → B/C sélective | CLASSIFICATION_REVIEW |
| `classical_political_economy` | B | RECLASSIFY → C ou scission doctrinale | CLASSIFICATION_TOO_EARLY |
| `clinicopathological_medicine` | C | KEEP_CLASS → C | CLASSIFICATION_REVIEW |
| `condensing_steam_engines` | B | RECLASSIFY → C | CLASSIFICATION_TOO_EARLY |
| `constitutional_government` | B | RECLASSIFY → A/B sélective | CLASSIFICATION_TOO_LATE |
| `cotton_gin` | C | KEEP_CLASS → C | CLASSIFICATION_REVIEW |
| `crystal_glass` | C | RECLASSIFY → B/C sélective | CLASSIFICATION_REVIEW |
| `hydraulic_cements` | C | KEEP_CLASS → C | CLASSIFICATION_REVIEW |
| `hydrographic_surveying` | C | KEEP_CLASS → C | CLASSIFICATION_REVIEW |
| `improved_agricultural_implements` | B | RECLASSIFY → A/B sélective | CLASSIFICATION_TOO_LATE |
| `industrial_acids` | A | SPLIT_TECH → A/B pour les acides historiques; déplacer l’industrie chimique/explosifs intégrée | MIXED_CONCEPT |
| `industrial_canals` | B | REDEFINE_TECH → B, mais définition mondiale préindustrielle | CLASSIFICATION_TOO_LATE |
| `industrial_ceramics` | B | RECLASSIFY → A/B sélective | CLASSIFICATION_TOO_LATE |
| `mechanized_weaving` | B | RECLASSIFY → C | CLASSIFICATION_TOO_EARLY |
| `medical_degrees` | B | RECLASSIFY → A sélective | CLASSIFICATION_TOO_LATE |
| `military_veterinary_services` | C | RECLASSIFY → B sélective | CLASSIFICATION_REVIEW |
| `organized_elementary_schooling` | B | RECLASSIFY → A/B sélective | CLASSIFICATION_TOO_LATE |
| `professional_civil_engineering` | C | KEEP_CLASS → C | CLASSIFICATION_REVIEW |
| `rifling` | C | KEEP_CLASS → C | CLASSIFICATION_REVIEW |
| `standardized_military_rockets` | C | KEEP_CLASS → C | CLASSIFICATION_REVIEW |
| `sugar_refining` | A | SPLIT_TECH → A pour le raffinage traditionnel; déplacer centrifugation/vapeur/vide vers une technologie ultérieure | MIXED_CONCEPT |
| `systematic_cadastral_surveying` | B | RECLASSIFY → A/B sélective | CLASSIFICATION_TOO_LATE |
| `systematic_legal_codification` | B | RECLASSIFY → A/B sélective | CLASSIFICATION_TOO_LATE |
| `systematic_population_registration` | B | RECLASSIFY → A/B sélective | CLASSIFICATION_TOO_LATE |

## 22. Incohérences interrégionales corrigées

- Les traditions médicales européennes, ottomanes, maghrébines et est-asiatiques sont comparées avec la même définition institutionnelle.
- Les canaux chinois ne sont plus filtrés par un modèle de turnpike britannique.
- Le papier, le verre et les meubles ne dépendent plus de la capacité forestière organisée.
- Le crédit public ottoman n’est plus assimilé aux seules bourses du XIXe siècle.
- La coupe de bois ordinaire ne suffit plus à `organized_forestry`.

## 23. Cible mondiale finale

### Technologies ayant le plus d’ADD

| Technologie | Pays actuels | Cible historique | Variation nette |
|---|---:|---:|---:|
| `traditional_food_processing` | 54 | 357 | +303 |
| `traditional_furniture_making` | 0 | 217 | +217 |
| `improved_agricultural_implements` | 2 | 138 | +136 |
| `sugar_refining` | 0 | 104 | +104 |
| `codified_practical_knowledge` | 18 | 117 | +99 |
| `light_infantry_tactics` | 36 | 107 | +71 |
| `variolation_networks` | 1 | 69 | +68 |
| `traditional_papermaking` | 16 | 78 | +62 |
| `traditional_glassmaking` | 0 | 62 | +62 |
| `international_relations` | 279 | 307 | +28 |
| `medical_degrees` | 2 | 54 | +52 |
| `distillation` | 220 | 260 | +40 |
| `organized_textile_production` | 293 | 291 | -2 |
| `permanent_engineer_services` | 4 | 44 | +40 |
| `advanced_crop_rotations` | 3 | 43 | +40 |

### Technologies ayant le plus de REMOVE

| Technologie | Pays actuels | Cible historique | Variation nette |
|---|---:|---:|---:|
| `urbanization` | 365 | 49 | -316 |
| `systematic_administrative_statistics` | 241 | 98 | -143 |
| `shaft_mining` | 184 | 53 | -131 |
| `improved_husbandry` | 461 | 399 | -62 |
| `organized_textile_production` | 293 | 291 | -2 |
| `international_relations` | 279 | 307 | +28 |
| `institutionalized_scientific_exchange` | 46 | 58 | +12 |
| `distillation` | 220 | 260 | +40 |
| `regulated_small_arms` | 44 | 74 | +30 |
| `organized_forestry` | 9 | 30 | +21 |
| `selective_breeding` | 6 | 13 | +7 |
| `light_infantry_tactics` | 36 | 107 | +71 |
| `codified_practical_knowledge` | 18 | 117 | +99 |
| `colonization` | 34 | 34 | +0 |
| `systematic_legal_codification` | 7 | 17 | +10 |

### Top 30 changements mondiaux significatifs

| Technologie | Actuel | Cible | Net | Importance |
|---|---:|---:|---:|---|
| `institutionalized_public_credit` | 3 | 24 | +21 | priorité historique/gameplay |
| `medical_degrees` | 2 | 54 | +52 | priorité historique/gameplay |
| `traditional_papermaking` | 16 | 78 | +62 | priorité historique/gameplay |
| `traditional_glassmaking` | 0 | 62 | +62 | priorité historique/gameplay |
| `traditional_furniture_making` | 0 | 217 | +217 | priorité historique/gameplay |
| `organized_textile_production` | 293 | 291 | -2 | priorité historique/gameplay |
| `organized_forestry` | 9 | 30 | +21 | priorité historique/gameplay |
| `sugar_refining` | 0 | 104 | +104 | priorité historique/gameplay |
| `industrial_acids` | 0 | 4 | +4 | priorité historique/gameplay |
| `regulated_small_arms` | 44 | 74 | +30 | priorité historique/gameplay |
| `atmospheric_engine` | 1 | 8 | +7 | priorité historique/gameplay |
| `industrial_canals` | 3 | 10 | +7 | priorité historique/gameplay |
| `stock_exchange` | 3 | 8 | +5 | priorité historique/gameplay |
| `commercial_insurance_markets` | 3 | 23 | +20 | priorité historique/gameplay |
| `codified_practical_knowledge` | 18 | 117 | +99 | priorité historique/gameplay |
| `variolation_networks` | 1 | 69 | +68 | priorité historique/gameplay |
| `systematic_administrative_statistics` | 241 | 98 | -143 | priorité historique/gameplay |
| `shaft_mining` | 184 | 53 | -131 | priorité historique/gameplay |
| `advanced_crop_rotations` | 3 | 43 | +40 | priorité historique/gameplay |
| `organized_elementary_schooling` | 2 | 26 | +24 | priorité historique/gameplay |
| `urbanization` | 365 | 49 | -316 | variation mondiale importante |
| `traditional_food_processing` | 54 | 357 | +303 | variation mondiale importante |
| `improved_agricultural_implements` | 2 | 138 | +136 | variation mondiale importante |
| `international_relations` | 279 | 307 | +28 | variation mondiale importante |
| `light_infantry_tactics` | 36 | 107 | +71 | variation mondiale importante |
| `improved_husbandry` | 461 | 399 | -62 | variation mondiale importante |
| `distillation` | 220 | 260 | +40 | variation mondiale importante |
| `permanent_engineer_services` | 4 | 44 | +40 | variation mondiale importante |
| `standardized_field_artillery` | 37 | 72 | +35 | variation mondiale importante |
| `institutionalized_scientific_exchange` | 46 | 58 | +12 | variation mondiale importante |

## 24. Delta avec le working tree

Le fichier delta contient 2,761 lignes : ADD=1,262, PENDING_CLASSIFICATION=488, PENDING_TREE_FIX=220, REMOVE=790, UNRESOLVED=1. Il s’agit d’un plan : aucune ligne n’a été appliquée. Les ADD bloqués par l’arbre ou la classification sont explicitement `PENDING_*`.

### Principales transformations par région

| Région | ADD | REMOVE | Non résolus | Revues arbre | Revues classification |
|---|---:|---:|---:|---:|---:|
| EAST_ASIA_SE_ASIA | 132 | 96 | 2 | 10 | 11 |
| NORTHERN_EASTERN_EUROPE | 179 | 15 | 3 | 11 | 8 |
| AMERICAS_CARIBBEAN | 175 | 103 | 3 | 6 | 6 |
| OTTOMAN_MIDDLE_EAST_CENTRAL_ASIA | 198 | 25 | 1 | 8 | 4 |
| CENTRAL_EUROPE_GERMAN_ITALY | 337 | 129 | 7 | 6 | 6 |
| OCEANIA_PACIFIC | 12 | 38 | 0 | 4 | 2 |
| AFRICA | 482 | 215 | 1 | 6 | 1 |
| WESTERN_EUROPE | 145 | 28 | 8 | 7 | 10 |
| SOUTH_ASIA | 253 | 141 | 33 | 6 | 6 |

## 25. Décisions humaines encore requises

- Valider les 26 révisions structurelles actives avant toute fermeture de prérequis.
- Arbitrer les 26 technologies portant une révision globale de classification ou de contenu.
- Résoudre les 7 cas historiques réellement indécidables listés dans le CSV dédié.
- Lancer une recherche régionale dédiée pour GAL, MLT et PPU.

## Contrôles finaux

- 471 TAG recherchés uniques; GAL/MLT/PPU seuls gaps.
- 28 731 relations A/B; aucun doublon TAG × technologie.
- 25 A, 36 B; aucun Technology_ID ou TAG inconnu détecté.
- Cible non fermée artificiellement par les prérequis.
- Aucun fichier gameplay modifié par cette synthèse; aucun setup réécrit.
- Aucun commit, aucun push, aucune PR.

## Résumé compact

| Indicateur | Valeur |
|---|---:|
| Régions chargées | 9 |
| TAG recherchés | 471 |
| Relations A/B auditées | 28 731 |
| KEEP / ADD / REMOVE / REVIEW bruts | 22,559 / 1,672 / 2,882 / 1,618 |
| REVIEW PRESENT / ABSENT / UNRESOLVED | 359 / 1,253 / 6 |
| Taille cible historique (471 TAG) | 3,696 |
| ADD / REMOVE vs working tree | 1,913 / 790 |
| TREE_STRUCTURE_REVIEW actifs | 26 |
| CLASSIFICATION_REVIEW actifs | 26 |
| READY | 164 |
| READY_AFTER_TREE_FIX | 71 |
| READY_AFTER_CLASSIFICATION_DECISION | 187 |
| NEEDS_REVIEW | 49 |
| RESEARCH_GAP | 3 |

**Aucun fichier gameplay modifié, aucun commit, aucun push.**
