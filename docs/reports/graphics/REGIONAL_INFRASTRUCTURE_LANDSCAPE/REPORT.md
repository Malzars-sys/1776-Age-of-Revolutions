# Paysage des infrastructures régionales — correctif partiel

Date : 2026-10-15. Cible déclarée du mod : Victoria 3 1.13.*.

**Statut : PASS_STATIC_PARTIAL. La demande complète n'est pas résolue.**
Les rails au sol et les routes ne sont PAS corrigés par cette livraison.
Aucun test moteur ni constat visuel en jeu n'est revendiqué.

## Diagnostic sur les données installées

- `common/buildings/11_private_infrastructure.txt:29-40` : le bâtiment
  `building_railway`, renommé pour les infrastructures régionales, conserve les
  groupes de PM routier, canal et ferroviaire. Leur identité économique est
  commune, même lorsque `pm_no_rail_network` est actif.
- `common/defines/00_defines.txt:46` : `NCountry.RAILWAY_BUILDING` désigne ce
  bâtiment. C'est un indice de la sélection native ; pas une preuve, à lui seul,
  de toute la logique interne du moteur.
- Dans l'installation `C:/Games/Victoria 3/game`, les types/styles de splines
  définissent des identifiants, matériaux, jonctions et paramètres de rendu.
  Aucun déclencheur de PM pour choisir dynamiquement leur style n'a été identifié
  dans ces définitions. `game_road_data.txt` contient des indices de tracés, pas
  des conditions scriptées. `spline_network.splnet` est un réseau préétabli.
- Le shader natif `gfx/FX/road_mulpass.shader` applique des textures, masques,
  dévastation et pollution. Il ne reçoit pas directement la liste des PM locaux.
  Inventer un test `has_active_production_method` dans ce shader ou dans un style
  de spline ne constituerait donc pas une correction fonctionnelle.
- `NTravel.PAVED_ROAD_TECH` et `PAVED_ROAD_MIN_INFRASTRUCTURE` sont des réglages
  globaux de connexions. Ils ne constituent pas un sélecteur documenté des quatre
  PM routiers locaux. Ils restent inchangés.
- Les véhicules, en revanche, possèdent des blocs `possible` avec `scope:state`.
  Les trains civils natifs peuvent être permis par le marché, une mine ou un camp
  de bûcherons. Le choix « experimental » est un test négatif des PM modernes :
  il ne suffit pas à prouver qu'un chemin de fer existe dans cet État.

## Modification réellement installée

1. `common/scripted_triggers/1776_infrastructure_landscape.txt` : condition
   positive vérifiant, dans l'État fourni au moteur graphique, un
   `building_railway` de niveau positif avec l'un des sept PM ferroviaires réels.
   Ni la technologie seule, ni une offre de transport dans le marché, ni un PM
   routier/canal seul ne satisfont cette condition.
2. `gfx/map/spline_network/route_graphics/02_railroad_vehicles.txt` : copie du
   fichier natif au même chemin, avec cette condition ajoutée aux quatre blocs
   `possible` (voyageurs, mines, bois et ancien rendu de mobilisation).
   Les conditions natives supplémentaires sont conservées, ainsi que les
   modèles, cultures, vitesses, quantités et autres propriétés.

Ce correctif concerne les véhicules et non les rails, les ponts ou les connexions.
Le système militaire plus récent dans `military_route_graphics` est distinct et
reste inchangé : son fichier ne fournit pas d'exemple de bloc `possible` que nous
puissions utiliser sans validation du moteur.

## Vérifications

`tools/validate_infrastructure_landscape.py` : **46/46 contrôles statiques**.
Le petit interpréteur teste le prédicat local ; il ne simule pas le moteur.

- Syntaxe et références aux sept PM du groupe ferroviaire vérifiées.
- Cas positifs pour chaque PM réel, négatifs sans bâtiment, sans scope, à niveau
  nul, sur un autre bâtiment, avec routes seules, canaux seuls ou données de PM
  absentes ; combinaisons route + rail et bâtiments multiples testées.
- Retirer les quatre conditions ajoutées restitue exactement l'arbre syntaxique
  du fichier natif. Aucun autre changement graphique implicite dans cette copie.
- Empreintes des 2 172 fichiers préexistants sous les six répertoires d'exécution
  contrôlés inchangées. Tous les fichiers MAP2N de son manifeste installé et le
  registre impérial sont conservés. Populations, bâtiments, PM économiques,
  unités, frontières et historiques non modifiés.
- HEAD et empreinte de l'index principal inchangés. Aucun commit/push.

Pour répéter le contrôle :

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:/Users/simeo/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/python.exe' -X utf8 tools/validate_infrastructure_landscape.py
```

## Prototype isolé autorisé et installé

Sur demande ultérieure du joueur, un compagnon **1776 — Paysage des
infrastructures (PROTOTYPE ISOLÉ)** a été créé et installé séparément. Source et
guide : `docs/prototypes/REGIONAL_INFRASTRUCTURE/README.md`. Il n'est pas activé
automatiquement ; le mod principal reste inchangé.

Il expérimente la désignation d'un témoin ferroviaire non productif via
`RAILWAY_BUILDING`, avec suivi des PM locaux et trois décisions A/B/automatique.
**146/146 contrôles statiques**, copie installée vérifiée par empreintes ; aucun
succès visuel ni neutralité complète de la logique interne du moteur présumé.
La demande globale (notamment croissance routière et canaux) reste partielle.
La validation manuelle MAP2N reçue du joueur est indépendante de ce prototype.

## Limite et prochaine décision technique

Il reste à trouver ou développer une liaison **de l'état local des PM vers le
réseau graphique**, pas simplement vers les véhicules. Aucun point d'extension
fiable de ce type n'a été identifié dans les fichiers examinés. Cela ne prouve
pas qu'aucune solution n'existe dans le moteur.

Une expérimentation isolée pourrait étudier la dissociation entre infrastructures
régionales et bâtiment reconnu comme ferroviaire par le moteur. Mais modifier
`RAILWAY_BUILDING`, ajouter un bâtiment miroir ou renommer le bâtiment actuel
peut affecter les connexions, l'IA, les sauvegardes et les mécanismes militaires.
Cette refonte n'est PAS appliquée au mod principal comme simple correctif visuel.
Autre piste non démontrée : un rendu graphique personnalisé avec un canal de
données dynamique réellement supporté ; aucun masque statique n'est présenté
comme une solution dynamique.

La croissance routière liée au niveau d'infrastructure, les matériaux selon PM et
les canaux restent ouverts. Aucun rail n'est globalement masqué ou remplacé par
une route, ce qui aurait aussi supprimé les vrais chemins de fer futurs.

## Contrôle en jeu, après rechargement des données

- Infrastructures régionales + routes/canaux mais sans PM ferroviaire : absence
  attendue des trains civils couverts par les quatre définitions modifiées.
  **Les rails peuvent encore être visibles : limitation connue.**
- Même État avec un vrai PM ferroviaire et les autres conditions natives : trains
  attendus ; un marché voisin équipé ne doit pas suffire au test local.
- Revenir à `pm_no_rail_network`, tester une sauvegarde/recharge et les deux
  propriétaires d'un État partagé. Vérifier aussi les messages du journal moteur.
- Distinguer les convois militaires du nouveau système, non corrigés ici.

Le lancement en cours de l'utilisateur n'est pas interrompu. Le fichier graphique
nouvellement ajouté peut nécessiter un redémarrage pour être chargé.

## Recherche locale

Un appel ColGrep-Agent-2B a fourni les pistes du bâtiment et des PM, vérifiées dans
les fichiers. Une piste `map2b_patch.py` concernait des transferts cartographiques,
pas le rendu des routes : écartée. Les données natives hors index ont été lues
directement. Aucun changement du modèle, de sa configuration ou reconstruction
globale d'index. Pas de mesure fiable d'économie de tokens sur cette intervention.
