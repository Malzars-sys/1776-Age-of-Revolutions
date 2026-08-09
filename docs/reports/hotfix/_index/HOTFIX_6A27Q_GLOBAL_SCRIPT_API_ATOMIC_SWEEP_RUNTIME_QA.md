# HOTFIX-6A.27Q — QA runtime consolidée du sweep atomique global des API script

Date : 9 août 2026

Branche : `hotfix-dlc-audit`

Commit gameplay validé : `90f696832ff736886be7bfd6f21ae724601682f4`

Mode : une ouverture humaine unique, aucun changement gameplay

## 1. Résultat

Une seule ouverture humaine de Victoria 3 valide ensemble les six familles d’API corrigées par 6A.27. Les 609 identités ciblées disparaissent toutes, aucune identité nouvelle n’apparaît et les 87 fichiers gameplay conservent exactement leur SHA-256 engagé.

La baseline fraîche réellement mesurée contient 420 diagnostics, soit exactement `1029 - 609`. Ce résultat n’est pas présumé : il est reconstruit depuis les segments frais prouvés par les manifestes avant/après.

```text
TOTAL_TARGET_API_DIAGNOSTICS_BEFORE = 609
TOTAL_TARGET_API_DIAGNOSTICS_AFTER = 0
NEW_6A27_ATTRIBUTABLE_ERRORS = 0
GAMEPLAY_HASHES_CHECKED = 87
GAMEPLAY_HASHES_MATCH = 87
GAMEPLAY_HASHES_CHANGED_DURING_RUNTIME = 0
HUMAN_RUNTIME_LAUNCHES = 1
```

## 2. Préflight et protections

Le HEAD porte le message exact `Migrate proven script API families for 1.13`. L’arbre suivi et l’index étaient propres ; seuls les sept fichiers de recherche technologique protégés étaient non suivis. `bject` était absent et n’a pas été recréé. Le stash NAVY-3C-3 est resté au hash `518df704fa14599c0f254fae13859210663dd976`.

Le CSV 6A.27 contient 695 lignes `SAFE_CANDIDATE_APPLIED` et 87 chemins uniques. Avant lancement, les 87 hashes correspondaient à `sha_after_actual` ; après fermeture, ils correspondent encore tous.

Afghanistan reste au hash `C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13`. Pologne reste au hash canonique `A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A`. La valeur Pologne divergente terminée par `C32EC22` dans la consigne opérateur est une coquille documentaire explicitement écartée ; aucun gameplay n’a été modifié.

BIC conserve `activate_law = law_type:law_frontier_colonization` et son fichier pays ne contient pas `law_colonial_exploitation`. Les 127 exceptions API et les 14 exceptions pinning restent séparées et inchangées. Le bloc pinning demeure fermé.

## 3. Ouverture humaine unique

L’opérateur a ouvert Victoria 3 une seule fois, confirmé le fork et la version demandés, créé une nouvelle partie Vietnam en 1776 sans console ni contenu forcé, puis avancé jusqu’au 11 janvier 1776. Aucune clé brute, aucun crash, aucune interface manifestement cassée ni anomalie majeure immédiate n’a été observé.

Le processus `victoria3.exe` a fini de se fermer naturellement huit secondes après la première vérification post-session. Le manifeste final n’a été capturé qu’après disparition de Victoria 3, Dowser et Paradox Launcher ; aucun second lancement n’a eu lieu.

Les logs confirment :

```text
fork monté = C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork
version = release/1.13.0 : d9ade554e
Transition Empty->Game = 1
Quit from inside game = 1
Transition Game->Empty = 1
players supprimés à la fermeture = 1
```

## 4. Manifestes et génération fraîche

Le manifeste avant lancement a été capturé à `21:06:24 UTC` : 60 fichiers et 10 271 648 octets. Le manifeste après fermeture a été capturé à `21:18:50 UTC` : 60 fichiers et 9 632 960 octets. Chaque ligne contient le chemin complet, le nom, la taille, la date de modification et le SHA-256 dans [HOTFIX_6A27Q_LOG_MANIFEST.csv](HOTFIX_6A27Q_LOG_MANIFEST.csv).

La comparaison trouve 49 chemins renouvelés ou déplacés, 11 inchangés et aucune création ou suppression. Les rotations `debug` sont prouvées par :

```text
after debug.2 = before debug
after debug.3 = before debug.1
after debug.4 = before debug.2
after debug.5 = before debug.3
```

Les deux segments frais de l’unique ouverture sont :

```text
debug.1.log = D2A5C169C60D4F21DD2399088C9478ABB552D1C4DFD35E2AF26912B3759AC2EE
debug.log   = AF31A9F15398F729AF9816043869F889CA31B8934FD0BD94FBCB6A7917DA2CAF
```

`debug.1.log` contient le montage initial du fork ; `debug.log` contient le chargement principal, les diagnostics, l’entrée en jeu et la fermeture.

## 5. Normalisation et baseline réelle

La règle appliquée est `generation + normalized_message + path + line`. Les erreurs parser entièrement qualifiées sur une ligne et les lignes `PostValidate` sont retenues ; les continuations multilignes ne sont pas recomptées.

Le même parseur appliqué à `debug.2.log`, dont le hash correspond au `debug.log` canonique 6A.25Q, reproduit exactement les 1 029 lignes de l’inventaire 6A.26 : aucune identité manquante ou supplémentaire. Appliqué à `debug.log` frais, il mesure :

| Génération fraîche | Identités |
|---|---:|
| parser | 98 |
| `PostValidate` | 322 |
| total | 420 |

```text
FRESH_TOTAL_DIAGNOSTICS_AFTER_6A27Q = 420
FRESH_PARSER_DIAGNOSTICS_AFTER_6A27Q = 98
FRESH_POSTVALIDATE_DIAGNOSTICS_AFTER_6A27Q = 322
FRESH_PATHS_AFTER_6A27Q = 113
FRESH_NORMALIZED_MESSAGES_AFTER_6A27Q = 65

IDENTITIES_DISAPPEARED = 609
IDENTITIES_APPEARED = 0
IDENTITIES_UNCHANGED = 420
GLOBAL_RESIDUAL_DIAGNOSTICS = 420
```

## 6. Six cohortes ciblées

| Famille | Historique ciblé | Frais ciblé | Verdict |
|---|---:|---:|---|
| `API_HAS_ROLE` | 434 | 0 | `PASS` |
| `API_IS_RULER` | 149 | 0 | `PASS` |
| `API_HAS_AMENDMENT` | 12 | 0 | `PASS` |
| `API_IS_HEIR` | 8 | 0 | `PASS` |
| `API_IS_IN_GEOGRAPHIC_REGION` | 4 | 0 | `PASS` |
| `API_ANY_COUNTRY_IN_IBERIA` | 2 | 0 | `PASS` |
| **Total** | **609** | **0** | **PASS** |

La matrice exhaustive des 135 couples famille/fichier se trouve dans [HOTFIX_6A27Q_GLOBAL_SCRIPT_API_RUNTIME_RESULTS.csv](HOTFIX_6A27Q_GLOBAL_SCRIPT_API_RUNTIME_RESULTS.csv). Elle inclut aussi les quatre fichiers dont les substitutions étaient sûres mais sans diagnostic historique ciblé.

Sept fichiers du sweep portent encore 23 identités indépendantes : une erreur parser et 22 `PostValidate`. Elles appartiennent aux familles résiduelles déjà séparées, sont inchangées par rapport à 6A.25Q et ne constituent ni une régression ni un échec de la cible `609 → 0`. Aucun de ces fichiers n’est déclaré entièrement terminé.

## 7. Hashes et exceptions

Les 87 SHA-256 après runtime sont identiques aux hashes engagés. Victoria 3 n’a modifié aucun gameplay. Les douze indentations historiques espace+tab de `events/balkans_events/bavarocracy.txt` restent volontairement intactes ; aucun reformatage n’a eu lieu.

```text
BOUNDED_API_EXCEPTIONS = 127
BOUNDED_PINNING_EXCEPTIONS = 14
GAMEPLAY_HASHES_CHECKED = 87
GAMEPLAY_HASHES_MATCH = 87
GAMEPLAY_HASHES_CHANGED_DURING_RUNTIME = 0
```

## 8. Suite sélectionnée

Le sweep atomique multi-API est fermé avec ses exceptions bornées. Aucune correction suivante n’est commencée. La seule phase sélectionnée est la réindexation statique finale des 420 diagnostics afin de déterminer le nombre réel de bloqueurs du merge :

```text
NEXT_EXECUTION_PHASE = HOTFIX_6A28_FINAL_RESIDUAL_MERGE_BLOCKER_REINDEX
```

## 9. Verdicts

```text
HOTFIX_6A27Q_GLOBAL_SCRIPT_API_ATOMIC_SWEEP_RUNTIME_QA_COMPLETE
GLOBAL_MULTI_API_ATOMIC_SWEEP_RUNTIME_PASS
GLOBAL_MULTI_API_TARGET_DIAGNOSTICS_609_TO_0
GLOBAL_MULTI_API_NO_NEW_ATTRIBUTABLE_ERRORS
GLOBAL_MULTI_API_GAMEPLAY_HASHES_87_OF_87_PRESERVED
GLOBAL_MULTI_API_SIX_FAMILIES_RUNTIME_VALIDATED
GLOBAL_MULTI_API_BOUNDED_EXCEPTIONS_127_PRESERVED
GLOBAL_PINNING_FAMILY_REMAINS_CLOSED
PINNING_14_BOUNDED_EXCEPTIONS_PRESERVED
AFGHANISTAN_BLOCK_REMAINS_CLOSED
POLAND_BLOCK_REMAINS_CLOSED
BIC_PROTECTIONS_PRESERVED
ONE_HUMAN_RUNTIME_ONLY
NO_GAMEPLAY_CHANGED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_EXECUTION_PHASE = HOTFIX_6A28_FINAL_RESIDUAL_MERGE_BLOCKER_REINDEX

FRESH_TOTAL_DIAGNOSTICS_AFTER_6A27Q = 420
FRESH_PARSER_DIAGNOSTICS_AFTER_6A27Q = 98
FRESH_POSTVALIDATE_DIAGNOSTICS_AFTER_6A27Q = 322
FRESH_PATHS_AFTER_6A27Q = 113
FRESH_NORMALIZED_MESSAGES_AFTER_6A27Q = 65
```
