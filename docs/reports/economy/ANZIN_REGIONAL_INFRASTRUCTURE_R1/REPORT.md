# Anzin, infrastructures régionales et transport industriel

Patch appliqué le 23 octobre 2026. **145/145 contrôles statiques réussis ; aucun essai moteur exécuté.**

## Compagnie des mines d’Anzin

- Activités principales : charbon et infrastructures régionales.
- Le fer reste une extension possible.
- Routes et rail partagent déjà `building_railway`, avec `building_land_transport_network` comme alias. Aucun second bâtiment ferroviaire n’est créé.
- Les méthodes ferroviaires conservent leurs technologies : chemins de fer, voitures ferroviaires en acier, traction électrique ou allumage par compression selon le PM. Aucune de ces technologies n’est attribuée à la France au démarrage par cette passe.
- Les conditions d’établissement restent fondées sur le bassin charbonnier du Nord : aucune technologie ferroviaire n’est ajoutée aux conditions de la compagnie.
- Siège préféré, directeur, icône de compagnie, conditions, cible de construction charbonnière et bonus de prospérité restent intacts. Les autres compagnies, dont Saint-Gobain, sont conservées exactement hors du bloc Anzin.

La diversification est l’abstraction de gameplay demandée ; elle ne présente pas Anzin comme exploitant un chemin de fer moderne en 1776.

## Houille grasse d’Anzin

Bien de prestige ajouté à la compagnie, basé sur le bien existant `coal`. Coefficient `prestige_bonus = 0.1`, comme les biens de prestige natifs et les miroirs de Saint-Gobain. Aucun bonus national de prestige séparé ni nouveau bien de marché ordinaire n’est ajouté. Les conditions générales natives d’activation des biens de prestige restent applicables ; aucun déblocage forcé au premier jour.

L’image fournie est conservée intégralement en PNG. Sa transparence existait déjà. L’export utilise le format natif d’un bien de prestige : DDS BGRA8, 256 × 256, neuf niveaux de mipmaps. Le PNG d’aperçu a été inspecté visuellement ; le rendu du DDS dans le jeu reste à vérifier. Français : « Houille grasse d’Anzin » ; anglais : « Anzin Coking Coal ».

## Routes et industries

- Terre : 360 ouvriers et 40 employés, contre 900 et 100. Infrastructure fixe de 3 conservée ; aucune recette de tickets inventée.
- Péage : 3,2 tickets au lieu de 2 ; emplois, bois, outils et infrastructure conservés.
- Routes pavées et goudronnées : aucune valeur modifiée.
- Vingt industries reçoivent un groupe de transport séparé, qui réutilise **les mêmes objets PM** que les mines : charrettes neutres et transport ferroviaire consommant 5 tickets, supprimant 1 000 emplois d’ouvriers et ajoutant 10 de pollution par niveau à plein emploi. Technologie `railways` conservée. Il n’y a donc aucun nouveau débouché industriel de transport en 1776 avant la recherche du rail.
- Aucun ajout aux bâtiments gouvernementaux, administrations, casernes, universités, laboratoires, forts ou monuments. Les usines d’armement sont des manufactures, distinctes des bâtiments militaires financés par l’État.

Les vingt bâtiments sont énumérés dans `VALIDATION.json`. Seuls leurs groupes de PM sont complétés ; leurs autres octets restent identiques à l’instantané courant.

## Économie et points ouverts

Le [comparatif économique](ECONOMIC_COMPARISON.md), les tableaux `PM_COMPARISON.csv` et `SCENARIOS.csv`, et les inventaires JSON couvrent les **19 PM** des infrastructures et **192 comparaisons** : référence, région peuplée, région rurale, forte/faible demande, intrants moins chers, plein/demi-emploi et débit de prospérité d’Anzin.

À prix et salaires de référence, le déficit propre aux routes en terre passe de 52,50 à 21 £ par niveau et par semaine, et celui du péage de 168,75 à 132,75 £. Dans le scénario de forte demande choisi, le déficit du péage baisse de 38,92 %. Ce sont des estimations conditionnelles, **pas des subventions observées dans une partie**.

Le transport est un bien local. Une baisse du prix supérieure à 37,5 % annule le gain brut de recettes associé à +60 % de tickets. L’IA reste libre de choisir les PM rentables ; le transport industriel n’est pas forcé et ne crée pas une demande garantie.

**Point ouvert matériel :** le transport minier retire exactement 1 000 ouvriers. Certaines combinaisons d’automatisation avancée peuvent ainsi produire un coefficient brut d’ouvriers négatif : 8 industries présentent déjà un tel cas avant ce patch, 15 après ajout du transport. Les sept cas supplémentaires et les combinaisons témoins figurent dans `INDUSTRIAL_EMPLOYMENT_SENSITIVITY.json`. Le comportement natif de plafonnement des emplois n’a pas été exécuté. Aucun rééquilibrage d’autres PM n’est entrepris contre la consigne de copie exacte ; ces cumuls demandent un essai moteur.

## Préservation et contrôles

- Six fichiers fonctionnels existants modifiés, six fichiers fonctionnels/artistiques créés ; voir `MANIFEST.json`.
- **2 414 fichiers** suivis hors périmètre. Deux évolutions concurrentes, `common/history/pops/01_south_europe.txt` et `common/history/states/00_states.txt`, correspondent exactement au reçu du chantier **SC4-MASSA-CARRARA**. Elles sont consignées dans `CONCURRENT_WORK_OBSERVED.json`, conservées sans restauration et distinguées des modifications de cette passe. Aucun autre changement inexpliqué.
- Fortifications, génie, États-Unis, Minutemen, accords franco-américains, Saint-Gobain et autres données françaises conservés hors des changements Anzin explicitement demandés.
- Prix des biens et salaires de référence lus dans le catalogue effectif ; aucun prix mondial modifié.
- Métadonnées natives et références lues dans `C:/Games/Victoria 3/game`, sans écriture vanilla. HEAD, branche et index Git inchangés.
- Localisations FR/EN complètes et uniques, UTF-8 BOM. Valeurs, références, technologies, exclusion des bâtiments gouvernementaux et format de texture contrôlés.

Les deux premiers essais de validation, désormais remplacés par le résultat final, avaient révélé une hypothèse de test incorrecte sur les gates ferroviaires et les écritures territoriales simultanées. Les gates réels ont été vérifiés sans modifier les technologies ; les deux écritures territoriales ont été rapprochées de leur reçu. Aucun fichier du chantier territorial n’a été restauré.

## Références et livraison

Les schémas natifs `common/company_types/companies.md`, `common/production_methods/production_methods.md`, `common/production_method_groups/production_method_groups.md`, les biens de prestige natifs et les fichiers du mod sont les références techniques. Les paramètres de prix et de salaire viennent de `common/defines/00_defines.txt`, des biens et des professions effectifs.

Le fichier joint de mission est conservé dans `USER_MISSION.txt`. Les ajouts ultérieurs demandés concernent le transport industriel et le bien de prestige avec l’image fournie ; l’audit des technologies de départ est annulé à la demande du joueur.

Voir [le protocole de test en jeu](RUNTIME_TEST_PROTOCOL.md) pour un mois de simulation, sauvegarde et rechargement. Les prix de marché, les salaires locaux et les subventions réellement versées restent non mesurés. La sauvegarde automatique locale repérée est binaire ; aucune donnée économique n’en a été inventée. La mission s’arrête à ce patch.
