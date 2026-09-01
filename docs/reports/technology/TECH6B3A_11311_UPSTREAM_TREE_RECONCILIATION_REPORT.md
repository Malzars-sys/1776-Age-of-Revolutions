# TECH6B3A — Réconciliation 1.13.11, arbre technologique et mod Steam

> Mise à jour TECH6B3E : les constats TECH6B3A restent la baseline historique, mais `joint_stock_companies` est maintenant recherchable en ère 6 et visible dans le GUI. Les sept familles de corrections humaines postérieures — Protectionnisme, assurance publique, partage droits/travail/aide sociale, athéisme d'État, Terakoya, cinq lois d'esclavage et visibilité financière — priment sur les anciennes affectations. La matrice d'exigences possède une colonne de réconciliation autoritative.

Audit statique uniquement. Aucun fichier gameplay n’a été modifié, aucun commit/push n’a été effectué et aucune nouvelle validation runtime n’est revendiquée.

## A. Checkpoint

- Branche : tech6b2-society-gameplay-implementation.
- Baseline à préserver : 50 fichiers gameplay TECH6B2 non committés, soit 34 shadows documentés et 16 fichiers mod existants.
- Vanilla canonique : C:\Games\Victoria 3\game.
- Exécutable : FileVersion=1.13.11 et ProductVersion=1.13.11.
- Checksum installé : d4d2f0b81a1f4812d11a8485922ea47f.
- Ancienne preuve : inventaire exact XXH3-128 C:\Games\Victoria 3\v1.13.9.xxh128, complété par les shadows 1.13.9 documentés.
- Livrables : les quatre documents TECH6B3A autorisés, et uniquement eux.

Il n’existe pas de copie source vanilla 1.13.9 complète. L’inventaire démontre exactement qu’un fichier est identique ou différent, mais ne permet pas de reconstruire les anciennes lignes d’un fichier changé. Les copies TECH6B2 sont classées DOCUMENTED_1139_SHADOW ; les contenus anciens non récupérables restent NO_1139_BASELINE_AVAILABLE. Aucun ancien contenu n’a été inventé.

## B. Version vanilla 1.13.9 → 1.13.11

5 531 fichiers de scripts/données installés ont été hashés sous common, events, map_data, gui et localization, puis tous les chemins coïncidant avec le fork ont été examinés.

- 754 fichiers du fork ont un chemin identique dans vanilla 1.13.11.
- 753 sont des fichiers de jeu/données ; common/amendments/amendments.md est le seul document non-runtime.
- 745 chemins ont exactement le même hash vanilla en 1.13.9 et 1.13.11.
- 9 shadows actuels ont changé côté vanilla.
- 14 anciens chemins encore présents dans le fork ont été supprimés ou consolidés en 1.13.11.
- MINI_MIGRATION_11311_REQUIRED = YES.

Les neuf collisions actuelles sont :

1. common/ai_strategies/00_default_strategy.txt
2. common/defines/00_defines.txt
3. common/journal_entries/02_coffee_and_milk.txt
4. common/on_actions/00_code_on_actions.txt
5. common/production_methods/04_plantations.txt
6. events/agitators_events/algeria_events.txt
7. events/tech_events/society_tech_events.txt
8. gui/building_details_panel.gui
9. gui/production_methods.gui

Le shadow Society est une copie byte-identique de 1.13.9. Les deux deltas Banana et deux nouveaux événements Society sont démontrés. Pour les sept autres chemins, le changement vanilla est prouvé mais le contenu source 1.13.9 n’est plus disponible : réconciliation manuelle, jamais remplacement intégral.

### Renommage des lois

Neuf fichiers 00_*.txt ont changé de chemin. Les shadows TECH6B2 ne remplacent donc plus le vanilla actuel et 50 IDs de lois peuvent être chargés deux fois.

| Ancien shadow | Chemin 1.13.11 | IDs |
|---|---|---:|
| common/laws/00_economic_system.txt | common/laws/01_economic_system.txt | 8 |
| common/laws/00_education_system.txt | common/laws/01_education_system.txt | 5 |
| common/laws/00_free_speech.txt | common/laws/02_free_speech.txt | 4 |
| common/laws/00_health_system.txt | common/laws/01_health_system.txt | 4 |
| common/laws/00_land_reform.txt | common/laws/01_land_reform.txt | 9 |
| common/laws/00_policing.txt | common/laws/01_policing.txt | 4 |
| common/laws/00_taxation.txt | common/laws/01_taxation.txt | 5 |
| common/laws/00_trade_policy.txt | common/laws/01_trade_policy.txt | 6 |
| common/laws/00_welfare.txt | common/laws/02_welfare.txt | 5 |

La future implémentation devra reconstruire chaque shadow depuis le fichier 1.13.11, réappliquer seulement l’intention TECH6B2/arbre approuvée, puis retirer l’ancien chemin.

Compatibilité des 34 shadows TECH6B2 :

- TECH6B2_SHADOW_11311_COMPATIBLE = 24
- TECH6B2_SHADOW_NEEDS_FORWARD_PORT = 1, society_tech_events.txt
- TECH6B2_SHADOW_CONFLICTS_WITH_11311 = 9, les lois renommées

## C. Sentinelles des notes de version

### Technologies

Les cinq fichiers vanilla des répertoires technology/technologies et technology/eras ont des hashes identiques entre 1.13.9 et 1.13.11.

- arc_welding : vanilla a electric_arc_process + pneumatic_tools et le bonus Capital Ships +20 ; le fork conserve le bonus mais seulement electric_arc_process.
- concrete_dockyards : parent floating_harbor et bonus +10 déjà équivalents.
- military_aviation : parent vanilla handcranked_machine_gun, parent fork wargaming ; écart de refonte, pas delta temporel démontré.
- l’objet Seaplane Tender exact est ship_type_seaplane_tender dans common/ship_types/00_ship_types.txt, gate dreadnought_tech. Aucun ID seaplane_tenders n’existe.

La nouvelle instruction reinforced_concrete → arc_welding est prioritaire sur une copie de l’arête vanilla.

### Starting technologies

Les six fichiers exacts sont luc - lucca.txt, mod - modena.txt, pap - papal states.txt, par - parma.txt, sic - two sicilies.txt et tus - tuscany.txt. Tous contiennent Banking et chacun a déjà le même hash en 1.13.9 et 1.13.11. Statut conservé : DEFER_STARTING_TECH.

### Ressources

Les 17 fichiers map_data/state_regions/*.txt sont inchangés. Aucun potentiel Coal/Iron/Sulfur/Lead inférieur à 3 n’existe dans le vanilla installé. Aucun port de carte. Le shadow total-conversion 13_australasia.txt reste intentionnel.

### Companies

- company_mozambique_company est dans common/company_types/00_companies_europe.txt, pas dans le shadow Afrique. Le fork n’en masque pas le fichier. Les bâtiments actuels sont Cotton, Tea et Millet. Le hash vanilla est inchangé : AUTO_INHERITED.
- company_nhm est dans 00_companies_ep2.txt. Vanilla possède Coffee/Sugar/Dye en base et Tobacco/Opium/Tea en extension ; le fork conserve cela et ajoute Spice en base selon TECH6A : FORK_ALREADY_EQUIVALENT.

### Banana Plantations

- default_building_banana_plantation : vanilla 30 Fruit, fork 35.
- automatic_irrigation_building_banana_plantation : vanilla 40 Fruit, fork 35.

Les deux ports sont exacts et candidats.

### Événements

- Le titre installé est A Doctrine of Iron and Steam, non Iron and Steel.
- L’ID est military_tech_events.403 et son bloc est inchangé.
- flamethrowers_event.1 et military_tech_events.402 utilisent désormais le scope optionnel ?=.
- Les fragments militaires doivent être consolidés vers military_tech_events.txt.
- Le fichier Society consolidé ajoute exactement society_tech_events.104 et .105 ; les anciens fragments Society doivent y être migrés.

### API

Seul days_since_movement_defeated est utilisé, dans common/political_movements/00_ideological_movements.txt. L’API 1.13.11 requise est disponible. Les six autres sentinelles ne sont pas utilisées et restent NOT_USED_BY_MOD.

## D. Compatibilité same-path

La matrice vanilla contient 768 lignes fichier, soit 754 shadows actuels et 14 anciens chemins déplacés, puis 26 lignes sémantiques.

- collisions demandant réconciliation : 23 chemins ;
- chemins actuels vanilla inchangés : 745 ;
- groupes de port mécaniques démontrés : 13 ;
- overrides mod changés sans source ancienne reconstructible : 7 ;
- copie intégrale d’un shadow : interdite.

## E. Compatibilité replace_path

descriptor.mod contient deux chemins : common/technology/eras et common/technology/technologies.

La metadata moderne en contient cinq : common/history/characters, common/history/diplomatic_plays, common/history/diplomacy, common/technology/eras et common/technology/technologies.

Les cinq fichiers vanilla des namespaces technologiques sont inchangés :

- VANILLA_REPLACE_PATH_COLLISIONS = 0
- REPLACE_PATH_DELTAS_REQUIRING_PORT = 0

Les différences Arc Welding/Military Aviation relèvent de la refonte du fork et du nouveau cahier, non d’un delta temporel local.

## F. Exigences de correction de l’arbre

Le cahier a été lu intégralement et décomposé en 79 demandes :

- Production : P01–P40
- Militaire : M01–M08
- Société : S01–S31

Répartition :

- 36 GAMEPLAY_GATE_CORRECTION_REQUIRED
- 17 NEW_USER_OVERRIDE
- 23 CONFLICT_REQUIRES_USER_DECISION
- 1 VISIBLE_DISPLAY_BUG
- 2 OLD_AUDIT_ALREADY_CORRECT

73 lignes désignent un objet existant exact. Les six lignes sans object_id décrivent volontairement des objets futurs ou des responsabilités agrégées encore à définir ; ce ne sont ni des IDs inconnus ni des IDs inventés.

## G. Causes réelles des gates/unlocks visibles

- Le premier +10 d’échelle existe sur mechanized_workshops, mais cette technologie est cachée par can_research=no.
- pm_gas_streetlights a un bloc unlocking_technologies vide.
- pm_market_squares dépend de professional_civil_engineering ; l’ID exact de Routes à péage est turnpike_road_networks.
- Les PM Dye, Sewing et Electric Sewing dépendent de organized_textile_production, mechanized_spinning et electrical_capacitors.
- Les six exploitations organisées héritées dépendent de enclosure ; la plantation de coton aussi.
- 13 compagnies utilisent building_cotton_plantation, avec des conditions technologiques différentes.
- Les cinq pompes à condensation ont condensing_steam_engines + deep_mine_engineering.
- mobilization_option_first_aid dépend de triage.
- pm_percussion_caps n’a pas de gate technologique explicite.
- Le deuxième PM naval dépend de breech_loading_artillery.
- L’université dépend de institutionalized_scientific_exchange.
- Les PM de philosophie dépendent de codified_practical_knowledge et analytical_philosophy.
- joint_stock_companies est cachée en era 7 ; stock_exchange porte +2 compagnies et +2 chartes.

Les nouvelles technologies/PM, la réforme Human Rights/Abolition, la diffusion, l’innovation et les topologies médicale/policière restent sans cible assez précise. Aucun ID ou chemin n’a été fabriqué.

## H. STEAM MAIN MOD — WORKSHOP 3780935876

- Chemin exact : C:\Program Files (x86)\Steam\steamapps\workshop\content\529340\3780935876.
- Identité confirmée par l’item 3780935876, le descriptor 1776 - Age of Revolutions Fork, la metadata 2.3.1 et l’entrée ACF manifest=2186545669577001610.
- descriptor : support 1.13.* ; metadata interne : support 1.13.9.

Baseline exacte retrouvée :

C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source

La metadata indique 1776 - Age of Revolutions, Total Conversion Mod, version 2.3.0.1, support 1.13.10. Elle contient 842 fichiers : EXACT_SNAPSHOT.

Cette copie n’a pas été mise à jour, car cela détruirait la seule preuve temporelle exacte. Une future copie actualisée devra utiliser un autre répertoire clairement nommé.

Le dossier Age of revolution Fork [Steam Build] est byte-identique au Workshop actuel pour 889 fichiers. workshop_build\Age_of_Revolution_Fork est un contrôle de packaging presque identique, non une baseline temporelle utile.

## I. Changements Steam détectés

- fichiers changés : 630
- ajoutés : 95
- supprimés : 48
- modifiés : 487
- shadows vanilla actuels : 687
- nouveaux shadows : 9
- shadows mis à jour : 445

Nouveaux shadows :

1. common/ai_strategies/00_default_strategy.txt
2. common/country_definitions/00_countries.txt
3. common/history/countries/skh - sakhalin.txt
4. common/history/countries/ult - ulta.txt
5. common/interest_groups/00_landowners.txt
6. gui/frontend/frontend_loadingscreen.gui
7. gui/frontend/frontend_main.gui
8. localization/french/country_flavor_text_l_french.yml
9. music/main_themes/music.txt

Parmi les 582 fichiers présents côté Workshop après changement, 502 sont déjà byte-identiques dans le fork, 80 divergent et 0 manque.

Sur 48 suppressions, 44 sont déjà absentes. Quatre fichiers restent dans le fork : Changelog.txt, Source.txt, events/japan_events/ep2_shogunate_events.txt et events/vampire_panic_events.txt. Les deux événements sont des responsabilités TECH6B2.

Aucun changement Steam ne devient byte-identique au vanilla 1.13.11 alors que le snapshot ancien différait : STEAM_11311_FORWARD_PORTS_ALREADY_PRESENT = 0.

## J. Conflits four-way

- collisions de chemin avec le fork : 586, soit 582 chemins actuels et 4 suppressions retenues ;
- réconciliations manuelles : 84 fichiers ;
- collisions objet exactes : 17 dans 11 fichiers.

Objets exacts : company_dutch_east_india_company ; COUNTRIES dans l’historique France ; je_age_of_princes ; je_liberalism_1 ; je_springtime_of_the_peoples ; je_technocracy ; law_mercantilism_navigation_acts ; law_merchant_banking ; on_monthly_pulse_country ; french_revolution_mod_events.14 et .18 ; ig_suppression_events.1000, .1001 et .3 ; STATE_QUEENSLAND ; STATE_SOUTH_AUSTRALIA ; STATE_WESTERN_AUSTRALIA.

Les deux lois de common/laws/00_inject_laws.txt touchent aussi l’arbre. Aucun fichier ne doit être copié en bloc.

## K. Réconciliation croisée

37 chemins sont concernés par au moins deux sources :

| Chemin | Sources |
|---|---|
| common/ai_strategies/00_default_strategy.txt | vanilla + Steam |
| common/company_types/00_companies_africa.txt | arbre + TECH6B2 |
| common/company_types/00_companies_asia.txt | arbre + TECH6B2 |
| common/company_types/00_companies_france.txt | arbre + TECH6B2 |
| common/company_types/00_companies_russia.txt | arbre + TECH6B2 |
| common/company_types/00_companies_soi.txt | arbre + TECH6B2 |
| common/defines/00_defines.txt | vanilla + Steam |
| common/journal_entries/00_ethiopia.txt | Steam + TECH6B2 |
| common/journal_entries/00_liberalism.txt | Steam + TECH6B2 |
| common/journal_entries/00_peoples_springtime_je.txt | Steam + TECH6B2 |
| common/journal_entries/02_coffee_and_milk.txt | vanilla + Steam |
| common/journal_entries/05_technocracy.txt | Steam + TECH6B2 |
| common/laws/00_church_and_state.txt | arbre + TECH6B2 |
| common/laws/00_economic_system.txt | vanilla + arbre + TECH6B2 |
| common/laws/00_education_system.txt | vanilla + TECH6B2 |
| common/laws/00_free_speech.txt | vanilla + TECH6B2 |
| common/laws/00_health_system.txt | vanilla + TECH6B2 |
| common/laws/00_inject_laws.txt | Steam + TECH6B2 |
| common/laws/00_land_reform.txt | vanilla + TECH6B2 |
| common/laws/00_policing.txt | vanilla + TECH6B2 |
| common/laws/00_taxation.txt | vanilla + TECH6B2 |
| common/laws/00_trade_policy.txt | vanilla + TECH6B2 |
| common/laws/00_welfare.txt | vanilla + TECH6B2 |
| common/on_actions/00_code_on_actions.txt | vanilla + Steam |
| common/technology/technologies/30_tech3a_society.txt | arbre + TECH6B2 |
| common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt | arbre + TECH6B2 |
| events/agitators_events/agitator_law_events_2.txt | Steam + TECH6B2 |
| events/agitators_events/algeria_events.txt | vanilla + Steam |
| events/belle_epoque_events.txt | Steam + TECH6B2 |
| events/french_revolution_mod_events.txt | Steam + TECH6B2 |
| events/ig_petitions.txt | Steam + TECH6B2 |
| events/ig_suppression_events.txt | Steam + TECH6B2 |
| events/japan_events/ep2_shogunate_events.txt | Steam + TECH6B2 |
| events/soi_events/00_lobbies_events_03.txt | Steam + TECH6B2 |
| events/tech_events/flamethrowers_event.txt | vanilla + Steam |
| events/tech_events/military_tech_events_01.txt | vanilla + Steam |
| events/vampire_panic_events.txt | Steam + TECH6B2 |

Priorité : instruction utilisateur actuelle, total conversion, compatibilité 1.13.11, correction Steam utile, ancien design figé, balance Steam non essentielle.

## L. Actions mécaniques sûres proposées

1. Reconstruire les neuf shadows de lois aux chemins 1.13.11.
2. Consolider les événements militaires et porter les deux opérateurs ?=.
3. Consolider les événements Society et ajouter .104/.105.
4. Porter les valeurs Banana 30/40.
5. Après approbation du lot, appliquer les 53 corrections d’arbre exactes.
6. Ne rien copier depuis Steam avant arbitrage des 17 objets et 84 fichiers.

## M. Décisions humaines restantes

24 exigences demandent encore un choix : propriétaire du +10 d’échelle ; identité de la technologie Electric Sewing ; gate de pm_percussion_caps ; réforme Human Rights/Abolition ; technologies tardives des lois ; clé/valeur de diffusion ; plafond d’innovation ; nouveaux PM universitaires ; topologie médicale ; position de professional_civil_policing ; era et relations de joint_stock_companies.

S’ajoutent sept shadows vanilla changés sans source ancienne et 84 fichiers Steam à réconcilier.

## N. Portée de la prochaine phase

Une implémentation globale n’est pas prête. Le travail futur doit être séparé :

1. mini-migration 1.13.11 mécanique ;
2. décisions humaines sur 24 lignes ;
3. implémentation des 53 corrections exactes approuvées ;
4. réconciliation Steam ciblée ;
5. phase Starting Technologies ;
6. validation statique et runtime après implémentation.

Le snapshot 2.3.0.1 doit rester immuable. Un miroir actualisé doit être distinct.

## Résumé final

TECH6B3A_RECONCILIATION_AUDIT = PASS

BRANCH = tech6b2-society-gameplay-implementation

OLD_CANONICAL_VANILLA = 1.13.9
NEW_CANONICAL_VANILLA = 1.13.11

VANILLA_11311_CONFIRMED = YES
VANILLA_11311_VERSION_CONFIRMED = YES
VANILLA_FILES_AUDITED = 5531
MINI_MIGRATION_11311_REQUIRED = YES

FORK_SAME_PATH_SHADOWS = 754
REPLACE_PATH_DIRECTORIES = 5
VANILLA_CHANGED_SHADOW_COLLISIONS = 23
VANILLA_REPLACE_PATH_COLLISIONS = 0
SHADOWS_REQUIRING_11311_REFRESH = 23
REPLACE_PATH_DELTAS_REQUIRING_PORT = 0
VANILLA_FORWARD_PORT_CANDIDATES = 13
VANILLA_DELTAS_REQUIRING_FORWARD_PORT = 13
VANILLA_FORWARD_PORT_ACTIONS = 13
ALREADY_EQUIVALENT = 745
INTENTIONAL_OVERRIDES = 7

TREE_CORRECTION_REQUIREMENTS = 79
TREE_CORRECTION_OBJECTS_RESOLVED = 73
TREE_CORRECTION_UNKNOWN_IDS = 0
TREE_CORRECTION_IMPLEMENTATION_CANDIDATES = 53
TREE_CORRECTION_HUMAN_REVIEW = 24

MAIN_MOD_PATH_RESOLVED = YES
MAIN_MOD_PATH = C:\Program Files (x86)\Steam\steamapps\workshop\content\529340\3780935876
UPSTREAM_SHADOWS_FOUND = 687
UPSTREAM_CHANGED_SHADOWS = 454
UPSTREAM_FORK_COLLISIONS = 586
UPSTREAM_SAFE_FORWARD_PORTS = 0
UPSTREAM_MANUAL_RECONCILIATIONS = 84

STEAM_MAIN_MOD_AUDIT = PASS
STEAM_MAIN_MOD = Workshop 3780935876
STEAM_MAIN_MOD_WORKSHOP_ID = 3780935876
STEAM_MAIN_MOD_PATH = C:\Program Files (x86)\Steam\steamapps\workshop\content\529340\3780935876
STEAM_MAIN_MOD_IDENTITY_CONFIRMED = YES
STEAM_BASELINE_RESOLVED = YES
STEAM_BASELINE_TYPE = EXACT_SNAPSHOT
STEAM_BASELINE_REF = C:\Users\simeo\Documents\Paradox Interactive\Victoria 3\mod\1776_Age_of_Revolutions_hotfix_source
STEAM_FILES_CHANGED_SINCE_BASELINE = 630
STEAM_NEW_FILES = 95
STEAM_REMOVED_FILES = 48
STEAM_MODIFIED_FILES = 487
STEAM_CURRENT_SHADOWS = 687
STEAM_NEW_SHADOWS = 9
STEAM_UPDATED_SHADOWS = 445
STEAM_FORK_SAME_PATH_COLLISIONS = 586
STEAM_FORK_SAME_OBJECT_COLLISIONS = 17
STEAM_FORK_COLLISIONS = 586
STEAM_TECH_TREE_COLLISIONS = 2
STEAM_11311_FORWARD_PORTS_ALREADY_PRESENT = 0
STEAM_SAFE_FORWARD_PORT_CANDIDATES = 0
STEAM_SAFE_FORWARD_PORTS = 0
STEAM_MANUAL_RECONCILIATION_REQUIRED = 84
STEAM_MANUAL_RECONCILIATIONS = 84
STEAM_CHANGES_NOT_RELEVANT = 0
UNKNOWN_STEAM_OBJECT_IDS = 0
INVENTED_STEAM_PATHS = 0

CROSS_SOURCE_COLLISIONS = 37

UNKNOWN_TECH_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0

GAMEPLAY_FILES_CHANGED = 0
RUNTIME = NOT_CLAIMED
COMMIT = NO
PUSH = NO

NEXT_PHASE_READY = NO

### 1. 1.13.11_FORWARD_PORT_ACTIONS

- Migrer séparément les neuf familles de lois vers leurs chemins 1.13.11.
- Consolider les événements militaires et les deux scopes optionnels.
- Consolider les événements Society et ajouter .104/.105.
- Porter les deux valeurs Banana 30/40.
- Récupérer la source 1.13.9 ou réconcilier sémantiquement les sept autres shadows changés.

### 2. TREE_CORRECTION_ACTIONS

- Préparer un lot mécanique limité aux 53 lignes exactes.
- Obtenir les 24 décisions humaines avant toute création d’objet.
- Pour les neuf familles renommées, intégrer les lois uniquement dans leurs nouveaux chemins 1.13.11 ; conserver les chemins inchangés comme 00_church_and_state.txt.
- Préserver TECH6A/TECH6B sauf override utilisateur explicite.

### 3. UPSTREAM_RECONCILIATION_ACTIONS

- Aucun forward-port Steam automatique.
- Examiner d’abord les 17 collisions objet.
- Examiner ensuite les 80 divergences actuelles et quatre suppressions retenues.
- Préserver le snapshot 2.3.0.1 ; utiliser un autre dossier pour un miroir futur.
