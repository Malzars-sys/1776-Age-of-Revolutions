# TECH6R1-UI1 — Fiche opérateur runtime

## Préparation

1. Fermer complètement Victoria 3, puis relancer le jeu avec uniquement le fork actif.
2. Charger une partie contenant une mine de cuivre et une industrie alimentaire, ou démarrer une partie de test appropriée.
3. Ne pas modifier les méthodes de production uniquement pour fabriquer un cas six à huit groupes : le fork courant s'arrête naturellement à cinq.

## A — Fiche détaillée d'un bâtiment

1. Ouvrir une `building_copper_mine` dans un État.
2. Confirmer quatre sélecteurs de taille normale sur la première ligne et `pmg_ore_concentration_building_copper_mine` au début de la deuxième.
3. Vérifier que la deuxième ligne ne recouvre ni les barres d'emploi/réserves, ni les valeurs de rentabilité, ni la section suivante.
4. Cliquer successivement les cinq sélecteurs. Pour chacun, vérifier l'ouverture du menu, l'infobulle, le survol et le cadre de sélection.
5. Vérifier qu'un PMG verrouillé reste à sa place et qu'un déverrouillage ne réordonne pas la grille.

## B — Vue générale des bâtiments

1. Ouvrir la vue générale/groupée contenant la mine de cuivre.
2. Confirmer que les cases ont retrouvé la taille normale 50 x 50 px et ne sont plus comprimées horizontalement.
3. Confirmer le retour 4 + 1 sur deux lignes et l'alignement inchangé des boutons d'action à droite.
4. Répéter sur `building_food_industry`. Confirmer cinq icônes normales, un retour 4 + 1 et des barres de progression à leur largeur normale de 230 px.
5. Contrôler un bâtiment à un, deux, trois et quatre PMG : l'entrée doit conserver sa hauteur compacte sur une seule ligne.

## C — Building Registry non groupé

1. Afficher le registre sans regroupement par type.
2. Localiser une mine de cuivre à cinq PMG et vérifier que sa rangée grandit, sans réduire les icônes.
3. Vérifier que la rangée suivante commence après la seconde ligne PM et qu'aucun séparateur ne la traverse.
4. Faire défiler plusieurs écrans vers le bas puis vers le haut ; confirmer l'absence de saut, chevauchement ou sélection décalée.
5. Vérifier le nom de l'État, la taille, l'emploi, les réserves, la productivité et tous les boutons d'action.

## D — Building Registry groupé

1. Activer le regroupement par type.
2. Contrôler l'en-tête de `building_copper_mine` puis celui de `building_food_industry` : disposition 4 + 1, taille normale, actions alignées.
3. Développer chaque type et vérifier les rangées individuelles à hauteur variable ainsi que le défilement.
4. Replier les types et confirmer que la liste revient à un espacement cohérent.

## E — Autres surfaces

1. Dans le panneau d'un bien par État, survoler une entrée de bâtiment comportant cinq PMG et vérifier les cinq cases 50 x 50. Si un futur bâtiment atteint six PMG, confirmer la deuxième ligne.
2. Dans la liste de construction sur la carte, vérifier qu'une entrée à cinq PMG reste sur une ligne compacte et qu'un futur sixième passe à la ligne sans recouvrir les biens consommés/produits.
3. Ouvrir le panneau Construction : confirmer que les méthodes du secteur de construction et du chantier naval militaire restent utilisables.
4. Si une flotte possède l'administration navale correspondante, vérifier sa vue de méthodes : elle hérite de la grille générale corrigée.
5. Contrôler au minimum une mine, l'industrie alimentaire, l'industrie chimique, l'industrie automobile, une centrale électrique, une université et une administration gouvernementale.

## F — Journaux et résultat à renvoyer

Après les vérifications, fermer normalement le jeu et rechercher dans `error.log`, `warning.log` et `gui.log` :

- `production_methods.gui`
- `building_details_panel.gui`
- `building_browser_panel.gui`
- `goods_state_panel.gui`
- `map_list_panel.gui`
- `pdx_gui_container`
- `datamodel_wrap`
- `dynamicgridbox`
- `unknown property`
- `invalid property`

Noter pour chaque vue : `PASS`, `FAIL` ou `NON TESTÉ`, joindre une capture de la mine de cuivre dans la fiche détaillée, une capture du registre non groupé et une capture du registre groupé. En cas d'échec, préciser la résolution d'écran et l'échelle d'interface.

