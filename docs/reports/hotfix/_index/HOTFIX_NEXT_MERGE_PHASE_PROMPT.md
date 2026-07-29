# Phase HOTFIX-6A.8R — Audit Victoria 3 1.13 de la Grande Crise orientale

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

- `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_RUNTIME_PASS`
- `GREEK_NATIONALISM_MONARCHY_TRIGGER_1_13_ALIGNED`
- `GREEK_NATIONALISM_JE_PINNING_1_13_ALIGNED`
- `GREEK_VISIBILITY_AND_GEOGRAPHY_UNCHANGED`
- `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT_COMPLETE`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md`

6A.7F doit avoir été commitée manuellement avant de commencer.

## Nature de la phase

6A.8R est strictement documentaire.

Codex ne doit jamais :

- lancer Victoria 3 ou le launcher Paradox ;
- piloter l’interface du jeu ;
- produire de nouveaux logs ;
- modifier un fichier gameplay ;
- appliquer un hunk de la Grande Crise orientale ;
- remplacer un fichier complet ;
- commencer une future correction.

Aucun runtime n’est requis pendant l’audit.

## Objectif unique

Auditer en trois voies les six hunks fonctionnels de l’objet :

`je_great_eastern_crisis`

dans :

`common/journal_entries/05_great_eastern_crisis.txt`

L’audit doit déterminer si ces six hunks forment une correction atomique
cohérente ou s’ils doivent être séparés, protégés ou reportés.

Ne présumer ni l’import de la source hotfix ni l’alignement complet sur vanilla.

## Préflight Git obligatoire

```powershell
Set-Location "C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork"

git rev-parse --show-toplevel
git branch --show-current
git status --short
git log -5 --oneline --decorate
git diff --check
git diff --cached --name-only
git stash list
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md
```

Exiger :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.7F présent dans le HEAD ;
- verdicts runtime et de clôture présents dans le HEAD ;
- 6A.7F commitée manuellement ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` non suivis ;
- stash NAVY-3C-3 intact ;
- Victoria 3 et launcher Paradox fermés.

En cas d’écart :

- `BLOCKED_WRONG_BRANCH`
- `BLOCKED_6A7F_NOT_COMMITTED`
- `BLOCKED_DIRTY_TREE`
- `BLOCKED_STAGED_FILES`
- `BLOCKED_UNEXPECTED_UNTRACKED_FILES`
- `BLOCKED_PROTECTED_STASH_MISSING`
- `BLOCKED_GAME_PROCESS_RUNNING`

Interdictions : aucun reset, restore, checkout, clean, merge, rebase, amend,
commit automatique ou opération sur le stash.

Enregistrer avant tout travail les huit hashes protégés de `bject` et des sept
recherches technologiques.

## Sources obligatoires

Lire intégralement :

- `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md` ;
- `HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les changelogs du fork et de la source hotfix ;
- les logs existants 6A.7F, en lecture seule.

Comparer intégralement :

1. fork :
   `common/journal_entries/05_great_eastern_crisis.txt` ;
2. source hotfix, lecture seule :
   `common/journal_entries/05_great_eastern_crisis.txt` ;
3. vanilla 1.13, lecture seule :
   `common/journal_entries/05_great_eastern_crisis.txt`.

Enregistrer les trois hashes SHA-256 et les conserver inchangés pendant
l’audit.

## Baseline actualisée

Après 6A.7F :

- anciennes erreurs globales de pinning : 387 ;
- erreur grecque : 0 ;
- `VANILLA_1_13_ALIGNMENT_REQUIRED` : 18 ;
- `ALREADY_MERGED` : 16 ;
- lignes directement exploitables : 112 ;
- total historique de 26 deltas : `UNVERIFIED`.

Les blocs 6A.3F à 6A.7F sont clos et ne peuvent pas redevenir candidats.

## Six hunks à auditer

Documenter séparément, avec numéros de ligne et blocs complets :

1. première référence géographique
   `geographic_region_balkans` /
   `geographic_region_balkans_old` ;
2. seconde référence géographique
   `geographic_region_balkans` /
   `geographic_region_balkans_old` ;
3. scope `region_balkans` / `sr:region_balkans` ;
4. bloc `should_show_when_not_involved` ;
5. propriété `can_revolution_inherit = yes` ;
6. sémantique de pinning :

```txt
should_be_pinned_by_default_involved = yes
should_be_pinned_by_default_uninvolved_or_context = no
```

Le fork contient historiquement une erreur directe sur l’ancien champ
`should_be_pinned_by_default`. La session 6A.7F doit en contenir exactement une
pour `05_great_eastern_crisis.txt`.

Ne pas réduire l’audit à cette seule erreur parser.

## Comparaison exigée pour chaque hunk

Pour chacun des six hunks, publier :

- chemin et objet exacts ;
- bloc parent ;
- texte exact du fork ;
- texte exact de la source hotfix ;
- texte exact de vanilla ;
- convergence ou divergence ;
- comportement moteur attendu ;
- impact 1776 ;
- dépendances de scope ou région ;
- collision avec les autres hunks ;
- localisation éventuelle ;
- risque de régression ;
- rollback futur ;
- décision exclusive :
  - `REQUIRED_1_13_ALIGNMENT`
  - `REQUIRED_HOTFIX_DELTA`
  - `INTENTIONAL_1776_DIVERGENCE`
  - `DEFER_REQUIRES_DESIGN_DECISION`
  - `ALREADY_EQUIVALENT`

Une différence de hash ou le nom identique d’un fichier ne constitue jamais une
preuve suffisante.

## Questions sémantiques obligatoires

L’audit doit répondre précisément :

1. pourquoi les deux régions utilisent ou non le suffixe `_old` ;
2. si `sr:region_balkans` est une correction de scope obligatoire en 1.13 ;
3. qui doit voir l’entrée sans être impliqué ;
4. si le comportement de pinning impliqué/non impliqué correspond au bloc de
   visibilité ;
5. pourquoi une révolution doit ou non hériter de l’entrée ;
6. si les six changements sont indissociables ;
7. si une future correction peut rester limitée à 1 fichier, 1 objet et
   exactement 6 hunks ;
8. si le diff prévu reste exactement de 23 additions et 4 suppressions ;
9. si un runtime humain sera requis après une future correction ;
10. quel scénario humain minimal pourra valider l’entrée.

## Protections absolues

Ne modifier ni rouvrir :

- nationalisme grec et `00_greek_nationalism.txt` ;
- Balkan National Awakening ;
- Yugoslavia ;
- Risorgimento ;
- DEI/VOC et Java ;
- Coup et Imperialism of Promise ;
- Merchant Banking et Navigation Acts ;
- NAVY, formations et lois navales ;
- MARATH, SAT, KHP et Travancore ;
- Inde, BIC, Sepoy et Bombay ;
- ADMIN ;
- Japon, Russie, Autriche, Croatie, Slavonie et Suisse ;
- révolutions américaine et française ;
- lettres de Kew ;
- technologies et recherches ;
- agriculture, alimentation et industrie ;
- localisations générales ;
- descripteurs, launcher, sauvegardes et `bject`.

Préserver BIC avec `law_frontier_colonization`. Ne jamais restaurer
`law_colonial_exploitation`.

## Liste fermée des fichiers modifiables

Uniquement :

- nouveau
  `docs/reports/hotfix/_index/HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT.md` ;
- `docs/reports/hotfix/INDEX.md` ;
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Le fichier `05_great_eastern_crisis.txt` est en lecture seule.

## Livrable

Créer le rapport 6A.8R avec :

1. préflight et HEAD ;
2. sources ;
3. hashes trois voies ;
4. erreur runtime historique ;
5. carte exacte des six hunks ;
6. comparaison trois voies de chaque hunk ;
7. classification exclusive ;
8. dépendances et collisions ;
9. impact 1776 ;
10. localisations ;
11. taille future exacte ;
12. rollback futur ;
13. scénario runtime humain futur ;
14. protections ;
15. décision atomique ;
16. futur prompt autonome ;
17. état Git final ;
18. décision de commit manuel.

Si les six hunks sont prouvés cohérents, préparer une future phase de correction
sans l’exécuter. Sinon, documenter exactement les sous-blocs ou décisions qui
bloquent.

## Contrôles finaux

Vérifier :

- zéro gameplay modifié ;
- exactement six documents de phase ;
- six hunks audités séparément ;
- une classification par hunk ;
- aucune phase close rouverte ;
- source hotfix et vanilla inchangées ;
- huit hashes protégés inchangés ;
- stash intact ;
- index Git vide ;
- `git diff --check` propre ;
- Victoria 3 et launcher fermés ;
- aucun lancement ou contrôle du jeu par Codex.

Ne committer rien automatiquement et ne commencer aucune correction.

## Verdicts possibles

Si l’audit est résolu :

- `HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT_COMPLETE`
- `GREAT_EASTERN_CRISIS_SIX_HUNK_DECISION_RECORDED`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = <phase décidée>`

Sinon :

- `HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT_BLOCKED`
- verdict de blocage précis.
