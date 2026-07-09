# Phase NAVY-1A-bis - Great Power Admirals Fix

## 1. Resume

Cette phase corrige uniquement les amiraux directement lies aux flottes initiales de Grande-Bretagne, France et Espagne.

Les flottes reactives en NAVY-1A n'ont pas ete modifiees dans leurs effectifs, types de navires ou `hq_region`. La correction porte sur :

- les amiraux anonymes qui etaient generes par le jeu ;
- les anachronismes evidents pour 1776 ;
- les `save_scope_as` dupliques ou ambigus ;
- les transferts d'amiraux vers les formations navales.

## 2. Fichiers modifies

- `common/history/military_formations/00_military_formations_europe.txt`
- `PHASE_NAVY_1A_BIS_GREAT_POWER_ADMIRALS_FIX.md`

Aucun fichier de batiments, lois, technologies, navires, Japon, Australasie ou Moyen-Orient n'a ete modifie.

## 3. Amiraux avant correction

Les noms observes en jeu etaient :

- Grande-Bretagne : Alan Mair, Neville Graham, Thomas Cochrane, George Cockburn.
- France : Michel Stevenot reutilise sur plusieurs escadres.
- Espagne : Pedro Rodriguez.

Dans les fichiers, Alan Mair, Neville Graham, Michel Stevenot et Pedro Rodriguez n'etaient pas ecrits comme personnages historiques. Ils venaient de `create_character` sans `first_name`/`last_name`, donc de personnages generes automatiquement par le jeu.

## 4. Problemes detectes

- France, Escadre du Nord : `frenchnavy1_gen` etait utilise a la fois comme scope de formation et comme scope du premier amiral. Les transferts pointaient ensuite vers le meme scope, ce qui pouvait provoquer une attribution confuse.
- France, Escadre de la Mediterranee : trois amiraux etaient generes sans nom historique.
- Grande-Bretagne, Portsmouth : plusieurs amiraux etaient anonymes, dont deux utilisaient le meme `save_scope_as = fleet_gbr2_adm`.
- Grande-Bretagne, Plymouth : deux amiraux anonymes, dont un n'etait pas transfere a la formation.
- Grande-Bretagne, Mediterranee : Thomas Cochrane etait anachronique pour 1776.
- Grande-Bretagne, Amerique du Nord : George Cockburn etait anachronique pour 1776.
- Grande-Bretagne, East Indies / China : James Dundas etait remplace par un choix naval plus coherent.
- Espagne : deux amiraux anonymes etaient generes pour la Real Armada Espanola.

Les blocs utilisent deja `is_admiral = yes`, qui est conserve.

## 5. Amiraux retenus apres correction

Grande-Bretagne :

- Augustus Keppel
- Peter Parker
- Richard Kempenfelt
- Samuel Barrington
- Francis Geary
- Samuel Hood
- Richard Howe
- Edward Hughes

France :

- Louis Guillouet d'Orvilliers
- Toussaint-Guillaume Picquet de la Motte
- Luc Urbain de Guichen
- Pierre-Andre de Suffren
- Jean-Baptiste d'Albert de Rions
- Charles Hector d'Estaing

Espagne :

- Luis de Cordova y Cordova
- Antonio de Ulloa

## 6. Justification historique courte

- Keppel, Parker, Kempenfelt, Barrington et Geary sont des officiers britanniques plausibles pour les stations metropolitaines de 1776.
- Hood remplace Cochrane en Mediterranee : Hood est adulte et actif dans la Royal Navy en 1776, contrairement a Thomas Cochrane.
- Howe remplace Cockburn pour l'Amerique du Nord : Howe correspond beaucoup mieux au contexte de la guerre d'Amerique.
- Hughes remplace Dundas pour l'East Indies / China Station : Hughes est un choix naval plus coherent pour l'ocean Indien.
- Orvilliers, Picquet de la Motte et Guichen donnent a l'Escadre du Nord des cadres navals francais plausibles.
- Suffren, Rions et d'Estaing remplacent les amiraux generes en Mediterranee. Le choix reste technique et conservateur : il evite les noms generes sans creer de nouvelle mecanique.
- Cordova et Ulloa remplacent les amiraux espagnols generes.

## 7. Flotte -> amiral avant/apres

| Pays | Flotte | Avant | Apres |
|---|---|---|---|
| FRA | Escadre du Nord | 3 amiraux generes, scope `frenchnavy1_gen` ambigu | Orvilliers, Picquet de la Motte, Guichen |
| FRA | Escadre de la Mediterranee | 3 amiraux generes | Suffren, d'Albert de Rions, d'Estaing |
| GBR | Portsmouth Station | Amiraux generes, scope `fleet_gbr2_adm` duplique | Keppel, Parker, Kempenfelt |
| GBR | Plymouth Station | Amiraux generes, un transfert manquant | Barrington, Geary |
| GBR | Mediterranean Station | Thomas Cochrane | Samuel Hood |
| GBR | North America and West Indies Station | George Cockburn | Richard Howe |
| GBR | East Indies and China Station | James Dundas | Edward Hughes |
| SPA | Real Armada Espanola | 2 amiraux generes | Luis de Cordova y Cordova, Antonio de Ulloa |

## 8. Ce qui n'a pas ete modifie

- Aucun `count` de navire.
- Aucun `hq_region`.
- Aucun type de navire.
- Aucun batiment naval.
- Aucune technologie.
- Aucune loi.
- Aucune localisation.
- Aucun pays hors Grande-Bretagne, France et Espagne.
- Aucun fichier de personnages separe : les amiraux concernes etaient definis inline dans `00_military_formations_europe.txt`.

## 9. Tests a faire en jeu

1. Lancer le mod seul.
2. Demarrer une partie en 1776.
3. Verifier les flottes de Grande-Bretagne, France et Espagne.
4. Confirmer que les effectifs NAVY-1A sont inchanges :
   - Grande-Bretagne : 28 ship-of-the-line, 28 frigates.
   - France : 18 ship-of-the-line, 16 frigates.
   - Espagne : 15 ship-of-the-line, 14 frigates.
5. Verifier que les amiraux generes Alan Mair, Neville Graham, Michel Stevenot et Pedro Rodriguez ne remplacent plus les commandants des flottes concernees.
6. Laisser tourner un mois.
7. Surveiller `error.log` et `debug.log` pour `create_character`, `create_military_formation`, `admiral`, `fleet`, `PostValidate`.

## 10. Risques restants

- Les noms composes utilisent des identifiants ASCII sans accents pour eviter d'introduire de nouvelle localisation dans cette phase.
- Certains choix restent approximatifs pour 1776, mais ils sont nettement moins incoherents que les personnages generes ou anachroniques.
- Si le jeu exige plus tard des localisations propres pour certains noms composes, cela devra etre traite dans une phase de localisation, pas dans cette correction gameplay.
