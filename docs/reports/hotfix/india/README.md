# Inde — HOTFIX-5

Statut final : `HOTFIX_5_INDIA_COMPLETE`.

## Navigation

- [Vue d’ensemble](00_overview/)
- [East India Company](east_india_company/)
- [Infrastructure et famines](infrastructure_and_famines/)
- [Chaîne Sepoy](sepoy/)
- [States et setup territorial](states_and_setup/)
- [Clôture](closure/HOTFIX_5_INDIA_CLOSURE.md)

## Ordre des grandes phases

Audit Inde → régions/Ryotwari → East India Company unique → références territoriales → Railway/Famines → migration Sepoy → APIs → scénarios fonctionnels A → protections Bengal/Madras/Bombay → radicaux → correction et validation du trigger Bombay → clôture AH.

## Chaîne canonique Sepoy

1. [Audit régional](sepoy/HOTFIX_5C2E_AUDIT_SEPOY_MUTINY_REGIONS.md) et [validation de chargement](sepoy/HOTFIX_5C2E4A_SEPOY_RUNTIME_LOAD_VALIDATION.md).
2. [APIs journal](sepoy/HOTFIX_5C2E4B1_SEPOY_PINNING_API.md) et [personnage](sepoy/HOTFIX_5C2E4B2_SEPOY_CHARACTER_ROLE_API.md), [retest B3](sepoy/HOTFIX_5C2E4B3_SEPOY_API_RUNTIME_RETEST.md).
3. Scénarios A-1 [C1E1](sepoy/HOTFIX_5C2E4C1E1_SEPOY_A1_OBSERVATION_COMPLETION.md), A-2 [C1G](sepoy/HOTFIX_5C2E4C1G_SEPOY_A2_RUNTIME_TEST.md), A-3 [C1I](sepoy/HOTFIX_5C2E4C1I_SEPOY_A3_RUNTIME_TEST.md).
4. Bengal [C1L](sepoy/HOTFIX_5C2E4C1L_B1_BENGAL_CORE_FIX.md) → [C1P](sepoy/HOTFIX_5C2E4C1P_B1_RADICAL_2B_RUNTIME_TEST.md).
5. Madras [C1S](sepoy/HOTFIX_5C2E4C1S_C1_MADRAS_CORE_FIX.md) → [C1T](sepoy/HOTFIX_5C2E4C1T_SEPOY_C1_FIX_RUNTIME_TEST.md).
6. Bombay [C1W](sepoy/HOTFIX_5C2E4C1W_E1_BOMBAY_CORE_FIX.md) → [C1AB](sepoy/HOTFIX_5C2E4C1AB_E1_RADICAL_CLEAN_RERUN.md) → [AE](sepoy/HOTFIX_5C2E4C1AE_E2_BOMBAY_TRIGGER_FIX.md) → [AG](sepoy/HOTFIX_5C2E4C1AG_BOMBAY_TRIGGER_RUNTIME_VALIDATION.md).

## Rapports finaux prioritaires

- [Clôture HOTFIX-5](closure/HOTFIX_5_INDIA_CLOSURE.md)
- [Validation combinée du trigger Bombay](sepoy/HOTFIX_5C2E4C1AG_BOMBAY_TRIGGER_RUNTIME_VALIDATION.md)
- [Validation finale Madras](sepoy/HOTFIX_5C2E4C1T_SEPOY_C1_FIX_RUNTIME_TEST.md)
- [Validation finale Bengal](sepoy/HOTFIX_5C2E4C1P_B1_RADICAL_2B_RUNTIME_TEST.md)
- [Validation propre des radicaux Bombay](sepoy/HOTFIX_5C2E4C1AB_E1_RADICAL_CLEAN_RERUN.md)

## Échecs historiques conservés

C1C (BOM), C1K (noyau Bengal), C1M/C1O (timing radical), C1R (noyau Madras), C1V (noyau Bombay), C1X et C1Z (diagnostic radical) restent disponibles comme preuves ayant conduit aux corrections ultérieures.

## Problèmes résolus

East India Company unique, BIC/Ryotwari, Railway, Famines, chaîne Sepoy, journal et rôles, A-1/A-2/A-3, noyaux Bengal/Madras/Bombay, radicaux, trigger Bombay, COO/JEY, Travancore et préservation MARATH/SAT/KHP sont clos dans le périmètre du hotfix.

`WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED` est résolu. Le comportement courant est `WEST_BENGAL_RETREAT_TRANSFER_EXPECTED`. Aucune protection West Bengal n’est recommandée.

## Hors périmètre

Les diagnostics globaux non liés, NAVY, ADMIN, MARATH hors contrôles de non-régression et `docs/research/technology/` ne font pas partie de cette clôture. Des améliorations futures de l’Inde restent possibles hors du périmètre de merge actuel.
