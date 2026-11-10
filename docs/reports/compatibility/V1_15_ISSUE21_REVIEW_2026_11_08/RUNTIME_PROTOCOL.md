# Mission 21 — essais groupés différés

Statut : **PENDING_RUNTIME_USER_VALIDATION**. Ce document prépare la passe demandée ; aucune case n'est un résultat observé.

## Configuration à consigner

- Version et build du moteur, DLC actifs, playset et chemin réel du mod chargé.
- Révision et empreintes de `INSTALLED_FILES.json`. Redémarrer complètement le jeu après installation ; une partie déjà ouverte ne charge pas cette livraison.
- Nouvelle partie 1776, autres mods désactivés pour le test de référence. Conserver les logs produits dans une capture séparée de `LOGS_BEFORE.json`.

## Parcours borné

1. **Chargement et simulation.** Atteindre sélection des pays, partie et premier jour. Simuler une durée mesurée, puis sauvegarder/recharger. Noter pays, dates, durée réelle et erreur ou crash éventuel ; la durée n'est pas présumée réussie.
2. **IA et diplomatie.** Examiner des cibles accessibles et inaccessibles pour conquête, soumission, marché/port et protection. Vérifier les paramètres `TARGET_COUNTRY/TARGET_STATE`, les refus `NOT` et l'absence des anciens appels inconnus. Tester péages et fermeture de détroit avec un détenteur direct, un sujet détenteur et un pays sans détroit. Reprendre les scénarios détaillés des missions 29 et 30 pour leurs effets et valeurs affichées.
3. **Décrets.** Dans des états de compositions différentes, examiner les conditions/poids autour des seuils de cultures primaires 10/30/50/90 %. Les seuils exacts et opérateurs sont ceux de `MIGRATIONS.json` ; les autres lois et conditions restent applicables. Aucun décret ne doit comparer les cultures primaires d'un pays étranger à celles du propriétaire par erreur.
4. **Personnages.** Contrôler souverain, héritier, général, amiral, agitateur et politicien dans leurs pays respectifs. Les rôles `character_role_*` existants doivent continuer à fonctionner. Vérifier la succession industrialiste EIC dans une copie de test éligible, sans changer les pays initiaux pour fabriquer une réussite.
5. **Protection temporaire et exil.** Vérifier le cas d'un personnage initialement mortel protégé durant un événement, sa révocation normale, le fallback après expiration mensuelle, et le cas d'un personnage initialement immortel. L'événement ne doit pas lui retirer sa protection permanente. Tester les pools d'exil avec les scopes, DLC et paramètres natifs requis ; ne pas forcer un événement sans ses scopes sauvegardés.
6. **Navires futurs.** Sur une copie adaptée disposant des technologies et navires nécessaires, évaluer les proportions pays/flotte pour dreadnoughts, destroyers, super-dreadnoughts, sous-marins et porte-avions. Vérifier séparément pré-dreadnoughts du canular et du Potemkine. Conserver les fractions 0,1/0,2 et leurs autres conditions. Les anciennes références de bâtiments navals documentées en dépendance 23/24 doivent être résolues avant de certifier le déclenchement complet de ces événements.
7. **Dates et initialisation.** Vérifier la fenêtre du 1er janvier 1776 des fortifications, l'absence de réensemencement sur une campagne plus ancienne, les changements de noms aux dates 1799/1801/1828 dans une copie de test, et sauvegarde/rechargement. Cette passe n'autorise pas de nouveaux changements de frontière ou de loi.
8. **Mouvements et principes.** Vérifier le callback modernisateur après activation d'une loi, le score social-démocrate 0..7 correspondant aux sept groupes conservés, et les proportions de population du lot précédent. Examiner les remises de sécurité au travail aux trois paliers et le bonus de débit de la carrière de calcaire. Comparer les valeurs et pays réellement affectés, pas seulement les libellés.
9. **Non-régression.** Reprendre les essais de soutien de guerre des missions 26/28, les cinq modificateurs navals de 30, et les objectifs de guerre de 32. Contrôler une partie Russie et une partie américaine représentatives. Les conclusions de journaux relèvent aussi de 27 et ne sont pas validées par la seule absence d'erreur d'API.

## Critères et reçu

- [ ] Les anciennes erreurs d'API listées dans `MIGRATIONS.json` et les quatre familles de helpers masqués ont disparu des nouveaux logs.
- [ ] Aucun nouveau rejet de clé, argument, scope ou cible introduit par ces fichiers.
- [ ] Opérateurs, signes, cibles et effets observés correspondent au lot et aux scénarios témoins.
- [ ] Simulation et sauvegarde/rechargement réussis pour la configuration réellement testée.
- [ ] Les erreurs de données/conclusions encore présentes sont attribuées avec leur chemin aux dépendances 23/24/27 ; aucun total global « propre » n'est déduit d'un test incomplet.

Le reçu humain doit citer la confirmation exacte, la version du lot, la configuration, les scénarios réellement exécutés et leurs résultats. Ne passer à **PASS_RUNTIME_USER_VALIDATED** et à Done qu'après confirmation explicite sur ce périmètre.
