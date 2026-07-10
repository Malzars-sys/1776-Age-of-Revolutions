# Phase NAVY-2C-bis - Fleet Name Localization Fix

## 1. Resume

Cette phase corrige uniquement l'affichage des noms de flottes crees ou renommes pendant NAVY-2C. Aucun fichier gameplay n'a ete modifie dans NAVY-2C-bis.

## 2. Probleme observe en jeu

Apres test de NAVY-2C, plusieurs flottes mediterraneennes fonctionnaient correctement mais affichaient leur identifiant brut avec underscores au lieu d'un nom lisible.

Les amiraux principaux ajoutes en NAVY-2C fonctionnaient :

- `TUR` : Cezayirli Gazi Hasan Pasha
- `VEN` : Angelo Emo

L'absence d'amiral pour `SIC`, `GEN`, `SAR`, `PAP`, `TUS`, `TUN` et `TRI` reste volontaire.

## 3. Noms de flottes concernes

| Cle | Anglais | Francais |
| --- | --- | --- |
| `Donanma_yi_Humayun` | Donanma-yi Humayun | Donanma-yi Humayun |
| `Armata_Grossa` | Armata Grossa | Armata Grossa |
| `Real_Marina_Napoletana` | Real Marina Napoletana | Real Marina Napoletana |
| `Marina_Genovese` | Marina Genovese | Marine génoise |
| `Escadre_de_Tripoli` | Escadre de Tripoli | Escadre de Tripoli |

## 4. Methode de correction utilisee

Les noms de flottes dans `common/history/military_formations` sont conserves tels quels. La correction consiste a ajouter des cles de localisation correspondant exactement aux identifiants directs utilises par les flottes.

Aucune syntaxe de formation militaire n'a ete changee.

## 5. Fichiers de localisation crees/modifies

Fichiers crees :

- `localization/english/phase_navy_2c_fleet_names_l_english.yml`
- `localization/french/phase_navy_2c_fleet_names_l_french.yml`

## 6. Confirmation UTF-8 BOM

Les deux fichiers de localisation ont ete reecrits en UTF-8 avec BOM.

## 7. Confirmation gameplay

NAVY-2C-bis ne modifie aucun gameplay :

- aucun navire modifie ;
- aucun `count` modifie ;
- aucun `hq_region` modifie ;
- aucune loi modifiee ;
- aucune technologie modifiee ;
- aucun batiment modifie ;
- aucune PM modifiee ;
- aucune pop modifiee ;
- aucune frontiere modifiee.

## 8. Confirmation amiraux

Aucun amiral n'a ete ajoute dans NAVY-2C-bis.

L'absence d'amiral pour les petites flottes mediterraneennes reste volontaire :

- `SIC`
- `GEN`
- `SAR`
- `PAP`
- `TUS`
- `TUN`
- `TRI`

## 9. Tests a refaire en jeu

1. Lancer une nouvelle partie 1776.
2. Verifier que les noms suivants s'affichent sans underscores :
   - Donanma-yi Humayun
   - Armata Grossa
   - Real Marina Napoletana
   - Marine génoise ou Marina Genovese selon la langue
   - Escadre de Tripoli
3. Verifier que `TUR` et `VEN` conservent leurs amiraux.
4. Verifier que `SIC`, `GEN`, `SAR`, `PAP`, `TUS`, `TUN` et `TRI` n'ont pas recu d'amiral par erreur.
5. Surveiller `error.log` pour :
   - `missing localization`
   - `invalid localization`
   - `invalid character`
   - `PostValidate`

## 10. Risques restants

- Si le jeu prefere afficher les noms directs non localises pour certaines formations, ces cles resteront inoffensives.
- Le fichier de localisation francais utilise `Marine génoise`. Les fichiers sont en UTF-8 BOM pour eviter les problemes d'encodage.
- Le statut Git contient encore les modifications NAVY-2C non commit ; elles sont anterieures a cette phase et n'ont pas ete modifiees par NAVY-2C-bis.
