# Issue #56 — HRE mensuel, IA et stabilisation du monde initial

17 novembre 2026. Essais réels sur le PC Windows de l’utilisateur, après `RELOAD_EXPERIMENT_2026_11_17/REPORT_FR.md`, conservé intact. Référence Git : `bd776919f625016cb9e63b2359cc04796c681ef5`. [Issue #56](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/56).

## Résultat principal

**Le contrôleur HRE mensuel n’explique pas une part substantielle du ralentissement dans ces essais. Le signal le plus fort concerne le fonctionnement de l’IA : désactiver tous ses contrôleurs fait passer les mêmes 56 premiers jours de 149 à 29 secondes.** Cette ablation modifie le gameplay ; ce n’est pas une optimisation installable. Elle ne localise pas une fonction C++ et n’exclut pas les scripts évalués par l’IA ou les conséquences de ses décisions.

La campagne normale instrumentée devient déjà beaucoup plus rapide en juillet 1776 : **148 secondes pour les 56 premiers jours de janvier, contre 39 secondes pour 56 jours à partir de juillet, dans le même processus**. Le contrôle antérieur d’avril 1777, rapide avant et après deux redémarrages, reste valable. Il n’a pas été répété dans cette passe.

**Aucun correctif préservant le gameplay n’est validé.** Le coût exact, nécessaire ou redondant, reste à identifier. Aucun correctif spéculatif n’a été intégré, fusionné ou publié.

## Environnement et méthode

- Exécutable **Steam Victoria 3 1.15.1**, sans DLC de gameplay ; seul le contenu précommande est présent dans cette installation. L’installation canonique locale **1.15.0 avec DLC** n’a pas servi aux mesures.
- Runtime normal figé : `C:/Users/simeo/AppData/Local/Temp/aor1776_simperf56_20261117/main_frozen`, comprenant COMPACT. Lancement direct avec profils de laboratoire séparés ; la différence observée dans la base normale du lanceur est examinée au §8, sans restauration de sa sélection.
- Sauvegarde commune France du 1er janvier 1776, mêmes paramètres initiaux, vitesse 5 vérifiée à l’interface, vue carte France au départ. Aucun pays, POP ou contenu historique retiré.
- Exécutable SHA256 `fb4ec0698afd3d3b1a785926d57bd5d68c95a4afd04b56f6bd45abd7a5672b15` ; paramètres initiaux `49c2686a57d7950b21297338107b005791c813532954ed55fb3d13c35ef4df6c`.
- Chronométrage des **journées simulées**, à partir des timestamps natifs HH:mm:ss. Première journée partielle exclue ; calendrier moteur de 365 jours ; continuité des DAY vérifiée. Résolution : erreur inférieure à une seconde sur une différence de deux timestamps. Les heures d’arrivée des logs tamponnés ne servent jamais de chronomètre.
- CPU cumulé et working set échantillonnés toutes les 500 ms, alignés en UTC sur les timestamps Paris UTC+1. CPU exprimé sur l’ensemble des **16 processeurs logiques**. CPU de démarrage, menus et chargements exclus. Aucun FPS ni délai d’ouverture d’interface mesuré ici.
- Le fonctionnement de Windows, les fréquences, les autres applications et la résidence mémoire ne sont pas intégralement contrôlés. L’ancienne référence initiale à 93 s ne doit pas être comparée directement à une variante actuelle à 122–149 s. Chaque conclusion utilise son témoin contemporain.

## 1. Contrôleur HRE mensuel seul : quatre passages exécutés

Ordre normal → diagnostic → diagnostic → normal, avec une tentative HMM2 interrompue **en pause, avant toute journée**, puis remplacée par HMM2R. Cette tentative n’est pas une mesure.

| Passage, dans l’ordre réel | 14 jours | 28 jours | 56 jours | CPU moyen, 56 jours |
|---|---:|---:|---:|---:|
| HMC1, normal | 35 s | 68 s | 122 s | 20,10 % |
| HMM1, mensuel HRE désactivé | 36 s | 69 s | 122 s | 21,38 % |
| HMM2R, mensuel HRE désactivé | 37 s | 71 s | 125 s | 21,26 % |
| HMC2, normal | 37 s | 71 s | 125 s | 21,10 % |

La seule différence de runtime est le corps de `aor1776_hre_monthly_hook` dans `common/on_actions/1776_imperial_constitution.txt`, remplacé par une trace. Les définitions quotidiennes HRE et l’IA régionale restent normales. L’appel de planification contenu dans le hook mensuel disparaît nécessairement avec ce hook ; la chaîne quotidienne déjà programmée continue. Le test n’est pas une ablation de tout le HRE.

Empreinte source : `686907a54bae899bcebe454ec949f9c4abac882f2d669f018fc71dbe8ff32123` ; diagnostic : `dbc95401eee41e5a106929a412d77eed6cdac1454d7f997c507995f96ffd6b1b`. Une seule différence de fichier vérifiée dans la copie expérimentale.

**Exécution vérifiée** : traces natives `HRE_MONTHLY_BYPASSED` aux 1er février, mars et avril dans chacun des deux diagnostics, aucune dans les témoins. La première fenêtre de 56 jours inclut le pulse de février ; les logs continuent au-delà de 100 jours et vérifient les pulses suivants.

Les deux paires de 56 jours donnent exactement le même temps : 122 contre 122, puis 125 contre 125. Ce résultat affaiblit fortement l’hypothèse d’un gros surcoût net provenant de ce contrôleur. Il n’exclut pas un coût plus petit, des effets indirects compensatoires ou un autre système HRE. Aucun gain certain n’est revendiqué à partir d’un écart d’une seconde.

## 2. Ablation de l’IA : signal majeur, portée encore large

Les deux passages utilisent le runtime normal, la même sauvegarde initiale et la même instrumentation supplémentaire : sonde CPU par thread, interface de commandes de laboratoire et invocation de `log_ticktask_performance`. Le menu de laboratoire est fermé pendant les mesures. Le profilage Legacy des scripts est **désactivé pendant les premières fenêtres des deux passages**.

| Passage comparable | 14 jours | 28 jours | 56 jours | Jours/s sur 56 jours | CPU moyen |
|---|---:|---:|---:|---:|---:|
| ENG_ON2, IA normale | 47 s | 87 s | 149 s | 0,376 | 20,93 % |
| ENG_OFF2, `disable_ai all` | 8 s | 15 s | 29 s | 1,931 | 17,67 % |

Différence observée : **80,5 % de temps en moins**, débit multiplié par **5,14**, sur une paire. Ce sont des estimations descriptives, sans intervalle de confiance statistique ni précision garantie du pourcentage.

La commande native a été appliquée avant la reprise. Une nouvelle sauvegarde du **19 avril 1776**, distincte de la source, confirme **646 contrôleurs `enabled=no`, zéro `yes`**, contre 646 `yes` dans la source. Preuve : `ENG_OFF2_RUNTIME_PROOF.json`. La restauration de la visibilité du jeu par l’utilisateur a eu lieu après les fenêtres mesurées et la pause.

La suppression de pays, de bâtiments ou de population ne sert donc pas à produire ce résultat. Toutefois, retirer l’IA retire des décisions et peut modifier des évaluations de scripts ou des conditions liées à l’IA. On ne peut pas traduire « IA désactivée = rapide » par « telle fonction économique native est coupable », ni par « tous les scripts moddés sont innocents ». La paire n’a pas été répétée dans l’ordre inverse ; les contrôles normaux supplémentaires donnent un ordre de grandeur compatible, pas une répétition strictement identique de cette paire.

## 3. Janvier puis juillet : même processus, même profilage

PROF_INIT conserve l’IA normale. Le profilage Legacy est activé **avant la première journée**, puis reste actif pendant les deux groupes ci-dessous. Une sauvegarde normale du **1er juillet 1776 à 18 h moteur** a été créée et vérifiée avant la deuxième reprise.

| Monde dans PROF_INIT | 14 jours | 28 jours | 56 jours | CPU moyen sur 56 jours |
|---|---:|---:|---:|---:|
| Janvier, première journée complète puis suivantes | 45 s | 85 s | 148 s | 21,09 % |
| Juillet, DAY du 2 juillet puis suivants | 9 s | 18 s | 39 s | 21,09 % |

La fenêtre tardive va du 2 juillet au 27 août. Elle se trouve après la préparation en pause du 1er juillet et avant la pause finale. Le débit est multiplié par 3,79, avec une occupation CPU moyenne similaire : la simulation consomme beaucoup moins de temps CPU pour ces 56 jours. Cela ne nomme pas le travail devenu moins coûteux. Le working set moyen passe d’environ 8 495 à 4 424 Mio ; la résidence des pages dépend aussi de Windows et des pauses, et ne prouve pas une cause mémoire.

Deux pauses de préparation, au 3 avril et au 1er juillet, sont explicitement séparées. Les fenêtres qui les traversent sont rejetées. ENG_ON2 comporte également une pause au 22 mars : ses fenêtres qui la traversent ne sont pas des benchmarks. Les 24 fenêtres retenues dans `MEASUREMENTS.csv` ont été contrôlées contre les pauses connues.

Le lanceur borné a fermé ses seuls processus ENG_ON2, ENG_OFF2 et PROF_INIT après les prises et sauvegardes, par requête d’arrêt contrôlée ; leurs EXIT portent `-1`, pas une sortie naturelle `0`. Les quatre passages HRE ont terminé avec `0`. La dernière ligne DAY de PROF_INIT est incomplète dans le log brut final : elle est conservée telle quelle. Une **copie d’analyse distincte** exclut uniquement cette dernière ligne non terminée ; les 277 DAY complets précédents sont consécutifs. Les résultats utiles sont antérieurs à cette fin de log.

## 4. Ce qui change dans les sauvegardes normales

Extraction en lecture seule. Les totaux de population obtenus indépendamment par pays et par État concordent exactement aux quatre dates. Juillet et août proviennent de deux branches normales distinctes issues de S0 ; avril 1777 vient de la branche MATURE1 antérieure. Ce n’est pas une trajectoire déterministe unique suivie sans interruption.

| Indicateur enregistré | 1er janvier 1776 | 1er juillet 1776 | 8 août 1776 | 21 avril 1777 |
|---|---:|---:|---:|---:|
| Population, personnes | 837 119 763 | 844 171 394 | 845 797 926 | 855 592 042 |
| Objets POP sérialisés | 31 475 | 26 133 | 26 286 | 28 217 |
| Enregistrements de bâtiments | 6 879 | 7 611 | 7 620 | 7 730 |
| Niveaux de bâtiments, tous types compris | 105 250 | 105 525 | 105 545 | 106 293 |
| Bâtiments avec profit après réserves négatif | 2 188 | 950 | 1 011 | 1 226 |
| Main-d’œuvre salariée, statistique pays | 31 577 271 | 30 421 044 | 30 359 393 | 29 968 816 |
| Main-d’œuvre au chômage, statistique pays | 1 833 128 | 2 283 212 | 2 517 625 | 3 720 647 |
| États en déficit d’infrastructure | 40 | 199 | 211 | 234 |
| Entrées `country_goal` IA | 38 090 | 38 493 | 38 494 | 38 227 |
| Compteur cumulé d’investissements autonomes échoués | 0 | 68 347 | 71 804 | 128 603 |
| Formations militaires sérialisées | 258 | 1 473 | 1 467 | 1 469 |
| Enregistrements de marchés | 479 | 485 | 485 | 484 |
| Enregistrements de traités | 25 | 26 | 26 | 28 |

**Économie, emploi et PM.** 465 ensembles de PM diffèrent en juillet parmi 6 597 identifiants de bâtiments ayant conservé type et État ; 581 parmi 6 570 en avril 1777. L’ordre textuel des PM est ignoré ; les identifiants recyclés sont écartés. Les profits et l’emploi changent, mais le chômage et les déficits d’infrastructure augmentent malgré l’accélération. Ces corrélations n’établissent pas le coût du calcul des prix, du recrutement ou de l’investissement. Les niveaux incluent notamment les bâtiments de subsistance et ne correspondent pas au seul inventaire historique de construction.

**Stratégies, priorités et files IA.** Les listes de stratégies enregistrées sont identiques pour les 643 pays peuplés comparables entre janvier et juillet. Seize listes diffèrent en avril 1777. Les entrées `country_goal` ne se vident pas : leur nombre reste proche de 38 000. Elles ne constituent pas une longueur de file de décisions exécutables démontrée. Les compteurs d’échecs sont cumulatifs, sans attribution de temps CPU. L’hypothèse d’une grosse file initiale qui se vide n’est donc pas établie par ces indicateurs.

**Commerce, diplomatie et militaire.** Les objets de marchés et traités varient peu ; les formations militaires augmentent fortement. Les deux enregistrements de guerre et de crise diplomatique présents à chaque point ne signifient pas nécessairement deux conflits actifs. L’état des routes commerciales, les arbitrages de construction, les prix et les files de décisions natives ne sont pas entièrement décodés ou profilés ; aucun de ces systèmes n’est exonéré par son seul nombre d’objets.

**Dates, variables et état persistant.** Les occurrences de `aor1776_ai_regional_cooldown` passent de 75 à 25 puis 12 aux trois dates janvier/juillet/avril. Les drapeaux de planification HRE quotidien et de certains événements de départ restent présents. Des champs d’expiration deviennent plus nombreux ; ils ont des significations différentes et ne comptent pas directement les modificateurs actifs. Aucun effet n’a été arbitrairement expiré pour tester les performances.

La section native `tasks` contient 34 entrées au départ, 267 en juillet et 272 en avril 1777. Six tâches ultérieures sérialisent un `update_index`, notamment les transitions de professions/chômage, le commerce d’esclaves et trois mises à jour des objectifs IA. Par exemple, `UpdateAICountryGoalsAddRemove` enregistre 260 en juillet et 440 en avril. **Cela démontre une persistance d’état du planificateur, pas un cache responsable ni une quantité de travail en attente.** Modifier ces curseurs sans contrat moteur validé ne serait pas un test interprétable.

L’ancien champ d’extraction `STATE_*.dated_data.aor_variable_names`, fondé sur `name=`, n’est pas un indicateur valable des flags. Les comparaisons corrigées utilisent le vrai champ `flag=` : `PERSISTENT_STATE_COMPARISON.json` et `FLAG_COMPARISON.json`.

## 5. Profilage obtenu et limites techniques

**Profilage Legacy des scripts réellement exporté**, avec activation avant le premier tick dans PROF_INIT. Dump janvier–3 avril : 4 994 lignes, dont 4 065 triggers, 863 script_values et 66 effets. Les compilations partageant un même fichier/numéro de ligne sont regroupées seulement dans la synthèse, sans modifier les dumps. Le second export au 1er juillet contient les 4 969 emplacements initiaux, avec compteurs et temps tous croissants ou égaux ; les compteurs cumulatifs sont donc cohérents.

| Emplacement | Janvier–3 avril | Appels | Cumul au 1er juillet |
|---|---:|---:|---:|
| `20_law_commitment.txt:108`, validité du type de loi | 2,049 s | 8 595 | 3,304 s |
| `00_victoria_progress_bars.txt:1097` | 0,859 s | 1 200 | 1,407 s |
| `00_default_strategy.txt:4526`, score régional IA | 0,745 s | 73 274 | 1,358 s |

La somme brute des lignes initiales vaut 24,917 s ; **ce n’est pas du CPU exclusif**, les appels pouvant être imbriqués et la couverture incomplète. Les effets HRE/régionaux ne sont pas tous présents comme entrées identifiables. Le plus gros emplacement observé ne suffit pas à expliquer un écart d’environ 120 s sur 56 jours, mais ce profil ne mesure pas l’ensemble des coûts natifs ni de tous les scripts. Aucune réorganisation spéculative du filtre de lois n’a été appliquée.

**CPU par thread réellement obtenu.** Dans ENG_ON2 initial, deux TID sans nom représentent environ 25,0 % et 23,9 % du CPU échantillonné, soit 83,4 % et 79,5 % d’un cœur pendant la fenêtre. Le CPU total observé des threads passe d’environ 496,5 secondes CPU sur les 149 secondes de simulation normale à 81,5 secondes CPU sur les 29 secondes sans IA. Les identifiants changent entre processus. Sans noms, piles ou symboles, on ne peut pas appeler ces threads « principal », « simulation » ou « économie ».

**Profilage détaillé du moteur non obtenu.** L’invocation native `log_ticktask_performance` n’a produit aucun `profiling.log` exploitable dans les emplacements inspectés. L’ouverture de l’autre interface Script Profiler affichait zéro échantillon ; les dumps Legacy constituent la preuve de profilage script, pas cette interface.

Windows Performance Recorder existe, mais la tentative ordinaire puis une seconde tentative hors des restrictions de l’outil d’exécution ont échoué avant tout enregistrement, code **0xc5585011**, « Failed to enable the policy to profile system performance ». La revue automatique avait autorisé cette seconde tentative : **ce n’est pas un refus d’approbation automatique**. Cette autorisation de l’outil ne certifie pas une élévation administrateur Windows, qui n’a pas été attestée dans la trace. Aucun ETL de piles CPU n’a été obtenu, aucun réglage de sécurité Windows n’a été changé et WPR est confirmé inactif après les essais. L’obstacle actuel à l’attribution C++ est précisément celui-ci.

## 6. État des hypothèses A/B/C/D

| Explication | Bilan contrôlé |
|---|---|
| A — calculs nécessaires mais très chers au départ | Compatible avec l’évolution normale et le signal IA ; nécessité et équivalence des résultats non démontrées. |
| B — scripts moddés répétés ou redondants | Les ablations quotidiennes HRE et mensuelles régionale/HRE n’expliquent pas le gros écart dans les configurations testées. Aucun hotspot VM observé ne l’explique à lui seul ; couverture trop partielle pour exclure tous les scripts. |
| C — IA/économie native réagissant au monde 1776 | **Hypothèse ayant gagné le plus de soutien** avec l’ablation IA vérifiée. Économie, diplomatie, militaire et évaluations scriptées restent confondus dans ce contrôle large. |
| D — effet de date ou état temporaire/persistant | Compatible avec la rapidité après rechargement mature et les états sérialisés différents. Date, économie et état du planificateur ne sont pas séparés causalement. |

On ne sait pas encore si l’IA réalise un travail nécessaire coûteux ou des tentatives répétitives évitables. Aucune capacité du système de modding à déplacer ces calculs vers le chargement n’a été démontrée. Aucun réglage de fréquence, cache ou préinitialisation ne peut être recommandé comme correction équivalente sur ces seules preuves.

Les ablations repartent de S0, où les initialisations de début de campagne ont déjà été appliquées. Elles n’exonèrent pas ces initialisations ni leurs conséquences persistantes sur l’économie et l’IA. Les isoler demanderait une expérience dédiée de création du monde, avec vérification des différences obtenues.

## 7. Expérience suivante à plus forte valeur diagnostique

**D’abord répéter le grand signal dans l’ordre inverse, sans Legacy : IA désactivée → IA normale**, même S0, instrumentation commune, fenêtres 14/28/56 et preuve des flags. Cela quantifiera la robustesse à la dérive de la machine ; la paire actuelle reste unique.

Puis, une seule variable supplémentaire : **désactiver uniquement les contrôleurs IA des pays décentralisés dans une copie de S0**, en gardant tous les pays, POPs, historiques, marchés et autres IA. Les tables vérifiées identifient 244 pays décentralisés peuplés, 400 autres pays peuplés et deux contrôleurs non classés dans la table des pays peuplés. Ne pas les assimiler automatiquement à une catégorie. Un témoin et le diagnostic doivent partager une petite instrumentation identique ; sauvegarde et champs AI vérifiés en jeu après les prises, puis ordre inverse si signal faible.

Cette partition distingue un groupe doté d’une IA différente du groupe comprenant les principales décisions économiques/diplomatiques ; elle ne nommera pas une fonction et n’est pas une optimisation. Un effet important justifiera une partition plus fine, **dans une prise suivante séparée**. Sans effet, priorité au groupe des autres pays et à ses choix économiques/diplomatiques, avant toute modification de l’économie initiale.

En parallèle, obtenir une trace CPU avec piles serait le meilleur moyen d’éviter les ablations trop larges. Cela dépend du problème Windows de profilage décrit ci-dessus. Aucun contournement de sa politique de sécurité n’a été entrepris. Une éventuelle initialisation économique différente devra ensuite reproduire les résultats de gameplay, pas simplement accélérer le chronomètre. La répétition inverse et l’ablation par cohorte sont des **expériences recommandées, non encore exécutées dans cette passe**.

## 8. Préservation et anomalie du lanceur examinée

Audit après : **2 996/2 996 fichiers runtime du mod identiques**, COMPACT inclus ; **79/80 fichiers suivis du profil normal identiques**, toutes les sauvegardes suivies comprises. Le seul écart binaire est `launcher-v2.sqlite`. Index Git, HEAD, exécutable Steam et **3/3 fichiers Russie–Kazakh** inchangés. Les 233 preuves antérieures, 449 preuves de performances préexistantes et outils protégés sont conservés. Aucun staging, commit, push, merge, reset ou changement de branche.

La différence du lanceur n’est pas masquée par un PASS global. Son écriture est datée du **17 novembre à 17:37:41 UTC**. La base a été copiée de manière stable puis examinée sans écriture sur l’original : contrôle SQLite `quick_check=ok`. Comparaison avec la base historique B2, après exclusion de ses deux playsets de test nommés :

- mêmes sept identifiants de playsets ; noms, ordre de chargement et tous les autres champs égaux hors cinq champs ci-dessous ;
- **11/11 associations de mods exactement identiques**, activation et positions comprises ; **51/51 associations DLC exactement identiques** ;
- différences dans `isActive`, `lastUsedAt`, `lastSyncAttemptAt`, `syncedOn`, `updatedOn` ; playset actif actuellement `hhhh`, aucun actif dans cette référence historique.

L’empreinte actuelle diffère réellement de celle du début de mission. Faute de copie exacte de la base à cet instant, le détail binaire de cette évolution et son auteur ne sont pas attribuables. La comparaison historique n’est pas artificiellement présentée comme une comparaison exacte de ce matin. Aucune perte d’association ni corruption n’est observée ; **la sélection actuelle est laissée telle quelle**, aucun ancien fichier ou réglage n’a été restauré. Voir `LAUNCHER_REVIEW.json`, détails externes et `PRESERVATION_AFTER.json`.

## 9. Preuves conservées et reprise

**Laboratoire externe court, avec toutes les preuves volumineuses :**

`C:/Users/simeo/AppData/Local/Temp/aor56_state_20261117`

Runtimes diagnostiques, profils, logs natifs, échantillons CPU/RAM/threads, dumps script, copies de lecture du lanceur et JSON d’extraction des sauvegardes restent hors du mod distribué. Aucun effacement des essais antérieurs. Le dépôt reçoit les scripts et les synthèses compactes de ce dossier.

| Sauvegarde vérifiée | Emplacement sous le laboratoire concerné | SHA256 |
|---|---|---|
| S0, 1er janvier 1776 | ancien lab `aor1776_simperf56_20261117/profiles/MAIN3/save games/royaume de france_1776_01_01.v3` | `387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2` |
| Juillet normal, nouveau | `profiles/PROF_INIT/save games/royaume de france_1776_07_01.v3` | `5bdd727a6e725be42677b51dc7e4a2f1d1e6bb54836d159d0384575fea0197fa` |
| Août normal, nouveau | `profiles/ENG_ON2/save games/royaume de france_1776_08_08.v3` | `e855958e9304bf4658d54723d8f1fe82786a01a526274182526f7d231f4e6045` |
| Avril 1777, antérieur | ancien lab `aor1776_simperf56_20261117/profiles/MATURE1/save games/royaume de france_1777_04_21.v3` | `879867ccd58f230c9eef2fbe04570171679cea015010e713be5c746707b732eb` |

Sauvegarde distincte IA désactivée : `profiles/ENG_OFF2/save games/royaume de france_1776_04_19.v3`, SHA256 `4f55dfaf2108b3f1ab24601e99efbcc94c0e3fbbf537df8427c9b5f21cb52273`. La copie S0 éditée en secours, `S0_AI_DISABLED_ONLY.v3`, n’a **jamais été chargée** ; elle ne sert pas de preuve d’exécution.

Fichiers de synthèse : `MEASUREMENTS.csv`, `SUMMARY.json`, `HRE_COMPARISON.json`, `FINAL_QUALITY.json`, `PRESERVATION_AFTER.json`, `LAUNCHER_REVIEW.json`. Les sources détaillées correspondantes sont dans le laboratoire. Vérifications réalisées : syntaxe de 24 scripts Python, continuité/date des fenêtres, exclusion des pauses connues, empreintes des quatre sauvegardes normales, flags IA en sauvegarde, traces de bypass HRE et fermeture des processus. Aucune fenêtre Victoria 3 ne reste ouverte après la série ; WPR n’enregistre pas.

L’Issue #56 a été mise à jour à **19:35:33 UTC le 17 novembre 2026**, puis une précision sur les permissions de l’outil et l’absence de preuve d’élévation administrateur Windows a été publiée à **19:37:49 UTC**. Les deux publications ont été relues par l’API : corps vérifiés exactement, ancien corps conservé intégralement ; titre, état ouvert, labels, responsables et jalon inchangés. La dernière version et son reçu sont archivés dans `ISSUE_BODY_PUBLISHED_FINAL.md` et `PUBLICATION_FINAL.json` ; la première publication reste conservée. Les rapports et outils locaux n’ont pas été commités.

**Statut : HRE mensuel testé en ordre inversé, grand signal IA obtenu, comparaison janvier/juillet exécutée, sauvegardes et profilage script conservés. Enquête causale ouverte ; aucun correctif de production validé.**
