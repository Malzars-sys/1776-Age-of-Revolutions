# Index global des rapports hotfix

## 1. Statut global du hotfix

Le périmètre Inde HOTFIX-5 est clos : `HOTFIX_5_INDIA_COMPLETE`. La bibliothèque documentaire est réorganisée et indexée. `HOTFIX-6A_GLOBAL_SCRIPT_DELTAS` reste le bloc global. Le paquet Autriche/Croatie-Slavonie/Suisse est complet. La migration des formations militaires 1.13 est validée en partie neuve et après sauvegarde/recharge, avec son correctif de QG séparé. La phase DEI/VOC 6A.3F et les alignements de `je_balkan_national_awakenings`, `je_yugoslavia`, `je_risorgimento`, `je_greek_nationalism`, `je_great_eastern_crisis` et des huit entrées Sick Man sont clos. Le démarrage Tanzimat reste désactivé en 1776 et son éventuelle activation différée demeure un backlog de design.

## 2. Navigation par région

| Région | Statut | Index régional | Rapport principal |
|---|---|---|---|
| Inde | `HOTFIX_5_INDIA_COMPLETE` | [India](india/README.md) | [Clôture Inde](india/closure/HOTFIX_5_INDIA_CLOSURE.md) |
| Japon | `CURRENT`, clôture consolidée encore distincte | [Japan](japan/README.md) | [Correction EZO/Hokkaido](japan/HOTFIX_4E8_FIX_EZO_HOKKAIDO_GATE.md) |
| Mamluk Iraq | `CURRENT`, sans clôture runtime dédiée | [Mamluk Iraq](mamluk_iraq/README.md) | [Objectif secret IR1](mamluk_iraq/HOTFIX_3F_IR1_SECRET_GOAL.md) |
| Russie | `CURRENT`, statique passé, runtime global différé | [_index](_index/) | [Alignement Subjecthood](_index/HOTFIX_6A_RUSSIA_SUBJECTHOOD_ALIGNMENT.md) |
| Autriche/Croatie/Suisse | `COMPLETE` | [_index](_index/) | [Correction runtime HOTFIX-6A.2F2](_index/HOTFIX_6A2F2_SWISS_POP_NAVAL_BASE_RUNTIME_CORRECTION.md) |
| DEI | `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE` | [_index](_index/) | [Clôture HOTFIX-6A.3F](_index/HOTFIX_6A3F_DEI_TARGETED_FIX.md) |
| Transversal | `REFERENCE` | [Shared](shared/README.md) | [Audit upstream](shared/HOTFIX_DLC_UPSTREAM_CHANGE_AUDIT.md) |

## 3. Navigation par sujet

- Inde : [vue d’ensemble](india/00_overview/), [East India Company](india/east_india_company/), [infrastructure et famines](india/infrastructure_and_famines/), [Sepoy](india/sepoy/), [states et setup](india/states_and_setup/), [clôture](india/closure/).
- Japon : Ryukyu, Hokkaido/Ezo/Sakhalin, Sakoku/Tenpo, Iwakura et Zaibatsu dans [japan/](japan/).
- Mamluk Iraq : base IR1, territoire, armée, protectorat, diplomatic play et secret goal dans [mamluk_iraq/](mamluk_iraq/).

## 4. Rapports de clôture

- [HOTFIX-5 — Clôture Inde](india/closure/HOTFIX_5_INDIA_CLOSURE.md), verdict `HOTFIX_5_INDIA_COMPLETE`, accompagné de son [manifeste](india/closure/HOTFIX_5_INDIA_CLOSURE_MANIFEST.csv).
- [Réorganisation de la bibliothèque](_index/HOTFIX_REPORT_LIBRARY_REORGANIZATION.md), verdict `HOTFIX_5_INDIA_COMPLETE_AND_REPORT_LIBRARY_INDEXED`.
- [Audit de retrait de la copie jetable Sepoy](_index/HOTFIX_DISPOSABLE_TEST_MOD_RETIREMENT.md), avec [manifeste individuel de 984 fichiers](_index/HOTFIX_DISPOSABLE_TEST_MOD_FINAL_MANIFEST.csv). Le retrait est autorisable mais n’est pas exécuté dans AH.
- [Feuille de route de fin du merge](_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md), avec [registre des 534 écarts fonctionnels](_index/HOTFIX_MERGE_REMAINING_WORK.csv), [inventaire trois voies](_index/HOTFIX_MERGE_THREE_WAY_INVENTORY.csv) et [matrice des blocs](_index/HOTFIX_MERGE_BLOCK_STATUS.csv).
- [Prompt autonome d’alignement Merchant Banking GEN/VEN HOTFIX-6A.13F](_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md).
- [Réconciliation des productions concurrentes C1AI](_index/HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md), verdict `GLOBAL_SCRIPT_DELTAS_WITH_RUSSIA_FIRST`.
- [Audit 6A.2](_index/HOTFIX_6A2_AUSTRIA_CROATIA_WEST_SWITZERLAND_AUDIT.md), [résolution 6A.2R](_index/HOTFIX_6A2R_TARGET_HUNK_RESOLUTION.md), [correction 6A.2F](_index/HOTFIX_6A2F_AUSTRIA_CROATIA_WEST_SWITZERLAND_TARGETED_FIX.md), [correction runtime 6A.2F2](_index/HOTFIX_6A2F2_SWISS_POP_NAVAL_BASE_RUNTIME_CORRECTION.md) et [delta map](_index/HOTFIX_6A2_AUSTRIA_CROATIA_WEST_SWITZERLAND_DELTA_MAP.csv). Statique et runtime PASS; Suisse autrichienne 30 K et flotte AUS 2,30 K / 2,30 K confirmées.
- [Audit DEI 6A.3](_index/HOTFIX_6A3_DEI_TARGETED_AUDIT.md), [résolution 6A.3R](_index/HOTFIX_6A3R_DEI_BREAKUP_HUNK_RESOLUTION.md), [correction et clôture 6A.3F](_index/HOTFIX_6A3F_DEI_TARGETED_FIX.md) et [delta map](_index/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv) : CEY/SAF, Java, Indonésie, refus et économie post-compagnie validés statiquement et en jeu.
- [QA runtime des formations militaires 1.13](_index/HOTFIX_MILITARY_FORMATIONS_1_13_RUNTIME_QA.md) : douze QG corrigés dans `3b02b2a`, partie neuve, sauvegarde/recharge et deux progressions de trois mois validées.
- [Sélection résiduelle 6A.4](_index/HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) : 161 lignes relues, 22 alignements de pinning 1.13 identifiés et sélection du correctif balkanique à deux hunks dans un seul fichier.
- [Alignement Balkan National Awakening 6A.4F](_index/HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md) : deux hunks appliqués, 51 erreurs propres ramenées à zéro, fork et `dlc014_ip3` montés, JE potentielle lisible en Valachie.
- [Sélection résiduelle 6A.5](_index/HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) : 115 lignes encore directement exploitables, trois candidats comparés et sélection du pinning 1.13 de `je_yugoslavia`, limité à un fichier, un objet et un hunk.
- [Alignement du pinning de `je_yugoslavia` 6A.5F](_index/HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md) : ancien champ remplacé par l’API 1.13 en un hunk, géographie inchangée, Serbie jouée jusqu’au 25 janvier 1776 et diagnostic ciblé ramené de un à zéro.
- [Sélection résiduelle 6A.6](_index/HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) : 389 erreurs de pinning restantes rapprochées de 146 fichiers, exactement trois candidats publiés et sélection de `je_risorgimento`, limitée à un fichier, un objet et un hunk.
- [Alignement du pinning de `je_risorgimento` 6A.6F](_index/HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md) : remplacement API 1.13 appliqué en un hunk ; Naples jouée jusqu’au 2 janvier 1776 ; erreur ciblée ramenée de un à zéro ; date 1836 et géographie préservées. Le suffixe `BUG_year_greater_or_equal` observé appartient au tooltip debug et non à une localisation manquante.
- [Sélection résiduelle 6A.7](_index/HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) : 388 erreurs de pinning restantes rapprochées de 145 fichiers, exactement trois candidats publiés et sélection de l’alignement API de `je_greek_nationalism`, limité à un fichier, un objet et deux hunks.
- [Alignement API du nationalisme grec 6A.7F](_index/HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md) : deux substitutions convergentes appliquées dans un seul objet ; visibilité et géographie préservées ; Grèce indépendante jouée le 30 janvier 1776 ; entrée potentielle lisible ; erreur ciblée ramenée de un à zéro.
- [Audit de la Grande Crise orientale 6A.8R](_index/HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT.md) : six groupes fonctionnels comparés séparément ; source hotfix et vanilla convergent ; les six sont classés `REQUIRED_1_13_ALIGNMENT` et autorisés dans une future correction atomique de 23 additions et 4 suppressions.
- [Alignement de la Grande Crise orientale 6A.8F](_index/HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT.md) : six groupes appliqués dans un objet ; hash cible et diff `23/4` conformes ; vues ottomane et britannique validées ; diagnostic ciblé ramené de un à zéro. L’absence de Tanzimat est isolée pour 6A.9R.
- [Audit de la chaîne ottomane Tanzimat 1776 6A.9R](_index/HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md) : désactivation de départ préservée ; chaîne vanilla jugée anachronique et géopolitiquement incompatible avec 1776 ; Grande Crise orientale toujours accessible par `nationalism` et sécession ; huit pinning classés `REQUIRED_1_13_ALIGNMENT` et sélectionnés pour 6A.9F.
- [Alignement des huit pinning Sick Man 6A.9F](_index/HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md) : huit substitutions exactes dans un fichier ; hash cible et snapshot conformes ; fork et `dlc014_ip3` montés ; huit erreurs parser ramenées à zéro sans activer Tanzimat.
- [Sélection résiduelle 6A.10](_index/HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) : 378 erreurs de pinning recalculées dans 142 fichiers, trois candidats publiés et sélection de deux alignements API 1.13 dans `00_romania.txt`, limités à un fichier, deux objets et deux hunks.
- [Alignement des deux pinning roumains 6A.10F](_index/HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md) : deux substitutions API dans `je_unite_the_principalities` et `je_all_for_one` ; Valachie validée au 2 janvier 1776 ; entrée potentielle lisible ; diagnostics ciblés ramenés de deux à zéro.
- [Sélection résiduelle 6A.11](_index/HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) : 376 erreurs de pinning recalculées dans 141 fichiers, exactement trois candidats publiés et sélection de deux alignements API 1.13 dans `06_portuguese_colonialism.txt`, limités à un fichier, deux objets et deux hunks.
- [Alignement des deux pinning du colonialisme portugais 6A.11F](_index/HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT.md) : deux substitutions API appliquées dans `je_portuguese_colonialism` et `je_the_pink_map` ; Portugal validé du 1er au 2 janvier 1776 ; diagnostics ciblés ramenés de deux à zéro et baseline globale de `376/141` à `374/140`. Les régions legacy et la répétition du nom portugais sont documentées comme dettes adjacentes distinctes.
- [Sélection résiduelle 6A.12](_index/HOTFIX_6A12_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) : baseline confirmée à 374 diagnostics dans 140 fichiers, 161 lignes d’inventaire reclassées, exactement trois candidats publiés et sélection du remplacement atomique de `region_congo` et `region_zanj` dans `je_portuguese_colonialism`. Merchant Banking GEN/VEN et Navigation Acts restent séparés ; la répétition française du nom portugais est systémique et non autonome.
- [Alignement des régions stratégiques portugaises 6A.12F](_index/HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT.md) : remplacement atomique de `region_congo` et `region_zanj` par les clés 1.13 dans un fichier, un objet et un hunk ; Portugal validé du 1er au 2 janvier 1776 ; diagnostics ciblés `186/186/373` ramenés à zéro, entrée potentielle lisible sans clé brute et baseline de pinning inchangée à `374/140`.
- [Sélection résiduelle 6A.13](_index/HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) : baseline directement recalculée à 374 diagnostics dans 140 fichiers (`83` mono-erreur, `57` multi-erreurs), distribution des 161 lignes d’inventaire inchangée et exactement trois candidats publiés. Merchant Banking GEN/VEN est l’unique phase sélectionnée, bornée à deux fichiers, deux objets et deux hunks ; Navigation Acts et Coup restent des audits distincts.
- [Loi initiale Merchant Banking de GEN et VEN 6A.13F](_index/HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW.md) : deux substitutions ciblées `law_traditionalism` → `law_merchant_banking` validées statiquement et en jeu pour Gênes puis Venise ; **Marine marchande** préservée, interface française lisible et zéro diagnostic ciblé. La puissance jugée trop moderne de la loi est enregistrée comme backlog d'équilibrage post-hotfix distinct.
- [Audit de la loi initiale Navigation Acts 6A.14R](_index/HOTFIX_6A14R_NAVIGATION_ACTS_STARTING_LAW_AUDIT.md) : le scope théorique de cinq historiques est résolu en huit fichiers gameplay pertinents, dont BIC, une activation événementielle américaine et le doublon `hubson`/`hudson` de HBC. Infrastructure déjà fusionnée, GBR/NAVY protégé, visibilité invalide pour les `chartered_company` et verdict principal `NAVIGATION_ACTS_STARTING_LAW_BLOCKED_BY_HBC_DEFINITION_CONFLICT`; aucune correction ni phase 6A.14F sélectionnée.
- [Audit de résolution de la double définition HBC 6A.14H](_index/HOTFIX_6A14H_HBC_DOUBLE_DEFINITION_RESOLUTION_AUDIT.md) : les deux historiques proviennent du même import; `hubson` est une variante 1776 legacy avec deux identifiants invalides et `hudson` suit la lignée vanilla. Le runtime confirme une fusion stable, sans clé brute : valeurs conflictuelles de `hudson`, lois et effets additifs de `hubson`, Industrialistes seuls au gouvernement, trois institutions et grain taxé. Verdict `HBC_DUPLICATE_HISTORY_UNKNOWN_REQUIRES_REVIEW`; aucune correction ni phase 6A.14HF sélectionnée.
- [Audit fonctionnel de la journal entry Coup 6A.15R](_index/HOTFIX_6A15R_COUP_JOURNAL_ENTRY_1_13_FUNCTIONAL_AUDIT.md) : treize fichiers fonctionnels ou entrypoints et trois overrides sont cartographiés. Le pinning obsolète de `je_ip4_coup` est isolable en un fichier, un objet et un hunk `1/1`; les deltas adjacents d'événements, scopes, lobby, lois, cooldown, cleanup et invalidation restent différés. Verdict `COUP_JOURNAL_ENTRY_PINNING_ISOLATABLE_ADJACENT_DELTAS_DEFERRED`; 6A.15F est sélectionnée pour le pinning uniquement.

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
| Formations 1.13 | Migration des formations militaires | `MILITARY_FORMATIONS_1_13_RUNTIME_QA_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_MILITARY_FORMATIONS_1_13_RUNTIME_QA.md) | [audit statique](_index/army.md) |
| 6A.3F | Dissolution de la DEI/VOC | `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A3F_DEI_TARGETED_FIX.md) | [delta map](_index/HOTFIX_6A3_DEI_TARGETED_AUDIT_DELTA_MAP.csv) |
| 6A.4F | Balkan National Awakening 1.13 | `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_ALIGNMENT.md) | [sélection 6A.4](_index/HOTFIX_6A4_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) |
| 6A.5F | Pinning de `je_yugoslavia` 1.13 | `HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A5F_YUGOSLAVIA_JE_PINNING_1_13_ALIGNMENT.md) | [sélection 6A.5](_index/HOTFIX_6A5_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) |
| 6A.6F | Pinning de `je_risorgimento` 1.13 | `HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A6F_ITALIAN_UNIFICATION_JE_PINNING_1_13_ALIGNMENT.md) | [sélection 6A.6](_index/HOTFIX_6A6_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) |
| 6A.7F | APIs de `je_greek_nationalism` 1.13 | `HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A7F_GREEK_NATIONALISM_1_13_API_ALIGNMENT.md) | [sélection 6A.7](_index/HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) |
| 6A.8F | Alignement de `je_great_eastern_crisis` 1.13 | `HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A8F_GREAT_EASTERN_CRISIS_1_13_ALIGNMENT.md) | [audit 6A.8R](_index/HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT.md) |
| 6A.9F | Huit pinning Sick Man 1.13 | `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md) | [audit 6A.9R](_index/HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md) |
| 6A.10 | Sélection du prochain résidu global | `HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) | [alignement 6A.10F](_index/HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md) |
| 6A.10F | Deux pinning roumains 1.13 | `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md) | [sélection 6A.10](_index/HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) |
| 6A.11F | Deux pinning du colonialisme portugais 1.13 | `HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT.md) | [sélection 6A.11](_index/HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) |
| 6A.12F | Régions stratégiques du colonialisme portugais 1.13 | `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT_COMPLETE` | `FINAL` | [rapport](_index/HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT.md) | [sélection 6A.12](_index/HOTFIX_6A12_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md) |

## 6. Corrections gameplay validées

- Bengal : [correction C1L](india/sepoy/HOTFIX_5C2E4C1L_B1_BENGAL_CORE_FIX.md), validée territorialement en C1M et radicalement en C1P.
- Madras : [correction C1S](india/sepoy/HOTFIX_5C2E4C1S_C1_MADRAS_CORE_FIX.md), validée en C1T.
- Bombay : [protection C1W](india/sepoy/HOTFIX_5C2E4C1W_E1_BOMBAY_CORE_FIX.md), radicaux validés en C1AB, [trigger AE](india/sepoy/HOTFIX_5C2E4C1AE_E2_BOMBAY_TRIGGER_FIX.md) validé en C1AG.
- APIs : [journal pinning](india/sepoy/HOTFIX_5C2E4B1_SEPOY_PINNING_API.md) et [rôle personnage](india/sepoy/HOTFIX_5C2E4B2_SEPOY_CHARACTER_ROLE_API.md), validés en E4B3.

## 7. Phases encore ouvertes

- Japon : une clôture consolidée distincte reste possible après les correctifs 4E5–4E8.
- Mamluk Iraq : aucun rapport de clôture/runtime global n’est présent ; 3F reste la dernière correction documentaire.
- Merge global : Russie terminée statiquement; paquet Autriche/Croatie/Suisse clos par `HOTFIX_6A2F2`; DEI/VOC clos par `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`; Balkan National Awakening clos par `HOTFIX_6A4F_BALKAN_NATIONAL_AWAKENING_1_13_COMPLETE`; `je_yugoslavia`, `je_risorgimento`, `je_greek_nationalism`, `je_great_eastern_crisis`, les huit entrées Sick Man, les deux entrées roumaines, les deux pinning et les deux régions stratégiques du colonialisme portugais sont clos. Merchant Banking GEN/VEN est également clos statiquement et en runtime par `HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW_COMPLETE`. Les audits Navigation Acts 6A.14R et HBC 6A.14H sont clos sans correction; l'intention HBC reste inconnue. L'audit Coup 6A.15R isole un seul hunk de pinning 1.13 et sélectionne `HOTFIX_6A15F_COUP_JOURNAL_ENTRY_1_13_ALIGNMENT`; tous les deltas fonctionnels d'événements, scopes, lobby, lois et lifecycle restent différés. GBR croise NAVY, BIC et la chaîne américaine restent protégées. Imperialism, Tanzimat et la répétition française du nom portugais ne sont pas autorisés. L'équilibrage 1776 de Merchant Banking est un backlog post-hotfix non bloquant. L'ancien total annoncé de 26 deltas reste `UNVERIFIED`.
- Les recherches technologiques sont hors bibliothèque et hors périmètre AH.

## 8. Rapports inconclusifs ou remplacés

Les échecs C1C, C1K, C1M, C1O, C1R, C1V et C1X ainsi que les audits inconclusifs C1N/C1Z sont conservés près de leurs correctifs et successeurs. Ils sont catalogués `FAILED_TEST`, `INCONCLUSIVE` ou `SUPERSEDED` dans le [catalogue exhaustif](_index/HOTFIX_REPORT_INDEX.csv).

`WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED` est un statut historique résolu par AE/AF/AG. Le statut courant est `WEST_BENGAL_RETREAT_TRANSFER_EXPECTED` ; les anciens rapports ne sont pas réécrits.

## 9. Conventions de nommage

Les noms `HOTFIX_*` restent inchangés et fournissent l’ordre de phase. Les CSV de manifeste/résultats restent avec leur Markdown compagnon. Les nouveaux documents de navigation utilisent `README.md` ou `INDEX.md`.

## 10. Légende des statuts

`FINAL` = validation finale ; `CURRENT` = référence active ; `INTERMEDIATE` = étape de chaîne ; `SUPERSEDED` = remplacé par un successeur ; `REFERENCE` = contexte ; `FAILED_TEST` = échec historique utile ; `INCONCLUSIVE` = preuve insuffisante ; `BLOCKED` = phase bloquée ; `ARCHIVAL` = conservation administrative.

## 11. Mise à jour HOTFIX-6A.3F du 28 juillet 2026

La correction ciblée DEI est appliquée et passe les contrôles statiques. Le runtime a confirmé la libération indépendante de `CEY` et `SAF`, le passage à `JAV`, la mise à jour du nom `Java` et la suppression des reliquats VOC.

Le test a ensuite justifié deux extensions ciblées et autorisées :

- un drapeau post-VOC propre à Java, séparé de `malaya_subject_var` afin de ne jamais réintroduire le nom `Malaisie` ;
- un événement économique post-compagnie qui remplace `law_extraction_economy` par le traditionalisme, le Mouvement agraire ou un interventionnisme strictement verrouillé par technologie et poids politique.

Rapport courant : [HOTFIX-6A.3F — Correction ciblée DEI](_index/HOTFIX_6A3F_DEI_TARGETED_FIX.md).

Statut final : `HOTFIX_6A3F_DEI_TARGETED_FIX_COMPLETE`. Le drapeau dédié, l’apparition naturelle de l’événement économique et le verrouillage de l’interventionnisme sont confirmés. Le Mouvement agraire, le nom Java et son drapeau persistent après sauvegarde/rechargement. L’option Indonésie et le refus de dissolution sont validés. La description a été développée au format narratif de « Jour de l’indépendance ».

La prise britannique du Cap et de Ceylan pendant que la VOC reste sujette des Pays-Bas n’est pas incluse : elle dépend des lettres de Kew, de la Révolution française et des guerres napoléoniennes, et reste reportée à cette future phase historique.
