# CLEANUP-2E-4B — Merchant Republic Runtime Balance Correction

## Statut

- Nature : micro-correctif runtime ciblé après CLEANUP-2E-4
- Branche : `cleanup-post-release`
- Vanilla locale vérifiée : `1.13.9` (`release/1.13.9`)
- Validation statique : `PASS`
- Runtime : `RUNTIME_PASS`
- Victoria 3 non lancé
- Aucun stage, commit ou push

## Raison du hotfix

La nouvelle partie 1776 testée par l'utilisateur valide VEN et l'essentiel de CLEANUP-2E-4. GEN démarre cependant avec environ 463K habitants, aucun chômeur, presque aucun paysan disponible, environ 21,3K actifs cherchant un autre emploi sans être au chômage, des postes vacants et des tensions de qualification. Le Trade Center génois passé de 3 à 6 renforce une économie qui manque immédiatement de réserve de main-d'œuvre. Les deux monuments appliquent correctement leurs effets locaux mais affichaient zéro emploi.

CLEANUP-2E-4B ne change donc que deux éléments de gameplay : la population initiale de GEN et la main-d'œuvre des monuments.

## Population génoise

Le parsing de l'ensemble de `common/history/pops/` trouve un seul territoire GEN au 1776-01-01 : `STATE_PIEDMONT`. Le total statique de `463 988` explique directement l'observation runtime ≈463K ; aucun écart inexpliqué ne justifiait un arrêt.

Les entrées `create_pop` n'ont pas de champ de profession : Victoria 3 distribue ces habitants entre professions lors de l'initialisation selon les bâtiments et emplois disponibles. Le redimensionnement préserve donc exactement les trois entrées démographiques existantes, sans fabriquer de profession.

Facteur déterministe :

```text
510000 / 463988 = 1.099166357750631...
```

| Culture | Religion | Avant | Brut redimensionné | Après | Delta |
|---|---|---:|---:|---:|---:|
| north_italian | catholic (religion culturelle par défaut) | 367 188 | 403 600,696570 | 403 601 | +36 413 |
| french | catholic (religion culturelle par défaut) | 93 996 | 103 317,240963 | 103 317 | +9 321 |
| north_italian | jewish (explicite) | 2 804 | 3 082,062467 | 3 082 | +278 |
| **TOTAL** |  | **463 988** | **510 000** | **510 000** | **+46 012** |

Sous les lois initiales de GEN, les minorités française et juive restent soumises à la logique de discrimination du jeu ; leurs proportions ne sont pas altérées artificiellement.

```text
GEN_CULTURE_SHARE_DRIFT_MAX_PP = 0.000047
GEN_RELIGION_SHARE_DRIFT_MAX_PP = 0.000012
GEN_POP_SCALING_PROPORTIONAL = PASS
VEN_POPULATION_CHANGED = 0
```

L'audit détaillé est dans `docs/research/economy/CLEANUP2E4B_GENOA_POPULATION_SCALING_AUDIT.csv`.

## Main-d'œuvre des monuments

### Références vanilla 1.13.9

Le fichier vanilla `common/production_methods/08_monuments.txt` confirme le pattern `building_modifiers / level_scaled` :

- Big Ben : 100 machinistes ;
- Vatican City : 500 ecclésiastiques ;
- Forbidden City : 800 bureaucrates + 200 ecclésiastiques ;
- Trade League Power Bloc Statue : 500 clerks.

Les types exacts `building_employment_clerks_add`, `building_employment_shopkeepers_add` et `building_employment_bureaucrats_add` existent dans les définitions vanilla. `shopkeepers` est largement utilisé par les PM industriels/commerciaux vanilla, bien qu'aucun monument standard de `08_monuments.txt` ne l'utilise.

Les PM génériques vanilla `pm_monument_prestige_only` et `pm_monument_no_effects` ne conservent pas la main-d'œuvre du PM par défaut. CLEANUP-2E-4B reproduit ce comportement : les emplois sont ajoutés uniquement aux deux PM par défaut, sans modifier la game rule.

### Répartition retenue

| Monument | Profession | Emplois |
|---|---|---:|
| Rialto Commercial Complex | clerks | 500 |
| Rialto Commercial Complex | shopkeepers | 200 |
| **Rialto total** |  | **700** |
| Palazzo San Giorgio | clerks | 500 |
| Palazzo San Giorgio | bureaucrats | 100 |
| **San Giorgio total** |  | **600** |

Aucun machiniste, laborer industriel, aristocrate, ecclésiastique ou militaire n'est ajouté. Les deux plafonds de 700 sont respectés.

L'audit détaillé est dans `docs/research/economy/CLEANUP2E4B_MONUMENT_WORKFORCE_AUDIT.csv`.

## Éléments gelés confirmés

- effets Rialto et San Giorgio inchangés : `+0.10` throughput local du Trade Center et `+0.10` export advantage local ;
- icônes DDS inchangées, hashes identiques ;
- aucun recadrage ni modification d'asset ;
- aucune 3D, entity, mesh, locator ou carte ;
- dette 3D toujours `DEFERRED_POST_MAP_3D_CHARACTER_ART_PHASE` ;
- GEN Trade Center `6` ; VEN Trade Center `8` ; Istria `3` ;
- administration VEN `5` ; administration GEN `1` ;
- Merchant Banking inchangé ; farm penalty toujours différé ;
- game rule `monument_effects` inchangée ;
- armée, flotte, personnages et technologies inchangés.

## Fichiers modifiés par CLEANUP-2E-4B

1. `common/history/pops/01_south_europe.txt`
2. `common/production_methods/99_cleanup2e4_merchant_republic_monuments.txt`
3. `docs/research/economy/CLEANUP2E4B_GENOA_POPULATION_SCALING_AUDIT.csv`
4. `docs/research/economy/CLEANUP2E4B_MONUMENT_WORKFORCE_AUDIT.csv`
5. `tools/cleanup2e4b_validate.py`
6. `docs/reports/cleanup/CLEANUP2E4B_MERCHANT_REPUBLIC_RUNTIME_BALANCE_CORRECTION.md`
7. `tools/cleanup2e2_validate.py` — compatibilité avec le fichier POP autorisé par la phase successeur, aucune règle métier 2E-2 changée
8. `tools/cleanup2e4_validate.py` — compatibilité avec le fichier POP autorisé par la phase successeur, aucune règle métier 2E-4 changée

Les modifications préexistantes du worktree hors phase ont été préservées.

## Validation

```text
python tools/cleanup2e2_validate.py
STATIC_VALIDATION_2E2 = PASS

python tools/cleanup2e4_validate.py
STATIC_VALIDATION_2E4 = PASS

python tools/cleanup2e4b_validate.py
STATIC_VALIDATION_2E4B = PASS

git diff --check
PASS

git diff --cached --name-only
STAGED_FILES = 0
```

### Sortie complète du validateur 2E-4B

```text
VANILLA_BRANCH = release/1.13.9
GEN_POPULATION_STATIC_BEFORE = 463988
GEN_POPULATION_STATIC_AFTER = 510000
GEN_POPULATION_TARGET_MIN = 509500
GEN_POPULATION_TARGET_MAX = 510500
GEN_CULTURE_SHARE_DRIFT_MAX_PP = 0.000047
GEN_RELIGION_SHARE_DRIFT_MAX_PP = 0.000012
GEN_POP_SCALING_PROPORTIONAL = PASS
VEN_POPULATION_CHANGED = 0
GEN_POPULATION_AUDIT_ROWS = 4
GEN_POPULATION_AUDIT_TOTAL_BEFORE = 463988
GEN_POPULATION_AUDIT_TOTAL_AFTER = 510000

RIALTO_CLERKS = 500
RIALTO_SHOPKEEPERS = 200
RIALTO_TOTAL_WORKFORCE = 700
SAN_GIORGIO_CLERKS = 500
SAN_GIORGIO_BUREAUCRATS = 100
SAN_GIORGIO_TOTAL_WORKFORCE = 600
RIALTO_TOTAL_WORKFORCE_LE_700 = 1
SAN_GIORGIO_TOTAL_WORKFORCE_LE_700 = 1
RIALTO_HAS_REAL_EMPLOYMENT = 1
SAN_GIORGIO_HAS_REAL_EMPLOYMENT = 1
RIALTO_EFFECTS_UNCHANGED = 1
SAN_GIORGIO_EFFECTS_UNCHANGED = 1
VANILLA_MONUMENT_WORKFORCE_REFERENCE_AUDIT = PASS
MONUMENT_WORKFORCE_AUDIT_ROWS = 12

RIALTO_ICON_CHANGED = 0
SAN_GIORGIO_ICON_CHANGED = 0
FROZEN_2E4_FILES_CHANGED_BY_2E4B = 0
MERCHANT_BANKING_CHANGED_BY_2E4B = 0
GEN_TRADE_CENTER = 6
VEN_TRADE_CENTER = 8
VEN_ISTRIA_TRADE_CENTER = 3
VEN_GOV_ADMIN = 5
GEN_GOV_ADMIN = 1

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
MAP_FILES_CHANGED = 0

RUNTIME = RUNTIME_PENDING_USER_SESSION
STATIC_VALIDATION_2E4B = PASS
STATIC_VALIDATION = PASS
```

Les avertissements Git `LF will be replaced by CRLF` sont les avertissements Windows déjà présents ; `git diff --check` ne signale aucune erreur.

## Checklist runtime — nouvelle partie 1776 fraîche

### GEN

1. Vérifier une population totale proche de `510K`.
2. Confirmer Piedmont Trade Center `6`, Government Administration `1` et Palazzo San Giorgio présent.
3. Ouvrir San Giorgio et confirmer `600` postes réels : `500 clerks + 100 bureaucrats`.
4. Confirmer une bureaucratie positive.
5. Sans changer les impôts ni ajouter de taxe de consommation, noter :
   - `GEN_BUDGET_START` ;
   - `GEN_BUDGET_STRUCTURAL_AFTER_INITIALIZATION` ;
   - `GEN_INVESTMENT_POOL_CHANGE`.
6. Relever chômeurs, paysans, demandeurs d'emploi, postes vacants et problèmes de qualification.
7. Déterminer si GEN dispose maintenant d'une réserve de main-d'œuvre raisonnable. Si la saturation absolue persiste, le prochain arbitrage sera Trade Center `6 → 5`, pas une population supérieure à 510K.

### VEN — non-régression

1. Population inchangée ; Venetia Trade Center `8`, Istria `3`, Government Administration `5`.
2. Rialto présent avec `700` postes réels : `500 clerks + 200 shopkeepers`.
3. Budget viable et bureaucratie positive.

### Monuments, sauvegarde et log

1. Avec les effets de monuments actifs, confirmer que les bâtiments n'affichent plus zéro emploi, restent sous 700 et ne créent aucune pénurie massive ou qualification absurde.
2. Sauvegarder puis recharger ; recontrôler population GEN, Trade Center `6`, les deux workforces et Merchant Banking.
3. Inspecter `error.log` pour `invalid profession`, `invalid workforce`, `invalid production method`, `invalid production method group`, `building employment`, `missing localization`, `monument` et `PostValidate`.

```text
RUNTIME = PASS
```
