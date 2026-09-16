# Recherche technologique — Europe occidentale — 1er janvier 1776

> **Recherche historique uniquement.** Aucun fichier du mod n'est modifié et aucun code Victoria 3 n'est produit.

## 1. Périmètre

Le CSV pays fournit directement **BEL, BEO, FRA, GBR, IREK, LUX, NET** en `Western Europe`. La consigne régionale ajoute les TAG ibériques **SPA, POR, SPC**. Total : **10 TAG**.

| TAG | Pays | Sous-région | Tier actuel | Action |
|---|---|---|---|---|
| GBR | Great Britain | British Isles | `tier_4` | `KEEP_TIER` |
| FRA | France | France | `tier_4` | `KEEP_TIER` |
| NET | Netherlands | Northern Low Countries | `tier_4` | `KEEP_TIER` |
| SPA | Spain | Iberia | `tier_4` | `KEEP_TIER` |
| POR | Portugal | Iberia | `tier_4` | `KEEP_TIER` |
| BEL | Belgium | Southern Low Countries | `tier_1` | `CHANGE_TIER` → `tier_4` |
| BEO | Belgium | Southern Low Countries | `tier_4` | `KEEP_TIER` |
| IREK | Kingdom of Ireland | British Isles | `tier_4` | `KEEP_TIER` |
| LUX | Luxembourg | Luxembourg | `tier_4` | `REPLACE_WITH_EXPLICIT_SETUP` |
| SPC | Carlist Spain | Iberia | `tier_3` | `CHANGE_TIER` → `tier_4` |

`BEL` et `BEO` sont traités séparément. `SPC` est inclus parce qu'il s'agit d'un TAG espagnol du CSV, mais aucune innovation carliste du XIXe siècle n'est rétroprojetée en 1776. Les possessions coloniales hors d'Europe à TAG propre restent exclues.

## 2. Méthode et sources

Toutes les technologies actuellement possédées par les dix TAG ont reçu une décision. Les ajouts et reviews ciblent les technologies frontière, les institutions majeures absentes du tier, et les cas où le gameplay du nœud ne correspond pas exactement au secteur historique. Une technologie postérieure au **1er janvier 1776** n'est pas antidatée.

La matrice CSV contient les URL complètes des sources pour chaque décision. Références structurantes :
- Newcomen britannique: https://collection.sciencemuseumgroup.org.uk/objects/co50900/newcomen-atmospheric-engine
- Wilkinson c.1775: https://collection.sciencemuseumgroup.org.uk/objects/co46448/cast-iron-boring-bar-and-boring-head
- coke Coalbrookdale: https://historicengland.org.uk/campaigns/100-places/industry-trade-commerce/
- Arkwright 1775: https://collection.sciencemuseumgroup.org.uk/objects/co44832/arkwrights-water-frame-1775-spinning-machine
- turnpikes: https://www.parliament.uk/about/living-heritage/transformingsociety/transportcomms/roadsrail/overview/turnpikestolls/
- Royal Dockyards: https://www.rmg.co.uk/stories/maritime-history/royal-naval-dockyards
- Ponts et Chaussées: https://ecoledesponts.fr/lecole/bienvenue-lecole/lecole-dans-lhistoire
- Académie des sciences: https://www.academie-sciences.fr/lhistoire-de-lacademie
- pompes Newcomen françaises: https://cnum.cnam.fr/pgi/redir.php?ident=M14066&onglet=c
- première fonte au coke française 1785: https://www.creusotmontceautourisme.com/discover/le-creusot/a-factory-town-turned-empire/from-royal-foundry-to-english-forge/
- Amsterdam et ses canaux: https://whc.unesco.org/en/list/1349
- première vapeur néerlandaise: https://www.dbnl.org/tekst/lint011gesc04_01/lint011gesc04_01_0005.php
- arsenal d'Amsterdam: https://www.hetscheepvaartmuseum.nl/over-ons/het-gebouw
- arsenaux espagnols: https://cvc.cervantes.es/actcult/museo_naval/patio_central/caracteristicas/
- Segovia 1764: https://ejercito.defensa.gob.es/unidades/Segovia/acart/Noticias/2019/059.html
- Coimbra 1772: https://www.uc.pt/org/historia_ciencia_na_uc/Textos/ocontexto/2_acriacao
- Arsenal da Marinha: https://www.marinha.pt/Conteudos_Externos/Revista_Armada/2014/484/files/basic-html/page13.html
- Jemeppe 1721: https://connaitrelawallonie.wallonie.be/histoire/timeline/18-janvier-1721-installation-de-la-toute-premiere-pompe-feu-du-continent-jemeppe
- coke belge vers 1820: https://www.industriemuseum.be/nl/collectie-item/geschiedenis-van-hoogovens
- agriculture flamande: https://www.cambridge.org/core/journals/annales-histoire-sciences-sociales/article/abs/les-campagnes-flamandes-du-xiiie-siecle-au-xviiie-siecle-ou-les-succes-dune-agriculture-traditionnelle/15A2A299629F9C8BC5877BDFAB733E5C
- Dublin Society: https://www.rds.ie/about-rds/governance/rds-history
- Grand Canal irlandais: https://archive.waterwaysireland.org/history-of-the-waterways/9/the-history-of-the-grand-canal
- forteresse de Luxembourg: https://whc.unesco.org/en/list/699
- presse luxembourgeoise: https://bnl.public.lu/en/a-la-une/a-la-loupe/2024/feller.html

## 3. Diagnostic régional

La Grande-Bretagne domine un ensemble étroit mais décisif de techniques industrielles : coke, diffusion de la machine atmosphérique, premières machines de filature, alésage de précision, turnpikes et canal age. Cette avance ne doit **pas** devenir une supériorité artificielle dans toutes les catégories.

La France est exceptionnellement forte dans l'ingénierie d'État, l'artillerie, les arsenaux et les institutions scientifiques. Les Provinces-Unies sont particulièrement fortes en crédit, assurance, marché de titres, réseaux commerciaux, canaux et infrastructures maritimes. L'Espagne et le Portugal conservent des capacités navales et techniques substantielles malgré une industrialisation mécanique plus lente.

Les Pays-Bas méridionaux combinent agriculture flamande avancée et vapeur minière précoce avec une sidérurgie encore au charbon de bois. L'Irlande possède un mécanisme local de diffusion des innovations autour de la Dublin Society. Luxembourg est d'abord un pôle de fortification.

## 4. Analyse pays par pays

### GBR — Great Britain

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `specialized_technical_academies`, `colonization`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `distillation`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `international_relations`, `codified_practical_knowledge`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `scientific_naval_architecture`, `coke_smelting`, `atmospheric_engine`, `improved_agricultural_implements`, `turnpike_road_networks`, `advanced_crop_rotations`, `industrial_canals`, `mechanized_spinning`, `selective_breeding`, `precision_boring`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `commercial_insurance_markets`, `stock_exchange`
- **Technologies à REMOVE:** `romanticism`
- **Technologies à REVIEW:** —
- **Frontière/sectoriel:** `light_infantry_tactics`, `standardized_field_artillery`, `improved_agricultural_implements`, `advanced_crop_rotations`, `industrial_canals`, `mechanized_spinning`, `selective_breeding`, `precision_boring`
- **Prérequis problématiques:**
  - `specialized_technical_academies` : Add institutionalized_scientific_exchange.
  - `colonization` : Parent international_relations is present.
  - `romanticism` : Remove the child rather than adding parents for tree completeness.
  - `regulated_small_arms` : Add scientific_fortification_siegecraft.
  - `scientific_naval_architecture` : Parent state_dockyard_systems is justified.
  - `atmospheric_engine` : shaft_mining and coke_smelting are independently justified.
  - `advanced_crop_rotations` : selective_breeding is also justified, though historically the processes are separable.
  - `industrial_canals` : turnpike_road_networks is also justified.
  - `precision_boring` : coke_smelting and atmospheric_engine are independently justified.
  - `commercial_insurance_markets` : Parent institutionalized_public_credit should be added.
  - `stock_exchange` : Parent institutionalized_public_credit should be added.
- **Justification historique:**
La Grande-Bretagne est le seul pays du périmètre pour lequel plusieurs technologies de la première révolution industrielle doivent être ajoutées simultanément, mais elles n'ont pas le même statut. `coke_smelting` et `atmospheric_engine` sont établies; `precision_boring` et `mechanized_spinning` sont des **frontières datées presque exactement de 1775**. Wilkinson construit son aléseuse à Bersham vers 1775, et le water frame d'Arkwright est attesté à Cromford en 1775. Ces deux nœuds doivent donc exister au départ, sans transformer cette avance en supériorité automatique dans toutes les catégories.

Les turnpikes couvrent plus de 11 500 miles après la vague de 1751-1772 et Bridgewater/Brindley ont déjà lancé l'âge des canaux. En agriculture, rotations, outils et élevage sélectif restent sectoriels/frontière. En parallèle, Royal Society, Royal Dockyards, Banque d'Angleterre et marché londonien des titres sont des institutions déjà solidement établies.
- **Sources:**
  - https://royalsociety.org/about-us/who-we-are/history/
  - https://www.royalsociety.org/journals/publishing-activities/publishing350/history-philosophical-transactions/
  - https://www.rmg.co.uk/stories/maritime-history/royal-naval-dockyards
  - https://histoiredesarts.culture.gouv.fr/Mouvements-artistiques/Le-romantisme
  - https://histoiredesarts.culture.gouv.fr/Fiches-reperes/Litterature
  - https://historicengland.org.uk/campaigns/100-places/industry-trade-commerce/
  - https://collection.sciencemuseumgroup.org.uk/objects/co50900/newcomen-atmospheric-engine
  - https://collection.sciencemuseumgroup.org.uk/objects/co46448/cast-iron-boring-bar-and-boring-head
  - https://academic.oup.com/book/25883/chapter-abstract/193573082
  - https://www.ans.iastate.edu/about/history/people/robert-bakewell
- **Confiance générale:** HIGH

### FRA — France

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `traditional_food_processing`, `specialized_technical_academies`, `systematic_population_registration`, `colonization`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `distillation`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `international_relations`, `codified_practical_knowledge`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `scientific_naval_architecture`, `permanent_engineer_services`, `atmospheric_engine`, `industrial_canals`, `institutionalized_scientific_exchange`, `periodical_print_networks`
- **Technologies à REMOVE:** `romanticism`
- **Technologies à REVIEW:** `coke_smelting`, `turnpike_road_networks`
- **Frontière/sectoriel:** `light_infantry_tactics`, `standardized_field_artillery`, `enclosed_dock_systems`, `atmospheric_engine`
- **Prérequis problématiques:**
  - `specialized_technical_academies` : Add institutionalized_scientific_exchange.
  - `systematic_population_registration` : Parent systematic_administrative_statistics is present.
  - `colonization` : Parent international_relations is present.
  - `romanticism` : Remove rather than repair parents.
  - `regulated_small_arms` : Add scientific_fortification_siegecraft.
  - `scientific_fortification_siegecraft` : Repairs regulated_small_arms.
  - `scientific_naval_architecture` : Parent state_dockyard_systems should be added.
  - `permanent_engineer_services` : Parent scientific_fortification_siegecraft should be added.
  - `coke_smelting` : Keep absent; tolerate the prerequisite mismatch.
  - `atmospheric_engine` : Tree mismatch: coke_smelting is historically absent in 1776; do not add it just to satisfy the parent.
  - `industrial_canals` : Do not auto-add turnpike_road_networks if interpreted literally; French canal engineering followed another institutional path.
- **Justification historique:**
La France ne doit pas être copiée sur le modèle britannique. Son avantage comparatif se situe dans la **capacité étatique organisée** : Corps des Ponts et Chaussées, école d'ingénieurs, Académie des sciences, génie militaire, arsenaux et système Gribeauval. Le Canal du Midi prouve une capacité de génie hydraulique de très haut niveau bien avant le canal industriel britannique.

La vapeur existe réellement dans certains bassins miniers dès les années 1730 mais sa diffusion est bien plus limitée qu'en Grande-Bretagne. Surtout, la fonte au coke n'est pas encore une capacité française : la première fonte au coke du Creusot date de 1785. Le prérequis `atmospheric_engine <- coke_smelting` doit donc être toléré comme abstraction. `romanticism` doit être retiré.
- **Sources:**
  - https://ecoledesponts.fr/lecole/bienvenue-lecole/lecole-dans-lhistoire
  - https://www.academie-sciences.fr/lhistoire-de-lacademie
  - https://www.terre.defense.gouv.fr/ecole-du-genie/lecole/presentation-lecole-du-genie
  - https://www.archivespasdecalais.fr/Chercher/Fonds-et-collections/Archives-de-l-etat-civil/Historique-de-la-production
  - https://histoiredesarts.culture.gouv.fr/Mouvements-artistiques/Le-romantisme
  - https://histoiredesarts.culture.gouv.fr/Fiches-reperes/Litterature
  - https://www.musee-armee.fr/collections/explorer-les-collections/portofolios/le-systeme-gribeauval.html
  - https://www.musee-marine.fr/en/collections/toulon/dry-dock-no1-in-toulon-1774-1778.html
  - https://www.musee-marine.fr/nos-musees/brest/collections/oeuvres-phares/la-bretagne.html
  - https://www.servicehistorique.sga.defense.gouv.fr/en/node/32598
- **Confiance générale:** HIGH

### NET — Netherlands

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `specialized_technical_academies`, `colonization`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `distillation`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `international_relations`, `codified_practical_knowledge`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `enclosed_dock_systems`, `state_dockyard_systems`, `scientific_naval_architecture`, `traditional_papermaking`, `industrial_canals`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `commercial_insurance_markets`, `stock_exchange`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `atmospheric_engine`
- **Frontière/sectoriel:** `light_infantry_tactics`, `standardized_field_artillery`
- **Prérequis problématiques:**
  - `specialized_technical_academies` : Add institutionalized_scientific_exchange.
  - `colonization` : Parent international_relations is present.
  - `scientific_naval_architecture` : Parent state_dockyard_systems should be added.
  - `atmospheric_engine` : Do not add at the strict cutoff.
  - `industrial_canals` : Do not auto-add turnpike_road_networks; the Dutch transport path was water-centric.
  - `commercial_insurance_markets` : Parent institutionalized_public_credit should be added.
  - `stock_exchange` : Parent institutionalized_public_credit should be added.
- **Justification historique:**
Les Provinces-Unies sont surtout **commerciales, financières, maritimes, hydrauliques et informationnelles** : crédit public, assurance maritime, marché de titres, imprimerie, canaux, infrastructures portuaires et amirautés. Elles ne doivent pas recevoir automatiquement les nouvelles techniques industrielles britanniques.

La première machine atmosphérique néerlandaise est un cas de cutoff strict : commandée plus tôt et arrivée en janvier 1775, elle n'est assemblée et mise en marche que le 9 mars 1776. `atmospheric_engine` reste donc REVIEW/ABSENT au 1er janvier. `industrial_canals` est ajouté seulement dans une lecture fonctionnelle des voies navigables artificielles à forte capacité.
- **Sources:**
  - https://whc.unesco.org/en/list/1349
  - https://www.hetscheepvaartmuseum.nl/over-ons/het-gebouw
  - https://www.zaans.nl/en/industrial-culture/mills
  - https://www.dbnl.org/tekst/lint011gesc04_01/lint011gesc04_01_0005.php
  - https://collection.sciencemuseumgroup.org.uk/objects/co50900/newcomen-atmospheric-engine
  - https://intellectualhistory.site.ox.ac.uk/article/parliamentary-culture-and-public-credit-how-merchants-overcame-their-weak-position
  - https://www.worldsfirststockexchange.com/
  - https://books.google.com/books/about/Marine_Insurance_in_the_Netherlands_1600.html?id=KPihRWh7BlUC
- **Confiance générale:** HIGH

### SPA — Spain

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `specialized_technical_academies`, `colonization`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `distillation`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `international_relations`, `codified_practical_knowledge`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `scientific_naval_architecture`, `permanent_engineer_services`, `applied_mineralogy`, `institutionalized_scientific_exchange`, `periodical_print_networks`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `atmospheric_engine`, `industrial_canals`
- **Frontière/sectoriel:** `light_infantry_tactics`, `standardized_field_artillery`, `atmospheric_engine`, `applied_mineralogy`, `industrial_canals`, `institutionalized_scientific_exchange`
- **Prérequis problématiques:**
  - `specialized_technical_academies` : Add institutionalized_scientific_exchange.
  - `colonization` : Parent international_relations is present.
  - `regulated_small_arms` : Add scientific_fortification_siegecraft.
  - `scientific_fortification_siegecraft` : Repairs regulated_small_arms.
  - `scientific_naval_architecture` : Parent state_dockyard_systems should be added.
  - `permanent_engineer_services` : Parent scientific_fortification_siegecraft should be added.
  - `atmospheric_engine` : Do not add coke_smelting; Spanish coke smelting was not established in 1776.
  - `applied_mineralogy` : Parent shaft_mining is present.
  - `industrial_canals` : Do not auto-add turnpike_road_networks.
- **Justification historique:**
L'Espagne de 1776 est moins avancée que la Grande-Bretagne dans le coke et la mécanisation, mais possède des capacités de premier ordre dans **les arsenaux, la construction navale, l'artillerie et le génie militaire**. Ferrol, Cartagena et La Carraca forment un système d'arsenaux d'État majeur; le Real Colegio de Artillería fonctionne depuis 1764.

La pompe de Cartagena prouve une capacité locale de vapeur avant 1776, mais le nœud du mod débloque exclusivement des pompes de mines : `atmospheric_engine` reste REVIEW. Le Canal de Castilla est encore en chantier, donc `industrial_canals` reste FRONTIER/REVIEW.
- **Sources:**
  - https://ejercito.defensa.gob.es/unidades/Segovia/acart/Noticias/2019/059.html
  - https://cvc.cervantes.es/actcult/museo_naval/patio_central/caracteristicas/
  - https://ejercito.defensa.gob.es/noticias/2020/04/7935_aniversario_ingenieros.html
  - https://www.rtve.es/play/audios/a-hombros-de-gigantes/palabra-ingeniero-primera-maquina-vapor-espana-05-10-21/6125838/
  - https://canalcastilla.es/
  - https://www.bne.es/es/blog/blog-bne/un-romano-un-escribano-con-malas-pulgas-y-la-tinta-que-usaba-el-rey-de-inglaterra
- **Confiance générale:** HIGH

### POR — Portugal

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `specialized_technical_academies`, `colonization`, `systematic_legal_codification`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `distillation`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `international_relations`, `codified_practical_knowledge`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `scientific_naval_architecture`, `institutionalized_scientific_exchange`, `periodical_print_networks`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** —
- **Frontière/sectoriel:** `light_infantry_tactics`, `standardized_field_artillery`, `enclosed_dock_systems`
- **Prérequis problématiques:**
  - `specialized_technical_academies` : Add institutionalized_scientific_exchange.
  - `colonization` : Parent international_relations is present.
  - `systematic_legal_codification` : Parent systematic_administrative_statistics is present.
  - `regulated_small_arms` : Add scientific_fortification_siegecraft.
  - `scientific_fortification_siegecraft` : Repairs regulated_small_arms.
  - `scientific_naval_architecture` : Parent state_dockyard_systems should be added.
- **Justification historique:**
Le Portugal combine un appareil maritime ancien et une modernisation scientifique très récente. Après 1755, la Ribeira das Naus est reconstruite et l'ensemble est désigné Arsenal da Marinha en 1774; des vaisseaux y sont construits avant le cutoff.

La réforme de Coimbra de **1772** est déterminante : facultés de Mathématiques et de Philosophie naturelle, laboratoire chimique, cabinet de physique expérimentale, jardin botanique et musée d'histoire naturelle. Elle justifie `institutionalized_scientific_exchange` et le maintien de `specialized_technical_academies`. La codification juridique est également défendable.
- **Sources:**
  - https://www.uc.pt/org/historia_ciencia_na_uc/Textos/ocontexto/2_acriacao
  - https://www.uc.pt/org/historia_ciencia_na_uc/Textos/oinstituto/matematica
  - https://www.marinha.pt/Conteudos_Externos/Revista_Armada/2014/484/files/basic-html/page13.html
  - https://bibliotecas.justica.gov.pt/bib/5144
  - https://whc.unesco.org/en/list/1367
  - https://academia.marinha.pt/pt/edicoes/historiadamarinha/HistoriaMarinhaPortuguesa_1669-1823.pdf
  - https://arquivohistorico.marinha.pt/details?id=6607
  - https://imprensanacional.pt/history/diario-do-governo/
- **Confiance générale:** HIGH

### BEL — Belgium

- **Current tier:** `tier_1`
- **Tier action:** `CHANGE_TIER` → `tier_4`
- **Technologies à KEEP:** `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `distillation`, `improved_husbandry`, `organized_forestry`, `organized_textile_production`, `shaft_mining`, `traditional_food_processing`, `traditional_papermaking`, `atmospheric_engine`, `advanced_crop_rotations`, `institutionalized_scientific_exchange`, `international_relations`, `periodical_print_networks`, `systematic_administrative_statistics`
- **Technologies à ADD:** `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `codified_practical_knowledge`, `urbanization`
- **Technologies à REMOVE:** `state_dockyard_systems`, `scientific_naval_architecture`, `coke_smelting`, `precision_boring`
- **Technologies à REVIEW:** `institutionalized_public_credit`, `commercial_insurance_markets`, `stock_exchange`
- **Frontière/sectoriel:** `enclosed_dock_systems`, `atmospheric_engine`, `commercial_insurance_markets`, `stock_exchange`
- **Prérequis problématiques:**
  - `scientific_naval_architecture` : Parent state_dockyard_systems is also removed.
  - `coke_smelting` : Remove rather than preserving it as atmospheric_engine prerequisite.
  - `atmospheric_engine` : Tree mismatch: coke_smelting should be removed even though listed as a parent.
  - `advanced_crop_rotations` : Do not auto-add selective_breeding; crop rotation had an independent path.
  - `precision_boring` : Do not preserve merely because atmospheric_engine is retained.
  - `commercial_insurance_markets` : Parent institutionalized_public_credit is itself under review.
  - `stock_exchange` : Parent institutionalized_public_credit is under review.
  - `regulated_small_arms` : scientific_fortification_siegecraft is retained.
  - `codified_practical_knowledge` : periodical_print_networks and institutionalized_scientific_exchange are retained.
- **Justification historique:**
`BEL` est le setup le plus problématique. Le `tier_1` mélange des capacités réellement locales avec des technologies britanniques importées par le tier. La **machine atmosphérique** est bien réelle : Jemeppe fonctionne en 1721 et le bassin wallon devient un foyer continental de Newcomen. L'agriculture flamande justifie aussi `advanced_crop_rotations`.

En revanche, la fonte au coke et l'alésage de précision ne sont pas des capacités locales en 1776 : le premier haut fourneau moderne au coke belge date d'environ 1820. Les grands nœuds d'arsenal d'État et d'architecture navale sont également trop forts. Recommandation : **tier_1 → tier_4**, puis réajouts explicites des capacités locales.
- **Sources:**
  - https://whc.unesco.org/en/list/1349
  - https://council.science/member/belgium-royal-academies-for-science-and-the-arts-of-belgium-rasab/
  - https://whc.unesco.org/en/list/699
  - https://www.hetscheepvaartmuseum.nl/over-ons/het-gebouw
  - https://www.industriemuseum.be/nl/collectie-item/geschiedenis-van-hoogovens
  - https://connaitrelawallonie.wallonie.be/histoire/timeline/18-janvier-1721-installation-de-la-toute-premiere-pompe-feu-du-continent-jemeppe
  - https://www.cambridge.org/core/journals/annales-histoire-sciences-sociales/article/abs/les-campagnes-flamandes-du-xiiie-siecle-au-xviiie-siecle-ou-les-succes-dune-agriculture-traditionnelle/15A2A299629F9C8BC5877BDFAB733E5C
  - https://collection.sciencemuseumgroup.org.uk/objects/co50900/newcomen-atmospheric-engine
  - https://researchportal.unamur.be/en/publications/diffusion-et-application-des-m%C3%A9thodes-culturales-flamandes-dans-l
  - https://collection.sciencemuseumgroup.org.uk/objects/co46448/cast-iron-boring-bar-and-boring-head
- **Confiance générale:** HIGH

### BEO — Belgium

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `distillation`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `international_relations`, `codified_practical_knowledge`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `atmospheric_engine`, `advanced_crop_rotations`, `institutionalized_scientific_exchange`, `periodical_print_networks`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `specialized_technical_academies`, `systematic_legal_codification`
- **Frontière/sectoriel:** `specialized_technical_academies`, `light_infantry_tactics`, `standardized_field_artillery`, `atmospheric_engine`
- **Prérequis problématiques:**
  - `specialized_technical_academies` : If retained, add institutionalized_scientific_exchange.
  - `systematic_legal_codification` : Parent systematic_administrative_statistics is present.
  - `regulated_small_arms` : Add scientific_fortification_siegecraft.
  - `scientific_fortification_siegecraft` : Repairs regulated_small_arms.
  - `atmospheric_engine` : Do not add coke_smelting merely to satisfy the parent.
  - `advanced_crop_rotations` : Do not auto-add selective_breeding.
- **Justification historique:**
`BEO` est beaucoup plus raisonnable car il part du tier_4. Il faut lui réinjecter les spécialités réelles des Pays-Bas méridionaux : vapeur minière de Newcomen, agriculture flamande intensive, fortification et réseaux savants/imprimés. `specialized_technical_academies` et `systematic_legal_codification` restent en REVIEW car leurs effets gameplay sont plus larges que les institutions locales clairement attestées.
- **Sources:**
  - https://council.science/member/belgium-royal-academies-for-science-and-the-arts-of-belgium-rasab/
  - https://researchportal.unamur.be/en/publications/diffusion-et-application-des-m%C3%A9thodes-culturales-flamandes-dans-l
  - https://whc.unesco.org/en/list/699
  - https://www.cambridge.org/core/journals/annales-histoire-sciences-sociales/article/abs/les-campagnes-flamandes-du-xiiie-siecle-au-xviiie-siecle-ou-les-succes-dune-agriculture-traditionnelle/15A2A299629F9C8BC5877BDFAB733E5C
  - https://connaitrelawallonie.wallonie.be/histoire/timeline/18-janvier-1721-installation-de-la-toute-premiere-pompe-feu-du-continent-jemeppe
  - https://collection.sciencemuseumgroup.org.uk/objects/co50900/newcomen-atmospheric-engine
  - https://whc.unesco.org/en/list/1349
- **Confiance générale:** HIGH

### IREK — Kingdom of Ireland

- **Current tier:** `tier_4`
- **Tier action:** `KEEP_TIER`
- **Technologies à KEEP:** `institutionalized_scientific_exchange`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `distillation`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `international_relations`, `codified_practical_knowledge`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `organized_forestry`, `improved_agricultural_implements`, `periodical_print_networks`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `industrial_canals`
- **Frontière/sectoriel:** `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `improved_agricultural_implements`, `industrial_canals`
- **Prérequis problématiques:**
  - `institutionalized_scientific_exchange` : Add periodical_print_networks.
  - `regulated_small_arms` : Do not auto-add scientific_fortification_siegecraft solely for tree completion.
  - `codified_practical_knowledge` : periodical_print_networks should be added alongside the existing scientific-exchange parent.
  - `improved_agricultural_implements` : Parent improved_husbandry is present.
  - `industrial_canals` : Do not auto-add turnpike_road_networks.
- **Justification historique:**
Le Royaume d'Irlande ne doit pas être traité comme une simple copie de la Grande-Bretagne. La Dublin Society, fondée en 1731, fournit un ancrage local très fort : agriculture, industrie, manufacture, arts, sciences, publications, primes et démonstrations d'outils. Cela justifie la presse périodique, les outils agricoles améliorés et même une forme d'organisation forestière.

Le Grand Canal est toutefois encore en chantier : travaux dès 1756 et première écluse urbaine en 1773, mais premier service de passage seulement en 1780. `industrial_canals` reste REVIEW.
- **Sources:**
  - https://digitalarchive.rds.ie/exhibits/show/artcollection/originsandobjectives
  - https://www.rds.ie/about-rds/governance/rds-history
  - https://www.rmg.co.uk/stories/maritime-history/royal-naval-dockyards
  - https://digitalarchive.rds.ie/exhibits/show/rdsshows/intro1
  - https://archive.waterwaysireland.org/history-of-the-waterways/9/the-history-of-the-grand-canal
  - https://catalogue.nli.ie/Record/vtls000829693
- **Confiance générale:** HIGH

### LUX — Luxembourg

- **Current tier:** `tier_4`
- **Tier action:** `REPLACE_WITH_EXPLICIT_SETUP`
- **Technologies à KEEP:** `light_infantry_tactics`, `distillation`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `systematic_administrative_statistics`, `urbanization`
- **Technologies à ADD:** `scientific_fortification_siegecraft`, `periodical_print_networks`
- **Technologies à REMOVE:** —
- **Technologies à REVIEW:** `regulated_small_arms`, `standardized_field_artillery`, `international_relations`, `codified_practical_knowledge`, `institutionalized_scientific_exchange`
- **Frontière/sectoriel:** `light_infantry_tactics`, `standardized_field_artillery`
- **Prérequis problématiques:**
  - `regulated_small_arms` : Add scientific_fortification_siegecraft; do not infer arms industry automatically.
  - `codified_practical_knowledge` : Missing institutionalized_scientific_exchange remains unresolved.
- **Justification historique:**
Luxembourg a un profil **extrêmement spécialisé**. Sa forteresse est l'une des plus importantes d'Europe et les Autrichiens poursuivent pendant plus de quarante ans les ouvrages, forts et casemates. `scientific_fortification_siegecraft` doit être ajouté avec confiance élevée.

En revanche, artillerie et garnison ne prouvent ni une industrie locale d'armes ni une diplomatie souveraine. Plusieurs nœuds du tier_4 sont donc REVIEW. La presse est bien attestée localement dès 1769/1773. Le meilleur choix est `REPLACE_WITH_EXPLICIT_SETUP`.
- **Sources:**
  - https://whc.unesco.org/en/list/699
  - https://whc.unesco.org/archive/advisory_body_evaluation/699.pdf
  - https://bnl.public.lu/en/a-la-une/a-la-loupe/2024/feller.html
- **Confiance générale:** HIGH

### SPC — Carlist Spain

- **Current tier:** `tier_3`
- **Tier action:** `CHANGE_TIER` → `tier_4`
- **Technologies à KEEP:** `periodical_print_networks`, `regulated_small_arms`, `light_infantry_tactics`, `standardized_field_artillery`, `distillation`, `improved_husbandry`, `organized_textile_production`, `shaft_mining`, `applied_mineralogy`, `international_relations`, `codified_practical_knowledge`, `systematic_administrative_statistics`, `specialized_technical_academies`, `urbanization`
- **Technologies à ADD:** `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `scientific_naval_architecture`, `permanent_engineer_services`, `institutionalized_scientific_exchange`
- **Technologies à REMOVE:** `stock_exchange`, `coke_smelting`, `commercial_insurance_markets`
- **Technologies à REVIEW:** `atmospheric_engine`, `medical_degrees`
- **Frontière/sectoriel:** `atmospheric_engine`, `light_infantry_tactics`, `standardized_field_artillery`, `applied_mineralogy`, `institutionalized_scientific_exchange`
- **Prérequis problématiques:**
  - `atmospheric_engine` : Do not add coke_smelting; tolerate or redesign the prerequisite later.
  - `stock_exchange` : Do not add institutionalized_public_credit merely to satisfy the parent.
  - `coke_smelting` : Remove rather than maintaining an ahistorical prerequisite chain.
  - `applied_mineralogy` : After tier change, keep explicitly; shaft_mining remains available.
  - `commercial_insurance_markets` : Do not add public credit mechanically.
  - `medical_degrees` : If retained after tier change, institutionalized_scientific_exchange should also be present.
  - `specialized_technical_academies` : After tier change, preserve explicitly; add institutionalized_scientific_exchange.
  - `scientific_fortification_siegecraft` : Repairs regulated_small_arms.
  - `scientific_naval_architecture` : Parent state_dockyard_systems should be added.
  - `permanent_engineer_services` : Parent scientific_fortification_siegecraft should be added.
  - `institutionalized_scientific_exchange` : Supports specialized_technical_academies and, if retained, medical_degrees.
- **Justification historique:**
`SPC` est politiquement anachronique comme «Carlist Spain», mais doit être évalué selon la **réalité matérielle espagnole de 1776**. Son tier_3 lui donne trop : `coke_smelting`, assurance commerciale large, etc., et `stock_exchange` est explicite alors que la Bourse de Madrid date de 1831.

La solution la plus propre est **tier_3 → tier_4**, puis conservation/ajout explicite des capacités espagnoles réellement fortes : Segovia, génie, arsenaux, architecture navale, presse et minéralogie. `atmospheric_engine` reste REVIEW à cause du décalage entre la pompe de Cartagena et les PM de mines du nœud.
- **Sources:**
  - https://www.rtve.es/play/audios/a-hombros-de-gigantes/palabra-ingeniero-primera-maquina-vapor-espana-05-10-21/6125838/
  - https://cvc.cervantes.es/actcult/museo_naval/patio_central/caracteristicas/
  - https://www.bne.es/es/blog/blog-bne/un-romano-un-escribano-con-malas-pulgas-y-la-tinta-que-usaba-el-rey-de-inglaterra
  - https://ejercito.defensa.gob.es/unidades/Segovia/acart/Noticias/2019/059.html
  - https://www.bolsasymercados.es/en/bme-exchange/madrid-stock-exchange/history.html
  - https://hispania.revistas.csic.es/index.php/hispania/article/view/625
  - https://portalinvestigacion.uniovi.es/documentos/64a84f6a258a1f326c226a14
  - https://ejercito.defensa.gob.es/noticias/2020/04/7935_aniversario_ingenieros.html
- **Confiance générale:** HIGH

## 5. Comparaison régionale

**Industrie et vapeur.** GBR est clairement devant pour le couple coke–vapeur et atteint en 1775 l'alésage de précision et la filature mécanisée. FRA et les Pays-Bas méridionaux utilisent des Newcomen sans disposer d'une filière au coke comparable. NET n'a pas encore de machine opérationnelle au cutoff strict. L'Espagne a un cas ponctuel à Cartagena, hors secteur minier.

**Finance.** NET doit être au sommet régional avec GBR pour le crédit public, l'assurance et le marché de titres. Ces nœuds ne doivent pas être transférés automatiquement à BEL/BEO sous prétexte d'appartenance aux anciens Pays-Bas.

**Génie/science.** FRA possède un appareil d'ingénieurs d'État particulièrement structuré; SPA dispose d'écoles militaires et d'arsenaux de très haut niveau; POR connaît une réforme scientifique majeure en 1772.

**Agriculture.** Les innovations britanniques (Bakewell, outils, rotations) ne sont pas la seule trajectoire. La Flandre possède une agriculture intensive et des rotations avancées propres; l'Irlande diffuse localement outils et pratiques via la Dublin Society.

## 6. Technologies frontière 1776

| Technologie | GBR | FRA | NET | SPA/SPC | POR | BEL/BEO | IREK |
|---|---|---|---|---|---|---|---|
| `atmospheric_engine` | ADD établi | ADD sectoriel | REVIEW, mise en marche 09-03-1776 | REVIEW, Cartagena mais mauvais secteur gameplay | — | KEEP/ADD mines wallonnes | — |
| `precision_boring` | ADD frontier c.1775 | — | — | — | — | REMOVE BEL | — |
| `mechanized_spinning` | ADD frontier 1775 | — | — | — | — | — | — |
| `industrial_canals` | ADD frontier | ADD établi | ADD abstrait | REVIEW chantier | — | — | REVIEW chantier |
| `improved_agricultural_implements` | ADD frontier | — | — | — | — | — | ADD frontier |
| `selective_breeding` | ADD frontier | — | — | — | — | ne pas auto-ajouter | — |
| `advanced_crop_rotations` | ADD frontier | — | — | — | — | KEEP/ADD force flamande | — |

## 7. Anachronismes

- **GBR — `romanticism`** : The gameplay node represents the Romantic movement as a developed cultural-political complex. The movement belongs to the late eighteenth/early nineteenth century, not 1 January 1776.
- **FRA — `romanticism`** : French Romanticism as a movement is post-1776. Precursors do not justify the gameplay node at the strict cutoff.
- **BEL — `state_dockyard_systems`** : The tier_1 grant implies a state naval-administration/shipyard system comparable to major naval powers; this is not supported locally in 1776.
- **BEL — `scientific_naval_architecture`** : No evidence supports a local state naval-architecture establishment comparable to Britain, France, Spain or the Dutch Republic.
- **BEL — `coke_smelting`** : Belgian blast furnaces still relied on charcoal into the early nineteenth century; the first modern coke blast furnace at Seraing dates to about 1820.
- **BEL — `precision_boring`** : No evidence supports a Wilkinson-style precision cylinder-boring capability in the Southern Low Countries by 1 January 1776.
- **SPC — `stock_exchange`** : Madrid's formal stock exchange was created in 1831. The explicit grant is not defensible for a Spain-based 1776 setup.
- **SPC — `coke_smelting`** : The tier_3 grant backdates a technology not established in Spain in 1776; important Spanish coke projects belong to the 1790s and later.
- **SPC — `commercial_insurance_markets`** : Iberian marine insurance existed, but the mature Cádiz market expanded especially after 1780; tier_3 overstates institutionalization at the strict cutoff.

Les retraits structurants sont `romanticism` pour GBR/FRA, `coke_smelting` et `precision_boring` pour BEL, et `coke_smelting`/`stock_exchange` pour SPC. Le grand arsenal et l'architecture navale de BEL sont également retirés faute de base locale comparable aux puissances navales.

## 8. Prérequis

Le cas le plus important est `atmospheric_engine <- coke_smelting`. La France et les Pays-Bas méridionaux ont des machines Newcomen sans sidérurgie locale au coke au sens du nœud. **Il ne faut donc pas ajouter `coke_smelting` pour réparer l'arbre.**

Même logique pour `advanced_crop_rotations <- selective_breeding` : les rotations flamandes suivent une trajectoire indépendante de l'élevage sélectif britannique. Pour les canaux français/néerlandais, le parent `turnpike_road_networks` encode un chemin britannique qui ne doit pas être imposé partout.

À l'inverse, certains parents doivent être ajoutés parce qu'ils sont historiquement justifiés : `institutionalized_scientific_exchange` pour plusieurs académies techniques; `scientific_fortification_siegecraft` pour plusieurs systèmes militaires déjà dotés de `regulated_small_arms`.

## 9. Incertitudes

- `turnpike_road_networks` : institution britannique littérale ou abstraction d'un réseau routier amélioré ? FRA reste REVIEW.
- `industrial_canals` : le Canal du Midi et les canaux néerlandais sont avancés mais ne sont pas le même phénomène que les canaux industriels charbonniers britanniques.
- `atmospheric_engine` en Espagne : vapeur réelle à Cartagena, mais le nœud ne débloque que des pompes de mines.
- BEL/BEO : les nœuds étatiques doivent être maniés prudemment car les Pays-Bas méridionaux de 1776 ne sont pas l'État belge moderne.
- LUX : la très haute capacité de fortification ne doit pas être transformée en industrie nationale d'armes ou en diplomatie souveraine.

## 10. Recommandations pour l'implémentation

- **KEEP_TIER + corrections explicites:** GBR, FRA, NET, SPA, POR, BEO, IREK.
- **CHANGE_TIER:** BEL `tier_1 → tier_4`; SPC `tier_3 → tier_4`, puis réajouts explicites des capacités attestées.
- **REPLACE_WITH_EXPLICIT_SETUP:** LUX.
- Ne pas ajouter `coke_smelting` à FRA/BEL/SPA uniquement pour satisfaire `atmospheric_engine`.
- Traiter canaux et routes selon leurs institutions locales, pas comme une diffusion automatique du modèle britannique.

## Contrôle final

- TAG étudiés : **10**
- KEEP : **127**
- ADD : **72**
- REMOVE : **9**
- REVIEW : **18**
- Pays avec tier à changer : **2** (BEL, SPC)
- Lignes de matrice : **226**
- Toutes les technologies actuellement possédées par les dix TAG ont une décision.
- Tous les `Technology_ID` présents dans la matrice existent dans le CSV technologies.
- Principales incertitudes : interprétation fonctionnelle des routes/canaux, vapeur espagnole hors secteur minier, institutions étatiques des Pays-Bas méridionaux, setup explicite de Luxembourg.
