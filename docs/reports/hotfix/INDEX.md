# Index global des rapports hotfix

## 1. Statut global du hotfix

Le périmètre Inde HOTFIX-5 est clos : `HOTFIX_5_INDIA_COMPLETE`. La bibliothèque documentaire est réorganisée et indexée. Les autres régions conservent leur historique et leurs états propres ; cette clôture ne les déclare pas globalement terminées.

## 2. Navigation par région

| Région | Statut | Index régional | Rapport principal |
|---|---|---|---|
| Inde | `HOTFIX_5_INDIA_COMPLETE` | [India](india/README.md) | [Clôture Inde](india/closure/HOTFIX_5_INDIA_CLOSURE.md) |
| Japon | `CURRENT`, clôture consolidée encore distincte | [Japan](japan/README.md) | [Correction EZO/Hokkaido](japan/HOTFIX_4E8_FIX_EZO_HOKKAIDO_GATE.md) |
| Mamluk Iraq | `CURRENT`, sans clôture runtime dédiée | [Mamluk Iraq](mamluk_iraq/README.md) | [Objectif secret IR1](mamluk_iraq/HOTFIX_3F_IR1_SECRET_GOAL.md) |
| Transversal | `REFERENCE` | [Shared](shared/README.md) | [Audit upstream](shared/HOTFIX_DLC_UPSTREAM_CHANGE_AUDIT.md) |

## 3. Navigation par sujet

- Inde : [vue d’ensemble](india/00_overview/), [East India Company](india/east_india_company/), [infrastructure et famines](india/infrastructure_and_famines/), [Sepoy](india/sepoy/), [states et setup](india/states_and_setup/), [clôture](india/closure/).
- Japon : Ryukyu, Hokkaido/Ezo/Sakhalin, Sakoku/Tenpo, Iwakura et Zaibatsu dans [japan/](japan/).
- Mamluk Iraq : base IR1, territoire, armée, protectorat, diplomatic play et secret goal dans [mamluk_iraq/](mamluk_iraq/).

## 4. Rapports de clôture

- [HOTFIX-5 — Clôture Inde](india/closure/HOTFIX_5_INDIA_CLOSURE.md), verdict `HOTFIX_5_INDIA_COMPLETE`, accompagné de son [manifeste](india/closure/HOTFIX_5_INDIA_CLOSURE_MANIFEST.csv).
- [Réorganisation de la bibliothèque](_index/HOTFIX_REPORT_LIBRARY_REORGANIZATION.md), verdict `HOTFIX_5_INDIA_COMPLETE_AND_REPORT_LIBRARY_INDEXED`.
- [Audit de retrait de la copie jetable Sepoy](_index/HOTFIX_DISPOSABLE_TEST_MOD_RETIREMENT.md), avec [manifeste individuel de 984 fichiers](_index/HOTFIX_DISPOSABLE_TEST_MOD_FINAL_MANIFEST.csv). Le retrait est autorisable mais n’est pas exécuté dans AH.

## 5. Rapports runtime finaux

| Phase | Sujet | Verdict | Statut | Rapport | Compagnon |
|---|---|---|---|---|---|
| C1AG | Trigger Bombay positif/négatif | `PASS_BOMBAY_TRIGGER_RUNTIME_VALIDATION` | `FINAL` | [rapport](india/sepoy/HOTFIX_5C2E4C1AG_BOMBAY_TRIGGER_RUNTIME_VALIDATION.md) | [résultats](india/sepoy/HOTFIX_5C2E4C1AG_BOMBAY_TRIGGER_RUNTIME_RESULTS.csv) |
| C1AB | Radicaux Bombay | `C1X_RADICAL_FAILURE_NON_REPRODUCIBLE_OR_TIMING_DEPENDENT` | `FINAL` | [rapport](india/sepoy/HOTFIX_5C2E4C1AB_E1_RADICAL_CLEAN_RERUN.md) | [résultats](india/sepoy/HOTFIX_5C2E4C1AB_E1_RADICAL_CLEAN_RESULTS.csv) |
| C1T | Retraite Madras 2.c | `PASS_C1_FIX_RUNTIME_PARTIAL_UI` | `FINAL` | [rapport](india/sepoy/HOTFIX_5C2E4C1T_SEPOY_C1_FIX_RUNTIME_TEST.md) | [résultats](india/sepoy/HOTFIX_5C2E4C1T_C1_FIX_RUNTIME_RESULTS.csv) |
| C1P | Retraite Bengal 2.b | `PASS_B1_RADICAL_2B_RUNTIME_PARTIAL_UI` | `FINAL` | [rapport](india/sepoy/HOTFIX_5C2E4C1P_B1_RADICAL_2B_RUNTIME_TEST.md) | [résultats](india/sepoy/HOTFIX_5C2E4C1P_B1_RADICAL_2B_RESULTS.csv) |
| C1E1 | Scénario A-1 | `PASS_A1_RUNTIME_OBSERVATION_COMPLETE` | `FINAL` | [rapport](india/sepoy/HOTFIX_5C2E4C1E1_SEPOY_A1_OBSERVATION_COMPLETION.md) | [résultats](india/sepoy/HOTFIX_5C2E4C1E1_A1_OWNER_COMPLETION.csv) |
| C1G | Scénario A-2 | validation runtime | `FINAL` | [rapport](india/sepoy/HOTFIX_5C2E4C1G_SEPOY_A2_RUNTIME_TEST.md) | [résultats](india/sepoy/HOTFIX_5C2E4C1G_A2_RUNTIME_RESULTS.csv) |
| C1I/I1 | Scénario A-3 | validation runtime et nettoyage tooltip | `FINAL` | [runtime](india/sepoy/HOTFIX_5C2E4C1I_SEPOY_A3_RUNTIME_TEST.md) | [résultats](india/sepoy/HOTFIX_5C2E4C1I_A3_RUNTIME_RESULTS.csv) |
| E4B3 | APIs Sepoy | `PASS` | `FINAL` | [rapport](india/sepoy/HOTFIX_5C2E4B3_SEPOY_API_RUNTIME_RETEST.md) | — |

## 6. Corrections gameplay validées

- Bengal : [correction C1L](india/sepoy/HOTFIX_5C2E4C1L_B1_BENGAL_CORE_FIX.md), validée territorialement en C1M et radicalement en C1P.
- Madras : [correction C1S](india/sepoy/HOTFIX_5C2E4C1S_C1_MADRAS_CORE_FIX.md), validée en C1T.
- Bombay : [protection C1W](india/sepoy/HOTFIX_5C2E4C1W_E1_BOMBAY_CORE_FIX.md), radicaux validés en C1AB, [trigger AE](india/sepoy/HOTFIX_5C2E4C1AE_E2_BOMBAY_TRIGGER_FIX.md) validé en C1AG.
- APIs : [journal pinning](india/sepoy/HOTFIX_5C2E4B1_SEPOY_PINNING_API.md) et [rôle personnage](india/sepoy/HOTFIX_5C2E4B2_SEPOY_CHARACTER_ROLE_API.md), validés en E4B3.

## 7. Phases encore ouvertes

- Japon : une clôture consolidée distincte reste possible après les correctifs 4E5–4E8.
- Mamluk Iraq : aucun rapport de clôture/runtime global n’est présent ; 3F reste la dernière correction documentaire.
- Les recherches technologiques sont hors bibliothèque et hors périmètre AH.

## 8. Rapports inconclusifs ou remplacés

Les échecs C1C, C1K, C1M, C1O, C1R, C1V et C1X ainsi que les audits inconclusifs C1N/C1Z sont conservés près de leurs correctifs et successeurs. Ils sont catalogués `FAILED_TEST`, `INCONCLUSIVE` ou `SUPERSEDED` dans le [catalogue exhaustif](_index/HOTFIX_REPORT_INDEX.csv).

`WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED` est un statut historique résolu par AE/AF/AG. Le statut courant est `WEST_BENGAL_RETREAT_TRANSFER_EXPECTED` ; les anciens rapports ne sont pas réécrits.

## 9. Conventions de nommage

Les noms `HOTFIX_*` restent inchangés et fournissent l’ordre de phase. Les CSV de manifeste/résultats restent avec leur Markdown compagnon. Les nouveaux documents de navigation utilisent `README.md` ou `INDEX.md`.

## 10. Légende des statuts

`FINAL` = validation finale ; `CURRENT` = référence active ; `INTERMEDIATE` = étape de chaîne ; `SUPERSEDED` = remplacé par un successeur ; `REFERENCE` = contexte ; `FAILED_TEST` = échec historique utile ; `INCONCLUSIVE` = preuve insuffisante ; `BLOCKED` = phase bloquée ; `ARCHIVAL` = conservation administrative.
