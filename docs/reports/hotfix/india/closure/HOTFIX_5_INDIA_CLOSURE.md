# HOTFIX-5 — Clôture définitive Inde

## 1. Résumé exécutif

Le périmètre Inde du hotfix courant est fonctionnellement clos. Les validations statiques et runtime canoniques aboutissent au verdict `HOTFIX_5_INDIA_COMPLETE`.

## 2. Périmètre initial

Le périmètre couvre l’East India Company, BIC/Ryotwari, Railway, famines, setup territorial, chaîne Sepoy, retraites régionales, protections des noyaux, radicaux et disponibilité Bombay.

## 3. État Git de clôture

Branche `hotfix-dlc-audit`, base de clôture `6d6db23 Validate Sepoy Bombay trigger at runtime`. La phase AH est documentaire et non commitée.

## 4. East India Company

L’unicité et le comportement institutionnel de l’East India Company sont couverts par les phases 5B1 et 5B2.

## 5. BIC et Ryotwari

La BIC et le dispositif Ryotwari sont inclus dans les audits et corrections territoriales du périmètre Inde.

## 6. Railway

Les régions de l’India Railway ont été corrigées et validées par 5C2C.

## 7. Famines

Les régions, complétions historiques et sélecteurs de famines ont été audités et corrigés par 5C2D à 5C2D3.

## 8. Setup territorial

Les références régionales, le découpage nord/sud, l’Afghanistan, l’Asie centrale et Krakatoa sont documentés par 5A et 5C1–5C2B.

## 9. Chaîne Sepoy

La migration, les présidences, la dissolution générale et les trois retraites régionales ont été testées jusqu’à leur validation finale.

## 10. Journal Sepoy

Le journal, son déclenchement et ses objectifs ont chargé et fonctionné dans les validations runtime.

## 11. APIs corrigées

Les APIs de pinning du journal et de rôle des personnages corrigées en 5C2E4B1/B2 sont validées par 5C2E4B3.

## 12. Scénario A-1

La dissolution générale est validée par 5C2E4C1E/E1, y compris la complétion d’observation propriétaire.

## 13. Scénario A-2

La redistribution sans receveur valide est validée par 5C2E4C1G.

## 14. Scénario A-3

La redistribution à deux receveurs est validée par 5C2E4C1I ; 5C2E4C1I1 nettoie uniquement les infobulles du harnais.

## 15. Retraite Bengal

La retraite Bengal 2.b est validée fonctionnellement par la chaîne 5C2E4C1K–P.

## 16. Retraite Madras

La retraite Madras 2.c est validée par 5C2E4C1T avec le verdict `PASS_C1_FIX_RUNTIME_PARTIAL_UI`.

## 17. Retraite Bombay

La retraite Bombay 2.e est validée territorialement, pour ses effets radicaux et pour sa disponibilité par 5C2E4C1X, AB et AG.

## 18. Protection Bengal

La correction 5C2E4C1L protège le noyau Bengal ; sa conservation runtime est confirmée par 5C2E4C1M.

## 19. Protection Madras

La correction 5C2E4C1S protège le noyau Madras ; sa conservation runtime est confirmée par 5C2E4C1T.

## 20. Protection Bombay

La correction 5C2E4C1W protège le noyau Bombay ; sa conservation runtime est confirmée par 5C2E4C1X.

## 21. Radicaux Bengal

Après les diagnostics N/O, la validation canonique P conclut `PASS_B1_RADICAL_2B_RUNTIME_PARTIAL_UI`.

## 22. Radicaux Madras

Les effets régionaux associés à la retraite Madras sont validés dans la chaîne C1 finale.

## 23. Radicaux Bombay

La relance propre AB confirme les effets radicaux ; l’échec antérieur est classé non reproductible et lié au moment d’observation.

## 24. Trigger Bombay

La correction minimale AE remplace le mauvais test territorial. La validation AG conclut `BOMBAY_TRIGGER_ACCESS_CONFIRMED`.

## 25. Contrôle négatif E-3

Sans Bombay, l’option de retraite vers Bombay reste indisponible. Aucun effet de l’événement n’est appliqué pendant l’inspection.

## 26. Contrôle positif E-2

Avec Bombay et sans portion réelle de West Bengal, l’option Bombay est disponible et sélectionnable.

## 27. Sujets COO et JEY

COO et JEY restent présents et intacts après la validation et le rechargement documentés par AG.

## 28. Travancore

Travancore et `STATE_TRAVANCORE` sont conservés ; aucun correctif supplémentaire n’est requis.

## 29. MARATH/SAT/KHP

Les références et protections MARATH, SAT et KHP sont préservées. Le stash MARATH n’a pas été appliqué ni modifié.

## 30. East Bengal

East Bengal demeure traité conformément aux effets territoriaux attendus de la chaîne Sepoy.

## 31. West Bengal

West Bengal est redistribué par la retraite concernée ; il ne doit pas être protégé artificiellement.

## 32. WEST_BENGAL_RETREAT_TRANSFER_EXPECTED

`WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED` est un statut historique désormais résolu et remplacé par `WEST_BENGAL_RETREAT_TRANSFER_EXPECTED`. Les anciens rapports ne sont pas réécrits.

## 33. Corrections gameplay finales

Les corrections canoniques finales sont celles des APIs B1/B2, des protections Bengal/Madras/Bombay et du trigger Bombay AE.

## 34. Tests runtime finaux

Les validations canoniques sont B3, E1, G, I, P, T, AB et AG, avec leurs CSV compagnons lorsqu’ils existent.

## 35. Rapports intermédiaires et inconclusifs

Les échecs K/R/V/X et les diagnostics N/O/Y/Z sont conservés comme preuves historiques ; les index indiquent leur successeur canonique.

## 36. Problèmes résolus

Sont résolus : APIs obsolètes, redistribution sans receveur, déterminisme à deux receveurs, pertes de noyaux, observation des radicaux et disponibilité Bombay.

## 37. Diagnostics globaux hors périmètre

Les améliorations futures non requises par le merge/hotfix actuel restent possibles, mais ne rouvrent pas cette clôture.

## 38. Fichiers gameplay finaux

Les références gameplay centrales sont `events/india_events/sepoy_mutiny_events.txt` et `common/journal_entries/04_sepoy_mutiny.txt`. AH ne les modifie pas.

## 39. Commits Inde

La chaîne canonique s’achève à `6d6db23`; les commits antérieurs restent traçables dans Git et dans l’index CSV global.

## 40. Intégrité des sauvegardes de test

Aucune sauvegarde n’a été créée, modifiée ou supprimée pendant AH. Les sauvegardes existantes restent des preuves distinctes.

## 41. Intégrité de la copie jetable

Les 984 fichiers ont été inventoriés. Sepoy est identique octet par octet au fork (63 653 octets, SHA-256 `66465CB840A5D7348E342F233205F0389E46E5E1C5ECA97B17870ED09D93C6BB`). Aucun gameplay non fusionné n’a été trouvé. La copie n’est pas supprimée dans AH.

## 42. Absence de correctif restant

`NO_FURTHER_INDIA_GAMEPLAY_FIX_REQUIRED` dans le périmètre du merge/hotfix actuel.

## 43. Éléments futurs optionnels

Une évolution de design, une nouvelle couverture UI ou l’archivage des sauvegardes pourront faire l’objet de phases séparées.

## 44. Verdict

- `HOTFIX_5_INDIA_COMPLETE`
- `NO_FURTHER_INDIA_GAMEPLAY_FIX_REQUIRED`
- `BOMBAY_TRIGGER_ACCESS_CONFIRMED`
- `WEST_BENGAL_RETREAT_TRANSFER_EXPECTED`
- `SEPOY_RUNTIME_VALIDATION_COMPLETE`

## 45. Navigation vers les rapports canoniques

Voir l’[index Inde](../README.md), la [validation Bombay AG](../sepoy/HOTFIX_5C2E4C1AG_BOMBAY_TRIGGER_RUNTIME_VALIDATION.md), la [validation Bengal P](../sepoy/HOTFIX_5C2E4C1P_B1_RADICAL_2B_RUNTIME_TEST.md) et la [validation Madras T](../sepoy/HOTFIX_5C2E4C1T_SEPOY_C1_FIX_RUNTIME_TEST.md).

## 46. Confirmation docs/research/technology/

`docs/research/technology/` est hors bibliothèque hotfix et demeure intact.

## 47. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` demeure intact.
