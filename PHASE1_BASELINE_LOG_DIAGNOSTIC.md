# PHASE 1 - Diagnostic baseline des logs Victoria 3 1.13

Mod : `1776_Age_of_Revolutions_fork`  
Branche d'audit : `migration-great-wave-1.13`  
Version du jeu detectee dans les logs : Victoria 3 `release/1.13.0` / The Great Wave  
Date du test : 2026-07-04

## 1. Resultat du test

### Etat observe

- Menu principal : OK.
- Ecran des objectifs : OK, mais plusieurs cles de localisation sont visibles directement.
- Selection de pays / carte 1776 : OK.
- Lancement d'une partie : non confirme de facon complete par les captures fournies.
- Passage du premier jour : non confirme.
- Crash : aucun crash explicite detecte dans les logs fournis.

### Indices dans les logs

- `debug.log` indique un chargement complet vers le jeu :
  - `Transition Empty->Game took: 328.07904 seconds`
- `debug.log` indique une sortie volontaire depuis le jeu :
  - `Quit: Quit from inside game`
  - `Transition Game->Empty took: 2.3065858 seconds`
- Aucun message de type exception fatale, crash dump ou fermeture brutale n'a ete identifie dans `error.log`, `game.log`, `system.log` ou `debug.log`.

### Conclusion de lancement

Le mod atteint au minimum le menu, l'ecran des objectifs et la selection pays. Les captures montrent la carte 1776 chargee au 1 janvier 1776, avec un pays selectionne et le bouton `Jouer` visible. La phase suivante doit verifier explicitement : clic sur `Jouer`, entree en partie active, pause/de-pause, puis passage au 2 janvier 1776.

## 2. Erreurs critiques

Ces erreurs sont les plus susceptibles d'empecher une partie stable ou de provoquer des erreurs de demarrage de scenario.

### Journal entry des famines indiennes

Fichier probable :

- `common/journal_entries/04_indian_famines.txt`

Erreurs observees :

- `Invalid right side during comparison 'sr'`
- Lignes signalees : `31`, `36`, `41`, `46`, `52`, `53`, `54`, `55`, `56`
- Occurrences : tres nombreuses, environ 45 par ligne pour la plupart des lignes signalees.

Diagnostic :

Le fichier utilise des comparaisons de region du type `region = sr:region_*` dans des blocs de journal entry. En 1.13, ce contexte semble rejeter le cote droit `sr`. Cette erreur pollue fortement `error.log` et peut casser l'evaluation de la journal entry concernee.

Priorite :

Critique pour nettoyer le chargement et stabiliser les journal entries liees a l'Inde.

### Batiments navals obsoletes

Fichiers probables :

- `common/history/buildings/00_west_europe.txt`
- `common/history/buildings/01_south_europe.txt`
- `common/history/buildings/03_north_africa.txt`
- `common/history/buildings/05_north_america.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/buildings/15_russia.txt`

Erreurs observees :

- `PostValidate of effect 'create_building' returned false`

Causes probables :

- `building_military_shipyard`
- `pm_military_shipbuilding_wooden`
- `pm_military_shipbuilding_wooden_2`

Diagnostic :

Ces references correspondent directement a l'ancien systeme naval / shipyards. The Great Wave / 1.13 a fortement modifie la marine, les chantiers navals, les convois et les formations navales. Ces fichiers sont donc au coeur de la migration.

Priorite :

Critique pour le demarrage economique et militaire des pays concernes.

### Formations militaires et navales obsoletes

Fichiers probables :

- `common/history/military_formations/00_military_formations_europe.txt`
- `common/history/military_formations/01_military_formations_north_america.txt`
- `common/history/military_formations/02_military_formations_south_america.txt`
- `common/history/military_formations/03_military_formations_north_africa.txt`
- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/military_formations/05_military_formations_india.txt`
- `common/history/military_formations/06_military_formations_asia.txt`
- `events/tech_events/military_tech_events_01.txt`

Erreurs observees :

- `PostValidate of effect 'create_military_formation' returned false`
- `PostValidate of effect 'create_character' returned false`

Causes probables :

- `unit_type:combat_unit_type_frigate`
- `unit_type:combat_unit_type_man_o_war`
- `unit_type:combat_unit_type_ironclad`
- anciennes formations navales incompatibles avec 1.13
- roles ou structures de commandants modifies

Diagnostic :

Les anciennes unites navales et formations militaires sont probablement incompatibles avec le nouveau systeme de The Great Wave. Le fichier europeen est le plus touche.

Priorite :

Critique pour obtenir une partie jouable au premier jour, surtout pour les puissances navales.

### Relations diplomatiques avec pays invalides

Fichiers probables :

- `common/history/diplomacy/00_relations.txt`
- `common/history/diplomacy/00_subject_relationships.txt`
- `common/country_definitions/*.txt`
- `common/history/countries/*.txt`

Erreur observee :

- `Assertion failed: Attempted to create relations for invalid countries!`

Tags a verifier en priorite :

- `AIT`
- `BLG`
- `CON`
- `DEI`
- `EGY`
- `GLD`
- `KTI`
- `LIB`
- `MAS`
- `MBS`
- `MOR`
- `ORA`
- `PLY`
- `SIL`
- `TRI`
- `TUG`
- `WTU`

Diagnostic :

Le log indique qu'au moins une relation est creee avec un pays invalide. Certains tags apparaissent dans les fichiers de diplomatie sans definition locale evidente dans le mod. Comme le jeu charge aussi du contenu vanilla selon les remplacements effectifs, cette liste doit etre confirmee tag par tag avant correction.

Priorite :

Critique si le clic sur `Jouer` ou le passage du premier jour declenche des erreurs diplomatiques.

### Interest group Landowners

Fichier probable :

- `common/interest_groups/00_landowners.txt`

Erreur observee :

- `has_law_or_variant trigger [ Given law is a variant, we expect the parent ]`
- Ligne signalee : `459`

Diagnostic :

Le trigger utilise probablement une loi variante la ou 1.13 attend le parent de la loi. Cela peut affecter les traits, conditions ou modificateurs des proprietaires fonciers.

Priorite :

Critique secondaire : probablement non bloquant pour le menu, mais a corriger avant test gameplay.

## 3. Erreurs importantes

Ces erreurs ne semblent pas empecher l'arrivee a la selection pays, mais elles peuvent casser des contenus historiques ou des boucles gameplay.

### Valeur absente dans East Indies

Fichier probable :

- `common/journal_entries/00_east_indies.txt`

Erreur observee :

- `Value of wrong type ... Got value of type 'none'`
- Ligne signalee : `109`

Diagnostic :

La journal entry lit `root.var:east_indies_revolt_var`, mais la variable semble absente ou non initialisee au moment du calcul. Cela peut casser l'affichage ou la progression de la journal entry.

### Custom tooltips invalides

Fichiers probables :

- `common/journal_entries/06_french_revolution_mod.txt`
- `common/journal_entries/07_american_mod_jes.txt`
- `common/journal_entries/07_iran_troubles_mod.txt`
- `common/journal_entries/07_poland_lithuania_mod.txt`
- `events/french_revolution_mod_events.txt`
- `events/iran_troubles_events_mod.txt`
- `events/new_imperialism_events_mod.txt`

Erreurs observees :

- `PostValidate of trigger 'custom_tooltip' returned false`
- `PostValidate of effect 'custom_tooltip' returned false`

Diagnostic :

Les tooltips custom sont nombreux dans les events et journal entries historiques. Certains blocs ou cles attendus par 1.13 ne valident plus. Cela peut casser l'affichage, les conditions visibles ou certains effets scriptes.

### Event namespaces invalides

Fichiers probables :

- `common/journal_entries/07_poland_lithuania_mod.txt`
- `common/journal_entries/01_french_monarchism.txt`
- `common/journal_entries/00_zanzibar.txt`
- fichiers `events/*.txt` associes a ces namespaces

Erreurs observees :

- `'random_mod_events.1' does not have a valid namespace`
- references a verifier :
  - `random_mod_events.1`
  - `french_pretenders.1`
  - `french_pretenders.10`
  - `zanzibar.2`

Diagnostic :

Certaines journal entries pointent vers des events dont le namespace est absent, mal declare ou non charge. Ces erreurs risquent de casser des chaines historiques.

### Institutions de pays coloniaux / compagnies

Fichiers probables :

- `common/history/countries/hbc - hubson bay company.txt`
- `common/history/countries/org -oregan.txt`

Erreur observee :

- `PostValidate of effect 'set_institution_investment_level' returned false`

Diagnostic :

Ces fichiers utilisent probablement des institutions qui ont change ou des conditions qui ne sont plus valides pour le type de pays concerne.

### Personnages et roles

Fichiers probables :

- `common/history/characters/aus.txt`
- `events/dreyfus_events.txt`
- `events/soi_events/00_ep1_caucasus_events.txt`
- `common/history/military_formations/*.txt`

Erreurs observees :

- `PostValidate of effect 'create_character' returned false`

Diagnostic :

Les roles de personnages, commandants, agitateurs ou structures liees aux formations peuvent avoir change depuis la version cible d'origine du mod.

## 4. Erreurs secondaires

Ces problemes sont visibles ou bruyants, mais ils ne bloquent pas le chargement initial.

### Localisation manquante visible en jeu

Constat visuel dans les captures :

- `objective_battle_for_india`
- `objective_battle_for_india_name_*`
- `objective_battle_for_india_desc_*`
- `objective_mercantile_republics`
- `objective_mercantile_republics_desc`
- `objective_mercantile_republics_name_*`
- `objective_tutorial_name_DENNOR`
- `objective_tutorial_desc_DENNOR`
- `objective_egalitarian_society_desc_SC1`

Diagnostic :

Les objectifs charges par le mod n'ont pas toutes leurs cles de localisation en francais ou dans les fichiers actuellement charges. Cela n'empeche pas le chargement, mais donne une interface incomplete.

### Events Japon / DLC orphelins

Erreurs observees :

- plusieurs events orphelins de type `ep2_meiji_pulse.*`, `ep2_sakoku.*`, `tenpo_events.*`, `zaibatsu.*`, `japan_religion.*`, `ryukyu_rivalry.*`

Diagnostic :

Ces messages peuvent venir de la combinaison entre fichiers vanilla/DLC et fichiers remplaces par le mod. A traiter apres les erreurs de lancement et les erreurs navales.

### Divers warnings techniques

Messages observes :

- `Unknown tooltip type`
- `CMapObjectManager::GetVisibleObjects: invalid camera index 0 requested`
- variables `used but is never set` ou `set but is never used`

Diagnostic :

Ces messages sont a surveiller, mais ils ne semblent pas expliquer un blocage de lancement dans cette baseline.

## 5. Fichiers responsables probables

| Probleme | Fichiers probables | Impact |
| --- | --- | --- |
| `Invalid right side during comparison 'sr'` | `common/journal_entries/04_indian_famines.txt` | Journal entry Inde, log tres pollue |
| `building_military_shipyard` / PM navales | `common/history/buildings/00_west_europe.txt`, `01_south_europe.txt`, `03_north_africa.txt`, `05_north_america.txt`, `11_east_asia.txt`, `15_russia.txt` | Economie navale et demarrage pays |
| Anciennes unites navales | `common/history/military_formations/*.txt`, `events/tech_events/military_tech_events_01.txt` | Flottes, commandants, formations |
| Relations de pays invalides | `common/history/diplomacy/00_relations.txt`, `00_subject_relationships.txt`, `common/country_definitions/*.txt` | Diplomatie initiale, assertion |
| Loi variante mal passee | `common/interest_groups/00_landowners.txt` | Interest groups / lois |
| Variable East Indies absente | `common/journal_entries/00_east_indies.txt` | Progression JE, affichage |
| Event namespace manquant | `common/journal_entries/07_poland_lithuania_mod.txt`, `01_french_monarchism.txt`, `00_zanzibar.txt`, events associes | Chaines historiques |
| Tooltips invalides | JE et events Revolution francaise, Amerique, Iran, Pologne-Lituanie, New Imperialism | UI, conditions, effets |
| Localisation objectifs | `localization/*`, fichiers d'objectifs associes | Interface seulement |

## 6. Ordre de correction recommande

1. `common/journal_entries/04_indian_famines.txt`
   - Objectif : supprimer la principale source d'erreurs repetitives dans `error.log`.

2. `common/history/buildings/00_west_europe.txt`
   - Objectif : traiter les premiers `create_building` invalides lies aux shipyards.

3. `common/history/buildings/01_south_europe.txt`
   - Objectif : meme correction pour l'Europe du Sud, tres touchee.

4. `common/history/buildings/03_north_africa.txt`
   - Objectif : verifier les shipyards et PM navales hors Europe.

5. `common/history/buildings/05_north_america.txt`
   - Objectif : verifier les shipyards americains et colonies.

6. `common/history/buildings/11_east_asia.txt`
   - Objectif : verifier les ports / shipyards asiatiques.

7. `common/history/buildings/15_russia.txt`
   - Objectif : verifier les shipyards russes et les PM associees.

8. `common/history/military_formations/00_military_formations_europe.txt`
   - Objectif : corriger le plus gros volume d'erreurs de formations.

9. Tous les autres fichiers `common/history/military_formations/*.txt`
   - Objectif : remplacer ou adapter les anciennes formations navales par region.

10. `events/tech_events/military_tech_events_01.txt`
    - Objectif : verifier les references aux anciennes unites comme `combat_unit_type_ironclad`.

11. `common/history/diplomacy/00_relations.txt`
    - Objectif : identifier la relation qui cible un pays invalide.

12. `common/history/diplomacy/00_subject_relationships.txt`
    - Objectif : verifier les dependances de sujets, protectorats et compagnies.

13. `common/country_definitions/*.txt` et `common/history/countries/*.txt`
    - Objectif : croiser tags definis, tags historiques et tags diplomatiques.

14. `common/interest_groups/00_landowners.txt`
    - Objectif : adapter `has_law_or_variant` aux attentes 1.13.

15. `common/journal_entries/00_east_indies.txt`
    - Objectif : initialiser ou securiser la variable de progression.

16. Journal entries avec event namespaces invalides :
    - `common/journal_entries/07_poland_lithuania_mod.txt`
    - `common/journal_entries/01_french_monarchism.txt`
    - `common/journal_entries/00_zanzibar.txt`

17. Events et journal entries avec `custom_tooltip` invalide :
    - Revolution francaise
    - Amerique
    - Iran
    - Pologne-Lituanie
    - New Imperialism

18. Localisation des objectifs
    - Objectif : corriger l'affichage visible, apres stabilisation du lancement.

## 7. Plan Phase 1

### Objectif A : menu principal OK

Etat actuel : atteint.

Tests a refaire apres chaque vague de correction :

- lancer Victoria 3 avec uniquement ce mod ;
- verifier que le menu principal apparait ;
- verifier que `error.log` ne contient pas de nouvelle erreur de parsing bloquante.

### Objectif B : selection pays OK

Etat actuel : atteint visuellement.

Tests recommandes :

- ouvrir chaque objectif ;
- selectionner au moins une nation recommandee par objectif ;
- verifier les pays centraux :
  - France
  - Grande-Bretagne / IREK
  - Russie
  - Qing
  - Suede / Dennor
  - Dai Nam
  - Prusse
  - Espagne
  - Japon
  - Etats-Unis / colonies nord-americaines
  - Compagnies et pays indiens : BIC, DEI, MARATH, HYD, DUR

### Objectif C : lancement partie OK

Etat actuel : a confirmer.

Test minimal :

- selectionner une grande puissance europeenne ;
- cliquer sur `Jouer` ;
- verifier l'arrivee dans l'interface de partie ;
- sauvegarder les logs immediatement apres l'entree en partie.

Nations prioritaires :

- Grande-Bretagne / IREK, car puissance navale majeure.
- France, car beaucoup de contenu revolutionnaire.
- Russie, car gros pays et contenu carte important.
- Qing, car grosse population et carte Asie.
- BIC ou autre acteur indien, car erreurs sur les famines indiennes et Battle for India.

### Objectif D : passage du premier jour OK

Etat actuel : a confirmer.

Test minimal :

- lancer une partie ;
- rester en pause 10 secondes pour verifier les erreurs immediates ;
- de-pause en vitesse 1 ;
- attendre le 2 janvier 1776 ;
- sauvegarder `error.log`, `game.log` et `debug.log`.

Points a surveiller :

- erreurs de creation de relations diplomatiques ;
- erreurs de formations militaires ;
- erreurs de batiments navals ;
- erreurs de journal entries ;
- erreurs d'economie liees aux goods ou production methods ;
- erreurs de commandants ou character roles.

## 8. Conclusion baseline

Le mod demarre mieux que prevu pour une migration majeure : il atteint le menu, les objectifs et la carte de selection pays sous Victoria 3 1.13. Aucun crash net n'est visible dans cette session.

Le risque principal n'est pas le chargement initial, mais la stabilite du scenario au moment de cliquer sur `Jouer` et de passer le premier jour. Les priorites absolues de Phase 1 sont :

1. nettoyer `common/journal_entries/04_indian_famines.txt`, car il domine `error.log` ;
2. adapter les shipyards et PM navales dans `common/history/buildings/*` ;
3. adapter les formations navales et anciennes unites dans `common/history/military_formations/*` ;
4. identifier la relation diplomatique qui cible un pays invalide ;
5. confirmer par test manuel que le 2 janvier 1776 est atteint sans crash.

Ce rapport ne modifie aucun fichier gameplay. Il sert uniquement de diagnostic de lancement pour guider les corrections minimales de Phase 1.
