# Lot 15 — fabrication et standardisation

**Version active : [révision 3](revision_v3/README.md), approuvée et intégrée.** Perspective des têtes de vis corrigée : faces fendues cachées. Les deux autres icônes viennent de la révision 2, sans gobelet ni feuilles séparés au premier plan. Trois DDS natifs et trois liaisons de texture vérifiés ; aucun changement de gameplay ni test moteur revendiqué. `ACTIVE_PREVIEW.json` désigne cette version. Les planches et descriptions ci-dessous sont conservées comme historique de la première proposition.

Statut : **trois aperçus prêts, non intégrés**. Validation utilisateur requise avant conversion DDS et liaison aux technologies. Mode de création : **BUILTIN_IMAGE_GEN**, fond réellement transparent.

Le lot 14 révisé a été intégré auparavant : `../asset17_preview_2026-10-05/revision_v2/integration_static_validation.json`. Cette nouvelle passe ne le modifie pas.

## Trois propositions

- **Pièces interchangeables** : trois vis identiques et un calibre fixe de contrôle, répétition plutôt qu'un assortiment de pièces.
- **Verre pressé** : presse manuelle, moule et poinçon alignés, un gobelet cannelé correspondant.
- **Blanchiment papetier industriel** : cuve avec agitateur, pâte pâle, petit paquet de feuilles blanches comme résultat.

## Contrôle visuel

`LOT_15_APERCU.png` : grandes vues et lectures 32/48/64 px sur fond clair et sombre.
`LOT_15_COMPARAISON_VANILLA.png` : trois technologies natives comparées côte à côte.
`LOT_15_ALPHA_DAMIER.png` : détourage réel sur damier.

Les trois planches ont été inspectées ; tons naturels et matières distinctes, sans dominante bleue. Les petits détails sont secondaires à la silhouette et moins distincts à 32 px. Technologie volumétrique peinte, pas pictogramme plat de PM.

`preview_validation.json` : **PASS_TECHNICAL_PREVIEW_CHECKS**, 1244 fichiers common/gfx inchangés depuis l'intégration du lot précédent. Aucun DDS de ce nouveau lot exporté. Coins transparents du maître et de la réduction 256 px contrôlés. Aucun essai moteur revendiqué.

## Sources et références

Sources brutes 1254 × 1254 et maîtres à marges transparentes 1574 × 1574 dans `previews/`, PNG 256 px dans `target_size_png/`. Les originaux imagegen restent également à leur emplacement natif ; chemins et empreintes dans `generation_results.json`. Les marges ont été ajoutées mécaniquement sans recolorier, effacer ni recadrer les pixels sources ; preuve dans `canvas_padding.json`.

Prompts exacts : `PROMPTS.md`, `generation_plan.json`. Références natives installées décodées : `references/`, `native_references.json`. Historique : `historical_references.json`.

Références consultées avant création :

- [Eli Whitney Museum — principe des pièces interchangeables](https://www.eliwhitney.org/precision-manufacturing) et [Science Museum — étalons Whitworth](https://collection.sciencemuseumgroup.org.uk/objects/co59394). La photographie des étalons est une référence de matière et de précision, pas le modèle de vis généré.
- [Corning — moule et poinçon du verre pressé](https://allaboutglass.cmog.org/definition/pressed-glass) et [Metropolitan Museum — plat de 1828–1832](https://www.metmuseum.org/art/collection/search/683004). Photo réellement examinée ; produit simplifié, pas copie du décor.
- [Alexander Watt — blanchiment papetier, chapitre IX et figure 20](https://www.gutenberg.org/cache/epub/55757/pg55757-images.html#Page_89). Gravure du mélangeur réellement examinée. Référence technique tardive : l'icône simplifie le principe d'agitation, elle n'est pas une reconstitution de la machine Donkin.

Aucune photographie externe téléchargée ou incorporée. Pas de changement de gameplay, recettes, coûts ou déblocages ; cuivre exclu et sept PM du laboratoire conservés.
