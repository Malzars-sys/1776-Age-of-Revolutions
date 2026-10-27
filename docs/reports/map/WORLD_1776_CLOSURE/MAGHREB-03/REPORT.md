# MAGHREB-03 — Quatre résolutions territoriales installées

26 octobre 2026. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Référence historique : 1er janvier 1776. Aucun moteur lancé ni reçu humain créé. La dernière décision du joueur conserve Siwa à l'Égypte et impose une continuité avec les territoires centralisés ; cette règle de mission n'est ajoutée ni à AGENTS.md ni aux guides `.agents/`.

## Corrections installées

| Point | Résolution |
| --- | --- |
| Fezzan | FZN reçoit neuf provinces existantes autour de Murzuq, Sabha et Sokna, avec une jonction terrestre à Tripoli. Le lien tributaire natif avec TRI est déclaré. Aucun désert entier annexé. |
| Siwa | **Reste égyptienne conformément au choix explicite du joueur.** Le passage existant vers la Basse-Égypte est praticable et conservé ; aucun SIW créé, aucun découpage autonome installé. Cette approximation de gameplay remplace la proposition historique de l'audit. |
| Maroc–Tekna | Les neuf RGB litigieux restent à TEK ; leurs occurrences dans la liste MOR sont retirées. Le contour local déjà déclaré est conservé, sans prétendre trancher l'allégeance générale au sultan. |
| Tripoli | xAFD438 et xD5C61D restent à TRI ; les quatre occurrences ZWY sont retirées. Les deux provinces touchent le territoire tripolitain, sans enclave centralisée nouvelle. |

Fezzan, STATE_LIBYAN_DESERT : **xCA4E6B, x009F47, xE6917C, xC724C8, x3B68A8, x92D93F, x7DEA64**. Jonction dans STATE_TRIPOLI : **x522D29, xCD6775**, contiguë à xFAB002 restée TRI. Les ancrages natifs échantillonnés sont Murzuq `(4409,1513)`, Sabha `(4423,1484)` et Sokna `(4441,1426)`. Ce sont des indices géographiques, pas des relevés cadastraux. Le noyau est une représentation limitée des oasis et de leur axe d'accès, pas la totalité des dépendances historiques du sultanat.

Maroc–Tekna : **x0FA44F, x4DE76B, x53C5EF, x88C527, x8ACEDE, x8DCD09, x9E582E, xE80E2E, xF414B2**. Les autres provinces marocaines et tekna restent identiques. Tripoli : les deux provinces résolues couvrent 153 et 298 pixels existants ; aucun pixel n'est recolorié. Les onze conflits sont retirés uniquement dans les régions autorisées. Des doublons préexistants ailleurs dans le monde sont conservés et consignés, sans lancer de correction américaine.

Siwa, xE0D021 : route vérifiée **xE0D021 → x252184 → x05FF42 → xC1822C → x246457 → x20CF20 → xF47AAA**. Chaque passage partage un bord terrestre ; les provinces infranchissables sont exclues. Tous les propriétaires égyptiens restent inchangés. CORRIDORS.json contient aussi l'axe Fezzan–Tripoli ; aucune traversée d'un pays décentralisé n'est nécessaire le long de ces chemins.

## Populations et données de départ nécessaires

**837 328 539 → 837 328 539**, delta mondial nul. **11 067 habitants** sont redistribués de ZWY vers FZN : 5 959 dans le désert libyen et 5 108 dans la portion de Tripoli. Chaque cohorte conserve son total, sa culture, sa religion et son statut. L'allocation est une répartition technique des pools existants (7/53 et 2/53 provinces natives), pas une nouvelle estimation historique, une densité par pixel ou un recensement des oasis. Les pools ZWY restants sont conservés. La démographie précise du sultanat demeure une limite explicite.

Le TAG FZN, sa définition et ses six technologies existaient déjà. Son profil est conservé, sans grant d'assurance commerciale, refonte du graphe ou retouche des recettes. La vérification a découvert que l'effet politique générique demandait un mercantilisme désormais verrouillé par cette assurance. Une copie de cet effet réservée à FZN substitue **Péages caravaniers**, avec les mêmes six valeurs commerciales natives et le prérequis `international_relations` déjà acquis. Aucun autre pays ou loi commune modifié. C'est une compatibilité d'activation du pays ; aucune chaîne économique ou amélioration de bâtiments ajoutée.

Les deux chefs FZN de la référence 1836 ne sont pas préinstallés en 1776 : une surcharge vide de leur fichier évite leur apparition. Aucun personnage historique inventé ou général ajouté. La génération ordinaire du dirigeant et les effets réels du statut tributaire restent à observer en moteur. Aucun bâtiment, PM ou unité supplémentaire scripté ; les capacités de subsistance relèvent de l'initialisation native.

## Sources, approximations et conservation

SOURCES.md distingue les textes réellement lus des cartes non calées. Hornemann (voyage de 1798, chapitre III et appendice de Rennell) énumère Murzuq, Sabha et Sokna et décrit le rapport tributaire ; la continuité dynastique au XVIIIe siècle est corroborée par la notice TDV. L'axe choisi utilise les provinces existantes et la consigne de continuité du joueur : il n'est pas présenté comme une frontière mesurée de 1776. La résolution des deux RGB de l'arrière-pays tripolitain conserve leur attribution TRI et l'abstraction de la juridiction nominale ; le contrôle tribal village par village n'est pas certifié.

Pour le Noun/Draa, l'autonomie locale est distinguée de l'allégeance. L'avis de 1975, lu comme recueil critique de pièces anciennes, ne vaut pas un jugement cadastral sur 1776 ; la controverse sur le traité de 1767 est conservée. Le patch supprime une double attribution technique dans le noyau TEK préexistant, sans réécrire les revendications historiques. La chronologie discutée de Kufra reste hors correction.

**Zéro nouveau RGB, zéro pixel peint, zéro modification de terrain, ressources ou hubs.** Trois fichiers partagés retouchés dans leurs blocs courants (États, POPs nord-africaines, historique FZN), six fichiers propres ajoutés. Ceuta, Melilla, Oran, Gibraltar, les Balkans et les interfaces SERG sont conservés. Le travail parallèle COLONIES-01 a changé le seul bloc du Nouveau-Brunswick dans le fichier d'États, plus cinq fichiers américains ; copies et empreintes sont archivées dans EXTERNAL_REVIEW.json. Les trois blocs maghrébins sont identiques à notre patch ; aucun retour à une ancienne baseline, Git d'écriture, modification vanilla ou suivi SERG.

## Vérifications et suite

**50/50 contrôles statiques**, puis **PASS_STATIC_ONLY pour FZN**, six technologies connues et aucun constat restant dans le contrat initial. Les traces initiales sont conservées : assertion trop large sur les doublons mondiaux, évolution concurrente américaine et demande de loi héritée identifiées séparément, sans les présenter comme des pannes moteur. TEST_MATRIX.md précise les commandes et les limites.

Les quatre entrées de l'audit reçoivent leur résolution dans RESOLUTIONS.json ; les preuves de MAGHREB-02 restent immuables. Les tests joueur Maghreb–Égypte restent **groupés et NOT_RUN**, protocole GROUPED_RUNTIME_ITEMS.md. Aucun critère régional supplémentaire ni reçu humain créé : WORLD reste à **10/320**, zéro validation joueur. Prochaine passe territoriale proposée : Afrique subsaharienne, conformément à la transition conditionnelle déjà autorisée ; aucune nouvelle correction territoriale certaine supplémentaire n'est établie par ce lot. Les limites historiques et de résolution documentées subsistent.
