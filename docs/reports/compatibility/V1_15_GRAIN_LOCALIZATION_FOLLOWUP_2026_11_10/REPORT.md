# Libellé des ordres de vente de céréales — suivi du test joueur

Le mainteneur rapporte que les tests groupés passent, en nommant le Japon, le Maroc, les forteresses, le tutoriel et les autres infobulles. Il relève une réserve commune aux événements essayés : le grain porte le nom de l'artillerie. `HUMAN_ACCEPTANCE.json` conserve ses messages exacts, la portée de son retour et les détails non attestés ; la capture fournie est conservée localement. Aucun résultat d'une ancienne exécution n'est réécrit.

## Cause et correction

Le fournisseur était la localisation française canonique `localization/french/modifiers_l_french.yml`, clé `state_sell_orders_grain_add` (ligne 871 lors du constat). Son icône utilisait `GetGoods('grain')`, mais son nom utilisait `GetGoods('artillery')`. Le descriptif voisin et la version anglaise visent déjà correctement les céréales. Le nom français du bien `grain` est « Céréales ».

Une surcharge française isolée est installée dans `localization/french/replace/1776_v115_grain_sell_orders_l_french.yml`. Elle remplace uniquement la référence du nom par `GetGoods('grain')`, en conservant l'icône, l'espace et le format de casse du texte d'origine. Elle corrige tous les consommateurs de ce modificateur, quel que soit l'événement : achats de réserves, distribution d'urgence, réquisition et autres emplois éventuels. Aucun patch individuel des événements n'est nécessaire.

Les trois effets japonais restent respectivement −10, +10 et +5 ordres de vente de grain. Aucun intrant, prix, montant, durée, modificateur ou scénario n'est modifié. La localisation anglaise correcte reste héritée, ainsi que le descriptif français. Le vanilla et les fichiers des autres missions sont préservés. Une seule addition de données runtime est effectuée ; les autres additions sont les preuves locales de ce suivi.

## Contrôles et suite

Sept vérifications ponctuelles réussissent : BOM/en-tête, fournisseur de remplacement unique dans le mod, accord icône/nom, substitution bornée, préservation des événements/modificateurs et de leurs textes, préservation des deux sources canoniques, cohérence de l'anglais hérité. Résultats dans `CHECKS.json`, empreintes dans `CONTRACT.json`. Aucun test moteur après la surcharge n'est inventé.

Il suffit de relancer le jeu pour charger le texte, puis au Japon d'exécuter `event phase1_japan_tenpo.1` et de survoler les réserves. La ligne doit maintenant afficher l'icône du grain et « céréales ». Un contrôle de cette ligne commune suffit pour cette correction ; les tests fonctionnels déjà confirmés ne sont pas à refaire. L'ajout forcé d'un événement ne rejoue pas une validation de sa date historique.

Les cartes GitHub et les anciens reçus restent inchangés dans ce suivi. Aucune opération Git d'écriture ni publication Steam n'est effectuée. La préparation de la distribution allégée reste l'étape suivante après le dernier contrôle d'affichage.
