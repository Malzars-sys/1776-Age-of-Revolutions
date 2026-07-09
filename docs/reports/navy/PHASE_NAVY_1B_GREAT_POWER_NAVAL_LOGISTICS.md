# Phase NAVY-1B - Logistique navale GBR / FRA / SPA

## 1. Resume des corrections

Cette phase corrige uniquement la logistique navale terrestre des trois grandes marines ciblees : Grande-Bretagne, France et Espagne.

Les flottes, les types de navires, les amiraux, les `hq_region` et les effectifs navals n'ont pas ete modifies.

Correction appliquee :
- ajout de `building_naval_administration` dans les grands centres navals existants ;
- ajout ou renforcement limite de `building_shipyard` pour quelques arsenaux evidents ;
- conservation des ports existants ;
- aucun retour a `building_military_shipyard`, `building_naval_base` ou aux anciennes PM `pm_military_shipbuilding_*`.

## 2. Fichiers modifies

- `common/history/buildings/00_west_europe.txt`
- `common/history/buildings/01_south_europe.txt`
- `common/history/buildings/06_central_america.txt`
- `PHASE_NAVY_1B_GREAT_POWER_NAVAL_LOGISTICS.md`

## 3. IDs vanilla The Great Wave utilises

Verification faite dans `C:\Games\Victoria 3 The Great Wave\game`.

IDs retenus :
- `building_port`
- `building_shipyard`
- `building_naval_administration`
- `pm_basic_port`
- `pm_basic_shipbuilding`
- `pm_simple_sailor_recruitment`

IDs volontairement non utilises :
- `building_military_shipyard` : obsolète / non compatible avec le setup 1.13 du mod.
- `building_naval_base` : ancien modele remplace par les formations et la logistique 1.13.
- `pm_military_shipbuilding_wooden`, `pm_military_shipbuilding_wooden_2` : anciennes PM navales.
- `building_naval_logistics_center` : existe en vanilla, mais `buildable = no` et `expandable = no`; non ajoute dans l'historique.

## 4. Audit avant correction

Avant correction, les pays disposaient deja de ports et de chantiers navals civils, mais presque pas de structure logistique navale 1.13 :

| Pays | Ports | Chantiers navals | Administration navale |
| --- | ---: | ---: | ---: |
| GBR | existants | 18 | 0 |
| FRA | existants | 9 | 0 |
| SPA | existants | 6 | 0 |

Le probleme principal etait donc moins l'absence de ports que l'absence de `building_naval_administration`, necessaire pour representer les personnels et l'administration navale dans The Great Wave.

## 5. Corrections appliquees

Grande-Bretagne :
- `STATE_HOME_COUNTIES` : ajout de `building_naval_administration`, niveau 20.
- `STATE_WEST_COUNTRY` : ajout de `building_naval_administration`, niveau 10.
- `STATE_UPPER_ANDALUSIA` / Gibraltar : ajout de `building_naval_administration`, niveau 3.

France :
- `STATE_BRITTANY` : ajout de `building_naval_administration`, niveau 12.
- `STATE_PROVENCE` : ajout de `building_shipyard`, niveau 3, et `building_naval_administration`, niveau 8.
- `STATE_POITOU` : ajout de `building_shipyard`, niveau 2, et `building_naval_administration`, niveau 4.

Espagne :
- `STATE_GALICIA` : chantier naval 1 -> 2, ajout de `building_naval_administration`, niveau 8.
- `STATE_LOWER_ANDALUSIA` : chantier naval 1 -> 2, ajout de `building_naval_administration`, niveau 8.
- `STATE_MURCIA` : chantier naval 1 -> 2, ajout de `building_naval_administration`, niveau 5.
- `STATE_WEST_INDIES` / bloc espagnol existant : ajout de `building_naval_administration`, niveau 3, comme point logistique colonial minimal pour les Caraibes espagnoles.

## 6. Tableau avant / apres

Avant correction :

| Pays | Ports | Chantiers navals | Administrations navales | Fortifications navales |
| --- | ---: | ---: | ---: | ---: |
| GBR | existants, non modifies | 18 | 0 | 0 |
| FRA | existants, non modifies | 9 | 0 | 0 |
| SPA | existants, non modifies | 6 | 0 | 0 |

Apres correction :

| Pays | Ports | Chantiers navals | Administrations navales | Fortifications navales |
| --- | ---: | ---: | ---: | ---: |
| GBR | inchanges | 18 | 33 | 0 |
| FRA | inchanges | 14 | 24 | 0 |
| SPA | inchanges | 9 | 24 | 0 |

Les ports et les fortifications navales n'ont pas ete modifies.

## 7. Justification historique et gameplay

La correction reste technique et conservatrice :
- la Grande-Bretagne recoit une capacite administrative concentree autour de Londres, du West Country et de Gibraltar ;
- la France recupere des arsenaux/logistiques coherents avec Brest, Toulon et Rochefort ;
- l'Espagne est renforcee autour de Ferrol, Cadix/La Carraca, Carthagene et un petit relais antillais ;
- aucun pays secondaire n'est modifie ;
- aucune colonie, flotte ou formation navale n'est creee.

Le but est de rendre les grandes puissances navales jouables sous The Great Wave sans refaire l'equilibrage naval mondial 1776.

## 8. Volontairement non modifie

Non modifies :
- navires et types de navires ;
- nombres de flottes ;
- `hq_region` ;
- `ship_type` ;
- amiraux et roles de commandants ;
- Russie ;
- Pays-Bas, Portugal, Danemark-Norvege, Suede, Ottomans, Japon ;
- Australie, Moyen-Orient, technologies, lois, localisation ;
- `building_naval_fortification`, garde pour une phase separee si necessaire.

## 9. Risques restants

- Les niveaux de `building_naval_administration` sont conservateurs mais devront etre testes en jeu avec les flottes de 1776.
- Les Caraibes espagnoles restent representees par le bloc existant `STATE_WEST_INDIES`; aucune refonte de Cuba/Havane n'a ete faite.
- Si The Great Wave utilise des contraintes supplementaires pour les formations navales, les logs peuvent encore signaler des problemes hors batiments.

## 10. Tests a faire

Tester en priorite :
- lancer une partie avec GBR, FRA et SPA ;
- verifier que le jeu passe le premier jour puis un mois sans erreurs PostValidate sur les batiments navals ;
- verifier `error.log` pour `building_military_shipyard`, `building_naval_base`, `pm_military_shipbuilding`;
- ouvrir les ecrans de construction et d'armee/navy pour GBR/FRA/SPA ;
- comparer les couts et besoins en main-d'oeuvre navale apres quelques semaines de simulation.
