> Version actuelle : [amendement Uruguay partagé](SHARED_URUGUAY_FEEDBACK/REPORT.md), 28 octobre 2026. Le corps ci-dessous décrit la livraison initiale, désormais amendée.

# R9-03 — Colônia do Sacramento au 1er janvier 1776

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** — installation technique réalisée, sans validation moteur ou joueur. Cette passe traite uniquement le premier point de la feuille de route transmise le 27 octobre 2026.

## Installé

Sacramento est désormais une enclave côtière du Brésil colonial portugais, lui-même sujet du Portugal. Aucun nouveau pays ni type de sujet n'est créé. Les territoires terrestres environnants restent espagnols sous SC4 ; aucun corridor ne rejoint artificiellement le Brésil.

À la demande explicite du joueur, la ville est **volontairement agrandie pour sa visibilité** : 51 pixels terrestres existants, dans une enveloppe de 10 × 7 pixels, sont recolorés de `x4E1442` en `x4E1443`. Cette surface est une concession de gameplay, pas une frontière historique. Aucune terre, île ou côte n'est ajoutée. La partie restante de la province espagnole conserve son propriétaire et ne devient pas fragmentée.

Un État technique distinct, `STATE_COLONIA_DO_SACRAMENTO`, ID 3161, permet d'initialiser ses propres habitants et son port. Cet ID de State Region ne doit pas être confondu avec la nouvelle couleur de province ni avec un identifiant historique. Le nom est localisé en français et en anglais. Les cinq locators de la nouvelle région restent sur ses terres, et les locators antérieurs sont intégralement conservés.

Le calage reprend le modèle régional R9-02 : position géographique projetée près du petit promontoire côtier, lecture du plan ancien et examen du bitmap courant. Le point projeté seul tombait dans l'eau ; il n'a donc pas servi à inventer une terre. Le contour est découpé exclusivement dans les cellules espagnoles existantes voisines. La précision cadastrale n'est pas établie et l'agrandissement rendrait de toute façon une telle qualification inappropriée.

## Habitants et économie

**3 317 habitants existants** sont réaffectés depuis la portion SC4 de l'Uruguay : 1 742 habitants libres de la cohorte `brazilian` et 1 575 personnes de la cohorte `afro_caribeno` déjà au statut `slaves`. Aucune personne n'est créée ou supprimée ; cultures, religions explicitement déclarées et statuts sont conservés. Les autres habitants du State_ID restent à SC4.

Ces nombres proviennent d'un **repère démographique de 1760**, publié et commenté par Fábio Kühn, et non d'un recensement de janvier 1776. La source utilise notamment des relevés ecclésiastiques et militaires, avec des limites d'âge et de périmètre. Les catégories du mod sont des identités héritées, pas une reconstitution de toutes les origines des habitants de la place. Ce proxy est réservé à l'allocation technique ; les naissances, décès et déplacements de 1760–1776 ne sont pas inventés.

Un port commercial de niveau 1 est initialisé pour représenter la desserte attestée de la place. Il utilise les PM existants `pm_aor1776_traditional_commercial_harbor` et `pm_1776_no_raw_data_reporting`, sans octroi technologique. Tous les bâtiments antérieurs restent identiques, y compris les ports de Montevideo et ceux de R9-02. La capacité agricole est répartie 99 + 1 et la capacité de pêche 5 + 1 entre l'Uruguay restant et Sacramento : aucune augmentation de potentiel régional.

Le nouveau port prévoit 700 emplois et une production de 6 unités de marine marchande **à plein emploi**. Ce sont les paramètres de son PM, pas un emploi effectivement observé, un bénéfice garanti ou une mesure de ravitaillement. Les entrées prévues à plein emploi sont 9 unités de bois et 3 de tissu. Aucun revenu ou rendement du reste du mod n'est rééquilibré dans cette passe.

## Mer et marché : deux vérifications distinctes

Le locator du port touche réellement une province maritime du Río de la Plata (`x1FDEFC`, sortie navale 3065). Une chaîne de cellules maritimes atteint la sortie navale existante de Rio de Janeiro ; elle ne traverse pas de terre. La relation coloniale BRZ → POR est conservée telle quelle. Le port, la sortie navale et l'appartenance nationale sont configurés pour la desserte native du jeu, sans modificateur artificiel donnant 100 % d'accès au marché.

**Le fonctionnement économique en jeu reste à vérifier.** La continuité d'eau et un port déclaré ne prouvent ni le calcul moteur des liaisons maritimes, ni la disponibilité effective des travailleurs et navires, ni l'absence de pénurie. Le blocus espagnol historique n'est pas transformé en guerre automatique au démarrage. Voir [MARITIME_SETUP.json](MARITIME_SETUP.json) et [le protocole](RUNTIME_PROTOCOL.md).

## Contrôles exécutés

- **26/26 contrôles statiques passent** : empreintes installées, syntaxe, attribution unique du nouveau RGB et de l'ID, exactement 51 pixels modifiés, aucune autre attribution changée, enclave connexe, maintien du pourtour espagnol, population et identités conservées, capacités réparties, ressources/hubs antérieurs conservés, port explicite, locators sur terre, sortie et chaîne maritimes, localisation FR/EN, protections CENTRAL et R9-02, absence de changement runtime non listé pendant l'installation.
- Audit technologique BRZ : **18 constats avant et après**, aucun ajouté ni retiré. Les dettes antérieures restent ouvertes. Les commandes d'audit retournent donc un échec statique préexistant, pas une validation globale du profil brésilien.
- Le premier export JSON du vérificateur refusait un booléen NumPy : conversion corrigée. Une dépendance optionnelle absente a ensuite été remplacée par un parcours de connexité sans installation de bibliothèque. Ces deux incidents appartenaient au vérificateur ; les 26 contrôles ont ensuite été effectivement exécutés.
- Aucun chargement de Victoria 3, simulation, sauvegarde/rechargement ou validation humaine du rendu n'est attesté.

Commandes : `tools/r903.py --prepare`, `--preview --staged`, `--apply`, `--verify` ; audit `tools/validate_starting_technology_1776.py --tag BRZ` avant/après. Les copies avant et patch ne sont jamais réappliquées sur une version concurrente : l'application exige les empreintes courantes capturées.

Voir [fichiers modifiés](IMPLEMENTED_FILES.md), [validation](VALIDATION.json), [delta technologique](TECH_DELTA.json), [manifeste](PATCH.json), [sources](SOURCES.md) et [aperçu](R9_03_SACRAMENTO.png).

## Recherche locale et réserves

Un appel ColGrep `--agent` s'est achevé en **126,14 secondes**. Ses quatre plages de fichiers retournées ont été vérifiées : chemins présents et lignes valides. Les résultats ont surtout fourni des exemples généraux ; l'implémentation d'Unalaska déjà connue restait plus directement utile pour l'État portuaire et ses locators. Les recherches exactes ont utilisé `rg`. Le temps global des recherches classiques et les tokens Codex n'ont pas été instrumentés. La sortie conservée ne fournit pas de télémétrie de chargement/calcul du modèle. Aucune économie de quota exacte n'est revendiquée ; l'intérêt du sous-agent pour ce lot très ciblé est limité. Voir les fichiers `COLGREP_*`.

Restent ouverts : lisibilité au zoom de jeu habituel, clic sur l'enclave, port et accès effectif au marché, démographie de janvier 1776 et détails du blocus. Cela ne résout pas l'ensemble de la Banda Oriental, des missions ou des souverainetés autochtones intérieures.

CENTRAL-01/02 et R9-01/02 conservent leurs preuves et statuts en attente de validation en jeu. Aucune correction des cinq autres secteurs de la nouvelle feuille de route n'est lancée dans ce lot. Aucun commit, push ou fichier vanilla modifié.
