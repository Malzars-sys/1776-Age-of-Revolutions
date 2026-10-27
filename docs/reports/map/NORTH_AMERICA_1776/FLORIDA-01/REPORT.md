# FLORIDA-01 — deux régions administratives installées

26 octobre 2026 — départ au **1er janvier 1776**.

**IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** : la division administrative est installée, sans création de pays indépendant. Les possessions britanniques restent à **GBR** et les territoires séminoles restent à **SML**. Aucun retour joueur ni chargement moteur certifié.

## Découpage

| Région | Représentation installée |
|---|---|
| Floride orientale — STATE_FLORIDA, ID 293 conservé | 29 provinces : 24 britanniques et les 5 séminoles préexistantes. Ville et port placés à Saint Augustine. Sortie maritime atlantique 3146. |
| Floride occidentale — STATE_WEST_FLORIDA, nouvel ID 3159 | 9 provinces britanniques : 6 provinces du panhandle à l'ouest de l'Apalachicola, plus les 3 provinces côtières britanniques de Mobile/Biloxi déjà corrigées par R8. Ville et port placés à Pensacola. Sortie maritime du golfe 3060. |

Les identifiants et RGB des cellules ne changent pas. Le bitmap et les terrains sont inchangés ; seule leur appartenance aux State Regions est modifiée. La séparation est une **approximation B par provinces existantes**, pas un tracé cadastral de 1776. Les revendications britanniques vers le nord et Natchez ne sont pas transformées en possession effective.

La région occidentale forme une seule composante terrestre et touche directement la région orientale. L'Orientale conserve **exactement l'île isolée des Keys déjà présente** : avant, composantes 34 + 1 ; après, 28 + 1. Aucun pont terrestre ni île artificielle ajouté. Le premier contrôle naïf exigeant une composante unique échouait sur cette île héritée ; résultat conservé dans VALIDATION_INITIAL.json, diagnostic et comparaison exacte dans CONNECTIVITY_AUDIT.json.

Voir [FLORIDA_1776.png](FLORIDA_1776.png) et les correspondances exhaustives dans PLAN.json.

## Sources et calage

- [Florida Department of State, British Heritage Trail](https://dos.fl.gov/historical/preservation/heritage-trails/british-heritage-trail/) : deux administrations britanniques depuis 1763 ; Pensacola et Saint Augustine. Page de présentation consultée ; téléchargement du PDF complet en échec.
- [Florida Historical Society, division du 7 octobre 1763](https://myfloridahistory.org/date-in-history/october-07-1763/florida-divided-two-territories) et [University of Florida, East Florida Papers](https://www.uflib.ufl.edu/eastflorida/descript.htm) : limite Chattahoochee–Apalachicola. Passages accessibles/indexés consultés.
- [University of South Florida, British Possessions 1763–1767](https://fcit.usf.edu/florida/maps/pages/2400/f2434/f2434.htm) : carte d'atlas rétrospective de 1920, utile pour l'organisation générale, **pas une carte d'occupation autochtone**. La datation divergente de l'extension septentrionale ne justifie aucune annexion dans ce patch.
- Le cours de rivière de Natural Earth **déjà conservé dans MAP1C** et le modèle local R8 servent à choisir de quel côté sont les provinces. Le jeu Natural Earth nomme aussi « Chattahoochee » son segment inférieur correspondant à l'Apalachicola. Cours moderne et calage empirique, pas preuve de son chenal exact en 1776.
- Le modèle R8 et ses résidus sont conservés. Les sièges demandés ont été rabattus sur la terre actuelle du bitmap, au lieu de conserver un point projeté dans la mer. PLAN.json publie coordonnées, RGB et écarts de rabattement. Aucune précision géodésique supérieure au calage existant n'est revendiquée.

La distinction du traité de **Mobile** avec les conférences de **Picolata** reste celle de SOURCES.md du dossier R8. La division administrative ne résout pas à elle seule les limites du contrôle britannique effectif.

## Population, ressources et économie

Les effectifs cumulés, cultures, religions implicites/explicites et types de POP sont conservés pour l'ensemble des trois anciennes régions touchées. Les cohortes des trois cellules côtières britanniques quittent leurs anciens blocs Mississippi/Alabama pour la Floride occidentale. La population britannique de l'ancienne Floride est ventilée techniquement selon **24 provinces britanniques orientales / 6 occidentales**, en excluant les cinq provinces SML du poids. Ce n'est pas un recensement de 1776. L'ajustement de cette pondération est tracé dans POP_ALLOCATION_AMENDMENT.json.

Les **7 200 habitants SML** et leurs cinq provinces sont inchangés. Aucune conversion culturelle ni religieuse, ni compensation démographique ailleurs. Toutes les autres POPs, dont HBC et Québec, sont inchangées.

Tous les anciens bâtiments, niveaux, propriétaires économiques, PM et réserves restent identiques. Le port de l'ancienne région est conservé, avec le hub oriental déplacé de la baie de Tampa vers Saint Augustine. **Un niveau de port britannique est ajouté à Pensacola**, installation maritime historiquement défendable ; le PM de base est déjà disponible au profil GBR. Pas de nouvelle formation militaire ni de connaissance européenne distribuée.

Les budgets totaux de terres arables, ressources plafonnées et ressources latentes des trois anciennes régions sont conservés, répartis entre quatre régions après découpage. Bone Valley/phosphates du modèle floridien restent dans la péninsule. Les autres potentiels sont une ventilation technique des données héritées, pas des découvertes ou mines exploitées en 1776.

## Dépendances et fichiers

Vingt fichiers de jeu, listés avec empreintes dans PATCH.json :

- `map_data/state_regions/05_north_america.txt` : seules Floride/Alabama/Mississippi et nouvelle région occidentale.
- `common/history/states/00_states.txt` et `common/history/pops/05_north_america.txt` : blocs britanniques concernés et nouvel État.
- `common/history/buildings/1776_florida_west_port.txt` : seul ajout économique, port de Pensacola.
- Deux localisations FR/EN sous `replace/`, pour les deux régions et les nouveaux hubs.
- Les cinq fichiers de locators city/port/farm/mine/wood : positions orientales nécessaires et nouveaux locators 3159. Les anciens emplacements portuaires non construits de l'Alabama/Mississippi, devenus intérieurs après transfert de tout leur littoral, sont retirés avec leurs sorties maritimes et leurs locators 291/292 ; **aucun bâtiment portuaire existant supprimé**. Les autres identifiants sont conservés. Les locators de fortifications ont des identifiants indépendants, **pas les ID des State Regions** : aucun remplacement aveugle de leur entrée 293.
- Régions stratégiques, géographiques et pays libérables : la nouvelle région suit les appartenances de l'ancienne Floride ; FLR/ASA incluent les deux parties. Lorsqu'aucun fichier de mod n'existait, création d'une surcharge du fichier vanilla effectif, sans écriture dans le jeu de base.
- Vente/achat de Floride, boutons et dépendances cubaines : filtres étendus aux deux régions ; la vente transfère **toutes les parts du vendeur** concernées, sans annexion de SML. Les scopes représentatifs d'affichage ne sont pas dupliqués.
- Intervention espagnole dans la guerre américaine : objectif distinct sur chacune des deux parts britanniques, gardé par l'existence de la part. Les guerres séminoles restent centrées sur la région orientale où se trouvent les territoires SML.

Aucun changement de pays, de frontière de souveraineté, de contenu économique cubain, de suivi SERG/WORLD ou de travaux techniques concurrents. Préparation/application protégées par empreintes ; les fichiers partagés sont patchés depuis leur état courant.

## Vérification et limites

Résultats finaux : **42 contrôles statiques + 9 contrôles de références + 3 comparaisons technologiques réussis**, et **5 tests de dépendances Floride réussis**. Les 16 tests HBC et 4 tests Québec ont également été réexécutés avec succès pendant cette livraison. Les effectifs hérités après ventilation sont 24 766 habitants GBR et 7 200 SML à l'est, 7 177 GBR à l'ouest ; ces valeurs conservent les anciennes cohortes et ne sont pas certifiées comme recensements de 1776.

VALIDATION.json contient les contrôles de conservation, partition, références, hubs, sorties maritimes, connexité et dépendances. TECHNOLOGY_COMPARISON.json compare GBR avant/après : connaissances et constats hérités identiques ; aucune erreur de port nouvelle. **GBR reste FAIL_STATIC pour sa dette antérieure**, sans que cette livraison lui attribue des technologies pour la masquer. Les huit pays R8 conservent les mêmes propriétaires de provinces, y compris les trois cellules britanniques désormais dans une autre State Region.

La validation R8 initiale demeure un constat de la version R8 seule : ses empreintes sur les fichiers partagés et son ancienne exigence de State_ID côtier sont désormais dépassées par ce découpage autorisé. Elle n'est pas réécrite pour faire passer la nouvelle version ; le contrôle cumulatif ici vérifie les mêmes pays, les POPs protégées et les nouveaux State_ID explicitement.

**Reste ouvert** : le contrôle britannique de larges secteurs péninsulaires est encore surestimé ; Alachua/Cuscowilla, les autres communautés autochtones et les zones de Picolata demandent un autre calage politique. Cette passe installe les deux administrations et leurs sièges, pas une homologation historique de chaque possession britannique de Floride. Les données démographiques héritées des années 1830 restent une dette distincte.

## Validation en jeu à effectuer

Nouvelle partie en 1776 : noms des deux régions, Saint Augustine/Pensacola, port oriental et port occidental, accès au marché, frontières et cinq provinces SML. Vérifier les noms et positions des modèles 3D ; les orientations n'ont pas été observées dans le moteur. Contrôler HBC/Québec et les huit pays du lot R8, puis un mois de simulation et sauvegarde/rechargement. Les événements de vente et objectifs espagnols doivent traiter les deux régions et respecter le vendeur ; ne pas déclarer leur fonctionnement observé sur la seule base des contrôles de structure.

Version locale : 1.13.11 Matcha, descriptor `1.13.*`. Aucun commit, push ni chargement moteur déclaré.
