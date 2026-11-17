# Issue #54 — comparaison interactive A–B–B–A, 12 novembre 2026

La lenteur de l’arbre est reproduite dans les deux passages de l’interface actuelle. La copie héritant de l’interface vanilla affiche nettement plus de FPS dans les deux passages témoins. **Ce résultat met en cause la surcharge GUI dans son ensemble ; il ne démontre pas que les deux expressions de visibilité en sont, à elles seules, la cause. Aucun correctif n’a été intégré au mod normal.**

## Résultats observés

FPS natifs lus visuellement après les captures stationnaires, valeurs approximatives :

| Branche | A1 : GUI actuelle | B1 : GUI vanilla | B2 : GUI vanilla | A2 : GUI actuelle |
| --- | ---: | ---: | ---: | ---: |
| Production | 8 | 30 | 30 | 8 |
| Militaire | 9 | 42 | 42 | 9 |
| Société | 8 | 27 | 27 | 7 |
| Société après déplacement | 7 | 26 | 26 | 7 |

CPU du processus, pourcentage de la capacité totale des 16 processeurs logiques, pondéré par les intervalles réellement échantillonnés :

| État observé | A1 | B1 | B2 | A2 |
| --- | ---: | ---: | ---: | ---: |
| Carte en pause | 10,36 % | 5,61 % | 5,61 % | 2,89 % |
| Production fixe | 7,00 % | 8,30 % | 8,10 % | 7,11 % |
| Militaire fixe | 7,21 % | 8,42 % | 8,58 % | 7,06 % |
| Société fixe | 7,11 % | 8,23 % | 8,15 % | 6,97 % |
| Société avec un déplacement | 6,83 % | 7,96 % | 7,99 % | 7,04 % |

La charge CPU totale de B est légèrement supérieure malgré ses meilleurs FPS. La charge CPU ne constitue donc pas, isolément, une mesure de fluidité. La variation de la référence carte, le long intervalle de pause avant A2 et l’absence de relevés de fréquence/température limitent les comparaisons fines ; aucun facteur d’accélération exact ou certification statistique n’est annoncé.

Les fichiers CSV et métadonnées sont les relevés CPU primaires. Les captures et `FPS_OBSERVATIONS.json` sont les preuves des lectures FPS ponctuelles. `consolidate_results.py` traite explicitement la virgule décimale du collecteur français et reconstitue le pourcentage CPU à partir du temps CPU et du temps écoulé. Les FPS ne sont ni une moyenne continue ni un percentile. Aucun temps de trame individuel ni délai clic-vers-image précis n’a été obtenu. La durée d’un appel au contrôleur n’est jamais utilisée comme latence du jeu.

## Protocole réellement exécuté

- Quatre processus distincts, ordre A1–B1–B2–A2. La première tentative A2, arrêtée à la demande du mainteneur avant mesure, reste conservée ; seule sa reprise mesurée entre dans le bilan.
- Même exécutable Steam 1.15.1, révision `7a630cdf29e`, SHA-256 `fb4ec0698afd3d3b1a785926d57bd5d68c95a4afd04b56f6bd45abd7a5672b15`.
- Même profil isolé, même sauvegarde France au 1er janvier 1776 en pause, empreinte `e6abb3c2305036855a11db308657164f71cecca29002ac6fdc7822c66fd24791`. La simulation n’a pas avancé.
- Mode fenêtré 1920 × 1080, interface 100 %, rendu DX11, VSync désactivée, limite FPS désactivée, réglages graphiques communs conservés. La capture du contrôleur est exprimée en pixels logiques Windows, ce qui ne change pas la résolution de rendu.
- A conserve la surcharge `gui/tech_tree.gui`. B retire uniquement ce fichier de la même copie figée et hérite du GUI du même exécutable. Les définitions technologiques et tous les autres fichiers sont identiques entre ces deux copies.
- Trois branches préchargées avant mesure. Vingt captures contrôlées de quinze secondes : carte fermée, trois branches stationnaires et un glissement vertical de 140 pixels dans Société pour chaque passage. Le zoom est conservé. Le glissement est un geste unique suivi d’un maintien de la vue ; ce n’est pas une mesure de défilement continu.
- Les changements d’onglet et glissements ont été observés sur les vraies fenêtres du jeu. Le cadrage France est vérifié avant/après chaque passage. Les captures initiales présentant une dérive de caméra ou une mauvaise synchronisation des glissements sont conservées comme calibration et exclues du tableau contrôlé.
- Le réglage « ignorer le curseur » modifie le comportement du zoom ; il **ne désactive pas** le défilement aux bords. Le cadrage contrôlé a été obtenu par rechargement et suppression des actions sur la barre de titre native, puis vérifié en images.
- Aucun nouveau relevé CPU de démarrage. Le collecteur n’échantillonne qu’après demande visant un état d’interface effectivement observé.

## Configuration DLC et portée

La route directe signale un échec d’initialisation Steam. **Les quatre journaux correspondant aux lancements mesurés confirment exactement le même contenu monté : `dlc/dlc001_preorder`, la bande-son remastérisée de Victoria 2 ; aucun DLC de gameplay.** La comparaison porte sur cette configuration effective, pas sur une session authentifiée avec tous les DLC de gameplay. La vérification utilise le journal correspondant à l’heure de chaque lancement : les autres journaux du même dossier sont des rotations historiques, pas des preuves de ce passage. Les listes et le résultat de leur comparaison sont conservés dans `FINAL_VALIDATION.json`.

## Capacités et protections

L’interface Windows autorisée `@oai/sky` a servi aux captures, clics et glissements. Les raccourcis clavier du jeu restent peu fiables ; le protocole utilise la souris. Une autorisation de l’outil de commandes a permis de lancer le processus d’essai et de lire les compteurs de cet enfant uniquement. Aucun réglage de sécurité, droit Windows, authentification, installation de contrôleur alternatif ou contournement du Gestionnaire des tâches n’a été effectué.

Les processus d’essai ont été arrêtés après leurs captures. Un code de sortie -1 correspond à l’arrêt borné du processus possédé par le lanceur après sa demande de fermeture ; il ne constitue pas la preuve d’un crash pendant une mesure. Les tentatives et journaux antérieurs sont conservés. Les profils de laboratoire sont conservés pour permettre une reprise diagnostique identique ; aucun ancien profil normal n’est restauré par-dessus les données courantes.

**44/44 contrôles réussis**, dont l’intégrité des copies A/B/C, les 1168 comparaisons booléennes, les vingt captures réellement obtenues, la synchronisation des quatre glissements, le même exécutable, la même sauvegarde et les mêmes DLC effectivement montés. Les 3781 entrées de la référence de conservation ne présentent aucun changement du produit normal ou de l’index Git ; les deux différences de fichiers d’état du lanceur/réglages déjà documentées restent distinctes du code du mod.

Les vérifications de conservation sont dans `FINAL_VALIDATION.json` et `NORMAL_PLAYSETS_FINAL.json`. Le second contrôle confirme en lecture seule la conservation des sept playsets normaux, de leurs onze liens de mods et de leurs cinquante et un liens DLC ; seul le champ de synchronisation `lastSyncAttemptAt` diffère dans cette comparaison historique. Aucun Git d’écriture ni modification du vanilla n’appartient à cette passe. Ces contrôles techniques ne constituent pas une validation humaine d’un correctif de performance.

## Expressions de visibilité : copie C

La copie diagnostique `C_simplified_gui` est séparée et non intégrée. Elle ne change que deux expressions du GUI. Les définitions technologiques restent inchangées :

| Expression | Caractères avant → après | Occurrences textuelles de GetTechnology | Profondeur avant → après |
| --- | ---: | ---: | ---: |
| Lignes de dépendance | 3713 → 3521 | 42 → 40 | 44 → 9 |
| Cartes de technologie | 3158 → 3078 | 43 → 42 | 45 → 11 |

Le modèle statique compare 584 cas par expression, soit 1168 cas : 291 identités technologiques, une identité inconnue et les deux valeurs de ShouldShow. Le maintien des alias masqués et des exceptions force-show est contrôlé dans ce modèle. L’équivalence suppose des identités valides et distinctes ; elle ne démontre ni les liaisons du moteur, ni le coût réel d’évaluation ou l’ordre de court-circuit. **C n’a pas été lancé au moteur. Aucun gain de C n’est revendiqué.**

## Prochaine action

Comparer séparément A à C sur la sauvegarde et les réglages conservés, avec répétition et inspection des technologies masquées/forcées. Si C conserve la lenteur, réduire progressivement les autres différences du GUI pour isoler le coût. Ne pas intégrer B comme correctif : il supprime aussi les filtres de compatibilité et change l’interface. La mission reste ouverte jusqu’à un correctif minimal vérifié, puis sa validation humaine et son autorisation d’intégration.

Le présent bilan remplace pour l’état courant les notices historiques de relais manuel et de pause ; leurs fichiers sont conservés sans réécriture des faits antérieurs.
