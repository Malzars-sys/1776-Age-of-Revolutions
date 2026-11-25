# Contrôle du rechargement d’un monde mature

Nouvelle mission explicite du joueur du 17 novembre 2026. Réutiliser le main figé, les sondes DAY et les profils isolés. Les anciens résultats restent historiques et ne sont pas réécrits.

1. MATURE1 repart de la sauvegarde commune France 1776. Vitesse 5 constante, aucune option d’événement. Observer une année environ et vérifier que le débit a rejoint le niveau tardif.
2. Mettre en pause dans le monde mature, sans viser un jour exact. Créer une nouvelle sauvegarde locale isolée S et vérifier son en-tête, sa taille et son empreinte. Garder le fichier intact.
3. Reprendre à vitesse 5 et mesurer le monde mature sans redémarrage. Bornes DAY à S+1 puis +14/+28/+56 jours ; étendre au-delà de 112 jours pour observer la stabilité. Les pauses et la sauvegarde précèdent S+1 et sont exclues.
4. Fermer complètement ce processus possédé. Préparer RELOAD1 et, si possible, RELOAD2 à partir du même fichier S, avec le même runtime, exécutable, DLC et réglages. Lancer chaque jeu dans un nouveau processus, recharger S, sélectionner vitesse 5 avant de reprendre, laisser tourner les sondes au moins 112 jours.
5. Comparer les mêmes dates simulées, les premières fenêtres et les tranches suivantes. Une lenteur seulement immédiate n’est pas assimilée à une lenteur persistante. Le calendrier moteur est de 365 jours. Résolution temporelle <1 seconde, CPU/RAM alignés par la collecte continue.
6. Selon les résultats, choisir une seule ablation suivante, avec priorité au contrôleur mensuel de l’IA des infrastructures, puis au HRE mensuel. Aucune suppression simultanée et aucune intégration de diagnostic dans le mod principal.

Les pauses sont commandées uniquement sur la copie d’essai. Aucun script ne doit intervenir sur une session habituelle. Les playsets et sauvegardes normaux, COMPACT, Russie–Kazakh et les travaux Git existants restent protégés. Aucun Git d’écriture.
