# Corrections de finition

Le fichier `HISTORY.patch` est conservé comme patch de préparation initiale, pas comme vérité unique du résultat final. Après installation, la nouvelle définition de gouvernement d’Ellwangen a été corrigée par un patch explicite : succession native `dictatorial` et effets `change_to_dictatorial` / `post_change_to_dictatorial`, à la place du type inexistant `theocratic`. Le générateur reproduit maintenant cette définition correcte. La date précise de naissance non vérifiée a été remplacée avant installation par l’âge approximatif 64, fondé sur l’année 1711 attestée.

`WHITESPACE.patch` retire les seuls espaces nouvellement insérés dans les trois historiques modifiés ; deux lignes héritées demeurent (`pops:2219`, `states:8165` dans cette version). Les contrôles finaux portent sur les fichiers installés et sur le résultat recompilé des mécanismes impériaux, pas sur une absence d’échecs pendant le développement.

Les descriptions manquantes des gouvernements de Baden, Ulm et des principautés Hohenzollern ont été ajoutées avant le checkpoint de la version validée. Le générateur de la première passe a ensuite été corrigé pour conserver ces descriptions lors d’une reproduction future. Cette correction de générateur, comme le présent sous-lot, reste locale et n’est pas prétendue incluse dans le checkpoint antérieur.
