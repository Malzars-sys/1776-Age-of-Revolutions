# Lot 3 — Chaîne du pétrole

Création : 2 octobre 2026. Mise à jour : 3 octobre 2026. **Les six icônes du lot sont intégrées et vérifiées hors jeu, dont la raffinerie V3 validée.**

## Périmètre

| Famille | Aperçu | Fichier original |
|---|---|---|
| Bien | Carburants raffinés — motif kérosène | [PNG](previews/refined_fuels.png) |
| Bien | Lubrifiants | [PNG](previews/lubricants.png) |
| Bien | Produits pétroliers lourds | [PNG](previews/heavy_petroleum_products.png) |
| Bâtiment | Raffinerie de pétrole — contraste renforcé derrière les produits | [PNG](previews/oil_refinery_v3_foreground_contrast.png) |
| PM | Distillation fractionnée | [PNG](previews/fractional_distillation_refinery.png) |
| PM | Craquage thermique et catalytique — ouverture autour de la flamme transparente | [PNG](previews/thermal_catalytic_cracking_refinery_v2_open_fire.png) |

Le kérosène sert à illustrer le bien déjà nommé « Carburants raffinés » ; aucun bien supplémentaire n'est créé. Les recettes, prix, emplois, technologies et données industrielles ne changent pas. La technologie de distillation fractionnée conserve son illustration native. Aucun asset du cuivre, des laboratoires ou du lot ciment n'est modifié.

Les définitions actuelles placent la raffinerie et la distillation fractionnée derrière `fractional_distillation`, ère VI ; le craquage derrière `plastics`, ère X. Ces ères ne sont pas traduites arbitrairement en une année historique précise.

## Recherches sur Internet, avant génération

Recherche d'images effectuée pour les quatre sujets demandés. Ces photos documentent les objets et matériaux ; elles ne sont ni copiées dans les fichiers de jeu ni utilisées comme illustrations finales.

- Raffinerie : [Oil City, vers 1880 — ExplorePAHistory, photographie de la collection NYPL](https://explorepahistory.com/displayimage.php%3FimgId%3D1-2-171%26storyId%3D1-9-E.html). Réservoirs cylindriques, bâtiments bas et cheminées ; pas de tour de forage présentée comme raffinerie.
- Lubrifiants : [burette brevetée en 1866 — Smithsonian, National Museum of American History](https://www.americanhistory.si.edu/collections/object/nmah_880362). Réservoir en laiton et bec étroit d'application ; aucune étiquette de brevet ou marque reprise.
- Kérosène : [bidon Pennant, K1326 — Powerhouse Collection](https://collection.powerhouse.com.au/object/260821). Cylindre en fer-blanc, épaulement conique et col court. Le catalogue donne une fabrication 1900–1940 : référence de contenant historique tardif, pas une attribution à 1776. Aucune marque Pennant/Shell reproduite.
- Produits lourds : [échantillon de fioul lourd — Bagwan Petroleum](https://www.tradeindia.com/products/heavy-fuel-oil-c7833897.html). Référence de matière sombre et visqueuse, pas de contenant commercial ou de photographie copiée.

Distinction des procédés : [EIA, séparation par distillation et conversion par craquage](https://www.eia.gov/energyexplained/oil-and-petroleum-products/refining-crude-oil-the-refining-process.php), [ACS, histoire du procédé Houdry](https://www.acs.org/education/whatischemistry/landmarks/houdry.html). Les glyphes sont des conventions lisibles d'interface, pas des plans techniques complets.

Les recherches et observations sont consignées dans [internet_references.json](internet_references.json). Certains liens d'image ou pages de musées n'ont pas pu être ouverts directement par le navigateur de recherche ; les notices et descriptions indexées ont été utilisées dans ces cas. Aucun média distant n'a été téléchargé.

## Création et contrôle

Mode : **génération d'images intégrée** (`BUILTIN_IMAGE_GEN`), pas de script d'API externe. Une génération distincte par sujet, puis une retouche ciblée de la transparence de la raffinerie. Les [prompts complets](prompts.json) et le [prompt de retouche](refinery_alpha_fix_prompt.json) décrivent explicitement le rôle des références et les contraintes. La première raffinerie est conservée séparément. Les photographies en ligne servent de documentation descriptive, pas d'images injectées à recopier.

Les sept références du jeu installé sont uniquement des comparaisons locales de style et ne sont pas des créations originales à redistribuer. Les biens sont détourés, le bâtiment est une scène encadrée, les PM sont des glyphes ocre en bas-relief. Le motif de carburant de la raffinerie reprend le nouveau bien afin de conserver une identité cohérente.

Livrables de contrôle : [planche générale](LOT_3_APERCU.png), [comparaison aux références natives](LOT_3_COMPARAISON_VANILLA.png), [transparence sur damier](LOT_3_ALPHA_DAMIER.png), [contrôles techniques](preview_validation.json), [manifest des six fichiers](preview_manifest.json).

Les masters ne sont pas retouchés automatiquement. Les PNG réduits sont des prévisualisations : 256 px pour les biens et le bâtiment, 208 px pour les PM. Les DDS, références de textures et essais en jeu attendent l'approbation visuelle. Si le contrôle signale une opacité intérieure imparfaite du bâtiment, elle doit être corrigée ou acceptée explicitement avant export.

Résultat du contrôle : six masters carrés de 1254 px, véritables coins transparents pour les six images, réductions et comparaison native produites. Les **1 200 fichiers** `common` et `gfx` sont inchangés ; aucun DDS ajouté. Avertissement restant : la scène intérieure de la raffinerie V2 conserve une opacité très légèrement imparfaite (minimum mesuré 250/255 dans la zone centrale). Les coins sont corrigés ; le défaut intérieur reste à résoudre ou à accepter explicitement avant intégration. Aucun essai en jeu n'est revendiqué.

Les chemins des sorties du générateur et de leurs copies dans ce dossier sont conservés dans [generation_results.json](generation_results.json).

Les paragraphes de contrôle ci-dessus décrivent le **premier état d'aperçu**, avant l'autorisation d'intégrer « le reste ». Leurs planches et rapports sont conservés comme historique ; ils ne décrivent pas l'état actuel des fichiers de jeu.

## Retouches demandées et intégration actuelle

La précision « je parle de la raffinerie » vise le décor derrière le bidon et la bouteille, pas la conduite du glyphe de craquage. La nouvelle raffinerie assombrit ce décor localement pour détacher les produits, sans modifier leur emplacement. Après présentation de cette version et de sa légère transparence intérieure (minimum 250/255 dans le master), le joueur a confirmé : « Hop, c'est mieux, tu peux l'intégrer. » La V3 est donc intégrée **telle que validée**, sans nouvelle génération, recoloriage ni correction automatique de l'alpha.

Une seconde demande rend transparent le noir autour de la flamme du glyphe de craquage. Cette retouche conserve la flamme, le cadre, le réacteur et la goutte. La transparence a été contrôlée dans le master **et dans le DDS décodé**, à l'intérieur de l'ouverture. Les marques rouges de la capture ne sont pas reprises.

Mode des deux retouches : **outil intégré de génération/retouche d'images**, sans API externe. Sources, sorties sauvegardées et prompts exacts : [requested_retouch_prompts.json](requested_retouch_prompts.json). Les versions antérieures des deux peintures restent disponibles dans `previews/`. Aucun recoloriage ni changement de masque automatique n'est appliqué lors de l'export.

| Icône intégrée | Fichier de jeu |
|---|---|
| Carburants raffinés | `gfx/interface/icons/goods_icons/1776_refined_fuels.dds` |
| Lubrifiants | `gfx/interface/icons/goods_icons/1776_lubricants.dds` |
| Produits pétroliers lourds | `gfx/interface/icons/goods_icons/1776_heavy_petroleum_products.dds` |
| Distillation fractionnée | `gfx/interface/icons/production_method_icons/1776_fractional_distillation_refinery.dds` |
| Craquage thermique et catalytique, ouverture transparente | `gfx/interface/icons/production_method_icons/1776_thermal_catalytic_cracking_refinery.dds` |
| Raffinerie V3, décor assombri derrière les produits | `gfx/interface/icons/building_icons/1776_oil_refinery.dds` |

La première intégration modifiait cinq références de textures dans trois fichiers de définition ; ses rapports sont archivés avec le préfixe `five_icons_`. La seconde intégration modifie **uniquement le champ d'icône du bâtiment raffinerie** et ajoute son DDS de 256 px avec neuf niveaux de réduction. Un nouvel état de référence est enregistré juste avant cette étape : les **1 204 autres fichiers protégés**, y compris les cinq DDS déjà intégrés, restent identiques. Le contrôle indépendant redécode les six DDS et confirme leurs références de jeu. Le contenu logique des définitions est identique avant/après, hors champs visuels : recettes, prix, emplois, construction et technologies ne changent pas. La transparence générée est conservée telle quelle. Aucun essai dans le moteur du jeu n'a été effectué.

Contrôles actuels : [retouches sur fond clair et sombre](LOT_3_RETOUCHES_QA.png), [icônes décodées depuis les DDS](LOT_3_DDS_INTEGRES_QA.png), [validation des retouches](requested_retouches_validation.json), [validation de l'intégration](integration_static_validation.json), [manifest d'intégration et état avant modification](integration_manifest.json).

Reproduction : `tools/check_asset6_requested_retouches.cjs` pour la comparaison des retouches et `tools/validate_asset6_approved_icons.py` pour le contrôle des DDS et des définitions. L'ancien `tools/build_asset6_preview_sheet.cjs` est réservé à l'état historique **avant intégration** ; son garde-fou refuse volontairement les fichiers de jeu désormais intégrés.
