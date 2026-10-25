# SERG TERRITORIAL 1.0 — PROGRESSION : 31,91 %

Passe du 19 octobre 2026. **SC2-AUSTRIAN-SILESIA : RESEARCH_COMPLETE, audit sans modification fonctionnelle, décision de conservation proposée mais non approuvée.** Aucun reçu moteur de Silésie ni point supplémentaire.

## Validation précédente et progression

Le joueur confirme explicitement le protocole **SC2-MORAVIA entier** : nouvelle partie au 1er janvier 1776, administration ajoutée présente et fonctionnelle, éléments contrôlés sans anomalie, un mois de simulation, sauvegarde et rechargement sans crash ni bug. Le [reçu Moravie](../SC2-MORAVIA/RUNTIME_USER_ATTESTATION_2026_10_19.json) couvre seulement la passe réellement installée/testée. Aucun relevé chiffré détaillé, date effective du test, langue ou fichier de sauvegarde n'est inventé; aucune extension à Silésie/Teschen/cadastre.

Après dix contrôles de conservation réussis, le suivi confirme **72/235 = 30,64 % → 75/235 = 31,91 %**, soit 22 jalons justifiés. Le rapport et protocole d'installation moraves antérieurs restent intacts; le statut actuel est consigné dans l'attestation et ACCEPTANCE_2026_10_19.md. Le validateur est exécuté avant la nouvelle intervention et sélectionne **SC2-AUSTRIAN-SILESIA**, P0, phase 2, sans dépendance. La mission autorise une seule nouvelle étape.

Après cet audit sans nouvelle installation : **75/235 = 31,91 %**, zéro point Silésie acquis. Périmètre 1.0.0, 81 tâches, poids et dénominateur inchangés. RESEARCH_COMPLETE ne vaut pas état terminal ni report P0.

## Recherche et décision concrète

Les [sources](SOURCES.md) confrontent l'ancienne correction MAP2A, le diagnostic méridional MAP1B, les recherches Moravie, l'atlas historique silésien et la chronologie indépendante d'Opava. Une carte Seutter/Lotter cataloguée **1740–1760** a été réellement ouverte : Teschen, Bielitz, Oderberg, Friedek et interfaces moraves/silésiennes. Sa datation ne permet pas d'utiliser ses couleurs comme démarcation politique de 1776. Trois autres notices datées sont examinées et leurs limites consignées, sans prétendre avoir lu leurs images.

Les sous-lots [SIL-P/W/N/I/T/D](SECTOR_AUDIT.md) distinguent partition, interfaces de Nysa/Opava/Krnov, institutions, Teschen/registre et dépendances démographiques/économiques. L'inventaire exhaustif de **26 RGB** documente géométrie, propriétaire, cellules, voisins et registre; il inclut les régions prussiennes comme contexte, sans clore la tâche future Silésie-Lusaces. La [carte technique numérotée](NATIVE_READING.png) n'est pas un calage historique.

La partition générale déjà installée est conservée. Les offices de Brno et d'Opava sont distincts dans la documentation de 1776; la capacité régionale du moteur les agrège et ne simule pas chaque institution. Aucun nouveau pays, gouverneur, PM, niveau administratif ou changement de loi ne corrigerait une différence fonctionnelle ici démontrée. Ajouter artificiellement un second niveau ne localiserait pas l'office d'Opava et modifierait sans justification chiffrée la capacité/coût du bâtiment déjà validé.

**Corrections fonctionnelles installées dans cette passe : aucune.** Les réparations historiques existantes suffisent à la représentation politique générale B ici retenue; les micro-limites restent non homologuées. L'écart réel de Teschen au registre est expressément réservé à SC2-TESCHEN, conformément à la séparation demandée. Les limites connues du vieux calage sont conservées; aucun essai redondant, translation arbitraire ou frontière de 1815/1836 ne sert à forcer un transfert.

La [décision proposée](PROPOSED_DECISION.json) conserve l'approximation B sans correction supplémentaire, avec ses réserves. `approved_by` reste nul. Le suivi exige un accord spécifique pour qualifier un état terminal sans correction; l'autorisation générale de travailler ne fournit pas cet accord. Aucune conformité cadastrale générale n'est proclamée.

## Avant / après

| Élément | Avant | Après |
| --- | --- | --- |
| x71E080 / xF0E080, MAP2A | AUS seul, STATE_MORAVIA; 92 / 219 cellules | Identique, 311 cellules protégées |
| Moravie technique entière | 10 RGB, 2 250 cellules AUS | Identique |
| Haute/Basse Silésie techniques de contexte | 6 / 9 RGB PRU, 1 042 / 2 249 cellules | Identiques; limites fines non certifiées |
| Teschen x9061E0 | AUS seul, STATE_WEST_GALICIA, 179 cellules | Identique, dossier distinct |
| Registre impérial | 574 lignes, MAP2A inclus; Teschen absent | Identique; aucune Galicie entière ajoutée |
| Pool Opava/Krnov / Teschen | 191 139 / 135 753 | Identiques; somme 326 892, pas recensement certifié |
| Population Moravie / Bohême | 1 570 622 / 2 500 000 | Identique |
| Population mondiale écrite | 834 926 252 | Identique |
| Niveau public morave | 1 AUS, méthodes déjà validées | Identique |
| Autres bâtiments, PM, propriétés, ressources, unités et pays | Historiques installés | Identiques |
| Bitmap, noyau SLZ et 21 RGB de Bohême | Version déjà testée | Identique |

[NATIVE_INVENTORY.json](NATIVE_INVENTORY.json), [BOUNDARY_AUDIT.json](BOUNDARY_AUDIT.json), [VALIDATION.json](VALIDATION.json). Les répétitions de déclarations de bâtiments ne sont pas additionnées comme résultat moteur assuré. Les proportions culturelles et allocations anciennes ne sont pas transformées en chiffres ethniques de 1776.

## Tests et conservation

- **44/44 contrôles statiques réussis** : inventaire mondial effectif, propriétaires uniques des portions protégées, géométrie, populations, bâtiments, niveaux, unités, références, registre, acquis, preuves, état Git et sources archivées. Aucun moteur exécuté.
- Suite cumulative : **328 réussites / 332**, **3 échecs hérités** de dernières couches du registre, **1 exclusion** d'initialisation. [Journal brut](TESTS.log), [résultat](TESTS.json), [analyse](TEST_REVIEW.json). Les assertions anciennes attendent une couche antérieure; le registre réel est inchangé et son garde courant passe. Aucun nouvel échec inexpliqué.
- Contrats courants : **71 réussites / 72**, **aucun échec**, une exclusion d'initialisation. [Résultat](SCOPED_TESTS.json), [journal](SCOPED_TESTS.log). Aucun ancien test modifié pour masquer ces résultats.
- **44 doublons RGB et 12 références invalides hérités**, inchangés; aucune nouvelle anomalie dans cet inventaire. Leur classement final reste SC7-NONREGRESSION, sans les déclarer corrigés.
- Tous les anciens rapports/reçus récents sont identiques octet par octet. Les 22 jalons acquis demeurent justifiés; les huit anciennes validations spécifiques en attente ne récupèrent pas le reçu Moravie.

SESSION_BEFORE.json précède toute écriture. BASELINE.json suit l'acceptation Moravie; les différences avec cette capture sont consignées dans FILES_MODIFIED.json. Pendant la passe, le chantier concurrent du génie modifie définitions militaires, illustration et alias culturels, interface, stratégie IA et traductions; les libellés de fortifications évoluent aussi. Ces fichiers restent conservés, sans écriture ni restauration de notre part. Deux contrôles interrompus sur des chemins concurrents nouvellement apparus sont archivés dans CONCURRENT_REVIEW_VALIDATION.json et CONCURRENT_REVIEW_2_VALIDATION.json, puis expliqués dans les revues correspondantes; le contrôle final passe. Cette conservation ne valide pas le gameplay des travaux parallèles.

Les États-Unis, Minutemen, accords financiers, bâtiments militaires, Saint-Gobain/Anzin, autres travaux français et territoires validés ne sont pas réécrits. HEAD, branche et index Git restent identiques. Aucun commit, push, staging, merge, reset, rebase, changement de branche ni écriture vanilla.

## État des travaux et prochaine action

- **Validés** : 22 jalons, dont Salzbourg, Bohême et maintenant Moravie, dans leurs seuls périmètres reçus.
- **Installés mais non attestés spécifiquement** : les huit tâches de validation antérieures restent ouvertes, notamment MAP2A; ce rapport ne les clôture pas.
- **Audité sans changement** : SC2-AUSTRIAN-SILESIA, RESEARCH_COMPLETE, proposition de conservation B en attente de décision explicite. Pas de nouvelle installation à déclarer READY ni de faux PASS humain.
- **Blocages et incertitudes** : Teschen hors registre reste une correction P1 distincte; limites cadastrales de Nysa/enclaves, représentation institutionnelle fine et démographie exacte non acquises. Les neuf tâches déjà BLOCKED conservent leurs statuts.
- **Différés** : décisions P2 antérieures conservées; aucun nouveau report approuvé, aucun P0 différé.

[Protocole joueur préparé](PLAYER_TEST_PROTOCOL.md) : contrôle de la partition conservée, administration morave existante, dépendances, puis mois/sauvegarde/rechargement si effectué; retour limité aux observations réelles et revue de la proposition sans changement. Le reçu Moravie ne se propage pas à cette tâche.

RM-0008 enregistre Moravie; RM-0009 consigne l'audit silésien sans points. ROADMAP_STATE.json, ROADMAP.md, NEXT_ACTION.md, BLOCKERS.md et historique sont régénérés. Prochaine action immédiate : **revue de la décision sans correction pour SC2-AUSTRIAN-SILESIA**. Après accord spécifique et contrôle des preuves, candidate prévue : **SC2-AUSTRIA**, P0 sans dépendance, **NOT_STARTED**. Aucune deuxième étape commencée.

Validation finale du suivi : PASS; tests spécifiques du suivi après régénération : **27 réussites sur 28**, une exclusion initiale, aucun échec. Les huit événements précédents et les 80 autres fiches sont conservés depuis la baseline après reçu Moravie. [Contrôle final](FINAL_TRACKER_VALIDATION.json) · [Tests du suivi](FINAL_TRACKER_TESTS.json) · [Manifeste de livraison](DELIVERY_MANIFEST.json).
