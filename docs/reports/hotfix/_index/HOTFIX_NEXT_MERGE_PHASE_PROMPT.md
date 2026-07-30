# Prompt autonome — HOTFIX-6A.13F Merchant Banking GEN/VEN

Nous poursuivons le portage du mod Victoria 3 :

`1776_Age_of_Revolutions_fork`

# Phase HOTFIX-6A.13F — Loi initiale Merchant Banking de GEN et VEN

## Modèle recommandé

GPT-5.6 Thinking avec raisonnement élevé.

## Nature et objectif unique

Appliquer exactement deux substitutions de loi économique initiale :

```txt
law_traditionalism -> law_merchant_banking
```

dans `c:GEN` et `c:VEN`, effectuer tous les contrôles statiques, créer le
rapport, préparer un runtime humain unique puis s'arrêter sur
`RUNTIME_OPERATOR_ACTION_REQUIRED`.

Codex ne lance ni ne pilote Victoria 3 ou le launcher, n'utilise pas la console,
n'ouvre aucune sauvegarde, n'étend pas le périmètre, ne crée aucun commit
automatique et ne commence aucune phase suivante.

## Chemins

FORK :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`

SOURCE HOTFIX, strictement en lecture seule :

`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source`

VANILLA 1.13, strictement en lecture seule :

`C:\Games\Victoria 3 The Great Wave\game`

## Verdicts d'entrée

Exiger dans `HEAD` :

- `HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`;
- `NO_GAMEPLAY_CHANGED`;
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`;
- `NEXT_EXECUTION_PHASE = HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW`.

Rapport canonique :

`docs/reports/hotfix/_index/HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md`

6A.13 doit être commitée manuellement. Ne jamais commencer depuis son worktree
documentaire non commité.

## Préflight Git

Exécuter :

```powershell
git rev-parse --show-toplevel
git branch --show-current
git status --short
git log -5 --oneline --decorate
git diff --check
git diff --cached --name-only
git stash list
git show HEAD:docs/reports/hotfix/_index/HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
```

Exiger la racine exacte, branche `hotfix-dlc-audit`, rapport et verdicts dans
`HEAD`, fichiers suivis propres, index vide, uniquement `bject` et les sept
recherches technologiques non suivis, stash exact
`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`, et
zéro processus Victoria 3, `dowser` ou Paradox.

Arrêts : `BLOCKED_WRONG_BRANCH`, `BLOCKED_6A13_NOT_COMMITTED`,
`BLOCKED_DIRTY_TREE`, `BLOCKED_STAGED_FILES`,
`BLOCKED_UNEXPECTED_UNTRACKED_FILES`, `BLOCKED_PROTECTED_STASH_MISSING`,
`BLOCKED_GAME_PROCESS_RUNNING`.

Interdictions : aucun reset, restore, checkout de fichier, clean, merge,
rebase, amend, commit automatique, stash apply/pop/drop ou inspection du
contenu du stash.

## Hashes de référence

| Preuve | SHA-256 |
| --- | --- |
| GEN fork avant | `B4EC2FB8C9916425FBFFBAA1CEF7FEDFB63C2E0510352A4744E088748AFD80EF` |
| VEN fork avant | `33503E48A69A431AD10ABC2AD71AF9D2147CDA6F19C0CD6C0C04434C1E5425B1` |
| GEN source | `05A10969F0C7C378920E3224F83C1BC445486143F130874AAA19DE9592E98EAF` |
| VEN source | `8DDDA736260B18E2412DA1AD9516336938E19BA7266FD79992BD31E84013E5BA` |
| GEN fork attendu après | `7FC780AB8A8793E1DD1B3E6A32022807CED720FB1BE3F3D63D9EC6FDE9F43327` |
| VEN fork attendu après | `51A65341A2E3947A3D7D71BC3E3B1F31DA5CCD9D000D200C75BFB9570010B6DB` |

Vanilla ne possède ni le fichier GEN ni le fichier VEN. Vérifier aussi les
hashes protégés Portugal final, Romania, Sick Man, Grande Crise orientale,
BIC, `bject` et les sept recherches technologiques consignés dans 6A.13.
Tout écart impose `BLOCKED_THREE_WAY_EVIDENCE_CHANGED`.

## Sources obligatoires

Lire intégralement :

- le rapport 6A.13;
- les rapports 6A.12F et 6A.12;
- la roadmap et les deux CSV de navigation;
- les versions fork et source de GEN et VEN;
- le changelog complet fork et source;
- `common/laws/00_inject_laws.txt`;
- `localization/english/hotfix_laws_l_english.yml`;
- `localization/french/hotfix_laws_l_french.yml`;
- l'icône `gfx/interface/icons/law_icons/merchant_banks.dds`;
- les logs et rotations de référence 6A.12F.

Ne lancer aucun runtime pour créer une preuve supplémentaire.

## Comparaison trois voies

Confirmer :

- fork GEN/VEN : `law_traditionalism`;
- source GEN/VEN : `law_merchant_banking`;
- vanilla : fichiers absents;
- changelog source : Merchant Banking pour les républiques maritimes;
- loi déjà définie et visible uniquement pour GEN/VEN;
- icône et localisations anglaise/française déjà présentes;
- `law_merchant_navy` présente dans les deux fichiers fork;
- source retire cette loi navale et ajoute un nom de propriétaires terriens,
  différences adjacentes expressément exclues.

## Fichiers et objets modifiables avant runtime

1. `common/history/countries/gen - genoa.txt`, objet `c:GEN`;
2. `common/history/countries/ven - venetia.txt`, objet `c:VEN`;
3. `docs/reports/hotfix/_index/HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW.md`.

Après runtime et fermeture explicite du jeu/launcher, seuls les quatre
documents de navigation habituels peuvent aussi être modifiés :

4. `docs/reports/hotfix/INDEX.md`;
5. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv`;
6. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv`;
7. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md`.

Ne pas modifier `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## Hunks exacts

Dans chacun des deux objets :

```diff
-		activate_law = law_type:law_traditionalism
+		activate_law = law_type:law_merchant_banking
```

Diff gameplay attendu : deux fichiers, deux objets, deux hunks, deux
additions et deux suppressions.

Préserver BOM UTF-8, LF, saut final, indentation et toutes les lignes
adjacentes.

## Exclusions et protections

Préserver absolument :

- `activate_law = law_type:law_merchant_navy` dans GEN et VEN;
- toutes les autres lois initiales;
- technologies, institutions, modificateurs et tarifs;
- l'absence du bloc `ideo_merchant_landowners`;
- fichiers de loi, icône et localisations;
- tous les autres pays.

Ne toucher à aucun élément NAVY, ADMIN, MARATH, Inde/BIC, Portugal, Romania,
Sick Man, Balkans, Russie, Japon, Autriche, technologies, descripteurs,
launcher, sauvegardes ou `bject`.

BIC conserve `law_frontier_colonization`; ne jamais restaurer
`law_colonial_exploitation`.

## Validations statiques

Exiger :

1. deux hashes cibles exacts;
2. zéro `law_traditionalism` dans les deux fichiers;
3. une `law_merchant_banking` dans chaque objet;
4. une `law_merchant_navy` inchangée dans chaque objet;
5. deux fichiers, deux objets, deux hunks, `2/2`;
6. aucune ligne adjacente modifiée;
7. autres lois et effets inchangés;
8. BOM, LF, saut final et accolades préservés;
9. source, vanilla et protections inchangés;
10. `git diff --check` propre;
11. index staged vide;
12. stash exact;
13. zéro processus du jeu/launcher.

Exécuter les commandes Git finales usuelles, dont le diff ciblé des deux
fichiers.

Si un hash cible échoue, annuler uniquement les deux substitutions et exiger
les hashes initiaux. Si le rollback ciblé échoue :
`BLOCKED_ROLLBACK_MISMATCH`.

## Rollback exact

Dans GEN et VEN seulement :

```txt
law_merchant_banking -> law_traditionalism
```

Le rollback doit restaurer exactement les hashes initiaux. Aucune commande Git
destructive.

## Livrable statique

Créer le rapport 6A.13F avec préflight, hashes, sources, snapshots, comparaison,
hunks, diff, exclusions, validations, rollback, fichiers, fiche runtime et
verdicts statiques.

Après PASS statique publier :

- `HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW_STATIC_PASS`;
- `GEN_VEN_MERCHANT_BANKING_TWO_FILE_TWO_HUNK_ALIGNMENT_COMPLETE`;
- `GEN_VEN_MERCHANT_NAVY_AND_OTHER_STARTING_LAWS_UNCHANGED`;
- `RUNTIME_OPERATOR_ACTION_REQUIRED`.

Puis s'arrêter. Ne pas lancer le jeu.

## Fiche runtime humaine unique

Un seul lancement du launcher et du jeu, avec fork et `dlc014_ip3` montés :

1. nouvelle partie GEN au 1er janvier 1776;
2. vérifier dans Politique/Législation que Banque marchande est la loi
   économique active, Marine marchande la loi navale active, et qu'aucune clé
   brute ou anomalie n'est visible;
3. avancer au 2 janvier 1776;
4. revenir normalement au menu principal;
5. nouvelle partie VEN au 1er janvier 1776;
6. effectuer les mêmes vérifications et avancer au 2 janvier;
7. prendre des captures si possible;
8. fermer normalement Victoria 3 puis le launcher;
9. confirmer explicitement leur fermeture.

Ne pas utiliser la console. L'opérateur transmet pays, dates, lois observées,
clés brutes/anomalies, captures et confirmation de fermeture.

Codex n'analyse les nouveaux logs qu'après cette confirmation. Exiger montage
du fork et de `dlc014_ip3`, absence de diagnostics ciblés et compte rendu
humain. Aucun PASS runtime sans compte rendu.

## Verdicts finaux attendus

- `HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW_RUNTIME_PASS`;
- `GEN_VEN_MERCHANT_BANKING_1776_START_VALIDATED`;
- `GEN_VEN_MERCHANT_NAVY_PRESERVED`;
- `HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW_COMPLETE`;
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`.

Finaliser le rapport et uniquement les quatre documents de navigation
autorisés. Confirmer exactement sept fichiers de phase après runtime, aucun
commit automatique et aucune phase suivante commencée.
