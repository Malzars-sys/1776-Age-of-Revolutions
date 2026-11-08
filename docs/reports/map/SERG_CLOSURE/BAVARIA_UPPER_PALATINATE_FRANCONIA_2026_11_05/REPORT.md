# SERG TERRITORIAL 1.0 — PROGRESSION : 45,11 %

**Trois noyaux BAV→KPF installés : 156 cellules. Les tests moteur sont regroupés à la fin de la Bavière, selon la dernière instruction du joueur.**

## Résultat installé

| Sous-lot | Périmètre exact | Cellules |
| --- | --- | ---: |
| BV-SULZBACH | Possessions nord-orientales du duché, autour du complexe Parkstein-Weiden/Floß/Vohenstrauß ; pas la ville de Sulzbach entière | 27 |
| BV-NEUBURG-DONAU | Noyau Neubourg/Graisbach–Monheim sur le Danube | 35 |
| BV-BURGLENGENFELD | Noyau Burglengenfeld–Hemau, raccords Kallmünz/Laaber/Regenstauf | 94 |

Approximation politique B documentée par juridictions, pas cadastre. KPF représente déjà Charles-Théodore ; aucun pays, électeur ou union bavaroise1777 anticipée. Amberg et Leuchtenberg ne sont pas attribuées intégralement au Palatinat. [Sources et limites](SOURCES.md), [tracé retenu](TRACING_REVIEWED.json), [avant/après installé](BEFORE_AFTER.png).

Six provinces parentes sont subdivisées en18 composantes connexes, avec12 nouveaux RGB. Le bitmap change sur176 cellules :156 changent de propriétaire et20 ne changent que d'identité technique BAV. Les régions économiques, leurs ID, ressources, capacités agraires, terrains hérités, hubs et positions physiques sont conservés. Aucun nouvel État régional ; seule une portion KPF est créée dans STATE_BAVARIA.

**55115 habitants courants sont transférés** de BAV à KPF, avec conservation exacte des effectifs mondiaux et profils culturels/religieux. Valeur technique provisoire issue de la portion donneuse, pas estimation historique1776 ni reprise du totalSulzbach1802. La démographie historique reste ouverte. Tous les bâtiments, PM, détenteurs, unités, recrutements et profils technologiques restent inchangés.

**599→611 titres impériaux**, même emprise géographique, mêmes membres et neuf électeurs. Les599 anciennes lignes du registre restent identiques ;12 titres techniques subdivisés sont ajoutés. Sept dérivés impériaux préparés sans conflit concurrent. Quatorze fichiers installés, dont le bitmap, le registre actif et son outil de chaînage. [Manifestes](INSTALLATION.json), [plan](PLAN.json).

## Conservation et contrôles

**48/48 contrôles de conservation réussis sur la version installée** : delta territorial exact, RGB connexes et uniques, frontières régionales/ressources/hubs, populations, bâtiments/PM/propriété/unités/pays, droits impériaux, archives et index Git. [Résultats](VALIDATION.json), commande : python -B -X utf8 puis validate_delivery.py dans ce dossier.

Innbaiern175, Obernberg4 et les anciens noyaux PAS40/SLZ12 restent installés et inchangés. EIC/ANS/NUR/FBM/WZB, Freising, Ratisbonne, la Prusse et les autres territoires non BAV sont conservés cellule par cellule. Les11 erreurs de références et14 doublons hérités restent identiques. Aucun moteur lancé ni reçu humain créé.

**82 tests ciblés exécutés : 81 réussis, une exclusion documentée, aucun échec ni erreur.** Le contrôle exclu exige le snapshot sans modification de l’initialisation ancienne ; sa source est conservée, la conservation actuelle est vérifiée par différence. **24/24 contrôles finaux réussis**, validateur canonique PASS. La recompilation documentaire inspecte73 sorties : les7 dérivés de cette passe correspondent exactement ; deux divergences préexistantes des actions diplomatiques d’autonomie37/38 restent préservées, sans restauration. Les différences de la passe sont propres ; deux espaces terminaux hérités du fichier de formations africaines restent inchangés. [Tests](TEST_RESULTS.json), [contrôles finaux](FINAL_CHECKS.json), [compilateur](COMPILER_FINAL_CHECK.json), [différences](DIFF_CHECK.json). Aucun résultat ancien n’est présenté comme une nouvelle exécution.

## Raccords réservés et suite

Hilpoltstein–Heideck–Allersberg et le noyau occidental de Sulzbach ont été inspectés : leurs enveloppes projetées rencontrent des noyaux déjà reçus. Aucun transfert de ces noyaux n'est forcé depuis une hypothèse cartographique ; ce résultat ne certifie pas leur frontière actuelle et ne démontre pas une régression. Les candidats préparatoires, y compris un contrôle de ville rejeté, restent archivés. Ils ne décrivent pas une installation antérieure.

Schwandorf, Reichertshofen, les prolongements occidentaux du Danube dont Höchstädt/Lauingen et les autres franges non retenues restent à traiter ou à arbitrer. Il n'est pas affirmé que la Bavière entière soit finie.

SC6-SWABIAN-ARBITRATIONS : NOT_STARTED→IN_PROGRESS, trois sous-lots IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION. SC2-AUSTRIA et son Innbaiern restent IN_PROGRESS/en attente ; aucune ancienne attestation modifiée. **106/235→106/235,45,11%→45,11%,36/81**, périmètre1.0.0 et81 tâches conservés. Événement additif SERG-RM-0077.

[Protocole moteur groupé](PLAYER_TEST_PROTOCOL_GROUPED.md) préparé pour la fin de la Bavière, avec Innbaiern et ces trois noyaux. Aucun test immédiat exigé. Prochaine candidate : revue des grands contours bavarois restants et arbitrages des raccords précités ; non commencée automatiquement. Aucun Git d'écriture ni vanilla modifié.
