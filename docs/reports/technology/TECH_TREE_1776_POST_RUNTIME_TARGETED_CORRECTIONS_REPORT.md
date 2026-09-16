# TECH TREE 1776 — Post-runtime targeted corrections report

Date: 2026-09-14  
Runtime target: Victoria 3 1.13.11  
Repository authority: local working tree

## 1. Résumé

La passe ciblée Société / Commerce / Militaire / Agriculture / Mines / Textile / Verre / Naval est appliquée. Les trois anciens nœuds abstraits sont conservés uniquement comme aliases de compatibilité non recherchables. Le graphe effectif contient 241 technologies recherchables, 343 arêtes, 15 racines, aucun cycle, aucun parent inconnu, aucune inversion d’ère, aucun nœud isolé et aucune feuille sans contenu.

Le validateur canonique lit maintenant le graphe et les objets gameplay effectivement chargés depuis vanilla + mod. Il recalcule aussi les 704 associations bâtiment/PM. Le résultat ajusté est de 0 violation.

La fermeture des starts a retiré les anciens grants d’aliases et ajouté uniquement les prérequis directement imposés par le nouveau graphe. Trois dettes sensibles `applied_mineralogy -> shaft_mining` sont volontairement conservées et rapportées pour `KRA`, `MOR` et `SC2`.

## 2. Fichiers modifiés par cette passe

Définitions principales :

- `common/technology/technologies/10_tech3a_production.txt`
- `common/technology/technologies/20_tech3a_military.txt`
- `common/technology/technologies/25_tech3a_naval.txt`
- `common/technology/technologies/30_tech3a_society.txt`
- `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`
- `common/buildings/01_industry.txt`
- `common/buildings/05_military.txt`
- `common/laws/01_trade_policy.txt`
- `common/production_methods/03_mines.txt`
- `common/production_methods/16_tech6r1_mine_processing.txt`

Migration de références et starts :

- `common/scripted_effects/00_starting_inventions.txt`
- 183 fichiers effectifs dans `common/history/countries/`
- `common/history/political_movements/00_movements.txt`
- `common/ideologies/01_character_ideologies.txt`
- `common/interest_groups/00_intelligentsia.txt`
- `common/journal_entries/00_art_jes.txt`
- `common/scripted_effects/00_victoria_scripted_effects.txt`
- `events/french_revolution_mod_events.txt`
- `events/tech_events/society_tech_events.txt`

Validation et documentation :

- `tools/tech_start_1776_implementation.py`
- `tools/tech_tree_1776_wave3_polish.py`
- ce rapport

Aucune localisation EN/FR n’a dû être renommée : les labels existants sont conservés pour la compatibilité des sauvegardes, tandis que `can_research = no` et l’absence de toute référence active neutralisent la présentation des trois aliases dans la progression normale.

## 3. Technologies supprimées du graphe recherchable

| ID | Décision | Parents | Enfants actifs | Unlocks/modifier | Grants actifs |
|---|---|---:|---:|---:|---:|
| `codified_practical_knowledge` | `KEEP_COMPATIBILITY_ALIAS` | 0 | 0 | 0 | 0 |
| `traditional_glassmaking` | `KEEP_COMPATIBILITY_ALIAS` | 0 | 0 | 0 | 0 |
| `organized_naval_establishments` | `KEEP_COMPATIBILITY_ALIAS` | 0 | 0 | 0 | 0 |

Chaque alias conserve son ID et sa localisation pour les anciennes sauvegardes et la compatibilité externe, avec `can_research = no`, sans parent, enfant, unlock ou modifier. Le scan de `common/` et `events/` ne trouve plus de référence active hors de leur définition de compatibilité.

## 4. Société et savoir

| Technologie | Era | Parents finaux | Décision |
|---|---:|---|---|
| `political_economy` | 3 | `periodical_print_networks`, `systematic_administrative_statistics` | remplace l’ancien tronc codifié et exige une base statistique d’État |
| `organized_elementary_schooling` | 3 | `periodical_print_networks` | remplace l’ancien tronc codifié |
| `medical_degrees` | 3 | `institutionalized_scientific_exchange` | parent déjà cohérent, maintenu |
| `variolation_networks` | 2 | `institutionalized_scientific_exchange` | n’est plus une racine |

### Arbitrage MEDICAL_DEGREES

Parent final choisi = `institutionalized_scientific_exchange`.  
Pourquoi = c’est le socle institutionnel existant le plus proche pour formaliser les diplômes médicaux. `variolation_networks` est une pratique sanitaire spécialisée et `veterinary_science` une branche professionnelle distincte ; aucun n’est un meilleur socle général. Aucun nouveau nœud n’a été créé.

Les anciennes responsabilités actives de `codified_practical_knowledge` ont été redistribuées vers `institutionalized_scientific_exchange`, `periodical_print_networks` ou `political_economy` selon leur sens : idéologies, mouvement antiesclavagiste, intelligentsia/empirisme, Révolution française, événements de technologie et effet d’exil.

`systematic_administrative_statistics` est désormais un second parent cumulatif de `political_economy` : l’analyse politique de l’économie repose ainsi sur une administration capable de produire des statistiques d’État.

### Construction structurelle tardive

`reinforced_concrete` est ajouté comme second parent de `arc_welding`, en complément de `electric_arc_process`. L’ID reste inchangé pour la compatibilité, mais sa présentation devient « Ingénierie structurelle moderne » / “Modern Structural Engineering”. Le PM de construction `pm_arc_welded_buildings` devient « Construction structurelle moderne » / “Modern Structural Construction”, afin de représenter ensemble le béton armé et les ossatures métalliques soudées. Les PM navals conservent leurs noms spécialisés.

### Colonisation, quinine et canal de Suez

`colonization` devient un second parent cumulatif de `quinine`, aux côtés de `active_principle_pharmacy`. Le déblocage de `building_suez_canal` est déplacé de `colonization` vers `quinine`. Le premier override séparé n’était pas prioritaire sur le fichier vanilla au runtime ; il est remplacé par un miroir au même chemin `common/buildings/10_canals.txt`. Les définitions de Panama et Kiel sont conservées à l’identique, respectivement gatées par `civilizing_mission` et `ironclad_tech`. Les études et les journaux de construction ne sont pas modifiés.

## 5. Commerce

L’audit mod + vanilla confirme qu’il n’existe aucune technologie `mercantilism`. L’ID réel est la loi `law_mercantilism`. Il aurait été incorrect d’inventer un nœud technologique ou de déplacer `commercial_insurance_markets`.

La solution minimale appliquée est donc un gate cumulatif sur la loi :

```text
law_mercantilism.unlocking_technologies = {
    commercial_insurance_markets
    international_relations
}
```

`commercial_insurance_markets`, `stock_exchange` et `institutionalized_public_credit` n’ont pas été déplacés. Les autres lois commerciales ne sont pas modifiées.

## 6. Militaire

| Objet | Gate/parent final |
|---|---|
| `scientific_fortification_siegecraft` | `organized_military_establishments` |
| `building_barrack` (alias `building_barracks`) | `organized_military_establishments` |
| `casemated_fortifications` | `scientific_fortification_siegecraft` |
| `pm_naval_fortification_reinforced` | `casemated_fortifications` |

Le bâtiment Casernes n’est donc plus rattaché à la technologie de fortification. Le PM casematé existait déjà sous le bon ID et n’a pas été dupliqué.

## 7. Agriculture

| Technologie | Era finale | Parents finaux |
|---|---:|---|
| `improved_agricultural_implements` | 1 | `improved_husbandry` |
| `selective_breeding` | 2 | `improved_husbandry` |
| `advanced_crop_rotations` | 3 | `improved_husbandry`, `selective_breeding` |
| `artificial_fertilizers` | 4 | `advanced_crop_rotations`, `industrial_acids` |

Le parent historique `improved_husbandry` de la rotation culturale est conservé ; `selective_breeding` est ajouté comme second prérequis cumulatif.

## 8. Chaîne engrais

| Stage | Technology | Building(s) | PM | Fertilizer |
|---|---|---|---|---:|
| 1 — source faible | `selective_breeding` (era 2) | `building_livestock_ranch` | `pm_sheep_farms` | output 2.5 |
| 2 — premiers usages | `advanced_crop_rotations` (era 3) | `building_rye_farm`, `building_wheat_farm`, `building_maize_farm`, `building_millet_farm` | `pm_soil_enriching_farming` | input 5 |
| 2 — variante riz | `advanced_crop_rotations` (era 3) | `building_rice_farm` | `pm_soil_enriching_farming_building_rice_farm` | input 10 |
| 3 — industrie de base | `artificial_fertilizers` (era 4) | `building_chemical_plant` | `pm_artificial_fertilizers` | output 40 |
| 4 — industrie avancée | `improved_fertilizer` (era 8) | `building_chemical_plant` | `pm_improved_fertilizer` | output 120 |
| 5 — fixation d’azote | `nitrogen_fixation` (era 11) | `building_chemical_plant` | `pm_nitrogen_fixation` | output 200 |

Arbitrage obligatoire :

- Fertilizer_Tech_ID = `artificial_fertilizers`
- Fertilizer_Tech_Era = `era_4`
- Fertilizer_Building_ID = `building_chemical_plant`
- Building_Unlock_Tech = `artificial_fertilizers`
- Base_PM_ID = `pm_artificial_fertilizers`
- Advanced_PMs = `pm_improved_fertilizer`, `pm_nitrogen_fixation`
- Correction_Applied = ajout de `artificial_fertilizers` en era 4, avec `advanced_crop_rotations` et `industrial_acids` comme prérequis cumulatifs. Le bâtiment passe sur ce gate précoce et `improved_fertilizer` en devient l’enfant direct.

La première source faible précède donc bien les premiers consommateurs : `selective_breeding`/era 2 avant `advanced_crop_rotations`/era 3.

## 9. Mines et vapeur

`applied_mineralogy` est maintenant en era 3 avec `shaft_mining` comme parent obligatoire. Le bâtiment `building_gold_mine` reste débloqué par `applied_mineralogy`.

Les gates cumulatifs `applied_mineralogy` ont été retirés uniquement des quatre PM vapeur concernés :

- `pm_atmospheric_engine_pump_building_gold_mine` -> `atmospheric_engine`
- `pm_condensing_engine_pump_building_gold_mine` -> `condensing_steam_engines`
- `pm_atmospheric_engine_pump_building_phosphate_mine` -> `atmospheric_engine`
- `pm_condensing_engine_pump_building_phosphate_mine` -> `condensing_steam_engines`

Le résultat est identique aux pompes des mines de charbon, fer, plomb, soufre, cuivre et phosphate : la ressource est garantie par le bâtiment ; la méthode est déterminée par la technologie motrice.

## 10. Audit complet de la mine d’or

Building gate = `building_gold_mine -> applied_mineralogy`.

| PM_ID | Current unlocks | Equivalent in other mines | Expected unlocks | Decision |
|---|---|---|---|---|
| `pm_picks_and_shovels_building_gold_mine` | aucun | variantes `pm_picks_and_shovels_building_*_mine` | aucun | KEEP |
| `pm_atmospheric_engine_pump_building_gold_mine` | `atmospheric_engine` | variantes charbon/fer/plomb/soufre/cuivre/phosphate | `atmospheric_engine` | FIXED |
| `pm_condensing_engine_pump_building_gold_mine` | `condensing_steam_engines` | variantes charbon/fer/plomb/soufre/cuivre/phosphate | `condensing_steam_engines` | FIXED |
| `pm_diesel_pump_building_gold_mine` | `compression_ignition` | variantes `pm_diesel_pump_building_*_mine` | `compression_ignition` | KEEP |
| `pm_no_explosives` | aucun | PM partagé | aucun | KEEP |
| `pm_nitroglycerin_building_gold_mine` | `nitroglycerin` | variantes `pm_nitroglycerin_building_*_mine` | `nitroglycerin` | KEEP |
| `pm_dynamite_building_gold_mine` | `dynamite` | variantes `pm_dynamite_building_*_mine` | `dynamite` | KEEP |
| `pm_no_steam_automation` | aucun | PM partagé | aucun | KEEP |
| `pm_steam_donkey_mine` | `steam_donkey` | PM partagé | `steam_donkey` | KEEP |
| `pm_road_carts` | aucun | PM partagé | aucun | KEEP |
| `pm_rail_transport_mine` | `railways` | PM partagé | `railways` | KEEP |
| `pm_no_ore_concentration_building_gold_mine` | aucun | variantes sans concentration | aucun | KEEP |
| `pm_ore_concentration_building_gold_mine` | `geological_surveying` | variantes de concentration des autres mines | `geological_surveying` | KEEP |
| `pm_no_mine_ventilation` | aucun | PM partagé | aucun | KEEP |
| `pm_steam_mine_ventilation` | `deep_mine_engineering` | PM partagé | `deep_mine_engineering` | KEEP |
| `pm_electric_mine_ventilation` | `deep_mine_engineering`, `electrical_capacitors` | PM partagé | mêmes gates | KEEP |

Les deux pompes vapeur ont une technologie autonome qui peut être antérieure au bâtiment dans l’arbre, mais elles ne peuvent jamais être exposées sans la mine d’or elle-même. Le validateur classe donc correctement ces associations comme `BUILDING_GATE_GUARANTEES_RESOURCE_CHAIN`, et non comme violation.

## 11. Textile

L’ID localisé « Mécanisation de la couture » est `advanced_spinning` (era 4). Il est ajouté comme parent cumulatif de `electrical_capacitors` :

```text
electrical_capacitors <- electrical_generation
electrical_capacitors <- mechanized_weaving
electrical_capacitors <- advanced_spinning
```

Coût collatéral explicite : tous les contenus dépendant du condensateur exigent désormais aussi la continuité textile `organized_textile_production -> mechanized_spinning -> advanced_spinning`. Cela touche notamment les machines à coudre électriques, mais aussi les autres PM électriques déjà rattachés au condensateur. Aucun autre parent valide n’a été retiré.

## 12. Cotton gin

- Current unlocks = modificateur direct `building_cotton_plantation_throughput_add = 0.25` et gates de compagnies utilisant `cotton_gin`.
- Candidate children inspected = `organized_textile_production`, `mechanized_spinning`, `mechanized_weaving`, `advanced_spinning`, `mechanized_farming`.
- Chosen child = `NONE`.
- Decision = `KEEP_TERMINAL`.
- Reason = `mechanized_spinning` est déjà son parent ; couture et tissage ne sont pas des descendants conceptuels fiables de l’égrenage, tandis que `mechanized_farming` est une chaîne agricole trop générale. Le nœud terminal possède déjà un effet gameplay utile et n’est donc pas une feuille vide.

## 13. Verre

| Élément | Résultat final |
|---|---|
| `traditional_glassmaking` | alias de compatibilité non recherchable |
| bâtiment verrerie | `building_glassworks -> organized_workshops` |
| `industrial_ceramics` | parent direct `organized_workshops` |
| `crystal_glass` | parents directs `industrial_ceramics` + `organized_workshops` |

Migration pays : 64 grants effectifs de l’ancien alias ont été supprimés. Dans le plan historique, 62 TAG le ciblaient explicitement ; les 62 disposent déjà de `organized_workshops` dans le setup final. Les deux occurrences effectives supplémentaires provenaient de la résolution/tier antérieure. Aucun grant supplémentaire de `organized_workshops` n’a été nécessaire, donc aucun pays n’a reçu artificiellement les déblocages meuble + outillage à cause de cette suppression.

## 14. Naval

`organized_naval_establishments` devient un alias de compatibilité non recherchable. `state_dockyard_systems` redevient racine sans parent.

Enfants directs finaux :

- `enclosed_dock_systems -> state_dockyard_systems`
- `scientific_naval_architecture -> state_dockyard_systems`
- `ship_classification_surveying -> state_dockyard_systems`

Les 54 grants structurels Wave 1 de `organized_naval_establishments` ont été retirés. Seulement 13 grants de fermeture vers `state_dockyard_systems` ont été ajoutés, car ces pays possédaient déjà un contenu naval spécialisé :

```text
BRE FJI GEN GR3 HAM HAW LUB MCR PAP PLY PRU TNG TUS
```

Répartition causale : 8 pour `enclosed_dock_systems` (`BRE GEN GR3 HAM LUB PAP PRU TUS`) et 5 pour `scientific_naval_architecture` (`FJI HAW MCR PLY TNG`). Aucun des 41 autres bénéficiaires Wave 1 n’a reçu automatiquement `state_dockyard_systems`.

## 15. Impact starts

La migration de cette passe a modifié 183 fichiers pays et 347 relations de technologie : 243 suppressions d’aliases et 104 ajouts de fermeture réelle.

| Type | Technologie | Nombre | TAGs / remarque |
|---|---|---:|---|
| REMOVE alias | `codified_practical_knowledge` | 125 relations explicites effectives | 135 occurrences avaient été observées avant neutralisation des tiers ; 10 étaient héritées de tiers |
| REMOVE alias | `traditional_glassmaking` | 64 | aucun remplacement coûteux requis |
| REMOVE alias | `organized_naval_establishments` | 54 | anciens grants Wave 1 |
| ADD closure | `institutionalized_scientific_exchange` | 51 | fermeture médecine/variolisation ; `CHL` possédait les deux enfants et ne compte qu’une fois |
| ADD closure | `periodical_print_networks` | 7 | `BOR CON ETH HAR MOR TRI TUN` |
| ADD closure | `selective_breeding` | 32 | fermeture de `advanced_crop_rotations` |
| ADD closure | `state_dockyard_systems` | 13 | liste détaillée section Naval |
| ADD closure | `systematic_administrative_statistics` | 1 | `ETH`, pour `systematic_legal_codification` |
| ADD closure | `systematic_administrative_statistics` | 1 | `KRA`, pour le nouveau parent de `political_economy` |

Tags ajoutés à `institutionalized_scientific_exchange` :

```text
ADG AIR ASH AWA BER BGI BGM BHV BND BRN CAY CHL CUB ECU FTJ FTR GJM GR3
GR5 HAU HDY JLF JUN KFA KOR KRT KUT MARATH MAS MEX MSN MUG NAW NPU PEU
PTN QWR SC1 SC3 SD1 SDM SGU SHW SIN SOK SPU TGR VNZ WAD WLG WLT
```

Tags ajoutés à `selective_breeding` :

```text
ASM AWA BEL BEO BER BIC CHI COC DAI FRA GWA HYD IND IREK JAI JAP JOD KNK
KOR KOT MARATH MEW MUG MYS NAG NEP NET PAN PTN SIA SIN TRA
```

## 16. Nouvelles dettes de prérequis

Les trois dettes suivantes sont laissées visibles, conformément à l’interdiction de masquer le cas sensible `applied_mineralogy -> shaft_mining` par un grant massif :

| TAG | Missing_Technology | Required_By | Reason | Proposed_Action |
|---|---|---|---|---|
| `KRA` | `shaft_mining` | `applied_mineralogy` | nouveau parent direct, justification historique non revue | arbitrage historique ultérieur |
| `MOR` | `shaft_mining` | `applied_mineralogy` | nouveau parent direct, justification historique non revue | arbitrage historique ultérieur |
| `SC2` | `shaft_mining` | `applied_mineralogy` | nouveau parent direct, justification historique non revue | arbitrage historique ultérieur |

Missing direct = 3. Missing transitive = 3. Elles sont explicitement reconnues par le validateur ; toute autre dette reste bloquante.

## 17. Métriques du graphe effectif

| Metric | Value |
|---|---:|
| researchable_nodes | 242 |
| roots | 15 |
| isolated_nodes | 0 |
| leaf_no_effect | 0 |
| edges | 347 |
| average_parent_count | 1.434 |
| average_child_count | 1.434 |
| max_child_count | 8 |
| cycles | 0 |
| unknown_parent_ids | 0 |
| negative_era_edges | 0 |
| same_era_edges | 39 |
| cross_era_plus1 | 119 |
| cross_era_plus2 | 89 |
| cross_era_plus3 | 55 |
| cross_era_gt3 | 45 |

Racines finales : `improved_husbandry`, `industrial_acids`, `institutionalized_scientific_exchange`, `international_relations`, `organized_financial_institutions`, `organized_military_establishments`, `organized_textile_production`, `organized_workshops`, `periodical_print_networks`, `shaft_mining`, `state_dockyard_systems`, `systematic_administrative_statistics`, `traditional_food_processing`, `traditional_papermaking`, `turnpike_road_networks`.

## 18. Causalité bâtiment/PM

- Associations effectives recalculées : 704.
- Violations brutes restantes après prise en compte du gate du bâtiment : 0.
- `building_gold_mine`, `building_phosphate_mine`, `building_chemical_plant`, `building_glassworks`, `building_artillery_foundry` et `building_cotton_plantation` audités explicitement.
- Les quatre pompes or/phosphate n’ont pas besoin de répéter `applied_mineralogy`, car cette technologie est déjà une condition d’existence du bâtiment.
- Aucun PM n’est exposé sans son bâtiment ; les technologies propres aux PM correspondent aux moteurs/processus réellement utilisés.

## 19. Validations statiques

- Validateur canonique `--validate-only` : PASS, exit 0.
- `managed_match = 473/473`.
- `files_to_write = 0` après application : idempotence confirmée.
- Définitions de technologie dupliquées : 0.
- Références actives vers aliases : 0.
- Accolades déséquilibrées : 0.
- IDs de technologie inconnus : 0.
- Parents inconnus : 0.
- Cycles : 0.
- Inversions d’ère : 0.
- Associations bâtiment/PM : 704, violations 0.
- `git diff --check` : PASS ; uniquement des avertissements de normalisation LF/CRLF, sans erreur de whitespace.

## 20. Arbitrages

### A. MEDICAL_DEGREES

Parent final choisi = `institutionalized_scientific_exchange`.  
Pourquoi = fondation institutionnelle existante la plus cohérente, sans nouveau nœud ni coût collatéral.

### B. FERTILIZER

Tech industrielle de base = `artificial_fertilizers`.  
Era = 4.  
Bâtiment = `building_chemical_plant`.  
Gate = `artificial_fertilizers`.  
Amélioration directe = `improved_fertilizer` (era 8).  
A-t-elle été restaurée/corrigée ? = oui, l’accès à l’usine a été avancé sans avancer ses PM améliorés.

### C. FERTILIZER EARLY SOURCE

PM précoce = `pm_sheep_farms`.  
Output engrais = 2.5.  
Tech gate = `selective_breeding` (era 2).

### D. COTTON_GIN

Candidat descendant choisi = `NONE`.  
KEEP_TERMINAL = oui.  
Pourquoi = effet gameplay direct utile et aucun descendant existant suffisamment cohérent.

### E. GOLD MINE

Building gate = `applied_mineralogy`.  
Atmospheric pump gate = `atmospheric_engine`.  
Condensing pump gate = `condensing_steam_engines`.  
Autres pumps = diesel `compression_ignition`; explosifs, transport, concentration et ventilation conservent leurs gates spécialisés.

### F. GLASS

`traditional_glassmaking` = retiré du graphe recherchable.  
deleted/alias = `KEEP_COMPATIBILITY_ALIAS`.  
building glass gate final = `organized_workshops`.  
industrial_ceramics parent = `organized_workshops`.  
crystal_glass parents = `industrial_ceramics`, `organized_workshops`.  
impact pays = 64 grants d’alias retirés, 0 nouveau grant coûteux.

### G. NAVAL

`organized_naval_establishments` = retiré du graphe recherchable.  
deleted/alias = `KEEP_COMPATIBILITY_ALIAS`.  
`state_dockyard_systems` root = oui.  
children = `enclosed_dock_systems`, `scientific_naval_architecture`, `ship_classification_surveying`.  
start grants removed = 54.  
new closure grants required = 13.

## Runtime checklist

SOCIETY

- [ ] Presse -> économie politique.
- [ ] Presse -> enseignement primaire.
- [ ] Échanges scientifiques -> médecine.
- [ ] Échanges scientifiques -> variolisation.

MILITARY

- [ ] Établissements militaires -> casernes.
- [ ] Établissements militaires -> fortification.
- [ ] Fortification -> fort casematé.
- [ ] PM fort casematé visible au bon gate.

AGRICULTURE

- [ ] Outils agricoles rang 1.
- [ ] Élevage sélectif rang 2.
- [ ] Élevage sélectif -> rotations.
- [ ] Première petite source d’engrais via élevage ovin.
- [ ] Usine d’engrais et PM industriels.

MINING

- [ ] Puits de mine -> minéralogie.
- [ ] Mine d’or débloquée par minéralogie.
- [ ] Pompe à feu débloquée par `atmospheric_engine`.
- [ ] Pompe à condensation débloquée par `condensing_steam_engines`.

TEXTILE

- [ ] Mécanisation couture -> condensateur.
- [ ] Cotton gin terminal avec son bonus de plantation.

GLASS

- [ ] Verrerie sur ateliers organisés.
- [ ] Céramique/cristal directement sous ateliers.

NAVAL

- [ ] Arsenaux d’État racine.
- [ ] Bassins fermés sous arsenaux.
- [ ] Architecture navale sous arsenaux.
- [ ] Classement/inspection sous arsenaux.

FINAL RUNTIME

- [ ] Contrôler `error.log`.
- [ ] Lancer au moins jusqu’au 1er février.
- [ ] Vérifier qu’aucune interface n’est cassée.

## Résultat terminal demandé

TECHS REMOVED/ALIASED = 3 : `codified_practical_knowledge`, `traditional_glassmaking`, `organized_naval_establishments` (`KEEP_COMPATIBILITY_ALIAS`).  
PARENTS ADDED = 12 arêtes ciblées : presse→économie politique, presse→enseignement, échanges→variolisation, fortification→casematé, élevage sélectif→rotations, puits de mine→minéralogie, couture mécanisée→condensateurs, ateliers→céramique, ateliers→cristal, arsenaux→bassins, arsenaux→architecture, arsenaux→classement. `medical_degrees` et `scientific_fortification_siegecraft` avaient déjà leurs parents finaux corrects et ont été maintenus.  
PARENTS REMOVED = toutes les arêtes actives impliquant les trois aliases ; les anciens parents de politique/enseignement, verre et naval ont été remplacés.  
ERAS CHANGED = `improved_agricultural_implements -> era_1`; `selective_breeding -> era_2`.  
BUILDING UNLOCKS MOVED = `building_glassworks -> organized_workshops`; `building_barrack -> organized_military_establishments`.  
PM UNLOCKS MOVED = 4 gates cumulatifs `applied_mineralogy` retirés des pompes atmosphériques/condensation des mines d’or et phosphate ; gates vapeur conservés.  
START GRANTS AFFECTED = 243 suppressions + 104 ajouts de fermeture, dans 183 fichiers pays.  
MISSING DIRECT PREREQUISITES = 3 : `KRA`, `MOR`, `SC2` manquent `shaft_mining` pour `applied_mineralogy` ; dette volontairement signalée.  
MISSING TRANSITIVE PREREQUISITES = 3, mêmes cas.  
CYCLES = 0.  
UNKNOWN IDS = 0.  
BUILDING/PM VIOLATIONS = 0 / 704 associations.  
git diff --check = PASS.  

NO COMMIT  
NO PUSH

## Correction runtime — gates construction et Grands Lacs

- Le gate de `building_construction_sector` est désormais remplacé dans le fichier effectif homonyme `common/buildings/13_construction.txt`, et passe de `urbanization` à `organized_financial_institutions`. L’ancien override tardif `99_tech_start_1776_construction_sector.txt`, que le runtime ne retenait pas, a été supprimé.
- La hausse manuelle de `pm_simple_forestry` à 40 bois a été conservée. Les trois PM visibles donnent donc 40 / 80 / 160 bois.
- ACH, ANK, BNY, BRD, BUG, KRG et RWD utilisent désormais le palier 7 vide et ne reçoivent plus aucune technologie explicite au départ.
- Cela retire notamment `international_relations` aux six pays qui la possédaient, ainsi que les grants artisanaux et agricoles trop avancés. Ces sept pays servent désormais de cas runtime pour vérifier le verrou des traités.
- Le plan pays canonique et la distribution finale ont été régénérés afin qu’une future exécution du générateur ne réintroduise pas ces grants.
- Validation ciblée : 473/473 setups gérés conformes, 0 mismatch, 0 technologie inconnue, 0 cycle, 0 erreur structurelle et 0 violation bâtiment/PM.
