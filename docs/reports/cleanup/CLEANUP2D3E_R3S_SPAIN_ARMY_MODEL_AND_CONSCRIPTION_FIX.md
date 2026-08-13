# CLEANUP-2D-3E-R3S — Modèle d'armée et conscription de l'Espagne

## Verdict

Le défaut n'est ni une mauvaise activation de loi, ni une confusion parent/variant. Dans le save R3, l'Espagne et les États-Unis ont le même objet actif `law_peasant_levies`. La différence critique est le modificateur espagnol `national_guard_preoccupied`, copié avec le setup carliste vanilla de 1836 dans le setup global du mod : son `state_conscription_rate_add = -0.04` annule exactement le `+0.04` de `law_peasant_levies`.

Le correctif R3S retire uniquement ce modificateur anachronique du setup espagnol de 1776 et rétablit 70 conscrits espagnols dans six États incorporés admissibles. La loi reste `law_peasant_levies`; les 95 réguliers, les 40 navires et les trois flottes espagnoles ne changent pas.

```text
ROOT_CAUSE = SPA_1776_INHERITS_VANILLA_1836_CARLIST_CONSCRIPTION_PENALTY
SPA_USA_CRITICAL_DIFFERENCE = national_guard_preoccupied (-0.04) on SPA only
SPA_NET_CONSCRIPTION_RATE_BEFORE = 0.04 - 0.04 = 0.00
SPA_NET_CONSCRIPTION_RATE_AFTER = 0.04
```

## Save R3 diagnostique

Le save `armée.v3`, daté du 13 août 2026 à 18:17:33, est postérieur sans ambiguïté aux saves R2. Il a été copié puis fondu dans un répertoire temporaire; l'original n'a jamais été modifié.

```text
R3_SAVE_ORIGINAL_SHA256 = 317D6FDA86E6EBAB8D5E4B0528317CE275CA931E503828328481A35557A7C855
SPA_COUNTRY_ID = 37
USA_COUNTRY_ID = 9

SPA_SCRIPTED_LAW_BEFORE = law_peasant_levies
SPA_RUNTIME_LAW_BEFORE = law_peasant_levies
SPA_LAW_PARENT_BEFORE = NONE
SPA_LAW_VARIANT_BEFORE = NO
SPA_RUNTIME_LAW_ACTIVE_BEFORE = YES

USA_SCRIPTED_LAW = law_peasant_levies
USA_RUNTIME_LAW = law_peasant_levies
USA_LAW_PARENT = NONE
USA_LAW_VARIANT = NO
USA_RUNTIME_LAW_ACTIVE = YES
```

Les deux objets runtime sont actifs dans `lawgroup_army_model`; tous deux portent la même date d'activation interne `1836.1.1` et la même référence de remplacement `law_professional_army`. Ces champs identiques ne peuvent pas expliquer le résultat divergent. Le save contient en revanche `national_guard_preoccupied` pour SPA seulement, zéro centre de conscription espagnol et 80 niveaux de centres américains.

Le détail champ par champ est conservé dans `docs/research/military/CLEANUP2D3E_R3S_SPAIN_LAW_COMPARISON.csv`.

## Gate A — modèle de lois vanilla 1.13.9

Audit effectué exclusivement contre `C:\Games\Victoria 3\game`, version 1.13.9 :

| Objet | Définition vanilla 1.13.9 | Conclusion |
|---|---|---|
| `law_peasant_levies` | loi de base de `lawgroup_army_model`; aucun champ `parent`; `state_conscription_rate_add = 0.04`; conscrits paysans et infanterie seulement | Activation history correcte : `activate_law = law_type:law_peasant_levies` |
| `law_warrior_caste` | variant avec `parent = law_peasant_levies` | N'est actif ni pour SPA ni pour USA |
| `law_professional_army` | loi de base séparée; technologie `military_drill`; taux `0.01`; plafond de centres 50 | Techniquement disponible pour SPA, mais capacité de mobilisation trop faible pour le modèle 2D-2 |
| `law_national_militia` | loi de base séparée; taux `0.05` | Modèle national moderne inadéquat pour la monarchie bourbonienne de 1776 |
| `law_mass_conscription` | loi de base séparée; taux `0.03` | Modèle de conscription de masse historiquement anachronique |

Le libellé UI « country must have a conscription law » provient d'un gate moteur non exposé sous la forme d'un trigger script définissable dans la baseline. L'inférence contrôlée par SPA/USA est que le gate UI/recrutement tombe à faux lorsque le taux effectif de conscription d'État est nul : l'objet de loi espagnol est actif, mais `+0.04 + (-0.04) = 0.00`. Après retrait de la seule différence causale, SPA retrouve le même taux effectif de base que le témoin USA.

## Gate B — différence SPA/USA

Les éléments suivants ont été comparés dans les histories et le save R3 : objet de loi, groupe, parent, variant, statut actif, syntaxe d'activation, gouvernement, religion, incorporation, modificateurs et effets de setup.

| Champ critique | SPA | USA | Pertinent |
|---|---|---|---|
| Loi scriptée/runtime | `law_peasant_levies` / active | `law_peasant_levies` / active | Non : identique |
| Parent/variant | aucun / non | aucun / non | Non : identique |
| Groupe | `lawgroup_army_model` | `lawgroup_army_model` | Non : identique |
| Loi religieuse | `law_state_religion` | `law_state_religion` | Non : identique |
| Gouvernement | `gov_absolute_kingdom` | `gov_cleanup2c1_usa` | Différent, mais aucun modificateur de conscription causal trouvé |
| États incorporés | 15 | 17 | Modifie la capacité, pas la reconnaissance de la loi |
| Modificateur pays | `national_guard_preoccupied` | aucun équivalent | Oui : cause directe |
| Taux net avant R3S | `0.00` | `0.04` | Oui : différence critique |

`common/history/global/00_global.txt` appliquait le modificateur à SPA sans condition. Dans vanilla, ce malus fait partie du contexte de la guerre carliste et `common/journal_entries/06_the_carlist_wars.txt` le retire lors de la résolution du journal. Le scénario 1776 n'exécute pas ce cycle carliste; le malus restait donc permanent.

## Gate D — choix historique

La recherche 2D-1 décrit pour SPA un établissement permanent de la Couronne, distinct des milices, levées provinciales et auxiliaires. La conversion 2D-2 classe explicitement le système comme `EUROPEAN_REGULAR_STATE`, avec 95 unités régulières, et la mobilisation comme `MILITIA_RESERVE`, avec une cible de 70.

`law_professional_army` décrit mieux le seul noyau permanent. Cependant, Victoria 3 impose une loi unique pour l'ensemble du système : son taux vanilla de 1 % ne donnerait que 39 niveaux bruts et 24 effectifs dans les États incorporés, donc au plus 24 conscrits. Cette option effacerait la réserve provinciale explicitement retenue par 2D-2. `law_peasant_levies`, malgré son nom trop rural, est le meilleur proxy 1.13.9 disponible pour combiner une armée régulière bourbonienne et une réserve provinciale importante, tout en limitant les conscrits à l'infanterie.

```text
SPA_1776_HISTORICAL_ARMY_MODEL = EUROPEAN_REGULAR_STATE_WITH_PROVINCIAL_MILITIA_RESERVE
SPA_TECHNICAL_ARMY_MODEL_REQUIRED = law_peasant_levies
SPA_SELECTED_ARMY_MODEL = law_peasant_levies
RATIONALE = BEST_SINGLE_LAW_PROXY_FOR_95_REGULAR_PLUS_70_MILITIA_RESERVE
```

## Trigger `has_law_or_variant`

Le log est réel mais indépendant :

```text
HAS_LAW_OR_VARIANT_ERROR_PREEXISTING = YES
LAW_ARGUMENT_IS_VARIANT = law_homesteading
EXPECTED_PARENT = law_peasant_proprietorship
HAS_LAW_OR_VARIANT_LOG_ERROR_RELATED = NO
```

Le mod passe `law_homesteading`, qui est un variant de `law_peasant_proprietorship`; vanilla 1.13.9 passe le parent. Cette divergence concerne la loi agraire et non `lawgroup_army_model`. Conformément au périmètre, `common/interest_groups/00_landowners.txt` n'a pas été modifié.

## Capacité et allocation après correction

Formule R2F conservée : `ceil(workforce × 0.04 / 1000)` pour le brut et `floor(workforce × 0.04 / 1000)` pour le plafond effectivement matérialisable, avec uniquement les États incorporés admissibles pour le second calcul.

```text
SPA_RAW_CONSCRIPTION_CAP_AFTER = 132
SPA_ELIGIBLE_RAW_CONSCRIPTION_CAP_AFTER = 130
SPA_EFFECTIVE_CONSCRIPTION_CAP_AFTER = 115
SPA_FINAL_SCRIPTED_CONSCRIPTS_AFTER = min(70, 115) = 70
```

Le brut 132 conserve la convention R1/R2F sur les 17 États directement détenus; deux niveaux appartiennent à `STATE_AL_RIF` et `STATE_WEST_INDIES`, non incorporés et donc exclus du brut admissible 130 comme de l'effectif 115.

| État incorporé | Plafond effectif | Allocation R3S |
|---|---:|---:|
| New Castile | 15 | 15 |
| Galicia | 14 | 14 |
| Lower Andalusia | 12 | 12 |
| Old Castile | 12 | 12 |
| Upper Andalusia | 11 | 11 |
| Catalonia | 9 | 6 |
| Total | 73 utilisés / 115 pays | 70 |

Tous les bataillons sont `combat_unit_type_line_infantry`, compatible avec la restriction de `law_peasant_levies`.

## Fichiers modifiés par R3S

- `common/history/global/00_global.txt` : suppression du seul `add_modifier = national_guard_preoccupied` dans le setup SPA.
- `common/history/military_formations/00_military_formations_europe.txt` : ajout des 70 conscrits dans la première formation terrestre SPA.
- présent rapport et CSV comparatif.

Aucune loi globale, technologie, population, carte, propriété, define, formation non espagnole, unité régulière ou unité navale n'a été modifiée par R3S.

## Validation statique

Un parseur équilibré par accolades a relu les huit fichiers actifs `0*_military_formations_*.txt` et recompté chaque objet `create_military_formation`.

```text
CLEANUP2D3E_R3S_STATIC = PASS

SPA_REGULAR = 95
SPA_NAVY = 40
SPA_FLEETS = 3
SPA_ACTIVE_ARMY_LAW_AFTER = law_peasant_levies
SPA_ARMY_LAW_RECOGNIZED_BY_CONSCRIPTION_EXPECTED = YES
SPA_CONSCRIPT_TARGET_AFTER = 70

GBR = 49 regular + 43 conscripts / 120 ships / 7 fleets
USA = 20 regular + 80 conscripts / 5 ships
TUR = 65 regular + 139 conscripts
RUS = 215 regular + 120 conscripts / 32 ships

GBR_CHANGED = 0
USA_CHANGED = 0
TUR_CHANGED = 0
RUS_CHANGED = 0
REGULAR_TOTAL = 2557
REGULAR_TOTAL_CHANGED = 0
NAVAL_TOTAL = 370
NAVAL_TOTAL_CHANGED = 0
NO_EMPTY_FORMATIONS = YES

TECH_CHANGED = 0
POP_CHANGED = 0
MAP_CHANGED = 0
DEFINES_CHANGED = 0
PROTECTED_TECH_FILES_CHANGED = 0
BJECT_PATH_PRESENT = 0

BRACE_BALANCE = PASS
git diff --check = PASS
CODEX_LAUNCHED_VICTORIA3 = NO
GIT_INDEX_MUTATED_BY_CODEX = NO
```

Les sept fichiers technologiques protégés conservent leurs sept empreintes SHA-256 de référence, restent non suivis et non indexés.

## Runtime restant

Le seul contrôle encore nécessaire est une nouvelle partie Espagne : confirmer `law_peasant_levies` active, 95 réguliers, 40 navires, 70 conscrits après stabilisation, capacité non nulle et bouton de recrutement fonctionnel. Aucun nouveau tour mondial n'est requis.

CLEANUP-2D-4 n'est pas commencé.
