# TECH-R3 — décisions et limites historiques

Référence : 1er janvier 1776. Aucun contrôle statique ne certifie une rentabilité, un marché ou une production effectivement observés. Les sources établissent des capacités qualitatives ; les coefficients de recettes sont des approximations de jeu B.

## Ports commerciaux et établissements navals

Les 18 déclarations initiales en conflit utilisent `pm_basic_port`, qui exige `enclosed_dock_systems`, lui-même enfant de `state_dockyard_systems`. Cela ne prouve ni l’absence d’un port historique ni une production nulle en jeu. Les noms et descriptions du mod associent ce dernier ensemble à des établissements navals et des bassins protégés. Un commerce maritime ancien ne justifie pas automatiquement tout cet appareil militaire.

Trois cas sont installés : JAP/Kyushu, KOR/Busan, SUL/Mindanao. Les niveaux existants 2/1/1, les propriétaires économiques, les emplacements et les réserves sont conservés. La source concernant Jolo étaye le rôle commercial du sultanat SUL, sans prétendre établir le pixel ou le hub exact du port de Mindanao.

- [Ville de Nagasaki : port international](https://www.city.nagasaki.lg.jp/uploaded/attachment/4724.pdf), texte municipal indexé : activité internationale depuis le XVIe siècle, contacts chinois et néerlandais encadrés au XVIIIe. Ces restrictions ne signifient pas une absence de commerce. Aucun débit réel de 1776 n’est déduit du nombre de navires.
- [Douane de Busan : commerce du waegwan](https://customs.go.kr/busan/cm/cntnts/cntntsView.do?cntntsId=2386&mi=7394), page officielle consultée : site de Choryang à partir de 1678, échanges réglementés antérieurs à l’ouverture de 1876. La source ne justifie pas un chantier naval industriel national.
- [Poggio, Lopez et Tremml-Werner, recherche originale](https://onlinelibrary.wiley.com/doi/10.1111/aehr.70030), introduction et contexte consultés : réseau maritime de Sulu déjà établi au début du XVIIIe siècle. L’objet principal de l’étude est 1836 : aucune clause de ce traité, frontière ou quantité du XIXe n’est rétroprojetée en 1776. La notice [Warren 1977](https://archium.ateneo.edu/phstudies/vol25/iss1/4/) est une piste bibliographique, pas une lecture intégrale de son PDF.

Le nouveau procédé `pm_aor1776_traditional_commercial_harbor` utilise bois 9 + tissu 3 → marine marchande 6, avec 700 emplois (490 ouvriers, 140 employés et 70 bureaucrates), infrastructure 2. Les navires et petits services côtiers sont une abstraction de l’entretien et de la manutention avec des matériaux courants ; aucune nouvelle industrie ni aucun bien n’est créé. La collecte de données est explicitement désactivée dans les trois ports pour éviter une dépendance implicite à la métrologie.

Comparateur écrit : le port spécialisé utilise 6 clippers → 9 marine marchande, 1000 emplois et infrastructure 3. Ce n’est pas une baisse de production réelle déjà mesurée : l’ancien procédé avait un gate absent. Le nouveau procédé ne devient pas le défaut global ; mouillage, port de base et variantes ultérieures sont conservés. Il devient une alternative mondiale, mais seuls les trois historiques sélectionnent explicitement ce nouveau procédé.

Un premier modèle utilisait quatre clippers. Le contrôle des intrants a montré l’absence de chantier naval explicite chez KOR/SUL et des demandes d’isolationnisme. Ce modèle est archivé et remplacé par bois/tissu, qui existent dans les recettes de subsistance. Au prix de référence, les deux propositions coûtent 240 et donnent une valeur de service 300 : marge brute 60 avant salaires. Le procédé final reste légèrement moins efficace par emploi que le port spécialisé (60/700 contre 90/1000). PORT_COST_SENSITIVITY.csv contient aussi des pertes : aucune viabilité moteur garantie.

KOR demande l’isolationnisme ; SUL contient des demandes concurrentes d’isolationnisme et de mercantilisme dont certaines ont des gates absents. JAP conserve le sakoku. Les lois réellement actives et les marchés demandent un contrôle en jeu. TECH ne modifie aucune loi ni pacte pour ouvrir artificiellement le commerce. Les quinze autres sélections portuaires restent signalées, même si la nouvelle alternative est désormais disponible.

## Crédit et commerce ordinaire : deux attributions ciblées

`organized_financial_institutions` est un socle d’ère I sans parent. Sa description actuelle couvre comptabilité, crédit et intermédiation, sans exiger banque centrale ou bourse modernes. L’omettre pour toute une nation peut être incohérent sans justifier une baisse uniforme de son commerce.

PRU : la [notice du Münzkabinett de Berlin](https://ikmk.smb.museum/object?id=18230184), consultée via son texte indexé (ouverture directe indisponible), décrit la Banque royale fondée en 1765 et le bankotaler frappé en 1766 avec date 1765. Cette preuve antérieure à 1776 justifie le socle financier, pas un ensemble industriel supplémentaire.

TUS : l’[histoire institutionnelle de Monte dei Paschi](https://www.gruppomps.it/en/about-us/history.html) atteste les structures bancaires de 1624 et le contrôle gouvernemental renforcé en 1759. Le crédit siennois appartient alors au contexte toscan ; aucun territoire n’est ajouté. Une seule technologie est accordée à chacun des deux TAGs.

Les quatre centres existants restent en commerce normal : PRU/Brandenburg, Prusse orientale et Poméranie ; TUS/Toscane. Aucune capacité haute ou maximale, aucun emploi ni intrant de recette n’est augmenté. L’effet réel peut cependant différer d’un éventuel repli moteur antérieur vers le commerce limité. Le coût de marine marchande est un intrant, les recettes proviennent des échanges : l’absence de sortie de biens dans un PM de service ne prouve pas un déficit. Ne pas assimiler le solde de biens à la rentabilité commerciale.

Les consommateurs directs du socle sont le commerce normal et les recherches de crédit public, bourse et assurance. Ces descendants ne sont pas attribués. Les choix R2 de KND/Ceylan et CAR/Circars/Madras restent limités et compatibles ; aucune répétition ni extension de leurs corrections.

## Artillerie traditionnelle et normalisation de campagne

Le procédé `pm_cannons` ne décrit pas à lui seul une standardisation complète des calibres, affûts et unités. Les [données patrimoniales scientifiques indiennes](https://indiascienceheritage.gov.in/WarTechnology5.html) distinguent l’artillerie de bronze et de fer antérieure au XVIIIe siècle ; l’[objet de 1541 étudié par Durham](https://stories.durham.ac.uk/VRM_25-objects-19/) confirme des capacités de fabrication anciennes. Ces sources motivent la distinction conceptuelle, sans certifier la localisation, les effectifs ou le rendement précis des arsenaux MUG et MARATH en 1776.

Décision minimale : `pm_cannons` exige désormais seulement `organized_military_establishments`, déjà possédé par MUG et MARATH. Aucun `standardized_field_artillery`, acier industriel, coke, vapeur ou alliages national ajouté. La recette économique du fichier courant est intégralement conservée ; les nouveaux procédés de bronze et groupes d’ECON-ALLOYS sont réservés à cet agent.

La construction de nouvelles fonderies reste conditionnée à `standardized_field_artillery`. Deux arsenaux historiques peuvent sélectionner leur procédé ancien sans que l’on prétende leur donner les capacités d’extension d’une fonderie normalisée. Les unités et formations restent inchangées.

Le premier essai ajoutait aussi `organized_workshops` : le contrôle des 471 pays a révélé une perte de disponibilité pour GAL et MLT. Ce second parent est retiré avant livraison finale. Le modèle final ne retire aucune disponibilité existante ; les preuves du premier essai sont archivées. GLOBAL_AVAILABILITY_IMPACT.csv décrit les implications mondiales, sans construire de nouvelles fonderies.

## Dossiers laissés ouverts

132 sélections explicites ont encore un gate absent : 15 ports et 117 centres commerciaux. Les 54 gates de construction restent distincts, dont cinq bâtiments militaires. Les huit historiques absents et les alertes régionales de ressources demeurent dans leur file indépendante. Les groupes omis dans les historiques ne sont pas certifiés par une reconstruction de sélection explicite ; ils figurent dans les CSV et dans le protocole.

TECH ne valide pas les évolutions de Raguse ni les recettes ECON. Leurs versions courantes sont conservées et signalées séparément ; le reçu R2 reste attaché à sa livraison historique, sans couverture automatique de ces révisions.
