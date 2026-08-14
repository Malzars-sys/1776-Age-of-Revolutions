# LOG-CLEANUP-1 — Baseline fraîche des logs de la release 2.3.0

Date d'audit : 14 août 2026

Mode : `STATIC / LOG ANALYSIS / DOCUMENTARY ONLY`

Release : `2.3.0`

Commit : `a7055c1d51402df99ce4051e1ff49e7452cbd823`

Tag : `workshop-release-2.3.0-20260814`

## Verdict

```text
LOG_CLEANUP_1 = PASS
FRESH_RUNTIME_AVAILABLE = YES
FRESH_RUNTIME_REQUIRED = NO
DIAGNOSTIC_CORRECTIONS_APPLIED = 0
GAMEPLAY_FILES_CHANGED = 0
TECH_TREE_FILES_CHANGED = 0
COMMIT_CREATED = NO
PUSH_PERFORMED = NO
```

Une génération post-release attribuable au fork publié est disponible. Cette phase l'inventorie et l'attribue sans corriger aucun diagnostic.

## Préflight Git

```text
BRANCH = post-2.3.0-log-cleanup
HEAD = a7055c1d51402df99ce4051e1ff49e7452cbd823
WORKTREE_BEFORE = CLEAN
BASELINE_RELEASE_COMMIT = a7055c1d51402df99ce4051e1ff49e7452cbd823
BASELINE_MATCH = YES
```

Les branches `main` et `cleanup-post-release`, ainsi que leurs références distantes observées pendant le préflight, pointent sur la même release. Aucun fichier préexistant inattendu n'était présent.

## Sources historiques

La comparaison utilise principalement :

- `HOTFIX_6A28_FINAL_RESIDUAL_MERGE_BLOCKER_REINDEX.md` ;
- `HOTFIX_6A28_FINAL_RESIDUAL_DIAGNOSTIC_INVENTORY.csv` ;
- `HOTFIX_6A28_FINAL_RESIDUAL_FAMILY_MATRIX.csv` ;
- `HOTFIX_6A29_FINAL_GLOBAL_RUNTIME_AND_MERGE_READINESS_QA.md` ;
- les manifestes et résultats runtime 6A.29 ;
- les sections 67 et 68 de `HOTFIX_MERGE_COMPLETION_ROADMAP.md` et les entrées correspondantes de l'index Hotfix.

La baseline historique contient 420 identités : 98 parser et 322 `PostValidate`, sur 113 chemins et 65 messages normalisés. Elle est utilisée comme comparateur, jamais comme résultat courant.

## Provenance de la génération actuelle

Le répertoire runtime confirmé est :

```text
C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs
```

La session commence à `18:49:42` heure locale et se ferme proprement à `19:03:36`. Les preuves concordantes sont :

- `system.log` : `release/1.13.9 : afea32b87` ;
- `debug.1.log` : The Great Wave monté ;
- `debug.1.log` : `Age of revolution /Fork|C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` ;
- `debug.1.log` : montage physique du même chemin ;
- aucun autre build local ou Workshop 1776 n'apparaît dans la liste de montage de cette session ;
- les timestamps sont postérieurs au commit de release et cohérents entre `system`, `debug`, `error` et `game`.

```text
VICTORIA_3_VERSION = release/1.13.9 : afea32b87
THE_GREAT_WAVE_MOUNTED = YES
TARGET_FORK_MOUNTED = YES
OTHER_1776_BUILD_MOUNTED = NO
SESSION_START_LOCAL = 2026-08-14T18:49:42+02:00
SESSION_END_LOCAL = 2026-08-14T19:03:36+02:00
```

### Fichiers utiles

| Fichier | Rôle/génération | Taille | Modification UTC | SHA-256 |
|---|---|---:|---|---|
| `debug.1.log` | segment initial courant, montage | 68 689 | 2026-08-14T16:49:51Z | `542285E9D06F2C01E195EED230D31EAAD4619B72413E3138211BB8590F07E78D` |
| `debug.log` | segment diagnostique courant | 319 392 | 2026-08-14T17:03:42Z | `F0C4CEC0FDF3359A967B7338F6B0F92EE6B90A6F2FBB45C48E956731FAC202DC` |
| `error.5.log` | rotation courante la plus ancienne | 524 105 | 2026-08-14T17:00:04Z | `2F87D61776A753DAF17133041DDC0768C2D74C5BEAE16B97A5EDEC57ED322AB5` |
| `error.4.log` | rotation courante | 524 105 | 2026-08-14T17:00:04Z | `2F87D61776A753DAF17133041DDC0768C2D74C5BEAE16B97A5EDEC57ED322AB5` |
| `error.3.log` | rotation courante | 524 105 | 2026-08-14T17:00:04Z | `2F87D61776A753DAF17133041DDC0768C2D74C5BEAE16B97A5EDEC57ED322AB5` |
| `error.2.log` | rotation courante | 524 105 | 2026-08-14T17:00:04Z | `2F87D61776A753DAF17133041DDC0768C2D74C5BEAE16B97A5EDEC57ED322AB5` |
| `error.1.log` | rotation courante | 524 212 | 2026-08-14T17:00:05Z | `3F6708710AD7DD7C5797C2A4BA652EDA1B3AA5BA8338F4DB90B662DC059A7365` |
| `error.log` | dernier segment courant | 28 341 | 2026-08-14T17:00:27Z | `FBF43F9EA0AC3AAF573FB24B21BB168F623417D350CEDDC1BECBE972AEFE9A8D` |
| `game.log` | corroboration runtime, non recomptée | 360 131 | 2026-08-14T17:00:24Z | `D15A972F40F126317798CB79D230249253EAF0D5DB0E9FB0A1EA82BF6B76F5CA` |
| `system.log` | version moteur | 1 101 | 2026-08-14T16:50:02Z | `0C4E9044372D2AF8E70C99E9EC868C80242766BF4F888A34A30D427FE96CCA38` |

`debug.2.log` et les rotations plus anciennes appartiennent à des ouvertures antérieures et sont exclues. Les rotations `error.5.log` à `error.log` portent toutes des timestamps `19:00:04–19:00:27` et appartiennent à la génération courante. `game.log` reflète une partie des mêmes émissions et n'est pas recompté.

## Méthode d'inventaire

La génération est nommée `release_2.3.0_20260814_184942`.

Les lignes entièrement qualifiées sont retenues comme suit :

- `PARSER` : erreur `pdx_persistent_reader` avec chemin et ligne ;
- `POSTVALIDATE_TRIGGER` et `POSTVALIDATE_EFFECT` : ligne complète avec chemin et ligne ;
- `OTHER_ERROR` : enregistrements de la génération courante d'`error.5.log` à `error.log`, avec rattachement de leurs continuations `Script location` ;
- `WARNING` : aucune identité n'est promue. Les émissions génériques de debug, dont les doublons de localisation, sont surveillées mais n'ont pas de sévérité stable comparable à la baseline 6A.28 et ne sont pas assimilées automatiquement à des erreurs corrigeables.

La clé déterministe reste `generation + normalized_message + path + line`. Pour les erreurs runtime sans chemin, elle est étendue par le contexte explicite fourni par le log (`country:<tag>` ou `achievement:<id>`), faute de quoi 234 objets distincts seraient artificiellement fusionnés.

Les occurrences répétées d'une même identité sont agrégées dans `count`. C'est notamment nécessaire pour l'erreur stratégique de `00_default_strategy.txt:5078`, répétée 14 163 fois.

## Compteurs actuels

Les compteurs principaux portent sur les identités uniques ; les occurrences brutes sont conservées séparément.

| Type | Identités | Occurrences |
|---|---:|---:|
| `PARSER` | 109 | 109 |
| `POSTVALIDATE_TRIGGER` | 189 | 221 |
| `POSTVALIDATE_EFFECT` | 22 | 22 |
| `OTHER_ERROR` | 238 | 14 400 |
| `WARNING` promu | 0 | 0 |
| **Total** | **558** | **14 752** |

```text
CURRENT_TOTAL_DIAGNOSTICS = 558
CURRENT_TOTAL_OCCURRENCES = 14752
CURRENT_PARSER = 109
CURRENT_POSTVALIDATE = 211
CURRENT_POSTVALIDATE_TRIGGER = 189
CURRENT_POSTVALIDATE_EFFECT = 22
CURRENT_OTHER_ERROR = 238
CURRENT_WARNING = 0
CURRENT_UNIQUE_PATHS = 79
CURRENT_UNIQUE_NORMALIZED_MESSAGES = 90
```

## Comparaison avec les 420 identités 6A.28/6A.29

La comparaison exacte est limitée aux 320 identités parser/PostValidate, car l'inventaire historique n'incluait pas `error.log`. Les 238 identités `OTHER_ERROR` sont donc `UNCOMPARABLE`, pas artificiellement déclarées nouvelles.

| Statut | Identités actuelles |
|---|---:|
| `CURRENT_AND_HISTORICAL` | 271 |
| `HISTORICAL_CHANGED` | 28 |
| `CURRENT_NEW` | 21 |
| `UNCOMPARABLE` | 238 |

```text
HISTORICAL_420_REPRODUCED = 271
HISTORICAL_420_NOT_REPRODUCED = 149
NEW_IDENTITIES = 21
CHANGED_IDENTITIES = 28
UNCOMPARABLE_CURRENT_IDENTITIES = 238
```

Les 28 identités actuelles déplacées correspondent à 29 anciennes identités de même type/message/chemin mais à une ligne différente. Parmi les 149 anciennes clés non reproduites exactement, 120 n'ont plus de lignée courante. Leur absence n'est pas déclarée corrigée : plusieurs chemins ont changé depuis 6A.29 et la session n'exerce pas nécessairement tous les contextes historiques.

Les 21 nouvelles identités comparables comprennent :

- 11 erreurs parser `country_law_enactment_time_mult` dans cinq fichiers présents dans le fork ;
- cinq diagnostics PostValidate absents du fork et présents dans vanilla ;
- cinq nouveaux PostValidate d'effets dans des overrides du fork, encore à auditer.

## Attribution primaire

Chaque identité possède exactement une classification primaire.

| Classification | Identités |
|---|---:|
| `FORK_ATTRIBUTABLE_FIXABLE` | 15 |
| `FORK_ATTRIBUTABLE_SEMANTIC_REWRITE` | 45 |
| `INTENTIONAL_FORK_DIVERGENCE` | 11 |
| `VANILLA_OR_EXTERNAL` | 175 |
| `ALREADY_ACCOUNTED_FOR` | 194 |
| `NEEDS_RUNTIME_REPRODUCTION` | 113 |
| `UNKNOWN_REQUIRES_AUDIT` | 5 |
| **Total** | **558** |

```text
CLASSIFICATION_SUM = 558
UNCLASSIFIED_DIAGNOSTICS = 0
DUPLICATE_PRIMARY_CLASSIFICATIONS = 0
```

### Présence physique

| Fork | Vanilla | Identités |
|---|---|---:|
| `YES` | `YES` | 252 |
| `YES` | `NO` | 18 |
| `NO` | `YES` | 54 |
| `UNKNOWN` | `UNKNOWN` | 234 |

Les 234 valeurs inconnues correspondent aux 113 validations de lois par pays et aux 121 identifiants d'achievements, qui ne fournissent aucun chemin de script. Elles ne sont pas transformées en overrides fictifs.

## Familles prioritaires

Les 15 identités corrigeables se répartissent en :

| Famille | Diagnostics | Chemins | Origine |
|---|---:|---:|---|
| `API_COUNTRY_CONVOYS_CAPACITY_MULT` | 1 | 1 | backlog post-merge historique |
| `API_CREATE_CHARACTER` | 2 | 1 | backlog post-merge historique |
| `API_HAS_TECHNOLOGY_RESEARCHED` | 1 | 1 | backlog post-merge historique |
| `LEGACY_LAW_ENACTMENT_MODIFIER` | 11 | 5 | nouvelles identités parser |

La matrice conserve séparément les familles sémantiques, intentionnelles, vanilla/externes, déjà comptabilisées et encore insuffisamment attribuées. Aucune correction n'est appliquée dans LOG-CLEANUP-1.

Les cinq identités `UNKNOWN_REQUIRES_AUDIT` sont deux `add_modifier` dans `morocco_makhzen_events.txt` et trois `add_enactment_modifier` dans `00_lobbies_events_03.txt`. Les fichiers existent dans le fork et vanilla mais divergent ; le log seul ne permet pas d'identifier le hunk responsable.

## Dettes connues vérifiées

- `state_religion` : aucune occurrence dans la génération sélectionnée ;
- `building_naval_base` : aucune occurrence dans la génération sélectionnée ;
- institutions legacy : deux PostValidate `set_institution_investment_level`, dont une dans HBC et une dans Oregon ;
- HBC : une identité actuelle, conservée dans son statut historique ;
- `00_default_strategy.txt:5078` : 14 163 occurrences d'`Invalid right side during comparison 'sr'`, déjà documentées et regroupées en une identité `ALREADY_ACCOUNTED_FOR`.

Une absence de log n'est pas une preuve de correction définitive.

## Limites

- Le runtime prouve le montage du bon chemin et de Victoria 3 1.13.9, mais le log n'encode pas le SHA Git ; l'association à `a7055c1` repose aussi sur le préflight Git propre au même chemin.
- Les 113 erreurs de rétention de lois nomment un pays et une loi mais pas leur fichier source effectif ; elles exigent une reproduction ciblée avant correction.
- Les lignes déplacées sont rapprochées par type + message + chemin. Ce rapprochement n'affirme pas que l'objet script est inchangé.
- Les warnings génériques de debug restent hors compteur principal pour éviter de mélanger une nouvelle taxonomie avec la baseline historique sans règle de sévérité fiable.
- Le Tech Tree et `docs/research/technology/` restent entièrement hors périmètre.

## Prochaine phase proposée

```text
NEXT_PHASE = LOG-CLEANUP-2-CONVOYS-CAPACITY-MODIFIER
```

Cette famille contient une seule identité parser, déjà classée `POST_MERGE_BACKLOG` par 6A.28, dans `common/company_types/02_new_companies.txt:53`. La phase suivante devra d'abord établir la sémantique et le remplacement 1.13 exacts, puis seulement proposer une correction bornée et son contrôle runtime. Elle est plus petite que les 11 occurrences `country_law_enactment_time_mult` et n'implique pas la refonte du Tech Tree.

LOG-CLEANUP-2 n'est pas commencé.
