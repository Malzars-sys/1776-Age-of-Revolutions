# MAP-2M-R9 — livraison partielle, audits et prochain secteur

**MAP-2M-R9_PARTIAL.** Le complément territorial de Wolgast est installé et la Peene est clôturée **pratiquement**, avec Peendamm abstrait. Les frontières prusso-polonaises ne sont pas déclarées terminées. Les autres possessions prussiennes ont été inventoriées, et le prochain lot du SERG est recommandé, **sans le lancer**.

## Résultats appliqués

- **2 cellules PRU→SWE**, `(4409,735)` et `(4410,735)`, dans `STATE_POMERANIA` : `xE1A03A` vers `x567452`.
- SWE 398→**400 cellules** ; parent PRU 292→**290**. Les 41 cellules R8, ainsi que toutes les 398 cellules suédoises préexistantes, sont conservées.
- **235 habitants redistribués**, sans ajout : 209 north_german/default, 21 north_german/catholic, 4 polish/default, 1 ashkenazi/default. Poméranie PRU 421 517, SWE 47 019 ; total 468 536, monde 835 804 980.
- Aucun nouveau RGB, État, pays, hub ou locator. Tous les bâtiments, PM, réserves, détenteurs économiques, infrastructures, formations et recrutements sont identiques.

La précision du joueur est prise en compte : **il n'existe pas de ville native Wolgast**. Le correctif rend son secteur géographique suédois dans la représentation de jeu ; il ne fait pas apparaître une nouvelle ville. Il n'y avait pas de locator Wolgast prussien à déplacer.

La nouvelle retouche est une approximation politique locale R9 ; contrairement à la règle très conservatrice de R8, son bord oriental peut dépasser l'aide de dessin de la rive moderne projetée. Cette limite est publiée dans `WOLGAST_CORRECTION.md`, pas transformée en frontière historique certifiée. Peendamm est omis par décision du joueur, et non déclaré reconstitué.

Statut Peene : **PEENE_GAMEPLAY_COMPLETE**, sous réserve du futur test manuel. Stralsund, Greifswald, Rügen, Anklam, Demmin, Usedom et Wollin passent les diagnostics politiques ; ceux-ci ne certifient pas au pixel chaque centre historique.

## Prusse–Pologne : ce qui reste réellement ouvert

**Zéro nouveau transfert.** Bromberg xEDB01085PRU et résidu xFCC7B7142PLC, Thorn x41A021153PRU, Dantzig x80A0A0PLC et Poznań x999CEEPLC restent inchangés. Les CSV de changements prusso-polonais et des autres frontières impériales ne contiennent que leurs en-têtes.

La ferme native Toruń n'est pas un centre historique certifié ; elle tombe au sud de la rivière native, à environ cinq pixels du diagnostic urbain de rive nord. La proposition technique R8 n'est pas installée. Deux abstractions urbaines **conditionnelles et non appliquées** sont séparées dans `THORN_ARBITRATION_PROPOSALS.csv` : U1une cellule ou U2deux cellules près du diagnostic de rive nord. Leur choix demande un arbitrage explicite ou une preuve locale, pas une annexion des153cellules.

L'audit signale aussi que le diagnostic géographique de Bromberg tombe dans le résidu PLC, tandis que le hub rural portant ce nom est dans le noyau PRU. Ce désaccord et l'anomalie d'Inowrocław ne sont pas cachés derrière la conservation du lot R3. Les limites des quatre districts et le conflit de datation du liseré méridional restent ouverts, sans nouvelle optimisation des mêmes sources ni importation1793.

## Autres possessions prussiennes et avancement impérial

Inventaire effectif : **124 références PRU**, 14 State_ID, 96 au registre impérial ; chaque RGB et ses voisins sont dans `PRUSSIAN_RGB_INVENTORY.csv`. Les corrections de Minden, Lingen/Tecklenburg, Cologne et des autres lots sont conservées.

Une anomalie supplémentaire est circonscrite : le parent portuaire Emden `xF9DCA2`,319cellules, est encore HAN. La souveraineté prussienne de Frise orientale depuis1744 est confirmée par les institutions régionales ; le contour de ce parent versus Jever et les voisins n'est pas arbitré. Aucun transfert global fondé sur le seul nom du port. Voir `PRUSSIAN_HRE_BORDERS_AUDIT.md` et ses sources.

L'inventaire `HRE_REGIONS_INVENTORY.csv` et `HRE_REGIONS_PROGRESS.md` distingue noyaux inspectés manuellement, lots installés sans reçu spécifique, franges partielles, recherches seules, audit seul et inconnues. Il couvre les State_ID du registre actif sans prétendre que ce registre soit un certificat historique. Les reçus manuels sont cités avec leurs exclusions ; **R8 et R9 ne reçoivent aucun PASS_RUNTIME_USER_VALIDATED**.

**Prochain lot recommandé : Wismar–Poel–Neukloster, STATE_MECKLENBURG/75.** La recherche existe, aucun lot correctif dédié n'est identifié, et les possessions suédoises ne sont pas représentées par un propriétaire SWE dans cette région. Aucun début de ce nouveau lot n'est autorisé ou réalisé par R9.

## Fichiers fonctionnels modifiés

1. `map_data/provinces.png` : exactement les deux cellules de Wolgast.
2. `common/history/pops/00_west_europe.txt` : quatre réductions PRU et quatre fragments SWE en Poméranie.

Les outils R9 et le présent dossier sont nouveaux. **Aucun autre fichier fonctionnel ne change depuis la capture R8**, notamment aucun fichier de locator, propriété de province, définition de région, mécanisme impérial, unité ou bâtiment. Les deux RGB étaient déjà enregistrés : leur union de jure reste inchangée, donc aucun élargissement du masque impérial n'est à régénérer.

Bitmap avant R9 : `4215acbfc274753df113979a2edb515c67ac41924696c087b15778ec52f7a054`.

Bitmap installé : `847bd58ce28426aa9be93e602641a33a689f77b68a26b58bd8cde64f98cf7ec9`.

## Contrôles

**47/47 contrôles statiques et 26/26 tests unitaires PASS** après le sous-correctif. `VALIDATION.json` détaille la conservation différentielle, les références/RGB, les connexions par côtés, les 41 cellules R8, les 235 habitants transférés, les profils complets, bâtiments/PM/propriété/armée, le registre et Git. Les tests unitaires sont enregistrés séparément dans `UNIT_TESTS.json` et `UNIT_TESTS.log`.

Les **44doublons RGB et12références invalides hérités** sont inchangés et restent des anomalies préexistantes. Les2815fichiers cartographiques antérieurs capturés et les outils R8 sont protégés par empreinte ; aucune baseline ancienne n'est réécrite. La conservation des autres corrections économiques est également couverte par les empreintes de tous les fichiers fonctionnels.

L'historique Git a été lu sans mutation ; HEAD reste f34a6b8 et l'index conserve son empreinte. Aucun commit, merge, reset, push, changement de branche ou staging. Le contrôle en nouvelle partie et un mois de simulation appartient au joueur.

## Recherche locale et limites de mesure

Une question exploratoire sur les rapports/reçus a été déléguée à `C:/Users/simeo/.cargo/bin/colgrep.exe --agent`. Premier essai refusé au verrou d'index par le sandbox ; second avec accès autorisé, sortie0 et cinq emplacements vérifiés, tous existants : deux reçus MAP2L, Franconia continuation et deux outils d'attestation/capture. Les reçus sont utiles ; plusieurs chemins étaient déjà connus.

La sortie conservée ne montre pas une bannière de chargement GGUF/GPU : **exécution effective de la commande en mode agent, pas preuve indépendante du modèle chargé ou de la Radeon**. Aucun modèle ni paramètre d'intégration changé, aucune reconstruction globale d'index demandée. Durée totale fiable non instrumentée ; compteur des tokens Codex indisponible ; aucune économie exacte de quota annoncée. Les CSV et les bitmaps sont lus directement ; recherches exactes avec `rg`, pas de prétention à les avoir tous trouvés via l'index.

Un contrôle ponctuel de chronologie d'Emden a utilisé des pages institutionnelles, sans nouvelle campagne cartographique générale. Aucun ancien recalage n'a été relancé.
