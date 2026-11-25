# Issue 56 — enquête de simulation initiale

**Note finale du 17 novembre 2026 :** ce plan initial est historique. Voir REPORT_FR.md, BENCHMARK_QUALITY.json et PRESERVATION_AFTER.json pour les résultats effectifs. Les essais sont arrêtés ; l'issue #56 reste ouverte, sans correctif validé. Le contrôle WARM1 n'a pas été exécuté. Aucune prochaine action de ce plan ne constitue une instruction de reprise automatique.

Mission active demandée dans le texte joint par le joueur, réponse en français. Référence main locale et distante : bd776919f625016cb9e63b2359cc04796c681ef5, workspace propre au début de la mission. COMPACT est commité dans 764095ed. Les anciennes autorisations Git ne s'étendent pas à cette mission.

Issue dédiée créée après recherche de doublon par titres simulation/slowdown/performance : https://github.com/Malzars-sys/1776-Age-of-Revolutions/issues/56. Liée à #54, qui traite l'interface technologique et dont le corps initial est historiquement dépassé. Ne pas recopier son ancien statut comme résultat de simulation.

## État acquis

- Consignes communes, économie, territoire/recherche lues ; aucune correction historique, économique ou territoriale autorisée dans le produit normal.
- Deux installations vérifiées : Steam 1.15.1 sans DLC de gameplay ; locale 1.15.0 avec dossiers DLC, à garder séparée.
- Contrôleur Windows @oai/sky via node_repl disponible et fenêtres énumérées. Une session locale 1.15.0 était ouverte ; le joueur a répondu « La session est fermée » à la demande de fermeture préalable. Vérifier effectivement l'inventaire avant de lancer les essais isolés.
- ColGrep existe et l'index est local, mais sa recherche agent échoue à créer son verrou (accès refusé). Repli sur rg et parseur du dépôt, sans changement du modèle, index ou droits.
- Inventaire statique initial dans STATIC_INVENTORY.json, produit par tools/performance/simperf56_static.py : aucun échec de parsing. Proxies des propriétaires d'états initiaux : 646 pour le mod, 449 vanilla Steam. Groupes POP : 6815 / 4483 ; population littérale : 837328654 / 1021666179 ; blocs de bâtiments : 4126 / 3171 ; niveaux explicites : 9404 / 8699. Ce sont des données de scripts, pas des comptes runtime certifiés.
- L'inventaire initial compte les définitions et tous les champs des journaux, y compris effets de conclusion ponctuels : ne pas transformer son classement brut en classement de coût récurrent. Distinguer noms uniques et contributions REPLACE_OR_CREATE (495 définitions JE brutes, ancien catalogue 494 effectives).
- Définitions natives NGame : JOURNAL_ENTRY_UPDATE_ACTIVE=4 jours, INACTIVE=14 jours. Aucun mod de cadence repéré à ce stade. Drapeaux graphiques NCoatOfArms : COA_FLAGS_FRAMES_BETWEEN_UPDATES=30 images, cleanup toutes 20 mises à jour ; ce n'est pas la cadence hebdomadaire éventuelle des triggers de choix de drapeau, qui reste inconnue.
- HRE : common/on_actions/1776_imperial_constitution.txt, hook mensuel global et nombreux helpers de pacts/membership. IA infrastructures : common/on_actions/13_1776_ai_regional_infrastructure.txt et common/scripted_effects/1776_ai_regional_infrastructure_effects.txt:414 ; tri répété de dix rangs GDP et parcours des États. Le cooldown 180 jours concerne seulement certains changements de PM, pas le contrôleur complet. Tout lien avec une amélioration après six mois reste une hypothèse.

## Prochain travail à exécuter

1. Affiner le risque récurrent : champs de conditions et pulses des JE, graphe enfant des on_actions ; exclure les seuls effets de conclusion du classement de cadence. Lire les blocs réellement actifs à 1776 et sans DLC.
2. Capturer les empreintes de préservation et figer une copie runtime de main dans un nouveau laboratoire Temp aor1776_simperf56_20261117. Aucun changement du mod normal, sauvegardes, playsets ou installations natives.
3. Préparer un module de télémétrie commun aux témoins et diagnostics. Des événements cachés peuvent écrire debug_log : exemple natif common/character_roles/01_appointment_roles.txt:18 utilise [TimeKeeper.GetCurrentDate.GetString], et les événements country_event hidden=yes existent dans events/1776_intervention.txt. Vérifier au moteur toute instrumentation avant de revendiquer un benchmark. Éviter les flags console devinés.
4. Capturer le débit de simulation dans des fenêtres fixées après les mois 0/1/3/6/12, CPU et RAM du seul enfant possédé ; exclure le démarrage et les pauses. Vanilla standard part de 1836, donc comparer aussi les offsets, sans prétendre à une sauvegarde ou un monde identique. Dates de février/avril/juillet diffèrent d'un calcul non bissextile : 1776 et 1836 sont bissextiles.
5. Essayer les actions via le contrôleur autorisé ; si capture après chargement encore indisponible, demander seulement le geste humain manquant. Le contrôleur avait des échecs FrameArrived lors de #54, les raccourcis clavier peu fiables, mais les clics de menu fonctionnaient.
6. Diagnostics réversibles, une variable par copie après choix étayé. Ne pas arrêter à la seule préparation si des mesures réelles sont possibles. Aucun correctif produit sans preuve et autorisation requise.
7. Rapport technique français, classement avec confiance, données réelles et limites, préservation finale, mise à jour de l'issue #56 autorisée explicitement par la demande.

Aucun nouveau benchmark de simulation ni gain de performance n'est encore acquis à ce point. Aucun lancement de jeu n'a encore été effectué pour l'issue 56. Aucun commit, push, fusion, changement de branche ou modification de main hors outils/rapports du présent chantier.
