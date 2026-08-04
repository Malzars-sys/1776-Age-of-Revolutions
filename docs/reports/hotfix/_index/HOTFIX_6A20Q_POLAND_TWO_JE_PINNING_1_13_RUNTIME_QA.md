# HOTFIX-6A.20Q — QA runtime des deux pinning Pologne sous Victoria 3 1.13

Date : 5 août 2026
Branche : hotfix-dlc-audit
Commit d’entrée : 1622f8359f7d7a9c0b7dc283917902730c1980c8
Message : Align two Poland journal entry pinning properties for 1.13

## 1. Résultat

La QA runtime humaine ciblée passe. Une seule ouverture de Victoria 3 a monté
le fork exact, chargé le moteur release/1.13.0 et créé une partie neuve 1776
avec le Vietnam. La simulation a atteint au moins le 5 janvier selon le retour
humain et le 6 janvier selon la capture fournie et les ticks du journal.

La génération fraîche contient zéro diagnostic visant
common/journal_entries/00_poland.txt. Les deux diagnostics historiques des
lignes 59 et 131 passent donc de 2 à 0. Aucune nouvelle erreur n’est attribuée
à ce fichier et aucun crash n’est observé.

Les deux journal entries polonaises n’ont pas été forcées et ne sont pas
apparues naturellement. Le comportement visuel du pinning n’est donc pas
revendiqué ; seule la compatibilité parser/runtime du correctif est validée.

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| racine Git | dépôt attendu |
| branche | hotfix-dlc-audit |
| HEAD | 1622f8359f7d7a9c0b7dc283917902730c1980c8 |
| message HEAD | Align two Poland journal entry pinning properties for 1.13 |
| rapport 6A.20F dans HEAD | présent avec les verdicts requis |
| arbre suivi avant runtime | propre |
| index Git | vide |
| git diff --check | propre |
| processus Victoria 3 / Dowser / launcher avant lancement | aucun |
| stash NAVY-3C-3 | 518df704fa14599c0f254fae13859210663dd976, intact |
| non-suivis | uniquement les huit éléments protégés connus |

Les non-suivis protégés n’ont pas été ouverts, modifiés, déplacés ou indexés.

## 3. Intégrité gameplay avant et après

| Fichier | Avant | Après | Résultat |
| --- | --- | --- | --- |
| common/journal_entries/00_poland.txt | A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A | A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A | identique |
| common/journal_entries/07_poland_lithuania_mod.txt | 5D3EFE884DE36B6B379FCE1A81D3DC39979DA137D329BD5B4B1D7F9ACC13B1C5 | 5D3EFE884DE36B6B379FCE1A81D3DC39979DA137D329BD5B4B1D7F9ACC13B1C5 | identique |

Après runtime, 00_poland.txt conserve 3 016 octets, 132 lignes, zéro ancienne
propriété et deux propriétés
should_be_pinned_by_default_uninvolved_or_context.

## 4. Manifeste avant lancement

Le manifeste complet de 60 fichiers .log a été capturé hors dépôt dans
%TEMP%\HOTFIX_6A20Q_LOGS_BEFORE.json à
2026-08-04T23:13:25.8185457Z.

| Log courant | Octets | Horodatage UTC | SHA-256 avant |
| --- | ---: | --- | --- |
| code_revisions.log | 1 133 | 2026-08-04T19:05:05.8839600Z | F0FF5C44B75A7181340D468D09633531F40B36282BD650A995BF8B3C0BB2B38D |
| debug.log | 307 325 | 2026-08-04T20:55:36.9332014Z | B401921CD7FF354A3D0D82E385DD514C5C28585638400908C5E98F6DC1D4DF40 |
| dedicated_server.log | 66 | 2026-08-04T19:26:22.8900219Z | 1D7E81F2337A907F4A8089B3CFAB1AFC79F3BFDFF94A388EB49BF126DCE066AD |
| error.log | 53 069 | 2026-08-04T20:23:40.2408927Z | C88C6E9B18B64C328347878EDBF8BF3F55014C7C2ABDEC58965D6AAB372E5536 |
| game.log | 295 590 | 2026-08-04T20:23:40.2408927Z | 7C8DDCC2BE79FA57AA5489D3671F298FABAC44D62D806AF5C694C3E78530C457 |
| system.log | 1 101 | 2026-08-04T19:05:39.1711262Z | 5AA70BF488C1A81B5BD8D513AB160E3AF248575C94977195D7110BAF6B1F26D3 |

## 5. Instructions données à l’opérateur

~~~text
HUMAN_RUNTIME_ACTION_REQUIRED

1. Ouvrir le launcher Paradox.
2. Vérifier que le playset actif monte exactement 1776_Age_of_Revolutions_fork.
3. Vérifier que Victoria 3 utilise la version 1.13 — The Great Wave.
4. Lancer Victoria 3 une seule fois.
5. Créer une partie neuve au 1er janvier 1776.
6. Choisir un pays témoin stable naturellement disponible, de préférence le Vietnam.
7. Ne lancer aucune commande de console.
8. Ne forcer aucune journal entry.
9. Ne modifier aucun pays, état, technologie, loi ou événement pour exposer les entrées polonaises.
10. Attendre le chargement complet de la carte.
11. Laisser passer au minimum jusqu’au 3 janvier 1776 afin de confirmer que la partie fonctionne.
12. Noter toute clé brute, erreur visible, crash ou comportement anormal.
13. Quitter au menu principal.
14. Fermer entièrement Victoria 3.
15. Fermer entièrement le launcher Paradox.
16. Confirmer ici : « jeu et launcher fermés » et signaler les anomalies observées.
~~~

## 6. Retour humain exact

Premier retour :

~~~text
avancé jusqu'au 5 janvier avec le fork monté en tant que vietnam je n'ai vue aucune clée brute ou autre
~~~

Le retour était accompagné d’une capture montrant le Vietnam, la carte chargée
et la date du 6 janvier 1776, sans clé brute visible.

Confirmation de fermeture :

~~~text
jeu et launcher fermés
~~~

Après cette confirmation, le contrôle de processus a renvoyé
NO_TARGET_PROCESSES. L’analyse des logs n’a commencé qu’après ce contrôle.

## 7. Fenêtre runtime et lancement unique

| Événement | Preuve |
| --- | --- |
| initialisation moteur | journaux à partir de 01:14:22 |
| montage fork/DLC | debug.1.log à 01:14:34 |
| chargement carte / ticks | dedicated_server.log à partir de 01:24:28 |
| dernier log courant | debug.log à 01:25:46 |
| fermeture humaine | confirmée ; heure murale exacte non disponible |
| nombre de lancements | un seul lancement humain |

Aucune console, aucune journal entry forcée et aucune manipulation destinée à
exposer les entrées polonaises n’ont été utilisées.

## 8. Manifeste après lancement et rotation

Le manifeste complet après lancement contient toujours 60 noms. Aucun nom
n’est créé ou supprimé ; 49 entrées changent de hash par réécriture ou
rotation et 11 restent identiques. Vingt-sept fichiers portent un horodatage
postérieur au manifeste avant.

Les principaux segments de la génération fraîche sont :

| Log | Octets | Horodatage UTC | SHA-256 après |
| --- | ---: | --- | --- |
| code_revisions.log | 1 133 | 2026-08-04T23:14:22.0210952Z | AB87218EB7382085A96504D6205DB5D6A1BC34561FB99CEC98C5BD078D0747F7 |
| debug.1.log | 216 883 | 2026-08-04T23:17:54.4459878Z | 109EBCACE21F5663AD917C7FA59DBDD61BB225BA9C9681AC25DE827A637B6CC1 |
| debug.log | 401 820 | 2026-08-04T23:25:46.7850342Z | FFEFFAF26F69C1A0E09F6EB4F1C9FD1723FBA9DF793967F26CF26159725BD4D8 |
| dedicated_server.log | 1 721 | 2026-08-04T23:24:33.7254774Z | 207BA07990A4A39ED83B23386C92348B9C585D1C7E4AABD489FD5CDE9815D546 |
| error.log | 450 343 | 2026-08-04T23:25:39.6033219Z | C7FF964815F62B1E06190B6201F28B98B53006D967E1D654B2888A4AAB34CC41 |
| game.log | 374 488 | 2026-08-04T23:25:39.6033219Z | 15E8996B4F15DB9A35F40462CC6F69FC9DEEE6E723E942EC7C2B285B0CB9C412 |
| system.log | 1 100 | 2026-08-04T23:14:54.6938470Z | 89CFC4FBF822AE41F2B8FFF154AD61A288BF9D3506C2C6ECE9BAB7AC34789161 |
| warning.log | 6 234 | 2026-08-04T23:14:55.1693773Z | 637059AAE8ADE03148E4B392CE7F6437AA73CEA66490CAC3A7CD7626CC262A7A |

La rotation est prouvée par l’ancien debug.log de hash B401921C…D4DF40,
devenu debug.2.log avec le même hash. L’ancien debug.1.log de hash
34269BB6…9ED5B9 devient debug.3.log. Les nouveaux segments sont donc
debug.1.log et debug.log, et non les rotations historiques.

## 9. Preuves de montage, version et partie

| Exigence | Preuve de la génération fraîche |
| --- | --- |
| fork exact | debug.1.log ligne 68 : nom du mod et chemin 1776_Age_of_Revolutions_fork |
| montage exact | debug.1.log ligne 87 : Mounted Data sur le chemin du fork |
| Victoria 3 1.13 | code_revisions.log ligne 4 : game_branch release/1.13.0 |
| exécutable 1.13 | system.log ligne 1 : Exe Git Version release/1.13.0 |
| The Great Wave | debug.1.log lignes 2 à 5 et 54 : installation et DLC The Great Wave |
| partie neuve 1776 | dedicated_server.log : ticks 1776.1.1 à 1776.1.6 |
| pays témoin | retour humain et capture : Vietnam |
| absence de crash | retour humain et zéro occurrence crash/exception/fatal dans la génération isolée |

Le descripteur du mod annonce encore la version 1.12.5 et produit un avertissement
de métadonnée face au moteur 1.13.0. Cet avertissement n’empêche ni le montage
positif du fork ni le chargement de la partie et ne vise pas 00_poland.txt.

## 10. Baseline historique et déduplication

Après rotation, la baseline qui était debug.log avant la session est conservée
dans debug.2.log avec le même hash B401921C…D4DF40.

| Génération | Log | Horodatage interne | Message | Chemin | Ligne script | Brut | Dédupliqué | Classe |
| --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| baseline pré-correction | debug.2.log | 21:09:37 | Unexpected token: should_be_pinned_by_default | common/journal_entries/00_poland.txt | 59 | 1 | 1 | ancien runtime |
| baseline pré-correction | debug.2.log | 21:09:37 | Unexpected token: should_be_pinned_by_default | common/journal_entries/00_poland.txt | 131 | 1 | 1 | ancien runtime |
| rotation antérieure séparée | debug.4.log | 19:38:06 | mêmes deux diagnostics | common/journal_entries/00_poland.txt | 59 et 131 | 2 | 2 | ancien runtime exclu |
| 6A.20Q fraîche | debug.1.log + debug.log | 01:14:22–01:25:46 | diagnostic ciblé absent | — | — | 0 | 0 | nouveau runtime |

La déduplication utilise génération + message normalisé + chemin + ligne.
Les 371 diagnostics génériques de pinning encore présents dans le nouveau
debug.log concernent d’autres fichiers et restent hors périmètre. Aucun n’est
confondu avec 00_poland.txt.

## 11. Recherche de régressions

Sur tous les segments non vides de la génération fraîche :

| Recherche | Résultat brut | Résultat dédupliqué |
| --- | ---: | ---: |
| common/journal_entries/00_poland.txt | 0 | 0 |
| diagnostic ciblé combinant propriété et chemin | 0 | 0 |
| je_christ_of_nations ou je_poland_lithuania | 0 | 0 |
| nouvelle erreur parser/trigger/effect/scope liée à 00_poland.txt | 0 | 0 |
| crash, exception ou fatal | 0 | 0 |

Les erreurs globales concernant d’autres fichiers, dont des pinning obsolètes,
ne sont ni corrigées ni reclassées par cette phase.

## 12. Observation visuelle limitée

La carte 1776 a chargé avec le Vietnam et la date visible atteint le
6 janvier. L’opérateur ne voit aucune clé brute, aucun crash et aucune
anomalie. Les deux entrées polonaises ne sont pas naturellement visibles
depuis ce témoin ; aucune validation UI du pinning n’est affirmée.

## 13. État Git final

Le HEAD reste 1622f8359f7d7a9c0b7dc283917902730c1980c8. Avant les écritures
documentaires, l’arbre suivi et l’index sont propres, les deux hashes gameplay
sont inchangés et le stash NAVY-3C-3 reste
518df704fa14599c0f254fae13859210663dd976.

Aucun fichier gameplay n’a changé pendant le runtime ou la finalisation.
Aucun commit automatique n’a été créé.

## 14. Documents modifiés

- création de HOTFIX_6A20Q_POLAND_TWO_JE_PINNING_1_13_RUNTIME_QA.md ;
- mise à jour de docs/reports/hotfix/INDEX.md ;
- mise à jour de HOTFIX_REPORT_INDEX.csv ;
- mise à jour de HOTFIX_MERGE_BLOCK_STATUS.csv ;
- mise à jour de HOTFIX_MERGE_COMPLETION_ROADMAP.md ;
- mise à jour de l’unique ligne common/journal_entries/00_poland.txt dans
  HOTFIX_MERGE_REMAINING_WORK.csv.

HOTFIX_NEXT_MERGE_PHASE_PROMPT.md n’est pas modifié : aucun identifiant précis
de prochaine phase documentaire n’est établi par les documents canoniques.

## 15. Verdict

~~~text
HOTFIX_6A20Q_POLAND_TWO_JE_PINNING_1_13_RUNTIME_PASS
POLAND_TWO_JE_PINNING_FRESH_LOG_GENERATION_CONFIRMED
POLAND_TWO_JE_PINNING_DIAGNOSTICS_2_TO_0
POLAND_00_POLAND_NEW_RUNTIME_ERRORS_0
POLAND_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE
POLAND_GAMEPLAY_HASH_PRESERVED
POLAND_CUSTOM_JOURNAL_ENTRY_FILE_UNCHANGED
POLAND_UI_PINNING_BEHAVIOR_NOT_CLAIMED_UNLESS_NATURALLY_OBSERVED
ONE_HUMAN_RUNTIME_LAUNCH_USED
NO_GAMEPLAY_CHANGED_DURING_RUNTIME
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NO_NEXT_EXECUTION_PHASE_SELECTED
~~~
