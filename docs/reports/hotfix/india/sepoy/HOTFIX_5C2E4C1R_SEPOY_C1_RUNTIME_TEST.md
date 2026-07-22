# HOTFIX-5C2E4C1R — Test runtime Sepoy C-1, retraite vers Madras

## 1. Résumé

Le test C-1 a été exécuté dans une seule session BIC avec la seule copie Disposable active. La préparation transfère correctement la province `xABADB1` de FRA à BIC et prépare une baseline radicale profonde malgré un affichage UI nul. L'option `sepoy_mutiny_events.2.c` est disponible et sélectionnée manuellement. La boucle termine, mais elle transfère ensuite la portion préparée à PUD. BIC perd toute présence dans `STATE_MADRAS`. Le verdict principal est **FAIL_C1_MADRAS_CORE_LOST**.

## 2. État Git initial

- racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork` ;
- branche : `hotfix-dlc-audit` ;
- HEAD : `63ad91e Prepare Sepoy Madras retreat test` ;
- aucun fichier suivi modifié ;
- aucun commit automatique.

## 3. Exception `docs/research/technology/`

L'unique chemin non suivi initial était `docs/research/technology/`. Il n'a été ni lu pour le test, ni modifié, ni inclus dans les livrables.

## 4. Vérification de la copie

Avant lancement, la copie Disposable contenait exactement 968 fichiers, dont 24 fichiers de harnais et quatre fichiers C-1. Elle ne contenait aucun dossier `.git` et aucune occurrence de `remote_file_id`. Les 29 lignes vérifiables du manifeste C1Q étaient conformes. Parmi les fichiers partagés avec le fork, 942 étaient identiques ; seul le `descriptor.mod` jetable différait comme prévu, et les 25 fichiers supplémentaires étaient le marqueur et les harnais jetables attendus.

## 5. Playset

L'opérateur a confirmé avant lancement que seule la copie Disposable était active, que le fork principal était désactivé et qu'aucune autre copie 1776 ni version Workshop n'était active. La barrière `BLOCKED_DUPLICATE_MODS_ENABLED` n'a pas été déclenchée.

## 6. Baseline des logs

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 392 984 | 2026-07-19 23:19:27.1163939 | `8A6B8921551A48E84626767222D55745A18C2E12539486B6BD4610D63739A384` |
| `game.log` | 115 990 | 2026-07-19 23:19:27.1163939 | `014C8539A3229D2EBDCD426537EFB4D9DAFBDED4F5111F9042F8B69D73F967B3` |
| `debug.log` | 260 919 | 2026-07-19 23:19:36.5147480 | `F693C08A9720788068C729FF0BE65E91822B657FA67AB3E07C48744972BEAB40` |

Les logs n'ont été ni supprimés, ni déplacés, ni renommés.

## 7. Fiche opérateur unique

La fiche complète a été fournie avant le lancement dans un seul message. Elle couvrait la nouvelle partie BIC, les trois portions initiales de Madras, la préparation, les ticks, les trois sauvegardes, l'ouverture manuelle de l'événement, la sélection exclusive de 2.c, les transferts, les sujets, les radicaux et l'unique fermeture finale. Aucune nouvelle branche de test n'a été ajoutée pendant la session.

## 8. Nombre réel d'ouvertures et fermetures

La conversation opérateur et la continuité du `playthrough_id` sérialisé attestent une seule ouverture, une seule nouvelle partie BIC et une seule fermeture finale. Aucune session GBR, aucune relance, aucun chargement d'une sauvegarde A/B/C et aucune commande console n'ont été signalés.

## 9. État initial de Madras

L'UI montre un state-region Carnatic/Madras partagé entre FRA, DENNOR et PUD. BIC n'y possède initialement aucune portion.

## 10. Portion FRA

La portion française est la province unique `xABADB1`, Pondichéry, affichée comme « Carnatic français ». Elle compte environ 230 000 habitants.

## 11. Portion DENNOR

DENNOR possède la province unique `x10B060`. Cette portion est préservée avant et après 2.c. Dans les sauvegardes, elle correspond au region state 474, pays 745 `DENNOR`, province interne 39613.

## 12. Portion PUD

PUD possède initialement les 24 autres provinces. Dans la sauvegarde pré-2.c, le region state 475 encode ces 24 provinces par `39599 13 39614 3 39619 5`.

## 13. Préparation C-1

La décision de préparation ouvre l'événement prévu et l'opérateur choisit explicitement « Transférer la portion française de Madras et créer la baseline C-1 ». L'option annonce un transfert à BIC et deux effets `+1.0 %`, hindou et sunnite.

## 14. Preuve de l'unique mutation

Après préparation, l'UI affiche « Carnatic indien » sous BIC, tandis que DENNOR et PUD restent présents. La sauvegarde pré-2.c contient le region state 473 avec `country=218` (BIC), `capital=39618` et la seule province interne 39618. Le rapprochement avec la portion unique préparée identifie 39618 comme `xABADB1`.

## 15. Absence d'autre mutation

L'opérateur signale que tout le reste est nominal après préparation. Les portions DENNOR et PUD restent distinctes, aucun événement Sepoy réel ne s'ouvre automatiquement et aucune autre mutation territoriale ou diplomatique n'est observée à cette étape.

## 16. Tick 0

L'UI affiche zéro radical sur la portion BIC immédiatement après préparation. La portion contient environ 182,2 K hindous et 20,1 K sunnites.

## 17. Premier tick

Le 2 janvier, l'UI affiche encore zéro radical. Ce résultat ne suffit pas à invalider l'effet, conformément aux tests Bengal précédents.

## 18. Second tick

Le checkpoint pré-option n'a pas respecté la date prévue : malgré son nom `1776_01_03`, la sauvegarde est sérialisée au **2 janvier 1776, tick 5**. L'événement 2.c a également été exécuté le 2 janvier. Cette déviation temporelle est documentée sans rechargement ni relance. Elle n'affecte pas la preuve territoriale du défaut principal.

## 19. Baseline radicale

La sauvegarde pré-2.c contient dix objets de pops ciblés dans le region state 473 : sept hindous et trois sunnites. La somme `loyalists_and_radicals` vaut `-0.02425`, répartie en `-0.02185` hindoue et `-0.00240` sunnite. Le bloc national BIC contient simultanément `radicals_increase=0.02769` et une composante de population `0.02425`. Ces signaux sont compatibles avec la petite baseline préparée, alors que `population_radicals`, `trend_radicals` et l'UI restent à zéro. La baseline profonde est donc confirmée ; l'absence de sauvegarde avant préparation empêche seulement d'isoler les faibles radicaux organiques avec davantage de précision.

## 20. Sauvegarde pré-2.c

`HOTFIX_5C2E4C1R_C1_PRE_2C_1776_01_03.v3` :

- date réelle sérialisée : `1776.1.2` ;
- tick : 5 ;
- taille : 8 022 567 octets ;
- LastWriteTime UTC : 2026-07-20 02:19:59.3818285 ;
- SHA-256 : `0F217CBFD6019C35FC669F215537109B0FEA81C9669104486C70112667D1ADB7`.

## 21. Ouverture manuelle de l'événement

La décision C-1 ouvre `sepoy_mutiny_events.2`, « Le coup de grâce », sur BIC. La capture montre les quatre options attendues.

## 22. Sélection exclusive de 2.c

L'option « La domination de la Compagnie continuera au sud. Retournez à Madras. » est disponible. Son tooltip reconnaît Carnatic indien et annonce les effets de 10 % sur les religions hindoue et sunnite. L'opérateur sélectionne cette option et aucune autre.

## 23. Terminaison de la boucle

L'événement se ferme, la carte redistribuée est affichée, le jeu reste réactif et les sauvegardes suivantes sont écrites. Aucun blocage, crash ou symptôme de boucle non terminée n'est observé.

## 24. Pays joué final

Les trois sauvegardes portent le nom BIC « Compagnie des Indes orientales », avec `previous_played.idtype=218`. BIC reste donc le pays joué après 2.c.

## 25. Madras après 2.c

Immédiatement après 2.c, le region state 473 conserve seulement `previous_country=218` mais n'a plus de `country`, plus de capitale et plus aucune province. Il s'agit d'un objet vidé, pas d'un territoire à owner nul. Le region state 475 de PUD encode désormais 25 provinces par `39599 13 39614 10`, plage qui inclut la province interne 39618. DENNOR conserve son region state 474 inchangé.

## 26. Receveur

L'opérateur confirme par l'UI que PUD/Pudukkottai est l'owner de `xABADB1`. La sauvegarde prouve le même transfert : owner BIC avant, owner PUD après. En l'absence de controller séparé, le controller suit l'owner : BIC avant, PUD après.

## 27. Analyse du noyau Madras

Le critère `MADRAS_CORE_PRESERVED` échoue : BIC perd `xABADB1` et toute présence réelle dans `STATE_MADRAS`. PUD absorbe la province dans sa portion sans fusionner DENNOR. Le libellé « retraite vers Madras » ne correspond donc pas au résultat territorial réel.

## 28. Autres transferts prioritaires

La comparaison pré/finale montre le transfert prioritaire effectivement applicable de la portion BIC d'Awadh, region state 494, vers MUG. Les témoins restent cohérents : Pegu est partagé entre BUR, BIC et DENNOR ; Gujarat entre POR et BHV ; Tenasserim entre BUR et SIA ; Travancore entre TRA, NET et COC ; Delhi appartient à MUG ; Agra à MARATH et GAR ; Central Provinces à HYD, NAG et MARATH ; Bombay à POR, MARATH, SAT et KHP. La petite portion BIC de Pegu reste cohérente avec le code, car son transfert est seulement dans le `on_created` de BUR.

## 29. Statut COO

COO/Cooch Behar devient indépendant et quitte le bloc britannique au 2 janvier. La sauvegarde représente ce pays par l'objet 412, définition courante `BGL`, avec `power_bloc_leave_date=1776.1.2`. La capture de notification confirme qu'il a quitté le bloc britannique.

## 30. Statut JEY

JEY devient indépendant. L'objet pays 428 contient `power_bloc_leave_date=1776.1.2`, et l'UI montre son propre marché/capital après la redistribution.

## 31. Owners nuls ou incohérents

Aucun territoire observé ne possède un owner nul et aucune double attribution incohérente n'est visible. Le region state 473 sans owner est vide de provinces ; `xABADB1` appartient sans ambiguïté au region state PUD 475.

## 32. Résultat radical immédiat

La sauvegarde post-2.c immédiate est encore datée du 2 janvier, tick 5. Le state PUD fusionné contient `population_radicals=2466`. Les anciens objets de pops du state BIC vidé ne reçoivent pas `large_radicals` et leurs valeurs cœur sont remises à zéro lors de la disparition/absorption de la portion.

## 33. Premier tick après 2.c

Le relevé intermédiaire du 4 janvier n'a pas été fourni sous forme numérique distincte. Aucun changement territorial supplémentaire de Madras n'est signalé : PUD conserve `xABADB1`.

## 34. Second tick après 2.c

La sauvegarde finale est datée du 5 janvier, tick 17. PUD conserve les 25 provinces, DENNOR conserve `x10B060`, BIC reste absente de Madras et l'UI/state PUD affiche 2 466 radicaux.

## 35. Analyse des pops hindoues

Avant 2.c, sept objets hindous de la portion BIC portent une somme `loyalists_and_radicals=-0.02185`. Après la disparition du region state BIC, ces objets fantômes restent référencés à l'ancien state 473 mais avec une valeur nulle ; la population réelle est agrégée dans le grand state PUD. Aucun test de `large_radicals` sur un Madras encore BIC n'est donc possible.

## 36. Analyse des pops sunnites

Avant 2.c, trois objets sunnites portent une somme `loyalists_and_radicals=-0.00240`. Comme pour les hindous, l'absence d'effet final de 10 % sur une portion BIC est cohérente avec l'ordre du script : le transfert à PUD précède le bloc `large_radicals`.

## 37. Comparaison UI

L'UI affiche zéro radical sur Carnatic indien avant 2.c, malgré la baseline profonde. Après transfert, Tamil Nadu/PUD affiche 2 466 radicaux au 5 janvier. L'UI confirme aussi l'absence de BIC dans le state-region et la préservation de DENNOR.

## 38. Comparaison sérialisée

| Champ | Pré-2.c | Post immédiat | 5 janvier |
|---|---|---|---|
| date / tick | 1776.1.2 / 5 | 1776.1.2 / 5 | 1776.1.5 / 17 |
| state 473 | BIC, province 39618 | vide, ancien BIC | vide, ancien BIC |
| state 474 | DENNOR, province 39613 | identique | identique |
| state 475 | PUD, 24 provinces | PUD, 25 provinces | PUD, 25 provinces |
| `population_radicals` PUD | absent/0 | 2 466 | 2 466 |
| `trend_radicals` BIC | `{ 0 }` | `{ 0 }` | `{ 0 0 0 }` |
| `radicals_increase` BIC | 0.02769 | 0.02769 | 0.02769 |
| somme ciblée `loyalists_and_radicals` | -0.02425 | 0 sur l'ancien state vidé | 0 sur l'ancien state vidé |

## 39. Logs ciblés

Après fermeture, les recherches imposées avec `Get-ChildItem` et `Select-String` donnent zéro occurrence pour `zz_sepoy_test_c1`, `zz_sepoy_functional_test_c1`, `sepoy_mutiny_events.2`, `STATE_MADRAS`, `xABADB1`, `add_radicals_in_state`, `very_small_radicals`, `large_radicals`, `set_state_owner`, `Invalid scope`, `jomini_trigger_description` et le diagnostic de tooltip personnalisé. Aucun diagnostic direct ne vise C-1, 2.c ou le transfert de Madras. Le texte visible `NULL_STATE` dans le tooltip de préparation n'apparaît dans aucun log ; il est consigné comme défaut d'affichage du harnais, sans effet sur le verdict gameplay.

## 40. Diagnostics hors périmètre

Les logs contiennent 1 759 occurrences globales de `Invalid right side`, 2 007 de `Script system error`, 677 `PostValidate`, 427 `Unexpected token` et 16 avertissements BOM. Les principaux `Invalid right side` visent `01_natural_borders_of_france.txt`, `00_landowners.txt`, `07_american_mod_jes.txt`, des stratégies IA et des scripted buttons. Les 16 BOM visent des fichiers généraux, japonais, historiques et `00_states.txt`, jamais les quatre fichiers C-1. Ces diagnostics sont hors périmètre.

## 41. Intégrité des sauvegardes

| Sauvegarde | Taille | LastWriteTime UTC | SHA-256 original | Taille fondue | SHA-256 fondu |
|---|---:|---|---|---:|---|
| pré-2.c | 8 022 567 | 2026-07-20 02:19:59.3818285 | `0F217CBFD6019C35FC669F215537109B0FEA81C9669104486C70112667D1ADB7` | 107 961 061 | `EA303129EBED948F39D9454D21C858700174F2648948AA37DD072449C855D599` |
| post-2.c immédiat | 8 031 220 | 2026-07-20 02:34:42.8843793 | `BBD957F0E3EEEF945B3333F42EF5D9CC44222B4C205C123EB18CD3B1C745E57E` | 108 092 631 | `D3758497EE6D039EBF53C8526D5A9EABC548EF45878066324F3C8BDE6C9F3D09` |
| post-2.c final | 8 370 631 | 2026-07-20 02:36:28.6026094 | `91CD3A1186890152AC81D76AAA404C55D894D3BD9F217F4593415E41E8831C79` | 111 285 078 | `47F0F6BF5B3B04020740B6C2CC6FE3DD32188B5815A8C077BC22F39ACCFC96D1` |

Rakaly 0.8.18 a fondu uniquement des copies temporaires hors de `save games`, avec `melt --format vic3 --unknown-key stringify`, code retour 0. Le dossier temporaire a été supprimé. Les hashes originaux ont été recalculés après analyse et sont inchangés. La sauvegarde supplémentaire `sav_post_option_2.c.v3`, 8 030 961 octets, SHA-256 `4204A09B2ED3A965B623AAE7D05BEA720E82146283790DC39EC6D51105BDDD09`, a été conservée sans modification.

## 42. Intégrité des fichiers

Le fichier Sepoy du fork et de la copie reste à 63 422 octets, SHA-256 `FFB4060E659FB8A30691E26BA5BBDA838650EF11AB1760C89EDACFA2310D9BBE`, avec identité octet par octet. Le journal Sepoy et les vingt anciens harnais correspondaient au manifeste. Aucun fichier gameplay, harnais ou localisation n'a été modifié pendant le runtime ou l'analyse.

## 43. Verdict

**FAIL_C1_MADRAS_CORE_LOST**

Motif décisif : `xABADB1` passe de BIC à PUD pendant la boucle et BIC ne conserve aucune portion réelle de `STATE_MADRAS`. La boucle termine et les données restent cohérentes, mais l'intitulé « retraite vers Madras » exige la conservation d'un noyau réel.

La baseline radicale profonde est confirmée. L'absence de `large_radicals` sur Madras n'est pas classée `FAIL_C1_RADICAL_EFFECT`, car la portion quitte BIC avant le bloc final. Aucun `FAIL_C1_RUNTIME_ERROR` direct n'est ajouté : les logs ne visent ni C-1, ni 2.c, ni Madras.

## 44. Ce que le test valide

Le test valide l'accessibilité manuelle de 2.c, l'unique préparation FRA → BIC, la baseline radicale sérialisée malgré une UI nulle, la terminaison de la boucle, l'indépendance de COO et JEY, la cohérence générale des transferts et surtout l'absence de protection runtime du noyau Madras.

## 45. Suite recommandée

Une phase gameplay distincte devrait exclure explicitement le region state BIC de `STATE_MADRAS` de la boucle générique de 2.c, puis répéter C-1 pour vérifier la conservation du noyau et l'application finale de `large_radicals`. Cette phase ne doit pas modifier les corrections Bengal, Bombay, Travancore ou MARATH.

## 46. Fichiers créés

- `docs/reports/hotfix/HOTFIX_5C2E4C1R_SEPOY_C1_RUNTIME_TEST.md` ;
- `docs/reports/hotfix/HOTFIX_5C2E4C1R_C1_RUNTIME_RESULTS.csv`.

## 47. Confirmation Travancore/Bengal/Bombay/MARATH

Le harnais C-1 ne référence aucun de ces périmètres et aucun fichier correspondant n'a été modifié. Les portions sérialisées de Travancore, Bengal, Bombay et MARATH restent cohérentes avec le setup et les corrections préexistantes.

## 48. Confirmation `docs/research/technology/`

L'arborescence reste l'exception non suivie préexistante et n'a pas été touchée.

## 49. Confirmation stash MARATH

Le stash `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` reste présent. Il n'a été ni appliqué, ni modifié, ni supprimé.
