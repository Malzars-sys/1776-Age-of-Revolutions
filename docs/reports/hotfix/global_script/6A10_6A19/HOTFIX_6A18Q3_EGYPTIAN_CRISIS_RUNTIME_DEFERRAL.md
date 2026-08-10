# HOTFIX-6A.18Q3 — Report de la validation runtime de la crise égyptienne

Date : 4 août 2026

## 1. Décision humaine

L’opérateur décide de ne pas forcer `egyptian_crisis_events.4` dans le cadre du
merge hotfix actuel. La validation sémantique de l’impulsion
`add_involvement = 2500` est reportée à une future extension flavor consacrée
au Moyen-Orient.

Cette décision supersède administrativement le blocage laissé par le résultat B
de 6A.18Q2. Elle ne transforme pas le test absent en succès runtime : le statut
exact reste « non exécuté, reporté avec justification ».

## 2. Justification dans le scénario 1776

Le setup initial du fork ne contient aucun historique pays instanciant `EGY`.
Les scripts de la crise référencent le tag, mais l’entrée de
`egyptian_crisis_events.1` exige explicitement `exists = c:EGY`. Aucune chaîne
actuelle documentée ne libère naturellement l’Égypte depuis l’Empire ottoman au
début de la partie.

Dans cet état, la crise ne devient accessible que si le joueur crée
délibérément l’Égypte ou si un futur contenu ajoute son émergence. Forcer
l’événement hors de cette chaîne testerait l’effet isolé, pas un parcours de
jeu réellement disponible dans le fork 1776.

## 3. État technique conservé

- le remplacement 1.13 de F2 reste inchangé et statiquement conforme au bloc
  vanilla `add_involvement`, région `sr:region_near_east`, valeur `2500` ;
- Q2 conserve son résultat historique : parsing propre, aucune sémantique de
  `2500` observée ;
- les 94 diagnostics legacy restent éliminés ;
- le retrait indochinois F3 reste validé en runtime ;
- aucun fichier gameplay, événement, historique pays ou localisation n’est
  modifié par Q3.

## 4. Condition de réouverture

La validation égyptienne ne devra être rouverte que dans une phase flavor
Moyen-Orient qui fournit ou audite une chaîne jouable d’émergence de l’Égypte.
Cette future phase devra alors tester la création/libération du pays, le
déclenchement naturel de la crise et la variation d’implication, sans utiliser
Q3 comme preuve runtime.

## 5. Conséquence pour le merge

L’absence de validation sémantique égyptienne n’est plus un bloqueur du merge
hotfix/fork. Le bloc des intérêts déclarés est clos avec un report documenté,
et le prochain travail sélectionné est la réindexation des résidus globaux après
6A.18.

```text
HOTFIX_6A18Q3_EGYPTIAN_CRISIS_RUNTIME_DEFERRAL_COMPLETE
HUMAN_OPERATOR_DECISION_DEFER_EGYPTIAN_CRISIS_RUNTIME
EGYPTIAN_CRISIS_RUNTIME_SEMANTIC_VALIDATION_DEFERRED_TO_MIDDLE_EAST_FLAVOR_EXTENSION
EGYPT_1776_NATURAL_ENTRY_CHAIN_ABSENT
DECLARED_INTEREST_BLOCK_CLOSED_WITH_DOCUMENTED_RUNTIME_DEFERRAL
NO_GAMEPLAY_CHANGED
NO_RUNTIME_EXECUTED
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_EXECUTION_PHASE = HOTFIX_6A19_RESIDUAL_GLOBAL_SCRIPT_REINDEX
```
