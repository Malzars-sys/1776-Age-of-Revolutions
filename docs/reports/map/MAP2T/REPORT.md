# MAP-2T — Noyaux saxons et thuringiens installés

Date : 17 octobre 2026. Situation historique visée : 1er janvier 1776.

**MAP2T_PARTIAL_INSTALLED_READY_FOR_SCOPED_RUNTIME_TEST**. Ce sous-lot est prêt pour un test ciblé, pas pour une certification de toute la Thuringe. Lobenstein, Ebersdorf, les possessions septentrionales et plusieurs enclaves ne sont pas terminés. Aucune validation moteur de MAP-2T n’est revendiquée.

## Modifications réelles

| Nouveau pays | TAG | Cellules du noyau | Population technique |
|---|---|---:|---:|
| Saxe-Gotha-Altenbourg | GOT | 61 | 45931 |
| Saxe-Hildburghausen | HIL | 19 | 6279 |
| Schwarzbourg-Sondershausen | SSO | 12 | 6734 |
| Comté de Reuss-Greiz | RGZ | 8 | 8420 |
| Comté de Reuss-Gera | RGE | 12 | 8229 |
| Comté de Reuss-Schleiz | RSL | 9 | 8369 |

121 cellules changent de propriétaire dans STATE_SAXONY, ID numérique73. Seize RGB nouveaux, xEDB400 à xEDB40F, portent les subdivisions nécessaires, y compris des fragments techniques conservant leur ancien propriétaire. Le registre passe de521 à537 RGB, sans changer l’étendue physique impériale.

| Avant | Après | Cellules transférées |
|---|---|---:|
| COB | GOT | 27 |
| COB | HIL | 4 |
| COB | SSO | 10 |
| MEI | GOT | 1 |
| MEI | HIL | 15 |
| MEI | SSO | 2 |
| SAX | GOT | 17 |
| SAX | RGZ | 8 |
| SAX | RSL | 6 |
| WEI | GOT | 16 |
| WEI | RGE | 12 |
| WEI | RSL | 3 |

Les souverainetés sont distinguées à partir des sources institutionnelles et des trajectoires dynastiques; les contours installés sont des noyaux généralisés B lus sur la reconstruction1789 de Putzger, et non des frontières1776 directement certifiées. Voir [preuves et limites](HISTORICAL_EVIDENCE.md). Les portions non attribuées restent chez leur propriétaire technique antérieur, ce qui n’en fait pas une attribution historique validée.

Gotha–Altenbourg est distinct de Cobourg–Saalfeld. Hildburghausen n’est pas fusionné avec Meiningen. SCW est désormais explicitement Schwarzbourg-Rudolstadt, tandis que SSO représente un noyau méridional de Schwarzbourg-Sondershausen. Greiz, Gera et Schleiz ont trois pays distincts et restent des comtés en1776, sans importer les regroupements ultérieurs. Les noms français/anglais et descriptions de gouvernement sont définis, ainsi que les souverains contemporains. Les modèles législatifs/technologiques des six nouveaux pays sont repris de COB: abstraction de gameplay, pas six audits législatifs historiques.

Les rangs anachroniques de SAX et WEI sont abaissés à principauté au sens technique du jeu. SAX conserve sa dignité et son titre de prince-électeur; WEI reste ducal. Aucun nouvel électeur, aucune nouvelle ville libre, aucune union personnelle ni sujétion impériale native n’est ajouté. Les nouvelles nations rejoignent le bloc et les droits de restitution existants comme membres ordinaires. Les mécanismes HRE-CENTRALIZATION, les deux icônes et les prototypes sont préservés.

## Géométrie et exclusions

Le profil diagnostique natif conservé est réutilisé sans optimisation ni translation7,20px. Le calage effectué concerne uniquement la nouvelle feuille historique. Ses résidus d’ajustement ne prouvent pas l’exactitude géographique du bitmap. Aucune borne indépendante de précision locale n’est revendiquée.

Un rectangle de protection X4342–4358/Y822–836 couvre les hypothèses anciennes et rejetées d’Erfurt avec marge. Tous ses RGB restent identiques. Eichsfeld et tous les pixels hors STATE_SAXONY sont inchangés. Aucun corridor artificiel n’est ajouté entre noyaux détachés. Les RGB franconiens de COB, les quatre Anhalt, Jever, Emden, Eutin, la Peene, la Belgique et la Souabe sont protégés par la comparaison mondiale exacte.

La [carte avant/après](SAXONY_THURINGIA_BEFORE_AFTER.png) représente le découpage réellement installé. Rouge: zone exclue d’Erfurt. La carte du journal est régénérée; le masque physique du mode carte reste identique car l’étendue impériale ne change pas. Les locators ne sont pas déplacés; seuls les RGB de référence nécessaires et les listes prime_land suivent les subdivisions.

## Démographie, économie et armée

Population mondiale directement mesurée avant/après: **835801255**, delta0. Ce total n’est pas imposé comme règle historique; il résulte de la redistribution technique conservatrice retenue ici. Aucun dénombrement proche de1776 avec le périmètre exact des noyaux n’a été établi. Les nombres du tableau ne sont pas des populations historiques certifiées.

Tous les profils culture/religion, bâtiments écrits, niveaux, PM, propriétaires économiques, infrastructures, unités et recrutements sont conservés. Aucun bâtiment ni soldat n’est créé pour les nouveaux pays. Ressources et capacité agraire de la région73 inchangées. Les effets moteur sur la subsistance, les marchés et la viabilité des petits pays restent à tester; leur partage d’une même région économique ne certifie pas les positions de leurs centres historiques. Le noyau SSO n’inclut pas la ville physique de Sondershausen.

## Vérifications

841/841 contrôles statiques passent. Les17 tests ciblés et60 tests de contrats cumulés passent. Les73 sorties impériales ont été vérifiées avant modification puis après installation. Les44 doublons RGB et12 références invalides hérités sont inchangés.

Les49 tests d’anciennes photographies donnent42 succès et7 échecs, détaillés dans [LEGACY_TEST_TRIAGE.md](LEGACY_TEST_TRIAGE.md). Ces échecs ne sont pas masqués: plusieurs attendent le monde exact d’un ancien lot. Deux assertions Anhalt deviennent obsolètes avec MAP-2T; la préservation effective des cellules Anhalt est vérifiée indépendamment. Les autres comparaisons figées ou l’ancienne attente de Wolgast ne sont pas des nouveaux transferts MAP-2T. Aucune ancienne baseline n’est réécrite.

Le détail complet est dans [VALIDATION.json](VALIDATION.json) et [UNIT_TESTS.json](UNIT_TESTS.json). Le [plan de test](RUNTIME_TEST_PLAN.md) ne concerne que les modifications nouvelles. Les anciens PASS_RUNTIME_USER_VALIDATED restent des attestations manuelles limitées aux inspections précédentes.

## Fichiers

Les fichiers runtime modifiés sont énumérés exactement dans VALIDATION.json, champ runtime_files_modified. Ils comprennent les historiques de propriétaires et populations, définitions de six pays, correction de deux rangs, souverains et gouvernements, noms français/anglais, drapeaux abstraits, RGB/terrains, registre, carte du journal et17 sorties impériales adaptées. Aucun fichier de bâtiments, formations, diplomatie native ou types de sujets n’est changé.

Outils: tools/map2t_saxony.py, tools/test_map2t_saxony.py, tools/map2t_tables.mjs; extension explicitement limitée de tools/map2l_registry.py. HEAD et l’index Git sont inchangés. Aucun commit, merge, reset, push ou fichier de l’installation du jeu modifié.

## ColGrep

La tentative de localisation exploratoire de l’étape précédente n’a livré aucune sortie exploitable avant interruption. L’exécution réelle du modèle2B n’est donc pas certifiée pour cette tentative. Aucun nouvel appel redondant n’a été lancé lorsque les chemins étaient connus. Vérifications exactes effectuées par lecture et rg. Compteurs de tokens Codex et temps d’inférence local non disponibles: aucune économie chiffrée revendiquée.
