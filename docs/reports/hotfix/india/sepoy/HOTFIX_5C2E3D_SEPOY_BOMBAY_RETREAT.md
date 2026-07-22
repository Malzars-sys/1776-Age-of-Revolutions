# HOTFIX-5C2E3D - Sepoy Mutiny Bombay retreat

## 1. Resume

Cette phase migre uniquement les sept filtres regionaux de l'option
`sepoy_mutiny_events.2.e`. Les 28 dernieres references invalides de la chaine
Sepoy ont ete remplacees par les paires north/south attestees dans le hotfix et
la vanilla 1.13.

La chaine Sepoy contient desormais zero ancien ID. Les listes territoriales,
les effets et les autres options sont inchanges.

## 2. Etat Git initial

- Branche : `hotfix-dlc-audit`.
- Working tree : propre avant modification.
- HEAD initial : `de4de55 Fix Sepoy Madras retreat regions`.
- HOTFIX-5C2E3C etait committe avant cette phase.
- Stash preserve :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.
- Aucun commit n'a ete cree pendant cette phase.

## 3. Comptage initial

| Option | References initiales |
|---|---:|
| 2.a | 0 |
| 2.b | 0 |
| 2.c | 0 |
| 2.e | 28 |
| Chaine Sepoy | 28 |

Le total runtime global initial etait de 159.

## 4. Comparaison fork, hotfix et vanilla

L'option 2.e a ete comparee entre le fork, le hotfix upstream et
`C:/Games/Victoria 3 The Great Wave/game/events/india_events/sepoy_mutiny_events.txt`.

Hotfix et vanilla sont alignes, mais l'ordre north/south varie selon le groupe :

- groupes 1 et 2 : capital north, puis south ;
- groupes 3 et 4 : state south, puis north ;
- groupes 5 et 6 : capital south, puis north ;
- groupe 7 : state north, puis south.

Ces ordres exacts ont ete reproduits. Aucun event complet n'a ete copie.

## 5. Inventaire des sept groupes de l'option 2.e

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
| 1 | Bengal, Madras, Punjab, Central India | North + South India | 4 |
| 2 | Bengal, Madras, Punjab, Central India | North + South India | 4 |
| 3 | Punjab, Central India, Bombay, Bengal | South + North India | 4 |
| 4 | Punjab, Central India, Madras, Bengal | South + North India | 4 |
| 5 | Madras, Bengal, Punjab, Central India | South + North India | 4 |
| 6 | Madras, Bengal, Punjab, Central India | South + North India | 4 |
| 7 | Punjab, Central India, Madras, Bengal | North + South India | 4 |
| **Total** | **28** | **14 references valides** | **28** |

## 7. Noyau de Bombay conserve

Aucune condition, exclusion ou liste explicite supposee definir le repli n'a
ete modifiee. La structure hotfix/vanilla de l'option 2.e contient toutefois un
trigger explicite sur `STATE_WEST_BENGAL`, et non sur `STATE_BOMBAY`.

Ce point a volontairement ete laisse intact conformement au perimetre ferme. Il
doit etre verifie en jeu ou dans une phase fonctionnelle distincte avant de
conclure que le repli Bombay se comporte comme son intention/localisation.

## 8. Exceptions frontalieres preservees

- `region_himalayas` : 3 occurrences conservees dans 2.e ;
- `STATE_PASHTUNISTAN` : 7 occurrences conservees ;
- `STATE_QUETTA` : 7 occurrences conservees ;
- tests de capitale, voisinage, ownership, sujet et independance inchanges.

## 9. Listes de states et effets territoriaux preserves

Les states explicitement presents restent inchanges, notamment West Bengal,
Madras, Mandalay, Pegu, Tenasserim, Travancore, Circars, Kurnool, Hyderabad,
Delhi, Agra, Awadh et Central Provinces. Aucun state n'a ete ajoute, supprime ou
reordonne.

Les tags receveurs, `make_independent`, `set_state_owner`, transferts, boucles,
limites numeriques, scopes sauvegardes et ordre des effets sont inchanges.
L'effet final de radicaux corrige par HOTFIX-5C2E2 est identique a HEAD.

## 10. Options 2.a, 2.b et 2.c

Les blocs extraits des options 2.a, 2.b et 2.c sont strictement identiques a
HEAD. Les corrections E3A, E3B et E3C restent donc intactes.

## 11. Tableau des 28 references retirees

| Identifiant | Avant dans 2.e | Apres dans 2.e | Retirees |
|---|---:|---:|---:|
| `region_bengal` | 7 | 0 | 7 |
| `region_bombay` | 1 | 0 | 1 |
| `region_central_india` | 7 | 0 | 7 |
| `region_madras` | 6 | 0 | 6 |
| `region_punjab` | 7 | 0 | 7 |
| **Total** | **28** | **0** | **28** |

## 12. Comptage de la chaine Sepoy

| Objet | Avant | Retirees | Apres |
|---|---:|---:|---:|
| Option 2.a | 0 | 0 | 0 |
| Option 2.b | 0 | 0 | 0 |
| Option 2.c | 0 | 0 | 0 |
| Option 2.e | 28 | 28 | 0 |
| **Chaine Sepoy** | **28** | **28** | **0** |

## 13. Total runtime global

- Avant HOTFIX-5C2E3D : 159 references invalides.
- Apres HOTFIX-5C2E3D : 131 references invalides.
- Diminution exacte : 28.

## 14. Zero ancien ID dans la chaine Sepoy

Le comptage des cinq anciens IDs donne zero dans :

- `common/journal_entries/04_sepoy_mutiny.txt` ;
- `events/india_events/sepoy_mutiny_events.txt` ;
- les options 2.a, 2.b, 2.c et 2.e ;
- `sepoy_mutiny_events.4` ;
- les journal entries `je_uneasy_raj` et `je_sepoy_mutiny`.

L'option 2.e contient sept usages de `region_north_india` et huit usages de
`region_south_india`. Le huitieme south est l'effet final de radicaux deja
present dans HEAD et non modifie par cette phase.

## 15. Repartition des 131 references globales restantes

| Fichier | Occurrences |
|---|---:|
| `common/ai_strategies/00_default_strategy.txt` | 43 |
| `common/scripted_buttons/00_new_colonial_admins.txt` | 40 |
| `common/history/military_formations/05_military_formations_india.txt` | 23 |
| `common/dynamic_country_names/00_dynamic_country_names.txt` | 10 |
| `common/journal_entries/07_hindustan_is_durrani_mod.txt` | 6 |
| `common/character_templates/country_bic.txt` | 2 |
| `common/history/interests/00_interests.txt` | 2 |
| `common/history/military_formations/04_military_formations_middle_east.txt` | 2 |
| `common/journal_entries/00_player_objectives_great_game.txt` | 2 |
| `common/history/military_formations/00_military_formations_europe.txt` | 1 |
| **Total** | **131** |

Ces references appartiennent a des domaines hors de la chaine Sepoy et ne sont
pas modifiees ici.

## 16. Risques restants

- Le trigger `STATE_WEST_BENGAL` de l'option 2.e doit etre valide par rapport a
  l'intention de retraite Bombay ; il est identique dans le hotfix et la
  vanilla, mais reste surprenant.
- Les paires north/south sont plus larges que les anciennes listes ; leur
  comportement est celui de la reference vanilla, avec les exceptions
  explicites preservees.
- Les 131 references globales restantes necessitent des audits separes par
  domaine et ne doivent pas etre remplacees globalement.

## 17. Plan de validation en jeu des quatre options

1. Preparer une sauvegarde de test permettant de declencher
   `sepoy_mutiny_events.2` de facon reproductible.
2. Tester 2.a et relever independances, receveurs et states transferes.
3. Tester 2.b et verifier le repli bengali ainsi que les listes prioritaires.
4. Tester 2.c et verifier le repli Madras et les listes prioritaires.
5. Tester 2.e et verifier explicitement si le trigger West Bengal correspond
   au comportement attendu pour Bombay.
6. Comparer les quatre resultats aux hunks vanilla/hotfix sans modifier la
   chronologie 1776 pendant cette validation.

## 18. Tests en jeu recommandes

Aucun test en jeu n'a ete realise pendant cette phase, conformement aux
instructions. Pour la validation future :

- charger BIC sans erreur ;
- declencher chaque option sur une sauvegarde separee ;
- verifier les exceptions Himalaya, Pashtunistan et Quetta ;
- verifier les sujets liberes, receveurs, capitales et transferts ;
- surveiller `error.log`, `game.log` et `debug.log` ;
- rechercher les cinq anciens IDs dans les nouvelles erreurs de log.

## 19. Fichiers modifies ou crees

- Modifie : `events/india_events/sepoy_mutiny_events.txt`.
- Cree :
  `docs/reports/hotfix/HOTFIX_5C2E3D_SEPOY_BOMBAY_RETREAT.md`.

## 20. Confirmation du perimetre gameplay

Aucun autre gameplay n'a ete modifie. La journal entry Sepoy,
`sepoy_mutiny_events.4`, les progress bars, localisations, scripted effects,
BIC, Durrani, Indian Famines, India Railway, NAVY, ADMIN, MARATH et Travancore
sont restes inchanges.

## 21. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` n'a ete ni applique, ni
modifie, ni supprime.
