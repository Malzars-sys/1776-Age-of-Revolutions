# Prototype permanent de géoréférencement — 13 octobre 2026

## Résultat livré

Atelier indépendant utilisable dans le navigateur, coordonnées interactives aller-retour, grille réglable, relevé de points, profils importables/exportables et PNG transparent aligné au bitmap 8192 × 3616. Serveur limité à 127.0.0.1 ; aucune écriture de fichiers depuis l’API. CLI de calibration, conversion, grille et déformation d’un scan historique. Documentation et lanceur dans `tools/georeference/`.

Le prototype fonctionne ; **la projection réelle exacte et la précision locale ne sont pas établies**. Il n’existe pas dans les fichiers inspectés de définition complète longitude/latitude → pixel. Le dessin d’équateur natif (`00_graphics.txt:227`, fraction 0,58) donne Y = 2097,28, pas une preuve de la formule de Miller. Ni Greenwich centré, ni un simple décalage constant, ne sont imposés comme vérité.

## Comparaison sans ajuster sur les contrôles

5 villes FIT, 10 villes CHECK, coordonnées et locators vérifiés dans deux sources conservées. Les CHECK européens sont hors de la boîte FIT locale. Les trois villes demandées restent TARGET sans observation pixel indépendante. La ferme « Erfurt » n’est jamais un point de calibration.

| Modèle diagnostique | RMS FIT (px) | RMS CHECK (px) | Maximum CHECK (px) |
| --- | ---: | ---: | ---: |
| Miller affine local | 1,716 | 12,082 | 24,299 |
| Affine latitude/longitude local | 1,717 | 12,583 | 22,682 |
| Miller, axes séparés | 1,723 | 12,108 | 24,617 |
| Miller théorique + équateur graphique natif | Non ajusté : écart 9,279 | 8,007 | 12,888 |

La variante théorique obtient ici de meilleurs CHECK que l’ajustement local : cela montre les limites d’extrapolation de ce dernier, pas la justesse absolue de la variante théorique. Les observations de hubs sont indicatives et peuvent elles-mêmes être décalées.

| Ville TARGET | Longitude, latitude fournies | Pixel calculé, Miller affine | Pixel calculé, hypothèse équateur natif |
| --- | --- | --- | --- |
| Erfurt | 11,0328 ; 50,9787 | 4352,411 ; 831,376 | 4347,057 ; 824,689 |
| Duderstadt | 10,2597 ; 51,5125 | 4335,463 ; 815,708 | 4329,465 ; 808,595 |
| Heiligenstadt | 10,1344 ; 51,3775 | 4332,721 ; 819,709 | 4326,614 ; 812,675 |

Ces chiffres sont des **prédictions**, pas des pixels certifiés. Deux hypothèses raisonnables donnent des différences de plusieurs pixels, même lorsque les variantes ajustées s’accordent à moins d’un pixel. Une erreur commune reste possible. Le problème d’environ sept pixels n’est donc pas résolu avec une marge garantie. Il faut identifier des repères physiques locaux homologues et réserver des CHECK indépendants ; aucune correction de frontière n’est autorisée par ce résultat seul.

## Vérifications

- 12 tests unitaires réussis : quatre modèles réversibles, affine connue, CHECK exclu du FIT, TARGET sans fausse erreur, extrapolation, refus des repères invalides/colinéaires, espacement, RGBA aligné, chaîne de warp synthétique, protection des sorties.
- 6 contrôles HTTP réussis : empreinte/session, ajustement, conversion réversible, PNG transparent, erreurs 400 explicites, découpe du bitmap.
- Syntaxe JavaScript vérifiée. Interface testée dans Chrome : chargement du vrai bitmap, Erfurt localisée, conversion inverse, réglage de grille, refus d’une grille mondiale trop fine et coordonnées interactives au survol/clic.
- Export depuis le bouton du navigateur réellement reçu : `C:/Users/simeo/Downloads/grille-geographique-8192x3616.png`, RGBA 8192 × 3616, origine transparente, empreinte identique à l’export contrôlé. Le suivi automatique de téléchargement du navigateur a expiré, mais le fichier reçu a été vérifié directement ; aucune erreur JavaScript signalée.
- Aperçu `INTERFACE.png` conservé. La capture pleine page n’était pas disponible ; capture visible utilisée.
- Empreintes protégées inchangées : `provinces.png`, propriétaires `00_states.txt`, populations/bâtiments ouest-européens, registre impérial. Le bitmap est toujours identique au dernier candidat approuvé Milan–Cremonese. Aucun RGB, territoire ou donnée de départ modifié.
- Aucun lancement de Victoria 3, changement de playset, intégration GUI, staging, commit, merge ou push. Les avertissements préexistants des lots MAP ne sont ni corrigés ni réattribués à ce prototype.

La superposition de scans est préparée et testée mathématiquement sur un cas synthétique. Aucune carte ancienne n’est présentée comme géoréférencée et validée par ce seul test. Les graduations d’origine des cartes historiques, les déformations du papier et leurs CHECK restent à traiter.

## Fichiers de l’outil

`tools/map_georeference.py`, `tools/georeference/model.py`, `controls.example.json`, `index.html`, `style.css`, `app.js`, `start-georeference.ps1`, `README.md`, `tools/test_map_georeference.py`, `tools/validate_map_georeference.py`.

Résultats : `VALIDATION.json`, quatre profils de modèle, `grille_locale_0p5deg.png`, `INTERFACE.png`. Le rapport territorial Erfurt–Eichsfeld reste NON IMPLÉMENTÉ ; les preuves anciennes rejetées ne sont pas écrasées.

## ColGrep et ressources

Un appel réussi à ColGrep-Agent-2B local pour localiser les outils et preuves de projection/graduations. Exécutable `C:/Users/simeo/.cargo/bin/colgrep.exe`, option `--agent`, recherche limitée à `./tools`. Les pistes `tools/map2l_erfurt.py:31–34` et `tools/map1_geography.py:29–146` ont été vérifiées : elles documentent une hypothèse et une projection non établie, pas une formule exacte nouvelle.

Les fichiers connus, identifiants exacts et formats raster sont contrôlés directement. Aucun nouvel index complet, modèle ou réglage d’intégration installé. Durée totale de cette recherche locale et nombre exhaustif des lectures/recherches classiques non instrumentés ; aucun compteur de tokens Codex par tâche accessible. Ces valeurs restent nulles plutôt qu’estimées arbitrairement. Le temps indiqué dans `VALIDATION.json` concerne uniquement l’exécution du validateur, pas ColGrep.

Dans cette passe ciblée, le sous-agent a surtout confirmé des chemins déjà connus : intérêt faible et aucune économie exacte démontrable. Il reste plus pertinent pour retrouver des dépendances inconnues dans les prochains lots, avec vérification systématique des résultats. Les binaires de carte ne sont pas une source sémantique fiable pour lui.
