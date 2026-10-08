# Génie routier — icône intégrée

Statut : **validé par le joueur et intégré le 6 octobre 2026**. Création commencée le 5 octobre ; export et contrôle indépendant terminés le 6 octobre. Aucun essai moteur revendiqué.

Le joueur a rejeté le simple patch de route pavée. Cette nouvelle composition met en avant un **niveau en bois à fil à plomb**, accompagné d'une **coupe de chaussée en couches** : elle doit évoquer le nivellement et la construction de fondations durables.

## Aperçus et fichiers

- [Planche principale](LOT_27_APERCU.png) : grande vue et lecture réduite sur deux fonds.
- [Comparaison aux technologies vanilla](LOT_27_COMPARAISON_VANILLA.png) : Outils mécaniques, Travail de l'acier et Académisme.
- [Contrôle de transparence](LOT_27_ALPHA_DAMIER.png).
- [Master original généré](previews/improved_road_engineering.png).
- [Master cadré approuvé](previews/improved_road_engineering_padded.png).
- [PNG à la taille cible 256 px](target_size_png/improved_road_engineering.png).
- [Consigne complète et provenance de génération](generation_plan.json).
- [Validation technique](preview_validation.json) et [preuve du cadrage sans retouche](canvas_padding.json).
- [Accord utilisateur](user_approval.json), [validation indépendante du DDS intégré](integration_static_validation.json) et [planche du DDS décodé](GENIE_ROUTIER_DDS_INTEGRE_QA.png).

La génération a utilisé l'outil imagegen intégré, avec fond réellement transparent. La consigne complète est conservée dans `entries[0].prompt` du plan. Aucun service/API de génération alternatif n'a été utilisé.

Le cadrage ajoute uniquement une marge transparente et recentre le sujet : les pixels RGBA de l'image source sont conservés exactement. Pas de recoloration, de masque refait ni de retouche par script.

Master brut SHA-256 : `533b150c8593f2f4e985c270152e729031d379461f27c54e0b0b17b78a45a1c9`.

Master cadré SHA-256 : `f8a98fd8f4f4b9c871b0e10dedaf2fd97a372873828184d82aad47fafe884c6f`.

## Sources consultées avant création

La composition est une interprétation artistique, **pas la reproduction exacte d'un instrument ou d'une chaussée datée**.

Les fondations en pierres, le profil bombé et le rôle du drainage sont documentés dans la recherche d'Anne Conchon, [Road construction in Eighteenth Century France](https://www.arct.cam.ac.uk/system/files/documents/vol-1-791-798-conchon.pdf), notamment la section Building Techniques.

Le principe du niveau en A avec un fil à plomb est décrit par le [Science Museum Group](https://collection.sciencemuseumgroup.org.uk/objects/co53142), dans sa présentation des instruments de nivellement. Ne pas confondre cette source sur le principe ancien avec une attribution précise de notre modèle en bois au XVIIIe siècle.

Une recherche d'images a aussi examiné le [niveau en A de Denton](https://collection.sciencemuseumgroup.org.uk/objects/co53227/dentons-a-frame-canal-level-by-w-and-s-jones-a-frame-level), daté 1840–1860 : utilisé seulement comme aide de compréhension de la forme, pas comme preuve de datation du concept du mod. Aucune photo trouvée sur Internet n'a été copiée dans l'asset.

## Contrôles et intégration

- Master cadré carré : 1542 × 1542.
- Coins transparents ; ouvertures du cadre transparentes ; contrôle sur damier et deux fonds.
- Lisibilité examinée à 32, 48 et 64 px et comparaison visuelle avec trois technologies natives.
- 1276 fichiers `common` et `gfx` de la référence d'intégration sont inchangés ; seule la ligne `texture` de Génie routier a changé, et un nouveau DDS a été ajouté. La logique du fichier est inchangée.
- Le DDS 256 × 256 est exporté en BGRA8 natif A8R8G8B8, avec neuf mipmaps. Toutes leurs couleurs et leur alpha concordent avec l'export approuvé, sans permutation rouge/bleu.
- La technologie référence désormais `gfx/interface/icons/invention_icons/1776_improved_road_engineering.dds`. Aucun lancement du jeu pendant cette intégration.
- Les anciens aperçus restent conservés comme historique et ne doivent plus être repris comme proposition actuelle.

L'[audit des biens et bâtiments](../goods_building_icon_audit_2026-10-06/README.md) a trouvé un dernier placeholder hors cuivre : Machines de précision.
