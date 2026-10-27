# Sources et arbitrages — départ au 1er janvier 1776

Les dossiers antérieurs sont réutilisés ; les sources ci-dessous complètent uniquement les points décisifs. Les seuils de sélection par province sont des **arbitrages B**, pas des coordonnées cadastrales attestées.

| Point | Source effectivement consultée | Conclusion et limite |
|---|---|---|
| Nouveau-Brunswick | [Gouvernement du Nouveau-Brunswick, histoire](https://www.gnb.ca/en/admin/about-nb/history.html) ; [Canada, Nouvelle-Écosse](https://www.canada.ca/en/canadian-heritage/services/provincial-territorial-symbols-canada/nova-scotia.html) | Séparation du Nouveau-Brunswick en 1784. La dualité NBS/NVS en 1776 est anachronique. Le dossier local `MAP1_CASE_DOSSIERS/R8_NORTH_AMERICA_CARIBBEAN-0065.md`, notamment lignes 1–22, avait déjà établi cette conclusion. Cela ne prouve pas le contrôle colonial de chaque forêt ni les limites des communautés autochtones. |
| Interdiction coloniale | [Archives nationales américaines, Roots of Rebellion](https://visit.archives.gov/whats-on/explore-exhibits/roots-rebellion) ; [texte de la Proclamation de 1763, gouvernement du Canada](https://www.rcaanc-cirnac.gc.ca/eng/1370355181092/1607905122267) | La Couronne interdit les établissements au-delà de la frontière réservée. L'interdiction est contournée et des cessions ultérieures déplacent la ligne. Le choix du joueur de bloquer toute politique de colonisation avant l'indépendance est une **abstraction de gameplay**, pas l'affirmation qu'aucun colon ne s'est installé à l'ouest après 1763. |
| Frontière septentrionale | [NPS, traité de Fort Stanwix de 1768](https://www.nps.gov/articles/000/1768-boundary-line-treaty-of-fort-stanwix.htm) | Négociations de 1768, maintien des patries des Six Nations, ambiguïté du portage Oneida et révisions ultérieures en Pennsylvanie. Les signatures ne valent pas consentement unanime des autres nations. Le secteur occidental de New York est corrigé ; la longitude du script est une simplification, pas le décalque de tout le traité. |
| Caroline du Nord | [NC Department of Natural and Cultural Resources, Tryon Mountain, O-77](https://www.dncr.nc.gov/blog/2024/01/19/tryon-mountain-o-77) | Bornes de 1767 : Reedy River, Tryon Mountain et projet de ligne vers les mines de Chiswell. L'expulsion des colons à l'ouest était exigée pour janvier 1768. Ces repères guident une répartition de provinces, sans prétendre résoudre chaque occupation ou révision ultérieure. |
| Basses villes cherokees | [NC Historic Preservation Office, ER 07-0850](https://files.nc.gov/ncdcr/historic-preservation-office/PDFs/ER%2007-0850.pdf) | Passage indexé consulté sur les campagnes de l'été 1776 contre Keowee, Seneca, Tugaloo et Tamassee. Ces destructions sont **postérieures** au départ du scénario ; le petit noyau occidental de Caroline du Sud reste cherokee au 1er janvier. Le PDF n'a pas été intégralement lu. |
| Cessions de Géorgie | [proclamation de James Wright du 11 juin 1773, Digital Library of Georgia / Library of Congress](https://dlg.usg.edu/record/loc_broadsides-and-other-printed-ephemera_rbpe-01401200) | Texte du document consulté : cession du 1er juin de terres vers les Little/Broad/Savannah et Oconee, et d'une autre bande Ogeechee–Altamaha. On ne supprime donc pas les terres ouvertes avant 1776 en recopiant simplement la ligne de 1763. Le noyau de la future Wilkes County est conservé. |
| Oconee et contrôle creek | [UGA Press, Georgia 1763–1774](https://ugapress.manifoldapp.org/read/the-american-revolution-in-georgia-1763-1789/section/dbff0882-9504-416c-90c5-307b74234f53) ; [UGA, The Georgia Indian Frontier, 1773–1783](https://dlg.usg.edu/record/dlg_ggpd_s-ga-bs730-b-pm1-b1975-bi5) | Limites et résistances aux extensions coloniales ; ne pas rétroprojeter les cessions de 1783 ou des décennies suivantes. Seuls les grands secteurs occidentaux manifestement trop étendus sont transférés ; le front oriental précis reste à affiner. |

## Géométrie vérifiée

Le calage neuf réemploie les coordonnées GeoNames **déjà présentes** dans MAP1C et les locators effectifs actuels. Les villes modernes servent de repères de géométrie, pas de preuve de contrôle historique. Fichiers : `FRONTIER/GEODETIC_CONTROLS.json`, `GEODETIC_MODEL.json`, `GEODETIC_EVALUATION.json`.

- 9 repères FIT : RMS **1,71 px**, maximum 2,68 px.
- 32 repères CHECK : RMS **5,87 px**, maximum **11,62 px**.
- Pas d'intervalle de confiance cadastral ni de certitude à la cellule frontière.

Les coordonnées des noyaux coloniaux conservés sont tracées dans `protected_sites` du plan. Le lien militaire demandé par le joueur est revalidé par **305 pixels contigus**, avec contrôle des impassabilités et des adjacences natives. L'ancien point d'arrivée près de l'ouest de New York n'est pas une obligation historique ou un RGB imposé par le joueur : le contact passe désormais par une autre frontière directe de l'Ontario avec les colonies. HBC et Québec ne changent pas de contour.

## ColGrep local

Un appel `colgrep --agent` dans `docs` a été exécuté, code 0, **249,47 s** de commande complète. Il cherchait les dossiers R8 sur les Maritimes, les Treize Colonies et les lignes de 1763/1768. Les résultats visibles renvoyaient surtout à `CANADA-01/SOURCES_AND_FRONTIERS.md:1–41` et aux anciens journaux d'utilisation de ColGrep ; chemins et passages utiles ont été relus. Le dossier NBS décisif a été retrouvé par recherche exacte.

Pas de nouvelle tentative redondante, de changement de modèle, de reconstruction d'index ou d'exécution de scripts globaux suggérés. La durée inclut recherche et inférence ; aucun compteur GPU ou de tokens Codex indépendant. **Aucune économie exacte ni recherche évitée démontrée pour cet appel.**
