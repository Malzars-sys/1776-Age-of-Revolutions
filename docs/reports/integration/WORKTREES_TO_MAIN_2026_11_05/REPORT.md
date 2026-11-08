# Intégration Massa-Carrare + Map-0 vers le mod principal

Date : 5 novembre 2026. Autorisation : « Fusionne les trois modes. Donc mode principal, Mascarar et Map zéro […] récupérer dans le mode principal tous les changements. »

Destination : `C:/Users/simeo/Documents/Paradox Interactive/Victoria 3/mod/1776_Age_of_Revolutions_fork`, confirmée dans `content_load.json`. Sources conservées : les worktrees Massa-Carrare et Map-0. Aucune opération Git d'écriture, aucune modification du vanilla ou du lanceur, aucune publication Steam.

## Contenu réuni

Plan initial résolu : **622 fichiers**, dont **17 fichiers de jeu**, 562 nouveaux et 60 mis à jour ; environ 415 Mo, principalement des preuves et rapports. Les 35 modifications fonctionnelles déjà propres au principal sont préservées ; les trois fichiers partagés de bâtiments/régions sont fusionnés par changements non chevauchants, avec cinq segments modifiés du principal explicitement conservés. Les autres éléments restent en place.

Massa-Carrare apporte les recherches complémentaires et les livraisons prussiennes, leurs historiques, populations, références de carte, locators, registre et dérivés impériaux, outils et suivis. Les deux modifications fonctionnelles de Map-0 sont déjà dépassées par les corrections validées : intégration complète du Luxembourg à BEO et représentation des Trois Ligues par SWI. Leur ancien état n'est pas réappliqué ; les fichiers et écarts Map-0 restent conservés dans les sources et le dossier d'audit. Les autres différences Map-0 sont des variations de fins de ligne ou du contenu déjà repris dans l'historique du principal.

Sept conflits examinés et résolus : cinq vues/état SERG cumulés, puis deux anciens historiques Map-0. Le suivi Massa contient tous les événements du principal comme préfixe exact ; les compléments Carrare/Zatta et Prusse sont ajoutés sans changer les anciens reçus. La progression SERG demeure **93/235, 39,57 %, 32/81**. L'événement technique **SERG-RM-0072** ne donne aucun point et ne valide aucun essai moteur. Le suivi WORLD et les chantiers technologie, économie, fortifications, génie, France et États-Unis ne sont pas réinitialisés.

## Vérification et reprise du jeu

Vérifications préalables réussies : syntaxe des scripts modifiés, JSON et outils Python, localisation avec BOM, conservation des segments propres au principal, absence de conflit restant. Les résultats après déploiement sont consignés dans VALIDATION.json, TEST_RESULTS.json et FINAL_CHECKS.json.

**Intégration terminée et vérifiée dans la copie principale : 626 fichiers au total avec les quatre pièces d'audit initiales, dont 17 fichiers de jeu ; 60 préimages sauvegardées.**

**34/34 contrôles de conservation réussis ; 73 tests ciblés exécutés, 72 réussis et un ancien contrôle exclu, aucun échec ni erreur. Validateur SERG PASS ; 9/9 contrôles finaux et vérification des différences PASS.** Les 11 erreurs de référence et 14 clés de références dupliquées préexistantes sont inchangées ; aucun nouvel écart de ce type. Les populations mondiales et leurs profils, les unités du principal, les niveaux de bâtiments et les données de pays sont conservés. Les déclarations de bâtiments combinent exactement les deltas prussiens et les changements propres au principal. Les cinq fichiers canoniques WORLD vérifiés sont inchangés.

Les huit cellules NET, les noyaux PRU/SAX et le registre à 599 titres sont présents dans la copie effectivement chargée. Les trois index et fichiers HEAD Git sont inchangés. Les deux livraisons d'agents sont conservées ; les caches ont été exclus de l'intégration. Aucun lancement du moteur ni reçu humain nouveau.

Les anciennes preuves sont des résultats datés de leurs livraisons ; leur intégration ne constitue pas une nouvelle attestation humaine. Les nouvelles installations prussiennes restent en attente du joueur. Les sauvegardes des fichiers remplacés et les empreintes sont conservées dans ce dossier d'intégration.

**Après l'intégration : fermer puis relancer Victoria 3 et démarrer une nouvelle partie en 1776.** La session déjà ouverte et les anciennes sauvegardes ne rechargent pas les nouveaux historiques de départ. Ensuite appliquer [le protocole groupé prussien](../../map/SERG_CLOSURE/WESTERN_RESERVES_ARBITRATION_2026_11_05/PLAYER_TEST_PROTOCOL_GROUPED.md). Les villes absentes de la carte ne sont pas exigées comme lieux de recherche ; contrôler les propriétaires et les formes avec les repères natifs visibles.
