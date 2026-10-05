# Lot 24 — architecture, inspection et sécurité navales

**Version approuvée et intégrée : [révision 2](revision_v2/README.md), avec un plan naval et deux gilets en liège près du canot.** La classification est conservée à l'identique. Les descriptions et images ci-dessous documentent uniquement la version initiale, remplacée et conservée comme historique. [Contrôles d'intégration](revision_v2/integration_static_validation.json) réussis, sans essai moteur.

**Historique de la proposition initiale, non intégrée sous cette forme.** La révision 2 ci-dessus est la version active intégrée. Aucun essai moteur n'est revendiqué.

## Trois sujets

- [Architecture navale](previews/scientific_naval_architecture_padded.png) : maquette de coque en coupe et compas de dessin. Remplace le réemploi actuel du voilier vapeur `screw_frigate.dds`.
- [Classification navale](previews/ship_classification_surveying_padded.png) : registre ouvert, profil de navire, grille d'inspection et compas d'épaisseur. Remplace la bourse de pièces `power_of_the_purse.dds`.
- [Sécurité maritime](previews/maritime_safety_standards_padded.png) : canot à deux extrémités relevées, bordure de liège et deux rames rangées. Remplace la carte de navigation `navigation.dds`.

Les trois technologies sont actives dans `25_tech3a_naval.txt`, respectivement ères II, III et VI. Aucune autre proposition antérieure pour ces identifiants n'a été trouvée dans les plans de génération.

## Références historiques

Les maquettes navales de conception sont documentées par [Royal Museums Greenwich](https://www.rmg.co.uk/collections/our-collection-worlds-largest-ship-model-collection). La composition est une interprétation simplifiée, pas un modèle certifié d'un navire précis.

[Lloyd's Register](https://www.lr.org/en/about-us/who-we-are/our-history/) documente son registre annuel commencé en 1764 et l'inspection/classement des navires. Le dessin de bateau et le compas d'épaisseur sont des symboles pour l'icône, pas des éléments attestés de sa couverture originale. Aucun logo, faux texte ou sceau officiel n'est copié.

Le [modèle Greathead de Greenwich, vers 1790](https://www.rmg.co.uk/collections/objects/rmgc-object-66523) documente une coque à deux extrémités, des bordés à clin et du liège intérieur/extérieur. Deux rames sont représentées pour la lisibilité, pas l'armement complet d'un canot en service. La [RNLI](https://rnli.org/about-us/our-history/timeline/1785-the-first-lifeboats) complète le contexte. Pas de bouée plastique moderne ou de gilet de 1854.

[Sources et choix d'interprétation complets](historical_references.json).

## Création et vérification

Génération avec **imagegen intégré**, une image par appel. Les sources PNG originales, leurs chemins et leurs empreintes sont conservés dans [source_provenance.json](source_provenance.json). [Prompts exacts](PROMPTS.md). Aucun visuel web n'est copié au mod ni envoyé comme cible d'édition.

Masters 1542 × 1542 avec véritable alpha. Seules des marges transparentes et un recentrage mécanique ont été ajoutés aux PNG générés, sans toucher leurs pixels ni leurs couleurs. Les PNG réduits 256 px sont dans [target_size_png](target_size_png).

[Planche d'aperçu](LOT_24_APERCU.png), [damier alpha](LOT_24_ALPHA_DAMIER.png), [comparaison avec trois technologies vanilla](LOT_24_COMPARAISON_VANILLA.png) : inspectées visuellement à 32/48/64 px sur fonds clair et sombre. [Revue et limites](visual_review.json).

[Contrôle technique](preview_validation.json) : 1271 fichiers gameplay/gfx inchangés depuis la préparation de ce lot, aucun nouveau DDS exporté, aucun lien de technologie changé. Les détails internes se simplifient à 32 px ; les formes principales restent distinctes. L'icône de maquette montre un modèle complet plutôt que le fragment de charpente diagonale déjà approuvé.

Le cuivre, les sept anciens PM du laboratoire et tous les visuels déjà approuvés restent hors périmètre. Les recettes, statistiques, coûts et déblocages ne sont pas modifiés. Export prévu seulement après accord séparé : DDS BGRA8 natif, 256 × 256 et neuf mipmaps.
