# Recherche technologique — Asie orientale et Asie du Sud-Est — 1er janvier 1776

> **Nature du travail : recherche historique uniquement.** Aucun fichier de gameplay n’est modifié et aucun code Victoria 3 n’est produit. La date de référence est strictement le **1er janvier 1776**.

## 1. Périmètre

Le CSV pays contient 45 TAG dans les quatre régions directement pertinentes (North China, Northeast Asia, Indochina, Indonesia). `PPU` (Papua) est exclu malgré son classement CSV « Indonesia », car la consigne exclut le Pacifique. `TIB` (Tibet), classé « Himalayas », est inclus comme cas frontière d’Asie orientale. Le périmètre traité contient donc **45 TAG**.

**Chine :** `CHI` — China.
**Japon, Corée et Nord-Est asiatique :** `JAP` — Japan, `KOR` — Korea, `RYU` — Ryukyu, `EZO` — Ezochi, `AIN` — Ainu Mosir, `SKH` — Evenki, `ULT` — Ulta.
**Asie du Sud-Est continentale et péninsule malaise :** `BUR` — Burma, `CAM` — Cambodia, `CHP` — Champasak, `CMI` — Chiang Mai, `DAI` — Dai Nam, `DGR` — Degar, `JOH` — Johore, `KLO` — Khmer Loeu, `LUA` — Luang Prabang, `PRK` — Perak, `SCT` — Sip Song Chau Tai, `SEL` — Selangor, `SHS` — Shan, `SIA` — Siam.
**Archipel indonésien, Philippines et mers adjacentes :** `ACE` — Aceh, `BAL` — Bali, `BLG` — Bulungan, `BNJ` — Banjar, `BRU` — Brunei, `BTN` — Buton, `DEI` — East Indies, `JMB` — Jambi, `KTI` — Kutai, `LAN` — Lanfang, `MGD` — Maguindanao, `MND` — Mindanao, `PHI` — Philippines, `PON` — Pontianak, `SAK` — Siak, `SLW` — Sulawesi, `SMB` — Sambas, `SRK` — Surakarta, `STG` — Sintang, `SUL` — Sulu, `TID` — Tidore, `YOG` — Yogyakarta.
**Cas frontière :** `TIB` — Tibet.

## 2. Méthode et sources

La méthode est asymétrique : un État peut être très solide en agriculture, impression ou administration et rester faible sur un nœud militaire ou industriel. Les noms de technologies ne sont jamais pris isolément : les déblocages gameplay et les prérequis du CSV technologies sont utilisés pour interpréter chaque nœud. Une technologie enfant ne conduit pas automatiquement à ajouter son parent lorsque l’arbre encode une trajectoire institutionnelle européenne qui ne correspond pas à la trajectoire locale.

Principales familles de sources : Oxford/Cambridge pour Qing, histoire militaire et print culture; National Diet Library et collections universitaires japonaises pour le rangaku; KCI pour les registres Joseon; Isis/University of the Ryukyus pour Ryukyu; Utrecht/Cambridge pour la VOC; CSIC/PARES et International Journal of Maritime History pour les Philippines; Cambridge/SOAS/Burma Library pour l’Asie du Sud-Est.

Sources pivots (URLs complètes également reprises ligne par ligne dans la matrice CSV) :
- https://academic.oup.com/edited-volume/63143/chapter/568216247
- https://academic.oup.com/edited-volume/61799/chapter-abstract/546329755
- https://escholarship.org/uc/item/5pz1b1rm
- https://www.cambridge.org/core/books/abs/blue-frontier/guarded-management/70CF806A7E6861E63D8B052EFDE6C6B4
- https://www.ndl.go.jp/nichiran/e/data/R/042/042-001r.html
- https://journals.sagepub.com/doi/10.1177/036319908601100401
- https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002235256
- https://www.journals.uchicago.edu/doi/10.1086/726185
- https://research-portal.uu.nl/en/publications/the-formative-years-of-the-modern-corporation-the-dutch-east-indi/
- https://www.cambridge.org/core/books/wars-overseas/naval-forces-fortifications-and-firepower/CB1D563F0BB92DBE225884075C686B6E
- https://revistadeindias.revistas.csic.es/index.php/revistadeindias/article/view/1058/0
- https://journals.sagepub.com/doi/10.1177/0843871419860698
- https://www.burmalibrary.org/en/the-administration-of-the-early-konbaung-period
- https://www.cambridge.org/core/journals/international-journal-of-asian-studies/article/all-political-power-comes-from-the-barrel-of-a-gun-arms-trading-gun-control-and-revolt-in-ayutthaya-16581709/018E8EAA0AAE07CBCF41E59EC02FA5EC
- https://www.cambridge.org/core/journals/international-journal-of-asian-studies/article/introduction-the-reception-of-the-harquebus-in-east-and-southeast-asia/AD08FBBF2D32EDBC28B3AE2D7200CBCF
- https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/civilization-on-loan-the-making-of-an-upstart-polity-mataram-and-its-successors-16001830/85009FD66852BA85AC132F193587B886
- https://www.cambridge.org/core/books/abs/british-traders-in-the-east-indies-17701820/political-allies-country-traders-and-the-malays-ii/D01FB8EF5722A08C3BA43B9E67F91D4C
- https://www.cambridge.org/core/services/aop-cambridge-core/content/view/84EFF842726212C9A430E41FDC1B94CC/S0022463400009322a.pdf/slave_markets_and_exchange_in_the_malay_world_the_sulu_sultanate_17701878.pdf
- https://www.cambridge.org/core/books/abs/chinese-indonesians/makam-juang-mandor-monument-remembering-and-distorting-the-history-of-the-chinese-of-west-kalimantan/1C7EF6F2A78826DF81EE6D9AAB8C9ABF
- https://www.cambridge.org/core/journals/international-journal-of-asian-studies/article/river-of-fire-and-ice-infrastructure-territoriality-and-the-colonization-of-eastern-hokkaido-japan-1600s1900s/7529A9AC3A37E5E2DBF449B87B1F2553
- https://escholarship.org/uc/item/0bk7n662

## 3. Diagnostic régional

### Asie orientale
La Chine Qing de 1776 combine agriculture intensive, proto-industries textiles, très vaste culture imprimée, bureaucratie fiscale et démographique, grands travaux hydrauliques, mines de cuivre organisées et appareil militaire/naval réel. La faiblesse relative de l’innovation militaire au XVIIIe siècle ne doit pas effacer ces capacités. L’analyse recommande donc plusieurs ajouts explicites plutôt qu’un relèvement uniforme de tier.

Le Japon Tokugawa possède une urbanisation et un marché du livre très développés, des registres de population anciens, des enquêtes foncières et une circulation savante rangaku suffisamment concrète pour justifier `institutionalized_scientific_exchange`. En revanche, les nœuds tactiques/artillerie du tier 4 et les interprétations navales de type Meiji doivent être dissociés de la réalité de 1776.

Joseon combine administration centralisée, registres de ménages, impression contrôlée par l’État et usage/fabrication d’armes à feu. Ryukyu constitue un cas remarquable de capacité cadastrale et forestière institutionnalisée avant 1776. Ezochi/Ainu, Sakhaline et les sociétés du Nord-Est doivent être traités comme économies et structures politiques propres, non comme des extensions technologiques automatiques du Japon.

### Asie du Sud-Est
La région n’est pas technologiquement homogène. Les États continentaux comme Konbaung, Đại Việt et Thonburi disposent d’administrations, de fiscalité et de traditions militaires fortes; les États maritimes se distinguent par commerce, navigation, ports et artillerie côtière. La présence d’armes à feu est ancienne dans toute la région, mais elle ne prouve pas automatiquement une artillerie de campagne standardisée ou une industrie d’armes à l’échelle nationale.

Les sultanats malais et indonésiens participent à des réseaux internationaux très denses. Pour plusieurs petits TAG du tier 4, les nœuds `light_infantry_tactics`, `standardized_field_artillery`, `shaft_mining` et parfois `systematic_administrative_statistics` sont trop génériques pour être validés sans réserves. La matrice utilise donc davantage REVIEW/REMOVE plutôt qu’un nivellement arbitraire.

### Colonies européennes
`DEI` et `PHI` sont évalués selon les infrastructures effectivement présentes en Asie. Pour DEI, fortifications, réseau naval, Batavia et appareil VOC sont locaux et justifient plusieurs nœuds militaires/navals. Pour les Philippines, Cavite/Manila et le système de fortification du XVIIIe siècle justifient des nœuds de dockyards/fortification. Cela ne signifie pas que l’ensemble des technologies néerlandaises ou espagnoles est copié à la colonie.

## 4. Analyse pays par pays

### ACE — Aceh

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `light_infantry_tactics` (SECTORAL), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `standardized_field_artillery` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (1 HIGH / 10 MEDIUM / 0 LOW dans la matrice)

### AIN — Ainu Mosir

- **Current tier:** `tier_7`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** —
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** aucun cas majeur retenu
- **Justification historique:** Le tier 7 vide évite de projeter des institutions étatiques/industrielles inadéquates. Cela ne signifie pas absence de techniques locales : le modèle de technologie du jeu représente mal plusieurs savoir-faire autochtones; aucune ADD n’est proposée sans correspondance gameplay suffisamment défendable.
- **Sources:** —
- **Confiance générale:** MEDIUM (0 HIGH / 0 MEDIUM / 0 LOW dans la matrice)

### BAL — Bali

- **Current tier:** `tier_5`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `shaft_mining`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `shaft_mining` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/civilization-on-loan-the-making-of-an-upstart-polity-mataram-and-its-successors-16001830/85009FD66852BA85AC132F193587B886 ; https://www.jstor.org/stable/jj.33506918.18
- **Confiance générale:** MEDIUM (0 HIGH / 6 MEDIUM / 0 LOW dans la matrice)

### BLG — Bulungan

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### BNJ — Banjar

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### BRU — Brunei

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `light_infantry_tactics` (SECTORAL), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `standardized_field_artillery` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (1 HIGH / 10 MEDIUM / 0 LOW dans la matrice)

### BTN — Buton

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### BUR — Burma

- **Current tier:** `tier_5`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `international_relations`, `regulated_small_arms`, `scientific_fortification_siegecraft`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `shaft_mining` (SECTORAL), `urbanization` (ABSTRACT), `regulated_small_arms` (SECTORAL), `standardized_field_artillery` (FRONTIER)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents.
- **Justification historique:** La documentation Konbaung 1752–1776 montre une administration centralisée et des relations extérieures actives; les transformations militaires des années 1760 rendent plusieurs nœuds militaires plausibles, mais la standardisation de l’artillerie reste REVIEW.
- **Sources:** https://www.burmalibrary.org/en/the-administration-of-the-early-konbaung-period ; https://www.burmalibrary.org/mm/additional-burmese-historical-sources-1752-76 ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://www.cambridge.org/core/journals/international-journal-of-asian-studies/article/introduction-the-reception-of-the-harquebus-in-east-and-southeast-asia/AD08FBBF2D32EDBC28B3AE2D7200CBCF
- **Confiance générale:** MEDIUM (2 HIGH / 8 MEDIUM / 0 LOW dans la matrice)

### CAM — Cambodia

- **Current tier:** `tier_5`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `international_relations`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `selective_breeding`, `shaft_mining`
- **Technologies frontière/sectorielles:** `selective_breeding` (ABSTRACT), `codified_practical_knowledge` (ABSTRACT), `shaft_mining` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://digitalcommons.unl.edu/tsaconf/528/ ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (0 HIGH / 8 MEDIUM / 0 LOW dans la matrice)

### CHI — China

- **Current tier:** `tier_5`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `international_relations`, `systematic_legal_codification`, `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `regulated_small_arms`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `systematic_population_registration`, `traditional_papermaking`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `coke_smelting`, `periodical_print_networks`, `scientific_naval_architecture`, `systematic_cadastral_surveying`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `urbanization` (ABSTRACT), `coke_smelting` (ABSTRACT), `periodical_print_networks` (ABSTRACT), `regulated_small_arms` (SECTORAL), `scientific_naval_architecture` (SECTORAL), `systematic_cadastral_surveying` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `coke_smelting`: Missing parent(s): organized_forestry. Do not add automatically; resolve by historical justification or tree abstraction. ; `traditional_papermaking`: organized_forestry is missing unless separately recommended. Papermaking is historically established independently of the tree abstraction; do not auto-grant the parent solely to repair the chain.
- **Justification historique:** Le tier 5 sous-représente certaines capacités Qing : imprimerie/papier, population registration, fortifications et systèmes navals. La métallurgie doit être traitée prudemment : usage ancien du charbon ≠ preuve du nœud Darby-style `coke_smelting`. Le cadastre moderne reste REVIEW malgré l’existence de registres fonciers.
- **Sources:** https://www.cambridge.org/core/books/abs/economic-change-in-china-c18001950/industry-traditional-and-modern/8D80FCFD69BEA6FD1F817BAACD79B3B7 ; https://academic.oup.com/edited-volume/63143/chapter/568216247 ; https://journals.sagepub.com/doi/10.1177/000944559603200403 ; https://www.cambridge.org/core/journals/social-science-history/article/abs/public-interest-and-the-financing-of-local-water-control-in-qing-china-17501850/D47BD12B8D0A7996A99CDD4F9847E84F ; https://escholarship.org/uc/item/5pz1b1rm
- **Confiance générale:** HIGH (9 HIGH / 8 MEDIUM / 0 LOW dans la matrice)

### CHP — Champasak

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/abs/british-traders-in-the-east-indies-17701820/political-allies-country-traders-and-the-malays-ii/D01FB8EF5722A08C3BA43B9E67F91D4C ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### CMI — Chiang Mai

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/abs/british-traders-in-the-east-indies-17701820/political-allies-country-traders-and-the-malays-ii/D01FB8EF5722A08C3BA43B9E67F91D4C ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### DAI — Dai Nam

- **Current tier:** `tier_5`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `international_relations`, `regulated_small_arms`, `scientific_fortification_siegecraft`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `selective_breeding`, `shaft_mining`, `state_dockyard_systems`
- **Technologies frontière/sectorielles:** `selective_breeding` (ABSTRACT), `codified_practical_knowledge` (ABSTRACT), `shaft_mining` (SECTORAL), `urbanization` (ABSTRACT), `state_dockyard_systems` (SECTORAL)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents.
- **Justification historique:** Le Đại Việt du XVIIIe siècle conserve une forte tradition administrative et une longue intégration des firearms; la littérature récente souligne l’habileté des gunners vietnamiens. Les systèmes navals sont plausibles mais restent REVIEW faute de preuve assez précise pour le 1er janvier 1776.
- **Sources:** https://www.cambridge.org/core/journals/international-journal-of-asian-studies/article/introduction-the-reception-of-the-harquebus-in-east-and-southeast-asia/AD08FBBF2D32EDBC28B3AE2D7200CBCF ; https://www.cambridge.org/core/journals/journal-of-southeast-asian-studies/article/abs/changing-nature-of-the-red-river-delta-villages-during-the-le-period-14281788/BC20DE6D50EDC9AC8FCD5138E0E8528B ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (2 HIGH / 9 MEDIUM / 0 LOW dans la matrice)

### DEI — East Indies

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `colonization`, `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`
- **Technologies à REMOVE:** `joint_stock_companies`
- **Technologies à REVIEW:** `shaft_mining`, `periodical_print_networks`
- **Technologies frontière/sectorielles:** `colonization` (ABSTRACT), `codified_practical_knowledge` (ABSTRACT), `light_infantry_tactics` (SECTORAL), `shaft_mining` (SECTORAL), `urbanization` (ABSTRACT), `periodical_print_networks` (ABSTRACT), `scientific_naval_architecture` (SECTORAL)
- **Prérequis problématiques:** `joint_stock_companies`: Missing parents: commercial_insurance_markets, postal_savings. Do NOT add automatically; postal_savings is itself post-1776 and strengthens the REMOVE decision. ; `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents.
- **Justification historique:** P0 : `joint_stock_companies` doit être retirée. La VOC est bien une corporation moderne au sens juridique, mais le nœud du jeu dépend de `postal_savings` et ouvre `laissez_faire`/des capacités générales de compagnies; il encode donc un régime financier beaucoup plus tardif qu’une compagnie à charte isolée. À l’inverse, fortifications, arsenaux et réseau naval sont réellement implantés localement.
- **Sources:** https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/opium-and-the-company-maritime-trade-and-imperial-finances-on-java-16841796/284C31A46D9A26AB6C12D942D62AC5F9 ; https://www.cambridge.org/core/books/wars-overseas/naval-forces-fortifications-and-firepower/CB1D563F0BB92DBE225884075C686B6E ; https://research-portal.uu.nl/en/publications/the-formative-years-of-the-modern-corporation-the-dutch-east-indi/ ; https://www.cambridge.org/core/journals/journal-of-southeast-asian-studies/article/abs/between-batavia-and-the-cape-shipping-patterns-of-the-dutch-east-india-company/9CD79760674B0AE0363828DF9FDE9C6D
- **Confiance générale:** MEDIUM (9 HIGH / 9 MEDIUM / 0 LOW dans la matrice)

### DGR — Degar

- **Current tier:** `tier_6`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `improved_husbandry`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `urbanization`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** aucun cas majeur retenu
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 2 MEDIUM / 0 LOW dans la matrice)

### EZO — Ezochi

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `distillation`, `international_relations`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `improved_husbandry` (SECTORAL), `organized_textile_production` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (SECTORAL)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Ezochi est une zone mixte Matsumae–Ainu structurée par postes de traite, pêche et réseaux fluviaux/maritimes. Le tier 4 ne doit pas transformer cette frontière commerciale en État doté automatiquement d’artillerie standardisée, mines souterraines et urbanisation générale.
- **Sources:** https://www.cambridge.org/core/journals/international-journal-of-asian-studies/article/river-of-fire-and-ice-infrastructure-territoriality-and-the-colonization-of-eastern-hokkaido-japan-1600s1900s/7529A9AC3A37E5E2DBF449B87B1F2553 ; https://academic.oup.com/book/45713/chapter-abstract/398152533
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### JAP — Japan

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `institutionalized_scientific_exchange`, `systematic_cadastral_surveying`, `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `systematic_population_registration`, `traditional_papermaking`
- **Technologies à REMOVE:** `light_infantry_tactics`
- **Technologies à REVIEW:** `colonization`, `standardized_field_artillery`, `periodical_print_networks`, `scientific_naval_architecture`
- **Technologies frontière/sectorielles:** `colonization` (ABSTRACT), `codified_practical_knowledge` (ABSTRACT), `standardized_field_artillery` (SECTORAL), `urbanization` (ABSTRACT), `periodical_print_networks` (ABSTRACT), `scientific_naval_architecture` (SECTORAL)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `scientific_naval_architecture`: Missing parent(s): state_dockyard_systems. Do not add automatically; resolve by historical justification or tree abstraction. ; `traditional_papermaking`: organized_forestry is missing unless separately recommended. Papermaking is historically established independently of the tree abstraction; do not auto-grant the parent solely to repair the chain.
- **Justification historique:** Le Japon de 1776 possède urbanisation, édition commerciale, registres de population et rangaku (Kaitai Shinsho, 1774). La recommandation retire les nœuds tactiques/artillerie trop génériques du tier 4 et conserve l’échange scientifique/cadastre sans projeter les institutions de Meiji.
- **Sources:** https://www.cambridge.org/core/journals/international-journal-of-asian-studies/article/river-of-fire-and-ice-infrastructure-territoriality-and-the-colonization-of-eastern-hokkaido-japan-1600s1900s/7529A9AC3A37E5E2DBF449B87B1F2553 ; https://journals.sagepub.com/doi/10.1177/036319908601100401 ; https://www.ndl.go.jp/nichiran/e/data/R/042/042-001r.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-japanese-literature/publishing-and-the-book-in-the-seventeenth-and-eighteenth-centuries/B1992E389B63A18FE936E1039ABBC860 ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (7 HIGH / 12 MEDIUM / 0 LOW dans la matrice)

### JMB — Jambi

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### JOH — Johore

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `light_infantry_tactics` (SECTORAL), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `standardized_field_artillery` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/abs/british-traders-in-the-east-indies-17701820/political-allies-country-traders-and-the-malays-ii/D01FB8EF5722A08C3BA43B9E67F91D4C ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (1 HIGH / 10 MEDIUM / 0 LOW dans la matrice)

### KLO — Khmer Loeu

- **Current tier:** `tier_6`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `improved_husbandry`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `urbanization`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** aucun cas majeur retenu
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 2 MEDIUM / 0 LOW dans la matrice)

### KOR — Korea

- **Current tier:** `tier_5`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `international_relations`, `regulated_small_arms`, `scientific_fortification_siegecraft`, `systematic_population_registration`, `traditional_papermaking`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `shaft_mining`, `periodical_print_networks`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `shaft_mining` (SECTORAL), `urbanization` (ABSTRACT), `periodical_print_networks` (ABSTRACT), `regulated_small_arms` (SECTORAL)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `traditional_papermaking`: organized_forestry is missing unless separately recommended. Papermaking is historically established independently of the tree abstraction; do not auto-grant the parent solely to repair the chain.
- **Justification historique:** Les registres Joseon à l’échelle du royaume, l’impression d’État et la documentation militaire du XVIIIe siècle justifient des ajouts administratifs et militaires ciblés, sans copier le paquet européen de tier 4.
- **Sources:** https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002235256 ; https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002089812 ; https://academic.oup.com/book/45713/chapter-abstract/398152533
- **Confiance générale:** MEDIUM (4 HIGH / 8 MEDIUM / 0 LOW dans la matrice)

### KTI — Kutai

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### LAN — Lanfang

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `institutionalized_scientific_exchange`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `international_relations`, `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `light_infantry_tactics` (SECTORAL), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `standardized_field_artillery` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Problème chronologique fondamental : Lanfang est fondée en 1777. Le setup du 1er janvier 1776 ne peut donc pas être validé comme celui d’un État Lanfang déjà constitué; l’explicite `institutionalized_scientific_exchange` est retiré et le reste du tier doit être réexaminé en fonction de ce que le TAG représente avant 1777.
- **Sources:** https://www.cambridge.org/core/books/abs/chinese-indonesians/makam-juang-mandor-monument-remembering-and-distorting-the-history-of-the-chinese-of-west-kalimantan/1C7EF6F2A78826DF81EE6D9AAB8C9ABF ; https://www.cambridge.org/core/books/abs/british-traders-in-the-east-indies-17701820/political-allies-country-traders-and-the-malays-ii/D01FB8EF5722A08C3BA43B9E67F91D4C ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (1 HIGH / 8 MEDIUM / 3 LOW dans la matrice)

### LUA — Luang Prabang

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/abs/british-traders-in-the-east-indies-17701820/political-allies-country-traders-and-the-malays-ii/D01FB8EF5722A08C3BA43B9E67F91D4C ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### MGD — Maguindanao

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `light_infantry_tactics` (SECTORAL), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `standardized_field_artillery` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (1 HIGH / 10 MEDIUM / 0 LOW dans la matrice)

### MND — Mindanao

- **Current tier:** `tier_7`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** —
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** aucun cas majeur retenu
- **Justification historique:** Le tier 7 vide évite de projeter des institutions étatiques/industrielles inadéquates. Cela ne signifie pas absence de techniques locales : le modèle de technologie du jeu représente mal plusieurs savoir-faire autochtones; aucune ADD n’est proposée sans correspondance gameplay suffisamment défendable.
- **Sources:** —
- **Confiance générale:** MEDIUM (0 HIGH / 0 MEDIUM / 0 LOW dans la matrice)

### PHI — Philippines

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `colonization`, `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `shaft_mining`
- **Technologies frontière/sectorielles:** `colonization` (ABSTRACT), `codified_practical_knowledge` (ABSTRACT), `light_infantry_tactics` (SECTORAL), `shaft_mining` (SECTORAL), `urbanization` (ABSTRACT), `scientific_naval_architecture` (SECTORAL)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents.
- **Justification historique:** La colonie possède localement un système de fortifications, ports et chantiers navals (Cavite/Manila) documenté au XVIIIe siècle. Les ajouts navals sont donc locaux, tandis que les technologies espagnoles non implantées ne sont pas importées par défaut.
- **Sources:** https://revistadeindias.revistas.csic.es/index.php/revistadeindias/article/view/1058/0 ; https://journals.sagepub.com/doi/10.1177/0843871419860698 ; https://pares.mcu.es/ParesBusquedas20/catalogo/description/12761126
- **Confiance générale:** MEDIUM (8 HIGH / 8 MEDIUM / 0 LOW dans la matrice)

### PON — Pontianak

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### PRK — Perak

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** `regulated_small_arms`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Cas minier important : l’étain est ancien au Perak, mais les méthodes pré-boom du XIXe siècle sont décrites comme simples, manuelles et alluviales. `shaft_mining` est donc retirée malgré l’importance économique du minerai.
- **Sources:** https://academic.oup.com/book/57608/chapter-abstract/469227832 ; https://www.cambridge.org/core/books/abs/british-traders-in-the-east-indies-17701820/political-allies-country-traders-and-the-malays-ii/D01FB8EF5722A08C3BA43B9E67F91D4C ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (1 HIGH / 10 MEDIUM / 0 LOW dans la matrice)

### RYU — Ryukyu

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `organized_forestry`, `state_dockyard_systems`, `systematic_cadastral_surveying`
- **Technologies à REMOVE:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `urbanization` (ABSTRACT), `state_dockyard_systems` (SECTORAL)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Ryukyu est technologiquement spécifique : le survey foncier 1737–1750 et les règlements forestiers de 1737 sont des preuves exceptionnellement fortes pour `systematic_cadastral_surveying` et `organized_forestry`; le package militaire du tier 4 est en revanche excessif.
- **Sources:** https://www.journals.uchicago.edu/doi/10.1086/726185 ; https://shimuchi.lib.u-ryukyu.ac.jp/collection/shimabukuro/si00901
- **Confiance générale:** MEDIUM (4 HIGH / 10 MEDIUM / 0 LOW dans la matrice)

### SAK — Siak

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### SCT — Sip Song Chau Tai

- **Current tier:** `tier_6`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `improved_husbandry`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `urbanization`
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** aucun cas majeur retenu
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 2 MEDIUM / 0 LOW dans la matrice)

### SEL — Selangor

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/abs/british-traders-in-the-east-indies-17701820/political-allies-country-traders-and-the-malays-ii/D01FB8EF5722A08C3BA43B9E67F91D4C ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### SHS — Shan

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/abs/british-traders-in-the-east-indies-17701820/political-allies-country-traders-and-the-malays-ii/D01FB8EF5722A08C3BA43B9E67F91D4C ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### SIA — Siam

- **Current tier:** `tier_6`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `improved_husbandry`, `urbanization`
- **Technologies à ADD:** `international_relations`, `organized_textile_production`, `regulated_small_arms`, `scientific_fortification_siegecraft`, `systematic_administrative_statistics`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `selective_breeding`
- **Technologies frontière/sectorielles:** `selective_breeding` (ABSTRACT), `urbanization` (ABSTRACT), `regulated_small_arms` (SECTORAL)
- **Prérequis problématiques:** aucun cas majeur retenu
- **Justification historique:** Le tier 6 sous-estime le Thonburi de Taksin : État en reconstruction mais militairement actif, connecté au commerce chinois et disposant d’une administration réelle. Des ajouts ciblés sont préférables à un simple passage de tier.
- **Sources:** https://www.cambridge.org/core/journals/international-journal-of-asian-studies/article/all-political-power-comes-from-the-barrel-of-a-gun-arms-trading-gun-control-and-revolt-in-ayutthaya-16581709/018E8EAA0AAE07CBCF41E59EC02FA5EC ; https://www.cambridge.org/core/journals/journal-of-southeast-asian-studies/article/siamese-state-trade-and-the-chinese-gobetween-17671855/B160B1DA1CBBCFD51A89E539C93300D3 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (1 HIGH / 7 MEDIUM / 0 LOW dans la matrice)

### SKH — Evenki

- **Current tier:** `tier_7`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** —
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** aucun cas majeur retenu
- **Justification historique:** Le tier 7 vide évite de projeter des institutions étatiques/industrielles inadéquates. Cela ne signifie pas absence de techniques locales : le modèle de technologie du jeu représente mal plusieurs savoir-faire autochtones; aucune ADD n’est proposée sans correspondance gameplay suffisamment défendable.
- **Sources:** —
- **Confiance générale:** MEDIUM (0 HIGH / 0 MEDIUM / 0 LOW dans la matrice)

### SLW — Sulawesi

- **Current tier:** `tier_7`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** —
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** aucun cas majeur retenu
- **Justification historique:** Le tier 7 vide évite de projeter des institutions étatiques/industrielles inadéquates. Cela ne signifie pas absence de techniques locales : le modèle de technologie du jeu représente mal plusieurs savoir-faire autochtones; aucune ADD n’est proposée sans correspondance gameplay suffisamment défendable.
- **Sources:** —
- **Confiance générale:** MEDIUM (0 HIGH / 0 MEDIUM / 0 LOW dans la matrice)

### SMB — Sambas

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### SRK — Surakarta

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `light_infantry_tactics` (SECTORAL), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `standardized_field_artillery` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/civilization-on-loan-the-making-of-an-upstart-polity-mataram-and-its-successors-16001830/85009FD66852BA85AC132F193587B886 ; https://www.jstor.org/stable/jj.33506918.18 ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (2 HIGH / 9 MEDIUM / 0 LOW dans la matrice)

### STG — Sintang

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### SUL — Sulu

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `light_infantry_tactics` (SECTORAL), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `standardized_field_artillery` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/services/aop-cambridge-core/content/view/84EFF842726212C9A430E41FDC1B94CC/S0022463400009322a.pdf/slave_markets_and_exchange_in_the_malay_world_the_sulu_sultanate_17701878.pdf ; https://www.cambridge.org/core/books/pirates-of-empire/sulu-sea/F532960AFF94E3D63209FA2A970F0696 ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (1 HIGH / 10 MEDIUM / 0 LOW dans la matrice)

### TIB — Tibet

- **Current tier:** `tier_6`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `improved_husbandry`, `urbanization`
- **Technologies à ADD:** `codified_practical_knowledge`, `traditional_papermaking`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** `urbanization` (ABSTRACT), `codified_practical_knowledge` (SECTORAL), `traditional_papermaking` (SECTORAL)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `traditional_papermaking`: organized_forestry is missing unless separately recommended. Papermaking is historically established independently of the tree abstraction; do not auto-grant the parent solely to repair the chain.
- **Justification historique:** Cas frontière inclus pour éviter un angle mort est-asiatique. Les grands ateliers d’impression de Dergé en 1744–1745 justifient une capacité sectorielle de papeterie/savoir codifié; le reste du setup doit rester prudent.
- **Sources:** https://escholarship.org/uc/item/0bk7n662 ; https://academic.oup.com/book/45713/chapter-abstract/398152533
- **Confiance générale:** MEDIUM (0 HIGH / 4 MEDIUM / 0 LOW dans la matrice)

### TID — Tidore

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** `light_infantry_tactics`, `standardized_field_artillery`
- **Technologies à REVIEW:** `codified_practical_knowledge`, `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `systematic_administrative_statistics` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957 ; https://assets.cambridge.org/97805216/63700/excerpt/9780521663700_excerpt.pdf
- **Confiance générale:** MEDIUM (0 HIGH / 11 MEDIUM / 0 LOW dans la matrice)

### ULT — Ulta

- **Current tier:** `tier_7`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** —
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Technologies frontière/sectorielles:** —
- **Prérequis problématiques:** aucun cas majeur retenu
- **Justification historique:** Le tier 7 vide évite de projeter des institutions étatiques/industrielles inadéquates. Cela ne signifie pas absence de techniques locales : le modèle de technologie du jeu représente mal plusieurs savoir-faire autochtones; aucune ADD n’est proposée sans correspondance gameplay suffisamment défendable.
- **Sources:** —
- **Confiance générale:** MEDIUM (0 HIGH / 0 MEDIUM / 0 LOW dans la matrice)

### YOG — Yogyakarta

- **Current tier:** `tier_4`
- **Tier action:** `REVIEW_TIER`
- **Technologies à KEEP:** `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** —
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`
- **Technologies frontière/sectorielles:** `codified_practical_knowledge` (ABSTRACT), `light_infantry_tactics` (SECTORAL), `regulated_small_arms` (SECTORAL), `shaft_mining` (SECTORAL), `standardized_field_artillery` (SECTORAL), `urbanization` (ABSTRACT)
- **Prérequis problématiques:** `codified_practical_knowledge`: Missing/partial parent chain may include institutionalized_scientific_exchange and periodical_print_networks. Treat as tree abstraction where local knowledge transmission followed different institutions; do not auto-grant parents. ; `regulated_small_arms`: Missing parent(s): scientific_fortification_siegecraft. Do not add automatically; resolve by historical justification or tree abstraction.
- **Justification historique:** Le diagnostic repose surtout sur l’écart entre capacités locales attestées (agriculture, textile, commerce, armes à feu, structures de cour) et la portée très large de certains nœuds du tier générique. Les décisions REVIEW signalent les cas où l’évidence régionale ne suffit pas à prouver une institution à l’échelle du TAG.
- **Sources:** https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/civilization-on-loan-the-making-of-an-upstart-polity-mataram-and-its-successors-16001830/85009FD66852BA85AC132F193587B886 ; https://www.jstor.org/stable/jj.33506918.18 ; https://www.cambridge.org/core/books/asian-military-revolution/southeast-asia/223876F2B9DF02FF675FD99275E04957
- **Confiance générale:** MEDIUM (2 HIGH / 9 MEDIUM / 0 LOW dans la matrice)

## 5. Comparaison régionale

1. **Qing vs Japon vs Joseon** : les trois espaces ont des capacités d’écriture/impression et d’administration fortes, mais sous des institutions différentes. Qing excelle par échelle bureaucratique, hydraulique, mines et réseaux impériaux; Tokugawa par urbanisation, édition commerciale, registres et rangaku; Joseon par bureaucratie, registres et impression étatique. Aucun de ces profils ne se résume à un « tier civilisationnel ».
2. **Mainland Southeast Asia** : Burma, Đại Việt et Siam ont des appareils d’État et des traditions militaires plus fortes que ne le suggèrent certains tiers génériques. À l’inverse, la présence de firearms n’implique pas automatiquement une standardisation européenne de l’artillerie.
3. **Maritime Southeast Asia** : commerce, ports, navigation et artillerie côtière sont souvent plus pertinents que mines souterraines ou administration statistique de type centralisé. Les sultanats doivent rester différenciés.
4. **Colonies** : DEI/PHI reçoivent seulement les capacités effectivement implantées localement (fortifications, chantiers, administration, garnisons), pas le paquet technologique intégral de la métropole.
5. **Frontières/autochtones** : Ainu, Evenki, Ulta, Degar, Khmer Loeu, etc. possèdent des techniques réelles que l’arbre Victoria 3 représente mal. L’absence d’ADD n’est pas un jugement de « retard », mais une prudence sur la correspondance entre savoir local et nœud gameplay.

## 6. Technologies frontière 1776

- `atmospheric_engine` : aucune ADD régionale. Une machine de Newcomen n’est pas déduite d’une mine profonde ou d’un contact européen.
- `precision_boring` : aucune ADD régionale. Les capacités métallurgiques asiatiques ne suffisent pas à prouver l’usage du procédé de boring de précision correspondant au nœud.
- `coke_smelting` : **CHI = REVIEW**, pas ADD. L’usage ancien du charbon/anthracite dans la métallurgie chinoise est réel, mais le nœud du mod représente la transition spécifique vers le coke-smelting industriel et ouvre steel mill/tooling workshop.
- `mechanized_spinning` / `mechanized_weaving` : aucune ADD. La Chine, le Japon, Java et d’autres régions ont des textiles proto-industriels très développés, mais ils restent majoritairement artisanaux/household; sophistication textile ≠ mécanisation britannique.
- `improved_agricultural_implements` : aucune ADD faute d’un lien suffisamment précis entre les outils locaux et le PM `pm_tools` du nœud.
- `systematic_population_registration` : ADD pour CHI, JAP, KOR; ces trois cas ont des systèmes d’enregistrement documentés avant 1776.
- `systematic_cadastral_surveying` : KEEP JAP, ADD RYU, REVIEW CHI. C’est un bon exemple d’asymétrie institutionnelle régionale.

## 7. Anachronismes

### DEI — `joint_stock_companies` — REMOVE (HIGH)
La VOC elle-même est un jalon majeur de l’histoire de la corporation moderne : capital permanent, actions transférables, séparation propriété/gestion et autres traits sont établis très tôt. Mais le nœud Victoria 3 n’est pas « existence d’une compagnie par actions ». Son arbre exige `commercial_insurance_markets` + `postal_savings`, et son gameplay ouvre notamment `law_laissez_faire` et des capacités générales de compagnies. `postal_savings` est un nœud postérieur à 1776. La présence de la VOC ne suffit donc pas à conserver `joint_stock_companies` dans DEI.

### LAN — problème de date du TAG
Lanfang est fondée en **1777**. Ce n’est pas seulement une technologie anachronique : le sujet est l’existence même du polity au 1er janvier 1776. `institutionalized_scientific_exchange` est REMOVE; le tier hérité est REVIEW_TIER jusqu’à décision sur la représentation pré-1777 du TAG.

Aucune autre technologie C/D actuellement distribuée dans ce périmètre n’a été identifiée par l’audit source : `joint_stock_companies` est le seul cas C/D régional actuel.

## 8. Prérequis

- `joint_stock_companies` DEI : parents `commercial_insurance_markets` et `postal_savings` absents. **Ne pas les ajouter** : `postal_savings` renforce au contraire la conclusion REMOVE.
- `codified_practical_knowledge` : de nombreux pays le possèdent sans `institutionalized_scientific_exchange` et/ou `periodical_print_networks`. Dans plusieurs sociétés asiatiques, le savoir pratique codifié existe via bureaucraties, manuscrits, xylographie, écoles de cour ou traditions savantes différentes. Le manque de parent peut être une abstraction de l’arbre plutôt qu’un motif pour distribuer automatiquement une presse périodique.
- `traditional_papermaking` : le parent `organized_forestry` ne doit pas être ajouté automatiquement. La production de papier peut être historiquement démontrée sans qu’un régime forestier organisé au sens du nœud soit prouvé.
- `regulated_small_arms` : lorsque recommandé en ADD (CHI/KOR/BUR/SIA/DAI), le parent `scientific_fortification_siegecraft` est également évalué explicitement quand les preuves le justifient; aucune réparation automatique de chaîne n’est faite.

## 9. Incertitudes

- L’interprétation exacte de `periodical_print_networks` : la Chine, le Japon et la Corée possèdent des cultures imprimées très avancées, mais le nœud « Periodical Press » ne doit pas devenir un simple alias de « sait imprimer ».
- La portée de `regulated_small_arms`, `light_infantry_tactics` et `standardized_field_artillery` en Asie du Sud-Est : les armes à feu sont anciennes et importantes, mais leur institutionnalisation varie fortement par État.
- Les petits sultanats/chefferies du tier 4 manquent souvent de sources techniques suffisamment fines pour trancher toutes les capacités génériques; REVIEW est préférable à une suppression arbitraire.
- `coke_smelting` en Chine : différence entre usage de charbon/anthracite dans des procédés chinois et nœud industriel spécifique de coke-smelting.
- `state_dockyard_systems`/`scientific_naval_architecture` : construction navale et flotte ne signifient pas automatiquement appareil naval scientifique; statut sectoriel fréquent.
- `TIB` est un cas frontière géographique ajouté à cette recherche; lors de la fusion mondiale, vérifier qu’il n’est pas doublonné avec la région Himalaya/Asie du Sud.

## 10. Recommandations pour l’implémentation

**Pas de code dans ce document.**

- **Tier pouvant rester avec ajouts explicites éventuels :** `AIN`, `BAL`, `BUR`, `CAM`, `CHI`, `DAI`, `KOR`, `MND`, `SKH`, `SLW`, `TIB`, `ULT`.
- **Setup explicite recommandé :** `DEI`, `DGR`, `EZO`, `JAP`, `KLO`, `PHI`, `PRK`, `RYU`, `SCT`, `SIA`.
- **Tier à réexaminer avant implémentation :** `ACE`, `BLG`, `BNJ`, `BRU`, `BTN`, `CHP`, `CMI`, `JMB`, `JOH`, `KTI`, `LAN`, `LUA`, `MGD`, `PON`, `SAK`, `SEL`, `SHS`, `SMB`, `SRK`, `STG`, `SUL`, `TID`, `YOG`.
- **Aucun `CHANGE_TIER` numérique recommandé** dans cette recherche régionale : les corrections nécessaires sont asymétriques et un changement de tier écraserait trop de différences sectorielles.

### Contrôle final

- TAG étudiés : **45**
- Décisions KEEP : **217**
- Décisions ADD : **38**
- Décisions REMOVE : **47**
- Décisions REVIEW : **123**
- Pays avec `CHANGE_TIER` : **0**
- Pays avec `REPLACE_WITH_EXPLICIT_SETUP` : **10**
- Pays avec `REVIEW_TIER` : **23**
- Relations pays-technologie documentées dans la matrice : **425**

Les **377 relations technologiques actuellement présentes** dans ces 45 TAG ont toutes reçu une décision. Les technologies explicites actuelles ont toutes été examinées; le seul grant C/D régional actuel, `joint_stock_companies` à DEI, est traité explicitement. Tous les IDs ajoutés à la matrice existent dans `TECH_START_1776_TECHNOLOGIES.csv`.
