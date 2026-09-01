# TECH6B3G — Starting Technology Reconciliation Audit

Status: `PASS` · `AUDIT_ONLY` · `NO_GAMEPLAY_CHANGE`  
Reference absolue: `1776-01-01`  
Vanilla canonique: `C:\Games\Victoria 3\game` · Victoria 3 `1.13.11`

## A. Checkpoint Git

Branche créée: `tech6b3g-starting-tech-reconciliation-audit`. Aucun reset, clean, stash, commit ou push. Le worktree TECH6B1–F a été conservé. Le checkpoint pré-audit comptait 142 entrées non-TECH6B3G et avait le digest documentaire de contrôle `4a144b8289f3c7a578b3f57afbdde1269ab3f17e2be424df1ece66b4bc4492f2`.

## B. Sources et méthode

Ordre d'autorité appliqué: décisions utilisateur récentes, overlay gameplay TECH6B3F, arbre 1776 effectif, setup au `1776-01-01`, puis vanilla 1.13.11 comme provenance mécanique seulement.

Sources internes lues et utilisées:

- `TECH6B3F_HIDDEN_TECH_RESPONSIBILITY_IMPLEMENTATION_REPORT.md` et sa matrice différée complète (`B3F`);
- `TECH6B3E_HIDDEN_TECH_RESPONSIBILITY_AUDIT_REPORT.md` et sa matrice complète (`B3E`);
- `TECH6B3D_TREE_CORRECTION_IMPLEMENTATION_REPORT.md` (`B3D`);
- `TECH6B3C_TREE_HUMAN_REVIEW_REPORT.md` (`B3C`);
- `TECH_TREE_1700_1836_INTEGRATED_V1.md/.csv` et les 285 définitions technologiques effectives (`D1`);
- overlay effectif des country histories, comparé sans sensibilité à la casse (`D2`);
- `C:\Games\Victoria 3\game\common\scripted_effects\00_starting_inventions.txt` (`V1`).

Références historiques ciblées:

- `H2` — [UK Parliament, création de la Metropolitan Police en 1829](https://www.parliament.uk/about/living-heritage/transformingsociety/laworder/policeprisons/overview/metropolitanpolice/);
- `H3` — [Routledge Encyclopedia of Philosophy, apparition du socialisme dans les années 1820–1830](https://www.rep.routledge.com/articles/thematic/socialism/v-1/sections/defining-socialism);
- `H4` — [U.S. Army, origine et généralisation du corps napoléonien](https://www.armyupress.army.mil/Portals/7/Research-and-Books/Archives/2017/PDF/December-2017-EssentialToSuccess.pdf);
- `H5` — [The Mariners' Museum, brevets de propulsion à hélice de 1836](https://catalogs.marinersmuseum.org/object/CL2749);
- `H6` — [Mackinac State Historic Parks, mousquet standard Pattern 1769](https://www.mackinacparks.com/blog/a-short-land-pattern-musket-of-1769/);
- `H7` — [Japan Search, ancienneté de la sériciculture chinoise et japonaise](https://jpsearch.go.jp/en/gallery/ndl-PkaAaPDloqW);
- `H9` — [Cambridge, institutions financières et compagnies par actions des XVIIe–XVIIIe siècles](https://www.cambridge.org/core/journals/journal-of-economic-history/article/financial-developments-in-london-in-the-seventeenth-century-the-financial-revolution-revisited/C79E018511FBB0F5690DE23F3248123C);
- `H10` — exemples institutionnels d'académies techniques avant 1776: [Woolwich 1741, National Army Museum](https://www.nam.ac.uk/explore/sandhurst-officers-and-role-history), [Mézières 1748, Musée du Génie](https://www.musee-du-genie-angers.fr/fpdb/20495135-10objets-juillet2024-poursite.pdf) et [école ottomane d'ingénierie navale 1773, İTÜ](https://mtte.itu.edu.tr/hakkimizda/i-t%C3%BC-tarih%C3%A7esi);
- `H11` — [Université de Zurich, surveys et cartes provinciales Tokugawa](https://www.adfontes.uzh.ch/tutorium/old-japanese-maps/surveying);
- `H12` — [Oxford Academic, destruction de la flotte marathe en 1756](https://academic.oup.com/reference/62399/reference-article-abstract/555376418);
- `H13` — [Cambridge, marine iranienne au XVIIIe siècle](https://www.cambridge.org/core/journals/iranian-studies/article/abs/iranian-navy-in-the-gulf-during-the-eighteenth-century/23F5E61D5C986BAED35282716DA32760);
- `H14` — [Encyclopaedia Iranica, opérations et dépendance navale de la Perse zand](https://www.iranicaonline.org/articles/east-india-company-british-ii-the-afsharid-zand-and-qajar-periods/);
- `H15` — [étude académique des institutions juridiques et administratives du Qing au XVIIIe siècle](https://www.jstor.org/stable/jj.17331655).

La recherche externe a été réservée aux arbitrages qui pouvaient changer l'action. Les autres lignes emploient le design daté du mod et une formulation prudente plutôt qu'une fausse précision nationale.

## C. Baseline des 229 grants

| Métrique | Valeur |
|---|---|
| TOTAL_DEFERRED | 229 |
| DIRECT_COUNTRY_GRANTS | 165 |
| SCRIPTED_TIER_GRANTS | 64 |
| OTHER_STARTING_GRANTS | 0 |
| UNIQUE_COUNTRIES_AFFECTED | 104 |
| UNIQUE_HIDDEN_TECH_IDS_GRANTED | 36 |
| UNIQUE_SOURCE_FILES | 107 |

Les quatre lignes vanilla PRG (`central_archives`, `egalitarianism`, `empiricism`, `mass_communication`) sont conservées dans le total obligatoire de 229, mais l'audit constate qu'elles sont shadowées par `prg - Paraguay.txt` sous le filesystem Windows insensible à la casse. Elles ne sont donc pas des grants runtime effectifs.

## D. Typologie des grants

Les 165 grants directs sont arbitrés pays par pays. Les 64 grants de tiers sont arbitrés comme architecture globale. Aucun troisième mécanisme n'est présent. Une ligne reçoit exactement une des six actions autorisées; aucune substitution token-par-token n'est utilisée.

| Action | Nombre |
|---|---|
| ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH | 17 |
| HUMAN_REVIEW_REQUIRED | 8 |
| KEEP_HIDDEN_ALIAS_COMPATIBILITY_ONLY | 4 |
| REMOVE_STARTING_GRANT | 46 |
| REPLACE_WITH_EARLIER_VISIBLE_TECH | 81 |
| REPLACE_WITH_VISIBLE_TECH | 73 |

## E. Technologies cachées concernées

| Hidden tech | Grants | Countries | Tier effects | Successeur B3E | Hidden era | Successor era |
|---|---|---|---|---|---|---|
| academia | 49 | ARG,AUS,BEO,BIC,BOL,BRZ,CRO,DEN,DENNOR,ECU,FRA,GAL,GBR,GEN,HAI,HBC,HUN,IR1,IREK,JAP,LAN,LOU,MEX,NBS,NET,NOR,NVS,ONT,ORG,PEU,POR,PRG,PRU,QUE,SC1,SC2,SC3,SC4,SPA,SWE,TRS,TUR,UCA,URU,USA,VEN,VNZ | effect_starting_technology_tier_3_tech | specialized_technical_academies | era_7 | era_3 |
| admiralty | 4 | MARATH,PER | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech | state_dockyard_systems | era_7 | era_1 |
| army_reserves | 1 | — | effect_starting_technology_tier_3_tech | corps_organization | era_7 | era_5 |
| artillery | 2 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech | standardized_field_artillery | era_7 | era_3 |
| central_archives | 2 | PRG | effect_starting_technology_tier_1_tech | central_statistical_offices | era_7 | era_5 |
| central_banking | 1 | — | effect_starting_technology_tier_1_tech | institutionalized_public_credit | era_7 | era_1 |
| centralization | 3 | JAP | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech | systematic_administrative_statistics | era_7 | era_2 |
| corporate_charters | 3 | DEI | effect_starting_technology_tier_1_tech,effect_starting_technology_tier_2_tech | joint_stock_companies | era_4 | era_6 |
| currency_standards | 1 | — | effect_starting_technology_tier_3_tech | scientific_metrology | era_7 | era_4 |
| democracy | 3 | KAU | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech | constitutional_government | era_7 | era_4 |
| dialectics | 3 | KRA | effect_starting_technology_tier_1_tech,effect_starting_technology_tier_2_tech | socialism | era_7 | era_7 |
| drydocks | 2 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech | mechanized_naval_dockyards | era_7 | era_5 |
| egalitarianism | 3 | PRG | effect_starting_technology_tier_1_tech,effect_starting_technology_tier_2_tech | liberal_constitutionalism | era_7 | era_6 |
| empiricism | 11 | CHL,CLM,GRE,IQU,LAN,NPU,PRG,SPC,SPU,TEX,VNZ | — | codified_practical_knowledge | era_7 | era_3 |
| enclosure | 4 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech,effect_starting_technology_tier_5_tech,effect_starting_technology_tier_6_tech | improved_husbandry | era_4 | era_1 |
| gunsmithing | 2 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech | regulated_small_arms | era_7 | era_2 |
| intensive_agriculture | 1 | — | effect_starting_technology_tier_1_tech | advanced_crop_rotations | era_5 | era_3 |
| international_trade | 34 | AGC,ARS,ASH,AWS,BEN,BGI,BHV,BRG,BST,CHI,CRI,DAH,DUR,ETH,GLD,GZA,HDY,ISQ,MAD,MARATH,MBS,MJT,OYO,PHL,PLY,SWZ,TGI,WBL,WSG,WTU,ZUL | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech,effect_starting_technology_tier_5_tech | commercial_insurance_markets | era_7 | era_1 |
| law_enforcement | 14 | AUS,BEO,BIC,CHI,CRO,GAL,HUN,PER,PHI,POR,RUS,SIL,TRS | effect_starting_technology_tier_3_tech | professional_civil_policing | era_7 | era_6 |
| line_infantry | 34 | AUS,BEO,BIC,CRO,CUB,DEN,DENNOR,FRA,GAL,GBR,GEN,GR5,HBC,HUN,NBS,NET,NOR,NVS,ONT,ORG,PAN,PAP,PCO,POR,PRU,QUE,RUS,SPA,SWE,TRS,USA,VEN | effect_starting_technology_tier_3_tech | regulated_small_arms | era_7 | era_2 |
| mandatory_service | 5 | BUR,GBR,HBC,PAN | effect_starting_technology_tier_3_tech | corps_organization | era_7 | era_5 |
| manufacturies | 3 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech,effect_starting_technology_tier_5_tech | interchangeable_manufacture | era_4 | era_6 |
| mass_communication | 3 | GRE,PRG,SPC | — | periodical_print_networks | era_7 | era_1 |
| military_drill | 3 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech,effect_starting_technology_tier_5_tech | light_infantry_tactics | era_7 | era_3 |
| napoleonic_warfare | 2 | EGY,SPC | — | corps_organization | era_7 | era_5 |
| navigation | 3 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech,effect_starting_technology_tier_5_tech | marine_chronometry | era_7 | era_3 |
| power_of_the_purse | 1 | — | effect_starting_technology_tier_1_tech | state_dockyard_systems | era_7 | era_1 |
| prospecting | 2 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech | applied_mineralogy | era_7 | era_3 |
| rationalism | 7 | BST,KAU,PHL,WBL | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech,effect_starting_technology_tier_5_tech | codified_practical_knowledge | era_7 | era_3 |
| screw_frigate | 1 | — | effect_starting_technology_tier_1_tech | iron_hull_construction | era_7 | era_6 |
| sericulture | 4 | CAM,DAI,SIA,WAL | — | selective_breeding | era_7 | era_3 |
| standing_army | 4 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech,effect_starting_technology_tier_5_tech,effect_starting_technology_tier_6_tech | corps_organization | era_7 | era_5 |
| steelworking | 2 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech | puddling_and_rolling | era_7 | era_4 |
| tech_bureaucracy | 5 | PHL,WBL | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech,effect_starting_technology_tier_5_tech | central_statistical_offices | era_7 | era_5 |
| urban_planning | 3 | JAP,PER | effect_starting_technology_tier_3_tech | modern_sewerage | era_7 | era_8 |
| urbanization | 4 | — | effect_starting_technology_tier_3_tech,effect_starting_technology_tier_4_tech,effect_starting_technology_tier_5_tech,effect_starting_technology_tier_6_tech | paved_roads | era_7 | era_10 |

`psychiatry` ne possède aucun Starting Grant dans ce périmètre (`PSYCHIATRY_STARTING_GRANTS = 0`). La règle d'interdiction `psychiatry → psychoanalysis` reste néanmoins documentée pour l'implémentation future.

## F. Audit des scripted tiers

Le fichier effectif est exclusivement vanilla 1.13.11. L'overlay complet contient 478 country setups: tier 1 = 1, tier 2 = 9, tier 3 = 14, tier 4 = 209, tier 5 = 62, tier 6 = 114, tier 7 = 69. Contrairement au seul sous-ensemble de fichiers du mod, les fichiers vanilla non shadowés font donc encore usage des tiers 1–3.

Comptage des `add_technology_researched` explicites actuels (les tiers 1 et 2 ajoutent aussi implicitement toute l'era 1):

| Tier | Setups | Techs | Visible | Hidden | Production | Military | Society | Eras actuelles |
|---|---|---|---|---|---|---|---|---|
| 1 | 1 | 13 | 5 | 8 | 4 | 4 | 5 | era_2:1, era_4:1, era_5:3, era_6:2, era_7:6 |
| 2 | 9 | 5 | 2 | 3 | 2 | 0 | 3 | era_2:1, era_4:1, era_5:1, era_7:2 |
| 3 | 14 | 31 | 7 | 24 | 7 | 10 | 14 | era_1:3, era_3:1, era_4:4, era_7:23 |
| 4 | 209 | 20 | 3 | 17 | 6 | 7 | 7 | era_1:3, era_4:2, era_7:15 |
| 5 | 62 | 10 | 1 | 9 | 3 | 3 | 4 | era_1:1, era_4:2, era_7:7 |
| 6 | 114 | 3 | 0 | 3 | 1 | 1 | 1 | era_4:1, era_7:2 |
| 7 | 69 | 0 | 0 | 0 | 0 | 0 | 0 | — |

Les 18 grants visibles explicites ci-dessous ne font pas partie des 229 responsabilités cachées et ne sont donc pas ajoutés aux six compteurs principaux. Ils sont néanmoins arbitrés ici pour éviter de reconstruire des tiers qui conserveraient des anachronismes visibles:

| Tier | Visible tech | Category | Current era | Future action | Target | Target era | Reason |
|---|---|---|---|---|---|---|---|
| 1 | railways | production | era_6 | REMOVE_STARTING_GRANT | — | — | Era 6 and rail transport are not a 1776 starting baseline. |
| 1 | mechanical_tools | production | era_5 | REPLACE_WITH_EARLIER_VISIBLE_TECH | precision_boring | era_4 | Keep early precision capability without granting the era-5 machine-tool system. |
| 1 | atmospheric_engine | production | era_2 | KEEP_CURRENT_VISIBLE_TECH | atmospheric_engine | era_2 | The era-2 pumping engine is established before 1776. |
| 1 | general_staff | military | era_6 | REMOVE_STARTING_GRANT | — | — | The era-6 general-staff system is later than the reference date. |
| 1 | percussion_cap | military | era_5 | REMOVE_STARTING_GRANT | — | — | Percussion-cap service arms are a 19th-century capability. |
| 2 | mechanical_tools | production | era_5 | REPLACE_WITH_EARLIER_VISIBLE_TECH | precision_boring | era_4 | Use the earlier precision capability rather than era-5 mechanical tools. |
| 2 | atmospheric_engine | production | era_2 | KEEP_CURRENT_VISIBLE_TECH | atmospheric_engine | era_2 | The technology is chronologically valid before 1776. |
| 3 | shaft_mining | production | era_1 | KEEP_CURRENT_VISIBLE_TECH | shaft_mining | era_1 | Era-1 mining capacity is valid. |
| 3 | distillation | production | era_1 | KEEP_CURRENT_VISIBLE_TECH | distillation | era_1 | Era-1 distillation is valid. |
| 3 | cotton_gin | production | era_4 | REMOVE_STARTING_GRANT | — | — | The era-4 node represents the post-1776 mechanized cotton-gin transition. |
| 3 | romanticism | society | era_7 | REMOVE_STARTING_GRANT | — | — | The post-1836 compatibility node is era 7 and inappropriate at start. |
| 3 | international_relations | society | era_1 | KEEP_CURRENT_VISIBLE_TECH | international_relations | era_1 | Era-1 diplomatic capacity is valid. |
| 3 | colonization | society | era_4 | REMOVE_STARTING_GRANT | — | — | A global tier grant overstates a polity-specific colonial state capacity. |
| 3 | medical_degrees | society | era_3 | KEEP_CURRENT_VISIBLE_TECH | medical_degrees | era_3 | Formal medical qualification is a valid era-3 capability for this tier. |
| 4 | shaft_mining | production | era_1 | KEEP_CURRENT_VISIBLE_TECH | shaft_mining | era_1 | Era-1 mining capacity is valid. |
| 4 | distillation | production | era_1 | KEEP_CURRENT_VISIBLE_TECH | distillation | era_1 | Era-1 distillation is valid. |
| 4 | international_relations | society | era_1 | KEEP_CURRENT_VISIBLE_TECH | international_relations | era_1 | Era-1 diplomatic capacity is valid. |
| 5 | shaft_mining | production | era_1 | KEEP_CURRENT_VISIBLE_TECH | shaft_mining | era_1 | Era-1 mining capacity is valid. |

`add_era_researched = era_1` des tiers 1 et 2 reste une opération implicite distincte. Elle devra être développée en liste explicite ou validée comme bloc complet pendant TECH6B3H, afin que l'ajout futur de nœuds era 1 ne modifie pas silencieusement les starts.

Constats d'architecture:

- les tiers 3 et 4 surreprésentent la marine, y compris pour des polities sans littoral;
- plusieurs paires se doublonnent après migration (`gunsmithing/line_infantry`, `centralization/tech_bureaucracy`, `currency_standards/tech_bureaucracy`);
- les successeurs `corps_organization`, `professional_civil_policing`, `iron_hull_construction`, `mechanized_naval_dockyards`, `modern_sewerage` et `paved_roads` sont trop tardifs pour une substitution globale en 1776;
- les tiers donnent parfois un enfant sans tous ses parents. Le moteur accepte un grant recherché direct; cela ne justifie pas de distribuer automatiquement tous les parents;
- `urbanization` est le seul alias de ce périmètre dont le grant garde un effet runtime indispensable: il verrouille encore les deux bâtiments urbains différés.

### Tier 1

AFFECTED_COUNTRY_SETUPS = 1

| Hidden tech | Category | Action | Target | Era | Reason |
|---|---|---|---|---|---|
| central_archives | society | REPLACE_WITH_VISIBLE_TECH | systematic_administrative_statistics | era_2 | Tier 1: A central archive is best represented by the era-2 administrative-statistics capacity. Reference date is strictly 1776-01-01. |
| central_banking | society | ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH | institutionalized_public_credit | era_1 | Tier 1: Tier 1 already researches all era-1 nodes, including institutionalized_public_credit. Reference date is strictly 1776-01-01. |
| corporate_charters | society | ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH | stock_exchange | era_1 | Tier 1: Tier 1 already researches all era-1 nodes; stock_exchange covers early chartered-capital practice without granting the era-6 successor. Reference date is strictly 1776-01-01. |
| dialectics | society | REMOVE_STARTING_GRANT | — | — | Tier 1: Neither socialism nor mature dialectical politics belongs in a blanket 1776 starting tier. Reference date is strictly 1776-01-01. |
| egalitarianism | society | REMOVE_STARTING_GRANT | — | — | Tier 1: A blanket advanced-power grant would turn a country-specific revolutionary rights trajectory into a generic capacity. Reference date is strictly 1776-01-01. |
| intensive_agriculture | production | REPLACE_WITH_VISIBLE_TECH | advanced_crop_rotations | era_3 | Tier 1: Advanced crop rotations are the period-appropriate agricultural capability. Reference date is strictly 1776-01-01. |
| power_of_the_purse | military | ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH | state_dockyard_systems | era_1 | Tier 1: Tier 1 already researches every era-1 node, including state_dockyard_systems. Reference date is strictly 1776-01-01. |
| screw_frigate | military | REPLACE_WITH_EARLIER_VISIBLE_TECH | scientific_naval_architecture | era_2 | Tier 1: Screw propulsion and iron-hull construction are post-1830; scientific naval architecture is the earlier valid abstraction. Reference date is strictly 1776-01-01. |

### Tier 2

AFFECTED_COUNTRY_SETUPS = 9

| Hidden tech | Category | Action | Target | Era | Reason |
|---|---|---|---|---|---|
| corporate_charters | society | ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH | stock_exchange | era_1 | Tier 2: Tier 2 already researches all era-1 nodes, including stock_exchange. Reference date is strictly 1776-01-01. |
| dialectics | society | REMOVE_STARTING_GRANT | — | — | Tier 2: The grant is a vanilla 1836 ideological inheritance; no socialism is justified at 1776-01-01. Reference date is strictly 1776-01-01. |
| egalitarianism | society | REMOVE_STARTING_GRANT | — | — | Tier 2: Rights capacity must be assigned by polity, not granted to an entire tier. Reference date is strictly 1776-01-01. |

### Tier 3

AFFECTED_COUNTRY_SETUPS = 14

| Hidden tech | Category | Action | Target | Era | Reason |
|---|---|---|---|---|---|
| academia | society | REPLACE_WITH_VISIBLE_TECH | specialized_technical_academies | era_3 | Tier 3: Tier 3 is narrow enough for an era-3 technical-education baseline, subject to future country overrides. Reference date is strictly 1776-01-01. |
| admiralty | military | REMOVE_STARTING_GRANT | — | — | Tier 3: A generic tier includes landlocked polities; naval administration must be country-specific. Reference date is strictly 1776-01-01. |
| army_reserves | military | REMOVE_STARTING_GRANT | — | — | Tier 3: Organized reserves and corps-scale mobilization are later than 1776. Reference date is strictly 1776-01-01. |
| artillery | military | REPLACE_WITH_VISIBLE_TECH | standardized_field_artillery | era_3 | Tier 3: Standardized field artillery fits the 1750-1774 capability band. Reference date is strictly 1776-01-01. |
| centralization | society | ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH | systematic_administrative_statistics | era_2 | Tier 3: The tech_bureaucracy row in this tier is recommended to supply the same visible capacity. Reference date is strictly 1776-01-01. |
| currency_standards | society | ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH | systematic_administrative_statistics | era_2 | Tier 3: Administrative standardization is already supplied by the recommended tech_bureaucracy replacement; scientific metrology is too specific. Reference date is strictly 1776-01-01. |
| democracy | society | REMOVE_STARTING_GRANT | — | — | Tier 3: Constitutional government in 1776 must be polity-specific, not a tier default. Reference date is strictly 1776-01-01. |
| drydocks | military | REMOVE_STARTING_GRANT | — | — | Tier 3: Mechanized dockyards are too late and naval infrastructure cannot be blanket-granted. Reference date is strictly 1776-01-01. |
| enclosure | production | REPLACE_WITH_VISIBLE_TECH | improved_husbandry | era_1 | Tier 3: Improved husbandry preserves a broad agrarian baseline without imposing one land-tenure system. Reference date is strictly 1776-01-01. |
| gunsmithing | military | ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH | regulated_small_arms | era_2 | Tier 3: The line_infantry row in the same tier is recommended to grant regulated_small_arms. Reference date is strictly 1776-01-01. |
| international_trade | society | REPLACE_WITH_VISIBLE_TECH | commercial_insurance_markets | era_1 | Tier 3: For this relatively advanced tier, established commercial insurance is a defensible early financial capability. Reference date is strictly 1776-01-01. |
| law_enforcement | society | REMOVE_STARTING_GRANT | — | — | Tier 3: Professional civil policing is an early-19th-century institution and should be country-specific. Reference date is strictly 1776-01-01. |
| line_infantry | military | REPLACE_WITH_VISIBLE_TECH | regulated_small_arms | era_2 | Tier 3: The explicit old unit capability now belongs to regulated_small_arms. Reference date is strictly 1776-01-01. |
| mandatory_service | military | REMOVE_STARTING_GRANT | — | — | Tier 3: Mass-service organization and corps capacity are post-revolutionary rather than a 1776 baseline. Reference date is strictly 1776-01-01. |
| manufacturies | production | REPLACE_WITH_EARLIER_VISIBLE_TECH | organized_textile_production | era_1 | Tier 3: Proto-industrial organized production is appropriate; interchangeable manufacture is not. Reference date is strictly 1776-01-01. |
| military_drill | military | REPLACE_WITH_VISIBLE_TECH | light_infantry_tactics | era_3 | Tier 3: The visible era-3 tactics node is the closest period-compatible military practice. Reference date is strictly 1776-01-01. |
| navigation | military | REMOVE_STARTING_GRANT | — | — | Tier 3: Marine chronometry was specialized and a generic tier also contains landlocked countries. Reference date is strictly 1776-01-01. |
| prospecting | production | REPLACE_WITH_VISIBLE_TECH | applied_mineralogy | era_3 | Tier 3: Applied mineralogy is a valid mid-18th-century knowledge capacity for this tier. Reference date is strictly 1776-01-01. |
| rationalism | society | REPLACE_WITH_VISIBLE_TECH | codified_practical_knowledge | era_3 | Tier 3: Codified practical knowledge preserves the non-ideological knowledge role. Reference date is strictly 1776-01-01. |
| standing_army | military | REMOVE_STARTING_GRANT | — | — | Tier 3: The era-5 corps successor is not a 1776 blanket capacity. Reference date is strictly 1776-01-01. |
| steelworking | production | REPLACE_WITH_EARLIER_VISIBLE_TECH | coke_smelting | era_1 | Tier 3: Puddling and rolling postdates the reference date; coke smelting is the earlier visible metallurgy node. Reference date is strictly 1776-01-01. |
| tech_bureaucracy | society | REPLACE_WITH_EARLIER_VISIBLE_TECH | systematic_administrative_statistics | era_2 | Tier 3: Era-2 administrative statistics is earlier than central statistical offices and fits a state-capacity tier. Reference date is strictly 1776-01-01. |
| urban_planning | society | REMOVE_STARTING_GRANT | — | — | Tier 3: Modern sewerage is far too late and the tier's urbanization alias separately preserves the temporary building gate. Reference date is strictly 1776-01-01. |
| urbanization | society | KEEP_HIDDEN_ALIAS_COMPATIBILITY_ONLY | urbanization | era_7 | Tier 3: The hidden alias still gates building_urban_center and building_construction_sector. Reference date is strictly 1776-01-01. |

### Tier 4

AFFECTED_COUNTRY_SETUPS = 209

| Hidden tech | Category | Action | Target | Era | Reason |
|---|---|---|---|---|---|
| admiralty | military | REMOVE_STARTING_GRANT | — | — | Tier 4: Naval administration is not coherent across a 209-country generic tier. Reference date is strictly 1776-01-01. |
| artillery | military | REPLACE_WITH_VISIBLE_TECH | standardized_field_artillery | era_3 | Tier 4: The visible era-3 node is the period-compatible artillery baseline. Reference date is strictly 1776-01-01. |
| centralization | society | ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH | systematic_administrative_statistics | era_2 | Tier 4: The tech_bureaucracy row in the same tier supplies this visible capacity. Reference date is strictly 1776-01-01. |
| democracy | society | REMOVE_STARTING_GRANT | — | — | Tier 4: A broad tier cannot assign constitutional government accurately in 1776. Reference date is strictly 1776-01-01. |
| drydocks | military | REMOVE_STARTING_GRANT | — | — | Tier 4: Mechanized dockyards are later and naval infrastructure is not universal. Reference date is strictly 1776-01-01. |
| enclosure | production | REPLACE_WITH_VISIBLE_TECH | improved_husbandry | era_1 | Tier 4: Improved husbandry is a broad agrarian baseline without a European land-tenure assumption. Reference date is strictly 1776-01-01. |
| gunsmithing | military | REPLACE_WITH_VISIBLE_TECH | regulated_small_arms | era_2 | Tier 4: Regulated flintlock arms are a defensible baseline for centralized tier-4 polities. Reference date is strictly 1776-01-01. |
| international_trade | society | REMOVE_STARTING_GRANT | — | — | Tier 4: Commercial insurance markets are too specific for 209 diverse setups; direct grants should express exceptional trade capacity. Reference date is strictly 1776-01-01. |
| manufacturies | production | REPLACE_WITH_EARLIER_VISIBLE_TECH | organized_textile_production | era_1 | Tier 4: Organized craft and textile production is earlier than interchangeable manufacture. Reference date is strictly 1776-01-01. |
| military_drill | military | REPLACE_WITH_VISIBLE_TECH | light_infantry_tactics | era_3 | Tier 4: The era-3 tactics abstraction is compatible with regular 18th-century forces. Reference date is strictly 1776-01-01. |
| navigation | military | REMOVE_STARTING_GRANT | — | — | Tier 4: Marine chronometry and naval navigation are not universal across this tier. Reference date is strictly 1776-01-01. |
| prospecting | production | REMOVE_STARTING_GRANT | — | — | Tier 4: Applied mineralogy would overstate a very broad tier; assign it directly where evidenced. Reference date is strictly 1776-01-01. |
| rationalism | society | REPLACE_WITH_VISIBLE_TECH | codified_practical_knowledge | era_3 | Tier 4: The visible era-3 node preserves practical knowledge without ideological anachronism. Reference date is strictly 1776-01-01. |
| standing_army | military | REMOVE_STARTING_GRANT | — | — | Tier 4: Corps organization is post-1800 and cannot be a generic 1776 grant. Reference date is strictly 1776-01-01. |
| steelworking | production | REMOVE_STARTING_GRANT | — | — | Tier 4: Neither puddling nor a universal coke-smelting capacity is justified across this tier. Reference date is strictly 1776-01-01. |
| tech_bureaucracy | society | REPLACE_WITH_EARLIER_VISIBLE_TECH | systematic_administrative_statistics | era_2 | Tier 4: Era-2 administrative statistics is a safer centralized-state abstraction than era-5 statistical offices. Reference date is strictly 1776-01-01. |
| urbanization | society | KEEP_HIDDEN_ALIAS_COMPATIBILITY_ONLY | urbanization | era_7 | Tier 4: The alias still gates both deferred urban buildings and therefore is not inert. Reference date is strictly 1776-01-01. |

### Tier 5

AFFECTED_COUNTRY_SETUPS = 62

| Hidden tech | Category | Action | Target | Era | Reason |
|---|---|---|---|---|---|
| enclosure | production | REPLACE_WITH_VISIBLE_TECH | improved_husbandry | era_1 | Tier 5: Agricultural know-how is valid; European enclosure tenure is not assumed. Reference date is strictly 1776-01-01. |
| international_trade | society | REMOVE_STARTING_GRANT | — | — | Tier 5: Commercial insurance markets are not a safe blanket capacity for this diverse tier. Reference date is strictly 1776-01-01. |
| manufacturies | production | REPLACE_WITH_EARLIER_VISIBLE_TECH | organized_textile_production | era_1 | Tier 5: Organized artisanal production is a safer early abstraction. Reference date is strictly 1776-01-01. |
| military_drill | military | REMOVE_STARTING_GRANT | — | — | Tier 5: The visible era-3 tactics capacity should be assigned by country at this tier. Reference date is strictly 1776-01-01. |
| navigation | military | REMOVE_STARTING_GRANT | — | — | Tier 5: Marine chronometry is neither universal nor required for every centralized polity. Reference date is strictly 1776-01-01. |
| rationalism | society | REPLACE_WITH_VISIBLE_TECH | codified_practical_knowledge | era_3 | Tier 5: Codified practical knowledge represents established learned and administrative practice. Reference date is strictly 1776-01-01. |
| standing_army | military | REMOVE_STARTING_GRANT | — | — | Tier 5: Corps organization is a later capability. Reference date is strictly 1776-01-01. |
| tech_bureaucracy | society | REPLACE_WITH_EARLIER_VISIBLE_TECH | systematic_administrative_statistics | era_2 | Tier 5: A basic era-2 administrative-information capacity is suitable for centralized powers. Reference date is strictly 1776-01-01. |
| urbanization | society | KEEP_HIDDEN_ALIAS_COMPATIBILITY_ONLY | urbanization | era_7 | Tier 5: The alias remains the active gate for both deferred urban buildings. Reference date is strictly 1776-01-01. |

### Tier 6

AFFECTED_COUNTRY_SETUPS = 114

| Hidden tech | Category | Action | Target | Era | Reason |
|---|---|---|---|---|---|
| enclosure | production | REPLACE_WITH_VISIBLE_TECH | improved_husbandry | era_1 | Tier 6: Improved husbandry captures agrarian knowledge without imposing enclosure institutions. Reference date is strictly 1776-01-01. |
| standing_army | military | REMOVE_STARTING_GRANT | — | — | Tier 6: Corps organization is not compatible with the decentralized tier at 1776-01-01. Reference date is strictly 1776-01-01. |
| urbanization | society | KEEP_HIDDEN_ALIAS_COMPATIBILITY_ONLY | urbanization | era_7 | Tier 6: Temporary retention is required solely because two buildings still use this hidden gate. Reference date is strictly 1776-01-01. |

### Tier 7

AFFECTED_COUNTRY_SETUPS = 69

| Hidden tech | Category | Action | Target | Era | Reason |
|---|---|---|---|---|---|
| — | — | — | — | — | No hidden grant |

## G. Audit pays par pays

### AGC — Angoche

COUNTRY_TAG = AGC  
COUNTRY_NAME = Angoche  
SOURCE_FILE = common/history/countries/agc -angoche.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Angoche, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### ARG — Argentina

COUNTRY_TAG = ARG  
COUNTRY_NAME = Argentina  
SOURCE_FILE = common/history/countries/arg - argentina.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Argentina had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### ARS — Arsiland

COUNTRY_TAG = ARS  
COUNTRY_NAME = Arsiland  
SOURCE_FILE = common/history/countries/ars - arsiland.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Arsiland, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### ASH — Ashanti

COUNTRY_TAG = ASH  
COUNTRY_NAME = Ashanti  
SOURCE_FILE = common/history/countries/ash - ashanti.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Ashanti, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### AUS — Austria

COUNTRY_TAG = AUS  
COUNTRY_NAME = Austria  
SOURCE_FILE = common/history/countries/aus - austria.txt  
CURRENT_HIDDEN_GRANTS = academia, law_enforcement, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, romanticism, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Austria's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_legal_codification  
CONFIDENCE = MEDIUM  
RATIONALE = Austria had a codified or centrally administered legal order before 1776, but not the professional civil-police model represented by the era-6 successor. Preserve legal-administrative capacity while avoiding a Metropolitan-Police-era institution.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Austria grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### AWS — Aussa

COUNTRY_TAG = AWS  
COUNTRY_NAME = Aussa  
SOURCE_FILE = common/history/countries/aws - aussa.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Aussa, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### BEN — Benin

COUNTRY_TAG = BEN  
COUNTRY_NAME = Benin  
SOURCE_FILE = common/history/countries/ben - benin.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Benin, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### BEO — Belgium (old setup)

COUNTRY_TAG = BEO  
COUNTRY_NAME = Belgium (old setup)  
SOURCE_FILE = common/history/countries/beo - belgium old.txt  
CURRENT_HIDDEN_GRANTS = academia, law_enforcement, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Belgium (old setup)'s explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_legal_codification  
CONFIDENCE = MEDIUM  
RATIONALE = Belgium (old setup) had a codified or centrally administered legal order before 1776, but not the professional civil-police model represented by the era-6 successor. Preserve legal-administrative capacity while avoiding a Metropolitan-Police-era institution.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Belgium (old setup) grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### BGI — Bagirmi

COUNTRY_TAG = BGI  
COUNTRY_NAME = Bagirmi  
SOURCE_FILE = common/history/countries/bgi - bagirmi.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Bagirmi, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### BHV — Gujarati Prince

COUNTRY_TAG = BHV  
COUNTRY_NAME = Gujarati Prince  
SOURCE_FILE = common/history/countries/bhv - gujarati prince.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = distillation, shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Gujarati Prince, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### BIC — British East India Company

COUNTRY_TAG = BIC  
COUNTRY_NAME = British East India Company  
SOURCE_FILE = common/history/countries/bic - british east india company.txt  
CURRENT_HIDDEN_GRANTS = academia, law_enforcement, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that British East India Company had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_administrative_statistics  
CONFIDENCE = MEDIUM  
RATIONALE = For British East India Company, the grant is better read as colonial administrative reach than as professional civil policing. Move to the earlier state-information capacity and avoid an era-6 police unlock.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit British East India Company grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:2; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### BOL — Bolivia

COUNTRY_TAG = BOL  
COUNTRY_NAME = Bolivia  
SOURCE_FILE = common/history/countries/bol - bolivia.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Bolivia had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### BRG — Borgu

COUNTRY_TAG = BRG  
COUNTRY_NAME = Borgu  
SOURCE_FILE = common/history/countries/brg - borgu.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Borgu, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### BRZ — Brazil

COUNTRY_TAG = BRZ  
COUNTRY_NAME = Brazil  
SOURCE_FILE = common/history/countries/brz - brazil.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Brazil had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### BST — Basuto

COUNTRY_TAG = BST  
COUNTRY_NAME = Basuto  
SOURCE_FILE = common/history/countries/bst - basuto.txt  
CURRENT_HIDDEN_GRANTS = international_trade, rationalism  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Basuto, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

HIDDEN_TECH = rationalism  
OLD_VANILLA_ROLE = codified practical knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = MEDIUM  
RATIONALE = The direct rationalism grant for Basuto is a coarse vanilla tier correction and lacks sufficient evidence for codified_practical_knowledge at the reference date. Avoid duplicating or inflating the broad tier-level knowledge architecture.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:1; REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### BUR — Burma

COUNTRY_TAG = BUR  
COUNTRY_NAME = Burma  
SOURCE_FILE = common/history/countries/bur - burma.txt  
CURRENT_HIDDEN_GRANTS = mandatory_service  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = mandatory_service  
OLD_VANILLA_ROLE = conscription and reserve organization  
TECH6B3E_SUCCESSOR = corps_organization  
SUCCESSOR_ERA = era_5  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = The Burma grant reflects later reserve/conscription organization rather than a defensible 1776 corps system. Do not replace it with era-5 corps_organization or an unrelated tactical node.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:1
  
HUMAN_REVIEW_REQUIRED = NO

### CAM — Cambodia

COUNTRY_TAG = CAM  
COUNTRY_NAME = Cambodia  
SOURCE_FILE = common/history/countries/cam - cambodia.txt  
CURRENT_HIDDEN_GRANTS = sericulture  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = sericulture  
OLD_VANILLA_ROLE = silk cultivation productivity  
TECH6B3E_SUCCESSOR = selective_breeding  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → selective_breeding  
CONFIDENCE = HIGH  
RATIONALE = Sericulture was an established pre-1776 production tradition for Cambodia; selective breeding is the visible owner of the transferred silk throughput responsibility. Preserve the real productive capability without retaining an inert silk alias.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### CHI — China

COUNTRY_TAG = CHI  
COUNTRY_NAME = China  
SOURCE_FILE = common/history/countries/chi - china.txt  
CURRENT_HIDDEN_GRANTS = international_trade, law_enforcement  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for China, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_legal_codification  
CONFIDENCE = MEDIUM  
RATIONALE = China had a codified or centrally administered legal order before 1776, but not the professional civil-police model represented by the era-6 successor. Preserve legal-administrative capacity while avoiding a Metropolitan-Police-era institution.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### CHL — Chile

COUNTRY_TAG = CHL  
COUNTRY_NAME = Chile  
SOURCE_FILE = common/history/countries/chl - chile.txt  
CURRENT_HIDDEN_GRANTS = empiricism  
OTHER_VISIBLE_STARTING_TECHS = colonization, cotton_gin, distillation, international_relations, medical_degrees, romanticism, shaft_mining

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: the country's tier rationalism row is recommended to supply codified_practical_knowledge  
RECOMMENDATION = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH → codified_practical_knowledge  
CONFIDENCE = MEDIUM  
RATIONALE = Chile's old empiricism role is already covered by the same country's tier-level rationalism reconciliation to codified_practical_knowledge. Implement the visible target once through the tier and delete the redundant direct hidden grant.

COUNTRY_STARTING_TECH_RESULT = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### CLM — Colombia

COUNTRY_TAG = CLM  
COUNTRY_NAME = Colombia  
SOURCE_FILE = common/history/countries/clm - colombia.txt  
CURRENT_HIDDEN_GRANTS = empiricism  
OTHER_VISIBLE_STARTING_TECHS = colonization, cotton_gin, distillation, international_relations, medical_degrees, romanticism, shaft_mining

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: the country's tier rationalism row is recommended to supply codified_practical_knowledge  
RECOMMENDATION = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH → codified_practical_knowledge  
CONFIDENCE = MEDIUM  
RATIONALE = Colombia's old empiricism role is already covered by the same country's tier-level rationalism reconciliation to codified_practical_knowledge. Implement the visible target once through the tier and delete the redundant direct hidden grant.

COUNTRY_STARTING_TECH_RESULT = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### CRI — Crimean Khanate

COUNTRY_TAG = CRI  
COUNTRY_NAME = Crimean Khanate  
SOURCE_FILE = common/history/countries/cri - crimean khanate.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Crimean Khanate, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### CRO — Croatia

COUNTRY_TAG = CRO  
COUNTRY_NAME = Croatia  
SOURCE_FILE = common/history/countries/cro - croatia.txt  
CURRENT_HIDDEN_GRANTS = academia, law_enforcement, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Croatia had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_legal_codification  
CONFIDENCE = MEDIUM  
RATIONALE = Croatia had a codified or centrally administered legal order before 1776, but not the professional civil-police model represented by the era-6 successor. Preserve legal-administrative capacity while avoiding a Metropolitan-Police-era institution.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Croatia grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:2; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### CUB — Cuba

COUNTRY_TAG = CUB  
COUNTRY_NAME = Cuba  
SOURCE_FILE = common/history/countries/cub - cuba.txt  
CURRENT_HIDDEN_GRANTS = line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, romanticism, shaft_mining

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Cuba grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### DAH — Dahomey

COUNTRY_TAG = DAH  
COUNTRY_NAME = Dahomey  
SOURCE_FILE = common/history/countries/dah - dahomey.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Dahomey, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### DAI — Dai Viet

COUNTRY_TAG = DAI  
COUNTRY_NAME = Dai Viet  
SOURCE_FILE = common/history/countries/dai - dai viet.txt  
CURRENT_HIDDEN_GRANTS = sericulture  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = sericulture  
OLD_VANILLA_ROLE = silk cultivation productivity  
TECH6B3E_SUCCESSOR = selective_breeding  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → selective_breeding  
CONFIDENCE = HIGH  
RATIONALE = Sericulture was an established pre-1776 production tradition for Dai Viet; selective breeding is the visible owner of the transferred silk throughput responsibility. Preserve the real productive capability without retaining an inert silk alias.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### DEI — Dutch East Indies Company

COUNTRY_TAG = DEI  
COUNTRY_NAME = Dutch East Indies Company  
SOURCE_FILE = common/history/countries/dei - dutch east indies company.txt  
CURRENT_HIDDEN_GRANTS = corporate_charters  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = corporate_charters  
OLD_VANILLA_ROLE = chartered joint-stock organization  
TECH6B3E_SUCCESSOR = joint_stock_companies  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → joint_stock_companies  
CONFIDENCE = HIGH  
RATIONALE = The Dutch East India Company is direct evidence for chartered joint-stock organization long before 1776, despite the node's era-6 placement. This is the documented pioneer exception that preserves the company's defining institutional capacity.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### DEN — Denmark

COUNTRY_TAG = DEN  
COUNTRY_NAME = Denmark  
SOURCE_FILE = common/history/countries/den - denmark.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Denmark's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Denmark grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### DENNOR — Denmark-Norway

COUNTRY_TAG = DENNOR  
COUNTRY_NAME = Denmark-Norway  
SOURCE_FILE = common/history/countries/dennor - denmark-norway.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Denmark-Norway's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Denmark-Norway grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### DUR — Durrani Empire

COUNTRY_TAG = DUR  
COUNTRY_NAME = Durrani Empire  
SOURCE_FILE = common/history/countries/dur - durrani empire.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Durrani Empire, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### ECU — Ecuador

COUNTRY_TAG = ECU  
COUNTRY_NAME = Ecuador  
SOURCE_FILE = common/history/countries/ecu - ecuador.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Ecuador had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### EGY — Egypt

COUNTRY_TAG = EGY  
COUNTRY_NAME = Egypt  
SOURCE_FILE = common/history/countries/egy - egypt.txt  
CURRENT_HIDDEN_GRANTS = napoleonic_warfare  
OTHER_VISIBLE_STARTING_TECHS = colonization, cotton_gin, distillation, international_relations, medical_degrees, romanticism, shaft_mining

HIDDEN_TECH = napoleonic_warfare  
OLD_VANILLA_ROLE = corps-scale Napoleonic organization  
TECH6B3E_SUCCESSOR = corps_organization  
SUCCESSOR_ERA = era_5  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = Napoleonic corps warfare cannot be a starting capability for Egypt on 1776-01-01. Remove the alias; corps_organization remains an era-5 progression node.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:1
  
HUMAN_REVIEW_REQUIRED = NO

### ETH — Ethopian Empire

COUNTRY_TAG = ETH  
COUNTRY_NAME = Ethopian Empire  
SOURCE_FILE = common/history/countries/eth - ethopian empire.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Ethopian Empire, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### FRA — France

COUNTRY_TAG = FRA  
COUNTRY_NAME = France  
SOURCE_FILE = common/history/countries/fra - france.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, romanticism, shaft_mining, systematic_administrative_statistics, systematic_population_registration, traditional_food_processing

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = France's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit France grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### GAL — Austrian Poland

COUNTRY_TAG = GAL  
COUNTRY_NAME = Austrian Poland  
SOURCE_FILE = common/history/countries/gal - austrian poland.txt  
CURRENT_HIDDEN_GRANTS = academia, law_enforcement, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Austrian Poland had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_legal_codification  
CONFIDENCE = MEDIUM  
RATIONALE = Austrian Poland had a codified or centrally administered legal order before 1776, but not the professional civil-police model represented by the era-6 successor. Preserve legal-administrative capacity while avoiding a Metropolitan-Police-era institution.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Austrian Poland grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:2; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### GBR — Great Britain

COUNTRY_TAG = GBR  
COUNTRY_NAME = Great Britain  
SOURCE_FILE = common/history/countries/gbr - great britain.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry, mandatory_service  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, romanticism, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Great Britain's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Great Britain grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

HIDDEN_TECH = mandatory_service  
OLD_VANILLA_ROLE = conscription and reserve organization  
TECH6B3E_SUCCESSOR = corps_organization  
SUCCESSOR_ERA = era_5  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = The Great Britain grant reflects later reserve/conscription organization rather than a defensible 1776 corps system. Do not replace it with era-5 corps_organization or an unrelated tactical node.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:1; REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### GEN — Genoa

COUNTRY_TAG = GEN  
COUNTRY_NAME = Genoa  
SOURCE_FILE = common/history/countries/gen - genoa.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Genoa's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Genoa grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### GLD — Geledi

COUNTRY_TAG = GLD  
COUNTRY_NAME = Geledi  
SOURCE_FILE = common/history/countries/gld - geledi.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Geledi, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### GR5 — Spanish Haiti

COUNTRY_TAG = GR5  
COUNTRY_NAME = Spanish Haiti  
SOURCE_FILE = common/history/countries/gr5 - spanish haiti.txt  
CURRENT_HIDDEN_GRANTS = line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, romanticism, shaft_mining

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Spanish Haiti grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### GRE — Greece

COUNTRY_TAG = GRE  
COUNTRY_NAME = Greece  
SOURCE_FILE = common/history/countries/gre - greece.txt  
CURRENT_HIDDEN_GRANTS = empiricism, mass_communication  
OTHER_VISIBLE_STARTING_TECHS = colonization, cotton_gin, distillation, international_relations, medical_degrees, romanticism, shaft_mining

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: the country's tier rationalism row is recommended to supply codified_practical_knowledge  
RECOMMENDATION = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH → codified_practical_knowledge  
CONFIDENCE = MEDIUM  
RATIONALE = Greece's old empiricism role is already covered by the same country's tier-level rationalism reconciliation to codified_practical_knowledge. Implement the visible target once through the tier and delete the redundant direct hidden grant.

HIDDEN_TECH = mass_communication  
OLD_VANILLA_ROLE = periodical print circulation  
TECH6B3E_SUCCESSOR = periodical_print_networks  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → periodical_print_networks  
CONFIDENCE = MEDIUM  
RATIONALE = Print and periodical circulation is the period-compatible communication capacity for Greece; mass mechanized circulation is later. Use the visible era-1 media owner and preserve later mechanized printing progression.

COUNTRY_STARTING_TECH_RESULT = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### GZA — Gaza

COUNTRY_TAG = GZA  
COUNTRY_NAME = Gaza  
SOURCE_FILE = common/history/countries/gza - gaza.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Gaza, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### HAI — Haiti

COUNTRY_TAG = HAI  
COUNTRY_NAME = Haiti  
SOURCE_FILE = common/history/countries/hai - haiti.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Haiti had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### HBC — Hudson Bay Company

COUNTRY_TAG = HBC  
COUNTRY_NAME = Hudson Bay Company  
SOURCE_FILE = common/history/countries/hbc - hubson bay company.txt ; common/history/countries/hbc - hudson bay company.txt  
CURRENT_HIDDEN_GRANTS = academia, academia, line_infantry, line_infantry, mandatory_service  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = UNCERTAIN  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: multiple effective country files initialize the same tag  
RECOMMENDATION = HUMAN_REVIEW_REQUIRED → institutionalized_scientific_exchange  
CONFIDENCE = LOW  
RATIONALE = Two distinct mod files ('hubson' and 'hudson') both initialize HBC, so historical intent cannot be separated safely from the duplicate setup. Choose the authoritative country file first; then keep one education/arms grant and remove duplicate or anachronistic service grants.

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = UNCERTAIN  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: multiple effective country files initialize the same tag  
RECOMMENDATION = HUMAN_REVIEW_REQUIRED → institutionalized_scientific_exchange  
CONFIDENCE = LOW  
RATIONALE = Two distinct mod files ('hubson' and 'hudson') both initialize HBC, so historical intent cannot be separated safely from the duplicate setup. Choose the authoritative country file first; then keep one education/arms grant and remove duplicate or anachronistic service grants.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = UNCERTAIN  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: multiple effective country files initialize the same tag  
RECOMMENDATION = HUMAN_REVIEW_REQUIRED → regulated_small_arms  
CONFIDENCE = LOW  
RATIONALE = Two distinct mod files ('hubson' and 'hudson') both initialize HBC, so historical intent cannot be separated safely from the duplicate setup. Choose the authoritative country file first; then keep one education/arms grant and remove duplicate or anachronistic service grants.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = UNCERTAIN  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: multiple effective country files initialize the same tag  
RECOMMENDATION = HUMAN_REVIEW_REQUIRED → regulated_small_arms  
CONFIDENCE = LOW  
RATIONALE = Two distinct mod files ('hubson' and 'hudson') both initialize HBC, so historical intent cannot be separated safely from the duplicate setup. Choose the authoritative country file first; then keep one education/arms grant and remove duplicate or anachronistic service grants.

HIDDEN_TECH = mandatory_service  
OLD_VANILLA_ROLE = conscription and reserve organization  
TECH6B3E_SUCCESSOR = corps_organization  
SUCCESSOR_ERA = era_5  
HISTORICAL_FIT_1776 = UNCERTAIN  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: multiple effective country files initialize the same tag  
RECOMMENDATION = HUMAN_REVIEW_REQUIRED  
CONFIDENCE = LOW  
RATIONALE = Two distinct mod files ('hubson' and 'hudson') both initialize HBC, so historical intent cannot be separated safely from the duplicate setup. Choose the authoritative country file first; then keep one education/arms grant and remove duplicate or anachronistic service grants.

COUNTRY_STARTING_TECH_RESULT = HUMAN_REVIEW_REQUIRED:5
  
HUMAN_REVIEW_REQUIRED = YES

### HDY — Hadiya

COUNTRY_TAG = HDY  
COUNTRY_NAME = Hadiya  
SOURCE_FILE = common/history/countries/hdy - hadiya.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Hadiya, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### HUN — Hungary

COUNTRY_TAG = HUN  
COUNTRY_NAME = Hungary  
SOURCE_FILE = common/history/countries/hun - hungary.txt  
CURRENT_HIDDEN_GRANTS = academia, law_enforcement, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Hungary had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_legal_codification  
CONFIDENCE = MEDIUM  
RATIONALE = Hungary had a codified or centrally administered legal order before 1776, but not the professional civil-police model represented by the era-6 successor. Preserve legal-administrative capacity while avoiding a Metropolitan-Police-era institution.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Hungary grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:2; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### IQU — Iquichia

COUNTRY_TAG = IQU  
COUNTRY_NAME = Iquichia  
SOURCE_FILE = common/history/countries/iqu - iquichia.txt  
CURRENT_HIDDEN_GRANTS = empiricism  
OTHER_VISIBLE_STARTING_TECHS = colonization, cotton_gin, distillation, international_relations, medical_degrees, romanticism, shaft_mining

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: the country's tier rationalism row is recommended to supply codified_practical_knowledge  
RECOMMENDATION = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH → codified_practical_knowledge  
CONFIDENCE = MEDIUM  
RATIONALE = Iquichia's old empiricism role is already covered by the same country's tier-level rationalism reconciliation to codified_practical_knowledge. Implement the visible target once through the tier and delete the redundant direct hidden grant.

COUNTRY_STARTING_TECH_RESULT = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### IR1 — Mamluk Iraq

COUNTRY_TAG = IR1  
COUNTRY_NAME = Mamluk Iraq  
SOURCE_FILE = common/history/countries/ir1 - mamluk iraq.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Mamluk Iraq had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### IREK — Ireland

COUNTRY_TAG = IREK  
COUNTRY_NAME = Ireland  
SOURCE_FILE = common/history/countries/irek - ireland.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Ireland had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### ISQ — Isaaq

COUNTRY_TAG = ISQ  
COUNTRY_NAME = Isaaq  
SOURCE_FILE = common/history/countries/isq - isaaq.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Isaaq, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### JAP — Japan

COUNTRY_TAG = JAP  
COUNTRY_NAME = Japan  
SOURCE_FILE = common/history/countries/jap - japan.txt  
CURRENT_HIDDEN_GRANTS = academia, centralization, urban_planning  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Japan had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = centralization  
OLD_VANILLA_ROLE = central state information and administration  
TECH6B3E_SUCCESSOR = systematic_administrative_statistics  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → systematic_administrative_statistics  
CONFIDENCE = MEDIUM  
RATIONALE = Tokugawa government combined domain administration, registers, surveys, and recurring provincial map submissions without being a unitary centralized state. Use the visible administrative-information owner; do not encode political centralization literally.

HIDDEN_TECH = urban_planning  
OLD_VANILLA_ROLE = urban administration and sanitation  
TECH6B3E_SUCCESSOR = modern_sewerage  
SUCCESSOR_ERA = era_8  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_cadastral_surveying  
CONFIDENCE = MEDIUM  
RATIONALE = Tokugawa cadastral surveys and ordered provincial mapping support a land-information capacity, not modern sewerage. Model the historical administrative substrate while the tier's urbanization alias separately preserves the building gate.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:2; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### KAU — Kaurna

COUNTRY_TAG = KAU  
COUNTRY_NAME = Kaurna  
SOURCE_FILE = common/history/countries/kau - kaurna.txt  
CURRENT_HIDDEN_GRANTS = democracy, rationalism  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = democracy  
OLD_VANILLA_ROLE = representative or constitutional politics  
TECH6B3E_SUCCESSOR = constitutional_government  
SUCCESSOR_ERA = era_4  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = Applying a democracy-derived capacity to Kaurna on 1776-01-01 would import a vanilla tier abstraction rather than a documented polity institution. Remove the inert alias without substituting constitutional government.

HIDDEN_TECH = rationalism  
OLD_VANILLA_ROLE = codified practical knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = MEDIUM  
RATIONALE = The direct rationalism grant for Kaurna is a coarse vanilla tier correction and lacks sufficient evidence for codified_practical_knowledge at the reference date. Avoid duplicating or inflating the broad tier-level knowledge architecture.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:2
  
HUMAN_REVIEW_REQUIRED = NO

### KRA — Krakow

COUNTRY_TAG = KRA  
COUNTRY_NAME = Krakow  
SOURCE_FILE = common/history/countries/kra - krakow.txt  
CURRENT_HIDDEN_GRANTS = dialectics  
OTHER_VISIBLE_STARTING_TECHS = atmospheric_engine, coke_smelting, commercial_insurance_markets, distillation, enclosed_dock_systems, improved_husbandry, institutionalized_public_credit, institutionalized_scientific_exchange, international_relations, mechanical_tools, organized_forestry, organized_textile_production, periodical_print_networks, scientific_fortification_siegecraft, shaft_mining, state_dockyard_systems, stock_exchange, traditional_food_processing, traditional_papermaking

HIDDEN_TECH = dialectics  
OLD_VANILLA_ROLE = later philosophical/socialist event gating  
TECH6B3E_SUCCESSOR = socialism  
SUCCESSOR_ERA = era_7  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = Krakow's vanilla dialectics grant is a 1836 setup inheritance; mature socialism and the term itself belong to the 19th century. Do not convert the starting grant to socialism or early_socialism_cooperativism.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:1
  
HUMAN_REVIEW_REQUIRED = NO

### LAN — Lanfang

COUNTRY_TAG = LAN  
COUNTRY_NAME = Lanfang  
SOURCE_FILE = common/history/countries/lan - lanfang.txt  
CURRENT_HIDDEN_GRANTS = academia, empiricism  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Lanfang had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: the country's tier rationalism row is recommended to supply codified_practical_knowledge  
RECOMMENDATION = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH → codified_practical_knowledge  
CONFIDENCE = MEDIUM  
RATIONALE = Lanfang's old empiricism role is already covered by the same country's tier-level rationalism reconciliation to codified_practical_knowledge. Implement the visible target once through the tier and delete the redundant direct hidden grant.

COUNTRY_STARTING_TECH_RESULT = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH:1; REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### LOU — Louisiana

COUNTRY_TAG = LOU  
COUNTRY_NAME = Louisiana  
SOURCE_FILE = common/history/countries/lou - louisiana.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Louisiana had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### MAD — Madagascar

COUNTRY_TAG = MAD  
COUNTRY_NAME = Madagascar  
SOURCE_FILE = common/history/countries/mad - madagascar.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Madagascar, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### MARATH — Maratha Empire

COUNTRY_TAG = MARATH  
COUNTRY_NAME = Maratha Empire  
SOURCE_FILE = common/history/countries/marath - maratha empire.txt  
CURRENT_HIDDEN_GRANTS = admiralty, international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = admiralty  
OLD_VANILLA_ROLE = naval administration and dockyard capacity  
TECH6B3E_SUCCESSOR = state_dockyard_systems  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → state_dockyard_systems  
CONFIDENCE = MEDIUM  
RATIONALE = The Maratha navy was damaged in 1756 but maritime forces remained relevant in the 1770s, supporting a limited state-dockyard abstraction. Give the early naval owner, not a later mechanized dockyard or generic admiralty alias.

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Maratha Empire, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### MBS — Mombasa

COUNTRY_TAG = MBS  
COUNTRY_NAME = Mombasa  
SOURCE_FILE = common/history/countries/mbs - mombasa.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Mombasa, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### MEX — Mexico

COUNTRY_TAG = MEX  
COUNTRY_NAME = Mexico  
SOURCE_FILE = common/history/countries/mex - mexico.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Mexico had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### MJT — Majerteen

COUNTRY_TAG = MJT  
COUNTRY_NAME = Majerteen  
SOURCE_FILE = common/history/countries/mjt - majerteen.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Majerteen, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### NBS — New Brunswick

COUNTRY_TAG = NBS  
COUNTRY_NAME = New Brunswick  
SOURCE_FILE = common/history/countries/nbs - new brunswick.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that New Brunswick had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit New Brunswick grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### NET — Netherlands

COUNTRY_TAG = NET  
COUNTRY_NAME = Netherlands  
SOURCE_FILE = common/history/countries/net - netherlands.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Netherlands's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Netherlands grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### NOR — Norway

COUNTRY_TAG = NOR  
COUNTRY_NAME = Norway  
SOURCE_FILE = common/history/countries/nor - norway.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Norway's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Norway grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### NPU — North Peru

COUNTRY_TAG = NPU  
COUNTRY_NAME = North Peru  
SOURCE_FILE = common/history/countries/npu - north peru.txt  
CURRENT_HIDDEN_GRANTS = empiricism  
OTHER_VISIBLE_STARTING_TECHS = colonization, cotton_gin, distillation, international_relations, medical_degrees, romanticism, shaft_mining

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: the country's tier rationalism row is recommended to supply codified_practical_knowledge  
RECOMMENDATION = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH → codified_practical_knowledge  
CONFIDENCE = MEDIUM  
RATIONALE = North Peru's old empiricism role is already covered by the same country's tier-level rationalism reconciliation to codified_practical_knowledge. Implement the visible target once through the tier and delete the redundant direct hidden grant.

COUNTRY_STARTING_TECH_RESULT = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### NVS — Nova Scotia

COUNTRY_TAG = NVS  
COUNTRY_NAME = Nova Scotia  
SOURCE_FILE = common/history/countries/nvs - nova scotia.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Nova Scotia had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Nova Scotia grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### ONT — Ontario

COUNTRY_TAG = ONT  
COUNTRY_NAME = Ontario  
SOURCE_FILE = common/history/countries/ont - ontario.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Ontario had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Ontario grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### ORG — Oregon

COUNTRY_TAG = ORG  
COUNTRY_NAME = Oregon  
SOURCE_FILE = common/history/countries/org -oregan.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = atmospheric_engine, coke_smelting, colonization, commercial_insurance_markets, distillation, enclosed_dock_systems, improved_husbandry, institutionalized_public_credit, institutionalized_scientific_exchange, international_relations, mechanical_tools, organized_forestry, organized_textile_production, periodical_print_networks, scientific_fortification_siegecraft, shaft_mining, state_dockyard_systems, stock_exchange, traditional_food_processing, traditional_papermaking

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Oregon had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Oregon grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### OYO — Oyo

COUNTRY_TAG = OYO  
COUNTRY_NAME = Oyo  
SOURCE_FILE = common/history/countries/oyo - oyo.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Oyo, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### PAN — Panjab

COUNTRY_TAG = PAN  
COUNTRY_NAME = Panjab  
SOURCE_FILE = common/history/countries/pan - panjab.txt  
CURRENT_HIDDEN_GRANTS = line_infantry, mandatory_service  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Panjab grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

HIDDEN_TECH = mandatory_service  
OLD_VANILLA_ROLE = conscription and reserve organization  
TECH6B3E_SUCCESSOR = corps_organization  
SUCCESSOR_ERA = era_5  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = The Panjab grant reflects later reserve/conscription organization rather than a defensible 1776 corps system. Do not replace it with era-5 corps_organization or an unrelated tactical node.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### PAP — Papal States

COUNTRY_TAG = PAP  
COUNTRY_NAME = Papal States  
SOURCE_FILE = common/history/countries/pap - papal states.txt  
CURRENT_HIDDEN_GRANTS = line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Papal States grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### PCO — Puerto Rico

COUNTRY_TAG = PCO  
COUNTRY_NAME = Puerto Rico  
SOURCE_FILE = common/history/countries/pco - puerto rico.txt  
CURRENT_HIDDEN_GRANTS = line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Puerto Rico grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### PER — Persia

COUNTRY_TAG = PER  
COUNTRY_NAME = Persia  
SOURCE_FILE = common/history/countries/per - persia.txt  
CURRENT_HIDDEN_GRANTS = admiralty, law_enforcement, urban_planning  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = admiralty  
OLD_VANILLA_ROLE = naval administration and dockyard capacity  
TECH6B3E_SUCCESSOR = state_dockyard_systems  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = UNCERTAIN  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = HUMAN_REVIEW_REQUIRED → state_dockyard_systems  
CONFIDENCE = LOW  
RATIONALE = Zand Persia pursued Gulf operations and sought Company naval support, but the evidence is ambiguous between indigenous state capacity and reliance on foreign shipping. A state_dockyard_systems grant preserves naval agency; removal avoids overstating institutional capacity.

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = No sufficient 1776 evidence supports professional civil policing for Persia; the closest TECH6B3E owner reflects the 1829-era institution. Remove rather than invent a weak semantic substitute.

HIDDEN_TECH = urban_planning  
OLD_VANILLA_ROLE = urban administration and sanitation  
TECH6B3E_SUCCESSOR = modern_sewerage  
SUCCESSOR_ERA = era_8  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: tier-4 urbanization remains for the only live urban-building gate  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = Persian urban traditions do not justify assigning the era-8 modern_sewerage node or a national cadastral substitute on 1776-01-01. The tier's urbanization alias already preserves the temporary building gate; this direct grant is inert and redundant.

COUNTRY_STARTING_TECH_RESULT = HUMAN_REVIEW_REQUIRED:1; REMOVE_STARTING_GRANT:2
  
HUMAN_REVIEW_REQUIRED = YES

### PEU — Peru

COUNTRY_TAG = PEU  
COUNTRY_NAME = Peru  
SOURCE_FILE = common/history/countries/peu - Peru.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Peru had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### PHI — Philippines

COUNTRY_TAG = PHI  
COUNTRY_NAME = Philippines  
SOURCE_FILE = common/history/countries/phi - philippines.txt  
CURRENT_HIDDEN_GRANTS = law_enforcement  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_administrative_statistics  
CONFIDENCE = MEDIUM  
RATIONALE = For Philippines, the grant is better read as colonial administrative reach than as professional civil policing. Move to the earlier state-information capacity and avoid an era-6 police unlock.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### PHL — Philippolis

COUNTRY_TAG = PHL  
COUNTRY_NAME = Philippolis  
SOURCE_FILE = common/history/countries/phl - philippolis.txt  
CURRENT_HIDDEN_GRANTS = international_trade, rationalism, tech_bureaucracy  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Philippolis, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

HIDDEN_TECH = rationalism  
OLD_VANILLA_ROLE = codified practical knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = MEDIUM  
RATIONALE = The direct rationalism grant for Philippolis is a coarse vanilla tier correction and lacks sufficient evidence for codified_practical_knowledge at the reference date. Avoid duplicating or inflating the broad tier-level knowledge architecture.

HIDDEN_TECH = tech_bureaucracy  
OLD_VANILLA_ROLE = state statistics and bureaucracy  
TECH6B3E_SUCCESSOR = central_statistical_offices  
SUCCESSOR_ERA = era_5  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = Central statistical offices or systematic state statistics are not justified for Philippolis on 1776-01-01. Remove the inert alias rather than promote a decentralized setup to an era-2 or era-5 bureaucracy node.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:2; REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### PLY — Tahiti

COUNTRY_TAG = PLY  
COUNTRY_NAME = Tahiti  
SOURCE_FILE = common/history/countries/ply - tahiti.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Tahiti, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### POR — Portugal

COUNTRY_TAG = POR  
COUNTRY_NAME = Portugal  
SOURCE_FILE = common/history/countries/por - portugal.txt  
CURRENT_HIDDEN_GRANTS = academia, law_enforcement, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Portugal's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_legal_codification  
CONFIDENCE = MEDIUM  
RATIONALE = Portugal had a codified or centrally administered legal order before 1776, but not the professional civil-police model represented by the era-6 successor. Preserve legal-administrative capacity while avoiding a Metropolitan-Police-era institution.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Portugal grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### PRG — Paraguay

COUNTRY_TAG = PRG  
COUNTRY_NAME = Paraguay  
SOURCE_FILE = common/history/countries/prg - Paraguay.txt ; common/history/countries/prg - paraguay.txt  
CURRENT_HIDDEN_GRANTS = academia, central_archives, egalitarianism, empiricism, mass_communication  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Paraguay had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = central_archives  
OLD_VANILLA_ROLE = central administrative records  
TECH6B3E_SUCCESSOR = central_statistical_offices  
SUCCESSOR_ERA = era_5  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: case-insensitive mod shadow makes this vanilla occurrence inactive  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = The vanilla Paraguay row is shadowed by the mod file whose name differs only by case; it is not an effective 1776 grant on the target Windows installation. Record the stale provenance but do not implement a change against the inactive vanilla file.

HIDDEN_TECH = egalitarianism  
OLD_VANILLA_ROLE = rights and liberal-reform gating  
TECH6B3E_SUCCESSOR = liberal_constitutionalism  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: case-insensitive mod shadow makes this vanilla occurrence inactive  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = The vanilla Paraguay row is shadowed by the mod file whose name differs only by case; it is not an effective 1776 grant on the target Windows installation. Record the stale provenance but do not implement a change against the inactive vanilla file.

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: case-insensitive mod shadow makes this vanilla occurrence inactive  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = The vanilla Paraguay row is shadowed by the mod file whose name differs only by case; it is not an effective 1776 grant on the target Windows installation. Record the stale provenance but do not implement a change against the inactive vanilla file.

HIDDEN_TECH = mass_communication  
OLD_VANILLA_ROLE = periodical print circulation  
TECH6B3E_SUCCESSOR = periodical_print_networks  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: case-insensitive mod shadow makes this vanilla occurrence inactive  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = The vanilla Paraguay row is shadowed by the mod file whose name differs only by case; it is not an effective 1776 grant on the target Windows installation. Record the stale provenance but do not implement a change against the inactive vanilla file.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:4; REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### PRU — Prussia

COUNTRY_TAG = PRU  
COUNTRY_NAME = Prussia  
SOURCE_FILE = common/history/countries/pru - prussia.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, romanticism, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Prussia's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Prussia grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### QUE — Quebec

COUNTRY_TAG = QUE  
COUNTRY_NAME = Quebec  
SOURCE_FILE = common/history/countries/que - quebec.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Quebec had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Quebec grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### RUS — Russia

COUNTRY_TAG = RUS  
COUNTRY_NAME = Russia  
SOURCE_FILE = common/history/countries/rus - russia.txt  
CURRENT_HIDDEN_GRANTS = law_enforcement, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_legal_codification  
CONFIDENCE = MEDIUM  
RATIONALE = Russia had a codified or centrally administered legal order before 1776, but not the professional civil-police model represented by the era-6 successor. Preserve legal-administrative capacity while avoiding a Metropolitan-Police-era institution.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Russia grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### SC1 — Colonial Mexico

COUNTRY_TAG = SC1  
COUNTRY_NAME = Colonial Mexico  
SOURCE_FILE = common/history/countries/sc1 - colonial mexico.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Colonial Mexico had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### SC2 — Colonial Colombia

COUNTRY_TAG = SC2  
COUNTRY_NAME = Colonial Colombia  
SOURCE_FILE = common/history/countries/sc2 - colonial colombia.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Colonial Colombia had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### SC3 — Colonial Peru

COUNTRY_TAG = SC3  
COUNTRY_NAME = Colonial Peru  
SOURCE_FILE = common/history/countries/sc3 - colonial peru.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Colonial Peru had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### SC4 — Colonial Argentina

COUNTRY_TAG = SC4  
COUNTRY_NAME = Colonial Argentina  
SOURCE_FILE = common/history/countries/sc4 - colonial argentina.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Colonial Argentina had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### SIA — Siam

COUNTRY_TAG = SIA  
COUNTRY_NAME = Siam  
SOURCE_FILE = common/history/countries/sia - siam.txt  
CURRENT_HIDDEN_GRANTS = sericulture  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = sericulture  
OLD_VANILLA_ROLE = silk cultivation productivity  
TECH6B3E_SUCCESSOR = selective_breeding  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → selective_breeding  
CONFIDENCE = HIGH  
RATIONALE = Sericulture was an established pre-1776 production tradition for Siam; selective breeding is the visible owner of the transferred silk throughput responsibility. Preserve the real productive capability without retaining an inert silk alias.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### SIL — Sierra Leone

COUNTRY_TAG = SIL  
COUNTRY_NAME = Sierra Leone  
SOURCE_FILE = common/history/countries/sil - sierra leone.txt  
CURRENT_HIDDEN_GRANTS = law_enforcement  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = No sufficient 1776 evidence supports professional civil policing for Sierra Leone; the closest TECH6B3E owner reflects the 1829-era institution. Remove rather than invent a weak semantic substitute.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:1
  
HUMAN_REVIEW_REQUIRED = NO

### SPA — Spain

COUNTRY_TAG = SPA  
COUNTRY_NAME = Spain  
SOURCE_FILE = common/history/countries/spa - spain.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Spain's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Spain grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### SPC — Carlist Spain

COUNTRY_TAG = SPC  
COUNTRY_NAME = Carlist Spain  
SOURCE_FILE = common/history/countries/spc - carlist spain.txt  
CURRENT_HIDDEN_GRANTS = empiricism, mass_communication, napoleonic_warfare  
OTHER_VISIBLE_STARTING_TECHS = atmospheric_engine, colonization, cotton_gin, distillation, international_relations, medical_degrees, romanticism, shaft_mining, stock_exchange

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: the country's tier rationalism row is recommended to supply codified_practical_knowledge  
RECOMMENDATION = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH → codified_practical_knowledge  
CONFIDENCE = MEDIUM  
RATIONALE = Carlist Spain's old empiricism role is already covered by the same country's tier-level rationalism reconciliation to codified_practical_knowledge. Implement the visible target once through the tier and delete the redundant direct hidden grant.

HIDDEN_TECH = mass_communication  
OLD_VANILLA_ROLE = periodical print circulation  
TECH6B3E_SUCCESSOR = periodical_print_networks  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → periodical_print_networks  
CONFIDENCE = MEDIUM  
RATIONALE = Print and periodical circulation is the period-compatible communication capacity for Carlist Spain; mass mechanized circulation is later. Use the visible era-1 media owner and preserve later mechanized printing progression.

HIDDEN_TECH = napoleonic_warfare  
OLD_VANILLA_ROLE = corps-scale Napoleonic organization  
TECH6B3E_SUCCESSOR = corps_organization  
SUCCESSOR_ERA = era_5  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = Napoleonic corps warfare cannot be a starting capability for Carlist Spain on 1776-01-01. Remove the alias; corps_organization remains an era-5 progression node.

COUNTRY_STARTING_TECH_RESULT = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH:1; REMOVE_STARTING_GRANT:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### SPU — South Peru

COUNTRY_TAG = SPU  
COUNTRY_NAME = South Peru  
SOURCE_FILE = common/history/countries/spu - south peru.txt  
CURRENT_HIDDEN_GRANTS = empiricism  
OTHER_VISIBLE_STARTING_TECHS = colonization, cotton_gin, distillation, international_relations, medical_degrees, romanticism, shaft_mining

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: the country's tier rationalism row is recommended to supply codified_practical_knowledge  
RECOMMENDATION = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH → codified_practical_knowledge  
CONFIDENCE = MEDIUM  
RATIONALE = South Peru's old empiricism role is already covered by the same country's tier-level rationalism reconciliation to codified_practical_knowledge. Implement the visible target once through the tier and delete the redundant direct hidden grant.

COUNTRY_STARTING_TECH_RESULT = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### SWE — Sweden

COUNTRY_TAG = SWE  
COUNTRY_NAME = Sweden  
SOURCE_FILE = common/history/countries/swe - sweden.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Sweden's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Sweden grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### SWZ — Swaziland

COUNTRY_TAG = SWZ  
COUNTRY_NAME = Swaziland  
SOURCE_FILE = common/history/countries/swz - swaziland.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Swaziland, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### TEX — Texas

COUNTRY_TAG = TEX  
COUNTRY_NAME = Texas  
SOURCE_FILE = common/history/countries/tex - texas.txt  
CURRENT_HIDDEN_GRANTS = empiricism  
OTHER_VISIBLE_STARTING_TECHS = colonization, cotton_gin, distillation, international_relations, medical_degrees, romanticism, shaft_mining

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: the country's tier rationalism row is recommended to supply codified_practical_knowledge  
RECOMMENDATION = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH → codified_practical_knowledge  
CONFIDENCE = MEDIUM  
RATIONALE = Texas's old empiricism role is already covered by the same country's tier-level rationalism reconciliation to codified_practical_knowledge. Implement the visible target once through the tier and delete the redundant direct hidden grant.

COUNTRY_STARTING_TECH_RESULT = ALREADY_REPRESENTED_BY_OTHER_STARTING_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### TGI — Tungi

COUNTRY_TAG = TGI  
COUNTRY_NAME = Tungi  
SOURCE_FILE = common/history/countries/tgi - tungi.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Tungi, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### TRS — Transylvania

COUNTRY_TAG = TRS  
COUNTRY_NAME = Transylvania  
SOURCE_FILE = common/history/countries/trs - transylvania.txt  
CURRENT_HIDDEN_GRANTS = academia, law_enforcement, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Transylvania had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = law_enforcement  
OLD_VANILLA_ROLE = civil policing and legal administration  
TECH6B3E_SUCCESSOR = professional_civil_policing  
SUCCESSOR_ERA = era_6  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → systematic_legal_codification  
CONFIDENCE = MEDIUM  
RATIONALE = Transylvania had a codified or centrally administered legal order before 1776, but not the professional civil-police model represented by the era-6 successor. Preserve legal-administrative capacity while avoiding a Metropolitan-Police-era institution.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Transylvania grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:2; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### TUR — Ottoman Empire

COUNTRY_TAG = TUR  
COUNTRY_NAME = Ottoman Empire  
SOURCE_FILE = common/history/countries/tur - ottoman empire.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Ottoman Empire's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### UCA — Central America

COUNTRY_TAG = UCA  
COUNTRY_NAME = Central America  
SOURCE_FILE = common/history/countries/uca - central america.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Central America had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### URU — Uruguay

COUNTRY_TAG = URU  
COUNTRY_NAME = Uruguay  
SOURCE_FILE = common/history/countries/uru - uruguay.txt  
CURRENT_HIDDEN_GRANTS = academia  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Uruguay had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### USA — Usa

COUNTRY_TAG = USA  
COUNTRY_NAME = Usa  
SOURCE_FILE = common/history/countries/usa - usa.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = colonization, distillation, international_relations, romanticism, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → institutionalized_scientific_exchange  
CONFIDENCE = MEDIUM  
RATIONALE = An explicit 1836 academia grant does not prove that Usa had specialized technical academies on 1776-01-01; learned exchange is the safer early abstraction. Retain a modest education/knowledge distinction without over-granting the era-3 specialized academy node.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Usa grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1; REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### VEN — Venetia

COUNTRY_TAG = VEN  
COUNTRY_NAME = Venetia  
SOURCE_FILE = common/history/countries/ven - venetia.txt  
CURRENT_HIDDEN_GRANTS = academia, line_infantry  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → specialized_technical_academies  
CONFIDENCE = MEDIUM  
RATIONALE = Venetia's explicit education grant can reasonably represent established technical, military, naval, or learned academies by 1776. Preserve the explicit country differentiation with the visible era-3 owner rather than leaving an inert alias.

HIDDEN_TECH = line_infantry  
OLD_VANILLA_ROLE = regular musket infantry unlock  
TECH6B3E_SUCCESSOR = regulated_small_arms  
SUCCESSOR_ERA = era_2  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → regulated_small_arms  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit Venetia grant represents regular musket infantry and standardized flintlock supply, a valid 18th-century capability. The old unit responsibility now belongs to regulated_small_arms; this is a mechanical and historical match.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:2
  
HUMAN_REVIEW_REQUIRED = NO

### VNZ — Venezuela

COUNTRY_TAG = VNZ  
COUNTRY_NAME = Venezuela  
SOURCE_FILE = common/history/countries/vnz - venezuela.txt ; common/history/countries/vnz - venezula.txt  
CURRENT_HIDDEN_GRANTS = academia, empiricism  
OTHER_VISIBLE_STARTING_TECHS = colonization, cotton_gin, distillation, international_relations, medical_degrees, romanticism, shaft_mining

HIDDEN_TECH = academia  
OLD_VANILLA_ROLE = higher education and qualification capacity  
TECH6B3E_SUCCESSOR = specialized_technical_academies  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = UNCERTAIN  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: multiple effective country files initialize the same tag  
RECOMMENDATION = HUMAN_REVIEW_REQUIRED → institutionalized_scientific_exchange  
CONFIDENCE = LOW  
RATIONALE = Vanilla 'venezuela' and mod 'venezula' are separate effective files and assign conflicting tier-3/tier-4 starts to the same tag. Consolidate the country setup before deciding which one of the overlapping knowledge grants survives.

HIDDEN_TECH = empiricism  
OLD_VANILLA_ROLE = codified practical and learned knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = UNCERTAIN  
DUPLICATED_BY_OTHER_STARTING_TECH = YES: multiple effective country files initialize the same tag  
RECOMMENDATION = HUMAN_REVIEW_REQUIRED → codified_practical_knowledge  
CONFIDENCE = LOW  
RATIONALE = Vanilla 'venezuela' and mod 'venezula' are separate effective files and assign conflicting tier-3/tier-4 starts to the same tag. Consolidate the country setup before deciding which one of the overlapping knowledge grants survives.

COUNTRY_STARTING_TECH_RESULT = HUMAN_REVIEW_REQUIRED:2
  
HUMAN_REVIEW_REQUIRED = YES

### WAL — Wallachia

COUNTRY_TAG = WAL  
COUNTRY_NAME = Wallachia  
SOURCE_FILE = common/history/countries/wal - wallachia.txt  
CURRENT_HIDDEN_GRANTS = sericulture  
OTHER_VISIBLE_STARTING_TECHS = distillation, international_relations, shaft_mining

HIDDEN_TECH = sericulture  
OLD_VANILLA_ROLE = silk cultivation productivity  
TECH6B3E_SUCCESSOR = selective_breeding  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = YES  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_VISIBLE_TECH → selective_breeding  
CONFIDENCE = MEDIUM  
RATIONALE = Sericulture was an established pre-1776 production tradition for Wallachia; selective breeding is the visible owner of the transferred silk throughput responsibility. Preserve the real productive capability without retaining an inert silk alias.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### WBL — Waterboersland

COUNTRY_TAG = WBL  
COUNTRY_NAME = Waterboersland  
SOURCE_FILE = common/history/countries/wbl - waterboersland.txt  
CURRENT_HIDDEN_GRANTS = international_trade, rationalism, tech_bureaucracy  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Waterboersland, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

HIDDEN_TECH = rationalism  
OLD_VANILLA_ROLE = codified practical knowledge  
TECH6B3E_SUCCESSOR = codified_practical_knowledge  
SUCCESSOR_ERA = era_3  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = MEDIUM  
RATIONALE = The direct rationalism grant for Waterboersland is a coarse vanilla tier correction and lacks sufficient evidence for codified_practical_knowledge at the reference date. Avoid duplicating or inflating the broad tier-level knowledge architecture.

HIDDEN_TECH = tech_bureaucracy  
OLD_VANILLA_ROLE = state statistics and bureaucracy  
TECH6B3E_SUCCESSOR = central_statistical_offices  
SUCCESSOR_ERA = era_5  
HISTORICAL_FIT_1776 = NO  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REMOVE_STARTING_GRANT  
CONFIDENCE = HIGH  
RATIONALE = Central statistical offices or systematic state statistics are not justified for Waterboersland on 1776-01-01. Remove the inert alias rather than promote a decentralized setup to an era-2 or era-5 bureaucracy node.

COUNTRY_STARTING_TECH_RESULT = REMOVE_STARTING_GRANT:2; REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### WSG — Warsangali

COUNTRY_TAG = WSG  
COUNTRY_NAME = Warsangali  
SOURCE_FILE = common/history/countries/wsg - warsangali.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Warsangali, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### WTU — Witu

COUNTRY_TAG = WTU  
COUNTRY_NAME = Witu  
SOURCE_FILE = common/history/countries/wtu - witu.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = shaft_mining

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Witu, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO

### ZUL — Zulu

COUNTRY_TAG = ZUL  
COUNTRY_NAME = Zulu  
SOURCE_FILE = common/history/countries/zul - zulu.txt  
CURRENT_HIDDEN_GRANTS = international_trade  
OTHER_VISIBLE_STARTING_TECHS = NONE

HIDDEN_TECH = international_trade  
OLD_VANILLA_ROLE = external commerce  
TECH6B3E_SUCCESSOR = commercial_insurance_markets  
SUCCESSOR_ERA = era_1  
HISTORICAL_FIT_1776 = PARTIAL  
DUPLICATED_BY_OTHER_STARTING_TECH = NO  
RECOMMENDATION = REPLACE_WITH_EARLIER_VISIBLE_TECH → international_relations  
CONFIDENCE = MEDIUM  
RATIONALE = The explicit grant supports external commercial contact for Zulu, but commercial insurance markets would over-specify a European financial institution. Use the broad era-1 international capacity and preserve commercial insurance for countries with direct financial evidence.

COUNTRY_STARTING_TECH_RESULT = REPLACE_WITH_EARLIER_VISIBLE_TECH:1
  
HUMAN_REVIEW_REQUIRED = NO


## H. Grants à remplacer directement

Nombre = 73  
Indices matrice = 002, 003, 008, 009, 011, 013, 014, 026, 027, 032, 034, 040, 041, 043, 047, 049, 050, 055, 056, 058, 060, 063, 089, 090, 091, 092, 094, 095, 127, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 158, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 186, 188, 189, 190, 198, 204, 205, 206, 208, 209, 210, 211

Les remplacements directs sont limités aux concepts dont le propriétaire visible correspond au rôle initial et dont la capacité est défendable au 1776-01-01: armes réglementées, artillerie standardisée, connaissances codifiées, sériciculture, académies documentées et quelques capacités navales précises.

## I. Grants à remplacer par un nœud plus ancien

Nombre = 81  
Indices matrice = 001, 004, 005, 006, 007, 010, 012, 015, 018, 019, 020, 021, 022, 023, 024, 025, 028, 029, 030, 031, 033, 035, 036, 037, 038, 039, 042, 044, 045, 046, 096, 097, 098, 099, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 130, 131, 132, 133, 134, 135, 136, 138, 139, 140, 142, 183, 184, 185, 207, 216, 220, 221, 222, 223

Cette catégorie évite notamment `professional_civil_policing`, `corps_organization`, `iron_hull_construction`, `interchangeable_manufacture` et `modern_sewerage`. Les cibles sont des abstractions visibles plus anciennes et de même catégorie.

## J. Grants à supprimer

Nombre = 46  
Indices matrice = 052, 053, 054, 057, 067, 068, 069, 070, 071, 072, 073, 074, 075, 076, 077, 084, 128, 129, 137, 141, 143, 178, 179, 181, 182, 187, 191, 192, 193, 194, 195, 196, 199, 200, 201, 202, 203, 212, 213, 214, 215, 217, 218, 219, 224, 225

Les suppressions couvrent les héritages 1836 sans capacité 1776 suffisante, les concepts globalement trop spécifiques pour un tier, les grants napoléoniens/socialistes anachroniques et les quatre occurrences vanilla PRG inactives.

## K. Grants déjà couverts

Nombre = 17  
Indices matrice = 059, 061, 062, 064, 065, 066, 078, 079, 080, 081, 082, 083, 085, 086, 087, 093, 197

Les doublons sont explicitement reliés à `add_era_researched = era_1`, à une autre ligne du même tier, ou au remplacement tier-level `rationalism → codified_practical_knowledge`.

## L. Aliases à conserver exceptionnellement

Nombre = 4  
Indices matrice = 226, 227, 228, 229

Les quatre lignes sont exclusivement `urbanization` dans les tiers 3–6. Cette conservation est temporaire et strictement motivée par `building_urban_center` et `building_construction_sector`. Aucun autre alias de ce périmètre ne conserve un effet runtime non-starting.

## M. Technologies tardives proposées au start

LATE_STARTING_TECH_PROPOSALS = 1  
VERY_LATE_STARTING_TECH_PROPOSALS = 0

| Index | Scope | Target | Era | Justification |
|---|---|---|---|---|
| 063 | DEI | joint_stock_companies | era_6 | The Dutch East India Company is direct evidence for chartered joint-stock organization long before 1776, despite the node's era-6 placement. |

L'unique proposition tardive est `DEI → joint_stock_companies` (era 6). L'exception est volontaire: la VOC est précisément une compagnie à charte et capital-actions, ce qui démontre que l'era globale du nœud décrit mal ce pionnier particulier. Aucun target era 8+ n'est proposé.

## N. Cas historiques recherchés

- `dialectics`: les trois grants sont supprimés; aucune conversion vers `socialism` n'est proposée, le vocabulaire et les mouvements socialistes se consolidant au XIXe siècle (`H3`).
- `law_enforcement`: la police civile professionnelle est traitée comme postérieure à 1776 (`H2`); les polities à ordre légal codifié reçoivent un owner juridique plus ancien, les autres perdent le grant.
- `napoleonic_warfare`, reserves et mandatory service: le corps opérationnel relève de la période révolutionnaire/napoléonienne et postérieure (`H4`).
- `screw_frigate`: les brevets décisifs datent de 1836 (`H5`); seule l'architecture navale scientifique antérieure est proposée au tier 1.
- `line_infantry`: le Pattern 1769 confirme la cohérence d'une abstraction d'armes réglementées à la date de référence (`H6`).
- sériciculture asiatique: tradition ancienne, donc remplacement par l'owner visible du throughput et non suppression (`H7`).
- Japon: les surveys cadastraux et cartes provinciales Tokugawa soutiennent `systematic_cadastral_surveying`, jamais `modern_sewerage` (`H11`).
- Marathes/Perse: la flotte marathe subsiste comme capacité limitée malgré 1756 (`H12`); la Perse zand reste ambiguë entre projet naval propre et dépendance à la compagnie (`H13`, `H14`).
- DEI: les compagnies par actions sont attestées bien avant 1776, justifiant l'unique exception era 6 (`H9`).

## O. Arbitrages utilisateur

[START-01]

SCOPE = COUNTRY  
COUNTRY = HBC — Hudson Bay Company  
CURRENT_GRANT = deux fichiers mod effectifs donnent academia et line_infantry; le fichier `hubson` ajoute mandatory_service  
HIDDEN_TECH = academia, line_infantry, mandatory_service  
PROPOSED_ACTION = consolider le setup; garder une seule paire education/armes et supprimer mandatory_service  
PROPOSED_TARGET = institutionalized_scientific_exchange; regulated_small_arms  
ERA = era_1; era_2  
WHY = `hubson bay company.txt` et `hudson bay company.txt` initialisent tous deux `c:HBC`; l'intention canonique n'est pas déductible sans choisir le fichier autoritaire.  
ALTERNATIVE = conserver les deux fichiers et ne dédupliquer que les grants identiques  
CONSEQUENCE_RECOMMENDED = setup unique, aucun double grant, aucune conscription anachronique  
CONSEQUENCE_ALTERNATIVE = double initialisation HBC conservée et risque de divergences futures  
CONFIDENCE = LOW

[START-02]

SCOPE = COUNTRY  
COUNTRY = VNZ — Venezuela  
CURRENT_GRANT = vanilla `venezuela` appelle tier 3 + empiricism; mod `venezula` appelle tier 4 + academia  
HIDDEN_TECH = empiricism, academia  
PROPOSED_ACTION = consolider vers le fichier mod/canonique choisi puis conserver une seule capacité de connaissance  
PROPOSED_TARGET = codified_practical_knowledge ou institutionalized_scientific_exchange selon le setup retenu  
ERA = era_3 ou era_1  
WHY = les noms ne diffèrent pas seulement par la casse; les deux fichiers sont effectifs et assignent deux tiers concurrents au même tag.  
ALTERNATIVE = maintenir les deux blocs et accepter le cumul tier 3 + tier 4  
CONSEQUENCE_RECOMMENDED = un seul profil technologique 1776 cohérent  
CONSEQUENCE_ALTERNATIVE = sur-attribution massive et ordre de setup difficile à raisonner  
CONFIDENCE = LOW

[START-03]

SCOPE = COUNTRY  
COUNTRY = PER — Perse zand  
CURRENT_GRANT = admiralty  
HIDDEN_TECH = admiralty  
PROPOSED_ACTION = HUMAN_REVIEW_REQUIRED  
PROPOSED_TARGET = state_dockyard_systems  
ERA = era_1  
WHY = la Perse mène des opérations du Golfe et recherche du soutien naval, mais les sources ne tranchent pas clairement entre capacité étatique propre durable et dépendance aux navires de la Compagnie.  
ALTERNATIVE = REMOVE_STARTING_GRANT  
CONSEQUENCE_RECOMMENDED = reconnaît une capacité navale zand limitée  
CONSEQUENCE_ALTERNATIVE = évite de surestimer l'institutionnalisation navale  
CONFIDENCE = LOW

## P. Plan d'implémentation futur

`TECH6B3H_STARTING_TECH_RECONCILIATION_IMPLEMENTATION` devra:

1. résoudre START-01 à START-03;
2. créer un override mod de `00_starting_inventions.txt` reconstruit par tier et catégorie, en appliquant aussi l'audit des 18 grants déjà visibles et en explicitant/gelant les `add_era_researched`, sans substitution brute;
3. appliquer les décisions directes dans les country histories effectives seulement;
4. dédupliquer les targets visibles par country après expansion du tier;
5. conserver temporairement `urbanization`, puis le retirer lorsque les deux gates bâtiments auront un owner visible approuvé;
6. exécuter validation statique, smoke launch et revue visuelle de l'arbre dans une phase distincte.

NEXT_PHASE_READY = NO tant que les trois paquets START ne sont pas arbitrés.

## Q. Validation

| Contrôle | Résultat |
|---|---|
| TOTAL_INPUT_GRANTS | 229 |
| TOTAL_CLASSIFIED_GRANTS | 229 |
| SUM_SIX_ACTIONS | 229 |
| DIRECT + TIER + OTHER | 229 |
| UNCLASSIFIED_STARTING_GRANTS | 0 |
| UNKNOWN_COUNTRY_TAGS | 0 |
| UNKNOWN_TECH_IDS | 0 |
| INVENTED_TECH_IDS | 0 |
| INVENTED_OBJECT_IDS | 0 |
| INVENTED_FILE_PATHS | 0 |
| TARGET_CATEGORY_INVALID | 0 |
| PSYCHIATRY_STARTING_GRANTS | 0 |

Tous les targets existent. Tous sont visibles/recherchables et de même catégorie, sauf `urbanization`, explicitement conservé comme alias non recherchable pour compatibilité runtime. Les trois lignes `HUMAN_REVIEW_REQUIRED` de groupes comptent 8 grants individuels.

## R. Aucun changement gameplay

Cette phase a créé uniquement les trois documents TECH6B3G. Elle n'a modifié aucun fichier sous `common/`, `events/`, `gui/` ou `localization/`.

```text
GAMEPLAY_FILES_CHANGED = 0
STARTING_TECH_FILES_CHANGED = 0
STARTING_TECH_GRANTS_CHANGED = 0
TECH_TREE_FILES_CHANGED = 0
URBAN_BUILDING_GATE_CHANGES = 0
GUI_FILES_CHANGED = 0
COMMIT = NO
PUSH = NO
```

## Addendum TECH6B3H — arbitrages utilisateur désormais résolus

Cet addendum ne réécrit pas le constat historique de l'audit. Il enregistre les décisions utilisateur ultérieures appliquées par TECH6B3H et remet la matrice TECH6B3G en cohérence avec elles.

- `START-01 HBC = APPROVED` : consolidation vers l'unique fichier canonique `hbc - hudson bay company.txt`; `institutionalized_scientific_exchange` est conservée une fois; `regulated_small_arms` est fournie une fois par le tier 4 réconcilié; `mandatory_service` est supprimée.
- `START-02 VNZ = APPROVED` : le setup du mod est conservé sous le nom canonique exact `vnz - venezuela.txt`, ce qui neutralise le setup vanilla concurrent; le Venezuela n'est pas présent au lancement 1776 parce que la Nouvelle-Grenade détient alors ces territoires; aucune double attribution tier 3/tier 4 ne subsiste.
- `START-03 PER = APPROVED` : `admiralty` est remplacée par `state_dockyard_systems` pour la Sublime Zand.

Les huit lignes individuelles auparavant marquées `HUMAN_REVIEW_REQUIRED` ont été converties dans `TECH6B3G_STARTING_TECH_RECONCILIATION_MATRIX.csv` vers leurs actions finales. La matrice tier ne contenait aucun arbitrage humain et reste inchangée.

```text
HUMAN_REVIEW_REQUIRED_AFTER_ADDENDUM = 0
START_01_HBC_RESOLVED = YES
START_02_VNZ_RESOLVED = YES
START_03_PER_RESOLVED = YES
NEXT_PHASE_READY = YES
IMPLEMENTED_BY = TECH6B3H_STARTING_TECH_RECONCILIATION_IMPLEMENTATION
```
