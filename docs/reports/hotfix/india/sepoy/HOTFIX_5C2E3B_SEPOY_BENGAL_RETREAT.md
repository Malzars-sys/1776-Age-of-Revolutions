# HOTFIX-5C2E3B - Sepoy Mutiny Bengal retreat

## 1. Resume

Cette phase migre uniquement les sept filtres regionaux de l'option
`sepoy_mutiny_events.2.b`. Les 28 references invalides ont ete remplacees par
les conditions `region_north_india` et `region_south_india` attestees dans le
hotfix et la vanilla 1.13.

La logique de retraite de BIC vers son noyau bengali, les listes de reprises
prioritaires et tous les effets territoriaux sont inchanges.

## 2. Etat Git initial

- Branche : `hotfix-dlc-audit`.
- Working tree : propre avant modification.
- HEAD initial : `1e0ae83 Fix Sepoy general breakup regions`.
- HOTFIX-5C2E3A etait donc committe avant cette phase.
- Stash preserve :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.
- Aucun commit n'a ete cree pendant cette phase.

## 3. Comptage initial

Le comptage porte sur les IDs complets, commentaires exclus, sans compter les
identifiants valides `geographic_region_*_old`.

| Option | References initiales |
|---|---:|
| 2.a | 0 |
| 2.b | 28 |
| 2.c | 28 |
| 2.e | 28 |
| Chaine Sepoy | 84 |

Le total runtime global initial etait de 215.

## 4. Comparaison fork, hotfix et vanilla

L'option 2.b a ete comparee entre :

- le fork : `events/india_events/sepoy_mutiny_events.txt` ;
- le hotfix upstream : le meme chemin sous
  `1776_Age_of_Revolutions_hotfix_source` ;
- la vanilla :
  `C:/Games/Victoria 3 The Great Wave/game/events/india_events/sepoy_mutiny_events.txt`.

Hotfix et vanilla utilisent la meme structure dans les sept groupes :

- scope country/capital : `capital.region = sr:region_south_india`, puis
  `capital.region = sr:region_north_india` ;
- scope state : `region = sr:region_north_india`, puis
  `region = sr:region_south_india`.

L'event complet n'a pas ete copie. Seuls les hunks contenant les quatre IDs
invalides de chaque groupe ont ete adaptes.

## 5. Inventaire des sept groupes de l'option 2.b

| Groupe | Sous-bloc | Scope | Fonction |
|---:|---|---|---|
| 1 | `if.limit.any_subject_or_below` | Country/capital | Detecter les princely states concernes |
| 2 | `custom_tooltip.every_country.limit` | Country/capital | Rendre independants les sujets hors du repli |
| 3 | `if.limit.any_scope_state` | State | Autoriser le breakup territorial |
| 4 | `while.limit.any_scope_state` | State | Choisir un state BIC source de propagation |
| 5 | `any_neighbouring_state.owner.OR` | Country/capital | Valider le prince voisin |
| 6 | `every_country.limit.OR` | Country/capital | Selectionner le prince receveur |
| 7 | `random_scope_state.limit.OR` | State | Selectionner le state transfere |

## 6. Tableau avant/apres par groupe

| Groupe | Avant | Apres | References retirees |
|---:|---|---|---:|
| 1 | Bombay, Madras, Punjab, Central India | South + North India | 4 |
| 2 | Bombay, Madras, Punjab, Central India | South + North India | 4 |
| 3 | Punjab, Central India, Bombay, Madras | North + South India | 4 |
| 4 | Punjab, Central India, Bombay, Madras | North + South India | 4 |
| 5 | Bombay, Madras, Punjab, Central India | South + North India | 4 |
| 6 | Bombay, Madras, Punjab, Central India | South + North India | 4 |
| 7 | Punjab, Central India, Bombay, Madras | North + South India | 4 |
| **Total** | **28** | **14 references valides** | **28** |

## 7. Noyau bengali conserve

La retraite bengalie reste definie par les conditions et listes explicites de
l'option, notamment :

- penalite IA si BIC ne possede pas `STATE_EAST_BENGAL` ;
- option disponible seulement avec un scope state dans `STATE_WEST_BENGAL` ;
- logique de reprise et de conservation territoriale deja presente dans le
  hunk local.

Ces lignes n'ont pas ete remplacees par une geographic region large. Aucun
usage de `geographic_region_bengal_old` n'a ete invente.

## 8. Exceptions frontalieres preservees

- `region_himalayas` : 3 occurrences conservees dans 2.b ;
- `STATE_PASHTUNISTAN` : 7 occurrences conservees ;
- `STATE_QUETTA` : 7 occurrences conservees ;
- conditions de capitale, voisinage, ownership, sujet et independance
  inchangees.

## 9. Listes de states et effets territoriaux preserves

Toutes les listes explicites de states et de reprises prioritaires sont restees
identiques. Cela inclut notamment Madras, Mandalay, Pegu, Gujarat, Tenasserim,
Travancore, Circars, Kurnool, Delhi, Agra, Awadh, Central Provinces et Bombay.

Les tags receveurs, `make_independent`, `set_state_owner`, transferts, boucles,
limites numeriques, scopes sauvegardes et ordre des effets sont inchanges.
L'effet final de radicaux de HOTFIX-5C2E2 est egalement identique a HEAD.

## 10. Options 2.a, 2.c et 2.e

Les blocs extraits ont ete compares a HEAD :

- option 2.a : identique, avec les corrections HOTFIX-5C2E3A conservees ;
- option 2.c : identique, avec 28 anciennes references ;
- option 2.e : identique, avec 28 anciennes references.

## 11. Tableau des 28 references retirees

| Identifiant | Avant dans 2.b | Apres dans 2.b | Retirees |
|---|---:|---:|---:|
| `region_bengal` | 0 | 0 | 0 |
| `region_bombay` | 7 | 0 | 7 |
| `region_central_india` | 7 | 0 | 7 |
| `region_madras` | 7 | 0 | 7 |
| `region_punjab` | 7 | 0 | 7 |
| **Total** | **28** | **0** | **28** |

## 12. Comptage de la chaine Sepoy

| Option | Avant | Retirees | Apres |
|---|---:|---:|---:|
| 2.a | 0 | 0 | 0 |
| 2.b | 28 | 28 | 0 |
| 2.c | 28 | 0 | 28 |
| 2.e | 28 | 0 | 28 |
| **Chaine Sepoy** | **84** | **28** | **56** |

## 13. Total runtime global

- Avant HOTFIX-5C2E3B : 215 references invalides.
- Apres HOTFIX-5C2E3B : 187 references invalides.
- Diminution exacte : 28.

## 14. Zero ancien ID dans l'option 2.b

L'option 2.b ne contient plus aucun des cinq anciens IDs. Les sept groupes
migres contiennent chacun une paire north/south. L'option compte huit usages de
`region_north_india` au total, car un huitieme usage preexistant appartient a
l'effet final de radicaux committe dans HOTFIX-5C2E2 ; cet usage n'a pas ete
modifie. Elle contient sept usages de `region_south_india`.

## 15. Repartition des 56 references restantes

Les 56 anciennes references restantes dans `sepoy_mutiny_events.2`
appartiennent uniquement a :

- option 2.c : 28 ;
- option 2.e : 28.

## 16. Risques restants

- Les options 2.c et 2.e conservent volontairement leurs filtres obsoletes
  jusqu'a leurs phases dediees.
- North/South India couvrent des zones plus larges que les quatre anciennes
  regions excluant Bengal ; le comportement territorial reste toutefois celui
  du hunk vanilla/hotfix, borne par les listes explicites du repli bengali.
- Une validation en jeu de la branche 2.b reste necessaire pour confirmer la
  repartition territoriale effective.

## 17. Tests en jeu recommandes

1. Lancer une partie BIC et verifier l'absence d'erreur au chargement.
2. Declencher `sepoy_mutiny_events.2` dans une sauvegarde de test.
3. Choisir l'option 2.b et confirmer que BIC conserve son noyau bengali.
4. Verifier l'independance des sujets et les reprises prioritaires explicites.
5. Controler les transferts vers les princes voisins, y compris les exceptions
   Himalaya, Pashtunistan et Quetta.
6. Confirmer que l'effet de radicaux north India est toujours execute.
7. Surveiller `error.log`, `game.log` et `debug.log` pendant le breakup.

## 18. Fichiers modifies ou crees

- Modifie : `events/india_events/sepoy_mutiny_events.txt`.
- Cree :
  `docs/reports/hotfix/HOTFIX_5C2E3B_SEPOY_BENGAL_RETREAT.md`.

## 19. Confirmation du perimetre gameplay

Aucun autre gameplay n'a ete modifie. La journal entry Sepoy,
`sepoy_mutiny_events.4`, les progress bars, localisations, scripted effects,
BIC, Durrani, Indian Famines, India Railway, NAVY, ADMIN, MARATH et Travancore
sont restes inchanges.

## 20. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` n'a ete ni applique, ni
modifie, ni supprime.
