# HOTFIX-5C2E4C1AA — BOM E1D et préparation du rerun propre

## 1. Résumé

Les deux scripts E1D de la copie jetable ont reçu exactement un BOM UTF-8 `EF BB BF`. Leur texte décodé, leurs LF, leur indentation et leur logique sont inchangés. Aucun fichier gameplay, E-1 ou de localisation n’a été modifié. Le futur runtime est réduit à une branche A Bombay complète et une branche C propre, avec un seul rechargement et une sauvegarde pré-2.e obligatoire. Verdict : `READY_FOR_E1_RADICAL_CLEAN_RERUN`.

## 2. État Git

- Racine : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`.
- Branche : `hotfix-dlc-audit`.
- HEAD initial : `320acfe Document inconclusive Sepoy radical diagnostic`.
- Aucun fichier suivi n’était modifié.
- Seule exception non suivie initiale : `docs/research/technology/`.
- Aucun processus Victoria 3, launcher, dowser ou Paradox n’était actif.
- Aucun commit automatique n’a été créé.

## 3. Copie jetable

Avant et après correction, la copie contient exactement 976 fichiers et 32 fichiers de harnais `zz_*`, dont quatre E1D et quatre E-1. Elle ne contient aucun `.git` ni `remote_file_id`. Les 39 contrôles non auto-référentiels du manifeste C1Y étaient conformes avant correction. L’empreinte agrégée des 974 fichiers autres que les deux scripts corrigés est restée `84951AE24C148E9D9E645942EA3B3342D5F6578F72E8DB6286C930CA6651C266`.

## 4. Résultat C1Z

C1Z reste classé `INCONCLUSIVE_E1_RADICAL_DIAGNOSTIC`. Il a montré un effet SMALL_BOMBAY immédiat, deux contrôles West Bengal matériels et un signal Bombay matériel sous 2.e. Bombay a été conservé et West Bengal perdu. Ces preuves ne sont pas reclassées en PASS.

## 5. Limites du protocole C1Z

Le contrôle direct LARGE_BOMBAY manque. Trois sauvegardes ont été mal nommées. Surtout, la branche C conserve la signature `-11.90044` du contrôle LARGE_WEST_BENGAL sur la pop 14845 : sa base radicale n’était pas propre. Aucune cause racine ne peut être tirée de cette branche.

## 6. Avertissement BOM décision

Dans `debug.log` final C1Z, SHA-256 `E0F01E2B98AB2A685174EAA6AFABE0D41D6A7D52DD541BF64445CFA660EDB695`, ligne 2182 :

`File 'common/decisions/zz_sepoy_radical_diagnostic_e1d.txt' should be in utf8-bom encoding (will try to use it anyways)`.

Avant correction : 855 octets, SHA-256 `015724557E3ACFED476F3C0700A155CC5EA88C45735BA69CD18BFEADBCF89725`, premiers octets `23 20 44`, UTF-8 valide, BOM absent, 42 LF, zéro CR.

## 7. Avertissement BOM événement

Dans le même `debug.log`, ligne 1952 :

`File 'events/zz_sepoy_radical_diagnostic_e1d_events.txt' should be in utf8-bom encoding (will try to use it anyways)`.

Avant correction : 2 446 octets, SHA-256 `2E1FF0C381F9686BCDB06AB0685B71A4376422B98441C98C0438D22848ACF86E`, premiers octets `23 20 44`, UTF-8 valide, BOM absent, 101 LF, zéro CR.

## 8. Octets avant

Les deux scripts commençaient directement par le commentaire ASCII `# D`, soit `23 20 44`. Aucun BOM correct, incorrect ou dupliqué n’était présent. Leur contenu complet se décodait sans erreur avec un décodeur UTF-8 strict. Les fins de ligne étaient exclusivement LF.

## 9. Correction appliquée

La seule mutation binaire est l’ajout de `EF BB BF` à l’offset zéro de chaque script. Aucun caractère du texte décodé n’a été ajouté, retiré ou remplacé ; aucun CR n’a été créé.

## 10. Octets après

| Script | Taille après | SHA-256 après | Six premiers octets | BOM |
|---|---:|---|---|---|
| décision E1D | 858 | `D0605A942B70B0CABE1159AA296000A4FAA0A5F1D65359C785EE0B638F24A750` | `EF BB BF 23 20 44` | exactement un |
| événement E1D | 2 449 | `B962465965502A6F4532957EF41EC654072EF28B7EE9A68AE850BD74280E89F8` | `EF BB BF 23 20 44` | exactement un |

Les deux fichiers restent UTF-8 valides et LF-only.

## 11. Preuve de texte identique

Après retrait du BOM, le SHA-256 sémantique de la décision reste `015724557E3ACFED476F3C0700A155CC5EA88C45735BA69CD18BFEADBCF89725`. Celui de l’événement reste `2E1FF0C381F9686BCDB06AB0685B71A4376422B98441C98C0438D22848ACF86E`. La décision conserve 43 lignes et 42 LF ; l’événement 102 lignes et 101 LF.

## 12. Preuve de logique identique

La décision conserve 11 accolades ouvrantes et 11 fermantes ; l’événement 29 et 29. Le texte sans BOM est octet-identique avant/après : identifiants, ordre, déclencheurs, scopes, valeurs, indentation et commentaires sont identiques. Le diff sémantique est nul.

## 13. Structure E1D

- namespace `zz_sepoy_test_e1d` : une occurrence déclarative ;
- décision `zz_sepoy_test_e1d_open` : une ;
- événement `zz_sepoy_test_e1d.1` : un ;
- cinq options manuelles : SMALL_BOMBAY, LARGE_BOMBAY conditionné par le marqueur small, SMALL_WEST_BENGAL_CONTROL, LARGE_WEST_BENGAL_CONTROL conditionné par le marqueur small Bengal, et CANCEL sans effet ;
- quatre `add_radicals_in_state` et quatre affectations de marqueurs ;
- zéro `set_state_owner`, zéro appel `sepoy_mutiny_events.2`, zéro hasard et zéro option automatique.

## 14. Localisations inchangées

Les localisations E1D anglaise et française sont inchangées : respectivement 1 280 octets/SHA `3185D2F93957C115DD2AA17FBA06B5F7EEE6ACFE2769A65E40D3BC2653E2EE4B` et 1 441 octets/SHA `59349FE6D79851952B6B1EF1246613BED04A9049BC9740FE33051C26A65B157D`. Elles conservent leur BOM UTF-8 et leurs LF.

## 15. Gameplay inchangé

`events/india_events/sepoy_mutiny_events.txt` reste inchangé dans le fork et la copie : 63 658 octets, SHA-256 `51F489F00FA6CB2D7BBF1D1FDC587104F2A17D4932187DAA8BBE954F7312A9FB`. Le journal Sepoy, les fichiers E-1, les protections Bombay, West Bengal, MARATH, SAT, KHP, Travancore et toutes les sauvegardes restent hors du diff.

## 16. Conclusions C1Z conservées

1. SMALL_BOMBAY fonctionne immédiatement.
2. Les contrôles West Bengal fonctionnent.
3. L’API et les script values sont chargées.
4. Les effets observés ne sont pas exclusivement différés.
5. Le ciblage Bombay n’est pas intrinsèquement nul.
6. Le test direct LARGE_BOMBAY manque.
7. La branche C est contaminée.
8. Aucune cause racine n’est prouvée.
9. Aucun correctif gameplay n’est justifié.
10. West Bengal reste une décision fonctionnelle différée.

## 17. Pourquoi Bengal n’est pas répété

C1Z a déjà fourni un contrôle positif small et large sur West Bengal dans la même session. Le futur runtime doit seulement combler LARGE_BOMBAY et obtenir une branche 2.e propre. Répéter Bengal consommerait un rechargement et réintroduirait le principal risque de contamination sans apporter de discrimination nouvelle.

## 18. Plan runtime réduit

Une seule ouverture Victoria 3, une seule nouvelle partie BIC, aucune session GBR, une seule recharge dans la même session, aucune fermeture intermédiaire, une seule fermeture finale et aucune branche Bengal. L’analyse des sauvegardes et logs n’a lieu qu’après la fermeture.

Base commune : démarrer BIC au 1er janvier, exécuter la préparation E-1, attendre le second tick quotidien du 3 janvier, vérifier Bombay et West Bengal BIC, puis créer l’immuable `HOTFIX_5C2E4C1AB_E1D_BASE` sans jamais l’écraser.

## 19. Branche A complète

1. Ouvrir E1D et choisir SMALL_BOMBAY.
2. Confirmer l’option et le marqueur small ; sauvegarder `HOTFIX_5C2E4C1AB_A_SMALL_IMMEDIATE`.
3. Avancer exactement un tick ; sauvegarder `HOTFIX_5C2E4C1AB_A_SMALL_TICK1`.
4. Ouvrir E1D et choisir LARGE_BOMBAY.
5. Confirmer le marqueur large ; sauvegarder `HOTFIX_5C2E4C1AB_A_LARGE_IMMEDIATE`.
6. Avancer exactement un tick ; sauvegarder `HOTFIX_5C2E4C1AB_A_LARGE_TICK1`.

Après chaque sauvegarde, confirmer dans la liste le nom exact, la branche, l’option précédente, le marqueur attendu et la date visible.

## 20. Branche C propre

1. Recharger `HOTFIX_5C2E4C1AB_E1D_BASE` sans quitter Victoria 3 ; compter exactement `RELOAD_1`.
2. Ne prendre aucune option E1D après ce rechargement.
3. Créer immédiatement `HOTFIX_5C2E4C1AB_C_PRE_2E_CLEAN`.
4. Ouvrir `sepoy_mutiny_events.2` avec la décision E-1 existante et choisir uniquement 2.e.
5. Attendre la fin de la boucle, vérifier Bombay BIC et relever West Bengal séparément.
6. Sauvegarder `HOTFIX_5C2E4C1AB_C_2E_IMMEDIATE`, avancer exactement un tick, puis sauvegarder `HOTFIX_5C2E4C1AB_C_2E_TICK1`.
7. Fermer Victoria 3 une seule fois.

## 21. Barrière anti-contamination

Avant toute interprétation de 2.e, l’analyse profonde doit comparer `C_PRE_2E_CLEAN` à `E1D_BASE` et exiger : aucun marqueur small/large E1D ; pop Bombay revenue exactement à sa baseline ; pop West Bengal 14845 revenue exactement à sa baseline ; absence de `-11.90044` ; mêmes owners, provinces et états territoriaux Bombay/West Bengal ; même date et tick, ou toute différence explicitement justifiée.

Si une empreinte A subsiste : `BLOCKED_E1AB_BASE_CONTAMINATED`. Aucune interprétation différentielle de 2.e n’est alors autorisée.

## 22. Barrière de nommage des sauvegardes

Chaque nom doit décrire l’effet réellement exécuté. SMALL et LARGE ne peuvent pas être réutilisés pour un autre checkpoint. Le futur rapport doit vérifier les marqueurs sérialisés avant de croire les noms. Toute divergence nom/marqueur/date est consignée avant calcul.

## 23. Matrice d’interprétation

| Résultat propre | Interprétation autorisée |
|---|---|
| SMALL et LARGE directs fonctionnent ; 2.e fonctionne | `C1X_RADICAL_FAILURE_NON_REPRODUCIBLE_OR_TIMING_DEPENDENT` |
| SMALL et LARGE directs fonctionnent ; 2.e échoue | `ROOT_CAUSE_E1_RADICAL_2E_PATH_PROVEN` |
| SMALL fonctionne ; LARGE direct échoue | `E1_RADICAL_LARGE_DIRECT_ANOMALY` |
| SMALL et LARGE directs échouent après BOM | `E1D_BOMBAY_CONTROL_FAILURE` |
| C reste contaminée | `BLOCKED_E1AB_BASE_CONTAMINATED` |

Aucun `ROOT_CAUSE_*_PROVEN` ne doit être employé si plusieurs causes restent compatibles.

## 24. Validation statique

Deux fichiers seulement ont changé dans la copie, chacun de trois octets. La copie reste à 976 fichiers et 32 harnais, sans ajout ni suppression. Les 974 autres fichiers ont une empreinte agrégée identique. Les quatre E-1, deux localisations E1D, vingt-quatre anciens harnais, Sepoy, journal, descripteurs et marqueur sont inchangés. Aucun jeu ou launcher n’a été lancé.

## 25. Résumé du manifeste

Le manifeste C1AA inventorie 41 lignes : deux scripts `MODIFIED_BOM_ONLY`, deux localisations E1D, quatre E-1, vingt-quatre anciens harnais, deux Sepoy, deux journaux, trois descripteurs/marqueur et deux livrables C1AA. Le manifeste lui-même est auto-référentiel.

## 26. Verdict

`READY_FOR_E1_RADICAL_CLEAN_RERUN`.

Les BOM sont uniques et valides, les LF et le texte sont préservés, la logique et le gameplay sont inchangés, et le plan AB contient une seule ouverture et une seule recharge avec barrières explicites.

## 27. Fichiers modifiés dans la copie

- `common/decisions/zz_sepoy_radical_diagnostic_e1d.txt` — BOM uniquement ;
- `events/zz_sepoy_radical_diagnostic_e1d_events.txt` — BOM uniquement.

## 28. Fichiers créés dans le fork

- `docs/reports/hotfix/HOTFIX_5C2E4C1AA_E1D_BOM_AND_RERUN_PREPARATION.md` ;
- `docs/reports/hotfix/HOTFIX_5C2E4C1AA_E1D_BOM_FIX_MANIFEST.csv`.

## 29. WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED

`WEST_BENGAL_FUNCTIONAL_DECISION_DEFERRED` reste en vigueur. AA ne protège, ne corrige et ne réinterprète pas West Bengal.

## 30. Confirmation docs/research/technology/

Le répertoire préexistant non suivi `docs/research/technology/` est resté entièrement hors périmètre et n’a pas été touché.

## 31. Confirmation stash MARATH

`stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` est intact. Aucun `stash apply`, `pop` ou `drop` n’a été exécuté.
