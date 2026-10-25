# R2 — correction du déclenchement et du journal

**Avant correction : FAIL_RUNTIME_USER_REPORTED.** Le joueur confirme une absence d'offre après le 3 janvier et montre une condition de journal « Le pays a cette variable ».

**Correctif installé : READY_FOR_RUNTIME_VALIDATION.** Les contrôles statiques passent ; aucune création effective du traité ou réception d'argent après ce correctif n'a encore été observée. Les précédents contrôles statiques ne couvraient pas convenablement la différence entre un coup diplomatique et une guerre commencée. Leur réussite ne validait pas le déclenchement en jeu.

## Diagnostic établi

L'autosave de sortie retrouvée est datée du **6 janvier 1776**, joueur USA. Elle n'est pas présentée comme une nouvelle simulation de l'agent ou comme la sauvegarde exacte de chaque capture. Les fichiers ont été décodés en lecture seule.

- Le gestionnaire de guerre contient bien USA (identifiant 9) et GBR (identifiant 1) dans la guerre d'indépendance, rattachée au coup diplomatique 0, passé à l'état 5.
- L'initialisation du soutien est présente, avec zéro tranche, mais aucun drapeau d'offre française ouverte. Le marqueur d'initialisation de la ferveur n'est pas présent non plus.
- La France possède 715 384,63 £ de trésorerie dans ce relevé. Sa série sauvegardée `balance_trend.current` vaut zéro : ce cache n'est pas assimilé sans preuve à toutes les valeurs économiques accessibles au moteur.
- Les journaux du jeu signalent des suppressions de modificateurs de ferveur absents. Ces erreurs découlaient du nettoyage sans vérification préalable ; elles n'établissent pas à elles seules la cause du blocage de l'offre.

Le filtre partagé utilisait `is_diplomatic_play_enemy_of` pour la situation USA–GBR. Le correctif utilise désormais **`has_war_with = c:GBR`**, condition native explicitement employée dans `00_treaty_of_london.txt` et `05_eastern_question.txt`. Le second fichier emploie distinctement guerre et opposition diplomatique, ce qui confirme qu'il faut traiter les deux situations. Les deux entrées héritées du journal d'indépendance reçoivent également cette correction de filtre ; les valeurs du modificateur R1 restent identiques.

Les conditions d'hostilité France–USA vérifient maintenant la guerre **et** l'opposition diplomatique, pour que les aides et missions cessent réellement si les deux pays deviennent ennemis. Aucun pays n'est ajouté à une guerre.

## Modifications installées

1. L'offre initiale est programmée deux jours après `on_game_started_after_lobby`, quand l'initialisation de la partie est terminée, plutôt que depuis l'historique des pays. Un verrou évite de la programmer plusieurs fois.
2. Le journal américain réessaie chaque semaine à partir du 3 janvier si aucune tranche, offre ou demande n'est en cours, si les délais sont écoulés et si les conditions financières/diplomatiques le permettent. Aucun balayage mondial ajouté. Chaque tranche conserve deux consentements ; six tranches maximum, mêmes montants et durées.
3. Le journal possède **« Solliciter un concours français »** et, pendant une tranche, **« Mettre fin au concours financier »**. Les décisions américaine et française utilisent la même demande protégée. Les conditions du bouton sont décrites en français et en anglais, sans exposer les noms de variables.
4. La condition de fin des deux nouveaux journaux affiche **« La guerre d’indépendance américaine a trouvé son issue. »**. Le marqueur interne de résolution est conservé, avec une infobulle lisible ; on ne termine pas prématurément le journal durant l'initialisation avant la création de la guerre.
5. La base financière exige toujours 84 000 £ de réserves, mais accepte un solde hebdomadaire nul. Le niveau renforcé garde son seuil de 22 000 £ à la proposition. Le versement reste un transfert français réel et un déficit français entraîne toujours l'arrêt au contrôle mensuel. Ce changement du seuil de base évite d'écarter une France disposant de réserves lorsque son bilan est à l'équilibre ; il ne garantit pas sa capacité à tenir vingt-six semaines.
6. Une France qui refuse prévient désormais explicitement le Congrès ; la notification indique le délai de quatre-vingt-dix jours. L'absence d'offre ne doit plus masquer ce choix de l'IA. L'acceptation américaine revérifie aussi les réserves et finances avant de présenter un choix utilisable.
7. Les nettoyages des dettes héritées, des états de ferveur et des commissions vérifient désormais l'existence du modificateur avant suppression. Les quatre anciens événements financiers passent par ce nettoyage protégé ; les événements français 5 et suivants sont préservés.

## Vérification et protocole

`VALIDATION.json` contient **159 contrôles R2 réussis**, dont 21 contrôles ajoutés pour ce correctif, ainsi que les vérifications antérieures. Ils couvrent le filtre de guerre, l'entrée après le lobby, la programmation unique, le rattrapage hebdomadaire, les verrous de demande, le seuil financier, les boutons, les conditions traduites et les suppressions protégées. Les références, clés FR/EN sans doublons et assets passent également. L'index Git et HEAD restent inchangés ; aucune carte, population ou mécanique impériale modifiée par ce correctif.

Les montants de transfert, articles natifs, obligations et fournitures sont conservés. L'audit de cavalerie reste séparé : 22 contrôles déjà réussis, candidat toujours non appliqué. Les fichiers et empreintes actuels sont dans le manifeste R2. `PRE_FIX_VALIDATION.json` conserve le dernier résultat statique de la livraison initiale ; `EVIDENCE.json` distingue les observations antérieures de l'état non encore validé après réparation.

Pour vérifier cette version, **fermer complètement puis relancer Victoria 3**, afin de recharger les nouveaux scripts et boutons. En nouvelle partie USA : ouvrir « Les voies discrètes du secours », vérifier les boutons et la phrase de fin ; avancer jusqu'au 3 janvier. L'offre doit ouvrir la négociation française si les conditions affichées sont satisfaites ; si la France refuse, une notification américaine doit le dire. Le Congrès conserve son propre choix d'acceptation. Vérifier ensuite la présence du traité et le débit/crédit hebdomadaire des deux pays.

Le bouton peut aussi solliciter l'offre directement, y compris depuis une sauvegarde R2 existante après rechargement des scripts, si la guerre continue et les conditions sont satisfaites. Tester une offre initiale empêchée puis des conditions rétablies : le contrôle hebdomadaire doit reprendre la négociation, sans double traité. Vérifier enfin qu'aucune erreur de suppression de modificateur absent n'est répétée par la ferveur.

Une réussite de ces contrôles de fichiers ne constitue pas une confirmation moteur. La prochaine validation du joueur doit encore confirmer l'offre, les choix, le traité et les transferts effectifs.
