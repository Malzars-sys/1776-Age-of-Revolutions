# Lot 25 — outils et ateliers traditionnels

**Lot intégré : [révision 2](revision_v2/README.md), avec la roue démontée pour réparation sur l'établi.** Les trois masters du lot 25 ont été approuvés et intégrés le 5 octobre 2026. Outils agricoles et Papeterie traditionnelle sont conservées à l'identique. Le lot naval 24 est déjà intégré. Les images et descriptions ci-dessous documentent uniquement la proposition initiale, conservée comme historique.

- [Outils agricoles](previews/improved_agricultural_implements_padded.png) : charrue de type ancien bois/fer, deux manches, soc et versoir, sans semoir ni décor de champ.
- [Papeterie traditionnelle](previews/traditional_papermaking_padded.png) : cuve de pâte de chiffons et forme rectangulaire, feuille humide en formation et eau qui revient dans la cuve ; pas de pile de papier fini.
- [Ateliers organisés](previews/organized_workshops_padded.png) : établi artisanal avec presse en bois, pièce en cours de travail et un seul rabot ; pas de bâtiment ou d'atelier entier.

Les trois technologies sont actives, d'ère I, dans `10_tech3a_production.txt`. Leurs fichiers actuels sont les illustrations provisoires `preview_basileia_...` ; ils restent inchangés tant que ces nouvelles propositions ne sont pas approuvées. Le cuivre, les sept PM du laboratoire et les autres icônes validées sont exclus.

## Références consultées avant génération

Une recherche d'images précède les créations. La forme de la charrue s'appuie sur la [collection du Science Museum Group](https://collection.sciencemuseumgroup.org.uk/objects/co38812/early-english-rotherham-plough-1720-plows). Un [autre exemplaire](https://collection.sciencemuseumgroup.org.uk/objects/co38780/wooden-rotherham-plough-and-fragments) comporte des modifications après 1800, non retenues comme modèle du XVIIIe siècle.

Le procédé papetier est documenté avec des gravures de 1767 et une forme à papier dans l'[article de la Library of Congress](https://blogs.loc.gov/bibliomania/2024/12/05/papermaking-a-rags-to-riches-story/).

L'établi s'inspire des dessins de [Roubo dans L'Art du Menuisier](https://commons.wikimedia.org/wiki/File:Andr%C3%A9_Jacob_Roubo_Workbench.jpg), complétés par la [démonstration PBS](https://www.pbs.org/video/woodwrights-shop-french-work-bench-part-1/). Il symbolise un métier artisanal, pas tous les ateliers. Ces trois images sont des interprétations simplifiées, pas des répliques certifiées ou des représentations universelles pour chaque pays.

[Références historiques et limites](historical_references.json). Aucun visuel web téléchargé ou incorporé ; aucune image de référence envoyée au générateur.

## Création et contrôle

Trois générations originales séparées avec **imagegen intégré**, vrai alpha transparent. [Prompts exacts](PROMPTS.md) et [sources/empreintes](source_provenance.json) conservés. Masters bruts 1254 px, masters centrés 1542 px : uniquement ajout de marges transparentes et réductions, sans retouche des pixels générés.

[Planche principale](LOT_25_APERCU.png), [damier](LOT_25_ALPHA_DAMIER.png), [comparaison avec trois technologies vanilla](LOT_25_COMPARAISON_VANILLA.png) inspectées, avec miniatures 32/48/64 px et fonds clair/sombre. À 32 px, les petits détails du soc, du grillage et des gouttes se simplifient ; la lecture est meilleure à 48/64 px. [Revue visuelle](visual_review.json).

[Validation technique](preview_validation.json) réussie : 1274 fichiers gameplay/gfx inchangés pendant la création de ce lot, aucun DDS exporté, aucune texture reliée au jeu. L'export futur sera BGRA8 natif 256 px / 9 mipmaps, seulement après accord séparé. Aucun essai moteur ni approbation du joueur revendiqués.
