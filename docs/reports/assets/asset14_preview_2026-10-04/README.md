# Lot 11 — technologies agricoles intégrées

Date : 4 octobre 2026. Les trois icônes ont été approuvées par le joueur puis intégrées. Sources créées ou retouchées avec imagegen intégré (`BUILTIN_IMAGE_GEN`).

## Sources retenues

- [Élevage sélectif](previews/selective_breeding_padded.png), master initial.
- [Drainage agricole](water_revision_v2/previews/systematic_field_drainage_padded.png), version V2.
- [Irrigation mécanisée](water_revision_v4/previews/mechanized_irrigation_padded.png), version V4 : eau par la grande ouverture à gauche, petit tuyau en laiton sec.

## Intégration et vérification

[Planche décodée depuis les DDS](LOT_11_DDS_INTEGRES_QA.png) · [Validation indépendante](integration_static_validation.json) · [Manifeste](integration_manifest.json) · [Approbation exacte](user_approval.json).

Trois DDS BGRA8 legacy A8R8G8B8, 256 × 256 et neuf mipmaps. Tous les niveaux ont été décodés indépendamment : couleurs et alpha correspondent aux PNG approuvés. Seules les trois lignes texture de selective_breeding, systematic_field_drainage et mechanized_irrigation ont changé dans 10_tech3a_production.txt. Les 1231 autres fichiers protégés restent identiques. Aucun changement de gameplay, coût, déblocage ou PM.

Cette validation est statique, pas un essai moteur. Ne pas présenter le lot comme vérifié en partie sans observation après rechargement du jeu.

## Historique et prompts

[Prompt initial](PROMPTS.md) · [Retouches V2](water_revision_v2/REVISION_PROMPTS.md) · [Retouche retenue V4](water_revision_v4/REVISION_PROMPTS.md).

Les références et versions antérieures sont conservées : [références historiques](historical_references.json), [V4](water_revision_v4/README.md), [V3](water_revision_v3/README.md), [V2](water_revision_v2/README.md). L’ouverture d’écoulement de la V4 suit la demande du joueur ; cette illustration stylisée n’est pas un schéma du fonctionnement hydraulique historique.

Les sept anciennes icônes des PM du laboratoire, le cuivre et les autres assets précédemment approuvés restent inchangés.

