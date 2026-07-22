# 1. Résumé

Le scénario E-1 a été exécuté dans une seule session Victoria 3. La préparation POR → BIC, l’ouverture manuelle de `sepoy_mutiny_events.2`, la sélection exclusive de 2.e, la terminaison de la boucle et l’indépendance de COO/JEY sont nominales. En revanche, la boucle générique redistribue le noyau de retraite : `x51F0A0` quitte BIC pour KHP et le region state Bombay BIC devient vide. La portion BIC de West Bengal est aussi transférée à COO. Verdict : `FAIL_E1_BOMBAY_CORE_LOST / WEST_BENGAL_LOST`.

# 2. État Git initial

Racine exacte : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`. Branche : `hotfix-dlc-audit`. HEAD : `f7b2bf3 Prepare Sepoy Bombay retreat test`. Aucun fichier suivi n’était modifié. Le stash attendu était présent : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.

# 3. Exception docs/research/technology/

La seule exception non suivie initiale était `docs/research/technology/`. Elle est restée hors périmètre et aucune opération ne l’a visée.

# 4. Vérification de la copie

La copie jetable contenait exactement 972 fichiers, 28 fichiers de harnais dont quatre E-1, aucun dossier `.git` et aucun `remote_file_id`. Les 24 anciens harnais étaient conformes au manifeste C1U. Le Sepoy du fork et celui de la copie étaient identiques octet par octet : 63 540 octets, SHA-256 `98C4A50C1DCF2CE79B13AFF82B1FE461651BB99A9B42B002914FD10C338FDCAD`.

# 5. Playset

L’opérateur a confirmé explicitement que seule `1776_Age_of_Revolutions_sepoy_test` était active ; le fork principal, les autres copies 1776 et les versions Workshop étaient désactivés.

# 6. Logs avant session

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 236 121 | 2026-07-20T04:57:57.5418746Z | `CE544A63904F9109AADCD78B45138E58DE700890F404D30FC8D159E0BFA6B439` |
| `game.log` | 426 441 | 2026-07-20T04:57:57.5418746Z | `723CBE8CCE6F069009A47D73B1FFE85D2E0ABB1A7FD6ACD43F89380BCF7B180F` |
| `debug.log` | 400 729 | 2026-07-20T04:58:05.4297328Z | `B6D8C9E80101BFD50EB3C2C99E670152B2FC1320BF7F1D366DC49BE749B763BB` |

Aucun log n’a été supprimé, déplacé ou renommé.

# 7. Fiche opérateur unique

La fiche complète a été transmise avant lancement en un seul message. Elle couvrait la nouvelle partie BIC, les portions initiales de West Bengal et Bombay, la préparation exclusive de `x51F0A0`, les observations des 1er, 2 et 3 janvier, la sauvegarde pré‑2.e, l’ouverture manuelle de l’événement, le choix exclusif de 2.e, les contrôles immédiats, les observations des 4 et 5 janvier, les trois sauvegardes distinctes et la fermeture finale.

# 8. Nombre réel d’ouvertures et fermetures

Compte rendu opérateur : une ouverture de Victoria 3, une nouvelle partie BIC, aucune session GBR, aucune relance, une fermeture finale. Après le compte rendu, aucun processus Victoria 3 ou launcher n’était actif.

# 9. État initial West Bengal

La sauvegarde pré‑2.e contient une portion BIC réelle, region state 487, provinces sérialisées `40292` et `40306`, population 17 269 307, ainsi qu’une portion COO séparée, region state 488, province `40305`, population 243 388. Cette portion BIC rend le trigger anormal de 2.e vrai.

# 10. État initial Bombay

Avant préparation, Bombay est divisé entre POR, MARATH, SAT et KHP. BIC ne possède aucune portion Bombay. L’interface et les contrôles opérateur confirment les quatre portions attendues.

# 11. Portion POR

POR possède uniquement `x51F0A0`, identifiant interne sérialisé `39686`, dans Bombay. La population transférable est de 446 391 personnes.

# 12. Portion MARATH

MARATH conserve ses 25 provinces. Le region state 483 a une population de 11 811 923 et son encodage de provinces est strictement identique dans les trois sauvegardes analysées.

# 13. Portion SAT

SAT conserve ses 10 provinces. Le region state 484 a une population de 742 713 et son encodage de provinces est strictement identique dans les trois sauvegardes.

# 14. Portion KHP

KHP commence avec trois provinces dans le region state 485, population 517 691. Cette portion devient ensuite le receveur exact de `x51F0A0`.

# 15. Préparation POR → BIC

L’option de préparation E-1 transfère uniquement `x51F0A0` de POR à BIC. Dans la sauvegarde pré‑2.e, la province `39686` pointe vers le region state 482, pays BIC (ID 218). Le nouvel état Bombay BIC contient 446 391 personnes.

# 16. Absence d’autre mutation

L’opérateur signale le reste nominal : MARATH/SAT/KHP et West Bengal sont inchangés pendant la préparation, POR conserve ses autres territoires, aucune mutation diplomatique parasite et aucun événement Sepoy réel ne s’ouvre automatiquement. Les données pré‑2.e concordent.

# 17. Tick 0

La portion Bombay BIC existe et contient 446 K personnes. L’interface montre 0 radical avant matérialisation de la petite baseline. Aucune conclusion négative n’a été tirée de ce seul agrégat UI.

# 18. Premier tick

Au 2 janvier, la portion reste à BIC et l’interface affiche encore la structure démographique attendue. Aucun transfert territorial anormal n’est observé.

# 19. Second tick

Au 3 janvier, avant 2.e, `x51F0A0` appartient toujours à BIC. La portion compte 446 391 personnes, dont 75 852 hindoues, et 909 radicaux sont visibles/sérialisés.

# 20. Sauvegarde pré‑2.e

`HOTFIX_5C2E4C1V_E1_PRE_2E_1776_01_03.v3` : date sérialisée `1776.1.3.12`, 8 269 254 octets, LastWriteTime UTC `2026-07-20T19:12:39.6596550Z`, SHA-256 `3004330E199D2D57C2DD6B0F29FB81D68A60C3F31B8D4389EA1F716981B81E7E`.

# 21. Baseline hindoue profonde

La pop hindoue ciblée pré‑2.e est l’objet 14727 : workforce 18 963, dependents 56 889, total 75 852, location 482, religion `hindu`, `loyalists_and_radicals=-0.00909`. Le region state 482 porte `population_radicals=909`. Le signal profond est compatible avec `very_small_radicals` à 1 % : baseline validée.

# 22. Absence de cible sunnite

La portion préparée ne contient aucune pop sunnite. L’appel sunnite reste exécuté par le harnais, mais son delta nul est attendu et ne constitue ni `FAIL_E1_RADICAL_SCOPE` ni `FAIL_E1_RADICAL_EFFECT`.

# 23. Ouverture manuelle de l’événement

La décision d’ouverture E-1 a ouvert manuellement `sepoy_mutiny_events.2` sur BIC. La capture montre l’événement « Le coup de grâce » et le trigger affiché sur West Bengal.

# 24. Sélection exclusive de 2.e

L’option « Bombay tient bon ! Dirigez toutes les forces restantes vers l’ouest. » était disponible et a été la seule option sélectionnée. Aucun autre choix de l’événement n’a été utilisé.

# 25. Terminaison de la boucle

La fenêtre s’est fermée, le jeu est resté réactif, la sauvegarde immédiate a été créée et le calendrier a avancé jusqu’au 5 janvier. La boucle termine donc techniquement ; il n’y a pas `FAIL_E1_LOOP`.

# 26. Pays joué final

BIC reste le pays joué après l’effet. Le script ne change pas le pays joueur et les captures postérieures montrent toujours l’interface BIC.

# 27. x51F0A0 après 2.e

Dans la sauvegarde immédiate, la province interne `39686` ne pointe plus vers le region state BIC 482 mais vers le region state KHP 485. Le résultat est stable dans la sauvegarde du 5 janvier. Owner effectif : KHP ; aucun état d’occupation ou de guerre n’est signalé, le controller observé suit KHP.

# 28. Region state Bombay BIC

L’objet 482 subsiste comme objet cache avec `previous_country=218`, population/radicaux historiques, mais sans `country` et avec `provinces={ }`. Il ne constitue plus un region state réel détenu par BIC. BIC ne conserve aucune portion réelle de `STATE_BOMBAY`.

# 29. Receveur éventuel Bombay

Le receveur exact est KHP/Kolhapur (country ID 424), et non MARATH. Le region state 485 gagne `39686`, passe de 517 691 à 964 082 personnes et de trois à quatre provinces logiques.

# 30. MARATH après 2.e

MARATH conserve ses 25 provinces et une population sérialisée inchangée de 11 811 923. Aucune portion MARATH n’a été sélectionnée par le harnais ou transférée par 2.e dans ce test.

# 31. SAT après 2.e

SAT conserve ses 10 provinces et sa population sérialisée de 742 713. Aucun transfert n’est constaté.

# 32. KHP après 2.e

KHP conserve ses trois provinces initiales et reçoit en plus `x51F0A0`. La nouvelle population 964 082 est exactement 517 691 + 446 391.

# 33. West Bengal après 2.e

Le region state BIC 487 devient vide, sans `country`, avec `previous_country=218`. La portion initiale BIC est intégrée au region state COO 488, dont la population passe de 243 388 à 17 513 023. Statut : `WEST_BENGAL_LOST`.

# 34. Analyse distincte du trigger West Bengal

West Bengal doit être séparé du défaut principal. La localisation et l’intention de 2.e désignent Bombay comme noyau de retraite ; C1U identifie West Bengal comme trigger probablement copié de 2.b. Sa perte démontre qu’il reste admissible à la redistribution, mais ne prouve pas qu’il soit un second noyau intentionnel. Aucune protection West Bengal n’est donc recommandée automatiquement sans décision fonctionnelle préalable.

# 35. Statut COO

COO devient indépendant comme attendu et reçoit la portion BIC de West Bengal. Son marché passe du marché britannique (ID 0) à un marché indépendant (ID 281). Au 5 janvier, le pays ID 412 porte `definition="BGL"` et `previous_definitions={"COO"}` : transformation en Bengal/BGL, sans remettre en cause l’indépendance observée.

# 36. Statut JEY

JEY devient indépendant comme attendu ; son marché passe de 0 à un marché indépendant (ID 282). Aucun défaut territorial JEY n’est signalé.

# 37. Owners nuls ou incohérents

Aucun territoire réel observé n’a un owner nul et aucune double attribution n’est visible. Les objets BIC 482 et 487 sans `country` sont des region states vidés ; leurs provinces réelles sont rattachées respectivement à KHP 485 et COO 488.

# 38. Résultat radical immédiat

La portion Bombay n’existe plus chez BIC au moment de l’effet final `every_scope_state` South India. L’absence de hausse `large_radicals` sur cette portion est donc cohérente avec l’ordre du script et n’est pas classée comme défaillance de l’API radicale.

# 39. Premier tick après 2.e

Au 4 janvier, l’opérateur confirme que Bombay reste perdu, West Bengal reste transféré et le jeu demeure nominal/réactif. La population transférée de Bombay présente 909 radicaux visibles.

# 40. Second tick après 2.e

La sauvegarde du 5 janvier (`1776.1.5.18`) confirme la stabilité : `39686` reste dans KHP 485, BIC 482 reste vide, BIC 487 reste vide et COO/BGL 488 conserve West Bengal.

# 41. Analyse des pops hindoues

Après le transfert, la pop hindoue BIC 14727 devient un shell sans workforce. Ses 18 963 travailleurs et 56 889 dépendants sont fusionnés dans la pop hindoue KHP 14772 : celle-ci passe de 99 718/299 155 à 118 681/356 044, soit exactement +18 963/+56 889. La population hindoue transférée est donc suivie sans perte.

# 42. Analyse des pops sunnites sans cible

Il n’existe aucune cible sunnite dans la portion Bombay préparée. Aucun delta sunnite n’est attendu avant ou après 2.e ; aucune cible artificielle n’est inférée.

# 43. Radicals increase

Pour BIC, `radicals_increase=0.01473` dans les trois sauvegardes. `population_radicals=1234` et l’objet `trend_radicals` (`sample_rate=4`, `count=3650`) restent également inchangés. Ces agrégats nationaux ne prouvent pas un effet `large_radicals` sur une portion qui a déjà quitté BIC.

# 44. Loyalists and radicals

La pop hindoue cible porte `-0.00909` avant 2.e. Après fusion dans KHP 14772, `loyalists_and_radicals` reste `-0.00909` immédiatement et au 5 janvier. Il n’existe donc aucune hausse compatible avec `large_radicals` sur cette population, résultat attendu après la perte territoriale préalable.

# 45. Comparaison UI

L’UI passe de Bombay BIC, 446 K personnes et 909 radicaux, à une région Bombay sans portion BIC. Les captures montrent Maharashtra/Satara/Kolhapur après l’événement et la carte des radicaux montre 909 pour la population transférée. L’UI et les données profondes sont cohérentes ; il ne s’agit pas d’un cas `PARTIAL_UI`.

# 46. Comparaison sérialisée

Les trois sauvegardes originales ont été copiées hors de `save games`, puis fondues avec Rakaly 0.8.18 au moyen de `melt --format vic3 --unknown-key stringify` (avec sortie explicitement dirigée vers le dossier temporaire). Dates : `1776.1.3.12`, `1776.1.3.12`, `1776.1.5.18`. Les fontes faisaient respectivement 110 451 371, 110 510 977 et 111 300 524 octets. Les copies, fontes, archive et binaire temporaires ont été supprimés après analyse.

# 47. Logs ciblés

La recherche obligatoire a été faite avec `Get-ChildItem` et `Select-String`, sans `rg`, sur les trois logs. Les onze motifs directs (`zz_sepoy_test_e1`, `zz_sepoy_functional_test_e1`, `sepoy_mutiny_events.2`, `STATE_BOMBAY`, `STATE_WEST_BENGAL`, `x51F0A0`, `add_radicals_in_state`, `very_small_radicals`, `large_radicals`, `set_state_owner`, `random_scope_state`) ont zéro occurrence. Il n’existe donc aucune erreur directe E-1/2.e/Bombay/West Bengal, aucun diagnostic de scope/transfert ciblé, aucun tooltip/BOM E-1 et aucun signe de boucle non terminée.

Métadonnées après fermeture :

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 279 152 | 2026-07-20T19:17:56.0668606Z | `BAF33E8211B97A2456722D65E0E7CDE327FAAF051AEF2459763E7557C31938FA` |
| `game.log` | 178 847 | 2026-07-20T19:17:56.0668606Z | `F1053734D6DEDFF494FDFB31D3099AD4A6DFA4C045B691ED60509F9A3C502029` |
| `debug.log` | 471 009 | 2026-07-20T19:18:10.0413423Z | `83353B0C5B774460B24BFF32AAEC2ED2B1896233AB1C9A2ACD804E61F82CD9F9` |

# 48. Diagnostics hors périmètre

Les logs contiennent des diagnostics globaux préexistants/non ciblés : `Invalid right side` 762 fois dans `error.log` et 363 dans `game.log`, `Script system error` 773/371, `PostValidate` 677 fois dans `debug.log`, `Unexpected token` 427 fois et `should be in utf8-bom encoding` 16 fois. Aucun ne contient les identifiants E-1/2.e/Bombay/West Bengal recherchés ; ils sont classés hors périmètre et ne masquent pas le résultat territorial sérialisé.

# 49. Intégrité des sauvegardes

Après analyse, les trois originaux ont été rehashés sans changement :

| Sauvegarde | Taille | SHA-256 |
|---|---:|---|
| `HOTFIX_5C2E4C1V_E1_PRE_2E_1776_01_03.v3` | 8 269 254 | `3004330E199D2D57C2DD6B0F29FB81D68A60C3F31B8D4389EA1F716981B81E7E` |
| `HOTFIX_5C2E4C1V_E1_POST_2E_IMMEDIATE_1776_01_03.v3` | 8 274 555 | `946A6405BCD93789479825E1D668BB743FC16E945796FE35FA8425D727A589D0` |
| `HOTFIX_5C2E4C1V_E1_POST_2E_TICK2_1776_01_05.v3` | 8 370 838 | `13C1249BB0D14B8313B27337DE9E486D952B3FAC085D99DB81DC1239DF9AE30D` |

# 50. Intégrité des fichiers

La comparaison post‑runtime au manifeste C1U donne zéro divergence pour le Sepoy fork/copie, le journal Sepoy fork/copie, les quatre fichiers E‑1, les 24 anciens harnais, `descriptor.mod`, le marqueur et le descripteur launcher. La copie reste à 972 fichiers et 28 harnais. Aucun gameplay, harnais ou fichier de localisation n’a été modifié.

# 51. Verdict principal

`FAIL_E1_BOMBAY_CORE_LOST`. Les trois critères matériels sont réunis : `x51F0A0` quitte BIC, le region state Bombay BIC devient vide et BIC ne conserve aucune portion réelle de `STATE_BOMBAY`. La terminaison technique de la boucle ne peut pas convertir ce résultat en PASS.

# 52. Statut West Bengal

`WEST_BENGAL_LOST`. Verdict combiné final : `FAIL_E1_BOMBAY_CORE_LOST / WEST_BENGAL_LOST`.

# 53. Ce que le test valide

Le test valide la préparation POR → BIC, la baseline hindoue profonde, l’absence attendue de cible sunnite, l’accessibilité de 2.e par West Bengal, la sélection manuelle exclusive, la terminaison de la boucle, le maintien de BIC comme pays joué, l’indépendance de COO/JEY, l’absence d’owner réel nul, la stabilité sur deux ticks et le diagnostic statique C1U : Bombay et West Bengal sont tous deux effectivement sélectionnables par la boucle générique.

# 54. Suite recommandée

Ouvrir une phase corrective distincte pour exclure explicitement `STATE_BOMBAY` à la fois :

1. de la garde territoriale du `while` ;
2. du filtre de `random_scope_state`.

Une correction limitée à la sélection est interdite, car la garde pourrait rester vraie sans candidat transférable et produire une boucle vide. Traiter West Bengal dans une décision fonctionnelle séparée : déterminer d’abord s’il doit seulement déclencher 2.e, rester redistribuable, ou constituer un second noyau ; la localisation actuelle ne démontre que le noyau Bombay.

# 55. Fichiers créés

- `docs/reports/hotfix/HOTFIX_5C2E4C1V_SEPOY_E1_RUNTIME_TEST.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1V_E1_RUNTIME_RESULTS.csv`

Aucun commit automatique n’est effectué.

# 56. Confirmation Bengal/Madras/Travancore/MARATH

Le runtime n’a modifié aucun fichier ni harnais Bengal, Madras ou Travancore. L’opérateur indique que tout le reste est nominal. MARATH est prouvé inchangé par ses provinces et sa population dans les trois sauvegardes. La perte de la portion BIC de West Bengal documentée ici est l’effet observé de 2.e, distinct des corrections antérieures de noyau.

# 57. Confirmation docs/research/technology/

`docs/research/technology/` est resté non suivi, hors périmètre et intact ; aucun fichier C1V n’y a été créé.

# 58. Confirmation stash MARATH

Le stash `WIP NAVY-3C-3 Maratha Konkan Flotilla` est resté présent. Aucune opération `stash`, `apply`, `pop`, `drop` ou modification de son contenu n’a été effectuée.
