# Correction des couleurs des bâtiments

Date : 3 octobre 2026. Périmètre : quatre icônes intégrées, sans modification de gameplay ni retouche artistique.

**Complément après la capture du calcaire :** ce rapport décrit seulement la première passe. Le [diagnostic étendu](../all_asset_color_layout_2026-10-03/README.md) couvre aussi les biens, technologies, PM et illustrations militaires (38 conversions supplémentaires). Son état de référence courant remplace ce rapport pour les vérifications globales : le contrôle global historique limité à quatre DDS ne doit plus être exécuté comme si les autres textures n'avaient pas été corrigées.

## Diagnostic établi avant modification

Les PNG approuvés et le décodage standard des DDS correspondent exactement. Le problème n'est donc pas une peinture modifiée pendant l'export. Les quatre exports utilisent cependant des octets **RGBA**, alors que la mine de charbon vanilla installée utilise des octets **BGRA**, avec des masques rouge et bleu inversés.

La lecture de l'ancien stockage suivant la convention native reproduit le cadre cyan, la végétation bleutée et la pierre froide visibles dans la capture du joueur. C'est une preuve forte de l'origine du défaut ; la façon dont le moteur traite en interne les masques reste une déduction, non une inspection du code moteur. La [documentation Microsoft des masques DDS](https://learn.microsoft.com/en-us/windows/win32/direct3ddds/dds-pixelformat) confirme la signification des masques, pas le comportement de Victoria 3.

Le contrôle précédent utilisait uniquement un décodeur DDS respectant les masques : il pouvait valider les pixels tout en manquant cette incompatibilité en jeu. Les anciens rapports ASSET4–6 sont des instantanés historiques et **ne constituent pas une validation du rendu moteur**. La nouvelle vérification compare aussi le stockage natif.

## Correction minimale

Convertir les quatre DDS au même agencement que le bâtiment vanilla : échanger les octets de stockage rouge/bleu et changer simultanément leurs masques. **Les couleurs logiques, l'alpha, les dimensions et les neuf mipmaps restent strictement identiques.** Aucun PNG n'est recolorié, aucun asset n'est régénéré.

- Carrière de calcaire : `gfx/interface/icons/building_icons/1776_limestone_quarry.dds`.
- Laboratoire : `gfx/interface/icons/building_icons/1776_research_laboratory.dds`.
- Mine de phosphate : `gfx/interface/icons/building_icons/1776_phosphate_mine.dds`.
- Raffinerie : `gfx/interface/icons/building_icons/1776_oil_refinery.dds`.

Les originaux DDS sont conservés dans `backups/`, avec leur empreinte dans le nom. Les scripts d'export correspondants appliquent désormais cette convention aux bâtiments ; les autres familles ne sont pas modifiées dans cette passe.

## Contrôle et limite

[Diagnostic avant correction](diagnosis.json), [validation après conversion](validation.json), [planche comparative](DDS_CORRIGES_COMPARAISON.png). La colonne centrale est une **simulation diagnostique de l'ancien ordre de couleurs**, pas une capture du jeu. Les colonnes de gauche et de droite doivent être identiques.

Le contrôle vérifie tous les pixels de tous les mipmaps, l'alpha, la correspondance au PNG approuvé et le respect de la référence native. Un état de référence de l'ensemble des fichiers `common` et `gfx` vérifie que seuls les quatre DDS sont changés. Les sources restent intactes.

Résultats : **quatre fichiers DDS convertis, 1 206 autres fichiers de jeu inchangés**. Un [second contrôle indépendant avec Pillow](independent_validation.json) décode séparément les neuf mipmaps de chaque original et de chaque sortie ; tous les pixels RGBA sont identiques. Les validateurs ASSET4–6 et du laboratoire vérifient maintenant le stockage natif pour les bâtiments. Les anciennes empreintes d'export restent conservées ; le contrôle accepte uniquement une conversion de format dont la reconstitution octet par octet retrouve exactement cette empreinte.

**Le rendu après correction doit encore être confirmé dans Victoria 3.** Aucun lancement, redémarrage ou rechargement du jeu n'est revendiqué. Le jeu déjà ouvert peut conserver les anciennes textures en mémoire ; un redémarrage complet est recommandé. Il n'est pas nécessaire de recommencer la partie pour une correction d'icônes.

Reproduction : `node tools/fix_building_icon_color_layout.cjs --verify`. Le mode `--audit` est réservé au diagnostic initial et refuse d'écraser celui-ci ; `--fix` est une conversion contrôlée par l'état de référence et refuse un état modifié depuis l'audit.
