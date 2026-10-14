# Sélecteur de cartes bloqué — 13 octobre 2026

La configuration de chargement de la relance contient bien le mod principal local
et le prototype, dans cet ordre. Le problème constaté est une erreur d'interface
dans le mod principal, pas une preuve d'échec du masque graphique du prototype.

Le journal `gui.log` de 01:53:25 signale `pdx_gui_factory.h:603`,
`gui/lens_toolbar.gui:388` : un descripteur d'élément ne peut contenir qu'un seul
enfant et aucune propriété. L'ajout du bouton d'atlas à côté du `fixedgridbox`
à l'intérieur du `scrollwidget` enfreignait cette contrainte.

Correction appliquée : suppression de l'entrée d'atlas dans la liste et de son
décalage de 40 pixels. Le bloc `dropDown` complet est maintenant identique au
fichier vanilla installé. Le bouton indépendant d'atlas est conservé à x=252,
à l'extérieur du sélecteur natif large de 246 pixels. Le générateur est corrigé
pour ne pas réintroduire l'erreur.

Validation : 406 contrôles statiques réussis, dont unicité des enfants des
descripteurs natifs, égalité exacte du sélecteur vanilla et répétabilité du
générateur. Aucun changement au prototype installé ni au playset n'est nécessaire.

Il faut relancer le jeu avec « 1776 — Test carte impériale » pour confirmer que
le menu s'ouvre à nouveau. Les journaux consultés datent d'avant la correction :
la réparation n'est pas encore confirmée par le moteur. L'apparition du nouveau
mode et son rendu jaune restent à tester une fois le sélecteur accessible.
