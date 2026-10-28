# NORTHWEST-01 — Nouvelle-Espagne et Alaska, 1er janvier 1776

**27 octobre 2026 — IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION.** Installation effectuée. Aucun moteur lancé, reçu joueur, commit, merge, rebase ou push. Le vanilla reste en lecture seule.

## Résultat en Nouvelle-Espagne

Les implantations espagnoles sont distinguées de la souveraineté revendiquée et des domaines autochtones. La Californie entière n'appartient plus aux Apaches ; les noyaux de missions et présidios, la vallée du Rio Grande et les postes texans sont reliés au territoire principal.

| State Region | Provinces SC1 après correction |
|---|---:|
| Haute-Californie | 11 |
| Arizona | 4 |
| Nouveau-Mexique | 9 |
| Texas | 15 |
| Sonora | 23 |
| Chihuahua | 49 |
| Baja California | 28, conservées |
| Durango | 26, conservées |
| Rio Grande | 66, conservées |
| Sinaloa | 9, conservées |

Les **25 points de référence**, comprenant deux passages de corridor, sont reliés par côtés de provinces au même ensemble principal de **504 provinces SC1**, pas seulement à une autre enclave. Les portions SC1 traitées sont explicitement incorporées. Les tronçons sur des territoires non administrés représentent la concession de jouabilité demandée ; **un itinéraire d'Anza ne prouve pas une annexion historique continue**.

Les sièges affichés deviennent **Monterey, Tubac et San Antonio** ; le port californien est déplacé de San Francisco à Monterey. San Francisco, San Juan Capistrano, Nacogdoches et le présidio de Tucson ne sont pas avancés au 1er janvier. Socorro est un point de passage du corridor, pas une ville réoccupée. Les noyaux de Janos, Carrizal, Casas Grandes, Santa Fe, Abiquiu, Taos, San Antonio, La Bahía et Bucareli sont représentés à l'échelle des provinces existantes.

## Alaska : les Russes sont présents, la compagnie pas encore

La **Compagnie russo-américaine de 1799 est retirée du démarrage russe**, ainsi que sa tutelle de compagnie à charte sur ALK. Les autres commandes initiales de Russie sont conservées. ALK devient une dépendance ordinaire, nommée avant 1799 **Comptoirs russes des Aléoutiennes**. Cette représentation mécanique ne prétend pas qu'un gouvernement colonial unifié existait déjà.

Son territoire est limité à une nouvelle petite région d'**Unalaska**, capitale et port. La présence commerciale des années 1770 n'est pas confondue avec la colonie de Kodiak de 1784 ou le monopole de 1799. Le claim ALK sur tout l'Alaska est retiré ; seul le comptoir reçoit un claim. Les définitions futures de la compagnie restent disponibles et son nom exige désormais une date au moins égale à 1799.

Un composant insulaire de **459 pixels existants** est séparé de `xC00000` en `xC00001`, dans le State_ID **3160**. Aucune côte n'est redessinée, aucune terre ni aucun pont marin ajoutés. L'exception maritime a été explicitement autorisée par le joueur. Le port possède une sortie réelle vers la **mer de Béring (3041)** et utilise le PM de havre commercial traditionnel déjà présent dans le mod. Ni dock industriel ni paquet technologique européen copié.

Les **1 921 habitants du comptoir** sont des cohortes héritées : 721 Russes et 1 200 personnes de la famille culturelle inuit du jeu. Ce placement est technique, pas un recensement d'Unalaska. L'île-province est un token de présence, pas une certification de domination exclusive sur tous les Unangans. Le port emploie théoriquement 700 personnes à plein régime et consomme bois/tissu : disponibilité de main-d'œuvre, importations, marine marchande et connexion au marché russe doivent être observées en jeu.

## Représentations autochtones et revendications

**16 nouveaux regroupements** : Unangan, Sugpiaq, Yupik, Iñupiat, Dena’ina, Tlingit/Haïda ; nord, vallée centrale et sud de Californie ; O’odham, peuples du Colorado, Hopis, Seris ; Lipans, Tonkawas et peuples du littoral texan. L'intérieur athabaskan et les Navajos, Apaches, Comanches, Caddos et Wichitas existants sont réutilisés là où le découpage les retient.

Ces ensembles ne simulent pas 16 gouvernements centralisés uniformes. Les limites sont régionales, parfois diffusement attestées, et les groupes côtiers divers ne sont pas tous individualisés. Les cartes linguistiques contemporaines servent seulement de repère ; les anciennes cultures de POPs restent imparfaites, notamment au Texas. Voir [les réserves sourcées](SOURCES.md).

Les revendications sont corrigées dans **13 State Regions**, plus celle du nouveau comptoir. Les claims USA de l'Ouest espagnol et les claims HBC de la façade pacifique sont retirés ; les prétentions nominales espagnoles de 1775 sont représentées au Washington, à l'Oregon et en Colombie-Britannique, sans transfert de leur contrôle autochtone. Ces claims portent sur des State Regions entiers : ils débordent parfois la côte ou le bassin justifié. Il ne s'agit ni d'une occupation espagnole de tout l'intérieur ni d'un règlement de 1819. La prétention espagnole sur le seul sud-est de l'Alaska reste insuffisamment représentable sans sous-région côtière : aucun claim sur tout l'Alaska n'a été ajouté pour la remplacer.

## Conservation, références et résultats

**1 144 attributions de provinces** changent par rapport à la baseline, nouveau RGB compris. Les **14 doubles attributions** héritées des zones Alaska/Nouveau-Mexique sont résolues ; le nombre mondial connu passe de 28 à 14, sans nouveau doublon ni province traitée laissée vide. Les anomalies extérieures ne sont ni masquées ni corrigées par cette passe.

Chaque total de cohorte, culture, religion et type de POP est conservé par State Region ; Alaska + comptoir constitue un seul domaine de conservation. Aucune inflation, conversion culturelle ou suppression de population. Les nouveaux propriétaires changent la ventilation par pays, sans déplacer des habitants entre régions continentales. **Tous les anciens bâtiments, niveaux, PM, propriétés économiques et formations sont conservés** ; seul un port est ajouté à Unalaska. Deux terres arables et deux potentiels de pêche sont transférés d'Alaska au comptoir, avec somme exacte conservée. Aucun don de réserve géologique.

Contrôles techniques : **76 réussites** dans `VALIDATION.json` ; **8 tests** de non-régression de la loi américaine réussis. Les 16 nouvelles initialisations autochtones sont `PASS_STATIC_ONLY`, avec seul savoir explicite de traitement alimentaire traditionnel. Les sept profils existants audités conservent leurs résultats hérités : SC1 14 signalements, ALK 3, ATB 3, APC 2, NVJ 2, COM 2 et RUS 4. **Aucun nouveau signalement** de cette famille n'est ajouté ; ces dettes ne sont pas déclarées résolues.

Les territoires approuvés HBC, Québec, Treize Colonies, Louisiane, Florides et autres témoins protégés restent identiques. Le bitmap est comparé pixel par pixel au départ de cette mission ; seule l'île autorisée change de couleur. Les travaux sahéliens concurrents sont conservés et distingués dans `CONCURRENT_FILES.json` ; l'échec initial du contrôle global avant cette identification reste archivé. Aucun suivi WORLD ou SERG n'est mis à jour.

## Fichiers et preuves

Les **23 fichiers runtime** modifiés ou créés sont listés avec empreintes dans `PATCH.json`, avec copies avant et patch livrable. Ils couvrent histoires d'États/POPs/bâtiments, définitions ALK et nouveaux pays, initialisations Russie/ALK/peuples, relation russe, nom dynamique, flags de représentation, localisation FR/EN, région stratégique, définition de régions, cinq familles de locators, terrain et bitmap. Les flags autochtones sont des marqueurs de jeu, pas des drapeaux historiques certifiés.

Les trois outils `northwest01_geometry.py`, `northwest01.py` et `northwest01_verify.py` conservent la chaîne de préparation et de contrôle. La première localisation rejetée et les raisons de son rejet restent archivées. [ColGrep](COLGREP.md) : un appel local terminé, 272,65 secondes, pertinence partielle ; pas d'économie exacte de quota démontrée.

## Test joueur et questions ouvertes

Créer une **nouvelle partie en 1776** : vérifier les postes espagnols, sièges et claims ; parcourir leurs corridors et contrôler les bâtiments conservés. Vérifier que les Russes n'ont plus une compagnie de 1799 ni le littoral continental d'Alaska, puis ouvrir le port d'Unalaska et ses importations, son emploi et son accès au marché russe. Contrôler les intérêts et priorités de colonisation entre SC1, USA, Russie et HBC. Faire un mois de simulation, vérifier un éventuel changement de PM du petit port par l'IA, sauvegarder/recharger.

Restent ouverts : frontières fines entre peuples, autonomie locale dans les noyaux mexicains conservés et Baja, détails du contrôle des missions, démographie historique et cultures fines, claim espagnol du sud-est alaskien, limites précises des revendications côtières et effets économiques réellement observés. Les corridors et le traitement géographique insulaire sont des approximations explicites. Cette livraison ne clôt pas toute l'Amérique du Nord ni ne certifie toutes ses frontières.
