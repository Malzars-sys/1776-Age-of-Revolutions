# Phase LOC-1 - Localisation francaise

## 1. Objectif

Supprimer les cles brutes visibles quand le mod est lance en francais, sans toucher au gameplay.

## 2. Perimetre

Fichiers modifies ou crees uniquement dans :
- `localization/french/*_l_french.yml`
- `PHASE_LOC_1_FRENCH_LOCALIZATION.md`

Aucun fichier `common`, `events`, `map_data`, historique, loi, technologie, journal entry gameplay, formation militaire ou navire n'a ete modifie.

## 3. Methode

Chaque fichier `localization/english/*_l_english.yml` du mod a maintenant un equivalent `localization/french/*_l_french.yml`.

Les cles sont conservees a l'identique. Les variables Paradox, scopes, references `$KEY$`, marqueurs `#v ...#!` et retours `\n` sont preserves.

La phase LOC-1 couvre toutes les cles pour eviter les cles brutes. Les textes les plus visibles ont ete traduits en priorite : objectifs, pays dynamiques, entrees de journal, boutons, evenements principaux, noms de pays et textes de saveur majeurs. Certains longs textes secondaires restent en anglais comme fallback lisible et devront etre repris dans une phase LOC-2.

## 4. Couverture

Total controle :
- 1033 cles anglaises detectees ;
- 1033 cles presentes dans les fichiers francais ;
- 0 cle manquante ;
- 255 valeurs differentes de l'anglais apres traduction prioritaire ;
- 778 valeurs encore identiques a l'anglais, principalement textes longs secondaires, noms propres ou fallback.

Detail par fichier :
- `76mod_event_l_french.yml` : 29 / 29 cles couvertes.
- `76mod_modifiers_l_french.yml` : 16 / 16 cles couvertes.
- `country_flavor_text_l_french.yml` : 324 / 324 cles couvertes.
- `mod_journal_entries_l_french.yml` : 127 / 127 cles couvertes.
- `mod_v2content_l_french.yml` : 472 / 472 cles couvertes.
- `NM_Countries_l_french.yml` : 56 / 56 cles couvertes.
- `NM_Names_l_french.yml` : 4 / 4 cles couvertes.
- `NM_power_blocs_l_french.yml` : 2 / 2 cles couvertes.
- `phase1_7d_sakoku_l_french.yml` : 3 / 3 cles couvertes.

## 5. Cles brutes explicitement traitees

- `objective_battle_for_india`
- `objective_mercantile_republics`
- `objective_tutorial_name_DENNOR`
- `objective_tutorial_desc_DENNOR`
- `objective_egalitarian_society_desc_SC1`
- `je_irish_question`
- `dyn_c_rus_empire`
- `DENNOR`
- `DENNOR_ADJ`

## 6. Verifications effectuees

- comparaison des cles anglais/francais : aucune cle manquante ;
- recherche des cles brutes signalees : toutes presentes dans `localization/french` ;
- recherche de mojibake `Ã` ou caractere de remplacement : aucun resultat ;
- fichiers francais ecrits en UTF-8 avec BOM.

## 7. Tests recommandes

1. Lancer Victoria 3 en francais avec uniquement le mod actif.
2. Verifier l'ecran des objectifs :
   - tutoriel / Danemark-Norvege ;
   - Battle for India ;
   - republiques marchandes ;
   - societe egalitaire.
3. Ouvrir une partie avec Japon, Grande-Bretagne, France, Danemark-Norvege, Russie, Venise, Durrani et Marathes.
4. Surveiller `error.log` pour `Missing localization` ou `Invalid localization`.
5. Noter les textes encore en anglais pour une phase LOC-2 de traduction fine.
