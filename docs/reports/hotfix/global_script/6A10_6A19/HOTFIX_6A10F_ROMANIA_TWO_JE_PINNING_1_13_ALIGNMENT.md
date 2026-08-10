# HOTFIX-6A.10F — Alignement du pinning de deux journal entries roumaines

Date : 29 juillet 2026

Phase : `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT`

Branche : `hotfix-dlc-audit`

HEAD initial : `e2eecfd380c584d50a5952d99e844e3ef25e2ff7`

HEAD final :
`e2eecfd380c584d50a5952d99e844e3ef25e2ff7`

## 1. État de la phase

Le correctif statique et le runtime humain sont validés. L'opérateur a joué la
Valachie jusqu'au 2 janvier 1776, a ouvert l'entrée potentielle `Unir les
principautés` et n'a constaté aucune clé brute ni anomalie visible.

Le gameplay est limité à deux substitutions d'API Victoria 3 1.13 dans un
fichier, deux objets et deux hunks. Aucun autre candidat ni aucune dette
adjacente n'a été commencé.

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| Racine | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` |
| Branche | `hotfix-dlc-audit` |
| HEAD | `e2eecfd Select Romania journal entry pinning alignment` |
| Rapport 6A.10 dans HEAD | présent |
| Verdicts d'entrée 6A.10 | quatre présents |
| Worktree suivi initial | propre |
| Index staged initial | vide |
| Non suivis initiaux | seulement `bject` et les sept fichiers de `docs/research/technology/` |
| `git diff --check` initial | propre |
| Stash protégé | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Processus Victoria 3, `dowser`, Paradox | aucun |

La phase 6A.10 était commitée manuellement avant le début de 6A.10F. Aucun
reset, restore, checkout de fichier, clean, merge, rebase, amend, commit
automatique, accès au contenu du stash ou lancement du jeu n'a été effectué.

## 3. Sources consultées

Ont été lus ou chargés intégralement :

- `HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- les versions fork, source hotfix et vanilla de `00_romania.txt` ;
- les localisations anglaises et françaises vanilla des deux journal entries ;
- les cinq nouveaux logs/rotations de 6A.9F.

## 4. Hashes trois voies et non-régressions

| Preuve | SHA-256 initial | Résultat statique |
| --- | --- | --- |
| Fork `common/journal_entries/00_romania.txt` | `D5925DEB54D4E0E4BB6E96DAF5106CAADBA35CC18E451D4898A7F1B7AA1AE078` | conforme avant patch |
| Source hotfix `00_romania.txt` | `74149D3A3B778732DE318D7FB522CE4255289B410F6184625BA9670E6CCCAB9A` | inchangée |
| Vanilla `00_romania.txt` | `9B5C9A9D06DAA420030BBC3B31581CD030356145FD31E1589E590AB9DF904A51` | inchangé |
| Fork `00_sick_man.txt` | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` | inchangé |
| Histoire TUR fork | `81ABC8DEA9DE93EC6A4DD417FD05FD6859F3122758D2B27E712B1880013F9CA9` | inchangée |
| Grande Crise orientale fork | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` | inchangée |
| BIC fork | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` | inchangé |

Source et vanilla convergent exactement sur
`should_be_pinned_by_default_uninvolved_or_context = yes` dans les deux
objets. Leurs autres différences globales n'ont autorisé aucun import.

## 5. Hashes protégés

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

Les huit hashes sont conformes avant le patch et après le runtime.

## 6. Snapshot initial

| Mesure | Valeur initiale |
| --- | ---: |
| Octets | 3 857 |
| UTF-8 BOM | oui |
| LF | 150 |
| CRLF | 0 |
| Saut final | présent |
| Accolades ouvrantes | 48 |
| Accolades fermantes | 48 |
| Ancienne propriété | 2 |
| Propriété moderne | 0 |
| Hash | `D5925DEB54D4E0E4BB6E96DAF5106CAADBA35CC18E451D4898A7F1B7AA1AE078` |

Le nouveau `debug.log` de 6A.9F contenait 378 diagnostics de pinning dans 142
fichiers, dont exactement deux dans `00_romania.txt`, aux lignes gameplay 76
et 149. Il ne contenait aucun rejet de la propriété moderne dans ce fichier.

## 7. Objets et substitutions

| Objet | Ligne initiale | Avant | Après |
| --- | ---: | --- | --- |
| `je_unite_the_principalities` | 76 | `should_be_pinned_by_default = yes` | `should_be_pinned_by_default_uninvolved_or_context = yes` |
| `je_all_for_one` | 149 | `should_be_pinned_by_default = yes` | `should_be_pinned_by_default_uninvolved_or_context = yes` |

Diff gameplay exact :

```diff
@@ -73,7 +73,7 @@
     weight = 1000
-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
 }

@@ -146,5 +146,5 @@
     weight = 10000
-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
 }
```

Le diff compte exactement un fichier gameplay, deux objets, deux hunks, deux
additions et deux suppressions.

## 8. Snapshot après patch

| Mesure | Attendu | Obtenu | Verdict |
| --- | ---: | ---: | --- |
| Octets | 3 901 | 3 901 | PASS |
| UTF-8 BOM | oui | oui | PASS |
| LF | 150 | 150 | PASS |
| CRLF | 0 | 0 | PASS |
| Saut final | présent | présent | PASS |
| Accolades ouvrantes | 48 | 48 | PASS |
| Accolades fermantes | 48 | 48 | PASS |
| Ancienne propriété | 0 | 0 | PASS |
| Propriété moderne | 2 | 2 | PASS |

Hash final obtenu :

`DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578`

Il est identique au hash attendu.

## 9. Exclusions et protections

Aucune ligne de `is_shown_in_lobby`, `is_shown_when_inactive`, géographie,
scope, helper, condition, complétion, échec, pulse, variable, progression,
scripted button, tooltip ou localisation n'a changé. Les histoires WAL, MOL et
ROM restent intactes.

Les localisations vanilla anglaises et françaises de
`je_unite_the_principalities`, de sa description, de ses conditions et de
`je_all_for_one` existent ; aucune localisation n'était nécessaire.

DEI/VOC, Java, économie post-compagnie, Balkan National Awakening, Yugoslavia,
Risorgimento, nationalisme grec, Grande Crise orientale, Sick Man, activation
Tanzimat, NAVY, MARATH, SAT, KHP, Travancore, Inde/BIC/Sepoy/Bombay, ADMIN,
Japon, Russie, Autriche/Croatie/Slavonie/Suisse, révolutions, lettres de Kew,
technologies, recherche, agriculture, alimentation, industrie, descripteurs,
launcher, sauvegardes et `bject` sont hors périmètre et intacts.

BIC conserve :

```txt
activate_law = law_type:law_frontier_colonization
```

et ne contient pas `law_colonial_exploitation`.

Merchant Banking, Navigation Acts, Coup, Imperialism of Promise et Tanzimat
n'ont pas été commencés.

## 10. Snapshot des logs avant runtime

| Log | Horodatage | Octets | SHA-256 |
| --- | --- | ---: | --- |
| `debug.log` | `2026-07-29 18:55:35.567 +02:00` | 472 823 | `78068296741B912AFC46A4E763ED393F35F7D00967E4F17EB98075BC8EB177F5` |
| `debug.1.log` | `2026-07-29 18:50:40.867 +02:00` | 158 358 | `456557E5AAD303159180496C024286C5966BCE5C3FB46401A86BB0746CA84559` |
| `error.log` | `2026-07-29 18:55:28.629 +02:00` | 236 501 | `B94DC10E06A68649CC91F7828CD4018A53A8DF31DE3AE0D6E9C09AB853EBB5C1` |
| `game.log` | `2026-07-29 18:55:28.629 +02:00` | 144 371 | `7BF100E41F31F7391CFA3907AE7D63B3C2E79AF10EC7B3FD65D84A7FA6042AA4` |
| `system.log` | `2026-07-29 18:47:16.559 +02:00` | 1 100 | `E67BB0321A458DA5D6A4249416EEF744F148FCC6DF33945D4382181E58DFBECD` |

Ces logs sont des preuves antérieures. Aucun nouveau log n'a été analysé avant
la confirmation humaine explicite que le jeu et le launcher étaient fermés.

## 11. Validations statiques

| Contrôle | Verdict |
| --- | --- |
| Hash gameplay final | PASS |
| Snapshot structurel | PASS |
| Ancienne propriété 2 → 0 | PASS |
| Propriété moderne 0 → 2 | PASS |
| Un fichier gameplay | PASS |
| Deux objets | PASS |
| Deux hunks | PASS |
| Deux additions / deux suppressions | PASS |
| Lignes adjacentes inchangées | PASS |
| Source hotfix / vanilla inchangés | PASS |
| BIC intact | PASS |
| Stash NAVY-3C-3 intact | PASS |
| `git diff --check` | PASS |
| Index staged vide | PASS |
| Processus jeu/launcher | aucun |

## 12. Rollback exact

Dans les deux objets seulement :

```diff
-    should_be_pinned_by_default_uninvolved_or_context = yes
+    should_be_pinned_by_default = yes
```

Le rollback doit restaurer exactement le hash
`D5925DEB54D4E0E4BB6E96DAF5106CAADBA35CC18E451D4898A7F1B7AA1AE078`
et le snapshot initial. Aucune commande Git destructive n'est autorisée.

## 13. Compte rendu runtime humain

| Point | Résultat |
| --- | --- |
| Pays | Valachie (`WAL`) |
| Date initiale | 1er janvier 1776 |
| Date finale | 2 janvier 1776 |
| Écran de jeu atteint | oui |
| Entrée potentielle | `Unir les principautés`, visible |
| Titre | lisible |
| Description et conditions | lisibles |
| Clé brute | aucune |
| Anomalie de pinning | aucune |
| Anomalie de géographie, visibilité ou progression | aucune détectée |
| Capture | fournie par l'opérateur |
| Jeu et launcher fermés | confirmation humaine explicite |

La capture montre le journal de la Valachie, l'onglet `Potentiel`, le titre
`Unir les principautés` et ses conditions françaises lisibles. Elle ne montre
aucune clé brute. `je_all_for_one` n'a pas été activée artificiellement ; son
chargement est validé par le parser, conformément au protocole.

## 14. Nouveaux logs et rotations

| Log | Horodatage | Octets | SHA-256 | Usage |
| --- | --- | ---: | --- | --- |
| `debug.2.log` | `2026-07-29 20:54:01.554 +02:00` | 51 456 | `38B2B29FAD0922C6192B27CB69BC202F0C431F1DC9FDF5427C3835EBFDD75C35` | démarrage et montage |
| `debug.1.log` | `2026-07-29 21:00:37.020 +02:00` | 524 256 | `A75AD954D9AA33D27B11BFDBB75A804F319555610F75266604E0565C4D5004E8` | baseline parser du runtime |
| `debug.log` | `2026-07-29 21:02:59.675 +02:00` | 54 942 | `72E998A9E079984DB6D93B24F1CD4E6B13F2755FF2640E81BA660A01DE417899` | fin de session |
| `error.log` | `2026-07-29 21:02:49.351 +02:00` | 287 509 | `DF3960F4A72B632CDF767797706C5AA13F2546950A9FBAE921711C848D0C61EB` | erreurs courantes |
| `game.log` | `2026-07-29 21:02:49.351 +02:00` | 388 704 | `AFCAAA6520CF21F11934E1E08817101E689B092CE453AAEACCF587923A6CE868` | session courante |
| `system.log` | `2026-07-29 20:54:11.327 +02:00` | 1 100 | `E320CDB3AA176CFF36C3491C699013053E760D62AA70D8578DE84357DF0C6943` | système courant |

`debug.3.log` conserve la baseline antérieure 6A.9F au hash
`78068296741B912AFC46A4E763ED393F35F7D00967E4F17EB98075BC8EB177F5`.
Elle n'est pas mélangée aux nouveaux résultats.

Preuves de montage dans `debug.2.log` :

- ligne 68 : chemin exact du fork
  `1776_Age_of_Revolutions_fork` ;
- ligne 80 : montage de `game/dlc/dlc014_ip3` ;
- ligne 87 : montage du répertoire exact du fork.

La progression au 2 janvier 1776 est attestée par le compte rendu humain. Les
logs ne produisent pas de ligne de calendrier exploitable pour cette session ;
ils prouvent indépendamment le chargement, le montage et l'état du parser.

## 15. Comparaison parser avant/après

| Mesure | Avant, `debug.3.log` | Après, `debug.1.log` | Verdict |
| --- | ---: | ---: | --- |
| Diagnostics `Unexpected token: should_be_pinned_by_default,` | 378 | 376 | conforme |
| Fichiers uniques | 142 | 141 | conforme |
| Diagnostics `00_romania.txt` | 2 | 0 | PASS |
| Rejets de la propriété moderne dans `00_romania.txt` | 0 | 0 | PASS |

Les diagnostics Romania aux anciennes lignes 76 et 149 sont absents. Le
résultat exact est donc :

`ROMANIA_TWO_JE_PINNING_PARSER_ERRORS_2_TO_0`

Les diagnostics Tanzimat restent séparés : `.5`, `.10` et `.9` sont toujours
signalés dans `00_sick_man.txt`, et `.10` reste aussi référencé par
`00_code_on_actions.txt`. Ils sont inchangés et hors périmètre. Les autres
erreurs moteur et namespaces manquants sont également hors périmètre ; aucune
nouvelle correction n'a été commencée.

## 16. Fichiers modifiés

Fichiers de phase autorisés :

1. `common/journal_entries/00_romania.txt` ;
2. le présent rapport ;
3. `docs/reports/hotfix/INDEX.md` ;
4. `HOTFIX_REPORT_INDEX.csv` ;
5. `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
6. `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
7. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Les non-suivis protégés préexistants `bject` et
`docs/research/technology/` restent inchangés.

## 17. Fiche runtime humaine exécutée

L'opérateur humain a suivi la fiche suivante :

1. lancer le launcher Paradox ;
2. confirmer le montage du fork et de `dlc014_ip3` ;
3. lancer Victoria 3 ;
4. commencer une partie neuve au setup 1776 avec la Valachie (`WAL`) ;
5. confirmer que l'écran de jeu est atteint ;
6. ouvrir le journal et rechercher l'entrée potentielle
   `Unir les principautés` ;
7. vérifier titre, description et conditions lisibles, sans clé brute ni
   anomalie de pinning, géographie, visibilité ou progression ;
8. noter la date initiale ;
9. avancer au 2 janvier 1776 et noter la date finale ;
10. prendre une capture si possible ;
11. fermer normalement Victoria 3 puis le launcher ;
12. confirmer explicitement que les deux sont fermés.

Ne pas utiliser la console et ne pas tenter d'activer artificiellement
`je_all_for_one`.

Compte rendu demandé :

- pays joué ;
- dates initiale et finale ;
- écran de jeu atteint ;
- entrée visible ;
- titre, description et conditions lisibles ;
- clé brute éventuelle ;
- anomalie de pinning, géographie, visibilité ou progression ;
- capture éventuelle ;
- confirmation explicite de fermeture du jeu et du launcher.

## 18. Contrôles finaux

Les contrôles finaux confirment :

- hash gameplay final et snapshot conformes ;
- un fichier gameplay, deux objets, deux hunks et un diff `2/2` ;
- deux diagnostics ciblés ramenés à zéro ;
- aucune dette adjacente importée ;
- source hotfix, vanilla, BIC, stash NAVY-3C-3 et huit hashes protégés
  intacts ;
- CSV valides ;
- `git diff --check` propre ;
- index staged vide ;
- aucun processus Victoria 3, `dowser` ou Paradox ;
- runtime fondé sur le compte rendu humain et la capture ;
- aucune interaction Codex avec le jeu ;
- aucun commit automatique ;
- aucune phase suivante commencée.

## 19. État Git final

```text
 M common/journal_entries/00_romania.txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A10_6A19/HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md
?? docs/research/technology/
```

L'index staged est vide. Aucun commit automatique n'est créé. HEAD reste
`e2eecfd380c584d50a5952d99e844e3ef25e2ff7`.

La décision de commit reste manuelle.

## 20. Verdicts

`HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_STATIC_PASS`

`ROMANIA_TWO_JE_PINNING_TWO_HUNK_1_13_ALIGNMENT_COMPLETE`

`HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_RUNTIME_PASS`

`ROMANIA_TWO_JE_PINNING_PARSER_ERRORS_2_TO_0`

`ROMANIA_1776_VISIBILITY_GEOGRAPHY_AND_PROGRESSION_UNCHANGED`

`HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
