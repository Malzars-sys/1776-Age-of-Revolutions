# Prompt autonome — HOTFIX-6A.10F Romania two-JE pinning 1.13 alignment

Nous poursuivons le portage du mod Victoria 3 :

`1776_Age_of_Revolutions_fork`

# Phase HOTFIX-6A.10F — Alignement du pinning de deux journal entries roumaines

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Nature de la phase

Cette phase applique exactement deux substitutions d'API Victoria 3 1.13 dans
un seul fichier gameplay, effectue les contrôles statiques, prépare une seule
fiche runtime humaine condensée, puis s'arrête.

Codex ne doit jamais :

- lancer Victoria 3 ;
- lancer le launcher Paradox ;
- cliquer ou interagir dans le jeu ;
- piloter ou automatiser l'interface ;
- utiliser la console ;
- ouvrir une sauvegarde ;
- produire un PASS runtime sans compte rendu humain ;
- créer un commit automatique.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, STRICTEMENT EN LECTURE SEULE :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA VICTORIA 3 1.13, STRICTEMENT EN LECTURE SEULE :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d'entrée requis

- `HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

La phase 6A.10 doit avoir été commitée manuellement avant de commencer. Ne
commence jamais 6A.10F depuis le worktree documentaire non commité de 6A.10.

## Objectif unique

Dans `common/journal_entries/00_romania.txt`, remplacer uniquement les deux
propriétés obsolètes :

```txt
should_be_pinned_by_default = yes
```

par :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

Objets exacts :

1. `je_unite_the_principalities`, ligne initiale 76 ;
2. `je_all_for_one`, ligne initiale 149.

Le futur diff gameplay doit compter exactement :

- un fichier ;
- deux objets ;
- deux hunks unifiés `@@` ;
- deux suppressions ;
- deux additions.

Ne modifier aucune autre ligne.

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
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
```

Exige :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.10 et ses quatre verdicts présents dans HEAD ;
- phase 6A.10 déjà commitée manuellement ;
- worktree suivi propre ;
- index staged vide ;
- seuls `bject` et les sept fichiers de
  `docs/research/technology/` peuvent être non suivis ;
- stash exact
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- aucun processus Victoria 3, `dowser` ou Paradox.

Avant toute modification, enregistre les hashes de `bject` et des sept fichiers
de recherche technologique et compare-les à 6A.10.

Arrête immédiatement avec un verdict précis en cas d'écart :

- `BLOCKED_WRONG_BRANCH`
- `BLOCKED_6A10_NOT_COMMITTED`
- `BLOCKED_DIRTY_TREE`
- `BLOCKED_STAGED_FILES`
- `BLOCKED_UNEXPECTED_UNTRACKED_FILES`
- `BLOCKED_PROTECTED_STASH_MISSING`
- `BLOCKED_GAME_PROCESS_RUNNING`

Interdictions Git : aucun reset, restore, checkout de fichier, clean, merge,
rebase, amend, commit automatique, stash apply/pop/drop ou inspection du
contenu du stash.

## Étape 2 — Hashes obligatoires

Vérifie avant toute modification :

| Preuve | SHA-256 |
| --- | --- |
| Fork `common/journal_entries/00_romania.txt` | `D5925DEB54D4E0E4BB6E96DAF5106CAADBA35CC18E451D4898A7F1B7AA1AE078` |
| Source hotfix `00_romania.txt` | `74149D3A3B778732DE318D7FB522CE4255289B410F6184625BA9670E6CCCAB9A` |
| Vanilla `00_romania.txt` | `9B5C9A9D06DAA420030BBC3B31581CD030356145FD31E1589E590AB9DF904A51` |
| Fork `00_sick_man.txt` | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` |
| Histoire TUR fork | `81ABC8DEA9DE93EC6A4DD417FD05FD6859F3122758D2B27E712B1880013F9CA9` |
| Grande Crise orientale fork | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` |
| BIC fork | relever et consigner sans le modifier |

Hashes protégés à comparer avec 6A.10 :

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

Source hotfix et vanilla restent strictement en lecture seule.

## Étape 3 — Sources obligatoires

Lis intégralement :

- `HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- les trois copies de `common/journal_entries/00_romania.txt` ;
- les localisations anglaise et française vanilla des deux JE ;
- les nouveaux logs 6A.9F et leurs rotations, en lecture seule.

## Étape 4 — Snapshot initial ciblé

Avant modification, exige pour le fichier fork :

- hash
  `D5925DEB54D4E0E4BB6E96DAF5106CAADBA35CC18E451D4898A7F1B7AA1AE078` ;
- 3 857 octets ;
- UTF-8 BOM ;
- 150 LF ;
- zéro CRLF ;
- saut final conservé ;
- 48 accolades ouvrantes et 48 fermantes ;
- exactement deux propriétés anciennes ;
- zéro propriété moderne ;
- exactement deux diagnostics ciblés dans le nouveau `debug.log`, lignes
  gameplay 76 et 149.

Vérifie séparément que source et vanilla utilisent la propriété moderne dans
les deux objets. Une différence de hash globale ne justifie aucune autre
modification.

## Étape 5 — Modification fermée

Modifie avec un patch ciblé uniquement :

```diff
 je_unite_the_principalities = {
@@
-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
 }

 je_all_for_one = {
@@
-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
 }
```

Préserve exactement l'indentation existante, l'UTF-8 BOM, les LF et le saut
final. Ne remplace jamais le fichier complet.

Hash gameplay attendu après ces deux substitutions :

`DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578`

Snapshot attendu :

- 3 901 octets ;
- UTF-8 BOM ;
- 150 LF ;
- zéro CRLF ;
- 48/48 accolades ;
- zéro propriété ancienne ;
- deux propriétés modernes.

## Étape 6 — Exclusions absolues

Ne modifie pas :

- `is_shown_in_lobby` ;
- `is_shown_when_inactive` ;
- `geographic_region_greater_romania` ou toute autre géographie ;
- `any_country`, tout helper de state ou tout scope ;
- `possible`, `complete`, `fail`, `on_complete` ou `on_fail` ;
- `on_monthly_pulse`, `romanian_union_var` ou la progression ;
- les scripted buttons ;
- les tooltips ;
- les localisations ;
- l'histoire de WAL, MOL ou ROM ;
- tout autre journal entry.

Protections absolues : DEI/VOC, Java, économie post-compagnie, Balkan National
Awakening, Yugoslavia, Risorgimento, nationalisme grec, Grande Crise orientale,
Sick Man, activation Tanzimat, NAVY, formations et événements navals, MARATH,
SAT, KHP, Travancore, Inde, BIC, Sepoy, Bombay, ADMIN, Japon, Russie, Autriche,
Croatie, Slavonie, Suisse, révolutions américaine et française, lettres de
Kew, technologies, recherche technologique, localisations françaises
générales, agriculture, alimentation, industrie générale, descripteurs,
launcher, sauvegardes et `bject`.

BIC doit conserver :

```txt
activate_law = law_type:law_frontier_colonization
```

et ne doit jamais recevoir :

```txt
law_colonial_exploitation
```

Merchant Banking, Navigation Acts, Coup, Imperialism of Promise et Tanzimat
restent hors périmètre. Ne commence aucune de ces phases.

## Étape 7 — Validations statiques avant tout runtime

Vérifie :

1. hash gameplay final exact ;
2. snapshot structurel exact ;
3. deux propriétés anciennes → zéro ;
4. zéro propriété moderne → deux ;
5. exactement un fichier gameplay modifié ;
6. exactement deux objets ;
7. exactement deux hunks `@@` ;
8. exactement deux additions et deux suppressions gameplay ;
9. aucune ligne adjacente modifiée ;
10. source hotfix et vanilla inchangés ;
11. huit hashes protégés inchangés ;
12. BIC intact ;
13. stash NAVY-3C-3 intact ;
14. `git diff --check` propre ;
15. index staged vide ;
16. aucun processus Victoria 3, `dowser` ou Paradox.

En cas d'écart, applique le rollback exact avant tout runtime :

```diff
-    should_be_pinned_by_default_uninvolved_or_context = yes
+    should_be_pinned_by_default = yes
```

dans les deux objets, puis confirme le hash initial. Si le rollback ciblé ne
restaure pas exactement le snapshot initial, arrête avec
`BLOCKED_ROLLBACK_MISMATCH` sans utiliser de commande Git destructive.

## Étape 8 — Fiche runtime humaine unique

Seulement après tous les PASS statiques, prépare une seule fiche :

1. l'opérateur humain lance Victoria 3 avec le fork ;
2. il commence une partie neuve au setup 1776 avec la Valachie (`WAL`) ;
3. il confirme que le mod fork et `dlc014_ip3` sont montés ;
4. il ouvre le journal et vérifie que « Unir les principautés » est lisible
   parmi les entrées potentielles, sans clé brute ni anomalie de pinning ;
5. il avance au 2 janvier 1776 ;
6. il ferme le jeu et le launcher ;
7. il transmet un compte rendu humain condensé.

Codex s'arrête alors obligatoirement avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

Codex n'analyse aucun nouveau log avant la confirmation humaine explicite que
le jeu et le launcher sont fermés. Aucun PASS runtime ne peut être déduit de
la seule absence de processus ou des logs.

## Étape 9 — Analyse après fermeture humaine

Après confirmation humaine :

- snapshotte les nouveaux logs et rotations ;
- prouve le montage du fork et de `dlc014_ip3` ;
- recalcule le nombre de diagnostics
  `Unexpected token: should_be_pinned_by_default,` ;
- exige zéro diagnostic ciblant `00_romania.txt:76` et `:149` ;
- exige zéro rejet de
  `should_be_pinned_by_default_uninvolved_or_context` dans ce fichier ;
- sépare les diagnostics Tanzimat et toutes les autres erreurs hors périmètre ;
- ne corrige aucune nouvelle anomalie.

Baseline attendue si aucun autre changement n'intervient :

- diagnostics globaux de pinning : 378 → 376 ;
- fichiers uniques concernés : 142 → 141 ;
- diagnostics ciblés Romania : 2 → 0.

Le compte rendu humain doit confirmer l'ouverture lisible de l'entrée
potentielle et le passage au 2 janvier 1776. Il ne doit pas prétendre rendre
active `je_all_for_one`, qui dépend d'une union roumaine ; son chargement est
validé par le parser.

## Étape 10 — Périmètre d'écriture fermé

Seuls les sept fichiers suivants peuvent être modifiés ou créés :

1. `common/journal_entries/00_romania.txt`
2. `docs/reports/hotfix/_index/HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md`
3. `docs/reports/hotfix/INDEX.md`
4. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
6. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`
7. `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`

Tout autre changement impose :

`BLOCKED_SCOPE_VIOLATION`

## Étape 11 — Livrables

Crée le rapport
`HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md` avec :

- date, phase, branche, HEAD initial/final ;
- préflight et état Git initial ;
- hashes trois voies et protégés ;
- snapshot avant/après ;
- diff exact ;
- exclusions et protections ;
- validations statiques ;
- fiche et compte rendu runtime humain ;
- comparaison des logs avant/après ;
- rollback ;
- documents modifiés ;
- contrôles finaux ;
- état Git final ;
- décision de commit manuel ;
- verdicts.

Mets à jour les quatre index/roadmap et remplace le prochain prompt uniquement
après le verdict runtime. Le prochain prompt doit sélectionner
documentairement le résidu suivant ; il ne doit commencer ni Merchant Banking
ni Navigation Acts automatiquement.

## Étape 12 — Contrôles finaux

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

Confirme :

- un seul fichier gameplay, deux objets et deux hunks ;
- uniquement les sept fichiers autorisés ;
- hash cible et snapshot conformes ;
- deux erreurs ciblées ramenées à zéro ;
- aucune dette adjacente importée ;
- aucun bloc clos rouvert ;
- protections, BIC, stash, source et vanilla intacts ;
- CSV valides ;
- index staged vide ;
- aucun processus Victoria 3, `dowser` ou Paradox ;
- aucune interaction Codex avec le jeu ;
- aucun commit automatique ;
- aucune phase suivante commencée.

## Verdicts

Après PASS statique mais avant action humaine :

- `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_STATIC_PASS`
- `ROMANIA_TWO_JE_PINNING_TWO_HUNK_1_13_ALIGNMENT_COMPLETE`
- `RUNTIME_OPERATOR_ACTION_REQUIRED`

Après compte rendu humain et analyse des nouveaux logs :

- `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_RUNTIME_PASS`
- `ROMANIA_TWO_JE_PINNING_PARSER_ERRORS_2_TO_0`
- `ROMANIA_1776_VISIBILITY_GEOGRAPHY_AND_PROGRESSION_UNCHANGED`
- `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

En cas d'échec :

- `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT_FAIL`
- verdict de blocage précis.

Ne committe rien automatiquement. Ne commence aucune autre phase.
