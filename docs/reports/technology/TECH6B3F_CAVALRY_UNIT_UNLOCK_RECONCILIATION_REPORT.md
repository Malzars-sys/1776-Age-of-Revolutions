# TECH6B3F-CAV2 — Cavalry Unit Unlock Order Reconciliation

## A. Checkpoint

- Audit effectué sur Victoria 3 1.13.11 avec le vanilla canonique `C:/Games/Victoria 3/game`.
- Branche réellement checkoutée : `tech6b3h-starting-tech-reconciliation-implementation`.
- La branche annoncée dans le prompt (`tech6b3f-hidden-tech-responsibility-implementation`) ne correspond donc pas au checkpoint Git effectif.
- Le worktree contenait déjà des modifications non commitées, notamment dans `common/combat_unit_types/00_land_combat_unit_types.txt`. Elles ont été préservées.
- Les cinq gates autoritatifs étaient déjà présents dans l'overlay au début de cette passe. Aucun gate n'a été réécrit.
- À la demande explicite de l'utilisateur en cours de passe, les blocs des unités ont été réordonnés dans leur fichier de données afin que la liste runtime suive l'ordre chronologique de haut en bas. Aucun fichier sous `gui/` n'a été modifié.
- Commit : non. Push : non.

## B. Décision utilisateur antérieure retrouvée

La matrice fournie par l'utilisateur est traitée comme autorité finale :

1. Lanciers → aucun gate ;
2. Dragons → `regulated_small_arms` ;
3. Hussards → `horse_artillery` ;
4. Cuirassiers → `military_veterinary_services` ;
5. Chars légers → `mobile_armor`.

La capture runtime fournie pendant la passe montrait l'ancien ordre d'affichage `Hussards, Dragons, Cuirassiers, Lanciers, Chars légers`. Cet ordre reproduisait exactement l'ancien ordre de déclaration du fichier des types d'unités. Les blocs sont désormais déclarés dans l'ordre autoritatif ci-dessus.

## C. IDs des cinq unités

| DISPLAY_NAME | UNIT_ID | SOURCE_FILE | CURRENT_UNLOCK_TECH | VISIBLE | ERA | EXPECTED | STATUS |
|---|---|---|---|---|---|---|---|
| Lanciers | `combat_unit_type_lancers` | `common/combat_unit_types/00_land_combat_unit_types.txt` | NONE | N/A | NONE | NONE | ALREADY_CORRECT |
| Dragons | `combat_unit_type_dragoons` | `common/combat_unit_types/00_land_combat_unit_types.txt` | `regulated_small_arms` | YES | `era_2` | `regulated_small_arms` | ALREADY_CORRECT |
| Hussards | `combat_unit_type_hussars` | `common/combat_unit_types/00_land_combat_unit_types.txt` | `horse_artillery` | YES | `era_4` | `horse_artillery` | ALREADY_CORRECT |
| Cuirassiers | `combat_unit_type_cuirassiers` | `common/combat_unit_types/00_land_combat_unit_types.txt` | `military_veterinary_services` | YES | `era_5` | `military_veterinary_services` | ALREADY_CORRECT |
| Chars légers | `combat_unit_type_light_tanks` | `common/combat_unit_types/00_land_combat_unit_types.txt` | `mobile_armor` | YES | `era_12` | `mobile_armor` | ALREADY_CORRECT |

Les noms français proviennent du vanilla 1.13.11 `localization/french/interfaces_l_french.yml`. Les quatre technologies possèdent chacune une définition unique dans l'univers technologique remplacé par le mod, n'ont pas `can_research = no` et sont donc visibles/recherchables.

## D. Gates avant la passe

Le checkpoint overlay contenait déjà :

```text
combat_unit_type_lancers      -> NONE
combat_unit_type_dragoons     -> regulated_small_arms
combat_unit_type_hussars      -> horse_artillery
combat_unit_type_cuirassiers  -> military_veterinary_services
combat_unit_type_light_tanks  -> mobile_armor
```

Ces valeurs sont les gates effectifs au début de TECH6B3F-CAV2, indépendamment du contenu de `HEAD`. Le diff Git montrait que plusieurs d'entre elles appartenaient à des modifications antérieures non commitées ; elles n'ont pas été revendiquées comme nouvelles corrections de cette passe.

## E. Gates attendus

La comparaison avant/attendu donne cinq égalités exactes. Il n'existe ni gate additionnel dans les blocs concernés, ni alias caché requis pour rendre l'unité disponible.

`UNIT_GATES_CHANGED = 0`

`UNIT_GATES_ALREADY_CORRECT = 5`

## F. Corrections appliquées

Aucune correction de gate n'était nécessaire. Une correction distincte d'ordre d'affichage a été appliquée après le rappel explicite de l'utilisateur :

- ancien ordre de déclaration : Hussards → Dragons → Cuirassiers → Lanciers → Chars légers ;
- nouvel ordre de déclaration : Lanciers → Dragons → Hussards → Cuirassiers → Chars légers ;
- fichier modifié : `common/combat_unit_types/00_land_combat_unit_types.txt` ;
- fichiers GUI modifiés : 0 ;
- statistiques, upkeep, images, gates et relations `upgrades` préservés à l'identique pendant le déplacement des blocs.

## G. Progression finale, upgrades, AI et statistiques

### Disponibilité technologique et affichage

```text
START                 Lanciers
era_2                 regulated_small_arms          -> Dragons
era_4                 horse_artillery               -> Hussards
era_5                 military_veterinary_services  -> Cuirassiers
era_12                mobile_armor                  -> Chars légers
```

L'ordre de déclaration des cinq objets suit désormais ce même ordre de haut en bas.

### Upgrade path effectif

Le moteur utilise des listes de cibles `upgrades`, pas un pointeur unique de remplacement. L'architecture existante est conservée :

- Lanciers → Dragons, Hussards ou Cuirassiers ;
- Dragons → Hussards ou Cuirassiers ;
- Hussards → Cuirassiers ;
- Cuirassiers → Chars légers ;
- Chars légers → aucune cible déclarée.

Cette architecture autorise la chaîne souhaitée et certains raccourcis. Aucune syntaxe linéaire artificielle n'a été inventée.

### AI et autres références

- Aucun des cinq IDs n'est référencé dans `common/ai_strategies/` ou `common/mobilization_options/` comme substitution d'unité.
- `events/soi_events/00_ep1_kazakh_events.txt` crée ponctuellement des Hussards ; cette référence d'événement n'est pas un gate du type d'unité.
- Les références des formations historiques sont auditées séparément ci-dessous.

### Statistiques inventoriées

| Unité | Attaque | Défense | Caractéristiques majeures |
|---|---:|---:|---|
| Lanciers | 16 | 10 | morale loss +12 ; kill rate +0.03 ; occupation +0.15 ; mobilisation/mouvement +0.10 |
| Dragons | 20 | 24 | morale loss +9 ; occupation +0.25 ; mobilisation/mouvement +0.10 |
| Hussards | 24 | 18 | morale loss +8 ; occupation +0.30 ; mobilisation/mouvement +0.25 |
| Cuirassiers | 32 | 28 | morale loss +6 ; kill rate +0.05 ; morale damage +0.05 ; occupation +0.30 |
| Chars légers | 45 | 45 | morale loss +4 ; devastation +0.10 ; occupation +0.30 ; mobilisation +0.20 |

Les Dragons privilégient la défense et les Hussards la vitesse, ce qui constitue une spécialisation lisible plutôt qu'une régression stricte. `STAT_ORDER_CONCERN = NO`.

## H. Ordre des quatre technologies

| Technologie | Fichier | Ère | Parents directs pertinents | Visible/recherchable |
|---|---|---|---|---|
| `regulated_small_arms` | `common/technology/technologies/20_tech3a_military.txt` | `era_2` | `scientific_fortification_siegecraft` (`era_1`) | YES |
| `horse_artillery` | `common/technology/technologies/20_tech3a_military.txt` | `era_4` | `standardized_field_artillery` (`era_3`), lui-même enfant de `regulated_small_arms` | YES |
| `military_veterinary_services` | `common/technology/technologies/20_tech3a_military.txt` | `era_5` | `horse_artillery` (`era_4`) | YES |
| `mobile_armor` | `common/technology/technologies/90_tech3a_vanilla_post1836_compatibility.txt` | `era_12` | `military_aviation`, `stormtroopers` | YES |

L'ordre d'ère est strictement croissant : 2 → 4 → 5 → 12. `horse_artillery` est topologiquement en aval de `regulated_small_arms`, et `military_veterinary_services` est directement en aval de `horse_artillery`. `mobile_armor` reste une rupture tardive. `TECH_ORDER_CONFLICT = NO`.

## I. Conflits de topologie

- Aucun parent inconnu parmi les quatre technologies.
- Aucun cycle ajouté.
- Aucune arête technologique ajoutée.
- Aucune arête cross-category ajoutée.
- Aucun des cinq gates n'appartient aux 44 aliases cachés de TECH6B3F.

`CAVALRY_HIDDEN_TECH_GATES = 0`

## J. Formations de départ potentiellement incohérentes

Méthode : audit de l'overlay VFS effectif. Un fichier pays du mod masque le vanilla lorsqu'il possède le même chemin relatif ; les fichiers vanilla non masqués restent inclus. Les appels de tiers sont développés avec le `common/scripted_effects/00_starting_inventions.txt` effectif du mod. Les Lanciers sont exclus des anomalies car ils n'ont aucun gate.

Synthèse :

| Unité | Formations utilisant l'unité | Sans gate requis |
|---|---:|---:|
| Lanciers | 43 | 0 |
| Dragons | 66 | 34 |
| Hussards | 34 | 34 |
| Cuirassiers | 14 | 14 |
| Chars légers | 0 | 0 |

Chaque ligne suivante a `COUNTRY_HAS_GATE = NO` et doit être transmise à la réconciliation des technologies de départ, sans correction dans cette passe.

| COUNTRY | FORMATION | UNIT | EXPECTED_GATE | COUNTRY_HAS_GATE |
|---|---|---|---|---|
| CRI | `cleanup2d3e_r1_cri_land_1` | Hussards | `horse_artillery` | NO |
| PLC | `cleanup2d3e_r1_plc_land_1` | Hussards | `horse_artillery` | NO |
| PRU | `cleanup2d3b_pru_land_4` | Hussards | `horse_artillery` | NO |
| PRU | `cleanup2d3b_pru_land_1` | Cuirassiers | `military_veterinary_services` | NO |
| PRU | `cleanup2d3b_pru_land_3` | Hussards | `horse_artillery` | NO |
| AUS | `cleanup2d3b_aus_land_3` | Cuirassiers | `military_veterinary_services` | NO |
| AUS | `cleanup2d3b_aus_land_4` | Cuirassiers | `military_veterinary_services` | NO |
| AUS | `cleanup2d3b_aus_land_2` | Cuirassiers | `military_veterinary_services` | NO |
| HUN | `generalkommando_ofen` | Hussards | `horse_artillery` | NO |
| RUS | `cleanup2d3b_rus_land_1` | Cuirassiers | `military_veterinary_services` | NO |
| RUS | `cleanup2d3b_rus_land_2` | Cuirassiers | `military_veterinary_services` | NO |
| CIR | `cleanup2d3e_r1_cir_land_1` | Hussards | `horse_artillery` | NO |
| CHC | `Murtazeki` | Hussards | `horse_artillery` | NO |
| BAV | `I_ArmeeKorps` | Hussards | `horse_artillery` | NO |
| HEK | `Kurfrstlich_Hessische_Armee` | Hussards | `horse_artillery` | NO |
| SWE | `Kungliga_Svenska_Armn` | Hussards | `horse_artillery` | NO |
| WAL | `Armata_rii_Romneti` | Hussards | `horse_artillery` | NO |
| MON | `Montengrin_Raiders` | Hussards | `horse_artillery` | NO |
| MOL | `Armata_Principatului_Moldovei` | Hussards | `horse_artillery` | NO |
| SIC | `Guardia_Reale` | Hussards | `horse_artillery` | NO |
| POR | `Exercito_Portugues` | Hussards | `horse_artillery` | NO |
| SPA | `cleanup2d3b_spa_land_2` | Cuirassiers | `military_veterinary_services` | NO |
| SPA | `cleanup2d3b_spa_land_3` | Hussards | `horse_artillery` | NO |
| GAL | `cleanup2d3b_gal_land_1` | Hussards | `horse_artillery` | NO |
| KOR | `cleanup2d3b_kor_land_1` | Dragons | `regulated_small_arms` | NO |
| NEP | `cleanup2d3b_nep_land_1` | Dragons | `regulated_small_arms` | NO |
| SWI | `cleanup2d3b_swi_land_1` | Hussards | `horse_artillery` | NO |
| TIB | `cleanup2d3b_tib_land_1` | Dragons | `regulated_small_arms` | NO |
| USA | `cleanup2d3b_usa_land_1` | Hussards | `horse_artillery` | NO |
| BRZ | `Exrcito_Imperial_Brasileiro` | Cuirassiers | `military_veterinary_services` | NO |
| SC4 | `Ejrcito_Argentino` | Cuirassiers | `military_veterinary_services` | NO |
| SC2 | `Ejrcito_del_Ecuador` | Cuirassiers | `military_veterinary_services` | NO |
| SC2 | `Ejrcito_de_la_Nueva_Granada` | Cuirassiers | `military_veterinary_services` | NO |
| SC2 | `Ejrcito_de_Venezuela` | Cuirassiers | `military_veterinary_services` | NO |
| TUN | `cleanup2d3b_tun_land_1` | Dragons | `regulated_small_arms` | NO |
| TRI | `cleanup2d3b_tri_land_1` | Dragons | `regulated_small_arms` | NO |
| MAS | `Jaish_alMohammadi` | Hussards | `horse_artillery` | NO |
| CON | `cleanup2d3b_con_land_1` | Dragons | `regulated_small_arms` | NO |
| DFR | `cleanup2d3b_dfr_land_1` | Dragons | `regulated_small_arms` | NO |
| IR1 | `cleanup2d3e_r1_ir1_land_1` | Hussards | `horse_artillery` | NO |
| TUR | `cleanup2d3b_tur_land_1` | Hussards | `horse_artillery` | NO |
| TUR | `cleanup2d3b_tur_land_2` | Hussards | `horse_artillery` | NO |
| TUR | `cleanup2d3b_tur_land_4` | Hussards | `horse_artillery` | NO |
| OMA | `cleanup2d3e_r1_oma_land_1` | Hussards | `horse_artillery` | NO |
| PER | `cleanup2d3e_r1_per_land_1` | Hussards | `horse_artillery` | NO |
| DUR | `cleanup2d3e_r1_dur_land_1` | Hussards | `horse_artillery` | NO |
| DUR | `cleanup2d3e_r1_dur_land_2` | Hussards | `horse_artillery` | NO |
| ARB | `cleanup2d3e_r1_arb_land_1` | Hussards | `horse_artillery` | NO |
| PAN | `FaujiAin` | Cuirassiers | `military_veterinary_services` | NO |
| MUG | `MughalArmy` | Hussards | `horse_artillery` | NO |
| CHI | `cleanup2d3b_chi_land_1` | Hussards | `horse_artillery` | NO |
| CHI | `cleanup2d3b_chi_land_2` | Hussards | `horse_artillery` | NO |
| CHI | `cleanup2d3b_chi_land_3` | Hussards | `horse_artillery` | NO |
| CHI | `cleanup2d3b_chi_land_4` | Hussards | `horse_artillery` | NO |
| CHI | `cleanup2d3b_chi_land_5` | Dragons | `regulated_small_arms` | NO |
| CHI | `cleanup2d3b_chi_land_6` | Dragons | `regulated_small_arms` | NO |
| CHI | `cleanup2d3b_chi_land_7` | Dragons | `regulated_small_arms` | NO |
| CHI | `cleanup2d3b_chi_land_8` | Dragons | `regulated_small_arms` | NO |
| BUR | `tatmadaw` | Cuirassiers | `military_veterinary_services` | NO |
| BAL | `cleanup2d3b_bal_land_1` | Dragons | `regulated_small_arms` | NO |
| AGC | `army_of_angoche` | Dragons | `regulated_small_arms` | NO |
| ASH | `cleanup2d3b_ash_land_1` | Dragons | `regulated_small_arms` | NO |
| BEN | `cleanup2d3b_ben_land_1` | Dragons | `regulated_small_arms` | NO |
| BOR | `cleanup2d3b_bor_land_1` | Dragons | `regulated_small_arms` | NO |
| BRD | `cleanup2d3b_brd_land_1` | Dragons | `regulated_small_arms` | NO |
| BST | `cleanup2d3b_bst_land_1` | Dragons | `regulated_small_arms` | NO |
| BUG | `cleanup2d3b_bug_land_1` | Dragons | `regulated_small_arms` | NO |
| DAH | `cleanup2d3b_dah_land_1` | Dragons | `regulated_small_arms` | NO |
| ETH | `cleanup2d3b_eth_land_1` | Dragons | `regulated_small_arms` | NO |
| FTJ | `cleanup2d3b_ftj_land_1` | Dragons | `regulated_small_arms` | NO |
| FTR | `cleanup2d3b_ftr_land_1` | Dragons | `regulated_small_arms` | NO |
| GLD | `cleanup2d3b_gld_land_1` | Dragons | `regulated_small_arms` | NO |
| HAU | `cleanup2d3b_hau_land_1` | Dragons | `regulated_small_arms` | NO |
| KON | `cleanup2d3b_kon_land_1` | Dragons | `regulated_small_arms` | NO |
| KRT | `cleanup2d3b_krt_land_1` | Dragons | `regulated_small_arms` | NO |
| MAD | `cleanup2d3b_mad_land_1` | Dragons | `regulated_small_arms` | NO |
| MJT | `cleanup2d3b_mjt_land_1` | Dragons | `regulated_small_arms` | NO |
| MSN | `cleanup2d3b_msn_land_1` | Dragons | `regulated_small_arms` | NO |
| OYO | `cleanup2d3b_oyo_land_1` | Dragons | `regulated_small_arms` | NO |
| RWD | `cleanup2d3b_rwd_land_1` | Dragons | `regulated_small_arms` | NO |
| SGU | `cleanup2d3b_sgu_land_1` | Dragons | `regulated_small_arms` | NO |
| WAD | `cleanup2d3b_wad_land_1` | Dragons | `regulated_small_arms` | NO |

`STARTING_ARMIES_WITH_POTENTIAL_MISMATCH = 82`

`STARTING_ARMY_FILES_CHANGED = 0`

`STARTING_TECH_FILES_CHANGED = 0`

## K. Validation

| Contrôle | Résultat |
|---|---|
| CAVALRY_UNITS_FOUND | 5 |
| LANCERS_FINAL_GATE | NONE |
| DRAGOONS_FINAL_GATE | `regulated_small_arms` |
| HUSSARS_FINAL_GATE | `horse_artillery` |
| CUIRASSIERS_FINAL_GATE | `military_veterinary_services` |
| LIGHT_TANKS_FINAL_GATE | `mobile_armor` |
| DECLARATION_DISPLAY_ORDER | Lanciers → Dragons → Hussards → Cuirassiers → Chars légers |
| CAVALRY_HIDDEN_TECH_GATES | 0 |
| UNKNOWN_UNIT_IDS | 0 |
| UNKNOWN_TECH_IDS | 0 |
| INVENTED_UNIT_IDS | 0 |
| INVENTED_TECH_IDS | 0 |
| TECH_ORDER_CONFLICT | NO |
| STAT_ORDER_CONCERN | NO |
| CROSS_CATEGORY_TECH_EDGES_ADDED | 0 |
| STARTING_TECH_FILES_CHANGED | 0 |
| STARTING_ARMY_FILES_CHANGED | 0 |
| GUI_FILES_CHANGED | 0 |
| STATIC_VALIDATION | PASS |
| PARSER_LOG_SMOKE | NOT_RUN |

La validation statique couvre l'unicité des cinq IDs, l'extraction exacte de leurs gates, l'existence/unicité/visibilité des technologies, l'ordre des ères et parents, l'absence d'alias caché parmi les gates, l'équilibrage des accolades, l'ordre de déclaration et l'absence de changement dans les répertoires de départ et GUI. Aucun lancement Victoria 3 frais n'a été exécuté pendant cette passe ; le contrôle runtime de l'ordre devra être confirmé au prochain chargement.

## Résultat terminal

```text
TECH6B3F_CAVALRY_UNIT_UNLOCK_RECONCILIATION = PASS

CAVALRY_UNITS_FOUND = 5

LANCERS_FINAL_GATE = NONE
DRAGOONS_FINAL_GATE = regulated_small_arms
HUSSARS_FINAL_GATE = horse_artillery
CUIRASSIERS_FINAL_GATE = military_veterinary_services
LIGHT_TANKS_FINAL_GATE = mobile_armor

UNIT_GATES_CHANGED = 0
UNIT_GATES_ALREADY_CORRECT = 5

TECH_ORDER_CONFLICT = NO
STAT_ORDER_CONCERN = NO

STARTING_ARMIES_WITH_POTENTIAL_MISMATCH = 82

CAVALRY_HIDDEN_TECH_GATES = 0

UNKNOWN_UNIT_IDS = 0
UNKNOWN_TECH_IDS = 0
INVENTED_UNIT_IDS = 0
INVENTED_TECH_IDS = 0

STARTING_TECH_FILES_CHANGED = 0
STARTING_ARMY_FILES_CHANGED = 0
GUI_FILES_CHANGED = 0

STATIC_VALIDATION = PASS
PARSER_LOG_SMOKE = NOT_RUN

GAMEPLAY_FILES_CHANGED = 1

COMMIT = NO
PUSH = NO
```
