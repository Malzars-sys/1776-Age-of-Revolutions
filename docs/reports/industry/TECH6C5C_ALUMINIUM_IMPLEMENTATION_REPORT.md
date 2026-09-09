# TECH6C5C — Rapport d’implémentation de la métallurgie de l’aluminium

## 1. Résultat

**TECH6C5C RESULT: PASS (validation statique).**

L’aluminium est implémenté comme bien industriel tardif produit par une usine de métallurgie non ferreuse. La chaîne ne crée ni bauxite, ni alumine, ni mine, ni ressource d’État. Deux débouchés ciblés sont ajoutés : avions entièrement métalliques et conducteurs électriques substituables au cuivre.

**Nombre de nouvelles technologies : 0.**

## 2. Stratégie technologique

La documentation canonique de Victoria 3 1.13.11 confirme explicitement que `unlocking_technologies` est une liste de technologies **requises** :

- `C:/Games/Victoria 3/game/common/buildings/buildings.md` : « optional list of required technologies » pour construire un bâtiment ;
- `C:/Games/Victoria 3/game/common/production_methods/production_methods.md` : même sémantique pour activer un PM.

Le fork fournit en plus des exemples fonctionnels dans `common/production_methods/04_plantations.txt` : les PM sucriers à vapeur combinent `sugar_refining` avec `high_pressure_steam`, `watertube_boiler` ou `rotary_valve_engine`. Les entrées multiples expriment donc bien une conjonction, et non une alternative.

Les verrous retenus sont :

| Objet | Technologies existantes requises |
|---|---|
| `building_non_ferrous_metallurgy_works` | `electrical_capacitors` ET `industrial_alkalis` |
| `pm_hall_heroult_process` | `electrical_capacitors` ET `industrial_alkalis` |
| `pm_all_metal_aircraft` | `military_aviation` ET `electrical_capacitors` ET `industrial_alkalis` |
| `pm_aluminium_conductors_building_power_plant` | `electrical_capacitors` ET `industrial_alkalis` |

`industrial_alkalis` est en `era_5`, parent `industrial_acids`. `electrical_capacitors` est en `era_9`, avec `electrical_generation` et `mechanized_weaving` comme parents. `military_aviation`, seul nœud local explicitement aéronautique et donc le plus tardif historiquement approprié, est en `era_10`, parent `wargaming`.

Aucun parent technologique n’a été modifié et `gui/tech_tree.gui` est inchangé.

## 3. Bien aluminium

`aluminium` possède :

- `cost = 80` ;
- `category = industrial` ;
- `tradeable = yes` ;
- aucune consommation directe des POP ;
- `gfx/error_deer.dds` comme visuel temporaire.

L’orthographe canonique britannique/internationale est utilisée partout dans les nouveaux IDs. Aucun ID parallèle `aluminum` n’est introduit.

## 4. Infrastructure du bien personnalisé

Le propriétaire unifié TECH6C est étendu avec exactement quatre modificateurs :

- `goods_input_aluminium_add` ;
- `goods_input_aluminium_mult` ;
- `goods_output_aluminium_add` ;
- `goods_output_aluminium_mult`.

Les libellés de modificateurs directs et `modifier_` sont présents en anglais et en français. Le texticon `@aluminium!` utilise `gfx/error_deer.dds`. Les fichiers de localisation concernés sont en UTF-8 avec BOM.

## 5. Usine de métallurgie non ferreuse

```text
building_non_ferrous_metallurgy_works
building_group = bg_heavy_industry
city_type = city
required_construction = construction_cost_very_high
ownership_type = self
unlock = electrical_capacitors AND industrial_alkalis
PMG = pmg_base_building_non_ferrous_metallurgy_works
```

Le bâtiment reste exclusivement consacré à l’aluminium. Le cuivre demeure produit par `building_copper_mine`.

Le PMG ne contient que `pm_hall_heroult_process`. Aucun PM neutre n’est nécessaire, puisque le bâtiment et son unique procédé possèdent le même double verrou technologique.

## 6. Procédé Hall-Héroult

Les prix locaux sont inchangés : produits chimiques industriels 40, charbon 30, électricité 30, aluminium 80.

```text
INPUT  20 industrial_chemicals = 800
INPUT  10 coal                 = 300
INPUT  50 electricity          = 1 500
TOTAL INPUT                    = 2 600

OUTPUT 40 aluminium            = 3 200
GROSS PRE-WAGE MARGIN          = 600
```

L’électricité représente 57,7 % de la valeur des intrants. La production reste viable, mais dépend réellement d’un approvisionnement électrique abondant.

Composition de l’emploi :

- 500 commerçants ;
- 2 500 ouvriers ;
- 1 250 machinistes ;
- 750 ingénieurs ;
- total : 5 000.

La pollution `20` est placée correctement dans `state_modifiers -> workforce_scaled`. Aucun intrant factice ne représente la bauxite ou l’alumine.

## 7. Avions entièrement métalliques

L’architecture existante a été conservée : `pmg_aeroplanes` est un PMG additif de l’industrie automobile qui transforme une partie de sa production d’automobiles en avions.

La méthode ancienne reste inchangée :

```text
4 hardwood + 4 fabric + opportunity cost of 10 automobiles
-> 10 aeroplanes
```

Aux prix de base : intrants et production abandonnée 1 240, avions 800, marge additive `-440`. Comme pour de nombreux biens militaires, la rentabilité dépend d’un prix de demande supérieur au prix de base.

La nouvelle méthode est :

```text
pm_all_metal_aircraft
gate = military_aviation AND electrical_capacitors AND industrial_alkalis
10 aluminium + opportunity cost of 10 automobiles
-> 20 aeroplanes
employment delta = +500 engineers
```

Valeur effective des intrants : 1 800. Valeur des avions : 1 600. Marge additive : `-200`. Le PM double la production aéronautique, améliore la marge par rapport à l’avion ancien et remplace totalement le bois dur et la toile par un intrant aluminium significatif. Il ne modifie pas le PM aéronautique ancien.

## 8. Conducteurs électriques

La solution sûre est un PMG additif sans emplois :

```text
pmg_electrical_conductors_building_power_plant
  -> pm_copper_conductors_building_power_plant
  -> pm_aluminium_conductors_building_power_plant
```

Le fichier vanilla `common/buildings/06_urban_center.txt` est recopié localement et conserve une parité sémantique complète avec le canon, hormis l’ajout de ce PMG au `building_power_plant`.

Options :

| Méthode | Disponibilité | Intrant | Coût de base | Effet |
|---|---|---:|---:|---|
| Conducteurs en cuivre | dès `electrical_generation`, choix par défaut | 2 cuivre | 100 | service de conducteurs pour le PM électrique sélectionné |
| Conducteurs en aluminium | `electrical_capacitors` ET `industrial_alkalis` | 1 aluminium | 80 | substitution complète du cuivre |

Le seuil d’indifférence est un prix de l’aluminium de 100 : en dessous, l’aluminium est moins coûteux; au-dessus, le cuivre redevient économiquement préférable.

Les `2 copper` de `pm_early_power_plant` sont déplacés, pas supprimés, vers le choix cuivre. Ainsi :

- les premiers réseaux utilisent obligatoirement le cuivre ;
- les centrales ultérieures utilisent également le cuivre par défaut ;
- la substitution aluminium n’apparaît qu’avec la capacité technologique de produire l’aluminium ;
- aucun PM ne consomme simultanément cuivre et aluminium ;
- aucun emploi n’est compté deux fois.

## 9. Interaction avec le cuivre

Les consommateurs cuivre suivants restent inchangés :

- doublage en cuivre des chantiers navals : 5 ;
- téléphones : 15 ;
- moteurs électriques : 10 ;
- radios : 2.

La demande des premières centrales reste 2 cuivre par niveau via le nouveau PMG. Les centrales avancées utilisent aussi le cuivre tant que le joueur ne choisit pas explicitement les conducteurs aluminium. L’aluminium n’est donc ni une substitution universelle ni une suppression de la chaîne cuivre.

## 10. Estimation indicative de l’offre et de la demande

Chaque niveau d’usine produit 40 aluminium. Les deux consommateurs demandent :

- 10 aluminium par niveau d’industrie automobile utilisant les avions entièrement métalliques ;
- 1 aluminium par niveau de centrale utilisant les conducteurs aluminium.

| Usines non ferreuses | Offre | Exemple de demande | Demande | Utilisation |
|---:|---:|---|---:|---:|
| 10 | 400 | 20 niveaux automobiles + 100 centrales | 300 | 75 % |
| 25 | 1 000 | 50 niveaux automobiles + 300 centrales | 800 | 80 % |
| 50 | 2 000 | 100 niveaux automobiles + 750 centrales | 1 750 | 87,5 % |

Les deux débouchés suffisent pour une première économie industrielle cohérente : l’avion absorbe l’essentiel du volume, tandis que les conducteurs offrent une demande large mais légère. Le risque principal reste un excès d’offre dans un marché pacifique construisant peu d’avions et conservant ses conducteurs cuivre. Ce risque doit être mesuré en jeu avant d’ajouter d’autres consommateurs.

## 11. Ressources d’État

TECH6C5C modifie **zéro** fichier `map_data/state_regions`.

Le hash agrégé des 16 fichiers avant et après l’implémentation reste :

```text
3BAA853AD5EC5D9626330EA4B93FFA4BFA726DE300DB92773B6670FCB69BFE21
```

Il existe zéro ressource d’État aluminium, aluminum, bauxite ou alumine.

## 12. Validation statique

`tools/tech6c5c_validate.py` retourne **PASS** :

- bien aluminium défini exactement une fois ;
- bâtiment défini exactement une fois ;
- PM et PMG uniques ;
- toutes les références de PM résolues ;
- tous les biens utilisés sont connus ;
- quatre types de modificateur présents ;
- texticon présent ;
- localisations anglaise et française présentes sans nouvelle clé dupliquée ;
- aucun `ggoods_`, `oods_` orphelin ou `goods_aluminium_add` ;
- aucun ID `aluminum` introduit ;
- tous les nouveaux visuels temporaires utilisent `gfx/error_deer.dds` ;
- accolades équilibrées ;
- parité sémantique du fichier de bâtiments urbains avec la vanilla, hors ajout du PMG : vraie ;
- graphe technologique : 285 nœuds, zéro cycle, zéro nouvelle technologie aluminium ;
- parents des trois technologies utilisées inchangés ;
- `gui/tech_tree.gui` inchangé ;
- état des 16 fichiers de carte identique au début et à la fin de TECH6C5C ;
- `git diff --check` réussi, avec seulement les avertissements informatifs LF/CRLF sous Windows.

Aucun démarrage du jeu ni contrôle visuel du marché, des texticons ou des sélecteurs de PM n’a été réalisé. La validation statique ne constitue pas une preuve d’exécution dans l’interface.

## 13. Fichiers créés

- `common/goods/14_tech6c5c_aluminium.txt`
- `common/buildings/14_tech6c5c_non_ferrous_metallurgy_works.txt`
- `common/buildings/06_urban_center.txt` — copie locale canonique nécessaire pour rattacher le PMG de conducteurs
- `common/production_method_groups/14_tech6c5c_aluminium_pmgs.txt`
- `common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt`
- `localization/english/tech6c5c_aluminium_l_english.yml`
- `localization/french/tech6c5c_aluminium_l_french.yml`
- `docs/reports/industry/TECH6C5C_ALUMINIUM_IMPLEMENTATION_REPORT.md`
- `docs/reports/industry/TECH6C5C_ALUMINIUM_CONSUMER_MATRIX.csv`
- `docs/reports/industry/TECH6C5C_ALUMINIUM_ECONOMIC_VALIDATION.csv`
- `tools/tech6c5c_validate.py`

## 14. Fichiers modifiés

- `common/modifier_type_definitions/12_tech6c_custom_goods_modifier_types.txt`
- `common/production_method_groups/01_industry.txt`
- `common/production_methods/06_urban_center.txt`
- `gui/tech6c_goods_texticons.gui`
- `localization/english/tech6c_goods_modifiers_l_english.yml`
- `localization/french/tech6c_goods_modifiers_l_french.yml`

Aucun fichier de technologie ou de région d’État n’est modifié par TECH6C5C. Les changements cuivre, ciment et leurs rapports déjà présents dans le worktree sont préservés.

## 15. Consommateurs explicitement différés

Ne sont pas ajoutés à ce stade : carrosseries automobiles, automobiles de masse, chars, trains et wagons, construction, navires, emballages, appareils domestiques, radios et autres machines électriques.

## 16. Portée recommandée pour TECH6C5D

TECH6C5D devrait être une phase de validation économique et runtime, pas une nouvelle expansion automatique :

1. démarrer une partie de test et vérifier les quatre types de modificateurs, le texticon, le marché et les sélecteurs de PM ;
2. observer la construction IA de l’usine non ferreuse et la sélection Hall-Héroult ;
3. mesurer prix, emploi et débit avec 10, 25 et 50 niveaux ;
4. vérifier que l’IA ne bascule pas vers l’aluminium lorsque son prix dépasse le seuil économique ;
5. mesurer la demande cuivre après introduction du choix de conducteurs ;
6. seulement si l’aluminium s’effondre durablement faute de demande, auditer un unique débouché supplémentaire parmi les automobiles de masse ou les wagons légers ;
7. seulement si l’offre est insuffisante, ajuster d’abord la recette Hall-Héroult avant d’ajouter des producteurs ou des biens intermédiaires.

Les modifications ne sont ni commitées ni poussées.
