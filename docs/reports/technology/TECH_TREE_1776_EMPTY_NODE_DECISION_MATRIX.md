# Matrice de décision — derniers nœuds technologiques vides

Périmètre : technologies visibles et recherchables qui n'avaient aucun effet direct affiché avant cette passe. Les alias techniques non recherchables sont exclus.

## Dette technique obligatoire

Les modificateurs ci-dessous sont désormais implémentés, mais ils sont uniquement des effets temporaires. Chaque ligne conservée constitue une dette de conception à résorber : le bonus devra être remplacé ou complété par de vrais bâtiments, méthodes de production, institutions, unités ou systèmes correspondant à la branche future indiquée. Une technologie ne doit sortir de ce registre qu'après intégration et validation runtime de ce contenu propre.

| Nom du nœud | Décision | Modificateur temporaire implémenté | Branche future supportée |
|---|---|---|---|
| Classement et inspection (`ship_classification_surveying`) | Garder | `building_naval_administration_throughput_add = 0.05` | Registres navals, inspection des coques et administration maritime |
| Contrôle de l’armement (`armament_standardization_inspection`) | Garder | `building_group_bg_military_industry_throughput_add = 0.05` | Normalisation, contrôle qualité et bancs d’épreuve de l’armement |
| Topographie militaire (`military_topographic_surveying`) | Garder | `unit_army_offense_mult = 0.025` | Cartographie d’état-major, reconnaissance et planification opérationnelle |
| Évacuation des blessés (`battlefield_evacuation`) | Garder | `unit_recovery_rate_add = 0.05` | Ambulances, hôpitaux de campagne et médecine militaire |
| Charpente diagonale (`diagonal_ship_framing`) | Garder | `ship_hit_points_max_mult = 0.05` | Construction navale en bois renforcé et transition vers les coques métalliques |
| Levé hydrographique (`hydrographic_surveying`) | Garder | `ship_max_distance_to_port_mult = 0.05` | Cartes marines, balisage, phares et services hydrographiques |
| Coques en fer (`iron_hull_construction`) | Garder | `ship_armor_mult = 0.05` | Chantiers métalliques, blindage et familles de navires cuirassés |
| Sécurité maritime (`maritime_safety_standards`) | Garder | `ship_suffered_crew_damage_mult = -0.05` | Réglementation maritime, sauvetage, assurance et marine marchande |
| Drainage agricole (`systematic_field_drainage`) | Garder | `building_group_bg_agriculture_throughput_add = 0.03` | Drainage, assèchement, irrigation et amélioration foncière |
| Fonte à vent chaud (`hot_blast_smelting`) | Garder | `building_group_bg_heavy_industry_throughput_add = 0.03` | Hauts-fourneaux, combustibles métallurgiques et sidérurgie avancée |
| Réseaux de variolisation (`variolation_networks`) | Garder | `state_mortality_mult = -0.0025` | Campagnes sanitaires précoces et diffusion des soins préventifs |
| Science vétérinaire (`veterinary_science`) | Garder | `building_livestock_ranch_throughput_add = 0.05` | Santé animale, élevage, épizooties et services vétérinaires militaires |
| Souveraineté populaire (`national_sovereignty`) | Garder | `country_influence_add = 10` | Nationalités, citoyenneté, autodétermination et diplomatie des États-nations |
| Métrologie scientifique (`scientific_metrology`) | Garder | `country_tech_spread_mult = 0.025` | Poids et mesures, normes industrielles, laboratoires et industrie de précision |
| Codification juridique (`systematic_legal_codification`) | Garder | `country_law_enactment_success_add = 0.02` | Codes civils, tribunaux, professions juridiques et administration judiciaire |
| Vaccination (`vaccination`) | Garder | `state_mortality_mult = -0.005` | Vaccination de masse, production vaccinale et institution sanitaire |
| Médecine anatomoclinique (`clinicopathological_medicine`) | Garder | `state_harvest_condition_disease_outbreak_impact_mult = -0.10` | Hôpitaux cliniques, diagnostic, laboratoires médicaux et pathologie |
