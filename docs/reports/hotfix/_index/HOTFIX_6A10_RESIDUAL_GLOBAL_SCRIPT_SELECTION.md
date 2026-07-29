# HOTFIX-6A.10 — Sélection du prochain résidu global

Date : 29 juillet 2026

Phase : `HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION`

Branche : `hotfix-dlc-audit`

HEAD initial : `a46aeb5d491478ccf7fc0beecac15f5d74bd404b`

HEAD final : `a46aeb5d491478ccf7fc0beecac15f5d74bd404b`

## 1. Décision

La phase est strictement documentaire. Aucun gameplay, événement, journal
entry, historique, loi, localisation ou asset n'a été modifié. Victoria 3 et
le launcher Paradox n'ont été ni lancés ni pilotés.

Le prochain sous-bloc retenu est l'alignement de deux propriétés de pinning
Victoria 3 1.13 dans `common/journal_entries/00_romania.txt`. Le futur
correctif sera limité à un fichier, deux objets, deux substitutions et deux
hunks.

`NEXT_EXECUTION_PHASE = HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT`

La phase 6A.10F n'est pas commencée dans ce rapport.

## 2. Préflight et état Git initial

| Contrôle | Résultat |
| --- | --- |
| Racine | `C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_fork` |
| Branche | `hotfix-dlc-audit` |
| HEAD | `a46aeb5 Align Sick Man journal entry pinning with Victoria 3 1.13` |
| Rapport 6A.9F dans HEAD | présent |
| Dix verdicts d'entrée 6A.9F | présents |
| Fichiers suivis modifiés avant 6A.10 | aucun |
| Index staged | vide |
| Non suivis | seulement `bject` et les sept fichiers de `docs/research/technology/` |
| `git diff --check` initial | propre |
| Stash protégé | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Processus Victoria 3, `dowser`, Paradox | aucun |

La source hotfix et vanilla ont été consultés en lecture seule. Aucun reset,
restore, checkout de fichier, clean, merge, rebase, amend, commit ou accès au
contenu du stash n'a été effectué.

## 3. Hashes de référence

| Preuve | SHA-256 | Verdict |
| --- | --- | --- |
| Fork `common/journal_entries/00_sick_man.txt` | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` | conforme |
| Source hotfix `00_sick_man.txt` | `E48405BFABB52F6CE757880E436C8D44C67111E246AF3215FD3F96EC4F3477F9` | conforme |
| Vanilla `00_sick_man.txt` | `1EAD43BE40DAF22D585712442AFD379C893C3075007CDA0AADDB126CCF1DCA41` | conforme |
| Histoire TUR fork | `81ABC8DEA9DE93EC6A4DD417FD05FD6859F3122758D2B27E712B1880013F9CA9` | conforme |
| Grande Crise orientale fork | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` | conforme |
| Événements Sick Man source/vanilla | `D110D1FD83CD98E131D4C2769B606CC908F17844EFF88EF65F51FEBF313A0C2B` | conforme |
| Événements Tanzimat source/vanilla | `F5DAABC9D36BEAE714E5BDFC3B156995B3EAE7758004CE3C7B8C3512BA80AD30` | conforme |

### Hashes protégés

| Élément | SHA-256 |
| --- | --- |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` |
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410` |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` |

Les huit hashes protégés concordent exactement avec 6A.9F.

## 4. Sources consultées

Ont été lus intégralement ou chargés intégralement pour interrogation :

- `HOTFIX_6A9F_SICK_MAN_EIGHT_JE_PINNING_1_13_ALIGNMENT.md` ;
- `HOTFIX_6A9R_OTTOMAN_TANZIMAT_1776_ENTRY_CHAIN_AUDIT.md` ;
- `HOTFIX_6A7_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md` ;
- `HOTFIX_6A8R_GREAT_EASTERN_CRISIS_1_13_AUDIT.md` ;
- `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
- `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
- `HOTFIX_REPORT_INDEX.csv` ;
- `HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` ;
- `HOTFIX_C1AI_CONCURRENT_WORK_RECONCILIATION.md` ;
- les deux changelogs complets du fork et les deux copies du changelog source ;
- les nouveaux `debug.log`, `debug.1.log`, `error.log`, `game.log` et
  `system.log` de 6A.9F, ainsi que les snapshots de rotations consignés dans
  6A.9F.

## 5. Inventaire canonique après 6A.9F

| Catégorie effective exclusive | Lignes |
| --- | ---: |
| `REQUIRED_HOTFIX_DELTA` | 7 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 17 |
| `ALREADY_MERGED` | 17 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 |
| `PROTECTED_CONCURRENT_WORK` | 19 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 |
| **Total** | **161** |

Les catégories sont mutuellement exclusives et leur somme vaut 161. Les
lignes directement exploitables par une revue sont
`7 + 17 + 87 = 111`. Elles ne constituent pas 111 correctifs. L'ancien total
annoncé de 26 deltas à haute confiance reste `UNVERIFIED`, faute de liste
canonique exacte retrouvée.

## 6. Baseline parser 6A.9F recalculée

Le nouveau
`C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\logs\debug.log`
(`78068296741B912AFC46A4E763ED393F35F7D00967E4F17EB98075BC8EB177F5`)
contient exactement :

- 378 lignes `Unexpected token: should_be_pinned_by_default,` ;
- 142 chemins uniques ;
- zéro diagnostic de pinning dans `00_sick_man.txt` ;
- zéro
  `should_be_pinned_by_default_uninvolved_or_context` rejeté dans ce fichier ;
- trois paires de diagnostics Tanzimat propres aux références `.5`, `.10` et
  `.9` de `00_sick_man.txt`.

Les rotations historiques ne sont pas additionnées à cette baseline. Le
`debug.1.log` nouveau
(`456557E5AAD303159180496C024286C5966BCE5C3FB46401A86BB0746CA84559`)
sert uniquement à prouver le montage du fork et de `dlc014_ip3`. Les erreurs
de namespace et les autres erreurs moteur sans rapport avec le pinning sont
traitées séparément et ne sont jamais comptées parmi les 378.

### Rapprochement avec l'inventaire

| Statut effectif des fichiers | Fichiers | Occurrences |
| --- | ---: | ---: |
| `INTENTIONAL_FORK_DIVERGENCE` | 104 | 242 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 16 | 94 |
| `PENDING_REVIEW` | 8 | 19 |
| `MERGED_STATIC_ONLY` | 10 | 19 |
| `HORS_INVENTAIRE` | 4 | 4 |
| **Total** | **142** | **378** |

Les huit `PENDING_REVIEW` de cette table sont des fichiers protégés ou des
extensions custom sans convergence moderne exploitable. La propriété moderne
`should_be_pinned_by_default_uninvolved_or_context` est présente dans les
copies source et vanilla de 133 des 142 chemins. Les neuf exceptions sont les
huit fichiers custom/mod sans propriété moderne convergente et
`06_new_imperialism.txt`, absent de la source et de vanilla.

## 7. Liste exhaustive des 142 fichiers

Légende : `IFD` = divergence fork intentionnelle ; `VAI` = alignement vanilla
1.13 requis ; `PCW` = travail concurrent protégé ; `MSO` = fusion statique
seulement ; `HI` = hors inventaire. Les lignes sont celles déclarées par le
moteur. L'objet est le bloc racine immédiatement propriétaire de la propriété.
Le tableau est trié par occurrences décroissantes puis par chemin ; ses
25 premières lignes constituent aussi le top 25 requis.

| Rang | Chemin | Occ. | Lignes | Objets | Statut |
| ---: | --- | ---: | --- | --- | --- |
| 1 | `common/journal_entries/00_tutorial.txt` | 52 | 2,77,131,195,257,332,338,374,430,518,569,607,631,646,656,662,695,732,756,762,846,969,986,1004,1010,1052,1085,1090,1103,1108,1121,1126,1158,1163,1210,1217,1227,1232,1250,1257,1373,1380,1489,1531,1546,1582,1588,1620,1639,1670,1697,1723 | `je_subject_liberty, je_tutorial_capacity_deficit, je_tutorial_change_production_method, je_tutorial_colonize_state, je_tutorial_convoy_raiding, je_tutorial_create_formation, je_tutorial_declare_an_interest, je_tutorial_earn_obligation, je_tutorial_enact_institution_law, je_tutorial_establish_company, je_tutorial_expand_basic_building, je_tutorial_expand_military, je_tutorial_expand_productive_building, je_tutorial_fix_budget_deficit, je_tutorial_fix_unproductive_building, je_tutorial_foreign_investment, je_tutorial_form_power_bloc, je_tutorial_grow_gdp, je_tutorial_improve_consumer_goods_access, je_tutorial_improve_market_access_with_railways, je_tutorial_improve_rank, je_tutorial_improve_supply_network, je_tutorial_incorporate_state, je_tutorial_increase_immigration, je_tutorial_increase_market_access_by_decree, je_tutorial_increase_relations, je_tutorial_invest_into_an_institution, je_tutorial_is_play_target, je_tutorial_lobbies, je_tutorial_make_interest_group_happy, je_tutorial_make_peace, je_tutorial_mobilize_army, je_tutorial_prevent_revolution, je_tutorial_promote_movement, je_tutorial_recover_from_default, je_tutorial_recruit_promote_commander, je_tutorial_reform_government, je_tutorial_research_technology, je_tutorial_send_general_to_front, je_tutorial_start_diplomatic_play` | VAI |
| 2 | `common/journal_entries/00_player_objectives_great_game.txt` | 17 | 3,659,697,735,794,856,916,957,997,1045,1154,1232,1483,1527,1716,1743,1781 | `je_achieve_sovereignty, je_acquire_korean_protectorate, je_chinese_concessions, je_codify_chinese_border, je_consolidate_afghanistan_objective, je_consolidate_british_india, je_consolidate_central_asia, je_consolidate_persia, je_counter_russian_pacific_influence, je_disrupt_russian_caucasus, je_great_game_control, je_maintain_afghan_protectorate, je_pacify_kazakh_steppes, je_pamir_expedition_objective, je_secure_influence_over_persia, je_secure_persian_border, je_unify_afghanistan_objective` | IFD |
| 3 | `common/journal_entries/05_prestige_goods.txt` | 16 | 127,256,385,514,643,772,901,1030,1159,1288,1417,1546,1675,1804,1933,2062 | `je_prestige_goods_artillery, je_prestige_goods_clothes, je_prestige_goods_coffee, je_prestige_goods_explosives, je_prestige_goods_fertilizer, je_prestige_goods_fish, je_prestige_goods_furniture, je_prestige_goods_grain, je_prestige_goods_groceries, je_prestige_goods_meat, je_prestige_goods_merchant_marine, je_prestige_goods_opium, je_prestige_goods_paper, je_prestige_goods_small_arms, je_prestige_goods_steel, je_prestige_goods_tools` | IFD |
| 4 | `common/journal_entries/03_russia.txt` | 12 | 76,325,532,636,741,939,1003,1101,1172,1215,1300,1344 | `je_caucasian_war, je_caucasian_war_circassia, je_caucasian_war_imamate, je_circassian_expulsions, je_conquest_of_central_asia, je_great_reformer, je_great_reforms_bureaucratic, je_great_reforms_military, je_great_reforms_serfdom, je_pacify_the_steppes, je_the_eastern_border, je_the_last_kazakh_khan` | IFD |
| 5 | `common/journal_entries/00_player_objectives_hegemon.txt` | 11 | 2,27,54,74,101,151,170,187,204,221,244 | `je_african_colonies, je_colonization_laws, je_expand_navy_and_army, je_form_alliance, je_great_power, je_greater_power, je_greatest_power, je_increase_technology, je_take_subject, je_the_hegemon, je_unrecognized_power` | IFD |
| 6 | `common/journal_entries/00_player_objectives_economic_dominance.txt` | 10 | 2,61,90,119,139,170,238,262,291,315 | `je_expanding_the_market, je_exporting_profits, je_lower_production_costs, je_objective_expand_goods_production, je_raise_exports_value, je_refining_goods, je_specialized_goods, je_specialized_inputs, je_strong_market, je_utilizing_our_strength` | IFD |
| 7 | `common/journal_entries/00_negotiation_quests_je.txt` | 7 | 117,235,355,471,585,687,825 | `je_government_petition_negotiation_version, je_government_petition_negotiation_version_b, je_negotiate_army_quest, je_negotiate_building_group, je_negotiate_buildings, je_negotiate_sol, je_negotiate_taxes` | IFD |
| 8 | `common/journal_entries/06_economic_regeneration.txt` | 7 | 285,412,623,869,981,1311,1488 | `je_spa_economic_regeneration_land_reform, je_spa_economic_regeneration_light_industry, je_spa_economic_regeneration_master, je_spa_economic_regeneration_mining, je_spa_economic_regeneration_modernise_agriculture, je_spa_economic_regeneration_railways, je_spa_economic_regeneration_ultramar` | IFD |
| 9 | `common/journal_entries/07_poland_lithuania_mod.txt` | 7 | 238,311,345,390,440,510,570 | `je_plc_reform, je_plc_reform_education, je_plc_reform_farming, je_plc_reform_industry, je_plc_reform_military, je_plc_reform_railways, je_plc_reform_trade` | PCW |
| 10 | `common/journal_entries/00_acw_entries.txt` | 6 | 86,123,162,298,352,447 | `je_acw_countdown, je_acw_equality, je_acw_reconstruction, je_acw_reincorporate, je_acw_war, je_acw_wild_wild_west` | IFD |
| 11 | `common/journal_entries/00_meiji_restoration.txt` | 6 | 26,161,215,260,313,346 | `je_meiji_army, je_meiji_diplomacy, je_meiji_economy, je_meiji_main, je_meiji_restoration, je_terakoya` | MSO |
| 12 | `common/journal_entries/00_player_objectives_egalitarian_society.txt` | 6 | 2,30,44,71,122,157 | `je_egalitarian_society, je_liberate_the_slaves, je_objective_encourage_liberal_ideas, je_pass_laws, je_public_services, je_women_and_children` | IFD |
| 13 | `common/journal_entries/06_portugal_politics.txt` | 6 | 177,308,515,573,641,688 | `je_devorismo, je_portugal_regeneration, je_portugal_regeneration_agriculture, je_portugal_regeneration_institutions, je_portugal_regeneration_public_works, je_second_liberalism` | VAI |
| 14 | `common/journal_entries/00_german_unification.txt` | 5 | 105,275,333,394,447 | `je_german_unification, je_german_unification_idea, je_north_german_unification, je_schleswig_holstein_question, je_south_german_unification` | VAI |
| 15 | `common/journal_entries/05_montenegro_je.txt` | 5 | 320,445,558,662,799 | `je_mon_austria_alliance, je_mon_serb_unity, je_mon_state_formation, je_montenegrin_raiding, je_tur_raided` | IFD |
| 16 | `common/journal_entries/06_iberian_twilight_monuments.txt` | 5 | 177,300,413,530,651 | `je_atocha_railway, je_gran_teatro, je_manila_cathedral, je_pena_palace, je_sagrada_familia` | IFD |
| 17 | `common/journal_entries/00_canada_australia.txt` | 4 | 71,161,206,259 | `je_australia_aus, je_australia_gbr, je_canada_can, je_canada_gbr` | VAI |
| 18 | `common/journal_entries/00_canals.txt` | 4 | 52,92,146,186 | `je_panama_canal, je_panama_survey, je_suez_canal, je_suez_survey` | IFD |
| 19 | `common/journal_entries/00_central_and_south_america.txt` | 4 | 6,124,170,180 | `central_america_falls_apart, je_reunify_central_america, ragamuffin_war, ragamuffin_war_minors` | IFD |
| 20 | `common/journal_entries/00_taiping.txt` | 4 | 124,237,286,340 | `je_chinese_missions, je_heavenly_kingdom_main, je_taiping, je_taiping_revolution` | IFD |
| 21 | `common/journal_entries/00_trade_route_event_missions.txt` | 4 | 41,90,140,190 | `je_build_local_arms_industry, je_set_up_grain_import, je_set_up_paper_import, je_set_up_steel_import` | IFD |
| 22 | `common/journal_entries/01_algeria.txt` | 4 | 92,241,280,314 | `je_conquest_of_algeria, je_french_foreign_legion, je_reconquest_of_algeria, je_the_algerian_departements` | IFD |
| 23 | `common/journal_entries/02_paraguay.txt` | 4 | 36,110,308,418 | `je_expanding_paraguay, je_francocracia, je_modernizing_paraguay, je_paraguayan_war` | IFD |
| 24 | `common/journal_entries/03_lobbies.txt` | 4 | 2,125,253,392 | `je_anti_lobby_demand, je_anti_lobby_opportunity, je_pro_lobby_demand, je_pro_lobby_opportunity` | IFD |
| 25 | `common/journal_entries/04_india_british_dictates.txt` | 4 | 2,146,339,343 | `je_british_dictate_law, je_british_dictate_military, je_british_dictate_plantations, je_british_dictate_universities` | MSO |
| 26 | `common/journal_entries/06_spanish_africa.txt` | 4 | 5,162,255,342 | `je_conquest_of_tetouan, je_guinean_conquest, je_moroccan_conquest, je_western_saharan_conquest` | VAI |
| 27 | `common/journal_entries/06_spanish_new_world.txt` | 4 | 115,196,308,379 | `je_hispanoamerica, je_reconquista, je_spanish_american_independence, je_spanish_new_world_dummy` | IFD |
| 28 | `common/journal_entries/00_fascism.txt` | 3 | 281,405,476 | `je_fascism_1, je_fascism_2, je_modernization_program` | VAI |
| 29 | `common/journal_entries/01_paris_commune.txt` | 3 | 70,229,325 | `je_the_paris_commune_communards, je_the_paris_commune_display, je_the_paris_commune_france` | IFD |
| 30 | `common/journal_entries/02_gran_colombia.txt` | 3 | 72,135,229 | `je_andean_federation, je_gran_colombia, je_la_plata` | VAI |
| 31 | `common/journal_entries/02_pedro_brazil.txt` | 3 | 251,304,396 | `je_isabel, je_pedro_brazil, je_pedro_republic` | IFD |
| 32 | `common/journal_entries/02_south_america_migration.txt` | 3 | 143,296,471 | `je_american_west_migration, je_central_america_migration, je_south_america_migration` | IFD |
| 33 | `common/journal_entries/03_korea.txt` | 3 | 2,95,186 | `je_donghak_movement, je_gyojo_shinwon, je_korean_rebellion` | VAI |
| 34 | `common/journal_entries/06_cuba.txt` | 3 | 134,318,493 | `je_cuba_espanol, je_cuba_independencia, je_cuba_la_vida_dulce` | IFD |
| 35 | `common/journal_entries/06_philippines_je.txt` | 3 | 171,311,463 | `je_filipino_ethnogenesis, je_philippines_development, je_philippines_main` | IFD |
| 36 | `common/journal_entries/07_american_mod_jes.txt` | 3 | 96,193,256 | `je_buying_florida_mod, je_northwest_frontier_mod, je_sale_of_florida_mod` | PCW |
| 37 | `common/journal_entries/00_alaska.txt` | 2 | 113,210 | `je_alaska, je_sale_of_alaska` | IFD |
| 38 | `common/journal_entries/00_hawaii.txt` | 2 | 73,135 | `je_hawaii, je_hawaiian_interest` | IFD |
| 39 | `common/journal_entries/00_manifest_destiny.txt` | 2 | 21,54 | `je_manifest_destiny_frontier_wars, je_manifest_destiny_mexico` | IFD |
| 40 | `common/journal_entries/00_opium_wars.txt` | 2 | 112,191 | `je_opium_obsession, je_opium_wars` | IFD |
| 41 | `common/journal_entries/00_peoples_springtime_je.txt` | 2 | 324,478 | `je_red_summer, je_springtime_of_the_peoples` | VAI |
| 42 | `common/journal_entries/00_poland.txt` | 2 | 59,131 | `je_christ_of_nations, je_poland_lithuania` | VAI |
| 43 | `common/journal_entries/00_romania.txt` | 2 | 76,149 | `je_all_for_one, je_unite_the_principalities` | VAI |
| 44 | `common/journal_entries/00_skyscraper.txt` | 2 | 62,99 | `je_skyscraper_construction, je_skyscraper_site` | IFD |
| 45 | `common/journal_entries/00_zanzibar.txt` | 2 | 39,323 | `je_lion_of_the_zanj, je_splitting_oman` | IFD |
| 46 | `common/journal_entries/01_french_monarchism.txt` | 2 | 266,512 | `je_cement_the_rightful_dynasty, je_divided_monarchists` | PCW |
| 47 | `common/journal_entries/01_natural_borders_of_france.txt` | 2 | 77,240 | `je_confederation_of_the_rhine, je_french_natural_borders` | IFD |
| 48 | `common/journal_entries/02_brazilian_slavery.txt` | 2 | 69,262 | `je_aberdeen_act, je_matter_of_slavery` | IFD |
| 49 | `common/journal_entries/02_coffee_and_milk.txt` | 2 | 128,283 | `je_agricultural_development, je_coffee_with_milk` | IFD |
| 50 | `common/journal_entries/02_south_american_national_identity.txt` | 2 | 406,608 | `je_south_american_national_identity, je_south_american_national_identity_emergence` | PENDING_REVIEW |
| 51 | `common/journal_entries/02_vargas.txt` | 2 | 139,226 | `je_new_republic, je_populist_unrest` | IFD |
| 52 | `common/journal_entries/03_afghanistan.txt` | 2 | 2,1826 | `je_consolidate_afghanistan, je_unify_afghanistan` | VAI |
| 53 | `common/journal_entries/04_india_home_rule.txt` | 2 | 2,153 | `je_india_home_rule, je_india_nationalism_britain` | MSO |
| 54 | `common/journal_entries/05_austria_journal_entries.txt` | 2 | 146,426 | `je_austrian_neo_absolutism, je_matter_of_hungary` | IFD |
| 55 | `common/journal_entries/05_balkan_wars.txt` | 2 | 16,283 | `je_spoils_of_war, je_the_balkan_league` | IFD |
| 56 | `common/journal_entries/05_danubian_federation.txt` | 2 | 292,689 | `je_danubian_federation, je_danubian_federation_observer` | IFD |
| 57 | `common/journal_entries/05_eastern_question.txt` | 2 | 130,137 | `je_eastern_question_austria, je_eastern_question_russia` | VAI |
| 58 | `common/journal_entries/06_portuguese_colonialism.txt` | 2 | 6,181 | `je_portuguese_colonialism, je_the_pink_map` | VAI |
| 59 | `common/journal_entries/06_usa_independence_mod.txt` | 2 | 86,151 | `je_usa_independence, je_usa_independence_fra` | PCW |
| 60 | `common/journal_entries/00_antarctica.txt` | 1 | 122 | `je_antarctica` | IFD |
| 61 | `common/journal_entries/00_autocracy.txt` | 1 | 210 | `je_king_in_parliament` | IFD |
| 62 | `common/journal_entries/00_battle_for_india_mod.txt` | 1 | 80 | `je_battle_for_india_goal` | HI |
| 63 | `common/journal_entries/00_boxer_rebellion.txt` | 1 | 49 | `je_boxer_rebellion` | IFD |
| 64 | `common/journal_entries/00_central_africa.txt` | 1 | 142 | `je_central_africa_expedition` | IFD |
| 65 | `common/journal_entries/00_communism.txt` | 1 | 109 | `je_communism_1` | IFD |
| 66 | `common/journal_entries/00_congo.txt` | 1 | 150 | `je_congo_expedition` | IFD |
| 67 | `common/journal_entries/00_congo_free_state.txt` | 1 | 161 | `je_free_state` | IFD |
| 68 | `common/journal_entries/00_corn_laws.txt` | 1 | 80 | `je_corn_laws` | IFD |
| 69 | `common/journal_entries/00_east_indies.txt` | 1 | 117 | `je_consolidate_colonial_rule` | IFD |
| 70 | `common/journal_entries/00_establish_colonial_administration.txt` | 1 | 85 | `je_colonial_administration` | IFD |
| 71 | `common/journal_entries/00_ethiopia.txt` | 1 | 38 | `je_age_of_princes` | IFD |
| 72 | `common/journal_entries/00_grand_exhibition.txt` | 1 | 151 | `je_grand_exhibition` | IFD |
| 73 | `common/journal_entries/00_ig_agendas.txt` | 1 | 286 | `je_government_petition` | IFD |
| 74 | `common/journal_entries/00_impose_law.txt` | 1 | 103 | `je_law_imposition` | IFD |
| 75 | `common/journal_entries/00_indian_removal.txt` | 1 | 70 | `je_indian_removal` | MSO |
| 76 | `common/journal_entries/00_krakatoa.txt` | 1 | 103 | `je_krakatoa` | MSO |
| 77 | `common/journal_entries/00_land_reclamation.txt` | 1 | 76 | `je_land_reclamation` | IFD |
| 78 | `common/journal_entries/00_niger_river.txt` | 1 | 141 | `je_niger_river_expedition` | IFD |
| 79 | `common/journal_entries/00_patagonia.txt` | 1 | 82 | `je_patagonia` | IFD |
| 80 | `common/journal_entries/00_plague.txt` | 1 | 132 | `je_spanish_flu` | IFD |
| 81 | `common/journal_entries/00_prohibition_laws.txt` | 1 | 120 | `je_prohibition` | IFD |
| 82 | `common/journal_entries/00_red_scare.txt` | 1 | 87 | `je_the_red_scare` | IFD |
| 83 | `common/journal_entries/00_request_recognition.txt` | 1 | 69 | `je_earn_recognition` | IFD |
| 84 | `common/journal_entries/00_reunify_china.txt` | 1 | 2 | `je_reunify_china` | IFD |
| 85 | `common/journal_entries/00_scramble_for_africa.txt` | 1 | 193 | `je_scramble_for_africa` | IFD |
| 86 | `common/journal_entries/00_seminole_wars.txt` | 1 | 84 | `je_seminole_wars` | IFD |
| 87 | `common/journal_entries/00_standard_of_living.txt` | 1 | 92 | `je_sol_1` | IFD |
| 88 | `common/journal_entries/00_strike_je.txt` | 1 | 156 | `je_strike` | IFD |
| 89 | `common/journal_entries/00_suffragists.txt` | 1 | 74 | `je_suffragists` | IFD |
| 90 | `common/journal_entries/00_turtle_island.txt` | 1 | 85 | `je_unite_the_nations` | IFD |
| 91 | `common/journal_entries/00_veiled_protectorate.txt` | 1 | 73 | `je_veiled_protectorate` | IFD |
| 92 | `common/journal_entries/00_victoria.txt` | 1 | 100 | `je_victoria` | IFD |
| 93 | `common/journal_entries/00_warlord_china.txt` | 1 | 106 | `je_warlord_china` | IFD |
| 94 | `common/journal_entries/00_west_america.txt` | 1 | 145 | `je_west_america_expedition` | IFD |
| 95 | `common/journal_entries/01_coup.txt` | 1 | 139 | `je_ip4_coup` | VAI |
| 96 | `common/journal_entries/01_dreyfus_affair.txt` | 1 | 92 | `je_dreyfus_affair` | IFD |
| 97 | `common/journal_entries/01_hispaniola.txt` | 1 | 90 | `je_haitian_debt` | IFD |
| 98 | `common/journal_entries/01_indochina.txt` | 1 | 82 | `je_indochina` | IFD |
| 99 | `common/journal_entries/01_krakow.txt` | 1 | 64 | `je_the_krakow_uprising` | IFD |
| 100 | `common/journal_entries/01_nihilism.txt` | 1 | 205 | `je_nihilist_movement` | IFD |
| 101 | `common/journal_entries/01_silkworm_diseases.txt` | 1 | 158 | `je_silkworm_diseases` | IFD |
| 102 | `common/journal_entries/02_acre_dispute.txt` | 1 | 33 | `je_acre_dispute` | IFD |
| 103 | `common/journal_entries/02_amazonas.txt` | 1 | 61 | `je_amazonas` | IFD |
| 104 | `common/journal_entries/02_brazil_navy.txt` | 1 | 135 | `je_brazil_navy` | IFD |
| 105 | `common/journal_entries/02_brazilian_nation_building.txt` | 1 | 79 | `je_brazilian_nation_building` | IFD |
| 106 | `common/journal_entries/02_caudillo.txt` | 1 | 69 | `je_caudillo` | IFD |
| 107 | `common/journal_entries/02_cristo_redentor.txt` | 1 | 65 | `je_cristo_redentor` | IFD |
| 108 | `common/journal_entries/02_peru_bolivia.txt` | 1 | 355 | `je_peru_bolivia` | IFD |
| 109 | `common/journal_entries/02_positivism.txt` | 1 | 140 | `je_positivist_movement` | IFD |
| 110 | `common/journal_entries/03_eastern_frontier.txt` | 1 | 2 | `je_eastern_frontier` | IFD |
| 111 | `common/journal_entries/03_tibetan_expedition.txt` | 1 | 258 | `je_tibet_expedition` | IFD |
| 112 | `common/journal_entries/04_communal_divides.txt` | 1 | 200 | `je_communal_divides` | IFD |
| 113 | `common/journal_entries/04_dravidian_movement.txt` | 1 | 100 | `je_dravidian_movement` | IFD |
| 114 | `common/journal_entries/04_imperialism_of_promise.txt` | 1 | 140 | `je_imperialism_of_promise` | VAI |
| 115 | `common/journal_entries/04_india_nationalism.txt` | 1 | 2 | `je_india_nationalism` | MSO |
| 116 | `common/journal_entries/04_india_non_cooperation.txt` | 1 | 2 | `je_india_non_cooperation_movement` | MSO |
| 117 | `common/journal_entries/04_indian_famines.txt` | 1 | 234 | `je_indian_famines` | MSO |
| 118 | `common/journal_entries/04_indian_federation.txt` | 1 | 141 | `je_federation_of_india` | MSO |
| 119 | `common/journal_entries/04_mughals.txt` | 1 | 61 | `je_mughal_hindustan` | IFD |
| 120 | `common/journal_entries/04_princely_states.txt` | 1 | 96 | `je_princely_states` | MSO |
| 121 | `common/journal_entries/04_sikh_empire.txt` | 1 | 199 | `je_sikh_sovereignty` | IFD |
| 122 | `common/journal_entries/04_victoria_terminus.txt` | 1 | 104 | `je_victoria_terminus` | IFD |
| 123 | `common/journal_entries/05_austrian_fascism.txt` | 1 | 7 | `je_standestaat` | PCW |
| 124 | `common/journal_entries/05_bulgaria_je.txt` | 1 | 179 | `je_prussia_of_the_balkans` | IFD |
| 125 | `common/journal_entries/05_greece.txt` | 1 | 14 | `je_bavarocracy` | IFD |
| 126 | `common/journal_entries/05_grunderzeit.txt` | 1 | 19 | `je_grunderzeit` | IFD |
| 127 | `common/journal_entries/05_hungary_je.txt` | 1 | 15 | `je_hungarian_revolution` | IFD |
| 128 | `common/journal_entries/05_hungry_forties.txt` | 1 | 6 | `je_the_hungry_forties` | IFD |
| 129 | `common/journal_entries/05_metternich.txt` | 1 | 157 | `je_metternich` | PCW |
| 130 | `common/journal_entries/05_national_awakening_monument.txt` | 1 | 240 | `je_kaiserforum` | IFD |
| 131 | `common/journal_entries/05_struggle_for_the_highveld.txt` | 1 | 275 | `je_struggle_for_the_highveld` | IFD |
| 132 | `common/journal_entries/05_technocracy.txt` | 1 | 74 | `je_technocracy` | IFD |
| 133 | `common/journal_entries/05_the_grand_collapse.txt` | 1 | 13 | `je_the_grand_collapse` | IFD |
| 134 | `common/journal_entries/06_dominican_content.txt` | 1 | 121 | `je_la_trinitaria` | IFD |
| 135 | `common/journal_entries/06_french_revolution_mod.txt` | 1 | 176 | `je_fr_rev_summon_estates` | HI |
| 136 | `common/journal_entries/06_language_policy.txt` | 1 | 418 | `je_vernacular_policy` | IFD |
| 137 | `common/journal_entries/06_morocco_lands_of_anarchy.txt` | 1 | 18 | `je_lands_of_anarchy` | IFD |
| 138 | `common/journal_entries/06_new_imperialism.txt` | 1 | 57 | `je_new_imperialism` | IFD |
| 139 | `common/journal_entries/07_hindustan_is_durrani_mod.txt` | 1 | 50 | `je_hindustan_is_durrani` | PCW |
| 140 | `common/journal_entries/07_iran_troubles_mod.txt` | 1 | 96 | `je_deputy_of_the_people` | HI |
| 141 | `common/journal_entries/07_irish_question_mod.txt` | 1 | 75 | `je_irish_question` | HI |
| 142 | `common/journal_entries/99_test_global_je.txt` | 1 | 137 | `je_global_test` | IFD |

Contrôle de somme : les 142 lignes du tableau représentent exactement 378
occurrences.

## 8. Familles principales

- Tutoriels : 52 occurrences dans un fichier et 40 objets racine distincts ;
  la portée est massive et plusieurs objets portent plusieurs occurrences.
- Objectifs joueur : 44 occurrences dans Great Game, Hegemon, Economic
  Dominance et Egalitarian Society ; ces overrides 1776 sont intentionnels.
- Prestige goods : 16 occurrences, 16 objets custom, divergence intentionnelle.
- Russie : 12 occurrences, 12 objets, protection absolue ; aucun candidat.
- Autres journal entries : 254 occurrences réparties entre alignements 1.13,
  divergences 1776, fichiers déjà fusionnés et travaux protégés.
- Fichiers hors inventaire : quatre fichiers et quatre occurrences ; aucune
  preuve d'import.
- Fichiers à erreur unique : 83 fichiers ; leur petite taille parser ne suffit
  pas à autoriser une correction.
- Fichiers multi-objets : 59 fichiers comportent au moins deux diagnostics ;
  la plupart ont un objet distinct par propriété.
- Divergence source/vanilla : elle existe dans tous les petits fichiers
  sérieux examinés au niveau du fichier complet, même lorsque la propriété de
  pinning ciblée converge. Une correction future doit donc rester hunkée.

Pour les 133 chemins disposant de l'API moderne dans source et vanilla, la
propriété moderne est
`should_be_pinned_by_default_uninvolved_or_context = yes`. La présence
convergente de cette ligne autorise seulement l'analyse du hunk correspondant,
jamais le remplacement du fichier ni l'import des dettes adjacentes.

## 9. Blocs clos et protections

Ont été exclus de tout candidat : Balkan National Awakening, Yugoslavia,
Risorgimento, nationalisme grec, Grande Crise orientale et les huit pinning
Sick Man. L'activation Tanzimat, `sick_man.1`, `sick_man_of_europe` et
`outmoded_bureaucracy` restent dans
`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG`.

Sont également exclus : DEI/VOC, Java, économie post-compagnie, NAVY, MARATH,
SAT, KHP, Travancore, Inde/BIC/Sepoy/Bombay, ADMIN, Japon, Russie,
Autriche/Croatie/Slavonie/Suisse, révolutions américaine et française, lettres
de Kew, technologies, agriculture/alimentation/industrie générale,
descripteurs, launcher, sauvegardes et `bject`.

BIC conserve
`activate_law = law_type:law_frontier_colonization` et ne contient pas
`law_colonial_exploitation`.

## 10. Diagnostics Tanzimat hors pinning

Le namespace déclaré par source et vanilla est `tanzimat_events`. Le fichier
`events/tanzimat_events.txt` est absent du fork, mais la source et vanilla
convergent bit à bit sur le hash
`F5DAABC9D36BEAE714E5BDFC3B156995B3EAE7758004CE3C7B8C3512BA80AD30`.
L'inventaire le classe donc `OBSOLETE_HOTFIX_CONTENT` avec l'instruction de ne
pas le copier : vanilla 1.13 est censé le fournir. `dlc014_ip3` National
Awakening est monté et le contenu Sick Man est conditionné par `ip3_content`.

| ID | Référence fork | Objet/pulse | Message moteur exact | Déclaration source/vanilla |
| --- | --- | --- | --- | --- |
| `tanzimat_events.5` | `common/journal_entries/00_sick_man.txt:347` | `je_sick_man_separatism`, `on_monthly_pulse.random_events` | `'tanzimat_events.5' does not have a valid namespace`; `OnAction on_monthly_pulse is trying to add unknown random event with ID [tanzimat_events.5]` | `events/tanzimat_events.txt:458`, `country_event`, namespace `tanzimat_events` |
| `tanzimat_events.10` | `common/journal_entries/00_sick_man.txt:436` | `je_sick_man_army`, `on_monthly_pulse.events` | `'tanzimat_events.10' does not have a valid namespace`; `Invalid event id tanzimat_events.10` | `events/tanzimat_events.txt:1094`, `country_event`, même namespace |
| `tanzimat_events.9` | `common/journal_entries/00_sick_man.txt:484` | `je_sick_man_bureaucracy`, `on_monthly_pulse.random_events` | `'tanzimat_events.9' does not have a valid namespace`; `OnAction on_monthly_pulse is trying to add unknown random event with ID [tanzimat_events.9]` | `events/tanzimat_events.txt:985`, `country_event`, même namespace |

Une référence adjacente à `.10` existe aussi dans
`common/on_actions/00_code_on_actions.txt:4375`, avec `.1`, `.2` et `.4`.
Cela prouve que les trois lignes JE ne constituent pas une unité autonome.
Importer le fichier de 1 139 lignes contredirait son classement
`OBSOLETE_HOTFIX_CONTENT`, augmenterait la surface d'override et réintroduirait
une dette événementielle plus large.

La chaîne Tanzimat restant inactive au setup 1776, les trois pulses propres aux
JE ne peuvent pas produire de contenu actif supplémentaire ; l'erreur de
résolution est toutefois émise au chargement. Une correction autonome n'est
pas démontrée sans auditer la résolution VFS de l'ensemble du namespace. Toute
suppression de pulse, modification de Sick Man ou copie d'événement risquerait
de modifier le design 1776. Ces diagnostics sont donc documentés et reportés,
sans sélection ni changement.

## 11. Comparaisons trois voies

### 11.1 Romania — candidat sélectionné

| Élément | Fork | Source hotfix | Vanilla 1.13 |
| --- | --- | --- | --- |
| Fichier | `common/journal_entries/00_romania.txt` | même chemin | même chemin |
| Hash | `D5925DEB54D4E0E4BB6E96DAF5106CAADBA35CC18E451D4898A7F1B7AA1AE078` | `74149D3A3B778732DE318D7FB522CE4255289B410F6184625BA9670E6CCCAB9A` | `9B5C9A9D06DAA420030BBC3B31581CD030356145FD31E1589E590AB9DF904A51` |
| `je_unite_the_principalities` | ancien champ, ligne 76 | API contexte/non impliqué | API contexte/non impliqué |
| `je_all_for_one` | ancien champ, ligne 149 | API contexte/non impliqué | API contexte/non impliqué |

Preuve fonctionnelle : deux erreurs parser directes dans le nouveau log et
convergence exacte source/vanilla sur les deux propriétés modernes. Le futur
delta est d'un fichier, deux objets, deux hunks, deux suppressions et deux
additions :

```diff
-    should_be_pinned_by_default = yes
+    should_be_pinned_by_default_uninvolved_or_context = yes
```

Dette adjacente exclue : source ajoute deux gates
`geographic_region_greater_romania` absentes de vanilla et remplace une
itération par `any_state_in_poland_old`/un helper roumain selon les versions.
Ces écarts de lobby, géographie, scope, tooltip, visibilité, progression,
pulse, scripted buttons et complétion ne seront pas importés. Aucune
localisation n'est ajoutée : les clés anglaises et françaises des deux JE
existent dans vanilla. Aucune protection active ni collision n'est identifiée.
Le setup 1776 conserve WAL et MOL.

Snapshot futur calculé en mémoire, sans modifier le fichier : UTF-8 BOM, LF,
zéro CRLF, 48/48 accolades, 3 857 → 3 901 octets, hash attendu
`DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578`.
Rollback exact : remplacer les deux propriétés modernes par les deux
propriétés anciennes, ou restaurer le blob initial au hash ci-dessus. Priorité
`P0_REQUIRED_CORRECTION`. Un runtime humain condensé sera nécessaire après les
contrôles statiques : charger une partie neuve avec WAL, vérifier l'entrée
potentielle lisible, avancer au 2 janvier 1776, fermer le jeu puis confirmer les
deux diagnostics de pinning ramenés à zéro.

### 11.2 Merchant Banking GEN/VEN

| Chemin | Fork | Source hotfix | Vanilla |
| --- | --- | --- | --- |
| `common/history/countries/gen - genoa.txt` | `law_traditionalism`, hash `B4EC2FB8C9916425FBFFBAA1CEF7FEDFB63C2E0510352A4744E088748AFD80EF` | `law_merchant_banking`, hash `05A10969F0C7C378920E3224F83C1BC445486143F130874AAA19DE9592E98EAF` | absent |
| `common/history/countries/ven - venetia.txt` | `law_traditionalism`, hash `33503E48A69A431AD10ABC2AD71AF9D2147CDA6F19C0CD6C0C04434C1E5425B1` | `law_merchant_banking`, hash `8DDDA736260B18E2412DA1AD9516336938E19BA7266FD79992BD31E84013E5BA` | absent |

Le changelog source 2.3 annonce explicitement « New laws Merchant Banking
(Maritime Republics) ». Le fork s'arrête avant cette entrée. La loi est déjà
définie dans `common/laws/00_inject_laws.txt`, son icône
`gfx/interface/icons/law_icons/merchant_banks.dds` existe et les localisations
anglaise et française de la loi et de sa description existent.

Le delta sérieux est de deux fichiers, deux pays, deux hunks, deux additions et
deux suppressions. Les blocs adjacents de la source ajoutent un nom spécifique
aux propriétaires terriens et retirent `law_merchant_navy` : ces deux écarts
sont expressément exclus. Aucune autre loi et aucun fichier NAVY ne doivent
changer. Les hashes futurs d'une substitution isolée seraient
`7FC780AB8A8793E1DD1B3E6A32022807CED720FB1BE3F3D63D9EC6FDE9F43327`
pour GEN et
`51A65341A2E3947A3D7D71BC3E3B1F31DA5CCD9D000D200C75BFB9570010B6DB`
pour VEN. Rollback : remettre `law_traditionalism` aux deux lignes 30.

Le candidat est fonctionnellement justifié malgré l'absence vanilla, mais il
est `P1_REQUIRED_HOTFIX_DELTA`, derrière une erreur parser 1.13 convergente. Un
runtime humain devra vérifier les lois initiales de GEN et VEN et la
préservation de `law_merchant_navy`.

### 11.3 Navigation Acts

Les cinq fichiers sont :

- `common/history/countries/gbr - great britain.txt`, ligne source 53 ;
- `common/history/countries/hbc - hudson bay company.txt`, ligne source 13 ;
- `common/history/countries/nbs - new brunswick.txt`, ligne source 18 ;
- `common/history/countries/ont - ontario.txt`, ligne source 18 ;
- `common/history/countries/ora - oranje.txt`, ligne source 13.

Le fork active `law_mercantilism`; la source active
`law_mercantilism_navigation_acts`; vanilla 1.13 active
`law_protectionism` pour GBR et `law_mercantilism` pour HBC/NBS/ONT/ORA.
Source et vanilla divergent donc fonctionnellement. La justification custom
est le changelog 2.3 : « Navigation Acts (Britain and it's colonies) ». La loi,
l'icône `regulation_acts.dds` et les localisations anglaise/française sont déjà
présentes.

La taille minimale est de cinq fichiers, cinq pays, cinq hunks, cinq additions
et cinq suppressions. Les autres écarts de chaque fichier sont exclus. GBR
entre en collision avec le domaine NAVY protégé et la source déplace aussi
`law_professional_navy`; BIC est hors périmètre et doit conserver
`law_frontier_colonization`. Le runtime humain devrait vérifier les lois de
GBR et de ses quatre pays associés. Rollback : remettre
`law_mercantilism` dans chacun des cinq hunks. Priorité
`P1_REQUIRED_HOTFIX_DELTA`, reporté pour collision et divergence vanilla.

### 11.4 Petits alignements 1.13

Les seize fichiers parser classés `VANILLA_1_13_ALIGNMENT_REQUIRED`
représentent 94 occurrences. Les comparaisons ciblées montrent :

- `01_coup.txt` : une erreur et un objet, mais 10 hunks source/fork et quatre
  hunks source/vanilla touchent variables de localisation, cleanup, cooldown,
  invalidité et scopes ; candidat immédiat écarté ;
- `04_imperialism_of_promise.txt` : une erreur et un objet, mais les rôles
  personnage et le tooltip bureaucratie divergent, y compris entre source et
  vanilla ; écarté ;
- `00_tutorial.txt` : 52 erreurs, 40 objets et 57 hunks source/fork ; portée
  massive ;
- Canada/Australie, fascisme, unification allemande, Pologne, Portugal,
  colonies portugaises et Afrique espagnole : plusieurs hunks fonctionnels
  adjacents, à séparer avant correction ;
- Afghanistan et Corée : diffs massifs, non atomiques ;
- Question orientale : Russie et Autriche protégées ;
- People's Springtime : domaine Révolution française protégé ;
- Roumanie : seuls les deux hunks de pinning convergents forment un sous-bloc
  court, reproductible et sans protection.

Les localisations anglaises et françaises de la Roumanie existent dans
vanilla ; aucun fichier de localisation n'est requis.

### 11.5 Inconnus pertinents

Les 87 `UNKNOWN_REQUIRES_REVIEW` restent des lignes d'inventaire, pas des
correctifs. Merchant Banking et Navigation Acts disposent d'une preuve
changelog précise et de dépendances déjà intégrées ; ils sont donc les deux
inconnus/deltas custom pertinents examinés en profondeur. Aucun autre inconnu
n'a été promu sur une simple différence de hash. Les fichiers sans log moteur,
changelog, convergence trois voies ou dépendance déjà intégrée restent en
revue.

## 12. Top 3

| Rang | Phase candidate | Fichiers | Objets | Hunks | Priorité | Preuve | Collision | Runtime |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | `HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT` | 1 | 2 | 2 | P0 | 2 erreurs parser et convergence source/vanilla | aucune | humain, 1 lancement |
| 2 | `HOTFIX_6A11F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW` | 2 | 2 | 2 | P1 | changelog 2.3, loi/icône/loc déjà présentes | aucune | humain, lois GEN/VEN |
| 3 | `HOTFIX_6A12R_NAVIGATION_ACTS_STARTING_LAW_AUDIT` | 5 | 5 | 5 | P1 | changelog 2.3 et dépendances présentes | GBR/NAVY ; divergence vanilla | audit puis runtime |

Exactement un candidat est sélectionné : le rang 1. Merchant Banking est
reporté uniquement parce qu'une erreur parser/API 1.13 convergente est
prioritaire. Navigation Acts est reporté parce que sa divergence avec vanilla
et la collision GBR/NAVY exigent une résolution distincte.

## 13. Futur périmètre fermé

La future phase 6A.10F pourra modifier uniquement :

1. `common/journal_entries/00_romania.txt` ;
2. son rapport
   `docs/reports/hotfix/_index/HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT.md` ;
3. `docs/reports/hotfix/INDEX.md` ;
4. `docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv` ;
5. `docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv` ;
6. `docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
7. `docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Deux objets seulement : `je_unite_the_principalities` et `je_all_for_one`.
Deux hunks seulement : les propriétés aux lignes initiales 76 et 149. Aucun
changement de géographie, lobby, visibilité, condition, scripted button,
pulse, progression, effet, scope, tooltip ou localisation.

Le futur rollback exact est la substitution inverse dans les deux objets et la
vérification du hash initial
`D5925DEB54D4E0E4BB6E96DAF5106CAADBA35CC18E451D4898A7F1B7AA1AE078`.

## 14. Documents modifiés par 6A.10

Exactement six documents :

1. le présent rapport ;
2. `docs/reports/hotfix/INDEX.md` ;
3. `HOTFIX_REPORT_INDEX.csv` ;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv` ;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md` ;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

## 15. Contrôles finaux et état Git

Les contrôles finaux confirment :

- zéro fichier gameplay modifié ;
- exactement six documents de phase modifiés/créés ;
- exactement trois candidats et exactement un sélectionné ;
- catégories exclusives, somme 161, lignes exploitables 111 ;
- baseline recalculée à 378 diagnostics et 142 fichiers ;
- top 25 et liste exhaustive publiés ;
- Tanzimat séparé du pinning ;
- blocs clos et protections non rouverts ;
- BIC, stash NAVY-3C-3, source hotfix, vanilla, `bject` et recherche
  technologique intacts ;
- CSV valides, `git diff --check` propre et index staged vide ;
- aucun processus Victoria 3, `dowser` ou Paradox ;
- aucun lancement, contrôle du jeu ou commit automatique ;
- phase 6A.10F non commencée.

HEAD final identique au HEAD initial :
`a46aeb5d491478ccf7fc0beecac15f5d74bd404b`.

La décision de commit reste manuelle.

## 16. Verdicts

`HOTFIX_6A10_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`

`NO_GAMEPLAY_CHANGED`

`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`

`NEXT_EXECUTION_PHASE = HOTFIX_6A10F_ROMANIA_TWO_JE_PINNING_1_13_ALIGNMENT`
