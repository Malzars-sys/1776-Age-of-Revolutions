# MAP-2W — Inventaire et premier sous-lot Fulda

17 octobre 2026. Date historique : 1er janvier 1776.

**MAP2W_READY_FOR_SCOPED_RUNTIME_VALIDATION**. Ce statut concerne exclusivement le noyau MAP2W-R1. Les 94 entrées de l’inventaire ne signifient pas que toute l’Allemagne occidentale et méridionale est achevée. Aucun test moteur MAP2W n’a été exécuté.

## Le risque de refaire les mêmes zones était réel

Le prompt recoupe des territoires déjà travaillés. La lecture chronologique des migrations et des derniers rapports évite de traiter les anciennes listes d’incertitudes comme l’état actuel :

| Secteur | Travail existant conservé | Ce que cela ne certifie pas |
| --- | --- | --- |
| Franconie | FRANCONIA puis FRANCONIA_CONTINUATION : Ansbach/Bayreuth, Bamberg, Würzburg, Nuremberg, fragments Eichstätt/Cobourg | Hohenlohe, Castell, Wertheim, villes secondaires et résidus bavarois |
| Rhin central/Mayence/Palatinat | RHINE_CENTRAL, MAINZ_PALATINATE, MAINZ_ESTATES, MAINZ_COMPLETION | Toutes les juridictions de Hesse ou toutes les possessions de Mayence |
| Rhin–Westphalie | Münster, Paderborn, Juliers–Berg sous souverain palatin, Minden/Ravensberg, Westphalie et Vest de Cologne, Osnabrück, Niederstift, Lingen/Tecklenburg | Gueldre prussienne, limites fines Clèves/Mark, petits comtés/abbayes, toutes les branches de Nassau |
| Souabe | SWABIA, CONTINUATION, FINISH, COMPLETION : Fürstenberg, Ellwangen, Salem, Weingarten, Waldburg, Constance/Markdorf, Augsbourg et Kempten distincts, villes libres | Montbéliard, Oettingen, dépendances et condominiums, toutes les franges ecclésiastiques |
| Saxe/Thuringe | MAP2T puis MAP2U : nouveaux noyaux, Reuss, Sondershausen | Les résidus laissés C ne deviennent pas des possessions saxonnes historiquement certifiées |

Liège et la Belgique restent protégés ; leur absence éventuelle d’une migration tardive ne signifie pas absence de travail. Eutin, Anhalt, Poméranie et possessions suédoises, Emden, les papeteries et Erfurt–Eichsfeld ne sont pas modifiés.

L’inventaire compare les pays effectifs à des juridictions identifiées et aux dossiers conservés. Il contient également des groupes (Solms, Isembourg, Hohenlohe, Oettingen...) dont les branches restent à inventorier. Les lignes sans souverain vérifié ou sans carte précise restent C. Un lien de catalogue dans ces lignes est une piste, pas une preuve de frontière. Une participation d’un TAG à un lot ne valide pas tous ses territoires.

## Correction réellement installée

**Un nouveau pays : FUL, prince-évêché de Fulda, Heinrich VIII von Bibra.** Noyau intérieur de Fulda–Hünfeld–Neuhof : **39 cellules transférées**, quatre nouveaux RGB. Les limites sont une généralisation B tirée de la carte institutionnelle de Hesse 1789, sous réserve de continuité du noyau sous le même souverain depuis 1759 ; pas un cadastre de 1776.

| Parent RGB | Région économique | Propriétaire avant/après | RGB après | Cellules |
| --- | --- | --- | --- | ---: |
| xD04121 | STATE_HESSE | HEK → FUL | xEDB600 | 16 |
| xD04121 | STATE_HESSE | HEK → HEK | xD04121 | 118 |
| xD04121 | STATE_HESSE | HEK → HEK | xEDB601 | 6 |
| xD04121 | STATE_HESSE | HEK → HEK | xEDB602 | 1 |
| xD0C021 | STATE_SAXONY | MEI → FUL | xEDB603 | 23 |
| xD0C021 | STATE_SAXONY | MEI → MEI | xD0C021 | 181 |

Le parent xD0C021 était un résidu MEI inchangé, classé non certifié lors de MAP2T. La cellule historique GOT xEDB40F, ainsi que tous les autres nouveaux noyaux T/U, restent intacts. Le découpage de Fulda traverse deux régions économiques natives : Hesse/74 et Saxe/73. Cela n’attribue pas toute la Saxe à Fulda et ne rouvre pas la reconstruction thuringienne. Capitale technique : STATE_SAXONY ; aucun locator déplacé.

Les RGB parents comptaient 345 cellules : toutes sont conservées. 39 changent de souveraineté et 46 changent de couleur ; sept cellules HEK résiduelles sont seulement séparées en composantes RGB connexes. Une cellule de Würzburg touchée par le polygone est exclue. Geisa, Dermbach, Herbstein et les franges restent ouverts.

La nouvelle appartenance impériale, le registre de jure et la carte du journal sont intégrés par le compilateur existant. Les neuf électeurs et les règles des sujets ne changent pas. FUL n’est pas créé comme sujet natif de l’empereur. Le drapeau à croix noire est provisoire. Lois/technologies : modèle du prince-évêché de Würzburg, abstraction technique documentée.

## Population et économie

Population FUL : **20 047**, dont 14 240 prélevés à HEK/Hesse et 5 807 à MEI/Saxe. Redistribution technique provisoire, **pas** recensement historique. Les profils culturels et religieux restent identiques à l’échelle mondiale ; leurs éventuels défauts historiques ne sont pas corrigés par invention.

Population mondiale : **835,801,255 → 835,801,255**, delta zéro. Bâtiments, PM, propriétaires économiques, unités, recrutements et infrastructures existants sont conservés, sans industrie artificielle. Les données de départ ne permettent pas d’assigner historiquement des installations du reste de la Hesse/Saxe à ce petit noyau ; aucun bâtiment n’est déplacé arbitrairement. La subsistance et la viabilité de FUL restent à vérifier en jeu.

## Vérifications

Contrôles statiques actuels : **1341/1341**. Détail dans VALIDATION.json. Sont vérifiés : bitmap et propriétaires exacts, connexité, références RGB/régions, ressources/capacités inchangées, démographie entière par profil, bâtiments/unités, capitales, localisations FR/EN, références de personnage/gouvernement/drapeau, relecture cumulative du registre et compilation impériale.

- MAP2W_targeted: 17 tests, 0 échecs, 0 erreurs.
- cumulative_contracts: 60 tests, 0 échecs, 0 erreurs.
- earlier_stage_snapshots: 39 tests, 9 échecs, 0 erreurs.

Les anciennes suites MAP2T/U restent exécutées comme photographies d’étape : leurs attentes « monde exact après mon seul lot » et « seulement mes nouveaux pays » ne peuvent inclure FUL ni les lots ultérieurs. Les échecs ne sont ni effacés ni convertis en PASS ; UNIT_TESTS.json conserve les noms et sorties. Les éventuelles divergences économiques/militaires par rapport à ces anciennes baselines sont contrôlées séparément contre la baseline immédiate MAP2W, où elles sont déjà présentes. Aucune attente historique n’est réécrite.

Sur les 39 anciens tests, 30 passent et neuf échouent : sept attentes globales d’étape obsolètes et deux comparaisons économiques/militaires déjà divergentes avant MAP2W. EARLIER_TEST_DIAGNOSTICS.json documente chaque cas. Les 17 tests ciblés et les 60 contrats cumulatifs actuels passent tous. REFERENCE_VALIDATION.json confirme séparément les technologies, lois, culture, religion, groupe d’intérêts et idéologie utilisés par FUL.

Anomalies héritées : **44 doublons RGB et 12 sélecteurs invalides**, identiques à la capture initiale. Aucun accroissement n’est autorisé. Ce PASS local ne signifie donc pas que le mod entier est exempt d’erreurs.

MAP2T, MAP2U et les papeteries : attestation manuelle de l’utilisateur enregistrée séparément dans PREVIOUS_LOTS_RUNTIME_USER_ATTESTATION.json. Elle n’est ni un test automatisé ni une certification historique, et ne valide pas MAP2W.

HEAD conservé : `31556939116deaa1664eb2d25bc91f753f0a7f75`. Empreinte de l’index identique. Aucun staging, commit, push, merge, reset, changement de branche ou modification de l’installation du jeu. La modification nord-américaine des formations militaires déjà présente au départ reste byte-identique et n’est pas un changement MAP2W.

## Suite proposée, sans la commencer automatiquement

1. MAP2W-R2 : Hesses/Nassau, différences de branches et compléments de Fulda après validation du noyau.
2. MAP2W-R3 : Hohenlohe, Castell, Wertheim et villes franconiennes encore absentes ; préserver les noyaux déjà validés.
3. MAP2W-R4 : Freising, Passau, Ratisbonne et principales juridictions bavaroises ; Bavière et Palatinat ont encore des souverains distincts au 1er janvier 1776.
4. Compléments souabes ciblés seulement avec preuves nouvelles : ne pas recommencer les quatre passes déjà installées.

## Fichiers fonctionnels modifiés/ajoutés

- `common/coat_of_arms/coat_of_arms/1776_map2w_fulda.txt`
- `common/country_definitions/1776_map2w_fulda.txt`
- `common/customizable_localization/1776_imperial_reply_lists.txt`
- `common/flag_definitions/1776_map2w_fulda.txt`
- `common/government_types/00_1776_map2w_fulda.txt`
- `common/history/characters/ful - map2w.txt`
- `common/history/countries/ful - map2w.txt`
- `common/history/pops/00_west_europe.txt`
- `common/history/power_blocs/00_power_blocs.txt`
- `common/history/states/00_states.txt`
- `common/journal_entries/1776_imperial_situation.txt`
- `common/power_bloc_identities/1776_imperial_federation.txt`
- `common/scripted_buttons/1776_imperial_voting.txt`
- `common/scripted_effects/1776_imperial_constitution.txt`
- `common/scripted_triggers/1776_imperial_centralization.txt`
- `common/scripted_triggers/1776_imperial_constitution.txt`
- `events/1776_imperial_constitution_events.txt`
- `gfx/interface/journal_entries/aor1776_hre_registered_map.dds`
- `localization/english/1776_imperial_constitution_l_english.yml`
- `localization/english/1776_imperial_electoral_choices_l_english.yml`
- `localization/english/1776_imperial_feedback_l_english.yml`
- `localization/english/1776_imperial_repairs_l_english.yml`
- `localization/english/1776_map2w_l_english.yml`
- `localization/french/1776_imperial_constitution_l_french.yml`
- `localization/french/1776_imperial_electoral_choices_l_french.yml`
- `localization/french/1776_imperial_feedback_l_french.yml`
- `localization/french/1776_imperial_repairs_l_french.yml`
- `localization/french/1776_map2w_l_french.yml`
- `map_data/province_terrains.txt`
- `map_data/provinces.png`
- `map_data/state_regions/00_west_europe.txt`

Outillage et preuves : tools/map2w_west_south.py, tools/map2w_tables.mjs, tools/test_map2w_west_south.py, garde étroite dans tools/map2l_registry.py, ce dossier de rapport et l’image source de la carte du journal dans workshop_pack/source. La liste fonctionnelle est comparée à la capture immédiate et n’inclut pas à tort tous les fichiers sales de Git.

## ColGrep

Deux tentatives d’appel de `C:/Users/simeo/.cargo/bin/colgrep.exe --agent` : première bloquée par le verrou d’index hors workspace, seconde relancée avec accès à l’index existant. Une actualisation incrémentale et une session agent (réflexion et commandes de localisation) ont été observées. La sortie finale ne fournit pas de localisation exploitable et vérifiée utilisée pour cette livraison. Recherche documentaire finale par fichiers déjà connus et identifiants exacts. Pas de reconstruction complète d’index ni de changement de modèle. Temps et tokens exacts non récupérés, aucune économie de quota chiffrée revendiquée.
