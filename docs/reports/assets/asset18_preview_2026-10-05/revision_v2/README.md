# Lot 15 — révision 2

**Version suivante : [révision 3](../revision_v3/README.md), approuvée et intégrée.** Elle corrige uniquement les têtes de vis ; les deux autres images de ce dossier ont été intégrées sans modification. Cette révision 2 reste conservée comme historique.

Statut : **trois aperçus révisés, non intégrés**. Validation utilisateur requise avant toute conversion DDS ou liaison aux technologies. Retouches réalisées avec l'outil intégré **imagegen** ; aucun changement de gameplay.

## Modifications demandées

- **Pièces interchangeables** : deux vis identiques et deux roues crantées assorties. Le calibre est retiré pour conserver un groupe compact et lisible ; les pièces restent standardisées par paire.
- **Verre pressé** : gobelet de premier plan retiré. Presse, moule, poinçon aligné et verre chaud à l'intérieur conservés.
- **Blanchiment papetier industriel** : paquet de feuilles de premier plan retiré. Cuve, pâte claire, agitateur et supports conservés ; paroi et pied auparavant masqués reconstitués.

Il s'agit de technologies : appareil ou groupe conceptuel isolé, sans reprendre la composition des bâtiments avec un produit fini au premier plan. Les versions originales restent dans le dossier parent comme historique, pas comme aperçu actif.

## Vérifications

Les trois planches ont été examinées : `LOT_15_APERCU.png`, `LOT_15_COMPARAISON_VANILLA.png`, `LOT_15_ALPHA_DAMIER.png`. Comparaison avec trois technologies natives ; lecture à 32/48/64 px sur fonds clair/sombre. Matières naturelles, pas de dominante bleue ; appareils et contours détachés sur damier. Les détails fins sont secondaires à la silhouette.

`preview_validation.json` : PASS_TECHNICAL_PREVIEW_CHECKS. Les **1244 fichiers common/gfx sont inchangés** ; aucun DDS du lot 15 n'a été exporté. Aucun test en jeu revendiqué.

## Sources

Sources imagegen brutes 1254 × 1254 et maîtres à marges transparentes 1574 × 1574 dans `previews/`, réductions 256 px dans `target_size_png/`. `canvas_padding.json` vérifie que l'ajout de marges ne change aucun pixel source. Les seules retouches artistiques proviennent d'imagegen, aucune recoloration ou suppression locale par script.

`generation_results.json` conserve les cibles d'édition, leurs empreintes, les copies et emplacements imagegen originaux. `PROMPTS_V2.md` et `generation_plan.json` contiennent les consignes exactes. Les originaux imagegen sont conservés. Références historiques : `historical_references_v2.json` et `../historical_references.json` ; engrenages conceptuels, pas une réplique de musée. `visual_review.json` détaille les contrôles.

