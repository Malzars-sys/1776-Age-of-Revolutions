# Magdebourg–Halberstadt et frontière de la Saale — livraison du 5 novembre 2026

**SERG TERRITORIAL 1.0 — PROGRESSION : 39,57 %**

**77 cellules PRU→SAX installées, en deux sous-lots politiques B.** Le raccord saxon de Mersebourg–Querfurt–Weißenfels–Naumbourg est corrigé sur **69 cellules** ; un noyau de l'office saxon de Gommern est rétabli sur **8 cellules**. Halle, Magdebourg et Halberstadt restent prussiennes. [Avant/après installé](BEFORE_AFTER.png).

## Sélection et recherche

Le joueur autorise cette passe par « Okvaziñ », après la proposition Magdebourg/Halberstadt et interfaces Saxe/Anhalt. La candidate canonique est `SC3-BRANDENBURG`, **P1 sans dépendance**, explicitement laissée ouverte par Nord saxon 1. Les instructions du dépôt, la feuille de route, l'état, la prochaine action, les blocages, l'historique et les anciennes passes utiles ont été relus. Le maintien approuvé de Glatz/Silésie reste acquis dans sa portée exacte.

La carte primaire Schenk **1758** est réutilisée et obtenue en meilleure définition pour lire la partie occidentale. Les notices des archives saxonnes distinguent les anciens apanages de leur réunion à la ligne électorale avant 1776. Les ensembles saxons concernés ne doivent pas rester attribués à PRU sur la seule base de la situation de 1836. Les cartes complémentaires de Magdebourg et Halberstadt ont été examinées ; la feuille Güssefeld **1784** reste comparative et n'applique pas à 1776 la succession de Mansfeld de 1780. [Sources, cartes lues et limites](SOURCES.md).

Le modèle natif Miller et les anciens tracés livrés sont conservés. Une nouvelle lecture de la partie occidentale de la feuille donne des résidus FIT de 0,67–2,11 cellules et CHECK de 0,88–1,45 : contrôles de lecture, **pas précision cadastrale indépendante**. Aucune frontière contemporaine n'est projetée sur 1776 et aucun ancien recalage infructueux n'est relancé. `TRACING.json` et `SOURCE_TRACE_REVIEW.jpg` rendent le choix révisable.

## Changements réellement installés

| Sous-lot | Cellules PRU→SAX | Provinces nouvelles | Portée |
| --- | ---: | --- | --- |
| `MH-SAALE-CORE` | 69 | `xEEC500` (20), `xEEC502` (49) | Noyau et raccord méridional saxons ; Mersebourg, Querfurt, Weißenfels, Naumbourg dans le diagnostic grossier |
| `MH-GOMMERN-CORE` | 8 | `xEEC501` | Noyau de l'office de Gommern ; pas le comté entier de Barby |

Les parents PRU `x618061`, `xA080E0` et `xCF5D8E` sont conservés avec leurs résidus. Tous les changements restent dans la région technique `STATE_ANHALT`, déjà partagée entre PRU et SAX ; **aucun nouvel État économique partagé**, aucun pays nouveau. Les limites économiques, ressources, capacité agraire, terrains parents et repères physiques sont conservés. Les terrains des trois enfants sont hérités de leur parent ; aucun hub ne nécessite de changement de référence ni de déplacement.

**23 202 habitants existants sont réaffectés de PRU à SAX**, par allocation entière des profils de la portion PRU de l'État. Ce n'est ni un recensement, ni une estimation historique de la population des offices : la répartition reste technique et provisoire. Les profils écrits et résolus sont conservés ; total mondial écrit inchangé, **837 328 654**. Les valeurs et ventilations figurent dans `PLAN.json` et les inventaires avant/après.

**Aucun bâtiment, niveau, PM, détenteur économique, unité, recrutement ou technologie modifié.** Les programmes économiques BUILD, les fortifications, le Corps du génie, les travaux américains/français et les autres fichiers concurrents restent préservés hors de la liste explicite d'installation.

Le registre passe de **595 à 598 titres**, par subdivision seulement. Tous les anciens titres et bénéficiaires sont identiques ; les trois titres nouveaux sont SAX. **Même étendue physique impériale, mêmes membres, neuf électeurs.** Sept dérivés territoriaux du système impérial sont régénérés après comparaison au workspace courant ; aucun conflit concurrent trouvé. La chaîne accepte ce seul manifeste borné. [Précontrôle du compilateur](COMPILER_PREFLIGHT.json), [migration](REGISTRY_MIGRATION.json), [14 fichiers installés et empreintes](INSTALLATION.json).

`GEOMETRY.json` et `PLAN.json` conservent le candidat et leurs états de préparation. Pour l'installation effective et le statut courant, les références sont `INSTALLATION.json` et le suivi canonique ; les anciens états de préparation ne sont pas des désinstallations.

## Conservation et contrôles

[VALIDATION.json](VALIDATION.json) : **41/41 contrôles différentiels réussis** sur l'installation réelle. Ils vérifient les 77 coordonnées exactes, les trois nouvelles provinces, l'ensemble des attributions mondiales, les profils démographiques, l'invariance des bâtiments/PM/unités/pays, les anciennes preuves, la chaîne du registre et l'absence de modification concurrente hors manifeste. Tous les pixels non PRU sont identiques au début de passe : Anhalt, Saxe, principautés thuringiennes et autres noyaux approuvés préservés.

Les diagnostics grossiers donnent SAX pour les cinq repères corrigés et PRU pour Halle/Magdebourg/Halberstadt. Ils ne certifient pas des positions urbaines natives. Le fragment PRU de 11 cellules près d'Anhalt, déjà présent avant cette livraison, est conservé ; il n'est pas produit par la nouvelle frontière méridionale.

Les **11 références orphelines héritées** et la dette de doublons sont inchangées et restent visibles dans les résultats. Ce contrôle différentiel n'annonce pas une carte mondiale sans erreur. Les anciens échecs de snapshots et résultats bruts ne sont pas réécrits.

Les suites ciblées réellement relancées après mise à jour du suivi sont consignées dans `TEST_RESULTS.json` et `TEST_RESULTS_RAW.txt`. Le validateur canonique et les derniers contrôles de suivi figurent dans `CANONICAL_CHECK.json` et `FINAL_CHECKS.json`. Aucun résultat ancien n'est présenté comme une nouvelle exécution. **Aucun test moteur effectué par l'agent, aucun reçu humain nouveau, aucune opération Git d'écriture et aucune modification du vanilla.**

Cette exécution comprend **73 tests : 72 réussis, 1 ignoré explicitement, 0 échec et 0 erreur**. Le test ignoré vérifie l'absence de toute modification lors de l'initialisation ancienne ; il ne s'applique pas à une installation ultérieure autorisée. La conservation différentielle du workspace actuel est couverte séparément par les 41 contrôles ci-dessus.

## Statut et réserves

Les deux sous-lots sont **`IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`**. `SC3-BRANDENBURG` reprend **`IN_PROGRESS`** ; il ne s'agit pas d'une clôture régionale. Les 393 cellules du noyau lusacien et les 606 cellules de Nord saxon 1 sont conservées avec leurs propres attentes de réception, ainsi que les autres livraisons prussiennes.

Réserves explicites :

- **Barby** : appartenance saxonne établie, correspondance recoupant la représentation Anhalt protégée ; aucune reprise automatique de ces noyaux. Gommern ne clôt pas Barby.
- **Mansfeld** : parts et succession de 1780 à distinguer ; aucune réattribution globale du comté. Les franges du Harz et obligations régionales non démontrées restent ouvertes.
- **Micro-juridictions** : aucune création pour Quedlinbourg, aucun redécoupage automatique de Hoym/Roßlau ou des enclaves. Elles restent hors priorité opérationnelle V1.
- **Démographie et fonctionnement** : la ventilation technique ne recertifie pas le peuplement historique. L'emploi, l'accès au marché, l'affichage et la simulation restent à observer par le joueur.

**Progression avant/après : 93/235 → 93/235 points, 39,57 % → 39,57 %, 32/81 tâches qualifiées.** Les 81 tâches, 235 points et le périmètre 1.0.0 sont conservés. Événement additif `SERG-RM-0069`, statuts/preuves/historique et vues canoniques actualisés sans point pour une installation partielle non reçue.

## Suite

Le [protocole joueur groupé](PLAYER_TEST_PROTOCOL_GROUPED.md) conserve les anciennes installations et ajoute les deux noyaux contrôlables séparément. **Tous les tests moteur restent différés jusqu'à la fin de la Prusse**, à la demande du joueur.

Prochaine candidate recommandée : **tri des seuls grands écarts résiduels en Gueldre/Clèves/Mark**, en réutilisant les sources et sans relancer automatiquement les anciens recalages occidentaux ou les micro-enclaves. Les réserves polonaises complètes ne sont pas effacées. Cette deuxième passe n'est pas commencée ; aucune Bavière lancée. La Prusse entière n'est pas déclarée terminée par cette livraison.

Installation dans **C:/Users/simeo/.codex/worktrees/massa-carrara-finalisation/1776_Age_of_Revolutions_fork** uniquement ; les autres copies du mod et le hotfix ne sont pas synchronisés automatiquement.
