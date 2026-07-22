# HOTFIX-5C2E4C1Z — Diagnostic runtime différentiel E1D

## 1. Résumé

Verdict : `INCONCLUSIVE_E1_RADICAL_DIAGNOSTIC`, avec `WEST_BENGAL_LOST` et `WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED`.

Le contrôle direct `SMALL_BOMBAY` a produit immédiatement un signal matériel (`-0,00909` → `-0,01742`, delta `-0,00833`). Le contrôle West Bengal a chargé et exécuté les deux script values avec des effets matériels immédiats. L’option réelle 2.e a conservé Bombay et sa pop hindoue, et cette pop porte un delta immédiat de `-0,07585`. Ces résultats réfutent un échec général du harnais et montrent que Bombay peut recevoir des radicaux.

La session ne permet toutefois pas une conclusion causale : le contrôle direct `LARGE_BOMBAY` n’a pas été exécuté/sauvegardé, trois sauvegardes sont mal nommées, et la branche C conserve dans ses pops West Bengal l’empreinte exacte du contrôle `LARGE_WEST_BENGAL`. La branche C n’est donc pas issue de la base radicale commune annoncée. Aucun verdict `ROOT_CAUSE_*_PROVEN` n’est soutenu.

## 2. État Git

- Racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD avant création des livrables : `c579c2a Prepare Sepoy Bombay radical diagnostics`.
- Avant runtime, aucun fichier suivi modifié ; seule exception non suivie : `docs/research/technology/`.
- Aucun commit n’a été créé.

## 3. Vérification de la copie

La copie jetable contenait 976 fichiers, 32 fichiers `zz_*`, aucun `.git` et aucun `remote_file_id`. Les 39 lignes non auto-référentielles du manifeste C1Y passent encore après la session. Le Sepoy fork/copie est identique : 63 658 octets, SHA-256 `51F489F00FA6CB2D7BBF1D1FDC587104F2A17D4932187DAA8BBE954F7312A9FB`.

## 4. Playset

L’opérateur a confirmé que seule `1776_Age_of_Revolutions_sepoy_test` était active ; fork principal, autres copies 1776 et versions Workshop étaient désactivés.

## 5. Logs initiaux

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 324440 | 2026-07-21T23:30:37.9841594Z | `14725DCE6515FC3A7C8B43EA30021B4C57B955FDC1E92289A724D81BEA2E997D` |
| `game.log` | 191242 | 2026-07-21T23:30:37.9841594Z | `F4587717F7EA33A635A3A336298495BD366432614324E6CDAED9DED11DD` |
| `debug.log` | 351372 | 2026-07-21T23:30:44.4122355Z | `3E87919DD475E31F249A0FCEB11327BC2EA81519B374CAC0A9FE3B6CD8B6F9EC` |

## 6. Fiche opérateur unique

La fiche A–C a été fournie avant le lancement : construction d’une base E-1, branche A Bombay directe, `RELOAD_1`, branche B West Bengal, `RELOAD_2`, branche C événement réel 2.e, sauvegardes immédiates/tick et fermeture finale. L’exécution réelle s’en écarte comme documenté aux sections 10 à 14.

## 7. Nombre d’ouvertures, rechargements et fermetures

Compte opérateur : une ouverture, une nouvelle partie BIC, deux rechargements, aucune fermeture intermédiaire et une fermeture finale. Après la fermeture, aucun processus Victoria 3/launcher n’était actif.

## 8. Construction de E1D_BASE

La préparation E-1 a transféré x51F0A0/39686 de POR à BIC. La sauvegarde `HOTFIX_5C2E4C1Z_E1D_BASE.v3` est datée `1776.1.3.12`, conserve les states BIC `14 462 486 487 494 504 1034 482`, et contient `zz_sepoy_test_e1_ready`.

Bombay : state ID 482, owner BIC (country object 218), une pop hindoue active de 75 852 personnes (`workforce=18963`, `dependents=56889`, `location=482`). West Bengal : state ID 487, owner BIC, 44 pops hindoues actives, 12 515 881 personnes.

## 9. Baseline de préparation E-1

UI : zéro radical le 1er janvier, zéro le 2 janvier, puis environ 1,23 K BIC et 909 à Bombay le 3 janvier. La sauvegarde profonde du 3 janvier contient `population_radicals=1234`, `radicals_increase=0.01474` et, pour la pop Bombay, `loyalists_and_radicals=-0.00909`. La baseline E-1 s’est donc matérialisée au second tick quotidien.

## 10. Branche A — small Bombay

`A_BOMBAY_SMALL_IMMEDIATE` contient le marqueur `zz_sepoy_test_e1d_small_bombay_done`. La pop cible passe immédiatement de `-0.00909` à `-0.01742`; le delta est `-0.00833`. `radicals_increase` passe de `0.01474` à `0.02307`, également `+0.00833`. L’effet est `PARTIAL_BUT_MATERIAL`, ratio observé/attendu `0.833`.

La sauvegarde appelée `A_BOMBAY_LARGE_TICK1` est en réalité le tick de SMALL : elle ne contient que le marqueur small et garde `-0.01742`. Elle est datée `1776.1.4.18`.

## 11. Branche A — large Bombay

Non testée. `A_BOMBAY_LARGE_IMMEDIATE` est absente et aucune sauvegarde A ne contient `zz_sepoy_test_e1d_large_bombay_done`. Le fichier nommé `A_BOMBAY_LARGE_TICK1` ne constitue pas une preuve large. Classement : `NOT_APPLICABLE` / `MISSING_TEST`.

## 12. Branche B — small West Bengal

Effet immédiat et matériel. La somme des champs `loyalists_and_radicals` des 44 pops hindoues actives passe de `-0.00301` à `-1.25482`; l’estimation pondérée des radicaux augmente d’environ 11 721 394. `radicals_increase` passe de `0.01474` à `1.32206`. Le marqueur small est présent.

Le fichier nommé `B_BENGAL_LARGE_TICK1` est le tick de SMALL : seul le marqueur small est présent. Sa date `1776.1.5` diverge aussi du tick quotidien nominal attendu après `1776.1.3.12`.

## 13. Branche B — large West Bengal

`B_BENGAL_LARGE_IMMEDIATE` contient les marqueurs small et large. Depuis le checkpoint small tick, la somme des fractions passe de `-1.25536` à `-13.77420`; l’incrément pondéré est d’environ 117 214 943 radicaux. `radicals_increase` passe de `1.37194` à `14.44619`. Le contrôle large est matériel et immédiat.

Le tick large a été sauvegardé sous `B_BENGAL_SMALL_TICK.v3` : date `1776.1.6.18`, somme `-13.77435`, `radicals_increase=14.45374`. Les deux noms de tick Bengal sont inversés.

## 14. Branche C — 2.e

L’événement réel `sepoy_mutiny_events.2` a été ouvert et l’option 2.e « Bombay tient bon » choisie. La boucle s’est terminée, BIC est restée jouée et Bombay state 482 est resté BIC, réel et non vide. Les states BIC sauvegardés deviennent `504 482` : West Bengal est perdu. La pop Bombay reste 75 852 et passe à `loyalists_and_radicals=-0.08494`.

Mais la branche est contaminée : la pop West Bengal 14845 porte `-11.90044` dans `C_2E_IMMEDIATE`, valeur identique à `B_BENGAL_LARGE_IMMEDIATE`. La base E1D avait zéro champ sérialisé pour cette pop. Ce résidu prouve que `RELOAD_2` n’a pas restauré la base radicale commune, même si l’état territorial affiché avant l’option paraissait nominal.

## 15. Comparaison immédiat/tick

| Chemin | Immédiat | Tick | Classe |
|---|---:|---:|---|
| A small Bombay, pop | `-0.01742` | `-0.01742` | immédiat matériel |
| B small, somme | `-1.25482` | `-1.25536` | immédiat matériel |
| B large, somme | `-13.77420` | `-13.77435` | immédiat matériel |
| C 2.e Bombay, pop | `-0.08494` | `-0.08494` | immédiat matériel, branche contaminée |

Aucun des effets ciblés observés n’attend le tick suivant pour se matérialiser.

## 16. Analyse Bombay

Le ciblage direct Bombay n’est pas intrinsèquement nul : SMALL fonctionne immédiatement sur l’unique pop hindoue. L’événement réel 2.e laisse aussi un signal Bombay matériel. Le test direct LARGE manque, empêchant de comparer exactement le même script value au chemin 2.e.

## 17. Analyse West Bengal contrôle

Les deux contrôles sont positifs et prouvent le chargement du harnais, la résolution de `very_small_radicals`/`large_radicals` et l’activité de `add_radicals_in_state`. Leur magnitude est très supérieure à la fraction théorique simple, probablement parce que l’effet state-wide est invoqué dans une portée répétée par pop ; ce comportement n’est pas corrigé dans C1Z.

## 18. Analyse 2.e

Par comparaison numérique avec E1D_BASE, Bombay présente un delta de `-0.07585`, proche du signal large attendu `0.0759`, et `radicals_increase` augmente aussi de `0.07585`. Cela constitue une preuve positive que le chemin 2.e peut produire un effet Bombay. Ce n’est pas une preuve différentielle propre, car la branche C n’a pas la base West Bengal attendue et aucun checkpoint pré-option C n’a été sauvegardé.

## 19. Calculs des deltas

- A small : `-0.01742 - (-0.00909) = -0.00833`; country `0.02307 - 0.01474 = 0.00833`.
- B small immédiat : somme `-1.25482 - (-0.00301) = -1.25181`; country `1.32206 - 0.01474 = 1.30732`.
- B large incrémental : somme `-13.77420 - (-1.25536) = -12.51884`; country `14.44619 - 1.37194 = 13.07425`.
- C 2.e : `-0.08494 - (-0.00909) = -0.07585`; country apparent `0.09059 - 0.01474 = 0.07585`.

Les égalités pop/country sont exactes à cinq décimales pour A small et pour la comparaison apparente C ; elles ne le sont pas pour le contrôle multi-pop Bengal.

## 20. Ratios observé/attendu

- A small : `0.00833 / 0.01 = 0.833`.
- C 2.e : `0.07585 / 0.10 = 0.7585`.
- B small, estimation pondérée : `11 721 393,53 / 125 158,81 ≈ 93,652`.
- B large incrémental : `117 214 943,06 / 1 251 587,7 ≈ 93,652`.

Les deux ratios Bengal montrent un contrôle positif sur-amplifié, pas un zéro ou un plancher d’une personne.

## 21. Matrice de causalité

- Cas 6 (Bombay et Bengal directs échouent) : exclu, car A small et B fonctionnent.
- Cas 7 (effets seulement après tick) : exclu pour les effets observés.
- Cas 3 (small échoue, large fonctionne) : exclu pour small, mais large direct manque.
- Cas 1, 2, 4 et 5 : non décidables proprement en raison de LARGE_BOMBAY absent et de C contaminée.

## 22. Hypothèses exclues

Échec total de chargement E1D, script values non résolues, `add_radicals_in_state` globalement inactif, effet Bombay limité à `0.00001`, et matérialisation exclusivement différée.

## 23. Hypothèses restantes

Résultat C1X non reproductible, différence de timing post-transfert, particularité du chemin 2.e dans certaines séquences, ou contamination/rechargement opérateur. La session actuelle ne départage pas ces explications.

## 24. Cause racine ou limite de preuve

Limite de preuve : protocole différentiel incomplet et base C non commune. Aucune cause racine n’est déclarée. Le signal C positif ne peut pas être promu en `C1X_RADICAL_FAILURE_NON_REPRODUCIBLE` sans une branche C propre et un contrôle LARGE_BOMBAY direct.

## 25. Statut territorial Bombay

`BOMBAY_PRESERVED`. State ID 482 et province x51F0A0/39686 restent à BIC après 2.e ; la pop hindoue cible conserve location, workforce et dependents.

## 26. Statut West Bengal

`WEST_BENGAL_LOST`. Après 2.e, le state 487 n’apparaît plus dans la liste des states BIC. Cette perte correspond au comportement territorial observé pour l’option, mais elle est relevée séparément du diagnostic radical.

## 27. WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED

Conservé tel qu’exigé. C1Z ne décide pas si West Bengal doit être un noyau protégé ni si sa perte doit être corrigée.

## 28. Logs ciblés

Zéro occurrence de `Invalid scope`, `STATE_BOMBAY`, `STATE_WEST_BENGAL`, `x51F0A0`, `add_radicals_in_state`, des script values, de l’événement 2.e, des tooltips ciblés ou d’une boucle non terminée. Deux avertissements directs E1D existent néanmoins dans `debug.log` :

- ligne 1952 : `events/zz_sepoy_radical_diagnostic_e1d_events.txt should be in utf8-bom encoding` ;
- ligne 2182 : `common/decisions/zz_sepoy_radical_diagnostic_e1d.txt should be in utf8-bom encoding`.

L’exigence « zéro diagnostic BOM E1D » échoue. Le moteur indique qu’il essaie malgré tout de charger les fichiers, ce que confirment marqueurs et effets. Aucun fichier n’a été corrigé pendant C1Z.

Logs finaux : `error.log` 397743 octets, SHA `7945FB3ADDC8BF17E6FF99645D84D92F8A6DEBACC3BABBC42A68253FEC9FB44F`; `game.log` 497723, SHA `3728DE94966853C29618C3125795C4DB23F990DDD4BA3343B2BDBA733B7551B1`; `debug.log` 421908, SHA `E0F01E2B98AB2A685174EAA6AFABE0D41D6A7D52DD541BF64445CFA660EDB695`.

## 29. Diagnostics hors périmètre

Diagnostics globaux non reliés directement à E1D : `Invalid right side` 3506, `Script system error` 3744, `PostValidate` 677, `Unexpected token` 427, avertissements BOM globaux 18. Ils sont classés hors périmètre sauf les deux lignes E1D détaillées ci-dessus.

## 30. Intégrité des sauvegardes

Rakaly 0.8.18 a fondu uniquement des copies temporaires avec `--unknown-key stringify`. Les copies, fontes, archive et binaire temporaires ont été supprimés. Les neuf originaux ont été rehashés après suppression et sont inchangés.

| Sauvegarde originale | Date sérialisée | SHA-256 |
|---|---|---|
| `E1D_BASE` | 1776.1.3.12 | `D388423B2A097B806443F892EC3135AE3E97E747766F4828D9E98C1F7B87F472` |
| `A_BOMBAY_SMALL_IMMEDIATE` | 1776.1.3.12 | `826E7EAAF97FBE9257BC0DD3FCC6115FE28E311D992CE5161E30D9E01558C4B4` |
| `A_BOMBAY_LARGE_TICK1` (small tick réel) | 1776.1.4.18 | `B512D74605056FAD0C409330CF43C793CC93BE811F315F766E651CBC5A23C1F6` |
| `B_BENGAL_SMALL_IMMEDIATE` | 1776.1.3.12 | `DC7B6588558A0F349A20ABD3E660E00E09D9A3485A5FAB70C5DD4B09D8AF359C` |
| `B_BENGAL_LARGE_TICK1` (small tick réel) | 1776.1.5 | `53D57F3BAEF78976601ABE937DBBEDCD8DACFF05228ACBE2F5046E8D9B6E538D` |
| `B_BENGAL_LARGE_IMMEDIATE` | 1776.1.5 | `A8F16972C9F7D9A830D50FCB839200A758A1F9158176F9085AB64897EDA4B20B` |
| `B_BENGAL_SMALL_TICK` (large tick réel) | 1776.1.6.18 | `021202FC637D53D04442DE58B8A2555ADAA9AE5F72290D5EFC5EFD36605A6854` |
| `C_2E_IMMEDIATE` | 1776.1.3.12 | `00B92D431B4446E6A5EF85D45EC438EDC7CCE0F0B1BFE2451622F0E71F898B0F` |
| `C_2E_TICK1` | 1776.1.4.18 | `0E3EF8D75B12DB33456E0B0834277D3C3592934F348F2A3E061C300995803778` |

Il manque les deux checkpoints LARGE_BOMBAY attendus ; le fichier A portant le nom large est le tick small. Les deux ticks Bengal sont inversés, comme signalé par l’opérateur et confirmé par les marqueurs.

## 31. Intégrité des fichiers

Après session : 976 fichiers dans la copie, 32 harnais, zéro `.git`, zéro `remote_file_id`, 39/39 contrôles non auto-référentiels C1Y conformes, journal/descripteurs/marqueur conformes et Sepoy inchangé. Aucun original de sauvegarde n’a été modifié.

## 32. Verdict

`INCONCLUSIVE_E1_RADICAL_DIAGNOSTIC`

Qualificatifs : `WEST_BENGAL_LOST`, `WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED`, `BOMBAY_PRESERVED`, `E1D_BOM_WARNING_PRESENT`, `BRANCH_A_LARGE_MISSING`, `BRANCH_C_BASE_CONTAMINATED`.

## 33. Correction éventuellement recommandée

Aucune correction gameplay n’est recommandée sur la base de C1Z. Phase suivante distincte : corriger uniquement l’encodage BOM du harnais si autorisé, puis refaire depuis E1D_BASE une branche A LARGE_BOMBAY complète et une branche C précédée d’un checkpoint pré-option fondu. Vérifier avant 2.e que la pop West Bengal 14845 ne porte pas `-11.90044`.

## 34. Fichiers créés

- `docs/reports/hotfix/HOTFIX_5C2E4C1Z_E1_RADICAL_DIAGNOSTIC_RUNTIME.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1Z_E1_RADICAL_DIAGNOSTIC_RESULTS.csv`

## 35. Confirmation gameplay inchangé

Aucun gameplay, harnais, fichier de localisation, protection territoriale, trigger West Bengal, donnée MARATH ou sauvegarde originale n’a été modifié.

## 36. Confirmation docs/research/technology/

Le répertoire non suivi `docs/research/technology/` n’a pas été touché.

## 37. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est resté intact.
