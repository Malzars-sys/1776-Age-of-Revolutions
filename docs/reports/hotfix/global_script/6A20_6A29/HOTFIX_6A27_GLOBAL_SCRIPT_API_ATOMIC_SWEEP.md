# HOTFIX-6A.27 — Sweep atomique global des six familles d’API script 1.13

Date : 9 août 2026

Branche : `hotfix-dlc-audit`

HEAD d’entrée et de sortie : `eb4e72d756b85220dc96253e0c2d0724ab61c16d`

Mode : correction statique globale, aucun runtime

## 1. Résultat

Les 695 lignes `SAFE_CANDIDATE` du plan 6A.26 ont été appliquées, et elles seules, dans 87 fichiers gameplay. Les 127 lignes `BOUNDED_EXCEPTION` sont restées byte-identiques. Le diff gameplay réel est exactement `695+/695-` ; chaque empreinte finale réelle correspond à l’empreinte théorique du plan, et l’inversion des substitutions restitue les octets d’entrée de chaque fichier.

La source exclusive de vérité était `HOTFIX_6A26_ATOMIC_API_PATCH_PLAN.csv`, au SHA-256 :

```text
D8C6DA5830C38B81348197141258F31BA8B5451E232E4ACD1C11A9FFE4B47466
```

Le détail des 695 occurrences et le résumé par famille sont enregistrés dans [HOTFIX_6A27_GLOBAL_SCRIPT_API_APPLIED_RESULTS.csv](HOTFIX_6A27_GLOBAL_SCRIPT_API_APPLIED_RESULTS.csv).

## 2. Préflight et dry-run

Le dépôt, la branche, le commit manuel 6A.26, l’index vide, le stash NAVY-3C-3 et les sept recherches technologiques non suivies protégées correspondaient aux préconditions. Aucun processus `victoria3.exe`, `dowser.exe` ou Paradox Launcher n’était actif. Les fichiers non suivis protégés n’ont été ni ouverts, ni déplacés, ni modifiés, ni indexés.

Le CSV a été lu avec un parseur CSV réel. Sa colonne de décision est `status`. Le dry-run byte-level intégral a établi avant toute écriture :

```text
SAFE_CANDIDATE rows = 695
unique files = 87
BOUNDED_EXCEPTION rows = 127
THEORETICAL_CHANGED_FILES = 87
THEORETICAL_CHANGED_LINES = 695
THEORETICAL_NUMSTAT = 695+/695-
THEORETICAL_INVERSE_VALIDATION = PASS
OTHER_REQUIRED_HUNKS = 0
```

Pour chaque fichier, le SHA-256 d’entrée, le fragment exact à la ligne planifiée, le SHA-256 final théorique et l’inversion en mémoire ont été vérifiés avant l’écriture atomique.

## 3. Six familles appliquées

| Famille | Substitutions sûres | Exceptions préservées | Fichiers | Objets | Diagnostics runtime ciblés | Statique |
|---|---:|---:|---:|---:|---:|---|
| `API_HAS_ROLE` | 434 | 91 | 61 | 166 | 434 | `PASS` |
| `API_IS_RULER` | 190 | 27 | 47 | 75 | 149 | `PASS` |
| `API_HAS_AMENDMENT` | 12 | 1 | 6 | 10 | 12 | `PASS` |
| `API_IS_HEIR` | 49 | 8 | 19 | 21 | 8 | `PASS` |
| `API_IS_IN_GEOGRAPHIC_REGION` | 4 | 0 | 1 | 4 | 4 | `PASS` |
| `API_ANY_COUNTRY_IN_IBERIA` | 6 | 0 | 1 | 2 | 2 | `PASS` |
| **Total** | **695** | **127** | **87 uniques** | — | **609** | **PASS** |

Les changements sont limités aux six transformations locales prévues : `has_role_of_type`, `is_ruler_of_own_country`, `amendment_type:`, `is_heir_of_own_country` et les deux suffixes Iberia `_old`. Les valeurs, booléens, rôles, scopes, pays, personnages et contenus internes des blocs sont inchangés.

## 4. Validation atomique après écriture

La reconstruction du résultat attendu depuis les octets du HEAD et les 695 lignes du plan est identique byte-for-byte aux 87 fichiers de travail. Elle prouve simultanément l’absence de hunk étranger. Les contrôles donnent :

```text
actual SHA256 after == theoretical SHA256 after = PASS (87/87)
actual diff == planned diff = PASS
inverse(actual) == original = PASS (87/87)
SAFE_LEGACY_OCCURRENCES_BEFORE = 695
SAFE_LEGACY_OCCURRENCES_CORRECTED = 695
SAFE_LEGACY_OCCURRENCES_AFTER = 0
BOUNDED_API_EXCEPTIONS_PRESERVED = 127
BOUNDED_PINNING_EXCEPTIONS_PRESERVED = 14
GAMEPLAY_NUMSTAT = 695+/695-
```

`git diff --check` signale douze lignes de `events/balkans_events/bavarocracy.txt` pour une indentation historique « espace avant tabulation ». Les mêmes octets d’indentation sont présents avant et après sur les douze substitutions planifiées ; seule la propriété API change, et les hashes finaux correspondent au plan. Corriger cette indentation aurait créé des hunks étrangers et invalidé les empreintes autorisées, elle est donc volontairement préservée.

Les 14 exceptions de pinning restent séparées et inchangées ; le bloc global de pinning demeure fermé.

## 5. Protections historiques

Afghanistan reste au SHA-256 fermé `C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13`.

Pologne reste au SHA-256 fermé `A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A`.

BIC conserve exactement `activate_law = law_type:law_frontier_colonization` et aucune restauration de `law_colonial_exploitation` n’a eu lieu dans son fichier pays. Les périmètres pinning, Inde, Sepoy, Bombay, Travancore, NAVY, ADMIN, MARATH, SAT, KHP, Russie, Japon, Mamluk Iraq, DEI/VOC, HBC/Navigation Acts, intérêts déclarés, Égypte, technologie, localisation, metadata et sauvegardes n’ont reçu aucun hunk non autorisé.

## 6. Runtime différé

Aucun jeu, Dowser ou launcher n’a été lancé. La présente phase ne mesure donc aucune disparition de diagnostic. Les seules valeurs runtime sont les cibles de la future QA :

```text
TARGET_RUNTIME_API_DIAGNOSTICS_BEFORE = 609
EXPECTED_TARGET_RUNTIME_API_DIAGNOSTICS_AFTER = 0
CURRENT_BASELINE_TOTAL_DIAGNOSTICS = 1029
EXPECTED_BASELINE_AFTER_6A27Q_IF_NO_OTHER_CHANGE = 420
```

`420` est exclusivement une attente mathématique (`1029 - 609`) ; ce n’est pas un résultat observé. La phase suivante doit être une QA consolidée avec une seule ouverture humaine et doit mesurer la valeur réelle.

## 7. Mesures finales

```text
ATOMIC_API_FAMILIES_APPLIED = 6
SAFE_API_SUBSTITUTIONS_APPLIED = 695
SAFE_API_CHANGED_FILES = 87
BOUNDED_API_EXCEPTIONS_PRESERVED = 127

API_HAS_ROLE_APPLIED = 434
API_IS_RULER_APPLIED = 190
API_HAS_AMENDMENT_APPLIED = 12
API_IS_HEIR_APPLIED = 49
API_IS_IN_GEOGRAPHIC_REGION_APPLIED = 4
API_ANY_COUNTRY_IN_IBERIA_APPLIED = 6

GAMEPLAY_NUMSTAT = 695+/695-

TARGET_RUNTIME_API_DIAGNOSTICS_BEFORE = 609
EXPECTED_TARGET_RUNTIME_API_DIAGNOSTICS_AFTER = 0
EXPECTED_GLOBAL_RESIDUAL_AFTER_RUNTIME = 420
```

## 8. Verdicts

```text
HOTFIX_6A27_GLOBAL_SCRIPT_API_ATOMIC_SWEEP_COMPLETE
GLOBAL_MULTI_API_ATOMIC_SWEEP_STATIC_PASS
GLOBAL_MULTI_API_SIX_FAMILIES_APPLIED
GLOBAL_MULTI_API_SAFE_SUBSTITUTIONS_695_APPLIED
GLOBAL_MULTI_API_CHANGED_FILES_87
GLOBAL_MULTI_API_GAMEPLAY_DIFF_695_PLUS_695_MINUS
GLOBAL_MULTI_API_PATCH_PLAN_SHA256_CONFIRMED
GLOBAL_MULTI_API_BYTE_INVERSION_PASS
GLOBAL_MULTI_API_ONLY_PLANNED_HUNKS_CHANGED
GLOBAL_MULTI_API_BOUNDED_EXCEPTIONS_127_PRESERVED
GLOBAL_PINNING_FAMILY_REMAINS_CLOSED
PINNING_14_BOUNDED_EXCEPTIONS_PRESERVED
AFGHANISTAN_BLOCK_REMAINS_CLOSED
POLAND_BLOCK_REMAINS_CLOSED
BIC_PROTECTIONS_PRESERVED
NON_TARGET_APIS_UNCHANGED
NO_RUNTIME_EXECUTED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_EXECUTION_PHASE = HOTFIX_6A27Q_GLOBAL_SCRIPT_API_ATOMIC_SWEEP_RUNTIME_QA
TARGET_RUNTIME_API_DIAGNOSTICS_BEFORE = 609
EXPECTED_TARGET_RUNTIME_API_DIAGNOSTICS_AFTER = 0
EXPECTED_GLOBAL_RESIDUAL_AFTER_RUNTIME = 420
```
