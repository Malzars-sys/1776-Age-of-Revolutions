# TECH6B3E — Hidden Technology Responsibility Redistribution Audit

Résultat documentaire : **PASS**  
Nature : audit uniquement ; aucune modification gameplay, aucun commit, aucun push.  
Vanilla canonique : Victoria 3 `1.13.11`, `C:/Games/Victoria 3/game`.

## A. État Git

- Branche : `tech6b3d-tree-correction-implementation`.
- Le worktree gameplay était déjà non propre à l'ouverture de TECH6B3E ; il contient les travaux TECH6B1–D et les corrections humaines manuelles.
- Checkpoint TECH6B3E : 977 fichiers sous `common`, `events`, `map_data`, `gui` et `localization` ; agrégat SHA-256 déterministe `6bc7c8499dbe0e0f9f9ef095555a81ba6f3f66bf9907f80056e3d2f1d350c397`.
- Les seules écritures TECH6B3E sont documentaires sous `docs/reports/technology`.

## B. Méthode

L'audit a construit l'overlay effectif de 3 705 fichiers : vanilla 1.13.11, puis remplacement fichier par fichier par le fork, avec exclusion intégrale des technologies vanilla à cause de `replace_path="common/technology/technologies"`.

Ont été croisés :

- les cinq fichiers technologiques effectifs ;
- `can_research = no` ;
- le filtre d'alias de `gui/tech_tree.gui` ;
- les blocs directs `modifier` et `on_researched` ;
- les blocs `unlocking_technologies` ;
- les conditions, effets, progressions et paramètres technologiques ;
- les fichiers vanilla non shadowés, notamment partis, unités, scripted effects et setup pays ;
- les attributions objet par objet déjà figées dans `TECH2H_VANILLA_SPLIT_UNLOCK_MATRIX.csv`.

Une ligne de la matrice principale représente une responsabilité homogène : modifier direct, bloc direct, gate d'objet, trigger/effect scripté ou attribution de technologie initiale. Les occurrences répétées dans un même objet et fichier sont consolidées avec leurs numéros de ligne.

## C. Inventaire des technologies cachées

`HIDDEN_TECHS_AUDITED = 44` : 20 Society, 16 Military et 8 Production.

Society : `academia`, `banking`, `central_archives`, `central_banking`, `centralization`, `corporate_charters`, `currency_standards`, `democracy`, `dialectics`, `egalitarianism`, `empiricism`, `international_trade`, `law_enforcement`, `mass_communication`, `pharmaceuticals`, `psychiatry`, `rationalism`, `tech_bureaucracy`, `urban_planning`, `urbanization`.

Military : `admiralty`, `army_reserves`, `artillery`, `drydocks`, `gunsmithing`, `hydraulic_cranes`, `line_infantry`, `mandatory_service`, `military_drill`, `mysorean_iron_cased_rocketry`, `napoleonic_warfare`, `navigation`, `power_of_the_purse`, `screw_frigate`, `standing_army`, `triage`.

Production : `enclosure`, `intensive_agriculture`, `lathe`, `manufacturies`, `mechanized_workshops`, `prospecting`, `sericulture`, `steelworking`.

`joint_stock_companies` est exclue : elle est recherchable en ère 6 et explicitement visible dans le GUI.

## D. Raisons de leur masquage

- 42 IDs sont des alias consommés : `can_research = no` et présence dans le filtre GUI historique.
- `mysorean_iron_cased_rocketry` est un cas spécial désactivé, sans position fonctionnelle.
- `sericulture` est non recherchable et n'est pas positionnée dans le filtre d'alias standard.
- La présence physique dans `90_tech3a_vanilla_post1836_compatibility.txt` ne leur rend aucune accessibilité normale.

## E. Responsabilités directes

La matrice contient 409 responsabilités réelles, plus quatre lignes sentinelles pour les nœuds vides.

- 19 modifiers directs ;
- 1 bloc `on_researched`, sur `egalitarianism` ;
- 7 gates de lois ;
- 0 gate de Production Method restant ;
- 382 autres gates, triggers, effets et grants, dont 229 attributions de technologies initiales.

Les quatre `SAFE_EMPTY_COMPATIBILITY_NODE` sont `banking`, `mechanized_workshops`, `mysorean_iron_cased_rocketry` et `pharmaceuticals`. Ils ne doivent pas être supprimés pendant cet audit.

## F. Lois orphelines

| Loi | Owner caché courant | Proposition visible | Confiance |
|---|---|---|---|
| `law_universal_suffrage` | `egalitarianism` | `liberal_constitutionalism` | HIGH |
| `law_proportional_taxation` | `egalitarianism` | `classical_political_economy` | MEDIUM |
| `law_national_guard` | `law_enforcement` | `professional_civil_policing` | HIGH |
| `law_national_militia` | `mandatory_service` | `corps_organization` | HIGH |
| `law_professional_army` | `military_drill` | `corps_organization` | HIGH |
| `law_diplomatic_navy` | `military_drill` | `state_dockyard_systems` | HIGH |
| `law_professional_navy` | `military_drill` | `state_dockyard_systems` | HIGH |

Les quinze gates humains récents sont déjà corrigés et ne figurent donc pas comme orphelins actuels.

## G. Production Methods orphelins

`HIDDEN_TECH_PM_UNLOCKS_FOUND = 0`. Les transferts TECH5/TECH6 antérieurs ont supprimé les gates PM vers les 44 IDs cachés. Les noms d'objets ou textures contenant un ancien nom ne sont pas confondus avec des références technologiques.

## H. Bâtiments et autres objets orphelins

Les familles principales sont :

- 11 bâtiments encore gatés par un alias, principalement les plantations/vignobles hérités d'`enclosure` ;
- 9 unités de combat ;
- 4 décrets ;
- 1 option de mobilisation ;
- 1 type de navire ;
- 12 conditions de compagnies ;
- 34 groupes de triggers d'événements ;
- 229 grants de setup ou de tier technologique.

Les recommandations réutilisent uniquement des IDs visibles existants. Les grants de setup sont documentés, mais leur implémentation doit rester une passe pays par pays séparée.

## I. Partis politiques

Le cas confirmé est `radical_party`, qui contient notamment l'affichage « Republican Union » et reste gaté par `egalitarianism` dans le fichier vanilla effectif. La recommandation est `liberal_constitutionalism`.

Cinq autres groupes de triggers de partis emploient un ancien ID comme condition. Ils sont tracés séparément dans la matrice, notamment autour d'`academia`, `currency_standards` et `law_enforcement`.

## J. Modifiers directs

| Technologie cachée | Nombre | Proposition |
|---|---:|---|
| `army_reserves` | 2 | `corps_organization` |
| `mandatory_service` | 2 | `corps_organization` |
| `dialectics` | 1 | `polytechnical_education`, arbitrage requis |
| `military_drill` | 1 | `light_infantry_tactics` |
| `power_of_the_purse` | 1 | `state_dockyard_systems` |
| `psychiatry` | 3 | proposition `psychoanalysis`, arbitrage requis |
| `sericulture` | 1 | `selective_breeding` |
| `urban_planning` | 4 | `modern_sewerage`, arbitrage requis |
| `urbanization` | 4 | `paved_roads`, arbitrage requis |

Chaque clé et chaque valeur exacte figurent individuellement dans la matrice. Aucun modifier n'est supprimé par défaut.

## K. Audit complet de taxation

| Loi | Gate courant | État | Proposition |
|---|---|---|---|
| `law_consumption_based_taxation` | aucun | correct | rester sans gate |
| `law_land_based_taxation` | aucun | correct | rester sans gate |
| `law_per_capita_based_taxation` | `scientific_metrology`, ère 4 | visible mais sémantiquement faible | `systematic_population_registration`, ère 3 |
| `law_proportional_taxation` | `egalitarianism`, ère 7 | caché | `classical_political_economy`, ère 4 |
| `law_graduated_taxation` | `socialism`, ère 7 | visible et cohérent | conserver |

La capitation dépend d'abord du registre de population, pas des étalons de mesure. La taxation proportionnelle forme alors une étape visible avant la fiscalité graduée socialiste. Le choix exact de son owner reste le seul arbitrage fiscal demandé.

## L. Technologies visibles surchargées

La métrique `VISIBLE_TECH_RESPONSIBILITY_COUNT` compte modifiers directs et références effectives hors grants initiaux. Les nœuds actuellement les plus chargés sont `nationalism` (164), `pan-nationalism` (122), `railways` (80), `military_statistics` (62), `political_agitation` (60), `socialism` (56), `corporatism` (49), `civilizing_mission` (45) et `ironclad_tech` (44).

Si toutes les propositions de redistribution étaient appliquées sans nouvelle ventilation, les principales charges entrantes seraient `specialized_technical_academies` (55), `regulated_small_arms` (47), `corps_organization` (38), `commercial_insurance_markets` (36), `codified_practical_knowledge` (29) et `liberal_constitutionalism` (28). Ces nombres sont dominés par le setup historique ; ils imposent une passe dédiée avant implémentation.

## M. Recommandations à forte confiance

- `egalitarianism` → `liberal_constitutionalism` pour le suffrage universel, `radical_party` et le système du Printemps des peuples ;
- `army_reserves`/`mandatory_service` → `corps_organization` ;
- `artillery` → `standardized_field_artillery` pour les objets exacts correspondants ;
- `navigation` → `marine_chronometry` ;
- `power_of_the_purse` → `state_dockyard_systems` ;
- `law_enforcement` → `professional_civil_policing` ;
- `mass_communication` → `periodical_print_networks` ;
- `sericulture` → `selective_breeding` ;
- maintenir les quatre alias vides sans responsabilité.

## N. Cas nécessitant arbitrage utilisateur

[TAX-01]

HIDDEN_TECH = `egalitarianism`  
RESPONSIBILITY = `law_proportional_taxation`  
CURRENT_OWNER = `egalitarianism`  
RECOMMENDED_OWNER = `classical_political_economy`  
WHY = crée une étape fiscale cohérente entre la capitation et la taxation graduée  
ALTERNATIVE = `political_economy` ou `human_rights`  
CONFIDENCE = MEDIUM

[DIALECTICS-01]

HIDDEN_TECH = `dialectics`  
RESPONSIBILITY = modifier scolaire, grants initiaux et événements socialistes  
CURRENT_OWNER = `dialectics`  
RECOMMENDED_OWNER = ventilation : `polytechnical_education` pour le modifier, `early_socialism_cooperativism`/`socialism` pour le contenu politique  
WHY = un owner unique mélangerait éducation et socialisme  
ALTERNATIVE = tout placer sur `socialism`  
CONFIDENCE = MEDIUM

[PSYCHIATRY-01]

HIDDEN_TECH = `psychiatry`  
RESPONSIBILITY = trois modifiers directs, positivisme et événements psychologiques  
CURRENT_OWNER = `psychiatry`  
RECOMMENDED_OWNER = `philosophical_pragmatism` pour le positivisme et `psychoanalysis` pour la psychologie ; revoir séparément les trois modifiers  
WHY = les modifiers d'influence, de manœuvres diplomatiques et de bureaucratie ne sont pas médicalement homogènes  
ALTERNATIVE = préserver tout le paquet sur `psychoanalysis`  
CONFIDENCE = LOW

[URBAN-01]

HIDDEN_TECH = `urban_planning`; `urbanization`  
RESPONSIBILITY = huit modifiers d'infrastructure/construction et grants historiques  
CURRENT_OWNER = deux alias cachés successifs  
RECOMMENDED_OWNER = `modern_sewerage`, puis `paved_roads`  
WHY = préserve deux paliers visibles sans créer de technologie  
ALTERNATIVE = redistribution plus fine vers les technologies Production d'ingénierie, sans aucune arête intercatégorie  
CONFIDENCE = MEDIUM

## O. Compatibilité avec les corrections humaines récentes

Les décisions autoritatives ont été vérifiées dans les objets courants :

- `law_protectionism` → `political_economy` ;
- `law_public_health_insurance` → `organized_immunization_campaigns` ;
- `human_rights` → travail des enfants restreint, organismes réglementaires, subventions salariales ;
- `labor_movement` → école primaire obligatoire, protection des travailleurs, pension de vieillesse ;
- `law_state_atheism` → `socialism` ;
- `law_terakoya` → aucun gate ;
- esclavage : aucun gate / `constitutional_government` / `human_rights` / `organized_reform_movements` / `abolitionist_mobilization` ;
- `joint_stock_companies` est recherchable et visible ;
- `stock_exchange` est explicitement affichable ;
- aucune arête Society ↔ Production n'est proposée pour Steel Frame ou le béton.

`MANUAL_DECISIONS_OVERRIDDEN = 0`.

## P. Aucun changement gameplay

TECH6B3E n'applique aucune recommandation. Les matrices et anciens rapports ont été mis à jour uniquement sous `docs/reports/technology`.

```text
TECH6B3E_HIDDEN_TECH_RESPONSIBILITY_AUDIT = PASS
GAMEPLAY_FILES_CHANGED = 0
HIDDEN_TECHS_AUDITED = 44
HIDDEN_TECH_RESPONSIBILITIES_FOUND = 409
HIDDEN_TECH_DIRECT_MODIFIERS_FOUND = 19
HIDDEN_TECH_LAW_UNLOCKS_FOUND = 7
HIDDEN_TECH_PM_UNLOCKS_FOUND = 0
HIDDEN_TECH_OTHER_UNLOCKS_FOUND = 383
SAFE_EMPTY_COMPATIBILITY_NODES = 4
ORPHANED_RESPONSIBILITIES_WITHOUT_RECOMMENDATION = 0
UNKNOWN_TECH_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0
MANUAL_DECISIONS_OVERRIDDEN = 0
COMMIT = NO
PUSH = NO
```

## Addendum TECH6B3F — implémentation contrôlée

TECH6B3F a appliqué les responsabilités non-starting autorisées par cette matrice : 178 lignes sont implémentées, deux gates de bâtiments urbains sont explicitement différés et les quatre sentinelles d'alias vides restent autorisées. Les sept gates de lois cachés, les 19 responsabilités de modifiers directs et les autres hooks non-starting ont été redistribués vers leurs owners visibles validés.

Les 229 grants initiaux ne sont pas modifiés. Ils sont enregistrés dans `TECH6B3F_STARTING_TECH_DEFERRED_MATRIX.csv` pour `TECH6B3G_STARTING_TECH_RECONCILIATION`. Les 44 alias restent présents comme couche de compatibilité. Les décisions humaines post-TECH6B3D, le GUI financier, les Starting Technologies et le design béton sont inchangés.
