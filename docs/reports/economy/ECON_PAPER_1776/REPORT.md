# ECON-PAPER-1776

Date de l’intervention : 17 octobre 2026. Départ représenté : 1er janvier 1776.

Les quatre implantations demandées sont installées aux niveaux totaux 4, 3, 2 et 1. Les deux niveaux ajoutés précédemment en Prusse-Occidentale sont retirés. Le gain net est de huit niveaux de papeterie. Les contrôles statiques passent ; aucune baisse de prix ni validation moteur n’est revendiquée.

## Implantations

| Papeterie | Pays | State_ID | Région du jeu | Avant | Après | Méthodes | Source historique |
|---|---|---:|---|---:|---:|---|---|
| Franzensthal, près d’Ebergassing | AUS | 51 | STATE_AUSTRIA | 0 | 4 | Pressage de pâte, sans automatisation, sans collecte de données | [Musée de Basse-Autriche](https://www.gedaechtnisdeslandes.at/orte/ort/ebergassing/) |
| Wolfswinkel, près d’Eberswalde | PRU | 65 | STATE_BRANDENBURG | 0 | 3 | Idem | [Office de tourisme d’Eberswalde](https://tourismus-eberswalde.de/entdecken-und-erleben/kunst-kultur-geschichte/baukultur/papierfabrik-wolfswinkel/) |
| Niederzwönitz | SAX | 73 | STATE_SAXONY | 0 | 2 | Idem | [Musée municipal de Zwönitz](https://www.zwoenitz.de/stadtleben/kultur-freizeit/museen/technisches-museum-papiermuehle-niederzwoenitz) |
| Reinerz, aujourd’hui Duszniki-Zdrój | PRU | 155 | STATE_LOWER_SILESIA | 0 | 1 | Idem | [Office de tourisme de Duszniki](https://visitduszniki.pl/mlyn-papierniczy/) |

Les quatre subdivisions ne contenaient aucune papeterie déclarée avant cette intervention, y compris après résolution des fichiers vanilla remplacés par le mod. Un seul ajout de papeterie est déclaré pour chacun des quatre couples région/pays. Les nouvelles installations sont détenues par les districts financiers domestiques de leur région. Elles ne représentent pas des entreprises nominatives dans le moteur.

La vérification géographique supplémentaire de Reinerz, par le modèle de géoréférencement existant, situe son emplacement approximatif dans la province `xC00121`, attribuée à `STATE_LOWER_SILESIA / PRU`. Aucun dessin de frontière n’a été modifié.

Les niveaux constituent une calibration de gameplay demandée par le joueur. Ils ne correspondent pas au nombre documenté de moulins ni à une capacité industrielle historique mesurée. Les preuves et limites figurent dans [HISTORICAL_PAPER_MILLS.md](HISTORICAL_PAPER_MILLS.md).

## Identification de « Westburn »

L’ajout antérieur est précisément identifié dans `common/history/buildings/99_1776_prussian_start_micro_adjustment.txt` : `STATE_WEST_PRUSSIA`, identifiant 158, propriétaire territorial PRU, bâtiment `building_paper_mill`, deux niveaux détenus par le district financier prussien de Prusse-Occidentale.

Le générateur antérieur `tools/prussian_start_micro_adjustment.py` indique le même emplacement, ainsi que le rapport préexistant `docs/reports/economy/PRUSSIA_MICRO_ADJUSTMENT_2026_10_14/PLAN.json`. Il s’agit donc de la Prusse-Occidentale, et non d’une papeterie arbitrairement choisie ailleurs. Seule cette déclaration de deux niveaux a été retirée. Les fermes déplacées et la mine de plomb du même fichier sont conservées à l’identique.

## Complément forestier et agricole

| Région et propriétaire | Bâtiment | Avant | Après | Décision |
|---|---|---:|---:|---|
| Brandebourg / PRU | Camps de bûcherons | 6 | 1 | Déplacement de cinq niveaux, propriété publique prussienne conservée |
| Basse-Silésie / PRU | Camps de bûcherons | 0 | 3 | Bois ordinaire, exploitation forestière organisée |
| Haute-Silésie / PRU | Camps de bûcherons | 0 | 2 | Exploitation organisée avec sélection de bois dur |
| Saxe / SAX | Camps de bûcherons | 0 | 2 | Deux niveaux supplémentaires, districts financiers saxons |
| Bavière / BAV | Fermes d’élevage | 10 | 15 | Cinq niveaux supplémentaires, manoirs bavarois |

Le terme « Silésie prussienne » du complément est interprété comme `STATE_UPPER_SILESIA / PRU`, distinct de la Basse-Silésie explicitement nommée. La sélection de bois dur est activée dans les deux niveaux de Haute-Silésie. La Basse-Silésie conserve du bois ordinaire pour les papeteries.

Le déplacement porte sur cinq niveaux de camps : trois niveaux de papeterie consomment `3 × 1,5 = 4,5` points d’infrastructure, tandis qu’un niveau de camp en consomme un. L’arrondi à cinq niveaux libère cinq points et abaisse de 0,5 point la consommation des bâtiments explicitement déclarés du Brandebourg. Le sixième niveau de camp reste sur place. Les autres méthodes et l’actionnariat des cinq niveaux déplacés sont conservés.

Les plafonds forestiers régionaux restent inchangés. Les niveaux de camps déclarés après intervention restent inférieurs aux plafonds régionaux : Brandebourg 1/6, Basse-Silésie 3/10, Haute-Silésie 2/4 et Saxe 2/6. Le partage exact des ressources des régions divisées relève du moteur. Les cinq fermes supplémentaires portent l’élevage bavarois à quinze niveaux ; la capacité arable régionale n’est pas modifiée.

## Production, travail et infrastructure

La méthode native `pm_pulp_pressing` fournit une base de 40 unités de papier, consomme 30 unités de bois et ouvre 5 000 postes par niveau. Les quatre implantations représentent donc 400 unités de papier et 300 de bois consommé par semaine à plein emploi. Après retrait des deux niveaux précédents : **+320 unités de papier, +240 unités de bois consommé et +40 000 postes papetiers nets**. Les bonus de rendement, les prix et les pénuries ne sont pas simulés.

| Subdivision | Population écrite | Variation de demande d’infrastructure | Demande après | Capacité nominale écrite après | Marge nominale |
|---|---:|---:|---:|---:|---:|
| Basse-Autriche / AUS | 1 638 057 | +6 | 29 | 47 | 18 |
| Brandebourg / PRU | 665 983 | −0,5 | 34 | 58 | 24 |
| Saxe / SAX | 1 270 098 | +5 | 39 | 48 | 9 |
| Basse-Silésie / PRU | 783 411 | +4,5 | 14,5 | 30 | 15,5 |
| Haute-Silésie / PRU | 300 385 | +2 | 13 | 30 | 17 |
| Bavière / BAV | 1 231 183 | +5 | 16 | 29 | 13 |
| Prusse-Occidentale / PRU | 325 344 | −3 | 14 | 15 | 1 |

La capacité nominale additionne les valeurs de base, les traits régionaux et la production d’infrastructure des méthodes déclarées à plein fonctionnement. La demande porte sur les bâtiments explicitement déclarés. Ce calcul ne mesure pas l’accès au marché en partie : il exclut notamment les bâtiments urbains ou de propriété créés implicitement, les variations d’emploi, les effets de population et les multiplicateurs nationaux. Aucun niveau ni méthode de transport n’a été modifié.

La population totale ne constitue pas une réserve de travailleurs immédiatement disponibles. Les historiques de population ne renseignent pas le chômage et les qualifications après initialisation. Le recrutement effectif, les salaires concurrentiels et l’approvisionnement en bois restent à vérifier en jeu. Aucune population n’a été créée ou déplacée.

Voir [MARKET_BALANCE_AUDIT.md](MARKET_BALANCE_AUDIT.md), `BUILDINGS_BEFORE_AFTER.csv` et `PAPER_PRODUCTION_ESTIMATE.csv` pour les bilans.

## Périmètre et validation

Trois fichiers de jeu seulement ont été écrits :

- `common/history/buildings/99_1776_prussian_start_micro_adjustment.txt` : retrait exact de la papeterie de deux niveaux.
- `common/history/buildings/99_1776_prussian_forestry_addon.txt` : six niveaux de camps deviennent un dans le Brandebourg ; la Poméranie reste identique.
- `common/history/buildings/99_1776_econ_paper_forestry_livestock.txt` : ajouts demandés et cinq niveaux de camps déplacés.

Les grands fichiers d’historique partagés avec l’agent cartographique n’ont pas été réécrits. Les textes des deux petits fichiers préexistants ont été comparés avant/après pour préserver toutes leurs autres déclarations, propriétaires et méthodes. Les contrôles couvrent les niveaux finaux exacts, les seuls écarts de bâtiments autorisés, les groupes de méthodes et leurs technologies déjà acquises. Les empreintes des fichiers protégés sont restées identiques pendant l’application. Aucun fichier vanilla, prix de base, technologie, loi, formation, relation diplomatique, frontière, ressource ou population n’a été écrit. Aucun commit ni changement d’index ou de branche Git n’a été effectué.

Le statut détaillé est dans `VALIDATION.json`. Le test moteur reste à réaliser selon [RUNTIME_TEST_PLAN.md](RUNTIME_TEST_PLAN.md).
