# Validation en jeu — CONTENT-USA-MINUTEMEN-REFORM

Statut : **NOT_RUN**. Ce document décrit des essais à effectuer, pas des essais réussis. Utiliser une nouvelle partie avec le mod courant et des sauvegardes de test distinctes. Relever date, version du jeu, mods actifs et erreurs nouvelles dans les journaux moteur. Conserver une sauvegarde avant chaque branche.

## A — Déclenchement et illustration

1. Commencer avec les USA le 1er janvier 1776. Contrôler les Minutemen actifs, l’absence de doublon visible de la milice nationale standard et les formations : 12 infanteries régulières, 1 artillerie, 15 conscrits potentiels non levés, 5 navires et commandants existants.
2. Vérifier que **Corps du génie** n’est pas recherché. Prendre **Examiner la réorganisation des milices** : l’événement doit apparaître avec son illustration et ses deux choix. Réorganiser doit être visible et indisponible ; son survol doit expliquer la recherche manquante.
3. Pendant l’événement, vérifier qu’une autre demande ne crée pas de copie. Laisser passer ou résoudre normalement le choix par défaut sur une sauvegarde distincte ; contrôler l’absence de relance automatique.
4. Sur une branche où aucune décision n’a encore été prise, gagner l’indépendance et terminer le journal : recevoir l’offre une seule fois. Sur une branche ayant déjà résolu l’événement, la victoire ne doit pas en créer une seconde.
5. Ne pas attendre un événement particulier au 4 juillet ou en 1783. Si les USA demeurent engagés dans une autre guerre, le journal original peut ne pas être complet : vérifier alors l’accès par décision.

## B — Réorganisation et promulgation

1. Sur une autre branche, rechercher normalement **Corps du génie**. Réunir une légitimité d’au moins 25 et une chance de promulgation positive. Vérifier dans le panneau des lois la disponibilité native de la loi et les conditions politiques, mouvements, restrictions de bloc et délais éventuels.
2. Avec aucune autre promulgation active, choisir **Réorganisons nos milices !** : une promulgation de la Milice nationale réorganisée doit commencer. Les Minutemen doivent rester la loi active durant les étapes politiques.
3. Refaire le choix avec une autre loi en cours : option indisponible, aucune annulation de l’autre loi et aucune adoption immédiate.
4. Tester soutien nul et légitimité insuffisante : option indisponible. Si une tentative de cette même loi a été précédemment annulée ou a échoué, vérifier que l’événement respecte le délai natif de nouvelle tentative ; noter toute divergence avec l’écran des lois.
5. Mener la promulgation jusqu’à son terme par la procédure native. Les contributions des Minutemen doivent cesser et celles de la nouvelle loi s’appliquer une seule fois. Contrôler les plafonds, le taux de conscription et les vitesses réelles avec leurs autres modificateurs.
6. Vérifier que les unités régulières, commandants et bâtiments existent toujours. Mesurer le nouveau nombre de conscrits potentiels, leurs qualifications, leurs effectifs et le budget après stabilisation. La loi peut modifier le potentiel natif sans ajouter gratuitement les bataillons dans les scripts.
7. Tester l’annulation ou l’échec de la réforme : les Minutemen restent en vigueur ; les règles ordinaires de nouvelle tentative continuent de s’appliquer. Le débat narratif ne se répète pas.

## C — Conservation

1. Choisir **Les Minutemen ont fait leurs preuves !** sur une sauvegarde séparée.
2. Vérifier que la loi, les unités, les effets et le budget ne reçoivent aucun bonus ou coût supplémentaire du choix.
3. Après recherche, vérifier que la Milice nationale réorganisée est encore disponible dans l’écran normal des lois, sous les conditions politiques ordinaires. L’événement ne doit pas verrouiller les autres lois militaires.

## D — Résolution de guerre

1. **Victoire sans réforme engagée** : l’événement est proposé, les Minutemen restent actifs jusqu’à une éventuelle adoption volontaire.
2. **Victoire ou paix indépendante avec réforme en cours** : la procédure se poursuit, sans nouvelle copie d’événement et sans loi imposée à la paix.
3. **Défaite avec Minutemen actifs** : vérifier le retour automatique aux **levées paysannes**, conformément à la dernière demande de l’utilisateur. Cette règle remplace l’exigence contraire du test D initial.
4. **Défaite avec cette réforme en cours** : annuler cette seule promulgation et conserver le retour aux levées paysannes. Avec une autre loi en cours, le nouveau bloc d’annulation ne doit pas l’affecter ; relever séparément les conséquences natives de la paix et de l’assujettissement.
5. **Paix négociée maintenant les USA sujets** : contrôler l’application du parcours de défaite existant et l’indisponibilité d’une réforme nationale indépendante. Si la paix les laisse indépendants, conserver l’accès institutionnel.

## E — Sauvegarde et rechargement natifs

Sauvegarder, quitter puis recharger dans chacun des cas : événement ouvert, réforme choisie et en cours, loi adoptée, maintien des Minutemen. Vérifier respectivement le maintien de l’événement ou de son attente, la procédure native, la loi adoptée et la résolution du choix. Aucune deuxième copie ni perte de progression. Refaire les contrôles après la victoire du journal.

## F — Non-régression et clôture

Contrôler l’aide française de bout en bout, les deux conditions d’intérêt, le traité, les transferts et la dette ; Liberty Or Death et la ferveur ; les commandants et formations ; les coûts militaires et qualifications ; les autres variantes de lois et un pays non américain. Vérifier les ouvertures France/USA prévues par R6. Inspecter également les erreurs impériales et territoriales sans modifier ces chantiers.

Rejouer les contrôles statiques avec `tools/validate_usa_minutemen_reform.py`. Joindre les sauvegardes avant/après, captures des lois et survols, valeurs budgétaires et erreurs moteur. Passer au statut **CONTENT_USA_MINUTEMEN_REFORM_RUNTIME_VALIDATED** seulement après réussite réelle des essais pertinents ; consigner les échecs au lieu de les remplacer par les projections statiques.
