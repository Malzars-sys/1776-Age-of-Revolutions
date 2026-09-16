# TECH START 1776 — Résolution finale arbre et classifications

Date historique absolue : **1776-01-01**  
Version auditée : **Victoria 3 1.13.11**  
Statut : **recherche, audit, décision et simulation uniquement**.

## 1. Résumé exécutif

Les 26 relations structurelles, 26 problèmes de classification et 7 cas historiques ont été arbitrés. La proposition retire les prérequis qui confondaient proximité visuelle, matière première ou modèle institutionnel particulier avec une nécessité technique universelle. Elle remplace `traditional_furniture_making` par `organized_workshops`, sans augmenter le nombre net de technologies, et déplace le gate de `building_tooling_workshop` hors de `coke_smelting`.

La simulation documentaire du graphe proposé donne **0 dette directe** et **0 dette transitive** sur les cibles historiques des pays recherchés. L'audit complémentaire confirme que `urbanization` n'est pas encore un alias inerte : ses modificateurs ont bien été déplacés, mais deux gates de bâtiment et des attributions temporaires/historiques subsistent. La résolution finale conserve l'ID tout en supprimant ces responsabilités dans une future opération atomique.

## 2. Méthodologie

L'autorité est, dans l'ordre : working tree local, sept fichiers canoniques SECOND PASS, puis vanilla 1.13.11. Chaque technologie a été rapprochée de ses usages réels dans `common/buildings`, `common/production_methods`, lois, événements et effets scriptés. Les sources historiques de la SECOND PASS ont été conservées; les sept cas ouverts ont reçu une recherche ciblée supplémentaire. La fermeture a ensuite été simulée sur les listes `Historical_Target_Technologies`, sans modifier le gameplay et sans ajouter automatiquement les parents manquants.

La liste `unlocking_technologies` est traitée comme une exigence cumulative. C'est essentiel pour `sugar_refining`: les PM vapeur, vide et centrifuge possèdent déjà un second gate tardif et ne sont donc pas ouverts par la seule technologie A.

## 3. 26 décisions d'arbre

| Enfant | Parent actuel | Décision | Architecture finale | Confiance |
|---|---|---|---|---|
| advanced_crop_rotations | selective_breeding | REMOVE_EDGE | improved_husbandry (conservé comme seul parent) | HIGH |
| applied_mineralogy | shaft_mining | REMOVE_EDGE | aucun parent | HIGH |
| atmospheric_engine | coke_smelting | REPLACE_EDGE | shaft_mining | HIGH |
| codified_practical_knowledge | institutionalized_scientific_exchange | REMOVE_EDGE | aucun parent | HIGH |
| codified_practical_knowledge | periodical_print_networks | REMOVE_EDGE | aucun parent | HIGH |
| commercial_insurance_markets | institutionalized_public_credit | REMOVE_EDGE | aucun parent | HIGH |
| commercial_insurance_markets | international_relations | REMOVE_EDGE | aucun parent | MEDIUM |
| industrial_canals | turnpike_road_networks | REMOVE_EDGE | aucun parent | HIGH |
| industrial_ceramics | traditional_glassmaking | REMOVE_EDGE | aucun parent | HIGH |
| light_infantry_tactics | regulated_small_arms | REMOVE_EDGE | aucun parent | HIGH |
| medical_degrees | institutionalized_scientific_exchange | REMOVE_EDGE | aucun parent | HIGH |
| military_topographic_surveying | permanent_engineer_services | REMOVE_EDGE | aucun parent | MEDIUM |
| organized_elementary_schooling | periodical_print_networks | REMOVE_EDGE | aucun parent | HIGH |
| permanent_engineer_services | scientific_fortification_siegecraft | REMOVE_EDGE | aucun parent | MEDIUM |
| permanent_military_hospitals | scientific_fortification_siegecraft | REMOVE_EDGE | aucun parent | HIGH |
| political_economy | codified_practical_knowledge | REMOVE_EDGE | aucun parent | MEDIUM |
| political_economy | commercial_insurance_markets | REMOVE_EDGE | aucun parent | HIGH |
| political_economy | systematic_administrative_statistics | REMOVE_EDGE | aucun parent | MEDIUM |
| regulated_small_arms | scientific_fortification_siegecraft | REMOVE_EDGE | aucun parent | HIGH |
| scientific_naval_architecture | state_dockyard_systems | REMOVE_EDGE | aucun parent | MEDIUM |
| ship_classification_surveying | enclosed_dock_systems | REMOVE_EDGE | aucun parent | HIGH |
| standardized_field_artillery | regulated_small_arms | REMOVE_EDGE | aucun parent | MEDIUM |
| stock_exchange | institutionalized_public_credit | REMOVE_EDGE | aucun parent | HIGH |
| sugar_refining | traditional_food_processing | REMOVE_EDGE | aucun parent | MEDIUM |
| systematic_legal_codification | systematic_administrative_statistics | REMOVE_EDGE | aucun parent | HIGH |
| traditional_furniture_making | organized_textile_production | REDEFINE_TECH | organized_workshops (sans parent; parent ajouté à precision_boring) | HIGH |

Décision structurante supplémentaire : ajouter `organized_workshops` comme parent de `precision_boring`. Ce lien relie la manufacture générale aux PM ultérieurs des outils (`pm_pig_iron`) et du mobilier (`mechanical_tools` puis `pm_lathe`) sans rattacher l'atelier d'outils à la fonte au coke.

## 4. 26 décisions de classification

| Technologie | Classe actuelle | Décision | Classe finale | Contenu déplacé |
|---|---|---|---|---|
| advanced_crop_rotations | B | RECLASSIFY | A (sélective) | — |
| advanced_spinning | B | REDEFINE_TECH | C | — |
| casemated_fortifications | C | KEEP_CLASS | C | — |
| classical_political_economy | B | RECLASSIFY | C | — |
| clinicopathological_medicine | C | KEEP_CLASS | C | — |
| condensing_steam_engines | B | RECLASSIFY | C | — |
| constitutional_government | B | RECLASSIFY | A (sélective) | — |
| cotton_gin | C | KEEP_CLASS | C | — |
| crystal_glass | C | KEEP_CLASS | C | — |
| hydraulic_cements | C | KEEP_CLASS | C | — |
| hydrographic_surveying | C | KEEP_CLASS | C | — |
| improved_agricultural_implements | B | RECLASSIFY | A (sélective) | — |
| industrial_acids | A | MOVE_UNLOCKS | A (sélective) | building_chemical_plant; building_explosives_factory |
| industrial_canals | B | REDEFINE_TECH | B (sélective) | — |
| industrial_ceramics | B | KEEP_CLASS | B (sélective) | — |
| mechanized_weaving | B | RECLASSIFY | C | — |
| medical_degrees | B | RECLASSIFY | A (sélective) | — |
| military_veterinary_services | C | KEEP_CLASS | C | — |
| organized_elementary_schooling | B | RECLASSIFY | A (sélective) | — |
| professional_civil_engineering | C | KEEP_CLASS | C | — |
| rifling | C | KEEP_CLASS | C | — |
| standardized_military_rockets | C | KEEP_CLASS | C | — |
| sugar_refining | A | MOVE_UNLOCKS | A (sélective) | pm_sugar_beets |
| systematic_cadastral_surveying | B | RECLASSIFY | A (sélective) | — |
| systematic_legal_codification | B | RECLASSIFY | A (sélective) | — |
| systematic_population_registration | B | RECLASSIFY | A (sélective) | — |

Les classes C déjà hors de la matrice A/B sont conservées lorsqu'un précurseur isolé ne suffit pas au paquet gameplay national. Cela évite d'ouvrir une nouvelle recherche mondiale non couverte par la SECOND PASS.

## 5. 7 cas historiques résolus

| TAG | Pays | Technologie | Décision | Confiance | Motif |
|---|---|---|---|---|---|
| CLM | Colombia | medical_degrees | ABSENT | HIGH | Une institution antérieure mais interrompue ne constitue pas une capacité active au 1er janvier 1776. |
| JAP | Japan | medical_degrees | PRESENT | MEDIUM | La définition finale accepte collège/école médicale institutionnelle, sans exiger une licence nationale moderne; l'école existe avant le cutoff. |
| MOR | Morocco | sugar_refining | ABSENT | HIGH | L'existence historique ancienne ne suffit pas à établir une capacité active au cutoff. |
| MYS | Mysore | mysorean_iron_cased_rocketry | ABSENT | MEDIUM | Le nœud vise spécifiquement la fusée à enveloppe de fer, pas l'usage générique de fusées; le cutoff strict impose ABSENT. |
| PER | Persia | medical_degrees | ABSENT | MEDIUM | La tradition savante est réelle mais le seuil institutionnel national du nœud n'est pas démontré pour la Perse zand en 1776. |
| PLC | Poland-Lithuania | medical_degrees | PRESENT | MEDIUM | Une faculté active mais imparfaite satisfait la définition A sélective; le nœud ne requiert pas la clinique réformée de 1780. |
| SC2 | Nueva Granada | medical_degrees | ABSENT | HIGH | Le TAG de Nouvelle-Grenade ne reçoit pas une technologie nationale sur la seule base d'un diplôme de 1764 suivi d'une interruption. |

Résultat : **2 PRESENT**, **5 ABSENT**, **0 UNRESOLVED**. Les décisions reposent notamment sur l'Université du Rosario, le Tokyo National Museum, PubMed, Encyclopaedia Iranica, l'Université Jagellonne, Persée, le National Army Museum et Cambridge.

## 6. `atmospheric_engine`

Architecture finale : `shaft_mining -> atmospheric_engine`. `coke_smelting` est retirée des parents. La pompe atmosphérique répond à un problème d'exhaure et non à une obligation de fonte au coke; `shaft_mining` suffit comme infrastructure productive préalable.

## 7. Agriculture

`advanced_crop_rotations` conserve seulement `improved_husbandry` et passe en A sélective. `improved_agricultural_implements` passe également en A sélective. Le modèle britannique associant rotations et élevage sélectif n'est pas imposé aux systèmes agricoles asiatiques ou continentaux.

## 8. Armement

`regulated_small_arms` est découplée de la fortification scientifique. `light_infantry_tactics` et `standardized_field_artillery` sont également découplées des armes légères réglementées; elles convergent plus tard avec les autres capacités dans `armament_standardization_inspection`. Cette architecture permet doctrine, artillerie et industrie d'arsenal distinctes.

## 9. Savoirs codifiés

Les deux parents de `codified_practical_knowledge` sont retirés. Manuscrits, ateliers, archives et écoles sont des supports suffisants; presse périodique et réseau savant institutionnel ne sont pas des exigences universelles. Le nœud peut être sans parent mais reste connecté par ses descendants.

## 10. Canaux et infrastructures

`industrial_canals` perd `turnpike_road_networks`, reste B sélective et doit être localisé comme réseau de voies d'eau commerciales organisées. `professional_civil_engineering` reste C car son gameplay actuel ouvre cimenterie, routes bétonnées et canaux aménagés, même si le Corps des Ponts et Chaussées constitue un précurseur antérieur.

## 11. Médecine et éducation

`medical_degrees` passe en A sélective et perd le parent `institutionalized_scientific_exchange`. Sa définition couvre facultés, collèges, examens, titres et licences reconnus, sans exiger le diplôme professionnel moderne. `organized_elementary_schooling` passe en A sélective et perd le parent presse périodique. `clinicopathological_medicine` reste C: Morgagni est un précurseur, pas encore une généralisation nationale.

## 12. Finance et économie politique

Assurance, crédit public, bourse et diplomatie sont séparés. `commercial_insurance_markets` perd ses deux parents; `stock_exchange` perd `institutionalized_public_credit`. `political_economy` perd ses trois parents cumulatifs. `classical_political_economy` passe en C: la physiocratie reste représentée par le nœud antérieur, tandis que le paquet classique/libéral et les clauses commerciales sont postérieurs au cutoff strict.

## 13. Manufactures traditionnelles

Architecture retenue :

```text
organized_workshops (era_1, production, sans parent)
├── ouvre building_furniture_manufactory
├── ouvre building_tooling_workshop
└── parent de precision_boring
    ├── ouvre pm_pig_iron dans l'outillage
    └── mène à mechanical_tools, puis pm_lathe dans la manufacture domestique
```

`traditional_furniture_making` disparaît comme nœud dédié et sa cible historique est migrée 1:1 vers `organized_workshops`. Le bâtiment de mobilier doit être compris/localisé comme manufacture générale de meubles et autres biens utiles au foyer. `coke_smelting` conserve l'aciérie mais perd la fabrique d'outils. Le nombre net de technologies ne change pas.

## 14. Textile

`mechanized_weaving` passe en C parce que `pm_mechanized_looms` représente des métiers industriels. `advanced_spinning` est redéfini en C comme mécanisation de la couture, car son seul unlock réel est `pm_sewing_machines`; cette réutilisation évite de créer une technologie supplémentaire et évite un nœud vide. Les machines électriques restent sur `electrical_capacitors`.

## 15. Chimie

`industrial_acids` reste A sélective pour `building_chemical_works`. `building_chemical_plant` doit migrer vers `improved_fertilizer`; `building_explosives_factory` vers `nitroglycerin`. Cela sépare chimie/acides anciens, engrais minéraux et explosifs industriels sans créer une nouvelle technologie.

## 16. Sucre

`sugar_refining` reste A sélective. `pm_sweeteners` reste attaché au nœud. `vacuum_pan_sugar`, `steam_powered_evaporation_sugar` et `centrifugal_machine_sugar` restent aussi attachés comme exigence de base, mais leurs seconds gates (`high_pressure_steam`, `watertube_boiler`, `rotary_valve_engine`) empêchent tout déblocage anticipé. Seul `pm_sugar_beets`, actuellement ouvert par `sugar_refining` seul, migre vers `improved_fertilizer`.

## 17. Technologies navales

`scientific_naval_architecture` perd le parent obligatoire `state_dockyard_systems`: des chantiers privés ou royaux peuvent formaliser la conception. `ship_classification_surveying` perd `enclosed_dock_systems`; assurance maritime peut guider son placement visuel mais ne devient pas un nouveau verrou. `hydrographic_surveying` reste C car quelques missions de levé ne suffisent pas à un service national systématique.

## 18. `urbanization` et compatibilité

| Nœud | Recherchable | Gameplay | Action |
|---|---|---|---|
| urbanization | NO (can_research = no) | building_urban_center; building_construction_sector; Aucun modificateur actif | REDEFINE |
| colonization | YES | Lois coloniales, décisions/JE et possibilités de colonisation via usages externes; institution coloniale +2; infamie contre non-reconnus -10 % | KEEP_NORMAL |
| multilateral_alliances | YES | Alliances multiples; infamie -25 %; manœuvres diplomatiques +50 %; alliances multiples | KEEP_NORMAL |
| political_agitation | YES | Lois de suffrage/liberté et contenu d'agitateurs; SOL attendu/alphabétisation +1; autorité +10 %; pouvoir électoral +10 %; +1 agitateur | KEEP_NORMAL |
| mysorean_iron_cased_rocketry | NO (can_research = no) | Aucun; Aucun | REMOVE_FROM_START_AUDIT |

`urbanization` est cachée et sans modificateur actif, mais elle ouvre effectivement `building_urban_center` dans le mod et `building_construction_sector` via le fichier vanilla chargé. Elle est aussi parent de `tech_bureaucracy` et `urban_planning`, figure dans **267 historiques pays** et reçoit encore **4 attributions de palier**. Les rapports TECH6B3F et TECH6B3H montrent que ce traitement avait été explicitement différé parce que `paved_roads` (era 10) ne pouvait pas remplacer le gate d'un bâtiment fondamental : il ne s'agit donc pas d'un modificateur oublié, mais d'une dette de compatibilité non fermée.

Le contrôle des **43 technologies `can_research = no`** trouve **0 modificateur actif** dans un alias caché. Les seuls blocs `modifier` présents dans `admiralty` et `screw_frigate` sont vides et ne contiennent que des commentaires. La matrice TECH6B3F compte 178 responsabilités transférées, 4 références de compatibilité autorisées et exactement 2 responsabilités différées : les deux bâtiments ci-dessus.

Action finale : **REDEFINE**. Dans une même implémentation, retirer les gates technologiques de `building_urban_center` et `building_construction_sector`, retirer les deux arêtes cachées, supprimer les 267 grants pays et les 4 grants de palier, puis conserver seulement la définition inerte de l'alias. Retirer les grants avant les gates casserait le démarrage; déplacer les gates vers `paved_roads` les rendrait artificiellement tardifs.

## 19. Technologies E

`colonization` reste une technologie normale à gameplay réel. `multilateral_alliances` et `political_agitation` sont également de vraies technologies tardives et recherchables; elles restent simplement absentes au départ 1776. `mysorean_iron_cased_rocketry` est un placeholder caché, vide et sans usage externe : il est retiré de l'audit de départ tant qu'une phase événementielle ne lui attribue pas une responsabilité gameplay.

## 20. Simulation du nouvel arbre

Le graphe simulé applique les 26 décisions, remplace `traditional_furniture_making` par `organized_workshops`, ajoute le lien vers `precision_boring`, simule `urbanization` comme alias inerte après nettoyage atomique et applique les sept décisions pays. Résultat : **0 prérequis directs manquants** et **0 prérequis transitifs manquants**.

| Statut simulé | Pays |
|---|---|
| READY | 154 |
| READY_AFTER_SIMPLE_TREE_CHANGE | 53 |
| READY_AFTER_TECH_CONTENT_CHANGE | 264 |
| NEEDS_HUMAN_DECISION | 0 |
| RESEARCH_GAP | 3 |

## 21. Dettes de prérequis restantes

Aucune.

Les absences de `urbanization` ne sont pas comptées comme dettes historiques : le nœud n'est pas une capacité de 1776 et son ID est conservé uniquement comme alias externe inerte. La suppression de ses attributions internes dépend impérativement du retrait simultané des deux gates de bâtiment.

## 22. Cible pays après résolution

La cible conserve 471 pays recherchés et trois gaps (`GAL`, `MLT`, `PPU`). Les relations `traditional_furniture_making` sont renommées `organized_workshops`. JAP et PLC gagnent `medical_degrees`; CLM, PER et SC2 restent sans ce nœud; MOR reste sans `sugar_refining`; MYS ne reçoit pas le placeholder rocketry.

## 23. Risques gameplay

- Risque critique : retirer les grants de `urbanization` avant les deux gates casserait la construction et les centres urbains; l'opération doit être atomique.
- Risque élevé : déplacer `building_tooling_workshop` exige de conserver une offre minimale d'outils au départ et de tester l'IA.
- Risque moyen : le nouveau parent de `precision_boring` doit être testé contre les cycles et les positions visuelles.
- Risque moyen : les déplacements chimie/sucre changent les dates de disponibilité de bâtiments ou PM et exigent un smoke test économique.
- Risque faible : les reclassifications A/B/C sont documentaires jusqu'à la future réécriture des setups.

## 24. Plan d'implémentation futur

Le fichier `TECH_START_1776_POST_RESOLUTION_IMPLEMENTATION_PLAN.csv` contient les opérations déterministes : arêtes, remplacement du nœud manufacturier, déplacements d'unlocks, nettoyage atomique de `urbanization`, préservation de son ID inerte et delta pays issu de la SECOND PASS. Les centaines de changements `urbanization` ne sont pas dupliqués ligne par ligne : deux lignes agrégées couvrent précisément les 267 grants pays et les 4 grants de palier. Les autres lignes pays remplacent l'ancien ID mobilier par `organized_workshops`.

Ordre recommandé : (1) arbre et nouveau nœud; (2) opération atomique `urbanization` — gates, arêtes cachées, grants pays et paliers; (3) déplacements chimie/sucre; (4) localisation EN/FR; (5) validation statique; (6) setups pays; (7) runtime et IA bêta.

## 25. Décisions nécessitant encore validation humaine

Aucun arbitrage historique ne reste ouvert. La future implémentation doit toutefois faire valider en runtime le nom final EN/FR de `organized_workshops`, sa position graphique, l'offre d'outils et la capacité de l'IA à construire les deux manufactures. Les trois `RESEARCH_GAP` restent volontairement hors périmètre.

## Contrôles de complétude

- TREE REVIEWS : **26/26**.
- CLASSIFICATION REVIEWS : **26/26**.
- Cas historiques : **7/7**, aucun UNRESOLVED.
- Nœuds de compatibilité : **5/5** audités.
- Technologies et TAG inconnus dans les données canoniques : **0 détecté**.
- Fichiers gameplay modifiés par cette phase : **0**.

## Résumé demandé

TREE REVIEWS
- KEEP_EDGE = 0
- REMOVE_EDGE = 24
- REPLACE_EDGE = 1
- OTHER = 1

CLASSIFICATION
- KEEP_CLASS = 11
- RECLASSIFY = 11
- MOVE_UNLOCKS = 2
- SPLIT_TECH = 0
- REDEFINE_TECH = 2

UNRESOLVED
- resolved PRESENT = 2
- resolved ABSENT = 5
- still unresolved = 0

COMPATIBILITY
- urbanization = REDEFINE (conserver l'alias inerte après nettoyage atomique)
- autres alias/nœuds = colonization KEEP_NORMAL; multilateral_alliances KEEP_NORMAL; political_agitation KEEP_NORMAL; mysorean_iron_cased_rocketry REMOVE_FROM_START_AUDIT

POST-RESOLUTION
- remaining prerequisite issues = 0
- READY countries = 154
- READY_AFTER_SIMPLE_TREE_CHANGE = 53
- READY_AFTER_TECH_CONTENT_CHANGE = 264
- NEEDS_HUMAN_DECISION = 0
- RESEARCH_GAP = 3

Aucun fichier gameplay modifié, aucun commit, aucun push.
