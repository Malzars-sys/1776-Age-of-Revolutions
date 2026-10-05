# Lot 10 — technologies textiles

Date : 4 octobre 2026. **Les trois icônes ont été approuvées et intégrées.** Export et liaisons validés hors moteur ; aucun changement de gameplay.

| Technologie | Motif proposé |
|---|---|
| Production textile proto-industrielle | Navette en bois avec sa bobine, sur du lin ivoire plié |
| Filature mécanisée précoce | Machine à filer à quatre broches, rouleaux et courroie latérale |
| Tissage mécanique | Métier à châssis de fer, chaîne et tissu, roue d'entraînement latérale |

## Aperçus approuvés

- [Planche principale](LOT_10_APERCU.png), lectures à 32, 48 et 64 pixels.
- [Comparaison vanilla](LOT_10_COMPARAISON_VANILLA.png), sur fonds clair et sombre.
- [Transparence sur damier](LOT_10_ALPHA_DAMIER.png).

Les trois masters sélectionnés de 1574 × 1574 sont les fichiers *_padded.png de previews, identifiés par empreinte dans le [manifeste](preview_manifest.json). Sources générées non modifiées et versions non retenues également archivées. Réductions de 256 × 256 dans target_size_png.

## Références recherchées et examinées avant génération

Les photos ont été recherchées puis examinées dans le navigateur, sans téléchargement ni réutilisation dans les assets.

- [National Park Service — vocabulaire du tissage](https://www.nps.gov/articles/000/glossary-of-weaving-terms.htm) : forme d'une navette et position de sa bobine. Cette photo n'est pas utilisée pour dater cet objet précis.
- [Science Museum — machine à filer d'Arkwright](https://collection.sciencemuseumgroup.org.uk/objects/co8411373/arkwrights-water-frame) : machine à quatre broches vers 1775, à entraînement hydraulique. Une courroie et des poulies évoquent l'entraînement sans représenter une roue hydraulique entière. Une Jenny manuelle aurait contredit la description motorisée de la technologie.
- [Science Museum — modèle de métier mécanique](https://collection.sciencemuseumgroup.org.uk/objects/co44891/model-of-power-loom-with-double-shuttle-box-scale-1-2-power-loom) : modèle de 1815–1820, référence de formes et de matériaux. Ce n'est pas une reproduction revendiquée du premier métier de 1785. Socle d'exposition exclu.

[Sources archivées](historical_references.json). Assemblages simplifiés pour l'interface, ni copies exactes ni plans mécaniques validés.

## Génération et contrôles

Mode : **BUILTIN_IMAGE_GEN**. [Prompts initiaux](PROMPTS.md), [retouches des fils](REVISION_PROMPTS.md), [occultation des fils sur la filature](SPINNING_OCCLUSION_REVISION_PROMPT.md), [provenance des six générations](generation_results.json).

La navette conserve sa première génération. Le tissage retient sa deuxième, avec cadres de lisses pleine largeur successifs. La filature retient sa troisième : le rouleau supérieur occulte les fils, qui ne traversent plus sa face avant.

Seul traitement local : ajout de marges transparentes, centrage et réduction. Aucun pixel RGBA source modifié par le cadrage : [preuve](canvas_padding.json). Pas de peinture, recoloration, masque ni fond noir factice.

[Contrôles techniques](preview_validation.json) : alpha réel, coins transparents, format carré, sources ≥ 1024 pixels et réduction à 256 pixels. Les **1229 fichiers de common/ et gfx/** présents après l'intégration vapeur restent identiques pendant la préparation textile. [Revue visuelle](visual_review.json) : silhouette, ouvertures transparentes, couleurs naturelles, absence de texte et de cadre, comparaison vanilla. À 32 pixels, les silhouettes restent identifiables ; le trajet fin des fils n'est pas destiné à être lu à cette taille.

Les sept PM du laboratoire, la chaîne cuivre, les assets approuvés, les recettes, coûts et déblocages sont inchangés. Aucun test moteur effectué.

## Intégration effectuée

[Approbation du joueur](user_approval.json). Les trois masters approuvés sont exportés en DDS BGRA8 legacy A8R8G8B8, 256 × 256, neuf mipmaps. Seuls leurs trois champs texture ont été remplacés dans common/technology/technologies/10_tech3a_production.txt, aux lignes 277, 667 et 1229. Aucun coût, effet, parent ou déblocage modifié.

[Validation indépendante](integration_static_validation.json) : couleurs et alpha exacts dans les neuf niveaux, y compris le décodage par Pillow ; les 1228 autres fichiers protégés restent identiques. [Planche des DDS décodés](LOT_10_DDS_INTEGRES_QA.png) examinée visuellement sur fonds clair et sombre. [Manifeste d'intégration](integration_manifest.json). Les contrôles de preview_validation.json décrivent l'état avant intégration et sont conservés comme historique.

Aucun lancement du jeu effectué pour ce lot : le rendu moteur reste à vérifier.
