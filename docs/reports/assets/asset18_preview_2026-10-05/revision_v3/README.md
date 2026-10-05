# Lot 15 — révision 3 : perspective des vis

Statut : **trois icônes approuvées et intégrées le 5 octobre 2026**. Correction artistique réalisée avec l'outil intégré imagegen ; consigne exacte dans `PROMPT_V3.md`. L'approbation exacte et les empreintes sont conservées dans `user_approval.json`.

Intégration : trois DDS BGRA8 legacy A8R8G8B8, 256 × 256 et neuf mipmaps. `integration_static_validation.json` confirme les couleurs et l'alpha de toutes les mipmaps, les trois liaisons aux technologies et l'absence de changement de gameplay. Seules trois lignes `texture` sont modifiées ; 1243 autres fichiers common/gfx sont inchangés. `LOT_15_DDS_INTEGRES_QA.png` a été inspectée après décodage indépendant. Aucun test en jeu revendiqué. Les paragraphes de préparation ci-dessous restent l'historique de l'aperçu avant approbation.

Les deux vis pointent vers le spectateur : les fentes de tournevis sont donc sur les faces opposées, cachées. L'illustration montre maintenant le dessous des têtes entourant les tiges, sans fente visible. La composition reste composée de deux vis et deux roues crantées assorties.

**Verre pressé et Blanchiment papetier industriel sont repris de la révision 2 sans retouche ni nouvelle génération.** Leurs empreintes sont contrôlées ; cela ne vaut pas approbation utilisateur. Les versions précédentes restent conservées.

Planches inspectées : `LOT_15_APERCU.png`, `LOT_15_COMPARAISON_VANILLA.png`, `LOT_15_ALPHA_DAMIER.png`. Lecture 32/48/64 px, trois références de technologies vanilla, fonds clair/sombre et damier. Pas de dominante bleue, fentes invisibles aux deux têtes ; silhouette compacte et contours non coupés.

`preview_validation.json` confirme **1244 fichiers common/gfx inchangés**, coins transparents et aucun DDS du lot 15 exporté. Pas de test en jeu. Approbation requise avant intégration.

Sources : `previews/interchangeable_manufacture_v3.png` (1254²) et maître à marges transparentes `previews/interchangeable_manufacture_padded.png` (1574²). `canvas_padding.json` prouve la conservation exacte des pixels lors de l'ajout mécanique de marges ; les modifications artistiques viennent uniquement d'imagegen. Copies, cibles d'édition, chemins natifs et empreintes : `generation_results.json`. Références historiques inchangées : `../revision_v2/historical_references_v2.json`.

