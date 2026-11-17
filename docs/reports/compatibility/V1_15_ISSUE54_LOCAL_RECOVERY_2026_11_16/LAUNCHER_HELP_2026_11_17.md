# Ouverture de l'assistant — 17 novembre 2026

La capture fournie par le joueur montre que les deux lignes du fichier batch ont été saisies dans Windows PowerShell 5.1. `@echo off`, `start ""` et `%~dp0` n'ont pas le même sens dans cet interpréteur ; les erreurs affichées ne démontrent pas une panne du mod.

L'assistant a été relancé directement avec le PowerShell 7 déjà installé, en mode STA, sans changement de règle d'exécution. La commande hôte attend sa fermeture pour garder son processus disponible. Le contrôle préalable des entrées a réussi. Un reçu `MANUAL_…/CONTROL1/LAUNCH.json` atteste le lancement du premier passage isolé à `2026-11-16T23:47:05.1769758Z`, processus 35676, avec les empreintes attendues du GUI témoin, de l'exécutable et de la sauvegarde. Cela n'est pas encore une mesure de fluidité ni une validation humaine du correctif.

Un raccourci `OUVRIR_ASSISTANT_TEST.lnk` a été créé dans ce dossier et relu pour vérifier sa cible existante, ses arguments et son dossier de travail. Il exécute le script directement ; aucun contenu de fichier n'est à coller dans un terminal. Le guide a été précisé. Le raccourci n'a pas été relancé pendant la session déjà ouverte, pour éviter un deuxième assistant.

Les fichiers du mod, les trois fichiers du chantier russe, l'index Git et le code de l'assistant n'ont pas été modifiés par cette correction du relais. Le jeu d'essai déjà lancé est laissé au joueur. Les résultats seront à lire dans le sous-dossier MANUAL correspondant.
