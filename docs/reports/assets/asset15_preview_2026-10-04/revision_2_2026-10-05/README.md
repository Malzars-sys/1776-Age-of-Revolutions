# Lot 12 — Révision du 5 octobre 2026

**Aperçus uniquement : aucune intégration.** Deux icônes sont corrigées avec l'outil imagegen intégré :

- **Céramique industrielle** : trois pots assortis de même forme et un moule commun ouvert en deux parties. Le moule remplace la cassette de cuisson ; la répétition des pots exprime la production en série.
- **Alcalis industriels** : la chambre du four rejoint le conduit de cheminée. Une petite coupe à droite rend le passage ascendant visible, sans changer le reste du sujet.
- **Acides industriels** : master inchangé, empreinte vérifiée.

La règle TECH conserve une illustration peinte en volume, les couleurs naturelles et l'alpha transparent. La demande explicite de plusieurs pots est traitée comme un groupe homogène dominant, avec un seul moule comme accessoire. Les règles des PM ne sont pas appliquées à ces technologies.

![Lot 12 révisé](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/LOT_12_APERCU.png)

## Images retenues

- [Céramique industrielle — master transparent](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/previews/industrial_ceramics_padded.png)
- [Alcalis industriels — master transparent](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/previews/industrial_alkalis_padded.png)
- [Acides industriels — master conservé](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/previews/industrial_acids_padded.png)

[Comparaison vanilla](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/LOT_12_COMPARAISON_VANILLA.png) · [Alpha sur damier](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/LOT_12_ALPHA_DAMIER.png)

## Prompts et provenance

Mode : **outil imagegen intégré**, deux éditions indépendantes. Chaque master local a été inspecté avant édition. Les originaux générés restent à leur chemin par défaut ; leurs copies sont enregistrées dans ce dossier. Les anciennes versions ne sont ni supprimées ni retouchées.

[Prompts exacts](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/REVISION_PROMPTS.md) · [Chemins et historique de génération](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/generation_results.json) · [Références consultées](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/historical_references.json)

Le contexte du moulage est documenté par le [V&A](https://www.vam.ac.uk/articles/a-z-of-ceramics) et le [récit de Simeon Shaw consacré aux Potteries](https://www.thepotteries.org/shaw/006a.htm). L'image reste une interprétation visuelle, sans date précise ni copie d'un moule identifié. La coupe du conduit n'est pas un plan d'ingénierie certifié. Les résultats commerciaux de la recherche d'images n'ont pas été utilisés comme preuve historique.

## Contrôles

Trois masters carrés de 1574 × 1574 avec vraie transparence, lecture en 32/48/64 px, et comparaison avec trois textures natives. L'ajout de marges transparentes et le centrage ne modifient aucun pixel RGBA source. Les 1235 fichiers de common/gfx sont identiques au début de cette révision. Aucun changement de gameplay, coût, déblocage ou PM ; aucun DDS exporté.

[Validation technique](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/preview_validation.json) · [Revue visuelle](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/visual_review.json) · [Centrage sans retouche](C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/assets/asset15_preview_2026-10-04/revision_2_2026-10-05/canvas_padding.json)

Le rendu en jeu n'a pas été testé. Après approbation, exporter ces mêmes masters en DDS BGRA8 natif et contrôler leur décodage avant essai moteur.

## Intégration approuvée — 5 octobre 2026

Les trois masters de la révision 2 ont été approuvés par le joueur et intégrés. Acides inchangés ; alcalis avec conduit de cheminée continu ; céramique avec trois pots identiques et leur moule. Voir ../integration_static_validation.json et ../LOT_12_DDS_INTEGRES_QA.png.

DDS natifs BGRA8 256 × 256, neuf mipmaps : couleurs et alpha identiques aux PNG de réduction, trois liens texture seulement, 1 234 autres fichiers protégés inchangés. Pas de test en jeu revendiqué. Les mentions d’attente de validation ci-dessus décrivent l’étape de prévisualisation antérieure ; cette intégration est désormais approuvée.

