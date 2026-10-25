# Sources examinées — SC2-AUSTRIAN-SILESIA

Date cible : **1er janvier 1776**. Consultation : 19 octobre 2026. SOURCE_FILES.json donne les empreintes des copies effectivement obtenues. Les références anciennes sont réutilisées sans modifier leurs fichiers.

## S1 — Partition et limites locales

[Grand atlas historique de la Silésie tchèque](https://mapa.atlas-slezska.cz/en.html), ACCENDO, musée silésien et université d'Ostrava, 2021, chapitres 1.3 et 1.5. La partition de 1742, ratifiée dans sa démarcation en 1743, laisse aux Habsbourg Teschen, des parties d'Opava/Krnov et de Nysa, ainsi que des enclaves moraves. La majorité silésienne et Glatz passent à la Prusse. L'Opava et l'Opavice guident une partie de la limite; Nysa exige aussi des limites de domaines. Un titre ducal ne prouve donc pas la possession du duché entier. L'office royal est propre à Opava en 1776; l'union administrative avec Brno est ultérieure. Le résumé anglais contient « 1783-1783 »; le corps précise 1782-1783. Aucun village n'est assimilé à un RGB entier sur cette seule lecture.

## S2 — Vérification institutionnelle indépendante

[Chronologie de la ville d'Opava](https://www.opava-city.cz/cz/mesto-urad/o-meste/aktuality/vyznamne-udalosti.html), lignes historiques 1742 et 1782–1849 : partition Prusse/Autriche, rôle frontalier de l'Opava, capitale de la Silésie autrichienne, office royal et convention des états; rattachement administratif à Brno seulement à partir de 1782. Cela corrobore la distinction de 1776. La chronologie municipale résume des transitions : les dates détaillées de l'office sont prises dans S1. Copie OPAVA_CHRONOLOGY.html.

## S3 — Carte ancienne réellement lue, sans calage forcé

[Seutter/Lotter, Nova et accurata geographica delineatio ducatus Teschenensis](https://doi.org/10.3931/e-rara-122057), UB Bern, Ryhiner **4408:43**, datation du catalogue **1740–1760**, environ 1:160 000. Notice individuelle 29505967_MANIFEST.json, image SEUTTER_TESCHEN_1740_1760.jpg, vue SEUTTER_READING.png.

Lecture : Teschen au centre, Bielitz à l'est, Friedek au sud-ouest, Oderberg au nord-ouest, Moravie sur la marge occidentale et principautés d'Opava/Krnov au-delà. Les cours d'eau et domaines montrent la complexité des interfaces. Cette datation encadre 1742 : les couleurs ne sont pas utilisées comme preuve de la démarcation de 1743 ni comme état politique précis de 1776. Aucun géoréférencement ni nouveau transfert n'en est déduit. La consultation de l'interface Teschen ne commence pas son installation distincte.

Trois autres notices ont seulement été examinées : Reilly, Ryh 4408:41, **1789–1806**, écartée pour établir 1776; Lotter, 4408:44, **après 1758**, sans terminus supérieur permettant d'affirmer 1776; Wieland/Homann, 4408:45, **1736**, antérieure à la partition. Leurs images n'ont pas été prétendues lues. Les dates de mise en ligne de 2023 ne sont pas des dates historiques.

## S4 — Anciennes preuves et limites conservées

- [MAP2A, bilan installé](../../MAP2A/MAP2A_EXECUTIVE_SUMMARY.md) : fin des deux doubles propriétaires, rattachement physique et pools déplacés sans perte; c'est une preuve d'implémentation, pas une source historique indépendante.
- [Diagnostic MAP1B Silésie](../../MAP1B/MAP1B_GEOGRAPHIC_EVIDENCE/SILESIA_READING.md) : partition confirmée en 1763, mais contrôle méridional Lotter 1758 insuffisant; erreurs de contrôle **Glogau 6,632**, **Görlitz 9,429**, **Olomouc 27,864** pixels. Ces résultats restent visibles; aucune répétition du même calage ni translation arbitraire.
- [Sources de Moravie](../SC2-MORAVIA/SOURCES.md) : gubernium de Brno, découpage technique composite, limites démographiques et méthodes compatibles. La proximité d'un total publié Moravie + Silésie en 1770 avec une population technique n'en démontre pas l'équivalence. Les pools silésiens existants ne deviennent pas un recensement de 1776.
- [Écart impérial connu](../../SERG_GLOBAL_CLOSURE_AUDIT/SUPPLEMENTAL_CHECKS.json) : x9061E0, 179 cellules AUS, hors registre. Ce défaut reste affecté à SC2-TESCHEN/SC7-REGISTRY; ne pas inscrire toute WEST_GALICIA.

## Appartenance impériale et portée de la preuve

Souveraineté AUS/PRU et appartenance impériale sont deux questions distinctes. Le contrôle du registre existant retrouve les deux RGB MAP2A sous AUS et les quinze RGB des régions silésiennes natives sous PRU; aucune règle « tous les territoires d'un TAG sont impériaux » n'est introduite. Le périmètre impérial des possessions retenues est celui documenté par les audits antérieurs, sans nouvelle homologation des micro-limites.

Le [catalogue IEG, carte 720, Allemagne au 1er janvier 1792](https://www.ieg-maps.uni-mainz.de/mapsp/mapp792d.htm) a été consulté pour distinguer territoire impérial et royaume prussien extérieur. Sa date est postérieure : aucune frontière de 1792 n'est appliquée à 1776. L'image GIF n'a pas pu être affichée par l'outil web et n'est pas une carte lue ici. La tentative d'ouverture du PDF cartographique Princeton/De Gruyter sur les possessions 1740–1780 a échoué (405); le PDF austriaca a renvoyé une réponse sans texte exploitable. Ces pistes ne servent à justifier aucune correction.

## Décision de traduction

La partition politique générale déjà installée est conservée, catégorie B. Les propriétés dynastiques, seigneuriales et épiscopales internes ne deviennent pas des pays indépendants par déduction. Un second niveau administratif dans STATE_MORAVIA ne permettrait pas de placer un office distinct à Opava : il renforcerait l'agrégat déjà administré depuis la passe morave. Aucun effectif historique ou déficit fonctionnel ne justifie ce doublage. Le modèle conserve donc sa limite institutionnelle explicite, sans prétendre représenter séparément chaque office.

La conclusion est bornée : **aucune nouvelle correction fonctionnelle démontrée dans cette passe**, et proposition de conserver l'approximation politique B. Elle ne certifie pas le cadastre de Nysa, les enclaves ni les marges lusaciennes. Le défaut concret de Teschen reste ouvert et distinct; ce n'est pas une conclusion de conformité générale de toutes les possessions habsbourgeoises.
