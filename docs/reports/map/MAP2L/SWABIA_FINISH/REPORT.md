# MAP-2L — Finition souabe : domaines supplémentaires de 1776

## Corrections réellement appliquées

Ce sous-lot poursuit la Souabe sans prétendre clôturer toutes ses juridictions. **63 cellules changent de propriétaire**, dans trois masques provisoires seulement. Neuf RGB nouveaux, `xEDAF00`–`xEDAF08`, sont ajoutés ; **241 cellules sont recolorées** pour obtenir des provinces distinctes et connexes, y compris les franges dont le propriétaire ne change pas.

| Domaine représenté | Avant | Après | Cellules | Population redistribuée |
|---|---|---|---:|---:|
| Salem, noyau temporel de Salmannsweiler | BAD | SLM | 6 | 4 751 |
| Waldburg-Wolfegg-Waldsee, noyau de la branche Waldsee | WUR | SWW | 8 | 7 891 |
| Waldburg-Wolfegg-Wolfegg, noyau de Wolfegg | WUR | SWF | 18 | 17 754 |
| Waldburg-Zeil-Wurzach, noyau de Wurzach | WUR | SWX | 19 | 18 739 |
| Waldburg-Zeil-Trauchburg, noyau de Zeil seulement | WUR/BAV | SWY | 6/2 | 5 918/728 |
| Évêché temporel de Constance, office de Markdorf seulement | BAD | SKC | 4 | 3 167 |

Les six pays sont membres du bloc impérial, **sans nouvel électeur ni ville libre fictive**. Les comtes de Waldburg n’obtiennent pas le titre princier de 1803. Les capitales sont les subdivisions partagées `STATE_BADEN` ou `STATE_WURTTEMBERG`, et non des coordonnées urbaines prétendument mesurées. Les identifiants existants de la Suède (`SWE`), du Swaziland (`SWZ`) et du Swat (`SWT`) sont conservés ; une collision de TAG détectée en préparation a été corrigée avant installation.

Salem reçoit Anselme II Schwab, abbé de 1746 à 1778 ; Constance reçoit Maximilien-Christophe de Rodt, élu en décembre 1775. Les quatre comtes séculiers restent générés par le moteur : leurs identités historiques ne sont pas inventées. Les drapeaux procéduraux sont des repères de jeu, pas une certification héraldique.

## Sources et approximations

Le tracé reprend la correspondance antérieure, puis la raccorde à une carte territoriale ciblée : **Herrschaftsgebiete und Ämtergliederung in Südwestdeutschland 1790**, feuille VI.13 du [Historischer Atlas de Baden-Württemberg](https://www.lgl-bw.de/Produkte/Karten/Historische-Karten/Historischer-Atlas-von-Baden-Wuerttemberg/index.html), Nüske et Kerkhoff, publication 1987. Seuls les noyaux de juridictions identifiables et compatibles avec 1776 sont retenus. La carte de 1790 n’est pas copiée aveuglément : Friedberg-Scheer vendu en 1785 est exclu, ainsi que la réunification de Wolfegg en 1798 et les titres de 1803.

Salem est corroboré par sa **Mappa de 1765**, représentant les limites de haute juridiction par les bornes 1–129, conservée dans `EVIDENCE/SALEM_1765.jpg` et présentée par le [portail éducatif institutionnel du Bade-Wurtemberg](https://www.schule-bw.de/faecher-und-schularten/gesellschaftswissenschaftliche-und-philosophische-faecher/geschichte/unterrichtsmaterialien/sekundarstufe-I/mittelalter/salem/politik.html). Il s’agit de terres temporelles, pas du diocèse. Le noyau choisi exclut Heiligenberg et Meersburg.

La séparation des branches Wolfegg-Waldsee et Wolfegg-Wolfegg est antérieure à 1776 et leur réunion date de 1798 : [chronologie de la commune de Waldburg](https://www.gemeinde-waldburg.de/gaeste/die-waldburg/geschichte). La succession de Trauchburg en 1772 ne sert pas à attribuer des domaines inconnus en bloc : seul le noyau de Zeil est tracé, ses possessions éloignées restent ouvertes.

Les raccords entre cartes ont des résidus d’ajustement de **0,246 à 1,054 pixel**, mais **ce ne sont pas des erreurs indépendantes de localisation physique**. L’incertitude du calage antérieur reste entière ; son contrôle économique indépendant à Lindau était d’environ 9,575 pixels. Les enveloppes sont des approximations conservatrices de juridictions à l’échelle du jeu, pas un cadastre ni une preuve de précision à deux pixels. Aucun repère économique n’est utilisé pour déduire seul une souveraineté.

La carte de Fallot de **1750**, BnF GE C-1623, est désormais conservée pour Montbéliard. Aucun transfert n’en est tiré à ce stade : les propriétés wurtembergeoises ne suffisent pas à distinguer les territoires impériaux des dépendances sous souveraineté française depuis 1748. Le traité de 1786 n’est pas rétroprojeté. Les autres limites ouvertes figurent dans `UNRESOLVED.csv`.

## Conservation et dépendances techniques

**58 948 habitants sont redistribués, aucun n’est créé.** La population mondiale reste **835 804 980**. Les cultures, religions effectives, profils et attributs démographiques sont conservés par allocation entière depuis les sources immuables. Ces poids de surfaces ne sont pas présentés comme un recensement historique local.

Les bâtiments, méthodes de production, niveaux et propriétaires économiques, formations militaires, unités et recrutements sont conservés. Aucun nouveau bâtiment ou bataillon n’est créé artificiellement. Les historiques des pays ajoutés réemploient les variantes juridiques et technologies de départ déjà utilisées par les États impériaux.

Le registre passe de **476 à 485 RGB**, mais sa surface reste **62 580 cellules** : subdivision de droits déjà enregistrés, sans extension territoriale de l’Empire. Le registre, les déclencheurs et effets compilés, le tableau impérial et les deux rendus de carte sont actualisés.

Un seul repère économique nécessite une mise à jour de référence : le champ `mine` de `STATE_WURTTEMBERG`, nommé « Lindau » par le jeu, passe de `xDBB84C` à `xEDAF06`, au **même pixel (4316,927)**. Aucun locator n’est déplacé. Son nom n’est pas utilisé comme preuve de position de Lindau. Les validations rejouent uniquement cette liaison explicite ; elles ne dispensent pas de contrôler les autres repères.

Les **211 cellules des noyaux souabes de première passe** et les **92 cellules Fürstenberg–Ellwangen**, avec leurs RGB, restent exactes. Rhin–Westphalie, Minden, Belgique, Franconie et Mayence sont conservés. Aucun changement à Erfurt–Eichsfeld, à la France ou à un nouveau lot régional.

## Fichiers et contrôles

`PLAN.json` liste les historiques, définitions d’États, six pays, lois, caractères, gouvernements, drapeaux et localisations FR/EN modifiés. `IMPERIAL_FILES.json` liste les dépendances impériales compilées. Le bitmap, les terrains et les textures dérivées sont également actualisés. `TERRITORIAL_CHANGES.csv` détaille chaque RGB, les propriétaires avant/après et les cellules ; `POPULATION_VALIDATION.csv` détaille la conservation par profil.

Les résultats effectifs sont dans `VALIDATION.json`, `NON_REGRESSION.json` et `CUMULATIVE_RUN.json`. Les **44 doublons RGB et 12 références invalides préexistants** sont conservés comme anomalies héritées. Les écarts Git anciens résultant du changement de HEAD autorisé sont conservés dans les rapports bruts, séparément des contrôles de données. Le HEAD et l’index de cette passe doivent rester ceux de sa capture immuable.

Le sous-lot supplémentaire passe **518/518 contrôles statiques**. Les textures et l’aide au rendu passent **16/16 contrôles hors jeu**, et les tests unitaires de migrations et d’attestations **20/20**. Les lignes à espaces terminaux des deux historiques restent identiques à la capture : 28 dans les populations, 50 dans les États ; les deux lignes signalées par le diff Git sont antérieures à cette passe et ne sont pas nettoyées au passage.

La revue cumulative des **16 lots** termine à **12 827/12 837 contrôles bruts**. Les dix écarts concernent uniquement les références Git antérieures au changement de HEAD autorisé : **tous les contrôles de données passent**. Les rapports bruts ne sont pas rebaptisés PASS. Le HEAD reste `f34a6b88db749a8be77ec558fd55ad196b45f72a`, l’index conserve l’empreinte `0ec78afee9417a38092441b78a2274aeb46e3fa58cfa0d51334f73c269841d53`.

La première exécution du contrôle de Franconie-continuation rejetait la nouvelle couleur du repère « Lindau ». Ce contrôle est désormais étendu à la chaîne exacte des liaisons explicitement déclarées, sans déplacement physique ni tolérance générale. Sa relance donne **997/998**, seul l’écart Git restant. `CUMULATIVE_RUN.json` conserve le premier résultat ; `QA_RECHECKS.json` atteste le résultat corrigé. Deux tests négatifs garantissent qu’un autre pixel ou une chaîne RGB incohérente restent refusés.

**Statut manuel : PASS_RUNTIME_USER_VALIDATED.** Le joueur a achevé les sept vérifications demandées dans une nouvelle partie, puis laissé passer un mois sans problème. La portée est limitée aux territoires et mécanismes inspectés ; les RGB exacts contrôlés n’ont pas été fournis. Attestation : `../RUNTIME_USER_VALIDATION_SWABIA_FINISH.json`. Les contrôles techniques restent statiques, sans chargement moteur automatisé ni certification historique de toutes les frontières. Les modifications ultérieures de `SWABIA_COMPLETION` ne sont pas couvertes.

### Vérification dans une nouvelle partie

Vérifier Salem, les quatre Waldburg et le noyau de Markdorf : présence, propriétaires, capitales partagées, gouvernements et descriptions sans clé brute, appartenance impériale, économie et passage d’un mois. Examiner aussi les raccords au lac, les petites dépendances de Zeil dans `STATE_BAVARIA`, le repère minier inchangé et les deux cartes de jure. Les limites encore ouvertes ne deviennent pas historiquement certifiées à la suite de ce test.

## Recherche locale et sauvegarde

Aucun appel ColGrep n’était nécessaire pour retrouver les fichiers d’implémentation déjà connus ; les recherches exactes et les formats cartographiques non indexés ont été traités directement. Aucune économie exacte de quota Codex n’est revendiquée, aucun modèle ni paramètre d’intégration n’est changé, aucun index n’est reconstruit.

Aucun commit, merge, reset, changement de branche, push ou nouveau checkpoint n’est effectué. Le checkpoint publié précédemment reste celui de la version antérieure validée, pas de cette finition locale.

Les deux gros PNG d’aperçu générés (`AT_OVERLAY` et `SALEM_READING`) ont été remplacés par des JPEG de mêmes dimensions. Les sources et données nécessaires à leur régénération restent conservées ; environ **59 Mo** d’intermédiaires redondants ont été libérés. Aucun fichier source, bitmap de jeu, sauvegarde immuable ou travail du collaborateur n’est supprimé.
