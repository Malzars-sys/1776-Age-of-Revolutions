# R9-02 — Rio Grande et Santa Tecla au 1er janvier 1776

Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION**. Installation partielle de R9 ; aucun chargement moteur ni résultat économique attesté.

## Correction installée

Cinq provinces existantes du State_ID `STATE_RIO_GRANDE_DO_SUL` passent de BRZ à SC4, gouvernement colonial espagnol existant :

| RGB | Fonction de la correction |
| --- | --- |
| x52B247 | Noyau portuaire de Rio Grande, rive méridionale |
| xD3A197 | Approche terrestre occidentale du port et continuité avec la Banda Oriental |
| xCC2135 | Segment côtier méridional intermédiaire |
| xCD9ECD | Segment côtier vers Chuí, raccord à la Banda Oriental existante |
| xD9D235 | Représentation à l'échelle des cellules du fort de Santa Tecla |

Ce sont des cellules du bitmap actuel, pas des identifiants cadastraux historiques. Aucune côte, couleur, State_ID, ressource ou position de hub n'est redessinée. Le transfert corrige les noyaux occupés avant les reprises portugaises de mars–avril 1776 ; il ne certifie pas la frontière entière. Porto Alegre et la longue rive littorale au nord (`xE17D15`) restent portugaises, tout comme Sainte-Catherine. Aucun résultat de conquête de 1777 n'est placé au départ.

Les cinq cellules ont une continuité terrestre vérifiée vers Montevideo, par côtés de pixels/provinces et hors adjacences explicitement bloquées ou provinces impassables. Aucun poste continental isolé ni pont maritime n'est ajouté.

## Population et bâtiments

Les 92 288 habitants existants du State_ID sont conservés. **686 habitants libres sulista** sont transférés de la portion BRZ à la portion SC4 ; 91 602 restent BRZ. Aucun habitant n'est créé, supprimé ou converti ; les cohortes guarani et afro-brésiliennes restent intactes.

L'effectif 686 est une **allocation technique bornée**, appuyée sur une observation d'avril 1776 rapportée par Cunha, pas un recensement du 1er janvier ni l'effectif complet de toute la bande transférée. La garnison espagnole, les populations rurales et les identités fines restent à réviser sur des sources adaptées. Aucun ratio de pixels n'est utilisé comme démographie historique.

Les deux commandes de port déjà présentes, chacune avec un niveau de propriété, suivent le contrôle du port vers SC4, avec leurs PM, réserves et effectifs installés inchangés. Une commande provient du fichier régional et l'autre du fichier de redistribution mondiale : cette structure héritée reste conservée, sans prétendre déduire de sa seule lecture l'agrégation exacte du moteur. Les élevages, le réseau routier, leurs propriétaires et tous les autres bâtiments restent identiques.

## Vérifications

- **15/15 contrôles statiques** : syntaxe ; exactement cinq transferts ; aucune nouvelle province vide/doublement attribuée ; cohortes et totaux conservés ; seuls les ports changent d'administration ; continuité terrestre ; témoins CENTRAL-02 et R9-01 ; empreintes hors lot.
- Technologies et PM : SC4 conserve **12 constats préexistants**, BRZ **18**, sans constat ajouté ni retiré dans cet audit. Ces profils ne sont donc pas déclarés exempts d'erreurs.
- Aucun changement concurrent de fichier runtime hors des quatre fichiers du manifeste n'est constaté pendant la préparation/application/vérification du lot. Les baselines précédentes ne sont pas restaurées.
- Les erreurs d'attribution globales déjà présentes hors lot sont tolérées seulement si strictement inchangées ; ce test ne blanchit pas la carte mondiale.

Commandes exécutées : `tools/r902.py --prepare`, `--apply`, `--verify`, `--preview` ; `tools/validate_starting_technology_1776.py --tag SC4 --tag BRZ --output …/TECH_BEFORE.json` puis `TECH_AFTER.json`. Les audits technologiques retournent un code d'échec attendu à cause des dettes existantes. Le rendu documentaire du PDF a signalé deux polices de remplacement ; le passage démographique a aussi été inspecté visuellement.

Voir [VALIDATION.json](VALIDATION.json), [TECH_DELTA.json](TECH_DELTA.json), [PATCH.json](PATCH.json), [carte](R9_02_RIO_GRANDE.png), [sources](SOURCES.md) et [protocole en jeu](RUNTIME_PROTOCOL.md).

## Réserves ouvertes

Colônia do Sacramento est encore portugaise, mais **n'est pas corrigée dans ce lot** : le calage approximatif tombe sur la côte/eau près de plusieurs cellules. Il faut isoler le noyau réellement défendu sans transférer une grande province espagnole, puis traiter son accès au marché. Aucun corridor portugais imaginaire n'est fabriqué à travers l'Uruguay espagnol. L'exception maritime autorisée pour les îles aléoutiennes n'est pas étendue tacitement à cette enclave.

Les missions, les territoires autochtones de la Campanha, les limites intérieures, la démographie détaillée, les Guyanes, la Guajira, l'Araucanie et la Patagonie restent ouverts. L'appartenance initiale de SC4 est une représentation de gouvernement subordonné à l'Espagne, pas une certification de vice-royauté avant la cédule d'août.

CENTRAL-01 et CENTRAL-02 gardent leur statut technique et leurs protocoles ; l'acceptation explicite du joueur est conservée dans leurs reçus datés. Talamanca, Belize/Petén et les dossiers insulaires restent historiquement non résolus. Aucun commit, push ou fichier vanilla modifié.
