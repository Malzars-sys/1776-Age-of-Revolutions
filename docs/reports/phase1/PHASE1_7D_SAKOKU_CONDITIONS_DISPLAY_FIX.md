# Phase 1.7D - Sakoku condition display fix

## 1. Probleme corrige

`je_sakoku` apparaissait bien en jeu, mais les conditions automatiques generees depuis les triggers `has_law` etaient illisibles en francais.

Exemple observe :
- `Shogunat japonaisShogunat japonais n'Shogunat japonais pas la loi sakoku promulguee`
- `Shogunat japonaisShogunat japonais n'Shogunat japonais pas la loi frontieres fermees promulguee`

## 2. Comparaison vanilla

Reference utilisee :
- `C:\Games\Victoria 3 The Great Wave\game\common\journal_entries\07_sakoku.txt`

La definition du mod etait deja presque identique a la vanilla The Great Wave. La vanilla utilise directement :
- `NOR = { has_law = law_type:law_sakoku has_law = law_type:law_closed_borders }`
- `NOT = { has_law = law_type:law_monarchy }`

Le probleme vient donc du rendu automatique de ces triggers en francais, pas d'une mecanique Sakoku manquante.

## 3. Correction appliquee

`common/journal_entries/07_sakoku.txt` garde la logique vanilla, mais les conditions de fin et d'echec sont enveloppees dans des `custom_tooltip`.

Conditions de fin :
- ne plus avoir `law_sakoku` ;
- ne plus avoir `law_closed_borders`.

Condition d'echec modifiee pour l'affichage :
- ne plus avoir `law_monarchy`.

La condition deja propre `ruler_is_japanese_emperor_tt` est conservee.

## 4. Localisation ajoutee

Fichiers ajoutes :
- `localization/french/phase1_7d_sakoku_l_french.yml`
- `localization/english/phase1_7d_sakoku_l_english.yml`

Ces fichiers ajoutent uniquement trois tooltips Sakoku :
- `je_sakoku_no_sakoku_law_tt`
- `je_sakoku_no_closed_borders_law_tt`
- `je_sakoku_no_monarchy_law_tt`

## 5. Fichiers modifies

- `common/journal_entries/07_sakoku.txt`
- `localization/french/phase1_7d_sakoku_l_french.yml`
- `localization/english/phase1_7d_sakoku_l_english.yml`
- `PHASE1_7D_SAKOKU_CONDITIONS_DISPLAY_FIX.md`

## 6. Fichiers volontairement non modifies

- Australie / Nouvelle-Zelande ;
- Moyen-Orient ;
- technologies ;
- navires ;
- formations militaires ;
- `je_tenpo_crisis` ;
- `je_terakoya` ;
- pays non japonais.

## 7. Tests a faire

1. Lancer le mod seul en francais.
2. Demarrer comme Japon.
3. Ouvrir `Le pays enferme`.
4. Verifier que les conditions affichent des phrases lisibles au lieu des repetitions `Shogunat japonaisShogunat japonais`.
5. Verifier que l'entree reste epinglee au demarrage.
6. Surveiller `error.log` pour des cles manquantes :
   - `je_sakoku_no_sakoku_law_tt`
   - `je_sakoku_no_closed_borders_law_tt`
   - `je_sakoku_no_monarchy_law_tt`
