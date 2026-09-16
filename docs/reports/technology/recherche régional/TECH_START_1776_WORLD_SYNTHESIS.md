# Synthèse mondiale — technologies initiales au 1er janvier 1776

## Verdict

Cette synthèse fusionne les 9 recherches régionales, les 9 matrices régionales et l’audit global Codex. Aucune nouvelle recherche historique n’est introduite dans les arbitrages, sauf une règle de synthèse conservatrice pour les lignes `REVIEW`.

- TAG globaux dans l’audit : **474**.
- TAG avec matrice régionale : **466**.
- TAG étudiés dans un Markdown régional mais sans ligne de matrice car leur tier est vide : **AIN, MND, SKH, SLW, ULT**.
- TAG non couverts par les livrables régionaux : **GAL, MLT, PPU**. Décision de synthèse : **aucun changement dans cette passe**.
- Relations pays-technologie dans les 9 matrices : **3877**.
- Décisions régionales : **KEEP=2045 / ADD=373 / REMOVE=651 / REVIEW=808**.
- Pays dont le set effectif change après synthèse : **311 / 474**.
- Relations technologiques de départ : **3421 → 3143** (**-278**).
- Après synthèse, **aucune technologie classée C ou D par l’audit global ne reste distribuée au départ**.

## Règle d’arbitrage des REVIEW

Les 808 lignes `REVIEW` ne sont pas transformées en nouvelle hypothèse historique :
- technologie actuellement présente : **conservée** (701 cas) ;
- technologie actuellement absente : **laissée absente** (107 cas).

Cette règle rend la synthèse intégralement implémentable par Codex sans forcer les incertitudes régionales.

## Stratégie d’implémentation synthétique

| Stratégie | TAG | Règle |
|---|---:|---|
| `KEEP_TIER_AND_PATCH` | 283 | Garder le tier actuel ; ajouter les `ADD` et retirer seulement les grants explicites `REMOVE`. |
| `EXPLICIT_SETUP` | 186 | Au moins une technologie provenant du tier doit être retirée : supprimer l’effet de tier et accorder exactement `Final_Technologies`. |
| `CHANGE_TIER_AND_PATCH` | 2 | BEL et SPC passent à `tier_4`, puis reçoivent les ajouts explicites calculés par la synthèse. |
| `KEEP_CURRENT_RESEARCH_GAP` | 3 | GAL, MLT, PPU : aucune modification faute de recherche régionale dédiée. |

Cette stratégie est volontairement plus minimale que certains `REPLACE_WITH_EXPLICIT_SETUP` régionaux : si aucune technologie issue du tier n’est marquée `REMOVE`, garder le tier et appliquer seulement les patches produit exactement le même set effectif tout en réduisant les modifications de fichiers.

## Résultats régionaux

| Région | TAG | TAG changés | ADD | REMOVE | Relations avant | Relations après |
|---|---:|---:|---:|---:|---:|---:|
| Europe occidentale | 10 | 10 | 72 | 9 | 147 | 210 |
| Europe centrale / germanique / Italie | 41 | 9 | 13 | 4 | 460 | 469 |
| Europe du Nord et de l’Est | 10 | 10 | 56 | 23 | 130 | 163 |
| Ottomans / Moyen-Orient / Caucase / Asie centrale | 49 | 43 | 13 | 115 | 506 | 404 |
| Asie du Sud | 59 | 57 | 30 | 165 | 585 | 450 |
| Asie orientale / Asie du Sud-Est | 45 | 32 | 38 | 47 | 377 | 368 |
| Amériques / Caraïbes | 57 | 38 | 15 | 151 | 558 | 422 |
| Afrique | 161 | 75 | 95 | 37 | 487 | 545 |
| Océanie / Pacifique | 39 | 37 | 41 | 100 | 147 | 88 |
| Non couvert | 3 | 0 | 0 | 0 | 24 | 24 |

## Technologies structurantes après synthèse

- `railways` : **0 pays** au départ (BRA perd l’attribution anachronique).
- `joint_stock_companies` : **0 pays** au départ (DEI perd l’attribution P0).
- `romanticism` : **0 pays** au départ (retrait des 7 grants explicites).
- `coke_smelting` : **1 pays** — GBR.
- `precision_boring` : **1 pays** — GBR.
- `mechanized_spinning` : **1 pays** — GBR.
- `industrial_canals` : **3 pays** — FRA, GBR, NET.
- `atmospheric_engine` : **6 pays** — AUS, BEL, BEO, FRA, GBR, SPC.
- `scientific_fortification_siegecraft` : **51 pays**.
- `state_dockyard_systems` : **28 pays**.

Le résultat global est donc beaucoup plus asymétrique : la vapeur/coke/mécanisation industrielle précoce deviennent très concentrés, tandis que les fortifications, arsenaux, administrations et traditions artisanales sont attribués selon leurs implantations régionales réelles.

## Grandes puissances et cas prioritaires

| TAG | Pays | Stratégie | ADD | REMOVE | Techs avant → après |
|---|---|---|---|---|---:|
| GBR | Great Britain | `KEEP_TIER_AND_PATCH` | advanced_crop_rotations; atmospheric_engine; coke_smelting; commercial_insurance_markets; enclosed_dock_systems; improved_agricultural_implements; industrial_canals; institutionalized_public_credit; institutionalized_scientific_exchange; mechanized_spinning; periodical_print_networks; precision_boring; scientific_fortification_siegecraft; scientific_naval_architecture; selective_breeding; state_dockyard_systems; stock_exchange; turnpike_road_networks | romanticism | 14 → 31 |
| FRA | France | `KEEP_TIER_AND_PATCH` | atmospheric_engine; enclosed_dock_systems; industrial_canals; institutionalized_scientific_exchange; periodical_print_networks; permanent_engineer_services; scientific_fortification_siegecraft; scientific_naval_architecture; state_dockyard_systems | romanticism | 16 → 24 |
| NET | Netherlands | `KEEP_TIER_AND_PATCH` | commercial_insurance_markets; enclosed_dock_systems; industrial_canals; institutionalized_public_credit; institutionalized_scientific_exchange; periodical_print_networks; scientific_naval_architecture; state_dockyard_systems; stock_exchange; traditional_papermaking | — | 13 → 23 |
| SPA | Spain | `KEEP_TIER_AND_PATCH` | applied_mineralogy; enclosed_dock_systems; institutionalized_scientific_exchange; periodical_print_networks; permanent_engineer_services; scientific_fortification_siegecraft; scientific_naval_architecture; state_dockyard_systems | — | 13 → 21 |
| POR | Portugal | `KEEP_TIER_AND_PATCH` | enclosed_dock_systems; institutionalized_scientific_exchange; periodical_print_networks; scientific_fortification_siegecraft; scientific_naval_architecture; state_dockyard_systems | — | 14 → 20 |
| AUS | Austria | `KEEP_TIER_AND_PATCH` | atmospheric_engine; scientific_fortification_siegecraft | romanticism | 14 → 15 |
| PRU | Prussia | `KEEP_TIER_AND_PATCH` | scientific_fortification_siegecraft | colonization; romanticism | 14 → 13 |
| RUS | Russia | `KEEP_TIER_AND_PATCH` | applied_mineralogy; armament_standardization_inspection; enclosed_dock_systems; institutionalized_scientific_exchange; periodical_print_networks; scientific_fortification_siegecraft; scientific_naval_architecture; specialized_technical_academies; state_dockyard_systems; systematic_cadastral_surveying; systematic_population_registration | systematic_legal_codification | 13 → 23 |
| TUR | Turkey | `KEEP_TIER_AND_PATCH` | scientific_fortification_siegecraft; scientific_naval_architecture; state_dockyard_systems; traditional_food_processing; variolation_networks | — | 12 → 17 |
| SWE | Sweden | `KEEP_TIER_AND_PATCH` | applied_mineralogy; enclosed_dock_systems; institutionalized_scientific_exchange; periodical_print_networks; scientific_fortification_siegecraft; scientific_naval_architecture; state_dockyard_systems; systematic_cadastral_surveying; systematic_population_registration | colonization | 13 → 21 |
| DEN | Denmark | `EXPLICIT_SETUP` | colonization; enclosed_dock_systems; institutionalized_scientific_exchange; periodical_print_networks; scientific_fortification_siegecraft; scientific_naval_architecture; state_dockyard_systems; systematic_cadastral_surveying; systematic_population_registration | shaft_mining | 12 → 20 |
| DENNOR | Denmark-Norway | `KEEP_TIER_AND_PATCH` | applied_mineralogy; enclosed_dock_systems; institutionalized_scientific_exchange; periodical_print_networks; scientific_fortification_siegecraft; scientific_naval_architecture; state_dockyard_systems; systematic_cadastral_surveying; systematic_population_registration | — | 13 → 22 |
| PLC | Poland-Lithuania | `KEEP_TIER_AND_PATCH` | institutionalized_scientific_exchange; organized_elementary_schooling; periodical_print_networks; scientific_fortification_siegecraft; specialized_technical_academies | — | 11 → 16 |
| USA | America | `EXPLICIT_SETUP` | medical_degrees; periodical_print_networks | romanticism; shaft_mining | 14 → 14 |
| CHI | China | `KEEP_TIER_AND_PATCH` | regulated_small_arms; scientific_fortification_siegecraft; state_dockyard_systems; systematic_population_registration; traditional_papermaking | — | 8 → 13 |
| JAP | Japan | `EXPLICIT_SETUP` | scientific_fortification_siegecraft; systematic_population_registration; traditional_papermaking | light_infantry_tactics | 14 → 16 |
| DEI | East Indies | `KEEP_TIER_AND_PATCH` | enclosed_dock_systems; scientific_fortification_siegecraft; scientific_naval_architecture; state_dockyard_systems | joint_stock_companies | 13 → 16 |
| BIC | East India | `KEEP_TIER_AND_PATCH` | enclosed_dock_systems; military_topographic_surveying; scientific_fortification_siegecraft; state_dockyard_systems; traditional_food_processing | — | 13 → 18 |
| MYS | Mysore | `KEEP_TIER_AND_PATCH` | distillation; international_relations; light_infantry_tactics; regulated_small_arms; scientific_fortification_siegecraft; standardized_field_artillery; traditional_food_processing | — | 6 → 13 |
| MARATH | Maratha Confederacy | `KEEP_TIER_AND_PATCH` | scientific_fortification_siegecraft; traditional_food_processing; traditional_papermaking | — | 8 → 11 |
| MUG | Hindustan | `EXPLICIT_SETUP` | international_relations; traditional_food_processing; traditional_papermaking | shaft_mining | 6 → 8 |
| PER | Persia | `EXPLICIT_SETUP` | traditional_food_processing | standardized_field_artillery; state_dockyard_systems | 12 → 11 |
| BRA | Brunswick | `KEEP_TIER_AND_PATCH` | — | railways | 12 → 11 |

## Prérequis

Les relations avec prérequis directs manquants passent de **578** à **434**. La synthèse en résout **208** mais en introduit volontairement **64** lorsque la recherche régionale justifie l’enfant sans justifier le chemin technologique européen encodé par l’arbre.

Parents encore le plus souvent absents après synthèse :
- `institutionalized_scientific_exchange` : 248 relations.
- `periodical_print_networks` : 243 relations.
- `scientific_fortification_siegecraft` : 125 relations.
- `regulated_small_arms` : 22 relations.
- `organized_forestry` : 13 relations.
- `institutionalized_public_credit` : 5 relations.
- `coke_smelting` : 5 relations.
- `selective_breeding` : 2 relations.
- `turnpike_road_networks` : 2 relations.
- `permanent_engineer_services` : 1 relations.

**Règle impérative pour Codex : ne jamais auto-ajouter un parent uniquement pour fermer le graphe.** Le fichier `TECH_START_1776_WORLD_PREREQUISITE_DEBT.csv` constitue la dette attendue après implémentation.

## Cas spéciaux

- **BHV** possède deux fichiers historiques actifs (`tier_4;tier_5`) : le setup technologique final doit être rendu unique sans supprimer du contenu historique non technologique.
- **ORG** possède deux fichiers historiques actifs (`tier_2;tier_4`) : même règle.
- **BEL** : `tier_1 → tier_4`; les capacités tier_1 historiquement conservées mais absentes de tier_4 sont réajoutées explicitement.
- **SPC** : `tier_3 → tier_4`; les capacités espagnoles attestées sont réajoutées explicitement.
- **GAL, MLT, PPU** : non couverts par les recherches régionales ; aucune modification dans cette passe.

## Validation attendue

Après implémentation, un audit automatique doit reconstruire les technologies effectives de départ de chaque TAG et comparer exactement le résultat à `Final_Technologies` dans `TECH_START_1776_WORLD_COUNTRY_PLAN.csv`. Toute divergence est une erreur d’implémentation.

Contrôles globaux minimaux :
- aucun pays avec `railways`, `joint_stock_companies` ou `romanticism` au 1776-01-01 ;
- `coke_smelting`, `precision_boring`, `mechanized_spinning` seulement selon les listes ci-dessus ;
- aucune technologie C/D dans les sets finaux ;
- les 434 dettes de prérequis du CSV de dette sont tolérées et ne doivent pas être « réparées » automatiquement ;
- TECH6D et TECH7A ne doivent pas être modifiés.

## Fichiers de synthèse

- `TECH_START_1776_WORLD_MATRIX.csv` : fusion ligne par ligne des décisions régionales, avec résolution conservatrice des REVIEW.
- `TECH_START_1776_WORLD_COUNTRY_PLAN.csv` : plan canonique des 474 TAG, stratégies d’implémentation et `Final_Technologies` exactes.
- `TECH_START_1776_WORLD_PREREQUISITE_DEBT.csv` : prérequis directs volontairement manquants après synthèse.
- `TECH_START_1776_CODEX_IMPLEMENTATION_PROMPT.md` : consigne finale d’implémentation.