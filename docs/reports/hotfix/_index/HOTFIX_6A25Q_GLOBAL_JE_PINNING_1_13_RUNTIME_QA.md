# HOTFIX-6A.25Q — QA runtime consolidée globale des pinning 1.13

Date : 9 août 2026
Branche : `hotfix-dlc-audit`
HEAD testé : `b13fff5b06c01064172ee33a075ad4beddec31f3` — `Migrate proven journal entry pinning properties for 1.13`
Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé
Ouvertures humaines de Victoria 3 : **1**

## 1. Résultat

La QA consolidée passe. L'unique ouverture humaine a monté le fork exact sous
Victoria 3 `release/1.13.0 : d9ade554e`, puis une partie neuve 1776 avec le
Vietnam a été jouée jusqu'au 5 janvier. L'opérateur n'a observé aucune clé brute
ni anomalie, puis a fermé le jeu et le launcher. Aucune journal entry n'a été
forcée et aucun contenu n'a été déclenché par console.

```text
TOTAL_TARGET_PINNING_DIAGNOSTICS_BEFORE = 355
TOTAL_TARGET_PINNING_DIAGNOSTICS_AFTER = 0
NEW_PINNING_REGRESSIONS = 0
NEW_6A25_ATTRIBUTABLE_NORMALIZED_ERRORS = 0
GAMEPLAY_HASHES_CHANGED_DURING_RUNTIME = 0
```

Cette validation porte sur le chargement et le parser de la migration. Aucun
comportement UI d'une journal entry non naturellement visible n'est revendiqué.

## 2. Préflight et protections

Le préflight a confirmé la branche et le HEAD attendus, un arbre suivi propre,
un index vide, `git diff --check` propre et uniquement les huit non-suivis
protégés connus. Aucun processus Victoria 3, Dowser ou Paradox Launcher n'était
actif. Le stash supérieur est resté exactement :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

L'inventaire 6A.25 a été parsé intégralement : 399 occurrences, 28 colonnes,
356 corrections réparties dans 129 fichiers et 14 exceptions D. Les hashes des
129 fichiers ont été dérivés automatiquement de `sha_after`, sans liste codée
manuellement, puis tous vérifiés avant le lancement. Les contrôles particuliers
étaient conformes :

```text
00_german_unification.txt = 30A3F3356AA43060C0E8D315DDF34D8D304680290134E0212AE6AEB852C8F239
03_afghanistan.txt         = C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13
00_poland.txt              = A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A
```

Les protections BIC sont intactes : une occurrence
`law_type:law_frontier_colonization`, aucune
`law_colonial_exploitation`. NAVY, ADMIN, MARATH, les non-suivis protégés et les
14 exceptions n'ont pas été modifiés.

## 3. Manifestes et génération fraîche

Le manifeste avant lancement a été capturé à `18:43:54 UTC` : 60 fichiers et
8 135 387 octets. Le manifeste après fermeture a été capturé à `18:58:14 UTC` :
60 fichiers et 10 271 648 octets. Les deux instantanés contiennent pour chaque
log le chemin, la taille, la date de modification et le SHA-256 ; leur registre
durable est `HOTFIX_6A25Q_LOG_MANIFEST.csv`.

La comparaison trouve 49 fichiers renouvelés ou déplacés, 11 inchangés et
aucune création ou suppression. La rotation est démontrée par l'égalité des
hashes `after debug.2 = before debug`, `after debug.3 = before debug.1`,
`after debug.4 = before debug.2` et `after debug.5 = before debug.3`. Les seuls
segments frais de l'ouverture sont donc `debug.1.log` et `debug.log` : le
premier contient le montage initial, le second le chargement principal.

`debug.1.log` nomme et monte exactement :

```text
C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork
```

Les segments système donnent `release/1.13.0 : d9ade554e`. Le journal principal
contient `Transition Empty->Game`, la création d'un joueur, `Quit from inside
game`, puis `Transition Game->Empty` et la suppression d'un joueur. Il s'agit de
deux segments techniques d'une seule ouverture humaine, pas de deux lancements.

## 4. Normalisation des diagnostics

La règle est `generation + normalized_message + path + line`. Comme en 6A.23,
les erreurs persistantes entièrement qualifiées sur une ligne et les lignes
`PostValidate` sont retenues ; les continuations d'erreurs multilignes ne sont
pas recomptées comme des diagnostics autonomes.

| Génération fraîche | Identités | Chemins | Messages |
|---|---:|---:|---:|
| parser | 257 | 68 | 45 |
| `PostValidate` | 772 | 157 | 22 |
| total dédupliqué | 1 029 | 189 | 67 |

La baseline canonique 6A.23 comptait 1 384 identités : 612 parser et 772
`PostValidate`. La nouvelle génération conserve exactement les 772
`PostValidate` et les 257 diagnostics parser non corrigés. La comparaison
canonique reconstruite donne donc 355 disparitions, 0 apparition et 1 029
identités inchangées. Les seules disparitions sont la cohorte pinning corrigée.

La génération immédiatement précédente dans la rotation ne porte aucun signal
de montage du fork et ne contient aucune identité comparable. Sa comparaison
brute (`1 029` apparues, `0` disparue, `0` inchangée) est conservée comme donnée
documentaire uniquement et n'est pas utilisée pour attribuer le verdict 6A.25.

## 5. Test principal et matrice par fichier

Les 355 diagnostics historiques ciblés sont dérivés des lignes corrigées dont
`fresh_diagnostic=true` dans l'inventaire. La 356e substitution PLC reste
correctement absente de cette baseline, car elle était masquée par l'erreur de
parsing antérieure. Dans la génération fraîche :

```text
Unexpected token: should_be_pinned_by_default (cohorte corrigée) = 0
rejet de should_be_pinned_by_default_uninvolved_or_context       = 0
nouvelle identité attribuable à 6A.25                             = 0
```

La matrice exhaustive des 129 fichiers se trouve dans
`HOTFIX_6A25Q_GLOBAL_JE_PINNING_RUNTIME_RESULTS.csv`. Elle contient pour chaque
fichier les diagnostics historiques ciblés, les diagnostics frais ciblés, les
autres diagnostics parser et `PostValidate`, les nouvelles identités
attribuables, les hashes engagés et après runtime, et le verdict borné. Tous les
fichiers passent pour le pinning ; un verdict ne prétend pas fermer les autres
API résiduelles du fichier.

## 6. Exceptions bornées

Les 14 diagnostics legacy encore présents correspondent exactement, chemin et
ligne, aux 14 `PINNING_ATOMICITY_EXCEPTION` de l'inventaire : 12 contradictions
booléennes documentaires et deux protections BIC. Il n'existe aucune exception
supplémentaire, aucune régression pinning et aucune justification pour ouvrir
automatiquement quatorze micro-phases. Les exceptions restent inchangées et
séparées de la cible `355 → 0`.

## 7. Validation post-runtime

Les 129 hashes recalculés après fermeture correspondent tous au commit 6A.25 ;
le nombre de hashes gameplay modifiés est zéro. Les hashes allemand, afghan et
polonais restent ceux attendus. L'arbre suivi est demeuré propre jusqu'à
l'écriture de cette documentation, l'index Git est vide et le stash NAVY-3C-3
conserve son hash. Aucun fichier gameplay n'a été écrit par cette QA.

Le bloc global de pinning est fermé avec ses 14 exceptions bornées. Les cinq
pinning allemands sont validés dans cette QA globale ; la phase 6A.24F reste
`SUPERSEDED_NOT_EXECUTED`. Les blocs Afghanistan et Pologne restent clos.

Aucune prochaine phase d'exécution n'est sélectionnée ici. La future opération,
si l'opérateur l'autorise, devra être une réindexation globale consolidée des
diagnostics résiduels non-pinning, suivie d'un regroupement par famille d'API,
et non une correction fichier par fichier.

## 8. Verdicts

```text
HOTFIX_6A25Q_GLOBAL_JE_PINNING_1_13_RUNTIME_QA_COMPLETE
GLOBAL_JE_PINNING_RUNTIME_PASS
GLOBAL_JE_PINNING_TARGET_DIAGNOSTICS_355_TO_0
GLOBAL_JE_PINNING_NO_NEW_ATTRIBUTABLE_ERRORS
GLOBAL_JE_PINNING_GAMEPLAY_HASHES_PRESERVED
GLOBAL_JE_PINNING_ATOMIC_MIGRATIONS_RUNTIME_VALIDATED
GERMAN_UNIFICATION_FIVE_JE_PINNING_RUNTIME_VALIDATED_IN_GLOBAL_QA
AFGHANISTAN_TWO_JE_PINNING_BLOCK_REMAINS_CLOSED
POLAND_TWO_JE_PINNING_BLOCK_REMAINS_CLOSED
PINNING_SWEEP_EXCEPTIONS_REMAIN_BOUNDED_14
BIC_PROTECTIONS_PRESERVED
NO_GAMEPLAY_CHANGED
ONE_HUMAN_RUNTIME_ONLY
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_JE_PINNING_FAMILY_CLOSED_EXCEPT_BOUNDED_EXCEPTIONS
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NO_NEXT_EXECUTION_PHASE_SELECTED
```
