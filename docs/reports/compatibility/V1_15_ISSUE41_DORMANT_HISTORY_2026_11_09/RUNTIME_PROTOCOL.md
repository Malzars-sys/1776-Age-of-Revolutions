# Vérification ciblée — mission 41

Cette livraison modifie uniquement les outils d'audit et leurs preuves. Elle ne nécessite ni création d'un pays absent, ni concession de lois/technologies, ni manipulation de sauvegarde pour tester un correctif de gameplay.

Lors du prochain essai moteur déjà prévu pour le hotfix :

1. Noter version du jeu, configuration DLC et état exact des fichiers du mod ; démarrer une nouvelle partie 1776.
2. Observer le chargement et les premiers jours avec la Russie ou la Pologne-Lituanie, puis effectuer la sauvegarde/reprise prévue par les autres protocoles. Ne pas inventer de durée testée ou de résultat.
3. Dans les nouveaux logs, relever intégralement toute erreur mentionnant `c:BKH`, `c:MNL`, `c:SVN`, `c:TKI` ou les quatre fichiers d'histoire concernés. Distinguer la ligne et la chaîne d'appel : un consommateur gouvernement/IA n'est pas le bloc d'histoire optionnel.
4. Si un message est effectivement produit par l'un de ces blocs, conserver la preuve et réexaminer la qualification avant toute correction. L'absence d'une cible dans les scripts ne prouve pas seule une erreur moteur ; l'absence d'un message ne valide pas toute la carte.

Aucun résultat moteur n'est fourni ici. Le contrôle statique n'acquiert pas le statut `PASS_RUNTIME_USER_VALIDATED`. La fermeture de 41 relève de la revue de cette qualification ; les validations de fonctionnement des parents 24/25 demeurent indépendantes.
