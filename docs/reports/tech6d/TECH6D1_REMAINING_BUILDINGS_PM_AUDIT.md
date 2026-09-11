# TECH6D1 — Audit des bâtiments et méthodes de production restants

Date de l'audit : 11 septembre 2026  
Branche observée : `tech6c-goods-buildings-pm-implementation`  
Référence vanilla : Victoria 3 1.13.11, `C:/Games/Victoria 3/game`

## Conclusion exécutive

L'architecture locale issue de TECH6C couvre tous les besoins de bâtiments de l'ancienne étude. Aucun nouveau bâtiment n'est encore requis, et aucun ne doit être ajouté avant la bêta. Sur les 24 candidats de méthodes de production, 10 sont pleinement couverts, 8 sont partiellement couverts, 5 sont réellement absents et 1 est différé par décision de conception.

Le principal vide structurel est la sidérurgie initiale : `coke_smelting` ne mène à aucun PM sidérurgique sélectionnable et `puddling_and_rolling` ne sert que de verrou au bâtiment, dont le PM de base reste `pm_blister_steel_process`. En revanche, la progression Bessemer → foyer ouvert → arc électrique est déjà valide. Le prochain bloc conseillé est donc **P01 + P02 + P03**, sans nouveau bien ni nouveau bâtiment.

La pharmacie dans `building_chemical_works`, la précision dans `building_tooling_workshop`, la séparation engrais/chimie industrielle, la mine de cuivre autonome et l'aluminium sans bauxite/alumine sont des choix actuels valides. L'ancien document de recherche ne doit pas les rouvrir.

### Méthode et niveau de preuve

La copie locale est prioritaire. Une méthode n'est considérée accessible que si la chaîne **PM → PMG → bâtiment** est démontrée et si tous ses identifiants technologiques existent. La vanilla 1.13.11 n'est utilisée que lorsque le fork hérite un PMG sans le redéfinir, notamment pour la réfrigération et le raffinage du sucre. La localisation seule n'a jamais servi de preuve.

## Statut des bâtiments

| ID | Candidat ancien | Statut actuel | Architecture effective | Couverture | Décision |
|---|---|---|---|---:|---|
| B01 | Cement Works | `IMPLEMENTED_AS_ORIGINALLY_PROPOSED` | `building_cement_works` → `pmg_base_building_cement_works` → trois procédés cimentiers | 100 % | Conserver. |
| B02 | Oil Refinery | `IMPLEMENTED_AS_ORIGINALLY_PROPOSED` | `building_oil_refinery` → `pmg_base_building_oil_refinery` → distillation fractionnée | 100 % | Conserver ; P15 est un manque de PM, pas de bâtiment. |
| B03 | Non-Ferrous Metallurgy Works | `IMPLEMENTED_WITH_DIFFERENT_ARCHITECTURE` | `building_non_ferrous_metallurgy_works` produit l'aluminium ; le cuivre vient d'une mine séparée | 80 % | Conserver. Les alliages restent une décision distincte. |
| B04 | Pharmaceutical Laboratories | `FUNCTION_ABSORBED_BY_EXISTING_BUILDING` | PMG secondaire pharmaceutique dans `building_chemical_works` | 100 % | Ne pas créer de laboratoire autonome. |
| B05 | Precision Engineering Works | `FUNCTION_ABSORBED_BY_EXISTING_BUILDING` | PMG de précision dans `building_tooling_workshop` | 100 % | Ne pas créer d'usine séparée. |
| B06 | Copper and Alloy Mine | `IMPLEMENTED_WITH_DIFFERENT_ARCHITECTURE` | `building_copper_mine` couvre extraction, pompage, explosifs, transport et concentration | 90 % | Conserver ; l'absence d'« alloy metals » est volontaire. |
| B07 | Fertilizer and Alkali Works | `IMPLEMENTED_WITH_DIFFERENT_ARCHITECTURE` | engrais dans `building_chemical_plant`, chimie industrielle dans `building_chemical_works` | 100 % | Conserver la séparation. |
| B08 | Cold Storage Network | `EXISTING_VANILLA_SYSTEM_SUFFICIENT` | PMG de réfrigération sur élevage, pêche et chasse à la baleine | 90 % | `REJECT` pour le bâtiment autonome ; compléter seulement P16. |

Bilan des huit bâtiments : 2 implémentés comme proposés, 3 implémentés avec une architecture différente, 2 fonctions absorbées et 1 besoin couvert par le système vanilla. Aucun candidat n'est `STILL_MISSING`.

## Statut détaillé des PM

La colonne « effets actuels » décrit les recettes et emplois présents, pas une proposition d'équilibrage. « Requis » désigne `required_input_goods` lorsqu'il existe.

| ID | Objet historique | Représentation effective, chemin et verrou | Effets actuels pertinents | Accessibilité, écart et recommandation |
|---|---|---|---|
| P01 | Passage du charbon de bois au coke | Aucun PM dans `pmg_steelmaking_process`. La technologie `coke_smelting` existe. | Aucun input, output, emploi ou modificateur de PM. | Non sélectionnable. Vide réel : la technologie ne crée pas de stade sidérurgique. `ADD_PM`, priorité haute. |
| P02 | Puddlage et laminage, pont 1784–Bessemer | `building_steel_mill`, verrouillé par `puddling_and_rolling`, sélectionne par défaut `pm_blister_steel_process`. | Fer 40 + charbon 30 → acier 65 ; 500 boutiquiers, 3 500 ouvriers, 750 machinistes, 250 ingénieurs ; pollution +10. | Sélectionnable, mais seulement sous une identité « blister ». Couverture 75 %. `MINOR_REVISION` pour rendre le PM explicitement puddlage/laminage. |
| P03 | Convertisseur basique Thomas et scories phosphatées | `pm_bessemer_process` dans `pmg_steelmaking_process`, verrou `bessemer_process`. | Fer 60 + charbon 30 → acier 90 ; 500/3 000/1 000/500 emplois ; pollution +15. | Le Bessemer générique est accessible ; la variante calcaire et le coproduit engrais manquent. Couverture 55 %. `ADD_PM` alternatif. |
| P04 | Foyer ouvert, flexibilité et recyclage | `pm_open_hearth_process` → `pmg_steelmaking_process` → `building_steel_mill`, verrou `open_hearth_process`. | Fer 90 + charbon 30 → acier 120 ; 500/2 500/1 250/750 emplois ; pollution +20. | Accessible. Le rôle chronologique est couvert ; le recyclage explicite exigerait un bien ferraille absent et redondant pour ce seul usage. `NO_ACTION_EXISTING_VANILLA_SUFFICIENT`. |
| P05 | Aciers alliés | Seul `pm_electric_arc_process` est proche, verrou `electric_arc_process`. | Fer 100 + charbon 30 + électricité 30 → acier 150 ; 500/2 000/1 500/1 000 emplois ; pollution +25 ; électricité requise. | L'acier électrique est accessible, pas l'alliage. Aucun intrant d'alliage propre n'existe. Couverture 25 %. `DEFER` — **DESIGN DECISION REQUIRED**. |
| P06 | Pompage atmosphérique des mines | Variantes `pm_atmospheric_engine_pump_building_*` dans les PMG d'équipement de charbon, fer, plomb, soufre, or, cuivre, phosphate et sel ; verrou `atmospheric_engine`. | Exemple charbon : outils 10 → charbon 40 ; 500/3 750/500/250 emplois ; pollution +5. Les rendements varient par ressource. | Chaînes PM→PMG→bâtiment vérifiées. Le calcaire est correctement traité comme carrière. `NO_ACTION_EXISTING_VANILLA_SUFFICIENT`. |
| P07 | Ventilation mécanique et sécurité | Aucun PM/PMG de ventilation. Les PMG actuels couvrent pompage, explosifs, treuils, rail et concentration. | Aucun effet actuel. | Manque réel. `ADD_PMG` réutilisable sur les mines profondes. La contrepartie doit être énergie + machines + emplois qualifiés contre mortalité des employés ; pas un bonus gratuit de débit. |
| P08 | Flottation/concentration des minerais | Variantes `pm_ore_concentration_building_*` dans des PMG dédiés pour charbon, fer, plomb, soufre, or, cuivre et phosphate ; verrou `geological_surveying`. | En général outils 5 + produits chimiques industriels 5 → supplément de ressource propre ; pollution +5 ; pas de remplacement d'emplois. | Accessible partout où applicable. Le sel conserve sa purification et le calcaire son concassage. `NO_ACTION_ALREADY_IMPLEMENTED`. |
| P09 | Blanchiment au chlore | Textile : `pm_chemical_bleaching_textile_mill` dans `pmg_base_building_textile_mill`, verrou `chemical_bleaching`. Papier : `pm_bleached_paper` dans `pmg_base_building_paper_mill`, verrou `industrial_paper_bleaching`. | Textile : tissu 40 + teinture 5 + chimie 10 → vêtements 80, emplois 500/3 500/750/250, pollution +5. Papier : bois 30 + soufre 10 + teinture 10 + chimie 10 → papier 100, emplois 500/3 000/1 000/500, pollution +5. | Les deux sont accessibles et consomment bien `industrial_chemicals`. Le papier conserve toutefois les anciens intrants soufre/teinture. Couverture 85 %. `MINOR_REVISION` ciblée sur la recette papier ; ne pas toucher au textile. |
| P10 | Colorants synthétiques | `pm_dye_production` → `pmg_synthetic_dyes` → `building_synthetics_plant`. Le bâtiment est verrouillé par `aniline`. | Soufre 10 + produits pétroliers lourds 20 + sel 10 + chimie 30 → teinture 90 ; 500/1 000/1 500/2 000 emplois ; pollution +5. | Accessible par le verrou du bâtiment. Fonction entièrement couverte. `NO_ACTION_ALREADY_IMPLEMENTED`. |
| P11 | Procédé Solvay | `pm_solvay_process_building_chemical_works` → PMG de base → `building_chemical_works`, verrou `nitroglycerin`. | Sel 25 + calcaire 25 + charbon 10 + outils 5 → chimie industrielle 75 ; 500/2 000/1 500/1 000 emplois ; pollution +15. | Sélectionnable dans la séquence plomb/Leblanc/Solvay/électrolyse. L'ancien bâtiment combiné n'est plus pertinent. `NO_ACTION_ALREADY_IMPLEMENTED`. |
| P12 | Superphosphate | `pm_improved_fertilizer` → `pmg_fertilizer_production` → `building_chemical_plant`, verrou `improved_fertilizer`. | Calcaire 30 + phosphates 20 + chimie 20 + charbon 10 → engrais 120 ; 500/2 000/1 500/1 000 emplois ; pollution +15. | Fonction complète et sélectionnable. `NO_ACTION_ALREADY_IMPLEMENTED`. |
| P13 | Haber-Bosch / fixation azotée | `pm_nitrogen_fixation` dans le même PMG, verrou `nitrogen_fixation`. | Calcaire 20 + chimie 20 + charbon 15 + fer 5 + phosphates 15 → engrais 200 ; 500/1 000/2 000/1 500 emplois ; pollution +15. | Fonction complète selon l'abstraction actuelle ; les nitrates restent différés. `NO_ACTION_ALREADY_IMPLEMENTED`. |
| P14 | Raffinage fractionné | `pm_fractional_distillation_refinery` → `pmg_base_building_oil_refinery` → `building_oil_refinery`, verrou `fractional_distillation`. | Pétrole 30 + charbon 5 + outils 5 → carburants raffinés 22 + lubrifiants 6 + produits lourds 16 ; 500/2 500/1 500/500 emplois ; pollution +20. | Accessible et validé. `NO_ACTION_ALREADY_IMPLEMENTED`. |
| P15 | Craquage thermique/catalytique | Aucun second PM dans le PMG de raffinerie. Les technologies existantes les plus proches sont `plastics` et `compression_ignition`. | Aucun effet actuel. | Manque réel. `ADD_PM` unique et agrégé, verrouillé de préférence par `plastics`. Il doit déplacer la part des produits lourds vers les carburants avec chimie et électricité, pas augmenter gratuitement tous les outputs. |
| P16 | Réfrigération à compression mécanique | Les PMG de réfrigération existent, mais passent directement de `pm_unrefrigerated` aux PM électriques. | Les PM électriques actuels consomment 1 ou 5 électricité et retirent 500 à 1 000 ouvriers selon le bâtiment. | Couverture 45 %. `ADD_PM` intermédiaire dans les trois PMG existants, verrou `high_pressure_steam`, consommant moteurs + charbon. Aucun bâtiment ou technologie dédié nécessaire. |
| P17 | Chaîne du froid électrique | Stockage réfrigéré, wagons frigorifiques et surgélation existent sur élevage, pêche et chasse à la baleine ; verrous `pasteurization`, `electric_railway`, `flash_freezing`. | Électricité requise ; les wagons ajoutent transport ; réduction de 500 à 3 000 ouvriers ; la pêche/baleine ajoute de la pollution sur les wagons. | Les intrants transport représentent la liaison ferroviaire. Ajouter aussi des PM au port/rail ferait doublon. `NO_ACTION_EXISTING_VANILLA_SUFFICIENT`. |
| P18 | Minoterie à cylindres | `automated_flour_milling` existe en ère 4 mais ne verrouille aucun PM. `pm_automated_bakery`, dans le PMG d'automatisation alimentaire, n'arrive qu'avec `dough_rollers` en ère 12. | PM actuel : outils 10, −2 500 ouvriers, aucun gain d'output direct. | Couverture 35 %. `ADD_PM` intermédiaire utilisant moteurs/outils et remplaçant du travail, sans bien farine. |
| P19 | Raffinage du sucre sous vide | `vacuum_pan_sugar` et `steam_powered_evaporation_sugar` → `pmg_refinement_building_sugar_plantation` → plantation sucrière. | Vide : charbon 1 → sucre +5, −1 000 ouvriers. Évaporation : moteurs 1 + charbon 2 → sucre +15, −2 000 ouvriers +500 machinistes. | Verrous `high_pressure_steam`/`sugar_refining`, puis `watertube_boiler`/`sugar_refining`. Fonction complète. `NO_ACTION_EXISTING_VANILLA_SUFFICIENT`. |
| P20 | Entraînement électrique unitaire | Représentation fragmentée : `pm_electric_sewing_machines`, `pm_automatic_power_looms` et PM d'assemblage électriques. Plusieurs PMG vapeur n'ont pas d'étape moteur électrique. | Exemples textile : électricité 10, outils et intrants textiles ; output ou forte économie de travail ; électricité requise. | Couverture 45 %. `ADD_PM` uniquement dans une courte liste de PMG d'automatisation existants ; ne pas ajouter un PMG mondial cumulable qui doublerait l'automatisation. |
| P21 | Organisation scientifique du travail | Aucun PM. `corporate_management` et `shift_work` existent comme verrous possibles. | Aucun input/output/emploi actuel. | Manque réel. `ADD_PMG` organisationnel : papier + services, davantage de commis/ingénieurs, avantage productif limité et non gratuit. À implémenter après P22. |
| P22 | Chaîne de montage mobile | Six PM `pm_assembly_lines_building_*` dans les PMG d'automatisation du meuble, outillage, moteurs, automobiles, armes/artillerie et munitions ; verrou `conveyors`. | Tous consomment lubrifiants 4 + électricité 5 ; certains outils 5 ; réduction de 1 500 à 3 000 ouvriers ; électricité requise ; aucun ne consomme `precision_machinery`. | Architecture accessible, couverture 75 %. `MINOR_REVISION` : ajouter la précision aux secteurs standardisés (outillage, moteurs, automobiles, armes/artillerie, munitions), pas au meuble. Papier/services appartiennent à P21. |
| P23 | Composition mécanique et presse rotative | `mechanized_printing` et `mass_circulation_press` existent, sans PM productif associé. Aucun bâtiment de publication n'est nécessaire. | Aucun effet actuel. | Manque réel. `ADD_PMG` sur `building_urban_center`, avec arrêt + presse mécanique + presse électrique, consommant papier puis moteurs/électricité et produisant des services. |
| P24 | Bureaux à tabulatrices | `pm_simple_organization`, tiroirs horizontaux, classeurs verticaux et `pm_switch_boards` dans le PMG de base de l'administration. | Les étapes existantes produisent 10/50/65/100 bureaucratie et 2/10/15/30 capacité fiscale ; papier 0/10/20/20, puis téléphones 5 ; 500 commis. | Accessible, mais sans étape électricité + précision. Couverture 45 %. `ADD_PM` dans le PMG existant avec `central_statistical_offices` + `electrical_capacitors`, sans nouveau bien ni bâtiment. |

## Progression acier / métallurgie

### Progression effective actuelle

| Rôle chronologique | Technologie | PM réellement sélectionnable | Inputs → output | Bâtiment | Diagnostic |
|---|---|---|---|---|---|
| Charbon de bois / métallurgie pré-coke | aucun stade acier explicite | aucun | abstrait hors aciérie | aucun accès à l'aciérie | L'amorce 1776 n'est pas représentée comme choix sidérurgique. |
| Coke, 1709–début XIXe | `coke_smelting` (ère 1) | aucun PM d'acier | aucun | la technologie déverrouille l'outillage, pas l'aciérie | **Vide structurel P01.** |
| Puddlage/laminage, 1784–1860 | `puddling_and_rolling` (ère 4) | `pm_blister_steel_process` par défaut | fer 40 + charbon 30 → acier 65 | `building_steel_mill`, lui-même déverrouillé ici | Fonction présente mais identité inexacte : **P02 partiel**. |
| Bessemer, seconde moitié XIXe | `bessemer_process` (ère 7) | `pm_bessemer_process` | fer 60 + charbon 30 → acier 90 | aciérie | Progression générique solide ; route Thomas absente. |
| Foyer ouvert | `open_hearth_process` (ère 8) | `pm_open_hearth_process` | fer 90 + charbon 30 → acier 120 | aciérie | Stade couvert ; pas de bien ferraille à introduire pour lui seul. |
| Arc électrique | `electric_arc_process` (ère 10) | `pm_electric_arc_process` | fer 100 + charbon 30 + électricité 30 → acier 150 | aciérie | Stade couvert ; électricité explicitement requise. |
| Aciers alliés | aucune technologie d'alliage dédiée approuvée | aucun | aucun intrant d'alliage propre | aciérie | **Décision de conception requise**, pas une implémentation automatique. |

Conclusion : il existe bien un vide entre la technologie du coke et la représentation explicite du puddlage. Après Bessemer, la chaîne n'a plus de vide structurel. La solution minimale consiste à rendre l'aciérie accessible au stade coke, ajouter un PM coke, puis convertir l'identité du PM de base en puddlage/laminage. Aucun nouveau métal n'est nécessaire.

Pour P03, la route Thomas peut employer les biens existants : fer + calcaire, acier comme produit principal et une petite quantité d'engrais comme coproduit. Elle doit être une alternative au Bessemer générique, non une amélioration strictement dominante.

## Progression minière

| Système | Couverture | Bâtiments concernés | Conclusion |
|---|---|---|---|
| Extraction de base | Complète | charbon, fer, plomb, soufre, or, cuivre, phosphate, sel ; carrière calcaire séparée | Aucun manque générique. |
| Pompage atmosphérique | Complète | les huit mines citées | P06 couvert. |
| Pompage à condensation | Complète | mêmes mines lorsque pertinent | `condensing_steam_engines` prolonge la progression. |
| Pompage diesel | Complète | mêmes mines lorsque pertinent | `compression_ignition`, avec carburants raffinés sur les recettes révisées. |
| Explosifs | Complète | nitroglycérine puis dynamite | Offre débit, pollution et parfois mortalité ; ne remplace pas la sécurité. |
| Treuils/automation vapeur | Complète | PMG spécifiques | Moteurs contre réduction de travail et parfois perte d'output. |
| Transport ferroviaire | Complète | `pm_rail_transport_mine` dans les PMG de transport | La logistique minière est déjà séparée. |
| Concentration | Complète | charbon, fer, plomb, soufre, or, cuivre, phosphate | P08 couvert par outils + chimie industrielle contre output et pollution. |
| Sel | Spécifique et suffisante | mine de sel | Pompage/explosifs/rail, mais purification propre au sel. |
| Calcaire | Spécifique et suffisante | carrière | Concassage/criblage ; ne doit pas recevoir artificiellement tous les PM de mine profonde. |
| Ventilation | Absente | mines profondes | P07 est le seul vrai manque transversal. |

La ventilation reste distincte : ni le pompage ni le rail ni les explosifs ne réduisent structurellement les risques respiratoires. Une future PMG devrait offrir :

- une option sans ventilation mécanique ;
- une ventilation vapeur consommant moteurs, charbon et/ou outils, ajoutant machinistes/ingénieurs, un peu de pollution et réduisant la mortalité des employés ;
- une ventilation électrique consommant électricité et équipement, avec moins de pollution et une réduction de mortalité plus forte ;
- aucun gain gratuit de débit, ou au plus un gain secondaire compensé.

Les modificateurs `building_laborers_mortality_mult`, `building_machinists_mortality_mult` et `building_engineers_mortality_mult` existent déjà dans les fichiers locaux et conviennent mieux qu'un effet démographique appliqué à tout l'État.

## Écarts chimie / textile

P10 à P13 sont couverts par l'architecture actuelle. Le seul travail restant est P09 : le PM textile consomme déjà `industrial_chemicals` et conserve légitimement la teinture pour la finition ; le PM papier a reçu la chimie industrielle sans abandonner les anciens `sulfur` et `dye`. La révision future doit être limitée à cette recette papier et précédée d'un contrôle de rentabilité.

Il n'est pas recommandé de rouvrir la chimie Solvay ni les engrais : les PM sont sélectionnables, leurs technologies existent, et la séparation `building_chemical_works` / `building_chemical_plant` est cohérente.

## Écarts pétroliers

Le PMG de la raffinerie ne contient aujourd'hui que `pm_fractional_distillation_refinery` : il possède donc une place claire pour une progression tardive. Un seul PM agrégé de craquage suffit. Le meilleur verrou existant est `plastics`, car il représente une maturité pétrochimique tardive ; `compression_ignition` reste une alternative de conception centrée sur la demande en carburant.

Le futur PM doit :

- rester mutuellement exclusif avec la distillation fractionnée ;
- consommer pétrole, produits chimiques industriels et électricité, éventuellement davantage d'outillage ;
- augmenter la part de carburants raffinés en réduisant la part relative des produits pétroliers lourds ;
- conserver un rôle aux lubrifiants ;
- éviter un simple multiplicateur positif sur les trois outputs.

Un étage « thermique » puis un étage « catalytique » serait trop fin pour la période et augmenterait inutilement la charge IA. P15 doit rester un seul PM.

## Écarts de chaîne du froid

Le système électrique est déjà propre : PMG séparés sur élevage, pêche et baleine, stockage réfrigéré, wagons réfrigérés puis surgélation. Les coûts en transport des wagons représentent la composante ferroviaire sans imposer un PM supplémentaire à chaque gare. Les ports ne nécessitent pas non plus un groupe dédié.

Le plus petit ajout utile est P16 : un PM mécanique pré-électrique inséré dans chacun des trois PMG existants, verrouillé par `high_pressure_steam` et alimenté par moteurs + charbon. Il peut réduire le travail et/ou apporter un petit avantage de conservation, mais doit rester inférieur au froid électrique. Il ne faut créer ni `building_cold_storage`, ni technologie spécialisée, ni bien glace/ammoniac.

## Écarts de l'industrie alimentaire

P18 reste utile parce que `automated_flour_milling` est actuellement une technologie sans PM associé, tandis que `pm_automated_bakery` n'arrive qu'en ère 12. Un PM intermédiaire dans `pmg_automation_building_food_industry` suffit : moteurs/outils, substitution d'ouvriers par machinistes et petit gain de produits alimentaires. Aucun bien farine n'est justifié.

P19 est déjà pleinement représenté à la plantation sucrière. Cette localisation est préférable à une nouvelle chaîne farine/mélasse/sucre raffiné : elle donne un choix régional avec les biens actuels et ne surcharge pas l'industrie alimentaire.

## Écarts d'électrification

P20 est partiellement représenté, mais une PMG électrique globale serait une mauvaise solution : elle pourrait se cumuler avec les PMG vapeur/assemblage et dupliquer l'automatisation. La solution minimale est d'ajouter une alternative électrique aux PMG d'automatisation existants d'une courte liste :

- `building_steel_mill` ;
- `building_tooling_workshop` ;
- `building_paper_mill` ;
- `building_glassworks` ;
- `building_motor_industry`.

`electrical_capacitors` est un verrou existant approprié. Le textile est exclu car ses PM électriques existent déjà. Automobile, armes/artillerie et munitions sont exclues de P20 parce que leur chaîne d'assemblage consomme déjà de l'électricité. Il ne faut pas mass-éditer toutes les industries.

## Écarts de production de masse

P22 existe déjà sous six variantes. Toutes consomment électricité et lubrifiants ; aucune ne consomme la nouvelle `precision_machinery`. Une révision ciblée est maintenant justifiée sur l'outillage, les moteurs, les automobiles, les armes/artillerie et les munitions. Le meuble peut garder son PM actuel sans précision, car l'intrant y serait moins lisible et plus artificiel.

Répartition future des intrants :

| Intrant | PM concernés | Justification |
|---|---|---|
| `precision_machinery` | assemblage outillage, moteurs, automobiles, armes/artillerie, munitions | Gabarits, jauges et équipement spécialisé. |
| `electricity` | déjà présente dans les six PM d'assemblage | Aucun ajout requis. |
| `paper` | P21 Scientific Management, pas P22 | Procédures, planification et suivi. |
| `services` | P21 Scientific Management, pas P22 | Encadrement et organisation. |

P21 doit rester un groupe organisationnel distinct : papier/services et davantage de commis/ingénieurs contre un avantage de productivité limité. Il ne doit pas être un bonus gratuit et doit être testé après la révision matérielle de P22.

## Écarts information / administration

P23 doit être un PMG de services d'impression dans `building_urban_center`, non un bâtiment de publication. Deux étapes utilisant les technologies existantes sont possibles : presse mécanique (`mechanized_printing`, papier + moteurs) puis presse rotative/électrique (`mass_circulation_press`, papier + électricité). L'output doit rester des services ; autorité et éducation ne devraient pas être injectées directement sans validation d'équilibrage.

P24 appartient au PMG de base de `building_government_administration`. Une alternative « bureaux à tabulatrices » entre classeurs verticaux et centraux téléphoniques peut consommer papier, électricité et `precision_machinery`, augmenter bureaucratie/capacité fiscale et déplacer une part des commis vers les ingénieurs. Aucun bien « machine de bureau » ni nouveau bâtiment n'est justifié.

## Contenu manquant confirmé

Les cinq candidats véritablement absents sont :

- P01 Coke Blast Furnaces ;
- P07 Mechanical Mine Ventilation ;
- P15 Thermal and Catalytic Cracking ;
- P21 Scientific Management ;
- P23 Mechanized Typesetting / Rotary Press.

Huit autres sont partiels et demandent soit une révision, soit une étape supplémentaire : P02, P03, P09, P16, P18, P20, P22 et P24.

## Contenu déjà couvert fonctionnellement

Les dix candidats PM pleinement couverts sont P04, P06, P08, P10, P11, P12, P13, P14, P17 et P19. Les candidats bâtiments B01 à B07 sont tous implémentés ou absorbés par l'architecture actuelle ; B08 est couvert par les PM vanilla hérités.

Les couvertures particulièrement importantes à ne pas dupliquer sont :

- pharmacie dans les travaux chimiques ;
- machines de précision dans l'outillage ;
- cuivre dans sa mine dédiée ;
- aluminium dans la métallurgie non ferreuse sans bauxite/alumine ;
- superphosphate et fixation azotée dans l'usine d'engrais ;
- concentration des minerais dans les PMG de mines ;
- froid électrique sur les producteurs alimentaires ;
- raffinage du sucre à la plantation.

## Candidats rejetés ou différés

- **B08 Cold Storage Network — REJECT.** Le bâtiment ferait doublon avec les PMG existants. P16 suffit pour compléter la chronologie.
- **P05 Alloy Steel — DEFER.** L'arc électrique ne fournit pas un intrant d'alliage. Cuivre et aluminium ne sont pas des substituts propres au nickel/chrome/tungstène. Ne pas inventer `alloy_metals` sans décision explicite sur les biens et la géographie.

## Vagues d'implémentation recommandées

| Vague | Contenu | Résultat attendu | Risque principal |
|---|---|---|---|
| A — sidérurgie initiale | P01, P02, P03 | Coke sélectionnable, pont puddlage explicite, alternative Thomas | Accessibilité de l'aciérie et équilibre du marché acier. |
| B — liens industriels | P09, P15, P07 | Nettoyage du blanchiment papier, raffinage tardif, sécurité minière | Coproduits pétroliers et cumul d'effets sur grandes régions minières. |
| C — froid et alimentation | P16, P18 | Stade mécanique du froid et minoterie à cylindres | Rentabilité des PM intermédiaires face aux options tardives. |
| D — production de masse | P22, P20, P21 | Demande de précision, moteurs électriques ciblés, organisation scientifique | Cumul des groupes et comportement IA. |
| E — administration et information | P24, P23 | Tabulation administrative et presse mécanisée | Surproduction de bureaucratie/services par bâtiments à haut niveau. |
| Décision ultérieure | P05 | Définir ou abandonner l'abstraction des alliages | Nouveau bien et géographie non autorisés à ce stade. |

Tous les verrous proposés existent déjà ; ce plan ne requiert donc aucune technologie dédiée supplémentaire. Les quantités exactes restent à concevoir et à tester dans les phases d'implémentation correspondantes.

## Classification finale

```text
BUILDINGS_STILL_REQUIRED = 0
NEW_BUILDINGS_REQUIRED_BEFORE_BETA = 0
PM_CANDIDATES_FULLY_COVERED = 10
PM_CANDIDATES_PARTIAL = 8
PM_CANDIDATES_MISSING = 5
PM_CANDIDATES_REJECTED_OR_DEFERRED = 1
NEXT_IMPLEMENTATION_BLOCK = Wave A — P01 Coke Blast Furnaces + P02 Puddling and Rolling + P03 Basic Bessemer/Thomas route
```

Listes exactes sur les 32 candidats :

```text
IMPLEMENT_NOW = P01, P02, P03
IMPLEMENT_LATER = P07, P09, P15, P16, P18, P20, P21, P22, P23, P24
NO_ACTION = B01, B02, B03, B04, B05, B06, B07, P04, P06, P08, P10, P11, P12, P13, P14, P17, P19
DEFER = P05
REJECT = B08
```

La matrice CSV constitue la source ligne par ligne des statuts et preuves, et la file d'implémentation ne contient que les candidats demandant encore un travail ou une décision future.
