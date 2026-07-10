# Phase NAVY-3C-1 - Travancore Technical Naval Fix

## 1. Resume

Cette phase corrige uniquement la flotte existante de Travancore (`TRA`) pour la rendre compatible avec Victoria 3 The Great Wave / 1.13.

Corrections appliquees :

- `TravancoreNavy` passe de `region_madras` a `region_south_india`.
- La flotte reste a 1 fregate.
- `STATE_TRAVANCORE` recoit une administration navale niveau 1 dans `region_state:TRA`.
- Une localisation minimale anglais/francais est ajoutee pour le nom de flotte.

Aucun amiral, aucune loi navale, aucune technologie, aucune PM, aucune pop et aucune frontiere ne sont modifies.

## 2. Constats NAVY-3C repris

NAVY-3C avait identifie :

- tag : `TRA` / Travancore ;
- flotte existante : `TravancoreNavy` ;
- composition : 0 vaisseau de ligne + 1 fregate ;
- `hq_region = sr:region_madras`, invalide en vanilla 1.13 ;
- aucun amiral ;
- pas de logistique navale propre detectee ;
- pas de fichier `common/history/countries/tra*.txt` trouve pendant l'audit ;
- `TRA` reste actif mais ambigu.

## 3. Fichiers modifies

- `common/history/military_formations/05_military_formations_india.txt`
- `common/history/buildings/10_india.txt`
- `localization/english/phase_navy_3c_travancore_fleet_l_english.yml`
- `localization/french/phase_navy_3c_travancore_fleet_l_french.yml`
- `docs/reports/navy/PHASE_NAVY_3C_1_TRAVANCORE_TECHNICAL_NAVAL_FIX.md`

## 4. Correction hq_region

Correction appliquee uniquement dans la formation navale `TravancoreNavy` :

```txt
hq_region = sr:region_madras
```

devient :

```txt
hq_region = sr:region_south_india
```

Justification :

- `region_south_india` existe dans la vanilla locale The Great Wave.
- C'est le choix terrestre prudent pour un HQ de flotte.
- `region_laccadive_sea` existe aussi, mais n'est pas utilisee ici pour eviter le risque lie aux HQ maritimes.

Les formations terrestres indiennes restent hors perimetre. `TravancoreArmy` conserve donc son `hq_region` actuel dans cette phase.

## 5. Taille de flotte

La flotte est conservee telle quelle :

- 0 vaisseau de ligne ;
- 1 fregate ;
- total : 1 navire.

Aucun navire n'a ete ajoute ou supprime.

## 6. Logistique navale

Logistique ajoutee :

```txt
building_naval_administration niveau 1
```

Emplacement :

```txt
common/history/buildings/10_india.txt
s:STATE_TRAVANCORE
region_state:TRA
```

Justification :

- `region_state:TRA` existe clairement dans `STATE_TRAVANCORE`.
- Le bloc contient deja une ownership `c:TRA`.
- Une fregate demande environ 0.50K marins.
- La regle NAVY-2D-bis donne environ 1K marins par niveau d'administration navale.
- Niveau 1 suffit donc pour une flotte symbolique d'une fregate.

Aucun chantier naval n'a ete ajoute.

## 7. Localisation

La cle `TravancoreNavy` n'existait pas dans `localization`.

Deux fichiers dedies sont ajoutes :

- `localization/english/phase_navy_3c_travancore_fleet_l_english.yml`
- `localization/french/phase_navy_3c_travancore_fleet_l_french.yml`

Cles ajoutees :

```yml
TravancoreNavy: "Travancore Coastal Flotilla "
TravancoreNavy: " Flottille côtière de Travancore"
```

Les deux fichiers sont encodes en UTF-8 BOM.

## 8. Amiraux

Aucun amiral n'est ajoute.

Raison :

- une recherche historique separee est necessaire ;
- cette phase est technique ;
- aucun commandant naval ne doit etre invente.

## 9. Lois

Aucune loi navale n'est ajoutee.

Raison :

- la flotte est symbolique ;
- les lois navales indiennes doivent etre decidees dans une phase separee ;
- `law_jeune_ecole` et `law_professional_navy` sont hors perimetre.

## 10. Confirmation autres pays indiens

Aucun autre pays indien n'a ete modifie.

Non modifies :

- `BIC`
- `MARATH`
- `MUG`
- `MYS`
- `HYD`
- `SIN`
- `BHV`
- `PUD`
- `COC`
- `PAN`
- `AWA`
- `GWA`
- `NAG`

## 11. hq_region terrestres hors perimetre

Les anciens `hq_region` terrestres indiens restent hors perimetre.

Non corriges volontairement :

- `TravancoreArmy`
- `MysoreArmy`
- `Bengal_Army`
- `OudhRoyalArmy`
- `SindhArmy`
- autres armees indiennes utilisant `region_madras`, `region_bengal`, `region_bombay`, `region_punjab` ou `region_central_india`.

## 12. Tests a faire en jeu

1. Lancer une nouvelle partie 1776.
2. Verifier Travancore :
   - `Travancore Navy` / `Marine de Travancore` visible ;
   - 1 fregate ;
   - HQ valide ;
   - pas d'amiral ;
   - aucune nouvelle loi navale.
3. Verifier l'administration navale :
   - niveau 1 en `STATE_TRAVANCORE` ;
   - environ 1K de capacite pour 0.5K requis.
4. Verifier que `BIC` et `MARATH` n'ont pas change.
5. Laisser tourner un mois.
6. Surveiller `error.log` pour :
   - `region_madras` ;
   - `invalid hq_region` ;
   - `create_military_formation` ;
   - `invalid building` ;
   - `invalid localization` ;
   - `PostValidate`.

## 13. Risques restants

- `TRA` reste un tag ambigu, sans fichier history country trouve pendant l'audit.
- `TravancoreArmy` conserve son ancien `region_madras`, car cette phase ne corrige pas les formations terrestres.
- L'administration navale niveau 1 ajoute une petite infrastructure economique visible a Travancore.
- Une phase future devra decider si `TRA` doit recevoir un fichier pays plus complet ou rester comme tag partiel.

## 14. Liste exacte des fichiers modifies

- `common/history/military_formations/05_military_formations_india.txt`
- `common/history/buildings/10_india.txt`
- `localization/english/phase_navy_3c_travancore_fleet_l_english.yml`
- `localization/french/phase_navy_3c_travancore_fleet_l_french.yml`
- `docs/reports/navy/PHASE_NAVY_3C_1_TRAVANCORE_TECHNICAL_NAVAL_FIX.md`
