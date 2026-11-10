# Dernières finitions avant essai — mission 53, 10 novembre 2026

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Aucun lancement moteur ni accord humain postérieur au correctif n'est attesté.

## Corrections installées

Le tutoriel `je_tutorial_improve_supply_network` utilisait encore `num_convoys_available`, rejeté dans le journal d'erreurs du joueur. Seule cette entrée de `common/journal_entries/00_tutorial.txt` est alignée sur le vanilla canonique 1.15 installé : deux explications d'activation, cible de type bien d'État, existence de cette cible et prix relatif de la marine marchande strictement inférieur à 10 %. Le compteur de convois et son objectif de +400 disparaissent de cette entrée.

Le sous-objectif appelant est hérité sans modification de `common/objective_subgoals/00_subgoals_tutorial.txt`. Il sélectionne un État côtier dont la marine marchande dépasse 30 % de surcoût, enregistre son bien d'État puis le transmet à l'entrée. Il ne passe ni un pays ni un simple État. L'entrée modifiée est identique à son homologue canonique ; aucun autre journal n'a été remplacé depuis le vanilla.

Huit clés manquantes reçoivent chacune une localisation française et anglaise dans deux nouveaux fichiers isolés : objectif Meiji, succès/échec de consolidation du Caucase et des steppes kazakhes, absence de possessions russes au Kouban, au Daghestan et dans le Caucase du Nord. Les textes décrivent les conditions conservées. Les variables de résultat et les mécaniques des trois journaux consommateurs restent inchangées. Le but Meiji indique l'exclusion des propriétaires du gouvernement, la paix, l'absence d'insurrection, la possession du Kantō et la condition légitimité/marginalisation ; aucun délai supplémentaire n'est inventé.

## Vérification et limites

- 48 contrôles sur la proposition, puis 48 sur les fichiers installés : réussis.
- Quatre cas de frontière du prédicat de prix et neuf mutations de régression détectées : réussis. Ce sont des simulations bornées et des contrôles statiques, pas un moteur de jeu.
- Vérificateur existant des dépendances des journaux : 494 entrées, zéro constat dans les références littérales et métadonnées qu'il inspecte. Il ne certifie pas tous les types de portée, tous les DLC ni la disponibilité effective des chaînes.
- Préservation : 2 537 entrées existantes capturées ; seul le fichier de tutoriel change. Dans celui-ci, tous les octets hors du bloc sélectionné sont conservés. Les deux seules additions de données du mod sont les fichiers de localisation. Les sources canoniques consultées et les journaux consommateurs sont inchangés.
- Les travaux concurrents et acceptés, notamment les missions 48–52, sont préservés. Aucune opération Git d'écriture, modification du vanilla, suppression de documentation ni publication Steam.

`CONTRACT.json` et `INSTALLATION.json` contiennent les empreintes des trois fichiers. `OBSERVED_DIAGNOSTICS.json` conserve douze messages antérieurs à la correction ; leur capture ne constitue pas un nouveau test. `CANDIDATE_CHECKS.json`, `LIVE_CHECKS.json`, `PRESERVATION.json` et `JOURNAL_DEPENDENCIES.json` contiennent les résultats effectifs. Audit réexécutable : `tools/compatibility/issue53_final_polish_audit.py`.

Sources techniques : installation canonique locale 1.15, sous-objectif hérité, conditions existantes de `00_meiji_restoration.txt`, `00_player_objectives_great_game.txt`, `03_russia.txt` et déclencheur `meiji_completion_trigger`. Il s'agit d'une correction de compatibilité et de texte, sans nouvelle affirmation historique.

## Étape suivante

Le mainteneur exécute la liste regroupée `TESTS_JOUEUR.md`. Les branches impossibles à atteindre pendant cet essai restent indiquées non testées. Après son retour, préparer une distribution Steam limitée aux données et ressources nécessaires au jeu depuis la version locale testée. Exclure de cet export les outils, rapports lourds, fichiers temporaires et données de développement ; les conserver dans le dépôt source. Cette livraison n'effectue pas encore cet export et ne publie rien.
