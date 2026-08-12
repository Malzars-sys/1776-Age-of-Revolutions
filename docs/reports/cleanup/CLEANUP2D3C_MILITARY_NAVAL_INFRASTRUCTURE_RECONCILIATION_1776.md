# CLEANUP-2D-3C — Réconciliation de l'infrastructure militaire et navale (1776)

## 1. Baseline Git

Baseline relevée avant 3C :

```text
BRANCH = cleanup-post-release
HEAD = 07d45b0eef59382231f7c176c55de410a423ac95
INDEX_STATE = CLEAN
WORKTREE_STATE = DIRTY_PREEXISTING_PRESERVED
```

Le HEAD a avancé depuis l'exécution 3B et contient ses livrables. Les écarts préexistants visibles avant 3C — rapport 2B3 modifié, rapport CLEANUP1D non suivi, deux fichiers hotfix non suivis et sept fichiers technologiques protégés — ont été conservés sans nettoyage. Aucune mutation Git n'a été effectuée.

## 2. Entrées

Les onze entrées obligatoires 2D0, 2D2, 3A et 3B ont été relues. Les formations réellement présentes après 3B sont l'autorité : 2 557 unités terrestres et 239 300 marins. Le CSV de résultat 3B identifie neuf tags avec formations terrestres gelées et trois tags avec flottes gelées.

La baseline canonique utilisée pour le Gate A est exclusivement `C:\Games\Victoria 3`, version 1.13.9. Aucun élément 1.13.10 n'a été consulté.

## 3. Modèle de matérialisation des casernes

Le moteur dispose de deux voies de création cumulatives :

1. un `combat_unit` régulier créé dans une formation matérialise son niveau de recrutement dans l'État indiqué par `state_region` ;
2. un `building_barrack` écrit explicitement dans l'historique ajoute une capacité de recrutement distincte.

Le premier mécanisme ne nécessite pas qu'un bloc `building_barrack` duplique l'unité dans `history/buildings`, à condition que l'État de recrutement appartienne directement au pays. Un niveau explicite ajouté au même pays/État est additionnel ; il ne représente pas le niveau déjà matérialisé par la formation.

```text
LAND_INFRA_MATERIALIZATION_MODEL = FORMATION_AUTOMATERIALIZATION_PLUS_ADDITIVE_EXPLICIT_BUILDING_HISTORY
FORMATION_UNIT_AUTOCREATES_OR_REQUIRES_BARRACKS = OTHER (AUTOMATERIALIZES; NO EXPLICIT HISTORY BLOCK REQUIRED)
EXPLICIT_BARRACKS_AND_FORMATION_UNITS_STACK = YES
CONFIDENCE = HIGH
```

## 4. Preuves vanilla 1.13.9

L'audit intégral des fichiers vanilla trouve 3 276 unités régulières de formation dans 388 couples pays–État et 1 058 niveaux explicites de caserne dans 167 autres couples. Le chevauchement est exactement nul, même au niveau pays : aucune des 138 puissances dotées d'une formation régulière n'utilise en parallèle les casernes explicites, et les 128 pays à casernes explicites n'ont pas de formation scriptée.

Les exemples les plus probants sont GBR 121 unités / 0 caserne explicite, FRA 187/0, PRU 128/0, CHI 485/0 et BIC 208/0. À l'inverse, SWI possède dix casernes explicites et aucune formation historique.

Le bâtiment canonique `building_barrack` déclare `recruits_combat_units = yes` et l'alias `building_barracks`. `NMilitary.COMBAT_UNITS_PER_LEVEL = 1` fixe une unité par niveau. Le runtime 3A confirme enfin que les 121 unités GBR se matérialisaient malgré zéro caserne explicitement écrite. L'ensemble exclut le modèle « ajouter une copie explicite pour chaque unité de formation ».

## 5. État des casernes avant 3C

```text
EXPLICIT_BARRACK_LEVELS_BEFORE = 894
NONSTRUCTURAL_EXPLICIT_BARRACKS_BEFORE = 723
STRUCTURAL_DISPOSITION_EXPLICIT_BARRACKS_BEFORE = 171
FORMATION_SCRIPTED_LAND_UNITS_3B = 2557
FORMATION_MATERIALIZED_LEVELS_BEFORE = 2551
EFFECTIVE_BARRACK_CAPACITY_BEFORE = 3445
```

Les 723 niveaux non structurels constituaient soit un doublon direct avec une formation 3B, soit une capacité permanente pré-3B sans formation cible. Ils ne sont pas une réserve de mobilisation autorisée : cette couche appartient à 3D.

Les 171 niveaux structurels appartiennent à DAI 55, IQU 1, NBS 2, NVS 3, ONT 5, ORA 2, PHL 1, QUE 5, SC1 8, SC3 15, SOK 70, TRN 3 et WTU 1.

## 6. Méthode terrestre retenue

Pour chaque tag non structurel, les niveaux explicites `building_barrack` ont été supprimés : les unités permanentes 3B matérialisent déjà exactement leur capacité dans leur État de recrutement. Les niveaux explicites sans formation ont également été retirés comme capacité permanente obsolète ; aucune capacité de milice ou de levée n'a été convertie en caserne.

Les 34 dispositions structurelles conservent intégralement leurs 171 niveaux explicites. Aucun centre de conscription n'a été créé ou modifié.

Les 304 lignes du résultat état par état distinguent `FORMATION_MATERIALIZATION_ONLY`, `REMOVE_DUPLICATE_WITH_FORMATION_MATERIALIZATION`, `REMOVE_STALE_PRE_3B_CAPACITY` et `STRUCTURAL_DEFER_PRESERVE`.

## 7. Infrastructure terrestre après 3C

```text
EXPLICIT_BARRACK_LEVELS_AFTER = 171
FORMATION_MATERIALIZED_BARRACKS_AFTER = 2551
EFFECTIVE_BARRACK_CAPACITY_AFTER = 2722

NONDEFERRED_LAND_UNITS_3B = 2431
STRUCTURAL_DEFER_FROZEN_LAND_UNITS = 126
TOTAL_SCRIPTED_LAND_UNITS = 2557

NONDEFERRED_LAND_CAPACITY_SHORTFALLS_AFTER = 0
STRUCTURAL_DEFER_LAND_SHORTFALL_COUNTRIES = 2
STRUCTURAL_DEFER_LAND_SHORTFALLS = 6
```

La capacité effective se décompose en 2 431 niveaux matérialisés pour les formations numériques, 120 niveaux valides sur les 126 unités gelées et 171 niveaux explicites structurels préservés. Les cinq unités SIC recrutées depuis Sicily possédée par GR3 et l'unité UBD recrutée depuis Courland possédée par PLC restent six risques structurels sans capacité directement possédée. Ces 171 niveaux ne sont pas présentés comme une validation historique des forces structurelles.

## 8. Capacité navale avant 3C

L'historique comportait 159 niveaux de `building_naval_administration` : 156 non différés et trois SIC différés. Plusieurs puissances étaient fortement déficitaires : GBR 33 niveaux pour 83 400 marins, FRA 24 pour 27 400, RUS 0 pour 21 400, SWE 10 pour 15 800, USA 0 pour 2 500 et CHI 0 pour 4 000.

Les administrations existantes des flottes non différées étaient toutes situées dans des États directement possédés et côtiers. Aucun pays sans flotte ne possédait de capacité navale explicite à retirer.

## 9. Méthode de calcul naval

Pour chaque pays non différé :

```text
crew = frigates × 500 + ships_of_the_line × 800
required_admin = ceil(crew / 1000)
```

Les niveaux sont réglés à ce minimum national exact. Les distributions existantes valides sont conservées proportionnellement lorsque possible. CHI, RUS et USA, qui n'avaient aucune administration, utilisent des États directement possédés, côtiers et dotés de ports ou shipyards cohérents. Aucun niveau d'un sujet ou d'une compagnie n'est crédité au parent.

```text
NONDEFERRED_NAVAL_CREW = 229400
NONDEFERRED_REQUIRED_NAVAL_ADMIN_LEVELS = 239
NAVAL_ADMIN_OVERBUILD = 0
```

## 10. Grande-Bretagne

GBR passe de 33 à 84 niveaux, soit le minimum couvrant 83 400 marins : Home Counties 35, West Country 25, Lancashire 10, Upper Andalusia 9 et Ceylon 5. Tous les États sont directement GBR et côtiers. Ceylon supporte l'abstraction East Indies sans utiliser le territoire de BIC.

```text
GBR_NAVAL_ADMIN_BEFORE = 33
GBR_NAVAL_ADMIN_AFTER = 84
GBR_NAVAL_CAPACITY_AFTER = 84000
GBR_NAVAL_SHORTFALL_AFTER = 0
```

## 11. France

FRA passe de 24 à 28 niveaux pour 27 400 marins : Brittany 14, Poitou 5 et Provence 9. Les trois implantations antérieures sont conservées et augmentées proportionnellement.

## 12. Espagne

SPA passe de 24 à 27 niveaux pour 26 600 marins : Galicia 9, Lower Andalusia 9, Murcia 6 et West Indies 3. Les quatre États sont directement possédés par SPA dans la structure de départ et côtiers.

## 13. Russie

RUS passe de zéro à 22 niveaux pour 21 400 marins. Ingria reçoit 17 niveaux pour la flotte baltique ; Rostov reçoit cinq niveaux pour l'escadre sud/retour d'Archipel. Les deux États sont directement russes, côtiers et possèdent déjà des shipyards.

## 14. Autres puissances navales

Les principaux résultats sont : NET 13→9, SWE 10→16, DENNOR 9→9, POR 9→8, USA 0→3, CHI 0→4 et DEI 2→1. AUS 3→2, GEN 3→2, SAR 2→3 et TUR 9→6. MARATH, OMA, PAP, TRA, TRI, TUN, TUS et VEN étaient déjà à leur minimum et le restent.

```text
NET_NAVAL_ADMIN_AFTER = 9
SWE_NAVAL_ADMIN_AFTER = 16
DENNOR_NAVAL_ADMIN_AFTER = 9
POR_NAVAL_ADMIN_AFTER = 8
USA_NAVAL_ADMIN_AFTER = 3
DEI_NAVAL_ADMIN_AFTER = 1
```

## 15. Structural-defer

Les infrastructures explicites des 34 dispositions structurelles sont préservées. Les flottes gelées ajoutent 9 900 marins : BRZ 4 800, SC4 500 et SIC 4 600. SIC conserve ses trois niveaux existants ; aucun niveau n'est créé pour BRZ ou SC4.

```text
STRUCTURAL_DEFER_INFRA_ACTION = PRESERVE_EXISTING
STRUCTURAL_DEFER_SUPPORT_ONLY = NO

STRUCTURAL_DEFER_FROZEN_NAVAL_CREW = 9900
STRUCTURAL_DEFER_EXISTING_NAVAL_ADMIN = 3
STRUCTURAL_DEFER_UNSUPPORTED_CREW = 6900
STRUCTURAL_DEFER_NAVAL_CAPACITY_SHORTFALL_COUNTRIES = 3
```

Les déficits conservés sont BRZ 4 800, SC4 500 et SIC 1 600 marins. Ils ne participent pas à l'invariant zéro déficit des flottes numériques.

À terre, deux anomalies de recrutement gelées restent également séparées : cinq unités SIC pointent vers Sicily directement possédée par GR3, et une unité UBD vers Courland directement possédée par PLC. Aucun bâtiment n'est ajouté dans ces territoires étrangers ; les six unités constituent `STRUCTURAL_DEFER_LAND_SHORTFALLS = 6`.

## 16. Placements temporaires liés à la map

Les 35 couples pays–État recevant une administration navale finale satisfont tous :

```text
OWNER_DIRECT = YES
COASTAL = YES
STATE_VALID_1_13_9 = YES
```

Le seul placement explicitement marqué comme abstraction est `GBR / STATE_CEYLON / 5`. Il maintient sous GBR le support de l'East Indies Station et suit la correction HQ de 3B.

```text
INFRA_TEMPORARY_MAP_ABSTRACTION = YES (GBR / STATE_CEYLON)
INVALID_FINAL_NAVAL_ADMIN_PLACEMENTS = 0
```

## 17. Budget GBR / risque économique

Le passage de 33 à 84 administrations navales représente un risque budgétaire significatif, même après la réduction 3B de l'armée et de la flotte. Aucun résultat net n'est déduit statiquement : l'emploi, les salaires, les qualifications et les prix devront être contrôlés lors du runtime consolidé.

```text
GBR_PRE_3B_RUNTIME_WEEKLY_BALANCE ≈ -35K to -38K
GBR_3C_BUDGET_RISK = HIGH
ECONOMIC_FIX_ATTEMPTED_IN_3C = NO
ECONOMIC_RECHECK_REQUIRED_AT_CONSOLIDATED_RUNTIME = YES
```

## 18. Invariants

```text
NONDEFERRED_LAND_CAPACITY_SHORTFALL_COUNTRIES_AFTER = 0
NONDEFERRED_NAVAL_CAPACITY_SHORTFALL_COUNTRIES_AFTER = 0
STRUCTURAL_DEFER_LAND_SHORTFALL_COUNTRIES = 2
STRUCTURAL_DEFER_LAND_SHORTFALLS = 6

NONDEFERRED_NAVAL_CREW = 229400
STRUCTURAL_DEFER_FROZEN_NAVAL_CREW = 9900
TOTAL_SCRIPTED_NAVAL_CREW = 239300

NONDEFERRED_REQUIRED_NAVAL_ADMIN_LEVELS = 239
NAVAL_ADMIN_LEVELS_BEFORE = 159
NAVAL_ADMIN_LEVELS_AFTER = 242
FINAL_EXPLICIT_NAVAL_ADMIN = 242

GBR_NAVAL_ADMIN_AFTER = 84
FRA_NAVAL_ADMIN_AFTER = 28
SPA_NAVAL_ADMIN_AFTER = 27
RUS_NAVAL_ADMIN_AFTER = 22

NEW_CONSCRIPTION_CENTER_LEVELS = 0
SHIPYARD_REBALANCE = 0
NAVAL_ADMIN_OVERBUILD = 0
```

## 19. Fichiers modifiés

Douze fichiers d'historique bâtiment sont modifiés :

- `00_west_europe.txt`
- `01_south_europe.txt`
- `03_north_africa.txt`
- `04_subsaharan_africa.txt`
- `05_north_america.txt`
- `06_central_america.txt`
- `08_middle_east.txt`
- `09_central_asia.txt`
- `10_india.txt`
- `11_east_asia.txt`
- `12_indonesia.txt`
- `15_russia.txt`

Deux CSV de recherche et ce rapport sont créés. Aucun autre fichier gameplay n'est modifié par 3C.

## 20. Validation statique

Le parse final retrouve 171 casernes explicites, toutes structurelles, et 242 administrations navales : 239 numériques plus trois SIC gelées. Les 23 pays à flotte non différée ont exactement leur minimum national et aucun placement invalide.

La comparaison bloc par bloc avec HEAD montre que les 2 575 blocs bâtiment hors `building_barrack` et `building_naval_administration` sont identiques. Les 65 blocs shipyard sont inchangés. Les treize références `building_naval_base` hors périmètre sont présentes avant et après.

```text
FORMATION_FILES_CHANGED = 0
DEFINES_CHANGED = 0
COUNTRY_HISTORY_FILES_CHANGED = 0
MAP_FILES_CHANGED = 0
STATE_REGION_FILES_CHANGED = 0
OWNERSHIP_FILES_CHANGED = 0
DIPLOMACY_FILES_CHANGED = 0
TECHNOLOGY_FILES_CHANGED = 0
LOCALISATION_FILES_CHANGED = 0
COMMANDER_FILES_CHANGED = 0
PROTECTED_TECH_FILES_CHANGED = 0

BJECT_PATH_PRESENT = 0
BIC_FRONTIER_COLONIZATION_PRESERVED = YES
BIC_COLONIAL_EXPLOITATION_PRESENT = NO

CODEX_LAUNCHED_VICTORIA3 = NO
GIT_INDEX_MUTATED_BY_CODEX = NO
GIT_DIFF_CHECK = PASS
```

Le define 3A reste à 204 487 octets, SHA-256 `0C3765A9273EE1B34E05E5677DB82518E1296894BA428760EE4492848C415EFF`.

## 21. Readiness CLEANUP-2D-3D

Le modèle terrestre est établi avec une confiance élevée, la capacité navale non différée est complète et aucune incertitude statique ne bloque la mobilisation. Aucun lancement Victoria 3 ni runtime utilisateur intermédiaire n'est demandé.

```text
CLEANUP2D3C_STATIC = PASS
RUNTIME_BLOCKER = NO
NEXT_RECOMMENDED_PHASE = CLEANUP-2D-3D_MOBILISATION_CONSCRIPTION_LEVEES_1776
```
