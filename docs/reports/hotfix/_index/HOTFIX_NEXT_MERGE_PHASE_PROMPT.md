# Prompt autonome — HOTFIX-6A.11 Sélection du prochain résidu global

Nous poursuivons le portage du mod Victoria 3 :

`1776_Age_of_Revolutions_fork`

# Phase HOTFIX-6A.11 — Sélection du prochain résidu global

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Nature de la phase

Cette phase est strictement documentaire.

Aucun gameplay ne doit être modifié. Aucun runtime ne doit être produit.

Codex ne doit jamais :

- lancer Victoria 3 ;
- lancer le launcher Paradox ;
- cliquer ou interagir dans le jeu ;
- piloter ou automatiser l'interface ;
- utiliser la console ;
- ouvrir une sauvegarde ;
- produire de nouveaux logs ;
- corriger un candidat ;
- commencer la future correction sélectionnée ;
- créer un commit automatique.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, STRICTEMENT EN LECTURE SEULE :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA VICTORIA 3 1.13, STRICTEMENT EN LECTURE SEULE :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d'entrée requis

- `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_STATIC_PASS`
- `ROMANIA_TWO_JE_PINNING_TWO_HUNK_1_13_ALIGNMENT_COMPLETE`
- `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_RUNTIME_PASS`
- `ROMANIA_TWO_JE_PINNING_PARSER_ERRORS_2_TO_0`
- `ROMANIA_1776_VISIBILITY_GEOGRAPHY_AND_PROGRESSION_UNCHANGED`
- `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md`

La phase 6A.10F doit avoir été commitée manuellement avant de commencer. Ne
commence jamais 6A.11 depuis le worktree non commité de 6A.10F.

## Objectif unique

Sélectionner exactement un prochain sous-bloc atomique parmi les résidus
globaux encore ouverts.

La phase doit uniquement :

1. actualiser l'inventaire documentaire après 6A.10F ;
2. analyser les 376 diagnostics de pinning restants sans les corriger ;
3. rapprocher ces diagnostics des 141 fichiers et de l'inventaire canonique ;
4. comparer en trois voies les candidats sérieux ;
5. publier exactement trois meilleurs candidats ;
6. sélectionner exactement un candidat ;
7. définir son futur périmètre fermé et son rollback ;
8. produire le prompt autonome de sa future exécution.

Ne modifier aucun gameplay et ne commencer aucun candidat.

## Étape 1 — Préflight Git obligatoire

Exécute :

```powershell
Set-Location "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork"

git rev-parse --show-toplevel
git branch --show-current
git status --short
git log -5 --oneline --decorate
git diff --check
git diff --cached --name-only
git stash list
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md
```

Exige :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.10F et tous ses verdicts présents dans HEAD ;
- 6A.10F déjà commitée manuellement ;
- worktree suivi propre ;
- index staged vide ;
- seuls `bject` et les sept fichiers de
  `docs/research/technology/` peuvent être non suivis ;
- stash exact
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- aucun processus Victoria 3, `dowser` ou Paradox.

Enregistre les hashes SHA-256 de `bject` et des sept fichiers technologiques et
compare-les à 6A.10F.

Arrête avec un verdict précis en cas d'écart :

- `BLOCKED_WRONG_BRANCH`
- `BLOCKED_6A10F_NOT_COMMITTED`
- `BLOCKED_DIRTY_TREE`
- `BLOCKED_STAGED_FILES`
- `BLOCKED_UNEXPECTED_UNTRACKED_FILES`
- `BLOCKED_PROTECTED_STASH_MISSING`
- `BLOCKED_GAME_PROCESS_RUNNING`

Interdictions Git absolues : aucun reset, restore, checkout de fichier, clean,
merge, rebase, amend, commit automatique, stash apply/pop/drop ou inspection
du contenu du stash.

## Étape 2 — Hashes obligatoires

| Preuve | SHA-256 |
| --- | --- |
| Fork `common/journal_entries/00_romania.txt` corrigé | `DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578` |
| Source hotfix `00_romania.txt` | `74149D3A3B778732DE318D7FB522CE4255289B410F6184625BA9670E6CCCAB9A` |
| Vanilla `00_romania.txt` | `9B5C9A9D06DAA420030BBC3B31581CD030356145FD31E1589E590AB9DF904A51` |
| Fork `00_sick_man.txt` | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` |
| Histoire TUR fork | `81ABC8DEA9DE93EC6A4DD417FD05FD6859F3122758D2B27E712B1880013F9CA9` |
| Grande Crise orientale fork | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` |
| BIC fork | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` |

Hashes protégés :

| Élément | SHA-256 |
| --- | --- |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` |
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410` |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` |

Si une preuve imposée diffère :

`BLOCKED_THREE_WAY_EVIDENCE_CHANGED`

La source hotfix et vanilla restent strictement inchangées.

## Étape 3 — Sources obligatoires

Lis intégralement :

- `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les changelogs complets du fork et de la source ;
- les nouveaux logs 6A.10F et leurs rotations, en lecture seule.

Ne lance pas le jeu pour obtenir une preuve supplémentaire.

## Étape 4 — Inventaire canonique après 6A.10F

Actualise les 161 anciennes lignes `PENDING_REVIEW` selon la répartition
effective :

| Catégorie exclusive | Lignes |
| --- | ---: |
| `REQUIRED_HOTFIX_DELTA` | 7 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 16 |
| `ALREADY_MERGED` | 18 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 |
| `PROTECTED_CONCURRENT_WORK` | 19 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 |
| **Total** | **161** |

Il reste 110 lignes directement exploitables par une revue :

- 7 deltas hotfix requis ;
- 16 alignements vanilla 1.13 ;
- 87 inconnus.

Ces 110 lignes ne représentent pas 110 correctifs. Le total historique de 26
deltas à haute confiance reste `UNVERIFIED`.

## Étape 5 — Baseline parser 6A.10F

Recalcule depuis les nouveaux logs sans présumer :

- 376 erreurs exactes
  `Unexpected token: should_be_pinned_by_default,` ;
- 141 fichiers uniques ;
- zéro erreur dans `00_romania.txt` ;
- zéro rejet de
  `should_be_pinned_by_default_uninvolved_or_context` dans ce fichier ;
- trois diagnostics Tanzimat connus `.5`, `.9` et `.10`, indépendants de
  Romania.

Sépare :

- `debug.1.log`, baseline parser du runtime ;
- `debug.2.log`, preuve de montage ;
- `debug.3.log`, rotation historique 6A.9F ;
- diagnostics de pinning ;
- diagnostics Tanzimat ;
- autres erreurs hors périmètre.

Preuves attendues :

- `debug.1.log` :
  `A75AD954D9AA33D27B11BFDBB75A804F319555610F75266604E0565C4D5004E8` ;
- `debug.2.log` :
  `38B2B29FAD0922C6192B27CB69BC202F0C431F1DC9FDF5427C3835EBFDD75C35` ;
- fork monté ligne 87 de `debug.2.log` ;
- `dlc014_ip3` monté ligne 80.

## Étape 6 — Analyse exhaustive

Regroupe les 376 diagnostics par :

- chemin exact ;
- objet exact ;
- occurrences et lignes ;
- statut d'inventaire ;
- présence source et vanilla ;
- propriété moderne source et vanilla ;
- protection active ;
- dette fonctionnelle adjacente ;
- localisation ;
- besoin de runtime futur.

Publie la liste des 141 fichiers, le top 25 et les familles principales :
tutoriels, objectifs joueur, prestige goods, Russie protégée, autres journal
entries, fichiers hors inventaire, erreurs uniques, fichiers multi-objets et
divergences source/vanilla.

Une occurrence parser ne constitue jamais à elle seule une autorisation de
correction.

## Étape 7 — Blocs clos interdits

Ne rouvre ni ne sélectionne :

- Balkan National Awakening ;
- Yugoslavia ;
- Risorgimento ;
- nationalisme grec ;
- Grande Crise orientale ;
- les huit pinning Sick Man ;
- `common/journal_entries/00_romania.txt` ;
- `je_unite_the_principalities` ;
- `je_all_for_one`.

Ne sélectionne pas l'activation Tanzimat, `sick_man.1`,
`sick_man_of_europe` ou `outmoded_bureaucracy`. Ils restent dans
`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`.

## Étape 8 — Pistes obligatoires

Réexamine séparément, sans présumer leur sélection :

1. Merchant Banking GEN/VEN :
   deux fichiers, deux pays, deux hunks potentiels ; loi, icône et
   localisations déjà présentes ; preuve changelog 2.3 ; préserver
   `law_merchant_navy`, exclure le nom spécifique des landowners et NAVY.
2. Navigation Acts :
   GBR/HBC/NBS/ONT/ORA ; cinq fichiers et cinq pays ; preuve changelog 2.3 ;
   divergence vanilla ; collision GBR/NAVY ; BIC totalement hors périmètre.
3. Petits alignements parser 1.13 :
   Coup, Imperialism of Promise et les autres fichiers d'une ou deux erreurs ;
   vérifier chaque dette adjacente, scope, rôle, tooltip et localisation.
4. Diagnostics Tanzimat `.5`, `.9`, `.10` :
   analyser le namespace, les on-actions, l'absence du fichier dans le fork,
   le classement `OBSOLETE_HOTFIX_CONTENT` et le risque de design 1776 ;
   ne modifier aucun événement.
5. Inconnus :
   uniquement lorsqu'un log, changelog, convergence trois voies ou dépendance
   déjà intégrée constitue une preuve précise.

Écarte tout candidat avec portée massive, localisation manquante, divergence
source/vanilla injustifiée, décision de design, collision active ou fichier
protégé.

## Étape 9 — Protections absolues

Ne sélectionne ni ne modifie aucun élément relatif à DEI/VOC, Java, économie
post-compagnie, Balkans clos, Romania close, activation Tanzimat, NAVY,
formations et événements navals, MARATH, SAT, KHP, Travancore, Inde, BIC,
Sepoy, Bombay, ADMIN, Japon, Russie, Autriche, Croatie, Slavonie, Suisse,
révolutions américaine et française, lettres de Kew, technologies, recherche,
localisations françaises générales, agriculture, alimentation, industrie,
descripteurs, launcher, sauvegardes ou `bject`.

BIC conserve :

```txt
activate_law = law_type:law_frontier_colonization
```

et ne reçoit jamais `law_colonial_exploitation`.

## Étape 10 — Comparaison trois voies

Pour chaque candidat sérieux, documente :

- chemin, objet, propriété ou bloc exact ;
- comportements fork, source et vanilla ;
- preuve changelog ou runtime ;
- nombre exact de fichiers, objets et hunks ;
- additions et suppressions prévues ;
- dépendances et localisations ;
- dette adjacente ;
- collision/protection ;
- compatibilité 1776 ;
- rollback exact ;
- priorité P0/P1 ou inférieure ;
- runtime humain futur.

Une différence de hash n'est jamais une preuve suffisante. Ne remplace jamais
un fichier complet et ne combine jamais plusieurs candidats.

## Étape 11 — Critères et top 3

Le candidat retenu doit répondre à un problème unique, disposer d'une preuve
claire, avoir un périmètre atomique, éviter les protections, permettre des
validations statiques reproductibles et posséder un rollback exact.

Ordre de priorité à preuve équivalente :

1. erreur de parsing ou API Victoria 3 1.13 ;
2. erreur moteur directe avec convergence source/vanilla ;
3. delta hotfix explicitement annoncé et dépendances présentes ;
4. petit correctif autonome ;
5. design ou équilibrage.

Publie exactement :

| Rang | Phase candidate | Fichiers | Objets | Hunks | Priorité | Preuve | Collision | Runtime |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |

Explique la comparaison trois voies, la taille, les dépendances, les
localisations, la collision, le report/sélection, le runtime et le rollback de
chacun.

Sélectionne exactement un candidat et publie :

`NEXT_EXECUTION_PHASE = <phase atomique sélectionnée>`

Ne commence pas cette phase.

## Étape 12 — Périmètre d'écriture fermé

Seuls les six documents suivants peuvent être modifiés ou créés :

1. `docs/reports/hotfix/_index/HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`
2. `docs/reports/hotfix/INDEX.md`
3. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
4. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
6. `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Tout changement gameplay impose :

`BLOCKED_SCOPE_VIOLATION`

## Étape 13 — Rapport requis

Crée `HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` avec :

- date, phase, branche, HEAD initial/final ;
- préflight et état Git ;
- hashes et protections ;
- sources ;
- inventaire actualisé, somme 161 et 110 lignes exploitables ;
- analyse des 376 diagnostics et liste des 141 fichiers ;
- top 25 et familles ;
- blocs clos ;
- diagnostics Tanzimat ;
- comparaisons trois voies ;
- pistes obligatoires ;
- exactement trois candidats ;
- exactement un candidat sélectionné ;
- futur périmètre, dépendances, localisations, collision, rollback et runtime ;
- six documents modifiés ;
- contrôles finaux ;
- décision de commit manuel ;
- verdicts.

## Étape 14 — Prompt autonome futur

Remplace `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` par le prompt complet de la phase
atomique sélectionnée. Il doit contenir préflight, hashes, sources, objectif,
fichiers modifiables, objets, hunks, exclusions, protections, validations,
rollback, livrables, verdicts et interdiction de commit automatique.

Si un runtime futur est nécessaire, impose :

- aucun lancement ni pilotage par Codex ;
- tous les contrôles statiques avant lancement ;
- une fiche humaine unique ;
- arrêt `RUNTIME_OPERATOR_ACTION_REQUIRED` ;
- analyse des logs seulement après fermeture humaine confirmée ;
- aucun PASS sans compte rendu humain.

Ne commence pas la phase sélectionnée.

## Étape 15 — Contrôles finaux

Vérifie :

- zéro gameplay modifié ;
- exactement six documents de phase ;
- exactement trois candidats et un sélectionné ;
- catégories exclusives, somme 161, 110 lignes exploitables ;
- baseline 376/141 recalculée ;
- top 25 publié ;
- Tanzimat séparé ;
- Romania et tous les blocs clos non rouverts ;
- huit hashes protégés, BIC, stash, source et vanilla intacts ;
- CSV valides ;
- `git diff --check` propre ;
- index staged vide ;
- aucun processus Victoria 3, `dowser` ou Paradox ;
- aucun lancement ou contrôle du jeu ;
- aucun commit automatique ;
- aucune phase suivante commencée.

Exécute :

```powershell
git diff --check
git status --short
git diff --name-only
git diff --name-status
git diff --stat
git diff --cached --name-only
git stash list
```

## Verdicts

Si la sélection est valide :

- `HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = <phase atomique sélectionnée>`

En cas d'échec :

- `HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION_FAIL`
- verdict de blocage précis.

Ne committe rien automatiquement. Ne commence aucune correction.
