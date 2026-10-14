# MAP-2B — Intégration locale et observation après un mois

Date : 10 octobre 2026. Aucun commit, merge ou push ; aucune intégration automatique MAP-2C.

## Résultat

Six provinces ont changé de propriétaire dans quatre régions : Trentin, Istrie, Lombardie et Provence. La géométrie, les TAGs, les capitales, les technologies et les dépendances diplomatiques sont inchangés. Les compromis sont explicitement classés `DOCUMENTED_GAMEPLAY_APPROXIMATION`, et non présentés comme des frontières vérifiées au village près.

Le correctif des infrastructures couvre les 69 États initialement signalés. La sauvegarde fournie `observateur_3`, au **1er février 1776**, permet une première observation native : **59 de ces 69 États ont un solde d'infrastructure non négatif ; dix restent déficitaires**. Il existe également sept déficits hors de cette liste initiale. Le problème global n'est donc pas déclaré entièrement résolu.

## Territoires intégrés

| Région | RGB | Transfert | Habitants réaffectés, sans création |
|---|---|---|---:|
| Trentin | xD0BF60 et x1120FF | VEN → AUS | 245 500 ensemble |
| Istrie septentrionale/orientale | x3060BF et xF0A040 | VEN → AUS | 226 500 ensemble |
| Lombardie orientale | x4713EE | AUS → VEN | 350 058 |
| Avignon/Comtat | xB0C0E0 | FRA → PAP | 99 500 |

Total réaffecté : **921 558**. Le total mondial reste exactement **835 804 980** ; les totaux par culture/religion, à l'échelle mondiale et dans chacune des régions concernées, sont conservés. Les allocations locales sont des hypothèses de gameplay qualitatives et documentées, pas des recensements de 1776 et pas une simple division par nombre de provinces.

Limites importantes :

- Trente et Bressanone étaient des principautés ecclésiastiques impériales. AUS sert ici de représentation simplifiée de cet espace sous influence/protection habsbourgeoise, **pas d'affirmation d'une annexion directe avant 1803**. Rovereto n'est plus vénitien après 1509. Références : recherches R2 et [archives de Trente](https://archiviodistatotrento.cultura.gov.it/antichi-regimi/), [fonds vénitiens de Rovereto](https://www.bibliotecacivica.rovereto.tn.it/Patrimonio-e-risorse/Archivi-storici/Fondi-e-documenti-del-periodo-veneziano).
- La correction d'Istrie distingue littoral vénitien et secteur habsbourgeois. Elle ne prétend pas tracer exactement Pazin : la grande province centrale/côtière `x36B2E3` demeure un cas mixte. [Document municipal de Pazin/Lindar](https://www.pazin.hr/wp-content/uploads/Obrazlo%C5%BEenje-Plana-UPU-Lindar.pdf), R2-0004/0005.
- `x4713EE` représente Brescia/Crema, mais absorbe une frange vers Crémone. Milan, Côme, Mantoue et les autres possessions autrichiennes sont conservés ; `x867A90` VEN et `x9AC196` SWI restent protégés. [Institutions lombardes](https://www.lombardiabeniculturali.it/istituzioni/storia/?unita=03.03), R1-0008/0009.
- La province d'Avignon/Comtat contient un peu d'arrière-pays français. Les protestants français existants restent tous dans la subdivision FRA ; aucune conversion n'est effectuée. Les plantations françaises de soie et de coton et Nice sarde sont préservées. [FranceArchives](https://francearchives.gouv.fr/fr/article/350923806), R1-0016/0017.

Bénévent/Pontecorvo et Côme/Chiavenna sont reportés : une province entière absorberait un territoire voisin disproportionné. Aucun nouveau TAG ni redécoupage du bitmap n'est introduit. Les corrections pertinentes héritées du collaborateur sont conservées ; sa branche n'est pas fusionnée globalement et sa proposition contradictoire sur `x9AC196` n'est pas importée.

## Bâtiments et unités

Onze niveaux de bâtiments hors infrastructures sont réaffectés territorialement : Trentin (blé 1, vigne 1), Lombardie (vigne 1, soie 1), Istrie (port 2, pêche 2, commerce 1, chantier naval gouvernemental 1), Provence (industrie alimentaire 1).

Les propriétaires économiques étrangers, les niveaux, réserves et PM sont conservés. Seul le siège de l'investisseur vénitien de l'ancienne subdivision du Tyrol du Sud est déplacé vers la Vénétie pour éviter une référence disparue. Aucun bâtiment n'est nationalisé automatiquement. Les deux niveaux de riz autrichiens en Lombardie restent inchangés.

Une référence de recrutement de conscrits vénitiens est déplacée du Tyrol du Sud à la Lombardie vénitienne. Le total des unités, types et services reste exactement identique : **3 883** dans l'inventaire global, conscrits compris. Aucun changement d'armée ottomane ou d'administration ottomane.

## Infrastructures : réglage initial

Les cibles des 69 États ajoutent finalement **172 niveaux effectifs par rapport aux historiques réellement présents avant ce lot** ; la Wallonie, déjà corrigée à 13, reste à 13. Sept autres niveaux accompagnent les transferts territoriaux (AUS Tyrol du Sud 2, AUS Istrie 2, VEN Lombardie 2, PAP Provence 1).

Le différentiel écrit dans tous les fichiers est de 257 niveaux, car certaines déclarations sont répétées entre historiques de base et surcouche. **257 n'est pas le nombre de niveaux supplémentaires effectivement chargés.** Le manifeste distingue les niveaux écrits et les cibles par État.

La première projection prévoyait 33 niveaux à Rio sur la base d'un cache initial dégradé. L'observation native montre 71,79897 d'infrastructure avec 19,93299 niveaux effectivement employés, trois ports élémentaires remplis (9 d'infrastructure) et la base de 3 : soit exactement `12 + 3 × 19,93299`. Les huit niveaux routiers historiques permettent donc déjà 36 à pleine occupation ; les 25 niveaux supplémentaires sont retirés du projet, pas des bâtiments historiques. La demande estimée après retrait de leurs investisseurs supplémentaires devient 20,6. Ce dernier ajustement est statiquement contrôlé mais **pas encore mesuré dans une nouvelle partie**.

Les routes traditionnelles sans consommation de biens sont retenues dans 67 cas ; les deux PM de routes à péage britanniques déjà sélectionnés (Terre-Neuve et Jamaïque) sont conservés. Aucune technologie n'est accordée et aucun canal/train/passager non fiable n'est compté dans la réserve. Les salaires restent à payer. Les projections supposent une occupation complète et une réserve minimale estimée de 2,1 ; elles ne garantissent ni recrutement, ni budget, ni accès au marché au premier jour.

## Test natif fourni : observateur_3

Source lue sans modification : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/save games/observateur_3.v3`.

SHA-256 : `9d3f2f71c224edbfe54d279576184b5126d630609981dfa3de5ce307f09299b9`.

Version 1.13.11, date de jeu 1776.2.1 ; 1 048 États inspectés. Les marqueurs PAP en Provence, absence de VEN au Tyrol du Sud et Wallonie à 13 confirment que des changements MAP-2B sont chargés. **68 des 69 cibles préliminaires de niveaux correspondent**, mais la Prusse orientale a chargé 1 au lieu des 3 présents dans les fichiers finaux. Rio, ensuite ramené à huit, diffère également de la sauvegarde. On ne peut pas distinguer ici une partie créée pendant les modifications d'une démolition ultérieure par l'IA en Prusse orientale ; un démarrage après stabilisation des fichiers reste nécessaire.

| Wallonie | observateur_2, 1er janvier | observateur_3, 1er février |
|---|---:|---:|
| Niveaux chargés | 6 | 13 |
| Occupation, équivalent niveaux | 6 | 13 |
| Infrastructure | 23,1 après retrait du cache périmé des canaux | 46,2 sérialisés |
| Utilisation | 40,5 | 41,9 |
| Solde | −17,4 reconstitués, interface initiale arrondie −17 | **+4,3 observés** |

Le cache de janvier indiquait encore 29,7, avant actualisation des changements de PM ; il ne doit pas être présenté comme l'infrastructure effective constatée à l'écran. Aucun pourcentage d'accès au marché n'est déduit du champ `counters.market_access`, qui est un compteur de recalcul et non une mesure d'accès.

Les dix déficits persistants de la liste initiale :

| État / propriétaire | Solde de février | Occupation / niveaux |
|---|---:|---:|
| District of Columbia / USA | −16,532 | 0,056 / 7 |
| Géorgie / USA | −5,007 | 0,086 / 4 |
| Antilles / SPA | −5,30306 | 0 / 4 |
| Floride / GBR | −0,18809 | 1,83995 / 7 |
| Bermudes / GBR | −3,59378 | 0,02499 / 3 |
| Jamaïque / GBR | −2,60626 | 2,23332 / 4 |
| Alxa / CHI | −1,897 | 0,002 / 5 |
| Amour / CHI | −3,75 | 0 / 3 |
| Åland / SWE | −2,71454 | 0,3 / 3 |
| Prusse orientale / PRU | −2,87 | 1 / 1, cible finale 3 |

Neuf sont sous-employés. Huit utilisent des routes traditionnelles sans intrants : une pénurie de bois/outils ne peut pas expliquer directement leur production routière. En Jamaïque, l'IA a sélectionné routes à péage et canaux ; occupation et consommation doivent être suivies séparément.

Les statistiques d'emploi révèlent une véritable concurrence avec les emplois publics/militaires : Alxa compte 13 410 salariés militaires pour 13 412 salariés au total ; les Antilles espagnoles 3 965 pour 4 328 ; Washington 1 420 employés gouvernementaux pour 1 637 salariés. Washington n'a qu'environ 5 248 habitants, alors que sept niveaux routiers demandent 7 000 postes à pleine occupation. Il ne suffit donc pas d'empiler des niveaux ; il faut un correctif distinct de recrutement/dimensionnement des emplois, à autoriser sans annuler les protections démographiques et militaires de MAP-2B.

Les sept autres déficits observés concernent Minsk, Nouveau-Brunswick, Guyenne, îles de la Sonde, Tonkin, Jiangsu et Galicie orientale. Ils sont documentés, **pas automatiquement modifiés hors de la liste initiale**. Tonkin/Jiangsu notamment ont des réseaux remplis mais une capacité insuffisante en février.

## Validations et fichiers

`validate_map2b.py` : **PASS_STATIC**. Conservation des populations/cultures/religions, bâtiments hors infrastructures et effectifs ; RGB valides, aucune province perdue ni nouvelle attribution double, capitales/dépendances inchangées, protection MAP-2A et Luxembourg/BEO. Les 62 doubles attributions et **14 anomalies de référence préexistantes** restent inventoriées ; aucune nouvelle, aucune dans le périmètre territorial de ce lot.

Sur 1 617 fichiers protégés à l'instantané, 1 599 sont strictement inchangés. Dix-huit fichiers de gameplay sont modifiés, exclusivement dans les historiques : 14 fichiers de bâtiments, un de formations militaires, deux de populations et un de propriétaires territoriaux. Rio revient à ses niveaux initiaux ; les autres corrections d'Amérique du Sud sont maintenues. La liste complète figure dans `MAP2B_VALIDATION.json`. Les sources, outils et livrables ajoutés sont hors de ce décompte.

Dix scénarios de modèles sur les scripts d'infrastructure passent. Les contrôles ottomans passent, notamment 1 024 combinaisons administratives, 192 combinaisons politiques, introduction des journaux et indépendance de leurs conditions. Le vieux contrôle qui gelait tout le fichier Europe du Sud contre un ancien commit ne peut pas valider ce lot de Lombardie ; il est marqué non applicable, et remplacé pour ce point par la comparaison ciblée des administrations ottomanes avec l'instantané réel, qui passe. Ces modèles ne sont pas des tests dans le moteur du jeu.

Les quatre manifestes CSV sont contrôlés cellule par cellule avec la compétence de tableaux, recalculés et prévisualisés ; les observations de sauvegarde sont clairement séparées des réserves théoriques. `OBSERVATEUR_3_COMPARISON.json` contient les mesures natives et les statistiques d'emploi.

Le contrôle de mise en forme `git diff --check` signale neuf lignes blanches avec espaces/tabulations en fin de ligne dans la surcouche des bâtiments ; il n'est donc pas présenté comme réussi. Cette comparaison porte sur l'ensemble des changements locaux depuis HEAD, pas uniquement ce lot. Les contrôles de syntaxe et de structure exécutés ci-dessus passent indépendamment de ces avertissements de mise en forme.

Conclusion : **lot territorial intégré et contrôlé ; infrastructures améliorées mais pas entièrement résolues en jeu**. Ne pas annoncer 69/69 corrigés. Avant extension MAP-2C : décider du correctif de recrutement, confirmer les trois niveaux de Prusse orientale sur un nouveau démarrage, puis mesurer une nouvelle sauvegarde à un mois.
