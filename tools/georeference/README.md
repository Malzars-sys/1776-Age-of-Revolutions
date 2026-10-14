# Atelier de géoréférencement MAP — prototype indépendant

Outil local réutilisable, pas un mode de carte du jeu. Il lit `map_data/provinces.png` sans le modifier. Les fichiers de jeu, populations, bâtiments et droits impériaux restent intacts. Aucun service distant, téléchargement ou entraînement de modèle au lancement.

## Démarrer

Depuis PowerShell, à la racine du dépôt :

```powershell
& 'C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 tools/map_georeference.py serve
```

Ouvrir **http://127.0.0.1:8766** dans un navigateur. Arrêter avec Ctrl+C. Le lanceur `tools/georeference/start-georeference.ps1` fournit la même commande ; il ne change pas la politique d’exécution PowerShell. Python avec NumPy et Pillow est requis ; le runtime existant les fournit. `--port 8767` permet un autre port, sans modifier les paramètres du mod. Le test de développement utilise ce port.

## Utilisation

- Glisser pour déplacer la vue, molette pour zoomer ; boutons de cadrage local, Europe et monde.
- Survol : pixel X/Y et longitude/latitude calculées. Les coordonnées pixel ont leur origine **en haut à gauche**, X vers la droite, Y vers le bas ; coordonnées géographiques en degrés, longitude Est et latitude Nord positives.
- Saisie longitude/latitude → **Localiser** ; saisie X/Y → **Pixel → géographie**. L’ordre dans les profils/API est `[longitude, latitude]`, jamais l’inverse.
- Espacement 0,05° à 30°. La grille est limitée par défaut à la boîte des repères FIT ; celle-ci est seulement indicative, pas un domaine de précision démontrée. Extrapolation mondiale volontaire : minimum 0,5°.
- **FIT** : observations utilisées pour ajuster. **CHECK** : observations indépendantes exclues de l’ajustement. **TARGET** : positions à rechercher, sans observation pixel obligatoire.
- Sélectionner un point puis « Enregistrer le prochain clic » pour relever un pixel. Un clic manuel reste non vérifié et ne devient pas automatiquement un repère fiable. Ne pas cliquer sur la position calculée pour prétendre la valider.
- Modifier les coordonnées, le rôle et la provenance des repères ; cliquer **Recalculer** après changement de rôle/qualité. La qualité « landmark identifié indépendamment » doit être justifiée par une source, une méthode et une incertitude de lecture. Ce choix n’est pas une certification automatique.
- **Exporter le profil JSON** / **Importer un profil** conserve les observations et le modèle ; le modèle est recalculé à l’import. Une empreinte du bitmap différent déclenche un avertissement. Le navigateur ne conserve pas automatiquement les modifications à la fermeture.
- **Exporter le quadrillage PNG** produit un RGBA transparent **8192 × 3616**, à superposer sans redimensionnement au bitmap courant. Le quadrillage ne contient pas les frontières et n’écrit jamais dans `provinces.png`. Les étiquettes de degrés sont affichées dans l’interface ; le PNG contient les traits.

## Ce qui est réellement connu sur la projection

Les fichiers de carte de l’installation actuelle donnent les dimensions et la conversion des locators du moteur (`PNG_Y = 3616 - ENGINE_Z`), pas une projection géodésique exacte. Le paramètre natif `C:/Games/Victoria 3/game/common/defines/00_graphics.txt:227`, `FLATMAP_EQUATOR_POSITION = 0.58`, place le dessin de l’équateur à **Y = 2097,28**. Ni ce dessin ni la grille de la texture papier ne démontrent une projection standard exacte, un datum ou la position de Greenwich.

Quatre modèles **diagnostiques**, comparables et inversibles, sont disponibles : Miller avec affine ajusté ; Miller avec axes séparés ; affine local en latitude/longitude ; hypothèse Miller isotrope avec équateur graphique natif et Greenwich au centre horizontal. Cette dernière hypothèse n’est PAS reconnue comme la projection exacte du jeu. Un ajustement local n’est pas une correction universelle de la carte.

Les trois villes demandées utilisent les coordonnées fournies par l’utilisateur. Les quinze autres villes utilisent les coordonnées GeoNames conservées dans le dépôt (CC BY 4.0) et des locators natifs de ville, vérifiés dans `MAP1_HUB_LOCATOR_CHECKS.csv`. **La ferme native appelée Erfurt n’est pas utilisée.** Les locators de ville peuvent être décalés pour des raisons de représentation et ne sont pas des observations exactes du centre historique.

## Précision et problème des sept pixels

Exemple fourni : 5 repères FIT et 10 CHECK européens, sans réutiliser les CHECK pour ajuster. Avec Miller affine, RMS FIT **1,716 px**, RMS CHECK **12,082 px**, maximum CHECK **24,299 px**. Tous ces CHECK sont en dehors de la boîte locale FIT : ils testent notamment l’échec de l’extrapolation. Ils ne fournissent pas une marge locale garantie.

La variante Miller théorique/non ajustée donne RMS CHECK **8,007 px**, maximum **12,888 px** ; cela ne la rend pas exacte. Les résultats complets des quatre modèles, les prédictions des trois villes et les écarts entre modèles sont conservés dans `docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/VALIDATION.json`.

Erfurt, Duderstadt et Heiligenstadt n’ont actuellement **aucun pixel indépendamment relevé et certifié**. Leur marge d’erreur reste donc **non établie**, pas ±1,7 pixel et pas ±7 pixels. Le désaccord entre modèles ajustés, très petit, n’est pas une mesure de leur erreur commune. Le prototype permet de tester une correction dès que des repères physiques identifiables (confluences, côtes, positions historiquement documentées) sont relevés indépendamment. Il ne justifie aucun déplacement de frontière.

Les statistiques sont des distances euclidiennes en pixels, séparées FIT/CHECK, avec signalement des extrapolations et diagnostic leave-one-out sur les FIT. Aucun intervalle de confiance à 95 % n’est inventé. La précision locale n’est considérée comme empiriquement contrôlée qu’avec au moins trois CHECK locaux déclarés comme repères indépendants, et même alors elle n’est pas « exacte ».

## Réemploi en ligne de commande

Les exports CLI sont limités aux dossiers `docs/reports` et `tools/georeference`, refusent toute sortie déjà existante et ne peuvent remplacer une source. Utiliser des noms de résultat nouveaux.

```powershell
python tools/map_georeference.py calibrate --controls tools/georeference/controls.example.json --kind miller_affine --output docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/mon-calage.json
python tools/map_georeference.py convert --profile docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json 11.0328 50.9787
python tools/map_georeference.py convert --profile docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json --inverse 4352.411 831.376
python tools/map_georeference.py grid --profile docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json --spacing 0.5 --output docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/ma-grille.png
python tools/test_map_georeference.py
```

`python` représente le même runtime Python que dans la commande de démarrage si celui-ci n’est pas dans PATH. Le script `validate_map_georeference.py --port 8767` vérifie aussi les sources, les quatre modèles, les API, l’export et les empreintes des données de jeu. Il conserve des résultats avec noms fixes et refuse leur écrasement ; utiliser une copie du dossier de sortie ou adapter le dossier pour une nouvelle campagne.

## Cartes historiques : chaîne déjà préparée

`calibrate --controls carte-controles.json` accepte un champ `dimensions` correspondant au scan. Les observations doivent utiliser le même référentiel géographique que le profil cible. Vérifier notamment les anciens méridiens d’origine (Ferro, Paris, etc.), ne pas traiter leurs graduations comme Greenwich par défaut. Garder des CHECK exclus du calage et documenter l’incertitude de lecture et les déformations du papier.

```powershell
python tools/map_georeference.py warp --image chemin/scan.png --source-profile docs/reports/map/scan-calage.json --target-profile docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/miller_affine.json --box 4280,780,4420,865 --output docs/reports/map/MAP2L/GEOREFERENCE_PROTOTYPE/scan-superpose.png
```

La chaîne est `pixel bitmap cible → coordonnées géographiques → pixel scan source`. L’export RGBA est une découpe à replacer à son coin supérieur gauche X/Y. Le rééchantillonnage est bilinéaire avec une maille de 16 pixels, **testé sur cas synthétique**, pas encore validé pour les frontières d’une carte ancienne. Les profils affine/Miller ne corrigent pas toutes les déformations d’un scan : un calage GIS plus complexe pourra être ajouté séparément si les CHECK le nécessitent. Pas d’inférence automatique de souveraineté, pas d’édition du bitmap et pas d’intégration dans le jeu à ce stade.
