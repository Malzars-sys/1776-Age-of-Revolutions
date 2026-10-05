# Lot 11 — retouches eau, version 2

**Aperçus seulement, en attente de validation du joueur.** Les deux fichiers générés sont édités avec imagegen intégré (BUILTIN_IMAGE_GEN). Aucune intégration, aucun changement de gameplay.

- Drainage agricole : eau dans le fond de l'ouverture, s'écoulant au-dessus du bord de la semelle.
- Irrigation mécanisée : jet continu relié à l'extrémité ouverte de la grande conduite en laiton, puis retombant à côté de la pompe.
- Élevage sélectif : master précédent conservé à l'identique, empreinte contrôlée.

[Planche courante](LOT_11_APERCU.png) · [Transparence](LOT_11_ALPHA_DAMIER.png) · [Comparaison vanilla](LOT_11_COMPARAISON_VANILLA.png).

## Fichiers sélectionnés

- [Drainage avec eau](previews/systematic_field_drainage_padded.png).
- [Irrigation avec eau](previews/mechanized_irrigation_padded.png).
- [Élevage inchangé](previews/selective_breeding_padded.png).

Les deux nouvelles images sources sont archivées sans modification à côté des fichiers cadrés. [Prompts exacts](REVISION_PROMPTS.md), [provenance](generation_results.json), [plan](generation_plan.json), [empreintes](preview_manifest.json). Les références historiques restent celles du [dossier original](../historical_references.json) : aucun nouveau modèle de machine ajouté.

## Contrôles

[Revue visuelle](visual_review.json) : origines des deux écoulements cohérentes ; eau localisée, terre cuite/bois/métal dans leurs couleurs naturelles ; fond et ouvertures réellement transparents. Planche examinée à 32, 48 et 64 pixels sur fonds clair et sombre. À 48/64 pixels l'écoulement reste un repère lisible ; à 32 pixels il ne faut pas chercher à lire les fines rides ou gouttes.

[Contrôles techniques](preview_validation.json) : masters carrés 1574 × 1574, coins transparents, alpha conservé. Vérification des bords des sources : aucun pixel alpha ≥ 16 sur les quatre dernières bordures. Une trace alpha 1 sur la bordure droite de l'irrigation est invisible ; les gouttes ne sont pas coupées. Marges transparentes ajoutées sans toucher aux pixels RGBA : [preuve](canvas_padding.json). Aucune peinture ni modification artistique par script.

Les **1232 fichiers de common/ et gfx/** présents dans la référence du lot initial sont inchangés. Les sept PM du laboratoire, les assets déjà intégrés et la chaîne cuivre sont protégés. Aucun DDS exporté, aucune liaison remplacée, aucun test moteur.

Les nouvelles peintures conservent l'assemblage et les matériaux, mais une retouche générative ne garantit pas l'identité pixel à pixel des deux objets retouchés. L'élevage, lui, est exactement identique. Toutes les versions initiales sont conservées dans le dossier parent.

