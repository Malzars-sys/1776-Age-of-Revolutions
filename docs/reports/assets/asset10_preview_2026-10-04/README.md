# Lot 7 — navigation maritime, intégré

Date : 4 octobre 2026. Statut : **trois icônes approuvées par le joueur, intégrées et validées statiquement**. Aucun essai en jeu revendiqué. Les sources imagegen approuvées sont conservées sans retouche ni nouvelle génération.

## Trois propositions

| Technologie | Concept | Master PNG |
|---|---|---|
| Chronométrie marine | Montre marine à cadran blanc, inspirée de la silhouette du H4 | [Master](previews/marine_chronometry.png) |
| Levé hydrographique | Carte côtière claire avec sextant en laiton | [Master](previews/hydrographic_surveying.png) |
| Optique des phares | Tambour optique à lentilles à échelons | [Master](previews/modern_lighthouse_optics.png) |

Les trois anciens liens `gfx/error_manul.dds` ont été remplacés dans `common/technology/technologies/25_tech3a_naval.txt`. Seules ces trois lignes de texture changent ; recettes, effets, prérequis et tous les autres paramètres restent identiques. Les technologies sont dans la branche navale de l'onglet militaire.

## Fichiers intégrés et preuve

| Technologie | DDS final |
|---|---|
| Chronométrie marine | [1776_marine_chronometry.dds](../../../../gfx/interface/icons/invention_icons/1776_marine_chronometry.dds) |
| Levé hydrographique | [1776_hydrographic_surveying.dds](../../../../gfx/interface/icons/invention_icons/1776_hydrographic_surveying.dds) |
| Optique des phares | [1776_modern_lighthouse_optics.dds](../../../../gfx/interface/icons/invention_icons/1776_modern_lighthouse_optics.dds) |

- [Autorisation et empreintes des masters approuvés](user_approval.json).
- [Manifeste d'intégration](integration_manifest.json) et [validation indépendante](integration_static_validation.json).
- [Contrôle des couleurs et de la transparence après décodage des DDS](LOT_7_DDS_INTEGRES_QA.png).

Chaque DDS : 256 × 256 px, neuf mipmaps, format natif BGRA8 legacy A8R8G8B8. Le décodage indépendant correspond exactement au PNG réduit ; les neuf niveaux conservent les couleurs et l'alpha. Les quatre coins restent transparents. **1 219 autres fichiers protégés sous common et gfx sont inchangés** ; les seules additions sont les trois DDS ci-dessus.

Le joueur doit redémarrer/recharger le jeu pour vérifier le rendu moteur. Cette validation technique n'est pas présentée comme une validation en partie.

## Aperçus et contrôles

- [Planche du lot et miniatures 32/48/64 px](LOT_7_APERCU.png).
- [Comparaison avec trois technologies vanilla](LOT_7_COMPARAISON_VANILLA.png).
- [Contrôle de transparence sur damier](LOT_7_ALPHA_DAMIER.png).
- [Contrôles techniques](preview_validation.json) et [revue visuelle](visual_review.json).
- [Plan de génération](generation_plan.json), [prompts exacts](generation_requests.json) et [provenance des fichiers générés](generation_results.json).

Génération avec **imagegen intégré**, pas le CLI ni un montage dessiné par script. Les scripts ne font que décoder les références vanilla, réduire les PNG, composer des planches et calculer les empreintes. Les originaux générés restent conservés.

Les masters font 1254 × 1254 px et possèdent un canal alpha réel ; leurs quatre coins et ceux des PNG réduits à 256 px sont transparents. Le rapport d'aperçu et sa comparaison des **1 220 fichiers sous common et gfx**, inchangés pendant la préparation, restent archivés sans écrasement. Ils décrivent l'état avant intégration ; les preuves de l'état final sont dans la section précédente.

## Références recherchées avant génération

- [H4, Royal Museums Greenwich](https://www.rmg.co.uk/collections/objects/rmgc-object-79142) : silhouette de montre marine, objet daté de 1759 dans le catalogue.
- [Sextant de Jesse Ramsden, Royal Museums Greenwich](https://www.rmg.co.uk/collections/objects/rmgc-object-43317) : instrument vers 1790.
- [Cartes marines, Royal Museums Greenwich](https://www.rmg.co.uk/stories/maritime-history/curatorial/mapping-untold-stories-women-london-chart-trade) : exemples de cartes de 1804.
- [Première optique de Cordouan, Ministère de la Culture](https://cordouan.culture.gouv.fr/fr/la-premiere-optique-de-cordouan) et [photographie de l'appareil](https://cordouan.culture.gouv.fr/fr/media/view/5357) : appareil installé en 1823.

Les images de musée et les résultats de recherche servent à étudier les formes et les périodes, sans téléchargement ni copie dans les nouveaux assets. Les trois illustrations sont des interprétations simplifiées, pas des répliques techniques exactes. Les chiffres des cadrans et cartes sont omis selon la règle sans texte. Le catalogue de la lentille Science Museum de 1968 et l'optique d'Hourtin de 1894 ont été écartés comme modèles d'époque exacte.

Les références de style locales `navigation`, `mechanical_tools` et `crystal_glass` ont été décodées et examinées avant création ; elles restent de simples références, pas de nouveaux assets du mod.

## Garde-fous appliqués à l'intégration

La chaîne du cuivre, les sept anciens PM du laboratoire et les autres assets déjà validés restent intacts. Aucun changement de recette, prérequis, effet, statistique ou localisation.

L'export et les trois liens ont été créés après autorisation uniquement, au format natif **BGRA8 legacy A8R8G8B8** et non RGBA8. Cela conserve les couleurs validées et évite la disposition des canaux qui avait inversé le rouge et le bleu dans des lots précédents. Les champs `current_texture` du plan gardent l'état observé avant intégration pour la traçabilité ; le manifeste d'intégration et les définitions du mod indiquent les liens finaux.
