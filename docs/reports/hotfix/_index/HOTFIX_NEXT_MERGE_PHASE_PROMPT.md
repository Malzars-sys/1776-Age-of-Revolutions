# Prompt autonome — HOTFIX-6A.12F Alignement 1.13 des régions stratégiques du colonialisme portugais

Nous poursuivons le portage du mod Victoria 3 :

`1776_Age_of_Revolutions_fork`

# Phase HOTFIX-6A.12F — Alignement Victoria 3 1.13 des deux régions stratégiques du colonialisme portugais

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Nature de la phase

Cette phase applique exactement deux substitutions de clés de régions
stratégiques dans un seul objet de journal entry, effectue les contrôles
statiques, prépare un runtime humain unique puis s'arrête. Codex ne doit
jamais lancer Victoria 3, lancer ou piloter le launcher, cliquer dans le jeu,
utiliser la console, ouvrir une sauvegarde, créer un commit automatique ni
étendre le périmètre.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, strictement en lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, strictement en lecture seule :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d'entrée requis

- `HOTFIX_6A12_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_SELECTED`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A12_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

6A.12 doit être commitée manuellement avant de commencer. Ne jamais commencer
depuis son worktree documentaire non commité.

## Objectif unique

Dans l'objet `je_portuguese_colonialism` de
`common/journal_entries/06_portuguese_colonialism.txt`, remplacer exactement :

```txt
sr:region_congo
sr:region_zanj
```

par :

```txt
sr:region_equatorial_africa
sr:region_east_africa
```

Conserver les noms de scopes sauvegardés `congo_scope` et `zanj_scope`. Ne
modifier aucun autre octet gameplay.

## Préflight Git obligatoire

Exécuter :

```powershell
Set-Location "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork"

git rev-parse --show-toplevel
git branch --show-current
git status --short
git log -5 --oneline --decorate
git diff --check
git diff --cached --name-only
git stash list
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A12_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
```

Exiger :

- racine exacte et branche `hotfix-dlc-audit`;
- rapport et verdicts 6A.12 présents dans `HEAD`;
- fichiers suivis propres et index staged vide;
- seuls `bject` et les sept fichiers de `docs/research/technology/` non suivis;
- stash exact
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`;
- aucun processus Victoria 3, `dowser` ou Paradox.

Arrêter avec le verdict précis en cas d'écart :

- `BLOCKED_WRONG_BRANCH`
- `BLOCKED_6A12_NOT_COMMITTED`
- `BLOCKED_DIRTY_TREE`
- `BLOCKED_STAGED_FILES`
- `BLOCKED_UNEXPECTED_UNTRACKED_FILES`
- `BLOCKED_PROTECTED_STASH_MISSING`
- `BLOCKED_GAME_PROCESS_RUNNING`

Interdictions Git : reset, restore, checkout de fichier, clean, merge, rebase,
amend, commit automatique, stash apply/pop/drop et inspection du stash.

## Hashes de référence obligatoires

| Preuve | SHA-256 |
| --- | --- |
| Fork `06_portuguese_colonialism.txt` avant correction | `DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20` |
| Source hotfix | `04CCCCF13E9D7B4EA1DBBB29F86861CA8B1DB7F77B635175A39D889B9234EE7A` |
| Vanilla 1.13 | `15834E8FE1DBA56ADD9D970F9CECDF8AD1FB45100585770A457DF96BDF65FDF4` |
| Fork après les deux seules substitutions | `99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126` |
| Romania fork | `DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578` |
| Sick Man fork | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` |
| Grande Crise orientale fork | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` |
| BIC fork | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` |

Vérifier aussi les sept hashes technologie consignés dans 6A.12. Tout écart
avant correction impose `BLOCKED_THREE_WAY_EVIDENCE_CHANGED`. Source et
vanilla restent strictement inchangées.

## Sources obligatoires

Lire intégralement :

- les rapports 6A.12, 6A.11F et 6A.11;
- roadmap, block status et report index;
- les trois versions du fichier cible;
- les définitions vanilla
  `common/strategic_regions/african_strategic_regions.txt`;
- les localisations anglaises et françaises de la chaîne portugaise;
- les logs 6A.11F et leurs rotations, en lecture seule.

Ne pas lancer le jeu pour créer une preuve.

## Snapshot pré-correction obligatoire

Exiger dans l'`immediate` de `je_portuguese_colonialism` :

```txt
sr:region_congo = {
	save_scope_as = congo_scope
}
sr:region_zanj = {
	save_scope_as = zanj_scope
}
```

Exiger exactement une occurrence de chaque ancienne clé et zéro occurrence
des deux clés modernes dans ce fichier. Conserver les deux propriétés de
pinning modernes aux lignes historiques 6 et 181 et enregistrer leur contexte.

## Périmètre d'écriture fermé avant le runtime

Seuls ces deux fichiers peuvent être modifiés ou créés avant l'arrêt opérateur :

1. `common/journal_entries/06_portuguese_colonialism.txt`
2. `docs/reports/hotfix/_index/HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT.md`

Après confirmation humaine du runtime et fermeture complète du jeu et du
launcher, seuls les quatre documents de navigation suivants peuvent aussi être
modifiés :

3. `docs/reports/hotfix/INDEX.md`
4. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`
6. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`

Ne pas modifier ce prompt pendant 6A.12F. Tout autre changement impose
`BLOCKED_SCOPE_VIOLATION`.

## Hunk exact

Un seul hunk unifié, dans `je_portuguese_colonialism` :

```diff
-        sr:region_congo = {
+        sr:region_equatorial_africa = {
             save_scope_as = congo_scope
         }
-        sr:region_zanj = {
+        sr:region_east_africa = {
             save_scope_as = zanj_scope
         }
```

Diff attendu : un fichier, un objet, un hunk unifié, deux additions et deux
suppressions. Ne jamais remplacer le fichier complet.

## Preuve géographique

Source hotfix et vanilla 1.13 convergent sur les deux nouvelles clés. Dans
`african_strategic_regions.txt`, `region_equatorial_africa` couvre notamment
le Congo et l'Angola, tandis que `region_east_africa` couvre notamment le
Mozambique. Le fork et la source ne redéfinissent pas ces régions : ils
héritent des définitions vanilla.

## Exclusions adjacentes absolues

Ne pas importer ou modifier :

- le filtre de culture portugaise;
- `geographic_region_iberia_old`;
- la prise en charge de `c:IBE`;
- les événements ou la progression de Pink Map;
- les titres, raisons, tooltips ou autres localisations;
- les noms `congo_scope` et `zanj_scope`;
- le texte français répété « Royaume de Portugal ».

La répétition du nom est systémique : elle implique la clé générique française
`TRIGGER_HAS_LAW_OR_VARIANT_FIRST` et le nom dynamique
`dyn_c_portu_king`. Elle n'appartient pas à ce correctif atomique.

## Protections absolues

Ne toucher à aucun élément DEI/VOC, Java, NAVY, MARATH, SAT, KHP, Travancore,
Inde/BIC/Sepoy/Bombay, ADMIN, Japon, Russie, Autriche/Croatie/Suisse,
révolutions américaine ou française, technologies, recherche, agriculture,
alimentation, industrie générale, descripteur, launcher, sauvegarde, `bject`,
Tanzimat, Sick Man, Grande Crise orientale, Balkans clos ou Romania.

BIC doit conserver :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer `law_colonial_exploitation`.

## Validations statiques obligatoires

Après correction, exiger :

1. hash cible
   `99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126`;
2. zéro `sr:region_congo` et zéro `sr:region_zanj` dans le fichier;
3. exactement un `sr:region_equatorial_africa` et un
   `sr:region_east_africa`;
4. `congo_scope` et `zanj_scope` inchangés;
5. diff limité à un fichier, un objet, un hunk unifié et `2/2`;
6. propriétés de pinning modernes conservées dans leurs deux objets;
7. accolades équilibrées;
8. BOM et fins de ligne LF préservés;
9. aucune modification source/vanilla;
10. hashes Romania, Sick Man, Grande Crise orientale, BIC, `bject`,
    technologie et stash inchangés;
11. aucun processus de jeu;
12. `git diff --check` propre et index staged vide.

Si le hash cible n'est pas atteint, ne pas reformater : annuler les deux
substitutions puis diagnostiquer.

## Rollback exact

Dans `je_portuguese_colonialism` seulement, remplacer :

```txt
sr:region_equatorial_africa
sr:region_east_africa
```

par :

```txt
sr:region_congo
sr:region_zanj
```

Le rollback doit restaurer le hash
`DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20`.

## Runtime humain obligatoire

Après tous les contrôles statiques et la fiche opérateur rédigée, Codex doit
s'arrêter avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

La fiche humaine doit demander un seul lancement avec le fork monté et
`dlc014_ip3`, une nouvelle partie avec le Portugal au 1er janvier 1776, puis
une progression au 2 janvier 1776. Ouvrir Journal > Potentiel > « Além-mar
africain » et vérifier :

- chargement sans anomalie;
- entrée potentielle visible et lisible;
- les raisons géographiques parlent correctement de l'Angola et du Mozambique;
- aucune clé brute ou anomalie visible de portée;
- fermeture complète du jeu et du launcher;
- compte rendu humain explicite.

Codex ne lance et ne pilote rien. Après confirmation de fermeture, lire les
nouveaux logs seulement. Le PASS attendu est :

- `region_congo` invalide : `186 → 0`;
- `region_zanj` invalide : `186 → 0`;
- diagnostics associés `sr` non défini : `373 → 0`;
- zéro diagnostic ciblé nouveau;
- baseline du parser de pinning inchangée à `374/140`;
- montage du fork et de `dlc014_ip3` prouvé.

Aucun PASS runtime ne peut être déclaré sans compte rendu humain.

## Livrables

Le rapport 6A.12F doit contenir préflight, hashes, snapshot, comparaison trois
voies, preuve géographique, diff exact, exclusions, validations statiques,
fiche humaine, compte rendu humain, logs post-runtime, baseline parser,
montage, protections, rollback, état Git initial/final et décision de commit
manuel.

Mettre à jour les quatre documents de navigation autorisés seulement après le
runtime. Ne créer aucun commit.

## Verdicts

Après statique :

- `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_STATIC_PASS`
- `PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_ONE_HUNK_1_13_ALIGNMENT_COMPLETE`
- `PORTUGUESE_COLONIALISM_SCOPE_NAMES_PINNING_AND_PROGRESSION_UNCHANGED`
- `RUNTIME_OPERATOR_ACTION_REQUIRED`

Après runtime humain et analyse des logs :

- `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_RUNTIME_PASS`
- `PORTUGUESE_COLONIALISM_INVALID_STRATEGIC_REGION_DIAGNOSTICS_REMOVED`
- `PORTUGUESE_COLONIALISM_1776_VISIBILITY_GEOGRAPHY_AND_PROGRESSION_VALIDATED`
- `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

En cas d'échec :

- `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT_FAIL`
- verdict de blocage précis.

## Contrôles finaux

Exécuter :

```powershell
git diff --check
git status --short
git diff --name-only
git diff --name-status
git diff --stat
git diff --cached --name-only
git stash list
```

Confirmer un seul fichier gameplay, exactement cinq documents, aucun autre
fichier, source/vanilla intactes, BIC intact, neuf groupes de hashes protégés
intacts, stash intact, aucun processus de jeu, aucun lancement par Codex et
aucun commit automatique.
