# PM — grain fin et dégradé vertical

Révision commencée le 3 octobre 2026, terminée le 4 octobre 2026.
Statut au 4 octobre : **10 PM validés et intégrés ; 7 PM du laboratoire conservés dans leur ancienne version en jeu**.

Le joueur a exclu les PM du laboratoire : ni la proposition plate ni la proposition granuleuse du laboratoire ne doivent être intégrées. Les sept DDS et leurs liaisons initiales restent inchangés. Les aperçus rejetés restent archivés, sans être sélectionnés.

Les quatre PM des routes et les six PM d'industrie/extraction sont désormais exportés et intégrés. [Planche des dix DDS décodés](DIX_PM_DDS_INTEGRES_QA.png), [accord du joueur](user_approval.json), [contrôle d'intégration](integration_static_validation.json).

## Résultat

Les 17 PM de la précédente révision ont reçu une texture granuleuse mate et un dégradé graphique du haut clair vers le bas plus sombre. Les sujets et leur composition restent ceux des versions plates. Aucun relief, biseau, ombre portée ou rendu réaliste de métal n'a été ajouté.

Les contours restent plus francs que ceux des références vanilla. Leur proximité de style reste donc une appréciation visuelle à valider par le joueur, et non une conformité parfaite déclarée automatiquement.

## Aperçus

- [4 PM des routes](PM_ROUTES_GRAIN_DEGRADE.png)
- [7 propositions du laboratoire — rejetées, non intégrées](PM_LABORATOIRE_GRAIN_DEGRADE.png)
- [6 PM d'industrie et d'extraction](PM_INDUSTRIE_GRAIN_DEGRADE.png)
- Comparaison avant/après avec les trois références vanilla, à 64 pixels : [page 1](PM_COMPARAISON_VANILLA_1.png), [page 2](PM_COMPARAISON_VANILLA_2.png), [page 3](PM_COMPARAISON_VANILLA_3.png).
- [Transparence sur damier](TRANSPARENCE_DAMIER.png).

Les planches par famille montrent aussi les formats 32, 48 et 64 pixels sur fond clair et sombre.

## Vérifications et limites

Les masters PNG et les réductions à 208 pixels ont un canal alpha réel, des coins totalement transparents et des silhouettes visibles. Les ouvertures des fioles, fenêtres, roues, tamis et de l'espace autour du feu ont été regardées sur damier et en petit format.

Avant l'intégration, les empreintes de **1 213 fichiers** de `common` et `gfx` étaient identiques à celles du début de la retouche ; ce contrôle historique reste dans `preview_validation.json`. Après accord, six DDS industriels ont été remplacés avec sauvegarde et quatre DDS des routes ont été ajoutés. Seules les quatre lignes `texture` du fichier des PM routiers ont changé dans les définitions. Les 1 206 autres fichiers protégés, dont les sept DDS et toutes les définitions du laboratoire, restent identiques. Aucun effet de gameplay n'a changé.

Les dix DDS utilisent le stockage natif BGRA8 et huit mipmaps (208, 104, 52, 26, 13, 6, 3, 1). Un décodage indépendant a confirmé que les couleurs et l'alpha de chaque mipmap correspondent à l'export attendu. Les six anciens DDS remplacés sont conservés dans `backups/`.

L'image vanilla du bâtiment Infrastructures régionales et la proposition de technologie Génie routier restent inchangées. Aucun test en jeu de ces nouveaux aperçus n'a été effectué.

## Sources et génération

Mode : **imagegen intégré (BUILTIN_IMAGE_GEN), édition des images précédentes**. Chaque requête prend le PM plat comme cible et les trois exemples vanilla fournis comme références de style.

- [Prompts complets et références de chaque PM](generation_requests.json)
- [Chemins des originaux générés et des copies](generation_results.json)
- [Plan des 17 PM et de leurs liaisons futures](revision_plan.json)
- [Contrôles techniques](preview_validation.json)
- [Relecture visuelle](visual_review.json)
- `inputs/` : copies intactes des 17 versions plates.
- `previews/` : les 17 nouveaux masters PNG, copiés sans retouche artistique.
- `target_size_png/` : réductions mécaniques à 208 pixels, non installées dans le jeu.
- `references/` : copies des trois exemples vanilla.
- `baseline.json` : empreintes initiales protégées.

Après imagegen, seules les copies, les réductions de format et les planches de comparaison ont été réalisées. Pas de grain ni de dégradé ajouté manuellement.

## Suite

Les dix PM validés sont intégrés et contrôlés statiquement. Une vérification en jeu après redémarrage reste à effectuer ; aucun rendu moteur n'est revendiqué. Les sept PM du laboratoire ne font pas partie de cette intégration.

Les anciennes propositions restent disponibles dans [le dossier précédent](../asset8_flat_revision_2026-10-03/README.md). Seuls ses dix PM hors laboratoire sont remplacés par la révision granuleuse intégrée. Les deux séries proposées du laboratoire sont écartées au profit des anciennes icônes en jeu. La technologie et le bâtiment vanilla restent inchangés.
