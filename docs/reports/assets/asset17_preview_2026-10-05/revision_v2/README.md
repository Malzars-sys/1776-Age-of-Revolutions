# Lot 14 — révision 2

Trois icônes **validées par l'utilisateur et intégrées le 5 octobre 2026**. Les deux corrections utilisent imagegen intégré ; la lampe de Sécurité minière est conservée à l'identique.

- **Mines profondes** : coupe de roche, puits vertical, galeries étagées sur deux niveaux, seau descendant profondément. Le petit treuil de surface n'est plus le sujet principal.
- **Soufflage à chaud** : chambre métallique portée au rouge-orange ; rivets, foyer, conduits connectés et cheminée conservés. Incandescence du métal, pas seulement du charbon.
- **Sécurité minière** : même PNG que la première proposition, empreinte vérifiée.

## Aperçus et sources

`LOT_14_APERCU.png` présente la proposition active et les lectures 32/48/64 px. `LOT_14_COMPARAISON_VANILLA.png` compare trois références natives de technologies. `LOT_14_ALPHA_DAMIER.png` contrôle le détourage.

Maîtres révisés : `previews/deep_mine_engineering_padded.png` et `previews/hot_blast_smelting_padded.png`, 1574 × 1574 après marges transparentes. Sources imagegen brutes 1254 × 1254 conservées en fichiers frères `*_v2.png`. Aucun pixel source recolorié ou effacé localement.

Prompts exacts et rôles des images : `PROMPTS_V2.md`, `generation_plan.json`. Provenance et empreintes : `generation_results.json`. Référence historique de coupe minière inspectée : `historical_references_v2.json`.

Les premières propositions et leurs rapports restent dans le dossier parent ; elles ne sont pas les images actives de cette révision. Le plan initial demandait trois niveaux de galeries ; la génération en montre deux plus un fond de puits plus bas. Ce résultat est présenté sans revendiquer trois niveaux.

## Vérification et limites

`preview_validation.json` conserve la preuve avant intégration : 1241 fichiers common/gfx inchangés. `user_approval.json` identifie les trois maîtres approuvés par leur empreinte.

`integration_static_validation.json` : trois DDS BGRA8 natifs, 256 × 256, neuf niveaux de mipmaps, couleurs et alpha identiques aux PNG convertis. Seules trois lignes de texture ont changé ; les 1240 autres fichiers protégés restent inchangés. `LOT_14_DDS_INTEGRES_QA.png` a été inspectée après décodage indépendant.

`visual_review.json` : les trois planches ont été inspectées. Profondeur et incandescence lisibles à 48/64 px. Couleurs naturelles, sans dominante bleue. Illustration conceptuelle, pas une reconstitution technique ni un thermomètre.

Aucun essai moteur, aucun changement de gameplay, de recettes ou de déblocages. Les propositions initiales rejetées restent archivées ; seules les images de cette révision approuvée ont été intégrées.
