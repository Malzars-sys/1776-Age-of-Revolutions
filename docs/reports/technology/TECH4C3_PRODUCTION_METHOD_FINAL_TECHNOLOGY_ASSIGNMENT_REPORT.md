# TECH4C3 — Production Methods Final Technology Assignment

## 1. Checkpoint et périmètre

- Dépôt : `Malzars-sys/1776-Age-of-Revolutions`
- Branche : `tech4c2-audit-snapshot`
- État de départ : `62346303b5e51541056f70dede11bbbb1718291b`
- Référence vanilla autoritative : installation Victoria 3 1.13.9 sous `C:\Games\Victoria 3\game`
- Périmètre gameplay : uniquement les champs `unlocking_technologies` des production methods vanilla
- PMG, bâtiments, IDs et contenu économique des PM : inchangés

Le fichier demandé `VANILLA_TECHNOLOGY_PRODUCTION_AUDIT.md` n'existe ni dans le checkout, ni dans les refs Git locales, ni sous les deux emplacements plausibles de la branche distante. L'audit ne prétend donc pas l'avoir lu. Les sources internes disponibles qui couvrent son rôle ont été utilisées :

- `TECH4C2_PRE1836_VANILLA_RESIDUAL_AUDIT.csv` ;
- `TECH5A_PRODUCTION_METHOD_TECH_GATE_AUDIT.csv` ;
- `TECH5A_HIDDEN_ALIAS_BUILDING_PM_RESPONSIBILITY_MATRIX.csv` ;
- `TECH5A_PM_PROGRESSION_AUDIT.csv` ;
- `TECH2H_VANILLA_SPLIT_UNLOCK_MATRIX.csv` ;
- `TECH1A_VANILLA_OVERLAP_MATRIX.csv` ;
- `TECH5B2_CURRENT_TARGETED_PM_PROGRESSION_AUDIT.csv`.

## 2. Méthode

L'inventaire vanilla complet a été comparé à l'état effectif du mod. Pour chaque ID PM vanilla, le fichier effectif a été résolu selon la priorité VFS, puis le champ `unlocking_technologies` a été extrait et contrôlé contre l'univers technologique effectif fourni par le `replace_path` du mod.

Les PM prioritaires sont ceux qui utilisaient encore une technologie définie avec `can_research = no`, puis ceux signalés par les anciens audits de progression. Chaque cas modifié a été remonté par la chaîne bâtiment → PMG → PM → technologie. Les transitions PMG ont aussi été contrôlées pour les inversions d'ère et les relations d'ancêtre technologique.

## 3. Résultat global

| Contrôle | Résultat |
|---|---:|
| IDs PM vanilla examinés | 433 |
| IDs PM vanilla résolus dans l'état effectif | 433 |
| PM vanilla avec au moins une gate technologique | 210 |
| PM vanilla sans gate technologique | 223 |
| Références vers un ID technologique inconnu après correction | 0 |
| Références vers une technologie non recherchable après correction | 0 |
| PM supprimés ou renommés | 0 |
| PM nouveaux créés | 0 |
| Transitions adjacentes PMG avec gate aval examinées | 247 |
| Inversions d'ère détectées parmi les transitions restantes | 0 |

## 4. PM corrigés

| Bâtiment | PMG | PM | Gate avant | Gate finale | Décision historique et fonctionnelle |
|---|---|---|---|---|---|
| `building_university` | `pmg_base_building_university` | `pm_philosophy_department` | `dialectics` (alias non recherchable) | `codified_practical_knowledge` (Société, ère III) | Le PM fournit innovation et qualifications. Les savoirs pratiques codifiés et encyclopédiques représentent mieux l'institution universitaire des Lumières que l'équivalence idéologique générale `dialectics` → socialismes précoces. |
| `building_trade_center` | `pmg_trade_quantity_trade_center` | `pm_trade_center_trade_quantity_high` | `hydraulic_cranes` (alias non recherchable) | `mechanized_naval_dockyards` (Naval, ère V) | L'audit historique classe cette correspondance comme forte : mécanisation des arsenaux, grues et logistique portuaire soutiennent l'augmentation du débit commercial. |
| `building_shipyard` | `pmg_base_building_shipyard` | `pm_complex_shipbuilding` | `screw_frigate` (alias non recherchable) | `paddle_steamer` (Naval, ère V) | Le PM consomme des moteurs tout en restant une construction navale en bois renforcée. Le bateau à roues à aubes est le prédécesseur actif direct de la propulsion à hélice et reste en aval de l'architecture navale scientifique. |
| Aucun consommateur bâtiment résolu dans la vanilla 1.13.9 | `pmg_military_base` | `pm_military_shipbuilding_wooden_2` | `screw_frigate` (alias non recherchable) | `paddle_steamer` (Naval, ère V) | Même famille de construction navale en bois motorisée. Le PMG orphelin est conservé sans modification pour compatibilité externe ; seule sa gate morte est réparée. |
| `building_urban_center` | `pmg_amenities` | `pm_market_squares` | `urban_planning` (alias non recherchable) | `professional_civil_engineering` (Production, ère V) | Les places de marché aménagées relèvent directement du génie civil et des réseaux urbains. L'audit d'overlap retient déjà cette correspondance croisée. |
| `building_construction_sector` | `pmg_base_building_construction_sector` | `pm_iron_frame_buildings` | `urban_planning` (alias non recherchable) | `professional_civil_engineering` (Production, ère V) | L'application de structures en fer à la construction est cohérente avec la professionnalisation du génie civil, en amont des méthodes à ossature d'acier postérieures. |

## 5. Cas prioritaires vérifiés sans nouveau changement

Les anciens cas `lathe`, `manufacturies`, `intensive_agriculture`, `central_archives`, `centralization`, `artillery` et `power_of_the_purse` ont déjà une destination active dans l'état de départ. Ils ont été revérifiés et conservés.

La progression papier ouverte dans TECH5B2 est déjà corrigée à l'état courant :

`pm_pulp_pressing` → `pm_sulfite_pulping (continuous_papermaking)` → `pm_bleached_paper (industrial_paper_bleaching)`.

Les transitions sans relation d'ancêtre technologique restantes ne comportent aucune inversion d'ère. Elles correspondent à des substitutions de matériau ou de procédé, à des applications indépendantes, ou à des familles post-1836 distinctes. Exemples conservés : verre → plastiques, vapeur → diesel, bois → métal → soudure dans les chantiers navals, tramways → véhicules à moteur, réalisme → photographie et stockage frigorifique → rail frigorifique.

Neuf transitions de cette classe impliquent l'électricité. Elles ont été laissées strictement inchangées, conformément au gel des PM électriques déjà validés. Aucun `unlocking_technologies` électrique ne diffère de la vanilla à cause de TECH4C3.

## 6. Fichiers gameplay

Fichiers déjà présents, modifiés uniquement dans la gate des trois PM concernés :

- `common/production_methods/01_industry.txt` ;
- `common/production_methods/07_government.txt`.

Fichiers vanilla 1.13.9 transférés à chemin identique pour permettre une surcharge VFS atomique :

- `common/production_methods/06_urban_center.txt` ;
- `common/production_methods/11_private_infrastructure.txt` ;
- `common/production_methods/13_construction.txt`.

Pour chacun des trois fichiers transférés, la parité textuelle avec la source vanilla est exacte après application de l'unique substitution de gate autorisée. Aucun fichier de bâtiment ou de PMG n'est modifié.

## 7. Validation statique

- `VANILLA_PM_ID_PRESERVATION = PASS (433/433)`
- `UNKNOWN_PM_TECH_GATE = PASS (0)`
- `UNRESEARCHABLE_PM_TECH_GATE = PASS (0)`
- `ELECTRICAL_PM_FREEZE = PASS`
- `TRANSFERRED_FILE_SEMANTIC_PARITY = PASS`
- `GIT_DIFF_CHECK = PASS`
- `RUNTIME_VALIDATION = NOT_RUN`

`TECH4C3_PRODUCTION_METHOD_FINAL_TECHNOLOGY_ASSIGNMENT = STATIC_PASS`
