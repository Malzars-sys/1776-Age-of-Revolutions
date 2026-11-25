# État de travail — nouveau contrôle explicitement demandé

## État final — 17 novembre 2026, après publication GitHub

**EXPÉRIENCES TERMINÉES. AUCUN PROCESSUS VICTORIA 3 D’ESSAI ENCORE OUVERT.**

Le contrôle prioritaire a été exécuté : sauvegarde du 21 avril 1777, mesure avant redémarrage, fermeture complète, puis deux rechargements indépendants du même fichier. DAY 14/28/56 : **9/17/33 s avant**, **9/17/33 s** puis **8/16/31 s** après rechargement. Aucun retour du ralentissement fort dans les journées complètes mesurées.

Le contrôle initial INIT_REF1 et l’ablation mensuelle régionale INFRA_M0 sont eux aussi **terminés** et fermés : **27/52/93 s** contre **28/53/96 s**. Aucun gain net observé. Six traces du bypass mensuel sont présentes. Cette ablation n’exonère pas l’initialisation régionale déjà appliquée avant la sauvegarde initiale.

Rapport canonique de cette passe : **REPORT_FR.md** ; mesures détaillées : MEASUREMENTS.csv et cinq fichiers de résultats JSON. SUMMARY.json porte l’empreinte du rapport. Audit final PRESERVATION_AFTER.json entièrement conforme : runtime 2996/2996, profil normal 80/80, diplomatie 3/3, anciennes preuves 233/233, index/HEAD/exécutable inchangés.

**Issue #56 mise à jour et relue après publication**, toujours ouverte, le 2026-11-17T14:50:51Z. Voir GITHUB_PUBLICATION.json et GITHUB_UPDATE_FR.md ; le corps précédent est conservé intégralement dans GITHUB_BEFORE_RELOAD_UPDATE.md et sur GitHub sous historique.

Prochaine expérience recommandée : **HRE mensuel seul**, avec HRE quotidien et infrastructures régionales normaux, sans cumuler les ablations. Aucun diagnostic n’est intégré au mod principal. Aucune cause précise ni correction équivalente validée. La sauvegarde mature et tous les profils restent conservés.

Les sections ci-dessous sont un **historique dépassé**. Ne pas suivre leurs anciennes mentions « actif », « pas encore lancé » ou leurs prochaines actions : ces étapes sont maintenant accomplies.

## Mise à jour prioritaire — 14:08 UTC

Le contrôle mature a été RÉELLEMENT EXÉCUTÉ et répété. MATURE1 fermé (session20083 terminée), sauvegarde **royaume de france_1777_04_21.v3**, version1.15.1,122443314octets, SHA256 **879867ccd58f230c9eef2fbe04570171679cea015010e713be5c746707b732eb**. Voir MATURE_SAVE.json. Le monde est alors âgé d’environ16mois ; ne pas annoncer une sauvegarde exactement au1janvier1777.

MATURE1 avant redémarrage : après sauvegarde et reprise le21avril, bornes DAY du22avril et dates suivantes, **14/28/56jours en9/17/33secondes**. Monde laissé au-delà de155jours aprèsS pour les tranches suivantes. Résultat complet MATURE_BEFORE_RESTART.json. Pause et préparation exclues avantS+1. Requête requests/MATURE1.stop créée et processus complètement fermé avant RELOAD1.

RELOAD1 terminé : processus32668, session11530, runtime/RELOAD1_20261117T134725590Z. MêmeS/mêmehash, mêmes paramètres et exécutable. Débit **9/17/33secondes** pour14/28/56jours, puis56jours suivants35s (contre38s avant redémarrage). DAY196consécutifs, sortiecontrôlée0. Voir RELOAD1_RESULTS.json.

RELOAD2 terminé : processus30228, session44218, runtime/RELOAD2_20261117T135627113Z. MêmeS. **8/16/31secondes**, puis56jours suivants36s.196DAYconsécutifs. Voir RELOAD2_RESULTS.json. Le ralentissement fort initial ne revient pas dans ces deux répétitions ; ne pas prétendre en avoir identifié la fonction causale ni exclure un effet inférieur à unjour/pendant préparationenpause.

UI des trois passages harmonisée avant reprise : ouvrir Menu puis Reprendre, sans choisir d’option, pour masquer le popup colonial ; vuecarteFrance, même zoom, vitesse5 avantJouer. Aucune intervention pendant les fenêtres. Quelquescaptures WGC ont expiré après menus/sauvegarde ; **js_reset du node_repl puis réimport @oai/sky et nouvelle sélection unique** a rétabli la capture, sans action aveugle ni changement de jeu. Variablescourantes globalThis.r56window/r56state explicites.

**Maintenant actif : INIT_REF1**, lancé14:07:48UTC, processus20244, session exec81572. -MaxSeconds1800 -KeepAfterWindows -StopAfterHeartbeatDays171. Profil initial1776 depuis le mêmefichier387a3637... que les anciennes références. Objectif : contrôle positif contemporain, vérifier que la lenteur revient avec le MONDEINITIAL malgré les redémarrages déjà effectués. Àla dernière action : chargementinitial dujeu, pasencore cliquéContinuer niunpause. Refaire sélection unique de la nouvellefenêtre, ne pasréutiliser handleRELOAD2.

Expérience suivante déjà préparée après résultat RELOAD1 : **INFRA_M0** (profil enregistré, pas encore lancé). Même sauvegarde initiale et réglages que INIT_REF1, seule différence un fichier **common/on_actions/13_1776_ai_regional_infrastructure.txt** dans LAB/diagnostic_no_regional_monthly. Seul corps du child aor1776_ai_regional_infrastructure_monthly est bypassé ; initialisation, natif et toutHRE inchangés. Trace mensuelle limitée àFRA : SIM56|DIAG|INFRA_MONTHLY_BYPASSED. Voir INFRA_MONTHLY_VARIANT.json pour SHA sourcef1b3cc... et candidat492383.... Cette ablation n’est pas un correctif équivalent. Un seul système àla fois.

Après INIT_REF1 fini : analyser comme avant (save-date1776.1.1, mêmesancres DAY) puis lancer INFRA_M0 avec171DAY. Vérifier sa trace et comparer aux mêmesdates initiales ; ne pas confondre gain net et profil CPU pur, car le monde peut évoluer différemment. Selon résultat recommander HREmensuel séparément. Les outils de préparation et caches sont prêts, aucun besoin de refaire les anciens essais vanilla/COMPACT.

Àlivrer : nouveau REPORT_FR.md dans CE sous-dossier avec tableaux CPU/RAM, incertitudes, interprétation bornée et prochaineexpérience ; CSV/JSON des métriques ; audit après avec simperf56_reload_audit.py after ; update #56 par API en préservant historique ; aucun commit/push/merge. Ne pas remplacer les anciens rapports. PREPARATION est étendu avec archives exactes avant chaque nouveauprofil. Avant audit protège aussi233preuves antérieures et15outils ; l’analyseur aétéétendu AVANT snapshot outils et anciencode archivé (2lignes/argumentoptionnel), pas de perte de travail préexistant.

## Historique initial ci-dessous (dépassé)

Mission active du 17 novembre 2026 : exécuter réellement le rechargement mature, puis sélectionner une seule expérience mensuelle pertinente. Préserver les anciens rapports, le mod normal et les sauvegardes habituelles. Réponses en français.

MATURE1 lancé à13:24:33UTC, processus16504, session exec20083 ; dossier runtime/MATURE1_20261117T132433675Z. Profil isolé MATURE1. Lanceur existant avec -MaxSeconds3600 -KeepAfterWindows. France commune1janvier1776 chargée ; vitesse5 vérifiée et reprise vers13:31:13UTC. Aucun choix d’événement. Au contrôle13:34:19UTC, date19juin1776. Fenêtres natives initiales29s puis22s pour14jours. Le monde n’est pas encore sauvegardé en1777.

**Prochaine action :** attendre une date après le16janvier1777 (fin de dernière fenêtre originale) ; vers février convient. Lire capture fraîche, cliquer Pause du levier àgauche du cadran (ancienne vue962×570 : x866,y43 pour Pause ; Jouer x866,y60). Ne pas changer la vitesse. Menu enhautàdroite x951,y40 → Sauvegarder x232,y231 → nompar défaut daté1777 → bouton x592,y465. Toutes coordonnées àreprendre d’une capture fraîche, uneaction puis rafraîchissement. Vérifier le fichier réel et son en-tête date/version/hash. Aucun écrasement d’ancienne sauvegarde.

Ensuite : reprendre àvitesse5 et mesurer avant tout redémarrage au moins112jours aprèsS, idéalement171pour disposer des tranches suivantes. Le fichierS demeure immuable. Utiliser les bornesDAY S+1 pourexclure la pause/sauvegarde et le premierjourpartiel ; dates identiques dans les nouveaux processus. Ne pas employer les métriques d’arrivée tamponnée des journaux. Lorsque lesDAY nécessaires sont effectivement écrits, requête d’arrêt LAB/requests/MATURE1.stop pourfermer uniquement l’enfant possédé (ou sortie GUIpropre après collecte).

Préparer ensuite RELOAD1 depuis S avec `simperf56_reload_prepare.py RELOAD1 --save <S> --seed MATURE1`. Mêmeexécutable/runtime/paramètres/DLC. Nouveauprocessus complet via lanceur `-Trial RELOAD1 -MaxSeconds1800 -KeepAfterWindows -StopAfterHeartbeatDays171` ; Continuer puisvitesse5, Jouer. Répéter RELOAD2 depuis mêmeS sipossible.

`simperf56_reload_compare.py <run> --save-date YYYY.M.D --output <nouveau fichier>` réutilise l’analyseur existant avecancres DAY arbitraires. Celui-ci aété étendu parun argument facultatif extra_starts ; octets précédents archivés dans ANALYZER_BEFORE_ANCHORS.py et régression des anciens temps MAIN2 vérifiée. Produit SAVED_PLUS_0_14/28/56 ettranches suivantes pour comparer le mêmeétat du monde etles mêmesdates. Collecter ≥155jours pour toutesles ancres préparées ; 171prévu.

Preservation avant enregistrée dans ce sous-dossier : 2996runtime,80profilnormal, index,exe,3diplomatie,233preuves anciennes,15outils actuels. PREPARATION.json estétendu avec archivage exact avant chaqueprofil ; autres preuves anciennes àlaisserintactes. Main figé entièrement revérifié :2996empreintes identiques. Aucun Git d’écriture.

Contrôle Windows via @oai/sky dans node_repl. Variables **globalThis.r56window**, **globalThis.r56state**, références globalThis explicites. Refaire sélection unique aprèschaque relancement. Ne pas utiliser d’anciens handles. Le bureau ne montrait aucuneautre sessionVictoria3 au départ. Unecapture aaffiché unevueCodex ; activation duwindowVictoria3 et rafraîchissement ont rétabli la vraieimage. Aucuneinput surCodex.

Choix d’expérience suivant àfaire APRÈSles résultats : priorité contrôleurmensuel d’infrastructures, en le désactivant seul dansune copiede diagnostic avec tracebornée ; HREmensuel séparément ensuite sijustifié. Ne pas déclarer lacause prouvée ni intégrerunsystème désactivé.
