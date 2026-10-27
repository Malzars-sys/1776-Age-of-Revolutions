# BALKANS-03 — Monténégro et interface de Cattaro

Livraison du 25 octobre 2026 — référence : 1er janvier 1776.
Statut : IMPLEMENTED_STATIC_VERIFIED_WITH_HISTORICAL_OBLIGATIONS. Moteur : NOT_RUN. Validation joueur WORLD : aucune nouvelle.

## Installation

MON est conservé. Sava demeure souverain, avec le titre de vladika ; Arsenije Plamenac est le coadjuteur initial désigné. Jovan Radonjić remplace le général procédural et représente le guvernadur. Gouvernement associant chefs laïcs et dévots, oligarchie et levées explicites ; formation « Levée des clans » avec la réserve irrégulière existante, sans les cinq réguliers de ligne et le hussard. Les relations avec Venise sont calibrées à +20, sans traité de sujétion. Détails et conventions dans INSTITUTIONS.md.

Deux fichiers courants sont retouchés uniquement dans leurs blocs MON ; six fichiers fonctionnels nouveaux. Le fichier natif des théocraties est surchargé par son nom ; seuls le titre, le titre du successeur et le commentaire du gouvernement réservé à MON changent, tous les autres gouvernements sont identiques. Aucun nouveau pays, bâtiment ou PM ; aucune recette commune ni graphe technologique modifié.

## Cellules et populations

`STATE_MONTENEGRO` : MON conserve `x8C6292`, Venise `x90A0E0` et la Porte `xF5F6C2`, `xA12F82`, `x446E84`. Zéro nouveau RGB, zéro pixel recoloré, zéro province ou habitant transféré. Bouches de Cattaro vénitiennes ; noyau ragusain, Neum et Sutorina intacts. CELLS.json et GEOGRAPHIC_CROSSWALK.md séparent les cellules du jeu des quatre nahije historiques.

| Périmètre | Avant | Après | Variation |
| --- | ---: | ---: | ---: |
| MON dans la région | 93 909 | 93 909 | 0 |
| VEN dans la région | 22 728 | 22 728 | 0 |
| TUR dans la région | 145 441 | 145 441 | 0 |
| Région complète | 262 078 | 262 078 | 0 |
| Monde | 834 936 539 | 834 936 539 | 0 |

Ce sont les POPs héritées, pas un recensement de 1776. Cultures, religions, professions et propriété des bâtiments ne changent pas.

## Technologies et institutions

Les neuf technologies sont conservées, résolues et fermées sur leurs prérequis : distillation, improved_husbandry, international_relations, light_infantry_tactics, organized_textile_production, regulated_small_arms, shaft_mining, traditional_food_processing, organized_military_establishments. La réserve est compatible avec les levées. Aucun déblocage ni PM nouveau à financer artificiellement. Le gouvernement de clans et les offices sont des approximations explicites des mécanismes disponibles, pas une administration centralisée reconstruite.

## Sources et incertitudes

SOURCES.md et SOURCE_MANIFEST.json relient chaque décision aux notices CANU, à Radosavljević et aux sources primaires publiées. Les quatre nahije — Katunska, Riječka, Lješanska, Crmnička — sont étudiées sans créer quatre polygones arbitraires. Le berat ottoman et le rattachement ecclésiastique ne sont pas confondus avec une preuve de contrôle administratif territorial intégral. Les prétentions ottomanes ne sont pas effacées par la reconnaissance internationale postérieure.

Restent ouverts : limites exactes et contenu du RGB MON ; revendication native à l'échelle de toute la région ; fiscalité/tribut effectifs en janvier ; effectifs et population datés des clans ; naissance précise d'Arsenije ; succession à long terme, hubs et viabilité économique. Aucun chiffre de recrutement hérité ou relation +20 n'est présenté comme mesure d'archive. Les limites B02 restent toutes actives : îles, Lastovo, recteur de janvier, démographie, tribut, ressources/Krka partagés, hubs et budget.

## Vérification et concurrence

113/113 contrôles propres et 36/36 contrôles de réconciliation/non-régression réussis. Le rejeu des 99 anciens contrôles B02 conserve son résultat brut 92/99 : 7 références datées ne correspondent plus au workspace courant après les mises à jour concurrentes, avec justification explicite et empreintes séparées ; les fichiers de preuve historiques ne sont pas réécrits. Les 23 derniers reçus fonctionnels B01/B02 correspondaient tous à l’entrée ; trois fichiers ensuite partagés avec Ortenbourg sont réconciliés par ses préimages et sa mutation exacte hors Balkans. Voir TEST_MATRIX.md.

2482 des 2 504 fichiers fonctionnels protégés restent identiques à l’entrée ; 22 changements externes sont recensés, sans modification ou annulation par B03. Les cinq fichiers partagés d’Ortenbourg sont reconstruits depuis les preuves indépendantes, dont les quatre pixels bavarois et le transfert de 1 000 habitants, sans variation mondiale. Les autres mutations impériales hors lot sont observées, sans valider ici leurs mécaniques. TECH-R1/R2/R3 et ECON-ALLOYS/quincaillerie sont préservés. Les deux fichiers communs changent seulement dans MON. Les 113 preuves antérieures/revue technique sont identiques. Sur 873 documents SERG initiaux, cinq ont été modifiés concurremment après notre capture pour le reçu limité de Ratisbonne SERG-RM-0039 ; ils sont conservés, archivés et recensés dans EXTERNAL_SERG_UPDATE.json, 868 restent identiques. Aucune écriture SERG par cette tâche. Aucune écriture Git, aucune modification du vanilla ; identité Git courante inchangée depuis l'entrée B03, sans retour au HEAD historique de B02.

## Progression et prochaine action

L'entrée a été recalculée à partir des critères : 5/80 Balkans et 5/320 WORLD. Ce lot ajoute uniquement T et S au noyau MON : **7/80 Balkans (8,75 %) et 7/320 WORLD (2,19 %)**. O/I/D/E/R restent PARTIAL ; V reste NOT_STARTED. Zéro nouvelle validation joueur ; aucune région close.

Prochaine passe canonique : **BALKANS-04 — possessions ioniennes et places de l'Épire**. Rester en phase balkanique. Les obligations Raguse/Monténégro seront reprises avant clôture technique. Un seul test joueur groupé à la fin des travaux balkaniques techniquement réalisables, puis attente de confirmation explicite avant toute autre région.
