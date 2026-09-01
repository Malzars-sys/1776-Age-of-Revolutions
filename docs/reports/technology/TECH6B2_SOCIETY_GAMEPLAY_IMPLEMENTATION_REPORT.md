# TECH6B2 — Society Gameplay Implementation Report

> Addendum TECH6B3E : plusieurs affectations TECH6B2 ont été ensuite remplacées par une revue humaine runtime. `law_protectionism` relève maintenant de `political_economy`; `law_public_health_insurance` de `organized_immunization_campaigns`; `law_state_atheism` de `socialism`; `law_terakoya` est sans gate. `human_rights` possède `law_restricted_child_labor`, `law_regulatory_bodies` et `law_wage_subsidies`; `labor_movement` possède `law_compulsory_primary_school`, `law_worker_protections` et `law_old_age_pension`. La progression esclavagiste autoritative est consignée dans TECH6B3E. `joint_stock_companies` n'est plus un alias caché.

## A. Checkpoint Git

- Branche : `tech6b2-society-gameplay-implementation`
- Baseline : `ed8351d5daf3fdcf65a67643ff4ef87e95c0231d`
- Branche source : `tech6b1-society-gameplay-audit`
- Vanilla autoritative : Victoria 3 `1.13.9`, `C:/Games/Victoria 3/game`
- Matrice canonique : `TECH6B1_SOCIETY_GAMEPLAY_RESPONSIBILITY_MATRIX.csv`
- `UNRESOLVED = 0`
- Commit : aucun
- Push : aucun
- Runtime : non revendiqué, test utilisateur requis

Les deux livrables TECH6B1 non suivis ont été conservés tels quels lors de la création de la branche. TECH6B2 ajoute ce rapport et modifie uniquement les responsabilités actionnables figées par TECH6B1/TECH6B1-R.

## B. Fichiers gameplay modifiés

`GAMEPLAY_FILES_CHANGED = 50`, dont 34 shadows vanilla créés au même chemin relatif exact et 16 fichiers mod existants modifiés.

### Technologies

- `common/technology/technologies/30_tech3a_society.txt`
- `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt`

### Lois

- `common/laws/00_church_and_state.txt`
- `common/laws/00_distribution_of_power.txt`
- `common/laws/00_economic_system.txt`
- `common/laws/00_education_system.txt`
- `common/laws/00_free_speech.txt`
- `common/laws/00_governance_principles.txt`
- `common/laws/00_health_system.txt`
- `common/laws/00_inject_laws.txt`
- `common/laws/00_internal_security.txt`
- `common/laws/00_land_reform.txt`
- `common/laws/00_policing.txt`
- `common/laws/00_taxation.txt`
- `common/laws/00_trade_policy.txt`
- `common/laws/00_welfare.txt`

### Compagnies

- `common/company_types/00_companies_africa.txt`
- `common/company_types/00_companies_asia.txt`
- `common/company_types/00_companies_france.txt`
- `common/company_types/00_companies_ip3.txt`
- `common/company_types/00_companies_russia.txt`
- `common/company_types/00_companies_soi.txt`

### Journal entries et événements

- `common/journal_entries/00_art_jes.txt`
- `common/journal_entries/00_ethiopia.txt`
- `common/journal_entries/00_liberalism.txt`
- `common/journal_entries/00_peoples_springtime_je.txt`
- `common/journal_entries/05_technocracy.txt`
- `events/agitators_events/agitator_law_events_2.txt`
- `events/belle_epoque_events.txt`
- `events/cholera.txt`
- `events/french_revolution_mod_events.txt`
- `events/ig_petitions.txt`
- `events/ig_suppression_events.txt`
- `events/japan_events/ep2_shogunate_events.txt`
- `events/soi_events/00_lobbies_events_03.txt`
- `events/vampire_panic_events.txt`

### Autres responsabilités externes

- `common/character_traits/condition_traits.txt`
- `common/decisions/goa_macao_decisions.txt`
- `common/decrees/00_decree.txt`
- `common/diplomatic_actions/13_embargo.txt`
- `common/diplomatic_actions/30_fund_lobby.txt`
- `common/parties/liberal_party.txt`
- `common/political_movements/00_ideological_movements.txt`
- `common/treaty_articles/04_take_on_debt.txt`
- `common/treaty_articles/05_transfer_money.txt`
- `common/treaty_articles/13_goods_transfer.txt`
- `common/treaty_articles/17_prohibit_trade_with_global_market.txt`
- `common/treaty_articles/18_acquire_monopoly_for_company.txt`
- `common/treaty_articles/21_no_tariffs.txt`
- `common/treaty_articles/26_no_subventions.txt`

## C. Onze agrégats de modifiers implémentés

| Technologie | Bloc final |
|---|---|
| `institutionalized_scientific_exchange` | `country_influence_mult = 0.25`; `country_diplomatic_play_maneuvers_mult = 0.25` |
| `institutionalized_public_credit` | `country_minting_mult = 0.2`; `country_loan_interest_rate_add = -0.04`; `state_max_trade_advantage_from_capacity_add = 0.1` |
| `stock_exchange` | `state_market_access_price_impact = 0.1`; `country_max_companies_add = 2`; `country_free_charters_add = 2`; `state_urbanization_per_level_mult = -0.1` |
| `periodical_print_networks` | `country_authority_mult = 0.1`; `country_voting_power_mult = 0.1` |
| `systematic_administrative_statistics` | `state_tax_capacity_add = 50`; `country_institution_home_affairs_max_investment_add = 1`; `state_incorporation_speed_mult = 0.1` |
| `organized_elementary_schooling` | `country_institution_schools_max_investment_add = 2`; `state_education_access_wealth_add = 0.02` |
| `constitutional_government` | `country_institution_social_security_max_investment_add = 2` |
| `human_rights` | `state_expected_sol_from_literacy = 1`; `country_institution_social_security_max_investment_add = 2` |
| `central_statistical_offices` | `country_institution_home_affairs_max_investment_add = 1` |
| `active_principle_pharmacy` | `country_institution_health_system_max_investment_add = 1`; `state_harvest_condition_disease_outbreak_impact_mult = -0.2` |
| `professional_civil_policing` | `country_institution_police_max_investment_add = 3` |

Les 32 lignes `modifier` transférées sont consolidées dans ces onze blocs. Leurs quinze blocs sources intégralement transférés ont été retirés des aliases non recherchables `academia`, `banking`, `central_archives`, `central_banking`, `centralization`, `corporate_charters`, `democracy`, `egalitarianism`, `empiricism`, `joint_stock_companies`, `law_enforcement`, `mass_communication`, `pharmaceuticals`, `rationalism` et `tech_bureaucracy`. Les modifiers différés de `dialectics`, `psychiatry`, `nationalism`, `feminism`, `socialism`, `pan-nationalism`, `mutual_funds`, `electric_telegraph` et `military_statistics` sont inchangés.

## D. Transfert central_archives.on_researched

Le bloc vanilla 1.13.9 a été transféré, sans découpage ni changement de condition, vers `central_statistical_offices.on_researched`. La comparaison normalisée du bloc source vanilla et du bloc destination est exacte. `central_archives` ne contient plus de `on_researched` dans le fichier de compatibilité.

## E. Lois et pondérations IA retargetées

Les transferts légaux de la matrice sont appliqués, notamment :

- écoles religieuses, privées et publiques → `organized_elementary_schooling` ; `law_terakoya` → `institutionalized_scientific_exchange` ;
- séparation totale et athéisme d'État → `institutionalized_scientific_exchange` ; liberté de conscience → `codified_practical_knowledge` ;
- technocratie → `central_statistical_offices` ; secret police et lois policières auditées → `professional_civil_policing` ;
- laissez-faire, mercantilisme, libre-échange et navigation acts → `commercial_insurance_markets` ;
- landed/wealth/census voting, républiques présidentielle/parlementaire et poor laws → `constitutional_government` ;
- assurances maladie privées/publiques → `active_principle_pharmacy` ;
- `law_censorship` → `periodical_print_networks` ;
- unlock principal de `law_per_capita_based_taxation` : `currency_standards` → `scientific_metrology`.

Les cinq pondérations IA auparavant attachées à `human_rights` ont été modifiées individuellement :

| Loi | Nouvelle référence IA |
|---|---|
| `law_interventionism` | `classical_political_economy` |
| `law_agrarianism` | `political_economy` |
| `law_merchant_banking` | `institutionalized_public_credit` |
| `law_tenant_farmers` | `systematic_legal_codification` |
| `law_per_capita_based_taxation` | `scientific_metrology` |

Les autres conditions, notamment `civilizing_mission` et `pan-nationalism`, sont conservées. Aucun effet `set_law` n'a été ajouté et aucune technologie n'impose automatiquement une loi.

## F. Mouvements, JEs, événements et décisions corrigés

- `movement_anti_slavery` teste désormais `abolitionist_mobilization`, sans abolir automatiquement l'esclavage.
- `je_liberalism_1`, `je_springtime_of_the_peoples`, `je_age_of_princes`, `je_technocracy` et `je_romanticism` utilisent les cibles exactes de la matrice.
- Les événements audités de presse, suppression d'IG, Révolution française, choléra, Belle Époque, lobbies, Shogunate et vampire panic ont été retargetés.
- `macao_decision`, les décrets de voirie/secours, `fund_lobbies`, `embargo`, `liberal_party` et le trait `cocaine_addiction` ont été corrigés.
- Les treaty articles de dette, transfert d'argent, commerce mondial, tarifs, subventions et monopole de compagnie utilisent les nouvelles responsabilités exactes.

## G. Company gates corrigés

Les gates de neuf objets de compagnie, répartis sur six fichiers, ont été retargetés vers `stock_exchange` : `company_misr`, `company_egyptian_rail`, `company_nam_dinh`, `company_imperial_tobacco`, `company_san_miguel`, `company_united_tobacco_factories`, `company_guinness`, `company_cgv` et `company_savva_morozov`. Plusieurs objets contiennent la même condition dans plus d'un sous-bloc ; toutes les occurrences internes auditées ont été corrigées. Aucun bonus, prestige good ou objet TECH6A n'a été modifié.

## H. Aliases consommés corrigés

Les neuf lignes `STALE_ALIAS_REFERENCE` et les deux lignes `WRONG_TECH_TARGET` actionnables ne laissent aucun ancien propriétaire dans leurs objets cibles. L'audit ciblé valide 45 lignes externes et 77 associations ligne/objet, représentant 75 IDs d'objet uniques.

Les occurrences résiduelles d'aliases ne sont pas automatiquement des erreurs. Recherche effectuée dans `common/` et `events/`, commentaires exclus :

| Classification | Occurrences | Traitement |
|---|---:|---|
| `EXPECTED_POST1836_COMPATIBILITY` | 53 | Conservées : responsabilités différées ou hooks de compatibilité non actionnables dans TECH6B2. |
| `DEFER_STARTING_TECH` | 77 | Conservées dans les historiques/setup initiaux ; aucune attribution initiale modifiée. |
| `DEFER_TECH6C` | 1 | `law_national_guard` conserve `law_enforcement`. |
| `INTENTIONAL_ALIAS_DEFINITION` | 54 | Définitions/prérequis internes du fichier de compatibilité conservés. |
| `UNEXPECTED_RESIDUAL` | 0 | Aucun résidu applicable aux objets TECH6B2. |

## I. Responsabilités volontairement non implémentées

- Tous les statuts `DEFER_POST1836`, notamment les modifiers de `dialectics` et `psychiatry`, `egalitarianism.on_researched`, le contenu politique de masse/1848, les hooks tardifs de dialectique et le système psychiatrie/positivisme.
- Tous les statuts `DEFER_STARTING_TECH`.
- Tous les statuts `DEFER_TECH6C`, notamment `law_national_guard`, `modern_nursing`, `electric_telegraph` et `military_statistics`.
- Toutes les lignes `STRUCTURAL_ONLY`, sans création de bonus artificiel.
- Toutes les lignes `ALREADY_HANDLED_BY_TECH5`, sans réouverture des buildings ou PMs.

## J. Validation statique

```text
MATRIX_ROWS = 191
TRANSFER_REQUIRED_MATRIX_ROWS = 82
TRANSFER_REQUIRED_COVERAGE_ROWS = 16
TRANSFER_REQUIRED_ACTIONABLE_ROWS = 66
TRANSFER_REQUIRED_ACTIONABLE_IMPLEMENTED = 66
TRANSFER_REQUIRED_ACTIONABLE_BREAKDOWN = 32 modifier responsibilities + 1 on_researched + 33 external rows
NEW_HOOK_REQUIRED = 1/1
STALE_ALIAS_REFERENCE = 9/9
WRONG_TECH_TARGET = 2/2

ACTIONABLE_MATRIX_ROWS_INCLUDING_COVERAGE = 94
PHYSICAL_RESPONSIBILITY_ROWS = 78
UNIQUE_ACTIONABLE_TARGET_PATHS = 49
ALIAS_HOLDER_CLEANUP_PATHS = 1
GAMEPLAY_FILES_CHANGED = 50
SAME_PATH_SHADOWS_CREATED = 34
EXISTING_MOD_FILES_CHANGED = 16

MODIFIER_AGGREGATES = 11/11
MODIFIER_VALUES_CHECKED = 23
MODIFIER_AGGREGATE_ERRORS = 0
ON_RESEARCHED_EXACT_MATCH = YES
EXTERNAL_ACTION_ROWS = 45/45
EXTERNAL_OBJECT_ASSOCIATIONS_VALIDATED = 77
EXTERNAL_VALIDATION_ERRORS = 0
MISSING_OBJECT_IDS = 0
DUPLICATE_OBJECT_IDS_CREATED = 0
UNKNOWN_TECH_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0
SHADOWS_WITHOUT_SAME_PATH_VANILLA = 0
STATIC_SCRIPT_ERRORS = 0

POST1836_RESPONSIBILITIES_TOUCHED = 0
STARTING_TECH_FILES_TOUCHED = 0
TECH5_RESPONSIBILITIES_REOPENED = 0
TECH6C_RESPONSIBILITIES_IMPLEMENTED = 0
RUNTIME = USER_REQUIRED
```

Les 50 fichiers gameplay modifiés ont été vérifiés pour l'équilibre des accolades, les guillemets non fermés et les profondeurs négatives. `git diff --check` ne signale aucune erreur. Les 34 nouveaux shadows possèdent tous une source vanilla au même chemin relatif exact. Les 49 chemins d'action canoniques sont modifiés et aucun chemin gameplay supplémentaire n'apparaît, hors nettoyage requis du détenteur alias dans `90_tech3a_vanilla_post1836_compatibility.txt`.

## K. Checklist runtime utilisateur

1. Démarrer une nouvelle partie en 1776.
2. Vérifier les tooltips des technologies Society modifiées.
3. Vérifier les niveaux maximum des institutions education, health, police, home affairs et social security.
4. Vérifier les modifiers de `stock_exchange`, `institutionalized_public_credit`, `systematic_administrative_statistics`, `organized_elementary_schooling`, `human_rights` et `professional_civil_policing`.
5. Vérifier que les lois attendues apparaissent avec les technologies correctes, sans adoption automatique.
6. Vérifier que les cinq pondérations IA de loi ne produisent aucune erreur de script.
7. Vérifier l'apparition et les conditions de `movement_anti_slavery` après `abolitionist_mobilization`.
8. Vérifier les JEs, événements et décisions retargetés.
9. Vérifier les company gates utilisant `stock_exchange`.
10. Vérifier qu'aucun contenu 1848, psychiatrie ou dialectique post-1836 ne s'active prématurément.
11. Inspecter `error.log` pour `unknown technology`, `invalid trigger`, `invalid modifier`, `duplicate object`, `scripted effect error`, `law error`, `institution error` et `event error`.

La validation runtime n'est pas revendiquée par TECH6B2.
