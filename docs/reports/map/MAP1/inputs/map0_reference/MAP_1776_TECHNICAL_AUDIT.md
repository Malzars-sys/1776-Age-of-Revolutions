# MAP-0 — Audit technique de la carte

Audit local, 2026-10-10; pas de recherche historique exécutée.
Exécutable installé : `C:/Games/Victoria 3/binaries/victoria3.exe`, FileVersion et
ProductVersion **1.13.11**. Le fichier d'empreintes v1.13.9.xxh128 encore présent
ne suffit pas à identifier la version de l'exécutable. Descriptor du mod : 1.13.*.
Départ fixé par `common/defines/00_defines.txt` à `1776.1.1`.

## Référence mesurée

Bitmap natif : 8192 × 3616, RGB. **40 875 couleurs/provinces réelles** :
40 717 terrestres, 106 marines, 52 lacs. Il n'y a pas de couleur de fond exclue
arbitrairement. SHA-256 :
`e3911fd80a40c6b297a68f66e898d9b187863b64483a9608123606143ee2ea78`.
675 États terrestres; 781 State Regions en incluant les 106 marines.
1 043 couples initiaux Owner_TAG + State_ID, sans fusion des États partagés.
La baseline contient 40 928 lignes : une province à propriétaires contradictoires
occupe plusieurs lignes, pas plusieurs provinces. Elle inclut mers et lacs avec
Region_ID vide; une attribution politique à un lac reste visible comme anomalie.

Toutes les couleurs du bitmap sont couvertes par une State Region ou la liste des
lacs. Aucun nouveau pixel/province ni regroupement géographique n'est observé par
rapport au vanilla installé. Les 16 fichiers régionaux du mod changent notamment
les ressources et paramètres du scénario; leurs listes `provinces` sont identiques
aux listes vanilla. **10 223 provinces / 251 États** ont des attributions historiques
différentes du vanilla installé de 1836 : c'est un écart technique de scénario,
pas un décompte de corrections historiquement exactes.

Les anciens travaux cartographiques identifiés du collaborateur ont changé 519
attributions dans huit États. Le candidat nouveau change trois provinces dans
deux États propriétaires, et introduit en plus une corruption textuelle en
Bessarabie. Les mentions Collaborator_Preexisting_Edit sont des drapeaux par
État, pas l'affirmation que toutes ses provinces ont changé.

## Fichiers réellement présents et chargement

Racine native vérifiée : `C:/Games/Victoria 3/game`. Les chemins ci-dessous sont
relatifs à cette racine ou à celle du mod selon la colonne. L'inventaire assemble
les fichiers vanilla et les remplacements mod de même nom; il n'exécute pas les
effets conditionnels. Les seuls replace_path du descriptor concernent les eras et
technologies, pas map_data ou les historiques.

| Chemin réel | Origine / rôle |
|---|---|
| map_data/default.map | Natif hérité : noms des ressources, sea_starts, lakes, wrap_x. |
| map_data/provinces.png | Natif hérité : couleur RGB unique = province, identifiée `xRRGGBB`; pas de definition.csv dans cette installation. |
| map_data/province_terrains.txt | Natif hérité : terrain par couleur de province. |
| map_data/state_regions/00_west_europe.txt … 15_russia.txt | 16 remplacements mod : identifiants d'État numériques, provinces, ressources, terre arable, traits, hubs et sorties navales. |
| map_data/state_regions/99_seas.txt | Natif hérité : 106 régions marines, IDs numériques autour de 3000. |
| map_data/state_regions/state_regions.md | Documentation native des champs : lue pour interprétation, pas un script du mod. |
| map_data/adjacencies.csv | Natif hérité : connexions spéciales/détroits, colonnes From/To/Type/Through, coordonnées et règles. Les contacts terrestres ordinaires viennent du bitmap. |
| map_data/rivers.png | Natif hérité : tracés fluviaux; pas un propriétaire politique. |
| map_data/heightmap.heightmap, heightmap.png, indirection_heightmap.png, packed_heightmap.png, nodes.dat | Ressources natives héritées de relief/topologie et données dérivées; ne pas fabriquer leur format binaire. |
| common/history/states/00_states.txt | Mod : create_state/country/owned_provinces, états divisés, homelands et claims. Une revendication n'est pas une propriété. |
| common/country_definitions/00_countries.txt, 02_modded_countries.txt | Mod + union native : TAGs, types recognized/unrecognized/decentralized, cultures et capitale par défaut. |
| common/strategic_regions/*_strategic_regions.txt | Sept fichiers natifs hérités : african, east_asia, europe, north_america, south_america, water, west_south_asia. Regroupent les États, capital_province et couleur. Aucune surcharge dans le mod. |
| common/history/pops/*.txt, population/*.txt | Mod + fichiers natifs non remplacés : populations/cultures/religions et paramètres démographiques par scope. Pas de coordonnées de population par province. |
| common/history/buildings/*.txt | Mod + héritage : bâtiment dans region_state, PM, réserves et niveaux détenus par pays/bâtiments investisseurs. Les fichiers 98_* doivent aussi être examinés. |
| common/history/military_formations/*.txt, military_deployments/*.txt | Recrutement state_region, services réguliers/conscrits, HQ stratégique, formations/navires et déploiements. |
| common/history/diplomacy/*.txt, treaties/*.txt, power_blocs/*.txt, trade/*.txt | Sujets, pactes, relations, traités, blocs et commerce : dépendances d'un changement de pays/port. |
| common/history/countries/*.txt, characters/*.txt, global/00_global.txt, common/on_actions/00_code_on_actions.txt | Initialisation politique, capitales éventuelles, personnages et effets de démarrage; exigent un contrôle moteur pour l'état final. |
| localization/english/**/*.yml, localization/french/**/*.yml | Clés State_ID/TAG et noms dynamiques; union native/mod. Définition d'une clé ne garantit pas l'absence d'erreur de format ou son affichage dynamique. |
| gfx/map/fleet_entities/10_1776_early_ships.txt | Seul fichier gfx/map du fork : entités de flotte, pas géométrie des provinces. |
| gfx/map/map_object_data/generated/*.bin, gfx/map/spline_network/spline_network.splnet | Natifs hérités : locators/objets et réseau graphique. Des exports pourraient devenir nécessaires en méthode C. |
| gfx/map/spline_network/game_road_data.txt; gfx/map/terrain, rivers, water, borders, masks | Natifs hérités : routes affichées et habillage géographique. Aucun remplacement géométrique du fork constaté. |

Le port est un hub dans une province de State Region; naval_exit_id renvoie à un
ID de région marine. Ni l'accès au marché ni le recrutement d'une marine ne sont
prouvés par la seule validité de cet ID. Tester côte, connectivité et bâtiments.
Les neuf régions de recherche ne sont **pas** les régions stratégiques du moteur.

## Catalogue canonique : pertinent mais pas figé

Catalogue retrouvé : `docs/reports/buildings/BUILD_START_1776_RESEARCH_REGIONS.csv`.
Toujours 1 043 lignes et 675 États, mais **20 différences de membres de couples**,
donc ensemble non identique au départ actuel. Elles concernent les anciens
transferts cartographiques et les cinq régions égyptiennes passées TUR→EGY.
Conserver ce fichier original; utiliser les couples actuels reconstruits pour la
carte. Les anciens 8 couples EXCLUDED_SERENISSIMA ne sont plus une exclusion :
9 couples actuels VEN/GEN sont inclus et marqués Protected_Specific_History=YES.

MAP_1776_9_REGIONS.csv contient la liste complète Province_IDs pour chaque couple.
Dans la baseline, Owner_State_Key permet cette jointure sans répéter cette longue
liste sur chaque province. State_ID désigne la géographie; Ownership_History_State_IDs
conserve le scope historique lorsque celui-ci est incohérent. Owner_Name et
State_Display_Name reprennent les libellés du catalogue lorsqu'ils existent, sinon
le TAG/ID; ils ne prétendent pas reproduire le nom dynamique exact de l'interface.
Proposed_Historical_Owner_TAG reste vide partout.

### Allocation des neuf missions

| Identifiant canonique | États | Couples pays/État |
|---|---:|---:|
| R1_WESTERN_EUROPE | 73 | 82 |
| R2_NORTHERN_CENTRAL_EASTERN_EUROPE | 136 | 164 |
| R3_MIDDLE_EAST_NORTH_AFRICA_CAUCASUS_CENTRAL_ASIA | 93 | 145 |
| R4_SOUTH_ASIA | 29 | 54 |
| R5_EAST_ASIA | 75 | 84 |
| R6_SOUTHEAST_ASIA_OCEANIA | 52 | 130 |
| R7_SUBSAHARAN_AFRICA | 71 | 196 |
| R8_NORTH_AMERICA_CARIBBEAN | 93 | 125 |
| R9_SOUTH_AMERICA | 53 | 63 |
| Total | 675 | 1 043 |

Les listes exactes d'États/TAGs sont dans chaque prompt et les listes de provinces
dans 9_REGIONS.csv. Les exceptions géographiques corrigent les classements par
nom de fichier : Groenland→R8, Hawaii et Birmanie/Indochine→R6, États des steppes
dans le fichier russe→R3, Sibérie russe→R5, zones sahéliennes stockées en Afrique
du Nord→R7, Tibet→R5. Un principal et un secondaire sont renseignés aux interfaces
alpine/adriatique, ottomane, caucasienne, himalayenne, sahélienne et autres frontières
de mission. Ces conventions répartissent le travail, pas la souveraineté de 1776.

Sovereign_TAG est seulement la fin d'une chaîne de pactes initiaux explicites non
conditionnels; les chaînes multiples/conditionnelles restent indéterminées.
NO_INITIAL_SUBJECT_PACT_FOUND ne signifie pas indépendance historique. Les effets
de démarrage, changements de bloc, traités et autonomie politique ne sont pas
simulés; une souveraineté historique doit être sourcée séparément.

## Anomalies et dépendances

Le registre distingue MAIN_WORKING_TREE et COLLABORATOR_CANDIDATE.
Main contient 53 provinces à attributions multiples incompatibles et 11 répétées
pour le même propriétaire. Il contient six occurrences de propriétaire/scope
hors de la géographie déclarée (dont le lac xBD5671 en Gansu et les Silésies),
trois sélecteurs de pops et six de bâtiments sans couple territorial correspondant.
xEF50C0 dans West Micronesia est non possédée sans impassable déclaré : à examiner,
pas à attribuer automatiquement. Les capitales non possédées et écarts au catalogue
restent des points de revue, pas des crashs démontrés.

Les doublons contradictoires concernent notamment le Maghreb/Sahara, le Caucase,
l'Amérique du Nord, l'Afrique orientale et quelques autres États; les identifiants
exacts figurent dans le CSV, sans décision historique inventée. Les
sélecteurs orphelins concernent Algiers/Constantine/Oran (pops et bâtiments FRA),
Brest/RUS, Chiapas/UCA et Pastaza/SC2 (bâtiments). Le candidat ajoute deux
sélecteurs de bâtiments LUX orphelins et un conflit lombard.

### À migrer systématiquement pour un transfert A

Owner/state scopes de pops et bâtiments; conservation des effectifs et de leur
composition; niveaux et investisseurs; existence du pays, capitale effective et
références directes. Préserver propriété économique étrangère : ce n'est pas la
souveraineté territoriale. Une province transférée ne permet pas une redistribution
proportionnelle automatique de tous les habitants de la State Region.

### À examiner selon le cas

Recrutement et casernes, formations/HQ, bases navales et ports; incorporation,
infrastructure et centre urbain, potentiel naturel et hubs; sujets et pactes,
traités/commerce, journaux/décisions et événements ciblant un pays/État. En B,
toutes les références de State_ID et régions stratégiques deviennent obligatoires;
en C s'ajoutent raster, connexions, relief et exports graphiques.

Les histoires de population et bâtiments sont agrégées au sous-État : la géométrie
ne fournit pas une ventilation démographique fiable. Le total de tailles create_pop
écrit ici est 835 804 980, **pas** une population en jeu calculée après initialisation.

## Limites de l'audit

Les tests sont statiques, non une certification de chargement du jeu. La géométrie
native est couverte mais la connectivité terrestre/coastline n'est pas reconstruite
pixel par pixel. Les identifiants des connexions explicites, hubs, sorties navales,
terrains et présence des clés de localisation sont vérifiables; leur comportement
visuel et dynamique reste à tester. Le parseur auxiliaire vérifie structure et
certains tokens interdits, pas toute la grammaire des effets Victoria 3.

Aucune zone nécessitant C n'est encore prouvée. Les preuves historiques et le
mapping fin doivent précéder un prototype géométrique. Les risques principaux
sont le doublon d'appartenance, la perte de populations/bâtiments, les références
à un pays disparu et une migration incomplète des ressources dérivées.
