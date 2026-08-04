# Prochaine phase — QA runtime combinée des événements d'intérêt 6A.18Q2

État canonique après l'audit R3 et la correction F3 choisie explicitement par
l'opérateur humain :

```text
INDOCHINA_LEGACY_INTEREST_LOGIC_REMOVAL_PROVEN
HUMAN_OPERATOR_DECISION_REMOVE_INDOCHINA_LEGACY_INTEREST_LOGIC
HOTFIX_6A18F3_INDOCHINA_REMOVE_LEGACY_INTEREST_LOGIC_1_13_ALIGNMENT_COMPLETE
RUNTIME_DEFERRED_TO_COMBINED_DECLARED_INTEREST_EVENT_QA
NEXT_EXECUTION_PHASE = HOTFIX_6A18Q2_COMBINED_DECLARED_INTEREST_EVENT_RUNTIME_QA
```

F3 a supprimé uniquement, dans `indochina.3.a`, le garde de slots et l'effet
`add_declared_interest = region_indochina`. Le fichier fait 9494 octets,
509 lignes et porte le SHA-256
`70965044236460BFD2ADE5EDE18A0BEF6DC2E1EEAFB496423E027E80091B28A9`.
Les quatre autres hunks du fichier et la crise égyptienne restent inchangés.

6A.18Q2 devra ouvrir une nouvelle partie avec le fork et le bon hash, puis
contrôler ensemble l'absence des diagnostics legacy de la crise égyptienne et
de l'Indochine, ainsi que la non-régression des implications naturelles. Aucun
runtime n'est lancé pendant la présente mise à jour documentaire.

Le prompt ci-dessous est conservé uniquement comme preuve historique de la
phase 6A.18R2 exécutée. Il ne constitue plus une instruction active.

---

# Prompt historique — audit du mécanisme d'initialisation des intérêts 1.13

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave :

`1776_Age_of_Revolutions_fork`

Tu dois exécuter exclusivement la phase suivante :

`HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT`

Cette phase est un audit en lecture seule. Elle ne doit appliquer aucune
correction gameplay et ne doit pas lancer Victoria 3.

## 1. Objectif exact

Le runtime 6A.18Q a confirmé que :

- `common/history/interests/00_interests.txt` est chargé;
- ses 91 actions actives sont toutes atteintes;
- le moteur 1.13 émet `Unknown effect add_declared_interest` pour chacune;
- l'Autriche ne reçoit aucune implication au Sud de la Chine malgré la ligne
  126;
- le Canada témoin reste sans implication;
- les intérêts visibles sont générés par le nouveau système d'implication.

6A.18R2 doit rechercher le mécanisme exact et documenté par lequel Victoria 3
1.13 initialise ou augmente une implication régionale au démarrage. Il faut
déterminer si un équivalent script utilisable existe avant toute correction.

## 2. État d'entrée obligatoire

Branche : `hotfix-dlc-audit`.

La phase 6A.18Q doit être commitée manuellement dans le HEAD avec le message :

`Validate declared interest history runtime for 1.13`

Rapport obligatoire :

`docs/reports/hotfix/_index/HOTFIX_6A18Q_DECLARED_INTEREST_HISTORY_RUNTIME_VALIDATION.md`

Verdicts obligatoires dans le HEAD :

```text
HOTFIX_6A18Q_DECLARED_INTEREST_HISTORY_RUNTIME_VALIDATION_COMPLETE
DECLARED_INTEREST_POSITIVE_AND_NEGATIVE_CONTROLS_EXECUTED
DECLARED_INTEREST_RUNTIME_LOGS_DEDUPLICATED
NO_GAMEPLAY_CHANGED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
DECLARED_INTEREST_LEGACY_EFFECT_RUNTIME_FAIL
DECLARED_INTEREST_HISTORY_API_INVALIDITY_CONFIRMED
NEXT_EXECUTION_PHASE = HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT
```

Si ces conditions ne sont pas réunies, arrêter sans écriture avec :

`HOTFIX_6A18R2_BLOCKED_6A18Q_NOT_COMMITTED`

## 3. Préflight

Exécuter en lecture seule :

```powershell
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git log -5 --oneline --decorate
git status --short --untracked-files=all
git diff --check
git diff --cached --name-only
git stash list
git rev-parse 'stash@{0}'
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A18Q_DECLARED_INTEREST_HISTORY_RUNTIME_VALIDATION.md
```

Exiger : racine exacte, branche exacte, HEAD au message attendu, arbre suivi
propre, staged vide, uniquement `bject` et les sept recherches technologiques
non suivis, stash intact et aucun processus Victoria 3/Dowser/launcher.

Stash attendu :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

## 4. Protections absolues

Ne jamais inspecter ou modifier `bject`, les sept recherches technologiques,
le stash, BIC, GBR, Inde, Sepoy, Bombay, Travancore, NAVY, ADMIN, HBC,
Navigation Acts, Coup, Imperialism of Promise, Tanzimat, Merchant Banking, les
localisations françaises, les descripteurs ou les sauvegardes.

Ne jamais restaurer `law_colonial_exploitation`. BIC doit conserver
`law_frontier_colonization`.

Ne lancer ni le jeu ni le launcher. Ne modifier aucun fichier gameplay.

## 5. Arbres de référence

Fork :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

Source hotfix, lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

Vanilla 1.13, lecture seule :

`C:\Games\Victoria 3 The Great Wave\game`

## 6. Recherche obligatoire

Rechercher séparément, dans les scripts, métadonnées techniques, GUI anglaise,
exemples et chaînes lisibles installées :

- les effets contenant `interest`, `interest_marker`, `involvement` ou
  `strategic_region`;
- `create_interest_marker`, `set_interest_marker`,
  `add_interest_marker_rank`, `remove_interest_marker` et toute signature
  associée;
- les getters d'implication actuelle, cible et de ventilation;
- les initialisations vanilla de territoire, capitale, revendication, armée,
  flotte, traité, pacte et sujet;
- les on-actions exécutés lors de la création du monde ou d'un pays;
- les racines historiques reconnues en 1.13;
- les effets documentés utilisables depuis un scope pays avec une région
  stratégique actuelle;
- les exemples de test ou scripts DLC qui initialisent une implication sans
  action humaine.

Séparer formellement :

1. API de lecture et de tooltip;
2. commandes debug internes;
3. effets script enregistrés;
4. calcul naturel dynamique;
5. initialisation historique au jour 1;
6. mécanismes réservés au code moteur.

La simple présence d'une chaîne binaire, d'un getter GUI ou d'une commande
debug ne prouve pas qu'un effet script soit utilisable.

## 7. Questions à trancher

Le rapport doit répondre explicitement :

1. Existe-t-il un effet 1.13 enregistré qui accepte un pays et une région ?
2. Cet effet définit-il une implication actuelle, une implication cible, un
   rang d'intérêt ou un marqueur legacy ?
3. Est-il autorisé dans `common/history` au chargement du monde ?
4. Existe-t-il un exemple vanilla ou DLC exécutable qui en prouve la syntaxe ?
5. Les cinq niveaux actifs peuvent-ils être initialisés directement ou doivent
   ils découler uniquement des sources naturelles ?
6. Une valeur historique fixe survivrait-elle au recalcul hebdomadaire de
   l'implication ?
7. Un remplacement des 91 lignes est-il techniquement possible sans inventer
   une nouvelle source d'implication ou modifier l'équilibrage ?
8. Un remappage des 26 régions legacy serait-il utile avant la preuve de ce
   mécanisme ?

## 8. Conditions de sélection d'une correction future

Ne sélectionner une phase de correction que si toutes les preuves suivantes
sont réunies :

- nom exact de l'effet enregistré;
- signature exacte des scopes et arguments;
- contexte historique autorisé;
- exemple vanilla/DLC ou test officiel directement comparable;
- sémantique d'implication actuelle/cible démontrée;
- interaction avec le recalcul dynamique comprise;
- remplacement borné sans toucher aux cartographies protégées;
- hash théorique et diff minimal reproductibles.

Si une seule preuve manque, conclure que le mécanisme reste non démontré et ne
sélectionner aucune correction.

## 9. Documentation

Créer uniquement :

`docs/reports/hotfix/_index/HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT.md`

Mettre à jour seulement si nécessaire :

- `docs/reports/hotfix/INDEX.md`;
- `HOTFIX_REPORT_INDEX.csv`;
- `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## 10. Git

Ne jamais exécuter `git add`, `git reset`, `git restore`, `git checkout` de
fichier, `git clean`, merge, rebase, amend, commit, push, `stash apply`,
`stash pop` ou `stash drop`.

Le HEAD, l'index, le stash et tous les fichiers gameplay doivent rester
inchangés.

## 11. Verdicts minimaux

Terminer par :

```text
HOTFIX_6A18R2_DECLARED_INTEREST_INITIALIZATION_MECHANISM_1_13_AUDIT_COMPLETE
DECLARED_INTEREST_1_13_INITIALIZATION_PATHS_AUDITED
DECLARED_INTEREST_LEGACY_AND_INVOLVEMENT_SEMANTICS_SEPARATED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
```

Ajouter ensuite exactement l'un des résultats suivants :

```text
DECLARED_INTEREST_1_13_REPLACEMENT_MECHANISM_PROVEN
NEXT_EXECUTION_PHASE = HOTFIX_6A18F_DECLARED_INTEREST_HISTORY_1_13_ALIGNMENT
```

ou :

```text
DECLARED_INTEREST_1_13_REPLACEMENT_MECHANISM_UNPROVEN
NO_NEXT_EXECUTION_PHASE_SELECTED
```

Ne jamais commencer la phase éventuellement sélectionnée.
