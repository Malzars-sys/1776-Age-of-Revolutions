# HOTFIX-6A.2R — Résolution des hunks cibles Autriche–Croatie–Suisse

Date : 2026-07-23  
Périmètre : résolution statique et documentaire, aucun gameplay modifié

## 1. Résumé

Les quatre décisions héritées de 6A.2 sont closes. Le hunk suisse de 30 000 habitants doit être omis faute de preuve. Le shipyard croate est compatible sous forme du seul bloc hotfix. La flotte autrichienne doit être reconstruite à l’échelle NAVY actuelle (1 vaisseau de ligne et 3 frégates, nommée `K_K_Kriegsmarine`, HQ Balkans, unités en Croatia). `generalkommando_agram` doit migrer de CRO vers AUS sans changer ses 24 unités. Verdict : `READY_FOR_AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX`.

## 2. Verdict d’entrée

Entrée : `BLOCKED_TARGET_HUNKS_UNVERIFIED`, dans `HOTFIX-6A_GLOBAL_SCRIPT_DELTAS` et `HOTFIX_6A2R_TARGET_HUNK_RESOLUTION`.

## 3. État Git initial

Racine exacte du fork, branche `hotfix-dlc-audit`, HEAD `f4d3398 Audit Austria Croatia and Swiss hotfix deltas`, aucun fichier suivi modifié, aucun staged, seule exception non suivie `docs/research/technology/`. `git diff --check` était propre. Le stash MARATH attendu était intact. Victoria 3 et le launcher étaient fermés. Le fichier Russie ne différait pas du commit `991f6a1`.

## 4. Sources

Rapport et delta map 6A.2, roadmap, registres de travail restant et différences globales, les 22 rapports suivis sous `docs/reports/navy/`, les commits NAVY suivis, et les versions fork/hotfix/vanilla 1.13 des fichiers pops, buildings, states, sujets et formations.

## 5. Méthode

Lecture et comparaison par `Get-ChildItem`, `Get-FileHash`, `Get-Content`, `Select-String`, `Compare-Object`, `git log`, `git show` et `git diff --no-index`. Aucun `rg`, aucun accès au contenu du stash, aucun lancement et aucune modification des sources hotfix/vanilla.

## 6. Blockers hérités de 6A.2

Les neuf hunks territoriaux/de cohérence étaient déjà prouvés. Restait à décider : le bloc pop AUS de 30 000, le shipyard Croatia, la flotte AUS et le devenir de l’armée CRO `generalkommando_agram`.

## 7. Population suisse actuelle

Dans le fork, `STATE_EAST_SWITZERLAND/region_state:SWI` contient trois groupes sans profession explicite : 320 014 Alemannic catholiques, 388 400 Alemannic de religion par défaut et 186 786 North Italian de religion par défaut. Total : 895 200. Aucun `region_state:AUS`.

## 8. Population suisse hotfix

Le hotfix conserve intégralement les 895 200 SWI et ajoute `region_state:AUS/create_pop`, culture `south_german`, religion et profession non précisées, taille 30 000. Total résultant : 925 200, soit +30 000.

## 9. Population suisse vanilla

Vanilla 1.13 contient les mêmes trois groupes SWI et le même total de 895 200, sans bloc AUS. Les différences de fichier hors bloc ne fournissent aucune preuve de transfert.

## 10. Recherche de preuve des 30 000

La recherche dans le corpus hotfix, les changelogs, rapports, commentaires, historiques et fichiers liés ne trouve qu’une occurrence cible : le bloc hotfix lui-même. Le changelog prouve le transfert de `x90C0E0`, pas une hausse démographique. Les autres valeurs 30 000 du corpus concernent d’autres régions. Aucune source n’associe une population exacte à la province.

## 11. Calculs de population

- avant : SWI 895 200, AUS 0, cumul 895 200 ;
- hotfix brut : SWI 895 200, AUS 30 000, cumul 925 200, variation +30 000 ;
- proposition : SWI 895 200, AUS 0, cumul 895 200, variation nette 0.

`x90C0E0` est la province `mine` de la state region, mais aucune population n’est attachée directement aux provinces dans ce fichier.

## 12. Solutions POP-A à POP-D

- POP-A : rejetée, aucun groupe SWI à réduire n’est identifié par une preuve exacte ;
- POP-B : rejetée, aucune source ne prouve une addition intentionnelle au total ;
- POP-C : rejetée, aucune donnée provinciale défendable ne permet une proportion ;
- POP-D : retenue, omission du seul hunk pop AUS.

## 13. Décision population suisse

`SWISS_POP_HUNK_SHOULD_BE_OMITTED`.

Valeur fork et vanilla : bloc SWI 895 200, aucun AUS. Valeur hotfix : même bloc SWI plus 30 000 South Germans AUS. Groupe à créer : aucun. Groupe à réduire : aucun. Ancre : fin de `s:STATE_EAST_SWITZERLAND`, après `region_state:SWI`. Hunk futur : aucun. Rollback : sans objet, car le fichier ne doit pas être modifié.

La portion AUS peut exister sans population initiale dédiée : le state territorial est valide mais commence vide; les pops et bâtiments SWI restent dans le `region_state:SWI`. Le runtime devra vérifier que ce choix ne produit pas d’erreur et que la portion AUS est bien créée.

## 14. Variation nette retenue

Variation nette recommandée : **0**. Total avant et après : 895 200.

## 15. Architecture NAVY actuelle

Les formations utilisent `create_military_formation`, `type = fleet`, un `hq_region` vanilla 1.13 valide, un identifiant ASCII localisable, puis des `ship` avec `ship_type:*`, `state_region` et `count`. Les HQ terrestres valides sont privilégiés. Une flotte initiale n’exige pas de shipyard pour apparaître, mais le chantier soutient construction/remplacement. Les petites flottes méditerranéennes finales vont de 1 frégate à 2 vaisseaux de ligne + 5 frégates.

## 16. Historique Git NAVY

Le fichier de formations porte les commits `7c789b8`, `8283dcc`, `6e8428e`, `cf7b0a5`, `083b765`, `3f93a5a` et `f0eed80`. Le fichier buildings porte `fbcc090`, `8c741ef` et `72afe86`. Aucun n’est annulé. Aucun commit suivi n’a créé de flotte AUS; le seul historique de `K_K_Kriegsmarine` vient de vanilla. Les rapports NAVY ne contiennent pas de décision autrichienne antérieure.

## 17. Shipyard Croatia

Fork et vanilla : port CRO niveau 1, aucun shipyard dans Croatia. Hotfix : même port re-clé AUS et ajout d’un `building_shipyard` possédé par un `building_financial_district` AUS, `levels=2`, `region="STATE_CROATIA"`, `reserves=1`, PM `pm_basic_shipbuilding`.

Décision : `SHIPYARD_CROATIA_REQUIRED_COMPATIBLE`. Le PM et le type sont 1.13/NAVY compatibles; le niveau 2 reste inférieur à une infrastructure de grande puissance et soutient la flotte régionale reconstruite. Aucun doublon n’existe dans Croatia. Hunk minimal : insérer uniquement ce `create_building` entre le fishing wharf et le port, après re-clé du scope vers AUS. Rollback : supprimer exactement ce bloc.

## 18. Flottes AUS existantes

Le fork ne contient aucune formation `type = fleet` dans `c:AUS`. Le setup 1776 donne Istria à VEN; AUS ne possède donc ni port ni chantier avant l’absorption de Croatia. Vanilla possède `K_K_Kriegsmarine`, 5 frégates, mais ce setup 1836 n’est pas copiable.

## 19. Flottes CRO existantes

Fork et vanilla ne contiennent aucune flotte CRO. CRO possède seulement `generalkommando_agram`. Aucune unité navale ne peut donc être transférée depuis CRO.

## 20. Flotte hotfix proposée

Le hotfix ajoute à AUS une flotte anonyme, HQ `region_balkans`, 3 vaisseaux de ligne et 6 frégates, sans `state_region`. Elle est intentionnelle d’après le changelog, mais dépasse les petites flottes régionales actuelles et ne respecte pas toutes les conventions documentées.

## 21. Décision flotte AUS

`AUS_FLEET_REQUIRED_RECONSTRUCTED`.

Hunk retenu sous `c:AUS`, avant les armées : identifiant `K_K_Kriegsmarine` (clé vanilla déjà localisée), pays AUS, `hq_region = sr:region_balkans` (valide et contenant Croatia), un `ship_type_ship_of_the_line` count 1 en `STATE_CROATIA`, et un `ship_type_frigate` count 3 en `STATE_CROATIA`. Origine : création hotfix réduite à l’échelle NAVY régionale actuelle; aucun transfert CRO. Absence de doublon : zéro flotte AUS et CRO dans le fork. Rollback : supprimer exactement cette formation.

La composition 1+3 correspond au palier inférieur des flottes méditerranéennes suivies (GEN 1+3, SIC 1+4, VEN 2+5) et évite que la nouvelle marine autrichienne dépasse d’emblée les puissances navales régionales établies.

## 22. Generalkommando Agram

Le fork et vanilla définissent sous `c:CRO` une armée HQ Balkans nommée `generalkommando_agram` : 2 line infantry en Slavonia, 12 puis 4 line infantry en Croatia, et 6 line infantry en Slavonia, total 24. Le hotfix la recrée sous AUS mais transforme le contenu en 22 line infantry, 4 cuirassiers et 6 canons, total 32.

## 23. Formations CRO

`generalkommando_agram` est l’unique formation CRO. Après transfert des deux states et suppression des pactes, la laisser sous un CRO sans territoire créerait une formation orpheline. Les 24 unités du fork sont plus récentes et cohérentes avec le setup 1776; aucune preuve n’autorise les 8 unités supplémentaires ni les changements de types hotfix.

## 24. Décision Agram

`AGRAM_MIGRATION_REQUIRED_MINIMAL`.

Déplacer exactement le `create_military_formation` existant de `c:CRO` dans `c:AUS`, sans modifier nom, HQ, commentaires, types, state regions ni comptes; supprimer seulement le wrapper CRO devenu vide. Ancre d’insertion : sous `c:AUS`, après la flotte reconstruite et avant `generalkommando_lemberg`. Rollback : retirer ce bloc d’AUS et restaurer byte-for-byte le wrapper et bloc CRO d’origine.

## 25. Cohérence de CRO sans territoire

CRO reste défini mais dormant/libérable. Son fichier pays doit être préservé. Les deux pactes AUS→CRO doivent disparaître; states, pops et buildings sont re-clés vers AUS; sa formation migre. Les références d’événements, journal, mouvement, drapeaux et noms dynamiques utilisent des gardes `exists`, des scopes optionnels ou des mécanismes de libération : elles justifient de conserver le tag, pas de lui laisser territoire ou armée au départ.

## 26. Compatibilité Victoria 3 1.13

Les deux HQ retenus (`region_balkans`) existent. `STATE_CROATIA` et `STATE_SLAVONIA` appartiennent à cette strategic region. Les types `ship_type_ship_of_the_line`, `ship_type_frigate`, le bâtiment `building_shipyard` et `pm_basic_shipbuilding` sont valides. Chaque navire reçoit un `state_region` explicite.

## 27. Compatibilité ADMIN

Le PM de l’administration Croatia reste exactement `pm_horizontal_drawer_cabinets`, `pm_hereditary_bureaucrats`, `pm_religious_bureaucrats`. Seuls le scope et les huit références d’ownership CRO du bloc sont re-clés AUS. Les owners HUN et tous les PM restent inchangés.

## 28. Compatibilité NAVY

Aucun bloc NAVY existant n’est remplacé. La flotte suit la syntaxe, le HQ valide, le nom localisé et l’échelle régionale documentés. Le shipyard utilise le bâtiment et le PM actuels. Agram conserve intégralement les valeurs fork.

## 29. Compatibilité setup 1776

Les fichiers pays AUS/CRO/SWI, événements, journaux et relations générales restent inchangés. La flotte est volontairement inférieure à VEN et le bloc militaire hotfix 32 unités est rejeté au profit des 24 unités 1776 du fork.

## 30. Hunks territoriaux déjà prouvés

Dans `00_states.txt` : owner Croatia CRO→AUS, owner Slavonia CRO→AUS, retrait de `x90C0E0` de SWI et création d’une portion AUS avec cette seule province dans `STATE_EAST_SWITZERLAND`.

## 31. Hunks population résolus

Dans `01_south_europe.txt`, re-clé des scopes Croatia et Slavonia CRO→AUS sans changer aucun groupe. Dans `00_west_europe.txt`, aucun hunk : omission des 30 000.

## 32. Hunks buildings résolus

Croatia : scope CRO→AUS, huit ownerships CRO→AUS, ajout du seul shipyard niveau 2; HUN et PM inchangés. Slavonia : scope CRO→AUS et manor house CRO→AUS; HUN et PM inchangés.

## 33. Hunks formations résolus

Ajouter la flotte AUS reconstruite 1+3; déplacer Agram CRO→AUS byte-for-byte; ne copier aucun bloc complet hotfix.

## 34. Hunks diplomatiques résolus

Supprimer uniquement les deux blocs `create_diplomatic_pact` AUS→CRO de types `crown_land` et `decrease_payments`.

## 35. Liste fermée des fichiers du futur correctif

Gameplay, exactement cinq fichiers :

1. `common/history/states/00_states.txt`;
2. `common/history/pops/01_south_europe.txt`;
3. `common/history/buildings/01_south_europe.txt`;
4. `common/history/diplomacy/00_subject_relationships.txt`;
5. `common/history/military_formations/00_military_formations_europe.txt`.

`common/history/pops/00_west_europe.txt` est explicitement exclu.

## 36. Ordre exact du futur correctif

1. states; 2. pops Croatia/Slavonia; 3. buildings et shipyard; 4. pactes; 5. flotte et Agram; 6. contrôles statiques; 7. préparation du runtime unique. Aucun import complet.

## 37. Rollback

Restaurer les trois blocs states; remettre les deux scopes pops à CRO; remettre scope et neuf ownerships buildings (huit Croatia, un Slavonia) à CRO puis supprimer le shipyard; restaurer les deux pactes; supprimer la flotte AUS et remettre Agram sous son wrapper CRO. Aucun rollback dans `00_west_europe.txt` puisqu’il ne change pas.

## 38. Tests statiques futurs

Vérifier les occurrences et comptes exacts, les 8+1 ownerships buildings, les provinces inchangées, l’absence des pactes, une seule flotte `K_K_Kriegsmarine`, 1 SOL + 3 frégates avec `STATE_CROATIA`, un seul Agram sous AUS avec 24 line infantry, aucune formation CRO de départ, accolades équilibrées, `git diff --check`, diff limité aux fichiers fermés, Russie intacte et staging vide.

## 39. Runtime futur consolidé

Un seul lancement après les tests statiques : charger 1776, inspecter AUS/CRO/SWI et RUS, confirmer owners, absence de sujet CRO, portion suisse AUS sans inflation, pops/buildings Croatia-Slavonia, accès côtier et port, shipyard, flotte 1+3, Agram 24, puis contrôler `error.log`, `game.log` et `debug.log` pour states, pops, buildings, formations, HQ et pactes.

## 40. Risques restants

La portion suisse AUS sera initialement vide; ce comportement doit être observé au runtime. Le niveau 2 du shipyard et l’échelle 1+3 restent des choix de compatibilité, pas une copie brute. Les événements pouvant libérer CRO doivent rester non régressifs. Aucun de ces risques ne bloque la correction ciblée.

## 41. Fichiers créés ou modifiés

Créé : ce rapport. Modifiés : delta map 6A.2 et documents autorisés de navigation, statut, roadmap et prompt. Aucun fichier gameplay.

## 42. Confirmation gameplay inchangé

`NO_GAMEPLAY_CHANGED`. Aucun fichier sous `common/`, `events/`, `history/`, `map_data/` ou `localization/` n’a été modifié.

## 43. Confirmation Russie intacte

Le fichier `common/history/countries/rus - russia.txt` reste identique au commit `991f6a1`.

## 44. Confirmation blocs clos

Inde, Japon, Mamluk Iraq, Russie, ADMIN et les autres blocs clos n’ont pas été modifiés. 6A.2R résout seulement les décisions nécessaires au futur paquet ciblé.

## 45. Confirmation docs/research/technology/

Le répertoire non suivi préexistant reste intact et hors périmètre.

## 46. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est intact; aucun apply, pop, drop ou inspection de contenu.

## 47. Verdict

- `READY_FOR_AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX`
- `HOTFIX_6A2R_TARGET_HUNK_RESOLUTION_COMPLETE`
- `SWISS_POP_HUNK_SHOULD_BE_OMITTED`
- `SHIPYARD_CROATIA_REQUIRED_COMPATIBLE`
- `AUS_FLEET_REQUIRED_RECONSTRUCTED`
- `AGRAM_MIGRATION_REQUIRED_MINIMAL`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
