# Lot 6 — technologies politiques

Date : 4 octobre 2026. Statut : **trois icônes validées par le joueur, intégrées et contrôlées sur fichiers ; rendu en jeu encore à vérifier**.

## Intégration terminée

Accord du joueur : « Donc tu peux tout intégrer. » Les trois masters sélectionnés sont exportés en **DDS BGRA8 legacy natif, 256 × 256, neuf mipmaps**, avec transparence conservée. La relecture indépendante de chaque niveau de mipmap confirme les couleurs et l'alpha ; les PNG décodés sont identiques aux réductions des masters approuvés.

Seules les trois lignes `texture` de Régime constitutionnel, Souveraineté populaire et Mouvements réformistes ont changé dans `common/technology/technologies/30_tech3a_society.txt`. Aucun parent, effet, déblocage, loi, PM ou recette n'a été changé par cette intégration. Les autres **1 216 fichiers** déjà présents dans `common` et `gfx` sont identiques à l'état avant intégration ; seuls les trois nouveaux DDS attendus ont été ajoutés. Les modifications antérieures du joueur sont conservées.

- [Planche des DDS intégrés, décodés indépendamment](LOT_6_DDS_INTEGRES_QA.png).
- [Accord sur les masters exacts](user_approval.json).
- [Manifeste d'intégration](integration_manifest.json) et [contrôle indépendant](integration_static_validation.json).

Aucun essai moteur n'est revendiqué. Redémarrer le jeu avec le mod activé pour vérifier les trois icônes dans l'arbre Société. Les sections d'aperçu ci-dessous restent l'historique de conception ; leurs anciennes mentions d'attente ne décrivent plus le statut actuel.

## Sélection actuelle — demande du joueur

- Régime constitutionnel : couronne posée sur un livre fermé, sans parchemin ni sceau — validé par le joueur.
- Souveraineté populaire : cocarde ajoutée au bonnet phrygien ; **hampe conservée**, conformément à la dernière précision du joueur — validé par le joueur.
- Mouvements réformistes : ancienne pétition écartée ; tribune d'orateur en bois validée et intégrée.

[Tribune et prompt actuel](tribune_preview/README.md), [planche complète actuelle](complete_preview/LOT_6_APERCU.png) et [accord du joueur sur les deux premières icônes](user_revision_v2/user_approval.json). Le plan `generation_plan.json` contient les trois chemins sélectionnés. Les anciennes planches et les rapports ci-dessous restent l'historique de la première proposition, pas un lot autorisé à intégrer.

## Règle des PM enregistrée

La règle figure déjà dans le [cahier des charges, Couleurs des PM](../ASSET4_CAHIER_DES_CHARGES_ET_LOT_1_2026-10-01.md) : pictogrammes schématiques beige/ocre, grain fin mat, haut plus clair et bas plus sombre, sans relief, extrusion, biseau ni ombre portée. Les sept anciennes icônes des PM du laboratoire sont une exception expressément conservée par le joueur.

Ce lot ne contient que des technologies : le style peint et volumétrique de cette famille est conservé. Il ne reprend pas la règle graphique plate des PM.

## Trois propositions initiales — historique, remplacé par la sélection ci-dessus

| Technologie | Sujet | État actuel |
|---|---|---|
| Régime constitutionnel | Charte claire, couronne secondaire et sceau | Icône provisoire `gfx/error_manul.dds` |
| Souveraineté populaire | Bonnet de liberté rouge sur une courte hampe | Icône provisoire `gfx/error_manul.dds` |
| Mouvements réformistes | Pétition partiellement déroulée et plume taillée | Icône provisoire `gfx/error_manul.dds` |

- [Planche des trois aperçus avec formats 32 / 48 / 64 pixels](LOT_6_APERCU.png)
- [Comparaison avec Démocratie, Académie et Agitation politique vanilla](LOT_6_COMPARAISON_VANILLA.png)
- [Transparence sur damier](LOT_6_ALPHA_DAMIER.png)

La technologie Constitution libérale garde son icône vanilla actuelle ; aucun parent de technologie ni déblocage de loi n'a été changé.

## Références historiques recherchées avant génération

Les sujets sont des **adaptations conceptuelles originales**, pas des copies exactes de documents historiques.

- Le support en parchemin est informé par la [Constitution de 1787, National Archives](https://www.archives.gov/milestone-documents/constitution). La couronne ajoutée symbolise les limites écrites au pouvoir royal ; elle n'appartient pas à ce document américain.
- Le bonnet reprend une silhouette de bonnet de liberté attestée par un [objet de 1793 au musée historique de Strasbourg, photographié sur Commons](https://commons.wikimedia.org/wiki/File:Bonnet_phrygien_d'une_section_du_club_des_Jacobins_%C3%A0_Strasbourg_(1793).jpg). L'objet photographié est en tôle peinte ; notre image est une variante conceptuelle textile, pas une réplique.
- La forme du document roulé est éclairée par le [Reform Act de 1832 conservé par le Parlement britannique](https://www.parliament.uk/about/living-heritage/transformingsociety/electionsvoting/chartists/case-study/the-right-to-vote/thomas-attwood-and-the-birmingham-political-union/1832-reform-act/1832-reform-act-1/). Cet acte est une loi, non une pétition. Une [pétition de réforme de 1837 présentée par la LSE Library](https://www.lse.ac.uk/library/whats-on/online-exhibitions/the-power-to-vote/history-of-general-elections-the-1800s) documente séparément le sujet de mobilisation collective. Ces références postérieures au début du mod ne sont pas présentées comme des objets de 1776.

Les recherches d'images précèdent les créations. Les images distantes restent des références de recherche, sans téléchargement ou copie dans les fichiers du jeu. Les trois références de style vanilla sont décodées depuis l'installation locale et conservées dans `references/`.

## Génération et retouche

Mode : **imagegen intégré (BUILTIN_IMAGE_GEN)**. Trois générations distinctes, puis une retouche ciblée de la pétition : le premier rendu avait un embout métallique ; il a été remplacé par une pointe taillée dans la hampe de la plume. La variante initiale est conservée dans `variants/`.

- [Prompts complets de génération](generation_requests.json)
- [Prompt de la retouche ciblée](targeted_revision.json)
- [Résultats et chemins des originaux](generation_results.json)
- [Plan des futures liaisons](generation_plan.json)
- [Références historiques](historical_references.json) et [références vanilla](native_references.json)
- `previews/` : trois masters PNG sélectionnés.
- `target_size_png/` : réductions à 256 pixels, non installées dans le jeu.

Aucune retouche artistique manuelle : seules des copies, des réductions et des planches de comparaison suivent les créations imagegen.

## Contrôles et suite

Les trois masters de 1 254 × 1 254 pixels et leurs réductions ont un canal alpha réel et quatre coins transparents. Les silhouettes complètes, leurs couleurs et leur lecture réduite ont été inspectées. Les marques d'encre évoquent des manuscrits sans texte destiné à être lu. Le rendu reste plus détaillé que certains exemples vanilla ; l'adéquation artistique reste à valider par le joueur.

Les empreintes de **1 217 fichiers** de `common` et `gfx` sont identiques à celles relevées avant ce lot. Aucun nouveau DDS ni changement de gameplay, des PM intégrés ou du laboratoire.

[Contrôle technique](preview_validation.json) et [relecture visuelle](visual_review.json). Aucun test de ces images en jeu n'est revendiqué.

Attendre l'accord du joueur avant intégration. L'export ultérieur devra utiliser le stockage natif BGRA8 et contrôler indépendamment couleurs, alpha et neuf mipmaps, puis vérifier le rendu en jeu.
