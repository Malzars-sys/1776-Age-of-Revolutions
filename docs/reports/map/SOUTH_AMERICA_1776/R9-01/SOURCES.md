# R9-01 — première passe andine, 27 octobre 2026

Date cible : **1er janvier 1776**. Pas de nouveau pays, de nouveaux habitants ou de modification du bitmap.

## Recherche déjà établie réutilisée

`docs/reports/map/MAP1/inputs/regional_originals/R9_SOUTH_AMERICA_RECOMMENDATIONS.csv`, lignes 30–64 vérifiées après localisation ColGrep, puis lecture CSV ciblée : cas 0028–0029 (Iquicha/Ica), 0032 (La Paz), 0047 (Potosí), 0059 (Malouines), 0062 (Uruguay). Fichiers frères `SOURCES.csv` et `UNCERTAINTIES.md` conservés sans réécriture. Les priorités et incertitudes originales ne sont pas déclarées résolues par cette première passe.

## Iquicha et le Pérou colonial

- Cecilia Méndez, [_The Plebeian Republic: The Huanta Rebellion and the Making of the Peruvian State, 1820–1850_](https://www.dukeupress.edu/the-plebeian-republic), Duke University Press, 2005. Présentation de l'éditeur consultée : rébellion royaliste de Huanta au XIXe siècle, pas une colonie distincte de 1776.
- Cecilia Méndez Gastelumendi, [_El poder del nombre, o la construcción de identidades étnicas y nacionales en el Perú: mito e historia de los iquichanos_](https://www.history.ucsb.edu/wp-content/uploads/histpublications/files/02724-poder_del_nombre_iep.pdf), IEP, Documento de Trabajo 115, janvier 2002, copie universitaire UCSB. Introduction et section sur les archives tributaires consultées dans le texte PDF accessible : apparition de la désignation dans le contexte de 1826–1828 et critique de sa rétroprojection. Pas de lecture intégrale revendiquée.

Les 17 RGB IQU étaient **déjà ceux d'une colonie espagnole** (`country_type = colonial`, pacte SPA–IQU), pas une autorité indigène indépendante que l'on aurait découverte. Les réunir à SC3 supprime une subdivision anachronique sans étendre par cette opération la souveraineté impériale à de nouvelles terres. Le pays IQU et ses sources restent définis pour usages ultérieurs ; seul son territoire et son pacte initiaux disparaissent.

`STATE_ICA` est une vaste enveloppe technique qui comprend côte et hautes terres. Son hub de ville natif correspond à **Cusco**, pas à la ville d'Ica. L'hypothèse initiale fondée sur le nom du State_ID a échoué en CHECK, avec 86 pixels d'écart ; elle a été rejetée et archivée, sans entrer dans le FIT ni décider d'un transfert.

## La Paz, Charcas et la date de 1776

- Instituto Nacional de Estadística de Bolivia, [_Aspectos históricos_](https://www.ine.gob.bo/index.php/bolivia/aspectos-historicos/), sections «La Audiencia de Charcas» et «Fundación de ciudades», texte consulté : Charcas dépend du Pérou jusqu'en 1776, fondation de La Paz en 1548, rôle des villes coloniales. Ce résumé ne justifie pas l'administration de toutes les forêts du State_ID.
- Carlos III, **cédule du 1er août 1776**, [_Real cédula de erección del virreinato del Río de la Plata_](https://es.wikisource.org/wiki/Real_c%C3%A9dula_de_erecci%C3%B3n_del_virreinato_del_R%C3%ADo_de_la_Plata), transcription primaire consultée, paragraphes «EL REY» et datation. L'acte énumère Charcas/Potosí et modifie les dépendances sept mois après le départ : il ne doit pas placer rétroactivement La Paz dans la nouvelle vice-royauté au 1er janvier.
- Ana Meléndez Crespo, [_La Paz, Bolivia: Una traza de ideal religioso y motivos políticos_](https://espaciosurbanos.azc.uam.mx/index.php/path/article/view/134), Anuario de Espacios Urbanos, résumé universitaire consulté : implantation urbaine et institutions coloniales de 1548–1550.
- [_Síntesis histórica y geográfica de la ciudad de La Paz_](https://boletinmuseoprecolombino.cl/html/02-arano-27-1/), Boletín del Museo Chileno de Arte Precolombino, passage historique consulté : ville-relais du trafic Potosí–Cusco. Sert à justifier le noyau urbain, pas chaque province frontalière.

## Correspondance et compromis

Calage diagnostique à cinq hubs natifs FIT (Lima, Arequipa, Cajamarca, Potosí, Santa Cruz), RMS **4,35 pixels** ; deux CHECK (Cusco, La Paz), RMS **6,58 pixels**. Ce sont des contrôles empiriques du fond de jeu, pas une précision cadastrale ni des points historiques indépendamment levés.

La Paz n'est pas attribuée en bloc : **`xDE2B7D`**, ville actuelle du bitmap, rejoint SC3 avec les deux cellules de raccord **`x57125B` et `xA2A5FA`**. Le chemin vers le noyau de Lima est vérifié avec les contacts par côtés, les provinces infranchissables et les règles d'adjacence. Ce raccord est le compromis de continuité demandé par le joueur, pas un tracé attesté de corregimiento. L'essai d'enveloppe numérique par latitude/longitude, non installé, a été archivé et abandonné.

## Population et limites

Les **39 600 Quechua** d'IQU et les **158 970 South Andean** de la portion AP7 de La Paz sont des effectifs hérités, réaffectés dans leur région existante. Aucune valeur n'est présentée comme un recensement local de 1776 ; aucune distribution n'est déduite de la superficie des pixels. Les **458 067 autres habitants** de La Paz gardent provisoirement leur propriétaire et leur identité. Cette prudence conserve les données, sans valider l'attribution kayapó des autres secteurs andins ou amazoniens : elle demeure à revoir avec les autorités locales et les districts de missions.

Les documents BNE/Cruz Cano de 1775 restent des pistes du dossier canonique ; l'accès BNE a renvoyé 403 lors de cette passe. **Aucune superposition de ses huit feuilles n'est revendiquée.** Les droits contestés aux Malouines et les opérations hispano-portugaises ne sont pas tranchés par les présentes sources.
