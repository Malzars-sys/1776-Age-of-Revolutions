# Navires primitifs : corrections intégrées et proposition d'équipements

Date : 8 octobre 2026. **Archive de la proposition initiale.** Le joueur a depuis validé les améliorations, demandé des techniques et modèles précis, choisi les chaloupes pour la cogue, blocus + débarquement pour la caravelle et batterie côtière + éperon d'étrave pour la galère. L'[intégration suivante](early_ship_equipment_integration_2026-10-08.md) remplace les intitulés et le principe d'une seule spécialisation ci-dessous. Équipements et déblocages sont désormais intégrés ; nouveaux visuels en proposition seulement. Aucun essai en jeu.

## Corrections déjà intégrées

- Caravelle : groupe des navires capitaux et icône de catégorie capitale. Son profil conserve le dessin approuvé, recoloré avec la teinte et la saturation du profil natif du vaisseau de ligne. Le marron/orange précédent est remplacé par le jaune capital ; alpha, relief et proportions sont conservés.
- Galère : groupe des croiseurs et fonctionnement de défense côtière primitif. Distance maximale au port : 1, comme le défenseur côtier natif ; hors de cette portée, dégâts de coque et d'équipage réduits de 80 %.
- Les chiffres primitifs de la galère sont conservés : 1 000 points de coque, 15 dégâts de coque, 8 de blindage et 240 marins, contre 2 600 / 70 / 30 / 300 pour le défenseur côtier moderne. Aucun fer, moteur ni charbon moderne n'est ajouté à ses recettes.
- Cogue : transport de troupes, profil et paramètres inchangés. Elle reste dans le groupe natif des croiseurs, comme le transport existant ; ne pas inventer un groupe de transport non défini.
- Les coûts, effectifs, technologies et compositions des flottes de départ ne sont pas modifiés dans cette passe. Les trois coques restent actuellement sans équipement configurable et sans nouveau déblocage technologique : ce sont précisément les étapes suivantes à valider.

La [révision graphique](../assets/early_ship_sources_2026-10-08/capital_colour_revision.json) complète le manifeste d'origine, conservé comme historique. Le registre courant contient toujours 151 exports. Le contrôle `tools/validate_early_ship_roles.py --check` distingue strictement ces corrections de la proposition suivante.

## Quatre catégories, trois niveaux chacune

Réutiliser les quatre emplacements du concepteur : coque, armement, propulsion, réserves/aménagements. Les intitulés suivants sont des choix de gameplay, pas une chronologie archéologique stricte.

| Catégorie | Caravelle : projection de puissance | Galère : défense côtière | Cogue : transport de troupes |
| --- | --- | --- | --- |
| Coque et charpente | Bordage simple → membrures renforcées → charpente renforcée et bordage doublé | Coque légère → membrures renforcées → coque côtière renforcée | Coque à clins → membrures renforcées → cale et charpente renforcées |
| Armement | Pièces légères → canons sur affûts → batterie organisée | Petites pièces d'étrave → batterie avant → batterie avant lourde | Armes d'abordage → pièces pivotantes → petits canons défensifs |
| Propulsion traditionnelle | Voiles latines → gréement mixte → gréement océanique à trois/quatre mâts | Bancs d'avirons simples → nage organisée → nage perfectionnée et voile auxiliaire | Voile carrée simple → voile de plus grande surface → gréement perfectionné, sans moteur |
| Aménagements et réserves | Magasins simples → réserves de croisière → magasins de longue campagne | Vivres de cabotage → magasins améliorés → réserves côtières organisées | Cale marchande → pont adapté aux troupes → transport militaire aménagé |

Effets proposés : charpente plus robuste = coque et protection structurelle ; armement = dégâts ; voiles/aviron = vitesse ; réserves = ravitaillement pour caravelle/galère et capacité de transport pour cogue. La défense de la cogue reste faible : elle ne devient pas un navire de ligne. Les réserves améliorées de la galère ne suppriment **jamais** sa limite côtière.

Pas de moteur, charbon, blindage métallique moderne, obus ni équipement électronique. Les améliorations ont un coût croissant en bois, tissu, outils et pièces d'artillerie adaptées aux technologies ; l'organisation des rameurs peut également demander davantage de marins. Les valeurs détaillées seront fixées à l'intégration, en préservant le coût faible du modèle de base et en vérifiant les budgets au démarrage. Choisir explicitement le premier niveau comme équipement par défaut, plutôt que laisser le concepteur sélectionner automatiquement un niveau intermédiaire plus cher.

Ces choix de voilure s'appuient sur la [caravelle à quatre mâts du National Maritime Museum](https://www.rmg.co.uk/collections/objects/rmgc-object-66267), les avirons et voiles latines de sa [galère](https://www.rmg.co.uk/collections/objects/rmgc-object-66490), et le [mât unique à voile carrée de la cogue hanséatique](https://www.hanse.org/en/the-medieval-hanseatic-league/the-cog). Ils servent de références de conception, non de permission de redistribuer les images des musées.

## Modifications de fonction

Proposer un emplacement de spécialisation optionnel, avec un seul choix actif. Les trois choix d'une coque ne sont pas trois niveaux et ne se cumulent pas.

| Coque | Spécialisations proposées | Paramètres de jeu visés |
| --- | --- | --- |
| Galère | Batterie côtière ; patrouille des ports ; abordage côtier | Dégâts/précision ; détection/écran ; dégâts d'équipage/capacité de débarquement |
| Caravelle | Croisière océanique ; blocus ; détachement de débarquement | Ravitaillement ; force de blocus ; capacité de débarquement |
| Cogue | Transport d'infanterie ; transport de matériel ; chaloupes de débarquement | Capacité de transport ; capacité contre vitesse ; capacité de débarquement |

Ne pas inventer une statistique globale de « projection de puissance », ni prétendre que le moteur filtre automatiquement le type de troupe transporté. Les intitulés définissent des compromis utilisant les paramètres navals réellement exposés.

## Déblocages technologiques proposés

Les trois coques primitives exigeraient chacune une technologie maritime précoce. Les classes avancées auraient des technologies de construction dédiées plus tardives, pour ne pas retirer `scientific_naval_architecture` aux pays qui en ont besoin pour d'autres contenus.

| Coque | Technologie proposée | Place dans la progression |
| --- | --- | --- |
| Cogue | Construction maritime à clins | Ère 1, début de branche |
| Galère | Construction de galères | Ère 1, début de branche |
| Caravelle | Gréements océaniques | Ère 1, après les bases de construction maritime |
| Frégate | Construction de frégates | Ère 2, après les gréements océaniques et l'architecture navale scientifique |
| Vaisseau de ligne / man-o'-war | Construction de vaisseaux de ligne | Ère 3, après les frégates et la classification des navires |

L'ère est celle de l'arbre personnalisé du mod, pas une date historique universelle. Les prérequis conjoints sont portés par la technologie dédiée : dans la documentation native des types de navires, plusieurs entrées de `unlocking_technologies` signifient **l'une ou l'autre**, pas « toutes ».

Au départ, seules France, Grande-Bretagne, Espagne, Russie, Portugal, Pays-Bas, Danemark-Norvège et Suède recevraient les deux nouvelles technologies avancées. Prévoir aussi les tags Danemark et Norvège indépendants pour les départs où ils existent ; dans le départ courant, c'est l'union Danemark-Norvège. Les autres nations pourront rechercher ces technologies ensuite : la restriction demandée concerne l'état initial, pas une interdiction nationale permanente.

La passe d'intégration devra auditer chaque flotte de départ : tout pays hors de cette liste possédant actuellement une frégate ou un vaisseau de ligne sera adapté à des coques primitives autorisées, sans modification arbitraire du nombre de navires. Accorder les prérequis nécessaires aux pays qui possèdent déjà les coques correspondantes. Aucune modification des histoires de pays ou de flottes n'a encore été faite pour cette proposition.

## Succession et limites du rééquipement

- Caravelle → vaisseau de ligne / man-o'-war.
- Galère → navire de défense côtière.
- Cogue → navire de transport.

Ces liens désignent une progression technologique. La définition native de `concept_ship_retrofit_desc` décrit le remplacement des **équipements** pour rejoindre la dernière version du modèle de navire, et celle de `concept_ship_template_desc` rattache le modèle à un type de coque. La documentation `common/ship_types/ship_types.md` n'expose pas de champ de conversion vers un autre type. **Aucune conversion directe entre ces coques n'est confirmée ou intégrée.** La galère et le défenseur côtier moderne appartiennent même actuellement à des groupes différents.

Solution compatible à proposer : améliorer les équipements d'une coque existante, puis remplacer cette coque par une construction de sa classe successeure quand la technologie le permet. Une conversion payante scriptée serait un travail distinct à valider et tester ; ne pas inventer un champ `upgrade_to` ni promettre un bouton natif non vérifié.

## Contrôles

- Correction des rôles et recoloration : contrôle statique passé, paramètres de base et fichiers économiques/technologiques protégés.
- Reconstruction des DDS : vérifier le registre courant, pas les anciens snapshots d'intégration navale qui décrivent les rôles et la couleur précédents.
- Les contrôles de raccordement des PM et des flèches restent indépendants et préservent les cinq placeholders individuels du cuivre en attente de la version 1.15.
- Validation moteur, fonctionnement du concepteur avec les nouveaux équipements, équilibre naval et départs technologiques : à faire **après** intégration approuvée. Ne pas annoncer ces fonctionnalités comme terminées sur la base de cette proposition.
