# R9 — Repérage joueur et noms non trouvables

Retour du joueur, 29 octobre 2026 : les noms historiques donnés dans le protocole ne sont pas retrouvés dans la recherche du jeu. Sa capture montre la portion « Uruguay brésilien » près de Buenos Aires, sans étiquette Sacramento visible à cette échelle. Cette observation ne valide pas le placement des hubs, leur rendu ou la desserte maritime.

## Vérification et correction des consignes

Les scripts de noms de Sacramento et Puerto Soledad existent. La sauvegarde moteur initiale du contrôle précédent contient respectivement leurs cinq clés dans `localized_hub_names`, lignes 1934070 et 2044493 du fichier `FINAL_VALIDATION_2026-10-28/FRESH_INITIAL_MELTED.txt`. Cela confirme leur enregistrement, pas leur présence dans l'index de recherche ni une ville visible dans chaque portion partagée.

L'amendement Sacramento partagé avait retiré les locators spécifiques de l'ancienne région indépendante, en conservant les hubs régionaux d'Uruguay. La ville régionale reste sur `x302DDA`, le port sur `xA46ED2`, alors que l'enclave BRZ est `x4E1443`. Le bon placement automatique de ses modèles dans un État partagé reste à vérifier. Un port économique de niveau 1 chargé ne prouve pas l'affichage d'un modèle portuaire dans l'enclave. Ne pas promettre que la recherche « Sacramento » mène à cette portion.

Tabatinga est représenté par une province BRZ dans Pastaza (`x3C0D20`) et ses 74 habitants ; R9-05 n'avait pas ajouté de hub portant ce nom. Le secteur espagnol de Chiloé/Calbuco/Maullín se trouve dans Araucanie, avec son port régional hérité `x553B3F`. La localisation vanilla de ce hub est « Puerto Montt » ; « Chiloé » désignait un secteur de contrôle et non une ville nouvellement nommée. Les noms modernes hérités étaient explicitement reportés dans les rapports R9-04/05.

**Erreur de consigne corrigée :** demander au joueur de chercher quatre villes nommées supposait à tort des objets de carte tous installés et indexés. Chercher d'abord les régions, puis repérer la portion possédée :

| Numéro | Repère documentaire | Région à rechercher | Portion à sélectionner |
| --- | --- | --- | --- |
| 1 | Sacramento | Uruguay | Petite enclave BRZ sur le Río de la Plata, près de Buenos Aires |
| 2 | Tabatinga | Pastaza | Portion BRZ à l'extrémité occidentale du réseau amazonien brésilien |
| 3 | Secteur de Chiloé | Araucanie | Portion SC3 à l'ouest/sud-ouest des territoires huilliches ; hub portuaire hérité |
| 4 | Puerto Soledad | Îles de l’Atlantique Sud | Portion SC4 des Malouines, à l'est de l'extrémité sud du continent |

`R9_REPERES_JOUEUR.png` est un guide dessiné à partir du bitmap et des propriétaires courants, avec vue continentale et quatre agrandissements. Les numéros sont des annotations du guide, pas des objets ajoutés au jeu. Les coordonnées/RGB et empreintes sources sont consignés dans `GEOMETRY_RECEIPT.json`. Les marqueurs sont les proxys de provinces déjà livrés, pas des implantations historiques nouvellement certifiées.

Aucun changement de frontières, population, bâtiments, régions ni locators n'est installé dans ce correctif de repérage. Cela résout la difficulté de localisation du protocole ; cela ne prétend pas résoudre les villes/hubs manquants ou invisibles. Ceux-ci restent une réserve technique explicitement ouverte, à examiner avant toute affirmation de placement valide. Aucune homologation du lot R9-02 ou de la simulation n'est déduite du retour.
