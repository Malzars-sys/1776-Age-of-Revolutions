# HOTFIX-5C2E4C1M — Validation runtime condensée de la correction B-1

## 1. Résumé

La correction territoriale de `sepoy_mutiny_events.2.b` réussit en runtime : BIC conserve ses portions de West Bengal et East Bengal, la boucle termine, les autres transferts observés restent cohérents et COO/JEY deviennent indépendants. En revanche, la préparation B-1 laisse les radicaux à zéro et l'effet final de 2.b ne produit aucune hausse visible. Verdict obligatoire : **`FAIL_B1_FIX_RADICAL_BASELINE`**. Sous-résultat territorial : **PASS**.

## 2. Préconditions

Le fork était sur `hotfix-dlc-audit`, HEAD `fbb7bc2 Protect Sepoy Bengal retreat core`, sans changement suivi et avec la seule exception non suivie `docs/research/technology/`. Le stash MARATH était intact. La copie contenait 964 fichiers, aucun `.git`, aucun `remote_file_id`, vingt fichiers de harnais et zéro divergence sur les 27 contrôles applicables du manifeste C1L.

Les sources Sepoy fork/copie faisaient 63 422 octets, SHA-256 `FFB4060E659FB8A30691E26BA5BBDA838650EF11AB1760C89EDACFA2310D9BBE`, identiques octet par octet.

## 3. Playset

Le harnais B-1 était effectivement chargé : `game.log:294–295` enregistre le namespace `zz_sepoy_test_b1` et le chargement de `events/zz_sepoy_functional_test_b1_events.txt`. Les décisions B-1 étaient visibles dans les captures opérateur. Le compte rendu final n'a toutefois pas répété textuellement la confirmation d'unicité du playset; aucun symptôme de doublon n'a été observé.

## 4. Session condensée

Une instance `victoria3` (PID 38884, démarrée le 18 juillet 2026 à 09:54:34 UTC) a été observée pendant la session. L'opérateur rapporte une seule nouvelle partie BIC, aucune fermeture intermédiaire, aucun crash, blocage ou redémarrage. Après les observations et la seconde sauvegarde, le processus était arrêté. Une seule fermeture finale est donc retenue.

## 5. Logs avant session

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 76 069 | 2026-07-17T21:43:39.4040045Z | `F544FD1C72DFDB9F27A40E4E2B91699FC9C9F7ED80BE1E8A5E07E3BF9AEFA16F` |
| `game.log` | 417 684 | 2026-07-17T21:43:39.4040045Z | `38CBB73EFFDC330E93FA2EC737BBA641011969C4C956195C72BCDC365A1FDFB2` |
| `debug.log` | 412 051 | 2026-07-17T21:43:46.2827122Z | `FD805F77BE23EE391574B0C67CE2A4AD1EE99A5B485DD339E39AC6289F1D7C7E` |

## 6. Situation initiale

BIC était le pays joué, sujet de GBR. COO et JEY étaient sujets de BIC. Les captures initiales attestent West Bengal partagé entre BIC et COO; East Bengal BIC; Bihar BIC; Awadh partagé AWA/BIC; Bundelkhand partagé MARATH/BIC; Northern Circars partagé BIC/JEY; Pegu partagé BUR/BIC/DEN.

## 7. Préparation B-1

La décision et l'option explicite de préparation ont été utilisées. Aucun territoire, controller ou rapport diplomatique n'a changé; l'événement Sepoy réel ne s'est pas ouvert automatiquement. Le marqueur de préparation a rendu disponible la décision d'ouverture.

## 8. Échec de la baseline radicale

Les radicaux visibles étaient 0 avant préparation et sont restés 0 après préparation dans les portions BIC de West/East Bengal. La condition obligatoire d'une baseline non nulle compatible avec `very_small_radicals = 0.01` n'est donc pas satisfaite.

L'explication opérateur « zéro de base » est consignée comme observation, mais elle n'est pas retenue comme sémantique prouvée de l'API. Cette phase ne modifie ni ne diagnostique dynamiquement le harnais : la cause exacte reste à auditer séparément.

## 9. Sauvegarde pré-option pendant la session

`HOTFIX_5C2E4C1M_B1_FIX_PRE_OPTION_1776_01_01.v3` a été contrôlée pendant que Victoria 3 restait ouvert :

- taille : 7 899 432 octets;
- LastWriteTime : `2026-07-18T10:07:48.1148764Z`;
- SHA-256 : `771B4AB364ABED9BCF306ED070ECCCD6D973F561AB155FB2F166957469080CA4`.

## 10. Ouverture et choix de 2.b

La décision B-1 a ouvert l'événement réel sur BIC. L'opérateur a sélectionné manuellement et uniquement 2.b. L'événement s'est fermé, la redistribution a terminé et le jeu est resté actif sans crash ni blocage.

## 11. West Bengal

PASS. La portion BIC initiale reste BIC. La portion COO demeure distincte; aucune fusion ou annexion artificielle n'est visible. La capture post-option montre explicitement les deux region states BIC et COO.

## 12. East Bengal

PASS. La portion BIC initiale reste BIC. Aucune portion tierce n'a été annexée artificiellement.

## 13. Bihar

PASS. Bihar passe de BIC à NAG/Nagpur, conformément au comportement C1K attendu.

## 14. Awadh

PASS. La région reste divisée entre AWA et la portion moghole détenue par Hindoustan/MUG; la portion BIC a été redistribuée par la branche attendue.

## 15. Bundelkhand

PASS. La portion BIC est absorbée par la Confédération marathe; le state final est MARATH.

## 16. Northern Circars

PASS. La portion BIC passe à HYD/Hyderabad et la portion JEY reste distincte.

## 17. Pegu

PASS. Le partage BUR/BIC/DEN demeure visible après 2.b, y compris le reliquat BIC déjà observé en C1K. La branche n'a pas régressé.

## 18. COO et JEY

PASS. Les deux anciens sujets deviennent indépendants. Leurs captures diplomatiques ne montrent plus BIC comme suzerain; leurs exemptions de service militaire avec GBR restent visibles. Les portions COO/JEY ne sont pas annexées par BIC.

## 19. Terminaison et propriétaires

La boucle termine, BIC reste jouée et conserve un noyau bengali réel. Aucun owner nul ou double attribution incohérente n'a été observé.

## 20. Radicaux après 2.b

West Bengal et East Bengal restent à 0 après 2.b. Il n'existe donc ni hausse mesurable compatible avec `large_radicals`, ni comparaison valide au-dessus d'une baseline préparée. L'absence de valeur hors North India ne suffit pas à valider le scope : résultat radical **FAIL_B1_FIX_RADICAL_BASELINE**, scope quantitatif inconclusif.

## 21. Sauvegarde post-option

`HOTFIX_5C2E4C1M_B1_FIX_POST_OPTION_1776_01_01.v3` est distincte :

- taille : 7 902 306 octets;
- LastWriteTime : `2026-07-18T22:31:16.8609998Z`;
- SHA-256 : `08845B6E7A572F0E8A71D8030A839DCBC562616022BB3C4B8B7B0F006B5776B9`.

## 22. Intégrité de la baseline après fermeture

Après la fermeture finale, la sauvegarde pré-option conserve exactement sa taille, son LastWriteTime et son SHA-256 relevés pendant la session. Verdict : baseline immuable, aucun `BLOCKED_B1_FIX_BASELINE_CHANGED`.

## 23. Logs après fermeture

Victoria 3 était arrêté avant l'analyse.

| Log | Taille | LastWriteTime UTC | SHA-256 |
|---|---:|---|---|
| `error.log` | 217 066 | 2026-07-18T22:31:34.5071814Z | `BEA42F7D7DE2EF31A7013605AFCD269A6FA7C3F41ECB163E218C5C8C6B61C0CA` |
| `game.log` | 312 129 | 2026-07-18T22:31:34.5071814Z | `459CC97E2F38C763D9A39E944AE0F440943EECB999578DDDCB4C195C278815E2` |
| `debug.log` | 22 531 | 2026-07-18T22:31:48.2878407Z | `DE073BF421C59C29676471B0945F30BA8057AF432B5EF88256E3899CD13EF32B` |

Les trois logs sont frais par rapport aux baselines.

## 24. Recherche ciblée des logs

La recherche imposée a été exécutée avec `Get-ChildItem` et `Select-String`, sans `rg`.

| Motif | Occurrences | Classement |
|---|---:|---|
| `zz_sepoy_test_b1` | 2 | chargement namespace + diagnostic sans option par défaut |
| `zz_sepoy_functional_test_b1` | 1 | chargement réussi du fichier event |
| `sepoy_mutiny_events.2` | 0 | aucune erreur ciblée |
| West/East Bengal, APIs radicales, `set_state_owner` | 0 | aucune erreur ciblée |
| `Invalid scope` | 0 | conforme |
| `Unexpected token` | 0 | conforme |
| diagnostics custom tooltip/BOM | 0 | conforme |
| `Invalid right side` | 204 | global, hors B-1/2.b |
| `Script system error` | 1 154 | global, hors B-1/2.b |
| `PostValidate` | 392 | global, hors B-1/2.b |

`game.log:746` indique `No default option in event zz_sepoy_test_b1.1`; cela correspond à la contrainte voulue de zéro choix automatique et n'est associé à aucun échec d'exécution.

Deux erreurs de chargement mentionnent `events/india_events/sepoy_mutiny_events.txt:2046` et `:2077` pour `region_persia`. Elles appartiennent exclusivement aux branches de `sepoy_mutiny_events.4`, hors option 2.b, hors lignes corrigées 956–1017 et préexistent à C1M. Elles sont consignées comme diagnostics Sepoy hors périmètre, sans attribution à la correction.

## 25. Intégrité des fichiers après runtime

Les 27 entrées applicables du manifeste C1L ont été recalculées : zéro différence de taille ou SHA-256. La copie contient toujours 964 fichiers, aucun `.git`, aucun `remote_file_id` et vingt fichiers de harnais. Aucun gameplay, journal, harnais, descriptor ou marqueur n'a changé pendant le runtime.

## 26. Résultat territorial

**PASS TERRITORIAL** : West Bengal BIC préservé; East Bengal BIC préservé; BIC jouée; boucle terminée; autres transferts cohérents; COO/JEY indépendants; aucun owner nul.

## 27. Résultat radical

**FAIL_B1_FIX_RADICAL_BASELINE** : 0 avant préparation, 0 après préparation, 0 après 2.b. Le scope et l'amplitude de `large_radicals` ne sont pas validés.

## 28. Verdict global

**`FAIL_B1_FIX_RADICAL_BASELINE`**

La correction du noyau bengali est validée en runtime, mais les critères C1M interdisent `PASS_B1_FIX_RUNTIME` tant que la préparation ne crée pas une baseline non nulle.

## 29. Risques et suite

Une phase séparée doit auditer pourquoi les deux appels `add_radicals_in_state` du harnais n'ont aucun résultat visible, sans remettre en cause ni modifier la correction territoriale validée. Aucun correctif n'a été appliqué pendant cette session.

## 30. Fichiers créés

- `docs/reports/hotfix/HOTFIX_5C2E4C1M_B1_FIX_RUNTIME_TEST.md`
- `docs/reports/hotfix/HOTFIX_5C2E4C1M_B1_FIX_RUNTIME_RESULTS.csv`

## 31. Git et stash

Les deux livrables C1M sont les seuls nouveaux fichiers de cette phase. `docs/research/technology/` reste l'exception concurrente non suivie. Le stash MARATH reste présent et intact. Aucun commit n'a été créé automatiquement.
