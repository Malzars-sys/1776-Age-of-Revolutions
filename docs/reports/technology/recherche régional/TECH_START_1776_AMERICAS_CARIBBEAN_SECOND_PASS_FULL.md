# Second pass complet — Technologies de départ — Amériques et Caraïbes — 1er janvier 1776

> **Recherche historique uniquement.** Aucun fichier gameplay n'a été modifié. Aucun code Victoria 3 n'a été produit. Aucun commit/push n'a été effectué.

## Résumé exécutif

- **TAG étudiés : 57**.
- **Technologies A auditées systématiquement : 25**.
- **Technologies B auditées systématiquement : 36**.
- **Relations A/B obligatoires : 3 477**.
- **Lignes totales : 3 763** (A/B + E pertinentes + `rifling` C pour USA).
- Décisions : **110 ADD**, **24 REMOVE**, **3402 KEEP**, **227 REVIEW**.
- **TREE_STRUCTURE_REVIEW : 122** lignes; **ADD_WITH_PREREQUISITES : 19** lignes.
- **CLASSIFICATION_REVIEW : 1** ligne (`rifling`/USA). S'ajoutent **228** lignes `CLASSIFICATION_TOO_EARLY` et **9** lignes `CLASSIFICATION_TOO_LATE`.

**Convention importante pour une matrice exhaustive :** `KEEP` signifie aussi *conserver l'absence actuelle* lorsque `Current_Status=ABSENT` et que la capacité est historiquement absente. Sans cette convention, chaque relation négative aurait dû être artificiellement marquée `REVIEW`; le couple `Current_Status` + `Decision` rend le sens non ambigu.

## 1. Périmètre

La région reprend le périmètre de la première passe et traite les TAG comme proxys territoriaux lorsque le nom politique est postérieur à 1776. Les capacités métropolitaines ne sont attribuées que lorsqu'elles sont effectivement déployées localement.

- **Atlantic Coast (5)** : `MICC` Michigan Tribal Confederation; `NBS` New Brunswick; `NVS` Nova Scotia; `SML` Yat’siminoli; `USA` America.
- **Brazil (4)** : `BRZ` Brazil; `PNI` Piratini; `PRA` Grão-Pará; `URU` Uruguay.
- **Canada (6)** : `ATB` Athabaska; `BLF` Niitsitapi; `HBC` Hudson's Bay Company; `IRC` Iron Confederacy; `ONT` Ontario; `QUE` Quebec.
- **Central America (8)** : `CUB` Cuba; `GR5` Santo Domingo; `HAI` Haiti; `MEX` Mexico; `MKT` Miskitia; `PCO` Puerto Rico; `SC1` Nueva España; `UCA` Central America.
- **Gran Colombia (3)** : `CLM` Colombia; `SC2` Nueva Granada; `VNZ` Venezuela.
- **Great Plains (10)** : `ABS` Absaroka; `APC` Apache; `ARP` Arapaho; `COM` Comanche; `LKT` Lakota; `LOU` Louisiana; `PWN` Pawnee; `SEQ` Indian Territory; `SLS` Séliš; `TEX` Texas.
- **La Plata (8)** : `ARG` Argentina; `CHL` Chile; `GNI` Guarani; `PAT` Mapuche; `PRG` Paraguay; `SC4` Río de la Plata; `SLK` Selk’nam; `THL` Tehuelche.
- **Pacific Coast (6)** : `ALK` Alaska; `BNN` Pannakwati; `NVJ` Navajo; `NZP` Nimíipuu; `ORG` Oregon; `UTE` Ute.
- **The Andes (7)** : `BOL` Bolivia; `ECU` Ecuador; `IQU` Iquicha; `NPU` North Peru; `PEU` Peru; `SC3` Perú; `SPU` South Peru.

Cas chronologiques structurants : `USA` est lu au 1er janvier 1776 avant les constructions institutionnelles postérieures de l'indépendance; `SC4` n'est pas traité comme un vice-royaume déjà constitué; `ALK` ne reçoit pas les capacités d'un établissement russe permanent qui n'existe pas encore; `HAI`, `ARG`, `URU`, `TEX` et `PNI` sont évalués comme proxys territoriaux de 1776.

## 2. Sources et méthode

### Autorité technique

- `TECH_START_1776_TECHNOLOGIES.csv` : IDs, classification A/B/C/D/E, catégories, déblocages et prérequis.
- `TECH_START_1776_COUNTRIES.csv` : liste et région des TAG.
- `TECH_START_1776_AMERICAS_CARIBBEAN_MATRIX.csv` : première passe régionale.
- `TECH_START_1776_WORLD_COUNTRY_PLAN.csv` : baseline post-synthèse utilisée pour `Current_Status`; sa colonne `Final_Technologies` représente la distribution issue de la première passe mondiale.

### Changement de méthode

1. Chaque relation **57 TAG × 61 technologies A/B** est explicitement décidée; le tier n'est jamais utilisé comme preuve historique.
2. La présence locale d'une capacité est décidée avant l'examen des prérequis.
3. Les trois anciens liens `organized_forestry -> traditional_papermaking/traditional_glassmaking/traditional_furniture_making` sont traités comme **obsolètes** conformément à la nouvelle définition de l'arbre. Le logging rudimentaire ne vaut pas `organized_forestry`.
4. Les colonies ne copient pas automatiquement la métropole : arsenal, école, faculté, assurance, crédit ou manufacture doivent être localement attestés.
5. Les technologies C restent hors distribution; un conflit manifeste avec 1776 produit `CLASSIFICATION_REVIEW`.
6. Une absence est formulée prudemment : `ABSENT` signifie qu'aucune capacité correspondant au nœud gameplay n'est suffisamment établie dans le jeu de sources consulté au cutoff, non que tout savoir apparenté soit inexistant.

### Principales sources historiques et institutionnelles

- Treize Colonies — crédit public — https://www.cambridge.org/core/journals/studies-in-american-political-development/article/our-own-and-our-countrys-ruin-public-credit-war-markets-and-political-transition-in-the-colonial-american-northeast-17581768/89C121DD9C17499E7AC5C3ED69F5A5FF
- Treize Colonies — assurance commerciale — https://commonplace.online/article/insurance-in-colonial-america/
- Philadelphie — papier/papeterie — https://philadelphiaencyclopedia.org/essays/paper-and-papermaking/
- American Philosophical Society — https://www.amphilsoc.org/about/history
- Penn — histoire de la formation médicale — https://www.med.upenn.edu/evpdean/perelman-school-of-medicine-history-timeline.html
- Québec — Forges du Saint-Maurice — https://parks.canada.ca/lhn-nhs/qc/saintmaurice/culture/histoire-history/site/fer-iron
- Québec — Gazette/Imprimerie — https://www.patrimoine-culturel.gouv.qc.ca/detail.do?id=26761&methode=consulter&type=pge
- Halifax — Gazette — https://archives.novascotia.ca/gazette/
- Cuba — arsenal/chantiers de La Havane — https://revistadeindias.revistas.csic.es/index.php/revistadeindias/article/view/630/0
- Cuba — grades médicaux — https://paperity.org/p/188947957/septiembre-6-de-1728-graduacion-del-primer-medico-en-la-universidad-de-la-habana
- Puerto Rico — fortifications espagnoles — https://www.nps.gov/saju/learn/historyculture/history.htm
- Saint-Domingue — université — https://uasd.edu.do/sobre-la-uasd/
- Nouvelle-Espagne — presse — https://gazetademexico.colmex.mx/
- Nouvelle-Espagne — fiscalité — https://www.cambridge.org/core/journals/journal-of-economic-history/article/building-fiscal-capacity-in-colonial-mexico-from-fragmentation-to-centralization/C1E8886F925D1B83BDF1681AE31FF4E9
- Potosí — complexe minier — https://whc.unesco.org/en/list/420
- Huancavelica — mercure/mines — https://whc.unesco.org/en/tentativelists/6263/
- Lima — histoire de la médecine — https://medicina.unmsm.edu.pe/resena-historica/
- Chili — formation médicale — https://www.memoriachilena.gob.cl/602/w3-article-3526.html
- Chili — variolisation — https://www.memoriachilena.gob.cl/602/w3-article-545921.html
- Brésil — Arsenal do Rio — https://arquivodamarinha.marinha.mil.br/index.php/arsenal-de-marinha-do-rio-de-janeiro-4
- Brésil — exploitation organisée du bois — https://www.scielo.br/j/rbh/a/jjjL3bvkjXHhCTMhXsGpRpz/?lang=pt
- Alaska russe — chronologie — https://www.nps.gov/subjects/nhlalaska/russian-alaska.htm
- Río de la Plata — création du vice-royaume — https://buenosaires.gob.ar/gcaba_historico/laciudad/calendario-historico/agosto
- Coke — Ironbridge/Darby — https://www.ironbridge.org.uk/about-us/key-figures-in-the-history-of-the-ironbridge-gorge/
- Newcomen — Science Museum — https://blog.sciencemuseum.org.uk/a-new-age/

## 3. Production

La nouvelle séparation de `organized_forestry` est décisive. La papeterie, la verrerie et la fabrication de meubles sont évaluées sur leurs propres ateliers, fours, moulins et réseaux artisanaux; elles ne sont plus rejetées parce qu'une sylviculture rationalisée manquerait. C'est la principale raison de l'élargissement de `traditional_papermaking`, `traditional_glassmaking` et `traditional_furniture_making`.

Deux nœuds classés A posent en revanche un problème de contenu gameplay. `industrial_acids` débloque une véritable industrie chimique et des usines d'explosifs; `sugar_refining` débloque des procédés comprenant centrifugeuse, betterave, évaporation à vapeur et vacuum pan. L'existence d'un raffinage sucrier colonial traditionnel ne suffit donc pas à attribuer le nœud actuel. `mechanized_weaving` et `advanced_spinning` sont également trop tardifs dans leur contenu actuel.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `traditional_food_processing` | A | 1 | 44 | 43 | 0 | 1 | — |
| `traditional_papermaking` | A | 0 | 3 | 1 | 0 | 2 | — |
| `traditional_glassmaking` | A | 0 | 7 | 5 | 0 | 2 | — |
| `traditional_furniture_making` | A | 0 | 21 | 21 | 0 | 0 | — |
| `organized_textile_production` | A | 36 | 33 | 1 | 0 | 22 | — |
| `distillation` | A | 33 | 33 | 0 | 0 | 1 | — |
| `sugar_refining` | A | 0 | 9 | 0 | 0 | 9 | CLASSIFICATION_TOO_EARLY |
| `industrial_acids` | A | 0 | 0 | 0 | 0 | 0 | CLASSIFICATION_TOO_EARLY |
| `industrial_ceramics` | B | 0 | 0 | 0 | 0 | 0 | — |
| `mechanized_spinning` | B | 0 | 1 | 1 | 0 | 0 | — |
| `mechanized_weaving` | B | 0 | 0 | 0 | 0 | 0 | CLASSIFICATION_TOO_EARLY |
| `advanced_spinning` | B | 0 | 0 | 0 | 0 | 0 | CLASSIFICATION_TOO_EARLY |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

## 4. Agriculture

L'agriculture est séparée de la simple existence de cultures ou d'élevage. `improved_husbandry` reste large lorsque des systèmes agricoles/pastoraux organisés sont attestés, mais il est retiré de plusieurs setups où la première passe avait transformé automatiquement une économie de subsistance ou de chasse en élevage amélioré. Les rotations, instruments améliorés et sélection restent beaucoup plus sélectifs; la plupart des cas américains sont sectoriels plutôt que nationaux.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `improved_husbandry` | A | 57 | 51 | 0 | 4 | 15 | — |
| `selective_breeding` | B | 0 | 2 | 1 | 0 | 1 | — |
| `advanced_crop_rotations` | B | 0 | 1 | 1 | 0 | 0 | — |
| `improved_agricultural_implements` | B | 0 | 3 | 1 | 0 | 2 | — |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

## 5. Mines/métallurgie

La région possède plusieurs centres miniers majeurs — surtout Nouvelle-Espagne et Andes — mais leur sophistication ne doit pas être confondue avec la chaîne britannique coke–Newcomen–alésage de précision. `shaft_mining` et `applied_mineralogy` peuvent donc être positifs dans des zones minières coloniales sans entraîner `coke_smelting`, `atmospheric_engine` ou `precision_boring`. Potosí/Huancavelica servent de cas emblématiques de cette asymétrie.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `shaft_mining` | A | 14 | 14 | 0 | 0 | 4 | — |
| `applied_mineralogy` | B | 11 | 12 | 1 | 0 | 1 | — |
| `coke_smelting` | A | 0 | 0 | 0 | 0 | 0 | — |
| `atmospheric_engine` | B | 0 | 0 | 0 | 0 | 0 | — |
| `precision_boring` | B | 0 | 0 | 0 | 0 | 0 | — |
| `condensing_steam_engines` | B | 0 | 0 | 0 | 0 | 0 | — |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

## 6. Infrastructure

`organized_forestry` signifie désormais exploitation forestière organisée/rationalisée. La simple coupe de bois ne suffit pas; l'audit retient surtout des systèmes coloniaux ou étatiques de fourniture navale/commerciale. Les réseaux de turnpikes au sens du nœud et les canaux industriels restent absents au cutoff dans la région; les projets et voies ordinaires ne sont pas assimilés à ces technologies.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `organized_forestry` | A | 1 | 7 | 6 | 0 | 2 | — |
| `turnpike_road_networks` | B | 0 | 0 | 0 | 0 | 0 | — |
| `industrial_canals` | B | 0 | 0 | 0 | 0 | 0 | — |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

**E pertinente : `urbanization`.** Elle est conservée lorsque le nœud abstrait raisonnablement des centres urbains/constructifs locaux, mais **REMOVE** pour 16 TAG où la première passe avait conservé un alias de compatibilité sans équivalent institutionnel local.

## 7. Finance et économie

Le second passage corrige la sous-évaluation des institutions de crédit tout en évitant de confondre commerce et marchés financiers. Les Treize Colonies obtiennent `institutionalized_public_credit` et `commercial_insurance_markets` sur la base de finances publiques provinciales et d'une assurance commerciale effective. Inversement, `commercial_insurance_markets` est retirée de plusieurs setups sud-américains où le premier passage l'avait héritée sans institution locale suffisamment démontrée. `stock_exchange` reste absent: l'existence de crédit ou de compagnies n'est pas une bourse organisée.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `institutionalized_public_credit` | A | 0 | 7 | 1 | 0 | 6 | — |
| `commercial_insurance_markets` | A | 4 | 5 | 1 | 4 | 4 | — |
| `stock_exchange` | A | 0 | 0 | 0 | 0 | 0 | — |
| `political_economy` | B | 0 | 0 | 0 | 0 | 0 | — |
| `classical_political_economy` | B | 0 | 0 | 0 | 0 | 0 | — |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

## 8. Commerce

`international_relations` est traité comme capacité diplomatique/commerciale institutionnalisée, non comme simple contact avec des étrangers. Les colonies et compagnies sont évaluées localement: un port exportateur ne reçoit pas automatiquement toutes les institutions de la métropole. Les puissances marchandes régionales ou administrations coloniales structurées peuvent néanmoins l'établir de façon sectorielle.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `international_relations` | A | 38 | 0 | 3 | 0 | 16 | — |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

**E pertinentes : `colonization`, `multilateral_alliances`.** Elles sont examinées pour leurs déblocages/abstractions; aucune nouvelle attribution n'est créée sur la seule base d'un empire métropolitain.

## 9. Administration

L'audit distingue statistiques administratives, recensement, cadastre, codification et doctrines politiques. Des fiscalités sophistiquées existent en Amérique espagnole et portugaise, mais cela n'implique pas automatiquement population registration, cadastre systématique ou codification moderne. Pour `constitutional_government`, `human_rights` et `national_sovereignty`, le 1er janvier 1776 est particulièrement strict aux États-Unis: les développements postérieurs de 1776 ne sont pas rétro-projetés.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `systematic_administrative_statistics` | A | 32 | 21 | 0 | 0 | 11 | — |
| `systematic_population_registration` | B | 0 | 5 | 0 | 0 | 5 | — |
| `systematic_cadastral_surveying` | B | 0 | 6 | 0 | 0 | 6 | — |
| `systematic_legal_codification` | B | 0 | 0 | 0 | 0 | 13 | — |
| `codified_practical_knowledge` | A | 13 | 1 | 0 | 0 | 12 | — |
| `constitutional_government` | B | 0 | 1 | 0 | 0 | 1 | — |
| `human_rights` | B | 0 | 1 | 0 | 0 | 1 | — |
| `national_sovereignty` | B | 0 | 1 | 0 | 0 | 1 | — |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

**E pertinente : `political_agitation`.** Aucun cas américain ne justifie une nouvelle attribution au cutoff selon le contenu gameplay actuel.

## 10. Science/éducation

Les sociétés savantes, presses périodiques, académies spécialisées et réseaux scolaires sont distingués. Les Treize Colonies disposent d'un échange scientifique institutionnalisé, d'un réseau périodique et, dans certaines colonies, d'une scolarisation élémentaire légalement organisée. Québec et Halifax fournissent des exemples de presse coloniale locale. Les universités traditionnelles seules ne suffisent pas à attribuer une académie technique.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `institutionalized_scientific_exchange` | A | 14 | 9 | 1 | 0 | 11 | — |
| `periodical_print_networks` | A | 3 | 9 | 1 | 0 | 5 | — |
| `specialized_technical_academies` | B | 0 | 2 | 0 | 0 | 2 | — |
| `organized_elementary_schooling` | B | 0 | 1 | 1 | 0 | 0 | — |
| `veterinary_science` | B | 0 | 0 | 0 | 0 | 0 | — |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

## 11. Médecine

C'est l'une des plus fortes révisions. `medical_degrees` représente bien des facultés, collèges, grades et certification institutionnalisée, pas un diplôme médical moderne du XIXe siècle. Des systèmes nettement antérieurs à 1776 existent à Mexico, Lima, Quito, La Havane, Saint-Domingue, Caracas et Santiago. La classification B est donc trop tardive pour plusieurs TAG. La variolisation reste plus rare et est ajoutée lorsqu'un réseau/pratique organisée est attesté, notamment au Chili et dans les Treize Colonies.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `medical_degrees` | B | 5 | 14 | 8 | 0 | 2 | CLASSIFICATION_TOO_LATE |
| `variolation_networks` | B | 0 | 2 | 2 | 0 | 0 | — |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

## 12. Militaire

Une armée ou une milice ne suffit pas à recevoir l'ensemble des nœuds. Fortification scientifique, artillerie standardisée, inspection des armes, services du génie, topographie, hôpitaux permanents et tactiques légères sont séparés. Les grands complexes fortifiés espagnols de Cuba, Porto Rico et Nouvelle-Grenade justifient certaines capacités de génie, tandis que beaucoup de milices locales ne les justifient pas. `rifling` est examiné séparément comme cas C pour les Treize Colonies.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `scientific_fortification_siegecraft` | A | 3 | 3 | 0 | 0 | 0 | — |
| `regulated_small_arms` | A | 19 | 19 | 0 | 0 | 19 | — |
| `light_infantry_tactics` | B | 37 | 27 | 0 | 0 | 6 | — |
| `standardized_field_artillery` | B | 20 | 20 | 0 | 0 | 13 | — |
| `armament_standardization_inspection` | B | 0 | 4 | 0 | 0 | 4 | — |
| `horse_artillery` | B | 0 | 0 | 0 | 0 | 0 | — |
| `military_topographic_surveying` | B | 0 | 6 | 0 | 0 | 6 | — |
| `permanent_engineer_services` | B | 0 | 8 | 6 | 0 | 2 | — |
| `permanent_military_hospitals` | B | 0 | 5 | 1 | 0 | 4 | — |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

**E/C pertinentes : `field_works` et `rifling`.** `field_works` ne produit pas d'ajout; `rifling` est `REVIEW` pour `USA` avec `CLASSIFICATION_REVIEW`, car des compagnies de riflemen existent dès 1775 mais le PM `pm_rifles` peut représenter une généralisation plus tardive.

## 13. Marine

Les capacités navales sont réservées aux ports où existent réellement arsenaux, chantiers, méthodes de conception ou systèmes d'administration navale locaux. La Havane et Rio de Janeiro sont les principaux cas forts; Halifax fournit aussi un dockyard impérial local. La chronométrie marine, le survey/classification institutionnalisé et le cuivrage restent essentiellement des frontières métropolitaines/atlantiques qui ne sont pas automatiquement transférées aux colonies.

| Technologie | Cl. | Présente actuellement | Positive historiquement* | ADD | REMOVE | REVIEW | Classification issue |
|---|:---:|---:|---:|---:|---:|---:|---|
| `enclosed_dock_systems` | A | 0 | 3 | 0 | 0 | 3 | — |
| `state_dockyard_systems` | A | 2 | 4 | 1 | 0 | 1 | — |
| `scientific_naval_architecture` | A | 0 | 5 | 2 | 0 | 3 | — |
| `marine_chronometry` | B | 0 | 0 | 0 | 0 | 0 | — |
| `ship_classification_surveying` | B | 0 | 0 | 0 | 0 | 0 | — |
| `copper_sheathing` | B | 0 | 0 | 0 | 0 | 0 | — |

\* *Positive historiquement* = `ESTABLISHED`, `SECTORAL` ou `FRONTIER`, y compris si la décision finale reste `REVIEW` à cause du périmètre gameplay du nœud.

## 14. Analyse pays par pays

Les tableaux ci-dessous donnent un diagnostic dans **les onze domaines obligatoires**. Toutes les relations A/B, y compris les absences non affichées dans le résumé, sont détaillées ligne par ligne dans le CSV.

### ABS — Absaroka (Great Plains)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 1, REVIEW 2; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `urbanization`.
- **REVIEW** : `improved_husbandry`, `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### ALK — Alaska (Pacific Coast)

Aucun établissement russe permanent n'existe encore au 1er janvier 1776; le TAG est évalué d'abord selon les capacités locales autochtones.

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 2, REVIEW 1; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `improved_husbandry`, `urbanization`.
- **REVIEW** : `organized_textile_production`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | aucun A/B positif attesté; **REMOVE** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://www.nps.gov/subjects/nhlalaska/russian-alaska.htm
- https://www.burkemuseum.org/collections-and-research/heritage/artscultures/coast-salish-art/carving-tools-technologies
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/

### APC — Apache (Great Plains)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 1, REVIEW 2; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `urbanization`.
- **REVIEW** : `improved_husbandry`, `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### ARG — Argentina (La Plata)

Le TAG est interprété comme les territoires du futur espace argentin sous institutions coloniales de 1776.

- **Écarts à l'implémentation actuelle** : ADD 2, REMOVE 0, REVIEW 2; TREE_STRUCTURE_REVIEW 1.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`.
- **REVIEW** : `organized_textile_production`, `systematic_administrative_statistics`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté; **REVIEW** `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://buenosaires.gob.ar/gcaba_historico/laciudad/calendario-historico/agosto
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://whc.unesco.org/en/list/420
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### ARP — Arapaho (Great Plains)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 1, REVIEW 2; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `urbanization`.
- **REVIEW** : `improved_husbandry`, `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://home.nps.gov/glac/learn/education/intro-to-native-american.htm
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/

### ATB — Athabaska (Canada)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 2, REVIEW 1; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `improved_husbandry`, `urbanization`.
- **REVIEW** : `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | aucun A/B positif attesté; **REMOVE** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://whc.unesco.org/en/list/420
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### BLF — Niitsitapi (Canada)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 1, REVIEW 2; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `urbanization`.
- **REVIEW** : `improved_husbandry`, `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://home.nps.gov/glac/learn/education/intro-to-native-american.htm
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/

### BNN — Pannakwati (Pacific Coast)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 0.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `improved_husbandry`, `international_relations`, `urbanization`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`; **ADD** `traditional_food_processing`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REVIEW/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.burkemuseum.org/collections-and-research/heritage/artscultures/coast-salish-art/coast-salish-weaving-tools
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### BOL — Bolivia (The Andes)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 3.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `regulated_small_arms`, `standardized_field_artillery`, `institutionalized_scientific_exchange`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté; **REVIEW** `institutionalized_scientific_exchange` |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `regulated_small_arms`, `standardized_field_artillery`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://whc.unesco.org/en/list/420
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://whc.unesco.org/en/tentativelists/6263/
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### BRZ — Brazil (Brazil)

- **Écarts à l'implémentation actuelle** : ADD 5, REMOVE 0, REVIEW 8; TREE_STRUCTURE_REVIEW 5.
- **ADD** : `scientific_naval_architecture`, `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `applied_mineralogy`.
- **REVIEW** : `enclosed_dock_systems`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `permanent_engineer_services`, `sugar_refining`, `codified_practical_knowledge`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`, `sugar_refining`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `sugar_refining`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; **ADD** `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | positif: `organized_forestry`; **ADD** `organized_forestry`; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `systematic_legal_codification`, `codified_practical_knowledge` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `regulated_small_arms`, `standardized_field_artillery`, `permanent_engineer_services`; **REVIEW** `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `permanent_engineer_services`; limites: `horse_artillery` |
| Marine | positif: `enclosed_dock_systems`, `state_dockyard_systems`, `scientific_naval_architecture`; **ADD** `scientific_naval_architecture`; **REVIEW** `enclosed_dock_systems`; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://arquivodamarinha.marinha.mil.br/index.php/arsenal-de-marinha-do-rio-de-janeiro-4
- https://www.scielo.br/j/rbh/a/jjjL3bvkjXHhCTMhXsGpRpz/?lang=pt
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://www.fazenda.mg.gov.br/secretaria/historia/

### CHL — Chile (La Plata)

- **Écarts à l'implémentation actuelle** : ADD 3, REMOVE 1, REVIEW 6; TREE_STRUCTURE_REVIEW 7.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`, `variolation_networks`.
- **REMOVE** : `commercial_insurance_markets`.
- **REVIEW** : `regulated_small_arms`, `permanent_military_hospitals`, `standardized_field_artillery`, `permanent_engineer_services`, `codified_practical_knowledge`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; **REMOVE** `commercial_insurance_markets`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `systematic_legal_codification`, `codified_practical_knowledge` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | positif: `medical_degrees`, `variolation_networks`; **ADD** `variolation_networks` |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `permanent_engineer_services`, `permanent_military_hospitals`; **REVIEW** `regulated_small_arms`, `standardized_field_artillery`, `permanent_engineer_services`, `permanent_military_hospitals`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://buenosaires.gob.ar/gcaba_historico/laciudad/calendario-historico/agosto
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://www.memoriachilena.gob.cl/602/w3-article-545921.html
- https://www.memoriachilena.gob.cl/602/w3-article-3526.html

### CLM — Colombia (Gran Colombia)

- **Écarts à l'implémentation actuelle** : ADD 4, REMOVE 1, REVIEW 7; TREE_STRUCTURE_REVIEW 5.
- **ADD** : `permanent_engineer_services`, `traditional_food_processing`, `traditional_furniture_making`, `institutionalized_scientific_exchange`.
- **REMOVE** : `commercial_insurance_markets`.
- **REVIEW** : `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `military_topographic_surveying`, `codified_practical_knowledge`, `medical_degrees`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; **REMOVE** `commercial_insurance_markets`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `systematic_legal_codification`, `codified_practical_knowledge` |
| Science/éducation | positif: `institutionalized_scientific_exchange`; **ADD** `institutionalized_scientific_exchange` |
| Médecine | positif: `medical_degrees`; **REVIEW** `medical_degrees` |
| Militaire | positif: `regulated_small_arms`, `standardized_field_artillery`, `military_topographic_surveying`, `permanent_engineer_services`; **ADD** `permanent_engineer_services`; **REVIEW** `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `military_topographic_surveying`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://revistadeindias.revistas.csic.es/index.php/revistadeindias/article/view/1113/0
- https://www.imprenta.gov.co/museodeartesgraficas
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://urosario.edu.co/sites/default/files/static/cedulasreales/paginas/articulos/cedula-real-sobre-pasquines.html

### COM — Comanche (Great Plains)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 1, REVIEW 1; TREE_STRUCTURE_REVIEW 0.
- **ADD** : `international_relations`.
- **REMOVE** : `urbanization`.
- **REVIEW** : `improved_husbandry`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **ADD** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### CUB — Cuba (Central America)

- **Écarts à l'implémentation actuelle** : ADD 5, REMOVE 0, REVIEW 12; TREE_STRUCTURE_REVIEW 6.
- **ADD** : `scientific_naval_architecture`, `permanent_engineer_services`, `traditional_food_processing`, `traditional_furniture_making`, `medical_degrees`.
- **REVIEW** : `enclosed_dock_systems`, `regulated_small_arms`, `permanent_military_hospitals`, `armament_standardization_inspection`, `military_topographic_surveying`, `organized_textile_production`, `sugar_refining`, `institutionalized_public_credit`, `periodical_print_networks`, `codified_practical_knowledge`, `commercial_insurance_markets`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`, `sugar_refining`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`, `sugar_refining`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | positif: `institutionalized_public_credit`, `commercial_insurance_markets`; **REVIEW** `institutionalized_public_credit`, `commercial_insurance_markets`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `systematic_legal_codification`, `codified_practical_knowledge` |
| Science/éducation | positif: `periodical_print_networks`; **REVIEW** `periodical_print_networks` |
| Médecine | positif: `medical_degrees`; **ADD** `medical_degrees` |
| Militaire | positif: `scientific_fortification_siegecraft`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `armament_standardization_inspection`, `military_topographic_surveying`, `permanent_engineer_services`, `permanent_military_hospitals`; **ADD** `permanent_engineer_services`; **REVIEW** `regulated_small_arms`, `armament_standardization_inspection`, `military_topographic_surveying`, `permanent_military_hospitals`; limites: `horse_artillery` |
| Marine | positif: `enclosed_dock_systems`, `state_dockyard_systems`, `scientific_naval_architecture`; **ADD** `scientific_naval_architecture`; **REVIEW** `enclosed_dock_systems`; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://revistadeindias.revistas.csic.es/index.php/revistadeindias/article/view/630/0
- https://pares.cultura.gob.es/ParesBusquedas20/catalogo/autoridad/109060
- https://www.nps.gov/saju/learn/historyculture/history.htm
- https://www.new.ox.ac.uk/english-literature-through-the-ages/eighteenth-century-and-romanticism-1701-1836

### ECU — Ecuador (The Andes)

- **Écarts à l'implémentation actuelle** : ADD 3, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 2.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`, `medical_degrees`.
- **REVIEW** : `shaft_mining`, `institutionalized_scientific_exchange`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`; **REVIEW** `shaft_mining`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `systematic_legal_codification` |
| Science/éducation | aucun A/B positif attesté; **REVIEW** `institutionalized_scientific_exchange` |
| Médecine | positif: `medical_degrees`; **ADD** `medical_degrees` |
| Militaire | positif: `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://whc.unesco.org/en/list/420
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://revistadigital.uce.edu.ec/index.php/CIENCIAS_MEDICAS/article/view/1457
- https://revistadigital.uce.edu.ec/index.php/CIENCIAS_MEDICAS/article/view/326

### GNI — Guarani (La Plata)

- **Écarts à l'implémentation actuelle** : ADD 3, REMOVE 0, REVIEW 0; TREE_STRUCTURE_REVIEW 0.
- **ADD** : `organized_textile_production`, `traditional_food_processing`, `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `organized_textile_production`; **ADD** `traditional_food_processing`, `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **ADD** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/SECTORAL |

Sources principales de ce diagnostic :
- https://www.cambridge.org/core/journals/journal-of-economic-history/article/guarani-and-their-missions-a-socioeconomic-history-by-j-s-sarreal-julia-stanford-ca-stanford-university-press-2014-pp-xiii-335-6500-cloth/9DE161D10001BBFEE73BBB7903FCF229
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### GR5 — Santo Domingo (Central America)

- **Écarts à l'implémentation actuelle** : ADD 3, REMOVE 0, REVIEW 4; TREE_STRUCTURE_REVIEW 3.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`, `medical_degrees`.
- **REVIEW** : `standardized_field_artillery`, `organized_textile_production`, `sugar_refining`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`, `sugar_refining`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`, `sugar_refining`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `systematic_legal_codification` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | positif: `medical_degrees`; **ADD** `medical_degrees` |
| Militaire | positif: `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `standardized_field_artillery`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.new.ox.ac.uk/english-literature-through-the-ages/eighteenth-century-and-romanticism-1701-1836
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://uasd.edu.do/sobre-la-uasd/
- https://uasd.edu.do/facultad-ciencias-salud/historia/

### HAI — Haiti (Central America)

Le TAG sert de proxy pour la colonie française de Saint-Domingue en janvier 1776, pas pour l'État haïtien ultérieur.

- **Écarts à l'implémentation actuelle** : ADD 2, REMOVE 0, REVIEW 7; TREE_STRUCTURE_REVIEW 4.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`.
- **REVIEW** : `standardized_field_artillery`, `organized_textile_production`, `sugar_refining`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `codified_practical_knowledge`, `commercial_insurance_markets`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`, `sugar_refining`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`, `sugar_refining`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | positif: `institutionalized_public_credit`, `commercial_insurance_markets`; **REVIEW** `institutionalized_public_credit`, `commercial_insurance_markets`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `codified_practical_knowledge` |
| Science/éducation | positif: `periodical_print_networks`; **REVIEW** `institutionalized_scientific_exchange` |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `standardized_field_artillery`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://catalogue.bnf.fr/ark:/12148/cb32780604j
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://catalogue.bnf.fr/ark:/12148/cb155838965
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### HBC — Hudson's Bay Company (Canada)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 2; TREE_STRUCTURE_REVIEW 1.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `organized_forestry`, `organized_textile_production`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | positif: `organized_forestry`; **REVIEW** `organized_forestry`; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics` |
| Science/éducation | positif: `institutionalized_scientific_exchange` |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://parks.canada.ca/culture/designation/evenement-event/scientifiques-canada-science
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://www.parks.canada.ca/lhn-nhs/ns/halifax/culture/histoire-history/citadelles-4-citadels
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### IQU — Iquicha (The Andes)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 4; TREE_STRUCTURE_REVIEW 2.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `distillation`, `improved_husbandry`, `shaft_mining`, `applied_mineralogy`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `distillation`; **ADD** `traditional_food_processing`; **REVIEW** `distillation`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | aucun A/B positif attesté; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; **REVIEW** `shaft_mining`, `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://whc.unesco.org/en/list/420
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://whc.unesco.org/en/tentativelists/6263/
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### IRC — Iron Confederacy (Canada)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 2, REVIEW 1; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `improved_husbandry`, `urbanization`.
- **REVIEW** : `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | aucun A/B positif attesté; **REMOVE** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://whc.unesco.org/en/list/420
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### LKT — Lakota (Great Plains)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 1, REVIEW 2; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `urbanization`.
- **REVIEW** : `improved_husbandry`, `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### LOU — Louisiana (Great Plains)

- **Écarts à l'implémentation actuelle** : ADD 2, REMOVE 0, REVIEW 5; TREE_STRUCTURE_REVIEW 3.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`.
- **REVIEW** : `regulated_small_arms`, `standardized_field_artillery`, `organized_textile_production`, `sugar_refining`, `systematic_administrative_statistics`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`, `sugar_refining`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`, `sugar_refining`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté; **REVIEW** `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `regulated_small_arms`, `standardized_field_artillery`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://www.tshaonline.org/handbook/entries/spanish-texas
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### MEX — Mexico (Central America)

- **Écarts à l'implémentation actuelle** : ADD 5, REMOVE 0, REVIEW 14; TREE_STRUCTURE_REVIEW 9.
- **ADD** : `permanent_engineer_services`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `medical_degrees`.
- **REVIEW** : `regulated_small_arms`, `armament_standardization_inspection`, `military_topographic_surveying`, `traditional_papermaking`, `improved_agricultural_implements`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `codified_practical_knowledge`, `commercial_insurance_markets`, `specialized_technical_academies`, `systematic_population_registration`, `systematic_cadastral_surveying`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_papermaking`, `traditional_glassmaking`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_glassmaking`, `traditional_furniture_making`; **REVIEW** `traditional_papermaking`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`, `improved_agricultural_implements`; **REVIEW** `improved_agricultural_implements` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | positif: `institutionalized_public_credit`, `commercial_insurance_markets`; **REVIEW** `institutionalized_public_credit`, `commercial_insurance_markets`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`, `systematic_population_registration`, `systematic_cadastral_surveying`; **REVIEW** `systematic_population_registration`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `codified_practical_knowledge` |
| Science/éducation | positif: `institutionalized_scientific_exchange`, `periodical_print_networks`, `specialized_technical_academies`; **REVIEW** `institutionalized_scientific_exchange`, `periodical_print_networks`, `specialized_technical_academies` |
| Médecine | positif: `medical_degrees`; **ADD** `medical_degrees` |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `armament_standardization_inspection`, `military_topographic_surveying`, `permanent_engineer_services`; **ADD** `permanent_engineer_services`; **REVIEW** `regulated_small_arms`, `armament_standardization_inspection`, `military_topographic_surveying`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://ulua.uv.mx/index.php/ulua/article/view/2676
- https://www.cambridge.org/core/journals/journal-of-economic-history/article/building-fiscal-capacity-in-colonial-mexico-from-fragmentation-to-centralization/C1E8886F925D1B83BDF1681AE31FF4E9
- https://gazetademexico.colmex.mx/
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF

### MICC — Michigan Tribal Confederation (Atlantic Coast)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 2; TREE_STRUCTURE_REVIEW 1.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `organized_textile_production`, `urbanization`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`; **ADD** `traditional_food_processing`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REVIEW/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.nps.gov/articles/erosion-of-the-middle-ground.htm
- https://www.loc.gov/collections/continental-congress-and-constitutional-convention-from-1774-to-1789/articles-and-essays/timeline/1775/
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/

### MKT — Miskitia (Central America)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 1.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `improved_husbandry`, `organized_textile_production`, `urbanization`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`; **ADD** `traditional_food_processing`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REVIEW/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.cambridge.org/core/journals/business-history-review/article/rise-and-fall-of-george-frederic-augustus-ii-the-central-american-caribbean-and-atlantic-life-of-a-miskitu-king-18051824/95104178A18D586FD39B892D1BC2BA18
- https://www.nps.gov/saju/learn/historyculture/history.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/

### NBS — New Brunswick (Atlantic Coast)

- **Écarts à l'implémentation actuelle** : ADD 2, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 1.
- **ADD** : `organized_forestry`, `traditional_food_processing`.
- **REVIEW** : `light_infantry_tactics`, `organized_textile_production`, `systematic_administrative_statistics`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | positif: `organized_forestry`; **ADD** `organized_forestry`; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté; **REVIEW** `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; **REVIEW** `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.pc.gc.ca/apps/dfhd/page_nhs_eng.aspx?id=284
- https://www.parks.canada.ca/lhn-nhs/ns/halifax/culture/histoire-history/citadelles-4-citadels
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://library-biblio.parl.ca/sites/PublicWebsite/default/en_CA/About/Spotlight/RareBooks/Archives/LaGazettedeQu%C3%A9bec-

### NPU — North Peru (The Andes)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 1, REVIEW 4; TREE_STRUCTURE_REVIEW 5.
- **ADD** : `traditional_food_processing`.
- **REMOVE** : `commercial_insurance_markets`.
- **REVIEW** : `regulated_small_arms`, `standardized_field_artillery`, `traditional_glassmaking`, `codified_practical_knowledge`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_glassmaking`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`; **REVIEW** `traditional_glassmaking`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; **REMOVE** `commercial_insurance_markets`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `codified_practical_knowledge` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | positif: `medical_degrees` |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `regulated_small_arms`, `standardized_field_artillery`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://whc.unesco.org/en/list/420
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://whc.unesco.org/en/tentativelists/6263/
- https://revistas.pucp.edu.pe/index.php/historica/article/view/7721

### NVJ — Navajo (Pacific Coast)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 1, REVIEW 2; TREE_STRUCTURE_REVIEW 0.
- **ADD** : `traditional_food_processing`.
- **REMOVE** : `urbanization`.
- **REVIEW** : `organized_textile_production`, `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `organized_textile_production`; **ADD** `traditional_food_processing`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://www.nps.gov/articles/000/new-mexico-fiber-arts-traditions.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### NVS — Nova Scotia (Atlantic Coast)

- **Écarts à l'implémentation actuelle** : ADD 5, REMOVE 0, REVIEW 6; TREE_STRUCTURE_REVIEW 2.
- **ADD** : `state_dockyard_systems`, `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `periodical_print_networks`.
- **REVIEW** : `enclosed_dock_systems`, `regulated_small_arms`, `scientific_naval_architecture`, `permanent_military_hospitals`, `organized_textile_production`, `institutionalized_scientific_exchange`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | positif: `organized_forestry`; **ADD** `organized_forestry`; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics` |
| Science/éducation | positif: `periodical_print_networks`; **ADD** `periodical_print_networks`; **REVIEW** `institutionalized_scientific_exchange` |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `scientific_fortification_siegecraft`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `permanent_military_hospitals`; **REVIEW** `regulated_small_arms`, `permanent_military_hospitals`; limites: `horse_artillery` |
| Marine | positif: `enclosed_dock_systems`, `state_dockyard_systems`, `scientific_naval_architecture`; **ADD** `state_dockyard_systems`; **REVIEW** `enclosed_dock_systems`, `scientific_naval_architecture`; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.pc.gc.ca/apps/dfhd/page_nhs_eng.aspx?id=284
- https://archives.novascotia.ca/gazette/
- https://www.parks.canada.ca/lhn-nhs/ns/halifax/culture/histoire-history/citadelles-4-citadels
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF

### NZP — Nimíipuu (Pacific Coast)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 0.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `improved_husbandry`, `international_relations`, `urbanization`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`; **ADD** `traditional_food_processing`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REVIEW/ABSTRACT |

Sources principales de ce diagnostic :
- https://home.nps.gov/glac/learn/education/intro-to-native-american.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### ONT — Ontario (Canada)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 1.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `light_infantry_tactics`, `organized_textile_production`, `systematic_administrative_statistics`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté; **REVIEW** `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; **REVIEW** `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.parks.canada.ca/lhn-nhs/ns/halifax/culture/histoire-history/citadelles-4-citadels
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://library-biblio.parl.ca/sites/PublicWebsite/default/en_CA/About/Spotlight/RareBooks/Archives/LaGazettedeQu%C3%A9bec-
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### ORG — Oregon (Pacific Coast)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 1, REVIEW 4; TREE_STRUCTURE_REVIEW 1.
- **REMOVE** : `urbanization`.
- **REVIEW** : `improved_husbandry`, `organized_forestry`, `organized_textile_production`, `traditional_food_processing`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`; **REVIEW** `traditional_food_processing`, `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | aucun A/B positif attesté; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; **REVIEW** `organized_forestry`; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://www.oregonencyclopedia.org/articles/cartography_of_oregon_1507_1848/
- https://home.nps.gov/fova/learn/historyculture/hbcfort1.htm
- https://www.burkemuseum.org/collections-and-research/heritage/artscultures/coast-salish-art/coast-salish-weaving-tools
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### PAT — Mapuche (La Plata)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 1, REVIEW 1; TREE_STRUCTURE_REVIEW 0.
- **ADD** : `traditional_food_processing`.
- **REMOVE** : `urbanization`.
- **REVIEW** : `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`; **ADD** `traditional_food_processing`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://www.memoriachilena.gob.cl/602/w3-article-95800.html
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### PCO — Puerto Rico (Central America)

- **Écarts à l'implémentation actuelle** : ADD 3, REMOVE 0, REVIEW 6; TREE_STRUCTURE_REVIEW 2.
- **ADD** : `permanent_engineer_services`, `traditional_food_processing`, `traditional_furniture_making`.
- **REVIEW** : `regulated_small_arms`, `permanent_military_hospitals`, `military_topographic_surveying`, `organized_textile_production`, `sugar_refining`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`, `sugar_refining`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`, `sugar_refining`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `systematic_legal_codification` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `scientific_fortification_siegecraft`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `military_topographic_surveying`, `permanent_engineer_services`, `permanent_military_hospitals`; **ADD** `permanent_engineer_services`; **REVIEW** `regulated_small_arms`, `military_topographic_surveying`, `permanent_military_hospitals`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.nps.gov/saju/learn/historyculture/history.htm
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://www.loc.gov/item/2013201074/
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### PEU — Peru (The Andes)

- **Écarts à l'implémentation actuelle** : ADD 4, REMOVE 0, REVIEW 8; TREE_STRUCTURE_REVIEW 5.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `medical_degrees`.
- **REVIEW** : `regulated_small_arms`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `codified_practical_knowledge`, `systematic_population_registration`, `systematic_cadastral_surveying`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_glassmaking`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_glassmaking`, `traditional_furniture_making`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | positif: `institutionalized_public_credit`; **REVIEW** `institutionalized_public_credit`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`, `systematic_population_registration`, `systematic_cadastral_surveying`; **REVIEW** `systematic_population_registration`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `codified_practical_knowledge` |
| Science/éducation | positif: `institutionalized_scientific_exchange`, `periodical_print_networks`; **REVIEW** `institutionalized_scientific_exchange`, `periodical_print_networks` |
| Médecine | positif: `medical_degrees`; **ADD** `medical_degrees` |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `regulated_small_arms`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://whc.unesco.org/en/list/420
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://revistas.pucp.edu.pe/index.php/historica/article/view/7721
- https://medicina.unmsm.edu.pe/resena-historica/

### PNI — Piratini (Brazil)

Le TAG Piratini est anachronique politiquement; les capacités sont évaluées comme celles du territoire sud-brésilien correspondant en 1776.

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 3.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `distillation`; **ADD** `traditional_food_processing`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté; **REVIEW** `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `regulated_small_arms`, `standardized_field_artillery`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.fazenda.mg.gov.br/secretaria/historia/
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://arquivodamarinha.marinha.mil.br/index.php/arsenal-de-marinha-do-rio-de-janeiro-4
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### PRA — Grão-Pará (Brazil)

- **Écarts à l'implémentation actuelle** : ADD 2, REMOVE 0, REVIEW 5; TREE_STRUCTURE_REVIEW 2.
- **ADD** : `organized_forestry`, `traditional_food_processing`.
- **REVIEW** : `state_dockyard_systems`, `scientific_naval_architecture`, `organized_textile_production`, `sugar_refining`, `systematic_administrative_statistics`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `organized_textile_production`, `distillation`, `sugar_refining`; **ADD** `traditional_food_processing`; **REVIEW** `organized_textile_production`, `sugar_refining`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | positif: `organized_forestry`; **ADD** `organized_forestry`; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté; **REVIEW** `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | positif: `state_dockyard_systems`, `scientific_naval_architecture`; **REVIEW** `state_dockyard_systems`, `scientific_naval_architecture`; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://revistas.usp.br/anaismp/en/article/view/216289
- https://www.scielo.br/j/rbh/a/jjjL3bvkjXHhCTMhXsGpRpz/?lang=pt
- https://www.fazenda.mg.gov.br/secretaria/historia/
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF

### PRG — Paraguay (La Plata)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 1; TREE_STRUCTURE_REVIEW 1.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `systematic_administrative_statistics`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté; **REVIEW** `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://buenosaires.gob.ar/gcaba_historico/laciudad/calendario-historico/agosto
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://whc.unesco.org/en/list/420
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### PWN — Pawnee (Great Plains)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 2; TREE_STRUCTURE_REVIEW 0.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `international_relations`, `urbanization`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`; **ADD** `traditional_food_processing`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REVIEW/ABSTRACT |

Sources principales de ce diagnostic :
- https://repository.si.edu/bitstreams/d2df1c71-2f08-47f6-b540-2bddcaf517e8/download
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### QUE — Quebec (Canada)

- **Écarts à l'implémentation actuelle** : ADD 3, REMOVE 0, REVIEW 8; TREE_STRUCTURE_REVIEW 3.
- **ADD** : `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`.
- **REVIEW** : `regulated_small_arms`, `light_infantry_tactics`, `organized_textile_production`, `shaft_mining`, `institutionalized_scientific_exchange`, `codified_practical_knowledge`, `systematic_population_registration`, `systematic_cadastral_surveying`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`; **REVIEW** `shaft_mining`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | positif: `organized_forestry`; **ADD** `organized_forestry`; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`, `systematic_population_registration`, `systematic_cadastral_surveying`; **REVIEW** `systematic_population_registration`, `systematic_cadastral_surveying`, `codified_practical_knowledge` |
| Science/éducation | positif: `institutionalized_scientific_exchange`, `periodical_print_networks`; **REVIEW** `institutionalized_scientific_exchange` |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `regulated_small_arms`; **REVIEW** `regulated_small_arms`, `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://classiques.uqam.ca/contemporains/minville_esdras/foret/foret_texte.html
- https://parks.canada.ca/lhn-nhs/qc/saintmaurice/culture/histoire-history/site/fer-iron
- https://library-biblio.parl.ca/sites/PublicWebsite/default/en_CA/About/Spotlight/RareBooks/Archives/LaGazettedeQu%C3%A9bec-
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF

### SC1 — Nueva España (Central America)

- **Écarts à l'implémentation actuelle** : ADD 5, REMOVE 0, REVIEW 14; TREE_STRUCTURE_REVIEW 9.
- **ADD** : `permanent_engineer_services`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `medical_degrees`.
- **REVIEW** : `regulated_small_arms`, `armament_standardization_inspection`, `military_topographic_surveying`, `traditional_papermaking`, `improved_agricultural_implements`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `codified_practical_knowledge`, `commercial_insurance_markets`, `specialized_technical_academies`, `systematic_population_registration`, `systematic_cadastral_surveying`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_papermaking`, `traditional_glassmaking`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_glassmaking`, `traditional_furniture_making`; **REVIEW** `traditional_papermaking`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`, `improved_agricultural_implements`; **REVIEW** `improved_agricultural_implements` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | positif: `institutionalized_public_credit`, `commercial_insurance_markets`; **REVIEW** `institutionalized_public_credit`, `commercial_insurance_markets`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`, `systematic_population_registration`, `systematic_cadastral_surveying`; **REVIEW** `systematic_population_registration`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `codified_practical_knowledge` |
| Science/éducation | positif: `institutionalized_scientific_exchange`, `periodical_print_networks`, `specialized_technical_academies`; **REVIEW** `institutionalized_scientific_exchange`, `periodical_print_networks`, `specialized_technical_academies` |
| Médecine | positif: `medical_degrees`; **ADD** `medical_degrees` |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `armament_standardization_inspection`, `military_topographic_surveying`, `permanent_engineer_services`; **ADD** `permanent_engineer_services`; **REVIEW** `regulated_small_arms`, `armament_standardization_inspection`, `military_topographic_surveying`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://ulua.uv.mx/index.php/ulua/article/view/2676
- https://www.cambridge.org/core/journals/journal-of-economic-history/article/building-fiscal-capacity-in-colonial-mexico-from-fragmentation-to-centralization/C1E8886F925D1B83BDF1681AE31FF4E9
- https://gazetademexico.colmex.mx/
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF

### SC2 — Nueva Granada (Gran Colombia)

- **Écarts à l'implémentation actuelle** : ADD 3, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 3.
- **ADD** : `permanent_engineer_services`, `traditional_food_processing`, `traditional_furniture_making`.
- **REVIEW** : `military_topographic_surveying`, `medical_degrees`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `systematic_legal_codification` |
| Science/éducation | positif: `institutionalized_scientific_exchange` |
| Médecine | positif: `medical_degrees`; **REVIEW** `medical_degrees` |
| Militaire | positif: `light_infantry_tactics`, `military_topographic_surveying`, `permanent_engineer_services`; **ADD** `permanent_engineer_services`; **REVIEW** `military_topographic_surveying`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://revistadeindias.revistas.csic.es/index.php/revistadeindias/article/view/1113/0
- https://www.imprenta.gov.co/museodeartesgraficas
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://urosario.edu.co/escuela-de-medicina/la-escuela

### SC3 — Perú (The Andes)

- **Écarts à l'implémentation actuelle** : ADD 4, REMOVE 0, REVIEW 8; TREE_STRUCTURE_REVIEW 5.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `medical_degrees`.
- **REVIEW** : `regulated_small_arms`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `codified_practical_knowledge`, `systematic_population_registration`, `systematic_cadastral_surveying`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_glassmaking`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_glassmaking`, `traditional_furniture_making`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | positif: `institutionalized_public_credit`; **REVIEW** `institutionalized_public_credit`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`, `systematic_population_registration`, `systematic_cadastral_surveying`; **REVIEW** `systematic_population_registration`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `codified_practical_knowledge` |
| Science/éducation | positif: `institutionalized_scientific_exchange`, `periodical_print_networks`; **REVIEW** `institutionalized_scientific_exchange`, `periodical_print_networks` |
| Médecine | positif: `medical_degrees`; **ADD** `medical_degrees` |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `regulated_small_arms`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://whc.unesco.org/en/list/420
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://revistas.pucp.edu.pe/index.php/historica/article/view/7721
- https://medicina.unmsm.edu.pe/resena-historica/

### SC4 — Río de la Plata (La Plata)

Le vice-royaume du Río de la Plata n'est créé que le 1er août 1776; le TAG est donc traité comme proxy géographique/administratif pré-viceregal au cutoff.

- **Écarts à l'implémentation actuelle** : ADD 2, REMOVE 0, REVIEW 2; TREE_STRUCTURE_REVIEW 1.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`.
- **REVIEW** : `organized_textile_production`, `systematic_administrative_statistics`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté; **REVIEW** `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://buenosaires.gob.ar/gcaba_historico/laciudad/calendario-historico/agosto
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://whc.unesco.org/en/list/420
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### SEQ — Indian Territory (Great Plains)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 1.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `improved_husbandry`, `organized_textile_production`, `urbanization`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`; **ADD** `traditional_food_processing`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REVIEW/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.tshaonline.org/handbook/entries/spanish-texas
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/

### SLK — Selk’nam (La Plata)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 2, REVIEW 1; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `improved_husbandry`, `urbanization`.
- **REVIEW** : `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | aucun A/B positif attesté; **REMOVE** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://buenosaires.gob.ar/gcaba_historico/laciudad/calendario-historico/agosto
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### SLS — Séliš (Great Plains)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 1, REVIEW 2; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `urbanization`.
- **REVIEW** : `improved_husbandry`, `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://home.nps.gov/glac/learn/education/intro-to-native-american.htm
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/

### SML — Yat’siminoli (Atlantic Coast)

- **Écarts à l'implémentation actuelle** : ADD 2, REMOVE 0, REVIEW 1; TREE_STRUCTURE_REVIEW 0.
- **ADD** : `traditional_food_processing`, `international_relations`.
- **REVIEW** : `urbanization`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`; **ADD** `traditional_food_processing`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **ADD** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REVIEW/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.floridamuseum.ufl.edu/staugustine/timeline/new-arrivals/
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.rmg.co.uk/collections/archive/rmgc-object-511161

### SPU — South Peru (The Andes)

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 1, REVIEW 4; TREE_STRUCTURE_REVIEW 5.
- **ADD** : `traditional_food_processing`.
- **REMOVE** : `commercial_insurance_markets`.
- **REVIEW** : `regulated_small_arms`, `standardized_field_artillery`, `traditional_glassmaking`, `codified_practical_knowledge`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_glassmaking`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`; **REVIEW** `traditional_glassmaking`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`, `applied_mineralogy`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; **REMOVE** `commercial_insurance_markets`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `codified_practical_knowledge` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | positif: `medical_degrees` |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `regulated_small_arms`, `standardized_field_artillery`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://whc.unesco.org/en/list/420
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://whc.unesco.org/en/tentativelists/6263/
- https://revistas.pucp.edu.pe/index.php/historica/article/view/7721

### TEX — Texas (Great Plains)

Le TAG est interprété comme le Texas espagnol / espace local en 1776, pas comme la république ou l'État du XIXe siècle.

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 4; TREE_STRUCTURE_REVIEW 3.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `regulated_small_arms`, `standardized_field_artillery`, `selective_breeding`, `systematic_administrative_statistics`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`, `selective_breeding`; **REVIEW** `selective_breeding` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté; **REVIEW** `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `regulated_small_arms`, `standardized_field_artillery`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.tshaonline.org/handbook/entries/spanish-texas
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://www.tshaonline.org/handbook/entries/ranching-in-spanish-texas
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### THL — Tehuelche (La Plata)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 1, REVIEW 2; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `urbanization`.
- **REVIEW** : `improved_husbandry`, `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://buenosaires.gob.ar/gcaba_historico/laciudad/calendario-historico/agosto
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/

### UCA — Central America (Central America)

- **Écarts à l'implémentation actuelle** : ADD 2, REMOVE 0, REVIEW 3; TREE_STRUCTURE_REVIEW 1.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`.
- **REVIEW** : `light_infantry_tactics`, `organized_textile_production`, `institutionalized_scientific_exchange`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté; **REVIEW** `institutionalized_scientific_exchange` |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; **REVIEW** `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.ingenieria.unam.mx/historia.php
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://www.nps.gov/saju/learn/historyculture/history.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### URU — Uruguay (Brazil)

Le TAG est interprété comme la Banda Oriental / espace colonial de 1776, pas comme l'État uruguayen ultérieur.

- **Écarts à l'implémentation actuelle** : ADD 1, REMOVE 0, REVIEW 4; TREE_STRUCTURE_REVIEW 3.
- **ADD** : `traditional_food_processing`.
- **REVIEW** : `regulated_small_arms`, `standardized_field_artillery`, `organized_textile_production`, `systematic_administrative_statistics`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `organized_textile_production`, `distillation`; **ADD** `traditional_food_processing`; **REVIEW** `organized_textile_production`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | aucun A/B positif attesté; **REVIEW** `systematic_administrative_statistics` |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`; **REVIEW** `regulated_small_arms`, `standardized_field_artillery`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.fazenda.mg.gov.br/secretaria/historia/
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://arquivodamarinha.marinha.mil.br/index.php/arsenal-de-marinha-do-rio-de-janeiro-4
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem

### USA — America (Atlantic Coast)

Évalué comme réalité des Treize Colonies / structures révolutionnaires **au 1er janvier 1776**, sans importer la Déclaration, les Articles ou les institutions fédérales ultérieures.

- **Écarts à l'implémentation actuelle** : ADD 14, REMOVE 0, REVIEW 11; TREE_STRUCTURE_REVIEW 10.
- **ADD** : `permanent_military_hospitals`, `organized_forestry`, `traditional_food_processing`, `traditional_papermaking`, `improved_agricultural_implements`, `traditional_furniture_making`, `traditional_glassmaking`, `advanced_crop_rotations`, `mechanized_spinning`, `selective_breeding`, `institutionalized_public_credit`, `commercial_insurance_markets`, `variolation_networks`, `organized_elementary_schooling`.
- **REVIEW** : `regulated_small_arms`, `scientific_naval_architecture`, `standardized_field_artillery`, `armament_standardization_inspection`, `sugar_refining`, `systematic_administrative_statistics`, `constitutional_government`, `human_rights`, `national_sovereignty`, `systematic_cadastral_surveying`, `rifling`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_papermaking`, `traditional_glassmaking`, `traditional_furniture_making`, `organized_textile_production`, `distillation`, `sugar_refining`, `mechanized_spinning`; **ADD** `traditional_food_processing`, `traditional_papermaking`, `traditional_glassmaking`, `traditional_furniture_making`, `mechanized_spinning`; **REVIEW** `sugar_refining`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`, `selective_breeding`, `advanced_crop_rotations`, `improved_agricultural_implements`; **ADD** `selective_breeding`, `advanced_crop_rotations`, `improved_agricultural_implements` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | positif: `organized_forestry`; **ADD** `organized_forestry`; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | positif: `institutionalized_public_credit`, `commercial_insurance_markets`; **ADD** `institutionalized_public_credit`, `commercial_insurance_markets`; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_cadastral_surveying`, `codified_practical_knowledge`, `constitutional_government`, `human_rights`, `national_sovereignty`; **REVIEW** `systematic_administrative_statistics`, `systematic_cadastral_surveying`, `constitutional_government`, `human_rights`, `national_sovereignty` |
| Science/éducation | positif: `institutionalized_scientific_exchange`, `periodical_print_networks`, `organized_elementary_schooling`; **ADD** `organized_elementary_schooling` |
| Médecine | positif: `medical_degrees`, `variolation_networks`; **ADD** `variolation_networks` |
| Militaire | positif: `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `armament_standardization_inspection`, `permanent_military_hospitals`; **ADD** `permanent_military_hospitals`; **REVIEW** `regulated_small_arms`, `standardized_field_artillery`, `armament_standardization_inspection`; limites: `horse_artillery` |
| Marine | positif: `scientific_naval_architecture`; **REVIEW** `scientific_naval_architecture`; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT; `rifling`=REVIEW/SECTORAL/CLASSIFICATION_REVIEW |

Sources principales de ce diagnostic :
- https://www.med.upenn.edu/evpdean/perelman-school-of-medicine-history-timeline.html
- https://www.loc.gov/collections/continental-congress-and-constitutional-convention-from-1774-to-1789/articles-and-essays/timeline/1775/
- https://founders.archives.gov/documents/Adams/05-02-02-0007-0001
- https://www.philamuseum.org/exhibitions/the-fix-on-colonial-philadelphia-furniture-a-secret-guide-to-cabinetmakers-prices

### UTE — Ute (Pacific Coast)

- **Écarts à l'implémentation actuelle** : ADD 0, REMOVE 1, REVIEW 2; TREE_STRUCTURE_REVIEW 0.
- **REMOVE** : `urbanization`.
- **REVIEW** : `improved_husbandry`, `international_relations`.

| Domaine | Diagnostic |
|---|---|
| Production | aucun A/B positif attesté; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry`; **REVIEW** `improved_husbandry` |
| Mines/métallurgie | aucun A/B positif attesté; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté; **REVIEW** `international_relations` |
| Administration | aucun A/B positif attesté |
| Science/éducation | aucun A/B positif attesté |
| Médecine | aucun A/B positif attesté |
| Militaire | aucun A/B positif attesté; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=REMOVE/ABSENT |

Sources principales de ce diagnostic :
- https://home.nps.gov/glac/learn/education/intro-to-native-american.htm
- https://www.nps.gov/articles/comanches-and-horses.htm
- https://www.rmg.co.uk/stories/topics/harrison-clocks-longitude-problem
- https://www.lr.org/en/about-us/who-we-are/our-history/

### VNZ — Venezuela (Gran Colombia)

- **Écarts à l'implémentation actuelle** : ADD 3, REMOVE 0, REVIEW 5; TREE_STRUCTURE_REVIEW 2.
- **ADD** : `traditional_food_processing`, `traditional_furniture_making`, `medical_degrees`.
- **REVIEW** : `organized_textile_production`, `shaft_mining`, `sugar_refining`, `institutionalized_scientific_exchange`, `systematic_legal_codification`.

| Domaine | Diagnostic |
|---|---|
| Production | positif: `traditional_food_processing`, `traditional_furniture_making`, `organized_textile_production`, `distillation`, `sugar_refining`; **ADD** `traditional_food_processing`, `traditional_furniture_making`; **REVIEW** `organized_textile_production`, `sugar_refining`; limites: `industrial_acids`, `mechanized_weaving`, `advanced_spinning` |
| Agriculture | positif: `improved_husbandry` |
| Mines/métallurgie | positif: `shaft_mining`; **REVIEW** `shaft_mining`; limites: `coke_smelting`, `atmospheric_engine`, `precision_boring`, `condensing_steam_engines` |
| Infrastructure | aucun A/B positif attesté; limites: `turnpike_road_networks`, `industrial_canals` |
| Finance et économie | aucun A/B positif attesté; limites: `stock_exchange`, `classical_political_economy` |
| Commerce | aucun A/B positif attesté |
| Administration | positif: `systematic_administrative_statistics`; **REVIEW** `systematic_legal_codification` |
| Science/éducation | aucun A/B positif attesté; **REVIEW** `institutionalized_scientific_exchange` |
| Médecine | positif: `medical_degrees`; **ADD** `medical_degrees` |
| Militaire | positif: `light_infantry_tactics`; limites: `horse_artillery` |
| Marine | aucun A/B positif attesté; limites: `marine_chronometry`, `ship_classification_surveying`, `copper_sheathing` |
| E/C examinées | `urbanization`=KEEP/ABSTRACT; `colonization`=KEEP/ABSTRACT |

Sources principales de ce diagnostic :
- https://www.imprenta.gov.co/museodeartesgraficas
- https://www.cambridge.org/core/books/cambridge-economic-history-of-the-modern-world/latin-america-17001870/C8AEB15FB4841B919B5827F7847FC0CF
- https://revista.svhm.org.ve/ediciones/2019/1-2/art-4
- https://whc.unesco.org/en/list/420

## 15. TREE_STRUCTURE_REVIEW

Le fait historique est décidé **avant** l'arbre. Résultat : **122 relations** nécessitent une révision structurelle parce que la capacité est historiquement plausible/établie alors qu'un parent n'est pas justifié localement ou représente une autre institution. **19 relations** sont des `ADD_WITH_PREREQUISITES` : l'enfant et les parents sont historiquement plausibles.

| Technologie | TREE_STRUCTURE_REVIEW |
|---|---:|
| `light_infantry_tactics` | 37 |
| `standardized_field_artillery` | 20 |
| `regulated_small_arms` | 16 |
| `codified_practical_knowledge` | 12 |
| `medical_degrees` | 11 |
| `permanent_engineer_services` | 6 |
| `armament_standardization_inspection` | 4 |
| `commercial_insurance_markets` | 4 |
| `permanent_military_hospitals` | 2 |
| `applied_mineralogy` | 2 |
| `specialized_technical_academies` | 2 |
| `scientific_naval_architecture` | 2 |
| `human_rights` | 1 |
| `national_sovereignty` | 1 |
| `systematic_cadastral_surveying` | 1 |
| `rifling` | 1 |

Cas prioritaires :

- `medical_degrees` : les facultés/grades de Mexico, Lima, Quito, La Havane, Saint-Domingue, Caracas et Santiago ne doivent pas être supprimés parce que `institutionalized_scientific_exchange` serait absent ou trop étroitement interprété.
- `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery` : plusieurs capacités militaires existent localement sans que toutes les chaînes d'académies/fortifications de l'arbre soient institutionnellement équivalentes.
- `permanent_engineer_services` : les ingénieurs militaires espagnols de Cuba, Porto Rico, Nouvelle-Espagne et Nouvelle-Grenade peuvent être attestés indépendamment d'autres nœuds militaires.
- **Nouvelle règle forestière** : `traditional_papermaking`, `traditional_glassmaking` et `traditional_furniture_making` ne sont plus bloqués par `organized_forestry`; ces trois anciennes dettes de prérequis sont donc intentionnellement ignorées dans la seconde passe.

`ADD_WITH_PREREQUISITES` par technologie :

| Technologie | Nombre |
|---|---:|
| `sugar_refining` | 9 |
| `military_topographic_surveying` | 6 |
| `medical_degrees` | 1 |
| `scientific_naval_architecture` | 1 |
| `advanced_crop_rotations` | 1 |
| `commercial_insurance_markets` | 1 |

## 16. CLASSIFICATION_REVIEW

### 16.1 `CLASSIFICATION_TOO_EARLY`

Quatre nœuds ont un contenu gameplay trop tardif par rapport à leur classement A/B actuel. Le flag est répété pour chaque TAG afin que la matrice soit exhaustive; il s'agit de **4 problèmes de classification globaux**, pas de 228 inventions indépendantes.

| Technologie | Classe actuelle | Problème | Lignes flaggées |
|---|:---:|---|---:|
| `industrial_acids` | A | Débloque chemical plant/chemical works/explosives factory; le bundle dépasse très largement les acides artisanaux pré-1776. | 57 |
| `sugar_refining` | A | Le nœud débloque centrifugation, betterave, évaporation vapeur et vacuum pan; le raffinage colonial traditionnel ne suffit pas. | 57 |
| `mechanized_weaving` | B | Le contenu `pm_mechanized_looms` correspond à la mécanisation/power loom postérieure au cutoff. | 57 |
| `advanced_spinning` | B | Le nœud débloque `pm_sewing_machines`, clairement postérieur à 1776. | 57 |

### 16.2 `CLASSIFICATION_TOO_LATE`

`medical_degrees` est classée B, mais les institutions de grades médicaux sont déjà anciennes dans plusieurs territoires. TAG flaggés : `CUB`, `ECU`, `GR5`, `MEX`, `NPU`, `PEU`, `SC1`, `SC3`, `SPU`.

### 16.3 `CLASSIFICATION_REVIEW`

- **`USA` — `rifling`** : Des compagnies de riflemen sont levées par le Congrès dès juin 1775 et le long rifle rayé est effectivement employé; cela contredit une lecture simple de `rifling` comme uniquement post-1776. Le nœud gameplay peut toutefois représenter la généralisation industrielle du fusil rayé, donc CLASSIFICATION_REVIEW plutôt qu'ADD. Sources : https://www.nps.gov/sara/learn/historyculture/daniel-morgan.htm ; https://www.loc.gov/collections/continental-congress-and-constitutional-convention-from-1774-to-1789/articles-and-essays/timeline/1775/.

## 17. Principales différences avec la première passe

La seconde passe ne se contente pas de patcher les technologies présentes : elle transforme l'unité d'analyse en **capacité historique × pays**. Les différences principales sont :

1. passage de 579 relations sélectives dans la première matrice régionale à **3 763 relations** ici;
2. audit obligatoire des **61 A/B** pour chacun des 57 TAG;
3. baseline `Current_Status` prise après synthèse mondiale (`Final_Technologies`), pas depuis les vieux tiers;
4. découplage complet papier/verre/meuble de `organized_forestry`;
5. finance réévaluée : crédit public ≠ assurance ≠ bourse;
6. médecine réévaluée comme institution historique de grades/certification;
7. retrait de compatibilités artificielles `urbanization`/`improved_husbandry` dans plusieurs espaces autochtones;
8. signalement des nœuds dont le **bundle gameplay** est plus tardif que le nom générique;
9. séparation plus stricte entre capacités locales coloniales et capacités de la métropole.

### 20 changements les plus importants par rapport à la distribution actuellement implémentée

| # | Pays / groupe | Technologie | Changement | Motif |
|---:|---|---|---|---|
| 1 | Région entière | `traditional_food_processing` | ADD pour 43 TAG | La première passe sous-évaluait le socle d'ateliers/moulins/transformation alimentaire; le second passage l'évalue indépendamment du tier. |
| 2 | Région entière | `traditional_furniture_making` | ADD pour 21 TAG | La fabrication organisée de meubles est désormais indépendante de `organized_forestry`; des centres coloniaux urbains/artisanaux deviennent positifs. |
| 3 | 16 TAG autochtones/territoriaux | `urbanization` | REMOVE pour 16 TAG | Le nœud débloque centre urbain + secteur de construction; la compatibilité de première passe est retirée lorsqu'elle ne correspond pas à la réalité locale. |
| 4 | ALK, ATB, IRC, SLK | `improved_husbandry` | REMOVE pour 4 TAG | La simple subsistance/chasse ou présence animale ne suffit plus à représenter l'élevage amélioré. |
| 5 | CHL, CLM, NPU, SPU | `commercial_insurance_markets` | REMOVE pour 4 TAG | Le commerce colonial n'est plus assimilé automatiquement à un marché local d'assurance institutionnalisé. |
| 6 | USA | `institutionalized_public_credit` | ADD — HIGH | Finances provinciales, émissions/crédit public et financement militaire sont institutionnalisés avant 1776. |
| 7 | USA | `commercial_insurance_markets` | ADD — HIGH | Assurance maritime/commerciale effectivement organisée à Philadelphie/Boston avant le cutoff. |
| 8 | USA | `traditional_papermaking` | ADD — HIGH | 26 moulins à papier recensés dans les Treize Colonies en 1769, forte concentration autour de Philadelphie. |
| 9 | USA | `traditional_glassmaking` | ADD — HIGH | La verrerie coloniale est réellement implantée avant 1776; le nouveau découplage forestier enlève un faux obstacle. |
| 10 | USA | `organized_elementary_schooling` | ADD — HIGH | Des colonies de Nouvelle-Angleterre ont des obligations scolaires institutionnalisées bien avant 1776. |
| 11 | USA | `variolation_networks` | ADD — HIGH | La variolisation est pratiquée et diffusée dans les colonies avant 1776, sans être confondue avec la vaccination ultérieure. |
| 12 | USA | `mechanized_spinning` | ADD — MEDIUM / FRONTIER | La mécanisation précoce du filage apparaît comme capacité de frontière; maintien prudent, sans attribuer le power loom. |
| 13 | NVS | `state_dockyard_systems` | ADD — HIGH | Halifax possède un système de dockyard impérial effectivement déployé localement. |
| 14 | NVS | `periodical_print_networks` | ADD — HIGH | La presse/gazette de Halifax est établie avant 1776. |
| 15 | QUE | `organized_forestry` | ADD — MEDIUM / SECTORAL | L'approvisionnement forestier est organisé à l'échelle coloniale; décision désormais fondée sur l'exploitation rationalisée, non sur le simple logging. |
| 16 | CUB | `medical_degrees` | ADD — HIGH + CLASSIFICATION_TOO_LATE | Faculté de médecine et grades de licencié/docteur à La Havane dès 1728. |
| 17 | CUB | `scientific_naval_architecture` | ADD — HIGH / SECTORAL | Le grand chantier de La Havane construit localement des navires de guerre et mobilise un savoir de conception navale. |
| 18 | MEX + SC1 | `medical_degrees` | ADD — HIGH + CLASSIFICATION_TOO_LATE | La formation et les grades médicaux de Nouvelle-Espagne sont antérieurs au cutoff; le nœud B est trop tardif pour ce contexte. |
| 19 | CHL | `variolation_networks` | ADD — HIGH / SECTORAL | Environ 5 000 inoculations attribuées à Chaparro à partir de 1765 rendent le réseau/pratique locale clairement pré-1776. |
| 20 | BRZ | `organized_forestry + scientific_naval_architecture` | ADD — HIGH | Le bois royal organisé et l'Arsenal de Rio montrent des capacités locales distinctes de la seule technologie théorique portugaise. |

## 18. Recommandations finales

1. **Ne pas implémenter mécaniquement tous les `REVIEW`.** Les 110 `ADD` et 24 `REMOVE` sont les écarts affirmatifs; les 227 `REVIEW` doivent être arbitrés lors de la synthèse mondiale.
2. **Traiter d'abord les problèmes de classification globaux** (`industrial_acids`, `sugar_refining`, `mechanized_weaving`, `advanced_spinning`, puis `medical_degrees` et `rifling`) avant une nouvelle implémentation nationale; sinon la distribution continuera à compenser un mauvais découpage d'arbre.
3. **Résoudre les TREE_STRUCTURE_REVIEW séparément.** Une dette de prérequis ne doit jamais annuler une capacité historiquement établie.
4. **Conserver l'asymétrie coloniale.** La Havane, Halifax, Rio, Mexico, Lima ou Québec peuvent disposer de capacités très avancées dans un domaine sans recevoir le portefeuille technologique de Madrid, Londres, Lisbonne ou Paris.
5. **Conserver la date absolue 1776-01-01.** Aucun développement plus tardif de 1776 n'est rétro-projeté, en particulier pour les institutions américaines et le vice-royaume du Río de la Plata.

## Contrôle final

- TAG : **57**.
- Technologies A auditées : **25**.
- Technologies B auditées : **36**.
- Lignes totales : **3763**.
- ADD : **110**.
- REMOVE : **24**.
- KEEP : **3402**.
- REVIEW : **227**.
- TREE_STRUCTURE_REVIEW : **122**.
- CLASSIFICATION_REVIEW : **1**.
- CLASSIFICATION_TOO_EARLY : **228** lignes, représentant 4 technologies globales.
- CLASSIFICATION_TOO_LATE : **9** lignes (`medical_degrees`).
- Aucun fichier gameplay modifié.
- Aucun code produit.
- Aucun commit.
- Aucun push.
