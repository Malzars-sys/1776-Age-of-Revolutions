# TECH8D — hausse progressive des coûts de recherche

Date : 30 septembre 2026. Demande : augmenter les coûts en points des ères, particulièrement les dernières, après l'introduction du prototype de laboratoires TECH8C.

## Valeurs appliquées

Coûts de base **par technologie** de l'ère, avant modificateurs et pénalités. Il ne s'agit pas d'un prix unique pour débloquer l'ère entière.

| Ère | Avant | Après | Hausse arrondie |
|---|---:|---:|---:|
| I | 2 500 | 3 000 | +20 % |
| II | 3 500 | 4 500 | +29 % |
| III | 4 500 | 6 000 | +33 % |
| IV | 6 000 | 8 000 | +33 % |
| V | 7 500 | 10 000 | +33 % |
| VI | 9 000 | 12 500 | +39 % |
| VII | 10 000 | 16 000 | +60 % |
| VIII | 11 250 | 20 000 | +78 % |
| IX | 12 500 | 25 000 | +100 % |
| X | 13 750 | 30 000 | +118 % |
| XI | 15 000 | 37 500 | +150 % |
| XII | 17 500 | 45 000 | +157 % |

Les valeurs exactes n'étaient pas imposées par l'utilisateur : cette courbe est un premier réglage, avec une hausse contenue aux premières ères et renforcée à partir de VII. Les derniers coûts dépassent le double de leur ancienne valeur. Ce choix ne constitue pas une mesure du rythme de recherche en partie ni une compensation quantitativement démontrée des laboratoires.

## Portée

Seul `common/technology/eras/00_tech3a_eras.txt` change dans le gameplay de ce lot. Le descripteur remplace déjà le dossier des ères du jeu par celui du mod ; les douze définitions locales restent donc la référence.

Pas de modification des prérequis, du classement des technologies, des technologies acquises au départ, de la production d'innovation, des pénalités de recherche anticipée ou des recettes / contributions des laboratoires. Les technologies déjà terminées ne sont pas retirées.

Les coûts cités dans les anciens rapports restent des relevés historiques et ne sont pas réécrits rétroactivement. Cette note définit la nouvelle base.

## Vérifications et suite

Contrôle des douze ères : une définition chacune, coûts tous augmentés, strictement croissants et correspondant au tableau. Contrôle du diff ciblé et réexécution du validateur statique TECH8C.

Le rythme réel reste à mesurer dans le moteur, avec et sans laboratoires : pays avancé, petit pays et économie à faible alphabétisation. Redémarrer le jeu pour charger les valeurs ; relever également le coût restant des recherches déjà engagées sur une copie de sauvegarde. Aucun essai moteur n'est revendiqué par cette passe.
