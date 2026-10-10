# IA et infrastructures régionales — 10 octobre 2026

## Modifications

- Les routes utilisent désormais la sélection IA `most_productive` au lieu du défaut `most_profitable`. Les locomotives et wagons utilisaient déjà ce réglage.
- Les poids IA des routes, locomotives et wagons augmentent fortement avec leur niveau technologique. Les variantes liées aux principes de bloc sont conservées.
- Au lancement d'une partie puis chaque mois, un contrôleur réservé aux pays IA sélectionne les meilleures méthodes admissibles des infrastructures existantes. Le test natif `can_activate_production_method` vérifie leur disponibilité ; les technologies ne sont jamais accordées par le script.
- Une méthode déjà sélectionnée reste inchangée : le contrôleur ne réapplique pas inutilement le même PM. Les wagons sont désactivés lorsqu'il n'y a pas de réseau ferroviaire actif.
- Les États de chaque pays sont classés selon leur PIB total, en incluant ceux sans infrastructure régionale. Les positions 0 à 9 peuvent recevoir les meilleurs canaux disponibles ; les autres repassent à « Aucun réseau de canaux ». Un pays de moins de dix États utilise tous ses États. Le classement est réévalué chaque mois.
- Les pays joueurs sont exclus. Aucun niveau, coût, recette, emploi, icône, technologie, subvention ou bâtiment historique n'est modifié par cette intervention.

## Fichiers

- `common/production_method_groups/22_tech7a_wave_a_land_transport_pmgs.txt` : sélection productive des routes.
- `common/production_methods/22_tech7a_wave_a_land_transport_production.txt` : poids IA routiers.
- `common/production_methods/11_private_infrastructure.txt` : poids IA ferroviaires et wagons bois/acier.
- `common/production_methods/14_tech6c5c_aluminium_production_and_consumers.txt` : poids IA des wagons aluminium, sans changement graphique.
- `common/scripted_effects/1776_ai_regional_infrastructure_effects.txt` : classement PIB et sélection des PM.
- `common/on_actions/13_1776_ai_regional_infrastructure.txt` : actions secondaires au lancement et au contrôle mensuel, sans remplacement des actions natives.
- `tools/validate_ai_regional_infrastructure_1776.py` : validations statiques et modèle d'exécution des effets réellement écrits.

## Validation

Le validateur vérifie les références PM, les branchements, les poids croissants, la conservation des recettes/emplois/déblocages et les scénarios suivants : méthodes verrouillées, paliers intermédiaires, meilleure méthode déjà active, répétition sans changement, protection du joueur, pays de 1/5/10/11 États, égalités de PIB, changement du top 10 et État riche sans bâtiment. Aucun bâtiment n'est créé ou agrandi dans ces tests.

Les tests de modèle des journaux ottomans précédemment modifiés passent également. Le contrôle des différences ne signale pas d'erreur d'espacement.

Ces vérifications ne démarrent pas le jeu. À vérifier après redémarrage : absence de nouvelles erreurs dans les logs, sélection des PM au début puis après un mois, maintien des canaux dans le top 10 et évolution réelle des coûts/infrastructures. La règle des canaux est une correction mensuelle, pas une interdiction native permanente : une décision autonome de l'IA entre deux contrôles sera corrigée au contrôle suivant. Aucun résultat budgétaire précis n'est garanti.

Aucun push, merge ou commit effectué. Les changements antérieurs présents dans le répertoire de travail sont préservés.
