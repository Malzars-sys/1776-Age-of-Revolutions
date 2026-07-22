# HOTFIX-5C2E4C1AD — Disponibilité runtime de l’option Sepoy 2.e

## 1. Résumé

Le scénario E-2 est concluant. Après préparation, BIC possède une portion Bombay réelle et ne possède plus aucune portion réelle de West Bengal, intégralement agrégée chez COO. Dans `sepoy_mutiny_events.2`, seule l’option d’abandon de l’Inde est affichée : 2.e « Bombay tient bon » est absente de l’interface. Verdict principal : `PASS_E2_OPTION_BLOCKED`. Sous-verdict : `PASS_E2_OPTION_HIDDEN`. Interprétation : `TRIGGER_WEST_BENGAL_GOVERNS_2E_CONFIRMED`.

## 2. État Git

Racine exacte : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`. Branche : `hotfix-dlc-audit`. HEAD initial : `f19fbd7 Prepare Sepoy Bombay availability test`. Aucun fichier suivi n’était modifié. Seul `docs/research/technology/` était non suivi.

## 3. Vérification de la copie

La copie comptait exactement 980 fichiers et 36 harnais : quatre E-2, quatre E-1, quatre E1D et vingt-quatre anciens harnais. Aucun `.git`, aucun `remote_file_id`. Les 44 contrôles non auto-référentiels du manifeste C1AC correspondaient. Sepoy fork/copie faisait 63 658 octets, SHA-256 `51F489F00FA6CB2D7BBF1D1FDC587104F2A17D4932187DAA8BBE954F7312A9FB`, avec identité octet par octet.

## 4. Playset

L’opérateur a confirmé que seule `1776_Age_of_Revolutions_sepoy_test` était active ; fork principal, autres copies 1776 et versions Workshop étaient désactivés.

## 5. Logs initiaux

| Log | Taille | LastWriteTime | SHA-256 |
|---|---:|---|---|
| `error.log` | 46 004 | 2026-07-22T16:56:32.8074329+02:00 | `8C09498A630BDCCA528AB6B4B13D22B980FDBED8EAEF22E09C1D8E3E73C307E7` |
| `game.log` | 379 509 | 2026-07-22T16:56:32.8074329+02:00 | `905FD8FE09BEEEA8490DFA678F0B74CCEA5381AC58312D13D8CAFEA670F80132` |
| `debug.log` | 492 554 | 2026-07-22T16:56:42.8137584+02:00 | `4CDFAE4367FB186AE3BBE8F8D6FE1D9F9935467E9E006217999220C7B9F747CB` |

## 6. Fiche opérateur unique

La fiche complète de 34 étapes a été fournie avant lancement dans un seul message. Elle imposait une nouvelle partie BIC, la préparation E-2, deux noms de sauvegarde exacts, l’inspection sans clic de 2.e, une recharge unique, aucune option réelle, une fermeture finale et aucune relance.

## 7. Nombre d’ouvertures, rechargements et fermetures

Compte rendu opérateur : une ouverture, une nouvelle partie BIC, une recharge `RELOAD_1`, aucune session GBR, aucune fermeture intermédiaire et une fermeture finale. Après fermeture, Victoria 3, launcher et dowser étaient arrêtés.

## 8. Baseline Bombay

Avant préparation, POR possédait `x51F0A0`/39686 et BIC ne possédait aucune portion Bombay. MARATH, SAT et KHP possédaient respectivement 25, 10 et 3 provinces.

## 9. Baseline West Bengal BIC

La nouvelle partie contenait une portion réelle West Bengal BIC, correspondant au state 487 avant mutation, et la capitale initiale BIC se trouvait dans West Bengal.

## 10. Baseline West Bengal COO

COO possédait sa portion réelle initiale de West Bengal et restait sujet de BIC.

## 11. Baseline East Bengal

East Bengal était un state BIC réel, non vide et distinct. La capture opérateur le montre sous le nom « Bengale de l’Est », propriétaire Compagnie des Indes orientales, avec environ 21,5 M d’habitants.

## 12. Préparation E-2

L’option explicite de préparation a été choisie. Le marqueur `zz_sepoy_test_e2_ready` est sérialisé dans les deux sauvegardes. Aucun appel radical, indépendance ou choix de l’événement réel n’est sérialisé.

## 13. Bombay après préparation

Dans PRE et POST, state 482 a `country=218` BIC, `capital=39686` et `provinces={39686 0}`. Ses 23 objets de pops totalisent 111 597 travailleurs et 334 794 dépendants, soit 446 391 personnes. MARATH/SAT/KHP restent 25/10/3 et leurs encodages territoriaux sont inchangés entre les checkpoints.

## 14. West Bengal après préparation

State 487 conserve seulement `previous_country=218`, sans `country`, sans province réelle et avec zéro population active. State 488 a `country=412` COO, `capital=40300`, `provinces={40292 16}` et 17 512 663 habitants. COO a donc agrégé sa portion initiale et toute l’ancienne portion BIC, sans owner nul ni double attribution.

## 15. East Bengal après préparation

State 14 a `country=218`, `previous_country=218`, `capital=40324` et `provinces={40309 29}`, soit les trente provinces attendues. Ses 51 objets de pops, dont 34 actifs, totalisent 5 656 667 travailleurs et 15 900 007 dépendants, soit 21 556 674 personnes. PRE et POST sont identiques sur ces valeurs.

## 16. Capitale BIC

BIC sérialise `capital=14` dans PRE et POST : après la perte de West Bengal, sa capitale moteur est East Bengal. Le harnais n’appelle aucun effet de capitale ; il s’agit de la relocalisation automatique attendue.

## 17. Statut COO

COO (pays 412) conserve `capital=488`, `market=0` et le pacte `puppet` dont BIC 218 est le premier pays. Il reste sujet de BIC dans PRE et POST.

## 18. Statut JEY

JEY (pays 428) conserve `capital=463`, `market=0` et le pacte `puppet` avec BIC 218. Il reste sujet de BIC dans PRE et POST.

## 19. Sauvegarde pré-événement

`HOTFIX_5C2E4C1AD_E2_PRE_EVENT.v3` : 7 911 168 octets, LastWriteTime `2026-07-22T19:08:36.2579135+02:00`, SHA-256 `C4155C0C88472CE16FEF1C428A548FC58AA7479F3AE2A049E06DA30E463F0EB9`, date sérialisée `1776.1.1`.

## 20. Ouverture de sepoy_mutiny_events.2

La décision E-2 a ouvert « Le coup de grâce » sur BIC. L’opérateur n’a sélectionné aucune option réelle.

## 21. Présentation UI de 2.e

La capture montre un seul bouton : « L’Inde est perdue. Laissons Whitehall se disputer nos ressources restantes. » Toutes les autres options, dont 2.e « Bombay tient bon », sont absentes. Classement : `OPTION_2E_HIDDEN`.

## 22. Tooltip ou condition échouée

2.e étant cachée, aucun bouton ni tooltip propre à 2.e n’était accessible. Le contrôle statique C1AC établit que son unique trigger est `any_scope_state` sur `STATE_WEST_BENGAL`, sans aucune condition Bombay. L’état runtime satisfait Bombay BIC mais pas West Bengal BIC.

## 23. Absence de sélection réelle

Aucune option de `sepoy_mutiny_events.2` n’a été choisie. La seule référence Sepoy jetable sérialisée est l’événement de préparation `zz_sepoy_test_e2.1`; aucun marqueur d’option réelle ni référence sérialisée à `sepoy_mutiny_events.2` n’est présent.

## 24. Recharge unique

L’opérateur a rechargé `HOTFIX_5C2E4C1AD_E2_PRE_EVENT` sans quitter Victoria 3 et a compté exactement `RELOAD_1`.

## 25. Bombay après recharge

Bombay state 482 reste BIC, réel, non vide, avec 39686 et 446 391 habitants. MARATH/SAT/KHP restent à 25/10/3.

## 26. West Bengal après recharge

State 487 reste vide et sans country réel ; state 488 reste COO avec la totalité de West Bengal et la même population totale.

## 27. East Bengal après recharge

State 14 reste BIC, réel, non vide, avec les mêmes trente provinces et 21 556 674 habitants.

## 28. Sujets après recharge

Les pactes `puppet` BIC→COO et BIC→JEY sont identiques. COO et JEY restent sur le marché britannique `market=0`; aucune indépendance ni marché propre n’est créé.

## 29. Contrôle de fuite d’effet

`PASS_NO_EVENT_EFFECT_LEAK`. Le pays joué reste BIC 218, les owners/provinces contrôlés sont identiques, les pactes et marchés sont inchangés, aucun sujet n’est libéré et aucune redistribution 2.e n’a lieu. West Bengal conserve exactement 17 512 663 habitants. Une micro-évolution interne de consolidation des pops COO (69 à 68 objets actifs) et environ 1,57 personne pondérée de loyalistes/radicaux est non matérielle, sans changement d’effectifs, et n’a pas la signature de `large_radicals`.

## 30. Comparaison sérialisée

PRE et POST ont la même date `1776.1.1`, le même playthrough, le même pays joué 218 et la même topologie. Le compteur interne `seed_count` passe de 75051 à 75262 et certains compteurs/budgets sont réémis après recharge ; ces différences techniques ne correspondent à aucun effet de l’événement réel.

## 31. Logs ciblés

Après fermeture : `error.log` 117 339 octets/SHA `2DF87D4AD697A4D1F066064F941EAD1B4891B2F898B8C42DFD8214E032E1D8D2`; `game.log` 160 814/SHA `69B0A1415CA4063A9A2471D0F683E9318C888768EDE15BB52285F7DB6CFFE0AC`; `debug.log` 38 689/SHA `F637A7D693CBF9A1136BB70701044DEC6D9514F27D3771E3A5CCF65D7511CBBE`. Les recherches prescrites donnent zéro occurrence E-2, événement 2, Bombay/West/East Bengal, `x51F0A0`, `set_state_owner`, `Invalid scope`, tooltip E-2 et avertissement BOM.

## 32. Diagnostics hors périmètre

Les diagnostics globaux sont : `Invalid right side` 1 307, `Script system error` 1 309, `PostValidate` 164, `Unexpected token` 0. Aucun ne contient les identifiants E-2/Sepoy ou les states ciblés ; ils sont classés hors périmètre.

## 33. Intégrité des sauvegardes

Rakaly 0.8.18 a fondu uniquement des copies temporaires hors de `save games` avec `melt --format vic3 --unknown-key stringify`. Les copies, fontes, archives et binaires temporaires ont été supprimés. Après suppression, les originaux conservent exactement leurs tailles et SHA-256 initiaux.

## 34. Intégrité des fichiers

Après runtime : 980 fichiers, 36 harnais et 44/44 contrôles C1AC conformes. Sepoy fork/copie reste inchangé au SHA attendu. Aucun gameplay, harnais, localisation, descripteur ou sauvegarde originale n’a été modifié.

## 35. Verdict principal

`PASS_E2_OPTION_BLOCKED`.

## 36. Sous-verdict UI

`PASS_E2_OPTION_HIDDEN`.

## 37. Interprétation du trigger

`TRIGGER_WEST_BENGAL_GOVERNS_2E_CONFIRMED`. Bombay BIC est réel et peuplé, mais 2.e est cachée lorsque BIC ne possède plus West Bengal. Le trigger réel ne teste que West Bengal.

## 38. Conséquence fonctionnelle

Le texte et l’effet annoncé de 2.e désignent Bombay comme noyau de retraite, alors que l’accès est gouverné par West Bengal. La contradiction localisation/script est reproduite. La redistribution ultérieure de West Bengal après un choix de 2.e reste normale et n’est pas reclassée comme défaut.

## 39. Correction éventuellement recommandée

Ouvrir une phase corrective distincte pour étudier le remplacement du trigger West Bengal par une vérification d’une portion réelle BIC de `STATE_BOMBAY`. Ne recommander ni protection ni conservation de West Bengal dans cette correction.

## 40. Fichiers créés

- `docs/reports/hotfix/HOTFIX_5C2E4C1AD_SEPOY_E2_AVAILABILITY_RUNTIME.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1AD_E2_AVAILABILITY_RESULTS.csv`

## 41. Confirmation gameplay inchangé

Aucun gameplay, trigger réel, harnais, localisation ou sauvegarde originale n’a été modifié. Aucune option réelle n’a été sélectionnée.

## 42. Confirmation MARATH/Bengal/Madras/Bombay/Travancore

MARATH/SAT/KHP restent 25/10/3 ; East Bengal reste BIC ; Bombay reste BIC ; West Bengal est intégralement COO comme préparé. Aucune protection Bengal/Madras/Bombay, aucun fichier Travancore et aucune donnée MARATH n’ont été modifiés.

## 43. Confirmation docs/research/technology/

Le répertoire non suivi `docs/research/technology/` est resté intact et hors périmètre.

## 44. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est resté intact. Aucun commit automatique n’a été créé.
