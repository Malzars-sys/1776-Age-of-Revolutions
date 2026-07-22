# HOTFIX-5C2E4C1T — Validation runtime finale du noyau Madras de l’option 2.c

## 1. Résumé

Le test C-1 corrigé a été exécuté dans une seule session BIC avec la seule copie jetable active. La préparation transfère `xABADB1` de FRA à BIC. Après sélection manuelle exclusive de `sepoy_mutiny_events.2.c`, la boucle termine et BIC conserve réellement la province dans le region state 473. PUD reste à 24 provinces, DENNOR conserve `x10B060`, BIC reste le pays joué et COO/JEY deviennent indépendants.

La preuve profonde est immédiate : la somme `loyalists_and_radicals` des pops hindoues et sunnites de Madras BIC passe de `-0.02425` à `-0.24683`, delta `-0.22258`, exactement égal à la hausse de `radicals_increase` BIC, de `0.03263` à `0.25521`. `population_radicals`, `trend_radicals` et l’UI restent à leur baseline. Verdict : **PASS_C1_FIX_RUNTIME_PARTIAL_UI**.

## 2. État Git initial

- racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork` ;
- branche : `hotfix-dlc-audit` ;
- HEAD : `4d6fc36 Protect Sepoy Madras retreat core` ;
- aucun fichier suivi modifié ;
- seule exception non suivie : `docs/research/technology/` ;
- stash : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

## 3. Exception `docs/research/technology/`

Les sept fichiers non suivis préexistants sous `docs/research/technology/` n’ont été ni modifiés, ni inclus dans le runtime, ni inclus dans les livrables C1T.

## 4. Vérification de la copie

Avant lancement, la copie contenait exactement 968 fichiers, 24 fichiers de harnais et quatre fichiers C-1. Elle ne contenait aucun dossier `.git` ni aucune occurrence de `remote_file_id`. Les 31 contrôles applicables du manifeste C1S ont été recalculés sans divergence. Le fichier Sepoy fork/copie faisait 63 540 octets, SHA-256 `98C4A50C1DCF2CE79B13AFF82B1FE461651BB99A9B42B002914FD10C338FDCAD`, avec identité octet par octet.

## 5. Playset

Avant lancement, l’opérateur a confirmé en une fois que seule `1776_Age_of_Revolutions_sepoy_test` était active, que le fork principal, les autres copies 1776 et les versions Workshop étaient désactivés. La barrière `BLOCKED_DUPLICATE_MODS_ENABLED` n’a pas été déclenchée.

## 6. Logs avant session

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 218 015 | 2026-07-20 02:36:44.1232101 | `7BD91DE2CDED3CE40F77048CF538DC1967C3A4EE943E120115912F523013B43B` |
| `game.log` | 174 530 | 2026-07-20 02:36:44.1232101 | `C2475C35FA1E9FC85493C361B4611C39A2B608EBC2F24E6235066A0FC2850B37` |
| `debug.log` | 330 884 | 2026-07-20 02:37:00.0416762 | `C243039C82592A2867422CC00F2DB04B5C404395D909D77F4B6686987F6843BB` |

Aucun log n’a été supprimé, déplacé ou renommé.

## 7. Fiche opérateur unique

La fiche complète a été fournie avant lancement dans un seul message. Elle couvrait l’unique ouverture, la nouvelle partie BIC, l’état initial des trois portions Madras, la préparation, les checkpoints des 1er/2/3 janvier, la sauvegarde pré-2.c immuable, l’ouverture manuelle de l’événement, le choix exclusif de 2.c, les contrôles immédiats, les checkpoints des 4/5 janvier, les trois sauvegardes distinctes et l’unique fermeture finale. Aucune nouvelle branche de test n’a été ajoutée pendant la session.

## 8. Nombre réel d’ouvertures et fermetures

L’opérateur rapporte une seule session et une fermeture finale. Les trois sauvegardes partagent le `playthrough_id` `b5087862-8e19-4812-a65b-295c039b769b`, sont chronologiquement continues, et passent du tick 10 au tick 18. Après le compte rendu, aucun processus `victoria`, `victoria3` ou `dowser` n’était actif. Aucune session GBR, relance, ancienne sauvegarde, commande console ou fermeture intermédiaire n’a été rapportée.

## 9. État initial Madras

La capture initiale du 1er janvier montre un Carnatic partagé entre Carnatic français/FRA, Carnatic dano-norvégien/DENNOR et Tamil Nadu/PUD, sans portion BIC. Le scénario attendu est donc présent : `xABADB1` à FRA, `x10B060` à DENNOR et les 24 autres provinces à PUD.

## 10. Préparation FRA → BIC

Après l’option explicite de préparation C-1, l’UI montre « Carnatic indien » sous la Compagnie des Indes orientales. La sauvegarde pré-2.c confirme `39618`, correspondant à `xABADB1`, dans le state 473, `country=218` BIC, avec `capital=39618` et la liste de provinces `39618 0`.

## 11. Absence d’autre mutation

L’opérateur rapporte que tous les transferts d’état sont nominaux. DENNOR et PUD restent distincts ; aucune autre portion Madras, mutation territoriale ou mutation diplomatique ne survient pendant la préparation ; aucun événement Sepoy réel ne s’ouvre automatiquement.

## 12. Tick 0

La portion BIC compte environ 230 K habitants : 182,2 K hindous, 20,1 K sunnites et 28,2 K catholiques. Le compteur visible reste initialement nul, résultat autorisé par le protocole.

## 13. Premier tick

La capture du 2 janvier montre la portion Madras toujours BIC avec les mêmes ordres de grandeur démographiques. Aucun échec n’est prononcé sur l’état encore nul ou non rafraîchi de l’UI radicale.

## 14. Second tick

La capture du 3 janvier confirme la date exacte et affiche environ 2,80 K radicaux nationaux. La portion BIC reste réelle, peuplée et détenue par BIC. La sauvegarde sérialise `population_radicals=2426` dans le state 473 et `population_radicals=2808` au niveau national BIC.

## 15. Sauvegarde pré-2.c

`HOTFIX_5C2E4C1T_C1_FIX_PRE_2C_1776_01_03.v3` :

- date sérialisée : `1776.1.3.6` ;
- tick : 10 ;
- taille : 8 263 309 octets ;
- LastWriteTime UTC : 2026-07-20 04:52:59.5304337 ;
- SHA-256 : `24F3ABA83FD3B3282B6A80259B6BD882E9196150CB8F9052EE236766FA903636`.

Le nom et la date sérialisée concordent ; aucun `SAVE_DATE_MISMATCH`.

## 16. Baseline radicale profonde

Le state 473 contient avant 2.c six objets de pops hindoues, population totale 182 284, somme `loyalists_and_radicals=-0.02185`, et un objet sunnite, population 20 098, valeur `-0.00240`. Le total ciblé vaut `-0.02425`. Cette valeur correspond au signal profond C-1 attendu et coexiste avec `population_radicals=2426`, `trend_radicals={ 0 0 2808 }` et `radicals_increase=0.03263` pour BIC. La baseline est validée.

## 17. Ouverture manuelle de l’événement

La décision C-1 ouvre manuellement `sepoy_mutiny_events.2`, « Le coup de grâce », sur BIC. La capture montre les quatre options attendues.

## 18. Sélection exclusive de 2.c

L’option « La domination de la Compagnie continuera au sud. Retournez à Madras. » est disponible. Son tooltip reconnaît Carnatic indien et annonce `+10.0 %` pour les religions hindoue et sunnite. L’opérateur a sélectionné cette option uniquement.

## 19. Terminaison de la boucle

L’événement se ferme, le jeu reste réactif, la redistribution s’achève et les deux sauvegardes postérieures sont écrites. Aucun crash, blocage ou symptôme de boucle non terminée. **PASS LOOP**.

## 20. Pays joué final

Les trois sauvegardes portent le nom « Compagnie des Indes orientales » et `previous_played.idtype=218`. BIC reste donc le pays joué. Après 2.c, ses states sérialisés sont 504 et 473 : son noyau Madras est bien un territoire réel, pas seulement une revendication.

## 21. `xABADB1` après 2.c

Dans les sauvegardes immédiate et finale, la province interne 39618 reste mappée vers le state 473. Ce state appartient à `country=218` BIC. `xABADB1` ne passe ni à PUD ni à un autre owner. Les données ne portent pas de controller distinct contradictoire ; le controller effectif suit l’owner BIC. **PASS territorial**.

## 22. Region state BIC après 2.c

Le state 473 conserve `capital=39618`, `country=218`, `region="STATE_MADRAS"` et `provinces={ 39618 0 }` dans les trois sauvegardes. Il n’est jamais vide. Sa population est de 230 605 avant et immédiatement après 2.c, puis 230 591 au 5 janvier par faible évolution démographique.

## 23. PUD après 2.c

Le state 475 reste `country=415` PUD avec `capital=39622`. Son encodage de provinces reste strictement `39599 13 39614 3 39619 5`, le même ensemble de 24 provinces qu’avant 2.c et que dans C1R avant le transfert défectueux. Il n’inclut pas 39618. PUD n’absorbe pas Pondichéry.

## 24. DENNOR après 2.c

Le state 474 reste `country=745`, `previous_country=745`, `capital=39613`, avec la seule province `39613 0`, correspondant à `x10B060`. La capture finale montre également Carnatic dano-norvégien distinct. DENNOR est inchangé.

## 25. Statut COO

La notification UI indique que Cooch Behar quitte le bloc britannique. L’objet pays 412 sérialise `definition="COO"` immédiatement après l’événement, `states={ 488 14 }` et `power_bloc_leave_date=1776.1.3.6`. L’UI montre son propre marché et aucun traité actif. COO est indépendant comme attendu. La définition dynamique courante devient `BGL` au 5 janvier sans remettre en cause l’identité de l’objet 412 ni sa date de sortie.

## 26. Statut JEY

L’objet pays 428, `definition="JEY"`, conserve le state 463 et reçoit `power_bloc_leave_date=1776.1.3.6`. L’UI montre « Pays du marché jeypore » et aucun traité actif. JEY est indépendant comme attendu.

## 27. Owners nuls ou incohérents

Les trois portions Madras observées ont chacune un owner non nul et unique : state 473/BIC, 474/DENNOR et 475/PUD. Les mappings 39618→473 et 39613→474 sont stables. L’opérateur n’observe aucune double attribution, et aucune fusion artificielle n’apparaît dans les sauvegardes. Aucun `FAIL_C1_FIX_INVALID_TRANSFER`.

## 28. Résultat radical immédiat

Immédiatement après 2.c :

| Signal | Pré-2.c | Post immédiat | Delta |
|---|---:|---:|---:|
| somme hindoue `loyalists_and_radicals` | -0.02185 | -0.22234 | -0.20049 |
| somme sunnite | -0.00240 | -0.02449 | -0.02209 |
| total ciblé | -0.02425 | -0.24683 | **-0.22258** |
| `radicals_increase` BIC | 0.03263 | 0.25521 | **+0.22258** |

L’égalité exacte des deltas profonds prouve l’exécution immédiate de `large_radicals` sur les pops hindoues et sunnites du state 473 BIC. **PASS_RADICALS_DEEP**.

## 29. Premier tick après 2.c

La capture du 4 janvier montre BIC toujours joué, la portion Madras conservée et le tooltip à 2 426 radicaux. Aucun changement territorial supplémentaire ni perte de réactivité n’est rapporté.

## 30. Second tick après 2.c

La sauvegarde finale est datée `1776.1.5.6`, tick 18. Le state 473 reste BIC et non vide, PUD reste à 24 provinces, DENNOR conserve 39613. `population_radicals` reste 2 426 dans le state et 2 808 au niveau national ; le signal profond reste présent.

## 31. Analyse des pops hindoues

Les six objets hindous sont les mêmes avant et immédiatement après 2.c. Leur population totale reste 182 284. Leurs valeurs groupées passent de `-0.02185` à `-0.22234`, puis `-0.22235` au 5 janvier. Les six objets sont dans `location=473`, donc exactement dans la portion Madras BIC protégée.

## 32. Analyse des pops sunnites

L’objet sunnite 14558 reste dans `location=473`, population 20 098. Sa valeur passe de `-0.00240` à `-0.02449` immédiatement et reste `-0.02449` au 5 janvier. Le scope religieux sunnite est donc validé.

## 33. `Radicals increase`

Le signal BIC passe immédiatement de `0.03263` à `0.25521`, soit `+0.22258`, puis atteint `0.25808` au 5 janvier avec de faibles évolutions générales. Le delta immédiat est exactement l’opposé du delta groupé des objets de pops ciblés, à cinq décimales.

## 34. `Loyalists and radicals`

Le total hindou+sunnite passe immédiatement de `-0.02425` à `-0.24683`, puis `-0.24684`. Les objets catholiques ne participent pas à ce delta C-1 : leur somme reste `-0.00029` entre pré-2.c et post immédiat. Il n’existe donc aucun `FAIL_C1_FIX_RADICAL_SCOPE`.

## 35. Comparaison UI

L’UI montre environ 2,80 K radicaux nationaux au 3 janvier et 2 426 sur la portion Madras BIC après 2.c et au 4 janvier. Elle confirme le maintien territorial mais ne reflète pas la hausse additionnelle de 10 %, exactement comme le comportement d’agrégats retardés déjà documenté par C1P.

## 36. Comparaison sérialisée

| Champ | Pré-2.c | Post immédiat | 5 janvier |
|---|---:|---:|---:|
| date / tick | 1776.1.3.6 / 10 | 1776.1.3.6 / 10 | 1776.1.5.6 / 18 |
| owner state 473 | BIC | BIC | BIC |
| provinces state 473 | 39618 | 39618 | 39618 |
| provinces PUD | 24 | 24 | 24 |
| DENNOR | 39613 | 39613 | 39613 |
| `population_radicals` state 473 | 2 426 | 2 426 | 2 426 |
| `population_radicals` BIC | 2 808 | 2 808 | 2 808 |
| `trend_radicals` BIC | `0 0 2808` | identique | identique |
| `radicals_increase` BIC | 0.03263 | 0.25521 | 0.25808 |
| somme ciblée | -0.02425 | -0.24683 | -0.24684 |

La mutation profonde est immédiate, tandis que les agrégats/UI sont obsolètes.

## 37. Logs ciblés

Après fermeture, la recherche imposée avec `Get-ChildItem` et `Select-String`, sans `rg`, donne zéro occurrence pour :

- `zz_sepoy_test_c1`, `zz_sepoy_functional_test_c1` ;
- `sepoy_mutiny_events.2`, `STATE_MADRAS`, `xABADB1` ;
- `add_radicals_in_state`, `very_small_radicals`, `large_radicals`, `set_state_owner` ;
- `Invalid scope`, `jomini_trigger_description` ;
- `should be hidden by a custom_tooltip`.

Aucune erreur directe C-1, 2.c, Madras, scope, transfert, tooltip ou boucle.

Logs après fermeture :

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 236 121 | 2026-07-20 04:57:57.5418746 | `CE544A63904F9109AADCD78B45138E58DE700890F404D30FC8D159E0BFA6B439` |
| `game.log` | 426 441 | 2026-07-20 04:57:57.5418746 | `723CBE8CCE6F069009A47D73B1FFE85D2E0ABB1A7FD6ACD43F89380BCF7B180F` |
| `debug.log` | 400 729 | 2026-07-20 04:58:05.4297328 | `B6D8C9E80101BFD50EB3C2C99E670152B2FC1320BF7F1D366DC49BE749B763BB` |

## 38. Diagnostics hors périmètre

Les logs contiennent 1 734 `Invalid right side`, 1 746 `Script system error`, 677 `PostValidate`, 427 `Unexpected token` et 16 avertissements BOM. Les exemples concernent notamment des comparaisons génériques `sr`, `00_landowners.txt`, de nombreux journaux globaux et des fichiers Japan/historiques. Les 16 BOM citent des fichiers généraux, japonais et historiques, jamais le harnais C-1 ni le fichier Sepoy. Ces diagnostics sont classés hors périmètre.

## 39. Intégrité des sauvegardes

| Sauvegarde | Taille originale | SHA-256 original | Taille fondue | SHA-256 fondu |
|---|---:|---|---:|---|
| pré-2.c | 8 263 309 | `24F3ABA83FD3B3282B6A80259B6BD882E9196150CB8F9052EE236766FA903636` | 110 365 455 | `D4952070D64AB3A18DF3A143BECFBB3FF89EBEECD34765883C952E2F9F79F997` |
| post immédiat | 8 271 635 | `BE1D2277A6FD869CBD6954DF35BF62EA495EE74FE167CB63570B34CBABF8EA57` | 110 493 919 | `F3010E1DA5A9CD0E7E800E5C904BDC166384DBFC3700B40249B36003CA8ED038` |
| post tick 2 | 8 366 412 | `A93D2250AC4F89F516938B79A8FB3B9BD90F1B62C810CD0C201A5CFFAA694A08` | 111 270 470 | `CE1642EBDF94A54A6F15D9F2EB6F3B096D912A041E374537D96989307ECB1009` |

Rakaly 0.8.18 provient de la release officielle, contrôlée par `rakaly --version`. La commande utilisée sur des copies temporaires hors de `save games` est `melt --format vic3 --unknown-key stringify`. Les trois fontes terminent avec code 0. Les tailles et SHA-256 originaux sont identiques après analyse. Le dossier temporaire, les copies, les fontes et le binaire temporaire ont été supprimés.

## 40. Intégrité des fichiers

Après runtime et analyse, les 31 contrôles applicables du manifeste C1S présentent zéro divergence. La copie contient toujours 968 fichiers, 24 harnais, quatre C-1, aucun `.git` et aucun `remote_file_id`. Le fichier Sepoy fork/copie reste à 63 540 octets et au SHA-256 `98C4A50C1DCF2CE79B13AFF82B1FE461651BB99A9B42B002914FD10C338FDCAD`. Aucun gameplay, harnais ou fichier de localisation n’a été modifié.

## 41. Verdict

**PASS_C1_FIX_RUNTIME_PARTIAL_UI**

Tous les critères territoriaux et techniques passent : préparation FRA→BIC, choix manuel exclusif de 2.c, conservation de `xABADB1` et du state 473 réel, PUD à 24 provinces, DENNOR inchangé, boucle terminée, BIC joué, COO/JEY indépendants, aucun owner nul et aucune erreur directe. La baseline et `large_radicals` sont démontrés profondément. L’UI, `population_radicals` et `trend_radicals` restent à la baseline, d’où le suffixe `PARTIAL_UI`.

## 42. Ce que le test valide

Le test valide définitivement la correction C1S : exclure Madras de la garde et de la sélection génériques suffit à préserver le noyau territorial sans casser la terminaison. Il valide également que le bloc radical final s’exécute désormais sur les pops hindoues et sunnites de la portion Madras restée BIC.

## 43. Suite recommandée

Aucune nouvelle correction gameplay n’est justifiée pour l’option 2.c. Le comportement d’agrégats/UI obsolètes est déjà cohérent avec C1P et ne remet pas en cause la mutation des objets sources. La phase peut être close ou documentée par commit séparé des deux livrables C1T.

## 44. Fichiers créés

- `docs/reports/hotfix/HOTFIX_5C2E4C1T_SEPOY_C1_FIX_RUNTIME_TEST.md` ;
- `docs/reports/hotfix/HOTFIX_5C2E4C1T_C1_FIX_RUNTIME_RESULTS.csv`.

Aucun commit automatique n’a été créé.

## 45. Confirmation Travancore/Bengal/Bombay/MARATH

Le runtime C1T et l’analyse n’ont modifié aucun fichier associé à Travancore, Bengal, Bombay ou MARATH. Les branches correspondantes ne sont pas réauditées au-delà des témoins nécessaires. Le stash MARATH n’a subi aucune opération.

## 46. Confirmation `docs/research/technology/`

Le dossier reste l’unique exception non suivie préexistante et n’a pas été touché.

## 47. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` reste présent et intact. Aucun `stash apply`, `pop` ou `drop` n’a été exécuté.
