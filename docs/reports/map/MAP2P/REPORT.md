# MAP-2P — Audit ciblé de Frise orientale

Date : 16 octobre 2026. Date historique : 1er janvier 1776.

**Audit livré sans modification du mod. Aucun nouveau transfert A/B prêt à installer. La Frise orientale n'est pas déclarée historiquement achevée.**

La validation manuelle de MAP2O communiquée dans le prompt est consignée uniquement dans `MAP2O_RUNTIME_USER_VALIDATION.json`, ici. Durée et points inspectés non fournis ; aucun mois de simulation, journal moteur ou certificat de frontière n'est inventé. Les dossiers antérieurs restent intacts, y compris leurs statuts statiques historiques.

## Décisions

| Question | Réponse de l'audit |
|---|---|
| Les 319 cellules représentent-elles le noyau d'Emden ? | Représentation jouable à conserver en **B**, acceptée en jeu ; pas une correspondance géographique démontrée cellule par cellule avec toutes les juridictions. |
| Quelles portions prussiennes restent incorrectes ? | La souveraineté de Leer et du Rheiderland relève bien de la Frise prussienne, mais leur intersection exacte avec les RGB du jeu n'est pas établie. Leur exclusion de xF9DCA2 n'est pas démontrée non plus. |
| Des territoires étrangers ont-ils été absorbés par MAP2O ? | **Aucune cellule étrangère identifiée avec une preuve suffisante.** Cela ne prouve pas qu'il n'en existe aucune. Ne pas affirmer que Jever est entièrement hors du RGB sur la seule foi du propriétaire OLD voisin. |
| Que peut-on corriger immédiatement ? | Aucun nouveau transfert A/B. Maintenir xF9DCA2 sous PRU. Refuser les transferts globaux de x784B8E, de la province néerlandaise et des enveloppes OLD sans intersection historique identifiée. |
| Quels effectifs ? | 319 cellules PRU conservées ; 20 RGB inventoriés dans la fenêtre d'examen ; 1 240 cellules réparties dans six enveloppes/bandes C, **pas 1 240 erreurs**. Zéro cellule de transfert recommandée, zéro nouveau RGB. |
| Prochain secteur recommandé ? | **Eutin / principauté-évêché de Lübeck, distincte de la ville libre**, principalement STATE_SCHLESWIG_HOLSTEIN (66). Ne pas le lancer. |

## Ce que la nouvelle pièce apporte

La reproduction complète de Coldewey/Homann (1730) a été téléchargée et inspectée : `COLDEWEY_1730.png`, avec recadrage méridional. Elle distingue les ensembles de Leerort, Rheiderland, Overledingen, Harlingerland et les juridictions orientales. Elle est antérieure à 1744 : les archives prussiennes sont utilisées séparément pour la souveraineté de 1776. Une couleur de cette carte n'est donc pas assimilée automatiquement à un pays de 1776.

Elle confirme surtout qu'une restitution du sud ne doit pas devenir une simple ligne horizontale du bitmap ni une annexion de toute province voisine. Le passage de cette limite historique à la géométrie native reste non démontré : pas de levé local homologue de l'Ems/Leda/Dollard ni de contrôle indépendant suffisant dans les données conservées. Aucun nouveau modèle de projection n'a été ajusté ; le profil baltique n'est pas utilisé.

Un défaut du diagnostic précédent a été identifié : le heightmap mesure 16 384 × 7 232, contre 8 192 × 3 616 pour les provinces. L'ancien recadrage MAP2O utilisait le même rectangle sans facteur deux et n'était donc pas aligné. `ALIGNED_HEIGHTMAP_DIAGNOSTIC.png` et `PHYSICAL_LAYER_DIAGNOSTIC.json` corrigent cette seule lecture dans MAP2P. Le relief local ainsi observé ne livre toujours pas une limite juridictionnelle ou un centre urbain certifié. Aucun fichier ancien ni raster du jeu n'a été modifié pour corriger cet aperçu.

## Vérification du transfert antérieur

Les 319 cellules sont listées dans `MAP2O_319_CELL_AUDIT.csv`. Pour l'examen, elles sont divisées en trois bandes de lecture : 104 au nord, 153 au centre et 62 au sud. **Ces bandes ne sont ni des Ämter ni des frontières historiques.** Toutes restent dans STATE_HANNOVER, PRU, RGB xF9DCA2. Le hub portuaire fournit un contrôle technique, pas une preuve d'emplacement historique.

Le CSV `MAP2O/PRUSSIAN_TERRITORY_AUDIT.csv` indiquait HAN parce qu'il décrivait l'état initial de ce lot. Il n'est ni réécrit ni pris comme inventaire actuel. `CURRENT_TERRITORIES.csv` décrit le mod réellement installé.

## Propositions, et limite réelle de livraison

`PROPOSED_CHANGES.csv` contient uniquement l'en-tête : **aucun correctif supplémentaire ne satisfait simultanément la preuve de souveraineté et une délimitation native suffisamment défendable**. Ce n'est pas une liste de zéros présentée comme des transferts réalisés.

`CANDIDATE_CELLS_NOT_AUTHORIZED.csv` contient les coordonnées vérifiées des enveloppes à examiner, avec propriétaire proposé vide, catégorie C et `DO_NOT_APPLY`. La carte distingue les propriétaires actuels, le maintien B et ces enveloppes C ; elle ne dessine pas une frontière inventée. Le nombre de cellules effectivement erronées reste indéterminé, avec des bornes explicites, non une estimation statistique.

Les effectifs d'enveloppes portent sur les RGB complets ; certaines portions de contrôle dépassent le recadrage de la carte. L'inventaire distingue le nombre total du RGB de son nombre de cellules visibles dans la fenêtre.

Une source locale homologable est nécessaire avant de livrer un transfert du sud directement applicable. Répéter les mêmes ajustements ou demander au joueur de choisir arbitrairement un décalage ne résoudrait pas ce manque. Les recherches s'arrêtent ici conformément au prompt.

## Protection

Seul ce nouveau dossier reçoit des fichiers. `VALIDATION.json` contrôle les empreintes de tous les fichiers fonctionnels, le registre actif, HEAD/index et la conservation des anciens rapports ; il ne rejoue pas un moteur de jeu. Les populations, bâtiments, PM, propriétés économiques, unités, littoral, Poel, Wismar, Neukloster, Poméranie et prototype de pont ne sont pas modifiés. Les 44 doublons et 12 références invalides restent les anomalies héritées.

Dernière exécution : **44/44 contrôles d'audit réussis**, sans mutation fonctionnelle. Ce résultat valide la protection du workspace et la cohérence des livrables, pas une frontière historique ou une nouvelle partie moteur.

ColGrep n'est pas invoqué : les chemins requis étaient fournis et les anciennes localisations étaient connues ; la règle 3 des instructions locales évite une recherche redondante. Aucune intégration ou reconstruction d'index. Aucun commit, merge, reset, changement de branche ou push.
