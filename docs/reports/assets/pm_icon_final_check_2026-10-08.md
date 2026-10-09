# Vérification finale des icônes de PM — 8 octobre 2026

## Verdict

**Icônes de groupe et harmonisation locale des couleurs terminées et intégrées**, avec le bleu des données conservé et les deux dernières recolorations autorisées. Les **122 groupes définis dans le fork** utilisent une double flèche correspondant à leur famille. La clôture initiale a corrigé **76 raccordements** dans 16 fichiers ; sept corrections de famille la complètent ci-dessous. Aucun groupe visuel actif ne garde de placeholder ou de texture absente. Ce résultat n'est pas une approbation artistique exhaustive de tous les PM : les cinq placeholders individuels du cuivre restent en attente des icônes de la mise à jour 1.15, à la demande du joueur.

## Lot intégré

Salines, épices traditionnelles et épices mécanisées : trois raccordements, deux fichiers de PM, trois nouveaux DDS 208 × 208 BGRA8 natif avec huit mipmaps. Recettes, emplois, déblocages et groupes inchangés, masters copiés sans retouche.

[Sources finales, prompts complets de l'outil intégré imagegen et paramètres d'export](pm_salt_spices_sources_2026-10-08/manifest.json). Les planches et dérivés restent uniquement dans le cache ignoré par Git. Avec les profils navals, les flèches partagées et les dernières recolorations, le registre contient **151 exports**, reconstructibles octet pour octet.

Le [lot 13 intégré](pm_group_arrow_sources_2026-10-08/manifest.json) raccorde les groupes des routes et d'extraction du phosphate à une même double flèche jaune ; l'automatisation du phosphate utilise la flèche verte native. La [clôture de tous les groupes](pm_group_arrow_sources_2026-10-08/completion.json) intègre ensuite le lot 14, les six concentrations restantes, les six groupes cuivre et les incohérences de couleur des autres groupes locaux. Le doublage cuivre est **violet**, explicitement confirmé par le joueur. Santé : une seule variante vert bleuté de la flèche native, recolorée sans changer le dessin, l'alpha, les dimensions ou la valeur HSV. Les PM de santé et les constellations scientifiques gardent leurs dessins individuels approuvés ; seules leurs flèches de groupe changent.

Le [lot 15 approuvé et intégré](pm_secondary_colour_sources_2026-10-08/manifest.json) harmonise en violet « Aucune machine de précision », distillation fractionnée et craquage thermo-catalytique. Les dessins, dimensions, alpha et valeur HSV sont conservés. Deux exports existants sont remplacés et un export dédié est ajouté pour ne pas recolorer la texture native partagée de désactivation. Aucun changement de recette.

Le [lot 16 de cohérence des familles](pm_group_arrow_sources_2026-10-08/family_corrections.json) conserve les trois dessins bleus des données et raccorde leurs six groupes à la flèche bleue existante, selon la réponse « Conserver le bleu des données ». La cuisine fine épicée produit un bien secondaire : ses dessins violets restent inchangés et sa flèche de groupe devient violette. Sept raccordements dans deux fichiers, aucun nouveau DDS, aucun redessin ni changement de recette.

Le [lot 17 final de couleurs](pm_final_colour_sources_2026-10-08/manifest.json), explicitement autorisé pour terminer l'harmonisation, comprend les deux derniers cas, sans ajouter artificiellement un troisième dessin : avions tout métal et articles ménagers aluminium. Ils prennent le jaune de leurs groupes de production, en conservant leurs dessins, dimensions, alpha et valeur HSV par pixel. Le dessin de l'avion est natif ; celui des articles ménagers reste le dessin TKR. Deux DDS dédiés évitent d'écraser les originaux. L'export aluminium conserve ses 256 px et ajoute une chaîne complète de neuf mipmaps dans le DDS, sans miniatures PNG séparées. Aucun changement d'équilibrage.

## Contrôles effectués

- 518 définitions locales de PM, dont 152 identifiants absents du jeu installé, examinées avec les références vanilla.
- 576 PM distincts reliés aux 254 groupes utilisés par les bâtiments, toutes origines confondues.
- Au contrôle initial, 306 textures distinctes des PM locaux hors cuivre ont été décodées : aucune absente, illisible, totalement invisible ou copie du cerf sous un autre nom. Les exports des recolorations ultérieures sont également décodés et vérifiés.
- Aucun PM hors cuivre ne référence directement une texture d'erreur. Les cinq PM d'erreur restants sont ceux du cuivre ; leurs dessins individuels restent protégés en attendant la 1.15. Les six groupes cuivre ont désormais leurs flèches correctes.
- Aucun membre de groupe PM ni groupe référencé par un bâtiment n'est introuvable.
- Le contrôle initial recensait 54 nouveaux PM hors cuivre avec un dessin vanilla, dont 19 réemplois `unused/` à conserver. Les lots 15 et 17 remplacent deux de ces raccordements par des variantes de couleur dédiées. Ce recensement n'est pas une commande de nouveaux dessins : pics, pompes, explosifs, transport, états désactivés et monuments peuvent partager leur motif.
- Dessins et recettes individuels du cuivre et sept anciens PM de laboratoire conservés, vérification des empreintes protégées passée.
- 122 groupes locaux harmonisés, 253 groupes visuels actifs contrôlés avec le repli natif. Le 254e, `pmg_dummy`, est un auxiliaire natif non visuel pour les hubs urbains : sa texture volontairement absente est conservée et son identité vérifiée, pas traitée comme une panne.
- Lot 15 : recoloration seule vérifiée, 1 355 fichiers runtime hors périmètre protégés. Lot 16 : identité sémantique des groupes hors texture vérifiée, 1 359 autres fichiers runtime protégés par empreinte ; tous les dessins individuels, wagons, recettes, technologies, portraits, populations et révisions navales/économiques sont inchangés pendant cette correction de groupes.
- Lot 17 : deux recolorations seules vérifiées, alpha/valeur HSV et top mip identiques aux masters, recettes et groupes inchangés, 1 360 fichiers runtime hors périmètre protégés. Les DDS natifs et TKR d'origine, les populations, les bâtiments de départ et les technologies restent intacts.
- Reconstruction exacte des 151 exports et audit des raccordements passés : aucune référence absente ni correction restante hors cuivre.
- Aucun contrôle en jeu réalisé : ce résultat est statique.

## Oublis de groupes résolus

Après la clôture approuvée, **aucun groupe visuel actif, cuivre compris, ne conserve de texture d'erreur ou de référence introuvable**. Les pictogrammes des PM routiers déjà validés sont strictement conservés. Les groupes de production sont jaunes ; locomotives et automatisation vertes ; préparation, productions secondaires et organisation scientifique violettes ; militaire et canaux rouges ; santé vert bleuté ; imprimerie/distillation blanches ; personnel et données bleus.

Le lot 12 a aussi harmonisé en violet les deux PM de concassage du calcaire, sans redessin, et raccordé la flèche violette à leur groupe. L'imprimerie reprend sa flèche blanche existante. Voir [le registre du lot intégré](pm_limestone_colour_sources_2026-10-08/manifest.json).

## Points à vérifier sans les compter comme nouveaux dessins obligatoires

### Groupes sans champ de texture

Les neuf omissions constatées après le lot 13 sont maintenant corrigées avec des flèches existantes :

- `pmg_explosives_building_phosphate_mine`
- `pmg_ore_concentration_building_coal_mine`
- `pmg_ore_concentration_building_gold_mine`
- `pmg_ore_concentration_building_iron_mine`
- `pmg_ore_concentration_building_lead_mine`
- `pmg_ore_concentration_building_phosphate_mine`
- `pmg_ore_concentration_building_sulfur_mine`
- `pmg_salt_processing_building_salt_mine`
- `pmg_train_automation_building_phosphate_mine`

Le lot 14 intégré reprend les flèches existantes pour les explosifs du phosphate (jaune), le transport/automatisation du phosphate (vert) et la purification du sel (violet). Les six groupes de concentration des minerais utilisent aussi la flèche violette. Aucun nouveau fichier image par groupe : sept variantes partagées suffisent à tous les groupes locaux.

### Palette et sujet

**Lot 15 intégré après validation :** les masters finaux et la provenance sont conservés dans `pm_secondary_colour_sources_2026-10-08/`. La planche comparative à 32/48/64 px, les sorties candidates et les snapshots restent uniquement dans `.asset-cache/pm_batch_15_secondary_colours_2026-10-08/`. Le cuivre, les laboratoires, les fichiers vanilla `unused/`, les PM de chimie, les locomotives et les wagons n'ont pas été repris dans ce lot.

Après les lots 15 à 17, la file heuristique des PM nouveaux ou à image locale ne contient plus d'écart de couleur hors périmètres protégés. Les deux derniers cas ont été harmonisés sans redessin : avion tout métal et articles ménagers aluminium. Les données restent bleues, la cuisine fine épicée et les deux PM de raffinerie violets. L'audit peut toujours signaler des couleurs de PM vanilla hérités ou `unused/` retenus : ces signalements ne sont pas une commande de les modifier, et aucun original partagé n'est écrasé.

La **poudre sans fumée** (`pm_brine_electrolysis`, nom historique conservé) utilise encore `vaccum_brine_electrolysis.dds`, un bain à électrodes. La série poudre noire/nitroglycérine/dynamite a été approuvée, mais ce quatrième état n'a pas reçu de proposition spécifique à la poudre sans fumée. Son sujet reste donc à valider ; aucune nouvelle image de chimie n'a été générée pendant cette vérification.

L'exploitation forestière organisée réutilise la hache de la sylviculture simple et les deux institutions commerciales utilisent le symbole générique des monuments. Ces sujets sont cohérents avec leur fonction ; leur absence de dessin unique ne constitue pas à elle seule une panne ou une commande.

## Reproduction et limites

Contrôles communs : `tools/rebuild_asset_icons.cjs --verify`, `tools/audit_runtime_icon_bindings.py --check`, `tools/audit_pm_group_palette.py --report`. Couverture des groupes, sans les snapshots temporaires : `tools/preview_pm_group_bindings.py docs/reports/assets/pm_group_arrow_sources_2026-10-08/family_corrections.json --check-coverage`. Le mode `--check-integration` vérifie le périmètre exact avec les snapshots du cache de chaque intégration ; ces contrôles historiques ne doivent pas être relancés après une intégration ultérieure qui change légitimement leur périmètre protégé.

Inventaire final et planche de lecture des réemplois : `.asset-cache/pm_batch_11_salt_spices_2026-10-07/final_inventory.json` et `remaining_native_review.png`. Les snapshots complets, planches et PNG réduits ne sont pas versionnés. L'inventaire des chemins présents n'est jamais assimilé à une approbation artistique exhaustive.

