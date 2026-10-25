**AUDIT TECHNOLOGIQUE 1776 — MICRO-ÉTATS ET PAYS RESTAURÉS**

Audit complet des pays présents, correction fonctionnelle partielle installée ; le monde entier n'est pas déclaré conforme. **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** pour les huit corrections, aucun reçu humain nouveau.

## 1. Cause racine et moteur

BGT avait un historique, un gouvernement et un souverain, mais aucun grant de technologie : son effet politique vanilla ne donne aucun savoir. Le nouveau TAG n'hérite pas des technologies AUS. BRX et TRT n'avaient que des grants ponctuels. Syntaxe et effets contrôlés sur le vanilla local **1.13.11**, avec arbre et paliers 1776 du mod. Aucun effet vanilla 1836 copié et aucun problème d'exécution moteur prétendument observé par l'agent.

La mine BGT exige `shaft_mining` pour sa construction ; l'absence de ce gate ne prouve pas à elle seule qu'un bâtiment forcé par l'historique n'avait aucune production. La méthode additionnelle de données exigeait aussi `scientific_metrology`, sans rapport nécessaire avec l'extraction traditionnelle. Ces deux problèmes sont traités séparément.

## 2. Inventaire exhaustif et catégories

**470 pays présents**, dont **93 nouveaux TAGs du mod**. **462** ont au moins un historique retrouvé ; **442** ont un ensemble technologique non vide après correction. **252 PASS** de cohérence statique de profil, sans validation moteur. Les 28 ensembles vides restants comprennent 17 choix explicites de la recherche existante, trois cas à revoir et huit historiques absents ; ils ne sont pas assimilés à l'omission BGT.

| Catégorie principale, exclusive | Avant | Après |
| --- | ---: | ---: |
| PASS | 246 | 252 |
| MISSING_HISTORY | 8 | 8 |
| MISSING_TECH_INITIALIZATION | 1 | 0 |
| INCORRECT_TECH_PROFILE | 12 | 7 |
| BUILDING_TECH_CONFLICT | 43 | 45 |
| RESOURCE_OR_PM_CONFLICT | 0 | 0 |
| REQUIRES_HISTORICAL_REVIEW | 160 | 158 |

Les colonnes détaillées conservent les anomalies simultanées. Ainsi les 45 lignes de catégorie principale bâtiments ne sont pas tous les pays ayant un conflit : **114 pays** portent au moins un signalement bâtiment/PM/ressource. Un profil en revue historique reste classé en revue même s'il porte aussi un tel signalement. Les écarts aux vieux plans ne sont pas tous des erreurs actuelles : IDs supprimés et évolutions ultérieures sont visibles.

## 3. Corrections installées

**28 ajouts ciblés**, sans suppression technologique, dans **huit pays**. Un socle commun partagé et cinq extensions étroites remplacent les listes copiées. Aucun coke, vapeur, rail, métrologie ou génie professionnel supplémentaire n'est accordé.

| TAG | Avant | Après | Ajouts |
| --- | ---: | ---: | --- |
| BGT | 0 | 10 | distillation, improved_husbandry, international_relations, organized_forestry, organized_textile_production, organized_workshops, periodical_print_networks, shaft_mining, traditional_food_processing, traditional_papermaking |
| BRX | 1 | 8 | distillation, improved_husbandry, organized_textile_production, organized_workshops, periodical_print_networks, traditional_food_processing, traditional_papermaking |
| TRT | 4 | 10 | distillation, improved_husbandry, institutionalized_scientific_exchange, organized_textile_production, periodical_print_networks, traditional_food_processing |
| PAP | 15 | 16 | organized_military_establishments |
| CAR | 6 | 7 | organized_military_establishments |
| ARK | 18 | 19 | improved_husbandry |
| VIE | 18 | 19 | improved_husbandry |
| LGE | 12 | 13 | shaft_mining |

BGT et BRX restent sans technologie militaire nouvelle. TRT reçoit notamment le parent scientifique de sa médecine déjà attribuée. PAP et CAR reçoivent seulement le parent administratif de leurs capacités militaires existantes. ARK/VIE reçoivent un socle sous leurs techniques agricoles existantes, sans certification générale de leurs profils. Liège reçoit le savoir d'extraction attesté pour sa houille, sans importer tout le profil belge. MCA conserve ses dix nœuds : pas de mine de Carrare créée pour un territoire absent du noyau.

## 4. Mine de Berchtesgaden et économie

Mine native publique **niveau 1**, capacité écrite de **5000 postes**, pioches/pelles, sans explosif ni vapeur ; **collecte de données désactivée**, sans nouvelle définition de PM. Les 10 postes de données et l'intrant papier de la recette auparavant sélectionnée disparaissent ; l'extraction conserve outils **2** → sel **20** par niveau à plein fonctionnement. Ces flux sont des paramètres écrits, pas des résultats observés. Aucune saline spéciale réintroduite, aucune subvention ou population ajoutée.

La région technique Tyrol contient **18** niveaux de sel découverts ; ce n'est pas la capacité propre à BGT. La portion locale et l'accès effectif au marché restent à vérifier. Avec **1000 habitants**, qui ne sont pas tous des actifs, et une chancellerie de 100 postes, le recrutement partiel est attendu. Aucun revenu, prix, emploi réel ou rentabilité n'est inventé ; aucun marché ou accord ajouté artificiellement.

## 5. Questions ouvertes précises

- **Huit historiques absents** : AP7, CKC, FRS, GR7, HWA, INDOP, PLW, TTI, tous décentralisés. Pas de profil occidental forcé ; recherches par communauté nécessaires.
- **Sept dettes de prérequis** : AUS, BEO, FRA, PRU, RUS, SAX et SWE possèdent `alloysworking` sans le `coke_smelting` actuellement exigé. La note historique des alliages et le graphe doivent être arbitrés ; le coke n'est pas offert pour masquer la contradiction.
- **158 profils en revue historique** et d'autres cas techniques portent notamment des différences avec les plans anciens, des profils régionaux copiés, ou les huit distributions de signaux navals classées tardives par une ancienne matrice. Les listes de 21 nœuds PAS/FSI/RBI/RCI/SLZ sont techniquement présentes et fermées, mais ne sont pas automatiquement certifiées dans toutes leurs spécialisations.
- **207 conflits de gates dans les déclarations initiales**, contre 210 avant, et **16 avertissements de ressource régionale**, soit **223 lignes** dans le CSV complet. Ports, universités, baleinières, armureries, centres commerciaux et recettes industrielles exigent une réconciliation par procédé. Certains historiques complètent d'autres couches : ce sont des signalements statiques, pas 223 blocages moteur certifiés. Aucune flotte, finance ou machine avancée attribuée en masse.
- BGT a aussi des incompatibilités politiques **préexistantes et distinctes** : variantes impériales réservées à certains TAGs n'incluant pas BGT ; écoles religieuses incompatibles avec le servage. L'effet politique vanilla demande également des lois dont les gates 1776 sont différents. Le journal existant du joueur en donne des avertissements, conservés comme extrait antérieur, sans prétendre à un nouveau test moteur. Les lois et déclencheurs restent inchangés conformément au périmètre de protection.

La liste exhaustive est dans COUNTRIES_REQUIRING_REVIEW.csv, pas dans une liste limitée aux micro-États européens. `sericulture` reste un marqueur régional ancien fonctionnel ; `can_research = no` ne suffit pas à le traiter comme obsolète.

## 6. Vérifications et conservation

**72/72 contrôles statiques**, **29/29 tests ciblés**. **521/533 tests cumulatifs réussis**, onze anciennes assertions de snapshots/reçus classées, une exclusion héritée, **aucun nouvel échec inexpliqué**. Traces et classements sont conservés ; aucun ancien test supprimé ou modifié.

Seuls trois fichiers fonctionnels appartiennent à cette passe : un nouvel effet partagé, un nouvel historique additionnel et le seul choix de PM de données dans l'historique du bâtiment BGT. Tous les anciens historiques nationaux sont identiques ; définitions de pays, souverains, lois écrites, populations, diplomaties, frontières, bâtiments/PM globaux, fortifications/génie, Anzin, drainage, infrastructures, Saint-Gobain et États-Unis sont préservés. Le marché et l'équilibre réel ne sont pas simulés par ce contrôle.

Les profils sont appelés dans l'historique national uniquement : aucune attribution au premier tick ajoutée. Le chargement réel et la sauvegarde/rechargement relèvent du protocole joueur.

## 7. Suivi et prochaine action

**SERG inchangé : 82/235, 34,89 %, 24/81 tâches qualifiées**. Tous les fichiers de suivi, événements et reçus ont gardé leurs octets. RG-D-CITY demeure distinct et en attente ; aucun nouveau PASS_RUNTIME_USER_VALIDATED, aucune tâche territoriale commencée, notamment Ortenburg. Aucun Git d'écriture ni fichier vanilla modifié.

Prochaine action : nouvelle partie, vérifier BGT et les huit profils corrigés, quelques témoins dont MCA/SLZ/PAS/Anhalt et l'échantillon asiatique, absence de paquet supplémentaire au premier jour, un mois, sauvegarde/rechargement. Le test ne clôturera pas automatiquement les régions ou les autres signalements.


Fichiers : [STARTING_TECH_AUDIT_1776.csv](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/technology/STARTING_TECH_AUDIT_1776_R1/STARTING_TECH_AUDIT_1776.csv>), [STARTING_TECH_BEFORE_AFTER.csv](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/technology/STARTING_TECH_AUDIT_1776_R1/STARTING_TECH_BEFORE_AFTER.csv>), [BUILDING_TECH_CONFLICTS.csv](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/technology/STARTING_TECH_AUDIT_1776_R1/BUILDING_TECH_CONFLICTS.csv>), [TECH_VALIDATION.json](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/technology/STARTING_TECH_AUDIT_1776_R1/TECH_VALIDATION.json>), [SOURCES_AND_DECISIONS.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/technology/STARTING_TECH_AUDIT_1776_R1/SOURCES_AND_DECISIONS.md>), [PLAYER_TEST_PROTOCOL.md](<C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork/docs/reports/technology/STARTING_TECH_AUDIT_1776_R1/PLAYER_TEST_PROTOCOL.md>).
