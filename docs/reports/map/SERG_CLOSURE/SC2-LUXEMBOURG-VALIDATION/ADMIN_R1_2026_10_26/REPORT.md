# SERG TERRITORIAL 1.0 — PROGRESSION : 34,89 %

26 octobre 2026. Mission unique : résolution administrative de SC2-LUXEMBOURG-VALIDATION. **82/235 → 82/235 points ; 81 tâches, périmètre 1.0.0 inchangé.** Aucun test moteur ni reçu humain créé.

## Cause et décision installée

Le conflit combine une régression locale de configuration et une attente de conservation devenue obsolète. BUILD avait prévu un recalibrage de la bureaucratie nationale, mais sa matrice et son catalogue conservaient le propriétaire LUX antérieur au transfert : cible positive de 1 niveau pour LUX/Wallonie, contre 0 pour BEO/Wallonie. La disparition des deux déclarations anciennes est réelle ; attendre leur conservation littérale dans deux fichiers n’est plus un contrat fonctionnel adapté.

La Wallonie technique est partagée entre **BEO, LGE et STM**. La Flandre est un autre État partagé, entre BEO et LGE. Les trois administrations BEO flamandes alimentent la bureaucratie nationale ; leur capacité fiscale est locale à leur État. Les déclarations LGE wallonnes relèvent d’un autre propriétaire. Aucune de ces capacités n’est présumée couvrir fiscalement BEO/Wallonie.

Une administration provinciale luxembourgeoise est historiquement défendable : les [Archives nationales](https://anlux.public.lu/fr/rechercher/fonds-collections/fonds-anciens.html) identifient le Conseil provincial et les Trois États ; la [Ville de Luxembourg](https://www.vdl.lu/fr/visiter/art-et-culture/architecture-et-patrimoine/unesco) situe l’administration dans la ville haute de la place forte. **Un niveau est une approximation B minimale, pas un nombre de bureaux ou d’employés certifié pour 1776.** Les sources et limites figurent dans [SOURCES.md](SOURCES.md).

Correction installée : **une seule administration ordinaire de niveau 1, propriété de BEO dans son bloc wallon existant**. Les trois niveaux flamands restent intacts. Les anciens blocs ne sont pas restaurés. La création dessert techniquement toute la portion BEO de Wallonie comprenant Luxembourg ; elle ne crée ni commune, ni province, ni pays distinct.

Les quatre PM du nouveau niveau sont explicites : organisation simple, bureaucrates héréditaires, administration religieuse, absence de rapport organisé. Le PM héréditaire admet la loi demandée de diètes provinciales ; le PM professionnel des bâtiments existants n’est pas copié et n’est pas modifié. L’effectivité des lois et des PM reste à observer en jeu.

À effectif plein, avant autres modificateurs, les scripts déclarent +10 de bureaucratie nationale et +2 de capacité fiscale locale pour ce niveau ; les trois PM d’emploi totalisent 1 500 emplois. Aucun intrant matériel n’est ajouté par ces quatre PM. Cela ne garantit ni plein emploi, ni budget positif, ni collecte complète des impôts. Aucune population ou subvention n’est ajoutée pour assurer artificiellement son fonctionnement.

## Contrat BUILD et protections

La matrice runtime **active** reçoit deux corrections : BEO/Wallonie 0 → 1 ; LUX/Wallonie 1 → 0. Les 4 196 autres lignes, sur 4 198 au moment de la passe, sont conservées à l’identique ; le total des niveaux cibles est inchangé. Les colonnes de diagnostic initial ne sont pas présentées comme des mesures de cette nouvelle partie. Les préimages actuelles et le détail des deux amendements sont archivés dans le nouveau [BASELINE.json](BASELINE.json) et [BUILD_TARGET_AMENDMENT.json](BUILD_TARGET_AMENDMENT.json). Aucun ancien rapport, ancien résultat brut ou ancienne baseline n’est réécrit.

Seul fichier fonctionnel modifié : `common/history/buildings/00_west_europe.txt`, par insertion dans le bloc BEO existant. Autres bâtiments, propriétaires, PM préexistants, réserves, populations, formation luxembourgeoise et général sont conservés. Les répétitions de blocs et les autres déclarations préexistantes entre fichiers régionaux et overlay sont conservées ; une déclaration unique du nouveau niveau est contrôlée sur toutes les couches. Leur interprétation moteur n’est pas déduite d’un simple comptage.

## Contrôles et limites

La [validation ciblée](STATIC_VALIDATION.json) contrôle le delta exact du fichier partagé, la création unique, les deux seules lignes BUILD, les États partagés, les quatre groupes et 137 881 habitants du transfert, les unités et la dépendance envers AUS, les PM, ainsi que la conservation des anciennes preuves.

Résultats exécutés sur cette livraison : **23/23 contrôles ciblés** ; **27 tests du suivi réussis sur 28, aucun échec et un ancien test désactivé**, réservé à l’instantané immuable de l’initialisation. La comparaison BUILD bornée utilise aussi le parseur historique sur le fichier régional concerné et son overlay, avec ses résultats propres dans [BUILD_SCOPED_REGRESSION.json](BUILD_SCOPED_REGRESSION.json). Aucune suite mondiale ancienne n’est présentée comme rejouée ici.

Le [contrôle TECH différentiel](TECH_DELTA.json) confirme quatre groupes de PM affectés, sans technologie de construction ou de PM manquante pour ce niveau, et **aucune nouvelle anomalie BEO**. Le diagnostic BEO global reste `FAIL_STATIC` avant et après : port flamand soumis à `enclosed_dock_systems`, lois demandées et recrutement d’infanterie de ligne signalés ailleurs. Ce sont des incompatibilités de scripts ou de disponibilité préexistantes, pas des pannes moteur observées, et elles ne sont pas corrigées par cette mission.

Le parseur global BUILD historique rejette déjà les déclarations compactes d’un fichier Berchtesgaden inchangé. Ce résultat est conservé dans [BUILD_COMPATIBILITY.json](BUILD_COMPATIBILITY.json) ; aucun ancien validateur n’est modifié pour le rendre vert. La non-régression adaptée à cette correction s’appuie sur les signatures de toutes les déclarations de bâtiments avant/après et sur les lignes du contrat actif, sans relancer l’application mondiale BUILD.

Les résultats de suivi, contrôles de conservation et empreintes finaux figurent dans [FINAL_CHECKS.json](FINAL_CHECKS.json). Les deux échecs du précédent audit restent dans son résultat brut, avec leur contexte historique ; ils ne sont ni supprimés ni déclarés rétrospectivement réussis.

## Statut réel et prochaine validation

Le conflit administratif technique est résolu. **SC2-LUXEMBOURG-VALIDATION : IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**, sans clôture ni point supplémentaire avant reçu humain spécifique. La régression de configuration est établie statiquement ; aucune panne de jeu ni rentabilité n’est prétendue observée.

[Protocole Luxembourg limité](PLAYER_TEST_PROTOCOL.md) : nouvelle partie 1776, administration BEO wallonne niveau 1 et trois niveaux flamands conservés, PM et emploi, transfert politique/démographique et formation, un mois puis sauvegarde/rechargement.

[Liste groupée actualisée](PLAYER_TEST_PROTOCOL_GROUPED.md) : les huit tâches peuvent être inspectées dans la même session, avec les contrôles restants de Teschen et de la mine de sel distingués. Aucun nouveau territoire ni deuxième tâche de clôture n’est commencé. Teschen n’est pas retraité cartographiquement. Aucune écriture Git, aucune modification du vanilla.
