# Phase 1.9 - Chaine japonaise pre-Tenpo 1776 -> crise Tenpo

## 1. Resume de la phase

Cette phase ajoute une petite chaine japonaise, limitee au Japon, pour faire vivre la periode 1776-1833 avant de declencher la crise Tenpo vanilla. `je_tenpo_crisis` ne demarre pas en 1776 : elle est ajoutee uniquement par l'evenement final, apres plusieurs variables de progression.

## 2. Chemin vanilla utilise

Reference vanilla The Great Wave utilisee :

`C:\Games\Victoria 3 The Great Wave\game`

## 3. Audit vanilla de `je_tenpo_crisis`

La journal entry vanilla est definie dans :

`C:\Games\Victoria 3 The Great Wave\game\common\journal_entries\07_tenpo_crisis.txt`

Elle utilise :
- `tenpo_events.1` comme evenement d'introduction ;
- `tenpo_events.2`, `tenpo_events.7`, `tenpo_events.8` et `japan_events.31` dans sa pulse mensuelle ;
- `tenpo_events.3` en resolution reussie ;
- `tenpo_events.4` en timeout ;
- la variable `tenpo_gdp_goal`.

Dans ce mod, `.metadata/metadata.json` declare `replace_path` sur `events` et `common/journal_entries`. Pour eviter une reference absente au moment ou `je_tenpo_crisis` est ajoutee, les fichiers vanilla strictement necessaires ont ete importes :
- `common/journal_entries/07_tenpo_crisis.txt`, copie identique de la vanilla ;
- `events/japan_events/ep2_tenpo_events.txt`, copie identique de la vanilla ;
- `events/japan_events/ep2_japan_events_03.txt`, version minimale contenant seulement `japan_events.31`, car la JE Tenpo le reference directement.

## 4. Methode de declenchement choisie

Un `on_yearly_pulse` minimal a ete cree dans :

`common/on_actions/phase1_japan_tenpo_on_actions.txt`

Il cible directement `c:JAP` et declenche uniquement les six evenements `phase1_japan_tenpo.*` quand leurs fenetres sont valides. Chaque evenement se protege aussi lui-meme avec :
- `c:JAP ?= this` ;
- une fenetre de dates stricte ;
- une variable anti-repetition ;
- des conditions de lois quand elles sont utiles.

Ce n'est pas un monthly pulse mondial lourd.

## 5. Evenements ajoutes

Fichier :

`events/phase1_japan_tenpo_events.txt`

Evenements :
- `phase1_japan_tenpo.1` : Les lecons de la famine Tenmei, 1787-1790.
- `phase1_japan_tenpo.2` : Les reformes Kansei, 1789-1793.
- `phase1_japan_tenpo.3` : Repousser les navires etrangers, 1825-1827.
- `phase1_japan_tenpo.4` : Des recoltes inquietantes, 1832-1833.
- `phase1_japan_tenpo.5` : Le prix du riz grimpe, 1833-1834.
- `phase1_japan_tenpo.6` : La famine Tenpo commence, 1833-1835.

## 6. Conditions de chaque evenement

`phase1_japan_tenpo.1`
- Japon uniquement.
- `game_date >= 1787.1.1`, `game_date < 1791.1.1`.
- Pas de variable `phase1_japan_tenmei_lessons_done`.

`phase1_japan_tenpo.2`
- Japon uniquement.
- `game_date >= 1789.1.1`, `game_date < 1794.1.1`.
- Variable `phase1_japan_tenmei_lessons_done`.
- Pas de variable `phase1_japan_kansei_reforms_done`.

`phase1_japan_tenpo.3`
- Japon uniquement.
- `game_date >= 1825.1.1`, `game_date < 1828.1.1`.
- `has_law = law_type:law_sakoku`.
- Pas de variable `phase1_japan_foreign_ships_edict_done`.

`phase1_japan_tenpo.4`
- Japon uniquement.
- `game_date >= 1832.1.1`, `game_date < 1834.1.1`.
- `has_law = law_type:law_bakufu`.
- `has_law = law_type:law_sakoku`.
- Pas de variable `phase1_japan_bad_harvests_1832`.

`phase1_japan_tenpo.5`
- Japon uniquement.
- `game_date >= 1833.1.1`, `game_date < 1835.1.1`.
- Variable `phase1_japan_bad_harvests_1832`.
- Pas de variable `phase1_japan_rice_price_crisis_done`.

`phase1_japan_tenpo.6`
- Japon uniquement.
- DLC feature `ep2_content`.
- `game_date >= 1833.1.1`, `game_date < 1836.1.1`.
- Variables `phase1_japan_bad_harvests_1832` et `phase1_japan_rice_price_crisis_done`.
- Pas de variable `phase1_japan_tenpo_crisis_started_from_1776_mod`.
- `je_tenpo_crisis` absente.

## 7. Variables utilisees

- `phase1_japan_tenmei_lessons_done`
- `phase1_japan_kansei_reforms_done`
- `phase1_japan_foreign_ships_edict_done`
- `phase1_japan_bad_harvests_1832`
- `phase1_japan_rice_price_crisis_done`
- `phase1_japan_tenpo_crisis_started_from_1776_mod`
- `tenpo_gdp_goal`, initialisee au declenchement final pour la JE vanilla.

## 8. Effets appliques

Les cinq premiers evenements restent narratifs et legers :
- variables anti-repetition ;
- petits ajouts de loyalistes ou radicaux par strate.

L'evenement final :
- initialise `tenpo_gdp_goal` a 135% du PIB japonais courant ;
- ajoute `je_tenpo_crisis` ;
- declenche `tenpo_events.1` un jour plus tard pour conserver l'introduction vanilla.

## 9. Pourquoi `je_tenpo_crisis` ne demarre pas en 1776

Aucun fichier d'historique pays n'a ete modifie. `common/history/countries/jap - japan.txt` continue d'ajouter `je_sakoku`, mais pas `je_tenpo_crisis`.

La crise Tenpo demande maintenant la progression de la chaine jusqu'aux variables de 1832/1833, puis l'evenement final verifie que la JE n'est pas deja active.

## 10. Declenchement vers 1833/1834

Le declenchement naturel passe par :
1. Tenmei, 1787-1790.
2. Kansei, 1789-1793.
3. Edit contre les navires etrangers, 1825-1827.
4. Mauvaises recoltes, 1832-1833.
5. Hausse du prix du riz, 1833-1834.
6. Ajout de `je_tenpo_crisis`, 1833-1835.

## 11. Fichiers modifies ou crees

Fichiers crees pour la chaine :
- `events/phase1_japan_tenpo_events.txt`
- `common/on_actions/phase1_japan_tenpo_on_actions.txt`
- `localization/english/phase1_japan_tenpo_l_english.yml`
- `localization/french/phase1_japan_tenpo_l_french.yml`

Imports vanilla necessaires a cause des `replace_path` :
- `common/journal_entries/07_tenpo_crisis.txt`
- `events/japan_events/ep2_tenpo_events.txt`
- `events/japan_events/ep2_japan_events_03.txt`

Rapport :
- `PHASE1_9_JAPAN_TENPO_PRECURSOR_CHAIN.md`

## 12. Fichiers volontairement non modifies

Non modifies :
- Australie et Nouvelle-Zelande ;
- Moyen-Orient ;
- technologies ;
- navires ;
- formations militaires ;
- pays non japonais ;
- `common/journal_entries/07_sakoku.txt` ;
- `je_terakoya` ;
- historiques Japon/Ryukyu/Ezochi/Sakhaline.

## 13. Verification encodage/localisation

Les fichiers de localisation de la chaine ont ete crees avec BOM UTF-8 :
- `localization/english/phase1_japan_tenpo_l_english.yml`
- `localization/french/phase1_japan_tenpo_l_french.yml`

Les localisations vanilla de `je_tenpo_crisis`, `tenpo_events.*` et `japan_events.31` restent fournies par la vanilla, car `localization` n'est pas remplace par `replace_path`.

## 14. Tests a refaire en jeu

Tester au lancement 1776 :
- `je_sakoku` active ;
- `je_tenpo_crisis` absente ;
- aucun evenement `phase1_japan_tenpo.*` immediat.

Tester avec avance rapide ou console :
- `event phase1_japan_tenpo.1 JAP`
- `event phase1_japan_tenpo.2 JAP`
- `event phase1_japan_tenpo.3 JAP`
- `event phase1_japan_tenpo.4 JAP`
- `event phase1_japan_tenpo.5 JAP`
- `event phase1_japan_tenpo.6 JAP`

Surveiller les logs :
- `phase1_japan_tenpo`
- `je_tenpo_crisis`
- `tenpo_events`
- `japan_events.31`
- `PostValidate`
- `Missing localization`
- `Invalid localization`

## 15. Risques restants

La chaine utilise un `on_yearly_pulse` additionnel, donc il faut verifier en jeu que les entrees d'un meme `on_action` se fusionnent bien avec les autres fichiers du mod.

La JE Tenpo vanilla depend de nombreux contenus The Great Wave hors `events` et `common/journal_entries` : scripted buttons, script values, modifiers, localisations et character templates. Ces dossiers ne sont pas en `replace_path`, donc ils devraient rester accessibles via la vanilla. Si les logs signalent une reference absente, il faudra importer uniquement la definition manquante.

`events/japan_events/ep2_japan_events_03.txt` contient seulement `japan_events.31`, pas tout le fichier vanilla, pour eviter d'ajouter des evenements japonais non necessaires a cette phase.
