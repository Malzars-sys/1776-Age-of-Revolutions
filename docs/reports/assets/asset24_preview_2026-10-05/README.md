# Lot 21 — fortification et instruments militaires

Statut : **trois icônes approuvées, intégrées et validées statiquement** le 5 octobre 2026. La version « forteresse de Vauban » est retenue, pas le plan sur papier. Seules les trois références de texture ont changé ; les couleurs et l’alpha de chaque mipmap sont identiques aux sources approuvées.

[Contrôle des DDS intégrés](LOT_21_DDS_INTEGRES_QA.png) · [Rapport indépendant](integration_static_validation.json) · [Approbation exacte des sources](user_approval.json). Aucun lancement du jeu n’est revendiqué.

- Fortification et poliorcétique : forteresse bastionnée de Vauban, inspirée de Lille, en vue élevée de trois quarts. Elle remplace le plan sur papier à la demande de l’utilisateur.
- Normes d’armement : compas d’artilleur mesurant un boulet de fer.
- Topographie militaire : planchette sur trépied, munie d’une alidade.

## Aperçus

- [Les trois icônes, avec contrôle à 32 / 48 / 64 pixels](LOT_21_APERCU.png)
- [Transparence sur damier](LOT_21_ALPHA_DAMIER.png)
- [Comparaison avec trois références Vanilla](LOT_21_COMPARAISON_VANILLA.png)

## Sources et contrôles

Les trois images ont été créées avec l’outil intégré imagegen. Les [prompts exacts actuels](PROMPTS_VAUBAN_REVISION.md), les [références historiques](historical_references.json) et la [provenance des originaux](source_provenance.json) sont conservés. Le [plan initial](generation_plan_initial.json) et l’ancienne illustration sur papier sont archivés, non sélectionnés.

La forteresse est une interprétation simplifiée, pas une reconstitution archéologique exacte. Sa géométrie est guidée par la [description du Réseau des sites majeurs Vauban](https://sites-vauban.org/ressources/site-vauban/lille). Les références en ligne ont été recherchées avant génération ; aucune image distante n’a été téléchargée ni incorporée.

Seules des opérations mécaniques ont suivi la génération : copie, ajout de marges transparentes sans recadrage ni changement des pixels, réduction et planches de comparaison. Aucun recoloriage, aucune peinture ou modification de masque alpha.

[Contrôle technique](preview_validation.json) : les 1 262 fichiers de jeu protégés sont identiques à leur état après l’intégration des neuf icônes des lots 18–20. [Revue visuelle](visual_review.json) : fonds clairs/sombres et damier vérifiés, ainsi que la lisibilité réduite. Aucun test du moteur ou lancement du jeu n’est revendiqué.

Les sept anciens PM du laboratoire, les coûts, les déblocages, la chaîne du cuivre et les assets déjà validés sont inchangés. Les contrôles d’aperçu ci-dessus sont l’historique de préparation ; le rapport d’intégration confirme que les 1 261 autres fichiers de jeu protégés sont restés inchangés.

[Lot suivant : génie, évacuation et forts casematés](../asset25_preview_2026-10-05/README.md) — aperçus uniquement, approbation séparée nécessaire.

[Rapport de l’intégration précédente (neuf icônes)](../asset21_to23_preview_2026-10-05/integration_static_validation.json)
