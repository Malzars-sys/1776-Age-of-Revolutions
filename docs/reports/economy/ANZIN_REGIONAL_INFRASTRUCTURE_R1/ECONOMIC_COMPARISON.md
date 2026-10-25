# Comparatif économique détaillé

Les montants sont des estimations hebdomadaires par niveau/module à plein emploi. Prix de référence lus : transport 30 £, bois 20 £, outils 40 £, calcaire 20 £, ciment 40 £, produits pétroliers lourds 30 £. Aucun prix n’est modifié par le patch.

Salaire de référence : 500 £ par semaine pour 10 000 ouvriers de poids salarial 1, valeur native de secours `NORMAL_WAGE_RATE_FALLBACK`, **pas un salaire français observé**. Masse salariale = somme(emplois × poids salarial de profession) × taux / 10 000. Les poids proviennent du catalogue effectif du mod et du vanilla canonique.

Solde = recettes − intrants − salaires. Sa partie négative est un besoin de financement indicatif, pas la subvention exacte calculée par le moteur. Trésorerie, impôts, dividendes, ajustements des salaires, embauche, pénuries et formation endogène des prix ne sont pas simulés.

| Méthode | Emplois avant → après | Salaires £ | Intrants £ | Tickets | Recettes £ | Solde £ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Terre | 1 000 → 400 | 52,50 → 21 | 0 | 0 | 0 | −52,50 → −21 |
| Péage | 1 000 | 68,75 | 160 | 2 → 3,2 | 60 → 96 | −168,75 → −132,75 |
| Pavées | 1 000 | 67,50 | 220 | 4 | 120 | −167,50 |
| Goudronnées | 1 000 | 76,25 | 520 | 6 | 180 | −416,25 |

| Méthode | Emplois après | Intrants inchangés | Infrastructure fixe | Autres effets conservés |
| --- | --- | --- | ---: | --- |
| Terre | 360 ouvriers, 40 employés | Aucun | 3 | Service d’infrastructure, sans tickets marchands |
| Péage | 750 ouvriers, 150 employés, 100 bureaucrates | 4 bois, 2 outils | 7 | Population : coefficient +0,02, plafond +0,5 |
| Pavées | 600 ouvriers, 200 machinistes, 100 ingénieurs, 100 employés | 5 calcaire, 3 outils | 12 | Population : +0,05, plafond +1 |
| Goudronnées | 400 ouvriers, 250 machinistes, 150 ingénieurs, 200 employés | 4 outils, 5 ciment, 5 calcaire, 2 produits pétroliers lourds | 20 | Population : +0,1, plafond +2 ; consommation d’automobiles : +0,01 |

Les méthodes avancées restent plus capacitaires : 4 et 6 tickets contre 3,2 ; 12 et 20 points fixes contre 7, avec des plafonds de population supérieurs. Leur intérêt demeure lié à la capacité et au développement régional, sans prétendre qu’elles deviennent financièrement autonomes. Les routes goudronnées restent coûteuses ; leur rendement réel demande une mesure avant un autre réglage.

## Situations comparées

Les populations indiquent le contexte des scénarios. Le salaire et le prix sont des hypothèses imposées ; la population synthétique ne calcule pas une demande native.

| Situation | Salaire / 10 000 £ | Prix transport £ | Déficit péage avant £ | Après £ | Réduction |
| --- | ---: | ---: | ---: | ---: | ---: |
| Référence | 500 | 30 | 168,75 | 132,75 | 21,33 % |
| Région peuplée, salaires élevés (3 M) | 900 | 30 | 223,75 | 187,75 | 16,09 % |
| Région rurale (0,2 M) | 300 | 30 | 141,25 | 105,25 | 25,49 % |
| Forte demande, prix +50 % | 500 | 45 | 138,75 | 84,75 | 38,92 % |
| Faible demande, prix −50 % | 300 | 15 | 171,25 | 153,25 | 10,51 % |
| Forte demande, intrants −25 % | 500 | 45 | 98,75 | 44,75 | 54,68 % |

L’objectif indicatif de −30 à −50 % est atteint dans le scénario de forte demande retenu ; il n’est pas universel. Les routes peu utilisées restent déficitaires. La réduction de 60 % du déficit propre aux routes en terre se dilue si le bâtiment utilise simultanément des canaux ou du rail coûteux.

Les 192 comparaisons incluent le demi-emploi et un débit de production de 1,1 représentant le bonus de prospérité d’Anzin. Le modèle applique ce débit aux intrants et aux sorties, séparément des salaires. Il ne monétise pas les gains d’infrastructure ou d’économies d’échelle.

## Prix, demande, IA et propriété

Le transport est local. Avec +60 % d’offre, une chute de prix de plus de 37,5 % efface le gain brut de recettes. `ECONOMICS.json` teste des baisses de 0, 10, 25, 37,5 et 50 %. Ces sensibilités ne prédisent pas les prix d’équilibre.

Les industries reprennent exactement les PM des mines. Aucun débouché nouveau avant `railways`. À plein emploi et avec au moins 1 000 ouvriers disponibles, le transport économise au maximum 50 £ de salaires au taux 500, contre 150 £ pour 5 tickets au prix de référence : son adoption par l’IA n’est donc pas garantie. Des tickets moins chers ou des salaires plus élevés le rendent plus intéressant. Le choix natif du nouveau groupe reste `most_profitable` par défaut.

Le bâtiment régional reste dans `bg_land_transport_network`, enfant de `bg_private_infrastructure` : il n’est pas directement financé comme une administration, mais conserve le modèle natif de subventions et de propriété transférable. `ownership_type = self`, les réserves, l’absence d’économies d’échelle et les règles de construction restent intacts. Les autres compagnies et les protections de l’IA contre les pénuries sont inchangées ; leurs infrastructures bénéficient du même réglage routier.

## Cumul d’automatisation : contrôle encore ouvert

Sur les combinaisons examinées, dépendances entre PM respectées et technologies présumées disponibles, 8 industries avaient déjà un coefficient brut d’ouvriers négatif ; 15 en présentent après copie du transport. Le moteur n’a pas été exécuté pour vérifier son traitement des emplois. Les sept cas supplémentaires demandent donc un test, notamment le textile très automatisé : 500 ouvriers avant, coefficient brut −500 après le transport. Il ne s’agit pas de populations négatives observées.

Le coefficient demandé de −1 000 est conservé exactement. Les autres automatisations ne sont pas modifiées dans cette passe. Les témoins et les périmètres de calcul sont consignés dans `INDUSTRIAL_EMPLOYMENT_SENSITIVITY.json`.

## Inventaire intégral

`PM_COMPARISON.csv` donne les deux versions de chacun des 19 modules : emplois par profession, salaires, quantités et coûts d’intrants, tickets, effets d’État, recettes et solde. `PM_BEFORE.json` et `PM_AFTER.json` conservent les références et technologies. Les quatre groupes se cumulent ; les valeurs ci-dessous décrivent les modules isolés et doivent être additionnées pour représenter un bâtiment réel.

Une sauvegarde automatique locale a été repérée mais son état est binaire. Les prix de marché observés et les subventions effectivement payées restent **non mesurés**. Aucun résultat statique n’est présenté comme une simulation en jeu.

| Module | Emplois avant → après | Salaires £ | Intrants £ | Tickets | Recettes £ | Solde £ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| `pm_traditional_road_network` | 1000,00 → 400,00 | 52,50 → 21,00 | 0,00 | 0,00 | 0,00 | -52,50 → -21,00 |
| `pm_turnpike_road_network` | 1000,00 | 68,75 | 160,00 | 2,00 → 3,20 | 60,00 → 96,00 | -168,75 → -132,75 |
| `pm_engineered_road_network` | 1000,00 | 67,50 | 220,00 | 4,00 | 120,00 | -167,50 |
| `pm_paved_road_network` | 1000,00 | 76,25 | 520,00 | 6,00 | 180,00 | -416,25 |
| `pm_no_canal_network` | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| `pm_industrial_canals` | 800,00 | 43,75 | 260,00 | 0,00 | 0,00 | -303,75 |
| `pm_engineered_canals` | 800,00 | 56,25 | 340,00 | 0,00 | 0,00 | -396,25 |
| `pm_no_rail_network` | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| `pm_early_trains` | 1000,00 | 60,00 | 360,00 | 20,00 | 600,00 | 180,00 |
| `pm_steam_trains` | 1000,00 | 62,50 | 450,00 | 25,00 | 750,00 | 237,50 |
| `pm_steam_trains_principle_transport_3` | 1000,00 | 62,50 | 540,00 | 30,00 | 900,00 | 297,50 |
| `pm_electric_trains` | 1000,00 | 68,75 | 540,00 | 35,00 | 1050,00 | 441,25 |
| `pm_electric_trains_principle_transport_3` | 1000,00 | 68,75 | 660,00 | 45,00 | 1350,00 | 621,25 |
| `pm_diesel_trains` | 1000,00 | 72,50 | 540,00 | 40,00 | 1200,00 | 587,50 |
| `pm_diesel_trains_principle_transport_3` | 1000,00 | 72,50 | 600,00 | 50,00 | 1500,00 | 827,50 |
| `pm_no_passenger_trains` | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 | 0,00 |
| `pm_wooden_passenger_carriages` | 100,00 | 7,50 | 160,00 | 10,00 | 300,00 | 132,50 |
| `pm_steel_passenger_carriages` | 200,00 | 15,00 | 250,00 | 15,00 | 450,00 | 185,00 |
| `pm_aluminium_passenger_carriages` | 200,00 | 15,00 | 250,00 | 20,00 | 600,00 | 335,00 |
