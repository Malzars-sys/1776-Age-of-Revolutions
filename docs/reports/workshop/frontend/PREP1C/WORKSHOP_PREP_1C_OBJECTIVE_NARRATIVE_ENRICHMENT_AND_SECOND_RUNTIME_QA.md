# WORKSHOP_PREP_1C OBJECTIVE NARRATIVE ENRICHMENT AND SECOND RUNTIME QA

## Status

- Phase: `WORKSHOP_PREP_1C_OBJECTIVE_NARRATIVE_ENRICHMENT_AND_SECOND_RUNTIME_QA`
- Branch: `workshop-prep-frontend-objectives`
- Base HEAD: `3f7200d7a7f984fb703877ff7c1dbccd97f1f256`
- PREP1B manually committed: `PASS`
- Runtime state: `SINGLE_RUNTIME_COMPLETE_STATIC_REMEDIATION_AWAITING_FOLLOWUP`
- Human runtime launches: `1 / 1`
- Automatic commit/push: `NO / NO`

## Scope

The four objective introductions and all seventeen recommended-country descriptions were rewritten in French and English. The runtime then expanded the operator-approved scope to the Learn the Game objective: its introduction and four country descriptions were rewritten, and the fork's valid 1776 Belgian tag `BEO` was added to the recommendations. No objective IDs, icons, art paths, subgoals, journal mechanics, gameplay setup, or GUI layout were changed.

The runtime also established that objective cards bypass political flag definitions and render the base country CoA. Static follow-up overrides the base `BIC` and `DEI` CoAs with the existing East India Company ensign and VOC-lettered flag. Finally, because the Victoria 3 1.13 `main_theme_track` API has no loop field, all four title-theme slots now reference a 30-minute continuous Cantus Firmus master rather than the 100.3-second source.

## UI capacity audit

Vanilla 1.13 uses `gui/objective_types.gui`:

- general objective descriptions are rendered in a scroll area;
- recommended-country cards are `320x540` for four or fewer tags and `320x400` for more than four tags;
- the description widget is expanding multiline text at `fontsize_large`;
- the longest audited vanilla country flavor text is 379 characters in English and 445 in French.

PREP1C texts deliberately use two to four sentences and range from 364 to 495 visible characters. Battle for India remains the densest screen because it has eight `320x400` cards. The single runtime screenshots and operator report confirmed that the rewritten French text is readable, unclipped, and free of raw keys.

## January 1776 setup audit

The fork, rather than later real history, was treated as the source of truth. The narrative was grounded in `common/history/countries`, `common/history/characters`, `common/history/states`, `common/history/diplomacy`, `common/history/diplomatic_plays`, and starting journal entries.

| Objective | Tag | Audited setup used in the description |
|---|---|---|
| Battle for India | FRA | Louis XVI, absolute Bourbon monarchy, surviving Indian enclaves, war against Britain with the American rebels |
| Battle for India | BIC | British chartered company, Warren Hastings, Bengal/Bihar/Awadh/Circars, high-tax extraction, consolidation journal |
| Battle for India | MARATH | Oligarchic monarchy, Bombay/Malwa/Agra arc, four starting vassals, hostile BIC/HYD/Mysore relations |
| Battle for India | DUR | Timur Durrani, Punjab/Kashmir/Afghan core, Mughal tributary, Sindh and Kafiristan vassals, Hindustan journal |
| Battle for India | HYD | Hyderabad and central Deccan, Kurnool/Pudukkottai vassals, hostile BIC/Maratha/Mysore relations |
| Battle for India | DEI | Dutch chartered company, Reinier de Klerk, Java/Ceylon/Moluccas/Celebes network, extraction and dependent rulers |
| Battle for India | NET | Mercantile monarchy, wealth voting, direct Travancore station, DEI chartered subject, Portugal rivalry |
| Battle for India | POR | Absolute mercantile monarchy, Brazil and African colonies, Goa/Macau/Timor chain, Portugal-Netherlands rivalry |
| Age of Revolutions | FRA | Louis XVI, Bourbon absolutism and privileged ruling groups, active American war |
| Age of Revolutions | USA | British colonial subject in an independence war, George Washington, presidential republic, wealth voting, slavery |
| Age of Revolutions | PLC | Stanisław August Poniatowski, elective-monarchy amendment, magnate oligarchy, serfdom, reform journal, hostile partition powers |
| Imperial Rivalries | GBR | George III, American revolt, France/Spain rivalry, Canadian and Caribbean colonies, BIC and HBC chartered companies |
| Imperial Rivalries | SPA | Charles III, absolute Bourbon monarchy, large colonial network, active American war and British rivalry |
| Imperial Rivalries | RUS | Catherine Romanov, autocracy and serfdom, Ottoman rivalry, Caucasus journal, steppe protectorates and Alaska company |
| Imperial Rivalries | PRU | Autocratic monarchy, professional army, geographically scattered possessions, Commonwealth hostility, Hohenzollern puppet |
| Mercantile Republics | VEN | Patrician merchant republic, merchant banking/navy, Venetia-Istria-Dalmatia-Ionian-Aegean possessions |
| Mercantile Republics | GEN | Compact Ligurian merchant republic, merchant banking and navy, capital-and-credit strategy |
| Learn the Game | SWE | Iron exports, oligarchic monarchy, professional navy, German puppets, Russia/Prussia balance |
| Learn the Game | BEO | Austrian crown land, Flanders and Wallonia, landed voting, traditionalism, autonomy from Vienna |
| Learn the Game | DAI | Traditional unrecognized kingdom, sericulture, Cambodian tributary, Siam rivalry, Chinese suspicion |
| Learn the Game | DENNOR | Danish straits, Norwegian resources, Holstein/Schleswig unions, colonies, professional navy |

## Localization audit

- English and French files retain UTF-8 BOM and valid language headers.
- All 52 scoped bilingual description values are quoted, have balanced formatting markers, and are unique within their active language layer.
- Visible custom titles remain `Age of Revolutions` / `Âge des Révolutions` and `Imperial Rivalries` / `Rivalités impériales`; no visible objective card falls back to Hegemony or Egalitarian Society wording.
- Legacy `SC1` text and unrelated uses of the gameplay concept `hegemony` were not modified because they are outside the seventeen recommended tags.
- The USA flag is intentionally unchanged. The thirteen-star Stars and Stripes was adopted in June 1777, whereas a Grand Union flag is more exact for January 1776; the present design is retained by operator choice and remains a documented approximation.

## Company-flag correction

The objective GUI explicitly calls `CountryDefinition.GetBaseFlag`, bypassing `common/flag_definitions`. This exposed the Raj-star base CoA for `BIC` and the plain Dutch tricolor base CoA for `DEI`, even though the political variants already selected `BIC_republic` and `DEI_voc`. Static follow-up copies those existing company designs into the two base CoAs used by the cards. This is a presentation-layer correction; country setup and flag triggers remain unchanged.

## Main-menu music correction

The single runtime confirmed that Cantus Firmus starts correctly, but the original 100.301-second Ogg reaches EOF and vanilla music then takes over. Victoria 3 1.13 documents `music`, `can_be_interrupted`, and DLC gating for a main theme but no loop switch. PREP1C therefore adds `cantus_firmus_monks_menu_30m.ogg`, a 1,805.452-second continuous stream made by losslessly repeating the supplied Ogg, and points all four title-theme slots to it. The original short asset is retained. A later authorized runtime must verify the new stream and its menu-to-game transition.

## Runtime evidence

- Planned sequence: `WORKSHOP_PREP_1C_RUNTIME_TEST_MATRIX.csv`
- Results: `WORKSHOP_PREP_1C_RUNTIME_RESULTS.csv`
- Text inventory: `WORKSHOP_PREP_1C_OBJECTIVE_TEXT_INVENTORY.csv`
- Before/after log evidence: `WORKSHOP_PREP_1C_LOG_MANIFEST.csv`

The only authorized launch is complete. The operator supplied screenshots of the main menu and all rewritten objective pages and explicitly reported no raw key. The four objective artworks, main-menu composition, rewritten narratives, and previously corrected period flags passed. Three runtime defects were isolated: title music reached EOF, BIC showed the Raj star, and DEI showed the Netherlands tricolor. The operator also requested richer tutorial narratives and Belgium as a recommendation. All five findings have static remediations applied, but no second launch is permitted in PREP1C; tests `PREP1C-03`, `26`, `30`, `31`, and `32` therefore require a later runtime confirmation.

Tests `PREP1C-01`, `27`, and `28` were not explicitly observed during this launch and also remain follow-up items. Shutdown passed and the final process check confirmed that both game and launcher were closed with the launch quota at `1 / 1`.

## Pre-runtime static QA

Result before launch: `PASS` (`66 / 66` checks).

- All 42 scoped descriptions exist exactly once, remain within the requested character windows, and preserve UTF-8 BOM encoding.
- The four CSV artifacts parse successfully; the runtime matrix and result sheet both contain 30 aligned tests, all pending before launch.
- The BIC base definition resolves to the vanilla `BIC_republic` company ensign, and the full flag-definition file has balanced braces.
- Objective mechanics are unchanged, no forbidden legacy title is active, and `git diff --check` passes.
- The game and launcher are closed, the protected stash hash is unchanged, and exactly seven protected technology files remain untracked.

## Post-runtime static QA

- `BIC` and `DEI` base CoAs reproduce the existing `BIC_republic` and `DEI_voc` definitions that the objective GUI previously bypassed.
- Learn the Game now recommends `SWE BEO DAI DENNOR`; `BEO` is the playable Austrian-Netherlands crown land present in the fork, whereas vanilla `BEL` is not a 1776 starting country.
- The tutorial introduction and four country descriptions are 398–487 visible characters per language and retain UTF-8 BOM encoding.
- The continuous title asset is valid stereo Vorbis at 44.1 kHz, lasts 1,805.452 seconds, and is referenced by all four main-theme slots.
- Fresh logs contain no scoped objective, localization, music, or CoA parse error. Existing law/history warnings are out of PREP1C scope and are recorded as such in the manifest.
- No second runtime, commit, push, stash operation, reset, or PREP2 work was performed.

## Protected state

- The seven untracked technology-research files remain protected and untouched.
- `stash@{0}` remains `518df704fa14599c0f254fae13859210663dd976`.
- Workshop descriptor, published ID, thumbnail, tags, description, and changelog remain untouched.
- PREP2 has not started.
