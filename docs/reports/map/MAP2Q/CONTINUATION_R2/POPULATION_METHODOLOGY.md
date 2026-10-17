# MAP-2Q-R2 — Estimation installée : 7 600 habitants

**Statut démographique : estimation historique approximative acceptée par le joueur, pas recensement de 1776.** Fourchette de travail : **6 500–9 000**. Elle n'est ni un intervalle statistique de confiance ni une limite prouvée de la population réelle.

Le joueur avait d'abord choisi le maintien de 11 325, puis a explicitement corrigé sa réponse : « Prends l'autre réponse ». L'autre option était l'installation de 7 600 habitants pour les 31 cellules figées, avec l'incertitude de périmètre annoncée. Cette dernière réponse est celle appliquée.

## Périmètre et non-double comptage

La cible porte sur **HLB dans STATE_SCHLESWIG_HOLSTEIN**, noyau d'Eutin déjà créé par MAP-2Q : 19 cellules précédemment LUB et 12 précédemment HOL. Aucune frontière n'est modifiée dans R2. Le noyau est traité comme une généralisation de la ville et de l'Amt ; ce rapprochement est une hypothèse acceptée, non une correspondance exhaustive de chaque village ou propriété.

La liste AGGSH distingue notamment le Stiftsdistrikt autour de Bosau, le Kirchspieldistrikt autour d'Eutin, Rothensande et Redingsdorf/Bujendorf. Ces secteurs éclairent le noyau représenté sur Reilly. Les désignations sont toutefois postérieures à 1776 et la couverture des bords des 31 cellules n'est pas vérifiée village par village. Aucune aire de pixels n'est convertie en habitants pour établir la cible historique.

Schwartau/Kaltenhof, Großvogtei et Collegiatstift ne sont pas ajoutés au calcul central. Benz est une ligne allodiale distincte dans l'AGGSH : son inclusion spatiale et juridique exacte dans le noyau n'est pas suffisamment contrôlée pour ajouter ses 254 habitants de 1819. Leur traitement demeure ouvert et ne déclenche aucun transfert chez les voisins. L'incertitude des petites portions incluses ou omises n'est pas résolue par un coefficient de surface arbitraire.

La ville et les quatre districts sont des lignes disjointes dans l'agrégation AGGSH utilisée. On n'ajoute **pas** simultanément un total de Kohli à ces détails. Les listes des chapitres ne sont pas additionnées à celles de l'Amt.

## Ville : interpolation autorisée

Deux valeurs urbaines rapportées : environ 2 000 en 1755 et 2 283 en 1791. Sous l'hypothèse d'une ville comparable, sans preuve d'un changement majeur de périmètre entre ces deux mentions :

`Ville_1776 = 2000 + (2283 - 2000) × (1776 - 1755) / (1791 - 1755) = 2165,08`.

Centre de travail arrondi : **2 165**. Plage de travail : **2 000–2 300**, qui tient compte du premier chiffre arrondi et de la comparabilité imparfaite. Confiance moyenne sous cette hypothèse, pas haute. Les jours et mois des observations ne sont pas connus ; la valeur interpolée ne prétend pas certifier le 1er janvier à l'habitant près. Les dénombrements urbains de 1819 sont uniquement des contrôles postérieurs, pas des habitants ajoutés à la ville de 1776.

## Amt rural : interpolation entre deux bases locales

Base antérieure : **5 218 vers 1769**, estimation de Hennings fondée sur une densité locale supposée, donc moins solide qu'un relevé nominatif. Base postérieure : **7 070 en 1819**, somme des quatre districts de l'AGGSH. On suppose l'agrégat rural assez comparable pour une approximation, sans déclarer cette comparabilité juridiquement démontrée.

Interpolation géométrique centrale :

`Amt_1776 = 5218 × (7070 / 5218)^(7 / 50) = 5444,68`.

Sensibilité à une interpolation linéaire :

`5218 + (7070 - 5218) × 7 / 50 = 5477,28`.

Le total ville + rural vaut respectivement **7 609,76** et **7 642,36**. Le choix installé est arrondi à la centaine : **7 600**. Le calcul géométrique correspond à un lissage entre ces deux bases locales, **pas à un taux historiquement observé**. L'écart de 32,60 entre modèles ne mesure pas l'incertitude réelle, bien plus grande.

L'usage alternatif de 6 824 de Kohli modifierait le résultat, mais mélanger cette ventilation non réconciliée avec les détails de l'AGGSH serait trompeur. Kohli reste un contrôle contradictoire explicite, pas un chiffre à moyenner.

## Fourchette et secteurs

L'enveloppe 6 500–9 000 est une **sensibilité de scénario choisie**, pas une observation. Une variation illustrative de ±20 % de l'estimation rurale initiale, non issue d'une erreur publiée par Hennings, donne environ 4 494–6 369 habitants ruraux avec le modèle géométrique et l'ancrage de 1819 fixe. Le dossier retient la plage grossière arrondie **4 500–6 700**, élargie vers le haut pour la méthode et les portions de périmètre mal identifiées. Avec 2 000–2 300 urbains, l'enveloppe de travail arrondie est 6 500–9 000. Les ±20 % ne sont pas une précision certifiée de la source ; ils rendent visible la dépendance du résultat à une hypothèse faible.

Après arrondi du total, 2 165 sont attribués au terme urbain du modèle, et le reliquat rural est **5 435**. Pour fournir une lecture par secteur, ce reliquat est ventilé proportionnellement aux poids AGGSH de 1819, par plus forts restes : Stiftsdistrikt **1 618**, Kirchspieldistrikt **1 700**, Rothensander Ort **1 800**, Redingsdorf **317**. Ce détail est un **modèle conditionnel de poids stables**, non une population observée en 1776 ; il n'est pas écrit comme de nouveaux blocs géographiques dans le jeu. Les colonnes de bornes du CSV suivent la même convention illustrative. Il ne faut pas additionner à nouveau les sous-totaux avec leurs détails.

Les postes sans estimation défendable restent vides dans les colonnes 1776 du CSV, jamais mis à zéro. Les chiffres de 1819 y sont clairement datés.

## Écriture dans le mod et bilan mondial

Seul le fichier `common/history/pops/00_west_europe.txt` est changé à l'exécution : six valeurs `size` de HLB. Les quatre profils culture/religion sont conservés. Leurs totaux sont réduits proportionnellement, avec arrondi entier par plus forts restes, puis ventilés entre les blocs originaux identiques. Aucun changement de culture, religion, population voisine, bâtiment, propriétaire économique, unité, infrastructure, loi, province ou registre impérial.

Avant : **11 325** ; après : **7 600** ; écart : **−3 725**. Monde recalculé à partir des historiques : **835 804 980 → 835 801 255**. Aucune compensation artificielle dans HOL, LUB, OLD ou un autre pays. Les contrôles comparent l'intégralité du delta autorisé, et non un total mondial figé.

Les fichiers actuels de validation Q sont mis à jour, leurs versions précédentes archivées ici sous `PRE_R2_`. Les baselines Q et R1 et les autres lots ne sont pas réécrits. Les anciens CSV du premier Q décrivent sa phase technique initiale ; les tableaux R2 donnent l'état démographique courant.

## Résultats des vérifications

**31/31 contrôles R2, 167/167 contrôles cumulatifs Q et 11/11 tests ciblés réussis.** Les tests négatifs rejettent une compensation dans un pays voisin, un habitant supplémentaire non déclaré et une seconde application de la même correction. Les deux tableaux CSV ont été produits et relus avec des cellules typées, puis contrôlés visuellement. Les inconnues restent vides. Les catégories culturelles et religieuses changent de moins d'un habitant par rapport à la proportion théorique avant arrondi.

Les seuls changements runtime sont les six valeurs `size` de HLB dans l'historique de population. Le validateur Q et les outils/tests R2 sont les changements de code de cette phase ; la documentation courante Q et la règle permanente portent la nouvelle application. Aucune écriture dans HEAD ou l'index, aucun commit, merge ou push.

Les 44 doublons RGB et 12 références invalides déjà connus sont identiques avant/après. Les six anciens échecs de snapshots d'autres lots ne sont pas déclarés réparés. Aucun lancement du jeu ni certification historique exhaustive ; consulter `UNRESOLVED.md` pour le contrôle en nouvelle partie et les secteurs territoriaux encore incomplets.
