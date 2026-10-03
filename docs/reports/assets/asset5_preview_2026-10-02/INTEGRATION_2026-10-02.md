# Intégration du lot phosphate–minerais

> Mise à jour ultérieure du 2 octobre : seule l'icône **Levé géologique** a été remplacée par la variante au papier plus blanc, sur demande explicite. Voir [la retouche et son intégration](../geological_survey_white_paper_2026-10-02.md). La planche du lot et le contrôle global ci-dessous sont les relevés historiques de la première intégration ; l'aperçu et les contrôles ciblés de la nouvelle version sont reliés dans cette note.

Date : 2 octobre 2026. Autorisation utilisateur : « OK, c'est bon, tu peux intégrer tout au mod. »

Les six images du lot sont exportées et branchées dans les définitions du mod. La mine utilise la variante V4 au lever du soleil ; les cinq autres utilisent les dernières propositions validées. Les PNG originaux et variantes restent conservés.

| Objet | Export |
|---|---|
| Phosphates | `gfx/interface/icons/goods_icons/1776_phosphates.dds` |
| Mine de phosphate, lever du soleil | `gfx/interface/icons/building_icons/1776_phosphate_mine.dds` |
| Minéralogie appliquée | `gfx/interface/icons/invention_icons/1776_applied_mineralogy.dds` |
| Levé géologique | `gfx/interface/icons/invention_icons/1776_geological_surveying.dds` |
| Tri manuel | `gfx/interface/icons/production_method_icons/1776_manual_ore_sorting.dds` |
| Concentration des minerais | `gfx/interface/icons/production_method_icons/1776_ore_concentration.dds` |

## Vérifications

Les quatre premières textures sont en 256 × 256 avec neuf mipmaps ; les deux PM sont en 208 × 208 avec huit mipmaps (208, 104, 52, 26, 13, 6, 3, 1). Export DDS RGBA8 sans compression destructive supplémentaire. Le DDS est décodé indépendamment et comparé pixel par pixel au PNG réduit. Les coins extérieurs sont réellement transparents et les sources approuvées sont contrôlées par empreinte.

Seuls six champs visuels changent, dans quatre fichiers de définition. Une comparaison avec l'état de travail juste avant l'intégration confirme que recettes, emplois, prix, statistiques, technologies et autres champs sont inchangés. Les 1 190 autres fichiers protégés de `common/` et `gfx/` sont identiques ; les seuls ajouts dans ces dossiers sont les six DDS attendus. Les modifications antérieures du mod sont conservées.

**Réserve conservée :** l'intérieur de la mine n'est pas exactement opaque : alpha 249–253 au lieu de 255 dans la zone centrale, soit environ 97,6–99,2 % d'opacité. L'image approuvée est exportée avec son alpha d'origine ; le défaut n'est pas présenté comme corrigé. Les blocages d'export des anciens rapports de préparation sont historiques : cette intégration est une livraison explicite avec réserve, pas une conformité à l'exigence initiale d'opacité intérieure exacte.

Aucun test dans le jeu en cours n'est revendiqué. Le cuivre, les laboratoires et les quatre aperçus ciment encore non validés ne sont pas modifiés. Aucun asset historique ou tiers n'est supprimé.

## Livrables et reproduction

- [Planche des DDS réellement décodés](LOT_2_DDS_INTEGRES_QA.png).
- [Approbation, sources, prompts et état initial](integration_manifest.json).
- [Contrôle d'export](integration_export_validation.json) et [contrôle indépendant](integration_static_validation.json).
- PNG réduits correspondants dans `integrated_target_png/`.

Reproduction depuis la racine du mod : `tools/export_asset5_approved_icons.cjs`, puis `tools/validate_asset5_approved_icons.py`. L'exporteur refuse toute collision avec un DDS différent. Les anciens outils de génération de planches de préparation conservent leur garde contre l'intégration et ne doivent plus être relancés comme validation finale.
