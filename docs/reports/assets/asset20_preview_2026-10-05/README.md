# Lot 17 — enseignement, registres et télégraphe optique

**Trois icônes approuvées et intégrées le 5 octobre 2026. Vérification statique réussie ; aucun essai en jeu revendiqué.**

**Révision active : [revision_v3](revision_v3/README.md).** Le tableau noir de l'Enseignement primaire porte « 2 + 2 », puis « = 4 » décalé en dessous, à la demande de l'utilisateur ; le registre et le télégraphe sont conservés exactement. Sources sélectionnées dans [ACTIVE_PREVIEW.json](ACTIVE_PREVIEW.json). Le contenu ci-dessous conserve l'historique de la première proposition.

Le lot 16 est intégré et contrôlé dans [son rapport](../asset19_preview_2026-10-05/revision_v2/integration_static_validation.json). Ce lot 17 est maintenant intégré : trois liens de texture et trois nouveaux DDS natifs, sans changement de gameplay. [Contrôle d'intégration](revision_v3/integration_static_validation.json).

## Première proposition (historique)

- **Enseignement primaire** (`organized_elementary_schooling`, ère 3) : abécédaire en bois de type hornbook, feuille protégée et petit cordon de perles de comptage.
- **Registres de population** (`systematic_population_registration`, ère 3) : registre relié ouvert avec entrées répétées, une seule plume.
- **Télégraphe optique** (`optical_telegraph_networks`, ère 4) : mécanisme Chappe isolé, un régulateur central et deux indicateurs articulés à ses extrémités. Pas de tour miniature.

Les trois technologies utilisent encore `gfx/error_manul.dds`. Recettes, déblocages, coûts, bonus et noms du jeu sont inchangés. La chaîne cuivre et les sept anciennes icônes de PM du laboratoire restent exclues.

## Références et limites historiques

- [NYPL — Hornbook du XVIIIe siècle](https://www.nypl.org/events/exhibitions/galleries/childhood/item/5461) : photo examinée, forme de palette en bois et feuille protégée.
- [Library of Congress Magazine, janvier/février 2021, p. 7 imprimée](https://www.loc.gov/lcm/pdf/LCM_2021_0102.pdf) : texte et légende consultés pour l'utilisation de perles de comptage ; photo non accessible à l'inspection, position du cordon adaptée conceptuellement.
- [Archives municipales d'Aubervilliers](https://archives.aubervilliers.fr/Registres-paroissiaux) : existence de registres de baptêmes, mariages et sépultures d'octobre 1774 à août 1776 vérifiée. Registre générique, pas reproduction de sa reliure ou de sa mise en page.
- [Musée des Arts et Métiers — Télégraphe Chappe](https://www.arts-et-metiers.net/musee/modele-telegraphe-optique-systeme-chappe) : photo du modèle vers 1815 examinée pour les trois bras et leurs articulations. Invention présentée en 1792. L'appareil en bois compact est une interprétation du principe ; le modèle du musée est en laiton/marbre/fer.

Aucune photographie de musée ou d'archives n'est incorporée aux créations. Illustrations originales générées, pas reconstructions certifiées. Le détail des accès et des limites figure dans [historical_references.json](historical_references.json).

## Aperçus et contrôles

- [Planche principale](LOT_17_APERCU.png), lecture à 32/48/64 px.
- [Comparaison avec trois technologies vanilla](LOT_17_COMPARAISON_VANILLA.png) : enseignement, archives et télégraphe électrique, références de style uniquement.
- [Alpha sur damier](LOT_17_ALPHA_DAMIER.png).
- [Aperçus individuels](previews/), masters sélectionnés de 1574 × 1574 px.
- [Prompts exacts](PROMPTS.md), backend intégré **image_gen.imagegen**, un appel indépendant par sujet.
- [Provenance](provenance.json), [ajout de marges](canvas_padding.json), [contrôle technique](preview_validation.json), [examen visuel](visual_review.json).

Seules des marges transparentes et un centrage mécanique ont été ajoutés, sans masque, retouche, recoloration ni recadrage. Les pixels RGBA originaux sont exactement conservés. Les PNG à 256 px servent au contrôle seulement.

**1250 fichiers de common/gfx inchangés ; aucun DDS créé ; aucun test moteur revendiqué.**

Les silhouettes restent distinctes à 48/64 px. Les détails des cordes, de l'écriture et des barreaux ne sont pas censés rester lisibles à cette taille. Le télégraphe est particulièrement fin à 32 px sur fond sombre : ce point reste soumis à la validation visuelle de l'utilisateur.

L'intégration future, uniquement après approbation, utilisera le format natif BGRA8 legacy A8R8G8B8, 256 px et neuf mipmaps, avec décodage indépendant des couleurs/alpha. Seules les trois textures seront raccordées.

## Reproduire

Préparation des références : `tools/prepare_asset20_preview_references.py`.
Vérification des aperçus : `tools/build_asset12_preview_sheet.cjs --verify --pack=docs/reports/assets/asset20_preview_2026-10-05`.
Inspection sans retouche de l'alpha : `tools/inspect_asset20_preview_alpha.py`.

La préparation et le padding refusent d'écraser les originaux. Le contrôle d'aperçus reste valable tant que ce lot n'est pas intégré ; sa référence des fichiers protégés décrit précisément l'étape de prévisualisation.

