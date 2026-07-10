# Phase NAVY-2D-bis - Naval Crew Capacity Fix

## 1. Resume

Cette phase recalibre les niveaux de `building_naval_administration` ajoutes ou requis apres NAVY-2D, en se basant sur le besoin reel d'equipage naval observe en jeu.

Le principe applique est simple : couvrir la flotte actuelle sans creer une grosse marge.

## 2. Probleme observe en jeu

Le test en jeu montre qu'un niveau de `building_naval_administration` fournit environ 1.000 marins / equipage naval.

Exemples observes :

- `TUR` : 4.00K / 8.30K avec administration navale 4.
- `SIC` : 1.00K / 2.80K avec administration navale 1.
- `DEI` : 0 / 1.50K sans administration navale.

Les niveaux NAVY-2D etaient donc techniquement valides, mais insuffisants pour couvrir les flottes existantes.

## 3. Regle utilisee

Regle de calcul :

```txt
niveau minimal d'administration navale = plafond(besoin equipage naval / 1000)
```

Exemples :

- 8.30K -> niveau 9
- 4.10K -> niveau 5
- 2.80K -> niveau 3
- 1.50K -> niveau 2
- 0.50K -> niveau 1

## 4. Table avant / apres

| Pays | Besoin equipage estime | Admin avant NAVY-2D-bis | Admin apres | Statut |
| --- | ---: | ---: | ---: | --- |
| `NET` | 12.10K | 3 | 13 | Couvre la flotte actuelle |
| `POR` | 8.30K | 2 | 9 | Couvre la flotte actuelle |
| `DENNOR` | 8.30K | 2 | 9 | Couvre la flotte actuelle |
| `SWE` | 9.10K | 2 | 10 | Couvre la flotte actuelle |
| `DEI` | 1.50K | 0 | 2 | Couvre la flotte coloniale actuelle |
| `TUR` | 8.30K | 4 | 9 | Couvre la flotte actuelle |
| `VEN` | 4.10K | 2 | 5 | Couvre la flotte actuelle |
| `SIC` | 2.80K | 1 | 3 | Couvre la flotte actuelle |
| `GEN` | 2.30K | 0 | 3 | Couvre la flotte actuelle |
| `SAR` | 1.50K | 0 | 2 | Couvre la flotte actuelle |
| `PAP` | 0.50K | 0 | 1 | Couvre la flotte symbolique |
| `TUS` | 0.50K | 0 | 1 | Couvre la flotte symbolique |
| `TUN` | 0.50K | 0 | 1 | Couvre la flotte littorale |
| `TRI` | 0.50K | 0 | 1 | Couvre la flotte littorale |
| `NOR` | 0.50K | 0 | 0 | Non corrige : setup DENNOR/NOR ambigu |

## 5. Corrections appliquees

`common/history/buildings/00_west_europe.txt` :

- `STATE_HOLLAND` / `NET` : administration navale 3 -> 13.
- `STATE_ZEALAND` / `DENNOR` : administration navale 2 -> 9.
- `STATE_SCANIA` / `SWE` : administration navale 2 -> 10.

`common/history/buildings/01_south_europe.txt` :

- `STATE_ESTREMADURA` / `POR` : administration navale 2 -> 9.
- `STATE_EASTERN_THRACE` / `TUR` : administration navale 4 -> 9.
- `STATE_VENETIA` / `VEN` : administration navale 2 -> 5.
- `STATE_CAMPANIA` / `SIC` : administration navale 1 -> 3.
- `STATE_PIEDMONT` / `GEN` : ajout administration navale niveau 3.
- `STATE_SARDINIA` / `SAR` : ajout administration navale niveau 2.
- `STATE_LAZIO` / `PAP` : ajout administration navale niveau 1.
- `STATE_TUSCANY` / `TUS` : ajout administration navale niveau 1.

`common/history/buildings/03_north_africa.txt` :

- `STATE_TUNISIA` / `TUN` : ajout administration navale niveau 1.
- `STATE_TRIPOLI` / `TRI` : ajout administration navale niveau 1.

`common/history/buildings/12_indonesia.txt` :

- `STATE_WEST_JAVA` / `DEI` : ajout administration navale niveau 2.
- Le chantier naval niveau 1 ajoute par NAVY-2D est conserve.

## 6. Cas non corriges ou ambigus

`NOR` n'a pas ete corrige.

Raison :

- la petite flotte norvegienne existe, mais le setup politique et les blocs de batiments sont surtout portes par `DENNOR` ;
- aucun bloc de batiments clair avec proprietaire `c:NOR` n'a ete identifie dans le perimetre attendu ;
- ajouter une administration separee risquerait de sur-interpreter le setup Danemark-Norvege.

`MOR` / `MAS` restent hors perimetre, car les tags sont encore ambigus.

`OMA`, Inde, Chine, Japon, Coree et Siam ne sont pas traites dans NAVY-2D-bis.

## 7. Confirmation de perimetre

NAVY-2D-bis ne modifie pas :

- flottes ;
- navires ;
- counts ;
- `hq_region` ;
- amiraux ;
- lois ;
- technologies ;
- PM existantes ;
- pops ;
- frontieres ;
- fichiers `common/history/military_formations` ;
- fichiers `common/history/countries` ;
- localisation.

Les modifications portent uniquement sur des niveaux ou ajouts de `building_naval_administration` dans les fichiers `common/history/buildings`, plus ce rapport.

## 8. Fichiers modifies

- `common/history/buildings/00_west_europe.txt`
- `common/history/buildings/01_south_europe.txt`
- `common/history/buildings/03_north_africa.txt`
- `common/history/buildings/12_indonesia.txt`
- `docs/reports/navy/PHASE_NAVY_2D_BIS_NAVAL_CREW_CAPACITY_FIX.md`

Note : `docs/reports/navy/PHASE_NAVY_2D_SECONDARY_NAVAL_LOGISTICS.md` est le rapport de la phase precedente et reste present dans le statut si NAVY-2D n'a pas encore ete commit.

## 9. Tests a refaire en jeu

1. Lancer une nouvelle partie 1776.
2. Verifier les barres d'equipage naval :
   - `NET` : environ 13K disponibles pour 12.10K requis.
   - `POR` : environ 9K disponibles pour 8.30K requis.
   - `DENNOR` : environ 9K disponibles pour 8.30K requis.
   - `SWE` : environ 10K disponibles pour 9.10K requis.
   - `TUR` : environ 9K disponibles pour 8.30K requis.
   - `VEN` : environ 5K disponibles pour 4.10K requis.
   - `SIC` : environ 3K disponibles pour 2.80K requis.
   - `DEI` : environ 2K disponibles pour 1.50K requis.
3. Verifier `GEN`, `SAR`, `PAP`, `TUS`, `TUN`, `TRI`.
4. Verifier que les flottes et amiraux n'ont pas change.
5. Laisser tourner un mois.
6. Surveiller `error.log` pour :
   - `invalid building` ;
   - `invalid production method` ;
   - `building_naval_administration` ;
   - `building_shipyard` ;
   - `PostValidate`.

## 10. Risques restants

- Les niveaux sont calcules pour couvrir l'equipage actuel, pas pour anticiper une expansion navale.
- Les petites flottes symboliques ont maintenant une administration minimale ; cela ameliore la maintenance, mais ajoute une petite infrastructure navale visible.
- `NOR` reste non couvert directement. Si le jeu affiche une penurie pour la flotte norvegienne independamment de `DENNOR`, il faudra une phase dediee au setup Danemark-Norvege / Norvege.
- Les niveaux exacts peuvent varier si le jeu applique des modificateurs d'efficacite, de main-d'oeuvre ou de production sur les administrations navales.
