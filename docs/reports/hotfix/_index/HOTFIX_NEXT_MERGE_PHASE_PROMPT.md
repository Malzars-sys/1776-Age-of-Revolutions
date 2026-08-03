# Prompt autonome — HOTFIX-6A.17R audit fonctionnel d'Imperialism of Promise

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The Great
Wave :

`1776_Age_of_Revolutions_fork`

Exécuter exclusivement :

`HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT`

## 1. Objectif unique

Auditer en lecture seule l'objet `je_imperialism_of_promise` dans :

`common/journal_entries/04_imperialism_of_promise.txt`

Comparer fork, source hotfix et vanilla 1.13 par groupe fonctionnel. Séparer le
pinning, les API de rôles, le jeu de rôles divergent, le tooltip de
bureaucratie et toutes les dépendances protégées. Classer chaque groupe et
sélectionner au maximum une future correction atomique seulement si toutes ses
conditions sont prouvées.

Cette phase ne modifie aucun gameplay, ne lance aucun runtime, ne stage rien,
ne crée aucun commit et ne commence aucune correction.

## 2. Chemins

Fork :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

Source hotfix, lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

Vanilla 1.13, lecture seule :

`C:\Games\Victoria 3 The Great Wave\game`

Logs existants, lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs`

Branche : `hotfix-dlc-audit`.

## 3. État d'entrée

Exiger que le rapport 6A.17 soit présent dans `HEAD` après commit manuel :

`docs/reports/hotfix/_index/HOTFIX_6A17_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

Le hash et le message du futur HEAD ne sont pas imposés. Les capturer et exiger
les verdicts suivants dans le rapport committé :

```text
HOTFIX_6A17_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE
POST_6A16R_RESIDUAL_DIAGNOSTICS_REINDEXED
RESIDUAL_P0_P1_PRIORITY_MATRIX_COMPLETE
COUP_EVENT_APIS_REMAIN_UNSELECTED
HBC_AND_NAVIGATION_ACTS_REMAIN_BLOCKED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
IMPERIALISM_OF_PROMISE_1_13_AUDIT_SELECTED
NEXT_EXECUTION_PHASE = HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT
```

Ne jamais commencer depuis un rapport 6A.17 non committé.

## 4. Préflight Git

Exécuter uniquement en lecture seule :

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
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A17_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
```

Exiger la racine et la branche exactes, le rapport et ses verdicts dans HEAD,
aucun changement suivi, index staged vide, seulement `bject` et les sept
recherches technologiques non suivis, stash exact et aucun processus Victoria
3, Dowser ou Paradox.

Ignorer Ankama Launcher. Ne jamais chercher le mot générique `launcher` :
détecter seulement `victoria3.exe`, `dowser.exe` ou une ligne de commande
contenant `Paradox Interactive\launcher`.

Arrêts :

```text
HOTFIX_6A17R_BLOCKED_WRONG_BRANCH
HOTFIX_6A17R_BLOCKED_6A17_NOT_COMMITTED
HOTFIX_6A17R_BLOCKED_DIRTY_TRACKED_TREE
HOTFIX_6A17R_BLOCKED_STAGED_FILES
HOTFIX_6A17R_BLOCKED_UNEXPECTED_UNTRACKED_FILES
HOTFIX_6A17R_BLOCKED_PROTECTED_STASH_CHANGED
HOTFIX_6A17R_BLOCKED_GAME_PROCESS_RUNNING
HOTFIX_6A17R_BLOCKED_CANONICAL_DOCUMENT_MISMATCH
HOTFIX_6A17R_BLOCKED_THREE_WAY_EVIDENCE_CHANGED
```

## 5. Protections absolues

Ne jamais inspecter ni modifier `bject`, les sept recherches technologiques ou
le contenu du stash.

Stash attendu :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

Ne jamais rouvrir ou modifier NAVY, MARATH, ADMIN, technologies, HBC `hubson`
ou `hudson`, Navigation Acts, Inde, BIC, Sepoy, Bombay, Travancore, Japon,
Russie, Autriche/Croatie/Suisse, DEI/VOC, Java, Balkans/Yugoslavia/Risorgimento,
nationalisme grec, Grande Crise orientale, Sick Man/Tanzimat, Romania,
Portuguese Colonialism, Merchant Banking, révolutions américaine et française,
localisations françaises générales, descripteurs ou sauvegardes.

BIC doit conserver :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer `law_colonial_exploitation`.

Ne jamais exécuter `git add`, reset, restore, checkout de fichier, clean,
merge, rebase, amend, commit, `stash apply`, `stash pop` ou `stash drop`.

## 6. Preuves d'entrée

Fichier ciblé :

| Arbre | Octets | SHA-256 |
| --- | ---: | --- |
| Fork | 2 912 | `80E38C181A5AEB547E8F98EBFD03844F3522CADC59426D9FC16588B908105C3B` |
| Source | 3 182 | `F97A929A3CC9FAA98A8CE3824A4A6196866AFBA18A89E477600DDA230153D7FC` |
| Vanilla | 3 143 | `AB08635DC8EAA5C3A1523F70693BADB58A607576B06C5EF979E682008B0D4C0C` |

Objet : `je_imperialism_of_promise`.

Fork/source et fork/vanilla : trois hunks, `13+ / 5-`. Repères fork :

- lignes 18–19 : `has_role = agitator/politician`;
- lignes 38–39 : bureaucratie et shortage sans tooltip englobant;
- ligne 140 : `should_be_pinned_by_default = yes`.

Le pinning seul donne théoriquement, sans écriture :

```text
future_size = 2934
future_sha256 = EF5200E0B9E7A58AF904C73CDD82F3CC4009FFE0CA9364952F793AB4F3E2A682
```

Ces preuves doivent être recalculées. Toute divergence impose
`HOTFIX_6A17R_BLOCKED_THREE_WAY_EVIDENCE_CHANGED`.

## 7. Lecture obligatoire

Lire intégralement avant conclusion :

- 6A.17, 6A.16R, 6A.16, 6A.15R et 6A.15F;
- les trois versions complètes du fichier ciblé;
- les rapports canoniques BIC/Inde nécessaires pour comprendre les frontières,
  sans rouvrir leurs fichiers gameplay;
- les rapports et définitions documentaires des événements utilitaristes,
  scopes BIC, Sepoy, groupe de journal entries et DLC `ip2_content`;
- roadmap, matrice de blocs, index, inventaires trois voies et résiduels;
- changelogs complets du fork et de la source;
- logs courants et rotations pertinentes, sans les additionner aveuglément.

Parser les CSV avec un vrai parseur CSV.

## 8. Groupes fonctionnels obligatoires

Auditer séparément :

1. pinning ancien vers
   `should_be_pinned_by_default_uninvolved_or_context`;
2. `has_role = agitator` vers `has_role_of_type = agitator`;
3. `has_role = politician` et le seuil de prominence;
4. ajout du rôle ruler;
5. `character_role_ig_leader`, présent seulement dans la source;
6. composition de l'OR et changement du vivier de personnages;
7. tooltip `bureaucrats_no_shortage_trigger`;
8. visibilité et `subject_type_chartered_company`;
9. scopes `BIC_scope` et `industrialists_ig`;
10. conditions d'échec BIC/Sepoy/sécession;
11. progression, lois et géographie;
12. événements `utilitarian.1` à `.10`, pulses et variables;
13. DLC, localisations et groupe `je_group_british_india`.

Les groupes 8 à 13 sont des dépendances à cartographier par rapports et
références en lecture seule. Ils ne peuvent jamais être modifiés ni absorbés
dans une future correction.

## 9. Questions obligatoires

Pour chaque groupe, établir : scope, objet, ligne, diagnostic actuel et
historique, convergence exacte/partielle/absente, effet gameplay, dépendances,
protection, nombre de hunks, isolation, hash théorique éventuel, rollback,
critère statique et runtime futur.

Répondre explicitement :

- le pinning a-t-il encore une preuve runtime actuelle ou seulement historique?
- le pinning peut-il être corrigé sans toucher aucun autre groupe?
- les deux `has_role` peuvent-ils être modernisés sans changer le vivier?
- le seuil de prominence est-il un correctif API ou un changement gameplay?
- le rôle IG source-only est-il valide en 1.13 et intentionnel pour ce mod?
- la convergence du tooltip suffit-elle sans diagnostic?
- les avertissements de JE déjà présente sur des révoltes proviennent-ils de
  cet objet ou du transfert générique des journal entries?
- une future correction peut-elle exclure formellement BIC et l'Inde?

Ne jamais inventer une réponse ou une API moderne.

## 10. Classifications

Classer chaque sous-delta exactement une fois :

```text
REQUIRED_HOTFIX_DELTA
VANILLA_1_13_ALIGNMENT_REQUIRED
ALREADY_MERGED
INTENTIONAL_FORK_DIVERGENCE
OBSOLETE_HOTFIX_CONTENT
POST_MERGE_DESIGN_BACKLOG
PROTECTED_CONCURRENT_WORK
UNKNOWN_REQUIRES_REVIEW
```

## 11. Sélection éventuelle

Sélectionner au maximum une future correction F, sans la commencer. Elle exige
simultanément : diagnostic actuel, un groupe extrêmement borné, convergence
source/vanilla exacte, effet purement technique, aucun changement de scope ou
gameplay, aucun fichier protégé, hash théorique et rollback exacts, et runtime
futur raisonnable.

Les diagnostics historiques seuls ne suffisent pas. Si une condition manque,
ne sélectionner aucune correction.

## 12. Runtime

6A.17R ne lance aucun jeu, launcher, sauvegarde, console ou runtime automatisé
et ne demande pas à l'opérateur de lancer le jeu. Aucun nouveau log ne doit
être produit.

## 13. Documentation autorisée

Créer uniquement :

`docs/reports/hotfix/_index/HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT.md`

Puis mettre à jour, seulement si nécessaire :

- `docs/reports/hotfix/INDEX.md`;
- `HOTFIX_REPORT_INDEX.csv`;
- `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Si aucune correction n'est prouvée, conserver la trace du prompt d'audit et ne
pas inventer de prompt F.

## 14. Sortie exigée

Le rapport doit inclure préflight, hashes, logs actuels/historiques, carte des
groupes, comparaison trois voies, dépendances, classifications exclusives,
diff/hash/rollback de tout candidat, exclusions BIC/Inde, décision, documents,
état Git final, `git diff --check`, staged vide, stash/processus inchangés,
absence de gameplay et de runtime.

Verdicts minimaux :

```text
HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT_COMPLETE
IMPERIALISM_OF_PROMISE_THREE_WAY_COMPARISON_COMPLETE
IMPERIALISM_OF_PROMISE_FUNCTIONAL_GROUPS_CLASSIFIED
BIC_INDIA_GEOGRAPHY_PROGRESSION_DELTAS_PROTECTED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
```

Ajouter exactement une décision :

```text
NO_NEXT_EXECUTION_PHASE_SELECTED
```

ou :

```text
NEXT_EXECUTION_PHASE = <une correction atomique prouvée>
```

S'arrêter après le compte rendu. Ne jamais commencer la phase suivante.
