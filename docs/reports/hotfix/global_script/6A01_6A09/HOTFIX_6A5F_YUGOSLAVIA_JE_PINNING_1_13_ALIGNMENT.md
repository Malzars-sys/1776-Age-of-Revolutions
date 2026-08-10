# HOTFIX-6A.5F — Alignement Victoria 3 1.13 du pinning de `je_yugoslavia`

Date : 29 juillet 2026

Phase : `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT`

Branche : `hotfix-dlc-audit`

HEAD initial :
`a74426f Select Yugoslavia journal entry 1.13 alignment`

## 1. Verdict final

`HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_STATIC_PASS`

`HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_RUNTIME_PASS`

`HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_COMPLETE`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

Le correctif statique a été testé exclusivement par l’opérateur humain. Le
runtime monté confirme la disparition de l’erreur ciblée et l’interface
serbe ne présente aucune clé brute ou anomalie visible.

## 2. État Git initial

Le préflight a confirmé :

- racine exacte du fork ;
- branche `hotfix-dlc-audit` ;
- rapport 6A.5 présent dans HEAD ;
- aucun fichier suivi modifié ;
- aucun fichier staged ;
- seuls `bject` et les sept fichiers de
  `docs/research/technology/` non suivis ;
- stash exact intact :
  `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` ;
- zéro processus Victoria 3 ;
- zéro processus launcher Paradox.

Aucun reset, restore, checkout, clean, merge, rebase, amend, commit
automatique ou opération sur le stash n’a été effectué.

## 3. Sources consultées

Sources lues avant modification :

- `HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- versions fork, source hotfix et vanilla 1.13 de
  `common/journal_entries/05_creation_of_yugoslavia.txt` ;
- `error.log`, `game.log`, `debug.log` et leurs rotations déjà existantes.

Victoria 3 et le launcher n’ont pas été lancés pour produire de nouveaux
journaux.

## 4. Diagnostic runtime historique ciblé

Dans les journaux existants de la dernière session :

- références directes à
  `common/journal_entries/05_creation_of_yugoslavia.txt` : **1** ;
- références directes à `je_yugoslavia` : **0** ;
- messages contenant
  `Unexpected token: should_be_pinned_by_default` : **390** ;
- les 390 messages se trouvent dans `debug.log` ;
- le diagnostic propre au fichier cible est à la ligne 2364 de `debug.log` et
  désigne la ligne 144 du script.

Diagnostic exact :

```text
[00:24:52][pdx_persistent_reader.cpp:268]: Error: "Unexpected token: should_be_pinned_by_default, near line: 144" in file: "common/journal_entries/05_creation_of_yugoslavia.txt" near line: 144
```

Une seule des 390 erreurs globales vise ce fichier. Les 389 autres restent hors
périmètre.

## 5. Comparaison fork, hotfix et vanilla

Le fork employait :

```txt
should_be_pinned_by_default = yes
```

La source hotfix et le vanilla Victoria 3 1.13 emploient chacun exactement une
fois :

```txt
should_be_pinned_by_default_uninvolved_or_context = yes
```

La convergence de l’API est donc directe. La source hotfix contient aussi :

```txt
is_in_geographic_region = geographic_region_balkans
```

Cette condition n’existe pas dans le fichier vanilla correspondant. Elle est
hors périmètre et n’a pas été importée.

## 6. Hunk gameplay appliqué

Fichier unique :

`common/journal_entries/05_creation_of_yugoslavia.txt`

Objet unique :

`je_yugoslavia`

Hunk unique :

```diff
-	should_be_pinned_by_default = yes
+	should_be_pinned_by_default_uninvolved_or_context = yes
```

Aucune condition, durée, technologie, loi, pays, géographie, progression,
complétion, effet ou localisation n’a changé.

## 7. Encodage avant et après

Avant modification :

- taille : 3 010 octets ;
- SHA-256 :
  `C9035D2832445F701D69B3D951C2EEBF6AE9EC13DA8AC2C4F8F641E87100EC51` ;
- UTF-8 avec BOM ;
- 145 fins de ligne LF ;
- zéro CRLF ;
- saut de ligne final présent.

Après modification :

- taille : 3 032 octets ;
- SHA-256 :
  `4371E202B494B2F7FA1FCF06BDFE1E0562895480E160AD37E551E3587606E46C` ;
- UTF-8 avec BOM ;
- 145 fins de ligne LF ;
- zéro CRLF ;
- saut de ligne final présent.

La différence de taille correspond uniquement au nom de propriété plus long.

## 8. Validations statiques

| Contrôle | Résultat |
|---|---:|
| Définitions actives de `je_yugoslavia` dans le mod | 1 |
| Profondeur finale des accolades | 0 |
| Profondeur minimale des accolades | 0 |
| Ancien champ exact dans l’objet | 0 |
| Nouveau champ exact avec `yes` dans l’objet | 1 |
| Nouveau champ exact dans la source hotfix | 1 |
| Nouveau champ exact dans le vanilla 1.13 | 1 |
| Condition `geographic_region_balkans` dans le fichier fork | 0 |
| Condition `geographic_region_balkans` ajoutée au diff | 0 |
| Lignes ajoutées/supprimées dans le diff gameplay | 1 / 1 |
| Autre fichier gameplay modifié | 0 |
| BOM UTF-8, LF et saut final | conservés |
| `git diff --check` | PASS |
| Index Git | vide |
| Stash NAVY-3C-3 | intact |
| Victoria 3 et launcher | fermés |

## 9. Fichiers autorisés de la phase

Gameplay :

- `common/journal_entries/05_creation_of_yugoslavia.txt`.

Documentation :

- `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md` ;
- `docs/reports/hotfix/INDEX.md` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun autre fichier n’est autorisé.

## 10. Protections confirmées

Sont restés intacts : DEI/VOC, Java, économie post-compagnie, Balkan National
Awakening, NAVY, lois et formations navales, MARATH/SAT/KHP, Travancore,
Inde/BIC/Sepoy/Bombay, ADMIN, Japon, Russie, Autriche/Croatie/Suisse,
Révolutions américaine et française, lettres de Kew, technologies,
localisations françaises générales, agriculture, alimentation, industrie,
descripteurs, launcher et sauvegardes.

`activate_law = law_type:law_frontier_colonization` reste préservé pour BIC.
`law_colonial_exploitation` n’a pas été restaurée.

Les empreintes de `bject` et des sept recherches technologiques ont été
comparées avant le hunk et après toutes les mises à jour documentaires :
zéro différence.

## 11. Fiche de test pour l’opérateur humain

### Lancement unique

1. Lancer Victoria 3 depuis le launcher habituel avec le fork actif.
2. Démarrer une partie neuve en 1776.
3. Utiliser un pays balkanique pertinent.
4. La Valachie peut être utilisée si l’entrée apparaît dans les entrées
   potentielles.
5. Ouvrir `Journal > Potentiel`.
6. Rechercher `Création de la Yougoslavie`.
7. Si elle est visible, vérifier :
   - aucune clé de localisation brute ;
   - titre et description lisibles ;
   - conditions lisibles ;
   - aucune anomalie visible d’épinglage ;
   - aucun effet inattendu.
8. Laisser passer au moins un jour en jeu.
9. Noter la date atteinte.
10. Fermer normalement Victoria 3.
11. Fermer le launcher Paradox.
12. Transmettre :
   - pays choisi ;
   - entrée visible ou inaccessible ;
   - résultat des contrôles visuels ;
   - date atteinte ;
   - capture éventuelle.

Aucune commande console n’est requise ni autorisée. Si l’entrée est
inaccessible, le signaler simplement sans second lancement automatique et sans
élargir le correctif.

## 12. Résultat communiqué par l’opérateur

La première tentative a utilisé la Valachie. Elle ne pouvait pas former la
Yougoslavie, car ses cultures principales ne satisfaisaient pas les
conditions. Ce résultat est un contrôle négatif cohérent et non une
régression.

L’opérateur a ensuite libéré la Serbie comme sujet ottoman et l’a jouée. Avec
la culture serbe principale, l’interface « Formation de nation » rend la
Yougoslavie disponible et affiche :

- les cultures serbe, croate, slovène, bosniaque et bulgare ;
- les États requis et contrôlés ;
- les boutons d’unification ;
- aucune clé de localisation brute ;
- aucun texte illisible ;
- aucune anomalie visible d’épinglage ;
- aucun effet inattendu.

Les captures fournies montrent la Valachie le 1er janvier puis la Serbie le
24 janvier. L’opérateur signale une fin de session le 25 janvier 1776, puis la
fermeture du jeu. Les processus Victoria 3 et launcher Paradox sont tous deux
nuls lors de la reprise Codex.

## 13. Preuve du montage et de la progression

La session produit 16 fichiers courants ou rotations après 10:00 :

- six `error*.log` ;
- six `game*.log` ;
- trois `debug*.log` ;
- `dedicated_server.log`.

`debug.2.log` prouve :

- ligne 68 : le mod
  `1776 - Age of Revolutions, Total Conversion Mod` associé au chemin exact
  du fork ;
- ligne 87 : `Mounted Data` sur
  `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork` ;
- ligne 80 : montage de
  `C:/Games/Victoria 3 The Great Wave/game/dlc/dlc014_ip3`.

`dedicated_server.log` enregistre une progression de `1776.1.1.6` à
`1776.1.25`. La partie a donc progressé de plus que le minimum d’un jour.

Le diagnostic de version du descripteur du mod, encore déclaré `1.12.5` face
au jeu `1.13.0`, est hors périmètre. Il n’empêche pas le montage positif du
fork.

## 14. Analyse des journaux après correction

Comparaison entre la session précédente conservée dans `debug.3.log` et les
16 journaux de la nouvelle session :

| Diagnostic | Avant | Après |
|---|---:|---:|
| `Unexpected token: should_be_pinned_by_default,` | 390 | 389 |
| Références à `05_creation_of_yugoslavia.txt` | 1 | 0 |
| Références à `je_yugoslavia` | 0 | 0 |
| Erreurs sur `should_be_pinned_by_default_uninvolved_or_context` | 0 | 0 |

La baisse de 390 à 389 correspond exactement à la disparition de l’unique
occurrence visant le fichier corrigé. Les 389 diagnostics restants sont tous
attribués à d’autres fichiers.

Principales familles hors périmètre :

- `00_tutorial.txt` : 52 ;
- `00_player_objectives_great_game.txt` : 17 ;
- `05_prestige_goods.txt` : 16 ;
- `03_russia.txt` : 12, bloc protégé ;
- `00_player_objectives_hegemon.txt` : 11 ;
- `00_player_objectives_economic_dominance.txt` : 10 ;
- `00_sick_man.txt` : 8.

Aucun de ces diagnostics n’est absorbé dans 6A.5F.

## 15. Rollback exact

En cas de régression attribuable au hunk, inverser uniquement :

```diff
-	should_be_pinned_by_default_uninvolved_or_context = yes
+	should_be_pinned_by_default = yes
```

Ne jamais restaurer le fichier complet. Ce rollback réintroduirait l’API
obsolète et imposerait un verdict d’échec.

## 16. Décision

La preuve minimale et le contrôle visuel sont réunis. 6A.5F est close.

La prochaine phase est une nouvelle sélection documentaire :

`HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION`

Elle ne doit commencer ni Merchant Banking, ni Navigation Acts, ni un autre
correctif avant d’avoir sélectionné exactement un sous-bloc.

Ne rien committer automatiquement.

## 17. État Git final

Le diff est limité aux sept fichiers autorisés. `git status --short` :

```text
 M common/journal_entries/05_creation_of_yugoslavia.txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/global_script/6A01_6A09/HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md
?? docs/research/technology/
```

- fichier gameplay modifié : un ;
- autres fichiers gameplay modifiés : zéro ;
- fichiers staged : zéro ;
- commit créé : zéro ;
- fichiers autorisés modifiés ou créés : sept ;
- fichiers autorisés inattendus : zéro ;
- empreintes protégées divergentes : zéro ;
- stash NAVY-3C-3 : intact ;
- processus Victoria 3 : zéro ;
- processus launcher Paradox : zéro.
