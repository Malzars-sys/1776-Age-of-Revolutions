# TECH6B3C — Revue humaine de l'arbre technologique

> Réconciliation TECH6B3E : la matrice contient désormais les 24 arbitrages TECH6B3C originaux plus 7 familles `H01–H07` issues de la revue humaine runtime post-TECH6B3D. Elles figent Protectionnisme → `political_economy`, assurance publique → `organized_immunization_campaigns`, la répartition `human_rights`/`labor_movement`, athéisme d'État → `socialism`, Terakoya sans gate, la progression des cinq lois d'esclavage et l'affichage de `stock_exchange`/`joint_stock_companies`. Ces décisions postérieures priment sur toute formulation contradictoire ci-dessous.

Statut documentaire : **PASS**  
Branche : `tech6b3c-tree-human-review`  
Portée : audit, arbitrage et spécification seulement. Aucune recommandation n'est implémentée pendant TECH6B3C.

> Addendum moteur avant TECH6B3D : `steel_frame_buildings` appartient à Society. Victoria 3 interdisant les prérequis entre catégories, toute arête prévue entre ce nœud et une technologie Production est abandonnée. Cette correction utilisateur postérieure prime sur les formulations initiales de P31/P32/P35.

## A. Checkpoint

TECH6B3C reprend les livrables TECH6B3A et TECH6B3B sans modifier leur état mécanique. Le checkpoint contient exactement les 24 exigences `HUMAN_REVIEW` attendues : `P01`, `P06`, `P07`, `P28`, `P33`, `P34`, `P35`, `M06`, `S01`, `S03`, `S04`, `S05`, `S07`, `S10`, `S13`, `S14`, `S15`, `S16`, `S19`, `S20`, `S21`, `S22`, `S27`, `S29`.

Sources principales :

- matrice d'exigences TECH6B3A : 79 lignes, dont 24 `HUMAN_REVIEW` ;
- matrice vanilla 1.13.11 : 794 lignes, SHA-256 `96a9984de0e1b711e61bf252006dbbacb3bf9008c609362fdcfcd369d71162a8` ;
- matrice du mod principal Steam : 647 lignes, SHA-256 `d83ffb54e9e42b4654411d6288943872eacbb92f9fbe4b217c19ebcc70445255` ;
- installation canonique vérifiée sous `C:/Games/Victoria 3/game` ;
- ancienne copie locale du mod principal utilisée comme troisième point de comparaison lorsque l'objet était présent.

## B. État Git

La branche `tech6b3c-tree-human-review` a été créée depuis l'état de travail non validé de TECH6B3B. Le checkpoint comportait déjà 23 fichiers suivis modifiés ainsi que les nouveaux fichiers non suivis des phases TECH6B1 à TECH6B3B. Ils ont été préservés tels quels.

Les seuls livrables ajoutés par TECH6B3C sont :

- `docs/reports/technology/TECH6B3C_TREE_HUMAN_REVIEW_MATRIX.csv` ;
- `docs/reports/technology/TECH6B3C_TREE_HUMAN_REVIEW_REPORT.md`.

Aucun commit, push, stash, reset ou nettoyage de changements antérieurs n'a été effectué.

## C. Méthode

Chaque ligne a été traitée selon la même séquence : vérification de l'objet actuel, du propriétaire effectif de l'unlock, de l'ère et des parents ; comparaison avec vanilla 1.13.11 et le mod principal ; construction d'alternatives ; évaluation historique, gameplay et topologique ; identification des dépendances ; décision de confiance et besoin éventuel d'un choix utilisateur.

Une recommandation `HIGH` est dominante au regard des fichiers et de la topologie. Une recommandation `MEDIUM` reste le meilleur compromis observé mais dépend d'une préférence de design ou d'un équilibrage futur. Aucun point n'est resté sans recommandation exploitable.

Règles de sûreté appliquées : aucun ID futur n'est figé sans objet existant, aucun chemin futur n'est prétendu existant, et aucun objet gameplay n'a été édité.

## D. Inventaire exact des 24 décisions

| ID | Domaine | Décision recommandée | Confiance | Choix utilisateur |
|---|---|---|---|---|
| P01 | Production | déplacer le premier plafond d'économie d'échelle `+10` vers `interchangeable_manufacture` | HIGH | non |
| P06 | Production | ne pas créer Electric Sewing ; conserver `electrical_capacitors` | HIGH | non |
| P07 | Production | conserver le gate actuel de `pm_electric_sewing_machines` | HIGH | non |
| P28 | Production | conserver l'ère et le parent de `cotton_gin` | HIGH | non |
| P33 | Production | renommer Steel-Frame Buildings seulement avec la future chaîne béton | HIGH | non |
| P34 | Production | préparer 30 béton et réduire le verre à 20 dans `pm_steel_frame_buildings` | MEDIUM | oui |
| P35 | Production | faire consommer 40 béton au PM arc-welded, sans aucune arête technologique inter-catégorie | MEDIUM | oui |
| M06 | Military | gater `pm_percussion_caps` par `percussion_cap` | HIGH | non |
| S01 | Society | progression Human Rights → mobilisation abolitionniste → loi | HIGH | non |
| S03 | Society | répartir les responsabilités de `commercial_insurance_markets` | MEDIUM | oui |
| S04 | Society | gater Laissez-Faire par `joint_stock_companies` | MEDIUM | oui |
| S05 | Society | gater réellement Interventionism par `classical_political_economy` | HIGH | non |
| S07 | Society | ajouter `country_tech_spread_mult = 0.05` | MEDIUM | oui |
| S10 | Society | gater Total Separation par `liberal_constitutionalism` | HIGH | non |
| S13 | Society | ajouter `country_weekly_innovation_max_add = 5` | MEDIUM | oui |
| S14 | Society | préparer un PM universitaire intermédiaire Professional Faculties | MEDIUM | oui |
| S15 | Society | conserver Analytical Philosophy Department à `analytical_philosophy` | HIGH | non |
| S16 | Society | conserver `medical_degrees` et faire converger la branche à Vaccination | MEDIUM | oui |
| S19 | Society | donner deux parents à Vaccination | MEDIUM | oui |
| S20 | Society | faire converger Vaccination et Active Principle Pharmacy à Organized Immunization | HIGH | non |
| S21 | Society | ajouter Professional Civil Policing comme parent d'Identification Documents | HIGH | non |
| S22 | Society | ne pas ajouter d'arête directe redondante plus tard dans la chaîne policière | HIGH | non |
| S27 | Society | rendre `joint_stock_companies` recherchable en ère 6 | HIGH | non |
| S29 | Society | faire hériter Investment Banks de Joint Stock via Mutual Funds | HIGH | non |

Total : 24 analysées ; 15 HIGH ; 9 MEDIUM ; 0 LOW ; 9 décisions utilisateur.

## E. Recommandations Production

### Économie d'échelle

Le `+10` est actuellement porté par `mechanized_workshops`, alias caché avec `can_research = no`. Le déplacer vers `interchangeable_manufacture` en ère 6 crée un premier palier visible avant le `+20` de `shift_work` en ère 8. `mechanical_tools` en ère 5 serait trop précoce.

### Textile et Electric Sewing

`industrial_spinning` n'existe pas comme ID. « Industrial Spinning » correspond à l'objet exact `advanced_spinning`. Cette anomalie d'entrée ne doit pas devenir un nouvel ID. `pm_electric_sewing_machines` est déjà gaté par `electrical_capacitors` en ère 9, dont la topologie réunit électricité et textile mécanisé. Aucun nouveau nœud Electric Sewing n'est justifié.

### Cotton Gin

`cotton_gin`, en ère 4 après `mechanized_spinning`, est cohérent avec l'invention de 1793–1794 et avec la nouvelle responsabilité des compagnies cotonnières. Aucun déplacement n'est requis.

### Préparation du béton — sans implémentation

La décision utilisateur est explicite : **le béton sera implémenté plus tard ; TECH6B3C prépare cette implémentation**. Le mod et vanilla ne possèdent actuellement aucun bien Concrete. Le cahier futur doit donc prévoir :

- un concept de bien Concrete ;
- un concept de bâtiment Cement Works ;
- un PM de production initial gaté par `hydraulic_cements` ;
- un PM de production amélioré gaté par `reinforced_concrete` ;
- une branche Production autonome `hydraulic_cements -> reinforced_concrete`, avec l'éventuelle arête Production `reinforced_concrete -> arc_welding` différée à la phase béton ;
- le maintien de `electric_arc_process` comme parent Production de `arc_welding` ;
- une branche Society autonome pour `steel_frame_buildings`, qui conserve uniquement des parents Society ;
- le renommage d'affichage de `steel_frame_buildings` en « Concrete and Steel Buildings » uniquement lors de la livraison coordonnée ;
- des valeurs provisoires, à simuler : steel-frame consomme 30 béton avec verre réduit de 40 à 20 ; arc-welded consomme 40 béton avec verre réduit de 40 à 20.

Une technologie ne peut pas consommer un bien : le consommateur tardif valide est `pm_arc_welded_buildings`. Surtout, Victoria 3 n'autorise pas les prérequis entre catégories technologiques : `steel_frame_buildings` est Society alors que `reinforced_concrete` et `arc_welding` sont Production. Aucune arête ne doit donc entrer dans `steel_frame_buildings` depuis Production, ni l'utiliser comme gate d'une technologie Production. Le lien futur entre les deux branches passe uniquement par les gates et inputs des PM de construction.

## F. Recommandations Military

`pm_percussion_caps` est disponible sans gate alors qu'il utilise plomb et explosifs. Le gate exact est `percussion_cap` en ère 6. `dynamite` doit rester le gate du successeur `pm_explosive_shells`. Cette solution produit une progression lisible sans nouvel objet militaire.

## G. Recommandations Society

- `law_interventionism` : remplacer le gate effectif caché `manufacturies` par `classical_political_economy` ; conserver la vérification AI déjà alignée sur ce nœud.
- `law_total_separation` : remplacer le gate très précoce par `liberal_constitutionalism` en ère 6.
- `commercial_insurance_markets` : conserver les responsabilités commerciales précoces ; déplacer les institutions libérales mûres vers `classical_political_economy`.
- `law_laissez_faire` : le meilleur propriétaire est le futur nœud recherchable `joint_stock_companies` en ère 6.
- Diffusion, innovation, universités, médecine, police, abolition et finance sont détaillées ci-dessous.

## H. Diffusion

Le moteur calcule une base de diffusion à partir de `25 + 75 × literacy + 0.2 × excess innovation`, puis applique les multiplicateurs pays. `TECH_SPREAD_RANDOM_RANGE = 0.5` ajoute une variation moteur ; aucune modification de define n'est nécessaire.

| Élément | Spécification proposée |
|---|---|
| propriétaire | `institutionalized_scientific_exchange` |
| effet exact | `country_tech_spread_mult = 0.05` |
| portée | toutes les branches de technologie |
| intention | bonus global conservateur de +5 % |
| risque | faible à moyen, cumul à tester avec literacy et excess innovation |

## I. Innovation

Le plafond observé suit `50 + 150 × literacy + additions`. Les départements universitaires produisent actuellement +1, +1.5 et +2 innovation par niveau. L'effet exact recommandé est `country_weekly_innovation_max_add = 5` sur `experimental_research_laboratories`.

Ce bonus absorbe environ cinq niveaux Scholastic, 3,33 niveaux Philosophy ou 2,5 niveaux Analytical à plein emploi. Il est assez visible pour soutenir la spécialisation scientifique sans neutraliser le plafond lié à l'alphabétisation. La valeur reste soumise à décision utilisateur.

## J. Universités

| PM | Gate recommandé | Innovation | Rôle |
|---|---|---:|---|
| Scholastic | existant | +1 | base ancienne |
| Philosophy Department | `polytechnical_education` selon S11 mécanique | +1.5 | transition technique |
| Professional Faculties, nouveau concept | `specialized_professional_societies` | +1.75 provisoire | palier professionnel intermédiaire, papier et outils |
| Analytical Philosophy Department | `analytical_philosophy` | +2 | sommet analytique tardif |

Un seul nouveau PM est recommandé, dans le groupe existant `pmg_base_building_university`. Aucun nouveau groupe de PM n'est requis. S12 doit être invalidé : déplacer le PM Analytical vers `experimental_research_laboratories` écraserait la progression et rendrait `analytical_philosophy` moins utile.

## K. Topologie médicale

Topologie figée proposée :

```text
variolation_networks ─┐
                     ├─> vaccination ───────────────┐
medical_degrees ─────┘                              ├─> organized_immunization_campaigns
medical_degrees ─┬─> clinicopathological_analysis   │
                 └─> active_principle_pharmacy ─────┘
experimental_research_laboratories est conservé comme parent existant
de clinicopathological_analysis et active_principle_pharmacy.
```

`medical_degrees` reste inchangé. Vaccination reçoit `variolation_networks` et `medical_degrees`. Clinicopathological Analysis et Active Principle Pharmacy restent des branches parallèles ; imposer Pharmacy après Clinicopathology n'est plus requis. La convergence finale a lieu à Organized Immunization, avec Vaccination et Active Principle Pharmacy comme parents.

## L. Topologie policière

`professional_civil_policing`, en ère 6, doit devenir un parent additionnel de `identification_documents`, tout en préservant `central_statistical_offices`. `central_planning` hérite ensuite de cette exigence par Identification Documents, puis `mass_surveillance` par Central Planning.

```text
professional_civil_policing ─┐
central_statistical_offices ─┴─> identification_documents
                                 -> central_planning
                                 -> mass_surveillance
```

Une arête directe depuis Professional Civil Policing vers Central Planning ou Mass Surveillance serait redondante. Les gates de lois Local Police et Dedicated Police déjà portés mécaniquement sont conservés.

## M. Human Rights / Abolition

`human_rights` est un véritable nœud d'ère 4, pas un alias. La séparation conceptuelle recommandée est :

```text
constitutional_government
  -> human_rights
  -> organized_reform_movements
  -> abolitionist_mobilization
  -> autorise law_slavery_banned
```

L'arête directe actuellement redondante de `human_rights` vers `abolitionist_mobilization` peut être supprimée, car l'héritage passe par Organized Reform Movements. Dans vanilla 1.13.11, `law_slavery_banned` n'a pas d'`unlocking_technologies`; Human Rights sert seulement dans la pondération AI. La future implémentation devra donc créer un shadow du fichier vanilla existant `common/laws/02_slavery.txt`, sans gater les lois esclavagistes régressives.

## N. `joint_stock_companies`

Le nœud caché `joint_stock_companies` doit redevenir une technologie recherchable en ère 6, avec les parents revus par S26 : `postal_savings` et `commercial_insurance_markets`. Il devient le propriétaire naturel de Laissez-Faire et prépare Mutual Funds.

Chaîne recommandée :

```text
postal_savings ───────────────┐
commercial_insurance_markets ─┴─> joint_stock_companies
institutional_public_credit ─────> mutual_funds
joint_stock_companies ───────────> mutual_funds
stock_exchange ──────────────────> investment_banks
mutual_funds ────────────────────> investment_banks
```

Investment Banks hérite ainsi de Joint Stock Companies via Mutual Funds ; une arête directe supplémentaire n'est pas nécessaire. Les déplacements mécaniques prévus de capacité de compagnie depuis `stock_exchange` restent cohérents avec cette restauration.

## O. Dépendances entre décisions

| Groupe | Dépendances | Résultat coordonné |
|---|---|---|
| Electric Sewing | P06 ↔ P07, correction P05 | aucun nouveau nœud ; utiliser `advanced_spinning` lorsque P05 cite le textile |
| béton | P31, P32, P33, P34, P35 | branches Production/Society séparées, valeurs provisoires, implémentation différée |
| assurance et lois | S02, S03, S04, S05 | responsabilités réparties entre Commercial Insurance, Classical Political Economy et Joint Stock |
| universités | S11, S12, S13, S14, S15 | palier intermédiaire nouveau ; sommet Analytical conservé tardif |
| médecine | S16 à S20 | deux branches parallèles, convergence à Organized Immunization |
| police | S21, S22 | une seule nouvelle arête à Identification Documents |
| joint-stock | S23 à S30 | nœud recherchable, Mutual Funds comme relais vers Investment Banks |

## P. Impact sur les 53 candidats mécaniques

La base TECH6B3A contient 53 candidats mécaniques. La revue humaine en affecte exactement cinq :

| Candidat | Impact de TECH6B3C |
|---|---|
| P05 | `TARGET_TECH_CHANGED` : remplacer le faux ID `industrial_spinning` par `advanced_spinning` |
| P31 | `DEFERRED_CONCRETE` : une éventuelle arête `reinforced_concrete -> arc_welding` reste dans Production et sera décidée avec la livraison béton |
| P32 | `SUPERSEDED_BY_ENGINE_CATEGORY_CONSTRAINT` : aucune arête n'est autorisée entre `steel_frame_buildings` (Society) et une technologie Production |
| S12 | `IMPLEMENTATION_NO_LONGER_REQUIRED` : Analytical Philosophy Department reste à `analytical_philosophy` |
| S18 | `IMPLEMENTATION_NO_LONGER_REQUIRED` : Active Principle Pharmacy reste parallèle à Clinicopathology |

Les 48 autres candidats ne sont pas modifiés par les arbitrages TECH6B3C. Aucun candidat mécanique supplémentaire n'a été créé.

## Q. Nouveaux objets éventuellement requis

| Type | Concept | Statut TECH6B3C |
|---|---|---|
| technologie | aucun | 0 recommandé |
| PM | Professional Faculties | concept préparé, ID final non inventé |
| PM | production initiale de béton | concept préparé, ID final non inventé |
| PM | production améliorée de béton | concept préparé, ID final non inventé |
| autre | bien Concrete | concept préparé, ID final non inventé |
| autre | bâtiment Cement Works | concept préparé, ID final non inventé |

Les chemins de définition futurs du béton restent volontairement non résolus. Ils devront être choisis seulement pendant la phase d'implémentation, après inventaire des conventions du dépôt.

## R. Décisions à soumettre réellement à l'utilisateur

Les neuf choix restants sont : `P34`, `P35`, `S03`, `S04`, `S07`, `S13`, `S14`, `S16`, `S19`. Ils ont tous une recommandation MEDIUM et figurent sous une forme directement répondable dans le User Decision Packet.

Les 15 décisions HIGH peuvent être intégrées au prochain cahier mécanique sans nouvelle consultation, sous réserve de l'acceptation globale du cahier figé.

## S. Proposition de cahier figé

Si les neuf recommandations MEDIUM sont acceptées, le prochain cahier mécanique est :

1. appliquer P01 et M06 avec les IDs existants ;
2. supprimer le faux besoin Electric Sewing et corriger la référence P05 vers `advanced_spinning` ;
3. préserver Cotton Gin ;
4. préparer séparément la livraison béton avec des branches technologiques par catégorie, sans l'inclure avant que bien, bâtiment, PM, localisation et équilibrage soient tous prêts ;
5. appliquer la progression abolitionniste et les gates de lois validés ;
6. répartir Commercial Insurance et restaurer Joint Stock Companies comme nœud d'ère 6 ;
7. appliquer le bonus de diffusion +5 % et le plafond d'innovation +5 ;
8. ajouter Professional Faculties tout en conservant Analytical Philosophy tardif ;
9. appliquer les topologies médicales et policières décrites ci-dessus ;
10. faire précéder tout changement économique du béton d'une simulation de prix, throughput et coût de construction.

Ce cahier ne crée aucune nouvelle technologie. Il prépare trois concepts de PM et deux concepts d'autres objets. Les IDs et chemins futurs restent à définir au moment approprié.

## T. Vérification du non-scope

Checkpoint gameplay initial du fork : 970 fichiers, agrégat SHA-256 `23756b95cf9302718563622b61c17ce0a0756495deb918877b1a65b6035cedb5`.  
Checkpoint initial de l'ancienne copie locale du mod principal : 842 fichiers, agrégat SHA-256 `d1fd931b4afe7229057069e7fc7241ba6b92aa925966e2f883544b4133ad2f9b`.  
Source Steam autoritaire, restée en lecture seule : 909 fichiers, agrégat SHA-256 `d7a89af3f1943148740ef12dbf14531dac292647abc9720b5f141e955c7a1d78`.

La validation finale recalcule les empreintes. Les seules écritures TECH6B3C dans le fork se trouvent sous `docs/reports/technology`. Après clôture de l'audit, la maintenance séparément demandée par l'utilisateur a synchronisé `1776_Age_of_Revolutions_hotfix_source` depuis le workshop `3617930953` : la copie contient désormais 909 fichiers et le même agrégat `d7a89af3f1943148740ef12dbf14531dac292647abc9720b5f141e955c7a1d78`, en version 2.3.1 pour Victoria 3 1.13.11. Le miroir a supprimé 11 fichiers obsolètes absents de la source actuelle ; un dry-run ne relève désormais plus aucune différence. Cette synchronisation n'a écrit ni dans le fork ni dans le workshop Steam. Par conséquent :

- `GAMEPLAY_FILES_CHANGED = 0` ;
- `TREE_CORRECTION_IMPLEMENTED = 0` ;
- `STEAM_FILES_CHANGED = 0` ;
- `STARTING_TECH_FILES_CHANGED = 0` ;
- `UNKNOWN_TECH_IDS = 0` ;
- `INVENTED_OBJECT_IDS = 0` ;
- `INVENTED_FILE_PATHS = 0` ;
- runtime non requis ; commit non ; push non.

## USER DECISION PACKET

### P34

PROBLEM = Le futur input béton de `pm_steel_frame_buildings` n'a ni quantité ni substitution validées.  
RECOMMENDATION = 30 béton et verre réduit de 40 à 20, valeurs provisoires soumises à simulation.  
WHY = Le nouveau bien devient significatif sans ajouter tout son coût au PM actuel.  
ALTERNATIVE = Ajouter le béton sans réduire le verre, ou différer tous les chiffres.  
CONSEQUENCE_OF_RECOMMENDATION = Coût partiellement substitué et chaîne prête à tester.  
CONSEQUENCE_OF_ALTERNATIVE = Risque d'inflation excessive de la construction, ou cahier incomplet.  
CODEX_CONFIDENCE = MEDIUM

### P35

PROBLEM = `arc_welding` ne peut pas consommer un bien ; le consommateur et la topologie doivent être choisis.  
RECOMMENDATION = 40 béton et verre réduit à 20 dans `pm_arc_welded_buildings`; aucune arête entre `steel_frame_buildings` (Society) et `arc_welding` (Production).  
WHY = Le PM est le bon objet économique et les catégories technologiques doivent rester isolées.  
ALTERNATIVE = Conserver le PM sans béton, ou créer un PM supplémentaire.  
CONSEQUENCE_OF_RECOMMENDATION = Sink tardif de béton sans prérequis inter-catégorie invalide.  
CONSEQUENCE_OF_ALTERNATIVE = Béton moins utile, ou granularité et maintenance accrues.  
CODEX_CONFIDENCE = MEDIUM

### S03

PROBLEM = `commercial_insurance_markets` possède trop d'unlocks commerciaux, légaux et diplomatiques dès l'ère 1.  
RECOMMENDATION = Conserver mercantilisme, Navigation Acts, embargo, Goods Transfer, market prohibition et `je_liberalism`; déplacer Free Trade, No Tariffs et No Subventions vers `classical_political_economy`; traiter Laissez-Faire sous S04.  
WHY = La séparation suit la maturité institutionnelle sans vider le nœud précoce.  
ALTERNATIVE = Tout conserver ou tout déplacer.  
CONSEQUENCE_OF_RECOMMENDATION = Progression graduelle et nœuds tous utiles.  
CONSEQUENCE_OF_ALTERNATIVE = Unlocks libéraux trop précoces ou technologie d'ère 1 vidée.  
CODEX_CONFIDENCE = MEDIUM

### S04

PROBLEM = Laissez-Faire est une loi puissante actuellement gatée par un nœud d'ère 1.  
RECOMMENDATION = La gater par `joint_stock_companies`, rendu recherchable en ère 6.  
WHY = Les sociétés par actions fournissent la base institutionnelle pratique de la capitalisation privée.  
ALTERNATIVE = `classical_political_economy` plus tôt, ou `investment_banks` beaucoup plus tard.  
CONSEQUENCE_OF_RECOMMENDATION = Loi retardée mais disponible avant Mutual Funds et Investment Banks.  
CONSEQUENCE_OF_ALTERNATIVE = Loi encore précoce, ou délai potentiellement frustrant.  
CODEX_CONFIDENCE = MEDIUM

### S07

PROBLEM = Le rôle exact de Scientific Exchange dans la diffusion n'était pas quantifié.  
RECOMMENDATION = `country_tech_spread_mult = 0.05` sur `institutionalized_scientific_exchange`.  
WHY = Bonus global modeste, compatible avec la formule literacy/excess innovation.  
ALTERNATIVE = +10 %, bonus ciblé, ou aucun effet.  
CONSEQUENCE_OF_RECOMMENDATION = Diffusion légèrement accélérée pour tous les pays ayant le nœud.  
CONSEQUENCE_OF_ALTERNATIVE = Effet plus visible mais risque de compression, ou nœud moins distinctif.  
CODEX_CONFIDENCE = MEDIUM

### S13

PROBLEM = Experimental Research Laboratories doit relever le plafond d'innovation sans neutraliser l'alphabétisation.  
RECOMMENDATION = `country_weekly_innovation_max_add = 5`.  
WHY = Valeur visible correspondant à 2,5–5 niveaux universitaires selon le PM.  
ALTERNATIVE = +3 prudent ou +10 affirmé.  
CONSEQUENCE_OF_RECOMMENDATION = Spécialisation scientifique utile mais bornée.  
CONSEQUENCE_OF_ALTERNATIVE = Bonus presque imperceptible ou forte accélération de recherche.  
CODEX_CONFIDENCE = MEDIUM

### S14

PROBLEM = Un palier manque entre Philosophy et Analytical sans justification pour un nouveau groupe de PM.  
RECOMMENDATION = Un PM Professional Faculties dans `pmg_base_building_university`, gaté par `specialized_professional_societies`, avec papier, outils et +1.75 innovation provisoire.  
WHY = Le palier représente la professionnalisation universitaire et préserve le sommet analytique tardif.  
ALTERNATIVE = Aucun nouveau PM, ou déplacement du PM Analytical existant.  
CONSEQUENCE_OF_RECOMMENDATION = Progression à quatre paliers et coûts matériels plus riches.  
CONSEQUENCE_OF_ALTERNATIVE = Saut plus abrupt ou perte de valeur d'Analytical Philosophy.  
CODEX_CONFIDENCE = MEDIUM

### S16

PROBLEM = La place de `medical_degrees` entre institutionnalisation, vaccination et médecine expérimentale était ambiguë.  
RECOMMENDATION = Conserver le nœud où il est et faire converger la branche à Vaccination.  
WHY = Les diplômes médicaux structurent la profession sans devoir devenir l'unique tronc de toutes les découvertes.  
ALTERNATIVE = Déplacer Medical Degrees ou en faire le parent direct de toutes les branches.  
CONSEQUENCE_OF_RECOMMENDATION = Topologie lisible avec branches parallèles.  
CONSEQUENCE_OF_ALTERNATIVE = Chaîne trop linéaire et plusieurs nœuds moins autonomes.  
CODEX_CONFIDENCE = MEDIUM

### S19

PROBLEM = Vaccination ne dépend actuellement que de la tradition de variolisation.  
RECOMMENDATION = Parents `variolation_networks` et `medical_degrees`.  
WHY = La découverte exige à la fois l'antécédent pratique et une profession médicale organisée.  
ALTERNATIVE = Conserver seulement Variolation Networks.  
CONSEQUENCE_OF_RECOMMENDATION = Convergence historique plus riche et Medical Degrees reste utile.  
CONSEQUENCE_OF_ALTERNATIVE = Progression plus simple et plus rapide, mais branche institutionnelle déconnectée.  
CODEX_CONFIDENCE = MEDIUM

## Sortie terminale attendue

```text
TECH6B3C_TREE_HUMAN_REVIEW = PASS
BRANCH = tech6b3c-tree-human-review
HUMAN_REVIEW_REQUIREMENTS_EXPECTED = 24
HUMAN_REVIEW_REQUIREMENTS_ANALYZED = 24
HIGH_CONFIDENCE_RECOMMENDATIONS = 15
MEDIUM_CONFIDENCE_RECOMMENDATIONS = 9
LOW_CONFIDENCE_RECOMMENDATIONS = 0
USER_DECISIONS_STILL_REQUIRED = 9
NEW_TECH_CONCEPTS_RECOMMENDED = 0
NEW_PM_CONCEPTS_RECOMMENDED = 3
NEW_OTHER_OBJECT_CONCEPTS_RECOMMENDED = 2
IMPLEMENTATION_CANDIDATES_BASELINE = 53
IMPLEMENTATION_CANDIDATES_AFFECTED_BY_HUMAN_REVIEW = 5
GAMEPLAY_FILES_CHANGED = 0
TREE_CORRECTION_IMPLEMENTED = 0
STEAM_FILES_CHANGED = 0
STARTING_TECH_FILES_CHANGED = 0
UNKNOWN_TECH_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0
RUNTIME = NOT_REQUIRED
COMMIT = NO
PUSH = NO
MATRIX = docs/reports/technology/TECH6B3C_TREE_HUMAN_REVIEW_MATRIX.csv
REPORT = docs/reports/technology/TECH6B3C_TREE_HUMAN_REVIEW_REPORT.md
NEXT_PHASE_READY = NO
```

`NEXT_PHASE_READY = NO` signifie uniquement que les neuf choix du paquet doivent être acceptés ou amendés avant toute phase mécanique. Le rapport documentaire TECH6B3C est, lui, complet.
