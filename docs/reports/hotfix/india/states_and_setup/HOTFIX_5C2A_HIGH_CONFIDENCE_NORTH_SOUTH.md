# HOTFIX-5C2A - References indiennes nord/sud a haute confiance

## 1. Resume

Cette phase remplace exactement 50 references aux cinq anciennes strategic regions indiennes par les deux regions vanilla valides :

- `region_north_india` ;
- `region_south_india`.

Le total runtime, commentaires exclus dans `common/` et `events/`, passe de **515** a **465**. Les changements sont limites aux cinq fichiers gameplay autorises et a leurs objets explicitement autorises.

## 2. Etat Git initial

| Element | Resultat |
|---|---|
| Branche | `hotfix-dlc-audit` |
| Working tree initial | Propre |
| HEAD initial | `e559efc Audit India strategic region references` |
| Commit HOTFIX-5C1 | Present |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |

Le stash MARATH n'a pas ete applique, restaure, supprime ou modifie.

## 3. Definitions vanilla verifiees

Reference : `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\west_south_asia_strategic_regions.txt`.

- `region_south_india` est definie ligne 29 ;
- `region_north_india` est definie ligne 43 ;
- `region_bengal`, `region_bombay`, `region_central_india`, `region_madras` et `region_punjab` ne sont pas definies par la vanilla locale.

## 4. Company type DEI

Fichier modifie : `common/company_types/02_new_companies.txt`.

Objet modifie exclusivement : `company_dutch_east_india_company`.

Les cinq listes regionales autorisees ont ete adaptees dans :

- `possible` ;
- `ai_will_do` ;
- cible de construction `building_tea_plantation` ;
- cible de construction `building_tobacco_plantation` ;
- cible de construction `building_opium_plantation`.

Chaque liste remplace ses cinq IDs invalides par nord/sud. Les conditions Indonesia, les buildings, niveaux, poids IA et conditions voisines sont inchanges.

References retirees : **25**.

## 5. Setup global BIC

Fichier modifie : `common/history/global/00_global.txt`.

Objet modifie exclusivement : le bloc `GLOBAL` de `c:BIC` marquant les sujets princiers au demarrage.

Les cinq regions indiennes invalides de la condition de capitale ont ete remplacees par nord/sud. Les conditions `region_himalayas` ainsi que les state regions de Birmanie sont strictement conservees, de meme que les scopes, variables, modifiers et autres blocs `GLOBAL`.

References retirees : **5**.

## 6. Interets GBR et BIC

Fichier modifie : `common/history/interests/00_interests.txt`.

Seuls les blocs `c:GBR` et `c:BIC` ont ete modifies. Chacun passe de quatre anciennes regions indiennes a deux interests valides, nord et sud. Les interests hors Inde et l'ordre des pays sont conserves.

References retirees : **8**.

## 7. Immediate British India

Fichier modifie : `common/journal_entries/00_player_objectives_great_game.txt`.

Dans `je_consolidate_british_india.immediate` uniquement, les scopes `sr:region_bengal` et `sr:region_madras` sont devenus respectivement `sr:region_north_india` et `sr:region_south_india`. Les sauvegardes de scope existantes, les states de Birmanie, l'objectif et toutes ses recompenses sont inchanges.

References retirees : **2**.

## 8. Hindu-German Conspiracy

Fichier modifie : `events/india_events/india_misc_events.txt`.

Objet modifie exclusivement : `india_events.6`.

Dans `trigger` et `immediate`, les deux OR cherchant un ennemi great power avec un marqueur d'interet indien utilisent maintenant nord/sud. La garde `ip2_content`, la selection de l'ennemi, les scopes, options, relations et modifiers sont inchanges.

References retirees : **10**.

## 9. Tableau des references retirees

| Fichier | Objet | Avant | Apres | Retirees |
|---|---|---:|---:|---:|
| `common/company_types/02_new_companies.txt` | `company_dutch_east_india_company` | 25 | 0 | 25 |
| `common/history/global/00_global.txt` | `GLOBAL / c:BIC` | 5 | 0 | 5 |
| `common/history/interests/00_interests.txt` | `c:GBR` et `c:BIC` | 10 | 2 | 8 |
| `common/journal_entries/00_player_objectives_great_game.txt` | `je_consolidate_british_india.immediate` | 4 | 2 | 2 |
| `events/india_events/india_misc_events.txt` | `india_events.6` | 10 | 0 | 10 |
| **Total** | | **54** | **4** | **50** |

Les quatre references restantes dans les deux fichiers partiellement corriges sont intentionnelles : deux dans `c:DUR`, reservees a HOTFIX-5D, et deux dans la completion British India, reservees a HOTFIX-5C3.

## 10. Total global avant/apres

| Mesure | Occurrences |
|---|---:|
| Avant HOTFIX-5C2A | 515 |
| Retirees par cette phase | 50 |
| Apres HOTFIX-5C2A | **465** |

Le recomptage couvre `common/` et `events/` et ignore les commentaires. Le total n'est pas cense etre nul : les chaines Durrani, Sepoy, Famines, IA, HQ et boutons legacy restent hors scope.

## 11. c:DUR inchange

Le bloc `c:DUR` de `common/history/interests/00_interests.txt` est strictement inchange. Il conserve :

- `region_central_india` ;
- `region_bombay` ;
- `region_central_asia`.

Ces deux references invalides font partie du lot Durrani reserve a HOTFIX-5D.

## 12. Completion British India inchangee

Le bloc `complete` de `je_consolidate_british_india`, y compris son tooltip, est strictement inchange. Les deux references suivantes restent volontairement en place :

- `region_bengal` ;
- `region_madras`.

La completion doit etre adaptee plus tard avec des state regions explicites dans HOTFIX-5C3 ; elle ne doit pas recevoir un remplacement large dans cette phase.

## 13. Frontier colonization BIC inchangee

La loi BIC `activate_law = law_type:law_frontier_colonization` reste intacte. Aucune ligne contenant `activate_law`, `law_frontier_colonization`, `law_colonial_exploitation` ou `law_mercantilism_navigation_acts` n'entre dans le diff.

## 14. Risques restants

- Les 465 references restantes exigent encore des corrections par lots ; une recherche globale ne doit pas etre utilisee pour les modifier.
- Les chains Sepoy et Famines melangent perimetres panindiens et sous-regions historiques, ce qui requiert parfois des geographic regions ou des state regions explicites.
- Le lot Durrani est historiquement sensible et reste isole.
- Les HQ de formations restent hors scope, notamment MARATH, Travancore et les amiraux BIC.
- Les definitions de boutons coloniaux legacy restent preservees par choix de compatibilite transitoire.

## 15. Tests en jeu recommandes

1. Lancer BIC, GBR et une puissance eligible a la DEI ; verifier les company conditions et cibles IA.
2. Verifier que les interests initiaux GBR/BIC existent dans nord et sud de l'Inde.
3. Verifier `je_consolidate_british_india` et sa partie immediate sans modifier sa completion.
4. Avec IP2 active, verifier le declenchement et la selection ennemie de `india_events.6`.
5. Passer le premier jour puis plusieurs mois et surveiller `error.log` pour les IDs regionaux et erreurs de scope.
6. Confirmer que les blocs Durrani, MARATH, Travancore et les boutons legacy ont le meme comportement qu'avant la phase.

## 16. Fichiers modifies/crees

Fichiers gameplay modifies :

- `common/company_types/02_new_companies.txt` ;
- `common/history/global/00_global.txt` ;
- `common/history/interests/00_interests.txt` ;
- `common/journal_entries/00_player_objectives_great_game.txt` ;
- `events/india_events/india_misc_events.txt`.

Fichier cree :

- `docs/reports/hotfix/HOTFIX_5C2A_HIGH_CONFIDENCE_NORTH_SOUTH.md`.

## 17. Confirmation du perimetre

Aucune formation, flotte, loi, localisation, building, production method, fichier Durrani, fichier MARATH ou bouton colonial legacy n'a ete modifie. Aucun fichier entier n'a ete remplace et aucun merge automatique n'a ete effectue.

## 18. Confirmation stash MARATH

Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est reste present et intact. Aucune commande de restauration ou d'application du stash n'a ete executee.
