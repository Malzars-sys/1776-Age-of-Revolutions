# Lot 5 — routes et infrastructures régionales

**Aperçus retirés après la correction du joueur du 3 octobre 2026.** Le bâtiment créé est abandonné au profit de l'image vanilla des chemins de fer. Les quatre PM sont à refaire en pictogrammes plats sans ombre ni relief ; Génie routier doit reprendre la photo de pavés en éventail fournie par le joueur. Voir `withdrawal.json` et `../asset8_flat_revision_2026-10-03/`. Les anciens masters et contrôles restent conservés comme historique, pas comme versions approuvées à intégrer.

**Six aperçus créés, contrôlés et présentés. Aucune intégration en jeu avant validation du joueur.**

## Voir les images

- `LOT_5_APERCU.png` : planche des six images et lecture à 32 / 48 / 64 pixels sur fonds clairs et sombres.
- `LOT_5_COMPARAISON_VANILLA.png` : deux références vanilla par famille, bâtiment / technologie / méthode de production.
- `LOT_5_ALPHA_DAMIER.png` : contrôle visuel de la transparence.
- `previews/` : masters PNG RGBA de 1254 × 1254 pixels. La version sélectionnée du bâtiment est `regional_infrastructure_v2.png` ; la première version est conservée.
- `target_size_png/` : réductions à 256 × 256 pixels (bâtiment / technologie) et 208 × 208 pixels (méthodes). Ce sont encore des PNG, pas des textures intégrées.

## Contenu

| Famille | Libellé en jeu | Sujet proposé |
| --- | --- | --- |
| Bâtiment | Infrastructures régionales | Relais routier, pont, péage et diligence au premier plan |
| Technologie | Génie routier | Coupe d'une chaussée empierrée drainée et dame de compactage |
| Méthode | Routes en terre | Ornières et roue de chariot |
| Méthode | Routes à péage | Barrière en bois et pièce sans inscription |
| Méthode | Routes pavées | Fondations en pierre et compactage |
| Méthode | Routes goudronnées | Revêtement sombre et seau de goudron |

Le bâtiment utilise actuellement l'identifiant technique `building_railway`, avec l'alias de réseau de transport terrestre du mod. Son image proposée représente le stade routier initial, sans train. Les méthodes ferroviaires, les canaux et le bien Transport ne sont pas concernés par ce lot. L'icône des Routes pavées pourrait aussi servir au groupe de méthodes de routes, sous réserve de validation.

## Références recherchées avant création

- [Chiltern Open Air Museum : histoire du péage](https://www.coam.org.uk/blogs/historyofthetollhouse), contexte de péage et de relais.
- [Historic England : Toll Bar et piliers de portail](https://historicengland.org.uk/listing/the-list/list-entry/1072919), architecture et porte de péage.
- [Institution of Civil Engineers : routes de Telford](https://www.ice.org.uk/what-is-civil-engineering/infrastructure-projects/telfords-roads), inspiration pour les couches de pierres et le drainage du génie routier.
- [Tring Local History : coupes de chaussées](https://tringlocalhistory.org.uk/Tring/c_chapter%2010.htm), comparaison visuelle des principes de construction.
- [Kent Archaeological Society : Searching for Ebony](https://www.kentarchaeology.org.uk/books/searching-for-ebony), illustration de travaux routiers manuels. La date exacte de la photographie n'a pas été vérifiée et n'est pas affirmée.

Les images sont des compositions originales, pas des copies de photos ni des reconstitutions certifiées d'un site en 1776. Les méthodes avancées correspondent à leurs époques de déblocage, notamment les Routes goudronnées en `era_10`, pas au début de partie.

## Contrôles et conservation

Génération et retouche par imagegen ; aucune recoloration ni suppression de fond manuelle. Seules les réductions et planches de contrôle ont été assemblées localement. Les couleurs naturelles du bâtiment et de la technologie restent distinctes de la série ocre des méthodes. Une retouche ciblée a remplacé la barrière rouge/blanche du bâtiment par du bois naturel.

La vraie transparence extérieure, les quatre coins transparents et les marges ont été vérifiés sur les masters et les réductions. La zone centrale du bâtiment a un alpha minimum de 251/255 ; elle ne comporte pas de trou transparent. Les silhouettes et objets principaux restent reconnaissables à 32, 48 et 64 pixels. Le relief des nouvelles méthodes n'est pas prétendu identique à toutes les familles d'icônes vanilla : la planche de comparaison permet au joueur de juger le style.

Les 1213 fichiers de `common/` et `gfx/` présents lors de l'enregistrement du lot sont inchangés pendant cette phase d'aperçus. Cet état de référence est **postérieur** aux changements de déblocages et de parents de Souveraineté populaire demandés séparément par le joueur. Aucun DDS du lot 5 n'a été créé ; aucun test en jeu n'est revendiqué.

Les prompts, provenance, hashes et contrôles sont conservés dans `generation_requests.json`, `generation_results.json`, `generation_edits.json`, `generation_plan.json`, `preview_manifest.json`, `preview_validation.json` et `visual_review.json`. Contrôle reproductible : `tools/build_asset8_preview_sheet.cjs --verify`.
