# TECH6B3F-CIT — Citizenship Law Technology Reconciliation

## A. Checkpoint

- Vanilla canonique : Victoria 3 `1.13.11`, sous `C:/Games/Victoria 3/game`.
- Dépôt local : `1776_Age_of_Revolutions_fork`.
- Branche observée au checkpoint : `tech6b3h-starting-tech-reconciliation-implementation`.
- Branche annoncée dans la demande : `tech6b3f-hidden-tech-responsibility-implementation`.
- Commit observé : `950a141 chore: ignore Python cache files`.
- Le worktree contenait déjà des modifications non commitées, notamment dans `90_tech3a_vanilla_post1836_compatibility.txt`. Elles ont été préservées.
- Aucun changement de branche, commit ou push n'a été effectué.

## B. Lois de citoyenneté trouvées

Le fichier effectif vanilla 1.13.11 est `common/laws/00_citizenship.txt`. Le fork ne possédait pas ce chemin au checkpoint ; un shadow complet du fichier canonique a donc été créé, avec seulement les cinq changements de gate requis. Les six IDs exacts sont :

| ID | Nom |
|---|---|
| `law_subjecthood` | Sujétion |
| `law_national_supremacy` | Suprématie nationale |
| `law_ethnostate` | État ethnique |
| `law_racial_segregation` | Ségrégation raciale |
| `law_cultural_exclusion` | Exclusion culturelle |
| `law_multicultural` | Multiculturalisme |

`UNKNOWN_LAW_IDS = 0` et chaque ID possède exactement une définition dans l'overlay effectif.

## C. Gates avant

| Loi | Gate effectif avant |
|---|---|
| `law_subjecthood` | `NONE` |
| `law_national_supremacy` | `NONE` |
| `law_ethnostate` | `nationalism` |
| `law_racial_segregation` | `NONE` |
| `law_cultural_exclusion` | `NONE` |
| `law_multicultural` | `human_rights` |

## D. Gates décidés

| Loi | Gate final | Résultat |
|---|---|---|
| `law_subjecthood` | `NONE` | PASS |
| `law_national_supremacy` | `nationalism` | PASS |
| `law_ethnostate` | `pan-nationalism` | PASS |
| `law_racial_segregation` | `constitutional_government` | PASS |
| `law_cultural_exclusion` | `human_rights` | PASS |
| `law_multicultural` | `egalitarianism` | PASS |

Tous les gates sont des IDs technologiques définis. Aucun gate de cette famille ne cible l'un des 43 alias encore cachés.

## E. Réactivation d'Egalitarianism

La définition existante `egalitarianism` a été conservée dans `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`; aucun second ID ni doublon n'a été créé. Le verrou `can_research = no` a été retiré. Son ère est passée de `era_7` à `era_9`, car `feminism` se trouve en `era_8` et la topologie demandée interdit une inversion temporelle.

État final :

```text
EGALITARIANISM_DEFINED_ONCE = YES
EGALITARIANISM_STATUS = ACTIVE_VISIBLE_RESEARCHABLE_TECH
EGALITARIANISM_RESEARCHABLE = YES
EGALITARIANISM_CATEGORY = society
EGALITARIANISM_ERA = era_9
```

## F. Parent Feminism

L'ancien parent `democracy`, hérité du nœud de compatibilité et lui-même classé parmi les alias consommés, n'a pas été conservé. L'unique parent final est `feminism` :

```text
FEMINISM_CATEGORY = society
FEMINISM_ERA = era_8
EGALITARIANISM_CATEGORY = society
EGALITARIANISM_ERA = era_9
FEMINISM_IS_PARENT_OF_EGALITARIANISM = YES
```

La chaîne directe est donc `feminism -> egalitarianism -> law_multicultural`, sans cycle ni arête intercatégorie.

## G. Anciennes responsabilités Egalitarianism préservées comme migrées

Aucune ancienne responsabilité redistribuée par TECH6B3F n'a été restaurée. Le suffrage universel, la taxation proportionnelle, `radical_party`, le Printemps des Peuples, les anciens triggers et l'ancien `on_researched` restent sur leurs owners issus de TECH6B3F ou de corrections utilisateur ultérieures.

Le bloc final d'`egalitarianism` ne reçoit ni modifier direct ni `on_researched`. Sa nouvelle responsabilité gameplay exclusive dans cette phase est le gate de `law_multicultural`.

```text
OLD_EGALITARIANISM_RESPONSIBILITIES_RESTORED = 0
MULTICULTURALISM_UNLOCKED_BY_EGALITARIANISM = YES
```

## H. Changements AI

Aucune des six définitions vanilla 1.13.11 ne contenait de condition `has_technology_researched = X` dans son bloc IA. Les blocs `ai_will_do` et `ai_enact_weight_modifier` ont donc été préservés sans modification.

`CITIZENSHIP_AI_TECH_CONDITIONS_CHANGED = 0`.

## I. GUI

`gui/tech_tree.gui` contenait deux feuilles masquant explicitement `egalitarianism` : une pour les arêtes et une pour les cartes. Seules ces deux feuilles ont été retirées des expressions existantes. Les filtres et exceptions de `stock_exchange`, `joint_stock_companies` et de toutes les autres technologies sont inchangés.

```text
EGALITARIANISM_VISIBLE = YES
GUI_FILES_CHANGED = 1
```

## J. Validation

Le contrôle statique de l'overlay effectif donne :

```text
STATIC_VALIDATION = PASS
CITIZENSHIP_LAWS_AUDITED = 6
HIDDEN_ALIAS_COUNT_BEFORE = 44
HIDDEN_ALIAS_COUNT_AFTER = 43
UNKNOWN_TECH_IDS = 0
UNKNOWN_LAW_IDS = 0
DUPLICATE_TECH_IDS = 0
DUPLICATE_LAW_IDS = 0
UNKNOWN_TECH_PREREQUISITES = 0
TECH_TREE_CYCLES = 0
CROSS_CATEGORY_TECH_EDGES = 0
CITIZENSHIP_LAWS_WITH_HIDDEN_GATE = 0
STARTING_TECH_FILES_CHANGED = 0
STARTING_TECH_GRANTS_CHANGED = 0
```

Un smoke de 40 secondes a lancé `victoria3.exe -debug_mode -mod=".../descriptor.mod"`, régénéré `error.log`, puis arrêté uniquement le processus créé pour le test. Le journal frais contient zéro diagnostic ciblant `egalitarianism`, `feminism`, les six IDs de loi, `00_citizenship.txt`, `tech_tree.gui`, une technologie inconnue, un doublon de technologie/loi ou une erreur de parsing. Les diagnostics observés concernent des doublons de localisation, trois textes GUI non localisés et une métadonnée de version préexistante, hors périmètre de cette phase.

```text
PARSER_LOG_SMOKE = PASS
RUNTIME = SMOKE_ONLY
```

Le menu et une partie complète n'ont pas été observés ; aucun runtime gameplay complet n'est revendiqué.

## K. Fichiers modifiés

Fichiers gameplay/GUI de cette phase :

- `common/laws/00_citizenship.txt` — nouveau shadow complet du fichier vanilla 1.13.11, cinq gates modifiés ;
- `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt` — réactivation et topologie d'`egalitarianism` ;
- `gui/tech_tree.gui` — retrait local des deux filtres `egalitarianism`.

Documentation de cette phase :

- `docs/reports/technology/TECH6B3F_CITIZENSHIP_LAW_GATE_RECONCILIATION_REPORT.md` ;
- `docs/reports/technology/TECH6B3F_CITIZENSHIP_LAW_GATE_RECONCILIATION_MATRIX.csv` ;
- addenda append-only dans les rapports TECH6B3E et TECH6B3F de responsabilité des technologies cachées.

`GAMEPLAY_FILES_CHANGED = 2` et `GUI_FILES_CHANGED = 1`, sans compter la documentation. Aucun fichier de starting technologies n'a été modifié par cette phase.
