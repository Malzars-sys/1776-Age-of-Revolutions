# Lot 12 — Chimie et céramique : aperçus à valider

Les trois icônes de technologie sont créées. **Ce lot n'est pas intégré** : aucun DDS n'est exporté et les trois technologies conservent leur texture actuelle. Le lot agricole 11 approuvé est déjà intégré séparément.

## Aperçus

![Trois aperçus et contrôles en petites tailles](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/LOT_12_APERCU.png)

- [Acides industriels — master transparent](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/previews/industrial_acids_padded.png) : chambre en plomb simplifiée et petit flacon.
- [Alcalis industriels — master transparent V2](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/previews/industrial_alkalis_padded.png) : four stationnaire Leblanc et plateau de soude.
- [Céramique industrielle — master transparent](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/previews/industrial_ceramics_padded.png) : cassette de cuisson réfractaire et bol blanc.

[Comparaison avec le vanilla](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/LOT_12_COMPARAISON_VANILLA.png) · [Contrôle sur damier](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/LOT_12_ALPHA_DAMIER.png)

## Méthode et références

Mode : **outil imagegen intégré**. Trois créations originales sans image d'entrée, puis une édition du four avec son master initial comme seule image d'entrée. La V1 rectangulaire avait un halo brun ; elle est conservée et non retenue. La V2 le retire et fournit une découpe transparente.

Les règles TECH influencent la composition : appareils volumétriques peints, matériaux naturels, pas de dominante bleue, ni scène ou encadrement. Les règles des pictogrammes PM ne sont pas appliquées à ces technologies. Les anciens PM de laboratoire restent intacts.

Les références ont été recherchées sur internet avant génération. Les illustrations d'appareils dans [Acids, Alkalis and Salts, G. H. J. Adlam](https://www.gutenberg.org/files/50552/50552-h/50552-h.htm) et la [photographie d'un saggar du British Museum](https://commons.wikimedia.org/wiki/File:Stoneware_saggar_from_a_kiln,_British_Museum.jpg) ont été examinées dans le navigateur. [London Museum](https://www.londonmuseum.org.uk/collections/v/object-282673/kiln-furniture-saggar/) et [V&A](https://www.vam.ac.uk/articles/ceramics-a-risky-business) fournissent le contexte de la cuisson protégée.

La chambre ancienne est représentée sans les tours plus tardives de la gravure. Le four est stationnaire, sans mécanisme rotatif ni équipement Solvay. Le saggar est une technique plus ancienne ; l'image symbolise la maîtrise de la cuisson, pas son invention à l'ère 3. Ces compositions sont des interprétations pour une icône, non des reconstitutions certifiées. Aucune image internet n'est téléchargée ou réutilisée dans le mod.

- [Prompts exacts des trois créations](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/PROMPTS.md)
- [Prompt exact de correction du four](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/ALKALIS_REVISION_PROMPT.md)
- [Provenance, chemins des originaux et copies](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/generation_results.json)
- [Détail des références et limites historiques](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/historical_references.json)

## Contrôles

Les trois masters retenus sont carrés, 1574 × 1574, avec un alpha réel. L'ajout de marges transparentes et le centrage ne changent aucun pixel RGBA source. Les miniatures sont contrôlées sur fonds clair et sombre en 32, 48 et 64 px, avec trois références vanilla de même famille.

Les **1235 fichiers common/gfx** présents après l'intégration du lot 11 restent identiques. Aucun changement de gameplay, coût ou prérequis. Aucun test en jeu n'est revendiqué.

[Validation technique](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/preview_validation.json) · [Revue visuelle](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/visual_review.json) · [Marges sans retouche](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/canvas_padding.json)

Après approbation seulement : exporter ces mêmes masters en DDS 256 × 256, neuf mipmaps, format natif BGRA8/A8R8G8B8, puis remplacer uniquement les trois références de texture. Vérifier indépendamment les couleurs et l'alpha décodés avant contrôle en jeu.

