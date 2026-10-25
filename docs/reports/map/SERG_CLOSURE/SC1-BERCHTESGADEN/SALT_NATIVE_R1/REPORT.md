**SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %**

# Berchtesgaden — remplacement demandé par une mine standard

La première capture montre la mine générique à 0/2 et le joueur signale que la saline spéciale n'est pas visible. La seconde montre un PIB de 0,57 K £ avec contribution du sel de 29,2 £ : une activité existe donc vraisemblablement malgré le défaut d'affichage. Ni cette capture ni le PIB ne constituent une validation intégrale du protocole. La cause moteur exacte de l'affichage n'a pas été isolée. Le joueur demande explicitement : « Annule. Annule ce bâtiment spécial. Donne-lui juste un niveau de mine de sel qui sera pas complètement rempli, c'est tout. » Cette décision remplace la tentative intermédiaire de petite mine spéciale SALT_FIX_R1, jamais validée en jeu.

## Installation finale

Un seul niveau de **building_salt_mine**, propriété nationale BGT, remplace la saline spécifique dans l'historique de STATE_TYROL/BGT. Méthodes ordinaires : pioches et pelles, aucun explosif, aucune automatisation vapeur, charrettes, aucun traitement supplémentaire du sel et déclaration ordinaire des données. Aucun niveau additionnel de mine n'est attribué à AUS ou à un voisin.

La mine conserve ses paramètres globaux : **5000 postes de capacité**, dont 4500 ouvriers et 500 commerçants ; sel 20 et outils 2 à plein emploi pour la méthode de base. Ces valeurs ne sont pas des effectifs initiaux ou une production effective promis. Avec 1000 habitants, le bâtiment est volontairement sous-occupé ; aucun habitant n'est ajouté pour le remplir. Aucun PM, technologie, subvention ou correctif d'effectifs spécial n'est créé. La capacité minière régionale reste identique ; aucune modification de la définition, des méthodes ou du groupe de la mine standard pour les autres pays.

La définition de saline spécifique, son PM, son groupe de PM et ses quatre clés dans chaque langue sont retirés. Le groupe de petite mine spéciale créé dans la tentative annulée est supprimé. Tous les effets et appels d'initialisation de cette tentative sont retirés ; les effets et appels de nommage Berchtesgaden retrouvent exactement leurs octets livrés avant cette passe. La chancellerie publique de 100 postes reste intégralement conservée.

## Conservation et état

Carte BGT xEDBF00/quatre cellules, populations (BGT 1000, monde 834926252), souverain, gouvernement, capitale, ressources, unités, diplomatie et registre impérial restent inchangés. Les douze cellules SLZ, BRX/TRT/MCA et tous les autres noyaux sont conservés. Travaux concurrents fortifications/génie, France/Anzin/Saint-Gobain/drainage et États-Unis conservés : seuls six fichiers fonctionnels diffèrent de la livraison précédente. Aucun retour d'un fichier partagé depuis une ancienne baseline, aucune écriture Git ou vanilla.

Les anciens rapports, preuves, attestations et 32 événements sont conservés intégralement. Le rapport original SC1-BERCHTESGADEN/REPORT.md décrit l'installation précédente ; le présent rapport la remplace seulement pour le sel. Les preuves de la tentative spéciale annulée demeurent des archives, sans rôle dans la livraison courante. Votre document joint répète la validation Brixen déjà enregistrée : aucun second reçu, événement de validation ou crédit n'est ajouté. BR-I-CORE reste PASS_RUNTIME_USER_VALIDATED ; SC1-BRIXEN reste BLOCKED P1 avec ses cinq obligations.

SC1-BERCHTESGADEN reste **BLOCKED P1**, six obligations régionales conservées ; seul BG-I-CORE révisé est **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, avec **RETEST_REQUIRED**. Aucune attestation BGT. Progression **82/235 → 82/235**, **34,89 % → 34,89 %**, 24 tâches qualifiées, 81 tâches, périmètre 1.0.0 et poids inchangés.

## Contrôles et prochaine action

VALIDATION.json : **35/35 contrôles actuels**, dont remplacement exact d'un niveau, conservation démographique et cartographique, six PM ordinaires, suppression de tout bâtiment ou initialiseur spécial du sel et conservation des fichiers concurrents. TESTS.json/log consignent la suite cumulative réellement exécutée ; les huit échecs antérieurement classés restent distingués des régressions. Les anciens tests ne sont pas modifiés ; plusieurs contrats de l'ancienne saline lisent volontairement la preuve figée de la première livraison, pas la version courante. Les 35 contrôles actuels vérifient la nouvelle version. Le validateur canonique et FINAL_CHECKS.json contrôlent suivi et conservation après les tests.

**Prochaine action : nouvelle partie 1776 et test de la mine ordinaire**, selon PLAYER_TEST_PROTOCOL.md de ce dossier. L'agent n'a pas exécuté le moteur. Le démarrage en jeu n'est pas annoncé comme acquis. SC1-PASSAU-OUTLIERS reste la candidate indépendante non commencée ; aucun autre territoire n'est traité. Blocages Brixen, Trente, Autriche/Innviertel, Teschen et Italie inchangés.

Référence historique réutilisée : [Finanzamt Berchtesgaden-Laufen](https://www.finanzamt-berchtesgaden-laufen.de/ueber-uns/geschichte), mine du Petersberg depuis 1517 et saline de Frauenreuth antérieure à 1776. Le remplacement moteur demandé ne nie pas cette distinction historique ; il regroupe l'activité dans le bâtiment ordinaire du mod.
