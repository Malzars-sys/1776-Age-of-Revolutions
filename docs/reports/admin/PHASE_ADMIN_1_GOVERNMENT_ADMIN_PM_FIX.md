# Phase ADMIN-1 - PM des administrations gouvernementales FRA / GBR

## 1. Resume du probleme observe

En jeu, les administrations gouvernementales de la France et de la Grande-Bretagne pouvaient demarrer sur une methode administrative trop primitive ou retomber dessus, alors que ces pays disposent deja du niveau technologique permettant une meilleure administration au depart.

Le point important est que le nom affiche en francais peut preter a confusion. La PM corrigee n'est pas la PM avancee `pm_vertical_filing_cabinets`, mais la deuxieme PM administrative vanilla disponible avec la technologie de depart : `pm_horizontal_drawer_cabinets`.

## 2. Confirmation de la technologie de depart FRA / GBR

Fichiers verifies :
- `common/history/countries/fra - france.txt`
- `common/history/countries/gbr - great britain.txt`

Les deux pays utilisent :

```txt
effect_starting_technology_tier_4_tech = yes
```

Dans la vanilla The Great Wave, cet effet donne notamment :

```txt
add_technology_researched = tech_bureaucracy
add_technology_researched = centralization
```

Il ne donne pas `central_archives`.

Conclusion :
- FRA et GBR ont bien `centralization` au depart ;
- FRA et GBR n'ont pas explicitement `central_archives` au depart ;
- la PM compatible est donc `pm_horizontal_drawer_cabinets`.

## 3. PM vanilla identifiee

Reference vanilla :
- `C:\Games\Victoria 3 The Great Wave\game\common\production_methods\07_government.txt`

PM pertinentes :
- `pm_simple_offices` : PM primitive.
- `pm_horizontal_drawer_cabinets` : deverrouillee par `centralization`.
- `pm_vertical_filing_cabinets` : deverrouillee par `central_archives`.

La correction utilise uniquement :

```txt
pm_horizontal_drawer_cabinets
```

## 4. Syntaxe vanilla confirmee

La syntaxe vanilla dans `common/history/buildings` est :

```txt
activate_production_methods={ "pm_horizontal_drawer_cabinets" "pm_professional_bureaucrats" "pm_religious_bureaucrats" }
```

ou equivalent avec les PM dans un autre ordre.

## 5. Administrations auditees avant correction

Les administrations FRA/GBR ciblees avaient `pm_vertical_filing_cabinets`, une PM trop avancee pour leur technologie de depart effective.

GBR :
- `STATE_HOME_COUNTIES`, niveau 10.
- `STATE_LANCASHIRE`, niveau 5.
- `STATE_YORKSHIRE`, niveau 5.
- `STATE_MIDLANDS`, niveau 5.
- `STATE_EAST_ANGLIA`, niveau 2.
- `STATE_WEST_COUNTRY`, niveau 5.
- `STATE_LOWLANDS`, niveau 3.

FRA :
- `STATE_ILE_DE_FRANCE`, niveau 30.
- `STATE_NORMANDY`, niveau 5.
- `STATE_RHONE`, niveau 6.
- `STATE_AUVERGNE_LIMOUSIN`, niveau 3.
- `STATE_BRITTANY`, niveau 5.

## 6. Corrections appliquees

Fichier modifie :
- `common/history/buildings/00_west_europe.txt`

Correction appliquee uniquement dans les blocs `building_government_administration` de FRA et GBR :

```txt
pm_vertical_filing_cabinets -> pm_horizontal_drawer_cabinets
```

Les PM d'organisation bureaucratique existantes ont ete conservees :
- `pm_professional_bureaucrats`
- `pm_religious_bureaucrats`

## 7. Niveaux de batiments

Aucun niveau de batiment n'a ete modifie.

La correction ne change que les PM initiales.

## 8. Elements non modifies

Non modifies :
- flottes ;
- navires ;
- amiraux ;
- `hq_region` ;
- lois ;
- technologies ;
- niveaux de batiments ;
- batiments navals ;
- Espagne ;
- Russie ;
- Japon, Australie, Moyen-Orient et autres pays.

Les occurrences restantes de `pm_vertical_filing_cabinets` concernent d'autres pays, notamment BEO et PRU, et ont ete laissees intactes.

## 9. Tests a refaire en jeu

1. Lancer une nouvelle partie 1776 avec le mod seul.
2. Ouvrir la France.
3. Verifier les administrations gouvernementales : elles doivent utiliser la PM correspondant a `pm_horizontal_drawer_cabinets`.
4. Ouvrir la Grande-Bretagne.
5. Faire la meme verification.
6. Verifier que l'Espagne, la Russie et les autres pays n'ont pas ete modifies.
7. Laisser tourner un mois en observateur.
8. Verifier `error.log` pour :
   - `invalid production method`;
   - `building_government_administration`;
   - `PostValidate`.

## 10. Risques restants

- Si le mod donne plus tard `central_archives` a FRA/GBR dans une phase separee, il faudra reevaluer `pm_vertical_filing_cabinets`.
- Cette phase ne corrige pas les administrations d'autres pays, meme si certaines utilisent aussi `pm_vertical_filing_cabinets`.
- L'equilibre economique general n'a pas ete retouche.
