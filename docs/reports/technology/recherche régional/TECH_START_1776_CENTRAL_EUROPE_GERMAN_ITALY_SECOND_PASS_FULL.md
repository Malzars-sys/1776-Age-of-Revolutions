# Recherche technologique — Europe centrale, monde germanique et Italie — SECOND PASS FULL — 1er janvier 1776

> **Statut : recherche uniquement.** Aucun fichier gameplay n’a été modifié. Aucun code Victoria 3 n’est produit. Aucun commit/push n’est effectué.

Cette seconde passe repart des capacités historiques réelles au **1776-01-01**, indépendamment du tier générique et sans utiliser les prérequis de l’arbre comme filtre historique.

## 1. Périmètre

**41 TAG** sont étudiés. La matrice couvre exhaustivement les 25 technologies A et les 36 technologies B pour chacun de ces TAG.

TAG : PRU, AUS, BAV, SAX, BRA, HAN, WUR, SWI, SAR, VEN, GEN, TUS, PAP, GR4, SIC, GR3, ANH, BAD, BRE, COB, FRM, HAM, HEK, HES, HOH, HOL, LIP, LUB, MEC, MEI, MST, NAS, OLD, SCH, SCM, SCW, WEI, WLD, LUC, MOD, PAR.

Sous-ensembles particuliers : la Suisse est traitée comme profil manufacturier/cantonal propre ; l’Italie distingue explicitement SAR, VEN, GEN, TUS, PAP, MOD, PAR, LUC, GR3, GR4 et SIC. `GR3` (Sicily), `GR4` (Naples) et `SIC` (Two Sicilies) sont conservés comme TAG techniques distincts parce qu’ils coexistent dans le CSV pays.

## 2. Sources et méthode

### Autorité technique

- `TECH_START_1776_TECHNOLOGIES.csv` : IDs exacts, classification A/B/C/D/E, catégories, prérequis et déblocages.

- `TECH_START_1776_COUNTRIES.csv` : TAG et distribution actuellement implémentée.

- `TECH_START_1776_CENTRAL_EUROPE_GERMAN_ITALY_MATRIX.csv` et le rapport de première passe : comparaison méthodologique et historique.

- La distribution actuelle sert uniquement à calculer `Current_Status`; elle n’est jamais une preuve historique.

### Procédure

- Audit exhaustif : **25 A × 41 TAG = 1025 relations** et **36 B × 41 TAG = 1476 relations**, soit **2501 décisions A/B obligatoires**.

- Les décisions sont prises en deux temps : (1) capacité historique au 1er janvier 1776 ; (2) seulement ensuite fermeture des prérequis et éventuel `TREE_STRUCTURE_REVIEW`.

- `organized_forestry` est interprété dans sa **nouvelle définition** : exploitation forestière rationalisée/organisée. Papier, verre et meuble ne dépendent plus historiquement de ce nœud, et la simple coupe de bois ne suffit pas à l’attribuer.

- Cinq nœuds E à contenu gameplay direct ou institutionnel identifiable sont développés pays par pays : `field_works`, `colonization`, `urbanization`, `multilateral_alliances`, `political_agitation`. Les alias réellement vides/non pertinents ne sont pas distribués pour combler l’arbre.

- Sept relations C sont examinées : les trois anachronismes actuellement distribués (`railways` BRA, `romanticism` AUS/PRU) et quatre relations susceptibles de `CLASSIFICATION_REVIEW` (`clinicopathological_medicine` AUS/VEN ; `military_veterinary_services` AUS/SAR).

### Principales sources historiques

- **Monde germanique — économie, armée, manufactures** : https://www.cambridge.org/core/journals/journal-of-economic-history/article/economic-growth-in-germany-15001850/3FB21F575B6056CE6BCFF04C97FC1E49 ; https://www.cambridge.org/core/books/abs/cultures-of-power-in-europe-during-the-long-eighteenth-century/military-culture-in-the-reich-c-16801806/F52FD6774258813E7A482606C91377B9 ; https://www.cambridge.org/core/books/abs/globalized-peripheries/linen-and-merchants-from-the-duchy-of-berg-lower-saxony-and-westphalia-and-their-global-trade-in-eighteenthcentury-london/8C3BFA133DB7FDE29BE7CED56AB0662E

- **Prusse** : https://cp.tu-berlin.de/history ; https://germanhistorydocs.org/en/the-holy-roman-empire-1648-1815/friedrich-der-grosse-koeniglich-preussisches-general-land-schul-reglement-1763 ; https://www.cambridge.org/core/books/abs/how-a-ledger-became-a-central-bank/prussias-debasement-during-the-seven-years-war-the-role-of-the-bank/437DCCA7BA61ADF546E0B44944BFD6AA ; https://www.finowkanal.info/en/historical-facts-about-the-finowkanal/

- **Autriche / Habsbourg** : https://geschichte.univie.ac.at/en/node/23380 ; https://geschichte.univie.ac.at/de/node/29042 ; https://pubmed.ncbi.nlm.nih.gov/40378550/ ; https://www.vetmeduni.ac.at/en/bibliothek/historical-archive ; https://www.mdpi.com/2220-9964/12/6/220 ; https://www.senat.fr/colloques/actes_bicentenaire_code_penal/actes_bicentenaire_code_penal_mono.html ; https://www.tandfonline.com/doi/full/10.1080/17581206.2024.2437551 ; https://whc.unesco.org/en/list/618 ; https://www.archivinformationssystem.at/detail.aspx?ID=2029

- **Saxe** : https://tu-freiberg.de/en/university/history ; https://tu-freiberg.de/en/lfbw ; https://www.meissen.com/en/geschichte ; https://books.fupress.com/chapter/promotion-of-high-quality-textiles-by-prize-competitions-during-the-enlightenment-in-saxony-from-raw/13603 ; https://www.bmel.de/DE/themen/wald/wald-in-deutschland/carlowitz-jahr.html ; https://www.archiv.sachsen.de/archiv/bestand.jsp?bestandid=10694&oid=02.01&syg_id=144066 ; https://www.deutsche-digitale-bibliothek.de/item/3IIWU766E533VWV6LKBENVDKYQHNUWRD

- **Bavière / Wurtemberg** : https://www.nymphenburg.com/en/pages/haus-wittelsbach ; https://www.deutsche-digitale-bibliothek.de/item/OUO5DWBMRCV24F3DMAPF4PXYMCWFXO5O

- **Suisse** : https://hls-dhs-dss.ch/de/articles/013957/2014-10-07/ ; https://hls-dhs-dss.ch/de/articles/013961/2015-03-20/ ; https://hls-dhs-dss.ch/fr/articles/013882/2006-10-23/

- **Piémont-Sardaigne** : https://www.museotorino.it/view/s/276a506f80994a3a943a5600e4b944ce ; https://www.museotorino.it/view/s/66901479df374aaf80fd472c76944ff2 ; https://patrimoines.savoie.fr/web/psp_10906/cadastre ; https://atom.unito.it/index.php/esami-per-il-conferimento-dei-gradi-medicina ; https://ojs.unito.it/index.php/RSUT/article/view/4342 ; https://en.chateauversailles.fr/royal-silks-europe/consortium-royal-residences-savoy

- **Venise / Padoue** : https://www.treccani.it/enciclopedia/l-arsenale-di-venezia-e-i-cantieri-navali-della-marina_(Il-Contributo-italiano-alla-storia-del-Pensiero%3A-Tecnica)/ ; https://www.treccani.it/enciclopedia/la-finanza-pubblica-bilanci-fisco-moneta-e-debito-pubblico_%28altro%29/ ; https://www.cambridge.org/core/journals/continuity-and-change/article/borrowing-in-a-preindustrial-city-financial-behaviour-and-economic-rationality-in-eighteenthcentury-venice/A3F420B07CEED5B4B5486048FD6B2C39 ; https://www.treccani.it/enciclopedia/le-riforme_%28Storia-di-Venezia%29/ ; https://museovetro.visitmuve.it/en/il-museo/layout-and-collections/glass-14th-17th-century/ ; https://heritage.unipd.it/en/timeline/il-settecento/ ; https://heritage.unipd.it/en/storia/giovanni-battista-morgagni/

- **Gênes** : https://www.journals.uchicago.edu/doi/10.1086/721231 ; https://www.museidigenova.it/en/textured-and-embroidered-fabrics ; https://museo.accademialigustica.it/storia/

- **États pontificaux / Naples** : https://www.cambridge.org/core/books/abs/government-debts-and-financial-markets-in-europe/public-debt-in-the-papal-states-financial-market-and-government-strategies-in-the-long-run-seventeenthnineteenth-centuries/522DBD82C53055463B55A1FE89D0E5E8 ; https://www.cambridge.org/core/books/abs/government-debts-and-financial-markets-in-europe/from-subordination-to-autonomy-public-debt-policies-and-the-creation-of-a-selfruled-financial-market-in-the-kingdom-of-naples-in-the-long-run-15001800/86646BBED21D906ACD6F23E64244C1E1 ; https://www.cambridge.org/core/books/abs/naples-in-the-eighteenth-century/arrogance-of-the-market-the-economy-of-the-kingdom-between-the-mediterranean-and-europe/E275AD8133C1ABA8555C21B6441255AC ; https://www.metmuseum.org/es/essays/art-of-the-seventeenth-and-eighteenth-centuries-in-naples ; https://www.esercito.difesa.it/en/organization/the-chief-of-general-staff-of-the-army/training-specialization-and-doctrine-command/training-command-and-application-school-of-the-army/military-academy/nunziatella/history-and-traditions/124245.html

- **Toscane** : https://www.treccani.it/enciclopedia/pietro-leopoldo-d-asburgo-lorena-granduca-di-toscana-poi-imperatore-del-sacro-romano-impero-come-leopoldo-ii_(Dizionario-Biografico)/ ; https://brill.com/display/book/edcoll/9789004392489/BP000025.xml

- **Villes marchandes allemandes** : https://brill.com/display/title/34830?language=en ; https://live.deutsche-boerse.com/en/know-how/about/geschichte-der-frankfurter-wertpapierboerse/11th-to-17th-century-fairs-coins-letters-of-exchange ; https://live.deutsche-boerse.com/en/know-how/about/geschichte-der-frankfurter-wertpapierboerse/18th-and-19th-centuries-citizens-princes-new-stock-exchanges

- **Repères de datation et classification** : https://dbmuseum.de/en/nuremberg/exhibitions/the-history-of-the-railway-in-germany ; https://82nd-and-fifth.metmuseum.org/toah/ht/10/euwc.html ; https://www.lindahall.org/about/news/scientist-of-the-day/edmund-cartwright/ ; https://www.unipd.it/en/sala-laurea-medicina ; https://pmc.ncbi.nlm.nih.gov/articles/PMC13361031/ ; https://ehne.fr/en/node/14167/printable/print


La matrice conserve en plus deux URL au maximum par relation afin que la justification puisse être transférée indépendamment de ce rapport.

## 3. Production

La seconde passe relève fortement les savoir-faire traditionnels tout en restant stricte sur la mécanisation. `traditional_food_processing` et `traditional_furniture_making` deviennent largement établis sans passer par `organized_forestry`; le papier est ajouté à 22 TAG et le verre à 13. En revanche, le gameplay de `mechanized_weaving` et `advanced_spinning` est postérieur au cutoff : ces deux B sont signalées `CLASSIFICATION_TOO_EARLY`.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `traditional_food_processing` (A) | ADD : ANH, AUS, BAD, BAV, BRA, BRE, COB, FRM (+33) | 41 | 0 | 0 |

| `traditional_papermaking` (A) | ADD : AUS, BAD, BAV, BRA, FRM, GEN, GR4, HAM (+14) | 22 | 0 | 19 |

| `traditional_glassmaking` (A) | ADD : AUS, BAD, BAV, GEN, GR4, HAN, PRU, SAX (+5) | 13 | 0 | 7 |

| `traditional_furniture_making` (A) | ADD : ANH, AUS, BAD, BAV, BRA, BRE, COB, FRM (+33) | 41 | 0 | 0 |

| `organized_textile_production` (A) | aucun changement majeur | 0 | 0 | 0 |

| `distillation` (A) | aucun changement majeur | 0 | 0 | 0 |

| `sugar_refining` (A) | ADD : GEN, HAM, PRU, TUS, VEN | 5 | 0 | 5 |

| `industrial_acids` (A) | cas limites : AUS, SAX | 0 | 0 | 2 |

| `industrial_ceramics` (B) | ADD : AUS, BAV, BRA, GEN, GR4, PRU, SAX, SIC (+3) | 11 | 0 | 4 |

| `mechanized_spinning` (B) | cas limites : SAR | 0 | 0 | 1 |

| `mechanized_weaving` (B) | CLASSIFICATION_TOO_EARLY | 0 | 0 | 0 |

| `advanced_spinning` (B) | CLASSIFICATION_TOO_EARLY | 0 | 0 | 0 |


## 4. Agriculture

L’existence d’une agriculture n’est jamais suffisante. `improved_husbandry` est maintenu quand les méthodes améliorées sont plausibles, mais plusieurs micro-États passent en REVIEW. Les instruments améliorés, rotations avancées et sélection sont réservés aux pays où des pratiques précises sont documentées ; la Saxe et l’Autriche ressortent davantage que le tier uniforme ne le laissait voir.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `improved_husbandry` (A) | cas limites : ANH, BRE, COB, FRM, GR3, GR4, HAM, HOH (+16) | 0 | 0 | 24 |

| `selective_breeding` (B) | ADD : AUS, SAX | 2 | 0 | 2 |

| `advanced_crop_rotations` (B) | cas limites : AUS, HAN, PRU, SAR, SAX, SWI, TUS, VEN | 0 | 0 | 8 |

| `improved_agricultural_implements` (B) | ADD : AUS, PRU, SAR, SAX, TUS | 5 | 0 | 5 |


## 5. Mines/métallurgie

C’est un des domaines où le tier 4 produisait le plus de faux positifs. `shaft_mining` est retiré de nombreux petits États sans mines profondes avancées, tandis que Saxe, Prusse, Autriche, Hanovre/Harz, Brunswick, Bavière et quelques États italiens conservent ou reçoivent des capacités sectorielles. Aucun TAG régional ne reçoit `coke_smelting`. L’Autriche reçoit `atmospheric_engine` en FRONTIER pour la monarchie habsbourgeoise, mais avec `TREE_STRUCTURE_REVIEW` car le parent `coke_smelting` n’est pas historiquement justifié.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `shaft_mining` (A) | REMOVE : ANH, BRE, COB, FRM, GR3, HAM, HOH, HOL (+15) | 0 | 23 | 9 |

| `applied_mineralogy` (B) | ADD : AUS, PRU, SAX | 3 | 0 | 3 |

| `coke_smelting` (A) | aucun changement majeur | 0 | 0 | 0 |

| `atmospheric_engine` (B) | ADD : AUS | 1 | 0 | 0 |

| `precision_boring` (B) | aucun changement majeur | 0 | 0 | 0 |

| `condensing_steam_engines` (B) | aucun changement majeur | 0 | 0 | 0 |


## 6. Infrastructure

La redéfinition de `organized_forestry` change fortement le résultat : le nœud est attribué seulement aux États présentant une gestion rationalisée documentable, notamment la Saxe de Carlowitz (1713), la Prusse, le Wurtemberg, la Bavière, l’Autriche, Brunswick et Hanovre ; la simple économie forestière ne suffit plus. `industrial_canals` reste exceptionnel : ADD sectoriel à PRU pour le Finowkanal, REVIEW à Venise. `urbanization` est conservé dans la matrice comme E gameplay-active mais placé en REVIEW/ABSTRACT plutôt que traité comme une preuve historique de tier.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `organized_forestry` (A) | ADD : AUS, BAV, BRA, HAN, PRU, SAX, WUR | 7 | 0 | 4 |

| `turnpike_road_networks` (B) | ADD : AUS, HAN, PRU, SAR, SAX, TUS | 6 | 0 | 3 |

| `industrial_canals` (B) | ADD : PRU | 1 | 0 | 1 |

| `urbanization` (E) | cas limites : ANH, AUS, BAD, BAV, BRA, BRE, COB, FRM (+33) | 0 | 0 | 41 |


## 7. Finance et économie

C’est la plus forte correction positive de la seconde passe. `institutionalized_public_credit` est ajouté à VEN, GEN, PAP, GR4, SIC, AUS et SAX, alors que PRU reste absent : la recherche sur les finances prussiennes pendant la guerre de Sept Ans décrit encore un système sans véritable marché obligataire. Le résultat confirme qu’une petite république marchande peut être beaucoup plus avancée financièrement qu’une grande monarchie militaire.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `institutionalized_public_credit` (A) | ADD : AUS, GEN, GR4, PAP, SAX, SIC, VEN | 7 | 0 | 5 |

| `commercial_insurance_markets` (A) | ADD : GEN, HAM, VEN | 3 | 0 | 7 |

| `stock_exchange` (A) | ADD : GEN, VEN | 2 | 0 | 5 |

| `political_economy` (B) | ADD : AUS, HAN, PRU, SAX, TUS | 5 | 0 | 4 |

| `classical_political_economy` (B) | CLASSIFICATION_TOO_EARLY; cas limites : PRU, TUS | 0 | 0 | 2 |


Comparaison critique :

- **VEN** : ADD `institutionalized_public_credit`, `commercial_insurance_markets`, `stock_exchange`; le crédit vénitien du XVIIIe siècle est structuré et l’État possède une longue histoire de dette financée.

- **GEN** : ADD des trois mêmes capacités financières fondamentales, cohérentes avec la tradition génoise de dette publique et d’intermédiation.

- **PAP** : ADD `institutionalized_public_credit`, mais `stock_exchange` reste REVIEW : dette publique structurée ne signifie pas automatiquement bourse moderne.

- **GR4/SIC** : ADD `institutionalized_public_credit`, REVIEW assurance/bourse.

- **PRU** : aucun ADD de crédit public institutionnalisé malgré son appareil d’État : le contre-exemple empêche toute logique « grande puissance = finance avancée ».

## 8. Commerce

`international_relations` reste largement justifié comme capacité diplomatique de base du monde européen considéré, mais les nœuds commerciaux plus institutionnels sont différenciés. Hamburg reçoit l’assurance commerciale, Frankfurt conserve une lecture prudente de la bourse (les titres publics n’y deviennent centraux qu’après le cutoff), et Venise/Gênes dominent nettement le profil marchand italien. `colonization` est retiré à PRU et reste REVIEW à VEN comme abstraction politique, sans propagation automatique aux États maritimes.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `international_relations` (A) | aucun changement majeur | 0 | 0 | 0 |

| `commercial_insurance_markets` (A) | ADD : GEN, HAM, VEN | 3 | 0 | 7 |

| `stock_exchange` (A) | ADD : GEN, VEN | 2 | 0 | 5 |

| `colonization` (E) | REMOVE : PRU | 0 | 1 | 1 |


## 9. Administration

Le tier 4 surestimait l’administration normalisée des petits États. `systematic_administrative_statistics` est retiré à 20 TAG et `codified_practical_knowledge` à 18. À l’inverse, les dispositifs réellement documentés sont explicitement ajoutés : population registration à PRU/AUS, cadastre systématique à SAR, codification à BAV/SAR, avec maintien de la codification autrichienne déjà présente.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `systematic_administrative_statistics` (A) | REMOVE : ANH, BAD, BRE, COB, GR3, HOH, HOL, LIP (+12) | 0 | 20 | 8 |

| `systematic_population_registration` (B) | ADD : AUS, PRU | 2 | 0 | 4 |

| `systematic_cadastral_surveying` (B) | ADD : SAR | 1 | 0 | 4 |

| `systematic_legal_codification` (B) | ADD : BAV, SAR | 2 | 0 | 3 |

| `codified_practical_knowledge` (A) | REMOVE : ANH, BRE, COB, GR3, HOH, HOL, LIP, LUB (+10) | 0 | 18 | 6 |


## 10. Science/éducation

Les universités traditionnelles ne sont pas assimilées automatiquement à des académies techniques ou à des réseaux scientifiques. `institutionalized_scientific_exchange` est néanmoins ajouté à 19 TAG disposant d’institutions savantes solides, et `periodical_print_networks` à 21. La Saxe reçoit désormais `specialized_technical_academies` grâce à Freiberg (1765), SAR grâce aux écoles turinoises, et GR4/SIC grâce aux institutions techniques/militaires napolitaines. L’enseignement primaire organisé est réservé à quelques États où l’intervention institutionnelle est démontrable, notamment la Prusse de 1763.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `institutionalized_scientific_exchange` (A) | ADD : AUS, BAV, GEN, GR4, HAN, HEK, HES, MOD (+11) | 19 | 0 | 4 |

| `periodical_print_networks` (A) | ADD : AUS, BAV, FRM, GEN, GR4, HAM, HAN, HEK (+13) | 21 | 0 | 20 |

| `specialized_technical_academies` (B) | ADD : GR4, SAR, SAX, SIC | 4 | 0 | 2 |

| `organized_elementary_schooling` (B) | ADD : AUS, HAN, PRU, SAX, WUR | 5 | 0 | 14 |

| `veterinary_science` (B) | ADD : AUS, SAR | 2 | 0 | 1 |


## 11. Médecine

`medical_degrees` est un résultat majeur : il est classé B dans le CSV, mais la réalité des facultés, examens, licences/laureae et titres reconnus est bien antérieure à 1776. La matrice le marque donc **`CLASSIFICATION_TOO_LATE` pour les 41 relations**, tout en décidant pays par pays s’il existe réellement une institution correspondante. Vingt TAG reçoivent ADD. Turin fournit un exemple particulièrement net : les constitutions universitaires de 1729 imposent cinq années d’études et la laurea pour exercer la médecine.

Les réseaux de variolisation restent beaucoup plus sélectifs : ADD à PRU, AUS, VEN, TUS, GR4 et SIC, REVIEW à SAR/PAP/GEN. Les cas C `clinicopathological_medicine` AUS/VEN sont signalés `CLASSIFICATION_REVIEW`, car des pratiques de corrélation clinique/pathologique existent avant 1776 mais le nœud gameplay paraît plus large.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `medical_degrees` (B) | CLASSIFICATION_TOO_LATE; ADD : AUS, BAV, GEN, GR3, GR4, HAN, HEK, HES (+12) | 20 | 0 | 2 |

| `variolation_networks` (B) | ADD : AUS, GR4, PRU, SIC, TUS, VEN | 6 | 0 | 3 |

| `clinicopathological_medicine` (C) | CLASSIFICATION_REVIEW; cas limites : VEN, AUS | 0 | 0 | 2 |


## 12. Militaire

La seconde passe démonte l’idée d’un paquet militaire tier 4 uniforme. Les armées de PRU/AUS/SAX/BAV/HAN/SAR et de quelques États italiens conservent ou gagnent plusieurs capacités spécialisées, tandis que les micro-États perdent souvent `standardized_field_artillery`, `light_infantry_tactics`, voire `regulated_small_arms`. La recherche distingue l’existence d’une armée permanente de la standardisation industrielle des armes, de services d’ingénieurs permanents, de la topographie militaire et des hôpitaux permanents.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `regulated_small_arms` (A) | REMOVE : BRE, FRM, GR3, HAM, HOH, HOL, LIP, LUB (+11) | 0 | 19 | 9 |

| `standardized_field_artillery` (B) | REMOVE : ANH, BAD, BRE, COB, FRM, GEN, GR3, HAM (+20) | 0 | 28 | 2 |

| `scientific_fortification_siegecraft` (A) | ADD : AUS, BAV, GEN, GR4, HAN, HEK, PRU, SAR (+4) | 12 | 0 | 5 |

| `light_infantry_tactics` (B) | REMOVE : ANH, BAD, BRE, COB, FRM, GR3, HAM, HES (+17) | 0 | 25 | 6 |

| `permanent_military_hospitals` (B) | ADD : AUS, GR4, PRU, SAR, SIC | 5 | 0 | 3 |

| `armament_standardization_inspection` (B) | ADD : AUS, PRU, SAR | 3 | 0 | 4 |

| `horse_artillery` (B) | ADD : PRU | 1 | 0 | 1 |

| `military_topographic_surveying` (B) | ADD : AUS, SAR | 2 | 0 | 2 |

| `permanent_engineer_services` (B) | ADD : AUS, BAV, GR4, HAN, PRU, SAR, SAX, SIC (+1) | 9 | 0 | 3 |

| `military_veterinary_services` (C) | CLASSIFICATION_REVIEW; cas limites : SAR, AUS | 0 | 0 | 2 |

| `field_works` (E) | aucun changement majeur | 0 | 0 | 0 |


## 13. Marine

Venise ressort comme le profil naval le plus riche de la région : Arsenal, architecture navale et structures d’État justifient plusieurs ADD. Naples/SIC et Piémont-Sardaigne obtiennent également des capacités de dockyard/architecture documentables. Gênes conserve une forte dimension marchande mais ses capacités navales étatiques sont traitées plus prudemment. `marine_chronometry` et `copper_sheathing` restent absentes ou REVIEW : leur existence internationale ne suffit pas à les généraliser en 1776.

| Technologie | Synthèse régionale | ADD | REMOVE | REVIEW |

|---|---|---:|---:|---:|

| `enclosed_dock_systems` (A) | ADD : BRE, GEN, GR3, GR4, HAM, LUB, PAP, PRU (+4) | 12 | 0 | 3 |

| `state_dockyard_systems` (A) | ADD : GR4, SAR, SIC, VEN | 4 | 0 | 3 |

| `scientific_naval_architecture` (A) | ADD : GR4, SAR, SIC, VEN | 4 | 0 | 2 |

| `marine_chronometry` (B) | cas limites : VEN | 0 | 0 | 1 |

| `ship_classification_surveying` (B) | ADD : VEN | 1 | 0 | 4 |

| `copper_sheathing` (B) | cas limites : VEN | 0 | 0 | 1 |


## 14. Analyse pays par pays

Chaque diagnostic ci-dessous résume les changements/reviews et le socle actuellement présent qui reste historiquement défendable. **Toutes les autres relations A/B, y compris les KEEP-ABSENT, figurent individuellement dans le CSV**.

### PRU — Prussia

- **Bilan matrice** : KEEP 33 · ADD 24 · REMOVE 2 · REVIEW 8.

- **Profil historique** : Prusse: État militaire et administratif puissant, mais cela ne vaut pas preuve automatique pour finance, industrie ou marine.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `sugar_refining`, `traditional_furniture_making`, `traditional_glassmaking`, `industrial_ceramics`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : ADD `improved_agricultural_implements`; REVIEW `advanced_crop_rotations`, `selective_breeding`; socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : ADD `applied_mineralogy`; socle maintenu `shaft_mining`.

- **Infrastructure** : ADD `organized_forestry`, `turnpike_road_networks`, `industrial_canals`; REVIEW `urbanization`.

- **Finance et économie** : ADD `political_economy`; REVIEW `classical_political_economy`.

- **Commerce / relations internationales** : REMOVE `colonization`; socle maintenu `international_relations`.

- **Administration** : ADD `systematic_population_registration`; REVIEW `systematic_cadastral_surveying`, `systematic_legal_codification`; socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`, `organized_elementary_schooling`; REVIEW `veterinary_science`; socle maintenu `specialized_technical_academies`.

- **Médecine** : ADD `variolation_networks`, `medical_degrees`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`, `permanent_military_hospitals`, `armament_standardization_inspection`, `horse_artillery`, `permanent_engineer_services`; REVIEW `military_topographic_surveying`; socle maintenu `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : ADD `enclosed_dock_systems`.

- **E/C examinées** : `colonization` REMOVE; `urbanization` REVIEW; `romanticism` REMOVE.


### AUS — Austria

- **Bilan matrice** : KEEP 36 · ADD 25 · REMOVE 1 · REVIEW 7.

- **Profil historique** : Monarchie habsbourgeoise: réformes thérésiennes, appareil militaire/administratif et institutions savantes sont réels mais territorialement hétérogènes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`, `traditional_glassmaking`, `industrial_ceramics`; REVIEW `industrial_acids`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : ADD `improved_agricultural_implements`, `selective_breeding`; REVIEW `advanced_crop_rotations`; socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : ADD `atmospheric_engine`, `applied_mineralogy`; socle maintenu `shaft_mining`.

- **Infrastructure** : ADD `organized_forestry`, `turnpike_road_networks`; REVIEW `urbanization`.

- **Finance et économie** : ADD `institutionalized_public_credit`, `political_economy`.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : ADD `systematic_population_registration`; REVIEW `systematic_cadastral_surveying`; socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`, `systematic_legal_codification`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`, `organized_elementary_schooling`, `veterinary_science`; socle maintenu `specialized_technical_academies`.

- **Médecine** : ADD `variolation_networks`, `medical_degrees`; REVIEW `clinicopathological_medicine`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`, `permanent_military_hospitals`, `armament_standardization_inspection`, `military_topographic_surveying`, `permanent_engineer_services`; REVIEW `horse_artillery`, `military_veterinary_services`; socle maintenu `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW; `romanticism` REMOVE; `clinicopathological_medicine` REVIEW [CLASSIFICATION_REVIEW]; `military_veterinary_services` REVIEW [CLASSIFICATION_REVIEW].


### BAV — Bavaria

- **Bilan matrice** : KEEP 45 · ADD 12 · REMOVE 0 · REVIEW 9.

- **Profil historique** : Bavière: État territorial important avec codification et manufactures de cour, mais moins systématiquement militaro-minier que Prusse/Autriche.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`, `traditional_glassmaking`, `industrial_ceramics`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_agricultural_implements`; socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : socle maintenu `shaft_mining`.

- **Infrastructure** : ADD `organized_forestry`; REVIEW `turnpike_road_networks`, `urbanization`.

- **Finance et économie** : REVIEW `institutionalized_public_credit`, `political_economy`.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : ADD `systematic_legal_codification`; socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`; REVIEW `organized_elementary_schooling`, `specialized_technical_academies`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`, `permanent_engineer_services`; REVIEW `permanent_military_hospitals`, `armament_standardization_inspection`; socle maintenu `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### SAX — Saxony

- **Bilan matrice** : KEEP 39 · ADD 19 · REMOVE 0 · REVIEW 8.

- **Profil historique** : Saxe: pôle manufacturier et minier majeur; Freiberg (1765) renforce nettement les capacités minières/scientifiques.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`, `traditional_glassmaking`, `industrial_ceramics`; REVIEW `industrial_acids`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : ADD `improved_agricultural_implements`, `selective_breeding`; REVIEW `advanced_crop_rotations`; socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : ADD `applied_mineralogy`; socle maintenu `shaft_mining`.

- **Infrastructure** : ADD `organized_forestry`, `turnpike_road_networks`; REVIEW `urbanization`.

- **Finance et économie** : ADD `institutionalized_public_credit`, `political_economy`.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REVIEW `systematic_population_registration`, `systematic_legal_codification`; socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`, `organized_elementary_schooling`, `specialized_technical_academies`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`, `permanent_engineer_services`; REVIEW `permanent_military_hospitals`, `armament_standardization_inspection`, `military_topographic_surveying`; socle maintenu `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### BRA — Brunswick

- **Bilan matrice** : KEEP 50 · ADD 5 · REMOVE 1 · REVIEW 11.

- **Profil historique** : Brunswick: ne pas extrapoler le tier prussien; le Harz et Fürstenberg donnent des capacités sectorielles précises, mais `railways` reste anachronique.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`, `industrial_ceramics`; REVIEW `traditional_glassmaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `applied_mineralogy`; socle maintenu `shaft_mining`.

- **Infrastructure** : ADD `organized_forestry`; REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REVIEW `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `institutionalized_scientific_exchange`, `periodical_print_networks`, `organized_elementary_schooling`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REVIEW `scientific_fortification_siegecraft`, `light_infantry_tactics`, `standardized_field_artillery`; socle maintenu `regulated_small_arms`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW; `railways` REMOVE.


### HAN — Hanover

- **Bilan matrice** : KEEP 47 · ADD 13 · REMOVE 0 · REVIEW 6.

- **Profil historique** : Hanovre: Göttingen et le Harz donnent des capacités scientifiques/minières ciblées, sans identité technologique avec la Prusse.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`, `traditional_glassmaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_agricultural_implements`, `advanced_crop_rotations`, `selective_breeding`; socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `applied_mineralogy`; socle maintenu `shaft_mining`.

- **Infrastructure** : ADD `organized_forestry`, `turnpike_road_networks`; REVIEW `urbanization`.

- **Finance et économie** : ADD `political_economy`.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`, `organized_elementary_schooling`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`, `permanent_engineer_services`; socle maintenu `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : REVIEW `enclosed_dock_systems`.

- **E/C examinées** : `urbanization` REVIEW.


### WUR — Württemberg

- **Bilan matrice** : KEEP 50 · ADD 11 · REMOVE 0 · REVIEW 5.

- **Profil historique** : Wurtemberg: proto-industrie textile et réglementation forestière importantes; capacité militaire plus limitée que Prusse/Autriche.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`, `traditional_glassmaking`, `industrial_ceramics`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_agricultural_implements`; socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `shaft_mining`.

- **Infrastructure** : ADD `organized_forestry`; REVIEW `turnpike_road_networks`, `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`, `organized_elementary_schooling`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`; REVIEW `permanent_engineer_services`; socle maintenu `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### SWI — Switzerland

- **Bilan matrice** : KEEP 46 · ADD 7 · REMOVE 1 · REVIEW 12.

- **Profil historique** : Suisse: proto-industrie textile très avancée mais institutions militaires/administratives restent cantonales et asymétriques.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`, `traditional_glassmaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_agricultural_implements`, `advanced_crop_rotations`; socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `shaft_mining`.

- **Infrastructure** : REVIEW `organized_forestry`, `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REVIEW `systematic_administrative_statistics`; socle maintenu `codified_practical_knowledge`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`; REVIEW `organized_elementary_schooling`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : REMOVE `standardized_field_artillery`; REVIEW `scientific_fortification_siegecraft`, `regulated_small_arms`, `light_infantry_tactics`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### SAR — Sardinia-Piedmont

- **Bilan matrice** : KEEP 32 · ADD 20 · REMOVE 0 · REVIEW 15.

- **Profil historique** : Piémont-Sardaigne: administration savoyarde, cadastre, écoles d'artillerie/fortification, médecine et vétérinaire fournissent des preuves institutionnelles fortes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`; REVIEW `sugar_refining`, `traditional_glassmaking`, `industrial_ceramics`, `mechanized_spinning`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : ADD `improved_agricultural_implements`; REVIEW `advanced_crop_rotations`; socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `applied_mineralogy`; socle maintenu `shaft_mining`.

- **Infrastructure** : ADD `turnpike_road_networks`; REVIEW `urbanization`.

- **Finance et économie** : REVIEW `institutionalized_public_credit`, `commercial_insurance_markets`, `political_economy`.

- **Commerce / relations internationales** : REVIEW `commercial_insurance_markets`; socle maintenu `international_relations`.

- **Administration** : ADD `systematic_cadastral_surveying`, `systematic_legal_codification`; REVIEW `systematic_population_registration`; socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`, `specialized_technical_academies`, `veterinary_science`; REVIEW `organized_elementary_schooling`.

- **Médecine** : ADD `medical_degrees`; REVIEW `variolation_networks`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`, `permanent_military_hospitals`, `armament_standardization_inspection`, `military_topographic_surveying`, `permanent_engineer_services`; REVIEW `military_veterinary_services`; socle maintenu `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : ADD `enclosed_dock_systems`, `state_dockyard_systems`, `scientific_naval_architecture`; REVIEW `ship_classification_surveying`.

- **E/C examinées** : `urbanization` REVIEW; `military_veterinary_services` REVIEW [CLASSIFICATION_REVIEW].


### VEN — Venice

- **Bilan matrice** : KEEP 32 · ADD 19 · REMOVE 0 · REVIEW 16.

- **Profil historique** : Venise: Arsenal, dette publique, crédit, commerce et Padoue produisent un profil naval-financier-scientifique exceptionnel malgré le déclin politique.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `sugar_refining`, `traditional_furniture_making`, `traditional_glassmaking`, `industrial_ceramics`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_agricultural_implements`, `advanced_crop_rotations`; socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `shaft_mining`.

- **Infrastructure** : REVIEW `turnpike_road_networks`, `industrial_canals`, `urbanization`.

- **Finance et économie** : ADD `institutionalized_public_credit`, `commercial_insurance_markets`, `stock_exchange`; REVIEW `political_economy`.

- **Commerce / relations internationales** : ADD `commercial_insurance_markets`, `stock_exchange`; REVIEW `colonization`; socle maintenu `international_relations`.

- **Administration** : REVIEW `systematic_population_registration`, `systematic_cadastral_surveying`; socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`; socle maintenu `specialized_technical_academies`.

- **Médecine** : ADD `variolation_networks`, `medical_degrees`; REVIEW `clinicopathological_medicine`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`, `permanent_engineer_services`; REVIEW `light_infantry_tactics`, `permanent_military_hospitals`; socle maintenu `regulated_small_arms`, `standardized_field_artillery`.

- **Marine** : ADD `enclosed_dock_systems`, `state_dockyard_systems`, `scientific_naval_architecture`, `ship_classification_surveying`; REVIEW `marine_chronometry`, `copper_sheathing`.

- **E/C examinées** : `colonization` REVIEW; `urbanization` REVIEW; `clinicopathological_medicine` REVIEW [CLASSIFICATION_REVIEW].


### GEN — Most Serene Republic of Genoa

- **Bilan matrice** : KEEP 41 · ADD 14 · REMOVE 1 · REVIEW 10.

- **Profil historique** : Gênes: république marchande avec crédit ancien et manufactures de soie; la marine d'État de 1776 est plus limitée que son héritage commercial.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `sugar_refining`, `traditional_furniture_making`, `traditional_glassmaking`, `industrial_ceramics`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : ADD `institutionalized_public_credit`, `commercial_insurance_markets`, `stock_exchange`.

- **Commerce / relations internationales** : ADD `commercial_insurance_markets`, `stock_exchange`; socle maintenu `international_relations`.

- **Administration** : socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`; socle maintenu `specialized_technical_academies`.

- **Médecine** : ADD `medical_degrees`; REVIEW `variolation_networks`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`; REMOVE `standardized_field_artillery`; REVIEW `regulated_small_arms`, `light_infantry_tactics`, `permanent_engineer_services`.

- **Marine** : ADD `enclosed_dock_systems`; REVIEW `state_dockyard_systems`, `scientific_naval_architecture`, `ship_classification_surveying`.

- **E/C examinées** : `urbanization` REVIEW.


### TUS — Tuscany

- **Bilan matrice** : KEEP 35 · ADD 14 · REMOVE 1 · REVIEW 16.

- **Profil historique** : Toscane: réformes léopoldines, commerce de Livourne et traditions manufacturières fortes; plusieurs réformes culminent toutefois après 1776.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `sugar_refining`, `traditional_furniture_making`, `traditional_glassmaking`, `industrial_ceramics`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : ADD `improved_agricultural_implements`; REVIEW `advanced_crop_rotations`; socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : socle maintenu `shaft_mining`.

- **Infrastructure** : ADD `turnpike_road_networks`; REVIEW `urbanization`.

- **Finance et économie** : ADD `political_economy`; REVIEW `institutionalized_public_credit`, `commercial_insurance_markets`, `classical_political_economy`.

- **Commerce / relations internationales** : REVIEW `commercial_insurance_markets`; socle maintenu `international_relations`.

- **Administration** : REVIEW `systematic_population_registration`, `systematic_cadastral_surveying`, `systematic_legal_codification`; socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`; REVIEW `organized_elementary_schooling`, `specialized_technical_academies`.

- **Médecine** : ADD `variolation_networks`, `medical_degrees`.

- **Militaire terrestre** : REMOVE `standardized_field_artillery`; REVIEW `scientific_fortification_siegecraft`, `regulated_small_arms`, `light_infantry_tactics`.

- **Marine** : ADD `enclosed_dock_systems`; REVIEW `state_dockyard_systems`, `scientific_naval_architecture`.

- **E/C examinées** : `urbanization` REVIEW.


### PAP — Rome

- **Bilan matrice** : KEEP 47 · ADD 8 · REMOVE 1 · REVIEW 10.

- **Profil historique** : États pontificaux: dette publique et marché secondaire anciens, universités/médecine fortes; capacités industrielles et militaires plus inégales.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`; REVIEW `traditional_glassmaking`, `industrial_ceramics`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : socle maintenu `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : ADD `institutionalized_public_credit`; REVIEW `stock_exchange`.

- **Commerce / relations internationales** : REVIEW `stock_exchange`; socle maintenu `international_relations`.

- **Administration** : socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`.

- **Médecine** : ADD `medical_degrees`; REVIEW `variolation_networks`.

- **Militaire terrestre** : REMOVE `standardized_field_artillery`; REVIEW `scientific_fortification_siegecraft`, `regulated_small_arms`, `light_infantry_tactics`.

- **Marine** : ADD `enclosed_dock_systems`; REVIEW `state_dockyard_systems`.

- **E/C examinées** : `urbanization` REVIEW.


### GR4 — Naples

- **Bilan matrice** : KEEP 41 · ADD 17 · REMOVE 0 · REVIEW 8.

- **Profil historique** : Naples: grande capitale, dette/finance, manufactures royales et académies militaires; ne pas confondre avec la Sicile insulaire.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`, `traditional_glassmaking`, `industrial_ceramics`; REVIEW `sugar_refining`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : ADD `institutionalized_public_credit`; REVIEW `commercial_insurance_markets`, `stock_exchange`.

- **Commerce / relations internationales** : REVIEW `commercial_insurance_markets`, `stock_exchange`; socle maintenu `international_relations`.

- **Administration** : socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`, `specialized_technical_academies`.

- **Médecine** : ADD `variolation_networks`, `medical_degrees`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`, `permanent_military_hospitals`, `permanent_engineer_services`; REVIEW `armament_standardization_inspection`; socle maintenu `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : ADD `enclosed_dock_systems`, `state_dockyard_systems`, `scientific_naval_architecture`; REVIEW `ship_classification_surveying`.

- **E/C examinées** : `urbanization` REVIEW.


### SIC — Two Sicilies

- **Bilan matrice** : KEEP 41 · ADD 17 · REMOVE 0 · REVIEW 8.

- **Profil historique** : TAG composite Two Sicilies: les institutions napolitaines sont pertinentes pour le setup composite, mais l'asymétrie continent/Sicile doit rester visible.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`, `traditional_glassmaking`, `industrial_ceramics`; REVIEW `sugar_refining`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : ADD `institutionalized_public_credit`; REVIEW `commercial_insurance_markets`, `stock_exchange`.

- **Commerce / relations internationales** : REVIEW `commercial_insurance_markets`, `stock_exchange`; socle maintenu `international_relations`.

- **Administration** : socle maintenu `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`, `specialized_technical_academies`.

- **Médecine** : ADD `variolation_networks`, `medical_degrees`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`, `permanent_military_hospitals`, `permanent_engineer_services`; REVIEW `armament_standardization_inspection`; socle maintenu `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : ADD `enclosed_dock_systems`, `state_dockyard_systems`, `scientific_naval_architecture`; REVIEW `ship_classification_surveying`.

- **E/C examinées** : `urbanization` REVIEW.


### GR3 — Sicily

- **Bilan matrice** : KEEP 52 · ADD 4 · REMOVE 6 · REVIEW 4.

- **Profil historique** : Sicile: économie et institutions propres; ne pas copier automatiquement toutes les capacités de Naples.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : ADD `enclosed_dock_systems`.

- **E/C examinées** : `urbanization` REVIEW.


### ANH — Anhalt

- **Bilan matrice** : KEEP 53 · ADD 2 · REMOVE 5 · REVIEW 6.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`, `organized_elementary_schooling`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `light_infantry_tactics`, `standardized_field_artillery`; REVIEW `regulated_small_arms`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### BAD — Baden

- **Bilan matrice** : KEEP 50 · ADD 4 · REMOVE 3 · REVIEW 9.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`, `traditional_glassmaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `shaft_mining`.

- **Infrastructure** : REVIEW `organized_forestry`, `urbanization`.

- **Finance et économie** : REVIEW `political_economy`.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `systematic_administrative_statistics`; REVIEW `codified_practical_knowledge`.

- **Science / éducation** : REVIEW `institutionalized_scientific_exchange`, `periodical_print_networks`, `organized_elementary_schooling`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `light_infantry_tactics`, `standardized_field_artillery`; REVIEW `regulated_small_arms`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### BRE — Bremen

- **Bilan matrice** : KEEP 50 · ADD 3 · REMOVE 6 · REVIEW 7.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`, `sugar_refining`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : REVIEW `commercial_insurance_markets`.

- **Commerce / relations internationales** : REVIEW `commercial_insurance_markets`; socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : ADD `enclosed_dock_systems`.

- **E/C examinées** : `urbanization` REVIEW.


### COB — Saxe-Coburg-Gotha

- **Bilan matrice** : KEEP 53 · ADD 2 · REMOVE 5 · REVIEW 6.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`, `organized_elementary_schooling`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `light_infantry_tactics`, `standardized_field_artillery`; REVIEW `regulated_small_arms`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### FRM — Frankfurt

- **Bilan matrice** : KEEP 48 · ADD 4 · REMOVE 4 · REVIEW 10.

- **Profil historique** : Francfort: grande place commerciale et boursière, mais l'existence d'une bourse de change ne signifie pas encore un marché moderne de titres d'État.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : REVIEW `institutionalized_public_credit`, `commercial_insurance_markets`, `stock_exchange`.

- **Commerce / relations internationales** : REVIEW `commercial_insurance_markets`, `stock_exchange`; socle maintenu `international_relations`.

- **Administration** : REVIEW `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `periodical_print_networks`; REVIEW `institutionalized_scientific_exchange`.

- **Médecine** : REVIEW `medical_degrees`.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### HAM — Hamburg

- **Bilan matrice** : KEEP 46 · ADD 7 · REMOVE 4 · REVIEW 9.

- **Profil historique** : Hambourg: place de commerce et d'assurance maritime de premier rang; faible logique d'attribution des technologies terrestres prussiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `sugar_refining`, `traditional_furniture_making`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : ADD `commercial_insurance_markets`; REVIEW `institutionalized_public_credit`, `stock_exchange`.

- **Commerce / relations internationales** : ADD `commercial_insurance_markets`; REVIEW `stock_exchange`; socle maintenu `international_relations`.

- **Administration** : REVIEW `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `periodical_print_networks`; REVIEW `institutionalized_scientific_exchange`.

- **Médecine** : REVIEW `medical_degrees`.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : ADD `enclosed_dock_systems`.

- **E/C examinées** : `urbanization` REVIEW.


### HEK — Hesse-Kassel

- **Bilan matrice** : KEEP 52 · ADD 6 · REMOVE 0 · REVIEW 8.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`, `traditional_glassmaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `shaft_mining`.

- **Infrastructure** : REVIEW `organized_forestry`, `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REVIEW `systematic_administrative_statistics`; socle maintenu `codified_practical_knowledge`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`; REVIEW `organized_elementary_schooling`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : ADD `scientific_fortification_siegecraft`; REVIEW `permanent_engineer_services`; socle maintenu `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### HES — Hesse

- **Bilan matrice** : KEEP 51 · ADD 6 · REMOVE 1 · REVIEW 8.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`; REVIEW `traditional_glassmaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REVIEW `shaft_mining`.

- **Infrastructure** : REVIEW `organized_forestry`, `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REVIEW `systematic_administrative_statistics`; socle maintenu `codified_practical_knowledge`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`; REVIEW `organized_elementary_schooling`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : REMOVE `light_infantry_tactics`; REVIEW `scientific_fortification_siegecraft`, `standardized_field_artillery`; socle maintenu `regulated_small_arms`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### HOH — Hohenzollern

- **Bilan matrice** : KEEP 54 · ADD 2 · REMOVE 6 · REVIEW 4.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### HOL — Holstein

- **Bilan matrice** : KEEP 52 · ADD 2 · REMOVE 6 · REVIEW 6.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`, `organized_elementary_schooling`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : REVIEW `enclosed_dock_systems`.

- **E/C examinées** : `urbanization` REVIEW.


### LIP — Lippe

- **Bilan matrice** : KEEP 54 · ADD 2 · REMOVE 6 · REVIEW 4.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### LUB — Lübeck

- **Bilan matrice** : KEEP 50 · ADD 3 · REMOVE 6 · REVIEW 7.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`, `sugar_refining`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : REVIEW `commercial_insurance_markets`.

- **Commerce / relations internationales** : REVIEW `commercial_insurance_markets`; socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : ADD `enclosed_dock_systems`.

- **E/C examinées** : `urbanization` REVIEW.


### MEC — Mecklenburg

- **Bilan matrice** : KEEP 54 · ADD 2 · REMOVE 6 · REVIEW 4.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### MEI — Saxe-Meiningen

- **Bilan matrice** : KEEP 53 · ADD 2 · REMOVE 5 · REVIEW 6.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`, `organized_elementary_schooling`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `light_infantry_tactics`, `standardized_field_artillery`; REVIEW `regulated_small_arms`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### MST — Mecklenburg-Strelitz

- **Bilan matrice** : KEEP 54 · ADD 2 · REMOVE 6 · REVIEW 4.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### NAS — Nassau

- **Bilan matrice** : KEEP 54 · ADD 2 · REMOVE 6 · REVIEW 4.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### OLD — Oldenburg

- **Bilan matrice** : KEEP 54 · ADD 2 · REMOVE 6 · REVIEW 4.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### SCH — Schleswig

- **Bilan matrice** : KEEP 52 · ADD 2 · REMOVE 6 · REVIEW 6.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`, `organized_elementary_schooling`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : REVIEW `enclosed_dock_systems`.

- **E/C examinées** : `urbanization` REVIEW.


### SCM — Schaumburg-Lippe

- **Bilan matrice** : KEEP 54 · ADD 2 · REMOVE 6 · REVIEW 4.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### SCW — Schwarzburg

- **Bilan matrice** : KEEP 54 · ADD 2 · REMOVE 6 · REVIEW 4.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### WEI — Saxe-Weimar

- **Bilan matrice** : KEEP 52 · ADD 5 · REMOVE 4 · REVIEW 5.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `systematic_administrative_statistics`; socle maintenu `codified_practical_knowledge`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`; REVIEW `organized_elementary_schooling`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : REMOVE `light_infantry_tactics`, `standardized_field_artillery`; REVIEW `regulated_small_arms`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### WLD — Waldeck

- **Bilan matrice** : KEEP 54 · ADD 2 · REMOVE 6 · REVIEW 4.

- **Profil historique** : État germanique secondaire ou micro-État ; la proximité institutionnelle avec le Saint-Empire ne justifie pas le transfert automatique des capacités prussiennes, saxonnes ou autrichiennes.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_furniture_making`; REVIEW `traditional_papermaking`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### LUC — Lucca

- **Bilan matrice** : KEEP 53 · ADD 3 · REMOVE 6 · REVIEW 4.

- **Profil historique** : État italien secondaire ; ne pas projeter automatiquement sur lui les capacités de Venise, Naples ou Piémont. Les institutions locales sont évaluées séparément.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : REVIEW `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REMOVE `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : REVIEW `periodical_print_networks`.

- **Médecine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### MOD — Modena

- **Bilan matrice** : KEEP 51 · ADD 6 · REMOVE 4 · REVIEW 5.

- **Profil historique** : État italien secondaire ; ne pas projeter automatiquement sur lui les capacités de Venise, Naples ou Piémont. Les institutions locales sont évaluées séparément.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`; REVIEW `traditional_glassmaking`, `industrial_ceramics`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REVIEW `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


### PAR — Parma

- **Bilan matrice** : KEEP 51 · ADD 6 · REMOVE 4 · REVIEW 5.

- **Profil historique** : État italien secondaire ; ne pas projeter automatiquement sur lui les capacités de Venise, Naples ou Piémont. Les institutions locales sont évaluées séparément.

- **Production et artisanat** : ADD `traditional_food_processing`, `traditional_papermaking`, `traditional_furniture_making`; REVIEW `traditional_glassmaking`, `industrial_ceramics`; socle maintenu `distillation`, `organized_textile_production`.

- **Agriculture** : socle maintenu `improved_husbandry`.

- **Mines / métallurgie** : REMOVE `shaft_mining`.

- **Infrastructure** : REVIEW `urbanization`.

- **Finance et économie** : aucun changement majeur; les capacités non démontrées restent absentes.

- **Commerce / relations internationales** : socle maintenu `international_relations`.

- **Administration** : REVIEW `codified_practical_knowledge`, `systematic_administrative_statistics`.

- **Science / éducation** : ADD `institutionalized_scientific_exchange`, `periodical_print_networks`.

- **Médecine** : ADD `medical_degrees`.

- **Militaire terrestre** : REMOVE `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`.

- **Marine** : aucun changement majeur; les capacités non démontrées restent absentes.

- **E/C examinées** : `urbanization` REVIEW.


## 15. TREE_STRUCTURE_REVIEW

**10 relations** nécessitent une révision de structure d’arbre, après décision historique. **108 ADD** supplémentaires sont historiquement justifiés avec des parents eux-mêmes plausibles (`ADD_WITH_PREREQUISITES`).

| TAG | Technologie | Décision | Problème d’arbre |

|---|---|---|---|

| AUS | `atmospheric_engine` | ADD | Parent(s) non justifié(s) historiquement: coke_smelting=ABSENT |

| AUS | `political_economy` | ADD | Parent(s) non justifié(s) historiquement: commercial_insurance_markets=ABSENT |

| GR3 | `medical_degrees` | ADD | Parent(s) non justifié(s) historiquement: institutionalized_scientific_exchange=ABSENT |

| HAN | `political_economy` | ADD | Parent(s) non justifié(s) historiquement: commercial_insurance_markets=ABSENT |

| PRU | `political_economy` | ADD | Parent(s) non justifié(s) historiquement: commercial_insurance_markets=ABSENT |

| SAX | `political_economy` | ADD | Parent(s) non justifié(s) historiquement: commercial_insurance_markets=ABSENT |

| VEN | `clinicopathological_medicine` | REVIEW | Le parent C `experimental_research_laboratories` est plus tardif/plus large que la pratique anatomoclinique effectivement attestée. |

| AUS | `clinicopathological_medicine` | REVIEW | Le parent C `experimental_research_laboratories` ne reflète pas correctement l'origine clinique/anatomique de cette capacité. |

| SAR | `military_veterinary_services` | REVIEW | Le parent `horse_artillery` ne doit pas conditionner historiquement un service vétérinaire militaire attesté indépendamment. |

| AUS | `military_veterinary_services` | REVIEW | Le parent `horse_artillery` ne représente pas la chaîne historique réelle de la formation vétérinaire militaire. |


Règle spécifique de cette seconde passe : les anciennes dépendances de `traditional_papermaking`, `traditional_glassmaking` et `traditional_furniture_making` vers `organized_forestry` ne sont **pas** réintroduites artificiellement. Le logging rudimentaire ne constitue pas non plus une preuve d’`organized_forestry`.

## 16. CLASSIFICATION_REVIEW

### CLASSIFICATION_TOO_EARLY

- `mechanized_weaving` (B) : **41 relations**. Le gameplay représente une mécanisation industrielle postérieure au 1er janvier 1776.

- `advanced_spinning` (B) : **41 relations**. Le gameplay débloque notamment des machines à coudre nettement postérieures au cutoff.

- `classical_political_economy` (B) : **41 relations**. Au 1er janvier 1776, le système classique/libre-échangiste représenté par le nœud n’est pas encore pleinement constitué ; TUS/PRU restent REVIEW pour des précurseurs.

### CLASSIFICATION_TOO_LATE

- `medical_degrees` (B) : **41 relations**. La capacité institutionnelle (facultés, examens, licences/laureae, titres reconnus) est ancienne ; le caractère « frontière » du nœud est trop tardif globalement.

### CLASSIFICATION_REVIEW au sens strict des technologies C

- `clinicopathological_medicine` : AUS et VEN → REVIEW ; présence de pratiques précoces mais nœud gameplay plus large.

- `military_veterinary_services` : AUS et SAR → REVIEW ; institutions vétérinaires/militaires précoces mais branche gameplay et parent `horse_artillery` discutables.

Total demandé `CLASSIFICATION_REVIEW` : **4 relations**, sur **2 technologies C**.

## 17. Principales différences avec la première passe

La première matrice contenait **479 lignes** (KEEP 336, ADD 13, REMOVE 4, REVIEW 126). La seconde passe contient **2713 lignes** et **224 relations déjà présentes dans la première matrice changent de décision**.

Différences de méthode et de fond :

1. Audit exhaustif des 61 technologies A/B pour chacun des 41 TAG au lieu d’un échantillon ciblé.

2. Fin du raisonnement par tier : les micro-États ne reçoivent plus automatiquement mines profondes, artillerie standardisée, statistiques ou doctrine d’infanterie légère.

3. Réhabilitation des capacités fondamentales sous-évaluées : papier, meuble, verre, alimentation, diplômes médicaux, réseaux savants, crédit public.

4. Nouvelle définition stricte de `organized_forestry`, indépendante du papier/verre/meuble.

5. Finance dissociée de la puissance militaire : VEN/GEN/PAP/GR4/SIC gagnent du crédit public là où PRU ne l’obtient pas.

6. Les prérequis ne bloquent plus une capacité attestée ; ils déclenchent `ADD_WITH_PREREQUISITES` ou `TREE_STRUCTURE_REVIEW` après le verdict historique.

7. Les classifications elles-mêmes sont auditées : 3 B trop précoces, 1 B trop tardive et 2 C à réexaminer.

## 18. Recommandations finales

### Contrôle quantitatif

| Indicateur | Résultat |
|---|---:|

| TAG | 41 |

| Technologies A auditées | 25 |

| Technologies B auditées | 36 |

| Relations A obligatoires | 1025 |

| Relations B obligatoires | 1476 |

| Lignes totales | 2713 |

| KEEP | 1970 |

| ADD | 310 |

| REMOVE | 137 |

| REVIEW | 296 |

| TREE_STRUCTURE_REVIEW | 10 |

| CLASSIFICATION_REVIEW | 4 |


### 20 changements les plus importants par rapport à la distribution actuellement implémentée

| # | TAG | Technologie | Changement | Importance |

|---:|---|---|---|---|

| 1 | BRA | `railways` | PRESENT → **REMOVE** | Retrait P0 : première ligne ferroviaire allemande en 1835, donc impossibilité absolue en 1776. |

| 2 | AUS | `romanticism` | PRESENT → **REMOVE** | Retrait : le nœud est postérieur au cutoff. |

| 3 | PRU | `romanticism` | PRESENT → **REMOVE** | Retrait : le nœud est postérieur au cutoff. |

| 4 | PRU | `colonization` | PRESENT → **REMOVE** | Retrait du nœud E : capacité institutionnelle coloniale non démontrée pour la Prusse de 1776. |

| 5 | VEN | `institutionalized_public_credit` | ABSENT → **ADD** | Ajout : dette publique et marchés de crédit structurés. |

| 6 | GEN | `institutionalized_public_credit` | ABSENT → **ADD** | Ajout : tradition institutionnelle de dette publique / Casa di San Giorgio. |

| 7 | PAP | `institutionalized_public_credit` | ABSENT → **ADD** | Ajout : dette publique pontificale et marché secondaire durable. |

| 8 | GR4 | `institutionalized_public_credit` | ABSENT → **ADD** | Ajout : marché financier napolitain autonome au XVIIIe siècle. |

| 9 | SIC | `institutionalized_public_credit` | ABSENT → **ADD** | Ajout : même capacité structurelle du royaume méridional représenté par SIC. |

| 10 | AUS | `institutionalized_public_credit` | ABSENT → **ADD** | Ajout sectoriel : Wiener Stadtbank et dispositifs de crédit public. |

| 11 | SAX | `institutionalized_public_credit` | ABSENT → **ADD** | Ajout sectoriel : institutions de crédit public saxonnes après 1763. |

| 12 | AUS | `atmospheric_engine` | ABSENT → **ADD** | Ajout FRONTIER : machine atmosphérique attestée dans la monarchie habsbourgeoise dès 1721–1722. |

| 13 | SAR | `systematic_cadastral_surveying` | ABSENT → **ADD** | Ajout : cadastre savoyard/piémontais systématique du XVIIIe siècle. |

| 14 | SAR | `specialized_technical_academies` | ABSENT → **ADD** | Ajout : écoles d’artillerie et de fortification de Turin. |

| 15 | SAX | `specialized_technical_academies` | ABSENT → **ADD** | Ajout : Bergakademie Freiberg fondée en 1765. |

| 16 | GR4 | `specialized_technical_academies` | ABSENT → **ADD** | Ajout : institutions techniques/militaires napolitaines antérieures à 1776. |

| 17 | VEN | `state_dockyard_systems` | ABSENT → **ADD** | Ajout : Arsenal de Venise comme système d’arsenal d’État. |

| 18 | PRU | `organized_elementary_schooling` | ABSENT → **ADD** | Ajout : règlement scolaire général prussien de 1763. |

| 19 | AUS | `medical_degrees` | ABSENT → **ADD** | Ajout : réforme médicale universitaire et certification institutionnelle. |

| 20 | PRU | `medical_degrees` | ABSENT → **ADD** | Ajout sectoriel : formation/titres médicaux institutionnels; le nœud B est globalement sous-classé. |


### Corrections systémiques à ne pas perdre lors de la synthèse mondiale

- `standardized_field_artillery` — Le tier courant est trop généreux : 28 REMOVE.

- `light_infantry_tactics` — 25 REMOVE : grande armée ≠ doctrine légère institutionnalisée.

- `shaft_mining` — 23 REMOVE : présence de mines ≠ exploitation profonde avancée.

- `systematic_administrative_statistics` — 20 REMOVE : centralisation politique ≠ statistiques administratives systématiques.

- `codified_practical_knowledge` — 18 REMOVE : le nœud est trop abstrait pour être un socle automatique.

- `traditional_papermaking` — 22 ADD : papier réévalué indépendamment d’`organized_forestry`.

- `traditional_furniture_making` — 41 ADD : artisanat structuré, sans prérequis forestier artificiel.

- `traditional_food_processing` — 41 ADD : capacité artisanale fondamentale largement établie.

- `medical_degrees` — 20 ADD et reclassification globale proposée `CLASSIFICATION_TOO_LATE`.


### Verdict d’implémentation

- Ne pas réintroduire de tier régional uniforme pour résoudre cette passe.

- Utiliser la matrice comme vérité de décision pays × technologie pour la future synthèse mondiale, puis résoudre séparément les dix `TREE_STRUCTURE_REVIEW`.

- Arbitrer mondialement les six technologies signalées par une question de classification (`mechanized_weaving`, `advanced_spinning`, `classical_political_economy`, `medical_degrees`, `clinicopathological_medicine`, `military_veterinary_services`).

- Préserver les asymétries : puissance militaire prussienne, finance vénitienne/génoise/pontificale/napolitaine, industrie saxonne, administration et écoles techniques savoyardes, proto-industrie suisse.

- Aucun fichier gameplay n’a été modifié ; aucun code n’a été produit ; aucun commit/push n’a été effectué.
