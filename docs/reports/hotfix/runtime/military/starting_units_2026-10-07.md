# Unités terrestres de départ — 7 octobre 2026

Corrections demandées par le joueur, effectuées sur l'arbre de travail existant sans commit, push ou lancement du jeu. Deux fichiers de jeu concernés : `common/combat_unit_types/00_land_combat_unit_types.txt` et `common/history/military_formations/00_military_formations_europe.txt`.

## Bombardes

`combat_unit_type_cannon_artillery`, affiché « Bombarde », consomme désormais `goods_input_iron_add = 0.5` dans son `upkeep_modifier`, à la place de `goods_input_artillery_add = 1`. Ce coût est par unité de combat. Les canons de campagne et l'artillerie à cheval gardent leurs coûts d'artillerie existants. Statistiques, images, upgrades et déblocage `organized_military_establishments` sont conservés.

## Alignement des pays demandés

L'audit prend les technologies ajoutées directement par l'historique du pays **et** les technologies effectivement accordées par `effect_starting_technology_tier_4_tech`, défini dans `common/scripted_effects/00_starting_inventions.txt`. Aucun déblocage n'est supposé à partir d'un simple parent de technologie, aucune recherche supplémentaire n'est accordée.

Les seuils de sélection sont ceux des unités présentes dans le mod : infanterie de ligne (`light_infantry_tactics`), canons de campagne (`standardized_field_artillery`), artillerie à cheval et hussards (`horse_artillery`), dragons (`regulated_small_arms`). Aucun pays de ce périmètre ne possède `military_veterinary_services` ; les cuirassiers prématurés sont remplacés. Le Danemark et la Norvège sont réunis sous le tag `DENNOR` dans la partie de 1776 ; les tags séparés `DEN` et `NOR` n'ont pas de formations de départ à modifier.

| Pays / tag de départ | Artillerie avant → après | Cavalerie après | Réguliers avant → après | Conscrits conservés |
| --- | --- | --- | ---: | ---: |
| France — FRA | 8 bombardes → 16 canons de campagne | 19 dragons | 165 → 173 | 72 |
| Grande-Bretagne — GBR | 2 bombardes → 2 canons de campagne | 5 dragons | 49 → 49 | 43 |
| Espagne — SPA | 8 bombardes → 8 canons de campagne | 14 dragons | 95 → 95 | 70 |
| Autriche — AUS | 15 bombardes → 15 canons de campagne | 20 dragons | 140 → 140 | 39 |
| Prusse — PRU | 8 bombardes → 8 artilleries à cheval | 20 hussards | 108 → 108 | 24 |
| Portugal — POR | 2 bombardes → 2 canons de campagne | 4 dragons | 24 → 24 | 30 |
| Pays-Bas — NET | 2 bombardes → 2 canons de campagne | 4 dragons | 24 → 24 | 6 |
| Danemark–Norvège — DENNOR | 1 bombarde → 1 canon de campagne | 3 dragons | 18 → 18 | 3 |
| Suède — SWE | 2 bombardes → 2 canons de campagne | 5 dragons | 30 → 30 | 7 |

Chaque corps français `cleanup2d3b_fra_land_1` à `cleanup2d3b_fra_land_4` possède exactement quatre canons de campagne, au lieu de deux bombardes. Seules ces huit unités supplémentaires augmentent les effectifs. L'infanterie de ligne était déjà au bon niveau, sauf trois conscrits danois/norvégiens passés d'irréguliers à ligne, sans changement de leur nombre. La réduction antérieure de la Prusse est conservée ; la Russie n'est pas modifiée par ce lot.

Les unités régulières de formation matérialisent leurs casernes dans l'État de recrutement : aucun doublon de caserne explicite n'a été ajouté. Voir la réconciliation du modèle de recrutement dans `docs/reports/cleanup/CLEANUP2D3C_MILITARY_NAVAL_INFRASTRUCTURE_RECONCILIATION_1776.md`.

## Vérification

- `PASS_EXACT_BOMBARD_UPKEEP_CHANGE` : une seule substitution de bien et quantité dans le type Bombarde, tous les autres types strictement conservés.
- `PASS_STARTING_LAND_UNIT_TECH_ALIGNMENT` : comparaison exacte avec un snapshot du fichier de formations avant cette demande ; uniquement les types d'unités prévus et les quatre comptes français 2 → 4 changent.
- Aucun pays hors périmètre, technologie de départ, flotte, commandant, localisation de recrutement ou QG modifié. Effectifs conscrits conservés ; Prusse 108 réguliers et France quatre artilleries par corps vérifiés.
- Diagnostics et snapshots dans `.asset-cache/bombard_upkeep_2026-10-07/` et `.asset-cache/starting_units_2026-10-07/`, non versionnés.

Contrôles statiques uniquement, pas de validation en jeu. Les historiques concernent une nouvelle partie ; une sauvegarde existante n'est pas migrée par ces fichiers.
