# HOTFIX-6A.11 — Sélection du prochain résidu global

Date : 29 juillet 2026  
Branche : `hotfix-dlc-audit`  
HEAD initial : `01ed391` — `Align Romania journal entry pinning with Victoria 3 1.13`  
HEAD final : `01ed391` — aucun commit créé

## 1. Verdict

La phase documentaire est complète. Les 376 diagnostics de pinning encore
présents ont été recalculés dans 141 fichiers. Exactement trois candidats ont
été comparés et un seul est sélectionné :

`NEXT_EXECUTION_PHASE = HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT`

La future phase est limitée à deux substitutions d'API dans
`common/journal_entries/06_portuguese_colonialism.txt`. Aucune correction n'est
appliquée ici.

## 2. Préflight Git et processus

| Contrôle | Résultat |
| --- | --- |
| Racine | fork exact |
| Branche | `hotfix-dlc-audit` |
| Rapport 6A.10F et tous ses verdicts dans `HEAD` | PASS |
| 6A.10F commitée manuellement | PASS, commit `01ed391` |
| Fichiers suivis avant phase | propres |
| Index staged | vide |
| Non-suivis | uniquement `bject` et `docs/research/technology/` |
| Stash | `stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla` |
| Victoria 3, `dowser`, processus Paradox | absents |
| `git diff --check` initial | PASS |

Les interdictions Git ont été respectées : aucun reset, restore, checkout de
fichier, clean, merge, rebase, amend, commit, ni accès au contenu du stash.
Victoria 3 et le launcher n'ont été ni lancés ni pilotés.

## 3. Hashes de référence

| Preuve | SHA-256 | État |
| --- | --- | --- |
| Fork `00_romania.txt` corrigé | `DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578` | PASS |
| Source `00_romania.txt` | `74149D3A3B778732DE318D7FB522CE4255289B410F6184625BA9670E6CCCAB9A` | PASS |
| Vanilla `00_romania.txt` | `9B5C9A9D06DAA420030BBC3B31581CD030356145FD31E1589E590AB9DF904A51` | PASS |
| Fork `00_sick_man.txt` | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` | PASS |
| Histoire TUR fork | `81ABC8DEA9DE93EC6A4DD417FD05FD6859F3122758D2B27E712B1880013F9CA9` | PASS |
| Grande Crise orientale fork | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` | PASS |
| BIC fork | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` | PASS |

### 3.1 Éléments protégés

| Élément | SHA-256 | État |
| --- | --- | --- |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` | PASS |
| `TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv` | `315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5` | PASS |
| `TECH_TREE_INDUSTRIAL_CHAINS.md` | `88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410` | PASS |
| `TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md` | `0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596` | PASS |
| `TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv` | `01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D` | PASS |
| `TECH_TREE_RESEARCH_BIBLIOGRAPHY.md` | `C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5` | PASS |
| `TECH_TREE_RESOURCE_CANDIDATES.csv` | `6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A` | PASS |
| `TECH_TREE_VICTORIA3_GAP_ANALYSIS.md` | `150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA` | PASS |

## 4. Sources consultées intégralement

Les rapports 6A.10F, 6A.10, 6A.9F et 6A.9R, la roadmap, les deux
CSV de navigation, l'inventaire global, la réconciliation C1AI, les
changelogs complets du fork et de la source, ainsi que les nouveaux logs et
leurs rotations ont été lus en entier. La source hotfix et vanilla sont
restées en lecture seule.

Preuves des logs :

| Fichier | SHA-256 | Rôle |
| --- | --- | --- |
| `debug.1.log` | `A75AD954D9AA33D27B11BFDBB75A804F319555610F75266604E0565C4D5004E8` | baseline parser courante |
| `debug.2.log` | `38B2B29FAD0922C6192B27CB69BC202F0C431F1DC9FDF5427C3835EBFDD75C35` | montage |
| `debug.3.log` | `78068296E91D41EDE0BAEB6ED4E20FD4B8A2EC1E342E351C9E263D4D2F08030A` | rotation historique 6A.9F |

Dans `debug.2.log`, `dlc014_ip3` est monté ligne 80 et le chemin exact du fork
ligne 87. Les rotations historiques ne sont pas additionnées à la baseline.

## 5. Inventaire canonique après 6A.10F

| Catégorie exclusive | Lignes |
| --- | ---: |
| `REQUIRED_HOTFIX_DELTA` | 7 |
| `VANILLA_1_13_ALIGNMENT_REQUIRED` | 16 |
| `ALREADY_MERGED` | 18 |
| `INTENTIONAL_FORK_DIVERGENCE` | 3 |
| `OBSOLETE_HOTFIX_CONTENT` | 1 |
| `POST_MERGE_DESIGN_BACKLOG` | 10 |
| `PROTECTED_CONCURRENT_WORK` | 19 |
| `UNKNOWN_REQUIRES_REVIEW` | 87 |
| **Total** | **161** |

Chaque ligne appartient à une seule catégorie. Les lignes directement
exploitables sont `7 + 16 + 87 = 110`. Elles ne représentent pas 110
correctifs. L'ancien total de 26 deltas à haute confiance reste `UNVERIFIED`.

## 6. Baseline parser 6A.10F

Le message exact
`Unexpected token: should_be_pinned_by_default,` apparaît 376 fois dans
`debug.1.log`, réparti sur 141 chemins. Il reste 83 fichiers à une seule
erreur et 58 fichiers multi-objets; chacun de ces 58 fichiers porte aussi
plusieurs occurrences. `00_romania.txt` ne porte plus aucun de ces diagnostics
et aucune erreur ne rejette sa propriété moderne.

La différence avec la rotation 6A.9F est exactement la disparition des deux
occurrences de `00_romania.txt` : `378/142` devient `376/141`.

## 7. Top 25

| Rang | Chemin | Occurrences |
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

## 8. Liste exhaustive des 141 fichiers

Le manifeste ci-dessous est issu directement du regroupement de
`debug.1.log`. Les lignes gameplay et objets exacts sont inchangés par rapport
à la table exhaustive 6A.10, à la seule exception de la ligne
`common/journal_entries/00_romania.txt` (`76,149`,
`je_all_for_one, je_unite_the_principalities`), désormais absente. Cette
incorporation contrôlée conserve donc le regroupement exact par objet et par
ligne sans confondre la rotation historique.

| # | Chemin | Occ. | Statut 6A.10 |
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
| 57 | `common/journal_entries/06_portuguese_colonialism.txt` | 2 | VAI |
| 58 | `common/journal_entries/06_usa_independence_mod.txt` | 2 | PCW |
| 59 | `common/journal_entries/00_antarctica.txt` | 1 | IFD |
| 60 | `common/journal_entries/00_autocracy.txt` | 1 | IFD |
| 61 | `common/journal_entries/00_battle_for_india_mod.txt` | 1 | HI |
| 62 | `common/journal_entries/00_boxer_rebellion.txt` | 1 | IFD |
| 63 | `common/journal_entries/00_central_africa.txt` | 1 | IFD |
| 64 | `common/journal_entries/00_communism.txt` | 1 | IFD |
| 65 | `common/journal_entries/00_congo.txt` | 1 | IFD |
| 66 | `common/journal_entries/00_congo_free_state.txt` | 1 | IFD |
| 67 | `common/journal_entries/00_corn_laws.txt` | 1 | IFD |
| 68 | `common/journal_entries/00_east_indies.txt` | 1 | IFD |
| 69 | `common/journal_entries/00_establish_colonial_administration.txt` | 1 | IFD |
| 70 | `common/journal_entries/00_ethiopia.txt` | 1 | IFD |
| 71 | `common/journal_entries/00_grand_exhibition.txt` | 1 | IFD |
| 72 | `common/journal_entries/00_ig_agendas.txt` | 1 | IFD |
| 73 | `common/journal_entries/00_impose_law.txt` | 1 | IFD |
| 74 | `common/journal_entries/00_indian_removal.txt` | 1 | MSO |
| 75 | `common/journal_entries/00_krakatoa.txt` | 1 | MSO |
| 76 | `common/journal_entries/00_land_reclamation.txt` | 1 | IFD |
| 77 | `common/journal_entries/00_niger_river.txt` | 1 | IFD |
| 78 | `common/journal_entries/00_patagonia.txt` | 1 | IFD |
| 79 | `common/journal_entries/00_plague.txt` | 1 | IFD |
| 80 | `common/journal_entries/00_prohibition_laws.txt` | 1 | IFD |
| 81 | `common/journal_entries/00_red_scare.txt` | 1 | IFD |
| 82 | `common/journal_entries/00_request_recognition.txt` | 1 | IFD |
| 83 | `common/journal_entries/00_reunify_china.txt` | 1 | IFD |
| 84 | `common/journal_entries/00_scramble_for_africa.txt` | 1 | IFD |
| 85 | `common/journal_entries/00_seminole_wars.txt` | 1 | IFD |
| 86 | `common/journal_entries/00_standard_of_living.txt` | 1 | IFD |
| 87 | `common/journal_entries/00_strike_je.txt` | 1 | IFD |
| 88 | `common/journal_entries/00_suffragists.txt` | 1 | IFD |
| 89 | `common/journal_entries/00_turtle_island.txt` | 1 | IFD |
| 90 | `common/journal_entries/00_veiled_protectorate.txt` | 1 | IFD |
| 91 | `common/journal_entries/00_victoria.txt` | 1 | IFD |
| 92 | `common/journal_entries/00_warlord_china.txt` | 1 | IFD |
| 93 | `common/journal_entries/00_west_america.txt` | 1 | IFD |
| 94 | `common/journal_entries/01_coup.txt` | 1 | VAI |
| 95 | `common/journal_entries/01_dreyfus_affair.txt` | 1 | IFD |
| 96 | `common/journal_entries/01_hispaniola.txt` | 1 | IFD |
| 97 | `common/journal_entries/01_indochina.txt` | 1 | IFD |
| 98 | `common/journal_entries/01_krakow.txt` | 1 | IFD |
| 99 | `common/journal_entries/01_nihilism.txt` | 1 | IFD |
| 100 | `common/journal_entries/01_silkworm_diseases.txt` | 1 | IFD |
| 101 | `common/journal_entries/02_acre_dispute.txt` | 1 | IFD |
| 102 | `common/journal_entries/02_amazonas.txt` | 1 | IFD |
| 103 | `common/journal_entries/02_brazil_navy.txt` | 1 | IFD |
| 104 | `common/journal_entries/02_brazilian_nation_building.txt` | 1 | IFD |
| 105 | `common/journal_entries/02_caudillo.txt` | 1 | IFD |
| 106 | `common/journal_entries/02_cristo_redentor.txt` | 1 | IFD |
| 107 | `common/journal_entries/02_peru_bolivia.txt` | 1 | IFD |
| 108 | `common/journal_entries/02_positivism.txt` | 1 | IFD |
| 109 | `common/journal_entries/03_eastern_frontier.txt` | 1 | IFD |
| 110 | `common/journal_entries/03_tibetan_expedition.txt` | 1 | IFD |
| 111 | `common/journal_entries/04_communal_divides.txt` | 1 | IFD |
| 112 | `common/journal_entries/04_dravidian_movement.txt` | 1 | IFD |
| 113 | `common/journal_entries/04_imperialism_of_promise.txt` | 1 | VAI |
| 114 | `common/journal_entries/04_india_nationalism.txt` | 1 | MSO |
| 115 | `common/journal_entries/04_india_non_cooperation.txt` | 1 | MSO |
| 116 | `common/journal_entries/04_indian_famines.txt` | 1 | MSO |
| 117 | `common/journal_entries/04_indian_federation.txt` | 1 | MSO |
| 118 | `common/journal_entries/04_mughals.txt` | 1 | IFD |
| 119 | `common/journal_entries/04_princely_states.txt` | 1 | MSO |
| 120 | `common/journal_entries/04_sikh_empire.txt` | 1 | IFD |
| 121 | `common/journal_entries/04_victoria_terminus.txt` | 1 | IFD |
| 122 | `common/journal_entries/05_austrian_fascism.txt` | 1 | PCW |
| 123 | `common/journal_entries/05_bulgaria_je.txt` | 1 | IFD |
| 124 | `common/journal_entries/05_greece.txt` | 1 | IFD |
| 125 | `common/journal_entries/05_grunderzeit.txt` | 1 | IFD |
| 126 | `common/journal_entries/05_hungary_je.txt` | 1 | IFD |
| 127 | `common/journal_entries/05_hungry_forties.txt` | 1 | IFD |
| 128 | `common/journal_entries/05_metternich.txt` | 1 | PCW |
| 129 | `common/journal_entries/05_national_awakening_monument.txt` | 1 | IFD |
| 130 | `common/journal_entries/05_struggle_for_the_highveld.txt` | 1 | IFD |
| 131 | `common/journal_entries/05_technocracy.txt` | 1 | IFD |
| 132 | `common/journal_entries/05_the_grand_collapse.txt` | 1 | IFD |
| 133 | `common/journal_entries/06_dominican_content.txt` | 1 | IFD |
| 134 | `common/journal_entries/06_french_revolution_mod.txt` | 1 | HI |
| 135 | `common/journal_entries/06_language_policy.txt` | 1 | IFD |
| 136 | `common/journal_entries/06_morocco_lands_of_anarchy.txt` | 1 | IFD |
| 137 | `common/journal_entries/06_new_imperialism.txt` | 1 | IFD |
| 138 | `common/journal_entries/07_hindustan_is_durrani_mod.txt` | 1 | PCW |
| 139 | `common/journal_entries/07_iran_troubles_mod.txt` | 1 | HI |
| 140 | `common/journal_entries/07_irish_question_mod.txt` | 1 | HI |
| 141 | `common/journal_entries/99_test_global_je.txt` | 1 | IFD |

Contrôle de somme : les 141 lignes représentent exactement 376 occurrences.
Légende : `VAI` alignement vanilla 1.13, `IFD` divergence intentionnelle,
`PCW` travail protégé, `MSO` fusion statique close, `HI` hors inventaire.

## 9. Familles, protections et clôtures

- Tutoriels : 52 occurrences, portée massive, donc non atomique.
- Objectifs joueur : 44 occurrences dans quatre fichiers, overrides 1776
  intentionnels.
- Prestige goods : 16 occurrences, divergence fork intentionnelle.
- Russie : 12 occurrences, protection absolue.
- Autres journal entries vanilla : petits alignements possibles, à condition
  d'isoler toute dette adjacente.
- Extensions custom : pas d'autorisation sans preuve fonctionnelle.
- Hors inventaire : `00_battle_for_india_mod.txt`,
  `06_french_revolution_mod.txt`, `07_iran_troubles_mod.txt` et
  `07_irish_question_mod.txt`.
- Fichiers à erreur unique : 83. Fichiers multi-objets : 58.
- Les fichiers source/vanilla divergents ne sont pas sélectionnables sans
  justification fonctionnelle claire.

Les blocs Balkan National Awakening, Yugoslavia, Risorgimento, nationalisme
grec, Grande Crise orientale, les huit pinning Sick Man et les deux pinning
roumains restent clos. Les protections DEI/VOC, Java, NAVY, MARATH, Inde/BIC,
ADMIN, Japon, Russie, Autriche/Croatie/Suisse, révolutions américaine et
française, technologies et recherches sont intactes.

## 10. Diagnostics Tanzimat séparés

| ID | Diagnostic courant | Référence fork | Déclaration source/vanilla |
| --- | --- | --- | --- |
| `tanzimat_events.5` | lignes 3080–3081 de `debug.1.log` | `00_sick_man.txt:347`, pulse mensuel | `events/tanzimat_events.txt:458` |
| `tanzimat_events.9` | lignes 3084–3085 | `00_sick_man.txt:484`, pulse mensuel | `events/tanzimat_events.txt:985` |
| `tanzimat_events.10` | lignes 2924–2925 et 3082–3083 | `00_code_on_actions.txt:4375` et `00_sick_man.txt:436` | `events/tanzimat_events.txt:1094` |

Source et vanilla déclarent le namespace `tanzimat_events`; le fichier est
absent du fork. L'inventaire le classe `OBSOLETE_HOTFIX_CONTENT` parce que
vanilla est censé le fournir. Les références Sick Man appartiennent à une
chaîne désactivée en 1776, mais `.10` possède aussi une référence on-action.
Copier l'événement ou changer le `replace_path` ne constitue donc pas un
correctif autonome : cela pourrait réactiver du contenu Tanzimat. Ces
diagnostics restent dans
`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG` et ne sont pas
sélectionnés.

## 11. Analyses trois voies

### 11.1 Colonialisme portugais — sélectionné

Fichier : `common/journal_entries/06_portuguese_colonialism.txt`.

| Version | SHA-256 | Propriété |
| --- | --- | --- |
| Fork | `6FEF16A90E2E133CC82A912F40944E50E26B65FD524B5898086CF47557DA2894` | legacy aux lignes 6 et 181 |
| Source | `04CCCCF13E9D7B4EA1DBBB29F86861CA8B1DB7F77B635175A39D889B9234EE7A` | API moderne aux lignes 7 et 185 |
| Vanilla | `15834E8FE1DBA56ADD9D970F9CECDF8AD1FB45100585770A457DF96BDF65FDF4` | API moderne aux lignes 7 et 184 |

Les objets exacts sont `je_portuguese_colonialism` et `je_the_pink_map`.
Source et vanilla convergent exactement sur
`should_be_pinned_by_default_uninvolved_or_context = yes`. Les différences
adjacentes de source — régions stratégiques, visibilité culturelle et
géographique, prise en charge d'IBE dans le lobby — sont fonctionnelles et
explicitement exclues. Vanilla diffère également de la source sur
`geographic_region_iberia_old`, sans affecter la convergence de l'API.

La future correction fait exactement 2 suppressions, 2 additions, 2 objets et
2 hunks dans un fichier. Le hash futur reproductible, obtenu par les deux
seules substitutions et en conservant BOM et fins de ligne, est
`DB0B4CDC27B670F419D52148E6E5DF0C1D77CEA81BD9FD52115CAD27F1CCDB20`.
Les quatre clés de titre/raison existent en anglais et en français dans
vanilla IP4; aucune localisation ne sera modifiée. Aucun scope, rôle, tooltip,
trigger, visibilité, géographie, poids, transfert ou progression ne changera.
Compatibilité 1776 : oui, correction d'API indépendante du scénario.

Rollback : remplacer exactement les deux propriétés modernes par
`should_be_pinned_by_default = yes`. Runtime futur humain requis : un seul
lancement portugais condensé après tous les contrôles statiques, pour confirmer
les diagnostics ciblés `2 → 0`, l'absence de clé brute et l'absence d'anomalie
de visibilité/pinning.

### 11.2 Merchant Banking GEN/VEN — reporté

Fork GEN/VEN active `law_traditionalism` ligne 30 et conserve
`law_merchant_navy` ligne 26. La source active `law_merchant_banking` ligne 33,
mais retire la loi navale et ajoute un nom spécifique de propriétaires
terriens. Vanilla ne fournit aucun de ces deux fichiers. Le changelog 2.3
annonce explicitement Merchant Banking pour les républiques maritimes; la loi,
l'icône `merchant_banks.dds` et les localisations anglaise/française sont déjà
intégrées.

Une future correction sûre serait limitée à GEN et VEN, un objet pays et un
hunk par fichier : deux suppressions et deux additions. Elle préserverait
`law_merchant_navy`, n'importerait pas le nom des propriétaires terriens et ne
toucherait aucune autre loi. Hashes futurs déjà reproductibles :

- GEN : `7FC780AB8A8793E1DD1B3E6A32022807CED720FB1BE3F3D63D9EC6FDE9F43327`;
- VEN : `51A65341A2E3947A3D7D71BC3E3B1F31DA5CCD9D000D200C75BFB9570010B6DB`.

Rollback : restaurer seulement `law_traditionalism` dans les deux fichiers.
Runtime humain futur requis pour GEN et VEN. Ce delta P1 est reporté parce
qu'une erreur parser convergente P0 est prioritaire.

### 11.3 Navigation Acts — reporté pour audit

Les cinq fichiers exacts sont GBR, HBC, NBS, ONT et
`ora - oranje.txt`. Le fork active `law_mercantilism`; la source active
`law_mercantilism_navigation_acts`. Vanilla active `law_protectionism` pour
GBR et `law_mercantilism` pour les quatre autres. La loi, l'icône
`regulation_acts.dds`, les localisations anglaise/française et la preuve
changelog 2.3 existent.

Le futur delta annoncé serait 5 fichiers, 5 objets, 5 hunks, 5 suppressions et
5 additions. Toutefois source et vanilla divergent fonctionnellement, et GBR
est en collision avec la protection NAVY. BIC est exclu et conserve
`law_frontier_colonization`; `law_colonial_exploitation` ne doit jamais être
restaurée. Rollback théorique : restaurer les cinq seules lois commerciales
du fork. Un audit distinct puis un runtime humain seraient requis. Le candidat
n'est pas exécutable directement.

### 11.4 Petits alignements et inconnus pertinents

`01_coup.txt` a une erreur dans `je_ip4_coup`, mais les diffs adjacents portent
variables de localisation, cleanup, cooldown et invalidation; source et
vanilla divergent encore. `04_imperialism_of_promise.txt` a une erreur dans
`je_imperialism_of_promise`, mais les diffs adjacents touchent rôles de
personnage et tooltip bureaucratique, avec une divergence source/vanilla.
Ils sont donc écartés.

Les autres fichiers à une ou deux erreurs sont soit protégés, déjà fusionnés,
intentionnels, hors inventaire, massifs par dépendance, ou sans preuve
fonctionnelle suffisante. Aucun `UNKNOWN_REQUIRES_REVIEW` ne dépasse les trois
candidats retenus. Une différence de hash ou une occurrence parser isolée
n'est pas une autorisation.

## 12. Top 3 exact

| Rang | Phase candidate | Fichiers | Objets | Hunks | Priorité | Preuve | Collision | Runtime |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | `HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT` | 1 | 2 | 2 | P0 | 2 erreurs parser, convergence source/vanilla | aucune | humain, 1 lancement |
| 2 | `HOTFIX_6A12F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW` | 2 | 2 | 2 | P1 | changelog 2.3, loi et dépendances intégrées | aucune si exclusions respectées | humain, GEN/VEN |
| 3 | `HOTFIX_6A13R_NAVIGATION_ACTS_STARTING_LAW_AUDIT` | 5 | 5 | 5 | P1 | changelog 2.3, dépendances intégrées | GBR/NAVY et divergence vanilla | audit puis humain |

Exactement un candidat est sélectionné : le rang 1. Merchant Banking est
reporté derrière l'erreur d'API directe. Navigation Acts est reporté pour sa
collision et sa divergence trois voies.

## 13. Futur périmètre fermé

La phase 6A.11F pourra modifier uniquement :

1. `common/journal_entries/06_portuguese_colonialism.txt`;
2. son rapport canonique;
3. les cinq documents de navigation autorisés par son prompt.

Gameplay autorisé : remplacer ligne 6 dans `je_portuguese_colonialism` et
ligne 181 dans `je_the_pink_map`, chacune par l'API moderne exacte. Tous les
autres octets gameplay sont exclus. Aucun fichier complet ne sera remplacé.

Validations futures : hashes fork/source/vanilla, snapshot des deux anciennes
occurrences, diff `2/2` à deux hunks, hash futur exact, accolades, encodage,
localisations EN/FR et protections. Ensuite seulement, arrêt
`RUNTIME_OPERATOR_ACTION_REQUIRED`. Codex ne lancera ni ne pilotera le jeu.

## 14. Documents de phase

Les six seuls documents créés ou modifiés sont :

1. ce rapport;
2. `docs/reports/hotfix/INDEX.md`;
3. `HOTFIX_REPORT_INDEX.csv`;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv`;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun fichier gameplay, source hotfix, vanilla, BIC, fichier de recherche,
`bject` ou stash n'a été modifié.

## 15. Contrôles finaux et décision de commit

| Contrôle | Résultat |
| --- | --- |
| Gameplay modifié | 0 fichier, PASS |
| Documents de phase | exactement 6, PASS |
| Manifeste parser | 141 lignes, somme 376, PASS |
| Top 25 | 25 lignes, PASS |
| Candidats | exactement 3, PASS |
| Candidat sélectionné | exactement 1, PASS |
| Inventaire | 161, catégories exclusives, PASS |
| Lignes directement exploitables | 110, PASS |
| Diagnostics Tanzimat séparés | PASS |
| CSV | 22 et 17 colonnes, toutes les lignes lisibles, PASS |
| `git diff --check` | propre |
| Index staged | vide |
| BIC, `bject`, sept recherches | hashes inchangés |
| Source hotfix et vanilla | hashes inchangés |
| Stash NAVY-3C-3 | exact et intact |
| Victoria 3, `dowser`, Paradox | aucun processus |
| Jeu ou launcher lancé/piloté par Codex | non |

État Git final :

```txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/_index/HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
?? docs/research/technology/
```

Les seuls non-suivis hors rapport sont les éléments préexistants autorisés.
Le HEAD initial et final reste `01ed391`. Aucun commit automatique n'est créé.
La décision de commit appartient à l'opérateur humain.

## 16. Verdicts

`HOTFIX_6A11_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`  
`NO_GAMEPLAY_CHANGED`  
`GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`  
`NEXT_EXECUTION_PHASE = HOTFIX_6A11F_PORTUGUESE_COLONIALISM_TWO_JE_PINNING_1_13_ALIGNMENT`
