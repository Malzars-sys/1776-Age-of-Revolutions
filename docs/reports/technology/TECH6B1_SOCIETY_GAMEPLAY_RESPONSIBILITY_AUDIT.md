# TECH6B1 — Society Gameplay Responsibility Audit

> Mise à jour autoritative TECH6B3E : ce rapport décrit l'audit historique TECH6B1, mais ses anciens owners ne doivent plus être lus comme l'état courant. `joint_stock_companies` est désormais visible et recherchable en ère 6. Les gates manuellement figés après TECH6B3D sont : Protectionnisme → `political_economy`; assurance maladie publique → `organized_immunization_campaigns`; athéisme d'État → `socialism`; Terakoya sans gate; partage droits/travail/aide sociale entre `human_rights` et `labor_movement`; progression complète des cinq lois d'esclavage. La matrice associée contient une colonne `post_tech6b3d_authoritative_update`.

## 1. Checkpoint et périmètre

- Branche locale : `tech6b1-society-gameplay-audit`
- Baseline : `ed8351d5daf3fdcf65a67643ff4ef87e95c0231d`
- Vanilla autoritative : `C:/Games/Victoria 3/game`
- Version : Victoria 3 `1.13.9`
- Nature : audit statique uniquement
- Fichiers gameplay modifiés : aucun
- Validation runtime : non revendiquée

Le dépôt utilise `replace_path="common/technology/technologies"`. L'état effectif n'est donc pas une simple superposition de `30_society.txt` vanilla : il résulte de `30_tech3a_society.txt` et de `90_tech3a_vanilla_post1836_compatibility.txt`.

L'univers Society effectif des Eras I–VI contient **41 technologies**. Les 40 nodes de l'index TECH3A sont complétés par `colonization`, survivant vanilla explicitement restauré par TECH2H. Sa présence est intentionnelle et distincte de `systematic_cadastral_surveying`.

## 2. Méthode

L'audit a croisé :

- les définitions Society effectives du mod ;
- `30_society.txt` et, pour les trois sources militaires conceptuellement croisées, `20_military.txt` vanilla 1.13.9 ;
- les décisions de design Society et arbre intégré ;
- la matrice TECH2H ;
- les résultats TECH4C2 disponibles sur les résidus vanilla ;
- les audits et transferts TECH5, sans rouvrir les responsabilités building/PM ;
- les références effectives dans les lois, institutions, mouvements, décisions, journal entries, events, scripted effects, diplomacy, treaty articles, companies et autres objets pertinents.

La matrice contient une ligne par responsabilité ou groupe homogène d'objets partageant la même source, la même destination et la même architecture. Les **65 effets `modifier` vanilla** pertinents sont enregistrés individuellement. Les **5 blocs `on_researched`** pertinents sont enregistrés séparément.

Une référence dans un alias de compatibilité `can_research = no` n'est pas considérée comme fonctionnellement raccordée : le bloc existe physiquement, mais un pays ne peut pas obtenir normalement la responsabilité par recherche.

## 3. État effectif des IDs hérités

### IDs pré-1836 conservés et corrects

Les responsabilités directement présentes sont conservées sur :

| Technologie | Effets directs actuels | Décision |
|---|---|---|
| `stock_exchange` | `state_market_access_price_impact = 0.1` | KEEP, puis compléter les responsabilités MERGE |
| `medical_degrees` | santé institutionnelle `+1` | KEEP |
| `human_rights` | sécurité sociale `+1` | KEEP, puis agréger la part `egalitarianism` |
| `colonization` | affaires coloniales `+2`, infamie `-0.1` | KEEP |
| `postal_savings` | cinq efficacités d'investissement `+0.15`, réserves `+0.2` | KEEP |
| `labor_movement` | SOL/alphabétisation `+1`, sécurité au travail `+3`, agitateur `+1`, variable globale | KEEP |

`international_relations` n'a pas de bonus direct vanilla, mais garde correctement son ensemble diplomatique et ses treaty articles.

### Alias consommés

Les anciens IDs suivants portent encore des effets ou des hooks mais sont non recherchables dans le fichier de compatibilité : `academia`, `empiricism`, `banking`, `central_banking`, `corporate_charters`, `joint_stock_companies`, `international_trade`, `mass_communication`, `central_archives`, `tech_bureaucracy`, `rationalism`, `centralization`, `psychiatry`, `democracy`, `egalitarianism`, `currency_standards`, `pharmaceuticals`, `law_enforcement` et `dialectics`.

Leurs blocs ne doivent ni être copiés intégralement ni rester les détenteurs fonctionnels. La matrice décide chaque effet séparément.

## 4. Redistribution vanilla figée

Les valeurs ci-dessous sont les valeurs **agrégées à écrire une seule fois** dans TECH6B2. Elles proviennent de l'addition mécanique de responsabilités vanilla successives lorsqu'un MERGE les concentre sur un seul node.

| Cible TECH6B2 | Bloc direct final démontré |
|---|---|
| `institutionalized_scientific_exchange` | `country_influence_mult = 0.25`; `country_diplomatic_play_maneuvers_mult = 0.25` |
| `institutionalized_public_credit` | `country_minting_mult = 0.2`; `country_loan_interest_rate_add = -0.04`; `state_max_trade_advantage_from_capacity_add = 0.1` |
| `stock_exchange` | garder `state_market_access_price_impact = 0.1`; ajouter `country_max_companies_add = 2`, `country_free_charters_add = 2`, `state_urbanization_per_level_mult = -0.1` |
| `periodical_print_networks` | `country_authority_mult = 0.1`; `country_voting_power_mult = 0.1` |
| `systematic_administrative_statistics` | `state_tax_capacity_add = 50`; `country_institution_home_affairs_max_investment_add = 1`; `state_incorporation_speed_mult = 0.1` |
| `organized_elementary_schooling` | `country_institution_schools_max_investment_add = 2`; `state_education_access_wealth_add = 0.02` |
| `constitutional_government` | `country_institution_social_security_max_investment_add = 2` |
| `human_rights` | `state_expected_sol_from_literacy = 1`; valeur agrégée `country_institution_social_security_max_investment_add = 2` |
| `central_statistical_offices` | `country_institution_home_affairs_max_investment_add = 1`; bloc `central_archives.on_researched` exact |
| `active_principle_pharmacy` | `country_institution_health_system_max_investment_add = 1`; `state_harvest_condition_disease_outbreak_impact_mult = -0.2` |
| `professional_civil_policing` | `country_institution_police_max_investment_add = 3` |

Cette redistribution n'ajoute aucun modifier inédit. Elle ne duplique aucun bloc vanilla complet.

## 5. A — État actuel correctement hérité

Sont correctement hérités :

- les six blocs directs conservés listés plus haut ;
- le réseau diplomatique de `international_relations` ;
- les hooks actuels de `medical_degrees`, `human_rights`, `colonization`, `stock_exchange` et `labor_movement` qui continuent à tester un ID actif ;
- les responsabilités post-1836 laissées sur `feminism`, `nationalism`, `pan-nationalism`, `quinine`, `mutual_funds`, `anarchism` et `socialism` ;
- les responsabilités militaires laissées sur `modern_nursing`, `electric_telegraph` et `military_statistics`.

`systematic_cadastral_surveying` ne récupère pas les lois, expéditions ou bonus de `colonization` : les deux responsabilités sont distinctes.

## 6. B — Responsabilités perdues par la refonte

Les pertes démontrées sont de deux types :

1. effets directs encore stockés sur un alias `can_research = no` ;
2. objets externes testant ou accordant encore cet alias.

Les familles principales sont :

- éducation/science : `academia`, `empiricism`, `rationalism` ;
- crédit/entreprises : `banking`, `central_banking`, `corporate_charters`, `joint_stock_companies` ;
- commerce : `international_trade` ;
- presse : `mass_communication` ;
- administration/police : `centralization`, `central_archives`, `tech_bureaucracy`, `law_enforcement` ;
- constitution/droits : `democracy`, `egalitarianism` ;
- santé : `pharmaceuticals` ;
- standardisation : `currency_standards`.

Neuf enregistrements sont explicitement classés `STALE_ALIAS_REFERENCE`. Deux références de loi sont classées `WRONG_TECH_TARGET` : `law_censorship` doit relever de `periodical_print_networks`, pas de la responsabilité policière, et la pondération IA de `law_per_capita_based_taxation` doit suivre `scientific_metrology`, propriétaire exact de sa responsabilité `currency_standards` déjà figée par TECH2H.

## 7. C — Future implémentation TECH6B2

Les corrections démontrées nécessitent deux architectures :

- `EXISTING_MOD_FILE` pour compléter `common/technology/technologies/30_tech3a_society.txt` et modifier les fichiers déjà présents dans le mod ;
- `SAME_PATH_SHADOW` pour tout fichier vanilla existant sans homologue mod, au même chemin relatif exact.

Les lots mécaniques sont :

1. écrire les onze blocs agrégés de la section 4 ;
2. déplacer exactement `central_archives.on_researched` vers `central_statistical_offices` ;
3. remplacer les gates de lois et systèmes figés dans TECH2H ;
4. remplacer les gates company de `corporate_charters` et `joint_stock_companies` par `stock_exchange` ;
5. raccorder `movement_anti_slavery` à `abolitionist_mobilization` ;
6. remplacer les références démontrées aux alias consommés dans les décisions, JEs et events listés dans la matrice.

Aucune loi ne doit être automatiquement imposée par la recherche.

## 8. D — Responsabilités TECH5 non rouvertes

Six enregistrements sont fermés comme `ALREADY_HANDLED_BY_TECH5` :

- `building_university` → `institutionalized_scientific_exchange` ;
- `building_government_administration` → `systematic_administrative_statistics` ;
- `pm_horizontal_drawer_cabinets` → `systematic_population_registration` ;
- `pm_vertical_filing_cabinets` → `central_statistical_offices` ;
- `pm_philosophy_department` → `codified_practical_knowledge` ;
- la ligne de couverture `systematic_population_registration`, dont la responsabilité démontrée est déjà fermée par TECH5.

`TECH5_REGRESSION_CANDIDATES = 0`.

## 9. E — Starting technologies différées

Douze groupes de références de `common/scripted_effects/00_starting_inventions.txt` sont enregistrés `DEFER_STARTING_TECH`.

Aucune attribution pays par pays n'a été proposée. Ces références devront être traitées dans la phase dédiée au setup initial.

## 10. F — TECH6C Military/Naval

Huit enregistrements sont différés à TECH6C, notamment :

- `mobilization_option_field_hospitals` / `modern_nursing` ;
- le bonus de pertes d'`electric_telegraph` ;
- le bonus d'organisation et les hooks de `military_statistics` ;
- `law_national_guard`.

Aucune modification militaire, navale, de formation, port, shipyard ou convoy n'est proposée.

## 11. G — Décisions humaines résolues / TECH6B1-R

Les treize anciens enregistrements `UNRESOLVED_REQUIRES_DESIGN_REVIEW` ont reçu une décision finale. `UNRESOLVED = 0`. La résolution reste un gel d'audit : aucun fichier gameplay n'est modifié dans TECH6B1-R.

| Cas | Décision finale | Cible finale | Justification et autorité de design |
|---:|---|---|---|
| 1 | `STRUCTURAL_ONLY` | `variolation_networks` | Aucun objet ou effet vanilla pré-1836 exact n'est démontré ; le node reste un prérequis de `vaccination`. Autorité : design Society, arbre intégré et état effectif. |
| 2 | `STRUCTURAL_ONLY` | `organized_reform_movements` | Aucun hook unique exact n'est démontré ; le node structure les descendants abolitionnistes et ouvriers. Autorité : design Society, arbre intégré et état effectif. |
| 3 | `TRANSFER_REQUIRED` | `systematic_legal_codification` | La responsabilité property/contract/civil-status est concrétisée par la pondération IA de `law_tenant_farmers`. Autorité : design Society, arbre intégré et vanilla 1.13.9. |
| 4 | `STRUCTURAL_ONLY` | `early_socialism_cooperativism` | Aucun effet exact pré-1836 n'est démontré ; le contenu socialiste mûr reste post-1836. Autorité : design Society, arbre intégré et état effectif. |
| 5 | `DEFER_POST1836` | aucune cible pré-1836 | Le `+1` d'investissement scolaire de `dialectics` n'a aucun owner pré-1836 explicitement figé. Autorité : TECH2H, arbre intégré et vanilla 1.13.9. |
| 6 | `DEFER_POST1836` | aucune cible pré-1836 | `psychiatry.country_influence_mult = 0.25` n'a pas de destination médicale ou pré-1836 exacte. Autorité : TECH2H, design Society, arbre intégré et vanilla 1.13.9. |
| 7 | `DEFER_POST1836` | aucune cible pré-1836 | `psychiatry.country_diplomatic_play_maneuvers_mult = 0.25` n'a pas de destination médicale ou pré-1836 exacte. Même autorité que le cas 6. |
| 8 | `DEFER_POST1836` | aucune cible pré-1836 | `psychiatry.state_bureaucracy_population_base_cost_factor_mult = -0.05` pourrait relever de plusieurs domaines, mais aucun transfert n'est figé. Même autorité que le cas 6. |
| 9 | `DEFER_POST1836` | bloc indivisible, aucune cible pré-1836 | `egalitarianism.on_researched` ne gère que l'inscription au `je_springtime_of_the_peoples`; il appartient à la politique de masse ultérieure. Autorité : vanilla 1.13.9 et principes du design Society. |
| 10 | décisions individuelles ci-dessous | cinq cibles exactes | Les cinq références à `human_rights` sont des pondérations IA hétérogènes et non un gate unique duplicable. Autorité : TECH2H, design Society, arbre intégré, vanilla 1.13.9 et état effectif. |
| 11 | `DEFER_POST1836` | aucune cible pré-1836 | Suffrage universel, taxation proportionnelle, Printemps des peuples, radicalisme et événements de 1848 forment une responsabilité de politique de masse mûre. Autorité : design Society, arbre intégré, vanilla et état effectif. |
| 12 | `DEFER_POST1836` | aucune cible pré-1836 | Kerensky, Plekhanov et les événements de progression/suppression de `dialectics` sont du contenu socialiste ultérieur. Même autorité que le cas 11. |
| 13 | `DEFER_POST1836` | aucune cible pré-1836 | Le JE/mouvement positiviste et les événements de psychologie/psychiatrie forment un système post-1836 cohérent. Même autorité que le cas 11. |

### CUSTOM LAWS REMOVED FROM HUMAN_RIGHTS

Les cinq occurrences auditées de `human_rights` se trouvent dans `ai_enact_weight_modifier`. Elles influencent la maturité de l'IA pour l'adoption de la loi ; elles ne sont pas les `unlocking_technologies` de ces lois. TECH6B2 doit remplacer uniquement cette référence précise et préserver toutes les autres alternatives du bloc.

| Loi | Ancienne référence | Décision finale | Cible | Justification | Autorité / architecture |
|---|---|---|---|---|---|
| `law_interventionism` | pondération IA : `human_rights` | `TRANSFER_REQUIRED` | `classical_political_economy` | Le node possède le marché, l'investissement et la pondération des lois économiques. Le vrai unlock `manufacturies`, déjà retargeté vers `interchangeable_manufacture` par TECH2H, ne change pas. | Design Society + arbre intégré + TECH2H + vanilla ; `SAME_PATH_SHADOW` de `common/laws/00_economic_system.txt`. |
| `law_agrarianism` | pondération IA : `human_rights` | `TRANSFER_REQUIRED` | `political_economy` | Le node possède agriculture, richesse publique et pondération des lois économiques. Le vrai unlock `romanticism` et l'alternative `pan-nationalism` restent inchangés. | Design Society + arbre intégré + TECH2H + vanilla ; `SAME_PATH_SHADOW` du même fichier. |
| `law_merchant_banking` | pondération IA : `human_rights` | `TRANSFER_REQUIRED` | `institutionalized_public_credit` | Le node possède les intermédiaires financiers et les hooks bancaires. La loi n'a aucune technologie de déverrouillage. | Design Society + arbre intégré + état effectif ; `EXISTING_MOD_FILE` dans `common/laws/00_inject_laws.txt`. |
| `law_tenant_farmers` | pondération IA : `human_rights` | `TRANSFER_REQUIRED` | `systematic_legal_codification` | Le régime de tenure est une responsabilité de propriété, contrat et statut juridique, non de relevé cadastral. La loi n'a aucun bloc de déverrouillage technologique. | Design Society + arbre intégré + vanilla ; `SAME_PATH_SHADOW` de `common/laws/00_land_reform.txt`. |
| `law_per_capita_based_taxation` | pondération IA : `human_rights` | `WRONG_TECH_TARGET` | `scientific_metrology` | TECH2H attribue déjà exactement sa responsabilité `currency_standards` à cette cible ; la pondération IA doit suivre le même owner. Le vrai unlock reste le transfert TECH2H existant. | TECH2H + arbre intégré + vanilla ; `SAME_PATH_SHADOW` de `common/laws/00_taxation.txt`. |

Les alternatives `civilizing_mission` et `pan-nationalism` présentes dans les pondérations IA sont conservées. Aucune loi n'est accordée automatiquement par une recherche.

### DEFERRED POST-1836 RESPONSIBILITIES

Les décisions post-1836 ajoutées par TECH6B1-R sont :

- le modifier scolaire de `dialectics` ;
- les trois modifiers de `psychiatry` ;
- le bloc indivisible `egalitarianism.on_researched` ;
- le groupe politique de masse `egalitarianism` ;
- le groupe historique et événementiel de `dialectics` ;
- le groupe JE/mouvement/events de psychiatrie et positivisme.

Ces responsabilités restent sur leurs propriétaires de compatibilité post-1836. Elles n'ont aucune cible TECH6B2 et ne doivent pas être copiées vers `early_socialism_cooperativism`, `medical_degrees` ou `human_rights`.

## 12. Technologies sans bonus artificiel

Dix-sept lignes de couverture sont `STRUCTURAL_ONLY`. Cela n'interdit pas un hook futur démontré, mais interdit d'inventer un bonus pour remplir le node.

Sont concernés : `political_economy`, `specialized_technical_academies`, `veterinary_science`, `variolation_networks`, `classical_political_economy`, `systematic_cadastral_surveying`, `vaccination`, `polytechnical_education`, `organized_immunization_campaigns`, `organized_reform_movements`, `mechanized_printing`, `experimental_research_laboratories`, `specialized_professional_societies`, `clinicopathological_medicine`, `mass_circulation_press`, `liberal_constitutionalism` et `early_socialism_cooperativism`.

## 13. Validations statiques

Les compteurs de la matrice finale sont :

```text
SOCIETY_TECHS_AUDITED = 41
EXTERNAL_GAMEPLAY_RESPONSIBILITIES_FOUND = 68
KEEP_CURRENT = 27
TRANSFER_REQUIRED = 82
NEW_HOOK_REQUIRED = 1
STALE_ALIAS_REFERENCES = 9
ALREADY_HANDLED_BY_TECH5 = 6
TECH5_REGRESSION_CANDIDATES = 0
DEFERRED = 47
UNRESOLVED = 0
WRONG_TECH_TARGET = 2

VANILLA_MODIFIER_EFFECTS_AUDITED = 65
ON_RESEARCHED_BLOCKS_AUDITED = 5

UNKNOWN_TECH_IDS = 0
INVENTED_OBJECT_IDS = 0
INVENTED_FILE_PATHS = 0
```

`EXTERNAL_GAMEPLAY_RESPONSIBILITIES_FOUND` compte les lignes de responsabilité externes homogènes ; une ligne peut contenir plusieurs IDs exacts partageant la même destination et architecture.

## 14. TECH6B2_IMPLEMENTATION_CANDIDATES

Uniquement les changements mécaniquement démontrés :

1. appliquer les onze agrégats de modificateurs de la section 4 dans `common/technology/technologies/30_tech3a_society.txt` ;
2. transférer exactement `central_archives.on_researched` vers `central_statistical_offices` ;
3. appliquer les lignes `TRANSFER_REQUIRED`, `NEW_HOOK_REQUIRED`, `STALE_ALIAS_REFERENCE` et `WRONG_TECH_TARGET` de la matrice, seulement lorsque `expected_target_tech` est un ID exact non vide, y compris les cinq retargetings individuels de pondération IA de la section 11 ;
4. utiliser `SAME_PATH_SHADOW` ou `EXISTING_MOD_FILE` exactement comme enregistré ;
5. exclure toutes les lignes `DEFER_*`, `ALREADY_HANDLED_BY_TECH5` et `STRUCTURAL_ONLY` ; aucune ligne non résolue ne subsiste.

TECH6B1 n'implémente aucun de ces changements.
