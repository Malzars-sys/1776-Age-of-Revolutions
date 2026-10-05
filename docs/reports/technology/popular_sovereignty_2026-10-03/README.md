# Souveraineté populaire — changements demandés le 3 octobre 2026

Les lois République présidentielle, République parlementaire et Suffrage censitaire sont désormais débloquées par **Souveraineté populaire** (`national_sovereignty`), au lieu de Régime constitutionnel.

Le parent direct **Régime constitutionnel → Constitution libérale** est remplacé par **Souveraineté populaire → Constitution libérale**. Les deux autres parents de Constitution libérale (Droits de l'Homme et Économie classique) sont conservés. Souveraineté populaire conserve ses propres prérequis existants.

Le **Vote des riches** est une autre loi : il n'a pas été modifié.

## Actualisation du contrôle — 6 octobre 2026

La référence de publication est désormais le commit d'assets `731d7955c8947d7cbf4d6f661c14e8a7a0593767`. Cela inclut les icônes déjà approuvées, sans ignorer d'autres différences arbitraires. Les trois fichiers de jeu contiennent exactement les quatre changements de prérequis demandés ; les autres paramètres, les icônes et le Vote des riches restent inchangés par rapport à ce commit.

Le contrôle vérifie les accolades, les définitions en double, les prérequis exacts et l'arbre complet de 292 technologies, sans parent manquant ni cycle. Les 1 275 autres fichiers de jeu suivis dans `common` et `gfx` sont inchangés par rapport à la référence de publication. Le mode de préparation du commit vérifie également que l'index Git contient exactement les sept fichiers de ce lot.

`baseline.json` reste l'archive historique du 3 octobre, sans modification de contenu. Son empreinte est contrôlée en normalisant seulement les fins de ligne Windows/Linux, comme Git. Son ancien résultat de validation est conservé dans la section `historical_validation` de `validation.json` ; il ne décrit pas le dépôt après intégration des assets.

Le validateur est désormais en lecture seule : il affiche un résultat JSON sans réécrire les rapports ni les fichiers de jeu.

- Contrôle actuel : `python tools/validate_popular_sovereignty_changes.py --verify`.
- Contrôle exact de l'index avant commit : `python tools/validate_popular_sovereignty_changes.py --verify --staged`.
- Ancien contrôle strict : `python tools/validate_popular_sovereignty_changes.py --verify-historical`. Son échec après les ajouts d'assets est attendu ; il conserve les exigences historiques et n'est pas le contrôle de publication.

Voir `validation.json` pour les résultats de publication. Ce contrôle reste statique : le rendu en jeu n'a pas été testé. Recharger le jeu pour vérifier les déblocages et les connexions de l'arbre.
