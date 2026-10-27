# CANADA-01 — province de Québec britannique au 1er janvier 1776

26 octobre 2026. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**.

## Résultat installé

L'affirmation était juste : Haut et Bas-Canada n'existent pas encore séparément en 1776. **ONT est réuni à QUE**, une seule colonie britannique nommée Province de Québec dans les deux langues, avec Guy Carleton. Son TAG reste QUE ; ONT demeure disponible pour une évolution ultérieure. 103 provinces changent seulement de TAG, les 220 autres provinces de QUE restent identiques : **323 provinces**. Aucun RGB, pixel, terrain, ressource ou hub modifié.

Le régime initial n'a plus de vote censitaire ni de homesteading : gouverneur sans assemblée élue et tenure locative, approximations du cadre de l'Acte de 1774. Les mouvements de rébellion de 1837 ne sont plus initialisés. Les noms dynamiques et l'introduction de sélection sont corrigés en FR/EN. La culture personnelle du gouverneur est britannique, sans changer la culture principale franco-canadienne de la colonie.

Population réunie **98 000 → 90 000**, variation mondiale **−8 000**, sans compensation artificielle. 87 621 franco-canadiens, 1 500 anglo-canadiens et les 879 Autochtones déjà présents dans les blocs coloniaux ; les 13 franco-canadiens protestants restent présents. 1 000 personnes dans la portion occidentale, 89 000 dans la région québécoise. Calibration pré-Loyalistes, pas recensement ethnique local exact ; séries historiques divergentes et périmètres détaillés dans [SOURCES_AND_FRONTIERS.md](SOURCES_AND_FRONTIERS.md).

Tous les bâtiments économiques de QUE sont conservés, avec PM, réserves et propriétaires économiques. Les deux commandes identiques de caserne, chacune de cinq niveaux, deviennent une commande de dix niveaux dans STATE_QUEBEC sous QUE ; les deux formations gardent leurs dix emplacements irréguliers. L'ancienne formation ONT conserve son point de ravitaillement occidental, mais recrute dans la région québécoise pour ne pas dépendre de seulement 1 000 habitants. Ce regroupement conserve la capacité du scénario ; il ne prétend pas reconstituer dix bataillons historiques.

**HBC inchangée : 108 626 habitants, tous les bâtiments et les 278 provinces protégés.** Aucun changement des 13 ensembles décentralisés ni des 2,4 millions d'habitants ajoutés. Même passage terrestre, dont le pays intermédiaire devient QUE : HBC–QUE–USA.

## Frontières : diagnostic et limites

Frontière politique intérieure supprimée. Cinq claims de juridiction occidentale ajoutés (Michigan, Ohio, Indiana, Illinois, Wisconsin), sans changement du contrôle territorial de ces États. Le découpage extérieur précis reste à faire : Labrador/îles annexés juridiquement en 1774, noyaux des postes occidentaux, marges du peuplement et occupation militaire américaine de Montréal. Les anciens contours coloniaux sont conservés provisoirement, sans les certifier comme administration effective. Voir le tableau de décisions dans SOURCES_AND_FRONTIERS.md. **La carte extérieure du Canada n'est pas déclarée terminée.**

## Vérification effectivement effectuée

- **26 contrôles de fusion réussis**, dont propriétaires mondiaux identiques sauf succession ONT→QUE, unicité locale, population, conservation HBC et autres POPs, actifs économiques, capacité militaire, pacte colonial unique, mouvements, lois, claims et localisation. `VALIDATION.json`.
- **Quatre tests négatifs/positifs de consolidation réussis** : seuls propriétaires publics successifs équivalents ; refus de perdre un propriétaire étranger, un PM distinct ou des réserves différentes. Commande : `python -X utf8 -m unittest discover -s tools -p test_canada01*.py -v`.
- **Audit technologique global local : FAIL_STATIC préexistant**, avant comme après. Deux alertes P0 de déblocage de PM (port et quantité commerciale), prérequis de construction et demandes de lois déjà présents. **Aucune nouvelle alerte** ; celle du vote censitaire disparaît. Résultats et delta conservés, sans modifier les tests ni attribuer ces dettes à la fusion. Aucune panne moteur observée à partir de ces seuls diagnostics.
- Aperçu dérivé du bitmap courant inspecté : `QUEBEC_1776.png`. Modèle de données politiques, pas carte de contrôle militaire.

Pas de lancement du jeu, de validation du budget, du marché, de l'emploi, de mouvement effectif, du siège de Québec ou de sauvegarde/rechargement. [Protocole et prochaines limites à préciser](NEXT_ACTION.md). Les anciennes preuves HBC restent des instantanés ; leurs assertions d'un ONT actif sont remplacées, pour cette interface seulement, par les preuves CANADA-01. Aucun fichier ancien restauré pour faire passer ces assertions obsolètes.

## Fichiers du jeu

- `common/history/states/00_states.txt`
- `common/history/pops/05_north_america.txt`
- `common/history/buildings/05_north_america.txt`
- `common/history/military_formations/01_military_formations_north_america.txt`
- `common/history/countries/que - quebec.txt`
- `common/history/diplomacy/00_subject_relationships.txt`
- `common/history/diplomacy/00_relations.txt`
- `common/history/political_movements/00_movements.txt`
- `common/history/ai/00_secret_goals.txt`
- `common/history/characters/cleanup2c1 - non europe rulers 1776.txt`
- `common/dynamic_country_names/1776_quebec_province.txt`
- `localization/french/1776_quebec_province_l_french.yml`
- `localization/french/country_flavor_text_l_french.yml`
- `localization/english/1776_quebec_province_l_english.yml`
- `localization/english/country_flavor_text_l_english.yml`

Patch borné sur les versions courantes, contrôlées par empreinte avant installation. Copies avant intervention dans `before/`, octets installés dans `patch/`. Aucun commit, staging, merge, rebase ou push ; aucune écriture vanilla ou suivi WORLD/SERG.

## Recherche déléguée

Un appel ColGrep-Agent local terminé, utile surtout pour retrouver le contexte et les dépendances générales. Les fiches territoriales décisives 0084 et 0090 ont été retrouvées par recherche exacte dans le CSV régional ; elles ont été relues. Pas de second appel redondant ni reconstruction d'index. Les chemins et extraits locaux ont été vérifiés. Durée complète et compteurs de tokens non instrumentés : aucune économie exacte de quota annoncée. Voir `COLGREP.json`.
