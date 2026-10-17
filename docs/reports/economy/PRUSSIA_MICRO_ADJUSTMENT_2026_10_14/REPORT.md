# Ajustements de départ de la Prusse — 14 octobre 2026

Modifications appliquées aux données de **nouvelle partie**, pas à une sauvegarde en cours. La localisation « westreben » a été confirmée par le joueur comme la **Prusse-Occidentale / Westpreußen**, et non la Westphalie.

| État prussien | Bâtiment | Avant | Après |
|---|---|---:|---:|
| Brandebourg | Administration | 13 | 7 |
| Brandebourg | Manufacture d’armes | 4 | 6 |
| Brandebourg | Élevage | 8 | 4 |
| Haute-Silésie / Oberschlesien | Mine de fer | 1 | 3 |
| Partie prussienne du Brunswick | Mine de plomb | 0 | 1 |
| Prusse-Occidentale | Manufacture de papier | 0 | 2 |
| Basse-Silésie / Niederschlesien | Élevage | 8 | 10 |
| Poméranie | Élevage | 8 | 10 |
| Basse-Silésie / Niederschlesien | Manufacture textile | 3 | 0 |

Les quatre niveaux d’élevage déplacés restent donc présents dans le total mondial : deux en Basse-Silésie, deux en Poméranie. Leurs recettes, réserves et détenteurs économiques sont conservés : le manoir propriétaire reste situé en Brandebourg, alors que les quatre niveaux de production sont désormais répartis dans les deux États destinataires. Aucun habitant n’est créé, supprimé ou déplacé par cette opération.

La suppression textile concerne exactement les trois niveaux montrés dans la capture en Niederschlesien : deux niveaux détenus par le quartier d’affaires et un niveau auto-détenu. La déclaration de bâtiment et ses trois niveaux d’appropriation sont retirés, sans supprimer les populations correspondantes ni d’autres industries textiles.

## Fichiers de jeu modifiés

- `common/history/buildings/00_west_europe.txt` : administration et armes en Brandebourg.
- `common/history/buildings/02_east_europe.txt` : fer en Haute-Silésie et retrait textile en Basse-Silésie.
- `common/history/buildings/98_build_start_1776_world_redistribution.txt` : élevages du Brandebourg, huit à quatre.
- `common/history/buildings/99_1776_prussian_start_micro_adjustment.txt` : deux élevages dans chacun des deux États destinataires, plomb du Brunswick prussien et papier en Prusse-Occidentale.

Les camps de bûcherons ajoutés précédemment restent inchangés. Aucun découpage, RGB, propriétaire territorial, gouvernement, unité, population, technologie ou fichier du Saint-Empire n’est modifié.

## Choix des destinations agricoles

Le calcul est dérivé des groupes de bâtiments et méthodes de production réellement présents dans le mod : élevage à une unité d’infrastructure par niveau, réseaux routiers à trois unités par niveau à effectif complet, ports éventuels, base de trois et trait de l’Oder à quinze. Il inclut les bâtiments de départ écrits, y compris les anciennes déclarations répétées, sans corriger ces répétitions ni les assimiler à un résultat moteur.

Après toutes les modifications, dont le retrait des textiles :

| Destination | Besoin des bâtiments écrits | Capacité nominale calculée | Marge nominale | Niveaux ruraux écrits / terres régionales |
|---|---:|---:|---:|---:|
| Basse-Silésie | 10 | 30 | +20 | 10 / 90 |
| Poméranie | 18,5 | 30 | +11,5 | 10 / 55 |

Ce calcul justifie le choix des destinations, **mais n’est pas une mesure en jeu**. Il ne simule pas les emplois réellement pourvus, les pénuries, les bâtiments générés automatiquement, les modificateurs dynamiques, les bonus de population ou de technologies. Il faut vérifier l’infrastructure effective et l’accès au marché dans une nouvelle partie. Les anciens chiffres avant retrait textile restent dans `INFRASTRUCTURE_FORECAST.json` ; le résultat final est enregistré séparément dans `FINAL_INFRASTRUCTURE_FORECAST.json`.

## Vérifications

- Première étape, ajustements prussiens : **2 202 / 2 202 contrôles statiques réussis**, avant le retrait textile supplémentaire.
- Deuxième étape, retrait textile : **2 187 / 2 187 contrôles réussis**. Cette étape vérifie aussi les neuf niveaux finaux du tableau ci-dessus.
- Population mondiale inchangée : **835 804 980** ; cultures, religions, attributs, unités, propriétaires territoriaux et gouvernements préservés.
- Comparaisons exactes des déclarations, recettes, réserves et détenteurs économiques ; seuls les changements demandés sont autorisés.
- Méthodes de production et technologies prussiennes compatibles ; ressources de fer et de plomb existantes, sans augmentation des plafonds régionaux.
- Partie prussienne du Brunswick ciblée uniquement : ni BRA ni HAN ne reçoivent la mine.
- Les **44 doublons RGB et 12 références invalides hérités** restent identiques à la baseline ; aucun nouveau cas.
- Empreintes des autres fichiers de jeu et état de HEAD/index conservés. Aucun commit, merge, changement de branche ou push.

Les anciens rapports souabes et industriels restent des attestations de leurs étapes respectives : leurs baselines ne sont pas réécrites pour masquer ces nouvelles modifications économiques volontaires. Les preuves successives se trouvent dans `VALIDATION.json`, puis `LOWER_SILESIA_TEXTILE_REMOVAL/VALIDATION.json`.

Statut moteur : **NOT_YET_TESTED**. Vérifier dans une nouvelle partie les niveaux du tableau, l’infrastructure et les salariés des nouveaux bâtiments. Les bâtiments déjà présents dans une sauvegarde ne disparaissent pas du seul fait de cette modification du mod.
