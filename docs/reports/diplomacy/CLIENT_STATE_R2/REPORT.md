# État client, règles de liberté et armée éthiopienne

Livraison du31 octobre 2026 — **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Référence historique : 1er janvier 1776. Aucune validation moteur ni attestation humaine nouvelle.

## Changements installés

- Nom visible **État client** / **Client state**, descriptions, concepts, notifications et ruptures harmonisés. Les identifiants internes `aor1776_protected_state` et `subject_type_aor1776_protected_state` restent stables : les anciens noms des deux vassalités fusionnées ne redeviennent pas des types distincts.
- Icône fournie par le joueur archivée avec son original, détourée par l'outil d'image, et exportée avec transparence dans les cinq emplacements de R1 : action128 px, variantes30 px et icônes de lentille64 px. Main, bouclier, lauriers et socle conservés dans le master. Les previews sont dans `.asset-cache/client_state_r2/`. Les fichiers DDS sont BGRA8 avec chaînes de mipmaps complètes. Aucun emplacement dépendant du nom interne n'est abandonné lors du renommage visible.
- Tigré, Godjam, Wollo : **tributaire → État client de l'Éthiopie**. Pas de modification des frontières, populations, pays, lois ou technologies. Les quatre liens Durrani/Kalat de R1 restent clients.
- Armée ETH : **10 bataillons réguliers d'infanterie irrégulière et15 conscrits de réserve**, dans Gonder ; formation et général existants conservés. Avant : 4 dragons et12 irréguliers, plus25+23 conscrits rattachés au même État après l'ancien découpage. Les dragons demandaient `regulated_small_arms`, absent du profil ETH : l'infanterie irrégulière évite d'accorder une technologie nouvelle pour maintenir cette composition héritée.

## Désir de liberté : correction réelle du branchement

Le calcul natif `liberty_desire_weekly_change` ne comportait aucun cas pour la nouvelle action : les composantes comparatives de prestige et de puissance militaire n'étaient donc pas appliquées au nouveau statut. R2 ajoute deux branches exclusives à celui-ci, après les cas natifs sans prestige/sans armée. Le reste du calcul est comparé structurellement à sa version d'entrée et préservé.

| Facteur | État client | Tributaire natif inchangé |
|---|---:|---:|
| Rapport de prestige au-delà duquel la contribution devient négative | >1fois celui du sujet | >1,5fois |
| Rapport de puissance militaire au-delà duquel la contribution devient négative | >2,5fois celle du sujet | >5fois |
| Tribut financier de base | 0% | 20% |
| Diplomatie propre | Oui | Oui |
| Participation automatique aux guerres du suzerain | Non | Non |

Pour un rapport `r = puissance du suzerain / puissance du sujet`, prestige client : au-dessus de1, contribution `−clamp(r/100,0,01,0,05)` ; sinon `min(1/r/5,0,5)`. Puissance militaire client : au-dessus de2,5, `−clamp(r/50,0,01,0,10)` ; sinon `min(2,5/r/10,0,5)`. Les cas natifs de valeur nulle évitent la division par zéro et conservent leurs effets. Le test strict`>` est conservé : l'égalité au seuil n'est pas un bonus négatif.

Ces rapports concernent la **projection de puissance**, pas un nombre fixe de bataillons ; qualité et effectifs comptent. Ils décrivent deux contributions à la tendance, pas une garantie de désir de liberté décroissant : relations, économie, ferveur, souveraineté nationale et autres facteurs natifs continuent de s'appliquer. Aucun bonus global aux autres sujets ni baisse artificielle forfaitaire n'est ajouté.

La chaîne reste **État client → tributaire → vassal → intégration**. Les actions d'augmentation/diminution d'autonomie, et l'exclusion des paiements supplémentaires du client, sont conservées et contrôlées.

## Capacité éthiopienne et limites

Population déclarée ETH : **871059**, dont **783931 hors cohortes explicitement esclaves**, inchangée. Loi effective déclarée : levées paysannes, taux de conscription 4%, plafond 25 niveaux par État ; diviseur natif 1000. Plafond statique : `min(25,floor(783931×0,04/1000)) =25`, supérieur aux15 réserves demandées. Les10 réguliers restent sous le plafond 25 des casernes.

La loi ne permet de recruter que des paysans. Le plafond calculé n'est ni une observation de la répartition des emplois au premier tick, ni une garantie de remplissage immédiat des unités, ni une validation du budget. Les conscrits sont des réserves déclarées, pas15 bataillons mobilisés en permanence. Aucun bâtiment civil ni recette n'est modifié pour financer cette armée ; il s'agit du choix de gameplay demandé, pas d'un ordre de bataille historique de 1776.

## Revue mondiale des dépendances

Voir `REVIEW.md` et l'inventaire calculé :35 liens actifs de suzerains non reconnus examinés. Trois conversions éthiopiennes installées ; aucun nouveau sujet indépendant créé faute de preuve suffisamment précise. Les autres candidats et les rapports de tribut effectivement documentés sont distingués. Aucun lien impérial avec le Choa ou les royaumes méridionaux n'est déduit de la seule distance.

## Vérification et préservation

Commande de vérification : Python `tools/client_state_r2.py validate` ; résultat effectif : **90/90 contrôles statiques réussis**, dans `STATIC_CHECKS.json`, cas numériques évalués à partir des expressions installées dans `SCRIPT_VALUE_BOUNDARY_TESTS.json`. Le reçu R1 est conservé comme preuve de sa livraison antérieure ; ses anciennes attentes de noms et de pixels ne sont pas réécrites comme des tests R2.

Préimages des fichiers courants, empreintes, version Git en lecture seule, art source et inventaire avant installation : `BASELINE.json`, `preimages/`, `INSTALLED.json`, `ASSETS.json`, `DELIVERY_MANIFEST.json`. Les protections couvrent les fichiers de carte, POP, technologies, recettes, événements, interface et suivi SERG extérieurs au lot. Les blocs militaires des autres pays sont comparés octet par octet. Aucune écriture Git et aucun vanilla modifié.

## Contrôle moteur restant

Sur une nouvelle partie 1776 : ouvrir le tableau des sujets et le panneau d'un client ; vérifier nom, icônes et absence de doublon ; comparer les infobulles de tendance prestige/armée d'un client et d'un tributaire ; vérifier les trois liens éthiopiens sans paiement ; confirmer10 réguliers et15 réserves, puis mobiliser ces réserves et observer le remplissage/coût ; contrôler une transition client/tributaire et sauvegarde/rechargement. Ces vérifications sont préparées, **pas déclarées réalisées**. Elles ne sont pas un nouveau test territorial imposé entre deux lots.
