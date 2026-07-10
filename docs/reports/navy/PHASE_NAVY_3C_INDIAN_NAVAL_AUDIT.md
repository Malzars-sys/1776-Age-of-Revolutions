# Phase NAVY-3C - Audit prudent de l'Inde navale

## 1. Resume executif

Cette phase est un audit uniquement. Aucun fichier gameplay n'a ete modifie.

Constats principaux :

- `BIC` est un tag colonial complet : country definition, history country, states, diplomacy, formations terrestres et batiments existent.
- `BIC` a une forte infrastructure navale dans le sous-continent : 9 ports et 2 chantiers navals, mais aucune flotte propre.
- `MARATH` a une infrastructure navale minimale : 2 ports et 1 chantier naval en `STATE_BOMBAY`, mais aucune flotte.
- `MUG`, `MYS`, `HYD` existent et ont des formations terrestres, mais pas de flotte ni infrastructure navale evidente.
- `SIN` est present en country definition, states, diplomacy, buildings et formation terrestre, mais aucun fichier `common/history/countries/sin*.txt` n'a ete trouve ; il reste donc ambigu.
- Un petit tag indien non liste dans NAVY-3A, `TRA` / Travancore, possede deja une flotte : `TravancoreNavy`, 1 fregate, avec `hq_region = sr:region_madras`, invalide en vanilla 1.13.
- Les anciens `hq_region` indiens sont massivement invalides : `region_bengal`, `region_madras`, `region_central_india`, `region_bombay`, `region_punjab`.
- Les regions vanilla 1.13 utiles confirmees sont surtout `region_north_india`, `region_south_india`, `region_bay_of_bengal` et `region_laccadive_sea`.

La suite la plus prudente est de separer clairement :

- une phase technique terrestre pour les `hq_region` d'armees indiennes ;
- une decision separee sur `BIC` ;
- une decision separee sur `MARATH` ;
- une petite phase specifique sur `TRA` / Travancore si la flotte existante doit etre corrigee.

## 2. Confirmation audit uniquement

NAVY-3C-AUDIT ne modifie pas :

- fichiers `common/history/military_formations` ;
- fichiers `common/history/buildings` ;
- fichiers `common/history/countries` ;
- localisation ;
- navires ;
- flottes ;
- `hq_region` ;
- lois ;
- technologies ;
- PM ;
- pops ;
- frontieres ;
- amiraux.

Le seul fichier cree par cette phase est :

```txt
docs/reports/navy/PHASE_NAVY_3C_INDIAN_NAVAL_AUDIT.md
```

## 3. Tags indiens trouves

| Tag | Nom historique probable | Fichier pays ? | Country definition ? | Presence states ? | Presence diplomacy ? | Statut |
|---|---|---|---|---|---|---|
| `BIC` | British East India Company | oui, `bic - british east india company.txt` | oui | oui | oui | colonial complet |
| `MARATH` | Empire marathe | oui, `marath - maratha empire.txt` | oui, modded | oui | oui | actif clair, potentiel naval |
| `MUG` | Empire moghol | oui, `mug - mughals.txt` | oui | oui | oui | actif, terrestre |
| `MYS` | Mysore | oui, `mys - mysore.txt` | oui | oui | oui | actif, terrestre |
| `HYD` | Hyderabad | oui, `hyd - hyderabad.txt` | oui | oui | oui | actif, terrestre |
| `SIN` | Sindh | non trouve | oui | oui | oui | ambigu |
| `PAN` | Punjab | non trouve | oui | oui | oui | actif/ambigu, terrestre |
| `AWA` | Awadh / Oudh | non trouve | oui | oui | non | actif/ambigu, terrestre |
| `GWA` | Gwalior | non trouve | oui | oui | oui | actif/ambigu, terrestre |
| `NAG` | Nagpur | oui, `nag - nagpur.txt` | oui | oui | non | actif, terrestre |
| `BHV` | Bhavnagar / Gujarati prince | oui, `bhv - gujarati prince.txt` | oui | oui | non | actif, petit cotier |
| `PUD` | Pudukottai | oui, `pud - pudukottai.txt` | oui | oui | oui | actif, petit cotier |
| `COC` | Cochin | oui, `coc - cochin.txt` | oui | oui | oui | actif, cotier mais sans batiments navals propres trouves |
| `TRA` | Travancore | non trouve | oui | oui | non | actif/ambigu, flotte existante |
| `COO` | Cooch Behar | oui, `coo - cooch behar.txt` | oui | oui | oui | actif, terrestre |
| `GAR` | Garhwal | non trouve | oui | oui | oui | actif/ambigu, terrestre |
| `SAT` | Satara | non trouve | oui | oui | oui | actif/ambigu, terrestre |
| `KHP` | Kolhapur | non trouve | oui | oui | oui | actif/ambigu, terrestre/cotier potentiel |
| `KNO` | Kurnool | non trouve | oui | oui | oui | actif/ambigu, terrestre |
| `JEY` | Jeypore | non trouve | oui | oui | oui | actif/ambigu, terrestre |
| `SIK` | Sikkim | non trouve | oui | oui | non | actif/ambigu, non naval |
| `NEP` | Nepal | oui, `nep - nepal.txt` | oui | oui | non | actif, non naval |
| `BHU` | Bhutan | non trouve | oui | oui | non | actif/ambigu, non naval |
| `BNG` | Bengal ? | non trouve | non trouve | oui | non | ambigu |
| `ORI` | Orissa ? | non trouve | oui | non | non | absent/hors setup indien actuel |
| `CEY` | Ceylon ? | non trouve | oui | non | non | tag defini mais non utilise ici ; Ceylon est colonial `DEI`/`GBR` |
| `TRV` | Travancore ? | non trouve | non trouve | non | non | absent ; le mod utilise `TRA` |
| `CARN` | Carnatic ? | non trouve | non trouve | non | non | absent dans l'audit |
| `RAJ` | Rajputana ? | non trouve | oui | non | non | tag defini, mais pas actif dans les fichiers audites |
| `AWD` | Awadh alternatif ? | non trouve | non trouve | non | non | absent ; le mod utilise `AWA` |

Tags europeens/coloniaux presents dans les fichiers indiens mais hors NAVY-3C gameplay :

- `GBR`
- `FRA`
- `NET`
- `POR`
- `DENNOR`
- `DEI`

Ils ne doivent pas etre modifies dans une phase indienne sans decision dediee.

## 4. Batiments navals par pays

Comptage sur tous les fichiers `common/history/buildings/*`, avec focus sur les owners indiens ou directement presents dans `10_india.txt`.

| Pays | Ports | Chantiers navals | Administration navale | States concernes | Statut logistique |
|---|---:|---:|---:|---|---|
| `BIC` | 9 | 2 | 0 | `STATE_WEST_BENGAL`, `STATE_EAST_BENGAL`, `STATE_CIRCARS`, `STATE_PEGU` | infrastructure coloniale forte sans flotte propre |
| `MARATH` | 2 | 1 | 0 | `STATE_BOMBAY` | ports/chantiers sans flotte |
| `BHV` | 1 | 0 | 0 | `STATE_GUJARAT` | petit port sans flotte |
| `PUD` | 1 | 0 | 0 | `STATE_MADRAS` | petit port sans flotte |
| `TRA` | 0 | 0 | 0 | aucun batiment naval propre detecte | flotte existante sans infrastructure propre |
| `COC` | 0 | 0 | 0 | aucun batiment naval propre detecte | pas de logistique navale |
| `MUG` | 0 | 0 | 0 | aucun | pas de besoin naval clair |
| `MYS` | 0 | 0 | 0 | aucun | pas de besoin naval clair |
| `HYD` | 0 | 0 | 0 | aucun | pas de besoin naval clair |
| `SIN` | 0 | 0 | 0 | aucun | tag ambigu, pas de logistique navale |
| `NAG` | 0 | 0 | 0 | aucun | pas de besoin naval clair |
| `PAN`, `AWA`, `GWA`, `COO`, `GAR`, `SAT`, `KHP`, `KNO`, `JEY` | 0 | 0 | 0 | aucun | pas de logistique navale detectee |

Colonial hors correction indienne :

| Pays | Ports | Chantiers navals | Administration navale | Note |
|---|---:|---:|---:|---|
| `DEI` | 6 | 1 | 2 | deja traite NAVY-2, possede aussi Ceylon |
| `GBR` | 38 | 18 | 33 | grande puissance deja traitee |
| `NET` | 12 | 4 | 13 | deja traite NAVY-2 |
| `POR` | 16 | 6 | 9 | deja traite NAVY-2 |
| `FRA` | 21 | 14 | 24 | deja traitee NAVY-1 |
| `DENNOR` | 11 | 4 | 9 | deja traite NAVY-2 |

Aucun ancien ID naval obsolete `building_military_shipyard`, `building_naval_base` ou `pm_military_shipbuilding_*` n'a ete trouve dans les blocs indiens audites.

## 5. Flottes existantes ou absence de flottes

Une seule flotte indienne ou princely-state indienne a ete trouvee :

| Pays | Flotte | Fichier / ligne | hq_region | Valide vanilla ? | SOL | Fregates | Total | Amiral ? | Statut |
|---|---|---:|---|---|---:|---:|---:|---|---|
| `TRA` | `TravancoreNavy` | `common/history/military_formations/05_military_formations_india.txt:646` | `region_madras` | non | 0 | 1 | 1 | non | flotte existante, petite, HQ invalide, pas de logistique propre |

Absence de flotte confirmee pour les principaux tags :

- `BIC`
- `MARATH`
- `MUG`
- `MYS`
- `HYD`
- `SIN`
- `BHV`
- `PUD`
- `COC`
- `NAG`
- `PAN`
- `AWA`
- `GWA`
- `KHP`
- `KNO`
- `JEY`

Conclusion : l'Inde du mod n'est pas totalement sans marine, mais la seule marine locale trouvee est Travancore, pas `BIC` ni `MARATH`.

## 6. hq_region invalides ou suspects

Comparaison vanilla 1.13 :

- `region_north_india` existe.
- `region_south_india` existe.
- `region_bay_of_bengal` existe.
- `region_laccadive_sea` existe.
- `region_bengal` n'existe pas.
- `region_madras` n'existe pas.
- `region_central_india` n'existe pas.
- `region_bombay` n'existe pas.
- `region_punjab` n'existe pas.

| Pays | Formation | Type | hq_region actuel | Valide vanilla ? | Region recommandee future | Type de correction |
|---|---|---|---|---|---|---|
| `PAN` | `FaujiKhas`, `FaujiAin`, `FaujiBe_Qawaid` | armees | `region_punjab` | non | `region_north_india` | terrestre |
| `BIC` | `Bengal_Army` | armee | `region_bengal` | non | `region_north_india` ou `region_south_india` selon decoupage final | terrestre |
| `HYD` | `sarf_e_khas` | armee | `region_madras` | non | `region_south_india` | terrestre |
| `AWA` | `OudhRoyalArmy` | armee | `region_central_india` | non | `region_north_india` | terrestre |
| `MARATH` | `OudhRoyalArmy` | armee | `region_central_india` | non | `region_north_india` ou `region_south_india` a verifier | terrestre |
| `GWA` | `GwaliorArmy` | armee | `region_central_india` | non | `region_north_india` | terrestre |
| `NAG` | `NagpurArmy` | armee | `region_central_india` | non | `region_south_india` ou `region_north_india` a verifier | terrestre |
| `MYS` | `MysoreArmy` | armee | `region_madras` | non | `region_south_india` | terrestre |
| `COO` | `CoochBeharArmy` | armee | `region_bengal` | non | `region_north_india` | terrestre |
| `GAR` | `GarhwalArmy` | armee | `region_punjab` | non | `region_north_india` | terrestre |
| `SAT` | `SataraArmy` | armee | `region_bombay` | non | `region_south_india` | terrestre |
| `KHP` | `KolhapurArmy` | armee | `region_bombay` | non | `region_south_india` | terrestre |
| `KNO` | `KurnoolArmy` | armee | `region_madras` | non | `region_south_india` | terrestre |
| `BHV` | `BhavnagarArmy` | armee | `region_bombay` | non | `region_south_india` ou `region_north_india` a verifier | terrestre |
| `PUD` | `PudukottaiArmy` | armee | `region_madras` | non | `region_south_india` | terrestre |
| `JEY` | `JeyporeArmy` | armee | `region_madras` | non | `region_south_india` | terrestre |
| `COC` | `CochinArmy` | armee | `region_madras` | non | `region_south_india` | terrestre |
| `TRA` | `TravancoreArmy` | armee | `region_madras` | non | `region_south_india` | terrestre |
| `TRA` | `TravancoreNavy` | flotte | `region_madras` | non | `region_south_india` en choix terrestre prudent ; `region_laccadive_sea` seulement si HQ maritime accepte | naval |
| `SIN` | `SindhArmy` | armee | `region_bombay` | non | `region_north_india` ou `region_south_india` a verifier | terrestre |
| `MUG` | `MughalArmy` | armee | `region_punjab` | non | `region_north_india` | terrestre |

Important : la majorite des corrections sont terrestres, pas navales. Elles ne doivent pas etre enfouies dans une phase de creation de flottes.

## 7. Lois navales et techs pertinentes

| Pays | Loi navale actuelle | Techs pertinentes | Loi future possible | Commentaire |
|---|---|---|---|---|
| `BIC` | aucune | tier 4, `colonization`, `line_infantry` | aucune par defaut ; `law_merchant_navy` seulement si flotte propre decidee | risque fort de duplication avec `GBR` |
| `MARATH` | aucune | tier 5, `international_trade` | `law_merchant_navy` possible mais non prioritaire | seulement apres recherche historique dediee |
| `BHV` | aucune | tier 5, `international_trade` | aucune par defaut | petit port, pas de flotte |
| `MUG` | aucune | tier 5 | aucune | terrestre |
| `MYS` | aucune | tier 5 | aucune | terrestre |
| `HYD` | aucune | tier 4 | aucune | terrestre/interieur |
| `NAG` | aucune | tier 5 | aucune | terrestre |
| `NEP` | aucune | tier 5 | aucune | non naval |
| `PUD` | aucune | tier 4 | aucune par defaut | petit port, pas de flotte |
| `COC` | aucune | tier 5 | aucune par defaut | cotier, mais pas d'infrastructure navale trouvee |
| `TRA` | aucun fichier history country trouve | inconnu | aucune par defaut | flotte existante a corriger techniquement plus tard |
| `SIN` | aucun fichier history country trouve | inconnu | aucune | tag ambigu |

Regles de prudence :

- ne pas recommander `law_jeune_ecole` ;
- ne pas recommander `law_professional_navy` pour les Etats indiens sans justification historique forte ;
- `law_merchant_navy` peut etre une option future pour `MARATH` ou une compagnie coloniale, mais ne doit pas etre appliquee automatiquement ;
- `BIC` doit etre analyse comme compagnie coloniale liee a `GBR`, pas comme puissance navale autonome evidente.

## 8. Analyse BIC

`BIC` est un tag colonial complet.

Elements confirmes :

- country definition : oui ;
- fichier pays : `common/history/countries/bic - british east india company.txt` ;
- states : oui ;
- diplomacy : oui ;
- formations militaires : oui, notamment `Bengal_Army` ;
- batiments navals : 9 ports, 2 chantiers navals ;
- flotte propre : aucune ;
- loi navale : aucune.

Interpretation prudente :

- L'absence de flotte peut etre volontaire : `BIC` est une compagnie britannique et peut etre couverte par la Royal Navy.
- Ajouter une flotte `BIC` risque de dupliquer la puissance navale britannique si `GBR` conserve deja sa flotte globale.
- Une petite flotte symbolique de commerce/transport pourrait etre envisagee plus tard, mais seulement si on accepte que `BIC` ait une capacite autonome limitee.
- Une flotte de combat `BIC` importante serait probablement une erreur d'equilibrage.

Recommendation :

- ne rien changer pour l'instant ;
- faire une phase dediee `NAVY-3C-2` pour decider entre :
  - laisser `BIC` sans flotte propre ;
  - ajouter une flotte symbolique minimale ;
  - representer la capacite maritime via ports/chantiers seulement.

## 9. Analyse MARATH

`MARATH` est actif et clair.

Elements confirmes :

- country definition : oui, dans `02_modded_countries.txt` ;
- fichier pays : `common/history/countries/marath - maratha empire.txt` ;
- states : oui ;
- diplomacy : oui ;
- formation terrestre : oui ;
- batiments navals : 2 ports + 1 chantier naval en `STATE_BOMBAY` ;
- flotte propre : aucune ;
- loi navale : aucune ;
- tech pertinente : `international_trade`.

Interpretation prudente :

- `STATE_BOMBAY` donne un littoral clair et une infrastructure navale minimale.
- Le chantier existant peut justifier une petite flotte future, mais pas automatiquement.
- La marine marathe / cote konkan demande une recherche historique dediee avant ajout, notamment pour eviter une flotte trop moderne ou trop forte.
- Si une flotte est ajoutee plus tard, elle devrait probablement etre symbolique ou cotiere, avec peu de fregates et aucune grosse doctrine.

Recommendation :

- ne rien modifier dans cette phase ;
- lancer une recherche historique dediee avant tout ajout ;
- separer la question de flotte de la correction terrestre `region_central_india`.

## 10. Analyse des autres Etats indiens

| Pays | Analyse | Recommandation |
|---|---|---|
| `TRA` | possede deja `TravancoreNavy`, 1 fregate, mais pas de logistique navale propre et HQ invalide | phase technique dediee possible, sans creation de nouvelle flotte |
| `BHV` | petit port en Gujarat, pas de flotte | ne rien faire sans recherche |
| `PUD` | petit port en Madras, pas de flotte | ne rien faire sans recherche |
| `COC` | Cochin est cotier, mais aucun port/chantiers propres detectes | clarification avant toute marine |
| `MUG` | puissance symbolique/terrestre, pas de port naval | aucune action navale |
| `MYS` | terrestre/interieur dans le setup actuel | aucune action navale |
| `HYD` | terrestre/interieur dans le setup actuel | aucune action navale |
| `SIN` | Sindh a formation terrestre mais pas de fichier pays | clarification tag avant tout |
| `NAG`, `GWA`, `AWA`, `PAN`, `COO`, `GAR`, `SAT`, `KHP`, `KNO`, `JEY` | formations terrestres, pas de logistique navale detectee | traiter seulement dans une phase hq_region terrestre |
| `NEP`, `BHU`, `SIK` | non navals | hors naval |

## 11. Tags ambigus

| Tag | Ambiguite | Action future |
|---|---|---|
| `SIN` | pas de fichier history country trouve, mais states/diplomacy/formations existent | clarifier avant toute correction majeure |
| `TRA` | flotte existante mais pas de fichier history country trouve | clarifier avant correction navale/logistique |
| `AWA`, `GWA`, `PAN`, `GAR`, `SAT`, `KHP`, `KNO`, `JEY` | country definitions et formations, mais pas de fichiers pays trouves | phase terrestre/tag audit |
| `BNG` | apparait dans states, mais pas de country definition ni history country | ne pas toucher |
| `TRV`, `CARN`, `AWD` | absents dans les fichiers audites | ne pas utiliser ; le mod emploie d'autres tags |
| `CEY` | country definition presente mais Ceylon est gere par `DEI`/`GBR` dans buildings | ne pas utiliser sans audit colonial |
| `RAJ`, `ORI` | country definitions presentes mais pas actifs dans les fichiers indiens audites | hors correction navale |

## 12. Recommandations futures

Priorite technique :

1. Corriger les `hq_region` terrestres indiens dans une phase non navale.
2. Corriger `TRA` / `TravancoreNavy` si les logs signalent directement sa flotte.
3. Decider si `BIC` doit rester sans flotte propre.
4. Decider si `MARATH` merite une petite flotte cotiere.

Recommandations par pays :

| Pays | Recommendation |
|---|---|
| `BIC` | probablement laisser sans flotte propre tant que `GBR` couvre la mer ; audit dedie avant toute creation |
| `MARATH` | recherche historique dediee sur marine marathe / cote konkan avant ajout |
| `TRA` | correction technique possible de la flotte existante, mais ne pas ajouter de navires |
| `BHV`, `PUD`, `COC` | pas de flotte sans recherche et clarification |
| `MUG`, `MYS`, `HYD`, `NAG`, `GWA`, `AWA`, `PAN` | pas de phase navale ; corriger seulement les HQ terrestres plus tard |
| `SIN` | clarifier tag avant toute intervention |

## 13. Separation corrections navales / corrections terrestres

Corrections navales futures possibles :

- `TRA` : corriger `TravancoreNavy`, `region_madras` invalide, et verifier si une logistique minimale est necessaire.
- `BIC` : decider s'il faut une flotte symbolique ou conserver l'absence de flotte.
- `MARATH` : decider s'il faut une petite flotte cotiere.

Corrections terrestres futures :

- remplacer les anciens `hq_region` des armees indiennes ;
- traiter `region_bengal`, `region_madras`, `region_central_india`, `region_bombay`, `region_punjab` ;
- utiliser `region_north_india` / `region_south_india` apres verification state par state.

Ces deux chantiers ne doivent pas etre melanges.

## 14. Risques techniques

- Ajouter une flotte `BIC` peut doubler artificiellement la Royal Navy.
- Ajouter une flotte `MARATH` sans recherche peut surmodeler une puissance cotiere.
- Corriger tous les `hq_region` indiens en une seule phase navale risquerait de casser les formations terrestres.
- `TRA` a deja une flotte mais pas de fichier pays clair ; une correction de logistique pourrait exiger une clarification tag.
- Les petits tags indiens ont des niveaux de completion inegaux : certains ont country definition et formation, mais pas de history country.
- Les regions maritimes `region_bay_of_bengal` et `region_laccadive_sea` existent, mais il faut confirmer qu'elles sont acceptees comme HQ de flotte avant usage.

## 15. Decoupage recommande apres audit

Suite prudente proposee :

- `NAVY-3C-1` : correction technique des `hq_region` terrestres indiens, hors naval.
- `NAVY-3C-2` : decision `BIC`, flotte propre ou absence volontaire.
- `NAVY-3C-3` : decision `MARATH`, petite flotte cotiere ou pas.
- `NAVY-3C-4` : traitement specifique `TRA` / TravancoreNavy si les logs ou le gameplay le justifient.
- `NAVY-3C-5` : petits tags cotiers (`BHV`, `PUD`, `COC`, `SIN`) seulement apres clarification.

Aucune de ces phases n'est lancee maintenant.

## 16. Liste exacte des fichiers lus

Fichiers du mod lus ou analyses :

- `docs/reports/navy/PHASE_NAVY_3A_NON_EUROPEAN_NAVAL_AUDIT.md`
- `common/country_definitions/00_countries.txt`
- `common/country_definitions/02_modded_countries.txt`
- `common/history/countries/bic - british east india company.txt`
- `common/history/countries/marath - maratha empire.txt`
- `common/history/countries/mug - mughals.txt`
- `common/history/countries/mys - mysore.txt`
- `common/history/countries/hyd - hyderabad.txt`
- `common/history/countries/bhv - gujarati prince.txt`
- `common/history/countries/pud - pudukottai.txt`
- `common/history/countries/coc - cochin.txt`
- `common/history/countries/coo - cooch behar.txt`
- `common/history/countries/nag - nagpur.txt`
- `common/history/countries/nep - nepal.txt`
- `common/history/states/00_states.txt`
- `common/history/buildings/09_central_asia.txt`
- `common/history/buildings/10_india.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/military_formations/05_military_formations_india.txt`
- `common/history/diplomacy/00_relations.txt`
- `common/history/diplomacy/00_subject_relationships.txt`

Fichiers vanilla lus :

- `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\west_south_asia_strategic_regions.txt`
- `C:\Games\Victoria 3 The Great Wave\game\common\strategic_regions\water_strategic_regions.txt`

## 17. Confirmation qu'aucun fichier gameplay n'a ete modifie

Cette phase n'a modifie aucun fichier gameplay.

Le seul fichier cree est :

```txt
docs/reports/navy/PHASE_NAVY_3C_INDIAN_NAVAL_AUDIT.md
```
