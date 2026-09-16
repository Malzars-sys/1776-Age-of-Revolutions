# Recherche technologique — Afrique — SECOND PASS FULL — 1er janvier 1776

## 1. Périmètre

Cette seconde passe couvre **161 TAG africains** des régions `North Africa`, `West Africa`, `Equatorial Africa`, `East Africa`, `Southern Africa` et `Nile Basin`, en excluant explicitement `EGY`. Elle audite chaque relation TAG × technologie A/B, puis les technologies E à effet gameplay direct/significatif.

- **East Africa (58)** : `ACH` Acholi, `AGC` Angoche, `AJR` Ajuran, `ANK` Ankole, `ANU` Anuak, `ARS` Arsiland, `AUL` Aulihan, `AWS` Aussa, `BGM` Begemder, `BMB` Bemba, `BNY` Bunyoro, `BRD` Burundi, `BRN` Borana, `BUG` Buganda, `ETH` Ethiopia, `GGO` Gogo, `GJM` Gojjam, `GLD` Geledi, `GZA` Gaza, `HAR` Harar, `HDY` Hadiya, `HHE` Hehe, `ISQ` Isaaq, `KFA` Kaffa, `KKY` Kikuyu, `KRG` Karagwe, `KZM` Kazembe, `LUO` Luo, `LZO` Barotse, `MAD` Madagascar, `MBS` Mombasa, `MJK` Mijikenda, `MJT` Majerteen, `MNC` Manica, `MRV` Maravi, `MSH` Mashona, `MSI` Masai, `MSK` Maseko, `MTB` Ndebele, `MTP` Mutapa, `NYM` Unyamwezi, `OGD` Ogaden, `OMO` Omo, `ORM` Orma, `QWR` Qwara, `RWD` Rwanda, `SDM` Sidamo, `SHW` Shewa, `SKM` Usukuma, `SKY` Sakuye, `SNG` Sangu, `TGI` Tungi, `TGR` Tigray, `TRK` Turkana, `WLG` Welega, `WLT` Wolaita, `WSG` Warsangali, `WTU` Witu
- **Equatorial Africa (23)** : `BGI` Bagirmi, `BMM` Bamum, `BNG` Bangala, `BOB` Bobangi, `CHK` Chokwe, `DAK` Dar al Kuti, `DLA` Duala, `FNG` Fang, `HMB` Hemba, `KBA` Kuba, `KON` Kongo, `KSN` Kasanje, `LBA` Luba, `LGA` Lega, `LND` Lunda, `LNG` Loango, `MNB` Mangbetu, `OVM` Ovimbundu, `TBI` Tubu, `TKE` Teke, `WAD` Wadai, `YKA` Yaka, `ZND` Azande
- **Nile Basin (6)** : `DFR` Darfur, `DFT` Dar Fertit, `DNK` Dinka, `NUE` Nuer, `SD1` The Sudan, `TPS` Toposa
- **North Africa (18)** : `AHG` Kel Ahaggar, `AIT` Ait Abbas, `AJJ` Kel Ajjer, `CMB` Chaamba, `CON` Constantine, `DLM` Delim, `FZN` Fezzan, `MAS` Mascara, `MOR` Morocco, `MZB` Mzab, `RGB` Reguibat, `SAH` Sahrawi, `TEK` Tekna, `TRI` Tripolitania, `TUA` Tuat, `TUG` Touggourt, `TUN` Tunis, `ZWY` Zuwayya
- **Southern Africa (16)** : `BST` Basutoland, `HRO` Herero, `NAM` Nama, `ORA` Oranje, `OVB` Ovambo, `PDI` Pedi, `PHL` Philippolis, `SAF` South Africa, `SAN` San, `SWZ` Swaziland, `TRN` Transvaal, `TSW` Tswana, `VND` Venda, `WBL` Griqualand, `XHO` Xhosa, `ZUL` Zulu
- **West Africa (40)** : `ADG` Kel Adagh, `ADR` Adrar, `AIR` Kel Air, `ASH` Ashanti, `ATR` Kel Ataram, `AYI` Anyi, `BEN` Benin, `BLE` Baule, `BND` Bundu, `BOR` Bornu, `BRG` Borgu, `BRK` Brakna, `CAY` Cayor, `DAH` Dahomey, `DIN` Kel Dinnik, `DIO` Diola, `EWE` Ewe, `FTJ` Futa Jallon, `FTR` Futa Toro, `HAU` Gobir, `IBO` Igbo, `JLF` Jolof, `KBD` Kabadougou, `KBU` Kaabu, `KNG` Kong, `KRT` Kaarta, `KRU` Kru, `LIB` Liberia, `MDK` Mandinka, `MOS` Mossi, `MSN` Massina, `OUA` Tagant, `OYO` Oyo, `SGU` Segou, `SIL` Sierra Leone, `SOK` Sokoto, `SRR` Serer, `SSU` Susu, `TMN` Temne, `TRZ` Trarza

**Note de baseline.** Les fichiers techniques joints décrivent l’état avant la première matrice Afrique. Pour représenter la “distribution actuellement implémentée” de la seconde passe, `Current_Status` est reconstruit à partir de cette distribution + des décisions de la matrice Afrique précédente, en supposant que les `ADD/KEEP/REMOVE` ont été implémentés et que les `REVIEW` sont restés inchangés. Si l’implémentation mondiale a divergé de cette matrice, il faudra régénérer uniquement la colonne `Current_Status` avant merge final.


## 2. Sources et méthode

Méthode : (1) déterminer la capacité historique indépendamment du tier et des prérequis ; (2) seulement ensuite comparer au statut actuel ; (3) qualifier les incohérences de l’arbre. Les conclusions conservatrices distinguent utilisation/importation d’une technologie, production locale, diffusion sectorielle et institutionnalisation nationale.

Sources structurantes :
- https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5
- https://www.cambridge.org/core/journals/annales-histoire-sciences-sociales/article/abs/esclaves-chretiens-et-esclaves-noirs-a-tunis-au-xviiie-siecle/B6D63DDA1CDEE63BFF2CE876BB6F3657
- https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/decline-or-survival-iron-production-in-west-africa-from-the-seventeenth-to-the-twentieth-centuries/DB53AF615BFC1FB0B7F677C61059517A
- https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- https://www.cambridge.org/core/journals/history-in-africa/article/abs/what-africans-got-for-their-slaves-a-master-list-of-european-trade-goods1/DAD83A839DB71F6AF2E44A9A9E455543
- https://www.cambridge.org/core/journals/africa/article/abs/financing-of-the-ashanti-expansion-17001820/D6DBF0405E655EE438E72591646E2D14
- https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/continuity-revolution-or-evolution-on-the-slave-coast-of-west-africa-royal-architecture-and-political-order-in-precolonial-dahomey/9161CAD3798C67BD6D61BB0AEBB3CB44
- https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/firearms-in-the-central-sudan/6E62EDB849B9F16A83DEB9A956EC11A9
- https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/smallpox-inoculation-in-africa/E43D8B3146D1EC4649699AD758E3B37A
- https://makingscience.royalsociety.org/items/rbo_14_18/paper-relating-to-the-inoculation-of-smallpox-as-it-is-practised-in-the-kingdoms-of-tripoli-tunis-and-algiers
- https://www.cambridge.org/core/journals/annales-histoire-sciences-sociales/article/abs/lautorite-de-lecrit-pragmatique-dans-la-societe-chretienne-ethiopienne-xvexviiie-siecle/6A051E194A4F22B1EB0BDCA8566FF48F
- https://www.cambridge.org/core/books/abs/inbetween-textiles-14001800/globalisation-and-the-manufacture-of-tabletwoven-sanctuary-curtains-in-ethiopia-in-the-eighteenth-century/4E9B2B7EFC904C677A18D7AB588E1CFD
- https://assets.cambridge.org/052183/9351/excerpt/0521839351_excerpt.htm
- https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/riziculture-and-the-founding-of-monarchy-in-imerina/655827178C79752D51106C976FC550D2
- https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- https://sahistory.org.za/archive/african-farmers-southern-africa
- https://www.cambridge.org/core/journals/international-review-of-social-history/article/economics-of-slavery-in-the-eighteenthcentury-cape-colony-revising-the-nieboerdomar-hypothesis/B7EB0A6EC343E570F6D339D8BB1EAC2F
- https://www.cambridge.org/core/journals/journal-of-wine-economics/article/slave-labor-productivity-and-wine-output-stellenbosch-16801828/1220D349D6DEE842C7BD7C9DC0DCA97C
- https://sahistory.org.za/place/simons-town-cape-peninsula
- https://pmc.ncbi.nlm.nih.gov/articles/PMC13110399/
- https://www.cambridge.org/core/books/medicine-and-power-in-tunisia-17801900/colonization-and-collapse-of-arab-medical-institutions/D7F157787E097C6A2E40FF5F9B7E1A2D

## 3. Production

- **`traditional_food_processing`** — KEEP 9, ADD 107, REMOVE 0, REVIEW 45. Point saillant : La transformation domestique est certaine, mais l’échelle d’ateliers/manufactures correspondant au bâtiment gameplay reste incertaine.
- **`traditional_papermaking`** — KEEP 158, ADD 0, REMOVE 0, REVIEW 3. Point saillant : Usage de papier ou culture manuscrite ne signifie pas fabrication locale; dans de nombreuses régions le papier est importé.
- **`traditional_glassmaking`** — KEEP 154, ADD 5, REMOVE 0, REVIEW 2. Point saillant : Le verre est souvent importé, travaillé ou refondu; cela ne démontre pas une verrerie locale complète.
- **`traditional_furniture_making`** — KEEP 31, ADD 89, REMOVE 0, REVIEW 41. Point saillant : Le travail du bois est établi, mais l’échelle manufacturière du bâtiment de meubles reste difficile à fixer.
- **`organized_textile_production`** — KEEP 76, ADD 34, REMOVE 4, REVIEW 47. Point saillant : Des fibres, vêtements et métiers artisanaux existent, mais l’échelle d’une production textile organisée correspondant au bâtiment textile reste incertaine.
- **`distillation`** — KEEP 87, ADD 26, REMOVE 6, REVIEW 42. Point saillant : Pas de preuve suffisante d’une distillation locale organisée à l’échelle du nœud.
- **`sugar_refining`** — KEEP 160, ADD 0, REMOVE 0, REVIEW 1. Point saillant : Pas de raffinage du sucre local suffisamment établi au seuil industriel représenté par le PM.
- **`industrial_acids`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Aucune diffusion locale attestée en Afrique au 1er janvier 1776 au niveau industriel/technique représenté par ce nœud.
- **`mechanized_spinning`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Aucune diffusion locale attestée en Afrique au 1er janvier 1776 au niveau industriel/technique représenté par ce nœud.
- **`mechanized_weaving`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Aucune diffusion locale attestée en Afrique au 1er janvier 1776 au niveau industriel/technique représenté par ce nœud.
- **`advanced_spinning`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Aucune diffusion locale attestée en Afrique au 1er janvier 1776 au niveau industriel/technique représenté par ce nœud.

**Conclusion production.** La deuxième passe ajoute largement les capacités artisanales réellement attestées (`traditional_food_processing`, mobilier, textile) tout en refusant de confondre importations de verre/papier avec fabrication locale. La suppression du lien historique artificiel avec `organized_forestry` permet notamment d’attribuer mobilier/papier/verre indépendamment lorsque les preuves l’exigent.

## 4. Agriculture

- **`improved_husbandry`** — KEEP 160, ADD 0, REMOVE 0, REVIEW 1. Point saillant : Agriculture ou pastoralisme spécialisés sont structurels; ici le nœud est interprété comme socle productif préindustriel, sans supposer une révolution agricole européenne.
- **`selective_breeding`** — KEEP 149, ADD 0, REMOVE 0, REVIEW 12. Point saillant : Élevage important ne prouve pas une sélection organisée au seuil de cette technologie frontière.
- **`advanced_crop_rotations`** — KEEP 160, ADD 0, REMOVE 0, REVIEW 1. Point saillant : Interculture, jachère ou itinérance culturale ne sont pas automatiquement la rotation avancée représentée par le nœud.
- **`improved_agricultural_implements`** — KEEP 63, ADD 73, REMOVE 0, REVIEW 25. Point saillant : L’existence de l’agriculture seule ne suffit pas; preuve insuffisante de l’outillage amélioré représenté par ce nœud.

**Conclusion agriculture.** `improved_husbandry` reste un socle gameplay large, mais `improved_agricultural_implements`, `selective_breeding` et les rotations avancées sont traités séparément : agriculture existante ≠ outils améliorés ≠ sélection systématique.

## 5. Mines/métallurgie

- **`shaft_mining`** — KEEP 110, ADD 4, REMOVE 39, REVIEW 8. Point saillant : La présence de métallurgie ou d’extraction de surface ne suffit pas à établir des techniques de puits miniers avancées correspondant au nœud.
- **`applied_mineralogy`** — KEEP 157, ADD 0, REMOVE 0, REVIEW 4. Point saillant : Aucune preuve d’une pratique minéralogique systématique équivalente au nœud au 1er janvier 1776.
- **`coke_smelting`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Aucune diffusion locale attestée en Afrique au 1er janvier 1776 au niveau industriel/technique représenté par ce nœud.
- **`atmospheric_engine`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Aucune diffusion locale attestée en Afrique au 1er janvier 1776 au niveau industriel/technique représenté par ce nœud.
- **`precision_boring`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Aucune diffusion locale attestée en Afrique au 1er janvier 1776 au niveau industriel/technique représenté par ce nœud.
- **`condensing_steam_engines`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Aucune diffusion locale attestée en Afrique au 1er janvier 1776 au niveau industriel/technique représenté par ce nœud.

**Conclusion mines.** La métallurgie du fer africaine est prise au sérieux, mais elle ne justifie pas automatiquement `shaft_mining`. Le second passage réduit fortement ce dernier aux zones où les travaux souterrains sont réellement plausibles/attestés et laisse `applied_mineralogy` presque toujours en REVIEW/ABSENT.

## 6. Infrastructure

- **`turnpike_road_networks`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Routes, pistes caravanières et corvées d’entretien n’équivalent pas à un réseau de routes à péage/turnpike institutionnalisé.
- **`industrial_canals`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Aucune diffusion locale attestée en Afrique au 1er janvier 1776 au niveau industriel/technique représenté par ce nœud.
- **`organized_forestry`** — KEEP 157, ADD 0, REMOVE 0, REVIEW 4. Point saillant : La coupe et le commerce du bois ne démontrent pas une exploitation forestière organisée/rationalisée; la nouvelle définition du nœud impose un seuil plus élevé.

## 7. Finance

- **`institutionalized_public_credit`** — KEEP 157, ADD 0, REMOVE 0, REVIEW 4. Point saillant : Tribut, prêts privés et trésor royal ne suffisent pas à établir un système institutionnalisé de crédit public.
- **`commercial_insurance_markets`** — KEEP 155, ADD 0, REMOVE 0, REVIEW 6. Point saillant : Aucune preuve d’un marché d’assurance commerciale institutionnalisé correspondant au nœud.
- **`stock_exchange`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Marchés, foires et crédit marchand ne constituent pas une bourse institutionnalisée au sens du nœud.
- **`political_economy`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : La capacité gameplay renvoie à une doctrine/institution d’économie politique formalisée, non à la seule sophistication commerciale ou fiscale.
- **`classical_political_economy`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : La capacité gameplay renvoie à une doctrine/institution d’économie politique formalisée, non à la seule sophistication commerciale ou fiscale.

**Conclusion finance.** Commerce, tribut, crédit privé et fiscalité ne sont pas assimilés à une dette publique institutionnalisée, à l’assurance marchande ou à une bourse. Les régences maghrébines restent REVIEW pour `institutionalized_public_credit`/assurance plutôt que recevoir automatiquement les institutions européennes de finance publique.

## 8. Commerce

- **`international_relations`** — KEEP 113, ADD 43, REMOVE 0, REVIEW 5. Point saillant : Relations commerciales occasionnelles ne suffisent pas à établir une capacité diplomatique institutionnalisée au niveau du nœud.
- **`commercial_insurance_markets`** — KEEP 155, ADD 0, REMOVE 0, REVIEW 6. Point saillant : Aucune preuve d’un marché d’assurance commerciale institutionnalisé correspondant au nœud.
- **`institutionalized_public_credit`** — KEEP 157, ADD 0, REMOVE 0, REVIEW 4. Point saillant : Tribut, prêts privés et trésor royal ne suffisent pas à établir un système institutionnalisé de crédit public.
- **`stock_exchange`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Marchés, foires et crédit marchand ne constituent pas une bourse institutionnalisée au sens du nœud.

## 9. Administration

- **`systematic_administrative_statistics`** — KEEP 114, ADD 1, REMOVE 37, REVIEW 9. Point saillant : Administration ou tribut ne suffisent pas à démontrer des statistiques d’État systématiques.
- **`systematic_population_registration`** — KEEP 156, ADD 1, REMOVE 0, REVIEW 4. Point saillant : Pas de preuve de registres de population systématiques correspondant au nœud.
- **`systematic_cadastral_surveying`** — KEEP 160, ADD 0, REMOVE 0, REVIEW 1. Point saillant : Mesure locale des terres ou droits coutumiers ne démontrent pas un levé cadastral systématique.
- **`systematic_legal_codification`** — KEEP 154, ADD 1, REMOVE 0, REVIEW 6. Point saillant : Pas de preuve d’une codification juridique systématique correspondant au nœud.
- **`codified_practical_knowledge`** — KEEP 102, ADD 1, REMOVE 33, REVIEW 25. Point saillant : Les savoirs artisanaux transmis oralement ne suffisent pas, à eux seuls, à établir le nœud de savoirs codifiés.

## 10. Science/éducation

- **`institutionalized_scientific_exchange`** — KEEP 143, ADD 8, REMOVE 0, REVIEW 10. Point saillant : Pas de preuve suffisante d’un réseau institutionnalisé d’échanges savants correspondant au nœud.
- **`periodical_print_networks`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Aucun réseau local de presse périodique comparable au nœud n’est établi en Afrique au 1er janvier 1776.
- **`specialized_technical_academies`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Pas d’académie technique spécialisée correspondant au bâtiment université et à la formation technique institutionnelle du nœud en 1776.
- **`organized_elementary_schooling`** — KEEP 124, ADD 7, REMOVE 0, REVIEW 30. Point saillant : Pas de preuve d’un réseau d’enseignement élémentaire organisé correspondant au nœud.
- **`veterinary_science`** — KEEP 157, ADD 0, REMOVE 0, REVIEW 4. Point saillant : Savoirs empiriques d’élevage ne suffisent pas à établir une science vétérinaire institutionnalisée.

## 11. Médecine

- **`medical_degrees`** — KEEP 156, ADD 2, REMOVE 0, REVIEW 3. Point saillant : Médecine traditionnelle ou praticiens de cour ne suffisent pas à établir facultés/collèges/titres médicaux reconnus au sens du nœud.
- **`variolation_networks`** — KEEP 111, ADD 34, REMOVE 0, REVIEW 16. Point saillant : Aucune preuve suffisamment localisée d’un réseau de variolisation en 1776.

**Conclusion médecine.** La variolisation est la principale correction africaine de la seconde passe : l’historiographie la documente dans le Soudan occidental/central, en Éthiopie et en Afrique australe. `medical_degrees` est ajouté au Maroc et à Tunis sous une lecture pré-moderne de l’ijaza/certification médicale, avec `CLASSIFICATION_TOO_LATE` pour le classement B.

## 12. Militaire

- **`scientific_fortification_siegecraft`** — KEEP 154, ADD 2, REMOVE 0, REVIEW 5. Point saillant : Fortifications vernaculaires ou palissades seules ne suffisent pas au seuil scientifique/artillerie du nœud.
- **`regulated_small_arms`** — KEEP 157, ADD 1, REMOVE 2, REVIEW 1. Point saillant : L’usage ou l’importation massive d’armes à feu ne suffit pas : absence de preuve d’une industrie locale réglementée d’armes complètes/artillerie.
- **`light_infantry_tactics`** — KEEP 153, ADD 0, REMOVE 2, REVIEW 6. Point saillant : Aucune preuve d’une doctrine d’infanterie légère institutionnalisée correspondant au nœud.
- **`standardized_field_artillery`** — KEEP 155, ADD 3, REMOVE 2, REVIEW 1. Point saillant : Possession de quelques canons ne vaut pas système d’artillerie de campagne standardisé.
- **`armament_standardization_inspection`** — KEEP 157, ADD 0, REMOVE 0, REVIEW 4. Point saillant : Pas de système attesté de normes et inspection d’armement correspondant au nœud.
- **`horse_artillery`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Technologie frontière très spécialisée; aucune implantation locale suffisamment établie dans ce TAG africain au 1er janvier 1776.
- **`military_topographic_surveying`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Technologie frontière très spécialisée; aucune implantation locale suffisamment établie dans ce TAG africain au 1er janvier 1776.
- **`permanent_engineer_services`** — KEEP 156, ADD 0, REMOVE 0, REVIEW 5. Point saillant : Aucune preuve d’un corps permanent du génie militaire.
- **`permanent_military_hospitals`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Technologie frontière très spécialisée; aucune implantation locale suffisamment établie dans ce TAG africain au 1er janvier 1776.

## 13. Marine

- **`enclosed_dock_systems`** — KEEP 156, ADD 0, REMOVE 1, REVIEW 4. Point saillant : Un port, mouillage ou chantier naval ne suffit pas à démontrer un système de bassins fermés.
- **`state_dockyard_systems`** — KEEP 157, ADD 1, REMOVE 0, REVIEW 3. Point saillant : Navigation ou construction de boutres ne suffisent pas à établir un système d’arsenaux d’État.
- **`scientific_naval_architecture`** — KEEP 157, ADD 0, REMOVE 0, REVIEW 4. Point saillant : Savoir-faire de construction navale traditionnel ou réparation ne suffit pas à l’architecture navale scientifique du nœud.
- **`marine_chronometry`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Technologie frontière très spécialisée; aucune implantation locale suffisamment établie dans ce TAG africain au 1er janvier 1776.
- **`ship_classification_surveying`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Technologie frontière très spécialisée; aucune implantation locale suffisamment établie dans ce TAG africain au 1er janvier 1776.
- **`copper_sheathing`** — KEEP 161, ADD 0, REMOVE 0, REVIEW 0. Point saillant : Technologie frontière très spécialisée; aucune implantation locale suffisamment établie dans ce TAG africain au 1er janvier 1776.

## 14. Analyse pays par pays

Le détail exhaustif est dans le CSV (une ligne par technologie). Tableau de synthèse des écarts non triviaux :

| TAG | Pays | Région | ADD | REMOVE | REVIEW | Principaux changements |
|---|---|---|---:|---:|---:|---|
| `ACH` | Acholi | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `ADG` | Kel Adagh | West Africa | 1 | 0 | 4 | ADD `variolation_networks`, REVIEW `traditional_food_processing`, REVIEW `organized_elementary_schooling`, REVIEW `codified_practical_knowledge`, REVIEW `urbanization` |
| `ADR` | Adrar | West Africa | 0 | 0 | 4 | REVIEW `traditional_food_processing`, REVIEW `organized_elementary_schooling`, REVIEW `codified_practical_knowledge`, REVIEW `urbanization` |
| `AGC` | Angoche | East Africa | 2 | 3 | 3 | REMOVE `systematic_administrative_statistics`, REVIEW `state_dockyard_systems`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `AHG` | Kel Ahaggar | North Africa | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `urbanization` |
| `AIR` | Kel Air | West Africa | 1 | 0 | 4 | ADD `variolation_networks`, REVIEW `traditional_food_processing`, REVIEW `organized_elementary_schooling`, REVIEW `codified_practical_knowledge`, REVIEW `urbanization` |
| `AIT` | Ait Abbas | North Africa | 2 | 6 | 3 | REMOVE `regulated_small_arms`, REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, REVIEW `variolation_networks`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements` |
| `AJJ` | Kel Ajjer | North Africa | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `urbanization` |
| `AJR` | Ajuran | East Africa | 5 | 0 | 2 | ADD `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, REVIEW `organized_elementary_schooling`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `ANK` | Ankole | East Africa | 4 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations`, REVIEW `distillation` |
| `ANU` | Anuak | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `ARS` | Arsiland | East Africa | 3 | 3 | 2 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, REVIEW `organized_elementary_schooling`, ADD `traditional_furniture_making` |
| `ASH` | Ashanti | West Africa | 5 | 1 | 3 | REVIEW `systematic_administrative_statistics`, ADD `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `ATR` | Kel Ataram | West Africa | 0 | 0 | 4 | REVIEW `traditional_food_processing`, REVIEW `organized_elementary_schooling`, REVIEW `codified_practical_knowledge`, REVIEW `urbanization` |
| `AUL` | Aulihan | East Africa | 5 | 0 | 3 | ADD `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, REVIEW `organized_elementary_schooling`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `AWS` | Aussa | East Africa | 3 | 3 | 2 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, REVIEW `organized_elementary_schooling`, ADD `traditional_furniture_making` |
| `AYI` | Anyi | West Africa | 4 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `BEN` | Benin | West Africa | 3 | 3 | 2 | REMOVE `systematic_administrative_statistics`, REVIEW `scientific_fortification_siegecraft`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `BGI` | Bagirmi | Equatorial Africa | 5 | 0 | 0 | ADD `variolation_networks`, ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `BGM` | Begemder | East Africa | 6 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `institutionalized_scientific_exchange` |
| `BLE` | Baule | West Africa | 4 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `BMB` | Bemba | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `BMM` | Bamum | Equatorial Africa | 5 | 0 | 0 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `BND` | Bundu | West Africa | 6 | 0 | 1 | ADD `variolation_networks`, ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `BNG` | Bangala | Equatorial Africa | 1 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `BNY` | Bunyoro | East Africa | 4 | 1 | 2 | REVIEW `variolation_networks`, ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `BOB` | Bobangi | Equatorial Africa | 1 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `BOR` | Bornu | West Africa | 6 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `institutionalized_scientific_exchange` |
| `BRD` | Burundi | East Africa | 5 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations`, REVIEW `distillation` |
| `BRG` | Borgu | West Africa | 3 | 3 | 1 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `BRK` | Brakna | West Africa | 0 | 0 | 4 | REVIEW `traditional_food_processing`, REVIEW `organized_elementary_schooling`, REVIEW `codified_practical_knowledge`, REVIEW `urbanization` |
| `BRN` | Borana | East Africa | 1 | 0 | 4 | ADD `variolation_networks`, REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making`, REVIEW `selective_breeding` |
| `BST` | Basutoland | Southern Africa | 0 | 0 | 2 | REVIEW `international_relations`, REVIEW `urbanization` |
| `BUG` | Buganda | East Africa | 4 | 1 | 2 | REVIEW `variolation_networks`, ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `CAY` | Cayor | West Africa | 6 | 0 | 1 | ADD `variolation_networks`, ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `CHK` | Chokwe | Equatorial Africa | 1 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `CMB` | Chaamba | North Africa | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `urbanization` |
| `CON` | Constantine | North Africa | 12 | 0 | 15 | ADD `regulated_small_arms`, REVIEW `systematic_administrative_statistics`, REVIEW `medical_degrees`, REVIEW `systematic_population_registration`, ADD `scientific_fortification_siegecraft`, ADD `state_dockyard_systems` |
| `DAH` | Dahomey | West Africa | 3 | 2 | 3 | REVIEW `systematic_administrative_statistics`, REVIEW `scientific_fortification_siegecraft`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `DAK` | Dar al Kuti | Equatorial Africa | 1 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `DFR` | Darfur | Nile Basin | 3 | 1 | 4 | REVIEW `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `institutionalized_scientific_exchange` |
| `DFT` | Dar Fertit | Nile Basin | 0 | 0 | 1 | REVIEW `traditional_food_processing` |
| `DIN` | Kel Dinnik | West Africa | 0 | 0 | 4 | REVIEW `traditional_food_processing`, REVIEW `organized_elementary_schooling`, REVIEW `codified_practical_knowledge`, REVIEW `urbanization` |
| `DIO` | Diola | West Africa | 4 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `DLA` | Duala | Equatorial Africa | 2 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making`, ADD `international_relations` |
| `DLM` | Delim | North Africa | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `urbanization` |
| `DNK` | Dinka | Nile Basin | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `selective_breeding` |
| `ETH` | Ethiopia | East Africa | 8 | 1 | 2 | REVIEW `systematic_administrative_statistics`, REVIEW `scientific_fortification_siegecraft`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements` |
| `EWE` | Ewe | West Africa | 4 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `FNG` | Fang | Equatorial Africa | 1 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `FTJ` | Futa Jallon | West Africa | 5 | 3 | 1 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `FTR` | Futa Toro | West Africa | 5 | 3 | 1 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `FZN` | Fezzan | North Africa | 2 | 5 | 5 | REMOVE `regulated_small_arms`, REMOVE `systematic_administrative_statistics`, REVIEW `shaft_mining`, REVIEW `variolation_networks`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements` |
| `GGO` | Gogo | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `GJM` | Gojjam | East Africa | 6 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `institutionalized_scientific_exchange` |
| `GLD` | Geledi | East Africa | 3 | 3 | 2 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, REVIEW `organized_elementary_schooling`, ADD `traditional_furniture_making` |
| `GZA` | Gaza | East Africa | 0 | 0 | 4 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making`, REVIEW `urbanization` |
| `HAR` | Harar | East Africa | 5 | 2 | 4 | REMOVE `systematic_administrative_statistics`, REVIEW `medical_degrees`, REVIEW `scientific_fortification_siegecraft`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements` |
| `HAU` | Gobir | West Africa | 5 | 3 | 1 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `HDY` | Hadiya | East Africa | 5 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `institutionalized_scientific_exchange` |
| `HHE` | Hehe | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `HMB` | Hemba | Equatorial Africa | 1 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `HRO` | Herero | Southern Africa | 2 | 0 | 4 | REVIEW `variolation_networks`, REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `traditional_furniture_making`, REVIEW `selective_breeding` |
| `IBO` | Igbo | West Africa | 4 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `ISQ` | Isaaq | East Africa | 3 | 3 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, REVIEW `variolation_networks`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, REVIEW `organized_elementary_schooling` |
| `JLF` | Jolof | West Africa | 6 | 0 | 1 | ADD `variolation_networks`, ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `KBA` | Kuba | Equatorial Africa | 3 | 1 | 1 | REVIEW `shaft_mining`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REMOVE `codified_practical_knowledge` |
| `KBD` | Kabadougou | West Africa | 0 | 0 | 0 | aucun écart majeur |
| `KBU` | Kaabu | West Africa | 5 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations`, REVIEW `distillation` |
| `KFA` | Kaffa | East Africa | 6 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `institutionalized_scientific_exchange` |
| `KKY` | Kikuyu | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `KNG` | Kong | West Africa | 5 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations`, REVIEW `distillation` |
| `KON` | Kongo | Equatorial Africa | 3 | 2 | 1 | REMOVE `systematic_administrative_statistics`, REVIEW `shaft_mining`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REMOVE `codified_practical_knowledge` |
| `KRG` | Karagwe | East Africa | 4 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations`, REVIEW `distillation` |
| `KRT` | Kaarta | West Africa | 5 | 3 | 1 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `KRU` | Kru | West Africa | 4 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `KSN` | Kasanje | Equatorial Africa | 4 | 0 | 0 | ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `KZM` | Kazembe | East Africa | 4 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations`, REVIEW `distillation` |
| `LBA` | Luba | Equatorial Africa | 3 | 0 | 1 | REVIEW `shaft_mining`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `LGA` | Lega | Equatorial Africa | 1 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `LIB` | Liberia | West Africa | 0 | 2 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making`, REMOVE `distillation`, REMOVE `codified_practical_knowledge` |
| `LND` | Lunda | Equatorial Africa | 3 | 0 | 1 | REVIEW `shaft_mining`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `LNG` | Loango | Equatorial Africa | 3 | 1 | 0 | ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REMOVE `codified_practical_knowledge` |
| `LUO` | Luo | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `LZO` | Barotse | East Africa | 4 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations`, REVIEW `distillation` |
| `MAD` | Madagascar | East Africa | 4 | 1 | 1 | REVIEW `regulated_small_arms`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `distillation`, REMOVE `codified_practical_knowledge` |
| `MAS` | Mascara | North Africa | 5 | 3 | 3 | REMOVE `systematic_administrative_statistics`, ADD `scientific_fortification_siegecraft`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements` |
| `MBS` | Mombasa | East Africa | 2 | 3 | 5 | REMOVE `systematic_administrative_statistics`, REVIEW `scientific_fortification_siegecraft`, REVIEW `state_dockyard_systems`, REMOVE `shaft_mining`, REVIEW `variolation_networks`, ADD `traditional_food_processing` |
| `MDK` | Mandinka | West Africa | 4 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `MJK` | Mijikenda | East Africa | 4 | 0 | 2 | ADD `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations`, REVIEW `distillation` |
| `MJT` | Majerteen | East Africa | 3 | 3 | 3 | REMOVE `systematic_administrative_statistics`, REVIEW `state_dockyard_systems`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, REVIEW `organized_elementary_schooling` |
| `MNB` | Mangbetu | Equatorial Africa | 5 | 0 | 0 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `MNC` | Manica | East Africa | 3 | 0 | 3 | ADD `shaft_mining`, ADD `organized_textile_production`, REVIEW `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `traditional_furniture_making`, REVIEW `applied_mineralogy` |
| `MOR` | Morocco | North Africa | 6 | 0 | 18 | REVIEW `systematic_administrative_statistics`, ADD `medical_degrees`, REVIEW `systematic_population_registration`, REVIEW `shaft_mining`, REVIEW `organized_forestry`, ADD `traditional_food_processing` |
| `MOS` | Mossi | West Africa | 5 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations`, REVIEW `distillation` |
| `MRV` | Maravi | East Africa | 4 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations`, REVIEW `distillation` |
| `MSH` | Mashona | East Africa | 2 | 0 | 3 | ADD `shaft_mining`, REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `traditional_furniture_making` |
| `MSI` | Masai | East Africa | 0 | 0 | 4 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making`, REVIEW `selective_breeding` |
| `MSK` | Maseko | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `MSN` | Massina | West Africa | 1 | 3 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, REMOVE `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `organized_elementary_schooling` |
| `MTB` | Ndebele | East Africa | 0 | 0 | 4 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making`, REVIEW `urbanization` |
| `MTP` | Mutapa | East Africa | 6 | 0 | 2 | ADD `shaft_mining`, ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `MZB` | Mzab | North Africa | 3 | 0 | 3 | ADD `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `traditional_glassmaking`, REVIEW `codified_practical_knowledge` |
| `NAM` | Nama | Southern Africa | 0 | 0 | 3 | REVIEW `variolation_networks`, REVIEW `traditional_food_processing`, REVIEW `selective_breeding` |
| `NUE` | Nuer | Nile Basin | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `selective_breeding` |
| `NYM` | Unyamwezi | East Africa | 4 | 0 | 3 | REVIEW `variolation_networks`, REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `OGD` | Ogaden | East Africa | 5 | 0 | 2 | ADD `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, REVIEW `organized_elementary_schooling`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `OMO` | Omo | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `ORA` | Oranje | Southern Africa | 0 | 3 | 1 | REMOVE `organized_textile_production`, REMOVE `distillation`, REMOVE `codified_practical_knowledge`, REVIEW `urbanization` |
| `ORM` | Orma | East Africa | 0 | 0 | 4 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making`, REVIEW `selective_breeding` |
| `OUA` | Tagant | West Africa | 0 | 0 | 4 | REVIEW `traditional_food_processing`, REVIEW `organized_elementary_schooling`, REVIEW `codified_practical_knowledge`, REVIEW `urbanization` |
| `OVB` | Ovambo | Southern Africa | 2 | 0 | 3 | REVIEW `variolation_networks`, REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `traditional_furniture_making` |
| `OVM` | Ovimbundu | Equatorial Africa | 4 | 0 | 0 | ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `OYO` | Oyo | West Africa | 3 | 3 | 1 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `PDI` | Pedi | Southern Africa | 2 | 0 | 3 | REVIEW `variolation_networks`, REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `traditional_furniture_making` |
| `PHL` | Philippolis | Southern Africa | 0 | 0 | 2 | REVIEW `international_relations`, REVIEW `urbanization` |
| `QWR` | Qwara | East Africa | 6 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `institutionalized_scientific_exchange` |
| `RGB` | Reguibat | North Africa | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `urbanization` |
| `RWD` | Rwanda | East Africa | 4 | 1 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation`, REMOVE `codified_practical_knowledge` |
| `SAF` | South Africa | Southern Africa | 5 | 1 | 10 | ADD `systematic_administrative_statistics`, ADD `systematic_population_registration`, REVIEW `variolation_networks`, REVIEW `organized_textile_production`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `SAH` | Sahrawi | North Africa | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `urbanization` |
| `SAN` | San | Southern Africa | 0 | 0 | 1 | REVIEW `improved_husbandry` |
| `SD1` | The Sudan | Nile Basin | 4 | 0 | 4 | REVIEW `systematic_administrative_statistics`, ADD `variolation_networks`, REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making`, ADD `international_relations` |
| `SDM` | Sidamo | East Africa | 6 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `institutionalized_scientific_exchange` |
| `SGU` | Segou | West Africa | 5 | 3 | 1 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `SHW` | Shewa | East Africa | 6 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `institutionalized_scientific_exchange` |
| `SIL` | Sierra Leone | West Africa | 0 | 2 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making`, REMOVE `distillation`, REMOVE `codified_practical_knowledge` |
| `SKM` | Usukuma | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `SKY` | Sakuye | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `SNG` | Sangu | East Africa | 0 | 0 | 3 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `SOK` | Sokoto | West Africa | 1 | 3 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, REMOVE `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `organized_elementary_schooling` |
| `SRR` | Serer | West Africa | 4 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `SSU` | Susu | West Africa | 4 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `SWZ` | Swaziland | Southern Africa | 2 | 0 | 4 | REVIEW `variolation_networks`, REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `traditional_furniture_making`, REVIEW `international_relations` |
| `TBI` | Tubu | Equatorial Africa | 1 | 0 | 3 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making`, REVIEW `urbanization` |
| `TEK` | Tekna | North Africa | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `urbanization` |
| `TGI` | Tungi | East Africa | 2 | 3 | 2 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `TGR` | Tigray | East Africa | 6 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `institutionalized_scientific_exchange` |
| `TKE` | Teke | Equatorial Africa | 5 | 0 | 0 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `TMN` | Temne | West Africa | 4 | 0 | 1 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `distillation` |
| `TPS` | Toposa | Nile Basin | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `selective_breeding` |
| `TRI` | Tripolitania | North Africa | 8 | 1 | 13 | REVIEW `systematic_administrative_statistics`, REVIEW `medical_degrees`, REVIEW `systematic_population_registration`, REMOVE `shaft_mining`, ADD `variolation_networks`, REVIEW `organized_forestry` |
| `TRK` | Turkana | East Africa | 0 | 0 | 4 | REVIEW `organized_textile_production`, REVIEW `traditional_food_processing`, REVIEW `traditional_furniture_making`, REVIEW `selective_breeding` |
| `TRN` | Transvaal | Southern Africa | 0 | 3 | 1 | REMOVE `organized_textile_production`, REMOVE `distillation`, REMOVE `codified_practical_knowledge`, REVIEW `urbanization` |
| `TRZ` | Trarza | West Africa | 0 | 0 | 4 | REVIEW `traditional_food_processing`, REVIEW `organized_elementary_schooling`, REVIEW `codified_practical_knowledge`, REVIEW `urbanization` |
| `TSW` | Tswana | Southern Africa | 2 | 0 | 4 | REVIEW `variolation_networks`, REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `traditional_furniture_making`, REVIEW `selective_breeding` |
| `TUA` | Tuat | North Africa | 3 | 0 | 2 | ADD `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `codified_practical_knowledge` |
| `TUG` | Touggourt | North Africa | 3 | 0 | 2 | ADD `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, ADD `traditional_furniture_making`, REVIEW `codified_practical_knowledge` |
| `TUN` | Tunis | North Africa | 9 | 0 | 15 | REVIEW `systematic_administrative_statistics`, ADD `medical_degrees`, REVIEW `systematic_population_registration`, REVIEW `shaft_mining`, ADD `variolation_networks`, REVIEW `organized_forestry` |
| `VND` | Venda | Southern Africa | 2 | 0 | 3 | REVIEW `variolation_networks`, REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `traditional_furniture_making` |
| `WAD` | Wadai | Equatorial Africa | 5 | 3 | 0 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making` |
| `WBL` | Griqualand | Southern Africa | 0 | 0 | 2 | REVIEW `international_relations`, REVIEW `urbanization` |
| `WLG` | Welega | East Africa | 6 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `institutionalized_scientific_exchange` |
| `WLT` | Wolaita | East Africa | 6 | 2 | 3 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `variolation_networks`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `institutionalized_scientific_exchange` |
| `WSG` | Warsangali | East Africa | 3 | 3 | 2 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, REVIEW `organized_elementary_schooling`, ADD `traditional_furniture_making` |
| `WTU` | Witu | East Africa | 3 | 3 | 2 | REMOVE `systematic_administrative_statistics`, REMOVE `shaft_mining`, ADD `traditional_food_processing`, REVIEW `improved_agricultural_implements`, REVIEW `organized_elementary_schooling`, ADD `traditional_furniture_making` |
| `XHO` | Xhosa | Southern Africa | 2 | 0 | 3 | REVIEW `variolation_networks`, REVIEW `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, REVIEW `traditional_furniture_making` |
| `YKA` | Yaka | Equatorial Africa | 1 | 0 | 2 | REVIEW `organized_textile_production`, ADD `traditional_food_processing`, REVIEW `traditional_furniture_making` |
| `ZND` | Azande | Equatorial Africa | 5 | 0 | 0 | ADD `organized_textile_production`, ADD `traditional_food_processing`, ADD `improved_agricultural_implements`, ADD `traditional_furniture_making`, ADD `international_relations` |
| `ZUL` | Zulu | Southern Africa | 0 | 0 | 2 | REVIEW `international_relations`, REVIEW `urbanization` |
| `ZWY` | Zuwayya | North Africa | 0 | 0 | 2 | REVIEW `traditional_food_processing`, REVIEW `urbanization` |

## 15. TREE_STRUCTURE_REVIEW

**215 relations** sont marquées `TREE_STRUCTURE_REVIEW`. Le motif dominant est une capacité historiquement plausible dont la généalogie dans l’arbre suppose un parent institutionnel européen non nécessaire historiquement. Exemples structurants : `codified_practical_knowledge` sans `periodical_print_networks`, enseignement élémentaire religieux sans presse périodique, ou certification médicale sans tout le paquet d’échange scientifique moderne. Ces cas ne doivent pas être résolus en supprimant la capacité enfant.

- `ACH` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `ADG` `codified_practical_knowledge` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `ADG` `organized_elementary_schooling` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `ADR` `codified_practical_knowledge` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `ADR` `organized_elementary_schooling` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `AGC` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `AIR` `codified_practical_knowledge` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `AIR` `organized_elementary_schooling` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `AIT` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `AIT` `codified_practical_knowledge` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `AJR` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `AJR` `organized_elementary_schooling` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `ANK` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `ANU` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `ARS` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `ARS` `organized_elementary_schooling` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `ASH` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `ATR` `codified_practical_knowledge` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `ATR` `organized_elementary_schooling` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `AUL` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `AUL` `organized_elementary_schooling` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `AWS` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `AWS` `organized_elementary_schooling` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `AYI` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `BEN` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `BGI` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `BGM` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.
- `BGM` `codified_practical_knowledge` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `BGM` `organized_elementary_schooling` : TREE_STRUCTURE_REVIEW: le parent imposé par l’arbre est plus difficile à justifier que la capacité examinée.
- `BLE` `traditional_furniture_making` : TREE_STRUCTURE_REVIEW: capacité historiquement justifiée mais au moins un parent n’est pas historiquement justifié/établi au même niveau.

## 16. CLASSIFICATION_REVIEW

**2 relations** portent un problème de classification. `CLASSIFICATION_REVIEW` strict : **0**. Les autres signaux peuvent être `CLASSIFICATION_TOO_LATE/TOO_EARLY`.

- `MOR` `medical_degrees` — **CLASSIFICATION_TOO_LATE** : Al-Qarawiyyin et la tradition de l’ijaza fournissent un précédent institutionnel de formation et certification médicales très antérieur à 1776; le nœud ne doit pas être lu comme diplôme moderne du XIXe siècle.
- `TUN` `medical_degrees` — **CLASSIFICATION_TOO_LATE** : Tunis conserve des institutions médicales arabo-islamiques, maristan et délivrance d’ijazas; le principe de certification médicale est antérieur à 1776.

## 17. Principales différences avec la première passe

- Audit exhaustif des **61 technologies A/B** pour chaque TAG, au lieu d’un échantillon de technologies pertinentes/courantes.
- `organized_forestry` est désormais interprétée strictement comme exploitation organisée/rationalisée : la simple coupe du bois ne justifie plus la technologie.
- `traditional_papermaking`, `traditional_glassmaking` et `traditional_furniture_making` sont évaluées indépendamment de la foresterie organisée.
- `shaft_mining` est fortement resserrée : métallurgie et exploitation minérale ne valent pas automatiquement puits miniers avancés.
- `systematic_administrative_statistics` est resserrée aux registres réellement systématiques; fiscalité/tribut seuls ne suffisent plus.
- `variolation_networks` est positivement redistribuée selon l’historiographie africaine au lieu de rester une simple incertitude mondiale.
- `medical_degrees` est relu comme certification pré-moderne : Maroc et Tunis deviennent des cas positifs, non des exclusions par analogie avec le diplôme médical XIXe.
- Les capacités artisanales de base (transformation alimentaire, mobilier, outillage agricole) sont beaucoup moins sous-évaluées dans les États africains à forte spécialisation artisanale.

### 20 changements les plus importants par rapport à la distribution reconstruite comme actuellement implémentée

| # | TAG | Pays | Technologie | Changement | Statut historique | Pourquoi |
|---:|---|---|---|---|---|---|
| 1 | `AIT` | Ait Abbas | `regulated_small_arms` | **REMOVE** | ABSENT | L’usage ou l’importation massive d’armes à feu ne suffit pas : absence de preuve d’une industrie locale réglementée d’armes complètes/artillerie. |
| 2 | `SAF` | South Africa | `systematic_administrative_statistics` | **ADD** | ESTABLISHED | Les registres VOC, notamment recensements/tax rolls et comptabilité administrative, constituent une pratique statistique-fiscale systématique à l’échelle coloniale. |
| 3 | `SAF` | South Africa | `systematic_population_registration` | **ADD** | ESTABLISHED | Les opgaaf rolls et autres listes de population/taxation de la VOC fournissent un enregistrement régulier des ménages et ressources. |
| 4 | `AGC` | Angoche | `systematic_administrative_statistics` | **REMOVE** | ABSENT | Administration ou tribut ne suffisent pas à démontrer des statistiques d’État systématiques. |
| 5 | `MOR` | Morocco | `medical_degrees` | **ADD** | ESTABLISHED | Al-Qarawiyyin et la tradition de l’ijaza fournissent un précédent institutionnel de formation et certification médicales très antérieur à 1776; le nœud ne doit pas être lu comme diplôme moderne du XIXe siècle. |
| 6 | `CON` | Constantine | `variolation_networks` | **ADD** | ESTABLISHED | Une communication publiée par la Royal Society en 1728 décrit directement l’inoculation de la variole à Tripoli, Tunis et Alger comme une pratique ancienne et répandue; le nœud représente ici un réseau local de variolisation, non la vaccination moderne. |
| 7 | `MAS` | Mascara | `variolation_networks` | **ADD** | ESTABLISHED | Une communication publiée par la Royal Society en 1728 décrit directement l’inoculation de la variole à Tripoli, Tunis et Alger comme une pratique ancienne et répandue; le nœud représente ici un réseau local de variolisation, non la vaccination moderne. |
| 8 | `AGC` | Angoche | `shaft_mining` | **REMOVE** | ABSENT | La présence de métallurgie ou d’extraction de surface ne suffit pas à établir des techniques de puits miniers avancées correspondant au nœud. |
| 9 | `AIT` | Ait Abbas | `shaft_mining` | **REMOVE** | ABSENT | La présence de métallurgie ou d’extraction de surface ne suffit pas à établir des techniques de puits miniers avancées correspondant au nœud. |
| 10 | `CON` | Constantine | `scientific_fortification_siegecraft` | **ADD** | ESTABLISHED | Fortifications d’artillerie, garnisons et pratiques de siège organisées justifient le nœud; au Cap il s’agit de fortification coloniale locale, non de toute la technologie néerlandaise. |
| 11 | `CON` | Constantine | `state_dockyard_systems` | **ADD** | ESTABLISHED | Arsenaux et flotte d’État/corsaire nécessitent administration navale, construction et entretien organisés. |
| 12 | `MSN` | Massina | `organized_textile_production` | **REMOVE** | ABSENT | Pas de preuve suffisante d’une production textile organisée au seuil du nœud. |
| 13 | `AGC` | Angoche | `traditional_food_processing` | **ADD** | ESTABLISHED | Moulins, pressage, fermentation, préparation de denrées ou autres ateliers de transformation sont établis; le nœud représente ici une production artisanale organisée. |
| 14 | `AIT` | Ait Abbas | `traditional_food_processing` | **ADD** | ESTABLISHED | Moulins, pressage, fermentation, préparation de denrées ou autres ateliers de transformation sont établis; le nœud représente ici une production artisanale organisée. |
| 15 | `ANK` | Ankole | `improved_agricultural_implements` | **ADD** | ESTABLISHED | L’agriculture repose sur un outillage de fer spécialisé (houes, haches, outils de travail du sol) produit ou largement disponible localement; l’attribution vise l’outillage, pas la mécanisation. |
| 16 | `ASH` | Ashanti | `improved_agricultural_implements` | **ADD** | ESTABLISHED | L’agriculture repose sur un outillage de fer spécialisé (houes, haches, outils de travail du sol) produit ou largement disponible localement; l’attribution vise l’outillage, pas la mécanisation. |
| 17 | `BOR` | Bornu | `institutionalized_scientific_exchange` | **ADD** | SECTORAL | Des réseaux savants institutionnels, religieux ou de cour assurent circulation de textes et de savoirs; l’interprétation est non européenne et sectorielle. |
| 18 | `BOR` | Bornu | `organized_elementary_schooling` | **ADD** | SECTORAL | Écoles coraniques, institutions ecclésiastiques ou réseaux d’enseignement élémentaire structurés assurent un accès organisé à l’instruction, sans supposer une école publique moderne. |
| 19 | `ETH` | Ethiopia | `systematic_legal_codification` | **ADD** | ESTABLISHED | Le Fetha Nagast et la tradition écrite juridico-ecclésiastique structurent durablement la pratique du droit; le nœud est interprété comme codification établie. |
| 20 | `AGC` | Angoche | `traditional_furniture_making` | **ADD** | ESTABLISHED | Menuiserie, travail du bois et mobilier spécialisé sont attestés dans les centres urbains, cours ou réseaux artisanaux; le nœud ne requiert plus organized_forestry comme preuve historique. |

## 18. Recommandations finales

1. Implémenter les ADD/REMOVE de confiance HIGH/MEDIUM en priorité, sans réintroduire les anciens tiers génériques comme raccourci.
2. Garder les REVIEW comme arbitrages de synthèse mondiale, surtout Maghreb (finance, arsenaux), minéralogie et pratiques agricoles frontière.
3. Traiter séparément les `TREE_STRUCTURE_REVIEW` : l’arbre ne doit pas forcer la suppression d’une capacité historiquement attestée.
4. Revoir globalement la classification de `medical_degrees` : les cas marocain et tunisien montrent que la capacité de certification médicale est bien antérieure à 1776.
5. Avant merge final, régénérer `Current_Status` depuis le working tree si l’implémentation mondiale a divergé des décisions de la première matrice Afrique.

### Contrôle final

- TAG : **161**
- Technologies A auditées : **25**
- Technologies B auditées : **36**
- Technologies E gameplay auditées : **5**
- Lignes totales : **10626**
- ADD : **443**
- REMOVE : **126**
- KEEP : **9637**
- REVIEW : **420**
- TREE_STRUCTURE_REVIEW : **215**
- CLASSIFICATION_REVIEW : **0**
- Autres Classification_Issue : **2**
- Aucun fichier gameplay modifié. Aucun code Victoria 3 produit. Aucun commit/push.