# Contrôle ciblé MAP-2R — à effectuer par le joueur

Nouvelle partie au1erjanvier1776 avec le mod courant. Ce plan n’est pas un résultat moteur.

1. Vérifier quatre pays distincts ANH,ABG,AKT,AZR : noms Dessau,Bernbourg,Köthen,Zerbst, carte politique et sélection jouable. Les armes ascaniennes communes sont provisoires.
2. Vérifier les souverains historiques et l’absence des personnages ANH de1836 ou de doubles monarques. Aucun nouveau pays ne doit être un sujet automatique de Dessau.
3. Vérifier population et profils : ANH91513,ABG12603,AKT18083,AZR30687. Ce sont des chiffres techniques, pas des objectifs démographiques historiques. HLB doit rester9206.
4. Vérifier capitales valides dans STATE_ANHALT, sans déduire de la position de Magdebourg ou de la ferme la position historique des quatre résidences. Vérifier accès au marché, subsistance, ressources partagées et infrastructures des nouveaux petits États.
5. Vérifier bloc impérial, journal, droits de restitution et absence de nouveaux électeurs ou villes libres pour ABG/AKT/AZR. Tester une restitution sans annexion globale à Dessau.
6. Vérifier que les bâtiments, PM, propriétaires et armées de l’ancien ANH/PRU sont conservés. Les nouveaux pays n’ont pas reçu d’industrie ou d’armée artificielle ; leur viabilité économique reste à observer.
7. Vérifier le mode carte impérial et la carte du journal ; l’étendue impériale totale doit être inchangée. Le locator agricole a seulement changé de RGB de référence, pas de position.
8. Contrôler que Jever, Emden, OLD–HLB, Eutin/Schwartau, Erfurt–Eichsfeld et les autres lots acceptés restent inchangés. Jever encore OLD est une anomalie ouverte explicitement documentée.
9. Laisser passer un mois et vérifier le hook impérial, budgets, pays existants, cartes et erreurs nouvelles. Ne qualifier PASS_RUNTIME_USER_VALIDATED que les points effectivement inspectés après retour explicite du joueur.

Ne pas considérer une exécution statique ou l’ouverture d’un rapport comme un test de chargement du jeu.
