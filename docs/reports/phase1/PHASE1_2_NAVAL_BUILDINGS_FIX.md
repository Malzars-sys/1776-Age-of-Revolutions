# Phase 1.2 - Correction des batiments navals 1.13

Branche : `phase1-critical-log-cleanup`

## 1. Erreurs trouvees

Le diagnostic Phase 1 signalait des erreurs :

```text
PostValidate of effect 'create_building' returned false
```

Les erreurs venaient des anciens batiments et production methods navals utilises dans `common/history/buildings` :

- `building_military_shipyard`
- `pm_military_shipbuilding_wooden`
- `pm_military_shipbuilding_wooden_2`

Ces IDs correspondent a l'ancien systeme de chantiers navals militaires. Victoria 3 1.13 / The Great Wave utilise un systeme naval refondu avec des shipyards unifies, ce qui rend ces references obsoletes.

## 2. Anciens IDs remplaces

Remplacements effectues :

| Ancien ID | Nouveau ID utilise | Raison |
| --- | --- | --- |
| `building_military_shipyard` | `building_shipyard` | Equivalent minimal le plus evident apres fusion des shipyards |
| `pm_military_shipbuilding_wooden` | `pm_basic_shipbuilding` | PM deja utilisee par les shipyards voisins et non signalee par les logs |
| `pm_military_shipbuilding_wooden_2` | `pm_basic_shipbuilding` | Pas d'equivalent militaire evident sans refonte navale ; retour temporaire vers la PM shipyard de base |

Rien n'a ete invente pour les nouveaux systemes 1.13 de flotte, supply ships ou naval bases. Cette phase retire seulement les IDs obsoletes qui faisaient echouer `create_building`.

## 3. Fichiers modifies

Fichiers modifies :

- `common/history/buildings/00_west_europe.txt`
- `common/history/buildings/01_south_europe.txt`
- `common/history/buildings/03_north_africa.txt`
- `common/history/buildings/05_north_america.txt`
- `common/history/buildings/11_east_asia.txt`
- `common/history/buildings/15_russia.txt`

Volume de correction :

| Fichier | `building_military_shipyard` remplaces | PM militaires remplacees |
| --- | ---: | ---: |
| `00_west_europe.txt` | 8 | 8 |
| `01_south_europe.txt` | 9 | 9 |
| `03_north_africa.txt` | 1 | 1 |
| `05_north_america.txt` | 2 | 2 |
| `11_east_asia.txt` | 1 | 1 |
| `15_russia.txt` | 3 | 3 |
| Total | 24 | 24 |

## 4. Pourquoi la correction est minimale

La correction garde les blocs `create_building` existants, les pays proprietaires, les niveaux, les reserves et les emplacements historiques. Elle ne change que les IDs invalides :

- ancien batiment militaire naval vers shipyard unifie ;
- ancienne PM militaire navale vers PM shipyard de base deja presente dans les memes fichiers.

Aucune formation militaire n'a ete modifiee. Aucun event n'a ete modifie. Aucune localisation n'a ete modifiee. Aucun systeme naval 1.13 complet n'a ete reconstruit dans cette phase.

La correspondance `pm_military_shipbuilding_wooden_2 -> pm_basic_shipbuilding` est volontairement conservatrice : il n'y a pas d'equivalent militaire evident dans le contexte de cette phase, donc le but est seulement d'obtenir des `create_building` valides.

## 5. Tests a faire ensuite

1. Lancer Victoria 3 1.13 avec uniquement le mod active.
2. Demarrer une partie en 1776.
3. Tester en priorite les pays navals concernes :
   - Grande-Bretagne / `GBR` ou `IREK`
   - France
   - Espagne
   - Portugal
   - Pays-Bas
   - Suede / Dennor
   - Russie
   - Etats-Unis
   - Qing
   - Turquie / Ottomans
4. Laisser tourner au moins un mois.
5. Verifier `logs/error.log` et `logs/debug.log`.
6. Confirmer la disparition des erreurs `PostValidate of effect 'create_building' returned false` pour les fichiers suivants :
   - `00_west_europe.txt`
   - `01_south_europe.txt`
   - `03_north_africa.txt`
   - `05_north_america.txt`
   - `11_east_asia.txt`
   - `15_russia.txt`

Si de nouvelles erreurs navales apparaissent ensuite, elles doivent etre traitees dans une phase separee, probablement avec les formations militaires/navales et les nouveaux systemes de supply ships.
