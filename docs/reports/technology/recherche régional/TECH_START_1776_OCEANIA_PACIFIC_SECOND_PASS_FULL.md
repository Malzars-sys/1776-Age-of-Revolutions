# Recherche technologique — Océanie et Pacifique — SECOND PASS FULL — 1er janvier 1776

**Statut : recherche historique uniquement. Aucun fichier gameplay modifié, aucun code Victoria 3 produit, aucun commit/push.**

Cette seconde passe réévalue les capacités indépendamment des anciens tiers. La matrice exhaustive contient une décision pour chaque combinaison **TAG × technologie A/B**, plus les technologies E ayant un déblocage ou modificateur significatif. Les distributions actuelles servent uniquement à déterminer `Current_Status`, jamais à prouver l'existence historique d'une capacité.

## 1. Périmètre

Région auditée : **Océanie et Pacifique**. Le CSV pays contient **39 TAG** régionaux, tous inclus :

- **Australie — labels coloniaux non encore fondés en 1776** : `NSW` (New South Wales), `SAS` (South Australia), `TAS` (Tasmania), `WAS` (Western Australia)
- **Australie — polities autochtones** : `ARH` (Arnhem), `ARR` (Arrernte), `GRW` (Garawa), `KAU` (Kaurna), `KLN` (Kulin), `KNC` (Karna), `KRI` (Douriango), `KTU` (Kartu), `KYN` (Pilbara), `LRR` (Larrakia), `MRA` (Mara), `MRN` (Mirning), `NNG` (Noongar), `NYP` (Ngumpin-Yapa), `PAA` (Paakintyi), `PMA` (Pama), `WDJ` (Wiradjuri), `WKB` (Waka-Gabi), `WRR` (Worrorra), `WTI` (Anangu), `YGU` (Yolngu), `YUR` (Yura)
- **Aotearoa / Māori** : `NTO` (Ngāti Toa), `NTU` (Ngāi Tahu), `UNT` (United Tribes)
- **Polynésie** : `HAW` (Hawaii), `PLY` (Tahiti), `TNG` (Tonga)
- **Mélanésie** : `BLA` (Bilua), `FJI` (Fiji), `HLA` (Halia), `KNK` (Kanak), `VNT` (Vanuatu)
- **Micronésie** : `MCR` (Micronesia), `NRU` (Nauru)

Périmètre technologique obligatoire : **25 technologies A + 36 technologies B = 61 technologies A/B**. À cela s'ajoutent **5 technologies E** à effet gameplay direct : `field_works`, `colonization`, `urbanization`, `multilateral_alliances`, `political_agitation`.

Aucun nœud C n'est ajouté à la matrice : aucun cas régional n'a fourni une correspondance suffisamment forte avec un nœud C pour déclencher `CLASSIFICATION_REVIEW`. Les anomalies de classification trouvées concernent plutôt deux A/B : `mechanized_weaving` et `medical_degrees`.

## 2. Sources et méthode

### Principe

1. La question primaire est : **la capacité existe-t-elle localement au 1er janvier 1776 ?**
2. Les prérequis sont examinés **après** le verdict historique. Un parent absent ne supprime pas une capacité réelle.
3. Les pratiques autochtones sont évaluées selon leurs propres institutions et techniques. On ne convertit pas automatiquement un savoir maritime en chronométrie européenne, une carrière en mine industrielle, un tissu d'écorce en papeterie, ni une chefferie en bureaucratie statistique.
4. Pour les nœuds qui débloquent directement un bâtiment/PM/loi, le niveau de capacité exigé est celui du **gameplay réellement débloqué**, pas seulement celui suggéré par le nom.

### Mise à jour de l'arbre prise en compte

Les relations déclarées supprimées dans la consigne sont neutralisées dans l'analyse de prérequis : `organized_forestry` n'est plus considéré comme parent nécessaire de `traditional_papermaking`, `traditional_glassmaking` ou `traditional_furniture_making`. L'ancien lien forêt → coke signalé lors de la correction précédente n'est pas utilisé non plus pour décider l'existence historique.

Conséquence importante : **retirer le verrou forestier ne crée pas automatiquement ces manufactures**. Chaque papeterie, verrerie ou manufacture de meubles est recherchée comme capacité indépendante. `organized_forestry` est désormais interprétée strictement comme exploitation forestière organisée/rationalisée; la simple coupe de bois ou sélection d'arbres pour des canoës ne suffit pas.

### Sources de référence majeures
- **Australie autochtone — techniques, transformation alimentaire et réseaux** : https://australian.museum/learn/cultures/first-nations-collections/cultural-objects/grindstones/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=
- **Wilgie Mia — exploitation minière souterraine pré-contact** : https://www.dcceew.gov.au/parks-heritage/heritage/places/national/wilgie-mia ; https://visit.museum.wa.gov.au/learn/news-stories/aboriginal-ochre-mining-midwest
- **Māori — horticulture et outils** : https://teara.govt.nz/en/kumara ; https://teara.govt.nz/en/kumara/page-3
- **Māori — tissage / navigation** : https://teara.govt.nz/en/maori-weaving-and-tukutuku-te-raranga-me-te-whatu ; https://teara.govt.nz/en/canoe-navigation
- **Hawaiʻi pré-contact — agriculture, ingénierie, navigation, gouvernement** : https://www.nps.gov/locations/hawaii/colonization.htm ; https://home.nps.gov/locations/hawaii/social-structure.htm
- **Tahiti — agriculture et commerce interinsulaire** : https://www.cambridge.org/core/journals/radiocarbon/article/radiocarbon-chronology-for-prehistoric-agriculture-in-the-society-islands-french-polynesia/3E2AB548D46A032B3413343B09838193 ; https://manifold.uhpress.hawaii.edu/read/tahiti-nui-change-and-survival-in-french-polynesia-1767-1945/section/50138d5f-0a1e-41e0-9aaa-63c41076c16c
- **Tonga — chefferie maritime et agriculture** : https://www.cambridge.org/core/journals/antiquity/article/abs/monumentality-and-the-development-of-the-tongan-maritime-chiefdom/7C61425966301608C08E533650C87795 ; https://openresearch-repository.anu.edu.au/items/006082cd-8b1f-4087-824a-040b651a16f5
- **Fidji — navires et agriculture** : https://collections.tepapa.govt.nz/topic/3189 ; https://www.cambridge.org/core/journals/antiquity/article/land-tenure-competition-and-ecology-in-fijian-prehistory/D0B010BD01A2963C33858D86F1B83C9D
- **Kanak — irrigation, terrasses, rotations** : https://www.ird.fr/en-nouvelle-caledonie-leau-cest-le-lien ; https://link.springer.com/chapter/10.1007/978-3-031-49140-5_6
- **Vanuatu — horticulture ancienne** : https://www.nature.com/articles/s43247-024-01831-8 ; https://www.tandfonline.com/doi/full/10.1080/00664677.2021.2004878
- **Micronésie — wayfinding et construction de canoës** : https://ich.unesco.org/en/RL/carolinian-wayfinding-and-canoe-making-01735 ; https://ocean.si.edu/human-connections/history-cultures/navigating-waters-micronesian-stick-charts
- **Nauru — subsistance traditionnelle** : https://pacific-data.sprep.org/system/files/b5e38462-d3ab-4c86-ac55-b85dbf0fb89a/viviani_1970.pdf
- **Repère chronologique métiers mécaniques** : https://collection.sciencemuseumgroup.org.uk/people/ap13666/cartwright-edmund
- **Repères institutionnels médecine** : https://facmedecine.umontpellier.fr/patrimoine-historique/son-histoire/ ; https://history.rcp.ac.uk/about/history

## 3. Production

### Diagnostic

La correction de l'arbre confirme que papier, verre et meuble doivent être évalués indépendamment de la forêt. Le résultat régional demeure cependant conservateur : aucun des 39 TAG ne fournit une preuve de 1776 suffisante pour une **papeterie**, une **verrerie** ou une **manufacture de meubles** correspondant aux bâtiments débloqués. Les traditions de tapa/kapa, tissage, sculpture et menuiserie sont réelles mais ne sont pas automatiquement les manufactures du jeu.

`traditional_food_processing` est au contraire massivement sous-attribuée : elle est historiquement adaptée à des systèmes de broyage, cuisson, séchage, stockage et transformation établis dans toute la région. La seconde passe produit **35 ADD** de ce nœud, auxquels s'ajoutent les KEEP déjà présents.

`organized_textile_production` reste en `REVIEW` pour les traditions les mieux documentées (Māori, Hawaiʻi, Tahiti et quelques sociétés insulaires), car le nœud débloque une textile mill et dépasse la simple existence d'un artisanat textile.

`distillation`, `sugar_refining`, `industrial_acids`, `mechanized_spinning`, `advanced_spinning` sont absentes régionalement. `mechanized_weaving` est en outre signalée `CLASSIFICATION_TOO_EARLY` : le métier mécanique de Cartwright est breveté en 1785, après la borne.

## 4. Agriculture

Les systèmes horticoles intensifs de Hawaiʻi, Tahiti, Tonga, Fidji, Kanak, Vanuatu et du nord Māori justifient `improved_husbandry` indépendamment des anciens tiers. La Polynésie/Mélanésie ne doit donc pas être laissée technologiquement vide simplement parce que ses systèmes ne suivent pas une trajectoire agricole européenne.

Cas le plus important : **KNK — Kanak**. Les sources décrivent terrasses, irrigation, combinaisons culturales, rotations et jachères. `advanced_crop_rotations` devient **ADD / ESTABLISHED**, mais son parent `selective_breeding` n'est pas justifié : c'est un `TREE_STRUCTURE_REVIEW` net.

Pour l'Australie autochtone, l'existence d'une gestion élaborée du Country, de la récolte, du broyage et de pratiques culturales locales ne suffit pas à valider mécaniquement `improved_husbandry`, dont le gameplay ouvre fermes/plantations/ranchs. La majorité des TAG australiens restent donc `REVIEW` sur ce nœud plutôt que de conserver l'ancien tier comme preuve.

## 5. Mines/métallurgie

Les quatre labels coloniaux australiens héritaient artificiellement de `coke_smelting`, `atmospheric_engine`, `precision_boring` et `shaft_mining`. La colonie de NSW ne débute qu'en 1788, la Tasmanie britannique en 1803, la Swan River Colony en 1829 et la province d'Australie-Méridionale en 1836 : aucune chaîne industrielle britannique ne peut être projetée localement en 1776.

Exception nouvelle et importante : **Wilgie Mia**, dans le territoire couvert par `WAS`, est la plus grande et la plus profonde mine traditionnelle d'ocre aborigène connue en Australie, avec galeries, stop-and-pillar, étayage et plateformes. Cela fait passer `shaft_mining` de REMOVE (première passe) à **REVIEW** : la technique d'exploitation souterraine est réelle, mais le nœud déverrouille un ensemble beaucoup plus large de mines industrielles. `applied_mineralogy` passe également en REVIEW pour le même problème de granularité.

Aucun TAG ne reçoit coke, vapeur atmosphérique, vapeur à condensation ou alésage de précision.

## 6. Infrastructure

Aucun TAG ne reçoit `turnpike_road_networks` ni `industrial_canals`. Les routes/tracks, canaux d'irrigation kanak, fossés tongiens et aménagements hydrauliques ne sont pas les réseaux routiers à péage ou canaux industriels représentés par ces nœuds.

`organized_forestry` est **REMOVE** pour toute la région sous sa nouvelle définition. Le choix rituel ou technique du bois, l'abattage communautaire d'un arbre ou la sélection de bois de canoë constituent une compétence forestière, mais pas encore une exploitation forestière rationalisée au sens du logging camp amélioré.

`urbanization` est réévaluée malgré son statut E parce qu'elle débloque urban center + construction sector. Elle est retirée de **22 setups actuellement présents**; elle reste en REVIEW pour Hawaiʻi, Tahiti, Tonga, Fidji, Kanak et les trois TAG Māori, où des centres politiques/rituels, pā ou grands établissements rendent le mapping moins trivial.

## 7. Finance et économie

Aucun TAG régional ne possède en 1776 les institutions correspondant à `institutionalized_public_credit`, `commercial_insurance_markets`, `stock_exchange`, `political_economy` ou `classical_political_economy`. Cette conclusion **ne nie pas** les systèmes de tribut, redistribution, dette coutumière ou échange : elle distingue ces mécanismes d'une dette publique institutionnalisée, d'un marché organisé de l'assurance, d'une bourse et d'une économie politique formalisée.

Les quatre labels coloniaux `NSW/SAS/TAS/WAS` constituent le principal faux positif : leur `tier_2` leur attribue actuellement crédit public, assurance commerciale et bourse alors qu'aucun gouvernement colonial local n'existe au 1er janvier 1776.

Le cas demandé FRA/VEN ne relève pas de cette région : il devra être comparé lors de la synthèse mondiale. Cette passe fournit néanmoins un benchmark propre : **aucun TAG océanien n'est utilisé comme justification pour réduire le seuil de `institutionalized_public_credit`**.

## 8. Commerce

`international_relations` est le principal nœud commercial/social régional à réhabiliter. Il est ADD pour Hawaiʻi, Tonga, Fidji, Micronésie et les TAG Māori; `PLY` le conserve. Ces décisions reposent sur des réseaux de guerre, alliance, tribut, échange et navigation entre polities, pas sur l'existence d'un ministère européen.

Les TAG australiens restent en REVIEW : les réseaux continentaux d'échange sont immenses, mais la transformation de ces réseaux en nœud de relations extérieures étatiques requiert davantage de preuves tag-spécifiques. `YGU` reste le cas frontière, car la date de début des contacts Yolŋu–Makasar autour de 1776 demeure débattue.

`colonization` et `multilateral_alliances` (E) sont REMOVE : leurs effets gameplay représentent respectivement les institutions coloniales du jeu et un système moderne de multiples alliances, non la mobilité, la migration ou les alliances coutumières.

## 9. Administration

Les hiérarchies politiques et systèmes coutumiers de la région ne sont pas automatiquement des `systematic_administrative_statistics`, registres de population, cadastres ou codes juridiques écrits. Ces nœuds restent majoritairement absents.

Deux exceptions analytiques :

- **MCR `codified_practical_knowledge` — ADD / TREE_STRUCTURE_REVIEW** : la tradition carolinienne comporte un système de mesure mathématique détaillé, précis et vérifiable, transmis par apprentissage de maître. Les parents `institutionalized_scientific_exchange` + `periodical_print_networks` ne sont donc pas des préconditions universelles de la capacité.
- **HAW `systematic_legal_codification` — REVIEW** : Hawaiʻi possède un ordre normatif structuré (kanawai/kapu), mais le nœud implique une codification étatique plus proche du droit écrit; le chevauchement est réel sans être identique.

`UNT` demande une prudence supplémentaire : la Confédération des United Tribes est formalisée en 1835. Les décisions positives sont donc interprétées comme capacités des communautés Māori du territoire, non comme institutions d'un État « United Tribes » existant en 1776.

## 10. Science/éducation

Aucun TAG ne reçoit `periodical_print_networks`, `institutionalized_scientific_exchange`, `specialized_technical_academies`, `organized_elementary_schooling` ou `veterinary_science`. Cela ne signifie pas absence d'enseignement, d'apprentissage ou d'expertise; cela signifie que les institutions précises déverrouillées/représentées par ces nœuds ne sont pas établies.

Le cas micronésien est justement traité par `codified_practical_knowledge` + TREE_STRUCTURE_REVIEW plutôt que par l'invention d'une presse ou d'une académie européenne.

## 11. Médecine

Aucun TAG océanien n'a une institution de `medical_degrees` ou un réseau de `variolation_networks` établi au 1er janvier 1776 selon les preuves trouvées. Les spécialistes de guérison locaux sont réels, mais ne correspondent pas à ces deux institutions.

Cependant, **`medical_degrees` est classée B trop tardivement à l'échelle mondiale** : Montpellier dispose d'un cadre institutionnel médical dès 1220 et le Royal College of Physicians réglemente/licencie la pratique en Angleterre depuis 1518. La matrice porte donc `CLASSIFICATION_TOO_LATE` sur ce nœud, sans pour autant l'ajouter à un TAG océanien.

## 12. Militaire

Aucun TAG ne reçoit armes réglementaires, artillerie standardisée, inspection d'armement, artillerie à cheval, corps permanent du génie, hôpital militaire permanent ou service topographique militaire.

Pour les Māori, la source NZHistory situe le premier emploi de mousquets au combat vers **1807**, donc `regulated_small_arms` est clairement absent en 1776.

`scientific_fortification_siegecraft` reste en REVIEW pour les trois TAG Māori, Fidji et Tonga : les fortifications sont réelles, mais le nœud combine fortification/siegecraft avec barracks et naval fortification et risque de sur-européaniser la capacité.

`field_works` (E) est REMOVE partout parce que son effet direct est un PM de barbelés, manifestement postérieur à 1776.

## 13. Marine

C'est le domaine où la seconde passe diffère le plus de la première méthodologie. **Ne pas posséder `marine_chronometry` ne signifie pas être maritime technologiquement faible.** La chronométrie est un chemin instrumental européen précis; les traditions océaniennes peuvent posséder une architecture navale et un wayfinding très avancés sans chronomètre.

Décisions majeures :

- **MCR — Micronesia** : `scientific_naval_architecture` = **ADD**, ESTABLISHED, confiance HIGH. Centuries-old ocean-voyaging canoe technology used explicit measurement systems, specialist construction and high-performance asymmetric designs. The functional naval-architecture capacity is established even without a state dockyard.
- **FJI — Fiji** : `scientific_naval_architecture` = **ADD**, FRONTIER, confiance MEDIUM. Fiji had specialist large-vessel construction; the drua tradition combined Fijian, Tongan/Uvean and Micronesian innovations and the improved form was developing in the second half of the eighteenth century. The broader naval-architecture capability is present, but the newest configuration is frontier around 1776.
- **TNG — Tonga** : `scientific_naval_architecture` = **ADD**, ESTABLISHED, confiance HIGH. Tonga was a long-standing maritime chiefdom whose political integration depended on inter-island canoe transport; Te Papa identifies the Tongan kalia as the equivalent of the large Fijian drua tradition.
- **HAW — Hawaii** : `scientific_naval_architecture` = **ADD**, ESTABLISHED, confiance MEDIUM. Pre-contact Hawaiʻi had specialists in canoe-building and a high degree of technical skill in celestial navigation and marine construction; this is a functional naval-architecture capability, not European dockyard science.
- **PLY — Tahiti** : `scientific_naval_architecture` = **ADD**, ESTABLISHED, confiance MEDIUM. Tahiti and the Society Islands maintained large specialist-built canoes for war, trade and inter-island movement; contemporary accounts describe acquisition and deployment of the best canoes as major chiefly resources.

Pour ces ADD, le parent `state_dockyard_systems` reste REVIEW : un réseau de spécialistes/chiefs commanditaires n'est pas nécessairement un arsenal d'État avec administration navale. C'est donc un `TREE_STRUCTURE_REVIEW` : l'arbre impose une séquence institutionnelle trop européenne.

`marine_chronometry` est REMOVE même pour Micronésie : l'UNESCO décrit explicitement une navigation sans cartes ni instruments. C'est une capacité différente, pas un degré inférieur de la même technologie.

## 14. Analyse pays par pays

La matrice CSV contient les 66 décisions ligne par ligne pour chaque TAG. Le diagnostic ci-dessous résume **tous les domaines** : seuls les KEEP/ADD/REVIEW sont détaillés; les autres nœuds du domaine sont REMOVE.

### NSW — New South Wales

- **Retraits sur distribution actuelle** : `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `coke_smelting`, `distillation`, `organized_forestry`, `organized_textile_production`, `shaft_mining`, `traditional_papermaking`, `atmospheric_engine`, `precision_boring`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `commercial_insurance_markets`, `stock_exchange`
- **Présents mais à REVIEW** : `improved_husbandry`, `international_relations`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **KEEP** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://www.parliament.nsw.gov.au/about-parliament/heritage-history/history-democracy-nsw/1788-to-1810-early-european-settlement ; https://australian.museum/learn/cultures/first-nations-collections/timeline/

**Note de statut politique :** le label colonial est postérieur à 1776; les capacités positives/reviews concernent les sociétés locales du territoire, pas une colonie britannique déjà implantée.

### SAS — South Australia

- **Retraits sur distribution actuelle** : `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `coke_smelting`, `distillation`, `organized_forestry`, `organized_textile_production`, `shaft_mining`, `traditional_papermaking`, `atmospheric_engine`, `precision_boring`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `commercial_insurance_markets`, `stock_exchange`
- **Présents mais à REVIEW** : `improved_husbandry`, `international_relations`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **KEEP** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://sahistoryhub.history.sa.gov.au/subjects/the-proclamation/ ; https://australian.museum/learn/cultures/first-nations-collections/timeline/

**Note de statut politique :** le label colonial est postérieur à 1776; les capacités positives/reviews concernent les sociétés locales du territoire, pas une colonie britannique déjà implantée.

### TAS — Tasmania

- **Retraits sur distribution actuelle** : `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `coke_smelting`, `distillation`, `improved_husbandry`, `organized_forestry`, `organized_textile_production`, `shaft_mining`, `traditional_papermaking`, `atmospheric_engine`, `precision_boring`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `commercial_insurance_markets`, `stock_exchange`
- **Présents mais à REVIEW** : `international_relations`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **KEEP** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | 4 nœud(s) audité(s) : tous REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://www.libraries.tas.gov.au/slat/guides-to-records/early-colonial-administration-records/introduction/ ; https://australian.museum/learn/cultures/first-nations-collections/timeline/

**Note de statut politique :** le label colonial est postérieur à 1776; les capacités positives/reviews concernent les sociétés locales du territoire, pas une colonie britannique déjà implantée.

### WAS — Western Australia

- **Retraits sur distribution actuelle** : `enclosed_dock_systems`, `scientific_fortification_siegecraft`, `state_dockyard_systems`, `coke_smelting`, `distillation`, `organized_forestry`, `organized_textile_production`, `traditional_papermaking`, `atmospheric_engine`, `precision_boring`, `institutionalized_public_credit`, `institutionalized_scientific_exchange`, `periodical_print_networks`, `commercial_insurance_markets`, `stock_exchange`
- **Présents mais à REVIEW** : `improved_husbandry`, `shaft_mining`, `international_relations`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **KEEP** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | `shaft_mining` **REVIEW** (ABSTRACT, HIGH); `applied_mineralogy` **REVIEW** (ABSTRACT, MEDIUM); 4 autre(s) nœud(s) REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://museum.wa.gov.au/welcomewalls/history ; https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://www.dcceew.gov.au/parks-heritage/heritage/places/national/wilgie-mia ; https://visit.museum.wa.gov.au/learn/news-stories/aboriginal-ochre-mining-midwest

**Note de statut politique :** le label colonial est postérieur à 1776; les capacités positives/reviews concernent les sociétés locales du territoire, pas une colonie britannique déjà implantée.

### ARH — Arnhem

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### ARR — Arrernte

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### GRW — Garawa

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### KAU — Kaurna

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### KLN — Kulin

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### KNC — Karna

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### KRI — Douriango

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### KTU — Kartu

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### KYN — Pilbara

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### LRR — Larrakia

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### MRA — Mara

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### MRN — Mirning

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### NNG — Noongar

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### NYP — Ngumpin-Yapa

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### PAA — Paakintyi

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### PMA — Pama

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### WDJ — Wiradjuri

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### WKB — Waka-Gabi

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### WRR — Worrorra

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### WTI — Anangu

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### YGU — Yolngu

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (FRONTIER, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://www.nma.gov.au/defining-moments/resources/trade-with-the-makasar ; https://www.nma.gov.au/audio/behind-the-scenes-australian-journeys-series/transcripts/from-makassar-to-marege-to-the-museum ; https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### YUR — Yura

- **Retraits sur distribution actuelle** : `urbanization`
- **Présents mais à REVIEW** : `improved_husbandry`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://australian.museum/learn/cultures/first-nations-collections/timeline/ ; https://press-files.anu.edu.au/downloads/press/p122571/html/ch02.xhtml?page=5&referer=

### NTO — Ngāti Toa

- **Retraits sur distribution actuelle** : `shaft_mining`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **Présents mais à REVIEW** : `organized_textile_production`, `urbanization`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); `organized_textile_production` **REVIEW** (ABSTRACT, MEDIUM); 10 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_agricultural_implements` **REVIEW** (ABSTRACT, MEDIUM); `improved_husbandry` **KEEP** (ESTABLISHED, HIGH); 2 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | `urbanization` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **ADD** (ESTABLISHED, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | `scientific_fortification_siegecraft` **REVIEW** (ABSTRACT, MEDIUM); 9 autre(s) nœud(s) REMOVE |
| Marine | `scientific_naval_architecture` **REVIEW** (ABSTRACT, MEDIUM); 5 autre(s) nœud(s) REMOVE |

**Sources principales du TAG :** https://teara.govt.nz/en/maori/print ; https://teara.govt.nz/en/kumara

### NTU — Ngāi Tahu

- **Retraits sur distribution actuelle** : `shaft_mining`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **Présents mais à REVIEW** : `improved_husbandry`, `organized_textile_production`, `urbanization`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); `organized_textile_production` **REVIEW** (ABSTRACT, MEDIUM); 10 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_agricultural_implements` **REVIEW** (ABSTRACT, MEDIUM); `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | `urbanization` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **ADD** (ESTABLISHED, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | `scientific_fortification_siegecraft` **REVIEW** (ABSTRACT, MEDIUM); 9 autre(s) nœud(s) REMOVE |
| Marine | `scientific_naval_architecture` **REVIEW** (ABSTRACT, MEDIUM); 5 autre(s) nœud(s) REMOVE |

**Sources principales du TAG :** https://teara.govt.nz/en/maori/print ; https://teara.govt.nz/en/kumara

### UNT — United Tribes

- **Retraits sur distribution actuelle** : —
- **Présents mais à REVIEW** : `urbanization`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); `organized_textile_production` **REVIEW** (ABSTRACT, MEDIUM); 10 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_agricultural_implements` **REVIEW** (ABSTRACT, MEDIUM); `improved_husbandry` **KEEP** (ESTABLISHED, HIGH); 2 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | `urbanization` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **ADD** (ESTABLISHED, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | `scientific_fortification_siegecraft` **REVIEW** (ABSTRACT, MEDIUM); 9 autre(s) nœud(s) REMOVE |
| Marine | `scientific_naval_architecture` **REVIEW** (ABSTRACT, MEDIUM); 5 autre(s) nœud(s) REMOVE |

**Sources principales du TAG :** https://nzhistory.govt.nz/media/interactive/he-whakaputanga-declaration-independence-1835 ; https://teara.govt.nz/en/kumara ; https://teara.govt.nz/en/canoe-navigation

**Note de statut politique :** la Confédération des United Tribes date de 1835; le setup 1776 ne peut être qu'un proxy géographique pour les sociétés Māori correspondantes.

### HAW — Hawaii

- **Retraits sur distribution actuelle** : `shaft_mining`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **Présents mais à REVIEW** : `organized_textile_production`, `urbanization`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); `organized_textile_production` **REVIEW** (ABSTRACT, MEDIUM); 10 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **KEEP** (ESTABLISHED, HIGH); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | `urbanization` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **ADD** (ESTABLISHED, HIGH); 2 autre(s) nœud(s) REMOVE |
| Administration | `systematic_legal_codification` **REVIEW** (ABSTRACT, MEDIUM); 8 autre(s) nœud(s) REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | `state_dockyard_systems` **REVIEW** (ABSTRACT, MEDIUM); `scientific_naval_architecture` **ADD** (ESTABLISHED, MEDIUM); 4 autre(s) nœud(s) REMOVE |

**Sources principales du TAG :** https://www.nps.gov/locations/hawaii/colonization.htm ; https://home.nps.gov/locations/hawaii/social-structure.htm

### PLY — Tahiti

- **Retraits sur distribution actuelle** : `shaft_mining`, `codified_practical_knowledge`, `systematic_administrative_statistics`
- **Présents mais à REVIEW** : `organized_textile_production`, `urbanization`

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); `organized_textile_production` **REVIEW** (ABSTRACT, MEDIUM); 10 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **KEEP** (ESTABLISHED, HIGH); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | `urbanization` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **KEEP** (ESTABLISHED, HIGH); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | `state_dockyard_systems` **REVIEW** (ABSTRACT, MEDIUM); `scientific_naval_architecture` **ADD** (ESTABLISHED, MEDIUM); 4 autre(s) nœud(s) REMOVE |

**Sources principales du TAG :** https://manifold.uhpress.hawaii.edu/read/tahiti-nui-change-and-survival-in-french-polynesia-1767-1945/section/50138d5f-0a1e-41e0-9aaa-63c41076c16c ; https://www.cambridge.org/core/journals/radiocarbon/article/radiocarbon-chronology-for-prehistoric-agriculture-in-the-society-islands-french-polynesia/3E2AB548D46A032B3413343B09838193

### TNG — Tonga

- **Retraits sur distribution actuelle** : —
- **Présents mais à REVIEW** : —

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); `organized_textile_production` **REVIEW** (ABSTRACT, LOW); 10 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **ADD** (ESTABLISHED, HIGH); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | `urbanization` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **ADD** (ESTABLISHED, HIGH); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | `scientific_fortification_siegecraft` **REVIEW** (ABSTRACT, MEDIUM); 9 autre(s) nœud(s) REMOVE |
| Marine | `state_dockyard_systems` **REVIEW** (ABSTRACT, MEDIUM); `scientific_naval_architecture` **ADD** (ESTABLISHED, HIGH); 4 autre(s) nœud(s) REMOVE |

**Sources principales du TAG :** https://www.cambridge.org/core/journals/antiquity/article/abs/monumentality-and-the-development-of-the-tongan-maritime-chiefdom/7C61425966301608C08E533650C87795 ; https://openresearch-repository.anu.edu.au/items/006082cd-8b1f-4087-824a-040b651a16f5

### BLA — Bilua

- **Retraits sur distribution actuelle** : —
- **Présents mais à REVIEW** : —

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, MEDIUM); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://www.britishmuseum.org/sites/default/files/2020-08/R24_Solomon_LPG.pdf ; https://openresearch-repository.anu.edu.au/items/2e211767-dbcc-4b5c-a23e-3973e9a7550d

### FJI — Fiji

- **Retraits sur distribution actuelle** : —
- **Présents mais à REVIEW** : —

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); `industrial_ceramics` **REVIEW** (ABSTRACT, MEDIUM); `organized_textile_production` **REVIEW** (ABSTRACT, LOW); 9 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **ADD** (ESTABLISHED, HIGH); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | `urbanization` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **ADD** (ESTABLISHED, HIGH); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | `scientific_fortification_siegecraft` **REVIEW** (ABSTRACT, MEDIUM); 9 autre(s) nœud(s) REMOVE |
| Marine | `state_dockyard_systems` **REVIEW** (ABSTRACT, MEDIUM); `scientific_naval_architecture` **ADD** (FRONTIER, MEDIUM); 4 autre(s) nœud(s) REMOVE |

**Sources principales du TAG :** https://www.cambridge.org/core/journals/antiquity/article/land-tenure-competition-and-ecology-in-fijian-prehistory/D0B010BD01A2963C33858D86F1B83C9D ; https://collections.tepapa.govt.nz/topic/3189

### HLA — Halia

- **Retraits sur distribution actuelle** : —
- **Présents mais à REVIEW** : —

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, MEDIUM); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://www.britishmuseum.org/sites/default/files/2020-08/R24_Solomon_LPG.pdf ; https://openresearch-repository.anu.edu.au/items/2e211767-dbcc-4b5c-a23e-3973e9a7550d

### KNK — Kanak

- **Retraits sur distribution actuelle** : —
- **Présents mais à REVIEW** : —

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); `organized_textile_production` **REVIEW** (ABSTRACT, LOW); 10 autre(s) nœud(s) REMOVE |
| Agriculture | `advanced_crop_rotations` **ADD** (ESTABLISHED, HIGH); `improved_husbandry` **ADD** (ESTABLISHED, HIGH); 2 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | `urbanization` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://ehrafworldcultures.yale.edu/cultures/op04/description ; https://www.ird.fr/en-nouvelle-caledonie-leau-cest-le-lien ; https://link.springer.com/chapter/10.1007/978-3-031-49140-5_6

### VNT — Vanuatu

- **Retraits sur distribution actuelle** : —
- **Présents mais à REVIEW** : —

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); `organized_textile_production` **REVIEW** (ABSTRACT, LOW); 10 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **ADD** (ESTABLISHED, HIGH); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, MEDIUM); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://www.nature.com/articles/s43247-024-01831-8 ; https://www.tandfonline.com/doi/full/10.1080/00664677.2021.2004878

### MCR — Micronesia

- **Retraits sur distribution actuelle** : —
- **Présents mais à REVIEW** : —

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); `organized_textile_production` **REVIEW** (ABSTRACT, LOW); 10 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **ADD** (ESTABLISHED, HIGH); 2 autre(s) nœud(s) REMOVE |
| Administration | `codified_practical_knowledge` **ADD** (ESTABLISHED, HIGH); 8 autre(s) nœud(s) REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | `state_dockyard_systems` **REVIEW** (ABSTRACT, MEDIUM); `scientific_naval_architecture` **ADD** (ESTABLISHED, HIGH); 4 autre(s) nœud(s) REMOVE |

**Sources principales du TAG :** https://ich.unesco.org/en/RL/carolinian-wayfinding-and-canoe-making-01735 ; https://ocean.si.edu/human-connections/history-cultures/navigating-waters-micronesian-stick-charts

### NRU — Nauru

- **Retraits sur distribution actuelle** : —
- **Présents mais à REVIEW** : —

| Domaine | Diagnostic 1776 |
|---|---|
| Production et artisanat | `traditional_food_processing` **ADD** (ESTABLISHED, HIGH); 11 autre(s) nœud(s) REMOVE |
| Agriculture | `improved_husbandry` **REVIEW** (ABSTRACT, MEDIUM); 3 autre(s) nœud(s) REMOVE |
| Mines / métallurgie | 6 nœud(s) audité(s) : tous REMOVE |
| Infrastructure | 4 nœud(s) audité(s) : tous REMOVE |
| Finance / économie | 5 nœud(s) audité(s) : tous REMOVE |
| Commerce / relations | `international_relations` **REVIEW** (ABSTRACT, LOW); 2 autre(s) nœud(s) REMOVE |
| Administration | 9 nœud(s) audité(s) : tous REMOVE |
| Science / éducation | 5 nœud(s) audité(s) : tous REMOVE |
| Médecine | 2 nœud(s) audité(s) : tous REMOVE |
| Militaire terrestre | 10 nœud(s) audité(s) : tous REMOVE |
| Marine | 6 nœud(s) audité(s) : tous REMOVE |

**Sources principales du TAG :** https://pacific-data.sprep.org/system/files/b5e38462-d3ab-4c86-ac55-b85dbf0fb89a/viviani_1970.pdf ; https://ocean.si.edu/human-connections/history-cultures/navigating-waters-micronesian-stick-charts

## 15. TREE_STRUCTURE_REVIEW

**14 lignes** de la matrice déclenchent `TREE_STRUCTURE_REVIEW` :

| TAG | Technologie | Décision | Parent(s) problématique(s) | Pourquoi |
|---|---|---|---|---|
| FJI | `scientific_naval_architecture` | ADD | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (state_dockyard_systems=REVIEW). | Fiji had specialist large-vessel construction; the drua tradition combined Fijian, Tongan/Uvean and Micronesian innovations and the improved form was developing in the second half of the eighteenth century. The broader naval-architecture capability is present, but the newest configuration is frontier around 1776. |
| FJI | `industrial_ceramics` | REVIEW | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (traditional_glassmaking=REMOVE). | Pre-contact/early-contact Fiji had pottery and specialized salt production using large clay dishes, but the node represents industrial ceramics inside a glassworks chain; the craft is real while the gameplay mapping is uncertain. |
| HAW | `scientific_naval_architecture` | ADD | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (state_dockyard_systems=REVIEW). | Pre-contact Hawaiʻi had specialists in canoe-building and a high degree of technical skill in celestial navigation and marine construction; this is a functional naval-architecture capability, not European dockyard science. |
| HAW | `systematic_legal_codification` | REVIEW | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (systematic_administrative_statistics=REMOVE). | Hawaiʻi had a structured system of kanawai/kapu governing land, resources and social order, but the game's 'systematic legal codification' implies a codified state-law apparatus; the functional overlap is real but not exact. |
| KNK | `advanced_crop_rotations` | ADD | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (selective_breeding=REMOVE). | Pre-colonial Kanak agriculture used extensive terracing plus crop combinations, rotations and fallow systems; the agronomic capacity is directly attested even though the game's prerequisite chain is unsuitable. |
| MCR | `scientific_naval_architecture` | ADD | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (state_dockyard_systems=REVIEW). | Centuries-old ocean-voyaging canoe technology used explicit measurement systems, specialist construction and high-performance asymmetric designs. The functional naval-architecture capacity is established even without a state dockyard. |
| MCR | `codified_practical_knowledge` | ADD | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (institutionalized_scientific_exchange=REMOVE, periodical_print_networks=REMOVE). | Carolinian canoe construction uses a detailed, accurate and verifiable indigenous mathematical measurement tradition transmitted by master apprenticeship. This is a strong functional case for codified practical knowledge even though the knowledge is non-print and the current parent chain is Eurocentric. |
| NTO | `scientific_naval_architecture` | REVIEW | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (state_dockyard_systems=REMOVE). | Waka construction and navigation were sophisticated and specialist, but the node's 'scientific naval architecture' abstraction and state-dockyard parent make the exact gameplay mapping uncertain. |
| NTU | `scientific_naval_architecture` | REVIEW | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (state_dockyard_systems=REMOVE). | Waka construction and navigation were sophisticated and specialist, but the node's 'scientific naval architecture' abstraction and state-dockyard parent make the exact gameplay mapping uncertain. |
| NTU | `improved_agricultural_implements` | REVIEW | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (improved_husbandry=REVIEW). | Māori developed a wide range of specialized gardening tools and soil-modification techniques, but the game's PM implies an improved farm-tool/tool-industry package; the functional match is incomplete. |
| PLY | `scientific_naval_architecture` | ADD | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (state_dockyard_systems=REVIEW). | Tahiti and the Society Islands maintained large specialist-built canoes for war, trade and inter-island movement; contemporary accounts describe acquisition and deployment of the best canoes as major chiefly resources. |
| TNG | `scientific_naval_architecture` | ADD | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (state_dockyard_systems=REVIEW). | Tonga was a long-standing maritime chiefdom whose political integration depended on inter-island canoe transport; Te Papa identifies the Tongan kalia as the equivalent of the large Fijian drua tradition. |
| UNT | `scientific_naval_architecture` | REVIEW | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (state_dockyard_systems=REMOVE). | Waka construction and navigation were sophisticated and specialist, but the node's 'scientific naval architecture' abstraction and state-dockyard parent make the exact gameplay mapping uncertain. |
| WAS | `applied_mineralogy` | REVIEW | historical capability is plausible/established while parent chain is absent, ambiguous, or Eurocentric (shaft_mining=REVIEW). | Wilgie Mia demonstrates sophisticated underground ochre extraction and material selection, but the game's applied-mineralogy node unlocks gold/phosphate mining. The local mineral expertise is real while the gameplay mapping is too broad. |

Les trois familles structurelles dominantes sont :

1. **Architecture navale → arsenal d'État** : MCR/FJI/TNG/HAW/PLY peuvent avoir une vraie architecture navale spécialisée sans `state_dockyard_systems`.
2. **Savoir pratique → presse/science institutionnelle** : MCR possède un système de mesure/apprentissage codifié sans presse périodique.
3. **Rotations culturales → élevage sélectif** : KNK possède rotations/jachères sans nécessiter le parent `selective_breeding` centré sur l'élevage.

## 16. CLASSIFICATION_REVIEW

### C → `CLASSIFICATION_REVIEW`

**0 technologie C régionale** atteint le seuil de reclassification dans cette passe. Plusieurs capacités maritimes autochtones sont avancées, mais elles correspondent fonctionnellement à des nœuds A/B ou révèlent un trou de structure plutôt qu'à un nœud C précis.

### Autres anomalies de classification

- **`mechanized_weaving` — CLASSIFICATION_TOO_EARLY** : le PM du nœud est le métier mécanique; Cartwright propose la mécanisation en 1784 et brevète son métier en 1785. Une classification B « frontière 1776 » est trop précoce.
- **`medical_degrees` — CLASSIFICATION_TOO_LATE** : l'enseignement médical institutionnalisé et la régulation/licence des praticiens existent depuis des siècles avant 1776. La classification B sous-estime la diffusion historique mondiale, même si aucun TAG de cette région ne reçoit le nœud.

## 17. Principales différences avec la première passe

La première matrice régionale contenait **205 lignes** ciblées. La seconde en contient **2574** : elle couvre désormais chaque A/B pour chaque TAG, plus cinq E.

Parmi les relations déjà examinées lors de la première passe, **10 décisions changent** :

| TAG | Technologie | Première passe | Seconde passe | Motif |
|---|---|---:|---:|---|
| BLA | `traditional_food_processing` | REVIEW | **ADD** | Traditional food preparation and preservation are integral to the documented Solomon Islands subsistence complex; evidence is sufficient for an ADD, but tag-specific 1776 documentation is thinner than for the major island groups. |
| HAW | `urbanization` | REMOVE | **REVIEW** | Substantial settlements, chiefly/ritual centers, pā or engineered landscapes existed, but the compatibility node directly unlocks a generic urban center and construction sector; settlement complexity alone is insufficient for a clean ADD. |
| HLA | `traditional_food_processing` | REVIEW | **ADD** | Traditional food preparation and preservation are integral to the documented Solomon Islands subsistence complex; evidence is sufficient for an ADD, but tag-specific 1776 documentation is thinner than for the major island groups. |
| NTO | `international_relations` | REVIEW | **ADD** | Iwi and hapū interacted through alliance, conflict, migration and exchange; treating distinct Māori polities as capable of structured external relations is more accurate than withholding the abstract node because they lacked a European foreign ministry. |
| NTU | `improved_husbandry` | KEEP | **REVIEW** | Cultivation or resource management existed, but the node unlocks a broad farm/plantation/ranch package that does not map cleanly onto the local 1776 system. |
| NTU | `international_relations` | REVIEW | **ADD** | Iwi and hapū interacted through alliance, conflict, migration and exchange; treating distinct Māori polities as capable of structured external relations is more accurate than withholding the abstract node because they lacked a European foreign ministry. |
| PLY | `urbanization` | REMOVE | **REVIEW** | Substantial settlements, chiefly/ritual centers, pā or engineered landscapes existed, but the compatibility node directly unlocks a generic urban center and construction sector; settlement complexity alone is insufficient for a clean ADD. |
| TAS | `improved_husbandry` | REVIEW | **REMOVE** | Palawa subsistence and landscape management were sophisticated, but the agricultural farm/plantation/ranch package represented by this node is not supported for Tasmania in 1776. |
| UNT | `international_relations` | REVIEW | **ADD** | Iwi and hapū interacted through alliance, conflict, migration and exchange; treating distinct Māori polities as capable of structured external relations is more accurate than withholding the abstract node because they lacked a European foreign ministry. |
| WAS | `shaft_mining` | REMOVE | **REVIEW** | Within the territory represented by WAS, Wilgie Mia was a large, deep pre-contact underground ochre mine using galleries, stop-and-pillar support, shoring and scaffolding. That is genuine shaft/underground mining expertise, but the node unlocks industrial coal/metal/salt mines and therefore overgeneralizes the capability. |

Nouveaux constats qui n'étaient pas nécessairement présents ligne par ligne dans la première matrice :

- ADD d'`scientific_naval_architecture` pour MCR/FJI/TNG/HAW/PLY, avec TREE_STRUCTURE_REVIEW du parent arsenal.
- ADD de `codified_practical_knowledge` pour MCR malgré l'absence des parents imprimés/scientifiques.
- ADD d'`advanced_crop_rotations` pour KNK malgré le parent `selective_breeding` injustifié.
- Réouverture de `shaft_mining` et `applied_mineralogy` pour WAS en REVIEW grâce à Wilgie Mia.
- `traditional_food_processing` devient un nœud régional fondamental : 35 nouveaux ADD.
- Les corrections de prérequis de `organized_forestry` n'entraînent **aucun** ADD automatique de papier/verre/meuble dans la région.
- Deux anomalies de classification mondiale sont désormais explicitement signalées : métier mécanique trop tôt, diplômes médicaux trop tard.

## 18. Recommandations finales

### Verdict régional

La seconde passe confirme qu'un système de tiers génériques est particulièrement mauvais pour l'Océanie. Il produit simultanément :

- des **sur-attributions européennes** aux labels coloniaux australiens (vapeur, coke, machine-outil, finance, presse, arsenaux);
- des **sous-attributions majeures** aux sociétés insulaires (horticulture, transformation alimentaire, relations régionales, architecture navale, savoir pratique spécialisé);
- des **faux équivalents** où une capacité autochtone réelle est forcée dans un parent institutionnel européen qui n'est pas historiquement nécessaire.

La recommandation reste donc un **setup explicite par TAG**, avec arbitrage mondial des 14 `TREE_STRUCTURE_REVIEW` et des deux anomalies de classification A/B avant l'implémentation.

### 20 changements les plus importants par rapport à la distribution actuelle

| # | Changement | TAG | Transition | Importance historique |
|---:|---|---|---|---|
| 1 | Retirer `atmospheric_engine` des quatre labels coloniaux australiens | `NSW`, `SAS`, `TAS`, `WAS` | **PRESENT → REMOVE** | Aucune de ces colonies britanniques n'existe encore en 1776; aucune infrastructure locale de pompage minier à vapeur. |
| 2 | Retirer `precision_boring` des quatre labels coloniaux | `NSW`, `SAS`, `TAS`, `WAS` | **PRESENT → REMOVE** | L'alésage de précision est une frontière machine-outil britannique des années 1770, sans implantation locale. |
| 3 | Retirer `coke_smelting` des quatre labels coloniaux | `NSW`, `SAS`, `TAS`, `WAS` | **PRESENT → REMOVE** | Pas de sidérurgie locale au coke; l'ancien tier copiait une capacité métropolitaine. |
| 4 | Retirer `traditional_papermaking` des quatre labels coloniaux | `NSW`, `SAS`, `TAS`, `WAS` | **PRESENT → REMOVE** | Le nouveau découplage d'`organized_forestry` ne crée pas une papeterie locale; barkcloth/fibres ≠ papier. |
| 5 | Retirer `institutionalized_public_credit` des quatre labels coloniaux | `NSW`, `SAS`, `TAS`, `WAS` | **PRESENT → REMOVE** | Il n'existe pas de gouvernement colonial local portant dette publique/crédit institutionnalisé en 1776. |
| 6 | Retirer `stock_exchange` des quatre labels coloniaux | `NSW`, `SAS`, `TAS`, `WAS` | **PRESENT → REMOVE** | Aucune bourse locale; attribution héritée artificiellement du tier. |
| 7 | Retirer `commercial_insurance_markets` des quatre labels coloniaux | `NSW`, `SAS`, `TAS`, `WAS` | **PRESENT → REMOVE** | Aucun marché local d'assurance commerciale/maritime institutionnalisé. |
| 8 | Retirer les réseaux imprimés/scientifiques coloniaux | `NSW`, `SAS`, `TAS`, `WAS` | **PRESENT → REMOVE** | `periodical_print_networks` et `institutionalized_scientific_exchange` ne doivent pas être hérités de la métropole. |
| 9 | Retirer docks/arsenaux d'État des quatre labels coloniaux | `NSW`, `SAS`, `TAS`, `WAS` | **PRESENT → REMOVE** | `enclosed_dock_systems` et `state_dockyard_systems` ne sont pas implantés localement en 1776. |
| 10 | Ajouter `traditional_food_processing` à 35 TAG actuellement dépourvus | 35 TAG | **ABSENT → ADD** | La transformation, le stockage, le broyage, le séchage ou la cuisson organisée sont largement attestés et avaient été sous-évalués. |
| 11 | Retirer `urbanization` des 22 TAG australiens autochtones qui l'ont actuellement | 22 TAG australiens autochtones | **PRESENT → REMOVE** | L'alias débloque urban center + construction sector; campements, paysages aménagés et réseaux d'échange ne suffisent pas. |
| 12 | Retirer `shaft_mining` de HAW/NTO/NTU/PLY et des faux setups coloniaux hors cas WAS | `HAW`, `NTO`, `NTU`, `PLY`, `NSW`, `SAS`, `TAS` | **PRESENT → REMOVE** | La carrière/extraction lithique ne justifie pas le complexe de mines industrielles du nœud. |
| 13 | Réouvrir `shaft_mining` pour le territoire `WAS` | `WAS` | **PRESENT → REVIEW** | Wilgie Mia est une véritable mine souterraine pré-contact avec galeries, étayage, stop-and-pillar et échafaudages; le nœud reste trop large. |
| 14 | Ajouter `scientific_naval_architecture` à Micronésie | `MCR` | **ABSENT → ADD** | Construction hauturière, mesures indigènes vérifiables, conception asymétrique et apprentissage spécialisé; parent `state_dockyard_systems` à revoir. |
| 15 | Ajouter `scientific_naval_architecture` à Fidji | `FJI` | **ABSENT → ADD** | Grands drua, spécialistes et transferts techniques régionaux; statut FRONTIER autour de 1776. |
| 16 | Ajouter `scientific_naval_architecture` à Tonga | `TNG` | **ABSENT → ADD** | État maritime ancien, intégration interinsulaire et tradition de grands canoës. |
| 17 | Ajouter `scientific_naval_architecture` à Hawaiʻi | `HAW` | **ABSENT → ADD** | Spécialistes de construction de canoës et savoir nautique pré-contact documentés. |
| 18 | Ajouter `scientific_naval_architecture` à Tahiti | `PLY` | **ABSENT → ADD** | Grands canoës de guerre/commerce et production spécialisée dans les réseaux des îles de la Société. |
| 19 | Ajouter `codified_practical_knowledge` à Micronésie | `MCR` | **ABSENT → ADD** | Système de mesure mathématique précis et vérifiable transmis par apprentissage; l'exigence print/science du parent est structurellement eurocentrée. |
| 20 | Ajouter `advanced_crop_rotations` aux Kanak | `KNK` | **ABSENT → ADD** | Rotations, jachères, terrasses et irrigation sont attestées; le parent `selective_breeding` est historiquement inadapté et déclenche TREE_STRUCTURE_REVIEW. |

### Contrôle final

- Nombre de TAG : **39**
- Technologies A auditées : **25**
- Technologies B auditées : **36**
- Technologies E auditées : **5**
- Technologies C ajoutées à la matrice pour CLASSIFICATION_REVIEW : **0**
- Lignes totales : **2574**
- ADD : **53**
- REMOVE : **2413**
- KEEP : **9**
- REVIEW : **99**
- TREE_STRUCTURE_REVIEW : **14 lignes**
- CLASSIFICATION_REVIEW (technologies C) : **0**
- CLASSIFICATION_TOO_EARLY : **1 technologie unique** (`mechanized_weaving`; répétée sur 39 lignes TAG×tech)
- CLASSIFICATION_TOO_LATE : **1 technologie unique** (`medical_degrees`; répétée sur 39 lignes TAG×tech)
- Changements implémentatoires directs identifiés : **53 ADD sur nœuds actuellement absents + 98 REMOVE sur nœuds actuellement présents = 151**
- Nœuds actuellement présents mais laissés en REVIEW : **40**

**Aucun fichier gameplay modifié. Aucun code. Aucun commit. Aucun push.**
