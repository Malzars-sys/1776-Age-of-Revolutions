# HOTFIX-5C2E4C1O — Test runtime discriminant du tick radical B-1

## 1. Résumé

Le test runtime a été exécuté dans une seule session BIC avec la copie jetable du mod. La baseline radicale est restée à zéro au premier tick journalier du 2 janvier 1776. Conformément au protocole, `sepoy_mutiny_events.2` et son option 2.b n'ont pas été exécutés.

L'analyse de la seconde sauvegarde apporte une précision importante : malgré son nom `...1776_01_02`, elle a été écrite au 3 janvier 1776. Son historique `trend_radicals` prouve 0 au 1er janvier, 0 au 2 janvier, puis 383 338 au 3 janvier. La préparation B-1 avait déjà sérialisé au tick 0 un signal interne `radicals_increase=3.83013`, mais la valeur nationale n'a été matérialisée qu'au second tick journalier.

Verdict : **FAIL_B1_RADICAL_BASELINE_AFTER_TICK**.

## 2. Intégrité initiale

- Racine : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD : `4f93927 Audit Sepoy Bengal radical baseline`.
- Aucun fichier suivi modifié ; seul `docs/research/technology/` était non suivi.
- Copie jetable : exactement 964 fichiers, dont 20 fichiers de harnais ; aucun `.git` et aucun `remote_file_id`.
- Manifeste C1L : 28 lignes non auto-référentes contrôlées, toutes conformes.
- `events/india_events/sepoy_mutiny_events.txt` dans le fork et la copie : 63 422 octets, SHA-256 `FFB4060E659FB8A30691E26BA5BBDA838650EF11AB1760C89EDACFA2310D9BBE`, identité octet par octet.
- Victoria 3 n'était pas lancé avant la session.

## 3. Playset

L'opérateur a confirmé avant lancement que seule la copie Disposable était active, que le fork principal était désactivé et qu'aucune autre copie 1776 ni version Workshop n'était active.

## 4. Logs avant session

Répertoire : `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs`.

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 217 066 | 2026-07-18 22:31:34.5071814Z | `BEA42F7D7DE2EF31A7013605AFCD269A6FA7C3F41ECB163E218C5C8C6B61C0CA` |
| `game.log` | 312 129 | 2026-07-18 22:31:34.5071814Z | `459CC97E2F38C763D9A39E944AE0F440943EECB999578DDDCB4C195C278815E2` |
| `debug.log` | 22 531 | 2026-07-18 22:31:48.2878407Z | `DE073BF421C59C29676471B0945F30BA8057AF432B5EF88256E3899CD13EF32B` |

## 5. Fiche opérateur unique

La fiche complète a été fournie avant lancement dans un message unique. Elle prescrivait : une seule ouverture ; une nouvelle partie BIC au 1er janvier ; pause immédiate ; contrôle des propriétaires de West/East Bengal ; relevés au tick 0 avant et après préparation ; sauvegarde tick 0 ; passage exact au 2 janvier ; mêmes relevés ; sauvegarde tick 1 ; arrêt immédiat sans 2.b si la baseline restait nulle, ou ouverture manuelle de l'événement et sélection exclusive de 2.b seulement si elle devenait mesurable ; une seule fermeture finale et aucune relance.

## 6. Nombre réel d'ouvertures et fermetures

D'après le compte rendu opérateur et les artefacts de session : une ouverture de Victoria 3, une nouvelle partie BIC, aucune session GBR, aucune fermeture intermédiaire, aucune relance et une fermeture finale propre. Le processus Victoria 3 était arrêté avant l'analyse.

## 7. Tick 0 avant préparation

Le 1er janvier 1776, le compteur national visible indiquait 0 radical. Les contrôles visuels fournis ne montrent aucune baseline radicale observable avant préparation. West Bengal comportait une portion BIC et une portion COO ; East Bengal appartenait à BIC.

## 8. Tick 0 après préparation

Toujours le 1er janvier, après la préparation B-1, le compteur national visible restait à 0. La décision d'ouverture réelle B-1 était disponible, sans ouverture automatique de l'événement. Aucune mutation territoriale ou diplomatique n'a été observée.

## 9. Sauvegarde tick 0

`HOTFIX_5C2E4C1O_B1_RADICAL_TICK0_AFTER_PREP_1776_01_01.v3` :

- taille : 7 910 491 octets ;
- LastWriteTime UTC : 2026-07-18 23:50:18.2169325Z ;
- SHA-256 : `D0706CA5B43577267E0EB32057B85256700093ADBFAC5F3367733F70AD7D2920` ;
- date sérialisée : `1776.1.1` ;
- marqueur B-1 prêt présent avec `tick=0` ;
- `trend_radicals={ 0 }` et absence de `population_radicals`, donc valeur nationale sérialisée égale à zéro ;
- signal interne déjà présent : `radicals_increase=3.83013`.

## 10. Passage exact au premier tick

L'opérateur a signalé avoir fait avancer un jour et avoir encore observé 0 radical au 2 janvier. Aucun fichier distinct arrêté au 2 janvier n'est disponible : la sauvegarde nommée pour le 2 janvier contient en réalité l'état du 3 janvier. L'historique sérialisé de cette sauvegarde permet néanmoins de contrôler rétrospectivement le premier tick : la deuxième valeur de `trend_radicals` est 0.

## 11. Tick 1 après préparation

Au premier tick journalier, le 2 janvier 1776, la baseline nationale est restée nulle : observation opérateur égale à 0 et historique sérialisé égal à 0. Le critère d'arrêt de la branche A était donc satisfait.

## 12. Sauvegarde tick 1

Le fichier `HOTFIX_5C2E4C1O_B1_RADICAL_TICK1_1776_01_02.v3` a :

- taille : 8 257 520 octets ;
- LastWriteTime UTC : 2026-07-18 23:51:02.2073104Z ;
- SHA-256 : `F4250106076DD1B4E21F700996CB26163340C36343B48F2C86BD9ED40BFC0EA7` ;
- date sérialisée réelle : `1776.1.3` ;
- `population_radicals=383338` ;
- `trend_radicals`, index 3 : `{ 0 0 383338 }`.

Le nom de fichier ne concorde donc pas avec son contenu. Cette dérive `SAVE_DATE_MISMATCH` signifie qu'un second tick a été inclus avant l'écriture effective de la sauvegarde ; elle ne rend pas le premier tick indéterminé puisque son zéro est conservé dans l'historique.

## 13. Décision de poursuivre ou d'arrêter avant 2.b

La baseline étant encore nulle au premier tick, l'opérateur a arrêté le scénario destructif, créé la sauvegarde puis quitté proprement le jeu. Cette décision est conforme à la branche A du protocole.

## 14. Éventuelle exécution de 2.b

`sepoy_mutiny_events.2` n'a pas été ouvert et l'option 2.b n'a pas été sélectionnée. Aucun test de `large_radicals` ne peut donc être conclu dans cette phase.

## 15. Éventuel tick supplémentaire

Aucun tick supplémentaire n'était prévu dans la branche A. Cependant, la seconde sauvegarde et la troisième capture sont datées du 3 janvier : elles révèlent fortuitement le second tick journalier. À ce checkpoint, 383 338 radicaux sont visibles et sérialisés, sans exécution de 2.b.

## 16. West/East Bengal

Les propriétaires sérialisés restent inchangés dans les deux sauvegardes :

- objet pays 218 : BIC ; objet pays 412 : COO ;
- state 14, East Bengal : BIC ;
- state 487, West Bengal : BIC ;
- state 488, West Bengal : COO.

Populations ciblées après le second tick : West Bengal BIC, hindous 13 071 323 et sunnites 3 822 116 ; East Bengal BIC, hindous 5 992 000 et sunnites 15 408 126. Les portions BIC sont préservées.

## 17. Comparaison UI

- 1er janvier avant préparation : 0 national.
- 1er janvier après préparation : 0 national.
- 2 janvier après le premier tick : 0 selon l'opérateur.
- 3 janvier après le second tick : environ 383K sur la capture, cohérent avec les 383 338 sérialisés.

Les vues par État et religion n'ont pas fourni de compte radical distinct exploitable ; aucune valeur de sous-groupe n'est inventée à partir du compteur national.

## 18. Comparaison sérialisée

La sauvegarde du 1er janvier contient `trend_radicals={ 0 }`, mais aussi un signal agrégé interne non nul (`radicals_increase=3.83013`). La sauvegarde réelle du 3 janvier contient `trend_radicals={ 0 0 383338 }`, `population_radicals=383338` et `radicals_increase=3.83577`.

Les hashes des blocs comparés changent :

- `pop_radicals_and_loyalists_statistics` : `C6563D94581CF37849A17C5B904A4134A2094432DCE813E34DCBA49F695105A2` au tick 0, puis `04590C97F7D712F0AA236C8C92B10EBAC7E43C47E8907670D77F237281980697` au 3 janvier ;
- `radicals_increase_data` : `5094A3A39E24B52433F4E3AC954A5FACB5A3810458A7F4C6D14B4F9A6ADAF743`, puis `55CA05CC19F5263330EAC0086ADDB29B152F3C915307629F9942576AF257B179`.

Les 383 338 radicaux représentent un ordre de grandeur compatible avec 1 % de la population BIC des portions bengalies ciblées, sans que cette compatibilité permette d'attribuer chaque radical à un objet pop individuel.

## 19. Cause retenue ou hypothèse réfutée

L'hypothèse « la baseline devient observable au premier tick journalier » est réfutée. Les preuves indiquent plutôt une **matérialisation différée jusqu'au second tick journalier** (`DEFERRED_UNTIL_SECOND_DAILY_TICK`). La présence du signal `radicals_increase` dès le tick 0 montre que l'API du harnais a produit un état interne ; elle ne doit donc pas être déclarée inopérante sur la seule base du compteur du premier tick.

## 20. Logs ciblés

Après fermeture :

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 387 969 | 2026-07-18 23:51:17.4813471Z | `14B654424841E39E5EB3B4E842113551DFB33E3C4DD8019EFF3AE436522108A0` |
| `game.log` | 190 629 | 2026-07-18 23:51:17.4813471Z | `1D427BC83BA988E28C77A422BD69651BB82B9FB507A922096BC07349EED23A75` |
| `debug.log` | 99 182 | 2026-07-18 23:51:22.4794829Z | `0B81422B93488918E1D6824F50BC85960DFBD933137AEBA4D40AB559D89125E8` |

La recherche imposée avec `Get-ChildItem` et `Select-String` ne trouve aucune occurrence ciblée de B-1, `sepoy_mutiny_events.2`, `add_radicals_in_state`, `very_small_radicals`, `large_radicals`, Bengal, erreur de scope, token inattendu ou avertissement BOM. Les recherches directes de `sepoy_mutiny_events.txt`, `zz_sepoy` et `functional_test_b1` ne retournent également rien.

## 21. Diagnostics hors périmètre

Les occurrences globales de `Script system error` sont 1 989 dans `error.log` et 977 dans `game.log`. `PostValidate` apparaît 558 fois dans `debug.log`. Elles ne citent ni B-1, ni le fichier Sepoy, ni les lignes de 2.b ; elles sont donc classées hors périmètre et ne constituent pas une erreur runtime directe du test.

## 22. Intégrité des sauvegardes

Les deux originaux ont uniquement été lus et hashés. La fonte Rakaly a été faite sur des copies temporaires hors de `save games`, avec Rakaly 0.8.18 et un code retour 0. Les fichiers fondus ont respectivement les SHA-256 `517BCE35DCE7E32B8AFF493CAA4B66D0E1B5EBC617444276FC5C1818ECCC17B0` et `A4BF50ADBE254455801F8D92972504E1E427C498A0AC68A0DD2B98C96CF50D50`. Les hashes et tailles des originaux sont restés inchangés après analyse.

## 23. Intégrité des fichiers

Aucun fichier gameplay, harnais ou localisation n'a été modifié. La copie jetable conserve 964 fichiers et le fichier Sepoy fork/copie conserve la taille, le hash et l'identité attendus. Le manifeste C1L reste conforme.

## 24. Verdict

**FAIL_B1_RADICAL_BASELINE_AFTER_TICK**

La baseline reste nulle après le premier tick. L'événement 2.b n'a donc pas été exécuté, conformément au verdict prescrit. L'apparition au second tick est une découverte complémentaire, mais ne transforme pas ce test en PASS et ne valide pas `large_radicals` de 2.b.

## 25. Suite recommandée

Prévoir une phase runtime distincte dont le protocole attend explicitement le 3 janvier et contrôle la matérialisation de la baseline au second tick avant d'ouvrir manuellement `sepoy_mutiny_events.2` et de choisir uniquement 2.b. Aucune correction de code n'est justifiée par cette phase seule.

## 26. Fichiers créés

- `docs/reports/hotfix/HOTFIX_5C2E4C1O_B1_RADICAL_TICK_RUNTIME_TEST.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1O_B1_RADICAL_TICK_RESULTS.csv`

## 27. Confirmation docs/research/technology/

Le répertoire non suivi préexistant `docs/research/technology/` n'a pas été touché.

## 28. Confirmation stash MARATH

Le stash MARATH préexistant reste intact : `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla`.
