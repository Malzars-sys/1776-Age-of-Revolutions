# TECH6R1-UI1 — Rapport de mise en page globale des méthodes de production

## Verdict

`USER_RUNTIME_REQUIRED`

La correction globale est implémentée et le smoke de chargement Victoria 3 1.13.11 est propre. La syntaxe, le montage du mod et les journaux ciblés passent. La disposition visuelle, les clics et le défilement doivent encore être confirmés par l'opérateur dans une partie.

## Périmètre et cause racine

L'audit a trouvé six propriétaires directs du modèle `AccessProductionMethodGroups` et trois consommateurs indirects des widgets partagés.

La dégradation provenait de deux contraintes cumulées :

1. `buildings_production_method_item` avait été modifié pour faire tenir cinq groupes sur une seule ligne : pas horizontal réduit de 52 à 42 px et case réduite de 50 x 50 à 40 x 50 px. La bordure et l'espace cliquable n'étaient donc plus à la taille vanilla.
2. Les autres vues utilisaient des conteneurs ou des lignes de hauteur fixe (54, 80 ou 95 px). Une grille conservant des cases normales ne pouvait pas exposer une seconde rangée sans être coupée ou recouvrir la rangée suivante.
3. L'industrie alimentaire possédait un contournement dédié qui réduisait ses barres de progression de 230 à 170 px. Ce cas spécial masquait le problème architectural au lieu de le résoudre.

## Fichiers GUI impliqués

- `gui/production_methods.gui`
- `gui/building_details_panel.gui`
- `gui/building_browser_panel.gui`
- `gui/goods_state_panel.gui`
- `gui/map_list_panel.gui`

Les trois derniers fichiers sont des copies locales de leurs propriétaires vanilla 1.13.11, nécessaires pour modifier les vues correspondantes sans toucher aux données de jeu.

## Widgets et appelants

### Widgets modifiés

- `buildings_production_method_item`
- `buildings_production_method_item_potential`
- `old_buildings_production_method_item`
- `condensed_building_information`
- `condensed_building_information_pms`
- `building_browser_building_item`
- `building_browser_building_type_item`
- liste de bâtiments non groupée du Building Registry
- liste de bâtiments développée du Building Registry groupé
- sélecteur PM animé de `goods_state_panel.gui`
- zone PM de `construction_interaction_item_full`

### Appelants indirects couverts

- fiche détaillée d'un bâtiment : `condensed_building_information` ;
- vue générale/groupée des bâtiments : `buildings_production_method_item` ;
- bâtiments potentiels : `buildings_production_method_item_potential` ;
- panneau Construction : `old_buildings_production_method_item` ;
- panneau de flotte : `buildings_production_method_item` ;
- liste de construction sur la carte : `condensed_building_information_pms` ;
- Building Registry groupé et non groupé : widget partagé et grille directe.

## Dimensions préservées

| Surface | Case/bouton | Art de l'icône | Pas de grille |
|---|---:|---:|---:|
| Vue générale/groupée | 50 x 50 px | 40 x 40 px ; mixte 35 x 35 px | 52 x 50 px |
| Fiche détaillée / entrée développée | 70 x 70 px | 56 x 56 px (`80 %`) | 72 x 70 px |
| Building Registry individuel | 50 x 50 px | 40 x 40 px | 52 x 50 px |
| Panneau du bien par État | 50 x 50 px | 35 x 35 px | 54 x 50 px |
| Liste de construction sur la carte | 33 x 33 px | environ 26 x 26 px (`80 %`) | 32 x 33 px |

La vue générale retrouve ainsi sa case vanilla de 50 x 50 px et son pas de 52 px. L'industrie alimentaire n'utilise plus de réduction dédiée.

## Nouvelle architecture

- Les vues principales emploient `fixedgridbox` avec `datamodel_wrap = 4`. La largeur sûre est dérivée des emplacements disponibles : 4 x 52 = 208 px dans les cellules de 220 px du registre, et 4 x 72 = 288 px à côté des barres de progression de 230 px dans le panneau de 540 px.
- Les entrées générales conservent 95 px pour un à quatre PMG et réservent 145 px seulement lorsque `GetDataModelSize(...) > 4`.
- La fiche détaillée conserve 80 px pour un à quatre PMG et réserve 150 px lorsqu'une deuxième ligne de 70 px est nécessaire.
- Les deux listes individuelles du Building Registry passent d'une grille extérieure à hauteur fixe à une `dynamicgridbox` verticale d'un élément par rangée. La cellule PM possède une hauteur minimale vanilla et peut grandir à 100 px. La hauteur réelle participe donc au calcul du défilement.
- L'en-tête groupé du registre utilise quatre colonnes de 52 px dans sa cellule de 220 px et peut grandir avec la deuxième ligne.
- Le panneau d'un bien par État dispose de cinq colonnes de 54 px dans ses 270 px réellement disponibles et réserve deux lignes, soit jusqu'à dix groupes sans réduction.
- La liste de construction sur la carte conserve son format compact existant : cinq colonnes de 32 px dans 160 px, puis une deuxième ligne. Son entrée utilise désormais une hauteur minimale et non une hauteur verrouillée.
- La source des PMG n'est jamais dupliquée ni filtrée. L'ordre du datamodel reste l'ordre du bâtiment, y compris pour les groupes verrouillés.

## Matrice 1 à 8 PMG

Pour les vues principales à quatre colonnes :

| Nombre | Ligne 1 | Ligne 2 | Résultat structurel |
|---:|---|---|---|
| 1 | 1 | — | une ligne compacte |
| 2 | 1–2 | — | une ligne compacte |
| 3 | 1–3 | — | une ligne compacte |
| 4 | 1–4 | — | une ligne compacte |
| 5 | 1–4 | 5 | seconde ligne |
| 6 | 1–4 | 5–6 | seconde ligne |
| 7 | 1–4 | 5–7 | seconde ligne |
| 8 | 1–4 | 5–8 | seconde ligne complète |

La grille peut continuer au-delà de huit en ajoutant des lignes. Les vues secondaires à cinq colonnes placent 1–5 sur la première ligne et 6–10 sur la seconde.

## Bâtiments existants audités

L'inventaire courant comporte 73 bâtiments avec PMG : 20 à un groupe, 22 à deux, 16 à trois, 13 à quatre et 2 à cinq. Aucun bâtiment courant n'en possède six à huit ; ces tailles sont donc validées structurellement, sans modification gameplay de test.

- 5 PMG : `building_copper_mine`, `building_food_industry` ;
- 4 PMG : `building_automotive_industry`, mines de charbon/fer/plomb/soufre/or, centre urbain, élevage, plusieurs plantations ;
- 3 PMG : textile, verrerie, université, administration gouvernementale et plusieurs fermes/plantations ;
- 1–2 PMG : usines chimiques séparées, acier, moteurs, chantier naval et autres bâtiments simples.

Pour `building_copper_mine`, l'ordre attendu reste : équipement minier, explosifs, automatisation vapeur, transport ferroviaire, concentration du minerai. Le cinquième groupe `pmg_ore_concentration_building_copper_mine` doit donc apparaître seul au début de la deuxième ligne.

## Validation exécutée

- équilibre des accolades des cinq fichiers : profondeur finale 0, aucune profondeur négative ;
- audit de tous les accès et appelants PMG : terminé ;
- comparaison ciblée aux fichiers vanilla 1.13.11 : seules les modifications de disposition décrites sont présentes dans les trois nouveaux propriétaires GUI ;
- `git diff --check` : PASS ;
- smoke Victoria 3 : 9 septembre 2026, 17:52:49–17:53:35 Europe/Paris, lancement caché en `-debug_mode -gdpr-compliant`, mod monté depuis le chemin du fork, version `release/1.13.11` ;
- processus Victoria 3 restant après smoke : 0 ;
- journaux frais : `error.log` 537 lignes, `warning.log` 38 lignes, `gui.log` 48 lignes ;
- diagnostics ciblés nouveaux pour les cinq fichiers, `unknown property`, `invalid property`, erreur de parsing, `pdx_gui_container`, `datamodel_wrap` ou `dynamicgridbox` : 0.

Le premier rechargement à chaud avait détecté une tentative invalide de placer directement un `hbox` dans un `container`. Cette tentative a été corrigée avant le smoke final. Elle n'apparaît pas dans les journaux frais et n'est pas comptée comme erreur finale.

## Limites et runtime requis

- Le smoke prouve le chargement et l'absence d'erreur ciblée, pas le rendu à l'écran.
- Les cas naturels disponibles vont jusqu'à cinq PMG. Les cas six à huit sont couverts par le calcul déterministe de grille, mais nécessiteront une vérification visuelle lorsqu'un bâtiment réel atteindra ces nombres.
- Les clics, infobulles, cadres sélectionnés/verrouillés et le calcul visuel du défilement du registre doivent être confirmés avec la checklist opérateur.
- Aucun fichier gameplay n'a été modifié par TECH6R1-UI1.

