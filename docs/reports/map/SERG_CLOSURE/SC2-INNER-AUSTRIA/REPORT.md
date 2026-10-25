# SC2-INNER-AUSTRIA — livraison du 19 octobre 2026

**SERG TERRITORIAL 1.0 — PROGRESSION : 33,19 %**

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Une seule nouvelle étape : Styrie, Carinthie et Carniole, P0, poids 4, sans dépendance. Trois sous-lots installés, sans reçu humain. **Avant : 78/235 = 33,19 %. Après : 78/235 = 33,19 %.** Les 23 jalons acquis restent justifiés; aucune nouvelle validation ni point présumé.

## Décision autrichienne conservée et sélection

La prise d'acte explicite du joueur est enregistrée séparément dans [USER_ACKNOWLEDGMENT_2026_10_19.json](../SC2-AUSTRIA/USER_ACKNOWLEDGMENT_2026_10_19.json), événement RM-0012. **SC2-AUSTRIA reste BLOCKED**. L'Innviertel est encore bavarois au 1er janvier 1776; la cession est de 1779. La conservation définitive de l'erreur potentielle n'est pas approuvée. Aucun test moteur supplémentaire demandé pour ce diagnostic sans installation; aucun PASS ni crédit. Une reprise future devra proposer une approximation politique B étayée par cartes historiques et voisins, ou un arbitrage explicite. Aucun ancien recalage n'a été relancé.

Après lecture des cinq fichiers canoniques et des anciennes attestations, le validateur initial confirme PASS, 78/235, prochain P0 **SC2-INNER-AUSTRIA**. Le Tyrol attend Trente/Brixen; le blocage local autrichien n'interrompt pas ce dossier indépendant. SESSION_BEFORE.json capture avant nos écritures, BASELINE.json après la prise d'acte sans changement fonctionnel.

## Recherche appliquée

Trois cartes primaires Seutter de Styrie, Carinthie et Carniole, datées dans leurs notices individuelles **entre 1740 et 1760**, ont été examinées. Les archives de Graz, la documentation des fonds de Carniole et les serments de 1763, la notice ÖStA du 14 septembre 1763 et l'histoire du bâtiment administratif de Klagenfurt documentent les offices antérieurs à 1776. Les réformes de 1782/83 ne sont pas rétroprojetées. [Sources, liens et limites](SOURCES.md), [audit territorial](SECTOR_AUDIT.md).

La Styrie comprend sa partie méridionale autour de Marburg/Pettau/Cilli. La Carinthie est un duché distinct, avec centre à Klagenfurt. La Carniole comprend ses subdivisions historiques; elle n'est pas une Slovénie nationale contemporaine. Les trois pays relèvent de Marie-Thérèse, dans le périmètre impérial, mais leurs limites internes ne coïncident pas avec les deux régions économiques du moteur. STATE_STYRIA agrège notamment Graz et la Carinthie; STATE_SLOVENIA regroupe Ljubljana et des lieux de Basse-Styrie. Cette conservation est de catégorie B, pas une homologation cadastrale.

Les possessions carinthiennes de Bamberg figurées sur l'ancienne carte sont vendues à l'État autrichien en 1759 : aucun BMB territorial recréé. Propriété et droits locaux de Salzbourg, Freising ou d'un diocèse ne démontrent pas à eux seuls une souveraineté immédiate nouvelle; le récessus de 1535 et les sources patrimoniales sont distingués. Aucun territoire des noyaux validés n'est déplacé.

L'interface impériale est contrôlée dans les données : les voisins hongrois x124D73/x30A020/xA709B7 restent HUN, les voisins croates x458E4C/x71A041/xF021C0 restent AUS, tous hors registre. Les douze RGB de la passe restent impériaux avec bénéficiaire AUS. Les territoires vénitiens restent vénitiens. Trieste, Gorizia/Gradisca et l'Istrie servent ici au bornage; leur examen propre appartient à SC2-ANTERIOR-AUSTRIA, non commencée comme nouvelle étape.

## Corrections installées et sous-lots

- **IA-I-ST** : un niveau d'administration gouvernementale public AUS ajouté dans STATE_STYRIA, fichier nouveau common/history/buildings/1776_sc2_inner_austria_styria.txt. Capacité régionale minimale autour de Graz et de l'agrégat carinthien; aucun second office placé artificiellement à Klagenfurt.
- **IA-I-C** : un niveau public AUS ajouté dans STATE_SLOVENIA, fichier nouveau common/history/buildings/1776_sc2_inner_austria_carniola.txt, pour la capacité provinciale de Carniole dans l'agrégat de Ljubljana. Ce niveau n'est pas nommé gubernium de Ljubljana de 1783.
- **IA-E-C** : retrait du seul port et du seul chantier naval déclarés dans l'agrégat intérieur de Ljubljana, dans chacun des fichiers common/history/buildings/01_south_europe.txt et 98_build_start_1776_world_redistribution.txt. **Quatre blocs retirés**. Les définitions effectives exigent une côte; l'agrégat n'a ni locator de port, ni sortie navale, ni voisin maritime. Routes et commerce demeurent. Aucun bâtiment côtier voisin déplacé ni compensation installée.

Les quatre PM administratifs sont existants et compatibles avec les lois/technologies AUS : organisation simple, bureaucrates héréditaires, administration religieuse, absence de rapports organisés de recherche. Les deux derniers libellés d'organisation du personnel restent des abstractions nationales du moteur; ils ne décrivent pas littéralement le recrutement des offices. Aucun changement de loi nationale pour imposer un PM professionnel incompatible.

Pour IA-E-C, les six niveaux de port et deux niveaux de chantier retirés sont des **niveaux écrits dans des déclarations répétées**, pas des niveaux moteur cumulés certifiés. MARITIME_BEFORE conserve les deux fichiers courants avant correction; MARITIME_CLEANUP.json et les candidats prouvent que les autres octets restent identiques. Aucune restauration depuis une ancienne baseline. Le premier contrôle administratif est archivé sous BEFORE_MARITIME_*; les résultats ci-dessous portent sur la version finale corrigée.

## Avant / après

| Élément | Avant | Après |
| --- | --- | --- |
| STATE_STYRIA, 54 | 8 RGB, 2002 cellules, AUS | Identique |
| STATE_SLOVENIA, 114 | 4 RGB, 1128 cellules, AUS | Identique |
| Administrations dans ces régions | 0 / 0 | 1 / 1, publiques AUS |
| Déclarations port/chantier dans Ljubljana | 2 ports et 2 chantiers, base/overlay | 0 |
| Population des deux agrégats | 599143 + 395031 = 994174 | Identique |
| Population mondiale | 834926252 | Identique |
| Conscrits de ces régions | 2 + 1 | Identique |
| Registre impérial | 574 entrées, dernière couche Salzbourg | Identique |

| RGB | Région technique conservée | Cellules avant = après | Propriétaire |
| --- | --- | --- | --- |
| x017E3C | STATE_STYRIA | 209 | AUS → AUS |
| x1101A0 | STATE_STYRIA | 189 | AUS → AUS |
| x155A44 | STATE_STYRIA | 133 | AUS → AUS |
| x31E041 | STATE_SLOVENIA | 447 | AUS → AUS |
| x44F127 | STATE_SLOVENIA | 337 | AUS → AUS |
| x59D927 | STATE_STYRIA | 186 | AUS → AUS |
| x792B8A | STATE_SLOVENIA | 193 | AUS → AUS |
| x86FD73 | STATE_STYRIA | 312 | AUS → AUS |
| x8F8020 | STATE_STYRIA | 230 | AUS → AUS |
| xB06141 | STATE_STYRIA | 228 | AUS → AUS |
| xB0E040 | STATE_SLOVENIA | 151 | AUS → AUS |
| xB4D292 | STATE_STYRIA | 515 | AUS → AUS |

Aucune capitale, souveraine, gouvernement, loi, culture, religion, profession, population, formation ou unité modifiée. Le montant de 509420 donné pour 1770 par la série officielle de Styrie n'est pas au périmètre démontré des huit RGB, lesquels incluent la Carinthie. Aucun faux recensement des trois duchés n'est installé. Les limites internes et les effectifs historiques restent des incertitudes explicites; le test moteur ne les certifiera pas.

## Contrôles réellement exécutés

- **96/96 contrôles statiques réussis**, [VALIDATION.json](VALIDATION.json) : inventaire mondial, seuls deltas de bâtiments permis, autres octets, absence d'accès côtier, PM disponibles, géométrie et propriété, voisins impériaux/extérieurs, populations, unités, reçus, anciens rapports, sources, outils et état Git.
- **349/353 réussites cumulatives**, trois échecs hérités et une exclusion. Les trois anciens tests attendent une ancienne dernière couche du registre; la chaîne cumulative courante, terminant à Salzbourg, passe. Aucun test ancien réécrit ni résultat caché. [Résultats](TESTS.json), [journal brut](TESTS.log), [analyse](TEST_REVIEW.json).
- **92/93 contrats courants réussis**, aucun échec, une exclusion initiale; contrats négatifs sur niveaux, PM, propriétaire, région, ajout d'effets, débordement de correction maritime et faux reçus. [SCOPED_TESTS.json](SCOPED_TESTS.json).
- **44 doublons RGB et 12 références invalides hérités inchangés**. Les incohérences historiques de l'Innviertel ne sont pas masquées par ces PASS techniques.
- Contrôle ciblé des différences sans erreur d'espacement. Les deux nouveaux fichiers et les deux corrections ciblées constituent tout le changement fonctionnel de cette mission. [Périmètre des écritures](FILES_MODIFIED.json), [comparaisons](DIFF_CHECK.json).

Les noyaux Salzbourg/Passau/Freising/Ratisbonne, Bohême/Moravie, Silésie/MAP2A et les autres acquis conservent leurs données et preuves. Le bâtiment morave testé reste identique. Les modifications fortifications/Corps du génie, États-Unis/Minutemen/accords, Saint-Gobain/Anzin et France étaient déjà présentes dans la capture et restent préservées. Aucune différence concurrente supplémentaire observée pendant cette passe; aucune remise à zéro de leurs fichiers. Cette conservation n'est pas une validation des fonctionnalités parallèles.

HEAD, branche et index Git identiques. **Aucune opération Git d'écriture ni modification vanilla.** Aucun moteur lancé par l'agent et aucun reçu humain pour ces nouvelles corrections.

## Suivi et suite

RM-0012 conserve la décision explicite de blocage autrichien; RM-0013 enregistre cette seule nouvelle installation. Les 80 autres fiches et les 12 événements antérieurs sont conservés après la prise d'acte. Périmètre 1.0.0 et dénominateur 235 inchangés. Les vues ROADMAP, BLOCKERS, NEXT_ACTION, historique et instantané sont régénérées et contrôlées.

**Prochaine action : [protocole joueur des trois sous-lots](PLAYER_TEST_PROTOCOL.md)**, nouvelle partie 1776, administrations et retrait maritime intérieur, conservations, un mois complet, sauvegarde/rechargement. Statut IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION; zéro point nouveau. Un résultat humain sera enregistré uniquement après votre confirmation, dans le périmètre réellement confirmé.

**Prochaine candidate territoriale : SC2-ANTERIOR-AUSTRIA**, P0 indépendant, restée NOT_STARTED. Aucun lancement automatique d'une deuxième étape. SC2-AUSTRIA demeure BLOCKED; Teschen et Tyrol restent distincts. La précision cadastrale, les effectifs historiques comparables et les périphéries ne sont pas certifiés par cette livraison administrative.

Contrôle final après régénération : suivi **PASS**, tests du suivi et contrats Inner Austria **48/49**, une exclusion initiale, aucun échec. Comparaison finale : les quatre seuls chemins fonctionnels autorisés diffèrent, les anciennes preuves et l’index Git restent identiques. [Tests finaux](FINAL_TRACKER_TESTS.json) · [Suivi final](FINAL_TRACKER_VALIDATION.json) · [Manifeste de livraison](DELIVERY_MANIFEST.json).
