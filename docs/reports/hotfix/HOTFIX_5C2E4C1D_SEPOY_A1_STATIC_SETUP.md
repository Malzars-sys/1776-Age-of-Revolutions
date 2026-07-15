# HOTFIX-5C2E4C1D - Setup statique du harnais Sepoy A-1

## 1. Résumé

Le setup du 1er janvier 1776 satisfait déjà les prérequis du scénario A-1.
Aucune mutation territoriale, diplomatique, culturelle ou de capitale n'est
nécessaire. Le harnais séparé créé dans la copie jetable ne fait qu'ajouter un
marqueur pays après confirmation, puis offre une seconde décision qui ouvre
manuellement `sepoy_mutiny_events.2` sur le root BIC.

**Verdict : `READY_FOR_A1_RUNTIME_TEST`.**

Cette phase est strictement statique : ni Victoria 3 ni le launcher n'ont été
lancés et aucune option de l'événement Sepoy n'a été exécutée.

## 2. État Git initial

- Racine : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD : `d12ad35 Fix disposable Sepoy harness encoding`.
- Le commit C1C1 est donc présent.
- Aucun fichier suivi n'était modifié.
- Stash présent : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception docs/research/technology

`docs/research/technology/` était la seule exception non suivie avant la
phase. Le dossier n'a été ni lu pour modifier son contenu, ni modifié, ni
copié vers la copie jetable.

## 4. Vérification de la copie C1C1

Avant création, la copie contenait exactement 948 fichiers et aucun fichier
A-1. Elle possédait son `descriptor.mod`, le descripteur launcher externe, le
marqueur de sécurité, les quatre fichiers du harnais racine et aucun `.git` ou
`remote_file_id`.

| Contrôle C1C1 | SHA-256 vérifié |
|---|---|
| Décision racine | `E8CC4B78AB7447A5CED31C525B99814542C82AEEE5C47C530446870772C120FF` |
| Event racine | `E69B386716B7E33BC311CF3450C89B0605A0E92AA6C74B689591171810D156EE` |
| JE Sepoy | `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` |
| Events Sepoy | `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7` |
| Descripteur interne | `1921791546626A938E18EEADC765538120325AFA87E0EA309C2C3C6502175B40` |
| Marqueur | `280066169F9D9D7020FEF4342264D18C5B1613CA40B74D519ADD4E7F3492838A` |
| Descripteur launcher | `FBFDFB891E3E355C05ED996B4A6866475E259081E8196187A2424C9DECCC3733` |

## 5. Audit du setup BIC 1776

| Objet | Valeur 1776 | Fichier source | Ligne ou bloc | Rôle dans A-1 |
|---|---|---|---|---|
| Root | `BIC`, pays colonial, capitale configurée `STATE_WEST_BENGAL` | `common/country_definitions/00_countries.txt` | 2526-2535 | Root de l'event |
| Overlord | `GBR` | `common/history/diplomacy/00_subject_relationships.txt` | bloc GBR, 238-240 | Annexion finale |
| Type de sujet | `chartered_company` | même fichier | même bloc | Satisfait `is_subject_of = c:GBR` |
| Sujets directs | `JEY`, `COO`, tous deux `puppet` | même fichier | 337-345 | `make_independent` |
| États BIC | 7 region states, 123 provinces valides | `common/history/states/00_states.txt` | blocs détaillés ci-dessous | Transferts et reliquat |
| Controller | aucun override de controller trouvé | même fichier | blocs BIC | Le controller initial suit l'owner hors occupation |
| Incorporation | `state_type` omis pour 6 states ; Pegu explicitement `unincorporated` | même fichier | blocs BIC | Sans incidence sur 2.a |

Les cinq fichiers structurants du setup ont des hashes identiques dans le
fork et la copie. La reconstruction ne dépend donc pas d'une session de jeu
antérieure.

## 6. Tableau des sujets BIC

| Sujet | Relation | Capitale configurée | Possession 1776 | Culture primaire | Héritage | Filtre 2.a |
|---|---|---|---|---|---|---|
| `COO` | puppet direct | `STATE_EAST_BENGAL` | enclave dans `STATE_WEST_BENGAL` | bengali | `heritage_gangetic`, groupe sud-asiatique | Oui : capitale configurée et fallback possédé sont en North India |
| `JEY` | puppet direct | `STATE_ORISSA` | enclave dans `STATE_CIRCARS` | oriya | `heritage_gangetic`, groupe sud-asiatique | Oui : capitale configurée en North India ; fallback possédé en South India |

Les capitales configurées ne sont pas possédées par ces tags au départ. Le
moteur peut donc choisir leur unique region state possédé comme capitale
effective. Cette ambiguïté ne bloque pas A-1 : les deux couples
configuré/fallback appartiennent tous aux zones admises par l'option 2.a.

## 7. Tableau des states BIC North/South

| State | Provinces BIC | Zone utilisée par 2.a | `state_type` historique | Traitement attendu |
|---|---:|---|---|---|
| `STATE_EAST_BENGAL` | 30 | North India | défaut moteur | redistribution générique |
| `STATE_BIHAR` | 39 | North India | défaut moteur | redistribution générique |
| `STATE_WEST_BENGAL` | 16 | North India | défaut moteur | redistribution générique |
| `STATE_AWADH` | 13 | North India | défaut moteur | reprise prioritaire vers MUG |
| `STATE_BUNDELKHAND` | 7 | North India | défaut moteur | témoin générique retenu |
| `STATE_CIRCARS` | 17 | South India | défaut moteur | reprise prioritaire vers HYD |
| `STATE_PEGU` | 1 | hors zones de 2.a | unincorporated | reliquat BIC avant annexion finale |

BIC ne possède aucun region state dans `region_himalayas`,
`STATE_PASHTUNISTAN` ou `STATE_QUETTA`.

## 8. Tableau des voisins et receveurs

| State BIC | Voisin/partage pertinent | Preuve | Receveur valide ? | Usage |
|---|---|---|---|---|
| `STATE_BUNDELKHAND` | `MARATH` | parts BIC et MARATH dans le même state ; frontières de provinces `x5CBFF7-xD0F986` et `x5CBFF7-x0E5FEA` dans la carte vanilla | Oui | témoin de redistribution générique |
| `STATE_CIRCARS` | `JEY` partage le state ; HYD possède tout Hyderabad | history states 4069-4080 et 4184-4196 | HYD reçoit par priorité | témoin prioritaire |
| `STATE_AWADH` | AWA partage le state ; MUG existe | history states 4298-4311 et définition MUG | MUG reçoit selon le `else_if` actuel | témoin prioritaire |
| `STATE_PEGU` | BUR partage le state | history states 4378-4399 | non, Pegu est hors zones génériques | reliquat attendu |

`MARATH` a la culture primaire marathi. La vanilla définit marathi avec
`heritage_deccani`, lequel appartient à `heritage_group_south_asian`.
Sa capitale configurée est `STATE_BOMBAY`, membre de `region_south_india`.
Il satisfait donc les deux filtres du receveur générique.

## 9. Prérequis A-1

| # | Prérequis | Statut | Preuve |
|---:|---|---|---|
| 1 | BIC existe | `SATISFIED_BY_BASELINE` | définition BIC et 7 region states |
| 2 | BIC contrôlable par le joueur | `SATISFIED_BY_BASELINE` | tag normal colonial ; harnais root C1C1 validé pour un joueur BIC |
| 3 | GBR existe | `SATISFIED_BY_BASELINE` | définition GBR et setup mondial |
| 4 | BIC sujet de GBR | `SATISFIED_BY_BASELINE` | pacte direct `chartered_company` |
| 5 | State BIC North India | `SATISFIED_BY_BASELINE` | cinq region states |
| 6 | State BIC South India | `SATISFIED_BY_BASELINE` | `STATE_CIRCARS` |
| 7 | Sujet direct à capitale admissible | `SATISFIED_BY_BASELINE` | COO et JEY |
| 8 | State redistribuable avec voisin valide | `SATISFIED_BY_BASELINE` | Bundelkhand vers MARATH |
| 9 | Priorités n'empêchent pas le témoin générique | `SATISFIED_BY_BASELINE` | Bundelkhand n'est dans aucune reprise prioritaire |
| 10 | Reliquat annexable par GBR | `SATISFIED_BY_BASELINE` | BIC reste sujet GBR ; Pegu est hors boucle générique |

## 10. Mutations minimales requises

**Zéro mutation de setup.** Aucun owner, controller, sujet, capitale, culture,
heritage, pays ou state n'est changé. L'option de préparation ajoute seulement
le marqueur country-scoped `zz_sepoy_test_a1_ready`.

## 11. Justification du nombre de mutations

Les dix prérequis sont déjà satisfaits. Une mutation territoriale aurait
réduit la fidélité au setup 1776 et augmenté le risque sans améliorer le test.
Le compteur de mutations de setup du manifest est donc `0`.

## 12. Acteurs et states retenus

- Root : `BIC`.
- Overlord final attendu : `GBR`.
- Sujets directs observés : `COO` et `JEY`.
- State North India observé : `STATE_BUNDELKHAND`.
- State South India observé : `STATE_CIRCARS`.
- Redistribution générique : portion BIC de `STATE_BUNDELKHAND`.
- Receveur voisin attendu : `MARATH`.
- Reprises prioritaires observables : HYD pour Circars, MUG pour Awadh.
- Reliquat attendu avant annexion : au minimum la portion BIC de `STATE_PEGU`.

La boucle générique reste aléatoire. MARATH est un receveur valide attesté,
mais le propriétaire final de chaque autre state ne doit pas être prédit de
façon déterministe.

## 13. Exemples syntaxiques utilisés

- `trigger_event = { id = ... popup = yes }` reprend le harnais racine validé
  et les décisions vanilla.
- `set_variable = zz_sepoy_test_a1_ready` et
  `has_variable = zz_sepoy_test_a1_ready` sont attestés dans
  `common/decisions/00_decisions.txt` vanilla.
- Aucune API de `country_flag` n'est attestée dans la vanilla locale ; le
  « flag jetable » demandé est donc implémenté par l'unique variable booléenne
  country-scoped autorisée.

## 14. Namespace et identifiants

- Namespace : `zz_sepoy_test_a1`.
- Décisions : `zz_sepoy_test_a1_prepare`, `zz_sepoy_test_a1_open_event`.
- Event : `zz_sepoy_test_a1.1`.
- Marqueur unique : `zz_sepoy_test_a1_ready`.
- La recherche préalable dans fork, copie et vanilla donnait zéro conflit.

## 15. Décision de préparation

`zz_sepoy_test_a1_prepare` est visible seulement pour le joueur BIC. Son bloc
`possible` répète `is_player = yes` et `c:BIC ?= this`, puis refuse une seconde
préparation si le marqueur existe. Sa chance IA vaut zéro. Son unique effet
est l'ouverture du popup `zz_sepoy_test_a1.1`.

## 16. Event de confirmation/préparation

L'event est un `country_event` placé sur root, gardé par joueur BIC et absence
du marqueur. Il contient exactement deux options :

1. préparation explicite, qui ajoute uniquement le marqueur ;
2. annulation sans effet.

Il ne contient aucune mutation de setup.

## 17. Décision d'ouverture

`zz_sepoy_test_a1_open_event` n'est visible que pour le joueur BIC après
préparation. Les mêmes gardes sont répétées dans `possible`. Sa chance IA vaut
zéro. Son unique effet est l'ouverture de `sepoy_mutiny_events.2` sur le root
pays courant.

## 18. Sécurité de l'appel à sepoy_mutiny_events.2

- Un seul appel dans les quatre fichiers A-1.
- Aucun appel depuis l'event de préparation.
- Aucun appel au chargement.
- Aucun appel aux events `.3` ou `.4`.
- Aucune boucle et aucun hasard dans le harnais.
- Aucune mutation dans la décision d'ouverture.
- Les fichiers Sepoy restent bit à bit identiques.

## 19. Absence de choix automatique de 2.a

Le harnais ouvre seulement l'event réel. Il ne contient ni sélection d'option,
ni effet copié depuis 2.a, ni chaîne d'appel automatique. Le joueur devra
choisir manuellement 2.a dans une future session, idéalement en restant en
pause jusqu'au clic.

## 20. Localisations EN/FR

Les dix clés demandées existent dans les deux langues. Les textes distinguent
la préparation et l'ouverture réelle, préviennent du caractère destructif,
de l'annexion possible de BIC, du passage possible à GBR, de l'obligation de
choisir seulement 2.a et de l'absence de restauration automatique.

## 21. Contrôles BOM

| Fichier A-1 | Taille | SHA-256 | BOM | Fins de ligne |
|---|---:|---|---|---|
| décision | 683 | `74642E139F07C58A8184759FB1140F2741D5622DA3A17B3810D017328E43E3A1` | `EF BB BF` | 44 LF, 0 CRLF |
| event | 650 | `82569A22DD65DED1385FAB993E6D9243C49558ECF46E744C3CE70EF353C9523A` | `EF BB BF` | 33 LF, 0 CRLF |
| localisation EN | 1376 | `3A0ABAD442262E0F20E76C23BDBBB596D0914EBC8FCB373715663907695863E9` | `EF BB BF` | 11 LF, 0 CRLF |
| localisation FR | 1560 | `791FEF8CD8240C88D7BD3AA2EB87CB99FCCD31A73529D428F6FD332BCAD720B3` | `EF BB BF` | 11 LF, 0 CRLF |

Les YAML commencent logiquement par `l_english:` et `l_french:` après le BOM.
Les fichiers C1B/C1C1 n'ont subi aucune normalisation.

## 22. Termes interdits

La recherche sur les quatre fichiers A-1 donne zéro occurrence pour tous les
termes interdits de la phase, notamment les autres events Sepoy, les JE, les
boucles, le hasard, les effets de radicaux/loyalistes, les créations de pays,
les IDs territoriaux protégés et les strategic regions. Aucun terme n'était
nécessaire puisque le setup n'est pas muté.

## 23. Validation statique

- Accolades : décision `13/13`, event `6/6`.
- Namespace : un seul namespace A-1.
- Décisions : exactement 2.
- Event de préparation : exactement 1.
- Options de préparation : exactement 2.
- Identifiant de marqueur : exactement 1 identifiant unique.
- Appel event 2 : exactement 1.
- Choix automatique : 0.
- Clés de localisation EN/FR : 10/10 dans chaque langue, sans doublon.
- BOM : présent sur les 4 fichiers.
- Copie : 952 fichiers, aucun `.git`, aucun `remote_file_id`.

Cette validation ne prétend pas que le breakup a déjà fonctionné en jeu.

## 24. Résumé du manifest

Le manifest couvre 17 entrées : quatre créations A-1, quatre contrôles du
harnais racine, quatre contrôles Sepoy copie/fork, les trois fichiers de
sécurité/descripteurs et les deux livrables C1D. Les hashes auto-référentiels
du manifest lui-même sont laissés vides.

## 25. Procédure runtime suivante

1. Vérifier que le jeu et le launcher sont fermés avant inspection des fichiers.
2. Activer uniquement `1776_Age_of_Revolutions_sepoy_test`.
3. Démarrer une nouvelle partie BIC au 1er janvier 1776 et rester en pause.
4. Créer une sauvegarde jetable distincte de la baseline.
5. Prendre `Préparer le test de dissolution Sepoy A-1` puis confirmer.
6. Vérifier qu'aucun owner, sujet ou pays n'a changé.
7. Prendre `Ouvrir l'événement réel de dissolution Sepoy`.
8. Choisir manuellement et uniquement l'option 2.a.
9. Ne pas écraser la baseline ; relever sujets, owners, pays joué et logs.

## 26. Résultats attendus avant le choix 2.a

- BIC reste root et sujet direct de GBR.
- COO et JEY restent sujets directs de BIC.
- Les sept possessions BIC restent inchangées.
- Seul le marqueur jetable existe après préparation.
- L'event réel est visible, sans effet exécuté tant que le joueur n'a pas
  choisi une option.

## 27. Résultats attendus après le choix 2.a

- COO et JEY deviennent indépendants si leur capitale effective passe le
  filtre, ce qui est attendu pour les deux.
- Circars est repris prioritairement par HYD.
- Awadh est repris selon le chemin MUG actuel.
- Bundelkhand entre dans la redistribution générique ; MARATH est un receveur
  voisin admissible, sans garantie qu'il gagne chaque tirage.
- Les autres states admissibles sont distribués aux princes voisins valides.
- Le reliquat BIC, notamment Pegu, est annexé par GBR.
- Le pays joué peut devenir GBR via `play_as`.

## 28. Risques restants

- La boucle réelle est aléatoire et doit être surveillée pour non-termination.
- Les capitales configurées de COO/JEY diffèrent de leurs possessions ; leur
  capitale effective doit être relevée au runtime.
- Le chemin Awadh/MUG reflète le code actuel, même si AWA existe.
- Les erreurs globales hors harnais restent présentes dans les logs du mod.
- Le comportement exact de tous les transferts ne peut être validé statiquement.

## 29. Verdict

**`READY_FOR_A1_RUNTIME_TEST`**

La baseline suffit avec zéro mutation, le harnais est statiquement valide,
l'appel à l'event réel est unique et manuel, aucun choix n'est automatisé et
les sources Sepoy sont inchangées.

## 30. Fichiers créés dans la copie

- `common/decisions/zz_sepoy_functional_test_a1.txt`
- `events/zz_sepoy_functional_test_a1_events.txt`
- `localization/english/zz_sepoy_functional_test_a1_l_english.yml`
- `localization/french/zz_sepoy_functional_test_a1_l_french.yml`

## 31. Fichiers créés dans le fork

- `docs/reports/hotfix/HOTFIX_5C2E4C1D_SEPOY_A1_STATIC_SETUP.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1D_A1_HARNESS_MANIFEST.csv`

## 32. Confirmation des fichiers Sepoy

Les JE et events Sepoy du fork et de la copie conservent les hashes C1C1.
Aucune ligne n'a été modifiée dans ces quatre contrôles.

## 33. Confirmation du harnais racine

Les quatre fichiers du harnais racine sont inchangés. Les deux scripts
conservent les hashes C1C1 et les deux YAML conservent leurs hashes antérieurs.

## 34. Confirmation docs/research/technology

Le dossier `docs/research/technology/` reste l'exception non suivie initiale.
Aucun de ses fichiers n'a été modifié.

## 35. Confirmation du stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` est toujours présent, non
appliqué et intact. Aucun `git stash pop` et aucun commit n'ont été exécutés.
