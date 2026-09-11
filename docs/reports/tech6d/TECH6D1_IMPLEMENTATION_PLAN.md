# TECH6D1 — Plan d'implémentation proposé

Ce document ordonne les travaux identifiés par l'audit. Il ne constitue pas une autorisation d'implémenter. Les quantités, les localisations et les tests runtime devront être traités dans des phases séparées.

## Principes directeurs

1. Ne créer aucun nouveau bâtiment pour les candidats B01–B08.
2. Réutiliser exclusivement les biens et technologies déjà présents, sauf décision ultérieure explicite sur P05.
3. Ajouter le moins possible de PMG : préférer un PM dans un groupe existant lorsqu'il s'agit d'une progression du même processus.
4. Ne jamais déduire l'accessibilité d'un PM de sa seule définition ; valider PM → PMG → bâtiment → technologie.
5. Éviter les bonus gratuits : chaque hausse de productivité doit avoir un coût matériel, énergétique ou d'emploi.
6. Conserver les architectures TECH6C validées : pharmacie dans les travaux chimiques, précision dans l'outillage, cuivre séparé, aluminium sans bauxite/alumine, engrais séparés de la chimie industrielle.
7. Ne pas créer de technologie dédiée si un verrou actuel exprime correctement l'étape historique. Les cinq vagues ci-dessous peuvent utiliser uniquement des technologies existantes.

## Wave A — Sidérurgie initiale

### A1 — P01 Coke Blast Furnaces

- Ajouter un PM coke à `pmg_steelmaking_process` dans `building_steel_mill`.
- Utiliser `coke_smelting` comme verrou.
- Réexaminer le verrou du bâtiment : dans l'état actuel, l'aciérie n'est accessible qu'avec `puddling_and_rolling`, ce qui rendrait un PM coke historiquement antérieur inaccessible.
- Employer fer + charbon et produire moins d'acier que le stade puddlage ; ne créer ni fonte ni charbon de bois comme nouveaux biens.

Critères d'acceptation : PM visible après `coke_smelting`, sélectionnable avant `puddling_and_rolling`, non dominant après l'arrivée du puddlage, aucune technologie vide créée.

### A2 — P02 Puddling and Rolling

- Transformer l'identité du stade de base actuel `pm_blister_steel_process` en une représentation explicite du puddlage/laminage, ou ajouter le nouveau PM puis retirer proprement l'ambiguïté de l'ancien.
- Conserver `puddling_and_rolling` comme verrou.
- Garder un écart économique lisible face au coke : davantage d'outillage et/ou d'emplois qualifiés contre plus d'acier.

Critères d'acceptation : progression coke → puddlage visible dans la même PMG, sauvegardes existantes traitées, aucune rupture de l'activation historique actuelle du PM de base.

### A3 — P03 Route Thomas / Bessemer basique

- Ajouter une alternative au `pm_bessemer_process`, non un remplacement.
- Réutiliser `bessemer_process` comme verrou.
- Employer le calcaire comme coût distinctif et produire une petite quantité d'engrais comme coproduit ; éviter un PM strictement supérieur sur tous les axes.
- Ne créer ni phosphoric ore ni slag.

Critères d'acceptation : Bessemer générique et Thomas ont chacun un cas économique, l'engrais ne déséquilibre pas la chaîne phosphate, la sélection IA reste stable.

Point d'arrêt après la vague A : test parser, démarrage, visibilité des quatre stades sidérurgiques, rentabilité comparative et comportement IA sur une économie disposant ou non de calcaire.

## Wave B — Liens chimiques, raffinage et mines

### B1 — P09 Blanchiment du papier

- Modifier seulement `pm_bleached_paper`.
- Conserver `industrial_chemicals` comme intrant chimique central.
- Retirer ou réduire les anciens intrants soufre/teinture uniquement après calcul de rentabilité ; ne pas toucher au PM textile.

Risque : faible. Contrôle principal : prix du papier et demande de chimie industrielle.

### B2 — P15 Craquage tardif

- Ajouter un unique PM au `pmg_base_building_oil_refinery`.
- Verrou recommandé : `plastics`; `compression_ignition` n'est qu'une alternative si la chronologie de la branche l'exige.
- Employer pétrole + produits chimiques industriels + électricité.
- Déplacer le rendement vers les carburants raffinés et hors des produits lourds, plutôt qu'augmenter simultanément tous les coproduits.

Risque : élevé. Contrôles : prix des trois produits raffinés, choix IA, pénuries d'électricité/chimie, rentabilité comparée à la distillation fractionnée.

### B3 — P07 Ventilation minière

- Créer une seule PMG réutilisable sur charbon, fer, plomb, soufre, or, cuivre et phosphate.
- Commencer sans sel ; exclure le calcaire.
- Prévoir arrêt, ventilation vapeur puis ventilation électrique.
- Utiliser moteurs/charbon ou électricité/équipement, remplacer une part des ouvriers par machinistes/ingénieurs et réduire la mortalité propre aux employés du bâtiment.
- Ne pas accorder de débit gratuit ; un éventuel petit gain doit être compensé.

Risque : moyen. Contrôles : effets par niveau, cumul sur États miniers, coût salarial et énergétique, absence d'effet démographique global injustifié.

Point d'arrêt après la vague B : validation économique sur marchés avec et sans pétrole/chimie, comparaison mines ventilées/non ventilées et absence de doublon avec pompage/explosifs.

## Wave C — Chaîne du froid et alimentation

### C1 — P16 Réfrigération mécanique

- Ajouter une étape à chacun des trois PMG hérités : élevage, quai de pêche, station baleinière.
- Verrou : `high_pressure_steam`.
- Intrants : moteurs + charbon ; aucune technologie ni ressource nouvelle.
- Positionner ce PM sous le stockage électrique et conserver l'option non réfrigérée.

### C2 — P18 Minoterie à cylindres

- Ajouter un PM intermédiaire dans `pmg_automation_building_food_industry`.
- Verrou : `automated_flour_milling`.
- Employer moteurs et/ou outils, réduire les ouvriers au profit des machinistes, et limiter le gain de produits alimentaires.
- Ne créer ni farine, ni moulin autonome.

Point d'arrêt après la vague C : vérifier que les options intermédiaires sont réellement choisies avant les PM électriques/tardifs et qu'elles ne deviennent pas des choix permanents dominants.

## Wave D — Électrification et production de masse

### D1 — P22 Révision des chaînes d'assemblage

- Ajouter `precision_machinery` aux PM existants d'outillage, moteurs, automobiles, armes/artillerie et munitions.
- Ne pas ajouter cet intrant au PM du meuble.
- Conserver l'électricité et les lubrifiants déjà présents.
- Ne pas ajouter papier/services à P22.

Cette révision est placée avant P20/P21 parce qu'elle réutilise six PM déjà sélectionnables et raccorde immédiatement le nouveau bien de précision à la production de masse.

### D2 — P20 Entraînement électrique unitaire

- Ajouter des alternatives électriques uniquement aux PMG d'automatisation de l'aciérie, de l'outillage, du papier, du verre et des moteurs.
- Verrou : `electrical_capacitors`.
- Ne pas créer de PMG global cumulable.
- Comparer chaque PM à son alternative vapeur sur coût d'électricité, emplois et débit.

### D3 — P21 Organisation scientifique

- Créer une PMG organisationnelle réutilisable pour les industries standardisées : outillage, moteurs, automobiles, armes/artillerie, munitions et électrotechnique.
- Verrou : `corporate_management`.
- Employer papier + services et davantage de commis/ingénieurs.
- Calibrer l'avantage pour qu'il ne soit pas automatique dans tous les marchés.

Point d'arrêt après la vague D : tests de cumul P20/P21/P22, demande de précision, électricité, papier et services, ainsi que choix IA dans les bâtiments à haut niveau.

## Wave E — Administration et information

### E1 — P24 Bureaux à tabulatrices

- Ajouter le PM à `pmg_base_building_government_administration`.
- Verrous : `central_statistical_offices` et `electrical_capacitors`.
- Employer papier, électricité et `precision_machinery` ; augmenter bureaucratie/capacité fiscale et convertir une part des commis en ingénieurs.
- Préserver `pm_switch_boards` comme étape tardive distincte ou alternative selon les tests.

### E2 — P23 Presse mécanisée

- Ajouter une PMG de services d'impression à `building_urban_center` avec option inactive.
- Stade mécanique : `mechanized_printing`, papier + moteurs.
- Stade électrique/rotatif : `mass_circulation_press`, papier + électricité.
- Produire des services ; ne pas créer de bâtiment de publication.
- Ne pas attribuer directement autorité, éducation ou assimilation sans phase de conception séparée.

Point d'arrêt après la vague E : surveiller l'échelle des centres urbains, la consommation de papier et la surproduction de services/bureaucratie.

## Décision différée — P05 Alloy Steel

P05 reste bloqué. Avant toute implémentation, il faut décider explicitement entre :

- abandonner le PM et considérer l'arc électrique comme abstraction terminale ;
- autoriser un nouveau système d'intrants d'alliage et sa géographie ;
- accepter une abstraction documentée avec des biens existants, malgré son imprécision historique.

La troisième option ne doit pas être choisie implicitement : cuivre et aluminium ne remplacent pas proprement nickel, chrome ou tungstène. Aucun fichier de gameplay ne doit être préparé avant cette décision.

## Ordre final et frontières de périmètre

```text
IMPLEMENT_NOW  = P01, P02, P03
IMPLEMENT_LATER = P07, P09, P15, P16, P18, P20, P21, P22, P23, P24
DEFER = P05
REJECT = B08 comme bâtiment autonome
```

Les autres candidats sont `NO_ACTION`. En particulier, ne pas rouvrir P04, P06, P08, P10–P14, P17 ou P19, et ne pas créer de remplacement pour B01–B07.

## Validation minimale exigée pour chaque future vague

- contrôle syntaxique et accolades ;
- existence de chaque PM, PMG, bâtiment, technologie, bien et type de modificateur cité ;
- preuve PM → PMG → bâtiment ;
- preuve que le PM est visible et sélectionnable avec la technologie attendue ;
- comparaison des recettes et emplois entre alternatives du même groupe ;
- démarrage sans erreur nouvelle ;
- test humain de l'interface sur toutes les vues concernées ;
- test économique sur plusieurs tailles de bâtiment ;
- test IA reporté à la bêta si la mise en place automatisée reste disproportionnée.

Le travail naval, la distribution initiale des technologies, les infrastructures route/rail/canal, l'équilibrage mondial des ressources et la préparation de bêta restent hors périmètre.
