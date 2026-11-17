# Reprendre les essais sans commande technique

Dans l'Explorateur de fichiers Windows, double-cliquer sur **OUVRIR_ASSISTANT_TEST.lnk** dans ce dossier. L'assistant possède deux boutons et indique la vue à préparer. Si sa fenêtre est déjà ouverte, utiliser cette fenêtre. Aucun changement des options Steam ou des playsets n'est nécessaire.

Le raccourci se lance directement : aucun texte à copier dans PowerShell. Le fichier `LANCER_LES_TESTS.cmd` reste une autre possibilité, à exécuter lui aussi par double-clic dans l'Explorateur ; son contenu n'est pas une commande PowerShell.

1. Cliquer **Lancer ce passage isolé**. Attendre le menu du jeu, puis cliquer **Continuer** : Royaume de France, 1er janvier 1776.
2. Garder la partie en pause. Attendre trente secondes après chargement. Pour la première vue, laisser simplement la carte affichée.
3. Revenir à l'assistant. Si un compteur FPS est visible en bas à droite du jeu, saisir la valeur observée ; sinon laisser le champ vide.
4. Cliquer **Mesurer cette vue pendant 15 secondes**, puis cliquer dans le jeu pendant le délai de cinq secondes. L'assistant se masque pendant environ vingt secondes et revient après la collecte. Le jeu reste ouvert pendant cette mesure.
5. Suivre la vue suivante indiquée : Production, Militaire, Société, puis un glissement dans Société. L'assistant ferme son propre jeu et propose le passage suivant. La série comporte quatre passages : témoin, COMPACT, COMPACT, témoin.

Les captures CPU sont enregistrées automatiquement dans un nouveau sous-dossier **MANUAL_…** de ce dossier. Elles déclarent explicitement que la vue a été préparée par vous ; elles ne prétendent pas contenir une vérification visuelle automatique. Le nombre FPS saisi reste une observation ponctuelle, pas une moyenne. Les délais exacts d'ouverture restent non mesurés.

Le bouton **Fermer l'assistant** termine uniquement le jeu lancé par cet assistant. Les sauvegardes, réglages et playsets habituels restent dans leur emplacement normal. La sauvegarde utilisée ici est une copie du laboratoire. Aucun correctif n'est installé dans le mod principal.

Une fois la série terminée, revenir dans cette conversation et indiquer simplement **« Les quatre passages sont terminés »**. Les résultats seront alors analysés depuis votre PC.

Les entrées et la syntaxe de l'assistant ont été contrôlées et son mode aperçu se ferme sans erreur. Sa séquence complète de collecte manuelle attend encore une première utilisation ; aucun résultat d'essai utilisateur n'est déjà revendiqué.

Le défaut de fermeture au premier clic Mesurer a été corrigé le 17 novembre. Un test sans Victoria 3 reproduit la panne de l'ancien fonctionnement ; le fonctionnement corrigé enregistre quinze secondes de CPU, réaffiche l'assistant et conserve le processus observé ouvert. Ces relevés de diagnostic sont séparés des mesures du jeu. La première tentative interrompue reste conservée et doit être reprise depuis le début.
