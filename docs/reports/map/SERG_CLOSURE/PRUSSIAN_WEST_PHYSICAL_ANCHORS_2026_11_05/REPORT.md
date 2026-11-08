# Prusse occidentale — repères physiques et noyau B de Ravensberg

5 novembre 2026 ; scénario du 1er janvier 1776. **32 cellules supplémentaires attribuées à PRU**, sous-lot **PW-RAVENSBERG-B32**, `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`. Aucun reçu humain. Le test moteur est différé jusqu'à la fin de la passe prussienne, conformément à la dernière instruction du joueur.

La mission autorisait une tentative bornée de recherche de repères, puis une solution politique pragmatique si la précision restait insuffisante. La recherche de précision n'est pas prolongée automatiquement. Aucun territoire bavarois ou nouveau pays créé.

## Résultat concret

| Portion source | Région technique | Transfert vers PRU | Nouvelle province |
| --- | --- | ---: | --- |
| SCM, frange de `x1BA4F6` | WESTPHALIA | 9 cellules | `xEEC400` |
| WPM, frange de `x910095` | WESTPHALIA | 6 cellules | `xEEC401` |
| HAN, frange de `xEDAC00` | HANNOVER | 17 cellules | `xEEC402` |

Les parents restent présents chez leurs propriétaires précédents. Les 32 coordonnées et toutes les portions conservées sont dans [GEOMETRY.json](GEOMETRY.json). [Avant/après installé](RAVENSBERG_BEFORE_AFTER.png). **Ce noyau ne constitue pas tout le comté de Ravensberg ni toute la frontière occidentale de la Prusse.**

Le contour vient de la carte de Schloenbach de **1772**, lue pendant la passe précédente. Une bande d'une cellule sur les limites du dessin est écartée ; les portions WPO/Osnabrück et toutes les cellules déjà prussiennes sont protégées. L'interprétation politique B laisse ainsi des franges ouvertes, notamment les diagnostics Bünde/Oldendorf et Vlotho ; elle ne certifie pas leur attribution actuelle. Lippe est inchangée. Les limites antérieures de Minden, Lingen et Tecklenburg ne sont pas retracées.

## Repères trouvés et décision sur le positionnement

Six correspondances physiques explicites ont été relevées dans le dessin des fleuves et les données hydrographiques Natural Earth déjà présentes dans le dépôt. Les deux jonctions Rhin–Moselle et Rhin–Main sont nettes ; les coudes de la Weser, du Rhin et de la Meuse sont des correspondances plus grossières. **Il ne s'agit pas de positions GPS certifiées dans le moteur.**

| Repère | Écart R5, cellules | Écart Miller, cellules |
| --- | ---: | ---: |
| Rhin–Moselle | 3,42 | 11,22 |
| Rhin–Main | 2,50 | 8,11 |
| Boucle de la Weser, Rehme–Porta/Vlotho | 3,29 | 7,79 |
| Coude de la Weser, secteur de Hameln | 3,60 | 4,52 |
| Coude occidental du Rhin, Düsseldorf | 3,98 | 14,54 |
| Saillant de la Meuse, Venlo–Arcen | 5,81 | 13,04 |

Les deux anciens modèles restent **inchangés**. Ces observations favorisent le modèle R5 pour une traduction politique grossière dans ce secteur. Elles ne lui donnent pas une garantie cadastrale, et n'invalident pas les usages antérieurs du modèle Miller dans d'autres régions.

Un nouvel ajustement sur les trois premiers repères a aussi été essayé une seule fois. Il interpole ces trois points, mais échoue sur les trois témoins réservés : **6,61 ; 12,86 ; 10,58 cellules**. Il est donc **rejeté**, sans déplacement de la carte pour le faire correspondre. [Repères et provenance](PHYSICAL_ANCHORS.json), [ajustement rejeté](PHYSICAL_MODEL.json), [superposition diagnostique](PHYSICAL_RIVER_OVERLAY.png).

La carte de Ravensberg est raccordée à des coordonnées modernes de villes issues de GeoNames, puis à l'hypothèse R5. Six villes servent à lire la carte et trois autres à contrôler cette lecture. Les écarts des trois contrôles sur la source sont de **0,64 ; 0,13 ; 1,24 cellule** ; ils ne mesurent pas l'erreur absolue du placement dans le jeu. [Lecture de la carte](RAVENSBERG_TRACE_REVIEW.jpg), [matrices et limites](RAVENSBERG_TRACING.json), [références géographiques](CITY_GEO_REFERENCES.json).

Le noyau de Berg de la passe précédente n'est pas déplacé : les 39 cellules proposées par l'ancien modèle Miller ne deviennent pas des erreurs avérées. L'exigence antérieure d'un transfert commun aux deux modèles n'est plus employée comme blocage général de la Prusse.

## Populations et dépendances

**11 559 habitants existants** sont réaffectés à PRU avec leurs profils culturels et religieux, à partir des subdivisions sources complètes : SCM **1 990**, WPM **1 974**, HAN **7 595**. C'est une ventilation technique provisoire, **pas un recensement de Ravensberg en 1776**. Aucun total historique du comté entier n'est attribué à ce noyau partiel. Le total mondial écrit reste **837 328 654** ; aucune compensation extérieure.

Tous les bâtiments, niveaux, PM, détenteurs économiques, unités, pays, lois et technologies sont conservés. Aucune nouvelle portion nationale n'est créée : PRU possède déjà des portions dans les deux régions techniques. Aucun repère physique de ville, mine ou ferme n'est déplacé. Les trois terrains enfants reprennent leurs parents.

Le registre impérial passe de **592 à 595 titres RGB**, avec les mêmes droits anciens et la même étendue physique. Les trois nouveaux titres appartiennent à PRU ; aucun membre, électeur ou statut impérial supplémentaire. Les sept dérivés textuels concernés sont préparés par comparaison avec le compilateur courant ; aucun chevauchement concurrent n'est détecté. [Préparation](PLAN.json), [contrôle du compilateur](COMPILER_PREFLIGHT.json), [installation](INSTALLATION.json), [différence revue](REVIEW.diff).

## Vérifications et limites

[VALIDATION.json](VALIDATION.json) donne les contrôles de cette version et [TEST_RESULTS.json](TEST_RESULTS.json) la nouvelle exécution des tests existants. Les preuves et données des précédentes passes sont conservées par empreintes ; aucun Git d'écriture ni changement du vanilla.

Résultats exécutés sur la livraison : **40/40 contrôles statiques et de conservation**, **11/11 contrôles finaux du suivi**, **73 tests ciblés exécutés : 72 réussis, 1 ignoré**, aucun échec ni erreur. Les cinq suites couvrent le suivi canonique, les garde-fous du registre, les reçus et les primitives de géoréférencement. Le contrôle ignoré concerne uniquement l'ancienne interdiction de toute écriture lors de l'initialisation ; il ne certifie pas cette installation. Le validateur canonique retourne `PASS` et `git diff --check` retourne 0. Aucun moteur de jeu exécuté.

La première vérification signalait une déclaration répétée de `x26A0BA`, Yukon/ATB. Elle existe déjà, identique, dans la baseline de cette passe. L'échec brut reste dans [INITIAL_VALIDATION.json](INITIAL_VALIDATION.json). Le contrôle amendé exige l'absence de nouveau doublon et l'unicité des trois nouvelles provinces ; **l'unicité globale reste une dette héritée**, pas une réussite annoncée. Les onze références orphelines héritées ne sont pas modifiées.

Deux préparations ont été arrêtées avant installation pour des problèmes du générateur de patch : décalage de position dû au BOM, puis ancre ne reconnaissant pas CRLF. Ces problèmes ont été corrigés dans le nouvel outil ; les scripts installés ont été reparsés avant écriture. Aucune de ces préparations refusées n'a été chargée en jeu. [Journal des contrôles de développement](DEVELOPMENT_CHECKS.json).

## Suivi et prochaine action

**93/235 points, 39,57 %, 32/81 tâches qualifiées**, avant comme après. Le noyau est installé, pas reçu humainement. `SC5-PRUSSIAN-WEST` reprend `IN_PROGRESS`, avec ce sous-lot prêt au moteur ; ses obligations régionales restantes ne sont ni supprimées ni réputées satisfaites.

Les tests moteur sont regroupés **à la fin de la Prusse** : [protocole groupé](PLAYER_TEST_PROTOCOL_GROUPED.md). Leur attente ne bloque pas les corrections indépendantes autorisées. Pour la suite géographique, une autre frontière prussienne peut être abordée ; la candidate préparée est la frontière **Glatz/Silésie** de `SC3-SILESIA-LUSATIA`. Elle n'est pas commencée ici. Aucun second ajustement des anciens modèles ni nouvelle chasse aux micro-limites occidentales n'est lancé automatiquement.
