# Protocole joueur — A1

État : **NOT_RUN**. Aucun démarrage, résultat de bataille ou rechargement n'est déclaré validé par cette livraison.

## Nouvelle partie de 1776

1. Relancer le jeu avec la version modifiée du mod. Créer une **nouvelle partie au 1er janvier 1776**. Les anciennes sauvegardes après cette date ne reçoivent pas automatiquement les forts historiques.
2. Vérifier les douze lignes de [FORTRESS_PLACEMENT.csv](FORTRESS_PLACEMENT.csv) : propriétaire, État, bâtiment, niveau **1** et PM **simple**. Aucun PM renforcé/avancé ni second type de fort dans le même État.
3. Vérifier surtout **Gibraltar britannique**, dans la portion britannique de Haute-Andalousie. L'Espagne n'y reçoit aucun fort de ce lot. Maastricht ne reçoit aucun ajout.
4. En Flandre française, Alentejo et Beira, attendre un **fort côtier**, même si le site historique nommé dans le rapport est intérieur. Les bâtiments restent régionaux et ne doivent pas produire de bonus terrestre caché.
5. Vérifier qu'aucun bataillon du génie, régiment d'infanterie, commandant, population ou frontière n'a été ajouté ou supprimé par ce lot. Les régiments spécialisés restent recrutables selon les technologies existantes.
6. Consulter les erreurs du journal de jeu : relever toute référence inconnue ou erreur visant `1776_historical_forts_start`, `create_building`, les nouveaux effets ou les branchements de démarrage. Une projection statique ne prouve pas l'ordre d'exécution des branchements natifs.

## Un mois, puis sauvegarde et reprise

1. Laisser passer au moins un jour et vérifier que le niveau n'est pas passé à 2 à cause des deux branchements de démarrage.
2. Laisser passer **un mois**. Noter emploi, achats d'armes/fer, budget et pénuries des cinq pays. Ne pas déduire le coût national du seul montant de réserves.
3. Vérifier que les forts ne créent pas automatiquement des bataillons de campagne. Contrôler particulièrement la petite subdivision de Gibraltar.
4. Sur une copie de test, agrandir un fort terrestre : le second niveau doit afficher 900 points mais utiliser le ralentissement déjà prévu pour viser 1 100 effectifs avant autres bonus. Le fort côtier garde son coût natif.
5. Sauvegarder, quitter au menu et recharger. Les niveaux, PM et propriétaires doivent rester identiques ; aucun doublon.
6. Sur une copie distincte, démolir un fort après le départ puis recharger : il ne doit pas réapparaître.

## Scénario séparé de bataille terrestre

Préparer une partie de test indépendante ; ne pas altérer une campagne de référence pour ce scénario.

| Cas | Attendu pour la seule protection du fort |
| --- | --- |
| Défenseur propriétaire/contrôleur, un niveau simple entièrement employé, aucun génie adverse | −5 % terrain perdu, −5 % pertes, +5 % défense |
| Même cas, cinq bataillons du génie attaquants à 1 000 hommes effectivement engagés chacun | Annulation de ces seuls bonus |
| Cinq niveaux simples / renforcés / avancés à plein emploi | 25 / 50 / 75 % de protection supplémentaire |
| Génie attaquant complet : 25 / 50 / 75 bataillons contre ces cinq niveaux | Annulation de ces seuls bonus, pas inversion en malus |
| Génie seulement en défense | Pas d'annulation de ses propres forts |
| Génie partiellement rempli | Réduction proportionnelle aux hommes présents, avec l'arrondi du script |
| Aucun fort, État côtier, ou province déjà contrôlée par l'ennemi | Pas de condition spéciale de fort terrestre |
| Artillerie ordinaire seule | Pas de contre-mesure réservée au génie |

Comparer les conditions de bataille et leurs effets, pas seulement l'issue aléatoire de deux combats. Les protections de moral/retraite natives doivent rester présentes. Le fort côtier doit être contrôlé séparément par invasion/blocus ; le scénario terrestre ne valide pas son fonctionnement naval.

## Observation américaine

Vérifier le départ neutre de l'Espagne, la chaîne franco-américaine et l'absence de changement des armées déjà installées. Simuler suffisamment pour observer les effets budgétaires britanniques : il s'agit d'un contrôle d'équilibrage, pas d'une réécriture de la révolution dans ce lot.

Le statut ne devient `PASS_RUNTIME_USER_VALIDATED` qu'après confirmation explicite du joueur avec date, pays testés et résultats. Aucun reçu n'est créé automatiquement.
