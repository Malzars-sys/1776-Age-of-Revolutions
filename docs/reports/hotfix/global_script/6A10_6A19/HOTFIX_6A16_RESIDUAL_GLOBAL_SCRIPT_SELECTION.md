# HOTFIX-6A.16 — Sélection documentaire du prochain résidu global

Date : 30 juillet 2026

Phase : `HOTFIX_6A16_RESIDUAL_GLOBAL_SCRIPT_SELECTION`

Branche : `hotfix-dlc-audit`

HEAD initial et final attendu :
`fd74a88e9bd4ed67bbb49ffa80e7162da008c022` —
`Align Coup journal entry pinning with 1.13`

## 1. Verdict

La réindexation post-6A.15F et la comparaison trois voies sont terminées.
Une seule phase est sélectionnée :

```text
NEXT_EXECUTION_PHASE = HOTFIX_6A16R_COUP_EVENT_APIS_1_13_FUNCTIONAL_AUDIT
```

Il s'agit d'un audit statique en lecture seule des API obsolètes dans :

- `events/iberia_events/ip4_coup_events.txt`;
- `events/agitators_events/coup_events.txt`.

6A.16 ne modifie aucun gameplay, ne lance aucun runtime et n'autorise encore
aucune correction de ces deux fichiers.

## 2. Préflight et protections

| Contrôle | Résultat |
| --- | --- |
| Racine | fork exact |
| Branche | `hotfix-dlc-audit` |
| HEAD | `fd74a88` |
| Sujet HEAD | `Align Coup journal entry pinning with 1.13` |
| Rapport 6A.15F dans `HEAD` | PASS |
| Verdicts 6A.15F dans `HEAD` | PASS |
| Hash gameplay 6A.15F | `37C2669619CD26C30450F41082716BF30CA12949AA5FEE59BA0D25D498339602` |
| Fichiers suivis | propres |
| Index staged | vide |
| Non-suivis | uniquement `bject` et sept recherches technologiques |
| `git diff --check` | PASS |
| Victoria 3 et launcher Paradox | fermés |

Le stash protégé reste exactement :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
```

Objet :
`518df704fa14599c0f254fae13859210663dd976`.

Son contenu n'a pas été inspecté. Aucun `git add`, commit, reset, restore,
checkout, clean, merge, rebase, amend ou changement de stash n'a été exécuté.

## 3. Sources documentaires

Ont été rapprochés :

- les rapports canoniques 6A.13 à 6A.15F;
- la roadmap et les deux CSV de navigation;
- les inventaires global, trois voies et travail restant;
- les changelogs complets du fork et de la source hotfix;
- le fork, la source hotfix et vanilla 1.13 pour les candidats ciblés;
- les journaux courants `debug.1.log` et `debug.log`, sans produire de
  nouveau log.

Les CSV ont été lus avec leurs en-têtes réels et validés par parsing :

| CSV | Dimensions avant 6A.16 | Lignes nulles | Clés dupliquées |
| --- | ---: | ---: | ---: |
| `HOTFIX_MERGE_BLOCK_STATUS.csv` | `41 × 17` | 0 | 0 |
| `HOTFIX_REPORT_INDEX.csv` | `128 × 22` | 0 | 2 groupes historiques (`S`, `INDEX`) |
| `HOTFIX_MERGE_THREE_WAY_INVENTORY.csv` | `541 × 21` | 0 | 0 |
| `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` | `534 × 22` | 0 | 0 |
| `HOTFIX_MERGE_REMAINING_WORK.csv` | `512 × 20` | 0 | 0 |

## 4. Réindexation des diagnostics

La session courante reste partagée entre `debug.1.log` et `debug.log`.
Les rotations historiques ne sont pas additionnées aux comptes courants.

Méthode de déduplication : suppression des horodatages, conservation du
composant et du message exact, y compris fichier et ligne lorsqu'ils sont
présents.

| Mesure | Résultat |
| --- | ---: |
| Enregistrements de composants script actuels | 1 233 |
| Diagnostics script actuels dédupliqués | 1 189 |
| Occurrences avec chemin `.txt` extractible | 1 537 |
| Fichiers avec chemin extractible | 310 |
| Pinning legacy `should_be_pinned_by_default` | 373 |
| Fichiers de pinning legacy | 139 |
| Pinning ciblé de `01_coup.txt` | 0 |

La baseline de pinning 6A.15F `373/139` est donc confirmée. Les diagnostics
d'événements Coup sont distincts du pinning déjà clos.

## 5. Inventaire canonique

La classification exclusive des 161 anciennes lignes reste inchangée :

| Catégorie | Lignes |
| --- | ---: |
| `REQUIRED_HOTFIX_DELTA` | 7 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 15 |
| `ALREADY_MERGED` | 19 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 |
| `PROTECTED_CONCURRENT_WORK` | 19 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 |
| **Total** | **161** |

6A.15F ferme un sous-delta dans une ligne qui conserve d'autres écarts
fonctionnels; elle ne justifie donc pas un déplacement de catégorie.

## 6. Matrice de priorité résiduelle

| Candidat | Diagnostics actuels | Taille fonctionnelle | Classement | Décision |
| --- | ---: | --- | --- | --- |
| API d'événements Coup | 16, 2 fichiers, 7 objets, environ 9 groupes API | bornable par audit; convergence partielle source/vanilla | `VANILLA_1_13_ALIGNMENT_REQUIRED`, avec deltas adjacents à séparer | **sélectionné pour audit** |
| Chaîne Coup `.11` / lobby / sponsor / cleanup | 1 avertissement courant, 3 traces historiques | chaîne multi-entrypoints héritée | `VANILLA_1_13_ALIGNMENT_REQUIRED`, intention fonctionnelle à résoudre | différé après l'audit API |
| `04_imperialism_of_promise.txt` | 3 dans un objet | couplage BIC/Inde, rôles et progression | mélange `VANILLA_1_13_ALIGNMENT_REQUIRED`, `UNKNOWN_REQUIRES_REVIEW` et `PROTECTED_CONCURRENT_WORK` | exclu |
| `00_interests.txt` | 91 | fichier custom sans référence vanilla | `UNKNOWN_REQUIRES_REVIEW` | trop peu prouvé |
| grands fichiers événements, tutoriel et on_actions | plusieurs dizaines chacun | dizaines à centaines de hunks | `UNKNOWN_REQUIRES_REVIEW` | non atomiques |

Le nombre brut d'erreurs ne suffit pas à choisir un lot. Coup est prioritaire
car les 16 diagnostics sont actuels, reliés à une chaîne déjà cartographiée en
6A.15R et concentrés dans deux fichiers comparables trois voies.

## 7. Candidat sélectionné : API d'événements Coup

### 7.1 `ip4_coup_events.txt`

| Version | SHA-256 |
| --- | --- |
| Fork | `8DD5A07F60A3E1C623CF48495B062AFE0388602E256CBA8384CD8540067B5AD2` |
| Source hotfix | `F806A772F86EB379EBC7ED05F7808A5B16C0CACFC0CD784E94B6AA1FB9C8C9D4` |
| Vanilla 1.13 | `22A7B94EE4A0CB4DA7C31DA2F488CEB845473EBDF44EB32ED649F56200886E92` |

Les huit diagnostics courants sont des échecs PostValidate de `has_role` aux
lignes fork 30, 31, 56, 57, 321, 332, 426 et 432. Ils concernent
`ip4_coup.1` et `ip4_coup.2`.

La source et vanilla utilisent `has_role_of_type`, mais ne convergent pas sur
les huit conditions du fork : la source moderne n'en conserve que six. Le
diff complet contient 37 hunks fork/source et 33 hunks fork/vanilla. Une
substitution mécanique globale n'est donc pas autorisée.

### 7.2 `coup_events.txt`

| Version | SHA-256 |
| --- | --- |
| Fork | `88D1B0AE45F296A84FBB997C3F089423A2240790742291DDE359A9509DA5F3CE` |
| Source hotfix | `AEE3D155D3C347AC5338468F5814CC5DAAFCBB9862E801D3287643587D525990` |
| Vanilla 1.13 | `F1CD65506555E45D1C08C27EAA96EE6939F94D313DC44DFC2B20DD4E3106CB7F` |

Les huit diagnostics courants sont :

- deux échecs PostValidate de `has_role` dans `coup_pulse_events.1`;
- six `Unknown trigger type: is_ruler`, dont deux dans
  `coup_pulse_events.1` et quatre dans `coup_aftermath_events.1` à `.4`.

Source et vanilla convergent sur les formes modernes
`has_role_of_type = general` et `is_ruler_of_own_country`. Elles divergent
toutefois sur des garde-fous adjacents tels que
`is_heir_of_own_country`, `character_is_valid_for_events`, le groupe d'intérêt
optionnel et d'autres effets fonctionnels. Le diff complet contient 12 hunks
fork/source et 9 hunks fork/vanilla.

### 7.3 Bornage de 6A.16R

La phase sélectionnée doit décider chaque groupe séparément et distinguer :

1. remplacement direct d'API obsolète;
2. changement de formule ou de sélection de personnage;
3. garde-fou source-only;
4. chaîne `.11`, sponsor, lobby, scopes et cleanup;
5. changement de design ou d'équilibrage.

Elle ne doit appliquer aucun hunk et ne doit pas présumer que les deux fichiers
seront corrigés ensemble.

## 8. Candidats non sélectionnés

`04_imperialism_of_promise.txt` conserve trois diagnostics, dont un ancien
pinning et deux `has_role`. Ses branches sont liées à BIC, à l'Inde, à la
géographie, à la progression et aux événements utilitaristes. Source et
vanilla ne convergent pas exactement sur le rôle de chef de groupe d'intérêt.
Une isolation de pinning seule laisserait deux erreurs et rouvrirait une dette
protégée.

La chaîne Coup `.11` est fonctionnellement pertinente mais plus large :
`ip4_coup.11`, `orchestrate_coup`, `coup_lobby`, scopes sponsor et cleanup
sont absents du fork override alors que des entrypoints vanilla hérités les
référencent. Elle doit rester séparée de la décision sur les 16 API explicites.

Les 91 diagnostics `add_declared_interest` dans `00_interests.txt` n'ont pas
de remplacement moderne prouvé par vanilla. Les grands fichiers d'événements,
de tutoriel et d'on_actions dépassent le niveau de confiance requis pour une
prochaine phase bornée.

## 9. Blocs clos et protections

Restent clos : DEI/VOC/Java, Balkan National Awakening, Yugoslavia,
Risorgimento, nationalisme grec, Grande Crise orientale, Sick Man, Romania,
Portugal, Merchant Banking et le pinning de `je_ip4_coup`.

Restent protégés : NAVY, MARATH, ADMIN, technologies, HBC, Navigation Acts,
Inde/BIC/Sepoy/Bombay/Travancore, Japon, Russie, Autriche/Croatie/Suisse,
révolutions américaine et française, localisations françaises générales,
descripteurs, sauvegardes, `bject`, recherches technologiques et stash.

HBC reste `HBC_DUPLICATE_HISTORY_UNKNOWN_REQUIRES_REVIEW`; aucune 6A.14HF
n'est réouverte. Navigation Acts reste bloquée; aucune 6A.14F n'est réouverte.

## 10. Fichiers documentaires

6A.16 crée ou modifie exactement six documents :

1. ce rapport;
2. `docs/reports/hotfix/INDEX.md`;
3. `HOTFIX_REPORT_INDEX.csv`;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv`;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun fichier gameplay n'est modifié.

## 11. Verdicts

```text
HOTFIX_6A16_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE
POST_6A15F_RESIDUAL_DIAGNOSTICS_REINDEXED
RESIDUAL_CANDIDATE_PRIORITY_MATRIX_COMPLETE
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
COUP_EVENT_APIS_1_13_AUDIT_SELECTED
NEXT_EXECUTION_PHASE = HOTFIX_6A16R_COUP_EVENT_APIS_1_13_FUNCTIONAL_AUDIT
```
