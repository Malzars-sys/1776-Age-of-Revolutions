# HOTFIX-6A.23 — Sélection résiduelle globale post-Afghanistan

Date : 5 août 2026

Branche : `hotfix-dlc-audit`

HEAD d'entrée : `1214c0ca2bd912be90076941494115847baac4df`

Nature : réindexation documentaire et audit statique, sans modification gameplay ni runtime

Modèle recommandé : GPT-5.6 Thinking avec raisonnement élevé. Nombre de
lancements Victoria 3 : **0**.

## 1. Verdict

La génération fraîche produite par 6A.22Q est séparée des générations
précédentes et de leurs rotations. Les deux diagnostics de pinning Afghanistan
ont disparu, aucune nouvelle identité normalisée n'est apparue et les 17
diagnostics régionaux `PostValidate` préexistants restent strictement
inchangés. Les blocs de pinning Afghanistan et Pologne demeurent clos.

Parmi les onze chemins encore classés
`VANILLA_1_13_ALIGNMENT_REQUIRED`, `00_german_unification.txt` est le seul
prochain audit sélectionné : ses cinq diagnostics frais sont homogènes, bornés
à cinq objets, et source hotfix comme vanilla 1.13 convergent sur la même
propriété racine. L'audit 6A.24 est seulement sélectionné ; il n'est pas
commencé et aucune correction n'est autorisée ici.

## 2. Préflight et protections

Le dépôt est sur `hotfix-dlc-audit`, au HEAD attendu, avec un arbre suivi et un
index propres. Aucun processus Victoria 3, Dowser ou launcher Paradox n'était
actif. Les huit non-suivis protégés n'ont pas été ouverts. Le stash
`NAVY-3C-3` reste en tête au hash
`518df704fa14599c0f254fae13859210663dd976`.

Les hashes gameplay restent :

| Fichier | SHA-256 |
|---|---|
| `common/journal_entries/03_afghanistan.txt` | `C9165714127E017486949AF8DDE742FD5A0E5F3093C5A43191695FE213969E13` |
| `common/journal_entries/00_poland.txt` | `A5EAF687DC6A736CD50D3C66E5E7601D29442FF3FA8A292C4EE751A7FF981E6A` |

## 3. Générations et méthode

Les diagnostics sont reconstruits depuis les enregistrements multi-lignes du
parser et les lignes `PostValidate`, puis dédupliqués par génération, message
normalisé, chemin et ligne.

| Génération | Segments | Diagnostics bruts | Dédupliqués | Chemins | Messages |
|---|---|---:|---:|---:|---:|
| fraîche 6A.22Q | `debug.1.log` + `debug.log` | 1 384 | 1 384 | 300 | 67 |
| précédente | `debug.3.log` + `debug.2.log` | 1 386 | 1 386 | 300 | 67 |
| rotations plus anciennes | `debug.5.log` + `debug.4.log` | 1 388 | 1 388 | 301 | 67 |

Dans la génération fraîche, le parser représente 612 identités sur 189 chemins
et 45 messages ; `PostValidate` représente 772 identités sur 157 chemins et 22
messages. La différence fraîche/précédente donne exactement 0 apparition, 2
disparitions et 1 384 identités inchangées. Deux identités supplémentaires,
les anciens pinning Pologne aux lignes 59 et 131, ne subsistent que dans les
rotations plus anciennes.

Les messages frais les plus nombreux sont :

| Message normalisé | Compte |
|---|---:|
| `has_role` PostValidate | 525 |
| `should_be_pinned_by_default` | 369 |
| `is_ruler` | 170 |
| `has_journal_entry` PostValidate | 79 |
| `has_template` PostValidate | 51 |
| `is_involved_in_journal_entry` PostValidate | 28 |
| `has_interest_marker_in_region` PostValidate | 23 |
| `add_journal_entry` PostValidate | 14 |
| `has_amendment` PostValidate | 13 |
| `is_building_type` PostValidate | 11 |

## 4. Afghanistan séparé et clos

Les deux seules disparitions sont :

```text
Unexpected token: should_be_pinned_by_default
common/journal_entries/03_afghanistan.txt:2
common/journal_entries/03_afghanistan.txt:1826
```

Les 17 identités restantes appartiennent toutes à
`je_consolidate_afghanistan` et portent sur
`has_interest_marker_in_region`, aux lignes 13, 101, 112, 126, 148, 166, 197,
208, 222, 244, 262, 286, 298, 318, 336, 443 et 461. Elles sont identiques dans
les trois générations et sont classées séparément :

```text
AFGHANISTAN_GREAT_GAME_REGIONAL_POSTVALIDATE_PREEXISTING
```

Elles ne sont ni causées par le correctif de pinning, ni une raison de rouvrir
celui-ci. Tout futur audit régional devra établir la sémantique 1.13 et rester
indépendant des frontières et de l'équilibrage Great Game.

## 5. Cohorte résiduelle 1.13

Le registre contient toujours exactement onze chemins :

| Chemin | Objets et lignes fraîches exactes | Frais / précédent / rotations | Trois voies, dépendances et traitement |
|---|---|---:|---|
| `00_canada_australia.txt` | `je_canada_can` 71 ; `je_canada_gbr` 161 ; `je_australia_aus` 206 ; `je_australia_gbr` 259 | 4 / 4 / 4 | quatre anciens pinning ; `ALL_THREE_DIFFER`, forme 1.13 source/vanilla convergente ; logique Canada/Australie et backlog Amériques protégés ; patch de propriétés potentiellement atomique mais audit et runtime futurs requis ; décision humaine requise |
| `00_fascism.txt` | `je_fascism_1` rôles 119/120/202 et pinning 281 ; `je_fascism_2` pinning 405 ; `je_modernization_program` pinning 476 ; `je_ethno_nationalist` rôles 489/490/507/508 | 10 / 10 / 10 | 3 anciens pinning + 7 `has_role` ; `ALL_THREE_DIFFER`, pinning source/vanilla convergent mais API mixte dans un même objet ; dépendances de rôles/personnages ; portée atomique non démontrée ; décision humaine et audit fonctionnel requis |
| `00_german_unification.txt` | `je_schleswig_holstein_question` 105 ; `je_german_unification_idea` 275 ; `je_north_german_unification` 333 ; `je_south_german_unification` 394 ; `je_german_unification` 447 | 5 / 5 / 5 | cinq anciens pinning uniquement ; `ALL_THREE_DIFFER`, propriété 1.13 racine identique dans source/vanilla ; deltas adjacents fonctionnels exclus, aucune collision protégée ; audit atomique possible sans choix de design ; runtime seulement après une éventuelle correction |
| `00_peoples_springtime_je.txt` | `je_springtime_of_the_peoples` rôles 195/196/296 et pinning 324 ; `je_red_summer` pinning 478 | 5 / 5 / 5 | 2 anciens pinning + 3 `has_role` ; `ALL_THREE_DIFFER`, API mixte ; personnages/rôles et future refonte France protégés ; patch non sélectionnable sans subdivision et décision humaine |
| `00_tutorial.txt` | 52 pinning aux lignes 2/77/131/195/257/332/338/374/430/518/569/607/631/646/656/662/695/732/756/762/846/969/986/1004/1010/1052/1085/1090/1103/1108/1121/1126/1158/1163/1210/1217/1227/1232/1250/1257/1373/1380/1489/1531/1546/1582/1588/1620/1639/1670/1697/1723 ; rôle 1144 | 53 / 53 / 53 | `ALL_THREE_DIFFER` ; au moins 40 objets, fonctions tutoriel hétérogènes et rôle mêlé à `je_tutorial_convoy_raiding` ; aucune portée atomique globale ; subdivision, décision humaine et runtime futurs requis |
| `02_gran_colombia.txt` | `je_gran_colombia` 72 ; `je_la_plata` 135 ; `je_andean_federation` 229 | 3 / 3 / 3 | trois anciens pinning ; `ALL_THREE_DIFFER`, forme source/vanilla convergente ; géographie et backlog Amériques protégés ; futur audit objet par objet requis, sans sélection automatique |
| `03_korea.txt` | `je_donghak_movement` 2 ; `je_gyojo_shinwon` 95 ; `je_korean_rebellion` pinning 186 et `is_ruler` 218/233/320/338 | 7 / 7 / 7 | 3 anciens pinning + 4 triggers inconnus ; `ALL_THREE_DIFFER`, API mixte au sein de la rébellion ; personnages/rôles et logique coréenne adjacente ; portée atomique non démontrée, décision humaine requise |
| `05_eastern_question.txt` | `je_eastern_question_russia` 130 ; `je_eastern_question_austria` 137 | 2 / 2 / 2 | deux anciens pinning ; `ALL_THREE_DIFFER`, forme source/vanilla convergente ; dépendance géopolitique Tanzimat/Question d'Orient protégée ; futur audit séparé et décision humaine requis |
| `06_portugal_politics.txt` | `je_devorismo` 177 ; `je_second_liberalism` 308 ; `je_portugal_regeneration` 515 ; `je_portugal_regeneration_public_works` 573 ; `je_portugal_regeneration_agriculture` 641 ; `je_portugal_regeneration_institutions` 688 | 6 / 6 / 6 | six anciens pinning ; `ALL_THREE_DIFFER`, forme source/vanilla convergente ; politique et flavor Ibérie custom protégés ; aucun audit automatique, décision humaine requise |
| `06_spanish_africa.txt` | `je_conquest_of_tetouan` 5 ; `je_western_saharan_conquest` 162 ; `je_guinean_conquest` 255 ; `je_moroccan_conquest` 342 | 4 / 4 / 4 | quatre anciens pinning ; `ALL_THREE_DIFFER`, forme source/vanilla convergente ; géographie et contenu Ibérie custom protégés ; aucun audit automatique, décision humaine requise |
| `07_poland_lithuania_mod.txt` | `je_plc_reform` 238 ; `je_plc_industry` 311 ; `je_plc_trade` 345 ; valeur inconnue 365 dans `je_plc_education`, pinning 390 ; `je_plc_railways` 440 ; `je_plc_farming` 510 ; `je_plc_military` 570 ; `je_plc_great_power` remove/add modifier 591/594 | 10 / 10 / 10 | 7 anciens pinning + 3 API custom ; `BOTH_CUSTOM_DIFFER`, vanilla absente ; Pologne-Lituanie custom protégée, dépendances fonctionnelles propres au fork ; aucune correction atomique globale ni sélection sans décision humaine |

Pour le tutoriel, les objets concernés sont précisément
`je_tutorial_expand_basic_building`, `je_tutorial_fix_budget_deficit`,
`je_tutorial_change_production_method`, `je_tutorial_expand_productive_building`,
`je_tutorial_fix_unproductive_building`, `je_tutorial_grow_gdp`,
`je_tutorial_promote_movement`, `je_tutorial_increase_market_access_by_decree`,
`je_tutorial_improve_market_access_with_railways`,
`je_tutorial_increase_immigration`, `je_tutorial_improve_supply_network`,
`je_tutorial_improve_consumer_goods_access`,
`je_tutorial_make_interest_group_happy`, `je_tutorial_enact_institution_law`,
`je_tutorial_invest_into_an_institution`, `je_tutorial_reform_government`,
`je_tutorial_increase_relations`, `je_tutorial_improve_rank`,
`je_tutorial_prevent_revolution`, `je_tutorial_earn_obligation`,
`je_tutorial_expand_military`, `je_tutorial_recruit_promote_commander`,
`je_tutorial_mobilize_army`, `je_tutorial_send_general_to_front`,
`je_tutorial_convoy_raiding`, `je_tutorial_recover_from_default`,
`je_tutorial_start_diplomatic_play`, `je_tutorial_is_play_target`,
`je_tutorial_capacity_deficit`, `je_tutorial_incorporate_state`,
`je_tutorial_declare_an_interest`, `je_tutorial_colonize_state`,
`je_tutorial_make_peace`, `je_tutorial_research_technology`,
`je_tutorial_create_formation`, `je_subject_liberty`,
`je_tutorial_foreign_investment`, `je_tutorial_establish_company`,
`je_tutorial_form_power_bloc` et `je_tutorial_lobbies`.

`03_afghanistan.txt` n'appartient plus à cette cohorte : il reste
`ALREADY_MERGED`, validé en statique et runtime, priorité `CLOSED`.

## 6. Revue trois voies des candidats admissibles

### Fascisme

Les trois pinning se trouvent dans `je_fascism_1`, `je_fascism_2` et
`je_modernization_program`. Le même fichier produit aussi sept diagnostics
`has_role` : trois dans `je_fascism_1` et quatre dans
`je_ethno_nationalist`. Le premier objet mélange donc deux familles d'API dans
le même périmètre fonctionnel. Malgré la convergence source/vanilla des
propriétés de pinning, ce fichier n'est pas sélectionné sans audit préalable
plus fin de ses rôles et dépendances.

### Unification allemande

Les cinq diagnostics `should_be_pinned_by_default` sont aux lignes actuelles
105, 275, 333, 394 et 447, à la racine de :

1. `je_schleswig_holstein_question` ;
2. `je_german_unification_idea` ;
3. `je_north_german_unification` ;
4. `je_south_german_unification` ;
5. `je_german_unification`.

Le fork contient cinq fois l'ancienne propriété avec valeur `yes`. La source
hotfix contient la forme 1.13 aux lignes 108, 196, 255, 317 et 371 ; la vanilla
1.13 la contient aux lignes 106, 277, 336, 398 et 452. Les trois versions la
placent à la racine des mêmes objets et source/vanilla convergent. Aucun autre
diagnostic parser ou `PostValidate` ne concerne ce fichier dans la génération
fraîche.

Les hashes comparés sont : fork
`A52D4525DED1BE8F804CEEDD99329E03EAABB9E53376D04F4BBE9A8CDC32EC22`,
source `38A42BBFAE01CBC32D42B9076C904A4D0CB65C3C2959F7F7C3ACA2271A7C66B8`
et vanilla `842D3205CAB766B681DED9BF53D3D17381DA5284CF5DC25EEAB9DE6803B0BF6F`.
Les hunks adjacents ne sont pas uniformes : Schleswig fork/vanilla
convergent, nord et sud source/vanilla convergent, l'idée diffère dans les
trois versions et le dernier objet est identique. Cette asymétrie interdit tout
remplacement intégral et impose un futur audit limité aux cinq propriétés.

## 7. Matrice P0/P1

| candidate_id | relative_path | objects | current_diagnostics | previous_generation_diagnostics | rotation_only_diagnostics | diagnostic_types | fork_vs_source | fork_vs_vanilla | source_vs_vanilla | static_invalidity | runtime_reproduced | atomic_scope | adjacent_functional_deltas | protected_collision | human_design_required | future_runtime_required | merge_blocker | confidence | recommended_treatment |
|---|---|---:|---:|---:|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `FASCISM_MIXED_JE_APIS` | `common/journal_entries/00_fascism.txt` | 4 | 10 | 10 | 0 | 3 pinning + 7 `has_role` | différent | différent | pinning convergent, rôles à auditer | prouvée pour le pinning | oui | non démontrée pour l'ensemble | rôles dans deux objets, dont un objet partagé | aucune connue | oui | à déterminer | oui | moyenne | différer et subdiviser |
| `GERMAN_UNIFICATION_FIVE_JE_PINNING` | `common/journal_entries/00_german_unification.txt` | 5 | 5 | 5 | 0 | pinning uniquement | différent | différent | convergent sur les cinq propriétés | prouvée | oui | cinq propriétés racine auditables | progression, visibilité, géographie, conditions, événements et effets exclus | aucune | non | oui après correction éventuelle | oui | élevée | sélectionner l'audit documentaire 6A.24 |

Les exclusions automatiques maintiennent tous les neuf autres chemins hors
sélection. Aucun P0 autonome n'est démontré. L'unification allemande est le P1
le mieux borné : signal homogène, syntaxe 1.13 démontrable, aucun choix de
design et aucune collision protégée.

## 8. Métadonnées

Le warning frais indiquant que la version de mod `1.12.5` ne correspond pas à
la version de jeu `1.13.0` vient de `.metadata/metadata.json` et reste classé
`METADATA_COMPATIBILITY_WARNING`. Il est non gameplay, non bloquant pour le
montage observé, et réservé à un futur audit de publication.

## 9. Phase suivante sélectionnée, non commencée

```text
HOTFIX_6A24_GERMAN_UNIFICATION_FIVE_JE_PINNING_1_13_ALIGNMENT_AUDIT
```

Cet audit devra rester en lecture seule, limité à
`common/journal_entries/00_german_unification.txt`, aux cinq objets nommés et
au seul type `should_be_pinned_by_default`. Il exclura explicitement
progression, visibilité, géographie, conditions, événements, effets et tout
remplacement de fichier. Il n'autorisera ni correction gameplay ni runtime.

```text
HOTFIX_6A23_POST_AFGHANISTAN_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE
POST_6A22Q_FRESH_DIAGNOSTICS_REINDEXED
AFGHANISTAN_TWO_JE_PINNING_BLOCK_REMAINS_CLOSED
POLAND_TWO_JE_PINNING_BLOCK_REMAINS_CLOSED
AFGHANISTAN_REGIONAL_POSTVALIDATE_DIAGNOSTICS_SEPARATED
RESIDUAL_VANILLA_1_13_ALIGNMENT_COHORT_REVIEWED
RESIDUAL_CURRENT_AND_ROTATION_ONLY_DIAGNOSTICS_SEPARATED
RESIDUAL_P0_P1_PRIORITY_MATRIX_COMPLETE
METADATA_1_12_5_WARNING_REMAINS_SEPARATE
NO_GAMEPLAY_CHANGED
NO_RUNTIME_REQUIRED
NO_AUTOMATIC_COMMIT
STASH_NAVY_3C_3_INTACT
GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES
NEXT_RESIDUAL_AUDIT_SELECTED
NEXT_EXECUTION_PHASE = HOTFIX_6A24_GERMAN_UNIFICATION_FIVE_JE_PINNING_1_13_ALIGNMENT_AUDIT
```
