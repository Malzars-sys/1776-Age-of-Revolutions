# TECH-3A GUI — audit de faisabilité du placement manuel

## Verdict

Pour Victoria 3 **1.13.9**, il n'existe pas de support vanilla permettant d'associer `technology_id, x, y` à chaque technologie. Les positions des nœuds **et** la géométrie des lignes sont produites séparément par le moteur natif. Un petit override GUI ne peut donc pas déplacer librement les nœuds tout en conservant correctement les lignes vanilla. Un résultat fonctionnel demanderait un arbre technologique custom complet, solution disproportionnée et fragile. Recommandation : **USE_VANILLA_AUTO_LAYOUT**.

Version contrôlée : `victoria3.exe` et `launcher/launcher-settings.json` indiquent **1.13.9**.

## 1. Engine findings

- Les trois graphes sont alimentés par `TechTreePanel.GetProductionTechTreeItems`, `GetMilitaryTechTreeItems` et `GetSocietyTechTreeItems` (`game/gui/tech_tree.gui`, lignes 509–584).
- Chaque instance de nœud reçoit `TechTreeItem.GetTechnology`, puis sa position opaque via `position = "[TechTreeItem.GetPosition]"` (lignes 757–763). Aucun calcul X/Y n'est présent dans le script GUI.
- Les lignes viennent d'autres collections natives (`...Get*TechTreeLines`). Chaque spline reçoit séparément `TechTreeLine.GetPosition` et `TechTreeLine.GetPointsInContainer` (lignes 1294–1319).
- La recherche dans tout `game/gui` ne révèle aucun setter de position, index, rang, voie ou ligne pour `TechTreeItem`, ni fonction GUI employée pour construire/remplacer un `CVector2` par technologie.

Conclusion démontrée : le moteur construit le graphe, les `TechTreeItem`, leurs coordonnées et les `TechTreeLine`. Le GUI vanilla ne fait que les rendre.

## 2. Actual layout controls

Les seuls contrôles accessibles trouvés sont globaux :

- taille d'un nœud : `{ 465 150 }` ;
- marges du graphe : widgets réservés `margin_top_left = { 50 150 }` et `margin_bottom_right = { 70 170 }` ;
- décalage/espacement des arêtes : widget réservé `line_offset`, position `{ 0 -10 }`, taille `{ 30 0 }` ;
- zoom, pan initial et recentrage : defines `NGUI.TECH_TREE_*` dans `common/defines/00_interfaces.txt` ;
- séparateurs d'ères décoratifs, placés globalement dans chaque graphe.

Ces valeurs modifient l'espacement, la caméra ou la décoration, pas la position d'une technologie donnée.

`category` sélectionne l'un des trois graphes natifs séparés. `era` participe au regroupement par bande d'ère (principalement l'axe Y dans ce GUI), mais l'API GUI n'expose ni la formule des axes ni le départage intra-bande. Les coordonnées internes exactes restent opaques.

L'inventaire exact des champs de premier niveau des technologies vanilla est : `era`, `texture`, `category`, `can_research`, `modifier`, `unlocking_technologies`, `ai_weight`, `on_researched`, `should_update_map`. Aucun `position`, `offset`, `x`, `y`, `row`, `column`, `lane`, `rank`, `index`, `order`, `sort`, `layout` ou `grid` n'existe. Les définitions d'ères ne donnent que `technology_cost` dans cette version.

## 3. Manual coordinate support

**Vanilla data only : non.** Une technologie ne peut pas fournir de coordonnées explicites. Modifier `era`, `category` ou le graphe des prérequis influence indirectement le layout, mais change sa classification ou ses données gameplay et ne constitue pas un placement libre.

L'effet de l'ordre des technologies, des fichiers et des éléments de `unlocking_technologies` reste **UNKNOWN** : aucun ordre n'est transmis au GUI et aucun dump de coordonnées n'est exposé. Un micro-test fiable aurait exigé deux lancements et une comparaison visuelle runtime après mutations temporaires ; il n'a pas été exécuté dans cet audit court. Même si un départage d'ordre existait, il ne fournirait pas des coordonnées libres ni une stabilité contractuelle.

## 4. GUI override feasibility

Un override léger pourrait au mieux remplacer visuellement la propriété `position` du widget par une liste de cas codée en dur. Il n'existe toutefois aucun fichier de mapping X/Y lu par le GUI vanilla, et surtout les points des splines resteraient ceux de `TechTreeLine`. Les nœuds et les connexions divergeraient : ce n'est pas une solution fonctionnelle.

Pour conserver recherche, tooltips, recherche en file, zoom, scroll, états visuels et lignes correctes avec des positions libres, il faudrait remplacer le modèle/rendu du graphe et recalculer aussi toutes les arêtes. Cela correspond à un **FULL_CUSTOM_TECH_TREE**, pas à un override localisé.

## 5. External editor feasibility

Un éditeur drag-and-drop peut facilement produire `tech_id,x,y`, mais le jeu 1.13.9 n'a aucun lecteur vanilla de ces données. Il ne devient utile qu'avec une chaîne de génération du type :

`éditeur → coordonnées → génération de GUI/nœuds/lignes custom → écran Technologie custom`

Il s'agit donc d'un outil de fabrication pour l'option C, pas d'une solution runtime autonome ni d'un simple fichier de données consommable par le GUI actuel.

## 6. Prerequisite-line behavior

Les lignes ne sont pas attachées dynamiquement aux ancres des widgets déplacés. Le moteur fournit à chaque `TechTreeLine` sa propre position et ses propres points de spline. Déplacer uniquement un nœud ne déplace donc pas correctement ses connexions. Un système manuel devrait recalculer et rendre les lignes lui-même.

## 7. Risk matrix

| Option | Faisable | Complexité | Maintenance | Risques principaux | Recommandée |
|---|---|---:|---:|---|---|
| A — `VANILLA_DATA_ONLY` | NO pour X/Y libre | LOW | LOW | Seulement influence indirecte via ère/catégorie/graphe ; prérequis à préserver | NO pour le manuel ; YES pour l'auto-layout |
| B — `LIGHT_GUI_OVERRIDE_WITH_MANUAL_LAYOUT` | NO fonctionnellement | HIGH | HIGH | Lignes désynchronisées, mapping codé en dur, scaling/résolutions | NO |
| C — `FULL_CUSTOM_TECH_TREE_GUI` | YES en principe | VERY_HIGH | HIGH | Réimplémentation interactions, lignes, zoom/scroll, recherche, DLC, mises à jour UI, performances | NO |
| D — `EXTERNAL_EDITOR + GAME_GUI_SUPPORT` | PARTIAL ; seulement avec C | VERY_HIGH | HIGH | Pipeline supplémentaire ; données inutilisables sans GUI custom | NO |

Compatibilité : A conserve le comportement DLC/sans DLC, sauvegardes, scaling, résolutions et performances vanilla. B casse la cohérence géométrique. C/D ne devraient pas altérer les sauvegardes si les IDs gameplay restent identiques, mais sont très sensibles aux mises à jour, contenus DLC, scaling, résolutions, zoom/scroll et régressions de l'écran Technologies.

## 8. Recommendation

Adopter **USE_VANILLA_AUTO_LAYOUT** pour TECH-3A.1. Traiter les nœuds de compatibilité isolés et les grands vides par une revue ciblée des données temporaires/du graphe prévue pour TECH-3A.1, sans lancer une réécriture GUI. Ne développer ni override de position ni éditeur externe tant que le bénéfice attendu ne justifie pas un arbre entièrement custom.

L'audit est concluant sur la question principale malgré les départages d'ordre non documentés : aucune variante d'ordre ne peut fournir le contrat `technology_id,x,y`, et le rendu indépendant des splines invalide l'override léger.
