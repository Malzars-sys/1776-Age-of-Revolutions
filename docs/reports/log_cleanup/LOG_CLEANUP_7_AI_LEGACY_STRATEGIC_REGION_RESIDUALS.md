# LOG-CLEANUP-7 — AI legacy strategic-region residuals

## État

`STATIC_AUDIT = PASS`

`RUNTIME = PASS`

Cette phase ferme statiquement la cause racine des 49 références `sr:` invalides restantes dans `common/ai_strategies/00_default_strategy.txt`. Le patch ne modifie que les sélecteurs géographiques : scores, valeurs numériques, conditions, journaux, commentaires et structures AI sont conservés.

## Prévol Git

- branche : `post-2.3.0-log-cleanup` ;
- HEAD : `21e5fdb28bb76c5b7519297cac76e2af91c6ad93` ;
- commit HEAD : `21e5fdb Migrate legacy AI strategy regions for Victoria 3 1.13` ;
- worktree initial : propre ;
- index initial : vide ;
- `KNOWN_FORK_ERRORS_OPERATIONAL_BEFORE = 15` ;
- fichier gameplay autorisé unique : `common/ai_strategies/00_default_strategy.txt`.

## Inventaire canonique

Le recomptage au HEAD confirme `STATIC_INVALID_SR_REFERENCES_BEFORE = 49` :

| Ancienne région | Occurrences | `sr:` valide en 1.13.9 |
|---|---:|---|
| `region_bombay` | 10 | NO |
| `region_punjab` | 9 | NO |
| `region_madras` | 8 | NO |
| `region_bengal` | 8 | NO |
| `region_central_india` | 8 | NO |
| `region_persia` | 6 | NO |

Les 49 décisions occurrence par occurrence figurent dans `LOG_CLEANUP_7_AI_RESIDUAL_MIGRATION_MATRIX.csv`. Elles couvrent 48 comparaisons dans un scope d'État et une comparaison de la région de la capitale d'un pays.

## Sources et gate sémantique

Sources vanilla 1.13.9 inspectées directement sous `C:\Games\Victoria 3\game` :

- `common/geographic_regions/06_old_strategic_regions.txt` définit les six empreintes `_old` ;
- `common/strategic_regions/west_south_asia_strategic_regions.txt` confirme la nouvelle géographie stratégique ;
- `common/ai_strategies/00_default_strategy.txt` emploie `is_in_geographic_region` sur les scopes d'État homologues ;
- `common/scripted_triggers/00_geography_triggers.txt`, `common/scripted_progress_bars/00_sepoy_mutiny_progress_bars.txt` et d'autres scripts 1.13.9 utilisent physiquement les mêmes objets `_old` ;
- les scripts vanilla utilisent aussi la forme `capital = { is_in_geographic_region = geographic_region_*_old }`, qui prouve la migration de la comparaison directe de capitale.

`AI_RESIDUAL_SR_MIGRATION_SAFE = YES`

La règle globale prouvée est :

```text
state scope:
region = sr:region_x
->
is_in_geographic_region = geographic_region_x_old

country scope through capital:
capital.region = sr:region_persia
->
capital = { is_in_geographic_region = geographic_region_persia_old }
```

Chaque remplacement conserve exactement la liste des state regions de l'ancien objet. Les condensations plus larges observées dans certains blocs vanilla (`geographic_region_india`, `geographic_region_indian_frontier`, `sr:region_greater_persia`) ne sont pas copiées lorsque leur empreinte diffère de celle du fork.

## Audit des six régions

### `region_bombay`

- `STATIC_OCCURRENCES = 10`
- `VALID_SR_IN_1_13_9 = NO`
- `OLD_GEOGRAPHIC_FOOTPRINT = STATE_BOMBAY, STATE_GUJARAT, STATE_SINDH, STATE_BALUCHISTAN`
- `MODERN_GEOGRAPHIC_OBJECT = geographic_region_bombay_old`
- `MODERN_STRATEGIC_REGION_IF_RELEVANT = split across region_south_india, region_north_india and region_greater_persia`
- `SEMANTIC_EQUIVALENCE = EXACT_LEGACY_STATE_REGION_FOOTPRINT`
- `MIGRATION_RULE = state.region comparison -> state is_in_geographic_region`

### `region_punjab`

- `STATIC_OCCURRENCES = 9`
- `VALID_SR_IN_1_13_9 = NO`
- `OLD_GEOGRAPHIC_FOOTPRINT = STATE_PUNJAB, STATE_HILL_PUNJAB, STATE_DELHI, STATE_RAJPUTANA`
- `MODERN_GEOGRAPHIC_OBJECT = geographic_region_punjab_old`
- `MODERN_STRATEGIC_REGION_IF_RELEVANT = subset of region_north_india`
- `SEMANTIC_EQUIVALENCE = EXACT_LEGACY_STATE_REGION_FOOTPRINT`
- `MIGRATION_RULE = state.region comparison -> state is_in_geographic_region`

### `region_madras`

- `STATIC_OCCURRENCES = 8`
- `VALID_SR_IN_1_13_9 = NO`
- `OLD_GEOGRAPHIC_FOOTPRINT = STATE_CEYLON, STATE_CIRCARS, STATE_MYSORE, STATE_TRAVANCORE, STATE_MADRAS, STATE_HYDERABAD, STATE_KURNOOL`
- `MODERN_GEOGRAPHIC_OBJECT = geographic_region_madras_old`
- `MODERN_STRATEGIC_REGION_IF_RELEVANT = subset of region_south_india`
- `SEMANTIC_EQUIVALENCE = EXACT_LEGACY_STATE_REGION_FOOTPRINT`
- `MIGRATION_RULE = state.region comparison -> state is_in_geographic_region`

### `region_bengal`

- `STATIC_OCCURRENCES = 8`
- `VALID_SR_IN_1_13_9 = NO`
- `OLD_GEOGRAPHIC_FOOTPRINT = STATE_BIHAR, STATE_EAST_BENGAL, STATE_WEST_BENGAL, STATE_ASSAM, STATE_ORISSA`
- `MODERN_GEOGRAPHIC_OBJECT = geographic_region_bengal_old`
- `MODERN_STRATEGIC_REGION_IF_RELEVANT = subset of region_north_india`
- `SEMANTIC_EQUIVALENCE = EXACT_LEGACY_STATE_REGION_FOOTPRINT`
- `MIGRATION_RULE = state.region comparison -> state is_in_geographic_region`

### `region_central_india`

- `STATIC_OCCURRENCES = 8`
- `VALID_SR_IN_1_13_9 = NO`
- `OLD_GEOGRAPHIC_FOOTPRINT = STATE_CENTRAL_PROVINCES, STATE_AWADH, STATE_MALWA, STATE_AGRA, STATE_BUNDELKHAND`
- `MODERN_GEOGRAPHIC_OBJECT = geographic_region_central_india_old`
- `MODERN_STRATEGIC_REGION_IF_RELEVANT = subset of region_north_india`
- `SEMANTIC_EQUIVALENCE = EXACT_LEGACY_STATE_REGION_FOOTPRINT`
- `MIGRATION_RULE = state.region comparison -> state is_in_geographic_region`

### `region_persia`

- `STATIC_OCCURRENCES = 6`
- `VALID_SR_IN_1_13_9 = NO`
- `OLD_GEOGRAPHIC_FOOTPRINT = 22 state regions listed by geographic_region_persia_old`
- `MODERN_GEOGRAPHIC_OBJECT = geographic_region_persia_old`
- `MODERN_STRATEGIC_REGION_IF_RELEVANT = region_greater_persia, but it adds five state regions and is therefore broader`
- `SEMANTIC_EQUIVALENCE = EXACT_LEGACY_STATE_REGION_FOOTPRINT`
- `MIGRATION_RULE = state.region comparison -> state is_in_geographic_region; direct capital.region comparison -> capital state scope`

## Portée du patch

- `TARGET_FILE_SHA256_BEFORE = ACD69F3AA69BB61DA79CD66734D2868DBEEA92E472AF785914A39603192A7515`
- `TARGET_FILE_SHA256_AFTER = 8DDCF06EF2A5C606F433A7C1390D64D94D110CD4B19B3E33A3F41EBAD6B4C3C6`
- `STATIC_INVALID_SR_REFERENCES_BEFORE = 49`
- `STATIC_INVALID_SR_REFERENCES_PATCHED = 49`
- `STATIC_INVALID_SR_REFERENCES_DEFERRED = 0`
- `STATIC_INVALID_SR_REFERENCES_AFTER = 0`
- `GAMEPLAY_CHANGED_FILES = 1`
- `GAMEPLAY_CHANGED_HUNKS = 16`
- `GAMEPLAY_INSERTIONS = 49`
- `GAMEPLAY_DELETIONS = 49`

Le BOM UTF-8 original est conservé. Le diff retire exactement les 49 expressions invalides et ajoute exactement les 49 expressions géographiques correspondantes.

## Validation statique

- six anciennes formes `sr:` : 49 → 0 ;
- références `sr:` absentes des définitions vanilla dans le fichier AI complet : 0 ;
- six objets `geographic_region_*_old` introduits : tous définis en vanilla 1.13.9 ;
- accolades hors commentaires : 2285 ouvrantes / 2285 fermantes ;
- `git diff --check` : PASS ;
- fichier gameplay modifié : le fichier autorisé uniquement ;
- valeurs, scores, conditions et commentaires changés : 0 ;
- index Git : vide ;
- staging/commit/push : aucun.

Les protections LOG-CLEANUP-6 restent en place : la structure moderne de `strategic_region_scores`, les sept triggers typés `has_port_country` / `has_port_state`, et les migrations Manchuria/Japan n'ont pas été modifiés. Aucune ancienne forme corrigée par LOG-CLEANUP-6 n'est réintroduite.

## Runtime humain et provenance

Codex n'a pas lancé Victoria 3. L'opérateur a chargé une nouvelle partie 1776 et l'a laissée tourner jusqu'au tick `1778.1.1`, confirmé dans `dedicated_server.log`, avant une fermeture propre.

- début de session : `2026-08-14 23:03:31 +02:00` ;
- fin de session : `2026-08-14 23:31:13 +02:00` ;
- build : `release/1.13.9 : afea32b87` ;
- DLC The Great Wave : monté ;
- mod monté : `Age of revolution /Fork|.../1776_Age_of_Revolutions_fork` ;
- autre build 1776 monté : aucun ;
- fermeture : `Quit from inside game`, transition `Game->Empty`, un joueur supprimé proprement.

Cette session a fait tourner `debug.1.log` à 23:03:35 avant de continuer dans `debug.log`. Les deux segments appartiennent donc au même runtime et ont été analysés. Les six rotations `error.5.log` à `error.log`, les six rotations `game.5.log` à `game.log`, `dedicated_server.log`, `system.log` et `code_revisions.log` ont également été parcourus.

Empreintes principales :

| Segment | Octets | SHA-256 |
|---|---:|---|
| `debug.1.log` | 79222 | `E5AB7E4F740801290E6AF34F9BD072C0E1EFF9CB2EFDB2A618B7521ED94A281E` |
| `debug.log` | 365891 | `3F8EAAB25AD4B02C4BA9274A2091A65D176D9E179EA8DF7540B2777D2BB75368` |
| `error.5.log` | 524108 | `5BD5C11AC1A8FD3B770CE9AF38886D376A710253FA042FC747D7CEABD7CC05B5` |
| `error.4.log` | 524145 | `DAD96A6F0CD3A8B5FF42AEAD1A04B4D923E5E2BB3486D180AB7870DF22BA389C` |
| `error.3.log` | 524140 | `7CB64A44FBAD96B9FA702B3127E314ED15DF6DFBC171F9CE59DB7C8CA505ACC4` |
| `error.2.log` | 524211 | `4B317F66B7139E8085AE41B818AF8CC0C90903010A979E42CED8888BD8EA0EC0` |
| `error.1.log` | 524160 | `B3261FABF6BDEB31CA6CB09D2DB97D55231F4882FD96BEB692CA5702024867C6` |
| `error.log` | 22705 | `BA02C944A4D250B91F041EB999EF87C432C762059AC754FF01F5794F9DC80378` |
| `dedicated_server.log` | 204748 | `AA3AAC66D5420AF2D4B71255ED3017E90171A842DF5F69EEAB4BE28CE342613A` |

## Résultats runtime

Les recherches couvrent les six anciennes régions, les six objets `_old`, le message `Invalid right side during comparison 'sr'` et chaque diagnostic visant `common/ai_strategies/00_default_strategy.txt`.

- `AI_RESIDUAL_RUNTIME_IDENTITIES_BEFORE = 8`
- `AI_RESIDUAL_RUNTIME_IDENTITIES_AFTER = 0`
- `AI_RESIDUAL_RUNTIME_OCCURRENCES_BEFORE = 96`
- `AI_RESIDUAL_RUNTIME_OCCURRENCES_AFTER = 0`
- diagnostics `jomini_script_system` visant le fichier AI : 0 identité / 0 occurrence ;
- erreur parser ou trigger visant les nouvelles expressions `is_in_geographic_region` : 0 ;
- `NEW_ATTRIBUTABLE_DIAGNOSTICS_FROM_PATCH = 0`.

Le seul diagnostic actuel visant le fichier AI est le `PostValidate of trigger 'is_building_type' returned false` à la ligne runtime 5119. Il est intentionnel, déjà connu et hors compteur correctif.

- `AI_FILE_DIAGNOSTICS_AFTER = 1` ;
- `AI_FILE_NEW_DIAGNOSTICS = 0` ;
- `KNOWN_AI_ERRORS_CLEARED = 8` ;
- `NEW_CONFIRMED_FORK_ERRORS_DISCOVERED = 0` ;
- `KNOWN_FORK_ERRORS_OPERATIONAL_AFTER = 15 - 8 + 0 = 7`.

Les sept erreurs opérationnelles restantes sont les deux diagnostics Interest Group et les cinq diagnostics create-character/template déjà réservés aux phases suivantes. Les cinq `UNKNOWN_REQUIRES_AUDIT` et les 113 diagnostics country-law historiques restent hors de ce compteur et hors du périmètre de LOG-CLEANUP-7.

## Conclusion et suite

`LOG_CLEANUP_7 = PASS` : les 49 références statiques sont migrées, les huit identités connues et leurs 96 occurrences sont absentes après une couverture plus longue que le minimum demandé, et aucune nouvelle erreur AI n'est découverte.

- `ESTIMATED_PHASES_REMAINING_MIN = 4`
- `ESTIMATED_PHASES_REMAINING_LIKELY = 5`
- `ESTIMATED_PHASES_REMAINING_MAX = 7`

`NEXT_PHASE = LOG-CLEANUP-8-INTEREST-GROUP-LEADER-SEMANTICS` n'est pas commencée.
