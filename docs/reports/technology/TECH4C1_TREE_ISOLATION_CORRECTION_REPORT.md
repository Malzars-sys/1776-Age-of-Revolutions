# TECH-4C1 — Vanilla Tree Isolation Correction

**Statut statique :** `TECH4C1_SAME_TREE_PREREQUISITES_STATIC_PASS_RUNTIME_PENDING`

## 1. Baseline et périmètre

- Branche : `technology-rework`
- Baseline Git avant TECH-4C : `c8958b9020d3b97247a776d0e079ecb9f156e4e2`
- Référence vanilla : Victoria 3 `release/1.13.11`
- État initial : TECH-4C non commitée, avec un fichier gameplay modifié et cinq livrables TECH-4C non suivis.
- TECH-4C1 corrige directement cette implémentation TECH-4C non commitée ; aucun reset n'a été effectué.
- Fichier gameplay autorisé : `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`
- Mutation autorisée et effectuée : listes `unlocking_technologies` de technologies actives Ères VII–XII uniquement.

## 2. Audit vanilla obligatoire

Les trois sources TECH-1A ont été relues, puis contrôlées contre les fichiers vanilla installés `10_production.txt`, `20_military.txt` et `30_society.txt`.

| Mesure | Résultat |
|---|---:|
| `VANILLA_TECHS` | 179 |
| `VANILLA_PREREQUISITE_EDGES` | 221 |
| `VANILLA_CROSS_CATEGORY_PREREQUISITE_EDGES` | 0 |

La règle canonique est donc confirmée : chaque technologie vanilla ne dépend que de technologies de sa catégorie moteur. Les technologies navales portant `category = military` appartiennent à Military et ne constituent pas un quatrième arbre.

Le champ TECH-1A de `multilateral_alliances` sérialise `pan-nationalism` sous la forme `pan;nationalism`. Le fichier vanilla installé confirme un seul ID, `pan-nationalism`. Après cette normalisation documentée, les 221 arêtes TECH-1A concordent exactement avec les fichiers 1.13.11.

## 3. Mesures du graphe actif

| Mesure | Avant TECH-4C1 | Après TECH-4C1 |
|---|---:|---:|
| `ACTIVE_TECHS_TOTAL` | 238 | 238 |
| `ACTIVE_POST1836_TECHS` | 111 | 111 |
| `ACTIVE_EDGES_TOTAL` | 316 | 307 |
| `POST1836_INCOMING_EDGES` | 149 | 140 |
| `CROSS_TREE_EDGES_TOTAL` | 37 | 18 |
| `CROSS_TREE_EDGES_TARGETING_ERA_VII_XII` | 19 | 0 |

Les 18 arêtes cross-tree restantes ciblent exclusivement des technologies Ères I–VI. Elles sont inventoriées dans `TECH4C1_CROSS_TREE_EDGE_AUDIT.csv` avec l'action `OUT_OF_SCOPE_ERA_I_VI_NO_CHANGE`. Cette phase interdit explicitement toute modification des définitions I–VI ; elles devront être traitées dans une phase d'isolation distincte si le runtime ancien arbre présente le même défaut.

### Détail par paire — graphe actif complet

| Paire | Avant | Après |
|---|---:|---:|
| Production → Military | 17 | 8 |
| Production → Society | 10 | 5 |
| Military → Production | 2 | 1 |
| Military → Society | 1 | 0 |
| Society → Production | 0 | 0 |
| Society → Military | 7 | 4 |

### Détail par paire — cibles Ères VII–XII

| Paire | Avant | Après |
|---|---:|---:|
| Production → Military | 9 | 0 |
| Production → Society | 5 | 0 |
| Military → Production | 1 | 0 |
| Military → Society | 1 | 0 |
| Society → Production | 0 | 0 |
| Society → Military | 3 | 0 |

## 4. Arêtes cross-tree post-1836 corrigées

| Arête TECH-4C supprimée | Action | Remplacement same-tree |
|---|---|---|
| `pressed_glass → camera` | remplacement | `experimental_research_laboratories → camera` |
| `optical_telegraph_networks → electric_telegraph` | remplacement | `logistics → electric_telegraph` |
| `medical_degrees → modern_nursing` | remplacement | `battlefield_evacuation → modern_nursing` |
| `interchangeable_manufacture → breech_loading_artillery` | suppression | aucun ; `shell_gun` reste |
| `nitroglycerin → self_propelled_torpedoes` | remplacement | `shell_gun → self_propelled_torpedoes` |
| `professional_civil_engineering → steel_frame_buildings` | remplacement | `investment_banks → steel_frame_buildings` |
| `electric_telegraph → telephone` | suppression | aucun ; `electrical_generation` reste |
| `reinforced_concrete → concrete_dockyards` | suppression | aucun ; `floating_harbor` reste |
| `combustion_engine → military_aviation` | remplacement | `wargaming → military_aviation` |
| `professional_civil_engineering → paved_roads` | remplacement | `steel_frame_buildings → paved_roads` |
| `political_agitation → war_propaganda` | suppression | aucun ; `enlistment_offices` reste |
| `combustion_engine → zeppelins` | remplacement | `steel_frame_buildings → zeppelins` |
| `pneumatic_tools → concrete_fortifications` | suppression | aucun ; `defense_in_depth` reste |
| `reinforced_concrete → concrete_fortifications` | suppression | aucun ; `defense_in_depth` reste |
| `steam_turbine → dreadnought_tech` | suppression | aucun ; `pre_dreadnought_tech` reste |
| `radio → mass_propaganda` | remplacement | `political_agitation → mass_propaganda` |
| `war_propaganda → mass_propaganda` | suppression | aucun ; `political_agitation` et `film` restent |
| `nitrogen_fixation → chemical_warfare` | remplacement | `trench_works → chemical_warfare` |
| `compression_ignition → mobile_armor` | suppression | aucun ; `military_aviation` et `stormtroopers` restent |

Total : 19 arêtes cross-tree retirées, 10 arêtes same-tree ajoutées, 9 suppressions sans remplacement.

## 5. Cas runtime obligatoires

- `modern_nursing` : `battlefield_evacuation` est Military, Ère V, médical et logistique. Il est le propriétaire canonique actif du concept vanilla `triage`.
- `electric_telegraph` : `logistics` restaure le prédécesseur Military vanilla actif. Le bridge optique reste historique mais non bloquant.
- `camera` : `experimental_research_laboratories` fournit la capacité Society d'expérimentation chimique et optique. `realism` n'est pas restauré.
- `military_aviation` : `wargaming` fournit une capacité Military d'expérimentation opérationnelle et d'intégration doctrinale. Le moteur à combustion reste une condition industrielle implicite.
- `dreadnought_tech` : la chaîne Military/Naval directe reste `pre_dreadnought_tech → dreadnought_tech`. La turbine reste implicite.
- `chemical_warfare` : `trench_works` représente le contexte Military opérationnel de la guerre chimique. L'industrie de l'azote reste implicite.
- `mobile_armor` : `military_aviation` et `stormtroopers` conservent les fondations Military de mobilité, armes combinées et infiltration.
- `telephone` : seul `electrical_generation`, Production, reste requis.
- `mass_propaganda` : `political_agitation` et `film`, tous deux Society, couvrent mobilisation politique et média de masse.

## 6. Validation sémantique

Les dix remplacements sont classés `PLAUSIBLE` ou plus forts. Aucun lien n'est justifié par la seule proximité d'Ère :

- propriétaire canonique actif : `battlefield_evacuation` ;
- prédécesseur vanilla actif : `logistics` ;
- capacité scientifique : `experimental_research_laboratories` ;
- ordnance navale : `shell_gun` ;
- financement institutionnel des grands projets : `investment_banks` ;
- expérimentation doctrinale : `wargaming` ;
- continuité d'infrastructure urbaine : `steel_frame_buildings` ;
- mobilisation politique : `political_agitation` ;
- contexte opérationnel des tranchées : `trench_works`.

`ARBITRARY_EDGES = 0`  
`WEAK_EDGES = 0`

## 7. Roots, dead ends et fan-in

| Mesure | Avant | Après |
|---|---:|---:|
| Roots recherchables involontaires VII–XII | 0 | 0 |
| Root non recherchable légitime | `sericulture` | `sericulture` |
| Dead ends VII–XI | 27 | 34 |
| Dead ends VII–XII bruts | 41 | 48 |
| `AVOIDABLE_DEAD_ENDS` | 0 | 0 |

Les sept nouveaux terminaux VII–XI sont `compression_ignition`, `electric_telegraph`, `nitrogen_fixation`, `pneumatic_tools`, `radio`, `reinforced_concrete` et `war_propaganda`. Chacun perd uniquement un faux successeur cross-tree ; aucun successeur artificiel n'a été ajouté pour réduire le compteur.

Distribution finale des prérequis post-1836 :

| Nombre de prérequis | Technologies |
|---:|---:|
| 0 | 1 |
| 1 | 82 |
| 2 | 26 |
| 3 | 2 |
| 4+ | 0 |

## 8. Validation structurelle finale

| Contrôle | Résultat |
|---|---:|
| `ACTIVE_POST1836_TECHS` | 111 |
| `BROKEN_PREREQUISITE_REFERENCES` | 0 |
| `ACTIVE_PREREQUISITES_TO_COMPATIBILITY_ALIASES` | 0 |
| `PREREQUISITE_CYCLES` | 0 |
| `LATER_ERA_PREREQUISITE_INVERSIONS` | 0 |
| `DUPLICATE_TECH_IDS` | 0 |
| `UNINTENDED_RESEARCHABLE_ROOTS` | 0 |
| `POST1836_CROSS_CATEGORY_PREREQUISITE_EDGES` | 0 |
| `PRODUCTION_TARGETS_WITH_NON_PRODUCTION_PREREQ` | 0 |
| `MILITARY_TARGETS_WITH_NON_MILITARY_PREREQ` | 0 |
| `SOCIETY_TARGETS_WITH_NON_SOCIETY_PREREQ` | 0 |
| `ARBITRARY_EDGES` | 0 |
| `WEAK_EDGES` | 0 |
| `AVOIDABLE_DEAD_ENDS` | 0 |

## 9. Diff guard

Les contrôles statiques confirment :

- `ERA_CHANGES = 0`
- `CATEGORY_CHANGES = 0`
- `COST_CHANGES = 0`
- `ICON_CHANGES = 0`
- `EFFECT_CHANGES = 0`
- `UNLOCK_OWNERSHIP_CHANGES = 0`
- `LOCALIZATION_CHANGES = 0`
- `GUI_CHANGES = 0`
- `ERA_I_VI_DEFINITION_CHANGES = 0`
- `COMPATIBILITY_ALIAS_CHANGES = 0`

Le diff gameplay cumulé TECH-4C + TECH-4C1 reste limité aux blocs `unlocking_technologies` du fichier post-1836 autorisé. Les cinq anciens livrables TECH-4C restent préservés et non commités.

## 10. Livrables

- `TECH4C1_VANILLA_TREE_ISOLATION_AUDIT.csv` : 179 technologies vanilla.
- `TECH4C1_CROSS_TREE_EDGE_AUDIT.csv` : 37 arêtes cross-tree avant correction, dont 19 corrigées et 18 I–VI consignées hors périmètre.
- `TECH4C1_SAME_TREE_PREREQUISITE_MATRIX.csv` : 111 technologies VII–XII.
- `TECH4C1_PREREQUISITE_CHANGE_LOG.csv` : 17 listes de prérequis modifiées.

## 11. Checklist runtime utilisateur

Le runtime n'est pas déclaré PASS. Vérifier manuellement :

- retour des lignes entrantes visibles ;
- `modern_nursing` relié correctement ;
- `electric_telegraph` relié correctement ;
- disparition des cartes post-1836 paraissant isolées ;
- disparition des lignes post-1836 traversant plusieurs arbres ;
- aucun trait vers le vide ;
- aucun alias TECH-3B visible ;
- progression naturelle dans Production ;
- progression naturelle dans Military/Naval ;
- progression naturelle dans Society ;
- continuité jusqu'à l'Ère XII.

## 12. Statut

`TECH4C1_SAME_TREE_PREREQUISITES_STATIC_PASS_RUNTIME_PENDING`
