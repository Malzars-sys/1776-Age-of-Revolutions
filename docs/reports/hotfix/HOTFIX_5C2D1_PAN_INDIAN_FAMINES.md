# HOTFIX-5C2D1 - Pan-Indian Famines

## 1. Resume

Cette phase retire exactement 90 references aux cinq anciennes strategic regions indiennes dans la chaine Indian Famines. Les controles larges de la journal entry utilisent maintenant `geographic_region_india`; son sous-bloc `possible` et les huit listes des events utilisent les strategic regions valides `region_north_india` et `region_south_india`.

La journal entry conserve volontairement dix anciennes references: cinq selecteurs regionaux ambigus et cinq completions historiques reservees aux phases suivantes.

## 2. Etat Git initial

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `c75ea27 Audit Indian Famines region migration` |
| Audit HOTFIX-5C2D | Commit present |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Action sur le stash | Aucune |

## 3. Comptage initial

| Fichier | References initiales |
|---|---:|
| `common/journal_entries/04_indian_famines.txt` | 60 |
| `events/india_events/indian_famines.txt` | 40 |
| **Total** | **100** |

Le total runtime global initial, commentaires exclus, etait de **373**.

## 4. Comparaison fork/hotfix/vanilla

L'audit HOTFIX-5C2D a confirme que les versions hotfix et vanilla sont bit-a-bit identiques pour les deux fichiers de la chaine. Aucun fichier entier n'a ete copie. Seuls les hunks regionaux autorises ont ete reproduits:

- `is_in_geographic_region = geographic_region_india` dans les state scopes larges;
- `region = sr:region_north_india` et `region = sr:region_south_india` dans les controles fondes sur les strategic regions.

## 5. Controles Geographic India corriges

Neuf listes de cinq anciennes regions de `je_indian_famines` ont ete remplacees par neuf tests `geographic_region_india`:

| Bloc | Listes | Anciennes references retirees |
|---|---:|---:|
| `is_shown_when_inactive` | 1 | 5 |
| `possible`, seuil de grande famine | 1 | 5 |
| `immediate`, definition de `great_indian_famine_var` | 1 | 5 |
| Cinq gardes d'exclusion de grande famine | 5 | 25 |
| `complete`, fin de la grande famine | 1 | 5 |
| **Total** | **9** | **45** |

Les seuils de quinze states, `has_famine`, les `NOT`, variables, scopes, garde IP2, modifiers, tooltips et poids d'events sont inchanges.

## 6. Hunk `possible` north/south

Les cinq branches regionales invalides de `je_indian_famines.possible` ont ete remplacees par le hunk exact hotfix/vanilla:

```txt
any_scope_state = {
	region = sr:region_north_india
	has_famine = yes
	count >= 4
}
any_scope_state = {
	region = sr:region_south_india
	has_famine = yes
	count >= 4
}
```

La troisieme branche de grande famine reste separee avec `geographic_region_india` et `count >= 15`. Aucun seuil n'a ete invente ou modifie independamment du hunk de reference.

## 7. Events corriges

Dans `events/india_events/indian_famines.txt`, huit listes de cinq anciennes regions ont ete remplacees par les deux strategic regions valides, dans l'ordre exact hotfix/vanilla `south`, puis `north`.

| Event | Blocs corriges | Listes | References retirees |
|---|---|---:|---:|
| `indian_famines.1` | `trigger`; `immediate/random_scope_state.limit` | 2 | 10 |
| `indian_famines.2` | `trigger`; `immediate`; option A tooltip; option A effet cache | 4 | 20 |
| `indian_famines.4` | `trigger`; `immediate/random_scope_state.limit` | 2 | 10 |
| **Total** | | **8** | **40** |

`indian_famines.3` est strictement identique a HEAD. Aucun ID, trigger non regional, random/ordered iterator, plantation, niveau de building, agitateur, variable, option, modifier, effet, delai, poids IA, tooltip ou localisation appelee n'a change.

## 8. Tableau des 90 references retirees

| Domaine | Geographic India | North/south | Total retire |
|---|---:|---:|---:|
| JE, controles larges | 45 | 0 | 45 |
| JE, hunk `possible` | 0 | 5 | 5 |
| Events Indian Famines | 0 | 40 | 40 |
| **Total** | **45** | **45** | **90** |

## 9. Chaine avant/apres

| Fichier | Avant | Retirees | Apres |
|---|---:|---:|---:|
| JE Indian Famines | 60 | 50 | **10** |
| Events Indian Famines | 40 | 40 | **0** |
| **Total chaine** | **100** | **90** | **10** |

## 10. Total global avant/apres

Le recomptage de `common/` et `events/`, commentaires exclus, passe exactement de **373** a **283** anciennes references runtime.

## 11. Dix references volontairement conservees

| Type protege | Variable | Reference conservee | Ligne apres modification |
|---|---|---|---:|
| Selecteur `immediate` | `bengal_famine_var` | `region_bengal` | 61 |
| Selecteur `immediate` | `punjab_famine_var` | `region_punjab` | 78 |
| Selecteur `immediate` | `bombay_famine_var` | `region_bombay` | 95 |
| Selecteur `immediate` | `madras_famine_var` | `region_madras` | 112 |
| Selecteur `immediate` | `central_india_famine_var` | `region_central_india` | 129 |
| Completion historique | `bengal_famine_var` | `region_bengal` | 152 |
| Completion historique | `bombay_famine_var` | `region_bombay` | 163 |
| Completion historique | `madras_famine_var` | `region_madras` | 174 |
| Completion historique | `punjab_famine_var` | `region_punjab` | 185 |
| Completion historique | `central_india_famine_var` | `region_central_india` | 196 |

## 12. Selecteurs inchanges

Les cinq tests directs qui definissent les variables regionales sont strictement inchanges par rapport a HEAD. Leur ordre `else_if`, leurs seuils, leurs variables et leurs anciennes references sont preserves pour HOTFIX-5C2D3.

## 13. Completions historiques inchangees

Les cinq `trigger_if` de `complete` lies aux variables regionales sont strictement inchanges par rapport a HEAD. Ils restent reserves a HOTFIX-5C2D2.

## 14. Seuils importes

Le hunk `possible` correspond exactement au hotfix et a la vanilla: `count >= 4` pour north, `count >= 4` pour south, et `count >= 15` pour Geographic India. Aucun autre seuil n'a ete modifie.

## 15. Risque de declenchement en 1776

La JE est gardee par `ip2_content`, mais ne possede pas de garde chronologique ou technologique. Une fois les controles valides, elle peut donc devenir active en 1776 si les seuils de famine sont atteints. Son `on_yearly_pulse` peut alors appeler `.1`, `.2` et `.4`. Cette phase ne change aucune date ni frequence; le comportement doit etre observe en jeu avant toute adaptation historique distincte.

## 16. Tests recommandes

1. Lancer une partie 1776 avec IP2 actif et uniquement le mod.
2. Verifier l'affichage et l'activation de `je_indian_famines` pour BIC et un pays sud-asiatique.
3. Tester les seuils north/south de quatre states et le seuil panindien de quinze states.
4. Verifier les selections de state des events `.1`, `.2` et `.4`.
5. Confirmer que `.2` conserve ses conditions de plantations, agitateur et `hunger_strike_var`.
6. Surveiller `error.log` pour les cinq anciens IDs, `Invalid right side`, `Invalid strategic region` et erreurs de scope.

## 17. Fichiers modifies/crees

- `common/journal_entries/04_indian_famines.txt`
- `events/india_events/indian_famines.txt`
- `docs/reports/hotfix/HOTFIX_5C2D1_PAN_INDIAN_FAMINES.md`

## 18. Autre gameplay inchange

Aucun autre gameplay n'a ete modifie. Sepoy Mutiny, Durrani, BIC historique, `law_frontier_colonization`, India Railway, company types, formations, buildings, localisations, scripted buttons, NAVY, ADMIN, MARATH et Travancore sont inchanges.

## 19. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present et intact. Il n'a ete ni applique, ni inspecte comme contenu courant, ni restaure, ni supprime.
