# TECH6A-3P — Spices Prestige Good & Company Integration

Date : 2026-08-28

Runtime : non exécuté, contrôle utilisateur requis

Commit / push : non effectués

## Résultat

Le prestige good exclusif de la VOC `prestige_good_fine_batavian_spices` est défini et relié au bien `spices`. La plantation d’épices est intégrée aux cinq compagnies de la whitelist TECH6A-3P, et les huit niveaux initiaux de Java sont possédés par `company_dutch_east_india_company` pour `c:NET`.

Aucun événement, monthly pulse, scripted effect ou système parallèle n’a été créé. Le nouveau bien suit le mécanisme vanilla normal des prestige goods de compagnie.

## Inspection vanilla 1.13.9

Les références directes suivantes ont été inspectées dans `C:\Games\Victoria 3\game` :

- prestige goods : `prestige_good_java_coffee`, `prestige_good_bengal_opium`, `prestige_good_generic_coffee`, `prestige_good_generic_opium` ;
- compagnies : `company_east_india_company`, `company_guthrie`, `company_nhm`, `company_basic_colonial_plantations_2` ;
- ownership de compagnies dans les historiques de bâtiments d’Inde et d’Indonésie ;
- création de la VOC et de l’East India Company dans les historiques de pays.

La syntaxe retenue reproduit les objets agricoles vanilla : `possible`, `base_good`, `prestige_bonus` et `texture`. L’ownership reprend exactement le bloc vanilla `company = { type, country, levels }`.

## Prestige good VOC

Fichier : `common/prestige_goods/10_tech6a3_spices.txt`

```text
ID = prestige_good_fine_batavian_spices
base_good = spices
possible = has_dlc_feature mp1_content
prestige_bonus = 0.1
texture = gfx/interface/icons/goods_icons/prestige_goods/generic_spices_prestige.dds
```

Le bonus `0.1` et le gate `mp1_content` sont repris sans changement de `prestige_good_java_coffee`, `prestige_good_bengal_opium` et des variantes génériques comparables.

Localisations :

- EN : **Fine Batavian Spices** ;
- FR : **Fines épices de Batavia**.

Le DDS existant est réutilisé et son en-tête a été validé. Aucun nouvel asset n’a été créé.

## Compagnies intégrées

| Compagnie | Intégration de `building_spice_plantation` | Prestige good VOC | Logique de formation | Cible IA ajoutée |
|---|---|---|---|---|
| `company_dutch_east_india_company` | Core | Oui, exclusif ; Java Coffee retiré | Épices ajoutées à la liste compatible existante, sans réduire les seuils | Indonésie, Inde du Nord et Inde du Sud |
| `company_east_india_company` | Core | Non ; Bengal Opium conservé | Épices ajoutées à la liste compatible en Inde | Inde du Sud |
| `company_nhm` | Core | Non ; Java Coffee conservé | Épices ajoutées à la liste compatible de Java occidental | Java occidental |
| `company_guthrie` | Extension | Non | Fondation maintenue sur café/thé pour ne pas permettre une création uniquement par les épices | Malaya |
| `company_basic_colonial_plantations_2` | Core | Non ; Reserve Coffee conservé | Épices ajoutées aux listes `possible` et `ai_will_do` | Pas de bloc `ai_construction_targets` vanilla à étendre |

Toutes les industries et tous les prestige goods précédents sont conservés. `company_basic_colonial_plantations_1` et toutes les compagnies hors whitelist sont inchangées.

## Fichiers vanilla shadowés

Les trois fichiers suivants reproduisent l’intégralité du fichier vanilla 1.13.9 au même chemin relatif. La comparaison objet par objet confirme que seuls les quatre IDs autorisés diffèrent :

- `common/company_types/00_companies_asia.txt` : seulement `company_east_india_company` ;
- `common/company_types/00_companies_ep2.txt` : seulement `company_guthrie` et `company_nhm` ;
- `common/company_types/99_basic_companies.txt` : seulement `company_basic_colonial_plantations_2`.

La VOC, qui est un objet propre au mod, reste modifiée dans `common/company_types/02_new_companies.txt`.

## Ownership initial de Java

Les niveaux ont été contrôlés avant modification : 4 / 2 / 2, conformément à la spécification. Seul le type de propriétaire a changé.

| État | Avant | Après | Niveaux |
|---|---|---|---:|
| `STATE_WEST_JAVA` | Manor House, `c:DEI` | VOC, `c:NET` | 4 |
| `STATE_CENTRAL_JAVA` | Manor House, `c:DEI` | VOC, `c:NET` | 2 |
| `STATE_EAST_JAVA` | Manor House, `c:DEI` | VOC, `c:NET` | 2 |
| **Total** |  | **VOC** | **8** |

Les dix-sept autres producteurs ou régions potentielles ne reçoivent aucun changement d’ownership dans cette phase. Le total mondial initial reste 87 niveaux dans 18 régions.

## Protection du gameplay

TECH6A-3P n’a modifié aucun chiffre ou objet de balance concernant :

- `spices` ;
- `building_spice_plantation` ;
- les PM de plantation et Food Industries ;
- le besoin POP ;
- la carte des ressources ;
- les niveaux initiaux ;
- le sel et la Gabelle ;
- les technologies initiales.

## QA statique

```text
PRESTIGE_GOOD_FINE_BATAVIAN_SPICES_DEFINED = YES
PRESTIGE_GOOD_BASE_GOOD = spices
PRESTIGE_GOOD_ICON_VALID = YES
VOC_SPICE_CORE_BUILDING = YES
VOC_SPICE_PRESTIGE_AVAILABLE = YES
VOC_JAVA_COFFEE = NO
NHM_JAVA_COFFEE = YES
WEST_JAVA_SPICE_LEVELS = 4
CENTRAL_JAVA_SPICE_LEVELS = 2
EAST_JAVA_SPICE_LEVELS = 2
JAVA_SPICE_LEVELS_TOTAL = 8
VOC_OWNED_JAVA_SPICE_LEVELS = 8
EIC_SPICE_BUILDING = YES
NHM_SPICE_BUILDING = YES
GUTHRIE_SPICE_EXTENSION = YES
GENERIC_COLONIAL_PLANTATIONS_2_SPICE_BUILDING = YES
BASIC_COLONIAL_PLANTATIONS_1_CHANGED = NO
SPICE_RESOURCE_MAP_CHANGED = NO
SPICE_STARTING_LEVEL_TOTAL_CHANGED = NO
SPICE_PM_BALANCE_CHANGED = NO
SPICE_POP_NEED_CHANGED = NO
FOOD_INDUSTRY_BALANCE_CHANGED = NO
SALT_FILES_TOUCHED = 0
GABELLE_FILES_TOUCHED = 0
STARTING_TECH_FILES_TOUCHED = 0
INVALID_COMPANY_REFS = 0
INVALID_PRESTIGE_GOOD_REFS = 0
INVALID_BUILDING_REFS = 0
INVALID_OWNERSHIP_REFS = 0
DUPLICATE_COMPANY_IDS = 0
DUPLICATE_PRESTIGE_GOOD_IDS = 0
```

## TECH6A-3F — FINAL POLISH / FINE FOOD

Le prestige spices a été renommé en `prestige_good_fine_batavian_spices` sans changer son `base_good = spices`, son bonus 0.1, son gate DLC ou son asset. La VOC ne possède désormais qu’un prestige good possible, **Fines épices de Batavia** ; `prestige_good_java_coffee` reste exclusivement préservé dans la NHM parmi ces deux compagnies néerlandaises.

La whitelist des compagnies est figée et inchangée : VOC, East India Company, NHM, Guthrie et `company_basic_colonial_plantations_2`. Les niveaux et owners de Java restent exactement 4/2/2, soit 8/8 possédés par la VOC.

Le nouveau bien manufacturé `fine_food` et sa conversion par les Food Industries sont documentés dans le rapport TECH6A-3 principal. L’audit des technologies Society conclut `KEEP_CURRENT_GATE` : aucun candidat Society existant n’est assez directement lié à l’alimentation pour remplacer proprement `distillation` et `baking_powder`.

Les variantes prestige restent substituables comme inputs via leurs `base_good` et le define moteur inchangé `PRESTIGE_GOODS_INPUT_THROUGHPUT_BONUS = 0.2`.

```text
LA_GABELLE_PERMISSION = GRANTED
PERMISSION_DATE = 2026-08-28
ORIGINAL_AUTHOR = Tokugawa_Mori
LA_GABELLE_GIT_EXCLUDES_REMOVED = YES
LA_GABELLE_ATTRIBUTION_ADDED = YES
SPICES_GLOBAL_BALANCE = DEFERRED_UNTIL_NAVAL_CONVOY_SETUP_FIXED
```

Assets intégrés : icône `fine_food`, icônes des trois options du PMG Food Industries, dont l’icône barrée fournie pour « Aucune préparation raffinée », et version finalisée de `building_spice_plantation`. L’asset prestige `epice de lux.dds` était déjà installé à l’identique et a été conservé.

La QA statique finale confirme : anciennes références du prestige spices = 0, références goods/PM/prestige invalides = 0, localisations manquantes = 0, textures manquantes = 0. Le runtime TECH6A-3P déjà fourni par l’utilisateur reste validé ; seul le nouveau contenu TECH6A-3F demande un contrôle en jeu.

## Checklist runtime utilisateur

1. Redémarrer complètement Victoria 3 et lancer une nouvelle partie en 1776.
2. Vérifier que la VOC apparaît et fonctionne normalement.
3. Vérifier que `building_spice_plantation` figure parmi les industries principales de la VOC, sans disparition du thé, du tabac ou du café.
4. Vérifier que les 4 niveaux de Java occidental, les 2 de Java central et les 2 de Java oriental appartiennent à la VOC de `c:NET`.
5. Vérifier que la VOC peut construire de nouvelles plantations d’épices dans les régions TECH6A-3 éligibles.
6. Vérifier que l’East India Company accepte les plantations d’épices comme industrie principale.
7. Vérifier que la NHM accepte les plantations d’épices comme industrie principale.
8. Vérifier que Guthrie accepte les plantations d’épices uniquement comme extension.
9. Vérifier que `company_basic_colonial_plantations_2` accepte les plantations d’épices comme industrie principale.
10. Faire prospérer la VOC et vérifier l’apparition de **Fines épices de Batavia** via le mécanisme normal des prestige goods.
11. Vérifier l’icône `generic_spices_prestige.dds` dans l’interface du prestige good.
12. Vérifier que **Java Coffee** n’est plus disponible pour la VOC mais reste disponible pour la NHM.
13. Vérifier qu’aucune autre compagnie ne propose le prestige good VOC.
14. Vérifier que la carte, les niveaux initiaux, les outputs 20/45 des plantations et la consommation POP directe des épices restent identiques au runtime validé.
15. Contrôler `error.log` pour les IDs company, prestige good, building et ownership.

## Sortie finale

```text
TECH6A3F_FINAL_POLISH = PASS
LA_GABELLE_PERMISSION = GRANTED
LA_GABELLE_GIT_EXCLUDES_REMOVED = YES
LA_GABELLE_ATTRIBUTION_ADDED = YES
FINE_FOOD_IMPLEMENTED = YES
FINE_FOOD_BASE_PRICE = 50
FINE_FOOD_BASIC_FOOD = YES
FINE_FOOD_LUXURY_FOOD = YES
SPICED_FOOD_PM_UPDATED = YES
REFINED_SPICED_FOOD_PM_UPDATED = YES
PRESTIGE_SPICE_ID = prestige_good_fine_batavian_spices
VOC_PRESTIGE_GOODS_COUNT = 1
VOC_JAVA_COFFEE = NO
NHM_JAVA_COFFEE = YES
SOCIETY_GATE_AUDIT = KEEP_CURRENT_GATE
SOCIETY_GATE_SELECTED = NONE
VOC_JAVA_SPICE_OWNERSHIP = 8/8
PRESTIGE_INPUT_THROUGHPUT_BONUS = 0.20
SPICES_DIRECT_POP_CONSUMPTION = PRESERVED
SPICES_GLOBAL_BALANCE = DEFERRED_UNTIL_NAVAL_CONVOYS
INVALID_REFERENCES = 0
MISSING_LOCALIZATION = 0
MISSING_TEXTURES = 0
COMMIT = NO
PUSH = NO
```
