# Phase NAVY-3A - Audit des puissances navales non europeennes

## 1. Resume executif

Cette phase est un audit uniquement. Aucun fichier gameplay n'a ete modifie.

Le perimetre audite couvre les puissances non europeennes ou extra-europeennes prioritaires indiquees dans le prompt : Oman / Golfe / ocean Indien, Perse, Inde, Qing, Japon, Coree, Ryukyu, Ezo, Siam, Birmanie, Dai Viet, Brunei, Aceh, Johor et tags malais/indonesiens visibles. `DEI` est conserve en note, car il a deja ete traite dans NAVY-2B/NAVY-2D.

Constats principaux :

- Les seules flottes non europeennes ciblees trouvees sont `OMA`, `CHI` et `DEI`.
- `OMA` a une flotte de 6 navires, mais son `hq_region = sr:region_arabic` est invalide dans la vanilla The Great Wave / 1.13.
- `CHI` a deux flottes, `Bohai_Gulf_Fleet` et `Guangdong_Fleet`, avec des `hq_region` valides.
- `DEI` a une flotte coloniale de 3 fregates et une logistique minimale deja traitee ; ce tag reste hors correction NAVY-3A.
- Aucun des pays audites n'a de loi navale explicite `law_merchant_navy`, `law_professional_navy`, `law_diplomatic_navy` ou `law_jeune_ecole`.
- Plusieurs pays ont des ports ou chantiers sans flotte : `MARATH`, `JAP`, `KOR`, `DAI`, `ACE`, `LAN`, `BIC`.
- Plusieurs anciens `hq_region` non navals sont invalides dans les formations terrestres de Perse et d'Inde : `region_persia`, `region_bengal`, `region_madras`, `region_central_india`, `region_bombay`, `region_punjab`. Ils ne doivent pas etre corriges dans NAVY-3, mais ils meritent un audit militaire terrestre separe.
- Les tags indonesiens/malais `ACE`, `BRU`, `JOH`, `LAN`, ainsi que plusieurs tags utilises dans les states mais sans fichier pays complet apparent, doivent etre traites prudemment.

La suite recommandee est :

- NAVY-3B : Oman / Golfe / ocean Indien.
- NAVY-3C : Inde et compagnies indiennes non deja traitees.
- NAVY-3D : Asie de l'Est.
- NAVY-3E : Asie du Sud-Est et monde malais/indonesien.

## 2. Chemin vanilla utilise

Reference vanilla confirmee :

```txt
C:\Games\Victoria 3 The Great Wave\game
```

Fichiers vanilla consultes :

- `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\east_asia_strategic_regions.txt`
- `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\west_south_asia_strategic_regions.txt`
- `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\water_strategic_regions.txt`
- `C:\Games\Victoria 3 The Great Wave\game\common\ship_types\00_ship_types.txt`

Regions vanilla utiles confirmees :

- `region_arabia`
- `region_greater_persia`
- `region_south_india`
- `region_north_india`
- `region_indochina`
- `region_indonesia`
- `region_south_china`
- `region_north_china`
- `region_northeast_asia`
- `region_persian_gulf`
- `region_arabian_sea`
- `region_laccadive_sea`
- `region_bay_of_bengal`
- `region_east_china_sea`
- `region_sea_of_japan`
- `region_yellow_sea`
- `region_japan_current`
- `region_western_indian_ocean`

`region_arabic`, `region_persia`, `region_bengal`, `region_madras`, `region_central_india`, `region_bombay`, `region_punjab` et `region_manchuria` n'ont pas ete trouves comme regions vanilla 1.13.

Les types de navires `ship_type_ship_of_the_line` et `ship_type_frigate` existent bien dans la vanilla 1.13.

## 3. Tags trouves par zone

| Zone | Nom historique | Tag trouve | Fichier pays trouve ? | Presence buildings ? | Presence military_formations ? | Statut |
|---|---|---:|---|---|---|---|
| Ocean Indien / Golfe | Oman / Mascate | `OMA` | oui, `oma - oman.txt` | oui | oui, flotte | actif, a traiter en NAVY-3B |
| Ocean Indien / Golfe | Perse | `PER` | oui, `per - persia.txt` | oui, mais pas naval | oui, armees | actif, pas de flotte |
| Inde | Empire moghol | `MUG` | oui, `mug - mughals.txt` | oui, non naval | oui, armee | actif, pas de flotte |
| Inde | Marathes | `MARATH` | oui, `marath - maratha empire.txt` | oui, naval minimal | oui, armee | actif, pas de flotte |
| Inde | Mysore | `MYS` | oui, `mys - mysore.txt` | oui, non naval | oui, armee | actif, pas de flotte |
| Inde | Hyderabad | `HYD` | oui, `hyd - hyderabad.txt` | oui, non naval | oui, armee | actif, pas de flotte |
| Inde / colonial | British East India Company | `BIC` | oui, `bic - british east india company.txt` | oui, naval | oui, armee | tag colonial separe, a isoler |
| Inde | Sindh | `SIN` | pas de fichier history country trouve | oui, non naval | oui, armee | tag ambigu |
| Asie de l'Est | Qing | `CHI` | oui, `chi - china.txt` | oui, naval | oui, deux flottes | actif |
| Asie de l'Est | Japon | `JAP` | oui, `jap - japan.txt` | oui, naval minimal | oui, armees | actif, pas de flotte |
| Asie de l'Est | Coree | `KOR` | oui, `kor - korea.txt` | oui, naval minimal | non | actif, pas de flotte |
| Asie de l'Est | Ryukyu | `RYU` | oui, `ryu - ryukyu.txt` | oui, non naval | non | actif, tributaire, pas de flotte |
| Asie de l'Est | Ezo | `EZO` | oui, `ezo - ezochi.txt` | non | non | actif, pas naval |
| Asie du Sud-Est | Siam | `SIA` | oui, `sia - siam.txt` | oui, non naval dans le parsing | non | actif, pas de flotte |
| Asie du Sud-Est | Birmanie | `BUR` | oui, `bur - burma.txt` | oui, non naval | oui, armees | actif, pas de flotte |
| Asie du Sud-Est | Dai Viet | `DAI` | oui, `dai - dai viet.txt` | oui, ports | non | actif, pas de flotte |
| Asie du Sud-Est | Brunei | `BRU` | country definition oui, pas de history country | oui, non naval | non | tag incomplet/ambigu |
| Asie du Sud-Est | Aceh | `ACE` | country definition oui, pas de history country | oui, port | non | tag incomplet/ambigu |
| Asie du Sud-Est | Johor | `JOH` | country definition oui, pas de history country | oui, non naval | non | tag incomplet/ambigu |
| Asie du Sud-Est | Bali | `BAL` | oui, `bal - bali.txt` | oui, non naval | non | actif, pas de flotte |
| Asie du Sud-Est | Cambodge | `CAM` | oui, `cam - cambodia.txt` | oui, non naval | non | actif, pas de flotte |
| Asie du Sud-Est | Lanfang | `LAN` | country definition oui, pas de history country | oui, port | non | tag ambigu |
| Asie du Sud-Est | Luang Prabang / Laos | `LUA` | country definition oui, pas de history country | oui, non naval | non | tag ambigu |
| Hors perimetre direct | Dutch East Indies Company | `DEI` | oui, `dei - dutch east indies company.txt`, pas de country definition directe | oui, naval | oui, flotte | deja traite NAVY-2 |

## 4. Flottes existantes par pays

| Pays | Flotte | Fichier / ligne | hq_region | Valide vanilla ? | Vaisseaux de ligne | Fregates | Total | Amiral ? | Statut |
|---|---|---:|---|---|---:|---:|---:|---|---|
| `OMA` | `Bahriat_alMasqat` | `common/history/military_formations/04_military_formations_middle_east.txt:260` | `region_arabic` | non | 1 | 5 | 6 | non | flotte active, HQ invalide, pas d'admin navale |
| `CHI` | `Bohai_Gulf_Fleet` | `common/history/military_formations/06_military_formations_asia.txt:481` | `region_north_china` | oui | 0 | 7 | 7 | non | flotte de jonques representee en fregates |
| `CHI` | `Guangdong_Fleet` | `common/history/military_formations/06_military_formations_asia.txt:511` | `region_south_china` | oui | 0 | 8 | 8 | non | flotte de jonques representee en fregates |
| `DEI` | `Koloniale_Marine` | `common/history/military_formations/06_military_formations_asia.txt:586` | `region_indonesia` | oui | 0 | 3 | 3 | non | deja traite, hors NAVY-3A sauf note |

Commentaire :

- `OMA` est la priorite technique NAVY-3B : une flotte existe deja, mais son HQ est invalide.
- `CHI` a deja un modele naval symbolique important : 15 fregates au total. C'est beaucoup pour une flotte non modernisee, mais le commentaire de fichier indique explicitement une representation de jonques de guerre.
- Aucun amiral historique n'est attache aux flottes ciblees.

## 5. Pays avec 0 navire mais qui pourraient en meriter

| Pays | Situation actuelle | Pourquoi un audit futur peut etre utile | Priorite |
|---|---|---|---|
| `MARATH` | 2 ports, 1 chantier, 0 flotte | puissance indienne cotiere avec infrastructure navale minimale | NAVY-3C |
| `BIC` | 9 ports, 2 chantiers, 0 flotte | compagnie coloniale separee, non couverte par les corrections europeennes directes | NAVY-3C, avec prudence coloniale |
| `JAP` | 3 ports, 1 chantier, 0 flotte | pays insulaire, mais Sakoku 1776 justifie une marine limitee ou absente | NAVY-3D, recherche dediee |
| `KOR` | 1 port, 1 chantier, 0 flotte | pays cotier avec infrastructure minimale | NAVY-3D, recherche dediee |
| `DAI` | 2 ports, 0 chantier, 0 flotte | pays cotier d'Asie du Sud-Est | NAVY-3E |
| `ACE` | 1 port, 0 chantier, 0 flotte | tag maritime possible, mais fichier pays incomplet | NAVY-3E apres clarification tag |
| `LAN` | 1 port, 0 chantier, 0 flotte | tag present en buildings/states, statut politique a clarifier | NAVY-3E ou hors perimetre si non maritime |
| `SIA` | pas de port/chantiers detectes pour le tag, 0 flotte | royaume regional majeur, mais setup actuel ne lui donne pas de logistique navale claire | NAVY-3E, diagnostic historique avant ajout |
| `BUR` | pas de port/chantiers detectes pour le tag, 0 flotte | possede des armees, peut avoir une facade maritime selon states | NAVY-3E seulement si les states confirment un littoral utile |
| `BRU` / `JOH` | tags definis, pas de history country trouve, 0 flotte | petits Etats malais potentiellement maritimes | ne pas modifier sans completer l'audit tag |

## 6. hq_region invalides ou suspects

### Flottes ciblees

| Pays | Flotte | hq_region actuel | Valide vanilla ? | Region recommandee future |
|---|---|---|---|---|
| `OMA` | `Bahriat_alMasqat` | `region_arabic` | non | `region_arabia` en choix terrestre prudent ; `region_arabian_sea`, `region_persian_gulf` ou `region_western_indian_ocean` seulement si les HQ maritimes sont confirmes acceptes |
| `CHI` | `Bohai_Gulf_Fleet` | `region_north_china` | oui | aucune correction HQ evidente |
| `CHI` | `Guangdong_Fleet` | `region_south_china` | oui | aucune correction HQ evidente |
| `DEI` | `Koloniale_Marine` | `region_indonesia` | oui | deja traite |

### Formations non navales dans le meme perimetre

Ces erreurs ne sont pas des corrections NAVY-3A, mais elles sont importantes pour un audit technique futur :

| Pays | hq_region invalide | Fichier / ligne | Note |
|---|---|---:|---|
| `PER` | `region_persia` | `common/history/military_formations/04_military_formations_middle_east.txt:281`, `:323` | vanilla 1.13 utilise `region_greater_persia` |
| `BIC` | `region_bengal` | `common/history/military_formations/05_military_formations_india.txt:118` | ancien decoupage indien |
| `HYD` | `region_madras` | `common/history/military_formations/05_military_formations_india.txt:231` | ancien decoupage indien |
| `MARATH` | `region_central_india` | `common/history/military_formations/05_military_formations_india.txt:314` | ancien decoupage indien |
| `MYS` | `region_madras` | `common/history/military_formations/05_military_formations_india.txt:410` | ancien decoupage indien |
| `SIN` | `region_bombay` | `common/history/military_formations/05_military_formations_india.txt:661` | ancien decoupage indien |
| `MUG` | `region_punjab` | `common/history/military_formations/05_military_formations_india.txt:692` | ancien decoupage indien |
| `CHI` | `region_manchuria` | `common/history/military_formations/06_military_formations_asia.txt:174` | a verifier hors flottes Qing |

## 7. Batiments navals par pays

Comptage base sur les `levels` d'ownership des blocs `create_building`.

| Pays | Ports | Chantiers navals | Administration navale | Flotte actuelle | Statut logistique |
|---|---:|---:|---:|---:|---|
| `OMA` | 5 | 1 | 0 | 6 | flotte sans administration navale ; chantier present |
| `PER` | 0 | 0 | 0 | 0 | aucun besoin naval evident |
| `MUG` | 0 | 0 | 0 | 0 | aucun besoin naval evident dans le setup |
| `MARATH` | 2 | 1 | 0 | 0 | infrastructure navale sans flotte |
| `MYS` | 0 | 0 | 0 | 0 | aucun besoin naval evident |
| `HYD` | 0 | 0 | 0 | 0 | aucun besoin naval evident |
| `CHI` | 19 | 4 | 0 | 15 | flotte importante sans administration navale |
| `JAP` | 3 | 1 | 0 | 0 | ports/chantiers sans flotte ; Sakoku a respecter |
| `KOR` | 1 | 1 | 0 | 0 | infrastructure minimale sans flotte |
| `RYU` | 0 | 0 | 0 | 0 | tributaire, pas de logistique propre |
| `EZO` | 0 | 0 | 0 | 0 | pas de logistique propre |
| `SIA` | 0 | 0 | 0 | 0 | pas de logistique navale claire |
| `BUR` | 0 | 0 | 0 | 0 | pas de logistique navale claire |
| `DAI` | 2 | 0 | 0 | 0 | ports sans flotte |
| `BRU` | 0 | 0 | 0 | 0 | tag a clarifier |
| `ACE` | 1 | 0 | 0 | 0 | port sans flotte |
| `JOH` | 0 | 0 | 0 | 0 | tag a clarifier |
| `BAL` | 0 | 0 | 0 | 0 | pas de logistique propre |
| `CAM` | 0 | 0 | 0 | 0 | pas de logistique propre |
| `LAN` | 1 | 0 | 0 | 0 | port sans flotte, statut a clarifier |
| `LUA` | 0 | 0 | 0 | 0 | pas de logistique propre |
| `BIC` | 9 | 2 | 0 | 0 | grosse infrastructure coloniale sans flotte propre |
| `SIN` | 0 | 0 | 0 | 0 | tag ambigu, pas de logistique propre |
| `DEI` | 6 | 1 | 2 | 3 | deja traite, logistique minimale coherente |

Aucun ancien ID naval obsolete `building_military_shipyard`, `building_naval_base` ou `pm_military_shipbuilding_*` n'a ete detecte dans les blocs audites.

## 8. Lois navales actuelles par pays

Recherche effectuee dans `common/history/countries/*` pour :

- `law_merchant_navy`
- `law_professional_navy`
- `law_diplomatic_navy`
- `law_jeune_ecole`
- `lawgroup_navy_model`
- `effect_starting_technology_tier_*`
- `military_drill`

| Pays | Loi navale actuelle | Tech de depart pertinente | Loi future recommandee | Commentaire |
|---|---|---|---|---|
| `OMA` | aucune | `effect_starting_technology_tier_4_tech` | `law_merchant_navy` possible | a verifier en NAVY-3B, pas de doctrine moderne |
| `PER` | aucune | tier 4 + `admiralty` | aucune a ce stade | pas de flotte, pays surtout terrestre |
| `MUG` | aucune | tier 5 | aucune a ce stade | pas de flotte |
| `MARATH` | aucune | tier 5 + `international_trade` | aucune ou `law_merchant_navy` si flotte future | ne pas ajouter avant audit historique |
| `MYS` | aucune | tier 5 | aucune a ce stade | pas de logistique navale |
| `HYD` | aucune | tier 4 | aucune a ce stade | pas de logistique navale |
| `CHI` | aucune | tier 5 + techs civiles | aucune ou `law_merchant_navy` tres prudente | flotte symbolique deja forte ; ne pas surmoderniser |
| `JAP` | aucune | tier 4 + techs civiles | aucune a ce stade | Sakoku 1776, eviter doctrine navale moderne |
| `KOR` | aucune | tier 5 | aucune a ce stade | pas de flotte |
| `RYU` | aucune | tier 4 | aucune a ce stade | tributaire japonais |
| `EZO` | aucune | tier 4 | aucune | non naval |
| `SIA` | aucune | tier 6 + `sericulture` | aucune ou `law_merchant_navy` apres recherche | setup naval absent |
| `BUR` | aucune | tier 5 + `mandatory_service` | aucune a ce stade | pas de flotte |
| `DAI` | aucune | tier 5 + `sericulture` | aucune ou `law_merchant_navy` apres recherche | ports sans flotte |
| `BAL` | aucune | tier 5 | aucune | pas de flotte |
| `CAM` | aucune | tier 5 + `sericulture` | aucune | pas de flotte |
| `BIC` | aucune | tier 4 + colonization + line infantry | a traiter avec prudence | compagnie coloniale, pourrait dependre de la marine britannique |
| `DEI` | aucune | tier 4 + colonization + corporate charters | deja traite, ne pas modifier ici | flotte coloniale minimale |

`law_jeune_ecole` ne doit etre recommande nulle part pour 1776 dans ce perimetre.

## 9. Classification historique / gameplay

| Categorie | Pays | Lecture prudente |
|---|---|---|
| Puissance regionale maritime reelle | `OMA` | flotte existante, ports et chantier ; priorite technique HQ + logistique |
| Grande puissance terrestre avec flotte limitee | `CHI` | deux flottes symboliques deja presentes ; eviter de renforcer sans recherche dediee |
| Grande puissance terrestre sans flotte | `PER`, `MUG` | pas de correction navale immediate |
| Etat indien cotier ou semi-cotier a potentiel | `MARATH`, `BIC` | ports/chantiers presents ; audit dedie avant creation de flotte |
| Etat indien interieur ou peu naval | `MYS`, `HYD`, `SIN` | pas de flotte a creer sans preuve historique |
| Pays insulaire ou peninsulaire sous contraintes politiques | `JAP`, `KOR`, `RYU`, `EZO` | presence de ports/chantiers mais Sakoku/tributs/statut local doivent primer |
| Pays cotiers d'Asie du Sud-Est | `SIA`, `BUR`, `DAI`, `ACE`, `BRU`, `JOH`, `BAL`, `CAM`, `LAN` | besoin de clarification tag + historique ; pas de creation mecanique |
| Tag colonial deja traite | `DEI` | ne pas retoucher dans NAVY-3A |

## 10. Propositions futures par pays

| Pays | Action future proposee | Priorite | Commentaire |
|---|---|---|---|
| `OMA` | corriger `region_arabic`, evaluer reduction ou maintien de la flotte, ajouter administration navale minimale si la flotte reste a 6 navires | haute | NAVY-3B |
| `CHI` | ne pas toucher d'abord ; verifier en jeu les besoins d'equipage de 15 fregates sans administration navale | moyenne | NAVY-3D |
| `MARATH` | auditer historique maritime + role du chantier existant avant toute flotte | moyenne | NAVY-3C |
| `BIC` | clarifier si une flotte propre est souhaitable ou si elle doit rester couverte par `GBR` | moyenne | NAVY-3C |
| `JAP` | conserver Sakoku ; eventuelle flotte symbolique seulement si recherche dediee | basse-moyenne | NAVY-3D |
| `KOR` | ne pas ajouter de flotte sans recherche ; verifier si chantier represente une capacite cotiere | basse | NAVY-3D |
| `DAI` | petit audit cotier possible, sans doctrine navale forte | basse-moyenne | NAVY-3E |
| `ACE` / `BRU` / `JOH` | clarifier fichiers pays avant toute marine | moyenne | NAVY-3E |
| `SIA` / `BUR` | verifier states littoraux et ports avant toute flotte | basse-moyenne | NAVY-3E |
| `PER`, `MUG`, `MYS`, `HYD` | aucune correction navale immediate | basse | risque principal plutot terrestre / hq_region |
| `DEI` | aucune correction NAVY-3A | aucune | deja traite |

## 11. Besoins en logistique navale

| Pays | Besoin probable | Justification |
|---|---|---|
| `OMA` | administration navale minimale a evaluer | 6 navires, 0 `building_naval_administration` |
| `CHI` | grosse question ouverte | 15 fregates, 0 `building_naval_administration`, mais flotte symbolique/jonques |
| `DEI` | deja couvert | 3 fregates, 2 administrations navales apres NAVY-2D-bis |
| `MARATH` | pas de besoin tant qu'il n'y a pas de flotte | 2 ports + 1 chantier, 0 navire |
| `BIC` | pas de besoin tant qu'il n'y a pas de flotte propre | peut rester dependante de `GBR` |
| `JAP` / `KOR` | pas de besoin tant qu'il n'y a pas de flotte | ports/chantiers presents mais 0 navire |
| `DAI` / `ACE` / `LAN` | pas de besoin tant qu'il n'y a pas de flotte | ports seuls |

Hypothese de prudence reprise des phases NAVY-2D-bis : si une flotte est conservee, l'administration navale doit couvrir l'equipage reel observe en jeu, mais ce calcul ne doit etre applique qu'au moment d'une correction, pas dans cet audit.

## 12. Noms de flottes et amiraux candidats

Cette phase ne cree aucun amiral.

| Pays | Nom de flotte possible | Amiral candidat | Confiance | Recommandation |
|---|---|---|---|---|
| `OMA` | `Bahriat_alMasqat`, Flotte de Mascate, Flotte d'Oman | recherche dediee necessaire | faible | ne pas inventer ; verifier Mascate/Zanzibar/Oman 1776 |
| `CHI` | `Bohai_Gulf_Fleet`, `Guangdong_Fleet` | recherche dediee necessaire | faible | ne pas ajouter d'amiral Qing sans source solide |
| `MARATH` | flotte de la cote konkan / Maratha navy | recherche dediee necessaire | faible-moyenne | attention a l'anachronisme et au niveau reel en 1776 |
| `BIC` | Bengal Marine / Bombay Marine selon setup | recherche dediee necessaire | moyenne | clarifier si tag doit avoir flotte propre ou dependance britannique |
| `JAP` | flotte cotiere du shogunat | recherche dediee necessaire | faible | Sakoku : ne pas moderniser |
| `KOR` | flotte cotiere Joseon | recherche dediee necessaire | faible | pas d'ajout sans recherche |
| `DAI` | flotte de Dai Viet / flotte de Nguyen ou Trinh selon setup | recherche dediee necessaire | faible | verifier l'etat politique exact du mod |
| `ACE` | flotte d'Aceh | recherche dediee necessaire | faible | d'abord creer/clarifier history country si necessaire |
| `BRU` / `JOH` | flottes malaises locales | recherche dediee necessaire | faible | tags incomplets, ne pas toucher |
| `DEI` | `Koloniale_Marine` | deja hors perimetre | moyenne | ne pas retoucher dans NAVY-3A |

Pour les liens Wikipedia des personnages historiques, la recommandation reste de ne les ajouter qu'apres selection d'amiraux historiquement solides. Aucun candidat non europeen n'est assez confirme dans cet audit pour justifier une fiche personnage.

## 13. Tags ambigus ou a ne pas toucher

| Tag | Probleme | Recommandation |
|---|---|---|
| `DEI` | pas de country definition directe, mais history country et setup colonial existent | ne pas retoucher dans NAVY-3A |
| `BRU` | country definition presente, pas de history country trouve | clarifier avant tout navire |
| `ACE` | country definition presente, pas de history country trouve | clarifier avant tout navire |
| `JOH` | country definition presente, pas de history country trouve | clarifier avant tout navire |
| `SIN` | military formations et buildings existent, mais pas de history country trouve | clarifier avant correction indienne |
| `LAN` | country definition presente, pas de history country trouve | clarifier role politique |
| `LUA` | country definition presente, pas de history country trouve | probablement hors naval |
| `BAL` | history country existe, mais pas de flotte/logistique navale | ne pas toucher sans recherche |
| Tags indonesiens visibles sans definition complete (`YOG`, `SRK`, `SAK`, `JMB`, `BNJ`, `KTI`, `BLG`, `SMB`, `PON`, `SUL`, `TID`, `SLW`, `PRK`, `SEL`) | utilises ou possibles dans states/buildings, mais pas de fichier pays clair dans l'audit rapide | ne pas creer de flottes avant audit tag par tag |

## 14. Decoupage recommande NAVY-3B / 3C / 3D / 3E

### NAVY-3B - Oman / ocean Indien

Perimetre recommande :

- `OMA`
- verification des possessions omanaises en Afrique orientale et Golfe
- Mascate / Zanzibar seulement si les tags existent clairement

Objectif probable :

- remplacer `region_arabic` par une region vanilla valide ;
- decider si `1 SOL + 5 fregates` est conserve ou reduit ;
- ajouter une logistique navale minimale uniquement si la flotte reste maintenue.

### NAVY-3C - Inde

Perimetre recommande :

- `MARATH`
- `BIC`
- `MUG`
- `MYS`
- `HYD`
- `SIN` et autres tags indiens cotiers seulement apres clarification

Objectif probable :

- ne pas creer de flotte partout ;
- traiter d'abord les tags avec ports/chantiers (`MARATH`, `BIC`) ;
- separer la question navale de l'audit des `hq_region` terrestres invalides.

### NAVY-3D - Asie de l'Est

Perimetre recommande :

- `CHI`
- `JAP`
- `KOR`
- `RYU`
- `EZO`

Objectif probable :

- verifier si les deux flottes Qing doivent rester a 15 fregates ;
- ne pas ajouter d'amiral Qing/Japon/Coree sans recherche ;
- conserver la logique Sakoku du Japon ;
- ne pas donner de flotte a Ryukyu ou Ezo sans justification forte.

### NAVY-3E - Asie du Sud-Est

Perimetre recommande :

- `SIA`
- `BUR`
- `DAI`
- `ACE`
- `BRU`
- `JOH`
- `BAL`
- `CAM`
- `LAN` si pertinent

Objectif probable :

- clarifier les tags incomplets ;
- identifier quels pays ont vraiment un littoral et un role naval ;
- eviter les ajouts de flottes mecaniques aux petits tags.

## 15. Risques techniques

- Corriger `OMA` sans verifier la region HQ peut faire passer l'erreur de `region_arabic` a une autre region inadaptee ; `region_arabia` est le choix terrestre le plus prudent.
- Ajouter de l'administration navale a `CHI` ou `OMA` changera l'economie et les emplois, meme si cela corrige une penurie d'equipage.
- Les flottes Qing sont deja volumineuses pour des navires symboliques ; les renforcer serait risque pour l'equilibrage.
- Les tags indiens utilisent plusieurs anciens `hq_region` invalides, mais les corriger dans une phase navale melangerait deux systemes.
- `BIC` et `DEI` sont des compagnies coloniales : les traiter comme des puissances navales autonomes peut dupliquer la puissance navale britannique/neerlandaise.
- Les tags malais/indonesiens incomplets peuvent provoquer des erreurs si on leur ajoute des flottes ou des personnages avant d'avoir verifie country definitions, history countries, diplomacy et localisation.
- Ajouter des amiraux non sources risque de creer des personnages anachroniques.

## 16. Liste exacte des fichiers lus

Fichiers du mod lus ou analyses :

- `docs/reports/navy/PHASE_NAVY_2A_SECONDARY_EUROPEAN_NAVAL_AUDIT.md`
- `docs/reports/navy/PHASE_NAVY_2D_SECONDARY_NAVAL_LOGISTICS.md`
- `docs/reports/navy/PHASE_NAVY_2D_BIS_NAVAL_CREW_CAPACITY_FIX.md`
- `common/country_definitions/00_countries.txt`
- `common/country_definitions/02_modded_countries.txt`
- `common/history/countries/oma - oman.txt`
- `common/history/countries/per - persia.txt`
- `common/history/countries/mug - mughals.txt`
- `common/history/countries/marath - maratha empire.txt`
- `common/history/countries/mys - mysore.txt`
- `common/history/countries/hyd - hyderabad.txt`
- `common/history/countries/chi - china.txt`
- `common/history/countries/jap - japan.txt`
- `common/history/countries/kor - korea.txt`
- `common/history/countries/ryu - ryukyu.txt`
- `common/history/countries/ezo - ezochi.txt`
- `common/history/countries/sia - siam.txt`
- `common/history/countries/bur - burma.txt`
- `common/history/countries/dai - dai viet.txt`
- `common/history/countries/dei - dutch east indies company.txt`
- `common/history/countries/bic - british east india company.txt`
- `common/history/countries/bal - bali.txt`
- `common/history/countries/cam - cambodia.txt`
- `common/history/military_formations/04_military_formations_middle_east.txt`
- `common/history/military_formations/05_military_formations_india.txt`
- `common/history/military_formations/06_military_formations_asia.txt`
- `common/history/buildings/04_subsaharan_africa.txt`
- `common/history/buildings/08_middle_east.txt`
- `common/history/buildings/09_central_asia.txt`
- `common/history/buildings/10_india.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/buildings/12_indonesia.txt`
- `common/history/states/00_states.txt`
- `common/history/diplomacy/*.txt`

Fichiers vanilla lus :

- `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\east_asia_strategic_regions.txt`
- `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\west_south_asia_strategic_regions.txt`
- `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\water_strategic_regions.txt`
- `C:\Games\Victoria 3 The Great Wave\game\common\ship_types\00_ship_types.txt`

## 17. Confirmation qu'aucun fichier gameplay n'a ete modifie

Cette phase NAVY-3A n'a modifie aucun fichier gameplay.

Le seul fichier cree pour cette phase est :

```txt
docs/reports/navy/PHASE_NAVY_3A_NON_EUROPEAN_NAVAL_AUDIT.md
```

Note de contexte : au moment de l'audit, la branche active locale etait `phase1-map-compatibility`, et le depot contenait deja des modifications ou rapports precedents NAVY-2D/NAVY-2D-bis. Ces changements preexistants n'ont pas ete modifies par NAVY-3A.
