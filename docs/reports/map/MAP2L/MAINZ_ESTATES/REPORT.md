# MAP2L — Possessions de Mayence : Bergstraße et Main–Spessart

Statut : **lot appliqué, contrôles statiques réussis, test en jeu différé** conformément à la demande d'attendre la fin de tous les lots du Saint-Empire. Aucun commit, staging, merge, rebase ou push.

## Territoires appliqués

Mayence reçoit les fragments tracés de la Bergstraße–Starkenburg (Lorsch, Bensheim, Heppenheim et raccord de Viernheim) et du Main–Spessart (raccord Steinheim/Seligenstadt/Dieburg, Orb, Lohr, Aschaffenburg, Klingenberg, Miltenberg et Amorbach). Les sources, exclusions et réserves sont détaillées dans [GEOGRAPHIC_EVIDENCE.md](GEOGRAPHIC_EVIDENCE.md).

Rieneck n'est **pas** une acquisition mayençaise : la seigneurie est aux Nostitz depuis 1673. Les domaines voisins figurés comme non mayençais restent exclus. Cette passe termine le raccord nommé, pas toutes les possessions de l'électorat.

| State_ID conservé | ID numérique conservé | Transfert de pixels de souveraineté |
| --- | --- | --- |
| STATE_HESSE | 74 | HEK → KMZ : 57 |
| STATE_FRANCONIA | 72 | BAV → KMZ : 99 ; KMZ → contrôleur résiduel BAV : 9 |
| STATE_BADEN | 68 | BAD → KMZ : 62, dont 23 Bergstraße et 39 raccord Miltenberg–Amorbach |

Les neuf pixels rendus au contrôleur résiduel corrigent l'ancien petit noyau d'Aschaffenburg hors du nouveau contour confirmé ; **ils ne certifient pas une souveraineté bavaroise en 1776**. Le résidu BAV de Franconie reste à traiter (552 pixels, contre 642 avant cette passe).

**18 nouveaux identifiants RGB** (`xEDA500` à `xEDA511`), six masques parents explicites et **203 pixels recolorés**. Les subdivisions de couleur peuvent aussi séparer des fragments restant au même propriétaire. RGB du bitmap, State_ID et ID numérique sont distincts. Les trois State_ID restent partagés entre plusieurs pays, sans déplacer les ressources ni les locators.

Le registre de jure passe de 366 à **384 RGB**. Le périmètre jaune reste exactement **62 516 pixels** : les parents figuraient déjà parmi les terres impériales. Carte principale et carte du journal sont régénérées ; leurs textures restent identiques lorsque le périmètre ne change pas. Le contenu territorial des listes et des demandes impériales est recompilé à partir du nouveau registre.

## Fichiers modifiés

Runtime territorial :

- `map_data/provinces.png`, `map_data/province_terrains.txt` et `map_data/state_regions/00_west_europe.txt`.
- `common/history/states/00_states.txt` et `common/history/pops/00_west_europe.txt`.
- `common/history/buildings/98_build_start_1776_world_redistribution.txt`.

Runtime impérial recompilé :

- `common/scripted_triggers/1776_imperial_constitution.txt`.
- `common/scripted_effects/1776_imperial_constitution.txt`.
- `common/power_bloc_identities/1776_imperial_federation.txt`.
- `localization/{english,french}/1776_imperial_feedback_l_{english,french}.yml`.
- `localization/{english,french}/1776_imperial_repairs_l_{english,french}.yml`.

Documentation et outils : registre actif `../IMPERIAL_DE_JURE_REGISTRY.json`, manifeste `REGISTRY_MIGRATION.json`, tracés/alignement, candidats, aperçu avant/après, plan d'allocation, patchs et validations de ce dossier ; nouveau pilote `tools/map2l_mainz_estates.py` et validateur `tools/validate_map2l_mainz_estates.py` ; générateur `tools/map2l_mainz.py`, migrations explicites `tools/map2l_registry.py` et validateurs cumulatifs Belgique/Franconie/Neckar/Mayence adaptés aux subdivisions successives. Les baselines, sources et anciens candidats ne sont pas réécrits.

## Conservation et tests

Population mondiale écrite : **835 804 980**, inchangée. Chaque profil démographique et tous ses attributs restent conservés par région ; cultures et religions explicites ou résolues sont contrôlées. Les transferts reposent sur les superficies des subdivisions sources complètes : approximation de gameplay, pas recensement historique.

Transferts démographiques du seul nouveau lot : 49 092 BAD → KMZ, 50 731 HEK → KMZ, 73 024 BAV → KMZ et 6 639 KMZ → BAV. Le gain net mayençais est **166 208 habitants**, sans création ni disparition.

Deux niveaux d'élevage sont redistribués à des subdivisions KMZ (un en Bade et un en Hesse). Total des niveaux, méthodes de production, réserves et attributs sont conservés, ainsi que les propriétaires économiques privés et leurs niveaux. Les bâtiments ne sont donc **pas tous byte-identiques**, mais les fichiers hors allocations explicites le restent. Les populations sont réparties une seule fois depuis les scopes originaux : les fragments reçus ne sont pas retraités comme de nouvelles populations sources.

Résultats des commandes, exécutées sans lancer Victoria 3 :

- `tools/validate_map2l_mainz_estates.py` : **477/477**.
- `tools/validate_map2l_mainz.py`, lot initial contrôlé cumulativement : **491/491**.
- `tools/validate_map2l_rhine.py` : **408/408**.
- `tools/validate_map2l_franconia.py` : **535/535**.
- `tools/validate_map2l_belgium.py` : **315/315**.
- `tools/map2l_piedmont.py validate` : **232/232**.
- Carte principale : **16/16 hors moteur**, DDS sans perte et helper HLSL compilé ; ni chargement en jeu ni compilation complète du shader par Victoria 3 n'ont été vérifiés.

Les contrôles couvrent notamment : propriétaires exacts, absence de nouvelle double attribution ou référence orpheline, RGB enfants confinés à leurs parents déclarés, connexité, matrices reproduites et exclusions respectées, Fulda/Francfort/Würzburg inchangés, conservation démographique et économique, ID/ressources/locators inchangés, terrains hérités, registre exact, compilation impériale reproductible, fichiers protégés, HEAD et index Git inchangés.

Les **44 RGB doublement attribués et 12 erreurs de référence préexistants** restent identiques à la baseline. Ce ne sont pas de nouvelles régressions, ni des anomalies corrigées par ce lot. Détails dans `VALIDATION.json`.

## Limites et suite

Restent à traiter séparément les prolongements méridionaux du Tauber/Jagst (Buchen, Tauberbischofsheim, Krautheim), Erfurt/Eichsfeld, le noyau grossier de Mayence et le complément du Rheingau, ainsi que les propriétaires résiduels et le Palatinat occidental. Les micro-enclaves invisibles sont abstraites sans agrandissement. Les tracés de jeu ne sont pas des frontières cadastrales. Le prochain lot cohérent est le prolongement méridional mayençais, avec ses dépendances aux États voisins.

## ColGrep

**Un appel `--agent`** a localisé les dossiers conservés, dans `./docs/reports/map/MAP2L`, avec la question : « Locate the retained primary-map images and provenance for the Le Rouge map already used to corroborate the Franconia lot, plus any existing usable alignment covering the western Main-Spessart Mainz estates. Return verified file paths and line numbers only. Do not edit files, do not research the web, do not decide ownership. » Exécutable : `C:/Users/simeo/.cargo/bin/colgrep.exe`.

Résultats vérifiés : `FRANCONIA/GEOGRAPHIC_EVIDENCE.md:7` et `FRANCONIA/TRACING.json:1–24`. Localisation utile mais **partielle** : pas de calage occidental utilisable ni de nouvelle attribution historique fournis. Les fichiers et lignes ont été relus avant utilisation. Le backend GPU/llama.cpp et le temps d'inférence ne sont pas attestés par une bannière capturée pour cet appel ; aucun réglage ni modèle n'a été changé.

La réutilisation des dossiers évite une recherche exploratoire plus large, sans pouvoir en chiffrer le nombre de recherches ou les tokens économisés. Les appels classiques du tour n'ont pas été comptés exhaustivement, les compteurs de tokens Codex par opération ne sont pas accessibles et aucune comparaison A/B n'a été réalisée. Les bitmaps, DDS et coordonnées sont inspectés directement, pas décidés par le modèle 2B. L'intérêt observé est la localisation initiale de documents ; l'analyse historique, le calage et les tests constituent l'essentiel de cette passe.

L'actualisation incrémentale finale de l'index est consignée dans `COLGREP_REFRESH.md` ; elle n'est pas une exécution de l'agent 2B et ne reconstruit pas volontairement l'index.
