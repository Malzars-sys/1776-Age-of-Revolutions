# HOTFIX-5C2E4C1P — Validation runtime finale des radicaux de l’option Sepoy 2.b

## 1. Résumé

Le test B-1 a été exécuté dans une seule session BIC avec la seule copie jetable active. La baseline de 1 % vaut 0 au 1er janvier après préparation, 0 au 2 janvier, puis 383 338 radicaux nationaux sérialisés au 3 janvier. L’événement réel `sepoy_mutiny_events.2` a ensuite été ouvert manuellement et seule l’option 2.b, « Le fort William doit tenir bon », a été sélectionnée.

Le compteur UI, `population_radicals`, `trend_radicals` et les agrégats des deux states restent à la baseline jusqu’au 5 janvier. En revanche, la sauvegarde post-2.b immédiate prouve une mutation radicale sérialisée dans les objets de pops ciblés : la somme de `loyalists_and_radicals` passe de `-3.83315` à `-42.13557`, soit un delta de `-38.30242`. Le même delta apparaît dans `radicals_increase`, qui passe de `3.83577` à `42.13819`. L’échelle interne est confirmée empiriquement par la baseline : `3.83315 × 100 000` correspond aux 383 273 radicaux des deux states BIC. L’effet 2.b représente donc environ 3 830 242 radicaux supplémentaires sérialisés immédiatement au niveau des pops.

West Bengal BIC et East Bengal BIC restent possédés par BIC, la boucle termine, BIC reste jouée et aucun diagnostic runtime direct ne vise B-1 ou 2.b.

Classification temporelle : **IMMEDIATE au niveau des objets de pops et du signal interne, agrégats nationaux/state et UI non rafraîchis au 5 janvier**.

Verdict : **PASS_B1_RADICAL_2B_RUNTIME_PARTIAL_UI**.

## 2. Intégrité initiale

- Racine : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD : `a41b0be Identify Sepoy radical second-tick delay`, commit C1O présent.
- Aucun fichier suivi modifié avant le test.
- Seule exception non suivie : sept fichiers sous `docs/research/technology/`.
- Stash : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.
- Copie jetable : exactement 964 fichiers, vingt fichiers `zz_sepoy*`, aucun dossier `.git`, aucune occurrence de `remote_file_id`.
- Manifeste C1L : 28 entrées non auto-référentes contrôlées, zéro divergence de taille ou de SHA-256.
- Fichier Sepoy fork/copie : 63 422 octets, SHA-256 `FFB4060E659FB8A30691E26BA5BBDA838650EF11AB1760C89EDACFA2310D9BBE`, identité octet par octet.
- Victoria 3 n’était pas lancé lors du contrôle initial.

## 3. Playset

L’opérateur a confirmé que seule `1776_Age_of_Revolutions_sepoy_test` était active. La capture du launcher montre un playset à un mod, la copie Disposable activée, le fork principal et toutes les autres copies 1776/Workshop absents du playset actif.

## 4. Logs avant session

Répertoire : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs`.

| Log | Taille | LastWriteTime | SHA-256 |
|---|---:|---|---|
| `error.log` | 380 941 | 2026-07-19 00:50:17.8812268 +00:00 | `E238701DC20A7698B6F155A919D0453779DE4CF034CE0ABF70225A9D4868714C` |
| `game.log` | 394 786 | 2026-07-19 00:50:17.8812268 +00:00 | `353403392D79BF87A1BB922DDB958537BE0170F68AF8CCFA357317441A1FBB8A` |
| `debug.log` | 190 668 | 2026-07-19 00:50:26.1133306 +00:00 | `935FAEFFE7679AB7E97BD5064658038F05EB39E999F18B8CB68064D181F89C28` |

Les logs n’ont été ni supprimés ni renommés.

## 5. Fiche opérateur unique

Une fiche complète en un seul message a été fournie avant lancement. Elle prescrivait une ouverture, une nouvelle partie BIC, les contrôles territoriaux et religieux initiaux, la préparation B-1, les checkpoints des 1er/2/3 janvier, la sauvegarde pré-2.b immuable, l’ouverture manuelle de l’événement, le choix exclusif de 2.b, les checkpoints immédiat/4 janvier/5 janvier, trois sauvegardes distinctes, une fermeture finale et aucune relance.

## 6. Nombre réel d’ouvertures et fermetures

La séquence opérateur, les captures datées et les artefacts continus attestent une ouverture de Victoria 3, une nouvelle partie BIC, aucune session GBR, aucune fermeture intermédiaire, aucune relance et une fermeture finale propre. Après fermeture, aucun processus `victoria`, `victoria3` ou `dowser` n’était actif.

## 7. Tick 0 avant préparation

Le 1er janvier 1776, BIC est joué, sujet de GBR, avec 58,3 millions d’habitants et 0 radical national visible. West Bengal BIC compte 17,2 millions d’habitants, dont environ 13,0 millions d’hindous et 3,8 millions de sunnites. East Bengal BIC compte 21,5 millions d’habitants, dont environ 5,9 millions d’hindous et 15,4 millions de sunnites. West Bengal est divisé entre BIC et COO.

## 8. Tick 0 après préparation

Après la décision et l’option explicite de préparation B-1, toujours le 1er janvier : 0 radical visible, aucune mutation territoriale ou diplomatique, West/East Bengal BIC préservés et aucun événement Sepoy réel ouvert automatiquement.

## 9. Premier tick

Au 2 janvier 1776, le compteur national reste à 0. Ce zéro est cohérent avec la phase C1O et ne déclenche pas un arrêt du protocole C1P.

## 10. Second tick

Au 3 janvier 1776, le compteur affiche environ 383 K. La sauvegarde pré-2.b sérialise `population_radicals=383338` et `trend_radicals={ 0 0 383338 }`.

## 11. Baseline radicale matérialisée

La baseline est non nulle au second tick. Les deux states BIC affichent et sérialisent 169 256 radicaux à West Bengal et 214 017 à East Bengal, soit 383 273 au total. Les 65 radicaux nationaux restants proviennent d’autres données nationales mineures. `radicals_increase=3.83577` est cohérent avec l’ordre de grandeur de la baseline.

## 12. Sauvegarde pré-2.b

`HOTFIX_5C2E4C1P_B1_RADICAL_PRE_2B_1776_01_03.v3` :

- taille : 8 251 083 octets ;
- LastWriteTime : 2026-07-19 23:13:19.9796899 +00:00 ;
- SHA-256 : `9E41F8B741407A105056CD47C96BA24CF2A5BABCBE2468E0E85168865E75D22B` ;
- date sérialisée : `1776.1.3` ;
- tick global : 9 ;
- pays joueur : objet 218, définition BIC.

## 13. Ouverture manuelle de l’événement

La décision B-1 a ouvert `sepoy_mutiny_events.2` sur BIC. La capture montre l’événement « Le coup de grâce » et les options attendues. Le code associe « Le fort William doit tenir bon » à `sepoy_mutiny_events.2.b`.

## 14. Sélection exclusive de 2.b

L’opérateur a sélectionné l’option de retraite vers le Bengale. Le résultat territorial exclut 2.a : BIC n’est pas annexée par GBR, reste jouée et conserve son noyau bengali. Aucune autre option n’a été utilisée.

## 15. Résultat immédiat

L’événement se ferme et la redistribution termine. Le compteur UI reste à 383 K ; les agrégats restent `population_radicals=383338`, West Bengal 169 256 et East Bengal 214 017. Cependant, les données profondes changent immédiatement :

- `radicals_increase` : `3.83577` → `42.13819` ;
- delta : `38.30242` ;
- somme `loyalists_and_radicals` des 121 pops ciblées : `-3.83315` → `-42.13557` ;
- delta pop exact : `-38.30242`, soit environ 3 830 242 radicaux supplémentaires à l’échelle attestée par la baseline ;
- 88 objets de pops sur 121 changent immédiatement dans les champs cœur, sans ajout ni suppression d’objet.

La matérialisation runtime de 2.b est donc sérialisée immédiatement dans les pops et dans le signal interne, malgré l’agrégat UI/state/national non rafraîchi.

## 16. Premier tick après 2.b

Le 4 janvier, l’opérateur relève les mêmes valeurs visibles : environ 383 K national, 169 256 à West Bengal et 214 017 à East Bengal. Aucune sauvegarde distincte n’était requise à ce checkpoint ; il est documenté par l’observation opérateur.

## 17. Second tick après 2.b

Le 5 janvier, les mêmes agrégats sont visibles et sérialisés : `population_radicals=383338`, West Bengal 169 256, East Bengal 214 017 et `trend_radicals={ 0 0 383338 }`. Le signal interne vaut `radicals_increase=42.141`. Les objets de pops conservent l’augmentation 2.b ; seules cinq pops ont de petites évolutions démographiques ou de fond entre le 3 et le 5 janvier.

## 18. Classification temporelle

**IMMEDIATE** pour la mutation sérialisée des pops et le signal `radicals_increase`. La sauvegarde immédiate contient déjà le delta complet `38.30242`.

La classification ne peut pas être `NOT_MATERIALIZED`, car ce delta est présent dans les objets ciblés et correspond exactement à l’augmentation du signal interne. Les agrégats `population_radicals`, `trend_radicals` et l’UI sont en revanche **STALE_THROUGH_TICK2** pour cet effet additionnel.

## 19. West Bengal

- State 487 : owner/pays 218 BIC dans les trois sauvegardes.
- State 488 : owner/pays 412 COO dans les trois sauvegardes.
- Portion BIC : 169 256 radicaux agrégés avant 2.b, immédiatement après et au 5 janvier.
- Pops ciblées : 65 hindoues, population 13 071 323 au 3 janvier ; 15 sunnites, population 3 822 116.
- Delta `loyalists_and_radicals` immédiat : environ `-13.07426` pour les hindous et `-3.82608` pour les sunnites.

## 20. East Bengal

- State 14 : owner/pays 218 BIC dans les trois sauvegardes.
- 214 017 radicaux agrégés avant 2.b, immédiatement après et au 5 janvier.
- Pops ciblées : 30 hindoues, population 5 992 000 au 3 janvier ; 11 sunnites, population 15 408 126.
- Delta `loyalists_and_radicals` immédiat : environ `-5.99197` pour les hindous et `-15.41011` pour les sunnites.

## 21. Terminaison de la boucle

L’événement s’est fermé, le jeu est resté réactif, la carte redistribuée a été affichée et les sauvegardes des 3 et 5 janvier ont été écrites. Aucun symptôme de boucle vide ou non terminée n’existe.

## 22. Comparaison UI

| Checkpoint | National | West Bengal BIC | East Bengal BIC |
|---|---:|---:|---:|
| 1er janvier avant préparation | 0 | non séparé | non séparé |
| 1er janvier après préparation | 0 | non séparé | non séparé |
| 2 janvier | 0 | non séparé | non séparé |
| 3 janvier avant 2.b | 383 K | 169 256 | 214 017 |
| 3 janvier immédiatement après 2.b | 383 K | 169 256 | 214 017 |
| 4 janvier | 383 K | 169 256 | 214 017 |
| 5 janvier | 383 K | 169 256 | 214 017 |

L’UI prouve la baseline et la préservation territoriale, mais ne montre pas l’effet additionnel pourtant sérialisé dans les pops.

## 23. Comparaison sérialisée

| Champ | Pré-2.b | Immédiat | 5 janvier |
|---|---:|---:|---:|
| `population_radicals` BIC | 383 338 | 383 338 | 383 338 |
| `trend_radicals` | `0 0 383338` | identique | identique |
| `radicals_increase` | 3.83577 | 42.13819 | 42.141 |
| somme ciblée `loyalists_and_radicals` | -3.83315 | -42.13557 | -42.13829 |
| hash `trend_radicals` | `36D9FA6E...` | identique | identique |
| hash `pop_radicals_and_loyalists_statistics` | `8CFEC231...` | `2FFF3254...` | `A8C341CE...` |
| hash `radicals_increase_data` | `69B960AE...` | `57364D27...` | `68D4FB28...` |

Le delta profond immédiat et le delta du signal sont identiques à cinq décimales : `38.30242`.

## 24. Population radicale

La baseline agrégée vaut 383 338. L’effet 2.b ajoute environ 3 830 242 unités-personnes dans les objets de pops, soit l’ordre prévu de plusieurs millions pour `large_radicals=0.1`. L’agrégat `population_radicals` n’est pas recalculé dans la fenêtre observée ; cela ne supprime pas la mutation des objets sources.

## 25. Trend radicals

Le bloc `trend_radicals` reste strictement identique dans les trois sauvegardes, SHA-256 `36D9FA6E1A8598467A40281CB230527A7794F5678F68D153B1771E3683C77632`, avec valeurs `{ 0 0 383338 }`. Il reflète la baseline du 3 janvier, pas le delta immédiat de 2.b.

## 26. Radicals increase

Le bloc `radicals_increase_data` ajoute immédiatement une composante `38.30242`, en plus de la composante baseline `3.83013` et de faibles facteurs généraux. La valeur agrégée passe à `42.13819`, puis `42.141` au 5 janvier. Ce signal est la contrepartie exacte du changement mesuré dans les objets de pops.

## 27. Analyse des pops hindoues

Les deux portions BIC contiennent 95 objets hindous : 65 à West Bengal et 30 à East Bengal. Entre pré-2.b et immédiat, 76 objets hindous changent dans `loyalists_and_radicals`. Les deltas groupés correspondent à environ 1 307 426 radicaux additionnels à West Bengal et 599 197 à East Bengal. Les effectifs restent pratiquement identiques ; les variations ultérieures au 5 janvier sont démographiques et marginales.

## 28. Analyse des pops sunnites

Les deux portions BIC contiennent 26 objets sunnites : 15 à West Bengal et 11 à East Bengal. Entre pré-2.b et immédiat, 12 objets sunnites changent dans `loyalists_and_radicals`. Les deltas groupés correspondent à environ 382 608 radicaux additionnels à West Bengal et 1 541 011 à East Bengal. Les deux religions et les deux states sont donc dans le scope effectif.

## 29. Logs ciblés

Après fermeture :

| Log | Taille | LastWriteTime | SHA-256 |
|---|---:|---|---|
| `error.log` | 392 984 | 2026-07-19 23:19:27.1163939 +00:00 | `8A6B8921551A48E84626767222D55745A18C2E12539486B6BD4610D63739A384` |
| `game.log` | 115 990 | 2026-07-19 23:19:27.1163939 +00:00 | `014C8539A3229D2EBDCD426537EFB4D9DAFBDED4F5111F9042F8B69D73F967B3` |
| `debug.log` | 260 919 | 2026-07-19 23:19:36.5147480 +00:00 | `F693C08A9720788068C729FF0BE65E91822B657FA67AB3E07C48744972BEAB40` |

La recherche imposée avec `Get-ChildItem` et `Select-String` donne zéro occurrence pour `zz_sepoy_test_b1`, `zz_sepoy_functional_test_b1`, `sepoy_mutiny_events.2`, `add_radicals_in_state`, `very_small_radicals`, `large_radicals`, `STATE_WEST_BENGAL`, `STATE_EAST_BENGAL`, `Invalid scope` et `jomini_trigger_description`. Aucun diagnostic direct B-1/2.b, aucune erreur de scope, aucun problème de tooltip/BOM B-1 et aucune boucle non terminée.

## 30. Diagnostics hors périmètre

Les logs contiennent 1 628 occurrences génériques de `Script system error` (`error.log` 1 175, `game.log` 453), 677 `PostValidate`, 427 `Unexpected token` et 16 avertissements BOM. Aucun `Script system error` ne contient B-1, Sepoy, radical ou Bengal. Les `Unexpected token` et BOM citent des fichiers globaux tels que `common/interest_groups/00_landowners.txt`, de nombreux journaux généraux et des fichiers Japan ; aucun ne vise les quatre fichiers B-1 ou `sepoy_mutiny_events.2`. Ils sont classés hors périmètre.

## 31. Intégrité des sauvegardes

| Sauvegarde | Taille | SHA-256 original | Taille fondue | SHA-256 fondu |
|---|---:|---|---:|---|
| pré-2.b | 8 251 083 | `9E41F8B741407A105056CD47C96BA24CF2A5BABCBE2468E0E85168865E75D22B` | 110 281 615 | `268FF581DFCAE97D9DAB17979AC5A28EDC5D9ED17534260E912AEE55C41B05FA` |
| post-2.b immédiat | 8 253 860 | `D6758A45CEA575F2EB9368FD66BDE769E5AEDCB2DA6601EA9C24326DE829637A` | 110 315 807 | `A6A5B65FE0DB1B52BB11C6680BEBAA266D97EA6FF603FB33F1ED687445002D06` |
| post-2.b tick 2 | 8 358 130 | `9556141FA0BBF907B30733E4F321C893BCB38B0D81D7256C18765FD6183AED6F` | 111 137 754 | `C43F9B13EF2273763B77A6161DEC5C8FD596F3702E37CA17F387A398231D96AB` |

Les originaux ont été uniquement lus et hashés. Des copies temporaires hors de `save games` ont été fondues avec Rakaly 0.8.18, commande `melt --format vic3 --unknown-key stringify`, code retour 0. Les hashes originaux ont été recalculés après l’analyse et sont inchangés.

## 32. Intégrité des fichiers

Après runtime et analyse, la copie conserve 964 fichiers, vingt harnais, aucun `.git` et aucun `remote_file_id`. Le fichier Sepoy conserve sa taille, son hash et son identité fork/copie. Aucun fichier gameplay, harnais ou localisation n’a été modifié.

## 33. Verdict

**PASS_B1_RADICAL_2B_RUNTIME_PARTIAL_UI**

Motifs : baseline non nulle au second tick ; exécution manuelle exclusive de 2.b ; hausse supplémentaire sérialisée immédiatement dans les pops ; delta d’environ 3,83 millions conforme à `large_radicals` ; scope limité aux pops hindoues/sunnites des portions BIC de West/East Bengal ; noyau bengali préservé ; boucle terminée ; aucune erreur B-1/Sepoy. L’UI et les agrégats nationaux/state ne reflètent pas cette hausse dans la fenêtre observée et ne permettent pas une séparation religieuse fiable.

## 34. Ce que le test valide

Le test valide que les deux appels `add_radicals_in_state` de 2.b s’exécutent sur les states BIC protégés, touchent les religions prévues et sérialisent une hausse de 10 % à l’échelle des objets de pops. Il valide aussi la correction territoriale Bengal et la terminaison de la redistribution.

Il ne valide pas un délai précis de rafraîchissement de `population_radicals`, `trend_radicals` ou du compteur UI après 2.b ; ceux-ci restent à la baseline jusqu’au 5 janvier.

## 35. Suite recommandée

Aucune correction gameplay n’est justifiée pour `large_radicals` ou le scope de 2.b. Si une phase supplémentaire est souhaitée, elle doit porter uniquement sur le calendrier de recalcul des agrégats/UI à partir des objets de pops, sans remettre en cause l’effet ni la correction Bengal déjà validés.

## 36. Fichiers créés

- `docs/reports/hotfix/HOTFIX_5C2E4C1P_B1_RADICAL_2B_RUNTIME_TEST.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1P_B1_RADICAL_2B_RESULTS.csv`

## 37. Confirmation docs/research/technology/

Les sept fichiers préexistants sous `docs/research/technology/` restent non suivis et n’ont pas été touchés.

## 38. Confirmation stash MARATH

Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` reste présent et intact. Aucun commit n’a été créé automatiquement.
