# Lot 11 — technologies agricoles

Date : 4 octobre 2026. **Trois aperçus créés avec imagegen intégré ; validation du joueur requise avant intégration.** Aucun DDS créé et aucune définition du jeu modifiée pour ce lot.

| Technologie | Motif proposé |
|---|---|
| Élevage sélectif | Brebis à longue laine et son agneau |
| Drainage agricole | Deux drains en terre cuite sur leurs semelles, avec une bêche |
| Irrigation mécanisée | Bélier hydraulique, chambre d'air sphérique et conduites distinctes |

## Aperçus à valider

- [Planche principale](LOT_11_APERCU.png), avec lectures à 32, 48 et 64 pixels.
- [Comparaison avec trois technologies vanilla](LOT_11_COMPARAISON_VANILLA.png), sur fonds clair et sombre.
- [Transparence sur damier](LOT_11_ALPHA_DAMIER.png).

Masters sélectionnés de 1574 × 1574 dans previews/*_padded.png ; les fichiers sources générés non modifiés sont conservés à côté. [Empreintes des masters](preview_manifest.json). Réductions à 256 × 256 dans target_size_png.

## Références examinées avant génération

Les photos et dessins externes ont été consultés sans téléchargement, copie dans les assets ni transmission au générateur. Seules leurs caractéristiques sont décrites dans les prompts.

- [Rare Breeds Survival Trust — Leicester Longwool](https://www.rbst.org.uk/watchlist-breed/leicester-longwool/) : photographie réellement examinée, laine longue et claire, face pâle, absence de cornes. La sélection de Leicester par Bakewell au XVIIIe siècle motive ce choix. La [société de la race](https://www.llsba.co.uk/longwool.php) avertit que l'animal actuel diffère de l'ancien : l'icône est une évocation, pas une reconstitution exacte du troupeau de Bakewell. L'agneau exprime la transmission des caractères sans ajouter un symbole abstrait.
- [York Archaeological Trust — guide des matériaux céramiques, section 5.5](https://research.yorkarchaeology.co.uk/wp-content/uploads/2023/08/AGuidetoCeramicBuildingMaterials-JMMcComish.pdf) : texte consulté sur les drains agricoles en fer à cheval et leurs semelles séparées, employés à partir de la fin du XVIIIe siècle. L'affichage de la planche du PDF n'a pas fonctionné ; il n'est pas présenté comme une image examinée. La [photographie de drains anciens chez Jetstream](https://www.trustjetstream.com/history-of-drain-tile) a été réellement examinée pour la forme de la section, sans reprendre la datation de cet exemple américain plus tardif.
- [Science Museum Group — bélier hydraulique, modèle Montgolfier](https://collection.sciencemuseumgroup.org.uk/objects/co61409/easton-hydraulic-ram-montgolfier-pattern) : dessin réellement examiné, dont la légende porte « Hydraulic Ram, c.1822 ». Chambre sphérique, arrivée horizontale, soupape de décharge et conduite de refoulement distinctes. Ni couleur bleue de coupe, ni texte, ni mesures ne sont copiés.
- [Catalogue du musée du CNAM, section C](https://cnum.cnam.fr/pgi/redir.php?ident=M6770&onglet=c) : texte consulté sur le premier bélier automatique français de Montgolfier en 1796. Le [traité de Borgnis, 1819](https://cnum.cnam.fr/pgi/redir.php?ident=4DY4.4&onglet=c) précise le réservoir d'air, les soupapes et les matériaux ; ses planches non accessibles ne sont pas revendiquées comme examinées.

Le bélier est un exemple de relevage mécanique de l'eau, pas l'affirmation que la technologie et son parent Vapeur rotative décrivent uniquement cet appareil. La pompe centrifuge Appold de 1851 a été écartée pour retenir un exemple plus ancien. [Dossier des références et limites](historical_references.json).

## Génération et contrôles

Mode : **BUILTIN_IMAGE_GEN**. [Prompts exacts des trois créations](PROMPTS.md), [provenance des fichiers](generation_results.json). Chaque sujet a sa propre génération ; les images sources sont conservées.

Seul traitement local : ajout de marges transparentes, centrage et réduction. Aucun pixel RGBA de la source modifié lors du cadrage : [preuve](canvas_padding.json). Aucune recoloration, peinture, extraction de fond ou création d'ombre par script.

[Contrôles techniques](preview_validation.json) : alpha réel, coins transparents, carré ≥ 1024 pixels, réduction à 256 pixels. Les **1232 fichiers de common/ et gfx/** présents après l'intégration textile sont restés identiques. [Revue visuelle](visual_review.json) : trois silhouettes distinctes, matières naturelles, pas de teinte bleue, texte ou cadre intégré ; comparaison avec enclosure, intensive_agriculture et mechanical_tools du jeu installé.

À 48 et 64 pixels, le mouton avec l'agneau, le drain avec la bêche et la pompe restent identifiables. À 32 pixels, les joints, détails de laine et pièces de soupape ne sont pas destinés à être lus. Illustrations simplifiées, non plans mécaniques certifiés.

Les sept PM du laboratoire, la chaîne cuivre et tous les assets déjà approuvés sont protégés. Aucun gameplay, coût, parent ou déblocage modifié. Aucun test moteur effectué.

## Après approbation seulement

Exporter les trois masters sélectionnés en DDS BGRA8 legacy A8R8G8B8, 256 × 256, neuf mipmaps. Contrôler indépendamment couleurs et alpha de chaque niveau et décoder les exports. Remplacer uniquement les trois champs texture des identifiants selective_breeding, systematic_field_drainage et mechanized_irrigation dans common/technology/technologies/10_tech3a_production.txt. [Plan et destinations](generation_plan.json).
