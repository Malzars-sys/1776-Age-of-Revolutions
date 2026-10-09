# Départ britannique, Indes orientales et flottes — 8 octobre 2026

Statut actuel : profils navals approuvés intégrés, nouvelle révision économique et démographique intégrée, contrôles statiques passés. Aucun essai moteur ni budget en partie confirmé. Les lots PM 13 à 17 sont intégrés ; leur vérification préserve les fichiers navals, économiques et démographiques. Le lot 16 garde les données bleues et corrige uniquement les flèches de groupe ; le lot 17 termine deux recolorations sans redessin. Aucun changement de gameplay supplémentaire pendant cette clôture graphique. Les nombres d'exports ci-dessous décrivent les contrôles navals à leur date d'intégration ; le registre graphique actuel en contient 151.

## Correction navale ultérieure : rôles et couleur

La passe suivante classe la **caravelle en navire capital**, recolore son profil dans le jaune natif des capitaux, et classe la **galère en croiseur de défense côtière primitif** : portée au port 1 et dégâts réduits de 80 % hors de portée. Les coûts, équipages, chiffres de base et effectifs de départ décrits ci-dessous restent inchangés. Les comparaisons historiques avec les classes remplacées ne définissent donc plus le rôle actuel de chaque coque. Les mentions orange du bilan initial ci-dessous sont historiques : la [révision jaune](../../assets/early_ship_sources_2026-10-08/capital_colour_revision.json) fait autorité pour la texture courante. La [proposition des quatre catégories, spécialisations et déblocages](../../naval/early_ship_design_proposal_2026-10-08.md) attend validation ; aucun équipement configurable ni nouveau déblocage technologique n'est encore intégré. Contrôles statiques seulement, aucun nouveau résultat budgétaire en partie.

L'[étape d'équipement autorisée ensuite](../../naval/early_ship_equipment_integration_2026-10-08.md) intègre les modèles précis, les fonctions cumulables demandées et les nouvelles portes technologiques. Les nombres de navires britanniques et des autres flottes sont conservés, comme les administrations, bâtiments et populations. Les flottes hors de la liste autorisée sont ramenées aux coques primitives pour rester compatibles avec leurs déblocages. Les valeurs et répartitions ci-dessous restent un historique économique : aucune nouvelle garantie budgétaire ni observation en partie n'est ajoutée. Les nouveaux dessins d'équipement sont encore en proposition, non intégrés.

## Révision finale après le retour en jeu

Le joueur rapporte désormais **+283** de bureaucratie britannique et **−1 200** aux Indes orientales, avec administrations à moitié remplies. Cette section remplace les objectifs chiffrés de la première passe ci-dessous.

### Navires et graphismes intégrés

Les trois profils approuvés sont raccordés aux classes : caravelle **orange**, galère **bleue**, cogue **bleue comme les transports**. Masters finaux, prompts et paramètres dans [la provenance navale](../../assets/early_ship_sources_2026-10-08/manifest.json). Les trois DDS 240 × 160 / huit mipmaps sont ajoutés au registre : **146 exports** reproductibles octet pour octet. Aucun redessin des profils approuvés, aucune miniature de contrôle versionnée.

Les modèles 3D standards en bois sont conservés : `military_navy_frigate_generic_entity`, `military_navy_manowar_generic_entity` et `sail_transport_ship_01_entity`. Le contrôle retrouve ces entités complètes dans les assets natifs. Ce sont des modèles de repli, pas de nouvelles reconstitutions 3D.

| Classe économique | Bois dur de construction | Tissu de construction | Équipage nominal | Coque / dégâts de coque |
| --- | ---: | ---: | ---: | ---: |
| Caravelle | 72 contre 358 | 43 contre 215 | 150 contre 500 | 450 / 12 contre 700 / 20 |
| Galère | 130 contre 650 | 78 contre 390 | 240 contre 800 | 1 000 / 15 contre 1 600 / 25 |
| Cogue | 104 contre 520 | 52 contre 260 | 60 contre 200 | 600 / 5 contre 1 500 / 25 |

Les coques économiques demandent environ **80 % de biens de construction en moins** et **70 % de marins en moins**. Caravelle et galère : grain 0,2 et bois dur 0,02 pour le ravitaillement, contre 1 et 0,1 pour les classes supérieures. Cogue : aucun charbon ni fer d'entretien, contrairement au transport moderne. Coques fixes sans amélioration moderne cachée ; puissances offensives, endurance et blindages inférieurs. Ces pourcentages concernent les paramètres, pas une garantie de réduction identique de la dépense totale de l'État.

La règle de répartition devient un huitième des catégories initiales **par pays**, avec minimum un navire avancé pour une catégorie présente chez un pays disposant d'`scientific_naval_architecture`. Ils sont concentrés d'abord dans les grandes formations. Le total de chaque flotte actuelle reste inchangé ; pas de seconde réduction arbitraire des 97 navires britanniques.

| Pays | Frégates | Vaisseaux de ligne / man-o'-war | Coques économiques | Total |
| --- | ---: | ---: | ---: | ---: |
| Royaume-Uni | 4 | 7 | 86 | 97 |
| France | 2 | 2 | 37 | 41 |
| Espagne | 2 | 2 | 36 | 40 |
| Russie | 1 | 2 | 29 | 32 |
| Pays-Bas | 1 | 1 | 12 | 14 |
| Portugal | 1 | 1 | 10 | 12 |
| Danemark-Norvège | 1 | 1 | 12 | 14 |
| Suède | 1 | 2 | 19 | 22 |

Les autres flottes suivent la même condition technologique. La classe supérieure existante du mod est `ship_type_ship_of_the_line`, correspondant ici aux man-o'-war demandés ; aucune classe moderne supplémentaire n'est inventée. Aucun transport initial explicite à convertir, donc la cogue reste disponible à construire sans être ajoutée artificiellement.

Équipage nominal britannique : **25 540**, contre 39 500 après la première passe et avant cette révision. Établissements de marins : **48 → 31 niveaux**, capacité nominale 31 000, soit plus de 20 % de réserve. Les amiraux, quartiers généraux et armées terrestres sont conservés.

### Bureaucratie britannique

Retrait supplémentaire prudent de **20 administrations**, plutôt que consommer tout l'excédent annoncé : métropole **72 → 52** ; total déclaré avec Jamaïque **74 → 54**.

| État | Après première passe | Maintenant |
| --- | ---: | ---: |
| Home Counties | 38 | 27 |
| Lancashire | 15 | 11 |
| Yorkshire | 8 | 6 |
| Midlands | 11 | 8 |

Perte de production de base à plein emploi : 200 de bureaucratie. Depuis le +283 rapporté, réserve estimée **+83 avant bonus nationaux**, ou environ +43 avec un bonus de 20 %. Le coût en population et en institutions, l'acceptation, les bonus et l'emploi restent calculés par le moteur ; il ne s'agit pas d'un solde observé. Les PM, lois et institutions britanniques ne sont pas modifiés.

### Recrutement des administrations indiennes

Les 170 niveaux existants sont conservés. Leur PM de propriété héréditaire était incompatible avec la loi initiale `law_appointed_bureaucrats` : raccordement à `pm_professional_bureaucrats`, sans changement de loi. Avec `pm_secular_bureaucrats` et `pm_simple_organization`, chaque niveau prévoit **1 000 bureaucrates et 500 commis**.

À la demande explicite du joueur, une portion de populations hindoues libres est transformée en familles **anglaises (`british`) protestantes**, spécialisées en bureaucrates et commis. Pas de création nette d'habitants ni de conversion des esclaves. Les anciens contingents anglais existants sont déduits du besoin ; les Écossais et tous les autres groupes sont conservés.

`british` est la culture primaire de BIC. `law_subjecthood` lui donne 100 d'acceptation primaire ; la religion protestante est aussi celle par défaut des Anglais et est compatible avec la liberté de conscience. La hiérarchie de caste vise les Hindous de cultures sud-asiatiques, pas ce contingent. Le type bureaucrate a une cible d'alphabétisation native de 40 % ; les métiers explicites évitent de compter exclusivement sur une promotion lente depuis les paysans.

Le calcul utilise le **ratio de travailleurs du mod, 30 %**, pas le 25 % vanilla. Réserve de recrutement **20 % pour chacun des deux métiers et dans chaque province**. Ce contingent permet théoriquement de fournir tous les emplois des administrations, même si une partie des travailleurs est indisponible.

| Province BIC | Niveaux d'administration | Personnes converties |
| --- | ---: | ---: |
| Bengale occidental | 75 | 435 948 |
| Bengale oriental | 50 | 297 495 |
| Bihar | 23 | 137 780 |
| Circars | 16 | 95 405 |
| Awadh | 6 | 36 000 |
| Total | 170 | **1 002 628** |

Soit **1,52 %** des 66 128 457 habitants déclarés dans ces cinq régions BIC. Les totaux régionaux sont strictement conservés, y compris les régions d'autres pays partageant le même État. C'est un réglage de gameplay demandé, pas une affirmation démographique historique.

À plein emploi, ces administrations donnent 1 700 de bureaucratie de base, soit 2 550 avec le bonus existant du service civil indien de +50 %, hors autres effets. Passer d'un emploi de 50 % à 100 % ajoute théoriquement **1 275**, ce qui couvre le déficit de 1 200 rapporté avec une faible marge. Le recrutement, les dépenses des administrations et le solde exact doivent être confirmés en nouvelle partie.

### Contrôles de cette révision

- `tools/audit_naval_admin_revision.py --check` : `PASS_STATIC_NAVAL_ADMIN_REVISION` ; 1 341 fichiers runtime hors périmètre inchangés, niveaux et PM ciblés, population conservée, réserves professionnelles suffisantes, totaux navals inchangés et technologies disponibles.
- `tools/rebuild_asset_icons.cjs --verify` : `PASS_EXACT_REBUILD`, **146** exports, anciens 143 inchangés.
- `git diff --check` : aucun défaut d'espacement après nettoyage des cinq lignes ajoutées.

Le snapshot de la première passe n'est pas écrasé. Le nouveau plan et les diagnostics sont dans `.asset-cache/naval_admin_revision_2026-10-08/`, ignoré par Git. **Ne pas relancer `--prepare` sur le départ modifié.** Ce contrôle ne confirme ni un budget réel ni l'emploi effectif du moteur. Aucune action dans le jeu ouvert, aucun redémarrage, commit ou push.

## Première passe — historique, chiffres remplacés par la révision ci-dessus

## Administrations

La dernière précision du joueur donne un excédent britannique d'environ 500 de bureaucratie, et non un manque de 500. Retrait mesuré de 18 niveaux en métropole : 90 → 72 ; les deux niveaux déclarés en Jamaïque sont inchangés. La perte théorique est de 180 de bureaucratie à effectifs complets, sans modification des PM.

| État britannique | Avant | Après |
| --- | ---: | ---: |
| Home Counties | 47 | 38 |
| Lancashire | 19 | 15 |
| Yorkshire | 10 | 8 |
| Midlands | 14 | 11 |

Les administrations de BIC passent de 30 à 170 niveaux (+140). Le PM initial produit 10 de bureaucratie par niveau ; le bonus existant du service civil indien de +50 % porte l'ajout théorique à 2 100 à plein emploi. Les effets réels dépendent du recrutement, des qualifications et de l'approvisionnement.

| État de BIC | Avant | Après |
| --- | ---: | ---: |
| Bengale occidental | 15 | 75 |
| Bengale oriental | 10 | 50 |
| Bihar | 3 | 23 |
| Circars | 1 | 16 |
| Awadh | 1 | 6 |

Pour éviter que ces administrations saturent les infrastructures, ajout de 51 niveaux de routes traditionnelles : 36 → 87. Répartition finale : Bengale occidental 38, oriental 25, Bihar 11, Circars 10, Awadh 3. Les PM routiers existants sont conservés ; aucune voie ferrée ni aucun service de voyageurs moderne n'est ajouté. Le contrôle statique ne relève plus de déficit d'infrastructure dans ces États.

## Propriété britannique en Inde

Toutes les implantations privées explicitement déclarées pour BIC, dans les fichiers régionaux et la redistribution mondiale, reçoivent une propriété britannique :

- Plantations autorisées par la définition effective de la Compagnie des Indes orientales : propriété `company_east_india_company`, pays GBR.
- Autres fermes et plantations : manoirs britanniques des Home Counties.
- Industries, commerce et routes : quartiers d'affaires britanniques des Home Counties.

Total déclaré après l'ajout des routes : 164 niveaux privés, dont 134 rattachés aux quartiers d'affaires, 17 à la compagnie et 13 aux manoirs. Les administrations et ports publics restent BIC : ils ne sont pas transférés à un propriétaire privé. Les bâtiments générés automatiquement par le moteur ne sont pas créés ou réécrits arbitrairement. Les autres compagnies et propriétaires hors BIC sont conservés.

## Classes navales économiques et flottes initiales

Trois classes disponibles pour tous, sans remplacer les classes modernes constructibles : caravelle, galère et cogue. Coûts de bois dur, tissu et ravitaillement réduits ; statistiques et équipages inférieurs aux classes remplacées. Coques fixes sans améliorations modernes automatiques. Ce choix suit la correspondance demandée par le joueur, pas une reconstitution historique universelle des flottes de 1776.

La dernière consigne demande de garder des navires avancés chez les pays technologiquement avancés. Critère explicite : présence initiale d'`scientific_naval_architecture`. Pour chaque ancien groupe de frégates ou vaisseaux de ligne, conserver un quart arrondi à l'entier inférieur, convertir le reste en caravelles ou galères. Les transports auraient été remplacés par des cogues ; aucun bloc de transport explicite n'était présent dans les formations initiales examinées. La cogue est constructible, pas ajoutée artificiellement aux flottes.

Seuls les effectifs britanniques sont réduits d'environ 20 %, avec arrondi par flotte : total 120 → 97. Les autres pays conservent leurs effectifs et changent uniquement leur mélange de types. 41 flottes de 26 pays examinées. Armées terrestres, amiraux, quartiers généraux et métadonnées des formations inchangés par cette passe.

| Flotte britannique | Avant | Après |
| --- | ---: | ---: |
| Channel Fleet (`cleanup2d3b_gbr_naval_1`) | 50 | 40 |
| `cleanup2d3b_gbr_naval_2` | 28 | 22 |
| Mediterranean Station | 12 | 10 |
| North America and West Indies Station | 12 | 10 |
| `cleanup2d3b_gbr_naval_5` | 7 | 6 |
| `cleanup2d3b_gbr_naval_6` | 5 | 4 |
| `cleanup2d3b_gbr_naval_7` | 6 | 5 |

Le Royaume-Uni garde 18 navires avancés et reçoit 79 coques économiques. L'équipage nominal de cette flotte est de 39 500. Les établissements de marins britanniques passent de 84 à 48 niveaux : capacité nominale de 48 000, au moins 20 % de réserve. Aucun établissement naval d'un autre pays n'est réduit.

## Graphismes et noms

Les trois classes disposent de noms français/anglais et de règles de nommage avec les préfixes nationaux natifs. Les entités 3D existantes de frégate, man-o'-war et transport à voile servent de repli ; aucun nouveau modèle 3D n'est créé.

À la demande du joueur, trois profils 2D originaux ont été préparés avec l'outil intégré imagegen. **Correction de palette du 8 octobre : caravelle orange, galère bleue, cogue de la couleur des transports de troupes natifs (bleue, vérifiée sur `silhouette_troop_ship.dds`).** Cette consigne remplace l'association initiale erronée aux couleurs des groupes. Les deux premiers masters ont été recolorés uniquement, sans nouvelle génération, en conservant leurs dimensions, alpha et valeurs ; la cogue est inchangée octet pour octet. Les groupes et statistiques navals ne changent pas pendant cette correction graphique.

Les masters, prompts, paramètres de recoloration et DDS candidats sont uniquement dans `.asset-cache/early_ship_graphics_2026-10-08/`, ignoré par Git, tant que le lot n'est pas validé. Export candidat : 240 × 160, BGRA8 natif, huit mipmaps, vraie transparence. Décodage indépendant, alpha et lisibilité à 30/48 pixels contrôlés. Les définitions utilisent encore les profils vanilla de repli ; ne pas présenter les nouveaux dessins comme déjà visibles en partie.

Le lot PM 12 approuvé est intégré. Le lot 13 propose seulement trois images de groupes (routes, extraction du phosphate, automatisation du phosphate), sans redessiner les PM routiers existants. Il reste en attente.

## Vérification et limites de la première passe

`tools/audit_british_colonial_start.py` retourne `PASS_STATIC_BRITISH_COLONIAL_START`. Le snapshot et les diagnostics détaillés restent dans le cache ignoré. Contrôles : niveaux agrégés, propriété de chaque implantation, conservation des PM, données des formations hors navires, disponibilité des classes, textures de repli, entités et nommage, infrastructures et empreintes des fichiers hors périmètre.

`tools/rebuild_asset_icons.cjs --verify` : 143 exports approuvés reconstructibles exactement. Le prévisualiseur du lot 13 confirme trois propositions sans modification runtime ; celui des navires confirme les trois DDS candidats et leur stockage natif.

Ces changements d'histoire s'appliquent à une nouvelle partie. Les soldes budgétaires ne sont pas calculés exactement par ces vérifications et le déficit britannique de 27 k n'est pas déclaré résolu sans essai en jeu. Aucun redémarrage, sauvegarde, commit ni push effectué pendant cette passe.
