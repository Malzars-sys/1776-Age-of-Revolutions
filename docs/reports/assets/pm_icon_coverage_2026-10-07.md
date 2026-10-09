# Inventaire des PM sans illustration dédiée et des placeholders — 7 octobre 2026

État de l'arbre de travail sur `codex/frederick-tricorne`, base Git `d8b1c7e`. Les tableaux d'inventaire décrivent la passe initiale ; les intégrations successives sont documentées jusqu'au dixième lot de canaux intégré (section 23), puis aux locomotives recolorées en vert uniquement (section 24) ; les PM routiers sont laissés tels quels à la demande de l'utilisateur. L'aluminium a été uniquement recoloré, sans redessin (section 19). Les icônes vanilla `unused/` retenues par l'utilisateur sont conservées. Le cuivre reste hors du lot de création. Les codes couleur et écarts sont consignés en section 15. Les ajustements navals et routiers sont documentés en sections 8 et 9 ; l'esclavage colonial en section 11.

## Résultat

| Contrôle | Nombre |
| --- | ---: |
| Identifiants de PM du fork absents du jeu installé | 152 |
| Nouveaux PM hors cuivre utilisant une illustration vanilla | 77 |
| Dont PM utilisant des icônes `unused/` conservées à la demande de l'utilisateur | 19 |
| Nouveaux PM du cuivre utilisant une illustration vanilla | 6 |
| Nouveaux PM utilisant une texture locale | 64 |
| Dont réemploi provisoire de l'icône de concassage pour deux procédés de ciment | 0 |
| Nouveaux PM utilisant encore le cerf d'erreur, tous liés au cuivre | 5 |
| PM à identifiant vanilla réaffectés à un autre procédé et à illustrer également | 5 |
| Groupes de PM hors cuivre encore liés au cerf d'erreur | 5 |
| Références textuelles d'erreur dans les fichiers de jeu du mod | 27 |

Les 77 références vanilla ne correspondent pas à 77 illustrations à générer séparément : 19 utilisent des icônes `unused/` que l'utilisateur a demandé de conserver ; sept sont des états « aucun/désactivé », et de nombreuses variantes d'un même équipement peuvent partager une icône de famille. Les 58 autres références ne représentent donc pas non plus 58 créations obligatoires. La cohérence du sujet, de la palette et de la suite de PM reste le critère. Les cinq PM réaffectés s'ajoutent aux 152 nouveaux identifiants ; ils ne sont pas inclus dans le compte de 77.

La précédente passe avait remplacé les chemins d'erreur de 71 PM par des images vanilla ou locales. Elle avait réparé les raccordements, mais pas terminé la création des illustrations dédiées. Elle ne contrôlait pas les icônes des groupes de PM.

## 1. Nouveaux PM hors cuivre encore sur une image vanilla

Les chemins ci-dessous sont relatifs à `gfx/interface/icons/production_method_icons/`, y compris les sous-dossiers `unused/` réellement livrés avec le jeu. « Partage technique possible » distingue les équipements génériques des réemplois dont le sujet est différent ; ce n'est pas une validation artistique.

| PM — nom français et identifiant exact | Image actuelle | Qualification | Source : ligne de texture | Première apparition Git |
| --- | --- | --- | --- | --- |
| Hauts-fourneaux au coke — `pm_coke_blast_furnaces` | `blister_steel_process.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F10:1570 | `8e8794b` (2026-09-11) |
| Procédé Thomas — `pm_thomas_process` | `bessemer_process.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F10:1665 | `8e8794b` (2026-09-11) |
| Exploitation forestière organisée — `pm_organized_forestry` | `simple_forestry.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F12:18 | `bf0b53a` (2026-09-16) |
| Pelles et pioches — `pm_picks_and_shovels_building_salt_mine` | `picks_and_shovels.dds` | Équipement générique ; partage technique possible | F13:2 | `4db77ce` (2026-08-27) |
| Pompe à feu — `pm_atmospheric_engine_pump_building_salt_mine` | `pumps.dds` | Équipement générique ; partage technique possible | F13:18 | `4db77ce` (2026-08-27) |
| Motopompe à condensation — `pm_condensing_engine_pump_building_salt_mine` | `condensing_engine_pump.dds` | Équipement générique ; partage technique possible | F13:46 | `4db77ce` (2026-08-27) |
| Pompe diesel — `pm_diesel_pump_building_salt_mine` | `diesel_pump.dds` | Équipement générique ; partage technique possible | F13:74 | `4db77ce` (2026-08-27) |
| Nitroglycérine — `pm_nitroglycerin_building_salt_mine` | `nitroglycerin.dds` | Équipement générique ; partage technique possible | F13:102 | `4db77ce` (2026-08-27) |
| Dynamite — `pm_dynamite_building_salt_mine` | `dynamite.dds` | Équipement générique ; partage technique possible | F13:132 | `4db77ce` (2026-08-27) |
| Production de base — `default_building_salt_pan` | `gold_mining.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F13:156 | `4db77ce` (2026-08-27) |
| Culture traditionnelle des épices — `pm_spice_cultivation` | `plantation_production.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F14:2 | `ff0c74a` (2026-08-28) |
| Culture mécanisée des épices — `pm_mechanized_spice_cultivation` | `automatic_irrigation.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F14:17 | `ff0c74a` (2026-08-28) |
| Pics et pelles — `pm_picks_and_shovels_building_limestone_quarry` | `picks_and_shovels.dds` | Équipement générique ; partage technique possible | F15:2 | `000af39` (2026-09-08) |
| Pas de réseau ferroviaire — `pm_no_rail_network` | `no_rail_transport.dds` | État désactivé générique ; peut rester partagé | F16:98 | `bf0b53a` (2026-09-16) |
| Procédé des chambres de plomb — `pm_lead_chamber_process` | `ammonia_soda_process.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F18:6 | `000af39` (2026-09-08) |
| Procédé Leblanc — `pm_leblanc_alkali_process` | `leblanc_process.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F18:40 | `000af39` (2026-09-08) |
| Blanchiment chimique des textiles — `pm_chemical_bleaching_textile_mill` | `bleached_paper.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F18:78 | `000af39` (2026-09-08) |
| Procédé Solvay — `pm_solvay_process_building_chemical_works` | `vaccum_evaporation.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F18:109 | `8e8794b` (2026-09-11) |
| Électrolyse de saumure — `pm_brine_electrolysis_building_chemical_works` | `vaccum_brine_electrolysis.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F18:142 | `8e8794b` (2026-09-11) |
| Procédé Wöhler-Deville — `pm_wohler_deville_process` | `blister_steel_process.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F22:71 | `bf0b53a` (2026-09-16) |
| Avions entièrement métalliques — `pm_all_metal_aircraft` | `aeroplanes_production.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F22:129 | `87d030e` (2026-09-09) |
| Conducteurs en aluminium — `pm_aluminium_conductors_building_power_plant` | `electric_streetlights.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F22:160 | `87d030e` (2026-09-09) |
| Pics et pelles — `pm_picks_and_shovels_building_bauxite_mine` | `picks_and_shovels.dds` | Équipement générique ; partage technique possible | F22:226 | `bf0b53a` (2026-09-16) |
| Pompe à moteur atmosphérique — `pm_atmospheric_engine_pump_building_bauxite_mine` | `pumps.dds` | Équipement générique ; partage technique possible | F22:247 | `bf0b53a` (2026-09-16) |
| Pompe à moteur à condensation — `pm_condensing_engine_pump_building_bauxite_mine` | `condensing_engine_pump.dds` | Équipement générique ; partage technique possible | F22:268 | `bf0b53a` (2026-09-16) |
| Pompe Diesel — `pm_diesel_pump_building_bauxite_mine` | `diesel_pump.dds` | Équipement générique ; partage technique possible | F22:289 | `bf0b53a` (2026-09-16) |
| Nitroglycérine — `pm_nitroglycerin_building_bauxite_mine` | `nitroglycerin.dds` | Équipement générique ; partage technique possible | F22:310 | `bf0b53a` (2026-09-16) |
| Dynamite — `pm_dynamite_building_bauxite_mine` | `dynamite.dds` | Équipement générique ; partage technique possible | F22:330 | `bf0b53a` (2026-09-16) |
| Treuil à vapeur — `pm_steam_donkey_building_bauxite_mine` | `steam_donkey.dds` | Équipement générique ; partage technique possible | F22:364 | `bf0b53a` (2026-09-16) |
| Transport ferroviaire — `pm_rail_transport_building_bauxite_mine` | `rail_transport.dds` | Équipement générique ; partage technique possible | F22:380 | `bf0b53a` (2026-09-16) |
| Ventilation mécanique à vapeur — `pm_steam_mine_ventilation_building_bauxite_mine` | `pumps.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F22:392 | `bf0b53a` (2026-09-16) |
| Ventilation électrique — `pm_electric_mine_ventilation_building_bauxite_mine` | `electric_engines.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F22:413 | `bf0b53a` (2026-09-16) |
| Pics et pelles — `pm_picks_and_shovels_building_phosphate_mine` | `picks_and_shovels.dds` | Équipement générique ; partage technique possible | F23:2 | `87d030e` (2026-09-09) |
| Aucune production de machines de précision — `pm_no_precision_machinery` | `no_automation.dds` | État désactivé générique ; peut rester partagé | F24:2 | `8e8794b` (2026-09-11) |
| Pompe à moteur atmosphérique — `pm_atmospheric_engine_pump_building_phosphate_mine` | `pumps.dds` | Équipement générique ; partage technique possible | F25:110 | `87d030e` (2026-09-09) |
| Pompe à moteur à condensation — `pm_condensing_engine_pump_building_phosphate_mine` | `condensing_engine_pump.dds` | Équipement générique ; partage technique possible | F25:140 | `87d030e` (2026-09-09) |
| Pompe Diesel — `pm_diesel_pump_building_phosphate_mine` | `diesel_pump.dds` | Équipement générique ; partage technique possible | F25:170 | `87d030e` (2026-09-09) |
| Nitroglycérine — `pm_nitroglycerin_building_phosphate_mine` | `nitroglycerin.dds` | Équipement générique ; partage technique possible | F25:200 | `87d030e` (2026-09-09) |
| Dynamite — `pm_dynamite_building_phosphate_mine` | `dynamite.dds` | Équipement générique ; partage technique possible | F25:231 | `87d030e` (2026-09-09) |
| Purification du sel — `pm_salt_purification_building_salt_mine` | `vaccum_evaporation.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F25:293 | `68a40ce` (2026-09-09) |
| Aucun approvisionnement médical organisé — `pm_no_organized_medical_supply` | `unused/no_pharmaceuticals.dds` | Unused conservée ; cohérence de famille à maintenir | F26:101 | `8e8794b` (2026-09-11) |
| Hôpitaux confessionnels — `pm_confessional_hospitals` | `field_hospitals.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F26:111 | `8e8794b` (2026-09-11) |
| Services de santé publique — `pm_public_health_services` | `pharmacies.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F26:166 | `8e8794b` (2026-09-11) |
| Verre pressé — `pm_pressed_glass` | `molds.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F27:4 | `a643882` (2026-09-11) |
| Absence de ventilation mécanique — `pm_no_mine_ventilation` | `unused/disabled.dds` | Unused conservée ; cohérence de famille à maintenir | F27:78 | `a643882` (2026-09-11) |
| Ventilation mécanique à vapeur — `pm_steam_mine_ventilation` | `pumps.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F27:83 | `a643882` (2026-09-11) |
| Ventilation électrique — `pm_electric_mine_ventilation` | `electric_engines.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F27:111 | `a643882` (2026-09-11) |
| Réfrigération à compression de vapeur — `pm_vapor_compression_refrigeration_building_livestock_ranch` | `refrigerated_storage.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F28:4 | `a643882` (2026-09-11) |
| Réfrigération à compression de vapeur — `pm_vapor_compression_refrigeration_building_fishing_wharf` | `refrigerated_storage.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F28:23 | `a643882` (2026-09-11) |
| Réfrigération à compression de vapeur — `pm_vapor_compression_refrigeration_building_whaling_station` | `refrigerated_storage.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F28:42 | `a643882` (2026-09-11) |
| Entraînement électrique individuel — `pm_unit_electric_drive_building_steel_mill` | `electric_engines.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F29:2 | `a643882` (2026-09-11) |
| Entraînement électrique individuel — `pm_unit_electric_drive_building_tooling_workshop` | `electric_engines.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F29:23 | `a643882` (2026-09-11) |
| Entraînement électrique individuel — `pm_unit_electric_drive_building_paper_mill` | `electric_engines.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F29:48 | `a643882` (2026-09-11) |
| Entraînement électrique individuel — `pm_unit_electric_drive_building_glassworks` | `electric_engines.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F29:73 | `a643882` (2026-09-11) |
| Entraînement électrique individuel — `pm_unit_electric_drive_building_motor_industry` | `electric_engines.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F29:98 | `a643882` (2026-09-11) |
| Sans organisation scientifique du travail — `pm_no_scientific_management` | `unused/no_org.dds` | Unused conservée ; état barré cohérent avec le nouvel état actif | F29:120 | `a643882` (2026-09-11) |
| Bureaux à tabulatrices — `pm_tabulating_offices` | `unused/census.dds` | Unused conservée ; cohérence de famille à maintenir | F30:2 | `a643882` (2026-09-11) |
| Pas d'impression mécanisée — `pm_no_printing_services` | `unused/disabled.dds` | Unused conservée ; cohérence de famille à maintenir | F30:37 | `a643882` (2026-09-11) |
| Composition mécanisée — `pm_mechanized_typesetting` | `unused/printing_presses.dds` | Unused conservée ; cohérence de famille à maintenir | F30:41 | `a643882` (2026-09-11) |
| Presse rotative — `pm_rotary_press` | `unused/newspapers.dds` | Unused conservée ; cohérence de famille à maintenir | F30:69 | `a643882` (2026-09-11) |
| Drainage des champs — `field_drainage_building_cotton_plantation` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:4 | `756e6c1` (2026-10-01) |
| Drainage des champs — `field_drainage_building_dye_plantation` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:20 | `756e6c1` (2026-10-01) |
| Drainage des champs — `field_drainage_building_opium_plantation` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:36 | `756e6c1` (2026-10-01) |
| Drainage des champs — `field_drainage_building_tea_plantation` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:52 | `756e6c1` (2026-10-01) |
| Drainage des champs — `field_drainage_building_tobacco_plantation` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:68 | `756e6c1` (2026-10-01) |
| Drainage des champs — `field_drainage_building_sugar_plantation` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:84 | `756e6c1` (2026-10-01) |
| Drainage des champs — `field_drainage_building_banana_plantation` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:105 | `756e6c1` (2026-10-01) |
| Drainage des champs — `field_drainage_building_silk_plantation` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:121 | `756e6c1` (2026-10-01) |
| Drainage des champs — `field_drainage_building_rubber_plantation` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:137 | `756e6c1` (2026-10-01) |
| Drainage des champs — `field_drainage_building_vineyard` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:153 | `756e6c1` (2026-10-01) |
| Drainage des champs — `pm_field_drainage_spice_cultivation` | `unused/maintained_sewers.dds` | Unused conservée ; cohérence de famille à maintenir | F31:169 | `756e6c1` (2026-10-01) |
| Pas de réseau de canaux — `pm_no_canal_network` | `unused/disabled.dds` | Unused conservée ; cohérence de famille à maintenir | F33:2 | `bf0b53a` (2026-09-16) |
| Canaux industriels — `pm_industrial_canals` | `canals.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F33:6 | `bf0b53a` (2026-09-16) |
| Canaux aménagés — `pm_engineered_canals` | `canals.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F33:35 | `bf0b53a` (2026-09-16) |
| Institutions commerciales du Rialto — `pm_default_building_rialto_commercial_complex` | `wonders.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F36:2 | `2c2ae7d` (2026-08-14) |
| Casa di San Giorgio — `pm_default_building_palazzo_san_giorgio` | `wonders.dds` | Vanilla réutilisée ; pas d'artwork propre au fork | F36:21 | `2c2ae7d` (2026-08-14) |
| Transport ferroviaire à vapeur — `pm_steam_rail_transport_building_rubber_plantation` | `rail_transport.dds` | Équipement générique ; partage technique possible | F37:2 | `bf0b53a` (2026-09-16) |

Priorités relevées lors de l'audit initial (liste historique, pas la file actuelle des lots) : ventilation des mines (pompe/moteur) ; conducteurs en aluminium (lampadaire) ; hauts-fourneaux au coke et procédé Thomas ; procédé Wöhler-Deville ; chambres de plomb et procédé Solvay ; blanchiment textile (papier) ; hôpitaux confessionnels et santé publique. Les procédés de ciment sont couverts en section 13, les machines-outils et la mouture en section 14. Les icônes `unused/` du drainage, des tabulatrices et des presses sont conservées ; l'organisation scientifique est corrigée en section 10. Les canaux et l'entraînement électrique doivent être examinés comme familles, pas écartés parce qu'ils ont un DDS.

## 2. Réemploi local des procédés de ciment — résolu

| PM | Image finale | Statut | Source |
| --- | --- | --- | --- |
| Ciment naturel — `pm_natural_cement_process` | `1776_natural_cement_process.dds` | Four à bois et pierres approuvés, intégrés | F17:2 |
| Ciment hydraulique — `pm_hydraulic_cement_process` | `1776_hydraulic_cement_process.dds` | Four vertical et goutte approuvés, intégrés | F17:30 |
| Ciment Portland — `pm_portland_cement_process` | `1776_portland_cement_process.dds` | Four industriel au charbon et meule approuvés, intégrés | F17:59 |

Les deux réemplois de concassage et le réemploi de moulage ont été remplacés après approbation. L'icône de concassage reste réservée au traitement du calcaire. L'organisation scientifique est documentée séparément en section 10.

## 3. PM vanilla réaffectés : ne pas se limiter aux nouveaux identifiants

| PM | Nom du procédé dans le jeu installé → nom dans le fork | Illustration actuelle | Décision d'inventaire | Source |
| --- | --- | --- | --- | --- |
| `pm_sewing_machines` | Machines à coudre → Machines à coudre industrielles | `sewing_machines.dds` | Reformulation ou évolution du même sujet ; pas de nouvel artwork manquant établi | [01_industry.txt:327](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt:327>) |
| `pm_craftsman_sewing` | Couture artisanale → Ateliers de confection artisanale | `craftsman_sewing.dds` | Reformulation ou évolution du même sujet ; pas de nouvel artwork manquant établi | [01_industry.txt:404](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt:404>) |
| `pm_elastics` | Tissu élastique → Textiles élastiques | `elastics.dds` | Reformulation ou évolution du même sujet ; pas de nouvel artwork manquant établi | [01_industry.txt:429](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt:429>) |
| `pm_mechanized_looms` | Métiers à tisser mécanisés → Métiers à tisser mécaniques | `mechanized_looms.dds` | Reformulation ou évolution du même sujet ; pas de nouvel artwork manquant établi | [01_industry.txt:464](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt:464>) |
| `pm_automatic_power_looms` | Métiers à tisser mécaniques automatiques → Métiers à tisser électriques automatisés | `automatic_power_looms.dds` | Reformulation ou évolution du même sujet ; pas de nouvel artwork manquant établi | [01_industry.txt:488](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt:488>) |
| `pm_leblanc_process` | Procédé Leblanc → Poudre noire | `leblanc_process.dds` | Sujet réaffecté : illustration dédiée à prévoir | [01_industry.txt:1386](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt:1386>) |
| `pm_ammonia-soda_process` | Procédé Solvay → Nitroglycérine | `ammonia_soda_process.dds` | Sujet réaffecté : illustration dédiée à prévoir | [01_industry.txt:1413](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt:1413>) |
| `pm_vacuum_evaporation` | Évaporation sous vide → Dynamite | `vaccum_evaporation.dds` | Sujet réaffecté : illustration dédiée à prévoir | [01_industry.txt:1444](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt:1444>) |
| `pm_brine_electrolysis` | Électrolyse de saumure → Poudre sans fumée | `vaccum_brine_electrolysis.dds` | Sujet réaffecté : illustration dédiée à prévoir | [01_industry.txt:1476](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt:1476>) |
| `pm_blister_steel_process` | Procédé de l’acier de cémentation → Puddlage et laminage | `blister_steel_process.dds` | Sujet réaffecté : illustration dédiée à prévoir | [01_industry.txt:1599](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt:1599>) |
| `pm_analytical_philosophy_department` | Département de philosophie analytique → Séminaires de philosophie analytique | `analytical_philosophy_department.dds` | Reformulation ou évolution du même sujet ; pas de nouvel artwork manquant établi | [07_government.txt:271](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/07_government.txt:271>) |
| `pm_simple_forestry` | Exploitation forestière simple → Exploitation forestière rudimentaire | `simple_forestry.dds` | Reformulation ou évolution du même sujet ; pas de nouvel artwork manquant établi | [09_misc_resource.txt:2](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/09_misc_resource.txt:2>) |
| `pm_arc_welded_buildings` | Bâtiments soudés à l’arc → Construction structurelle moderne | `arc_welded_buildings.dds` | Reformulation ou évolution du même sujet ; pas de nouvel artwork manquant établi | [13_construction.txt:117](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_construction.txt:117>) |

Les quatre procédés d'explosifs utilisent toujours les images de Leblanc, Solvay, évaporation et électrolyse malgré leurs noms Poudre noire, Nitroglycérine, Dynamite et Poudre sans fumée. `pm_blister_steel_process` est désormais Puddlage et laminage et se débloque par `puddling_and_rolling` : c'est un cinquième cas à ne pas masquer derrière un identifiant vanilla.

`pm_no_explosives_production`, également concerné par le précédent raccordement, reste le symbole natif `no_explosives.dds`. C'est un état générique « Prioriser la production d'engrais », sans bâtiment raccordé dans les groupes actuels ; il n'est pas compté comme nouveau procédé à illustrer. Le contrôle des types de biens produits n'a révélé en plus que le retrait d'une sortie teinture dans le PM rayon et l'ajout d'outils aux cinq variantes d'ateliers de subsistance : ces changements de recette ne constituent pas de nouveaux sujets d'icônes.

## 4. Tous les placeholders encore définis

Les noms réels des fichiers sont `gfx/error_deer.dds` (le cerf, appelé « error dir » dans la demande) et `gfx/error_manul.dds` (l'erreur manuelle). Il reste 20 références au premier et sept au second : 26 définitions d'objets et un glyphe d'interface, sans compter les simples mentions dans les rapports historiques.

### 4.1. Hors cuivre : cinq groupes de PM reliés à des bâtiments

| Groupe de PM | Bâtiments concernés | Source |
| --- | --- | --- |
| Réseau ferroviaire — `pmg_base_building_railway` | `building_railway` | [24_tech7a_wave_c_rail_pmgs.txt:2](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/24_tech7a_wave_c_rail_pmgs.txt:2>) |
| Services médicaux — `pmg_medical_services_building_urban_center` | `building_urban_center` | [17_tech6c8_pharmaceuticals_pmgs.txt:13](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/17_tech6c8_pharmaceuticals_pmgs.txt:13>) |
| Services d'impression — `pmg_printing_services` | `building_urban_center` | [21_tech6d_wave_e_pmgs.txt:2](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/21_tech6d_wave_e_pmgs.txt:2>) |
| Réseau routier — `pmg_base_building_land_transport_network` | `building_railway` | [22_tech7a_wave_a_land_transport_pmgs.txt:2](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/22_tech7a_wave_a_land_transport_pmgs.txt:2>) |
| Réseau de canaux — `pmg_land_transport_canals` | `building_railway` | [23_tech7a_wave_b_canals_pmgs.txt:2](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/23_tech7a_wave_b_canals_pmgs.txt:2>) |

Les infrastructures régionales cumulent donc encore les trois icônes de groupe Routes, Canaux et Rail. Les quatre PM routiers eux-mêmes ont déjà leurs textures locales : il ne faut pas régénérer leurs illustrations pour corriger ce problème de groupe.

### 4.2. Cuivre : quinze raccordements d'erreur

| Type | Identifiant | Texture | Source |
| --- | --- | --- | --- |
| PM | `pm_no_ore_concentration_building_copper_mine` | `gfx/error_deer.dds` | [13_tech6c5b_copper_production_and_consumers.txt:115](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt:115>) |
| PM | `pm_ore_concentration_building_copper_mine` | `gfx/error_deer.dds` | [13_tech6c5b_copper_production_and_consumers.txt:119](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt:119>) |
| PM | `pm_no_copper_sheathing_building_shipyard` | `gfx/error_deer.dds` | [13_tech6c5b_copper_production_and_consumers.txt:134](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt:134>) |
| PM | `pm_copper_sheathing_building_shipyard` | `gfx/error_deer.dds` | [13_tech6c5b_copper_production_and_consumers.txt:138](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt:138>) |
| PM | `pm_copper_conductors_building_power_plant` | `gfx/error_deer.dds` | [14_tech6c5c_aluminium_production_and_consumers.txt:150](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt:150>) |
| PMG | `pmg_mining_equipment_building_copper_mine` | `gfx/error_deer.dds` | [13_tech6c5b_copper_pmgs.txt:2](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/13_tech6c5b_copper_pmgs.txt:2>) |
| PMG | `pmg_explosives_building_copper_mine` | `gfx/error_deer.dds` | [13_tech6c5b_copper_pmgs.txt:12](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/13_tech6c5b_copper_pmgs.txt:12>) |
| PMG | `pmg_steam_automation_building_copper_mine` | `gfx/error_deer.dds` | [13_tech6c5b_copper_pmgs.txt:21](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/13_tech6c5b_copper_pmgs.txt:21>) |
| PMG | `pmg_train_automation_building_copper_mine` | `gfx/error_deer.dds` | [13_tech6c5b_copper_pmgs.txt:29](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/13_tech6c5b_copper_pmgs.txt:29>) |
| PMG | `pmg_ore_concentration_building_copper_mine` | `gfx/error_deer.dds` | [13_tech6c5b_copper_pmgs.txt:37](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/13_tech6c5b_copper_pmgs.txt:37>) |
| PMG | `pmg_copper_sheathing_building_shipyard` | `gfx/error_deer.dds` | [13_tech6c5b_copper_pmgs.txt:45](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/13_tech6c5b_copper_pmgs.txt:45>) |
| BUILDING | `building_copper_mine` | `gfx/error_deer.dds` | [13_tech6c5b_copper_mine.txt:3](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/buildings/13_tech6c5b_copper_mine.txt:3>) |
| GOOD | `copper` | `gfx/error_deer.dds` | [13_tech6c5b_copper.txt:2](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/goods/13_tech6c5b_copper.txt:2>) |
| TECH | `copper_sheathing` | `gfx/error_manul.dds` | [25_tech3a_naval.txt:111](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/25_tech3a_naval.txt:111>) |
| Glyphe de bien | `copper` | `gfx/error_deer.dds` | [gui/tech6c_goods_texticons.gui:65](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/gui/tech6c_goods_texticons.gui:65>) |

Cela comprend cinq PM, six groupes de PM, la mine, le bien, son petit glyphe et la technologie Doublage en cuivre. Les conducteurs en cuivre sont définis dans le fichier aluminium : une exclusion par nom de fichier seul aurait manqué ce cas.

### 4.3. Sept technologies hors cuivre non recherchables

| Technologie | Texture | Statut | Source |
| --- | --- | --- | --- |
| Turbines hydrauliques — `hydraulic_turbines` | `gfx/error_manul.dds` | `can_research = no` | [10_tech3a_production.txt:1051](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/10_tech3a_production.txt:1051>) |
| Verrerie traditionnelle — `traditional_glassmaking` | `gfx/error_manul.dds` | `can_research = no` | [10_tech3a_production.txt:1157](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/10_tech3a_production.txt:1157>) |
| Fusées mysoréennes — `mysorean_iron_cased_rocketry` | `gfx/error_manul.dds` | `can_research = no` | [20_tech3a_military.txt:156](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/20_tech3a_military.txt:156>) |
| Munitions explosives — `explosive_field_ammunition` | `gfx/error_manul.dds` | `can_research = no` | [20_tech3a_military.txt:243](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/20_tech3a_military.txt:243>) |
| Fusées militaires — `standardized_military_rockets` | `gfx/error_manul.dds` | `can_research = no` | [20_tech3a_military.txt:307](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/20_tech3a_military.txt:307>) |
| Savoirs codifiés — `codified_practical_knowledge` | `gfx/error_manul.dds` | `can_research = no` | [30_tech3a_society.txt:148](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/30_tech3a_society.txt:148>) |
| Établissements navals organisés — `organized_naval_establishments` | `gfx/error_deer.dds` | `can_research = no` | [99_tech_tree_wave1_structural_trunks.txt:16](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/99_tech_tree_wave1_structural_trunks.txt:16>) |

Ces sept entrées sont des alias de compatibilité ou des concepts neutralisés. Elles restent dans les fichiers et sont donc inventoriées ; elles ne sont pas traitées comme sept technologies actives à illustrer. `can_research = no` ne suffit pas, à lui seul, à prouver leur invisibilité dans toutes les interfaces : aucun contrôle en jeu n'a été fait.

## 5. Nouveaux PM possédant déjà une image locale

Les 64 raccordements locaux sont recensés pour éviter de refaire les sujets existants. L'absence de copie exacte d'une image vanilla ou d'erreur ne prouve pas la qualité artistique ni la conformité des couleurs : la passe de palette en section 15 ajoute des corrections à prévoir. Les partages d'une même famille sont indiqués ; les trois procédés de ciment et les trois PM du lot machines/mouture sont approuvés et intégrés.

| Texture locale | PM raccordés | Couverture |
| --- | --- | --- |
| `1776_precision_machine_tools.dds` | `pm_precision_machine_tools` | Machine manuelle, violet secondaire, lot 2 intégré |
| `1776_electrical_precision_machinery.dds` | `pm_electrical_precision_machinery` | Machine électrique, violet secondaire, lot 2 intégré |
| `1776_cylinder_flour_milling.dds` | `pm_cylinder_flour_milling` | Mouture à cylindres, vert automatisation, lot 2 intégré |
| `1776_engineered_road_network.dds` | `pm_engineered_road_network` | Image locale existante |
| `1776_fractional_distillation_refinery.dds` | `pm_fractional_distillation_refinery` | Image locale existante |
| `1776_laboratory_advanced.dds` | `pm_1776_advanced_research_laboratory` | Image locale existante |
| `1776_laboratory_electrical.dds` | `pm_1776_electrical_research_laboratory` | Image locale existante |
| `1776_laboratory_general.dds` | `pm_1776_general_research` | Image locale existante |
| `1776_laboratory_manual.dds` | `pm_1776_manual_research_laboratory` | Image locale existante |
| `1776_laboratory_military.dds` | `pm_1776_military_research` | Image locale existante |
| `1776_laboratory_production.dds` | `pm_1776_production_research` | Image locale existante |
| `1776_laboratory_society.dds` | `pm_1776_society_research` | Image locale existante |
| `1776_manual_ore_sorting.dds` | `pm_no_ore_concentration_building_bauxite_mine`, `pm_no_ore_concentration_building_coal_mine`, `pm_no_ore_concentration_building_gold_mine`, `pm_no_ore_concentration_building_iron_mine`, `pm_no_ore_concentration_building_lead_mine`, `pm_no_ore_concentration_building_phosphate_mine`, `pm_no_ore_concentration_building_sulfur_mine`, `pm_no_salt_processing_building_salt_mine` | Image de famille partagée |
| `1776_no_stone_processing.dds` | `pm_no_stone_processing_building_limestone_quarry` | Image locale existante |
| `1776_ore_concentration.dds` | `pm_ore_concentration_building_bauxite_mine`, `pm_ore_concentration_building_coal_mine`, `pm_ore_concentration_building_gold_mine`, `pm_ore_concentration_building_iron_mine`, `pm_ore_concentration_building_lead_mine`, `pm_ore_concentration_building_phosphate_mine`, `pm_ore_concentration_building_sulfur_mine` | Image de famille partagée |
| `1776_paved_road_network.dds` | `pm_paved_road_network` | Image locale existante |
| `1776_stone_crushing_screening.dds` | `pm_crushing_and_screening_building_limestone_quarry` | Concassage couvert |
| `1776_natural_cement_process.dds` | `pm_natural_cement_process` | Four à bois approuvé et intégré |
| `1776_hydraulic_cement_process.dds` | `pm_hydraulic_cement_process` | Four vertical approuvé et intégré |
| `1776_portland_cement_process.dds` | `pm_portland_cement_process` | Four industriel au charbon approuvé et intégré |
| `1776_thermal_catalytic_cracking_refinery.dds` | `pm_thermal_catalytic_cracking_refinery` | Image locale existante |
| `1776_traditional_road_network.dds` | `pm_traditional_road_network` | Image locale existante |
| `1776_turnpike_road_network.dds` | `pm_turnpike_road_network` | Image locale existante |
| `no_fine_food_preparations.dds` | `pm_no_spiced_food` | Image locale existante |
| `pm_aluminium_inox_houseware.dds` | `pm_aluminium_housewares` | Image locale existante |
| `pm_aluminium_passenger_carriages.dds` | `pm_aluminium_passenger_carriages` | Image locale existante |
| `pm_basic_smelting_process.dds` | `pm_basic_smelting_process` | Image locale existante |
| `pm_electric_arc_process_alloying.dds` | `pm_electric_arc_process_alloying` | Image locale existante |
| `pm_hall_heroult_process.dds` | `pm_hall_heroult_process` | Image locale existante |
| `pm_no_aluminium_production.dds` | `pm_no_aluminium_production` | Image locale existante |
| `preview_ef_private_pharmacies.dds` | `pm_private_pharmacies` | Image locale existante |
| `professional_faculties.dds` | `pm_professional_faculties` | Image locale existante |
| `refined_spiced_food_preparations.dds` | `pm_refined_spiced_food_preparations` | Image locale existante |
| `spiced_food_preparations.dds` | `pm_spiced_food_preparations` | Image locale existante |
| `tech_and_res_antibiotics_pharmaceuticals.dds` | `pm_antibiotic_mass_production` | Image locale existante |
| `tech_and_res_disabled.dds` | `pm_no_fertilizer_production`, `pm_no_industrial_chemicals`, `pm_no_pharmaceutical_production` | État désactivé générique partagé |
| `tech_and_res_manual_data_optimization.dds` | `pm_1776_administrative_data_reporting`, `pm_1776_institutional_data_reporting`, `pm_1776_trade_data_reporting` | Image de famille partagée |
| `tech_and_res_manual_data_reporting.dds` | `pm_1776_heavy_data_reporting`, `pm_1776_light_data_reporting`, `pm_1776_raw_data_reporting` | Image de famille partagée |
| `tech_and_res_no_data_reporting.dds` | `pm_1776_no_organized_data_reporting`, `pm_1776_no_raw_data_reporting` | État désactivé générique partagé |
| `tech_and_res_rudimental_chemical_pharmaceuticals.dds` | `pm_standardized_pharmaceuticals` | Image locale existante |
| `tech_and_res_synthetic_pharmaceuticals.dds` | `pm_synthetic_pharmaceuticals` | Image locale existante |

Le fichier `preview_ef_private_pharmacies.dds` est bien un asset local utilisé par le PM de pharmacies privées : le mot `preview` dans son nom n'est pas une preuve de placeholder. Aucune copie exacte d'icône vanilla ou d'erreur n'a été détectée parmi les 39 DDS locaux utilisés par les PM ; comparaison des fichiers et des pixels RGBA décodés avec 395 images natives/d'erreur, y compris le format BGRA sRGB de cette pharmacie.

## 6. Complément cuivre : six nouveaux PM encore sur des images vanilla

Ils sont hors du prochain lot non cuivre, mais font partie de l'inventaire complet.

| PM | Texture actuelle | Source |
| --- | --- | --- |
| `pm_atmospheric_engine_pump_building_copper_mine` | `pumps.dds` | [13_tech6c5b_copper_production_and_consumers.txt:17](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt:17>) |
| `pm_condensing_engine_pump_building_copper_mine` | `condensing_engine_pump.dds` | [13_tech6c5b_copper_production_and_consumers.txt:38](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt:38>) |
| `pm_diesel_pump_building_copper_mine` | `diesel_pump.dds` | [13_tech6c5b_copper_production_and_consumers.txt:59](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt:59>) |
| `pm_dynamite_building_copper_mine` | `dynamite.dds` | [13_tech6c5b_copper_production_and_consumers.txt:100](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt:100>) |
| `pm_nitroglycerin_building_copper_mine` | `nitroglycerin.dds` | [13_tech6c5b_copper_production_and_consumers.txt:80](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt:80>) |
| `pm_picks_and_shovels_building_copper_mine` | `picks_and_shovels.dds` | [13_tech6c5b_copper_production_and_consumers.txt:2](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt:2>) |

## 7. Méthode et limites

Comparaison des définitions locales avec le jeu installé dans `C:/Games/Victoria 3/game` ; 588 PM catalogués, dont 518 définis dans les fichiers du mod, et 436 identifiants vanilla. Les fichiers de même nom sont substitués et le dossier de technologies suit le `replace_path` du mod. Les ajouts sont recoupés avec tout l'historique Git courant, pas uniquement les deux derniers commits ; les dates dans les tables désignent la première apparition de la définition dans ce dépôt, pas la date de création de l'image.

Les groupes définis avec le préfixe `REPLACE_OR_CREATE:` sont résolus sous leur identifiant de jeu normal. C'est un mode de remplacement/création reconnu pour ces bases de données, et non un groupe orphelin. Référence primaire : [Paradox, Dev Diary 164 — Database Entry Modes](https://forum.paradoxplaza.com/forum/developer-diary/victoria-3-dev-diary-164-marvelous-modding-monday.1868975/). Les 152 nouveaux PM ont ainsi tous un chemin de raccordement bâtiment → groupe → PM. Cela ne garantit pas leur disponibilité à chaque date ou sous chaque loi.

Recherche exhaustive des chemins d'erreur dans les textes de `common`, `gfx`, `gui` et `.metadata`, hors commentaires et dossiers documentaires. Les textures ne sont pas jugées terminées sur la seule existence du fichier. L'inventaire initial était en lecture seule. La correction ultérieure de l'organisation scientifique crée une seule illustration, documentée en section 10 ; ses contrôles visuels restent dans `.asset-cache/`, ignoré par Git. Le présent rapport est mis à jour sans ajouter de rapports ou de déclinaisons d'image. Aucun Steam Build, portrait, stage, commit ou push n'a été modifié pendant cette passe.

## 8. Ajustements navals demandés pendant la passe

- `standardized_naval_signals` (« Signaux navals ») est accordée au départ à la France, la Grande-Bretagne, l'Espagne et la Russie, dans leurs quatre fichiers d'historique de pays.
- L'Espagne reçoit aussi `ship_classification_surveying` (« Classification des navires »), prérequis jusque-là absent. Le second prérequis indirect, `state_dockyard_systems`, était déjà présent dans les quatre pays.
- `building_whaling_station` retrouve `unlocking_technologies = { marine_chronometry }` dans `common/buildings/09_misc_resource.txt`. Avant cette modification, le bâtiment n'avait aucun verrou technologique.
- Aucune autre technologie de départ n'est ajoutée, notamment pas la chronométrie marine à l'Espagne ou à la Russie. L'ère de recherche des signaux, les lois et les PM navals restent inchangés. Les nouveaux octrois historiques demandent une nouvelle partie ; ils ne s'ajoutent pas automatiquement à une sauvegarde existante.

Justification historique : il s'agit ici de signaux par pavillons et de procédures convenues au sein des flottes, pas du code international moderne. Les archives du [Royal Museums Greenwich, collection Tunstall](https://www.rmg.co.uk/collections/archive/rmgc-object-492171) recensent des livres de signaux britanniques antérieurs à 1776, notamment de 1756 et 1760. La [Revista de Historia Naval, no 52, p. 66](https://armada.defensa.gob.es/archivo/mardigitalrevistas/rhn/1996/1996n52.pdf), publiée par l'Institut d'histoire et de culture navale de l'Armada espagnole, mentionne le recueil du marquis de la Victoria diffusé en septembre 1759. La notice du [musée d'Onega sur Artefact](https://ar.culture.ru/en/subject/kolokol-rynda), plateforme du ministère russe de la Culture, décrit les signaux par pavillons et autres moyens du règlement maritime de 1720. L'attribution commune aux quatre grandes flottes est donc un choix de modélisation cohérent avec ces pratiques, sans prétendre qu'elles partageaient déjà un code unique.

## 9. Routes régionales : coûts et petit complément de transport

| Méthode routière | Consommation de biens | Transport par niveau à plein emploi | Infrastructure fixe par niveau à plein emploi |
| --- | --- | ---: | ---: |
| Routes en terre — `pm_traditional_road_network` | Aucune : retrait des 5 bois ; salaires conservés | 0 | 3 |
| Routes à péage — `pm_turnpike_road_network` | Inchangée : 4 bois, 2 outils | 2 | 7 |
| Routes pavées — `pm_engineered_road_network` | Inchangée : 5 calcaire, 3 outils | 4 | 12 |
| Routes goudronnées — `pm_paved_road_network` | Inchangée : 4 outils, 5 ciment, 5 calcaire, 2 produits pétroliers lourds | 6 | 20 |

Les sorties de transport sont dans `building_modifiers.workforce_scaled`, comme celles des trains : elles diminuent avec l'emploi. Les quatre compositions d'effectifs, chacune totalisant 1 000 employés par niveau, les bonus d'infrastructure liés à la population et aux automobiles, les prérequis et les icônes sont conservés. Le complément maximal de 6 transports reste très inférieur aux 25 transports du PM de trains à vapeur actuellement défini dans le fork.

Contrôles statiques réussis lors de la passe navale/routière initiale : valeurs des quatre recettes, conservation exacte des autres contenus des six fichiers modifiés et de leur encodage, prérequis des signaux présents pour les quatre pays, absence de doublons d'octroi, verrou des ports baleiniers, équilibre des accolades et contrôle Git des espaces. Le test existant des permissions/du modèle de propriété des infrastructures régionales reste passant. L'audit effectué à ce stade confirmait des comptes d'icônes et de placeholders inchangés ; la comparaison des empreintes ne détectait que les six modifications de gameplay décrites ici. Les compteurs du présent rapport incluent maintenant la correction supplémentaire de la section 10. Aucun test en jeu n'a été réalisé.

## 10. Organisation scientifique : cohérence et effet cumulatif

### Icônes conservées et correction de famille

Les 19 nouveaux PM utilisant sept images `unused/` sont laissés tels quels : onze PM de drainage sur `maintained_sewers.dds` ; composition mécanisée sur `printing_presses.dds` ; presse rotative sur `newspapers.dds` ; tabulatrices sur `census.dds` ; trois états désactivés sur `disabled.dds` ; absence d'approvisionnement médical sur `no_pharmaceuticals.dds` ; absence d'organisation scientifique sur `no_org.dds`. Cette conservation ne transforme pas les autres références vanilla en obligations de création ; les familles doivent rester cohérentes.

L'état désactivé de l'organisation scientifique conserve les cinq étoiles mauves barrées de `unused/no_org.dds`. L'état actif utilise désormais les cinq étoiles dans leur cercle, sans barre, à la place de l'organigramme `simple_organization.dds`. La même image active est raccordée aux trois variantes (générale, automobile, électrique) et à leurs trois groupes, qui n'utilisent plus `gfx/error_deer.dds`. Les membres des groupes et leurs bâtiments consommateurs restent inchangés. L'outil de réparation des raccordements est actualisé pour conserver ce choix lors d'une prochaine passe.

### Recette et bonus

Pour les trois variantes, le bonus fixe `unscaled { building_throughput_add = 0.05 }` est remplacé par `level_scaled { building_throughput_add = 0.005 }` : **+0,5 % de débit par niveau construit**, soit +5 % à 10 niveaux, +10 % à 20 et +25 % à 50. Ce bonus porte sur le débit : il augmente les entrées et les sorties, ce n'est pas une réduction des intrants par unité produite.

La recette `workforce_scaled` ajoute `goods_input_organized_research_data_add = 1` : une donnée organisée par niveau à plein emploi, **avant les multiplicateurs de débit**. Les consommations de base de cinq papiers et dix services restent inchangées. Les variations d'effectifs restent −500 ouvriers, −250 machinistes, +500 employés et +250 ingénieurs par niveau. Le verrou `corporate_management` reste inchangé. Les données organisées et leur type de modificateur existent déjà dans le fork.

### Source, génération et régénération

- Source maîtresse unique : [1776_scientific_management_source.png](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/gfx/interface/icons/production_method_icons/1776_scientific_management_source.png>), 1254 × 1254 RGBA.
- Asset utilisé en jeu : [1776_scientific_management.dds](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/gfx/interface/icons/production_method_icons/1776_scientific_management.dds>), 208 × 208 BGRA8, huit mipmaps, 230 828 octets.
- Exporteur et contrôle : [build_scientific_management_icon.py](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/tools/build_scientific_management_icon.py>).

L'illustration a été produite avec la compétence `imagegen` et l'outil intégré, à partir de la texture native désactivée décodée sans modification (`C:/Games/Victoria 3/game/gfx/interface/icons/production_method_icons/unused/no_org.dds`). La référence de travail et la comparaison côte à côte sont temporaires et ignorées. Aucune déclinaison de qualité ou miniature n'est ajoutée au dépôt. L'outil a renvoyé un PNG réellement transparent malgré la demande de fond chroma ; le fichier maître est conservé directement, sans retouche de peinture ou de palette.

Prompt de génération utilisé :

```text
Use case: precise-object-edit. Asset type: Victoria 3 production-method UI icon. Input image 1 is the edit target: the shipped unused/no_org disabled symbol. Create its ENABLED counterpart. Remove ONLY the diagonal prohibition slash, reconstructing the portions of the stars beneath it. Preserve the circular outline and the SAME FIVE five-point stars, arranged exactly as in the reference (top centre; left; right; bottom-left; bottom-right), the mauve-purple/lavender palette, the understated beveled painted metal shading, and the composition and relative scale. Do not draw astronomy charts, people, factories, gears, letters or new decorations. The active and disabled symbols must look like a matched pair from the same UI set. All shapes opaque. Replace empty background and spaces between symbols with perfectly flat solid #00ff00 chroma key green, one uniform color, no gradient, no texture, no glow, no cast shadow, no floor. No green anywhere in the symbol. Square canvas, keep the complete emblem centered with about 10% padding around it, no cropping. No text, watermark, prohibition mark or slash.
```

Depuis la racine du dépôt, avec Python et Pillow disponibles :

```powershell
python tools/build_scientific_management_icon.py --export
python tools/build_scientific_management_icon.py
```

La première commande reconstruit uniquement ce DDS depuis le maître conservé ; la seconde contrôle sans écrire. L'export normalise seulement le format, le cadrage et le padding ; il ne régénère ni les images natives ni les définitions. Empreinte SHA-256 du DDS : `e7be9f8ff122d35a4004d1359ad08b06d8195f1ea6436fa126b8d5d8dc3ebd60`.

### Vérifications et limites

Contrôles ciblés réussis : trois recettes, effectifs et prérequis ; trois groupes correctement raccordés ; exemples aux niveaux 1, 10, 20 et 50 ; maître transparent ; format DDS, dimensions et huit mipmaps ; export reproductible octet pour octet ; bordures transparentes ; conservation exacte des autres contenus et de l'encodage des fichiers modifiés ; contrôle Git des espaces. L'audit des raccordements ne trouve aucune réparation restante ni texture absente hors cuivre. L'audit complet retrouve 152 nouveaux PM tous raccordés, 27 références d'erreur, 39 DDS locaux sans copie exacte d'une des 395 images natives/d'erreur contrôlées, et aucune erreur de décodage.

Le validateur historique `tools/tech8c_validate.cjs` n'est pas globalement passant : après 1 173 contrôles et 109 tests arithmétiques, il signale cinq écarts entre ses anciennes références et les bâtiments actuels : `15_tech6c6b_phosphate_mine.txt`, `12_tech6c4_oil_refinery.txt`, `11_private_infrastructure.txt`, `10_tech6c1_limestone_quarry.txt`, `09_misc_resource.txt`. Aucun de ces fichiers n'est modifié par la correction scientifique ou légale de cette section ; les références historiques ne sont pas écrasées pour masquer ces écarts. Aucun test en jeu n'est effectué, ni commit/push/Steam Build.

## 11. Esclavage colonial : déblocage par Colonisation

Dans [02_slavery.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/laws/02_slavery.txt:156>), le seul prérequis technologique de `law_colonial_slavery` passe de `human_rights` à `colonization`. La technologie Colonisation existe dans l'arbre du fork. Ce déplacement répond à la demande concernant la disponibilité des lois au démarrage ; il ne modifie pas les lois historiques des pays et ne leur accorde aucune technologie supplémentaire.

Les conditions territoriales, les actions d'activation, les poids politiques et toutes les autres lois d'esclavage sont inchangés. Les contrôles de la définition parsée et du diff exact à un seul identifiant réussissent ; l'encodage du fichier est préservé.

## 12. Complément des départs navals — Portugal, Pays-Bas et autres lois

Le Portugal (`POR`) et les Pays-Bas (`NET`) reçoivent `standardized_naval_signals` et son prérequis direct jusque-là absent, `ship_classification_surveying`. Le prérequis indirect `state_dockyard_systems` était déjà présent dans les deux pays. Leur loi `law_diplomatic_navy` est conservée ; aucune autre loi ou technologie de départ n'est changée.

L'audit des historiques de pays résolus, avec les fichiers locaux prioritaires sur ceux de même nom du jeu installé, relève deux lois demandant les signaux : `law_professional_navy` et `law_diplomatic_navy`. Après les deux octrois demandés, seuls le Danemark-Norvège (`DENNOR`), la Suède (`SWE`) et l'Empire ottoman (`TUR`) activaient encore une de ces lois sans posséder la technologie. Leur unique activation de `law_professional_navy` est remplacée par `law_merchant_navy` (Flotte marchande), sans octroi de technologie. Les pays sans aucune activation de ces lois ne sont pas modifiés. Les signaux déjà accordés à la France, à la Grande-Bretagne, à l'Espagne et à la Russie sont préservés.

Contrôles ciblés réussis : aucune activation navale explicitement définie sans signaux ne subsiste ; les octrois et remplacements sont uniques ; les prérequis des deux pays sont présents ; les autres contenus et l'encodage des cinq fichiers sont identiques à leur état avant cette passe. L'ensemble de `common/`, `gfx/` et `gui/` est comparé par empreinte : seuls ces cinq historiques changent, aucun fichier n'est ajouté ou supprimé dans ces dossiers. Contrôle Git des espaces passant. Ces départs nécessitent une nouvelle partie ; aucun test en jeu, commit, push ou Steam Build effectué.

## 13. Premier lot de trois PM de ciment — approuvé et intégré

Le joueur approuve la révision 2 avec « ok tu peut integré en passé au lot suivant ». Les textures de `pm_natural_cement_process`, `pm_hydraulic_cement_process` et `pm_portland_cement_process` sont remplacées par leurs trois exports dédiés. Seuls ces champs de texture et leurs commentaires provisoires changent dans les définitions ; recettes, pollution, emplois, déblocages et PMG restent identiques.

La première proposition, qui réutilisait le même four pour les trois PM, est refusée par le joueur. La révision 2 conserve les repères au premier plan — pierres, goutte et meule ronde à ouverture carrée — mais remplace chaque four par une silhouette différente : fourneau bas et simple à bois pour le ciment naturel, four vertical à chambre de chargement et renforts pour le ciment hydraulique, puis four industriel au charbon avec grande cheminée, trémie, grille et porte à cendres pour le ciment Portland. Les trois éditions sont générées par l'outil intégré `imagegen`, avec les premières images comme cibles d'édition. Pictogrammes ocre plats, grain fin mat, dégradé vertical et marges transparentes ; aucune scène ou cadre. La goutte est un repère graphique de prise hydraulique, pas l'affirmation que seul ce type de ciment peut durcir dans l'eau. Les PM des laboratoires, les icônes `unused/` retenues, les lots approuvés et le cuivre restent inchangés.

Références générales de la première proposition : [Historic England, fours à chaux préindustriels](https://historicengland.org.uk/images-books/publications/iha-preindustrial-lime-kilns/) et [four d'Aspdin](https://historicengland.org.uk/listing/the-list/list-entry/1004227). La progression visuelle de la révision 2 suit la demande du joueur ; ce sont des silhouettes schématiques, pas des relevés architecturaux. Comparaison de style avec les PM natifs Bessemer/four à sole et les pictogrammes plats déjà approuvés de concassage/raffinage. Le bois du premier four est uniquement un choix visuel demandé : aucune recette de consommation n'est modifiée par cette révision.

Les trois masters approuvés 1254 × 1254 RGBA sont conservés sans modification artistique dans `docs/reports/assets/pm_cement_sources_2026-10-07/`, avec un seul `manifest.json` réunissant les prompts, l'approbation, les empreintes et les paramètres de cadrage/export. Aucun master abandonné, miniature par taille ou DDS candidat n'est copié dans le dépôt. Les trois DDS de jeu sont en 208 × 208 BGRA8 legacy A8R8G8B8 avec huit mipmaps. Les contrôles, décodages et la planche unique restent dans `.asset-cache/pm_batch_1_cement_2026-10-07/`, ignoré par Git.

Le registre commun contient les trois nouvelles recettes d'export. `tools/rebuild_asset_icons.cjs --verify` confirme une reconstruction identique octet pour octet pour les 114 entrées. Son installation explicite exige une sélection unique et une empreinte d'export approuvée ; les modes de vérification et de cache restent sans écriture dans le jeu. L'audit des raccordements est actualisé pour ne pas restaurer les anciennes images de concassage/moulage. Contrôles DDS, alpha, marges, PMG et identité des définitions hors textures réussis : un fichier de définition modifié et trois DDS ajoutés seulement dans `common/`, `gfx/`, `gui/`. Aucun test moteur, commit, push ou Steam Build effectué.

## 14. Deuxième lot de trois PM — approuvé et intégré

| PM | Texture de jeu dédiée | Palette et sujet |
| --- | --- | --- |
| `pm_precision_machine_tools` | `1776_precision_machine_tools.dds` | Violet secondaire ; machine à tailler les engrenages, manivelle |
| `pm_electrical_precision_machinery` | `1776_electrical_precision_machinery.dds` | Violet secondaire ; même mécanisme, moteur électrique |
| `pm_cylinder_flour_milling` | `1776_cylinder_flour_milling.dds` | Vert automatisation ; deux rouleaux en coupe, trémie et épi |

Génération par l'outil intégré `imagegen`. La machine manuelle reprend les références de machine à tailler les engrenages déjà fournies par le joueur ; une correction enlève le relief de la première ébauche, et la variante électrique dérive ensuite de la base plate. La mouture montre des rouleaux, pas la meule traditionnelle de l'illustration de technologie existante. Ce sont des glyphes schématiques : [Winterthur, machine à tailler les roues](https://dominycollections.winterthur.org/tools-of-the-trade/clockmaking-shop/engine/) et [Science Museum Group, machine de 1751](https://collection.sciencemuseumgroup.org.uk/objects/co484251/large-wheel-engine-used-to-cut-the-teeth-of-clocks) étayent le principe du mécanisme manuel ; [Science Museum Group, moulin à rouleaux de 1899–1909](https://collection.sciencemuseumgroup.org.uk/objects/co154218/roller-mill-flour-mill-with-rolls-ipswich-1899-1909) et [Minnesota Historical Society, description historique de la mouture](https://www.mnhs.org/forestsfieldsfalls/flourmilling/flourmilling-fulltext) étayent celui des cylindres. Aucun relevé de modèle exact ni reproduction de photographie de musée n'est revendiqué.

Approbation reçue avec la condition de corriger le code couleur. Trois éditions artistiques par imagegen conservent les silhouettes et passent les deux machines en violet (`pmg_precision_machinery_production`, groupe secondaire), la mouture en vert (`pmg_automation_building_food_industry`). Les trois masters finaux 1254 × 1254 RGBA seulement, leurs prompts et les paramètres d'export sont conservés dans `pm_machinery_sources_2026-10-07/manifest.json` ; aucune déclinaison miniature ou ancienne palette n'est versionnée. DDS 208 × 208 BGRA8 legacy avec huit mipmaps, alpha et décodages contrôlés. Les 117 recettes du registre se reconstruisent octet pour octet.

Contrôle d'intégration : deux fichiers de PM changés uniquement sur trois textures, trois DDS ajoutés, aucun autre changement à `common/`, `gfx/`, `gui/` depuis le début de ce lot. Recettes, états désactivés, laboratoires, chaîne du cuivre et icônes `unused/` retenues inchangés. L'audit de raccordement conserve les nouvelles textures dédiées. La recette électrique reste inchangée même si elle consomme du cuivre. Les contrôles et l'unique planche restent dans `.asset-cache/pm_batch_2_machinery_2026-10-07/`, ignoré. Aucun test en jeu, commit, push ou Steam Build.

## 15. Code couleur par groupe et passe élargie

Le contrat `pm_palette_rules.json` et l'audit en lecture seule `tools/audit_pm_group_palette.py` remplacent l'hypothèse « tout ocre ». Références natives inspectées localement, puis décisions du joueur demandées pour les groupes ambigus :

| Famille | Palette |
| --- | --- |
| Production standard ; routes et réseau ferroviaire | Jaune/beige |
| Automatisation, dont ventilation et entraînement individuel | Vert olive |
| Productions secondaires ; concassage, concentration des minerais, sel | Violet |
| Organisation du personnel | Bleu |
| Organisation scientifique | Violet, constellation |
| Canaux ; groupes militaires personnalisés | Rouge |
| Services médicaux | Vert bleuté, distinct du vert olive |
| Services d'imprimerie | Blanc |

La distillation garde ses glyphes natifs blancs/gris ; son ancienne flèche de groupe violette ne doit pas faire recolorer ses PM. Le jaune des trains désigne ici le groupe de production du réseau ferroviaire : le transport de matières en tant qu'automatisation d'une mine reste dans sa famille verte native.

214 groupes utilisés par des bâtiments et pertinents pour les définitions locales examinés. Après les réponses du joueur, aucun de ces groupes hors exclusions ne reste sans palette définie. **Ce n'est pas une déclaration de conformité de toutes les textures actuelles.** Le tri des pixels signale 54 identifiants nouveaux ou utilisant une image locale à revoir, hors `unused/` protégées : 9 automatisation, 2 canaux, 3 médical, 18 préparation, 16 production, 6 secondaire. Les partages réduisent le nombre d'images à corriger ; ces nombres sont une file de contrôle heuristique, pas 54 commandes de génération. Les cinq groupes hors cuivre encore sur le cerf d'erreur sont également suivis. Les sept anciens PM de laboratoire, le cuivre et les `unused/` retenues sont protégés. Les corrections se poursuivent par lots de trois avec preview avant intégration ; ne pas recolorer globalement un fichier vanilla partagé.

Les trois PM du lot 2 correspondent à leur palette attendue. JSON détaillé et référence native de comparaison dans `.asset-cache/pm_palette_2026-10-07/` seulement. Le contrôle des chemins d'icônes n'a aucune réparation ni fichier manquant dans son périmètre, mais ne valide pas les sujets ou les couleurs restantes.

## 16. Troisième lot — automatisation verte, approuvé et intégré

| Icône intégrée | PM destinataires | Bâtiments |
| --- | --- | --- |
| Ventilation à vapeur, ventilateur + machine à vapeur | `pm_steam_mine_ventilation` et variante bauxite | Mines dotées du groupe de ventilation |
| Ventilation électrique, même principe + moteur | `pm_electric_mine_ventilation` et variante bauxite | Mêmes mines |
| Entraînement électrique individuel, moteur ouvert + courroie + marteau de forge | Les cinq `pm_unit_electric_drive_building_*` | Aciéries, ateliers d'outillage, papeteries, verreries, industries des moteurs |

Trois images peuvent ainsi couvrir neuf définitions de PM, sans confondre un ventilateur et un moteur d'entraînement. Le principe de ventilation est étayé par [Historic England, ventilateurs à vapeur puis électriques de Skelton](https://historicengland.org.uk/listing/the-list/list-entry/1420051) ; celui du moteur individuel par [Science Museum Group, moteur entraînant un tour](https://collection.sciencemuseumgroup.org.uk/objects/co8414626/electric-motor). Il s'agit de concepts schématiques, pas de reproductions exactes des machines conservées.

Le joueur rejette le moteur moderne et la roue dentée, puis demande un moteur ouvert de fin du XIXe siècle avec bobinages visibles, entraînant un marteau mécanique par courroie. Une retouche ciblée remonte le brin supérieur à la poulie du moteur. Cette version et les deux ventilations sont ensuite explicitement approuvées. Génération et retouche par imagegen, vert olive, grain mat, compositions plates, transparence réelle. Aucun moteur ou marteau de musée n'est reproduit exactement : le concept de moteur ancien est étayé par le [catalogue Crocker-Wheeler vers 1890 conservé par The Henry Ford](https://www.thehenryford.org/collections/explore/artifact/31897?AssetId=THF285896). La [notice du musée de Příbram](https://www.muzeum-pribram.cz/wp-content/uploads/2021/10/The-Tour-site-C.pdf) décrit un marteau mécanique de fin XIXe entraîné par courroie, avec un moteur conservé plus tardif ; elle ne date pas notre combinaison exacte.

Trois masters finaux seulement et leurs prompts conservés dans `pm_automation_sources_2026-10-07/manifest.json`. DDS `1776_steam_mine_ventilation`, `1776_electric_mine_ventilation` et `1776_unit_electric_drive` en 208 × 208 BGRA8 legacy, huit mipmaps. Neuf références de texture remplacées dans trois fichiers de PM ; contrôle des tokens hors texture identique, aucune recette modifiée. Transparence, marges, appartenance aux PMG et reconstruction exacte des 120 entrées du registre contrôlées. L'audit de raccordement est actualisé pour conserver ces nouveaux chemins. Contrôles et unique planche dans `.asset-cache/pm_batch_3_automation_2026-10-07/` seulement. Aucun test en jeu, commit, push ou Steam Build.

Après ce lot, la même passe de couleur examine toujours 214 groupes, sans palette inconnue dans le périmètre : la file heuristique des identifiants nouveaux ou utilisant une texture locale passe de 54 à 45, les neuf PM d'automatisation étant corrigés. Les autres écarts et les cinq placeholders de groupe hors cuivre restent à traiter par lots ; les réemplois `unused/` retenus et les laboratoires sont préservés.

## 17. Quatrième lot — services médicaux, approuvé et intégré

| PM proposé | Glyphes | Palette |
| --- | --- | --- |
| `pm_confessional_hospitals` | Fenêtre de chapelle et croix latine, lit d'hôpital | Vert bleuté |
| `pm_private_pharmacies` | Tas irrégulier de pièces de monnaie, flacon de médicament | Vert bleuté |
| `pm_public_health_services` | Croix médicale droite et caducée ailé à deux serpents légèrement incliné, superposés en un seul glyphe | Vert bleuté |

Génération par l'outil intégré imagegen : pictogrammes plats, grain mat, dégradé vertical et transparence réelle, pas de scène médicale réaliste. La palette vert bleuté est celle explicitement choisie par le joueur pour les services médicaux, distincte du vert olive d'automatisation. Recettes, lois et identifiants inchangés. L'état désactivé `pm_no_organized_medical_supply` garde l'icône native `unused/no_pharmaceuticals.dds`.

Révision 2 demandée par le joueur : hôpitaux confessionnels approuvés et source strictement conservée ; pour le privé, le mortier est remplacé par des pièces afin de rendre le paiement immédiatement visible tout en gardant le flacon ; pour le public, seul le registre est remplacé par le bâton d'Hermès/caducée ailé à deux serpents, la croix médicale est conservée. Deux symboles principaux par icône, même vert bleuté. Retouches ciblées par imagegen, ensuite remplacées par les révisions ci-dessous.

Révision 3 demandée par le joueur : les pièces du privé sont décalées, inclinées et partiellement superposées pour former un petit tas désordonné, sans pile verticale régulière ; le caducée public est centré et superposé à la croix pour former un glyphe compact unique. Hôpitaux confessionnels toujours strictement inchangés. Cette version privée est la source finale approuvée ; le public reçoit encore la retouche ci-dessous.

Révision 4 : le joueur approuve le privé. Sa source de révision 3 et celle des hôpitaux confessionnels sont conservées sans régénération. Seul le caducée public est incliné légèrement par rapport à la croix, qui reste droite, afin de différencier les deux formes à petite taille. Retouche ciblée par imagegen, nouveau contrôle 32/48/64 px sur deux fonds. Le joueur approuve ensuite tout le lot : « Ok, tu peux intégrer le tout et passer au lot suivant. »

Les trois masters finaux seulement sont conservés dans `pm_medical_sources_2026-10-07/`, avec leurs prompts et paramètres dans le manifeste. Trois DDS 208 × 208 BGRA8 legacy avec huit mipmaps sont intégrés : `1776_confessional_hospitals`, `1776_private_pharmacies`, `1776_public_health_services`. Le groupe médical reprend la santé publique à la place de `gfx/error_deer.dds`, sans quatrième asset. Quatre références de texture dans deux fichiers seulement ; comparaison des tokens hors texture identique, recettes, lois et état désactivé native `unused/` inchangés. Reconstruction exacte des 123 exports, raccordements, transparence et préservation du cuivre et des sept PM de laboratoire vérifiés. QA et planches restent dans `.asset-cache/pm_batch_4_medical_2026-10-07/`, ignoré par Git. Aucun test en jeu, commit, push ou Steam Build.

Après intégration médicale, la file heuristique des identifiants nouveaux ou utilisant une texture locale passe de 45 à 42, sans palette inconnue sur les 214 groupes examinés. Quatre placeholders de groupe hors cuivre subsistent : routes, rail, canaux, imprimerie. Les réemplois natifs `unused/` déjà retenus ne sont pas régénérés.

## 18. Cinquième lot — préparation des matières, approuvé et intégré

| Proposition | Glyphes | Palette |
| --- | --- | --- |
| Tri manuel, sans concentration supplémentaire | Main sélectionnant une roche parmi des morceaux anguleux | Violet des productions secondaires |
| Concentration des minerais | Tamis rectangulaire, gros morceaux au-dessus et morceaux sélectionnés en dessous | Même violet |
| Purification du sel | Bassin d'évaporation et petit groupe de cristaux, composition compacte | Même violet |

Les deux premiers motifs existants sont conservés et retouchés uniquement pour corriger leur palette ocre. La purification reçoit un glyphe dédié au lieu du réemploi vanilla `vaccum_evaporation.dds` ; les autres consommateurs de cette icône native ne sont pas modifiés. La famille de préparation adopte le violet explicitement choisi par le joueur. Glyphes conceptuels, non reconstruction d'un appareil historique précis : formes plates, grain mat, dégradé vertical discret et transparence réelle, aucune scène réaliste.

Approbation reçue : « Ok, tu peux intégrer le lot et passer au lot suivant. » Seize raccordements sont couverts : huit PM d'état manuel, sept PM de concentration hors cuivre, un PM de purification du sel. Les deux DDS existants `1776_manual_ore_sorting.dds` et `1776_ore_concentration.dds` sont remplacés en place ; `1776_salt_purification.dds` est ajouté et seul le champ de texture du PM de purification change. Cuivre, sept PM de laboratoire et réemplois natifs `unused/` retenus restent protégés. Trois masters finaux seulement et leurs prompts/paramètres sont conservés dans `pm_preparation_sources_2026-10-07/manifest.json`. Les contrôles et l'unique planche restent dans `.asset-cache/pm_batch_5_mine_processing_2026-10-07/`, ignoré par Git. La référence d'empreintes est capturée après l'intégration médicale.

La purification est recomposée en carré puis ses cristaux sont aplatis et son violet harmonisé par retouches ciblées imagegen. Trois masters finaux 1254 × 1254 RGBA, alpha 0–255 avec coins transparents ; contrôle visuel 32/48/64 px sur fonds sombre et clair et damier. La phase de proposition avait le statut `PASS_STATIC_PREVIEW_ONLY`, sans changement de `common/`, `gfx/`, `gui/` avant approbation. L'intégration a ensuite le statut `PASS_STATIC_PREPARATION_INTEGRATION` : recettes inchangées, exactement un fichier de PM et deux DDS existants modifiés, un DDS ajouté ; format 208 × 208 BGRA8 legacy, huit mipmaps et transparence contrôlés. Les 124 exports du registre se reconstruisent octet pour octet ; aucune réparation de raccordement ni texture absente dans le périmètre audité hors cuivre. L'audit de palette n'a aucun groupe inconnu et relève encore 26 nouveaux identifiants ou textures locales à revoir. Aucun test en jeu, commit, push ou Steam Build.

## 19. Sixième lot — aluminium, recoloration seulement, approuvé et intégré

Le joueur rappelle que la chaîne possède déjà ses images, puis précise : « juste changer les couleurs, pas régénérer les assets ». Les copies locales de `pm_no_aluminium_production.dds` et `pm_hall_heroult_process.dds` sont effectivement identiques octet pour octet aux fichiers du mod Tech & Res installé (Workshop `3472248460`). Wöhler–Deville utilise `blister_steel_process.dds`, exactement comme dans les définitions Tech & Res. Il ne manque donc aucun fichier pour ces trois PM. La piste de nouveaux motifs est abandonnée ; l'ébauche générée avant l'interruption n'est ni retenue ni intégrée.

Une harmonisation chromatique est néanmoins justifiée : `pmg_aluminiummaking_process` utilise `mixed_icon_refining.dds`, donc le violet secondaire, alors que ses trois membres étaient ocre. Le lot reprend strictement leurs images existantes :

| PM | Source conservée | Intervention intégrée |
| --- | --- | --- |
| `pm_no_aluminium_production` | État barré Tech & Res, 208 × 208 | Teinte et saturation violettes uniquement |
| `pm_wohler_deville_process` | Four vanilla, 104 × 104 | Même recoloration, sans remplacer le fichier vanilla partagé |
| `pm_hall_heroult_process` | Cuve Tech & Res, 256 × 256 | Même recoloration |

Le traitement est déterministe, sans IA ni redessin, par `tools/recolour_pm_icons.py`. Il décale la teinte et ajuste la saturation vers la référence violette native `craftsman_sewing.dds`, sans modifier les dimensions, le cadrage, les positions ou l'alpha d'un seul pixel. La valeur HSV de chaque pixel reste exacte : relief/contours/grain existants ne sont pas refaits. Les pixels totalement transparents sont inchangés. Pendant la proposition, les fichiers Tech & Res ayant une signature PNG malgré leur extension DDS étaient lus tels quels. L'intégration les exporte en véritables DDS, sans changement des pixels du niveau principal par rapport aux masters approuvés.

La proposition avait le statut `PASS_COLOUR_ONLY_PREVIEW`, sans modification de `common/`, `gfx/`, `gui/` avant approbation. Le joueur demande ensuite de passer au lot suivant. Les trois masters finaux et leurs paramètres/empreintes sont conservés dans `pm_aluminium_colour_sources_2026-10-07/manifest.json`. Une seule planche de comparaison et les contrôles intermédiaires restent dans `.asset-cache/pm_batch_6_aluminium_colour_only_2026-10-07/`, ignoré par Git.

L'intégration a le statut `PASS_COLOUR_ONLY_INTEGRATION` : deux DDS remplacés en place et le DDS local distinct `1776_wohler_deville_process.dds` ajouté ; seul le champ de texture du PM Wöhler–Deville change. Le fichier vanilla partagé reste intact. Dimensions natives 208, 104 et 256 pixels conservées, respectivement huit, sept et neuf mipmaps BGRA8 legacy ; niveau principal exactement égal aux masters RGBA. Recettes, emplois, déblocages et groupes inchangés ; cuivre et sept PM de laboratoire protégés. Les 127 exports du registre se reconstruisent octet pour octet. L'audit des raccordements ne relève aucune réparation requise ni texture absente dans son périmètre ; l'audit de palette relève encore 23 nouveaux identifiants ou textures locales à revoir, sans groupe inconnu. Aucun test en jeu, commit, push ou Steam Build.

## 20. Septième lot — procédés industriels, approuvé et intégré

Trois réemplois dont le sujet ne distingue pas suffisamment le procédé ont reçu leurs pictogrammes dédiés. Tous appartiennent à des groupes de production de base utilisant `mixed_icon_base.dds` : palette jaune/beige, et non vert d'automatisation ou violet secondaire.

| PM | Image actuelle | Proposition |
| --- | --- | --- |
| Verre pressé — `pm_pressed_glass` | `molds.dds` | Presse manuelle à levier avec piston aligné sur un moule ouvert |
| Blanchiment chimique des textiles — `pm_chemical_bleaching_textile_mill` | `bleached_paper.dds` | Cuve avec une bande de tissu drapée et un petit flacon chimique |
| Procédé Solvay — `pm_solvay_process_building_chemical_works` | `vaccum_evaporation.dds` | Colonne de traitement reliée à une cuve basse |

Le principe du verre pressé, piston appliqué au verre dans un moule métallique, est documenté par le [Corning Museum of Glass](https://allaboutglass.cmog.org/glass-dictionary/p). Le motif cuve/tissu s'appuie sur une [gravure de blanchiment de 1804 conservée par Wellcome](https://wellcomecollection.org/works/ktrrfwwr) ; le flacon est un symbole de traitement chimique, pas la reproduction d'un appareil de cette gravure. La colonne Solvay est un raccourci graphique du traitement gaz/liquide décrit dans le [support de la Royal Society of Chemistry](https://edu.rsc.org/download?ac=15610), non une reconstruction technique exacte.

Génération intégrée `imagegen`, trois PNG RGBA 1254 × 1254, coins transparents et alpha 0–255. Style pictogramme simplifié jaune/beige, grain mat discret, contours graphiques et dégradé vertical ; pas de scène d'usine, texte ou schéma détaillé. Après l'approbation « Je valide, tu peux passer au prochain lot et intégrer celui-là », les trois originaux sont copiés sans modification artistique dans `pm_industrial_process_sources_2026-10-07/`, avec les prompts complets, références, approbation et paramètres dans `manifest.json`. Les dérivés de contrôle restent dans le cache ignoré par Git.

La proposition avait le statut `PASS_STATIC_PREVIEW_ONLY`, avec contrôle visuel en grand, à 32/48/64 pixels sur fonds sombre et clair et sur damier ; aucune texture ni définition n'était modifiée avant approbation. L'intégration a ensuite le statut `PASS_STATIC_INDUSTRIAL_PROCESS_INTEGRATION` : exactement deux fichiers de PM modifiés, uniquement trois références de texture, et trois DDS ajoutés. Noms finaux : `1776_pressed_glass_pm.dds`, `1776_textile_bleaching.dds`, `1776_solvay_process.dds`. Le suffixe `_pm` évite toute ambiguïté avec la technologie Verre pressé déjà enregistrée. Aucun fichier vanilla partagé ou asset de technologie n'est remplacé.

Les trois exports sont des DDS BGRA8 legacy de 208 × 208 avec huit mipmaps et coins transparents ; décodage indépendant et contrôle visuel réalisés. Les 130 exports du registre se reconstruisent octet pour octet. Les recettes, emplois, déblocages et groupes restent identiques ; cuivre et sept PM de laboratoire protégés. L'audit des raccordements ne relève ni réparation requise ni texture absente dans son périmètre. L'audit chromatique conserve 22 nouveaux identifiants ou textures locales à revoir et aucun groupe inconnu. Aucun test en jeu, commit, push ou Steam Build.

## 21. Huitième lot — sidérurgie intégrée après validation

Le groupe réel `pmg_steelmaking_process` utilise `mixed_icon_base.dds` : jaune/beige de production. Trois procédés actuellement difficiles à distinguer par leurs réemplois sont proposés, sans toucher à l'icône native du procédé Bessemer ni aux autres consommateurs des fichiers partagés.

| PM | Réemploi actuel | Proposition |
| --- | --- | --- |
| Hauts-fourneaux au coke — `pm_coke_blast_furnaces` | `blister_steel_process.dds`, partagé avec le puddlage | Four vertical effilé, tuyère latérale et petit groupe de coke |
| Puddlage et laminage — `pm_blister_steel_process` | `blister_steel_process.dds`, ancien sujet de cémentation | Four bas, tige de brassage dans le foyer et paire de rouleaux |
| Procédé Thomas — `pm_thomas_process` | `bessemer_process.dds`, partagé avec Bessemer | Convertisseur incliné, bordure de revêtement et petit groupe de calcaire |

Il s'agit de raccourcis graphiques, pas de plans d'installations historiques exactes. La notice du [haut-fourneau au coke de Bedlam, Historic England](https://historicengland.org.uk/education/schools-resources/educational-images/the-bedlam-furnace-ironbridge-telford-and-wrekin-ioe01-08734-02) documente cette famille de four. Le brassage par une tige et le passage entre deux rouleaux s'appuient sur la [présentation des NorthLan Museums](https://www.northlanmuseums.co.uk/story/puddlers-shinglers-rollers-the-story-of-malleable-iron/). Le revêtement du convertisseur est le trait distinctif décrit par la [documentation du site patrimonial de Blaenavon](https://www.visitblaenavon.co.uk/assets/documents/world-heritage-site/The-Blaenavon-Story/Gilchrist-Thomas.pdf) ; le calcaire reprend aussi l'ingrédient déjà présent dans la recette du PM, sans modification de cette recette.

Génération intégrée `imagegen`, trois masters 1254 × 1254 RGBA, alpha 0–255 et coins transparents. Pictogrammes simplifiés à grain fin mat, dégradé vertical jaune/beige et contours bruns graphiques ; aucun texte, cadre ou scène d'aciérie. Deux sujets principaux au maximum par proposition, les pièces du même appareil faisant un seul sujet. Après l'approbation « Je valide, tu peux intégrer, passer au le suivant. », les trois masters ont été copiés sans changement artistique dans `docs/reports/assets/pm_steelmaking_sources_2026-10-07/`. Le manifeste conserve les prompts complets, références, empreintes et paramètres d'export. Une seule planche et les diagnostics restent dans le cache ignoré par Git.

La validation d'intégration obtient `PASS_STATIC_STEELMAKING_INTEGRATION` : exactement un fichier de PM modifié, uniquement trois références de texture, et trois DDS ajoutés. Noms finaux : `1776_coke_blast_furnaces_pm.dds`, `1776_puddling_and_rolling_pm.dds`, `1776_thomas_process_pm.dds`. Les fichiers vanilla partagés restent intacts. DDS BGRA8 legacy 208 × 208, huit mipmaps et coins transparents ; décodage indépendant et contrôle visuel réalisés. Les 133 exports du registre se reconstruisent octet pour octet. Recettes, emplois, déblocages et groupes inchangés dans ce lot ; cuivre et sept anciens PM de laboratoire protégés. Audit des raccordements : aucune réparation requise ni texture absente dans son périmètre. Aucun test en jeu, commit, push ou Steam Build.

## 22. Neuvième lot — explosifs intégrés après validation

Les noms français effectifs des trois PM ne correspondent plus aux procédés chimiques portés par leurs anciens identifiants vanilla. Leur groupe `pmg_explosives_building_chemical_plant` utilise `mixed_icon_base.dds` : jaune/beige de production, et non rouge militaire.

| PM affiché | Texture actuelle | Proposition |
| --- | --- | --- |
| Poudre noire — `pm_leblanc_process` | `leblanc_process.dds` | Nouvelle icône : tonneau de poudre et étoile d'explosion graphique |
| Nitroglycérine — `pm_ammonia-soda_process` | `ammonia_soda_process.dds` | Raccordement à l'icône native `nitroglycerin.dds` : goutte et étoile d'explosion |
| Dynamite — `pm_vacuum_evaporation` | `vaccum_evaporation.dds` | Raccordement à l'icône native `dynamite.dds` : cartouches liées |

Seule la poudre noire a été générée avec l'outil intégré `imagegen`. Les deux autres dessins existent déjà, correspondent au sujet et à la famille chromatique : aucune régénération, recoloration, copie dans `gfx/` ni modification des DDS vanilla. Leurs fichiers sources natifs sont les `production_method_icons/nitroglycerin.dds` et `production_method_icons/dynamite.dds` de `C:/Games/Victoria 3/game/gfx/interface/icons/`, 104 × 104 et sept mipmaps.

Master final de poudre noire : `docs/reports/assets/pm_explosives_sources_2026-10-07/black_powder.png`, copié sans modification artistique après l'approbation « Ok, tu peux passer au prochain lot et intégrer celui-là. ». PNG 1254 × 1254 RGBA, alpha 0–255, SHA-256 `d4d9e14d31ee60d4c9995f1ab50dec596a96ce9887bd7cb59302ef2d8ffdba17`. Deux symboles principaux maximum, grain fin mat et dégradé graphique jaune/beige ; raccourci d'interface, sans recette ou plan technique. Le manifeste de ce dossier conserve le prompt intégral, les références, l'approbation et les paramètres d'export.

Une seule planche `lot_9.png`, inspection visuelle et contrôles à 32/48/64 pixels, fonds clair/sombre et damier, puis décodage des fichiers effectivement raccordés. Les deux DDS natifs restent intacts, sans copie ni réexport. L'intégration obtient `PASS_STATIC_EXPLOSIVES_INTEGRATION` : exactement trois références de texture changées dans un fichier de PM, un seul nouveau DDS `1776_black_powder_pm.dds`, aucune recette, emploi, technologie ou définition de groupe modifiés. Le nouveau DDS BGRA8 legacy fait 208 × 208 et huit mipmaps. Les 134 exports enregistrés se reconstruisent octet pour octet ; l'audit des raccordements ne relève ni réparation requise ni texture manquante dans son périmètre. Cuivre et sept anciens PM de laboratoire inchangés. Référence de contrôle capturée après le lot 8 et les corrections militaires précédentes, conservées. Aucun test en jeu, commit, push ou Steam Build.

## 23. Dixième lot — canaux, approuvé et intégré

Approbation : « Tout est validé aussi. ». Les routes restent intactes, conformément à « Les PM routiers ont déjà leur image. Concentre-toi sur les PM de canal. ».

| PM | Raccordement final |
| --- | --- |
| Pas de réseau de canaux — `pm_no_canal_network` | `unused/disabled.dds` natif conservé sans modification |
| Canaux industriels — `pm_industrial_canals` | `1776_industrial_canals_pm.dds`, porte simple et barge rouges |
| Canaux aménagés — `pm_engineered_canals` | `1776_engineered_canals_pm.dds`, écluse maçonnée renforcée et barge rouges |

Le groupe `pmg_land_transport_canals` utilise maintenant la flèche rouge native `mixed_icon_military.dds` au lieu du cerf d'erreur, sans changement de recette. Les masters originaux, prompts complets et paramètres sont conservés dans [le manifeste des canaux](pm_canals_sources_2026-10-07/manifest.json). Deux créations avec l'outil intégré imagegen : symboles graphiques, pas des plans techniques. Références : [écluses](https://canalrivertrust.org.uk/canals-and-rivers/how-does-a-canal-lock-work), [portes](https://canalrivertrust.org.uk/our-cause/looking-after-canals-and-rivers/engineering/building-lock-gates).

Contrôle `PASS_STATIC_CANALS_INTEGRATION` effectué avant la recoloration ferroviaire : seules deux textures de PM et la flèche du groupe changent ; deux DDS 208/8 BGRA8 natifs ajoutés, alpha réel et reconstruction exacte. L'état désactivé natif, les recettes et les routes sont inchangés. Les planches et sauvegardes de contrôle restent dans le cache ignoré. Aucun essai moteur.

## 24. Locomotives vertes seulement — recoloration intégrée

Dernière instruction, prioritaire sur l'ancienne règle jaune des trains : « Ne change pas la couleur des PM de wagon, change juste la couleur des PM de locomotive pour les mettre en vert. ». Les wagons voyageurs, y compris aluminium, gardent exactement leurs DDS, couleurs et raccordements.

| Dessin natif conservé | Copie locale verte | PM raccordés |
| --- | --- | ---: |
| `experimental_trains.dds` | `1776_experimental_locomotive_green.dds` | 1 |
| `trains_steam.dds` | `1776_steam_locomotive_green.dds` | 2 |
| `trains_electric.dds` | `1776_electric_locomotive_green.dds` | 2 |
| `trains_diesel.dds` | `1776_diesel_locomotive_green.dds` | 2 |

Les variantes avec bonus de transport partagent la même copie verte que leur locomotive. `pm_no_rail_network`, déjà vert, reste natif. La flèche de `pmg_base_building_railway` passe du cerf d'erreur à `mixed_icon_automation.dds` natif, vert.

Aucune génération IA ni redessin : décalage déterministe de teinte vers le vert natif de `rail_transport.dds`, saturation et valeur HSV conservées, alpha identique pixel pour pixel. Dimensions natives conservées : 208/8 pour la primitive, 104/7 pour vapeur, électrique et diesel. Aucun fichier vanilla écrasé. [Manifeste et paramètres exacts](pm_locomotive_colour_sources_2026-10-07/manifest.json), fonctions de `tools/recolour_pm_icons.py`.

`PASS_COLOUR_ONLY_INTEGRATION` : sept raccordements de PM, une flèche, quatre DDS ; recettes, wagons, autres PM et fichiers natifs intacts. Les 140 exports du registre passent la reconstruction exacte ; audit : zéro correction restante hors cuivre, aucun fichier manquant, laboratoires et cuivre protégés inchangés. Aucun test en jeu.

La chimie industrielle est considérée couverte, conformément à la correction du joueur « Non pas besoin de faire la chimie, on a déjà tout. Fais un autre lot. ». Les deux propositions de chimie préparées sont abandonnées sans aucun raccordement, export ou changement des recettes ; conserver les icônes chimiques existantes.


## 25. Onzième lot — salines et épices, intégré le 8 octobre

La chimie reste inchangée à la demande du joueur. Avant ce lot, les trois PM retenus utilisaient des images génériques : lingot de `gold_mining.dds` pour les salines, pousses de `plantation_production.dds` pour les épices traditionnelles et roue/goutte de `automatic_irrigation.dds` pour les épices mécanisées. Les trois nouveaux pictogrammes sont désormais raccordés au jeu après approbation.

| PM | Proposition |
| --- | --- |
| Production des salines — `default_building_salt_pan` | Bassin d'évaporation et cristaux de sel, sans lingot d'or |
| Culture traditionnelle des épices — `pm_spice_cultivation` | Rameau à grappes de poivre et petit panier de récolte |
| Culture mécanisée des épices — `pm_mechanized_spice_cultivation` | Même motif végétal associé à une motopompe d'irrigation à volant |

Palette jaune/ocre de production standard pour les trois : leurs groupes sont `pmg_base_building_salt_pan` et `pmg_base_building_spice_plantation`, pas des groupes d'automatisation. Le mot « mécanisée » ne rend donc pas cette icône verte. Les états de drainage `unused/` des plantations, les PM de trains, l'ancienne chimie et tous les raccordements actuels restent intacts.

Le poivre est une convention représentative du bien « épices », pas une obligation de remplacer toutes les cultures par une espèce unique : motif de feuilles et grappes inspiré de la [notice de Kew sur Piper nigrum](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:682369-1/general-information). Le bassin évoque l'évaporation saline présentée par le [musée du sel](https://www.salineroyale.com/wp-content/uploads/2025/08/Refonte-FALC-MUSEE-DU-SEL.pdf), pas les bâtiments complets d'Arc-et-Senans. La pompe est un raccourci de l'irrigation mécanisée déjà prévue par la recette du PM, pas un plan d'installation.

Trois créations distinctes avec l'outil intégré imagegen, masters 1254 × 1254 RGBA à alpha réel 0–255, coins transparents. Les originaux ci-dessous ont été copiés dans `docs/reports/assets/pm_salt_spices_sources_2026-10-08/` sous leurs noms de sujet, sans modification :
- `salt_pan` : `exec-5dfe7bb3-8b48-4d24-a59e-1f1dd5c03f67.png`, SHA-256 `f2fc636f0b2a919dcf0f057ab8622ebc0eaa6697de3774850de15c5bc42d54ab`.
- `spice_cultivation` : `exec-7a09be1e-3ec2-49fa-9af7-c7d88a368701.png`, SHA-256 `e6989a1f63a95f9c0842c61e9eece7addc4fb71132e63027357434e4cba736ab`.
- `mechanized_spice_cultivation` : `exec-e779b9b2-40dd-42bd-a8ed-51447b212104.png`, SHA-256 `0179b62627da97ff8118a782453dd229611ba6d3773de08b42bf9a8811997cf5`.

Approbation reçue le 8 octobre : « Ok, j'approuve le lot. » Les trois masters sont conservés sans retouche artistique dans [les sources finales et leurs prompts](pm_salt_spices_sources_2026-10-08/manifest.json). Trois DDS 208 × 208 BGRA8 legacy, huit mipmaps, sont raccordés aux trois PM. `PASS_STATIC_SALT_SPICES_INTEGRATION` : exactement deux fichiers de PM et trois textures ajoutées, uniquement les références d'image changées ; recettes, groupes, fichiers natifs et tout autre fichier de jeu inchangés pendant l'intégration. La reconstruction exacte des 143 exports passe. Une seule planche de preview et les diagnostics restent dans le cache ignoré, aucun PNG miniature versionné. Aucun essai moteur.

## 26. Dernière vérification — 8 octobre 2026

L'audit final ne conclut **pas** à une couverture entièrement terminée hors cuivre. Aucun PM hors cuivre n'a de texture absente, illisible, totalement transparente ou copiée du cerf d'erreur ; mais deux groupes actifs ont encore le cerf (imprimerie et infrastructures terrestres), douze groupes omettent leur texture, et des palettes demandent encore harmonisation. La poudre sans fumée conserve aussi un symbole d'électrolyse de saumure, sans nouvelle validation dédiée à ce sujet. Les réemplois cohérents (pompes, pics, dynamite, axe forestier, monuments) ne sont pas automatiquement de nouvelles commandes de dessin ; chimie, aluminium, icônes `unused/` retenues et laboratoire restent intacts.

Le [bilan actuel détaillé](pm_icon_final_check_2026-10-08.md) remplace les compteurs historiques du début de ce document pour décider de la fin du travail. Cette passe intègre uniquement le lot 11 validé ; elle n'applique aucune correction supplémentaire sans demande du joueur.

## 27. Douzième lot intégré — 8 octobre 2026

À la demande du joueur de choisir le prochain lot dans l'audit final : trois corrections proposées, sans génération ni redessin. Le groupe d'imprimerie reprend la flèche blanche existante `gfx/interface/icons/generic_icons/mixed_icon_distillery.dds` au lieu du cerf ; les deux états du concassage du calcaire conservent exactement leurs masters approuvés, avec un changement déterministe de teinte vers le violet de `1776_manual_ore_sorting.dds`. Saturation, valeur HSV, alpha, dimensions, silhouette et texture mate conservés. La future intégration associera aussi la flèche violette native au groupe de concassage actuellement sans texture, sans quatrième artwork.

Approbation reçue : « Je valide tout. » `PASS_COLOUR_ONLY_INTEGRATION` : exactement deux fichiers de groupes et deux DDS modifiés ; aucune recette ni autre donnée de jeu touchée pendant cette intégration. Les deux couleurs remplacent les entrées précédentes dans le registre, qui reste à 143 exports. [Masters finaux et paramètres reproductibles](pm_limestone_colour_sources_2026-10-08/manifest.json). La flèche blanche d'imprimerie et les dessins d'origine restent intacts. Chimie, cuivre, routes, wagons, laboratoire et PM `unused/` conservés. Les planches et diagnostics restent dans `.asset-cache/pm_batch_12_printing_limestone_colour_2026-10-08/`. Aucun test moteur.

## 28. Treizième lot proposé, non intégré — 8 octobre 2026

Trois images de groupe : infrastructures terrestres, extraction du phosphate, automatisation du phosphate. Les deux premières reprennent la silhouette de flèche native, teintée en jaune par rotation HSV déterministe depuis la flèche verte d'automatisation ; référence de couleur : salines approuvées. La troisième conserve la flèche verte native intacte. La flèche native `mixed_icon_base.dds` est blanche dans le jeu installé : une variante locale jaune est donc proposée, sans écraser le fichier partagé. Un seul master de couleur pour les deux groupes de production, aucune génération IA ni redessin. Les pictogrammes routiers déjà approuvés sont conservés.

`PASS_THREE_GROUP_PREVIEW` : exactement trois propositions, sources natives intactes, aucun fichier de jeu modifié par cette preview. Planche unique, master de teinte, paramètres et empreintes dans `.asset-cache/pm_batch_13_group_bindings_2026-10-08/`. Aucune intégration avant l'approbation du joueur. Les ajustements budgétaires demandés séparément sont réalisés avant le snapshot de ce lot.

## Sources des tables

Le code `F…:ligne` indique le fichier ci-dessous et la ligne de la texture, dans l'état audité.

- F1 — [common/buildings/13_tech6c5b_copper_mine.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/buildings/13_tech6c5b_copper_mine.txt>)
- F2 — [common/goods/13_tech6c5b_copper.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/goods/13_tech6c5b_copper.txt>)
- F3 — [common/production_method_groups/13_tech6c5b_copper_pmgs.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/13_tech6c5b_copper_pmgs.txt>)
- F4 — [common/production_method_groups/17_tech6c8_pharmaceuticals_pmgs.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/17_tech6c8_pharmaceuticals_pmgs.txt>)
- F5 — [common/production_method_groups/20_tech6d_wave_d_pmgs.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/20_tech6d_wave_d_pmgs.txt>)
- F6 — [common/production_method_groups/21_tech6d_wave_e_pmgs.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/21_tech6d_wave_e_pmgs.txt>)
- F7 — [common/production_method_groups/22_tech7a_wave_a_land_transport_pmgs.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/22_tech7a_wave_a_land_transport_pmgs.txt>)
- F8 — [common/production_method_groups/23_tech7a_wave_b_canals_pmgs.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/23_tech7a_wave_b_canals_pmgs.txt>)
- F9 — [common/production_method_groups/24_tech7a_wave_c_rail_pmgs.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_method_groups/24_tech7a_wave_c_rail_pmgs.txt>)
- F10 — [common/production_methods/01_industry.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/01_industry.txt>)
- F11 — [common/production_methods/07_government.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/07_government.txt>)
- F12 — [common/production_methods/09_misc_resource.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/09_misc_resource.txt>)
- F13 — [common/production_methods/10_tech6a1b_salt_producers.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/10_tech6a1b_salt_producers.txt>)
- F14 — [common/production_methods/10_tech6a3_spices.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/10_tech6a3_spices.txt>)
- F15 — [common/production_methods/10_tech6c1_limestone_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/10_tech6c1_limestone_production.txt>)
- F16 — [common/production_methods/11_private_infrastructure.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/11_private_infrastructure.txt>)
- F17 — [common/production_methods/11_tech6c1b_cement_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/11_tech6c1b_cement_production.txt>)
- F18 — [common/production_methods/12_tech6c3a_chemical_works_and_consumers.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/12_tech6c3a_chemical_works_and_consumers.txt>)
- F19 — [common/production_methods/12_tech6c4_oil_refinery_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/12_tech6c4_oil_refinery_production.txt>)
- F20 — [common/production_methods/13_construction.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_construction.txt>)
- F21 — [common/production_methods/13_tech6c5b_copper_production_and_consumers.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/13_tech6c5b_copper_production_and_consumers.txt>)
- F22 — [common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt>)
- F23 — [common/production_methods/15_tech6c6b_phosphate_extraction.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/15_tech6c6b_phosphate_extraction.txt>)
- F24 — [common/production_methods/16_tech6c7_precision_machinery_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/16_tech6c7_precision_machinery_production.txt>)
- F25 — [common/production_methods/16_tech6r1_mine_processing.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/16_tech6r1_mine_processing.txt>)
- F26 — [common/production_methods/17_tech6c8_pharmaceuticals_production_and_consumers.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/17_tech6c8_pharmaceuticals_production_and_consumers.txt>)
- F27 — [common/production_methods/18_tech6d_wave_b_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/18_tech6d_wave_b_production.txt>)
- F28 — [common/production_methods/19_tech6d_wave_c_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/19_tech6d_wave_c_production.txt>)
- F29 — [common/production_methods/20_tech6d_wave_d_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/20_tech6d_wave_d_production.txt>)
- F30 — [common/production_methods/21_tech6d_wave_e_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/21_tech6d_wave_e_production.txt>)
- F31 — [common/production_methods/22_field_drainage_plantations.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/22_field_drainage_plantations.txt>)
- F32 — [common/production_methods/22_tech7a_wave_a_land_transport_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/22_tech7a_wave_a_land_transport_production.txt>)
- F33 — [common/production_methods/23_tech7a_wave_b_canals_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/23_tech7a_wave_b_canals_production.txt>)
- F34 — [common/production_methods/23_tech8c_research_data.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/23_tech8c_research_data.txt>)
- F35 — [common/production_methods/24_tech8c_research_laboratory.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/24_tech8c_research_laboratory.txt>)
- F36 — [common/production_methods/99_cleanup2e4_merchant_republic_monuments.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/99_cleanup2e4_merchant_republic_monuments.txt>)
- F37 — [common/production_methods/99_tech_tree_wave3_causality.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/production_methods/99_tech_tree_wave3_causality.txt>)
- F38 — [common/technology/technologies/10_tech3a_production.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/10_tech3a_production.txt>)
- F39 — [common/technology/technologies/20_tech3a_military.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/20_tech3a_military.txt>)
- F40 — [common/technology/technologies/25_tech3a_naval.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/25_tech3a_naval.txt>)
- F41 — [common/technology/technologies/30_tech3a_society.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/30_tech3a_society.txt>)
- F42 — [common/technology/technologies/99_tech_tree_wave1_structural_trunks.txt](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/common/technology/technologies/99_tech_tree_wave1_structural_trunks.txt>)

