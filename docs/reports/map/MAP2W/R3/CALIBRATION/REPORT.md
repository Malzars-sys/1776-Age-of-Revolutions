# MAP-2W-R3-CALIBRATION — décision finale

Date : 18 octobre 2026. **Cas B : correspondance locale insuffisante.**

Statut territorial maintenu : **MAP2W_R3_BLOCKED**. Aucun pays, RGB, propriétaire, population, bâtiment, unité ou mécanisme impérial ajouté ou modifié par cette passe. Aucun test moteur effectué ; aucune nouvelle validation en jeu demandée.

## 1. Origines précises des référentiels

### Affine historique franconienne

Ancien document : `MAP2L/FRANCONIA/ALIGNMENT.json`. Le scan Homann de 2263 × 2600 pixels est envoyé vers le bitmap par une affine à six paramètres, calculée avec exactement trois couples de points. Formule : `[sx, sy, 1] @ T = [X, Y]`.

```text
T = [[0.029492293710111982, 0.005888939080532318], [-0.0016747473712444005, 0.027387013519378556], [4318.161171091778, 826.2133799005417]]
```

Les positions natives proviennent de `FRANCONIA/NATIVE_ANCHORS.json`, lui-même extrait de `MAP1/MAP1_HUB_LOCATOR_CHECKS.csv` :

- Wurzburg : [4322.24, 861.541] ; wood / Würzburg ; FIT.
- Nuremberg : [4351.554, 877.18] ; city / Nuremberg ; FIT.
- Bayreuth : [4362.608, 862.394] ; mine / Bayreuth ; FIT.
- Regensburg : [4373.729, 892.864] ; farm / Regensburg ; CHECK.
- Bamberg versus displaced native Coburg farm : [4347.858, 862.075] ; farm / Coburg ; DIAGNOSTIC_NOT_FIT.
- Coburg rejected native farm label : [4347.858, 862.075] ; farm / Coburg ; REJECTED_LABEL_CONTROL.

La formule reproduit numériquement les trois FIT, ce qui est attendu pour trois points non colinéaires et six paramètres. Cela ne mesure pas leur justesse géographique. Le mot « surveyed » de l’ancien commentaire signifie une lecture de positions dans les fichiers, pas un relevé géodésique des villes. En particulier, Würzburg est un **hub de bûcherons**, Bayreuth un **hub minier** et le contrôle Ratisbonne un **hub de ferme**. Le contrôle Ratisbonne de 5,121 pixels mêle déformation du scan, affine et placement du hub ; il ne certifie pas le secteur Jagst–Kocher.

### Miller affine hérité

Ancien profil : `MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json`. Base sphérique diagnostique : `u = radians(lon)`, `v = 1,25 × log(tan(π/4 + 0,4 × radians(lat)))`, puis `[X,Y] = [u,v] @ A + b`. Il ne s’agit pas d’une formule de projection moteur prouvée.

```text
[A;b] = [[1255.167041359254, -5.159846201805137], [-0.9688003245595548, -1274.9110326762366], [4111.662940799494, 2076.7654941378114]]
```

Cinq points FIT, tous des locators non relevés géodésiquement :

- Hanover : géographie [9.73322, 52.37052] → locator [4325.178, 788.162].
- Magdeburg : géographie [11.63189, 52.13129] → locator [4365.351, 796.94].
- Frankfurt : géographie [8.68417, 50.11552] → locator [4300.876, 856.939].
- Brunswick : géographie [10.52673, 52.26594] → locator [4339.979, 795.886].
- Dresden : géographie [13.73832, 51.05089] → locator [4411.987, 828.656].

Domaine des points FIT : longitude 8,68417–13,73832°, latitude **50,11552–52,37052° N**. Langenbourg et Kirchberg, vers 49,2° N, sont environ 0,86–0,91° au sud : c’est une extrapolation. RMS FIT 1,716 pixel et RMS CHECK européen 12,082 pixels ne constituent pas une marge locale garantie. Les biais de locators et l’extrapolation peuvent se combiner ; on ne peut attribuer le désaccord à une simple translation ou à la seule formule Miller.

### Calage intermédiaire du candidat retiré

`R3/SOURCE_ALIGNMENT.json` envoie le dessin de Gerabronn vers **trois positions prédites par le Miller hérité**, et non vers trois nouveaux points physiques natifs. Les contrôles de feuille Gerabronn/Schrozberg, 0,079 et 0,222 pixel, partagent ce même référentiel parent. Ils vérifient une cohérence relative, pas la position réelle dans le jeu. Le SVG ne déclare pas de CRS : ses unités nominales ne sont pas assimilées arbitrairement à UTM ou Gauss–Krüger.

Les anciens écarts Würzburg 7,57 / Nuremberg 2,29 / Bayreuth 1,99 / Ratisbonne 4,97 pixels sont des désaccords entre référentiels, pas des erreurs certifiées des villes. Aucun des deux n’est promu comme vérité par défaut. Aucun profil ancien ou frontière validée n’a été réécrit.

Les rasters provinciaux et fluviaux partagent le même repère image 8192 × 3616, origine en haut à gauche, Y vers le bas. Le facteur deux de la hauteur 16384 × 7232 est un facteur de résolution, pas une correction géographique. `default.map` et les defines natifs indiquent le bouclage horizontal et une position graphique d’équateur 0,58 ; ils ne fournissent pas une formule géodésique exacte. Aucun retournement, facteur deux ou translation n’a été introduit pour faire coïncider les hypothèses.

## 2. Nouvelles données physiques indépendantes

Source primaire : [LUBW, réseau hydrographique officiel AWGN](https://www.lubw.baden-wuerttemberg.de/wasser/awgn). Service `Gewaessernetz_AWGN`, couche 0 : système natif EPSG:25832, export demandé en EPSG:4326. Réponse complète : Neckar OBJECTID 18518 (**8 341 sommets**), Jagst 4294 (**9 722**), Kocher 4311 (**7 402**), soit **25 465 sommets**. Métadonnées et réponse GeoJSON conservées avec empreintes.

Le réseau moderne sert à rechercher des formes physiques, pas à définir les frontières de 1776. Rectifications de cours d’eau et écart de date restent des limites. Le réseau Natural Earth 1:10 millions déjà conservé ne contient pas ici la Jagst, le Kocher ou le Neckar ; son seul ajout ou sa meilleure interpolation ne pouvait pas créer ces informations.

Six candidats physiques sont examinés. P1/P2 correspondent aux embouchures ; P3–P6 à des secteurs de boucle, choisis par la géométrie hydrographique seule dans des fenêtres déclarées. Les points réservés ne sont jamais utilisés pour ajuster un modèle.

| ID | Repère physique candidat | Longitude / latitude WGS84 | Rôle prévu | Pixel natif homologue | Résidu indépendant | Utilisé |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | Confluent Jagst–Neckar | 9.178179 / 49.233266 | Ajustement candidat | Non identifié | Non mesurable | Non |
| P2 | Confluent Kocher–Neckar | 9.198495 / 49.224801 | Ajustement candidat | Non identifié | Non mesurable | Non |
| P3 | Boucle Jagst près de Bächlingen | 9.832621 / 49.249831 | Ajustement candidat | Non identifié | Non mesurable | Non |
| P4 | Boucle Kocher près de Künzelsau | 9.678824 / 49.283853 | Ajustement candidat | Non identifié | Non mesurable | Non |
| P5 | Coude Jagst près de Kirchberg | 9.981771 / 49.210284 | Contrôle réservé | Non identifié | Non mesurable | Non |
| P6 | Coude Kocher près de Schwäbisch Hall | 9.748273 / 49.103266 | Contrôle réservé | Non identifié | Non mesurable | Non |


## 3. Vérification des données natives et du relief

Le raster fluvial est lu dans le mod actif, palette P, 8192 × 3616. L’extraction comprend **toutes les largeurs 3–15**, conformément aux treize valeurs natives, plus les marqueurs 0–2 ; ce n’est pas un filtre limité aux seuls bleus 3–11. Les fonds 254/255 sont distingués des cours d’eau.

Dans le corridor `[4300,870]–[4340,892]`, couvrant 40 × 22 cellules autour des positions diagnostiques : **zéro pixel de rivière ou de marqueur**, aucun indice inconnu masquant une rivière. Le raster modifié pour les lots antérieurs et le vanilla sont **identiques dans la fenêtre régionale examinée**. Le Rhin, le Main et le Danube sont visibles dans le contexte large, mais pas les branches Jagst–Kocher–Neckar nécessaires aux petites cibles. Les deux confluences P1/P2 ne sont en outre séparées que de 0,507 pixel dans le modèle diagnostique : elles ne fourniraient pas deux ancrages bien séparés à cette résolution.

Le relief est aussi inspecté : source 16384 × 7232, contrôle de **110 échantillons** de la hauteur compactée réellement référencée par l’indirection native. Écart source/packed nul sur ces échantillons. L’image locale montre un modelé lissé, sans sommet ou vallée homologue identifié indépendamment. Les extrema de gris ne deviennent pas des contrôles géographiques, et les valeurs ne sont pas converties en mètres sans preuve.

## 4. Contrôles indépendants et incertitude

**Quatre candidats d’ajustement, deux candidats de contrôle réservés ; zéro couple physique accepté pour le calcul, zéro contrôle natif indépendant mesurable.** Aucun nouveau modèle n’est ajusté. Moyenne des résidus, maximum, borne d’erreur et intervalle de confiance locaux restent `null` / **non établis**, pas zéro.

Les distances aux rivières natives les plus proches sont conservées comme diagnostics de non-correspondance, jamais comme résidus de repères homologues. Les segments entre deux prédictions sur la figure ne représentent ni des barres d’erreur ni une confiance à 95 %. La discrétisation d’une cellule identifiée peut à elle seule représenter jusqu’à ±0,5 pixel par axe ; elle ne borne pas les erreurs de modèle, d’identification ou de source.

L’incertitude totale n’est donc **pas bornable utilement avec les observations disponibles**. On ne peut garantir le choix des noyaux proposés de deux à trois cellules de large. La documentation n’affirme pas que la géographie de ces villes soit impossible à connaître : elle constate l’absence de contrôle physique natif suffisamment discriminant dans ces données.

Carte : `CORRESPONDENCES_AND_UNCERTAINTY.png`. Le panneau gauche est une vue géographique indépendante ; le droit montre les rivières natives et deux hypothèses non validées. Les anciens candidats retirés restent marqués comme tels, sans être installés.

## 5. Décision et alternatives

**Ne rien installer ; Langenbourg/Kirchberg restent en catégorie C pour leur correspondance avec le bitmap.** Leur souveraineté historique n’est pas remise en cause. Leurs sept anciennes cellules ne sont pas réattribuées ; aucun nouveau TAG/RGB, aucun besoin de contrôle en nouvelle partie.

| Secteur | Possibilité indépendante examinée | Décision actuelle |
| --- | --- | --- |
| Castell | Le Main offre un contexte régional, pas un contrôle local précis déjà accepté. Partages des branches et possessions communes à tracer séparément. | Aucun sous-lot territorial prêt ; ne pas reprendre le RGB WZB entier. |
| Wertheim | Une étude autonome des boucles du Main est une piste réelle. Le confluent de la Tauber n’est pas identifié dans le réseau natif et les droits des branches restent à délimiter. | Piste future, pas un calage indépendant validé dans cette passe. |
| Rothenburg, Windsheim, Weißenburg | Tauber, Aisch et Rezat non disponibles comme homologues natifs acceptés ici. | Différer ; pas de pays artificiel d’une cellule. |
| Schweinfurt | Le Main peut soutenir un futur pilote, mais ni la position de la ville ni son territoire ne se déduisent de la courbe régionale seule. | Aucun transfert automatique du noyau WZB protégé. |


**Recommandation explicite : différer R3 et passer à MAP-2W-R4, juridictions bavaroises et ecclésiastiques**, après consigne du joueur. Les boucles du Main restent une piste de recherche indépendante pour une reprise ultérieure, pas un sous-lot déjà testable. Aucune autre région ne démarre automatiquement.

## 6. Protection, reproductibilité et limites

La capture fraîche `BASELINE.json` conserve les empreintes de **2 328 fichiers fonctionnels** et de Git. Le contrôle final distingue les fichiers inchangés des **9 chemins précis du chantier américain concurrent**, dont l’évolution a été observée sans écriture ou restauration par cette passe. Une modification de visibilité de loi est notamment limitée aux États-Unis, et l’ancien fichier séparé des minutemen a été retiré par ce chantier externe ; les autres lois natives sont comparées à leur source antérieure et conservées. Ces observations ne constituent pas une validation fonctionnelle du chantier américain. La liste et les empreintes observées sont dans `CONCURRENT_OBSERVATION.json` ; la baseline n’est pas réécrite.

Carte provinciale, propriétaires, populations, bâtiments, unités, registre impérial de 567 RGB, compilateur existant, anciens profils, Erfurt–Eichsfeld et lots validés sont préservés. HEAD et index inchangés. Aucun commit, push, merge, reset, rebase, changement de branche ou staging. Installation du jeu en lecture seule.

Le contrôle territorial moteur est **sans objet**, puisqu’aucun correctif fonctionnel n’est installé. **22/22 tests du diagnostic** et **11/11 contrôles de protection** passent. Les tests vérifient notamment le maintien de valeurs nulles en absence de contrôles, les rôles réservés, le refus d’un calage sans couples et les protections de périmètre. Ils ne certifient pas une précision géographique.

Outil indépendant : `tools/map2w_r3_calibration.py` ; commandes de lecture/diagnostic `inspect`, `origins`, `physics`, `map_evidence`, `decision`, `verify`. `snapshot` refuse d’écraser sa capture. Les réponses téléchargées sont conservées ; aucune intégration ou dépendance supplémentaire installée. Les chemins étaient connus ou retrouvables par identifiant/nom exact : aucun appel ColGrep redondant et aucune reconstruction d’index dans cette passe.
