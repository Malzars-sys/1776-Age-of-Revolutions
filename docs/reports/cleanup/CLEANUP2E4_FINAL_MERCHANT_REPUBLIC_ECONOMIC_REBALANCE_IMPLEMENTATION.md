# CLEANUP-2E-4 — Final Merchant Republic Economic Rebalance — Implementation

## Statut

- Branche : `cleanup-post-release`
- Baseline vanilla exclusive : installation locale `C:\Games\Victoria 3`
- Version vérifiée : `1.13.9` (`release/1.13.9`)
- Validation statique : `PASS`
- Runtime : `RUNTIME_PENDING_USER_SESSION`
- Victoria 3 non lancé
- Index Git vide ; aucun stage, commit ou push

## Sources de décision et résultat

Les rapports CLEANUP-2E-1, 2E-2 et 2E-3 ainsi que les quatre matrices économiques 2E-3 ont été lus intégralement avant l'implémentation. La direction retenue reste : « Own the trade, finance the powers, build the ships », avec une république marchande forte en commerce, crédit et construction navale, mais moins efficace pour exploiter directement de vastes territoires non incorporés.

Le socle CLEANUP-2E-2 de neuf modificateurs est conservé sans altération. Les trois anciens bonus de dividendes/nationalisation restent absents. Trois effets confirmés dans la vanilla locale 1.13.9 sont ajoutés à `law_merchant_banking` :

```text
building_group_bg_mining_unincorporated_throughput_add = -0.10
building_group_bg_plantations_unincorporated_throughput_add = -0.10
country_ship_construction_goods_cost_mult = -0.10
```

Le bonus naval est décrit uniquement comme une réduction du coût en biens couverte par cette clé. Son application aux refits n'est pas revendiquée sans preuve runtime.

Aucune clé vanilla exacte n'a été trouvée pour les fermes non incorporées. Aucune clé, aucun type de modificateur, aucun pulse et aucun `on_action` n'ont été inventés :

```text
MERCHANT_BANKING_FARMS_UNINCORPORATED = DEFERRED
FARM_UNINCORPORATED_IMPLEMENTATION = DEFERRED_POST_RELEASE
```

## Suppression de l'ancien Centre of Commerce

La recherche globale a confirmé que `modifier_centre_of_commerce_mod` n'avait comme consommateurs actifs que VEN et GEN. Ses deux applications ont été retirées, puis sa définition et ses localisations devenues mortes ont été supprimées.

L'ancien ensemble national gratuit n'est donc plus actif :

- `building_trade_center_throughput_add = 0.50` supprimé ;
- `state_export_advantage_mult = 0.20` supprimé ;
- `country_minting_add = 10000` supprimé sans compensation automatique.

La baseline runtime antérieure était d'environ `+£10.6K/semaine` pour VEN et `+£10.7K/semaine` pour GEN, valeurs comprenant le minting artificiel. Les nouveaux budgets structurels doivent être mesurés sur une partie 1776 fraîche.

## Bâtiments initiaux

| Pays / État | Élément | Avant statique | Après | Décision |
|---|---:|---:|---:|---|
| VEN / Venetia | Trade Center | 6 | 8 | capitale uniquement |
| VEN / Istria | Trade Center | 3 | 3 | inchangé |
| VEN total | Trade Center | 9 | 11 | attendu runtime |
| GEN / Piedmont | Trade Center | 3 | 6 | capitale uniquement |
| VEN / Venetia | Government Administration | 3 | 5 | correction de départ |
| GEN / Piedmont | Government Administration | 1 | 1 | inchangé |

La capture vénitienne montrait `4 + 1 en construction`, mais l'audit du history file a trouvé un seed statique de `3`. Le quatrième niveau et la file de construction provenaient de la construction lancée par l'utilisateur. Après cette clarification, le passage statique correct est donc `3 → 5`, et non `4 → 5`. Il n'existe qu'un seul bloc `building_trade_center` par capitale et aucune duplication d'ownership.

Aucune manufacture d'armes n'a été ajoutée à Gênes.

## Monuments institutionnels

Deux bâtiments uniques, présents au départ et non constructibles normalement, suivent le pattern data/UI vanilla `bg_monuments` :

- `Rialto Commercial Complex` / `Complexe commercial du Rialto`, dans `STATE_VENETIA` ;
- `Palazzo San Giorgio` / `Palais San Giorgio`, dans `STATE_PIEDMONT`.

Le Rialto représente le quartier et l'écosystème commercial — marchés, négociants, crédit, banques, assurances, notaires, justice et information commerciale — plutôt qu'un palais fictif. San Giorgio représente la Casa di San Giorgio, sa gestion de la dette et de la fiscalité, ses dépôts, son crédit et ses créanciers, sans être présenté comme une banque centrale moderne.

Chaque monument fournit uniquement dans son État, par un `state_modifiers / level_scaled` :

```text
building_trade_center_throughput_add = 0.10
state_export_advantage_mult = 0.10
```

Ils sont intégrés aux trois modes de la règle `monument_effects` : effets activés, prestige seul et aucun effet. Les modes prestige/no effects reprennent tous les flags vanilla 1.13.9 et ajoutent les deux flags de désactivation nécessaires.

### Assets et dette 3D autorisée

Les deux peintures fournies par l'utilisateur ont été préparées avec le workflow image intégré, cadrées en carré sans texte ni bordure, puis converties en icônes DDS `256 × 256` : la façade de San Giorgio pour le monument génois et la scène commerciale du Rialto pour le monument vénitien. Le fond de panneau monument vanilla reste réutilisé. L'existence, le format DDS et les dimensions des deux icônes dédiées sont contrôlés par le validateur.

Aucun asset 3D n'est inventé et aucun `locator`, `entity`, `mesh` ou fichier de carte n'est référencé. Sur instruction de l'utilisateur, les modèles et locators dédiés des deux monuments sont classés dans la même phase extérieure que les personnages :

```text
MONUMENT_3D_ASSETS = DEFERRED_POST_MAP_3D_CHARACTER_ART_PHASE
```

Cette livraison continue donc avec des monuments data/UI fonctionnels sans modèle 3D dédié. La session runtime doit néanmoins contrôler `error.log` pour confirmer que le moteur n'exige pas de locator implicite dans ce contexte.

## Fichiers modifiés par CLEANUP-2E-4

1. `common/laws/00_inject_laws.txt`
2. `common/static_modifiers/76mod_modifiers.txt`
3. `common/history/countries/gen - genoa.txt`
4. `common/history/countries/ven - venetia.txt`
5. `common/history/buildings/01_south_europe.txt`
6. `common/buildings/99_cleanup2e4_merchant_republic_monuments.txt`
7. `common/production_method_groups/99_cleanup2e4_merchant_republic_monuments.txt`
8. `common/production_methods/99_cleanup2e4_merchant_republic_monuments.txt`
9. `common/game_rules/99_cleanup2e4_monument_effects.txt`
10. `localization/english/76mod_modifiers_l_english.yml`
11. `localization/french/76mod_modifiers_l_french.yml`
12. `localization/english/hotfix_laws_l_english.yml`
13. `localization/french/hotfix_laws_l_french.yml`
14. `localization/english/cleanup2e4_monuments_l_english.yml`
15. `localization/french/cleanup2e4_monuments_l_french.yml`
16. `gfx/interface/icons/building_icons/cleanup2e4/building_rialto_commercial_complex.dds`
17. `gfx/interface/icons/building_icons/cleanup2e4/building_palazzo_san_giorgio.dds`
18. `tools/cleanup2e2_validate.py` — rendu conscient de l'extension successeur 2E-4
19. `tools/cleanup2e4_validate.py`
20. `docs/reports/cleanup/CLEANUP2E4_FINAL_MERCHANT_REPUBLIC_ECONOMIC_REBALANCE_IMPLEMENTATION.md`

Les autres modifications et fichiers non suivis déjà présents dans le worktree ont été préservés.

## Invariants

```text
LAND_FORMATIONS = 214
GENERAL_COMMAND_CAPACITY_SUFFICIENT = 214
FLEETS = 41
NAVAL_UNITS = 370
FINAL_FIXED_HISTORICAL_ADMIRALS = 26
MILITARY_FILES_CHANGED = 0
LAND_GENERAL_RANKS_CHANGED = 0
TECHNOLOGY_FILES_CHANGED = 0
PROTECTED_TECH_FILES_CHANGED = 0
PROTECTED_TECH_FILES_STAGED = 0
MAP_FILES_CHANGED = 0
STAGED_FILES = 0
```

## Sortie complète — `python tools/cleanup2e2_validate.py`

```text
VANILLA_VERSION = 1.13.9
VANILLA_POPULATION_BUREAUCRACY_MODIFIER_EXISTS = 1
VANILLA_POPULATION_BUREAUCRACY_SCOPE = INCORPORATED_POPULATION_BASE_ADMINISTRATIVE_COST
VANILLA_POSITIVE_POPULATION_BUREAUCRACY_INCREASES_COST = 1
VANILLA_INCORPORATION_SPEED_MODIFIER_EXISTS = 1
VANILLA_INCORPORATION_SPEED_SCOPE = ALL_STATE_INCORPORATION_SPEED
VANILLA_NEGATIVE_INCORPORATION_SPEED_SLOWS = 1
HEREDITARY_BUREAUCRATS_POPULATION_BUREAUCRACY_COST = -0.25
MERCHANT_BANKING_MARGINAL_POPULATION_BUREAUCRACY_COST = +0.10
VEN_GEN_COMBINED_STARTING_POPULATION_BUREAUCRACY_COST = -0.15

MERCHANT_BANKING_ARISTOCRATS = 0.40
MERCHANT_BANKING_SHOPKEEPERS = 0.50
MERCHANT_BANKING_TRADE_ADVANTAGE = 0.10
MERCHANT_BANKING_CAPITALISTS = -0.20
MERCHANT_BANKING_PRIVATE_CONSTRUCTION = 0.40
MERCHANT_BANKING_FREE_CHARTERS = 1
MERCHANT_BANKING_NO_UNCOMPENSATED_NATIONALIZATION = yes
MERCHANT_BANKING_POPULATION_BUREAUCRACY_COST = 0.10
MERCHANT_BANKING_INCORPORATION_SPEED = -0.15
CLEANUP2E4_EXTENSION_BUILDING_GROUP_BG_MINING_UNINCORPORATED_THROUGHPUT_ADD = -0.10
CLEANUP2E4_EXTENSION_BUILDING_GROUP_BG_PLANTATIONS_UNINCORPORATED_THROUGHPUT_ADD = -0.10
CLEANUP2E4_EXTENSION_COUNTRY_SHIP_CONSTRUCTION_GOODS_COST_MULT = -0.10
MERCHANT_BANKING_NATIONALIZATION_RETURN_PRESENT = 0
MERCHANT_BANKING_GOV_DIVIDEND_REINVESTMENT_PRESENT = 0
MERCHANT_BANKING_GOV_DIVIDEND_EFFICIENCY_PRESENT = 0
MERCHANT_BANKING_MODIFIER_COUNT = 9
MERCHANT_BANKING_POST_2E2_EXTENSION_COUNT = 3
MERCHANT_BANKING_UNEXPECTED_MODIFIER_COUNT = 0
MERCHANT_BANKING_REMOVED_PUBLIC_ECONOMY_BONUSES = 3
MERCHANT_BANKING_TERRITORIAL_CONSTRAINTS = 2

MERCHANT_BANKING_NON_ECONOMIC_LOGIC_UNCHANGED = 1
OTHER_LAWS_UNCHANGED = 1
VEN_STARTS_WITH_MERCHANT_BANKING = 1
GEN_STARTS_WITH_MERCHANT_BANKING = 1
MERCHANT_BANKING_LOCALIZATION_EN = PASS
MERCHANT_BANKING_LOCALIZATION_FR = PASS

LAND_FORMATIONS = 214
GENERAL_COMMAND_CAPACITY_SUFFICIENT = 214
FLEETS = 41
NAVAL_UNITS = 370
FINAL_FIXED_HISTORICAL_ADMIRALS = 26
MILITARY_FILES_CHANGED = 0
TECHNOLOGY_FILES_CHANGED = 0
PROTECTED_TECH_FILES_CHANGED = 0
PROTECTED_TECH_FILES_STAGED = 0
STAGED_FILES = 0
UNEXPECTED_GAMEPLAY_FILES_CHANGED = 0

CENTRE_OF_COMMERCE_BALANCE = RESOLVED_BY_CLEANUP2E4
MERCHANT_BANKING_AI_REWORK = DEFERRED
RUNTIME = RUNTIME_PENDING_USER_SESSION
STATIC_VALIDATION_2E2 = PASS
STATIC_VALIDATION = PASS
```

## Sortie complète — `python tools/cleanup2e4_validate.py`

```text
VANILLA_VERSION = 1.13.9
VANILLA_BRANCH = release/1.13.9
VANILLA_KEY_BUILDING_GROUP_BG_MINING_UNINCORPORATED_THROUGHPUT_ADD = 1
MERCHANT_BANKING_MINING_UNINCORPORATED = -0.10
VANILLA_KEY_BUILDING_GROUP_BG_PLANTATIONS_UNINCORPORATED_THROUGHPUT_ADD = 1
MERCHANT_BANKING_PLANTATIONS_UNINCORPORATED = -0.10
VANILLA_KEY_COUNTRY_SHIP_CONSTRUCTION_GOODS_COST_MULT = 1
MERCHANT_BANKING_SHIP_CONSTRUCTION_GOODS_COST = -0.10
MERCHANT_BANKING_FARMS_UNINCORPORATED = DEFERRED
FARM_UNINCORPORATED_IMPLEMENTATION = DEFERRED_POST_RELEASE
VANILLA_FARM_UNINCORPORATED_KEY_FOUND = 0
GEN_ARMS_INDUSTRY_ADDED = 0

OLD_CENTRE_OF_COMMERCE_DEFINITION = 0
OLD_CENTRE_OF_COMMERCE_VEN_APPLIED = 0
OLD_CENTRE_OF_COMMERCE_GEN_APPLIED = 0
OLD_FREE_MINTING_10000_ACTIVE_FOR_VEN = 0
OLD_FREE_MINTING_10000_ACTIVE_FOR_GEN = 0
VEN_CAPITAL_TRADE_CENTER = 8
GEN_CAPITAL_TRADE_CENTER = 6
VEN_ISTRIA_TRADE_CENTER = 3
VEN_GOV_ADMIN = 5
GEN_GOV_ADMIN_UNCHANGED = 1
VEN_CAPITAL_TRADE_CENTER_INSTANCES = 1
GEN_CAPITAL_TRADE_CENTER_INSTANCES = 1
RIALTO_INSTANCES = 1
SAN_GIORGIO_INSTANCES = 1
RIALTO_STARTING_LEVEL = 1
PALAZZO_SAN_GIORGIO_STARTING_LEVEL = 1

RIALTO_MONUMENT_DEFINED = 1
RIALTO_BUILDING_GROUP = bg_monuments
RIALTO_UNIQUE = yes
RIALTO_BUILDABLE = no
RIALTO_STATE_POTENTIAL = s:STATE_VENETIA
RIALTO_PMG_DEFINED = 1
RIALTO_PMG_GAME_RULE_ALTERNATIVES = 1
RIALTO_LOCAL_TRADE_CENTER_THROUGHPUT = 0.10
RIALTO_LOCAL_EXPORT_ADVANTAGE = 0.10
RIALTO_ICON_EXISTS = 1
RIALTO_ICON_DIMENSIONS = 256x256
RIALTO_BACKGROUND_EXISTS = 1
PALAZZO_SAN_GIORGIO_DEFINED = 1
SAN_GIORGIO_BUILDING_GROUP = bg_monuments
SAN_GIORGIO_UNIQUE = yes
SAN_GIORGIO_BUILDABLE = no
SAN_GIORGIO_STATE_POTENTIAL = s:STATE_PIEDMONT
SAN_GIORGIO_PMG_DEFINED = 1
SAN_GIORGIO_PMG_GAME_RULE_ALTERNATIVES = 1
SAN_GIORGIO_LOCAL_TRADE_CENTER_THROUGHPUT = 0.10
SAN_GIORGIO_LOCAL_EXPORT_ADVANTAGE = 0.10
SAN_GIORGIO_ICON_EXISTS = 1
SAN_GIORGIO_ICON_DIMENSIONS = 256x256
SAN_GIORGIO_BACKGROUND_EXISTS = 1
MONUMENT_LOCATOR_REFERENCES = 0
MONUMENT_ENTITY_REFERENCES = 0
MONUMENT_MESH_REFERENCES = 0
MONUMENT_MAP_DATA_REFERENCES = 0
MONUMENT_3D_ASSETS = DEFERRED_POST_MAP_3D_CHARACTER_ART_PHASE

MONUMENT_EFFECTS_GAME_RULE_SUPPORTED = 1
MONUMENT_LOCALIZATION_ENGLISH_MISSING = 0
MONUMENT_LOCALIZATION_FRENCH_MISSING = 0

LAND_FORMATIONS = 214
GENERAL_COMMAND_CAPACITY_SUFFICIENT = 214
FLEETS = 41
NAVAL_UNITS = 370
FINAL_FIXED_HISTORICAL_ADMIRALS = 26
MILITARY_FILES_CHANGED = 0
LAND_GENERAL_RANKS_CHANGED = 0
TECHNOLOGY_FILES_CHANGED = 0
PROTECTED_TECH_FILES_CHANGED = 0
PROTECTED_TECH_FILES_STAGED = 0
STAGED_FILES = 0
UNEXPECTED_GAMEPLAY_FILES_CHANGED = 0
MAP_FILES_CHANGED = 0

RUNTIME = RUNTIME_PENDING_USER_SESSION
STATIC_VALIDATION_2E4 = PASS
STATIC_VALIDATION = PASS
```

Les appels Git internes aux validateurs émettent uniquement les avertissements Windows habituels `LF will be replaced by CRLF`; `git diff --check` reste sans erreur.

## Checklist runtime consolidée — une seule nouvelle partie 1776

### VEN

1. Confirmer Merchant Banking actif et les effets `-10 %` mines/plantations non incorporées et coût en biens de construction navale.
2. Confirmer l'absence de malus farms revendiqué et de minting gratuit `+£10K`.
3. Vérifier Venetia Trade Center `8`, Istria `3`, total VEN `11`.
4. Vérifier Government Administration Venetia `5` et noter la bureaucratie initiale ; elle ne doit plus présenter le déficit structurel observé d'environ `-39.4`.
5. Vérifier le Rialto, ses deux effets locaux de `+10 %`, et noter le budget structurel hors dépenses temporaires.

### GEN

1. Confirmer Merchant Banking actif, Piedmont Trade Center `6` et Government Administration `1`.
2. Vérifier San Giorgio et ses deux effets locaux de `+10 %`.
3. Confirmer l'absence de minting gratuit, une bureaucratie positive et noter le budget structurel hors dépenses temporaires.

### Tests communs

1. Lancer une construction navale minimale et vérifier la baisse de `10 %` du coût matériel ; ne pas conclure sur les refits sans observation.
2. Si une situation simple existe, observer une mine et une plantation dans un État non incorporé ; sinon noter `NOT_TESTED`.
3. Sauvegarder puis recharger dans la même session. Recontrôler Rialto, San Giorgio, Merchant Banking, Venetia TC `8`, administration `5` et Piedmont TC `6`.
4. Examiner `error.log` : `invalid modifier`, `invalid building`, `invalid production method`, `invalid production method group`, `invalid game rule`, `missing localization`, `missing entity`, `missing locator`, `building history`, `create_building`, `monument`, `PostValidate`.
5. Toute erreur liée aux monuments est un échec runtime, y compris une exigence implicite de locator malgré l'absence volontaire de modèle 3D.

## Évaluation runtime à renseigner

```text
VEN_BUDGET_STRUCTURAL = ?
GEN_BUDGET_STRUCTURAL = ?
VEN_BUREAUCRACY = ?
GEN_BUREAUCRACY = ?
VEN_TRADE_CENTER = 8
GEN_TRADE_CENTER = 6
RIALTO_RUNTIME = PASS/FAIL
SAN_GIORGIO_RUNTIME = PASS/FAIL
SHIP_CONSTRUCTION_COST_RUNTIME = PASS/FAIL
UNINCORPORATED_MINING_RUNTIME = PASS/NOT_TESTED
UNINCORPORATED_PLANTATIONS_RUNTIME = PASS/NOT_TESTED
CENTRE_OF_COMMERCE_FREE_MODIFIER_REMOVED = PASS
SAVE_RELOAD = PASS/FAIL
RUNTIME = RUNTIME_PENDING_USER_SESSION
```
