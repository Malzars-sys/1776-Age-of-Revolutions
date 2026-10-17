# Essai dans la partie du joueur — résultat partiel

**PROTOTYPE_RUNTIME_PARTIAL_INCONCLUSIVE_VISUAL**. Ce n'est pas une validation
complète du rendu, ni un test moteur automatisé.

L'assistant a utilisé la compétence de contrôle Windows pour manipuler uniquement
Victoria 3, avec l'autorisation explicite du joueur. Aucune console système, aucun
mode debug, aucun ajout de technologie ou modification du code du mod pendant
l'essai. Les images de l'outil ont été inspectées directement dans la conversation.

## Ce qui a effectivement fonctionné

- Les trois décisions localisées sont présentes dans le journal.
- Île-de-France : les infrastructures régionales restent au niveau **17**.
- « Forcer » crée bien le **témoin niveau 1**. Sa fiche affiche **0 emploi**, un
  processus vide et une dépense gouvernementale affichée de **−0,00 £**.
- « Retirer », puis « Automatique » enlèvent le témoin ; son absence est vérifiée
  dans la liste des bâtiments de la capitale.
- Les routes ordinaires restent visibles. Le joueur avait constaté la disparition
  générale des rails avec le compagnon ; il n'y a pas eu de comparaison contrôlée
  avec le compagnon désactivé pendant cette intervention.

## Ce qui n'est pas démontré

Le forçage n'a pas donné un aller-retour visuel assez net des **rails au sol** pour
certifier l'hypothèse. Des lignes sombres ont d'abord été repérées, mais leur
comparaison rapprochée avec le témoin retiré ne permet pas de les identifier
sûrement comme des rails nouvellement apparus. Elles ne sont donc pas utilisées
comme preuve de succès. Les tracés, véhicules routiers, ponts et effets du zoom
doivent rester distingués.

Du temps a été laissé au moteur ; le niveau 1 neutre peut être insuffisant, une
condition interne de production/activité peut intervenir ou le rafraîchissement
peut être différé. **Ce sont des hypothèses, pas des causes établies.**

Le PM réel « Trains expérimentaux » a été examiné : son infobulle confirme que la
France doit rechercher **Chemins de fer**. Il est indisponible et n'a pas été
activé. Le PM actif reste **Pas de réseau ferroviaire**. Aucun prérequis n'a été
contourné et aucune recherche n'a été accordée à la partie du joueur.

Changer uniquement les PM routiers ou de canaux ne doit pas créer le témoin :
son prédicat automatique exige explicitement un véritable PM ferroviaire.

## Partie rendue à l'utilisateur

Départ : 29 juillet 1776 en pause. Fin : **7 août 1776 en pause, vitesse 1**.
L'essai a avancé la partie de neuf jours calendaires, franchissant le changement
de mois, sans crash observé. Ce n'est pas un mois complet de simulation ni une
validation globale des hooks. Le suivi automatique est rétabli ; pas de témoin
forcé laissé dans la capitale. Aucun bâtiment économique ni PM n'a été modifié
manuellement ; les évolutions ordinaires de simulation ne sont pas annulées.
Aucune sauvegarde/recharge manuelle n'a été effectuée.

## Journal moteur et suite

Deux avertissements propres au compagnon demandent un encodage UTF8-BOM dans les
fichiers d'on_actions et de décisions. Le moteur indique essayer de les utiliser
quand même ; leur fonctionnement UI est constaté. Ils restent à nettoyer lors
d'une prochaine révision du prototype, sans correction silencieuse de la version
en cours de test.

Les autres erreurs lues concernent des fichiers existants (cibles diplomatiques,
variantes de lois, événements/technologies). Elles ne sont pas attribuées au
prototype sans preuve. Aucune absence universelle d'erreurs moteur n'est annoncée.

Avant intégration : vérifier un vrai cycle de PM ferroviaire dans une partie où
la technologie existe, établir un contraste visuel sûr au même endroit/zoom et
tester la recharge. Conserver ensuite les contrôles des États partagés, de l'IA
et des connexions militaires. **Le compagnon reste isolé et non validé pour une
campagne normale. MAP2N conserve sa validation manuelle distincte.**
