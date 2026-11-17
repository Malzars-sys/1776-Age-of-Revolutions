# Cas sans correspondance vanilla suffisante — décisions proposées

Référence : **1er janvier 1776**. Ce document propose des solutions ; **aucune nouvelle loi, variante, catégorie ou technologie n'est installée par ces propositions**. Les quatre degrés mentionnés dans la demande sont conservés, bien que celle-ci les annonce comme « trois choix ».

| Degré | Intervention | Ce que cela permet / ne permet pas |
|---|---|---|
| Petit | Amendement d'une loi existante | Ajuster certains effets et donner un nom au compromis. Ne change pas, à lui seul, la catégorie, le prérequis technologique de la loi mère ou le mode de succession. |
| Moyen | Variante de loi | Garder une parenté idéologique tout en définissant nom, conditions, effets et visibilité propres. Les sélecteurs de gouvernement et les conditions `has_law` exactes doivent être contrôlés. |
| Gros | Nouvelle loi dans un groupe existant | Créer une option autonome de citoyenneté, gouvernance ou économie, avec opinions, transitions et choix IA explicites. Elle remplace les autres lois de ce groupe. |
| Énorme | Nouveau groupe de lois | Ajouter un axe politique indépendant. Demande une initialisation mondiale, des positions idéologiques, interface, IA, effets, migrations et contrôles. À réserver à un besoin qui traverse réellement plusieurs lois. |

## A. Espagne : allégeance monarchique et uniformisation bourbonienne

**Constat historique.** La cédule de 1768 prescrit le castillan dans l'enseignement et les juridictions. Cette politique précède 1776 et rend insuffisante la description vanilla d'une sujétion peu soucieuse d'identité officielle. Elle ne prouve pas que les populations sont déjà homogènes : la même source documente les revendications régionales. Les régimes foraux empêchent aussi une lecture d'uniformisation juridique complète [S03–S04].

**Constat technique.** SPA demande `law_national_supremacy`, sans `nationalism`. Sa culture primaire reste `spanish`. `law_official_nationality` est une variante russe de `law_subjecthood`, visible pour RUS, dont les textes et bonus font référence à la russification. Son absence de gate technologique ne la rend pas générique. L'emprunter telle quelle à l'Espagne serait une nouvelle erreur ; sa doctrine de référence est rattachée au XIXe siècle [S05].

| Choix | Proposition espagnole | Limite / travail associé |
|---|---|---|
| Amendement | Sujétion + **Uniformisation bourbonienne** : renforcer l'assimilation et favoriser la langue administrative dominante. | Conserve le descriptif et la structure de la loi mère ; ne représente pas finement les droits foraux. |
| Variante — **recommandée** | **Sujétion bourbonienne** : allégeance au souverain, uniformisation administrative castillane, assimilation accrue mais limitée ; périmètre espagnol de départ. | Rédiger FR/EN, contrôler les cultures réellement présentes et les échelons d'acceptation. Les valeurs restent à choisir ; ne pas assimiler politique prescrite et résultat accompli. |
| Nouvelle loi | **Uniformité dynastique**, dans Citoyenneté, distinguée de la citoyenneté nationaliste. | Intéressant pour plusieurs monarchies, mais exige d'étudier chacune avant extension. |
| Nouveau groupe | **Langue de l'administration**, séparé de la citoyenneté : pluralité, langue privilégiée, uniformisation obligatoire. | Solution la plus précise à long terme, mais trop large pour ce lot ; initialisation de tous les pays nécessaire. |

**Décision de cette passe :** Espagne inchangée, anomalie de gate conservée et signalée. Aucun nationalisme offert pour masquer le problème. La discussion fournie par le joueur est conservée dans `USER_SPANISH_DISCUSSION.png` ; elle a orienté la vérification, sans servir de preuve historique.

## B. Grande-Bretagne et France : économie d'Ancien Régime

`law_agrarianism` dépend ici de `romanticism` (ère 7). Le signalement technique est fondé, mais la primauté historique de l'agriculture ne dépend pas du romantisme. La France connaît déjà des politiques proches des physiocrates avant janvier 1776 ; la Grande-Bretagne conserve des institutions commerciales et des privilèges que le seul nom « agrarianisme » décrit mal [S06–S07]. « Traditionalisme » vanilla suppose peu de contrôle central ; l'interventionnisme est décrit comme une correction des excès d'entreprises privées. Aucune de ces étiquettes ne restitue exactement l'ensemble.

| Choix | Grande-Bretagne | France |
|---|---|---|
| Amendement | Agrarianisme + **Manufactures et privilèges commerciaux**. | Agrarianisme + **Réformes de Turgot**. |
| Variante — **recommandée** | **Économie de privilèges et manufactures**, avec un accès initial historiquement justifié, sans romantisme. | **Économie agraire réformatrice**, distinguant la structure du royaume et les réformes ministérielles. |
| Nouvelle loi | **Économie de privilèges**, dans Système économique, compatible avec une politique commerciale séparée. | Même famille, avec transitions vers des systèmes économiques ultérieurs ; ne pas fusionner économie et commerce. |
| Nouveau groupe | **Organisation de la production** : corporations, privilèges, libre établissement, séparé de l'investissement. | Permet de représenter les réformes corporatives sans remplacer tout le système économique. |

L'amendement seul **ne résout pas le gate de romantisme**. Sa correction demanderait une décision distincte sur la loi mère et tous ses consommateurs. Aucune réforme française de février–mai 1776 n'est supposée déjà réalisée au départ. Lois économiques maintenues en attente, sans grant de romantisme ou de technologies futures.

## C. Autriche et Prusse : agriculture, caméralisme et manufactures

Les **dernières demandes** sont l'agrarianisme dans les deux pays : un effet appliqué après une première ligne d'interventionnisme explique l'apparence contradictoire du fichier. Le caméralisme et la politique de manufactures ne se réduisent ni à un État peu interventionniste ni à la protection sociale industrielle du XIXe siècle [S08].

| Choix | Proposition | Portée |
|---|---|---|
| Amendement | **Direction camérale** sur la loi économique conservée. | Petit ajustement ; gate mère inchangé. |
| Variante — **recommandée** | **Économie caméraliste**, parent économique à choisir après comparaison des effets agraires et industriels. | Périmètre initial AUS/PRU ; aucune assimilation à une identité culturelle nationale. |
| Nouvelle loi | **Manufactures et domaines de la Couronne**, dans Système économique. | Option autonome si les différences d'investissement le justifient. |
| Nouveau groupe | **Administration économique**, séparant privilèges, régies et bureaucratie du régime d'investissement. | Chantier transversal, non nécessaire pour réparer la citoyenneté de départ. |

La sujétion autrichienne déjà demandée est préservée ; celle de Prusse est corrigée dans ce lot. Aucun changement économique de ces pays n'est installé.

## D. États italiens : ne pas donner une technologie à tous pour sauver une loi

| Pays | État courant et précision historique | Orientation |
|---|---|---|
| Toscane, TUS | Interventionnisme sans économie politique classique. Des réformes effectives et une influence physiocratique sont documentées avant 1776 [S16]. | Variante **Réformes économiques léopoldines** ; ne pas projeter les mesures des années 1780. |
| Parme, PAR | Même loi/gate, mais rupture avec Du Tillot après 1771 [S17]. | Variante conservant une économie de privilèges ; aucune copie du profil toscan. |
| Modène, MOD | Interventionnisme sans gate ; sources détaillées insuffisantes dans cette passe pour certifier la totalité du système économique. | Étudier une variante de manufactures ducales ; conserver l'incertitude. |
| Massa-Carrara, MCA | Même défaut technique. **MCA**, pas MAS : MAS est Mascara. L'absence de gate ne démontre pas l'absence de toute activité commerciale. | Variante ou maintien documenté après recherche spécifique supplémentaire. |
| Lucques, LUC | Oligarchie et économie urbaine/agricole ; le patrimoine commercial ne prouve pas la mise en œuvre d'un système économique classique national [S15]. | Variante **Économie patrimoniale de la cité** ; sujétion déjà demandée mais condition de gouvernance à résoudre. |
| Gênes et Venise, GEN/VEN | **Banques marchandes** déjà actives dans les demandes, avec variante propre. Le signalement d'interventionnisme y est dépassé. | Préserver le travail existant, traiter séparément les lois de citoyenneté/gouvernance. |

Pour **chaque** profil économique italien non résolu :

1. **Amendement :** privilèges manufacturiers, économie rurale réformatrice ou patriciat investisseur ; effets limités, gate de la loi mère non réparé.
2. **Variante — recommandée :** nom et accès propres au cas documenté ci-dessus, après choix des effets économiques.
3. **Nouvelle loi :** économie corporative/ducale dans le groupe existant, si l'écart concerne réellement le mode d'investissement.
4. **Nouveau groupe :** organisation corporative indépendante du système économique ; chantier de grande ampleur.

La technologie `classical_political_economy` est en **ère 4**, pas 7. Son octroi implique ses propres parents et d'autres déblocages : l'accord n'est pas donné en bloc à TUS/PAR/LUC/MOD/MCA. Les recettes, bâtiments, PM et profils technologiques restent intacts.

## E. Pologne-Lituanie : le montage électif existe déjà

PLC possède `amendment_elective_monarchy`, `amendment_liberum_veto` et un gouvernement `gov_elective_monarchy` sélectionné par **république présidentielle + oligarchie**. Ce gouvernement donne une titulature royale et une succession de type `dictatorial`. Cela représente partiellement l'élection nobiliaire, mais ne prouve pas une simulation fidèle du scrutin du Sejm. Remplacer simplement la loi par monarchie désactiverait ce montage et pourrait introduire un héritier dynastique [S11].

| Choix | Proposition | Limite |
|---|---|---|
| Amendement | Conserver et améliorer l'amendement électif existant. | Déjà présent ; ne change pas l'étiquette de la loi mère ni son gate. |
| Variante — **recommandée** | **Monarchie élective nobiliaire**, parent république présidentielle pour préserver le comportement électif ; adapter les sélecteurs et les amendements qui testent la loi exacte. | Contrôler l'absence d'héritier automatique, les élections et le maintien de Stanisław August. |
| Nouvelle loi | **Monarchie élective**, dans Principes de gouvernance, avec succession et IA propres. | Davantage de règles que le seul changement de nom. |
| Nouveau groupe | **Mode de désignation du souverain**, indépendant de la monarchie/république. | Distingue héritage, élection nobiliaire et désignation ; refonte mondiale nécessaire. |

La citoyenneté doit être résolue en même temps : la sujétion vanilla se débloque par monarchie, théocratie, chefferie ou administration coloniale, pas par cette république élective. Une variante de citoyenneté des ordres est préférable à une activation républicaine forcée sans explication. PLC reste inchangée dans ce lot.

## F. Pays-Bas, Venise, Gênes, Lucques et villes impériales

Le stathoudérat néerlandais est héréditaire à l'intérieur d'une république, les doges sont des magistrats électifs, les cités patriciennes ont des appartenances bourgeoises et des conseils restreints [S12, S14–S15]. La présence d'une loi de famille républicaine n'est donc pas à elle seule une erreur historique. Le gate `national_sovereignty`, la titulature, le mandat et la succession demandent des contrôles distincts.

| Choix | Gouvernance | Citoyenneté |
|---|---|---|
| Amendement | **Stathoudérat**, **Dogat** ou **Conseil patricien** sur une base républicaine ; conserver les variantes marchandes existantes. | **Droit de bourgeoisie** sur une base techniquement admissible ; ne supprime pas un gate de la loi mère. |
| Variante — **recommandée** | Variantes propres au stathoudérat et aux républiques patriciennes, avec modes de succession distincts. | **Appartenance corporative**, parent sujétion, avec disponibilité explicitement adaptée aux républiques et règles d'acceptation propres. |
| Nouvelle loi | **République patricienne** dans Principes de gouvernance, en distinguant ensuite les mandats. | **Citoyenneté des corps et bourgeoisies**, dans Citoyenneté. |
| Nouveau groupe | **Organisation territoriale et des conseils**, si le caractère fédéral doit devenir indépendant de la gouvernance. | **Accès à la bourgeoisie**, si les droits locaux doivent être séparés de l'acceptation culturelle. |

Villes allemandes réservées : BRE, FRM, HAM, LUB, NUR, RCI, SAC, SBI, SKI, SMM, SRQ, SRT, SUU. Les lois et gouvernements spécifiques déjà créés pour certaines sont préservés. LUC possède déjà une demande de sujétion : elle est signalée comme exception de compatibilité, pas présentée comme un exemple valide à généraliser.

## G. Suisse : une confédération de régimes différents

La loi de **suffrage censitaire** est remplacée par **oligarchie** comme approximation de l'ensemble représenté par SWI. Ce choix tient compte de la fermeture patricienne/corporative, sans effacer les cantons ruraux et leurs assemblées [S13]. La gouvernance et la citoyenneté restent ouvertes.

| Choix | Proposition |
|---|---|
| Amendement | **Diète et privilèges cantonaux** sur le montage parlementaire/oligarchique conservé. |
| Variante — **recommandée** | **Confédération des cantons**, avec représentation des délégués et absence d'un exécutif national moderne ; citoyenneté corporative apparentée au cas F. |
| Nouvelle loi | **Confédération d'États**, dans Principes de gouvernance. |
| Nouveau groupe | **Organisation territoriale** : centralisée, fédérale, confédérale. Coût de développement très élevé et effets transversaux. |

## H. Censure ottomane : loi adéquate, prérequis d'adoption à distinguer

La censure vanilla est une approximation historique acceptable [S18] ; sa demande est désormais explicite au départ. Son gate `periodical_print_networks` n'est pas détenu par TUR. La présence d'imprimeries autorisées ne justifie pas de lui offrir un réseau de périodiques national.

Ce cas n'exige pas une nouvelle loi pour sa seule description historique. Si le moteur refuse la demande initiale, les solutions à examiner sont : amendement de contrôle des publications sur une base disponible (ne résout pas un gate mère), variante **Contrôle des publications autorisées** sans gate anachronique, nouvelle loi dans Liberté d'expression, puis groupe indépendant d'administration de l'imprimé seulement si un projet plus large le justifie. La correction globale du gate de censure demanderait d'auditer tous ses consommateurs ; elle n'est pas faite ici.

## Priorités proposées pour la décision suivante

1. **Espagne : variante Sujétion bourbonienne.**
2. **Citoyenneté corporative des républiques**, avec la spécificité polonaise.
3. **Économies d'Ancien Régime**, par profils nationaux ; traiter les gates via les variantes plutôt que distribuer romantisme/nationalisme.
4. **Gouvernances électives et confédérales**, en préservant les mécanismes déjà présents.

Aucun nouveau groupe de lois n'est recommandé comme première solution : les besoins immédiats peuvent être traités par des variantes dans les groupes existants.
