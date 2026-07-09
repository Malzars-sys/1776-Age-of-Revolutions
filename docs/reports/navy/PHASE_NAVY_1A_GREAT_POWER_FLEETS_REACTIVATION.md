# Phase NAVY-1A - Reactivation des flottes GB/FRA/SPA

## 1. Resume

Cette phase reactive uniquement les flottes initiales des trois grandes puissances navales ciblees :

- Grande-Bretagne : `c:GBR`
- France : `c:FRA`
- Espagne : `c:SPA`

La correction porte sur deux points strictement limites aux flottes :

- remplacement des `hq_region` obsoletes par des strategic regions vanilla The Great Wave / 1.13 valides ;
- reduction conservative des counts, car les valeurs existantes etaient tres au-dessus de la grille NAVY-0.

Aucun batiment, aucune loi navale, aucune technologie, aucun design de navire, aucun type custom et aucune localisation n'ont ete modifies.

## 2. Fichiers modifies

Gameplay :

- `common/history/military_formations/00_military_formations_europe.txt`

Rapport :

- `PHASE_NAVY_1A_GREAT_POWER_FLEETS_REACTIVATION.md`

## 3. Tags utilises

| Pays | Tag utilise | Verification |
|---|---|---|
| Grande-Bretagne | `GBR` | `common/country_definitions/00_countries.txt`, `common/history/countries/gbr - great britain.txt`, bloc `c:GBR` dans `00_military_formations_europe.txt` |
| France | `FRA` | `common/country_definitions/00_countries.txt`, `common/history/countries/fra - france.txt`, bloc `c:FRA` |
| Espagne | `SPA` | `common/country_definitions/00_countries.txt`, `common/history/countries/spa - spain.txt`, bloc `c:SPA` |

Le tag `IREK` existe aussi dans le mod, mais il n'est pas le bloc britannique des formations navales. Il n'a pas ete modifie.

## 4. Anciennes hq_region invalides trouvees

Dans les flottes ciblees :

- `region_france`
- `region_occitania`
- `region_england`
- `region_italy`
- `region_new_england`
- `region_madras`
- `region_iberia`

Ces regions sont absentes ou commentees dans les fichiers vanilla 1.13.

## 5. Nouvelles hq_region vanilla valides utilisees

Regions confirmees dans `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions` :

- `region_western_europe`
- `region_southern_europe`
- `region_atlantic_coast`
- `region_indochina`

## 6. Table ancienne region -> nouvelle region

| Ancienne region | Nouvelle region | Justification |
|---|---|---|
| `region_france` | `region_western_europe` | France atlantique / Manche / Brest-Rochefort-Normandie |
| `region_occitania` | `region_southern_europe` | Provence, Languedoc, Aquitaine sud et Mediterranee francaise |
| `region_england` | `region_western_europe` | Grande-Bretagne metropolitaine |
| `region_italy` | `region_southern_europe` | Mediterranee / Malta / Gibraltar selon regroupement 1.13 |
| `region_new_england` | `region_atlantic_coast` | Station nord-americaine, Bermuda et cote atlantique |
| `region_madras` | `region_indochina` | Choix aligne sur l'exemple vanilla de `East_Indies_and_China_Station` |
| `region_iberia` | `region_southern_europe` | Iberie incluse dans `region_southern_europe` en vanilla 1.13 |

`region_caribbean` etait mentionnee dans NAVY-0, mais aucune flotte GB/FRA/SPA ciblee ici ne l'utilisait directement.

## 7. Flottes britanniques avant/apres

| Flotte | Avant region | Avant ligne | Avant fregates | Apres region | Apres ligne | Apres fregates |
|---|---:|---:|---:|---|---:|---:|
| `Portsmouth_Station` | `region_england` | 48 | 49 | `region_western_europe` | 10 | 9 |
| `Plymouth_Station` | `region_england` | 19 | 25 | `region_western_europe` | 6 | 6 |
| `Mediterranean_Station` | `region_italy` | 11 | 11 | `region_southern_europe` | 5 | 4 |
| `North_America_and_West_Indies_Station` | `region_new_england` | 1 | 12 | `region_atlantic_coast` | 4 | 5 |
| `East_Indies_and_China_Station` | `region_madras` | 2 | 7 | `region_indochina` | 3 | 4 |

Total britannique apres correction :

- navires de ligne : 28
- fregates : 28

## 8. Flottes francaises avant/apres

| Flotte | Avant region | Avant ligne | Avant fregates | Apres region | Apres ligne | Apres fregates |
|---|---:|---:|---:|---|---:|---:|
| `Escadre_du_Nord` | `region_france` | 20 | 40 | `region_western_europe` | 11 | 10 |
| `Escadre_de_la_Mditerrane` | `region_occitania` | 16 | 24 | `region_southern_europe` | 7 | 6 |

Total francais apres correction :

- navires de ligne : 18
- fregates : 16

## 9. Flottes espagnoles avant/apres

| Flotte | Avant region | Avant ligne | Avant fregates | Apres region | Apres ligne | Apres fregates |
|---|---:|---:|---:|---|---:|---:|
| `Real_Armada_Espaola` | `region_iberia` | 15 | 40 | `region_southern_europe` | 15 | 14 |

Total espagnol apres correction :

- navires de ligne : 15
- fregates : 14

## 10. Total par pays apres correction

| Pays | Navires de ligne | Fregates | Role voulu |
|---|---:|---:|---|
| Grande-Bretagne | 28 | 28 | Premiere puissance navale, presence multi-theatre |
| France | 18 | 16 | Deuxieme puissance, forte mais encore en montee |
| Espagne | 15 | 14 | Troisieme grande puissance, masse imperiale mais moins flexible |

## 11. Justification de l'echelle

NAVY-0 recommandait :

- 1 unite de jeu de navire de ligne = environ 3 a 4 vaisseaux de ligne historiques ;
- 1 unite de jeu de fregate = environ 4 a 6 fregates, sloops ou batiments legers historiques.

Les anciens counts du mod etaient probablement des chiffres proches d'un inventaire historique brut ou semi-brut, trop eleves pour un prototype jouable :

- Grande-Bretagne : 81 navires de ligne / 104 fregates ;
- France : 36 navires de ligne / 64 fregates ;
- Espagne : 15 navires de ligne / 40 fregates.

La nouvelle grille conserve la hierarchie :

1. Grande-Bretagne nettement premiere.
2. France deuxieme.
3. Espagne troisieme, avec une flotte lourde encore importante.

## 12. Ce qui n'a pas ete modifie

Non modifies volontairement :

- Russie ;
- Pays-Bas ;
- Portugal ;
- Danemark-Norvege ;
- Suede ;
- Empire ottoman ;
- puissances non europeennes ;
- Japon / Tenpo / Sakoku ;
- Australie / Nouvelle-Zelande ;
- Moyen-Orient ;
- lois navales ;
- technologies ;
- batiments navals ;
- designs ou composants de navires ;
- localisation ;
- types custom comme galeres, jonques, xebecs.

Les anciens `hq_region` d'armees GB/FRA/SPA et les autres pays restent hors perimetre de cette phase.

## 13. Tests a faire en jeu

1. Lancer le mod seul.
2. Demarrer ou observer au 1 janvier 1776.
3. Verifier Grande-Bretagne :
   - elle possede des navires ;
   - elle est premiere puissance navale ;
   - les stations Home / Mediterranee / Amerique / East Indies apparaissent.
4. Verifier France :
   - elle possede des navires ;
   - elle est deuxieme ou proche deuxieme ;
   - les deux escadres apparaissent.
5. Verifier Espagne :
   - elle possede des navires ;
   - elle reste une grande puissance navale.
6. Verifier Russie :
   - elle n'a pas ete modifiee ;
   - ses flottes visibles precedemment ne disparaissent pas.
7. Laisser tourner un mois.
8. Controler `error.log` et `debug.log` pour :
   - `create_military_formation`
   - `hq_region`
   - `strategic region`
   - `ship_type`
   - `fleet`
   - `PostValidate`

## 14. Risques restants

- Les commandants francais de `Escadre_du_Nord` utilisent encore un `save_scope_as = frenchnavy1_gen` partage entre formation et admiral. Je ne l'ai pas corrige pour rester dans le perimetre NAVY-1A ; si les navires apparaissent mais que les commandants ne sont pas affectes correctement, ce sera une correction NAVY-1A-bis ou NAVY-1D.
- Des `hq_region` invalides restent dans les armees et dans les flottes d'autres pays. Ils sont hors perimetre de cette phase.
- La logistique navale n'est pas traitee : sailors, naval administrations, shipyards, ports et supply ships devront etre verifies en NAVY-1B.
- Les flottes coloniales britanniques utilisent encore des `state_region` metropolitains pour certains navires ; cela respecte l'etat existant du mod mais reste a auditer plus tard.
- L'equilibrage final 1776 n'est pas fait. Cette phase donne un prototype jouable, pas un inventaire naval definitif.
