# TECH-0 — Vanilla Research Mechanics & Era Scalability Audit

Audit de code uniquement. Aucun fichier gameplay n'a été modifié et aucune proposition d'arbre historique n'est faite ici.

## Résultat canonique

```text
PHASE = TECH-0
AUDIT_STATUS = PASS_WITH_ENGINE_UNKNOWNS

GAME_VERSION = 1.13.9 (Matcha)
GAME_BRANCH = release/1.13.9
GAME_REVISION = afea32b87c002fe0621f2f732d60a80ba914c14e
VANILLA_ROOT = C:\Games\Victoria 3\game
VERSION_PROOF_SOURCE = C:\Games\Victoria 3\caligula_branch.txt:1;
                       C:\Games\Victoria 3\caligula_rev.txt:1;
                       C:\Games\Victoria 3\clausewitz_branch.txt:1;
                       C:\Games\Victoria 3\launcher\launcher-settings.json:5-6

VANILLA_TECHNOLOGIES_TOTAL = 179
PRODUCTION_TECHS = 57
MILITARY_TECHS = 58
SOCIETY_TECHS = 64
VANILLA_TECH_ERAS = era_1, era_2, era_3, era_4, era_5
ERA_COUNT = 5
ERA_IMPLEMENTATION = PARTIALLY_HARDCODED

TEN_TO_FOURTEEN_ERAS_SUPPORTED = PROBABLY

BASE_INNOVATION = 50/week
INNOVATION_CAP_FORMULA = 50 + 150 * incorporated_literacy_rate + other cap additions
LITERACY_EFFECT = cap +150*L and base spread +75*L; no direct raw-innovation output
OVER_CAP_BEHAVIOR = unspent innovation feeds spread at +0.2 spread per unspent point
TECH_SPREAD_FORMULA = exposed base: 25 + 75*L + 0.2*unspent_innovation + additive modifiers;
                      then global/category multipliers and engine randomization

AI_NEW_TECH_DEFAULT_BEHAVIOR = UNKNOWN_WITHOUT_EXPLICIT_AI_WEIGHT
AI_NEW_ERA_BEHAVIOR = PROBABLY_GENERIC_BUT_NOT_RUNTIME_PROVEN

VANILLA_TOTAL_RAW_TECH_COST = 2,157,500

TECH_UI_SCALABILITY_RISK = HIGH
ERA_SCALABILITY_RISK = MEDIUM_HIGH
AI_SCALABILITY_RISK = MEDIUM
```

Le verdict `PROBABLY` est volontaire. Les définitions d'ères, le graphe et les badges sont alimentés par des données, mais aucun fichier accessible ne prouve une limite moteur supérieure à cinq, et l'interface vanilla n'a pas été testée avec 10–14 ères.

## Standard de preuve

- `VERIFIED_FROM_VANILLA_1_13_9` : valeur ou comportement explicitement décrit dans les scripts/defines/localisations de la copie 1.13.9 prouvée ci-dessus.
- `VERIFIED_FROM_ENGINE_GUI_SCRIPT` : interface moteur ou modèle de données explicitement appelé depuis un fichier GUI/localisation, sans accès à son implémentation C++.
- `INFERRED` : conclusion nécessaire ou très probable, mais non entièrement exposée par les scripts.
- `UNKNOWN` : détail non prouvable depuis les fichiers accessibles et sans lancement du jeu.

Les numéros de ligne sont ceux de l'installation locale auditée. Ils changeront avec une autre version du jeu.

## 1. Provenance vanilla

| Preuve | Ligne | Valeur observée | Classe |
|---|---:|---|---|
| `C:\Games\Victoria 3\caligula_branch.txt` | 1 | `release/1.13.9` | VERIFIED_FROM_VANILLA_1_13_9 |
| `C:\Games\Victoria 3\caligula_rev.txt` | 1 | `afea32b87c002fe0621f2f732d60a80ba914c14e` | VERIFIED_FROM_VANILLA_1_13_9 |
| `C:\Games\Victoria 3\clausewitz_branch.txt` | 1 | `caligula/release/1.13.9` | VERIFIED_FROM_VANILLA_1_13_9 |
| `C:\Games\Victoria 3\launcher\launcher-settings.json` | 5–6 | `1.13.9 (Matcha)` / `1.13.9` | VERIFIED_FROM_VANILLA_1_13_9 |
| `C:\Games\Victoria 3\v1.13.9.xxh128` | fichier | marqueur de version présent | VERIFIED_FROM_VANILLA_1_13_9 |

La comparaison vanilla peut donc être menée : la version cible est exactement prouvée.

## 2. Architecture des fichiers

### Noyau technologie et ères

- `common/technology/technologies/10_production.txt`
- `common/technology/technologies/20_military.txt`
- `common/technology/technologies/30_society.txt`
- `common/technology/eras/00_eras.txt`
- `common/technology/eras/eras.md`

Les 179 objets ont tous `era`, `texture`, `category` et `ai_weight`; 172 ont `unlocking_technologies`, 99 un `modifier`, 6 un `on_researched`, un `should_update_map`, et un seul un override `can_research = no` (`sericulture`). L'inventaire ligne par ligne est dans `TECH_0_VANILLA_TECHNOLOGY_INVENTORY.csv`.

### Defines et types de modificateurs

- `common/defines/00_defines.txt` : spread aléatoire et pénalité inter-ères.
- `common/defines/00_ai.txt` : sélection technologique IA et investissement innovation.
- `common/defines/00_interfaces.txt` : position/zoom du graphe.
- `common/static_modifiers/00_code_static_modifiers.txt` : base, literacy et excès d'innovation.
- `common/modifier_type_definitions/00_modifier_types.txt`
- `common/modifier_type_definitions/99_todo_sort_into_other_files.txt`
- `common/modifier_type_definitions/01_building_modifier_types.txt`

### Universités, alphabétisation et systèmes externes

- `common/buildings/07_government.txt`
- `common/production_method_groups/07_government.txt`
- `common/production_methods/07_government.txt`
- `common/institutions/00_institutions.txt`
- `common/laws/00_education_system.txt`
- `common/power_bloc_principles/00_power_bloc_principles.txt`
- `common/diplomatic_actions/40_subjects_knowledge_sharing.txt`
- `common/treaty_articles/12_military_assistance.txt`
- `common/country_ranks/00_country_ranks.txt`
- `common/laws/00_free_speech.txt`, `00_trade_policy.txt`, `00_economic_system.txt`
- `common/interest_group_traits/00_armed_forces_traits.txt`, `00_industrialists_traits.txt`, `00_intelligentsia_traits.txt`, `00_devout_traits.txt`, `00_rural_folk_traits.txt`
- `common/character_traits/personality_traits.txt`
- `common/company_types/*.txt`
- `common/static_modifiers/*.txt`

Un scan exhaustif des clés directement liées à la recherche trouve 165 affectations, avec ID propriétaire, valeur et ligne, dans `TECH_0_RESEARCH_MODIFIER_INVENTORY.csv`. Un second inventaire contient les 49 affectations d'accès à l'éducation, de croissance de l'alphabétisation et de ferveur éducative indirectement pertinentes : `TECH_0_LITERACY_EDUCATION_INDIRECT_INVENTORY.csv`.

### Démarrage, effets et progression fixe

- `common/scripted_effects/00_starting_inventions.txt` : les lignes 5 et 30 accordent `era_1`; les autres tiers accordent des technologies individuellement.
- `common/scripted_effects/00_chris_scripted_effects.txt:366` : wrapper paramétré d'ajout de technologie.
- `common/effect_localization/00_country_effects_loc.txt` et `common/trigger_localization/00_trigger_localization.txt` : présentation des effets/triggers.
- 65 sites gameplay actifs `add_technology_progress` existent dans 25 fichiers d'événements. Ils doivent être revalidés si coûts ou IDs changent. La liste des fichiers figure dans la section « adaptation ».

Aucun `script_value` ni `scripted_trigger` ne calcule le coût, le cap, l'innovation ou le spread. Ces calculs résident dans les modificateurs statiques et le moteur.

### Interface, localisation et assets

- `gui/tech_tree.gui`
- `localization/english/inventions_l_english.yml`
- `localization/english/interfaces_l_english.yml`
- `localization/english/concepts_l_english.yml`
- `localization/english/modifiers_l_english.yml`
- équivalents dans les autres dossiers de langue
- `gfx/interface/icons/invention_icons/*.dds`
- `gfx/interface/tech_tree/*.dds`
- `gfx/interface/illustrations/tech_tree/*.dds`

Le fork ne possède actuellement aucun override local de `common/technology`, `gui/tech_tree.gui`, `inventions_l_*` ou `gfx/interface/icons/invention_icons`; il hérite donc de la structure vanilla au moment de cet audit.

## 3. Ères vanilla

Source : `common/technology/eras/00_eras.txt:1-21`.

| ERA_ID | Ordre | Affichage réellement disponible | Coût de base | Champs date | Modificateurs | Règles particulières |
|---|---:|---|---:|---|---|---|
| `era_1` | 1 | numéro moteur 1; prose « Era I » | 7,500 | aucun; commentaire `Pre-1836` | aucun | première ère |
| `era_2` | 2 | numéro moteur 2; prose « Era II » | 10,000 | aucun; commentaire `1836-1861` | aucun | pénalité si techs antérieures manquantes |
| `era_3` | 3 | numéro moteur 3; prose « Era III » | 12,500 | aucun; commentaire `1862-1886` | aucun | idem |
| `era_4` | 4 | numéro moteur 4; prose « Era IV » | 15,000 | aucun; commentaire `1887-1911` | aucun | idem |
| `era_5` | 5 | numéro moteur 5; prose « Era V » | 17,500 | aucun; commentaire `1911-1936` | aucun | idem |

`eras.md:1-6` documente les champs facultatifs `start_date`, `end_date`, `icon` et `technology_cost`. Vanilla ne renseigne que `technology_cost`. Les dates ci-dessus ne sont donc pas des barrières mécaniques : ce sont des commentaires, complétés par la prose localisée de `concepts_l_english.yml:1832-1836`.

Il n'existe aucune clé de localisation `era_1` à `era_5` pour un nom propre. L'UI appelle `[Technology.GetEra.GetNumber]` via `TECHNOLOGY_TYPE_DESCRIPTION` (`interfaces_l_english.yml:7968`) et affiche le numéro dans un badge (`gui/tech_tree.gui:1165-1184`).

Conclusion : la base d'ères est `DATA_DRIVEN`, mais l'écosystème total est `PARTIALLY_HARDCODED` à cause de la prose cinq-ères, des séparateurs graphiques fixes et de comportements moteur non exposés.

## 4. Scalabilité à 10–14 ères

### Preuves favorables

- `eras.md` décrit des objets nommés, pas une enum de cinq valeurs (`VERIFIED_FROM_VANILLA_1_13_9`).
- Les technologies référencent leur ère par ID (`era = era_n`) (`VERIFIED_FROM_VANILLA_1_13_9`).
- Le GUI obtient les nœuds et lignes depuis `TechTreePanel.Get*TechTreeItems/Lines`, puis les positions depuis `TechTreeItem.GetPosition` et les splines depuis `TechTreeLine.GetPointsInContainer` (`gui/tech_tree.gui:503-608, 749-763, 1294-1320`) (`VERIFIED_FROM_ENGINE_GUI_SCRIPT`).
- Le badge demande `Era.GetNumber`, sans liste GUI explicite de cinq IDs (`gui/tech_tree.gui:1165-1184`) (`VERIFIED_FROM_ENGINE_GUI_SCRIPT`).
- La formule de pénalité parle de « number of eras between the techs », donc l'écart ordinal est traité génériquement (`common/defines/00_defines.txt:1779-1784`) (`VERIFIED_FROM_VANILLA_1_13_9`).

### Limites et risques

- Aucun define n'annonce un nombre maximal d'ères (`UNKNOWN` pour la limite C++).
- Le concept localisé décrit explicitement les cinq ères I–V (`concepts_l_english.yml:1832-1836`).
- Chaque catégorie a exactement trois bandes décoratives avec positions/hauteurs fixes (`gui/tech_tree.gui:517-533, 552-568, 587-603`). Elles ne sont pas générées par ère.
- Le zoom minimal est `0.20`; les nœuds font `465 x 150`; les marges du graphe sont fixes (`gui/tech_tree.gui:636-690, 757-763`). Dix à quatorze ères augmenteront fortement la hauteur/largeur et les déplacements.
- Le badge fait `40 x 40` avec une grande police. Les nombres 10–14 ne sont pas validés visuellement.
- La pénalité inter-ères croît avec le nombre de technologies manquantes multiplié par la distance d'ère. Multiplier les ères sans recalibrage peut produire des pénalités extrêmes, même si le moteur charge correctement les objets.
- Aucune validation runtime ou benchmark GUI 10–14 ères n'est autorisée dans TECH-0.

```text
TEN_TO_FOURTEEN_ERAS_SUPPORTED = PROBABLY
```

Cela signifie « architecture vraisemblablement générique, mais prototype/runtime obligatoire avant adoption », pas « support garanti ».

## 5. Modèle de coût technologique

### Partie vérifiée

Pour une technologie cible `t`, dans la catégorie `k`, d'indice d'ère `e` :

```text
C_e = technology_cost de l'ère e
U_j = nombre de technologies non recherchées de la même catégorie k dans l'ère antérieure j
D_j = e - j

AHEAD_PENALTY_RAW = 0.25 * C_e * SUM_j(U_j * D_j), pour tout j < e
DISPLAYED_COST = C_e + pénalité d'avance effective
```

Preuves :

- `technology_cost` est défini uniquement par ère (`00_eras.txt:3-20`).
- `TECH_AHEAD_OF_TIME_PENALTY_FACTOR = 0.25` et le commentaire définit le facteur par technologie antérieure manquante, dans la même catégorie, multiplié par la distance d'ères (`00_defines.txt:1779-1782`).
- L'UI sépare coût de base d'ère et pénalité pour technologies non recherchées des ères précédentes (`interfaces_l_english.yml:8026-8035`).

### Modificateur de pénalité

`country_ahead_of_time_research_penalty_mult` est décrit comme une hausse/baisse de la pénalité (`modifier_type_definitions/00_modifier_types.txt:1469-1476`; `modifiers_l_english.yml:2188-2189`). `principle_advanced_research_2` et `_3` lui donnent chacun `-0.05` (`power_bloc_principles/00_power_bloc_principles.txt:354,382`).

L'application multiplicative attendue est :

```text
AHEAD_PENALTY_EFFECTIVE = AHEAD_PENALTY_RAW * (1 + sum(country_ahead_of_time_research_penalty_mult))
```

Cette ligne est `INFERRED` à partir de la convention `_mult` et de la description; l'ordre exact de clamp/stack est moteur et n'est pas exposé.

### Facteurs absents

Dans les 179 définitions et les defines accessibles :

- contribution de catégorie au coût : aucune;
- contribution d'année/date : aucune;
- « ahead of calendar date » : aucun; la pénalité concerne les lacunes des ères précédentes;
- réduction explicite « behind time » : aucune;
- modification du coût par les prérequis : aucune; ils contrôlent l'accès/le graphe;
- difficulté : aucun modificateur direct de coût trouvé;
- coût individuel par technologie : aucun champ;
- vitesse de recherche : elle modifie le progrès dépensé, pas `Technology.GetCost` (`modifiers_l_english.yml:2184-2185`; `interfaces_l_english.yml:8051-8052`).

Le coût final exact, y compris arrondi/clamp moteur et stacking du modificateur de pénalité, reste `UNKNOWN` au-delà de la formule exposée.

## 6. Innovation, cap, literacy et universités

### Valeurs de base

`common/static_modifiers/00_code_static_modifiers.txt:1-10` précise que ces objets sont utilisés par le code et donne :

```text
country_weekly_innovation_add = 50
country_weekly_innovation_max_add = 50
country_tech_spread_add = 25
```

### Cap et alphabétisation

`country_literacy_rate` est explicitement mis à l'échelle par le taux d'alphabétisation du pays (`00_code_static_modifiers.txt:824-829`) :

```text
INNOVATION_CAP = 50 + 150 * L + autres country_weekly_innovation_max_add
BASE_TECH_SPREAD = 25 + 75 * L + autres country_tech_spread_add
```

`L` est le taux d'alphabétisation des États incorporés : l'UI emploie `GetIncorporatedLiteracyRate` pour le cap et le spread (`interfaces_l_english.yml:1158-1161`). Donc, hors autres bonus : cap 50 à 0 % et 200 à 100 %.

L'alphabétisation ne produit pas directement de raw innovation dans le script. Elle augmente le cap et le spread.

### Universités

Le bâtiment est `building_university`, groupe `bg_technology`, dans `common/buildings/07_government.txt:35-53`. Ses méthodes de base sont dans `production_method_groups/07_government.txt:45-63`.

| PM | Innovation par niveau à plein emploi | Emplois de base par niveau | Déverrouillage | Source |
|---|---:|---|---|---|
| `pm_scholastic_education` | +1.0/semaine | 250 clerks + 250 laborers | aucun | `production_methods/07_government.txt:175-200` |
| `pm_philosophy_department` | +1.5/semaine | 250 clerks + 250 laborers | `dialectics` | lignes 202-231 |
| `pm_analytical_philosophy_department` | +2.0/semaine | 200 clerks + 200 laborers + 100 academics | `analytical_philosophy` | lignes 233-263 |

L'ownership ajoute soit 500 academics (`pm_secular_academia`, lignes 265-277), soit 250 clergymen + 250 academics (`pm_religious_academia`, lignes 279-293).

L'innovation est dans un bloc `country_modifiers = { workforce_scaled = { ... } }`. Le niveau seul ne suffit donc pas : l'emploi réel de l'université module la production. La production n'est pas attachée à un job particulier; clerks, laborers, academics et clergymen contribuent indirectement au taux d'emploi global du bâtiment. La fonction moteur exacte de `workforce_scaled` n'est pas exposée; les valeurs du tableau sont les maxima par niveau à plein emploi.

### Innovation brute et progrès actif

Pseudo-formule, avec séparation de preuve :

```text
RAW_INNOVATION_ADD = 50 + somme des outputs universitaires workforce_scaled
                     + autres country_weekly_innovation_add
RAW_INNOVATION = RAW_INNOVATION_ADD affecté par country_weekly_innovation_mult

ACTIVE_INVESTMENT = min(RAW_INNOVATION, INNOVATION_CAP), si une recherche est active
ACTIVE_PROGRESS = ACTIVE_INVESTMENT affecté par les research-speed multipliers
```

Les clés et leur objet sont vérifiés (`modifier_type_definitions/00_modifier_types.txt:1409-1467`), tout comme le fait que la research speed agit lorsque l'innovation est dépensée (`modifiers_l_english.yml:2184-2187`). L'ordre exact des sommes, multiplicateurs, clamps et arrondis est `UNKNOWN` car moteur.

### Au-dessus du cap

`excess_innovation` est mis à l'échelle par le nombre de points excédentaires et donne `country_tech_spread_add = 0.2` (`00_code_static_modifiers.txt:831-835`). L'UI confirme que l'innovation non dépensée à cause du cap ou de l'absence de recherche augmente le spread (`interfaces_l_english.yml:7961-7962`; `concepts_l_english.yml:1825-1826`).

```text
TECH_SPREAD_FROM_EXCESS_INNOVATION = 0.2 * unspent_innovation
```

Une innovation supérieure au cap n'est donc pas investie intégralement dans la recherche active; 20 % de l'excès est converti en ajout de spread.

## 7. Technology spread

### Formule exposée

```text
SPREAD_ADD_BASE = 25
SPREAD_FROM_LITERACY = 75 * incorporated_literacy_rate
SPREAD_FROM_EXCESS = 0.2 * unspent_innovation
SPREAD_FROM_UNIVERSITIES_DIRECT = 0

SPREAD_STAT = SPREAD_ADD_BASE + SPREAD_FROM_LITERACY + SPREAD_FROM_EXCESS
              + autres country_tech_spread_add

WEEKLY_SPREAD_FOR_CATEGORY = SPREAD_STAT affecté par country_tech_spread_mult
                             et country_<category>_tech_spread_mult,
                             puis randomisé par le moteur
```

Le stacking exact des multiplicateurs et tout cap interne restent `UNKNOWN`. L'UI possède une ligne `TECH_SPREAD_MAX_CAP` (`interfaces_l_english.yml:8057`), mais aucune valeur de cap n'est exposée dans les defines inspectés.

### Randomisation

`TECH_SPREAD_RANDOM_RANGE = 0.5` (`common/defines/00_defines.txt:1780`) et l'UI affiche un minimum/maximum hebdomadaire (`interfaces_l_english.yml:8053-8054`). La distribution exacte — uniforme ou autre, et interprétation précise de `0.5` — n'est pas exposée. Il serait incorrect d'affirmer comme fait vérifié que l'intervalle est exactement 50–150 % sans runtime ou code moteur.

### Nombre, sélection et éligibilité

`concepts_l_english.yml:1829-1830` donne les règles suivantes (`VERIFIED_FROM_ENGINE_GUI_SCRIPT`) :

- une technologie non acquise est en spread dans chacune des trois catégories;
- maximum fonctionnel annoncé : trois technologies simultanées, une Production, une Military, une Society;
- une technologie ne peut se répandre que si au moins un autre pays l'a acquise;
- les technologies anciennes sont de fait plus susceptibles d'être disponibles au spread, parce que davantage de pays les possèdent.

L'algorithme exact de sélection parmi les technologies éligibles, la durée de conservation d'une cible, les restrictions précises de prérequis/ère et le comportement en cas d'absence de candidat ne sont pas scriptés : `UNKNOWN`.

L'UI expose des contributions par voisin et par pacte (`interfaces_l_english.yml:8055-8056`). Les valeurs internes de chaque source et leur cap ne sont pas définis dans les scripts accessibles.

### Pays très en retard ou très innovant

- Très en retard : il bénéficie toujours du socle literacy/spread et a statistiquement davantage de technologies déjà connues ailleurs éligibles; aucune remise de coût « behind time » n'a été trouvée.
- Très innovant : son investissement actif reste plafonné; l'excès alimente le spread à 0.2 par point. Le spread continue sur trois catégories au maximum annoncé.

La seconde phrase est vérifiée pour la conversion et le nombre de catégories; toute affirmation sur la technologie précise sélectionnée reste inconnue.

## 8. Power blocs et autres bonus

### Power bloc principles

Source : `common/power_bloc_principles/00_power_bloc_principles.txt`.

| ID | Ligne | Effet exposé |
|---|---:|---|
| `principle_advanced_research_1` | 314 | global tech spread +5 % |
| `principle_advanced_research_2` | 351, 354 | global tech spread +5 %; ahead penalty -5 % |
| `principle_advanced_research_3` | 379, 382, 385 | global tech spread +5 %; ahead penalty -5 %; innovation cap +5 |
| `principle_shared_canon_1` | 1741 | Society spread +10 % |
| `principle_shared_canon_2` | 1762 | Society spread +10 % |
| `principle_shared_canon_3` | 1779 | Society spread +10 % |

Le tableau rapporte chaque objet tel qu'écrit. Le cumul entre niveaux dépend du système de principes du power bloc et n'est pas réinterprété ici.

Le groupe `pmg_principle_freedom_of_movement_3` est attaché aux universités (`buildings/07_government.txt:47-51`), mais sa PM (`production_methods/06_urban_center.txt:318-332`) donne du migration pull, pas de recherche. Elle n'ajoute donc aucun bonus direct d'innovation.

### Pactes, statuts, lois et traits persistants

- `da_knowledge_sharing` : donneur -10 % spread, bénéficiaire +25 % (`diplomatic_actions/40_subjects_knowledge_sharing.txt:49-53`).
- `military_assistance` : cible +10 % Military spread (`treaty_articles/12_military_assistance.txt:35-40`).
- rangs non reconnus : major -15 %, regional -20 %, autre -25 % global spread (`country_ranks/00_country_ranks.txt:174,209,241`).
- `law_outlawed_dissent` -15 %, `law_censorship` -10 %, `law_protected_speech` +25 % global spread (`laws/00_free_speech.txt:15,44,97`).
- `law_isolationism` -15 %, `law_canton_system` -10 %, `law_sakoku` -20 % global spread (`laws/00_trade_policy.txt:198,254,313`).
- `law_industry_banned` : Production research speed -25 % et Production spread -25 % (`laws/00_economic_system.txt:320-321`).
- `law_terakoya` : global research speed -10 % (`laws/00_education_system.txt:285`).
- IG traits : `veteran_consultation` et `self_strengthening` +10 % Military research; `engines_of_progress` +10 % Production; `avant_garde` +10 % Society; `traditsye` et `old_ways` -10 % spread.
- personnalité `innovative` : +10 % global spread (`character_traits/personality_traits.txt:711`).

### Entreprises, événements et throughput universitaire

Les 23 affectations de compagnies et les 108 affectations de static modifiers sont trop nombreuses pour être dupliquées sans risque de transcription; l'annexe CSV canonique fournit leurs IDs, valeurs, chemins et lignes exacts. Elle comprend notamment les 17 `building_university_throughput_add`.

`building_university_throughput_add` est un modificateur de throughput du bâtiment (`modifier_type_definitions/01_building_modifier_types.txt:2176`). Son effet exact sur le `country_modifier` `workforce_scaled` d'innovation n'est pas explicité dans les scripts : il est inventorié comme interaction indirecte, mais le coefficient final sur l'innovation est `UNKNOWN` sans moteur/runtime.

### Éducation et literacy indirectes

`institution_schools` est défini dans `common/institutions/00_institutions.txt:26-29`; ses valeurs viennent des lois dans `common/laws/00_education_system.txt`. Exemples :

- institution religieuse : +0.10 education access par niveau (`00_education_system.txt:57-62`);
- système fondé sur la richesse : +0.005 education access par richesse et niveau (`:182-186`);
- `law_terakoya` : +0.25 access et +0.20 peasants access, avec -10 % research speed (`:283-288`);
- autre institution du fichier : +0.125 access et +0.0001 literacy growth (`:315-321`);
- décret d'éducation : +0.25 access (`common/decrees/00_decree.txt:222-225`).

Ces effets modifient la literacy dans le temps, qui modifie ensuite cap et spread. Les 49 affectations exactes sont dans l'annexe education/literacy.

## 9. Recherche technologique IA

### Formule exposée

`common/defines/00_ai.txt:482-485` :

```text
TECH_RANDOM_FACTOR = 1.0
TECH_COST_PENALTY_FACTOR = 5.0

AI_TENDENCY_AFTER_AHEAD_PENALTY = AI_TENDENCY /
  (1 + 5.0 * ahead_of_time_penalty / era_base_cost)
```

La formule de division est explicitement donnée dans le commentaire du define. L'usage mathématique précis de `TECH_RANDOM_FACTOR` n'est pas documenté : `UNKNOWN`.

### Poids vanilla

Les 179 technologies possèdent toutes un `ai_weight` explicite :

| Poids de base | Nombre |
|---:|---:|
| 1.0 | 125 |
| 1.5 | 19 |
| 2.0 | 22 |
| 3.0 | 13 |

52 technologies ajoutent des conditions dynamiques : 16 Production, 20 Military, 16 Society. L'annexe technologie indique lesquelles.

Les conditions vérifiées comprennent notamment :

- stratégies Industrial/Resource/Agricultural/Plantation pour les technologies Production (`10_production.txt`, par exemple `lathe:85-99`);
- taille de marine 5 ou 20 et stratégie d'unification allemande pour diverses technologies Military (`20_military.txt`, par exemple `drydocks:36-45`);
- stratégies progressive/égalitaire/conservatrice/réactionnaire, colonial expansion, rang et reconnaissance pour Society (`30_society.txt`).

Aucun define global de priorité de catégorie n'a été trouvé. Les préférences résultent des poids des technologies candidates et de leurs conditions.

### Prérequis et nouvelles technologies

172 technologies ont `unlocking_technologies`. Le GUI appelle `ResearchWithUnlocks` et `AddToQueueWithUnlocks` (`gui/tech_tree.gui:1024-1039`), ce qui prouve que le moteur connaît et peut résoudre les prérequis pour le joueur. Le filtrage exact des candidats IA par prérequis reste dans le moteur.

Toutes les technologies vanilla ayant un poids explicite, il n'existe aucun cas contrôle permettant de mesurer le défaut d'un objet sans `ai_weight`.

```text
IF_NEW_TECH_HAS_NO_AI_WEIGHT = UNKNOWN
SAFE_AUTHORING_RULE = fournir un ai_weight explicite
```

Une technologie moddée valide devrait être chargée par la base et affichée via les data models (`INFERRED`), mais sa participation utile à la sélection IA n'est pas garantie sans poids.

### Nouvelle ère

Le coût d'ère et la distance inter-ères sont génériques dans les scripts, et l'IA normalise sa pénalité par `era base cost`. Elle devrait donc évaluer une nouvelle ère valide sans logique par ID (`INFERRED`). Mais aucune ère 6+ n'existe dans vanilla et aucune limite moteur n'est publiée.

```text
IF_NEW_ERA_IS_ADDED = probablement chargée et évaluée génériquement;
                       prototype et runtime IA obligatoires
```

### Construction d'universités par l'IA

`building_university` a `ai_value = 2000` (`buildings/07_government.txt:80-96`). L'IA considère l'innovation importante si production/cap < 1.0 et excessive à partir de 1.25 (`00_ai.txt:738-739`). Ceci traite l'investissement dans la capacité de recherche; ce n'est pas la formule de choix de la prochaine technologie.

## 10. Baseline de pacing vanilla

### Comptages et coûts bruts

| Ère | Production | Military | Society | Total | Coût unitaire | RAW_COST_SUM |
|---|---:|---:|---:|---:|---:|---:|
| `era_1` | 9 | 12 | 18 | 39 | 7,500 | 292,500 |
| `era_2` | 13 | 10 | 15 | 38 | 10,000 | 380,000 |
| `era_3` | 15 | 13 | 13 | 41 | 12,500 | 512,500 |
| `era_4` | 15 | 13 | 10 | 38 | 15,000 | 570,000 |
| `era_5` | 5 | 10 | 8 | 23 | 17,500 | 402,500 |
| **Total** | **57** | **58** | **64** | **179** | — | **2,157,500** |

Par catégorie : Production 697,500; Military 722,500; Society 737,500.

Le total inclut `sericulture` (7,500), qui a `can_research = no`. Il s'agit bien du coût brut de tous les objets, mais pas d'un parcours entièrement consommable par recherche active seule.

### Simulation théorique à innovation stable

Formule : `years = 2,157,500 / weekly_innovation / (365/7)`.

| Innovation hebdomadaire stable | Semaines | Années calendaires |
|---:|---:|---:|
| 25 | 86,300.00 | 1,655.07 |
| 50 | 43,150.00 | 827.53 |
| 75 | 28,766.67 | 551.69 |
| 100 | 21,575.00 | 413.77 |
| 150 | 14,383.33 | 275.84 |
| 200 | 10,787.50 | 206.88 |
| 300 | 7,191.67 | 137.92 |

Ces nombres sont une division de budget, pas une prédiction de partie. Ils ignorent technologies initiales, spread simultané, research-speed modifiers, pénalité inter-ères, non-researchable techs, progression d'événements, occupation universitaire variable et arrondis moteur. La valeur 25 n'est pas présentée comme un niveau vanilla normal : la base brute est 50 avant modificateurs.

## 11. Contraintes 1776–1936 et 1700–1936

### Capacité brute sans spread ni multiplicateur

| Innovation | Capacité en 160 ans | Capacité en 236 ans |
|---:|---:|---:|
| 25 | 208,571 | 307,643 |
| 50 | 417,143 | 615,286 |
| 75 | 625,714 | 922,929 |
| 100 | 834,286 | 1,230,571 |
| 150 | 1,251,429 | 1,845,857 |
| 200 | 1,668,571 | 2,461,143 |
| 300 | 2,502,857 | 3,691,714 |

Pour consommer directement la baseline brute entière :

```text
AVERAGE_ACTIVE_PROGRESS_REQUIRED_1776_1936 = 258.60/week
AVERAGE_ACTIVE_PROGRESS_REQUIRED_1700_1936 = 175.33/week
```

Contraintes mathématiques pour le futur design, sans proposer de nouveaux coûts :

1. La somme des coûts et pénalités doit être comparée à l'investissement actif moyen, pas à l'innovation brute au-dessus du cap.
2. À 100 % literacy, le cap vanilla de base n'est que 200 avant autres bonus. Une trajectoire 1776 finissant une enveloppe vanilla entière exige donc soit cap/bonus élevés, soit spread/progress grants importants, soit une enveloppe inférieure.
3. Le spread travaille parallèlement dans trois catégories et réduit le budget actif nécessaire, mais son rendement dépend de la diffusion mondiale et d'une sélection moteur non déterministe.
4. Davantage d'ères augmente mécaniquement la pénalité si les joueurs sautent des technologies anciennes. Le coût nominal seul sous-estime donc le pacing réel.
5. Les IA n'ont pas besoin de finir l'arbre, mais une grande puissance doit pouvoir entretenir assez d'universités employées pour approcher son cap; les seuils IA visent 100–125 % du cap produit.

## 12. UI, icônes et localisation

### Nouvelle technologie

```text
TECH_LOCALIZATION_KEYS_REQUIRED = <tech_id>, <tech_id>_desc
TECH_ICON_FORMAT = DDS; vanilla parity: 256x256, 32-bit BGRA avec alpha et mipmaps
TECH_ICON_PATH = chemin relatif valide renseigné dans texture;
                 convention vanilla gfx/interface/icons/invention_icons/<tech_id>.dds
```

`inventions_l_english.yml` contient les paires nom/description. Le cas `artillery` réutilise une clé de nom située dans `goods_l_english.yml`, mais possède sa description technologie; pour une nouvelle ID, définir les deux clés évite une dépendance de namespace. Les fichiers vanilla sont encodés UTF-8 avec BOM.

Les 179 références de texture ont été résolues sur disque. Les 179 DDS référencés ont le même profil observé : 256 x 256, 32-bit non-FourCC BGRA avec alpha, taille 349,652 octets correspondant aux mipmaps. Le GUI affiche directement `[Technology.GetTexture]` (`tech_tree.gui:1024-1056`).

### Nouvelle ère

```text
ERA_LOCALIZATION_KEYS_REQUIRED = aucune clé par ID dans l'UI vanilla actuelle
ERA_ASSET_REQUIREMENTS = aucun asset par ère requis par les cinq définitions vanilla
```

Le schéma accepte un champ `icon`, mais vanilla ne l'utilise pas dans `00_eras.txt`; son affichage effectif ailleurs est `UNKNOWN`. Il faut en revanche mettre à jour la prose `concept_technology_era_desc` et vérifier le badge numérique pour 10–14.

### Risques d'échelle GUI

- graphe positionné par le moteur : favorable;
- scroll/pan et zoom 0.20–1.0 : favorable mais limité;
- trois séparateurs décoratifs fixes par catégorie : adaptation nécessaire;
- nœud 465 x 150 et graphe beaucoup plus long : risque de navigation/chevauchement;
- lignes de prérequis calculées par le moteur : favorable, mais densité et performance non testées;
- maximum de cinq icônes d'unlock affichées (`00_interfaces.txt:131`) : les unlocks excédentaires nécessitent une UX de groupe/tooltip;
- performances avec plusieurs centaines de nœuds : `UNKNOWN`.

## 13. Fichiers à adapter ou revalider pour 10–14 ères

### Adaptation obligatoire

- `common/technology/eras/00_eras.txt`
- `common/technology/technologies/10_production.txt`
- `common/technology/technologies/20_military.txt`
- `common/technology/technologies/30_society.txt`
- `common/scripted_effects/00_starting_inventions.txt`
- `localization/*/concepts_l_*.yml` pour la description cinq-ères
- `localization/*/inventions_l_*.yml` pour noms/descriptions des nouveaux nœuds
- `gfx/interface/icons/invention_icons/*.dds` pour les nouveaux nœuds

### Adaptation GUI très probablement nécessaire

- `gui/tech_tree.gui` : bandes décoratives, zoom/navigation et badge deux chiffres
- `common/defines/00_interfaces.txt` : positions initiales et zoom si le layout final le demande
- `gfx/interface/illustrations/tech_tree/*.dds` et `gfx/interface/tech_tree/*.dds` seulement si le nouveau layout visuel change

### Revalidation mécanique obligatoire, modification non automatiquement nécessaire

- `common/defines/00_defines.txt`: facteur de pénalité et random range
- `common/defines/00_ai.txt`: pénalité de coût IA et seuils innovation
- principes, pactes, lois, rangs, compagnies et static modifiers listés dans l'annexe
- `common/static_modifiers/00_code_static_modifiers.txt`: base/cap/literacy/excès
- universités et PMs dans `buildings`, `production_method_groups` et `production_methods`
- inventaires education/literacy

### Progress grants à recalibrer si les coûts ou IDs changent

`00_eras.txt:1` le demande explicitement. Les 65 sites gameplay actifs sont répartis dans :

- `events/1848.txt`
- `events/agitators_events/historic_agitator_events.txt`
- `events/agitators_events/silkworm_diseases.txt`
- `events/brazil/positivism.txt`
- `events/cholera.txt`
- `events/commander_events.txt`
- `events/decree_events_02.txt`
- `events/ig_suppression_events.txt`
- `events/japan_events/ep2_iwakura_events.txt`
- `events/meiji_restoration.txt`
- `events/psychology_events.txt`
- `events/soi_events/00_lobbies_events_03.txt`
- `events/tech_events/camera_film_pm_events.txt`
- `events/tech_events/military_tech_events_01.txt`
- `events/tech_events/naval_tech_events.txt`
- `events/tech_events/nursing_events.txt`
- `events/tech_events/production_tech_events.txt`
- `events/tech_events/society_events_01.txt`
- `events/tech_events/society_events_03.txt`
- `events/tech_events/society_tech_events.txt`
- `events/tech_events/society_techs_02.txt`
- `events/tech_events/trench_warfare.txt`
- `events/tech_events/war_crimes_events.txt`
- `events/trade_route_events.txt`
- `events/vampire_panic_events.txt`

`events/test_events.txt` contient des exemples commentés et n'est pas un site gameplay actif.

## 14. Inconnues irréductibles depuis les fichiers accessibles

1. Limite C++ maximale du nombre d'ères et comportement avec `era_10`+.
2. Algorithme exact de layout du graphe et performance à plusieurs centaines de nœuds.
3. Distribution exacte appliquée à `TECH_SPREAD_RANDOM_RANGE = 0.5`.
4. Algorithme de sélection/remplacement des trois technologies en spread.
5. Valeurs et cap hardcodés des contributions de voisin/pacte affichées par l'UI.
6. Ordre exact des additions, multiplications, clamps et arrondis pour coût, progrès actif et spread.
7. Valeur par défaut d'un `ai_weight` absent; vanilla ne fournit aucun témoin.
8. Traitement IA d'une sixième ère en conditions réelles.
9. Effet exact du university throughput sur le `country_modifier` d'innovation `workforce_scaled`.
10. Effet visuel éventuel du champ d'ère optionnel `icon`.

Ces inconnues imposent une micro-phase de prototype technique avant la conception finale : petite ère 6 factice, nœuds factices avec poids IA explicites, contrôle GUI et observation runtime/IA. TECH-0 ne réalise pas cette implémentation.

## Livrables associés

- `TECH_0_VANILLA_TECHNOLOGY_INVENTORY.csv` — 179 technologies, catégorie, ère, coût, IA, texture et provenance.
- `TECH_0_RESEARCH_MODIFIER_INVENTORY.csv` — 165 affectations directes/throughput pertinentes avec ID, valeur et ligne.
- `TECH_0_LITERACY_EDUCATION_INDIRECT_INVENTORY.csv` — 49 affectations education/literacy indirectes.

```text
GAMEPLAY_FILES_CHANGED = 0
TECH_TREE_DESIGN_PROPOSED = NO
HISTORICAL_TECH_SELECTION_PERFORMED = NO
NEXT_TECHNICAL_GATE = ERA_6_PLUS_PROTOTYPE_AND_RUNTIME_VALIDATION
```
