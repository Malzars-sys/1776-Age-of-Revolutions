# Décisions historiques et limites de TECH-R2

Référence : 1er janvier 1776. Les choix de PM sont des approximations techniques bornées, soumises au joueur ; ils ne certifient pas l’absence de tous les savoirs correspondants dans chaque pays. Les profils historiques nationaux ne sont pas élargis sans preuve.

## Alliages : correction de la dépendance, sans cadeau national

Le nœud `alloysworking` représente, selon la note préexistante du mod, une production régulière et contrôlée d’alliages, et non toute pratique artisanale du bronze. L’usine `building_alloys_plant` et sa recette `pm_basic_smelting_process` sont relues : fer 25, cuivre 15, plomb 10 et charbon 10 donnent alliages 60 à pleine activité écrite ; la recette ne requiert pas de coke. Ces valeurs ne sont pas des observations moteur.

La notice archéologique de [Saltford, Historic England](https://historicengland.org.uk/listing/the-list/list-entry/1004607) décrit les ateliers de laiton du XVIIIe siècle, leurs marteaux hydrauliques, le recuit au charbon de bois puis les fours isolant le métal des fumées de houille. Elle permet de distinguer ces opérations de la fonte au coke. [Ironbridge Gorge Museum Trust](https://www.ironbridge.org.uk/about-us/key-figures-in-the-history-of-the-ironbridge-gorge/) situe en 1709 le procédé de Darby pour la fonte au coke. L’existence de ce procédé ne le rend pas nécessaire à toutes les productions d’alliages.

Décision de modèle, explicitement inférée de ces sources et du contenu de la recette : parents `shaft_mining` + `organized_workshops`. Le premier représente le socle minier, le second l’organisation des ateliers ; cela ne prétend pas que chaque établissement devait exploiter son propre puits. Aucun nœud intermédiaire nouveau, aucune généralisation du coke à AUS/BEO/FRA/PRU/RUS/SAX/SWE, aucun changement de leur savoir acquis. Les douze détenteurs actuels possèdent déjà les deux parents.

La note ancienne en énumérait neuf ; le résolveur actuel retrouve aussi MGL, XIN et YUN, déjà détenteurs avant R2. Ce constat ne valide pas historiquement ces extensions. Le relevé Git en lecture seule montre `shaft_mining` lors de l’introduction du nœud le 16 septembre (`bf0b53a`), puis son remplacement par `coke_smelting` le 17 octobre (`73877cf`). La correction s’applique au fichier courant et conserve les révisions ultérieures de l’aluminium : aucune restauration du fichier ancien.

Impact global exhaustif : cinq pays remplissaient les seuls parents directs de recherche, contre 93 après. C’est une modification réelle de l’accès futur, **pas 88 attributions**, ni une preuve que tous les autres critères de recherche sont remplis. Le coût, l’ère, la catégorie, les recettes, le nombre de détenteurs et tous les autres parents sont conservés. Bauxite, Bayer, chimie et électricité gardent leurs gates tardifs. ALLOYS_GLOBAL_IMPACT.csv contient les 470 pays.

## Ateliers : procédés compatibles avec le profil conservé

RUS/Brest et GEN : exploitation forestière simple plutôt que la recette de scierie exigeant `mechanical_tools`. GEN : meubles artisanaux et outils simples ; VEN/Istrie : outils simples. La recette d’outils avancée consommait acier et demandait `precision_boring`. Les anciens PM existent déjà dans les mêmes groupes ; aucune machine ou industrie n’est créée.

Les tours existaient avant 1776 : les [collections Dominy de Winterthur](https://dominycollections.winterthur.org/tools-of-the-trade/woodworking/lathe/) conservent notamment un tour à perche daté 1750–1775. Le repli de GEN ne signifie donc pas « aucun tour à Gênes ». Il évite d’assimiler un artisanat local à toute la capacité industrielle du nœud partagé `mechanical_tools`. Une future preuve locale pourrait justifier une autre solution ; aucune suppression mondiale de cette recette.

## Administration, transport et textile

VEN/Venetia et KND/Ceylan : organisation simple en l’absence de la technologie précise de registre systématique. On ne nie pas leurs archives ou leur administration. Ce repli retire le papier et ramène, par niveau et à activité comparable, bureaucratie 50→10 et capacité fiscale 10→2. Il peut créer une difficulté économique : le test joueur doit la mesurer. Aucune bureaucratie compensatoire ni nouveau registre national n’est inventé.

KND : la couche de canaux industriels est désactivée, tout en conservant routes traditionnelles, absence de rail et absence de train voyageurs. Ce choix ne supprime pas l’irrigation ancienne : les canaux représentés par ce PM sont un réseau industriel de transport avec intrants et métiers spécialisés. Les deux déclarations historiques sont corrigées sans les compter comme deux nouvelles constructions.

BIK : désactiver la conversion en vêtements de luxe incompatible avec le savoir textile écrit, tout en conservant vêtements cousus à la main et métiers traditionnels. Il ne s’agit pas de nier les traditions textiles du Rajasthan. Le gate de construction de la manufacture demeure un dossier P1 indépendant ; aucun profil textile complet n’est certifié.

## Commerce limité : trois centres, deux pays

KND et CAR conservent leurs centres et la propriété économique existante, avec `pm_trade_center_trade_quantity_limited` sans gate financier. Le commerce normal exige `organized_financial_institutions`. Les [papiers d’Arcot conservés au London Museum, 1750–1780](https://www.londonmuseum.org.uk/collections/v/object-779416/document/) attestent des relations financières et commerciales complexes dans le Carnatic. Cela ne prouve ni l’absence d’institutions, ni l’équivalence de toutes ces pratiques au nœud bancaire du mod. Le choix conservateur corrige la sélection incompatible sans attribuer un appareil financier complet ; ses effets, quantité commerciale −50 % et demande de marine marchande 4→3, restent à tester. CAR a deux centres, Circars et Madras.

## Huit absences d’historique : aucun faux succès

MISSING_HISTORY_REVIEW.csv donne pour chaque TAG cultures, religion écrite ou absente, capitales lues sans les modifier, régions, population effective écrite, bâtiments, unités, source et limites chronologiques. Les huit absences restent **OPEN_P3_NO_FUNCTIONAL_CHANGE** ; leur intention et leur innocuité moteur ne sont pas démontrées par le seul statut décentralisé. Sept n’ont aucun bâtiment explicite, INDOP possède sa plantation d’épices avec deux PM compatibles sans gate. Aucun profil européen, industrie, loi ou technologie n’est créé.

Sources individuelles : Institut Raoni pour AP7 (pratiques actuelles, sans rétroprojection certaine en 1776) ; AMNH pour CKC (collections tardives, sans projection des armes à feu) ; parc national Taroko pour FRS (exemple truku, pas l’ensemble de Taïwan) ; Smithsonian pour GR7 (kayaks, chronologie limitée) ; NPS et histoire agricole officielle hawaïenne pour HWA ; Australian Museum pour INDOP (textiles et parenté, sans couvrir tout Sumatra) ; patrimoine autochtone de Tasmanie pour PLW ; Te Papa pour TTI (fibres, tissage et adaptations). Les liens précis et restrictions sont conservés dans le CSV.

GR7 porte une capitale hors de sa région possédée ; PLW a une population écrite de 200. Ces constats sont des renvois documentaires à WORLD, jamais une permission TECH de modifier la carte ou les POP. La décision demeure ouverte pour chacun, y compris les pratiques agricoles, institutions locales et équivalences techniques qui demandent des recherches spécialisées.

## Signaux laissés ouverts et protections

Les 121 choix de commerce normal restants et les 18 ports ne sont pas tous rétrogradés en bloc : leur rôle économique et leurs capacités locales demandent une décision propre. Deux recettes d’artillerie sans alternative compatible restent P0. Les 54 gates de construction ne prouvent pas à eux seuls une production nulle d’un bâtiment déjà installé. Les 16 alertes régionales de ressource ne certifient pas l’allocation à la portion nationale. Aucun faux positif n’est déclaré sans preuve.

Lois et unités des 93 nouveaux TAGs sont signalées séparément par le nouveau contrat en lecture seule. Les demandes conditionnelles de lois ne sont pas des lois actives certifiées. Les incompatibilités politiques BGT préexistantes restent hors périmètre ; la validation humaine réelle de sa mine n’est ni annulée ni étendue.
