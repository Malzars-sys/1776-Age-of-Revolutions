# Limites et tests non effectués

- Les définitions, champs et effets sont fondés sur les scripts installés. Leur chargement par le binaire n’a pas été observé pendant cette mission.
- Aucun champ de masquage des types n’a été retenu. Le doublon est supprimé dans les définitions ; les deux nouveaux types peuvent apparaître dans la table même sans aucun pays les utilisant.
- Aucun champ hypothétique `can_be_annexed` n’est inventé. Les protections combinent champs natifs et gardes scriptées, dont les chemins automatiques doivent être testés.
- `join_overlord_wars=yes` suit le comportement moteur. Le cas où le suzerain ne fait que soutenir un autre initiateur/cible peut différer. Le système existant des cercles vérifie les alliances avant de rajouter des soutiens ; aucun nouvel appel militaire parallèle n’est ajouté.
- Le désir de liberté est natif ; la contestation reste soumise aux règles natives et au coup de sécession conservé. Les modifications d’un pacte, d’un marché ou de l’autonomie peuvent avoir des effets secondaires non modélisés.
- Aucun effet direct de changement de suzerain non vérifié n’est inventé. Le prototype utilise indépendance puis pacte, ce qui n’offre pas de rollback complet garanti.
- L’unification par pays et les buts de guerre peuvent avoir des traitements codés côté moteur. Les protections statiques ne garantissent pas toutes les exceptions, traités, événements d’autres mods ou commandes console.
- Le titre électoral dépend du trigger commun et d’effets autorisés. Les futurs changements de statut devront utiliser l’API de synchronisation ; aucun tick quotidien ne surveille arbitrairement toutes les lois.
- Les sauvegardes déjà entrées dans l’ancienne centralisation ne sont pas certifiées compatibles. Un alias de pacte ne garantit pas la migration de tout identifiant interne retiré. Ne pas charger une sauvegarde précieuse sans copie ; les essais proposés utilisent une nouvelle partie.
- Le compagnon n’a pas été activé et aucune simulation d’un mois n’a été exécutée. Les drapeaux de diagnostic et les modèles Python ne constituent pas une preuve moteur.

Les dix échecs des anciennes suites sont identiques à ceux archivés sous MAP2R/UNIT_TESTS.json. Les anciennes baselines ne sont pas modifiées ; les44 doublons RGB et12 références invalides restent des problèmes de données préexistants.
