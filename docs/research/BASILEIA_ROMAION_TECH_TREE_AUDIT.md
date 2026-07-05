# Audit de l'arbre technologique de Basileia Romaion 1736

## 1. Resume executif

Le mod possede bien un arbre technologique etendu. Ce n'est pas un simple paquet de quelques technologies ajoutees : l'arbre est restructure depuis un depart en 1736, les eres sont remplacees, les couts de recherche sont recalibres, une couche complete de technologies pre-1836 est ajoutee, et beaucoup de technologies vanilla sont reintegrees avec de nouveaux prerequis.

Verdict : **tres utile comme inspiration technique**, mais **utile partiellement comme source historique directe** pour un mod commencant en 1776.

Points principaux :

- Le mod cree 6 eres datees : 1736-1811, 1811-1836, 1836-1861, 1862-1886, 1887-1911, 1911-1936.
- Il ajoute environ 68 technologies ou pseudo-technologies nouvelles, dont 67 IDs `br_tech_*` et `tech_cavalry_specialization`.
- Il remplace/redefinit environ 179 technologies vanilla avec `REPLACE_OR_CREATE`, surtout pour deplacer les prerequis et les eras.
- Il ne semble pas ajouter d'ere apres 1936 ni d'arbre post-1936 ; la solution consiste plutot a etirer 1736-1936.
- L'arbre est tres pertinent pour 1776 sur les sujets agriculture, proto-industrie, voile, armes a feu du XVIIIe siecle, administration, fiscalite, Lumiere, colonisation et commerce.
- Une partie du contenu est specifique a l'uchronie byzantine ou aux bonus culturels/regionaux, donc a ne pas reprendre directement.

Conclusion courte : Basileia Romaion est une **bonne source secondaire majeure** pour concevoir l'arbre techno de `1776_Age_of_Revolutions_fork`, surtout pour la methode : ajouter une couche 1776-1836, retarder les technologies vanilla par prerequis, et augmenter les couts par eres. Ce n'est pas une source principale a copier.

## 2. Structure technique de l'arbre technologique

### Fichiers trouves

Fichiers technologiques :

- `common/technology/eras/00_eras.txt`
- `common/technology/technologies/br_production_1736-1836.txt`
- `common/technology/technologies/br_military_1736-1836.txt`
- `common/technology/technologies/br_society_1736-1836.txt`
- `common/technology/technologies/br_production_1836-1936.txt`
- `common/technology/technologies/br_military_1836-1936.txt`
- `common/technology/technologies/br_society_1836-1936.txt`
- `common/technology/technologies/br_unique_techs.txt`
- `common/technology/technologies/10_production.txt`
- `common/technology/technologies/20_military.txt`
- `common/technology/technologies/30_society.txt`

Les fichiers `10_production.txt`, `20_military.txt` et `30_society.txt` existent mais sont pratiquement vides dans cette copie. Les definitions actives sont dans les fichiers `br_*`.

Dossiers demandes mais absents :

- `common/technologies`
- `common/technology_eras`
- `common/technology_categories`

Dossiers lies aux deblocages :

- `common/production_methods/`
- `common/buildings/`
- `common/goods/`
- `common/laws/`
- `common/static_modifiers/`
- `common/modifier_type_definitions/`
- `common/scripted_triggers/`
- `common/scripted_effects/`
- `common/journal_entries/`
- `common/decisions/`
- `events/`
- `localization/`

### Emplacements fonctionnels

Les technologies sont definies dans `common/technology/technologies/*.txt`.

Les prerequis sont definis dans les blocs de technologies via :

```txt
unlocking_technologies = { ... }
```

Les couts ne sont pas definis technologie par technologie. Ils sont definis par ere dans `common/technology/eras/00_eras.txt` :

- `era_1` : 1736-1811, `technology_cost = 8500`
- `era_2` : 1811-1836, `technology_cost = 12000`
- `era_3` : 1836-1861, `technology_cost = 15000`
- `era_4` : 1862-1886, `technology_cost = 20000`
- `era_5` : 1887-1911, `technology_cost = 30000`
- `era_6` : 1911-1936, `technology_cost = 45000`

Les effets directs sont dans les blocs `modifier = { ... }` des technologies.

Les deblocages indirects sont dans :

- batiments : `common/buildings/br_building_*.txt`, `common/buildings/br_buildings_private_infrastructure.txt`
- methodes de production : `common/production_methods/br_pm_agro.txt`, `br_pm_industry.txt`, `br_mines.txt`, `br_pm_horses.txt`, `br_pm_embassy.txt`, `br_private_infrastucture_pms.txt`, `br_government.txt`
- lois : `common/laws/br_*.txt`
- technologies de depart : `common/scripted_effects/00_starting_inventions.txt`
- decisions et journal entries : `common/decisions/`, `common/journal_entries/`, `events/`

Localisation des technologies :

- principal : `localization/english/br_technology_l_english.yml`
- traductions correspondantes : `localization/french/br_technology_l_french.yml`, `localization/german/br_technology_l_german.yml`, `localization/spanish/br_technology_l_spanish.yml`, `localization/turkish/br_technology_l_turkish.yml`, `localization/russian/br_technology_l_russian.yml`, `localization/japanese/br_technology_l_japanese.yml`, `localization/korean/br_technology_l_korean.yml`, `localization/simp_chinese/br_technology_l_simp_chinese.yml`, etc.

## 3. Technologies ajoutees

Note : les couts sont par ere, pas par technologie. `era_1` coute 8500, `era_2` 12000, `era_3` 15000, `era_4` 20000, `era_5` 30000, `era_6` 45000.

### Production 1736-1836

| ID | Nom localise | Ere | Periode approx. | Prerequis | Suite principale | Effets / deblocages principaux | Fichier |
|---|---|---:|---|---|---|---|---|
| `br_tech_four_field_crop_rotation` | Four-Field Crop Rotation | 1 | avant 1700-18e | `enclosure` | `br_tech_seed_drill` | base agriculture preindustrielle | `br_production_1736-1836.txt` |
| `br_tech_new_world_crops` | New World Crops | 1 | 16e-18e | `enclosure` | `br_tech_plantation_system` | debloque notamment `building_maize_farm` | idem |
| `br_tech_plantation_system` | Plantation System | 1 | 17e-18e | `br_tech_new_world_crops` | `br_tech_selective_breeding` | plantations, economie coloniale | idem |
| `br_tech_seed_drill` | Seed Drill | 1 | debut 18e | `br_tech_four_field_crop_rotation` | `br_tech_rotherham_plough` | throughput agriculture/plantations +5% | idem |
| `br_tech_rotherham_plough` | Rotherham Plough | 1 | 18e | `br_tech_seed_drill` | `br_tech_horse_drawn_machinery` | PM agricoles | idem |
| `br_tech_selective_breeding` | Selective Breeding | 2 | 18e-debut 19e | `br_tech_plantation_system` | `br_tech_horse_drawn_machinery` | agriculture/plantations/ranching +5% | idem |
| `br_tech_horse_drawn_machinery` | Horse Drawn Machinery | 2 | 18e-19e | `br_tech_selective_breeding`, `br_tech_rotherham_plough` | `br_tech_standardized_farming`, `br_tech_track` | PM chevaux, transport, ranching | idem |
| `br_tech_standardized_farming` | Standardized Farming | 2 | debut 19e | `br_tech_horse_drawn_machinery` | `br_tech_organic_farming` | PM agricoles | idem |
| `br_tech_organic_farming` | Organic Farming | 2 | debut 19e | `br_tech_standardized_farming` | `intensive_agriculture` | PM agricoles | idem |
| `br_tech_artisan_manufacturing` | Artisan Manufacturing | 1 | avant 1700-18e | aucun | manufacturies vanilla | industries de base : textile, meubles, verre, papier, food | idem |
| `br_tech_murano_glass` | Murano Glass | 1 | avant 1700-18e | `br_tech_metallurgy` | `br_tech_leaded_glass` | PM verre | idem |
| `br_tech_leaded_glass` | Leaded Glassmaking | 2 | 18e | `br_tech_murano_glass` | `crystal_glass` | PM verre avance | idem |
| `br_tech_hand_tools` | Improved Hand Tools | 1 | avant 1700-18e | `br_tech_metallurgy`, `br_tech_standardized_measures` | `br_tech_experimental_construction` | debloque tooling workshop, PM mines | idem |
| `br_tech_standardized_measures` | Standardized Measures | 1 | 17e-18e | aucun | `br_tech_hand_tools` | tax capacity +10%, efficacite investment pool | idem |
| `br_tech_experimental_construction` | Improved Construction | 1 | 18e | `br_tech_hand_tools` | `manufacturies`, `shaft_mining` | max construction sector +5 | idem |
| `br_tech_textile_manufacturies` | Textile Manufacturies | 1 | 18e | `br_tech_artisan_manufacturing` | `br_tech_dye_workshops`, `manufacturies` | PM textile | idem |
| `br_tech_furniture_manufacturies` | Furniture Manufactories | 1 | 18e | `br_tech_artisan_manufacturing` | `br_tech_paper_manufacturies` | PM meubles | idem |
| `br_tech_paper_manufacturies` | Paper Manufactories | 1 | 18e | `br_tech_furniture_manufacturies` | `manufacturies` | PM papier | idem |
| `br_tech_dye_workshops` | Dye Workshops | 1 | 18e | `br_tech_textile_manufacturies` | `manufacturies` | PM textile/dye | idem |
| `br_tech_surface_mining` | Surface Mining | 1 | avant 1700-18e | aucun | `br_tech_metallurgy` | decouverte ressources +1% | idem |
| `br_tech_metallurgy` | Metallurgy | 1 | avant 1700-18e | `br_tech_surface_mining` | `br_tech_murano_glass`, `br_tech_hand_tools`, `br_tech_blast_furnaces` | mining throughput +5% | idem |
| `br_tech_blast_furnaces` | Blast Furnaces | 1 | 17e-18e | `br_tech_metallurgy` | `steelworking` | debloque steel mill | idem |
| `br_tech_newcomen_engine` | Newcomen Engine | 2 | debut 18e | `shaft_mining` | `atmospheric_engine` | mining throughput +5% | idem |
| `br_tech_track` | Track | 2 | 18e-debut 19e | `br_tech_horse_drawn_machinery` | `railways` | debloque railway / PM rail preindustriels | idem |

Technologies vanilla de production redeplacees dans ce fichier : `sericulture` et `enclosure`. `sericulture` est non recherchable (`can_research = no`) et `enclosure` devient une base agricole de l'arbre.

### Militaire 1736-1836

| ID | Nom localise | Ere | Periode approx. | Prerequis | Suite principale | Effets / deblocages principaux | Fichier |
|---|---|---:|---|---|---|---|---|
| `br_tech_military_levy` | Military Levy | 1 | avant 1700-18e | aucun | `br_tech_supply_train`, `br_tech_tech_hussar` | debloque barracks et loi militaire liee | `br_military_1736-1836.txt` |
| `br_tech_supply_train` | Supply Train | 1 | 17e-18e | `br_tech_military_levy` | `br_tech_lines_of_communication` | attrition -10%, supply consumption -10% | idem |
| `br_tech_lines_of_communication` | Lines of Communication | 1 | 18e | `br_tech_supply_train` | `standing_army` | organisation gain +10% | idem |
| `br_tech_tech_hussar` | Hussar | 1 | 16e-18e | `br_tech_military_levy` | `tech_cavalry_specialization` | cavalerie legere | idem |
| `tech_cavalry_specialization` | Cavalry Diversification | 1 | 18e-19e | `br_tech_tech_hussar` | `standing_army` | diversifie la cavalerie | idem |
| `br_tech_flintlock_musket` | Flintlock Musket | 1 | 17e-18e | `gunsmithing` | `line_infantry`, `percussion_cap` | debloque arms industry via fichiers batiments | idem |
| `br_tech_threadwheel_crane` | Threadwheel Crane | 1 | avant 1700 | aucun | `br_tech_standardized_shipbuilding` | ports / shipyards | idem |
| `br_tech_sextant` | Sextant | 1 | 18e | aucun | `navigation` | convoy defense +5% | idem |
| `br_tech_standardized_shipbuilding` | Standardized Shipbuilding | 1 | 17e-18e | `br_tech_threadwheel_crane` | `br_tech_frigate`, `br_tech_careening` | shipyards, naval administration | idem |
| `br_tech_frigate` | Frigate | 1 | 17e-18e | `br_tech_standardized_shipbuilding` | `br_tech_three_deckers` | navires a voile | idem |
| `br_tech_careening` | Careening | 1 | 17e-18e | `br_tech_standardized_shipbuilding` | `drydocks` | naval base throughput +5% | idem |
| `br_tech_three_deckers` | Three-Deckers | 2 | 18e-debut 19e | `br_tech_frigate` | `paddle_steamer` | transition vers vapeur navale | idem |
| `br_tech_naval_professionalization` | Naval Professionalization | 2 | 18e-19e | `navigation` | `admiralty` | naval base max +10, experience navale | `br_military_1836-1936.txt` |
| `br_tech_field_guns` | Field Guns | 2 | 18e-19e | `artillery` | `napoleonic_warfare`, `shell_gun` | kill rate +0.02 | idem |

Technologies vanilla deplacees dans ce segment : `gunsmithing`, `artillery`, `navigation`, puis beaucoup de technologies 1836-1936 (`standing_army`, `line_infantry`, `napoleonic_warfare`, etc.) sont raccordees a ces prerequis.

### Societe 1736-1836

| ID | Nom localise | Ere | Periode approx. | Prerequis | Suite principale | Effets / deblocages principaux | Fichier |
|---|---|---:|---|---|---|---|---|
| `br_tech_mercantilism` | Mercantilism | 1 | avant 1700-18e | aucun | `br_tech_agrarianism`, `br_tech_smithian_economics` | trade capacity +10%, lois commerciales | `br_society_1736-1836.txt` |
| `br_tech_public_sphere` | Public Sphere | 1 | 17e-18e | aucun | `br_tech_constabulary`, `br_tech_rights_of_man` | infra population, construction, urbanisation | idem |
| `br_tech_constabulary` | Constabulary | 1 | 17e-18e | `br_tech_public_sphere` | `br_tech_municipal_charter` | police institution +1 | idem |
| `br_tech_municipal_charter` | Municipal Charter | 1 | avant 1700-18e | `br_tech_constabulary` | `urbanization` | administration, government administration | idem |
| `br_tech_silver_standard` | Silver Standard | 1 | avant 1700-18e | aucun | `br_tech_smithian_economics` | interest rate -0.02, lois fiscales | idem |
| `br_tech_insurance_companies` | Insurance Companies | 2 | 18e-19e | `br_tech_smithian_economics` | `br_tech_mercantile_companies` | trade capacity +5%, company +1 | idem |
| `br_tech_mercantile_companies` | Mercantile Companies | 2 | 17e-19e | `br_tech_insurance_companies` | `international_trade` | free charter +1 | idem |
| `br_tech_agrarianism` | Agrarianism | 1 | 18e | `br_tech_mercantilism` | `br_tech_frontier_expansion` | lois economiques agrariennes | idem |
| `br_tech_frontier_expansion` | Frontier Expansion | 2 | 18e-19e | `br_tech_agrarianism` | `colonization` | colonial affairs +1 | idem |
| `br_tech_smithian_economics` | Smithian Economics | 1 | fin 18e | `br_tech_mercantilism`, `br_tech_silver_standard` | `br_tech_insurance_companies`, `br_tech_fiat_currency` | cash reserves +20%, market access impact | idem |
| `br_tech_early_modern_universities` | Early Modern Universities | 1 | avant 1700-18e | `br_tech_skepticism` | `br_tech_natural_history`, `academia` | education access, schools +1, innovation max +5 | idem |
| `br_tech_skepticism` | Skepticism | 1 | Lumieres | `br_tech_divine_right` | `br_tech_early_modern_universities`, `br_tech_rights_of_man`, `rationalism` | education / expected SoL from literacy | idem |
| `br_tech_divine_right` | Divine Right | 1 | avant 1700 | aucun | `br_tech_skepticism` | authority +10%, systeme ancien regime | idem |
| `br_tech_rights_of_man` | Rights of Man | 1 | fin 18e | `br_tech_skepticism`, `br_tech_public_sphere` | `br_tech_separation_of_powers` | education / SoL from literacy | idem |
| `br_tech_separation_of_powers` | Separation of Powers | 2 | fin 18e-debut 19e | `br_tech_rights_of_man` | `democracy` | prerequis lois constitutionnelles | idem |
| `br_tech_natural_history` | Natural History | 1 | 18e | `br_tech_early_modern_universities` | `academia` | innovation max +5 | idem |

### Technologies ajoutees apres 1836 ou uniques

| ID | Nom localise | Cat. | Ere | Type | Prerequis | Utilite 1776 |
|---|---|---|---:|---|---|---|
| `br_tech_fiat_currency` | Fiat Currency | society | 2 | ajout | `br_tech_smithian_economics` | utile comme transition monnaie/banque |
| `br_tech_constitutional_guarantees` | Constitutional Guarantees | society | 2 | ajout/remplacement | `democracy` | utile pour 1776-1836 si reecrit |
| `br_tech_administrative_formalization` | Administrative Formalization | society | 2 | ajout | `centralization`, `law_enforcement` | tres utile pour Etat moderne |
| `br_tech_hostile_climate_colonization` | Early Hostile Climate Colonization | society | 1 | unique non recherchable | aucun | inspiration seulement |
| `br_tech_greekfire` | Greekfire | military | 1 | unique non recherchable | aucun | inutilisable hors uchronie byzantine |
| `br_tech_defensive_military_bonus` | Defensive Ethos | military | 1 | unique non recherchable | aucun | inspiration mecanique, pas contenu |
| `br_tech_aggressive_military_bonus` | Offensive Ethos | military | 1 | unique non recherchable | aucun | inspiration mecanique, pas contenu |
| `br_tech_embassy` | Embassies | society | 3 | ajout | `central_archives` | utile pour diplomatie mais plus tardif ici |
| `br_tech_chinese_luxuries` | Chinese Luxuries | production | 1 | unique non recherchable | aucun | bonus regional, peu reutilisable |
| `br_tech_japanese_luxuries` | Japanese Luxuries | production | 1 | unique non recherchable | aucun | bonus regional, peu reutilisable |
| `br_tech_indian_luxuries` | Indian Luxuries | production | 1 | unique non recherchable | aucun | bonus regional, peu reutilisable |
| `br_tech_indonesia_spices` | Indonesian Spices and Dyes | production | 1 | unique non recherchable | aucun | commerce colonial, inspiration |
| `br_tech_steppe_horses` | Steppe Horse Traditions | production | 1 | unique non recherchable | aucun | inspiration pour traditions militaires/regionales |
| `br_tech_english_fabric` | English Woolen Boom | production | 1 | unique non recherchable | aucun | inspiration pour bonus regional |

## 4. Technologies vanilla modifiees

Le mod modifie fortement les technologies vanilla. Il utilise `REPLACE_OR_CREATE` pour reposer presque tout l'arbre vanilla 1836-1936 sur une base 1736-1836.

Modifications observees :

- `sericulture`, `enclosure`, `gunsmithing`, `artillery`, `navigation` sont deplaces en `era_1`.
- `standing_army`, `line_infantry`, `mandatory_service`, `military_drill`, `admiralty`, `drydocks`, `paddle_steamer`, etc. sont deplaces ou branches sur les nouvelles technologies militaires.
- `manufacturies`, `shaft_mining`, `steelworking`, `intensive_agriculture`, `atmospheric_engine`, `railways`, etc. dependent de technologies preindustrielles ajoutees.
- `urbanization`, `rationalism`, `tech_bureaucracy`, `currency_standards`, `democracy`, `international_trade`, `centralization`, `colonization`, `academia`, etc. sont raccordees a la couche sociale pre-1836.
- Les technologies des eres 3 a 6 restent globalement 1836-1936, mais avec des prerequis plus longs et des couts d'ere plus eleves.

Effet global :

- progression ralentie par couts d'ere ;
- progression ralentie par chaines de prerequis ;
- acces vanilla 1836 retarde par une couche 1736-1836 ;
- pas d'extension post-1936 substantielle ;
- pas de simple "inflation" uniforme des couts : la refonte est structurelle.

## 5. Organisation par periodes

### Avant 1700

Technologies pertinentes :

- `br_tech_divine_right`
- `br_tech_military_levy`
- `br_tech_threadwheel_crane`
- `br_tech_surface_mining`
- `br_tech_metallurgy`
- `br_tech_artisan_manufacturing`
- `br_tech_municipal_charter`
- `br_tech_mercantilism`
- `enclosure`

Utilite pour 1776 : utile surtout comme prerequis de depart. Pour un mod 1776, la plupart devraient etre deja connues par les Etats centralises, pas a rechercher partout.

### 1700-1776

Technologies pertinentes :

- `br_tech_seed_drill`
- `br_tech_rotherham_plough`
- `br_tech_new_world_crops`
- `br_tech_plantation_system`
- `br_tech_flintlock_musket`
- `br_tech_sextant`
- `br_tech_frigate`
- `br_tech_careening`
- `br_tech_public_sphere`
- `br_tech_skepticism`
- `br_tech_silver_standard`
- `br_tech_early_modern_universities`

Utilite pour 1776 : tres utile. Ce sont les meilleurs exemples pour une couche pre-revolution industrielle.

### 1776-1836

Technologies pertinentes :

- `br_tech_rights_of_man`
- `br_tech_separation_of_powers`
- `br_tech_smithian_economics`
- `br_tech_insurance_companies`
- `br_tech_mercantile_companies`
- `br_tech_selective_breeding`
- `br_tech_horse_drawn_machinery`
- `br_tech_standardized_farming`
- `br_tech_organic_farming`
- `br_tech_newcomen_engine`
- `br_tech_track`
- `br_tech_three_deckers`
- `br_tech_naval_professionalization`
- `br_tech_field_guns`
- `tech_cavalry_specialization`

Utilite pour 1776 : excellente. C'est la periode la plus directement exploitable.

### 1836-1900

Technologies pertinentes :

- technologies vanilla redecalees des eras 3 et 4 : `napoleonic_warfare`, `railways`, `atmospheric_engine`, `steelworking`, `colonization`, `nationalism`, `pharmaceuticals`, etc.

Utilite pour 1776 : utile comme cible a retarder. Le mod montre comment ne pas donner trop vite les technologies 1836 a des pays qui commencent 60 ans plus tot.

### 1900-1936

Technologies pertinentes :

- `trench_works`, `automatic_machine_guns`, `dreadnought_tech`, `military_aviation`, `mobile_armor`, `mass_propaganda`, `antibiotics`, etc.

Utilite pour 1776 : utile seulement pour calibrer la fin de partie. Pas d'inspiration pre-1836.

### Apres 1936

Je n'ai pas trouve de veritable extension post-1936. L'arbre finit toujours dans une logique 1911-1936.

Utilite pour 1776 : faible si le probleme est d'ajouter du contenu tardif ; forte si le probleme est de ralentir et etirer 1776-1936.

### Uchronique / specifique a Basileia Romaion

Technologies :

- `br_tech_greekfire`
- `br_tech_defensive_military_bonus`
- `br_tech_aggressive_military_bonus`
- bonus de luxes regionaux : `br_tech_chinese_luxuries`, `br_tech_japanese_luxuries`, `br_tech_indian_luxuries`, `br_tech_indonesia_spices`, `br_tech_steppe_horses`, `br_tech_english_fabric`

Utilite pour 1776 : faible comme contenu, mais utile comme technique de technologies non recherchables accordees par histoire, decision ou script.

## 6. Deblocages associes

### Batiments

Exemples importants :

- `br_tech_artisan_manufacturing` debloque plusieurs industries de base : food industry, textile mill, furniture manufactory, glassworks, paper mill.
- `br_tech_hand_tools` debloque `building_tooling_workshop`.
- `br_tech_blast_furnaces` debloque `building_steel_mill`.
- `br_tech_threadwheel_crane` debloque `building_shipyard` et `building_port`.
- `br_tech_standardized_shipbuilding` debloque `building_military_shipyard` et `building_naval_administration`.
- `br_tech_flintlock_musket` debloque `building_arms_industry`.
- `artillery` debloque `building_artillery_foundry`.
- `br_tech_military_levy` debloque `building_barrack`.
- `br_tech_municipal_charter` debloque `building_government_administration`.
- `br_tech_early_modern_universities` debloque `building_university`.
- `br_tech_embassy` debloque `building_embassy`.
- `br_tech_track` debloque `building_railway`.
- `br_tech_new_world_crops` debloque `building_maize_farm`.

### Methodes de production

Fichiers principaux :

- `common/production_methods/br_pm_agro.txt`
- `common/production_methods/br_pm_industry.txt`
- `common/production_methods/br_mines.txt`
- `common/production_methods/br_pm_horses.txt`
- `common/production_methods/br_pm_embassy.txt`
- `common/production_methods/br_private_infrastucture_pms.txt`
- `common/production_methods/br_government.txt`

Exemples :

- `br_tech_four_field_crop_rotation`, `br_tech_rotherham_plough`, `br_tech_selective_breeding`, `br_tech_horse_drawn_machinery`, `br_tech_organic_farming` debloquent des PM agricoles.
- `br_tech_hand_tools` debloque des PM de mines.
- `br_tech_textile_manufacturies`, `br_tech_dye_workshops`, `br_tech_furniture_manufacturies`, `br_tech_paper_manufacturies`, `br_tech_murano_glass`, `br_tech_leaded_glass`, `br_tech_blast_furnaces`, `br_tech_standardized_shipbuilding` debloquent des PM industriels.
- `br_tech_track` debloque plusieurs PM de transport a cheval/rail.
- Les technologies vanilla redecalees continuent de debloquer leurs PM vanilla, mais plus tard dans la chaine.

### Lois et institutions

Fichiers principaux :

- `common/laws/br_army_model.txt`
- `common/laws/br_church_and_state.txt`
- `common/laws/br_economic_system.txt`
- `common/laws/br_education_system.txt`
- `common/laws/br_colonial_affairs.txt`
- `common/laws/br_free_speech.txt`
- `common/laws/br_governance_principles.txt`
- `common/laws/br_land_reform.txt`
- `common/laws/br_distribution_of_power.txt`
- `common/laws/br_policing.txt`
- `common/laws/br_health_system.txt`
- `common/laws/br_taxation.txt`
- `common/laws/br_trade_policy.txt`

Exemples :

- `br_tech_military_levy` et `standing_army` servent a debloquer des lois militaires.
- `br_tech_skepticism` intervient dans `br_church_and_state.txt`.
- `br_tech_artisan_manufacturing`, `br_tech_agrarianism`, `br_tech_smithian_economics` interviennent dans les systemes economiques.
- `br_tech_divine_right` et `br_tech_early_modern_universities` interviennent dans l'education.
- `br_tech_frontier_expansion` intervient dans les affaires coloniales.
- `br_tech_public_sphere` intervient dans la liberte d'expression.
- `br_tech_separation_of_powers` intervient dans les principes de gouvernance et la distribution du pouvoir.
- `br_tech_constabulary` intervient dans la police.
- `br_tech_natural_history` intervient dans la sante.
- `br_tech_silver_standard` intervient dans la taxation.
- `br_tech_mercantilism` intervient dans la politique commerciale.

### Evenements, journal entries, decisions

Les technologies vanilla modifiees comme `nationalism`, `pan-nationalism`, `centralization`, `civilizing_mission`, `organized_sports`, `power_of_the_purse`, `screw_frigate`, `napoleonic_warfare` apparaissent dans des decisions, journal entries et evenements.

Les technologies `br_tech_*` servent surtout :

- a initialiser les pays via `common/scripted_effects/00_starting_inventions.txt` ;
- a debloquer des batiments, PM et lois ;
- a donner des bonus speciaux non recherchables selon les pays/regions.

## 7. Dependances internes

Dependance a l'uchronie byzantine :

- faible pour l'architecture generale de l'arbre ;
- moyenne pour certains batiments, decisions, journal entries ;
- forte pour `br_tech_greekfire`, les bonus militaires ethos et certains contenus Basileia/Romaion.

Dependance aux batiments et PM :

- forte. L'arbre ne vit pas seulement dans `common/technology`; il est raccorde aux batiments vanilla injectes/remplaces et a de nombreuses PM.
- Pour reutiliser l'arbre, il faut au minimum reecrire les deblocages de batiments et PM.

Dependance aux goods :

- moderee. Les bonus uniques touchent des biens (`porcelain`, `tea`, `silk`, `spices`, `dye`, `horse`, `fabric`, etc.).
- Le gros de l'arbre 1736-1836 reste reutilisable sans goods totalement nouveaux.

Dependance aux lois :

- forte pour la partie societe. Les technologies sociales sont utiles parce qu'elles debloquent des lois ou institutions refaites.

Dependance aux journal entries :

- faible a moyenne pour l'arbre pre-1836 lui-meme ;
- plus forte pour le contenu national/byzantin et les evenements de modernisation.

Dependance au Community Mod Framework :

- le mod contient un systeme de detection/alerte `Missing Community Mod Framework` et beaucoup de fichiers `eocfm_*`.
- L'arbre technologique pre-1836 semble comprehensible sans CMF, mais le mod complet depend de ces systemes religieux/GUI.
- Pour un mod 1776, il vaut mieux extraire l'idee d'architecture techno plutot que reprendre les dependances GUI/CMF.

Dependance GUI :

- pas necessaire pour comprendre l'arbre techno ;
- importante pour les systemes religieux EOCFM, mais non centrale au probleme "on finit l'arbre trop vite".

## 8. Utilite pour le mod 1776

### A. Directement utiles pour 1776

- Technologies agricoles : `br_tech_seed_drill`, `br_tech_rotherham_plough`, `br_tech_selective_breeding`, `br_tech_horse_drawn_machinery`, `br_tech_standardized_farming`.
- Proto-industrie : `br_tech_artisan_manufacturing`, `br_tech_textile_manufacturies`, `br_tech_furniture_manufacturies`, `br_tech_paper_manufacturies`, `br_tech_dye_workshops`, `br_tech_murano_glass`, `br_tech_leaded_glass`.
- Mines et metallurgie : `br_tech_surface_mining`, `br_tech_metallurgy`, `br_tech_blast_furnaces`, `br_tech_newcomen_engine`.
- Construction et infrastructure : `br_tech_hand_tools`, `br_tech_standardized_measures`, `br_tech_experimental_construction`, `br_tech_track`.
- Militaire : `br_tech_flintlock_musket`, `br_tech_field_guns`, `br_tech_supply_train`, `br_tech_lines_of_communication`, `tech_cavalry_specialization`.
- Naval : `br_tech_sextant`, `br_tech_standardized_shipbuilding`, `br_tech_frigate`, `br_tech_careening`, `br_tech_three_deckers`, `br_tech_naval_professionalization`.
- Societe/Lumieres : `br_tech_public_sphere`, `br_tech_skepticism`, `br_tech_rights_of_man`, `br_tech_separation_of_powers`, `br_tech_early_modern_universities`, `br_tech_natural_history`.
- Economie et Etat : `br_tech_mercantilism`, `br_tech_silver_standard`, `br_tech_smithian_economics`, `br_tech_insurance_companies`, `br_tech_mercantile_companies`, `br_tech_administrative_formalization`.

### B. Utiles comme inspiration mais a reecrire

- La structure en deux eres pre-1836 : 1736-1811 et 1811-1836.
- La methode `REPLACE_OR_CREATE` pour raccorder vanilla a des prerequis plus anciens.
- Le systeme de technologies de depart par tiers dans `00_starting_inventions.txt`.
- Les couts d'ere croissants.
- Les technologies non recherchables accordees par script, utiles pour traditions regionales.
- Les deblocages progressifs de batiments/PM, surtout industries, ports, mines et administrations.
- Les lois anciennes regime/reformes qui donnent du contenu avant la democratie vanilla.

### C. Peu utiles ou inutilisables

- `br_tech_greekfire`, trop byzantin.
- Les bonus `Defensive Ethos` / `Offensive Ethos` s'ils sont repris comme contenu, mais utiles comme idee de tradition militaire.
- Les bonus regionaux de luxes si copies tels quels.
- Les systemes EOCFM/orthodoxes/GUI.
- Les journal entries nationaux byzantins, HRE, Tartaria, etc.
- Les noms et textes localises directement issus du mod.

## 9. Reponse au probleme "on finit l'arbre trop tot"

Basileia Romaion resout le probleme par plusieurs leviers :

1. Ajout de technologies pre-1836.
2. Remplacement des eres vanilla par 6 eres datees de 1736 a 1936.
3. Augmentation des couts par ere, notamment 30000 en 1887-1911 et 45000 en 1911-1936.
4. Deplacement des prerequis vanilla vers une couche preindustrielle.
5. Nouveaux batiments et PM intermediaires.
6. Technologies de depart par tiers, pour eviter que tous les pays commencent au meme niveau.

Le mod ne semble pas resoudre le probleme par une vraie extension apres 1936. Il etire plutot le parcours entre 1736 et 1936.

Methode la plus adaptee a un mod 1776 :

- Ajouter une ere 1776-1815 et une ere 1815-1836.
- Donner aux pays avances une partie de la premiere ere via effets de depart.
- Retarder les technologies vanilla 1836 en les faisant dependre d'une ou deux technologies 1776-1836.
- Augmenter les couts d'ere avec moderation, surtout apres 1860.
- Eviter d'ajouter trop de technologies vides : chaque technologie 1776-1836 devrait debloquer au moins un PM, un batiment, une loi, un bonus ou un choix historique.

## 10. Proposition originale pour `1776_Age_of_Revolutions_fork`

### Structure proposee

Eres :

- `era_0` ou `era_1a` : 1776-1815, Age of Revolutions.
- `era_1b` : 1815-1836, Restoration and Early Industrial Transition.
- Puis reprendre les eres vanilla ou les decaler : 1836-1860, 1860-1885, 1885-1910, 1910-1936.

### Technologies 1776-1836 a ajouter

Production :

- `aor_crop_rotation`
- `aor_seed_drill`
- `aor_improved_ploughs`
- `aor_selective_breeding`
- `aor_proto_industrial_workshops`
- `aor_textile_putting_out_system`
- `aor_water_frame`
- `aor_coke_smelting`
- `aor_atmospheric_pumping_engines`
- `aor_turnpike_trusts`
- `aor_wagonways`
- `aor_standard_weights_measures`

Militaire :

- `aor_flintlock_standardization`
- `aor_regimental_drill`
- `aor_artillery_reforms`
- `aor_military_academies`
- `aor_staff_work`
- `aor_logistics_corps`
- `aor_light_infantry_doctrine`
- `aor_cavalry_screening`
- `aor_mass_conscription`
- `aor_napoleonic_operational_art`

Naval :

- `aor_age_of_sail_dockyards`
- `aor_frigate_doctrine`
- `aor_ship_of_the_line`
- `aor_copper_sheathing`
- `aor_celestial_navigation`
- `aor_naval_professionalization`
- `aor_blockade_doctrine`
- `aor_global_convoy_system`

Societe / politique :

- `aor_enlightenment_public_sphere`
- `aor_natural_rights`
- `aor_written_constitutions`
- `aor_separation_of_powers`
- `aor_revolutionary_nationalism`
- `aor_conservative_restoration`
- `aor_public_education_reform`
- `aor_statistical_bureaus`
- `aor_police_prefectures`
- `aor_fiscal_military_state`

Economie / commerce :

- `aor_mercantile_companies`
- `aor_colonial_preferences`
- `aor_smithian_political_economy`
- `aor_public_debt_markets`
- `aor_excise_administration`
- `aor_land_tax_surveys`
- `aor_insurance_markets`
- `aor_early_banking_networks`

### Technologies vanilla a retarder

- `railways` devrait dependre de `aor_wagonways` et d'une technologie vapeur.
- `line_infantry` devrait dependre de `aor_flintlock_standardization`.
- `napoleonic_warfare` devrait dependre de `aor_regimental_drill`, `aor_artillery_reforms` et `aor_mass_conscription`.
- `colonization` devrait dependre de `aor_colonial_preferences` ou `aor_global_convoy_system`.
- `democracy` devrait dependre de `aor_written_constitutions` et `aor_separation_of_powers`.
- `stock_exchange` devrait dependre de `aor_public_debt_markets` ou `aor_insurance_markets`.
- `academia` devrait dependre de `aor_public_education_reform` ou `aor_enlightenment_public_sphere`.
- `manufacturies` devrait dependre de `aor_proto_industrial_workshops`.
- `intensive_agriculture` devrait dependre de `aor_selective_breeding` et `aor_improved_ploughs`.

### Methode anti-fin trop rapide

- Ajouter 30 a 45 technologies entre 1776 et 1836, pas 100.
- Donner a la plupart des grandes puissances 50-70% des techs 1776 deja recherchees, selon leur profil.
- Ne pas donner automatiquement les techs 1815-1836 aux pays avances ; elles doivent occuper les 20-40 premieres annees.
- Augmenter les couts d'ere d'environ 10-20% par rapport a vanilla, puis ajuster par test.
- Ajouter des prerequis croises raisonnables entre militaire, economie et societe pour les technologies clefs.
- Ajouter des PM intermediaires faibles mais utiles pour que la periode 1776-1836 ait une vraie jouabilite.
- Eviter les bonus plats excessifs : preferer deblocages et choix de PM.

## 11. Risques legaux et ethiques

Il ne faut pas copier directement les fichiers de Basileia Romaion sans autorisation explicite ou licence compatible.

Peuvent servir d'inspiration :

- l'idee d'une couche 1776-1836 ;
- le principe de couts par ere ;
- la methode de prerequis intermediaires ;
- le principe de technologies de depart par tiers ;
- les grandes categories historiques : agriculture amelioree, proto-industrie, navigation a voile, Lumieres, fiscalite, administration, academies militaires.

Seraient trop proches d'une copie directe :

- reprendre les IDs `br_tech_*` tels quels ;
- copier les fichiers `br_*` ;
- copier les textes de localisation ;
- copier les chaines exactes de prerequis ;
- copier les bonus chiffres/PM/batiments a l'identique ;
- reprendre les contenus uchroniques propres a Basileia Romaion.

Si le mod s'inspire fortement de Basileia Romaion, il faut credit clairement dans la page du mod, par exemple : inspiration conceptuelle pour l'organisation d'un arbre pre-1836, sans reutilisation directe de fichiers. Si du code ou des assets sont reutilises, obtenir une permission ecrite et citer la licence/autorisation.

## 12. Conclusion finale

Basileia Romaion est une bonne source principale pour comprendre **comment** etendre un arbre Victoria 3 vers une date de depart anterieure a 1836. En revanche, ce n'est pas une bonne source principale pour le contenu final d'un mod 1776, car une partie du contenu est liee a son uchronie, ses lois, ses batiments, ses PM et ses systemes religieux.

Il faut plutot l'utiliser comme source secondaire forte :

- excellent pour la structure ;
- excellent pour les prerequis ;
- excellent pour l'idee de deux eres pre-1836 ;
- tres bon pour l'agriculture, la proto-industrie, la marine a voile, l'administration et les Lumieres ;
- moins bon pour le contenu byzantin, les bonus speciaux et les systemes dependants du reste du mod.

Je recommande de chercher au moins un autre mod ou une autre source historique en complement, idealement un mod 1789/1815/early industrialization ou une refonte vanilla centrée sur la progression technologique, puis de construire un arbre original pour `1776_Age_of_Revolutions_fork`.

Prochaine etape recommandee :

1. Definir les eres 1776-1815 et 1815-1836.
2. Lister 10-15 technologies par categorie maximum.
3. Choisir quelles technologies vanilla 1836 doivent etre retardees.
4. Creer un prototype minimal : technologies, couts d'ere, prerequis, quelques PM/batiments/lois.
5. Tester 50 ans de campagne avec une grande puissance, une puissance moyenne et un pays non reconnu.

