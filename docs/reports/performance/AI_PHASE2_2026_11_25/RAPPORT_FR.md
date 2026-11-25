# 1776 Age of Revolutions — IA des pays mineurs, phase 2

Le point de départ est le commit `50e718767918fb10b9a7fcc9f8f7e3490091646d`, `performance_SLAY_IA`. Son diff de gameplay et de localisation par rapport à `bd776919` est vide. Les tests utilisent donc le mod figé de la phase précédente, COMPACT compris, ainsi que les cultures et la population d’origine. La consolidation reste suspendue dans [#58](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/58). [Rapport de phase 1](../AGGRESSIVE_2026_11_24/RAPPORT_FR.md)

Les 39 fusions de la phase précédente avaient fait passer les définitions de culture de 324 à 285 et les POP sérialisés du 1er janvier de 31 482 à 30 219 (−4,0 %). La population initialisée passait de 837 119 763 à 837 119 765. L’écart de POP observé en juillet descendait à 1,47 %, avec des trajectoires de campagne différentes. Les chronos n’établissaient pas de gain propre aux fusions. [Liste des 39 fusions expérimentales](../AGGRESSIVE_2026_11_24/FUSIONS_CULTURELLES.tsv)

## Contrôleurs natifs et stratégies

L’exécutable Steam de Victoria 3 1.15.2 correspond à l’empreinte SHA-256 `57c4950e9f1046d61729e8faeedbbdbb7aa30ff2a45788217285eb735491ad36`. Le registre généré du moteur expose `set_strategy`, `has_strategy`, `is_ai` et `is_player`. `on_game_started_after_lobby` permet d’appliquer une politique après l’attribution des pays aux joueurs. Les hooks diplomatiques et les itérateurs de conflit donnent accès aux pays impliqués. La revue ciblée des effets, déclencheurs, règles, historiques d’IA et définitions n’a identifié aucun effet scripté documenté qui écrive le drapeau de contrôleur `ai.enabled`.

`common/defines/00_ai.txt` expose des interrupteurs globaux pour la construction publique, l’investissement et certaines dépenses. Les essais précédents les ont testés séparément. La suppression des chantiers privés a vidé la file correspondante, tandis que le temps sur 56 jours est resté à 119 s contre 121 s pour le témoin. Les trois essais ont conservé 646 contrôleurs et 400 objectifs d’expansion sérialisés. ARoAI, conçu pour Victoria 3 1.3.6, montre que l’on peut remplacer une partie des décisions économiques au moyen de ces interrupteurs globaux et de scripts. Il ne démontre pas l’arrêt sélectif de contrôleurs en 1.15.2. [Essais des interrupteurs](../INITIAL_SIMULATION_ISSUE56_2026_11_17/NATIVE_CATEGORIES_2026_11_23/RESULTS_FR.md) · [Documentation d’ARoAI](https://github.com/Anbeeld/ARoAI/blob/main/docs/analysis.md)

La stratégie par défaut fournit les scores de base du moteur. D’autres stratégies peuvent les compléter. Une stratégie vide ou une valeur de construction faible laisse le contrôleur et ses calculs natifs actifs. Les changements de comportements et les chronos doivent être mesurés séparément. [Journal développeur de Paradox](https://www.paradoxinteractive.com/games/victoria-3/news/victoria-3-dev-diary-59-ai) · [Registre public de modding 1.15.0](https://github.com/Victoria-3-Modding-Co-op/Modding-Digests/blob/main/1.15.0/types/changes_script_docs.md)

### Commandes depuis l’interface hors debug

Le registre `data_types_gui.txt` de 1.15.2 documente `ExecuteConsoleCommand` et `ExecuteConsoleCommands`. Le second accepte une suite de commandes et s’arrête à la première erreur. Le jeu de base utilise les deux dans ses interfaces de développement. Le premier essai normal enchaînait deux appels dans la même animation. Le moteur a refusé le second pendant le traitement du premier. La sauvegarde binaire de ce passage contenait 646 drapeaux actifs.

Le second essai appelle uniquement `disable_ai RAG` depuis l’interface au lancement d’une nouvelle campagne. Le processus est lancé sans `-debug_mode`. Le moteur confirme `Disabled AI` et sauvegarde exactement un drapeau désactivé, celui de Raguse. Les 645 autres restent actifs. Ce résultat atteste une voie par l’interface dans ce contexte. Les effets disponibles aux scripts de pays constituent une autre interface du moteur.

Le générateur [`build_native_overlay.py`](../../../../tools/performance/ai_phase2_2026_11_25/build_native_overlay.py) prépare un prototype solo et hors Ironman. Il groupe les commandes après le lobby et vérifie le statut de chaque pays avant de l’ajouter. Le réglage par défaut conserve l’IA complète. Une campagne neuve hors debug a été créée avec la variante et Raguse, candidate du lot E, comme pays joué. La sauvegarde a exactement **269 drapeaux désactivés** et **377 actifs**, dont Raguse. Les 269 tags correspondent à E sans le pays joué. Le marqueur de traitement de l’interface est sérialisé. La désactivation se fait en **12 lots**, espacés de quatre secondes dans ce prototype. Le traitement s’amorce pendant la pause du 1er janvier 1776. Il faut encore gérer un dépausé immédiat, un traitement partiel et la reprise après erreur. Les chronos obtenus sur des sauvegardes déjà configurées excluent ce traitement initial. [Contrôles binaires](PREUVES_NATIVE.json)

### Réveil d’un contrôleur pendant un conflit

Le jeu a chargé hors debug la copie binaire E et simulé jusqu’en avril. Un effet de laboratoire a ouvert une guerre entre la France jouée et Modène, dont le drapeau était à `no`. Douze jours après le début de l’essai, le moteur confirme que Modène combat la France, qu’elle possède une formation et que celle-ci reste démobilisée à cet instant. La condition du conflit déclenche alors une demande côté script. L’interface lit cette demande avec `ScriptedGui.IsValid` et appelle `enable_ai MOD`. Le moteur confirme la commande. L’autosauvegarde du 1er avril montre le drapeau de Modène actif.

Ce test démontre le transfert d’une demande du script à l’interface et la réactivation native pendant un conflit. Il porte sur un pays, avec un déclenchement retardé pour observer sa formation avant le réveil.

Un deuxième essai recharge la campagne de Raguse créée par le prototype de démarrage. Le jeu ouvre un conflit diplomatique direct contre Modène le 2 janvier à faible escalade. Le hook demande son réveil à la même seconde. Le premier relais générique transmet « Modène » au moteur, qui exige `MOD` et répond `Could not find country`. Le 1er avril, les 269 drapeaux initialement arrêtés, dont Modène, le sont toujours. Le relais corrigé lit le tag avec `Country.GetTagName` et attend le retrait de la demande avant d’autoriser un nouvel envoi. [Preuve du premier essai](PREUVES_NATIVE.json)

L’essai corrigé, en solo hors debug, recharge le même fichier natif. Le moteur reçoit et accepte `enable_ai MOD` deux secondes après l’ouverture du jeu diplomatique le 2 janvier. Modène a mobilisé au moins une formation le 14 janvier. Le 1er avril, le fichier natif enregistre **378 drapeaux actifs et 268 inactifs**, contre 377 et 269 au départ. Modène est le seul pays qui change de drapeau et aucune commande de désactivation de départ n’est rejouée. La sonde ouvre le conflit depuis le pays contrôlé par le joueur. Le hook de jeu diplomatique, puis l’interface, traitent la demande sans appel direct de la sonde à la commande. Une relance intermédiaire restée en pause au 1er janvier est exclue. [Journaux et contrôles binaires](PREUVES_NATIVE.json)

Le menu vanilla expose `PauseMenu.SwitchCountry`. Les hooks de conflit exposent `on_diplo_play_join_side` et `on_war_end`. Ce dernier fournit les belligérants principaux et permettrait de programmer un contrôle à la fin d’un délai pour les seuls pays réveillés. Le prototype de réactivation ne couvre actuellement que les deux parties principales d’un jeu diplomatique ou d’une guerre. Les changements de pays, les interventions de tiers et les pactes conclus en cours de partie restent à qualifier.

## Prototype de règle de partie

Le générateur `build_passive_overlay.py` crée une surcouche expérimentale hors du dépôt. Le réglage « IA complète » est la valeur par défaut du générateur. Le réglage « IA passive » marque les pays du lot E après la sélection des joueurs. Pour un pays marqué, la surcouche écarte les objectifs régionaux génériques et réduit les scores de construction, d’agressivité et de changement de loi. Elle ne bascule aucun drapeau de contrôleur et n’altère ni les règles de population ni les bâtiments initiaux.

La condition exclut les pays contrôlés par un joueur, ses sujets directs et les pays partageant un conflit avec lui. Elle consulte les participants du pays en cours d’évaluation. Elle n’ajoute aucune vérification mondiale quotidienne. La fin d’une guerre entre deux belligérants principaux dont l’un est humain peut prolonger la période d’activité du pays mineur de 60 jours. La couverture des traités, des conflits à plusieurs participants et des résolutions diplomatiques doit être vérifiée séparément.

### Deux campagnes neuves avec la règle

Les deux campagnes ont été créées dans l’interface normale, avec la France et les POP d’origine. Le mode debug sert aux marqueurs de mesure. Les surcouches ne diffèrent que par la valeur par défaut de la règle. Le moteur enregistre les deux réglages. Avec le réglage passif, les 270 marqueurs sont présents au départ et au 1er juillet. Le déclencheur effectif est vrai pour 268 pays lors de la création. Avec « IA complète », aucun pays ne reçoit le marqueur. Les deux campagnes gardent 646 contrôleurs actifs, France comprise.

| Règle | 14 j | 28 j | 56 j | 180 j | CPU moyen | RAM moyenne / pic, Mio | Intervalle P95 / maximum | Initialisation / lancement au premier jour |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| IA complète | 40 s | 75 s | 133 s | 275 s | 18,5 % | 10 635 / 11 558 | 3 / 4 s | 175,3 / 321,8 s |
| IA passive | 37 s | 69 s | 121 s | 254 s | 19,6 % | 11 025 / 13 775 | 3 / 4 s | 219,5 / 355,3 s |

Le temps baisse de 9 % sur 56 jours et de 8 % sur six mois, sur une seule paire. Ces écarts sont inférieurs aux écarts entre témoins en phase 2. La mémoire et le CPU moyen augmentent, tandis que les intervalles quotidiens sont stables. Les files de construction de juillet restent similaires. Le Yungui passe de 18 à 16 ordres publics, la Valachie reste à 8 et Malte passe de 2 à 4. Des armées se développent dans les deux campagnes. La règle active bien le traitement scripté, dont l’effet sur le coût global et sur l’activité autonome est insuffisant pour la recommander en production.

Une autre campagne a été lancée sans debug avec Raguse choisie depuis le menu. Le jeu enregistre Raguse comme pays humain et l’exclut de la condition passive. Un effet de laboratoire met Raguse en conflit avec Malte. La sauvegarde confirme que Malte satisfaisait la condition passive avant l’effet et qu’elle ne la satisfaisait plus pendant le conflit. Le journal signale un champ `initiator` superflu dans l’effet de test. Les marqueurs du jeu attestent le conflit malgré cet avertissement. Les 646 contrôleurs restent actifs dans cette prise, qui mesure le changement de stratégie.

## Protocole des copies de sauvegarde

Les profils A à F chargent la même sauvegarde native du 1er janvier 1776, créée dans l’interface de Victoria 3 1.15.2, SHA-256 `0254c0fc1e447a135ccc0c738270688479ae633244d523bb8c3d0f272863dece`. La France reste le pays joueur. Les copies diffèrent uniquement par les valeurs `ai.enabled` choisies. Le chronomètre lit les marqueurs du moteur du 2 janvier au 1er juillet à vitesse 5. La première série utilise l’écran principal, seul moniteur détecté au départ. Le témoin `P2A3` s’est interrompu avant le premier jour simulé et est exclu. La reprise utilise le deuxième écran, avec un nouveau témoin pour cette série. Les mesures en campagne neuve restent distinctes des essais de copies de sauvegarde.

Le laboratoire utilise Windows 11, un AMD Ryzen 7 8845HS à 16 processeurs logiques, la Radeon 780M et 31,26 Gio de RAM visibles par Windows. Le CPU moyen est la part cumulée du processus sur les 16 processeurs logiques. La RAM correspond à la mémoire résidente du processus. Les intervalles entre jours proviennent de dates émises par le moteur à la seconde près. Le P95 et le maximum décrivent les ralentissements de la simulation à cette résolution. Le chargement complet est compté séparément, depuis le lancement jusqu’au premier jour simulé.

| Lot | Candidats désactivés | Drapeaux actifs au départ | Pays autonomes en solo avec la France |
| --- | ---: | ---: | ---: |
| A — Témoin | 0 | 646 | 645 |
| B — Modéré | 170 | 476 | 475 |
| C — Seuil de 250 000 | 293 | 353 | 352 |
| D — Agressif | 386 | 260 | 259 |
| E — Agressif, décentralisés conservés | 270 | 376 | 375 |
| F — E avec deux exceptions historiques | 268 | 378 | 377 |

Le lot E conserve les 116 pays décentralisés que D désactive. C et E partagent 209 pays. Les 84 pays propres à C sont décentralisés. Les 61 propres à E relèvent du seuil plus large de D. La comparaison D–E isole l’effet des décentralisés. La comparaison C–E mesure deux classifications différentes. [Listes intégrales des cohortes](COHORTES_PHASE2.csv)

Le seuil croise population, territoire et rôle dans le scénario. Les électorats et gouvernements impériaux retenus en phase 1 gardent leur IA. La Valachie, la Moldavie et la Transylvanie dépassent chacune 1,4 million d’habitants. Le Yungui en compte 8,1 millions. Ces pays sont des inclusions régionales explicites. F protège la Transylvanie (`TRS`), désignée par le journal de la révolution hongroise, et l’Ili (`XIN`), que la fragmentation chinoise peut doter d’une stratégie d’unification. Les entrées balkaniques traitent aussi la Moldavie et la Valachie. F garde ces deux pays dans le lot afin de mesurer un compromis avec seulement deux exceptions supplémentaires. [Inventaire des pays et exceptions](../AGGRESSIVE_2026_11_24/INVENTAIRE_PAYS.csv)

E comprend 178 pays non reconnus, 86 reconnus et 6 administrations coloniales. Les six sont l’Alaska, Cuba, Santo Domingo, Haïti, Porto Rico et la Sierra Leone. L’Inde et la Grande Perse restent particulièrement sensibles aux pactes de sujétion et aux crises régionales. Les fichiers de cohorte permettent de revoir chaque cas d’après sa région, ses pactes et son rôle.

## Chronos de la première série

| Passage | 14 j | 28 j | 56 j | 180 j | CPU moyen | RAM moyenne / pic, Mio | Intervalle P95 / maximum | Initialisation / lancement au premier jour |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A1 — Témoin | 41 s | 80 s | 139 s | 302 s | 19,2 % | 7 606 / 8 060 | 3 / 5 s | 264,5 / 358,0 s |
| C — 293 IA | 29 s | 52 s | 96 s | 216 s | 18,2 % | 10 547 / 10 860 | 2 / 4 s | 272,0 / 356,1 s |
| A2 — Témoin | 41 s | 73 s | 117 s | 217 s | 22,1 % | 9 994 / 11 002 | 3 / 4 s | 195,5 / 278,7 s |
| E — 270 IA | 32 s | 53 s | 96 s | 223 s | 17,1 % | 9 321 / 9 847 | 2 / 3 s | 224,2 / 309,5 s |

Le premier passage de C et celui d’E gagnent 18 à 31 % sur 56 jours selon le témoin. Sur six mois, C rejoint le témoin rapide et E se trouve dans la plage des deux témoins. Les 293 drapeaux désactivés de C et les 270 d’E, ainsi que le drapeau actif de la France, sont confirmés au départ, en avril et en juillet. Les écarts de RAM et d’initialisation varient entre passages. [Chronos détaillés](BENCHMARKS_PHASE2.csv)

## Chronos de la reprise sur le deuxième écran

| Passage | 14 j | 28 j | 56 j | 180 j | CPU moyen | RAM moyenne / pic, Mio | Intervalle P95 / maximum | Initialisation / lancement au premier jour |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| A5 — Témoin | 41 s | 81 s | 160 s | 306 s | 22,0 % | 11 188 / 11 443 | 4 / 8 s | 329,8 / 411,4 s |
| D — 386 IA | 37 s | 74 s | 129 s | 252 s | 21,8 % | 11 491 / 13 079 | 4 / 5 s | 337,3 / 439,1 s |
| E — 270 IA | 46 s | 75 s | 127 s | 235 s | 21,8 % | 16 160 / 16 727 | 3 / 6 s | 223,5 / 326,3 s |
| B — 170 IA | 27 s | 60 s | 100 s | 200 s | 23,0 % | 14 095 / 16 346 | 2 / 5 s | 152,5 / 236,7 s |
| F — 268 IA | 26 s | 47 s | 78 s | 168 s | 23,6 % | 16 781 / 16 918 | 2 / 3 s | 154,7 / 237,0 s |

A5, D, E et B utilisent une fenêtre de 1 600 × 900 sur le deuxième écran, la même copie de départ et les mêmes réglages. D prend 2 secondes de plus qu’E sur 56 jours et 17 secondes de plus sur six mois. Cette paire n’établit aucun intérêt à arrêter les 116 contrôleurs décentralisés supplémentaires. B donne le meilleur chrono de cette série, avec des gains de 37,5 % à 56 jours et de 34,6 % à six mois face à A5. Face au témoin le plus rapide de la première série, l’écart tombe à 14,5 % et 7,8 %. Dans la phase précédente, le lot modéré avait mis 135 et 253 secondes sur un autre départ. Les mesures ne démontrent pas de gain proportionnel au nombre d’IA arrêtées.

En juillet, A5 conserve 646 contrôleurs actifs et E 376 actifs avec 270 arrêtés. Cooch Behar a disparu dans B et D. B compte alors 475 actifs et 170 arrêtés, et D 260 actifs et 385 arrêtés. Aucun drapeau des pays restants n’a changé dans les quatre essais et celui de la France reste actif. La RAM augmente dans les trois variantes de cette série. [Chronos détaillés](BENCHMARKS_PHASE2.csv)

F a été mesuré ensuite sur le même écran et avec le même départ. Ses 378 drapeaux actifs et 268 inactifs persistent au 1er avril et au 1er juillet. Le gain atteint 51 % sur 56 jours et 45 % sur six mois face à A5, ou 33 % et 23 % face au témoin A2, le plus rapide. Le temps CPU cumulé passe d’environ 1 079 à 633 secondes processeur face à A5. La mémoire résidente moyenne augmente, de 10,9 à 16,4 Gio. Ce passage unique ne permet pas d’attribuer l’écart entre E et F aux deux exceptions. Les chronos du tableau partent de sauvegardes préconfigurées et le nombre arrêté par la règle peut être plus faible si le joueur choisit un pays du lot ou en est le suzerain direct. [Chronos détaillés](BENCHMARKS_PHASE2.csv)

## Activité des pays dont le contrôleur est arrêté

Les sauvegardes du départ et du 1er juillet montrent que les budgets, les marchés, la production et la démographie continuent d’évoluer dans des pays dont le drapeau reste à `no`. Les huit pays ciblés de l’échantillon affichent encore des recettes fiscales et des bâtiments produisant des biens au 1er juillet. Les chiffres sont tirés du budget et des objets du moteur. [Relevés des huit pays et de la France](ACTIVITE_PAYS.json)

| Pays avec IA désactivée dans E | Population, janvier → juillet | Trésorerie, janvier → juillet | Recettes fiscales sérialisées, juillet | Dépenses hebdomadaires, juillet | Bâtiments produisant, juillet | Unités en juillet, témoin → E |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Modène | 495 752 → 499 806 | 6 875 → 28 058 | 1 230 | 1 102 | 3 | 5 → 5 |
| Valachie | 1 782 292 → 1 796 532 | 15 339 → 110 452 | 5 561 | 1 020 | 1 | 30 → 6 |
| Yungui | 8 100 000 → 8 132 353 | 45 401 → 189 530 | 6 507 | 2 374 | 4 | 24 → 0 |
| Raguse | 30 000 → 30 168 | 461 → 9 595 | 36 | 104 | 3 | 1 → 0 |

Les ordres publics du témoin atteignent 20 au Yungui et 8 en Valachie au 1er juillet. Les huit pays ciblés de l’échantillon n’ont alors ni ordre public ni ordre privé dans E. Le témoin contient un ordre privé au Yungui. Ces valeurs décrivent les files à une date donnée. Elles ne mesurent pas les investissements déjà terminés. Raguse change de marché dans les deux prises et conserve son entrée `je_abolish_monarchy` dans la sauvegarde E. La présence de l’entrée n’atteste pas la réalisation de ses actions. Les données ne séparent pas les migrations du solde naturel et ne démontrent pas le déclenchement d’une révolution dans les pays ciblés.

Dans la copie de combat, des effets scriptés font de Malte un protectorat français et annexent le Monténégro. Le moteur confirme les deux résultats alors que leurs contrôleurs étaient arrêtés au départ. La sauvegarde passe de 376 actifs et 270 inactifs à 377 et 268. L’écart correspond au réveil de Modène et à la disparition du Monténégro. Le premier essai de changement de loi à Malte utilisait une référence rejetée. Dans la campagne suivante, la sonde emploie `law_type:` et confirme le changement deux jours après application. L’IA de Malte est désactivée au départ et en avril. Une acceptation diplomatique autonome ou une révolution demande un autre contrôle.

## Distribution éventuelle

| Méthode | Démarrage et sélection | Workshop et multijoueur | Maintenance |
| --- | --- | --- | --- |
| Règle lançant les commandes natives depuis l’interface | Désactivation individuelle attestée en campagne neuve. Réveil et mobilisation vérifiés dès un jeu diplomatique direct | Surcouche de données et d’interface. Le prototype bloque l’appel en multijoueur et en Ironman | Vérifier l’interface, les commandes, la fin de traitement et les hooks de conflit à chaque mise à jour |
| Règle scriptée de passivité | Nouvelle campagne et sélection habituelle quand la règle fonctionne | Fichiers de mod usuels. Synchronisation multijoueur à tester | Vérifier les objectifs régionaux et valeurs modifiés à chaque mise à jour |
| Sauvegarde de départ préconfigurée | Charger une partie déjà créée avec un pays et des règles fixés. Changement de pays à éprouver | Diffusion distincte du lancement standard du Workshop. Partie multijoueur à tester | Regénérer après les mises à jour du moteur et du scénario. Réactivation dynamique à démontrer |
| Outil de copie locale | Choisir son pays puis créer une nouvelle copie à partir de la sauvegarde initiale | Utilitaire séparé du Workshop. Prototype limité aux départs solo de 1776 en 1.15.2 | Revalider les deux formats du moteur, les tags et la protection du pays joué |
| Scénario séparé | Sélection normale possible pour une variante fondée sur des stratégies | Même contrainte de contrôleur que le scénario principal | Reprise des changements de la carte et du contenu. Coût d’entretien supérieur à une règle |

Les générateurs produisent deux surcouches dans de nouveaux répertoires du laboratoire. La surcouche de réveil reprend le `timemanip.gui` généré au démarrage et se charge après la surcouche de départ. Les autres fichiers des deux surcouches restent nécessaires. Les arguments `--cohort B`, `C`, `D`, `E` ou `F` choisissent la liste compilée dans un profil. La règle en jeu oppose l’IA complète et le lot compilé. Une règle à plusieurs niveaux réunis dans le même profil reste à valider.

```text
python tools/performance/ai_phase2_2026_11_25/build_native_overlay.py "<Steam>/game/gui/timemanip.gui" "<laboratoire>/phase2-start" --cohort F
python tools/performance/ai_phase2_2026_11_25/build_native_wake_overlay.py "<laboratoire>/phase2-start/gui/timemanip.gui" "<laboratoire>/phase2-wake" --cohort F
```

L’outil [`copy_ai_save.py`](../../../../tools/performance/ai_phase2_2026_11_25/copy_ai_save.py) vérifie le format, la version, la date, l’absence d’Ironman et l’identité du pays joué. Il protège ce dernier et crée un nouveau fichier. Sur le départ texte, sa sortie est identique à la copie E chargée par le jeu. Sur le départ créé hors debug, la sauvegarde contient un conteneur ZIP et deux membres binaires, `gamestate` et `meta`. Le prototype a reconnu les 646 contrôleurs et la France. La décompression des deux versions confirme exactement 270 octets modifiés dans `gamestate`, tous de `1` à `0`. Les métadonnées sont identiques et la source conserve son SHA-256. Cette validation du fichier est distincte de sa validation au chargement. Les nouvelles versions et le multijoueur restent hors du périmètre du prototype. [Format des sauvegardes Paradox](https://docs.rs/jomini/latest/jomini/envelope/index.html)

Le script prend le chemin d’une sauvegarde de départ, un nouveau fichier `.v3` et un lot. Il passe par un fichier temporaire dans le dossier cible et publie le résultat seulement si le nom est libre. Les copies complètes et les journaux restent dans le laboratoire Windows.

La protection du pays joué a aussi été testée sur la sauvegarde binaire de Raguse. L’outil l’identifie dans le bloc joueur, écarte son tag du lot E et produit une copie à 377 drapeaux actifs et 269 inactifs.

```text
python tools/performance/ai_phase2_2026_11_25/copy_ai_save.py "source.v3" "copie-E.v3" --cohort E
```

## Recommandation pour `main`

Garder l’IA complète par défaut. Retenir F comme premier candidat à une règle de performance facultative en solo. Il conserve les pays décentralisés et deux acteurs de contenu historique. Il a donné le meilleur chrono de cette phase sur les quatre jalons simulés. E a aussi accéléré les 56 premiers jours dans les deux séries. Le meilleur résultat de F reste un passage unique, associé à la RAM moyenne la plus élevée de la série sur le deuxième écran.

Avant une diffusion, répéter F et un témoin contemporain sur des campagnes neuves hors debug en comptant la durée de la désactivation. Valider un traitement fiable si le joueur dépause tôt, les interactions multiples, le retour au sommeil après conflit et le changement de pays. Le prototype reste une copie de laboratoire. Les cultures, les POP d’origine et le travail de production sont préservés.

Suivi dans [#56](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/56), [#57](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/57) et [#58](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/58).
