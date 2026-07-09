# Audit technique - 1776_Age_of_Revolutions_fork vers Victoria 3 The Great Wave / Update 1.13

Audit realise le 2026-07-04 dans le dossier `1776_Age_of_Revolutions_fork`.

Sources externes consultees pour cadrer les risques 1.13 :
- Dev Diary officiel Steam `Victoria 3 - Dev Diary #175 - Free Update 1.13 Overview` : https://store.steampowered.com/news/app/529340/view/503978984819655097
- Page officielle Steam `Victoria 3: The Great Wave - Expansion` : https://store.steampowered.com/app/4314650/Victoria_3_The_Great_Wave__Expansion/

## 1. Etat Git initial

- Branche actuelle : `audit-great-wave-1.13`
- Statut Git initial avant creation de ce rapport : propre (`git status --short` ne retournait aucune ligne)
- Depot Git present dans le dossier du mod
- Confirmation : aucun fichier gameplay n'a ete modifie pendant cet audit. Le seul changement attendu est la creation de `AUDIT_1776_GREAT_WAVE_1.13.md`

## 2. Structure generale du mod

| Dossier/fichier | Volume observe | Role probable | Risque / remarque |
|---|---:|---|---|
| `.git/` | 876 fichiers internes | Depot Git local | Hors gameplay |
| `.metadata/` | 2 fichiers | Metadata Paradox Launcher, thumbnail | `metadata.json` indique `supported_game_version = 1.12.5` |
| `common/` | 456 fichiers | Donnees gameplay principales | Zone la plus critique au lancement |
| `events/` | 308 fichiers | Evenements narratifs, systemiques, regionaux | Tres forte dependance aux triggers/effects vanilla |
| `gfx/` | 4 fichiers | Emblemes COA et assets graphiques | Faible volume, verifier chemins DDS |
| `gui/` | 0 fichier | Dossier present mais vide | Suspect/obsolet ou reserve |
| `localization/` | 8 fichiers | Localisation anglaise | Risque de cles manquantes apres renommages |
| `map_data/` | 2 fichiers | Overrides de state regions | Critique avec 1.13 si sea nodes/naval exits changent |
| `victoria3/` | 0 fichier | Dossier vide | Suspect/obsolet ou reserve |
| `descriptor.mod` | 1 fichier | Descriptor local | `supported_version = "1.*"` tres permissif |
| `Changelog.txt` | 1 fichier | Historique du mod | Mentionne l'update/DLC du 2026-04-28 et le rollback March 13 2026 |
| `Source.txt` | 1 fichier | Source externe historique/carte | Contient `https://hadaril.github.io/` |
| `thumbnail.png` | 1 fichier | Image du mod | Hors gameplay |

Fichiers principaux :
- `descriptor.mod`
- `.metadata/metadata.json`
- `common/defines/00_defines.txt`
- `common/ai_strategies/00_default_strategy.txt`
- `common/on_actions/00_code_on_actions.txt`
- `common/history/states/00_states.txt`
- `common/history/countries/*.txt`
- `common/history/buildings/*.txt`
- `common/history/military_formations/*.txt`
- `common/journal_entries/*.txt`
- `events/**/*.txt`
- `localization/english/*.yml`

Fichiers ou dossiers suspects/obsoletes a surveiller :
- `common/defines/00_defines.txt` : copie/override lourd de defines vanilla, contient encore des constantes convoys.
- `common/on_actions/00_code_on_actions.txt` : override massif probable de code/on_actions vanilla, risque eleve apres 1.13.
- `common/ai_strategies/00_default_strategy.txt` : override massif d'IA, contient logique ports/naval bases/convoys/anciens goods navals.
- `events/test_events.txt` et `common/journal_entries/99_test_global_je.txt` : contenu de test potentiellement non destine a une release.
- `common/history/military_formations/99_military_formations_example.txt` : exemple potentiellement obsolete.
- `common/amendments/amendments.md`, `common/dynamic_country_names/dynamic_country_names.md`, `common/journal_entries/journal_entries.md`, `common/objectives/objectives.md` : fichiers Markdown dans `common/`, probablement documentation locale mais a verifier si le moteur les ignore bien.
- `gui/` et `victoria3/` : dossiers vides.

## 3. Contenu gameplay identifie

| Categorie | Fichiers concernes | Resume fonctionnel |
|---|---|---|
| Pays | `common/country_definitions/00_countries.txt`, `common/country_definitions/02_modded_countries.txt`, `common/history/countries/*.txt` (148 fichiers), `localization/english/NM_Countries_l_english.yml`, `localization/english/mod_v2content_l_english.yml` | Definitions de tags, cultures primaires, couleurs, capitales, technologies initiales, lois et pays historiques 1776. Pays centraux visibles : `USA`, `GBR`, `FRA`, `SPA`, `AUS`, `RUS`, `PLC`, `BIC`, `DEI`, `DUR`, `PER`, `DENNOR`, `MARATH`, `MUG`. |
| Cultures | Pas de dossier `common/cultures`; references dans `common/country_definitions/*.txt`, `common/history/pops/*.txt`, events culturels | Le mod s'appuie surtout sur cultures vanilla/moddees referencees dans pays et pops. Risque si cultures vanilla 1.13 ont ete renommees ou restructurees. |
| Religions | Pas de dossier `common/religions`; references dans pays, pops, events | Religions probablement vanilla. Risque faible sauf references de scripts a des religions supprimees/renommees. |
| Lois | `common/laws/00_inject_laws.txt`, `events/law_events/*.txt` (35 fichiers), `common/amendments/*.txt`, `common/government_types/*.txt` | Injection de lois/amendements, evenements d'enactment, formes de gouvernement, reformes politiques. |
| Batiments | `common/history/buildings/00_west_europe.txt` a `15_russia.txt` (16 fichiers), references events | Historique regional complet des batiments, ports, shipyards, ressources, monuments. Tres sensible aux IDs de batiments/PM 1.13. |
| Technologies | Pas de dossier `common/technology`; references dans `events/tech_events/*.txt`, `events/technology_events.txt`, `common/history/countries/*.txt` | Evenements et pays ajoutent/verifient des technologies (`admiralty`, `ironclad_tech`, `battlefleet_tactics`, etc.). |
| Goods | Pas de dossier `common/goods`; references dans IA, pays, JE et PM | Goods navals detectes : `clippers`, `steamers`, `manowars`, `ironclads`, `merchant_marine`, `convoys`. Risque eleve avec 1.13 pour `convoys` et goods navals. |
| Production methods | Pas de dossier PM dedie; references dans `common/history/buildings/*.txt` et events | PM sensibles : `pm_basic_shipbuilding`, `pm_military_shipbuilding_wooden`, `pm_military_shipbuilding_wooden_2`, `pm_metal_shipbuilding`, `pm_basic_port`, `pm_wooden_whaling_ships`. |
| Interest groups | `common/interest_groups/00_landowners.txt`, `common/ideologies/07_ig_ideologies_modded.txt`, `events/ig_*.txt`, events law/election | Ajuste IG/ideologies, leaders, petitions, revolutions, suppression. |
| Characters | `common/character_templates/*.txt` (26), `common/history/characters/*.txt` (12), `common/dna_data/*.txt` (7), nombreux events | Rulers, heirs, agitators, generals, admirals, templates historiques. Pays centraux avec fichiers dedies : AUS, BIC, DEI, DUR, FRA, GBR, PER, PLC, RUS, SIC, SPA, USA. |
| Events | `events/**/*.txt` (308 fichiers) | Systeme narratif massif : revolutions, lois, tech, expeditions, Inde, Iberie, Balkans, Bresil, Great Game, ACW, etc. |
| Journal entries | `common/journal_entries/*.txt` (165 fichiers) | JE vanilla/moddees, objectifs historiques, contenus regionaux. Numerotation thematique : `00_*` global, `02_*` Bresil/Sud-Amerique, `04_*` Inde, `05_*` Balkans/Autriche, `06_*` Iberie/French Revolution/New Imperialism, `07_*` modded late content. |
| Decisions / scripted buttons | Pas de dossier `common/decisions`; `common/scripted_buttons/*.txt` | Les decisions sont probablement absentes ou remplacees par scripted buttons : colonial admins, cheat Revolution francaise, buttons modSX. |
| Flags | `common/flag_definitions/*.txt`, `common/coat_of_arms/coat_of_arms/03_new.txt`, `gfx/coat_of_arms/**/*.dds` | Flags/drapeaux dynamiques, COA et emblemes nouveaux. |
| Map_data | `map_data/state_regions/08_middle_east.txt`, `map_data/state_regions/13_australasia.txt` | Overrides de state regions avec provinces, ports, villes, ressources, `naval_exit_id`. Critique en 1.13. |
| States / strategic regions | `common/history/states/00_states.txt`, `map_data/state_regions/*.txt`, `common/state_traits/13_mod_traitsSX.txt` | Ownership historique, state traits, ressources et ports. Pas de dossier `strategic_regions` observe. |
| GUI | `gui/` vide | Pas d'override GUI local detecte. Risque direct faible, mais les loc/JE peuvent appeler des icones/GUI vanilla modifiees. |
| Localization | `localization/english/*.yml` (8 fichiers) | Localisation anglaise : events, modifiers, country flavor, JE, pays, noms, power blocs. |
| Images / gfx | `thumbnail.png`, `.metadata/thumbnail.png`, 4 DDS dans `gfx/coat_of_arms` | Assets limites aux thumbnails et emblemes COA. |

## 4. Cartographie des dependances internes

Dependances structurelles :
- `descriptor.mod` et `.metadata/metadata.json` declarent le mod et ses `replace_paths`. Les replace paths les plus sensibles sont `common/history/characters`, `common/history/character_templates`, `common/history/diplomatic_plays`, `common/history/diplomacy`, `common/history/interests`, `common/history/treaties`, `common/history/military_deployments`, `common/flag_definitions`, `common/dynamic_country_names`, `events`, `common/journal_entries`.
- `common/country_definitions/*.txt` depend de `common/history/countries/*.txt`, `common/history/pops/*.txt`, `common/history/states/00_states.txt`, flags, dyn_names et localisation.
- `common/history/buildings/*.txt` depend des state regions, des building IDs, des goods et PM vanilla.
- `common/history/military_formations/*.txt` depend des countries, HQ, unit types, commanders et role/formations 1.13.
- `common/character_templates/*.txt` depend de cultures, religions, traits, ideologies, roles `general/admiral/agitator/ruler/heir`, et parfois `commander_usage`.
- `events/**/*.txt` depend de JE, modifiers, scripted buttons, on_actions, countries, states, character templates, technologies, laws et localisation.
- `common/journal_entries/*.txt` depend de events, scripted buttons, progress bars, modifiers, states/countries et localisation.
- `common/on_actions/00_code_on_actions.txt` depend des events et notifications.
- `common/ai_strategies/00_default_strategy.txt` depend des batiments, goods, technologies, power blocs, formations et strategies vanilla.

Localisation par fichier :
- `localization/english/76mod_event_l_english.yml` : environ 30 cles, surtout Haiti, Irish Question, Venetian Empire.
- `localization/english/76mod_modifiers_l_english.yml` : environ 17 cles, modifiers USA, PLC, Venice, colonies, standards of living.
- `localization/english/country_flavor_text_l_english.yml` : environ 325 cles `*_FLAVOR_TEXT`.
- `localization/english/mod_journal_entries_l_english.yml` : environ 128 cles, JE colonialisme britannique, New Imperialism, Irish Question, Great Revolution.
- `localization/english/mod_v2content_l_english.yml` : environ 472 cles, pays, dyn_names, amendments, events, modifiers, tooltips.
- `localization/english/NM_Countries_l_english.yml` : environ 57 cles pays/dyn_names/colonial admins.
- `localization/english/NM_Names_l_english.yml` : environ 5 cles de noms.
- `localization/english/NM_power_blocs_l_english.yml` : environ 3 cles power blocs.

Correspondances event/JE/localisation probables :
- `events/america_michigan_war_mod.txt` -> cles `america_michigan_war_mod.*` dans `mod_v2content_l_english.yml`.
- `events/battle_for_india_events.txt` et `common/journal_entries/00_battle_for_india_mod.txt` -> cles `battle_for_india_events.*`, `je_battle_for_india*`.
- `events/colonial_administration_events.txt`, `common/scripted_buttons/00_new_colonial_admins.txt`, `common/journal_entries/06_new_imperialism.txt` -> cles `colonial_administration_*`, `je_new_imperialism*`, `je_colonial_administration_button_*`.
- `events/french_revolution_mod_events.txt`, `common/journal_entries/06_french_revolution_mod.txt` -> cles French Revolution dans `mod_v2content_l_english.yml`.
- `events/brazil/brazil_navy.txt`, `common/journal_entries/02_brazil_navy.txt` -> cles Bresil/navy dans `mod_v2content_l_english.yml`.
- `events/india_events/*.txt`, `common/journal_entries/04_*.txt` -> contenus Inde/BIC/Mughal/Sikh/Sepoy/railway.
- `events/iberia_events/*.txt`, `common/journal_entries/06_*.txt` -> contenus Iberie, Portugal, Cuba, Philippines, Spanish Africa.
- `events/balkans_events/*.txt`, `common/journal_entries/05_*.txt` -> Balkans, Autriche, Hongrie, Montenegro, Serbie, Yugoslavie.

Pays/personnages/events centraux :
- Pays centraux : `GBR`, `USA`, `FRA`, `SPA`, `AUS`, `RUS`, `PLC`, `BIC`, `DEI`, `DUR`, `PER`, `BRZ`, `DENNOR`, `MARATH`, `MUG`, `SIC`.
- Personnages centraux : George Washington, Louis XVI, Charles III, Karim Khan Zand, Mohammed Qajar, Stanislaw PLC, king of Britain, rulers/heirs Habsbourg, commanders/admirals GBR/AUS/RUS/BIC.
- Events centraux : independence USA, PLC reform, French Revolution, Battle for India, New Imperialism/colonial admins, Brazil Navy, Great Game, Iberia/Spanish Africa, Balkans/Austria, ACW, Meiji/Japan, naval tech events.

## 5. Risques de casse avec The Great Wave / Update 1.13

Contexte 1.13 d'apres les annonces officielles : The Great Wave / Update 1.13 rework fortement la marine : systeme naval rework, suppression des convoys comme bien/systeme precedent, introduction des Supply Ships, shipyards fusionnes et utilises pour la Ship Construction, sea zones/sea route network retravailles, straits et naval fortifications ajoutes, troop transportation/naval missions modifies, ship types et technologies navales retravailles.

Risques prioritaires :
- Navires / shipyards : 51 occurrences de `building_shipyard`; PM historiques `pm_basic_shipbuilding`, `pm_military_shipbuilding_wooden`, `pm_military_shipbuilding_wooden_2`, `pm_metal_shipbuilding`. Ces IDs/PM peuvent avoir change avec les shipyards fusionnes et la Ship Construction.
- Convoys / supply ships : 55 occurrences de `convoy`, 13 de `convoys`, `num_convoys_available`, `country_convoys_capacity_mult`, `on_enemy_convoys_raided`, `on_our_convoys_raided`. 1.13 retire les convoys et les remplace fonctionnellement par Merchant Marine/Supply Ships selon usage civil/militaire.
- Naval bases : references a `building_naval_base` dans AI, defines, events Revolution, Brazil Navy, Dreadnought Hoax, Russo-Chinese events. A verifier contre les nouveaux fleets/naval bases/ship types.
- Naval invasions / transport : pas de gros bloc explicitement nomme `naval_invasion` detecte, mais formations, fleets, admirals et supply peuvent casser indirectement les invasions.
- Sea nodes / sea zones : `any_sea_node_adjacent_state` dans AI, `naval_exit_id` dans `map_data/state_regions/08_middle_east.txt` et `13_australasia.txt` (32 hits). 1.13 retravaille sea zones/route network : risque critique de mismatch.
- Straits : references a `STATE_STRAIT_OF_GIBRALTAR` dans `events/iberia_events/spanish_africa_events.txt` et `common/journal_entries/06_spanish_africa.txt`; la nouvelle mecanique de straits/naval forts peut necessiter adaptation.
- Naval forts : aucun `building_naval_fort` detecte. Il faudra ajouter/verifier les nouveaux batiments vanilla si necessaires, surtout Gibraltar, Hormuz, Suez, Denmark-Norway, Singapore/Ceylon/East Indies.
- Military formations : 9 fichiers `common/history/military_formations/*.txt`, 66 fichiers avec references formations/commanders. 1.13 ajoute logistics center/supply routes et change le comportement naval.
- Commanders / character roles : nombreux `is_admiral`, `has_role = admiral`, `commander_usage`, `commander_rank`. Risque si roles, fleets ou commander orders ont change.
- Map_data / state regions : deux overrides directs de state regions, avec ports, `naval_exit_id`, ressources et provinces. Tres critique car un ancien `naval_exit_id` peut provoquer erreurs de carte ou routes navales invalides.
- Goods supprimes/renommes : `convoys` a risque maximal; `manowars`, `ironclads`, `clippers`, `steamers`, `merchant_marine` a verifier car 1.13 change ship types et usage maritime.
- Triggers/effects potentiellement obsoletes : `num_convoys_available`, convoy raiding on_actions, `country_convoys_capacity_mult`, `is_fleet`, `commander_military_formation`, `any_sea_node_adjacent_state`, unit type `combat_unit_type_ironclad`, PM shipbuilding anciennes.
- GUI : dossier local vide, mais la top bar 1.13 remplace convoys par Supply Ships. Les JE/tutorial/objectives qui parlent de convoys risquent d'afficher des instructions obsoletes.
- Localisation : cles contenant "convoy", "supply convoy", "merchant marine", "strait", "navy" a reviser pour coherer avec 1.13.

Fichiers 1.13 les plus exposes detectes :
- `common/defines/00_defines.txt`
- `common/ai_strategies/00_default_strategy.txt`
- `common/on_actions/00_code_on_actions.txt`
- `common/company_types/02_new_companies.txt`
- `common/history/buildings/*.txt`
- `common/history/military_formations/*.txt`
- `map_data/state_regions/08_middle_east.txt`
- `map_data/state_regions/13_australasia.txt`
- `common/journal_entries/00_tutorial.txt`
- `common/journal_entries/02_brazil_navy.txt`
- `common/journal_entries/05_prestige_goods.txt`
- `common/journal_entries/06_spanish_africa.txt`
- `events/tech_events/naval_tech_events.txt`
- `events/tech_events/military_tech_events_01.txt`
- `events/titanic_events.txt`
- `events/dreadnought_hoax.txt`
- `events/brazil/brazil_navy.txt`
- `events/iberia_events/spanish_africa_events.txt`
- `events/russo_chinese_events.txt`
- `events/soi_events/00_ep1_kazakh_events.txt`
- `localization/english/mod_v2content_l_english.yml`
- `localization/english/mod_journal_entries_l_english.yml`
- `localization/english/country_flavor_text_l_english.yml`

## 6. Liste des fichiers a tester en priorite

Critique - peut empecher le mod de se lancer :
- `descriptor.mod`
- `.metadata/metadata.json`
- `common/defines/00_defines.txt`
- `common/on_actions/00_code_on_actions.txt`
- `common/ai_strategies/00_default_strategy.txt`
- `common/country_definitions/00_countries.txt`
- `common/country_definitions/02_modded_countries.txt`
- `common/history/states/00_states.txt`
- `common/history/countries/*.txt`
- `common/history/buildings/*.txt`
- `common/history/pops/*.txt`
- `common/history/military_formations/*.txt`
- `map_data/state_regions/08_middle_east.txt`
- `map_data/state_regions/13_australasia.txt`
- `common/flag_definitions/*.txt`
- `common/dynamic_country_names/00_dynamic_country_names.txt`
- `common/journal_entries/*.txt`
- `events/**/*.txt`
- `localization/english/*.yml`

Important - peut casser le gameplay :
- `events/tech_events/naval_tech_events.txt`
- `events/tech_events/military_tech_events_01.txt`
- `events/titanic_events.txt`
- `events/dreadnought_hoax.txt`
- `events/brazil/brazil_navy.txt`
- `common/journal_entries/02_brazil_navy.txt`
- `common/journal_entries/05_prestige_goods.txt`
- `common/journal_entries/06_spanish_africa.txt`
- `events/iberia_events/spanish_africa_events.txt`
- `common/company_types/02_new_companies.txt`
- `common/character_templates/country_gbr.txt`
- `common/character_templates/country_aus.txt`
- `common/character_templates/country_rus.txt`
- `common/character_templates/country_bic.txt`
- `common/history/characters/*.txt`
- `common/scripted_buttons/*.txt`
- `common/scripted_progress_bars/01_mod76_progress_bars.txt`

Secondaire - contenu a corriger plus tard :
- `events/test_events.txt`
- `common/journal_entries/99_test_global_je.txt`
- `common/history/military_formations/99_military_formations_example.txt`
- `common/amendments/amendments.md`
- `common/dynamic_country_names/dynamic_country_names.md`
- `common/journal_entries/journal_entries.md`
- `common/objectives/objectives.md`
- `Changelog.txt`
- `Source.txt`
- `gfx/coat_of_arms/**/*.dds`
- `thumbnail.png`

## 7. Plan de migration propose

Phase 0 - sauvegarde, Git, baseline :
- Conserver la branche d'audit intacte.
- Creer une branche de migration separee apres validation du rapport.
- Faire un commit baseline du mod actuel et du rapport.
- Conserver une copie zip hors depot.
- Noter la version Victoria 3 source actuellement supportee : metadata `1.12.5`, descriptor `1.*`.

Phase 1 - lancement du mod sans crash :
- Lancer Victoria 3 1.13.x avec uniquement ce mod active.
- Verifier crash avant menu, crash au chargement, crash a la selection pays, crash a J+1.
- Corriger uniquement les erreurs bloquantes de parser/load order.

Phase 2 - correction des erreurs de logs :
- Traiter d'abord `error.log`, `game.log`, `system.log`.
- Corriger IDs introuvables : buildings, PM, goods, technologies, traits, laws, events, scopes.
- Isoler les overrides massifs : `defines`, `on_actions`, `ai_strategies`.
- Refaire un lancement apres chaque petit lot de corrections.

Phase 3 - adaptation The Great Wave : marine, shipyards, sea nodes, convoys :
- Remplacer l'ancien vocabulaire convoy par les equivalents 1.13 : Merchant Marine / Supply Ships selon contexte.
- Adapter les PM shipyards historiques aux nouveaux PM 1.13.
- Verifier `building_shipyard`, `building_naval_base`, ports et naval forts.
- Revoir `common/history/military_formations/*.txt` pour fleets, transport capacity, supply/logistics.
- Revoir `map_data/state_regions/*.txt` et tous les `naval_exit_id`.
- Adapter `events/tech_events/naval_tech_events.txt` et `events/tech_events/military_tech_events_01.txt`.

Phase 4 - correction carte/pays/economie :
- Verifier ownership 1776, pops, buildings, technologies initiales, laws initiales.
- Tester ports/market access/supply sur iles et colonies.
- Verifier colonial admins, BIC/DEI, USA colonies, Iberie, Denmark-Norway, Australasie/Middle East.

Phase 5 - test gameplay 1776 :
- Lancer au moins 5 a 10 ans en observer.
- Tester guerres navales et debarquements.
- Tester les JE centrales : USA independence, French Revolution, PLC reform, Battle for India, New Imperialism, Brazil Navy.
- Verifier que les pays majeurs ne demarrent pas avec economie/navy/supply impossible.

Phase 6 - roadmap historique future :
- Ajouter contenu 1.13 volontaire : straits, naval forts, ship designer/flagships si exposables en script, marine units, gunboat diplomacy.
- Revoir equilibre naval 1776 par region.
- Documenter clairement ce qui reste vanilla 1.13 et ce qui est propre au mod.

## 8. Commandes ou tests recommandes

Commandes Git utiles :
```powershell
git status --short
git branch --show-current
git diff -- AUDIT_1776_GREAT_WAVE_1.13.md
git diff -- common events map_data localization
```

Recherches locales utiles :
```powershell
rg -n -i "convoy|convoys|supply_ship|shipyard|naval_base|building_port|sea_node|sea_zone|naval_exit_id|strait|is_fleet|admiral|military_formation|merchant_marine|clippers|steamers|manowars|ironclads" common events map_data localization
rg -n -i "unknown|error|deprecated|obsolete" "$env:USERPROFILE\Documents\Paradox Interactive\Victoria 3\logs"
```

Comment tester dans Victoria 3 :
- Activer uniquement `1776 - Age of Revolutions Fork` dans un playset dedie.
- Lancer Victoria 3 en version The Great Wave / 1.13.x.
- Tester d'abord sans autres mods.
- Entrer au menu principal, ouvrir le launcher, verifier que le mod apparait sans avertissement rouge.
- Lancer une partie 1776 avec une nation majeure puis avancer au moins un mois.
- Faire un test observer d'un an, puis un test 5 ans si les logs sont stables.

Logs a surveiller :
- `%USERPROFILE%\Documents\Paradox Interactive\Victoria 3\logs\error.log`
- `%USERPROFILE%\Documents\Paradox Interactive\Victoria 3\logs\game.log`
- `%USERPROFILE%\Documents\Paradox Interactive\Victoria 3\logs\system.log`
- `%USERPROFILE%\Documents\Paradox Interactive\Victoria 3\logs\debug.log` si present
- Dumps/crashs eventuels dans le dossier crash Paradox/Victoria 3

Fichiers a verifier apres crash :
- Si crash au chargement : `common/defines`, `common/on_actions`, `common/history/states`, `map_data/state_regions`, `common/country_definitions`.
- Si crash a la selection pays : `common/history/countries`, `common/history/pops`, `common/history/buildings`, `common/history/characters`.
- Si crash au premier jour : `common/on_actions`, `events`, `common/journal_entries`, `common/history/military_formations`.
- Si crash naval ou guerre : `common/history/military_formations`, `events/tech_events/naval_tech_events.txt`, `events/tech_events/military_tech_events_01.txt`, `common/ai_strategies/00_default_strategy.txt`.

Nations a tester en priorite :
- `GBR` : marine, colonies, BIC/DEI, New Imperialism, routes commerciales.
- `USA` / colonies americaines : independence, Michigan/ACW precoces, ownership 1776.
- `FRA` : French Revolution, navy, Europe.
- `SPA` : Spanish America, Cuba, Philippines, Gibraltar/Spanish Africa.
- `AUS` : Balkans, commanders/admirals, Danubian/Hungarian content.
- `RUS` : Great Game, naval commanders, Alaska/Siberia.
- `PLC` : reformes, partitions, laws/amendments.
- `BIC` : Battle for India, colonial admins, commanders/admirals.
- `DEI` : East Indies, companies, colonial gameplay.
- `BRZ` : Brazil Navy, South America content.
- `DENNOR` : straits, trade, colonies, naval choke points.
- `PER` / `DUR` : Qajar/Durrani, Great Game, Middle East map_data.

## 9. Resume final

Etat general :
- Le mod est volumineux et ressemble a une total conversion historique 1776 avec overrides profonds de `history`, `events`, `journal_entries`, `ai_strategies`, `defines` et `on_actions`.
- Le depot etait propre avant creation de ce rapport.
- Aucun fichier gameplay n'a ete modifie.
- La metadata cible encore `1.12.5`, alors que The Great Wave / 1.13 modifie fortement les systemes navals.

Difficulte estimee de migration :
- Elevee. Les risques ne sont pas seulement narratifs : le mod touche des fichiers centraux et remplace des chemins entiers.
- Le plus gros bloc de travail sera probablement la migration marine/supply/shipyards/sea network, puis la validation des overrides vanilla massifs.

Priorite absolue pour la prochaine etape :
- Creer une branche de migration separee, lancer le mod en 1.13.x sans correction initiale, recuperer `error.log`, puis traiter d'abord `common/defines/00_defines.txt`, `common/on_actions/00_code_on_actions.txt`, `common/ai_strategies/00_default_strategy.txt`, `common/history/buildings/*.txt`, `common/history/military_formations/*.txt` et `map_data/state_regions/*.txt`.
