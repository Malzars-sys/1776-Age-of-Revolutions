# Issue #56 — IA économique, reprise locale des 18–19 novembre 2026

Le signal associé aux 400 contrôleurs des pays non décentralisés reste fort. En revanche, **le coût de l'objectif d'extension des bâtiments n'est pas isolé** : les 400 instances retirées de la sauvegarde initiale réapparaissent dans la sauvegarde native dès le 4 janvier. Le passage long ne peut donc pas être interprété comme une désactivation de ce travail. Aucune optimisation préservant le gameplay n'est validée.

La série ultérieure des douze scores moddés de priorité de construction a été **exécutée et répétée sans gain** : 100/102 secondes contre 96/94 pour ses témoins contemporains. Un contrôle global avec les mêmes nouveaux réglages redonne 25 secondes lorsque tous les flags IA sont désactivés. Les tableaux ci-dessous distinguent les lots et leurs limites ; les anciens temps ne sont pas réutilisés comme nouveaux témoins.

Les manipulations et mesures sont réalisées sur le PC Windows local. Les sauvegardes, journaux bruts, profils et copies expérimentales volumineuses restent hors dépôt, dans `C:/Users/simeo/AppData/Local/Temp/aor56_ai_20261117`. [LAB_LOCATION.json](LAB_LOCATION.json) précise les autres emplacements. Aucun commit, push, merge ou changement du mod distribué n'accompagne ce rapport.

## 1. Environnement et mesure

Exécutable Steam **1.15.1**, SHA-256 `fb4ec0698afd3d3b1a785926d57bd5d68c95a4afd04b56f6bd45abd7a5672b15`. Aucun DLC de gameplay dans cette installation de test ; le contenu de précommande reste distinct. L'installation canonique `C:/Games/Victoria 3`, en 1.15.0 avec DLC, n'est ni utilisée pour ces chronométrages ni modifiée.

Runtime figé du mod : `aor1776_simperf56_20261117/main_frozen`, issu du HEAD `bd776919f625016cb9e63b2359cc04796c681ef5`. Réglages de départ communs : SHA-256 `49c2686a57d7950b21297338107b005791c813532954ed55fb3d13c35ef4df6c`. Même interface de mesure et mêmes observateurs CPU/RAM et threads à environ 500 ms ; vitesse 5 vérifiée pour les benchmarks, arbre technologique fermé, profilage des scripts désactivé pendant les fenêtres retenues.

S0 mod : France du 1er janvier 1776, 105 039 521 octets, SHA-256 `387a363748cecd677229d4d03e98c6699830a1da471416491fb6233184d93ed2`. Chaque essai charge une copie isolée. Les fenêtres commencent au premier DAY complet du 2 janvier et se terminent les 16 janvier, 30 janvier et 27 février : **14/28/56 jours du calendrier moteur de 365 jours**. Les heures natives de production du journal sont utilisées, jamais son arrivée tamponnée. La résolution de la différence des horodatages est inférieure à une seconde d'erreur absolue ; elle ne couvre pas la variabilité du PC ou du moteur.

Seules les fenêtres antérieures à la première pause de mesure sont retenues. Préparation, démarrage, sauvegarde, profilage et reprises destinées à vider les tampons sont exclus. Les journaux bruts restent intacts ; toute exclusion d'une dernière ligne incomplète se fait dans une copie d'analyse avec empreintes. Il s'agit de débit de simulation, **pas de FPS**, ni de latence d'ouverture de l'arbre technologique.

## 2. Résultats vérifiés du mod

Les anciennes prises sont reprises de leurs preuves, sans les présenter comme de nouvelles exécutions. Les nombres sont des secondes pour 14/28/56 jours cumulés.

| Série | Traitement | 14 j | 28 j | 56 j | Contrôle de l'état |
|---|---|---:|---:|---:|---|
| AI_OFF3R | Tous contrôleurs désactivés | 8 | 15 | 30 | PRE et POST : 646 non |
| AI_ON3 | Témoin normal de nuit | 46 | 88 | 155 | PRE et POST : 646 oui |
| AI_DEC1 | Décentralisés seuls désactivés | 33 | 65 | 120 | PRE : 246 non/400 oui ; POST : 246 non/399 oui |
| AI_OTHER1 | Autres pays seuls désactivés | 7 | 15 | 30 | PRE et POST : 246 oui/400 non |
| AI_DEC2 | Répétition décentralisés désactivés | 35 | 68 | 123 | PRE et POST : 246 non/400 oui |
| AI_ON4 | Témoin interrompu | 45 | 87 | indisponible | POST natif conservé ; 56 j non inférés |
| AI_ON4R | Témoin normal de jour | 39 | 72 | 122 | PRE et POST : 646 oui |
| AI_OFF4 | Tous désactivés, après témoin de jour | 7 | 15 | 30 | PRE et POST : 646 non |
| ECN1 | Nouveau témoin normal économique | 35 | 69 | 124 | PRE et POST : 646 oui ; objectifs intacts |

AI_DEC1 perd le contrôleur JEY (pays 428, contrôleur 643) avant la sauvegarde du 1er juillet. Les flags de tous les contrôleurs présents sont conformes ; la cause de cette disparition n'est pas établie. Cette réserve ne doit pas être effacée par la répétition AI_DEC2, qui conserve les 646 contrôleurs.

La paire diurne AI_ON4R/AI_OFF4 reproduit le contraste global : 122 contre 30 secondes. La référence nocturne de 155 secondes et celle de 122 secondes diffèrent d'environ 21 % en durée : elles ne sont pas interchangeables. Les essais ciblés et globaux ne constituent pas une décomposition additive des coûts. La forte accélération lorsque les 400 contrôleurs sont désactivés soutient leur association au surcoût, sans identifier leur fonction coûteuse.

ECN1, effectivement exécuté pendant cette reprise, commence à 14:46:16.514 UTC ; ses bornes natives utiles vont du 2 janvier à 14:46:19 au 27 février à 14:48:23. La première pause est à 14:48:51.176 UTC. La sauvegarde POST du 16 mars conserve 646 contrôleurs actifs et tous les objectifs attendus. CPU moyen sur 56 jours : environ **20,16 % de la machine à 16 processeurs logiques** ; mémoire résidente moyenne : environ 14 557 Mio. Ce CPU inclut l'ensemble du processus, dont le rendu, et ne mesure pas exclusivement l'IA.

Les chiffres détaillés, horodatages, CPU et mémoire figurent dans [MEASUREMENTS.csv](MEASUREMENTS.csv) ; les statuts et empreintes des preuves dans [MEASUREMENT_QUALITY.json](MEASUREMENT_QUALITY.json). Une fenêtre temporelle valide n'est pas automatiquement un traitement causal valide.

## 3. Extension des bâtiments : traitement invalidé en jeu

La variante existante `S0_WITHOUT_EXPAND_GOAL.v3`, SHA-256 `c1597fdfe5b6da2b0a0e3e9274d70cacf24a331093320c888268d945177a1b9c`, retire uniquement 400 blocs sérialisés `ai_goal` de type `expand_production_buildings`. Tous les autres octets hors section IA sont conservés ; aucun pays, POP, bâtiment ou marché n'est supprimé. Ce retrait est une ablation diagnostique, pas une optimisation de gameplay.

**EXB1, passage long exécuté :** la sauvegarde native PRE du 1er janvier confirme 646 contrôleurs actifs, les 400 objectifs absents et les autres objectifs/payloads inchangés. Les bornes DAY donnent 39/75/130 secondes. Mais la sauvegarde native POST du 9 mars contient de nouveau **400 objectifs d'extension**, avec les mêmes 646 contrôleurs actifs. `EXB1_POST_GOAL_PROOF.json` porte donc `treatment_verified=false`. Les 130 secondes sont conservées comme chronométrage brut ; elles sont **exclues de toute conclusion sur le coût de l'extension**. L'écart avec ECN1 ne prouve ni gain, ni absence de coût de cette fonction.

**EXB3, contrôle court exécuté séparément :** même preuve PRE, puis quelques jours au réglage de chargement (`speed=2` sérialisé), sans benchmark de débit. La sauvegarde native POST est datée **1776.1.4.18** : les 400 objectifs sont déjà revenus, avec 646 flags actifs. L'intervalle de recréation est ainsi borné entre le 1er janvier et le 4 janvier au soir. Ni l'heure exacte, ni le mécanisme interne de reconstruction, ni la fréquence d'exécution des objectifs ne sont déterminés par ces sauvegardes.

La PRE d'EXB3 a été renommée uniquement dans son nouveau profil isolé, afin de la préserver alors que la saisie du nom ne répondait pas. Son SHA-256 est inchangé ; `EXB3_PRE_SAVE_RELOCATION.json` relie l'ancien chemin enregistré dans la preuve au fichier conservé `PRE_NATIVE_EXB3_1776_01_01.v3`. Le POST a finalement été créé par le jeu sous son nom du 4 janvier. Aucun fichier de référence normal n'a été déplacé.

L'ancien GOAL_EXPAND1 reste une tentative interrompue avec PRE mais sans POST ; EXB2 s'est fermé sans mesure pendant une interruption. L'ordre inversé EXB2/ECN2 préparé n'est pas présenté comme réalisé : poursuivre une longue comparaison d'une désactivation qui ne persiste pas aurait produit une conclusion trompeuse.

## 4. Inventaire et interprétation des charges économiques

Les 646 contrôleurs de S0 sont tous classés : 244 pays décentralisés avec population enregistrée, **deux autres décentralisés** (S72 et S74), et 400 autres pays, soit 123 reconnus, 258 non reconnus et 19 coloniaux. S72 et S74 possèdent respectivement des États en Arizona et Sonora ; leur statistique de population vaut zéro dans l'inventaire. L'absence physique de tout objet POP dans leurs États n'a pas été vérifiée. Ils ne sont ni non classés ni sans territoire. Le groupe diagnostique décentralisé comprend donc 246 contrôleurs.

Les instances natives des objectifs économiques ciblés se trouvent chez les 400 autres pays. Le flag `enabled=yes` est également présent pour le contrôleur du pays humain ; il ne prouve pas que toutes ses routines s'exécutent comme celles d'un pays IA.

La synthèse locale `ECONOMIC_WORLD_INDICATORS_20261118.json` réutilise les extractions existantes, sans prétendre constituer une série causale à dates appariées :

| État observé | Objets POP | Bâtiments à profit négatif | Objets bâtiment / niveaux | Formations |
|---|---:|---:|---:|---:|
| S0, 1er janvier 1776 | 31 475 | 2 188 | 6 879 / 105 250 | 258 |
| IA normale, 13 mars 1776 | 23 734 | 776 | 7 505 / 105 066 | 1 401 |
| IA globale désactivée, 6 mai 1776 | 24 678 | 711 | 6 654 / 104 863 | 258 |
| 400 contrôleurs désactivés, 1er août 1776 | 24 714 | 746 | 6 655 / 104 800 | 1 295 |
| Monde mature, 21 avril 1777 | 28 217 | 1 226 | 7 730 / 106 293 | 1 469 |

La baisse des profits négatifs et la réorganisation des objets POP existent aussi avec les flags IA désactivés. Les compteurs d'investissement autonome échoué continuent également à croître dans ces mondes rapides. Leur présence ne suffit donc pas à expliquer le surcoût associé aux 400 contrôleurs. Les dates différentes interdisent d'en déduire des coûts ou des taux causaux comparables. Les 38 090 entrées initiales `country_goal` sont des cibles diplomatiques/relations, pas une file de construction.

L'augmentation du nombre d'objets bâtiment comprend des objets de niveau zéro. Par exemple, 301 objets de secteur de construction en mars ne signifient pas 301 secteurs achevés : ils représentent 116 niveaux et incluent 197 objets vides. Le monde mature rapide contient davantage d'objets bâtiment et de formations que S0 ; le simple nombre total de ces objets ne constitue pas une explication suffisante du ralentissement initial.

Les scores de construction du moteur peuvent appeler du script moddé : l'inventaire statique du runtime figé compte **12 blocs `ai_value` dans neuf fichiers** avec des callbacks `aor1776_ai_…`, notamment dans `common/buildings/01_industry.txt`. Ils consultent les triggers de pénurie régionale et parfois `any_scope_building`. Désactiver le **contrôleur mensuel** régional n'équivaut pas à retirer ces callbacks par candidat. Leur fréquence et leur coût effectifs restent à mesurer ; l'inventaire est dans `MODDED_AI_SCORE_CALLBACK_INVENTORY_20261118.json` hors dépôt. Aucun de ces callbacks n'a été modifié dans le mod principal.

## 5. Référence vanilla et inspection native

La comparaison vanilla et les limites de sa préparation sont consignées dans [VANILLA_REFERENCE_FR.md](VANILLA_REFERENCE_FR.md). Elle utilise la même installation Steam et l'instrumentation commune, avec le runtime du mod absent. Le monde initial comporte 449 contrôleurs, dont 158 décentralisés et 291 autres, et environ 1,022 milliard de personnes contre 837 millions dans S0 du mod. Les pays, technologies, bâtiments, marchés, date et vue ne doivent pas être supposés équivalents.

La référence est effectivement exécutée puis répétée : ancien Q1 ON 13/23/45 s contre OFF 10/18/34 ; nouvelle paire C1 OFF 6/20/50 contre ON 7/13/26, avec préparation inégale ; répétition inversée R ON 7/14/28 contre OFF 14/29/42, avec préparation rapprochée à environ 220/224 secondes. Les POST natifs confirment tous les flags attendus (450 actifs avec un nouveau pays dans ON, 449 inactifs dans OFF). Les deux paires nouvelles ont exactement les mêmes 6 302 ressources natives entre leurs conditions. **Le nouveau lot montre OFF plus lent et contredit Q1 ; aucun coût vanilla stable de l'IA ni pénalité du mod n'est déduit.** Les résultats contradictoires et les limites de premier plan/préparation restent explicitement conservés.

L'inspection des objectifs et scores économiques, ainsi que le contrôle de persistance de la variante PM, sont détaillés dans [ECONOMIC_INSPECTION_FR.md](ECONOMIC_INSPECTION_FR.md). Les résultats préparés ne sont pas comptés comme exécutés.

Le profileur Jomini a effectivement commencé une capture dans EXB1 **après** les fenêtres de mesure. L'interface a affiché 456 ticks capturés, puis une durée de capture croissante, mais aucune table de coûts exploitable ; le texte des échantillons était tronqué. Le bouton « Stop capture » n'a pas été actionné avant la fermeture du processus. Cela ne démontre ni zéro échantillon, ni un coût nul des scripts. Une image de preuve est conservée hors dépôt. Les anciens profils Legacy et la table TickTask sont partiels et ne fournissent pas de pile CPU native ni de décomposition exclusive complète. Les restrictions Windows de profilage n'ont pas été contournées.

**Nouvelle collecte effectivement terminée, PROFC1 :** l'activation Legacy est confirmée par le moteur, puis un export natif contient 5 003 entrées, avec secondes et nombres d'appels explicitement déclarés. Huit emplacements des douze priorités testées sont observés ; leurs temps rapportés sont faibles, par exemple 0,054465 seconde pour 5 998 appels des chemins de fer. La sauvegarde native du 1er avril confirme 646 contrôleurs actifs et les objectifs/payloads attendus. Cette collecte distincte couvre la simulation jusqu'au dernier DAY complet du 7 avril, ainsi que des périodes en pause et l'autosave ; elle est exclue des benchmarks. Elle ne représente ni une décomposition CPU exclusive ni tous les appels natifs. Voir [SCRIPT_PROFILE_FR.md](SCRIPT_PROFILE_FR.md).

Le score de région stratégique de `00_default_strategy.txt:4526`, observé 76 704 fois pour 0,617669 seconde, ne doit pas être confondu avec le contrôleur d'infrastructure régionale. Les 260 103 appels du trigger de dette diplomatique rapportent seulement 0,163887 seconde dans cette capture : beaucoup d'appels ne signifie pas automatiquement une grosse part du ralentissement. Aucun de ces classements ne justifie seul un correctif.

## 6. Confiance et prochaine expérience

- **Confiance élevée :** association du surcoût initial aux contrôleurs non décentralisés ; répétition du contraste global dans l'ordre inversé ; recréation précoce des objectifs d'extension retirés des sauvegardes.
- **Confiance limitée :** contribution exacte de l'extension, des PM, des stratégies, de la construction publique ou de l'investissement privé. Aucun de ces coûts n'est isolé par le seul retrait d'instances sérialisées.
- **Non démontré :** calcul nécessaire exceptionnellement lourd, travail redondant, callbacks moddés trop souvent appelés, réaction native à l'économie de 1776, cache persistant ou variable temporaire précise. Ces explications peuvent coexister. Le contraste initial/mature persistant après redémarrage soutient une composante liée à l'état du monde, sans désigner le champ responsable.

Le test des **callbacks moddés de priorité de construction** a désormais été exécuté et répété. Tous les contrôleurs, objectifs natifs et routines normales restent actifs ; seuls douze blocs `ai_value` dans neuf fichiers sont remplacés par leurs bases. Les deux vérifications natives de chargement confirment exactement ces neuf différences parmi 7 412 chemins virtuels, sans ajout ni retrait. La même interface et les mêmes réglages stabilisés sont partagés entre les conditions.

| Ordre réel | Condition | 14 j | 28 j | 56 j |
|---|---|---:|---:|---:|
| SCORC1 | Douze scores remplacés par leur base | 30 s | 56 s | 100 s |
| ECNC1 | Témoin normal | 30 s | 55 s | 96 s |
| ECNC2 | Témoin normal répété | 27 s | 52 s | 94 s |
| SCORC2 | Diagnostic répété | 31 s | 59 s | 102 s |

**Aucun gain observé.** Les diagnostics sont plus lents dans ces deux paires ; deux processus par condition et les variations de la machine ne démontrent pas une aggravation intrinsèque. Moyennes descriptives : 95 contre 101 secondes. Le détail, les CPU et les limites figurent dans [SCORE_CALLBACK_RESULTS_FR.md](SCORE_CALLBACK_RESULTS_FR.md). Les 14/28/56 jours sont imbriqués, pas trois répétitions indépendantes.

Les quatre POST natifs du 1er avril conservent 646 contrôleurs actifs et tous les objectifs attendus. Dans chacune des deux paires, **83 sections sérialisées sont strictement identiques ; seul `local_date_time` diffère**. Cette observation n'établit ni l'identité des décisions intermédiaires, ni la fréquence d'exécution des callbacks, ni l'équivalence pour d'autres campagnes ou dates.

Cette série C, décrite dans [PROTOCOL_STABLE_FR.md](PROTOCOL_STABLE_FR.md), utilise un nouveau réglage commun `9a759fceadc82095774b75030159250f67b51b488d192d0239f96f42a27e26c4` : fenêtre 1600×900 sur le seul écran secondaire, panoramique involontaire désactivé et contrôles de capture communs. Les anciens réglages 49c…/718e… et les prises G/Q restent des lots distincts. SCORG1, 29/57/103 s, est explicitement confondu par un panneau de carte différent ; SCORQ1, 52/101/174 s, n'a pas de témoin contemporain terminé. Aucune de ces deux prises n'est agrégée aux C. SCORG2 et SCORP1 restent des préparations écartées, sans résultat de débit accepté.

**Contrôle positif contemporain AIOFFC1 : 6/12/25 secondes.** Seuls les 646 flags `AI.enabled` de la copie initiale changent ; leur restauration reconstitue exactement la source normale. Même exécutable, runtime, réglages et instrumentation que les C normaux. La sauvegarde native du 1er avril confirme les 646 flags inactifs et les objectifs conservés. Le contraste avec les témoins 94–96 secondes persiste donc dans ce cadre. Il s'agit d'une ablation globale, non d'une optimisation de gameplay ni d'une décomposition additive des coûts.

La prochaine investigation informative doit vérifier les **appels effectivement exécutés** avec un profil natif exploitable, ou trouver un contrôle persistant d'une seule catégorie : rentabilité, construction publique, investissement privé ou sélection des PM. La suppression de blocs qui se recréent n'est pas une méthode suffisante. Les commandes d'évaluation préparées ne sont pas comptées comme exécutées. Un profil script ne remplace pas des piles CPU natives, et les limites du profilage Windows restent respectées.

Une éventuelle optimisation n'est justifiée qu'après identification reproductible d'un coût et preuve que son évitement, sa mise en cache ou une réorganisation des conditions conserve les décisions et résultats attendus. Aucune modification de fréquence IA, de répartition des pays, de population ou de structure économique n'est proposée comme correctif validé.

## 7. Préservation et reprise

Le contrôle à 18:01 UTC constate inchangés les 2 996 fichiers du mod principal, les 2 996 fichiers de la copie figée, les 80 fichiers surveillés du profil normal courant, les trois fichiers diplomatiques Russie–Petite Horde kazakhe protégés, l'index Git, l'exécutable Steam, 472 anciens rapports et 38 anciens outils. Les nouveaux outils et rapports de cette mission s'ajoutent dans leurs périmètres propres. Les contrôles et leur moment figurent dans les reçus de préservation.

Les sept modifications normales constatées lors de la précédente interruption restent préservées sans restauration. La base courante `launcher-v2.sqlite`, SHA-256 `93e44a0dcf07dffc007762903cc3077367d951923589f6a48cac01bc2b3b7620`, a été copiée et examinée : changements de taille de mod, horodatages de synchronisation et un statut de playset actif ; compositions des sept playsets, onze liens de mods et 51 liens DLC inchangés. L'auteur de ces écritures n'est pas établi. Il ne faut pas restaurer une ancienne base pour effacer ces différences.

COMPACT reste à l'empreinte `94fb72b75640fe1c8bbde01af235993225dff662d11974c8a267eaeca85ff9c0`. Les sauvegardes normales, travaux historiques et modifications Git existantes ne sont pas remplacés. Les paramètres réécrits par un jeu d'essai restent dans son profil isolé ; le garde-fou d'empreinte refuse leur réutilisation aveugle.

Pour reprendre, lire ce rapport, les deux compléments, `MEASUREMENT_QUALITY.json` et le `RUN_STATE.md` externe. Ne pas relancer les variantes d'objectifs comme si leur persistance était acquise. Les processus de test sont limités à leur propre profil `--userdir` ; leur arrêt contrôlé ne doit jamais viser une session normale de Victoria 3.

### Audit final du 19 novembre, après fermeture des essais

Le reçu [PRESERVATION_FINAL_20261119.json](PRESERVATION_FINAL_20261119.json), démarré à 02:36:53 UTC après la dernière fermeture, confirme **zéro différence** dans chacun des neuf groupes : mod principal 2 996/2 996 ; copie figée 2 996/2 996 ; profil normal 80/80 ; diplomatie protégée 3/3 ; index Git 1/1 ; exécutable Steam 1/1 ; anciens rapports 472/472 ; anciens outils 38/38 ; références 4/4. Le HEAD reste inchangé. Le contrôle des processus ne retrouve plus de Victoria 3 après les essais. Les paramètres expérimentaux restent dans leurs profils temporaires ; aucune ancienne base du lanceur n'est restaurée.

L'export final comporte **71 lignes temporelles**, avec les fenêtres partielles, les traitements invalidés et les comparaisons confondues clairement marqués. AI_DEC1 conserve ses temps mais est exclu d'une comparaison causale stricte à cohorte fixe, car son POST perd un contrôleur dont la date de disparition n'est pas établie ici. Le premier export a été préservé dans `export_initial_review_20261119` avant la correction de ce seul indicateur d'éligibilité ; aucun temps ni preuve brute n'a été modifié. [SUMMARY.json](SUMMARY.json) indexe les résultats actuels, leurs preuves et leurs limites.

## 8. Bilan de cette passe et travail restant

**Terminé :** reprise et vérification de l'ablation d'extension, preuve native de sa recréation précoce ; test répété des douze priorités moddés avec témoins contemporains, sans gain ; contrôle positif global IA contemporain ; référence vanilla exécutée et répétée en ordre inversé ; export natif des appels de scripts ; audits de préservation et export des mesures/qualités. Les épisodes de capture ont été récupérés sans demander de nouvelle manipulation au joueur pendant cette reprise. Le grand écran est resté libre des fenêtres de jeu ; les dimensions du bureau normal n'ont pas été changées.

**Ce qui reste inconnu :** la part propre de la rentabilité native, du parcours des candidats, de l'extension publique, de l'investissement privé et des PM ; la raison de l'inversion et de la variabilité des références vanilla ; le champ d'état du monde qui produit le contraste initial/mature. Le profil Legacy n'expose pas l'ensemble de ces opérations natives, et aucune pile CPU moteur complète n'est obtenue. Les commandes d'évaluation individuelles préparées ne sont pas comptées comme exécutées. Les contrôles actuels ne fournissent pas encore un arrêt persistant vérifié de chacune des catégories économiques.

**Prochain test à plus forte valeur diagnostique :** rechercher dans l'aide native un contrôle persistant d'une seule catégorie construction/rentabilité, vérifier son activité et son arrêt effectif au début et à la fin, puis l'apparier à un témoin normal sur la même S0 et dans l'ordre inversé. Si aucun contrôle adapté n'est exposé, obtenir une trace native de tâches ou un profil moteur pris en charge comparant le début de 1776 au monde mature. Les outils peuvent assurer le lancement isolé, les mesures DAY, les sauvegardes et leur analyse ; l'absence d'accès aux opérations natives internes limite l'attribution, pas l'exécution des benchmarks déjà obtenus.

Aucun retrait de pays/POP, changement de fréquence IA ou rééquilibrage spéculatif n'est proposé. **Aucune optimisation préservant le gameplay n'est démontrée ; aucune variante diagnostique n'est intégrée, commitée, poussée ou fusionnée.** L'enquête reste ouverte.

Le [bilan de cette passe dans l'Issue #56](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/56#issuecomment-6995976162) est publié et relu à l'identique. Le corps historique de l'issue est strictement conservé. Le commentaire public contient les mesures et leurs limites ; les chemins Windows, détails du matériel, empreintes et fichiers volumineux restent locaux. [GITHUB_PUBLICATION_20261119.json](GITHUB_PUBLICATION_20261119.json) conserve le reçu de publication et la résolution du refus initial de remplacement détaillé par cette publication limitée.
