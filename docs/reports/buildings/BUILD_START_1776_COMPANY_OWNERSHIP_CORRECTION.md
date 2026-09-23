# BUILD START 1776 — Correction ciblée de propriété VOC / BIC / HBC

## Résultat

La passe restaure des actifs réellement possédés par les trois compagnies sans rouvrir la redistribution mondiale. La HBC conserve exactement cinq niveaux possédés. Au Bengale occidental, les actifs économiques privatisables sont désormais contrôlés depuis les quartiers d'affaires britanniques ; les plantations relèvent directement de la BIC.

| Compagnie | Niveaux possédés après correction |
|---|---:|
| VOC | 15 |
| BIC | 10 |
| HBC | 5 |

## Répartition

| Compagnie | Colonie | État | Bâtiment | Niveaux compagnie |
|---|---|---|---|---:|
| BIC | BIC | STATE_BIHAR | building_opium_plantation | 2 |
| BIC | BIC | STATE_WEST_BENGAL | building_opium_plantation | 2 |
| BIC | BIC | STATE_WEST_BENGAL | building_silk_plantation | 3 |
| BIC | BIC | STATE_WEST_BENGAL | building_sugar_plantation | 1 |
| BIC | BIC | STATE_WEST_BENGAL | building_tobacco_plantation | 2 |
| HBC | HBC | STATE_MANITOBA | building_fishing_wharf | 1 |
| HBC | HBC | STATE_MANITOBA | building_logging_camp | 1 |
| HBC | HBC | STATE_ONTARIO | building_logging_camp | 1 |
| HBC | HBC | STATE_QUEBEC | building_fishing_wharf | 2 |
| VOC | DEI | STATE_CENTRAL_JAVA | building_coffee_plantation | 1 |
| VOC | DEI | STATE_CENTRAL_JAVA | building_sugar_plantation | 1 |
| VOC | DEI | STATE_CEYLON | building_spice_plantation | 4 |
| VOC | DEI | STATE_EAST_JAVA | building_sugar_plantation | 1 |
| VOC | DEI | STATE_MOLUCCAS | building_spice_plantation | 4 |
| VOC | DEI | STATE_WEST_JAVA | building_coffee_plantation | 4 |

## Garde-fous

- Les propriétaires sont les puissances mères : NET pour la VOC, GBR pour la BIC et la HBC.
- Chaque bâtiment est admis par `building_types` ou `extension_building_types` de sa compagnie.
- Les huit niveaux d'épices VOC restent quatre aux Moluques et quatre à Ceylan, mais vivent désormais dans l'overlay mondial final afin d'éviter leur disparition au chargement.
- La HBC possède exactement cinq niveaux : deux exploitations forestières et trois pêcheries. Manitoba utilise 2,5 d'infrastructure, Ontario 1,5 et Québec 2,0, pour 3 de capacité de base dans chaque État : accès au marché conservé sans ajout de route.
- La BIC possède dix niveaux de plantations : quatre d'opium, trois de soie, deux de tabac et un de sucre. Quatre de ces niveaux sont les nouvelles plantations limitées du Bengale occidental.
- Au Bengale occidental, tous les bâtiments économiques privatisables hors plantations appartiennent à des quartiers d'affaires britanniques des Home Counties. L'administration et le port restent les seules exceptions publiques BIC, car ces catégories ne peuvent pas être transférées à des quartiers d'affaires.
- Le réseau routier du Bengale occidental passe de 13 à 15 niveaux : 45 d'infrastructure pour 43 utilisés après les quatre nouvelles plantations.
- Aucun niveau militaire ou naval et aucune Sérénissime ne sont modifiés.

Validation ciblée : **PASS**.
