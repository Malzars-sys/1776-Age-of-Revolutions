# Cahier des charges des assets — 1776, lot 1

Date : 1er octobre 2026. Statut : références inspectées et lot proposé ; aucune nouvelle illustration de gameplay créée ou intégrée.

## 1. Périmètre et références réellement examinées

Ce document répond à la demande de comparer les technologies, biens, bâtiments et méthodes de production au jeu de base, en ajoutant les unités militaires. La chaîne du cuivre est exclue du lot : pas de création dédiée à son extraction, son raffinage ou ses produits dérivés. Un canon appartient ici au besoin d'illustration militaire, pas à un lot de production de cuivre.

L'étude utilise l'installation locale de Victoria 3, dans `C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game`. Les anciens rapports ASSET1–3 sont un historique, pas l'inventaire actuel. L'ancien générateur ASSET2 n'a pas été relancé ni ses rapports écrasés.

- 38 références vanilla inspectées visuellement : huit technologies, huit biens, huit bâtiments, huit PM et six illustrations d'unités terrestres.
- 705 en-têtes DDS examinés dans les répertoires principaux de ces cinq familles. Les variantes, sous-répertoires et fonds de panneaux ne sont pas tous inclus dans ce décompte technique.
- Inventaire courant : 243 technologies recherchables, 71 biens, 128 bâtiments, 561 PM reliés aux PMG de bâtiments, 21 unités terrestres et 21 types de navires. Il s'agit de définitions résolues, pas de bâtiments construits ni d'une vérification de visibilité en partie.
- 145 objets utilisent encore une texture provisoire ; 137 après exclusion des objets directement identifiés comme cuivre. Ce n'est **pas** une commande de 137 fichiers distincts : plusieurs objets peuvent partager une image. Les objets sans champ visuel explicite ne deviennent pas automatiquement des commandes d'assets.
- Les trois illustrations militaires provisoires sont l'infanterie à mousquet, la bombarde et le canon de campagne. Les navires référencent des icônes de catégorie et des silhouettes vanilla existantes ; aucun fichier manquant n'a été détecté sur ces liens. Cela ne constitue pas une validation artistique exhaustive de tous les navires.

Les statuts `VANILLA_REFERENCE_NOT_SEMANTICALLY_VALIDATED` et `LOCAL_EXISTING_PROVENANCE_AND_SUBJECT_TO_REVIEW` signifient « fichier présent », jamais « illustration définitivement approuvée ».

Pièces de référence :

- [Planche des quatre familles](ASSET4_VANILLA_FOUR_FAMILIES_REFERENCE.png) : grandes vues et miniatures de 32 px sur fonds clair/sombre.
- [Planche des unités](ASSET4_VANILLA_UNIT_REFERENCE.png) : six scènes natives opaques.
- [Dimensions, formats et empreintes des références](ASSET4_VANILLA_REFERENCE_METADATA.csv).
- [Inventaire courant](ASSET4_CURRENT_VISUAL_INVENTORY_2026-10-01.csv), [variantes des unités](ASSET4_UNIT_VISUAL_INVENTORY_2026-10-01.csv) et [résumé technique](ASSET4_AUDIT_SUMMARY_2026-10-01.json).

Ces planches sont des comparaisons locales du jeu installé, pas des créations originales à livrer ou à intégrer au mod.

## 2. Direction artistique commune

La cible n'est pas une esthétique « steampunk » générique. Elle est le langage des illustrations vanilla de Victoria 3 : peinture stylisée, matière identifiable, grandes masses lisibles et petits détails subordonnés à la silhouette. Les cinq familles ne doivent pas être traitées de manière identique.

Conserver des tons naturels et patinés, une source lumineuse principale cohérente et des ombres courtes sur les objets détourés. Les couleurs servent d'abord à identifier la matière ou la fonction : pierre claire, poudre grise, bois brun, métal sombre. Ne pas appliquer une teinte sépia uniforme à toutes les familles.

À exclure : texte, lettres et chiffres décoratifs, signatures, filigranes, logos, badges de niveau, statistiques, boutons d'interface dessinés dans l'image, contours fluorescents, glow et look d'icône d'application. Aucun fond noir ou gris simulant la transparence. Les niveaux, cases, cercles de technologie et états de sélection restent à la charge du jeu.

Les scènes doivent être adaptées à la période du contenu, pas systématiquement à 1776 : le Ciment Portland est actuellement une technologie d'ère VII, explicitement postérieure à 1836 dans sa définition. Valider le modèle d'outil, d'arme ou d'installation avant le rendu final ; une période exacte non documentée ne doit pas être inventée pour remplir le brief.

## 3. Règles par famille

| Famille | Langage visuel attendu | Composition et fond | Références inspectées |
|---|---|---|---|
| Technologie | Objet ou groupe conceptuel peint, volumétrique ; détails et reflets au service du sens. Ce n'est pas une vignette de paysage miniature. | Un sujet dominant et un accessoire signifiant au maximum ; silhouette compacte ; alpha transparent ; aucun médaillon intégré. | `mechanical_tools`, `steelworking`, `intensive_agriculture`, `rationalism`, `academia`, `rifling`, `artillery`, `electrical_generation`. |
| Bien | Matière, objet ou petit groupe homogène peint ; contour lisible, texture simplifiée mais identifiable. | Objet isolé, centré et assez gros ; marges transparentes ; pas de cadre ni de décor. Différencier d'abord la forme et la valeur, pas seulement la couleur. | Charbon, fer, acier, outils, engrais, soufre, verre, papier. |
| Bâtiment | Petite scène de site ou d'atelier vue en trois quarts/plongée, avec produit ou symbole fonctionnel au premier plan. | Cadre fin métallique patiné aux coins arrondis **intégré à cette famille**, décor dans le cadre, produit saillant généralement en bas à droite. Transparence aux coins extérieurs, pas sur toute la scène. | Mines de charbon/fer, chimie, verrerie, aciérie, université, armes et fonderie d'artillerie. |
| PM | Pictogramme plat schématique beige/ocre, contours discrets ; **grain fin mat et dégradé vertical du haut clair vers le bas sombre**, selon la précision ultérieure du joueur le 3 octobre 2026. Aucun relief, ombre portée, perspective, extrusion ni rendu d'objet peint en volume. Les références fournies par le joueur priment sur les descriptions antérieures. | Grandes masses, deux symboles principaux au maximum ; alpha transparent ; aucun paysage, aucune case carrée intégrée. Les variantes partagent leur base visuelle. | Pics et pelles, pompe, nitroglycérine, dynamite, Bessemer, four à sole, philosophie et métier automatique ; canon, Bessemer et moteur fournis par le joueur le 3 octobre. |
| Unité terrestre | Illustration narrative peinte avec soldats, matériel et profondeur atmosphérique ; gestes lisibles, matière brossée. | Scène carrée **opaque**, sujet dominant dans la zone centrale, arrière-plan plus calme. Pas de cadre de bâtiment ni d'objet détouré flottant. | Infanterie irrégulière/de ligne, artillerie ancienne/mobile, hussards et cuirassiers européens. |

### Technologies, biens et bâtiments ne sont pas interchangeables

**Précision du joueur, 5 octobre 2026 (lot 15) :** ne pas appliquer automatiquement aux technologies la composition des bâtiments avec un produit fini au premier plan. Pour Verre pressé et Blanchiment papetier industriel, retirer le gobelet et le paquet de feuilles séparés : l'appareil isolé porte le concept, avec son contenu utile au procédé. Pièces interchangeables peut montrer plusieurs familles de composants, notamment des roues crantées, mais conserver des pièces assorties à l'intérieur de chaque famille. Cela ne transforme pas les technologies en pictogrammes plats de PM et n'interdit pas un accessoire signifiant dans un autre concept validé.

Le bien ciment montre ce qui se vend ; le PM montre comment on le produit ; la technologie montre ce qui change dans le savoir-faire ; la cimenterie montre où l'on produit. Ne pas réutiliser un même sac de ciment comme seule image pour ces quatre rôles.

Dans les bâtiments, réutiliser la forme et les couleurs du bien validé pour le produit de premier plan, afin de garder une identité visuelle. Cela n'autorise pas à coller un agrandissement de pictogramme de PM à la place de la scène.

### Couleurs des PM

**Direction Génie routier révisée, 6 octobre 2026 :** le joueur rejette désormais la représentation directe d'une route pavée comme concept de technologie. Cette instruction remplace, pour Génie routier uniquement, la consigne de reprendre les pavés en éventail. Le nouvel aperçu propose un niveau en bois à fil à plomb avec une coupe de chaussée en couches ; cette composition reste soumise à validation avant intégration. Voir la [nouvelle proposition](road_engineering_revision_2026-10-05/README.md). Cela ne change pas les règles graphiques des PM ni le bâtiment vanilla d'infrastructures.

**Exception validée par le joueur le 4 octobre 2026 :** conserver les sept anciennes icônes des PM du laboratoire déjà en jeu. Ne pas intégrer leurs variantes plates ou granuleuses proposées. Les dix PM des routes et de l'industrie/extraction de cette révision sont validés avec grain fin et dégradé vertical ; cette décision ne change ni les recettes ni les déblocages.

**Précision complémentaire du joueur le 3 octobre 2026 :** plat ne veut pas dire uniquement des aplats lisses. Ajouter une texture légèrement granuleuse dans les surfaces et un dégradé graphique vertical continu, plus clair en haut et plus sombre en bas. Ne pas recréer de biseau, de lumière volumétrique, d'ombre portée ni de papier découpé en épaisseur. Conserver les silhouettes et les ouvertures transparentes des 17 PM refaits ; cette retouche n'affecte ni le bâtiment vanilla ni la technologie de pavage.

**Direction corrigée le 3 octobre 2026 :** les anciennes mentions « bas-relief », « relief discret » et « ombres brunes » ne constituent plus des consignes pour les PM. Utiliser des silhouettes graphiques plates, sans effet d'éclairage ni matière tridimensionnelle. Cette correction concerne les PM des lots précédents comme ceux des routes. Les autres familles gardent leur propre direction artistique ; une technologie n'est pas un pictogramme PM. La photo de pavés en éventail fournie par le joueur remplace l'ancienne coupe empierrée comme référence de l'icône de Génie routier. Pour les Infrastructures régionales, réutiliser directement le fichier vanilla `building_railway.dds`, sans nouvelle illustration.

La majorité des procédés examinés emploie un or/beige patiné, avec ombres brunes. Le métier automatique montre aussi une famille verte : la palette vanilla n'est donc pas uniformément monochrome. Pour le lot ciment, conserver une série ocre cohérente ; ne pas reprendre automatiquement les couleurs bleues/vertes des laboratoires et ne pas modifier ces assets déjà en place.

### Unités et variantes culturelles

Les trois unités prioritaires possèdent actuellement une seule illustration de repli, sans condition culturelle. Le lot propose trois illustrations de remplacement de ce repli, **pas** une couverture de tous les uniformes et pays. Une tenue européenne simplifiée sans drapeau reste une convention de repli, pas une représentation universelle historiquement neutre. Les variantes culturelles pourront former un lot distinct ; ne pas écraser les branches culturelles des autres unités.

L'infanterie à mousquet doit se distinguer de l'infanterie irrégulière et du rang de ligne vanilla à shakos. La bombarde et le canon de campagne doivent se distinguer par la silhouette de l'affût, le poids visuel et la mobilité suggérée, pas seulement par la couleur. Éviter les signes propres à l'artillerie moderne : pneus, bouclier blindé moderne, système de recul visible ou uniforme tardif non justifié.

## 4. Livrables et contraintes techniques

Les dimensions sont fondées sur les DDS inspectés ; les PM existent réellement dans deux tailles. Ne pas appliquer 256 × 256 à toutes les familles.

| Famille | Master PNG de travail recommandé | Export retenu pour le lot | Mipmaps proposées | Alpha |
|---|---:|---:|---:|---|
| Technologie | 1024 × 1024 | 256 × 256 | 9 | Vraie transparence |
| Bien | 1024 × 1024 | 256 × 256 | 9 | Vraie transparence |
| Bâtiment | 1024 ou 2048, carré | 256 × 256 | 9 | Coins extérieurs transparents, scène remplie |
| PM | 1024 × 1024 | 208 × 208 | 8 | Vraie transparence |
| Unité | 1024 ou 2048, carré | 512 × 512 | 10 si chaîne complète retenue | Scène opaque |

Observation native : technologies principalement 256/9 ; biens principalement 256/9 ; bâtiments principalement 256/9 ; PM principalement 104/7, avec aussi 208/8 ; unités 512, avec plusieurs choix de compression et de mipmaps, souvent sans chaîne déclarée. Le 208/8 choisi pour les nouveaux PM est un format natif constaté et correspond aux PM récents du laboratoire ; il n'est pas présenté comme l'unique format vanilla. Les dix mipmaps des futures unités sont un choix d'export proposé, pas une description de tous les fichiers natifs.

Livrer le master PNG, le PNG à la taille cible, le DDS final et une planche de contrôle. Utiliser un export BGRA8 legacy natif (A8R8G8B8) avec alpha conservé ; aucune compression destructive supplémentaire avant la validation visuelle. Conserver noms de fichier stables, profil PNG standard sRGB et sources séparées des exports. Ne pas intégrer de fond factice pour satisfaire un format RGB.

Pour le 208 px, chaîne complète : 208, 104, 52, 26, 13, 6, 3, 1. Ne pas étirer un master non carré. Réduire avec anticrénelage et vérifier les bords après réduction ; la transparence doit être testée sur les fichiers exportés, pas déduite de l'apparence du master.

**Correctif de compatibilité étendu, 3 octobre 2026 :** les biens, technologies, bâtiments, PM et illustrations militaires exportés par nos outils doivent tous utiliser BGRA8 legacy avec les masques natifs A8R8G8B8, pas RGBA8 legacy. Le décodage standard des anciens exports était conforme au PNG, mais ne reproduisait pas leur lecture en jeu : les captures du joueur et la lecture suivant le stockage vanilla révèlent une inversion rouge/bleu. Vérifier les couleurs avec la convention de stockage native et confirmer le rendu moteur avant de présenter un lot comme validé en jeu. La conversion de stockage ne recolorie pas la peinture ; alpha et mipmaps sont conservés. Le [contrôle étendu aux cinq familles](all_asset_color_layout_2026-10-03/README.md) complète la première passe limitée aux quatre bâtiments : 38 autres DDS convertis, sans changement artistique ou de gameplay. Les textures déjà natives ou compressées ne sont pas reconverties.

Les chemins de livraison proposés sont dans le [manifeste du lot](ASSET4_FIRST_BATCH_2026-10-01.json). Ils sont vérifiés comme encore inutilisés ; ils ne sont pas déjà branchés dans les définitions.

## 5. Premier lot proposé : calcaire–ciment et trois unités

**14 fichiers finaux : 2 biens, 2 bâtiments, 2 technologies, 5 PM et 3 unités.** Un PM est une variante dérivée ; cela ne demande pas 14 compositions entièrement indépendantes. Treize objets sont encore provisoires ; la cimenterie remplace un réemploi vanilla de fonderie, présent mais peu spécifique au sujet.

Ce choix termine une petite chaîne productive de bout en bout, fournit une série de PM comparable et supprime les trois cerfs militaires. Le visuel « Pics et pelles » de la carrière est déjà un réemploi cohérent : il n'est pas commandé une seconde fois. Aucun asset de laboratoire existant n'est refait et aucune image de la chaîne cuivre n'entre dans le lot.

| Ordre | Famille | Sujet | Composition à créer |
|---:|---|---|---|
| 1, pilote | Bien | Ciment | Sac de toile ouvert et poudre gris chaud ; un groupe compact, sans étiquette. |
| 2, pilote | Bâtiment | Carrière de calcaire | Site clair à gradins, équipements discrets ; bloc calcaire dominant en bas à droite. |
| 3, pilote | Technologie | Ciments hydrauliques | Échantillon durci à moitié immergé et truelle : exprimer la prise dans l'eau. |
| 4, pilote | PM | Concassage et criblage | Mâchoires et crible simplifiés, ocre mat en bas-relief, sans scène. |
| 5, pilote | Unité | Infanterie à mousquet | Deux ou trois soldats, un geste de recharge ou d'avance dominant, mousquets lisibles ; pas la même image que l'infanterie de ligne. |
| 6 | Bien | Calcaire | Blocs ivoire/ocre clair, grain mat et poreux ; ne pas évoquer un sac de poudre ou des cristaux de sel. |
| 7 | Bâtiment | Cimenterie | Fours fixes maçonnés et atelier, calcaire près du four ; ciment au premier plan. Pas d'usine contemporaine. |
| 8 | Technologie | Ciment Portland | Clinker, broyage et petit échantillon ; fabrication différente de la prise hydraulique. |
| 9, dérivé | PM | Pierre brute | Variante du concassage barrée, même silhouette/palette, état sans traitement. |
| 10 | PM | Procédé de ciment naturel | Four fixe et roche, pictogramme compact. |
| 11 | PM | Procédé de ciment hydraulique | Même famille de four, échantillon et grande goutte distinctive. |
| 12 | PM | Procédé du ciment Portland | Même famille de four, clinker ou roue de broyage distinctive ; aucun chiffre de niveau. |
| 13 | Unité | Bombarde | Pièce ancienne lourde, affût massif et servants ; poids visuel élevé et mobilité faible. |
| 14 | Unité | Canon de campagne | Grandes roues de bois, affût allongé et servants réguliers ; matériel plus mobile que la bombarde. |

Les identifiants exacts, prérequis, textures actuelles, fichiers de définition et chemins de sortie sont regroupés dans [la liste de fabrication CSV](ASSET4_FIRST_BATCH_2026-10-01.csv). Les noms affichés ne changent pas pendant ce travail visuel.

### Ordonnancement recommandé

Créer d'abord les cinq pilotes, un par famille, et les comparer aux références natives. Valider leur style **et** leur lecture réduite avant les variantes et les autres sujets. Le pilote de carrière peut définir le bloc calcaire, mais sa silhouette définitive de bien sera validée séparément au rang 6. Les trois unités formeront une série homogène après validation du pilote d'infanterie.

Ce lot est une proposition d'ordre de fabrication, pas une autorisation implicite de remplacer les fichiers de gameplay pendant la phase de conception.

## 6. Critères de réception

1. **Sujet** : identifiable sans lire le nom ; matières et procédés distincts. Les trois PM de ciment ne doivent pas paraître identiques à 32 px.
2. **Style** : comparaison côte à côte avec au moins deux fichiers natifs de la même famille. Pas de style glossy 3D pour les PM ni de médaille à la place d'une technologie.
3. **Réduction** : biens et PM contrôlés à 32 et 48 px ; technologies à 48/64 px ; bâtiments à 48/64/96 px ; unités à 96/128 px. Ces tailles sont des seuils de contrôle proposés, pas une mesure de toutes les interfaces du jeu.
4. **Fond** : transparence réelle et pas de halo sombre/clair sur les objets ; cadre des bâtiments propre ; illustrations militaires opaques. Contrôle sur damier et deux fonds d'interface.
5. **Cadrage** : éléments importants au centre, marges suffisantes pour l'interface ; pas d'arme, roue ou sac essentiel coupé. Vérifier notamment le recadrage des unités en jeu.
6. **Technique** : en-tête DDS, taille, alpha, payload et mipmaps contrôlés ; décodage indépendant du DDS final ; aucune texture manquante ni collision de nom.
7. **Intégration future** : ne changer que `texture`, `icon` ou l'illustration voulue. Ne modifier ni les recettes, ni les déblocages, ni les statistiques, ni les variantes culturelles existantes. Ne pas confondre `background` du panneau de bâtiment avec son `icon`.
8. **Provenance** : conserver les sources, références et historique de création. Les copies de mods tiers déjà présentes restent une question séparée ; leur simple présence n'est pas un statut d'original validé.
9. **Essai moteur** : contrôle après rechargement/redémarrage, dans le marché, les technologies, les bâtiments, les menus PM et les formations. Aucun essai moteur n'est revendiqué par cet audit de préparation.

## 7. Suite après le lot 1

Préparer les lots suivants selon le même ordre de vérification : phosphate/extraction, carburants raffinés/raffinerie, métrologie–données–recherche, puis transport et autres technologies provisoires. Les remplacements éventuels des copies externes seront listés par fichier distinct, pas en additionnant aveuglément les objets. Les unités culturellement spécifiques auront leurs propres briefs. Le cuivre reste hors de ce programme tant que l'utilisateur ne le réintroduit pas.

Reproduction de l'audit : `tools/asset4_style_reference_audit.py`, Python et Pillow. Le script écrit seulement les rapports ASSET4 et les planches de comparaison dans ce dossier ; les définitions et textures du jeu et du mod ne sont pas modifiées.
