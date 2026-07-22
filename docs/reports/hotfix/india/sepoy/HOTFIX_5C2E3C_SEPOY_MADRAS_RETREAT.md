# HOTFIX-5C2E3C - Sepoy Mutiny Madras retreat

## 1. Resume

Cette phase migre uniquement les sept filtres regionaux de l'option
`sepoy_mutiny_events.2.c`. Les 28 references invalides ont ete remplacees par
les conditions `region_south_india` et `region_north_india` attestees dans le
hotfix et la vanilla 1.13.

La retraite de BIC vers Madras, les listes de reprises prioritaires et tous les
effets territoriaux sont inchanges.

## 2. Etat Git initial

- Branche : `hotfix-dlc-audit`.
- Working tree : propre avant modification.
- HEAD initial : `b484200 Fix Sepoy Bengal retreat regions`.
- HOTFIX-5C2E3B etait committe avant cette phase.
- Stash preserve :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.
- Aucun commit n'a ete cree pendant cette phase.

## 3. Comptage initial

Le comptage porte sur les IDs complets, commentaires exclus, sans compter les
identifiants valides `geographic_region_*_old`.

| Option | References initiales |
|---|---:|
| 2.a | 0 |
| 2.b | 0 |
| 2.c | 28 |
| 2.e | 28 |
| Chaine Sepoy | 56 |

Le total runtime global initial etait de 187.

## 4. Comparaison fork, hotfix et vanilla

L'option 2.c a ete comparee entre le fork, le hotfix upstream et
`C:/Games/Victoria 3 The Great Wave/game/events/india_events/sepoy_mutiny_events.txt`.

Hotfix et vanilla utilisent la meme structure dans les sept groupes :

- country/capital scope : `capital.region = sr:region_south_india`, puis
  `capital.region = sr:region_north_india` ;
- state scope : `region = sr:region_south_india`, puis
  `region = sr:region_north_india`.

Une nuance du fork a ete preservee dans l'analyse : le premier groupe contenait
Madras parmi ses quatre anciens IDs, tandis que les six autres contenaient
Bengal a sa place. Aucun event complet n'a ete copie.

## 5. Inventaire des sept groupes de l'option 2.c

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

| Groupe | Anciennes references | Hunk vanilla applique | Retirees |
|---:|---|---|---:|
| 1 | Bombay, Madras, Punjab, Central India | South + North India | 4 |
| 2 | Bombay, Bengal, Punjab, Central India | South + North India | 4 |
| 3 | Punjab, Central India, Bombay, Bengal | South + North India | 4 |
| 4 | Punjab, Central India, Bombay, Bengal | South + North India | 4 |
| 5 | Bombay, Bengal, Punjab, Central India | South + North India | 4 |
| 6 | Bombay, Bengal, Punjab, Central India | South + North India | 4 |
| 7 | Punjab, Central India, Bombay, Bengal | South + North India | 4 |
| **Total** | **28** | **14 references valides** | **28** |

## 7. Noyau de Madras conserve

L'option reste conditionnee par la presence d'un scope state dans
`STATE_MADRAS`. Cette condition n'a pas ete modifiee, completee ou remplacee
par `geographic_region_madras_old`.

Les reprises prioritaires explicites du fork restent dans leur ordre initial.
La logique n'a pas ete transformee en breakup panindien generique.

## 8. Exceptions frontalieres preservees

- `region_himalayas` : 3 occurrences conservees dans 2.c ;
- `STATE_PASHTUNISTAN` : 7 occurrences conservees ;
- `STATE_QUETTA` : 7 occurrences conservees ;
- tests de capitale, voisinage, ownership, sujet et independance inchanges.

## 9. Listes de states et effets territoriaux preserves

Les states explicitement presents dans l'option restent inchanges, notamment
Madras, Mandalay, Pegu, Gujarat, Tenasserim, Travancore, Delhi, Agra, Awadh,
Central Provinces et Bombay. Aucun state absent n'a ete ajoute.

Les tags receveurs, `make_independent`, `set_state_owner`, transferts, boucles,
limites numeriques, scopes sauvegardes et ordre des effets sont inchanges.
L'effet final de radicaux corrige par HOTFIX-5C2E2 est identique a HEAD.

## 10. Options 2.a, 2.b et 2.e

Les blocs extraits ont ete compares a HEAD :

- option 2.a : identique ;
- option 2.b : identique, avec HOTFIX-5C2E3B conserve ;
- option 2.e : identique, avec ses 28 anciennes references reservees a la
  phase HOTFIX-5C2E3D.

## 11. Tableau des 28 references retirees

| Identifiant | Avant dans 2.c | Apres dans 2.c | Retirees |
|---|---:|---:|---:|
| `region_bengal` | 6 | 0 | 6 |
| `region_bombay` | 7 | 0 | 7 |
| `region_central_india` | 7 | 0 | 7 |
| `region_madras` | 1 | 0 | 1 |
| `region_punjab` | 7 | 0 | 7 |
| **Total** | **28** | **0** | **28** |

## 12. Comptage de la chaine Sepoy

| Option | Avant | Retirees | Apres |
|---|---:|---:|---:|
| 2.a | 0 | 0 | 0 |
| 2.b | 0 | 0 | 0 |
| 2.c | 28 | 28 | 0 |
| 2.e | 28 | 0 | 28 |
| **Chaine Sepoy** | **56** | **28** | **28** |

## 13. Total runtime global

- Avant HOTFIX-5C2E3C : 187 references invalides.
- Apres HOTFIX-5C2E3C : 159 references invalides.
- Diminution exacte : 28.

## 14. Zero ancien ID dans l'option 2.c

L'option 2.c ne contient plus aucun des cinq anciens IDs. Les sept groupes
migres contiennent chacun une paire south/north. L'option compte huit usages de
`region_south_india` au total car un huitieme usage preexistant appartient a
l'effet final de radicaux deja committe ; il n'a pas ete modifie. Elle contient
sept usages de `region_north_india`.

## 15. Repartition des 28 references restantes

Les 28 anciennes references restantes dans `sepoy_mutiny_events.2`
appartiennent uniquement a l'option 2.e.

## 16. Risques restants

- L'option 2.e conserve volontairement ses 28 filtres obsoletes jusqu'a
  HOTFIX-5C2E3D.
- South/North India couvrent des zones plus larges que les anciennes listes ;
  le comportement reste celui du hunk vanilla/hotfix, borne par les listes
  territoriales explicites de l'option.
- La branche Madras doit etre testee avec une mutinerie effectivement
  declenchee pour confirmer les transferts en jeu.

## 17. Tests en jeu recommandes

1. Charger une partie BIC et verifier l'absence d'erreur au demarrage.
2. Declencher `sepoy_mutiny_events.2` dans une sauvegarde de test.
3. Choisir l'option 2.c et confirmer que BIC conserve son noyau de Madras.
4. Verifier les independances et les reprises prioritaires explicites.
5. Controler les transferts aux princes voisins et les exceptions Himalaya,
   Pashtunistan et Quetta.
6. Confirmer que l'effet final de radicaux south India reste execute.
7. Surveiller `error.log`, `game.log` et `debug.log` pendant le breakup.

## 18. Fichiers modifies ou crees

- Modifie : `events/india_events/sepoy_mutiny_events.txt`.
- Cree :
  `docs/reports/hotfix/HOTFIX_5C2E3C_SEPOY_MADRAS_RETREAT.md`.

## 19. Confirmation du perimetre gameplay

Aucun autre gameplay n'a ete modifie. La journal entry Sepoy,
`sepoy_mutiny_events.4`, les progress bars, localisations, scripted effects,
BIC, Durrani, Indian Famines, India Railway, NAVY, ADMIN, MARATH et Travancore
sont restes inchanges.

## 20. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` n'a ete ni applique, ni
modifie, ni supprime.
