# Phase NAVY-3B - Oman / Golfe / ocean Indien

## 1. Resume

Cette phase corrige uniquement Oman (`OMA`) pour rendre sa flotte existante compatible avec Victoria 3 The Great Wave / 1.13 et maintenable cote equipage.

Corrections appliquees :

- `Bahriat_alMasqat` passe de `region_arabic` a `region_arabia`.
- La flotte omanaise est conservee a 1 vaisseau de ligne + 5 fregates.
- `STATE_OMAN` recoit une administration navale niveau 4.
- Une localisation minimale anglais/francais est ajoutee pour afficher `Bahriat al-Masqat`.
- Aucun amiral, aucune loi navale, aucune technologie et aucun autre pays ne sont modifies.

## 2. Constats NAVY-3A repris

NAVY-3A indiquait pour `OMA` :

- flotte existante : `Bahriat_alMasqat` ;
- composition : 1 `ship_type_ship_of_the_line` + 5 `ship_type_frigate`, soit 6 navires ;
- `hq_region = sr:region_arabic`, invalide en vanilla The Great Wave / 1.13 ;
- infrastructure : 5 ports, 1 chantier naval, 0 administration navale ;
- aucun amiral ;
- aucune loi navale explicite.

## 3. Fichiers modifies

- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/buildings/08_middle_east.txt`
- `localization/english/phase_navy_3b_oman_fleet_l_english.yml`
- `localization/french/phase_navy_3b_oman_fleet_l_french.yml`
- `docs/reports/navy/PHASE_NAVY_3B_OMAN_INDIAN_OCEAN_NAVY.md`

## 4. Correction hq_region

Correction appliquee dans la flotte `Bahriat_alMasqat` :

```txt
hq_region = sr:region_arabic
```

devient :

```txt
hq_region = sr:region_arabia
```

Justification :

- `region_arabia` existe dans la vanilla locale `C:\Games\Victoria 3 The Great Wave\game`.
- C'est le choix terrestre prudent recommande par NAVY-3A.
- Les regions maritimes `region_arabian_sea`, `region_persian_gulf` et `region_western_indian_ocean` existent aussi, mais elles ne sont pas utilisees ici pour eviter de prendre un risque inutile sur le type de region accepte comme HQ de formation.

Les autres `hq_region` invalides du Moyen-Orient, de Perse ou d'Inde ne sont pas modifies dans cette phase.

Note de verification : une occurrence preexistante de `region_arabic` reste dans `common/history/military_formations/04_military_formations_middle_east.txt` hors bloc `c:OMA`. Elle n'a pas ete corrigee ici, car NAVY-3B interdit de modifier les autres pays.

## 5. Decision sur la taille de flotte OMA

La flotte est conservee :

- 1 vaisseau de ligne ;
- 5 fregates ;
- total : 6 navires.

Justification :

- NAVY-3B est une correction technique, pas une recherche historique profonde.
- La flotte existait deja ; la conserver evite un reequilibrage naval plus large.
- Oman est traite comme puissance maritime regionale dans NAVY-3A.
- Une reduction du vaisseau de ligne reste possible plus tard, mais elle devrait venir d'une phase historique dediee Oman / Mascate / Zanzibar.

Aucun navire n'a ete ajoute.

## 6. Calcul de l'administration navale

Regle reprise de NAVY-2D-bis :

```txt
1 niveau de building_naval_administration ~= 1.000 marins
```

Besoin estime pour la flotte conservee :

```txt
1 vaisseau de ligne ~= 0.8K
5 fregates ~= 2.5K
total ~= 3.3K
```

Niveau ajoute :

```txt
building_naval_administration niveau 4
```

Le batiment est ajoute dans `STATE_OMAN`, dans le bloc `region_state:OMA`, car c'est le state principal d'Oman et il contient deja le chantier naval et le port omanais.

Les ports et le chantier naval existants ne sont pas modifies.

## 7. Loi navale

Aucune loi navale n'est modifiee.

Justification :

- aucune raison technique forte ne rend une loi navale obligatoire pour corriger le lancement ou la maintenance ;
- `law_merchant_navy` peut etre logique plus tard, mais devrait etre decidee dans une phase dediee aux lois non europeennes ;
- `law_professional_navy` serait trop fort sans justification historique ;
- `law_jeune_ecole` est hors periode et n'est pas utilisee.

## 8. Amiraux

Aucun amiral n'est ajoute.

Justification :

- NAVY-3A indique qu'une recherche dediee est necessaire pour Oman / Mascate / Zanzibar ;
- cette phase ne doit pas inventer de personnage ;
- les liens Wikipedia eventuels devront attendre une selection d'amiraux historiques fiable.

## 9. Localisation

La cle `Bahriat_alMasqat` n'existait pas dans `localization`.

Deux fichiers dedies sont ajoutes :

- `localization/english/phase_navy_3b_oman_fleet_l_english.yml`
- `localization/french/phase_navy_3b_oman_fleet_l_french.yml`

Cle ajoutee :

```yml
Bahriat_alMasqat: "Bahriat al-Masqat"
```

Les deux fichiers sont encodes en UTF-8 BOM.

## 10. Confirmation qu'aucun autre pays n'a ete modifie

Seuls les blocs `c:OMA` ou `region_state:OMA` ont ete modifies dans les fichiers gameplay.

Aucun autre pays n'a ete modifie.

## 11. Confirmation hors perimetre

Restent hors perimetre et inchanges :

- `CHI` ;
- `DEI` ;
- Inde : `PER`, `MUG`, `MARATH`, `MYS`, `HYD`, `BIC`, `SIN` ;
- Japon / Asie de l'Est : `JAP`, `KOR`, `RYU`, `EZO` ;
- Asie du Sud-Est : `SIA`, `BUR`, `DAI`, `ACE`, `BRU`, `JOH` ;
- pays europeens deja corriges.

## 12. Tests a faire en jeu

1. Lancer une nouvelle partie 1776.
2. Verifier Oman :
   - flotte `Bahriat al-Masqat` visible ;
   - HQ valide ;
   - 1 vaisseau de ligne + 5 fregates ;
   - administration navale niveau 4 en Oman ;
   - capacite d'equipage proche de 4K pour environ 3.3K requis.
3. Verifier qu'aucun amiral n'a ete ajoute.
4. Verifier que `CHI`, `DEI`, l'Inde, le Japon et l'Asie du Sud-Est n'ont pas change.
5. Laisser tourner un mois.
6. Surveiller `error.log` pour :
   - `region_arabic` ;
   - `invalid hq_region` ;
   - `create_military_formation` ;
   - `invalid building` ;
   - `invalid localization` ;
   - `PostValidate`.

## 13. Risques restants

- La flotte omanaise conserve un vaisseau de ligne ; ce choix est minimal techniquement, mais peut etre discutable historiquement.
- L'administration navale niveau 4 ajoute une infrastructure economique visible a Oman.
- Aucun amiral n'est ajoute, donc la flotte peut rester moins personnalisee que les grandes puissances navales.
- Les questions Oman / Mascate / Zanzibar restent ouvertes pour une recherche historique future.
- Une occurrence non-OMA de `region_arabic` reste a auditer separement si elle continue a polluer les logs.

## 14. Liste exacte des fichiers modifies

- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/buildings/08_middle_east.txt`
- `localization/english/phase_navy_3b_oman_fleet_l_english.yml`
- `localization/french/phase_navy_3b_oman_fleet_l_french.yml`
- `docs/reports/navy/PHASE_NAVY_3B_OMAN_INDIAN_OCEAN_NAVY.md`
