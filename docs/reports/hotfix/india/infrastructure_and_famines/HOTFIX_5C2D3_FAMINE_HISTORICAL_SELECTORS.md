# HOTFIX-5C2D3 - Famine historical selectors

## 1. Resume

Cette phase corrige uniquement les cinq selecteurs regionaux de `je_indian_famines.immediate`. Chaque ancienne reference est remplacee par la geographic region historique vanilla `*_old` correspondant a la variable posee. La chaine Indian Famines ne contient desormais plus aucune reference aux cinq anciennes strategic regions invalides.

## 2. Etat Git initial

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `6a993c6 Fix historical famine completion regions` |
| HOTFIX-5C2D2 | Commit present |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

## 3. Comptage initial

Avant modification, `common/journal_entries/04_indian_famines.txt` contenait exactement cinq anciennes references. Elles se trouvaient toutes dans les branches `else_if` de `immediate` et definissaient les cinq variables historiques. Le bloc `complete` contenait deja zero ancienne reference. Le total runtime global etait de **278**.

## 4. Decision de design

Les selecteurs utilisent les cinq subdivisions historiques vanilla plutot que les deux grandes strategic regions north/south. Ce choix maintient la coherence entre:

- la zone ou la famine est detectee;
- la variable historique posee;
- le nom dynamique affiche par la JE;
- la zone de completion corrigee dans HOTFIX-5C2D2.

L'ordre des branches et leurs seuils restent strictement identiques.

## 5. Pourquoi le hunk north/south n'a pas ete importe

Le hunk vanilla/hotfix fusionne Bengal, Punjab et Central India dans `region_north_india`, et Bombay/Madras dans `region_south_india`. Avec l'ordre actuel des `else_if`:

- Bengal north `count >= 5` capture la branche avant Central India;
- Bombay south `count >= 4` capture la branche avant Madras `count >= 5`;
- les variables historiques peuvent ensuite etre terminees par une subdivision `*_old` differente de la zone qui a declenche la variable.

Les subdivisions historiques evitent cette incoherence sans changer les seuils ou la structure.

## 6. Definitions vanilla verifiees

Reference: `C:\Games\Victoria 3 The Great Wave\game\common\geographic_regions\06_old_strategic_regions.txt`.

| Geographic region | State regions membres |
|---|---|
| `geographic_region_bengal_old` | Bihar, East Bengal, West Bengal, Assam, Orissa |
| `geographic_region_punjab_old` | Punjab, Hill Punjab, Delhi, Rajputana |
| `geographic_region_bombay_old` | Bombay, Gujarat, Sindh, Baluchistan |
| `geographic_region_madras_old` | Ceylon, Circars, Mysore, Travancore, Madras, Hyderabad, Kurnool |
| `geographic_region_central_india_old` | Central Provinces, Awadh, Malwa, Agra, Bundelkhand |

La syntaxe state-scope valide est `is_in_geographic_region = geographic_region_*_old`.

## 7. Tableau des cinq mappages

| Variable posee | Ancienne reference | Nouveau selecteur |
|---|---|---|
| `bengal_famine_var` | `region_bengal` | `geographic_region_bengal_old` |
| `punjab_famine_var` | `region_punjab` | `geographic_region_punjab_old` |
| `bombay_famine_var` | `region_bombay` | `geographic_region_bombay_old` |
| `madras_famine_var` | `region_madras` | `geographic_region_madras_old` |
| `central_india_famine_var` | `region_central_india` | `geographic_region_central_india_old` |

## 8. Modification des selecteurs immediate

Le diff remplace exactement cinq lignes dans `immediate`. Les `any_scope_state`, `has_famine`, `count >=`, `NOT`, gardes de grande famine, variables et structures englobantes sont inchanges. Aucune branche n'a ete fusionnee, supprimee ou reordonnee.

## 9. Coherence selecteur/completion

| Variable | Selecteur immediate | Completion |
|---|---|---|
| `bengal_famine_var` | `geographic_region_bengal_old` | `geographic_region_bengal_old` |
| `punjab_famine_var` | `geographic_region_punjab_old` | `geographic_region_punjab_old` |
| `bombay_famine_var` | `geographic_region_bombay_old` | `geographic_region_bombay_old` |
| `madras_famine_var` | `geographic_region_madras_old` | `geographic_region_madras_old` |
| `central_india_famine_var` | `geographic_region_central_india_old` | `geographic_region_central_india_old` |

Chaque geographic region historique apparait exactement deux fois dans la JE: une fois dans `immediate` et une fois dans `complete`.

## 10. Ordre et seuils inchanges

L'ordre reste Bengal, Punjab, Bombay, Madras, Central India. Les seuils restent respectivement 5, 4, 4, 5 et 5 states en famine. `great_indian_famine_var`, les gardes de quinze states, `is_shown_when_inactive`, `possible`, `complete` et `on_yearly_pulse` sont inchanges.

## 11. Comptage Famines avant/apres

| Fichier | Avant | Retirees | Apres |
|---|---:|---:|---:|
| JE Indian Famines | 5 | 5 | **0** |
| Events Indian Famines | 0 | 0 | **0** |
| **Total chaine** | **5** | **5** | **0** |

## 12. Total runtime global avant/apres

Le recomptage de `common/` et `events/`, commentaires exclus, passe exactement de **278** a **273** anciennes references runtime.

## 13. Risques restants

Si plusieurs subdivisions historiques atteignent leur seuil simultanement, l'ordre conserve des `else_if` choisit toujours la premiere branche eligible. La JE reste gardee par IP2 mais sans date ou technologie; elle peut donc fonctionner en 1776 si les seuils de famine sont atteints. Ces comportements sont preexistants et ne sont pas modifies dans cette phase.

## 14. Tests recommandes

1. Lancer une partie 1776 avec IP2 actif et uniquement le mod.
2. Tester separement Bengal, Punjab, Bombay, Madras et Central India aux seuils 5/4/4/5/5.
3. Verifier la variable posee et le nom dynamique de la JE pour chaque subdivision.
4. Verifier que la completion attend la fin des famines dans la meme subdivision historique.
5. Tester plusieurs famines regionales simultanees pour confirmer l'ordre des `else_if`.
6. Surveiller `error.log` pour les cinq anciens IDs, `Invalid right side`, `Invalid strategic region` et erreurs de scope.

## 15. Fichiers modifies/crees

- `common/journal_entries/04_indian_famines.txt`
- `docs/reports/hotfix/HOTFIX_5C2D3_FAMINE_HISTORICAL_SELECTORS.md`

## 16. Autre gameplay inchange

Aucun autre gameplay n'a ete modifie. Le bloc `complete`, les events Indian Famines, Sepoy Mutiny, Durrani, BIC, `law_frontier_colonization`, India Railway, formations, buildings, localisations, scripted buttons, NAVY, ADMIN, MARATH et Travancore sont inchanges.

## 17. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present et intact. Il n'a ete ni applique, ni inspecte comme contenu courant, ni restaure, ni supprime.
