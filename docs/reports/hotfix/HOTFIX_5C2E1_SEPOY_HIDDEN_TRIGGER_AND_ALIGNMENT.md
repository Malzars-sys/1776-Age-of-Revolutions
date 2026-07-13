# HOTFIX-5C2E1 - Sepoy hidden trigger and alignment

## 1. Resume

Cette phase retire exactement 13 references aux anciennes strategic regions indiennes dans quatre blocs fermes de la chaine Uneasy Raj / Sepoy Mutiny. Le hidden trigger de `je_sepoy_mutiny` utilise maintenant les deux strategic regions vanilla 1.13. Trois controles d'alignement de `sepoy_mutiny_events.4` utilisent respectivement north India, north India et south India.

Aucun autre bloc de gameplay n'a ete modifie. La chaine conserve son verrou organique en 1776.

## 2. Etat Git initial

- branche : `hotfix-dlc-audit` ;
- working tree initial : propre ;
- HEAD initial : `0ebb18a Audit Sepoy Mutiny region migration` ;
- audit HOTFIX-5C2E present ;
- stash MARATH present : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- aucun stash applique ou modifie ;
- aucun commit cree automatiquement.

## 3. Comptage initial

Le comptage porte sur les tokens exacts et exclut les commentaires.

| Fichier | Anciennes references |
|---|---:|
| `common/journal_entries/04_sepoy_mutiny.txt` | 10 |
| `events/india_events/sepoy_mutiny_events.txt` | 132 |
| **Total chaine** | **142** |

Le total runtime global etait de 273.

## 4. Comparaison fork / hotfix / vanilla

Les fichiers hotfix et vanilla 1.13 sont identiques par hash SHA-256 pour la journal entry et les events Sepoy. Les quatre hunks autorises ont ete compares separement.

| Bloc | Fork avant | Hotfix / vanilla | Decision locale |
|---|---|---|---|
| hidden trigger JE | cinq anciennes regions | north + south India | reprendre north + south uniquement |
| event 4 option A, MUG | Bengal + Punjab + Central India | north India | reprendre north India uniquement |
| event 4 option B, poids MUG | Bengal + Punjab + Central India | north India | reprendre north India uniquement |
| event 4 option C, poids SAT | Bombay + Madras | south India | reprendre south India uniquement |

Les differences voisines du hotfix n'ont pas ete importees. En particulier, `region_persia` reste inchange et aucune branche KNO/Madras n'a ete ajoutee.

## 5. Correction du hidden trigger

Dans `je_sepoy_mutiny.fail.hidden_trigger`, l'OR controlant la capitale de la cible du `dp_sepoy_mutiny` contenait les cinq anciens IDs. Son contenu regional devient :

```txt
OR = {
	region = sr:region_north_india
	region = sr:region_south_india
}
```

Le diplomatic play, les scopes `target` et `capital`, le `NOT` englobant et le reste de `fail` sont inchanges.

## 6. Correction du controle MUG option A

Dans `sepoy_mutiny_events.4`, option A, la condition de participation au play MUG remplace :

- `region_bengal` ;
- `region_punjab` ;
- `region_central_india` ;

par une seule condition :

```txt
region = sr:region_north_india
```

`region_himalayas`, `region_persia`, le tag MUG, les war goals et les effets restent inchanges.

## 7. Correction du poids MUG option B

Le premier modifier de `ai_chance` de l'option B remplace les trois memes anciennes regions par :

```txt
region = sr:region_north_india
```

La base `20`, le bonus `20`, les conditions de religion, `region_himalayas` et `region_persia` sont inchanges.

## 8. Correction du poids SAT option C

Le premier modifier de `ai_chance` de l'option C remplace `region_bombay` et `region_madras` par :

```txt
region = sr:region_south_india
```

La structure englobante, la base, le bonus, la culture marathi et la religion hindoue sont inchanges.

## 9. Tableau des treize references retirees

| Objet | Bloc | References retirees | Cible ajoutee |
|---|---|---:|---|
| `je_sepoy_mutiny` | `fail.hidden_trigger` | 5 | north + south India |
| `sepoy_mutiny_events.4` | option A, controle MUG | 3 | north India |
| `sepoy_mutiny_events.4` | option B, poids IA MUG | 3 | north India |
| `sepoy_mutiny_events.4` | option C, poids IA SAT | 2 | south India |
| **Total** | | **13** | **5 lignes valides** |

Le diff contient exactement 13 lignes d'anciens IDs retirees et cinq lignes north/south ajoutees.

## 10. Comptage de la chaine avant / apres

| Fichier | Avant | Apres | Reduction |
|---|---:|---:|---:|
| JE Sepoy | 10 | 5 | 5 |
| Events Sepoy | 132 | 124 | 8 |
| **Chaine totale** | **142** | **129** | **13** |

Les cinq references restantes dans la JE appartiennent toutes aux scopes de `je_uneasy_raj.immediate` reserves a E2.

Les 124 references restantes dans les events se decomposent comme prevu :

- 2 dans le controle SAT option A reserve a E2 ;
- 3 dans les effets de radicals de l'event 2 reserves a E2 ;
- 119 dans les selections territoriales de l'event 2 reservees a E3.

## 11. Total global avant / apres

Le recomptage exact dans `common/` et `events/`, commentaires exclus, donne :

- avant : 273 ;
- apres : 260 ;
- reduction : 13.

Le total global attendu est atteint sans modifier d'autre reference.

## 12. `je_uneasy_raj.immediate` inchange

Une comparaison avec HEAD confirme que l'objet `je_uneasy_raj` est strictement inchange. Les cinq scopes suivants restent presents :

- `bengal_sr_scope` ;
- `bombay_sr_scope` ;
- `madras_sr_scope` ;
- `punjab_sr_scope` ;
- `central_india_sr_scope`.

Les progress bars, variables, pulses, conditions et poids d'events sont inchanges.

## 13. SAT option A inchange

Le bloc SAT historique de l'option A conserve exactement :

```txt
region = sr:region_bombay
region = sr:region_madras
```

Ce bloc reste reserve a HOTFIX-5C2E2. Son fragment a ete compare a HEAD et est identique.

## 14. Aucune branche KNO ajoutee

Le diff ne contient aucune occurrence de `KNO`. La branche KNO/Madras du hotfix et de la vanilla n'a pas ete importee.

## 15. `sepoy_mutiny_events.2` inchange

L'objet complet `sepoy_mutiny_events.2` a ete compare a HEAD et est strictement identique. Aucune option 2.a, 2.b, 2.c ou 2.e, selection territoriale, liberation de sujet, propagation, reprise prioritaire, capitale, transfert ou ligne de radicals n'a ete modifiee.

`region_himalayas`, `STATE_PASHTUNISTAN`, `STATE_QUETTA` et toutes les listes de states explicites restent inchanges.

## 16. Chaine inactive organiquement en 1776

Cette phase ne modifie pas :

- `possible = { always = no }` de `je_uneasy_raj` ;
- les anciennes gardes date/technologie commentees ;
- l'ajout contextless commente ;
- les dates, technologies, lois ou variables d'activation.

La chaine ne devient donc pas accessible organiquement en 1776 a cause de HOTFIX-5C2E1.

## 17. Risques restants

- Les cinq scopes obsoletes de `je_uneasy_raj.immediate` restent a traiter en E2.
- Le controle SAT historique conserve deux anciennes references jusqu'a E2.
- Les trois effets de radicals de l'event 2 restent a traiter en E2.
- Les 119 selections territoriales de l'event 2 restent a traiter en E3.
- `region_persia` n'a pas ete aligne sur `region_greater_persia`, conformement au perimetre ; ce point est independant des 13 references corrigees.
- Le comportement des alignements ne peut etre observe organiquement tant que la chaine 1776 reste desactivee.

## 18. Tests en jeu recommandes

1. Lancer le mod et confirmer l'absence de nouvelles erreurs de parsing dans les deux fichiers.
2. Rechercher les cinq anciens IDs dans `error.log` apres chargement.
3. Confirmer que `je_uneasy_raj` ne s'active pas spontanement en 1776.
4. Sur une sauvegarde de test, forcer `je_sepoy_mutiny` et verifier que le hidden trigger reconnait les capitales north et south India.
5. Forcer l'event 4 et verifier l'alignement MUG depuis north India.
6. Verifier les poids IA des options B et C sans changement numerique.
7. Recompter 260 references globales avant E2.

## 19. Fichiers modifies / cree

Fichiers gameplay modifies :

- `common/journal_entries/04_sepoy_mutiny.txt` ;
- `events/india_events/sepoy_mutiny_events.txt`.

Rapport cree :

- `docs/reports/hotfix/HOTFIX_5C2E1_SEPOY_HIDDEN_TRIGGER_AND_ALIGNMENT.md`.

## 20. Aucun autre gameplay modifie

Aucun autre fichier n'a ete modifie ou cree. Sont notamment inchanges : BIC, `law_frontier_colonization`, technologies, batiments, formations, localisations, progress bars, scripted effects, scripted buttons, Indian Famines, India Railway, Durrani, NAVY, ADMIN, MARATH et Travancore.

## 21. Stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste present et intact. Aucun `git stash pop`, apply, drop ou restore n'a ete execute.
