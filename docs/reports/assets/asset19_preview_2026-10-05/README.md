# Lot 16 — forêt, transformation alimentaire et sucre

**État actuel : lot intégré et contrôlé statiquement, révision sélectionnée [revision_v2](revision_v2/README.md).** Les deux premières icônes sont conservées à l'identique ; le nouveau pain de sucre blanc et son moule remplacent la première proposition. Voir [ACTIVE_PREVIEW.json](ACTIVE_PREVIEW.json) pour les sources exactes et [le contrôle d'intégration](revision_v2/integration_static_validation.json). Les couleurs et la transparence des DDS décodés correspondent exactement aux PNG de contrôle. Aucun essai moteur n'est revendiqué.

Le contenu ci-dessous documente la première proposition, conservée comme historique.

Statut : **trois aperçus, non intégrés, en attente de validation de l'utilisateur**.

Le lot 15 précédent est intégré et contrôlé séparément dans [son dossier de validation](../asset18_preview_2026-10-05/revision_v3/integration_static_validation.json). Ce nouveau lot n'a exporté aucun DDS, ni modifié un fichier du jeu.

## Les trois propositions

- **Exploitation forestière organisée** (`organized_forestry`, ère 2) : scie à deux personnes et une hache secondaire. La coordination de l'exploitation est évoquée par les outils, sans forêt miniature.
- **Transformation alimentaire traditionnelle** (`traditional_food_processing`, ère 1) : meule manuelle à deux pierres ; poignée périphérique et alimentation centrale séparées.
- **Raffinage du sucre** (`sugar_refining`, ère 2) : moule conique dans son pot à mélasse, couche claire du procédé visible à l'intérieur. Pas de pain de sucre fini au premier plan.

Les trois emplacements utilisent actuellement le visuel de repli `gfx/error_manul.dds`. Leur gameplay reste intact. La chaîne cuivre et les sept PM originaux du laboratoire sont exclus.

## Références consultées avant génération

- [Colonial Williamsburg — Crosscut Saw](https://emuseum.colonialwilliamsburg.org/objects/56524/crosscut-saw) : scie datée de 1775–1800, en acier, fer et bois. Photo de la lame et des poignées examinée.
- [Cotswold Archaeology — Rotary Quern](https://cotswoldarchaeology.co.uk/museum/rotary-quern/) : structure d'une meule supérieure romaine, œil central et logement périphérique de poignée. Référence de principe ancien, pas datation de l'icône à 1776.
- [Barbara H. Magid / Chipstone — Sugar-Refining Pottery](https://chipstone.org/article.php/223/Ceramics-in-America-2005/Sugar-Refining-Pottery-from-Alexandria-and-Baltimore) : diagramme d'assemblage, pot de récupération et fragment de moule de la fin du XVIIIe siècle examinés.

Les appareils complets sont des interprétations conceptuelles historiquement informées, pas des reconstructions archéologiques certifiées. Les sources et les photos réellement examinées sont consignées dans [historical_references.json](historical_references.json).

## Génération et contrôles

Générateur d'images intégré : **image_gen.imagegen**. Un appel indépendant pour chacun des trois sujets, avec transparence demandée. Les [prompts exacts](PROMPTS.md), le [plan](generation_plan.json) et la [provenance avec empreintes](provenance.json) sont conservés.

Les originaux n'ont pas été supprimés. Seules des marges transparentes ont été ajoutées mécaniquement et les objets centrés, sans recadrage, retouche ou recoloration. Les pixels RGBA sont conservés exactement ; masters sélectionnés de **1574 × 1574**.

Comparaison avec trois technologies vanilla : outils mécaniques, agriculture intensive et conserve sous vide. Ces références servent au style uniquement, pas à dater les trois procédés.

- [Planche principale](LOT_16_APERCU.png), avec lecture à 32/48/64 px.
- [Comparaison vanilla](LOT_16_COMPARAISON_VANILLA.png), sur fonds clair et sombre.
- [Contrôle sur damier](LOT_16_ALPHA_DAMIER.png).
- [Contrôle technique](preview_validation.json) : **1247 fichiers de common/gfx inchangés**.
- [Examen visuel](visual_review.json).
- [Inspection de l'alpha](alpha_inspection.json) : transparence réelle extérieure, corps presque opaques, alpha original préservé.

**Aucun essai moteur n'est revendiqué.** Les PNG à 256 px sont uniquement des prévisualisations. Après validation, l'export utilisera le stockage natif BGRA8 legacy A8R8G8B8 et neuf mipmaps, avec comparaison des couleurs et de l'alpha après décodage indépendant ; seules les trois textures seront raccordées.

## Reproduire les contrôles

```text
tools/prepare_asset19_preview_references.py
tools/pad_asset12_preview_canvas.cjs --pack=docs/reports/assets/asset19_preview_2026-10-05
tools/build_asset12_preview_sheet.cjs --verify --pack=docs/reports/assets/asset19_preview_2026-10-05
tools/inspect_asset19_preview_alpha.py
```

Les scripts de préparation et de marges refusent d'écraser leurs résultats existants. Le contrôle de planche peut être relancé pour vérifier les PNG et les fichiers protégés.

