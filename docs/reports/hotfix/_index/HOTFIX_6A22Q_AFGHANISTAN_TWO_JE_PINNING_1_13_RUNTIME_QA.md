# HOTFIX-6A.22Q — QA runtime des deux pinning Afghanistan sous Victoria 3 1.13

Date : 5 août 2026
Branche : hotfix-dlc-audit
Commit d’entrée : 07c7a038b2c4d458e888435d11f95c644c7fb3d6
Message : Align two Afghanistan journal entry pinning properties for 1.13

## 1. Résultat

La QA runtime humaine ciblée passe. Une seule ouverture de Victoria 3 a monté
le fork exact, chargé le moteur `release/1.13.0` et créé une partie neuve 1776
avec le Vietnam. La simulation a atteint le 5 janvier 1776, sans crash, clé
brute ou anomalie observée.

Les deux diagnostics historiques `should_be_pinned_by_default` visant
`common/journal_entries/03_afghanistan.txt`, lignes script 2 et 1826, passent
de 2 à 0 dans la génération fraîche. Les 17 échecs `PostValidate` de
`has_interest_marker_in_region` visant ce fichier sont antérieurs au correctif :
ils existaient aux mêmes lignes dans la baseline et restent strictement
identiques. La comparaison normalisée ne trouve donc aucune nouvelle erreur
attribuable au fichier.

Les deux journal entries afghanes n’ont pas été forcées et ne sont pas apparues
naturellement. Le comportement visuel du pinning n’est pas revendiqué ; seule
la compatibilité parser/runtime des deux substitutions est validée.

## 2. Préflight et processus

| Contrôle | Résultat |
| --- | --- |
| racine Git | dépôt attendu |
| branche | `hotfix-dlc-audit` |
| HEAD | `07c7a038b2c4d458e888435d11f95c644c7fb3d6` |
| message HEAD | `Align two Afghanistan journal entry pinning properties for 1.13` |
| rapport 6A.22F dans HEAD | présent avec tous les verdicts requis |
| arbre suivi avant runtime | propre |
| index Git | vide |
| `git diff --check` | propre |
| processus Victoria 3 / Dowser / launcher avant lancement | aucun |
| stash NAVY-3C-3 | `518df704fa14599c0f254fae13859210663dd976`, intact |
| non-suivis | uniquement les huit éléments protégés connus |

Les non-suivis protégés n’ont pas été ouverts, modifiés, déplacés ou indexés.

## 3. Intégrité gameplay avant et après

| Fichier | Avant | Après | Résultat |
| --- | --- | --- | --- |
| `common/journal_entries/03_afghanistan.txt` | `C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13` | `C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13` | identique |
| `common/journal_entries/00_poland.txt` | `A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A` | `A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A` | identique |

Après runtime, le fichier Afghanistan conserve 36 813 octets, un BOM UTF-8,
1 877 fins LF, zéro CRLF, zéro ancienne propriété et deux propriétés
`should_be_pinned_by_default_uninvolved_or_context`. Son identité complète
étant inchangée, tous les hunks Great Game, géographiques et fonctionnels le
sont également.

## 4. Manifeste avant lancement

Le manifeste complet de 60 fichiers `.log` a été capturé hors dépôt dans
`%TEMP%\HOTFIX_6A22Q_LOGS_BEFORE.json` à
`2026-08-05T16:55:59.8607514Z`. Son SHA-256 est
`BC3EE103EDCAB06C689699666C6386A3668DAC71444B21240B33613535D367C3`.
Chaque ligne contient le nom, le chemin complet, la taille, l’horodatage UTC et
le SHA-256.

| Log courant | Octets | Horodatage local | SHA-256 avant |
| --- | ---: | --- | --- |
| `code_revisions.log` | 1 133 | 2026-08-05 01:14:22 | `AB87218EB7382085A96504D6205DB5D6A1BC34561FB99CEC98C5BD078D0747F7` |
| `debug.1.log` | 216 883 | 2026-08-05 01:17:54 | `109EBCACE21F5663AD917C7FA59DBDD61BB225BA9C9681AC25DE827A637B6CC1` |
| `debug.log` | 401 820 | 2026-08-05 01:25:46 | `FFEFFAF26F69C1A0E09F6EB4F1C9FD1723FBA9DF793967F26CF26159725BD4D8` |
| `dedicated_server.log` | 1 721 | 2026-08-05 01:24:33 | `207BA07990A4A39ED83B23386C92348B9C585D1C7E4AABD489FD5CDE9815D546` |
| `error.log` | 450 343 | 2026-08-05 01:25:39 | `C7FF964815F62B1E06190B6201F28B98B53006D967E1D654B2888A4AAB34CC41` |
| `game.log` | 374 488 | 2026-08-05 01:25:39 | `15E8996B4F15DB9A35F40462CC6F69FC9DEEE6E723E942EC7C2B285B0CB9C412` |
| `system.log` | 1 100 | 2026-08-05 01:14:54 | `89CFC4FBF822AE41F2B8FFF154AD61A288BF9D3506C2C6ECE9BAB7AC34789161` |

## 5. Baseline historique

La génération devenue `debug.2.log` après rotation contenait 19 diagnostics
afghans dédupliqués : les 2 erreurs de pinning ciblées et 17 échecs régionaux
déjà présents. Les deux erreurs ciblées étaient :

| Génération | Log | Heure interne | Message | Chemin | Ligne script |
| --- | --- | --- | --- | --- | ---: |
| pré-correction | `debug.2.log` | 01:19:39 | `Unexpected token: should_be_pinned_by_default` | `common/journal_entries/03_afghanistan.txt` | 2 |
| pré-correction | `debug.2.log` | 01:19:39 | `Unexpected token: should_be_pinned_by_default` | `common/journal_entries/03_afghanistan.txt` | 1826 |

## 6. Instructions et retour humain

L’opérateur a reçu l’instruction d’utiliser exactement un lancement, de monter
uniquement le fork attendu sous Victoria 3 1.13 — The Great Wave, de créer une
partie neuve au 1er janvier 1776 avec le Vietnam, de ne forcer aucune journal
entry ni utiliser la console, d’attendre le chargement complet, puis de fermer
le jeu et le launcher avant l’analyse.

Premier retour humain exact :

~~~text
fork monter et une partie avec le vietnam  à etait joué jusqu"au 5 janvier
~~~

La capture jointe montre le Vietnam, la carte chargée et le 5 janvier 1776.

Confirmation de fermeture et observation exactes :

~~~text
jeu et launcher fermés aucune anomalie vue
~~~

Après cette confirmation, le contrôle renvoie zéro processus cible. L’analyse
des logs n’a commencé qu’après ce contrôle.

## 7. Manifeste après lancement et rotation

Le manifeste complet après lancement contient encore 60 noms et se trouve dans
`%TEMP%\HOTFIX_6A22Q_LOGS_AFTER.json`, capturé à
`2026-08-05T17:13:33.4001538Z`. Son SHA-256 est
`4922FA35105053E2DE7B416CAEC284BBA3EE1347DA2DF4AC1B9A56678D59D5DF`.
Aucun nom n’est créé ou supprimé ; 49 entrées changent de hash et 11 restent
identiques. Vingt fichiers portent un hash absent du manifeste avant.

| Log frais | Octets | Horodatage local | SHA-256 après |
| --- | ---: | --- | --- |
| `code_revisions.log` | 1 133 | 2026-08-05 18:59:01 | `628058CF61119A4BBD7FF6238E2AE8D42C3BA01B16D89C26E210BFED47232E68` |
| `debug.1.log` | 122 261 | 2026-08-05 18:59:35 | `F0D820034D164FF22C7691D700F5ADD97C35D5921A4F12EEAF41EA75D98DB252` |
| `debug.log` | 496 616 | 2026-08-05 19:12:47 | `92BA705426CAE91590CFF40BC99243DA15226A6858C7B2988B6D553CC9D81123` |
| `dedicated_server.log` | 1 383 | 2026-08-05 19:08:48 | `864AD4B81D4089D1D8F0188EBD4B58A31770B51F7E87CF03A22C8387F846EC63` |
| `error.log` | 138 553 | 2026-08-05 19:12:39 | `2EA981A8E3587344D814C2548EBA5C1CA3875A29A5A2C82544AF14B8917FFED0` |
| `game.log` | 268 159 | 2026-08-05 19:12:39 | `6CA4FBD2EA0B51468367247FD7F828C6DA6B256CC21D190C729413145257C20E` |
| `system.log` | 1 100 | 2026-08-05 18:59:48 | `A69B4117FC5CFEBBB4DD61EE6DFEC099C760737AB45B8E9ACA19741644241266` |
| `warning.log` | 6 234 | 2026-08-05 18:59:49 | `FA363323E9DBA2EE7C0E14E094B1E4472B1CB77807254DB68185B667F40FC711` |

La rotation est prouvée par l’ancien `debug.log` de hash `FFEFFAF2…BD4D8`,
devenu `debug.2.log` avec le même hash, et l’ancien `debug.1.log` de hash
`109EBCAC…B6CC1`, devenu `debug.3.log`. Les segments de debug réellement frais
sont donc `debug.1.log` et `debug.log`. Les familles `code_revisions`,
`dedicated_server`, `system` et `warning` présentent la même rotation vers
leurs suffixes `.1` à `.5`.

## 8. Preuves de montage, version et partie

| Exigence | Preuve de la génération fraîche |
| --- | --- |
| fork exact | `debug.1.log` ligne 68 : nom du mod et chemin `1776_Age_of_Revolutions_fork` |
| montage exact | `debug.1.log` ligne 87 : `Mounted Data` sur le chemin du fork |
| Victoria 3 1.13 | `code_revisions.log` ligne 4 : `game_branch: release/1.13.0` |
| exécutable 1.13 | `system.log` ligne 1 : `Exe Git Version: release/1.13.0` |
| The Great Wave | `debug.1.log` lignes 2 à 5 et 54 : installation et DLC The Great Wave |
| partie neuve 1776 | `dedicated_server.log` : ticks de `1776.1.1.6` à `1776.1.5` |
| pays témoin | retour humain et capture : Vietnam |
| absence de crash | retour humain : aucune anomalie vue |

Le descripteur annonce encore la version 1.12.5 et produit un avertissement de
métadonnée face au moteur 1.13.0. Cet avertissement n’empêche ni le montage du
fork ni le chargement de la partie et ne vise pas le fichier Afghanistan.

## 9. Déduplication et recherche de régressions

La clé de déduplication est `génération + message normalisé + chemin + ligne`.

| Cohorte | Brut pertinent | Dédupliqué | Classe |
| --- | ---: | ---: | --- |
| baseline pré-correction, `debug.2.log` | 19 | 19 | 2 pinning ciblés + 17 régionaux historiques |
| rotation historique, `debug.4.log` | 19 | 19 | ancienne génération exclue |
| 6A.22Q fraîche, `debug.1.log` + `debug.log` | 17 | 17 | 0 pinning ciblé + 17 régionaux historiques |
| diagnostics de pinning visant d’autres fichiers | 369 | 369 | hors périmètre |

La différence d’ensembles normalisés retire exactement les diagnostics des
lignes 2 et 1826. Les 17 identités régionales historiques sont égales avant et
après ; le nombre d’identités fraîches absentes de la baseline est zéro.

| Recherche | Résultat |
| --- | ---: |
| diagnostic ciblé combinant propriété et chemin | 0 |
| nouvelle erreur normalisée liée à `03_afghanistan.txt` | 0 |
| erreur visant `je_consolidate_afghanistan` ou `je_unify_afghanistan` | 0 |
| erreurs régionales historiques inchangées | 17 |

Les erreurs globales concernant d’autres fichiers et les 17 erreurs régionales
préexistantes ne sont ni corrigées ni reclassées par cette QA.

## 10. État Git final et documents

Avant les écritures documentaires, le HEAD reste
`07c7a038b2c4d458e888435d11f95c644c7fb3d6`, l’arbre suivi et l’index sont
propres, les hashes gameplay sont inchangés, les huit non-suivis protégés sont
intacts et le stash NAVY-3C-3 reste
`518df704fa14599c0f254fae13859210663dd976`.

Documents modifiés :

- création du présent rapport ;
- mise à jour de `docs/reports/hotfix/INDEX.md` ;
- mise à jour de `HOTFIX_REPORT_INDEX.csv` ;
- mise à jour de `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- mise à jour de `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- mise à jour de l’unique ligne `common/journal_entries/03_afghanistan.txt`
  dans `HOTFIX_MERGE_REMAINING_WORK.csv`.

`HOTFIX_NEXT_MERGE_PHASE_PROMPT.md` n’est pas modifié : aucune prochaine phase
documentaire exacte n’est sélectionnée. Aucun fichier gameplay n’a changé et
aucun commit automatique n’a été créé.

## 11. Verdict

~~~text
HOTFIX_6A22Q_AFGHANISTAN_TWO_JE_PINNING_1_13_RUNTIME_PASS
AFGHANISTAN_TWO_JE_PINNING_FRESH_LOG_GENERATION_CONFIRMED
AFGHANISTAN_TWO_JE_PINNING_DIAGNOSTICS_2_TO_0
AFGHANISTAN_03_AFGHANISTAN_NEW_RUNTIME_ERRORS_0
AFGHANISTAN_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE
AFGHANISTAN_GAMEPLAY_HASH_PRESERVED
AFGHANISTAN_GREAT_GAME_HUNKS_UNCHANGED
AFGHANISTAN_UI_PINNING_BEHAVIOR_NOT_CLAIMED_UNLESS_NATURALLY_OBSERVED
POLAND_VALIDATED_ALIGNMENT_REMAINS_CLOSED
ONE_HUMAN_RUNTIME_LAUNCH_USED
NO_GAMEPLAY_CHANGED_DURING_RUNTIME
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NO_NEXT_EXECUTION_PHASE_SELECTED
~~~
