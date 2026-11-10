# Vérification moteur de la mission 47

Portée : retrait de l'appel annuel `on_memento_mori`, sans modification de la
mortalité ou de la succession. Ce protocole n'atteste aucune exécution.

1. Redémarrer le jeu avec le mod actuel, puis lancer une nouvelle partie en
   1776. Noter la version, la liste des mods et les DLC actifs. Conserver les
   nouveaux journaux sans effacer les captures antérieures.
2. Jouer au-delà d'un cycle annuel complet. Vérifier l'absence d'une référence
   invalide à `on_memento_mori` au chargement et lors des impulsions annuelles.
   Relever séparément toute autre erreur, sans l'attribuer automatiquement à 47.
3. Sauvegarder puis recharger ; poursuivre la simulation et confirmer que la
   partie continue normalement. Vérifier que les dirigeants et chefs de groupes
   d'intérêt conservent des fiches cohérentes. Aucun remplacement immédiat de
   personnage n'est attendu de cette correction.
4. En cas de décès ou de succession survenant naturellement, relever le
   personnage, la date et le successeur. L'absence de décès dans une courte
   simulation ne permet pas de conclure à une immortalité ou de certifier le
   taux de mortalité. Ne pas tuer artificiellement des dirigeants pour valider
   le seul retrait de cet appel.

Les missions 45 et 46 conservent leurs propres protocoles, notamment les
branches japonaises ou marxistes tardives. Une simulation de 1776 ne valide
pas ces histoires. La mission 47 reste ouverte jusqu'au retour humain ; les
contrôles statiques ne valent pas validation moteur.
