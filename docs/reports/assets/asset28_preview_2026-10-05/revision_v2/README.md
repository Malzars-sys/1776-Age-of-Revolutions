# Lot 25 — révision 2 : roue démontée pour réparation

Lot approuvé et intégré le 5 octobre 2026. La roue debout de la révision 1 est remplacée par une roue partiellement démontée, couchée sur le plateau : moyeu, rayons et morceaux de jante sont posés sur l'établi, sans le traverser. L'étau reste vide. L'établi équipé et son rangement d'outils conservent leur composition.

Outils agricoles et Papeterie traditionnelle sont conservés à l'identique. Seule l'icône Ateliers organisés a été retouchée avec **imagegen intégré**, à partir de la précédente illustration. La photographie fournie reste une référence de contexte conservée dans la révision 1 ; elle n'est pas une entrée de cette retouche. Aucune version antérieure n'a été supprimée.

[Lot complet](LOT_25_APERCU.png), [damier alpha](LOT_25_ALPHA_DAMIER.png), [comparaison vanilla](LOT_25_COMPARAISON_VANILLA.png), [icône corrigée](previews/organized_workshops_padded.png).

[Prompt exact](PROMPTS.md), [provenance](source_provenance.json), [revue visuelle](visual_review.json) et [validation technique](preview_validation.json). Contrôle à 32/48/64 px sur fonds clair et sombre ; à 32 px les petits éléments se confondent, la réparation se lit mieux à 48/64 px.

Les pixels de la sortie générée ont seulement reçu des marges transparentes et un recentrage mécanique, sans peinture, correction colorimétrique ni masquage alpha. Pendant la phase d'aperçu, les 1274 fichiers common/gfx protégés sont restés inchangés.

Après [accord du joueur](user_approval.json), trois DDS BGRA8 natifs 256 px / 9 mipmaps ont été exportés. Seules les trois lignes de texture correspondantes de `10_tech3a_production.txt` ont été remplacées ; les autres 1273 fichiers protégés, coûts, prérequis et effets sont inchangés. Le décodage indépendant vérifie tous les niveaux de couleur/alpha et l'identité avec les PNG réduits. [Validation d'intégration](integration_static_validation.json), [manifeste](integration_manifest.json), [planche DDS décodés](LOT_25_DDS_INTEGRES_QA.png). Aucun essai moteur revendiqué.

