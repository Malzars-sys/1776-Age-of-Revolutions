# Erfurt–Eichsfeld : résultat du recalage local

14 octobre 2026. **Amélioration diagnostique réelle, application territoriale non autorisée par les résultats.** Aucun nouveau lot de préparation : ce dossier conserve les essais concrets avec le prototype, les mesures comparables avant/après et leur décision d'application.

## Méthode et résultats

Réemploi de `tools/georeference/model.py` (`fit`, `forward`, `inverse`, `evaluate`) et des profils précédents. Source physique conservée : Natural Earth `ne_10m_rivers.geojson`, SHA-256 `65dca1bd1729a347dda0837f41b5d152252e33abd2d7ff3370a0539c33bdf89b`. Source raster : `C:/Games/Victoria 3/game/map_data/rivers.png`, SHA-256 `ce28f82e19925d8f4cca834ee0bfbcb079b37597f22b23d8f1a9d7393bb41f25`.

Les routes principales du bitmap sont sélectionnées par continuité à huit voisins, afin de ne pas comparer chaque position à n'importe quelle branche voisine. Les extrémités servent uniquement à sélectionner la route, pas de points GPS à ajuster. La forme générale est relue dans `HYDROGRAPHY_BEFORE.png` et `HYDROGRAPHY_TRANSLATION.png`.

355 sommets géographiques de la Weser–Werra sont utilisés pour tester une **translation robuste de deux paramètres**, limitée à ±15 pixels, avec sept départs fixes et une pondération robuste. Le choix du minimum utilise uniquement cette route. L'Elbe entière est exclue de l'optimisation. Les 337 sommets CHECK de l'Elbe sont conservés, avec les grands écarts et la vérification des correspondances aux extrémités. La bande locale, définie par les latitudes des villes ±0,15°, est 50,8287–51,6625° ; elle ne résulte pas d'une sélection des petits résidus.

| Mesure au même tracé CHECK de l'Elbe | Moyenne avant | Moyenne après | RMS avant | RMS après | Maximum avant | Maximum après |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Ensemble, 337 sommets | 3,432 | 2,057 | 3,898 | 2,275 | 7,828 | 4,758 |
| Bande locale, 95 sommets | 2,996 | 2,445 | 3,217 | 2,564 | 4,995 | 4,015 |

Toutes les valeurs sont en pixels. **Ce sont des distances au tracé physique tenu à l'écart, pas des erreurs de villes ou de landmarks géographiques homologues certifiés.** Une petite distance perpendiculaire au fleuve peut masquer un déplacement le long de celui-ci. Les sommets voisins sont corrélés : 337 sommets ne constituent pas 337 repères indépendants. Ces distances peuvent sous-estimer l'erreur de position réelle.

Sur la Weser–Werra utilisée pour ajuster : moyenne 3,456 → 0,876 ; maximum 7,883 → 2,785. Ces meilleurs chiffres FIT ne sont pas utilisés pour annoncer une précision indépendante.

Les dix villes CHECK européennes du prototype ne sont pas retirées : même ensemble, RMS 12,082 → 10,930 ; maximum 24,299 → 22,138. Elles restent des locators non relevés et majoritairement hors de la zone locale. **Comparer directement leurs 12 pixels à 2,44 pixels locaux ferait changer de jeu de contrôles et de métrique ; ce n'est pas une validation.**

Une seconde origine, Miller isotrope + équateur graphique natif, et deux similitudes contraintes ont également été évaluées. La similitude depuis l'ancien profil améliore le FIT, mais dégrade le CHECK : moyenne 2,762, maximum 5,751. La similitude depuis l'origine théorique donne maximum CHECK 5,927. Elles sont rejetées plutôt que sélectionnées pour leur faible erreur FIT. Tous les résultats restent dans les JSON `PHYSICAL_*_COMPARISON`.

## Décalage de sept pixels : ce qui est établi et ce qui ne l'est pas

Le raccordement physique propose une translation de **X −5,728 ; Y −4,359**, soit **7,198 pixels** en distance totale, par rapport au modèle ajusté sur les villes. Cette valeur apparaît dans l'optimisation sur la Weser–Werra ; elle n'est pas imposée comme une correction souhaitée. Il s'agit donc d'une piste chiffrée expliquant le décalage visuel d'environ sept pixels, **pas de la preuve d'un bug moteur ou d'une translation exacte universelle**.

Causes/limites distinguées :

- Le faible RMS des cinq locators d'ajustement masque leurs décalages possibles de représentation ; la ferme « Erfurt » reste exclue. Son pixel est (4336,258 ; 832,944), soit encore environ 12 pixels du nouveau candidat géographique d'Erfurt : le nouveau calage ne justifie pas de la traiter comme le centre urbain.
- L'affine locale issue des villes extrapole mal. Le changement d'origine et le FIT sur un autre type de preuve changent les placements de plusieurs pixels. Le paramètre d'équateur graphique ne fixe pas toute la projection.
- Le jeu schématise les cours d'eau et Natural Earth les généralise également. Les données conservées ne contiennent pas les petites rivières Gera, Unstrut, Leine, etc., nécessaires à des contrôles plus proches des trois villes. Leur absence dans cette source n'est pas une affirmation qu'elles n'existent pas géographiquement.
- Le passage raster 16 384 × 7 232 du relief au bitmap 8 192 × 3 616 est explicitement un facteur deux. Les centres de pixels sont traités comme tels. Un décalage de demi-pixel ne peut pas expliquer sept pixels.
- Les anciennes cartes n'ont pas un méridien d'origine Greenwich démontré. Leurs graduations ne sont pas injectées telles quelles comme coordonnées modernes. Les trois coordonnées WGS84 fournies par l'utilisateur restent les références des TARGET, pas des observations pixel du jeu.

Le relief natif `heightmap.png` a été inspecté et les maxima séparés sont enregistrés dans `RELIEF_PEAKS.json`. **Aucun maximum n'est automatiquement nommé Brocken, Inselsberg ou autre sommet.** L'identification et la fidélité du relief raster ne permettent pas ici de certifier des points supplémentaires. La [DGGV fournit un point au GeoInfozentrum du Großer Inselsberg](https://www.dggv.de/geotope/auf-der-spur-des-rhyoliths-gestein-des-jahres-2026-am-grossen-inselsberg/) : ce point d'excursion ne devient pas arbitrairement un sommet du bitmap.

## Positions estimées, non certifiées

| Ville | Ancien X ; Y | Candidat local X ; Y |
| --- | --- | --- |
| Erfurt | 4352,4 ; 831,4 | **4346,7 ; 827,0** |
| Duderstadt | 4335,5 ; 815,7 | **4329,7 ; 811,3** |
| Heiligenstadt | 4332,7 ; 819,7 | **4327,0 ; 815,3** |

Origine pixel en haut à gauche. Ces positions permettent une comparaison reproductible, mais **leur intervalle d'erreur géographique reste non établi**. Le désaccord entre quatre modèles candidats est enregistré séparément ; il ne constitue ni une précision de ±1 pixel, ni un intervalle à 95 %. Aucun pixel indépendant de centre urbain n'a été identifié pour ces trois villes dans le raster. Le seuil de maximum inférieur à trois pixels n'est pas satisfait, même avec la métrique physique susceptible de sous-estimer l'erreur.

Le domaine enregistré dans le profil est la boîte réelle des coordonnées Weser–Werra utilisées pour l'ajustement, pas une boîte artificiellement étendue jusqu'à l'Elbe. Le caractère extrapolé des TARGET par rapport à cette boîte est enregistré explicitement ; une appartenance à la boîte ne vaut toujours pas précision démontrée.

`PLACEMENT_COMPARATIF.png` montre les propriétaires actuels inchangés, les anciens points bleus et les candidats verts. `PIXEL_OWNER_COMPARISON.json` donne leurs RGB et State_ID sans les confondre avec des identifiants historiques. Par exemple, Erfurt passe du point `x51C021`/SCW au point `x3C9B93`/PRU dans `STATE_ANHALT`, et les deux points de l'Eichsfeld passent dans `xA001E0`/PRU, `STATE_BRUNSWICK`. **Cela ne justifie pas l'attribution de la totalité de ces provinces à Mayence.**

## Relecture des frontières historiques déjà conservées

Les trois sources ont été relues et leurs empreintes sont vérifiées, sans les remplacer :

- Schreiber, feuillet décrit comme 1749, `EICHSFELD_FULL_SOURCE.jpg` : légende distinguant Amt Duderstadt, Gieboldehausen, Scharfenstein, Worbis et d'autres juridictions, ainsi que le **Mühlhäuser Gebiet** séparé. Une union de ces territoires par proximité urbaine ou une absorption de Mühlhausen n'est pas admise.
- Homann, `ERFURT_SOURCE.jpg`, édition exacte toujours non certifiée : district central d'Erfurt et possessions distinctes **Vargula, Mühlberg et Tonndorf**. Un contour unique contigu ne doit pas effacer ces séparations.
- [Feuillet régional de Berne catalogué 1789](https://ryhiner.ub.unibe.ch/en/world/volume/172/image/14659), `BERN_ERFURT_1789.jpg` : contrôle complémentaire des secteurs et des localités ; la date postérieure ne vaut pas automatiquement preuve de toutes les frontières au 1er janvier 1776.

La souveraineté générale mayençaise n'est pas remise en cause ; le blocage précis est le raccordement suffisamment sûr de ces **limites**, et non des seuls centres, aux cellules du jeu. Aucun nouveau contour politique n'est inventé pour contourner cette incertitude. Les anciens essais rejetés restent conservés.

## Profil réutilisable et fichiers livrés

`THURINGIA_RIVER_DIAGNOSTIC_PROFILE.json` conserve la matrice, les sources, la méthode et le statut **REJECTED_FOR_TERRITORIAL_APPLICATION**. Utilisable avec les commandes `convert` et `grid` du prototype, pour retrouver les mêmes résultats ; ce n'est pas un profil GCP certifié à importer comme FIT/CHECK urbains dans l'interface.

```powershell
python tools/map_georeference.py convert --profile docs/reports/map/MAP2L/ERFURT_EICHSFELD/LOCAL_RECALIBRATION/THURINGIA_RIVER_DIAGNOSTIC_PROFILE.json 11.0328 50.9787
python tools/map2l_thuringia_calibration.py physical
python tools/map2l_thuringia_calibration.py report
python tools/test_map2l_thuringia_calibration.py
```

Utiliser le runtime Python existant indiqué dans le guide du prototype si `python` n'est pas dans PATH. Pas de nouvelle dépendance installée ; l'implémentation utilise NumPy, Pillow et la bibliothèque standard. Le diagnostic de similitude a confirmé l'intérêt de conserver les contrôles exclus plutôt que de réduire artificiellement le FIT.

Nouveaux fichiers de travail : `tools/map2l_thuringia_calibration.py`, `tools/test_map2l_thuringia_calibration.py` et les résultats de ce dossier. Le seul rapport territorial mis à jour est celui d'Erfurt–Eichsfeld. Aucun autre lot MAP n'est modifié.

## Contrôles et décision finale

- 5 tests propres au recalage local passent : recherche du pixel le plus proche, translation connue, similitude connue, inversion d'un profil modifié et statistiques.
- Les 12 tests du prototype sont réexécutés ; résultats techniques séparés de la validité géographique.
- Les aller-retour des trois villes sont contrôlés : cohérence mathématique, pas preuve de leur emplacement historique.
- **2 091 fichiers runtime et le registre impérial sont comparés à la baseline de cette reprise et restent identiques**, y compris bitmap, populations, bâtiments, propriétaires économiques, unités, recrutements, effets et corrections des collaborateurs. Les trois sources historiques conservent également leurs empreintes. Le compteur 2 091 inclut le registre.
- **0 province appliquée, 0 population créée ou transférée, 0 bâtiment ou formation militaire modifié.** Aucun manifeste n'est ajouté à la chaîne des migrations impériales, aucune recompilation du registre n'est lancée sans territoire approuvé. Les anomalies préexistantes restent inchangées.
- Pas de lancement de Victoria 3, de changement de playset, de staging, commit, merge ou push. Les vérifications en jeu restent différées : après un futur calage validé, contrôler les limites des enclaves, Mühlhausen séparée, propriétaires/données de départ et affichage de jure.

**Décision : ne pas appliquer la translation comme frontière.** Il faut encore des correspondances locales homologues identifiées indépendamment, pas un nouveau choix de points approximatifs demandé au joueur. Les preuves actuelles n'établissent pas la précision requise pour finir le découpage en sécurité.

ColGrep-Agent-2B : un appel local réussi, 123,98 secondes, sans changement de configuration. Il a retourné des chemins connus, y compris ceux explicitement exclus de la question ; leurs lignes ont été vérifiées. Aucune nouvelle méthode de calage physique exploitable n'en est issue. Aucun gain de quota exact n'est mesurable.
