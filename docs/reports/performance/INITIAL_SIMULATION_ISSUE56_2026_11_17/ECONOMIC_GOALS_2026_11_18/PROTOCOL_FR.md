# Issue #56 — objectifs IA économiques, reprise du 18 novembre 2026

Essais sur le PC Windows local, laboratoire externe réutilisé :
`C:/Users/simeo/AppData/Local/Temp/aor56_ai_20261117`.

Même exécutable Steam 1.15.1, aucun DLC de gameplay, même runtime figé avec COMPACT, mêmes réglages et interface de mesure, vitesse 5 et arbre technologique fermé. L’installation canonique locale 1.15.0 avec DLC reste distincte et n’est pas utilisée pour ces mesures.

Ordre préparé : **ECN1 normal → EXB1 sans extension → EXB2 sans extension → ECN2 normal**. Ce sont des prises à exécuter, pas des résultats acquis. La variante supprime uniquement les 400 blocs natifs `ai_goal` de type `expand_production_buildings` dans une copie de S0 ; les 646 contrôleurs restent actifs. Les variantes et sources déjà préparées sont réutilisées après vérification de leurs empreintes.

Avant simulation : sauvegarde native en pause, contrôle des identités, flags, types et nombres d’objectifs de chaque contrôleur, plus empreinte des autres blocs d’objectifs. Après mesure : nouvelle sauvegarde et contrôle de persistance du traitement. Aucun pays, POP, bâtiment, marché, réglage économique ou script historique n’est supprimé.

Mesures : bornes DAY natives du 2 janvier aux 16 janvier, 30 janvier et 27 février, soit 14/28/56 jours selon le calendrier moteur de 365 jours. Heure native du producteur, jamais arrivée tamponnée du journal. CPU/RAM et CPU par thread échantillonnés à environ 500 ms. Première journée partielle, préparation, menus, pauses et reprise supplémentaire pour vider le journal exclus. Profilage Legacy désactivé pendant les fenêtres.

Le précédent GOAL_EXPAND1 interrompu ne possède pas de preuve POST : son chargement est attesté, mais il ne sera pas présenté comme une ablation de performance validée. Les anciennes séries IA sont conservées avec leurs propres témoins ; aucune comparaison transversale entre 155, 122 secondes et une nouvelle référence ne sera assimilée à un gain.

Si l’extension ne produit pas un signal substantiel et reproductible, choisir une seule autre catégorie économique, en priorité la sélection des méthodes de production. Vérifier sa désactivation native avant toute conclusion. Les retraits d’objectifs modifient les décisions de gameplay : ils ne constituent pas une optimisation à intégrer.

Référence vanilla préparée : même exécutable, DLC, réglages et instrumentation, source France du 1er janvier 1836 préservée (`VANILLA1`), runtime du mod absent. VAN_ON2 et VAN_OFF2 doivent mesurer la même sauvegarde avec flags vérifiés. Monde, date, population et nombre de pays diffèrent de 1776 : référence supplémentaire, pas témoin équivalent du mod.

Préservation : nouvelle baseline de la mission dans `ECONOMIC_PRESERVATION_BEFORE_20261118.json`, incluant les 2 996 fichiers du mod, la copie figée, le profil normal actuel, les anciens rapports/outils et les références. Les sept fichiers normaux modifiés pendant l’interruption précédente ont été préservés sans restauration ; la base courante du lanceur est `93e44a0dcf07dffc007762903cc3077367d951923589f6a48cac01bc2b3b7620`. Aucun Git d’écriture et aucun changement de sécurité Windows.
