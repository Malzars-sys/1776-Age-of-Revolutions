# Lot 11 — technologies agricoles, version courante V2

Date : 4 octobre 2026. **Aperçus en attente de validation du joueur ; aucune intégration.** Retouches effectuées avec imagegen intégré (BUILTIN_IMAGE_GEN).

| Technologie | Motif courant |
|---|---|
| Élevage sélectif | Brebis et agneau ; master initial exactement inchangé |
| Drainage agricole | Drains en terre cuite et bêche, avec eau traversant le passage et coulant sur le bord avant |
| Irrigation mécanisée | Même pompe, avec jet relié à la grande conduite en laiton |

## Aperçus à valider

[Planche principale](LOT_11_APERCU.png) · [Comparaison vanilla](LOT_11_COMPARAISON_VANILLA.png) · [Transparence](LOT_11_ALPHA_DAMIER.png). Lectures réduites à 32, 48 et 64 pixels.

## Masters sélectionnés

- [Élevage inchangé](previews/selective_breeding_padded.png).
- [Drainage V2](water_revision_v2/previews/systematic_field_drainage_padded.png).
- [Irrigation V2](water_revision_v2/previews/mechanized_irrigation_padded.png).

Sources générées conservées sans retouche locale. Seuls centrage, marges transparentes et réductions sont réalisés par script. [Dossier détaillé V2](water_revision_v2/README.md), [prompts des deux éditions](water_revision_v2/REVISION_PROMPTS.md), [provenance V2](water_revision_v2/generation_results.json). Le générateur conserve le design des deux objets, sans garantir l'identité de chacun de leurs pixels. L'élevage est inchangé octet pour octet.

## Références et historique

Les mêmes références historiques du [dossier initial](historical_references.json) restent utilisées ; les retouches ne changent ni le modèle de drain ni celui de pompe. [Compte rendu initial et sources](water_revision_v2/initial_README.md), [prompts initiaux](PROMPTS.md), [provenance initiale](generation_results.json). Les planches et contrôles V1 sont archivés sous les noms initial_* dans water_revision_v2. Aucun master initial supprimé.

## Contrôles

[Contrôles techniques courants](preview_validation.json), [revue visuelle courante](visual_review.json), [manifeste sélectionné](preview_manifest.json). Masters de 1574 × 1574 et PNG réduits à 256 × 256, véritable alpha, eau lisible à 48/64 pixels, couleurs naturelles des objets sans teinte bleue globale. Eau réellement reliée aux sorties, pas un symbole de goutte détaché. À 32 pixels, ses détails restent petits.

Les **1232 fichiers de common/ et gfx/** présents au début du lot agricole restent identiques, y compris tous les assets textiles intégrés. Les sept PM du laboratoire, la chaîne cuivre et les assets précédemment approuvés restent protégés. Aucun DDS exporté, aucune définition modifiée, aucun test moteur.

## Après approbation seulement

Exporter uniquement les trois masters courants du [plan](generation_plan.json), en DDS BGRA8 legacy A8R8G8B8, 256 × 256 et neuf mipmaps. Vérifier indépendamment les couleurs et l'alpha puis changer seulement les trois textures de selective_breeding, systematic_field_drainage et mechanized_irrigation. Ne pas utiliser les variantes V1 de drainage ou d'irrigation.
