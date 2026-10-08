# Lot 24 — révision 2 : plan naval et gilets

**Trois icônes approuvées et intégrées le 5 octobre 2026.** Architecture navale utilise le plan technique et Sécurité maritime le canot avec les deux gilets ; Classification navale reste exactement identique au master validé.

- [Architecture navale](previews/scientific_naval_architecture_padded.png) : remplacement complet de la maquette par une feuille de plan technique, avec profil de coque, demi-largeur et sections transversales ; compas conservé comme instrument.
- [Sécurité maritime](previews/maritime_safety_standards_padded.png) : canot à liège et deux rames, plus deux gilets en toile et liège, un peu superposés.
- [Classification navale conservée](../previews/ship_classification_surveying_padded.png).

## Sources historiques et limites

Le [plan du Sphinx daté de 1773, Royal Museums Greenwich](https://www.rmg.co.uk/collections/objects/rmgc-object-83708), documente les trois familles de vues techniques. Le dessin de l'icône est générique et simplifié, pas une copie exacte ou un plan constructible.

Les gilets s'inspirent des équipements en liège et toile introduits en 1854 pour les équipages de sauvetage par Ward, documentés par [la RNLI](https://rnli.org/about-us/our-history/timeline/1854-first-lifejackets). Ils sont bien du XIXe siècle, mais ne sont pas attribués à 1776 ou à l'apparition des premiers canots Greathead. C'est un montage conceptuel des progrès du secours maritime, pas une scène précisément datée. Aucun changement d'ère, de gameplay ou de déblocage n'a été fait.

## Création et contrôles

Deux éditions avec **imagegen intégré**, à partir des deux masters locaux inspectés. Aucun visuel web envoyé à l'outil. La génération conserve la composition du canot et du compas mais peut redessiner légèrement les objets ; aucune identité pixel par pixel avec l'image d'entrée n'est revendiquée. Les anciennes versions restent conservées.

[Prompts exacts](PROMPTS.md), [provenance et empreintes des sources](source_provenance.json), [références historiques](historical_references.json). Masters 1542 × 1542, vrai alpha. Post-traitement limité aux marges transparentes/recentrage mécanique et aux réductions, sans retouche des pixels générés.

[Lot complet](LOT_24_APERCU.png), [transparence](LOT_24_ALPHA_DAMIER.png), [comparaison vanilla](LOT_24_COMPARAISON_VANILLA.png) : trois planches inspectées à 32/48/64 px sur fonds clair/sombre. Les lignes du plan et les attaches de gilet se simplifient à 32 px. [Revue visuelle](visual_review.json).

[Validation des aperçus avant intégration](preview_validation.json) : 1271 fichiers gameplay/gfx étaient inchangés. Après [approbation explicite](user_approval.json), trois DDS natifs BGRA8 256 px / 9 mipmaps sont reliés au jeu par exactement trois lignes de texture dans `25_tech3a_naval.txt`. [Validation indépendante](integration_static_validation.json) : couleurs et alpha identiques aux PNG réduits à tous les niveaux, aucun changement de gameplay, 1270 autres fichiers protégés inchangés. [Planche des DDS décodés](LOT_24_DDS_INTEGRES_QA.png) inspectée. Les anciennes variantes, les autres icônes et les sept PM du laboratoire restent conservés. Jeu non relancé ; contrôle moteur non revendiqué.
