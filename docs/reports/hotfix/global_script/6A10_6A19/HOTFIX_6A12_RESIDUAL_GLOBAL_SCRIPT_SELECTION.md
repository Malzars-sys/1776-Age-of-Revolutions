# HOTFIX-6A.12 — Sélection du prochain résidu global

Date : 30 juillet 2026

Branche : `hotfix-dlc-audit`

HEAD initial : `6b069a8` — `Align Portuguese colonialism journal entry pinning with Victoria 3 1.13`

HEAD final : `6b069a8` — aucun commit créé

## 1. Verdict

La phase documentaire est complète. La baseline courante est recalculée à 374
diagnostics dans 140 fichiers. Exactement trois candidats sont publiés et un
seul est sélectionné :

`NEXT_EXECUTION_PHASE = HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT`

Le futur correctif remplace uniquement deux clés de régions stratégiques dans
`je_portuguese_colonialism`. Aucun gameplay n'est modifié pendant 6A.12.

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| Racine | fork exact |
| Branche | `hotfix-dlc-audit` |
| Rapport et verdicts 6A.11F dans `HEAD` | PASS |
| 6A.11F commitée manuellement | PASS, commit `6b069a8` |
| Worktree suivi initial | propre |
| Index staged | vide |
| Non-suivis | uniquement `bject` et `docs/research/technology/` |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Victoria 3, `dowser`, Paradox | aucun processus |
| `git diff --check` initial | propre |

État Git initial :

```txt
?? bject
?? docs/research/technology/
```

Aucune commande Git destructive, aucun accès au contenu du stash, aucun
lancement du jeu ou du launcher et aucun commit automatique n'ont été
effectués.

## 3. Hashes de référence et protections

| Preuve | SHA-256 | État |
| --- | --- | --- |
| Fork portugais corrigé | `DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20` | PASS |
| Source hotfix portugaise | `04CCCCF13E9D7B4EA1DBBB29F86861CA8B1DB7F77B635175A39D889B9234EE7A` | PASS |
| Vanilla portugaise | `15834E8FE1DBA56ADD9D970F9CECDF8AD1FB45100585770A457DF96BDF65FDF4` | PASS |
| Romania corrigée | `DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578` | PASS |
| Sick Man corrigé | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` | PASS |
| Grande Crise orientale | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` | PASS |
| BIC | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` | PASS |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` | PASS |

Les sept recherches technologiques portent exactement les hashes protégés
consignés dans 6A.11F :

- `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5`;
- `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410`;
- `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596`;
- `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D`;
- `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5`;
- `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A`;
- `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA`.

## 4. Logs, rotations et montage

| Log courant | SHA-256 |
| --- | --- |
| `debug.1.log` | `1F25D03EAE1B45C68A84BE77CC36F8D8F8CCD9F540104CA5D7CE52B1F1C3194B` |
| `debug.log` | `31E79BBDA56B49BA16E2F07800D39CB7C579B622FA68E5BB92C67976265B1298` |
| `error.log` | `1D761021E38CC35578BB273E1DD82E7665D6EE8011F2D25370592FA808D311C8` |
| `game.log` | `04C9BC554C4A34D045291D5CD830BBE8D606923AE03F4F71E002202B28550C99` |
| `system.log` | `CA73FC2FC88D7E720083742B3C673812614065C90C58A808DDB0EDB78D2CF34E` |

Rotations historiques, non additionnées aux résultats :

| Rotation | SHA-256 |
| --- | --- |
| `debug.2.log` | `72E998A9E079984DB6D93B24F1CD4E6B13F2755FF2640E81BA660A01DE417899` |
| `debug.3.log` | `A75AD954D9AA33D27B11BFDBB75A804F319555610F75266604E0565C4D5004E8` |
| `debug.4.log` | `38B2B29FAD0922C6192B27CB69BC202F0C431F1DC9FDF5427C3835EBFDD75C35` |
| `debug.5.log` | `78068296741B912AFC46A4E763ED393F35F7D00967E4F17EB98075BC8EB177F5` |

Dans `debug.1.log`, `dlc014_ip3` est monté ligne 80 et le fork exact ligne 87.

## 5. Sources consultées

Les rapports 6A.11F, 6A.11, 6A.10F, 6A.10, 6A.9F et 6A.9R, la roadmap,
les deux CSV de navigation, l'inventaire global, la réconciliation C1AI, les
changelogs complets, les logs et rotations, ainsi que les versions trois voies
des candidats sérieux ont été lus intégralement. Source et vanilla sont
restées en lecture seule.

## 6. Inventaire canonique après 6A.11F

La ligne physique de
`HOTFIX_GLOBAL_DIFFERENCE_INVENTORY.csv` reste historiquement
`PENDING_REVIEW`, mais son classement effectif dans la revue exhaustive 6A.11
était `VANILLA_1_13_ALIGNMENT_REQUIRED`. La fermeture 6A.11F la reclasse donc
exclusivement en `ALREADY_MERGED`.

| Catégorie exclusive | Lignes |
| --- | ---: |
| `REQUIRED_HOTFIX_DELTA` | 7 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 15 |
| `ALREADY_MERGED` | 19 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 |
| `PROTECTED_CONCURRENT_WORK` | 19 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 |
| **Total** | **161** |

Les lignes directement exploitables deviennent `7 + 15 + 87 = 109`. Elles ne
représentent pas 109 correctifs. Le total historique de 26 reste `UNVERIFIED`.

## 7. Baseline parser 6A.11F

`debug.1.log` contient 373 diagnostics dans 139 fichiers et `debug.log` une
occurrence supplémentaire dans `99_test_global_je.txt`. La somme courante est
exactement 374 diagnostics dans 140 fichiers.

- `06_portuguese_colonialism.txt` : 0;
- `00_romania.txt` : 0;
- `00_sick_man.txt` : 0;
- rejet de la propriété moderne portugaise : 0;
- fichiers à erreur unique : 83;
- fichiers multi-objets : 57.

La différence avec 6A.11 est exactement le retrait du fichier portugais et de
ses deux occurrences legacy : `376/141 → 374/140`.

## 8. Top 25

| Rang | Chemin | Occ. |
| ---: | --- | ---: |
| 1 | `common/journal_entries/00_tutorial.txt` | 52 |
| 2 | `common/journal_entries/00_player_objectives_great_game.txt` | 17 |
| 3 | `common/journal_entries/05_prestige_goods.txt` | 16 |
| 4 | `common/journal_entries/03_russia.txt` | 12 |
| 5 | `common/journal_entries/00_player_objectives_hegemon.txt` | 11 |
| 6 | `common/journal_entries/00_player_objectives_economic_dominance.txt` | 10 |
| 7 | `common/journal_entries/00_negotiation_quests_je.txt` | 7 |
| 8 | `common/journal_entries/06_economic_regeneration.txt` | 7 |
| 9 | `common/journal_entries/07_poland_lithuania_mod.txt` | 7 |
| 10 | `common/journal_entries/00_acw_entries.txt` | 6 |
| 11 | `common/journal_entries/00_meiji_restoration.txt` | 6 |
| 12 | `common/journal_entries/00_player_objectives_egalitarian_society.txt` | 6 |
| 13 | `common/journal_entries/06_portugal_politics.txt` | 6 |
| 14 | `common/journal_entries/00_german_unification.txt` | 5 |
| 15 | `common/journal_entries/05_montenegro_je.txt` | 5 |
| 16 | `common/journal_entries/06_iberian_twilight_monuments.txt` | 5 |
| 17 | `common/journal_entries/00_canada_australia.txt` | 4 |
| 18 | `common/journal_entries/00_canals.txt` | 4 |
| 19 | `common/journal_entries/00_central_and_south_america.txt` | 4 |
| 20 | `common/journal_entries/00_taiping.txt` | 4 |
| 21 | `common/journal_entries/00_trade_route_event_missions.txt` | 4 |
| 22 | `common/journal_entries/01_algeria.txt` | 4 |
| 23 | `common/journal_entries/02_paraguay.txt` | 4 |
| 24 | `common/journal_entries/03_lobbies.txt` | 4 |
| 25 | `common/journal_entries/04_india_british_dictates.txt` | 4 |

## 9. Liste exhaustive des 140 fichiers

Ce manifeste provient directement de la session courante. Les lignes gameplay,
objets et statuts sont identiques à la table exhaustive 6A.11, moins
`06_portuguese_colonialism.txt` (anciennes lignes 6 et 181, désormais closes).

| # | Chemin | Occ. | Statut |
| ---: | --- | ---: | --- |
| 1 | `common/journal_entries/00_tutorial.txt` | 52 | VAI |
| 2 | `common/journal_entries/00_player_objectives_great_game.txt` | 17 | IFD |
| 3 | `common/journal_entries/05_prestige_goods.txt` | 16 | IFD |
| 4 | `common/journal_entries/03_russia.txt` | 12 | IFD |
| 5 | `common/journal_entries/00_player_objectives_hegemon.txt` | 11 | IFD |
| 6 | `common/journal_entries/00_player_objectives_economic_dominance.txt` | 10 | IFD |
| 7 | `common/journal_entries/00_negotiation_quests_je.txt` | 7 | IFD |
| 8 | `common/journal_entries/06_economic_regeneration.txt` | 7 | IFD |
| 9 | `common/journal_entries/07_poland_lithuania_mod.txt` | 7 | PCW |
| 10 | `common/journal_entries/00_acw_entries.txt` | 6 | IFD |
| 11 | `common/journal_entries/00_meiji_restoration.txt` | 6 | MSO |
| 12 | `common/journal_entries/00_player_objectives_egalitarian_society.txt` | 6 | IFD |
| 13 | `common/journal_entries/06_portugal_politics.txt` | 6 | VAI |
| 14 | `common/journal_entries/00_german_unification.txt` | 5 | VAI |
| 15 | `common/journal_entries/05_montenegro_je.txt` | 5 | IFD |
| 16 | `common/journal_entries/06_iberian_twilight_monuments.txt` | 5 | IFD |
| 17 | `common/journal_entries/00_canada_australia.txt` | 4 | VAI |
| 18 | `common/journal_entries/00_canals.txt` | 4 | IFD |
| 19 | `common/journal_entries/00_central_and_south_america.txt` | 4 | IFD |
| 20 | `common/journal_entries/00_taiping.txt` | 4 | IFD |
| 21 | `common/journal_entries/00_trade_route_event_missions.txt` | 4 | IFD |
| 22 | `common/journal_entries/01_algeria.txt` | 4 | IFD |
| 23 | `common/journal_entries/02_paraguay.txt` | 4 | IFD |
| 24 | `common/journal_entries/03_lobbies.txt` | 4 | IFD |
| 25 | `common/journal_entries/04_india_british_dictates.txt` | 4 | MSO |
| 26 | `common/journal_entries/06_spanish_africa.txt` | 4 | VAI |
| 27 | `common/journal_entries/06_spanish_new_world.txt` | 4 | IFD |
| 28 | `common/journal_entries/00_fascism.txt` | 3 | VAI |
| 29 | `common/journal_entries/01_paris_commune.txt` | 3 | IFD |
| 30 | `common/journal_entries/02_gran_colombia.txt` | 3 | VAI |
| 31 | `common/journal_entries/02_pedro_brazil.txt` | 3 | IFD |
| 32 | `common/journal_entries/02_south_america_migration.txt` | 3 | IFD |
| 33 | `common/journal_entries/03_korea.txt` | 3 | VAI |
| 34 | `common/journal_entries/06_cuba.txt` | 3 | IFD |
| 35 | `common/journal_entries/06_philippines_je.txt` | 3 | IFD |
| 36 | `common/journal_entries/07_american_mod_jes.txt` | 3 | PCW |
| 37 | `common/journal_entries/00_alaska.txt` | 2 | IFD |
| 38 | `common/journal_entries/00_hawaii.txt` | 2 | IFD |
| 39 | `common/journal_entries/00_manifest_destiny.txt` | 2 | IFD |
| 40 | `common/journal_entries/00_opium_wars.txt` | 2 | IFD |
| 41 | `common/journal_entries/00_peoples_springtime_je.txt` | 2 | VAI |
| 42 | `common/journal_entries/00_poland.txt` | 2 | VAI |
| 43 | `common/journal_entries/00_skyscraper.txt` | 2 | IFD |
| 44 | `common/journal_entries/00_zanzibar.txt` | 2 | IFD |
| 45 | `common/journal_entries/01_french_monarchism.txt` | 2 | PCW |
| 46 | `common/journal_entries/01_natural_borders_of_france.txt` | 2 | IFD |
| 47 | `common/journal_entries/02_brazilian_slavery.txt` | 2 | IFD |
| 48 | `common/journal_entries/02_coffee_and_milk.txt` | 2 | IFD |
| 49 | `common/journal_entries/02_south_american_national_identity.txt` | 2 | PENDING_REVIEW |
| 50 | `common/journal_entries/02_vargas.txt` | 2 | IFD |
| 51 | `common/journal_entries/03_afghanistan.txt` | 2 | VAI |
| 52 | `common/journal_entries/04_india_home_rule.txt` | 2 | MSO |
| 53 | `common/journal_entries/05_austria_journal_entries.txt` | 2 | IFD |
| 54 | `common/journal_entries/05_balkan_wars.txt` | 2 | IFD |
| 55 | `common/journal_entries/05_danubian_federation.txt` | 2 | IFD |
| 56 | `common/journal_entries/05_eastern_question.txt` | 2 | VAI |
| 57 | `common/journal_entries/06_usa_independence_mod.txt` | 2 | PCW |
| 58 | `common/journal_entries/00_antarctica.txt` | 1 | IFD |
| 59 | `common/journal_entries/00_autocracy.txt` | 1 | IFD |
| 60 | `common/journal_entries/00_battle_for_india_mod.txt` | 1 | HI |
| 61 | `common/journal_entries/00_boxer_rebellion.txt` | 1 | IFD |
| 62 | `common/journal_entries/00_central_africa.txt` | 1 | IFD |
| 63 | `common/journal_entries/00_communism.txt` | 1 | IFD |
| 64 | `common/journal_entries/00_congo.txt` | 1 | IFD |
| 65 | `common/journal_entries/00_congo_free_state.txt` | 1 | IFD |
| 66 | `common/journal_entries/00_corn_laws.txt` | 1 | IFD |
| 67 | `common/journal_entries/00_east_indies.txt` | 1 | IFD |
| 68 | `common/journal_entries/00_establish_colonial_administration.txt` | 1 | IFD |
| 69 | `common/journal_entries/00_ethiopia.txt` | 1 | IFD |
| 70 | `common/journal_entries/00_grand_exhibition.txt` | 1 | IFD |
| 71 | `common/journal_entries/00_ig_agendas.txt` | 1 | IFD |
| 72 | `common/journal_entries/00_impose_law.txt` | 1 | IFD |
| 73 | `common/journal_entries/00_indian_removal.txt` | 1 | MSO |
| 74 | `common/journal_entries/00_krakatoa.txt` | 1 | MSO |
| 75 | `common/journal_entries/00_land_reclamation.txt` | 1 | IFD |
| 76 | `common/journal_entries/00_niger_river.txt` | 1 | IFD |
| 77 | `common/journal_entries/00_patagonia.txt` | 1 | IFD |
| 78 | `common/journal_entries/00_plague.txt` | 1 | IFD |
| 79 | `common/journal_entries/00_prohibition_laws.txt` | 1 | IFD |
| 80 | `common/journal_entries/00_red_scare.txt` | 1 | IFD |
| 81 | `common/journal_entries/00_request_recognition.txt` | 1 | IFD |
| 82 | `common/journal_entries/00_reunify_china.txt` | 1 | IFD |
| 83 | `common/journal_entries/00_scramble_for_africa.txt` | 1 | IFD |
| 84 | `common/journal_entries/00_seminole_wars.txt` | 1 | IFD |
| 85 | `common/journal_entries/00_standard_of_living.txt` | 1 | IFD |
| 86 | `common/journal_entries/00_strike_je.txt` | 1 | IFD |
| 87 | `common/journal_entries/00_suffragists.txt` | 1 | IFD |
| 88 | `common/journal_entries/00_turtle_island.txt` | 1 | IFD |
| 89 | `common/journal_entries/00_veiled_protectorate.txt` | 1 | IFD |
| 90 | `common/journal_entries/00_victoria.txt` | 1 | IFD |
| 91 | `common/journal_entries/00_warlord_china.txt` | 1 | IFD |
| 92 | `common/journal_entries/00_west_america.txt` | 1 | IFD |
| 93 | `common/journal_entries/01_coup.txt` | 1 | VAI |
| 94 | `common/journal_entries/01_dreyfus_affair.txt` | 1 | IFD |
| 95 | `common/journal_entries/01_hispaniola.txt` | 1 | IFD |
| 96 | `common/journal_entries/01_indochina.txt` | 1 | IFD |
| 97 | `common/journal_entries/01_krakow.txt` | 1 | IFD |
| 98 | `common/journal_entries/01_nihilism.txt` | 1 | IFD |
| 99 | `common/journal_entries/01_silkworm_diseases.txt` | 1 | IFD |
| 100 | `common/journal_entries/02_acre_dispute.txt` | 1 | IFD |
| 101 | `common/journal_entries/02_amazonas.txt` | 1 | IFD |
| 102 | `common/journal_entries/02_brazil_navy.txt` | 1 | IFD |
| 103 | `common/journal_entries/02_brazilian_nation_building.txt` | 1 | IFD |
| 104 | `common/journal_entries/02_caudillo.txt` | 1 | IFD |
| 105 | `common/journal_entries/02_cristo_redentor.txt` | 1 | IFD |
| 106 | `common/journal_entries/02_peru_bolivia.txt` | 1 | IFD |
| 107 | `common/journal_entries/02_positivism.txt` | 1 | IFD |
| 108 | `common/journal_entries/03_eastern_frontier.txt` | 1 | IFD |
| 109 | `common/journal_entries/03_tibetan_expedition.txt` | 1 | IFD |
| 110 | `common/journal_entries/04_communal_divides.txt` | 1 | IFD |
| 111 | `common/journal_entries/04_dravidian_movement.txt` | 1 | IFD |
| 112 | `common/journal_entries/04_imperialism_of_promise.txt` | 1 | VAI |
| 113 | `common/journal_entries/04_india_nationalism.txt` | 1 | MSO |
| 114 | `common/journal_entries/04_india_non_cooperation.txt` | 1 | MSO |
| 115 | `common/journal_entries/04_indian_famines.txt` | 1 | MSO |
| 116 | `common/journal_entries/04_indian_federation.txt` | 1 | MSO |
| 117 | `common/journal_entries/04_mughals.txt` | 1 | IFD |
| 118 | `common/journal_entries/04_princely_states.txt` | 1 | MSO |
| 119 | `common/journal_entries/04_sikh_empire.txt` | 1 | IFD |
| 120 | `common/journal_entries/04_victoria_terminus.txt` | 1 | IFD |
| 121 | `common/journal_entries/05_austrian_fascism.txt` | 1 | PCW |
| 122 | `common/journal_entries/05_bulgaria_je.txt` | 1 | IFD |
| 123 | `common/journal_entries/05_greece.txt` | 1 | IFD |
| 124 | `common/journal_entries/05_grunderzeit.txt` | 1 | IFD |
| 125 | `common/journal_entries/05_hungary_je.txt` | 1 | IFD |
| 126 | `common/journal_entries/05_hungry_forties.txt` | 1 | IFD |
| 127 | `common/journal_entries/05_metternich.txt` | 1 | PCW |
| 128 | `common/journal_entries/05_national_awakening_monument.txt` | 1 | IFD |
| 129 | `common/journal_entries/05_struggle_for_the_highveld.txt` | 1 | IFD |
| 130 | `common/journal_entries/05_technocracy.txt` | 1 | IFD |
| 131 | `common/journal_entries/05_the_grand_collapse.txt` | 1 | IFD |
| 132 | `common/journal_entries/06_dominican_content.txt` | 1 | IFD |
| 133 | `common/journal_entries/06_french_revolution_mod.txt` | 1 | HI |
| 134 | `common/journal_entries/06_language_policy.txt` | 1 | IFD |
| 135 | `common/journal_entries/06_morocco_lands_of_anarchy.txt` | 1 | IFD |
| 136 | `common/journal_entries/06_new_imperialism.txt` | 1 | IFD |
| 137 | `common/journal_entries/07_hindustan_is_durrani_mod.txt` | 1 | PCW |
| 138 | `common/journal_entries/07_iran_troubles_mod.txt` | 1 | HI |
| 139 | `common/journal_entries/07_irish_question_mod.txt` | 1 | HI |
| 140 | `common/journal_entries/99_test_global_je.txt` | 1 | IFD |

Contrôle de somme : 140 lignes et exactement 374 occurrences.

## 10. Familles, hors inventaire, protections et clôtures

- Tutoriel : 52 diagnostics et portée massive.
- Objectifs joueur : 44 diagnostics dans quatre overrides intentionnels.
- Prestige goods : 16 diagnostics intentionnels.
- Russie : 12 diagnostics protégés.
- Autres entrées vanilla : petits alignements possibles seulement après
  fermeture des dettes adjacentes.
- Hors inventaire : `00_battle_for_india_mod.txt`,
  `06_french_revolution_mod.txt`, `07_iran_troubles_mod.txt` et
  `07_irish_question_mod.txt`.
- Source/vanilla divergents : aucune sélection sans preuve fonctionnelle.

Balkan National Awakening, Yugoslavia, Risorgimento, nationalisme grec, Grande
Crise orientale, Sick Man, Romania et les deux pinning portugais restent clos.
Toutes les protections absolues restent exclues.

## 11. Dette des régions portugaises

### 11.1 Preuve moteur

`error.log` contient :

- 186 clés invalides `region_congo`, ligne gameplay 11;
- 186 clés invalides `region_zanj`, ligne gameplay 14;
- 373 retours `Event target link 'sr' returned an unset scope`.

Le bloc propriétaire est `immediate` de `je_portuguese_colonialism`.

### 11.2 Comparaison trois voies

| Version | Ligne ou bloc | Région ou effet |
| --- | --- | --- |
| Fork | 11 | `sr:region_congo` puis `save_scope_as = congo_scope` |
| Fork | 14 | `sr:region_zanj` puis `save_scope_as = zanj_scope` |
| Source | 12 et 15 | `sr:region_equatorial_africa`, `sr:region_east_africa` |
| Vanilla | 12 et 15 | mêmes deux régions modernes |

Le préfixe `sr:` exige un objet de type strategic region. Le fork et la source
n'embarquent aucun override `common/strategic_regions`; ils héritent donc de
vanilla. `region_congo` et `region_zanj` ne sont pas définis comme strategic
regions. Les occurrences homonymes dans `ai_strategies` sont des clés de
stratégie et non des objets `sr:`.

Vanilla définit dans
`common/strategic_regions/african_strategic_regions.txt` :

- `region_equatorial_africa`, lignes 24–29, incluant Congo et Angola;
- `region_east_africa`, lignes 38–43, incluant Mozambique et Afrique orientale.

Les scopes sauvegardés conservent leurs noms `congo_scope` et `zanj_scope`;
les raisons anglaise et française les utilisent pour afficher les deux noms
de régions. L'événement d'initiation et les événements créant
`je_the_pink_map` restent inchangés. Aucun usage direct de ces deux scopes
n'existe dans le bloc de la Carte rose.

### 11.3 Atomicité

Le correctif futur est autonome :

- un fichier;
- un objet;
- un hunk unifié, car les lignes 11 et 14 sont dans le même contexte;
- deux suppressions et deux additions;
- aucun fichier de localisation;
- aucun changement de pinning.

Les différences adjacentes `country_has_primary_culture`,
`geographic_region_iberia_old` et `c:IBE` ne sont pas nécessaires pour
résoudre les clés invalides et restent exclues. Compatibilité 1776 : les
régions modernes contiennent les États angolais et mozambicains utilisés par
l'entrée.

Hash actuel :
`DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20`.
Hash futur calculé sans écriture :
`99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126`.

Rollback exact : restaurer uniquement `sr:region_congo` et `sr:region_zanj`.
Runtime humain portugais requis pour prouver les trois familles d'erreurs à
zéro et l'affichage des noms de régions dans la raison.

## 12. Répétition « Royaume de Portugal »

La répétition visible ne provient pas du titre
`je_portuguese_colonialism`, correctement localisé en anglais et en français.
La condition utilise le trigger générique `has_law_or_variant`; sa clé
française exacte est `TRIGGER_HAS_LAW_OR_VARIANT_FIRST_NOT` dans
`triggers_l_french.yml:1101` :

```txt
[COUNTRY.GetAltNameNoFormatting('Le')|U][COUNTRY.GetNameNoFlag]
n’[COUNTRY.GetAltNameNoFormatting('AOnt')] pas promulgué...
```

Le fork et la source définissent le nom dynamique custom `dyn_c_portu_king`
comme « Royaume de Portugal » dans `NM_Countries_l_french.yml:46`. Vanilla ne
définit pas ce nom custom. L'interaction entre ce nom dynamique et les deux
substitutions grammaticales `Le`/`AOnt` renvoie plusieurs fois le nom complet.
La même famille apparaît dans le titre vanilla français
`je_urbanization_events_2`, ce qui confirme une dette systémique et non une
clé propre au journal portugais.

L'anglais générique utilise une seule fois `COUNTRY.GetNameNoFlag` et ne
présente pas cette construction. Aucun scripted localization propre au fichier
portugais ne pilote la phrase.

Un correctif autonome n'est pas prouvé : il faudrait soit surcharger une
localisation française générale protégée, soit corriger la grammaire du nom
dynamique custom avec un impact transversal. Nombre exact de fichiers et
rollback fonctionnel restent indéterminés. La répétition est donc reportée,
non combinée aux régions et sans modification de localisation.

## 13. Merchant Banking GEN/VEN

Le fork active `law_traditionalism` ligne 30 dans GEN et VEN, tout en
conservant `law_merchant_navy` ligne 26. La source active
`law_merchant_banking` ligne 33, retire la loi navale et ajoute un nom de
propriétaires terriens. Vanilla ne fournit aucun de ces deux fichiers.

La preuve fonctionnelle est le changelog 2.3 source : Merchant Banking pour
les républiques maritimes. La loi, `merchant_banks.dds` et les localisations
anglaise/française existent déjà dans le fork.

Futur périmètre sûr : deux fichiers, deux objets pays, deux hunks, deux
suppressions et deux additions. Préserver `law_merchant_navy`, ne pas importer
le nom des propriétaires terriens et ne toucher à aucune autre loi. Hashes
futurs :

- GEN : `7FC780AB8A8793E1DD1B3E6A32022807CED720FB1BE3F3D63D9EC6FDE9F43327`;
- VEN : `51A65341A2E3947A3D7D71BC3E3B1F31DA5CCD9D000D200C75BFB9570010B6DB`.

Rollback : restaurer `law_traditionalism` dans les deux fichiers. Runtime
humain GEN et VEN requis. Le candidat reste P1 derrière une erreur moteur
directe P0.

## 14. Navigation Acts

Les cinq fichiers sont GBR, HBC, NBS, ONT et `ora - oranje.txt`. Le fork
active `law_mercantilism`; la source active
`law_mercantilism_navigation_acts`. Vanilla active `law_protectionism` pour
GBR et `law_mercantilism` pour les quatre autres.

La loi, l'icône `regulation_acts.dds`, les localisations anglaise/française et
le changelog 2.3 existent. Le delta théorique compte cinq fichiers, cinq
objets, cinq hunks, cinq suppressions et cinq additions. Source et vanilla
divergent cependant fonctionnellement et GBR reste en collision NAVY. BIC est
exclu et conserve `law_frontier_colonization`.

Rollback théorique : restaurer les cinq lois commerciales actuelles. Un audit
distinct puis un runtime humain sont requis; aucune correction immédiate n'est
autorisée.

## 15. Coup et Imperialism of Promise

`01_coup.txt` porte une erreur dans `je_ip4_coup`; source et vanilla
convergent sur la propriété moderne, mais les différences adjacentes touchent
variables de localisation, cleanup, cooldown et invalidation, avec divergence
source/vanilla.

`04_imperialism_of_promise.txt` porte une erreur dans
`je_imperialism_of_promise`; les différences adjacentes touchent rôles de
personnage et tooltip bureaucratique, avec divergence source/vanilla sur le
rôle de chef de groupe d'intérêt.

Ces deux petits alignements sont reportés : leurs dettes fonctionnelles ne sont
pas closes et 6A.12 ne les transforme pas en corrections isolées.

## 16. Tanzimat

La session courante reproduit séparément :

- `tanzimat_events.10`, `debug.1.log:3289–3290`, référence on-action fork
  `00_code_on_actions.txt:4375`;
- `.5`, lignes 3445–3446, référence Sick Man ligne 347;
- `.10`, lignes 3447–3448, référence Sick Man ligne 436;
- `.9`, lignes 3449–3450, référence Sick Man ligne 484.

Source et vanilla déclarent les événements aux lignes 458, 985 et 1094 de
`events/tanzimat_events.txt`; le fork ne porte pas le fichier et la ligne
d'inventaire est classée `OBSOLETE_HOTFIX_CONTENT` parce que vanilla est censé
le fournir. La chaîne Sick Man reste inactive en 1776, mais `.10` possède une
référence on-action. Copier le fichier ou changer l'héritage pourrait donc
réactiver Tanzimat. Aucun correctif autonome n'est sélectionné et
`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG` est conservé.

## 17. Inconnus pertinents

Les 87 inconnus restent examinables uniquement sur preuve précise. Aucun
inconnu ne présente ici une preuve plus forte, un périmètre plus court et
moins de dépendances que les régions portugaises. Une différence de hash ou
une occurrence parser seule ne constitue pas une autorisation.

## 18. Top 3 exact

| Rang | Phase candidate | Fichiers | Objets | Hunks | Priorité | Preuve | Collision | Runtime |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | `HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT` | 1 | 1 | 1 | P0 | 745 diagnostics moteur associés; convergence source/vanilla | aucune | humain Portugal |
| 2 | `HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW` | 2 | 2 | 2 | P1 | changelog 2.3 et dépendances intégrées | aucune avec exclusions | humain GEN/VEN |
| 3 | `HOTFIX_6A14R_NAVIGATION_ACTS_STARTING_LAW_AUDIT` | 5 | 5 | 5 | P1 | changelog 2.3 et dépendances intégrées | GBR/NAVY; divergence vanilla | audit puis humain |

Exactement un candidat est sélectionné : le rang 1. Merchant Banking est
reporté derrière l'erreur moteur directe. Navigation Acts est reporté pour
audit. La répétition du nom, Coup, Imperialism et Tanzimat ne disposent pas
d'un périmètre autonome prouvé.

## 19. Futur périmètre fermé

La phase 6A.12F pourra modifier uniquement :

1. `common/journal_entries/06_portuguese_colonialism.txt`;
2. son rapport;
3. les quatre documents de navigation autorisés par son prompt.

Dans `je_portuguese_colonialism`, un seul hunk :

```diff
-        sr:region_congo = {
+        sr:region_equatorial_africa = {
             save_scope_as = congo_scope
         }
-        sr:region_zanj = {
+        sr:region_east_africa = {
             save_scope_as = zanj_scope
         }
```

Diff attendu : un fichier, un objet, un hunk unifié, `2/2`. Les deux
propriétés modernes de pinning, les filtres culturel/géographique, `c:IBE`,
les événements et toutes les localisations sont exclus.

Rollback : restaurer seulement `region_congo` et `region_zanj`, avec retour au
hash `DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20`.
Hash futur attendu :
`99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126`.

Après tous les contrôles statiques, un runtime humain portugais condensé est
requis. Codex devra s'arrêter avec `RUNTIME_OPERATOR_ACTION_REQUIRED`.

## 20. Documents de phase et contrôles

Les six seuls documents créés ou modifiés sont :

1. ce rapport;
2. `docs/reports/hotfix/INDEX.md`;
3. `HOTFIX_REPORT_INDEX.csv`;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv`;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun gameplay, source hotfix, vanilla, BIC, fichier de recherche, `bject` ou
stash n'est modifié. Les contrôles finaux vérifient les CSV, le nombre exact
de candidats, le manifeste `140/374`, les hashes, le périmètre, l'index staged,
les processus et `git diff --check`.

## 21. Décision de commit et verdicts

Le HEAD initial et final reste `6b069a8`. Aucun commit automatique n'est créé.
La décision de commit appartient à l'opérateur humain.

- `HOTFIX_6A12_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_SELECTED`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A12F_PORTUGUESE_COLONIALISM_STRATEGIC_REGION_KEYS_1_13_ALIGNMENT`
