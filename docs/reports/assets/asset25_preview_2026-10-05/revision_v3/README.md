# Lot 22 — bouche du canon cachée

Statut : **trois icônes intégrées et vérifiées statiquement**, après approbation du joueur. [Contrôle de l’intégration](integration_static_validation.json), [planche décodée des DDS natifs](LOT_22_DDS_INTEGRES_QA.png), [approbation des masters exacts](user_approval.json). Le jeu n’a pas été relancé.

La bouche et toute la partie extérieure du canon sont supprimées. Le canon intérieur reste visible sur son affût, mais son extrémité est masquée par la maçonnerie. Les deux ouvertures secondaires sont conservées. Les deux autres icônes restent inchangées.

- [Aperçu corrigé](previews/casemated_fortifications_padded.png)
- [Planche du lot et miniatures 32 / 48 / 64 px](LOT_22_APERCU.png)
- [Transparence sur damier](LOT_22_ALPHA_DAMIER.png)
- [Comparaison vanilla](LOT_22_COMPARAISON_VANILLA.png)

Retouche avec **imagegen intégré**, un appel : [prompt exact](PROMPTS.md), [provenance](source_provenance.json). Les [versions antérieures](../revision_v2/README.md) restent conservées ; la révision 2 a été rejetée par le joueur pour le canon.

[Contrôle technique d’aperçu](preview_validation.json) : 1 265 fichiers protégés étaient inchangés avant intégration. Le contrôle final confirme seulement trois liens `texture` et trois nouveaux DDS 256 px / 9 mipmaps, sans modification de gameplay ; 1 264 autres fichiers protégés inchangés. [Revue visuelle](visual_review.json) : absence de bouche visible, maintien des ouvertures, couleurs naturelles et transparence contrôlés. Aucun lancement du jeu.

Après imagegen : copie, marges transparentes et réductions mécaniques uniquement, sans peinture ni modification de masque par script. Les pixels RGBA de la sortie brute sont conservés à l’identique par l’ajout de marges. [Références historiques déjà recueillies](historical_references.json), sans nouvelle affirmation historique pour cette suppression.
