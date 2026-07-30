# HOTFIX-6A.13 — Sélection du prochain résidu global

Date : 30 juillet 2026

Phase : `HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION`

Branche : `hotfix-dlc-audit`

HEAD initial et final : `7ba4785dfa53813c2765c2356c09c2ec28b7b6a6` —
`Align Portuguese colonialism strategic regions with Victoria 3 1.13`

## 1. Verdict

La revue documentaire est complète. Exactement trois candidats sont publiés et
un seul est sélectionné :

`NEXT_EXECUTION_PHASE = HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW`

La future correction remplacera uniquement la loi économique initiale
`law_traditionalism` par `law_merchant_banking` dans GEN et VEN. Elle
préservera `law_merchant_navy`, toutes les autres lois et le nom des
propriétaires terriens. Aucun gameplay n'est modifié pendant 6A.13.

## 2. Préflight

| Contrôle | Résultat |
| --- | --- |
| Racine | fork exact |
| Branche | `hotfix-dlc-audit` |
| HEAD | `7ba4785` |
| Rapport 6A.12F dans `HEAD` | PASS |
| Huit verdicts d'entrée dans `HEAD` | PASS |
| 6A.12F commitée manuellement | PASS |
| Fichiers suivis | propres |
| Index staged | vide |
| Non-suivis | uniquement `bject` et sept recherches technologiques |
| Stash | ligne unique exacte |
| Victoria 3, `dowser`, Paradox | aucun processus |
| `git diff --check` | propre |

Le stash est :

```txt
stash@{0}: On hotfix-dlc-audit: WIP NAVY-3C-3 Maratha Konkan Flotilla
```

État Git initial :

```txt
?? bject
?? docs/research/technology/TECH_TREE_BUILDING_AND_PRODUCTION_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_INDUSTRIAL_CHAINS.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_HISTORY_DEEP_RESEARCH.md
?? docs/research/technology/TECH_TREE_INDUSTRIAL_INNOVATIONS_DATABASE.csv
?? docs/research/technology/TECH_TREE_RESEARCH_BIBLIOGRAPHY.md
?? docs/research/technology/TECH_TREE_RESOURCE_CANDIDATES.csv
?? docs/research/technology/TECH_TREE_VICTORIA3_GAP_ANALYSIS.md
```

Aucune commande Git destructive, aucun accès au contenu du stash, aucun
runtime et aucun commit automatique n'ont été effectués.

## 3. Hashes de référence et protections

| Preuve | SHA-256 | État |
| --- | --- | --- |
| Fork portugais final | `99DB30D8078C39930B82E79242D70CD70DB422BA148DB2D655E1A534E5DDF126` | PASS |
| Source portugaise | `04CCCCF13E9D7B4EA1DBBB29F86861CA8B1DB7F77B635175A39D889B9234EE7A` | PASS |
| Vanilla portugaise | `15834E8FE1DBA56ADD9D970F9CECDF8AD1FB45100585770A457DF96BDF65FDF4` | PASS |
| Romania | `DEE084181C30A4DD72D85132F50EF725B654ACA70E22AA30E851FF7D743DE578` | PASS |
| Sick Man | `B04C07388C944E5DA74CFCE142599797F582EA809412B9690170735BFA17B04A` | PASS |
| Grande Crise orientale | `96F65E2B3CC7129DD8D4AD41382F9F8DD97FB5FA24C66C05F129B1E31615F75A` | PASS |
| BIC | `37B836DBE9A273F1202B592533EB8C851B3657DBB63422F50AE11021437F580C` | PASS |
| `bject` | `A6D3772BDFBFA8E9987DE8753D52079062AAC7F3277FEE22C338AA4AF2D6171B` | PASS |

Les sept hashes technologiques sont respectivement :

`315CB857B94D547492E1F7C36E10A67EF53DBCBDA0FF63CBA4246DBA7B6FC6D5`,
`88D090A496C1C3CDB8A04D24AA2E31369E6AB6FAD843052CBE4C26467F4AA410`,
`0FE06A1843F5B67413E222ECFDABBF4E6957EAA2E97D466A018C59FA27DA4596`,
`01A37C0BD8BE839EC59E11AA4742CB4D96824EEAFCEA94979839391D8798094D`,
`C4EF474D8C1502DBC1D36A9D52473EE4B5E41C3D14A2081F1A526B9383FF1AF5`,
`6E7A48765FB9C20A4F8992D1CCD32BB75340A7BD6FC00B365E503F930BFD8F9A`
et
`150256D3C56333CAF8C37A7631074110060678FC115DB24FC48F702DFD6840FA`.
Tous sont conformes.

## 4. Sources et logs

Les rapports 6A.12F, 6A.12, 6A.11F, 6A.11, 6A.10F, 6A.9F et
6A.9R, la roadmap, les deux CSV de navigation, l'inventaire global, la
réconciliation C1AI, les changelogs complets du fork et de la source, les logs
et rotations 6A.12F et les versions trois voies des candidats sérieux ont été
lus intégralement.

La session 6A.12F courante est portée par :

| Log | SHA-256 |
| --- | --- |
| `debug.1.log` | `A32A481753B631F757BC5A1A653DF34AC8F87261A91FE116A31F1C32E94757FD` |
| `debug.log` | `CC6C1C8E19DD564DBDA8FAC7BC9357338CB60F4E91441C71DE6FF57D15342C15` |
| `error.log` | `B59CAC5F9347290AB7D3EEC8C7DC8D62D78C43C6A48F97663F46F2664BDEAC60` |
| `game.log` | `D649F3E990F72FD273F2269E536AB46FF0E297DCE811A8C462FE39DEB10A816F` |
| `system.log` | `06EB548ED07E5F4FFB497897FAF62D3B7948F91B5A1774E3C6F74F942EE32867` |

Les rotations `error.1` à `.5` et `game.1` à `.5` appartiennent à la même
session. `debug.2` à `.5` et `system.1` sont des rotations historiques
identifiées par les hashes publiés dans 6A.12F et ne sont pas additionnées.
Aucun nouveau log n'a été produit.

## 5. Baseline canonique recalculée

La lecture directe de `debug.1.log` et `debug.log` donne :

| Mesure | Résultat |
| --- | ---: |
| `Unexpected token: should_be_pinned_by_default,` | 374 |
| Fichiers uniques | 140 |
| Fichiers à une erreur | 83 |
| Fichiers multi-objets | 57 |
| `06_portuguese_colonialism.txt` | 0 |
| `00_romania.txt` | 0 |
| `00_sick_man.txt` | 0 |
| Rejet du pinning moderne portugais | 0 |
| `region_congo` ciblé portugais | 0 |
| `region_zanj` ciblé portugais | 0 |
| Scope `sr` associé | 0 |

Les deux tokens homonymes restants sont exclusivement dans
`common/ai_strategies/00_default_strategy.txt`; ils ne sont pas des objets
strategic region portugais.

## 6. Liste exhaustive et top 25

La table est classée par nombre décroissant. Ses lignes 1 à 25 constituent le
top 25 exact; les lignes 1 à 57 sont les fichiers multi-objets et les lignes
58 à 140 les 83 fichiers à erreur unique.

| # | Fichier | Occ. |
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
| 26 | `common/journal_entries/06_spanish_africa.txt` | 4 |
| 27 | `common/journal_entries/06_spanish_new_world.txt` | 4 |
| 28 | `common/journal_entries/00_fascism.txt` | 3 |
| 29 | `common/journal_entries/01_paris_commune.txt` | 3 |
| 30 | `common/journal_entries/02_gran_colombia.txt` | 3 |
| 31 | `common/journal_entries/02_pedro_brazil.txt` | 3 |
| 32 | `common/journal_entries/02_south_america_migration.txt` | 3 |
| 33 | `common/journal_entries/03_korea.txt` | 3 |
| 34 | `common/journal_entries/06_cuba.txt` | 3 |
| 35 | `common/journal_entries/06_philippines_je.txt` | 3 |
| 36 | `common/journal_entries/07_american_mod_jes.txt` | 3 |
| 37 | `common/journal_entries/00_alaska.txt` | 2 |
| 38 | `common/journal_entries/00_hawaii.txt` | 2 |
| 39 | `common/journal_entries/00_manifest_destiny.txt` | 2 |
| 40 | `common/journal_entries/00_opium_wars.txt` | 2 |
| 41 | `common/journal_entries/00_peoples_springtime_je.txt` | 2 |
| 42 | `common/journal_entries/00_poland.txt` | 2 |
| 43 | `common/journal_entries/00_skyscraper.txt` | 2 |
| 44 | `common/journal_entries/00_zanzibar.txt` | 2 |
| 45 | `common/journal_entries/01_french_monarchism.txt` | 2 |
| 46 | `common/journal_entries/01_natural_borders_of_france.txt` | 2 |
| 47 | `common/journal_entries/02_brazilian_slavery.txt` | 2 |
| 48 | `common/journal_entries/02_coffee_and_milk.txt` | 2 |
| 49 | `common/journal_entries/02_south_american_national_identity.txt` | 2 |
| 50 | `common/journal_entries/02_vargas.txt` | 2 |
| 51 | `common/journal_entries/03_afghanistan.txt` | 2 |
| 52 | `common/journal_entries/04_india_home_rule.txt` | 2 |
| 53 | `common/journal_entries/05_austria_journal_entries.txt` | 2 |
| 54 | `common/journal_entries/05_balkan_wars.txt` | 2 |
| 55 | `common/journal_entries/05_danubian_federation.txt` | 2 |
| 56 | `common/journal_entries/05_eastern_question.txt` | 2 |
| 57 | `common/journal_entries/06_usa_independence_mod.txt` | 2 |
| 58 | `common/journal_entries/00_antarctica.txt` | 1 |
| 59 | `common/journal_entries/00_autocracy.txt` | 1 |
| 60 | `common/journal_entries/00_battle_for_india_mod.txt` | 1 |
| 61 | `common/journal_entries/00_boxer_rebellion.txt` | 1 |
| 62 | `common/journal_entries/00_central_africa.txt` | 1 |
| 63 | `common/journal_entries/00_communism.txt` | 1 |
| 64 | `common/journal_entries/00_congo.txt` | 1 |
| 65 | `common/journal_entries/00_congo_free_state.txt` | 1 |
| 66 | `common/journal_entries/00_corn_laws.txt` | 1 |
| 67 | `common/journal_entries/00_east_indies.txt` | 1 |
| 68 | `common/journal_entries/00_establish_colonial_administration.txt` | 1 |
| 69 | `common/journal_entries/00_ethiopia.txt` | 1 |
| 70 | `common/journal_entries/00_grand_exhibition.txt` | 1 |
| 71 | `common/journal_entries/00_ig_agendas.txt` | 1 |
| 72 | `common/journal_entries/00_impose_law.txt` | 1 |
| 73 | `common/journal_entries/00_indian_removal.txt` | 1 |
| 74 | `common/journal_entries/00_krakatoa.txt` | 1 |
| 75 | `common/journal_entries/00_land_reclamation.txt` | 1 |
| 76 | `common/journal_entries/00_niger_river.txt` | 1 |
| 77 | `common/journal_entries/00_patagonia.txt` | 1 |
| 78 | `common/journal_entries/00_plague.txt` | 1 |
| 79 | `common/journal_entries/00_prohibition_laws.txt` | 1 |
| 80 | `common/journal_entries/00_red_scare.txt` | 1 |
| 81 | `common/journal_entries/00_request_recognition.txt` | 1 |
| 82 | `common/journal_entries/00_reunify_china.txt` | 1 |
| 83 | `common/journal_entries/00_scramble_for_africa.txt` | 1 |
| 84 | `common/journal_entries/00_seminole_wars.txt` | 1 |
| 85 | `common/journal_entries/00_standard_of_living.txt` | 1 |
| 86 | `common/journal_entries/00_strike_je.txt` | 1 |
| 87 | `common/journal_entries/00_suffragists.txt` | 1 |
| 88 | `common/journal_entries/00_turtle_island.txt` | 1 |
| 89 | `common/journal_entries/00_veiled_protectorate.txt` | 1 |
| 90 | `common/journal_entries/00_victoria.txt` | 1 |
| 91 | `common/journal_entries/00_warlord_china.txt` | 1 |
| 92 | `common/journal_entries/00_west_america.txt` | 1 |
| 93 | `common/journal_entries/01_coup.txt` | 1 |
| 94 | `common/journal_entries/01_dreyfus_affair.txt` | 1 |
| 95 | `common/journal_entries/01_hispaniola.txt` | 1 |
| 96 | `common/journal_entries/01_indochina.txt` | 1 |
| 97 | `common/journal_entries/01_krakow.txt` | 1 |
| 98 | `common/journal_entries/01_nihilism.txt` | 1 |
| 99 | `common/journal_entries/01_silkworm_diseases.txt` | 1 |
| 100 | `common/journal_entries/02_acre_dispute.txt` | 1 |
| 101 | `common/journal_entries/02_amazonas.txt` | 1 |
| 102 | `common/journal_entries/02_brazil_navy.txt` | 1 |
| 103 | `common/journal_entries/02_brazilian_nation_building.txt` | 1 |
| 104 | `common/journal_entries/02_caudillo.txt` | 1 |
| 105 | `common/journal_entries/02_cristo_redentor.txt` | 1 |
| 106 | `common/journal_entries/02_peru_bolivia.txt` | 1 |
| 107 | `common/journal_entries/02_positivism.txt` | 1 |
| 108 | `common/journal_entries/03_eastern_frontier.txt` | 1 |
| 109 | `common/journal_entries/03_tibetan_expedition.txt` | 1 |
| 110 | `common/journal_entries/04_communal_divides.txt` | 1 |
| 111 | `common/journal_entries/04_dravidian_movement.txt` | 1 |
| 112 | `common/journal_entries/04_imperialism_of_promise.txt` | 1 |
| 113 | `common/journal_entries/04_india_nationalism.txt` | 1 |
| 114 | `common/journal_entries/04_india_non_cooperation.txt` | 1 |
| 115 | `common/journal_entries/04_indian_famines.txt` | 1 |
| 116 | `common/journal_entries/04_indian_federation.txt` | 1 |
| 117 | `common/journal_entries/04_mughals.txt` | 1 |
| 118 | `common/journal_entries/04_princely_states.txt` | 1 |
| 119 | `common/journal_entries/04_sikh_empire.txt` | 1 |
| 120 | `common/journal_entries/04_victoria_terminus.txt` | 1 |
| 121 | `common/journal_entries/05_austrian_fascism.txt` | 1 |
| 122 | `common/journal_entries/05_bulgaria_je.txt` | 1 |
| 123 | `common/journal_entries/05_greece.txt` | 1 |
| 124 | `common/journal_entries/05_grunderzeit.txt` | 1 |
| 125 | `common/journal_entries/05_hungary_je.txt` | 1 |
| 126 | `common/journal_entries/05_hungry_forties.txt` | 1 |
| 127 | `common/journal_entries/05_metternich.txt` | 1 |
| 128 | `common/journal_entries/05_national_awakening_monument.txt` | 1 |
| 129 | `common/journal_entries/05_struggle_for_the_highveld.txt` | 1 |
| 130 | `common/journal_entries/05_technocracy.txt` | 1 |
| 131 | `common/journal_entries/05_the_grand_collapse.txt` | 1 |
| 132 | `common/journal_entries/06_dominican_content.txt` | 1 |
| 133 | `common/journal_entries/06_french_revolution_mod.txt` | 1 |
| 134 | `common/journal_entries/06_language_policy.txt` | 1 |
| 135 | `common/journal_entries/06_morocco_lands_of_anarchy.txt` | 1 |
| 136 | `common/journal_entries/06_new_imperialism.txt` | 1 |
| 137 | `common/journal_entries/07_hindustan_is_durrani_mod.txt` | 1 |
| 138 | `common/journal_entries/07_iran_troubles_mod.txt` | 1 |
| 139 | `common/journal_entries/07_irish_question_mod.txt` | 1 |
| 140 | `common/journal_entries/99_test_global_je.txt` | 1 |

Contrôle de somme : 374 occurrences dans 140 fichiers.

## 7. Familles, hors inventaire et divergences

- Tutoriel : 52 diagnostics, périmètre massif.
- Objectifs joueur : 44 diagnostics, overrides intentionnels.
- Prestige goods : 16, divergence intentionnelle.
- Russie : 12, protégée.
- Fichiers à erreur unique : 83, sans autorisation automatique.
- Fichiers multi-objets : 57.
- Hors inventaire : `00_battle_for_india_mod.txt`,
  `06_french_revolution_mod.txt`, `07_iran_troubles_mod.txt` et
  `07_irish_question_mod.txt`.
- Source/vanilla divergents : Coup, Imperialism of Promise, GBR et plusieurs
  petits fichiers; aucune sélection sans dette fonctionnelle close.

## 8. Inventaire canonique

La répartition effective des 161 anciennes lignes reste :

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

Les lignes directement exploitables restent `7 + 15 + 87 = 109`. Elles ne
représentent pas 109 correctifs. Le total historique de 26 deltas à haute
confiance reste `UNVERIFIED`.

La ligne physique portugaise est historiquement `PENDING_REVIEW`, mais son
classement effectif était déjà `ALREADY_MERGED` après 6A.11F. 6A.12F ferme la
seconde dette du même fichier sans déplacer une ligne vers une autre catégorie;
la somme et la répartition restent donc exactes.

## 9. Blocs clos et protections

DEI/VOC, Java, Balkan National Awakening, Yugoslavia, Risorgimento,
nationalisme grec, Grande Crise orientale, Sick Man, Romania, les deux pinning
et les deux régions stratégiques portugaises restent clos. Le fichier portugais
final et les clés `region_equatorial_africa`/`region_east_africa` sont
inchangés.

NAVY, ADMIN, MARATH, Inde/BIC, Japon, Russie, Autriche, Croatie, Suisse,
révolutions américaine et française, technologies, descripteurs, sauvegardes
et `bject` restent protégés. BIC conserve
`activate_law = law_type:law_frontier_colonization`; aucune
`law_colonial_exploitation` n'est restaurée.

## 10. Merchant Banking GEN/VEN

### Comparaison trois voies

| Pays | Fork | Source hotfix | Vanilla |
| --- | --- | --- | --- |
| GEN | `law_traditionalism` | `law_merchant_banking` | fichier absent |
| VEN | `law_traditionalism` | `law_merchant_banking` | fichier absent |

Le changelog source annonce explicitement « Merchant Banking (Maritime
Republics) ». La loi est déjà définie dans `00_inject_laws.txt`, groupe
`lawgroup_economic_system`, visible uniquement pour GEN/VEN. L'icône
`merchant_banks.dds` et les localisations anglaise « Merchant Banking » et
française « Banque marchande » sont présentes dans le fork.

GEN et VEN sont des républiques maritimes en 1776; l'intention fonctionnelle et
historique est cohérente. Vanilla ne possède pas ces deux fichiers custom et
n'apporte donc ni convergence ni contradiction.

La source ajoute aussi un nom aux propriétaires terriens et retire
`law_merchant_navy`. Ces différences sont explicitement exclues. Le futur
correctif conserve la loi navale et remplace seulement une loi économique :

- deux fichiers;
- deux objets pays, `c:GEN` et `c:VEN`;
- deux hunks;
- deux suppressions et deux additions;
- aucune dépendance nouvelle;
- aucune localisation ou icône à créer;
- aucun chevauchement NAVY.

Hashes actuels :

- GEN : `B4EC2FB8C9916425FBFFBAA1CEF7FEDFB63C2E0510352A4744E088748AFD80EF`;
- VEN : `33503E48A69A431AD10ABC2AD71AF9D2147CDA6F19C0CD6C0C04434C1E5425B1`.

Hashes futurs calculés en mémoire :

- GEN : `7FC780AB8A8793E1DD1B3E6A32022807CED720FB1BE3F3D63D9EC6FDE9F43327`;
- VEN : `51A65341A2E3947A3D7D71BC3E3B1F31DA5CCD9D000D200C75BFB9570010B6DB`.

Rollback exact : restaurer uniquement `law_traditionalism` dans les deux
objets. Un runtime humain condensé doit confirmer pour GEN et VEN, au
1er/2 janvier 1776, Banque marchande active, Marine marchande préservée et
aucune autre loi initiale modifiée.

## 11. Navigation Acts

Les cinq fichiers théoriques sont GBR, `hbc - hudson bay company.txt`, NBS,
ONT et ORA; les objets sont `c:GBR`, `c:HBC`, `c:NBS`, `c:ONT` et `c:ORA`.
Le fork utilise `law_mercantilism`; la source
`law_mercantilism_navigation_acts`. Vanilla utilise `law_protectionism` pour
GBR et `law_mercantilism` pour les quatre colonies.

| Fichier exact | Delta fork/source | Delta fork/vanilla et dette adjacente |
| --- | --- | --- |
| `gbr - great britain.txt` | `2+/2-` : loi commerciale et déplacement sans effet de `law_professional_navy` | `52+/46-`; vanilla 1836 utilise Protectionism et de nombreuses autres lois; collision NAVY |
| `hbc - hudson bay company.txt` | `1+/1-`, loi seule | `1+/6-`; loi vanilla identique au fork, enveloppe de setup différente |
| `nbs - new brunswick.txt` | `1+/1-`, loi seule | `9+/7-`; fiscalité, propriété des femmes et système économique divergent |
| `ont - ontario.txt` | `1+/1-`, loi seule | `11+/9-`; vote, fiscalité, propriété des femmes, économie et police divergent |
| `ora - oranje.txt` | `1+/1-`, loi seule | `1+/1-`; vanilla converge avec le fork contre la source |

Le changelog, la loi, `regulation_acts.dds` et les localisations anglaise et
française existent. Le diff théorique serait cinq fichiers, cinq objets, cinq
hunks, cinq suppressions et cinq additions, rollback vers les cinq lois
courantes.

La source et vanilla divergent fonctionnellement pour les cinq pays. GBR
chevauche le bloc NAVY protégé. En outre,
`hbc - hubson bay company.txt`, identique dans fork et source, définit aussi
`c:HBC` et conserve `law_mercantilism`; l'ordre et l'effet de ces deux
définitions HBC doivent être audités avant toute correction. BIC est exclu.
La source hotfix constitue une intention 1776, mais la contradiction vanilla
et les deux définitions HBC empêchent de démontrer la compatibilité de départ
sans audit et runtime.

Verdict : audit documentaire futur seulement, puis runtime humain GBR et
colonies si un périmètre sûr est démontré. Sélection immédiate interdite.

## 12. Coup

`01_coup.txt:139`, objet `je_ip4_coup`, produit exactement un diagnostic
legacy. Fork : `should_be_pinned_by_default = yes`; source et vanilla :
`should_be_pinned_by_default_uninvolved_or_context = yes`.

Le remplacement isolé serait un fichier, un objet, un hunk, `1/1`, hash
théorique
`37C2669619CD26C30450F41082716BF30CA12949AA5FEE59BA0D25D498339602`;
rollback vers l'ancienne propriété. Les localisations anglaise et française
vanilla sont présentes.

Il existe toutefois des différences adjacentes importantes : scopes de loi et
lobby absents du fork, variables de localisation propres à la source, cleanup,
cooldown, invalidation et conditions d'existence divergents entre fork,
source et vanilla. Les événements `ip4_coup.2`, `.3`, `.4` et les dix pulses
restent liés. La visibilité et l'activation proviennent de la chaîne de coup,
pas d'un simple pinning. Un audit fonctionnel dédié et un runtime humain sont
requis avant correction.

L'objet n'a pas de gate autonome `is_shown_when_inactive` ou `possible`. Il
progresse par pulses hebdomadaires et mensuels, se complète à 120, expire après
730 jours, appelle `.2` au succès et `.3` à l'échec ou au timeout; `.4` est
appelé par le pulse hebdomadaire. Source et vanilla ajoutent les scopes de loi
en cours et de lobby, retirent les cooldowns locaux et délèguent plusieurs
nettoyages à `ip4_coup_cleanup_effects`; elles divergent encore sur les
variables de localisation et l'invalidation des scopes inexistants. Les
localisations anglaises et françaises des objets et événements existent, mais
aucune preuve ne garantit cette chaîne custom au départ de 1776.

## 13. Imperialism of Promise

`04_imperialism_of_promise.txt` contient un diagnostic de pinning ligne 140 et
deux erreurs runtime supplémentaires `has_role` lignes 18–19. L'objet unique
est `je_imperialism_of_promise`. L'ancienne propriété est
`should_be_pinned_by_default = yes`; source et vanilla utilisent
`should_be_pinned_by_default_uninvolved_or_context = yes`.

Source et vanilla convergent sur la propriété moderne et sur plusieurs
`has_role_of_type`, mais divergent sur le rôle de chef de groupe d'intérêt.
Le fork manque aussi le tooltip bureaucratique moderne. Les scopes BIC et
industrialists, la géographie de l'Inde, la progression, les événements
utilitarian et les conditions d'échec sont liés.

Plus précisément, source et vanilla ajoutent les rôles `ruler`, `agitator` et
`politician` avec seuil de prominence; seule la source conserve en plus
`has_role = character_role_ig_leader`. Elles enveloppent également la
disponibilité bureaucratique dans `bureaucrats_no_shortage_trigger`. Ces
différences touchent conditions, rôles et tooltip localisé, et ne permettent
pas une validation 1776 indépendante du bloc Inde/BIC.

Un pinning isolé serait `1/1/1`, `1/1`, hash théorique
`EF5200E0B9E7A58AF904C73CDD82F3CC4009FFE0CA9364952F793AB4F3E2A682`,
rollback legacy. Mais il laisserait deux erreurs de rôle et une dette
fonctionnelle plus large dans un bloc BIC/Inde protégé. Le candidat est écarté.

## 14. Tanzimat

Le fork ne contient pas `events/tanzimat_events.txt`; source et vanilla
possèdent le même fichier
`F5DAABC9D36BEAE714E5BDFC3B156995B3EAE7758004CE3C7B8C3512BA80AD30`,
namespace `tanzimat_events`, déclarant `.5` ligne 458, `.9` ligne 985 et `.10`
ligne 1094.

Le fournisseur est le fichier d'événements du jeu de base
`game/events/tanzimat_events.txt`; aucun fichier homonyme n'existe à la racine
des DLC installés. Le DLC `dlc014_ip3` monté pendant les runtimes précédents
n'est donc pas le fournisseur de ces trois déclarations.

Le fork les référence dans `00_sick_man.txt` lignes 347, 436 et 484, et `.10`
dans `00_code_on_actions.txt:4375`. Les nouveaux logs reproduisent les quatre
paires de diagnostics. Le `replace_path = "events"` du total conversion masque
le fichier vanilla malgré sa présence.

La ligne d'inventaire reste `OBSOLETE_HOTFIX_CONTENT` parce que la source égale
vanilla, mais copier le fichier restaurerait toute la chaîne et pourrait
réactiver Tanzimat. La chaîne Sick Man est désactivée au départ de 1776, tandis
que l'on-action globale `.10` reste active. Aucun correctif autonome ne peut
garantir l'absence de pulse, d'activation ou de changement ottoman.

`OTTOMAN_TANZIMAT_1776_DEFERRED_ACTIVATION_DESIGN_BACKLOG` est conservé.

## 15. Répétition française du Portugal

Vanilla définit :

- `TRIGGER_HAS_LAW_OR_VARIANT_FIRST`, français ligne 1100;
- `TRIGGER_HAS_LAW_OR_VARIANT_FIRST_NOT`, français ligne 1101;
- leurs équivalents anglais lignes 1377–1378.

Le français compose
`GetAltNameNoFormatting('Le')`, `GetNameNoFlag` et
`GetAltNameNoFormatting('AOnt')`; l'anglais n'utilise qu'une occurrence du nom.
Le nom dynamique fork/source `dyn_c_portu_king` vaut « Royaume de Portugal ».
Le scope `COUNTRY` passe donc plusieurs appels grammaticaux au nom dynamique,
ce qui explique la répétition visible. Chaque clé générique possède une
définition française, mais son utilisation par le moteur couvre globalement
tous les affichages `has_law_or_variant`.

Dans les fichiers locaux, chacune des deux clés génériques possède exactement
une définition française et une définition anglaise vanilla, et aucune
référence script littérale hors localisation. Le nombre de consommateurs
effectifs n'est pas bornable par recherche textuelle : le moteur choisit ces
clés génériques pour tous les triggers `has_law_or_variant`. Il ne peut donc pas
être réduit à l'unique entrée portugaise.

Une correction exigerait soit un override d'une localisation générique
utilisée ailleurs, soit une modification grammaticale du nom dynamique
portugais. Aucun correctif local à l'entrée n'est prouvé; nombre de consommateurs
moteur et impact transversal non bornés. Rollback théorique : restaurer la clé
générique ou `dyn_c_portu_king`, mais l'état corrigé sûr n'est pas défini. Un
audit global et un runtime français seraient requis. Dette non sélectionnée.

## 16. Autres petits candidats

Les 83 fichiers à erreur unique et les petits fichiers à deux erreurs ne sont
pas promus sur la seule occurrence parser. Les tutoriels, objectifs joueur,
Russie, NAVY, ADMIN, MARATH, technologies, révolutions custom et blocs clos
sont exclus. Aucun petit candidat inspecté n'offre simultanément une preuve
plus forte, un périmètre plus court et moins de dépendances que Merchant
Banking.

## 17. Top 3 exact

| Rang | Phase candidate | Fichiers | Objets | Hunks | Priorité | Preuve | Collision | Runtime |
| ---: | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| 1 | `HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW` | 2 | 2 | 2 | P1 | changelog et infrastructure complète | aucune | humain GEN/VEN |
| 2 | `HOTFIX_6A14R_NAVIGATION_ACTS_STARTING_LAW_AUDIT` | 5 | 5 | 5 théoriques | P1 | changelog et infrastructure | GBR/NAVY, divergence vanilla, doublon HBC | audit puis humain |
| 3 | `HOTFIX_6A15R_COUP_JOURNAL_ENTRY_1_13_FUNCTIONAL_AUDIT` | 1 | 1 | 1 pinning théorique | P1 | erreur parser et pinning convergent | dette fonctionnelle adjacente | audit puis humain |

Merchant Banking est sélectionné parce que son delta annoncé est déjà
entièrement infrastructuré et se réduit à deux substitutions autonomes.
Navigation Acts est reporté à un audit. Coup est reporté à un audit
fonctionnel. Imperialism, Tanzimat et la répétition française ne possèdent pas
de périmètre autonome sûr.

## 18. Futur périmètre fermé

La future phase pourra modifier avant runtime :

1. `common/history/countries/gen - genoa.txt`;
2. `common/history/countries/ven - venetia.txt`;
3. son rapport 6A.13F.

Après runtime, elle pourra mettre à jour uniquement les quatre documents de
navigation habituels. Dans `c:GEN` et `c:VEN`, deux hunks exacts :

```diff
-		activate_law = law_type:law_traditionalism
+		activate_law = law_type:law_merchant_banking
```

Préserver strictement `law_merchant_navy`, toutes les autres lois, tous les
effets et l'absence du nom spécifique des propriétaires terriens. Aucun fichier
de loi, icône ou localisation ne doit changer.

Rollback : restaurer `law_traditionalism` dans les deux objets et les hashes
initiaux. Runtime : un seul lancement humain, deux nouveaux départs GEN et VEN,
du 1er au 2 janvier 1776, vérification de Banque marchande et Marine marchande.

## 19. Documents de phase

Les six seuls documents créés ou modifiés sont :

1. ce rapport;
2. `docs/reports/hotfix/INDEX.md`;
3. `HOTFIX_REPORT_INDEX.csv`;
4. `HOTFIX_MERGE_BLOCK_STATUS.csv`;
5. `HOTFIX_MERGE_COMPLETION_ROADMAP.md`;
6. `HOTFIX_NEXT_MERGE_PHASE_PROMPT.md`.

Aucun gameplay, source hotfix, vanilla, localisation, recherche, `bject` ou
stash n'est modifié. Le prompt futur est autonome; la correction 6A.13F n'est
pas commencée.

## 20. Contrôles, commit et verdicts

Les contrôles finaux donnent :

| Contrôle | Résultat |
| --- | --- |
| Gameplay modifié | 0 |
| Documents de phase | 6 |
| Candidats publiés / sélectionnés | 3 / 1 |
| Inventaire | 161, catégories exclusives |
| Baseline exhaustive | 374 occurrences, 140 fichiers, 83 mono-erreur, 57 multi-erreurs |
| CSV | 123 lignes × 22 colonnes et 38 lignes × 17 colonnes, aucune cellule structurelle nulle |
| Hashes protégés | PASS |
| Source hotfix / vanilla | lectures seules, preuves ciblées inchangées |
| `git diff --check` | PASS |
| Index staged | vide |
| Stash | ligne exacte intacte |
| Processus Victoria / `dowser` / Paradox | 0 |

État Git final attendu et constaté, hors les éléments protégés déjà présents :

```txt
 M docs/reports/hotfix/INDEX.md
 M docs/reports/hotfix/_index/HOTFIX_MERGE_BLOCK_STATUS.csv
 M docs/reports/hotfix/_index/HOTFIX_MERGE_COMPLETION_ROADMAP.md
 M docs/reports/hotfix/_index/HOTFIX_NEXT_MERGE_PHASE_PROMPT.md
 M docs/reports/hotfix/_index/HOTFIX_REPORT_INDEX.csv
?? bject
?? docs/reports/hotfix/_index/HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION.md
?? docs/research/technology/
```

HEAD initial et final reste `7ba4785`. Aucun commit automatique n'est créé; la
décision de commit appartient à l'opérateur humain.

- `HOTFIX_6A13_RESIDUAL_GLOBAL_SCRIPT_SELECTION_COMPLETE`
- `NO_GAMEPLAY_CHANGED`
- `GLOBAL_SCRIPT_DELTAS_REVIEW_CONTINUES`
- `NEXT_EXECUTION_PHASE = HOTFIX_6A13F_GEN_VEN_MERCHANT_BANKING_STARTING_LAW`
