# Justification historique et abstractions

Référence : 1er janvier 1776. Statut : `IMPLEMENTED_READY_FOR_RUNTIME_VALIDATION`.

## Métallurgie traditionnelle

Conserver un déblocage précoce distingue les petites productions de bronze, laiton et alliages d'étain de la métallurgie électrique et de l'aluminium industriel. Le bien générique du mod demeure un agrégat : la recette ne prétend pas être une formulation métallurgique unique. Les volumes et prix sont des unités économiques, pas des masses stœchiométriques.

Les collections de [Glasgow Museums, English Pewter 1603–1850](https://collections.glasgowmuseums.com/mwebcgi/mweb?request=record%3Bid%3D534961%3Btype%3D801) documentent de la vaisselle et d'autres objets usuels en alliage d'étain aux XVIIe et XVIIIe siècles. Leur présence justifie un marché domestique antérieur à l'industrialisation ; la notice ne fournit pas de volumes nationaux utilisables pour calibrer une usine de jeu.

Les analyses des objets de l'épave du London (perdu en 1665), présentées dans [Historic England Research 16, The London wreck](https://historicengland.org.uk/images-books/publications/historic-england-research-16/he-research-16/), décrivent notamment des objets en laiton et en étain. Elles corroborent la diversité des petits objets métalliques ; les paramètres de jeu restent des choix d'équilibrage.

## Artillerie

L'étude des marquages et des pièces conservées publiée par Thor Borresen, [The Markings of English Cannon Captured at Yorktown](https://www.reenactor.ru/ARH/PDF/Borresen.pdf), reproduit entre autres un canon en bronze de 1761 et des obusiers coulés en 1755, 1758 et 1760. Ces pièces sont antérieures au départ du mod. Le PM de bronze est une alternative aux canons en fer, pas un remplacement universel de l'artillerie de 1776.

La consommation de fer résiduelle représente les ferrures et équipements, le bois dur les affûts, et le bien alliages les pièces coulées en bronze. Aucun cuivre brut supplémentaire n'est requis dans ce PM, pour éviter le double comptage du métal déjà contenu dans le produit acheté.

## Ustensiles et chaîne technologique

Le premier assortiment associe désormais le fer forgé et les alliages coulés : crochets et tisonniers de fer, boutons, ferrures et petits ustensiles moulés. Le cuivre et les alliages du palier suivant représentent des objets différents fabriqués dans un même atelier élargi : chaudronnerie de cuivre, bougeoirs et ferrures en alliage, pièces de fer. Ce n'est pas une charge de laiton à laquelle on ajouterait arbitrairement de grandes quantités de cuivre.

Le plomb est employé aux deux paliers tardifs pour des poids et garnitures d'objets non alimentaires, sans présenter une vaisselle au plomb comme un progrès sanitaire. Le dernier assortiment réunit acier, cuivre, alliages, plomb et aluminium comme demandé ; l'aluminium oblige à attendre le nœud existant `bayer_process` en ère X. Ce palier n'est pas distribué aux États de 1776.

À la demande ultérieure du joueur, les recettes secondaires produisent maintenant le bien distinct « Quincaillerie », classé parmi les biens courants. L'abstraction antérieure par les meubles est abandonnée ; elle reste documentée uniquement dans l'archive V1. Aucun nouveau besoin général : le bien rejoint les objets domestiques existants. Les noms historiques ne prétendent pas que la première matière était inconnue avant sa technologie de jeu ; les nœuds existants représentent l'organisation et l'échelle des ateliers.

La faible pollution et les emplois moins qualifiés du PM traditionnel distinguent l'atelier de l'aciérie électrique, sans donner au début de partie les volumes modernes. Les noms et descriptions FR/EN expliquent ces procédés ; les quantités restent affichées par les effets natifs.
