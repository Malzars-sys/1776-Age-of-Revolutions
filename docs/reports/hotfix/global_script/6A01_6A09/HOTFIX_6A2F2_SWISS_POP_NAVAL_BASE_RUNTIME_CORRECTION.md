# HOTFIX-6A.2F2 — Correction runtime population suisse et infrastructure navale croate

Date : 2026-07-23  
Statut : `INTERMEDIATE`, correction et runtime validés  
Périmètre gameplay : `common/history/pops/00_west_europe.txt` et `common/history/buildings/01_south_europe.txt`

## 1. Résumé

Le hunk de 30 000 habitants autrichiens en Suisse orientale a été restauré exactement depuis la source hotfix. L’audit NAVY 1.13 a prouvé que le bâtiment fonctionnel n’est pas l’ancien identifiant `building_naval_base`, mais `building_naval_administration`; un niveau 3 a donc été ajouté en Croatie pour couvrir le besoin observé de 2,30 K marins. Les contrôles statiques et l’unique runtime launcher passent.

## 2. État hérité de 6A.2F

Les transferts Croatia/Slavonia, la province `x90C0E0`, les scopes de pops et buildings, le shipyard croate niveau 2, la suppression des pactes CRO, la flotte 1+3 et Agram 24 étaient déjà appliqués. Les quatre fichiers gameplay protégés ont conservé exactement leurs empreintes post-6A.2F.

## 3. Runtime manuel opérateur

Le premier runtime manuel valide utilisait le bon playset et rendait le fork visible au 1er janvier 1776. Il montrait la portion autrichienne de Suisse orientale à 0,00 K, PIB 0,00, sans niveau de vie; `K_K_Kriegsmarine` était visible, composée de 1 capital et 3 croiseurs/frégates, au QG Balkans, mais à environ 0 / 2,30 K. Croatia était sous AUS et fonctionnelle.

## 4. Captures et observations

Preuves finales fournies par l’opérateur :

- `C:/Users/simeo/Pictures/Screenshots/Capture d'écran 2026-07-23 032921.png` : flotte 1+3, QG Balkans, 2,30 K / 2,30 K;
- `C:/Users/simeo/Pictures/Screenshots/Capture d'écran 2026-07-23 032944.png` : Croatia sous AUS, administration navale niveau 3 et port niveau 1;
- `C:/Users/simeo/Pictures/Screenshots/Capture d'écran 2026-07-23 033008.png` : Suisse orientale autrichienne, 30,0 K habitants, PIB 6,23 K£, niveau de vie 7,3.

L’opérateur conclut : « tous à l’air en norme ».

## 5. Portion suisse vide

La province autrichienne séparée existait territorialement mais le seul `region_state` de population appartenait à SWI. La preuve runtime invalide donc la décision de variation nette nulle.

## 6. Flotte sans effectifs

Le shipyard produisait les navires mais ne recrutait aucun marin. Le besoin affiché de la formation était 2,30 K.

## 7. Analyse shipyard / base navale

`building_shipyard` assure construction et remplacement. Dans les définitions vanilla 1.13, `building_naval_administration` porte `recruits_sailors = yes`; son PM `pm_simple_sailor_recruitment` ajoute 900 soldats, 100 officiers et 1 000 de capacité marins par niveau. Aucun bâtiment `building_naval_base` n’est défini.

## 8. Verdict population antérieur superseded

`SWISS_POP_HUNK_SHOULD_BE_OMITTED` devient `SUPERSEDED_BY_RUNTIME_EVIDENCE`. Nouvelle décision : `SWISS_POP_ADDITION_RUNTIME_JUSTIFIED`.

## 9. Hunk population hotfix

Sous `s:STATE_EAST_SWITZERLAND`, un seul `region_state:AUS` crée un seul pop `south_german` de taille `30000`, sans religion ni profession. Le bloc SWI existant n’est pas modifié.

## 10. Variation nette +30 000

Le total SWI reste 895 200. La variation nette assumée du fichier est +30 000, limitée à la portion autrichienne.

## 11. Architecture NAVY

Les rapports NAVY-2D et NAVY-2D-bis utilisent `building_naval_administration` avec `pm_simple_sailor_recruitment`. Le runtime antérieur établit environ 1 000 marins par niveau. GEN fournit l’analogue exact : flotte de quatre unités, besoin 2,30 K, administration niveau 3.

## 12. Niveau de base navale

Verdict : `NAVAL_BASE_CROATIA_OTHER_LEVEL_PROVEN`. Le niveau minimal est 3, car `ceil(2300 / 1000) = 3`. Le niveau 4 aurait créé une marge non justifiée.

## 13. Hunk naval

Un seul `building_naval_administration` a été ajouté dans `STATE_CROATIA`, scope et owner AUS, niveau 3, `reserves=1`, PM `pm_simple_sailor_recruitment`. Le port, le shipyard niveau 2, les ownerships HUN et les PM ADMIN sont inchangés.

## 14. Tests statiques

Population AUS unique, taille 30 000 unique, culture exacte, SWI 895 200 inchangée, administration navale croate unique, owner AUS, niveau 3 et PM exact : PASS. Port, shipyard, ownership HUN et PM ADMIN : PASS. Accolades, `git diff --check`, périmètre gameplay et zéro staged : PASS.

Verdict : `HOTFIX_6A2F2_SWISS_POP_NAVAL_BASE_STATIC_PASS`.

## 15. Playset

La base SQLite du launcher prouve que `hhhh` est le seul playset actif et contient exactement un mod activé : `1776_Age_of_Revolutions_fork`, position 0. `content_load.json` confirme le même dossier unique.

## 16. Preuve du montage du fork

L’unique lancement du jeu a été déclenché depuis le launcher. `debug.1.log`, lignes 68 et 87, nomme puis monte explicitement `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.

## 17. Résultat Suisse

La capture finale montre 30,0 K habitants, un PIB calculé de 6,23 K£, un niveau de vie calculé de 7,3, le marché autrichien et l’état divisé. Verdict : `AUSTRIAN_EAST_SWITZERLAND_30000_POP_CONFIRMED`.

## 18. Résultat infrastructure navale

La capture Croatia montre l’administration navale au niveau 3 dans l’état AUS, avec le port niveau 1 conservé. Verdict : `NAVAL_BASE_CROATIA_RUNTIME_CONFIRMED`, le terme « base navale » désignant ici l’administration navale valide de l’architecture 1.13.

## 19. Résultat flotte

`K. K. Kriegs-Marine` reste à 1 navire capital et 3 croiseurs, stationnée au QG des Balkans. La capacité est entièrement pourvue à 2,30 K / 2,30 K. Verdict : `AUS_FLEET_MANPOWER_RUNTIME_PASS`.

## 20. Résultat Agram

Le fichier formations est byte-for-byte identique au post-6A.2F et conserve Agram sous AUS avec 24 line infantry. L’opérateur a confirmé globalement que les éléments contrôlés paraissaient normaux; aucune erreur ciblée Agram n’apparaît dans les logs.

## 21. Non-régression Russie

Aucun fichier Russie n’a changé. Subjecthood reste la valeur statiquement protégée de 6A.1; aucune erreur ciblée RUS n’est issue de 6A.2F2. Verdict : `RUSSIA_SUBJECTHOOD_NON_REGRESSION_PASS`.

## 22. Logs

Aucune erreur ne vise les nouveaux hunks, `STATE_EAST_SWITZERLAND`, `building_naval_administration`, `STATE_CROATIA`, `K_K_Kriegsmarine` ou Agram. Le diagnostic `building_naval_base` de `common/ai_strategies/00_default_strategy.txt:5085` est un résidu préexistant et confirme que cet ancien ID n’est pas un objet valide. Les diagnostics `Invalid right side` proviennent de `01_natural_borders_of_france.txt`; les doublons de localisation et le tooltip naval français sont hors périmètre et préexistants.

## 23. Fichiers modifiés

Gameplay : `common/history/pops/00_west_europe.txt` et `common/history/buildings/01_south_europe.txt`. Documentation : ce rapport, la delta map et les six index/roadmap autorisés. Aucun autre gameplay n’a été ajouté à 6A.2F2.

## 24. Protections

Les hashes protégés restent : states `625C40...62067`, pops sud `B26A2F...71E9A2`, subject relationships `BA138E...3BCB1`, formations `F170CF...FEA33`. Aucune localisation, loi, formation, technologie, descripteur ou sauvegarde persistante n’a été modifiée.

## 25. Verdict final

`SWISS_POP_ADDITION_RUNTIME_JUSTIFIED`  
`AUSTRIAN_EAST_SWITZERLAND_30000_POP_CONFIRMED`  
`NAVAL_BASE_CROATIA_RUNTIME_CONFIRMED`  
`AUS_FLEET_MANPOWER_RUNTIME_PASS`  
`CROATIA_SLAVONIA_ABSORBED_BY_AUS`  
`EAST_SWITZERLAND_SLIVER_TRANSFERRED`  
`CRO_SUBJECT_RELATION_REMOVED`  
`SHIPYARD_CROATIA_LEVEL_2_CONFIRMED`  
`AGRAM_24_INFANTRY_MIGRATED_TO_AUS`  
`RUSSIA_SUBJECTHOOD_NON_REGRESSION_PASS`  
`AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_RUNTIME_PASS`  
`AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX_COMPLETE`  
`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

## 26. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` reste intact; son contenu n’a pas été inspecté, appliqué ou modifié.

## 27. Confirmation docs/research/technology

`docs/research/technology/` reste non suivi et intact.

## 28. Fermeture des processus

Victoria 3 puis le launcher ont été fermés après les captures et l’analyse. Aucun processus `victoria3`, `Paradox Launcher`, `cpatch` ou `dowser` ne restait actif.

## 29. Rollback ciblé

Le rollback 6A.2F2 consiste uniquement à supprimer le `region_state:AUS` de 30 000 habitants et le `building_naval_administration` AUS niveau 3 ajoutés. Aucun hunk 6A.2F antérieur ne doit être annulé.
