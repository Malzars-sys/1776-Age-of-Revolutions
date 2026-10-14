# MAP-1B — Méthode, erreurs et seuils de décision

## Réutilisation et périmètre

Lecture de `../MAP1/MAP1_BASELINE_PROVINCE_INDEX.csv`, `MAP1_GEOGRAPHIC_MATCHES.csv`, du répertoire des atlas SVG/JSON, de `geometry_index.json`, des locators et des runs exacts `PROVINCE_PIXEL_RUNS.jsonl.gz`. Les SVG préexistants de Wallonie, Lombardie et MAP1-P0-003 (Haute-Silésie) sont relus; la Basse-Silésie, sans SVG dédié préexistant, utilise les runs exacts déjà archivés, sans nouvel inventaire. Aucun des 410 dossiers, des 20 aperçus ou de l'inventaire mondial n'est reconstruit.

34 RGB distincts : **8 Wallonie, 8 Lombardie, 9 Basse-Silésie, 6 Haute-Silésie**, et **3 anomalies liées à la Silésie définies en Moravie/Galicie occidentale**. Les écritures multiples restent `AUS|PRU`, sans sélection silencieuse d'un propriétaire. `State_ID` désigne la géométrie réelle; `Ownership_History_State_IDs` expose séparément les scopes historiques.

## Reproduction de la géométrie

Les runs sont des carrés de pixels `(x,y)`, coordonnées d'image, origine en haut à gauche. La frontière affichée est uniquement l'ensemble de leurs arêtes exposées : pas de lissage, pas de simplification ni de dessin manuel d'un nouveau contour du jeu. Les scans originaux sont conservés; les images de lecture sont ramenées à **1600 pixels de large**, rapport d'aspect conservé. Les détails sont des recadrages à l'échelle 1:1 de ces dérivés.

Bitmap du jeu : 8192 × 3616, empreinte attendue `e3911fd80a40c6b297a68f66e898d9b187863b64483a9608123606143ee2ea78`. Ce bitmap n'est pas une projection géodésique validée. Le relief et le nom d'un hub ne constituent pas une souveraineté.

## Ancrage indépendant et contrôle

`anchor_observations.json` conserve les observations manuelles, estimées à **±5 pixels du scan dérivé** (précision de lecture, pas intervalle statistique). Coordonnées de villes lues sur chaque carte; contrepartie du jeu issue des locators MAP1. Ce choix comporte une erreur de représentation propre au placement des hubs : les résidus ne sont pas uniquement une erreur du scan.

Pour chaque région, quatre villes déterminent une transformation affine locale à six coefficients par moindres carrés : `[u,v] = [x,y,1] T`. Aucune latitude/longitude ni projection historique reconstruite. Les autres villes sont laissées **hors ajustement**, puis les écarts sont mesurés. Le résidu source est ramené en unités du bitmap par l'inverse de la partie linéaire de T. On ne retire pas un contrôle mauvais pour afficher une meilleure précision.

| Cas | Villes d'ajustement | Contrôles exclus du calcul | RMS ajustement, px scan | RMS contrôles, px jeu | Maximum contrôle, px jeu |
|---|---|---|---:|---:|---:|
| Luxembourg | Luxembourg, Namur, Liège, Charleroi | Bruxelles, Trèves, Reims | 34,91 | 8,02 | 10,122 |
| Lombardie | Milan, Como, Gênes, Parme | Plaisance, Vérone | 8,01 | 3,69 | 4,786 |
| Silésie | Breslau, Liegnitz, Oppeln, Ratibor | Glogau, Görlitz, Olomouc | 13,65 | 17,41 | 27,864 |

Ce maximum est **un écart observé, pas une borne garantie de l'erreur ailleurs**. Les points source sont manuels et les contrôles sont peu nombreux. Le feuillet lombard oriental est consulté mais non ajusté. Brescia/Bergame sont uniquement deux diagnostics supplémentaires : leur inversion apparente n'est ni masquée ni utilisée pour améliorer l'ajustement. Tous les coefficients et résidus individuels sont livrés dans `ALIGNMENT_METRICS.json` et `GCP_AND_CONTROLS.csv`.

## Qualification des résultats

- `MAPPING_VERIFIED` exigerait une autorité applicable au 01-01-1776 **et** une preuve que le polygone entier, ses enclaves et ses marges relèvent de cette autorité, avec des contrôles locaux suffisants. Une ville bien positionnée ne suffit pas. **Aucun RGB n'atteint ce seuil ici.**
- `MAPPING_PROPOSED` : noyau territorial corroboré et diagnostic concordant, mais contours ou calage restant à vérifier. Trois maintiens sont proposés : AUS `xD04060`, PRU `x6E617F`, PRU `xC108EA`. Aucun n'est un transfert admissible. Les deux derniers conservent explicitement l'échec de contrôle méridional.
- `MAPPING_REQUIRED` : juridiction complète non résolue, mélange apparent, bord de carte, manque d'annexe ou scope erroné. **31 RGB**. Aucun TAG nouveau ni partage de souveraineté n'est inventé pour remplir les cellules.

`MAP1B_VERIFIED_PROVINCES.csv` contient donc **l'en-tête et zéro ligne**. `MAP1B_UNRESOLVED.csv` contient **les 34 RGB non définitivement validés**, dont trois propositions signalées par `Mapping_Status`; il ne faut pas compter ses 34 lignes comme 34 échecs identiques. Une table lisible par région et la justification par RGB accompagnent les images.

Les colonnes d'autorité sont limitées au noyau documenté, jamais proclamées applicables à tous les pixels. Les localités de bord listées dans le registre sont des **voisinages diagnostiques**, non une affirmation qu'une ville tombe effectivement dans ce RGB. Les propriétés actuelles viennent exclusivement de la baseline du mod.

## A, B ou C : ne pas confondre frontière et State Region

**A — provinces existantes :** conservation/transfert d'un RGB sans modifier sa forme, ou choix d'une représentation politique dépendante. Retenu provisoirement pour les trois maintiens proposés. La dépendance éventuelle de LUX ne nécessite pas automatiquement de modifier le bitmap.

**B — regroupement de State Regions :** envisageable si le RGB est correct mais son regroupement doit changer. Les trois scopes silésiens incohérents sont des anomalies techniques démontrées; réparer la référence d'historique peut suffire, sans nouveau regroupement B. On n'ordonne donc pas B automatiquement.

**C — géométrie :** seulement si une frontière historique démontrée coupe une province et que A puis B ne permettent pas la représentation retenue. L'overlay imparfait suggère des zones multi-juridictions, surtout Crema, Ardennes et sud-Silésie; il ne prouve pas encore une scission nécessaire. **Aucune méthode C autorisée**, autres cas `UNDETERMINED` et décision `SUSPENDRE`.

Pour le prochain passage : obtenir plans administratifs et annexes primaires; ajouter des points indépendants de part et d'autre de chaque limite; comparer contour intégral avec une bande d'incertitude locale. Un warp flexible ajusté sur les mêmes villes sans contrôle indépendant ne résoudrait pas l'absence de preuve historique.

## Protection, contrôles et reproduction

Seuls les rapports MAP1B et quatre outils `map1b_*` ont été ajoutés. Aucun historique, State Region, population, bâtiment, formation, relation ou fichier de gameplay édité. `MAP1B_RUNTIME_BEFORE.json` correspond à la baseline runtime MAP1 et permet un contrôle fichier par fichier. Les modifications préexistantes de métadonnées, de description Steam et d'icône chimique sont conservées.

Séquence reproductible : `tools/map1b_images.py` (dérivés), `tools/map1b_align.py` (diagnostics et contrôles), `tools/map1b_report.py` (registres et validation). Python utilise numpy/Pillow, pas de serveur ni d'accès réseau pour reconstruire les rapports depuis les bruts. `map1b_research.py` sert uniquement aux téléchargements publics; l'exécution des trois autres ne télécharge rien. Aucun script MAP1 de génération n'a été relancé.

Validation finale : 34 RGB uniques, nombres et propriétaires recoupés avec MAP1, images lisibles et décodables, chemins des preuves présents, CSV UTF-8 avec BOM, 1900 empreintes runtime inchangées, manifeste MAP1 vérifié, bitmap et HEAD inchangés. Résultats chiffrés dans `MAP1B_VALIDATION.json`. **Pas de test en jeu** : aucune intégration n'a été faite. Les sources peuvent être reproduites visuellement, mais le contrôle automatique de fichier ne valide pas une frontière historique.

La fusion préexistante du collaborateur reste en attente dans son worktree; MAP1B ne l'a ni achevée ni annulée. L'anomalie Bessarabie contient `git status` et `git fetch origin` littéralement dans un `create_state` du candidat : **syntaxe**, sans valeur de preuve territoriale. Voir [décisions MAP1, section Bessarabie](../MAP1/MAP1_COLLABORATOR_MERGE_DECISIONS.md), anomalies MAP0-0090 à 0094. Elle n'est pas corrigée ici hors périmètre.
