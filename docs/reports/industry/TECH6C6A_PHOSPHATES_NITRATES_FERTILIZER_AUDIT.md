# TECH6C6A — Audit fondation phosphates, nitrates et chaîne des engrais

Date de l’audit : 9 septembre 2026  
Branche observée : `tech6c-goods-buildings-pm-implementation`  
Nature : audit et conception uniquement — aucune définition de gameplay n’est modifiée.

## 1. Résultat exécutif

**TECH6C6A RESULT: PASS**

La chaîne peut être enrichie sans créer de technologie vide ni de nouveau bâtiment d’engrais. La meilleure progression est séquentielle :

1. **TECH6C6B : phosphates seulement** — nouveau bien brut, mine plafonnée et deux routes phosphatées dans le bâtiment d’engrais existant ;
2. **TECH6C6C : nitrates et substitution synthétique** — ressource naturelle extrêmement concentrée, révision coordonnée des explosifs et route Haber-Bosch sans nitrate miné ;
3. les fermes, mines, munitions et armes chimiques continuent de consommer les biens transformés déjà établis.

Décisions obligatoires :

| Question | Décision |
|---|---|
| PHOSPHATES | **IMPLEMENT** |
| NITRATES | **DEFER** |
| GUANO GOOD | **REJECT** |
| PHOSPHATE MINE | **IMPLEMENT** |
| NITRATE MINE | **DEFER** |
| SYNTHETIC NITROGEN ROUTE | **DEFER** |
| NEW TECHNOLOGY REQUIRED | **NO** |
| FERTILIZER BUILDING ARCHITECTURE | conserver `building_chemical_plant` et `pmg_fertilizer_production`; transformer ses PM de base en routes mutuellement exclusives plutôt que créer un second bâtiment |

`DEFER` signifie ici « conception retenue mais hors du lot 6B », pas rejet. TECH6C5 reste gelé ; l’addendum opérateur a seulement été consigné dans son rapport de validation.

## 2. Sources et périmètre examiné

### Sources internes

- `docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` : chaîne acides/engrais/explosifs, superphosphate, nitrates naturels et Haber-Bosch ;
- `docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md` : séquence industrielle C22–C23 ;
- `docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv` : phosphates Tier A (33), nitrates Tier A (35), guano Tier C ;
- `docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` : priorité à l’extension du bâtiment d’engrais existant ;
- `docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` : superphosphate, guano et Haber-Bosch ;
- rapports TECH6C3A–D et TECH6C5A–D : chimie industrielle, compatibilité aval et périmètre cuivre/aluminium gelé ;
- toutes les définitions locales pertinentes de biens, bâtiments, PM, PMG, technologies, mobilisation, historique de bâtiments et régions d’État ;
- définitions vanilla des biens `fertilizer` et `explosives`, absentes du dossier local et donc héritées.

### Sources géologiques et historiques externes

- [USGS, Mineral Commodity Summaries 2026 — Phosphate Rock](https://pubs.usgs.gov/periodicals/mcs2026/mcs2026-phosphate.pdf) : réserves et grands pays producteurs ;
- [USGS, Phosphate Rock](https://pubs.usgs.gov/fs/fs155-99/fs155-99.html) : traitement du phosphate par l’acide sulfurique et principaux districts américains ;
- [USGS Professional Paper 1188 — The nitrate deposits of the Atacama Desert](https://pubs.usgs.gov/pp/1188/report.pdf) : ceinture commerciale de 700 km, Tarapacá et Antofagasta ;
- [USGS — stable isotope geochemistry of natural nitrate deposits](https://pubs.usgs.gov/publication/70019976) : occurrences hors Chili, notamment Death Valley, sans équivalence économique retenue ici ;
- [USGS — Deserts and mineral resources](https://pubs.usgs.gov/gip/deserts/minerals/) : exploitation chilienne pour engrais et explosifs depuis le XIXe siècle ;
- [Nobel Prize — Fritz Haber](https://www.nobelprize.org/prizes/chemistry/1918/haber/biographical/) et [ACS, Haber-Bosch process](https://pubs.acs.org/doi/10.1021/acsaem.1c03045) : synthèse catalytique d’ammoniac à haute pression et haute température, industrialisée en 1913.

Les deux matrices géographiques sont des criblages mondiaux préliminaires. Une source mondiale justifie une enveloppe nationale, mais pas toujours le découpage exact d’un État Victoria 3 ; les lignes non nulles de confiance `LOW` ou `MEDIUM` doivent donc recevoir une preuve géologique nationale avant implémentation finale.

## 3. Audit du système existant

### 3.1 Biens et bâtiments

| Objet | État actuel | Rôle observé |
|---|---|---|
| `fertilizer` | bien vanilla, prix de base £30 | intrant agricole, intrant-proxy de chimie/explosifs, production du bâtiment d’engrais et faible sous-produit d’élevage |
| `explosives` | bien vanilla, prix de base £50 | intrant des mines et des munitions |
| `industrial_chemicals` | bien local, prix de base £40 | produit du Chemical Works TECH6C3, intrant de plusieurs chaînes dont la méthode actuelle `pm_nitrogen_fixation` |
| `building_chemical_plant` | bâtiment local dans `01_industry.txt`, ouvert par `industrial_acids` | malgré son identifiant historique, il ne contient que le groupe de production d’engrais |
| `building_explosives_factory` | bâtiment distinct, ouvert par `industrial_acids` | transforme soufre et engrais-proxy en explosifs |
| `building_chemical_works` | bâtiment TECH6C3 distinct | produit `industrial_chemicals`; ne produit pas d’engrais |

Conclusion : l’architecture locale sépare déjà correctement chimie de base, engrais et explosifs. Ajouter une « usine d’engrais » parallèle créerait un doublon. L’identifiant `building_chemical_plant` peut être conservé pour la compatibilité tandis que sa localisation pourra rester/être clarifiée comme **Fertilizer Plant / Usine d’engrais**.

### 3.2 Production actuelle d’engrais

Les trois PM de `pmg_fertilizer_production` sont mutuellement exclusifs et emploient chacun 5 000 personnes.

| PM | Verrou | Recette actuelle par niveau | Emploi | Pollution | Valeur intrants | Valeur sortie | Marge brute |
|---|---|---|---:|---:|---:|---:|---:|
| `pm_artificial_fertilizers` | bâtiment : `industrial_acids`; aucun verrou PM | 30 soufre + 10 fer + 5 sel → 90 engrais | 500/3 000/1 000/500 | 5 | £2 050 | £2 700 | £650 |
| `pm_improved_fertilizer` | `improved_fertilizer` | 30 soufre + 30 fer + 10 sel → 140 engrais | 500/2 000/1 500/1 000 | 10 | £3 000 | £4 200 | £1 200 |
| `pm_nitrogen_fixation` | `nitrogen_fixation` | 40 soufre + 20 produits chimiques + 30 fer + 20 sel → 200 engrais | 500/1 000/2 000/1 500 | 15 | £4 600 | £6 000 | £1 400 |

Ordre de l’emploi : commerçants / manœuvres / machinistes / ingénieurs. La progression de qualification est cohérente. En revanche, les intrants fer/sel/soufre sont des proxys qui ne distinguent ni roche phosphatée, ni nitrate naturel, ni énergie de la synthèse d’ammoniac.

### 3.3 Explosifs et munitions

| PM | Verrou | Recette actuelle | Emploi | Pollution |
|---|---|---|---:|---:|
| `pm_leblanc_process` | bâtiment : `industrial_acids` | 20 soufre + 20 engrais → 50 explosifs | 5 000 | 10 |
| `pm_ammonia-soda_process` | `nitroglycerin` | 30 soufre + 30 engrais + 10 papier → 80 explosifs | 5 000 | 15 |
| `pm_vacuum_evaporation` | `dynamite` | 40 soufre + 40 engrais + 20 papier → 110 explosifs | 5 000 | 20 |
| `pm_brine_electrolysis` | `electrical_capacitors` | 40 soufre + 50 engrais + 30 papier + 20 électricité → 150 explosifs | 5 000 | 25 |

Les noms hérités Leblanc, ammonia-soda, évaporation sous vide et électrolyse de saumure ne décrivent pas réellement les explosifs. Leur correction touche compatibilité, localisation, recettes, historique de départ et équilibre ; elle doit être faite ensemble en 6C, pas partiellement en 6B.

Les munitions consomment correctement le bien fini `explosives` :

- `pm_percussion_caps` : 20 explosifs + 20 plomb → 50 munitions ;
- `pm_explosive_shells` : 40 explosifs + 30 plomb → 90 munitions.

Les sept familles de mines (charbon, fer, plomb, soufre, or, sel, cuivre) utilisent également les explosifs finis pour leurs variantes nitroglycérine/dynamite. Aucun de ces consommateurs ne doit recevoir directement des nitrates.

### 3.4 Agriculture et autres consommateurs

Les quatre cultures céréalières génériques utilisent successivement 5, 10 et 15 engrais pour produire 30, 45 et 60 céréales ; les rizières, à double échelle, utilisent 10, 20 et 30 engrais pour 50, 75 et 100 céréales. Les verrous sont respectivement `advanced_crop_rotations`, `improved_fertilizer` et `nitrogen_fixation`.

Cette interface est déjà la bonne abstraction : une ferme achète un engrais formulé, tandis que le bâtiment d’engrais arbitre entre phosphate naturel, nitrate naturel et azote synthétique. Ajouter phosphates ou nitrates à six PM agricoles fragmenterait le marché et rendrait les routes industrielles contournables.

Autres constats :

- `pm_sheep_farms` et `pm_intensive_grazing_ranch` produisent respectivement 2,5 et 5 engrais comme sous-produit ; ils restent une petite source résiliente ;
- `pm_dye_production` consomme actuellement 30 engrais comme proxy chimique ; cette anomalie est à revoir avec la chaîne nitrates/explosifs, sans changement en 6B ;
- `mobilization_option_chemical_weapons` consomme `industrial_chemicals`, pas engrais ni explosifs : conserver ce choix TECH6C3 ;
- une seule usine d’engrais de départ a été trouvée en Brandebourg avec `pm_artificial_fertilizers`; les usines d’explosifs de départ françaises, prussiennes et américaines utilisent `pm_leblanc_process` ;
- aucun historique de PM séparé, trait régional phosphate/nitrate ou ressource correspondante n’existe actuellement.

La matrice exhaustive comprend **42 décisions** : 2 `IMPLEMENT_NEXT`, 8 `DEFER`, 27 `KEEP_UNCHANGED` et 5 `REJECT`.

## 4. Architecture phosphates retenue

### 4.1 Bien et extraction

Créer en 6B :

- bien brut industriel `phosphates`, prix de base préliminaire **£30** ;
- bâtiment plafonné dédié `building_phosphate_mine` ;
- groupe de base et PM d’extraction utilisant outils, 5 000 emplois et pollution minière ;
- verrou de bâtiment **`applied_mineralogy`** ;
- potentiel `building_phosphate_mine = N` dans les régions retenues après validation géographique.

Un bâtiment dédié est préférable à un PM dans une mine de soufre : les gisements ont une géographie propre, un plafond propre et doivent être visibles par l’IA et le marché. `geological_surveying` reste un soutien historique possible pour une amélioration ultérieure, mais l’utiliser comme verrou initial repousserait artificiellement une industrie déjà pertinente après `industrial_acids`.

Exemple d’extraction par niveau : **5 outils → 25 phosphates**, 5 000 emplois, pollution 5. Aux prix de base : intrants £200, sortie £750, marge brute **£550**, soit le benchmark de la mine de cuivre et très près de la mine de plomb.

### 4.2 Production d’engrais

Ne créer ni nouveau bâtiment ni nouveau PMG. Réutiliser :

- bâtiment : `building_chemical_plant` ;
- PMG : `pmg_fertilizer_production` ;
- capacité : un seul PM de base actif à la fois.

En 6B, reconfigurer exactement deux emplacements existants :

1. `pm_artificial_fertilizers`, route phosphatée de base, disponible avec le bâtiment ouvert par `industrial_acids` ;
2. `pm_improved_fertilizer`, route superphosphate améliorée, verrouillée par `improved_fertilizer`.

Recettes de calibration proposées :

| Route | Recette par niveau | Sortie | Emploi | Pollution | Marge brute |
|---|---|---:|---:|---:|---:|
| phosphate de base | 20 phosphates + 20 produits chimiques industriels + 10 charbon | 80 engrais | 5 000 | 10 | £700 |
| phosphate amélioré | 30 phosphates + 25 produits chimiques industriels + 15 charbon | 120 engrais | 5 000 | 15 | £1 250 |

Les marges sont calculées aux prix de base (phosphates £30, produits chimiques £40, charbon £30, engrais £30). Elles suivent de près les marges actuelles £650/£1 200, limitant le choc économique tout en donnant une demande réelle aux phosphates et à TECH6C3.

## 5. Architecture nitrates et Haber-Bosch différée

### 5.1 Nitrates naturels

Le bien `nitrates` est recommandé à terme, prix de base préliminaire **£40**, avec une mine plafonnée dédiée `building_nitrate_mine`. Sa rareté n’est pas un défaut : elle doit créer commerce, vulnérabilité stratégique et incitation à la substitution synthétique.

Architecture 6C proposée :

- verrou de la mine : `nitroglycerin` ;
- extraction indicative : **5 outils → 20 nitrates**, 5 000 emplois, pollution 5 ;
- marge brute indicative : £800 − £200 = **£600** ;
- route d’engrais naturelle : 20 nitrates + 20 produits chimiques + 10 charbon → 90 engrais, pollution 15, marge **£800** ;
- intégration coordonnée dans les PM d’explosifs, sans donner le bien brut aux mines ni aux usines de munitions.

Un PM universel « lits de salpêtre » est volontairement différé. Il ne doit être ajouté que si la bêta joueurs démontre que le commerce depuis l’Atacama échoue structurellement ; l’ajouter d’emblée supprimerait l’identité géopolitique du bien.

### 5.2 Substitution synthétique

`pm_nitrogen_fixation` est classé **REWORK_NEXT en TECH6C6C**. Le remplacement local temporaire de pétrole par `industrial_chemicals` est acceptable comme crochet, mais sa recette actuelle ne représente pas assez le coût énergétique et la pression du procédé.

Architecture Haber-Bosch :

- verrou existant : **`nitrogen_fixation`** ;
- aucun nitrate miné en entrée ; l’azote atmosphérique est implicite ;
- aucun bien intermédiaire « ammonia » supplémentaire ;
- proposition : 30 produits chimiques + 30 charbon + 50 électricité + 10 outils → 180 engrais ;
- 5 000 emplois avec davantage de machinistes/ingénieurs ; pollution indicative 20 ;
- valeur intrants £4 000, sortie £5 400, marge brute **£1 400**, identique à la marge actuelle.

Cette route devient le substitut industriel coûteux mais disponible mondialement qui affaiblit progressivement la rente du nitrate naturel.

## 6. Guano

**REJECT comme bien de marché.** Le guano a une importance historique réelle, mais un marché autonome serait trop étroit, aurait peu de consommateurs distincts et doublerait les rôles fonctionnels des phosphates/nitrates/engrais.

La dimension insulaire est mieux représentée par de petits potentiels de phosphate (`STATE_NAURU`, Micronésie, territoire de l’océan Indien) ou, si une future preuve le justifie, par un trait/événement ciblé. Aucun « Guano Works », PM ou nouveau bien n’est proposé pour 6B.

## 7. Stratégie technologique

**Aucune nouvelle technologie n’est nécessaire.** Le graphe existant contient déjà chaque porte utile et chacune débloque quelque chose :

| Étape | Porte existante |
|---|---|
| ouverture du bâtiment d’engrais et chimie acide | `industrial_acids` |
| mine de phosphate | `applied_mineralogy` |
| premier usage agricole | `advanced_crop_rotations` |
| route superphosphate améliorée | `improved_fertilizer` |
| future mine/route nitrate et premier explosif avancé | `nitroglycerin` |
| substitution Haber-Bosch | `nitrogen_fixation` |

`geological_surveying` reste un nœud de découverte/modernisation ; `dynamite` reste un nœud explosifs/mines. `intensive_agriculture` est explicitement rejeté comme verrou car l’objet de compatibilité a `can_research = no`. Aucun parent, enfant, ère ou modificateur technologique n’est à changer dans 6A.

## 8. Géographie préliminaire

### Phosphates

Une carte mondiale est requise. La matrice couvre les **675** États du fork : **45** candidats non nuls, potentiel total préliminaire **1 328**.

Échelle : 0 `NONE`, 8 `LOW`, 16 `MODEST`, 24 `MEDIUM`, 36 `HIGH`, 48 `VERY_HIGH`, 60 `WORLD_CLASS`.

Principaux pôles proposés : Maroc/Sahara occidental, Chine du Sud-Ouest, Floride–Caroline du Nord et Idaho, péninsule de Kola, Tunisie–Algérie, Égypte, Jordanie–Levant, nord saoudien, Brésil, Pérou, Afrique du Sud, Sénégal/Togo, Australie et quelques îles phosphatées. La distribution est volontairement plus large que celle des nitrates, mais reste plafonnée.

### Nitrates

Une carte séparée est requise car la rareté géographique est le cœur du bien. La matrice couvre les **675** États : seuls `STATE_TARAPACA` et `STATE_ANTOFAGASTA` reçoivent chacun **60**, total préliminaire **120**.

`STATE_CALIFORNIA` reste à 0 : des occurrences naturelles sont documentées vers Death Valley, mais l’audit ne trouve pas de preuve suffisante pour une industrie de même échelle que l’Atacama. Toutes les autres lignes restent également à 0. Cette carte est conçue pour 6C et ne doit pas être appliquée en 6B.

## 9. Économie et risques

Prix de base proposés, encore ajustables :

- `phosphates` : **£30** — minerai industriel pondéreux, offre mondiale relativement distribuée ;
- `nitrates` : **£40** — intrant stratégique concentré, mais moins transformé que `explosives` à £50.

Risques et garde-fous :

- **pénurie initiale** : distribuer un minimum de phosphate dans plusieurs grandes zones et vérifier que les historiques de départ peuvent construire la mine ;
- **Chemical Works non rentable** : la demande d’acide/produits chimiques par l’engrais devrait au contraire l’aider, mais les quantités doivent être testées ;
- **effondrement agricole** : conserver les niveaux de marge proches des recettes actuelles et ne pas déployer les nitrates dans le même lot ;
- **monopole nitrate injouable** : tester le commerce et l’IA en bêta avant d’envisager un PM traditionnel de secours ;
- **Haber-Bosch trop dominant** : coût élevé d’électricité/charbon/outils, pollution et verrou tardif ;
- **technologies vides** : aucun nouveau nœud ; tous les déblocages vont dans des technologies déjà peuplées.

## 10. Portée recommandée des implémentations

### TECH6C6B — lot suivant

**Titre exact proposé : `TECH6C6B — PHOSPHATE RESOURCE AND FERTILIZER PRODUCTION IMPLEMENTATION`**

Portée exacte :

- créer le bien `phosphates` et tout son support obligatoire (modificateurs, texticon, localisation EN/FR ; `gfx/error_deer.dds` si aucune icône DDS propre n’existe) ;
- créer `building_phosphate_mine`, son PMG et son PM de base, verrouillés par `applied_mineralogy` ;
- appliquer uniquement la carte phosphate après revue des 45 lignes non nulles ;
- reconfigurer `pm_artificial_fertilizers` et `pm_improved_fertilizer` dans `pmg_fertilizer_production` ;
- conserver le bâtiment `building_chemical_plant`, toutes les interfaces agricoles et TECH6C5 inchangés ;
- ajouter validation statique, matrice d’implémentation et smoke limité ;
- exclure nitrates, explosifs, Haber-Bosch, guano et toute nouvelle technologie.

### TECH6C6C — lot ultérieur prévu

- créer `nitrates` et la mine très concentrée de l’Atacama ;
- traiter ensemble routes nitrate d’engrais, recettes/noms d’explosifs et historiques de départ ;
- reconfigurer `pm_nitrogen_fixation` comme route Haber-Bosch sans nitrates ;
- valider commerce, adoption IA et substitution sur bêta joueurs.

## 11. Livrables et validation documentaire

Livrables :

- `TECH6C6A_PHOSPHATES_NITRATES_FERTILIZER_AUDIT.md` ;
- `TECH6C6A_FERTILIZER_CONSUMER_MATRIX.csv` ;
- `TECH6C6A_PHOSPHATE_NITRATE_TECH_AUDIT.csv` ;
- `TECH6C6A_PHOSPHATE_RESOURCE_CANDIDATES.csv` ;
- `TECH6C6A_NITRATE_RESOURCE_CANDIDATES.csv`.

Contrôles de clôture exécutés :

- **PASS** — les quatre CSV ont été importés et inspectés avec l’outil de tableur : 9/10 colonnes attendues selon la matrice, aucune rupture de ligne CSV ;
- **PASS** — 675 lignes et 675 `state_id` uniques dans chaque matrice de ressource, zéro État manquant par rapport à la matrice mondiale cuivre ;
- **PASS** — phosphates : 45 États non nuls, total 1 328 ; nitrates : 2 États non nuls, total 120 ;
- **PASS** — consommateurs : 42 lignes, actions autorisées uniquement, totaux 2/8/27/5 ;
- **PASS** — `git diff --check`, code retour 0 ; les avertissements LF/CRLF concernent des fichiers de gameplay déjà modifiés dans le worktree ;
- **PASS** — fichiers de gameplay changés par TECH6C6A : **0** ; seules les cinq sorties documentaires 6A et la note de clôture documentaire 5D ont été écrites ;
- **PASS** — aucune modification de topologie technologique, `map_data/state_regions`, support de bien personnalisé, localisation de gameplay ou GUI par cette phase.

Le worktree était déjà volontairement sale à l’ouverture de TECH6C6A à cause des implémentations TECH6C1–5. La sortie finale de `git status --short` est reproduite ci-dessous pour ne pas présenter ces changements antérieurs comme appartenant à 6A :

```text
 M common/buildings/01_industry.txt
 M common/buildings/11_tech6c1b_cement_works.txt
 M common/history/buildings/11_east_asia.txt
 M common/modifier_type_definitions/12_tech6c_custom_goods_modifier_types.txt
 M common/production_method_groups/01_industry.txt
 M common/production_method_groups/11_tech6c1b_cement_pmgs.txt
 M common/production_methods/01_industry.txt
 M common/production_methods/11_tech6c1b_cement_production.txt
 M common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt
 M gui/tech6c_goods_texticons.gui
 M localization/english/tech6c1b_portland_cement_l_english.yml
 M localization/english/tech6c_goods_modifiers_l_english.yml
 M localization/french/tech6c1b_portland_cement_l_french.yml
 M localization/french/tech6c_goods_modifiers_l_french.yml
 M map_data/state_regions/00_west_europe.txt
 M map_data/state_regions/01_south_europe.txt
 M map_data/state_regions/02_east_europe.txt
 M map_data/state_regions/03_north_africa.txt
 M map_data/state_regions/04_subsaharan_africa.txt
 M map_data/state_regions/05_north_america.txt
 M map_data/state_regions/06_central_america.txt
 M map_data/state_regions/07_south_america.txt
 M map_data/state_regions/08_middle_east.txt
 M map_data/state_regions/09_central_asia.txt
 M map_data/state_regions/10_india.txt
 M map_data/state_regions/11_east_asia.txt
 M map_data/state_regions/12_indonesia.txt
 M map_data/state_regions/13_australasia.txt
 M map_data/state_regions/14_siberia.txt
 M map_data/state_regions/15_russia.txt
?? common/buildings/06_urban_center.txt
?? common/buildings/13_tech6c5b_copper_mine.txt
?? common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt
?? common/goods/13_tech6c5b_copper.txt
?? common/goods/14_tech6c5c_aluminium.txt
?? common/production_method_groups/13_tech6c5b_copper_pmgs.txt
?? common/production_method_groups/14_tech6c5c_aluminium_pmgs.txt
?? common/production_methods/13_tech6c5b_copper_production_and_consumers.txt
?? common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt
?? common/state_traits/12_oceania_traits.txt
?? docs/reports/industry/TECH6C4_5_CEMENT_PROGRESSION_HOTFIX_REPORT.md
?? docs/reports/industry/TECH6C5A_COPPER_ALUMINIUM_INTEGRATION_MATRIX.csv
?? docs/reports/industry/TECH6C5A_NON_FERROUS_METALLURGY_AUDIT.md
?? docs/reports/industry/TECH6C5A_NON_FERROUS_RESOURCE_CANDIDATES.csv
?? docs/reports/industry/TECH6C5A_NON_FERROUS_TECH_AUDIT.csv
?? docs/reports/industry/TECH6C5B_COPPER_CONSUMER_IMPLEMENTATION_MATRIX.csv
?? docs/reports/industry/TECH6C5B_COPPER_ECONOMIC_VALIDATION.csv
?? docs/reports/industry/TECH6C5B_COPPER_GLOBAL_RESOURCE_MATRIX.csv
?? docs/reports/industry/TECH6C5B_COPPER_IMPLEMENTATION_REPORT.md
?? docs/reports/industry/TECH6C5C_ALUMINIUM_CONSUMER_MATRIX.csv
?? docs/reports/industry/TECH6C5C_ALUMINIUM_ECONOMIC_VALIDATION.csv
?? docs/reports/industry/TECH6C5C_ALUMINIUM_IMPLEMENTATION_REPORT.md
?? docs/reports/industry/TECH6C5D_COPPER_ALUMINIUM_RUNTIME_QA.md
?? docs/reports/industry/TECH6C5D_ECONOMIC_OBSERVATIONS.csv
?? docs/reports/industry/TECH6C5D_RUNTIME_TEST_MATRIX.csv
?? docs/reports/industry/TECH6C5D_USER_RUNTIME_CHECKLIST.md
?? docs/reports/industry/TECH6C6A_FERTILIZER_CONSUMER_MATRIX.csv
?? docs/reports/industry/TECH6C6A_NITRATE_RESOURCE_CANDIDATES.csv
?? docs/reports/industry/TECH6C6A_PHOSPHATES_NITRATES_FERTILIZER_AUDIT.md
?? docs/reports/industry/TECH6C6A_PHOSPHATE_NITRATE_TECH_AUDIT.csv
?? docs/reports/industry/TECH6C6A_PHOSPHATE_RESOURCE_CANDIDATES.csv
?? localization/english/tech6c5b_copper_l_english.yml
?? localization/english/tech6c5c_aluminium_l_english.yml
?? localization/french/tech6c5b_copper_l_french.yml
?? localization/french/tech6c5c_aluminium_l_french.yml
?? tools/tech6c5b_build_copper_distribution.py
?? tools/tech6c5b_validate.py
?? tools/tech6c5c_validate.py
?? tools/tech6c5d_validate.py
```

**Aucune validation runtime n’est revendiquée pour TECH6C6A.**
