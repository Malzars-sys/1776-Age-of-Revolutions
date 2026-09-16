# Recherche technologique — Afrique — 1er janvier 1776

> **Statut : recherche uniquement.** Ce document ne modifie aucun fichier du mod et ne propose aucun code Victoria 3. La date de coupure est strictement le **1er janvier 1776**.

## 1. Périmètre

**161 TAG africains** du CSV pays sont traités. L’Égypte (`EGY`) est explicitement exclue. Le CSV classe plusieurs TAG africains dans `Nile Basin`; Darfour, Dar Fertit, Dinka, Nuer, The Sudan et Toposa sont inclus car leur centre géographique est africain.

### Afrique du Nord/Maghreb (18)
`AHG` — Kel Ahaggar, `AIT` — Ait Abbas, `AJJ` — Kel Ajjer, `CMB` — Chaamba, `CON` — Constantine, `DLM` — Delim, `FZN` — Fezzan, `MAS` — Mascara, `MOR` — Morocco, `MZB` — Mzab, `RGB` — Reguibat, `SAH` — Sahrawi, `TEK` — Tekna, `TRI` — Tripolitania, `TUA` — Tuat, `TUG` — Touggourt, `TUN` — Tunis, `ZWY` — Zuwayya

### Afrique de l’Ouest (40)
`ADG` — Kel Adagh, `ADR` — Adrar, `AIR` — Kel Air, `ASH` — Ashanti, `ATR` — Kel Ataram, `AYI` — Anyi, `BEN` — Benin, `BLE` — Baule, `BND` — Bundu, `BOR` — Bornu, `BRG` — Borgu, `BRK` — Brakna, `CAY` — Cayor, `DAH` — Dahomey, `DIN` — Kel Dinnik, `DIO` — Diola, `EWE` — Ewe, `FTJ` — Futa Jallon, `FTR` — Futa Toro, `HAU` — Gobir, `IBO` — Igbo, `JLF` — Jolof, `KBD` — Kabadougou, `KBU` — Kaabu, `KNG` — Kong, `KRT` — Kaarta, `KRU` — Kru, `LIB` — Liberia, `MDK` — Mandinka, `MOS` — Mossi, `MSN` — Massina, `OUA` — Tagant, `OYO` — Oyo, `SGU` — Segou, `SIL` — Sierra Leone, `SOK` — Sokoto, `SRR` — Serer, `SSU` — Susu, `TMN` — Temne, `TRZ` — Trarza

### Afrique centrale/équatoriale (23)
`BGI` — Bagirmi, `BMM` — Bamum, `BNG` — Bangala, `BOB` — Bobangi, `CHK` — Chokwe, `DAK` — Dar al Kuti, `DLA` — Duala, `FNG` — Fang, `HMB` — Hemba, `KBA` — Kuba, `KON` — Kongo, `KSN` — Kasanje, `LBA` — Luba, `LGA` — Lega, `LND` — Lunda, `LNG` — Loango, `MNB` — Mangbetu, `OVM` — Ovimbundu, `TBI` — Tubu, `TKE` — Teke, `WAD` — Wadai, `YKA` — Yaka, `ZND` — Azande

### Afrique orientale et Corne (58)
`ACH` — Acholi, `AGC` — Angoche, `AJR` — Ajuran, `ANK` — Ankole, `ANU` — Anuak, `ARS` — Arsiland, `AUL` — Aulihan, `AWS` — Aussa, `BGM` — Begemder, `BMB` — Bemba, `BNY` — Bunyoro, `BRD` — Burundi, `BRN` — Borana, `BUG` — Buganda, `ETH` — Ethiopia, `GGO` — Gogo, `GJM` — Gojjam, `GLD` — Geledi, `GZA` — Gaza, `HAR` — Harar, `HDY` — Hadiya, `HHE` — Hehe, `ISQ` — Isaaq, `KFA` — Kaffa, `KKY` — Kikuyu, `KRG` — Karagwe, `KZM` — Kazembe, `LUO` — Luo, `LZO` — Barotse, `MAD` — Madagascar, `MBS` — Mombasa, `MJK` — Mijikenda, `MJT` — Majerteen, `MNC` — Manica, `MRV` — Maravi, `MSH` — Mashona, `MSI` — Masai, `MSK` — Maseko, `MTB` — Ndebele, `MTP` — Mutapa, `NYM` — Unyamwezi, `OGD` — Ogaden, `OMO` — Omo, `ORM` — Orma, `QWR` — Qwara, `RWD` — Rwanda, `SDM` — Sidamo, `SHW` — Shewa, `SKM` — Usukuma, `SKY` — Sakuye, `SNG` — Sangu, `TGI` — Tungi, `TGR` — Tigray, `TRK` — Turkana, `WLG` — Welega, `WLT` — Wolaita, `WSG` — Warsangali, `WTU` — Witu

### Afrique australe (16)
`BST` — Basutoland, `HRO` — Herero, `NAM` — Nama, `ORA` — Oranje, `OVB` — Ovambo, `PDI` — Pedi, `PHL` — Philippolis, `SAF` — South Africa, `SAN` — San, `SWZ` — Swaziland, `TRN` — Transvaal, `TSW` — Tswana, `VND` — Venda, `WBL` — Griqualand, `XHO` — Xhosa, `ZUL` — Zulu

### Bassin du Nil (hors Égypte) (6)
`DFR` — Darfur, `DFT` — Dar Fertit, `DNK` — Dinka, `NUE` — Nuer, `SD1` — The Sudan, `TPS` — Toposa

### Problèmes d’identité temporelle
Plusieurs TAG portent le nom d’États/colonies postérieurs à 1776. Ils ne sont **pas** exclus : leurs technologies sont réévaluées à partir des sociétés présentes sur le territoire en 1776. Les cas les plus importants sont `LIB`, `SIL`, `SOK`, `MSN`, `BST`, `GZA`, `MTB`, `ZUL`, `ORA`, `TRN`, `PHL`, `WBL`, `SWZ` et `SD1`. Cela évite à la fois de projeter les institutions du XIXe siècle et d’effacer les capacités matérielles locales antérieures.

## 2. Méthode et sources

La matrice des pays et la matrice des technologies jointes sont utilisées comme autorité pour les TAG, tiers, IDs, catégories, prérequis et attributions actuelles. Les décisions distinguent capacité locale, importation, usage sectoriel et institution nationale. Un mousquet importé ne vaut pas `regulated_small_arms`; une métallurgie du fer ne vaut pas `coke_smelting`; navigation côtière/dhow ne vaut pas automatiquement `state_dockyard_systems`; tribut/fiscalité ne vaut pas automatiquement statistique d’État moderne.

Principales références utilisées (sélection) :
- Cambridge — histoire de l’Algérie ottomane: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5
- Cambridge — Tunis XVIIIe siècle: https://www.cambridge.org/core/journals/annales-histoire-sciences-sociales/article/abs/esclaves-chretiens-et-esclaves-noirs-a-tunis-au-xviiie-siecle/B6D63DDA1CDEE63BFF2CE876BB6F3657
- Met — âge du fer en Afrique de l’Ouest: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa
- Cambridge — importation d’armes à feu en Afrique de l’Ouest: https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Cambridge — financement de l’expansion ashanti: https://www.cambridge.org/core/journals/africa/article/abs/financing-of-the-ashanti-expansion-17001820/D6DBF0405E655EE438E72591646E2D14
- Met — Afrique centrale 1600-1800: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html
- Met — Luba/Lunda: https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Met — Afrique orientale 1600-1800: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html
- Cambridge — commerce est-africain: https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Cambridge — textile éthiopien XVIIIe: https://www.cambridge.org/core/books/abs/inbetween-textiles-14001800/globalisation-and-the-manufacture-of-tabletwoven-sanctuary-curtains-in-ethiopia-in-the-eighteenth-century/4E9B2B7EFC904C677A18D7AB588E1CFD
- Cambridge — mousquets à Madagascar XVIIIe: https://www.cambridge.org/core/journals/comparative-studies-in-society-and-history/article/abs/sacred-musket-tactics-technology-and-power-in-eighteenthcentury-madagascar/23C7FD2B3DB787855C4AAED2822FD057
- Cambridge — économie de Madagascar 1750-1895: https://assets.cambridge.org/052183/9351/excerpt/0521839351_excerpt.htm
- Cambridge — Haut-Nil: https://www.cambridge.org/core/books/abs/medieval-africa-12501800/upper-nile-basin-and-the-east-african-plateau/AC690A3863339F46EA0D4F76FB47AE44
- SA History Online — agriculteurs africains d’Afrique australe: https://sahistory.org.za/archive/african-farmers-southern-africa
- Cambridge — économie du Cap XVIIIe: https://www.cambridge.org/core/journals/international-review-of-social-history/article/economics-of-slavery-in-the-eighteenthcentury-cape-colony-revising-the-nieboerdomar-hypothesis/B7EB0A6EC343E570F6D339D8BB1EAC2F
- SAHO — Simon’s Town: https://sahistory.org.za/place/simons-town-cape-peninsula

## 3. Diagnostic régional

### 3.1 Principe général
L’Afrique de 1776 n’est ni technologiquement homogène ni correctement représentable par un unique “tier”. On trouve simultanément : métallurgie du fer ancienne et très spécialisée; grands systèmes agropastoraux; manufactures textiles/raffia/coton; commerce transsaharien, atlantique et indo-océanique; fiscalité et tribut de royaumes centralisés; ports fortifiés et arsenaux maghrébins; et, ailleurs, des sociétés mobiles où un nœud comme `urbanization` est surtout une convention de compatibilité. À l’inverse, vapeur, coke, alésage de précision, bourses et académies techniques ne doivent pas migrer vers une colonie simplement parce qu’une métropole européenne les connaît.

### 3.2 Métallurgie et mines
La métallurgie du fer ouest-africaine et australe est solidement attestée, mais l’arbre ne possède pas un bon nœud “sidérurgie traditionnelle africaine”. `coke_smelting` est donc **explicitement rejeté** comme substitut. `shaft_mining` est souvent mis en REVIEW : il peut représenter certaines extractions à puits, mais son paquet gameplay (charbon, cuivre, fer, plomb, sel, soufre) est trop large pour être accordé sur la seule preuve d’orfèvrerie, d’orpaillage ou de forge.

### 3.3 Armes à feu
L’Afrique de l’Ouest reçoit des volumes très importants d’armes importées au XVIIIe siècle, tandis que la fabrication locale d’armes complètes reste limitée; la poudre et les réparations sont plus largement locales. Par conséquent `regulated_small_arms` n’est **pas** ajouté automatiquement à Ashanti, Benin, Dahomey ou Oyo. Le Maghreb constitue un cas différent : arsenaux d’État, garnisons, course et artillerie permettent des KEEP/ADD sectoriels. Madagascar est placé en REVIEW strictement pour le 1er janvier 1776 : les sources des années 1760-1770 montrent mousquets et poudre, mais la chronologie de la fabrication complète d’armes reste délicate.

### 3.4 Administration et commerce
Les États ashanti, dahoméen, oyo, beninois, bornouan, darfurien, éthiopien, maghrébins, etc. ne sont pas traités comme “sans administration”. En revanche `systematic_administrative_statistics` est un nœud gameplay très large : taxation/tribut justifient parfois KEEP sectoriel, mais pas une statistique nationale moderne. `international_relations` est ajouté à plusieurs États majeurs sous-dotés lorsque diplomatie et commerce longue distance sont structurels.

### 3.5 Colonies et comptoirs
Le Cap est le test le plus clair du principe “colonie ≠ métropole”. Le dockyard VOC de Simon’s Town (1743) peut justifier `state_dockyard_systems` sectoriellement, tandis que `atmospheric_engine`, `precision_boring`, `coke_smelting`, `stock_exchange`, `periodical_print_networks` et plusieurs institutions financières sont retirés. La même logique vaut pour Sierra Leone/Liberia : leurs setups coloniaux/étatiques ultérieurs ne sont pas projetés en 1776.

## 4. Analyse pays par pays

## Afrique du Nord/Maghreb
### AHG — Kel Ahaggar
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### AIT — Ait Abbas
- Current tier: `tier_4`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### AJJ — Kel Ajjer
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### CMB — Chaamba
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### CON — Constantine
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### DLM — Delim
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### FZN — Fezzan
- Current tier: `tier_4`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/la-traite-des-esclaves-noirs-en-libye-au-xviiie-siecle/7245C0AEDD8C0103C7AF3AC0CE314C0F ; https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5
- Confiance générale: **MEDIUM**

### MAS — Mascara
- Current tier: `tier_4`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### MOR — Morocco
- Current tier: `tier_4`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `distillation`, `improved_husbandry`, `international_relations`, `light_infantry_tactics`, `organized_textile_production`, `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`, `urbanization`
- Technologies à ADD: `scientific_fortification_siegecraft`, `state_dockyard_systems`
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`
- Technologies frontière/sectorielles: `light_infantry_tactics`, `regulated_small_arms`, `standardized_field_artillery`, `systematic_administrative_statistics`, `scientific_fortification_siegecraft`, `state_dockyard_systems`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul. Arsenaux, ports fortifiés, corsaires et commerce méditerranéen justifient des capacités militaires/navales sectorielles plus élevées que leur tier générique dans certains domaines.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### MZB — Mzab
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### RGB — Reguibat
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### SAH — Sahrawi
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### TEK — Tekna
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### TRI — Tripolitania
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- Technologies à ADD: `international_relations`, `regulated_small_arms`, `scientific_fortification_siegecraft`, `state_dockyard_systems`
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `standardized_field_artillery`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`, `regulated_small_arms`, `scientific_fortification_siegecraft`, `standardized_field_artillery`, `state_dockyard_systems`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul. Arsenaux, ports fortifiés, corsaires et commerce méditerranéen justifient des capacités militaires/navales sectorielles plus élevées que leur tier générique dans certains domaines.
- Sources: https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87 ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/la-traite-des-esclaves-noirs-en-libye-au-xviiie-siecle/7245C0AEDD8C0103C7AF3AC0CE314C0F
- Confiance générale: **LOW**

### TUA — Tuat
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### TUG — Touggourt
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

### TUN — Tunis
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: `codified_practical_knowledge`, `international_relations`, `organized_textile_production`, `regulated_small_arms`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `systematic_administrative_statistics`
- Technologies à REMOVE: —
- Technologies à REVIEW: `standardized_field_artillery`
- Technologies frontière/sectorielles: `regulated_small_arms`, `scientific_fortification_siegecraft`, `standardized_field_artillery`, `state_dockyard_systems`, `systematic_administrative_statistics`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul. Arsenaux, ports fortifiés, corsaires et commerce méditerranéen justifient des capacités militaires/navales sectorielles plus élevées que leur tier générique dans certains domaines.
- Sources: https://www.cambridge.org/core/journals/annales-histoire-sciences-sociales/article/abs/esclaves-chretiens-et-esclaves-noirs-a-tunis-au-xviiie-siecle/B6D63DDA1CDEE63BFF2CE876BB6F3657 ; https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5
- Confiance générale: **LOW**

### ZWY — Zuwayya
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Évaluer ports, fiscalité, artisanat, commerce méditerranéen et structures ottomanes/locales sans importer automatiquement les capacités d’Istanbul.
- Sources: https://www.cambridge.org/core/books/history-of-algeria/ecologies-societies-cultures-and-the-state-15161830/6C59DEAD9F70913EC060EDD1465FA6A5 ; https://www.cambridge.org/core/books/abs/cambridge-history-of-islam/north-africa-in-the-sixteenth-and-seventeenth-centuries/4B2F63A65160CF588F520BEE5F57AC87
- Confiance générale: **MEDIUM**

## Afrique de l’Ouest
### ADG — Kel Adagh
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### ADR — Adrar
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### AIR — Kel Air
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### ASH — Ashanti
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `international_relations`, `urbanization`
- Technologies à ADD: `codified_practical_knowledge`, `organized_textile_production`, `systematic_administrative_statistics`
- Technologies à REMOVE: —
- Technologies à REVIEW: `regulated_small_arms`, `shaft_mining`
- Technologies frontière/sectorielles: `regulated_small_arms`, `shaft_mining`, `systematic_administrative_statistics`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée. Ashanti dispose d’un appareil fiscal/tributaire et finance son expansion via or, commerce et taxes; les armes sont surtout importées, avec réparation/poudre plus largement locales.
- Sources: https://www.cambridge.org/core/journals/africa/article/abs/financing-of-the-ashanti-expansion-17001820/D6DBF0405E655EE438E72591646E2D14 ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/ashanti-question-and-the-british-eighteenthcentury-origins/31ECA3E746C70147090FCA23AF454AC4
- Confiance générale: **MEDIUM**

### ATR — Kel Ataram
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### AYI — Anyi
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### BEN — Benin
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `regulated_small_arms`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`, `regulated_small_arms`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### BLE — Baule
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### BND — Bundu
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### BOR — Bornu
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- Technologies à ADD: `international_relations`
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### BRG — Borgu
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### BRK — Brakna
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### CAY — Cayor
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### DAH — Dahomey
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `regulated_small_arms`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`, `regulated_small_arms`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/continuity-revolution-or-evolution-on-the-slave-coast-of-west-africa-royal-architecture-and-political-order-in-precolonial-dahomey/9161CAD3798C67BD6D61BB0AEBB3CB44 ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/royal-monopoly-and-private-enterprise-in-the-atlantic-trade-the-case-of-dahomey1/885FB97D2FA6B22C2C762862DD6DB609
- Confiance générale: **MEDIUM**

### DIN — Kel Dinnik
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### DIO — Diola
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### EWE — Ewe
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### FTJ — Futa Jallon
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### FTR — Futa Toro
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### HAU — Gobir
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### IBO — Igbo
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### JLF — Jolof
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### KBD — Kabadougou
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### KBU — Kaabu
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### KNG — Kong
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### KRT — Kaarta
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### KRU — Kru
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### LIB — Liberia
- Current tier: `tier_3`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: `applied_mineralogy`, `coke_smelting`, `commercial_insurance_markets`, `light_infantry_tactics`, `medical_degrees`, `regulated_small_arms`, `shaft_mining`, `specialized_technical_academies`, `standardized_field_artillery`, `systematic_administrative_statistics`
- Technologies à REVIEW: `codified_practical_knowledge`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): shaft_mining. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Liberia/Monrovia settlement postdates 1776 (ACS settlement 1822). La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.loc.gov/collections/maps-of-liberia-1830-to-1870/articles-and-essays/history-of-liberia/ ; https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa
- Confiance générale: **MEDIUM**

### MDK — Mandinka
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### MOS — Mossi
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### MSN — Massina
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Massina Empire is a nineteenth-century formation; use local Fulani/Bambara predecessor capacities. La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.cambridge.org/core/journals/history-in-africa/article/centurys-firstborn-intimate-history-in-the-aftermath-of-nineteenthcentury-islamic-revolutions-in-central-mali/72F457F849651FDB98353DD6DD54465A ; https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa
- Confiance générale: **MEDIUM**

### OUA — Tagant
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### OYO — Oyo
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `regulated_small_arms`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`, `regulated_small_arms`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### SGU — Segou
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### SIL — Sierra Leone
- Current tier: `tier_4`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `distillation`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- Technologies à REVIEW: `codified_practical_knowledge`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: British Sierra Leone settlement begins in 1787; the TAG must represent local 1776 societies instead. La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://findingaids.loc.gov/repositories/7/resources/635 ; https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa
- Confiance générale: **MEDIUM**

### SOK — Sokoto
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Sokoto Caliphate is a nineteenth-century formation (jihad begins 1804); use Hausa/Fulani predecessor capacities. La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/ninetenthchntury-arabic-archives-of-west-africa/3404D2151FC22A845E1670EAC277E72C ; https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa
- Confiance générale: **MEDIUM**

### SRR — Serer
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### SSU — Susu
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### TMN — Temne
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

### TRZ — Trarza
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: La métallurgie du fer et les réseaux commerciaux sont anciens; l’usage massif d’armes importées ne vaut pas production locale réglementée.
- Sources: https://www.metmuseum.org/fr/essays/the-age-of-iron-in-west-africa ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/import-of-firearms-into-west-africa-in-the-eighteenth-century/84E8BF080DACF066CC957D56271DC721
- Confiance générale: **MEDIUM**

## Afrique centrale/équatoriale
### BGI — Bagirmi
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `international_relations`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### BMM — Bamum
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### BNG — Bangala
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### BOB — Bobangi
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### CHK — Chokwe
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### DAK — Dar al Kuti
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### DLA — Duala
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### FNG — Fang
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### HMB — Hemba
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### KBA — Kuba
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: `codified_practical_knowledge`, `international_relations`, `organized_textile_production`
- Technologies à REMOVE: —
- Technologies à REVIEW: `systematic_administrative_statistics`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://www.metmuseum.org/pt/essays/kingdoms-of-the-savanna-the-kuba-kingdom ; https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html
- Confiance générale: **MEDIUM**

### KON — Kongo
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: `international_relations`
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://www.metmuseum.org/exhibitions/listings/2015/kongo/blog/posts/kongo-textiles-renaissance-european-collections ; https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html
- Confiance générale: **MEDIUM**

### KSN — Kasanje
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`, `organized_textile_production`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### LBA — Luba
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`, `international_relations`, `organized_textile_production`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires ; https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html
- Confiance générale: **MEDIUM**

### LGA — Lega
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### LND — Lunda
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`, `international_relations`, `organized_textile_production`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires ; https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html
- Confiance générale: **MEDIUM**

### LNG — Loango
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: `codified_practical_knowledge`, `international_relations`, `organized_textile_production`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://www.metmuseum.org/exhibitions/listings/2015/kongo/blog/posts/kongo-textiles-renaissance-european-collections ; https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html
- Confiance générale: **MEDIUM**

### MNB — Mangbetu
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### OVM — Ovimbundu
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`, `organized_textile_production`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### TBI — Tubu
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### TKE — Teke
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### WAD — Wadai
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### YKA — Yaka
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

### ZND — Azande
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Les royaumes et réseaux du Congo/savanes combinent artisanat, textile/raffia, métallurgie et commerce; leur faiblesse en technologies industrielles européennes n’implique pas absence de capacités productives.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html ; https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires
- Confiance générale: **MEDIUM**

## Afrique orientale et Corne
### ACH — Acholi
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### AGC — Angoche
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`, `state_dockyard_systems`
- Technologies frontière/sectorielles: `state_dockyard_systems`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **LOW**

### AJR — Ajuran
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### ANK — Ankole
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### ANU — Anuak
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### ARS — Arsiland
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### AUL — Aulihan
- Current tier: `tier_6`
- Tier action: **REVIEW_TIER**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### AWS — Aussa
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### BGM — Begemder
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### BMB — Bemba
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### BNY — Bunyoro
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: `codified_practical_knowledge`, `international_relations`
- Technologies à REMOVE: —
- Technologies à REVIEW: `systematic_administrative_statistics`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### BRD — Burundi
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### BRN — Borana
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### BUG — Buganda
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: `codified_practical_knowledge`, `international_relations`
- Technologies à REMOVE: —
- Technologies à REVIEW: `systematic_administrative_statistics`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### ETH — Ethiopia
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `regulated_small_arms`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`, `regulated_small_arms`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État. Éthiopie: fort artisanat textile et institutions de cour; les armes à feu sont connues mais ne dominent pas encore le système militaire, donc pas d’industrie d’armes automatique.
- Sources: https://www.cambridge.org/core/books/abs/inbetween-textiles-14001800/globalisation-and-the-manufacture-of-tabletwoven-sanctuary-curtains-in-ethiopia-in-the-eighteenth-century/4E9B2B7EFC904C677A18D7AB588E1CFD ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/firearms-and-princely-power-in-ethiopia-in-the-nineteenth-century/6C5A764537B57A382CD9AEFC6EC4BF55
- Confiance générale: **MEDIUM**

### GGO — Gogo
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### GJM — Gojjam
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### GLD — Geledi
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### GZA — Gaza
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: `international_relations`
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Gaza kingdom is founded by Soshangane after c.1820; use local southeastern African societies. Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://www.cambridge.org/core/books/abs/five-hundred-years-rediscovered/rediscovering-the-ndwandwe-kingdom/BA03843A183BCC5D93A486506AB3C710 ; https://sahistory.org.za/archive/african-farmers-southern-africa
- Confiance générale: **MEDIUM**

### HAR — Harar
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: `international_relations`
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### HDY — Hadiya
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### HHE — Hehe
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### ISQ — Isaaq
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### KFA — Kaffa
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### KKY — Kikuyu
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### KRG — Karagwe
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### KZM — Kazembe
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://www.metmuseum.org/de/essays/kingdoms-of-the-savanna-the-luba-and-lunda-empires ; https://82nd-and-fifth.metmuseum.org/toah/ht/09/afc.html
- Confiance générale: **MEDIUM**

### LUO — Luo
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### LZO — Barotse
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### MAD — Madagascar
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `international_relations`, `urbanization`
- Technologies à ADD: `codified_practical_knowledge`, `organized_textile_production`
- Technologies à REMOVE: —
- Technologies à REVIEW: `improved_agricultural_implements`, `regulated_small_arms`
- Technologies frontière/sectorielles: `improved_agricultural_implements`, `regulated_small_arms`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État. Madagascar combine riziculture, artisanat du fer/textile, marchés et mousquets dans les années 1760-1770; l’unification merina postérieure ne doit pas être projetée en janvier 1776.
- Sources: https://www.cambridge.org/core/journals/comparative-studies-in-society-and-history/article/abs/sacred-musket-tactics-technology-and-power-in-eighteenthcentury-madagascar/23C7FD2B3DB787855C4AAED2822FD057 ; https://assets.cambridge.org/052183/9351/excerpt/0521839351_excerpt.htm
- Confiance générale: **LOW**

### MBS — Mombasa
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: `scientific_fortification_siegecraft`
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`, `state_dockyard_systems`
- Technologies frontière/sectorielles: `scientific_fortification_siegecraft`, `state_dockyard_systems`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **LOW**

### MJK — Mijikenda
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### MJT — Majerteen
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`, `state_dockyard_systems`
- Technologies frontière/sectorielles: `state_dockyard_systems`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **LOW**

### MNC — Manica
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### MRV — Maravi
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### MSH — Mashona
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### MSI — Masai
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### MSK — Maseko
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### MTB — Ndebele
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Ndebele state represented by this TAG is a nineteenth-century formation; use predecessor Nguni/Sotho-Tswana capacities. Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### MTP — Mutapa
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### NYM — Unyamwezi
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### OGD — Ogaden
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### OMO — Omo
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### ORM — Orma
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### QWR — Qwara
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### RWD — Rwanda
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: `codified_practical_knowledge`, `international_relations`
- Technologies à REMOVE: —
- Technologies à REVIEW: `systematic_administrative_statistics`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### SDM — Sidamo
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### SHW — Shewa
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### SKM — Usukuma
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### SKY — Sakuye
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### SNG — Sangu
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### TGI — Tungi
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### TGR — Tigray
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### TRK — Turkana
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### WLG — Welega
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### WLT — Wolaita
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### WSG — Warsangali
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

### WTU — Witu
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `international_relations`, `organized_textile_production`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`, `systematic_administrative_statistics`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer hauts plateaux, États des Grands Lacs et ports de l’océan Indien; la navigation/commerce n’équivaut pas automatiquement à un arsenal d’État.
- Sources: https://82nd-and-fifth.metmuseum.org/toah/ht/09/afa.html ; https://www.cambridge.org/core/books/abs/cambridge-history-of-africa/east-africa-the-expansion-of-commerce/8AE31B68FFE6ED0C29991E89FAB01006
- Confiance générale: **MEDIUM**

## Afrique australe
### BST — Basutoland
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `international_relations`, `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Basotho state under Moshoeshoe forms after 1818/1820; use predecessor Sotho communities. Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/people/king-moshoeshoe-i ; https://sahistory.org.za/archive/african-farmers-southern-africa
- Confiance générale: **MEDIUM**

### HRO — Herero
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/archive/african-farmers-southern-africa ; https://sahistory.org.za/article/pre-colonial-history-southern-africa
- Confiance générale: **MEDIUM**

### NAM — Nama
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/archive/african-farmers-southern-africa ; https://sahistory.org.za/article/pre-colonial-history-southern-africa
- Confiance générale: **MEDIUM**

### ORA — Oranje
- Current tier: `tier_4`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `international_relations`
- Technologies à ADD: —
- Technologies à REMOVE: `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- Technologies à REVIEW: `codified_practical_knowledge`, `distillation`, `organized_textile_production`, `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Orange Free State is founded in 1854; do not import Boer-republic institutions into 1776. Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/article/history-slavery-and-early-colonisation-south-africa ; https://sahistory.org.za/archive/african-farmers-southern-africa
- Confiance générale: **MEDIUM**

### OVB — Ovambo
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/archive/african-farmers-southern-africa ; https://sahistory.org.za/article/pre-colonial-history-southern-africa
- Confiance générale: **MEDIUM**

### PDI — Pedi
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/archive/african-farmers-southern-africa ; https://sahistory.org.za/article/pre-colonial-history-southern-africa
- Confiance générale: **MEDIUM**

### PHL — Philippolis
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `international_relations`, `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Philippolis mission station dates to 1822; use 1776 local San/Sotho-Tswana context. Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/article/general-south-african-history-timeline-1800s ; https://sahistory.org.za/archive/african-farmers-southern-africa
- Confiance générale: **MEDIUM**

### SAF — South Africa
- Current tier: `tier_2`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `distillation`, `improved_husbandry`, `organized_forestry`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `traditional_food_processing`
- Technologies à ADD: —
- Technologies à REMOVE: `atmospheric_engine`, `coke_smelting`, `commercial_insurance_markets`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `international_relations`, `periodical_print_networks`, `precision_boring`, `shaft_mining`, `stock_exchange`, `traditional_papermaking`
- Technologies à REVIEW: `enclosed_dock_systems`, `organized_textile_production`
- Technologies frontière/sectorielles: `enclosed_dock_systems`, `organized_forestry`, `scientific_fortification_siegecraft`, `state_dockyard_systems`
- Prérequis problématiques: Missing direct prerequisite(s): shaft_mining, coke_smelting. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle. Le Cap est une colonie VOC agricole et maritime: Simon’s Town donne une capacité de dockyard sectorielle, mais vapeur, alésage de précision, bourse, presse périodique et crédit public local sont surattribués.
- Sources: https://www.cambridge.org/core/journals/international-review-of-social-history/article/economics-of-slavery-in-the-eighteenthcentury-cape-colony-revising-the-nieboerdomar-hypothesis/B7EB0A6EC343E570F6D339D8BB1EAC2F ; https://sahistory.org.za/place/simons-town-cape-peninsula
- Confiance générale: **MEDIUM**

### SAN — San
- Current tier: `tier_7`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: —
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `improved_husbandry`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/archive/african-farmers-southern-africa ; https://sahistory.org.za/article/pre-colonial-history-southern-africa
- Confiance générale: **HIGH**

### SWZ — Swaziland
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `international_relations`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: The later Swazi state consolidated after 1776; use predecessor Nguni chiefdom capacities. Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/archive/african-farmers-southern-africa ; https://sahistory.org.za/article/pre-colonial-history-southern-africa
- Confiance générale: **MEDIUM**

### TRN — Transvaal
- Current tier: `tier_4`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`, `international_relations`
- Technologies à ADD: —
- Technologies à REMOVE: `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- Technologies à REVIEW: `codified_practical_knowledge`, `distillation`, `organized_textile_production`, `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Transvaal/ZAR is a nineteenth-century Boer republic; do not import its later institutions into 1776. Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/article/history-slavery-and-early-colonisation-south-africa ; https://sahistory.org.za/archive/african-farmers-southern-africa
- Confiance générale: **MEDIUM**

### TSW — Tswana
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/archive/african-farmers-southern-africa ; https://sahistory.org.za/article/pre-colonial-history-southern-africa
- Confiance générale: **MEDIUM**

### VND — Venda
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/archive/african-farmers-southern-africa ; https://sahistory.org.za/article/pre-colonial-history-southern-africa
- Confiance générale: **MEDIUM**

### WBL — Griqualand
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `international_relations`, `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Griqualand political institutions represented by the tag largely crystallize after 1776; use local Khoekhoe/Tswana context. Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/article/griqua ; https://sahistory.org.za/archive/african-farmers-southern-africa
- Confiance générale: **MEDIUM**

### XHO — Xhosa
- Current tier: `tier_6`
- Tier action: **KEEP_TIER**
- Technologies à KEEP: `improved_husbandry`, `urbanization`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/archive/african-farmers-southern-africa ; https://sahistory.org.za/article/pre-colonial-history-southern-africa
- Confiance générale: **MEDIUM**

### ZUL — Zulu
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `international_relations`, `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: The unified Zulu kingdom under Shaka postdates 1776; use late-eighteenth-century Nguni chiefdom capacities. Distinguer capacités locales des sociétés africaines, présence coloniale au Cap et entités politiques créées seulement au XIXe siècle.
- Sources: https://sahistory.org.za/article/zulu ; https://sahistory.org.za/article/pre-colonial-history-southern-africa
- Confiance générale: **MEDIUM**

## Bassin du Nil (hors Égypte)
### DFR — Darfur
- Current tier: `tier_5`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `codified_practical_knowledge`, `improved_husbandry`, `organized_textile_production`, `systematic_administrative_statistics`, `urbanization`
- Technologies à ADD: `international_relations`
- Technologies à REMOVE: —
- Technologies à REVIEW: `shaft_mining`
- Technologies frontière/sectorielles: `systematic_administrative_statistics`
- Prérequis problématiques: Missing direct prerequisite(s): institutionalized_scientific_exchange, periodical_print_networks. Do not auto-add; either tolerate tree abstraction or revise this child in synthesis.
- Justification historique: Pastoralisme, agriculture et commerce local doivent être représentés sans inventer une administration soudanaise unifiée.
- Sources: https://www.cambridge.org/core/books/land-in-dar-fur/F6769531B8A805FBC1E97907F0F8EB49 ; https://www.cambridge.org/core/books/abs/medieval-africa-12501800/upper-nile-basin-and-the-east-african-plateau/AC690A3863339F46EA0D4F76FB47AE44
- Confiance générale: **MEDIUM**

### DFT — Dar Fertit
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Pastoralisme, agriculture et commerce local doivent être représentés sans inventer une administration soudanaise unifiée.
- Sources: https://www.cambridge.org/core/books/abs/medieval-africa-12501800/upper-nile-basin-and-the-east-african-plateau/AC690A3863339F46EA0D4F76FB47AE44 ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/prehistory-in-the-upper-nile-basin1/C05AE342BF0110E91092D96D7B681597
- Confiance générale: **MEDIUM**

### DNK — Dinka
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Pastoralisme, agriculture et commerce local doivent être représentés sans inventer une administration soudanaise unifiée.
- Sources: https://www.cambridge.org/core/books/abs/medieval-africa-12501800/upper-nile-basin-and-the-east-african-plateau/AC690A3863339F46EA0D4F76FB47AE44 ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/prehistory-in-the-upper-nile-basin1/C05AE342BF0110E91092D96D7B681597
- Confiance générale: **MEDIUM**

### NUE — Nuer
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Pastoralisme, agriculture et commerce local doivent être représentés sans inventer une administration soudanaise unifiée.
- Sources: https://www.cambridge.org/core/books/abs/medieval-africa-12501800/upper-nile-basin-and-the-east-african-plateau/AC690A3863339F46EA0D4F76FB47AE44 ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/prehistory-in-the-upper-nile-basin1/C05AE342BF0110E91092D96D7B681597
- Confiance générale: **MEDIUM**

### SD1 — The Sudan
- Current tier: `tier_6`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: `improved_husbandry`
- Technologies à ADD: —
- Technologies à REMOVE: —
- Technologies à REVIEW: `urbanization`
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: “The Sudan” is a modern umbrella label rather than a unitary 1776 polity; assess local Nile/Sudan societies. Pastoralisme, agriculture et commerce local doivent être représentés sans inventer une administration soudanaise unifiée.
- Sources: https://www.cambridge.org/core/books/abs/medieval-africa-12501800/upper-nile-basin-and-the-east-african-plateau/AC690A3863339F46EA0D4F76FB47AE44 ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/prehistory-in-the-upper-nile-basin1/C05AE342BF0110E91092D96D7B681597
- Confiance générale: **MEDIUM**

### TPS — Toposa
- Current tier: `tier_7`
- Tier action: **REPLACE_WITH_EXPLICIT_SETUP**
- Technologies à KEEP: —
- Technologies à ADD: `improved_husbandry`
- Technologies à REMOVE: —
- Technologies à REVIEW: —
- Technologies frontière/sectorielles: —
- Prérequis problématiques: —
- Justification historique: Pastoralisme, agriculture et commerce local doivent être représentés sans inventer une administration soudanaise unifiée.
- Sources: https://www.cambridge.org/core/books/abs/medieval-africa-12501800/upper-nile-basin-and-the-east-african-plateau/AC690A3863339F46EA0D4F76FB47AE44 ; https://www.cambridge.org/core/journals/journal-of-african-history/article/abs/prehistory-in-the-upper-nile-basin1/C05AE342BF0110E91092D96D7B681597
- Confiance générale: **MEDIUM**

## 5. Comparaison régionale

- **Maghreb** : supériorité relative en arsenaux, ports fortifiés, artillerie, fiscalité urbaine et commerce méditerranéen; les sociétés sahariennes conservent en parallèle des capacités pastorales et caravanières sans devoir recevoir un paquet urbain/industriel.
- **Afrique de l’Ouest** : forte métallurgie du fer, agriculture, textiles et commerce; armes à feu très présentes mais souvent importées. Ashanti/Dahomey/Oyo/Benin exigent des setups d’État plus riches que les tiers 5/6, mais pas des technologies de vapeur/coke.
- **Afrique centrale** : royaumes Kuba, Kongo, Luba, Lunda et réseaux voisins combinent textile/raffia, cuivre/fer, artisanat et commerce. Les tiers 7 vides sous-estiment clairement ces capacités.
- **Corne/Éthiopie** : textile, artisanat, agriculture et institutions de cour propres; la diffusion des armes à feu ne justifie pas encore un modèle militaire centré sur une industrie d’armes réglementée.
- **Afrique orientale / côte swahilie** : ports et commerce de l’océan Indien sont avancés régionalement; distinguer navigation marchande, fortifications et véritable dockyard d’État.
- **Afrique australe** : agriculture, élevage et métallurgie africains doivent être séparés des technologies importées de la colonie du Cap. Les futurs États boers/nguni/sotho ne doivent pas fournir rétroactivement leurs institutions du XIXe siècle.
- **Haut-Nil/Darfour** : le pastoralisme nilotique est techniquement central; Darfour possède une capacité étatique/fiscale bien plus forte que les sociétés pastorales du Sudd. Un seul tier régional serait particulièrement trompeur.

## 6. Technologies frontière 1776

| Technologie | Zone/cas | Décision | Diagnostic |
|---|---|---|---|
| `light_infantry_tactics` / `standardized_field_artillery` | Maghreb surtout | **KEEP/REVIEW sectoriel** | États maghrébins disposent de troupes, fortifications et artillerie; la standardisation exacte reste inégale. |
| `atmospheric_engine` | Cap uniquement actuellement | **REMOVE** | La présence européenne ne prouve aucune implantation locale de pompes Newcomen au Cap en 1776. |
| `precision_boring` | Cap uniquement actuellement | **REMOVE** | Technique-frontière britannique/industrielle non implantée localement. |
| `applied_mineralogy` | Liberia actuellement | **REMOVE** | Liberia n’existe pas; ne pas confondre extraction minière africaine avec minéralogie appliquée institutionnelle. |
| `improved_agricultural_implements` | Madagascar (review) | **REVIEW** | Riziculture/irrigation avancée ≠ preuve d’outillage du nœud; pas de diffusion africaine automatique. |
| `variolation_networks` | Afrique, potentiel historique | **REVIEW mondial ultérieur** | La pratique d’inoculation mérite une étude dédiée si le nœud est redistribué, mais les preuves de réseaux institutionnels pays par pays sont insuffisantes ici. |
| autres B: mécanisation textile, canaux, académies, médecine, cadastral, etc. | Afrique | **pas d’ADD générique** | Aucune raison de les distribuer par “niveau” : seules preuves locales/institutionnelles spécifiques pourraient les justifier. |

## 7. Anachronismes et sur-attributions à retirer

- **GZA — Gaza**: `international_relations`
- **LIB — Liberia**: `applied_mineralogy`, `coke_smelting`, `commercial_insurance_markets`, `light_infantry_tactics`, `medical_degrees`, `regulated_small_arms`, `shaft_mining`, `specialized_technical_academies`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **ORA — Oranje**: `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **SAF — South Africa**: `atmospheric_engine`, `coke_smelting`, `commercial_insurance_markets`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `international_relations`, `periodical_print_networks`, `precision_boring`, `shaft_mining`, `stock_exchange`, `traditional_papermaking`
- **SIL — Sierra Leone**: `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`
- **TRN — Transvaal**: `light_infantry_tactics`, `regulated_small_arms`, `shaft_mining`, `standardized_field_artillery`, `systematic_administrative_statistics`

Points les plus robustes : vapeur/coke/alésage de précision au Cap; bourse et presse périodique au Cap; technologies d’académies/médecine/minéralogie et armement du Liberia; paquet militaire des futurs TAG boers; institutions d’État/coloniales explicitement postérieures lorsqu’elles sont la seule justification.

## 8. Prérequis

Le problème le plus fréquent est que l’arbre encode une généalogie européenne des institutions. Exemple : `codified_practical_knowledge` exige des parents d’échange scientifique/presse dans le mod, alors que des savoirs artisanaux codifiés ou transmis peuvent exister selon d’autres institutions. La matrice signale donc les parents directs absents mais **ne les ajoute jamais automatiquement**. Dans le Maghreb, `scientific_fortification_siegecraft` est ajouté lorsque l’histoire locale des fortifications/garnisons le justifie et qu’il répare aussi un parent manquant de `regulated_small_arms`; ailleurs la dette de prérequis peut être tolérée comme abstraction ou conduire à retirer l’enfant lors de la synthèse mondiale.

## 9. Incertitudes

1. **`shaft_mining`** : le nœud mélange trop de ressources et ne correspond pas proprement aux traditions africaines d’extraction/forge; beaucoup de relations restent REVIEW.
2. **`systematic_administrative_statistics`** : tribut, cadastres locaux, registres et fiscalité ne sont pas équivalents à la statistique d’État moderne; KEEP est souvent marqué SECTORAL/ABSTRACT.
3. **TAG postérieurs** : la technologie de 1776 doit représenter les sociétés du territoire, pas l’institution future. Une future refonte des TAG/start politiques pourrait changer la meilleure solution technique.
4. **`urbanization`** : c’est une exception de compatibilité dans l’audit; sa présence n’est pas lue comme preuve de ville industrielle. Les sociétés nomades/pastorales sont REVIEW.
5. **Armes à feu** : Afrique de l’Ouest et Madagascar montrent pourquoi il faut séparer importation, poudre/réparation et fabrication complète. `regulated_small_arms` est donc conservateur.
6. **Naval** : la côte swahilie et les régences maghrébines ont de vraies capacités maritimes, mais `state_dockyard_systems` est accordé seulement là où une infrastructure d’État est suffisamment plausible; Mombasa/Majerteen/Angoche restent REVIEW.

## 10. Recommandations pour l’implémentation (sans code)

### Tiers pouvant rester comme squelette
`AJR`, `ANK`, `BMB`, `BRD`, `CHK`, `KBD`, `KBU`, `KNG`, `LUO`, `MZB`, `NYM`, `PDI`, `SAN`, `TMN`, `TUA`, `TUG`, `VND`, `XHO`, `YKA`

### Pays à corriger explicitement
`ACH`, `AGC`, `AIT`, `ANU`, `ARS`, `ASH`, `AWS`, `AYI`, `BEN`, `BGI`, `BGM`, `BLE`, `BMM`, `BND`, `BNG`, `BNY`, `BOB`, `BOR`, `BRG`, `BRN`, `BST`, `BUG`, `CAY`, `CON`, `DAH`, `DAK`, `DFR`, `DFT`, `DIO`, `DLA`, `DNK`, `ETH`, `EWE`, `FNG`, `FTJ`, `FTR`, `FZN`, `GGO`, `GJM`, `GLD`, `GZA`, `HAR`, `HAU`, `HDY`, `HHE`, `HMB`, `HRO`, `IBO`, `ISQ`, `JLF`, `KBA`, `KFA`, `KKY`, `KON`, `KRG`, `KRT`, `KRU`, `KSN`, `KZM`, `LBA`, `LGA`, `LIB`, `LND`, `LNG`, `LZO`, `MAD`, `MAS`, `MBS`, `MDK`, `MJK`, `MJT`, `MNB`, `MNC`, `MOR`, `MOS`, `MRV`, `MSH`, `MSI`, `MSK`, `MSN`, `MTB`, `MTP`, `NAM`, `NUE`, `OGD`, `OMO`, `ORA`, `ORM`, `OVB`, `OVM`, `OYO`, `PHL`, `QWR`, `RWD`, `SAF`, `SD1`, `SDM`, `SGU`, `SHW`, `SIL`, `SKM`, `SKY`, `SNG`, `SOK`, `SRR`, `SSU`, `SWZ`, `TGI`, `TGR`, `TKE`, `TPS`, `TRI`, `TRK`, `TRN`, `TSW`, `TUN`, `WAD`, `WBL`, `WLG`, `WLT`, `WSG`, `WTU`, `ZND`, `ZUL`

### Pays dont le tier doit être revu
`ADG`, `ADR`, `AHG`, `AIR`, `AJJ`, `ATR`, `AUL`, `BRK`, `CMB`, `DIN`, `DLM`, `OUA`, `RGB`, `SAH`, `TBI`, `TEK`, `TRZ`, `ZWY`

**Aucun `CHANGE_TIER` global n’est recommandé dans cette vague.** Le diagnostic montre précisément pourquoi : déplacer un pays de tier corrigerait une capacité tout en en cassant plusieurs autres. Les corrections explicites sont préférables.

## Contrôle final

- TAG étudiés: **161**
- Décisions ADD: **95**
- Décisions REMOVE: **37**
- Décisions REVIEW: **146**
- Décisions KEEP: **322**
- Pays avec `CHANGE_TIER`: **0**
- Pays `REPLACE_WITH_EXPLICIT_SETUP`: **124**
- Pays `REVIEW_TIER`: **18**
- Pays `KEEP_TIER`: **19**
- Technologies C/D actuellement attribuées aux TAG africains: **0** (donc aucun anachronisme C/D à retirer dans cette région; les retraits concernent surtout des A/B localement absentes ou des institutions de TAG postérieurs).
- Principales incertitudes: correspondance de `shaft_mining`, portée de `systematic_administrative_statistics`, statut gameplay d’`urbanization`, fabrication locale d’armes vs importation, précision politique des TAG postérieurs à 1776.
