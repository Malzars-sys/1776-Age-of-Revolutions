# R1_WESTERN_EUROPE-0008 — Terraferma veneta: Bergamo, Brescia, Crema

Statut : MAPPING_REQUIRED. Pas de province historiquement vérifiée ni de transfert autorisé.

[Vue technique de l’État](../MAP1_GEOGRAPHIC_EVIDENCE/STATE_ATLAS/STATE_LOMBARDY.svg)

## Conclusion régionale (non visa central)

Les trois districts restent vénitiens en 1776; Crema forme enclave séparée.

Souveraineté de jure : République de Venise

Contrôle : Rettori vénitiens, podestà, conseils de vallée et organes fiscaux

Statut : LOCAL_AUTONOMY

## Localisation et incertitude

Bergame (45.70N,9.67E), Brescia (45.54N,10.22E), Crema (45.36N,9.69E); frontière Adda (ouest), Oglio, lac Iseo.

Impossible de valider RGB x867A90, x9AC196 sans overlay; relief du mod ne prouve pas identité.

Correspondance au bitmap et couverture de Crema non résolues.

## Résultat MAP-1

x867A90 (428 pixels) est VEN dans main; x9AC196 (79 pixels) aussi. x9AC196 est au nord-est immédiat du groupe lombard, pas une preuve automatique de Mantoue. Les hubs du jeu sont des repères déclarés; les noms Bergamo/Brescia ne valident pas à eux seuls les juridictions. REJECT_DUPLICATE_AUS_VEN; NO_OWNER_ARBITRATION

RGB cités (non vérifiés historiquement) : x867A90|x9AC196

Domaine actuel de recherche : x867A90|x9AC196

Hubs/locators à confronter : [{"State_ID": "STATE_LOMBARDY", "Hub_Type": "city", "Hub_Name": "Milan", "Defined_Hub_RGB": "xD04060", "Locator_Sampled_RGB": "xD04060", "Locator_X": "4307.216", "Locator_Y": "993.134", "Definition_Matches_Locator": "YES", "Locator_In_State": "YES", "Source": "C:\\Games\\Victoria 3\\game\\gfx\\map\\map_object_data\\generated_map_object_locators_city.txt", "Coordinate_Method": "ENGINE_X; PNG_Y=HEIGHT-ENGINE_Z; CHECKED_RGB", "Historical_Proof": "NONE: vanilla named anchor, not 1776 jurisdiction"}, {"State_ID": "STATE_LOMBARDY", "Hub_Type": "farm", "Hub_Name": "Brescia", "Defined_Hub_RGB": "x867A90", "Locator_Sampled_RGB": "x867A90", "Locator_X": "4318.261", "Locator_Y": "990.581", "Definition_Matches_Locator": "YES", "Locator_In_State": "YES", "Source": "C:\\Games\\Victoria 3\\game\\gfx\\map\\map_object_data\\generated_map_object_locators_farm.txt", "Coordinate_Method": "ENGINE_X; PNG_Y=HEIGHT-ENGINE_Z; CHECKED_RGB", "Historical_Proof": "NONE: vanilla named anchor, not 1776 jurisdiction"}, {"State_ID": "STATE_LOMBARDY", "Hub_Type": "mine", "Hub_Name": "Como", "Defined_Hub_RGB": "x3F1E38", "Locator_Sampled_RGB": "x3F1E38", "Locator_X": "4305.136", "Locator_Y": "987.61", "Definition_Matches_Locator": "YES", "Locator_In_State": "YES", "Source": "C:\\Games\\Victoria 3\\game\\gfx\\map\\map_object_data\\generated_map_object_locators_mine.txt", "Coordinate_Method": "ENGINE_X; PNG_Y=HEIGHT-ENGINE_Z; CHECKED_RGB", "Historical_Proof": "NONE: vanilla named anchor, not 1776 jurisdiction"}, {"State_ID": "STATE_LOMBARDY", "Hub_Type": "wood", "Hub_Name": "Bergamo", "Defined_Hub_RGB": "x4713EE", "Locator_Sampled_RGB": "x4713EE", "Locator_X": "4332.79", "Locator_Y": "987.005", "Definition_Matches_Locator": "YES", "Locator_In_State": "YES", "Source": "C:\\Games\\Victoria 3\\game\\gfx\\map\\map_object_data\\generated_map_object_locators_wood.txt", "Coordinate_Method": "ENGINE_X; PNG_Y=HEIGHT-ENGINE_Z; CHECKED_RGB", "Historical_Proof": "NONE: vanilla named anchor, not 1776 jurisdiction"}]

## Question ciblée

Fournir une carte pré-1776 de Bergame/Brescia/Crema et Mantoue avec Adda, Oglio, lac Iseo et villes repérables. Quelle portion exacte de x867A90 et x9AC196 relève de chaque autorité ? Ne pas imposer un contour au seul nom du hub.

## Sources

- R1_WESTERN_EUROPE-S008 — Lombardia Beni Culturali; Regione Lombardia; Il dominio della terraferma veneta: Bergamo, Brescia, Crema (sec. XV-1797); publication UNKNOWN; document 1427-1797; Sections Bergamo: juridictions; Brescia: territoire; Crema: enclave et institutions fiscales.
  Référence : https://www.lombardiabeniculturali.it/istituzioni/storia/?unita=03.03
  Limites : Divisions historiques très fines; ne donne aucun RGB du jeu.. Accès : FETCH_FAILED. Compte rendu centralisé dans MAP1_SOURCE_REVIEW.csv.

## Coordination

COORDINATION_REQUIRED ; région secondaire : R2_NORTHERN_CENTRAL_EASTERN_EUROPE

Fiches des autres régions dans le même State_ID : aucune : rechercher aussi les États voisins

## Méthodes A/B/C et dépendances

A : tester les polygones actuels après identification historique. B : recomposer/scinder les State Regions si A nécessite des scopes distincts; ne crée pas de polygone plus petit. C : aucune nécessité démontrée, aucune édition autorisée.

Conserver exactement populations par culture/religion, bâtiments/niveaux/PM/propriété économique, formations/recrutement. Auditer capitales, hubs, ports/naval exits, sujets/pactes/traités, journaux/décisions et localisations avant toute proposition intégrable.

[Incertitudes régionales originales](../inputs/regional_originals/R1_WESTERN_EUROPE_UNCERTAINTIES.md)
