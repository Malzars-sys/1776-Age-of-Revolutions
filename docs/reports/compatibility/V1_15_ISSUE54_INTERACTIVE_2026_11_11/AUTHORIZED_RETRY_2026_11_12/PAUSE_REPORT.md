# Issue #54 — pause demandée le 12 novembre 2026

Les essais sont arrêtés sur demande explicite du mainteneur : « met les test en pause je doit partir ». Aucune reprise automatique.

Trois passages contrôlés ont été réalisés : A1 (interface actuelle), B1 et B2 (interface vanilla, mêmes technologies). Quinze captures CPU de quinze secondes ont été obtenues dans les états d’interface réellement observés : carte en pause, production, militaire, société et déplacement unique de 140 px dans société. Les captures de calibration antérieures sont conservées et exclues de la comparaison contrôlée. A2 a été lancé, mais aucune mesure A2 n’a été faite avant la pause ; le processus d’essai a été arrêté.

Les captures FPS natives sont des lectures visuelles ponctuelles, pas des moyennes continues ni des temps de trame. L’écart provisoire après les captures stationnaires est 8/9/8 FPS en A1 contre environ 30/42/27 en B1 et B2 (production/militaire/société). Cela demande le retour A2 avant toute conclusion répétée complète. Le CPU total du processus est enregistré séparément dans CAPTURE_SUMMARIES.json ; une charge CPU plus basse ne signifie pas une interface plus rapide.

Même exécutable Steam 1.15.1, même profil isolé, même sauvegarde française du 1er janvier 1776, même résolution/réglages. Le lancement direct présente un échec Steam API ; la configuration effective des DLC doit encore être comparée dans les journaux archivés. Ne pas présenter ce test comme une reproduction tous DLC. Aucun benchmark CPU de démarrage ajouté.

Correction de la note de manipulation : le réglage choisi dans Contrôles était « ignorer le curseur » pour le zoom, et non la désactivation du défilement aux bords. Le cadrage a été établi par rechargement de la sauvegarde, puis vérifié visuellement avant/après chaque passage contrôlé. Le réglage et ses empreintes sont conservés ; ne pas modifier un seul bras à la reprise.

Les deux expressions ont été simplifiées seulement dans C_simplified_gui, avec les contrôles statiques précédents conservés ; C n’a pas été testé au moteur. Aucun correctif de performance n’est installé dans le mod normal. B retire tout le fichier GUI et ne permet pas d’attribuer le gain aux seules expressions.

Prochaine action autorisée après retour du mainteneur : reprendre uniquement A2 avec le même profil et la même sauvegarde ; conserver la tentative A2 interrompue et créer un nouveau reçu de lancement. Archiver le marqueur d’arrêt avant le nouveau lancement. Terminer ensuite les contrôles des DLC et de conservation, puis publier le bilan A/B complet. Le vérificateur verify_results.py est préparé mais non exécuté ; il attend vingt captures et devra distinguer la tentative A2 interrompue de sa reprise. Aucun contrôle final ne doit être déclaré réussi avant exécution.
