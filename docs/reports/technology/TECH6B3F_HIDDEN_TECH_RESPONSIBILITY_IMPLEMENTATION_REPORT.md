# TECH6B3F — Hidden Technology Responsibility Redistribution Implementation

Résultat : **PASS**  
Nature : implémentation gameplay contrôlée, sans commit ni push.  
Vanilla canonique : Victoria 3 `1.13.11`, `C:/Games/Victoria 3/game`.

## A. Checkpoint Git

- Branche de départ : `tech6b3d-tree-correction-implementation`.
- Branche de travail : `tech6b3f-hidden-tech-responsibility-implementation`.
- Le worktree non propre TECH6B1–E et les corrections humaines ont été conservés sans reset, clean, stash ni restauration globale.
- Checkpoint TECH6B3E : 977 fichiers gameplay, agrégat déterministe `6bc7c8499dbe0e0f9f9ef095555a81ba6f3f66bf9907f80056e3d2f1d350c397`.
- Après TECH6B3F : 1 010 fichiers gameplay. L'augmentation de 33 fichiers correspond exactement aux shadows vanilla requis ; les deux fichiers des bâtiments urbains différés n'ont pas été copiés.

## B. Sources lues

Avant toute écriture gameplay, les sept sources autoritatives ont été relues intégralement :

1. `TECH6B3E_HIDDEN_TECH_RESPONSIBILITY_AUDIT_REPORT.md` ;
2. `TECH6B3E_HIDDEN_TECH_RESPONSIBILITY_MATRIX.csv` ;
3. `TECH6B3E_TAXATION_GATE_REVIEW.csv` ;
4. `TECH6B3D_TREE_CORRECTION_IMPLEMENTATION_REPORT.md` ;
5. `TECH6B3D_TREE_CORRECTION_IMPLEMENTATION_MATRIX.csv` ;
6. `TECH6B3C_TREE_HUMAN_REVIEW_REPORT.md` ;
7. `TECH6B3C_TREE_HUMAN_REVIEW_MATRIX.csv`.

La matrice TECH6B3E contient 409 responsabilités réelles et quatre sentinelles d'alias vides. Parmi les responsabilités réelles, 229 sont des grants initiaux et 180 sont non-starting.

## C. Décisions utilisateur figées

Les corrections humaines post-TECH6B3D restent autoritatives :

- `joint_stock_companies` est recherchable, visible, en `era_6`, avec `postal_savings` et `commercial_insurance_markets` ;
- Laissez-Faire reste sur Joint Stock et Protectionnisme sur `political_economy` ;
- l'assurance publique reste sur `organized_immunization_campaigns` ;
- la répartition `human_rights` / `labor_movement`, l'athéisme d'État, Terakoya et les cinq lois d'esclavage sont inchangés ;
- le GUI financier est byte-identique au checkpoint TECH6B3F ;
- aucune arête Society ↔ Production et aucun élément Concrete/Cement Works n'ont été ajoutés.

## D. Exclusions Starting Tech

Les 229 lignes `starting_technology_grant` ont été copiées dans `TECH6B3F_STARTING_TECH_DEFERRED_MATRIX.csv` avec :

```text
ACTION = DEFER_TO_TECH6B3G_STARTING_TECH_RECONCILIATION
FUTURE_PHASE = TECH6B3G_STARTING_TECH_RECONCILIATION
```

Les 107 fichiers effectifs concernés par ces grants conservent leur agrégat de checkpoint. `git status` est vide sur `common/history/countries` et `common/scripted_effects/00_starting_inventions.txt`.

## E. Lois redistribuées

Les sept gates cachés ont été remplacés :

| Loi | Gate final |
|---|---|
| `law_universal_suffrage` | `liberal_constitutionalism` |
| `law_proportional_taxation` | `classical_political_economy` |
| `law_national_guard` | `professional_civil_policing` |
| `law_national_militia` | `corps_organization` |
| `law_professional_army` | `corps_organization` |
| `law_diplomatic_navy` | `state_dockyard_systems` |
| `law_professional_navy` | `state_dockyard_systems` |

Après reconstruction de l'overlay, aucune loi ne possède un owner parmi les 44 alias cachés.

## F. Modifiers redistribués

Les 19 responsabilités de modifier direct ont quitté neuf alias :

- `army_reserves` et `mandatory_service` → `corps_organization` ; les deux anciennes paires identiques convergent vers une seule paire finale ;
- `dialectics` → `polytechnical_education` ;
- `military_drill` → `light_infantry_tactics` ;
- `power_of_the_purse` → `state_dockyard_systems` ;
- `sericulture` → `selective_breeding` ;
- `urban_planning` → `modern_sewerage` ;
- `urbanization` → `paved_roads` ;
- les trois valeurs de `psychiatry` étaient déjà présentes à l'identique sur `philosophical_pragmatism` et n'ont pas été recopiées ; seul le bloc source a été retiré.

Toutes les clés et valeurs viennent des 19 lignes exactes TECH6B3E. Chaque paire cible clé/valeur apparaît exactement une fois dans son bloc cible.

## G. Bâtiments

Les neuf bâtiments encore hérités d'`enclosure` (`building_vineyard` et huit plantations) passent à `improved_husbandry`. Les fermes/ranchs et Cotton Gin déjà traités par TECH6B3D n'ont pas été réécrits.

### URBAN_BUILDING_GATE_DEFERRED

| Objet | CURRENT_GATE | CURRENT_EFFECT | WHY_NOT_PAVED_ROADS_AUTOMATICALLY | FUTURE_REVIEW_REQUIRED |
|---|---|---|---|---|
| `building_urban_center` | `urbanization` | bâtiment fondamental disponible selon le gate total-conversion courant | `paved_roads` est en `era_10` et pourrait empêcher le fonctionnement urbain de base | YES |
| `building_construction_sector` | `urbanization` | bâtiment fondamental du système de construction | un déplacement automatique vers `paved_roads` pourrait casser toute la boucle de construction | YES |

Les deux fichiers vanilla correspondants n'ont pas été shadowés pendant TECH6B3F.

## H. Unités / Military

Les neuf gates d'unités, le type de navire, l'option de mobilisation, les traits de commandement, les décrets militaires, les stratégies IA, les JEs et les effets paramétrés suivent les owners exacts de la matrice. Le cas multi-cible `napoleonic_warfare` est traité objet par objet : Lancers → `corps_organization`, Mobile Artillery → `horse_artillery`.

## I. Compagnies

Les 12 conditions de compagnies ont été migrées : trois vers `regulated_small_arms`, deux vers `gantry_cranes`, une vers `iron_hull_construction` et six vers `coke_smelting`. Les blocs voisins, notamment `possible` et `ai_will_do`, ont été préservés.

## J. Partis et mouvements

Les cinq triggers de partis, `radical_party`, les cinq mouvements politiques, les onze idéologies et les groupes d'intérêt inventoriés utilisent désormais leurs owners visibles. Republican Union / `radical_party` dépend de `liberal_constitutionalism`.

## K. Événements / JEs

Les 34 familles de triggers d'événements, 11 JEs, trois grants d'événement non-starting, deux progressions technologiques et les hooks scripted exacts ont été migrés. Chaque remplacement est limité aux lignes auditées ; les noms d'objets homonymes, comme l'objet IA `artillery`, n'ont pas été renommés.

## L. Dialectics

La séparation finale est appliquée :

- `country_institution_schools_max_investment_add = 1` sur `polytechnical_education` ;
- personnages, agitateurs, événements, conditions et progression politique sur `socialism` ;
- grants de Krakow et tiers initiaux inchangés.

Toutes les responsabilités non-starting inventoriées pour `dialectics` ont quitté l'alias.

## M. Psychiatry

- `events/psychology_events.txt` et `dt_society_events.1` passent à `psychoanalysis` ;
- `movement_positivist` et `je_positivist_movement` passent à `philosophical_pragmatism` ;
- les trois modifiers de `psychiatry` ont été retirés sans copie, car `philosophical_pragmatism` contenait déjà exactement `0.25`, `0.25` et `-0.05` sur les trois clés concernées.

`PSYCHIATRY_MODIFIER_DUPLICATION_AFTER = 0` selon le contrôle source/cible imposé.

## N. Urban Planning / Urbanization

Les quatre valeurs `urban_planning` sont présentes une seule fois sur `modern_sewerage`; l'événement Choléra suit ce nœud. Les quatre valeurs `urbanization` sont présentes une seule fois sur `paved_roads`. Les grants Japon, Perse et tiers scriptés ainsi que les deux gates de bâtiments restent différés.

## O. Taxation

Progression finale validée :

```text
consumption = NONE
land = NONE
per_capita = systematic_population_registration
proportional = classical_political_economy
graduated = socialism
```

Dans `law_per_capita_based_taxation`, le gate et l'unique condition IA représentant sa maturité technologique utilisent tous deux `systematic_population_registration`; les autres conditions IA sont inchangées.

## P. Alias encore présents

Les 44 alias sont toujours définis. Les quatre nœuds vides `banking`, `mechanized_workshops`, `mysorean_iron_cased_rocketry` et `pharmaceuticals` sont conservés. Aucun nouvel ID technologique n'a été créé.

## Q. Références cachées restantes classifiées

| Classification | Nombre | Résultat |
|---|---:|---|
| alias definitions | 44 | `ALLOWED_COMPATIBILITY_REFERENCE` |
| relations parentales internes aux fichiers technologiques | 33 | `ALLOWED_COMPATIBILITY_REFERENCE` |
| grants initiaux pays/tier | 229 | `DEFERRED_STARTING_TECH` |
| gates Urban Center / Construction Sector | 2 | `EXPLICITLY_DEFERRED_URBAN_BUILDING` |
| autre responsabilité gameplay non-starting inventoriée | 0 | aucune |
| `BUG` | 0 | PASS |

## R. Fichiers gameplay modifiés

TECH6B3F modifie 79 chemins gameplay : 59 sous `common` et 20 sous `events`. Le détail exact figure dans la colonne `actual_file_changed` de la matrice d'implémentation. Répartition `common` : 4 stratégies IA, 2 bâtiments, 1 template, 1 fichier de traits, 1 fichier d'unités, 7 compagnies, 1 décision, 1 décret, 1 historique de mouvements, 1 idéologies, 2 groupes d'intérêt, 10 JEs, 5 lois, 1 mobilisation, 1 on-action, 5 partis, 1 mouvements politiques, 4 scripted buttons, 3 scripted effects, 1 scripted trigger, 1 type de navire et 5 fichiers technologiques.

Trente-trois de ces chemins sont des shadows créés depuis le fichier vanilla 1.13.11 de même chemin relatif, puis modifiés uniquement sur les références auditées.

## S. Validations

```text
STATIC_VALIDATION = PASS
IMPLEMENTATION_IDEMPOTENCE = PASS
TECH_DEFINITIONS = 285
HIDDEN_ALIASES_PRESENT = 44
DUPLICATE_TECH_IDS = 0
TECH_TREE_CYCLES = 0
UNKNOWN_TECH_PREREQUISITES = 0
CROSS_CATEGORY_TECH_EDGES = 0
HIDDEN_TECH_LAW_UNLOCKS_AFTER = 0
HIDDEN_TECH_PM_UNLOCKS_AFTER = 0
HIDDEN_TECH_DIRECT_MODIFIERS_AFTER = 0
DUPLICATED_TRANSFERRED_MODIFIERS = 0
PSYCHIATRY_MODIFIER_DUPLICATION_AFTER = 0
UNKNOWN_TECH_IDS = 0
INVENTED_TECH_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0
STARTING_TECH_FILES_CHANGED = 0
STARTING_TECH_GRANTS_CHANGED = 0
GUI_FILES_CHANGED_BY_TECH6B3F = 0
GIT_DIFF_CHECK = PASS
```

Un smoke de 35 secondes a régénéré `error.log`. Il ne contient aucune erreur non-localisation ciblée concernant les technologies, lois, bâtiments, PM, événements ou chemins TECH6B3F. Les diagnostics restants sont des doublons de localisation et trois avertissements GUI préexistants, sans lien avec cette phase.

```text
PARSER_LOG_SMOKE = PASS
RUNTIME = SMOKE_ONLY
```

Aucune nouvelle partie ni passage d'un mois n'a été observé ; aucun runtime gameplay complet n'est revendiqué.

## T. Phase suivante

TECH6B3F est clos sans blocker. La phase suivante est `TECH6B3G_STARTING_TECH_RECONCILIATION`, qui devra examiner les 229 grants pays/tier un par un. Aucun commit, push, asset, GUI, Steam ou béton n'a été modifié.

## Addendum TECH6B3F-CIT — réactivation ciblée d'Egalitarianism

La classification TECH6B3F d'`egalitarianism` comme alias caché consommé est partiellement superseded. Par décision utilisateur ultérieure, l'ID existant est redevenu une technologie Society active, visible et recherchable en `era_9`, avec `feminism` pour unique parent et `law_multicultural` pour unique nouvelle responsabilité gameplay directe.

Les migrations TECH6B3F restent autoritatives : ni le suffrage universel, ni la taxation proportionnelle, ni `radical_party`, ni le Printemps des Peuples, ni l'ancien `on_researched`, ni les autres hooks redistribués ne reviennent sur `egalitarianism`. Le décompte courant des alias cachés est donc 43 ; les valeurs 44 de ce rapport demeurent le checkpoint historique avant TECH6B3F-CIT.
