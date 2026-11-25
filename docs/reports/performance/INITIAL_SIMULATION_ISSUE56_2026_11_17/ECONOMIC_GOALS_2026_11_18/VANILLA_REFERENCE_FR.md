# Référence vanilla — 18–19 novembre 2026

La paire du 18 novembre a été réellement exécutée avec la même installation Steam 1.15.1, sans le mod, et les mêmes observateurs que les essais économiques. Elle ne constitue pas un témoin équivalent du monde de 1776.

## Source et méthode

Source native France, 1er janvier 1836 : `aor1776_simperf56_20261117/profiles/VANILLA1/save games/france_1836_01_01.v3`, dans le dossier temporaire Windows. SHA-256 `3b9a4448bd1a31e95e1bb55b7a34eef59d29834f4eaf6038a78d3580904d794f`, 76 905 580 octets. Les deux copies initiales diffèrent uniquement par les flags des 449 contrôleurs ; la vitesse commune vaut 4 dans le fichier, soit 5 dans l'interface.

Source : 449 contrôleurs (158 décentralisés, 291 autres), 1 021 666 228 personnes, 27 252 objets POP, 1 156 États, 6 487 objets bâtiment et 96 182 niveaux, 1 478 bâtiments à profit négatif, 305 marchés, 388 formations. Ces inventaires décrivent l'état sérialisé et ne mesurent pas une charge CPU. Monde, date, technologies, pays, population, économie et vue diffèrent du scénario 1776.

Les réglages trimestriels portent l'empreinte `718eb8e11996500326bb3753c59f66b8513983bb8fc86e19eb2b782b8caafeaa`. Le témoin initial est la source préparée vérifiée, **pas une PRE native manuelle**. La sauvegarde automatique native du 1er avril vérifie l'état final. Aucun autosave observé dans la fenêtre 2 janvier–27 février ; le jeu continue ensuite pour sauvegarder et vider ses journaux. Les copies et leur calcul d'empreinte sont postérieurs au benchmark.

## Paire terminée, ordre ON puis OFF

| Essai | 14 jours | 28 jours | 56 jours | CPU moyen sur 56 j, % des 16 processeurs logiques | Contrôleurs dans l'autosave native du 1er avril |
|---|---:|---:|---:|---:|---|
| VAN_ONQ1 | 13 s | 23 s | 45 s | 26,96 % | 450 actifs |
| VAN_OFFQ1 | 10 s | 18 s | 34 s | 21,25 % | 449 inactifs |

Les 449 contrôleurs initiaux sont tous retrouvés dans les deux POST. Le 450e du passage normal correspond à un nouveau pays NIC reconnu, identifiant 16777948 ; il est actif comme tous les contrôleurs présents. Il ne faut pas rejeter cette évolution naturelle en exigeant artificiellement un nombre final constant. Le premier reçu trop strict reste conservé ; la révision `VAN_ONQ1_POST_AI_PROOF_POPULATION_REVIEW.json` garde l'exigence sur chaque flag et explicite la naissance de NIC. Aucune exigence de flag n'a été supprimée.

POST ON : SHA-256 `49623b2119173359b0ee77d72c593032b9670130351867a5eea37e9b558b046c`, 91 187 943 octets. POST OFF : `6ea94d90ae2b29d48f5195e338e22a05945e0142bf6201b48241530771ed45cf`, 87 050 604 octets. Preuves dans `aor56_ai_20261117/autosave_witnesses` et `*_RESULTS.json`.

Sur cette seule paire, OFF demande 24,4 % de temps en moins ; le débit augmente de 32,4 %. C'est un signal exploratoire vanilla, inférieur au contraste des anciens essais 1776, mais **pas une estimation causale de la pénalité du mod**. Les séries n'ont pas les mêmes mondes, dates, vues ni réglages d'affichage contemporains. Il faut comparer chaque variante à son propre témoin.

## Tentatives et répétitions

VAN_ON2 : préparation abandonnée après une avance de date inattendue ; aucun benchmark accepté. VAN_ON3 : journaux partiels et absence de POST, seulement 55 DAY complets disponibles ; aucun temps sur 56 jours accepté. L'utilisateur a précisé que le jeu avait redémarré et qu'il n'avait pas fait la sauvegarde demandée. Cette correction prévaut sur l'ancienne réponse ambiguë ; aucun fichier final n'est inventé. VAN_OFF2 et VAN_OFF3 n'ont pas été exécutés.

VAN_OFFQ2 et VAN_ONQ2 ont été préparés mais pas lancés avant le changement d'écran demandé le 19 novembre. Une nouvelle paire `VAN_OFFG1 → VAN_ONG1` a été préparée en 1600×900 fenêtré sur l'écran secondaire GAOMON, avec les mêmes réglages entre les deux conditions. Sa préparation ne vaut pas résultat ; son état final doit être lu dans le rapport principal et le CSV. Les deux paires d'affichage restent des groupes distincts.

La fermeture automatique du seul processus possédé après la sauvegarde et le nombre de DAY prévu peut produire EXIT −1. Ce code d'arrêt contrôlé ne doit pas être présenté comme un crash.

## Nouvelle paire C, ordre OFF puis ON, exécutée le 19 novembre

Les deux profils utilisent les réglages communs `9a759fceadc82095774b75030159250f67b51b488d192d0239f96f42a27e26c4`, les contrôles stabilisés et le seul écran secondaire. Le contrôle natif retrouve exactement les mêmes 6 302 chemins virtuels et contenus chargés entre les deux conditions, sans ajout ni retrait ; exécutable, réglages et liste des mods identiques.

| Essai | 14 j | 28 j | 56 j | CPU moyen sur 56 j | POST natif du 1er avril |
|---|---:|---:|---:|---:|---|
| VAN_OFFC1 | 6 s | 20 s | 50 s | 23,91 % de la machine | 449 inactifs |
| VAN_ONC1 | 7 s | 13 s | 26 s | 23,78 % de la machine | 450 actifs |

Les contrôleurs initiaux sont tous présents ; le contrôleur supplémentaire du passage ON est enregistré séparément dans sa preuve native. Aucun POST n'est supposé artificiellement garder un nombre de pays constant.

**Cette paire contredit le sens de l'ancienne paire Q1. Aucun effet causal vanilla reproductible n'est établi.** Les fenêtres sont réellement mesurées, mais l'absence d'action enregistrée après le départ ne certifie pas une présence continue au premier plan ni l'absence d'intervention physique ou de pause automatique. La préparation en pause depuis « Continuer » diffère également : environ 77 secondes pour OFF et 184 secondes pour ON, après les difficultés de capture. Cela peut affecter la comparabilité ; ce n'est pas une explication prouvée de l'inversion.

Le premier envoi de la touche Espace par Sky à 02:04:50.346 UTC n'a pas démarré VAN_ONC1 : une capture CUA fraîche montre encore le 1er janvier en pause. Le clic CUA confirmé de 02:06:08.539 UTC fait ensuite avancer la date au 12 janvier. Le journal original conserve les deux tentatives ; `VAN_ONC1_START_RECONCILIATION.json` identifie celle réellement retenue. L'heure exacte de la capture source n'ayant pas été mesurée, le reçu corrigé la marque inconnue ; l'ancienne valeur non mesurée est conservée séparément et retirée comme preuve temporelle. Les durées viennent des DAY natifs, pas de cette heure de capture.

## Répétition inversée R, exécutée et vérifiée

| Ordre réel | Essai | 14 j | 28 j | 56 j | CPU moyen sur 56 j | POST natif |
|---|---|---:|---:|---:|---:|---|
| 1 | VAN_ONR1 | 7 s | 14 s | 28 s | 23,92 % | 450 actifs, tous les initiaux présents |
| 2 | VAN_OFFR1 | 14 s | 29 s | 42 s | 24,66 % | 449 inactifs, tous les initiaux présents |

Les ressources natives sont à nouveau strictement identiques entre conditions : 6 302 chemins virtuels, aucun changement, ajout ou retrait ; exécutable, réglages et liste des mods identiques. La déclaration DLC native et le fichier `dlc_signature` sont identiques dans les dix nouvelles sessions contrôlées/profilées examinées. Aucun DLC de gameplay n'est apparu.

Préparations réelles depuis « Continuer » : **220,393 secondes pour ON et 223,677 pour OFF**. La source reste au 1er janvier en pause et la vue Europe occidentale sans panneau d'État est vérifiée avant chaque départ. La récupération d'image dans ON a nécessité des commandes de fenêtre et la fermeture d'un panneau ; OFF a attendu pour rapprocher les durées. Elles ne sont pas identiques à la seconde près. Les départs confirmés sont à 02:26:21.069 et 02:34:13.571 UTC. Aucun nouvel envoi d'entrée n'est enregistré après ces départs. L'image immédiatement après ON manque, mais les DAY natifs confirment l'avancement ; OFF est aussi observé au 10 janvier. Aucune absence continue de pause physique, de changement de premier plan ou de charge extérieure n'est certifiée.

**Le nouveau lot répète un passage OFF plus lent**, 42 contre 28 secondes ; l'ancien lot Q1 donnait OFF plus rapide, 34 contre 45. Les ON récents sont proches (26/28), les OFF restent variables (50/42, dont 6/14 secondes sur les premiers 14 jours). La résolution d'horodatage ne suffit pas à expliquer ces écarts. Les causes possibles — contexte d'exécution, préparation, évolution différente de l'économie sans contrôleurs, travail différé — ne sont pas départagées. On ne peut attribuer cette contradiction à un mécanisme précis ni annoncer un coût vanilla stable de l'IA.

Les preuves de traitement restent valides, avec leurs limites temporelles explicites. Le contraste n'est pas une pénalité causale du mod : ni ses pays ni son économie ne sont remplacés par ceux de 1836. Aucun chiffre des trois paires n'est agrégé pour obtenir une « moyenne vanilla » de référence.
