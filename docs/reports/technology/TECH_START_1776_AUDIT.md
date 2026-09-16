# Audit des technologies initiales au 1er janvier 1776

## Verdict

Audit statique du working tree local, sans modification de gameplay ni nouvelle attribution nationale. Le mod remplace intégralement les technologies, mais superpose ses historiques pays à ceux de Victoria 3 1.13.11.

- Technologies actives: **287**.
- Classification: **A=25**, **B=36**, **C=71**, **D=108**, **E=47**.
- Fichiers historiques effectifs: **476**, regroupés en **474 TAG**; pays avec au moins un ajout explicite propre: **91**.
- Attributions C/D: **9** occurrences pays-technologie, **9** pays, **3** technologies distinctes.
- Nœuds sans déblocage gameplay direct ni modificateur: **82**; feuilles réellement sans enfant: **34**.
- Priorités: **P0=2, P1=188, P2=103, P3=181**.

Repères externes utilisés uniquement pour dater: [Science Museum — moteur atmosphérique de Newcomen, 1712](https://blog.sciencemuseum.org.uk/a-new-age/) et [Science Museum Group — Stockton & Darlington, 1825](https://collection.sciencemuseumgroup.org.uk/objects/co205767).

## 1. Mécanisme de départ

Les fichiers `common/history/countries/*.txt` appellent un effet `effect_starting_technology_tier_N_tech = yes`, puis ajoutent éventuellement des IDs avec `add_technology_researched`. Les sept effets sont redéfinis dans `common/scripted_effects/00_starting_inventions.txt` sous forme de listes explicites, sans `add_era_researched`.

Répartition: tier 1=1, tier 2=9, tier 3=13, tier 4=208, tier 5=62, tier 6=114, tier 7=69. Les conditions `has_technology_researched` trouvées dans événements, journaux et IA ne sont pas des attributions initiales. Aucun autre mécanisme `starting_technology*` ne remplace cette architecture.

Inventaire de contrôle: 95 fichiers de l'arborescence locale contiennent une instruction active `add_technology_researched`, dont 91 historiques pays, le fichier des tiers et trois familles runtime hors départ: `00_chris_scripted_effects.txt` (effet paramétrique), `french_revolution_mod_events.txt` (`scientific_metrology`, `codified_practical_knowledge`) et `sepoy_mutiny_events.txt` (`central_statistical_offices`). L'occurrence de `events/test_events.txt` est commentée et exclue. Aucun `add_technology =` n'est présent. Le reste de `common/history`, les scripted triggers et les fichiers technologiques ne fournissent pas de voie initiale supplémentaire.

Deux TAG cumulent chacun deux fichiers actifs aux noms non identiques: **BHV** (`bhv - bhavnagar.txt` + `bhv - gujarati prince.txt`) et **ORG** (`org - oregon.txt` + `org -oregan.txt`). La matrice agrège leurs effets; cette duplication doit être résolue dans une future wave dédiée, pas pendant cet audit.

## 2. Classification

- **A**: établi avant/au plus tard en 1776.
- **B**: frontière de 1776, réservée à quelques États ou secteurs.
- **C**: post-1776, surtout fin XVIIIe/première moitié XIXe.
- **D**: nettement tardif, surtout milieu/fin XIXe ou XXe.
- **E**: abstraction difficile à dater ou alias non recherchable.

L'era est un indice d'arbre, pas une preuve chronologique. Le CSV technologie donne EN/FR, prérequis directs, enfants, déblocages et modificateurs pour les 287 IDs.

Une lacune de localisation est détectée sans être corrigée dans cet audit: `mechanized_spinning` possède le français «Filature mécanisée précoce», mais aucune clé anglaise effective; la matrice le marque `MISSING_EN_LOCALIZATION`.

## 3. Anachronismes actuellement distribués

| Technologie | Classe | Era | Pays | Motif |
|---|---:|---:|---|---|
| `romanticism` | C | era_7 | AUS, CUB, FRA, GBR, GR5, PRU, USA | Développement postérieur à 1776, surtout première industrialisation. |
| `joint_stock_companies` | C | era_6 | DEI | Développement postérieur à 1776, surtout première industrialisation. |
| `railways` | C | era_6 | BRA | Développement postérieur à 1776, surtout première industrialisation. |

Le «top 20» demandé se limite donc à ces **3 technologies**: aucune autre technologie C/D n'est actuellement accordée au départ.

### P0

- **BRA — Brunswick**: railways; dépendances absentes: codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | railways <- high_pressure_steam,professional_civil_engineering,puddling_and_rolling | regulated_small_arms <- scientific_fortification_siegecraft.
- **DEI — East Indies**: joint_stock_companies; dépendances absentes: codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | joint_stock_companies <- commercial_insurance_markets,postal_savings | regulated_small_arms <- scientific_fortification_siegecraft.

### P1

- **AUS — Austria**: anachronismes=romanticism; dépendances=codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange | specialized_technical_academies <- institutionalized_scientific_exchange.
- **CUB — Cuba**: anachronismes=romanticism; dépendances=codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange.
- **FRA — France**: anachronismes=romanticism; dépendances=codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange | specialized_technical_academies <- institutionalized_scientific_exchange.
- **GBR — Great Britain**: anachronismes=romanticism; dépendances=codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange | specialized_technical_academies <- institutionalized_scientific_exchange.
- **GR5 — Santo Domingo**: anachronismes=romanticism; dépendances=codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange.
- **PRU — Prussia**: anachronismes=romanticism; dépendances=codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange | specialized_technical_academies <- institutionalized_scientific_exchange.
- **USA — America**: anachronismes=romanticism; dépendances=codified_practical_knowledge <- periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft.
- **181 autres P1** n'ont pas d'anachronisme C/D mais héritent d'au moins trois prérequis transitifs absents, principalement par les paliers génériques. Ils sont tous listés dans le CSV pays.

## 4. Cas ferroviaire exhaustif

`railways` est accordée au départ uniquement à **BRA**, via `common/history/countries/bra - braunschweig.txt`. Elle dépend de `high_pressure_steam`, `puddling_and_rolling` et `professional_civil_engineering`; ces trois parents sont absents. Le grant débloque immédiatement le PM ferroviaire initial du bâtiment unifié: **P0**.

## 5. Prérequis manquants

Le moteur accepte un enfant recherché sans ses parents; l'audit signale cette dette sans recommander d'ajouter automatiquement tous les parents. Le compteur exclut `urbanization`, alias caché volontaire des tiers 3–6. Parents directs les plus souvent absents, en nombre d'occurrences dans les relations pays-enfant: `institutionalized_scientific_exchange`=297, `periodical_print_networks`=279, `scientific_fortification_siegecraft`=220, `institutionalized_public_credit`=14, `organized_forestry`=13, `selective_breeding`=1, `high_pressure_steam`=1, `professional_civil_engineering`=1, `puddling_and_rolling`=1, `commercial_insurance_markets`=1, `postal_savings`=1. Le détail `enfant <- parents` et le total transitif sont dans la matrice pays.

## 6. Frontière 1776

| Technologie | Era | Classe | Prérequis | Pays | Tags |
|---|---:|---:|---|---:|---|
| `atmospheric_engine` | era_2 | B | shaft_mining, coke_smelting | 11 | BCE, BEL, FIN, KRA, NSW, ORG, SAF, SAS, SPC, TAS, WAS |
| `coke_smelting` | era_1 | A | organized_forestry | 23 | BCE, BEL, CHL, CLM, EGY, FIN, GRE, ION, IQU, KRA, LIB, NPU, NSW, ORG, PNI, PRA, SAF, SAS, SPC, SPU (+3) |
| `improved_agricultural_implements` | era_2 | B | improved_husbandry | 0 | — |
| `industrial_canals` | era_3 | B | turnpike_road_networks | 0 | — |
| `precision_boring` | era_4 | B | coke_smelting, atmospheric_engine | 10 | BCE, BEL, FIN, KRA, NSW, ORG, SAF, SAS, TAS, WAS |
| `improved_husbandry` | era_1 | A | — | 405 | ABB, ABS, ABU, ACE, ADG, ADR, AGC, AHG, AIR, AIT, AJJ, AJR, ALK, ALW, ANH, ANK, APC, ARB, ARG, ARH (+385) |
| `distillation` | era_1 | A | — | 230 | ABU, ACE, AIT, ALK, ALW, ANH, ARG, ARM, ASM, AUS, AWA, BAD, BAS, BAV, BCE, BEL, BEO, BER, BHN, BHO (+210) |
| `traditional_papermaking` | era_1 | A | organized_forestry | 10 | BCE, BEL, FIN, KRA, NSW, ORG, SAF, SAS, TAS, WAS |
| `organized_textile_production` | era_1 | A | — | 291 | ABU, ACE, AGC, AIT, ALK, ALW, ANH, ARB, ARG, ARM, ARS, ASM, AUS, AWA, AWS, BAD, BAG, BAL, BAS, BAV (+271) |

Les capacités traditionnelles peuvent être larges; `atmospheric_engine`, `precision_boring`, `industrial_canals` et la mécanisation textile doivent rester sectorielles.

## 7. TECH7A

| Technologie | Era | Classe | Prérequis | Date approximative | Pays au départ | Conséquence actuelle |
|---|---:|---:|---|---|---|---|
| `turnpike_road_networks` | era_2 | B | — | XVIIe–XVIIIe; établi mais asymétrique | — | routes: +7 infrastructure, bonus population 0,02 (plafond 0,5) |
| `industrial_canals` | era_3 | B | turnpike_road_networks | milieu XVIIIe; frontière 1776 | — | canaux: +1 infrastructure, +0,05 plafond d'économies d'échelle |
| `improved_road_engineering` | era_5 | C | turnpike_road_networks | début XIXe | — | routes: +12 infrastructure, bonus population 0,05 (plafond 1) |
| `professional_civil_engineering` | era_5 | C | industrial_canals, improved_road_engineering | fin XVIIIe–début XIXe | — | canaux: +3 infrastructure, +0,1 plafond d'économies d'échelle |
| `paved_roads` | era_10 | D | professional_civil_engineering, combustion_engine | fin XIXe–début XXe | — | routes: +20 infrastructure, population + automobiles |
| `railways` | era_6 | C | high_pressure_steam, puddling_and_rolling, professional_civil_engineering | années 1820; réseau public à vapeur | BRA | rail initial: +20 Transportation et +5 infrastructure |

Les trois PMG routes/canaux/rail s'additionnent. Aucune valeur TECH7A n'a été modifiée. `railways`, les routes modernes et les routes goudronnées restent hors départ 1776.

## 8. Technologies structurantes déjà distribuées

| Technologie | Pays | Capacités immédiates principales |
|---|---:|---|
| `improved_husbandry` | 405 | bâtiment:building_banana_plantation, bâtiment:building_coffee_plantation, bâtiment:building_dye_plantation, bâtiment:building_livestock_ranch, bâtiment:building_maize_farm, bâtiment:building_millet_farm, bâtiment:building_opium_plantation, bâtiment:building_rice_farm (+9) |
| `railways` | 1 | PM:pm_diesel_trains, PM:pm_diesel_trains_principle_transport_3, PM:pm_early_trains, PM:pm_electric_trains, PM:pm_electric_trains_principle_transport_3, PM:pm_public_trams, PM:pm_rail_transport_building_logging_camp, PM:pm_rail_transport_building_oil_rig (+6) |
| `shaft_mining` | 291 | bâtiment:building_coal_mine, bâtiment:building_copper_mine, bâtiment:building_iron_mine, bâtiment:building_lead_mine, bâtiment:building_limestone_quarry, bâtiment:building_salt_mine, bâtiment:building_sulfur_mine, décret:decree_encourage_resource_industry |
| `atmospheric_engine` | 11 | PM:pm_atmospheric_engine_pump_building_coal_mine, PM:pm_atmospheric_engine_pump_building_copper_mine, PM:pm_atmospheric_engine_pump_building_gold_mine, PM:pm_atmospheric_engine_pump_building_iron_mine, PM:pm_atmospheric_engine_pump_building_lead_mine, PM:pm_atmospheric_engine_pump_building_phosphate_mine, PM:pm_atmospheric_engine_pump_building_salt_mine, PM:pm_atmospheric_engine_pump_building_sulfur_mine |
| `colonization` | 36 | bâtiment:building_suez_canal, loi:law_colonial_exploitation, loi:law_colonial_resettlement, loi:law_extraction_economy, loi:law_frontier_colonization |
| `romanticism` | 7 | bâtiment:building_art_academy, décret:decree_greener_grass_campaign, loi:law_agrarianism, loi:law_industry_banned |
| `systematic_administrative_statistics` | 283 | bâtiment:building_government_administration, décret:decree_emergency_relief, décret:decree_road_maintenance |
| `applied_mineralogy` | 13 | bâtiment:building_gold_field, bâtiment:building_gold_mine, bâtiment:building_phosphate_mine |
| `precision_boring` | 10 | PM:coffee_plantation_wet_process_manual, PM:molds, PM:pm_pig_iron |
| `urbanization` | 396 | bâtiment:building_construction_sector, bâtiment:building_urban_center |
| `organized_textile_production` | 291 | PM:pm_craftsman_sewing, bâtiment:building_textile_mill |
| `distillation` | 230 | PM:pm_pot_stills, PM:pm_spiced_food_preparations |
| `regulated_small_arms` | 221 | bâtiment:building_arms_industry, bâtiment:building_artillery_foundry |
| `coke_smelting` | 23 | bâtiment:building_steel_mill, bâtiment:building_tooling_workshop |
| `commercial_insurance_markets` | 23 | loi:law_mercantilism, loi:law_mercantilism_navigation_acts |
| `periodical_print_networks` | 12 | loi:law_censorship, loi:law_religious_schools |
| `state_dockyard_systems` | 12 | bâtiment:building_naval_administration, bâtiment:building_shipyard |
| `scientific_fortification_siegecraft` | 10 | bâtiment:building_barrack, bâtiment:building_naval_fortification |
| `advanced_crop_rotations` | 1 | PM:pm_soil_enriching_farming, PM:pm_soil_enriching_farming_building_rice_farm |
| `systematic_population_registration` | 1 | PM:pm_horizontal_drawer_cabinets, loi:law_per_capita_based_taxation |

Les lignes `NO_DIRECT_GAMEPLAY_UNLOCK` du CSV distinguent les nœuds de passage des feuilles réellement vides; ne pas distribuer une technologie uniquement pour remplir visuellement l'arbre.

Les contenus listés sont des objets qui citent la technologie comme verrou. Lorsqu'un PM possède plusieurs technologies requises, cette liste ne signifie pas que le nœud suffit à lui seul; par exemple `railways` ouvre immédiatement les premiers trains mais reste aussi co-prérequis des trains électriques et diesel.

## 9. Pays prioritaires

| TAG | Pays | Source | Ajouts explicites | Anachronismes | Prérequis directs absents |
|---|---|---|---|---|---|
| GBR | Great Britain | tier_4 | colonization;romanticism;specialized_technical_academies | romanticism | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange | specialized_technical_academies <- institutionalized_scientific_exchange |
| FRA | France | tier_4 | colonization;romanticism;specialized_technical_academies;systematic_population_registration;traditional_food_processing | romanticism | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange | specialized_technical_academies <- institutionalized_scientific_exchange |
| SPA | Spain | tier_4 | colonization;specialized_technical_academies | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | specialized_technical_academies <- institutionalized_scientific_exchange |
| POR | Portugal | tier_4 | colonization;specialized_technical_academies;systematic_legal_codification | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | specialized_technical_academies <- institutionalized_scientific_exchange |
| AUS | Austria | tier_4 | romanticism;specialized_technical_academies;systematic_legal_codification | romanticism | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange | specialized_technical_academies <- institutionalized_scientific_exchange |
| PRU | Prussia | tier_4 | colonization;romanticism;specialized_technical_academies | romanticism | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | romanticism <- institutionalized_scientific_exchange | specialized_technical_academies <- institutionalized_scientific_exchange |
| RUS | Russia | tier_4 | colonization;systematic_legal_codification | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft |
| TUR | Turkey | tier_4 | specialized_technical_academies | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | specialized_technical_academies <- institutionalized_scientific_exchange |
| SWE | Sweden | tier_4 | colonization;specialized_technical_academies | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | specialized_technical_academies <- institutionalized_scientific_exchange |
| DEN | Denmark | tier_4 | specialized_technical_academies | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | specialized_technical_academies <- institutionalized_scientific_exchange |
| DENNOR | Denmark-Norway | tier_4 | colonization;specialized_technical_academies | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | specialized_technical_academies <- institutionalized_scientific_exchange |
| NET | Netherlands | tier_4 | colonization;specialized_technical_academies | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | specialized_technical_academies <- institutionalized_scientific_exchange |
| USA | America | tier_4 | colonization;institutionalized_scientific_exchange;romanticism | romanticism | codified_practical_knowledge <- periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft |
| BAV | Bavaria | tier_4 | — | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft |
| SAX | Saxony | tier_4 | — | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft |
| SAR | Sardinia-Piedmont | tier_4 | — | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft |
| SIC | Two Sicilies | tier_4 | — | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft |
| NAP | absent | — | — | — | — |
| VEN | Venice | tier_4 | specialized_technical_academies | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft | specialized_technical_academies <- institutionalized_scientific_exchange |
| PLC | Poland-Lithuania | tier_4 | — | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft |
| PER | Persia | tier_4 | state_dockyard_systems | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft |
| CHI | China | tier_5 | international_relations;systematic_legal_codification | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks |
| JAP | Japan | tier_4 | colonization;institutionalized_scientific_exchange;systematic_cadastral_surveying | — | codified_practical_knowledge <- periodical_print_networks | regulated_small_arms <- scientific_fortification_siegecraft |
| MYS | Mysore | tier_5 | — | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks |
| MARATH | Maratha Confederacy | tier_5 | international_relations;state_dockyard_systems | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks |
| MUG | Hindustan | tier_5 | — | — | codified_practical_knowledge <- institutionalized_scientific_exchange,periodical_print_networks |

- **USA/Treize Colonies**: le départ est porté par `USA`; aucun second setup technologique «13 colonies» n'existe. Les journaux d'indépendance se greffent sur USA.
- **DEN/DENNOR**: deux setups distincts; la future consigne doit les harmoniser explicitement.
- **NAP** est absent; **SIC** porte les Deux-Siciles.
- **MUG**, **MYS**, **MARATH** sont séparés; ne pas propager automatiquement les technologies du Moghol aux successeurs.
- **PLC** existe et ne reçoit actuellement qu'un palier générique.

## 10. Asymétries

Un tier n'est pas un niveau de civilisation. Les capacités navales exigent une réalité maritime; les savoir-faire agricoles/artisanaux peuvent coexister avec une faible administration scientifique. `colonization` est classée E: pas automatiquement anachronique, mais son attribution à 36 pays doit être décidée politiquement, pays par pays.

## 11. Vagues proposées, sans changement ici

1. **Wave 0 P0**: traiter `railways` à BRA et `joint_stock_companies` à DEI.
2. **Wave 1 grandes puissances**: GBR, FRA, SPA, POR, AUS, PRU, RUS, TUR, SWE, DEN/DENNOR, NET, USA.
3. **Wave 2 Europe secondaire**: BAV, SAX, SAR, SIC, VEN, PLC.
4. **Wave 3 hors Europe**: PER, CHI, JAP, MYS, MARATH, MUG et successeurs.
5. **Wave 4 reste du monde**: remplacer les paliers seulement après arbitrage régional.
6. **Wave 5 nœuds vides**: audit séparé des déblocages; ne pas maquiller les trous par la distribution.

## 12. Livrables

- `TECH_START_1776_TECHNOLOGIES.csv`: 287 technologies.
- `TECH_START_1776_COUNTRIES.csv`: 474 TAG agrégés, y compris les pays au tier 7 vide.
- Aucun fichier de gameplay, aucun start et aucune valeur n'ont été modifiés.
