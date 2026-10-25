# SC2-MORAVIA — livraison du 19 octobre 2026

**SERG TERRITORIAL 1.0 — PROGRESSION : 30,64 %**

Phase 2, priorité P0, poids 3, **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Livraison `READY_FOR_SCOPED_RUNTIME_VALIDATION`; aucune validation humaine de la Moravie créée.

## Progression et validation effectivement reçue

Début de demande : **66/235 = 28,09 %**, 20 jalons acquis. La rectification directe du joueur confirme un mois de simulation, le rechargement sans crash ni bug et la réussite globale des vérifications pour SC2-BOHEMIA. Elle remplace la mention de lancement seul de la pièce jointe. Après contrôle de conservation, reçu borné enregistré : **72/235 = 30,64 %**, 21 jalons justifiés. Aucun relevé démographique, économique, langue, date de test ou nom de sauvegarde inventé. [Attestation bohémienne](../SC2-BOHEMIA/RUNTIME_USER_ATTESTATION_2026_10_19.json).

SC2-MORAVIA est sélectionnée par le validateur, P0 sans dépendance, avant les autres tâches de phase 2 et les P1 alpines. Le document joint autorise **une seule nouvelle étape**. Après livraison Moravie non testée : **72/235 = 30,64 %**, zéro point supplémentaire. Dénominateur, barème et périmètre 1.0.0 inchangés.

## Travaux historiques et décisions concrètes

Audit [MOR-W/E/N/I/D](SECTOR_AUDIT.md) : interfaces Jihlava/Znojmo avec Bohême/Autriche, vallée morave/Hradiště face à Hongrie, interface silésienne protégée, gouvernement provincial à Brno, populations/économie/unités. Quatre cartes Müller/Homann **1720–1730** ont été lues, confrontées à la chronologie institutionnelle 1735/1763/1783. Elles ne sont ni datées abusivement de 1776 ni appliquées comme cadastre contemporain. [Sources, limites et échecs de consultation](SOURCES.md).

Une omission est attestée : le gubernium morave existe à Brno depuis 1763/64, avec activité documentée avant 1776; aucun bâtiment administratif n'est déclaré dans la région effective. La seule installation est **un niveau d'administration public AUS**, sous-lot MOR-I. Le niveau est une approximation B minimale, pas un comptage du personnel historique.

Fichier fonctionnel nouveau : `common/history/buildings/1776_sc2_moravia.txt`. Méthodes existantes : organisation simple, bureaucrates héréditaires, administration religieuse, rapports organisés de recherche désactivés. Le PM professionnel est incompatible avec la loi AUS actuelle des états provinciaux; aucune réforme nationale ajoutée pour l'imposer. L'office historique n'est pas qualifié d'héréditaire : la traduction reprend l'abstraction nationale du moteur. Aucun nouveau souverain, loi, régime, TAG ou texte de journal.

## Avant / après et conservation

| Élément | Avant | Après |
| --- | --- | --- |
| Géographie technique STATE_MORAVIA, id 53 | 10 RGB, 2 250 cellules, AUS | Identique |
| Noyau de travail hors réparations | 8 RGB, 1 939 cellules, AUS | Identique |
| x71E080 / xF0E080 protégés MAP2A | 92 / 219 cellules, AUS | Identique |
| Population région technique | 1 570 622 | Identique |
| Pool morave hérité / pool Opava-Krnov | 1 379 483 / 191 139 | Identiques, 19 groupes conservés |
| Teschen technique WEST_GALICIA | Pool 135 753 et territoire antérieurs | Identiques, hors installation |
| Administration publique en Moravie | 0 niveau déclaré | **1 niveau AUS** |
| Manufacture et réseau routier | Déclarations, PM, réserves, propriétaires hérités | Identiques |
| Recrutement morave | 5 unités de conscrits | Identique |
| Registre impérial | 574 entrées, neuf électeurs | Identique |
| Population mondiale écrite | 834 926 252 | Identique |

[Inventaire avant](NATIVE_INVENTORY.json), [carte technique numérotée](NATIVE_INVENTORY.png), [RGB/propriétaires avant-après exhaustifs](BOUNDARY_AUDIT.json), [population et comparabilité](DEMOGRAPHY.json), [installation](IMPLEMENTATION.json).

La région technique inclut des districts silésiens : la capacité fiscale agrégée du bâtiment n'est pas une fusion juridique Moravie-Silésie avant 1783. Les deux réparations ne sont ni déplacées ni reconstruites. Les tâches SC2-AUSTRIAN-SILESIA, SC2-TESCHEN et SC2-MAP2A-VALIDATION restent distinctes. La manufacture existante est historiquement défendable; ses niveaux ne sont pas gonflés à partir de chiffres postérieurs. Les deux déclarations routières base/superposition ne sont pas additionnées comme résultat moteur assuré.

Les 21 jalons acquis, dont Bohême et Salzbourg, leurs reçus, populations et géométries restent conservés. Les fichiers fonctionnels préexistants sont identiques à l'instantané d'installation, sous réserve des modifications de fortifications concurrentes observées et documentées : quatre fichiers de conditions de bataille, déclencheurs et localisations FR/EN, ainsi que deux outils du même chantier, préservés sans écriture de notre part. L'instantané initial est immuable; INSTALL_BASELINE.json consigne les trois premières divergences avant installation. Le déclencheur parallèle apparu ensuite est documenté dans CONCURRENT_REVIEW.json, avec le contrôle interrompu conservé dans VALIDATION_CONCURRENT_REVIEW.json. Aucun changement concurrent n'est restauré ou attribué à cette passe.

## Contrôles et limites

- **51/51 contrôles statiques réussis** : nouveau bâtiment/propriété/niveau/PM, lois et technologies compatibles, géométrie, souveraineté, groupes démographiques, fichiers préexistants, registre et couches approuvées, acquis, preuves et état Git. [VALIDATION.json](VALIDATION.json).
- Suite cumulative : **328 réussites sur 332**, **3 échecs hérités** d'anciennes assertions de dernière couche du registre, **1 exclusion d'initialisation**, aucun nouvel échec inexpliqué. Anciens tests conservés et journal brut livré. [TESTS.json](TESTS.json), [TESTS.log](TESTS.log), [analyse](TEST_REVIEW.json).
- Contrats courants : **71 réussites sur 72**, aucune erreur, une exclusion. Les tests négatifs refusent niveaux supplémentaires, autre région/pays/propriétaire, PM incompatible, données de recherche ajoutées, population ou autre bâtiment et extension des reçus voisins. [SCOPED_TESTS.json](SCOPED_TESTS.json).
- **44 doublons RGB et 12 références invalides hérités** inchangés, aucun nouveau dans l'inventaire. Ces dettes ne sont pas résolues par la présence d'un bâtiment administratif.
- Aucun moteur exécuté par l'agent; aucune nouvelle attestation Moravie. Aucun commit, staging, push, merge, reset, rebase ou changement de branche, ni vanilla modifié; HEAD/branche/index vérifiés.

Les micro-frontières et enclaves locales restent non certifiées; pas de nouvelle série de population exacte au périmètre des huit RGB, proportions culturelles/sociales héritées. La comparaison historique publiée donne un agrégat Moravie + reste de la Silésie; sa proximité avec le total technique ne suffit pas à prouver l'équivalence des périmètres. Aucun recalage arbitraire ou rééquilibrage démographique pour produire un changement.

Le nouveau niveau change emplois, coût public et capacité administrative. Leur comportement réel et la persistance du bâtiment attendent le joueur. [Protocole ciblé](PLAYER_TEST_PROTOCOL.md) : nouvelle partie 1776 sous Autriche, contrôle du niveau public et PM, contours/populations/dépendances conservés, un mois, sauvegarde/rechargement.

## Suivi et prochaine action

RM-0006 reçoit la validation globale de Bohême; RM-0007 livre Moravie sans points acquis. ROADMAP_STATE.json, ROADMAP.md, NEXT_ACTION.md, BLOCKERS.md et historique régénérés. Les autres 80 fiches et les événements antérieurs à cette installation sont conservés tels qu'après l'acceptation bohémienne. [Validation du suivi](TRACKER_VALIDATION.json), [conservation](TRACKER_PRESERVATION.json), [manifeste](DELIVERY_MANIFEST.json).

Prochaine action : **test joueur SC2-MORAVIA**. Candidate suivante d'implémentation : **SC2-AUSTRIAN-SILESIA**, P0 sans dépendance actuelle, **NOT_STARTED**. Aucune recherche propre ou installation de cette tâche n'est commencée; seules ses interfaces nécessaires à la protection de MAP2A sont consultées ici. Arrêt de cette mission après la seule étape morave; sélection à revérifier lors de la prochaine mission autorisée.
