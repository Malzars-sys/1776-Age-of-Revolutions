# Cuivre : demande vanilla 1.15 et icônes de concentration — 7 novembre 2026

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Modifications installées localement ; contrôles statiques réussis, marché et rendu en jeu à vérifier après redémarrage. Aucun lancement du jeu, changement de sauvegarde ou écriture Git.

## Périmètre demandé

Comparer les nouvelles méthodes qui consomment du cuivre et les anciennes méthodes devenues consommatrices dans le vanilla canonique `C:/Games/Victoria 3/game`. Aligner leurs coefficients de cuivre en conservant les autres recettes du mod, ses gisements, capacités, bâtiments de départ et rendements miniers. Remplacer les deux icônes provisoires du cuivre par les icônes de concentration existantes des autres mines. L'Espagne reste en attente.

## Résultat

Les **28 méthodes natives consommatrices de cuivre** sont présentes, rattachées à des groupes utilisés par des bâtiments, et ont les mêmes coefficients directs de cuivre que le vanilla installé. Parmi les méthodes préexistantes, 25 coefficients sont corrigés ; les moteurs électriques étaient déjà à 10. Les téléphones passent de 15 à 30.

Deux méthodes absentes sont ajoutées : `pm_bronze_cannons` et `pm_bronze_smoothbores`, puis reliées à `pmg_foundries`. La méthode par défaut et l'alternative en bronze propre au mod sont conservées. Aucune méthode initiale n'est remplacée dans l'historique des pays.

### Comparaison des coefficients

Unités : consommation par niveau à effectif plein dans `building_modifiers/workforce_scaled`, avant autres modificateurs. Ces lignes sont des recettes alternatives ou cumulables selon leurs groupes ; **ne pas sommer la colonne pour en déduire une demande mondiale**.

| Méthode | Mod avant | Vanilla 1.15 | Mod après |
| --- | ---: | ---: | ---: |
| `pm_pot_stills` | 0 | 2 | 2 |
| `pm_patent_stills` | 0 | 4 | 4 |
| `pm_automated_bakery` | 0 | 1 | 1 |
| `pm_electric_sewing_machines` | 0 | 2 | 2 |
| `pm_automatic_power_looms` | 0 | 2 | 2 |
| `pm_assembly_lines_building_furniture_manufactory` | 0 | 1 | 1 |
| `pm_assembly_lines_building_tooling_workshop` | 0 | 1 | 1 |
| `pm_electric_engines` | 10 | 10 | 10 |
| `pm_assembly_lines_building_motor_industry` | 0 | 1 | 1 |
| `pm_assembly_lines_building_automotive_industry` | 0 | 1 | 1 |
| `pm_telephones` | 15 | 30 | 30 |
| `pm_bronze_cannons` | Absent | 10 | 10 |
| `pm_bronze_smoothbores` | Absent | 20 | 20 |
| `pm_assembly_lines_building_arms_industry` | 0 | 1 | 1 |
| `pm_percussion_caps` | 0 | 5 | 5 |
| `pm_explosive_shells` | 0 | 10 | 10 |
| `pm_assembly_lines_building_munition_plant` | 0 | 1 | 1 |
| `pm_arcades` | 0 | 1 | 1 |
| `pm_early_power_plant` | 0 | 2 | 2 |
| `pm_coal-fired_plant` | 0 | 4 | 4 |
| `pm_oil-fired_plant` | 0 | 5 | 5 |
| `pm_refrigerated_storage_building_fishing_wharf` | 0 | 1 | 1 |
| `pm_refrigerated_rail_cars_building_fishing_wharf` | 0 | 1 | 1 |
| `pm_flash_freezing_building_fishing_wharf` | 0 | 1 | 1 |
| `pm_refrigerated_storage_building_whaling_station` | 0 | 1 | 1 |
| `pm_refrigerated_rail_cars_building_whaling_station` | 0 | 1 | 1 |
| `pm_flash_freezing_building_whaling_station` | 0 | 1 | 1 |
| `pm_arc_welded_buildings` | 0 | 10 | 10 |

Les autres intrants, sorties, emplois et prérequis des méthodes existantes restent identiques. Les nouveaux canons reprennent les recettes et emplois natifs : 10 cuivre + 15 bois dur pour 25 artilleries ; les canons lisses en bronze, 20 cuivre + 20 bois dur pour 45 artilleries.

### Technologie des nouveaux canons

Le premier PM natif exige `artillery`. Dans ce mod, cette ancienne clé est un alias de compatibilité d'ère 7 avec `can_research = no`. Le nouveau PM utilise donc `organized_military_establishments`, comme les canons de premier niveau du mod. Le PM de canons lisses conserve `shell_gun`. Les deux clés existent ; aucun arbre technologique, profil national ou bâtiment initial n'est modifié.

Les titres natifs français et anglais des deux PM sont hérités sans fichier masquant ces clés ; leurs textures natives existent. Aucun nouveau texte ou asset n'est généré.

### Centrales et cumul des groupes

Le mod ajoutait déjà 2 cuivre via le groupe des conducteurs. Ajouter les intrants natifs sans adapter ce groupe aurait donné 4/6/7 au lieu de 2/4/5.

Les bases des centrales ont maintenant les coefficients natifs 2/4/5 ; le PM de conducteurs en cuivre ajoute 0 au lieu de 2. L'option aluminium conserve son intrant de 1 aluminium et son verrou `bayer_process`, et applique `goods_input_copper_mult = -1` dans les modificateurs **non mis à l'échelle** du bâtiment pour remplacer la consommation de cuivre de la base.

| Centrale avec conducteurs en cuivre | Cumul avant | Cumul après | Vanilla |
| --- | ---: | ---: | ---: |
| Première centrale | 2 | 2 | 2 |
| Centrale au charbon | 2 | 4 | 4 |
| Centrale au pétrole | 2 | 5 | 5 |

Dans le modèle statique sans autres modificateurs, l'option aluminium maintient une demande de cuivre nulle pour les trois bases. L'effet réel du modificateur, le basculement cuivre/aluminium et les autres modificateurs du pays doivent être vérifiés en jeu. Le contrat natif des PM décrit les blocs `building_modifiers/unscaled` ; le type `goods_input_copper_mult` est déjà enregistré dans le mod. Aucun intrant aluminium ni autre effet n'est supprimé.

### Usages propres au mod et prix

Les consommateurs spécifiques — alliages, ustensiles, radios, machines de précision et doublage des coques — sont conservés. L'alignement porte sur les 28 recettes natives, pas sur une égalité de demande agrégée entre deux économies comportant des bâtiments et biens différents.

Les recettes minières restent inchangées. La collision déjà documentée entre le bien cuivre du mod à prix de base 50 et le bien natif à 40, ainsi que les quatre groupes miniers homonymes, reste une dette séparée. Aucun ordre de chargement ni prix effectivement résolu n'est certifié ici ; aucun changement de prix ou de distribution n'a été ajouté.

Sensibilité du **seul surcoût de cuivre**, à effectif plein et avant autres modificateurs : les alambics simples ajoutent 2 unités, soit 80 à prix 40 ou 100 à prix 50 ; les téléphones ajoutent 15 unités, soit 600 ou 750. À moitié d'effectif, ces valeurs sont divisées par deux. Pour les centrales, raisonner sur le cumul des groupes : hausse nulle pour la première centrale, +2 au charbon, +3 au pétrole. Ce ne sont ni des profits, ni des budgets de bâtiment entiers, ni des prix observés.

## Icônes

Seules les références `texture` des PM de tri manuel et de concentration de la mine de cuivre sont changées :

- `1776_manual_ore_sorting.dds` pour le tri manuel ;
- `1776_ore_concentration.dds` pour la concentration.

Ce sont les mêmes fichiers que pour le fer, le charbon et les autres mines du mod. Les deux DDS existants se décodent en 208 × 208 et conservent leurs empreintes. Les rendements, coûts, pollution et prérequis de concentration restent identiques. La bauxite et les phosphates utilisaient déjà ces icônes ; aucune réécriture de ces PM n'était nécessaire. Les autres placeholders sans rapport avec la concentration ne sont pas remplacés dans ce lot.

## Contrôles et preuves

`tools/compatibility/v115_copper_demand_audit.py` vérifie les masquages par chemin, les remplacements explicites `REPLACE_OR_CREATE`, l'unicité des 28 consommateurs effectifs, leurs groupes/bâtiments, les technologies, la conservation des champs hors cuivre, les deux nouveaux PM, le cumul des centrales, les localisations natives et les textures.

```text
python -B tools/compatibility/v115_copper_demand_audit.py --mod-root . --baseline-root docs/reports/economy/V1_15_COPPER_DEMAND_2026_11_07/BASELINE --vanilla-root "C:/Games/Victoria 3/game"
```

Résultat : **PASS_STATIC_ONLY**, 28 consommateurs natifs alignés, huit fichiers de gameplay concernés, 29 PM existants modifiés au total en comptant les deux icônes et les deux adaptations de conducteurs, et deux nouveaux PM.

Les huit contrôles négatifs détectent une quantité de cuivre incorrecte, un intrant non cuivre modifié, un rendement minier altéré, une icône incorrecte, le cuivre des centrales compté deux fois, la substitution aluminium perdue, le retour à l'alias technologique non recherchable et un PM bronze détaché de son groupe. Les mutations de test ont lieu uniquement dans une copie temporaire, rétablie avant installation.

Les sources exactes sont conservées dans `BASELINE`. `PLAN.json`, `PREFLIGHT.json` et `VALIDATION.json` donnent les mappings, empreintes, comparaisons et résultats. **379 fichiers protégés** conservent leurs empreintes, dont les historiques de bâtiments/ressources, biens, bâtiments, autres groupes et méthodes, journaux et icônes réutilisées. Les champs non ciblés des fichiers partagés sont inchangés. `git diff --check` passe.

## Validation en jeu restante

Après redémarrage, vérifier les deux icônes du cuivre ; les alambics et les autres méthodes à cuivre ; la quantité 30 des téléphones ; les deux options bronze et leurs verrous ; les trois centrales avec cuivre puis aluminium, à effectif connu. Contrôler les intrants réellement affichés, le coût, l'approvisionnement et les pénuries du marché, puis sauvegarde/rechargement. L'état antérieur des gisements et niveaux construits doit être conservé.

Ces contrôles statiques ne certifient ni l'équilibre économique global, ni la rentabilité, ni l'affichage en jeu. Les effets des recettes nouvelles sur le marché sont à observer sur cette version installée.
