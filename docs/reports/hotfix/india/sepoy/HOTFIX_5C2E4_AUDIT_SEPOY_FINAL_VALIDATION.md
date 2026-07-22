# HOTFIX-5C2E4 - Audit final Uneasy Raj / Sepoy Mutiny

## 1. Resume executif

L'audit statique des commits HOTFIX-5C2E1 a HOTFIX-5C2E3D est conforme au
perimetre annonce. Les deux fichiers de la chaine Uneasy Raj / Sepoy Mutiny ne
contiennent plus aucun des cinq anciens IDs regionaux. Le diff cumule depuis
`0ebb18a` ne contient que les migrations regionales planifiees et la suppression
des cinq scopes inutilises.

Les listes de states, effets territoriaux, exceptions frontalieres, valeurs,
boucles, tags et ordre des effets sont preserves. Le seul point fonctionnel
suspect est le trigger `STATE_WEST_BENGAL` de l'option 2.e, probablement issu
d'un copier-coller vanilla. Il n'est pas modifie dans cette phase.

Conclusion statique : **migration regionale Sepoy validee, validation en jeu
requise avant toute correction fonctionnelle supplementaire**.

## 2. Etat Git

- Branche : `hotfix-dlc-audit`.
- Working tree initial : propre.
- HEAD initial : `eb15445 Fix Sepoy Bombay retreat regions`.
- Base avant corrections Sepoy : `0ebb18a`.
- Commits presents :
  - E1 `c273de7` ;
  - E2 `956c514` ;
  - E3A `1e0ae83` ;
  - E3B `b484200` ;
  - E3C `de4de55` ;
  - E3D `eb15445`.
- Stash present et intact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.
- Aucun commit cree pendant cet audit.

Note de validation finale : des fichiers non suivis sous
`docs/research/technology/` sont apparus apres la verification initiale propre.
Ils ne font pas partie de cet audit, n'ont pas ete crees ou modifies par cette
phase et ont ete laisses intacts. L'etat Git final contient donc ces ajouts
concurrents en plus des deux livrables HOTFIX-5C2E4.

## 3. Verification zero ancien ID

IDs recherches comme tokens complets, commentaires exclus :
`region_bengal`, `region_bombay`, `region_central_india`, `region_madras` et
`region_punjab`.

| Objet | Occurrences |
|---|---:|
| `je_uneasy_raj` | 0 |
| `je_sepoy_mutiny` | 0 |
| `sepoy_mutiny_events.2.a` | 0 |
| `sepoy_mutiny_events.2.b` | 0 |
| `sepoy_mutiny_events.2.c` | 0 |
| `sepoy_mutiny_events.2.e` | 0 |
| `sepoy_mutiny_events.4` | 0 |
| `common/journal_entries/04_sepoy_mutiny.txt` | 0 |
| `events/india_events/sepoy_mutiny_events.txt` | 0 |

## 4. Diff cumule E1-E3D

Le diff `0ebb18a..HEAD` porte uniquement sur deux fichiers :

| Fichier | Insertions | Suppressions | Nature |
|---|---:|---:|---|
| `common/journal_entries/04_sepoy_mutiny.txt` | incluses dans le total | incluses dans le total | Scopes inutilises et hidden trigger |
| `events/india_events/sepoy_mutiny_events.txt` | incluses dans le total | incluses dans le total | Filtres regionaux des events |
| **Total** | **65** | **154** | **Migrations attendues uniquement** |

La reduction de lignes vient du remplacement de listes de quatre ou cinq
anciennes regions par deux strategic regions valides.

## 5. Tableau des hunks par phase

| Fichier | Objet | Hunk | Phase | Ancienne logique | Nouvelle logique | Conforme ? |
|---|---|---|---|---|---|---|
| JE | `je_sepoy_mutiny` | Hidden trigger du diplomatic play | E1 | Cinq anciennes regions | North + South India | Oui |
| Events | Event 4 | Deux filtres nord | E1 | Bengal/Punjab/Central | North India, exceptions preservees | Oui |
| Events | Event 4 | Filtre sud | E1 | Bombay + Madras | South India | Oui |
| JE | `je_uneasy_raj.immediate` | Cinq scopes sauvegardes | E2 | Scopes jamais lus | Blocs supprimes | Oui |
| Events | Option 2.b | Radicaux Bengal | E2 | `region_bengal` | `region_north_india` | Oui |
| Events | Option 2.c | Radicaux Madras | E2 | `region_madras` | `region_south_india` | Oui |
| Events | Option 2.e | Radicaux Bombay | E2 | `region_bombay` | `region_south_india` | Oui |
| Events | Event 4 / SAT | Validation de capitale | E2 | Bombay ou Madras | `geographic_region_bombay_old` | Oui |
| Events | Option 2.a | Sept groupes regionaux | E3A | 35 anciennes references | Sept paires north/south | Oui |
| Events | Option 2.b | Sept groupes regionaux | E3B | 28 anciennes references | Sept paires north/south | Oui |
| Events | Option 2.c | Sept groupes regionaux | E3C | 28 anciennes references | Sept paires south/north | Oui |
| Events | Option 2.e | Sept groupes regionaux | E3D | 28 anciennes references | Ordres north/south vanilla | Oui |

Aucun autre type de hunk n'apparait dans le diff cumule.

## 6. Objets proteges

La comparaison avec `0ebb18a` confirme que les elements suivants sont
inchanges hors des hunks regionaux autorises :

- `possible = { always = no }` ;
- gardes date/technologie et ajout contextless toujours commentes ;
- trois progress bars et variables globales ;
- `sepoy_mutiny_timer_var` ;
- pulses hebdomadaire et mensuel ;
- valeurs numeriques et event weights ;
- cles de localisation appelees ;
- tags, war goals, lois et diplomatic plays ;
- `make_independent`, `set_state_owner` et ownership ;
- boucles `while`, limites et scopes sauvegardes ;
- listes de reprises prioritaires et states explicitement nommes ;
- ordre des effets.

Les seules modifications dans les effets de radicaux sont les trois filtres
regionaux E2. Les religions, valeurs et appels d'effet sont inchanges.

## 7. Exceptions frontalieres

Les nombres ci-dessous sont identiques avant et apres. Le nombre de feuilles
`capital.region` diminue volontairement, mais les quatre tests logiques de
capitale par option restent en place.

| Option | Element protege | Avant | Apres | Conforme ? |
|---|---|---:|---:|---|
| 2.a | `region_himalayas` | 3 | 3 | Oui |
| 2.a | `STATE_PASHTUNISTAN` | 7 | 7 | Oui |
| 2.a | `STATE_QUETTA` | 7 | 7 | Oui |
| 2.a | Tests de voisinage | 2 | 2 | Oui |
| 2.a | `is_subject_of` | 2 | 2 | Oui |
| 2.a | `make_independent` | 1 | 1 | Oui |
| 2.b | `region_himalayas` | 3 | 3 | Oui |
| 2.b | `STATE_PASHTUNISTAN` | 7 | 7 | Oui |
| 2.b | `STATE_QUETTA` | 7 | 7 | Oui |
| 2.b | Tests de voisinage | 2 | 2 | Oui |
| 2.b | `is_subject_of` | 1 | 1 | Oui |
| 2.b | `make_independent` | 1 | 1 | Oui |
| 2.c | `region_himalayas` | 3 | 3 | Oui |
| 2.c | `STATE_PASHTUNISTAN` | 7 | 7 | Oui |
| 2.c | `STATE_QUETTA` | 7 | 7 | Oui |
| 2.c | Tests de voisinage | 2 | 2 | Oui |
| 2.c | `is_subject_of` | 1 | 1 | Oui |
| 2.c | `make_independent` | 1 | 1 | Oui |
| 2.e | `region_himalayas` | 3 | 3 | Oui |
| 2.e | `STATE_PASHTUNISTAN` | 7 | 7 | Oui |
| 2.e | `STATE_QUETTA` | 7 | 7 | Oui |
| 2.e | Tests de voisinage | 2 | 2 | Oui |
| 2.e | `is_subject_of` | 1 | 1 | Oui |
| 2.e | `make_independent` | 1 | 1 | Oui |

Le multiensemble complet des IDs `STATE_*` de chaque option est strictement
identique a la base. Aucune difference bloquante n'est detectee.

## 8. Noyaux territoriaux des quatre options

| Option | Condition de repli | Noyau conserve | Reprises prioritaires | Zones redistribuees | Radicaux |
|---|---|---|---|---|---|
| 2.a | Aucune garde d'option ; option par defaut | Aucun noyau BIC durable ; reliquat repris par l'overlord | Liste generale complete | North/South, Himalaya, Pashtunistan, Quetta | Aucun effet final dedie |
| 2.b | BIC possede un scope state `STATE_WEST_BENGAL` | Bengal ; penalite IA sans East Bengal | Madras, Mandalay/Pegu, Gujarat, Tenasserim, Travancore, Circars/Kurnool, Delhi/Agra/Awadh, Central Provinces, Bombay | North/South plus exceptions | North India |
| 2.c | BIC possede un scope state `STATE_MADRAS` | Madras | Mandalay/Pegu, Gujarat, Tenasserim, Travancore, Delhi/Agra/Awadh, Central Provinces, Bombay | North/South plus exceptions | South India |
| 2.e | BIC possede un scope state `STATE_WEST_BENGAL` | Intention/localisation Bombay ; garde incoherente | Madras, Mandalay/Pegu, Tenasserim, Travancore, Circars/Kurnool, Delhi/Agra/Awadh, Central Provinces | North/South plus exceptions | South India |

Les sujets concernes sont filtres par capitale dans les zones north/south ou
les exceptions Pashtunistan/Quetta. Les receveurs doivent avoir un heritage
sud-asiatique et une capitale dans ces memes zones ; les states transferes
doivent etre voisins de leur receveur.

## 9. Audit detaille de STATE_WEST_BENGAL

### Constat

Le bloc de l'option 2.e contient :

```txt
trigger = {
    any_scope_state = {
        state_region = s:STATE_WEST_BENGAL
    }
}
```

Ce bloc est identique dans `0ebb18a`, le fork actuel, le hotfix et la vanilla
1.13.

### Reponses

1. **Accessibilite** : oui. Le bloc `trigger` controle si l'option 2.e est
   selectable.
2. **State selectionne** : non. Il ne teste pas un state choisi dans l'UI.
3. **Portee** : `any_scope_state` verifie l'existence d'au moins un state du
   scope country correspondant a West Bengal.
4. **Autre garde Bombay** : aucune vraie condition d'accessibilite Bombay
   n'existe ailleurs dans 2.e. `STATE_BOMBAY` n'apparait pas dans l'option.
5. **Localisation** : oui. La vanilla anglaise dit `Bombay holds! Direct all
   remaining forces to the West.` et le tooltip utilise
   `geographic_region_bombay_old`.
6. **Diagnostic** : copier-coller probable depuis l'option 2.b, et donc bug
   vanilla probable. La dependance est heritee par le hotfix et le fork.
7. **Test concret** : verifier 2.e avec West Bengal present/absent et Bombay
   present, puis avec Bombay absent et West Bengal present.
8. **Correction future candidate** : `STATE_BOMBAY` correspond le mieux au
   parallelisme avec 2.b/2.c. `geographic_region_bombay_old` serait une garde
   plus large et ne suit pas la structure actuelle des options.

Confiance : **HIGH** pour le diagnostic de copier-coller ; **MEDIUM** pour
l'application directe de `STATE_BOMBAY` avant validation en jeu.

## 10. Comparaison fork / hotfix / vanilla

| Option | Fork actuel | Hotfix | Vanilla | Identique regionalement ? | Differences non regionales |
|---|---|---|---|---|---|
| 2.a | Paires north/south + exceptions | Meme structure | Meme structure | Oui | Aucune difference regionale |
| 2.b | Paires north/south + noyau Bengal | Meme structure | Meme structure | Oui | Aucune difference regionale |
| 2.c | Paires south/north + noyau Madras | Meme structure | Meme structure | Oui | Aucune difference regionale |
| 2.e | Ordres north/south vanilla + West Bengal | Meme structure | Meme structure | Oui | Trigger West Bengal commun aux trois |
| Event 4 | North/South et Bombay old | KNO + Greater Persia | KNO + Greater Persia | Partiel, hunks cibles conformes | KNO absent ; `region_persia` legacy |

Le hotfix et la vanilla sont identiques pour les deux fichiers examines.

## 11. Differences non regionales non importees

La comparaison du fork actuel a la vanilla montre des ecarts hors perimetre :

- chaine desactivee par `possible = { always = no }` dans le fork ;
- anciennes API de pinning des journal entries dans le fork ;
- `kill_character` au lieu de `retire_character` dans l'event 1 ;
- branche KNO absente dans `sepoy_mutiny_events.4` ;
- `region_persia` au lieu de `region_greater_persia` dans deux gardes ;
- un `OR` redondant autour de `region_south_india` ;
- `has_role = general` au lieu de `has_role_of_type = general` dans l'event 10.

Ces differences ne sont pas des autorisations d'import automatique. Elles
doivent faire l'objet de phases separees.

## 12. Risques restants

- 2.e peut etre disponible ou indisponible sur une condition territoriale
  incoherente avec Bombay.
- La branche KNO manque toujours au fork.
- `region_persia` peut etre obsolete en 1.13.
- Les 131 anciens IDs restants sont hors chaine Sepoy et necessitent des audits
  dedies.
- La migration statique ne prouve pas que les boucles de redistribution
  terminent correctement dans tous les setups 1776.
- La chaine reste volontairement inactive organiquement, donc les tests exigent
  une sauvegarde preparee ou editee.

## 13. Matrice de tests

La matrice detaillee est fournie dans :
`docs/reports/hotfix/HOTFIX_5C2E4_SEPOY_TEST_MATRIX.csv`.

Elle couvre le chargement 1776, l'inactivite de la chaine, les hidden triggers,
les quatre options, West Bengal present/absent, les trois exceptions
frontalieres, les receveurs, la boucle et les radicaux north/south.

## 14. Protocole de validation en jeu

1. Creer une sauvegarde de base 1776 avec uniquement le mod actif.
2. Conserver une copie non modifiee pour confirmer que `je_uneasy_raj` reste
   inactive.
3. Dupliquer la sauvegarde une fois par ligne de la matrice.
4. Comme aucune commande console exacte n'est confirmee localement, utiliser
   `MANUAL_OR_SAVE_EDIT_REQUIRED` pour preparer les conditions.
5. Ne tester qu'une option par sauvegarde afin d'eviter la contamination.
6. Avant le choix, relever ownership, sujets, capitales, states BIC et
   accessibilite de l'option.
7. Apres le choix, relever les pays liberes, states transferes, receveurs et
   capitales.
8. Verifier les states conserves par BIC et les exceptions Himalaya,
   Pashtunistan et Quetta.
9. Relever les radicaux hindous et sunnites dans la zone attendue.
10. Pour les boucles, confirmer la fin de l'event et l'absence de state bloque.
11. Capturer l'ecran de choix, la carte avant/apres et les tooltips d'effets.
12. Sauvegarder `error.log`, `game.log` et `debug.log` apres chaque scenario.
13. Comparer les resultats a la ligne correspondante du CSV.
14. Classer comme echec toute erreur de scope, option inaccessible a tort,
    transfert hors zone, exception perdue ou boucle non terminee.

## 15. Commandes PowerShell pour les logs

Ne pas executer avant le test en jeu. Exemple reproductible :

```powershell
$LogRoot = "$env:USERPROFILE\Documents\Paradox Interactive\Victoria 3\logs"
$Patterns = @(
    'region_bengal', 'region_bombay', 'region_central_india',
    'region_madras', 'region_punjab', 'sepoy_mutiny_events.2',
    'sepoy_mutiny_events.4', 'je_uneasy_raj', 'je_sepoy_mutiny',
    'Invalid scope', 'Invalid right side', 'Invalid strategic region',
    'Script system error', 'PostValidate', 'while', 'random_scope_state',
    'set_state_owner', 'STATE_WEST_BENGAL', 'STATE_BOMBAY'
)

$Logs = @('error.log', 'game.log', 'debug.log') |
    ForEach-Object { Join-Path $LogRoot $_ } |
    Where-Object { Test-Path $_ }

Select-String -Path $Logs -Pattern $Patterns -SimpleMatch |
    Sort-Object Path, LineNumber
```

Pour isoler les anciens IDs :

```powershell
Select-String -Path $Logs -Pattern @(
    'region_bengal', 'region_bombay', 'region_central_india',
    'region_madras', 'region_punjab'
) -SimpleMatch
```

## 16. Total global restant : 131

Le recomptage dans `common/` et `events/`, commentaires exclus et IDs complets,
donne exactement **131** occurrences.

## 17. Repartition des 131 references

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

## 18. Criteres permettant de valider Sepoy

- Zero ancien ID dans les deux fichiers et dans les logs des tests.
- Aucun `Invalid scope`, `Invalid right side`, `PostValidate` ou erreur de
  strategic region lie a la chaine.
- Hidden trigger valide pour des cibles north et south India.
- Options 2.a, 2.b et 2.c disponibles dans leurs conditions attendues.
- Resultats territoriaux conformes aux listes explicites.
- Exceptions Himalaya, Pashtunistan et Quetta preservees.
- Boucles terminees avec receveur unique, multiple ou absent.
- Radicaux appliques a north pour 2.b et south pour 2.c/2.e.
- Comportement de 2.e documente sans ambiguite par les deux tests West Bengal.

## 19. Criteres imposant une correction supplementaire

- 2.e indisponible avec Bombay present et West Bengal absent, ou disponible
  uniquement grace a West Bengal : ouvrir une phase dediee au trigger.
- State transfere hors des zones et exceptions attendues.
- BIC perd son noyau Bengal/Madras/Bombay contrairement au choix.
- Sujet ou receveur invalide, capitale incoherente ou boucle non terminee.
- Erreur de scope/API dans les logs.
- `region_persia`, branche KNO ou API de role provoquant une erreur runtime :
  ouvrir une phase separee, sans les melanger au fix Sepoy regional.

## 20. Fichiers crees

- `docs/reports/hotfix/HOTFIX_5C2E4_AUDIT_SEPOY_FINAL_VALIDATION.md`.
- `docs/reports/hotfix/HOTFIX_5C2E4_SEPOY_TEST_MATRIX.csv`.

## 21. Confirmation gameplay

Aucun fichier gameplay n'a ete modifie. Aucun trigger, state, event, journal
entry, effet ou localisation n'a ete corrige pendant cet audit.

## 22. Inactivite organique en 1776

La chaine reste inactive organiquement : `je_uneasy_raj` conserve
`possible = { always = no }`. Les anciennes gardes date/technologie restent
commentees et aucune activation contextless n'a ete restauree.

## 23. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste intact. Il n'a ete ni
applique, ni inspecte comme contenu courant, ni supprime.
