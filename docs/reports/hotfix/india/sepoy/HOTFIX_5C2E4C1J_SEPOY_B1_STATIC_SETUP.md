# HOTFIX-5C2E4C1J - Préparation statique du test Sepoy B-1

## 1. Résumé

Cette phase prépare un harnais jetable pour tester manuellement l'option `sepoy_mutiny_events.2.b`, la retraite de BIC vers le Bengale. La baseline 1776 satisfait déjà le trigger d'accès : aucune mutation territoriale n'est nécessaire. Le harnais pose seulement `zz_sepoy_test_b1_ready`, puis ouvre l'événement réel sans sélectionner d'option. Verdict statique : **READY_FOR_B1_RUNTIME_TEST**.

## 2. État Git initial

- Dépôt : `1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD observé : `65538e1 Clean Sepoy A3 harness tooltips`.
- Aucun fichier suivi n'était modifié.
- Le stash MARATH était présent et n'a pas été appliqué.

## 3. Exception docs/research/technology/

`docs/research/technology/` était le seul chemin non suivi avant cette phase. Il est hors périmètre et n'a été ni lu pour produire le harnais, ni modifié.

## 4. Vérification de la copie

La copie jetable contenait 960 fichiers avant B-1, aucun dossier `.git`, aucun `remote_file_id`, les seize fichiers des harnais racine/A-1/A-2/A-3 et aucun des quatre fichiers B-1 autorisés. Les deux sources Sepoy correspondaient aux hashes attendus. Après ajout, la cible est de 964 fichiers.

## 5. Comparaison fork/hotfix/vanilla de 2.b

Le bloc complet de l'option `sepoy_mutiny_events.2.b` est identique dans le fork, la copie, le hotfix et la vanilla 1.13 : 437 lignes dans l'extraction par accolades, un accès par `STATE_WEST_BENGAL`, une pondération IA par `STATE_EAST_BENGAL`, puis les mêmes reprises prioritaires, redistribution générique et radicaux. Aucun remplacement de source n'est requis.

| Source | Option | Accès | East Bengal | Effet final |
|---|---|---|---|---|
| Fork | `sepoy_mutiny_events.2.b` | portion possédée de West Bengal | pondération IA seulement | redistribution puis radicaux |
| Copie | identique | identique | identique | identique |
| Hotfix | identique | identique | identique | identique |
| Vanilla 1.13 | identique | identique | identique | identique |

Pseudo-flux : BIC possède une portion de West Bengal -> option 2.b disponible -> sujets admissibles rendus indépendants -> reprises prioritaires -> redistribution générique des portions BIC adjacentes -> résidu territorial éventuel de BIC -> radicaux hindous et sunnites dans les states BIC restants de North India -> BIC reste jouée si elle conserve au moins un state.

## 6. Trigger d'accès

| Condition | Fork | Hotfix | Vanilla | Baseline 1776 | Satisfaite | Conséquence |
|---|---|---|---|---|---|---|
| `any_scope_state = { state_region = s:STATE_WEST_BENGAL }` | oui | oui | oui | BIC possède 16 provinces | oui | option 2.b accessible |
| `STATE_EAST_BENGAL` | IA seulement | IA seulement | IA seulement | BIC possède le state | sans effet joueur | augmente l'attrait IA |
| Claim seule suffisante | non | non | non | claims sans pertinence | non | une portion possédée est requise |

Le trigger ne diffère pas entre les quatre sources et n'est pas modifié.

## 7. Setup BIC 1776

BIC a sa capitale au Bengale occidental, est une compagnie à charte sujette de GBR, possède des portions au nord et au sud de l'Inde et a deux sujets initiaux, COO et JEY. Cette topologie suffit à ouvrir manuellement l'option Bengale sans préparation territoriale.

## 8. Noyau Bengal intentionnel

Le titre et la localisation de l'option annoncent un repli vers Fort William/Calcutta. L'intention fonctionnelle est donc qu'un noyau bengali demeure sous BIC pendant que les possessions périphériques sont abandonnées.

## 9. Noyau Bengal réellement protégé

Le code ne contient aucune exclusion explicite protégeant `STATE_WEST_BENGAL` ou `STATE_EAST_BENGAL` de la boucle générique. West Bengal n'est qu'une condition d'accès et East Bengal une pondération IA. Le noyau final dépend donc des adjacences et receveurs valides au moment de la boucle ; le harnais ne garantit aucun résultat territorial.

## 10. Analyse West Bengal

- Initial : BIC possède 16 provinces, COO une province.
- Région stratégique : `region_north_india`.
- Rôle : unique condition d'accès à 2.b.
- Protection : aucune exclusion explicite après l'accès.
- Attendu : doit être relevé avant/après ; une conservation totale ne peut pas être présumée.

## 11. Analyse East Bengal

- Initial : BIC possède les 30 provinces.
- Région stratégique : `region_north_india`.
- Rôle : seulement `has_state_in_state_region` dans le poids IA.
- Protection : aucune.
- Attendu : état témoin du cœur bengali, potentiellement redistribué si un receveur générique valide est voisin.

## 12. Analyse Bihar

- Initial : BIC possède les 39 provinces.
- Région stratégique : `region_north_india`.
- Pas de branche prioritaire dédiée.
- La redistribution générique peut l'attribuer à un pays sud-asiatique voisin admissible.

## 13. Analyse Awadh

- Initial : AWA possède 15 provinces, BIC 13.
- Région stratégique : `region_north_india`.
- Priorité : création d'AWA si nécessaire ; si MUG existe, la portion BIC d'Awadh peut lui être transférée selon la branche correspondante.

## 14. Analyse Bundelkhand

- Initial : MARATH possède 17 provinces, BIC 7.
- Région stratégique : `region_north_india`.
- Pas de reprise prioritaire dédiée dans 2.b.
- La boucle générique peut rendre la portion BIC à MARATH, NAG ou un autre receveur voisin valide selon la topologie runtime.

## 15. Analyse Circars

- Initial : BIC possède 17 provinces, JEY 7.
- Région stratégique : `region_south_india`.
- Priorité : transfert vers HYD si HYD possède entièrement Hyderabad.
- Sinon, la redistribution générique reste possible.

## 16. Analyse Pegu

- Initial : BUR possède 19 provinces, BIC une, DENNOR une.
- Région stratégique : East Asia, hors `region_north_india` et `region_south_india`.
- Une branche prioritaire autour de la Birmanie existe, mais cette portion périphérique doit être observée séparément ; elle ne relève pas du noyau bengali.

## 17. Sujets BIC

COO et JEY sont des puppets initiaux. La première phase de 2.b rend indépendants les sujets dont la capitale remplit les filtres géographiques prévus. Le test doit relever leur statut avant/après et vérifier qu'aucun sujet admissible ne reste attaché par erreur.

## 18. Receveurs prioritaires

| Zone | Receveur prioritaire ou repli |
|---|---|
| Madras | CAR |
| Mandalay/Pegu | BUR |
| Gujarat | BER |
| Tenasserim | BUR, puis SIA, sinon KRN |
| Travancore | COC, sinon TRA |
| Circars/Kurnool | HYD |
| Delhi/Agra | MUG |
| Awadh | AWA ou MUG selon existence |
| Central Provinces | NAG |
| Bombay | SAT, sinon KHP |

## 19. Receveurs génériques

Après les branches prioritaires, la boucle cherche des portions BIC restantes dans North/South India, adjacentes à un pays dont une culture primaire possède l'héritage sud-asiatique et dont la capitale se trouve dans North/South India. Les receveurs plausibles incluent HYD, MUG, NAG, MARATH et d'autres voisins satisfaisant ces critères. Le choix d'un state adjacent est aléatoire dans le script réel ; le harnais n'en reproduit ni n'en force le résultat.

## 20. Effet sur les radicaux

À la fin de l'option, `every_scope_state` limite les states encore possédés par BIC à `region_north_india`. Deux effets ajoutent `large_radicals`, l'un aux pops hindoues, l'autre aux pops sunnites. L'effet intervient après les transferts : les states déjà cédés ne sont donc plus dans le scope de BIC. Le runtime doit comparer au moins un state BIC restant de North India et vérifier que les radicaux ne sont pas appliqués dans une autre région.

## 21. Mutations nécessaires

Zéro mutation territoriale, diplomatique, culturelle, religieuse ou de capitale est nécessaire.

## 22. Justification du nombre de mutations

La baseline contient déjà une portion BIC dans `STATE_WEST_BENGAL`, seule condition réelle de l'option 2.b. Ajouter une mutation masquerait le comportement naturel du setup 1776. La seule écriture du harnais est le marqueur jetable `zz_sepoy_test_b1_ready`.

## 23. Résultat fonctionnel attendu

L'option 2.b doit être visible, être choisie manuellement, terminer sans boucle bloquée, laisser BIC jouée et territorialement présente si le code lui conserve un state, redistribuer les portions selon les branches valides, traiter les sujets, appliquer les radicaux uniquement aux states BIC restants de North India et ne créer aucun owner nul.

## 24. Namespace et identifiants

Namespace : `zz_sepoy_test_b1`. Décisions : `zz_sepoy_test_b1_prepare`, `zz_sepoy_test_b1_open_event`. Event : `zz_sepoy_test_b1.1`. Marqueur unique : `zz_sepoy_test_b1_ready`. La recherche dans le fork, la copie et la vanilla a retourné zéro conflit avant création.

## 25. Décision de préparation

Visible uniquement pour le joueur BIC sans marqueur, chance IA nulle. Elle réévalue sous `custom_tooltip` la possession d'une portion de West Bengal et ouvre seulement l'événement de confirmation B-1. Son `when_taken` ne modifie aucun état de jeu.

## 26. Event de préparation

L'événement contient exactement deux options. La première pose uniquement le marqueur de disponibilité ; la seconde annule sans effet. Il ne modifie aucun territoire et n'appelle aucun événement Sepoy réel.

## 27. Décision d'ouverture

Visible uniquement pour le joueur BIC avec le marqueur. Elle réévalue la condition réelle de West Bengal sous `custom_tooltip`, ne produit aucune mutation et appelle une seule fois `sepoy_mutiny_events.2` sur le root BIC.

## 28. Sécurité de l'appel

La chance IA est nulle pour les deux décisions. Aucun `random_`, aucune boucle, aucune création de pays et aucun choix automatique ne figurent dans le harnais. Le joueur doit sélectionner exclusivement 2.b dans l'événement réel.

## 29. Tooltips propres

Les trois occurrences du trigger complexe `any_scope_state` sont enveloppées dans des `custom_tooltip` évalués : préparation, événement de confirmation et ouverture. Les clés EN/FR sont définies et la logique reste réellement évaluée.

## 30. Localisations

Les fichiers anglais et français définissent exactement les dix clés demandées. Ils signalent le caractère jetable, zéro mutation, l'absence de garantie du noyau bengali, le choix manuel exclusif de 2.b, la sauvegarde pré-option, l'interdiction d'écraser la baseline ou d'utiliser A-1/A-2/A-3, et l'absence de restauration automatique.

## 31. Contrôles BOM

Les quatre fichiers B-1 sont normalisés en UTF-8 avec BOM, utilisent uniquement LF et ne contiennent aucun CRLF.

## 32. Validation statique

Contrôles prévus et exécutés : accolades équilibrées, deux décisions, un événement de deux options, un marqueur, un seul appel à `sepoy_mutiny_events.2`, zéro choix automatique, dix clés par langue, absence de doublon, trois `custom_tooltip` et zéro terme interdit.

## 33. Résumé du manifest

Le manifest inventorie les quatre fichiers B-1, les seize contrôles des harnais antérieurs, les quatre sources Sepoy fork/copie, le descriptor de copie, le marqueur, le descripteur launcher et les deux livrables C1J. La ligne du manifest lui-même est marquée `SELF_REFERENTIAL` pour sa taille et son hash.

## 34. PLAN DE SESSION RUNTIME CONDENSÉE

1. Ouvrir Victoria 3 une seule fois avec le playset contenant uniquement la copie jetable.
2. Démarrer une nouvelle partie BIC, jamais une sauvegarde A-1/A-2/A-3, et rester en pause.
3. Relever avant préparation : pays joué, portion BIC de West/East Bengal, Bihar, Awadh, Bundelkhand, Circars et Pegu ; sujets COO/JEY ; propriétaires voisins ; radicaux hindous/sunnites d'au moins un state BIC de North India.
4. Prendre `Préparer le test Sepoy B-1`, confirmer l'option de préparation, puis vérifier que la carte et la diplomatie sont inchangées.
5. Créer une sauvegarde pré-option immuable distincte sans écraser la baseline.
6. Prendre `Ouvrir l'événement réel...`, vérifier que 2.b est disponible, puis choisir uniquement l'option Bengale 2.b.
7. Sans fermer le jeu, relever immédiatement : pays joué, existence/territoire BIC, West/East Bengal, Bihar, Awadh, Bundelkhand, Circars, Pegu, sujets et propriétaires issus des reprises prioritaires/génériques.
8. Laisser passer au plus un jour si nécessaire pour stabiliser l'interface, puis relever les radicaux hindous/sunnites dans les states BIC restants de North India et rechercher tout owner nul.
9. Créer une sauvegarde post-option distincte si utile.
10. Ne recharger la sauvegarde pré-option dans cette même session que si une observation manquait ; ne pas créer une session GBR séparée.
11. Quitter Victoria 3 une seule fois après tous les relevés.
12. Analyser ensuite les logs frais pour B-1, l'événement 2, les states observés, les transferts et toute boucle/erreur de scope.

## 35. Nombre prévu d'ouvertures du jeu

Une seule ouverture de Victoria 3 est prévue pour tout le test B-1.

## 36. Justification de toute ouverture supplémentaire

Aucune ouverture supplémentaire n'est prévue. Une seconde ouverture ne serait acceptable qu'en cas de corruption de sauvegarde ou d'impossibilité technique de recharger dans la session courante ; elle devrait alors être marquée `TECHNICALLY_REQUIRED` et motivée précisément.

## 37. Observations avant option

Relever les owners/controllers et portions BIC des sept states audités, la présence de West Bengal donnant accès à 2.b, les sujets COO/JEY, les receveurs prioritaires/génériques disponibles, le pays joué et une baseline de radicaux hindous/sunnites dans North India.

## 38. Observations après option

Relever les mêmes states et relations, les pays créés ou utilisés par les branches réelles, le territoire BIC restant, le pays joué, l'achèvement de la boucle, les owners nuls éventuels et la variation de radicaux uniquement sur les states BIC restants de North India.

## 39. Critères de verdict runtime

PASS si 2.b est disponible et manuelle, l'événement se termine sans crash/blocage, les transferts prioritaires sont cohérents, les transferts génériques ont des receveurs valides, BIC conserve ou perd ses portions conformément au code, les sujets sont traités, les radicaux ciblent seulement le bon scope et aucun state n'a d'owner nul.

## 40. Risques restants

Le principal risque est l'écart entre la localisation de repli vers Calcutta et l'absence de protection explicite de West/East Bengal. La boucle générique est également sensible à l'ordre et aux adjacences runtime. Les radicaux peuvent être difficiles à mesurer si aucun state BIC de North India ne subsiste.

## 41. Verdict

**READY_FOR_B1_RUNTIME_TEST**

## 42. Fichiers créés dans la copie

- `common/decisions/zz_sepoy_functional_test_b1.txt`
- `events/zz_sepoy_functional_test_b1_events.txt`
- `localization/english/zz_sepoy_functional_test_b1_l_english.yml`
- `localization/french/zz_sepoy_functional_test_b1_l_french.yml`

## 43. Fichiers créés dans le fork

- `docs/reports/hotfix/HOTFIX_5C2E4C1J_SEPOY_B1_STATIC_SETUP.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1J_B1_HARNESS_MANIFEST.csv`

## 44. Confirmation des fichiers Sepoy

`common/journal_entries/04_sepoy_mutiny.txt` et `events/india_events/sepoy_mutiny_events.txt` n'ont été modifiés ni dans le fork ni dans la copie. Les hashes copie attendus restent respectivement `DAEFCB59CCF6B303D2E39C948D8038006C1346AFE40A2B812D45EE4D947E361C` et `557936500AC585F7F69B9F5B063BDDA377AFF4A5AFAA06C70650C55D4AD612F7`.

## 45. Confirmation des anciens harnais

Les seize fichiers racine/A-1/A-2/A-3 ont été utilisés uniquement comme contrôles et exemples. Aucun n'a été modifié.

## 46. Confirmation docs/research/technology/

`docs/research/technology/` demeure intact et conserve son statut préexistant non suivi.

## 47. Confirmation du stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est resté présent, intact et non appliqué.
