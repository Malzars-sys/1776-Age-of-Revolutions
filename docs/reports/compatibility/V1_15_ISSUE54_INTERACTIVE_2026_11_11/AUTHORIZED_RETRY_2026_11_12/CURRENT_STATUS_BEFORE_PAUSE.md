# État du 12 novembre 2026 — reprise interactive, A/B non mesuré

Le contrôle Windows autorisé a atteint une France en pause au 1er janvier 1776,
mais les commandes du jeu et les compteurs CPU n'ont pas permis une série A/B fiable.
Aucun benchmark CPU de démarrage supplémentaire n'a été réalisé.
Les options Steam normales ont été remises à vide et vérifiées.
Les copies d'autosauvegarde de Russie 1870 sont archivées dans les dossiers
rejected_inputs des quatre essais : ne pas les utiliser comme référence 1776.

Le protocole courant est runtime_ui_controlled/MANUAL_TEST_FR.md.
Créer d'abord TECHPERF54 avec la France en 1776 et effectuer A1–B1–B2–A2
sur cette même sauvegarde, le même exécutable et le même masque DLC.
C_simplified_gui reste un diagnostic statique non validé par le moteur.

## Historique précédent conservé

# Issue 54 — contrôle interactif arrêté, relais manuel (12 novembre 2026)

L'interface Windows officielle `@oai/sky` via l'outil JavaScript est disponible :
initialisation et inventaire des fenêtres ont réussi. Cependant, la première
capture demandée pour Victoria 3 montrait une autre application au premier
plan. Aucune entrée clavier/souris n'a été envoyée. À ta demande explicite,
l'essai interactif a été arrêté ; aucune fenêtre Victoria 3 ne restait ensuite.

**Aucun nouvel essai CPU de démarrage et aucune mesure de l'arbre, de FPS,
de frame time ou de comparaison A/B n'ont été réalisés.**

Le protocole manuel minimal est `runtime_ui_controlled/MANUAL_TEST.md`, avec
les profils isolés A1–B1–B2–A2 et `UI_RESULTS_TO_FILL.csv` laissé NON MESURÉ.
Les playsets et le mod normaux sont préservés. Le même exécutable Steam 1.15.1
est épinglé pour tous les essais ; la série locale 1.15.0 + DLC reste distincte.
Le lancement direct confirme le montage de A mais conserve l'avertissement
sur l'initialisation de l'API Steam ; ce n'est pas une reproduction authentifiée.

La copie `C_simplified_gui` ne change que les deux expressions de visibilité.
Le modèle booléen conserve leurs résultats sur 1 168 cas, sans changer les
technologies. Elle n'a pas été lancée ou mesurée et n'est pas un correctif validé.
Les anciens rapports et ZIP restent conservés comme historiques.
