# VOC — monogramme historique et plantations de poivre à Java (1776)

Date de préparation : 28 octobre 2026. Statut : **IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION** (PR non fusionnée).

## Portée et état réel examiné

- Base Git : `75a5ae9a190993d440f650097b0e09cbc7fc273e`, branche `main`.
- Icône actuelle de la compagnie : `nl_voc.dds` (monogramme dans un emblème bleu ornemental avec couronne, lions, inscription et date 1602). L'ancien fichier est **préservé**, sans effacer l'asset fourni antérieurement par le joueur.
- Source historique : le monogramme **VOC** entrelacé est attesté sur des objets de compagnie des XVIIe et XVIIIe siècles. Le nouvel asset `nl_voc_monogram_1776.dds` est une **adaptation graphique moderne simplifiée** du monogramme historique ; ce n'est pas un fac-similé certifié d'un sceau particulier de 1776. Aucune couronne ou armoirie imaginaire n'est ajoutée.
- L'historique de bâtiments `common/history/buildings/12_indonesia.txt` **ne contenait aucun** `building_spice_plantation` dans les trois blocs DEI de Java au moment de cette passe. L'ancien rapport `TECH6A3P_SPICES_PRESTIGE_COMPANY_INTEGRATION.md` annonçait 4/2/2 niveaux et leur ownership VOC, mais cette annonce ne correspond **pas** au fichier actuel ; il ne faut ni la présenter comme installée, ni additionner ses niveaux par inadvertance.

## Source et calibration historique

| Région technique | Avant sur DEI | Après | Justification et limite |
| --- | ---: | ---: | --- |
| `STATE_WEST_JAVA` | 0 | **3** | Poivre à Banten / Java occidental et interventions VOC bien attestées pour les années 1760–1790 ; l'État technique n'est pas un cadastre de Banten. |
| `STATE_CENTRAL_JAVA` | 0 | **2** | Approvisionnements javanais centraux moins concentrés, attestés au milieu du XVIIIe siècle ; niveau 2 de balance, pas un tonnage démontré pour 1776. |
| `STATE_EAST_JAVA` | 0 | **1** | Production/approvisionnement poivrier secondaire, attesté dans les réseaux de la côte nord-est ; niveau 1 prudent. |
| **Total** | **0** | **6** | Aucun niveau ajouté dans les États non contrôlés par DEI à Java. |

La catégorie `spices` représente ici **surtout le poivre**. La muscade et le macis de Banda, ainsi que le girofle d'Ambon, ne sont pas artificiellement attribués à Java. L'implication commerciale et la collecte VOC n'impliquent pas que la compagnie possédait directement toutes les parcelles cultivées : l'ownership `company_dutch_east_india_company` est une abstraction du système de monopoles et d'approvisionnements dans la portion `DEI`.

Toutes les nouvelles plantations sont initialisées avec `pm_spice_cultivation`, `pm_road_carts`, `reserves = 1`, propriété `company_dutch_east_india_company` de `c:NET`. Aucun changement des propriétaires politiques, POPs, bâtiments déjà présents, potentialités agricoles, recettes, technologies, États YOG/SRK ou PM externes. Aucun effectif ni profit garanti.

## Sources vérifiées

1. Ota Atsushi, **‘Traditional’ versus ‘Modern’ Administrative Concepts: Dutch Intervention and its Results in Rural Banten, 1760–1790**, *Itinerario* (2011), https://www.cambridge.org/core/journals/itinerario/article/abs/traditional-versus-modern-administrative-concepts-dutch-intervention-and-its-results-in-rural-banten-17601790/FE659CF627304EC37CD0E9C8DBB7A2C3 — promotion poivrière dans l'ouest de Java ; consulter notamment les rapports de plantation des années 1760–1770 cités par l'auteur.
2. Kwee Hui Kian, **The Political Economy of Java's Northeast Coast, c. 1740–1800**, TANAP Monographs (2006), chapitre sur les approvisionnements et contingents : la VOC cherchait à acheter du poivre au centre et à l'est de Java au cours des années 1750 ; ce constat ne permet pas de convertir directement les volumes en niveaux du jeu.
3. Amsterdam Museum, **emblème VOC sur porcelaine 1650–1674**, https://www.worldhistory.org/image/15178/dutch-east-india-company-logo/ — monogramme historique public-domain documenté.
4. Rijksmuseum, **The Arms of the Dutch East India Company and of the Town of Batavia** (1651), https://www.rijksmuseum.nl/en/collection/object/The-Arms-of-the-Dutch-East-India-Company-and-of-the-Town-of-Batavia--c168a0bb084734e9c6a9bc0ee5c4319e — distinction entre représentation héraldique d'époque et monogramme simplifié.
5. S. J. Miske, **Colonisation and cultivation: Nutmeg production, labour and ecology on the Banda Islands**, *Journal of Southeast Asian Studies* (2026), https://www.cambridge.org/core/journals/journal-of-southeast-asian-studies/article/colonisation-and-cultivation-nutmeg-production-labour-and-ecology-on-the-banda-islands-before-and-after-the-conquest-of-1621/BF86973D1324DB0D0FE680E0BF5291F7 — muscade concentrée dans les Banda, donc ne pas assimiler mécaniquement l'épice à la production javanaise.

## Contrôles du patch

- Exactement **un** nouveau bloc spice dans chacun des trois `region_state:DEI` javanais : 3/2/1 niveaux.
- Précédente déclaration des autres bâtiments inchangée ; niveaux des nouvelles plantations sous 1–3.
- DDS supplémentaire 256 × 256, RGBA 32 bits non compressé, alpha, sans remplacer l'ancien `nl_voc.dds` ; une seule référence de compagnie change.
- Recettes/PM de `building_spice_plantation` et potentiel agricole présents dans les scripts du dépôt ; aucun ajustement de capacité n'a été nécessaire.
- Contrôles statiques du patch ; **aucun lancement du moteur** ni vérification d'emploi, d'accès au marché, de prestige ou de rendu en jeu réalisés dans cette PR.

## Protocole humain

Nouvelle partie en 1776 : vérifier l'icône de la VOC (et la distinction avec l'EIC), la présence des plantations de poivre/épices **3/2/1** uniquement dans les portions DEI de Java occidental/central/oriental, leur ownership VOC (`c:NET`), les PM et l'emploi, puis comparer le café/sucre et les cours javanaises YOG/SRK ; exécuter un mois et sauvegarder/recharger. Signaler toute anomalie de production/market access. **Ne pas considérer la PR comme validée en jeu avant reçu du joueur.**
