# Contrôle par TAG — lecture seule

`tools/validate_starting_technology_1776.py --tag ABC --tag DEF --expectations fichier.json --output rapport.json`

Depuis Python : `snapshot = collect_snapshot()` une seule fois, puis `audit_country("ABC", snapshot, attentes_locales)` ; retourne un dictionnaire sans écrire. La commande retourne 1 si P0/P1, sinon 0 ; lire aussi REVIEW, qui ne vaut pas approbation.

Le fichier d’attentes associe chaque TAG à `required`, `forbidden`, éventuellement `allowed`, `historical_evidence`. Ce sont des attentes propres au pays, jamais un palier uniforme. Pour une absence d’historique, fournir `absence_policy` et `absence_evidence` : `OPEN_DOCUMENTED_REVIEW` conserve une revue P3, `INTENTIONAL_VERIFIED` exige une preuve et ne crée aucune validation humaine. Sans preuve, l’absence est signalée P0.

Vérifie les effets partagés, grants conditionnels séparés, références inconnues, parents, alertes chronologiques existantes, historiques, bâtiments, PM par groupe, gates de construction séparés des PM, ressources régionales, demandes de lois et types d’unités initiales. Les lois demandées ne sont pas certifiées actives ; l’allocation de ressource à la portion du propriétaire, les groupes omis et les choix par défaut du moteur exigent un contrôle en jeu. Les conditions non technologiques complètes des lois/PM ne sont pas simulées. Une alerte chronologique demande une source ; elle ne retire pas automatiquement un savoir.

Exemples d’attentes d’absence dans MISSING_HISTORY_EXPECTATIONS.json. Huit dossiers restent ouverts ; ce document n’affirme pas que leur omission était intentionnelle et fonctionnelle. Le rapport NEW_TAG_TECH_REVIEW.json couvre les 93 nouveaux TAGs, y compris les noyaux politiques approuvés, sans aucune intervention territoriale.
