# BALKANS-06 — Grèce continentale et Péloponnèse

26 octobre 2026. Départ : 1er janvier 1776. Statut IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION ; moteur NOT_RUN ; aucune nouvelle validation joueur. **Crète exclue de l’autorisation actuelle** ; P1-06 reste incomplet.

## Corrections installées

- **Hacı Ali Haseki**, voïvode d’Athènes dans sa première période 1775–1776, entre dans le vivier civil ottoman. Culture turque, sunnite, groupe des propriétaires, idéologie traditionaliste. Le trait « Voïvode d’Athènes » est descriptif et sans bonus. Pas de général, souverain ou chef national de groupe ajouté ; les titulaires existants restent identiques. Âge technique 45, non une naissance établie. La source situe sa naissance à Burdur : aucun home_region athénien n’est inféré de sa fonction, et sa région natale de jeu n’est pas forcée sans correspondance géographique vérifiée.
- **Un niveau de fortification côtière TUR en ATTICA**, représentant la capacité régionale des places de Lépante–Antirrio.
- **Un niveau en PELOPONNESE**, représentant Nauplie/Palamidi. Les installations attestées existent avant 1776 ; les murailles athéniennes de 1778 et les ouvrages tardifs d’Ali Pacha ne sont pas ajoutés.

Cinq fichiers propres nouveaux, **aucun fichier fonctionnel partagé retouché**. Aucun pays, traité, loi, recette commune, technologie ou PM-type créé. Les bandes armées d’après-Orlov ne sont pas assimilées à des formations régulières nouvelles. Les forces ottomanes, leurs réserves et les maisons B05 restent intégralement identiques.

## Cellules et populations

**Zéro RGB/pixel/propriétaire modifié, zéro nouveau TAG, zéro transfert de POPs.** Les cinq RGB TUR du Péloponnèse (`x0055D7`, `x43409D`, `x61E57E`, `xBA3449`, `xC0D060`) et tous les RGB d’ATTICA/THESSALIA restent identiques. Cérigo `xE8D215`, Vonitsa `xE8D214`, Parga/Prévéza `xE8D212/xE8D213`, Butrinto `xE8D211`, les Ioniennes, MON et RAG sont conservés. Hubs, locators, terrains, ressources et arable ne sont pas écrits.

| Portion technique | Avant | Après |
| --- | ---: | ---: |
| ATTICA TUR / VEN | 541 293 / 1 000 | 541 293 / 1 000 |
| PELOPONNESE TUR / VEN | 181 316 / 7 500 | 181 316 / 7 500 |
| THESSALIA TUR / VEN | 958 024 / 4 700 | 958 024 / 4 700 |
| Monde | 837 336 539 | 837 336 539 |

Le total mondial d’entrée diffère de l’ancien reçu B05 (834 936 539) de **+2 400 000** : ajout externe du chantier HBC-06 en Amérique du Nord, documenté avant cette passe. Son reçu et les neuf empreintes fonctionnelles ont été vérifiés et archivés ici ; aucune approbation historique ou validation humaine n’en est déduite. Les changements d’attribution extérieurs sont observés séparément dans EXTERNAL_HBC06_OBSERVATION.json. Aucune compensation démographique hors lot.

Les totaux locaux sont ceux du scénario actuel, non des recensements certifiés de 1776. Les musulmans, autres minorités, réfugiés et pertes d’après-Orlov ne sont pas réestimés arbitrairement. L’autonomie des clans du Magne n’est pas niée par le maintien provisoire du cadre TUR : ses limites, obligations et institutions doivent encore être distinguées. Le règlement de Koutifaris cité par la thèse date de janvier 1777 et n’est pas appliqué au lancement.

## Capacités, technologies et limites du moteur

PM de base existant pour les deux niveaux : **1 800 emplois de soldats et 200 d’officiers**, 10 armes légères et 10 fer par semaine à plein emploi au total. Il s’agit de capacités et de besoins théoriques, pas d’une embauche ou d’un budget constaté. Les réserves sont initialisées avec la valeur conventionnelle 1. Aucun bataillon ou habitant créé. Les effets navals et de contrôle de détroit du PM restent inchangés ; ils portent sur l’État du moteur, pas sur un périmètre cadastral de chaque fort. Aucun bonus terrestre supplémentaire inventé.

Les **23 technologies TUR** restent identiques. Le bâtiment requiert scientific_fortification_siegecraft, déjà acquis ; le PM de base n’a pas de prérequis supplémentaire. Groupes, PM, intrants et emplois sont résolus. L’audit impérial reste FAIL_STATIC avant/après avec les trois mêmes observations héritées : gate horse_artillery des hussards, ressource régionale cuivre à Diyarbakır, profil historique impérial non certifié. Les deux nouveaux forts n’ajoutent aucune anomalie technologique. Ni graphe TECH ni recettes ECON modifiés.

Les gouverneurs de Morée/Thessalie, les notables et autorités religieuses, le Magne, l’insécurité et l’économie d’après-Orlov restent partiellement étudiés. Le civil Haseki ne commande pas fonctionnellement la province ; son futur et l’évolution de sa carrière suivent les mécaniques du jeu. Rendu des traits, vivier, placement des forts, embauche, salaires et effets navals attendent le test groupé. Aucun statut de région complète.

## Sources, contrôles et concurrence

Sources et passages vérifiés : SOURCES.md. Küpeli 2020 pour Athènes, Karabıçak 2020 pour les négociations et la chronologie du Magne, ministère grec de la Culture pour les places. Original BOA non consulté directement ; téléchargements manqués distingués des archives effectives. Aucune précision de frontière ou de naissance inventée.

**55/55 contrôles statiques réussis** : sorties propres, parse/références, personnage civil sans leadership national, localisations FR/EN BOM sans collision, compatibilité des forts, recette conservée, POPs et propriétaires mondiaux/régionaux, armées entières, empreintes antérieures et Git. L’audit technologique FAIL_STATIC reste distinct de la non-régression du lot. Aucun moteur lancé.

Les **2538 fichiers fonctionnels antérieurs**, **335 preuves WORLD** et **975 preuves SERG** de la capture d’application sont identiques. Les travaux TECH-R1/R2/R3, ECON-ALLOYS/quincaillerie, génie/fortifications, HBC-06 et SERG sont préservés. Aucune écriture Git, vanilla ou suivi SERG, aucun retour à une baseline ancienne.

**Progression inchangée : 10/80 Balkans (12,50 %), 10/320 WORLD (3,13 % arrondis), zéro nouvelle validation joueur.** Aucun critère entier de P1-06 n’est crédité pour ce noyau partiel qui exclut la Crète. Les huit critères gardent leur périmètre canonique ; aucun dénominateur retiré. Prochaine candidate : **BALKANS-07 — Crète, complément de P1-06** ; les obligations continentales restent ouvertes. Aucun test intermédiaire ; aucune autre région WORLD avant confirmation explicite du test balkanique groupé.
