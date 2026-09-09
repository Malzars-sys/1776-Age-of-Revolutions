# TECH6C5A — Audit de fondation de la métallurgie non ferreuse

## 1. Résultat

**AUDIT RESULT: PASS.**

L'architecture recommandée est séquentielle et hybride :

1. implémenter d'abord `copper` comme bien marchand directement produit par une nouvelle `building_copper_mine`, sans bien intermédiaire « copper ore » ;
2. implémenter ensuite `aluminium` dans `building_non_ferrous_metallurgy_works`, bâtiment industriel distinct et tardif ;
3. ne créer ni `bauxite` ni `alumina` comme biens marchands.

Ce choix correspond à l'option D : deux architectures adaptées à deux chaînes matériellement différentes. Il évite aussi bien l'alchimie consistant à convertir le bien `lead` en cuivre que le PMG partagé qui contraindrait tous les niveaux d'un même bâtiment à une seule spécialisation.

```text
COPPER = IMPLEMENT_FIRST
ALUMINIUM = IMPLEMENT_AFTER_COPPER
BAUXITE = REJECT
ALUMINA = REJECT
```

## 2. Sources de vérité et périmètre

Ont été lus et comparés :

- le worktree local courant, autoritatif ;
- le canon Victoria 3 1.13.11 sous `C:/Games/Victoria 3/game` ;
- `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` ;
- `TECH_TREE_INDUSTRIAL_CHAINS.md` ;
- `docs/reports/technology/TECH_PRODUCTION_1700_1836_V1_1.md` (le chemin fourni sous `docs/research` n'existe pas ; le document a été retrouvé sous `docs/reports`) ;
- tous les rapports d'implémentation TECH6C présents sous `docs/reports/industry`.

Les recherches précédentes imposent une chaîne cuivre liée aux réseaux électriques, mais une chaîne aluminium seulement après Bayer, Hall-Héroult et électricité abondante. Elles rejettent déjà `alumina` comme bien mono-usage.

## 3. Audit actuel du mod et de la vanilla

Les recherches exactes `copper`, `aluminium`, `aluminum`, `bauxite` et `alumina` ne trouvent aucun bien, bâtiment, PM, PMG, ressource plafonnée, modificateur de bien, unité, modification navale ou input de construction correspondant.

| Fichier | Objet ID | Comportement actuel | Abstraction constatée |
|---|---|---|---|
| `common/technology/technologies/25_tech3a_naval.txt` | `copper_sheathing` | Technologie Militaire `era_4`, parent `scientific_naval_architecture`, sans enfant ni déblocage gameplay | Le cuivre existe nominalement mais sans bien ni demande. |
| `C:/Games/Victoria 3/game/common/history/buildings/11_east_asia.txt` | mines historiques d'Ashio et Besshi | Les deux mines de cuivre commentées sont créées comme `building_lead_mine` avec PM de plomb | Vanilla abstrait ici le cuivre par `lead`. |
| `common/history/treaties/00_historical_treaties.txt` | `treaty_name_nagasaki_trade` | L'article commenté « Copper trade » transfère `g:lead` en quantité 20 | Le commerce du cuivre est matériellement du plomb. |
| `C:/Games/Victoria 3/game/common/state_traits/12_oceania_traits.txt` | `state_trait_copper_coast` | `+0.1` throughput aux mines de plomb et de fer | La géologie cuivre est absorbée par `lead` et `iron`. |
| `C:/Games/Victoria 3/game/localization/english/inventions_l_english.yml` | `streamliners_desc` | Mention textuelle d'une construction en aluminium | Aucun objet gameplay `streamliners` ni input aluminium ne correspond. |
| `common/production_methods/01_industry.txt` | `pm_telephones` | `iron 20 + rubber 20 + lead 20 + tools 10 -> telephones 60` | `lead` porte une partie de l'abstraction des métaux conducteurs. |
| `common/production_methods/01_industry.txt` | `pm_electric_engines` | `steel 40 + electricity 30 -> engines 80` | Cuivre des bobinages entièrement abstrait. |
| `common/production_methods/01_industry.txt` | `pm_radios` | `electricity 50`, `telephones -20`, `radios +40` | Métaux conducteurs entièrement abstraits. |
| `common/production_methods/06_urban_center.txt` | `pm_early_power_plant` | `engines 4 + coal 5 + wood 5 -> electricity 25` | Cuivre des dynamos et réseaux entièrement abstrait. |
| `common/production_methods/01_industry.txt` | `pm_aeroplane_production` | `hardwood 4 + fabric 4`, puis conversion de 10 automobiles en 10 aeroplanes | Représente correctement l'aviation ancienne en bois et toile ; aucune place immédiate pour aluminium. |

Conclusion : vanilla possède une abstraction réelle du cuivre, mais elle devient incohérente dès que le cuivre est promu en bien Tier A. La conserver ferait de `lead` à la fois du plomb raffiné et un minerai universel. L'aluminium, lui, est entièrement immatériel dans le gameplay actuel.

## 4. Audit technologique

Le détail exhaustif est dans `TECH6C5A_NON_FERROUS_TECH_AUDIT.csv`.

### Cuivre

- `shaft_mining` (`era_1`) est le verrou sûr pour une mine de base ; il ouvre déjà toutes les mines minérales ordinaires.
- `applied_mineralogy` (`era_3`) convient à l'assayage et au dressing, mais ne doit pas retarder toute disponibilité du cuivre.
- `geological_surveying` (`era_6`) est un bon parent de spécialisation.
- `prospecting` ne convient pas : l'objet est un alias de compatibilité avec `can_research = no`.
- aucun équivalent de concentration/flottation des minerais n'existe. Une nouvelle technologie `ore_concentration`, proposée en `era_8` avec parents directs `geological_surveying` et `dynamite`, est justifiée pour un PM de montée en échelle ; elle n'est pas créée dans cet audit.
- `copper_sheathing` est visible et recherchable mais sans déblocage : elle doit fournir l'ancre de demande pré-électrique.

### Aluminium

Aucun équivalent de Bayer, Hall-Héroult, électrolyse de l'alumine ou métallurgie de l'aluminium n'existe. `electric_arc_process` est strictement un nœud sidérurgique et ne doit pas être recyclé.

La technologie proposée est :

```text
aluminium_metallurgy
ERA = era_10
PARENTS = electrical_capacitors + industrial_alkalis
UNLOCKS = building_non_ferrous_metallurgy_works + pm_hall_heroult_process
VISIBLE/RESEARCHABLE = yes
```

`electrical_capacitors` est le meilleur équivalent actuel de réseaux et électrochimie ; il dépend déjà d'`electrical_generation` et débloque la brine electrolysis. `industrial_alkalis` apporte la lignée caustique du procédé Bayer. `hydraulic_turbines` reste un facilitateur historique et un futur levier IA/hydroélectrique, pas un prérequis universel : l'aluminium exige de l'électricité abondante, pas nécessairement une seule source d'énergie.

## 5. Architecture cuivre

### Décision

Créer `building_copper_mine` et faire du bien `copper` l'abstraction agrégée du minerai extrait, concentré, fondu et livré au marché. Ne pas créer `copper_ore`.

La mine reprend le patron mécanique éprouvé :

```text
building_group = bg_mining
city_type = mine
required_construction = construction_cost_medium
terrain_manipulator = mining
ownership_type = self
ai_value = 1000
building_gate = shaft_mining
```

PMG recommandés :

1. `pmg_mining_equipment_building_copper_mine` : ladder extraction de base, atmosphérique, condensation, diesel ;
2. `pmg_explosives_building_copper_mine` : aucun explosif, nitroglycérine, dynamite ;
3. `pmg_steam_automation_building_copper_mine` ;
4. `pmg_train_automation_building_copper_mine` ;
5. `pmg_ore_concentration_building_copper_mine` : désactivé puis concentration/flottation sous `ore_concentration`.

Chaque nouveau PM sans DDS final propre devra utiliser `gfx/error_deer.dds`.

### Pourquoi pas `building_lead_mine`

L'abstraction vanilla est prouvée mais trop grossière pour un nouveau marché : tous les potentiels de plomb deviendraient implicitement des gisements de cuivre, la capacité serait partagée artificiellement, et les prix du plomb transmettraient les chocs électriques. Un bâtiment dédié coûte une distribution de ressource, mais produit une décision géographique lisible et n'ajoute aucun bien intermédiaire.

## 6. Architecture aluminium

### Options évaluées

| Option | Conclusion |
|---|---|
| `bauxite -> aluminium` directement dans Non-Ferrous Works | Rejetée : bon réalisme géographique, mais ajoute un bien mono-consommateur et une seconde lourde distribution mondiale. |
| minéral générique existant -> aluminium | Rejetée : `lead`, `iron` ou `sulfur` seraient des substitutions matériellement trompeuses. |
| mine de bauxite sans alumina marchand | Rejetée pour cette feuille de route : c'est la meilleure variante avec bauxite, mais son gain ne compense pas le coût de carte/IA avant preuve de besoin. |
| intrants industriels agrégés -> aluminium tardif | Retenue : le feedstock bauxite/alumine reste interne au bâtiment ; le marché représente uniquement l'aluminium. |

### Bâtiment et PM

```text
building_non_ferrous_metallurgy_works
building_group = bg_heavy_industry
city_type = city
required_construction = construction_cost_very_high
ownership_type = self
workforce = 5000 through base PM
pollution = 20 proposed
ai_value = inherited from bg_heavy_industry; no invented building-specific score
building_gate = aluminium_metallurgy

pmg_base_building_non_ferrous_metallurgy_works
  -> pm_hall_heroult_process (default; gate aluminium_metallurgy)
```

Le PM consomme explicitement beaucoup d'électricité et des `industrial_chemicals`. Le charbon représente notamment les anodes carbonées et l'énergie/thermique auxiliaire. La bauxite et l'alumine sont des coûts internes non marchands. Cette abstraction sacrifie la géographie du minerai, mais préserve la vraie barrière industrielle : chimie, capital et électricité à grande échelle.

Un bâtiment partagé cuivre/aluminium n'est pas recommandé. Un PMG de base unique empêcherait une même industrie régionale de produire les deux métaux simultanément, car le choix de PM s'applique à tous les niveaux du bâtiment. Deux PMG additifs permettraient la simultanéité, mais imposeraient PM désactivés, double comptage potentiel des emplois et recettes d'intrants difficiles à isoler. Les chaînes distinctes sont donc mécaniquement plus sûres.

## 7. Géographie des ressources

Le cuivre exige de nouveaux potentiels `building_copper_mine` dans `map_data/state_regions`. La matrice préliminaire contient 28 États et une échelle volontairement inférieure aux ressources communes :

```text
LOW = 8
MODEST = 16
MEDIUM = 24
HIGH = 36/48
VERY_HIGH = 60
```

Elle est fondée sur les districts historiques, les modèles USGS des porphyres et gisements stratiformes, la ceinture cuivreuse d'Afrique centrale, les données de Geoscience Australia et les propres abstractions vanilla d'Ashio/Besshi. Elle sert de noyau méthodologique, pas encore de distribution exhaustive des 675 États.

Références principales :

- USGS, `Where Does Copper Come From?` : https://pubs.usgs.gov/fs/2009/3031/FS2009-3031.pdf
- USGS, Global Porphyry Copper Deposits database : https://www.usgs.gov/data/a-global-database-porphyry-copper-deposits-and-prospects
- USGS, Global Copper Assessment : https://pubs.usgs.gov/publication/fs20143004
- USGS, Central African Copperbelt : https://www.usgs.gov/publications/descriptive-models-grade-tonnage-relations-and-databases-assessment-sediment-hosted

Aucune ressource bauxite n'est recommandée ; l'aluminium n'exige donc aucun edit de `state_regions` dans l'architecture retenue.

## 8. Matrice de demande aval

La matrice détaillée est dans `TECH6C5A_COPPER_ALUMINIUM_INTEGRATION_MATRIX.csv`.

### Cuivre

Cinq consommateurs sont proposés pour TECH6C5B :

1. nouveau PM optionnel de doublage en cuivre des chantiers navals ;
2. `pm_telephones` ;
3. `pm_electric_engines` ;
4. `pm_radios` ;
5. `pm_early_power_plant`.

Les éclairages urbains, trains électriques, munitions et automobiles restent différés jusqu'à simulation de l'échelle de demande. La construction et l'aciérie électrique sont rejetées comme consommateurs directs.

### Aluminium

Deux consommateurs structurants sont recommandés pour une phase ultérieure :

1. un nouveau PM d'avions entièrement métalliques, distinct de l'actuel PM bois/toile ;
2. un PM tardif de conducteurs de réseau en aluminium substituant une partie du cuivre.

L'automobile reste un essai différé. Les tanks, moteurs électriques et la simple mention localisée des streamliners sont rejetés comme ancrages directs.

## 9. Économie préliminaire

Prix courants lus dans les biens effectifs : `tools 40`, `lead 40`, `coal 30`, `electricity 30`, `industrial_chemicals 40`, `steel 50`, `engines 60`, `cement 40`.

Prix proposés :

```text
copper = 50
aluminium = 80
```

### Exemple cuivre — mine manuelle

```text
INPUT tools = 5       -> 5 x 40 = 200
OUTPUT copper = 15    -> 15 x 50 = 750
GROSS PRE-WAGE MARGIN = 550
WORKFORCE = 5000
```

Comparaisons : mine de plomb manuelle `5 tools -> 20 lead`, marge 600 ; carrière de calcaire `2 tools -> 30 limestone`, marge 520. Le cuivre est donc viable sans devenir une rente minière anormale. Les quantités des PM supérieurs doivent être calibrées en TECH6C5B.

### Exemple aluminium — Hall-Héroult agrégé

```text
INPUT industrial_chemicals = 20 -> 800
INPUT coal = 10                 -> 300
INPUT electricity = 50          -> 1500
TOTAL INPUT VALUE = 2600
OUTPUT aluminium = 40            -> 3200
GROSS PRE-WAGE MARGIN = 600
WORKFORCE = 5000
POLLUTION = 20
```

La marge égale celle du Lead Chamber Process (600), dépasse légèrement Portland Cement (550) et reste sous le Bessemer courant (1 200). L'électricité représente 57,7 % de la valeur des intrants : une économie sans production électrique abondante ne peut pas soutenir l'aluminium industriel.

## 10. Checklist de support des biens personnalisés

### `copper`

- `common/goods/` : définition du bien, prix 50, texture temporaire `gfx/error_deer.dds` ;
- `common/modifier_type_definitions/12_tech6c_custom_goods_modifier_types.txt` : input/output add/mult ;
- `gui/tech6c_goods_texticons.gui` : texticon ;
- localisations EN/FR du bien, bâtiment, PM/PMG et descriptions ;
- `localization/english/tech6c_goods_modifiers_l_english.yml` et équivalent français ;
- `common/buildings/` : `building_copper_mine` ;
- `common/production_method_groups/` : cinq PMG miniers recommandés ;
- `common/production_methods/` : ladder cuivre et consommateurs ;
- technologie existante `shaft_mining`, technologie nouvelle `ore_concentration` pour le palier avancé ;
- `map_data/state_regions/` : potentiels cuivre requis ;
- aucun besoin POP direct.

### `aluminium`

- `common/goods/` : définition du bien, prix 80, texture temporaire `gfx/error_deer.dds` ;
- mêmes quatre définitions de modificateurs et localisations EN/FR ;
- `gui/tech6c_goods_texticons.gui` : texticon ;
- `common/buildings/` : `building_non_ferrous_metallurgy_works` ;
- `common/production_method_groups/` : PMG de base ;
- `common/production_methods/` : Hall-Héroult et consommateurs tardifs ;
- `common/technology/technologies/` : nouvelle `aluminium_metallurgy` ;
- aucun `state_regions`, aucun bauxite, aucun alumina, aucun besoin POP direct ;
- tout nouveau PM sans DDS final propre : `gfx/error_deer.dds`.

## 11. Architecture et ordre de mise en œuvre

```text
shaft_mining
  -> building_copper_mine
      -> copper
          -> copper_sheathing PM
          -> telephones / electric engines / radios / early power

geological_surveying + dynamite
  -> ore_concentration
      -> advanced copper concentration PM

electrical_generation
  -> electrical_capacitors
industrial_alkalis -----------+
                              v
                    aluminium_metallurgy
                              |
                              v
          building_non_ferrous_metallurgy_works
                              |
                              v
                    pm_hall_heroult_process
                              |
                              v
                         aluminium
```

## 12. Portée exacte proposée pour TECH6C5B

**Titre : `TECH6C5B — Copper Foundation, Resource Distribution and Priority Demand Implementation`.**

Portée :

1. créer le bien `copper` à prix 50 et tout son support de modificateurs/texticons/localisation ;
2. créer `building_copper_mine` et son ladder minier standard, avec PM nouveaux en `gfx/error_deer.dds` tant qu'aucun DDS propre n'existe ;
3. finaliser une matrice mondiale cuivre à partir des 28 candidats, puis implémenter les potentiels approuvés ;
4. créer `ore_concentration` et le PM de concentration cuivre avancé ;
5. brancher exactement les cinq consommateurs `IMPLEMENT_NEXT` de la matrice ;
6. conserver aluminium, bauxite et alumina hors gameplay ;
7. valider définitions, recettes, IA, topologie, carte, localisation, parseur et démarrage économique du marché cuivre.

## 13. Validation de l'audit

- Aucun bien, bâtiment, PM, PMG, modificateur, asset ou `state_regions` cuivre/aluminium créé — PASS.
- Aucune topologie technologique changée par TECH6C5A — PASS.
- Aucun gameplay TECH6C existant modifié par TECH6C5A — PASS.
- Les seules modifications gameplay de la tâche appartiennent au correctif ciment préalable et sont documentées séparément — PASS.
- Matrice aval : 20 lignes, vocabulaire d'action limité à `IMPLEMENT_NEXT`, `DEFER`, `KEEP_UNCHANGED`, `REJECT` — PASS.
- Audit technologique : 17 lignes, dont deux technologies proposées mais non créées — PASS.
- Matrice ressource : 28 candidats cuivre, aucun candidat bauxite — PASS.
- Cohérence économique des exemples — PASS.
- `git diff --check` — PASS (seulement des avertissements informatifs LF/CRLF de Git sous Windows).
- Validation runtime — non exécutée et non revendiquée.

## 14. Recommandation explicite

```text
COPPER: IMPLEMENT
ALUMINIUM: IMPLEMENT
BAUXITE: REJECT
ALUMINA: REJECT

BUILDING ARCHITECTURE:
- building_copper_mine: dedicated capped-resource mine; direct copper output; no copper_ore good
- building_non_ferrous_metallurgy_works: late city heavy industry for aluminium; no copper PM in the same building

NEXT IMPLEMENTATION PHASE:
TECH6C5B — Copper Foundation, Resource Distribution and Priority Demand Implementation
```
