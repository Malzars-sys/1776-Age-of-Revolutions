# Issue 54 — reprise locale et état récupéré

> État actualisé le 17 novembre : après la série manuelle terminée et l'autorisation explicite du joueur, les deux expressions COMPACT sont appliquées au mod principal. Le fichier installé est identique au candidat mesuré ; les contrôles de visibilité et de préservation passent. Voir [le reçu d'application courant](INTEGRATION_2026_11_17/REPORT_FR.md) et [le bilan des mesures](MANUAL_RESULTS_2026_11_17/REPORT_FR.md). Le mod principal n'a pas encore été relancé après application. Les sections de récupération ci-dessous restent conservées comme historique.

La récupération locale et le contrôle de préservation sont terminés. Les nouvelles tentatives sont isolées du mod normal, des profils précédents et des deux installations du jeu. Aucun résultat nouveau de fluidité n'a été obtenu : la capture du jeu a échoué après la demande de chargement de la sauvegarde. Le diagnostic de performance reste ouvert.

## Accès et conservation vérifiés

Accès réel au PC Windows CLAYMORE, au dépôt et au laboratoire temporaire. L'interface Windows prise en charge énumère les fenêtres, active Steam et capture le menu de Victoria 3. Le clic Continuer a bien déclenché le chargement de la sauvegarde. Ensuite, `get_window_state` a échoué avec `FrameArrived timed out: timed out waiting on channel`, puis avec la même erreur après nouvelle sélection de l'unique fenêtre et réassociation. Aucun clic visant l'arbre n'a été envoyé après ces échecs. L'état réel de la carte et de l'arbre après chargement n'est donc pas vérifié dans cette reprise. Cette panne de capture ne prouve pas un gel du moteur.

Le reçu `BEFORE.json` vérifie les copies intégrales : A contient ses 3776 fichiers attendus, B les mêmes moins `gui/tech_tree.gui`, C ne change que ce fichier, et le probe COMPACT ne change également que ce fichier. Les neuf variantes archivées ont toutes leur empreinte attendue. La sauvegarde française du 1er janvier 1776 existe et conserve l'empreinte `e6abb3c2305036855a11db308657164f71cecca29002ac6fdc7822c66fd24791`. Les réglages du laboratoire correspondent à la référence de la série mesurée.

Les installations restent distinctes : Steam 1.15.1, exécutable `fb4ec0698afd3d3b1a785926d57bd5d68c95a4afd04b56f6bd45abd7a5672b15`, avec le seul dossier DLC de bande-son ; installation locale 1.15.0 avec d'autres dossiers DLC, consultée seulement. La présence de dossiers ne certifie pas leur activation.

Les sept playsets normaux, onze associations de mods et cinquante et une associations DLC sont identiques à la référence historique après exclusion des deux seuls playsets d'essai archivés et du champ de synchronisation. Le fichier de réglages normal correspond maintenant à l'empreinte initiale ; aucune restauration de réglages ou de base n'a été effectuée ici. Le contrôle historique 24/25 portait sur une dérive binaire d'état d'application, déjà analysée ; il ne prouvait pas une perte de playset.

Par rapport à la référence ancienne, les trois autres fichiers différents sont ceux du chantier russe : action diplomatique, histoire des relations, types de sujets. Ils conservent le pacte Russie–KZH `aor1776_protected_state`, la possibilité russe dans l'action et l'échelle autonomie 3 → tributaire 2 → vassal 1 → annexion. Il s'agit d'une vérification de présence dans les fichiers, sans nouvelle validation moteur ni historique. Ils restent hors du laboratoire et ne sont pas modifiés par cette reprise.

## État des essais retrouvés

Le corps de l'issue et les premiers guides manuels sont dépassés par le [rapport A/B](../V1_15_ISSUE54_INTERACTIVE_2026_11_11/AUTHORIZED_RETRY_2026_11_12/REPORT.md) et le [commentaire GitHub de résultats](https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/54#issuecomment-6836112054). La série A1–B1–B2–A2 a été terminée ; ses vingt captures CPU contrôlées ont été recalculées à partir des CSV, avec les vingt preuves d'état présentes. Le reçu historique annonce 44/44 contrôles à cette date ; ce chiffre n'est pas présenté comme une nouvelle exécution de ces 44 contrôles.

FPS ponctuels natifs archivés, approximatifs et lus visuellement :

| Branche | A1 | B1 | B2 | A2 |
| --- | ---: | ---: | ---: | ---: |
| Production | 8 | 30 | 30 | 8 |
| Militaire | 9 | 42 | 42 | 9 |
| Société | 8 | 27 | 27 | 7 |
| Société après un glissement | 7 | 26 | 26 | 7 |

Ces valeurs soutiennent un coût de la surcharge GUI. B enlève aussi les filtres de compatibilité ; il n'est pas un correctif prêt à intégrer. Les relevés CPU stationnaires étaient proches de 7 % de la capacité totale pour A et 8–9 % pour B : la charge CPU seule ne décrit pas la fluidité.

Une passe diagnostique ultérieure contient 31 captures CPU avec preuves présentes : cinq chacune pour EDGE_OFF, CARD_OFF, BOTH_OFF, FASTPATH (`OPTIMIZED_1R`), COMPACT_1 et CONTROL_REPEAT, plus une référence carte de BALANCED. Les candidats sans capture et la tentative COMPACT_2 sont conservés. `ARCHIVE_MEASUREMENTS.json` donne les sources et recalculs ; il distingue les archives de toute mesure nouvelle.

- EDGE_OFF : environ 19/22/21 FPS ; CARD_OFF : 9/10/8 ; BOTH_OFF : 36/43/26. Ces diagnostics retirent volontairement des filtres et ne doivent pas être intégrés.
- FASTPATH : environ 17/21/16 FPS lors de son passage exploitable.
- BALANCED, identique à C : examen ponctuel 8 FPS en production et 9 en militaire, aucune série CPU complète de l'arbre. Aucune amélioration suffisante établie.
- COMPACT_1 : environ 31/34/30 FPS et 30 après un glissement ; une seule série complète retrouvée.
- CONTROL_REPEAT : 8/9/7 FPS et 7 après glissement, confirmant la persistance du témoin lent.
- COMPACT_2 : lancement et sortie conservés, zéro capture CPU et aucune observation FPS enregistrée.
- KEY_CANDIDATE : rejet moteur de `GetKey`, zéro mesure ; ne pas le reprendre comme candidat fonctionnel.

Les séries utilisent le lancement direct Steam 1.15.1 ; il rapporte un échec d'initialisation de l'API Steam. Les journaux des passages A/B établissent le même contenu effectivement monté : bande-son seule, sans DLC de gameplay. Il ne s'agit pas d'une reproduction authentifiée avec tous les DLC.

## Reprise autorisée ici

Le protocole préparé est CONTROL1–COMPACT1–COMPACT2–CONTROL2, sur un nouveau dossier utilisateur du laboratoire, en gardant la même sauvegarde et les mêmes réglages. A et le probe COMPACT sont consultés sans réécriture. Aucun playset, paramètre Steam normal, fichier du vanilla ou fichier produit du mod n'est écrit.

Le premier lancement non mesuré a été arrêté pendant la compilation des shaders ; ses journaux sont conservés. Le cache déjà présent dans le laboratoire a été ajouté au nouveau profil sans écraser ses fichiers existants, puis le témoin a été relancé. Ce travail de préparation ne compte pas comme une mesure CPU de démarrage ou de fluidité.

`COMPACT_STATIC_RECHECK.json` reconfirme 1168 comparaisons de visibilité sur 291 technologies et 392 relations, y compris les témoins négatifs, avec uniquement les deux expressions modifiées. Le vieux vérificateur FASTPATH sélectionnait seulement les expressions de plus de 2000 caractères et rejetait donc COMPACT avant toute évaluation. Le petit adaptateur local sélectionne les deux expressions par leur contenu ; aucun contrôle sémantique n'est supprimé. Ce résultat reste statique.

La latence exacte clic-vers-image et la distribution des temps de trame restent non mesurées. La durée des appels de commande ou de capture n'est pas une latence du jeu. Aucun correctif n'est fusionné ou installé dans le mod normal ; toute validation humaine reste à obtenir.

## Résultat final de cette reprise

Les deux lancements CONTROL1 sont conservés, mais tous deux non mesurés : le premier pendant la préparation des shaders, le second après perte de capture. Les processus possédés ont été fermés par leur lanceur ; le dernier inventaire Windows ne contient aucune fenêtre Victoria 3. Les codes de sortie provoqués par cette fermeture bornée ne constituent pas des crashs mesurés de l'arbre. Zéro nouveau relevé CPU de démarrage, zéro nouvelle capture CPU de l'arbre, zéro nouveau FPS ou délai d'ouverture certifié.

Les journaux de chargement comportent aussi une erreur `Failed to read key reference` autour de la ligne 3174911 de la sauvegarde, ainsi que des erreurs de carte et d'interface. Elles sont conservées sans modification des données ; aucun lien causal avec l'échec de capture n'est démontré. Les anciens passages mesurés ne doivent pas être remplacés par ces tentatives de préparation.

Le vérificateur des diagnostics archivés a été réellement réexécuté : **158/163 contrôles**. Les cinq échecs désignent exclusivement les cinq captures absentes de COMPACT_2. Les fichiers, montages DLC, échantillons, relevés FPS et absence d'erreurs GUI technologiques des six séries complètes contrôlées passent les autres vérifications de ce script. Le résultat incomplet reste explicite dans `ARCHIVE_EXPRESSION_RECHECK.json`.

`AFTER.json` ne trouve **aucun changement pendant cette reprise** parmi les fichiers préservés du dépôt, y compris l'index Git, ni parmi les quatre-vingts fichiers surveillés du profil normal et des sauvegardes. Les copies A/B/C, le probe, les variantes, les exécutables, les deux GUI vanilla et la sauvegarde commune conservent leurs empreintes. Les sept playsets et leurs associations restent identiques à la référence sémantique.

La lecture complète de la section Steam `Software/Valve/Steam/apps/529340` confirme des **options de lancement vides**. Voir `STEAM_PARAMETERS_REVIEW.json`. La première occurrence textuelle de l'identifiant peut appartenir aux tickets d'application ; les extraits de 1200 caractères du premier audit ne prouvent donc pas l'égalité des options. Seules leur longueur et leur empreinte sont conservées dans les reçus locaux, sans contenu brut de ticket. Aucun fichier Steam n'a été écrit par l'agent.

## Relais le plus simple

Ouvrir [LIRE_MOI_FR.md](LIRE_MOI_FR.md), puis double-cliquer sur **LANCER_LES_TESTS.cmd**. Le petit assistant lance les variantes préparées et indique successivement les vues à ouvrir. Un clic Mesurer laisse cinq secondes pour revenir au jeu, puis relève quinze secondes de CPU. Les FPS peuvent être saisis s'ils sont visibles. Il n'envoie aucune commande au jeu et n'exige aucune modification des options Steam ou des playsets.

Les futurs relevés sont explicitement déclarés par l'utilisateur, sans fausse preuve de capture automatique ni validation humaine du correctif déduite de leur seule existence. Ils sont enregistrés dans un nouveau sous-dossier `MANUAL_…` de ce rapport. Une analyse des résultats et une vérification fonctionnelle de COMPACT restent nécessaires avant toute proposition d'intégration.

L'assistant a été vérifié par le parseur PowerShell, par `-CheckOnly` sur l'exécutable, les quatre choix GUI, les réglages et la sauvegarde, puis par deux démarrages `-Preview` terminés avec le code 0 et sans lancement du jeu. Sa fenêtre d'aperçu n'a pas été exposée par l'inventaire du contrôleur : aucune validation visuelle de sa mise en page n'est revendiquée. La collecte manuelle complète n'a pas encore été exécutée. Le lanceur utilise le PowerShell 7 déjà disponible, sans modifier les règles d'exécution ; le Windows PowerShell historique refusait l'exécution locale du script.

L'agent peut reprendre l'analyse des fichiers, la vérification des filtres et la préparation d'un correctif isolé. Dans l'état observé, les gestes en jeu et les observations visuelles manquantes demandent l'intervention du joueur. Aucun correctif expérimental, changement de branche, commit, PR, fusion ou publication ne fait partie de cette reprise.

## Relais corrigé — 17 novembre 2026

Après la capture montrant du batch saisi dans PowerShell, l'assistant a été ouvert directement et le premier passage manuel CONTROL1 a été lancé. Pour les prochaines ouvertures, le raccourci **OUVRIR_ASSISTANT_TEST.lnk** évite toute commande à copier. Voir [le reçu de cette continuation](LAUNCHER_HELP_2026_11_17.md). Les résultats antérieurs restent historiques ; le seul lancement de cette nouvelle session ne constitue pas une mesure.

## Fermeture au début d'une capture — corrigée le 17 novembre

La première capture manuelle a provoqué la fermeture de la boîte modale, puis celle du jeu par son nettoyage. Cette tentative est conservée sans mesure valide. Le cycle de fenêtre a été corrigé et le défaut reproduit dans un test sans jeu : l'ancienne boucle échoue, la nouvelle conserve le processus observé, relève 15,31 secondes de CPU et réaffiche l'assistant. Voir [la correction et ses preuves](CAPTURE_FIX_2026_11_17.md). Ces données de régression synthétiques n'ajoutent aucun résultat de fluidité à l'issue #54. Le parcours réel reste à reprendre depuis le premier témoin.

## Série manuelle terminée et analysée — 17 novembre

Le joueur transmet l'écran « Série terminée ». La session `MANUAL_20261117T000322802Z` contient les quatre lancements et sorties, vingt couples CSV/métadonnées et vingt relevés FPS ponctuels saisis par le joueur. L'analyse recalcule le CPU, contrôle les journaux correspondant aux bons lancements et passe 150/150 contrôles des fichiers de mesure. Les FPS stationnaires sont de 5–8 pour les témoins contre 25–34 pour COMPACT. Les vues sont déclarées par le joueur, sans capture automatique ; la latence exacte et les temps de trame ne sont pas mesurés.

À la question sur des technologies manquantes, liens anormaux ou boutons cassés pendant COMPACT, le joueur répond « Aucun problème remarqué ». Ce retour est une observation limitée, sans certification exhaustive ou accord implicite d'installation.

Le contrôle statique courant repasse 1168 cas et deux témoins négatifs. La comparaison de préservation ne trouve aucun changement dans les 4070 fichiers surveillés du dépôt (index inclus), ni dans les 80 fichiers du profil normal et des sauvegardes ; les playsets et le chantier russe sont préservés. Un patch de revue limité aux deux expressions de visibilité est prêt dans `MANUAL_RESULTS_2026_11_17/COMPACT_REVIEW_ONLY.patch`. Il n'est pas appliqué. Le [rapport courant](MANUAL_RESULTS_2026_11_17/REPORT_FR.md) et `CURRENT_STATE.json` remplacent les anciennes attentes de mesures pour l'état actuel de l'investigation.

## Application autorisée au mod principal — 17 novembre

Le joueur répond « Je t'autorise. » à la demande d'application des deux changements mesurés. Ils sont alors appliqués au seul `gui/tech_tree.gui` du dépôt principal, avec copie intégrale du fichier précédent. Le fichier obtenu est identique octet par octet au COMPACT mesuré. Le vérificateur principal passe 1168 cas et deux témoins négatifs ; la différence contient deux lignes modifiées et passe le contrôle de mise en forme Git en lecture seule. Aucun autre fichier surveillé du produit, de l'index Git ou du profil normal ne change pendant l'application.

Le statut devient `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION` pour la version installée, sans transformer les essais du laboratoire en relance déjà faite du mod principal ni en essai de la version locale 1.15.0 avec DLC. Les preuves, la sauvegarde du GUI et les limites sont dans [le rapport d'application](INTEGRATION_2026_11_17/REPORT_FR.md). Aucun commit, fusion, publication ou changement du chantier russe n'est réalisé.
