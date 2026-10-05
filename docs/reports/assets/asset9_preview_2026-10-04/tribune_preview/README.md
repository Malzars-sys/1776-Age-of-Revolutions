# Mouvements réformistes — tribune en bois

Date : 4 octobre 2026. Mode : **imagegen intégré**, génération distincte du nouveau concept. Statut : **validée par le joueur et intégrée, contrôles sur fichiers réussis, pas encore testée en jeu**. [Bilan d'intégration](../README.md).

[Master PNG](organized_reform_movements.png) : une tribune d'orateur en bois patiné, plateau de lecture incliné et petit marchepied intégré. Aucun personnage, inscription, livre, emblème, décor ou microphone. Peinture volumétrique de technologie, distincte des pictogrammes plats des PM.

[Prompt complet et recherches visuelles préalables](generation_request.json), [provenance et empreinte du fichier](generation_result.json).

Le master de 1 254 × 1 254 pixels et sa [réduction à 256 px](../complete_preview/target_size_png/organized_reform_movements.png) ont une transparence alpha réelle et quatre coins entièrement transparents. La silhouette et la lecture à 48/64 px ont été inspectées sur fonds sombre et clair, puis comparées à trois icônes vanilla. C'est une adaptation conceptuelle originale, pas une réplique d'un mobilier historique précisément identifié. Les images de recherche ne sont pas téléchargées ni copiées dans le jeu.

- [Aperçu complet avec miniatures](../complete_preview/LOT_6_APERCU.png).
- [Comparaison avec les technologies vanilla](../complete_preview/LOT_6_COMPARAISON_VANILLA.png).
- [Transparence sur damier](../complete_preview/LOT_6_ALPHA_DAMIER.png).
- [Contrôle technique](../complete_preview/preview_validation.json) et [relecture visuelle](visual_review.json).

Les deux premières icônes ont été validées par le joueur ; leurs masters restent identiques à leurs empreintes approuvées. Les contrôles décrits ci-dessus concernent la préparation en aperçu. L'intégration effectuée ensuite ajoute trois DDS natifs et remplace exactement trois liens de texture ; les **1 216 autres fichiers de `common` et `gfx` sont inchangés**. Aucun changement du laboratoire, des lois ou des effets/parents de l'arbre technologique ; aucun essai en jeu revendiqué.

Accord du joueur enregistré dans [user_approval.json](../user_approval.json). L'export BGRA8 natif, l'alpha, les couleurs et les neuf mipmaps passent le [contrôle indépendant](../integration_static_validation.json). Il reste la vérification du rendu en jeu après redémarrage.
