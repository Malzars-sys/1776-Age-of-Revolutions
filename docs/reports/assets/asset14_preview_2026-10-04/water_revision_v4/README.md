# Irrigation V4 — écoulement par la grande ouverture

Mode : imagegen intégré (`BUILTIN_IMAGE_GEN`), édition de la V3. Aperçu en attente de validation, non intégré.

L’eau sort maintenant de l’intérieur de la grande ouverture circulaire à gauche. Le petit tuyau en laiton reste sec. Le design de la pompe est conservé, mais une édition générative ne garantit pas l’identité des pixels. L’élevage et le drainage V2 sont conservés octet pour octet.

[Master sélectionné](previews/mechanized_irrigation_padded.png) · [Source brute](previews/mechanized_irrigation.png) · [Aperçus](LOT_11_APERCU.png) · [Comparaison vanilla](LOT_11_COMPARAISON_VANILLA.png) · [Alpha sur damier](LOT_11_ALPHA_DAMIER.png).

[Prompt exact](REVISION_PROMPTS.md) · [Provenance](generation_results.json) · [Validation technique](preview_validation.json) · [Revue visuelle](visual_review.json) · [Preuve de padding sans altération des pixels](canvas_padding.json).

Master : 1446 × 1446 ; source : 1254 × 1254 ; réductions à 256 pixels. Fond réellement transparent ; contrôle sur fonds clair/sombre et à 48/64 pixels. Aucun détourage ni recoloration locale. La trace d’alpha au bord de la source est de 1/255 au maximum, sans coupure visible.

Cette représentation suit l’ouverture demandée par le joueur ; elle n’est pas un schéma validant le fonctionnement hydraulique exact de la pompe historique. Les [références historiques](../historical_references.json) et les versions V1–V3 restent conservées.

Les 1232 fichiers protégés de common/ et gfx/ sont inchangés. Aucun DDS, aucune modification de gameplay, aucun essai moteur. Intégration uniquement après approbation.
