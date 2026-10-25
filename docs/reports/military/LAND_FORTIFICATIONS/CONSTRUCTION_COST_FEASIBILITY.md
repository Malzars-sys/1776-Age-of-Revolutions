# Coût progressif des fortifications terrestres — faisabilité

19 octobre 2026. Vérification documentaire et lecture des scripts ; aucun essai moteur.

**Suite autorisée :** l’utilisateur a ensuite choisi une base fixe de 900 et un ralentissement par efficacité, avec de nouvelles cibles de 900/1 100/1 300/1 500/1 700 points effectifs. Voir [CONSTRUCTION_R1/REPORT.md](CONSTRUCTION_R1/REPORT.md). Le présent document conserve la demande et le constat initiaux.

## Demande

Coût additionnel de chaque niveau : 400, 600, 800, 1 000 puis 1 200 points. Total des cinq niveaux : 4 000 points.

## Constat sur la version locale

Le bâtiment actuel utilise `required_construction = construction_cost_very_low`. La constante vanilla correspond à 100 points. Les 83 déclarations de coût trouvées dans les bâtiments vanilla utilisent toutes une référence scalaire.

L’interface de script documente `required_construction` sur la portée **building_type**, qui représente le type de bâtiment. Elle ne présente pas ce coût comme un paramètre d’un niveau ou d’un projet particulier. Aucun paramètre de supplément par niveau, tableau de coûts successifs ou modificateur de points requis par niveau n’a été trouvé dans les définitions de bâtiments, groupes, modificateurs et constantes consultées.

Les valeurs scriptées employées comme noms de constantes ne suffisent pas à démontrer que ce champ est une formule réévaluée dans le contexte de chaque chantier. Une expression utilisant le niveau du bâtiment ne doit donc pas être présentée comme une solution prise en charge sans essai moteur.

**Conclusion documentaire : aucun mécanisme natif documenté ne permet de définir ce barème directement sur les cinq niveaux du bâtiment actuel.** Un changement simple du coût de base s’appliquerait uniformément aux niveaux.

La documentation locale `buildings.md` comporte encore le nom ancien `construction_points`, déclaré comme entier. Le jeu installé utilise effectivement `required_construction`. Cette divergence limite l’usage du schéma textuel comme preuve d’un détail de parsing ; elle ne constitue pas un test de formule dynamique.

## Pistes pour reproduire le résultat

1. **Cinq étapes de construction distinctes**, chacune avec son propre type de bâtiment, coût fixe et limite d’un niveau. Les étapes suivantes exigeraient la précédente dans le même État. Les coûts seraient respectivement 400/600/800/1 000/1 200. Cette piste demande une refonte de la représentation des forts et des essais des prérequis, files, démolitions, PM, sauvegardes et comportement de l’IA. Ce n’est pas une implémentation validée dans ce lot.
2. **Efficacité de construction dépendant du développement du fort.** Les groupes peuvent exposer un modificateur d’efficacité de construction. Cela agit sur la progression hebdomadaire, avec les autres bonus applicables ; cela ne définit pas cinq coûts requis distincts. Cette piste ne répond donc pas exactement à la demande.

Conserver un seul bâtiment extensible, son interface habituelle et cinq coûts de points réellement différents n’est pas confirmé par les capacités documentées consultées. Le constat « aucun support natif documenté trouvé » ne prétend pas remplacer un essai du moteur ni une lecture du code source propriétaire.

## Références

- Mod : `common/buildings/1776_land_fortifications.txt`, `common/building_groups/1776_land_fortifications.txt`.
- Vanilla canonique `C:/Games/Victoria 3/game` : `common/buildings/buildings.md:37`, `common/script_values/building_values.txt:7`, les 83 déclarations de `required_construction` dans `common/buildings/*.txt`.
- Groupes et efficacité : `common/building_groups/00_building_groups.txt`, `common/modifier_type_definitions/01_building_modifier_types.txt`, `localization/english/modifiers_l_english.yml`.
- Documentation générée du moteur 1.13 : [event_targets.log — required_construction](https://github.com/Victoria-3-Modding-Co-op/Modding-Digests/blob/main/1.13.0/docs/event_targets.log). Copie déjà conservée dans `../ENGINEER_CORPS/sources/event_targets.log`.

Les fichiers de jeu n’ont pas été modifiés pendant cette vérification.
