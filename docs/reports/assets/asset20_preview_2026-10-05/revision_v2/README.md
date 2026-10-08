# Lot 17 — tableau noir pour l'Enseignement primaire

**Révision historique : remplacée par [revision_v3](../revision_v3/README.md) pour l'écriture à la craie. Aucune intégration et aucune approbation du lot déduite de la demande.**

Demande : « Pour renseignement primaire remplacé par un tableau noir. »

Seule l'icône d'Enseignement primaire est remplacée par un tableau noir mat dans un cadre de bois, sur des pieds reliés au cadre, avec une craie sur la tablette. La poignée, la feuille et les perles de l'abécédaire disparaissent. L'ancienne version et ses sources restent dans le dossier parent.

Les icônes Registres de population et Télégraphe optique sont réutilisées **sans retouche**, avec vérification exacte de leurs empreintes. Leur réutilisation ne vaut pas approbation de l'utilisateur.

## Livrables

- [Nouveau master du tableau noir](previews/organized_elementary_schooling_padded.png), 1574 × 1574 px.
- [Planche du lot mise à jour](LOT_17_APERCU.png), lecture 32/48/64 px.
- [Comparaison avec les technologies vanilla](LOT_17_COMPARAISON_VANILLA.png).
- [Alpha sur damier](LOT_17_ALPHA_DAMIER.png).
- [Prompt exact](PROMPT_TABLEAU_NOIR.md), générateur intégré **image_gen.imagegen**.
- [Provenance et empreintes](provenance.json), [contrôle technique](preview_validation.json), [examen visuel](visual_review.json).

Les seules opérations mécaniques après génération sont l'ajout de marges transparentes et le centrage ; les pixels RGBA originaux sont exactement conservés. Le tableau noir est du matériau sombre, pas un trou dans l'alpha. Le cadre est celui de l'objet, pas un cadre d'interface. Comparaison avec enseignement, archives et télégraphe électrique vanilla.

Le tableau noir est le symbole choisi par l'utilisateur ; aucune reconstitution exacte d'un tableau scolaire daté de 1776 n'est revendiquée. Les références historiques des deux autres sujets restent dans le dossier parent.

**1250 fichiers de common/gfx inchangés ; aucun DDS créé ; aucun changement de gameplay ; aucun test en jeu.**

Après validation seulement, export natif BGRA8 legacy A8R8G8B8 à 256 px et neuf mipmaps, puis décodage indépendant des couleurs et de l'alpha. Aucun fichier du jeu n'est modifié à cette étape.

