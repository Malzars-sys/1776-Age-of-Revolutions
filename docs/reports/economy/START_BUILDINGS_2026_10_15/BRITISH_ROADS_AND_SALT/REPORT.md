# Réseaux britanniques, bureaucratie irlandaise et salines

**PASS_STATIC_ENGINE_PENDING — 131/131 contrôles.** Pas de mesure moteur du budget ou du recrutement.

## Périmètre et règle de dimensionnement

Treize États métropolitains, Irlande comprise selon la réponse du joueur. Les neuf États britanniques appartiennent à GBR ; les quatre irlandais à IREK, pays distinct du mod. Aucun changement de propriétaire ou de dépendance. Les colonies et possessions extérieures ne sont pas touchées.

La demande d'infrastructure est calculée sur les niveaux de tous les bâtiments écrits, à leur fonctionnement complet, avec les usages des groupes hérités et leurs éventuelles valeurs spécifiques. Les quinze nouveaux bureaux irlandais sont inclus. La capacité utilise les ports et traits existants, la base de 3, les modificateurs applicables de lois/technologies, le PM des routes à péage et son apport de population plafonné. Le diviseur de population **100 000** provient des définitions du jeu installé. Les malus régionaux, notamment ceux des Highlands, ne sont pas perdus par une addition de compteurs supprimant les valeurs négatives.

Le niveau conservé est le plus petit entier couvrant cette demande avec une réserve de **10 %, au minimum 3 points**, sans augmenter un réseau déjà présent. Exception explicite : les Highlands gardent leur unique niveau, suffisant pour le besoin nominal actuel mais avec seulement **+1,065** de marge, sous la réserve cible ; aucun niveau supplémentaire n'y est créé uniquement pour arrondir cette réserve.

**Dernière instruction du joueur appliquée :** routes à péage (`pm_turnpike_road_network`) partout ; canaux industriels (`pm_industrial_canals`) **actifs et comptés uniquement dans Lancashire, Midlands et Yorkshire**. Ils étaient déjà actifs et n'ont jamais été désactivés pendant cette passe. Les autres États restent sans canaux. Aucune capacité de canal hypothétique n'est supposée. Les réseaux ferrés et passagers restent désactivés. Les deux pays possèdent déjà la technologie des routes à péage ; GBR possède celle des canaux industriels.

## Avant / après

| État | Pays | Niveaux avant | Après | Canaux |
|---|---|---:|---:|---|
| Home Counties | GBR | 54 | 19 | Non |
| East Anglia | GBR | 12 | 6 | Non |
| West Country | GBR | 28 | 10 | Non |
| Pays de Galles | GBR | 10 | 4 | Non |
| Midlands | GBR | 23 | 13 | Oui |
| Yorkshire | GBR | 28 | 12 | Oui |
| Lancashire | GBR | 38 | 10 | Oui |
| Lowlands | GBR | 14 | 4 | Non |
| Highlands | GBR | 1 | 1 | Non |
| Leinster | IREK | 8 | 3 | Non |
| Ulster | IREK | 6 | 2 | Non |
| Munster | IREK | 6 | 2 | Non |
| Connaught | IREK | 1 | 1 | Non |
| **Total** | | **229** | **87** | |

Réduction de **142 niveaux**, soit environ **62 %**. GBR : 208 → 79 ; IREK : 21 → 8. Détail des demandes, capacités avant à leurs véritables PM, capacités après et marges dans `STATE_REBALANCE.csv`. Les participations existantes sont réduites au prorata par allocation entière au plus fort reste, sans réattribuer leurs adresses ou pays détenteurs à un nouvel acteur. Tous les bâtiments non concernés restent sémantiquement identiques.

À plein régime nominal, les réseaux passent de **300 200 à 115 000 postes** (canaux compris), avec entrées de bois **805 → 523**, outils **358 → 244**, fer **178 → 70**. Ces chiffres décrivent des quantités physiques de PM, pas un prix ni une économie monétaire mesurée. Les nouveaux bureaux irlandais demandent séparément **22 500 postes** ; aucune population n'est ajoutée pour les remplir. Le solde budgétaire réel dépendra des salaires, prix, intrants et délais de recrutement.

## Bureaucratie irlandaise

Le PM de base actuel `pm_simple_organization` produit **10** de bureaucratie par niveau à plein effectif. Pour couvrir le déficit rapporté de **128**, plus une réserve d'environ 20, ajout de **15 niveaux**, soit **+150 nominaux** : Leinster +10, Ulster +3, Munster +2. Écart théorique après couverture du déficit : **+22**, hors autres effets évolutifs. Les bureaux sont détenus par IREK.

Pas de technologie accordée pour imposer des armoires plus avancées. Les nouveaux bureaux utilisent les bureaucrates professionnels, compatibles avec la loi irlandaise des fonctionnaires nommés, et le personnel religieux autorisé. Les anciennes déclarations administratives sont conservées. Le réseau du Leinster garde trois niveaux, et non deux comme dans le premier diagnostic routier sans ces nouveaux bureaux.

**Ce n'est pas une garantie de +22 au premier jour.** L'ajout de capacité doit recruter pour fournir son rendement ; contrôler l'Irlande après stabilisation, plutôt que de transformer une valeur sous-recrutée en promesse de solde exact.

## Sel

Modification mondiale de `default_building_salt_pan` : sortie de sel **10 → 20** par niveau pleinement employé. Rien d'autre n'est modifié dans ce PM. Le PM à pioches des mines de sel produisait déjà **20** ; il n'est pas doublé. Aucun niveau de saline n'est ajouté dans cette étape.

## Vérifications et limites

`tools/british_infrastructure_2026_10_15.py validate` : **131/131** contrôles, couvrant les différences sémantiques exactes des bâtiments et détenteurs, les PM, l'infrastructure calculée, le périmètre des canaux, les ajouts précédents, les autres fichiers, la population, les anomalies héritées, HEAD et index. Les données du premier ajout industriel/agricole restent intactes, dont les dix verreries chinoises avec porcelaine. Les frontières et le correctif d'interface ne changent pas.

Hypothèses : effectif complet, approvisionnement normal, population de départ. Les bâtiments implicites, pénuries, évolutions de l'emploi et effets dynamiques ne sont pas simulés. Les échelles d'économie et modificateurs de prix ne sont pas utilisés pour prétendre connaître un budget exact. Les colonies, ports, usines, unités et formations politiques ne sont pas remaniés. Les **44 doublons RGB et 12 références invalides préexistants** restent ouverts, sans nouvelle régression détectée dans les invariants examinés.

Test demandé au joueur : nouvelle partie, contrôler les niveaux et PM, puis laisser recruter les réseaux et bureaux. Comparer l'infrastructure réellement disponible, l'accès au marché, la bureaucratie irlandaise et les dépenses ; surveiller particulièrement les Highlands et le Rhône. Aucun `PASS_RUNTIME_USER_VALIDATED` accordé à cette passe. Aucun commit ni push.
