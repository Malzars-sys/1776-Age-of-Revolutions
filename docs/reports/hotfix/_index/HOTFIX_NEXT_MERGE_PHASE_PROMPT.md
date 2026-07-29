# Phase HOTFIX-6A.7F — Alignement API 1.13 du nationalisme grec

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, STRICTEMENT EN LECTURE SEULE :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA VICTORIA 3 1.13, STRICTEMENT EN LECTURE SEULE :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d’entrée requis

- `HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

La phase 6A.7 doit avoir été commitée manuellement avant de commencer. Ne jamais
commencer 6A.7F depuis le worktree documentaire non commité de 6A.7.

## Objectif unique

Dans le seul objet `je_greek_nationalism`, remplacer deux API obsolètes par
leurs équivalents Victoria 3 1.13 sur lesquels la source hotfix et vanilla
convergent.

Fichier gameplay unique :

`common/journal_entries/00_greek_nationalism.txt`

Périmètre exact :

- 1 fichier ;
- 1 objet ;
- 2 hunks ;
- 2 suppressions ;
- 2 additions ;
- aucune localisation ;
- aucune dépendance nouvelle.

Ne modifier aucun autre gameplay et ne remplacer jamais le fichier complet.

## Règle absolue concernant Victoria 3

Codex ne doit jamais :

- lancer Victoria 3 ;
- lancer le launcher Paradox ;
- cliquer dans le jeu ;
- automatiser ou piloter l’interface ;
- ouvrir une sauvegarde ;
- utiliser la console ;
- produire lui-même des observations visuelles ;
- déclarer le runtime PASS sans compte rendu humain.

Après toutes les modifications et validations statiques, Codex doit fournir la
fiche opérateur de la section « Runtime humain » et s’arrêter avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

Les nouveaux logs ne peuvent être analysés qu’après confirmation que Victoria 3
et le launcher sont fermés.

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
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
```

Exiger :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.7 présent dans le HEAD ;
- verdict 6A.7 présent dans le HEAD ;
- 6A.7 déjà commitée manuellement ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` non suivis ;
- stash exact NAVY-3C-3 intact ;
- Victoria 3 et launcher Paradox fermés.

En cas d’écart, arrêter avec :

- `BLOCKED_WRONG_BRANCH`
- `BLOCKED_6A7_NOT_COMMITTED`
- `BLOCKED_DIRTY_TREE`
- `BLOCKED_STAGED_FILES`
- `BLOCKED_UNEXPECTED_UNTRACKED_FILES`
- `BLOCKED_PROTECTED_STASH_MISSING`
- `BLOCKED_GAME_PROCESS_RUNNING`

Interdictions : aucun reset, restore, checkout de fichier, clean, merge, rebase,
amend, commit automatique ou opération sur le stash.

## Sources obligatoires

Lire intégralement avant modification :

- `HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- les trois versions de `common/journal_entries/00_greek_nationalism.txt` ;
- les logs et rotations existants de 6A.6F, en lecture seule.

Hashes de référence enregistrés par 6A.7 :

| Arbre | SHA-256 |
| --- | --- |
| Fork avant correction | `41E56B210D8D990B3F848AA02010E6CE11E0B93A32532FC74A2E225E9A8AFF58` |
| Source hotfix | `76925B166C659F1DA986A445FE8343638465860628DFC5881DB4427CE1877517` |
| Vanilla 1.13 | `E8ACC0F043E30C2578BD9A49375360534073D4562BBC31C6699FF6789BB0E7B9` |

Avant l’édition, exiger le hash fork exact. Pendant toute la phase, exiger que
les hashes source hotfix et vanilla restent identiques.

## Snapshot de protection obligatoire

Avant l’édition, enregistrer depuis le fork :

- le bloc complet `is_shown_in_lobby` ;
- le bloc complet `is_shown_when_inactive` ;
- toutes les occurrences de `geographic_region_megali_greece` ;
- toutes les occurrences de `is_greek_homeland`;
- le nombre d’occurrences des quatre propriétés anciennes et nouvelles ;
- le hash SHA-256 du fichier.

Les blocs de visibilité doivent être byte-for-byte identiques après correction.
Le fork doit conserver dans `is_shown_when_inactive` :

```txt
any_scope_state = {
	is_greek_homeland = yes
}
```

La source hotfix ajoute deux références à
`geographic_region_megali_greece`. Vanilla ne les contient pas. Ces changements
source-only sont explicitement exclus.

## Modifications autorisées

Hunk 1, dans `je_greek_nationalism` :

```diff
-			has_law = law_type:law_monarchy
+			country_has_monarchy_law = yes
```

Hunk 2, dans `je_greek_nationalism` :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Appliquer uniquement ces deux substitutions ciblées.

## Exclusions absolues

Ne modifier ni importer :

- `is_shown_in_lobby` ;
- `is_shown_when_inactive` ;
- `geographic_region_megali_greece` ;
- toute autre géographie grecque ;
- toute autre condition d’activation, d’échec ou de fin ;
- événements, décisions, formations ou pays ;
- localisations ;
- DEI/VOC, Java, Balkan National Awakening, Yugoslavia et Risorgimento ;
- `00_italian_unification.txt` ;
- Grande Crise orientale, Coup et Imperialism of Promise ;
- Merchant Banking et Navigation Acts ;
- NAVY, MARATH, SAT, KHP, Travancore, Inde, BIC, Sepoy, Bombay et ADMIN ;
- Japon, Russie, Autriche, Croatie, Slavonie et Suisse ;
- révolutions américaine et française, lettres de Kew ;
- technologies et recherches ;
- agriculture, alimentation et industrie ;
- descripteurs, launcher, sauvegardes et `bject`.

Préserver dans BIC :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer `law_colonial_exploitation`.

## Liste fermée des fichiers modifiables

Gameplay :

- `common/journal_entries/00_greek_nationalism.txt`.

Documentation :

- nouveau
  `docs/reports/hotfix/_index/HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md` ;
- `docs/reports/hotfix/INDEX.md` ;
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Tout autre changement impose `BLOCKED_SCOPE_VIOLATION`.

## Contrôles statiques obligatoires

Avant édition, le fichier fork doit contenir exactement :

- 1 occurrence de `has_law = law_type:law_monarchy` dans l’objet ;
- 1 occurrence de `should_be_pinned_by_default = yes` dans l’objet ;
- 0 occurrence de `country_has_monarchy_law = yes` dans l’objet ;
- 0 occurrence de
  `should_be_pinned_by_default_uninvolved_or_context = yes` dans l’objet.

Après édition, exiger exactement l’inverse :

- ancienne loi : 0 ;
- ancien pinning : 0 ;
- nouvelle loi : 1 ;
- nouveau pinning : 1.

Vérifier aussi :

1. `git diff -- common/journal_entries/00_greek_nationalism.txt` contient
   exactement 2 hunks, 2 suppressions et 2 additions ;
2. aucune ligne autre que les quatre lignes du diff attendu n’a changé ;
3. accolades équilibrées ;
4. encodage et fins de ligne préservés ;
5. objet `je_greek_nationalism` toujours unique ;
6. blocs `is_shown_in_lobby` et `is_shown_when_inactive` identiques au snapshot ;
7. aucune nouvelle occurrence de `geographic_region_megali_greece` ;
8. aucune localisation modifiée ou requise ;
9. hashes source hotfix et vanilla inchangés ;
10. fichiers protégés et leurs huit hashes 6A.7 inchangés ;
11. stash NAVY-3C-3 intact ;
12. index Git vide ;
13. `git diff --check` propre ;
14. aucun processus Victoria 3 ou Paradox actif.

Si le diff gameplay dépasse exactement deux hunks, arrêter et réduire le
périmètre. Ne corriger aucun autre résidu découvert.

## Rapport requis

Créer :

`docs/reports/hotfix/_index/HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md`

Y inclure :

1. date, branche, HEAD initial et état Git ;
2. preuves trois voies et hashes ;
3. snapshot des blocs protégés ;
4. ancien et nouveau compte des quatre propriétés ;
5. diff exact à deux hunks ;
6. contrôles d’accolades, encodage et périmètre ;
7. protections et exclusions ;
8. rollback ;
9. état statique ;
10. fiche opérateur ;
11. résultats humains et logs seulement après retour humain ;
12. état Git final et décision de commit manuel.

Avant le runtime, publier seulement :

- `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_STATIC_PASS`
- `RUNTIME_OPERATOR_ACTION_REQUIRED`

Ne publier ni `RUNTIME_PASS` ni `COMPLETE` à ce stade.

## Runtime humain

Après PASS statique, remettre exactement cette fiche condensée à l’opérateur :

1. lancer une partie neuve en 1776 avec le fork et `dlc014_ip3` montés ;
2. choisir un pays de culture principale grecque ;
3. si aucun n’est directement jouable, libérer la Grèce depuis l’Empire
   ottoman et la jouer, sans console ;
4. noter le pays et la date de départ ;
5. ouvrir `Journal > Potentiel` et rechercher l’entrée de nationalisme grec ;
6. vérifier que son texte et ses conditions sont lisibles ;
7. vérifier l’absence de clé brute et d’anomalie visible de pinning ;
8. avancer d’au moins un jour et noter la date de fin ;
9. fermer normalement Victoria 3 puis le launcher ;
10. confirmer explicitement leur fermeture et transmettre les observations.

Codex doit alors s’arrêter avec :

`RUNTIME_OPERATOR_ACTION_REQUIRED`

Après le retour humain et seulement après fermeture confirmée, analyser les
nouveaux logs. Exiger :

- erreur ciblée
  `Unexpected token: should_be_pinned_by_default` pour
  `00_greek_nationalism.txt` : 1 avant, 0 après ;
- aucune erreur visant
  `should_be_pinned_by_default_uninvolved_or_context` ;
- aucune erreur visant `country_has_monarchy_law` ;
- fork et `dlc014_ip3` positivement montés ;
- aucune nouvelle erreur propre au fichier corrigé.

Si l’entrée est inaccessible dans le scénario ou le pays choisi, consigner
`RUNTIME_ENTRY_INACCESSIBLE` sans élargir le code. Si les conditions sont
lisibles, sans clé brute ni anomalie de pinning, consigner ces observations
séparément sans inventer un PASS d’activation.

## Rollback exact

En cas de régression, inverser uniquement :

```diff
-			country_has_monarchy_law = yes
+			has_law = law_type:law_monarchy
```

```diff
-	should_be_pinned_by_default_uninvolved_or_context = yes
+	should_be_pinned_by_default = yes
```

Puis refaire tous les contrôles statiques. Ne jamais utiliser reset, restore ou
checkout pour le rollback.

## Verdicts finaux possibles

Après statique uniquement :

- `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_STATIC_PASS`
- `RUNTIME_OPERATOR_ACTION_REQUIRED`

Après compte rendu humain et analyse des nouveaux logs :

- `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_RUNTIME_PASS`
- `GREEK_NATIONALISM_MONARCHY_TRIGGER_1_13_ALIGNED`
- `GREEK_NATIONALISM_JE_PINNING_1_13_ALIGNED`
- `GREEK_VISIBILITY_AND_GEOGRAPHY_UNCHANGED`
- `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Ne committer automatiquement ni avant ni après le runtime. Ne commencer aucune
phase suivante.
