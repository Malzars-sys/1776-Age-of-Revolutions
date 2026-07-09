# Phase ADMIN-2 - Audit mondial des PM d'administration gouvernementale

## 1. Résumé du problème

ADMIN-1 avait montré que certaines administrations utilisaient `pm_vertical_filing_cabinets` alors que le pays propriétaire ne possédait que `centralization`, pas `central_archives`.

ADMIN-2 a étendu l'audit à tous les `building_government_administration` présents dans `common/history/buildings/*.txt`, en comparant :

- la PM administrative de départ du bâtiment ;
- le pays propriétaire du bâtiment ;
- les technologies de départ du pays dans `common/history/countries/*.txt` ;
- les effets vanilla The Great Wave situés dans `C:\Games\Victoria 3 The Great Wave\game`.

Résultat après correction :

- 227 administrations gouvernementales auditées ;
- 38 PM trop avancées corrigées ;
- 0 PM administrative restante clairement trop avancée par rapport aux technologies connues ;
- aucun niveau de bâtiment modifié.

## 2. PM vanilla identifiées

Référence : `C:\Games\Victoria 3 The Great Wave\game\common\production_methods\07_government.txt`

| PM administrative | Technologie requise | Niveau approximatif |
|---|---:|---|
| `pm_simple_organization` | aucune | primitive |
| `pm_horizontal_drawer_cabinets` | `centralization` | administration centralisée |
| `pm_vertical_filing_cabinets` | `central_archives` | administration avancée |
| `pm_switch_boards` | `central_planning` | administration tardive |

Note : l'ID vanilla n'est pas `pm_simple_offices`, mais `pm_simple_organization`.

## 3. Effets de départ technologique résolus

Référence : `C:\Games\Victoria 3 The Great Wave\game\common\scripted_effects\00_starting_inventions.txt`

| Effet | Technologies administratives utiles |
|---|---|
| `effect_starting_technology_tier_1_tech` | `add_era_researched = era_1`, donc `centralization`, plus `central_archives` explicite |
| `effect_starting_technology_tier_2_tech` | `add_era_researched = era_1`, donc `centralization` |
| `effect_starting_technology_tier_3_tech` | `centralization` |
| `effect_starting_technology_tier_4_tech` | `centralization` |
| `effect_starting_technology_tier_5_tech` | `tech_bureaucracy`, pas `centralization` |
| `effect_starting_technology_tier_6_tech` | aucune PM administrative avancée |
| `effect_starting_technology_tier_7_tech` | aucune |

La règle appliquée est donc :

- `central_archives` présent : `pm_vertical_filing_cabinets` autorisé ;
- `centralization` présent sans `central_archives` : `pm_horizontal_drawer_cabinets` ;
- pas de `centralization` : `pm_simple_organization`.

## 4. Tableau global des pays audités

70 tags propriétaires apparaissent dans des administrations gouvernementales de départ.

| Groupe | Pays / tags |
|---|---|
| Corrigés dans cette phase | `BEO`, `PRU`, `MUG`, `MYS`, `MARATH`, `CHI`, `KOR` |
| OK après audit, sans modification ADMIN-2 | `AUS`, `BAD`, `BAV`, `BHV`, `BIC`, `BRZ`, `BUR`, `CON`, `CRO`, `DAI`, `DEI`, `DENNOR`, `DUR`, `ETH`, `GAL`, `GBR`, `GEN`, `GR3`, `HAN`, `HAW`, `HUN`, `JAP`, `NET`, `PAP`, `PLC`, `POR`, `PUD`, `RUS`, `SAR`, `SAX`, `SCH`, `SIA`, `SIC`, `SPA`, `SWE`, `SWI`, `TIB`, `TRS`, `UBD`, `USA`, `VEN`, `WAL`, `WUR` |
| Trop primitives mais non corrigées | `FRA`, `GR5`, `HAI`, `HYD`, `OMA`, `PER`, `PHI`, `SC1`, `SC2`, `SC3`, `SC4`, `TUR`, `TUS` |
| Ambigus car tag propriétaire non résolu dans `common/history/countries` | `AIT`, `AWA`, `GWA`, `MAS`, `MOR`, `PAN`, `SOK` |

## 5. Tableau des administrations auditées

Résumé après correction :

| PM active après ADMIN-2 | Nombre de blocs |
|---|---:|
| `pm_horizontal_drawer_cabinets` | 132 |
| `pm_simple_organization` | 95 |
| `pm_vertical_filing_cabinets` | 0 |
| `pm_switch_boards` | 0 |

Statuts après correction :

| Statut | Nombre |
|---|---:|
| OK ou conservé car compatible | 188 |
| Trop primitive mais non corrigée | 29 |
| Ambigu, tag pays non résolu | 10 |
| Trop avancée restante | 0 |

## 6. Incohérences trouvées

### Trop avancées

Ces blocs utilisaient une PM nécessitant une technologie absente.

| Fichier | Pays | State | Ancienne PM | PM correcte |
|---|---:|---|---|---|
| `common/history/buildings/00_west_europe.txt` | `BEO` | `STATE_WALLONIA` | `pm_vertical_filing_cabinets` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/00_west_europe.txt` | `BEO` | `STATE_FLANDERS` | `pm_vertical_filing_cabinets` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/00_west_europe.txt` | `PRU` | `STATE_RHINELAND` | `pm_vertical_filing_cabinets` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/00_west_europe.txt` | `PRU` | `STATE_BRANDENBURG` | `pm_vertical_filing_cabinets` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/10_india.txt` | `MUG` | `STATE_DELHI` | `pm_horizontal_drawer_cabinets` | `pm_simple_organization` |
| `common/history/buildings/10_india.txt` | `MYS` | `STATE_MYSORE` | `pm_horizontal_drawer_cabinets` | `pm_simple_organization` |
| `common/history/buildings/10_india.txt` | `MARATH` | `STATE_BOMBAY` | `pm_horizontal_drawer_cabinets` | `pm_simple_organization` |
| `common/history/buildings/11_east_asia.txt` | `CHI` | 26 administrations chinoises | `pm_horizontal_drawer_cabinets` | `pm_simple_organization` |
| `common/history/buildings/11_east_asia.txt` | `KOR` | 5 administrations coréennes | `pm_horizontal_drawer_cabinets` | `pm_simple_organization` |

Les 26 states `CHI` corrigés sont :

`STATE_SICHUAN`, `STATE_YUNNAN`, `STATE_GUIZHOU`, `STATE_SHAOZHOU`, `STATE_GUANGXI`, `STATE_BEIJING`, `STATE_SOUTHERN_MANCHURIA`, `STATE_SHANXI`, `STATE_NINGXIA`, `STATE_XIAN`, `STATE_CHONGQING`, `STATE_GUANGDONG`, `STATE_FUJIAN`, `STATE_ZHEJIANG`, `STATE_JIANGSU`, `STATE_NANJING`, `STATE_HENAN`, `STATE_ZHILI`, `STATE_JIANGXI`, `STATE_SOUTHERN_ANHUI`, `STATE_NORTHERN_ANHUI`, `STATE_WESTERN_HUBEI`, `STATE_EASTERN_HUBEI`, `STATE_HUNAN`, `STATE_SHANDONG`, `STATE_SUZHOU`.

Les 5 states `KOR` corrigés sont :

`STATE_SEOUL`, `STATE_BUSAN`, `STATE_YANGHO`, `STATE_SARIWON`, `STATE_PYONGYANG`.

## 7. Corrections appliquées

Fichiers modifiés pour ADMIN-2 :

- `common/history/buildings/00_west_europe.txt`
- `common/history/buildings/10_india.txt`
- `common/history/buildings/11_east_asia.txt`

Corrections :

- `BEO` et `PRU` : `pm_vertical_filing_cabinets` -> `pm_horizontal_drawer_cabinets`, car ils ont `centralization` mais pas `central_archives`.
- `MUG`, `MYS`, `MARATH`, `CHI`, `KOR` : `pm_horizontal_drawer_cabinets` -> `pm_simple_organization`, car leurs effets de départ donnent `tech_bureaucracy` mais pas `centralization`.

Les PM secondaires existantes ont été conservées :

- `pm_professional_bureaucrats`
- `pm_hereditary_bureaucrats`
- `pm_religious_bureaucrats`
- `pm_secular_bureaucrats`

## 8. Cas ambigus non modifiés

### PM simples mais pays avec `centralization`

Ces blocs sont techniquement plus primitifs que ce que la technologie permettrait, mais les corriger reviendrait à renforcer l'administration de départ de régions entières. Ils sont donc documentés sans modification.

| Fichier | Pays | State | PM actuelle | PM possible |
|---|---:|---|---|---|
| `common/history/buildings/01_south_europe.txt` | `TUS` | `STATE_TUSCANY` | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/01_south_europe.txt` | `TUR` | `STATE_ATTICA` | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/03_north_africa.txt` | `FRA` | `STATE_ALGIERS` | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/05_north_america.txt` | `SC1` | `STATE_BAJIO` | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/06_central_america.txt` | `SC1` | `STATE_SAN_SALVADOR`, `STATE_GUATEMALA` | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/06_central_america.txt` | `HAI`, `GR5` | `STATE_HAITI`, `STATE_SANTO_DOMINGO` | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/07_south_america.txt` | `SC2` | 6 states | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/07_south_america.txt` | `SC3` | 5 states | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/07_south_america.txt` | `SC4` | 2 states | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/08_middle_east.txt` | `OMA` | `STATE_OMAN` | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/08_middle_east.txt` | `PER` | 5 states persans | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/10_india.txt` | `HYD` | `STATE_HYDERABAD` | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |
| `common/history/buildings/12_indonesia.txt` | `PHI` | `STATE_LUZON` | `pm_simple_organization` | `pm_horizontal_drawer_cabinets` |

### Tags non résolus

Ces tags sont propriétaires d'administrations, mais l'audit n'a pas trouvé de définition technologique fiable dans `common/history/countries/*.txt` :

`AIT`, `AWA`, `GWA`, `MAS`, `MOR`, `PAN`, `SOK`.

Ils restent non modifiés.

## 9. Confirmations de périmètre

Confirmé :

- aucun niveau de bâtiment n'a été modifié ;
- aucune technologie n'a été modifiée ;
- aucune loi n'a été modifiée ;
- aucune flotte, navire ou amiral n'a été modifié ;
- aucune frontière, pop, diplomatie, sujet ou pays n'a été modifié ;
- seules des PM initiales de `building_government_administration` ont été corrigées.

## 10. Tests à refaire en jeu

1. Lancer une nouvelle partie 1776.
2. Vérifier France et Grande-Bretagne : administrations toujours en `pm_horizontal_drawer_cabinets`.
3. Vérifier Prusse : administrations de Rhénanie et Brandebourg en `pm_horizontal_drawer_cabinets`.
4. Vérifier Belgique ancienne / `BEO` : Wallonie et Flandres en `pm_horizontal_drawer_cabinets`.
5. Vérifier Chine et Corée : administrations en `pm_simple_organization`, sans erreur de PM invalide.
6. Vérifier Mughals, Mysore et Maratha : administrations ciblées en `pm_simple_organization`.
7. Laisser tourner un mois en observateur.
8. Contrôler `error.log` pour :
   - `invalid production method`;
   - `building_government_administration`;
   - `PostValidate`.

## 11. Risques restants

- Les cas "trop primitifs" peuvent être revus plus tard si l'objectif devient l'équilibrage économique/historique, mais ils ne sont pas incompatibles avec les technologies.
- Les tags non résolus doivent être audités dans une phase séparée si les logs montrent des erreurs de pays ou de setup.
- Les modifications touchent la Chine et la Corée : il faut surveiller l'impact sur bureaucratie, fiscalité et budget de départ.
