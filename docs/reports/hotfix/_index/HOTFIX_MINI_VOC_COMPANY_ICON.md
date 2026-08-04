# Mini-phase — icône propre à la VOC

Date : 4 août 2026

La compagnie `company_dutch_east_india_company` partageait par erreur l’icône `gb_eic.dds` avec la British East India Company.

Modification appliquée :

- création de `gfx/interface/icons/company_icons/historical_company_icons/nl_voc.dds` à partir du visuel VOC fourni par l’opérateur ;
- conversion en DDS RGBA non compressé, 256 × 256, avec transparence ;
- remplacement de la référence `gb_eic.dds` par `nl_voc.dds` dans `common/company_types/02_new_companies.txt` ;
- remplacement de la plantation de sucre principale par `building_coffee_plantation`, la plantation de sucre restant disponible comme extension ;
- activation par l’opérateur du bien de prestige potentiel `prestige_good_java_coffee` pour la VOC ;
- correction de la date de fondation de la compagnie, de la valeur anachronique `1670.5.2` vers la date historique `1602.3.20` ;
- aucune modification du pays `DEI`, de ses drapeaux ou de la BIC.

Contrôle : chemin résolu, dimensions et en-tête DDS conformes aux icônes de compagnie de Victoria 3. La clé `prestige_good_java_coffee` et son bien de base `coffee` sont présents dans les définitions vanilla 1.13 ; la composition finale de la compagnie contient bien `building_coffee_plantation`. La capture fournie par l’opérateur confirme l’affichage en jeu de l’icône propre à la VOC. La composition café/sucre et la nouvelle date de fondation n’ont pas fait l’objet d’un nouveau runtime dans cette mini-phase.

`MINI_VOC_COMPANY_IDENTITY_COMPLETE`
`VOC_COMPANY_ICON_RUNTIME_PASS`
`VOC_JAVA_COFFEE_STATIC_PASS`
