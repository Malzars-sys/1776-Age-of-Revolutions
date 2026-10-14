# Révision historique du recrutement régional — 11 octobre 2026

## Résultat et limites

Les 882 400 habitants du calibrage économique précédent ont été retirés, et eux seuls. Tous les groupes antérieurs sont conservés exactement : effectifs, cultures, religions déclarées et statuts libres/esclaves. Cela **ne certifie pas historiquement les populations d'origine** : Åland, les Bermudes, le Nouveau-Brunswick et surtout la Jamaïque restent problématiques. Corriger ces bases exige une décision distincte sur les groupes historiques conservés ; leur réduction ou leur déplacement ne peut pas être maquillé en migration attestée.

Les bâtiments et routes disproportionnés sont révisés. Dix niveaux d'administration américains sont relocalisés ; quatorze niveaux théoriques sont retirés. Les trente unités suédoises et treize unités britanniques précédemment recrutées sur les îles sont recrutées sur le continent, conformément à l'autorisation donnée pendant cette révision. Le nombre, les types, les formations et les conscrits nationaux ne changent pas. Aucun recrutement chinois ou espagnol n'est déplacé sans arbitrage supplémentaire.

Cette révision est appliquée aux historiques. Les tests sont **statiques**, confrontés à la sauvegarde **observateur_3 au 1er février 1776, antérieure aux ajouts démographiques**. Aucun résultat économique après cette révision n'a encore été observé dans le jeu. Ni un recrutement à 80 %, ni un accès au marché à 100 % ne sont garantis.

## Instantané préalable, intégrité et restauration

`PRE_REVISION_FULL_MOD.zip` contient les **5 524 fichiers du mod**, y compris sources, assets et rapports existants, avant les modifications de gameplay de cette révision. Taille : **956 169 340 octets**. Exclusions explicites : base Git, cache dérivé `.asset-cache`, caches Python et ce nouveau dossier de rapport ; aucun fichier source ou asset nécessaire au mod n'est exclu.

SHA-256 de l'archive :

`c1a8e5947bfd6e4fe7d1517f938b84d662b1be0e7ee4673b29d55db9514bc7bf`

`SNAPSHOT_MANIFEST.json` conserve les empreintes et tailles individuelles, le HEAD, la branche et l'état Git initial. La liste des membres et les CRC de l'archive ont été vérifiés. `BASELINE.json` conserve également les textes des historiques et l'inventaire avant révision. Pour comparer ou restaurer, extraire l'archive **dans un dossier séparé**, puis comparer les seuls fichiers concernés : ne pas écraser le travail local courant en bloc.

Le précédent rapport et ses fichiers de calcul ne sont pas réécrits : ils restent la trace du calibrage économique rejeté. Population mondiale déclarée : **836 687 380 → 835 804 980**.

## Bilan des dix régions

« Avant » signifie avant les ajouts économiques ; « calibré » signifie avec ces ajouts ; « révisé » est le nouvel historique. Les repères historiques ne sont pas tous des recensements complets du périmètre RGB actuel.

| Région / propriétaire | Avant | Calibré | Révisé | Repère historique le plus utile | Appréciation |
|---|---:|---:|---:|---|---|
| District de Columbia / USA | 5 000 | 197 600 | 5 000 | District fédéral créé en 1790 ; aucune population d'un « district fédéral » en 1776 | Retrait certain de l'ajout ; total rural du périmètre actuel non établi |
| Åland / SWE | 14 347 | 114 847 | 14 347 | Environ 9 000 en 1750 ; ordre de grandeur de 10 000 au XVIIIe siècle | Base encore élevée, conservée pour préserver les groupes antérieurs |
| Géorgie / USA | 42 993 | 152 193 | 42 993 | 40–50 000 vers la Révolution ; estimation Census de 50 000 en 1776 | Base compatible avec cet ordre de grandeur ; comparer séparément les Autochtones |
| Bermudes / GBR | 19 584 | 79 284 | 19 584 | 10 381 en 1783 dans une transcription du retour de population | Base elle-même excessive ; retour original non consulté directement |
| Nouveau-Brunswick / NVS | 20 000 | 80 400 | 20 000 | Au plus 5 000 non-Autochtones avant l'arrivée loyaliste en 1783 | Base et composition déjà discutables ; pas d'importation anticipée des Loyalistes |
| Antilles espagnoles : Margarita / SPA | 14 000 | 173 600 | 14 000 | Environ 14 000 en 1771 ; 14 968 en 1773 ; environ 12 000 en 1775 | Base plausible à cette échelle ; aucun ajout de 159 600 Espagnols |
| Jamaïque / GBR | 520 000 | 536 200 | 520 000 | Environ 210 000 en 1775 ; transcription de 209 617 | Grave anomalie antérieure de total et de statut social, laissée explicite |
| Floride britannique / GBR | 30 957 | 120 057 | 30 957 | Environ 3 000–3 600 en Floride orientale au début de la Révolution, selon périmètre | Ni toute la Floride moderne, ni toutes les populations autochtones : base non certifiée |
| Alxa / CHI | 44 788 | 106 388 | 44 788 | Aucun total régional proche de 1776 suffisamment établi dans les sources retrouvées | UNRESOLVED ; identité de bannière mongole documentée, croissance mandchoue non étayée |
| Amour / CHI | 82 613 | 116 113 | 82 613 | Enregistrement du district d'Aigun : 6 953 personnes en 1771, 7 493 en 1780 | Catégorie administrative partielle, **pas** la population totale du STATE_AMUR ; UNRESOLVED |

### 1. District de Columbia

Le territoire rural représenté par la province moderne n'est pas supprimé ; les 1 133 Yankees, 3 545 Dixies et 322 Afro-Américains esclaves sont conservés. Aucun recensement comparable de tout ce périmètre en 1776 n'a été trouvé : les petits chiffres concernant la ville future ne doivent pas être appliqués mécaniquement à la région entière.

La capitale initiale américaine passe en **Pennsylvanie**, proxy de Philadelphie, où siégeait le Congrès au 1er janvier 1776. Le bâtiment initial du Capitole conditionné au DLC est retiré ; le déclencheur DLC reste intact. Les 19 niveaux d'administration de Washington disparaissent : un est transféré à New York, quatre en Pennsylvanie, quatorze sont retirés comme capacité fédérale surdimensionnée. Les routes passent de 7 à 1 niveau : 1 000 postes, dont 100 employés qualifiés, au lieu de 7 000 postes.

Le déficit relevé n'était donc pas la preuve qu'il manquait 192 600 habitants historiques : il résultait surtout du choix de capitale et de 28 500 postes administratifs théoriques face à une petite population rurale. Les niveaux transférés sont un compromis de jeu, pas un inventaire d'offices réels en 1776.

Sources : [Office of the Historian, premiers bâtiments et sièges du Congrès](https://history.state.gov/departmenthistory/buildings/section1) ; [National Park Service, naissance de Washington](https://www.nps.gov/articles/the-octagon-of-washington-d-c-the-house-that-helped-build-a-capital-teaching-with-historic-places.htm).

### 2. Åland

Les 13 708 Suédois et 639 Finlandais d'origine restent en place. Les 100 500 personnes ajoutées sont retirées. La recherche démographique rapporte environ 9 000 habitants en 1750 ; l'organisme statistique ålandais situe la population du milieu du XVIIIe siècle autour de 10 000. Ce ne sont pas des justifications de la base de 14 347, encore moins de 114 847.

Les 30 unités permanentes sont recrutées en Svealand (20) et Götaland (10), avec les mêmes armes et la même formation. Le grand ensemble fortifié de Bomarsund appartient au XIXe siècle, et ne justifie pas une concentration de 30 000 recrues à Åland en 1776. Les routes insulaires passent de 3 à 1 ; le port et la pêche sont conservés. La pêche peut rester partiellement employée : la remplir entièrement n'est pas un objectif. Une redistribution des 4 000 habitants « excédentaires » de la base serait un déplacement fictif sans preuve de mauvais périmètre ; elle n'est pas appliquée.

Sources : [ÅSUB, perspective historique de la population](https://www.asub.ax/sv/statistik/befolkningen-2023) ; [Demographic Patterns in the Åland Islands, Finland, 1987](https://journal.fi/fypr/article/download/44820/48317) ; [Ålands Museum, caserne du fort principal](https://www.museum.ax/vara-museer-och-sevardheter/bomarsunds-fastningsruin/sevardheter/huvudfastet).

### 3. Géorgie

L'estimation officielle de 50 000 habitants en 1776, et la fourchette de 40–50 000 rapportée par l'étude historique géorgienne, rendent inutile l'ajout de 109 200 personnes. Les 18 399 esclaves, 643 Cherokees, 189 Afro-Américains libres et groupes Dixie sont préservés. La statistique coloniale peut exclure des Autochtones : ces groupes ne sont pas retranchés pour faire artificiellement coïncider les totaux.

L'administration passe de 6 à 1 : deux niveaux vont au Maryland et trois en Pennsylvanie. Les routes passent de 4 à 2 (2 000 postes). Cela libère la contrainte des administrations sans exiger le plein emploi de tous les domaines agricoles. Aucune migration depuis les Carolines n'est ajoutée : leur proximité ne démontre pas un déficit démographique historique de la Géorgie.

Sources : [US Census, populations des treize colonies](https://www.census.gov/content/dam/Census/newsroom/facts-for-features/2017/cb17-ff10-july4-graphic.pdf) ; [Digital Library of Georgia, The Revolutionary background in Georgia](https://dlg.usg.edu/record/dlg_ggpd_s-ga-bs730-b-pm1-b1974-br4).

### 4. Bermudes

Les 59 700 personnes ajoutées sont retirées. La base préexistante contient 10 690 Britanniques et 8 894 Afro-Caribéens, tous déclarés libres. La transcription du recensement de 1783 distingue 5 462 personnes blanches et 4 919 personnes de couleur, pour 10 381 au total ; « personnes de couleur » n'est pas synonyme d'« esclaves ». Le document original identifié aux National Archives n'a pas été accessible dans cette consultation : ce chiffre est donc un repère secondaire, pas un recensement original vérifié ligne à ligne.

Les 13 unités permanentes écrites sont recrutées dans les Home Counties. La sauvegarde avait déjà 15 niveaux de casernes : les 13 unités de départ et les 15 niveaux après simulation ne sont pas confondus. Les routes passent de 3 à 1. Le port, le chantier commercial et les petits services navals sont conservés : l'ouverture du grand Royal Naval Dockyard en 1809 ne prouve pas l'absence de construction navale commerciale en 1776.

La population d'origine et ses statuts restent des points d'audit ; aucune conversion automatique de libres en esclaves ni migration inventée depuis la Grande-Bretagne.

Sources : [transcription des dénombrements historiques](https://en.wikipedia.org/wiki/Demographics_of_Bermuda#Historical_census_statistics) ; [référence du retour du 7 octobre 1783, National Archives](https://discovery.nationalarchives.gov.uk/details/r/C9163919) ; [chronologie du Royal Naval Dockyard](https://dockyard.bm/dockyard/visit/our-history/).

### 5. Nouveau-Brunswick

Les 60 400 ajouts sont retirés ; les 19 502 Anglo-Canadiens, 332 Afro-Américains et 166 Algonquiens préexistants restent intacts. L'étude de l'Université du Nouveau-Brunswick estime à au plus 5 000 les habitants **non autochtones** en 1783 avant les Loyalistes. Cette borne ne mesure pas toute la population autochtone, et n'autorise pas la suppression de celle-ci. Les arrivées loyalistes des années 1780 ne sont pas anticipées en 1776.

Le tag NVS ne possède actuellement que cet État : une relocalisation arbitraire de son administration dans un État britannique changerait de pays au lieu de simplement déplacer un bâtiment. L'unique administration et les deux niveaux de routes sont conservés. L'emploi observé des routes n'était que de 0,927 niveau sur 2 ; avec une garnison de 3 000 et les emplois civils déjà occupés, le plein recrutement des deux niveaux ne passe pas le budget de main-d'œuvre. Le petit déficit est accepté, sans construire davantage ni importer 60 400 habitants. Le chantier et la pêche ne doivent pas obligatoirement atteindre leur emploi théorique maximal.

Sources : [UNB, chapitre 3, population pré-loyaliste et limites des statistiques](https://educationhistory.lib.unb.ca/book/chapter-3) ; [Gouvernement du Nouveau-Brunswick, histoire provinciale](https://www.gnb.ca/en/admin/about-nb/history.html).

### 6. Antilles espagnoles : Margarita

Le périmètre SPA de `STATE_WEST_INDIES` concerne `xF07001`, associé dans les historiques à Nueva Esparta/Margarita ; ce n'est **pas Porto Rico**, qui possède son propre État. Le plan territorial historique de Nueva Esparta rapporte environ 14 000 personnes en 1771, 14 968 en 1773 et environ 12 000 en 1775, avec limites de recensement. Les 14 000 préexistants sont donc un ordre de grandeur défendable, contrairement à l'ajout de 159 600 Espagnols continentaux.

Les 12 327 `north_andean` (proxy imparfait), 944 Afro-Caribéens libres et 729 esclaves restent intacts. La source décrit des Guaiquerí ; leur représentation culturelle est imparfaite et n'est pas effacée par une prétendue immigration espagnole. Les trois administrations navales sont déplacées en Basse-Andalousie, région de Cadix/La Carraca : 9 → 12 niveaux. Les routes passent de 4 à 3. La garnison espagnole demeure une contrainte majeure : le déficit peut persister même avec moins d'emplois navals. La restructuration de cette garnison n'est pas implicitement étendue depuis l'autorisation concernant les Bermudes et Åland.

Sources : [Plan de ordenación del territorio del Estado Nueva Esparta, 1987, section Población, page PDF 43](https://bibliotecadigitalne.org/wp-content/uploads/2024/05/Plan-Ordenacion-del-Territorio-Estado-Nueva-Esparta.-Evolucion-Historica.-Patrimonio-arquitectonico-ambiental_C.-Caraballo-J.-Moreno-MARNR-1987.pdf) ; [Armada espagnole, arsenal de Cadix et installations du XVIIIe siècle](https://armada.defensa.gob.es/ArmadaPortal/page/Portal/ArmadaEspannola/conocenosorganizacion/prefLang-es/04Apoyofuerza--02jal--05Arsenales--01arsenalcadiz).

### 7. Jamaïque

Les 16 200 employés britanniques ajoutés sont retirés. La transcription historique donne 209 617 habitants en 1775, dont 192 787 esclaves ; d'autres reprises présentent une différence de mille personnes dans le nombre de Blancs. Retenir **environ 210 000**, pas une fausse précision unanimement établie. La base du mod, 488 604 Afro-Caribéens libres et 31 396 Britanniques, est bien supérieure et socialement incohérente pour 1776. Ces groupes ne sont ni supprimés ni réasservis pendant cette correction ciblée.

Dans observateur_3, la main-d'œuvre libre est de 152 109, mais seulement 61 travailleurs de type employé sont pleinement acceptés. Le chiffre de 4 665 du précédent rapport était une capacité de postes d'employés, **pas** 4 665 personnes déjà qualifiées. Le manque de candidats acceptés/qualifiés est distinct du total d'habitants.

Les quatre niveaux historiques de routes et leur PM à péage sans canal sont maintenus (4 000 postes, 600 employés et 400 bureaucrates). L'IA avait activé les canaux industriels dans la sauvegarde, portant cette capacité à 7 200 postes et 1 000 employés. Les pénuries, qualifications, salaires et choix de PM doivent être suivis après redémarrage. Aucune baisse globale des qualifications ou nouveau bonus provincial arbitraire n'est ajouté ; le correctif IA antérieur est préservé. Le déficit peut donc rester présent.

Source : [Jamaican Family Search, chronologie et population de 1775](https://www.jamaicanfamilysearch.com/Samples/Hisback.htm).

### 8. Floride

Les 89 100 ajouts sont retirés. Les travaux universitaires donnent environ 3 000 à 3 600 habitants pour la **Floride orientale** au commencement de la Révolution, selon inclusion des Minorquins, de certains groupes et des militaires. La Floride occidentale avait un autre périmètre, débordant largement la Floride moderne. Ces chiffres ne doivent pas être additionnés sans correspondance territoriale, ni servir à supprimer les populations autochtones ou les 22 450 esclaves présents dans l'historique britannique. Les 7 200 Muskogeans de la partie SML sont également inchangés.

Deux niveaux de carrière de calcaire, soit une capacité théorique de 10 000 emplois, sont déplacés au Lancashire (1 → 3, potentiel régional de 48). Le niveau représente une capacité abstraite : il ne s'agit pas de prétendre qu'un chantier floridien réel et ses ouvriers ont migré en 1776. L'exploitation de calcaire et la production de chaux au XVIIIe siècle sont documentées dans la région anglaise. Les propriétaires sont relocalisés avec les commandes auto-localisées de carrière, sans nouveau pays propriétaire. Les méthodes de production restent identiques. Les routes passent de 7 à 2.

La main-d'œuvre libre observée de 3 248 suffit difficilement à toutes les activités conservées ; les deux routes seules demandent 2 000 postes. Un recrutement partiel de certaines activités, voire un déficit temporaire, reste admissible. Pas de déplacement arbitraire des populations autochtones de Géorgie ou d'immigrants loyalistes arrivés plus tard.

Sources : [R. Smith, University of Florida, 2008, p. 85, estimation et périmètre de la Floride orientale](https://ufdcimages.uflib.ufl.edu/uf/e0/02/24/30/00001/smith_r.pdf) ; [National Park Service, période britannique](https://www.nps.gov/casa/learn/historyculture/the-british-period.htm) ; [Archaeology Data Service, carrière et four à chaux ancien de Coniston, Lancashire historique](https://archaeologydataservice.ac.uk/data-catalogue/resource/0cf4b431ef61c828c5a07fd71b673223d9df979ef188843f0afd4d0fa9553600).

### 9. Alxa

Aucun recensement régional complet assez proche de 1776 n'a été établi à partir des ressources accessibles. Les archives de bannière et la chronologie officielle documentent en revanche un territoire khoshut/mongol, sa création administrative en 1697 et son centre de Dingyuanying depuis 1730. Elles ne justifient pas l'ajout de 61 600 Mandchous.

Les 42 992 Mongols, 196 Mandchous et 1 600 Han d'origine restent en place. Le chiffre de 44 788 est donc conservé provisoirement, **pas historiquement vérifié**. Une redistribution depuis le Shanxi ou une autre bannière sans dénombrement comparable ne serait pas une correction historique démontrée.

Les routes passent de 5 à 2 : leur emploi théorique est ramené de 5 000 à 2 000. Dans la sauvegarde, les casernes occupaient l'équivalent de 13 368 postes et les routes seulement deux postes, sur une main-d'œuvre libre de 13 413. Le problème demeure une répartition militaire/civile et des qualifications, pas une preuve de population historiquement manquante. La pénurie d'infrastructure peut rester acceptée. Il faut des listes de bannière avec ménages, catégories et périmètre, pas un coefficient uniforme habitants/emplois.

Sources : [chronologie de la bannière d'Alxa, gazetteer officiel de Mongolie intérieure](https://nmgqq.com.cn/quqinggailan/jianzhiyange/alsm/2020-11-16/20026.html) ; [édition des archives historiques de la bannière, National Library of China Publishing](https://www.nlcpress.com/ProductView.aspx?Id=7101).

### 10. Amour

La gazetteer Qing enregistre 6 953 personnes dans la rubrique du district de Heilongjiang/Aigun en 1771 et 7 493 en 1780. Ces enregistrements administratifs ne recensent pas automatiquement toutes les bannières, les communautés autochtones et la rive nord représentées par le STATE_AMUR. Les chiffres provinciaux de **Jilin** ne sont pas ceux d'Amour/Heilongjiang ; ils ne sont pas substitués à ce périmètre.

Les 33 500 ajouts mandchous sont retirés. Les 81 123 `siberian`, 1 040 Mandchous et 450 Russes antérieurs sont préservés ; `siberian` reste un proxy grossier de peuples différents, pas une catégorie historique exhaustive. Aucun déplacement depuis Shengjing/Jilin n'est pratiqué sans preuve de répartition. Le total historique de toute la région reste UNRESOLVED.

Les 3 niveaux de routes sont maintenus. La garnison occupait presque toute la main-d'œuvre libre observée : 24 798 postes sur 24 798. Ajouter des routes ne recruterait pas magiquement leurs ouvriers. Un déficit durable est donc possible et accepté, en attendant une révision distincte du recrutement militaire frontalier.

Source : [Qinding Shengjing Tongzhi, volume 36, registres de population et district de Heilongjiang](https://zh.wikisource.org/zh-hans/欽定盛京通志_(四庫全書本)/卷036).

## Relocalisations et contrôle des destinations

Les administrations américaines sont redistribuées vers des colonies plus peuplées, mais ne sont pas toutes recréées : cela aurait transféré le surdimensionnement. Les estimations Census proches de la Révolution indiquent environ 190 000 habitants à New York, 302 000 en Pennsylvanie et 200 000 au Maryland. Les niveaux exacts suivants demeurent un compromis de capacité dans le jeu.

| Déplacement | Nouvelle capacité au destinataire | Routes avant → après |
|---|---|---|
| Washington → New York : 1 administration | Administration 9 → 10 | 6 → 5 |
| Washington → Pennsylvanie : 4 administrations | Avec les 3 de Géorgie : administration 7 → 14 | 10 → 7 |
| Géorgie → Maryland : 2 administrations | Administration 6 → 8 | 4 → 5 |
| Géorgie → Pennsylvanie : 3 administrations | Inclus dans les 14 ci-dessus | Inclus ci-dessus |
| Floride → Lancashire : 2 carrières | Calcaire 1 → 3 | 19 inchangés |
| Margarita → Basse-Andalousie : 3 administrations navales | Administration navale 9 → 12 | 8 inchangés |
| Åland → Svealand : 20 unités permanentes | Même formation et types | 6 → 9 |
| Åland → Götaland : 10 unités permanentes | Même formation et types | 4 inchangés |
| Bermudes → Home Counties : 13 unités permanentes | Même formation, types et destination stratégique | 16 inchangés |

Les infrastructures des régions modifiées passent au total de **59 à 38 niveaux**, soit **21 niveaux de moins**, en comptant les niveaux effectifs ciblés une seule fois, pas les commandes dupliquées dans les couches d'historique. Les doublons existants des seules commandes ciblées sont alignés pour éviter qu'un fichier tardif rétablisse les anciens niveaux. Les 14 administrations américaines retirées représentent 21 000 postes théoriques, et les 21 niveaux de routes retirés net représentent 21 000 autres postes. Ce sont des capacités, pas 42 000 emplois réellement occupés supprimés.

### Scénario conditionnel des destinataires

Calcul reproductible dans `REVISION_MEASURES.json` : conserver la capacité non routière observée, utiliser les PM historiques des routes avec 80 % d'emploi, appliquer une consommation prudente des bâtiments, et ne pas compter sur les bonus futurs de la nouvelle capitale. Pour le budget de main-d'œuvre, conserver les autres emplois observés et remplir les nouvelles fonctions publiques, recrues et routes ; ne compter les esclaves que là où ils étaient effectivement employés en agriculture, jamais dans les administrations ou les routes.

| Destination | Réserve d'infrastructure dans ce scénario | Postes libres projetés / main-d'œuvre libre observée |
|---|---:|---:|
| New York | +8,20 | 58 066 / 58 592 |
| Pennsylvanie | +5,80 | 86 821 / 87 651 |
| Maryland | +3,90 | 55 090 / 56 143 |
| Home Counties | +30,08 | 402 769 / 407 130 |
| Lancashire | +19,00 | 239 662 / 311 354 |
| Basse-Andalousie | +4,60 | 103 438 / 312 638 |
| Svealand | +3,05 | 99 446 / 299 307 |
| Götaland | +2,10 | 77 783 / 217 512 |

Ces contrôles éliminent un déficit **de capacité** au destinataire dans le scénario. Ils ne garantissent pas la formation des employés, la solvabilité, le remplissage instantané ni la réaction de l'IA. Les marges humaines américaines sont étroites : un déplacement des emplois privés vers les fonctions publiques peut rester nécessaire, sans prétendre remplir tous les nouveaux emplois urbains théoriques.

Les premières répartitions envisagées ont été rejetées : New York 16 administrations/Pennsylvanie 19 aurait dépassé les budgets d'emploi observés ; le transfert des cinq niveaux géorgiens au seul Maryland aussi. Les calculs ont été resserrés avec les esclaves **réellement employés** en agriculture, et non toute la population esclave potentiellement disponible. Ce sont des précautions, pas des tests en jeu réussis.

## Déficits acceptés et prochaine mesure en jeu

| Région | Solde réellement observé dans observateur_3, avant toute révision | Risque accepté après révision |
|---|---:|---|
| Nouveau-Brunswick | −0,519 | Garnison, administration et routes se disputent la petite main-d'œuvre ; pas d'ajout de population ni d'État donneur artificiel |
| Jamaïque | −2,60626 | Qualification/acceptation et choix IA de canaux ; pas de nouvelle immigration de clerks |
| Margarita | −5,30306 | Garnison disproportionnée et routes partiellement recrutées ; administration navale relocalisée seulement |
| Alxa | −1,897 | Routes sans employés, presque toute la main-d'œuvre dans les casernes |
| Amour | −3,75 | Main-d'œuvre absorbée par les casernes ; aucune preuve justifiant plus de Mandchous |
| Floride | −0,18809 | Faible main-d'œuvre civile libre ; les carrières déplacées réduisent la demande mais les qualifications et l'emploi restent à mesurer |

Les nombres ci-dessus ne sont **pas** des déficits post-correctif prédits. Les scénarios de capacité positifs pour certains de ces États ne sont pas retenus comme succès lorsqu'ils supposent des routes recrutées sans budget de main-d'œuvre suffisant.

Test à effectuer dans une nouvelle partie : relever au 1er janvier puis au 1er février la population, les niveaux effectifs, les PM, l'emploi et les pénuries des routes/administrations, l'infrastructure utilisée/disponible, l'accès au marché et la bureaucratie. Vérifier spécialement New York, Pennsylvanie, Maryland et Home Counties. Une sauvegarde ancienne contient les bâtiments et populations déjà créés : la recharger ne teste pas les nouveaux historiques.

## Validation et fichiers modifiés

`VALIDATION.json` : comparaison exacte des populations avec l'état antérieur au calibrage ; comparaison des propriétaires RGB, géométries, États, statuts et références avec l'instantané de cette révision ; conservation des unités par pays/formation/type/service ; comparaison des commandes de bâtiments hors liste autorisée ; empreintes de tous les autres fichiers du mod. L'unique définition de pays modifiée est la capitale USA. Les autres pays, sujets, diplomatie, technologies, PM, réformes ottomanes, correctifs IA et rapports MAP-2A/MAP-2B restent inchangés.

Les validations disponibles des infrastructures et des journaux ottomans sont exécutées ; leur résultat est conservé dans `VALIDATION.json`. Les anciens validateurs MAP-2 qui imposaient la conservation de tous les niveaux de bâtiments ne sont pas présentés comme applicables à ce nouveau mandat : leurs invariants territoriaux sont repris et contrôlés ici.

Le contrôle des destinataires vérifie huit régions, leur réserve conditionnelle d'infrastructure et leur budget d'emplois occupés. Aucun nouvel espace de fin de ligne n'est introduit par cette révision. Le contrôle Git global signale encore des espaces préexistants dans les modifications MAP et d'autres historiques : ils sont conservés plutôt que de reformater les travaux antérieurs.

Treize fichiers de gameplay concernés :

- Populations : `common/history/pops/05_north_america.txt`, `06_central_america.txt`, `11_east_asia.txt`, `14_siberia.txt`, `15_russia.txt`.
- Bâtiments : `common/history/buildings/00_west_europe.txt`, `01_south_europe.txt`, `05_north_america.txt`, `06_central_america.txt`, `98_build_start_1776_world_redistribution.txt`, `98b_build_start_1776_british_market_correction.txt`.
- Recrutement : `common/history/military_formations/00_military_formations_europe.txt`.
- Capitale : `common/country_definitions/00_countries.txt`, seul champ `USA.capital`.

Nouveau support reproductible : `tools/historical_workforce_revision.py`. Aucun commit, merge, push ou changement de branche n'est effectué.
