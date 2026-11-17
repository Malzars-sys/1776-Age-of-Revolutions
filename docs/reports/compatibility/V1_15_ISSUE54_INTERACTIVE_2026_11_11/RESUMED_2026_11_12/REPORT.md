# Issue 54 — reprise interactive du 12 novembre 2026

> Mise à jour : la comparaison A1–B1–B2–A2 a ensuite été menée à terme, avec vingt captures UI et 44/44 contrôles techniques. Voir le [bilan mesuré](../AUTHORIZED_RETRY_2026_11_12/REPORT.md). Aucun correctif intégré ; C reste non testé au moteur. Le statut et les faits ci-dessous décrivent la tentative antérieure conservée.

Statut : **comparaison A/B non mesurée, investigation ouverte**. Aucun gain de performance ni correctif validé n'est annoncé.

## Ce qui a réellement fonctionné

L'interface Windows autorisée `@oai/sky` a permis d'énumérer les fenêtres, de lancer le jeu, de capturer le menu et d'utiliser plusieurs commandes à la souris. Une session Steam 1.15.1, révision `7a630cdf29e`, a atteint une France en pause au **1er janvier 1776**, dans le profil A1 isolé. Les technologies et l'installation normale du mod n'ont pas été modifiées pour cette reprise.

Le lancement direct signalait un échec d'initialisation Steam. Le lancement depuis les interfaces Steam puis Paradox a utilisé le même exécutable et le dossier utilisateur A1 ; ce nouvel essai ne présentait plus cet avertissement dans son journal courant. Ces deux routes de lancement ne constituent pas deux bras comparables et sont exclues de tout résultat A/B. Le masque DLC effectivement monté par la route Steam reste à figer avant une série comparative.

Une perte de capture « FrameArrived timed out » a été observée pendant la première initialisation du monde en plein écran. Plus tard, la carte a été capturable après passage en mode fenêtré. Cela ne démontre ni la cause de cette perte de capture ni une amélioration des performances du jeu.

## Limites constatées

- Les raccourcis envoyés au jeu n'ont pas produit de résultat fiable, y compris pour le menu et la console. Les clics n'ont pas permis d'établir une séquence reproductible d'ouverture de l'arbre et de changement d'onglets. La fenêtre fenêtrée dépassait aussi le haut de l'écran. L'automatisation disponible est donc partielle, insuffisante pour cette mesure contrôlée.
- Le processus Victoria 3 n'était pas visible par l'énumération ordinaire du collecteur exécuté depuis l'outil de commandes. Une variante pouvait lire son propre enfant dans un lancement direct, mais aucune capture n'a été demandée pendant un état de l'arbre établi.
- Le Gestionnaire des tâches a signalé un niveau d'intégrité Windows supérieur à celui du contrôleur. Aucune entrée n'a été envoyée à cette fenêtre, aucune élévation ni méthode de contournement n'a été tentée.
- L'avertissement FPS natif a été vu sur la carte. Les vues de carte, le pointeur et les conditions variaient : ces affichages ne sont pas des relevés comparatifs. `3dstats` est confirmé dans l'interface native, mais n'a pas été activé et vérifié pendant une mesure de l'arbre.
- Les durées d'appels du contrôleur ne sont pas des latences clic-vers-image. Aucune latence d'ouverture, série de temps de trame, capture CPU de l'arbre ou comparaison A/B répétée n'a été obtenue. Aucun nouveau benchmark CPU de démarrage n'a été exécuté.

La demande de liaison des comptes a été laissée au mainteneur. Son premier retour a été suivi d'un arrêt du contrôleur provoqué par Échap ; il a ensuite précisé avoir utilisé Alt-Échap et a autorisé la reprise. Aucune de ces réponses ne constitue une validation moteur du correctif. Lors de la dernière reprise, Victoria 3 n'était plus présent dans l'inventaire des fenêtres et Steam affichait « Jouer ».

## Nettoyage et conservation

Les options de lancement Steam ont été **remises à vide**, leur valeur initiale, et vérifiées dans le champ des propriétés. Voir `STEAM_RESTORATION.json`. Aucun paramètre de confidentialité, compte ou autorisation Windows n'a été changé par l'agent.

L'autosauvegarde copiée pour une tentative de relais s'est révélée être une **Russie de 1870**. Elle n'a pas servi de référence. Ses quatre copies ont été déplacées dans `rejected_inputs` de chaque essai ; le fichier original reste extérieur au laboratoire. Il faut encore créer la sauvegarde française de 1776 commune aux quatre essais.

Les réglages A1 fenêtrés ont été recopiés dans B1, B2 et A2 après contrôle de leurs empreintes, avec sauvegarde de leurs anciens réglages. Leur égalité ne remplace pas une vérification visuelle de la résolution et du masque DLC. Les copies A/B/C restent séparées de l'installation normale.

Le contrôle statique réalisé pendant la reprise avait trouvé **23/25** contrôles réussis : les deux écarts portaient sur les fichiers normaux du lanceur/réglages réécrits par l'application, et sur les réglages A1 devenus différents des trois profils encore inutilisés. Ce résultat historique est conservé dans `STATIC_DURING_HANDOFF.json`, sans le transformer en réussite moteur.

Après alignement des profils, le contrôle final a donné **24/25**, avec la même version d'exécutable, les fichiers A/B/C attendus, les deux expressions et les réglages isolés identiques. Le seul écart restant est la différence binaire de la base du lanceur et des réglages normaux. L'examen complémentaire conserve les **7 playsets**, leurs **11 liens de mods** et leurs **51 liens DLC** ; seul `lastSyncAttemptAt` varie. Les trois valeurs explicites ajoutées aux réglages normaux sont `fullscreen`, écran `0`, VSync `true`. L'autosauvegarde source garde son empreinte. Voir `FINAL_STATIC_20261112.json`, `NORMAL_PRESERVATION_REVIEW.json` et `NORMAL_SETTINGS_DELTA.json`. Aucune ancienne base ni copie complète des réglages n'a été réinstallée par-dessus les données courantes.

Le vérificateur réutilisé conserve des champs décrivant le premier arrêt manuel dans son résultat ; ils concernent cet historique, pas les actions effectuées pendant la reprise. Le relevé courant des capacités est `CAPABILITIES_FINAL.json`.

## Copie diagnostique C

La copie `C_simplified_gui` conserve toutes les définitions technologiques. Seules deux expressions de visibilité dans `gui/tech_tree.gui` ont été simplifiées : suppression de tests redondants et rééquilibrage des arbres booléens. Les profondeurs de parenthèses passent de 44 à 9 et de 45 à 11 ; les appels textuels `GetTechnology` passent de 42 à 40 et de 43 à 42. Le modèle statique compare 584 cas par expression, soit 1 168 cas, sans divergence dans son périmètre.

Ces contrôles ne prouvent ni le rendu moteur, ni le coût d'évaluation, ni un gain de FPS. C n'a pas été installée comme correctif du mod normal et n'est pas une optimisation vérifiée.

## Prochaine action

Effectuer la série **A1–B1–B2–A2** avec intervention manuelle pour les commandes du jeu et la collecte depuis une session Windows ordinaire. Utiliser le même exécutable, le même masque DLC et la même sauvegarde française en pause. Le protocole concret et les commandes sont dans [MANUAL_TEST_FR.md](MANUAL_TEST_FR.md). Comparer A à C séparément seulement après un A/B exploitable ; ne pas attribuer à ces deux expressions un éventuel gain de B, qui hérite de l'ensemble de l'interface vanilla.

Sources : captures observées dans cette conversation, images conservées dans `images/`, journaux des profils isolés, reçus JSON de cette reprise, `game/gui/debug_menues.gui` et `game/gui/error_deer.gui` de l'exécutable Steam consultés en lecture seule. Toutes les captures en jeu observées dans la conversation n'ont pas été exportées en PNG ; ne pas inventer de pièce jointe correspondante.
