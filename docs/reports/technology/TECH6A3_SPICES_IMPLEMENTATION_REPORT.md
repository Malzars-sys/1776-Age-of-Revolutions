# TECH6A-3 — Spices — rapport d’implémentation

Date : 2026-08-28

Runtime : à exécuter par l’utilisateur

Commit / push : non effectués

## Résultat

Le système `spices` est implémenté comme bien de luxe commercialisable, produit par `building_spice_plantation`, consommé directement par le besoin POP `popneed_luxury_food` et comme input industriel d’une nouvelle chaîne `fine_food` des industries alimentaires.

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

| Méthode | Technologie | Inputs | Conversion d’output |
|---|---|---|---|
| `pm_no_spiced_food` | aucune | aucun | aucune |
| `pm_spiced_food_preparations` | `distillation` | 5 spices + 5 coffee + 10 wine | -15 groceries, +20 fine_food |
| `pm_refined_spiced_food_preparations` | `baking_powder` | 10 spices + 15 coffee + 20 wine | -30 groceries, +55 fine_food |

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
- `plantation_epice_finalisee.dds` → `gfx/interface/icons/building_icons/building_spice_plantation.dds` ;
- `nouriture de lux(met rafiné).dds` → `gfx/interface/icons/goods_icons/fine_food.dds` ;
- icône violette finale sans étoiles → `gfx/interface/icons/production_method_icons/spiced_food_preparations.dds` ;
- icône violette finale avec deux étoiles → `gfx/interface/icons/production_method_icons/refined_spiced_food_preparations.dds` ;
- icône violette finale barrée → `gfx/interface/icons/production_method_icons/no_fine_food_preparations.dds`.

Tous les fichiers ont un en-tête DDS valide. Les biens, le prestige spices, le bâtiment et les deux PM possèdent les textures, texticons et localisations EN/FR nécessaires. L’objet de prestige final est `prestige_good_fine_batavian_spices`.

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
SPICED_FOOD_BASIC = 5 spices + 5 coffee + 10 wine; -15 groceries output; +20 fine_food
SPICED_FOOD_REFINED = 10 spices + 15 coffee + 20 wine; -30 groceries output; +55 fine_food
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

- `pm_spiced_food_preparations` : 5 spices + 5 coffee + 10 wine, -15 groceries output, +20 fine_food ;
- `pm_refined_spiced_food_preparations` : 10 spices + 15 coffee + 20 wine, -30 groceries output, +55 fine_food.

### Icônes des PM

Les deux champs `texture` sont présents et leurs fichiers vanilla 1.13.9 ont été vérifiés :

- `pm_spiced_food_preparations` → `gfx/interface/icons/production_method_icons/spiced_food_preparations.dds` ;
- `pm_refined_spiced_food_preparations` → `gfx/interface/icons/production_method_icons/refined_spiced_food_preparations.dds`.

Aucun nouvel asset n’a été créé. Un redémarrage complet du jeu est requis pour recharger les définitions et confirmer l’affichage.

### Périmètre préservé

La carte des ressources, les 87 niveaux de départ, les outputs 20/45 des plantations, le besoin POP, le sel, la Gabelle, les technologies de départ et les objets de prestige n’ont pas été modifiés. L’habillage final du DDS de plantation reste un travail utilisateur.

```text
PM_SPICED_FOOD_SPICES_INPUT = 5
PM_SPICED_FOOD_COFFEE_INPUT = 5
PM_SPICED_FOOD_WINE_INPUT = 10
PM_SPICED_FOOD_GROCERIES_OUTPUT_ADJUSTMENT = -15
PM_SPICED_FOOD_FINE_FOOD_OUTPUT = 20
PM_REFINED_SPICED_FOOD_SPICES_INPUT = 10
PM_REFINED_SPICED_FOOD_COFFEE_INPUT = 15
PM_REFINED_SPICED_FOOD_WINE_INPUT = 20
PM_REFINED_SPICED_FOOD_GROCERIES_OUTPUT_ADJUSTMENT = -30
PM_REFINED_SPICED_FOOD_FINE_FOOD_OUTPUT = 55
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
SPICE_PLANTATION_FINAL_ICON = INTEGRATED
PRESTIGE_GOODS = DEFERRED
GAME_RUNTIME_RETEST = USER_REQUIRED
COMMIT = NO
PUSH = NO
```

## TECH6A-3F — FINAL POLISH / FINE FOOD

### Nouveau bien et besoins POP

`fine_food` (**Mets raffinés / Fine Food**) est un bien de luxe commercialisable de prix 50, avec `prestige_factor = 6`, `convoy_cost_multiplier = 0.5`, `traded_quantity = 5` et `obsession_chance = 1.0`.

Il satisfait simultanément :

- `popneed_basic_food` : weight 1.50, max share 1.00, min share 0.00 ;
- `popneed_luxury_food` : weight 2.50, max share 1.00, min share 0.00.

La demande directe de `spices` dans `popneed_luxury_food` est conservée sans modification. Aucun bonus artificiel de niveau de vie n’est ajouté.

### Conversion des aliments

Les valeurs négatives de groceries sont des ajustements d’**output**, pas des inputs. La chaîne principale du bâtiment continue donc de produire ses groceries, tandis que le PM actif en détourne une partie vers `fine_food`.

### Audit des gates Society

Décision : `KEEP_CURRENT_GATE`.

| Gate | Branche / ère | Prérequis dans l’arbre du mod | Analyse |
|---|---|---|---|
| `distillation` | Production / era_1 | aucun | Gate actuel cohérent avec la transformation alimentaire et déjà utilisé par le PM vanilla Sweeteners. |
| `baking_powder` | Production / era_7 | `industrial_acids`, `sugar_refining` | Gate actuel explicitement alimentaire, adapté au PM avancé. |
| `codified_practical_knowledge` | Society / era_3 | `institutionalized_scientific_exchange`, `periodical_print_networks` | Candidat général sur la diffusion des savoirs, mais sans lien alimentaire explicite. |
| `colonization` | Society / era_4 | `international_relations` | Candidat lié aux produits coloniaux, mais il ferait dépendre une technique culinaire d’une politique impériale. |
| `specialized_professional_societies` | Society / era_5 | `specialized_technical_academies`, `experimental_research_laboratories` | Évoque la professionnalisation, mais reste trop tardif et trop large pour la gastronomie. |

Aucun candidat Society n’est clairement supérieur aux gates productifs actuels ; aucun changement de technologie n’est appliqué.

### Prestige inputs

Le mécanisme reste entièrement natif : les variantes prestige déclarent leur `base_good` (`spices`, `coffee`, `wine`) et le define existant `PRESTIGE_GOODS_INPUT_THROUGHPUT_BONUS = 0.2` applique le bonus maximal de throughput. Aucun bonus spécifique n’est codé dans les PM.

### La Gabelle

```text
LA_GABELLE_PERMISSION = GRANTED
PERMISSION_DATE = 2026-08-28
ORIGINAL_AUTHOR = Tokugawa_Mori
```

Les exclusions locales Git liées à l’attente d’autorisation ont été retirées. Une attribution bilingue a été ajoutée dans `docs/workshop/STEAM_WORKSHOP_CREDITS.md`. Aucun statut de licence spécifique n’a été inventé.

### Balance différée

`SPICES_GLOBAL_BALANCE = DEFERRED_UNTIL_NAVAL_CONVOY_SETUP_FIXED`. La carte, les 87 niveaux initiaux, les outputs 20/45 de la plantation et la consommation directe des POPs restent figés.

### QA finale TECH6A-3F

```text
FINE_FOOD_DEFINED = YES
FINE_FOOD_ICON = YES
FINE_FOOD_BASE_PRICE = 50
FINE_FOOD_CATEGORY = luxury
FINE_FOOD_BASIC_FOOD = YES
FINE_FOOD_BASIC_MAX_SHARE = 1.00
FINE_FOOD_LUXURY_FOOD = YES
FINE_FOOD_LUXURY_MAX_SHARE = 1.00
SPICES_DIRECT_POP_CONSUMPTION = PRESERVED
SPICED_PM = 5 spices + 5 coffee + 10 wine; -15 groceries output; +20 fine_food
REFINED_SPICED_PM = 10 spices + 15 coffee + 20 wine; -30 groceries output; +55 fine_food
VOC_PRESTIGE_GOOD = prestige_good_fine_batavian_spices
VOC_JAVA_COFFEE = NO
NHM_JAVA_COFFEE = YES
OLD_PRESTIGE_SPICE_ID_REFERENCES = 0
PRESTIGE_INPUT_THROUGHPUT_DEFINE = 0.20
VOC_JAVA_SPICE_OWNERSHIP = 8/8
INVALID_GOODS_REFERENCES = 0
INVALID_PM_REFERENCES = 0
INVALID_PRESTIGE_REFERENCES = 0
MISSING_LOCALIZATION = 0
MISSING_TEXTURES = 0
SOCIETY_GATE_AUDIT = KEEP_CURRENT_GATE
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
11. Avec `distillation`, vérifier 5 épices + 5 café + 10 vin, -15 aliments en output et +20 mets raffinés.
12. Avec `baking_powder`, vérifier 10 épices + 15 café + 20 vin, -30 aliments en output et +55 mets raffinés.
13. Vérifier que les PM édulcorants et levure chimique conservent leurs inputs/outputs précédents, notamment le sel.
14. Laisser tourner plusieurs semaines et observer production, demande POP, consommation industrielle, prix et commerce.
15. Vérifier qu’aucune erreur `spices`, PM/PMG, building, localisation ou texture n’apparaît dans `error.log`.
16. Vérifier que **Mets raffinés** apparaît dans le marché, est commercialisable et utilise l’icône fournie.
17. Vérifier que les POPs peuvent substituer Mets raffinés dans les besoins nourriture de base et nourriture de luxe.
18. Vérifier les nouvelles icônes de **Nourriture épicée** et **Nourriture raffinée épicée**.
19. Vérifier l’icône barrée de **Aucune préparation raffinée**.
20. Vérifier que le DDS finalisé de la plantation d’épices remplace bien l’ancienne illustration.
21. Vérifier qu’une part d’inputs prestige spices, coffee ou wine augmente le throughput selon le mécanisme vanilla, sans dépasser le bonus défini de 20 %.

## TECH6A-3F-R1 — Runtime UI correction

L’utilisateur a validé en jeu tous les tests fonctionnels TECH6A-3F : bien, besoins POP, PM, outputs, compagnies, ownership et prestige. Le seul défaut observé était visuel dans la ligne condensée des Industries alimentaires.

Avec cinq groupes de méthodes, les icônes occupent `5 × 72 = 360 px`. Le panneau vanilla conservait simultanément une zone de `230 px` pour les barres d’emploi et de réserves dans une largeur totale de `540 px`, ce qui recouvrait le cinquième groupe `pmg_automation_building_food_industry`.

Correction dans le shadow vanilla 1.13.9 `gui/building_details_panel.gui` :

- tous les bâtiments autres que `building_food_industry` conservent les barres vanilla de 230 px ;
- `building_food_industry` utilise des barres de 170 px ;
- les cinq icônes de PM restent à leur taille vanilla de 70 px ;
- aucun PM, PMG, input, output, emploi ou gate technologique n’est modifié.

```text
TECH6A3F_RUNTIME_GAMEPLAY = PASS
FOOD_INDUSTRY_PM_GROUPS = 5
FOOD_INDUSTRY_AUTOMATION_GROUP_PRESERVED = YES
FOOD_INDUSTRY_CONDENSED_PROGRESSBAR_WIDTH = 170
OTHER_BUILDINGS_CONDENSED_PROGRESSBAR_WIDTH = 230
PM_GAMEPLAY_VALUES_CHANGED = NO
UI_RUNTIME_RETEST = USER_REQUIRED
```

### Correction complémentaire du résumé des bâtiments

Le premier correctif visait la vue table large du navigateur et n'agissait pas sur la liste compacte de 540 px montrée par le test runtime. Dans cette liste compacte, les PM commencent à la position horizontale 110 et les boutons d'interaction sont ancrés à droite. Avec l'espacement vanilla de 52 px et des emplacements de 50 px, le cinquième groupe de l'industrie alimentaire recouvrait directement le bouton de nationalisation.

Le shadow vanilla 1.13.9 correct est désormais `gui/production_methods.gui`. Seule la grille des PM du type `buildings_production_method_item` est compactée :

- espacement horizontal : 42 px au lieu de 52 px ;
- largeur de l'emplacement individuel : 40 px au lieu de 50 px ;
- largeur totale utilisée par cinq PM : 208 px ;
- positions et tailles des boutons de nationalisation, privatisation, subvention et extension inchangées.

L'icône affichée dans chaque emplacement reste à sa taille vanilla de 40 px. Le shadow inutile `gui/building_browser_panel.gui` créé pendant la première tentative a été retiré. Aucun PM, panneau détaillé ou effet de gameplay n'est modifié.

```text
COMPACT_BUILDING_SUMMARY_WIDTH = 540
COMPACT_BUILDING_PM_START_X = 110
COMPACT_BUILDING_PM_SLOT_SPACING = 42
COMPACT_BUILDING_PM_ITEM_WIDTH = 40
COMPACT_BUILDING_FIVE_PM_EXTENT = 208
FOOD_INDUSTRY_FIFTH_PM_VISIBLE = EXPECTED
COMPACT_BUILDING_ACTION_BUTTONS_CHANGED = NO
COMPACT_BUILDING_GAMEPLAY_CHANGED = NO
COMPACT_BUILDING_RUNTIME_RETEST = USER_REQUIRED
```

Les trois icônes initiales du nouveau PMG étaient trop détaillées, brillantes et saturées par rapport aux icônes vanilla. Le prompt de restylisation image-to-image est conservé dans `docs/prompts/TECH6A3F_FINE_FOOD_PM_ICON_VANILLA_RESTYLE_PROMPT.md`.

### Intégration des icônes finales

Les trois nouvelles versions violettes fournies par l’utilisateur ont été intégrées après inspection à la taille réelle. Le violet reprend le langage visuel des PM de luxe tout en conservant une silhouette proche des icônes vanilla :

- barrée : `pm_no_spiced_food` ;
- sans étoiles : `pm_spiced_food_preparations` ;
- avec deux étoiles : `pm_refined_spiced_food_preparations`.

Chaque source RGBA 1254 × 1254 a été réduite avec filtrage haute qualité à la taille vanilla de **104 × 104**, puis convertie en DDS RGBA. Les trois DDS conservent leur transparence alpha et correspondent pixel pour pixel aux aperçus PNG 104 × 104 validés.

```text
FINE_FOOD_PM_FINAL_ICON_STYLE = PURPLE_LUXURY
FINE_FOOD_PM_FINAL_ICON_SIZE = 104x104
FINE_FOOD_PM_FINAL_ICON_COUNT = 3
FINE_FOOD_PM_FINAL_ICONS_DDS_VALID = YES
FINE_FOOD_PM_FINAL_ICONS_ALPHA = YES
PM_GAMEPLAY_VALUES_CHANGED = NO
ICON_RUNTIME_RETEST = USER_REQUIRED
```

### Harmonisation des icônes de distillerie

Pour distinguer immédiatement la chaîne alcool de la nouvelle chaîne violette des mets raffinés, les trois icônes vanilla du groupe `pmg_distillery` ont été recolorées dans une palette neutre blanc, ivoire, argent et gris, avec contours anthracite :

- `pm_disabled_distillery` → `gfx/interface/icons/production_method_icons/no_distillery.dds` ;
- `pm_pot_stills` → `gfx/interface/icons/production_method_icons/pot_stills.dds` ;
- `pm_patent_stills` → `gfx/interface/icons/production_method_icons/patent_stills.dds`.

La troisième icône paraissait déjà grise dans la capture parce que la méthode était verrouillée ; son fichier source était néanmoins violet. Les trois fichiers ont donc été harmonisés. Chaque DDS est en RGBA **104 × 104** avec transparence alpha. Aucun coût, output, emploi, groupe de PM ou déblocage technologique n'a été modifié.

```text
DISTILLERY_PM_ICON_STYLE = IVORY_SILVER_GRAYSCALE
DISTILLERY_PM_ICON_SIZE = 104x104
DISTILLERY_PM_ICON_COUNT = 3
DISTILLERY_PM_ICONS_DDS_VALID = YES
DISTILLERY_PM_ICONS_ALPHA = YES
DISTILLERY_GAMEPLAY_VALUES_CHANGED = NO
DISTILLERY_ICON_RUNTIME_RETEST = USER_REQUIRED
```
