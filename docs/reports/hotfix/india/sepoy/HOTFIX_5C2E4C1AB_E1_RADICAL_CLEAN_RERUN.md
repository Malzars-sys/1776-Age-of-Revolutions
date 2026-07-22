# HOTFIX-5C2E4C1AB — Rerun runtime propre du diagnostic radical Bombay E1D

## 1. Résumé

Le rerun propre est concluant. `SMALL_BOMBAY`, `LARGE_BOMBAY` direct et l’option réelle 2.e produisent tous un effet radical Bombay matériel, complet à la précision sérialisée et immédiat. Le verdict principal est `C1X_RADICAL_FAILURE_NON_REPRODUCIBLE_OR_TIMING_DEPENDENT`.

## 2. État Git

Racine exacte du fork, branche `hotfix-dlc-audit`, HEAD initial `7a09a11 Prepare clean Sepoy radical rerun`. Aucun fichier suivi n’était modifié. Seul `docs/research/technology/` était non suivi.

## 3. Vérification de la copie

La copie jetable comptait 976 fichiers et 32 harnais, dont quatre E1D et quatre E-1. Aucun `.git`, aucun `remote_file_id` et aucune divergence avec les contrôles non auto-référentiels C1AA. L’empreinte agrégée des 974 fichiers hors scripts E1D est `84951AE24C148E9D9E645942EA3B3342D5F6578F72E8DB6286C930CA6651C266`.

## 4. Vérification des BOM E1D

La décision E1D fait 858 octets, SHA `D0605A942B70B0CABE1159AA296000A4FAA0A5F1D65359C785EE0B638F24A750`. L’événement E1D fait 2 449 octets, SHA `B962465965502A6F4532957EF41EC654072EF28B7EE9A68AE850BD74280E89F8`. Chacun commence par `EF BB BF 23 20 44` et contient exactement un BOM. Les localisations anglaise et française correspondent aussi à C1AA.

## 5. Playset

L’opérateur a confirmé que seule `1776_Age_of_Revolutions_sepoy_test` était active. Fork, autres copies 1776 et versions Workshop étaient désactivés.

## 6. Logs initiaux

| Log | Taille | LastWriteTime | SHA-256 |
|---|---:|---|---|
| error.log | 397 743 | 2026-07-22T15:18:15.3354517+02:00 | `7945FB3ADDC8BF17E6FF99645D84D92F8A6DEBACC3BABBC42A68253FEC9FB44F` |
| game.log | 497 723 | 2026-07-22T15:18:15.3354517+02:00 | `3728DE94966853C29618C3125795C4DB23F990DDD4BA3343B2BDBA733B7551B1` |
| debug.log | 421 908 | 2026-07-22T15:18:24.4734042+02:00 | `E0F01E2B98AB2A685174EAA6AFABE0D41D6A7D52DD541BF64445CFA660EDB695` |

## 7. Fiche opérateur unique

La fiche complète de 51 étapes a été fournie avant lancement. Elle imposait une base commune, SMALL puis LARGE directs, une recharge unique de la base, une branche réelle 2.e propre, les huit noms exacts, aucune branche E1D Bengal et une fermeture finale unique.

## 8. Nombre d’ouvertures, rechargements et fermetures

Une ouverture de Victoria 3, une nouvelle partie BIC, une recharge `RELOAD_1`, aucune session GBR, aucune fermeture intermédiaire et une fermeture finale. Aucun processus Victoria 3, launcher ou dowser ne subsistait avant l’analyse.

## 9. Construction E1D_BASE

La préparation POR → BIC a créé la portion réelle Bombay : state 482, province `39686`, propriétaire BIC (pays 218). La pop hindoue cible 14727 contient 18 963 workforce et 56 889 dependents, soit 75 852 personnes.

## 10. Baseline E-1

L’interface indiquait 0 radical Bombay initialement puis 909 au 3 janvier. `E1D_BASE` sérialise `loyalists_and_radicals=-0.00909`, `radicals_increase=0.01492`, `population_radicals=909` et `trend_radicals=0 0 1240`.

## 11. Branche A SMALL

SMALL ajoute immédiatement son marqueur. La pop passe de `-0.00909` à `-0.01667`, delta `-0.00758`. BIC passe simultanément de `0.01492` à `0.02250`, delta `+0.00758`.

## 12. Branche A LARGE

LARGE ajoute son marqueur à partir de `A_SMALL_TICK1`. La pop passe de `-0.01667` à `-0.09252`, delta incrémental `-0.07585`. BIC passe de `0.03502` à `0.11087`, delta `+0.07585`.

## 13. Recharge unique

La recharge unique a visé `HOTFIX_5C2E4C1AB_E1D_BASE`. Aucun choix E1D n’a ensuite été effectué dans la branche C.

## 14. Sauvegarde C_PRE_2E_CLEAN

`C_PRE_2E_CLEAN` sérialise le 3 janvier à 18 h, contre 00 h pour BASE. Bombay conserve exactement sa pop, son LR, son owner, sa province et ses statistiques radicales de base.

## 15. Barrière anti-contamination

La barrière passe. BASE et C_PRE ne contiennent aucun marqueur SMALL, LARGE ou Bengal, ni la valeur `-11.90044`. Bombay, `radicals_increase`, `population_radicals` et `trend_radicals` sont identiques. La pop West Bengal 14845 conserve 2 705 070 workforce et 8 115 208 dependents ; son LR varie seulement de `0` à `0.00001` pendant le décalage naturel de 18 heures. Les portions BIC Bombay et West Bengal ont les mêmes owners et provinces.

## 16. Branche C 2.e

L’événement réel `sepoy_mutiny_events.2` a été ouvert et l’option 2.e « Bombay tient bon » a été choisie. La boucle s’est terminée et le jeu est resté réactif. L’effet large passe immédiatement de `-0.00909` à `-0.08494`, tandis que BIC passe de `0.01492` à `0.09077`.

## 17. Statut territorial Bombay

`BOMBAY_PRESERVED`. Le state 482, province `39686`, reste BIC immédiatement et après le tick. La pop cible reste à 75 852.

## 18. Statut West Bengal

`WEST_BENGAL_LOST`. Avant 2.e, le state BIC 487 contient `40292` et `40306`. Après 2.e, le state 487 appartient à COO et contient `40292`; la portion BIC est perdue. Ce résultat est séparé du diagnostic radical Bombay.

## 19. Analyse SMALL direct

L’effet attendu pour 75 852 personnes à 1 % est `0.0075852`. L’observé est `0.00758`, ratio `0.999314`. Classement : `FULL_EXPECTED`.

## 20. Analyse LARGE direct

L’effet attendu à 10 % est `0.075852`. L’observé incrémental est `0.07585`, ratio `0.999974`. Classement : `FULL_EXPECTED`.

## 21. Analyse 2.e propre

Depuis C_PRE propre, l’observé est encore `0.07585`, exactement le delta direct LARGE à la précision sérialisée. Classement : `FULL_EXPECTED`.

## 22. Matérialisation immédiate ou différée

Les trois effets apparaissent dans les sauvegardes immédiates. Les checkpoints après tick conservent le LR des pops ; seules les statistiques nationales poursuivent leur évolution quotidienne. `E1_RADICAL_DEFERRED_MATERIALIZATION` est exclu.

## 23. Calculs des deltas

SMALL : `-0.01667 - (-0.00909) = -0.00758`. LARGE direct : `-0.09252 - (-0.01667) = -0.07585`. 2.e : `-0.08494 - (-0.00909) = -0.07585`.

## 24. Ratios observé/attendu

SMALL : `0.00758 / 0.0075852 = 0.999314`. LARGE et 2.e : `0.07585 / 0.075852 = 0.999974`.

## 25. Comparaison delta pop/country

Pour chaque effet immédiat, la valeur absolue du delta pop égale le delta `radicals_increase` BIC à cinq décimales : `0.00758`, `0.07585`, `0.07585`.

## 26. Matrice de conclusion

SMALL direct fonctionne, LARGE direct fonctionne et 2.e propre fonctionne. La première ligne de la matrice s’applique : `C1X_RADICAL_FAILURE_NON_REPRODUCIBLE_OR_TIMING_DEPENDENT`.

## 27. Cause racine ou limite de preuve

Le défaut C1X ne se reproduit pas ici. Les preuves ne permettent pas de départager non-reproductibilité et dépendance au timing. Aucun `ROOT_CAUSE_*_PROVEN` n’est justifié.

## 28. Logs ciblés

Après fermeture : error.log 46 004 octets/SHA `8C09498A630BDCCA528AB6B4B13D22B980FDBED8EAEF22E09C1D8E3E73C307E7`; game.log 379 509/SHA `905FD8FE09BEEEA8490DFA678F0B74CCEA5381AC58312D13D8CAFEA670F80132`; debug.log 492 554/SHA `4CDFAE4367FB186AE3BBE8F8D6FE1D9F9935467E9E006217999220C7B9F747CB`. Les recherches prescrites donnent zéro correspondance E1D/E-1/2.e/STATE_BOMBAY/STATE_WEST_BENGAL/x51F0A0/effets/tooltip et zéro avertissement BOM E1D.

## 29. Diagnostics hors périmètre

4 037 correspondances génériques concernent notamment `PostValidate`, `Unexpected token`, `Invalid right side` et `Script system error`. Les contextes représentatifs pointent vers `01_natural_borders_of_france.txt` et `07_american_mod_jes.txt`, pas vers Sepoy ou E1D. Les 16 avertissements BOM concernent d’autres fichiers.

## 30. Intégrité des sauvegardes

Les huit originaux exacts sont présents. Rakaly 0.8.18 a fondu uniquement des copies temporaires avec `melt --format vic3 --unknown-key stringify`. Le dossier temporaire a été supprimé. Les huit tailles et SHA-256 originaux sont inchangés après analyse; ils figurent dans le CSV.

## 31. Intégrité des fichiers

Après runtime : 976 fichiers, 32 harnais, zéro divergence avec le manifeste C1AA. Sepoy fork/copie reste à 63 658 octets et SHA `51F489F00FA6CB2D7BBF1D1FDC587104F2A17D4932187DAA8BBE954F7312A9FB`.

## 32. Verdict

Verdict principal : `C1X_RADICAL_FAILURE_NON_REPRODUCIBLE_OR_TIMING_DEPENDENT`.

Verdicts séparés : `BOMBAY_PRESERVED`, `WEST_BENGAL_LOST`, `WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED`.

## 33. Correction éventuellement recommandée

Aucune correction radicale supplémentaire n’est recommandée sur cette preuve. La fonctionnalité West Bengal reste une décision distincte et différée.

## 34. Fichiers créés

- `docs/reports/hotfix/HOTFIX_5C2E4C1AB_E1_RADICAL_CLEAN_RERUN.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1AB_E1_RADICAL_CLEAN_RESULTS.csv`

## 35. Gameplay inchangé

Aucun gameplay, harnais, fichier de localisation, descripteur ou sauvegarde originale n’a été modifié.

## 36. WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED

La perte West Bengal est documentée mais n’invalide pas le diagnostic radical Bombay. Son intention fonctionnelle doit être tranchée dans une phase séparée.

## 37. Confirmation docs/research/technology/

`docs/research/technology/` est resté non suivi et intact.

## 38. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est resté intact.
