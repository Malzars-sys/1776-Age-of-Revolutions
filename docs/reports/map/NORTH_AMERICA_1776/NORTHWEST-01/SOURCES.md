# NORTHWEST-01 — sources, interprétations et limites

Mission du 27 octobre 2026 ; situation au **1er janvier 1776**. Les documents ci-dessous établissent des présences et grands espaces. Ils ne constituent pas une homologation de frontières politiques exactes par RGB.

## Travail réutilisé

Fiches R8 `0002/0003` (Alaska), `0006` (Arizona), `0010` (Baja), `0014` (Californie), `0069–0072` (Nouveau-Mexique), `0098` (Sonora), `0102/0103` (Texas), ainsi que les conclusions de `R8-CORRECTIONS-01/OPEN_PROBLEMS.md`. Elles distinguaient déjà promyshlenniki et gouvernement colonial, signalaient les Apaches en Californie, Tubac, les présidios texans et les doubles attributions. Leurs anciens statuts `MAPPING_REQUIRED` ne sont pas traités comme une preuve géographique déjà acquise.

Les méthodes des passes HBC/Canada/Louisiane sont réutilisées pour conservation, références et corridors. Les noyaux approuvés de ces passes restent protégés.

## Alaska : commerce et compagnie sont distincts

- [État d’Alaska, Russian Heritage](https://alaska.gov/kids/learn/russianheritage.htm), chronologie consultée : traite après 1741, implantation à Unalaska en 1772, Kodiak 1784, compagnie à charte en 1799.
- [Library of Congress, Crown and Commerce](https://www.loc.gov/exhibits/russian/russch2.html), page consultée : promyshlenniki, première colonie de Shelikhov à Kodiak en 1784 et monopole de 1799.
- [NPS, Russian America](https://www.nps.gov/subjects/nhlalaska/russian-alaska.htm), passages consultés sur traite, coercition et résistances autochtones. L'emploi de « première implantation permanente » pour Kodiak ne doit pas faire disparaître les comptoirs antérieurs. Les sources ne définissent pas toutes « établissement » et « colonie » de la même façon. Le mod retient **un comptoir précompagnie**, sans projeter l'administration de 1799 sur 1776.
- [NPS, Alaska Native Cultures](https://home.nps.gov/locations/alaska/native-culture.htm), description et référence à la carte linguistique Krauss et al. 2011 ; [document de l’État d’Alaska sur les régions culturelles](https://dnr.alaska.gov/commis/uploads/FAQs_UAA_APU.pdf), extrait indexé du chapitre 1. Ce sont des guides régionaux, **pas une carte de gouvernements ou réserves de 1776**. Ils aident à distinguer Unangan, Sugpiaq, Yupik, Iñupiat, Dena’ina, intérieur athabaskan et côte tlingit/haïda. Aucun État centralisé unique de ces étendues n'est attesté ici.

Le bitmap regroupe une grande partie des Aléoutiennes dans `xC00000`, y compris de part et d'autre de la coupure du monde. Un seul composant insulaire existant, bbox 270,728–320,762, est séparé : **459 pixels terrestres**, sans retoucher la côte. Sa position dans la chaîne, sa forme et les proxys géographiques permettent une représentation provinciale d'Unalaska ; aucun emplacement archéologique du comptoir n'est certifié. Le port est placé près de la baie, sur un pixel côtier réel. La province reste un **token insulaire de présence**, pas la preuve d'une domination russe exclusive sur tous les habitants de l'île.

Autorisation explicite du joueur : **« Oui, exception maritime pour les îles »**, à la question proposant port et liaison au marché russe à vérifier en jeu. Aucun pont terrestre n'est créé.

## Californie et Arizona

- [California State Parks, Missions of the Californias](https://parks.ca.gov/?page_id=22679), liste datée consultée : San Diego 1769, Carmel 1770, San Antonio 1771, San Gabriel 1771, San Luis Obispo 1772 ; San Francisco et San Juan Capistrano seulement en 1776. Les deux dernières fondations ne sont pas avancées au 1er janvier.
- [NPS, Anza Trail](https://www.nps.gov/articles/bautista.htm) et [sites d’Arizona](https://www.nps.gov/juba/learn/historyculture/arizona-anza-trail-sites.htm), textes consultés : trajet de 1775–1776, San Xavier, départ de Tubac, arrivée en Californie, San Francisco ultérieur. Le franchissement de Yuma est un **passage**, pas une occupation espagnole de toute la zone.
- [NPS, Tubac Presidio](https://www.nps.gov/places/tubac-presidio.htm) et [Tumacácori](https://www.nps.gov/tuma/learn/historyculture/tumacacori-in-summary.htm), passages sur le présidio de 1752 et le déplacement de sa garnison à Tucson en 1776. Tubac reste le siège retenu au départ. La date d'un ordre de transfert ne prouve pas sa réalisation avant le 1er janvier.
- [California Office of Historic Preservation, Native Americans and California Mission System](https://ohp.parks.ca.gov/pages/1054/files/CA_Multiple_Native%20Americans%20and%20CA%20Mission%20System%20MPDF.pdf), tableau indexé consulté, sans lecture intégrale du PDF : populations et missions ne correspondent pas à une occupation apache uniforme de la Californie. Les regroupements nord, vallée centrale et sud restent techniques et hétérogènes.

## Nouveau-Mexique et présidios de Nouvelle-Vizcaye

- [NPS, El Camino Real, appendices](https://www.nps.gov/elca/learn/management/upload/Comprehensive-Management-Plan-Appendixes-E-and-F-508.pdf), passages indexés sur la visite de Domínguez en 1776 : Santa Fe, gouvernement et présidio, pueblos du Rio Grande. Pas de lecture intégrale ou recensement régional extrapolé.
- [INAH Chihuahua, Presidio de Janos](https://www.inahchihuahua.gob.mx/fondopresidio/articulo.pdf), tableau indexé : Janos et Carrizal comptés avant 1776 ; [catalogue de monuments INAH](https://www.inahchihuahua.gob.mx/sections.pl?id=71), notice de Casas Grandes fondée en 1661. Les actes de la [Benson Collection](https://snaccooperative.org/view/63457094) décrivent l'administration du présidio et les conflits apaches. Ces éléments établissent des points, sans donner une frontière continue d'occupation.
- [NPS, contexte historique de Socorro](https://npgallery.nps.gov/GetAsset/cd321866-3954-4639-8ccc-738411298d1e), passage indexé sur l'abandon de 1680. **Socorro n'est pas posé comme ville espagnole réoccupée en 1776** : le point du plan est seulement une étape géométrique du corridor Rio Grande/Jornada. `CORRIDOR_LABEL_CLARIFICATION.json` conserve cette distinction.

## Texas

- [Texas State Historical Association, Spanish Texas](https://www.tshaonline.org/handbook/entries/spanish-texas), texte détaillé renvoyé par recherche : réforme de 1772, noyaux de San Antonio et La Bahía, abandon des missions orientales, Bucareli 1774, Nacogdoches 1779 ; les chiffres tardifs ne servent pas à recalibrer les POPs.
- [TSHA, Bucareli](https://www.tshaonline.org/handbook/entries/bucareli), notice : implantation sur Trinity en septembre 1774, abandon ultérieur. L'emplacement est approximé par province ; aucune occupation de tout l'Est texan n'en est déduite.
- [TSHA, Lipan Apache](https://www.tshaonline.org/handbook/entries/lipan-apache-indians), passages indexés sur les conflits du début des années 1770 ; [dossier historique TxDOT Comanche](https://ftp.dot.state.tx.us/pub/txdot-info/env/toolkit/415-03-rpt.pdf), extraits indexés sur villages et voies de commerce. Lipans, Tonkawas et peuples du littoral ne sont pas remplacés par un territoire comanche uniforme. Le tracé de leurs domaines par cellules reste une approximation régionale ; les sous-groupes côtiers ne sont pas tous individualisés.

## Revendications sur le Pacifique

- [Armada espagnole, expédition Heceta de 1775](https://armada.defensa.gob.es/ArmadaPortal/page/Portal/ArmadaEspannola/cienciaorgano/prefLang-en/02cienciaihcn--10navegaciones--22expbrunoheceta), page consultée : Trinidad, côte du futur Washington, exploration vers 58° N, retour en 1775. [NPS, Heceta et Gray](https://www.nps.gov/articles/000/captain-robert-gray-s-connection-with-the-lewis-and-clark-expedition.htm), extrait sur la revendication espagnole.
- [Archives du Manitoba, glossaire HBCA](https://gov.mb.ca/chc/archives/hbca/glossaries.html), définitions consultées par recherche : charte de 1670 et bassin d'Hudson. La façade pacifique n'est pas assimilée à Rupert's Land.

Washington, Oregon et Colombie-Britannique reçoivent une **revendication nominale côtière espagnole agrégée au State Region**, sans changer leurs propriétaires autochtones. Le claim entier déborde la côte faute de sous-claim provincial : il ne certifie ni une frontière intérieure précise ni une occupation. Les claims tardifs USA/HBC y sont retirés. Les explorations espagnoles du sud de l'Alaska sont attestées mais ne sont pas transformées en claim sur tout l'Alaska, qui bloquerait artificiellement la colonisation de son intérieur. Le découpage de cette revendication côtière reste ouvert.

## Qualité de la localisation et données de population

Le premier ajustement géographique a été écarté : homonymes géographiques et hubs mexicains incohérents. Les fichiers rejetés restent dans `GEOMETRY_REJECTED_V1/`. La version retenue filtre les États/administrations des toponymes : **8 repères FIT, RMS 3,30 pixels ; 14 contrôles locaux, RMS 7,50, maximum 14,80 pixels**. Les gros écarts de certains hubs de Sinaloa restent visibles dans le contrôle global ; ils n'ont pas été corrigés ni utilisés pour dessiner la frontière.

En Alaska, trois repères côtiers ajustent le modèle, un quatrième contrôle indépendant a un écart de 7,76 pixels. Le locator de Fairbanks ne correspond pas à sa province déclarée et est exclu avec preuve. L'extrapolation vers les Aléoutiennes a été contrôlée par la forme et la place de l'île ; il n'y a aucune précision de levé historique.

Les effectifs et identités de cohortes hérités sont conservés. Les familles culturelles disponibles ne décrivent pas finement tous les peuples ; **les anciennes POPs comanches/apaches du Texas et athabaskanes/inuit d'Alaska ne deviennent pas un recensement ethnique exact parce qu'un propriétaire politique a changé**. Tonkawas et peuples côtiers ont notamment des placeholders culturels incompatibles hérités, signalés pour une passe démographique distincte. Aucune conversion silencieuse ni nouvelle inflation de population.
