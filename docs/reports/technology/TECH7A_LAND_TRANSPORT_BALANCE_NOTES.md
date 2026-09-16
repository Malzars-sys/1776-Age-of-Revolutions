# TECH7A — Notes d'équilibrage du réseau de transport terrestre

## Coût commun du bâtiment

Le bâtiment unifié `building_land_transport_network` coûte 800 points de construction par niveau.

## Règle d'addition des infrastructures

À terme, le bâtiment unifié contient trois groupes de méthodes de production actifs simultanément :

- routes ;
- canaux ;
- voies ferrées.

Les infrastructures fixes fournies par ces trois groupes s'additionnent. Les futurs PM ferroviaires ne doivent donc pas reprendre directement les valeurs d'infrastructure de l'ancien bâtiment `building_railway`.

À niveau de bâtiment égal et avec les meilleurs PM de fin de partie, la cible d'équilibrage est :

```text
infrastructure fixe des routes
+ infrastructure fixe des canaux
+ infrastructure fixe du rail
≈ infrastructure fixe de l'ancien building_railway avec son meilleur PM
```

Les bonus routiers variables dépendant de la population et de la consommation d'automobiles ne font pas partie de cette égalité de base. Ils restent des bonus situationnels.

Le rail doit être principalement différencié par sa production du bien local `transportation`, et non par une énorme quantité supplémentaire d'infrastructure fixe.

## Procédure obligatoire pour la future Wave Rail

1. Auditer la valeur terminale exacte d'infrastructure de l'ancien `building_railway`.
2. Calculer l'infrastructure fixe terminale déjà fournie par les routes et les canaux du bâtiment unifié.
3. Soustraire cette somme de la valeur terminale de l'ancien chemin de fer.
4. Utiliser le résidu comme cible approximative du PM ferroviaire terminal.
5. Conserver une progression croissante entre tous les PM ferroviaires.

Cette règle concerne uniquement l'infrastructure fixe. La production de `transportation` et les bonus routiers variables sont équilibrés séparément.

## Wave B — Canaux

Le groupe `pmg_land_transport_canals` est indépendant du groupe routier et reste actif simultanément avec lui. Les canaux ne produisent pas le bien local `transportation` : leur identité repose sur une petite quantité d'infrastructure fixe et sur un léger relèvement local du plafond des économies d'échelle.

| Méthode | Technologie | Entrants par niveau | Emplois par niveau | Infrastructure fixe | Plafond des économies d'échelle |
|---|---|---|---:|---:|---:|
| Pas de réseau de canaux | aucune | aucun | 0 | 0 | 0 |
| Canaux industriels | `industrial_canals` | 5 bois, 2 outils, 2 fer | 800 | +1 | +0,05 niveau |
| Canaux aménagés | `professional_civil_engineering` | 5 calcaire, 3 outils, 3 fer | 800 | +3 | +0,10 niveau |

Tous les entrants et effets opérationnels sont multipliés par le taux d'emploi. Les emplois restent définis par niveau afin de fixer la capacité nominale du bâtiment.

Le bonus MAPI envisagé a été écarté : `state_market_access_price_impact` complète une valeur de base bornée et devient dangereux lorsqu'il est cumulé librement par niveau. Le bonus retenu est le modificateur natif `building_economy_of_scale_level_cap_add`, appliqué localement à l'État et multiplié par l'emploi du réseau. Il repousse légèrement le niveau de bâtiment jusqu'auquel les industries admissibles reçoivent leurs économies d'échelle : +0,05 niveau par niveau de canaux industriels et +0,10 niveau par niveau de canaux aménagés à plein emploi.

Les restrictions géographiques ont été différées. `is_coastal` exclurait les canaux fluviaux intérieurs, tandis que les traits de rivière sont des identifiants régionaux particuliers sans test générique exhaustif. Une restriction fondée sur une liste manuelle serait donc fragile et difficile à maintenir.

## Audit de l'ancien chemin de fer et budget de la future Wave Rail

L'ancien `building_railway` coûte lui aussi 800 points de construction et possède deux groupes simultanés : traction ferroviaire et voitures de voyageurs.

| Configuration auditée | Infrastructure | Transportation | Entrants par niveau | Emplois par niveau |
|---|---:|---:|---|---:|
| Premier PM, trains primitifs | +20 | 20 | 5 moteurs, 2 charbon | 1 000 |
| Terminale normale, trains diesel + voitures en acier | +40 | 55 | 5 moteurs, 4 carburants raffinés, 5 acier | 1 200 |
| Maximum absolu avec principe Transport III + voitures en acier | +55 | 65 | 6 moteurs, 4 carburants raffinés, 5 acier | 1 200 |

À la fin de la Wave B, les meilleurs PM routier et canal fournissaient une base fixe de :

```text
routes goudronnées +10
+ canaux aménagés +3
= +13 infrastructure par niveau
```

Ce calcul constituait la cible provisoire avant le renforcement des routes de la Wave C :

- cible normale hors bonus de principe : `40 - 13 = 27` infrastructures fixes ;
- plafond absolu avec le principe Transport III : `55 - 13 = 42` infrastructures fixes.

La Wave C remplace cette cible provisoire par le budget final ci-dessous.

## Wave C — Architecture unifiée et rail

L'identifiant canonique du bâtiment unifié est désormais `building_railway`. L'ancien identifiant temporaire `building_land_transport_network` est conservé comme alias. Cette architecture maintient les références historiques, les journaux, les événements, les scripts et les modificateurs visant déjà `building_railway`, sans conserver un second bâtiment ferroviaire autonome.

Limite sémantique à contrôler : un ancien script qui teste seulement `has_building = building_railway` reconnaît désormais le bâtiment régional même lorsque son PM actif est `pm_no_rail_network`. L'identifiant reste valide et aucun bâtiment fantôme n'est créé, mais ces scripts ne peuvent pas distinguer automatiquement « infrastructure régionale présente » de « voie ferrée active ». Les fichiers 1.13.11 n'offrent pas d'alias conditionnel capable de résoudre cette différence ; les journaux concernés devront être vérifiés pendant le test runtime avant d'envisager des corrections ciblées.

Le bâtiment utilise toujours `bg_land_transport_network`, enfant de `bg_public_infrastructure`. Il reste donc financé par l'État, ne consomme aucune infrastructure et n'utilise pas l'ancien modèle de propriété privée du chemin de fer. Le groupe a pour bâtiment par défaut `building_railway`.

Ses groupes de méthodes de production sont simultanément :

1. réseau routier ;
2. réseau de canaux ;
3. réseau ferroviaire ;
4. trains de voyageurs.

Le bâtiment n'est plus verrouillé par `railways`. `pm_no_rail_network` est sa méthode ferroviaire par défaut et ne produit aucun effet. Tous les PM ferroviaires opérationnels exigent explicitement `railways` en plus de leur technologie avancée éventuelle.

Les fichiers 1.13.11 ne fournissent aucun mécanisme employé par les PM permettant d'imposer proprement une dépendance directe entre deux PMG. Les voitures de voyageurs sont donc verrouillées par `railways`, mais peuvent théoriquement rester sélectionnées si le joueur revient ensuite manuellement à `pm_no_rail_network`. Ce cas doit être contrôlé au runtime ; aucune pseudo-condition non reconnue n'a été inventée.

### FINAL STANDARD INFRASTRUCTURE BUDGET PER LEVEL

```text
Tarmac Roads       = 20
Engineered Canals  =  3
Diesel Rail        = 17
--------------------------------
TOTAL              = 40
```

Cette valeur remplace approximativement l'infrastructure terminale normale de l'ancien bâtiment ferroviaire autonome.

Bonus variables non inclus :

- infrastructure routière liée à la population ;
- infrastructure routière liée aux automobiles ;
- relèvement du plafond des économies d'échelle par les canaux ;
- variantes du principe Transport III ;
- autres principes et modificateurs externes.

Spécialisation principale du rail : production du bien local `transportation`.

### Progression ferroviaire standard

| PM | Infrastructure | Transportation |
|---|---:|---:|
| Pas de réseau ferroviaire | 0 | 0 |
| Trains expérimentaux | 5 | 20 |
| Trains à vapeur | 9 | 25 |
| Trains électriques | 14 | 35 |
| Trains diesel | 17 | 40 |

Le principe Transport III continue de remplacer les variantes standards, sans cumul entre les deux PM :

- vapeur : +14 infrastructure et 30 Transportation ;
- électrique : +24 infrastructure et 45 Transportation ;
- diesel : +32 infrastructure et 50 Transportation.

La variante diesel du principe conserve donc son différentiel historique de +15 infrastructure par rapport au diesel standard. Avec routes et canaux, le maximum devient `20 + 3 + 32 = 55`, identique au plafond absolu de l'ancien bâtiment. Les voitures de voyageurs ajoutent séparément 0, 10 ou 15 Transportation et aucune infrastructure.

## Audit des anciens bonus de throughput ferroviaire

Après l'unification, `building_railway_throughput_add` ne désigne plus un chemin de fer autonome : il multiplie tous les entrants et toutes les sorties du bâtiment régional, y compris les modificateurs d'infrastructure des routes et des canaux ainsi que le plafond d'économies d'échelle des canaux. L'audit a retrouvé exactement 17 occurrences actives.

La conversion retenue utilise `goods_output_transportation_mult`. Ce type suit la famille native `goods_output_<good>_mult`, déjà définie et utilisée par vanilla pour de nombreux biens (`tools`, `engines`, `electricity`, etc.) et par le mod pour ses biens personnalisés. La définition TECH7A ajoute uniquement la métadonnée manquante pour le bien vanilla `transportation`. L'effet ne modifie ni les entrants, ni l'infrastructure, ni le plafond d'économies d'échelle.

Limite technique : le moteur 1.13.11 ne fournit aucune clé attestée combinant à la fois un type de bâtiment et un bien, telle qu'un hypothétique `building_railway_goods_output_transportation_mult`. La clé retenue cible donc toute production de `transportation`, y compris la petite production des centres urbains, et non exclusivement le PMG ferroviaire. Aucun nom composé non attesté ni contournement scripté n'a été inventé.

### Classification et décision

| Source | Valeur | Classe | Base historique ou gameplay | Ancien effet réel après TECH7A | Nouvel effet / décision |
|---|---:|:---:|---|---|---|
| `company_fundidora_monterrey` | +5 % | A | Sidérurgie historiquement centrée sur rails et roues ferroviaires | Throughput de tout le bâtiment régional | +5 % de production de `transportation` |
| `company_william_sandford` | +15 % | A | Production de matériel et contrats d'acier ferroviaires à Lithgow | Throughput de tout le bâtiment régional | +15 % de production de `transportation` |
| `company_mines_anzin` | +10 % | B | Logistique d'un bassin charbonnier ; aucun bâtiment ferroviaire dans la compagnie | Throughput de tout le bâtiment régional | Conservé comme abstraction d'infrastructure régionale |
| `company_john_cockerill` | +10 % | A | Construction de locomotives et de matériel ferroviaire | Throughput de tout le bâtiment régional | +10 % de production de `transportation` |
| `company_kouppas` | +10 % | C | Construction mécanique générale ; lien ferroviaire insuffisamment explicite dans la définition | Throughput de tout le bâtiment régional | Conservé par prudence |
| `company_maschinenfabrik_oerlikon` | +10 % | A | Traction électrique et expérimentation ferroviaire | Throughput de tout le bâtiment régional | +10 % de production de `transportation` |
| `company_oesterreichisch_alpine_montangesellschaft` | +5 % | A | Rails, matériel ferroviaire et `building_railway` comme extension | Throughput de tout le bâtiment régional | +5 % de production de `transportation` |
| `company_hanseong_jeongi_hoesa` | +5 % | A | Compagnie électrique exploitant le tramway de Séoul ; `building_railway` comme extension | Throughput de tout le bâtiment régional | +5 % de production de `transportation` |
| `company_oriental_development_company` | +5 % | B | Développement agricole, migration et aménagement colonial général | Throughput de tout le bâtiment régional | Conservé comme abstraction d'infrastructure régionale |
| `company_turkish_petroleum` | +5 % | B | Extraction, commerce et logistique énergétique ; bonus de capacité commerciale associé | Throughput de tout le bâtiment régional | Conservé comme abstraction logistique générale |
| `company_putilov_company` | +10 % | A | Production majeure de locomotives, wagons et rails | Throughput de tout le bâtiment régional | +10 % de production de `transportation` |
| `company_branobel` | +5 % | B | Transport et distribution pétrolière multimodale ; aucun bâtiment ferroviaire dans la compagnie | Throughput de tout le bâtiment régional | Conservé comme abstraction logistique générale |
| `company_john_hughes` | +10 % | A | Société du charbon, du fer et des rails ; `building_railway` comme extension | Throughput de tout le bâtiment régional | +10 % de production de `transportation` |
| `company_morton_salt` | +10 % | B | Distribution de masse du sel et débouchés agricoles, sans spécialisation ferroviaire attestée dans le mod | Throughput de tout le bâtiment régional | Conservé comme abstraction logistique générale |
| `company_krupp` | +10 % | A | Rails, essieux, ressorts et bandages de roues ferroviaires | Throughput de tout le bâtiment régional | +10 % de production de `transportation` |
| `mod_polish_rail_throughput` | +10 % | A | ID explicitement ferroviaire | Throughput de tout le bâtiment régional | +10 % de production de `transportation` |
| `modifier_modded_rail_network` | +25 % | A | ID explicitement ferroviaire ; le +5 % de construction associé reste intact | Throughput de tout le bâtiment régional | +25 % de production de `transportation` |

Résultat : 6 occurrences de `building_railway_throughput_add` sont conservées et 11 sont converties en `goods_output_transportation_mult`.

Sources de décision : les `building_types`, `extension_building_types`, conditions de création et bonus associés des définitions de compagnie locales constituent la source gameplay primaire. La spécialisation ferroviaire des conversions est en outre corroborée par les archives ou historiques institutionnels disponibles pour [Fundidora Monterrey](https://www.hcnl.gob.mx/archivo/2022/05/fundidora-de-monterrey-1.php), [William Sandford/Lithgow](https://apps.environment.nsw.gov.au/dpcheritageapp/ViewHeritageItemDetails.aspx?ID=5045094), [John Cockerill](https://johncockerill.com/wp-content/uploads/2020/04/John-Cockerill_Services_Locomotives-and-Rail-Services.pdf?download=true), [Oerlikon](https://www.asme.org/getmedia/3d1324d1-2b71-4d41-9e5d-c84b8279d6c8/279-crocodile-locomotive-ce-68-ii.pdf), [Hanseong Jeongi Hoesa](https://contents.history.go.kr/mobile/tg/view.do?ganada=&levelId=tg_004_1340&pageUnit=10&subjectCode=tg_ty_020&tabId=02), [Putilov](https://www.socialhistoryportal.org/node/109766), [John Hughes](https://glamarchives.gov.uk/hughesovka-an-industrial-city-with-welsh-roots/the-works-from-iron-to-steel-1870s-1900/) et [Krupp](https://www.thyssenkrupp.com/en/company/history/companies-going-through-change/krupp-development-to-a-major-group.html).

### Simulation économique

Le multiplicateur s'applique à toute la production de `transportation` du bâtiment. Les voitures de voyageurs s'ajoutent au PM ferroviaire avant application du bonus.

| Configuration | Base | +5 % | +10 % | +15 % | +25 % |
|---|---:|---:|---:|---:|---:|
| Diesel terminal, sans voitures | 40 | 42 | 44 | 46 | 50 |
| Diesel + voitures en bois | 50 | 52,5 | 55 | 57,5 | 62,5 |
| Diesel + voitures en acier | 55 | 57,75 | 60,5 | 63,25 | 68,75 |
| Principe Transport III diesel, sans voitures | 50 | 52,5 | 55 | 57,5 | 62,5 |
| Principe Transport III + voitures en bois | 60 | 63 | 66 | 69 | 75 |
| Principe Transport III + voitures en acier | 65 | 68,25 | 71,5 | 74,75 | 81,25 |

Même au maximum combiné, le bonus de +25 % ajoute 16,25 unités de `transportation` par niveau sans créer d'infrastructure supplémentaire. L'ordre de grandeur économique de l'ancien pourcentage est donc conservé sans convertir le pourcentage en quantité fixe.

### Contrôles runtime ciblés

1. Charger une sauvegarde avec une compagnie convertie prospère et un `building_railway` employé.
2. Vérifier que l'infobulle affiche « Building Transportation output » ou « Production de transport des bâtiments » selon la langue.
3. Comparer les ordres de vente de `transportation` avant et après activation du bonus.
4. Confirmer que les valeurs d'infrastructure des PM routes, canaux et rail restent strictement inchangées.
5. Confirmer que le plafond d'économies d'échelle fourni par les canaux reste strictement inchangé.
6. Contrôler séparément un centre urbain produisant `transportation`, car le multiplicateur par bien s'y applique également.
