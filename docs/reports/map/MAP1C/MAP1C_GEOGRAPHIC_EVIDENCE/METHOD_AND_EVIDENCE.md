# MAP-1C — Méthode, sources et limites d'application

## Coordonnées et modèles

`GEODETIC_CONTROL_OBSERVATIONS.json` conserve séparément : ID et date du point GeoNames contemporain, latitude/longitude WGS84, observation du scan 1600 pixels, locator du jeu, rôle initial, résidu du modèle et résidu leave-one-out. Une coordonnée contemporaine peut servir à situer une ville, **pas à attribuer son territoire en 1776**, ni à localiser au mètre son centre ancien. Les pixels des locators ne sont pas des latitudes/longitudes.

Projection locale de diagnostic : est = 111,32 × cos(latitude centrale) × différence de longitude; nord = 111,32 × différence de latitude, en kilomètres. Ce développement local n'est pas une projection géodésique de précision. Deux modèles : affine à six paramètres et similitude à quatre paramètres, avec inversion nord/y du raster. Quatre observations FIT par dossier; trois témoins CHECK au Luxembourg et en Silésie, deux en Lombardie. Bergame/Brescia restent DIAGNOSTIC, sont évalués et participent à la validation croisée sur tous les points. Rien n'est supprimé pour améliorer les chiffres.

**Important :** ces modèles testent les observations héritées, ils ne les authentifient pas. La relecture de `lux_control_review_north.png` et `lux_control_review_south.png` montre notamment des décalages entre points hérités et symboles de Bruxelles, Namur et Reims. Il faut reprendre explicitement l'identification des symboles, en conservant les anciennes coordonnées et leurs résidus. Les fichiers `*_independent_geodetic_scan.png` affichent ces observations et leurs écarts, **pas une nouvelle frontière**. Aucun modèle calculé ici n'est admis pour un transfert.

### Résultats conservés, non utilisés pour attribuer les RGB

| Dossier | Affine WGS84 → scan, maximum CHECK (pixels du scan) | Similitude WGS84 → scan, maximum CHECK | Affine WGS84 → locators, maximum CHECK (pixels jeu) | Similitude WGS84 → locators, maximum CHECK |
|---|---:|---:|---:|---:|
| Luxembourg | 95,26 | 305,51 | 8,74 | 13,26 |
| Lombardie | 84,68 | 141,35 | 2,22 | 5,32 |
| Silésie | 116,28 | 72,02 | 20,05 | 8,45 |

Le maximum leave-one-out affine des locators lombards monte à **17,53 pixels** lorsque les deux locators contestés sont retenus. La faible erreur des deux seuls témoins CHECK ne doit donc pas masquer Bergame/Brescia. Le changement de modèle en Silésie n'efface pas l'erreur MAP-1B d'Olomouc (**27,864 pixels jeu**), enregistrée dans le fichier source intact. Les résultats des différentes chaînes ne sont ni additionnés comme des mesures indépendantes, ni traités comme des intervalles de confiance.

`MAP1C_MAPPING_DECISIONS.csv` compare cette référence MAP-1B à la petite dimension de chaque boîte englobante. Cela indique une échelle de risque, non la largeur effective de tous les passages du polygone. La géométrie exacte reste celle des runs de pixels de MAP-1; aucune simplification SVG ni boîte englobante ne remplace le contour.

## Repères physiques, indépendants des hubs : essai rejeté comme calage probant

Les fichiers `*_game_rivers_grid.png` proviennent de `C:/Games/Victoria 3/game/map_data/rivers.png` (8192 × 3616), avec grille de pixels. Les fichiers `*_game_rgb_grid.png` montrent le découpage exact, avec étiquettes intérieures issues de l'index MAP-1.

Les données Natural Earth modernes ont été comparées aux réseaux visibles. En Lombardie, des confluences sont repérables dans le bitmap, notamment aux pixels **(4301,997), (4319,1000), (4355,1005)**. Elles ne sont pas toutes suffisamment identifiées : la branche au dernier point arrive du sud, et **ne peut donc pas être assimilée au Mincio descendant du Garda par simple proximité**. Les deux premières constituent des hypothèses de travail Ticino/Adda, pas trois ancrages certifiés. Un ajustement exact sur trois points presque alignés, ou sur des sources de rivières supposées, donnerait une fausse précision. Il n'a pas été retenu.

Dans les deux autres dossiers, les confluences et détails topographiques actuellement reconnus ne donnent pas un réseau local de points non colinéaires suffisamment identifié, avec témoins indépendants. Les lacs modernes ne correspondent pas automatiquement à des provinces lacustres du bitmap. Le jeu schématise les cours d'eau; Natural Earth à 1:10 millions les généralise aussi. L'affirmation « calage indépendant validé » serait donc prématurée. Cet échec est une limite enregistrée, pas un point défavorable retiré d'un ajustement.

## Sources : documents, passages et ce qu'ils ne prouvent pas

Les pièces MAP-1B restent intactes dans `../../MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/`; la notice complète est `../../MAP1B/MAP1B_HISTORICAL_SOURCES.md`.

- **LUX-01 : Janvier, 1771, planche 6.** Scan entier et nouveaux extraits du secteur Namur–Luxembourg. [Notice/scan](https://commons.wikimedia.org/wiki/File:1771_Janvier_Map_of_Belgium_and_Luxembourg_-_Geographicus_-_BelgiumLuxembourg-janvier-1771.jpg). Localités et juridictions générales, pas recensement villageois du 1er janvier 1776.
- **LUX-02 : Uhrmacher / ANLux.** [Étude des cartes CP-A-45/46](https://anlux.public.lu/dam-assets/actualites/2016/pdf/anlux-cp-a-45-beschreibung-von-karte-und-akte.pdf), passages déjà examinés pp.2–3,5,7–10; [notice des cartes](https://anlux.public.lu/de/actualites/2016/Carte.html). Distingue limites, prétentions et condominium, dont Pronsfeld; les pièces originales de mai 1776 ne sont pas nouvellement dépouillées ici. Cadre du duché habsbourgeois, pas preuve des pixels voisins.
- **LUX-03 : ANLux, fonds anciens/cadastre Marie-Thérèse.** [Fonds anciens](https://anlux.public.lu/fr/rechercher/fonds-collections/fonds-anciens.html), [notice du cadastre](https://anlux.public.lu/fr/actualites/2023/mise-en-ligne-cadastre-marie-therese.html). Notices seulement : l'option de sujet AUS/LUX est un compromis de représentation, pas le résultat d'un dépouillement complet du duché.
- **LOM-01/-02 : Vaugondy, feuillets occidentaux/orientaux, 1750**, scans BnF via Commons conservés en MAP-1B, cartouches 1750. Repères territoriaux et hydrographiques; pas des frontières administratives fines certifiées à la cible.
- **LOM-03 : Regione Lombardia, [Lombardia austriaca, 1749–1796](https://www.lombardiabeniculturali.it/istituzioni/schede/8000357/).** Paragraphes paix de 1748 et édit du 10 juin 1757, six provinces et terres séparées. Les réformes de 1786 ne sont pas rétroprojetées.
- **LOM-04 : Regione Lombardia, [Terre Ferme vénitienne](https://www.lombardiabeniculturali.it/istituzioni/storia/?unita=03.03).** Sections Bergame/Brescia/Crema, notamment enclave de Crema et strada cremasca. Des droits documentés sur les villes ne prouvent pas une province du jeu entière.
- **LOM-05, ajout MAP-1C : Regione Lombardia, [Lombardia grigiona](https://www.lombardiabeniculturali.it/istituzioni/storia/?unita=03.04).** Sections Val­tellina, Bormio et Chiavenna : autorité des Trois Ligues durant 1639–1797. Cela établit une piste de changement politique réel au nord, mais pas la correspondance complète de `x9AC196`. Fichier brut `lbc_grigioni.html`, empreinte et URL dans `SOURCE_LEDGER.json`.
- **SIL-01 : Lotter, Silésie 1758.** Scan MAP-1B : carte de duchés pendant la guerre, pas un relevé de la frontière souveraine 1776.
- **SIL-02 : Kuzio-Podrucki, 2022, p.19 imprimée / PDF p.11.** [Article complet](https://zaranieslaskie.bs.katowice.pl/en/article/download/44/18/36). Accords de 1742, démarcation 1743, confirmations 1745/1763. Synthèse académique consultée antérieurement, pas annexes originales village par village.
- **GEO-01 : GeoNames, téléchargement du 10 octobre 2026.** [Données](https://download.geonames.org/export/dump/cities1000.zip), [dictionnaire WGS84 / licence CC BY 4.0](https://download.geonames.org/export/dump/readme.txt). Coordonnées contemporaines uniquement; les ID, dates des lignes et noms sont conservés. Ne pas remplacer les populations historiques par les populations du gazetteer.
- **GEO-02 : Natural Earth, 1:10 millions, domaine public.** [Lacs](https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-lakes/), [rivières](https://www.naturalearthdata.com/downloads/10m-physical-vectors/10m-rivers-lake-centerlines/). GeoJSON du [dépôt du projet](https://github.com/nvkelso/natural-earth-vector), URLs exactes et SHA256 dans le registre. Repères physiques généralisés contemporains, pas limites de souveraineté.

## Manifestes, dépendances et application future

Pour les treize lignes ciblées, le tableau donne les propriétaires **écrits**, y compris les doublons, et la région de définition physique. Les populations et les bâtiments sont par couple État/pays, pas par RGB. `DEPENDENCY_IMPACTS.json` conserve les enregistrements ciblés; `../MAP1/MAP1_DEPENDENCY_REFERENCES.csv` (depuis le répertoire MAP1C) et les dossiers d'État MAP-1 restent les références des capitales, formations et effets. Le nombre de commandes de bâtiments n'est pas une somme des niveaux exécutés.

Un transfert de province exigera un manifeste de conservation des populations/cultures/religions, propriétaires de bâtiments, PM, réserves, districts/manoirs, unités et recrutement; aucune redistribution arbitraire proportionnelle aux pixels. Les corps militaires, événements et autres références sont à contrôler à l'exécution. Il n'est pas acceptable de transférer un RGB pour faire disparaître un sélecteur invalidé.

Pour `x9061E0`, déplacer la référence conserve le propriétaire écrit AUS mais introduit un split AUS dans une région actuellement créée pour GAL seulement. Les populations écrites pour UPPER_SILESIA ne deviennent pas automatiquement celles de ce split : **ce candidat reste conditionnel**. Les deux autres RGB méridionaux gardent un arbitrage AUS/PRU indépendant du scope MORAVIA.

Pour LUX, l'approbation proposée porte uniquement sur le pacte `personal_union`, identifiant déjà utilisé dans `common/history/diplomacy/00_subject_relationships.txt`. Elle ne donne pas carte blanche pour modifier le dirigeant, les lois, les relations ni les frontières. Si le dirigeant existant ne convient pas au lien dynastique, signaler cette dépendance avant application. Tester ensuite sujet, marché, bloc, capitaux, bâtiments et participation militaire dans une nouvelle partie.

Pour la Bessarabie, le patch non appliqué vise uniquement le fichier candidat indiqué par le manifeste technique. `BESSARABIA_SIMULATION_CHECK.json` enregistre l'empreinte du fichier, les cinq tokens retirés en mémoire et l'égalité de l'arbre syntaxique après leur retrait. Aucun propriétaire, claim, homeland ou autre commande n'a été ajouté ou supprimé dans la simulation. Un analyseur statique ne constitue pas une exécution du moteur.

Tous les candidats restent `Applied=NO`, les approbations restent en attente; les valeurs `HISTORICALLY_VERIFIED` sont réservées aux provinces dont **l'ensemble** peut être défendu à la résolution du jeu. Aucune ligne actuelle ne prétend à ce niveau.
