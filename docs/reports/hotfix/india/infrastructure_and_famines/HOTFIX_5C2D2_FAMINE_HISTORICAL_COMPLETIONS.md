# HOTFIX-5C2D2 - Famine historical completions

## 1. Resume

Cette phase corrige uniquement les cinq conditions regionales de `je_indian_famines.complete`. Chaque ancienne reference est remplacee par sa geographic region historique vanilla `*_old`. Les cinq selecteurs regionaux ambigus du bloc `immediate` restent inchanges pour HOTFIX-5C2D3.

## 2. Etat Git initial

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `4b8b22a Fix pan-Indian famine region checks` |
| HOTFIX-5C2D1 | Commit present |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

## 3. Comptage initial

Avant modification, la JE contenait dix anciennes references: cinq selecteurs dans `immediate` et cinq completions dans `complete`. Le total runtime global, commentaires exclus, etait de **283**.

## 4. Definitions vanilla verifiees

Reference: `C:\Games\Victoria 3 The Great Wave\game\common\geographic_regions\06_old_strategic_regions.txt`.

| Geographic region | State regions membres |
|---|---|
| `geographic_region_bengal_old` | Bihar, East Bengal, West Bengal, Assam, Orissa |
| `geographic_region_bombay_old` | Bombay, Gujarat, Sindh, Baluchistan |
| `geographic_region_madras_old` | Ceylon, Circars, Mysore, Travancore, Madras, Hyderabad, Kurnool |
| `geographic_region_punjab_old` | Punjab, Hill Punjab, Delhi, Rajputana |
| `geographic_region_central_india_old` | Central Provinces, Awadh, Malwa, Agra, Bundelkhand |

La vanilla utilise dans les memes state scopes la syntaxe `is_in_geographic_region = geographic_region_*_old`.

## 5. Tableau des cinq mappages

| Variable | Ancienne reference | Nouveau test vanilla |
|---|---|---|
| `bengal_famine_var` | `region_bengal` | `geographic_region_bengal_old` |
| `bombay_famine_var` | `region_bombay` | `geographic_region_bombay_old` |
| `madras_famine_var` | `region_madras` | `geographic_region_madras_old` |
| `punjab_famine_var` | `region_punjab` | `geographic_region_punjab_old` |
| `central_india_famine_var` | `region_central_india` | `geographic_region_central_india_old` |

## 6. Modifications du bloc complete

Les cinq `trigger_if` concernes conservent strictement leur `has_variable`, `NOT`, `any_scope_state`, `has_famine`, ordre et structure. Chaque diff remplace une seule ligne `region = region_*` par une seule ligne `is_in_geographic_region = geographic_region_*_old`.

## 7. Selecteurs immediate inchanges

Les cinq selecteurs directs de `immediate` sont byte-a-byte identiques a HEAD:

- `bengal_famine_var` avec `region_bengal`;
- `punjab_famine_var` avec `region_punjab`;
- `bombay_famine_var` avec `region_bombay`;
- `madras_famine_var` avec `region_madras`;
- `central_india_famine_var` avec `region_central_india`.

Ils sont reserves a HOTFIX-5C2D3.

## 8. Comptage JE avant/apres

| Etat | Anciennes references exactes |
|---|---:|
| Avant HOTFIX-5C2D2 | 10 |
| Retirees | 5 |
| Apres HOTFIX-5C2D2 | **5** |

Les cinq references restantes sont toutes dans `immediate`. Les cinq conditions de `complete` ne contiennent plus aucune ancienne reference et contiennent exactement les cinq geographic regions historiques ci-dessus.

## 9. Total runtime global avant/apres

Le recomptage de `common/` et `events/`, commentaires exclus, passe exactement de **283** a **278** references invalides.

## 10. Variables et ordre des branches

Aucune variable n'a ete renommee. L'ordre des branches `trigger_if` de `complete` et des `else_if` de `immediate` est inchange. Aucun seuil, date, garde DLC, modifier ou tooltip n'a ete modifie.

## 11. Events Famines inchanges

`events/india_events/indian_famines.txt`, y compris `indian_famines.3`, est inchange par rapport a HEAD.

## 12. Risques restants

HOTFIX-5C2D3 reste necessaire pour les cinq selecteurs `immediate` ambigus. Ils decident quelle variable historique est posee; leur remplacement demande encore un choix explicite entre le comportement vanilla north/south et la preservation semantique par subdivisions `*_old`.

## 13. Tests recommandes

1. Lancer une partie avec IP2 actif et uniquement le mod.
2. Verifier que chaque variable de famine regionale se termine seulement quand aucune famine ne reste dans sa subdivision historique correspondante.
3. Verifier les tooltips et le nom dynamique de la JE pour Bengal, Bombay, Madras, Punjab et Central India.
4. Surveiller `error.log` pour les cinq anciens IDs, `Invalid right side`, `Invalid strategic region` et erreurs de scope.

## 14. Fichiers modifies/crees

- `common/journal_entries/04_indian_famines.txt`
- `docs/reports/hotfix/HOTFIX_5C2D2_FAMINE_HISTORICAL_COMPLETIONS.md`

## 15. Autre gameplay inchange

Aucun autre gameplay n'a ete modifie. `is_shown_when_inactive`, `possible`, `immediate`, `on_yearly_pulse`, les events Famines, Sepoy Mutiny, Durrani, BIC, `law_frontier_colonization`, formations, buildings, localisations, scripted buttons, NAVY, ADMIN, MARATH et Travancore sont inchanges.

## 16. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present et intact. Il n'a ete ni applique, ni inspecte comme contenu courant, ni restaure, ni supprime.
