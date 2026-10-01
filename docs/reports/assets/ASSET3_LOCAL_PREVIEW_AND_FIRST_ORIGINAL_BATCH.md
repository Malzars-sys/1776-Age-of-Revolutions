# Prévisualisation locale des assets externes — 26 septembre 2026

**Usage local uniquement. Ne pas copier ces huit fichiers dans le Steam build ni publier ce dépôt en l'état.** Les noms `preview_*` et ce registre permettent de retrouver les remplacements. Aucune autorisation de redistribution n'a été obtenue. Les fichiers ne sont pas présentés comme des créations originales de 1776.

Le jeu lit les copies dans `gfx/interface/icons/` et les huit définitions correspondantes pointent désormais vers elles. Les copies sont identiques octet pour octet aux fichiers installés par Steam. Redémarrer Victoria 3 pour voir les changements d'interface.

Aperçu visuel des candidats : `ASSET3_PREVIEW_SHEET.png` (planche locale de contrôle, également non publiable sans autorisations).

| Objet du mod | Source (Workshop ID, chemin sous `gfx/interface/icons/`) | Fichier local de prévisualisation | SHA-256 |
|---|---|---|---|
| `organized_workshops` | Basileia `2880120246`, `invention_icons/br_tech_artisan_manufacturing.dds` | `invention_icons/preview_basileia_organized_workshops.dds` | `3083E3BDE32078492C98F3FAADCCA634F4B2161C01047A23CC3CD24BD2A701AA` |
| `institutionalized_scientific_exchange` | Basileia `2880120246`, `invention_icons/br_tech_early_modern_universities.dds` | `invention_icons/preview_basileia_scientific_exchange.dds` | `226F3F3E6A9ADC15289789D28075368D7BD5B09EA8E9D13CFDCEB48580FF857C` |
| `traditional_papermaking` | Basileia `2880120246`, `invention_icons/br_tech_paper_manufacturies.dds` | `invention_icons/preview_basileia_traditional_papermaking.dds` | `876EE757FC68FAA98E004E43AF9BE266C76F6F1AC162193CC09A3BABBD69A2F1` |
| `improved_agricultural_implements` | Basileia `2880120246`, `invention_icons/br_tech_seed_drill.dds` | `invention_icons/preview_basileia_agricultural_implements.dds` | `938F85FA556028CE4904834697B177E3E468C00A70BE1929276411156B007A25` |
| `geological_surveying` | Morgenröte `2889925770`, `invention_icons/agassiz_geology_tech.dds` | `invention_icons/preview_morgenroete_geological_surveying.dds` | `6FD2E98098E7C1FEB269CAD5C0F7D0CBB5F612A5E02D14359AF0A71D4D895016` |
| `vaccination` | Morgenröte `2889925770`, `invention_icons/panum_vaccination_tech.dds` | `invention_icons/preview_morgenroete_vaccination.dds` | `E0BE4085414D65D12D611FCA88EDCEF36B005BB61104A1F3B5688A85207C96D3` |
| `mechanized_printing` | Morgenröte `2889925770`, `invention_icons/manzoni_rotary_press_tech.dds` | `invention_icons/preview_morgenroete_mechanized_printing.dds` | `C3147D6AAC19764F52B99B7BBEFEBDD4555E57A623BAE6C5F423612A528701CD` |
| `pm_private_pharmacies` | Economic & Financial Mod `3143591632`, `production_method_icons/unuse/apothecaries.dds` | `production_method_icons/preview_ef_private_pharmacies.dds` | `A2F21C819914D4BC0555902FA5CACDEDBA34E0F2745205380C26AFA92980DB23` |

Basileia affiche plusieurs auteurs (Alexedishi, Drogan, Smekens), mais la propriété fichier par fichier reste inconnue. Le fichier `MR_Artwork_credits.txt` de Morgenröte attribue les trois icônes retenues à Valerie P : une permission du mod seul ne suffit pas nécessairement. Aucun titulaire des droits n'est établi pour l'icône d'Economic & Financial Mod. Ces huit fichiers restent donc **permission en attente**. Une autorisation de visualisation locale n'est pas une autorisation de redistribuer.

## Nouveaux mods inspectés

- Economic and Financial Mod (E&F) - V4 (`3143591632`) : 857 images locales, principalement finances/monnaie. Trois icônes pharmaceutiques ont été comparées visuellement ; le mortier d'`apothecaries.dds` est le plus adapté à l'époque. Aucun remplacement convaincant trouvé pour les biens miniers prioritaires.
- Expanded Topbar Framework (`3508296963`) : trois images locales, aucune icône d'objet adaptée à ce lot.
- Morgenröte - Dawn of Flavor (`2889925770`) : 3 682 images locales, surtout événements, personnages et interfaces. Trois icônes de technologie ont une correspondance utilisable en prévisualisation. Les crédits distinguent plusieurs artistes ; ne pas appliquer une permission globale à tous les fichiers.

Les autres fichiers examinés, notamment la seringue moderne de Morgenröte et le bâtiment universitaire de Basileia, doivent être jugés **en jeu** pour leur adéquation à la période et à la signification précise de la technologie. Ils sont faciles à remplacer grâce au préfixe `preview_`.

## Premier lot d'originaux à créer

Huit images, pour remplacer des `gfx/error_deer.dds` encore actifs et couvrir trois chaînes de ressources visibles sur la carte et le marché. Créer un master carré à fond transparent (idéalement 1024 × 1024), puis fournir un PNG final de 256 × 256 pixels avec alpha. Nous convertirons les PNG validés au format DDS. Ne pas intégrer les chiffres de niveau du bâtiment : le jeu les superpose lui-même.

Pour chaque **bien**, objet isolé et centré, silhouette lisible à petite taille, sans socle ni cercle opaque. Pour chaque **bâtiment**, conserver la grammaire visuelle déjà convenue : établissement historique en arrière-plan, bien principal en bas à droite, bordure métallique aux coins arrondis. Éclairage et couleurs cohérents avec les icônes existantes du mod.

| Priorité | Objet / fichier final souhaité | Brief visuel |
|---|---|---|
| 1 | Bien `copper` → `gfx/interface/icons/goods_icons/1776_copper.dds` | Deux lingots rouge-cuivré et un fragment de minerai veinuré ; ne pas ressembler au fer gris ni à l'or jaune. |
| 2 | Bâtiment `building_copper_mine` → `gfx/interface/icons/building_icons/1776_copper_mine.dds` | Entrée de mine et treuil en bois du XVIIIe–XIXe siècle ; minerai cuivré en bas à droite. |
| 3 | Bien `limestone` → `gfx/interface/icons/goods_icons/1776_limestone.dds` | Blocs calcaires blanc cassé/ocre clair, surface poreuse ; distincts du sel et du ciment. |
| 4 | Bâtiment `building_limestone_quarry` → `gfx/interface/icons/building_icons/1776_limestone_quarry.dds` | Carrière à gradins, ouvriers/treuil discrets ; blocs calcaires en bas à droite. |
| 5 | Bien `phosphates` → `gfx/interface/icons/goods_icons/1776_phosphates.dds` | Roche phosphatée brun-sable à grains irréguliers ; distincte du calcaire pâle et du soufre jaune. |
| 6 | Bâtiment `building_phosphate_mine` → `gfx/interface/icons/building_icons/1776_phosphate_mine.dds` | Extraction de roche phosphatée, galerie ou carrière et wagonnet ; minerai brun-sable en bas à droite. |
| 7 | Bien `cement` → `gfx/interface/icons/goods_icons/1776_cement.dds` | Sac de toile ouvert avec poudre de ciment grise et petite truelle ; éviter l'aspect d'un sac de sel. |
| 8 | Bien `refined_fuels` → `gfx/interface/icons/goods_icons/1776_refined_fuels.dds` | Bidon métallique ancien et petite bouteille de distillat ambré ; distinct du pétrole brut noir. |

Ce lot ne requiert aucune copie d'images tierces. Les mines, biens et produits restants (raffinerie, chemins de fer, machines de précision, méthodes de production, etc.) constitueront les lots suivants après validation visuelle de celui-ci.
