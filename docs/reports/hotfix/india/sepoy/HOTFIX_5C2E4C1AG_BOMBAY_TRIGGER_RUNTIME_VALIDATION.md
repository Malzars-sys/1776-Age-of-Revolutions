# HOTFIX-5C2E4C1AG — Validation runtime combinée du trigger Bombay

## 1. Résumé

La validation runtime combinée passe dans les deux directions. Sans Bombay, 2.e est cachée ; avec Bombay et sans West Bengal, 2.e est visible et sélectionnable. Aucune option réelle n’a été exécutée et aucune fuite d’effet n’est sérialisée. Verdict : `PASS_BOMBAY_TRIGGER_RUNTIME_VALIDATION`.

## 2. État Git

Racine exacte du fork, branche `hotfix-dlc-audit`, HEAD initial `bc372f1 Prepare Sepoy Bombay trigger controls`. Aucun fichier suivi n’était modifié ; seule l’exception non suivie `docs/research/technology/` était présente. Le stash MARATH était intact.

## 3. Vérification de la copie

Avant et après runtime : 984 fichiers, 40 harnais, soit 4 E-3, 4 E-2, 4 E-1, 4 E1D et 24 legacy. Aucun `.git`, aucun `remote_file_id`. Les 48 lignes matérielles du manifeste AF correspondent après fermeture.

## 4. Trigger AE chargé

Sepoy fork/copie fait 63 653 octets, SHA-256 `66465CB840A5D7348E342F233205F0389E46E5E1C5ECA97B17870ED09D93C6BB`, BOM UTF-8, LF uniquement, zéro CR et identité octet par octet. Le trigger chargé teste exclusivement `any_scope_state` avec `state_region = s:STATE_BOMBAY`.

## 5. Playset

Confirmation utilisateur unique retenue avant lancement : seule `1776_Age_of_Revolutions_sepoy_test` active ; fork principal, autres copies 1776 et Workshop désactivés.

## 6. Logs initiaux

| Log | Taille initiale | LastWriteTime initial | SHA-256 initial |
|---|---:|---|---|
| `error.log` | 117 339 | `2026-07-22T19:10:45.4366092+02:00` | `2DF87D4AD697A4D1F066064F941EAD1B4891B2F898B8C42DFD8214E032E1D8D2` |
| `game.log` | 160 814 | `2026-07-22T19:10:45.4366092+02:00` | `69B0A1415CA4063A9A2471D0F683E9318C888768EDE15BB52285F7DB6CFFE0AC` |
| `debug.log` | 38 689 | `2026-07-22T19:10:54.1988463+02:00` | `F637A7D693CBF9A1136BB70701044DEC6D9514F27D3771E3A5CCF65D7511CBBE` |

## 7. Fiche opérateur unique

La fiche complète E-3 puis E-2, sauvegardes, deux rechargements, contrôles de fuite et fermeture finale a été fournie dans un seul message avant lancement. Aucune branche nouvelle n’a été ajoutée pendant la session.

## 8. Nombre d’ouvertures, rechargements et fermetures

Une ouverture de `victoria3.exe` observée (PID 23148), une nouvelle partie BIC, aucune session GBR, `RELOAD_1`, `RELOAD_2`, puis une fermeture finale. Aucun processus Victoria 3, launcher ou dowser après fermeture ; aucune deuxième ouverture.

## 9. Baseline E-3 West Bengal

State 487 : BIC 218, capitale 40300, provinces `{40292 12 40306 2}` soit 16 provinces, population 17 269 275. State 488 : COO 412, capitale 40305, province `{40305 0}`, population 243 388. Les deux portions sont réelles et non vides ; la capitale BIC est dans 487.

## 10. Baseline E-3 Bombay

State 482 : POR 30, capitale/province 39686 (`x51F0A0`), population 446 391. BIC ne possède aucun Bombay. Les states 483/484/485 restent respectivement MARATH 744, SAT 423 et KHP 424 avec 25/10/3 provinces.

## 11. Baseline E-3 East Bengal

State 14 : BIC 218, capitale 40324, provinces `{40309 29}` soit 30 provinces, population 21 556 674. Aucun effet E-3 ne le scope.

## 12. Sauvegarde négative

`HOTFIX_5C2E4C1AG_E3_NEGATIVE_PRE_EVENT.v3` : 7 908 170 octets, LastWriteTime `2026-07-22T20:28:32.5314449+02:00`, SHA-256 `7AE86C3A45E17DCDD866AE9AD39558683153B153FD1C8845AF2E95F91EE3599B`, date `1776.1.1`, joueur BIC 218, playthrough `5662cb9e-72fd-4921-80ad-11a9f9652054`.

## 13. Ouverture E-3

La décision E-3 et `OPEN_REAL_EVENT` ont ouvert `sepoy_mutiny_events.2` sur BIC. Aucun effet préparatoire, territorial ou radical n’a été exécuté.

## 14. Présentation négative de 2.e

Résultat UI : `OPTION_2E_HIDDEN_NEGATIVE`. La capture montre uniquement l’abandon de l’Inde et la tenue de Fort William/Calcutta ; « Bombay tient bon » est totalement absente.

## 15. Condition échouée négative

La sauvegarde prouve que BIC possède West Bengal mais aucun state Bombay. Le trigger Bombay échoue donc ; West Bengal présent ne réactive pas 2.e.

## 16. Absence de sélection réelle E-3

Aucun bouton réel n’a été sélectionné. L’opérateur a rechargé la sauvegarde négative depuis l’écran d’inspection.

## 17. Recharge 1

`RELOAD_1` a rechargé `HOTFIX_5C2E4C1AG_E3_NEGATIVE_PRE_EVENT`. La fenêtre Sepoy a disparu et la préparation E-2 a ensuite opéré depuis la baseline restaurée.

## 18. Contrôle de fuite E-3

Owners, provinces, populations, marchés et pactes de la baseline sont cohérents. Aucun sujet libéré, transfert, radical large, marché indépendant ou effet de l’événement réel n’est détecté.

## 19. Préparation E-2

Les deux seules mutations attendues sont sérialisées : Bombay 482 POR→BIC, puis West Bengal 487 BIC→COO 488. Le marqueur de préparation ne représente pas un effet de l’événement réel.

## 20. Bombay positif

State 482 devient BIC 218, capitale/province 39686, population 446 391. MARATH/SAT/KHP conservent leurs owners et encodages de 25/10/3 provinces.

## 21. West Bengal positif

State 487 conserve seulement son squelette/statistiques historiques mais n’a plus `country`, capitale ni provinces réelles. State 488 est COO 412, capitale 40300, provinces `{40292 16}` soit les 17 provinces, population 17 512 663. Aucun owner nul ou double.

## 22. East Bengal positif

State 14 reste BIC 218, réel, 30 provinces et 21 556 674 habitants. Après le transfert de West Bengal, BIC relocalise automatiquement sa capitale nationale vers state 14 ; ce changement appartient à la préparation E-2, pas à une option Sepoy réelle.

## 23. Sauvegarde positive

`HOTFIX_5C2E4C1AG_E2_POSITIVE_PRE_EVENT.v3` : 7 910 567 octets, LastWriteTime `2026-07-22T21:32:42.1072985+02:00`, SHA-256 `A43F912C9F26CF8671B4AA13AF22695E4B3BBB6E85A492616D8EBEF94A0B09AD`, date `1776.1.1`, joueur BIC 218, même playthrough.

## 24. Ouverture E-2

La décision E-2 a ouvert `sepoy_mutiny_events.2` sur BIC après vérification de Bombay présent, West Bengal BIC absent, West Bengal COO présent et East Bengal BIC présent.

## 25. Présentation positive de 2.e

Résultat UI : `OPTION_2E_AVAILABLE_POSITIVE`. La capture montre le bouton « Bombay tient bon ! Dirigez toutes les forces restantes vers l’ouest. »

## 26. Disponibilité et sélectionnabilité

Le bouton est visible et cliquable. Son tooltip vert dit que l’option est disponible parce que tout État indo-oriental dont la région étatique est Bombay satisfait la condition. Aucune condition West Bengal/Calcutta n’apparaît.

## 27. Absence de sélection réelle E-2

La capture représente le survol/contrôle de sélectionnabilité. Le contrôle post-recharge ne contient aucun effet territorial, diplomatique ou radical de 2.e : aucune option réelle n’a été exécutée.

## 28. Recharge 2

`RELOAD_2` a rechargé la sauvegarde positive. La fenêtre Sepoy a disparu avant la création du contrôle final.

## 29. Contrôle final post-recharge

Victoria 3 a tronqué le nom à `HOTFIX_5C2E4C1AG_POST_RELOAD_CONTRO.v3`. Ce fichier original n’a pas été renommé : 7 910 453 octets, LastWriteTime `2026-07-22T21:34:36.4739756+02:00`, SHA-256 `43D5BB46BBC756F7059E323D8525213F7531A2E1544577B6D1E1C1D73C68EEDF`, date `1776.1.1`, BIC 218, même playthrough.

## 30. Contrôle de fuite E-2

Le contrôle conserve les mêmes données critiques que PRE : Bombay 482 BIC/39686/446 391 ; West Bengal 487 sans country/provinces et 488 COO/17 provinces/17 512 663 ; East Bengal 14 BIC/30 provinces/21 556 674 ; MARATH/SAT/KHP inchangés. `PASS_NO_EVENT_EFFECT_LEAK`.

## 31. Comparaison négatif/positif

| Contrôle | E-3 négatif | E-2 positif |
|---|---|---|
| Bombay BIC | absent | présent, state 482 |
| West Bengal BIC | présent, state 487 | absent |
| 2.e | cachée | visible et cliquable |
| Option réelle choisie | non | non |

## 32. Nécessité de Bombay

E-3 garde West Bengal mais n’a pas Bombay : 2.e est cachée. Bombay BIC est donc nécessaire dans les états testés.

## 33. Suffisance de Bombay

E-2 possède Bombay mais aucun West Bengal BIC : 2.e est disponible. Bombay BIC est donc suffisant dans les états testés.

## 34. Non-nécessité de West Bengal

La disponibilité positive sans West Bengal BIC confirme que West Bengal n’est plus nécessaire au trigger.

## 35. Non-suffisance de West Bengal

L’indisponibilité négative avec West Bengal BIC mais sans Bombay confirme que West Bengal seul n’est plus suffisant.

## 36. Cohérence trigger/protection

Le trigger AE et les protections territoriales C1W convergent sur Bombay : Bombay ouvre 2.e et reste le noyau protégé lors d’une sélection réelle. Aucune correction supplémentaire n’est justifiée.

## 37. WEST_BENGAL_RETREAT_TRANSFER_EXPECTED

`WEST_BENGAL_RETREAT_TRANSFER_EXPECTED`. West Bengal reste volontairement redistribuable après une véritable retraite vers Bombay. Aucune protection West Bengal n’est recommandée.

## 38. Logs ciblés

Après fermeture, recherches réalisées par `Get-ChildItem` et `Select-String`. Zéro occurrence directe pour E-3, E-2, `sepoy_mutiny_events.2`, `STATE_BOMBAY`, `STATE_WEST_BENGAL`, `STATE_EAST_BENGAL`, `x51F0A0`, `set_state_owner`, `Invalid scope`, `Unexpected token`, diagnostics tooltip ou avertissements BOM.

Logs finaux :

| Log | Taille finale | LastWriteTime final | SHA-256 final |
|---|---:|---|---|
| `error.log` | 34 752 | `2026-07-22T21:34:38.3159815+02:00` | `65D7D784E80525C37697BB2C440715E53FE53B66AD9BC8F4E50022BA4178C8E0` |
| `game.log` | 312 376 | `2026-07-22T21:34:38.3159815+02:00` | `2A400E6BEBDABB523BCC0A421C0CB21C15599725F27C940DF256E905FF0129A8` |
| `debug.log` | 108 234 | `2026-07-22T21:34:46.6080060+02:00` | `F6924706001755AF9541832FBFFFF47440B3354B63BCF87119EE9B76FDB7BBD5` |

## 39. Diagnostics hors périmètre

245 couples `Script system error`/`Invalid right side during comparison 'sr'` pointent vers `common/ai_strategies/00_default_strategy.txt:5078`, associés à d’anciens identifiants de régions stratégiques. Les 675 `PostValidate` proviennent d’événements d’expéditions vanilla (`has_role`). Aucun ne vise les harnais, l’événement Sepoy ou les trois states contrôlés.

## 40. Intégrité des sauvegardes

Rakaly 0.8.18 a été utilisé avec `melt --format vic3 --unknown-key stringify` sur trois copies temporaires hors de `save games`. Copies, fontes, archive et binaire ont ensuite été supprimés. Les tailles et SHA-256 des trois originaux recalculés sont identiques aux valeurs antérieures à l’analyse.

## 41. Intégrité des fichiers

Les 48 contrôles non auto-référentiels du manifeste AF passent sans divergence. La copie reste à 984 fichiers et 40 harnais. Sepoy et journal fork/copie restent identiques. Aucun gameplay, harnais, localisation, descripteur ou marqueur n’a changé.

## 42. Verdict principal

`PASS_BOMBAY_TRIGGER_RUNTIME_VALIDATION`.

## 43. Sous-verdicts

- `PASS_E3_TRIGGER_FIX_NEGATIVE`
- `PASS_E2_TRIGGER_FIX_POSITIVE`
- `BOMBAY_TRIGGER_ACCESS_CONFIRMED`
- `PASS_NO_EVENT_EFFECT_LEAK`
- `WEST_BENGAL_RETREAT_TRANSFER_EXPECTED`

## 44. Conséquence fonctionnelle

Bombay BIC est nécessaire et suffisant ; West Bengal BIC n’est ni nécessaire ni suffisant. Le trigger correspond désormais au noyau territorial annoncé par l’option.

## 45. Correction supplémentaire éventuelle

Aucune correction gameplay supplémentaire n’est recommandée. Les diagnostics globaux hors périmètre doivent rester séparés d’AE/AG.

## 46. Fichiers créés

Uniquement `HOTFIX_5C2E4C1AG_BOMBAY_TRIGGER_RUNTIME_VALIDATION.md` et `HOTFIX_5C2E4C1AG_BOMBAY_TRIGGER_RUNTIME_RESULTS.csv` dans le fork.

## 47. Gameplay inchangé

Aucun gameplay, harnais, localisation ou sauvegarde originale n’a été modifié. Aucun commit automatique n’a été exécuté.

## 48. Confirmation Bengal/Madras/Bombay/Travancore/MARATH

Bengal 2.b, Madras 2.c, protections Bombay C1W, Travancore/`STATE_TRAVANCORE`, East Bengal et les données MARATH/SAT/KHP sont inchangés. Seules les deux mutations jetables E-2 attendues figurent dans les sauvegardes positives.

## 49. Confirmation docs/research/technology/

`docs/research/technology/` est resté intact et hors périmètre.

## 50. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est intact. Aucun apply, pop ou drop.
