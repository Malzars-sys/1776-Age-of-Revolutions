# TECH6A-3 — Spices — rapport d’implémentation

Date : 2026-08-28

Runtime : à exécuter par l’utilisateur

Commit / push : non effectués

## Résultat

Le système `spices` est implémenté comme bien de luxe commercialisable, produit par `building_spice_plantation`, consommé directement par le besoin POP `popneed_luxury_food` et par une nouvelle chaîne additive des industries alimentaires.

Les instructions utilisateur postérieures à la spécification ont été intégrées dans le document de conception :

- plantation de base : **20 spices** au lieu de 15 ;
- plantation mécanisée : **45 spices** au lieu de 35 ;
- aucune modification directe de `pm_sweeteners` ou `pm_baking_powder` ;
- nouvelle chaîne indépendante de préparations épicées dans `building_food_industry`.

## Bien et demande

`spices` utilise les valeurs suivantes :

- coût de base : 60 ;
- catégorie : luxury ;
- prestige factor : 10 ;
- convoy cost multiplier : 0.25 ;
- traded quantity : 10 ;
- obsession chance : 3.0.

Dans `popneed_luxury_food` :

- weight : 2.00 ;
- max supply share : 0.50 ;
- min supply share : 0.02.

## Plantation

Le bâtiment `building_spice_plantation` appartient à `bg_spice_plantations`, enfant du groupe vanilla `bg_plantations`. Il reprend l’architecture rurale vanilla : propriété autonome, coût de construction faible, PMG de base et PMG de transport ferroviaire.

| Méthode | Technologie | Inputs | Output | Emplois |
|---|---|---|---:|---:|
| `pm_spice_cultivation` | aucune | aucun | 20 spices | 9 000 laborers + 1 000 farmers |
| `pm_mechanized_spice_cultivation` | `mechanized_irrigation` | 5 engines | 45 spices | 6 000 laborers + 1 000 farmers + 500 machinists |

## Nouvelle chaîne Food Industries

Le PMG `pmg_spiced_food_building_food_industry` est ajouté au bâtiment sans remplacer les chaînes de base, de mise en conserve, de distillerie ou d’automatisation.

| Méthode | Technologie | Inputs | Output additionnel |
|---|---|---|---:|
| `pm_no_spiced_food` | aucune | aucun | 0 groceries |
| `pm_spiced_food_preparations` | `distillation` | 5 spices + 5 coffee | 20 groceries |
| `pm_refined_spiced_food_preparations` | `baking_powder` | 10 spices + 15 coffee | 45 groceries |

Le premier gate représente la maîtrise ancienne de la transformation et des extraits ; le second conserve une progression cohérente avec la recette alimentaire avancée déjà présente dans le mod.

## Géographie et setup 1776

- Régions éligibles : 28 exactement, toutes et seulement celles du CSV dont le potentiel est supérieur à zéro.
- Somme de l’indice de potentiel du CSV : 442.
- Régions productrices au départ : 18.
- Niveaux de plantation au départ : 87.
- `STATE_WEST_INDIES` reste exclu.
- Zanzibar, Madagascar, Cambodge, Bangkok/Siam, Tonkin, Annam, Guatemala, Honduras et Bornéo oriental ont le potentiel mais aucun bâtiment initial.

La syntaxe vanilla des plantations est une liste d’éligibilité `arable_resources` : l’indice numérique de potentiel du CSV reste donc un indicateur de conception et de contrôle de distribution. La capacité construisible en jeu est partagée avec l’`arable_land` de l’État, comme pour les autres plantations vanilla.

Les bâtiments initiaux sont placés dans des `region_state` qui existent réellement dans le setup 1776. Les principaux choix sont DEI pour les Moluques/Ceylan/Java, TRA pour Travancore, ACE pour Aceh, INDOP pour Sumatra, JOH pour Malaya, MYS pour Mysore, GBR pour la Jamaïque et SC1 pour Veracruz.

## Assets

- `epice.dds` → `gfx/interface/icons/goods_icons/spices.dds` ;
- `epice de lux.dds` → `gfx/interface/icons/goods_icons/prestige_goods/generic_spices_prestige.dds` ;
- `plantation d'epice.dds` → `gfx/interface/icons/building_icons/building_spice_plantation.dds`.

Les trois fichiers ont un en-tête DDS valide. Le bien normal, le bien de prestige différé et le bâtiment possèdent chacun leur texticon/localisation EN et FR lorsque nécessaire. Aucun objet de prestige n’est créé dans cette phase.

## QA statique

```text
SPICES_GOOD_DEFINED = YES
SPICES_BASE_PRICE = 60
SPICES_CATEGORY = luxury
SPICE_PLANTATION_DEFINED = YES
SPICE_BASE_OUTPUT = 20
SPICE_BASE_EMPLOYMENT = 10000
SPICE_ADV_OUTPUT = 45
SPICE_ADV_ENGINES_INPUT = 5
SPICE_ADV_EMPLOYMENT = 7500
SPICED_FOOD_BASIC = 5 spices + 5 coffee -> 20 groceries
SPICED_FOOD_REFINED = 10 spices + 15 coffee -> 45 groceries
RESOURCE_REGIONS_WITH_POTENTIAL = 28
CSV_POTENTIAL_TOTAL = 442
STARTING_REGIONS_1776 = 18
STARTING_LEVELS_1776 = 87
INVALID_STATE_REGION_IDS = 0
INVALID_REGION_STATE_OWNER_REFS = 0
DUPLICATE_NEW_IDS = 0
INVALID_TECH_REFS = 0
BRACE_OR_QUOTE_ERRORS = 0
LOCALIZATION_BOM_ERRORS = 0
GABELLE_FILES_TOUCHED = 0
SALT_BALANCE_CHANGED = NO
COUNTRY_STARTING_TECH_FILES_TOUCHED = 0
STARTING_TECH_ASSIGNMENT = DEFERRED
RUNTIME = USER_REQUIRED
COMMIT = NO
PUSH = NO
```

## TECH6A-3R — FIRST RUNTIME CORRECTIONS

Le premier runtime a validé le bien `spices`, son icône de marché, son marché, `building_spice_plantation`, `pm_spice_cultivation`, `pm_mechanized_spice_cultivation` et l’output avancé de 45 épices.

### Cause du café manquant

Les objets `pm_spiced_food_preparations` et `pm_refined_spiced_food_preparations` contenaient déjà respectivement `goods_input_coffee_add = 5` et `goods_input_coffee_add = 15` dans le bon bloc `building_modifiers/workforce_scaled`.

Le bug venait du registre des types de modificateurs : Victoria 3 1.13.9 définit `goods_output_coffee_add`, mais aucun `goods_input_coffee_add`, car aucun PM vanilla n’utilise le café comme input industriel. Le moteur ignorait donc la clé non enregistrée ; elle n’avait aucun effet et n’apparaissait pas dans le tooltip.

Correction effectuée dans `common/modifier_type_definitions/10_tech6a3_spices_modifier_types.txt` : ajout du type `goods_input_coffee_add`, avec les localisations anglaise et française correspondantes. Les deux objets exécutés restent définis dans `common/production_methods/10_tech6a3_spices.txt` :

- `pm_spiced_food_preparations` : 5 spices + 5 coffee → 20 groceries ;
- `pm_refined_spiced_food_preparations` : 10 spices + 15 coffee → 45 groceries.

### Icônes des PM

Les deux champs `texture` sont présents et leurs fichiers vanilla 1.13.9 ont été vérifiés :

- `pm_spiced_food_preparations` → `gfx/interface/icons/production_method_icons/sweeteners.dds` ;
- `pm_refined_spiced_food_preparations` → `gfx/interface/icons/production_method_icons/baking_powder.dds`.

Aucun nouvel asset n’a été créé. Un redémarrage complet du jeu est requis pour recharger les définitions et confirmer l’affichage.

### Périmètre préservé

La carte des ressources, les 87 niveaux de départ, les outputs 20/45 des plantations, le besoin POP, le sel, la Gabelle, les technologies de départ et les objets de prestige n’ont pas été modifiés. L’habillage final du DDS de plantation reste un travail utilisateur.

```text
PM_SPICED_FOOD_SPICES_INPUT = 5
PM_SPICED_FOOD_COFFEE_INPUT = 5
PM_SPICED_FOOD_GROCERIES_OUTPUT = 20
PM_REFINED_SPICED_FOOD_SPICES_INPUT = 10
PM_REFINED_SPICED_FOOD_COFFEE_INPUT = 15
PM_REFINED_SPICED_FOOD_GROCERIES_OUTPUT = 45
PM_SPICED_FOOD_TEXTURE_VALID = YES
PM_REFINED_SPICED_FOOD_TEXTURE_VALID = YES
SPICE_RESOURCE_MAP_CHANGED = NO
SPICE_STARTING_BUILDINGS_CHANGED = NO
SPICE_PLANTATION_BALANCE_CHANGED = NO
SPICES_POP_NEED_CHANGED = NO
SALT_FILES_TOUCHED = 0
GABELLE_FILES_TOUCHED = 0
STARTING_TECH_FILES_TOUCHED = 0
TECH6A3R_RUNTIME_CORRECTIONS = PASS
COFFEE_INPUT_BUG_FIXED = YES
SPICED_PM_ICON_FIXED = YES
REFINED_SPICED_PM_ICON_FIXED = YES
SPICE_PLANTATION_FINAL_ICON = USER_ASSET_PENDING
PRESTIGE_GOODS = DEFERRED
GAME_RUNTIME_RETEST = USER_REQUIRED
COMMIT = NO
PUSH = NO
```

## Checklist runtime utilisateur

1. Lancer une nouvelle partie au 1er janvier 1776 avec le mod seul ou la liste de mods prévue.
2. Vérifier que **Épices** apparaît dans le marché avec l’icône `epice.dds`.
3. Vérifier les texticons dans les infobulles de production et de consommation.
4. Ouvrir Moluques, Ceylan, Travancore et Aceh : les plantations doivent être présentes aux niveaux 15, 12, 10 et 8.
5. Vérifier le total mondial initial de 87 niveaux répartis entre 18 régions.
6. Vérifier l’absence de plantation initiale à Zanzibar, Madagascar, Cambodge/Siam et dans les Antilles hors Jamaïque.
7. Vérifier que la plantation n’est constructible que dans les 28 régions du CSV et consomme de la terre arable.
8. Vérifier le PM de base : 20 épices et 10 000 emplois par niveau.
9. Avec `mechanized_irrigation`, vérifier le PM avancé : 45 épices, 5 moteurs et 7 500 emplois.
10. Dans les industries alimentaires, vérifier une quatrième chaîne indépendante « Préparations épicées » en plus des chaînes existantes.
11. Avec `distillation`, vérifier 5 épices + 5 café → 20 aliments.
12. Avec `baking_powder`, vérifier 10 épices + 15 café → 45 aliments.
13. Vérifier que les PM édulcorants et levure chimique conservent leurs inputs/outputs précédents, notamment le sel.
14. Laisser tourner plusieurs semaines et observer production, demande POP, consommation industrielle, prix et commerce.
15. Vérifier qu’aucune erreur `spices`, PM/PMG, building, localisation ou texture n’apparaît dans `error.log`.
