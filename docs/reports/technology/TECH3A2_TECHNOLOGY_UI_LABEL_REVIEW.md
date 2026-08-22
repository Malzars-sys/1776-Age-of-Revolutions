# TECH-3A2 — Technology UI Label Review

## Status

`REVIEW_COMPLETE` · `LOCALIZATION_ONLY` · `RUNTIME_PENDING_AFTER_IMPLEMENTATION`

## Exact source baseline

- Commit: `e59685d60fd784f99fb64b8e16321524e5350880`
- English: `localization/english/tech3a_technology_l_english.yml`
- French: `localization/french/tech3a_technology_l_french.yml`
- Scope: the 118 implemented Era I–VI technologies.

Unlike the earlier draft, this review uses the **actual committed EN/FR localization values** from the implementation currently on `technology-rework`.

## Rule

- Keep the current label when it is **24 characters or fewer** in that language.
- Shorten only the language that exceeds 24 characters.
- Proposed labels are all **24 characters or fewer**.
- Do not rename technology IDs.
- Do not alter descriptions, prerequisites, eras, costs, layout, icons, unlocks, or gameplay.
- Long-form historical nuance remains available in the description/tooltips.

## Summary

- Technologies reviewed: **118**
- Technologies requiring at least one shorter label: **66**
- Technologies unchanged: **52**
- English values to change: **47**
- French values to change: **65**
- `SHORTEN_BOTH`: **46**
- `SHORTEN_EN`: **1**
- `SHORTEN_FR`: **19**
- Maximum proposed length: **24 EN / 24 FR**

## Proposed changes

| Branch | Era | Tech ID | English | French |
|---|---|---|---|---|
| Production | II | `improved_agricultural_implements` | Improved Agricultural Implements → **Improved Farm Tools** | Outils agricoles améliorés → **Outils agricoles** |
| Production | II | `turnpike_road_networks` | Turnpike Road Networks | Réseaux de routes à péage → **Routes à péage** |
| Production | III | `advanced_crop_rotations` | Advanced Crop Rotations | Rotations culturales avancées → **Rotations culturales** |
| Production | IV | `condensing_steam_engines` | Condensing Steam Engines | Machines à vapeur à condensation → **Vapeur à condensation** |
| Production | IV | `rotative_steam_power` | Rotative Steam Power | Force motrice à vapeur rotative → **Vapeur rotative** |
| Production | IV | `deep_mine_engineering` | Deep Mine Engineering | Ingénierie des mines profondes → **Mines profondes** |
| Production | V | `improved_road_engineering` | Improved Road Engineering → **Road Engineering** | Ingénierie routière améliorée → **Génie routier** |
| Production | V | `systematic_field_drainage` | Systematic Field Drainage → **Field Drainage** | Drainage agricole systématique → **Drainage agricole** |
| Production | V | `mine_safety_engineering` | Mine Safety Engineering | Ingénierie de la sécurité minière → **Sécurité minière** |
| Production | V | `continuous_papermaking` | Continuous Papermaking | Fabrication continue du papier → **Papier continu** |
| Production | V | `professional_civil_engineering` | Professional Civil Engineering → **Civil Engineering** | Génie civil professionnel → **Génie civil** |
| Production | VI | `interchangeable_manufacture` | Interchangeable Manufacture → **Interchangeable Parts** | Fabrication interchangeable → **Pièces interchangeables** |
| Military | I | `scientific_fortification_siegecraft` | Scientific Fortification & Siegecraft → **Fortification & Siege** | Fortification et poliorcétique scientifiques → **Fortification et siège** |
| Naval | I | `state_dockyard_systems` | State Dockyard Systems | Systèmes d’arsenaux d’État → **Arsenaux d’État** |
| Naval | I | `enclosed_dock_systems` | Enclosed Dock Systems | Systèmes de bassins fermés → **Bassins fermés** |
| Military | II | `regulated_small_arms` | Regulated Small Arms | Armes légères réglementaires → **Armes réglementaires** |
| Military | III | `light_infantry_tactics` | Light Infantry Tactics | Tactiques d’infanterie légère → **Infanterie légère** |
| Military | III | `standardized_field_artillery` | Standardized Field Artillery Systems → **Field Artillery** | Systèmes d’artillerie de campagne standardisés → **Artillerie de campagne** |
| Military | III | `permanent_military_hospitals` | Permanent Military Hospitals → **Military Hospitals** | Hôpitaux militaires permanents → **Hôpitaux militaires** |
| Naval | III | `scientific_naval_architecture` | Scientific Naval Architecture → **Naval Architecture** | Architecture navale scientifique → **Architecture navale** |
| Naval | III | `ship_classification_surveying` | Ship Classification & Surveying → **Ship Class & Survey** | Classification et inspection des navires → **Classement et inspection** |
| Military | IV | `armament_standardization_inspection` | Armament Standardization & Inspection → **Arms Standards & Checks** | Standardisation et inspection de l’armement → **Contrôle de l’armement** |
| Military | IV | `permanent_engineer_services` | Permanent Engineer Services → **Engineer Corps** | Services permanents du génie → **Corps du génie** |
| Military | IV | `military_topographic_surveying` | Military Topographic Surveying → **Military Surveying** | Levé topographique militaire → **Topographie militaire** |
| Military | IV | `mysorean_iron_cased_rocketry` | Mysorean Iron-Cased Rocketry → **Mysorean Rockets** | Fusées mysoréennes à enveloppe de fer → **Fusées mysoréennes** |
| Military | V | `corps_organization` | Corps Organization | Organisation en corps d’armée → **Corps d’armée** |
| Military | V | `field_engineering_pontoon_trains` | Field Engineering & Pontoon Trains → **Engineers & Pontoons** | Génie de campagne et trains de pontons → **Génie et pontons** |
| Military | V | `explosive_field_ammunition` | Explosive Field Ammunition → **Explosive Ammunition** | Munitions explosives de campagne → **Munitions explosives** |
| Military | V | `battlefield_evacuation` | Battlefield Evacuation | Évacuation du champ de bataille → **Évacuation des blessés** |
| Military | V | `military_veterinary_services` | Military Veterinary Services → **Veterinary Services** | Services vétérinaires militaires → **Services vétérinaires** |
| Military | V | `casemated_fortifications` | Casemated Fortifications | Fortifications casematées → **Forts casematés** |
| Naval | V | `standardized_naval_signals` | Standardized Naval Signals → **Naval Signals** | Signaux navals standardisés → **Signaux navals** |
| Naval | V | `mechanized_naval_dockyards` | Mechanized Naval Dockyards → **Mechanized Dockyards** | Arsenaux navals mécanisés → **Arsenaux mécanisés** |
| Naval | V | `diagonal_ship_framing` | Diagonal Ship Framing | Charpente navale diagonale → **Charpente diagonale** |
| Military | V | `standardized_military_rockets` | Standardized Military Rocket Systems → **Military Rockets** | Systèmes de fusées militaires standardisés → **Fusées militaires** |
| Naval | VI | `maritime_safety_standards` | Maritime Safety Standards → **Maritime Safety** | Normes de sécurité maritime → **Sécurité maritime** |
| Naval | VI | `modern_lighthouse_optics` | Modern Lighthouse Optics | Optique moderne des phares → **Optique des phares** |
| Naval | VI | `iron_hull_construction` | Iron Hull Construction | Construction de coques en fer → **Coques en fer** |
| Society | I | `institutionalized_scientific_exchange` | Institutionalized Scientific Exchange → **Scientific Exchange** | Échanges scientifiques institutionnalisés → **Échanges scientifiques** |
| Society | I | `international_relations` | International Relations | Relations internationales → **Relations extérieures** |
| Society | I | `institutionalized_public_credit` | Institutionalized Public Credit → **Public Credit** | Crédit public institutionnalisé → **Crédit public** |
| Society | I | `commercial_insurance_markets` | Commercial Insurance Markets → **Commercial Insurance** | Marchés de l’assurance commerciale → **Assurance commerciale** |
| Society | I | `periodical_print_networks` | Periodical Print Networks → **Periodical Press** | Réseaux de presse périodique → **Presse périodique** |
| Society | II | `systematic_administrative_statistics` | Systematic Administrative Statistics → **State Statistics** | Statistiques administratives systématiques → **Statistiques d’État** |
| Society | III | `codified_practical_knowledge` | Codified & Encyclopedic Practical Knowledge → **Codified Knowledge** | Savoirs pratiques codifiés et encyclopédiques → **Savoirs codifiés** |
| Society | III | `specialized_technical_academies` | Specialized Technical Academies → **Technical Academies** | Académies techniques spécialisées → **Académies techniques** |
| Society | III | `organized_elementary_schooling` | Organized Elementary Schooling → **Elementary Schooling** | Enseignement primaire organisé → **Enseignement primaire** |
| Society | III | `systematic_population_registration` | Systematic Population Registration → **Population Registers** | Enregistrement systématique de la population → **Registres de population** |
| Society | IV | `classical_political_economy` | Classical Political Economy → **Classical Economics** | Économie politique classique → **Économie classique** |
| Society | IV | `constitutional_government` | Constitutional Government → **Constitutional Rule** | Gouvernement constitutionnel → **Régime constitutionnel** |
| Society | IV | `national_sovereignty` | National & Popular Sovereignty → **Popular Sovereignty** | Souveraineté nationale et populaire → **Souveraineté populaire** |
| Society | IV | `organized_reform_movements` | Organized Reform Movements → **Reform Movements** | Mouvements réformateurs organisés → **Mouvements réformistes** |
| Society | IV | `abolitionist_mobilization` | Abolitionist Mobilization → **Abolitionism** | Mobilisation abolitionniste → **Abolitionnisme** |
| Society | IV | `systematic_cadastral_surveying` | Systematic Cadastral Surveying → **Cadastral Surveying** | Levé cadastral systématique → **Levé cadastral** |
| Society | IV | `systematic_legal_codification` | Systematic Legal Codification → **Legal Codification** | Codification juridique systématique → **Codification juridique** |
| Society | IV | `polytechnical_education` | Polytechnical Education | Enseignement polytechnique → **Éducation polytechnique** |
| Society | IV | `optical_telegraph_networks` | Optical Telegraph Networks → **Optical Telegraph** | Réseaux de télégraphie optique → **Télégraphe optique** |
| Society | V | `central_statistical_offices` | Central Statistical Offices → **Statistical Offices** | Bureaux centraux de statistique → **Bureaux statistiques** |
| Society | V | `organized_immunization_campaigns` | Organized Immunization Campaigns → **Immunization Campaigns** | Campagnes organisées d’immunisation → **Campagnes vaccinales** |
| Society | V | `experimental_research_laboratories` | Experimental Research Laboratories → **Research Laboratories** | Laboratoires de recherche expérimentale → **Recherche expérimentale** |
| Society | V | `specialized_professional_societies` | Specialized Professional Societies → **Professional Societies** | Sociétés professionnelles spécialisées → **Sociétés savantes** |
| Society | V | `clinicopathological_medicine` | Clinicopathological Medicine → **Clinical Pathology** | Médecine anatomoclinique |
| Society | V | `active_principle_pharmacy` | Active-Principle Pharmacy → **Active Principles** | Pharmacie des principes actifs → **Principes actifs** |
| Society | VI | `professional_civil_policing` | Professional Civil Policing → **Civil Policing** | Police civile professionnelle → **Police civile** |
| Society | VI | `liberal_constitutionalism` | Liberal Constitutionalism → **Liberal Constitution** | Constitutionnalisme libéral → **Constitution libérale** |
| Society | VI | `early_socialism_cooperativism` | Early Socialism & Cooperativism → **Socialism & Cooperatives** | Socialisme précoce et coopérativisme → **Socialismes coopératifs** |

## Semantic shorthand notes

The short labels below compress a concept rather than merely deleting an adjective. They are intentional UI shorthands; the full concept should remain in the description.

- `interchangeable_manufacture` — Uses the conventional 'interchangeable parts' shorthand for the manufacturing system.
- `ship_classification_surveying` — Both classification and surveying/inspection are retained in the short wording.
- `armament_standardization_inspection` — Condenses standardization + inspection into standards/checks (EN) and armament control (FR).
- `field_engineering_pontoon_trains` — Keeps both engineering and pontoons instead of dropping a co-equal concept.
- `international_relations` — FR uses 'Relations extérieures', a compact near-equivalent rather than the broader 'Diplomatie'.
- `national_sovereignty` — Short card prioritizes popular sovereignty; national dimension remains in the description.
- `experimental_research_laboratories` — FR short label emphasizes experimental research rather than the laboratory institution.
- `specialized_professional_societies` — FR uses the period-appropriate shorthand 'Sociétés savantes'.
- `active_principle_pharmacy` — Short card emphasizes the active-principle innovation; pharmacy context remains in description.
- `liberal_constitutionalism` — Short card uses 'Liberal Constitution / Constitution libérale' as UI shorthand for constitutionalism.
- `early_socialism_cooperativism` — Short label preserves socialism + cooperativism; the 'early' qualification is carried by Era VI and description.

## Unchanged labels

The remaining 52 technologies already fit the 24-character target in both languages and should not be modified in TECH-3A2.

## Runtime hand-off

After implementation, test at normal UI scale. The most important visual checks are the Society tree, the long Military/Naval institutional labels, and `optical_telegraph_networks`, whose current French label is visibly prone to truncation.