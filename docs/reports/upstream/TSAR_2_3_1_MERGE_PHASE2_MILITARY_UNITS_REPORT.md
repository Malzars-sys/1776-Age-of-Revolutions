# Fusion Tsar 2.3.1 — phase 2 : unités militaires ciblées

Date : 2026-09-16  
Portée : intégration adaptée des deux types d’unité retenus pendant la phase 1, sans copie globale des fichiers Tsar.

## Résultat

Deux paliers ont été ajoutés à la définition terrestre du fork :

| Chaîne | Unité | Technologie | Attaque | Défense | Perte de moral | Coût principal |
|---|---|---|---:|---:|---:|---|
| Infanterie | Irréguliers | aucune | 10 | 10 | 15 | aucun |
| Infanterie | Infanterie à mousquet | `regulated_small_arms` | 15 | 20 | 10 | 1 arme légère |
| Infanterie | Infanterie de ligne | `light_infantry_tactics` | 20 | 25 | 10 | 1 arme légère |
| Artillerie | Bombarde | `organized_military_establishments` | 20 | 15 | 10 | 1 artillerie |
| Artillerie | Canon de campagne | `standardized_field_artillery` | 25 | 15 | 10 | 1 artillerie |
| Artillerie | Artillerie mobile | `horse_artillery` | 30 | 15 | 8 | 2 artilleries |

La progression ne rend donc aucun palier ancien plus puissant que son successeur. L’artillerie mobile conserve également son avantage marqué en létalité, dévastation et moral.

## Adaptation sémantique

- l’unité Tsar `combat_unit_type_musket_infantry` est raccordée au nœud du fork `regulated_small_arms` ;
- l’ancien `combat_unit_type_cannon_artillery` devient le palier **Bombarde**, accessible avec le tronc `organized_military_establishments` ;
- l’unité Tsar `combat_unit_type_improved_cannon_artillery` devient **Canon de campagne** et dépend de `standardized_field_artillery` ;
- l’artillerie mobile existante reste dépendante de `horse_artillery` ;
- les chaînes d’amélioration conduisent désormais explicitement au nouveau palier intermédiaire.

Les formations initiales n’ont pas été réécrites : leur identifiant `combat_unit_type_cannon_artillery` reste valide et désigne désormais la bombarde. Les pays possédant les technologies ultérieures pourront les améliorer normalement.

## Ressources visuelles

Les trois unités nouvellement ajoutées ou réinterprétées — infanterie à mousquet, bombarde et canon de campagne — utilisent provisoirement `gfx/error_deer.dds`. Aucun asset Tsar n’a été importé ou réemployé comme illustration définitive.

## Portée préservée

- aucune formation de départ modifiée ;
- aucune distribution technologique modifiée ;
- aucune autre statistique militaire modifiée ;
- aucune technologie créée ou déplacée ;
- aucun commit et aucun push.

## Validation statique

- accolades équilibrées dans `00_land_combat_unit_types.txt` ;
- chaque nouvel identifiant d’unité est défini exactement une fois ;
- ordre des définitions conforme aux paliers croissants attendus par le moteur ;
- chaque technologie de déblocage existe exactement une fois ;
- progression attaque/défense/moral contrôlée pour les deux chaînes ;
- localisations anglaise et française présentes et encodées en UTF-8 avec BOM ;
- `gfx/error_deer.dds` présent ;
- `git diff --check` ciblé réussi.

Le validateur historique `tech_tree_1776_wave3_validate.py` reste rouge sur ses anciennes valeurs figées (nombre de racines et d’arêtes, parent de `applied_mineralogy`, portes de pompes minières). Ces écarts concernent des évolutions ultérieures déjà présentes dans l’arbre et ne sont pas produits par cette phase, qui ne modifie aucun fichier de technologie ou de méthode de production.
