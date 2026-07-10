# Phase NAVY-2D - Secondary Naval Logistics

## 1. Resume

Cette phase corrige uniquement la logistique navale terrestre des marines secondaires et regionales deja traitees en NAVY-2B et NAVY-2C.

Objectif applique :

- ajouter une administration navale limitee aux puissances secondaires fortes ;
- ajouter une logistique minimale a Venise et aux Deux-Siciles ;
- ajouter un chantier colonial minimal a `DEI` / VOC ;
- ne pas modifier les flottes, amiraux, lois, technologies, PM, pops ou frontieres.

Reference vanilla utilisee :

`C:\Games\Victoria 3 The Great Wave\game`

IDs vanilla utilises :

- `building_shipyard`
- `building_naval_administration`
- `pm_basic_shipbuilding`
- `pm_simple_sailor_recruitment`

## 2. Fichiers modifies

- `common/history/buildings/00_west_europe.txt`
- `common/history/buildings/01_south_europe.txt`
- `common/history/buildings/12_indonesia.txt`
- `docs/reports/navy/PHASE_NAVY_2D_SECONDARY_NAVAL_LOGISTICS.md`

## 3. Audit ports / chantiers / administrations

Audit apres correction :

| Pays | Flotte actuelle | Ports | Chantiers navals | Administration navale | Statut logistique |
| --- | ---: | ---: | ---: | ---: | --- |
| `NET` | 20 | 12 | 4 | 3 | OK, administration secondaire forte ajoutee |
| `POR` | 13 | 16 | 6 | 2 | OK, administration limitee ajoutee |
| `DENNOR` | 13 | 11 | 4 | 2 | OK, administration limitee ajoutee |
| `NOR` | 1 | 0 | 0 | 0 | Flotte symbolique, ne pas renforcer separement |
| `SWE` | 14 | 5 | 2 | 2 | OK, administration limitee ajoutee |
| `DEI` | 3 | 6 | 1 | 0 | OK, chantier colonial minimal ajoute |
| `TUR` | 13 | 20 | 7 | 4 | OK, administration regionale forte ajoutee |
| `VEN` | 7 | 11 | 2 | 2 | OK, Arsenal represente par administration limitee |
| `SIC` | 5 | 4 | 1 | 1 | OK, chantier et administration minimale ajoutes |
| `GEN` | 4 | 3 | 2 | 0 | OK, pas d'administration forcee |
| `SAR` | 3 | 2 | 3 | 0 | OK, pas d'administration forcee |
| `PAP` | 1 | 1 | 0 | 0 | Flotte symbolique, ne pas renforcer |
| `TUS` | 1 | 2 | 0 | 0 | Flotte symbolique, ne pas renforcer |
| `TUN` | 1 | 1 | 0 | 0 | Flotte corsaire/littorale, ne pas renforcer |
| `TRI` | 1 | 1 | 0 | 0 | Flotte corsaire/littorale, ne pas renforcer |

## 4. Incoherences trouvees

Incoherences principales :

- `NET`, `POR`, `DENNOR`, `SWE` et `TUR` avaient des flottes secondaires fortes mais 0 `building_naval_administration`.
- `VEN` avait une flotte regionale notable et des chantiers, mais aucune administration navale.
- `SIC` avait une flotte reelle mais 0 chantier naval et 0 administration navale.
- `DEI` avait 3 fregates apres NAVY-2B-bis, plusieurs ports coloniaux, mais 0 chantier naval.

Cas juges acceptables sans correction :

- `GEN` et `SAR` ont deja des chantiers pour leurs petites flottes.
- `PAP`, `TUS`, `TUN`, `TRI` sont des flottes symboliques ou littorales.
- `NOR` reste lie au setup `DENNOR` et ne recoit pas de logistique separee.

## 5. Corrections appliquees

`common/history/buildings/00_west_europe.txt` :

- `STATE_HOLLAND` / `NET` : ajout de `building_naval_administration`, niveau 3.
- `STATE_ZEALAND` / `DENNOR` : ajout de `building_naval_administration`, niveau 2.
- `STATE_SCANIA` / `SWE` : ajout de `building_naval_administration`, niveau 2.

`common/history/buildings/01_south_europe.txt` :

- `STATE_ESTREMADURA` / `POR` : ajout de `building_naval_administration`, niveau 2.
- `STATE_EASTERN_THRACE` / `TUR` : ajout de `building_naval_administration`, niveau 4.
- `STATE_VENETIA` / `VEN` : ajout de `building_naval_administration`, niveau 2.
- `STATE_CAMPANIA` / `SIC` : ajout de `building_shipyard`, niveau 1.
- `STATE_CAMPANIA` / `SIC` : ajout de `building_naval_administration`, niveau 1.

`common/history/buildings/12_indonesia.txt` :

- `STATE_WEST_JAVA` / `DEI` : ajout de `building_shipyard`, niveau 1.

## 6. Cas volontairement non corriges

Non renforces :

- `NOR` : flotte symbolique et setup politique lie a `DENNOR`.
- `GEN` : deja 2 chantiers pour une flotte de 4 navires.
- `SAR` : deja 3 chantiers pour une flotte de 3 fregates.
- `PAP` : flotte symbolique.
- `TUS` : flotte symbolique.
- `TUN` : flotte littorale/corsaire.
- `TRI` : flotte littorale/corsaire.
- `MOR` / `MAS` : tags encore ambigus, hors correction.
- `OMA` : hors perimetre, reserve a NAVY-3.

Aucun chantier n'a ete ajoute partout de facon mecanique.

## 7. Focus DEI / VOC

`DEI` dispose maintenant de 3 fregates, mais avait :

- 6 ports ;
- 0 chantier naval ;
- 0 administration navale.

Correction appliquee :

- ajout d'un seul `building_shipyard` niveau 1 en `STATE_WEST_JAVA`.

Justification :

- Java occidental est le centre colonial logique du tag `DEI`.
- Le chantier permet une capacite minimale de maintenance/construction sans transformer `DEI` en grande puissance navale.
- Aucune administration navale n'a ete ajoutee a `DEI`, pour rester dans la limite 0 ou 1 maximum et eviter de surmodeler une flotte coloniale de 3 fregates.

## 8. Confirmation de perimetre technique

NAVY-2D ne modifie pas :

- navires ;
- counts de flotte ;
- `hq_region` ;
- amiraux ;
- lois ;
- technologies ;
- production methods existantes hors activation standard des nouveaux batiments ;
- pops ;
- frontieres ;
- pays ;
- localisation ;
- fichiers `common/history/military_formations`;
- fichiers `common/history/countries`.

## 9. Confirmation hors perimetre

Non modifies :

- grandes puissances : `GBR`, `FRA`, `SPA`, `RUS` ;
- `MOR` / `MAS` ;
- `OMA` ;
- Inde ;
- Chine ;
- Japon ;
- Coree ;
- Siam ;
- toute phase NAVY-3 future.

## 10. Tests a faire en jeu

1. Lancer une nouvelle partie 1776.
2. Verifier `DEI` :
   - `Koloniale_Marine` toujours a 3 fregates ;
   - presence d'un chantier naval en Java occidental ;
   - pas de navire capital ;
   - pas d'amiral.
3. Verifier `NET`, `POR`, `DENNOR`, `SWE` :
   - flottes inchangees ;
   - administration navale presente aux niveaux indiques.
4. Verifier `TUR`, `VEN`, `SIC` :
   - flottes inchangees ;
   - logistique navale coherente ;
   - chantier minimal visible pour `SIC`.
5. Verifier `GEN`, `SAR`, `PAP`, `TUS`, `TUN`, `TRI` :
   - pas de sur-renforcement.
6. Laisser tourner un mois.
7. Surveiller `error.log` pour :
   - `invalid building` ;
   - `invalid production method` ;
   - `building_shipyard` ;
   - `building_naval_administration` ;
   - `PostValidate`.

## 11. Risques restants

- Les niveaux d'administration navale sont conservateurs mais peuvent modifier legerement le cout et l'emploi naval des pays secondaires.
- `DEI` reste sans administration navale ; si le jeu penalise trop la flotte coloniale, une administration niveau 1 pourra etre envisagee plus tard.
- `SIC` recoit seulement un chantier niveau 1 ; c'est suffisant pour une correction technique mais pas une representation complete de l'arsenal napolitain.
- `GEN`, `SAR`, `PAP`, `TUS`, `TUN` et `TRI` restent volontairement peu structures.

## 12. Liste exacte des fichiers modifies

- `common/history/buildings/00_west_europe.txt`
- `common/history/buildings/01_south_europe.txt`
- `common/history/buildings/12_indonesia.txt`
- `docs/reports/navy/PHASE_NAVY_2D_SECONDARY_NAVAL_LOGISTICS.md`
