# MAP-2M-R7 — Arbitrage prêt à soumettre au joueur

Date cible : **1er janvier 1776**. Statut de livraison : **MAP-2M-R7_READY_FOR_PLAYER_DECISION**. **MAP-2M n'est pas historiquement clos. Aucun transfert installé.**

## Les deux décisions

| Secteur | Proposition / conclusion | Effet réellement installé |
| --- | --- | --- |
| Peene, variante A conservatrice | 3 pixels PRU→SWE proposés, environ 30,6 km² | Aucun |
| Peene, variante B de généralisation | 41 pixels PRU→SWE proposés, environ 417,9 km², incluant les 3 de A | Aucun |
| Bromberg méridional | Pas de segment supplémentaire démontré ; 18 candidates locales restent C | Aucun |

**Attention : les noms des variantes A et B ne sont pas les catégories de preuve. Les deux variantes de la Peene sont des décisions de catégorie B, soumises à approbation. Il n'y a aucune nouvelle correction démontrée de catégorie A.**

## Peene : une décision cartographique concrète

Les variantes ne résultent pas d'un nouveau recalage. Elles traduisent la souveraineté du continent suédois figurée sur Mayer/Lotter 1763 en une proposition de dessin sur la grille actuelle, à l'ouest du Peenestrom. La géométrie exacte de chaque berge de 1776 n'est pas revendiquée.

Les sections occidentales de l'eau moderne LUNG sont projetées par les quatre modèles R5 figés. Cette enveloppe sert **d'aide au dessin**, pas de preuve historique. Dans les deux variantes, le bord droit de chaque nouvelle cellule reste à l'ouest de tous ces tracés. Les composantes proposées doivent toucher la Suède existante par un côté. Aucun territoire n'est ajouté à partir du seul point d'une ville ou d'un moulin.

- **A** ajoute seulement (4405,736), (4405,737), (4405,738), dans une couche directement adjacente à la Suède actuelle et en retrait du chenal. Elle réduit le risque et laisse une grande partie du problème ouverte.
- **B** représente davantage de l'arrière-pays continental et des approches occidentales de Wolgast. Elle reste bornée à X 4404–4411, Y 732–739, sans reprendre automatiquement les 149 candidates supplémentaires de R5. C'est un choix régional d'environ 418 km² de grille, **pas la restitution d'une petite enclave urbaine**.

Les deux variantes excluent toutes les nouvelles cellules à Y≥740 : les abords immédiats d'Anklam et Peendamm restent en attente, sans enclave artificiellement agrandie. Demmin est hors de la fenêtre. Les ensembles insulaires d'Usedom et de Wollin ne sont pas proposés à la Suède ; la généralisation reste du côté continental de tous les chenaux projetés employés.

**Limite importante :** le point urbain provisoire de Wolgast conservé de R5 tombe dans (4410,735), cellule qui n'est transférée par aucune variante. Ce point n'est pas un contrôle natif validé. B améliore donc le territoire continental, mais ne garantit pas à elle seule l'emplacement/affichage exact du centre de Wolgast. Il n'est pas déplacé arbitrairement et la frontière n'est pas forcée à travers le chenal pour l'englober. Cette réserve est visible sur le comparatif.

Les superficies sont des ordres de grandeur obtenus à l'échelle locale du profil (environ 10,2 km² par cellule). La superficie historique exacte de la portion manquante n'est pas établie : aucun pourcentage fictif de distorsion historique n'est donné. `PEENE_FRONTIER_DEFORMATION.csv` mesure seulement le retrait de la frontière proposée par rapport à l'aide de dessin moderne. Pour B, il va de **0,05 à 1,92 pixel**, selon la ligne et le modèle (environ 0,15 à 5,5 km à cette latitude), pas une erreur historique certifiée.

Je recommande **B si la priorité est une représentation continentale plus complète**, avec ces limites explicitement acceptées ; A convient à un changement minimal. Les choix sont exclusifs : installer B ne signifie pas additionner 3+41.

## Bromberg : le blocage est politique et chronologique avant d'être géométrique

Les deux rectos N 1146/1 et le segment méridional de la carte conservée comme Güssefeld/Homann 1775 ont été relus localement. Les raccords graphiques sont visibles, mais ils ne démontrent pas l'actualisation juridique de la limite au 1er janvier 1776. Les rectos appartiennent au même document ; leur recouvrement n'est pas une confirmation indépendante.

Un contre-contrôle précis apparaît : le symbole de **Schubin/Szubin est placé au sud/ouest de la bande délimitée par le liseré**, alors que la [commune de Szubin date son incorporation prussienne de 1773](https://szubin.pl/historia-gminy.html), donc avant la date cible. Cette source municipale est un résumé historique, pas un acte contemporain de bornage. Elle suffit à contester l'emploi automatique du liseré entier comme frontière de 1776 ; **elle ne prouve pas que tous ses tronçons sont faux**.

Il manque un document permettant d'établir quel tronçon de ce liseré était effectivement souverain après les acquisitions de 1773 et avant janvier 1776. Les notices déjà conservées sur les rectifications de 1776–1777 ne donnent pas leurs actes ni leur date d'effet pour ce segment. Le texte rouge de propriété Skorzewska et la couleur d'un nom ne remplacent pas cette preuve. Voir `BROMBERG_SOUTHERN_BORDER.md` et le CSV des indices.

Le contrôle Vistule de R6 est conservé avec son ambiguïté de 2,5 pixels. Les largeurs de rivière sont correctement lues aux indices 3–15. Aucun point géographique nouveau n'est recherché pour réduire artificiellement un résidu alors que la ligne politique n'est pas identifiée. Aucune nouvelle projection de ce liseré dans le jeu n'est produite. Les 18 candidates directement adjacentes au noyau restent **C**, sans annexion des 142 cellules polonaises résiduelles.

## Conservation et fichiers

Tous les nouveaux fichiers se trouvent dans **R7 uniquement** : les 12 livrables demandés, le script `arbitration.py`, les règles, les empreintes, les lectures des sources et les mesures de déformation. Les pixels exacts, State_ID et propriétaires sont dans `PEENE_PROPOSED_CELLS.csv` et `CELL_DECISIONS.csv` ; les cartes sont explicitement des simulations, pas l'état chargé par le jeu.

**Validation statique finale : PASS, 42/42 contrôles.** Elle compare les 2 169 fichiers fonctionnels, les 306 fichiers R1–R6, les populations/cultures/religions, bâtiments/PM/propriétaires économiques, infrastructures/unités, le bitmap, HEAD et l'index. La référence reste **357 cellules SWE x567452, 85 PRU xEDB010, 142 PLC xFCC7B7 ; population 835 804 980**. Les 44 doublons RGB et 12 références invalides hérités sont maintenus séparément. Résultats détaillés dans `VALIDATION.json`.

Aucun commit, merge, push, reset ou changement d'index/branche. Aucun test moteur R7 revendiqué. Aucun appel ColGrep redondant : les chemins de sources et d'outils étaient déjà connus. Aucun nouveau modèle ni point de calibration n'est ajusté.

**Suite : attendre le choix explicite du joueur.** Une approximation approuvée sera enregistrée comme telle, jamais requalifiée en frontière géométriquement certifiée. Les historiques et redistributions démographiques éventuelles seront examinés dans la passe d'installation, sans population artificielle ni pertes silencieuses.
