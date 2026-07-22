# HOTFIX-6A.2 — Audit Autriche, Croatie-Slavonie et Suisse occidentale

Date : 2026-07-23  
Périmètre : audit statique documentaire, aucun gameplay

## 1. Résumé

Les annonces 2.3 correspondent à de vrais deltas custom hotfix absents du fork. Le cœur territorial est précis, mais le paquet complet n’est pas encore corrigeable sans arbitrage : la population suisse ajoute 30 000 personnes sans transfert démontré et les formations/flotte croisent directement NAVY tout en modifiant types et comptes. Verdict : `BLOCKED_TARGET_HUNKS_UNVERIFIED`.

## 2. Verdict d’entrée

`HOTFIX_6A_RUSSIA_SUBJECTHOOD_ALIGNMENT_COMPLETE`; `HOTFIX-6A_GLOBAL_SCRIPT_DELTAS` continue avec la revue Autriche/Croatie/Slavonie/Suisse.

## 3. État Git initial

Racine exacte, branche `hotfix-dlc-audit`, HEAD `991f6a1 Align Russia with subjecthood law`, zéro fichier suivi modifié, zéro staged, seule exception non suivie `docs/research/technology/`, stash MARATH intact. La copie Sepoy était absente. Après fermeture demandée, Victoria 3 et Paradox Launcher étaient tous deux fermés.

## 4. Sources et méthode

Comparaison fork/hotfix/vanilla par `Get-ChildItem`, `Get-FileHash`, `Get-Content`, `Compare-Object`, `Select-String`, `git log` et `git blame`. Les blocs ont été extraits par ancres et équilibre d’accolades; aucun nom de tag, state ou province n’a été inventé.

## 5. Changelog

- ligne 10 : `Croatia-Slovenia is now absorbed into Austria to give them sea access and a fleet`;
- ligne 11 : `a sliver of West Switzerland is given to Austria to connect their Italian province`.

La première annonce est implémentée dans states, sujets, bâtiments, pops et formations. La seconde est implémentée dans `STATE_EAST_SWITZERLAND`, malgré le libellé « West Switzerland ».

## 6. Inventaire initial

La delta map contient 28 enregistrements : hunks territoriaux et de cohérence, protections NAVY/ADMIN, fichiers identiques, contenu hérité de vanilla, divergences 1776 et revues non liées. Les hashes et présences exacts figurent dans `HOTFIX_6A2_AUSTRIA_CROATIA_WEST_SWITZERLAND_DELTA_MAP.csv`.

Tailles fork / hotfix / vanilla en octets (`—` = absent du mod et hérité de vanilla) :

| Fichier | Fork | Hotfix | Vanilla |
|---|---:|---:|---:|
| `common/history/states/00_states.txt` | 469655 | 469089 | 476160 |
| `common/history/diplomacy/00_subject_relationships.txt` | 8164 | 7943 | 10580 |
| `common/history/diplomacy/00_relations.txt` | 12522 | 12522 | 13266 |
| `common/history/buildings/00_west_europe.txt` | 184862 | 186879 | 209081 |
| `common/history/buildings/01_south_europe.txt` | 137449 | 137062 | 137584 |
| `common/history/pops/00_west_europe.txt` | 33374 | 33468 | 33281 |
| `common/history/pops/01_south_europe.txt` | 17572 | 17572 | 17665 |
| `common/history/military_formations/00_military_formations_europe.txt` | 111467 | 93967 | 97621 |
| `common/history/countries/aus - austria.txt` | 1426 | 1426 | 1952 |
| `common/history/countries/cro - croatia.txt` | 1308 | 1308 | 1179 |
| `common/history/countries/swi - switzerland.txt` | 1023 | 1023 | 1310 |
| `common/journal_entries/05_austria_journal_entries.txt` | 9617 | 9667 | 9667 |
| `common/journal_entries/05_austrian_fascism.txt` | 5932 | 6746 | 6682 |
| `events/balkans_events/00_ip3_austria_events.txt` | 19507 | 20282 | 20282 |
| `events/balkans_events/03_ip3_austria_events.txt` | 18360 | 18655 | 18655 |
| `events/balkans_events/austria_federalism.txt` | 55666 | 55582 | 55582 |
| `map_data/state_regions/00_west_europe.txt` | — | — | 56290 |
| `common/strategic_regions/europe_strategic_regions.txt` | — | — | 7673 |
| `common/decisions/austria_decisions.txt` | — | — | 4826 |
| `localization/english/NM_Countries_l_english.yml` | 2151 | 2151 | — |
| `localization/french/NM_Countries_l_french.yml` | 2233 | — | — |

## 7. Audit Autriche

`aus - austria.txt` est strictement identique entre fork et hotfix et diffère de vanilla : le setup pays 1776 est déjà aligné et doit être préservé. Les changements légitimes concernent les territoires rattachés à AUS et leurs scopes dépendants, pas le fichier pays. Le runtime futur devra vérifier accès côtier, états, populations, bâtiments et formations.

## 8. Audit Croatie

Le fork et vanilla donnent les huit provinces de `STATE_CROATIA` à `c:CRO`; le hotfix conserve exactement les mêmes provinces mais remplace l’owner par `c:AUS`. Aucun controller séparé n’est défini. Le fichier pays CRO reste identique fork/hotfix et n’est pas supprimé.

## 9. Audit Slavonie

Le fork et vanilla donnent les sept provinces de `STATE_SLAVONIA` à `c:CRO`; le hotfix conserve exactement ces provinces et remplace l’owner par `c:AUS`. Aucun autre mécanisme territorial n’est utilisé.

## 10. Audit Croatie-Slavonie

Le changement complet implique au minimum deux owners d’états, deux scopes de pops, les scopes/owners de bâtiments et la suppression de deux pactes CRO. Le hotfix ajoute aussi un shipyard, une flotte AUS et remanie l’armée Agram. Les quatre premiers groupes sont prouvés; les éléments militaires/navals doivent être réconciliés avec NAVY avant correction.

## 11. Audit Suisse

Les fichiers pays SWI sont identiques fork/hotfix. `STATE_WEST_SWITZERLAND` est textuellement identique dans les trois arbres. Aucune décision, relation ou localisation nouvelle n’est requise.

## 12. Audit West Switzerland

Le seul hunk hotfix est dans `STATE_EAST_SWITZERLAND` : la province `x90C0E0` quitte la liste SWI et forme une portion AUS. Vanilla confirme que `x90C0E0` appartient à cette state region et y porte la mine. Le hotfix ajoute en parallèle un region_state AUS de 30 000 South Germans, mais ne réduit pas les 895 200 pops SWI : cette création est `UNVERIFIED` jusqu’à preuve qu’il ne s’agit pas d’une inflation involontaire.

## 13. Histoire des states

Trois hunks `REQUIRED_HOTFIX_DELTA` dans `00_states.txt` : owner CRO→AUS pour `STATE_CROATIA`, owner CRO→AUS pour `STATE_SLAVONIA`, et split de `x90C0E0` dans `STATE_EAST_SWITZERLAND`. Aucun remplacement de fichier complet n’est autorisé.

## 14. Histoire des pays

AUS, CRO et SWI sont identiques fork/hotfix. Leur contenu 1776 est `ALREADY_MERGED_EQUIVALENT`; aucune suppression de CRO ou modification de lois/technologies n’est prouvée.

## 15. Diplomatie et sujets

`00_relations.txt` est identique fork/hotfix. Dans `00_subject_relationships.txt`, le hotfix supprime exactement deux blocs AUS→CRO : `crown_land` et `decrease_payments`. Ces suppressions sont requises si CRO est absorbée; les autres sujets AUS restent inchangés.

## 16. Bâtiments et formations

Les blocs Croatia/Slavonia de `01_south_europe.txt` re-cléent CRO vers AUS sans changer PMs, tailles ou ownership HUN. Le hotfix ajoute séparément un shipyard Croatia; celui-ci est `NAVY_PROTECTED`. `00_military_formations_europe.txt` possède sept commits NAVY postérieurs à l’import : le hotfix ajoute une flotte AUS 3 ships-of-the-line/6 frigates, supprime le bloc CRO et recrée Agram sous AUS avec types et comptes différents. Aucun import de ce bloc n’est sûr sans résolution NAVY.

## 17. Événements, décisions et journaux

Les événements autrichiens où hotfix=vanilla mais fork diffère sont des adaptations 1776 à préserver. `05_austrian_fascism.txt` reste `UNVERIFIED` pour une revue JE globale ultérieure, sans lien prouvé avec les annonces territoriales. Les décisions autrichiennes sont fournies par vanilla et ne requièrent aucun override.

## 18. Cartes et régions stratégiques

Le fork et le hotfix n’override pas `map_data/state_regions/00_west_europe.txt` ni `common/strategic_regions/europe_strategic_regions.txt`; vanilla 1.13 les fournit. `x90C0E0` est déjà dans `STATE_EAST_SWITZERLAND`. Croatia/Slavonia restent dans la région Balkans et les deux Swiss states dans South Germany; aucun hunk cartographique n’est requis.

## 19. Localisations

La localisation anglaise Austria est identique fork/hotfix. La française est fork-only et protégée. Les changements d’owner et de region_state n’introduisent aucune clé.

## 20. Adaptations 1776

Préserver les définitions pays communes au fork/hotfix, les relations communes, les événements/JE adaptés, toutes les cultures et tailles de pops Croatia/Slavonia, les PMs, les owners HUN et tous les autres blocs de `00_states.txt`.

## 21. Adaptations vanilla 1.13

Conserver l’héritage des cartes, régions stratégiques et décisions. Une égalité hotfix/vanilla n’autorise aucun remplacement des overrides 1776.

## 22. Chevauchements NAVY

Le shipyard Croatia et toute modification de `00_military_formations_europe.txt` sont protégés. La flotte annoncée est réelle, mais doit être reconstruite contre l’architecture NAVY actuelle, pas copiée depuis le hotfix.

## 23. Chevauchements ADMIN

Le bloc Croatia contient une administration gouvernementale et le fichier buildings porte des historiques navals locaux. Les re-clés d’owner sont prouvées, mais aucun PM ADMIN ne doit changer.

## 24. Chevauchements concurrents

MARATH/SAT/KHP, BIC, Travancore, Inde, Japon, Mamluk Iraq, Russie et `docs/research/technology/` n’intersectent aucun hunk territorial identifié. Le stash MARATH n’a pas été inspecté ni appliqué.

## 25. Hunks requis

Requis après résolution des deux bloqueurs : trois hunks state; deux suppressions de pactes; re-clés Croatia/Slavonia dans buildings; deux re-clés de pops. Chaque hunk possède ancres, valeurs et rollback ciblé dans la delta map.

## 26. Hunks déjà intégrés

Les fichiers pays AUS/CRO/SWI, les relations générales et la localisation anglaise sont déjà identiques à la source hotfix. Les blocs buildings suisses inspectés sont identiques fork/hotfix.

## 27. Hunks obsolètes

Aucun hunk territorial annoncé n’est obsolète. Les copies de cartes, strategic regions et décisions seraient inutiles car vanilla 1.13 les fournit déjà.

## 28. Hunks non vérifiés

Deux bloqueurs : ajout net de 30 000 South Germans dans la portion AUS de East Switzerland; migration Agram/flotte/shipyard avec types, comptes et ownership différents au sein de fichiers NAVY protégés. `05_austrian_fascism.txt` reste non vérifié mais relève d’une autre revue et ne bloque pas ce paquet territorial.

## 29. Plan de correction minimal

Ne corriger qu’après 6A.2R. Ordre : résoudre population suisse et architecture NAVY; appliquer les trois hunks states; re-cléer les pops; re-cléer les buildings sans toucher aux PMs; supprimer les deux pactes CRO; appliquer seulement les hunks NAVY explicitement approuvés; vérifier références CRO/AUS et accolades; préparer un runtime unique.

## 30. Besoin de runtime

Oui après correction complète, en un lancement consolidé : ownership des trois portions, continuité/autonomie AUS, disparition fonctionnelle du sujet CRO, populations, bâtiments, accès côtier, absence d’erreurs de formations, puis logs. Aucun runtime pendant 6A.2.

## 31. Ordre des futures corrections

`HOTFIX_6A2R_TARGET_HUNK_RESOLUTION` d’abord; correction territoriale seulement ensuite; DEI reste la revue probable après clôture de ce paquet.

## 32. Risques

Inflation de population suisse, armée CRO orpheline, duplication ou régression de flotte, collision NAVY/ADMIN, remplacement massif de `00_states.txt`, perte d’owners HUN ou de PMs, et confusion East/West Switzerland.

## 33. Fichiers créés

Le présent rapport et `HOTFIX_6A2_AUSTRIA_CROATIA_WEST_SWITZERLAND_DELTA_MAP.csv` seulement, plus les mises à jour documentaires autorisées.

## 34. Confirmation gameplay inchangé

Aucun fichier gameplay, harnais, localisation gameplay, descripteur ou sauvegarde n’a été modifié.

## 35. Confirmation blocs clos

Russie, Mamluk Iraq, Japon et Inde n’ont pas été modifiés. Le fichier Russie reste celui du commit `991f6a1`.

## 36. Confirmation docs/research/technology/

Répertoire non suivi préexistant, intact et hors périmètre.

## 37. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` intact; aucun apply, pop ou drop.

## 38. Verdict

- `AUSTRIA_CROATIA_WEST_SWITZERLAND_AUDIT_COMPLETE`
- `BLOCKED_TARGET_HUNKS_UNVERIFIED`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
