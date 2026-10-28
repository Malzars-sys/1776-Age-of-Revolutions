# TECH6A3 — Conditions de travail des plantations d'épices (28 octobre 2026)

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Changement isolé du chantier administratif VOC / Pays-Bas (PR #10). Aucun merge demandé.

## Demande et portée

Ajouter un groupe global de conditions de travail au bâtiment `building_spice_plantation`, sur le modèle des autres plantations du mod : main-d’œuvre standard, pratiques abusives, mauvais traitements. Les deux variantes coercitives doivent être indisponibles sous l'interdiction de l'esclavage. Examiner séparément l'intérêt historique et ludique d'un groupe secondaire de préparation des épices ; aucun tel groupe n'est implémenté dans cette passe.

## Scripts installés

- `common/buildings/10_tech6a3_spice_plantation.txt` : rattache le nouveau groupe `pmg_spice_working_conditions` après la production de base et avant le transport.
- `common/production_method_groups/10_tech6a3_spices_pmgs.txt` : trois PMs, dans l'ordre de défaut ci-dessous.
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

## Recherche : un second PM de préparation ?

**Oui, le procédé physique est avéré.** Le séchage est essentiel à la conservation et au transport des épices au long cours, y compris dans les réseaux des compagnies orientales. Pour le poivre noir, on sèche le fruit entier ; pour le poivre blanc, une étape de trempage / séparation de l'enveloppe précède le séchage. Le girofle et la muscade/macis ont d'autres opérations de séchage, tri ou préparation.

**Mais ne pas implémenter un nouveau groupe à ce stade** : l'actuelle ressource `spices` représente plusieurs plantes et lieux, donc un choix strictement `poivre noir / poivre blanc` ne convient pas aux girofles et muscades. Un simple `aucun séchage / séchage` serait une fausse alternative historique : le séchage est déjà supposé dans la production du bien commercialisable. Une option `séchage solaire traditionnel / tri et séchage soigné` pourrait constituer un futur PMG, à condition de distinguer nettement ses coûts (emplois supplémentaires, consommation de matières) et gains (réduction des pertes / qualité), sans bonus gratuit ni technologies tardives placées en 1776. Les sources ne justifient pas à elles seules des chiffres de rendement précis.

Sources de recherche :
- EGO, *East India Companies* (aperçu scientifique), https://pure.eur.nl/files/122020582/East_India_Companies_EGO.pdf — épices séchées avant le transport transocéanique ; variété des espèces.
- FAO, *Production, handling and processing of nutmeg and mace*, https://www.fao.org/4/x5047E/x5047E06.htm — séparation, tri et séchage.
- PlantUse / PROSEA, *Piper nigrum*, https://plantuse.plantnet.org/en/Piper_nigrum_%28PROSEA%29 — transformation du poivre noir et du poivre blanc.
- UNIDO, *Pepper processing*, https://downloads.unido.org/ot/47/89/4789710/10001-15000_10198.pdf — distinction technique noir/blanc, séchage, préservation ; certaines techniques plus tardives ne conviennent pas à 1776.
- Cambridge, *Colonisation and cultivation: Nutmeg production, labour and ecology on the Banda Islands*, https://www.cambridge.org/core/journals/journal-of-southeast-asian-studies/article/colonisation-and-cultivation-nutmeg-production-labour-and-ecology-on-the-banda-islands-before-and-after-the-conquest-of-1621/BF86973D1324DB0D0FE680E0BF5291F7 — usage de travailleurs réduits en esclavage, mais ne confirme pas une amélioration systématique de productivité due à la coercition.

## Contrôles statiques

- Accolades équilibrées ; un seul nouveau groupe sur la plantation d'épices ; trois PMs uniques, correctement ordonnés et traduits en français et anglais.
- Tous les PMs existants des épices ainsi que les deux anciens groupes (base et transport) préservés.
- Standard sans verrou esclavagiste ; interdiction d'esclavage présente dans les restrictions des deux autres méthodes.
- Pas de changement de recette de base, de niveaux de bâtiments, de propriétaire VOC, d'histoire des POPs, de technologies ni d'icônes DDS.
- **Pas de chargement du moteur, d'interface PM ou de simulation** : vérifier le fonctionnement réel et les évolutions lors de changements de loi.

## Tests joueur

Démarrer une nouvelle partie en 1776, ouvrir une plantation d'épices DEI et une plantation d'épices dans un pays ayant interdit l'esclavage. Vérifier 3 PMs, leur traduction, le défaut standard, les effets en production et la non-disponibilité des deux méthodes coercitives dans le pays abolitionniste. Tester le passage ultérieur d'une loi de traite/servitude à une loi d'interdiction ; vérifier que le jeu reconfigure le PM et que la production reste stable et sans erreur. Avancer un mois et sauvegarder/recharger.
