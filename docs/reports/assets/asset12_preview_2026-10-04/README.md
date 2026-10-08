# Lot 9 — technologies de la vapeur

Date : 4 octobre 2026. **Archive de la première proposition, non intégrée.** La condensation est approuvée et conservée à l'identique ; les deux autres motifs ont été remplacés dans la [révision active](revision_2/README.md), désormais approuvée et intégrée. Les fichiers ci-dessous restent archivés et ne doivent pas servir à intégrer les deux motifs refusés. Les contrôles de cette archive décrivent uniquement son état initial ; consulter ceux de la révision 2 pour l'intégration actuelle.

| Technologie | Illustration initiale archivée |
|---|---|
| Vapeur à condensation | Cylindre et chambre de condensation séparée, reliés par une conduite |
| Vapeur rotative | Volant ouvert et transmission à deux engrenages ; deuxième version corrigée |
| Vapeur haute pression | Chaudière cylindrique robuste et petite soupape à levier |

## Aperçus

- [Planche principale](LOT_9_APERCU.png), avec lectures à 32, 48 et 64 pixels.
- [Comparaison aux trois technologies vanilla](LOT_9_COMPARAISON_VANILLA.png), sur fond clair et sombre.
- [Contrôle de transparence](LOT_9_ALPHA_DAMIER.png).

Les masters retenus sont les trois fichiers `previews/*_padded.png` de 1446 × 1446. L'ajout de marges et le centrage n'ont altéré aucun pixel RGBA original : voir [contrôle de cadrage](canvas_padding.json). Les PNG de 256 × 256 se trouvent dans `target_size_png/`. **Aucun DDS créé, aucune définition remplacée.**

## Références historiques

Les photos ont été recherchées puis examinées dans le navigateur, sans téléchargement ni réutilisation dans les assets.

- [Condenseur séparé de Watt — Science Museum](https://blog.sciencemuseum.org.uk/james-watt-and-the-separate-condenser/) : principe de séparation du cylindre chaud et de la chambre froide, brevet de 1769.
- [Deuxième modèle de Watt, 1765](https://collection.sciencemuseumgroup.org.uk/objects/co50928/watts-second-separate-condenser-1765-condensers) : ensemble cylindre–condenseur.
- [Modèle de transmission de Watt, 1782–1784](https://collection.sciencemuseumgroup.org.uk/objects/co51167) : engrenages et volant pour transformer le mouvement alternatif en rotation.
- [Machine et chaudière de Trevithick, 1805–1806](https://collection.sciencemuseumgroup.org.uk/objects/co51033/trevithicks-high-pressure-steam-engine-and-boiler-c-1806) : chaudière compacte en fer pour la haute pression.

Il s'agit d'interprétations illustrées simplifiées, pas de reproductions exactes ni de plans mécaniques validés. Les assemblages ont été simplifiés pour l'interface.

## Génération et contrôles

Création par l'outil imagegen intégré, une génération par sujet. [Prompts initiaux](PROMPTS.md), [retouche ciblée de la transmission](ROTATIVE_REVISION_PROMPT.md), [provenance](generation_results.json), [sources](historical_references.json), [contrôles techniques](preview_validation.json) et [revue visuelle](visual_review.json).

La première version rotative présentait une liaison ambiguë à la jante. Elle est conservée pour l'historique ; seule la deuxième version, avec marges ajoutées, est proposée. Les anciennes icônes des PM du laboratoire et tous les lots déjà approuvés restent inchangés.

Les empreintes des 1226 fichiers de `common/` et `gfx/` sont identiques à leur état avant ce lot. Les trois textures sont toujours provisoires dans les définitions. Pas de changement de gameplay, de recette, de prérequis ou de statistiques.

## Après validation seulement

**Suivre désormais le plan de la [révision active](revision_2/generation_plan.json), et non les deux anciens masters de rotation et de haute pression décrits ici.**

Exporter les trois masters sélectionnés en DDS **BGRA8 legacy A8R8G8B8**, 256 × 256, neuf mipmaps. Contrôler indépendamment le décodage, les couleurs natives et l'alpha. Ne modifier que les trois champs `texture` du fichier de technologies de production. Le rendu en jeu devra ensuite être vérifié après rechargement ; aucun test moteur n'est revendiqué ici.
