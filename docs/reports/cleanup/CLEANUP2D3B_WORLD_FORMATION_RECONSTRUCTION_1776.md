# CLEANUP-2D-3B — Reconstruction mondiale des formations militaires et navales (1776)

## 1. Baseline Git

Baseline relevée avant modification :

```text
BRANCH = cleanup-post-release
HEAD = e5d972613ccab1dd113ed5b304e38c5d66e6c086
INDEX_STATE = CLEAN
WORKTREE_STATE = DIRTY_PREEXISTING_PRESERVED
```

État préexistant conservé sans nettoyage : un rapport 2B3 modifié, le rapport non suivi CLEANUP1D, deux fichiers hotfix non suivis et les sept fichiers technologiques protégés non suivis. Codex n'a effectué aucune mutation Git.

## 2. Entrées

Les dix entrées obligatoires 2D0, 2D2 et 3A ont été lues intégralement. `CLEANUP2D2_FORMATION_RECONSTRUCTION_PLAN_1776.csv` a servi d'autorité de structure ligne par ligne. Les deux tables mondiales à 210 tags et la table d'allocation impériale/company ont servi aux contrôles de totalité et de non-double-comptage.

Une incohérence interne a été arbitrée sans changer le total mondial : le CSV de formation partageait par erreur BIC en 19/19/17, alors que le rapport 2D2, la table d'allocation impériale et la consigne 3B imposent tous Bengal 30, Madras 16, Bombay 9. L'implémentation applique donc 30/16/9, soit toujours 55 unités et la composition nationale 42 infanterie / 8 cavalerie / 5 artillerie.

## 3. Anomalie GBR 10/196 contre runtime 9/188

Les dix flottes GBR scriptées avant 3B étaient :

| Formation | Frégates | SOL | Total |
|---|---:|---:|---:|
| Mediterranean Station | 5 | 7 | 12 |
| Lisbon Station | 5 | 4 | 9 |
| North America and West Indies Station | 8 | 0 | 8 |
| Cape of Good Hope Station | 4 | 0 | 4 |
| East Indies and China Station | 7 | 1 | 8 |
| South America Station | 5 | 0 | 5 |
| Portsmouth Station | 12 | 40 | 52 |
| Plymouth Station | 10 | 35 | 45 |
| Sheerness Station | 8 | 30 | 38 |
| Chatham Station | 3 | 12 | 15 |
| **Total** | **67** | **129** | **196** |

```text
GBR_2D0_STATIC_FLEETS = 10
GBR_2D0_STATIC_SHIPS = 196
GBR_3A_RUNTIME_FLEETS = 9
GBR_3A_RUNTIME_SHIPS = 188
GBR_MISSING_RUNTIME_FORMATION = East_Indies_and_China_Station
GBR_MISSING_RUNTIME_SHIP_COUNT = 8
GBR_MISSING_RUNTIME_FORMATION_HQ = region_indochina
GBR_DIRECT_TERRITORY_IN_OLD_HQ = NO
```

Le bloc absent contient exactement sept frégates et un vaisseau de ligne. Il n'est ni conditionnel, ni mal fermé, ni doté d'un scope ou d'un commandant susceptible de casser sa création. Aucune référence externe ne dépend de cette formation.

## 4. Cause de l'anomalie GBR

`region_indochina` contient les États Cambodia, Mekong, Tonkin, Annam, Laos, Chiang Mai, Nakhon Ratchasima, Malaya, Tenasserim, Bangkok, Kachin, Shan, Mandalay, Pegu et Arakan. GBR ne possède directement aucun de ces États au 1776-01-01. Les possessions de BIC ne sont pas assimilées à celles de GBR.

Le déficit runtime correspond exactement au seul bloc ayant ce défaut : une formation et huit navires. L'antécédent connu du fork, la validité syntaxique du bloc, l'absence de scope cassé et l'égalité exacte du delta établissent la cause.

```text
GBR_RUNTIME_DISCREPANCY_ROOT_CAUSE = HQ region_indochina sans territoire directement possédé par GBR au démarrage; échec connu de matérialisation de formation
KNOWN_HQ_MATERIALIZATION_FAILURE_CONFIRMED = YES
```

La nouvelle `East Indies Station` reste une flotte GBR. Son HQ est `region_south_india`, validé par la possession directe GBR de Ceylon. Ce choix est une abstraction technique de map et non un transfert à BIC.

```text
HQ_TEMPORARY_MAP_ABSTRACTION = YES
```

## 5. Méthode d'implémentation

Les 259 lignes du plan se répartissent en 240 formations numériques, 15 lignes `STRUCTURAL_DEFER` et 4 suppressions. Les blocs existants ont été réemployés lorsque possible afin de conserver leur ordre d'exécution, leurs scopes et leurs commandants. Les créations sans bloc source ont été ajoutées au bloc pays approprié.

Les types de base sont ceux de la baseline 1.13.9 : infanterie de ligne ou irrégulière selon le système et le précédent technique du pays, cuirassiers/dragoons/hussards/lanciers existants ou régionaux, artillerie à canon, frégates et vaisseaux de ligne. `mobile_artillery` et `low_tier_marines` n'ont pas été conservés automatiquement : leurs lignes 2D2 ont `other_land=0` et ont été converties dans les catégories cibles explicites.

Chaque HQ proposé a été confronté aux États directement possédés dans `00_states.txt` et aux régions stratégiques vanilla 1.13.9. Soixante-deux propositions sans présence directe ont reçu un HQ valide ; chaque correction est marquée `HQ_TEMPORARY_MAP_ABSTRACTION=YES` dans le CSV de résultat. Les 255 formations finales, gels compris, ont ensuite été contrôlées une seconde fois.

```text
EVERY_TARGET_FORMATION_HQ_VALIDATED_FOR_STARTING_COUNTRY_PRESENCE = YES
FINAL_ACTIVE_FORMATIONS_WITH_INVALID_HQ = 0
```

## 6. Totaux mondiaux avant/après

| Mesure | Avant | Après scripté | Cible numérique 2D2 | Écart expliqué |
|---|---:|---:|---:|---:|
| Formations terrestres actives | 148 | 214 | 202 numériques | +12 gels |
| Flottes scriptées | 49 | 41 | 38 numériques | +3 gels |
| Unités terrestres | 2 948 | 2 557 | 2 431 | +126 gels |
| Frégates | 377 | 189 | 174 | +15 gels |
| Vaisseaux de ligne | 226 | 181 | 178 | +3 gels |
| Unités navales | 603 | 370 | 352 | +18 gels |
| Marins | 369 300 | 239 300 | 229 400 | +9 900 gels |

```text
ACTIVE_LAND_FORMATIONS_BEFORE = 148
ACTIVE_LAND_FORMATIONS_AFTER = 214
ACTIVE_FLEETS_BEFORE = 49
ACTIVE_FLEETS_AFTER = 41
LAND_UNITS_BEFORE = 2948
LAND_UNITS_AFTER = 2557
FRIGATES_BEFORE = 377
FRIGATES_AFTER = 189
SOL_BEFORE = 226
SOL_AFTER = 181
NAVAL_UNITS_BEFORE = 603
NAVAL_UNITS_AFTER = 370
NAVAL_CREW_BEFORE = 369300
NAVAL_CREW_AFTER = 239300
```

Les seules différences avec 2D2 sont les lignes gelées suivantes : BRZ land 4/naval 9, CUB land 11, HAI land 20, PCO land 7, PHI land 7, SC2 land 7+18+9, SC4 land 7/naval 1, SIC land 20+10/naval 8, UBD land 6. Leur détail de composition figure ligne par ligne dans le CSV de résultat.

## 7. Grande-Bretagne

GBR passe de 121 à 49 unités terrestres réparties dans cinq commandements, sans ajout au-dessus du pool Crown. La Royal Navy passe de 196 navires statiques à la cible de 120 : 42 frégates et 78 SOL, soit 83 400 marins, dans sept commandements distincts.

Les quatre scopes terrestres existants restent associés aux rôles survivants : Home, West Indies, Mediterranean et India. `med_fleet_gbr`, issu de Lisbon Station, est conservé sur la nouvelle Mediterranean Station. L'East Indies Station reste GBR, compte 4 frégates et 3 SOL selon le plan 2D2 et utilise le HQ valide `region_south_india`.

```text
GBR_TARGET_LAND_UNITS = 49
GBR_TARGET_NAVAL_UNITS = 120
GBR_TARGET_NAVAL_CREW = 83400
```

## 8. France

Les quatre armées françaises totalisent 165 unités. Les scopes `frencharmy1`, `secondcorpfra`, `thirdcorpfra` et `africacorpfra` sont conservés. Brest, Toulon et Rochefort/outre-mer totalisent 18 frégates et 23 SOL, soit 41 navires ; le niveau de guerre 1778-1783 n'est pas reproduit.

## 9. Espagne / Real Armada

Les deux blocs identiques `Real_Armada_Espaola` ont été reconstruits et renommés ; aucun doublon de ce nom ne subsiste. Les scopes et deux amiraux existants restent respectivement sur Cádiz et Cartagena. América est une troisième formation distincte.

| Escadre | Frégates | SOL | Total |
|---|---:|---:|---:|
| Escuadra de Cádiz | 7 | 10 | 17 |
| Escuadra de Cartagena | 4 | 6 | 10 |
| Escuadra de América | 7 | 6 | 13 |

```text
IDENTICAL_REAL_ARMADA_DUPLICATE = 0
SPA_DISTINCT_SQUADRONS = 3
```

## 10. Russie

La Russie possède cinq commandements terrestres totalisant 215 unités. Les scopes des corps fusionnés sont tous sauvegardés sur leurs formations cibles. Baltic Fleet et Archipelago Return Squadron totalisent 14 frégates, 18 SOL et 21 400 marins.

## 11. Prusse

Les quatre armées prussiennes totalisent 158 unités. `Kniglich_Preuische_Marine`, formation vide, est supprimée. Son seul dépendant était un `create_ship` de l'ancienne Princess Louise pointant vers `fleet_scope_prussian_navy` ; ce dépendant a été supprimé avec la flotte, de sorte qu'aucune référence orpheline nouvelle n'est créée.

```text
PRU_COMBAT_FLEETS = 0
PRU_FRIGATES = 0
PRU_SHIPS_OF_THE_LINE = 0
```

## 12. USA

Les trois anciennes armées sont consolidées dans une Continental Army de 20 unités : 17 infanterie, 2 cavalerie et 1 artillerie. Les six anciennes formations navales sont consolidées dans une Continental Squadron de cinq frégates et aucun SOL. Les trois scopes terrestres existants sont conservés.

```text
USA_STARTING_LAND_UNITS = 20
USA_STARTING_SOL = 0
```

## 13. Qing

Les seize formations terrestres sont consolidées en quatre Banner Commands et quatre Green Standard Commands. La cible est exactement 290 unités : 230 infanterie et 60 cavalerie, sans artillerie. Les huit scopes Banner et leurs commandants sont préservés ; les Green Standard sont consolidées entre elles, sans conversion 1:1 de l'établissement administratif de 800 000 hommes.

## 14. Habsbourg

L'allocation terrestre est AUS 140, HUN 28, BEO 12, GAL 12 et TRS 8, total 200. Les unités des sous-tags ne sont pas recréées sous AUS. La flotte BEO non soutenue est supprimée.

```text
HABSBURG_TOTAL_ALLOCATED = 200
HABSBURG_DOUBLE_COUNT = 0
```

## 15. BIC / DEI / HBC

BIC reçoit Bengal 30, Madras 16 et Bombay 9, total 55. Les huit catégories Crown comprises dans le modèle britannique ne sont pas dupliquées sous BIC. `bengal_army` reste préservé ; la référence préexistante `madras_army` demeure volontairement réservée à 2D4 conformément à la consigne, sans nouvelle dégradation.

DEI reçoit 12 unités company/garrison et deux frégates. HBC reçoit une unité de sécurité corporate/local security et aucune flotte. L'architecture company/executive issue de 2C n'est pas modifiée.

```text
BIC_TARGET_LAND_UNITS = 55
BIC_CROWN_DOUBLE_COUNT = 0
HBC_COMBAT_FLEETS = 0
```

## 16. Autres puissances principales

NET atteint 8 frégates / 6 SOL en deux escadres ; son escadre Méditerranée/convoyage utilise temporairement `region_western_europe`, directement possédée. SWE atteint 6/16, DENNOR 8/6 et POR 8/4. Le South Atlantic Squadron portugais reste POR et utilise temporairement `region_southern_europe`, faute de possession portugaise directe dans `region_brazil`.

## 17. Structural-defer

Les 34 tags à disposition structurelle sont tous comptabilisés. Quinze lignes correspondant à des formations physiques existantes sont gelées exactement, soit 12 formations terrestres et 3 navales. Les tags à allocation Habsbourg explicitement numérique sont implémentés depuis le pool partagé. Les autres dispositions sans formation physique restent sans armée fictive.

Les 35 tags sans ligne de formation sont également comptabilisés par leur cible zéro ou leur disposition sans force indépendante : ALK, ANH, BHN, BRA, DAI, EZO, GR3, GR5, HAW, IQU, IREK, KAU, LAH, LIP, LOU, MLD, MLT, NBS, NVS, ONT, ORA, PHL, PLY, QUE, RYU, SC1, SC3, SCM, SHS, SIL, SOK, TRN, UNT, UZH et WTU.

```text
ALL_210_TAGS_ACCOUNTED = YES
STRUCTURAL_DEFER_FAKE_FORCES_CREATED = 0
```

## 18. Scopes et références

Un audit dépôt a précédé les suppressions et fusions. Les 49 scopes de formation initiaux deviennent 48 : le seul supprimé est `fleet_scope_prussian_navy`, avec son unique dépendant. Les 44 références actives `transfer_to_formation` sont inchangées ; la seule référence sans formation reste le `madras_army` préexistant et explicitement différé. Les lignes commentées de `99_military_formations_example.txt` sont exclues du compte actif.

Les scopes multiples issus de fusions russes, Qing et américaines sont sauvegardés sur le même objet cible. Les scopes espagnols `spanishnavy1` et `spanishnavy2` sont conservés. Aucun scope final n'est dupliqué entre deux formations.

```text
NEW_DUPLICATE_FORMATION_SCOPES = 0
NEW_BROKEN_SCOPE_REFERENCES = 0
```

## 19. Commandants à réassigner en 2D-4

Le contenu des 54 blocs `create_character` présents dans les fichiers de formation est identique, dans le même ordre, avant et après 3B. Les formations supprimées BEO, HAN et PRU n'avaient aucun commandant. Les deux amiraux espagnols, les commandants Qing et les autres commandants scoped restent attachés via leurs scopes conservés.

```text
COMMANDER_REASSIGNMENT_REQUIRED_2D4 = 0
NEW_COMMANDERS_CREATED = 0
```

Les 240 formations numériques restent marquées comme devant être vérifiées/dotées selon le plan lors de 2D4 ; cela ne constitue pas une réassignation causée par une suppression 3B.

## 20. Localisations créées

Deux fichiers dédiés ont été créés, avec 152 clés identiques et uniques :

- `localization/english/cleanup2d3b_formations_l_english.yml`
- `localization/french/cleanup2d3b_formations_l_french.yml`

Les deux sont UTF-8 BOM. Les noms historiques propres sont conservés ; les libellés génériques « Modeled 1776 Field Force » sont traduits en français.

```text
NEW_DUPLICATE_FORMATION_NAMES_UNJUSTIFIED = 0
LOCALIZATION_UTF8_BOM = PASS
```

## 21. Déficit GBR et defer économique

```text
GBR_RUNTIME_PRE_REBALANCE_BUDGET = SEVERE_DEFICIT
GBR_PRE_3B_RUNTIME_WEEKLY_BALANCE ≈ -35K to -38K
ECONOMIC_FIX_ATTEMPTED_IN_3B = NO
ECONOMIC_RECHECK_REQUIRED_AFTER_3C = YES
```

Aucun impôt, revenu, prix, salaire, subside ou modificateur budgétaire n'a été modifié. La donnée runtime reste un point de QA pour 3C/3E.

## 22. Validation statique

Le parseur statique final trouve 255 formations : 214 armées et 41 flottes. Toutes les accolades se ferment, chaque formation a un domaine, chaque composition somme au total de sa ligne, et les types utilisés existent dans la baseline vanilla 1.13.9. Aucun `mobile_artillery` ou `low_tier_marines` nouveau n'est introduit.

Les invariants principaux sont validés : GBR 49/120, FRA 165/41, SPA 95/40, RUS 215/32, PRU 158/0, USA 20/5 avec zéro SOL, CHI 290, Habsbourg 200, BIC 55, DEI 12/2 et HBC 1/0.

Le define 3A reste à 204 487 octets, SHA-256 `0C3765A9273EE1B34E05E5677DB82518E1296894BA428760EE4492848C415EFF`.

```text
NEW_INVALID_UNIT_TYPE_REFERENCES = 0
DEFINES_CHANGED = 0
BUILDING_HISTORY_FILES_CHANGED = 0
COUNTRY_HISTORY_FILES_CHANGED = 0
MAP_FILES_CHANGED = 0
STATE_REGION_FILES_CHANGED = 0
OWNERSHIP_FILES_CHANGED = 0
DIPLOMACY_FILES_CHANGED = 0
TECHNOLOGY_FILES_CHANGED = 0
COMMANDER_CHARACTER_FILES_CHANGED = 0
PORTRAIT_FILES_CHANGED = 0
DNA_FILES_CHANGED = 0
PROTECTED_TECH_FILES_CHANGED = 0
BJECT_PATH_PRESENT = 0
BIC_FRONTIER_COLONIZATION_PRESERVED = YES
BIC_COLONIAL_EXPLOITATION_PRESENT = NO
CODEX_LAUNCHED_VICTORIA3 = NO
GIT_INDEX_MUTATED_BY_CODEX = NO
GIT_DIFF_CHECK = PASS
```

Les sept hashes technologiques protégés restent respectivement `315CB857…`, `88D090A4…`, `0FE06A18…`, `01A37C0B…`, `C4EF474D…`, `6E7A4876…` et `150256D3…`, identiques à la baseline.

## 23. Readiness 2D-3C

La reconstruction des formations est statiquement complète. Les écarts temporaires entre unités et bâtiments sont attendus et appartiennent à 3C ; aucun fichier d'infrastructure n'a été touché ici. Il n'existe pas d'incertitude statique bloquant la phase suivante et aucun runtime utilisateur n'est demandé après 3B.

```text
CLEANUP2D3B_STATIC = PASS
RUNTIME_BLOCKER = NO
NEXT_RECOMMENDED_PHASE = CLEANUP-2D-3C_INFRASTRUCTURE_MILITAIRE_ET_NAVALE_1776
```
