# Phase NAVY-0 - Audit technique naval The Great Wave

## 1. Resume executif

La vraie vanilla utilisee pour cet audit est Victoria 3 The Great Wave / 1.13 dans `C:\Games\Victoria 3 The Great Wave\game`.

Conclusion principale : le mod possede deja des flottes converties vers les nouveaux `ship_type:*` de The Great Wave, mais beaucoup de formations militaires/navales utilisent encore des `hq_region = sr:region_*` obsoletes. Ces anciennes strategic regions ne sont plus actives dans la vanilla 1.13. Une formation navale avec un `hq_region` invalide peut echouer ou ne pas apparaitre correctement, ce qui explique beaucoup mieux le probleme "0 bateau au depart" que les types de navires eux-memes.

Le cas russe est coherent avec cette hypothese : les grandes flottes russes du mod utilisent surtout `hq_region = sr:region_russia`, qui existe encore en vanilla 1.13. D'autres puissances navales majeures utilisent des regions supprimees ou renommees, par exemple `region_england`, `region_france`, `region_occitania`, `region_iberia`, `region_madras`, `region_caribbean` ou `region_new_england`.

Cette phase n'a cree aucune flotte historique et n'a modifie aucun fichier gameplay.

## 2. Chemin vanilla utilise

Chemin confirme :

```text
C:\Games\Victoria 3 The Great Wave\game
```

Le sous-dossier `game` existe et a ete utilise comme reference principale pour :

- `common/ship_types`
- `common/ship_groups`
- `common/ship_modification_slots`
- `common/ship_modifications`
- `common/naval_mission_types`
- `common/naval_battle_conditions`
- `common/laws/00_navy_model.txt`
- `common/buildings`
- `common/production_methods`
- `common/history/military_formations`
- `common/history/buildings`
- `common/strategic_regions`
- `events/tech_events/naval_tech_events.txt`
- `events/brazil/brazil_navy.txt`
- localisations francaises vanilla des navires et lois navales

## 3. Fichiers vanilla navals identifies

Fichiers coeur du nouveau systeme naval :

| Domaine | Fichiers vanilla |
|---|---|
| Types de navires | `common/ship_types/00_ship_types.txt` |
| Groupes de navires | `common/ship_groups/00_ship_groups.txt` |
| Slots de conception | `common/ship_modification_slots/00_ship_modification_slots.txt` |
| Composants de conception | `common/ship_modifications/00_ship_modifications.txt`, `common/ship_modifications/01_utility_modifications.txt` |
| Noms de navires | `common/ship_name_definitions/*.txt` |
| Missions navales | `common/naval_mission_types/00_naval_mission_types.txt` |
| Conditions de bataille navale | `common/naval_battle_conditions/00_naval_battle_conditions.txt` |
| Lois navales | `common/laws/00_navy_model.txt` |
| Batiments navals | `common/buildings/01_industry.txt`, `05_military.txt`, `11_private_infrastructure.txt` |
| PM navales | `common/production_methods/01_industry.txt`, `05_military.txt`, `11_private_infrastructure.txt` |
| Formations initiales | `common/history/military_formations/*.txt` |
| Batiments historiques | `common/history/buildings/*.txt` |
| Technologies navales | `common/technology/technologies/10_production.txt`, `20_military.txt` |
| Transfert de navires | `common/treaty_articles/31_ship_transfer.txt` |
| Triggers noms de navires | `common/scripted_triggers/00_ship_name_triggers.txt` |
| JEs navales | `common/journal_entries/02_brazil_navy.txt` |
| Events navals | `events/tech_events/naval_tech_events.txt`, `events/brazil/brazil_navy.txt` |
| Gunboat diplomacy | surtout videos/evenements diplomatiques ; pas un fichier unique de flotte initiale |

Note importante : `common/defines/00_defines.txt` vanilla contient `SUPPLY_SHIP_TYPE = "ship_type_supply_ship"`. Le `ship_type_supply_ship` est donc traite specialement par le code.

## 4. Fichiers navals du mod identifies

Le mod ne contient pas de dossier custom actif pour :

- `common/ship_types`
- `common/ship_groups`
- `common/ship_modifications`
- `common/ship_modification_slots`
- `common/naval_mission_types`
- `common/buildings`
- `common/production_methods`

Donc les definitions navales vanilla 1.13 restent accessibles.

Fichiers du mod contenant directement du naval :

| Domaine | Fichiers du mod |
|---|---|
| Flottes et armees initiales | `common/history/military_formations/*.txt` |
| Ports, shipyards, administrations | `common/history/buildings/*.txt` |
| Lois | `common/laws/00_inject_laws.txt` seulement ; pas d'override naval direct |
| IA navale ancienne | `common/ai_strategies/00_default_strategy.txt` |
| Defines anciens | `common/defines/00_defines.txt` contient encore `NAVAL_BASE_BUILDING = "building_naval_base"` |
| Evenements navals | `events/tech_events/naval_tech_events.txt`, `events/brazil/brazil_navy.txt`, `events/decree_events.txt`, `events/dreadnought_hoax.txt`, etc. |
| Journal entries navales | `common/journal_entries/02_brazil_navy.txt` |
| Carte / sorties navales | `map_data/state_regions/08_middle_east.txt`, `map_data/state_regions/13_australasia.txt` |

Les `replace_paths` du mod remplacent notamment `events` et `common/journal_entries`, mais pas les definitions vanilla de navires, ship mods, batiments, production methods ou lois navales.

## 5. Probleme probable "0 bateau au depart"

Les types de navires utilises par le mod sont valides :

- `ship_type:ship_type_frigate`
- `ship_type:ship_type_ship_of_the_line`
- quelques references modernes dans events : `ship_type_early_ironclad`, `ship_type_monitor`

Le probleme le plus probable vient des `hq_region` obsoletes dans `common/history/military_formations/*.txt`.

Strategic regions invalides trouvees dans les formations du mod :

```text
region_anatolia
region_arabic
region_baltic
region_baltic_states
region_bengal
region_bombay
region_caribbean
region_caucasus
region_central_india
region_danubia
region_dixie
region_dnieper
region_dniepr
region_east_siberia
region_england
region_finland
region_france
region_iberia
region_italy
region_madras
region_manchuria
region_new_england
region_north_germany
region_occitania
region_persia
region_poland
region_punjab
region_rhine
region_south_germany
region_west_siberia
region_zanj
```

Exemples critiques :

- France : `region_france`, `region_occitania`
- Grande-Bretagne : `region_england`, `region_italy`, `region_new_england`, `region_madras`
- Espagne : `region_iberia`
- Etats-Unis / Amerique du Nord : `region_dixie`, `region_new_england`, `region_caribbean`
- Inde : `region_madras`, `region_bombay`, `region_bengal`, `region_punjab`

Les state regions internes des formations sont moins suspectes : une seule reference invalide ressort dans les formations, `STATE_ESTONIA`.

## 6. Explication du cas russe

Les formations russes principales du mod utilisent encore une region valide :

```text
hq_region = sr:region_russia
```

Cette region existe dans la vanilla 1.13. Les flottes russes situees sur cette region peuvent donc etre creees correctement, alors que les flottes britannique, francaise, espagnole ou indienne echouent probablement sur leurs `hq_region` obsoletes.

Il reste toutefois une anomalie russe partielle : une formation utilise `region_east_siberia`, invalide en 1.13. Le cas russe n'est donc pas "propre", mais il contient assez de `region_russia` valide pour expliquer pourquoi la Russie conserve des navires visibles.

## 7. Syntaxe recommandee pour les flottes initiales

Oui, les flottes initiales se creent toujours dans :

```text
common/history/military_formations/*.txt
```

Syntaxe minimale vanilla valide :

```txt
c:TAG ?= {
	create_military_formation = {
		type = fleet
		hq_region = sr:region_western_europe
		name = exemple_fleet_name

		ship = {
			type = ship_type:ship_type_ship_of_the_line
			count = 5
		}

		ship = {
			type = ship_type:ship_type_frigate
			count = 8
		}

		save_scope_as = exemple_fleet_scope
	}
}
```

Reponses techniques :

| Question | Reponse |
|---|---|
| Une flotte initiale se cree-t-elle encore dans `common/history/military_formations` ? | Oui. |
| Les navires sont-ils dans des blocs `ship = {}` ? | Oui, c'est la syntaxe la plus simple pour des paquets de navires. |
| Faut-il utiliser `ship_type:ship_type_frigate` et `ship_type:ship_type_ship_of_the_line` ? | Oui pour une marine a voile 1776. |
| Faut-il definir un modele de navire ? | Non pour les flottes initiales simples ; la vanilla utilise seulement le type et le count. |
| Les navires apparaissent-ils sans commandant ? | Oui. Un commandant/admiral est optionnel. |
| Ont-ils besoin d'une administration navale pour exister ? | Non pour etre crees au lancement. L'administration sert surtout au recrutement de marins et a la soutenabilite. |
| Ont-ils besoin d'un shipyard pour exister ? | Non pour exister au jour 1. Oui pour construire/remplacer ensuite. |
| Exemple vanilla le plus simple | Un bloc `create_military_formation = { type = fleet ... ship = { type = ship_type:... count = ... } }`. |

La vanilla utilise aussi parfois :

```txt
create_ship = {
	type = ship_type:ship_type_frigate
}
```

Mais pour NAVY-1A, le bloc `ship = { type = ... count = ... }` est plus clair et plus stable.

## 8. Types de navires disponibles

| ID technique | Nom francais vanilla | Groupe | Tech requise | 1776 ? | Voile ? | Role |
|---|---|---|---|---|---|---|
| `ship_type_ship_of_the_line` | Navire de ligne | Capital ships | `drydocks` | Oui si la tech est presente | Oui | Ligne de bataille |
| `ship_type_frigate` | Fregate | Cruisers | aucune tech explicite dans le type | Oui | Oui | Patrouille, escorte, reconnaissance |
| `ship_type_supply_ship` | Navire de ravitaillement | Supply ships | aucune tech explicite | A verifier avant usage 1776 | Oui/abstrait | Supply naval code-side |
| `ship_type_monitor` | Monitor | Capital ships | `ironclad_tech` | Non | Non | Defense cotiere cuirassee |
| `ship_type_early_ironclad` | Premier cuirasse | Capital ships | `ironclad_tech` | Non | Non | Cuirasse vapeur |
| `ship_type_coastal_defense_ship` | Navire de defense cotiere | Capital ships | `monitor_tech` | Non | Non | Defense littorale |
| `ship_type_modern_ironclad` | Cuirasse moderne | Capital ships | `monitor_tech` | Non | Non | Cuirasse avance |
| `ship_type_pre_dreadnought` | Pre-dreadnought | Capital ships | `pre_dreadnought_tech` | Non | Non | Capital ship fin XIXe |
| `ship_type_dreadnought` | Dreadnought | Capital ships | `dreadnought_tech` | Non | Non | Capital ship XXe |
| `ship_type_super_dreadnought` | Super-dreadnought | Capital ships | `battleship_tech` | Non | Non | Capital ship tardif |
| `ship_type_iron_frigate` | Fregate en fer | Cruisers | `ironclad_tech` | Non | Non | Frigate cuirassee/vapeur |
| `ship_type_troop_ship` | Navire de transport de troupes | Cruisers | `ironclad_tech` | Non pour 1776 strict | Non | Transport militaire |
| `ship_type_protected_cruiser` | Croiseur protege | Cruisers | `sea_lane_strategies` | Non | Non | Croiseur moderne |
| `ship_type_armored_cruiser` | Croiseur cuirasse | Cruisers | `pre_dreadnought_tech` | Non | Non | Croiseur lourd |
| `ship_type_light_cruiser` | Croiseur leger | Cruisers | `dreadnought_tech` | Non | Non | Croiseur rapide |
| `ship_type_seaplane_tender` | Navire de transport d'hydravions | Cruisers | `dreadnought_tech` | Non | Non | Reconnaissance aeronavale |
| `ship_type_aircraft_carrier` | Porte-avions | Cruisers | `carrier_tech` | Non | Non | Aviation navale |
| `ship_type_torpedo_boat` | Torpilleur | Torpedo craft | `self_propelled_torpedoes` | Non | Non | Attaque torpille |
| `ship_type_torpedo_boat_destroyer` | Destructeur de torpilleurs | Torpedo craft | `sea_lane_strategies` | Non | Non | Contre-torpilleurs |
| `ship_type_submarine` | Sous-marin | Torpedo craft | `submarine` | Non | Non | Guerre sous-marine |
| `ship_type_destroyer` | Destroyer | Torpedo craft | `destroyer` | Non | Non | Escorte moderne |

Pour les premieres phases 1776, utiliser seulement :

- `ship_type_ship_of_the_line`
- `ship_type_frigate`

Ne pas introduire encore de galeres, jonques, xebecs ou types custom : ce serait une phase de design specifique, pas une correction technique.

## 9. Composants de conception disponibles

Slots vanilla :

- `ship_mod_slot_armor`
- `ship_mod_slot_guns`
- `ship_mod_slot_propulsion`
- `ship_mod_slot_range`
- `ship_mod_slot_utility_1`
- `ship_mod_slot_utility_2`
- `ship_mod_slot_utility_3`

Composants pertinents pour 1776 :

| Type | Composants 1776 conservateurs |
|---|---|
| Fregate - armure | `ship_mod_frigate_armor_light`, `medium`, `high` |
| Fregate - canons | `ship_mod_frigate_guns_light`, `medium`; `high` demande `shell_gun` |
| Fregate - propulsion | `ship_mod_frigate_propulsion_light`; medium demande vapeur ancienne |
| Fregate - range | `ship_mod_frigate_range_light`, `medium`, `high` |
| Navire de ligne - armure | `ship_mod_ship_of_the_line_armor_light`, `medium`, `high` |
| Navire de ligne - canons | `ship_mod_ship_of_the_line_guns_light`, `medium`; `high` demande `shell_gun` |
| Navire de ligne - propulsion | `ship_mod_ship_of_the_line_propulsion_light`; medium demande vapeur ancienne |
| Navire de ligne - range | `ship_mod_ship_of_the_line_range_light`, `medium`, `high` |

Utility mods visibles :

- `utility_mod_patrol_boats`
- `utility_mod_extended_sick_bay`
- `utility_mod_fire_suppression`
- `utility_mod_landing_skiffs`
- `utility_mod_large_carronades`
- `utility_mod_torpedo_nets`
- `utility_mod_fire_control_system`
- `utility_mod_range_finder`
- `utility_mod_searchlights`
- `utility_mod_advanced_explosives`
- `utility_mod_camouflage`

Reponses techniques :

| Question | Reponse |
|---|---|
| Les navires initiaux doivent-ils avoir une conception explicite ? | Non. |
| Les pays peuvent-ils utiliser un modele par defaut ? | Oui, les `ship_type` definissent des `default_modifications`. |
| Peut-on creer des navires sans definir chaque composant ? | Oui. |
| Composants 1776 les plus logiques | Light armor, light/medium guns, light propulsion, range selon puissance. |
| Les composants sont-ils debloques par tech ? | Certains oui : shell guns, vapeur, torpilles, ironclads, etc. |
| Risque si composants indisponibles | Faible si on laisse les defaults ; eleve si on force des composants non debloques. |

Recommendation NAVY-1A : ne pas definir de design explicite. Creer uniquement des navires par type et count.

## 10. Batiments logistiques navals

### `building_port`

- Definition : `common/buildings/11_private_infrastructure.txt`
- Tech : `navigation`
- PM : `pmg_base_building_port`
- PMs :
  - `pm_anchorage`
  - `pm_basic_port`
  - `pm_industrial_port`
  - `pm_modern_port`
- Role : infrastructure maritime, production de `merchant_marine`, soutien commercial/logistique.
- Contraintes : etat cotier.
- Emplois : laborers, clerks, bureaucrats ; versions industrielles ajoutent machinists/engineers.
- Biens :
  - `pm_basic_port` consomme `clippers`, produit `merchant_marine`, ajoute infrastructure.
  - `pm_industrial_port` consomme `steamers` et `coal`, produit plus de `merchant_marine`.
  - `pm_modern_port` consomme `steamers` et `oil`, produit davantage de `merchant_marine`.

### `building_shipyard`

- Definition : `common/buildings/01_industry.txt`
- Alias : `building_shipyards`
- Tech : `navigation`
- PM : `pmg_base_building_shipyard`
- Role : construction civile et militaire de navires via `country_ship_construction_add`.
- Contraintes : etat cotier.
- PMs importantes :
  - `pm_basic_shipbuilding` : bois + fabric -> clippers, ship construction +5.
  - `pm_complex_shipbuilding` : wood/hardwood/fabric/engines -> clippers, ship construction +10, tech `screw_frigate`.
  - `pm_metal_shipbuilding` : steel/coal/engines -> steamers, ship construction +15, tech `gantry_cranes`.
  - `pm_arc_welding_shipbuilding` : steel/electricity/engines -> steamers, ship construction +20, tech `arc_welding`.
  - `pm_no_military_shipbuilding`
  - `pm_military_shipbuilding_wooden` : ship construction +2.
  - `pm_military_shipbuilding_wooden_2` : ship construction +5, tech `screw_frigate`.
  - `pm_military_shipbuilding_steam` : ship construction +10, tech `ironclad_tech`.
  - `pm_military_shipbuilding_steam_2` : ship construction +15, tech `arc_welding`.

Nuance importante : dans la vraie vanilla 1.13, `pm_military_shipbuilding_wooden` et `pm_military_shipbuilding_wooden_2` existent encore. Les erreurs de Phase 1.2 venaient probablement surtout de l'ancien `building_military_shipyard` ou d'un contexte de validation anterieur.

### `building_naval_administration`

- Definition : `common/buildings/05_military.txt`
- Tech : `admiralty`
- PM : `pmg_base_building_naval_administration`
- Role : recrutement de marins (`recruits_sailors = yes`), entrainement et capacite navale soutenable.
- PMs :
  - `pm_no_naval_theory`
  - `pm_power_of_the_purse`
  - `pm_jeune_ecole`
  - `pm_sea_lane_strategies`
  - `pm_battlefleet_tactics`
  - `pm_simple_sailor_recruitment`
- Emplois : soldats/officiers selon PM.
- Effet majeur : `country_sailors_max_add = 1000` avec `pm_simple_sailor_recruitment`.

### `building_naval_fortification`

- Definition : `common/buildings/05_military.txt`
- Tech : pas de tech de base explicite dans le batiment ; PM renforcee/avancee demande `concrete_fortifications`.
- Role : defense contre invasion navale, bataille navale locale, resistance au bombardement/blocus, controle de detroit.
- PMs :
  - `pm_naval_fortification_basic`
  - `pm_naval_fortification_reinforced`
  - `pm_naval_fortification_advanced`
- Biens :
  - basic : small arms + iron
  - reinforced : small arms + artillery + steel
  - advanced : small arms + artillery + ammunition + steel

### `building_naval_logistics_center`

- Definition : `common/buildings/05_military.txt`
- Non constructible directement (`buildable = no`, `expandable = no`, `downsizeable = no`)
- PM : `pm_basic_naval_logistics_center`
- Emplois : laborers, bureaucrats, officers.
- Role : logistique navale interne au nouveau systeme.

Reponses directes :

| Question | Reponse |
|---|---|
| Un pays peut-il avoir une flotte initiale sans administration navale ? | Oui, pour l'apparition au lancement. |
| Une flotte initiale consomme-t-elle des marins ? | Elle interagit avec la capacite de marins/supply ; sans administration, la soutenabilite risque d'etre mauvaise. |
| Faut-il ajouter des administrations navales pour GB/FRA/SPA ? | Probablement oui en NAVY-1B, apres verification des ports et techs. |
| Faut-il ajouter des shipyards ? | Oui pour construction/remplacement, mais pas pour faire apparaitre les navires au jour 1. |
| Faut-il augmenter les ports ? | A auditer par theatre ; eviter un buff global sans test. |

Etats a auditer en priorite pour NAVY-1B :

- Grande-Bretagne : Portsmouth, Plymouth, Chatham/Home Counties, Gibraltar, Halifax/Nova Scotia, Caraibes.
- France : Brest/Brittany, Toulon/Provence, Rochefort/Poitou, Antilles, Ile-de-France plus tard.
- Espagne : Ferrol/Galicia, Cadix/Andalusia, Cartagena/Valencia ou Murcia selon decoupage, Havane, Manille plus tard.

## 11. Lois navales et effets

Fichier vanilla : `common/laws/00_navy_model.txt`.

| Loi | ID | Tech | Effets principaux | Cohérence 1776 |
|---|---|---|---|---|
| Marine marchande | `law_merchant_navy` | aucune tech explicite | +30% construction supply ships/troop ships, -10% efficacite construction navale globale, -10% gain d'interets par navires | Bonne pour puissances commerciales ou secondaires |
| Jeune Ecole | `law_jeune_ecole` | `jeune_ecole` | bonus torpedo craft, cruisers modernes, couts navy reduits | Pas 1776 |
| Flotte capitale | `law_professional_navy` | `military_drill` | +25% embauche administration navale, +20% force politique officiers, +25% construction capital ships, +20% prestige naval | Bonne pour grandes marines de ligne |
| Flotte diplomatique | `law_diplomatic_navy` | `military_drill` | +20% ship interest gain, +25% construction cruisers, +10% embauche administration navale | Bonne pour presence globale, stations et empire |

Les effets d'interets favorables/defavorables ne sont pas definis directement dans `00_navy_model.txt`; ils passent par ideologies, petitions et preferences politiques ailleurs. Pour NAVY-1C, il faudra verifier les IGs si l'on force des lois au depart.

Proposition initiale sans modification :

| Pays | Loi proposee | Justification |
|---|---|---|
| Grande-Bretagne | `law_professional_navy` ou `law_diplomatic_navy` | Capital fleet pour la battlefleet ; diplomatic navy si on veut accentuer les stations mondiales. Pour le prototype, `law_professional_navy`. |
| France | `law_professional_navy` | Marine royale de ligne, arsenaux d'Etat, remontee apres 1778. |
| Espagne | `law_professional_navy` | Grande flotte imperiale de ligne et arsenaux. |
| Pays-Bas | `law_merchant_navy` | Puissance commerciale armee plus que battlefleet dominante. |
| Portugal | `law_merchant_navy` | Empire maritime moyen, escorte et commerce. |
| Danemark-Norvege | `law_merchant_navy` ou `law_professional_navy` | Baltique serieuse ; commencer marchand si l'on veut limiter la projection globale. |
| Suede | `law_professional_navy` pour Baltique, ou merchant par prudence | A trancher selon niveau voulu de Karlskrona. |
| Russie | `law_professional_navy` | Baltic fleet et prestige post-Tchesme. |
| Empire ottoman | `law_professional_navy` | Marine d'Etat regionale importante malgre Tchesme. |
| Puissances non europeennes | `law_merchant_navy` par defaut | Evite d'occidentaliser trop vite les flottes non oceaniques. |

## 12. Echelle historique -> jeu

Le fichier demande `GREAT_POWER_NAVIES_1776_DETAILED_INVENTORY.md`, mais ce fichier exact n'est pas present dans le depot. Le document disponible est :

```text
docs/research/WORLD_NAVIES_1776_THE_GREAT_WAVE_ROADMAP.md
```

Synthese de ce document :

- Grande-Bretagne : rang S, seule puissance vraiment globale.
- France : A+, contrepoids principal apres 1778.
- Espagne : A, grande masse imperiale.
- Pays-Bas, Russie, Danemark-Norvege, Suede, Ottomans, Portugal : B+/B/B- selon role.
- Etats-Unis : faible flotte reguliere, importance corsaire.
- Qing/Japon/Joseon/Siam : trafic maritime ou defense cotiere, pas de battlefleet occidentale.

Recommandation d'echelle :

| Option | Verdict |
|---|---|
| 1 unite de jeu = 1 navire historique | Trop lourd, risque de performances/equilibrage et de micro-gestion. |
| 1 unite de jeu = plusieurs navires historiques | Recommande. |
| Prototype NAVY-1A | 1 unite de jeu = environ 3 a 5 navires historiques pour les grandes marines, avec ajustement par role. |

Grille de depart proposee :

- Navires de ligne : 1 unite jeu represente environ 3 a 4 vaisseaux de ligne historiques.
- Fregates : 1 unite jeu represente environ 4 a 6 fregates/sloops/croiseurs legers historiques.
- Corsaires et compagnies commerciales : ne pas tout convertir en navires militaires ; utiliser plus tard events, modifiers, trade/supply ou JE.

Objectif de hierarchy :

- Grande-Bretagne nettement premiere.
- France deuxieme, avec potentiel de montee apres 1778.
- Espagne troisieme, forte en masse et ports imperiaux.
- Pays-Bas riche et commerciale, mais pas battlefleet egale a France/Espagne.
- Russie, Suede, Danemark-Norvege, Ottomans forts regionalement.
- USA tres faible en ligne, utile en frégates/corsaires.

## 13. Recommandation Phase NAVY-1A : flottes GB/FRA/SPA

Ne pas encore creer toutes les marines mondiales.

Ordre conseille :

1. Corriger uniquement les `hq_region` des flottes de Grande-Bretagne, France et Espagne.
2. Utiliser des strategic regions vanilla 1.13 valides :
   - GB metropole : `region_western_europe`
   - GB Mediterranee/Gibraltar : `region_southern_europe` ou region valide locale a confirmer
   - GB Amerique/Atlantique : `region_atlantic_coast` ou region valide locale a confirmer
   - France Atlantique : `region_western_europe`
   - France Mediterranee : `region_southern_europe`
   - Espagne : `region_southern_europe` ou autre region vanilla valide couvrant Iberie
3. Garder seulement `ship_type_ship_of_the_line` et `ship_type_frigate`.
4. Ne pas definir de designs.
5. Ne pas ajouter de supply ships au premier prototype sauf si les logs/le gameplay l'imposent.
6. Tester au jour 1, puis au 1er mois.

## 14. Recommandation Phase NAVY-1B : logistique GB/FRA/SPA

Apres apparition correcte des navires :

1. Auditer les ports existants dans `common/history/buildings/00_west_europe.txt`, `01_south_europe.txt`, `05_north_america.txt`, `06_central_america.txt`, `10_india.txt`.
2. Verifier shipyards et PMs dans les arsenaux :
   - Portsmouth / Plymouth / Chatham
   - Brest / Toulon / Rochefort
   - Ferrol / Cadix / Cartagena / Havana
3. Ajouter ou ajuster `building_naval_administration` seulement si la flotte existe mais manque de marins/supply.
4. Garder les niveaux conservateurs ; ne pas compenser l'echelle historique avec des batiments geants.

## 15. Recommandation Phase NAVY-1C : lois navales

Appliquer les lois seulement apres validation des flottes et de la logistique.

Plan recommande :

1. Verifier que `military_drill` est disponible pour les pays qui doivent avoir `law_professional_navy`.
2. Si la tech manque, choisir entre :
   - donner temporairement `law_merchant_navy` ;
   - ou ajouter la tech dans une phase technologie dediee.
3. Ne pas utiliser `law_jeune_ecole` en 1776.
4. Tester l'affichage et les effets politiques dans l'ecran des lois.

## 16. Risques techniques

Risques principaux :

- `hq_region` invalide : risque numero 1 pour la disparition des flottes.
- `state_region = s:STATE_ESTONIA` invalide dans les formations : a corriger separement si lie a une formation bloquante.
- `building_naval_base` encore reference dans `common/defines/00_defines.txt`, IA et events : ancien systeme potentiellement incompatible avec 1.13.
- `NAVAL_BASE_BUILDING = "building_naval_base"` dans les defines du mod : a auditer avant toute phase de naval bases.
- Events de technologie navale et Brazil Navy : utilisent `naval_power_projection`, `any_scope_ship`, `is_ship_type`; semblent proches de la vanilla mais a tester.
- `map_data/state_regions/08_middle_east.txt` et `13_australasia.txt` : naval exits deja sensibles ; ne pas melanger avec NAVY-1A.
- Forcer des composants de design non debloques : risque inutile.
- Ajouter trop de navires historiques : risque d'equilibrage, performance, couts de marins/supply et IA.

## 17. Tests a faire avant d'ajouter les flottes

Avant NAVY-1A :

1. Lancer une partie en observateur et verifier que les logs ne contiennent pas de nouvelles erreurs `create_military_formation`.
2. Rechercher dans les logs :
   - `PostValidate of effect 'create_military_formation' returned false`
   - `Invalid database object`
   - `strategic region`
   - `ship_type`
   - `fleet`
   - `sailors`
3. Tester au minimum :
   - Grande-Bretagne / IREK
   - France
   - Espagne
   - Russie
   - Pays-Bas
4. Verifier dans l'UI :
   - nombre de navires par pays ;
   - presence des flottes ;
   - regions de HQ ;
   - absence de crash au premier jour ;
   - passage au moins jusqu'au premier mois.
5. Comparer la Russie avant/apres pour confirmer que les regions valides sont bien la variable explicative.

Commandes utiles pour NAVY-1A :

```powershell
rg -n "hq_region = sr:region_(england|france|occitania|iberia|madras|new_england|caribbean|italy)" common/history/military_formations
rg -n "type = fleet|ship = \\{|type = ship_type:" common/history/military_formations
rg -n "building_naval_base|NAVAL_BASE_BUILDING|building_naval_administration|building_shipyard|building_port" common events
```

## Verification finale de cette phase

Cette phase a uniquement cree :

```text
PHASE_NAVY_0_THE_GREAT_WAVE_NAVAL_AUDIT.md
```

Aucune flotte historique, aucun batiment, aucune loi, aucune technologie, aucun pays et aucune localisation n'ont ete modifies par cette phase.
