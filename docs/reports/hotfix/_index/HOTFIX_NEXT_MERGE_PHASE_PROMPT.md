# Prompt autonome — HOTFIX-6A.18R

Nous poursuivons le portage du mod Victoria 3 vers Victoria 3 1.13 — The
Great Wave :

`1776_Age_of_Revolutions_fork`

Tu dois exécuter exclusivement la phase documentaire suivante :

`HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT`

Cette phase doit auditer la validité 1.13 de l'effet historique
`add_declared_interest` sans modifier aucun fichier gameplay.

## 1. Nature et objectif

6A.18R est un audit :

- documentaire;
- statique;
- trois voies;
- fonctionnel;
- limité à un fichier historique et au registre de l'effet;
- sans runtime.

Il doit déterminer :

1. si `add_declared_interest` existe encore dans le moteur 1.13;
2. s'il accepte un scope pays et une région stratégique en argument;
3. si son absence des scripts vanilla signifie suppression, usage interne ou
   simple absence de besoin vanilla;
4. si les 91 actions du fork sont chargées, ignorées ou potentiellement
   invalides;
5. quel impact leur échec aurait sur les intérêts diplomatiques initiaux;
6. quelles différences source/fork sont des cartographies protégées;
7. si une future correction atomique est prouvable ou si aucune action ne doit
   être sélectionnée.

Ne jamais inventer une API de remplacement. Ne commencer aucune correction.

## 2. Chemins

Fork de travail :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

Source hotfix, lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

Vanilla Victoria 3 1.13, lecture seule :

`C:\Games\Victoria 3 The Great Wave\game`

Logs existants, lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs`

Branche obligatoire : `hotfix-dlc-audit`.

## 3. État d'entrée obligatoire

6A.18 doit être présent dans le HEAD après son commit manuel.

Message exact attendu du HEAD :

`Select declared interest history API audit`

Capturer le hash complet et l'utiliser comme HEAD initial et final.

Rapport obligatoire dans le HEAD :

`docs/reports/hotfix/_index/HOTFIX_6A18_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

Verdicts obligatoires :

```text
HOTFIX_6A18_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE
POST_6A17R_RESIDUAL_DIAGNOSTICS_REINDEXED
GAMEPLAY_SEVERITY_AND_MERGE_BLOCKERS_SEPARATED
RESIDUAL_P0_P1_PRIORITY_MATRIX_COMPLETE
COUP_AND_IMPERIALISM_CORRECTIONS_REMAIN_UNSELECTED
HBC_AND_NAVIGATION_ACTS_REMAIN_BLOCKED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
DECLARED_INTEREST_HISTORY_API_AUDIT_SELECTED
NEXT_EXECUTION_PHASE = HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT
```

Si le rapport, le message ou les verdicts ne sont pas présents dans le HEAD,
arrêter sans modification avec :

`HOTFIX_6A18R_BLOCKED_6A18_NOT_COMMITTED`

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
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A18_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
```

Exiger :

- racine exacte du fork;
- branche `hotfix-dlc-audit`;
- message HEAD exact;
- rapport et treize verdicts 6A.18 dans le HEAD;
- aucun changement suivi;
- staged vide;
- uniquement `bject` et les sept fichiers de
  `docs/research/technology/` non suivis;
- `git diff --check` PASS;
- stash protégé exact;
- aucun processus Victoria 3, Dowser ou launcher Paradox.

Ignorer Ankama Launcher. Ne jamais filtrer les processus sur le seul mot
générique `launcher`. Détecter seulement `victoria3.exe`, `dowser.exe` ou un
chemin/une commande contenant `Paradox Interactive\launcher`.

Arrêts autorisés :

```text
HOTFIX_6A18R_BLOCKED_WRONG_BRANCH
HOTFIX_6A18R_BLOCKED_6A18_NOT_COMMITTED
HOTFIX_6A18R_BLOCKED_DIRTY_TRACKED_TREE
HOTFIX_6A18R_BLOCKED_STAGED_FILES
HOTFIX_6A18R_BLOCKED_UNEXPECTED_UNTRACKED_FILES
HOTFIX_6A18R_BLOCKED_PROTECTED_STASH_CHANGED
HOTFIX_6A18R_BLOCKED_GAME_PROCESS_RUNNING
HOTFIX_6A18R_BLOCKED_CANONICAL_DOCUMENT_MISMATCH
```

## 5. Protections absolues

Ne jamais inspecter, modifier, stager, supprimer ou intégrer :

- `bject`;
- les sept fichiers non suivis de `docs/research/technology/`;
- le contenu du stash protégé.

Stash attendu :

```text
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
518df704fa14599c0f254fae13859210663dd976
```

Ne jamais appliquer, ouvrir, extraire, renommer ou supprimer ce stash.

Ne jamais rouvrir ou modifier NAVY, MARATH, ADMIN, technologies, HBC,
Navigation Acts, Inde, BIC, Sepoy, Bombay, Travancore, Japon, Russie,
Autriche/Croatie/Suisse, DEI/VOC, Java, les JE déjà closes, Coup, Imperialism
of Promise, Tanzimat, Merchant Banking, les révolutions, les localisations
françaises générales, descripteurs ou sauvegardes.

Exception de lecture strictement bornée : le fichier transversal cible
`common/history/interests/00_interests.txt` peut être lu dans le fork et la
source. Ses scopes BIC/GBR/Inde/Portugal doivent seulement être inventoriés;
aucun historique pays ou fichier géographique protégé ne doit être ouvert.

BIC doit conserver exactement :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer `law_colonial_exploitation`.

## 6. Règles Git absolues

Ne jamais exécuter `git add`, reset, restore, checkout de fichier, clean,
merge, rebase, amend, commit, `stash apply`, `stash pop` ou `stash drop`.

Le HEAD initial et final doit rester identique et l'index staged vide.

## 7. Baseline 6A.18

La sélection 6A.18 a établi :

- fork : 91 actions actives, 28 scopes pays, 45 régions, 4 415 octets, SHA-256
  `A528418D3C18379C1175E6B469C0313D0AF8C7CC04E80BBE6382F72A097F5DBD`;
- source : 96 actions, les mêmes 28 scopes et 45 régions, 4 609 octets,
  SHA-256
  `0BD9ADC58439BB6F81D1B0165954E827C332CB4FCC687980055D4C6A0DF3C92A`;
- fichier vanilla absent;
- zéro diagnostic courant et 91 diagnostics seulement documentés
  historiquement;
- aucune occurrence vanilla de l'effet exact dans `common`, `events` ou
  `map_data`;
- `has_interest_marker_in_region` et
  `can_have_declared_interest_here` existent, sans constituer des effets de
  remplacement;
- cinq actions de différence source/fork sont liées aux cartographies
  protégées de GBR, BIC, Inde et Portugal;
- les inventaires canoniques se contredisent entre
  `MERGED_AND_VALIDATED`/P3 et `PENDING_REVIEW`/P1;
- impact potentiel majeur, impact prouvé `UNKNOWN_RUNTIME_IMPACT`, statut
  `REQUIRES_AUDIT`.

Ne pas traiter cette baseline comme la preuve que l'effet est invalide.

Dimensions attendues avant 6A.18R :

- matrice des blocs : `44 × 17`;
- index des rapports : `133 × 22`;
- inventaire trois voies : `541 × 21`;
- différences globales : `534 × 22`;
- travail restant : `512 × 20`.

Parser tous les CSV avec un vrai parseur CSV.

## 8. Sources documentaires obligatoires

Lire intégralement avant toute écriture :

- `HOTFIX_6A18_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`;
- `HOTFIX_6A17_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`;
- `HOTFIX_6A17R_IMPERIALISM_OF_PROMISE_1_13_FUNCTIONAL_AUDIT.md`;
- `HOTFIX_6A16R_COUP_EVENT_APIS_1_13_FUNCTIONAL_AUDIT.md`;
- roadmap, matrice des blocs, index des rapports;
- les trois inventaires canoniques;
- le présent prompt;
- changelogs complets fork/source;
- logs courants et rotations pertinentes;
- versions fork/source du seul fichier cible.

## 9. Audit statique du fichier

Pour fork et source, établir exactement :

- encodage, taille, nombre de lignes, SHA-256;
- structure de la racine `INTERESTS`;
- tous les scopes pays;
- toutes les régions;
- toutes les occurrences actives et commentées;
- portée syntaxique de chaque effet;
- doublons pays/région;
- identifiants stratégiques présents ou absents de vanilla 1.13;
- différences exactes fork/source, par pays et par action;
- partition stricte entre groupe API et sous-deltas cartographiques protégés.

Ne modifier aucune action. Ne restaurer aucune ancienne région Inde.

## 10. Registre moteur et données vanilla

Rechercher l'effet exact, en lecture seule, dans :

- les scripts et fichiers `.md` de vanilla;
- les exemples/test events;
- les métadonnées de script disponibles;
- les journaux;
- les chaînes lisibles des binaires/données du jeu, uniquement avec un outil
  de lecture non exécutant si disponible.

Ne jamais lancer l'exécutable du jeu pour cette recherche.

Rechercher séparément :

- `add_declared_interest`;
- effets apparentés contenant `interest`, `interest_marker` ou
  `strategic_region`;
- triggers associés;
- signatures ou commentaires documentant les scopes d'entrée;
- exemples historiques équivalents dans une autre version/DLC installée.

Une simple ressemblance de nom ne prouve jamais l'équivalence. Si aucune API
moderne exacte n'est trouvée, conclure « remplacement inconnu », pas inventer
une substitution.

## 11. Diagnostics et sémantique

Séparer :

1. erreurs parser/PostValidate actuelles;
2. erreurs runtime actuelles;
3. rotations historiques encore disponibles;
4. preuves seulement citées dans les rapports;
5. absence de diagnostic;
6. preuve positive de reconnaissance par le registre moteur;
7. preuve positive ou négative d'effet fonctionnel.

Dédupliquer les logs par `(session, timestamp, message, chemin, ligne)`. Ne pas
additionner `error.log` et son miroir `game.log`.

Évaluer trois hypothèses sans en privilégier une sans preuve :

- effet encore valide mais inutilisé par vanilla;
- effet reconnu mais sémantique modifiée;
- effet obsolète, ignoré ou invalide.

Pour chacune, décrire l'impact sur les intérêts initiaux, les actions
diplomatiques et les 28 pays. Distinguer impact potentiel et impact démontré.

## 12. Comparaison trois voies et classifications

Vanilla n'ayant pas le fichier, comparer :

- présence/absence;
- registre d'effet;
- concepts de régions et d'intérêts;
- fork contre source action par action;
- fork/source contre les données stratégiques vanilla, sans ouvrir les
  périmètres protégés.

Chaque groupe ou sous-delta doit recevoir exactement une classification :

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

Attribuer séparément une gravité gameplay et un statut de merge parmi les
listes canoniques de 6A.18.

## 13. Preuve de validité et éventuel test futur

Une preuve positive de validité peut venir d'un registre moteur lisible, d'une
documentation 1.13 exacte ou d'un diagnostic explicitement positif. L'absence
d'erreur seule ne suffit pas.

Si le statique ne peut pas trancher, définir seulement un protocole futur
minimal reproductible, sans le lancer ni le demander pendant 6A.18R. Il doit
comparer au moins un pays non protégé et un témoin négatif, vérifier les
intérêts au jour 1 et isoler le montage du fork.

Ne pas ouvrir une sauvegarde et ne pas demander de test humain dans cette
phase.

## 14. Critères d'une éventuelle phase suivante

Sélectionner au maximum une phase, sans la commencer.

Une future correction F exige simultanément :

- effet 1.13 exact démontré;
- invalidité de l'effet legacy démontrée;
- remplacement sémantiquement équivalent;
- périmètre API séparé des cinq cartographies protégées;
- aucun changement de pays, région, quantité d'intérêts ou design;
- diff, hash final et rollback exacts;
- test futur borné;
- gain P0/P1 réel.

Si une condition manque, ne sélectionner aucune correction. Un audit runtime
ultérieur n'est sélectionnable que s'il est réellement nécessaire, autonome
et autorisable sans périmètre protégé.

Décisions possibles :

```text
DECLARED_INTEREST_LEGACY_EFFECT_VALID_NO_CORRECTION_REQUIRED
NO_NEXT_EXECUTION_PHASE_SELECTED
```

ou :

```text
DECLARED_INTEREST_HISTORY_API_REMAINS_UNRESOLVED
NO_NEXT_EXECUTION_PHASE_SELECTED
```

ou, seulement si toutes les conditions sont prouvées :

```text
NEXT_EXECUTION_PHASE = HOTFIX_6A18F_DECLARED_INTEREST_HISTORY_API_1_13_ALIGNMENT
```

## 15. Runtime interdit

Ne lancer ni Victoria 3, ni launcher Paradox, ni sauvegarde, ni console, ni
runtime automatisé. Ne demander aucun lancement à l'opérateur. Aucun nouveau
log ne doit être produit.

## 16. Documentation autorisée

Créer uniquement :

`docs/reports/hotfix/_index/HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT.md`

Mettre à jour seulement si nécessaire :

- `docs/reports/hotfix/INDEX.md`;
- `HOTFIX_REPORT_INDEX.csv`;
- `HOTFIX_MERGE_BLOCK_STATUS.csv`;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Ne créer aucun autre fichier. Si aucune phase n'est sélectionnée, conserver le
présent prompt comme preuve historique selon la convention canonique.

## 17. Contenu obligatoire du rapport

Inclure : phase/date, branche, HEAD initial/final, message, préflight, état Git,
stash, sources, CSV, hashes, structure du fichier, pays, régions, occurrences,
registre moteur, recherches vanilla, logs actuels/historiques, déduplication,
trois hypothèses, comparaison trois voies, diff fork/source, séparation des
cinq sous-deltas protégés, classifications exclusives, gravité, statut de
merge, impact fonctionnel, protocole futur éventuel, décision, documents,
contrôles finaux et verdicts.

## 18. Contrôles finaux

Vérifier : branche et HEAD inchangés; aucun gameplay modifié; staged vide;
aucun commit; stash inchangé; huit untracked protégés intacts et non inspectés;
Coup, Imperialism, HBC, Navigation Acts, BIC, Inde, NAVY, ADMIN, Tanzimat et
lois inchangés; aucune localisation modifiée; `git diff --check` PASS; aucun
processus Victoria 3/Dowser/Paradox; logs inchangés.

## 19. Verdicts minimaux

```text
HOTFIX_6A18R_DECLARED_INTEREST_HISTORY_API_1_13_AUDIT_COMPLETE
DECLARED_INTEREST_HISTORY_THREE_WAY_COMPARISON_COMPLETE
DECLARED_INTEREST_EFFECT_REGISTRY_AUDITED
DECLARED_INTEREST_COUNTRY_AND_REGION_SCOPES_CLASSIFIED
DECLARED_INTEREST_PROTECTED_MAPPINGS_SEPARATED
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
```

Ajouter exactement une des décisions de la section 14. Ne sélectionner qu'une
seule phase éventuelle. S'arrêter après le compte rendu et ne jamais commencer
la phase suivante.
