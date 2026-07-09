# Phase 1.7C - Sakoku / The Locked Country

## 1. Objectif

Corriger qualitativement `je_sakoku` apres le test en jeu :
- mauvaise icone ;
- entree non epinglee au tableau de bord ;
- conditions de completion/fail affichees de facon brute ou incomprehensible ;
- evenements `ep2_sakoku.*` absents du mod alors que `events` est remplace par `.metadata/metadata.json`.

## 2. Reference vanilla utilisee

La reference vanilla The Great Wave / Victoria 3 1.13 utilisee est :

`C:\Games\Victoria 3 The Great Wave\game`

Le sous-dossier `game` existe et a ete utilise pour les comparaisons.

Fichiers vanilla consultes :
- `common/journal_entries/07_sakoku.txt`
- `events/japan_events/ep2_sakoku_events.txt`
- `common/scripted_buttons/sakoku_buttons.txt`
- `common/static_modifiers/00_ep2_05_modifiers.txt`
- `localization/english/ep2_07_l_english.yml`

## 3. Cause des problemes

La definition locale de `common/journal_entries/07_sakoku.txt` etait une version minimale ajoutee en Phase 1.7B.

Problemes identifies :
- icone locale : `event_trade.dds`, alors que la vanilla utilise `event_scales.dds` ;
- pinning local : `should_be_pinned_by_default = yes`, moins fidele a la JE vanilla que `should_be_pinned_by_default_uninvolved_or_context = yes` ;
- completion locale : usage de `has_law_or_variant` et d'une variable `japan_forced_to_open_market`, ce qui donnait des conditions mal affichees ;
- pulse local : appelait directement `ep2_sakoku.4` et `ep2_sakoku.5`, alors que ces evenements sont des resolutions de completion/fail ;
- `.metadata/metadata.json` remplace `events`, donc les evenements vanilla `ep2_sakoku.2` a `ep2_sakoku.5` doivent exister dans le mod.

## 4. Fichiers modifies

- `common/journal_entries/07_sakoku.txt`
- `events/japan_events/ep2_sakoku_events.txt`
- `PHASE1_7C_SAKOKU_JOURNAL_FIX.md`

## 5. Corrections appliquees

`common/journal_entries/07_sakoku.txt` a ete remplace par la definition vanilla The Great Wave :
- icone `gfx/interface/icons/event_icons/event_scales.dds` ;
- `scripted_button = je_sakoku_stop_being_closed_button` ;
- pulse annuel limite a `ep2_sakoku.3` ;
- completion si le Japon n'a plus `law_sakoku` ni `law_closed_borders` ;
- resolution complete via `ep2_sakoku.4` ;
- fail via restauration imperiale ou fin de monarchie, avec tooltip `ruler_is_japanese_emperor_tt` ;
- resolution fail via `ep2_sakoku.5` ;
- pinning vanilla `should_be_pinned_by_default_uninvolved_or_context = yes`.

`events/japan_events/ep2_sakoku_events.txt` a ete ajoute depuis la vanilla The Great Wave :
- `ep2_sakoku.2` : bouton pour forcer la fin de Sakoku ;
- `ep2_sakoku.3` : Morrison Incident ;
- `ep2_sakoku.4` : The Picked Lock ;
- `ep2_sakoku.5` : Rusted Shut.

## 6. Fichiers volontairement non modifies

- `common/journal_entries/00_meiji_restoration.txt`
- `common/journal_entries/07_tenpo_crisis.txt`
- `common/journal_entries/07_terakoya.txt` ou toute entree equivalente
- `events/japan_events/ep2_tenpo_events.txt`
- `common/history/military_formations/*`
- `common/history/countries/jap - japan.txt`
- localisations
- technologies, navires, Australie, Moyen-Orient

Le bouton `je_sakoku_stop_being_closed_button` n'a pas ete copie : `common/scripted_buttons` n'est pas dans les `replace_paths`, donc le bouton vanilla reste disponible.

## 7. Adaptation au depart 1776

Aucune adaptation historique lourde n'a ete faite.

Le fichier `common/history/countries/jap - japan.txt` contient deja :
- `activate_law = law_type:law_sakoku`
- `activate_law = law_type:law_closed_borders`
- `add_journal_entry = { type = je_sakoku }`

La definition vanilla fonctionne donc avec le depart 1776 actuel sans toucher aux formations militaires japonaises.

## 8. Risques restants

- Les textes affiches dependent des localisations vanilla, car aucun fichier de localisation n'a ete modifie.
- Si le launcher ne charge pas correctement les contenus vanilla hors `replace_paths`, il faudra verifier en jeu que le bouton scripte est bien disponible quand la variable `je_sakoku_maybe_we_should_open_up` est posee.
- Les evenements ont `dlc = dlc018`, comme en vanilla The Great Wave.

## 9. Tests a faire

1. Lancer le mod seul.
2. Demarrer en Japon.
3. Verifier que `The Locked Country` / `Le pays enferme` :
   - utilise l'icone de balances ;
   - est epingle au tableau de bord ;
   - affiche des conditions lisibles ;
   - ne montre plus `Le pays a cette variable` pour Sakoku.
4. Laisser tourner au moins un an pour verifier que seul `ep2_sakoku.3` peut sortir du pulse annuel.
5. Tester une ouverture du pays :
   - enlever `law_sakoku` et `law_closed_borders` pour verifier `ep2_sakoku.4` ;
   - verifier que la restauration imperiale / fin de monarchie declenche bien `ep2_sakoku.5`.
6. Surveiller `error.log` pour :
   - event `ep2_sakoku.*` introuvable ;
   - scripted button `je_sakoku_stop_being_closed_button` introuvable ;
   - modifier ou notification Sakoku introuvable.
