# Phase HOTFIX-6A.7 — Sélection du prochain résidu global

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, STRICTEMENT EN LECTURE SEULE :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA VICTORIA 3 1.13, STRICTEMENT EN LECTURE SEULE :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d'entrée requis

- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_COMPLETE`
- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_RUNTIME_PASS`
- `ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md`

La phase 6A.6F doit avoir été commitée manuellement avant de commencer.

## Règle absolue concernant Victoria 3

Cette phase est strictement documentaire.

Codex ne doit jamais :

- lancer Victoria 3 ;
- lancer le launcher Paradox ;
- cliquer dans le jeu ;
- automatiser ou piloter l'interface ;
- ouvrir une sauvegarde ;
- utiliser la console ;
- produire de nouveaux logs ;
- déclarer une observation visuelle.

Aucun runtime n'est nécessaire pendant 6A.7.

Toute future phase sélectionnée qui exige un runtime devra :

1. terminer ses changements et contrôles statiques ;
2. préparer une fiche condensée pour un seul lancement humain ;
3. s'arrêter avec `RUNTIME_OPERATOR_ACTION_REQUIRED` ;
4. attendre le compte rendu de l'opérateur ;
5. analyser les nouveaux logs seulement après fermeture confirmée du jeu et du
   launcher.

## Objectif unique

Sélectionner exactement un prochain sous-bloc atomique parmi les résidus globaux
encore ouverts.

Cette phase doit uniquement :

- actualiser l'inventaire après clôture de 6A.6F ;
- analyser les 388 erreurs de pinning restantes sans les corriger ;
- comparer les candidats en trois voies ;
- publier exactement trois meilleurs candidats ;
- sélectionner un seul candidat ;
- préparer le prompt autonome de son exécution future.

Ne modifier aucun gameplay. Ne commencer aucun candidat.

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
```

Exiger :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.6F présent dans le HEAD ;
- 6A.6F déjà commitée manuellement ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls `bject` et les sept fichiers de `docs/research/technology/` non suivis ;
- stash exact NAVY-3C-3 intact ;
- Victoria 3 et launcher Paradox fermés.

En cas d'écart, arrêter avec :

- `BLOCKED_WRONG_BRANCH`
- `BLOCKED_6A6F_NOT_COMMITTED`
- `BLOCKED_DIRTY_TREE`
- `BLOCKED_STAGED_FILES`
- `BLOCKED_UNEXPECTED_UNTRACKED_FILES`
- `BLOCKED_PROTECTED_STASH_MISSING`
- `BLOCKED_GAME_PROCESS_RUNNING`

Interdictions : aucun reset, restore, checkout de fichier, clean, merge, rebase,
amend, commit automatique ou opération sur le stash.

## Sources obligatoires

Lire intégralement :

- `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- changelogs fork et source hotfix ;
- logs et rotations existants de 6A.6F.

Ne pas lancer le jeu pour obtenir de nouvelles preuves.

## Base canonique actualisée

Après clôture de 6A.6F, les 161 anciennes lignes `PENDING_REVIEW` doivent être
actualisées ainsi :

- 7 `REQUIRED_HOTFIX_DELTA` ;
- 19 `VANILLA_1_13_ALIGNMENT_REQUIRED` ;
- 15 `ALREADY_MERGED` ;
- 3 `INTENTIONAL_FORK_DIVERGENCE` ;
- 1 `OBSOLETE_HOTFIX_CONTENT` ;
- 10 `POST_MERGE_DESIGN_BACKLOG` ;
- 19 `PROTECTED_CONCURRENT_WORK` ;
- 87 `UNKNOWN_REQUIRES_REVIEW`.

Il reste 113 lignes directement exploitables par une revue :

- 7 deltas hotfix requis ;
- 19 alignements vanilla 1.13 ;
- 87 inconnus.

Ce total ne représente pas 113 correctifs. Le total historique de 26 deltas à
haute confiance reste `UNVERIFIED`.

Sont clos et ne doivent jamais redevenir candidats :

- `common/journal_entries/05_balkan_national_awakening.txt` ;
- `common/journal_entries/05_creation_of_yugoslavia.txt` ;
- `common/journal_entries/00_italian_unification.txt`.

## Diagnostics de pinning actualisés

La session 6A.6F confirme :

- anciennes erreurs globales : 389 avant, 388 après ;
- erreur visant `00_italian_unification.txt` : 1 avant, 0 après ;
- erreur visant la nouvelle propriété 1.13 : 0 ;
- fichiers encore concernés : 145.

Répartition attendue :

| Statut rapproché | Fichiers | Occurrences |
| --- | ---: | ---: |
| `INTENTIONAL_FORK_DIVERGENCE` | 104 | 242 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 19 | 104 |
| `PENDING_REVIEW` brut | 8 | 19 |
| `MERGED_STATIC_ONLY` brut | 10 | 19 |
| Hors inventaire | 4 | 4 |
| **Total** | **145** | **388** |

Regrouper par fichier, objet, propriété, occurrence, catégorie, protection,
présence hotfix et présence vanilla.

Séparer obligatoirement :

- tutoriels ;
- objectifs joueur ;
- prestige goods ;
- Russie protégée ;
- `sick_man` ;
- autres journal entries ;
- blocs hors inventaire.

## Observation debug italienne

La capture 6A.6F montre :

```text
En ou après 1836 (BUG_year_greater_or_equal missing perspective...)
```

Cette observation ne doit pas être promue automatiquement en correctif :

- la localisation française normale existe ;
- le préfixe `En ou après 1836` est traduit ;
- la capture affiche explicitement les informations développeur `Debug` ;
- aucun log ne contient l'erreur correspondante ;
- `year >= 1836` est une divergence 1776 protégée.

La classer comme diagnostic de tooltip debug documenté, sauf preuve nouvelle
trois voies démontrant un défaut fonctionnel hors debug.

## Comparaison trois voies obligatoire

Pour chaque candidat sérieux, documenter :

- chemin exact ;
- objet exact ;
- propriété ou bloc ;
- comportement du fork ;
- comportement de la source hotfix ;
- comportement vanilla ;
- erreur runtime éventuelle ;
- nombre exact de fichiers, objets et hunks ;
- dépendances ;
- collision ;
- localisation ;
- runtime humain ;
- rollback ;
- priorité P0, P1 ou inférieure.

Ne jamais remplacer un fichier complet.

Ne pas sélectionner un candidat lorsque source hotfix et vanilla divergent sans
justification claire.

## Pistes obligatoires

### Merchant Banking GEN/VEN

Revalider :

- `gen - genoa.txt` ;
- `ven - venetia.txt` ;
- `law_traditionalism` dans le fork ;
- `law_merchant_banking` dans la source ;
- loi, icône et localisations déjà présentes ;
- preuve du changelog 2.3 ;
- exclusion du nom spécifique des propriétaires terriens ;
- exclusion absolue du retrait de `law_merchant_navy`.

### Navigation Acts

Revalider :

- GBR, HBC, NBS, ONT et ORA ;
- absence actuelle de `law_mercantilism_navigation_acts` ;
- présence dans la source hotfix ;
- preuve du changelog ;
- autres écarts par fichier ;
- collision GBR/NAVY ;
- BIC absolument hors périmètre.

### Alignements 1.13 restants

Il reste 19 fichiers classés
`VANILLA_1_13_ALIGNMENT_REQUIRED`.

Ne créer aucun lot massif. Rechercher un hunk court, convergent, sans dette
adjacente ni protection. Revoir notamment les petits candidats déjà différés,
sans présumer leur sélection :

- `00_greek_nationalism.txt` ;
- `01_coup.txt` ;
- `04_imperialism_of_promise.txt` ;
- `05_great_eastern_crisis.txt`.

### Inconnus

Examiner un `UNKNOWN_REQUIRES_REVIEW` uniquement lorsqu'un log ou une
comparaison trois voies fournit une preuve précise.

## Protections absolues

Ne sélectionner ni modifier :

- DEI/VOC, Java et économie post-compagnie ;
- Balkan National Awakening ;
- Yugoslavia ;
- Risorgimento et `00_italian_unification.txt` ;
- NAVY, lois navales, formations et événements navals ;
- MARATH, SAT, KHP et Travancore ;
- Inde, BIC, Sepoy et Bombay ;
- ADMIN ;
- Japon, Russie, Autriche, Croatie, Slavonie et Suisse ;
- révolutions américaine et française ;
- lettres de Kew ;
- technologies et recherches technologiques ;
- localisations françaises générales ;
- agriculture, alimentation et industrie générale ;
- descripteurs, launcher, sauvegardes et `bject`.

Préserver dans BIC :

```txt
activate_law = law_type:law_frontier_colonization
```

Ne jamais restaurer `law_colonial_exploitation`.

## Top 3 obligatoire

Publier exactement :

| Rang | Phase candidate | Fichiers | Objets | Hunks | Priorité | Preuve | Collision | Runtime |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |

Expliquer pour chacun :

- comparaison trois voies ;
- preuve ;
- taille exacte ;
- dépendances ;
- collision ;
- raison de sélection ou report ;
- besoin de runtime humain.

Sélectionner exactement un candidat et publier :

`NEXT_EXECUTION_PHASE = <phase atomique sélectionnée>`

## Liste fermée des fichiers modifiables

Uniquement :

- `docs/reports/hotfix/_index/HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `docs/reports/hotfix/INDEX.md` ;
- `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun gameplay n'est modifiable.

## Rapport requis

Créer :

`docs/reports/hotfix/_index/HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

Inclure :

1. date, branche et HEAD ;
2. état Git initial/final ;
3. sources ;
4. inventaire actualisé ;
5. classification exclusive ;
6. 113 lignes directement exploitables ;
7. analyse des 388 erreurs ;
8. familles et protections ;
9. comparaisons trois voies ;
10. exactement trois candidats ;
11. exactement un candidat sélectionné ;
12. futur périmètre fermé ;
13. dépendances, collision et rollback ;
14. runtime humain futur ;
15. documents modifiés ;
16. décision de commit manuel.

## Prochain prompt autonome

Remplacer `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` par le prompt complet de la phase
atomique sélectionnée.

Si un runtime est nécessaire, imposer :

- aucun lancement par Codex ;
- tous les contrôles statiques avant le lancement ;
- une fiche condensée ;
- arrêt avec `RUNTIME_OPERATOR_ACTION_REQUIRED` ;
- attente du compte rendu humain ;
- analyse des logs seulement après fermeture.

Ne commencer pas la phase sélectionnée.

## Contrôles finaux

Vérifier :

- zéro gameplay modifié ;
- exactement trois candidats ;
- exactement un candidat sélectionné ;
- aucun fichier clos réintroduit ;
- catégories exclusives et sommes cohérentes ;
- prompt futur autonome ;
- `git diff --check` propre ;
- index Git vide ;
- seulement les six documents autorisés ;
- hashes protégés et stash intacts ;
- Victoria 3 et launcher fermés ;
- aucun lancement ou contrôle par Codex.

## Verdicts

- `HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = <phase atomique sélectionnée>`

Ne committe rien automatiquement et ne commence aucune autre phase.
