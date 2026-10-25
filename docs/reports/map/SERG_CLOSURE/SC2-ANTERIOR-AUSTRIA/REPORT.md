# SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %

Passe du 19 octobre 2026. Une seule nouvelle tâche : **SC2-ANTERIOR-AUSTRIA**, P0 admissible après l'enregistrement du reçu d'Autriche intérieure. Les cinq documents canoniques ont été lus, les dépendances et le workspace contrôlés. [Autorisation](AUTHORIZATION.md), [sources](SOURCES.md), [audit régional](SECTOR_AUDIT.md).

## Validation précédente et progression

La confirmation explicite du protocole intégral d'Autriche intérieure est conservée dans [le reçu utilisateur](../SC2-INNER-AUSTRIA/RUNTIME_USER_ATTESTATION_2026_10_19.json), avec la mission originale. Styrie, Carniole et retrait maritime de Ljubljana sont désormais PASS_RUNTIME_USER_VALIDATED pour les seuls trois sous-lots installés. Aucune date effective de test, langue, capture ou mesure supplémentaire n'est inventée. Les quatre fichiers testés et les anciennes preuves sont conservés.

Le contrôle d'acceptation réussit 14/14; le validateur de suivi confirme **78/235 = 33,19 % → 82/235 = 34,89 %**, soit quatre points acquis, 24 tâches qualifiées. La présente installation partielle ne rapporte aucun point : **82/235 reste le total final**, sur le même périmètre 1.0.0. Événements additifs SERG-RM-0014 puis SERG-RM-0015; aucune autre tâche modifiée.

## Corrections installées

| Sous-lot indépendant | Avant | Après | Fichier fonctionnel |
| --- | --- | --- | --- |
| AN-I-W, agrégat de Fribourg | Aucune administration initiale AUS | Un niveau public AUS | `common/history/buildings/1776_sc2_anterior_austria_forelands.txt` |
| AN-I-A, agrégat adriatique | Aucune administration initiale AUS | Un niveau public AUS | `common/history/buildings/1776_sc2_anterior_austria_adriatic.txt` |
| AN-P-A, port de la portion AUS d'Istrie | Deux niveaux, propriétaire national VEN | Deux niveaux, propriétaire national AUS | Un seul littéral dans `common/history/buildings/01_south_europe.txt` |

Les administrations utilisent les quatre méthodes déjà compatibles avec les lois et technologies initiales autrichiennes. Deux niveaux administratifs supplémentaires au total; aucune capacité portuaire créée, aucun changement de méthode ou de réserve du port. Les deux fichiers administratifs sont autonomes; le fichier partagé est identique octet pour octet hors du seul propriétaire public ciblé. [Implémentation](IMPLEMENTATION.json), [fichiers et empreintes](FILES_MODIFIED.json), préimage `PUBLIC_PORT_BEFORE.txt` et candidat `PUBLIC_PORT_CANDIDATE.txt`.

Les offices de Fribourg et l'Intendance triestine/Conseil de Gorizia préexistent au 1er janvier 1776. Un niveau par agrégat est une approximation politique et administrative B, sans équivalence avec un effectif historique. Les réformes d'avril 1776 et des années 1780 ne sont pas projetées au départ. La souveraineté habsbourgeoise n'entraîne pas la nationalisation automatique des propriétés privées vénitiennes. Le chantier naval de la portion AUS est **conservé provisoirement, sans approbation définitive**, car son histoire corporative ne démontre pas une propriété nationale autrichienne en 1776.

## Territoires, populations et conservation

[Inventaire RGB avant/après](NATIVE_INVENTORY.json), [vue occidentale](NATIVE_WEST.png), [vue adriatique](NATIVE_ADRIATIC.png). Ces vues montrent le mod, sans frontière historique superposée.

| Ensemble inspecté | RGB et cellules conservés | Population initiale conservée |
| --- | --- | --- |
| Fribourg, Nellenburg, Constance, Burgau, Landvogtei AUS | 5 RGB, 116 cellules | 68 095 AUS en Bade, 1 973 en Wurtemberg, 10 194 en Bavière |
| Portion adriatique AUS | 3 RGB, 295 cellules | 339 850 |
| Portion adriatique VEN | 3 RGB, 500 cellules | 340 246 |

Total observé : 11 RGB/911 cellules, dont 8 RGB AUS/411 cellules. Aucun transfert territorial. Les deux administrations concernent des subdivisions totalisant 407 945 habitants initiaux, sans modifier ces habitants. Population mondiale conservée : 834 926 252. Ces chiffres sont des données installées, pas une certification démographique historique.

Propriétaires, subdivisions, groupes culturels/religieux, unités, pays, capitales, titulaires, lois et institutions impériales conservés; 574 lignes du registre et neuf titres électoraux inchangés. Les noyaux Salzbourg, Passau, Freising, Ratisbonne, Bohême, Moravie, Silésie/MAP2A et anciens noyaux souabes/franconiens/rhénans sont protégés. Styrie/Carniole et la suppression maritime de Ljubljana restent intactes, y compris le fichier de redistribution.

L'instantané courant inclut la modification concurrente du prérequis de macroéconomie. Deux scripts de démarrage des fortifications ont ensuite été ajoutés concurremment : le garde a arrêté l'installation avant écriture, leur contenu a été examiné, puis ils ont été capturés dans `INSTALL_BASELINE.json`, sans restauration ni modification. Leurs cibles n'incluent pas les subdivisions autrichiennes de cette passe. Les autres travaux américains, militaires et français sont conservés par comparaison de tous les fichiers fonctionnels. HEAD, branche et index inchangés; aucune écriture Git, aucun fichier vanilla modifié.

## Contrôles réellement exécutés

- [Statique](VALIDATION.json) : **83/83** réussis, inventaire effectif mondial avant/après, contrats précis, méthodes compatibles, registre cumulatif, anciennes preuves et concurrence.
- [Suite cumulative](TESTS.json) : **366 tests, 362 réussis, 3 échecs hérités, 1 exclusion**. Les trois échecs présument une ancienne couche finale du registre; les 574 lignes et la couche Salzbourg actuelle passent leurs gardes. Les anciens tests ne sont pas modifiés ni masqués.
- [Suite ciblée](SCOPED_TESTS.json) : **106 tests, 105 réussis, 1 exclusion**, aucun échec. Elle comprend 13 nouveaux contrats, dont refus de modifier le chantier, les propriétés privées, les capacités, les autres régions, la préimage concurrente ou les attestations.
- L'exclusion concerne uniquement le contrôle de non-modification prévu pour l'initialisation d'origine. Les 44 doublons RGB et 12 références invalides hérités sont identiques à l'instantané, sans nouvelle anomalie de ces catégories. [Analyse](TEST_REVIEW.json).
- [Suivi recalculé](TRACKER_VALIDATION.json) et contrôles finaux dans `FINAL_CHECKS.json`. Aucun test moteur effectué par l'agent.

## Blocages et prochaine action

La tâche régionale reste **BLOCKED** : Hohenberg et Fricktal sont habsbourgeois en 1776, mais leur couverture par les noyaux existants n'est pas démontrée. Il faut une proposition B fondée sur des cartes et les voisins, avec candidats RGB documentés; les anciens recalages ne sont pas relancés. Le chantier naval reste une question de propriété P1 distincte. Ces points ne sont ni reclassés P2 ni réputés corrigés par les administrations.

Les trois installations portent **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. [Protocole joueur](PLAYER_TEST_PROTOCOL.md) : nouvelle partie 1776, vérification séparée des trois sous-lots, conservations ciblées, mois complet puis sauvegarde/rechargement. Leur validation future ne suffira pas à fermer la couverture régionale. Aucun nouveau reçu humain n'est créé.

SC2-AUSTRIA demeure BLOCKED : Innviertel bavarois en 1776, attribution géographique toujours à résoudre; aucune conservation définitive approuvée. SC2-TESCHEN reste indépendant. Le suivi identifie **SC4-EXISTING-ITALIAN-STATES** comme prochaine tâche P0 indépendante admissible; elle reste NOT_STARTED et n'a été ni recherchée ni installée dans cette mission. La prochaine action du joueur est le protocole partiel ci-dessus.
