# Détourage des icônes de laboratoire

Demande : retirer le fond sombre des sept icônes de PM déjà intégrées. Mode : outil intégré **imagegen**, édition `background-extraction`, `transparent_background: true`. Aucun recours à l'API/CLI payante configurée séparément.

Les PNG originaux `*_source.png` restent intacts. Les détourages retenus sont conservés ici dans `*_transparent.png`. Le manifeste `../tech8c_laboratory_pm_icons.json` conserve la provenance des originaux et l'empreinte des détourages approuvés. L'export DDS est une simple conversion avec alpha et mipmaps, sans retoucher les PNG détourés. Aucun fichier de recette ou de gameplay n'est modifié dans ce lot.

## Prompt commun exact

Remplacer `{subject}` par le sujet correspondant dans le tableau ci-dessous et fournir le PNG original indiqué dans le manifeste comme unique cible d'édition.

```text
Use case: background-extraction.
Asset type: existing Victoria 3 laboratory production-method UI icon.
Input image: edit target, not a style reference.
Primary request: precisely remove the entire dark gray/black backdrop from {subject}, making it genuinely transparent with alpha.
Constraints: change ONLY the background. Preserve the original symbol, colors, bevels, metallic texture, highlights, proportions, orientation, position and square canvas. Keep all subject parts intact. Remove background inside every hole/opening and between disconnected parts too; e.g. the flask is a symbolic outline and a solid liquid symbol, so its empty spaces must be transparent, not filled. Clean anti-aliased edges with no dark rectangle or gray halo. No cast shadow on a backdrop, no new symbols, no restyling, no crop, no text, no checkerboard painted into pixels. Output one isolated icon on actual transparent background.
```

| Icône | Sujet exact du prompt | PNG transparent | DDS consommé par le jeu |
|---|---|---|---|
| manual | the single blue metallic laboratory flask | `manual_transparent.png` | `1776_laboratory_manual.dds` |
| electrical | the blue metallic laboratory flask with a gear | `electrical_transparent.png` | `1776_laboratory_electrical.dds` |
| advanced | the three blue metallic symbols: flask, gear and atom | `advanced_transparent.png` | `1776_laboratory_advanced.dds` |
| general | the green metallic radial arrows and circular ring | `general_transparent.png` | `1776_laboratory_general.dds` |
| production | the green metallic factory and its curved smoke plume | `production_transparent.png` | `1776_laboratory_production.dds` |
| society | the green metallic quill and curved ink stroke | `society_transparent.png` | `1776_laboratory_society.dds` |
| military | the green metallic bicorne hat | `military_transparent.png` | `1776_laboratory_military.dds` |

Les DDS se trouvent dans `gfx/interface/icons/production_method_icons/`. Le contrôle d'alpha du validateur empêche un nouvel export entièrement opaque : plus de 20 % de pixels entièrement transparents, plus de 5 % de pixels du sujet quasi opaques (alpha ≥ 250/255), contours antialiasés et bordure transparente (tolérance de rééchantillonnage ≤ 2/255). Le décodage indépendant par Pillow contrôle le rendu sur damier, puis à 32 pixels sur fond clair et sombre, dans `../tech8c_laboratory_pm_preview.png`.

Le prompt exprime les invariants demandés ; un détourage génératif ne garantit pas la conservation pixel à pixel des symboles. L'inspection finale porte sur la reconnaissance de chaque symbole, les ouvertures, les contours et l'absence de rectangle de fond. L'affichage en jeu reste à confirmer après rechargement des textures.
