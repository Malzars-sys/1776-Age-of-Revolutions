# HOTFIX-5C2E4C1H - Préparation statique Sepoy A-3

## 1. Résumé

Cette phase prépare exclusivement un harnais jetable A-3 pour observer la redistribution générique de l'option `sepoy_mutiny_events.2.a` lorsqu'une portion BIC possède exactement deux receveurs voisins valides. Le témoin retenu est la portion BIC de `STATE_BUNDELKHAND`. Les deux seuls receveurs admissibles sont `MARATH` (Confédération marathe) et `NAG` (Nagpur).

La baseline 1776 fournit déjà cette topologie. Aucune mutation territoriale n'est nécessaire : l'option de préparation pose uniquement le marqueur country-scoped `zz_sepoy_test_a3_ready`. Le jeu et le launcher n'ont pas été lancés.

## 2. État Git initial

- Racine Git : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- Commit de tête observé : `15b866a Validate Sepoy no-receiver runtime`, correspondant à HOTFIX-5C2E4C1G.
- Aucun fichier suivi n'était modifié.
- Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` était présent et n'a pas été manipulé.

## 3. Exception docs/research/technology/

Les sept fichiers non suivis déjà présents sous `docs/research/technology/` constituaient l'unique exception concurrente autorisée. Ils n'ont été ni lus pour produire le harnais, ni modifiés, déplacés ou ajoutés à Git.

## 4. Vérification de la copie

Avant création, la copie jetable :

- existait et contenait exactement 956 fichiers ;
- ne contenait aucun dossier `.git` ;
- ne contenait aucune occurrence de `remote_file_id` ;
- contenait les quatre fichiers racine, les quatre fichiers A-1 et les quatre fichiers A-2 ;
- ne contenait aucun fichier A-3 ;
- conservait les douze hashes consignés dans le manifest A-2 ;
- conservait les fichiers Sepoy identiques au fork.

Hashes contrôlés :

| Fichier | SHA-256 |
|---|---|
| `common/journal_entries/04_sepoy_mutiny.txt` | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` |
| `events/india_events/sepoy_mutiny_events.txt` | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` |

## 5. Analyse de la boucle générique

Les blocs de l'option 2.a sont identiques ligne pour ligne dans le fork, la copie, le hotfix et la vanilla 1.13. Le traitement observé est :

1. exécuter les transferts prioritaires de Madras, Mandalay/Pégou, Gujarat, Tenasserim, Travancore, Circars septentrionaux, Kurnool, Delhi/Agra/Awadh, Central Provinces et Bombay lorsqu'ils sont applicables ;
2. rechercher ensuite les portions encore détenues par la racine BIC dans `region_north_india`, `region_south_india` et certaines zones périphériques ;
3. exiger qu'au moins un state voisin appartienne à un pays ayant une culture primaire du groupe d'héritage sud-asiatique et une capitale dans une zone admise ;
4. parcourir les pays receveurs admissibles, sauvegarder chacun dans `scope:prince_scope`, puis choisir un state racine admissible au moyen de `random_scope_state` ;
5. transférer le state choisi avec `set_state_owner = scope:prince_scope` ;
6. répéter tant qu'une portion BIC admissible possède encore un voisin admissible ;
7. faire jouer GBR puis annexer le reliquat BIC.

`any_neighbouring_state` ne choisit pas le receveur : il établit l'existence d'une frontière entre le state candidat et un state possédé par un pays qui passe les filtres. Le hasard visible vient de `random_scope_state` pour chaque pays admissible, combiné à l'ordre dans lequel les autres portions BIC cessent d'être disponibles. Ce n'est pas un tirage uniforme explicite entre deux tags.

Pseudo-flux du témoin :

```text
portion BIC de STATE_BUNDELKHAND
-> aucun transfert prioritaire
-> voisins valides = MARATH et NAG uniquement
-> sélection par le traitement générique
-> un transfert vers un seul des deux tags
-> owner final unique
-> poursuite de la boucle pour les autres states BIC
-> annexion finale du reliquat BIC par GBR
```

## 6. Définition fonctionnelle d'A-3

A-3 vérifie qu'un state témoin traité par la redistribution générique termine avec un owner appartenant à l'ensemble fermé `{ MARATH, NAG }`. Le test ne demande pas d'obtenir une distribution 50/50 sur cinq essais. Il exige que chaque résultat soit l'un des deux tags autorisés, jamais un troisième tag, BIC ou un owner nul.

## 7. States candidats

| State | Receveurs valides initiaux | Receveurs émergents possibles | Mutation 1 | Mutation 2 | Mutation 3 | Nombre final attendu | Risque | Décision |
|---|---|---|---|---|---|---:|---|---|
| `STATE_BUNDELKHAND` | MARATH, NAG | Aucun nouveau voisin requis | Aucune | Aucune | Aucune | 2 | Faible | Retenu |
| `STATE_BIHAR` | NAG au minimum | Awadh et Bundelkhand peuvent changer d'owner avant son traitement | Plusieurs seraient nécessaires | Plusieurs | Plusieurs | Instable | Élevé | Rejeté |
| `STATE_EAST_BENGAL` | COO, KKI, MGH, NGA, TIP potentiels | D'autres owners des states divisés voisins | Plus de trois nécessaires | - | - | Supérieur à 2 | Élevé | Rejeté |
| `STATE_CEYLON` | PUD avant A-2, zéro après A-2 | Pas de second receveur stable sans construction supplémentaire | Transférer DEI à BIC | Ajouter un second voisin | Neutraliser les autres selon le montage | Incertain | Moyen/élevé | Rejeté |
| `STATE_AWADH` | Non pertinent pour A-3 | MUG via le bloc prioritaire | - | - | - | Capturé avant la boucle | Élevé | Rejeté |

## 8. State témoin retenu

Le témoin est `s:STATE_BUNDELKHAND.region_state:BIC`. Il contient sept provinces BIC dans l'historique 1776 : `x66337F`, `x6B7184`, `x7884D6`, `x52001D`, `x4605A8`, `xD64336` et `x5CBFF7`.

Il appartient à `region_north_india`, n'est cité dans aucun bloc prioritaire de 2.a et entre donc exclusivement dans la redistribution générique.

## 9. Topologie baseline

Les frontières de provinces attestent :

- BIC vers MARATH dans le state divisé Bundelkhand : `x5CBFF7-xD0F986` et `x5CBFF7-x0E5FEA` ;
- BIC vers NAG dans Central Provinces : notamment `x4605A8-x471CDC`, `x4605A8-x4A2157`, `x66337F-x471CDC` et `x66337F-x78E85C` ;
- BIC vers NAG dans Malwa : notamment `x66337F-x404EEA`, `x66337F-xBAE4B3` et `x66337F-xFBF096`.

Les autres frontières de la portion témoin mènent à des portions possédées par BIC dans Bihar/Awadh ou à d'autres provinces internes du témoin. Elles ne créent pas un troisième pays receveur.

## 10. Receveurs valides initiaux

| Tag | Nom | Portion voisine | Culture primaire | Héritage | Groupe | Capitale | Région de capitale | Valide |
|---|---|---|---|---|---|---|---|---|
| `MARATH` | Confédération marathe | portion MARATH de Bundelkhand | marathi | `heritage_deccani` | `heritage_group_south_asian` | `STATE_BOMBAY` | South India | Oui |
| `NAG` | Nagpur | Central Provinces et Malwa | marathi | `heritage_deccani` | `heritage_group_south_asian` | `STATE_CENTRAL_PROVINCES` | North India | Oui |

`valid_receivers_before = 2`.

## 11. Mutations proposées

Aucune mutation territoriale n'est proposée. La préparation effectue uniquement :

```text
set_variable = zz_sepoy_test_a3_ready
```

Cette variable marque la session jetable comme prête. Elle ne modifie ni pays, state, culture, capitale, sujet, relation ni journal entry.

## 12. Justification du nombre de mutations

Le nombre de mutations territoriales est `0`, inférieur au maximum absolu de trois. Ajouter un transfert artificiel aurait dégradé une baseline qui satisfait déjà toutes les préconditions. Le marqueur technique n'est pas compté comme mutation territoriale dans le manifest, conformément aux manifests A-1/A-2 qui comptaient les effets de propriété et non leur marqueur de disponibilité.

## 13. RECEIVER_A

`RECEIVER_A = MARATH`, Confédération marathe.

- Frontière : portion MARATH du même `STATE_BUNDELKHAND`, attestée par deux paires de provinces.
- Culture : marathi.
- Héritage : `heritage_deccani`.
- Groupe : `heritage_group_south_asian`.
- Capitale : `STATE_BOMBAY`, dans `region_south_india`.
- Condition complète : voisin, héritage valide, capitale valide et pays distinct de NAG.

## 14. RECEIVER_B

`RECEIVER_B = NAG`, Nagpur.

- Frontière : portions NAG de `STATE_CENTRAL_PROVINCES` et `STATE_MALWA`, avec plusieurs paires de provinces indépendantes.
- Culture : marathi.
- Héritage : `heritage_deccani`.
- Groupe : `heritage_group_south_asian`.
- Capitale : `STATE_CENTRAL_PROVINCES`, dans `region_north_india`.
- Condition complète : voisin, héritage valide, capitale valide et pays distinct de MARATH.

## 15. Invalidité de tous les autres voisins

| Voisin | Tag | Culture | Héritage | Capitale | Condition échouée | Pourquoi il n'est pas un troisième receveur |
|---|---|---|---|---|---|---|
| Autres portions BIC de Bihar/Awadh | BIC | british/scottish | européen | West Bengal | héritage sud-asiatique | Même owner que le témoin et culture primaire invalide |
| Provinces internes du témoin | BIC | british/scottish | européen | West Bengal | pays externe et héritage | Ne constituent pas un voisin country distinct |
| Toute surface sans owner | aucun | aucune | aucune | aucune | owner requis | Impossible à sélectionner comme pays receveur |

Le harnais ne repose pas uniquement sur cet inventaire statique : il exige MARATH et NAG avec tous leurs filtres, puis interdit explicitement tout autre owner voisin qui satisferait simultanément le filtre culturel et le filtre de capitale.

## 16. Topologie finale

Après préparation, la topologie territoriale est identique à la baseline. Seul le marqueur `zz_sepoy_test_a3_ready` existe sur BIC. Les deux receveurs restent MARATH et NAG.

## 17. Preuve de deux receveurs exacts

La syntaxe locale ne fournit pas ici un compteur fiable et attesté de pays owners uniques derrière `any_neighbouring_state`. La décision applique donc la stratégie de repli autorisée :

1. présence explicite d'un voisin MARATH passant les filtres ;
2. présence explicite d'un voisin NAG passant les filtres ;
3. absence explicite de tout voisin dont l'owner est différent de MARATH/NAG et passe les mêmes filtres.

Le fait que NAG touche le témoin par plusieurs portions ou frontières ne le compte pas plusieurs fois : il reste un seul tag receveur. Résultat attendu : `valid_receivers_after = 2` exactement.

## 18. Stabilité de la topologie

La topologie est stable jusqu'au transfert du témoin :

- aucun transfert prioritaire ne vise Bundelkhand ;
- la boucle ne transfère que les portions dont l'owner est la racine BIC, donc elle ne retire aucun territoire à MARATH ou NAG ;
- les portions MARATH de Bundelkhand et NAG de Central Provinces/Malwa restent physiquement adjacentes ;
- les transferts prioritaires peuvent renforcer NAG mais ne suppriment aucune de ses frontières existantes ;
- les capitales Bombay et Central Provinces ne sont pas déplacées par 2.a ;
- COO et JEY restent exigés avant l'ouverture ;
- l'annexion de BIC par GBR intervient après la boucle.

L'ordre des autres states peut modifier d'autres voisins BIC, mais ne peut supprimer les deux frontières fixes ni créer un troisième owner admissible sur une frontière du témoin avant son transfert.

## 19. Résultat attendu pour chaque exécution

Pour chaque répétition :

- owner final autorisé : `MARATH` ou `NAG` ;
- owner final interdit : BIC, GBR, tout troisième pays ou aucun owner ;
- une seule portion témoin est observée ;
- le transfert ne doit s'exécuter qu'une fois ;
- la boucle doit se terminer et le jeu doit rester actif.

## 20. Namespace et identifiants

- Namespace : `zz_sepoy_test_a3`.
- Décisions : `zz_sepoy_test_a3_prepare`, `zz_sepoy_test_a3_open_event`.
- Event : `zz_sepoy_test_a3.1`.
- Marqueur : `zz_sepoy_test_a3_ready`.
- Dix clés de localisation conformes à la liste prescrite.

La recherche dans fork, copie et vanilla ne trouvait aucune occurrence A-3 avant création.

## 21. Décision de préparation

La décision de préparation :

- est visible seulement pour un joueur BIC ;
- exige l'absence du marqueur ;
- vérifie GBR, COO, JEY, MARATH, NAG et le témoin ;
- vérifie les deux receveurs et l'absence de troisième receveur ;
- a une chance IA nulle ;
- ouvre seulement `zz_sepoy_test_a3.1` ;
- n'effectue aucune mutation dans `when_taken`.

## 22. Event de préparation

L'event country-scoped contient exactement deux options :

1. préparer, sans mutation territoriale, puis poser `zz_sepoy_test_a3_ready` ;
2. annuler sans aucun effet.

Il n'appelle aucun event Sepoy réel.

## 23. Préconditions de l'ouverture

La décision d'ouverture répète directement : joueur BIC, marqueur, sujet de GBR, COO/JEY existants, MARATH/NAG existants, portion BIC de Bundelkhand, North India, MARATH valide voisin, NAG valide voisin et absence de tout autre owner voisin valide.

L'absence de transfert prioritaire est garantie par l'identité même de `STATE_BUNDELKHAND`, absent de la liste fermée des blocs prioritaires identiques dans les quatre sources comparées.

## 24. Décision d'ouverture

`zz_sepoy_test_a3_open_event` n'effectue aucune mutation. Son unique effet est :

```text
trigger_event = { id = sepoy_mutiny_events.2 popup = yes }
```

L'appel se fait sur le scope country BIC courant.

## 25. Sécurité de l'appel à l'event 2

Un seul appel à `sepoy_mutiny_events.2` est présent dans les quatre nouveaux fichiers. Il n'est accessible qu'après la préparation explicite et la validation des préconditions. Aucun appel automatique au chargement n'est ajouté.

## 26. Absence de choix automatique

Le harnais ouvre seulement l'event. Il ne contient ni appel d'option, ni effet reproduisant 2.a, ni branche automatique. Le joueur devra sélectionner manuellement et exclusivement l'option 2.a pendant la phase runtime.

## 27. Protocole des cinq répétitions

1. Lancer une nouvelle partie BIC avec uniquement la copie jetable.
2. Exécuter `zz_sepoy_test_a3_prepare` et choisir l'option de préparation.
3. Vérifier visuellement Bundelkhand BIC, MARATH et NAG.
4. Créer une sauvegarde pré-option immuable et relever son hash.
5. Exécuter `zz_sepoy_test_a3_open_event`.
6. Choisir uniquement 2.a.
7. Relever l'owner final de la portion témoin de Bundelkhand.
8. Quitter sans écraser la sauvegarde pré-option.
9. Recharger exactement cette même sauvegarde, avec le même hash et le même playset.
10. Répéter jusqu'à cinq exécutions totales, sans faire avancer préalablement la partie et sans modifier le harnais.

Chaque résultat devra occuper une ligne distincte du futur CSV runtime.

## 28. Exemples syntaxiques

| API/syntaxe | Exemple d'autorité | Scope | Usage A-3 |
|---|---|---|---|
| `s:STATE_*.region_state:TAG` | Harnais A-2 et scripts vanilla/fork | state portion | cibler la portion BIC de Bundelkhand |
| `owner = root` | option 2.a et harnais A-2 | state vers country | confirmer que BIC possède le témoin |
| `region = sr:region_north_india` | option 2.a | state | confirmer la zone générique |
| `any_neighbouring_state` | option 2.a identique aux quatre sources | state | confirmer l'adjacence des receveurs |
| `any_primary_culture` + `has_discrimination_trait_group` | option 2.a | country/culture | reproduire le filtre sud-asiatique |
| `capital.region = sr:...` | option 2.a | country vers state | reproduire exactement le filtre de capitale |
| `set_variable` | harnais A-1/A-2 | country root | poser le seul marqueur de préparation |
| `trigger_event = { id = ... popup = yes }` | harnais A-1/A-2 et scripts locaux | country | ouvrir manuellement l'event réel |

Aucune API provenant d'un autre jeu Paradox n'a été déduite.

## 29. Localisations EN/FR

Deux fichiers dédiés fournissent les dix clés visibles en anglais et en français. Les textes nomment MARATH/NAG, le Bundelkhand, l'absence de mutation territoriale, l'annulation, le caractère destructif de l'event réel, le choix exclusif de 2.a, la sauvegarde pré-option, les cinq rechargements et l'interdiction d'utiliser ou d'écraser les sauvegardes baseline/A-1/A-2.

## 30. Contrôles BOM

Les quatre nouveaux fichiers sont normalisés en UTF-8 avec BOM, utilisent LF uniquement et ne contiennent aucun CRLF. Les headers de localisation sont respectivement `l_english:` et `l_french:`.

## 31. Termes interdits

La recherche ciblée dans les quatre fichiers A-3 ne trouve aucun appel aux events ultérieurs, aucune journal entry, aucun effet de radicaux/loyalistes, aucune création de pays, aucun hasard ou boucle propre au harnais, aucun state interdit et aucune zone périphérique interdite. Seuls l'event réel `.2`, les tags MARATH/NAG et `STATE_BUNDELKHAND` sont employés conformément au scénario.

## 32. Validation statique

Contrôles exigés : encodage UTF-8 valide, BOM, LF, accolades équilibrées, namespace unique, deux décisions, un event, deux options, un seul `set_variable`, un seul appel à l'event 2, zéro choix automatique, zéro mutation d'ownership et zéro conflit d'identifiant.

Le nombre final attendu de fichiers dans la copie est 960, soit les 956 contrôles initiaux plus exactement quatre fichiers A-3.

## 33. Résumé du manifest

Le manifest C1H inventorie les quatre créations A-3, les douze anciens harnais, les deux fichiers Sepoy de la copie, les deux fichiers Sepoy du fork, les trois contrôles de descripteur/marqueur et les deux livrables C1H. Les contrôles préexistants conservent leurs hashes ; le manifest s'identifie comme auto-référentiel.

## 34. Procédure runtime suivante

La phase suivante devra lancer le jeu seulement après sélection du playset de la copie jetable, commencer une nouvelle partie BIC, préparer A-3, sauvegarder avant l'event réel, puis exécuter les cinq essais. Aucun résultat runtime n'est revendiqué ici.

## 35. Observations obligatoires avant 2.a

- pays joué : BIC ;
- BIC sujet de GBR ;
- COO et JEY présents ;
- portion témoin de Bundelkhand détenue par BIC ;
- portion MARATH adjacente ;
- portions NAG adjacentes ;
- décision d'ouverture disponible ;
- sauvegarde pré-option créée et hashée ;
- aucun troisième owner voisin admissible observé.

## 36. Observations obligatoires après chaque 2.a

- event fermé normalement ;
- jeu actif, sans crash ni blocage ;
- boucle terminée ;
- pays joué conforme au traitement final ;
- BIC dissoute/annexée comme prévu ;
- owner du témoin relevé ;
- owner appartenant à `{ MARATH, NAG }` ;
- aucun owner nul, double ou tiers ;
- logs frais conservés pour chaque exécution.

## 37. Critères de variance valide

Une série est valide si chacun des cinq owners observés est MARATH ou NAG. Une série `MARATH` cinq fois ou `NAG` cinq fois reste valide : le test ne prétend pas démontrer une probabilité uniforme. Toute valeur extérieure à cet ensemble, tout owner nul, toute double attribution, boucle ou absence de terminaison constitue un échec.

## 38. Risques restants

- L'itération des pays n'est pas un tirage uniforme entre receveurs ; la variance peut être faible ou nulle sur cinq essais.
- Le contrôle exact repose sur deux tests positifs par tag et un test négatif générique des autres owners valides, faute de compteur local attesté.
- Le jeu doit recalculer les voisinages comme la topologie statique vanilla ; le runtime reste l'autorité finale.
- Les erreurs globales hors Sepoy déjà connues peuvent encore polluer les logs et devront être distinguées des erreurs A-3.

## 39. Verdict

`READY_FOR_A3_RUNTIME_TEST`

Motifs : témoin stable isolé, deux receveurs exacts, zéro mutation territoriale, aucun troisième receveur, harnais manuel, un seul appel à l'event 2, aucun choix automatique et sources Sepoy intactes.

## 40. Liste exacte des fichiers créés dans la copie

1. `common/decisions/zz_sepoy_functional_test_a3.txt`
2. `events/zz_sepoy_functional_test_a3_events.txt`
3. `localization/english/zz_sepoy_functional_test_a3_l_english.yml`
4. `localization/french/zz_sepoy_functional_test_a3_l_french.yml`

## 41. Liste exacte des fichiers créés dans le fork

1. `docs/reports/hotfix/HOTFIX_5C2E4C1H_SEPOY_A3_STATIC_SETUP.md`
2. `docs/reports/hotfix/HOTFIX_5C2E4C1H_A3_HARNESS_MANIFEST.csv`

## 42. Confirmation que les fichiers Sepoy sont inchangés

Les fichiers `common/journal_entries/04_sepoy_mutiny.txt` et `events/india_events/sepoy_mutiny_events.txt` du fork et de la copie sont inchangés. Leurs hashes restent ceux consignés à la section 4.

## 43. Confirmation que les anciens harnais sont inchangés

Les quatre fichiers racine, quatre fichiers A-1 et quatre fichiers A-2 sont inchangés octet par octet par rapport au manifest C1F.

## 44. Confirmation que docs/research/technology/ est intact

Les sept fichiers non suivis sous `docs/research/technology/` restent l'exception concurrente initiale et n'ont subi aucune action.

## 45. Confirmation que le stash MARATH est intact

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` reste présent, non appliqué et non modifié. Aucun `stash pop`, `stash apply`, suppression ou inspection de contenu n'a été effectué.
