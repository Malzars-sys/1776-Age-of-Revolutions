# Comparaisons C — contrôles stabilisés sur écran secondaire

Cette série distincte répond aux défauts observés dans les préparations précédentes : défilement involontaire de la carte pendant la pause, captures Windows parfois bloquées et boutons du laboratoire superposés au menu. Les résultats G/Q restent conservés dans leurs groupes ; aucun gain transversal n'est calculé.

Tous les C utilisent le même exécutable Steam, les mêmes sources, préférences trimestrielles et observateurs natifs. La fenêtre 1600×900 reste sur le second écran GAOMON. Le profil normal et la résolution du bureau sont préservés. La préférence native `System.screen_edge_scroll_mode=screen_edge_scroll_mode_disabled`, sélectionnée et vérifiée en jeu, stabilise la carte lorsque le pointeur quitte la fenêtre. L'empreinte initiale des réglages C est `9a759fceadc82095774b75030159250f67b51b488d192d0239f96f42a27e26c4`.

Le même mince pack d'interface est chargé dans les deux conditions : position des six boutons de laboratoire corrigée dans une copie du menu, et animation de 16 pixels déclarée visible seulement en pause. Les derniers passages ont pu être pilotés avec des captures répétées de la pause, sans intervention humaine. Cela ne prouve pas la cause interne des anciennes erreurs de capture. L'ancien overlay commun reste intact à son empreinte de référence.

La **seule différence entre contrôle et diagnostic** est le pack de douze blocs `ai_value` remplacés par leurs bases, identique au diagnostic précédent. Les neuf surcharges de bâtiments doivent être vérifiées par les empreintes natives du moteur entre deux C terminés. Les autres ressources virtuelles doivent être identiques.

Ordre prévu : **SCORC1 → ECNC1 → ECNC2 → SCORC2**, puis référence vanilla **VAN_OFFC1 → VAN_ONC1**. L'exécution réelle et les exceptions figurent dans le rapport final et le CSV, pas dans le seul ordre prévu.

Avant chaque départ : date initiale et vitesse 5 vérifiées à l'écran, carte d'Europe occidentale sans panneau d'État supplémentaire pour le mod, source intacte et caméra stable. La préparation en pause dure plus d'une minute ; sa durée réelle depuis le clic Continuer est enregistrée dans chaque `*_SOURCE_UI.json`. Elle n'est pas présentée comme rigoureusement identique à la seconde près. Les préparations où la date a avancé avant le départ sont rejetées.

Après le clic de départ : aucune nouvelle entrée de l'agent ; observations seules. Les fenêtres DAY cumulées de 14/28/56 jours utilisent les horodatages natifs du 2 janvier au 27 février. Le jeu continue jusqu'à l'autosave native d'avril et suffisamment de DAY pour vider les tampons, puis le lanceur ferme uniquement son propre processus. Les travaux de sauvegarde et de copie restent après les fenêtres.

La source préparée est la preuve initiale ; aucun reçu n'invente une PRE native manuelle. Le POST natif vérifie tous les flags présents et les objectifs des contrôleurs communs. Les changements naturels de population de contrôleurs restent explicités. Comparaison de sections au même 1er avril possible ensuite, en lecture seule et après les benchmarks.

Les contrôles C servent à tester la reproductibilité ; de petits écarts, des écarts dépendant de l'ordre ou des différences de vue ne justifient pas une optimisation. Les préférences de construction peuvent changer dans ce diagnostic. Même un POST identique sur cette trajectoire ne prouve pas l'équivalence pour d'autres campagnes et dates.
