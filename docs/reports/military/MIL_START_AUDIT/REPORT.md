# MIL-START-AUDIT — 17 octobre 2026

Statut : **READY_FOR_RUNTIME_VALIDATION**. Audit statique ; aucun lancement moteur. Base Git : `f97dc56`. Les cinq navires américains constituent un point ouvert distinct, décrit ci-dessous.

## Résultat installé

Les nombres sont des unités scriptées, pas des effectifs historiques attestés ni des soldats effectivement employés.

| Pays | TAG | Réguliers avant → après | Conscrits avant → après | Navires avant → après |
|---|---|---|---|---|
| États-Unis | USA | 12 mousquets + 1 canon de campagne, inchangés | 15 mousquets, inchangés, non levés | 5 caravelles, inchangées |
| Nouvelle-Grenade | SC2 | 23 ligne + 6 irréguliers + 5 cuirassiers → 23 mousquets + 6 irréguliers + 5 lanciers | 0 → 0 | 0 → 0 |
| Río de la Plata | SC4 | 6 ligne + 1 cuirassier → 6 mousquets + 1 lancier | 0 → 0 | 1 caravelle indisponible → 0 |
| Brésil | BRZ | 1 ligne + 2 irréguliers + 1 cuirassier → 3 irréguliers + 1 lancier | 0 → 0 | 9 → 9 |
| Portugal | POR | 18 ligne + 4 dragons + 2 canons de campagne → 18 mousquets + 4 dragons + 2 canons de campagne | 30 ligne → 23 mousquets | 12 → 12 ; 1 vaisseau de ligne remplacé par 1 caravelle |

Les états d'origine, QG et portées sauvegardées des armées restent identiques. Les commandants de ces quatre pays sont conservés. Aucun régulier supplémentaire, technologie, population, loi, bâtiment ou pacte n'est ajouté.

Six noms propres de formations, localisés en français et anglais dans des fichiers indépendants, remplacent les appellations nationales postérieures : troupes royales/escadre du Brésil, garnison du Río de la Plata, garnison de Quito, troupes de Nouvelle-Grenade, garnison du Venezuela. Le commentaire argentin relatif à 1836–1837 est retiré. Aucun nom partagé n'est surchargé.

## Déblocages vérifiés

| Type | Technologie du mod | Conclusion |
|---|---|---|
| Infanterie de ligne | armament_standardization_inspection | absente des cinq pays |
| Infanterie à mousquet | light_infantry_tactics | présente USA, SC2, SC4, POR ; absente BRZ |
| Irréguliers / lanciers | aucun | solution de repli disponible au Brésil ; lanciers disponibles dans les colonies |
| Dragons | regulated_small_arms | disponible POR ; absent BRZ, SC2, SC4 |
| Cuirassiers | military_veterinary_services | absent BRZ, SC2, SC4 |
| Canons de campagne | standardized_field_artillery | disponible USA et POR |
| Caravelle | enclosed_dock_systems | disponible BRZ/POR ; absente SC4/USA |
| Galère / cogue | state_dockyard_systems | disponible BRZ/POR ; absente SC4/USA |
| Vaisseau de ligne | marine_chronometry | absent POR |

Les lanciers constituent une abstraction de cavalerie ancienne accessible. Cela ne signifie pas que tous les cavaliers coloniaux portaient historiquement des lances. Une représentation plus exacte des dragons coloniaux demanderait de revoir les déblocages globaux, volontairement préservés ici.

Le navire isolé de SC4 est retiré avec sa formation vide : aucune coque de remplacement accessible, aucun amiral ou scope sauvegardé à détacher. Ce retrait répond au déblocage du mod ; il ne prétend pas démontrer l'absence historique de toute embarcation armée espagnole dans l'estuaire. Le remplacement portugais conserve le nombre de coques mais réduit leurs capacités, sans compensation artificielle.

## Population, recrutement et lois

| Pays | Population totale scriptée | Loi militaire effective par lecture des effets de départ |
|---|---:|---|
| USA | 2 487 774 | levées paysannes, activation explicite |
| SC2 | 2 242 298 | armée professionnelle, héritée de effect_starting_politics_conservative |
| SC4 | 700 000 | même héritage |
| BRZ | 2 020 000 | même héritage |
| POR | 5 122 927, possessions comprises | levées paysannes, activation explicite après l'effet conservateur |

Les inventaires `BEFORE.json` et `AFTER.json` donnent chaque formation, chaque contingent, sa région, sa population, ses technologies et ses déblocages manquants. Le cumul des unités est vérifié séparément des populations nationales.

| Région portugaise | Population | Réguliers | Conscrits avant | Plan après |
|---|---:|---:|---:|---:|
| Alentejo | 289 912 | 24 | 0 | 0 |
| Entre Douro e Minho | 763 148 | 0 | 12 | 9 |
| Beira | 701 683 | 0 | 11 | 8 |
| Estremadura | 501 789 | 0 | 7 | 6 |

Plan prudent : partie entière de population × 0,30 × 0,04 / 1 000, plafonnée à 25 par état. `WORKING_ADULT_RATIO_BASE` vaut 0,30 ; les levées paysannes donnent 4 % de conscription, des centres limités à 25 et des casernes limitées à 25. Les 24 réguliers de l'Alentejo respectent ce dernier plafond. Les 30 conscrits excédaient déjà le calcul nominal de 23, avant les restrictions aux paysans éligibles.

**Ce calcul n'est pas une reconstitution exacte de l'algorithme moteur.** Emploi réel, qualifications, incorporation, modificateurs locaux et arrondis peuvent encore diminuer les capacités. Les bâtiments militaires sont recruteurs/centres automatiques selon les définitions natives : aucune double caserne n'a été créée. L'absence de general_staff empêche l'instruction générale ; les méthodes sans organisation, disponibles par défaut, restent la référence statique. Vérifier le choix réellement effectué en jeu.

## Contexte et provenance

Les pactes existants rattachent SC2 et SC4 à l'Espagne et BRZ au Portugal comme colonies. Ils restent inchangés. Les noms de garnisons représentent des forces locales de la Couronne, sans créer d'armée nationale indépendante.

L'[Archivo General de la Nación argentin](https://www.argentina.gob.ar/sites/default/files/librocolonia_1.pdf), *Fondos documentales, período colonial*, vol. 1, 2011, situe la nomination de Cevallos et la création de la vice-royauté au 1er août 1776, après la préparation de l'expédition en juin. La garnison de janvier ne porte donc pas de titre vice-royal.

L'[étude universitaire sur les milices réglées néogrenadines](https://noesis.uis.edu.co/bitstreams/a4b8f0ae-4ca1-4949-947c-c9a8511d2791/download) distingue la réforme des garnisons côtières et son extension aux milices de l'intérieur ; elle ne fournit pas les effectifs de chaque état du mod. Les volumes existants sont préservés faute de preuve suffisante pour une reconstruction exhaustive.

Le [catalogue de l'Arquivo Histórico do Exército brésilien](https://www.ahex.eb.mil.br/images/Catalogo_Destino_Acervo_EB-AHEX_2020_3.pdf) atteste les dragons du Rio Grande au XVIIIe siècle. Le [fonds portugais du commandement de Lippe](https://ahm-exercito.defesa.gov.pt/details?id=101998) décrit les réformes d'instruction et de discipline de 1762–1768. Ces références justifient le contexte de troupes royales, pas une équivalence entre régiment historique et bataillon du jeu.

`git blame` rattache les lignes BRZ anciennes à la limite historique disponible `b602804`, les scopes à `66ed0fc4`, et les personnages aux lots CLEANUP. Une limite Git ne démontre pas l'auteur antérieur réel. Le commentaire SC4 sur 1836 est un héritage vérifiable ; ne pas attribuer automatiquement tous les chiffres à Tsar.

## Points ouverts

1. **NAV-USA-TECH** : les 5 caravelles américaines, déjà présentes dans MIL-USA, demandent enclosed_dock_systems, absent. Le premier contrôle élargi a donc échoué sur cette flotte, tout en confirmant la conservation du fichier américain. Le contrôle terrestre passe. Aucun changement américain n'est fait dans ce lot ; examiner en jeu la conservation et la capacité de remplacement des coques avant un lot naval spécifique. Ne pas déclarer toutes les unités américaines compatibles.
2. BRZ et SC4 héritent d'une armée professionnelle malgré l'absence de permanent_engineer_services, son déblocage actuel. Loi préservée conformément à la mission. SC2 possède ce déblocage. Contrôler le maintien de la loi à l'initialisation.
3. Les activations `law_type:state_religion` sans préfixe law_ chez SC2/SC4 sont une anomalie héritée, hors correction militaire ; ne pas les corriger silencieusement ici.
4. Le général portugais de rang initial peut ne pas couvrir les 47 bataillons après levée complète (capacité de base 30). Aucun grade ou commandant fictif n'est ajouté pour compenser.
5. L'artillerie américaine n'a pas de fonderie nationale identifiée. Vérifier approvisionnement/importations et prix ; ne pas injecter une usine ou des revenus cachés.

## Validation

MIL-USA figurait dans main au début du lot et son fichier entier est resté identique pendant ce lot (SHA-256 dans VALIDATION.json). Les quatre pays corrigés n'ont plus de type terrestre ou naval à technologie manquante dans leurs formations conservées. Les stocks de conscrits ne sont pas marqués comme levés. Les rapports conservent le résultat du premier contrôle naval américain et son classement en point ouvert, au lieu d'en faire une réussite.

Guide moteur : nouvelle partie 1776, successivement USA, SC2, SC4, BRZ, POR ; relever formations, types, effectifs, bâtiments recruteurs et conscription à la pause puis après 1 jour, 1 semaine, 1 mois et 3 mois. Pour POR, comparer 24 réguliers / 23 conscrits potentiels, lever les trois contingents et surveiller leurs centres. Pour SC2, contrôler 7 + 18 + 9 réguliers ; SC4 7 ; BRZ 4. Comparer chaque nombre aux capacités réelles et aux journaux d'erreurs. Une diminution inexpliquée impose de conserver le point ouvert et la sauvegarde de reproduction.
