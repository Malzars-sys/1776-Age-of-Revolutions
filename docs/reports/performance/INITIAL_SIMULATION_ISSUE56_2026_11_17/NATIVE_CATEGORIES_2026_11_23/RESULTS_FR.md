# Comparaison des interrupteurs économiques sous Victoria 3 1.15.2

Cette série reprend le diagnostic de l’issue #56 à partir de la même sauvegarde de la France du 1er janvier 1776. Les essais tournent sur le deuxième écran, à vitesse 5. Ils lisent les secondes inscrites par le moteur pour des fenêtres imbriquées de 14, 28 et 56 jours qui commencent le 2 janvier. L’autosauvegarde du 1er avril permet de contrôler les files de construction et l’état des contrôleurs après la simulation. Les mesures incluent les effets sur le monde et le rendu de l’interface. Elles ne donnent pas le temps CPU exclusif d’une fonction.

Le lot utilise le même mod figé, les mêmes réglages et le même démarrage automatique. Deux fichiers d’interface proviennent de l’installation Steam 1.15.2 pour supprimer les appels navals incompatibles qui remplissaient les journaux. Les captures du 1er janvier lisent les valeurs effectives des trois interrupteurs avec `GetDefine`. Les variantes diffèrent du témoin par une seule valeur. [Reprise et qualité des prises](RECOVERY_FR.md)

| Condition | 14 j | 28 j | 56 j | File publique au 1er avril | File privée au 1er avril |
| --- | ---: | ---: | ---: | ---: | ---: |
| Témoin normal (`NAC2`) | 36 s | 68 s | 121 s | 1 220 | 22 |
| Construction publique de production désactivée (`NAU1`) | 57 s | 111 s | 195 s | 877 | 23 |
| Construction privée désactivée (`NAV1`) | 34 s | 66 s | 119 s | 1 209 | 0 |
| Décisions de dépenses publiques désactivées (`NAM1`) | 34 s | 66 s | 117 s | 344 | 11 |

La construction publique de production disparaît de la file d’avril quand son interrupteur est coupé. Les ordres restants portent sur des secteurs de construction, des casernes, des administrations gouvernementales ou navales et des universités. Les ordres privés restent présents. Les 400 objectifs sérialisés `expand_production_buildings` sont conservés dans la variante et le témoin. Le moteur continue donc d’enregistrer les objectifs alors que l’interrupteur empêche les mises en chantier correspondantes.

La construction privée désactivée vide la file privée, contre 22 ordres dans le témoin. Les deux secondes d’écart sur 56 jours restent trop faibles pour établir un gain avec une prise par condition et une horloge à la seconde. Le chiffre de 195 secondes pour la construction publique est un résultat de la prise, pas une estimation du surcoût intrinsèque de la désactivation.

Lorsque les décisions de dépenses publiques sont désactivées, la file publique d’avril passe de 1 220 à 344 ordres. Elle ne contient plus de secteurs de construction, de casernes, d’administrations ni d’universités. Les exploitations et usines ainsi que les ports et chemins de fer restent présents. Quatre secondes de moins sur 56 jours demanderaient une répétition avant d’attribuer un gain à l’interrupteur.

Les quatre autosauvegardes d’avril conservent les mêmes 646 contrôleurs actifs et les 400 objectifs de dépenses et d’expansion. Aucune des trois désactivations ne reproduit l’accélération nette observée lors de l’arrêt global des contrôleurs en 1.15.1. Les fichiers des anciennes mesures restent distincts. Ces essais montrent quels ordres restent en file à une date donnée. Pour savoir si le moteur continue de calculer la rentabilité ou d’évaluer des candidats avant d’appliquer l’interrupteur, il faudrait observer les appels natifs. La sélection des méthodes de production reste également ouverte. Aucun correctif de performance préservant le gameplay n’a été validé lors de cette série.

Les fichiers détaillés `NAU1_RESULTS.json`, `NAC2_RESULTS.json`, `NAV1_RESULTS.json` et `NAM1_RESULTS.json` dans le laboratoire contiennent les horodatages, les valeurs CPU, la liste des types d’ordres, les différences de contrôleurs et les empreintes des autosauvegardes. Le témoin interrompu `NAC1` reste dans l’historique du lot. Les quatre essais de la comparaison se sont fermés automatiquement après les fenêtres et l’autosauvegarde.
