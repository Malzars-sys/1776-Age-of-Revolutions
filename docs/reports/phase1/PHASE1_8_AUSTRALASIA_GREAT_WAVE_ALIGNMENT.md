# Phase 1.8 / 1.8B - Australasie / The Great Wave 1.13

## 1. Resume des corrections

Correction limitee a l'Australie, a la Nouvelle-Zelande et aux states du fichier `map_data/state_regions/13_australasia.txt`.

Corrections appliquees :
- alignement des `naval_exit_id` divergents identifies en Phase 1.4 ;
- correction de la liste `impassable` de `STATE_SOUTH_AUSTRALIA` ;
- nettoyage des doublons dans l'ownership historique de `STATE_SOUTH_AUSTRALIA` ;
- comparaison avec la vraie vanilla locale `C:\Games\Victoria 3 The Great Wave\game` ;
- remplacement de la repartition trop large `WTI` par les nations decentralisees vanilla 1.13 ;
- retrait des proprietaires, pops et buildings coloniaux britanniques (`NSW`, `SAS`, `WAS`, `TAS`) pour rester coherent avec 1776.

Aucun sujet britannique n'a ete ajoute en Australie.

## 2. Comparaison vanilla 1.13 / mod

La vraie vanilla locale The Great Wave a ete trouvee ici :
- `C:\Games\Victoria 3 The Great Wave\game`

La vanilla 1.13 introduit une repartition plus fine de l'Australie avec des tags decentralises comme :
- `KLN`, `KNC`, `WDJ`, `KRI`, `YUR`, `PAA`
- `KAU`, `KTU`, `KYN`, `NYP`, `WRR`
- `GRW`, `ARH`, `YGU`, `LRR`, `ARR`, `MRA`, `WKB`, `PMA`

La vanilla contient aussi des colonies britanniques (`NSW`, `SAS`, `WAS`, `TAS`), mais elles n'ont pas ete conservees car le depart du mod est en 1776.

## 3. Pays decentralises australiens avant/apres

Avant correction :
- `STATE_NEW_SOUTH_WALES` : `WTI`.
- `STATE_VICTORIA` : `WTI`.
- `STATE_TASMANIA` : `WTI`.
- `STATE_QUEENSLAND` : `WTI`.
- `STATE_SOUTH_AUSTRALIA` : `WTI`.
- `STATE_WESTERN_AUSTRALIA` : `NNG`, `WTI`, `MRN`.
- `STATE_NORTHERN_TERRITORY` : `WTI`.

Apres correction :
- `STATE_NEW_SOUTH_WALES` : `WDJ`, `KLN`, `KRI`, `KNC`, `YUR`, `PAA`.
- `STATE_VICTORIA` : `KLN`, `KRI`.
- `STATE_TASMANIA` : `WTI` temporaire, faute de tag tasmanien decentralise clair dans la vanilla consultee.
- `STATE_QUEENSLAND` : `WKB`, `ARR`, `KNC`, `PMA`, `MRA`, `GRW`, `PAA`, `WDJ`.
- `STATE_SOUTH_AUSTRALIA` : `KAU`, `MRN`, `WTI`, `KNC`, `YUR`, `PAA`, `KLN`.
- `STATE_WESTERN_AUSTRALIA` : `NNG`, `MRN`, `WTI`, `KTU`, `KYN`, `NYP`, `WRR`.
- `STATE_NORTHERN_TERRITORY` : `LRR`, `KNC`, `WTI`, `NYP`, `GRW`, `ARH`, `YGU`, `WRR`, `ARR`.

Les anciennes parts vanilla coloniales ont ete reintegrees dans les tags decentralises les plus conservateurs :
- `NSW` -> `WDJ`, `KLN`, `WKB`, `LRR` ou `UNT` selon le state ;
- `SAS` -> `KAU` ;
- `WAS` -> `NNG` ;
- `TAS` -> `WTI`.

## 4. Nouvelle-Zelande avant/apres

Avant correction :
- `STATE_NORTH_ISLAND` : `UNT`, `NTO`, avec une part vanilla `NSW` apres comparaison 1.13.
- `STATE_SOUTH_ISLAND` : `NTO`, `NTU`, avec un claim vanilla `NSW`.

Apres correction :
- `STATE_NORTH_ISLAND` : `UNT`, `NTO`; la part `NSW` est attribuee a `UNT`.
- `STATE_SOUTH_ISLAND` : `NTO`, `NTU`; le claim `NSW` est retire.
- Aucun sujet britannique n'est ajoute en Nouvelle-Zelande.

## 5. Provinces/states modifies

States modifies :
- `STATE_NEW_SOUTH_WALES`
- `STATE_VICTORIA`
- `STATE_TASMANIA`
- `STATE_QUEENSLAND`
- `STATE_SOUTH_AUSTRALIA`
- `STATE_WESTERN_AUSTRALIA`
- `STATE_NORTHERN_TERRITORY`
- `STATE_NORTH_ISLAND`
- `STATE_SOUTH_ISLAND`

Controle de couverture apres correction :
- `STATE_NEW_SOUTH_WALES` : 196 / 196, 0 manquante, 0 extra, 0 doublon.
- `STATE_VICTORIA` : 62 / 62, 0 manquante, 0 extra, 0 doublon.
- `STATE_TASMANIA` : 21 / 21, 0 manquante, 0 extra, 0 doublon.
- `STATE_QUEENSLAND` : 367 / 367, 0 manquante, 0 extra, 0 doublon.
- `STATE_SOUTH_AUSTRALIA` : 205 / 205, 0 manquante, 0 extra, 0 doublon.
- `STATE_WESTERN_AUSTRALIA` : 549 / 549, 0 manquante, 0 extra, 0 doublon.
- `STATE_NORTHERN_TERRITORY` : 292 / 292, 0 manquante, 0 extra, 0 doublon.
- `STATE_NORTH_ISLAND` : 35 / 35, 0 manquante, 0 extra, 0 doublon.
- `STATE_SOUTH_ISLAND` : 47 / 47, 0 manquante, 0 extra, 0 doublon.

## 6. naval_exit_id corriges

- `STATE_QUEENSLAND` : `3124` -> `3129`.
- `STATE_WESTERN_AUSTRALIA` : `3123` -> `3110`.
- `STATE_NORTHERN_TERRITORY` : `3126` -> `3125`.
- `STATE_SOUTH_ISLAND` : `3122` -> `3156`.

`STATE_SOUTH_AUSTRALIA` reste a `naval_exit_id = 3121`.

## 7. Impassables diagnostiques ou corriges

`STATE_SOUTH_AUSTRALIA` avait 98 impassables dans le mod contre 92 dans la reference 1.13.

Les six provinces retirees de la liste `impassable` sont :
- `x21C18C`
- `x0CA414`
- `x365B98`
- `x799A39`
- `xBA50D8`
- `x1622EC`

Ces provinces restent dans `provinces` et dans `owned_provinces`. Elles ne sont simplement plus marquees comme infranchissables.

## 8. Fichiers modifies

- `map_data/state_regions/13_australasia.txt`
- `common/history/states/00_states.txt`
- `common/history/pops/13_australasia.txt`
- `common/history/buildings/13_australasia.txt`
- `PHASE1_8_AUSTRALASIA_GREAT_WAVE_ALIGNMENT.md`

`common/history/diplomacy/00_subject_relationships.txt` ne contient pas de relation de sujet britannique ajoutee pour l'Australie dans l'etat final.

Fichiers volontairement non modifies pour cette correction :
- Japon, Sakhaline et Ryukyu ;
- Moyen-Orient ;
- technologies ;
- navires ;
- formations militaires ;
- events ;
- localisation generale.

## 9. Risques restants

- `STATE_TASMANIA` reste attribue a `WTI` par prudence, car la vanilla 1.13 consultee ne fournit pas de tag decentralise tasmanien evident.
- Les nouveaux tags decentralises australiens reposent sur les definitions vanilla chargees par le jeu. Le mod ne remplace pas completement `common/country_definitions`, donc ces tags devraient rester disponibles.
- Les buildings coloniaux britanniques vanilla ont ete retires. Cela evite l'anachronisme de 1776, mais il faudra verifier que les economies decentralisees restent stables en jeu.
- Cette phase est un portage technique, pas une refonte historique complete de l'Oceanie en 1776.

## 10. Tests a faire

1. Lancer le mod seul.
2. Ouvrir la selection pays et inspecter Australie / Nouvelle-Zelande.
3. Verifier qu'aucun sujet britannique australien (`NSW`, `SAS`, `WAS`, `TAS`) n'apparait.
4. Verifier visuellement :
   - New South Wales ;
   - Victoria ;
   - Tasmania ;
   - Queensland ;
   - South Australia ;
   - Western Australia ;
   - Northern Territory ;
   - North Island ;
   - South Island.
5. Lancer une partie en observateur.
6. Laisser tourner au moins un mois.
7. Surveiller `error.log` pour :
   - invalid `naval_exit_id` ;
   - provinces non assignees ;
   - invalid country/tag en Australasie ;
   - erreurs de pathfinding ou de state region.
