# Publication des assets — 6 octobre 2026

## Périmètre

Intégration de Génie routier et publication de l'ensemble du travail graphique déjà approuvé : icônes, illustrations, raccordements visuels, outils d'export, sources et rapports. Les variantes et propositions non approuvées restent archivées dans la documentation, sans raccordement supplémentaire en jeu.

Le commit exclut les changements de lois et de prérequis liés à la souveraineté populaire. Ils sont conservés dans le dossier de travail.

## Vérification

- 110 textures DDS contrôlées, comprenant 988 niveaux de réduction.
- Stockage natif BGRA, couleurs et transparence vérifiés ; export de Génie routier identique au PNG approuvé.
- Les six fichiers de définitions modifiés ne changent que leurs références d'images ; comparaison structurée avec HEAD.
- Les références visuelles de ces définitions sont présentes dans le mod ou le jeu installé.
- Le portrait encadré du laboratoire est volontairement opaque ; aucune transparence artificielle n'a été ajoutée.
- Aucun lancement du jeu effectué pendant cette publication. Les contrôles sont statiques.

Les avertissements de fin de fichier vide dans les archives et les espaces de contexte du patch de sélection ne sont pas des erreurs de script de jeu ; ces documents historiques restent conservés.

## Reste à faire

Machines de précision conserve son illustration temporaire. Le cuivre et sa mine restent hors du périmètre de cette passe. Cette publication ne prétend donc pas achever toutes les icônes du projet.

Résultat détaillé : [validation.json](validation.json). Le patch `society_visual_only.patch` documente la séparation des seuls raccordements visuels des changements de gameplay.

