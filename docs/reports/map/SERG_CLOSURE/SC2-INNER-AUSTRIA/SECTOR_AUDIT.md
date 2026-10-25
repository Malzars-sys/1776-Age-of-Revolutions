# Audit borné de l'Autriche intérieure

Date de référence : **1er janvier 1776**. Trois duchés historiques sous Marie-Thérèse, représentés dans deux régions économiques techniques AUS. Les deux régions ne sont pas deux souverainetés. Aucun pays « Slovénie » de 1776 n'est déduit de STATE_SLOVENIA. La capitale nationale reste Vienne; Graz, Klagenfurt et Ljubljana sont des centres provinciaux.

## IA-ST — Styrie, Haute et Basse

La carte Seutter montre Graz et la Styrie méridionale de Marburg/Pettau et Cilli, avec Hongrie et Croatie voisines. Le jeu regroupe Graz/Haute-Styrie et la Carinthie dans STATE_STYRIA (54), tandis que Maribor et Ptuj sont des locators de STATE_SLOVENIA (114). Tous ces points appartiennent à AUS et au registre impérial actuel. Déplacer une frontière internationale au seul motif de ce regroupement serait artificiel. Les limites internes des duchés et des cercles ne sont pas homologuées cellule par cellule.

## IA-K — Carinthie

Klagenfurt est un locator agricole dans STATE_STYRIA; le vaste RGB occidental xB4D292 et x8F8020 participent à cet agrégat. La carte ancienne identifie la Carinthie et ses interfaces avec Tyrol, Salzbourg, Styrie, Carniole et Frioul. Les domaines de Bamberg ne sont plus à attribuer à BMB en 1776, après la vente de 1759. Les droits salzbourgeois en Carinthie ne constituent pas une souveraineté immédiate indépendante après le récessus de 1535. Ne pas déduire le territoire politique d'un diocèse de Gurk, Lavant ou Salzbourg.

La présence de la Landeshauptmannschaft à Klagenfurt est documentée. Notre bâtiment est régional : un niveau ajouté à STATE_STYRIA n'est pas un second bâtiment situé à Klagenfurt ni la fusion juridique de ses offices avec Graz. La périphérie du Lungau/Salzbourg et les frontières internes restent des approximations de la carte; aucune extension de validation du noyau SLZ.

## IA-C — Carniole

Haute, Basse et Carniole intérieure sont distinguées par la carte et les archives, au sein de la monarchie et de l'Empire. Ljubljana est le centre natif x44F127; Novo Mesto, Maribor et Ptuj n'ont pas tous le même statut historique malgré leur regroupement technique. Le sud de la Carniole ne suit pas les frontières nationales contemporaines. Le fonds administratif de 1763–1782 et les serments contemporains attestent l'office provincial, avant le gubernium de 1783.

Les propriétés de Freising à Škofja Loka et autres biens ecclésiastiques ne suffisent pas à créer une nouvelle souveraineté FSI; leur propriété n'est pas niée. Aucun territoire des noyaux FSI/Brixen/SLZ validés n'est repris ni étendu.

## IA-E/S — Interfaces hongroise, croate et adriatique

Les pays hongrois et croates, y compris leurs administrations militaires, ne deviennent pas impériaux du fait de leurs liens dynastiques ou d'une attribution AUS. Le jeu conserve HUN dans les RGB hongrois voisins x124D73/x30A020/xA709B7 et AUS dans les RGB croates limitrophes x458E4C/x71A041/xF021C0; tous ces voisins restent hors registre impérial. Les douze RGB audités sont déjà bénéficiaires AUS au registre. Les souverainetés vénitiennes voisines sont conservées. Aucun regroupement HUN/AUS n'est effectué.

Gorizia/Gradisca, Trieste, Istrie intérieure habsbourgeoise et Istrie vénitienne sont distinguées de la Carniole dans les sources. Leur attribution fine appartient au futur SC2-ANTERIOR-AUSTRIA; consultation d'interface ici, aucun traitement de cette seconde étape. Ne pas confondre le littoral commercial de 1776 avec la province du XIXe siècle. Ni Frioul vénitien ni toute la Croatie ne sont ajoutés à l'Empire.

## IA-D/E/U — Population, économie et armées

Inventaire initial : STATE_STYRIA **599 143** habitants, STATE_SLOVENIA **395 031**, ensemble **994 174**. Ces pools hérités traversent les limites internes des duchés; ce ne sont pas des recensements des trois duchés. Le repère de 509 420 de la série officielle de Styrie pour 1770 n'a pas le même périmètre démontré. Faute de répartition défendable des districts entre les deux agrégats, aucun nouveau chiffre, culture, religion ou profession n'est imposé. La comparabilité démographique reste une limite explicite, sans certification nouvelle des effectifs.

Les mines de fer, forêts, routes et centres de commerce déjà déclarés sont conservés. Les répétitions base/overlay sont des déclarations, pas des niveaux moteur à additionner. Aucun effectif militaire, caserne, flotte ni recrutement n'est ajouté; les unités et formations initiales restent identiques : deux conscrits dans STATE_STYRIA, un dans STATE_SLOVENIA, aucun nouveau permanent.

**IA-E-C — incohérence côtière corrigée après le premier contrôle administratif.** Le contrôle détaillé relève un port de trois niveaux et un chantier naval d'un niveau dans chacune des deux déclarations initiales de STATE_SLOVENIA. Or cet agrégat est intérieur : ni locator de port ni naval_exit_id, et ses quatre RGB ne touchent aucune province maritime. Les définitions effectives du mod comme du vanilla exigent is_coastal = yes pour ces deux types. Les cartes historiques distinguent la Carniole intérieure des juridictions littorales; aucun transport fluvial ne justifie ici un bâtiment maritime côtier du moteur.

Retrait des **quatre seuls blocs create_building concernés**, dans 01_south_europe.txt et 98_build_start_1776_world_redistribution.txt. Cela retire six niveaux de port et deux de chantier **écrits**, sans prétendre qu'ils étaient tous cumulés ou fonctionnels en jeu. Les centres de commerce et les routes ne changent pas. Aucun port voisin n'est déplacé, supprimé ni ajouté; leur éventuelle réorganisation appartient à une mission adriatique future. Les fichiers courants sont lus juste avant édition; une garde d'empreinte et une comparaison intégrale bornent l'édition aux quatre blocs. Les autres octets sont conservés, sans réécriture depuis une ancienne baseline. Les premiers résultats avant cette correction sont archivés sous BEFORE_MARITIME_*; les contrôles sont ensuite rejoués.

## IA-I-ST et IA-I-C — Deux corrections indépendantes

L'inventaire effectif ne contient **aucune administration publique** dans l'une ou l'autre région. Deux fichiers nouveaux, chacun autonome, ajoutent **un seul niveau public AUS** : l'un dans STATE_STYRIA, l'autre dans STATE_SLOVENIA. Le premier abstrait la capacité provinciale de Graz et l'agrégat carinthien; le second représente la capacité de Carniole dans l'agrégat de Ljubljana. Aucun troisième niveau n'est empilé artificiellement pour reproduire chaque office.

Les quatre PM nationaux déjà utilisés en Moravie sont conservés : organisation simple, bureaucrates héréditaires, administration religieuse, absence de rapports organisés de recherche. Ils respectent les lois/technologies actuelles; le PM professionnel est incompatible avec law_crownland_diets. « Héréditaire » et « religieux » sont ici les abstractions nationales du jeu, pas une assertion sur le recrutement effectif du gubernium. Pas de réforme nationale destinée à contourner cette contrainte.

Catégorie **B administrative et politique**, sans prétention de cadastre, d'effectifs de fonctionnaires ni de fusion provinciale. Aucun changement de propriétaire territorial, RGB, State_ID, géométrie, registre, capitale, souveraine ou gouvernement. Les trois sous-lots IA-I-ST, IA-I-C et IA-E-C se contrôlent indépendamment. Cette installation requiert le test du joueur; elle ne clôt pas automatiquement le lot ni les incertitudes démographiques et périphériques.
