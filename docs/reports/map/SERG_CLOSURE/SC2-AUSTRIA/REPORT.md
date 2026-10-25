# SERG TERRITORIAL 1.0 — PROGRESSION : 33,19 %

Passe du 19 octobre 2026. **SC2-AUSTRIA — Haute et Basse Autriche : P0 BLOCKED sur la correspondance territoriale occidentale. Aucune nouvelle installation fonctionnelle.**

## Décision précédente enregistrée et progression

L'utilisateur approuve explicitement la décision silésienne de conservation B sans correction, dispense cette passe sans modification d'un nouveau test moteur et exclut cadastre/Teschen. Après huit contrôles de conservation, **SC2-AUSTRIAN-SILESIA devient NOT_APPLICABLE_VERIFIED**, jamais PASS_RUNTIME_USER_VALIDATED. [Décision utilisateur](../SC2-AUSTRIAN-SILESIA/DECISION_USER_APPROVED_2026_10_19.json), [acceptation et limites](../SC2-AUSTRIAN-SILESIA/ACCEPTANCE_2026_10_19.md). Rapport, proposition et anciens reçus laissés intacts.

Progression vérifiée : **75/235 = 31,91 % → 78/235 = 33,19 %**, 23 jalons justifiés. Le validateur préalable sélectionne SC2-AUSTRIA, P0 phase 2 sans dépendance. Une seule nouvelle étape autorisée. Après l'audit autrichien bloqué : **78/235 = 33,19 %**, zéro point Autriche acquis. Barème, périmètre 1.0.0 et 81 tâches inchangés.

## Audit et différence historique identifiée

Trois cartes réellement ouvertes : Jaillot/Ottens Haute/Basse Autriche **1725–1750**, Seutter Haute-Autriche **1740–1760**, Homann Basse-Autriche **1702–1715**. Elles sont confrontées au traité original du **13 mai 1779**, à la chronologie officielle de Haute-Autriche, aux notices de cadastres et à la chronologie des levés DORIS. [Sources datées et limites](SOURCES.md).

[Sous-lots AU-N/E/S/W/P/I/D](SECTOR_AUDIT.md) : interfaces Bohême/Moravie, Hongrie, Enns/Styrie, Innviertel/Hausruck, possessions intercalées de Salzbourg/Passau, institutions et dépendances. Les onze RGB sont inventoriés avec cellules, propriétaires, voisins et registre; les locators de Vienne/Linz/Freistadt identifient des repères du jeu, sans prouver une souveraineté de 1776.

**L'Innviertel est encore bavarois en 1776, sa cession étant postérieure.** Le polygone occidental xFDA6CB, aujourd'hui AUS, est un périmètre candidat à examiner, pas une frontière historiquement homologuée de l'Innviertel. Le transférer entier ne permet pas d'exclure les interfaces de Salzbourg, du Hausruck autrichien et des seigneuries passauviennes. Les acquisitions d'Obernberg/Vichtenstein de 1782 sont également distinguées. Les noyaux déjà validés ne sont pas rouverts.

Le diagnostic R4 préexistant n'est pas un profil d'installation : écart indépendant 4,6744 pixels, sensibilité 3,4104–6,0038. Aucun nouveau calage ou translation sur les mêmes points n'est lancé. Aucun rectangle autour d'une ville calculée n'est installé. [Options refusées et motif](OPTIONS_REVIEW.json).

**Ce blocage ne demande pas un cadastre parfait.** Une approximation politique B est autorisée, mais il faut pouvoir placer une portion excluant suffisamment les juridictions voisines. Cette correspondance n'est pas établie ici. Aucune correction fonctionnelle n'est donc installée; aucune décision « conforme sans correction » n'est proposée pour masquer le problème. La tâche reste **P0 BLOCKED**, sans report approuvé. Sa reprise exige un contrôle spatial indépendant applicable au bitmap ou un périmètre B étayé. Ce diagnostic précise R02 dans le périmètre déjà prévu, sans étendre les tâches ni changer le dénominateur.

## Avant / après

| Élément | Avant | Après |
| --- | --- | --- |
| STATE_AUSTRIA, id 51 | 11 RGB, 2 523 cellules AUS | Identique |
| xFDA6CB occidental | AUS, 179 cellules, [4387,905–4406,928] | Identique; correction non délimitée |
| Population autrichienne régionale | 1 638 057 | Identique |
| Population mondiale écrite | 834 926 252 | Identique |
| Bâtiments/PM/propriétés/réserves | Déclarations installées, dont administration | Identiques |
| Recrutement régional écrit | 70 permanents, 6 conscrits | Identique, formations et types conservés |
| Pays, capitale et souveraine | AUS, Vienne, Marie-Thérèse | Identiques |
| Géométrie et ressources | Bitmap et définitions actuels | Identiques |
| Registre impérial | 574 entrées, neuf électeurs | Identique |
| Bohême, Moravie, MAP2A, noyaux SLZ/PAS | Périmètres antérieurs | Identiques |

[Inventaire complet](NATIVE_INVENTORY.json), [frontières avant/après](BOUNDARY_AUDIT.json), [carte technique numérotée](NATIVE_READING.png). Aucune cellule, population, propriété ou unité transférée. Les déclarations répétées de bâtiments ne sont pas additionnées comme résultat moteur assuré.

Le chiffre contemporain voisin de 80 000 habitants pour l'acquisition de 1779 n'est pas un recensement des 179 cellules ni d'un noyau de 1776. Il ne permet pas de corriger le pool agrégé sans périmètre comparable. Les cultures et religions restent inchangées. Le modèle possède déjà une administration et des moyens dans cet agrégat; aucun nouveau bâtiment n'est ajouté pour simuler artificiellement chaque office provincial.

## Tests et travaux préservés

- **40/40 contrôles statiques réussis** : inventaire effectif mondial, géométrie, populations, bâtiments, niveaux, unités, registre, onze RGB, acquis, sources et état Git. [VALIDATION.json](VALIDATION.json). Ce PASS est celui de la conservation technique, pas celui de l'exactitude historique autrichienne.
- **Suite cumulative : 328 réussites sur 332**, trois échecs hérités de dernières couches du registre et une exclusion d'initialisation; aucun nouvel échec inexpliqué. [TESTS.json](TESTS.json), [journal brut](TESTS.log), [analyse](TEST_REVIEW.json).
- **Contrats courants : 71 réussites sur 72**, aucun échec et une exclusion initiale. [SCOPED_TESTS.json](SCOPED_TESTS.json). Aucun ancien test réécrit pour masquer les échecs.
- **44 doublons RGB et 12 références invalides hérités** inchangés. Les 23 jalons acquis restent justifiés; aucune attestation ne se propage à une autre tâche.
- SESSION_BEFORE.json capture avant toute écriture; BASELINE.json capture après la décision silésienne. Les anciens rapports et reçus récents restent identiques octet par octet.

Le chantier parallèle de construction des fortifications modifie huit fichiers de groupes/définitions, modificateurs, valeurs, déclencheurs, effets et actions génériques, puis deux fichiers de libellés FR/EN. Ces dix chemins sont consignés, conservés sans écriture et sans restauration depuis une baseline. Les contrôles interrompus sont archivés dans CONCURRENT_REVIEW_VALIDATION.json et CONCURRENT_REVIEW_2_VALIDATION.json; les revues précisent le périmètre et le contrôle final passe. Le chantier du génie, ses illustrations/traductions, les États-Unis, Minutemen, accords financiers, Saint-Gobain/Anzin et autres travaux français sont préservés. Cette conservation ne certifie pas les nouvelles mécaniques parallèles.

Un problème de destination du lanceur a initialement réécrit les seuls identifiants de tâche de deux résultats JSON de l'ancienne passe silésienne. Le callback est corrigé; **les deux fichiers historiques sont rétablis octet par octet, empreintes de capture vérifiées**, sans toucher aux fichiers du jeu ou reçus humains. [Preuve de rétablissement](EVIDENCE_OUTPUT_RECOVERY.json). Le contrôle de lecture seule a observé ce rétablissement pendant sa fenêtre de comparaison : cet échec transitoire reste dans INTERFERED_SCOPED_TESTS.json et TEST_INTERFERENCE_REVIEW.json. Une nouvelle exécution stabilisée réussit 71/72, une exclusion, sans échec. Les journaux historiques et ceux de chaque contrôle conservé restent disponibles.

HEAD, branche et index Git restent identiques. Aucun commit, push, staging, merge, reset, rebase, changement de branche ni écriture vanilla. Aucun moteur exécuté par l'agent; aucune observation humaine inventée.

## Suivi, limites et suite

RM-0010 enregistre la décision silésienne approuvée et ses trois points. RM-0011 consigne le seul nouvel audit autrichien bloqué, sans crédit. Les vues ROADMAP, NEXT_ACTION, BLOCKERS et historique sont régénérées; les 80 autres fiches et dix événements précédents sont conservés depuis la baseline.

État final distingué : **23 jalons acquis**, dont la décision silésienne sans correction; **8 installations antérieures en attente de reçu spécifique**; **SC2-AUSTRIA auditée mais bloquée**, aucune nouvelle installation à tester; aucun nouveau report P0/P1 approuvé. Teschen reste NOT_STARTED et indépendant. Les incertitudes fines et les anciens blocages restent visibles.

[Repères de contrôle joueur préparés](PLAYER_TEST_PROTOCOL.md) : conservation facultative des données actuelles, sans annoncer une correction inexistante. Un mois/sauvegarde/rechargement, s'il est effectué, ne lève pas le blocage cartographique. Un protocole décisif sera fixé avec la future correction réellement installée.

Prochaine candidate recalculée : **SC2-INNER-AUSTRIA — Styrie, Carinthie et Carniole**, P0 sans dépendance, **NOT_STARTED**. Elle n'est ni recherchée ni installée dans cette mission. SC2-AUSTRIA demeure à reprendre sur la preuve manquante; la mission s'arrête après cette seule nouvelle étape.

Contrôle final du suivi : **PASS**; tests du suivi après régénération : **27/28**, une exclusion initiale, aucun échec. Les deux résultats historiques récupérés ont toujours leurs empreintes originales. [Suivi final](FINAL_TRACKER_VALIDATION.json) · [Tests finaux](FINAL_TRACKER_TESTS.json) · [Manifeste](DELIVERY_MANIFEST.json).
