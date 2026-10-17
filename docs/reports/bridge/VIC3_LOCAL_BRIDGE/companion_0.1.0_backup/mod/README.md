# Prototype isolé — paysage des infrastructures

Version 0.1.0, Victoria 3 1.13.9 / mod principal 1776. **Essai à valider en jeu.**

Ce mod compagnon n'est pas activé automatiquement. Il ne remplace aucun fichier
du mod principal ni aucune carte MAP2N. Aucun playset existant, réglage du launcher
ou sauvegarde n'est modifié par son installation.

## Installation et activation

Le paquet source est dans `mod/` à côté de ce guide. Sa copie installée porte le
nom **1776 — Paysage des infrastructures (PROTOTYPE ISOLÉ)** dans le launcher.
Le nom du dossier est `aor1776_landscape_prototype`.

1. Au prochain lancement du launcher, ajouter ce mod à un **playset de test** avec
   uniquement **Age of revolution /Fork**, puis le prototype **après** le principal.
   Si le launcher était ouvert pendant l'installation, le rouvrir pour rafraîchir
   les mods locaux. Aucun besoin d'effacer ses caches.
2. Lancer une **nouvelle partie dédiée** et nommer ses sauvegardes « TEST-PAYSAGE ».
   Ne pas charger ou écraser une sauvegarde de campagne normale avec ce prototype.
3. Après l'essai, désactiver le prototype ; le principal seul conserve son
   comportement précédent. Ne pas continuer une sauvegarde de prototype en
   production : elle contient potentiellement ses témoins et variables de test.

## Hypothèse technique testée

Le bâtiment économique `building_railway` reste intact (infrastructures régionales,
emplois, biens, PM et financement). Un autre bâtiment, **Témoin ferroviaire**, est
désigné par `NCountry.RAILWAY_BUILDING` uniquement dans le compagnon.

Ce témoin a un seul niveau, aucun emploi, aucun bien, aucune urbanisation, aucune
consommation ou production d'infrastructure, aucun modèle de ville/station ajouté.
Il n'est ni constructible ni extensible manuellement. Il peut être visible dans
les listes de bâtiments : c'est volontaire pour le diagnostic, pas un bâtiment
économique ou un élément prétendument caché.

En mode automatique, il existe seulement dans la part d'État dont le bâtiment
régional a un niveau positif et l'un des sept PM ferroviaires réels. Routes seules,
canaux seuls, technologie seule ou transport dans un marché voisin ne suffisent
pas. Synchronisation à l'entrée en partie, construction/agrandissement, changement
de PM et propriétaire ; réparation mensuelle pour les cas sans hook dédié
(notamment suppression/réduction du bâtiment ou rechargement).

**L'hypothèse est que la désignation du bâtiment pilote les rails au sol. Ce n'est
pas encore prouvé.** Si le moteur exige aussi de l'emploi, une production, un
identifiant en dur ou utilise des tracés déjà mémorisés, ce témoin neutre peut ne
pas suffire. Ne pas conclure au succès parce que seul le train a disparu.

Changer cette désignation globale pourrait aussi influencer les connexions
militaires ou l'IA. La neutralité des définitions du témoin est vérifiée
statiquement ; l'absence totale d'effets indirects ne l'est pas.

## Test visuel court, sans débloquer de technologie

Choisir un pays dont la capitale possède des infrastructures régionales sans PM
ferroviaire (France/Île-de-France ou Prusse/Brandebourg, à vérifier dans la partie).
Dans les décisions du journal, trois entrées **PROTOTYPE** sont disponibles :

1. **Retirer le témoin ferroviaire de la capitale** : témoin absent ; observer et
   capturer les rails existants et les routes.
2. **Forcer le témoin ferroviaire dans la capitale** : un témoin, niveau 1 ; observer
   exactement le même lieu et le même zoom. Cette commande ne touche PAS aux PM
   du bâtiment régional. Les trains civils peuvent rester absents, leur condition
   exigeant toujours un vrai PM ferroviaire.
3. **Retirer le témoin** de nouveau : vérifier la réversibilité, puis **Revenir au
   suivi automatique des PM** pour terminer l'essai.

Entre chaque étape, laisser passer un jour, dézoomer/rezoomer. Si le rendu ne se
rafraîchit pas, sauvegarder/recharger seulement la partie de test et noter ce
besoin : il fait partie du résultat, pas d'un succès instantané présumé.

Ensuite, dans une partie de test permettant réellement un PM ferroviaire, activer
ce PM puis revenir au PM sans rail. Vérifier que le témoin apparaît/disparaît dans
le bon État, sans déborder sur l'État voisin ou l'autre propriétaire d'un État
partagé. Le prototype ne donne aucune technologie et ne change aucun PM économique.

Contrôler également : niveaux des bâtiments économiques et emplois identiques,
pas de facture/demande de biens du témoin, pas de route militaire anormale, budgets,
recrutement, progression mensuelle et rechargement sans erreur nouvelle.

## Résultats possibles

- Témoin et rails suivent A/B/A : preuve utile d'un contrôle de présence ; reste à
  tester les niveaux, densités et conséquences de la désignation globale.
- Témoin suit A/B/A mais rails restent identiques : les scripts fonctionnent mais
  l'hypothèse de rendu n'est pas validée. Garder les captures et logs.
- Témoin absent malgré « Forcer » : vérifier ordre de chargement et erreurs de
  script avant de tirer une conclusion sur le moteur graphique.

Ce prototype **ne rend pas encore la croissance des routes dépendante du niveau
des infrastructures**, ne change pas leurs textures selon PM et ne dessine pas
les canaux. Ces chantiers restent distincts ; aucun remplacement global des rails
par une texture de route n'est utilisé pour simuler un résultat dynamique.

MAP2N a reçu sa propre validation manuelle du joueur. Elle ne valide pas ce mod.

## Reproduction technique

`tools/infrastructure_landscape_prototype.py` : `--capture`, `--validate`,
`--deploy`, `--verify-installed`. La capture initiale ne doit pas être remplacée.
Déploiement refusé si un dossier homonyme différent existe ; aucun écrasement
de fichiers inconnus. Les checks restent statiques, pas un lancement du jeu.
