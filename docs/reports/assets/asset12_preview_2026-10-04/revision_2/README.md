# Lot 9 — deux motifs révisés, condensation conservée

Date : 4 octobre 2026. **Les trois icônes sont approuvées, intégrées et vérifiées hors jeu.** Le joueur a demandé : « Ok, intègre tout et passe au prochain lot. » Aucun essai moteur n'est revendiqué.

| Technologie | Proposition active | Validation |
|---|---|---|
| Vapeur à condensation | Cylindre et condenseur de la proposition précédente, fichier conservé à l'identique | Approuvé par le joueur |
| Vapeur rotative | Régulateur centrifuge de type Watt à deux boules | Approuvé et intégré |
| Vapeur haute pression | Soupape de sécurité isolée, à levier et contrepoids cylindrique, sans chaudière | Approuvé et intégré |

## Fichiers sélectionnés

- Condensation : [master conservé](../previews/condensing_steam_engines_padded.png).
- Rotation : [nouveau master](previews/rotative_steam_power_padded.png).
- Haute pression : [nouveau master](previews/high_pressure_steam_padded.png).
- [Planche de validation](LOT_9_APERCU.png), [comparaison vanilla](LOT_9_COMPARAISON_VANILLA.png), [alpha sur damier](LOT_9_ALPHA_DAMIER.png).
- Masters de 1446 × 1446 ; copies de lecture de 256 × 256 dans `target_size_png/`.

Les aperçus précédents restent archivés dans le dossier parent. Seul le présent [plan](generation_plan.json) définit les masters approuvés utilisés pour cette intégration.

## Références examinées avant génération

Le [moteur rotatif Boulton & Watt de 1788](https://collection.sciencemuseumgroup.org.uk/objects/co50948/rotative-steam-engine-by-boulton-and-watt-1788-beam-engine-steam-engine) documente l'emploi du régulateur centrifuge. La [photographie d'un régulateur Boulton & Watt](https://commons.wikimedia.org/wiki/File:Boulton_and_Watt_centrifugal_governor-MJ.jpg) a servi à examiner la forme des boules et des articulations.

Le [moteur haute pression de Trevithick construit en 1811](https://collection.sciencemuseumgroup.org.uk/objects/co50985/trevithicks-patent-1802-high-pressure-steam-engine-constructed-1811-for-threshing-purposes-at-trewithen-in-use-till-1879) possède dans son inventaire un piston et un poids de soupape de sécurité à levier, référence 1879-57/8. Cette référence inspire le nouveau motif. Le musée signale de possibles pièces remplacées : l'illustration ne revendique pas une reconstitution exacte datée de 1811.

Les photos ont été consultées dans le navigateur, sans téléchargement ni réutilisation dans les assets. [Sources archivées](historical_references.json).

## Génération et contrôles

Deux nouvelles générations originales par **imagegen intégré**, fond transparent. La condensation n'a pas été régénérée. [Prompts complets](PROMPTS.md), [provenance](generation_results.json), [contrôle des marges](canvas_padding.json), [contrôles techniques](preview_validation.json) et [revue visuelle](visual_review.json).

Des marges transparentes ont été ajoutées aux deux nouveaux masters, sans peinture, masque, recadrage ni changement de couleur. Tous les pixels RGBA générés ont été préservés exactement. L'empreinte du fichier de condensation est toujours `a336c9fc58e1456aa65bf14b3934146b0ef20da8a23a9d2deaaa3f33dbdf2424`.

Lecture contrôlée à 32, 48 et 64 pixels, sur fond clair et sombre. Comparaison aux icônes vanilla du moteur atmosphérique, du moteur à soupapes et de la chaudière tubulaire. Transparence contrôlée autour des objets et entre les pièces. Assemblages volontairement simplifiés ; ce ne sont pas des plans techniques validés.

Sur les **1226 fichiers de common/ et gfx/** présents avant le lot, 1225 restent identiques. Seules trois lignes de texture de `10_tech3a_production.txt` changent. Trois nouveaux DDS s'ajoutent ; aucun paramètre de jeu ne change. Les sept anciens PM du laboratoire sont inchangés. Aucun test moteur effectué.

## Intégration réalisée après approbation

Les trois masters sélectionnés ont été exportés en DDS BGRA8 legacy A8R8G8B8, 256 × 256, neuf mipmaps. Le contrôle indépendant de chaque niveau confirme les couleurs et l'alpha exacts des PNG de référence. Les deux propositions refusées du dossier parent ne sont pas intégrées. Le rendu moteur reste à vérifier après rechargement du jeu.

[Approbation et empreintes](user_approval.json), [manifeste d'intégration](integration_manifest.json), [contrôle indépendant](integration_static_validation.json), [planche des DDS décodés](LOT_9_DDS_INTEGRES_QA.png).
