# TECH6A3 — Conditions de travail des plantations d'épices (28 octobre 2026)

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Changement isolé du chantier administratif VOC / Pays-Bas (PR #10). Aucun merge demandé.

## Demande et portée

Ajouter un groupe global de conditions de travail au bâtiment `building_spice_plantation`, sur le modèle des autres plantations du mod : main-d’œuvre standard, pratiques abusives, mauvais traitements. Les deux variantes coercitives doivent être indisponibles sous l'interdiction de l'esclavage. Ajouter aussi un groupe de séchage des épices suivant les mêmes coûts et bénéfices que les méthodes de séchage du café, en substituant le bien épices au café.

## Scripts installés

- `common/buildings/10_tech6a3_spice_plantation.txt` : rattache `pmg_spice_drying` après la production de base, puis `pmg_spice_working_conditions`, avant le transport.
- `common/production_method_groups/10_tech6a3_spices_pmgs.txt` : deux PMs de séchage puis trois PMs de conditions de travail, avec séchage traditionnel et main-d'œuvre standard en premiers choix.
- `common/production_methods/10_tech6a3_spices.txt` : définitions et restrictions.
- Traductions dans `localization/french/tech6a3_spices_l_french.yml` et `localization/english/tech6a3_spices_l_english.yml`.

| PM | Conditions | Effet supplémentaire (par bâtiment de niveau 1 à recrutement complet) | Effets sociaux |
| --- | --- | --- | --- |
| `pm_spice_standard_labour` | Toujours disponible, y compris si l'esclavage est interdit ou si la traite est autorisée | Aucun | Aucun |
| `pm_spice_abusive_practices` | Indisponible si `law_slavery_banned` ; également incompatible avec la liste des lois de protection du travail de `worker_exploitation_coffee` | +5 épices | Mortalité des ouvriers +0,10 ; attractivité −0,25 ; niveau de vie des esclaves −1 ; modificateur de salaire minimum −0,20 |
| `pm_spice_violent_treatment` | Indisponible si `law_slavery_banned` | +10 épices | Mortalité des ouvriers +0,20 et esclaves +0,15 ; attractivité −0,75 ; niveau de vie des esclaves −2,5 ; modificateur de salaire minimum −0,25 ; importation d'esclaves +0,10 |

Les effets sont des **choix de balance** inspirés du système de plantations déjà installé, non des taux historiques mesurés de rendement ou de mortalité dans les plantations d'épices.

### Choix spécifiques

1. Ne pas réutiliser directement `default_labour` : son script générique actuel interdit `law_slave_trade`, alors que la méthode standard doit rester possible dans la VOC/DEI qui commence précisément avec cette loi.
2. Maintenir le verrou `law_slavery_banned` sur **les deux** options coercitives : l'abus ne reste donc pas accessible après l'abolition, contrairement au PM générique de café. La méthode violente demeure possible sous `law_colonial_slavery` et `law_debt_slavery` car ces lois n'abolissent pas complètement l'esclavage, ce qui correspond mieux à la demande de l'utilisateur. Les restrictions de protections ouvrières sur les abus reprennent le comportement de la plantation de café.
3. L'activation explicite des PMs dans les historiques de départ n'est pas changée : le groupe utilise son premier PM, standard, comme option par défaut. Les exploitations existantes et leurs propriétaires sont inchangés.

## Séchage secondaire : implémentation demandée et recherche

L'ancien plan de reporter ce groupe a été remplacé par la décision explicite du joueur d'implémenter deux PMs, analogues au séchage des plantations de café.

| PM | Technologie | Intrants par niveau | Production supplémentaire | Emplois additionnels | Autres |
|---|---|---|---|---|---|
| `pm_spice_traditional_drying` | Aucune | Aucun bien | **+5 épices** | **1 500 ouvriers** | Premier choix, opération en plein air |
| `pm_spice_mechanical_drying` | `high_pressure_steam` | **3 outils + 2 moteurs** | **+15 épices** | **500 ouvriers + 500 machinistes** | +5 de pollution |

Les valeurs reprennent exactement les entrées et la sortie des PMs `coffee_plantation_patio_drying` et `coffee_plantation_mechanical_drying` pour des épices, ainsi que leurs profils d'emplois supplémentaires, le verrou technologique et la pollution mécanique. Le malus de mortalité du séchage de café en plein air n'est pas recopié : l'utilisateur a seulement demandé une main-d'œuvre supplémentaire pour le procédé traditionnel.

Les textures provisoires des deux méthodes sont les icônes de séchage du café déjà livrées par le jeu ; on pourra les remplacer par une illustration spécifique aux épices si nécessaire.

La justification historique reste le séchage effectif du poivre noir, du girofle et de la muscade : cette activité fait partie de la conservation et préparation pour le transport. Le jeu représente le séchage dans une étape distincte pour offrir une décision économique sans distinguer chaque plante. Les bonus sont un choix de gameplay, pas des rendements documentés pour 1776.

Sources de recherche :
- EGO, *East India Companies* (aperçu scientifique), https://pure.eur.nl/files/122020582/East_India_Companies_EGO.pdf — épices séchées avant le transport transocéanique ; variété des espèces.
- FAO, *Production, handling and processing of nutmeg and mace*, https://www.fao.org/4/x5047E/x5047E06.htm — séparation, tri et séchage.
- PlantUse / PROSEA, *Piper nigrum*, https://plantuse.plantnet.org/en/Piper_nigrum_%28PROSEA%29 — transformation du poivre noir et du poivre blanc.
- UNIDO, *Pepper processing*, https://downloads.unido.org/ot/47/89/4789710/10001-15000_10198.pdf — distinction technique noir/blanc, séchage, préservation ; certaines techniques plus tardives ne conviennent pas à 1776.
- Cambridge, *Colonisation and cultivation: Nutmeg production, labour and ecology on the Banda Islands*, https://www.cambridge.org/core/journals/journal-of-southeast-asian-studies/article/colonisation-and-cultivation-nutmeg-production-labour-and-ecology-on-the-banda-islands-before-and-after-the-conquest-of-1621/BF86973D1324DB0D0FE680E0BF5291F7 — usage de travailleurs réduits en esclavage, mais ne confirme pas une amélioration systématique de productivité due à la coercition.

## Contrôles statiques

- Accolades équilibrées ; deux nouveaux groupes sur la plantation d'épices ; deux PMs de séchage et trois PMs de conditions de travail, tous uniques, correctement ordonnés et traduits en français et anglais.
- Tous les PMs existants des épices ainsi que les deux anciens groupes (base et transport) préservés. Séchage traditionnel +5 épices sans intrant, 1 500 ouvriers ; mécanique +15 épices pour 3 outils et 2 moteurs, 500 ouvriers et 500 machinistes et technologie vapeur à haute pression.
- Standard sans verrou esclavagiste ; interdiction d'esclavage présente dans les restrictions des deux autres méthodes.
- Pas de changement de recette de culture de base, de niveaux de bâtiments, de propriétaire VOC, d'histoire des POPs, de technologies ni d'icônes DDS.
- **Pas de chargement du moteur, d'interface PM ou de simulation** : vérifier le fonctionnement réel et les évolutions lors de changements de loi.

## Tests joueur

Démarrer une nouvelle partie en 1776, ouvrir une plantation d'épices DEI et une plantation d'épices dans un pays ayant interdit l'esclavage. Vérifier le groupe de séchage (2 PMs : traditionnel par défaut et mécanique débloqué par la technologie) ainsi que les 3 PMs de travail, leur traduction, le défaut standard, les effets en production et la non-disponibilité des deux méthodes coercitives dans le pays abolitionniste. Tester le passage ultérieur d'une loi de traite/servitude à une loi d'interdiction ; vérifier que le jeu reconfigure le PM et que la production reste stable et sans erreur. Avancer un mois et sauvegarder/recharger.
