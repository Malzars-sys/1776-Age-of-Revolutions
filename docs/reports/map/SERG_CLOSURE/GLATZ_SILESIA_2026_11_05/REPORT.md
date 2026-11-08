# Glatz et Silésie — passe limitée du 5 novembre 2026

**SERG TERRITORIAL 1.0 — PROGRESSION : 39,57 %**

**Résultat : Glatz déjà prussien ; maintien du tracé méridional existant proposé en catégorie B. Aucun fichier fonctionnel modifié.** La sous-passe de recherche est terminée. Elle n'exige pas une restitution cadastrale et ne crée pas de transfert artificiel pour modifier une carte déjà compatible à l'échelle des grands ensembles.

## Périmètre et sélection

Instruction courante du joueur : « Très bien, passons qu'à Glatz et la Silésien. » `SC3-SILESIA-LUSATIA`, P1 sans dépendance, est bien la candidate inscrite après la passe occidentale. Les instructions du dépôt, le suivi canonique et les preuves des passes prussiennes et autrichiennes ont été consultés. Aucun autre territoire, micro-État ou lot bavarois n'est commencé.

## Constats et décision proposée

- **Glatz** : le saillant est déjà PRU dans `STATE_LOWER_SILESIA`. Son support technique `xC00121` conserve ses **288 cellules**, identiques au vanilla. Ce RGB inclut davantage qu'un comté historiquement délimité : 288 n'est pas une mesure cadastrale de Glatz. Les cartes historiques, complétées par la confirmation municipale de la restitution de 1763, étayent ce maintien. Voir [sources](SOURCES.md).
- **Silésie méridionale** : toutes les géométries RGB de Haute-Silésie, Moravie et Bohême examinées sont identiques à celles du vanilla. Dans la fenêtre régionale de comparaison, les **20 pixels différents** sont exclusivement des fragments lusaciens antérieurement installés : aucune différence méridionale inexpliquée. Il ne s'agit pas d'une restauration du vanilla ni d'une validation historique fondée sur le seul jeu de base.
- **Partition politique et découpage économique** : le rapprochement des sources justifie de proposer le maintien des grands ensembles de la partition 1742/1763, avec les noyaux autrichiens conservés. Haute-Silésie PRU et région technique de Moravie AUS restent séparées ; aucune variante économique partagée n'est installée.
- **Limite de précision** : R5 et Miller ne sont pas une certification locale. Landeck et Broumov peuvent changer de côté selon leur projection ; les points projetés Hlučín/Krnov ne démontrent pas une erreur de souveraineté du RGB natif. Le diagnostic de l'Oder montre un décalage physique. Cela motive une réserve B, pas un transfert aveugle de provinces ni une nouvelle série de recalages. Hlučín est historiquement prussien en 1776 ; aucune frontière tchèque contemporaine n'est appliquée.

La [proposition](PROPOSED_DECISION.json) demande un maintien B **dans ce périmètre seulement**, sans prétendre une exactitude urbaine ou cadastrale. Elle n'a pas été approuvée par le joueur. Aucun `NOT_APPLICABLE_VERIFIED` ni `PASS_RUNTIME_USER_VALIDATED` nouveau n'est attribué.

## Conservation et contrôles réellement exécutés

[VALIDATION.json](VALIDATION.json) compare les **2 859 fichiers fonctionnels** à la capture de départ et réexamine l'inventaire complet : propriétaires, géométrie, profils de population, bâtiments, PM contenus dans les déclarations, pays et unités sont inchangés. Les manifestes des anciennes passes et des noyaux autrichiens sont vérifiés ; les **418 cellules SAX** du lot lusacien sont préservées, ainsi que `x71E080` (92), `xF0E080` (219) et `x9061E0` (179). Le registre est comparé à l'empreinte après installation du dernier manifeste B32 préservé ; aucune prétendue capture initiale du registre n'est inventée.

Les **11 erreurs de références globales héritées** et les doublons hérités, dont la déclaration répétée du Yukon, restent identiques. Ils ne sont ni réparés hors périmètre ni dissimulés sous une affirmation de carte mondiale sans erreur. Leur détail reste dans le résultat brut. Aucun test moteur n'a été lancé.

Les suites ciblées effectivement relancées sont détaillées dans [TEST_RESULTS.json](TEST_RESULTS.json), avec leur [sortie brute](TEST_RESULTS_RAW.txt). Le suivi, le registre, les reçus et les primitives de géoréférencement sont testés sur le workspace courant. [FINAL_CHECKS.json](FINAL_CHECKS.json) consigne le validateur canonique, la conservation finale et le contrôle de différences. Les résultats antérieurs ne sont pas présentés comme de nouvelles exécutions.

Résultats de cette exécution : **26/26 contrôles de conservation réussis ; 73 tests ciblés exécutés, 72 réussis et 1 ignoré explicitement** (contrôle de non-écriture propre à l'initialisation ancienne, inapplicable aux modifications ultérieures autorisées). Aucune erreur ou assertion en échec dans ces suites finales. Le validateur canonique confirme **93/235, 39,57 %, 32/81**. Les interruptions de développement du lecteur et du contrôle documentaire sont consignées séparément dans `DEVELOPMENT_CHECKS.json` ; ce ne sont pas des pannes moteur.

## Suivi, progression et suite

`SC3-SILESIA-LUSATIA` passe de `BLOCKED` à **`IN_PROGRESS`** : examen borné achevé et proposition concrète de maintien disponible. La clôture régionale reste ouverte, notamment la décision de maintien, la réception du noyau lusacien et la couverture démographique au périmètre requis. Les preuves antérieures et la décision autrichienne ne changent pas de portée. L'absence de réception n'est pas recyclée en blocage technique empêchant le travail autorisé.

**Avant / après : 93/235 points, 39,57 %, 32/81 tâches qualifiées.** Aucun point pour une proposition ou une simple lecture ; dénominateur, tâches et version 1.0.0 conservés. Événement additif `SERG-RM-0067`, vues canoniques et historique actualisés par contrôle du contenu courant avant écriture.

Les tests moteur restent différés, à la demande du joueur, jusqu'à la fin de sa passe Prusse. Le [protocole groupé](PLAYER_TEST_PROTOCOL_GROUPED.md) conserve les anciens contrôles et ajoute seulement des témoins visuels de Glatz/Silésie. **Prochaine action préparée : décision sur le maintien B, puis réception prussienne groupée lorsque la passe est terminée par le joueur.** Les réserves occidentales et polonaises déjà documentées ne sont pas effacées et la Prusse entière n'est pas déclarée close. Aucun autre chantier lancé, aucune opération Git d'écriture, aucune modification du vanilla.
