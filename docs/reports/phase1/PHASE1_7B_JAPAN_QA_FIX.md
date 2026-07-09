# Phase 1.7B - Japan QA Fix

## 1. Resume des corrections

Cette phase corrige uniquement deux problemes QA observes sur le Japon apres les phases 1.6 et 1.7 :

- suppression de l'ancienne armee japonaise generique de 100 unites ;
- activation technique de l'entree de journal `je_sakoku`, correspondant a "The Locked Country".

L'Australie, le Moyen-Orient, les navires, les technologies, `je_tenpo_crisis` et `je_terakoya` n'ont pas ete modifies.

## 2. Diagnostic de l'armee de 100 unites

Source exacte :

- l'armee `1. Armee (Pays)` venait des anciens niveaux de `building_barrack` appartenant a `c:JAP` dans `common/history/buildings/11_east_asia.txt`.
- ces casernes totalisaient 100 niveaux :
  - `STATE_TOHOKU` : 15 ;
  - `STATE_KANTO` : 20 ;
  - `STATE_TOKAI` : 8 ;
  - `STATE_HOKUSHINETSU` : 7 ;
  - `STATE_KANSAI` : 20 ;
  - `STATE_KYUSHU` : 15 ;
  - `STATE_CHUGOKU` : 10 ;
  - `STATE_SHIKOKU` : 5.

Fichier responsable :

- `common/history/buildings/11_east_asia.txt`

Correction appliquee :

- retrait uniquement des huit blocs `create_building` de `building_barrack` appartenant a `c:JAP`.
- les casernes des autres pays de la region ne sont pas modifiees.
- les trois formations japonaises ajoutees en Phase 1.7 sont conservees.

## 3. Setup militaire japonais final

Formations attendues au depart :

- `Edo_Guard_Army` : 26 unites ;
- `Kinai_Guard_Army` : 20 unites ;
- `Kyushu_Guard_Army` : 12 unites.

Total approximatif attendu :

- 58 unites, sans l'ancienne formation generique de 100 unites.

Comparaison vanilla 1.13 :

- le setup conserve les trois formations japonaises vanilla The Great Wave ajoutees en Phase 1.7 ;
- la correction ne cree aucun commandant et n'ajoute aucun buff militaire.

## 4. Diagnostic de "The Locked Country"

ID exact :

- `je_sakoku`

Cause probable de l'absence en jeu :

- `common/history/countries/jap - japan.txt` ajoutait bien `add_journal_entry = { type = je_sakoku }` ;
- les logs signalaient cependant `PostValidate of effect 'add_journal_entry' returned false` sur cette ligne ;
- le fichier local `common/journal_entries/00_meiji_restoration.txt` du mod est ancien et ne definit pas `je_sakoku`.

Correction appliquee :

- ajout de `common/journal_entries/07_sakoku.txt` avec une definition minimale de `je_sakoku` ;
- l'entree est limitee a `c:JAP` ;
- elle reste possible tant que `law_sakoku` est active et que le Japon n'a pas ete force a ouvrir son marche ;
- elle reference les evenements Sakoku vanilla deja detectes dans les logs : `ep2_sakoku.3`, `ep2_sakoku.4`, `ep2_sakoku.5`.

## 5. Confirmation de `law_sakoku`

`law_sakoku` reste active dans `common/history/countries/jap - japan.txt`.

## 6. Confirmation de `je_tenpo_crisis`

`je_tenpo_crisis` n'est pas ajoutee au depart 1776.

## 7. Fichiers modifies

Modifies pour cette phase :

- `common/history/buildings/11_east_asia.txt`
- `common/journal_entries/07_sakoku.txt`
- `PHASE1_7B_JAPAN_QA_FIX.md`

Fichiers volontairement non modifies :

- `common/history/military_formations/06_military_formations_asia.txt`
- `common/history/countries/jap - japan.txt`
- fichiers de localisation
- technologies
- navires
- pays non japonais

## 8. Tests a faire

1. Lancer le mod seul et demarrer une partie avec le Japon.
2. Verifier que l'armee `1. Armee (Pays)` de 100 unites n'apparait plus.
3. Verifier que les formations japonaises visibles sont :
   - Armee de la garde d'Edo ;
   - Armee de la garde de Kinai ;
   - Armee de la garde de Kyushu.
4. Verifier que le total militaire initial est proche de 58 unites.
5. Verifier que l'entree de journal "The Locked Country" / `je_sakoku` apparait au demarrage.
6. Verifier que `law_sakoku` reste active.
7. Verifier que `je_tenpo_crisis` et `je_terakoya` n'apparaissent pas au depart.
8. Surveiller `error.log` et `debug.log` pour confirmer qu'il n'y a plus de PostValidate sur `add_journal_entry = { type = je_sakoku }`.
