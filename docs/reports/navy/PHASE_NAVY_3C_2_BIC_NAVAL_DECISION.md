# PHASE NAVY-3C-2 - British East India Company naval decision

## 1. Resume

Cette phase examine si la British East India Company (`BIC`) doit recevoir une flotte propre apres l'audit naval indien NAVY-3C.

Decision recommandee : ne pas creer de flotte BIC maintenant.

Raison principale : `BIC` est deja structuree comme compagnie coloniale sous influence britannique, dispose de ports et de chantiers pour representer la logistique coloniale, tandis que `GBR` possede deja une Royal Navy explicite, une loi navale professionnelle et une station navale couvrant les Indes orientales et la Chine. Ajouter une flotte BIC risquerait de dupliquer partiellement la Royal Navy sans corriger une erreur technique immediate.

## 2. Statut BIC

| Element | Situation actuelle | Commentaire |
| --- | --- | --- |
| Tag | `BIC` defini dans `common/country_definitions/00_countries.txt` | Tag complet, non fantome. |
| Type de pays | `country_type = colonial` | Coherent avec une compagnie coloniale. |
| Rang | `tier = principality` | Statut inferieur a un Etat souverain majeur. |
| Culture principale | `british` | L'administration est modelisee comme britannique. |
| Capitale | `STATE_CEYLON` | Configuration actuelle du mod, non modifiee ici. |
| Fichier pays | `common/history/countries/bic - british east india company.txt` | Le pays recoit lois, technologies et variables de depart. |
| Lois civiles/coloniales | `law_colonial_administration`, `law_colonial_exploitation`, `law_subjecthood`, etc. | Renforce le role colonial et administratif. |
| Loi militaire terrestre | `law_professional_army` | Presence terrestre explicite. |
| Loi navale | Aucune loi navale explicite trouvee pour BIC | Pas de `law_professional_navy`, `law_merchant_navy`, `law_diplomatic_navy` ou equivalent. |
| Technologies | `effect_starting_technology_tier_4_tech`, `academia`, `colonization`, `line_infantry`, `law_enforcement` | Aucun signal naval specifique ajoute par le fichier pays. |
| Sujets | `JEY` et `COO` comme puppets de BIC | BIC a une sphere locale, mais pas une marine autonome. |
| Relation avec GBR | `GBR` cree un pacte `chartered_company` vers `BIC` | BIC depend formellement de GBR dans le setup diplomatique. |
| Relations diplomatiques | `GBR` a `set_relations = { country = c:BIC value = 80 }` | Relation fortement positive. |
| Service militaire | `GBR` cree `exempt_from_service` avec BIC | Le mod represente deja un statut special vis-a-vis de l'empire britannique. |

## 3. Infrastructure navale BIC

Les audits NAVY-3A et NAVY-3C indiquaient pour BIC : 9 ports, 2 chantiers navals, 0 administration navale.

Verification directe :

| Element | Situation actuelle | Commentaire |
| --- | --- | --- |
| Ports dans `10_india.txt` | 8 niveaux de `building_port` | Principalement Bengal / Circars. |
| Port dans `11_east_asia.txt` | 1 niveau de `building_port` a `STATE_PEGU` | Explique le total de 9 ports signale par NAVY-3C. |
| Chantiers navals | 2 niveaux de `building_shipyard` a `STATE_WEST_BENGAL` | Infrastructure de construction ou de support, pas forcement flotte autonome. |
| Administration navale | 0 `building_naval_base` trouve pour BIC | Aucune base navale militaire propre. |
| Administration civile | 45 niveaux de `building_government_administration` detectes dans les regions BIC | Forte presence administrative, non navale. |
| Propriete britannique indirecte | Plusieurs blocs `company_east_india_company` appartiennent a `c:GBR` | Confirme que l'economie coloniale est deja raccordee a GBR. |

Conclusion : les ports et chantiers BIC suffisent a representer la logistique et l'infrastructure coloniales sans imposer une flotte militaire BIC.

## 4. Flotte absente

`common/history/military_formations/05_military_formations_india.txt` contient pour `c:BIC` :

- une formation terrestre `Bengal_Army` ;
- des unites d'infanterie, cavalerie et artillerie ;
- plusieurs generaux ;
- aucune formation `type = fleet` dans le bloc BIC ;
- aucun amiral BIC.

La seule flotte proche dans le fichier indien est `TravancoreNavy`, mais elle appartient a `TRA` et n'est pas concernee par cette phase.

## 5. Relation avec GBR

Le fichier `common/history/diplomacy/00_subject_relationships.txt` indique :

- `c:GBR` cree un pacte `chartered_company` avec `c:BIC` ;
- `c:GBR` cree aussi un pacte `exempt_from_service` avec `c:BIC` ;
- `c:BIC` a ses propres puppets locaux (`JEY`, `COO`) ;
- `c:BIC` recoit `add_liberty_desire = -30`.

Le fichier `common/history/diplomacy/00_relations.txt` indique :

- `c:GBR` a une relation de `+80` avec `c:BIC` ;
- `c:BIC` entretient des relations negatives avec plusieurs puissances indiennes ou asiatiques, ce qui pose BIC comme acteur regional colonial, mais pas necessairement naval.

## 6. Risque de duplication Royal Navy

`GBR` possede deja une structure navale tres explicite :

- `law_professional_navy` activee dans `common/history/countries/gbr - great britain.txt` ;
- plusieurs flottes dans `common/history/military_formations/00_military_formations_europe.txt` ;
- `Portsmouth_Station` ;
- `Plymouth_Station` ;
- `Mediterranean_Station` ;
- `North_America_and_West_Indies_Station` ;
- `East_Indies_and_China_Station`.

La station `East_Indies_and_China_Station` couvre deja le role naval britannique en Asie orientale et dans l'ocean Indien. Elle comprend des vaisseaux de ligne et des fregates, avec l'amiral `Edward Hughes`.

Une flotte BIC propre risquerait donc :

- de doubler la couverture navale britannique en Inde ;
- de rendre BIC trop autonome militairement ;
- d'augmenter la puissance coloniale britannique indirecte sans besoin technique ;
- d'ajouter de nouveaux objets a tester alors que NAVY-3C n'a pas identifie de crash lie a l'absence de flotte BIC.

## 7. Options etudiees

### Option 1 - Ne rien faire

BIC conserve ses ports, ses chantiers et son armee terrestre, mais ne recoit pas de flotte propre.

Avantages :

- option la plus prudente ;
- respecte le role de `GBR` comme couverture navale imperiale ;
- evite la duplication de la Royal Navy ;
- ne cree pas d'amiral ni de nouvelle formation a tester ;
- conserve le setup NAVY-3C sans ajouter de risque.

Inconvenients :

- BIC ne peut pas projeter une force navale autonome ;
- les ports/chantiers BIC restent purement logistiques ou economiques.

### Option 2 - Flotte symbolique minimale

Creer une flotte BIC tres limitee, par exemple :

- 0 vaisseau de ligne ;
- 1 a 2 fregates maximum ;
- nom possible : `Bengal Marine` ou `East India Company Marine` ;
- aucune creation d'amiral dans cette phase.

Avantages :

- donne une presence navale locale visible a BIC ;
- peut representer une marine de compagnie ou de transport.

Inconvenients :

- duplication partielle de `East_Indies_and_China_Station` ;
- risque d'augmenter artificiellement la capacite militaire britannique en Inde ;
- demanderait une phase dediee pour verifier lois navales, amiraute, noms, localisation et equilibre ;
- non necessaire pour corriger un probleme de lancement.

### Option 3 - Flotte coloniale plus large

Creer une flotte militaire BIC autonome et significative.

Cette option est rejetee.

Raisons :

- elle surmodeliserait BIC ;
- elle ferait concurrence a la Royal Navy ;
- elle imposerait de nouveaux amiraux, nouvelles localisations et nouveaux tests ;
- elle depasse l'objectif technique de NAVY-3C-2.

## 8. Recommandation finale

Recommandation : Option 1 - ne rien faire maintenant.

BIC doit rester sans flotte propre dans cette phase. Ses 9 ports et ses 2 chantiers navals representent suffisamment l'infrastructure coloniale et commerciale. La protection navale et la projection maritime doivent rester du cote de `GBR`, deja dotee d'une Royal Navy puissante et d'une `East_Indies_and_China_Station`.

Si un besoin gameplay apparait plus tard, il faudra creer une phase future specifique et limitee, avec recherche historique, test d'equilibre et validation que la flotte ne duplique pas la Royal Navy.

## 9. Decision gameplay

Decision appliquee : aucune modification gameplay.

La phase NAVY-3C-2 est uniquement documentaire. Aucune flotte BIC, aucun amiral, aucune technologie, aucune PM, aucun batiment, aucun pays et aucune formation militaire n'ont ete modifies.

## 10. Confirmation des fichiers gameplay

Aucun fichier gameplay n'a ete modifie dans cette phase.

Le seul fichier cree par cette phase est :

- `docs/reports/navy/PHASE_NAVY_3C_2_BIC_NAVAL_DECISION.md`

## 11. Risques restants

- BIC reste sans capacite navale autonome, ce qui peut limiter son comportement si le moteur attend une flotte pour certaines actions maritimes.
- L'absence de loi navale BIC reste volontairement non corrigee.
- Les ports et chantiers BIC peuvent donner une impression d'infrastructure navale non exploitee, mais cela reste acceptable pour une compagnie coloniale dependante de GBR.
- Le fichier de formations indien contient encore des sujets hors scope NAVY-3C-2, notamment des armees terrestres et une flotte Travancore, mais ils ne doivent pas etre modifies ici.

## 12. Fichiers lus

- `docs/reports/navy/PHASE_NAVY_3C_INDIAN_NAVAL_AUDIT.md`
- `docs/reports/navy/PHASE_NAVY_3A_NON_EUROPEAN_NAVAL_AUDIT.md`
- `common/history/countries/bic - british east india company.txt`
- `common/history/countries/gbr - great britain.txt`
- `common/history/buildings/10_india.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/military_formations/05_military_formations_india.txt`
- `common/history/diplomacy/00_subject_relationships.txt`
- `common/history/diplomacy/00_relations.txt`
- `common/history/military_formations/00_military_formations_europe.txt`
- `common/country_definitions/00_countries.txt`

