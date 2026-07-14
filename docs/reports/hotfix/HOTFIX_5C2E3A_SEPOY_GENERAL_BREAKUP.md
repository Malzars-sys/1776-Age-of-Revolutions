# HOTFIX-5C2E3A - Sepoy Mutiny general breakup

## 1. Resume

Cette phase migre uniquement les filtres regionaux invalides de
`sepoy_mutiny_events.2`, option `sepoy_mutiny_events.2.a`. Les sept groupes de
cinq anciennes strategic regions ont ete remplaces par les deux strategic
regions vanilla 1.13 `region_north_india` et `region_south_india`.

Exactement 35 anciennes references ont ete retirees. Aucune autre logique de
l'option, aucun autre event et aucune autre option n'ont ete modifies.

## 2. Etat Git initial

- Branche : `hotfix-dlc-audit`.
- Working tree : propre avant modification.
- HEAD initial : `956c514 Fix Sepoy presidency regional effects`.
- HOTFIX-5C2E2 est donc bien present dans HEAD.
- Stash detecte et laisse intact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.
- Aucun commit n'a ete cree pendant cette phase.

## 3. Comptage initial

Le comptage utilise les identifiants complets, commentaires exclus. Il ne
compte pas les IDs valides tels que `geographic_region_bombay_old`.

| Option | References initiales |
|---|---:|
| `sepoy_mutiny_events.2.a` | 35 |
| `sepoy_mutiny_events.2.b` | 28 |
| `sepoy_mutiny_events.2.c` | 28 |
| `sepoy_mutiny_events.2.e` | 28 |
| Total de `sepoy_mutiny_events.2` | 119 |

Le total runtime global initial documente par HOTFIX-5C2E2 etait de 250.

## 4. Comparaison fork, hotfix et vanilla

Le hunk de l'option 2.a a ete compare dans :

- fork : `events/india_events/sepoy_mutiny_events.txt` ;
- hotfix : `1776_Age_of_Revolutions_hotfix_source/events/india_events/sepoy_mutiny_events.txt` ;
- vanilla : `C:/Games/Victoria 3 The Great Wave/game/events/india_events/sepoy_mutiny_events.txt`.

Les options 2.a du hotfix et de la vanilla sont identiques. Dans chacun des
sept groupes regionaux, elles utilisent les deux strategic regions north/south
avec la syntaxe adaptee au scope :

- country/capital scope : `capital.region = sr:region_*_india` ;
- state scope : `region = sr:region_*_india`.

L'event complet n'a pas ete copie. Seuls ces sept hunks regionaux attestes ont
ete adaptes dans le fork.

## 5. Inventaire des sept groupes de l'option 2.a

| Groupe | Sous-bloc | Scope | Fonction |
|---:|---|---|---|
| 1 | `if.limit.any_subject_or_below` | Country/capital | Detecter les princely states concernes |
| 2 | `custom_tooltip.every_country.limit` | Country/capital | Filtrer les sujets rendus independants |
| 3 | `if.limit.any_scope_state` | State | Autoriser le breakup si un state concerne existe |
| 4 | `while.limit.any_scope_state` | State | Selectionner un state source pour la propagation |
| 5 | `any_neighbouring_state.owner.OR` | Country/capital | Valider la capitale d'un prince voisin |
| 6 | `every_country.limit.OR` | Country/capital | Selectionner le prince receveur |
| 7 | `random_scope_state.limit.OR` | State | Selectionner le state effectivement transfere |

## 6. Tableau avant/apres par groupe

| Groupe | Avant | Apres | Anciennes references retirees |
|---:|---|---|---:|
| 1 | 5 `capital.region` obsoletes | South + North India | 5 |
| 2 | 5 `capital.region` obsoletes | South + North India | 5 |
| 3 | 5 `region` obsoletes | North + South India | 5 |
| 4 | 5 `region` obsoletes | North + South India | 5 |
| 5 | 5 `capital.region` obsoletes | South + North India | 5 |
| 6 | 5 `capital.region` obsoletes | South + North India | 5 |
| 7 | 5 `region` obsoletes | North + South India | 5 |
| **Total** | **35** | **14 references valides** | **35** |

L'ordre north/south de chaque hunk suit exactement la version hotfix/vanilla.

## 7. Exceptions frontalieres preservees

Les exceptions explicites voisines n'ont pas ete elargies ni absorbees dans
`geographic_region_india` :

- `region_himalayas` : 3 occurrences preservees dans l'option 2.a ;
- `STATE_PASHTUNISTAN` : 7 occurrences preservees ;
- `STATE_QUETTA` : 7 occurrences preservees ;
- tests de capitale, voisinage, ownership, sujet et independance inchanges.

## 8. Effets territoriaux preserves

Le diff ne modifie que les sept listes de filtres regionaux. Sont notamment
inchanges : pays et tags, independance, creation de pays, ownership,
`set_state_owner`, transferts, controle, war goals, pactes, lois, modifiers,
valeurs numeriques, scopes sauvegardes, boucles `while`, limites de boucle,
priorites de reprise et ordre des effets.

## 9. Options 2.b, 2.c et 2.e

Les blocs extraits des options 2.b, 2.c et 2.e ont ete compares a HEAD : ils
sont strictement identiques. Les trois corrections de radicaux de HOTFIX-5C2E2
restent dans HEAD et ne sont pas reintroduites dans le diff courant.

## 10. Tableau des 35 references retirees

| Identifiant obsolete | Avant dans 2.a | Apres dans 2.a | Retirees |
|---|---:|---:|---:|
| `region_bengal` | 7 | 0 | 7 |
| `region_bombay` | 7 | 0 | 7 |
| `region_central_india` | 7 | 0 | 7 |
| `region_madras` | 7 | 0 | 7 |
| `region_punjab` | 7 | 0 | 7 |
| **Total** | **35** | **0** | **35** |

## 11. Comptage de la chaine Sepoy

| Perimetre | Avant | Retirees | Apres |
|---|---:|---:|---:|
| Option 2.a | 35 | 35 | 0 |
| Option 2.b | 28 | 0 | 28 |
| Option 2.c | 28 | 0 | 28 |
| Option 2.e | 28 | 0 | 28 |
| Chaine Sepoy concernee | 119 | 35 | 84 |

## 12. Total runtime global

Le recomptage dans `common/` et `events/`, commentaires exclus et IDs complets,
donne :

- avant HOTFIX-5C2E3A : 250 ;
- apres HOTFIX-5C2E3A : 215 ;
- diminution exacte : 35.

## 13. Zero ancien ID dans l'option 2.a

Apres modification, l'option 2.a contient zero occurrence de chacun des cinq
IDs invalides. Elle contient sept occurrences de `region_north_india` et sept
occurrences de `region_south_india`, une paire par groupe autorise.

## 14. Repartition des 84 references restantes

Les 84 anciennes references restantes dans `sepoy_mutiny_events.2` sont
reparties uniquement ainsi :

- option 2.b : 28 ;
- option 2.c : 28 ;
- option 2.e : 28.

Aucune ancienne reference ne reste dans l'option 2.a.

## 15. Risques restants

- Les options 2.b, 2.c et 2.e conservent volontairement 84 references
  obsoletes pour leurs phases territoriales dediees.
- North/South India couvrent des strategic regions plus larges que les cinq
  anciennes regions ; ce comportement est celui de la vanilla 1.13 et reste
  borne par les conditions et exceptions explicites existantes.
- La logique de breakup doit encore etre validee en jeu avec une mutinerie
  effectivement declenchee, pas seulement au chargement.

## 16. Tests en jeu recommandes

1. Lancer le mod seul et verifier menu, selection de pays et chargement BIC.
2. Confirmer l'absence d'erreur `region_bengal`, `region_bombay`,
   `region_central_india`, `region_madras` ou `region_punjab` provenant du hunk
   de l'option 2.a.
3. Declencher `sepoy_mutiny_events.2` dans une sauvegarde de test.
4. Choisir l'option 2.a et verifier l'independance des princely states.
5. Verifier que les states Himalaya, Pashtunistan et Quetta suivent toujours
   les exceptions explicites.
6. Observer la selection du prince receveur et le transfert aleatoire d'un
   state voisin.
7. Surveiller `error.log`, `game.log` et `debug.log` pendant le breakup.

## 17. Fichiers modifies ou crees

- Modifie : `events/india_events/sepoy_mutiny_events.txt`.
- Cree :
  `docs/reports/hotfix/HOTFIX_5C2E3A_SEPOY_GENERAL_BREAKUP.md`.

## 18. Confirmation du perimetre gameplay

Aucun autre fichier gameplay n'a ete modifie. La journal entry Sepoy,
`sepoy_mutiny_events.4`, les progress bars, localisations, formations, BIC,
Durrani, Indian Famines, India Railway, NAVY, ADMIN, MARATH et Travancore sont
restes inchanges.

## 19. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` n'a ete ni applique, ni
modifie, ni supprime.
