# BALKANS-03 — Contrôles et limites

| Contrôle | Preuve | Portée |
| --- | --- | --- |
| Syntaxe et mutation ciblée | VALIDATION.json | 113/113 : reconstruction exacte des huit fichiers fonctionnels ; extérieur des deux blocs MON identique. |
| Souveraineté, population, assets | BASELINE/AFTER, CELLS, POPULATION_LEDGER | Tous les propriétaires mondiaux, POPs et bâtiments locaux identiques ; monde 834 936 539 ; aucun transfert. |
| Institutions / personnages | VALIDATION et REGRESSION | Lois résolues, Sava conservé, un seul souverain et un seul héritier MON, Jovan et trait d'office sans bonus. |
| Technologies | STARTING_TECH_CHECK.json | Neuf technologies existantes, prérequis fermés, réserve autorisée par sa technologie et les levées ; aucun bâtiment/PM nouveau. |
| Localisation FR/EN | REGRESSION.json | Clés propres uniques, deux surcharges vanilla intentionnelles, BOM et icône native valides. |
| B01/B02 | PRE_INSTALL_AUDIT et REGRESSION | 23 derniers reçus fonctionnels identiques à l’entrée, puis trois fichiers partagés réconciliés avec Ortenbourg ; Cyclades et lois danubiennes vérifiés ; archives anciennes non réécrites. |
| Rejeu B02 | prior_lot_replay/VALIDATION.json | Résultat brut conservé : 92/99. 7 échecs de référence datée après les mises à jour concurrentes ; voir EXTERNAL_ORTENBURG_UPDATE.json et REGRESSION.json. Ce ne sont pas 99 nouveaux succès. |
| Réconciliation du rejeu | REGRESSION.json | 36/36 : deux mutations propres à MON et les travaux externes recensés sont réconciliés séparément, anciens travaux externes préservés depuis l'entrée B03, Git courant stable, reçu SERG séparé. |
| Concurrence | CONCURRENT_CHANGES / EXTERNAL_SERG_UPDATE | 2482 fichiers fonctionnels hors lot identiques et 22 mutations externes recensées, dont cinq fichiers d’Ortenbourg vérifiés ; 113 preuves anciennes et de revue technique protégées. Sur 873 preuves SERG initiales, 868 identiques et cinq mises à jour externes archivées sans écriture de cette tâche. |
| Moteur / joueur | GROUPED_RUNTIME_ITEMS.md | NON EXÉCUTÉ ; aucune attestation humaine créée. À regrouper en fin des travaux balkaniques techniquement réalisables. |

Commandes reproductibles : `python tools/world1776_balkans03.py --validate`, puis `python tools/world1776_balkans03_regression.py`. Ne pas relancer `--apply`. Les tests historiques B01/B02 ne doivent pas réécrire leurs reçus ; le rejeu B02 ci-dessus redirige tous ses résultats vers B03.
