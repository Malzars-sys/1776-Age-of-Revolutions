# MAP-2U — Noyaux complémentaires de Thuringe installés

Situation visée : 1er janvier 1776. **MAP2U_READY_FOR_SCOPED_RUNTIME_VALIDATION**.

Le lot installe les deux comtés distincts et un noyau septentrional de SSO. Il ne certifie pas les limites de toutes les possessions dispersées. Aucun test moteur MAP2U n’est revendiqué.

## Avant / après

| Secteur | Avant | Après | Cellules transférées | Population technique du pays |
|---|---|---|---:|---:|
| Lobenstein | WEI, xC00A37 | RLO, xEDB503 | 3 | 2056 |
| Résidence d’Ebersdorf | WEI, xC00A37 | REB, xEDB502 | 1 | 1739 au total |
| Noyau de Hirschberg | SAX, x31E0C0 | REB, xEDB500 | 1 | inclus ci-dessus |
| Sondershausen nord | PRU, x3C9B93 | SSO, xEDB501 | 16 | 11555 dont 4821 au nord |

**21 cellules**, quatre RGB nouveaux xEDB500–xEDB503. Région 73 STATE_SAXONY pour les Reuss; région 62 STATE_ANHALT pour Sondershausen. Le nom technique de cette dernière région ne signifie pas une annexion des principautés d’Anhalt: leurs pixels, propriétaires et populations sont inchangés. Le registre passe de 537 à 541 RGB, sans extension physique de l’Empire.

RLO est un comté sous Heinrich II, REB sous Heinrich XXIV. Le rang technique natif « principality » ne dispose pas d’un équivalent « county »: le gouvernement et les titres affichés sont bien comtaux. Pas d’élévation princière de 1790 ou1806 appliquée d’avance, ni d’union de 1824. Drapeaux temporaires: mêmes armes dynastiques simplifiées que les autres Reuss, sans union politique. Les lois et technologies de départ reprennent le modèle existant COB, non un audit institutionnel complet.

SSO reste un seul pays, avec ses 12 cellules méridionales intactes et 16 cellules au nord. Sa région capitale technique est désormais STATE_ANHALT, où se trouve le point diagnostique de Sondershausen; aucun locator n’est créé ou déplacé. La région capitale du jeu ne certifie pas l’emplacement d’une ville physique.

## Portée géographique

Toutes les attributions installées sont des **généralisations B**. Les sources institutionnelles établissent les souverainetés; les cartes comparatives guident les contours intérieurs. Aucune borne indépendante d’erreur locale n’est établie. Le profil diagnostique est conservé, sans nouvelle optimisation ni translation 7,20 pixels. Les ajustements des nouvelles feuilles ne constituent pas un recalage de la projection du jeu.

Le territoire résidentiel d’Ebersdorf est étroit: sa trace intérieure n’occupe qu’environ 12,6 % de la cellule 4365/845. Une seule cellule est retenue pour représenter ce noyau, abstraction explicite de résolution, pas l’attribution de toute la province voisine. Hirschberg est séparé; aucun corridor ne les relie. Le point géographique diagnostique de Hirschberg est proche d’une limite de cellule: son noyau n’est pas une position urbaine certifiée.

Les prolongements Wurzbach/Oßla tombant sur SCW sont laissés inchangés, faute de séparation locale assez sûre pour rouvrir Rudolstadt. Les franges vers Keula/STATE_BRUNSWICK et les prolongements Ebeleben–Clingen sont différés. Ces derniers rencontrent le rectangle de protection d’Erfurt, qui couvre aussi des terrains bien au-delà de la ville. Ce rectangle n’est pas une frontière historique d’Erfurt. Toutes ses cellules restent identiques.

Voir [carte avant/après](THURINGIA_BEFORE_AFTER.png), [repérage moderne et dans le jeu](PLAYER_LOCATION_GUIDE.png), les trois audits et UNRESOLVED.csv. Les résidus inchangés ne sont pas validés comme historiquement corrects. Les petites enclaves ne prolongent pas ce lot.

## Population et économie

Population mondiale mesurée avant/après: **835 801 255**, delta 0. Ce total n’est pas une obligation historique; il résulte ici d’une redistribution technique provisoire. Les chiffres du tableau ne sont pas des recensements 1776. Des inventaires démographiques sont repérés, mais sans valeurs consultables au périmètre de ces noyaux, aucune estimation historique n’est appliquée. Pas de compensation ailleurs ni d’ajout artificiel.

MAP2U conserve les profils culture/religion, bâtiments, niveaux, PM écrits, propriétaires économiques, ressources, capacités agraires, unités et recrutements. Trois fichiers de bâtiments ont toutefois été modifiés en parallèle par un autre travail du workspace: leur différentiel exact est enregistré dans EXTERNAL_BUILDINGS_OBSERVED.json et conservé, sans être attribué à ce lot. HLB reste à 9206 habitants. Les six pays MAP2T et leurs noyaux sont conservés. Aucun bâtiment ni formation n’est fabriqué pour les nouveaux comtés; leur viabilité en nouvelle partie doit être contrôlée.

## Validation et coexistence

**871/871** contrôles statiques. **22/22** tests ciblés et **60/60** tests de contrats impériaux. Les 73 sorties du compilateur impérial sont vérifiées avant puis après;17 reçoivent seulement les membres et droits supplémentaires. Les 44 doublons RGB et 12 références invalides préexistants restent inchangés. Aucun nouvel électeur ni sujet natif de l’empereur. Les mécanismes HRE-CENTRALIZATION, icônes et prototypes sont préservés.

Les 66 tests d’étapes anciennes donnent52 succès et 14 échecs, détaillés dans LEGACY_TEST_TRIAGE.md. Sept étaient déjà signalés lors de MAP2T; quatre attentes globales de MAP2T deviennent dépassées, ainsi que l’ancienne assertion qui exigeait tous les pixels prussiens immuables. Deux comparaisons économiques anciennes rencontrent aussi les changements de bâtiments parallèles. Les principautés d’Anhalt et les 121 transferts/16 RGB de MAP2T sont vérifiés directement et restent intacts. Aucune ancienne baseline ou assertion n’est réécrite.

Des modifications concurrentes de 141 fichiers ont été observées avant installation, sans chevauchement des cibles territoriales. Elles sont conservées dans un constat additif PREINSTALL_CONCURRENT_SNAPSHOT.json, séparé de la baseline initiale immuable. Trois changements supplémentaires de bâtiments sont apparus après installation: papier, exploitation forestière et élevage, avec un delta global observé de+8/+2/+5 niveaux respectivement. Ces trois fichiers ont été lus et leurs empreintes, contenus et différences canoniques sont conservés dans EXTERNAL_BUILDINGS_OBSERVED.json. Il ne s’agit ni de modifications MAP2U ni d’une validation historique de cet équilibrage. Le contrôle final rejoue exclusivement ces deltas explicitement observés et les modifications territoriales déclarées; les autres données restent strictement protégées.

La validation manuelle MAP2T est enregistrée dans MAP2T/RUNTIME_USER_ATTESTATION_MAP2U.json: six nouveaux États, dignité saxonne, mécanismes, économies et un mois sans erreur signalée. Il s’agit du test du joueur, pas d’un test moteur automatisé ni d’une certification de toutes les frontières. MAP2U reste **NOT_TESTED_MAP2U**.

## Fichiers fonctionnels modifiés

- `common/country_definitions/1776_map2t_saxony.txt`
- `common/country_definitions/1776_map2u_reuss.txt`
- `common/customizable_localization/1776_imperial_reply_lists.txt`
- `common/flag_definitions/1776_map2u.txt`
- `common/government_types/00_1776_map2u.txt`
- `common/history/characters/reb - map2u.txt`
- `common/history/characters/rlo - map2u.txt`
- `common/history/countries/reb - map2u.txt`
- `common/history/countries/rlo - map2u.txt`
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
- `localization/english/1776_map2u_l_english.yml`
- `localization/french/1776_imperial_constitution_l_french.yml`
- `localization/french/1776_imperial_electoral_choices_l_french.yml`
- `localization/french/1776_imperial_feedback_l_french.yml`
- `localization/french/1776_imperial_repairs_l_french.yml`
- `localization/french/1776_map2u_l_french.yml`
- `map_data/province_terrains.txt`
- `map_data/provinces.png`
- `map_data/state_regions/00_west_europe.txt`

Outils nouveaux: map2u_thuringia.py, test_map2u_thuringia.py, map2u_tables.mjs. L’extension de map2l_registry.py est explicitement limitée aux trois parents de ce lot et au seul changement de région capitale de SSO. Les rapports antérieurs restent intacts; seule une attestation additive est ajoutée pour MAP2T.

HEAD et index Git inchangés. Aucun commit, merge, reset, push, changement de branche ou écriture dans l’installation du jeu. Aucune autre région commencée.

## Recherche locale

Aucun appel ColGrep redondant: les fichiers, identifiants et outils nécessaires étaient déjà localisés par MAP2T et par le prompt. Les lectures exactes ont été vérifiées localement. Cette passe ne mesure donc ni une exécution2B ni une économie de quota. Les compteurs de tokens Codex ne sont pas accessibles.
