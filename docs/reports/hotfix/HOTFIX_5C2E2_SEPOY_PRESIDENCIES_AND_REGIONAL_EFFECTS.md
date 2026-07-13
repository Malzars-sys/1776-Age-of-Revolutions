# HOTFIX-5C2E2 - Sepoy presidencies and regional effects

## 1. Resume

Cette phase retire exactement dix references aux anciennes strategic regions indiennes : cinq scopes inutilises de `je_uneasy_raj.immediate`, trois filtres regionaux d'effets de radicals dans `sepoy_mutiny_events.2`, et deux references du controle SAT dans `sepoy_mutiny_events.4`.

Apres correction, les 119 anciennes references restantes appartiennent toutes aux selections territoriales de `sepoy_mutiny_events.2` reservees a HOTFIX-5C2E3.

## 2. Etat Git initial

- branche : `hotfix-dlc-audit` ;
- working tree initial : propre ;
- HEAD initial : `c273de7 Fix Sepoy hidden trigger and alignments` ;
- HOTFIX-5C2E1 present et commite ;
- stash MARATH present : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- aucun stash applique ou modifie ;
- aucun commit cree automatiquement.

## 3. Comptage initial

Le comptage recherche les cinq tokens exacts et exclut les commentaires.

| Fichier | References avant E2 |
|---|---:|
| `common/journal_entries/04_sepoy_mutiny.txt` | 5 |
| `events/india_events/sepoy_mutiny_events.txt` | 124 |
| **Total chaine** | **129** |

Le total runtime global avant E2 etait de 260.

## 4. Comparaison fork / hotfix / vanilla

Les deux fichiers hotfix sont identiques a leurs homologues vanilla 1.13. Les hunks ont ete compares individuellement ; aucun fichier entier n'a ete copie.

| Bloc | Fork avant | Hotfix / vanilla | Decision appliquee |
|---|---|---|---|
| `je_uneasy_raj.immediate` | cinq scopes d'anciennes regions | cinq blocs absents | supprimer les blocs complets |
| radicals Bengal | `region_bengal` | `region_north_india` | reprendre north India |
| radicals Madras | `region_madras` | `region_south_india` | reprendre south India |
| radicals Bombay | `region_bombay` | `region_south_india` | reprendre south India |
| SAT option A | Bombay OR Madras anciennes | `geographic_region_bombay_old` | reprendre le predicat state-scope |
| branche KNO/Madras | absente | presente | ne pas importer |

## 5. Recherche de lecteurs des cinq scopes

Une recherche exacte a ete effectuee dans tout le fork pour :

- `bengal_sr_scope` ;
- `bombay_sr_scope` ;
- `madras_sr_scope` ;
- `punjab_sr_scope` ;
- `central_india_sr_scope`.

Avant suppression, chaque nom avait trois occurrences dans le depot :

1. sa propre definition `save_scope_as` dans la journal entry ;
2. une mention dans le rapport d'audit E ;
3. une mention dans le rapport E1.

Aucun `scope:<nom>`, lecteur, trigger ou effet gameplay ne les utilisait. Apres suppression, les cinq noms ont zero occurrence dans `common/` et `events/`. Les mentions documentaires historiques restent naturellement dans les rapports deja commites.

## 6. Suppression des cinq scopes obsoletes

Les cinq blocs suivants ont ete supprimes integralement de `je_uneasy_raj.immediate` :

- scope de `region_bengal` sauvegarde comme `bengal_sr_scope` ;
- scope de `region_bombay` sauvegarde comme `bombay_sr_scope` ;
- scope de `region_madras` sauvegarde comme `madras_sr_scope` ;
- scope de `region_punjab` sauvegarde comme `punjab_sr_scope` ;
- scope de `region_central_india` sauvegarde comme `central_india_sr_scope`.

Les blocs complets ont ete retires, conformement au hotfix et a la vanilla, et pas seulement leurs lignes regionales.

L'ordre des effets restants est conserve : `raj_scope`, les trois variables globales de progression, puis `sepoy_mutiny_timer_var`.

## 7. Correction des radicals Bengal

Dans l'effet final de l'option `sepoy_mutiny_events.2.b`, le filtre state-scope devient :

```txt
region = sr:region_north_india
```

Les deux appels `add_radicals_in_state`, leurs religions et la valeur `large_radicals` sont inchanges.

## 8. Correction des radicals Madras

Dans l'effet final de l'option `sepoy_mutiny_events.2.c`, le filtre state-scope devient :

```txt
region = sr:region_south_india
```

L'iterator, les religions et les valeurs sont inchanges.

## 9. Correction des radicals Bombay

Dans l'effet final de l'option `sepoy_mutiny_events.2.e`, le filtre state-scope devient :

```txt
region = sr:region_south_india
```

Tous les effets voisins sont inchanges.

## 10. Correction de l'alignement SAT

Dans l'option A de `sepoy_mutiny_events.4`, le controle de la capitale pour rejoindre le play SAT remplace le groupe Bombay/Madras par le predicat vanilla :

```txt
capital = {
	is_in_geographic_region = geographic_region_bombay_old
}
```

Le tag SAT, le `dp_sepoy_mutiny`, les war goals, la condition culturelle marathi et les effets restent inchanges.

## 11. Non-importation de KNO

La branche KNO/Madras de la vanilla et du hotfix utilise `geographic_region_madras_old`, mais elle est absente du fork. Elle n'a pas ete ajoutee car elle ne remplace aucune des dix references ciblees et constituerait un changement fonctionnel supplementaire.

Le diff ne contient aucune nouvelle occurrence de `KNO`. Une eventuelle integration devra etre decidee dans une phase separee apres test du setup 1776.

## 12. Tableau des dix references retirees

| Objet | References retirees | Cible ou action |
|---|---:|---|
| cinq scopes `je_uneasy_raj.immediate` | 5 | suppression des blocs inutilises |
| radicals Bengal, option 2.b | 1 | `region_north_india` |
| radicals Madras, option 2.c | 1 | `region_south_india` |
| radicals Bombay, option 2.e | 1 | `region_south_india` |
| alignement SAT, event 4 option A | 2 | `geographic_region_bombay_old` |
| **Total** | **10** | |

## 13. Comptage de la chaine avant / apres

| Fichier | Avant | Apres | Reduction |
|---|---:|---:|---:|
| JE Sepoy | 5 | 0 | 5 |
| Events Sepoy | 124 | 119 | 5 |
| **Chaine totale** | **129** | **119** | **10** |

La JE ne contient plus aucun des cinq anciens IDs. L'event 4 n'en contient plus non plus.

## 14. Total global avant / apres

Le recomptage dans `common/` et `events/`, commentaires exclus, donne :

- avant : 260 ;
- apres : 250 ;
- reduction : 10.

Le total attendu est atteint sans modifier d'autres references.

## 15. Progress bars inchangees

Les trois declarations restent presentes :

- `sepoy_mutiny_progress_bar_bengal` ;
- `sepoy_mutiny_progress_bar_bombay` ;
- `sepoy_mutiny_progress_bar_madras`.

Les variables globales `bengal_presidency_stability`, `bombay_presidency_stability` et `madras_presidency_stability` restent presentes et dans le meme ordre. Le timer `sepoy_mutiny_timer_var`, les pulses et toutes les valeurs de progression sont inchanges.

## 16. Chaine inactive organiquement en 1776

Cette phase ne modifie pas :

- `possible = { always = no }` ;
- les gardes date/technologie commentees ;
- l'ajout contextless commente ;
- les conditions, pulses, dates, technologies, lois ou variables d'activation.

La chaine Uneasy Raj / Sepoy Mutiny reste donc inactive organiquement en 1776.

## 17. Les 119 references territoriales sont inchangees

Le recomptage isole de `sepoy_mutiny_events.2` donne 119 anciennes references apres retrait des trois lignes de radicals. Le diff de cet objet ne contient que ces trois remplacements autorises.

Les blocs suivants sont inchanges :

- detection et liberation de sujets ;
- gardes de breakup ;
- propagation par voisinage ;
- validation de capitales ;
- selection des pays receveurs ;
- transfert et ownership des states ;
- reprises prioritaires et listes explicites ;
- `region_himalayas`, `STATE_PASHTUNISTAN` et `STATE_QUETTA` ;
- tags recrees, war goals, lois et modifiers non regionaux.

Ces 119 references sont reservees a HOTFIX-5C2E3.

## 18. Risques restants

- Les 119 selections territoriales restent invalides jusqu'a E3.
- L'effet des filtres north/south sur les radicals doit etre teste sur le setup 1776.
- `geographic_region_bombay_old` inclut Bombay, Gujarat, Sindh et Baluchistan ; l'alignement SAT doit etre verifie en jeu.
- KNO ne participe toujours pas par la branche vanilla Madras, decision volontaire de cette phase.
- La chaine ne peut pas etre testee organiquement tant qu'elle reste desactivee en 1776.

## 19. Tests en jeu recommandes

1. Charger le mod et verifier l'absence d'erreurs de parsing dans la JE et les events Sepoy.
2. Confirmer que `je_uneasy_raj` ne s'active pas spontanement en 1776.
3. Forcer une sauvegarde de test avec la chaine active et verifier les trois progress bars.
4. Tester les options de retraite Bengal, Madras et Bombay et relever les states recevant des radicals.
5. Forcer l'event 4 avec une capitale dans `geographic_region_bombay_old` et verifier l'alignement SAT.
6. Verifier qu'aucune branche KNO n'apparait.
7. Rechercher les cinq anciens IDs dans `error.log`.
8. Confirmer le total global de 250 avant E3.

## 20. Fichiers modifies / cree

Fichiers gameplay modifies :

- `common/journal_entries/04_sepoy_mutiny.txt` ;
- `events/india_events/sepoy_mutiny_events.txt`.

Rapport cree :

- `docs/reports/hotfix/HOTFIX_5C2E2_SEPOY_PRESIDENCIES_AND_REGIONAL_EFFECTS.md`.

## 21. Aucun autre gameplay modifie

Aucun autre fichier n'a ete modifie ou cree. Sont notamment inchanges : BIC, `law_frontier_colonization`, technologies, batiments, formations, localisations, progress bars, scripted effects, scripted buttons, Indian Famines, India Railway, Durrani, NAVY, ADMIN, MARATH et Travancore.

Les trois corrections HOTFIX-5C2E1 restent presentes : hidden trigger north/south, alignements MUG north India et poids SAT south India.

## 22. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present et intact. Aucun `git stash pop`, apply, drop ou restore n'a ete execute.
