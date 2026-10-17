# Prototype de succession — isolé

Le mod principal bloque l’installation d’un nouvel empereur lorsqu’existent des sujets impériaux natifs et pose `aor1776_hre_centralized_transfer_pending`. Il ne libère pas le candidat dans cet état bloqué. Sans ces dépendances, il appelle la même implémentation électorale préexistante. Le hook de décès n’est plus supprimé par le marqueur d’ancienne unification.

Le compagnon ajoute un scénario volontairement limité : ANH comme État impérial et KPF comme électorat sous l’empereur courant. Aucun pays déjà sujet non impérial n’est converti par ce scénario. Il faut une nouvelle partie, le compagnon explicitement activé et un armement console.

Précontrôles : ancien empereur indépendant, nouveau candidat légitime et non sujet étranger, paix, absence de dépendance cyclique connue et éligibilité des sujets concernés. Les seuls sujets sélectionnés sont les deux nouveaux types directement dépendants de l’ancien empereur.

Ordre : mémoriser types et désir de liberté ; libérer le candidat s’il fait partie des sujets sélectionnés ; appeler le mécanisme existant de changement de titulaire/bloc ; si sa réussite est observée par les conditions scriptées, recréer uniquement ces dépendances sous le nouveau titulaire, restaurer le désir de liberté et synchroniser les types ; laisser les unions et dépendances étrangères hors sélection. L’ancien titulaire n’est soumis que s’il appartient à la liste pure autorisée ; AUS et PRU n’en font pas partie.

En cas d’échec de création du bloc, tentative de restauration du seul candidat libéré. **Ce n’est pas une transaction moteur garantie** : un bloc partiellement modifié, les marchés, modificateurs de pactes et dépendances indirectes exigent des tests. Les variables `...test_completed` / `...test_failed` ne sont pas des certificats.

Les cinq modèles Python testent le graphe attendu, les cycles et la conservation de données fictives. Ils n’exécutent pas ces scripts dans Victoria3 et ne prouvent pas le transfert natif. L’ouverture à une réforme générale reste bloquée.
