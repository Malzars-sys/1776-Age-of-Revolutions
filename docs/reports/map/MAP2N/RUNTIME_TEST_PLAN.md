# MAP2N — Test groupé après livraison complète

Statique : **MAP2N_READY_FOR_RUNTIME_VALIDATION**. Retour manuel du 2026-10-15 : **PASS_RUNTIME_USER_VALIDATED**, voir RUNTIME_USER_VALIDATION_2026_10_15.json. La durée et les points inspectés ne sont pas détaillés dans cette confirmation. Le protocole ci-dessous reste un guide, pas une liste automatiquement cochée. Aucune validation du prototype graphique n'en découle.

## Nouvelle partie

1. Vérifier Wismar et son territoire principal, puis la dépendance orientale de Benz : cinq cellules à SWE dans STATE_MECKLENBURG. La division en trois RGB conserve les parents et les composantes ; elle ne crée pas trois pays.
2. Vérifier l'Amt Neukloster : huit cellules à SWE, au-delà de la seule ville, dans STATE_MECKLENBURG. Les petits contours restent généralisés.
3. Vérifier Poel : île distincte, trois cellules à SWE et une cellule sud-ouest à LUB, toutes dans STATE_POMERANIA par décision du joueur. Aucun pont latéral/diagonal avec le continent.
4. Passer en vue rapprochée : pas de trou, dalle, pont de relief ou ancien littoral émergé dans le détroit. Contrôler les connexions maritimes et l'accès militaire ; nodes.dat et les locators n'ont pas été déplacés.
5. Vérifier les accès au marché et à la mer des subdivisions nouvelles, notamment SWE en Mecklembourg et LUB sur Poel. Les bâtiments et infrastructures ont été conservés, pas artificiellement ajoutés pour présumer un résultat moteur.
6. Vérifier Rostock, Schwerin, MEC/MST, les ports et la Poméranie R9 : aucun changement d'attribution non demandé, de bâtiment, de PM, de propriétaire économique ou d'unité.
7. Contrôler la démographie prévue : Mecklembourg MEC−5066 et SWE+3874 ; Poméranie SWE+894 et LUB+298 ; MST et population mondiale inchangés. Ces allocations sont des fractions du stock existant, pas des habitants nouveaux.
8. Vérifier les cartes impériales principale et du journal : Poel, Wismar/Benz et Neukloster inclus ; détroit exclu. Registre504RGB. La Suède ne devient pas un membre national du bloc.
9. Vérifier les entrées du journal et actions impériales, les détenteurs légitimes des nouveaux RGB et l'absence de clés de localisation nouvelles.
10. Laisser passer un mois : absence de crash/erreur nouvelle, fonctionnement du hook et des compteurs impériaux.

## Enregistrement du retour

Distinguer le résultat manuel du joueur des151 contrôles statiques,44 tests de non-régression et16 contrôles hors moteur du filtre. R8/R9 ont déjà leur attestation séparée ; ne pas l'étendre rétroactivement à MAP2N.

Signaler les problèmes nouveaux précisément par secteur et capture. Conserver les44 doublonsRGB,12 références invalides et anomalies hors périmètre comme préexistants ; ne pas les déclarer réparés.

Ne pas effacer globalement les caches ni commencer un autre lot automatiquement.
