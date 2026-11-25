# Inspection économique et limites des ablations

## Travail exécuté

EXB1 et EXB3 vérifient dans des sauvegardes natives que 400 objectifs `expand_production_buildings`, absents au départ, sont recréés en jeu. EXB3 les retrouve dès le 4 janvier 1776 à 18 heures moteur. Les 646 contrôleurs restent actifs, les autres objectifs sont préservés. Ce résultat invalide le retrait sérialisé comme méthode de désactivation persistante ; il ne mesure ni la fréquence ni le coût CPU de l'extension.

Les inventaires de stratégies, profits, objets POP, bâtiments/niveaux, formations et investissement ont été extraits ou réutilisés sans toucher aux sauvegardes de référence. Ils sont conservés dans le laboratoire externe : `ECONOMIC_WORLD_INDICATORS_20261118.json`, `AI_STRATEGY_AND_GOAL_SNAPSHOTS_20261118.json`, `AI_STRATEGY_STABILITY_DESCRIPTIVE_20261118.json`, `BUILDING_RECORD_LEVEL_COMPARISON.json` et `MODDED_AI_SCORE_CALLBACK_INVENTORY_20261118.json`.

Les stratégies sérialisées des 646 pays ne changent pas entre S0 et le POST normal de mars examiné. Le monde mature change 16 stratégies parmi 645 contrôleurs communs, sans changement parmi les huit noms administratifs sélectionnés. Cela ne prouve pas que le moteur ne réévalue pas les mêmes stratégies. Les dates et branches des snapshots diffèrent : aucune corrélation n'est présentée comme une attribution de coût.

Les profits négatifs et objets POP diminuent aussi lorsque tous les flags IA sont désactivés. Le compteur d'investissements autonomes échoués continue à augmenter dans ces mondes rapides. Une décision privée n'est donc pas automatiquement suspendue par le flag du contrôleur national. Il faut vérifier l'activité réelle de chaque mécanisme au lieu de traiter « IA désactivée » comme l'arrêt de toute l'économie.

## Préparation sans résultat d'exécution

PM1 retire les seuls 400 blocs sérialisés `change_production_methods`, avec les autres objectifs conservés. Ce profil n'a pas été lancé. Étant donné la recréation de l'extension, sa persistance ne doit pas être supposée et aucune fonction PM n'est innocentée.

Un panneau de diagnostic natif a été préparé pour afficher les objectifs, les valeurs de stratégies, des scores de construction publique et autonome, et un score de PM dans un État choisi. Les commandes existent dans l'exécutable, mais ces boutons n'ont pas été exécutés. Leur présence dans un fichier GUI ne constitue ni une trace native ni une mesure.

## Expérience de remplacement effectivement chargée

La variante externe `building_priority_bases_20261118` remplace seulement douze blocs moddés `ai_value` par leurs constantes de base, dans neuf fichiers. Les autres octets sont conservés ; tous les contrôleurs, objectifs, PM, pays, POP, bâtiments, marchés et routines HRE/régionales restent présents. Elle peut changer les préférences de construction : c'est une ablation diagnostique, pas une optimisation équivalente.

Le contrôle natif de chargement SCORQ1 constate exactement ces neuf fichiers modifiés parmi 7 411 chemins virtuels, sans ajout ni suppression. Ce premier contrôle utilise un ancien témoin seulement pour vérifier les ressources chargées et ne vaut pas comparaison de performance. SCORQ1 donne 52/101/174 secondes, avec 646 flags actifs et tous les objectifs attendus dans l'autosave native d'avril ; son témoin ECNQ1 n'a pas simulé. Ce chiffre reste donc sans témoin contemporain exploitable.

La reprise du 19 novembre prépare une nouvelle série A–B–B–A sur le seul écran secondaire : ECNG1, SCORG1, SCORG2, ECNG2. Pour chaque paire retenue, une vérification native stricte doit confirmer les neuf surcharges, le même exécutable et les mêmes réglages, en plus de la source vérifiée, des DAY consécutifs et du POST natif. Lire le rapport principal et le CSV pour les passages effectivement terminés.

## Profilage

La tentative GUI Jomini dans EXB1 a commencé après le benchmark. Elle a affiché 456 ticks et une durée croissante, mais aucune table exploitable avant la fermeture ; « Stop capture » n'a pas été actionné. Les anciens résultats Legacy et TickTask sont partiels, sans pile native complète ni temps exclusifs sûrs. Les noms de threads absents empêchent leur attribution à une fonction moteur.

La tentative Windows antérieure s'est heurtée à la restriction 0xc5585011. Aucun réglage de sécurité n'a été contourné. Les avertissements de script observés dans les fenêtres communes sont peu nombreux et n'établissent pas une boucle d'échec coûteuse ; l'absence de traces ne suffirait pas non plus à exclure des répétitions silencieuses.

Si les callbacks testés n'expliquent pas un surcoût reproductible, la prochaine investigation doit cibler un contrôle natif persistant d'une seule catégorie, vérifier son activité effective, et distinguer les décisions publiques de l'investissement privé. À défaut de commande adaptée ou de profilage moteur exploitable, cette limitation doit être rapportée ; un retrait de pays, une baisse de fréquence IA ou une suppression de contenu ne remplace pas ce contrôle.

## Comparaison exacte à date appariée, ajout du 19 novembre

Les autosaves natives d'ECNG1 (scores normaux) et SCORG1 (douze scores remplacés par leur base) sont toutes deux du 1er avril 1776 et proviennent de la même source. Leur comparaison par sections sérialisées trouve **83 sections strictement identiques ; seul `local_date_time` diffère**, sans section ajoutée ou retirée. Le reçu est `ECNG1_SCORG1_MATCHED_POST_SECTIONS.json` dans le laboratoire. Les sauvegardes ne sont pas modifiées.

La différence de panneau observée invalide l'attribution causale de leur écart de performance, mais n'empêche pas cette comparaison descriptive des POST à même date. L'égalité des sections d'IA, d'économie et des autres données sérialisées est une observation plus forte que l'égalité de simples totaux. Elle ne prouve ni l'identité de toutes les décisions intermédiaires, ni l'exécution ou la fréquence de chaque callback, ni l'équivalence dans d'autres campagnes ou à des dates ultérieures.

Cela rend particulièrement utile un profil de **nombre d'appels et temps des callbacks réellement exécutés** : définitions chargées, valeurs effectivement différentes et fonction appelée sont trois vérifications distinctes. Le remplacement de toutes les priorités ne doit pas être intégré sur la seule base d'une trajectoire POST identique.

## Résultats ultérieurs effectivement acquis

La série stabilisée SCORC1–ECNC1–ECNC2–SCORC2 est terminée : 100/96/94/102 secondes sur 56 jours, dans cet ordre. Les deux paires de POST natifs du 1er avril ont également 83 sections égales et seulement `local_date_time` différent. Les vérifications de chargement native confirment les neuf fichiers attendus parmi 7 412, et les quatre POST conservent les 646 flags actifs et objectifs. Aucun gain n'est observé ; lire [SCORE_CALLBACK_RESULTS_FR.md](SCORE_CALLBACK_RESULTS_FR.md) pour les limites.

Le profilage distinct PROFC1 est maintenant terminé et exporté. Il compte 5 003 entrées ; huit des douze emplacements de priorité ciblés sont réellement observés avec nombres d'appels et temps déclarés en secondes. La preuve et les limites figurent dans [SCRIPT_PROFILE_FR.md](SCRIPT_PROFILE_FR.md). Il ne s'agit pas d'un benchmark ni d'une pile CPU native complète. Les commandes individuelles d'évaluation PM/construction préparées plus haut restent non exécutées : cet export ne leur invente pas de sortie.
