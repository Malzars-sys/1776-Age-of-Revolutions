# Phase NAVY-2C - Mediterranean Regional Navies

## 1. Resume

Cette phase corrige uniquement les marines regionales mediterraneennes ciblees par NAVY-2C. Les corrections portent sur les `hq_region` invalides des flottes, un reequilibrage prudent des effectifs, quelques noms de flottes manifestement mauvais, deux amiraux historiques solides, et des lois navales de depart quand le prerequis etait confirme.

La reference vanilla utilisee est :

`C:\Games\Victoria 3 The Great Wave\game`

Regions vanilla confirmees :

- `region_southern_europe`
- `region_north_africa`
- `region_near_east`

## 2. Fichiers modifies

- `common/history/military_formations/00_military_formations_europe.txt`
- `common/history/military_formations/03_military_formations_north_africa.txt`
- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/countries/tur - ottoman empire.txt`
- `common/history/countries/ven - venetia.txt`
- `common/history/countries/sic - two sicilies.txt`
- `common/history/countries/gen - genoa.txt`
- `common/history/countries/sar - sardinia.txt`
- `localization/english/phase_navy_2c_admirals_l_english.yml`
- `localization/french/phase_navy_2c_admirals_l_french.yml`
- `docs/reports/navy/PHASE_NAVY_2C_MEDITERRANEAN_REGIONAL_NAVIES.md`

## 3. Tags et pays reellement traites

| Pays historique | Tag | Fichier pays trouve | Flotte trouvee | Action NAVY-2C |
| --- | --- | --- | --- | --- |
| Empire ottoman | `TUR` | Oui | Oui | HQ corrige, flotte reduite, nom corrige, amiral ajoute, loi navale ajoutee |
| Venise | `VEN` | Oui | Oui | HQ corrige, flotte reduite, nom corrige, amiral ajoute, loi navale ajoutee |
| Deux-Siciles | `SIC` | Oui | Oui | HQ corrige, flotte reduite, nom simplifie, loi navale ajoutee |
| Genes | `GEN` | Oui | Oui | HQ corrige, flotte reduite, nom corrige, loi navale ajoutee |
| Sardaigne-Piemont | `SAR` | Oui | Oui | HQ corrige, flotte reduite, loi navale ajoutee |
| Etats pontificaux | `PAP` | Oui | Oui | HQ corrige seulement |
| Toscane | `TUS` | Oui | Oui | HQ corrige seulement |
| Tunis | `TUN` | Oui | Oui | Conserve tel quel, deja valide |
| Tripoli | `TRI` | Oui | Non | Petite flotte d'une fregate ajoutee |

## 4. Tags ambigus non traites

- `MOR` : utilise dans les states/buildings/diplomacy, mais a clarifier avant toute creation de flotte.
- `MAS` : utilise dans les states/buildings/diplomacy et dans un bloc militaire terrestre, mais son statut exact reste ambigu.

Aucune flotte n'a ete creee pour `MOR` ou `MAS`.

## 5. Corrections de hq_region

- `TUR` : `sr:region_anatolia` -> `sr:region_near_east`
- `VEN` : `sr:region_italy` -> `sr:region_southern_europe`
- `SIC` : `sr:region_italy` -> `sr:region_southern_europe`
- `GEN` : `sr:region_italy` -> `sr:region_southern_europe`
- `SAR` : `sr:region_italy` -> `sr:region_southern_europe`
- `PAP` : `sr:region_italy` -> `sr:region_southern_europe`
- `TUS` : `sr:region_italy` -> `sr:region_southern_europe`
- `TUN` : `sr:region_north_africa` conserve
- `TRI` : nouvelle flotte avec `sr:region_north_africa`

Des `region_italy` et `region_anatolia` restent visibles dans des armees ou dans des interets historiques hors perimetre NAVY-2C. Ils n'ont pas ete corriges automatiquement.

## 6. Reequilibrage des flottes

| Tag | Avant | Apres | Remarque |
| --- | --- | --- | --- |
| `TUR` | 8 vaisseaux de ligne + 7 fregates | 6 vaisseaux de ligne + 7 fregates | Puissance regionale forte, sans niveau Espagne/France |
| `VEN` | 1 vaisseau de ligne + 19 fregates | 2 vaisseaux de ligne + 5 fregates | Arsenal prestigieux mais flotte regionale |
| `SIC` | 2 vaisseaux de ligne + 6 fregates | 1 vaisseau de ligne + 4 fregates | Correction prudente |
| `GEN` | 1 vaisseau de ligne + 7 fregates | 1 vaisseau de ligne + 3 fregates | Conservation du bloc existant sans supprimer le vaisseau de ligne |
| `SAR` | 5 fregates | 3 fregates | Taille regionale |
| `PAP` | 1 fregate | 1 fregate | Symbolique conserve |
| `TUS` | 1 fregate | 1 fregate | Symbolique conserve |
| `TUN` | 1 fregate | 1 fregate | Deja valide |
| `TRI` | Aucune flotte | 1 fregate | Ajout minimal car tag actif et fichier pays present |

## 7. Noms de flottes conserves ou modifies

Modifies :

- `TUR` : `Donanmay_Humyn` -> `Donanma_yi_Humayun`
- `VEN` : `merchant_venice_fleet` -> `Armata_Grossa`
- `SIC` : `Armata_di_Mare_di_SM_il_Re_del_Regno_delle_Due_Sicilie` -> `Real_Marina_Napoletana`
- `GEN` : `merchant_venice_fleet` -> `Marina_Genovese`
- `TRI` : nouvelle flotte `Escadre_de_Tripoli`

Conserves :

- `SAR` : `Marina_del_Regno_di_Sardegna`
- `PAP` : `Marina_Pontificia`
- `TUS` : `Marina_del_Granducato_di_Toscana`
- `TUN` : `Bahriat_alTuwnusia`

## 8. Amiraux ajoutes ou non ajoutes

Ajoutes :

- `TUR` : Cezayirli Gazi Hasan Pasha, amiral historique, attache a `Donanma_yi_Humayun`.
- `VEN` : Angelo Emo, amiral historique, attache a `Armata_Grossa`.

Non ajoutes volontairement :

- `SIC` : John Acton n'a pas ete ajoute dans cette phase car le role exact en 1776 merite une verification dediee. Francesco Caracciolo n'a pas ete utilise comme grand amiral principal, son rang/age etant trop fragile pour cette phase.
- `GEN`, `SAR`, `PAP`, `TUS` : pas de candidat suffisamment solide sans recherche dediee.
- `TUN`, `TRI`, `MOR`, `MAS` : pas d'amiral ajoute pour eviter les noms anachroniques ou incertains.

Les fichiers de localisation EN/FR crees pour les amiraux sont en UTF-8 BOM.

## 9. Lois navales ajoutees ou non ajoutees

Ajoutees :

- `TUR` : `law_professional_navy`
- `VEN` : `law_merchant_navy`
- `SIC` : `law_merchant_navy`
- `GEN` : `law_merchant_navy`
- `SAR` : `law_merchant_navy`

Justification :

- `law_professional_navy` demande `military_drill`, confirme dans la vanilla 1.13.
- Les pays concernes ont un effet de depart technologique de niveau 4 qui inclut `military_drill`.
- `law_merchant_navy` est visible pour les pays cotiers et ne demande pas `military_drill`.

Non ajoutees :

- `PAP`, `TUS` : flottes symboliques, pas de loi forcee.
- `TUN`, `TRI`, `MOR`, `MAS` : pas de loi oceanique ou professionnelle forcee.
- `law_jeune_ecole` : jamais utilisee.

## 10. Confirmation des pays interdits

Les pays suivants n'ont pas ete modifies dans cette phase :

- `GBR`
- `FRA`
- `SPA`
- `RUS`
- `NET`
- `POR`
- `DENNOR`
- `NOR`
- `SWE`
- `DEI`

Les apparitions de lois navales existantes pour certains de ces pays dans les recherches viennent des phases precedentes ou du contenu deja present, pas de NAVY-2C.

## 11. Confirmation OMA et non-Europeens

`OMA` n'a pas ete modifie.

Aucune marine d'Inde, de Chine, du Japon, de Coree, du Siam ou d'une puissance non mediterraneenne n'a ete modifiee.

## 12. Tests a faire en jeu

1. Lancer une nouvelle partie 1776 avec uniquement le mod.
2. Verifier `TUR` :
   - flotte visible ;
   - HQ valide ;
   - 6 vaisseaux de ligne + 7 fregates ;
   - Cezayirli Gazi Hasan Pasha visible et attache.
3. Verifier `VEN` :
   - `Armata_Grossa` visible ;
   - 2 vaisseaux de ligne + 5 fregates ;
   - Angelo Emo visible et attache.
4. Verifier `SIC`, `GEN`, `SAR`, `PAP`, `TUS`.
5. Verifier `TUN` et `TRI`.
6. Laisser tourner au moins un mois.
7. Surveiller `error.log` pour :
   - `invalid hq_region` ;
   - `create_military_formation` ;
   - `invalid character` ;
   - `invalid law` ;
   - `missing localization` ;
   - `PostValidate`.

## 13. Risques restants

- Les lois navales peuvent modifier legerement le comportement interne des pays, mais elles restent limitees au modele naval.
- `TRI` recoit une flotte minimale ; si le tag a un statut politique inattendu en jeu, il faudra retirer ou ajuster cette flotte.
- `MOR` et `MAS` restent a clarifier avant toute correction navale nord-africaine.
- Les noms directs de flotte restent des identifiants simples sans accents, conformes au style deja utilise dans le mod.
- Les vieux `region_italy` / `region_anatolia` restants dans des armees ou interets n'ont pas ete touches, car la phase cible les flottes.

## 14. Liste exacte des fichiers modifies

- `common/history/military_formations/00_military_formations_europe.txt`
- `common/history/military_formations/03_military_formations_north_africa.txt`
- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/countries/tur - ottoman empire.txt`
- `common/history/countries/ven - venetia.txt`
- `common/history/countries/sic - two sicilies.txt`
- `common/history/countries/gen - genoa.txt`
- `common/history/countries/sar - sardinia.txt`
- `localization/english/phase_navy_2c_admirals_l_english.yml`
- `localization/french/phase_navy_2c_admirals_l_french.yml`
- `docs/reports/navy/PHASE_NAVY_2C_MEDITERRANEAN_REGIONAL_NAVIES.md`
