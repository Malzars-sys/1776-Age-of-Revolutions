# HOTFIX-5C2E4C1F - Préparation statique du test Sepoy A-2

## 1. Résumé

Cette phase prépare uniquement, dans la copie jetable, un scénario A-2 destiné à tester l'option `sepoy_mutiny_events.2.a` lorsqu'un state BIC admissible à la redistribution générique n'a aucun receveur voisin valide. Le témoin retenu est la portion principale de `STATE_CEYLON`. Deux mutations manuelles et jetables suffisent. Aucun jeu, launcher ou événement Sepoy n'a été lancé pendant cette phase.

## 2. État Git initial

- Racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD : `0b23d4f Complete Sepoy A1 runtime observations`, qui contient la clôture HOTFIX-5C2E4C1E1.
- Aucun fichier suivi n'était modifié.
- `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` était présent.
- Aucun processus Victoria 3, Paradox Launcher ou dowser n'était actif.

## 3. Exception `docs/research/technology/`

`git status --short` affichait uniquement `?? docs/research/technology/`. Cette exception concurrente autorisée n'a été ni lue pour produire le harnais, ni créée, ni modifiée, ni supprimée.

## 4. Vérification de la copie

Avant création, `1776_Age_of_Revolutions_sepoy_test` existait et contenait exactement 952 fichiers, sans `.git`, sans `remote_file_id`, avec les quatre fichiers du harnais racine et les quatre fichiers A-1. Aucun fichier A-2 n'existait. Les huit hashes de contrôle correspondaient aux valeurs A-1 enregistrées. Les deux fichiers Sepoy de la copie correspondaient octet pour octet au fork.

## 5. Analyse exacte de la boucle générique 2.a

Le fork et la copie ont le même event hash `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7`. Le hotfix et la vanilla ont ensemble le hash `14FE5650F573AA6E3AA8C3DA25B94F74F44DF2A3917B0F9DB7DBA5E84085E638`. Les différences locales concernent notamment le portage régional, mais le mécanisme générique reste le même.

Avant la boucle, 2.a traite explicitement Pegu, Gujarat, Tenasserim, Travancore, Circars, Kurnool, Delhi, Agra, Awadh, Central Provinces et Bombay. La boucle ne considère ensuite qu'un state BIC situé dans une zone indienne admise et possédant au moins un state voisin dont le propriétaire :

1. a une culture primaire du groupe d'héritage sud-asiatique ;
2. a sa capitale dans une zone de capitale admise.

Pour chaque pays admissible, `random_scope_state` cherche un state BIC admissible qui touche ce pays, puis `set_state_owner` le lui transfère. Le flux exact est donc :

```text
state BIC admissible
-> transfert prioritaire éventuel
-> voisin admissible présent ?
   -> oui : le state peut être sélectionné et transféré au receveur
   -> non : le state n'entre pas dans la garde de la boucle
-> répétition tant qu'au moins un autre state BIC possède un receveur
-> annexion finale du reliquat BIC par GBR si BIC est toujours son sujet
```

## 6. Comportement prévu en absence de receveur

L'absence de receveur ne provoque pas une sélection vide dans la boucle : le state sans receveur ne satisfait pas la garde `any_scope_state` et n'est donc pas candidat à `random_scope_state`. La boucle continue pour les autres states, puis s'arrête lorsqu'aucun state BIC redistribuable ne possède encore de voisin admissible. Le témoin reste alors à BIC jusqu'au bloc final `c:GBR ?= { annex = root }`. Il n'y a donc pas de raison statique d'attendre une boucle infinie.

## 7. Candidats étudiés

La topologie a été recalculée à partir de `provinces.png`, de `adjacencies.csv` et de l'ownership 1776 du fork.

| State | Receveurs valides baseline ou émergents | Priorité | Mutations nécessaires | Risque | Décision |
|---|---|---:|---:|---|---|
| `STATE_BUNDELKHAND` | MARATH (marathi, capitale Bombay) et NAG (marathi, capitale Central Provinces) | Non | Au moins 2 | Deux frontières NAG distinctes et voisin MARATH dans le state divisé | Rejeté |
| `STATE_BIHAR` | NAG est valide ; NEP a une culture sud-asiatique mais sa capitale himalayenne échoue au filtre. Awadh et Bundelkhand peuvent cependant devenir des voisins valides pendant 2.a | Non | Plus de 3 pour une isolation stable | La topologie change pendant les transferts prioritaires et génériques | Rejeté |
| `STATE_EAST_BENGAL` | COO, KKI, MGH, NGA et TIP sont des voisins potentiels ; leurs capitales East Bengal/Assam sont dans le nord de l'Inde | Non | Plus de 3 | Trop de receveurs et un bord de carte non propriétaire | Rejeté |
| `STATE_CEYLON` | PUD est l'unique receveur après création du témoin BIC | Non | 2 au total | PUD devient temporairement sans state ; acceptable seulement dans une sauvegarde jetable | Retenu |

## 8. State témoin retenu

`STATE_CEYLON` est retenu. Il est dans `region_south_india`, n'apparaît dans aucun transfert prioritaire de 2.a et sa portion principale n'a qu'une seule liaison de state vers le continent. L'isolation ne dépend donc pas de l'ordre aléatoire des autres redistributions.

## 9. Topologie initiale

Dans le setup 1776 :

- DEI possède les 13 provinces de l'île principale, dont `x8D6FA8` ;
- MLD possède `x95AAA3` ;
- GBR possède `x5B5C22` ;
- PUD possède 24 provinces de `STATE_MADRAS`, dont `x99B424`.

La liaison explicite attestée dans la vanilla est `x99B424;x8D6FA8;sea` dans `map_data/adjacencies.csv`. Les portions MLD et GBR de Ceylan ne touchent pas le bloc principal DEI dans le graphe de provinces. Les couleurs de carte sans owner rencontrées sur le pourtour sont des surfaces non étatiques et ne peuvent pas être des receveurs.

## 10. Receveurs valides initiaux

Pour le témoin après son transfert préparatoire à BIC mais avant neutralisation, le seul voisin propriétaire est PUD via sa portion de Madras. PUD a la culture primaire `tamil`, rattachée au groupe sud-asiatique, et sa capitale est `STATE_MADRAS` dans `region_south_india`. Il satisfait donc les deux filtres et constitue exactement un receveur valide.

## 11. Mutations proposées

L'option explicite de préparation exécute uniquement :

```text
s:STATE_CEYLON.region_state:DEI -> c:BIC
s:STATE_MADRAS.region_state:PUD -> c:GBR
```

La première mutation crée le témoin BIC. La seconde remplace l'unique propriétaire voisin admissible par GBR, dont les cultures primaires sont `british` et `scottish` et dont la capitale est `STATE_HOME_COUNTIES`.

## 12. Justification du nombre de mutations

Deux mutations sont nécessaires et suffisantes : une pour créer le témoin dans un state isolé et une pour neutraliser son unique receveur. Le maximum autorisé de trois n'est pas atteint. Aucun pays, culture, capitale, sujet, marqueur supplémentaire ou fichier source n'est modifié.

## 13. Topologie après préparation

Après confirmation manuelle :

- la portion DEI de Ceylan est une portion BIC ;
- la portion PUD de Madras est une portion GBR ;
- les portions FRA et DENNOR de Madras restent inchangées ;
- les portions MLD et GBR préexistantes de Ceylan restent inchangées ;
- la seule liaison étatique du témoin pointe vers une portion possédée par GBR.

## 14. Preuve de zéro receveur valide

| Voisin du témoin | Tag | Culture primaire | Heritage | Capitale | Condition échouée | Invalidité attestée |
|---|---|---|---|---|---|---|
| Portion de Madras après setup | GBR | british, scottish | britannique, hors groupe sud-asiatique | `STATE_HOME_COUNTIES` | Culture et capitale | Oui |
| Portion MLD de Ceylan | MLD | sinhala | sud-asiatique | `STATE_CEYLON` | Pas voisine du bloc principal dans le graphe | Oui |
| Portion GBR préexistante de Ceylan | GBR | british, scottish | britannique | `STATE_CEYLON` comme localisation de portion, mais capitale pays à Home Counties | Pas voisine du bloc principal et culture invalide | Oui |

La décision d'ouverture impose en plus qu'aucun `any_neighbouring_state` du témoin n'ait un owner doté d'une culture primaire du groupe sud-asiatique. Cette condition est plus stricte que le filtre complet de 2.a : si elle passe, aucun receveur valide ne peut subsister, quelle que soit sa capitale.

## 15. Traitement attendu avant annexion

Le témoin BIC est dans `region_south_india`, mais ne satisfait pas la garde de la boucle faute de voisin culturellement admissible. Aucun transfert prioritaire ne vise Ceylan. Le témoin doit donc rester à BIC pendant que les autres states suivent leur comportement normal.

## 16. Traitement attendu après annexion GBR

Une fois la redistribution terminée, BIC reste sujet de GBR. Le bloc final joue GBR puis annexe `root`. La portion témoin de Ceylan, encore détenue par BIC, doit alors passer à GBR avec le reste du reliquat. Aucun owner nul ne doit apparaître.

## 17. Namespace et identifiants

Le namespace est `zz_sepoy_test_a2`. Les décisions sont `zz_sepoy_test_a2_prepare` et `zz_sepoy_test_a2_open_event`, l'event est `zz_sepoy_test_a2.1`, et l'unique marqueur country-scoped est `zz_sepoy_test_a2_ready`. Une recherche dans le fork, la copie hors nouveaux fichiers et la vanilla a retourné zéro conflit.

## 18. Décision de préparation

La décision de préparation est visible uniquement pour le joueur BIC, exige `is_player = yes`, `c:BIC ?= this`, l'absence du marqueur, la relation de sujet avec GBR, l'existence de COO/JEY et les deux portions sources DEI/PUD. Son clic ouvre seulement `zz_sepoy_test_a2.1`; aucune mutation ne se trouve dans `when_taken`. La chance IA vaut zéro.

## 19. Event de préparation

`zz_sepoy_test_a2.1` répète les préconditions et contient exactement deux options. L'option explicite applique les deux `set_state_owner`, puis `set_variable = zz_sepoy_test_a2_ready`. L'option d'annulation ne contient aucun effet. Aucun autre marqueur ou variable n'est utilisé.

## 20. Préconditions de la décision d'ouverture

La décision d'ouverture vérifie : joueur BIC, marqueur prêt, BIC sujet de GBR, COO et JEY existants, portion BIC de Ceylan existante et possédée par `root`, portion GBR de Madras existante, ancienne portion PUD absente, témoin dans `region_south_india`, et absence de tout voisin propriétaire à culture primaire sud-asiatique. Ceylan n'étant pas cité dans les transferts prioritaires, son absence de priorité est structurelle.

L'event réel n'est référencé qu'une fois dans les quatre fichiers. Un second marqueur d'appel était interdit ; la procédure impose donc un clic unique. Après 2.a, BIC est annexée et le pays joué devient GBR, ce qui rend naturellement les décisions BIC indisponibles.

## 21. Décision d'ouverture

`zz_sepoy_test_a2_open_event` n'est visible que pour le joueur BIC prêt. Elle répète les conditions essentielles, a une chance IA nulle, ne contient aucune mutation et appelle uniquement `sepoy_mutiny_events.2` sur le scope BIC courant.

## 22. Sécurité de l'appel à l'event 2

Il n'existe aucun appel au chargement ni dans l'event de préparation. Le seul appel se trouve dans le clic manuel de la décision d'ouverture. Les events Sepoy suivants ne sont pas référencés. Les fichiers sources Sepoy ne sont pas modifiés.

## 23. Absence de choix automatique

Le harnais ne contient aucun effet de sélection d'option. Le joueur devra choisir manuellement et exclusivement l'option 2.a lors de la future phase runtime. Les recherches de termes de sélection automatique ont retourné zéro occurrence.

## 24. Exemples syntaxiques

- `exists = s:STATE_*.region_state:TAG` est attesté dans la vanilla, notamment `common/scripted_effects/00_sepoy_mutiny_scripted_effects.txt`.
- `s:STATE_*.region_state:TAG = { set_state_owner = c:TAG }` est attesté dans la vanilla et dans `sepoy_mutiny_events.2.a` du fork.
- `owner = root`, `region = sr:region_south_india`, `any_neighbouring_state` et `has_discrimination_trait_group = heritage_group_south_asian` sont attestés dans les scripts vanilla 1.13.

Le scope root est BIC. Le premier scope state cible la portion DEI de Ceylan, le second la portion PUD de Madras. Chaque effet change uniquement l'owner de cette portion et n'est exécuté qu'après confirmation manuelle dans l'event de préparation.

## 25. Localisations EN/FR

Les dix clés requises existent une fois en anglais et une fois en français. Les textes avertissent du scénario sans receveur, des deux mutations jetables, de Ceylan comme témoin, de l'annulation avant effet, du caractère destructif de l'event réel, du choix manuel exclusif de 2.a, du passage attendu à GBR, de la baseline à préserver et de l'interdiction d'utiliser la sauvegarde A-1.

## 26. Contrôles BOM

Les quatre fichiers A-2 commencent par `EF BB BF`, sont des UTF-8 valides, utilisent uniquement LF et contiennent zéro octet CR. Tailles et hashes après normalisation :

| Fichier | Taille | SHA-256 |
|---|---:|---|
| décision A-2 | 1399 | `1F11BDB7CD2F59EDF220E320AD996A11C44F143D9C99F7DAEE5913B7C1E571A2` |
| event A-2 | 1169 | `71EC607B1AA2290A429D02AB479B19A84EA54F0A7FF72FB19D0B96C8041B65FB` |
| localisation EN | 1407 | `882ED5B6B51095923FB614F27E03944C04DA25F3A236CC56685000D8154A8EF9` |
| localisation FR | 1546 | `0C50B823D8E96B8C4DF3F44E96A13F2010967ED307DF858AB0298BB20AEC630A` |

## 27. Termes interdits

La recherche sur les quatre fichiers A-2 retourne zéro occurrence pour tous les termes interdits : events `.3`/`.4`, journal entries Sepoy, effets de radicaux/loyaux, ajout/retrait de journal entry, création de pays, hasard, boucle, West Bengal, Bombay, région himalayenne, Pashtunistan et Quetta. La mention de Ceylan, témoin autorisé, est présente.

## 28. Validation statique

- Accolades : 21/21 dans les décisions et 9/9 dans l'event.
- Deux décisions, un event, exactement deux options.
- Deux appels de mutation, tous deux dans l'option explicite de préparation.
- Un seul appel à `sepoy_mutiny_events.2`.
- Zéro sélection automatique.
- Dix clés EN et dix clés FR, toutes uniques.
- Namespace unique et commentaire de sécurité présent dans les deux scripts.
- Copie après création : exactement 956 fichiers.

## 29. Résumé du manifest

Le manifest contient 21 lignes de données : quatre créations A-2, huit contrôles des anciens harnais, quatre contrôles Sepoy fork/copie, trois contrôles descriptor/marqueur/launcher et deux livrables C1F. Le hash de la ligne décrivant le manifest lui-même est indiqué comme auto-référentiel et n'est pas enregistré dans son propre contenu.

## 30. Procédure runtime suivante

1. Utiliser uniquement la copie jetable et un playset ne contenant qu'elle.
2. Démarrer une nouvelle partie BIC 1776 ; ne pas charger A-1.
3. Créer une nouvelle sauvegarde baseline A-2 et ne jamais l'écraser.
4. Cliquer `Préparer le test de redistribution Sepoy A-2`.
5. Lire l'event, puis confirmer l'option de préparation.
6. Vérifier toutes les observations de la section 31.
7. Sauvegarder sous un nouveau nom jetable.
8. Cliquer une seule fois la décision d'ouverture.
9. Choisir manuellement uniquement l'option 2.a.
10. Vérifier la section 32, laisser passer au moins un jour, quitter proprement, puis analyser les logs.

## 31. Observations obligatoires avant 2.a

- BIC possède la portion principale de Ceylan.
- La portion de Madras anciennement PUD appartient à GBR.
- BIC est toujours sujet de GBR.
- COO et JEY existent encore.
- Aucun event Sepoy réel ne s'est ouvert automatiquement.
- La décision d'ouverture est visible et disponible.
- Les autres territoires et relations n'ont pas changé hors des deux mutations documentées.

## 32. Observations obligatoires après 2.a

- L'event se ferme sans blocage et le jeu reste actif.
- Le pays joué devient GBR.
- BIC est annexée conformément au flux de 2.a.
- La portion témoin de Ceylan appartient à GBR, jamais à un owner nul.
- Elle n'a pas été transférée à PUD ou à un autre prince pendant la boucle.
- Les autres redistributions normales de 2.a restent possibles.
- Aucun crash et aucune nouvelle erreur ciblant A-2 ou `sepoy_mutiny_events.2` dans les logs.

## 33. Risques restants

La mutation de la portion PUD de Madras peut laisser PUD sans territoire ; ce comportement est volontairement limité à la sauvegarde jetable et aucune destruction explicite de pays n'est appelée. Le test de voisinage dépend du graphe runtime, même si la topologie statique ne montre qu'une liaison. L'absence de second marqueur impose de respecter la procédure de clic unique. Enfin, le test ne valide que 2.a et ne doit servir à aucune autre option.

## 34. Verdict

**READY_FOR_A2_RUNTIME_TEST**

Le témoin est isolé, le nombre de receveurs valides après préparation est zéro, deux mutations suffisent, les scripts sont statiquement cohérents, l'event 2 n'est appelé qu'une fois et manuellement, aucune option n'est automatisée et les sources Sepoy restent inchangées.

## 35. Liste exacte des fichiers créés dans la copie

1. `common/decisions/zz_sepoy_functional_test_a2.txt`
2. `events/zz_sepoy_functional_test_a2_events.txt`
3. `localization/english/zz_sepoy_functional_test_a2_l_english.yml`
4. `localization/french/zz_sepoy_functional_test_a2_l_french.yml`

## 36. Liste exacte des fichiers créés dans le fork

1. `docs/reports/hotfix/HOTFIX_5C2E4C1F_SEPOY_A2_STATIC_SETUP.md`
2. `docs/reports/hotfix/HOTFIX_5C2E4C1F_A2_HARNESS_MANIFEST.csv`

## 37. Confirmation que les fichiers Sepoy sont inchangés

Les hashes fork et copie sont identiques :

- `common/journal_entries/04_sepoy_mutiny.txt` : `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` ;
- `events/india_events/sepoy_mutiny_events.txt` : `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7`.

## 38. Confirmation que les anciens harnais sont inchangés

Les huit fichiers racine/A-1 conservent leurs hashes de contrôle : `E8CC...20FF`, `E69B...56EE`, `93BF...A6EF`, `59EA...C87`, `7464...E3A1`, `8256...523A`, `3A0A...63E9` et `791F...20B3`. Aucun n'a été modifié.

## 39. Confirmation que `docs/research/technology/` est intact

Ce dossier demeure l'unique exception concurrente non suivie. Aucun de ses sept fichiers n'a été créé, lu, modifié, supprimé ou ajouté à Git par cette phase.

## 40. Confirmation que le stash MARATH est intact

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est toujours présent. Aucun `stash pop`, `stash apply`, inspection de contenu ou changement MARATH n'a été effectué.
