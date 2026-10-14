# Tabriz — retrait de l'industrie alimentaire initiale

À la demande du joueur, l'industrie alimentaire de Tabriz est retirée des historiques de départ. Les deux déclarations superposées, chacune de niveau 1, sont supprimées dans `08_middle_east.txt` et `98_build_start_1776_world_redistribution.txt`, avec leurs blocs de propriété et PM. Il ne s'agit pas d'affirmer que deux bâtiments distincts étaient réellement chargés par le moteur.

Les autres bâtiments, infrastructures, populations, frontières, propriétaires et unités restent inchangés. Tabriz conserve les cinq unités permanentes et six conscriptions du correctif précédent. Aucun commit, merge ou push ; aucune archive complète créée. Une baseline légère des fichiers concernés et des inventaires permet de vérifier ou restaurer ce retrait.

Validation : `VALIDATION.json` contrôle l'absence d'industrie alimentaire dans tous les historiques effectifs de Tabriz, l'identité des autres éléments des deux fichiers, la conservation des populations, unités et données cartographiques, ainsi que les empreintes des autres fichiers et l'état Git.

Le joueur a observé un déficit après la redistribution militaire : l'ancienne estimation d'une réserve positive n'est donc pas un résultat confirmé en jeu. Le retrait alimentaire réduit la demande d'infrastructure et d'emploi, mais aucun nouveau solde effectif n'est garanti sans test natif. Ce correctif concerne une nouvelle partie ; il ne supprime pas le bâtiment dans une sauvegarde existante. Vérifier Tabriz au démarrage puis après un mois (emploi des routes, pénuries, infrastructure et accès au marché).
