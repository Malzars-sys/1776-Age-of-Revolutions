# TECH6A-1 — Audit de référence sel : La Gabelle

Statut : `PASS` · type de travail : `AUDIT / RECHERCHE UNIQUEMENT` · date : `2026-08-26`.

## Périmètre et méthode

Le contenu installé de La Gabelle a été lu directement et récursivement. Le comparateur a été lu directement dans `C:/Games/Victoria 3/game`, dont l’installation porte le marqueur `v1.13.9.xxh128`. Les anciens rapports du dépôt ont servi seulement de contrôle secondaire; les nombres et conclusions ci-dessous ont été recalculés depuis les fichiers actuels.

Aucun fichier de gameplay, fichier vanilla ou fichier de La Gabelle n’a été modifié. Les quatre seuls fichiers créés sont les rapports TECH6A-1 sous `docs/reports/technology/`.

## Installation locale

`LA_GABELLE_LOCAL_INSTALLATION = FOUND`

| Champ | Valeur vérifiée |
|---|---|
| Chemin | `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3715913236` |
| Workshop ID | `3715913236`, confirmé par le dossier et `appworkshop_529340.acf` |
| ID interne | `top.sleepingbed.la_gabelle` |
| Nom | `La Gabelle` |
| Version | `1.0.2` |
| Version de jeu annoncée | `1.13.*` |
| Métadonnées locales | `.metadata/metadata.json` |
| Mise à jour Steam déclarée | Unix `1778330418`, soit `2026-05-09 12:40:18Z` |
| Horodatage des fichiers locaux | `2026-08-21 19:40` heure locale |
| État du dernier chargement | non activé : `content_load.json` active seulement le dépôt 1776 et contient `enabledUGC: []` |

Une seule copie a été trouvée. `libraryfolders.vdf` ne déclare qu’une bibliothèque Steam, `C:/Program Files (x86)/Steam`. Les emplacements vérifiés sont :

- `C:/Program Files (x86)/Steam/steamapps/workshop/content/529340`;
- `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod`;
- `C:/Program Files/Steam/steamapps/workshop/content/529340` (absent);
- `C:/Games/Steam/steamapps/workshop/content/529340` (absent);
- `D:/SteamLibrary/steamapps/workshop/content/529340` (absent);
- `E:/SteamLibrary/steamapps/workshop/content/529340` (absent).

Le nom d’auteur n’est pas présent dans les métadonnées locales. Il n’est pas déduit de l’ID interne.

## Architecture réellement observée

```text
change_resource_potential visible
  -> building_salt_pan | building_salt_mine
  -> 5 PMG
  -> 7 PM définis pour produire le sel + 5 PM vanilla réutilisés
  -> good salt
  -> 10 PM vanilla injectés comme consommateurs
  -> 2 pop needs + 2 options de mobilisation
  -> taxes, compagnies, prestige good, JE et événements
```

La Gabelle ne contient aucun fichier `map_data`, aucun `undiscovered_amount`, aucun `discovered_amount`, aucun `depleted_type`, aucun `force_resource_discovery`, aucun effet scripté de découverte et aucun hook `on_resource_discovered`. Toute sa géographie est visible dès le setup.

## Good `salt`

Source : `common/goods/lagab_goods.txt:1-10`.

| Propriété | Valeur |
|---|---|
| ID | `salt` |
| texture | `gfx/interface/icons/goods_icons/salt.dds` |
| cost | `30` |
| category | `staple` |
| prestige_factor | `5` |
| traded_quantity | `10` |
| consumption_tax_cost | `200` |
| convoy_cost_multiplier | `0.5` |
| tradeable | omis, donc comportement tradable par défaut |
| local | omis, donc non local par défaut |
| fixed_price | omis, donc prix non fixe par défaut |
| obsession/taboo | aucun |

Les mêmes champs et catégories sont utilisés dans `vanilla/common/goods/00_goods.txt`, notamment les exemples staple à partir de la ligne 85 et les champs de commerce/taxe jusqu’aux lignes 95-110.

`GOOD_SCHEMA_1_13_9_COMPATIBLE = YES`

Le rôle `category = staple` n’impose pas à lui seul un besoin POP; ce sont les injections de `pop_needs` qui le font.

## Bâtiments

| ID | Nom EN / FR | Structure | Construction et propriété | PMG | Analogue vanilla |
|---|---|---|---|---|---|
| `building_salt_mine` | Salt Mines / Mines de sel | `bg_mining`; `city_type = mine`; `terrain_manipulator = mining`; 50 niveaux/mesh | `construction_cost_medium`; `ownership_type = self`; porte `shaft_mining` | équipement, explosifs, steam automation, train automation | mine plafonnée classique, proche des mines de `common/buildings/03_mines.txt` |
| `building_salt_pan` | Salt Pans / Marais salant | `bg_mining`; `city_type = port`; condition `is_sea_adjacent = yes`; 1 niveau/mesh | `construction_cost_medium`; `ownership_type = self`; aucune technologie | base unique | hybride ressource côtière/misc; aucun analogue exact; visuels de pêche mais sémantique `bg_mining` |

Les deux bâtiments héritent de `bg_mining` une consommation d’infrastructure de `2` par niveau, l’auto-expansion vanilla, `economy_of_scale_ai_factor = 3` et `foreign_investment_ai_factor = 1`. Aucun `ai_value` explicite n’est défini. Ils sont plafonnés par ressources via le parent `bg_extraction`; ils ne consomment pas d’arable land. La Gabelle ne définit ni découverte ni épuisement pour eux.

Point critique : `bg_mining` n’a pas `discoverable_resource = yes`. Le bâtiment mine est compatible comme ressource visible, mais pas comme ressource cachée native sans adaptation de groupe.

## Chaîne PM/PMG des producteurs

`SALT_PMG_FOUND = 5`. Les PMG sont tous de nouveaux IDs La Gabelle.

| Bâtiment / PMG | PM | Gate | Entrées | Sorties / emploi significatif | Origine |
|---|---|---|---|---|---|
| mine / équipement | `pm_picks_and_shovels_building_salt_mine` | aucune | tools 2 | salt 20; 500 shopkeepers; 4,500 laborers | nouveau |
| mine / équipement | `pm_atmospheric_engine_pump_building_salt_mine` | `atmospheric_engine` | tools 5; coal 10 | salt 35; 500/3,750/500/250; pollution 5 | nouveau |
| mine / équipement | `pm_condensing_engine_pump_building_salt_mine` | `watertube_boiler` | tools 10; coal 15 | salt 45; 500/3,000/1,000/500; pollution 15 | nouveau |
| mine / équipement | `pm_diesel_pump_building_salt_mine` | `compression_ignition` | tools 10; oil 5 | salt 55; 500/2,250/1,500/750; pollution 10 | nouveau |
| mine / explosifs | `pm_no_explosives` | aucune | aucune | aucun delta | vanilla réutilisé, `03_mines.txt:114` |
| mine / explosifs | `pm_nitroglycerin_building_salt_mine` | `nitroglycerin` | explosives 5 | salt +15; engineers +250; pollution 5; mortalité accrue | nouveau |
| mine / explosifs | `pm_dynamite_building_salt_mine` | `dynamite` | explosives 10 | salt +20; engineers +250; pollution 10 | nouveau |
| mine / vapeur | `pm_no_steam_automation` | aucune | aucune | aucun delta | vanilla réutilisé, `03_mines.txt:179` |
| mine / vapeur | `pm_steam_donkey_mine` | `steam_donkey` | engines 1; coal 4 | laborers -1,000; pollution 5 | vanilla réutilisé, `03_mines.txt:391` |
| mine / transport | `pm_road_carts` | aucune | aucune | aucun delta | vanilla réutilisé, `03_mines.txt:213` |
| mine / transport | `pm_rail_transport_mine` | `railways` | transportation 5 | laborers -1,000; pollution 10 | vanilla réutilisé, `03_mines.txt:420` |
| saline / base | `default_building_salt_pan` | aucune | aucune | salt 10; 500 shopkeepers; 2,000 laborers | nouveau |

La propriété reste celle du bâtiment (`ownership_type = self`); aucun PMG de propriété spécifique n’est ajouté. Aucun PM ne contient de modificateur AI propre.

Comptage : 7 définitions de PM producteurs nouvelles, 5 références vanilla inchangées, 10 injections consommatrices. Le résumé `SALT_PM_FOUND = 17` compte les PM définis ou modifiés dans `lagab_pms.txt`; la chaîne complète contient 22 IDs uniques en incluant les cinq références vanilla.

## Géographie La Gabelle

Le fichier `common/history/states/lagab_states.txt` contient 161 appels `change_resource_potential` dans 159 State Regions distinctes.

| Type | Relations/régions | Potentiel total | Visible au départ | Caché | États avec bâtiment initial |
|---|---:|---:|---:|---:|---:|
| `building_salt_pan` | 97 | 2,526 | 2,526 | 0 | 39 |
| `building_salt_mine` | 64 | 1,209 | 1,209 | 0 | 22 relations distinctes |
| Total | 161 relations / 159 régions | 3,735 | 3,735 | 0 | 61 relations distinctes |

`STATE_CATALONIA` et `STATE_UPPER_ANDALUSIA` portent les deux types. Les 159 IDs existent tous dans la carte effective actuelle de 1776.

Les quatre fichiers `common/history/buildings/lagab_*.txt` demandent :

- 39 créations de salines, total statique 102 niveaux;
- 23 créations de mines, total statique 64 niveaux;
- `STATE_URALSK` mine niveau 3 est dupliqué dans `lagab_asia.txt:420` et `lagab_europe.txt:376`.

Sans test runtime, la seconde instruction `create_building` ne peut pas être classée avec certitude comme addition, remplacement ou échec. Le CSV affiche donc `6 (duplicate records; runtime result unresolved)` et conserve les deux sources. Hors doublon, les mines demandent 61 niveaux uniques.

La table complète, avec nom anglais, potentiel, visibilité, caché, niveaux initiaux, propriétaire scripté et lignes sources, se trouve dans `TECH6A1_LA_GABELLE_SALT_RESOURCE_MAP.csv`.

## Compatibilité du système de ressources 1.13.9

Vanilla 1.13.9 utilise bien les building types comme ressources :

- `resource { type = "building_oil_rig" undiscovered_amount = 20 }` dans `map_data/state_regions/00_west_europe.txt:282-285`;
- `resource { type = "building_rubber_plantation" undiscovered_amount = 15 discovered_amount = 1 }` dans `07_south_america.txt:253-257`;
- `depleted_type = "building_gold_mine"` seulement pour les gold fields dans les exemples inspectés;
- `on_resource_discovered` existe dans `common/on_actions/00_code_on_actions.txt:4137-4147`;
- `force_resource_discovery` et les effets `add/remove/change_resource_potential` existent dans `common/effect_localization/00_state_region_effects_loc.txt:107-128`;
- les chances/fractions moteur existent dans `common/defines/00_defines.txt:521-527`.

Conclusion : le split connu/caché est natif, mais le groupe `bg_mining` de La Gabelle ne l’est pas. Détail et recommandation : `TECH6A1_SALT_DISCOVERY_ARCHITECTURE.md`.

## Consommateurs productifs

Tous les consommateurs PM sont des IDs vanilla réutilisés par `INJECT:` dans `common/production_methods/lagab_pms.txt:186-264`.

| Classe | Bâtiment / PM | Sel | Gate effective 1776 | Bien final / rôle |
|---|---|---:|---|---|
| EARLY_CONSUMER | Food Industries / `pm_sweeteners` | 10 | `distillation`, era_1 | groceries 65; conservation/alimentation transformée |
| EARLY_CONSUMER | Chemical Plant / `pm_artificial_fertilizers` | 5 | bâtiment `industrial_acids`, era_2 | fertilizer 90; chimie productive |
| MID_GAME_CONSUMER | Food Industries / `pm_cannery` | 10 | `canneries`, era_5 | groceries +30 |
| MID_GAME_CONSUMER | Food Industries / `pm_cannery_fish` | 10 | `canneries`, era_5 | groceries +30 |
| LATE_CONSUMER | Food Industries / `pm_baking_powder` | 30 | `baking_powder`, era_7 | groceries 120 |
| LATE_CONSUMER | Food Industries / `pm_vacuum_canning` | 15 | `vacuum_canning`, era_8 | groceries +60 |
| LATE_CONSUMER | Food Industries / `pm_vacuum_canning_principle_3` | 15 | vacuum + principe niveau 3 | groceries +70 |
| LATE_CONSUMER | Synthetics Plant / `pm_dye_production` | 10 | bâtiment `aniline`, era_8 | dye 80 |
| LATE_CONSUMER | Chemical Plant / `pm_improved_fertilizer` | 10 | `improved_fertilizer`, era_8 | fertilizer 140 |
| LATE_CONSUMER | Chemical Plant / `pm_nitrogen_fixation` | 20 | `nitrogen_fixation`, era_11 | fertilizer 200 |
| GOVERNMENT/MILITARY | `mobilization_option_extra_supplies` | 0.5 | sélection de l’option | upkeep militaire |
| GOVERNMENT/MILITARY | `mobilization_option_luxurious_supplies` | 1 | sélection de l’option | upkeep militaire |

`EARLY_PRODUCTIVE_SALT_SINK_PRESENT = YES`

Le sink le plus précoce et explicite est `pm_sweeteners`; il est disponible dans une industrie débloquée par `traditional_food_processing` era_1 et demande `distillation` era_1. Le Chemical Plant apporte un second débouché à era_2. Le marché La Gabelle ne repose donc pas uniquement sur les POPs.

## Pop needs

La Gabelle modifie deux besoins vanilla et aucun buy package :

| Pop need | weight | min_supply_share | max_supply_share | Biens vanilla du même besoin | Verdict 1776 |
|---|---:|---:|---:|---|---|
| `popneed_basic_food` | 1 | 0 | 0.20 | grain, fish, meat, fruit, groceries et autres substituts définis dans `00_pop_needs.txt` | `INCOMPATIBLE_WITH_1776_DESIGN` : BASIC_FOOD_INTEGRATION=NO |
| `popneed_luxury_food` | 0.5 | 0.05 | 0.15 | luxury-food substitutes du même besoin vanilla | `ADAPTATION_REQUIRED` : rôle correct, minimum incorrect |

Pour respecter `SALT_POP_ROLE = LUXURY_ONLY` et `SALT_POP_MINIMUM_SHARE = 0`, il faudra omettre l’injection basic food et mettre le minimum luxury à zéro. Aucune modification n’est effectuée ici.

`POP_SALT_CONSUMPTION_PRESENT = YES`

`POP_SALT_COMPATIBLE_WITH_LUXURY_ONLY = NO`

## Technologie

La porte du bâtiment de sel gemme est déjà exactement la décision canonique :

```text
LA_GABELLE_GATE = shaft_mining
1776_CANONICAL_GATE = shaft_mining
ADAPTATION_REQUIRED = NO
```

| Objet | Gate La Gabelle | Existe dans 1776 | Équivalent 1776 | Adaptation |
|---|---|---|---|---|
| `building_salt_mine` | `shaft_mining` | YES, era_1 | `shaft_mining` | NO |
| PM atmospheric | `atmospheric_engine` | YES, era_2 | même ID | NO |
| PM condensing | `watertube_boiler` | YES, era_7 compatibilité | même ID | NO |
| PM diesel | `compression_ignition` | YES, era_11 compatibilité | même ID | NO |
| PM nitroglycerin | `nitroglycerin` | YES, era_7 compatibilité | même ID | NO |
| PM dynamite | `dynamite` | YES, era_8 compatibilité | même ID | NO |
| PM steam donkey | `steam_donkey` | YES | même ID | NO |
| PM rail | `railways` | YES | même ID | NO |
| `pm_sweeteners` | `distillation` | YES, era_1 | même ID | NO |
| canneries | `canneries` | YES, era_5 | même ID | NO |
| baking/vacuum | `baking_powder` / `vacuum_canning` | YES, era_7/8 | mêmes IDs | NO |
| fertiliser/dye chain | `industrial_acids`, `improved_fertilizer`, `nitrogen_fixation`, `aniline` | YES | mêmes IDs | NO |

`LA_GABELLE_TECH_GATE_ADAPTATION_REQUIRED = NO`

Cette réponse porte sur le mapping technologique. L’adaptation du building group pour la découverte reste séparément requise.

## Assets, GUI et localisations

Assets spécifiques présents :

- `gfx/interface/icons/goods_icons/salt.dds`;
- `gfx/interface/icons/building_icons/building_salt_mine.dds`;
- `gfx/interface/icons/building_icons/building_salt_pan.dds`;
- `gfx/interface/icons/goods_icons/prestige_goods/generic_salt_prestige.dds`;
- `gfx/interface/icons/event_icons/gabelle.dds`;
- `gfx/interface/icons/company_icons/basic_salt.dds`;
- `gfx/interface/icons/company_icons/company_salt_union.dds`;
- `gfx/interface/icons/company_icons/company_groupe_salins.dds`;
- `gfx/interface/icons/company_icons/company_groupe_salins_2.dds`;
- `gfx/interface/icons/company_icons/company_morton_salt.dds`;
- `gfx/interface/icons/company_icons/company_kali_und_salz_ag.dds`;
- `gfx/interface/icons/company_icons/company_maldon_sea_salt.dds`.

Les 12 DDS font chacun 87,556 octets. `gui/lagab_salt_texticons.gui` déclare les text icons du good et du prestige good. Les PM n’ont pas d’icônes custom : leurs définitions pointent vers les icônes vanilla picks, pumps, condensing engine, diesel pump, nitroglycerin, dynamite et gold mining. Aucun mesh spécifique n’est présent.

Localisations : six fichiers dans chacune des langues `english`, `french` et `simp_chinese`, couvrant buildings, companies, events, goods, journal entries et modifiers. Les noms français canoniques observés sont `Sel`, `Mines de sel` et `Marais salant`.

Le package audité ne contient aucun `LICENSE`, fichier de crédits ou texte d’autorisation. `README.md` liste seulement les compagnies et pays taxant le sel. Ce constat historique sur le contenu du package reste exact, mais il a été remplacé juridiquement par l’autorisation directe donnée ultérieurement par Tokugawa_Mori le 2026-08-28 : « Yes, just go ahead! ».

`REDISTRIBUTION_PERMISSION_FOUND_IN_PACKAGE = NO`

Statut actuel : `LA_GABELLE_PERMISSION = GRANTED`. Les adaptations et assets concernés peuvent être trackés, commités ultérieurement et distribués avec attribution à Tokugawa_Mori. Aucune licence MIT, GPL ou autre n’est déduite de cette autorisation explicite.

## Autres objets sel

L’inventaire exhaustif se trouve dans `TECH6A1_LA_GABELLE_SALT_OBJECTS.csv`. Il comprend aussi : six compagnies, un prestige good, deux JE, sept événements, six static modifiers, quatre modifier types, un message, un script value, un scripted trigger, le setup global de taxes/tarifs et les trois pools mensuels d’événements.

Observations techniques :

- `company_maldon_sea_salt` existe dans les scripts et localisations mais n’est pas listée dans le README;
- `lagab_france.2` exige `lagab_gabelle_reformed` dans son trigger avant que son option ne pose cette variable, ce qui rend la première activation normalement douteuse;
- `REPLACE_OR_CREATE:lagab_is_active` et tous les `INJECT:` suivent une convention Community Mod Framework, alors que les métadonnées de La Gabelle ne déclarent aucune dépendance;
- aucun objet de découverte n’est attaché aux événements mensuels.

## Conflits et intégration future dans 1776

Le dépôt 1776 ne définit actuellement aucun good, bâtiment, PM, PMG, modifier ou clé de localisation `salt`/La Gabelle. Les nouveaux IDs principaux n’entrent donc pas en collision. Les conflits concernent les IDs vanilla que La Gabelle injecte et les fichiers déjà shadowés par 1776.

| ID | La Gabelle | 1776 | Vanilla | Type | Action future requise |
|---|---|---|---|---|---|
| `pm_sweeteners` | `lagab_pms.txt:218` | `common/production_methods/01_industry.txt:21` | même fichier/ligne 21 | ID vanilla déjà shadowé | modifier la copie complète 1776 `01_industry.txt` |
| `pm_baking_powder` | `:226` | `01_industry.txt:47` | ligne 47 | idem | same-relative-path merge |
| `pm_cannery` | `:186` | `01_industry.txt:78` | ligne 78 | idem | same-relative-path merge |
| `pm_cannery_fish` | `:194` | `01_industry.txt:103` | ligne 103 | idem | same-relative-path merge |
| `pm_vacuum_canning` | `:202` | `01_industry.txt:128` | ligne 128 | idem | same-relative-path merge |
| `pm_vacuum_canning_principle_3` | `:210` | `01_industry.txt:157` | ligne 157 | idem | same-relative-path merge |
| `pm_artificial_fertilizers` | `:242` | `01_industry.txt:1248` | vanilla ligne 1240 | idem | merge avec les changements TECH existants |
| `pm_improved_fertilizer` | `:250` | `01_industry.txt:1276` | vanilla ligne 1268 | idem | merge |
| `pm_nitrogen_fixation` | `:258` | `01_industry.txt:1307` | vanilla ligne 1299 | idem | merge |
| `pm_dye_production` | `:234` | `01_industry.txt:1474` | vanilla ligne 1466 | idem | merge |
| `popneed_basic_food` | `lagab_pop_needs.txt:1` | hérité | `common/pop_needs/00_pop_needs.txt:46` | ID vanilla + conflit de design | ne pas intégrer au basic food |
| `popneed_luxury_food` | `:11` | hérité | `00_pop_needs.txt:290` | ID vanilla | shadow complet et min=0 si retenu |
| deux mobilization options | `lagab_mobilization_option.txt` | héritées | `00_mobilization_option.txt:31,104` | IDs vanilla | shadow complet du fichier vanilla |
| `on_monthly_pulse_country` | `lagab_on_actions.txt:26` | `00_code_on_actions.txt:458` et `06_mod_on_actions.txt:1` | vanilla `:475` | trois définitions concurrentes | fusion explicite; ne pas recopier les pulses La Gabelle sans décision |
| `GLOBAL` | `lagab_global.txt` | `common/history/global/00_global.txt` | même scope | setup additif et tags 1836 | réécrire pour le setup 1776, sans copier les pays arbitrairement |
| 159 State Regions | `lagab_states.txt` | carte effective 1776 | objets vanilla existants | ajout de potentiel aux mêmes objets | shadow des fichiers `map_data/state_regions` pour le hidden split |
| 15 relations de région | `lagab_states.txt` | `map_data/state_regions/08_middle_east.txt` ou `13_australasia.txt` | mêmes fichiers vanilla | chevauchement avec deux shadows 1776 actuels | fusionner dans les fichiers 1776 existants |
| `shaft_mining` et autres gates | références | tech tree 1776 | vanilla | IDs intentionnellement réutilisés | aucun nouvel ID; conserver le mapping audité |

Les fichiers historiques de bâtiments La Gabelle sont conçus pour les propriétaires/tags de 1836. Les State Region IDs existent, mais les `region_state:TAG` et propriétaires ne doivent pas être copiés comme setup 1776 sans audit d’appartenance à la date de départ.

Le PM 1776 `pm_brine_electrolysis` existe déjà par son nom, mais il ne référence pas un good `salt` actuel. Il ne constitue pas un conflit d’ID avec La Gabelle; toute future consommation de sel serait une décision d’intégration distincte.

## Verdicts

| Question | Verdict |
|---|---|
| Schéma du good | `YES` |
| IDs réels des bâtiments | `building_salt_mine`, `building_salt_pan` |
| Géographie capturée | `YES`, 161 relations / 159 régions |
| Potentiel caché dans La Gabelle | `NO`, tout est visible |
| Découverte native possible sans système parallèle | `YES`, après adaptation de groupe et de map data |
| Architecture recommandée | `NATIVE_DISCOVERY_ONLY` |
| Sink productif précoce | `YES` |
| Pop needs compatibles tels quels | `NO` |
| Gate mine compatible avec la décision 1776 | `YES`, déjà `shaft_mining` |
| Permission de redistribution | `GRANTED` directement par Tokugawa_Mori le 2026-08-28 ; aucune permission incluse dans le package lui-même |
| Runtime nécessaire avant implémentation finale | `YES` pour découverte, doublon Uralsk, AI et économie |

## Résumé final obligatoire

TECH6A1_LA_GABELLE_AUDIT = PASS

LA_GABELLE_FOUND = YES
LA_GABELLE_PATH = C:/Program Files (x86)/Steam/steamapps/workshop/content/529340/3715913236

SALT_GOOD_FOUND = YES
SALT_BUILDINGS_FOUND = 2
SALT_PM_FOUND = 17
SALT_PMG_FOUND = 5
SALT_RESOURCE_REGIONS_FOUND = 159

EARLY_PRODUCTIVE_SALT_SINK_PRESENT = YES

POP_SALT_CONSUMPTION_PRESENT = YES
POP_SALT_COMPATIBLE_WITH_LUXURY_ONLY = NO

ROCK_SALT_BUILDING_ID = building_salt_mine
SURFACE_SALT_BUILDING_ID = building_salt_pan

RESOURCE_DISCOVERY_NATIVE_COMPATIBLE = PARTIAL

RECOMMENDED_DISCOVERY_ARCHITECTURE = NATIVE_DISCOVERY_ONLY

LA_GABELLE_TECH_GATE_ADAPTATION_REQUIRED = NO

REDISTRIBUTION_PERMISSION_FOUND_IN_PACKAGE = NO
LA_GABELLE_PERMISSION = GRANTED
PERMISSION_DATE = 2026-08-28
ORIGINAL_AUTHOR = Tokugawa_Mori

GAMEPLAY_FILES_CHANGED = 0
COMMITS_CREATED = 0
PUSH_PERFORMED = NO

TECH6A1_READY_FOR_DESIGN_FREEZE = YES
