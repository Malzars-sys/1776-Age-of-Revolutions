# Lot 16 — révision du sucre uniquement

**État actuel : les trois icônes sont approuvées et intégrées, après la demande « Ok, tu peux tout intégrer et passer au prochain lot. »**

Les sources sélectionnées figurent dans [user_approval.json](user_approval.json). Les trois DDS natifs BGRA8 à 256 px et neuf mipmaps ont été décodés indépendamment : couleurs et alpha correspondent exactement aux PNG de contrôle. Seules les trois lignes de texture ont changé ; le gameplay et les 1246 autres fichiers protégés sont inchangés. Voir [integration_static_validation.json](integration_static_validation.json) et [la planche des DDS décodés](LOT_16_DDS_INTEGRES_QA.png). Aucun essai en jeu n'est revendiqué.

## Historique de la proposition avant intégration

Demande : « Les deux premiers sont OK, mais refais le raffinage du sucre. Je trouve que c'est pas assez parlant. »

## Nouveau concept

Le pain blanc cristallisé devient le sujet dominant, avec son moule conique vide comme unique accessoire. Le groupe évoque la cristallisation et le formage, sans mini-usine ni produit ajouté devant un appareil indépendant. Le pot à mélasse de la première proposition disparaît.

Sources complémentaires : [Bristol Museums](https://museums.bristol.gov.uk/details.php?irn=153990) et [British Museum](https://www.britishmuseum.org/blog/story-sugar-5-objects). Le texte indexé des deux pages a été consulté ; leurs ouvertures directes ont échoué. Les limites et usages des références sont consignés dans [historical_references.json](historical_references.json). Interprétation conceptuelle, pas reconstruction certifiée.

## Fichiers et méthode

- [Nouvelle icône du sucre](previews/sugar_refining_padded.png).
- [Planche du lot actualisée](LOT_16_APERCU.png), avec lecture à 32/48/64 px.
- [Comparaison avec trois technologies vanilla](LOT_16_COMPARAISON_VANILLA.png).
- [Transparence sur damier](LOT_16_ALPHA_DAMIER.png).
- [Prompt exact](PROMPT_SUCRE.md), exécuté avec le générateur intégré **image_gen.imagegen**.
- [Provenance](provenance.json), [approbation partielle](partial_user_approval.json) et [contrôle technique](preview_validation.json).

La première proposition reste dans le dossier parent. Les deux sources approuvées sont réutilisées directement, sans nouvelle génération ou retouche :
`b55c773e53a75f2e2a7a18beb8f53809657764668d10afa77adcc7f1ba00895e` et
`45c68c80d1e783bda07011501775a25df6e4fb50acbda49187eb4ac40a7e774d`.

Le nouveau master de sucre a reçu uniquement des marges transparentes et un centrage mécanique ; tous ses pixels RGBA sont exactement conservés. Dimensions : 1574 × 1574. Le PNG à 256 px sert au contrôle seulement.

À l'étape de prévisualisation, **1247 fichiers de common/gfx étaient inchangés et aucun DDS n'avait été créé**. L'approbation et l'intégration ultérieures sont consignées ci-dessus ; les deux icônes déjà approuvées ont été conservées sans retouche.

