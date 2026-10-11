# MAP-0 — Stratégie d'édition

Recommandation : **A d'abord, B si les États existants empêchent le gameplay voulu,
C uniquement après démonstration d'une insuffisance géométrique**. Les limites
historiques restent à rechercher : aucune zone n'est déclarée devoir être redessinée
sur la seule base de cet audit informatique.

| Critère | A — réattribution | B — regroupement/scission d'États | C — géométrie |
|---|---|---|---|
| Faisabilité constatée | create_state/owned_provinces déjà utilisés | State Regions éditables, provinces RGB conservées | Bitmap/topologie natifs disponibles; chaîne d'export éditeur à établir et tester |
| Précision | Bornée aux provinces existantes | Même résolution des frontières, découpage administratif plus adapté | Peut améliorer une frontière à l'intérieur d'une province |
| Travail indicatif | Petit lot : heures à jours avec données préparées | Jours par lot et migration des dépendances | Jours à semaines par prototype; aucune estimation mondiale fiable avant essai |
| Risque de crash | Faible si IDs et dépendances valides; doublons restent bloquants | Moyen : références, ID numérique et régions stratégiques | Élevé relativement à A/B : ressources dérivées et raccords; pas de crash garanti |
| Performance | Géométrie inchangée; effet dépend des nouvelles entités | Plus d'États jouables peut augmenter simulation/GUI | Plus de provinces/ressources peut augmenter mémoire et temps de chargement; à mesurer |
| Mises à jour | Comparer historiques natifs et TAGs | Synchroniser régions/hubs/ressources/stratégie | Fort couplage à la version du bitmap et exports du jeu |
| Travail georg3mx | Préserver transferts déjà intégrés; lot nouveau à arbitrer | Ne pas perdre les sous-États AUS/VEN ni Nunavut | Nécessite remapping exhaustif des IDs de ses corrections |
| Populations/bâtiments | Migrer les couples owner/État impactés, conserver totaux | Ventiler explicitement agrégats, capitales et investisseurs | Même migration + nouveaux IDs et localisation spatiale |
| Validation | Structure, conservation, nouvelle partie | A + ressources, hubs, HQ, noms et interfaces | B + raster, topologie, ports, connexions, exports et benchmark |
| Automatisation | Bonne avec manifeste approuvé de transferts | Partielle; répartition démographique exige jugement | Contrôles de pixels automatisables, tracé historique non automatique |

Ces durées sont des ordres de grandeur de planification, non des tests chronométrés.

## Décision pour chaque correction

Si les provinces existantes permettent la bonne autorité territoriale, utiliser A.
Un State_ID partagé n'est pas un défaut : plusieurs create_state peuvent être
nécessaires. Si une nouvelle unité administrative, un bassin de ressources ou un port
ne peut pas être géré dans le regroupement actuel, justifier B sans changer les pixels.
Si la frontière documentée traverse une province et que l'approximation est
inacceptable après examen, préparer une preuve cartographique de C, un prototype
isolé et un plan de migration. Créer des provinces n'est pas la réponse par défaut.

## Ordre d'intégration ultérieur

Geler baseline/hash du bitmap → recherches séparées → arbitrage historique central
→ manifeste des transferts → migration des données → tests statiques → nouvelle
partie contrôlée → validation utilisateur → commit ciblé. Push/merge sur main
requièrent une autorisation distincte.

Le lot collaborateur actuel reste en attente : pas d'intégration définitive avant
résolution documentée des tokens Git en Bessarabie, du doublon lombard et du sort
de LUX (population, administrations, formation militaire et traité).

## Ce que MAP-0 ne conclut pas

Aucun tracé historique de 1776 n'a été validé. Les cas Luxembourg/Wallonie,
Lombardie/Istrie/Tyrol, Caucase/Bessarabie et Nunavut sont des priorités de recherche,
pas une liste prouvée de besoins de nouvelle géométrie. Les neuf chefs doivent
fournir les preuves nécessaires pour décider, notamment pour les comptoirs,
souverainetés autochtones et frontières non linéaires.
