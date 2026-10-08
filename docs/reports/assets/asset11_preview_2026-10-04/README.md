# Lot 8 — technologies navales

Statut : **lot intégré depuis la révision 2**. Les drapeaux approuvés ont été conservés ; les deux anciennes coques de ce dossier n'ont pas été intégrées.

La [révision 2](revision_2/README.md) contient les sources approuvées, l'accord du joueur et les vérifications d'intégration. Cette première version et les sections de préparation ci-dessous restent archivées pour la traçabilité.

## Les trois icônes

- **Signaux navals** : trois pavillons de communication suspendus à une drisse.
- **Charpente diagonale** : section de coque en bois avec renforts diagonaux.
- **Coques en fer** : coque métallique rivetée avec couples visibles.

[Planche des aperçus](LOT_8_APERCU.png) · [Comparaison vanilla](LOT_8_COMPARAISON_VANILLA.png) · [Transparence sur damier](LOT_8_ALPHA_DAMIER.png)

## Règles appliquées

Création avec l'outil imagegen intégré (`BUILTIN_IMAGE_GEN`), après recherche d'images réelles sur Internet et lecture des références historiques. Les trois références **technologie** vanilla inspectées sont Amirauté, Frégate et Sidérurgie. Les nouvelles icônes sont des objets peints en volume, pas des pictogrammes PM.

Masters générés : PNG carrés de 1254 px avec alpha réel. Aperçus sélectionnés : 1446 px après ajout et centrage sur une toile transparente. Aucune peinture, suppression de pixels, recoloration ou retouche artistique : les pixels RGBA des originaux sont conservés exactement. Les versions brutes et les originaux de génération restent disponibles.

Le cuivre, les anciennes icônes PM du laboratoire, les assets déjà approuvés, les localisations et les paramètres de jeu restent hors de ce lot.

## Sources et génération

- [Prompts exacts envoyés](generation_requests.json)
- [Références historiques et images trouvées](historical_references.json)
- [Références vanilla décodées](native_references.json)
- [Origines des images générées](generation_results.json)
- [Traçabilité du cadrage transparent](canvas_padding.json)
- [Plan et futurs chemins DDS](generation_plan.json)

Sources principales : [vocabulaire marin de Popham, 1803](https://www.rmg.co.uk/collections/objects/rmgc-object-522377), [modèle SLR2908 et principe amélioré vers 1814](https://www.rmg.co.uk/collections/objects/rmgc-object-68863), [construction originale du Vulcan, 1818–1819](https://culturenl.co.uk/the-vulcan/).

Les pavillons ne transcrivent pas un message historique précis. Les sections de coque sont des illustrations conceptuelles simplifiées, pas des reconstructions techniques complètes. La photographie du Vulcan moderne sert uniquement de repère de forme : la réplique en acier de 1988 n'est pas présentée comme un artefact original de 1819.

## Vérifications

[Contrôle technique](preview_validation.json) · [Relecture visuelle](visual_review.json)

- Trois sujets comparés à trois références vanilla sur fonds clair et sombre.
- Lecture contrôlée à 48/64 px, avec aperçu complémentaire à 32 px.
- Alpha vérifié aux quatre coins, entre les pavillons et dans les ouvertures des structures.
- **1223 fichiers de common et gfx inchangés** par rapport à l'état de départ de ce lot.
- Aucun export DDS, aucune liaison de texture modifiée ; **pas de test moteur revendiqué**.

Après accord du joueur, les futurs exports seront des DDS 256 × 256, neuf mipmaps, au stockage natif **BGRA8 legacy A8R8G8B8**. Une validation de décodage et de couleurs sera nécessaire avant de déclarer l'intégration terminée.
