# Lot 8 — révision 2

**Les trois icônes sont approuvées et intégrées.** Drapeaux conservés exactement ; charpente diagonale et coque en fer issues de cette révision 2.

[Validation d'intégration](integration_static_validation.json) · [Couleurs des DDS décodés](LOT_8_DDS_INTEGRES_QA.png) · [Accord du joueur](user_approval.json)

[Les deux corrections](DEUX_CORRECTIONS_APERCU.png) · [Comparaison vanilla](LOT_8_COMPARAISON_VANILLA.png) · [Alpha sur damier](LOT_8_ALPHA_DAMIER.png)

## Modifications intégrées

- **Charpente diagonale** : les renforts suivent désormais le flanc intérieur, au lieu de traverser le creux du bateau. L'espace central reste libre et les couples courbes restent lisibles.
- **Coques en fer** : le troisième élément ambigu a été retiré ; les courbes et les raccords de la partie ouverte sont simplifiés. L'identité du grand bordé riveté à droite, sa palette et son angle de vue sont conservés.
- **Signaux navals** : le PNG approuvé du premier aperçu est réutilisé directement, avec contrôle de son empreinte. Aucun appel de génération ni retouche pour ces drapeaux.

La relecture est visuelle, pas une certification d'ingénierie : les deux coques sont des illustrations conceptuelles simplifiées.

## Création et sources

Retouches artistiques réalisées uniquement avec l'outil **imagegen intégré**, en utilisant les anciennes versions comme cibles et deux technologies vanilla comme références de style. Aucun recours au CLI de génération.

[Prompts exacts et images d'entrée](generation_requests.json) · [Origines des résultats](generation_results.json) · [Plan actif](generation_plan.json) · [Retour du joueur](user_feedback.json)

[Références historiques de cette révision](historical_references.json) · [Archive initiale](../historical_references.json)

Le [catalogue du modèle SLR2908](https://www.rmg.co.uk/collections/objects/rmgc-object-68863) décrit les renforts diagonaux et longitudinaux du principe amélioré vers 1814. La [présentation du Vulcan](https://culturenl.co.uk/the-vulcan/) confirme la construction originale en plaques de fer et couples forgés en cornière. Le positionnement et la simplification des éléments de ces icônes restent des interprétations graphiques, pas une copie technique des objets.

Les liens directs vers certaines photographies de musée et le plan de 1818 n'ont pas pu être chargés cette fois. Leur consultation complète n'est donc pas revendiquée.

## PNG sélectionnés

- [Charpente diagonale v2](previews/diagonal_ship_framing_v2_padded.png)
- [Coques en fer v2](previews/iron_hull_construction_v2_padded.png)
- [Drapeaux approuvés, inchangés](../previews/standardized_naval_signals_padded.png)

Les anciens aperçus, les nouveaux PNG bruts de 1254 px et les originaux imagegen sont conservés. Seul le cadrage technique des nouveaux aperçus ajoute une toile transparente de 1446 px : [preuve de conservation exacte des pixels RGBA](canvas_padding.json). Aucun redessin ou masquage par les outils de mise en page.

## Contrôles des aperçus avant intégration

[Validation technique](preview_validation.json) · [Relecture visuelle](visual_review.json)

Transparence réelle, absence de fond intégré, comparaison avec trois technologies vanilla sur fonds clair/sombre et lecture à 48/64 px, plus 32 px en complément.

L'état avant intégration est conservé dans les rapports de préparation. Les PM du laboratoire et les assets précédemment approuvés restent hors périmètre.

## Intégration et vérification finales

Accord explicite du joueur : « Donc tu peux les intégrer hein. » Les trois PNG sélectionnés ont été identifiés par leur empreinte avant conversion, pour ne pas utiliser les anciennes versions des coques.

Trois DDS natifs 256 × 256, neuf mipmaps, **BGRA8 legacy A8R8G8B8** :

- [Signaux navals](../../../../../gfx/interface/icons/invention_icons/1776_standardized_naval_signals.dds)
- [Charpente diagonale](../../../../../gfx/interface/icons/invention_icons/1776_diagonal_ship_framing.dds)
- [Coques en fer](../../../../../gfx/interface/icons/invention_icons/1776_iron_hull_construction.dds)

Seules les trois lignes de texture correspondantes dans `common/technology/technologies/25_tech3a_naval.txt` ont été modifiées pendant cette intégration. Les autres **1222 fichiers protégés déjà présents** sont inchangés ; exactement trois nouveaux DDS ont été ajoutés. Les autres changements préexistants du dépôt sont conservés. Aucun changement de gameplay, de localisation ou d'icône du laboratoire.

Contrôle indépendant : les couleurs RGBA et l'alpha correspondent aux PNG de référence pour **les neuf mipmaps des trois DDS**. Décodage Pillow et comparaison pixel par pixel du niveau 256 px réussis, masques BGRA natifs et transparence des quatre coins vérifiés. La planche des DDS décodés a aussi été relue visuellement.

**Pas de test moteur revendiqué** : le jeu n'a pas été lancé pour cette demande. Le rendu en jeu reste à vérifier après rechargement ou redémarrage.
