# Second pass complet — Technologies de départ 1776 — Europe occidentale

**Date absolue : 1776-01-01.**  
**Recherche uniquement. Aucun fichier gameplay modifié. Aucun code Victoria 3. Aucun commit/push.**

## 1. Périmètre

TAG audités : **GBR, FRA, NET, SPA, POR, BEL, BEO, IREK, LUX, SPC**. SPA/POR/SPC sont inclus conformément au périmètre régional demandé, même si le CSV technique les classe géographiquement en `Southern Europe`. Les colonies extra-européennes à TAG propre restent exclues.

| TAG | Pays du CSV | Source générique actuelle |
|---|---|---|
| GBR | Great Britain | `tier_4` |
| FRA | France | `tier_4` |
| NET | Netherlands | `tier_4` |
| SPA | Spain | `tier_4` |
| POR | Portugal | `tier_4` |
| BEL | Belgium | `tier_1` |
| BEO | Belgium | `tier_4` |
| IREK | Kingdom of Ireland | `tier_4` |
| LUX | Luxembourg | `tier_4` |
| SPC | Carlist Spain | `tier_3` |

Le socle obligatoire contient **25 technologies A + 36 technologies B = 61 technologies par TAG**, soit **610 relations A/B**. Le rapport ajoute **20 relations E** (`colonization`, `urbanization`) et **8 relations C** effectivement examinées, pour **638 lignes** au total.

## 2. Sources et méthode

### Autorité technique

- `TECH_START_1776_TECHNOLOGIES.csv` : IDs, classifications, catégories, distribution actuelle et déblocages.
- `TECH_START_1776_COUNTRIES.csv` : TAG et noms.
- `TECH_START_1776_WESTERN_EUROPE_MATRIX.csv` : comparaison avec la première passe.
- La distribution actuelle sert **uniquement** à calculer `Current_Status`; elle n'est jamais utilisée comme preuve historique.

### Sémantique des décisions dans une matrice exhaustive

Comme chaque A/B doit recevoir une décision même lorsqu'elle est correctement absente, `KEEP` a deux usages explicitement distingués par `Current_Status` :
- `PRESENT + KEEP` = conserver l'attribution.
- `ABSENT + KEEP` = conserver l'absence.
- `ADD` et `REMOVE` sont donc de vrais changements de distribution ; `REVIEW` signifie que le dossier historique/gameplay reste ambigu.

### Mise à jour de l'arbre `organized_forestry`

La consigne de second pass est considérée comme plus récente que les anciennes dépendances visibles dans le snapshot CSV : **`traditional_papermaking`, `traditional_glassmaking` et `traditional_furniture_making` sont évaluées indépendamment d'`organized_forestry`**, et la simple coupe de bois ne suffit plus à justifier `organized_forestry`. Ces trois anciennes arêtes ne génèrent donc aucun `TREE_STRUCTURE_REVIEW`. Le nœud forestier n'est accordé que lorsqu'une exploitation/gestion organisée ou rationalisée est historiquement documentée.

### Références historiques principales

**Grande-Bretagne**
- https://collection.sciencemuseumgroup.org.uk/objects/co50900/newcomen-atmospheric-engine
- https://collection.sciencemuseumgroup.org.uk/objects/co46448/cast-iron-boring-bar-and-boring-head
- https://collection.sciencemuseumgroup.org.uk/objects/co44832/arkwrights-water-frame-1775-spinning-machine
- https://www.lr.org/en/about-us/who-we-are/our-history/
- https://www.lloyds.com/about-lloyds/history
- https://www.nam.ac.uk/explore/corps-royal-engineers
- https://www.rmg.co.uk/collections/objects/rmgc-object-79183
- https://www.bankofengland.co.uk/freedom-of-information/2020/details-of-the-bank-of-england-loan-to-the-government-in-1694
- https://www.rcpe.ac.uk/heritage/teaching
- https://www.nrscotland.gov.uk/learning-and-events/research-guides/education-records/

**France**
- https://ecoledesponts.fr/lecole/bienvenue-lecole/lecole-dans-lhistoire
- https://www.academie-sciences.fr/lhistoire-de-lacademie
- https://www.cambridge.org/core/journals/journal-of-economic-history/article/abs/financial-market-and-government-debt-policy-in-france-17461793/15A623836DA5D950BA79E33E1781FA7A
- https://www.economie.gouv.fr/facileco/historique
- https://www.jstor.org/stable/jj.7855347
- https://elischolar.library.yale.edu/gsas_dissertations/1226/
- https://facmedecine.umontpellier.fr/patrimoine-historique/son-histoire/
- https://www.defense.gouv.fr/sante/mieux-nous-connaitre/trois-cents-ans-dhistoire
- https://comptes-rendus.academie-sciences.fr/chimie/articles/10.1016/j.crci.2012.04.009/
- https://www.vet-alfort.fr/aaeaea/250-ans-d-histoire-documentation
- https://www.shom.fr/index.php/fr/300_ans

**Provinces-Unies**
- https://whc.unesco.org/en/list/1349
- https://www.hetscheepvaartmuseum.nl/over-ons/het-gebouw
- https://intellectualhistory.site.ox.ac.uk/article/parliamentary-culture-and-public-credit-how-merchants-overcame-their-weak-position
- https://books.google.com/books/about/Marine_Insurance_in_the_Netherlands_1600.html?id=KPihRWh7BlUC
- https://www.worldsfirststockexchange.com/
- https://www.rijksmuseumboerhaave.nl/en/article/museumbuilding
- https://www.nederlandseboekgeschiedenis.nl/en/handbook/1585-1725-hey-day-centre-world-trade/242-1585-1725-education-and-literacy
- https://www.dbnl.org/tekst/lint011gesc04_01/lint011gesc04_01_0005.php

**Espagne**
- https://cvc.cervantes.es/actcult/museo_naval/patio_central/caracteristicas/
- https://ejercito.defensa.gob.es/unidades/Segovia/acart/Noticias/2019/059.html
- https://ejercito.defensa.gob.es/noticias/2020/04/7935_aniversario_ingenieros.html
- https://www.bolsasymercados.es/en/bme-exchange/madrid-stock-exchange/history.html
- https://hispania.revistas.csic.es/index.php/hispania/article/view/625
- https://www.cultura.gob.es/cultura/areas/archivos/mc/archivos/ags/destacados/2019/comprobaciones-galicia.html
- https://facultadmedicina.usal.es/resena-historica/
- https://www.rtve.es/play/audios/a-hombros-de-gigantes/palabra-ingeniero-primera-maquina-vapor-espana-05-10-21/6125838/

**Portugal**
- https://www.uc.pt/org/historia_ciencia_na_uc/Textos/ocontexto/2_acriacao
- https://www.marinha.pt/Conteudos_Externos/Revista_Armada/2014/484/files/basic-html/page13.html
- https://www.euronext.com/en/markets/lisbon
- https://museuvirtualdoseguro.pt/en/history/
- https://www.cambridge.org/core/journals/itinerario/article/rise-and-fall-of-a-lisbon-family-business-17101773-the-case-of-the-house-of-torres/290F11748BB6897BEB6BD545AF63B15A/share/d03f7c739a8a5a01d2fc83d1b37c58d5e8857c69
- https://am.uc.pt/pombalia/items?_date_interval=1772&_fo=-title&_fp=2&_l=100&_o=-title&_p=1&_t=list&date=17721110
- https://imovel.patrimoniocultural.gov.pt/detalhes.php?code=71808

**Pays-Bas méridionaux**
- https://academieroyale.be/fr/l-academie-royale-histoire/
- https://med.kuleuven.be/en/about-us/facts-figures
- https://www.persee.fr/doc/pharm_0035-2349_1973_num_61_217_8414_t1_0458_0000_1
- https://connaitrelawallonie.wallonie.be/histoire/timeline/18-janvier-1721-installation-de-la-toute-premiere-pompe-feu-du-continent-jemeppe
- https://www.industriemuseum.be/nl/collectie-item/geschiedenis-van-hoogovens
- https://www.cambridge.org/core/journals/annales-histoire-sciences-sociales/article/abs/les-campagnes-flamandes-du-xiiie-siecle-au-xviiie-siecle-ou-les-succes-dune-agriculture-traditionnelle/15A2A299629F9C8BC5877BDFAB733E5C
- https://shop.ngi.be/fr/cartes-historiques/carte-de-ferraris-des-pays-bas-autrichiens-1771-1778/

**Irlande**
- https://www.rds.ie/about-rds/governance/rds-history
- https://digitalarchive.rds.ie/exhibits/show/rdsshows/intro1
- https://www.tcd.ie/medicine/about-us/history-of-the-school/
- https://historyireland.com/vaccination-in-ireland-the-evolution-of-a-process/
- https://archive.waterwaysireland.org/history-of-the-waterways/9/the-history-of-the-grand-canal
- https://www.centralbank.ie/docs/default-source/publications/quarterly-bulletins/quarterly-bulletin-signed-articles/irish-currency-report-of-1804.pdf?sfvrsn=4
- https://www.euronext.com/en/about-euronext/markets/dublin

**Luxembourg**
- https://whc.unesco.org/en/list/699
- https://bnl.public.lu/en/a-la-une/a-la-loupe/2024/feller.html
- https://www.uni.lu/en/about/profile/history/
- https://luxembourg.public.lu/fr/societe-et-culture/histoire/siderurgie-luxembourg.html

**Datation des nœuds problématiques**
- https://collection.sciencemuseumgroup.org.uk/people/ap13666/cartwright-edmund
- https://www.si.edu/object/nmah_630930
- https://www.scielo.org.mx/scielo.php?pid=S0187-893X2012000200010&script=sci_arttext
- https://www.adamsmithworks.org/documents/editor-s-introduction

### Règle de prérequis

La réalité historique est décidée d'abord. `ADD_WITH_PREREQUISITES` signifie que le ou les parents sont eux-mêmes historiquement défendables et doivent être ajoutés. `TREE_STRUCTURE_REVIEW` signifie que l'enfant est historiquement réel mais qu'au moins un parent ne l'est pas ou encode un chemin institutionnel différent.

## 3. Production

### Matrice production et artisanat

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `distillation` | A | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ |
| `organized_textile_production` | A | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ |
| `traditional_food_processing` | A | ADD | KEEP+ | ADD | ADD | ADD | KEEP+ | ADD | ADD | ADD | ADD |
| `traditional_papermaking` | A | ADD | ADD | ADD | ADD | ADD | KEEP+ | ADD | ADD | ADD | ADD |
| `industrial_acids` | A | ADD | ADD | KEEP− | KEEP− | KEEP− | ADD | ADD | KEEP− | KEEP− | KEEP− |
| `sugar_refining` | A | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− |
| `traditional_furniture_making` | A | ADD | ADD | ADD | ADD | ADD | ADD | ADD | ADD | ADD | ADD |
| `traditional_glassmaking` | A | ADD | ADD | ADD | ADD | ADD | ADD | ADD | ADD | REV− | ADD |
| `industrial_ceramics` | B | ADD | ADD | ADD | ADD | ADD | ADD | ADD | REV− | REV− | ADD |
| `mechanized_spinning` | B | ADD | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− |
| `mechanized_weaving` | B | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− |
| `advanced_spinning` | B | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− |

Constats : les manufactures traditionnelles de papier, verre et meuble sont beaucoup plus larges que dans la distribution actuelle une fois supprimée la dépendance artificielle à la foresterie organisée. `industrial_acids` est au contraire sélective : Grande-Bretagne, France et Pays-Bas autrichiens possèdent des productions chimiques pré-1776 documentées. `sugar_refining` est un problème de définition : le raffinage traditionnel est ancien, mais les PM débloqués (vacuum pan, vapeur, centrifuge, betterave) sont largement postérieurs ; toutes les lignes restent REVIEW avec `CLASSIFICATION_TOO_EARLY`.

## 4. Agriculture

### Matrice agriculture

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `improved_husbandry` | A | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ |
| `improved_agricultural_implements` | B | ADD | ADD | ADD | REV− | REV− | ADD | ADD | ADD | REV− | REV− |
| `advanced_crop_rotations` | B | ADD | REV− | ADD | KEEP− | KEEP− | KEEP+ | ADD | REV− | KEEP− | KEEP− |
| `selective_breeding` | B | ADD | KEEP− | REV− | KEEP− | KEEP− | REV− | REV− | REV− | KEEP− | KEEP− |

La Grande-Bretagne reste la seule attribution haute-confiance de `selective_breeding` au sens Bakewell. Les rotations flamandes sont au contraire une force propre des Pays-Bas méridionaux et ne doivent pas être bloquées par l'absence de sélection animale : ce prérequis est un cas de `TREE_STRUCTURE_REVIEW`. La Dublin Society donne à l'Irlande un dossier particulièrement solide pour les outils agricoles améliorés.

## 5. Mines/métallurgie

### Matrice mines et métallurgie

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `shaft_mining` | A | KEEP+ | KEEP+ | REMOVE | KEEP+ | REV+ | KEEP+ | KEEP+ | KEEP+ | REMOVE | KEEP+ |
| `applied_mineralogy` | B | REV− | REV− | KEEP− | ADD | KEEP− | REV− | REV− | REV− | KEEP− | KEEP+ |
| `coke_smelting` | A | ADD | KEEP− | KEEP− | KEEP− | KEEP− | REMOVE | KEEP− | KEEP− | KEEP− | REMOVE |
| `atmospheric_engine` | B | ADD | ADD | KEEP− | REV− | KEEP− | KEEP+ | ADD | REV− | KEEP− | REV+ |
| `precision_boring` | B | ADD | KEEP− | KEEP− | KEEP− | KEEP− | REMOVE | KEEP− | KEEP− | KEEP− | KEEP− |
| `condensing_steam_engines` | B | REV− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− |

Le couple coke–vapeur doit rester asymétrique. GBR possède les deux. FRA et BEL/BEO ont des machines Newcomen sans sidérurgie locale au coke, d'où `TREE_STRUCTURE_REVIEW`. NET n'a pas encore de machine opérationnelle au 1er janvier 1776 ; elle ne démarre qu'en mars. `precision_boring` est une frontière britannique c.1775 et doit être retirée de BEL. `condensing_steam_engines` reste REVIEW même pour GBR au cutoff strict.

## 6. Infrastructure

### Matrice infrastructure

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `organized_forestry` | A | ADD | ADD | REV− | ADD | ADD | KEEP+ | ADD | ADD | REV− | ADD |
| `turnpike_road_networks` | B | ADD | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− |
| `industrial_canals` | B | ADD | ADD | ADD | REV− | KEEP− | REV− | REV− | REV− | KEEP− | REV− |

| Technologie complémentaire | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `urbanization` | E | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | ADD | KEEP+ | KEEP+ | KEEP+ | KEEP+ |
| `professional_civil_engineering` | C | — | REV− | — | — | — | — | — | — | — | — |
| `hydraulic_cements` | C | REV− | — | — | — | — | — | — | — | — | — |

`organized_forestry` est désormais interprétée comme une capacité de gestion/exploitation organisée, pas comme le droit de couper du bois. Les routes/canaux restent institutionnellement hétérogènes : le modèle britannique de turnpike ne doit pas être imposé à la France ou aux Provinces-Unies. `professional_civil_engineering` est signalée C à revoir pour FRA, où le Corps des Ponts et Chaussées (1716) et son école (1747) sont antérieurs au cutoff.

## 7. Finance et économie

### Matrice finance et économie

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `institutionalized_public_credit` | A | ADD | ADD | ADD | REV− | ADD | REV+ | REV− | REV− | KEEP− | REV− |
| `commercial_insurance_markets` | A | ADD | ADD | ADD | ADD | ADD | REV+ | REV− | REV− | KEEP− | KEEP+ |
| `stock_exchange` | A | ADD | ADD | ADD | KEEP− | ADD | REV+ | REV− | KEEP− | KEEP− | REMOVE |
| `political_economy` | B | ADD | ADD | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− |
| `classical_political_economy` | B | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− |

Le plus grand correctif est la fin de l'assimilation « finance avancée = seulement GBR/NET ». FRA possède une bourse réglementée depuis 1724 et un marché actif de dette publique. POR possède une Casa dos Seguros pré-1776 et une institution de bourse/commerçants créée en 1769 ; son crédit public est moins profond mais suffisamment documenté pour ADD. L'Espagne reste plus prudente : assurance sectorielle oui, `stock_exchange` non (Madrid 1831).

## 8. Commerce

### Relations internationales

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `international_relations` | A | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | REV+ | REV+ | REV+ | REV+ | KEEP+ |

| Technologie E | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `colonization` | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP− | KEEP− | KEEP− | KEEP− | ADD |

Les puissances marchandes sont distinguées par leurs institutions réelles. Les territoires dépendants BEL/BEO/IREK/LUX restent REVIEW pour `international_relations` : ils participent à des circuits impériaux/crown, mais ne disposent pas d'une diplomatie souveraine équivalente. `colonization` est traité comme une abstraction institutionnelle et non comme une technologie matérielle transmissible aux colonies.

## 9. Administration

### Matrice administration et institutions politiques

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `systematic_administrative_statistics` | A | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ |
| `codified_practical_knowledge` | A | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | ADD | KEEP+ | KEEP+ | REV+ | KEEP+ |
| `systematic_population_registration` | B | REV− | KEEP+ | REV− | ADD | REV− | REV− | REV− | REV− | REV− | ADD |
| `systematic_cadastral_surveying` | B | KEEP− | KEEP− | KEEP− | ADD | KEEP− | REV− | REV− | KEEP− | REV− | ADD |
| `systematic_legal_codification` | B | KEEP− | REV− | REV− | REV− | KEEP+ | REV− | REV+ | KEEP− | REV− | REV− |
| `constitutional_government` | B | ADD | KEEP− | ADD | KEEP− | KEEP− | KEEP− | KEEP− | REV− | KEEP− | KEEP− |
| `human_rights` | B | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− |
| `national_sovereignty` | B | KEEP− | KEEP− | REV− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− |

L'administration de base est largement établie, mais les nœuds plus précis ne le sont pas automatiquement. Le Catastro de Ensenada justifie `systematic_cadastral_surveying` en Espagne. La France conserve `systematic_population_registration`. `systematic_legal_codification` reste très dépendante du sens du nœud : Portugal est le cas le plus solide du groupe, tandis que common law britannique/irlandaise ne justifie pas une codification générale.

## 10. Science/éducation

### Matrice science et éducation

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `institutionalized_scientific_exchange` | A | ADD | ADD | ADD | ADD | ADD | KEEP+ | ADD | KEEP+ | REV− | ADD |
| `periodical_print_networks` | A | ADD | ADD | ADD | ADD | ADD | KEEP+ | ADD | ADD | ADD | KEEP+ |
| `organized_elementary_schooling` | B | ADD | REV− | ADD | REV− | ADD | REV− | REV− | REV− | REV− | REV− |
| `specialized_technical_academies` | B | KEEP+ | KEEP+ | REV+ | KEEP+ | KEEP+ | REV− | REV+ | KEEP− | KEEP− | KEEP+ |
| `veterinary_science` | B | KEEP− | ADD | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− |

Les académies et sociétés savantes sont plus largement distribuées que dans l'ancien setup, mais `specialized_technical_academies` reste plus restrictive. L'enseignement élémentaire organisé est solide pour GBR via le système paroissial écossais, NET via la supervision municipale et POR après la réforme scolaire de 1772. FRA est la seule attribution haute-confiance de `veterinary_science` grâce à Lyon (1761) et Alfort (1765).

## 11. Médecine

### Matrice médecine

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `variolation_networks` | B | ADD | REV− | ADD | REV− | REV− | REV− | REV− | ADD | KEEP− | REV− |
| `medical_degrees` | B | ADD | ADD | ADD | ADD | ADD | ADD | ADD | ADD | KEEP− | KEEP+ |

`medical_degrees` est le correctif conceptuel le plus important : le brief la définit comme facultés/collèges médicaux, titres reconnus, formation et certification institutionnalisées. À ce sens, elle est **ESTABLISHED** dans GBR, FRA, NET, SPA, POR, BEL/BEO et IREK, et déjà présente dans SPC. Sa classification B est donc `CLASSIFICATION_TOO_LATE` dans neuf relations. Variolisation : GBR est clairement organisée ; NET et IREK sont sectoriels ; plusieurs autres pays restent REVIEW faute de preuve d'un réseau durable plutôt que de simples inoculations.

## 12. Militaire

### Matrice militaire terrestre

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `scientific_fortification_siegecraft` | A | ADD | ADD | ADD | ADD | ADD | KEEP+ | ADD | REV− | ADD | ADD |
| `regulated_small_arms` | A | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | ADD | KEEP+ | REV+ | REV+ | KEEP+ |
| `light_infantry_tactics` | B | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | ADD | KEEP+ | KEEP+ | KEEP+ | KEEP+ |
| `permanent_military_hospitals` | B | ADD | ADD | REV− | REV− | REV− | REV− | REV− | REV− | REV− | REV− |
| `standardized_field_artillery` | B | KEEP+ | KEEP+ | KEEP+ | KEEP+ | KEEP+ | ADD | KEEP+ | KEEP+ | KEEP+ | KEEP+ |
| `armament_standardization_inspection` | B | ADD | ADD | REV− | ADD | REV− | REV− | REV− | KEEP− | KEEP− | ADD |
| `horse_artillery` | B | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− |
| `military_topographic_surveying` | B | ADD | ADD | REV− | ADD | REV− | ADD | ADD | REV− | REV− | ADD |
| `permanent_engineer_services` | B | ADD | ADD | ADD | ADD | ADD | ADD | ADD | REV− | ADD | ADD |

Les grandes armées ne reçoivent pas mécaniquement tous les B. Les corps d'ingénieurs sont solides pour GBR/FRA/SPA ; le système Gribeauval rend l'inspection/standardisation particulièrement forte en FRA. La cartographie Ferraris (1771-1778) rend le topographic surveying très crédible dans BEL/BEO mais encore FRONTIER. `horse_artillery` reste absent dans toute la région au cutoff.

## 13. Marine

### Matrice marine

Légende : `KEEP+` = présent et conservé ; `KEEP−` = absent et maintenu absent ; `ADD` = à ajouter ; `REMOVE` = à retirer ; `REV+`/`REV−` = attribution présente/absente à réexaminer.

| Technologie | Cl. | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `enclosed_dock_systems` | A | ADD | ADD | ADD | ADD | ADD | REV+ | REV− | REV− | KEEP− | ADD |
| `state_dockyard_systems` | A | ADD | ADD | ADD | ADD | ADD | REMOVE | KEEP− | KEEP− | KEEP− | ADD |
| `scientific_naval_architecture` | A | ADD | ADD | ADD | ADD | ADD | REMOVE | KEEP− | KEEP− | KEEP− | ADD |
| `marine_chronometry` | B | ADD | ADD | REV− | REV− | REV− | KEEP− | KEEP− | KEEP− | KEEP− | REV− |
| `ship_classification_surveying` | B | ADD | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− |
| `copper_sheathing` | B | ADD | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− | KEEP− |

| Technologie C examinée | GBR | FRA | NET | SPA | POR | BEL | BEO | IREK | LUX | SPC |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `hydrographic_surveying` | — | REV− | — | — | — | — | — | — | — | — |

GBR et FRA obtiennent `marine_chronometry` comme FRONTIER ; Espagne reste REVIEW à cause du calendrier exact des instruments Berthoud autour de 1775-1776. Lloyd's Register justifie `ship_classification_surveying` seulement pour GBR. Le cuivre de coque britannique est FRONTIER : expérimentation avant 1776, généralisation plus tardive. FRA reçoit un `CLASSIFICATION_REVIEW` pour `hydrographic_surveying`, puisque son Dépôt des cartes et plans de la Marine existe depuis 1720.

## 14. Analyse pays par pays

### GBR — Great Britain

La Grande-Bretagne reste le principal foyer régional de la première industrialisation mécanique, mais le second pass la rend beaucoup plus **spécifique** : coke, Newcomen, water frame, alésage Wilkinson, réseaux de turnpikes/canaux et innovations navales sont ajoutés parce qu'ils sont documentés, non parce que GBR est une grande puissance. La finance publique, le marché des titres, la classification navale de Lloyd's, les écoles paroissiales écossaises et la médecine institutionnelle sont également des capacités autonomes. En revanche, `condensing_steam_engines` reste REVIEW au cutoff strict : Watt avait breveté le condenseur séparé, mais les premières installations commerciales n'entrent en service qu'en 1776.

**Comptage :** ADD 37 · REMOVE 1 · KEEP 19 · REVIEW 9.

**ADD :** `coke_smelting`, `industrial_acids`, `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`, `commercial_insurance_markets`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `stock_exchange`, `advanced_crop_rotations`, `atmospheric_engine`, `improved_agricultural_implements`, `industrial_canals`, `industrial_ceramics`, `mechanized_spinning`, `precision_boring`, `selective_breeding`, `turnpike_road_networks`, `armament_standardization_inspection`, `copper_sheathing`, `marine_chronometry`, `military_topographic_surveying`, `permanent_engineer_services`, `permanent_military_hospitals`, `ship_classification_surveying`, `constitutional_government`, `medical_degrees`, `organized_elementary_schooling`, `political_economy`, `variolation_networks`

**REMOVE :** `romanticism`

**REVIEW :** `sugar_refining`, `advanced_spinning`, `applied_mineralogy`, `condensing_steam_engines`, `mechanized_weaving`, `classical_political_economy`, `systematic_population_registration`, `crystal_glass`, `hydraulic_cements`

### FRA — France

La France ressort comme le pays le plus sous-évalué par l'ancienne logique de tier dans plusieurs domaines non industriels. `institutionalized_public_credit`, `stock_exchange`, `medical_degrees`, `political_economy`, `permanent_military_hospitals`, `veterinary_science`, `industrial_acids`, la chronométrie marine et plusieurs capacités de génie doivent être ajoutés. La Bourse de Paris est réglementée depuis 1724 ; la dette publique est activement négociée ; Montpellier fournit un exemple séculaire de formation médicale ; Lyon/Alfort rendent la science vétérinaire indiscutable. En revanche le coke reste absent avant Le Creusot (1785), même si des pompes Newcomen existent déjà : c'est un cas majeur de `TREE_STRUCTURE_REVIEW`.

**Comptage :** ADD 26 · REMOVE 1 · KEEP 27 · REVIEW 13.

**ADD :** `industrial_acids`, `organized_forestry`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`, `commercial_insurance_markets`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `stock_exchange`, `atmospheric_engine`, `improved_agricultural_implements`, `industrial_canals`, `industrial_ceramics`, `armament_standardization_inspection`, `marine_chronometry`, `military_topographic_surveying`, `permanent_engineer_services`, `permanent_military_hospitals`, `medical_degrees`, `political_economy`, `veterinary_science`

**REMOVE :** `romanticism`

**REVIEW :** `sugar_refining`, `advanced_crop_rotations`, `advanced_spinning`, `applied_mineralogy`, `mechanized_weaving`, `turnpike_road_networks`, `classical_political_economy`, `organized_elementary_schooling`, `systematic_legal_codification`, `variolation_networks`, `professional_civil_engineering`, `casemated_fortifications`, `hydrographic_surveying`

### NET — Netherlands

Les Provinces-Unies sont rehaussées dans les domaines où elles sont réellement fortes : crédit public, assurance maritime, bourse, papier, éducation locale, médecine universitaire, canaux et marine. Elles ne sont pas transformées en Grande-Bretagne industrielle : `shaft_mining` est retiré et `atmospheric_engine` demeure absent au 1er janvier, la première machine locale ne fonctionnant qu'en mars 1776. Le second pass renforce donc l'asymétrie commerce/finance/information plutôt que d'appliquer une échelle industrielle uniforme.

**Comptage :** ADD 22 · REMOVE 1 · KEEP 24 · REVIEW 16.

**ADD :** `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`, `commercial_insurance_markets`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `stock_exchange`, `advanced_crop_rotations`, `improved_agricultural_implements`, `industrial_canals`, `industrial_ceramics`, `permanent_engineer_services`, `constitutional_government`, `medical_degrees`, `organized_elementary_schooling`, `variolation_networks`

**REMOVE :** `shaft_mining`

**REVIEW :** `organized_forestry`, `sugar_refining`, `advanced_spinning`, `mechanized_weaving`, `selective_breeding`, `turnpike_road_networks`, `armament_standardization_inspection`, `marine_chronometry`, `military_topographic_surveying`, `permanent_military_hospitals`, `classical_political_economy`, `national_sovereignty`, `political_economy`, `specialized_technical_academies`, `systematic_legal_codification`, `systematic_population_registration`

### SPA — Spain

L'Espagne reçoit davantage de capacités institutionnelles qu'au premier audit : `medical_degrees`, `systematic_cadastral_surveying`, plusieurs arts manufacturiers traditionnels, arsenaux/génie et une assurance commerciale sectorielle. Le Catastro de Ensenada est particulièrement important pour le cadastre. À l'inverse, le marché boursier au sens du nœud reste absent (Madrid 1831), la vapeur de Cartagena demeure REVIEW parce que le nœud gameplay ne débloque que des pompes minières, et le coke est absent.

**Comptage :** ADD 20 · REMOVE 0 · KEEP 28 · REVIEW 15.

**ADD :** `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`, `commercial_insurance_markets`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `applied_mineralogy`, `industrial_ceramics`, `armament_standardization_inspection`, `military_topographic_surveying`, `permanent_engineer_services`, `medical_degrees`, `systematic_cadastral_surveying`, `systematic_population_registration`

**REMOVE :** —

**REVIEW :** `sugar_refining`, `institutionalized_public_credit`, `advanced_spinning`, `atmospheric_engine`, `improved_agricultural_implements`, `industrial_canals`, `mechanized_weaving`, `turnpike_road_networks`, `marine_chronometry`, `permanent_military_hospitals`, `classical_political_economy`, `organized_elementary_schooling`, `political_economy`, `systematic_legal_codification`, `variolation_networks`

### POR — Portugal

Le Portugal est l'un des plus grands changements du second pass. La réforme de Coimbra et des écoles de 1772, l'Arsenal da Marinha, la Casa dos Seguros, l'Assembleia dos Homens de Negócio de 1769 et les traces de dette publique négociée justifient des ajouts en science, enseignement, marine, assurance, bourse et crédit. Le pays reste cependant distinct de GBR : pas de mécanisation textile britannique, pas de coke et pas de vapeur minière établie.

**Comptage :** ADD 18 · REMOVE 0 · KEEP 31 · REVIEW 14.

**ADD :** `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`, `commercial_insurance_markets`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `stock_exchange`, `industrial_ceramics`, `permanent_engineer_services`, `medical_degrees`, `organized_elementary_schooling`

**REMOVE :** —

**REVIEW :** `shaft_mining`, `sugar_refining`, `advanced_spinning`, `improved_agricultural_implements`, `mechanized_weaving`, `turnpike_road_networks`, `armament_standardization_inspection`, `marine_chronometry`, `military_topographic_surveying`, `permanent_military_hospitals`, `classical_political_economy`, `political_economy`, `systematic_population_registration`, `variolation_networks`

### BEL — Belgium

Le setup `BEL` conserve le diagnostic critique du premier pass mais devient plus complet. La vapeur minière wallonne, l'agriculture flamande, l'académie bruxelloise, l'industrie des acides et les manufactures traditionnelles sont de vraies forces. `coke_smelting`, `precision_boring`, `state_dockyard_systems` et `scientific_naval_architecture` restent des sur-attributions du vieux tier. La nouvelle définition d'`organized_forestry` est traitée séparément du papier/verre/meuble. Le crédit, la bourse et l'assurance restent REVIEW au lieu d'être copiés des Provinces-Unies.

**Comptage :** ADD 13 · REMOVE 4 · KEEP 24 · REVIEW 22.

**ADD :** `industrial_acids`, `traditional_furniture_making`, `traditional_glassmaking`, `regulated_small_arms`, `codified_practical_knowledge`, `improved_agricultural_implements`, `industrial_ceramics`, `light_infantry_tactics`, `military_topographic_surveying`, `permanent_engineer_services`, `standardized_field_artillery`, `medical_degrees`, `urbanization`

**REMOVE :** `coke_smelting`, `scientific_naval_architecture`, `state_dockyard_systems`, `precision_boring`

**REVIEW :** `sugar_refining`, `enclosed_dock_systems`, `commercial_insurance_markets`, `institutionalized_public_credit`, `international_relations`, `stock_exchange`, `advanced_spinning`, `applied_mineralogy`, `industrial_canals`, `mechanized_weaving`, `selective_breeding`, `turnpike_road_networks`, `armament_standardization_inspection`, `permanent_military_hospitals`, `classical_political_economy`, `organized_elementary_schooling`, `political_economy`, `specialized_technical_academies`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `systematic_population_registration`, `variolation_networks`

### BEO — Belgium

`BEO` converge vers le même profil historique local que BEL malgré son ancien tier différent : vapeur minière sectorielle, agriculture intensive, acides, académie scientifique, papier/verre/meuble et cartographie militaire. Cette convergence est précisément l'objectif du second pass : deux TAG représentant le même espace ne doivent pas recevoir des réalités techniques opposées uniquement à cause de leur tier. Les institutions souveraines de finance/relations internationales restent toutefois ambiguës dans les Pays-Bas autrichiens.

**Comptage :** ADD 16 · REMOVE 0 · KEEP 25 · REVIEW 22.

**ADD :** `industrial_acids`, `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `scientific_fortification_siegecraft`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `advanced_crop_rotations`, `atmospheric_engine`, `improved_agricultural_implements`, `industrial_ceramics`, `military_topographic_surveying`, `permanent_engineer_services`, `medical_degrees`

**REMOVE :** —

**REVIEW :** `sugar_refining`, `enclosed_dock_systems`, `commercial_insurance_markets`, `institutionalized_public_credit`, `international_relations`, `stock_exchange`, `advanced_spinning`, `applied_mineralogy`, `industrial_canals`, `mechanized_weaving`, `selective_breeding`, `turnpike_road_networks`, `armament_standardization_inspection`, `permanent_military_hospitals`, `classical_political_economy`, `organized_elementary_schooling`, `political_economy`, `specialized_technical_academies`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `systematic_population_registration`, `variolation_networks`

### IREK — Kingdom of Ireland

L'Irlande gagne surtout des capacités locales documentées par la Dublin Society et Trinity : outils agricoles, foresterie organisée, sciences, médecine institutionnelle, variolisation et manufactures traditionnelles. Le Grand Canal est encore en chantier, donc REVIEW. Public credit, assurance et relations internationales restent prudents parce que l'existence de banques privées ou l'intégration au système britannique ne suffit pas à constituer une capacité souveraine autonome.

**Comptage :** ADD 9 · REMOVE 0 · KEEP 30 · REVIEW 24.

**ADD :** `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `periodical_print_networks`, `improved_agricultural_implements`, `medical_degrees`, `variolation_networks`

**REMOVE :** —

**REVIEW :** `sugar_refining`, `enclosed_dock_systems`, `regulated_small_arms`, `scientific_fortification_siegecraft`, `commercial_insurance_markets`, `institutionalized_public_credit`, `international_relations`, `advanced_crop_rotations`, `advanced_spinning`, `applied_mineralogy`, `atmospheric_engine`, `industrial_canals`, `industrial_ceramics`, `mechanized_weaving`, `selective_breeding`, `turnpike_road_networks`, `military_topographic_surveying`, `permanent_engineer_services`, `permanent_military_hospitals`, `classical_political_economy`, `constitutional_government`, `organized_elementary_schooling`, `political_economy`, `systematic_population_registration`

### LUX — Luxembourg

Luxembourg demeure le cas le plus spécialisé. Les fortifications et casemates sont de très haut niveau — au point que `casemated_fortifications`, pourtant C, reçoit un `CLASSIFICATION_REVIEW`. La presse est établie dès 1769. En revanche, `shaft_mining` est retiré, et les nœuds qui supposent une industrie d'armes, une diplomatie souveraine ou une université locale restent absents ou REVIEW. La présence d'une garnison impériale ne doit pas être transformée en économie nationale complète.

**Comptage :** ADD 6 · REMOVE 1 · KEEP 36 · REVIEW 21.

**ADD :** `traditional_food_processing`, `traditional_furniture_making`, `traditional_papermaking`, `scientific_fortification_siegecraft`, `periodical_print_networks`, `permanent_engineer_services`

**REMOVE :** `shaft_mining`

**REVIEW :** `organized_forestry`, `sugar_refining`, `traditional_glassmaking`, `regulated_small_arms`, `codified_practical_knowledge`, `institutionalized_scientific_exchange`, `international_relations`, `advanced_spinning`, `improved_agricultural_implements`, `industrial_ceramics`, `mechanized_weaving`, `turnpike_road_networks`, `military_topographic_surveying`, `permanent_military_hospitals`, `classical_political_economy`, `organized_elementary_schooling`, `political_economy`, `systematic_cadastral_surveying`, `systematic_legal_codification`, `systematic_population_registration`, `casemated_fortifications`

### SPC — Carlist Spain

Le TAG SPC est audité selon la capacité matérielle espagnole de 1776 et non selon le carlisme du XIXe siècle. Il converge donc largement avec SPA. Le second pass corrige une conclusion de la première passe : `commercial_insurance_markets` peut être conservé comme capacité **sectorielle** plutôt que retiré, car l'assurance maritime ibérique existe avant 1776 même si le grand marché de Cadix s'épanouit surtout après 1780. `stock_exchange` et `coke_smelting` restent en revanche à retirer.

**Comptage :** ADD 17 · REMOVE 2 · KEEP 29 · REVIEW 15.

**ADD :** `organized_forestry`, `traditional_food_processing`, `traditional_furniture_making`, `traditional_glassmaking`, `traditional_papermaking`, `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `scientific_naval_architecture`, `state_dockyard_systems`, `institutionalized_scientific_exchange`, `industrial_ceramics`, `armament_standardization_inspection`, `military_topographic_surveying`, `permanent_engineer_services`, `systematic_cadastral_surveying`, `systematic_population_registration`, `colonization`

**REMOVE :** `coke_smelting`, `stock_exchange`

**REVIEW :** `sugar_refining`, `institutionalized_public_credit`, `advanced_spinning`, `atmospheric_engine`, `improved_agricultural_implements`, `industrial_canals`, `mechanized_weaving`, `turnpike_road_networks`, `marine_chronometry`, `permanent_military_hospitals`, `classical_political_economy`, `organized_elementary_schooling`, `political_economy`, `systematic_legal_codification`, `variolation_networks`

## 15. TREE_STRUCTURE_REVIEW

**30 relations** exigent une révision de structure plutôt qu'une suppression de la capacité historique.

| TAG | Technologie | Décision | Problème |
|---|---|---|---|
| GBR | `hydraulic_cements` | REVIEW | Historically supported child despite absent/uncertain parent(s): professional_civil_engineering. Do not suppress the child merely to close the tree. |
| FRA | `advanced_crop_rotations` | REVIEW | Historically supported child despite absent/uncertain parent(s): selective_breeding. Do not suppress the child merely to close the tree. |
| FRA | `atmospheric_engine` | ADD | Historically supported child despite absent/uncertain parent(s): coke_smelting. Do not suppress the child merely to close the tree. |
| FRA | `industrial_canals` | ADD | Historically supported child despite absent/uncertain parent(s): turnpike_road_networks. Do not suppress the child merely to close the tree. |
| FRA | `professional_civil_engineering` | REVIEW | Historically supported child despite absent/uncertain parent(s): improved_road_engineering. Do not suppress the child merely to close the tree. |
| NET | `advanced_crop_rotations` | ADD | Historically supported child despite absent/uncertain parent(s): selective_breeding. Do not suppress the child merely to close the tree. |
| NET | `industrial_canals` | ADD | Historically supported child despite absent/uncertain parent(s): turnpike_road_networks. Do not suppress the child merely to close the tree. |
| SPA | `commercial_insurance_markets` | ADD | Historically supported child despite absent/uncertain parent(s): institutionalized_public_credit. Do not suppress the child merely to close the tree. |
| SPA | `atmospheric_engine` | REVIEW | Historically supported child despite absent/uncertain parent(s): coke_smelting. Do not suppress the child merely to close the tree. |
| SPA | `industrial_canals` | REVIEW | Historically supported child despite absent/uncertain parent(s): turnpike_road_networks. Do not suppress the child merely to close the tree. |
| BEL | `advanced_crop_rotations` | KEEP | Historically supported child despite absent/uncertain parent(s): selective_breeding. Do not suppress the child merely to close the tree. |
| BEL | `atmospheric_engine` | KEEP | Historically supported child despite absent/uncertain parent(s): coke_smelting. Do not suppress the child merely to close the tree. |
| BEL | `industrial_canals` | REVIEW | Historically supported child despite absent/uncertain parent(s): turnpike_road_networks. Do not suppress the child merely to close the tree. |
| BEO | `advanced_crop_rotations` | ADD | Historically supported child despite absent/uncertain parent(s): selective_breeding. Do not suppress the child merely to close the tree. |
| BEO | `atmospheric_engine` | ADD | Historically supported child despite absent/uncertain parent(s): coke_smelting. Do not suppress the child merely to close the tree. |
| BEO | `industrial_canals` | REVIEW | Historically supported child despite absent/uncertain parent(s): turnpike_road_networks. Do not suppress the child merely to close the tree. |
| IREK | `regulated_small_arms` | REVIEW | Historically supported child despite absent/uncertain parent(s): scientific_fortification_siegecraft. Do not suppress the child merely to close the tree. |
| IREK | `advanced_crop_rotations` | REVIEW | Historically supported child despite absent/uncertain parent(s): selective_breeding. Do not suppress the child merely to close the tree. |
| IREK | `industrial_canals` | REVIEW | Historically supported child despite absent/uncertain parent(s): turnpike_road_networks. Do not suppress the child merely to close the tree. |
| IREK | `light_infantry_tactics` | KEEP | Historically supported child despite absent/uncertain parent(s): regulated_small_arms. Do not suppress the child merely to close the tree. |
| IREK | `military_topographic_surveying` | REVIEW | Historically supported child despite absent/uncertain parent(s): permanent_engineer_services. Do not suppress the child merely to close the tree. |
| IREK | `permanent_engineer_services` | REVIEW | Historically supported child despite absent/uncertain parent(s): scientific_fortification_siegecraft. Do not suppress the child merely to close the tree. |
| IREK | `permanent_military_hospitals` | REVIEW | Historically supported child despite absent/uncertain parent(s): scientific_fortification_siegecraft. Do not suppress the child merely to close the tree. |
| IREK | `standardized_field_artillery` | KEEP | Historically supported child despite absent/uncertain parent(s): regulated_small_arms. Do not suppress the child merely to close the tree. |
| LUX | `industrial_ceramics` | REVIEW | Historically supported child despite absent/uncertain parent(s): traditional_glassmaking. Do not suppress the child merely to close the tree. |
| LUX | `light_infantry_tactics` | KEEP | Historically supported child despite absent/uncertain parent(s): regulated_small_arms. Do not suppress the child merely to close the tree. |
| LUX | `standardized_field_artillery` | KEEP | Historically supported child despite absent/uncertain parent(s): regulated_small_arms. Do not suppress the child merely to close the tree. |
| SPC | `commercial_insurance_markets` | KEEP | Historically supported child despite absent/uncertain parent(s): institutionalized_public_credit. Do not suppress the child merely to close the tree. |
| SPC | `atmospheric_engine` | REVIEW | Historically supported child despite absent/uncertain parent(s): coke_smelting. Do not suppress the child merely to close the tree. |
| SPC | `industrial_canals` | REVIEW | Historically supported child despite absent/uncertain parent(s): turnpike_road_networks. Do not suppress the child merely to close the tree. |

Cas structurants : `atmospheric_engine <- coke_smelting` ne fonctionne pas historiquement pour FRA/BEL/BEO ; `advanced_crop_rotations <- selective_breeding` ne doit pas bloquer les rotations flamandes ; `industrial_canals <- turnpike_road_networks` impose abusivement un chemin britannique à FRA/NET. Les anciens liens forêt→papier/verre/meuble sont volontairement exclus conformément au nouvel arbre.

## 16. CLASSIFICATION_REVIEW

`CLASSIFICATION_REVIEW` strict : **6 relations, 5 IDs uniques**.

| TAG | Technologie | Cl. actuelle | Statut historique | Motif |
|---|---|---:|---|---|
| GBR | `crystal_glass` | C | ESTABLISHED | George Ravenscroft developed lead crystal glass and operated dedicated glasshouses from 1673-1675; the C classification is much later than the capability represented by the crystal-glass PM. |
| GBR | `hydraulic_cements` | C | SECTORAL | Smeaton's Eddystone work in the 1750s used experimentally selected hydraulic lime/pozzolana mortar. The historical process predates 1776, but the node's industrial cement-work bundle is broader, so classification needs review. |
| FRA | `professional_civil_engineering` | C | ESTABLISHED | France had a permanent Corps des Ponts et Chaussées from 1716 and a dedicated engineering school from 1747. The professional civil-engineering capability predates 1776, although this C node also bundles later iron-frame/cement gameplay. |
| FRA | `casemated_fortifications` | C | ESTABLISHED | Casemated elements existed in French fortification practice before 1776, within the Vauban-era fortified system. The C date is too late for the underlying capability, while the exact reinforced naval-fortification PM remains an abstraction. |
| FRA | `hydrographic_surveying` | C | ESTABLISHED | France created the Dépôt des cartes et plans de la Marine in 1720 and had an official hydrographic charting service well before 1776. The C classification therefore deserves review. |
| LUX | `casemated_fortifications` | C | ESTABLISHED | Luxembourg's first casemates date to 1644 and were enlarged by Vauban and Austrian engineers before 1776. A C classification is plainly late for the historical capability, although the gameplay PM should still be reviewed. |

`CLASSIFICATION_TOO_EARLY` : **40 relations**, couvrant **4 technologies** : `advanced_spinning`, `classical_political_economy`, `mechanized_weaving`, `sugar_refining`.

`CLASSIFICATION_TOO_LATE` : **9 relations**, toutes sur `medical_degrees`, car la capacité est déjà institutionnalisée dans neuf TAG/espaces occidentaux.

Les C à revoir sont volontairement signalées en REVIEW et **pas silencieusement ajoutées**. Les deux `romanticism` actuels de GBR/FRA sont au contraire simplement REMOVE : leur classification C est cohérente avec leur caractère post-1776.

## 17. Principales différences avec la première passe

La première passe étudiait surtout les technologies présentes, les frontières B et quelques ajouts ciblés. Le second pass change d'échelle : les 61 A/B sont désormais explicitement évaluées pour chacun des 10 TAG.

Différences méthodologiques majeures :
- papier, verre et meuble ne dépendent plus de `organized_forestry` ;
- `organized_forestry` devient une vraie capacité de gestion/exploitation organisée ;
- médecine, finance, éducation et artisanats traditionnels sont audités systématiquement ;
- les classifications elles-mêmes sont testées contre le contenu gameplay ;
- un enfant historiquement réel n'est plus supprimé à cause d'un parent artificiel ;
- `KEEP` peut désormais signifier explicitement « correctement absent » dans la matrice exhaustive.

Parmi les relations déjà présentes dans la matrice de première passe, **14 décisions changent** :

| TAG | Technologie | Première passe | Second pass |
|---|---|---|---|
| FRA | `coke_smelting` | REVIEW | KEEP |
| NET | `shaft_mining` | KEEP | REMOVE |
| NET | `atmospheric_engine` | REVIEW | KEEP |
| NET | `specialized_technical_academies` | KEEP | REVIEW |
| POR | `shaft_mining` | KEEP | REVIEW |
| BEL | `enclosed_dock_systems` | KEEP | REVIEW |
| BEL | `international_relations` | KEEP | REVIEW |
| BEO | `international_relations` | KEEP | REVIEW |
| IREK | `regulated_small_arms` | KEEP | REVIEW |
| IREK | `international_relations` | KEEP | REVIEW |
| LUX | `shaft_mining` | KEEP | REMOVE |
| LUX | `standardized_field_artillery` | REVIEW | KEEP |
| SPC | `commercial_insurance_markets` | REMOVE | KEEP |
| SPC | `medical_degrees` | REVIEW | KEEP |

Deux changements de fond méritent d'être soulignés : SPC `commercial_insurance_markets` passe de REMOVE à KEEP/SECTORAL, car l'assurance maritime ibérique existe réellement avant 1776 même si le grand marché de Cadix est surtout post-1780 ; SPC `medical_degrees` passe de REVIEW à KEEP, car le nœud est redéfini explicitement comme formation/certification médicale institutionnelle, parfaitement pré-1776.

## 18. Recommandations finales

### 20 changements les plus importants par rapport à la distribution implémentée

| # | TAG | Technologie | Changement | Pourquoi |
|---:|---|---|---|---|
| 1 | Tous/large majorité | `traditional_papermaking` | ADD | La papeterie traditionnelle est largement pré-1776 et ne doit plus être bloquée par `organized_forestry`. |
| 2 | Tous/large majorité | `traditional_glassmaking` | ADD/REVIEW | Le verre traditionnel est largement établi ; l'ancien prérequis forestier créait des absences artificielles. |
| 3 | Tous | `traditional_furniture_making` | ADD | Le meuble artisanal/manufacturier doit être séparé de la gestion forestière rationalisée. |
| 4 | GBR/FRA/NET/SPA/POR/BEL/BEO/IREK | `medical_degrees` | ADD | Facultés/collèges et certification médicale sont déjà institutionnalisés ; classification B trop tardive. |
| 5 | FRA | `institutionalized_public_credit` | ADD | Dette publique et marché de crédit organisés bien avant 1776. |
| 6 | FRA | `stock_exchange` | ADD | Bourse de Paris légalement instituée et réglementée en 1724. |
| 7 | NET | `institutionalized_public_credit` | ADD | Le crédit public néerlandais est une force institutionnelle majeure. |
| 8 | NET | `commercial_insurance_markets` | ADD | Amsterdam est un grand marché d'assurance maritime. |
| 9 | NET | `stock_exchange` | ADD | Marché organisé des titres hérité de la VOC. |
| 10 | POR | `institutionalized_public_credit` | ADD | Dette publique/obligations et finance marchande documentées dans les années 1760. |
| 11 | POR | `commercial_insurance_markets` | ADD | Casa dos Seguros opérationnelle avant 1776 ; police connue en 1770. |
| 12 | POR | `stock_exchange` | ADD | Assembleia dos Homens de Negócio créée en 1769. |
| 13 | GBR | `coke_smelting` | ADD | Coke iron établi depuis Coalbrookdale 1709. |
| 14 | GBR | `atmospheric_engine` | ADD | Newcomen est une capacité minière établie. |
| 15 | GBR | `mechanized_spinning` | ADD | Water frame d'Arkwright attesté c.1775 ; FRONTIER. |
| 16 | GBR | `precision_boring` | ADD | Alésage Wilkinson c.1775 ; FRONTIER. |
| 17 | GBR | `ship_classification_surveying` | ADD | Lloyd's Register fondé 1760, Register Book 1764. |
| 18 | BEL | `coke_smelting / precision_boring` | REMOVE | Le vieux tier importe deux capacités britanniques non locales. |
| 19 | SPC | `coke_smelting / stock_exchange` | REMOVE | Ni coke industriel espagnol ni Bourse de Madrid en 1776. |
| 20 | SPA/SPC | `systematic_cadastral_surveying` | ADD | Le Catastro de Ensenada fournit une preuve directe d'un cadastre systématique pré-1776. |

### Contrôle final

- Nombre de TAG : **10**
- Technologies A auditées : **25** (250 relations TAG×tech)
- Technologies B auditées : **36** (360 relations TAG×tech)
- Lignes totales : **638**
- ADD : **184**
- REMOVE : **10**
- KEEP : **273**
- REVIEW : **171**
- TREE_STRUCTURE_REVIEW : **30**
- CLASSIFICATION_REVIEW : **6 relations** (5 technologies C distinctes)
- CLASSIFICATION_TOO_EARLY : **40 relations**
- CLASSIFICATION_TOO_LATE : **9 relations**
- Fichiers gameplay modifiés : **0**
- Code Victoria 3 produit : **0**
- Commit/push : **0**

La matrice CSV constitue l'autorité détaillée de ce second pass : une ligne pour chaque relation A/B obligatoire, plus les E/C effectivement auditées.
